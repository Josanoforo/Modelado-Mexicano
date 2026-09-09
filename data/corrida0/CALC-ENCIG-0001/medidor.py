"""`CALC-ENCIG-0001` — mordida por canal y adopción de gobierno digital, ENCIG 2025.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-ENCIG-1`, ANTES DE LEER
UN SOLO BYTE DE MICRODATO. Spec sellada que lo gobierna:
`forense/prereg-caja/ENCIG-MORDIDA-spec-v1_0.md`
(`prereg-caja-ENCIG-MORDIDA`, sha `00c7c4a6…`).

Lo unico abierto al escribir este archivo: `data/manifiesto.yaml`, el
descriptor `encig25_estructura_base_datos.pdf`, la lista de miembros del ZIP,
`data/inventario-reactivos-v1_2.tsv`, `milpa/tramite.yaml` y
`data/corrida0/demanda-*.tsv`. NINGUN `conjunto_de_datos/*.csv`.

Releva la demanda `CORR-0002` (12 RESULT). NO toca `CORR-0001`. NO cambia
ninguna cifra de `milpa/tramite.yaml`: la adopcion de P3 es CITA.
"""
from __future__ import annotations

import csv
import io
import sys
import zipfile

import numpy as np

# ── constantes de la spec congelada ───────────────────────────────────────

ZIP_ID = "encig25_base_datos_csv"
P = "RESULT-ENCIG-MOR-"

M_PER = "encig2025_01_sec1_A_3_4_5_8_9_10.csv"
M_S7 = "encig2025_04_sec_7.csv"
M_S8 = "encig2025_05_sec_8.csv"

COLS_PER = ["P8_3_1", "P8_3_2", "P8_3_3", "FAC_P18", "EST_DIS", "UPM_DIS"]
COLS_S7 = ["ID_TRA", "NT_TIPO", "N_TRA", "P7_3", "FAC_TRA", "EST_DIS",
           "UPM_DIS", "CVE_ENT", "UPM", "V_SEL", "R_ELE"]
COLS_S8 = ["ID_TRA", "P8_4", "P8_6", "FAC_P18"]

A_SOL1_UNO, A_SOL1_CERO = {1}, {2}
A_INCISOS = ["P8_3_1", "P8_3_2", "P8_3_3"]
B_UNO, B_CERO = {1}, {0}
B_PRE, B_DIG = {1}, {3, 4, 5}
B_RESIDUO = {2, 6, 7, 8, 9}
C_ADOPTA, C_NO_ADOPTA = {4, 5}, {1, 2, 6}
C_RESIDUO = {3, 7, 8, 9}
C_TIPO = 1
X_DIO_ALGO, X_NO_DIO = {2, 3, 4, 5, 6, 7}, {1}

REPLICAS = 2000
SEED = 20260909
GRANO = 6
UMBRAL = 1.0e-6

GEN1 = {
    "A-P-SOL1": 0.085118,
    "B-P-PRE-CD": 0.116000,
    "B-P-DIG-CD": 0.027358,
    "B-P-PRE-SD": 0.141041,
    "B-P-DIG-SD": 0.029868,
    "C-P-ADOPTA": 0.673393,
}
DELTA_KEY = {
    "A-P-SOL1": "DELTA-VS-GEN1-A-SOL1",
    "B-P-PRE-CD": "DELTA-VS-GEN1-B-PRE-CD",
    "B-P-DIG-CD": "DELTA-VS-GEN1-B-DIG-CD",
    "B-P-PRE-SD": "DELTA-VS-GEN1-B-PRE-SD",
    "B-P-DIG-SD": "DELTA-VS-GEN1-B-DIG-SD",
    "C-P-ADOPTA": "DELTA-VS-GEN1-C-ADOPTA",
}
ADOPCION = {
    "RES-0003": "A-P-SOL1",
    "RES-0009": "B-P-PRE-CD",
    "RES-0011": "B-P-DIG-CD",
    "RES-0013": "B-P-PRE-SD",
    "RES-0015": "B-P-DIG-SD",
    "RES-0021": "C-P-ADOPTA",
}


# ── utilidades ────────────────────────────────────────────────────────────

