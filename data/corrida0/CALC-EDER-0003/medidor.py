"""`CALC-EDER-0003` -- celda de `R5.3` sobre EDER 2017: tipo de la PRIMERA
union (libre / matrimonio directo), proporciones ponderadas con `factor_per`
e IC de diseno, contadas directamente; particion cerrada con el codigo 37.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO BYTE DE MICRODATO, contra el contrato
que `ACTO GEN2-SPECS-DEMANDA-1` congelo en NUBE (`spec.yaml` de este CALC y
`forense/prereg-caja/EDER-UNION-LIBRE-spec-v1_0.md`). Probado solo contra un
payload SINTETICO con la forma que la spec declara.

Lo que decide el CODIGO y no la spec, declarado aqui: (1) «primer codigo
no-cero» = en `historiavida.csv` ordenado por `(folioviv, foliohog, id_pobla,
anio_retro)` -- `anio_retro` numerico ascendente, empates en el orden del
archivo -- la primera fila cuyo `edo_civil1.strip()` no es `''` ni `'0'`; el
codigo se compara como TEXTO contra el mapa de la spec (`'1'` y `'1.0'` son
textos distintos, y `G-VEREDICTO-TIPO-CODIGO` lo declara antes); (2)
`A-N-SIN-CLASIFICAR` cuenta TODO primer codigo fuera de LIBRE y de DIRECTO
(37, disolucion pura, cualquier otro); al universo A entran LIBRE, DIRECTO y
el 37 declarado -- un codigo no previsto por el mapa queda fuera del universo
y visible en `G-SOPORTE-PRIMER-CODIGO`; (3) una persona con `factor_per` no
finito o negativo sale del universo sin RESULT propio (la spec lo nombra en
`filtros` y no lo declara como RESULT): su numero es el residuo
`A-N-PRIMER-NO-CERO - A-N-U - A-N-SIN-FACTOR-PER - A-N-FACTOR-PER-CERO -
(personas con primer codigo fuera del mapa)`; (4) `anio_nac` se toma de la
primera fila de la persona; una persona sin `anio_nac` numerico cae en un
tramo extra `SIN-ANIO-NAC` del RESULT B, que es descriptivo; (5) el IC se
calcula sobre las personas del universo CON vivienda y CON diseno; (6) una
guardia ESTRUCTURAL deja punto e IC en `null`, escribe el codigo
`NO-ESTIMABLE-…` en los RESULT de texto que dependen del punto y devuelve
los conteos alcanzados. Los conteos de referencia del censo L7 llegan por
`contrato["parametros"]`, no se teclean.
"""
# ── bloque comun de los cuatro medidores de ACTO GEN2-MEDICION-DEMANDA-1 ──
# (se deposita byte a byte en cada medidor: cada CALC es autocontenido)
from __future__ import annotations

import io
import re
import zipfile

import numpy as np
import pandas as pd

SEP = "␟"  # separador de la clave (estrato, upm); nunca aparece en un id INEGI


def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _perfil(valores) -> str:
    """'ancho=k:n_filas;...' sobre el TEXTO CRUDO de una llave opaca."""
    anchos: dict[int, int] = {}
    for v in valores:
        anchos[len(v)] = anchos.get(len(v), 0) + 1
    return ";".join(f"ancho={k}:{anchos[k]}" for k in sorted(anchos)) or "vacio"


