#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 m7 · dictámenes B-bis §2 de
forense/prereg-caja/MC2-ENIF2024-M7-spec-v1_0.md sobre CALC-MC2-ENIF2024-M7-0001. Escribe MC2-ENIF2024-M7-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, P = "CALC-MC2-ENIF2024-M7-0001", "RESULT-MC2-ENIF2024-M7-"
R = json.loads((RAIZ / f"data/corrida0/{CALC}/resultados.json").read_text())["resultados"]
V = {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def nivel(k, cifra):
    p, lo, hi = c(k)
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) <= 0.10 else "ROMPE")
    return d, f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


U = "proporción ponderada, persona elegida 18+"
k = "EFECTIVO-500-O-MENOS-NAC"
filas = []
d, t = nivel(k, 0.852)
filas.append(("CONS-010", d, t + "; el report dice «ENIF 2025», contrastado contra 2024 (no hay ola 2025)."))
d, t = nivel(k, 0.85)
filas.append(("APUEST-030", d + "-PARCIAL", t + "; ola 2021 (~90 %) y NTT Data (transacciones) no medidas."))
filas.append(("APUEST-032", "PISO-SIN-DICTAMEN", "Hallazgo de instrumento; pisos: " + " · ".join(
    f"{x} {c(x)[0]:.4f} [{c(x)[1]:.4f}, {c(x)[2]:.4f}]" for x in ("CODI-CONOCE-NAC", "CODI-USA-SI-CONOCE-NAC", "CODI-USA-POBLACION-NAC"))))
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
out = []
for i, dic, det in filas:
    rk = k if i != "APUEST-032" else "CODI-CONOCE-NAC"
    p, lo, hi = c(rk)
    out.append([f"ASTRA5-U0-{i}", "afirmacion", "DINERO", dic, P + rk + "-P", CALC, f"{p:.6f}", f"{lo:.6f}", f"{hi:.6f}", U,
                det + " Módulo 7 ABIERTA-PARCIAL (ADENDA-1). RETROSPECTIVA."])
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENIF2024-M7-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in out), encoding="utf-8")
for x in out:
    print(x[0], x[3])