def _num(v):
    """`NO-ESTIMABLE` viaja como `null`, nunca como NaN ni como cadena."""
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _norm(col: str) -> str:
    """CSV de INEGI: UTF-8 con BOM, leidos en latin-1 (nunca falla; todos los
    campos de esta spec son ASCII)."""
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _codigo(s):
    """Texto -> entero, o None si blanco / `b` / no numerico.

    NUNCA imputa: lo que no es un entero es BLANCO y se cuenta aparte."""
    if s is None:
        return None
    t = s.strip()
    if not t:
        return None
    try:
        return int(t)
    except ValueError:
        return None


def _peso(s):
    """Ponderador -> float finito y > 0, o None. Cero NO es peso valido."""
    if s is None:
        return None
    t = s.strip().replace(",", "")
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")) or f <= 0:
        return None
    return f


def _llave(s):
    """`EST_DIS`/`UPM_DIS` como LLAVE DE TEXTO OPACA: se agrupa por la cadena
    cruda. Nunca a entero, nunca re-rellenada a un ancho del descriptor —
    normalizarlas partiria o fusionaria estratos en silencio (leccion de
    `ACTO GEN2-LOTE-ENVIPE-1` §3.4)."""
    if s is None:
        return None
    t = s.strip()
    return t or None


def _abre(zf, miembro, cols):
    """Lee `cols` de `miembro`. Devuelve `(filas, n_filas, ausentes)`.

    `filas` es una lista de tuplas en el orden de `cols`. Orden de archivo
    conservado: las sumas ponderadas se hacen en ORDEN FIJO DE FILA."""
    with zf.open(miembro) as fh:
        txt = io.TextIOWrapper(fh, encoding="latin-1", newline="")
        rd = csv.reader(txt)
        try:
            cab = [_norm(c) for c in next(rd)]
        except StopIteration:
            return [], 0, list(cols)
        idx, ausentes = {}, []
        for c in cols:
            if c in cab:
                idx[c] = cab.index(c)
            else:
                ausentes.append(c)
        orden = [idx.get(c) for c in cols]
        filas, n = [], 0
        for fila in rd:
            n += 1
            filas.append(tuple(
                (fila[i] if (i is not None and i < len(fila)) else None)
                for i in orden))
        return filas, n, ausentes


def _unica(claves):
    """(veredicto, n_grupos, n_filas, n_repetidas). `None` en la clave =
    fila sin llave: cuenta como fila, nunca se funde con otra."""
    vistos, repetidos = set(), set()
    n = 0
    for k in claves:
        n += 1
        if k in vistos:
            repetidos.add(k)
        else:
            vistos.add(k)
    g = len(vistos)
    ver = "UNICA" if g == n else f"NO-UNICA:{g}/{n}"
    return ver, g, n, len(repetidos)


def _p(w, d):
    """Proporcion ponderada, sumas en orden fijo de fila."""
    sw = 0.0
    swd = 0.0
    for wi, di in zip(w, d):
        sw += wi
        if di:
            swd += wi
    return (swd / sw) if sw > 0 else None, sw


def _ic(w, d, est, upm, replicas=REPLICAS, seed=SEED):
    """Bootstrap de UPM CON REEMPLAZO dentro de estrato, percentiles 2.5/97.5.

    Devuelve `(lo, hi, n_estratos, n_upm, n_estratos_upm_unica, metodo)`.
    Un estrato de UPM unica se re-muestrea a si mismo (varianza cero): NO se
    colapsa y NO se descarta. Si eso ocurre, el IC es LIMITE INFERIOR de la
    anchura verdadera."""
    cl = {}
    n_sin = 0
    for wi, di, e, u in zip(w, d, est, upm):
        if e is None or u is None:
            n_sin += 1
            continue
        a = cl.setdefault((e, u), [0.0, 0.0])
        a[0] += wi
        if di:
            a[1] += wi
    if not cl:
        return None, None, 0, 0, 0, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin

    estratos = {}
    for (e, u), (sw, swd) in cl.items():
        estratos.setdefault(e, []).append((sw, swd))
    n_est = len(estratos)
    n_upm = len(cl)
    n_unica = sum(1 for v in estratos.values() if len(v) == 1)

    orden = sorted(estratos)
    bloques = [np.asarray(estratos[e], dtype=float) for e in orden]
    rng = np.random.Generator(np.random.PCG64(seed))
    reps = np.empty(replicas, dtype=float)
    for r in range(replicas):
        tw = 0.0
        twd = 0.0
        for b in bloques:
            k = b.shape[0]
            sel = b[rng.integers(0, k, size=k)]
            tw += float(sel[:, 0].sum())
            twd += float(sel[:, 1].sum())
        reps[r] = (twd / tw) if tw > 0 else np.nan
    finitos = reps[np.isfinite(reps)]
    if finitos.size == 0:
        return None, None, n_est, n_upm, n_unica, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    lo = float(np.percentile(finitos, 2.5))
    hi = float(np.percentile(finitos, 97.5))
    met = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_unica > 0
           else "IC-BOOTSTRAP-UPM-EN-ESTRATO")
    return lo, hi, n_est, n_upm, n_unica, met, n_sin


