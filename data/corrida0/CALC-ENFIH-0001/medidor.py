"""`CALC-ENFIH-0001` -- celda de `R1.2` sobre ENFIH 2019: proporcion ponderada
de hogares con `C_AFORE = 1` (tenencia de Afore), con IC de diseno,
complemento CONTADO, rama B de robustez (`H_PPAL = 1`) y perfil C por
`CAT_POS` (descriptivo, no sellado).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO BYTE DE MICRODATO, contra el contrato
que `ACTO GEN2-SPECS-DEMANDA-1` congelo en NUBE (`spec.yaml` de este CALC y
`forense/prereg-caja/ENFIH-AFORE-spec-v1_0.md`). Probado solo contra un
payload SINTETICO con la forma que la spec declara.

Lo que decide el CODIGO y no la spec, declarado aqui: (1) el punto se calcula
tras ordenar por `(FOLIO, VIV_SEL, HOGAR)` como texto; (2) `C_AFORE` se
compara como codigo entero derivado del texto crudo (`'1'`, `' 1'`, `'1.0'`
son el mismo codigo) y su soporte observado se reporta como texto crudo; un
nulo o un codigo fuera de `{0, 1}` en el universo produce
`NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA`; (3) el IC se calcula sobre las filas del
universo CON diseno; (4) una guardia ESTRUCTURAL deja punto e IC en `null`,
escribe el codigo `NO-ESTIMABLE-…` en los RESULT de texto que dependen del
punto y devuelve los conteos alcanzados; (5) el perfil C reporta, por
categoria de `CAT_POS` (texto crudo), `n` sin ponderar y la tasa PONDERADA de
`C_AFORE = 1` dentro de la categoria, a seis decimales. Las referencias GEN1
llegan por `contrato["parametros"]`, no se teclean.
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


def _codigo(t: str):
    """Texto -> entero, o None si vacio / no numerico / no entero."""
    if t is None:
        return None
    t = str(t).strip()
    if not t or t.lower() == "nan":
        return None
    try:
        return int(t)
    except ValueError:
        try:
            f = float(t)
        except ValueError:
            return None
        return int(f) if f == int(f) else None


# ── medicion ──────────────────────────────────────────────────────────────

P = "RESULT-ENFIH-"
ZIP_ID = "enfih2019_bd_csv_zip"
COLS = ["C_AFORE", "FAC_HOG", "EDIS", "UPM_DIS", "H_PPAL", "CAT_POS",
        "FOLIO", "VIV_SEL", "HOGAR"]


def medir(inputs, contrato):
    p = contrato["parametros"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = 1.0e-10  # espejo de `tolerancia.abs` de la spec
    g1 = p["valores_gen1_referencia"]
    grano = int(p["grano_gen1_decimales"])
    cod = p["codificacion"]
    soporte_esperado = {int(v) for v in cod["c_afore_soporte_esperado"]}
    llave = list(cod["llave_hogar"])
    h_ppal_b = int(cod["h_ppal_robustez"])
    miembro_decl = p["tablas"]["concentradora"]

    out: dict[str, object] = {}

    def no_estimable(codigo: str):
        for k in ("A-P", "A-P-COMPLEMENTO", "A-IC-LO", "A-IC-HI", "A-DELTA-VS-GEN1",
                  "A-DELTA-IC-VS-GEN1", "B-P", "B-IC-LO", "B-IC-HI", "B-DELTA-VS-A"):
            out.setdefault(P + k, None)
        for k in ("A-SUMA-UNO", "A-METODO-IC", "A-REPRODUCE-GEN1", "G-LLAVE-HOGAR-UNICA",
                  "G-SOPORTE-C-AFORE", "G-PERFIL-EDIS", "G-PERFIL-UPM-DIS",
                  "C-PERFIL-CAT-POS"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-FILAS-CONCENTRADORA", "G-N-COLUMNAS-CONCENTRADORA",
                  "G-N-NULOS-C-AFORE", "G-N-EDIS-DISTINTOS", "G-N-UPM-DISTINTAS",
                  "G-N-ESTRATOS-UPM-UNICA", "A-N-U", "A-N-SIN-PONDERADOR",
                  "A-N-SIN-DISENO", "B-N-U"):
            out.setdefault(P + k, 0)
        out.setdefault(P + "A-HOGARES-EXPANDIDOS", 0.0)
        out[P + "A-ADOPCION"] = "NO-ADOPTABLE-NO-ESTIMABLE"
        return out

    # ── G · estructura ────────────────────────────────────────────────────
    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])
    out[P + "G-N-MIEMBROS-ZIP"] = len(zf.namelist())
    miembro = _miembro(zf, miembro_decl)
    if miembro is None:
        return no_estimable(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{miembro_decl}")
    df, faltan, ncol = _lee_csv(zf, miembro, COLS)
    out[P + "G-N-COLUMNAS-CONCENTRADORA"] = ncol
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{faltan[0]}")
    out[P + "G-N-FILAS-CONCENTRADORA"] = int(len(df))
    for c in COLS:
        df[c] = _texto(df[c])
    df = df.sort_values(llave, kind="stable").reset_index(drop=True)
    unica = not df.duplicated(subset=llave).any()
    out[P + "G-LLAVE-HOGAR-UNICA"] = "SI" if unica else "NO"
    if len(df) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    if not unica:
        return no_estimable("NO-ESTIMABLE-LLAVE-NO-UNICA")

    crudo_afore = df["C_AFORE"].to_numpy()
    vals, cnts = np.unique(crudo_afore, return_counts=True)
    out[P + "G-SOPORTE-C-AFORE"] = ";".join(f"{v if v else '<vacio>'}:{c}"
                                           for v, c in zip(vals, cnts))
    codigos = np.array([_codigo(t) for t in crudo_afore], dtype=object)
    nulo = np.array([c is None for c in codigos])
    out[P + "G-N-NULOS-C-AFORE"] = int(np.sum(nulo))

    w = _flotante(df["FAC_HOG"])
    con_w = np.isfinite(w) & (w > 0)
    out[P + "A-N-SIN-PONDERADOR"] = int(np.sum(~con_w))
    u = con_w
    est, upm = df["EDIS"].to_numpy(), df["UPM_DIS"].to_numpy()
    con_dis = (est != "") & (upm != "")
    out[P + "A-N-SIN-DISENO"] = int(np.sum(u & ~con_dis))
    out[P + "A-N-U"] = int(np.sum(u))
    out[P + "G-PERFIL-EDIS"] = _perfil(est[u])
    out[P + "G-PERFIL-UPM-DIS"] = _perfil(upm[u])
    n_estr, n_upm, n_una = _conteo_upm_unica(est[u & con_dis], upm[u & con_dis])
    out[P + "G-N-EDIS-DISTINTOS"] = n_estr
    out[P + "G-N-UPM-DISTINTAS"] = n_upm
    out[P + "G-N-ESTRATOS-UPM-UNICA"] = n_una
    out[P + "A-HOGARES-EXPANDIDOS"] = _num(np.sum(w[u])) if u.any() else 0.0
    h_ppal = np.array([_codigo(t) for t in df["H_PPAL"].to_numpy()], dtype=object)
    ub = u & np.array([c == h_ppal_b for c in h_ppal])
    out[P + "B-N-U"] = int(np.sum(ub))
    if not u.any():
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    fuera = u & (nulo | np.array([c not in soporte_esperado for c in codigos]))
    if fuera.any():
        return no_estimable("NO-ESTIMABLE-CODIGO-FUERA-DE-MAPA")

    d = np.array([1.0 if c == 1 else 0.0 for c in codigos])
    d0 = np.array([1.0 if c == 0 else 0.0 for c in codigos])

    def punto_ic(mask):
        sw = float(np.sum(w[mask]))
        if sw <= 0:
            return None, None, None, None, "NO-ESTIMABLE-UNIVERSO-VACIO"
        pt = float(np.sum(w[mask] * d[mask]) / sw)
        cp = float(np.sum(w[mask] * d0[mask]) / sw)
        m = mask & con_dis
        if not m.any():
            return pt, cp, None, None, "NO-ESTIMABLE-DISENO-INCOMPLETO"
        serie, _e, _n, una = _bootstrap(w[m] * d[m], w[m], est[m], upm[m], replicas, semilla)
        lo, hi = _ic(serie, replicas)
        return pt, cp, lo, hi, ("IC-DE-DISENO" if una == 0 else "IC-CON-ESTRATOS-DE-UPM-UNICA")

    # ── A ─────────────────────────────────────────────────────────────────
    pa, ca, lo, hi, metodo = punto_ic(u)
    out[P + "A-P"] = _num(pa)
    out[P + "A-P-COMPLEMENTO"] = _num(ca)
    residuo = pa + ca - 1.0
    out[P + "A-SUMA-UNO"] = "SI" if abs(residuo) <= tol else f"NO:{residuo!r}"
    out[P + "A-IC-LO"] = _num(lo)
    out[P + "A-IC-HI"] = _num(hi)
    out[P + "A-METODO-IC"] = metodo
    out[P + "A-DELTA-VS-GEN1"] = _num(pa - float(g1["A_P"]))
    reproduce = round(pa, grano) == round(float(g1["A_P"]), grano)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if reproduce else "NO-REPRODUCE"
    anch_g1 = float(g1["A_IC_HI"]) - float(g1["A_IC_LO"])
    out[P + "A-DELTA-IC-VS-GEN1"] = _num((hi - lo) - anch_g1) if lo is not None else None
    out[P + "A-ADOPCION"] = ("LISTADO-PARA-MESA-REPRODUCE" if reproduce
                             else "LISTADO-PARA-MESA-NO-REPRODUCE")

    # ── B · robustez H_PPAL ───────────────────────────────────────────────
    if ub.any():
        pb, _cb, lob, hib, _mb = punto_ic(ub)
    else:
        pb = lob = hib = None
    out[P + "B-P"] = _num(pb)
    out[P + "B-IC-LO"] = _num(lob)
    out[P + "B-IC-HI"] = _num(hib)
    out[P + "B-DELTA-VS-A"] = _num(pb - pa) if pb is not None else None

    # ── C · perfil por CAT_POS (descriptivo, no sellado) ──────────────────
    cat = df["CAT_POS"].to_numpy()
    partes = []
    for v in sorted(set(cat[u])):
        m = u & (cat == v)
        sw = float(np.sum(w[m]))
        tasa = float(np.sum(w[m] * d[m]) / sw) if sw > 0 else float("nan")
        partes.append(f"cat_pos={v if v else '<vacio>'}:n={int(np.sum(m))}:p={tasa:.6f}")
    out[P + "C-PERFIL-CAT-POS"] = ";".join(partes) or "vacio"
    return out
