#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIGH 2022 · dictámenes B-bis §2 de forense/prereg-caja/MC2-ENIGH2022-spec-v1_0.md
sobre CALC-MC2-ENIGH2022-0001 y (E.5) CALC-ENIGH2022-INTENSIDAD-REMESAS-0001. Tope MATIZA (ola 2022 vs 2024).
Escribe MC2-ENIGH2022-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC, SEL, P, S = "CALC-MC2-ENIGH2022-0001", "CALC-ENIGH2022-INTENSIDAD-REMESAS-0001", "RESULT-MC2-ENIGH2022-", "RESULT-ENIGH22-REMINT-"
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def carga(c):
    R = json.loads((RAIZ / f"data/corrida0/{c}/resultados.json").read_text())["resultados"]
    return {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


V, W = carga(CALC), carga(SEL)


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def abs_(nom, t, cifra):
    p, lo, hi = t
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) <= 0.10 else "ROMPE")
    return d, f"{nom} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


def rel(nom, t, cifra):
    p, lo, hi = t
    d = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) / cifra <= 0.25 else "ROMPE")
    return d, f"{nom} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} (relativa) → {d}"


def tope(d):
    return "MATIZA" if d == "CONFIRMA" else d


D = []


def fila(i, dom, d, rid, calc, t, det, un):
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, tope(d), rid, calc, f"{t[0]:.6f}", f"{t[1]:.6f}", f"{t[2]:.6f}", un,
              "ENIGH 2022 en lugar de 2024 reservada (tope MATIZA): " + det + " RETROSPECTIVA."])


t = c("GASTO-RAZON-CDMX-CHIAPAS"); d, s = rel("gasto CDMX/Chiapas", t, 2.5)
fila("CONS-023", "CONSUMO", d, P + "GASTO-RAZON-CDMX-CHIAPAS-P", CALC, t, s + f"; mensual CDMX {c('GASTO-MON-MENSUAL-CDMX')[0]:.0f} y Chiapas {c('GASTO-MON-MENSUAL-CHIAPAS')[0]:.0f} (pesos 2022).", "razón de medias, hogar")
t = c("ING-RAZON-NUEVO-LEON-CHIAPAS"); d, s = rel("ingreso NL/Chiapas", t, round(117034 / 41084, 3))
fila("FAM-036", "DINERO", d, P + "ING-RAZON-NUEVO-LEON-CHIAPAS-P", CALC, t, s, "razón de medias, hogar")
xs = [abs_("D1 alimentos/ingreso", c("D1-ALIMENTOS-SOBRE-INGRESO"), 0.50), abs_("D1 transferencias/ingreso", c("D1-TRANSFER-SOBRE-INGRESO"), 0.36),
      abs_("D10 participación", c("D10-PARTICIPACION-INGRESO"), 0.303)]
d = max((x[0] for x in xs), key=ORD.get)
fila("FAM-034", "DINERO", d, P + "D10-PARTICIPACION-INGRESO-P", CALC, c("D10-PARTICIPACION-INGRESO"), " · ".join(x[1] for x in xs), "razón de totales, hogar")
t = c("GINI-CON-TRANSFERENCIAS"); d, s = abs_("Gini con transferencias", t, 0.391)
fila("MER-004", "MOVILIDAD", d, P + "GINI-CON-TRANSFERENCIAS-P", CALC, t, s, "Gini ponderado, hogar")
t2 = c("GINI-SIN-TRANSFERENCIAS"); d, s = abs_("Gini sin transferencias", t2, 0.450)
d = "ROMPE" if t2[0] <= t[0] else d
fila("MER-005", "MOVILIDAD", d, P + "GINI-SIN-TRANSFERENCIAS-P", CALC, t2, s, "Gini ponderado, hogar")
t = (W[S + "PARTICIPACION-MEDIA-HOGAR"], W[S + "PARTICIPACION-MEDIA-HOGAR-IC-LO"], W[S + "PARTICIPACION-MEDIA-HOGAR-IC-HI"])
d, s = abs_("remesas/ingreso (receptores)", t, 0.30)
fila("FIN-031", "DINERO", d, S + "PARTICIPACION-MEDIA-HOGAR", SEL, t, "E.5: " + s, "proporción media por hogar receptor")
m = W[S + "RECEPTORES-MASA"]; r = abs(m - 1530000) / 1530000
d = "CONFIRMA" if r <= 0.10 else ("MATIZA" if r <= 0.25 else "ROMPE")
fila("FIN-032", "DINERO", d, S + "RECEPTORES-MASA", SEL, (m, m, m), f"E.5: hogares receptores {m:,.0f} vs 1 530 000 (Δ relativo {r:.3f}, sin IC) → {d}", "hogares expandidos")
cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
D.append(["ASTRA5-U0-MIGR-006", "afirmacion", "MIGRACION", "PISO-SIN-DICTAMEN", "", "", "nan", "nan", "nan", "—", "Construcción de variables (remesas, transf_hog, bene_gob) verificada por texto en la descripción de la base; no es cifra."])
D.append(["ASTRA5-U0-SALMEN-028", "afirmacion", "SALUD_MENTAL", "NO-CONSTRUIBLE", "", "", "nan", "nan", "nan", "—", "ENIGH registra gasto trimestral por clase, no precio por sesión."])
(RAIZ / "forense/analisis/medicion-carriles-2/MC2-ENIGH2022-dictamenes.tsv").write_text(
    "\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3], x[6], x[7], x[8])
