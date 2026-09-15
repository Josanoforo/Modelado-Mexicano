"""`CALC-ENIF-0003` — (P3) reconciliación de la «cobertura 66.89 %» de GEN1 por
recuento y (P4) descomposición interna de `P4_10 = 1` por «ninguna vía de
ahorro en 12 meses» (ENIF 2024, `TMODULO.csv`).

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1`
(piezas P3/P4, `NC-0125`/`NC-0126`), ANTES DE LEER UN SOLO VALOR DEL
MICRODATO. Spec sellada: `forense/prereg-caja/ENIF-COBERTURA-Y-P410-spec-v1_0.md`.
Lector CSV copiado de `CALC-ENIF-0001/medidor.py`; varianza de
`CALC-EDER-0001/medidor.py`.
"""
from __future__ import annotations

import csv
import io
import zipfile

import numpy as np

SEP = "␟"


def _norm(col):
    return col.lstrip("﻿").lstrip("ï»¿").strip().upper()


def _cod(s):
    return "" if s is None else str(s).strip()


def _peso(s):
    if s is None:
        return None
    t = str(s).strip().replace(",", "")
    if not t:
        return None
    try:
        f = float(t)
    except ValueError:
        return None
    if f != f or f in (float("inf"), float("-inf")) or f <= 0:
        return None
    return f


def _abre(zf, miembro, cols):
    crudo = zf.read(miembro)
    enc = "utf-8-sig"
    try:
        txt = crudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        txt = crudo.decode("latin-1")
        enc = "latin-1"
    r = csv.reader(io.StringIO(txt, newline=""))
    try:
        cab = [_norm(c) for c in next(r)]
    except StopIteration:
        return [], 0, list(cols), enc
    idx = {c: cab.index(c) for c in cols if c in cab}
    ausentes = [c for c in cols if c not in idx]
    filas, n = [], 0
    for row in r:
        if not row:
            continue
        n += 1
        filas.append([row[idx[c]] if (c in idx and idx[c] < len(row)) else None for c in cols])
    return filas, n, ausentes, enc


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _p(d, w):
    sw = float(np.sum(w))
    if sw <= 0:
        return None
    return float(np.sum(w * d) / sw)


def _claves_diseno(estrato, upm):
    claves = np.array([f"{e}{SEP}{u}" for e, u in zip(estrato, upm)])
    upm_unicas, inverso = np.unique(claves, return_inverse=True)
    estr_de_upm = np.array([k.split(SEP)[0] for k in upm_unicas])
    return upm_unicas, inverso, estr_de_upm


