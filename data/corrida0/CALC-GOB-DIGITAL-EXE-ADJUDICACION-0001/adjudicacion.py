#!/usr/bin/env python3
"""CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001 · piloto 3 · COMMIT-3: R y adjudicación.

Congelado por `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1` (20/sep/2026) sin abrir
ENCIG 2025; corrió sobre un R sintético (tests/test_piloto3_v11.py) y, con
ola=2023, su `cruce()` reprodujo p(a,b), n y δ sellados en
CALC-ENCIG2023-CRUCES-HISTORICOS-0002 (control de oro, no se sella).

ES EL ÚNICO CÓDIGO AUTORIZADO A AGRUPAR ENCIG 2025 POR DOS VARIABLES (E.6), y
SE NIEGA A CORRER si no existe el sello de CALC-GOB-DIGITAL-EXE-EMISIONES-0002:
exige como inputs `emisiones_resultados` y `emisiones_sello`, verifica que el
sha256 del primero es el que el sello registra, y verifica que el C2 que
recalcula (misma semilla, mismas multiplicidades) reproduce el C2 sellado a
1e-9 antes de leer una sola celda del cruce.

Reglas heredadas VERBATIM de la spec v1.0 §4 (FP-400):
  · PUNTUADA si n ≥ 200 en 2021, 2023 y 2025 (el tercero se lee AQUÍ, no en
    COMMIT-2: leerlo es agrupar 2025 por dos variables); FUERA-DE-SOPORTE global
    si fallan ≥ 5 de 15.
  · Por celda, INDECIDIBLE con las dos condiciones del programa verbatim
    (CAREO-ADV-DUELO-diseno-v2:38): «INDECIDIBLE si ambos caen dentro del IC de
    R o si |d_L−d_M| < 0.5·EE(R)», aquí L = retador, M = C2; d = |cand − R| en pp;
    EE(R) = (IC95sup − IC95inf)/3.92.
  · Un retador GANA sólo si vence a C2 en ≥ ¾ de las PUNTUADA (INDECIDIBLE no
    es vencer; el denominador son todas las PUNTUADA).
  · ΔMAE = MAE(C2) − MAE(j) sobre las PUNTUADA, en pp, con IC réplica por
    réplica (R_r, C2_r y j_r de la misma réplica).
  · B-bis (§4.2): nadie vence y límite superior de ΔMAE ≤ 0.5 pp para TODOS los
    retadores → CORROBORADA; nadie vence pero algún IC admite > 0.5 pp →
    FALSADOR-DEBIL; si ambas caben, manda FALSADOR-DEBIL; un retador vence →
    LIMITA-C2 (sólo en este desenlace, rejilla y ola); Sλ vence y S½ no, o al
    revés → SOBRE-CUANTO-ENCOGER.
  · FP-399: si las emisiones traen S2-RESERVA = RESERVA-S2, el veredicto lleva
    esa marca; no detiene.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

_AQUI = Path(__file__).resolve().parent
_MEDIDOR = _AQUI.parent / "CALC-GOB-DIGITAL-EXE-EMISIONES-0002" / "medidor.py"
_spec = importlib.util.spec_from_file_location("piloto3_medidor", _MEDIDOR)
M = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M)

CANDIDATOS = ("C2", "C1A", "C1B", "S-MEDIO", "S-LAMBDA")
RETADORES = ("S-MEDIO", "S-LAMBDA")
TOL_C2 = 1e-9


class ParoDeGuardia(RuntimeError):
    pass


def prefijo(ola: str) -> str:
    return f"RESULT-GOB-EXE15-ADJ-{ola}"


# ══════════════════════════════ guardia de sello ══════════════════════════════

def _bytes(inputs: dict, iid: str) -> bytes:
    ent = inputs.get(iid)
    if ent is None:
        raise ParoDeGuardia(f"falta el input `{iid}`: sin sello de emisiones no hay COMMIT-3.")
    raw = ent.get("bytes")
    if raw is None:
        raw = Path(ent["ruta_absoluta"]).read_bytes()
    return raw


def _guardia_sello(inputs: dict) -> dict:
    res_raw = _bytes(inputs, "emisiones_resultados")
    sello = json.loads(_bytes(inputs, "emisiones_sello").decode("utf-8"))
    esperado = sello.get("resultados.json")
    real = hashlib.sha256(res_raw).hexdigest()
    if not esperado or esperado != real:
        raise ParoDeGuardia(f"sello de emisiones no coincide: sello={esperado!r} real={real}")
    doc = json.loads(res_raw.decode("utf-8"))
    return doc.get("resultados", doc)


# ══════════════════════════════ cruce ══════════════════════════════

def cruce(frame: pd.DataFrame, repetitions: int, seed: int) -> dict:
    """Marginales (9) + 16 celdas en UNA llamada al bootstrap: mismas
    multiplicidades que `medidor.marginales()`, así que C2 se reproduce y R
    comparte réplicas con C2. Devuelve también δ(a,b) al estilo del CALC
    histórico (control de oro sobre 2023)."""
    masks, nombres = [], []
    comp = frame["_completo"]
    for a in M.EDADES:
        masks.append(comp & frame["_edad"].eq(a)); nombres.append(("EDAD", a))
    for b in M.ESCOLARIDADES:
        masks.append(comp & frame["_esc"].eq(b)); nombres.append(("ESC", b))
    masks.append(comp.copy()); nombres.append(("ALL", "ALL"))
    for a, b in M.CELDAS:
        masks.append(comp & frame["_edad"].eq(a) & frame["_esc"].eq(b)); nombres.append(("CELDA", (a, b)))
    points, boot, den = M.bootstrap(frame, masks, repetitions, seed)
    idx = {n: i for i, n in enumerate(nombres)}
    out = {"n": {}, "R": {}, "R_rep": {}, "R_ic": {}, "delta": {}, "delta_ic": {}, "C2": {}, "C2_rep": {}}
    la = {a: idx[("EDAD", a)] for a in M.EDADES}
    lb = {b: idx[("ESC", b)] for b in M.ESCOLARIDADES}
    lall = idx[("ALL", "ALL")]
    for a, b in M.CELDAS:
        i = idx[("CELDA", (a, b))]
        out["n"][(a, b)] = int(masks[i].sum())
        out["R"][(a, b)] = float(points[i])
        out["R_rep"][(a, b)] = boot[:, i]
        out["R_ic"][(a, b)] = M.resumen(float(points[i]), boot[:, i])
        comp = M._logit(points[la[a]]) + M._logit(points[lb[b]]) - M._logit(points[lall])
        comp_rep = M._logit(boot[:, la[a]]) + M._logit(boot[:, lb[b]]) - M._logit(boot[:, lall])
        out["C2"][(a, b)] = float(M._expit(comp))
        out["C2_rep"][(a, b)] = M._expit(comp_rep)
        d = float(M._logit(points[i]) - comp)
        d_rep = M._logit(boot[:, i]) - comp_rep
        out["delta"][(a, b)] = d
        out["delta_ic"][(a, b)] = M.resumen(d, d_rep)
    return out


# ══════════════════════════════ adjudicación ══════════════════════════════

def soporte(sel: dict, n25: dict) -> dict:
    est = {}
    for c in M.CELDAS:
        if c in M.FUERA_DE_SOPORTE_EX_ANTE:
            est[c] = "FUERA-DE-SOPORTE-EX-ANTE"
        elif sel[c]["n21"] >= M.N_MINIMO and sel[c]["n23"] >= M.N_MINIMO and n25[c] >= M.N_MINIMO:
            est[c] = "PUNTUADA"
        else:
            est[c] = "FUERA-DE-SOPORTE"
    fallan = sum(1 for c, e in est.items() if e == "FUERA-DE-SOPORTE")
    est["_GLOBAL"] = ("FUERA-DE-SOPORTE-GLOBAL" if fallan >= M.FUERA_DE_SOPORTE_GLOBAL_SI_FALLAN
                      else "CON-SOPORTE")
    est["_FALLAN"] = fallan
    return est


def veredicto_celda(R: float, lo: float, hi: float, c2: float, j: float) -> tuple[str, float, float]:
    """Las dos condiciones INDECIDIBLE verbatim; luego VENCE/PIERDE por |d|."""
    ee = (hi - lo) / 3.92
    d_c2 = abs(c2 - R) * 100.0
    d_j = abs(j - R) * 100.0
    ambos_dentro = (lo <= c2 <= hi) and (lo <= j <= hi)
    if ambos_dentro or abs(d_j - d_c2) < 0.5 * ee * 100.0:
        return "INDECIDIBLE", d_c2, d_j
    return ("VENCE" if d_j < d_c2 else "PIERDE"), d_c2, d_j


def adjudicar(cr: dict, emis: dict, sel: dict, ola: str) -> dict:
    P = prefijo(ola)
    PE = M.prefijo(ola)
    out = {}
    sop = soporte(sel, cr["n"])
    puntuadas = [c for c in M.CELDAS if sop[c] == "PUNTUADA"]
    out[f"{P}-SOPORTE-GLOBAL"] = sop["_GLOBAL"]
    out[f"{P}-SOPORTE-FALLAN"] = sop["_FALLAN"]
    out[f"{P}-PUNTUADAS-N"] = len(puntuadas)
    reserva_s2 = emis.get(f"{PE}-S2-RESERVA")
    out[f"{P}-S2-RESERVA"] = reserva_s2

    # C2 sellado debe reproducirse antes de leer el cruce (guardia de sello 2/2).
    max_dif = 0.0
    for a, b in M.CELDAS:
        s = emis[f"{PE}-{a}-{b}-C2-P"]
        if s is not None and math.isfinite(cr["C2"][(a, b)]):
            max_dif = max(max_dif, abs(s - cr["C2"][(a, b)]))
    if max_dif > TOL_C2:
        raise ParoDeGuardia(f"C2 recalculado no reproduce el sellado (max |dif| = {max_dif:.3e} > {TOL_C2}).")
    out[f"{P}-C2-REPRODUCE-MAX-ABS"] = max_dif

    cand_pt: dict[str, dict] = {c: {} for c in CANDIDATOS}
    cand_rep: dict[str, dict] = {c: {} for c in RETADORES + ("C2",)}
    for a, b in M.CELDAS:
        base_e = f"{PE}-{a}-{b}"
        s = sel[(a, b)]
        dbar = (s["d21"] + s["d23"]) / 2.0
        cand_pt["C2"][(a, b)] = cr["C2"][(a, b)]
        cand_pt["C1A"][(a, b)] = emis[f"{base_e}-C1A-P"]
        cand_pt["C1B"][(a, b)] = emis[f"{base_e}-C1B-P"]
        cand_pt["S-MEDIO"][(a, b)] = float(M._expit(M._logit(cr["C2"][(a, b)]) + 0.5 * s["d23"]))
        cand_pt["S-LAMBDA"][(a, b)] = float(M._expit(M._logit(cr["C2"][(a, b)]) + M.LAMBDA * dbar))
        cand_rep["C2"][(a, b)] = cr["C2_rep"][(a, b)]
        cand_rep["S-MEDIO"][(a, b)] = M._expit(M._logit(cr["C2_rep"][(a, b)]) + 0.5 * s["d23"])
        cand_rep["S-LAMBDA"][(a, b)] = M._expit(M._logit(cr["C2_rep"][(a, b)]) + M.LAMBDA * dbar)

    # Por celda: R con IC, n, soporte, veredicto de cada retador contra C2.
    vence: dict[str, int] = {j: 0 for j in RETADORES}
    indec: dict[str, int] = {j: 0 for j in RETADORES}
    for a, b in M.CELDAS:
        base = f"{P}-{a}-{b}"
        R = cr["R"][(a, b)]
        ee, lo, hi, valid = cr["R_ic"][(a, b)]
        out.update({base + "-N-2025": cr["n"][(a, b)], base + "-SOPORTE": sop[(a, b)],
                    base + "-R-P": R if math.isfinite(R) else None, base + "-R-P-EE": ee,
                    base + "-R-P-IC-LO": lo, base + "-R-P-IC-HI": hi, base + "-R-B-VALIDAS": valid,
                    base + "-DELTA-25": cr["delta"][(a, b)] if math.isfinite(cr["delta"][(a, b)]) else None})
        for cid in CANDIDATOS:
            pt = cand_pt[cid][(a, b)]
            out[f"{base}-{cid}-P"] = pt
            out[f"{base}-{cid}-D-PP"] = (abs(pt - R) * 100.0) if (pt is not None and math.isfinite(R)) else None
        for j in RETADORES:
            if sop[(a, b)] != "PUNTUADA" or lo is None:
                out[f"{base}-{j}-VS-C2"] = "NO-PUNTUADA"
                continue
            v, _, _ = veredicto_celda(R, lo, hi, cand_pt["C2"][(a, b)], cand_pt[j][(a, b)])
            out[f"{base}-{j}-VS-C2"] = v
            vence[j] += v == "VENCE"
            indec[j] += v == "INDECIDIBLE"

    # ΔMAE con IC réplica por réplica sobre las PUNTUADA.
    umbral = math.ceil(M.FRACCION_PARA_GANAR * len(puntuadas)) if puntuadas else None
    gana = {}
    dmae_hi = {}
    for j in RETADORES:
        out[f"{P}-{j}-VENCE-N"] = vence[j]
        out[f"{P}-{j}-INDECIDIBLE-N"] = indec[j]
        gana[j] = bool(puntuadas) and vence[j] >= umbral
        out[f"{P}-{j}-GANA"] = "SI" if gana[j] else "NO"
        if puntuadas:
            mae_c2 = float(np.mean([abs(cand_pt["C2"][c] - cr["R"][c]) for c in puntuadas])) * 100.0
            mae_j = float(np.mean([abs(cand_pt[j][c] - cr["R"][c]) for c in puntuadas])) * 100.0
            rep = np.mean([np.abs(cand_rep["C2"][c] - cr["R_rep"][c]) - np.abs(cand_rep[j][c] - cr["R_rep"][c])
                           for c in puntuadas], axis=0) * 100.0
            d = mae_c2 - mae_j
            ee, lo, hi, valid = M.resumen(d, rep)
            out.update({f"{P}-{j}-MAE-PP": mae_j, f"{P}-C2-MAE-PP": mae_c2, f"{P}-{j}-DELTA-MAE-PP": d,
                        f"{P}-{j}-DELTA-MAE-EE": ee, f"{P}-{j}-DELTA-MAE-IC-LO": lo,
                        f"{P}-{j}-DELTA-MAE-IC-HI": hi, f"{P}-{j}-DELTA-MAE-B-VALIDAS": valid})
            dmae_hi[j] = hi
        else:
            out.update({f"{P}-{j}-MAE-PP": None, f"{P}-C2-MAE-PP": None, f"{P}-{j}-DELTA-MAE-PP": None,
                        f"{P}-{j}-DELTA-MAE-EE": None, f"{P}-{j}-DELTA-MAE-IC-LO": None,
                        f"{P}-{j}-DELTA-MAE-IC-HI": None, f"{P}-{j}-DELTA-MAE-B-VALIDAS": 0})
            dmae_hi[j] = None
    for cid in ("C1A", "C1B"):
        out[f"{P}-{cid}-MAE-PP"] = (float(np.mean([abs(cand_pt[cid][c] - cr["R"][c]) for c in puntuadas])) * 100.0
                                    if puntuadas else None)
    out[f"{P}-UMBRAL-VENCER-N"] = umbral

    # B-bis verbatim.
    if sop["_GLOBAL"] == "FUERA-DE-SOPORTE-GLOBAL":
        b_bis = "FUERA-DE-SOPORTE-GLOBAL"
    elif gana["S-MEDIO"] and gana["S-LAMBDA"]:
        b_bis = "LIMITA-C2"
    elif gana["S-MEDIO"] or gana["S-LAMBDA"]:
        b_bis = "LIMITA-C2-SOBRE-CUANTO-ENCOGER"
    else:
        cabe_corroborada = all(dmae_hi.get(j) is not None and dmae_hi[j] <= M.DELTA_MAE_UMBRAL_PP for j in RETADORES)
        b_bis = "CORROBORADA" if cabe_corroborada else "FALSADOR-DEBIL"
    if reserva_s2 == "RESERVA-S2":
        b_bis += "+RESERVA-S2"
    out[f"{P}-B-BIS"] = b_bis
    out[f"{P}-ALCANCE"] = ("C2 sigue adoptado en DIN y TRA (A.10); este veredicto limita sólo a "
                           "gobierno_digital/luz, edad×escolaridad, ENCIG 2025")
    return out


def esquema_resultados(ola: str) -> list[dict]:
    P = prefijo(ola)
    rows = []
    def add(i, t, u): rows.append({"id": i, "tipo": t, "unidad": u})
    for k, t, u in (("SOPORTE-GLOBAL", "texto", "estado"), ("SOPORTE-FALLAN", "entero", "celdas"),
                    ("PUNTUADAS-N", "entero", "celdas"), ("S2-RESERVA", "texto", "estado"),
                    ("C2-REPRODUCE-MAX-ABS", "flotante", "proporción"), ("UMBRAL-VENCER-N", "entero", "celdas"),
                    ("C2-MAE-PP", "flotante", "pp"), ("C1A-MAE-PP", "flotante", "pp"), ("C1B-MAE-PP", "flotante", "pp"),
                    ("B-BIS", "texto", "veredicto"), ("ALCANCE", "texto", "alcance")):
        add(f"{P}-{k}", t, u)
    for j in RETADORES:
        for k, t, u in (("VENCE-N", "entero", "celdas"), ("INDECIDIBLE-N", "entero", "celdas"), ("GANA", "texto", "SI/NO"),
                        ("MAE-PP", "flotante", "pp"), ("DELTA-MAE-PP", "flotante", "pp"), ("DELTA-MAE-EE", "flotante", "pp"),
                        ("DELTA-MAE-IC-LO", "flotante", "pp"), ("DELTA-MAE-IC-HI", "flotante", "pp"),
                        ("DELTA-MAE-B-VALIDAS", "entero", "réplicas definidas")):
            add(f"{P}-{j}-{k}", t, u)
    for a, b in M.CELDAS:
        base = f"{P}-{a}-{b}"
        for k, t, u in (("N-2025", "entero", "trámites"), ("SOPORTE", "texto", "estado"), ("R-P", "proporcion", "proporción [0,1]"),
                        ("R-P-EE", "flotante", "error estándar"), ("R-P-IC-LO", "proporcion", "límite inferior IC95"),
                        ("R-P-IC-HI", "proporcion", "límite superior IC95"), ("R-B-VALIDAS", "entero", "réplicas definidas"),
                        ("DELTA-25", "flotante", "logit")):
            add(f"{base}-{k}", t, u)
        for cid in CANDIDATOS:
            add(f"{base}-{cid}-P", "proporcion", "proporción [0,1]"); add(f"{base}-{cid}-D-PP", "flotante", "|cand − R| pp")
        for j in RETADORES:
            add(f"{base}-{j}-VS-C2", "texto", "VENCE/PIERDE/INDECIDIBLE/NO-PUNTUADA")
    return rows


def medir(inputs: dict, contrato: dict) -> dict:
    """Punto de entrada del COMMIT-3. Sin sello de emisiones, no corre."""
    emis = _guardia_sello(inputs)
    M._guardia_suspensiva(inputs, contrato)
    p = contrato["parametros"]
    ola = str(p["ola"])
    repetitions = int(p["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    if int(emis.get(f"{M.prefijo(ola)}-SEED", -1)) != seed or int(emis.get(f"{M.prefijo(ola)}-BOOTSTRAP-REPLICAS", -1)) != repetitions:
        raise ParoDeGuardia("semilla/réplicas del contrato no coinciden con las selladas en emisiones.")
    frame, _diag = M.cargar_universo(inputs, contrato)
    sel = M.sellados(inputs)
    cr = cruce(frame, repetitions, seed)
    return adjudicar(cr, emis, sel, ola)
