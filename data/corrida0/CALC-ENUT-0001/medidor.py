"""`CALC-ENUT-0001` -- celda de `R5.2` sobre ENUT 2024: razon ponderada de las
horas de cuidado del hogar que aportan las mujeres 40+, con IC de diseno de
RAZON (numerador y denominador de la misma replica), share poblacional como
contexto obligatorio, y tres guardas de ponderador.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO BYTE DE MICRODATO, contra el contrato
que `ACTO GEN2-SPECS-DEMANDA-1` congelo en NUBE (`spec.yaml` de este CALC y
`forense/prereg-caja/ENUT-CUIDADO-spec-v1_0.md`). Probado solo contra un
payload SINTETICO con la forma que la spec declara.

Lo que decide el CODIGO y no la spec, declarado aqui: (1) el share
poblacional de mujeres 40+ es una proporcion de PERSONAS y se pondera con
`FAC_PER` (el ponderador de persona; es como lo publico GEN1 y lo unico que
hace comparable el 0.2657 de referencia) sobre las personas con `FAC_PER`
finito y > 0 de los hogares del universo; `FAC_HOG` sigue siendo el UNICO
ponderador de la razon; (2) `FAC_HOG` del hogar se toma de `tsdem.csv`
exigiendo que sea CONSTANTE dentro de `LLAVEHOG` (tsdem es tabla de
personas): un hogar con dos valores distintos hace PARAR la corrida con
`RuntimeError` -- es un hecho de la corrida, no una eleccion del medidor;
(3) `G-FAC-HOG-TSDEM-IGUAL-THOGAR` compara, hogar por hogar presente en
ambas tablas, con |diferencia| <= 1e-9; (4) `G-FAC-PER-NO-CONSTANTE-EN-HOGAR`
sale `CONFIRMADO` si al menos un hogar trae dos valores distintos de
`FAC_PER`, y `REFUTADO:<n>` con `n` = hogares de mas de un integrante (donde
la constancia era comprobable) si ninguno lo hace; (5) `C-P-SIN-CP` usa las
cuatro variantes `*_SIN_CP` homologas de las `*_CON_CP` declaradas y sale
`null` si alguna falta o trae nulos; `C-P-RESIDUO-15A59` sale `null` si
`CUID_INT_15A59` trae nulos; (6) los hogares del universo se ordenan por
`LLAVEHOG` como texto antes de sumar; (7) una guardia ESTRUCTURAL deja punto
e IC en `null`, escribe el codigo `NO-ESTIMABLE-…` en los RESULT de texto
que dependen del punto y devuelve los conteos alcanzados. Las referencias
GEN1 llegan por `contrato["parametros"]`, no se teclean.
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

P = "RESULT-ENUT-"
ZIP_ID = "enut2024_bd_csv"
T_TV, T_TS, T_TH = "tvar_crea.csv", "tsdem.csv", "thogar.csv"


def medir(inputs, contrato):
    p = contrato["parametros"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    g1 = p["valores_gen1_referencia"]
    grano = int(p["grano_gen1_decimales"])
    cod = p["codificacion"]
    MUJER = str(cod["sexo_mujer"])
    CORTE = float(cod["corte_edad"])
    LLAVE = str(cod["llave_hogar"])
    CON_CP = list(p["horas_cuidado_definicion"]["columnas"])
    SIN_CP = [c.replace("_CON_CP", "_SIN_CP") for c in CON_CP]
    RESIDUO = "CUID_INT_15A59"
    miembros_decl = list(p["miembros_zip_declarados"])

    out: dict[str, object] = {}
    out[P + "A-GRANO-GEN1"] = grano

    def no_estimable(codigo: str):
        for k in ("A-R", "A-IC-LO", "A-IC-HI", "A-SHARE-POBLACIONAL-MUJERES-40MAS",
                  "A-R-MENOS-SHARE-POBLACIONAL", "A-DELTA-VS-GEN1", "C-P-RESIDUO-15A59",
                  "C-P-SIN-CP", "C-DELTA-CON-CP-VS-SIN-CP"):
            out.setdefault(P + k, None)
        for k in ("A-METODO-IC", "A-REPRODUCE-GEN1", "A-N-HOGARES-COINCIDE-GEN1",
                  "G-FAC-HOG-EN-TVAR-CREA", "G-FAC-HOG-TSDEM-IGUAL-THOGAR",
                  "G-FAC-PER-NO-CONSTANTE-EN-HOGAR", "G-DISENO-CONSTANTE-EN-HOGAR",
                  "G-N-NULOS-HORAS"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-FILAS-TVAR-CREA", "G-N-COLUMNAS-TVAR-CREA", "G-N-ESTRATOS-UPM-UNICA",
                  "A-N-HOGARES", "A-N-PERSONAS", "A-N-HOGARES-CON-CARGA",
                  "A-N-HOGARES-SIN-MUJER-40MAS", "A-N-HOGARES-SIN-FAC-HOG", "A-N-UPM"):
            out.setdefault(P + k, 0)
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
    cab_tv = [_norm(c).upper() for c in zf.read(reales[T_TV]).replace(b"\r\n", b"\n")
              .replace(b"\r", b"\n").split(b"\n", 1)[0].decode("latin-1").split(",")]
    out[P + "G-N-COLUMNAS-TVAR-CREA"] = len(cab_tv)
    out[P + "G-FAC-HOG-EN-TVAR-CREA"] = "PRESENTE" if "FAC_HOG" in cab_tv else "AUSENTE"
    sin_cp_ok = all(c in cab_tv for c in SIN_CP)
    cols_tv = (CON_CP + [RESIDUO, "SEXO", "EDAD", LLAVE, "EST_DIS", "UPM_DIS", "FAC_PER"]
               + (SIN_CP if sin_cp_ok else []))
    tv, faltan, _n = _lee_csv(zf, reales[T_TV], cols_tv)
    if faltan and any(f in SIN_CP for f in faltan):
        sin_cp_ok = False
        cols_tv = [c for c in cols_tv if c not in SIN_CP]
        tv, faltan, _n = _lee_csv(zf, reales[T_TV], cols_tv)
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_TV}:{faltan[0]}")
    ts, faltan, _n = _lee_csv(zf, reales[T_TS], [LLAVE, "FAC_HOG"])
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_TS}:{faltan[0]}")
    th, faltan, _n = _lee_csv(zf, reales[T_TH], [LLAVE, "FAC_HOG"])
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{T_TH}:{faltan[0]}")
    out[P + "G-N-FILAS-TVAR-CREA"] = int(len(tv))
    for c in ("SEXO", LLAVE, "EST_DIS", "UPM_DIS"):
        tv[c] = _texto(tv[c])
    ts[LLAVE] = _texto(ts[LLAVE])
    th[LLAVE] = _texto(th[LLAVE])
    if len(tv) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")

    # nulos en las horas CON_CP: cero nunca sustituye falta de dato
    horas_cols = {c: _flotante(tv[c]) for c in CON_CP}
    nulos = {c: int(np.sum(~np.isfinite(v))) for c, v in horas_cols.items()}
    out[P + "G-N-NULOS-HORAS"] = ";".join(f"{c}:{nulos[c]}" for c in CON_CP)
    # diseno constante dentro del hogar
    nun = tv.groupby(LLAVE)[["EST_DIS", "UPM_DIS"]].nunique()
    n_no_const = int(((nun["EST_DIS"] > 1) | (nun["UPM_DIS"] > 1)).sum())
    out[P + "G-DISENO-CONSTANTE-EN-HOGAR"] = "SI" if n_no_const == 0 else f"NO:{n_no_const}"
    # FAC_PER no constante dentro del hogar (motivo de que la unidad sea hogar)
    tv["_fp"] = _flotante(tv["FAC_PER"])
    nfp = tv.groupby(LLAVE)["_fp"].nunique(dropna=False)
    tam = tv.groupby(LLAVE).size()
    n_fp_var = int((nfp > 1).sum())
    n_multi = int((tam > 1).sum())
    out[P + "G-FAC-PER-NO-CONSTANTE-EN-HOGAR"] = ("CONFIRMADO" if n_fp_var > 0
                                                 else f"REFUTADO:{n_multi}")
    # FAC_HOG: tsdem (ponderador) vs thogar (guarda)
    ts["_fh"] = _flotante(ts["FAC_HOG"])
    nfh = ts.groupby(LLAVE)["_fh"].nunique(dropna=False)
    if int((nfh > 1).sum()) > 0:
        raise RuntimeError(f"FAC_HOG no constante dentro de {int((nfh > 1).sum())} "
                           f"hogares de {T_TS}: el ponderador del hogar no esta definido")
    fh_ts = ts.groupby(LLAVE)["_fh"].first()
    th["_fh"] = _flotante(th["FAC_HOG"])
    fh_th = th.drop_duplicates(LLAVE).set_index(LLAVE)["_fh"]
    comunes = fh_ts.index.intersection(fh_th.index)
    a, b = fh_ts.loc[comunes].to_numpy(), fh_th.loc[comunes].to_numpy()
    difieren = int(np.sum(~(np.isfinite(a) & np.isfinite(b) & (np.abs(a - b) <= 1e-9))))
    out[P + "G-FAC-HOG-TSDEM-IGUAL-THOGAR"] = "IGUAL" if difieren == 0 else f"DIFIERE:{difieren}"
    for c, n in nulos.items():
        if n > 0:
            return no_estimable(f"NO-ESTIMABLE-HORAS-NULAS:{c}:{n}")
    if n_no_const > 0:
        return no_estimable("NO-ESTIMABLE-DISENO-NO-CONSTANTE")

    # ── A · personas -> hogares ───────────────────────────────────────────
    edad = _flotante(tv["EDAD"])
    horas = np.sum(np.column_stack([horas_cols[c] for c in CON_CP]), axis=1)
    mujer40 = (tv["SEXO"].to_numpy() == MUJER) & np.isfinite(edad) & (edad >= CORTE)
    tv["_h"] = horas
    tv["_hm"] = np.where(mujer40, horas, 0.0)
    tv["_m40"] = mujer40.astype(int)
    tv["_r15"] = _flotante(tv[RESIDUO])
    hog = tv.groupby(LLAVE, sort=True).agg(
        den=("_h", "sum"), num=("_hm", "sum"), n_pers=("_h", "size"),
        n_m40=("_m40", "sum"), est=("EST_DIS", "first"), upm=("UPM_DIS", "first"),
        r15=("_r15", "sum"), r15_nulos=("_r15", lambda s: int(np.sum(~np.isfinite(s.to_numpy("float64"))))),
    )
    hog["w"] = fh_ts.reindex(hog.index).to_numpy("float64")
    hog = hog.sort_index(kind="stable")
    sin_fh = hog["w"].isna().to_numpy() & ~hog.index.isin(fh_ts.index)
    out[P + "A-N-HOGARES-SIN-FAC-HOG"] = int(np.sum(sin_fh))
    w = hog["w"].to_numpy("float64")
    u = np.isfinite(w) & (w > 0)
    hog_u = hog[u]
    out[P + "A-N-HOGARES"] = int(len(hog_u))
    d_g1 = int(len(hog_u)) - int(p["n_gen1_referencia"]["hogares"])
    out[P + "A-N-HOGARES-COINCIDE-GEN1"] = "COINCIDE" if d_g1 == 0 else f"DIFIERE:{d_g1:+d}"
    out[P + "A-N-PERSONAS"] = int(hog_u["n_pers"].sum())
    out[P + "A-N-HOGARES-CON-CARGA"] = int((hog_u["den"] > 0).sum())
    out[P + "A-N-HOGARES-SIN-MUJER-40MAS"] = int((hog_u["n_m40"] == 0).sum())
    est = hog_u["est"].to_numpy(); upm = hog_u["upm"].to_numpy()
    con_dis = (est != "") & (upm != "")
    n_estr, n_upm, n_una = _conteo_upm_unica(est[con_dis], upm[con_dis])
    out[P + "A-N-UPM"] = n_upm
    out[P + "G-N-ESTRATOS-UPM-UNICA"] = n_una
    if len(hog_u) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    wu = hog_u["w"].to_numpy("float64")
    num, den = hog_u["num"].to_numpy("float64"), hog_u["den"].to_numpy("float64")
    s_den = float(np.sum(wu * den))
    if s_den <= 0:
        return no_estimable("NO-ESTIMABLE-DENOMINADOR-CERO")
    r = float(np.sum(wu * num) / s_den)
    out[P + "A-R"] = _num(r)
    if not con_dis.any():
        lo = hi = None
        metodo = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        serie, _e, _n, una = _bootstrap((wu * num)[con_dis], (wu * den)[con_dis],
                                        est[con_dis], upm[con_dis], replicas, semilla)
        lo, hi = _ic(serie, replicas)
        metodo = "IC-DE-DISENO" if una == 0 else "IC-CON-ESTRATOS-DE-UPM-UNICA"
    out[P + "A-IC-LO"] = _num(lo)
    out[P + "A-IC-HI"] = _num(hi)
    out[P + "A-METODO-IC"] = metodo

    # share poblacional de mujeres 40+ (personas, FAC_PER)
    en_u = tv[LLAVE].isin(hog_u.index).to_numpy()
    fp = tv["_fp"].to_numpy("float64")
    mp = en_u & np.isfinite(fp) & (fp > 0)
    share = float(np.sum(fp[mp] * mujer40[mp]) / np.sum(fp[mp])) if mp.any() else None
    out[P + "A-SHARE-POBLACIONAL-MUJERES-40MAS"] = _num(share)
    out[P + "A-R-MENOS-SHARE-POBLACIONAL"] = _num(r - share) if share is not None else None
    out[P + "A-DELTA-VS-GEN1"] = _num(r - float(g1["A_R"]))
    reproduce = round(r, grano) == round(float(g1["A_R"]), grano)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if reproduce else "NO-REPRODUCE"
    out[P + "A-ADOPCION"] = ("LISTADO-PARA-MESA-REPRODUCE" if reproduce
                             else "LISTADO-PARA-MESA-NO-REPRODUCE")

    # ── C · secundarios ───────────────────────────────────────────────────
    if int(hog_u["r15_nulos"].sum()) == 0:
        r15 = hog_u["r15"].to_numpy("float64")
        tot = float(np.sum(wu * (den + r15)))
        out[P + "C-P-RESIDUO-15A59"] = _num(np.sum(wu * r15) / tot) if tot > 0 else None
    else:
        out[P + "C-P-RESIDUO-15A59"] = None
    p_sin = None
    if sin_cp_ok:
        hs = {c: _flotante(tv[c]) for c in SIN_CP}
        if all(np.isfinite(v).all() for v in hs.values()):
            h_s = np.sum(np.column_stack([hs[c] for c in SIN_CP]), axis=1)
            aux = pd.DataFrame({LLAVE: tv[LLAVE].to_numpy(), "_h": h_s,
                                "_hm": np.where(mujer40, h_s, 0.0)})
            hs_hog = aux.groupby(LLAVE, sort=True).agg(den=("_h", "sum"), num=("_hm", "sum"))
            hs_hog = hs_hog.reindex(hog_u.index)
            sd = float(np.sum(wu * hs_hog["den"].to_numpy("float64")))
            p_sin = float(np.sum(wu * hs_hog["num"].to_numpy("float64")) / sd) if sd > 0 else None
    out[P + "C-P-SIN-CP"] = _num(p_sin)
    out[P + "C-DELTA-CON-CP-VS-SIN-CP"] = _num(r - p_sin) if p_sin is not None else None
    return out
