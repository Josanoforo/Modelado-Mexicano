#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENUT 2024 · dictámenes B-bis §2 de forense/prereg-caja/MC2-ENUT2024-spec-v1_0.md
sobre CALC-MC2-ENUT2024-0001. Escribe MC2-ENUT2024-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, P = "CALC-MC2-ENUT2024-0001", "RESULT-MC2-ENUT2024-"
R = json.loads((RAIZ / f"data/corrida0/{CALC}/resultados.json").read_text())["resultados"]
V = {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def txt(k):
    p, lo, hi = c(k)
    return f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}]"


def nivel(k, cifra, relativa=False):
    p, lo, hi = c(k)
    tol = abs(p - cifra) / cifra <= 0.25 if relativa else abs(p - cifra) <= 0.10
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if tol else "ROMPE")
    return d, f"{txt(k)} vs {cifra} → {d}"


def peor(xs):
    return max((x[0] for x in xs), key=ORD.get), " · ".join(x[1] for x in xs)


D = []


def fila(i, dom, dic, k, det, un):
    p, lo, hi = c(k)
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, dic, P + k + "-P", CALC, f"{p:.6f}", f"{lo:.6f}", f"{hi:.6f}", un, det + " RETROSPECTIVA."])


d, t = nivel("CUIDADOR-DEP-MUJER-PROP", 0.953)
fila("FAM-007", "FAMILIA_CUIDADOS", d + "-PARCIAL", "CUIDADOR-DEP-MUJER-PROP", t + "; «62.3 % no recibe remuneración» no medido.", "proporción de mujeres entre quienes cuidan a dependientes")
d, t = peor([nivel("CUID-INT-MUJER", 54.3, True), nivel("CUID-INT-HOMBRE", 30.2, True)])
d = "ROMPE" if c("CUID-INT-MUJER")[0] <= c("CUID-INT-HOMBRE")[0] else d
fila("FAM-008", "FAMILIA_CUIDADOS", d, "CUID-INT-MUJER", t, "horas por semana entre quienes cuidan")
d, t = nivel("TNR-PROPORCION-HORAS-MUJERES", 0.73)
fila("GEN-012", "TRABAJO", d + "-PARCIAL", "TNR-PROPORCION-HORAS-MUJERES", t + "; partes de Cuenta Satélite (PIB) no son de ENUT.", "proporción de las horas de TNR")
ks = ["HOMBRES-CUID-PART-DIF-18-29-MENOS-60MAS", "HOMBRES-CUID-PART-DIF-URBANO-RURAL", "HOMBRES-CUID-PART-DIF-SUPERIOR-BASICA"]
ts = [c(k) for k in ks]
d = "CONFIRMA" if all(x[1] > 0 for x in ts) else ("ROMPE" if any(x[0] <= 0 for x in ts) else "MATIZA")
fila("GEN-018", "FAMILIA_CUIDADOS", d + "-PARCIAL", ks[0], " · ".join(txt(k) for k in ks) + f" → {d}; «pareja económicamente activa» no medida.", "diferencia de proporciones, hombres 12+")
p, lo, hi = c("COMUN-PART-DIF-MUJER-HOMBRE")
d = "CONFIRMA" if lo > 0 else ("ROMPE" if p <= 0 else "MATIZA")
fila("RURAL-038", "GENERO", d, "COMUN-PART-DIF-MUJER-HOMBRE", f"{txt('COMUN-PART-DIF-MUJER-HOMBRE')} → {d}.", "diferencia de proporciones mujer − hombre, persona 12+")
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
D.append(["ASTRA5-U0-FAM-039", "afirmacion", "GENERO", "NO-CONSTRUIBLE", "", "", "nan", "nan", "nan", "—", "ENUT §5.11 no pregunta «desea trabajar pero no puede por falta de quien cuide» (FD TMODULO P5_11, recorrido §5.10-5.11)."])
D.append(["ASTRA5-U0-CAPSOC-012", "afirmacion", "CAPITAL_SOCIAL", "PISO-SIN-DICTAMEN", "", "CALC-PDR1-ENUT2024-0001", "nan", "nan", "nan", "—", "Afirmación de instrumento (texto de 6.17), verificada por texto; piso citado de PDR1."])
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENUT2024-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3], x[6], x[7], x[8])
print(txt("CUID-INT-HOMBRE"), txt("CUIDADOR-TOTAL-MUJER-PROP"))
