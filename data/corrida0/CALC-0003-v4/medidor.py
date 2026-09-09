"""`CALC-0003-v4` — S6 **v1.3** Rama A' sobre ENNViH-1 2002: 4 celdas x brazos.

`repite_de: CALC-0003-v3`. UNICA diferencia operativa con `CALC-0003-v3`,
declarada aqui y en spec.md / spec.yaml:

    los atributos de diseno (`estrato`, `id_loc`) se toman de `c_portad.dta`
    por la llave de HOGAR (`folio`), no por la de PERSONA (`folio`, `ls`).

Por que. `c_portad.dta` es UNA FILA POR HOGAR: 8 437 folios en 8 438 filas, y
su `ls` identifica al respondente de la portada (valores 1..10, moda 1 y 2).
El join por (`folio`, `ls`) que v1/v2/v3 heredaron resuelve 7 870 de 19 804
personas en `iiib_es`; las demas se quedaban SIN estrato y SIN localidad. En
v2 eso pasaba desapercibido porque el conglomerado era el hogar y cada fila
huerfana conservaba su propio `folio`; en v3 la guardia
`RESULT-*-N-SIN-CONGLOMERADO` lo volvio numero (182 de 342 en C1-B3B, 1 655 de
3 179 en C2-B3B, 87 de 93 en C1-BX) y mostro el dano: todas las huerfanas
caian en UN conglomerado NaN que el remuestreo toma siempre entero, lo que
ESTRECHA el IC en vez de ensancharlo.

`estrato` e `id_loc` son atributos del HOGAR y son CONSTANTES dentro de
`folio` (medido: 0 folios con mas de un valor de cualquiera de los dos), asi
que la llave correcta es `folio` y la correccion no elige nada: lee el mismo
atributo por la llave a la que pertenece. Cobertura resultante ~100%.

Todo lo demas es byte por byte el de v3 -- que a su vez es el de v2 salvo el
conglomerado. `seed`, replicas, tablas, universo, estimando, ponderadores,
umbral: sin tocar. Los puntos estimados (`DELTA`, `DELTA-SENS`, `P-*`, `N-*`,
niveles de `LUGAR`) deben reproducir IDENTICOS los de v2 y v3: es el control
de regresion de spec.md §4, no un supuesto.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

Codigos: `1 = Si`, `3 = No`, `8 = NS` (solo brazo bx). NO existe el codigo `0`
(`S6 v1.3 §1`, FP-349).
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd
import pyreadstat


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _miembro(entrada, nombre):
    """Lee un `.dta` de dentro del zip resuelto por `resolver_payload`. Los
    miembros de microdato vienen en deflate normal (spec.md §7)."""
    with zipfile.ZipFile(entrada["ruta_absoluta"]) as z:
        crudo = z.read(nombre)
    df, _m = pyreadstat.read_dta(io.BytesIO(crudo))
    return df


def _llave(df, columnas):
    """S6 §3.4: `folio`/`ls` a entero ANTES de cualquier join. En los dos
    archivos de ponderador `folio` es CADENA (`%8s`) y en el microdato es
    numerico: sin esto el join da 0 filas y ningun error (spec.md §4)."""
    out = df.copy()
    for c in columnas:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").astype("Int64")
    return out


def _si_no(serie, si=1.0, no=3.0):
    """1 / 0 / NA. `8 = NS` y faltante quedan FUERA de los dos grupos."""
    v = pd.to_numeric(serie, errors="coerce").to_numpy(dtype="float64")
    out = np.full(v.shape, np.nan)
    out[v == si] = 1.0
    out[v == no] = 0.0
    return out


def _clasifica(df, tabla):
    """`LUGAR` de cuatro niveles mutuamente excluyentes (S6 §2.4), por
    `variable_id` y nunca por etiqueta (S6 §0.4)."""
    n = len(df)
    pub = np.zeros(n, dtype=bool)
    pri = np.zeros(n, dtype=bool)
    for var, clase in tabla.items():
        if var not in df.columns:
            continue
        marca = pd.to_numeric(df[var], errors="coerce").to_numpy(dtype="float64") == 1.0
        if clase == "PUBLICO":
            pub |= marca
        elif clase == "PRIVADO":
            pri |= marca
    lugar = np.full(n, "SOLO-OTRO", dtype=object)
    lugar[pub & ~pri] = "SOLO-PUBLICO"
    lugar[pri & ~pub] = "SOLO-PRIVADO"
    lugar[pub & pri] = "AMBOS"
    return lugar


def _p_pub(lugar, w, ambos_como_publico=False):
    """`P_PUB` = SOLO-PUBLICO / (SOLO-PUBLICO + SOLO-PRIVADO), ponderada.
    `AMBOS` y `SOLO-OTRO` quedan FUERA del cociente y se cuentan aparte
    (S6 §2.4). La sensibilidad de §2.4 mueve `AMBOS` al numerador y al
    denominador -- las dos se corren siempre."""
    ok = np.isfinite(w) & (w > 0)
    num = ok & (lugar == "SOLO-PUBLICO")
    den = num | (ok & (lugar == "SOLO-PRIVADO"))
    if ambos_como_publico:
        num = num | (ok & (lugar == "AMBOS"))
        den = den | (ok & (lugar == "AMBOS"))
    if not den.any():
        return None, 0
    return float(np.sum(w[num]) / np.sum(w[den])), int(den.sum())


def _boot_delta(lugar, t, w, cong, estrato, b, semilla, n_min, ambos=False):
    """IC95 percentil por bootstrap de LOCALIDADES dentro de estrato
    (S6 **v1.3** §3.5). UNICA diferencia operativa con `CALC-0003-v2`: alli
    `cong` era el hogar (`folio`); aqui es la localidad (`id_loc` de
    `c_portad.dta`), que es la unidad primaria del diseno de ENNViH y que
    `v1.2` habia dado por ausente del microdato sin verificarlo (`FP-351`).
    La forma del estimador no cambia: mismo remuestreo con reemplazo de
    conglomerados dentro de cada estrato, mismas replicas, misma `seed`,
    mismos percentiles 2.5/97.5. Cambia QUE se remuestrea, y solo eso."""
    base = np.isfinite(w) & (w > 0) & np.isfinite(t)
    if int(np.sum(base & (t == 1))) < n_min or int(np.sum(base & (t == 0))) < n_min:
        return None, None
    rng = np.random.Generator(np.random.PCG64(semilla))
    idx, orden = {}, []
    for i in np.flatnonzero(base):
        c = (estrato[i], cong[i])
        if c not in idx:
            idx[c] = []
            orden.append(c)
        idx[c].append(i)
    por_est = {}
    for e, f in orden:
        por_est.setdefault(e, []).append((e, f))
    reps = []
    for _ in range(b):
        tom = []
        for e, claves in por_est.items():
            for k in rng.integers(0, len(claves), len(claves)):
                tom.extend(idx[claves[k]])
        s = np.asarray(tom)
        p1, _ = _p_pub(lugar[s][t[s] == 1], w[s][t[s] == 1], ambos)
        p0, _ = _p_pub(lugar[s][t[s] == 0], w[s][t[s] == 0], ambos)
        if p1 is not None and p0 is not None:
            reps.append(p1 - p0)
    if len(reps) < b // 2:
        return None, None
    reps = np.asarray(reps)
    return float(np.percentile(reps, 2.5)), float(np.percentile(reps, 97.5))


def _signo(x):
    if x is None:
        return "NA"
    return "+" if x > 0 else ("-" if x < 0 else "0")


def _veredicto(delta, lo, hi):
    if delta is None or lo is None or hi is None:
        return "NO-ESTIMABLE"
    if lo > 0:
        return "CORROBORADA"
    if hi < 0:
        return "CONTRARIA"
    return "NO-DISCRIMINA"


def medir(inputs, contrato):
    p = contrato["parametros"]
    n_min, b = int(p["n_minimo_celda"]), int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    dta, pond = inputs[p["payload_microdato"]], inputs[p["payload_ponderador"]]
    M, joins = p["miembros"], {}
    out: dict[str, object] = {}

    def carga(nombre, entrada=None):
        return _llave(_miembro(entrada or dta, M[nombre]), ["folio", "ls"])

    # ── UNICA diferencia con CALC-0003 (FP-355) ─────────────────────────────
    # `c_portad.dta` trae 3 filas sin llave de join. `_llave` las vuelve <NA>,
    # `duplicated` cuenta NA == NA como repetido y el merge `validate="m:1"`
    # levanta MergeError: es exactamente lo que PARO a CALC-0003.
    #
    # NO son «filas totalmente vacias»: medido, cada una trae 8 de sus 11
    # columnas con dato (rel, reh, edo, mpio, loc, control, edad, id_loc) y le
    # faltan exactamente `folio`, `ls` y `estrato`; filas con las 11 columnas
    # vacias hay CERO. Se identifican por la LLAVE ausente -- que es lo que
    # rompe el join, y lo unico que las hace inalcanzables por construccion:
    # una fila sin `folio`/`ls` no puede casar con ninguna fila real. El
    # rotulo «vacia» filtraria CERO filas sobre este archivo.
    #
    # El filtro va ANTES de `_llave`, con la MISMA coercion que la llave usa,
    # para que lo que se descarta sea exactamente lo que el join no podria
    # resolver -- ni una fila mas.
    portad_crudo = _miembro(dta, M["c_portad"])
    _portad_leidas = int(len(portad_crudo))
    _sin_llave = (pd.to_numeric(portad_crudo["folio"], errors="coerce").isna()
                  | pd.to_numeric(portad_crudo["ls"], errors="coerce").isna())
    _portad_filtradas = int(_sin_llave.sum())
    _geo = p["cols_geografia"]           # ["edo", "mpio", "loc"]
    _cong = p["col_conglomerado"]        # "id_loc"
    portad_pers = _llave(portad_crudo[~_sin_llave], ["folio", "ls"])[
        ["folio", "ls", "estrato", _cong] + _geo]

    # ── LA UNICA DIFERENCIA OPERATIVA CON v3 ────────────────────────────────
    # `estrato` e `id_loc` son atributos del HOGAR. `c_portad` es una fila por
    # hogar y su `ls` es el respondente de la portada, NO la persona a la que
    # se le van a pegar los atributos: v1/v2/v3 unian por (folio, ls) y dejaban
    # sin diseno a ~60% de las personas, en silencio. Aqui se une por `folio`.
    # La deduplicacion es lossless y se verifica antes de aplicarla: si algun
    # folio trajera mas de un `estrato` o mas de un `id_loc`, la guardia lo
    # dice y NO se elige uno.
    _f_multi_est = int((portad_pers.groupby("folio")["estrato"].nunique() > 1).sum())
    _f_multi_cong = int((portad_pers.groupby("folio")[_cong].nunique() > 1).sum())
    portad = portad_pers.drop_duplicates(subset=["folio"])[
        ["folio", "estrato", _cong] + _geo]
    out["RESULT-COBERTURA-DISENO"] = (
        f"llave de diseno = folio (atributo de HOGAR) · c_portad: "
        f"{len(portad_pers)} filas con llave -> {len(portad)} hogares unicos "
        f"({len(portad_pers) - len(portad)} filas de mas por folio repetido, "
        f"descartadas tras verificar que no aportan otro valor) · "
        f"folios con >1 estrato: {_f_multi_est} · folios con >1 {_cong}: "
        f"{_f_multi_cong} · "
        + ("DEDUP-LOSSLESS" if (_f_multi_est == 0 and _f_multi_cong == 0)
           else "🛑 DEDUP-NO-LOSSLESS: el hogar no determina el atributo; "
                "se reporta y NO se elige uno"))

    # ── LA UNICA DIFERENCIA OPERATIVA CON v2, y sus dos guardias ────────────
    # S6 v1.3 §3.5 pre-registra conglomerado = LOCALIDAD e impone publicar el
    # conteo que decide con que llave se identifica. `loc` a secas NO es unico
    # a nivel nacional bajo la convencion INEGI (es unico dentro de municipio):
    # usarlo solo colapsaria localidades de estados distintos en un mismo
    # conglomerado. La llave que la spec congela es `id_loc`; la compuesta
    # (edo, mpio, loc) es su control. Si las dos NO particionan igual, la
    # compuesta manda -- y esto se dice en el propio RESULT, no en la prosa.
    _n_cong = int(portad[_cong].nunique())
    _n_comp = int(portad.groupby(_geo, dropna=False).ngroups)
    _n_loc_solo = int(portad[_geo[-1]].nunique())
    _n_estratos = int(portad["estrato"].nunique())
    _n_hogares = int(portad["folio"].nunique())   # == len(portad) tras dedup
    _coinciden = (_n_cong == _n_comp
                  and int((portad.groupby(_geo, dropna=False)[_cong]
                           .nunique() > 1).sum()) == 0
                  and int((portad.groupby(_cong)[_geo].nunique() > 1)
                          .any(axis=1).sum()) == 0)
    _por_est = portad.drop_duplicates(_geo).groupby("estrato").size()
    out["RESULT-CONGLOMERADO-LOCALIDAD"] = (
        f"conglomerado=LOCALIDAD por `{_cong}` (S6 v1.3 §3.5) · "
        f"{_cong}: {_n_cong} · ({', '.join(_geo)}): {_n_comp} · "
        f"{_geo[-1]} a secas: {_n_loc_solo} (NO es unico a nivel nacional: no se usa) · "
        f"estratos: {_n_estratos} · hogares: {_n_hogares} · "
        f"localidades por estrato min/max: {int(_por_est.min())}/{int(_por_est.max())} · "
        + ("BIYECCION-VERIFICADA: `{}` y la compuesta particionan IGUAL"
           .format(_cong) if _coinciden else
           "DISCREPAN: la compuesta manda (S6 v1.3 §3.5) -- ver ANIDAMIENTO"))

    # Anidamiento que el remuestreo supone: hogar dentro de localidad dentro
    # de estrato. Si se rompe, se reporta; NO se inventa un anidamiento que el
    # archivo no tiene.
    _loc_multi_est = int((portad.groupby(_cong)["estrato"].nunique() > 1).sum())
    _hog_multi_loc = int((portad_pers.groupby("folio")[_cong].nunique() > 1).sum())
    _cong_nulos = int(pd.to_numeric(portad[_cong], errors="coerce").isna().sum())
    out["RESULT-CONGLOMERADO-ANIDAMIENTO"] = (
        f"localidades que cruzan >1 estrato: {_loc_multi_est} de {_n_cong} · "
        f"hogares que cruzan >1 localidad: {_hog_multi_loc} de {_n_hogares} · "
        f"filas de c_portad con {_cong} nulo: {_cong_nulos} · "
        + ("ANIDADO" if (_loc_multi_est == 0 and _hog_multi_loc == 0
                         and _cong_nulos == 0)
           else "NO-ANIDADO: el IC95 se reporta igual y la ruptura se declara"))
    w_b3b = _llave(_miembro(pond, M["w_b3b"]), ["folio", "ls"])
    w_bx = _llave(_miembro(pond, M["w_bx"]), ["folio", "ls"])

    # Guardia de fan-out: un merge contra una tabla con llave repetida
    # MULTIPLICA filas y sube la n sin que nadie lo note. `validate="m:1"`
    # de abajo lo vuelve un error ruidoso; esto lo deja ademas medido.
    for nombre, tabla, llave in (("portad", portad, ["folio"]),
                                 ("w_b3b", w_b3b, ["folio", "ls"]),
                                 ("w_bx", w_bx, ["folio", "ls"])):
        dup = int(tabla.duplicated(subset=llave).sum())
        out[f"RESULT-LLAVE-UNICA-{nombre.upper()}"] = (
            "UNICA" if dup == 0 else f"REPETIDA ({dup} filas duplicadas)")

    # Conteo A.13 de la unica diferencia, dentro del RESULT de texto que la
    # spec YA declaraba: el conjunto de 128 ids es el mismo que el de v1.
    out["RESULT-LLAVE-UNICA-PORTAD"] = (
        f"{out['RESULT-LLAVE-UNICA-PORTAD']} (por folio) · A.13 c_portad.dta: "
        f"{_portad_leidas} filas leidas · {_portad_filtradas} filtradas por "
        f"llave (folio/ls) ausente · {len(portad_pers)} con llave · "
        f"{len(portad)} hogares al join")

    # ── Disparadores ────────────────────────────────────────────────────────
    es_b3b, es_bx = carga("iiib_es"), carga("p_es")
    es_b3b["T1"] = _si_no(es_b3b[p["var_t1"]])
    es_bx["T1"] = _si_no(es_bx[p["var_t1"]])

    ec = carga("iiib_ec")
    marcas = [pd.to_numeric(ec[v], errors="coerce") for v in p["vars_t2"] if v in ec.columns]
    mat = np.vstack([m.to_numpy(dtype="float64") for m in marcas])
    algun_si = np.nansum(mat == 1.0, axis=0) > 0
    algun_dato = np.sum(np.isfinite(mat), axis=0) > 0
    ec["T1"] = np.where(algun_si, 1.0, np.where(algun_dato, 0.0, np.nan))
    out["RESULT-T2-N-VARIABLES"] = len(marcas)

    # ── Desenlaces ──────────────────────────────────────────────────────────
    hs_b3b, hs_bx = carga("iiib_hs"), carga("p_hs")
    ce_b3b, ce_bx = carga("iiib_ce"), carga("p_ce")
    hs1 = carga("iiib_hs1")
    motivo = hs1[(pd.to_numeric(hs1[p["var_motivo_enf"]], errors="coerce") == 1)
                 | (pd.to_numeric(hs1[p["var_motivo_ope"]], errors="coerce") == 1)]
    personas_motivo = motivo[["folio", "ls"]].drop_duplicates()
    out["RESULT-DHS-N-EPISODIOS-TOTAL"] = int(len(hs1))
    out["RESULT-DHS-N-EPISODIOS-INCLUIDOS"] = int(len(motivo))
    out["RESULT-DHS-N-EPISODIOS-EXCLUIDOS"] = int(len(hs1) - len(motivo))

    def universo_hs(df, con_filtro):
        u = df[pd.to_numeric(df[p["var_hs01"]], errors="coerce") == 1].copy()
        if not con_filtro:
            return u, "SIN-FILTRO-DE-MOTIVO (no existe p_hs1.dta en el libro bx)"
        antes = len(u)
        u = u.merge(personas_motivo, on=["folio", "ls"], how="inner")
        joins["hs_x_hs1"] = (antes, len(u))
        return u, "hs01=1 Y >=1 episodio con hs08_1a o hs08_1e"

    def universo_ce(df):
        return df[pd.to_numeric(df[p["var_ce01"]], errors="coerce") == 1].copy()

    def fila(clave, disparador, universo, tabla, pesos, columnas_peso, filtro_txt):
        antes = len(universo)
        d = universo.merge(disparador[["folio", "ls", "T1"]], on=["folio", "ls"],
                           how="inner", validate="m:1")
        d = d.merge(portad[["folio", "estrato", _cong]], on=["folio"],
                    how="left", validate="m:1")
        d = d.merge(pesos, on=["folio", "ls"], how="left", validate="m:1")
        joins[clave] = (antes, len(d))
        out[f"RESULT-{clave}-N-UNIVERSO"] = int(len(d))
        out[f"RESULT-{clave}-FILTRO"] = filtro_txt
        lugar = _clasifica(d, tabla)
        t = d["T1"].to_numpy(dtype="float64")
        est = pd.to_numeric(d["estrato"], errors="coerce").to_numpy(dtype="float64")
        # Conglomerado de la celda. Una fila cuya localidad no resolvio en el
        # left-join entra al bootstrap con clave NaN y se agruparia con todas
        # las demas NaN en UN solo conglomerado -- que es exactamente el modo
        # de falla silencioso que esta guardia convierte en numero.
        cong = pd.to_numeric(d[_cong], errors="coerce").to_numpy(dtype="float64")
        out[f"RESULT-{clave}-N-CONGLOMERADOS"] = int(
            pd.Series(cong).dropna().nunique())
        out[f"RESULT-{clave}-N-SIN-CONGLOMERADO"] = int(np.sum(~np.isfinite(cong)))
        for nivel in ("SOLO-PUBLICO", "SOLO-PRIVADO", "AMBOS", "SOLO-OTRO"):
            out[f"RESULT-{clave}-N-{nivel}"] = int(np.sum(lugar == nivel))
        signos = []
        for etiqueta_w, col in columnas_peso:
            w = pd.to_numeric(d[col], errors="coerce").to_numpy(dtype="float64") \
                if col in d.columns else np.full(len(d), np.nan)
            pre = f"RESULT-{clave}-{etiqueta_w}"
            p1, n1 = _p_pub(lugar[t == 1], w[t == 1])
            p0, n0 = _p_pub(lugar[t == 0], w[t == 0])
            delta = None if (p1 is None or p0 is None) else p1 - p0
            lo, hi = _boot_delta(lugar, t, w, cong, est, b, semilla, n_min)
            s1, m1 = _p_pub(lugar[t == 1], w[t == 1], True)
            s0, m0 = _p_pub(lugar[t == 0], w[t == 0], True)
            d_sens = None if (s1 is None or s0 is None) else s1 - s0
            out[f"{pre}-P-T1"] = _num(p1)
            out[f"{pre}-P-T0"] = _num(p0)
            out[f"{pre}-DELTA"] = _num(delta)
            out[f"{pre}-IC-LO"] = _num(lo)
            out[f"{pre}-IC-HI"] = _num(hi)
            out[f"{pre}-N-T1"] = int(n1)
            out[f"{pre}-N-T0"] = int(n0)
            out[f"{pre}-DELTA-SENS"] = _num(d_sens)
            # S6 §2.4: la celda solo vale si base y sensibilidad coinciden en signo.
            coincide = (delta is not None and d_sens is not None
                        and _signo(delta) == _signo(d_sens))
            out[f"{pre}-VEREDICTO"] = (_veredicto(delta, lo, hi) if coincide
                                       else "NO-ESTIMABLE-POR-DEFINICION-INDETERMINADA")
            out[f"{pre}-N-PONDERADOR-VALIDO"] = int(np.sum(np.isfinite(w) & (w > 0)))
            signos.append(_signo(delta))
        if len(columnas_peso) == 2:
            # S6 §3.2: el brazo bx solo cuenta si los DOS ponderadores coinciden.
            out[f"RESULT-{clave}-PAREJA"] = (
                "COINCIDEN-EN-SIGNO" if signos[0] == signos[1] != "NA"
                else "NO-ESTIMABLE-PONDERADOR-INDETERMINADO")

    W3B = [("FAC3B", p["col_fac_3b"])]
    WBX = [("FAC3BPX", p["col_fac_3b_px"]), ("FAC3APX", p["col_fac_3a_px"])]
    u_hs_b3b, f_hs_b3b = universo_hs(hs_b3b, True)
    u_hs_bx, f_hs_bx = universo_hs(hs_bx, False)
    fila("C1-B3B", es_b3b, u_hs_b3b, p["tabla_A"], w_b3b, W3B, f_hs_b3b)
    fila("C1-BX", es_bx, u_hs_bx, p["tabla_B"], w_bx, WBX, f_hs_bx)
    fila("C2-B3B", es_b3b, universo_ce(ce_b3b), p["tabla_C"], w_b3b, W3B, "ce01=1")
    fila("C2-BX", es_bx, universo_ce(ce_bx), p["tabla_C"], w_bx, WBX, "ce01=1")
    fila("C3-B3B", ec, u_hs_b3b, p["tabla_A"], w_b3b, W3B, f_hs_b3b)
    fila("C4-B3B", ec, universo_ce(ce_b3b), p["tabla_C"], w_b3b, W3B, "ce01=1")

    out["RESULT-JOINS"] = "; ".join(f"{k}: {a}->{d}" for k, (a, d) in sorted(joins.items()))
    out["RESULT-VENTANAS"] = p["ventanas"]
    out["RESULT-CODIGOS-SI-NO"] = p["codigos_si_no"]
    return out
