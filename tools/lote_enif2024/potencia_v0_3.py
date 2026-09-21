#!/usr/bin/env python3
"""Simulación de potencia de la regla v0.3 sobre datos YA ABIERTOS (pilotos 1-3).

ACTO `GEN2-DIN-LOTE-ENIF2024-COMMIT-1`, pieza P3 (iii); enmienda v0.3 (firma
`FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01`): «El COMMIT-1 incluye una
simulación de potencia de esta regla sobre datos ya abiertos (pilotos 1 a 3)».
Pregunta: ¿con qué probabilidad un efecto como el del piloto 3 hace que el
IC95 de Δ = MAE(C2) − MAE(R2) despeje 0.5 pp, con 15, 35, 44 y 68 celdas?
**Reporta la curva; no cambia la regla** (PARO c del encargo).

QUÉ ENTRA (sellado, leído por id; nada se teclea)
-------------------------------------------------
  · piloto 3 (`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`): las 15 celdas
    puntuadas con `C2-D-PP` y `S-MEDIO-D-PP` (error absoluto por celda, pp) →
    la distribución POR CELDA de Δ_c = |e_C2| − |e_S½|; y su ΔMAE sellado con
    EE (`S-MEDIO-DELTA-MAE-EE`) para CALIBRAR el ruido.
  · las 35 celdas abiertas (8 del piloto 1, 12 del piloto 2, 15 del piloto 3)
    con el EE del árbitro R por celda (pp): la escala del ruido muestral que
    el remuestreo por réplica recoge.

MODELO (aproximación, declarada)
--------------------------------
  Δ_c = δ + r_c + ε_c, con r_c un residuo por celda re-muestreado de la
  distribución recentrada del piloto 3 (heterogeneidad entre celdas, FIJA en
  un lote real: no entra al IC) y ε_c ~ N(0, κ·EE_c) el ruido muestral de la
  celda (es lo que el IC por réplica recoge). κ se calibra para que, con las
  15 celdas del piloto 3, el EE simulado de Δ̂ iguale al EE sellado por
  réplica (0.330 pp): κ = EE_sellado·15 / sqrt(Σ EE_c²).
  IC95 de Δ̂ = Δ̂ ± 1.96·sqrt(Σ (κ·EE_c)²)/n (celdas independientes: el
  bootstrap real remuestrea UPM compartidas entre celdas y suele dar un IC
  más ANCHO, así que esta curva es una cota superior de la potencia).
  Potencia(δ, n) = P(Δ̂ − 1.96·SE > 0.5). Se reporta también P(despeja 0).
  Efectos: 0, 0.5, 1.10 (S½ del piloto 3), 1.47 (Sλ del piloto 3), 2.0 pp.
  n: 15, 35, 44 (5 pares primarios), 68 (9 pares con piso). 20 000 lotes
  simulados por punto, PCG64(20260921).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "forense" / "analisis" / "gen2-din-lote-enif2024-commit-1"
P1 = "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001"
P2 = "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001"
P3 = "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001"
EFECTOS = (0.0, 0.5, "S-MEDIO", "S-LAMBDA", 2.0)
N_CELDAS = (15, 35, 44, 68)
N_SIM = 20000
SEED = 20260921


def _res(calc):
    return json.loads((RAIZ / "data" / "corrida0" / calc / "resultados.json").read_text(encoding="utf-8"))["resultados"]


def celdas_abiertas() -> list:
    """[(piloto, celda, EE_pp, puntuada)] de las 35 celdas."""
    out = []
    r1 = _res(P1)
    for k, v in r1.items():
        m = re.match(r"RESULT-DIN-LXE8-ARB-R-D9-EE-(L\dxE\d)$", k)
        if m:
            c = m.group(1)
            out.append(("piloto-1", c, 100.0 * float(v), r1[f"RESULT-DIN-LXE8-ARB-PUNTUADA-{c}"] == "SI"))
    r2 = _res(P2)
    for k, v in r2.items():
        m = re.match(r"RESULT-TRA-SXD12-ARB-R-EE-(S\dxD\d)$", k)
        if m:
            c = m.group(1)
            out.append(("piloto-2", c, 100.0 * float(v), r2[f"RESULT-TRA-SXD12-ARB-PUNTUADA-{c}"] == "SI"))
    r3 = _res(P3)
    for k, v in r3.items():
        m = re.match(r"RESULT-GOB-EXE15-ADJ-2025-(.+?)-R-P-EE$", k)
        if m:
            c = m.group(1)
            out.append(("piloto-3", c, 100.0 * float(v), r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-SOPORTE"] == "PUNTUADA"))
    return out


def efecto_piloto3() -> dict:
    r3 = _res(P3)
    celdas = sorted({re.match(r"RESULT-GOB-EXE15-ADJ-2025-(.+?)-C2-D-PP$", k).group(1)
                     for k in r3 if re.match(r"RESULT-GOB-EXE15-ADJ-2025-(.+?)-C2-D-PP$", k)})
    d_medio, d_lambda, ee = [], [], []
    for c in celdas:
        if r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-SOPORTE"] != "PUNTUADA":
            continue
        d_medio.append(float(r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-C2-D-PP"]) - float(r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-S-MEDIO-D-PP"]))
        d_lambda.append(float(r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-C2-D-PP"]) - float(r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-S-LAMBDA-D-PP"]))
        ee.append(100.0 * float(r3[f"RESULT-GOB-EXE15-ADJ-2025-{c}-R-P-EE"]))
    return {"n": len(d_medio), "delta_medio": np.array(d_medio), "delta_lambda": np.array(d_lambda),
            "ee": np.array(ee),
            "sellado": {"S-MEDIO": {"dmae": float(r3["RESULT-GOB-EXE15-ADJ-2025-S-MEDIO-DELTA-MAE-PP"]),
                                    "ee": float(r3["RESULT-GOB-EXE15-ADJ-2025-S-MEDIO-DELTA-MAE-EE"]),
                                    "ic": [float(r3["RESULT-GOB-EXE15-ADJ-2025-S-MEDIO-DELTA-MAE-IC-LO"]),
                                           float(r3["RESULT-GOB-EXE15-ADJ-2025-S-MEDIO-DELTA-MAE-IC-HI"])]},
                        "S-LAMBDA": {"dmae": float(r3["RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-PP"]),
                                     "ee": float(r3["RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-EE"]),
                                     "ic": [float(r3["RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-IC-LO"]),
                                            float(r3["RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-IC-HI"])]}}}


def simula(pool_ee: np.ndarray, resid: np.ndarray, kappa: float, delta: float, n: int, rng) -> dict:
    ee = rng.choice(pool_ee, size=(N_SIM, n), replace=True)
    r = rng.choice(resid, size=(N_SIM, n), replace=True)
    eps = rng.normal(0.0, 1.0, size=(N_SIM, n)) * kappa * ee
    d_hat = delta + r.mean(axis=1) + eps.mean(axis=1)
    se = np.sqrt(((kappa * ee) ** 2).sum(axis=1)) / n
    lo = d_hat - 1.96 * se
    return {"potencia_0_5": float((lo > 0.5).mean()), "potencia_0": float((lo > 0.0).mean()),
            "se_medio": float(se.mean()), "d_hat_medio": float(d_hat.mean())}


def main(argv=None) -> int:
    escribe = "--escribe" in (argv or sys.argv[1:])
    todas = celdas_abiertas()
    pool = [c for c in todas if c[3]]          # las 35 PUNTUADAS (el piloto 3 tiene 16 nominales, 1 fuera de soporte ex ante)
    if len(pool) != 35:
        raise SystemExit(f"se esperaban 35 celdas puntuadas, hay {len(pool)} (nominales: {len(todas)})")
    pool_ee = np.array([c[2] for c in pool])
    e3 = efecto_piloto3()
    ee3 = e3["ee"]
    kappa = e3["sellado"]["S-MEDIO"]["ee"] * e3["n"] / float(np.sqrt((ee3 ** 2).sum()))
    resid = e3["delta_medio"] - e3["delta_medio"].mean()
    rng = np.random.Generator(np.random.PCG64(SEED))
    filas = []
    for ef in EFECTOS:
        delta = {"S-MEDIO": float(e3["delta_medio"].mean()), "S-LAMBDA": float(e3["delta_lambda"].mean())}.get(ef, ef)
        for n in N_CELDAS:
            r = simula(pool_ee, resid, kappa, float(delta), n, rng)
            filas.append({"efecto": ef if isinstance(ef, str) else f"{ef:.2f}", "delta_pp": float(delta), "n_celdas": n, **r})
    # control de calibración: 15 celdas del piloto 3 con su propio EE reproducen el EE sellado
    se_cal = float(np.sqrt(((kappa * ee3) ** 2).sum()) / e3["n"])
    cab = ["efecto", "delta_pp", "n_celdas", "potencia_despeja_0_5pp", "potencia_despeja_0", "se_medio_pp", "d_hat_medio_pp"]
    lineas = ["\t".join(cab)]
    for f in filas:
        lineas.append("\t".join([f["efecto"], f"{f['delta_pp']:.4f}", str(f["n_celdas"]), f"{f['potencia_0_5']:.4f}",
                                 f"{f['potencia_0']:.4f}", f"{f['se_medio']:.4f}", f"{f['d_hat_medio']:.4f}"]))
    tsv = "\n".join(lineas) + "\n"
    md = ["# Potencia de la regla v0.3 sobre datos ya abiertos — lote ENIF 2024", "",
          f"`tools/lote_enif2024/potencia_v0_3.py`, PCG64({SEED}), {N_SIM} lotes simulados por punto. "
          "Sellados leídos por id: pilotos 1 (`CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`), "
          "2 (`CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001`) y 3 (`CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`). "
          "**Reporta la curva; no cambia la regla.**", "",
          f"- Celdas en el pool: **{len(pool)}** puntuadas de {len(todas)} nominales (8 + 12 + 15; la 16.ª del piloto 3 está fuera de soporte ex ante); EE del árbitro por celda: mediana "
          f"{np.median(pool_ee):.2f} pp, mín {pool_ee.min():.2f}, máx {pool_ee.max():.2f}.",
          f"- Efecto del piloto 3 (15 celdas puntuadas): ΔMAE(S½) = {e3['delta_medio'].mean():.3f} pp "
          f"(sellado {e3['sellado']['S-MEDIO']['dmae']:.3f}, IC95 [{e3['sellado']['S-MEDIO']['ic'][0]:.3f}, "
          f"{e3['sellado']['S-MEDIO']['ic'][1]:.3f}]); ΔMAE(Sλ) = {e3['delta_lambda'].mean():.3f} pp "
          f"(sellado {e3['sellado']['S-LAMBDA']['dmae']:.3f}, IC95 [{e3['sellado']['S-LAMBDA']['ic'][0]:.3f}, "
          f"{e3['sellado']['S-LAMBDA']['ic'][1]:.3f}]). Desviación por celda de Δ_c: {resid.std(ddof=1):.3f} pp.",
          f"- Calibración del ruido: κ = {kappa:.4f} → con las 15 celdas del piloto 3 el EE simulado de Δ̂ es "
          f"{se_cal:.4f} pp (sellado por réplica {e3['sellado']['S-MEDIO']['ee']:.4f}).", "",
          "| efecto | Δ (pp) | n celdas | P(IC95 despeja 0.5 pp) | P(IC95 despeja 0) | SE medio (pp) |",
          "|---|---|---|---|---|---|"]
    for f in filas:
        md.append(f"| {f['efecto']} | {f['delta_pp']:.2f} | {f['n_celdas']} | {f['potencia_0_5']:.3f} | "
                  f"{f['potencia_0']:.3f} | {f['se_medio']:.3f} |")
    md += ["", "**Lectura, escrita antes de medir (spec v1_0 §7):** la potencia depende del efecto real y del "
           "ruido por celda; la curva de arriba es una cota superior (celdas tratadas como independientes; "
           "el bootstrap real comparte UPM entre celdas). Si con 44 celdas y el efecto del piloto 3 la regla no "
           "despeja 0.5 pp con probabilidad alta, **eso se declara antes de abrir y la consecuencia la decide "
           "mesa**, no el ejecutor y no después de ver el resultado.", ""]
    if escribe:
        SALIDA.mkdir(parents=True, exist_ok=True)
        (SALIDA / "potencia-v0_3.tsv").write_text(tsv, encoding="utf-8")
        (SALIDA / "potencia-v0_3.md").write_text("\n".join(md), encoding="utf-8")
        print(f"escrito: {SALIDA / 'potencia-v0_3.tsv'} y .md")
    else:
        print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