def _norm(col: str) -> str:
    """BOM (ya decodificado en latin-1 o no), comillas y espacios fuera. La
    caja se conserva: la identidad de la columna la resuelve `_col`."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().strip('"').strip()


def _miembro(zf: zipfile.ZipFile, nombre: str):
    """Miembro del ZIP: ruta exacta, o -- si `nombre` no trae directorio --
    el UNICO miembro cuyo nombre base coincide sin distinguir caja. Dos
    candidatos no se desempatan: elegir seria elegir el dato."""
    nombres = zf.namelist()
    if nombre in nombres:
        return nombre
    if "/" not in nombre:
        cand = [n for n in nombres if n.rsplit("/", 1)[-1].lower() == nombre.lower()]
        if len(cand) == 1:
            return cand[0]
    return None


def _lee_csv(zf: zipfile.ZipFile, miembro: str, columnas: list[str],
             dtype_str=()):
    """Lee SOLO `columnas` de un CSV del ZIP. Bytes normalizados (`\\r\\n` y
    `\\r` -> `\\n`: los CSV de datos abiertos de INEGI traen terminadores
    mixtos), decodificados en latin-1 (total sobre bytes; todo campo usado es
    ASCII). Devuelve `(df, faltantes, n_columnas)`; si falta una columna
    declarada, `df` es None y `faltantes` la nombra. Las columnas se
    resuelven por nombre exacto y, si no, por sufijo (BOM pegado al primer
    nombre); la caja se compara en MAYUSCULAS."""
    crudo = zf.read(miembro).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    cabecera = [_norm(c) for c in crudo.split(b"\n", 1)[0].decode("latin-1").split(",")]
    mapa, faltantes = {}, []
    for c in columnas:
        exactos = [h for h in cabecera if h.upper() == c.upper()]
        if not exactos:
            exactos = [h for h in cabecera if h.upper().endswith(c.upper())]
        if len(exactos) != 1:
            faltantes.append(c)
        else:
            mapa[exactos[0]] = c
    if faltantes:
        return None, faltantes, len(cabecera)
    inverso = {v: k for k, v in mapa.items()}
    df = pd.read_csv(io.BytesIO(crudo), encoding="latin-1", low_memory=False,
                     dtype=str, keep_default_na=False)
    df.columns = [_norm(c) for c in df.columns]
    df = df[[inverso[c] for c in columnas]].rename(columns=mapa)
    return df, [], len(cabecera)


def _texto(serie: pd.Series) -> np.ndarray:
    """Texto crudo con `strip()`; el vacio queda vacio (nunca 'nan')."""
    return serie.fillna("").astype(str).str.strip().to_numpy()


def _flotante(serie: pd.Series) -> np.ndarray:
    """Texto -> float64; vacio o no numerico -> NaN. Nada se imputa."""
    return pd.to_numeric(serie.replace("", np.nan), errors="coerce").to_numpy("float64")


def _claves_diseno(estrato, upm):
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    return upm_unicas, inverso, estr_de_upm


def _bootstrap(num, den, estrato, upm, replicas, semilla):
    """Bootstrap de UPM CON REEMPLAZO dentro de cada estrato, conservando el
    numero de UPM por estrato; un estrato con UNA sola UPM se re-muestrea a
    si mismo (varianza cero, contado en `n_una`). Devuelve la serie de
    replicas de `sum(num)/sum(den)` sobre conglomerados ya agregados
    (numerador y denominador DE LA MISMA replica), y los conteos
    (n_estratos, n_upm, n_estratos_de_upm_unica). `num` y `den` ya vienen
    multiplicados por el ponderador."""
    n = len(estrato)
    if n == 0:
        return None, 0, 0, 0
    upm_unicas, inverso, estr_de_upm = _claves_diseno(estrato, upm)
    n_upm = len(upm_unicas)
    estratos = np.unique(estr_de_upm)
    s_num = np.bincount(inverso, weights=num, minlength=n_upm)
    s_den = np.bincount(inverso, weights=den, minlength=n_upm)
    rng = np.random.Generator(np.random.PCG64(semilla))
    a_num, a_den = np.zeros(replicas), np.zeros(replicas)
    n_una = 0
    for e in estratos:
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_una += 1
            a_num += s_num[pos[0]]
            a_den += s_den[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        a_num += s_num[pos][elegidas].sum(axis=1)
        a_den += s_den[pos][elegidas].sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        serie = np.where(a_den > 0, a_num / np.where(a_den > 0, a_den, 1.0), np.nan)
    return serie, len(estratos), n_upm, n_una


def _ic(serie, replicas):
    if serie is None:
        return None, None
    fin = serie[np.isfinite(serie)]
    if fin.size < replicas // 2:
        return None, None
    return float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5))


def _conteo_upm_unica(estrato, upm):
    if len(estrato) == 0:
        return 0, 0, 0
    _u, _i, estr_de_upm = _claves_diseno(estrato, upm)
    _e, cuenta = np.unique(estr_de_upm, return_counts=True)
    return len(_e), len(_u), int(np.sum(cuenta == 1))


# ── medicion ──────────────────────────────────────────────────────────────

P = "RESULT-EDER-UNION-"
ZIP_ID = "eder_2017_eder2017_bases_csv"
T_HV, T_ANT, T_VIV = "historiavida.csv", "antecedentes.csv", "vivienda.csv"
COLS_HV = ["edo_civil1", "anio_retro", "anio_nac", "folioviv", "foliohog", "id_pobla"]
COLS_ANT = ["factor_per", "folioviv", "foliohog", "id_pobla"]
COLS_VIV = ["est_dis", "upm", "folioviv"]
RE_ENTERO = re.compile(r"^-?\d+$")
RE_DECIMAL = re.compile(r"^-?\d+\.\d+$")


def _tramo(anio):
    if anio is None or not np.isfinite(anio):
        return "SIN-ANIO-NAC"
    if anio <= 1970:
        return "<=1970"
    if anio <= 1980:
        return "1971-1980"
    if anio <= 1990:
        return "1981-1990"
    return "1991+"


def medir(inputs, contrato):
    p = contrato["parametros"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = 1.0e-10  # espejo de `tolerancia.abs` de la spec
    mapa = p["mapa_codigos"]
    LIBRE = {str(c) for c in mapa["LIBRE"]}
    DIRECTO = {str(c) for c in mapa["DIRECTO"]}
    DISOL = {str(c) for c in mapa["DISOLUCION_NUNCA_PRIMERA"]}
    SIN_CLAS = {str(c) for c in mapa["SIN_CLASIFICAR_DECLARADO"]}
    CERO = str(mapa["CERO_ES_AUSENCIA_DE_UNION"])
    llave_p = list(p["llave_persona"])
    llave_v = str(p["llave_vivienda"])
    tramos = list(p["tramos_cohorte"])
    l7 = p["conteos_l7_referencia"]
    miembros_decl = list(p["miembros_zip_declarados"])

    out: dict[str, object] = {}
    out[P + "A-DELTA-VS-GEN1"] = "NO-APLICA-ESTIMANDO-DISTINTO"

    def no_estimable(codigo: str):
        for k in ("A-P-LIBRE", "A-P-DIRECTO", "A-IC-LIBRE-LO", "A-IC-LIBRE-HI"):
            out.setdefault(P + k, None)
        for k in ("A-SUMA-PARTICION", "A-METODO-IC", "B-COHORTE-P-LIBRE",
                  "G-LLAVE-ANTECEDENTES-TERNA-UNICA", "G-LLAVE-VIVIENDA-UNICA",
                  "G-VEREDICTO-TIPO-CODIGO", "G-SOPORTE-PRIMER-CODIGO",
                  "G-PERFIL-EST-DIS", "G-PERFIL-UPM", "A-N-COINCIDE-L7",
                  "A-CONTEOS-COINCIDEN-L7", "A-CENSURA-IZQUIERDA"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-FILAS-HISTORIAVIDA", "G-N-FILAS-ANTECEDENTES", "G-N-FILAS-VIVIENDA",
                  "G-N-ESTRATOS-UPM-UNICA", "A-N-PRIMER-NO-CERO", "A-N-U",
                  "A-N-SIN-FACTOR-PER", "A-N-FACTOR-PER-CERO", "A-N-SIN-VIVIENDA",
                  "A-N-SIN-DISENO", "A-N-LIBRE-SIN-PONDERAR", "A-N-DIRECTO-SIN-PONDERAR",
                  "A-N-SIN-CLASIFICAR"):
            out.setdefault(P + k, 0)
        out.setdefault(P + "A-PERSONAS-EXPANDIDAS", 0.0)
        out[P + "A-ADOPCION"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G · estructura ────────────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    out[P + "G-N-MIEMBROS-ZIP"] = len(zf.namelist())
    reales = {}
    for m in miembros_decl:
        r = _miembro(zf, m)
        if r is None:
            return no_estimable(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{m}")
        reales[m] = r
    hv, faltan, _n = _lee_csv(zf, reales[T_HV], COLS_HV)
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_HV}:{faltan[0]}")
    ant, faltan, _n = _lee_csv(zf, reales[T_ANT], COLS_ANT)
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_ANT}:{faltan[0]}")
    viv, faltan, _n = _lee_csv(zf, reales[T_VIV], COLS_VIV)
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_VIV}:{faltan[0]}")
    out[P + "G-N-FILAS-HISTORIAVIDA"] = int(len(hv))
    out[P + "G-N-FILAS-ANTECEDENTES"] = int(len(ant))
    out[P + "G-N-FILAS-VIVIENDA"] = int(len(viv))
    for c in ("edo_civil1", "folioviv", "foliohog", "id_pobla"):
        hv[c] = _texto(hv[c])
    for c in ("folioviv", "foliohog", "id_pobla"):
        ant[c] = _texto(ant[c])
    for c in COLS_VIV:
        viv[c] = _texto(viv[c])
    terna_unica = not ant.duplicated(subset=llave_p).any()
    viv_unica = not viv.duplicated(subset=[llave_v]).any()
    out[P + "G-LLAVE-ANTECEDENTES-TERNA-UNICA"] = "SI" if terna_unica else "NO"
    out[P + "G-LLAVE-VIVIENDA-UNICA"] = "SI" if viv_unica else "NO"

    # tipo de codigo, declarado ANTES de aplicar el mapa
    no_vacio = hv["edo_civil1"].to_numpy()
    no_vacio = no_vacio[no_vacio != ""]
    if no_vacio.size == 0:
        tipo = "MIXTA"
    elif all(RE_ENTERO.match(t) for t in no_vacio):
        tipo = "CADENA-ENTERA"
    elif all(RE_DECIMAL.match(t) for t in no_vacio):
        tipo = "CADENA-DECIMAL"
    else:
        tipo = "MIXTA"
    out[P + "G-VEREDICTO-TIPO-CODIGO"] = tipo

    # ── A · primer codigo no-cero por persona ─────────────────────────────
    hv["_anio_retro"] = _flotante(hv["anio_retro"])
    hv["_anio_nac"] = _flotante(hv["anio_nac"])
    hv["_orden"] = np.arange(len(hv))
    hv = hv.sort_values(llave_p + ["_anio_retro", "_orden"], kind="stable",
                        na_position="last").reset_index(drop=True)
    primeras = hv.groupby(llave_p, sort=True).first()  # anio_nac de la 1a fila
    hv_nc = hv[(hv["edo_civil1"] != "") & (hv["edo_civil1"] != CERO)]
    primero = hv_nc.groupby(llave_p, sort=True)["edo_civil1"].first()
    per = pd.DataFrame({"codigo": primero})
    per["anio_nac"] = primeras.loc[per.index, "_anio_nac"].to_numpy()
    per = per.reset_index().sort_values(llave_p, kind="stable").reset_index(drop=True)
    n_primer = int(len(per))
    out[P + "A-N-PRIMER-NO-CERO"] = n_primer
    d_l7 = n_primer - int(l7["primer_no_cero"])
    out[P + "A-N-COINCIDE-L7"] = "COINCIDE" if d_l7 == 0 else f"DIFIERE:{d_l7:+d}"
    vals, cnts = np.unique(per["codigo"].to_numpy(), return_counts=True)
    out[P + "G-SOPORTE-PRIMER-CODIGO"] = ";".join(f"{v}:{c}" for v, c in zip(vals, cnts)) or "vacio"
    cod = per["codigo"].to_numpy()
    es_libre = np.array([c in LIBRE for c in cod])
    es_directo = np.array([c in DIRECTO for c in cod])
    es_37 = np.array([c in SIN_CLAS for c in cod])
    es_disol = np.array([c in DISOL for c in cod])
    n_libre, n_directo = int(es_libre.sum()), int(es_directo.sum())
    n_sin = int(np.sum(~es_libre & ~es_directo))
    out[P + "A-N-LIBRE-SIN-PONDERAR"] = n_libre
    out[P + "A-N-DIRECTO-SIN-PONDERAR"] = n_directo
    out[P + "A-N-SIN-CLASIFICAR"] = n_sin
    difs = []
    for k, v in (("libre", n_libre - int(l7["union_libre_sin_ponderar"])),
                 ("directo", n_directo - int(l7["matrimonio_directo_sin_ponderar"])),
                 ("sin_clasificar", n_sin - int(l7["sin_clasificar_37"]))):
        if v != 0:
            difs.append(f"{k}{v:+d}")
    out[P + "A-CONTEOS-COINCIDEN-L7"] = "COINCIDE" if not difs else "DIFIERE:" + ",".join(difs)
    n_disol = int(es_disol.sum())
    out[P + "A-CENSURA-IZQUIERDA"] = "AUSENTE" if n_disol == 0 else f"DETECTADA:{n_disol}"
    if not terna_unica or not viv_unica:
        return no_estimable("NO-ESTIMABLE-LLAVE-NO-UNICA")
    if n_primer == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")

    # ── A · join de ponderador y de diseno ────────────────────────────────
    ant["_w"] = _flotante(ant["factor_per"])
    per = per.merge(ant[llave_p + ["_w"]], on=llave_p, how="left", sort=False,
                    indicator="_ant")
    viv2 = viv[[llave_v, "est_dis", "upm"]]
    per = per.merge(viv2, on=llave_v, how="left", sort=False, indicator="_viv")
    per = per.sort_values(llave_p, kind="stable").reset_index(drop=True)
    w = per["_w"].to_numpy("float64")
    sin_fp = (per["_ant"] != "both").to_numpy()
    out[P + "A-N-SIN-FACTOR-PER"] = int(np.sum(sin_fp))
    cero = np.isfinite(w) & (w == 0)
    out[P + "A-N-FACTOR-PER-CERO"] = int(np.sum(cero))
    en_mapa = es_libre | es_directo | es_37
    u = en_mapa & np.isfinite(w) & (w > 0)
    out[P + "A-N-U"] = int(np.sum(u))
    est = per["est_dis"].fillna("").astype(str).to_numpy()
    upm = per["upm"].fillna("").astype(str).to_numpy()
    con_viv = (per["_viv"] == "both").to_numpy()
    con_dis = con_viv & (est != "") & (upm != "")
    out[P + "A-N-SIN-VIVIENDA"] = int(np.sum(u & ~con_viv))
    out[P + "A-N-SIN-DISENO"] = int(np.sum(u & con_viv & ~con_dis))
    out[P + "G-PERFIL-EST-DIS"] = _perfil(est[u & con_viv])
    out[P + "G-PERFIL-UPM"] = _perfil(upm[u & con_viv])
    _e, _n, n_una = _conteo_upm_unica(est[u & con_dis], upm[u & con_dis])
    out[P + "G-N-ESTRATOS-UPM-UNICA"] = n_una
    out[P + "A-PERSONAS-EXPANDIDAS"] = _num(np.sum(w[u])) if u.any() else 0.0
    if not u.any():
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")

    wu = w[u]
    sw = float(np.sum(wu))
    p_libre = float(np.sum(wu * es_libre[u]) / sw)
    p_directo = float(np.sum(wu * es_directo[u]) / sw)
    p_sin = float(np.sum(wu * (~es_libre & ~es_directo)[u]) / sw)
    out[P + "A-P-LIBRE"] = _num(p_libre)
    out[P + "A-P-DIRECTO"] = _num(p_directo)
    residuo = p_libre + p_directo + p_sin - 1.0
    out[P + "A-SUMA-PARTICION"] = "SI" if abs(residuo) <= tol else f"NO:{residuo!r}"

    m = u & con_dis
    dl = es_libre.astype("float64")
    if not m.any():
        lo = hi = None
        metodo = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        serie, _e, _n, una = _bootstrap(w[m] * dl[m], w[m], est[m], upm[m], replicas, semilla)
        lo, hi = _ic(serie, replicas)
        metodo = "IC-DE-DISENO" if una == 0 else "IC-CON-ESTRATOS-DE-UPM-UNICA"
    out[P + "A-IC-LIBRE-LO"] = _num(lo)
    out[P + "A-IC-LIBRE-HI"] = _num(hi)
    out[P + "A-METODO-IC"] = metodo
    out[P + "A-ADOPCION"] = "LISTADO-PARA-MESA"

    # ── B · cohorte por anio_nac (secundario, no adoptable) ───────────────
    tramo = np.array([_tramo(a) for a in per["anio_nac"].to_numpy("float64")])
    partes = []
    for t in tramos + ["SIN-ANIO-NAC"]:
        mt = u & (tramo == t)
        n_t = int(np.sum(mt))
        if t == "SIN-ANIO-NAC" and n_t == 0:
            continue
        if n_t == 0:
            partes.append(f"{t}=null:null:null:0")
            continue
        pt = float(np.sum(w[mt] * dl[mt]) / np.sum(w[mt]))
        mtd = mt & con_dis
        if mtd.any():
            serie, _e, _n, _u1 = _bootstrap(w[mtd] * dl[mtd], w[mtd], est[mtd], upm[mtd],
                                            replicas, semilla)
            lo_t, hi_t = _ic(serie, replicas)
        else:
            lo_t = hi_t = None
        f = lambda v: "null" if v is None else f"{v:.6f}"
        partes.append(f"{t}={pt:.6f}:{f(lo_t)}:{f(hi_t)}:{n_t}")
    out[P + "B-COHORTE-P-LIBRE"] = ";".join(partes)
    return out