# ── el medidor ────────────────────────────────────────────────────────────

def medir(inputs, contrato):
    R = {}

    def put(suf, val):
        R[P + suf] = val

    zf = zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"])

    # ── lectura ───────────────────────────────────────────────────────────
    per, n_per, falta_per = _abre(zf, M_PER, COLS_PER)
    s7, n_s7, falta_s7 = _abre(zf, M_S7, COLS_S7)
    s8, n_s8, falta_s8 = _abre(zf, M_S8, COLS_S8)
    ip = {c: i for i, c in enumerate(COLS_PER)}
    i7 = {c: i for i, c in enumerate(COLS_S7)}
    i8 = {c: i for i, c in enumerate(COLS_S8)}

    put("G-N-FILAS-PERSONA", n_per)
    put("G-N-FILAS-SEC7", n_s7)
    put("G-N-FILAS-SEC8", n_s8)

    ausentes = ([f"{M_PER}:{c}" for c in falta_per]
                + [f"{M_S7}:{c}" for c in falta_s7]
                + [f"{M_S8}:{c}" for c in falta_s8])

    # ── guardias de llave (G-2/G-3/G-4) ──────────────────────────────────
    if "ID_TRA" not in falta_s7 and "NT_TIPO" not in falta_s7:
        v, _, _, _ = _unica((r[i7["ID_TRA"]], r[i7["NT_TIPO"]]) for r in s7)
        put("G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA", v)
    else:
        put("G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    if "ID_TRA" not in falta_s7:
        v, _, _, rep = _unica(r[i7["ID_TRA"]] for r in s7)
        put("G-LLAVE-SEC7-IDTRA-UNICA", v)
        put("G-N-IDTRA-REPETIDOS-SEC7", rep)
    else:
        put("G-LLAVE-SEC7-IDTRA-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE")
        put("G-N-IDTRA-REPETIDOS-SEC7", 0)
    dec = ["CVE_ENT", "UPM", "V_SEL", "R_ELE", "N_TRA"]
    if not any(c in falta_s7 for c in dec):
        v, _, _, _ = _unica(tuple(r[i7[c]] for c in dec) for r in s7)
        put("G-LLAVE-SEC7-DECLARADA-UNICA", v)
    else:
        put("G-LLAVE-SEC7-DECLARADA-UNICA", "NO-ESTIMABLE-COLUMNA-AUSENTE")
    if "ID_TRA" not in falta_s8:
        v8, _, _, _ = _unica(r[i8["ID_TRA"]] for r in s8)
        put("G-LLAVE-SEC8-IDTRA-UNICA", v8)
    else:
        v8 = "NO-ESTIMABLE-COLUMNA-AUSENTE"
        put("G-LLAVE-SEC8-IDTRA-UNICA", v8)

    if ausentes:
        put("G-VEREDICTO-ESTRUCTURA", "COLUMNAS-AUSENTES:" + ";".join(ausentes))
    elif not v8.startswith("UNICA"):
        put("G-VEREDICTO-ESTRUCTURA", "JOIN-NO-EXACTO")
    elif (R[P + "G-LLAVE-SEC7-DECLARADA-UNICA"] != "UNICA"
          and R[P + "G-LLAVE-SEC7-IDTRA-NTTIPO-UNICA"] == "UNICA"):
        put("G-VEREDICTO-ESTRUCTURA",
            "DESCRIPTOR-INCOMPLETO-LLAVE-REAL-INCLUYE-NT-TIPO")
    else:
        put("G-VEREDICTO-ESTRUCTURA", "ESTRUCTURA-COMO-LA-DECLARA-EL-DESCRIPTOR")

    # ── FAMILIA A ─────────────────────────────────────────────────────────
    _familia_a(R, put, per, ip, falta_per)
    # ── FAMILIA B ─────────────────────────────────────────────────────────
    _familia_b(R, put, s7, i7, falta_s7, s8, i8, falta_s8, v8, n_s7)
    # ── FAMILIA C ─────────────────────────────────────────────────────────
    _familia_c(R, put, s7, i7, falta_s7)
    # ── FAMILIA X ─────────────────────────────────────────────────────────
    _familia_x(R, put, s8, i8, falta_s8)
    # ── control positivo y adopcion ──────────────────────────────────────
    _cierre(R, put)
    return R


def _familia_a(R, put, per, ip, falta):
    faltan = [c for c in ["P8_3_1", "FAC_P18"] if c in falta]
    if faltan:
        for s in ["A-N-U", "A-N-P831-NSNR", "A-N-P831-BLANCO",
                  "A-N-SIN-PONDERADOR", "A-N-SIN-DISENO", "A-N-U-SOLANY",
                  "A-N-SOLANY-EXCLUIDAS-POR-NSNR", "A-N-ESTRATOS", "A-N-UPM",
                  "A-N-ESTRATOS-UPM-UNICA"]:
            put(s, 0)
        for s in ["A-MASA-FAC-P18-U", "A-P-SOL1", "A-IC-LO-SOL1", "A-IC-HI-SOL1",
                  "A-P-SOLANY", "A-IC-LO-SOLANY", "A-IC-HI-SOLANY",
                  "A-DELTA-SOLANY-SOL1", "A-P-NORMAL-SOL1", "A-SUMA-SOL1",
                  "A-P-RESIDUO"]:
            put(s, None)
        put("A-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("A-VEREDICTO-EXHAUSTIVIDAD", "NO-APLICA")
        put("A-VEREDICTO", "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan))
        return

    w, d1, dn, est, upm = [], [], [], [], []
    wa, da, esta, upma = [], [], [], []
    n_nsnr = n_blanco = n_sinpond = n_solany_ex = 0
    w_res = 0.0
    for r in per:
        c1 = _codigo(r[ip["P8_3_1"]])
        pw = _peso(r[ip["FAC_P18"]])
        if c1 is None:
            n_blanco += 1
            if pw:
                w_res += pw
            continue
        if c1 not in A_SOL1_UNO and c1 not in A_SOL1_CERO:
            if c1 == 9:
                n_nsnr += 1
            if pw:
                w_res += pw
            continue
        if pw is None:
            n_sinpond += 1
            continue
        e = _llave(r[ip["EST_DIS"]]) if "EST_DIS" not in falta else None
        u = _llave(r[ip["UPM_DIS"]]) if "UPM_DIS" not in falta else None
        w.append(pw)
        d1.append(1 if c1 in A_SOL1_UNO else 0)
        dn.append(1 if c1 in A_SOL1_CERO else 0)
        est.append(e)
        upm.append(u)
        # SOLANY: si algun inciso = 1 -> 1; si los tres = 2 -> 0; si ninguno
        # es 1 y alguno es 9/blanco -> la fila SALE, contada.
        cods = [c1] + [_codigo(r[ip[c]]) if c not in falta else None
                       for c in A_INCISOS[1:]]
        if any(c == 1 for c in cods):
            wa.append(pw); da.append(1); esta.append(e); upma.append(u)
        elif all(c == 2 for c in cods):
            wa.append(pw); da.append(0); esta.append(e); upma.append(u)
        else:
            n_solany_ex += 1

    put("A-N-U", len(w))
    put("A-N-P831-NSNR", n_nsnr)
    put("A-N-P831-BLANCO", n_blanco)
    put("A-N-SIN-PONDERADOR", n_sinpond)
    put("A-N-U-SOLANY", len(wa))
    put("A-N-SOLANY-EXCLUIDAS-POR-NSNR", n_solany_ex)

    if not w:
        for s in ["A-MASA-FAC-P18-U", "A-P-SOL1", "A-IC-LO-SOL1", "A-IC-HI-SOL1",
                  "A-P-SOLANY", "A-IC-LO-SOLANY", "A-IC-HI-SOLANY",
                  "A-DELTA-SOLANY-SOL1", "A-P-NORMAL-SOL1", "A-SUMA-SOL1",
                  "A-P-RESIDUO"]:
            put(s, None)
        for s in ["A-N-SIN-DISENO", "A-N-ESTRATOS", "A-N-UPM",
                  "A-N-ESTRATOS-UPM-UNICA"]:
            put(s, 0)
        put("A-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("A-VEREDICTO-EXHAUSTIVIDAD", "NO-APLICA")
        put("A-VEREDICTO", "NO-ESTIMABLE-UNIVERSO-VACIO")
        return

    p1, sw = _p(w, d1)
    pn, _ = _p(w, dn)
    put("A-MASA-FAC-P18-U", _num(sw))
    put("A-P-SOL1", _num(p1))
    put("A-P-NORMAL-SOL1", _num(pn))
    put("A-SUMA-SOL1", _num(None if p1 is None or pn is None else p1 + pn))
    lo, hi, ne, nu, nun, met, nsin = _ic(w, d1, est, upm)
    put("A-IC-LO-SOL1", _num(lo)); put("A-IC-HI-SOL1", _num(hi))
    put("A-N-ESTRATOS", ne); put("A-N-UPM", nu)
    put("A-N-ESTRATOS-UPM-UNICA", nun); put("A-METODO-IC", met)
    put("A-N-SIN-DISENO", nsin)

    if wa:
        pa, _ = _p(wa, da)
        lo2, hi2, *_ = _ic(wa, da, esta, upma)
        put("A-P-SOLANY", _num(pa))
        put("A-IC-LO-SOLANY", _num(lo2)); put("A-IC-HI-SOLANY", _num(hi2))
        put("A-DELTA-SOLANY-SOL1",
            _num(None if pa is None or p1 is None else pa - p1))
    else:
        put("A-P-SOLANY", None); put("A-IC-LO-SOLANY", None)
        put("A-IC-HI-SOLANY", None); put("A-DELTA-SOLANY-SOL1", None)

    total = sw + w_res
    p_res = (w_res / total) if total > 0 else None
    put("A-P-RESIDUO", _num(p_res))
    put("A-VEREDICTO-EXHAUSTIVIDAD",
        "EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO" if (p_res == 0)
        else "EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE")
    put("A-VEREDICTO", "TASA-REPORTADA")


def _familia_b(R, put, s7, i7, falta7, s8, i8, falta8, v8, n_s7):
    ceros_i = ["B-N-EMPAREJADAS", "B-N-SEC7-SIN-PAREJA", "B-N-P84-BLANCO",
               "B-N-RESIDUO-CANAL", "B-N-EVENTOS-DESCARTADOS-POR-DEDUP",
               "B-N-PRE-SD", "B-N-DIG-SD", "B-N-PRE-CD", "B-N-DIG-CD",
               "B-N-ESTRATOS-PRE-SD", "B-N-UPM-PRE-SD",
               "B-N-ESTRATOS-UPM-UNICA-PRE-SD", "B-N-ESTRATOS-DIG-SD",
               "B-N-UPM-DIG-SD", "B-N-ESTRATOS-UPM-UNICA-DIG-SD"]
    nulos_f = ["B-COBERTURA", "B-P-RESIDUO-CANAL",
               "B-P-PRE-SD", "B-IC-LO-PRE-SD", "B-IC-HI-PRE-SD",
               "B-P-DIG-SD", "B-IC-LO-DIG-SD", "B-IC-HI-DIG-SD",
               "B-P-PRE-CD", "B-IC-LO-PRE-CD", "B-IC-HI-PRE-CD",
               "B-P-DIG-CD", "B-IC-LO-DIG-CD", "B-IC-HI-DIG-CD",
               "B-P-NORMAL-PRE-SD", "B-P-NORMAL-DIG-SD",
               "B-P-NORMAL-PRE-CD", "B-P-NORMAL-DIG-CD",
               "B-DIFERENCIA-PRE-DIG-SD", "B-RAZON-PRE-DIG-SD",
               "B-DIFERENCIA-PRE-DIG-CD", "B-RAZON-PRE-DIG-CD"]

    def rendirse(ver):
        for s in ceros_i:
            put(s, 0)
        for s in nulos_f:
            put(s, None)
        put("B-VEREDICTO-CANAL", "NO-APLICA")
        put("B-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("B-VEREDICTO", ver)

    faltan = ([c for c in ["ID_TRA", "P7_3", "FAC_TRA"] if c in falta7]
              + [c for c in ["ID_TRA", "P8_4"] if c in falta8])
    if faltan:
        return rendirse("NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan))
    if not v8.startswith("UNICA"):
        return rendirse("NO-ESTIMABLE-LLAVE-NO-UNICA")

    p84 = {}
    n_blanco = 0
    for r in s8:
        c = _codigo(r[i8["P8_4"]])
        k = r[i8["ID_TRA"]]
        if c is None:
            n_blanco += 1
            continue
        p84[k] = c
    put("B-N-P84-BLANCO", n_blanco)

    filas = []          # (w, d, canal, est, upm, id_tra)
    n_sin_pareja = 0
    n_emparejadas = 0
    n_res = 0
    w_res = 0.0
    for r in s7:
        k = r[i7["ID_TRA"]]
        if k not in p84:
            n_sin_pareja += 1
            continue
        n_emparejadas += 1
        c = p84[k]
        if c not in B_UNO and c not in B_CERO:
            continue
        pw = _peso(r[i7["FAC_TRA"]])
        if pw is None:
            continue
        canal = _codigo(r[i7["P7_3"]])
        e = _llave(r[i7["EST_DIS"]]) if "EST_DIS" not in falta7 else None
        u = _llave(r[i7["UPM_DIS"]]) if "UPM_DIS" not in falta7 else None
        d = 1 if c in B_UNO else 0
        if canal in B_PRE:
            filas.append((pw, d, "PRE", e, u, k))
        elif canal in B_DIG:
            filas.append((pw, d, "DIG", e, u, k))
        else:
            n_res += 1
            w_res += pw

    put("B-N-EMPAREJADAS", n_emparejadas)
    put("B-N-SEC7-SIN-PAREJA", n_sin_pareja)
    put("B-COBERTURA", _num(n_emparejadas / n_s7) if n_s7 else None)
    put("B-N-RESIDUO-CANAL", n_res)
    masa_u_b = sum(f[0] for f in filas) + w_res
    p_res = (w_res / masa_u_b) if masa_u_b > 0 else None
    put("B-P-RESIDUO-CANAL", _num(p_res))
    put("B-VEREDICTO-CANAL",
        "CANAL-DICOTOMICO-EN-EL-INSTRUMENTO" if (p_res == 0)
        else "DICOTOMIA-ES-PROPIEDAD-DEL-RECORTE")

    if not filas:
        for s in ceros_i:
            if s not in ("B-N-EMPAREJADAS", "B-N-SEC7-SIN-PAREJA",
                         "B-N-P84-BLANCO", "B-N-RESIDUO-CANAL"):
                put(s, 0)
        for s in nulos_f:
            if s not in ("B-COBERTURA", "B-P-RESIDUO-CANAL"):
                put(s, None)
        put("B-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("B-VEREDICTO", "NO-ESTIMABLE-UNIVERSO-VACIO")
        return

    # rama CD: deduplica por ID_TRA conservando la PRIMERA fila del archivo
    vistos = set()
    cd = []
    n_desc = 0
    for f in filas:
        if f[5] in vistos:
            n_desc += 1
            continue
        vistos.add(f[5])
        cd.append(f)
    put("B-N-EVENTOS-DESCARTADOS-POR-DEDUP", n_desc)

    metodos = []

    def brazo(fs, canal, suf, con_ic, con_diseno):
        sel = [f for f in fs if f[2] == canal]
        put(f"B-N-{suf}", len(sel))
        if not sel:
            put(f"B-P-{suf}", None)
            put(f"B-P-NORMAL-{suf}", None)
            if con_ic:
                put(f"B-IC-LO-{suf}", None); put(f"B-IC-HI-{suf}", None)
            if con_diseno:
                put(f"B-N-ESTRATOS-{suf}", 0); put(f"B-N-UPM-{suf}", 0)
                put(f"B-N-ESTRATOS-UPM-UNICA-{suf}", 0)
            return None
        w = [f[0] for f in sel]
        d = [f[1] for f in sel]
        nd = [1 - f[1] for f in sel]
        p, _ = _p(w, d)
        pn, _ = _p(w, nd)
        put(f"B-P-{suf}", _num(p))
        put(f"B-P-NORMAL-{suf}", _num(pn))
        if con_ic:
            lo, hi, ne, nu, nun, met, _ = _ic(w, d, [f[3] for f in sel],
                                              [f[4] for f in sel])
            put(f"B-IC-LO-{suf}", _num(lo)); put(f"B-IC-HI-{suf}", _num(hi))
            metodos.append(met)
            if con_diseno:
                put(f"B-N-ESTRATOS-{suf}", ne); put(f"B-N-UPM-{suf}", nu)
                put(f"B-N-ESTRATOS-UPM-UNICA-{suf}", nun)
        return p

    p_pre_sd = brazo(filas, "PRE", "PRE-SD", True, True)
    p_dig_sd = brazo(filas, "DIG", "DIG-SD", True, True)
    p_pre_cd = brazo(cd, "PRE", "PRE-CD", True, False)
    p_dig_cd = brazo(cd, "DIG", "DIG-CD", True, False)

    def dif_raz(a, b, suf):
        put(f"B-DIFERENCIA-PRE-DIG-{suf}",
            _num(None if a is None or b is None else a - b))
        put(f"B-RAZON-PRE-DIG-{suf}",
            _num(None if a is None or not b else a / b))

    dif_raz(p_pre_sd, p_dig_sd, "SD")
    dif_raz(p_pre_cd, p_dig_cd, "CD")

    put("B-METODO-IC",
        "IC-CON-ESTRATOS-DE-UPM-UNICA" if "IC-CON-ESTRATOS-DE-UPM-UNICA" in metodos
        else (metodos[0] if metodos else "NO-ESTIMABLE-DISENO-INCOMPLETO"))
    put("B-VEREDICTO", "TASA-REPORTADA")


def _familia_c(R, put, s7, i7, falta7):
    faltan = [c for c in ["N_TRA", "P7_3", "FAC_TRA"] if c in falta7]
    if faltan:
        for s in ["C-N-TIPO-01", "C-N-U", "C-N-RESIDUO", "C-N-SIN-PONDERADOR",
                  "C-N-ESTRATOS", "C-N-UPM", "C-N-ESTRATOS-UPM-UNICA"]:
            put(s, 0)
        for s in ["C-P-RESIDUO", "C-MASA-FAC-TRA-U", "C-P-ADOPTA",
                  "C-IC-LO-ADOPTA", "C-IC-HI-ADOPTA", "C-P-RECHAZA", "C-SUMA"]:
            put(s, None)
        put("C-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("C-VEREDICTO-EXHAUSTIVIDAD", "NO-APLICA")
        put("C-VEREDICTO", "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan))
        return

    w, d, dn, est, upm = [], [], [], [], []
    n_tipo = n_res = n_sinpond = 0
    w_res = 0.0
    for r in s7:
        if _codigo(r[i7["N_TRA"]]) != C_TIPO:
            continue
        n_tipo += 1
        canal = _codigo(r[i7["P7_3"]])
        pw = _peso(r[i7["FAC_TRA"]])
        if canal not in C_ADOPTA and canal not in C_NO_ADOPTA:
            n_res += 1
            if pw:
                w_res += pw
            continue
        if pw is None:
            n_sinpond += 1
            continue
        w.append(pw)
        d.append(1 if canal in C_ADOPTA else 0)
        dn.append(1 if canal in C_NO_ADOPTA else 0)
        est.append(_llave(r[i7["EST_DIS"]]) if "EST_DIS" not in falta7 else None)
        upm.append(_llave(r[i7["UPM_DIS"]]) if "UPM_DIS" not in falta7 else None)

    put("C-N-TIPO-01", n_tipo)
    put("C-N-U", len(w))
    put("C-N-RESIDUO", n_res)
    put("C-N-SIN-PONDERADOR", n_sinpond)

    if not w:
        for s in ["C-N-ESTRATOS", "C-N-UPM", "C-N-ESTRATOS-UPM-UNICA"]:
            put(s, 0)
        for s in ["C-P-RESIDUO", "C-MASA-FAC-TRA-U", "C-P-ADOPTA",
                  "C-IC-LO-ADOPTA", "C-IC-HI-ADOPTA", "C-P-RECHAZA", "C-SUMA"]:
            put(s, None)
        put("C-METODO-IC", "NO-ESTIMABLE-DISENO-INCOMPLETO")
        put("C-VEREDICTO-EXHAUSTIVIDAD", "NO-APLICA")
        put("C-VEREDICTO", "NO-ESTIMABLE-UNIVERSO-VACIO")
        return

    pa, sw = _p(w, d)
    pr, _ = _p(w, dn)
    put("C-MASA-FAC-TRA-U", _num(sw))
    put("C-P-ADOPTA", _num(pa))
    put("C-P-RECHAZA", _num(pr))
    put("C-SUMA", _num(None if pa is None or pr is None else pa + pr))
    lo, hi, ne, nu, nun, met, _ = _ic(w, d, est, upm)
    put("C-IC-LO-ADOPTA", _num(lo)); put("C-IC-HI-ADOPTA", _num(hi))
    put("C-N-ESTRATOS", ne); put("C-N-UPM", nu)
    put("C-N-ESTRATOS-UPM-UNICA", nun); put("C-METODO-IC", met)
    total = sw + w_res
    p_res = (w_res / total) if total > 0 else None
    put("C-P-RESIDUO", _num(p_res))
    put("C-VEREDICTO-EXHAUSTIVIDAD",
        "EXHAUSTIVAS-EN-EL-UNIVERSO-COMPLETO" if (p_res == 0)
        else "EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE")
    put("C-VEREDICTO", "TASA-REPORTADA")


def _familia_x(R, put, s8, i8, falta8):
    faltan = [c for c in ["P8_6", "FAC_P18"] if c in falta8]
    if faltan:
        put("X-N-U", 0); put("X-P-DIO-ALGO", None); put("X-P-NO-DIO-NADA", None)
        put("X-VEREDICTO-PAGO",
            "NO-ESTIMABLE-COLUMNA-AUSENTE:" + ";".join(faltan))
        return
    w, d, dn = [], [], []
    for r in s8:
        c = _codigo(r[i8["P8_6"]])
        if c not in X_DIO_ALGO and c not in X_NO_DIO:
            continue
        pw = _peso(r[i8["FAC_P18"]])
        if pw is None:
            continue
        w.append(pw)
        d.append(1 if c in X_DIO_ALGO else 0)
        dn.append(1 if c in X_NO_DIO else 0)
    put("X-N-U", len(w))
    if not w:
        put("X-P-DIO-ALGO", None); put("X-P-NO-DIO-NADA", None)
        put("X-VEREDICTO-PAGO", "NO-ESTIMABLE-UNIVERSO-VACIO")
        return
    pa, _ = _p(w, d)
    pn, _ = _p(w, dn)
    put("X-P-DIO-ALGO", _num(pa))
    put("X-P-NO-DIO-NADA", _num(pn))
    put("X-VEREDICTO-PAGO", "EL-ROTULO-PAGA-DESCRIBE-SOLICITUD-NO-PAGO")


def _cierre(R, put):
    n_ok = 0
    detalle = []
    for celda, ref in GEN1.items():
        v = R.get(P + celda)
        if v is None:
            put(DELTA_KEY[celda], None)
            detalle.append(f"{celda}=NO-COMPARABLE")
            continue
        delta = v - ref
        put(DELTA_KEY[celda], _num(delta))
        if abs(delta) <= UMBRAL:
            n_ok += 1
            detalle.append(f"{celda}=REPRODUCE")
        else:
            detalle.append(f"{celda}=NO-REPRODUCE({delta:+.9f})")
    put("REPRODUCE-GEN1", f"REPRODUCE-{n_ok}/6 · " + " · ".join(detalle))

    for res, celda in ADOPCION.items():
        v = R.get(P + celda)
        ref = GEN1[celda]
        if v is None:
            put("ADOPCION-P3-" + res, "NO-ADOPTABLE-NO-ESTIMABLE")
            continue
        d = round(v, GRANO) - ref
        put("ADOPCION-P3-" + res,
            "CANTIDAD-MEDIDA-ADOPTABLE" if d == 0
            else f"NO-ADOPTABLE-POR-GRANO:{d:+.9f}")

    residuos = [R.get(P + "A-P-RESIDUO"), R.get(P + "B-P-RESIDUO-CANAL"),
                R.get(P + "C-P-RESIDUO")]
    if all(r == 0 for r in residuos if r is not None) and any(
            r is not None for r in residuos):
        put("ADOPCION-P3-COMPLEMENTOS", "CANTIDAD-MEDIDA-ADOPTABLE")
    else:
        put("ADOPCION-P3-COMPLEMENTOS", "COMPLEMENTO-CON-DENOMINADOR-RECORTADO")
