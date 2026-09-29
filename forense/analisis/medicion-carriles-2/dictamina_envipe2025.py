#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENVIPE 2025 · dictámenes B-bis §3 de
forense/prereg-caja/MC2-ENVIPE2025-spec-v1_0.md, mecánicos, sobre CALC-MC2-ENVIPE2025-0001
(y E.5 sobre CALC-ENVIPE-PERCEPCION-2024-0001). Escribe MC2-ENVIPE2025-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, SEL = "CALC-MC2-ENVIPE2025-0001", "CALC-ENVIPE-PERCEPCION-2024-0001"
P = "RESULT-MC2-ENVIPE2025-"
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def carga(c):
    R = json.loads((RAIZ / f"data/corrida0/{c}/resultados.json").read_text())["resultados"]
    return {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


V, S = carga(CALC), carga(SEL)


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def nivel(k, cifra, t=None):
    p, lo, hi = t or c(k)
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) <= 0.10 else "ROMPE")
    return d, f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


def peor(xs):
    return max((x[0] for x in xs), key=ORD.get), " · ".join(x[1] for x in xs)


D = []


def fila(i, dom, dic, rid, t, det, un, calc=CALC):
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, dic, rid, calc] + [f"{x:.6f}" for x in t] + [un, det + " RETROSPECTIVA."])


UD, UP = "proporción ponderada, delito 2024 (ENVIPE 2025)", "proporción ponderada, persona 18+"
d, t = peor([nivel("DEL-CIFRA-NEGRA-NAC", 0.932), nivel("DEL-DENUNCIA-NAC", 0.096)])
fila("VIOL-007", "VIOLENCIA", d + "-PARCIAL", P + "DEL-CIFRA-NEGRA-NAC-P", c("DEL-CIFRA-NEGRA-NAC"), t + "; 0.8 % resolución positiva no medido.", UD)
p, lo, hi = c("DEL-CIFRA-NEGRA-NAC")
d = "CONFIRMA" if lo > 0.93 else ("ROMPE" if p <= 0.90 else "MATIZA")
fila("TRUST-026", "CONFIANZA", d + "-PARCIAL", P + "DEL-CIFRA-NEGRA-NAC-P", (p, lo, hi), f"«>93 %»: {p:.4f} [{lo:.4f}, {hi:.4f}] → {d}; sólo ola 2025.", UD)
d, t = peor([nivel("DEL-CIFRA-NEGRA-NAC", 0.924), nivel("DEL-DENUNCIA-NAC", 0.109)])
d = "MATIZA" if d == "CONFIRMA" else d
fila("CAPSOC-017", "VIOLENCIA", d, P + "DEL-CIFRA-NEGRA-NAC-P", c("DEL-CIFRA-NEGRA-NAC"), "Otra ola (2023), tope MATIZA: " + t, UD)
d, t = nivel("DEL-EXT-TELEFONICA-NAC", 0.85)
fila("VIOL-020", "DINERO", d + "-PARCIAL", P + "DEL-EXT-TELEFONICA-NAC-P", c("DEL-EXT-TELEFONICA-NAC"), t + "; total de 5.7 millones no medido.", "proporción ponderada, extorsiones 2024")
pre = {k: c(f"PREOC-{k}-2024-NAC")[0] for k in ("POBREZA", "DESEMPLEO", "NARCOTRAFICO", "PRECIOS", "INSEGURIDAD", "DESASTRES", "AGUA", "CORRUPCION", "EDUCACION", "SALUD", "IMPUNIDAD")}
o = ("CONFIRMA", "INSEGURIDAD es la mayor") if max(pre, key=pre.get) == "INSEGURIDAD" else ("ROMPE", f"la mayor es {max(pre, key=pre.get)}")
d, t = peor([nivel("PREOC-INSEGURIDAD-2024-NAC", 0.607), nivel("PREOC-AGUA-2024-NAC", 0.368), nivel("PREOC-PRECIOS-2024-NAC", 0.344), o])
fila("CAPSOC-018", "VIOLENCIA", d, P + "PREOC-INSEGURIDAD-2024-NAC-P", c("PREOC-INSEGURIDAD-2024-NAC"), t, UP)
esp = {"CAJERO": 0.723, "TRANSPORTE": 0.635, "CALLE": 0.610, "CARRETERA": 0.604, "BANCO": 0.602}
pts = {k: c(f"INSEGURO-{k}-2024-NAC")[0] for k in esp}
o = ("CONFIRMA", "CAJERO es el mayor") if max(pts, key=pts.get) == "CAJERO" else ("ROMPE", f"el mayor es {max(pts, key=pts.get)}")
d, t = peor([nivel(f"INSEGURO-{k}-2024-NAC", v) for k, v in esp.items()] + [o])
fila("VIOL-033", "VIOLENCIA", d, P + "INSEGURO-CAJERO-2024-NAC-P", c("INSEGURO-CAJERO-2024-NAC"), t, UP)
b = "RESULT-ENVIPE-PERCEPCION-2024-DEJO-PERMITIR-MENORES-SALIR-SOLOS-2024-TOTAL-TODOS-"
tm = (S[b + "P"], S.get(b + "IC95-INF", S.get(b + "IC-LO")), S.get(b + "IC95-SUP", S.get(b + "IC-HI")))
d, t = peor([nivel("MENORES(E.5)", 0.614, tm), nivel("DEJO-SALIR-NOCHE-2024-NAC", 0.459)])
fila("VIOL-032", "VIOLENCIA", d, P + "DEJO-SALIR-NOCHE-2024-NAC-P", c("DEJO-SALIR-NOCHE-2024-NAC"), t, UP)
dif = c("EDO-INSEGURO-SINALOA-DIF-2025-2024")
o = ("ROMPE", "diferencia ≤ 0") if dif[0] <= 0 else ("CONFIRMA", f"DIF {dif[0]:.4f} [{dif[1]:.4f}, {dif[2]:.4f}]")
d, t = peor([nivel("EDO-INSEGURO-2024-SINALOA", 0.549), nivel("EDO-INSEGURO-2025-SINALOA", 0.805), o])
sp = S["RESULT-ENVIPE-PERCEPCION-2024-ESTADO-INSEGURO-2024-ENTIDAD-25-P"]
fila("VIOL-043", "VIOLENCIA", d, P + "EDO-INSEGURO-SINALOA-DIF-2025-2024-P", dif,
     t + f"; control 2024 vs sellado {sp:.6f} (MC2 {c('EDO-INSEGURO-2024-SINALOA')[0]:.6f}); causa no contrastada.",
     "diferencia 2025−2024 de proporciones, persona 18+ en Sinaloa")
nan = (float("nan"),) * 3
fila("TIME-038", "VIOLENCIA", "NO-CONSTRUIBLE", "", nan, "Regla con mecanismo no observable; pisos DEJO-SALIR-NOCHE y EDO-INSEGURO quedan como insumo.", "—", "")
fila("POL-009", "POLITICA", "NO-CONSTRUIBLE", "", nan, "Costo total INEGI suma pérdidas, prevención y salud sobre PIB externo.", "—", "")
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENVIPE2025-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3], x[6], x[7], x[8])
print("DIAG", {k[len(P):]: v for k, v in V.items() if "DIAG" in k})
