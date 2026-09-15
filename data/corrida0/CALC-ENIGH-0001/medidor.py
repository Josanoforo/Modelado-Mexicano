"""`CALC-ENIGH-0001` -- celda de `R5.1` sobre ENIGH 2022 Nueva Serie, del lado
de la regla: proporcion ponderada de hogares con `remesas > 0`, con IC de
diseno y complemento CONTADO.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO POR `ACTO GEN2-MEDICION-DEMANDA-1` (CAJA, 15/sep/2026) EN
UN COMMIT PROPIO, ANTES DE ABRIR UN SOLO BYTE DE MICRODATO, contra el contrato
que `ACTO GEN2-SPECS-DEMANDA-1` congelo en NUBE (`spec.yaml` de este CALC y
`forense/prereg-caja/ENIGH-REMESAS-R51-spec-v1_0.md`). Probado solo contra un
payload SINTETICO con la forma que la spec declara.

Lo que decide el CODIGO y no la spec, declarado aqui para que se pueda
refutar: (1) el punto se calcula tras ordenar por la llave
`(folioviv, foliohog)` como texto -- «sumas en orden fijo de llave»; (2) el IC
se calcula sobre las filas del universo CON diseno (`est_dis` y `upm` no
vacios); si ninguna lo tiene, `NO-ESTIMABLE-DISENO-INCOMPLETO`; (3) una
guardia ESTRUCTURAL (miembro o columna ausente, llave no unica) deja el punto
y los IC en `null`, escribe el codigo `NO-ESTIMABLE-…` en los RESULT de texto
que dependen del punto y devuelve los conteos que si se alcanzaron a medir;
los enteros que no se alcanzaron a medir salen 0 SOLO cuando la propia
guardia explica ese 0 (un ZIP sin el miembro tiene 0 filas de ese miembro).
Ninguna cifra GEN1 ni de `CALC-B-0001` se teclea aqui: las referencias
llegan por `contrato["parametros"]`.
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

P = "RESULT-ENIGH-"
ZIP_ID = "enigh2022_nc_csv"
COLS = ["remesas", "factor", "est_dis", "upm", "folioviv", "foliohog"]


def medir(inputs, contrato):
    p = contrato["parametros"]
    replicas = int(p["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    tol = 1.0e-10  # espejo de `tolerancia.abs` de la spec (el contrato no la trae)
    g1 = p["valores_gen1_referencia"]
    b0 = p["valores_b0001_referencia"]
    grano = int(p["grano_gen1_decimales"])
    miembro_decl = p["miembros_zip_declarados"][0]
    llave = list(p["codificacion"]["llave_hogar"])

    out: dict[str, object] = {}

    def no_estimable(codigo: str):
        for k in ("A-P", "A-P-COMPLEMENTO", "A-IC-LO", "A-IC-HI",
                  "A-DELTA-VS-GEN1", "A-DELTA-VS-B0001", "A-DELTA-IC-VS-B0001"):
            out.setdefault(P + k, None)
        for k in ("A-SUMA-UNO", "A-METODO-IC", "A-REPRODUCE-GEN1", "A-REPLICA-B0001"):
            out.setdefault(P + k, codigo)
        for k in ("G-LLAVE-HOGAR-UNICA", "G-PERFIL-EST-DIS", "G-PERFIL-UPM"):
            out.setdefault(P + k, codigo)
        for k in ("G-N-FILAS-CONCENTRADOHOGAR", "G-N-COLUMNAS-CONCENTRADOHOGAR",
                  "G-N-NULOS-REMESAS", "G-N-EST-DIS-DISTINTOS", "G-N-UPM-DISTINTAS",
                  "G-N-ESTRATOS-UPM-UNICA", "A-N-U", "A-N-SIN-PONDERADOR",
                  "A-N-SIN-DISENO"):
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
    out[P + "G-N-COLUMNAS-CONCENTRADOHOGAR"] = ncol
    if faltan:
        return no_estimable(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{faltan[0]}")
    out[P + "G-N-FILAS-CONCENTRADOHOGAR"] = int(len(df))
    for c in ("est_dis", "upm", "folioviv", "foliohog"):
        df[c] = _texto(df[c])
    df = df.sort_values(llave, kind="stable").reset_index(drop=True)
    unica = not df.duplicated(subset=llave).any()
    out[P + "G-LLAVE-HOGAR-UNICA"] = "SI" if unica else "NO"
    if len(df) == 0:
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")
    if not unica:
        return no_estimable("NO-ESTIMABLE-LLAVE-NO-UNICA")

    rem = _flotante(df["remesas"])
    w = _flotante(df["factor"])
    n_nulos = int(np.sum(~np.isfinite(rem)))
    out[P + "G-N-NULOS-REMESAS"] = n_nulos

    # ── A · universo y embudo ─────────────────────────────────────────────
    con_w = np.isfinite(w) & (w > 0)
    out[P + "A-N-SIN-PONDERADOR"] = int(np.sum(~con_w))
    u = con_w & np.isfinite(rem)
    est, upm = df["est_dis"].to_numpy(), df["upm"].to_numpy()
    con_dis = (est != "") & (upm != "")
    out[P + "A-N-SIN-DISENO"] = int(np.sum(u & ~con_dis))
    out[P + "A-N-U"] = int(np.sum(u))
    out[P + "G-PERFIL-EST-DIS"] = _perfil(est[u])
    out[P + "G-PERFIL-UPM"] = _perfil(upm[u])
    n_estr, n_upm, n_una = _conteo_upm_unica(est[u & con_dis], upm[u & con_dis])
    out[P + "G-N-EST-DIS-DISTINTOS"] = n_estr
    out[P + "G-N-UPM-DISTINTAS"] = n_upm
    out[P + "G-N-ESTRATOS-UPM-UNICA"] = n_una
    out[P + "A-HOGARES-EXPANDIDOS"] = _num(np.sum(w[u])) if u.any() else 0.0
    if n_nulos > 0:
        return no_estimable("NO-ESTIMABLE-NULOS-INESPERADOS")
    if not u.any():
        return no_estimable("NO-ESTIMABLE-UNIVERSO-VACIO")

    wu, ru = w[u], rem[u]
    d1 = (ru > 0).astype("float64")
    d0 = (ru == 0).astype("float64")
    sw = float(np.sum(wu))
    punto = float(np.sum(wu * d1) / sw)
    compl = float(np.sum(wu * d0) / sw)
    out[P + "A-P"] = _num(punto)
    out[P + "A-P-COMPLEMENTO"] = _num(compl)
    residuo = punto + compl - 1.0
    out[P + "A-SUMA-UNO"] = "SI" if abs(residuo) <= tol else f"NO:{residuo!r}"

    # ── A · IC de diseno ──────────────────────────────────────────────────
    m = u & con_dis
    if not m.any():
        lo = hi = None
        metodo = "NO-ESTIMABLE-DISENO-INCOMPLETO"
    else:
        serie, _e, _n, n_una_ic = _bootstrap(w[m] * (rem[m] > 0).astype("float64"),
                                             w[m], est[m], upm[m], replicas, semilla)
        lo, hi = _ic(serie, replicas)
        metodo = "IC-DE-DISENO" if n_una_ic == 0 else "IC-CON-ESTRATOS-DE-UPM-UNICA"
    out[P + "A-IC-LO"] = _num(lo)
    out[P + "A-IC-HI"] = _num(hi)
    out[P + "A-METODO-IC"] = metodo

    # ── A · comparaciones que no se colapsan ──────────────────────────────
    out[P + "A-DELTA-VS-GEN1"] = _num(punto - float(g1["A_P"]))
    reproduce = round(punto, grano) == round(float(g1["A_P"]), grano)
    out[P + "A-REPRODUCE-GEN1"] = "REPRODUCE" if reproduce else "NO-REPRODUCE"
    delta_b = punto - float(b0["P"])
    out[P + "A-DELTA-VS-B0001"] = _num(delta_b)
    out[P + "A-REPLICA-B0001"] = "REPLICA-RESULTADO" if abs(delta_b) <= tol else "NO-REPLICA"
    anch_b = float(b0["IC_HI"]) - float(b0["IC_LO"])
    out[P + "A-DELTA-IC-VS-B0001"] = _num((hi - lo) - anch_b) if lo is not None else None
    out[P + "A-ADOPCION"] = ("LISTADO-PARA-MESA-REPRODUCE" if reproduce
                             else "LISTADO-PARA-MESA-NO-REPRODUCE")
    return out
