#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENDUTIH 2024 · dictámenes B-bis §2 de forense/prereg-caja/MC2-ENDUTIH2024-spec-v1_0.md
sobre CALC-MC2-ENDUTIH2024-0001 y (E.5) celdas de CALC-ENDUTIH-PISOS-2023/2024-0001. Escribe MC2-ENDUTIH2024-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, P = "CALC-MC2-ENDUTIH2024-0001", "RESULT-MC2-ENDUTIH2024-"
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def carga(c):
    R = json.loads((RAIZ / f"data/corrida0/{c}/resultados.json").read_text())["resultados"]
    return {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


V = carga(CALC)
PIS = {}
for ola in ("2023", "2024"):
    V2 = carga(f"CALC-ENDUTIH-PISOS-{ola}-0001")
    for x in json.loads(V2[f"RESULT-ENDUTIH-PISOS-{ola}-TABLA"])["celdas"]:
        PIS[(ola, x["medida"], x["dominio"])] = x


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def s(ola, med, dom):
    x = PIS[(ola, med, dom)]
    ic = x["ic95"]
    lo, hi = (ic[0], ic[1]) if isinstance(ic, (list, tuple)) else (ic["lo"], ic["hi"])
    return x["punto"], lo, hi


def nivel(nom, t, cifra, rel=False):
    p, lo, hi = t
    tol = abs(p - cifra) / cifra <= 0.25 if rel else abs(p - cifra) <= 0.10
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if tol else "ROMPE")
    return d, f"{nom} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


def peor(xs):
    return max((x[0] for x in xs), key=ORD.get), " · ".join(x[1] for x in xs)


def tope(d):
    return "MATIZA" if d == "CONFIRMA" else d


D = []


def fila(i, dom, dic, rid, calc, t, det, un):
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, dic, rid, calc, f"{t[0]:.6f}", f"{t[1]:.6f}", f"{t[2]:.6f}", un, det + " RETROSPECTIVA."])


d, t = peor([nivel("INTERNET 18-24", c("INTERNET-EDAD-18-24"), 0.97), nivel("HORAS 18-24", c("HORAS-DIA-EDAD-18-24"), 5.7, True)])
fila("JUV-007", "TECNOLOGIA", d + "-PARCIAL", P + "INTERNET-EDAD-18-24-P", CALC, c("INTERNET-EDAD-18-24"), t + "; smartphone 97.2 % sin reactivo.", "proporción ponderada, persona 18-24")
d, t = peor([nivel("INTERNET 55-64", c("INTERNET-EDAD-55-64"), 0.71), nivel("INTERNET 65+", c("INTERNET-EDAD-65-MAS"), 0.421)])
fila("TEC-008", "TECNOLOGIA", d, P + "INTERNET-EDAD-65-MAS-P", CALC, c("INTERNET-EDAD-65-MAS"), t, "proporción ponderada, persona 65+")
d, t = nivel("WhatsApp entre usuarios de internet", c("WHATSAPP-USUARIOS-INTERNET-NAC"), 0.91)
fila("TEC-033", "TECNOLOGIA", d, P + "WHATSAPP-USUARIOS-INTERNET-NAC-P", CALC, c("WHATSAPP-USUARIOS-INTERNET-NAC"), t, "proporción ponderada, usuarios de internet 6+")
S = "celda sellada de CALC-ENDUTIH-PISOS-{}-0001 (E.5)"
d, t = nivel("internet 2023 TOTAL", s("2023", "internet", "TOTAL"), 0.812)
fila("CONOC-008", "TECNOLOGIA", d, "RESULT-ENDUTIH-PISOS-2023-TABLA", "CALC-ENDUTIH-PISOS-2023-0001", s("2023", "internet", "TOTAL"), S.format(2023) + ": " + t, "proporción ponderada, persona 6+")
d, t = nivel("mensajes 2023 TOTAL", s("2023", "actividad_mensajes", "TOTAL"), 0.912)
fila("CONOC-007", "TECNOLOGIA", tope(d) + "-PARCIAL", "RESULT-ENDUTIH-PISOS-2023-TABLA", "CALC-ENDUTIH-PISOS-2023-0001", s("2023", "actividad_mensajes", "TOTAL"), S.format(2023) + " (universo usuarios de internet, tope MATIZA): " + t, "proporción ponderada, usuarios de internet")
a, b = s("2024", "internet", "TLOC_1"), s("2024", "internet", "TLOC_4")
d, t = peor([nivel("internet TLOC_1", a, 0.712), nivel("internet TLOC_4", b, 0.392)])
d = "ROMPE" if a[0] <= b[0] else tope(d)
fila("CONS-038", "TECNOLOGIA", d, "RESULT-ENDUTIH-PISOS-2024-TABLA", "CALC-ENDUTIH-PISOS-2024-0001", a, S.format(2024) + " (ola no nombrada, tope MATIZA): " + t, "proporción ponderada, persona 6+ en 100K+")
d, t = peor([nivel("internet TLOC_1", a, 0.86), nivel("internet TLOC_4", b, 0.67)])
fila("JUV-008", "TECNOLOGIA", d, "RESULT-ENDUTIH-PISOS-2024-TABLA", "CALC-ENDUTIH-PISOS-2024-0001", b, S.format(2024) + ": " + t, "proporción ponderada, persona 6+ en < 2 500")
d, t = peor([nivel("celular 12-17", s("2024", "celular", "EDAD_12_17"), 0.90), nivel("celular 18-29", s("2024", "celular", "EDAD_18_29"), 0.90)])
fila("SALMEN-025", "TECNOLOGIA", d + "-PARCIAL", "RESULT-ENDUTIH-PISOS-2024-TABLA", "CALC-ENDUTIH-PISOS-2024-0001", s("2024", "celular", "EDAD_12_17"), S.format(2024) + ": " + t + "; «35.3 millones» no medido.", "proporción ponderada, persona 12-17")
D.append(["ASTRA5-U0-TEC-031", "afirmacion", "TECNOLOGIA", "PISO-SIN-DICTAMEN", P + "WHATSAPP-USUARIOS-REDES-NAC-P", CALC, "nan", "nan", "nan", "—", "Mecanismo (capa transaccional) no observable; pisos WhatsApp reportados."])
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENDUTIH2024-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3], x[6], x[7], x[8])
print("horas 18-24", c("HORAS-DIA-EDAD-18-24"), "WA redes", c("WHATSAPP-USUARIOS-REDES-NAC"))