def _bootstrap(d, w, estrato, upm, replicas, semilla):
    n = len(estrato)
    if n == 0:
        return None, 0, 0, 0
    upm_unicas, inverso, estr_de_upm = _claves_diseno(estrato, upm)
    n_upm = len(upm_unicas)
    estratos = np.unique(estr_de_upm)
    sw = np.bincount(inverso, weights=w, minlength=n_upm)
    swd = np.bincount(inverso, weights=w * d, minlength=n_upm)
    rng = np.random.Generator(np.random.PCG64(semilla))
    a_sw, a_swd = np.zeros(replicas), np.zeros(replicas)
    n_una = 0
    for e in estratos:
        pos = np.flatnonzero(estr_de_upm == e)
        k = len(pos)
        if k == 1:
            n_una += 1
            a_sw += sw[pos[0]]
            a_swd += swd[pos[0]]
            continue
        elegidas = rng.integers(0, k, size=(replicas, k))
        a_sw += sw[pos][elegidas].sum(axis=1)
        a_swd += swd[pos][elegidas].sum(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        serie = np.where(a_sw > 0, a_swd / np.where(a_sw > 0, a_sw, 1.0), np.nan)
    return serie, len(estratos), n_upm, n_una


def _pct(serie):
    if serie is None:
        return None, None
    v = serie[~np.isnan(serie)]
    if v.size == 0:
        return None, None
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def _r2(x):
    return None if x is None else round(100.0 * x, 2)


def medir(inputs, contrato):
    par = contrato["parametros"]
    replicas = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    ref = par["referencias_gen1"]
    cod = par["codificacion"]
    INF = list(cod["informal"])
    FOR = list(cod["formal"])
    P313_CON = set(cod["p3_13_con_ss"])
    P313_SIN = str(cod["p3_13_sin_ss"])
    P313_VALIDOS = set(cod["p3_13_validos"])
    P410_VALIDOS = set(cod["p4_10_validos"])
    P410_DOM = set(cod["p4_10_dominio"])
    P313_DOM = set(cod["p3_13_dominio"])
    miembro = par["tablas"]["modulo"]

    P = "RESULT-ENIF-COB-"
    out = {P + s: None for s in par["sufijos_result"]}
    for s in par["sufijos_result"]:
        if s.startswith(("C-N-", "D-N-", "G-N-")):
            out[P + s] = 0
        elif "VEREDICTO" in s or s in ("ESTADO", "G-ENCODING-USADO", "D-METODO-IC"):
            out[P + s] = "NO-ESTIMABLE"

    def para(estado):
        out[P + "ESTADO"] = estado
        return out

    zf = zipfile.ZipFile(inputs[par["payload_id"]]["ruta_absoluta"])
    if miembro not in set(zf.namelist()):
        return para(f"NO-ESTIMABLE-MIEMBRO-AUSENTE:{miembro}")
    cols = ["P3_13", "P4_10", "FAC_PER", "EST_DIS", "UPM_DIS"] + INF + FOR
    filas, n, ausentes, enc = _abre(zf, miembro, cols)
    out[P + "G-ENCODING-USADO"] = enc
    if ausentes:
        return para(f"NO-ESTIMABLE-COLUMNA-AUSENTE:{ausentes[0]}")
    out[P + "C-N-TMODULO"] = n
    if n == 0:
        return para("NO-ESTIMABLE-UNIVERSO-VACIO")
    ci = {c: i for i, c in enumerate(cols)}

    p313 = np.array([_cod(f[ci["P3_13"]]) for f in filas])
    p410 = np.array([_cod(f[ci["P4_10"]]) for f in filas])
    wraw = [_peso(f[ci["FAC_PER"]]) for f in filas]
    w_ok = np.array([x is not None for x in wraw])
    w = np.array([x if x is not None else 0.0 for x in wraw], dtype=float)
    est = np.array([_cod(f[ci["EST_DIS"]]) for f in filas])
    upm = np.array([_cod(f[ci["UPM_DIS"]]) for f in filas])
    ninguna = np.ones(n, dtype=bool)
    for c in INF + FOR:
        ninguna &= np.array([_cod(f[ci[c]]) != "1" for f in filas])

    out[P + "C-N-FAC-PER-VALIDO"] = int(w_ok.sum())
    out[P + "G-N-SIN-FAC-PER"] = int((~w_ok).sum())
    out[P + "G-N-FUERA-DE-DOMINIO-P3-13"] = int((~np.isin(p313, list(P313_DOM))).sum())
    out[P + "G-N-FUERA-DE-DOMINIO-P4-10"] = int((~np.isin(p410, list(P410_DOM))).sum())
    for k in ("1", "2", "3", "4", "5", "8", "9"):
        out[P + f"C-N-P4-10-{k}"] = int((p410 == k).sum())

    # ── P3 · recuentos y fracciones ───────────────────────────────────────
    m17 = np.isin(p313, list(P313_VALIDOS))
    m179 = m17 | (p313 == "9")
    triple = m17 & np.isin(p410, list(P410_VALIDOS))
    out[P + "C-N-P3-13-1-7"] = int(m17.sum())
    out[P + "C-N-P3-13-9"] = int((p313 == "9").sum())
    out[P + "C-N-P3-13-BLANCO"] = int((p313 == "").sum())
    out[P + "C-N-UNIVERSO-TRIPLE"] = int(triple.sum())
    f_np = {"1-7": m17.sum() / n, "1-7-9": m179.sum() / n, "TRIPLE": triple.sum() / n}
    W = float(w[w_ok].sum())
    f_p = {k: (float(w[w_ok & m].sum()) / W if W > 0 else None)
           for k, m in (("1-7", m17), ("1-7-9", m179), ("TRIPLE", triple))}
    out[P + "C-FRAC-P3-13-1-7-NO-PONDERADA"] = _num(f_np["1-7"])
    out[P + "C-FRAC-P3-13-1-7-9-NO-PONDERADA"] = _num(f_np["1-7-9"])
    out[P + "C-FRAC-UNIVERSO-TRIPLE-NO-PONDERADA"] = _num(f_np["TRIPLE"])
    out[P + "C-FRAC-P3-13-1-7-PONDERADA"] = _num(f_p["1-7"])
    out[P + "C-FRAC-P3-13-1-7-9-PONDERADA"] = _num(f_p["1-7-9"])
    out[P + "C-FRAC-UNIVERSO-TRIPLE-PONDERADA"] = _num(f_p["TRIPLE"])
    out[P + "C-MASA-FAC-PER"] = _num(W)

    tabla = {"P3-13-1-7-NO-PONDERADA": f_np["1-7"], "P3-13-1-7-9-NO-PONDERADA": f_np["1-7-9"],
             "UNIVERSO-TRIPLE-NO-PONDERADA": f_np["TRIPLE"], "P3-13-1-7-PONDERADA": f_p["1-7"],
             "P3-13-1-7-9-PONDERADA": f_p["1-7-9"], "UNIVERSO-TRIPLE-PONDERADA": f_p["TRIPLE"]}
    out[P + "C-VEREDICTO-68-97"] = "REPRODUCE" if _r2(f_np["1-7"]) == 68.97 else "NO-REPRODUCE"
    out[P + "C-VEREDICTO-67-53"] = "REPRODUCE" if _r2(f_p["1-7"]) == 67.53 else "NO-REPRODUCE"
    out[P + "C-VEREDICTO-68-06"] = "REPRODUCE" if _r2(f_p["1-7-9"]) == 68.06 else "NO-REPRODUCE"
    calzan = [k for k, v in tabla.items() if v is not None and _r2(v) == 66.89]
    out[P + "C-VEREDICTO-66-89"] = ";".join("LOCALIZADA:" + k for k in calzan) if calzan else "NO-LOCALIZADA"
    r6 = float(ref["cobertura_propuesta_6dec"])
    if f_np["TRIPLE"] is not None and round(f_np["TRIPLE"], 6) == r6:
        out[P + "C-VEREDICTO-0-668937"] = "REPRODUCE:NO-PONDERADA"
    elif f_p["TRIPLE"] is not None and round(f_p["TRIPLE"], 6) == r6:
        out[P + "C-VEREDICTO-0-668937"] = "REPRODUCE:PONDERADA"
    else:
        out[P + "C-VEREDICTO-0-668937"] = "NO-REPRODUCE"
    out[P + "C-VEREDICTO-H1"] = ("REPRODUCIDA" if (int(triple.sum()) == int(ref["n_universo_triple"])
                                                 and n == int(ref["n_tmodulo"])) else "REFUTADA")
    esperados = {k: int(v) for k, v in ref["p4_10_conteos"].items()}
    disc = [f"{k}={out[P + f'C-N-P4-10-{k}']}!={v}" for k, v in esperados.items()
            if out[P + f"C-N-P4-10-{k}"] != v]
    if int(m17.sum()) != int(ref["n_p3_13_1_7"]):
        disc.append(f"P3-13-1-7={int(m17.sum())}!={ref['n_p3_13_1_7']}")
    out[P + "C-VEREDICTO-GUARDIAS-GEN1"] = "COINCIDEN" if not disc else "DISCORDAN:" + ";".join(disc)

    # ── P4 · descomposición de P4_10 = 1 ──────────────────────────────────
    def prop(mask, d):
        m = mask & w_ok
        if m.sum() == 0:
            return None
        return _p(d[m].astype(float), w[m])

    def ic(mask, d, pref):
        m = mask & w_ok & (est != "") & (upm != "")
        if m.sum() == 0:
            out[P + pref + "IC-LO"] = None
            out[P + pref + "IC-HI"] = None
            return 0
        serie, n_e, n_u, n_una = _bootstrap(d[m].astype(float), w[m], est[m], upm[m], replicas, semilla)
        lo, hi = _pct(serie)
        out[P + pref + "IC-LO"] = _num(lo)
        out[P + pref + "IC-HI"] = _num(hi)
        return n_una

    ning = ninguna.astype(float)
    n_una_total = 0
    for k, mask in (("1", p410 == "1"), ("2", p410 == "2"), ("3-5", np.isin(p410, ["3", "4", "5"]))):
        out[P + f"D-N-{k}"] = int((mask & w_ok).sum())
        out[P + f"D-N-NINGUNA-VIA-EN-{k}"] = int((mask & w_ok & ninguna).sum())
        out[P + f"D-P-NINGUNA-VIA-EN-{k}"] = _num(prop(mask, ning))
        if k in ("1", "2"):
            n_una_total += ic(mask, ning, f"D-P-NINGUNA-VIA-EN-{k}-")
    out[P + "D-N-NINGUNA-VIA-TOTAL"] = int((w_ok & ninguna).sum())
    out[P + "D-P-NINGUNA-VIA-TOTAL"] = _num(prop(np.ones(n, dtype=bool), ning))

    ua = {"SIN": (p313 == P313_SIN) & np.isin(p410, list(P410_VALIDOS)),
          "CON": np.isin(p313, list(P313_CON)) & np.isin(p410, list(P410_VALIDOS))}
    uno_ning = ((p410 == "1") & ninguna).astype(float)
    for k, U in ua.items():
        out[P + f"D-N-U-A-{k}"] = int((U & w_ok).sum())
        out[P + f"D-N-P410-1-{k}"] = int((U & w_ok & (p410 == "1")).sum())
        out[P + f"D-N-P410-1-NINGUNA-VIA-{k}"] = int((U & w_ok & (p410 == "1") & ninguna).sum())
        out[P + f"D-P-P410-1-NINGUNA-VIA-{k}"] = _num(prop(U, uno_ning))
        out[P + f"D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-{k}"] = _num(prop(U & (p410 == "1"), ning))
        n_una_total += ic(U & (p410 == "1"), ning, f"D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-{k}-")
        out[P + f"D-FRAC-DE-CORTO-12-QUE-ES-P410-1-NINGUNA-VIA-{k}"] = _num(
            prop(U & np.isin(p410, ["1", "2"]), uno_ning))
    out[P + "D-N-ESTRATOS-UPM-UNICA-ALGUN-IC"] = int(n_una_total)
    out[P + "D-METODO-IC"] = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_una_total > 0
                              else "IC-BOOTSTRAP-UPM-EN-ESTRATO")
    out[P + "ESTADO"] = "CALCULADO"
    return out
