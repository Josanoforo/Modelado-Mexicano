#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENOE · dictámenes B-bis §2 de forense/prereg-caja/MC2-ENOE-spec-v1_0.md
sobre CALC-MC2-ENOE-0001 y (E.5) celdas selladas de CALC-ENOE-PISOS-0003. Escribe MC2-ENOE-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, SEL, P = "CALC-MC2-ENOE-0001", "CALC-ENOE-PISOS-0003", "RESULT-MC2-ENOE-"
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def carga(c):
    R = json.loads((RAIZ / f"data/corrida0/{c}/resultados.json").read_text())["resultados"]
    return {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


V = carga(CALC)
T = {(x["ola"], x["conducta"], x["eje"], x["segmento"]): x for x in json.loads(carga(SEL)["RESULT-ENOE-PISOS-TABLA"])}


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def s(eje, seg, ola="2025T4", cond="empleo_informal"):
    x = T[(ola, cond, eje, seg)]
    return x["punto"], x["ic95_lo"], x["ic95_hi"]


def nivel(nom, t, cifra):
    p, lo, hi = t
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) <= 0.10 else "ROMPE")
    return d, f"{nom} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


def peor(xs):
    return max((x[0] for x in xs), key=ORD.get), " · ".join(x[1] for x in xs)


def tope(d):
    return "MATIZA" if d == "CONFIRMA" else d


D = []


def fila(i, dom, dic, rid, calc, t, det, un):
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, dic, rid, calc, f"{t[0]:.6f}", f"{t[1]:.6f}", f"{t[2]:.6f}", un, det + " RETROSPECTIVA."])


d, t = peor([nivel("PARTICIPA-MUJER", c("2025T4-PARTICIPA-MUJER"), 0.46), nivel("PARTICIPA-HOMBRE", c("2025T4-PARTICIPA-HOMBRE"), 0.77)])
fila("GEN-009", "TRABAJO", d + "-PARCIAL", P + "2025T4-PARTICIPA-MUJER-P", CALC, c("2025T4-PARTICIPA-MUJER"), t + "; alza 2005→2025 no medida.", "proporción ponderada, persona 15+")
b = c("2025T4-INGRESO-BRECHA-MUJER-HOMBRE")
d, t = nivel("BRECHA", b, 0.14)
d = "ROMPE" if b[0] <= 0 else d
fila("GEN-011", "TRABAJO", d, P + "2025T4-INGRESO-BRECHA-MUJER-HOMBRE-P", CALC, b, t + "; asociación sin control de horas, ocupación ni escolaridad.", "1 − razón de ingresos medios mujer/hombre, ocupados")
d, t = peor([nivel(f"{k}-{g}", c(f"2023T3-ECON-{k}-{g}"), v) for (k, g, v) in (
    ("UNION-LIBRE", "15MAS", 0.178), ("CASADO", "15MAS", 0.369), ("SOLTERO", "15MAS", 0.331),
    ("SOLTERO", "15-29", 0.727), ("UNION-LIBRE", "15-29", 0.17), ("CASADO", "15-29", 0.083))])
fila("PAREJA-003", "PAREJA", d, P + "2023T3-ECON-UNION-LIBRE-15MAS-P", CALC, c("2023T3-ECON-UNION-LIBRE-15MAS"), t, "proporción ponderada, persona 15+ (2023T3)")
d, t = nivel("OCUPADO-MENOR25", c("2025T4-OCUPADO-MENOR25-NAC"), 0.55)
fila("TRAB-022", "JUVENTUD", d, P + "2025T4-OCUPADO-MENOR25-NAC-P", CALC, c("2025T4-OCUPADO-MENOR25-NAC"), t, "proporción ponderada, población ocupada")
RS = "celda sellada de " + SEL
d, t = nivel("informal 2025T4 NAC", s("nacional", "NAC"), 0.55)
fila("CLASE-006", "TRABAJO", d, "RESULT-ENOE-PISOS-TABLA", SEL, s("nacional", "NAC"), f"E.5 ({RS}): " + t, "proporción ponderada, población ocupada")
ents = {e: s("entidad", e)[0] for (o, cd, ej, e) in T if o == "2025T4" and cd == "empleo_informal" and ej == "entidad"}
top3 = sorted(ents, key=ents.get, reverse=True)[:3]
o = ("CONFIRMA", f"top-3 entidades {top3}") if set(top3) == {"20", "12", "07"} else ("ROMPE", f"top-3 entidades {top3}")
d, t = peor([nivel("NAC", s("nacional", "NAC"), 0.55), nivel("ENT-20", s("entidad", "20"), 0.801),
             nivel("ENT-12", s("entidad", "12"), 0.757), nivel("ENT-07", s("entidad", "07"), 0.749), o])
fila("CONOC-029", "TRABAJO", d, "RESULT-ENOE-PISOS-TABLA", SEL, s("nacional", "NAC"), f"E.5 ({RS}): " + t, "proporción ponderada, población ocupada")
m, h = s("sexo", "MUJER"), s("sexo", "HOMBRE")
d, t = peor([nivel("MUJER", m, 0.55), nivel("HOMBRE", h, 0.49)])
d = "ROMPE" if m[0] <= h[0] else tope(d)
fila("GEN-010", "TRABAJO", d, "RESULT-ENOE-PISOS-TABLA", SEL, m, f"E.5 ({RS}; ola del report no nombrada, tope MATIZA): " + t, "proporción ponderada, mujeres ocupadas")
j = s("edad", "15-29")
d = "ROMPE" if j[0] < 0.5 else "MATIZA"
fila("JUV-028", "TRABAJO", d, "RESULT-ENOE-PISOS-TABLA", SEL, j, f"E.5 ({RS}; 15-29 como proxy de 20–30, tope MATIZA): informal 15-29 {j[0]:.4f} [{j[1]:.4f}, {j[2]:.4f}] vs > 0.5 → {d}.", "proporción ponderada, ocupados 15-29")
d, t = nivel("100K+", s("localidad", "100K+"), 0.429)
fila("TIME-009", "TRABAJO", tope(d), "RESULT-ENOE-PISOS-TABLA", SEL, s("localidad", "100K+"), f"E.5 ({RS}; 100K+ como proxy de «urbana», tope MATIZA): " + t, "proporción ponderada, ocupados en localidades 100K+")
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENOE-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3], x[6], x[7], x[8])
print({k[len(P):]: v for k, v in V.items() if "DIAG" in k})
