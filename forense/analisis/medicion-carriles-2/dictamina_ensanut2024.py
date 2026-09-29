#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENSANUT 2024 · dictámenes por la regla B-bis §3 de
forense/prereg-caja/MC2-ENSANUT2024-spec-v1_0.md, aplicada mecánicamente a
CALC-MC2-ENSANUT2024-0001 (y, para JUV-009, a CALC-ENSANUT-PISOS-SALUD-0001, E.5).
Escribe ENSANUT2024-dictamenes.tsv y el control de marginales BUSCO contra lo sellado."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC = "CALC-MC2-ENSANUT2024-0001"
SEL = "CALC-ENSANUT-PISOS-SALUD-0001"
P = "RESULT-MC2-ENSANUT2024-"


def carga(calc):
    R = json.loads((RAIZ / f"data/corrida0/{calc}/resultados.json").read_text())["resultados"]
    return {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R


V, S = carga(CALC), carga(SEL)
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def txt(k, t=None):
    p, lo, hi = t or c(k)
    return f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}]"


D = []


def fila(i, clase, dom, dic, rid, calc, t, det, unidad):
    D.append([i, clase, dom, dic, rid, calc, f"{t[0]:.6f}", f"{t[1]:.6f}", f"{t[2]:.6f}", unidad, det + " RETROSPECTIVA."])


# RG-41d71be87f
t1, t2 = c("BUSCO-DIF-RURAL-METRO"), c("ACCESO-DIF-RURAL-METRO")
d1 = "CONFIRMA" if t1[2] < 0 else ("ROMPE" if t1[0] >= 0 else "MATIZA")
d2 = "CONFIRMA" if t2[1] > 0 else ("ROMPE" if t2[0] <= 0 else "MATIZA")
d = max((d1, d2), key=ORD.get)
fila("RG-41d71be87f", "regla", "SALUD", d, P + "BUSCO-DIF-RURAL-METRO-P", CALC, t1,
     f"Spec §3 peor de (i) {txt('BUSCO-DIF-RURAL-METRO')} → {d1} y (ii) {txt('ACCESO-DIF-RURAL-METRO')} → {d2}. "
     f"Contexto (no decide): {txt('ACCESO-NAC')}; {txt('NO-GRAVE-NAC')}. «Ya falló antes», consejo del allegado y "
     "mecanismo no observables; el estrato también mueve gravedad y oferta.",
     "diferencia de proporciones RURAL−METRO, persona con necesidad de salud (3 meses)")
# SALUD-032
t1, t2 = c("DM-SUSPENDE-DIF-PAGA-NOPAGA"), c("DM-ECON-ACCESO-NAC")
d1 = "CONFIRMA" if t1[1] > 0 else ("ROMPE" if t1[0] <= 0 else "MATIZA")
d2 = "CONFIRMA" if t2[1] >= 0.5 else ("ROMPE" if t2[0] < 0.25 else "MATIZA")
d = max((d1, d2), key=ORD.get)
fila("ASTRA5-U0-SALUD-032", "afirmacion", "SALUD", d, P + "DM-SUSPENDE-DIF-PAGA-NOPAGA-P", CALC, t1,
     f"Spec §3 peor de (i) {txt('DM-SUSPENDE-DIF-PAGA-NOPAGA')} → {d1} y (ii) {txt('DM-ECON-ACCESO-NAC')} → {d2}. "
     "«Gasto alto» leído como pagar algo (> 0).",
     "diferencia de proporciones PAGA−NOPAGA, adulto 20+ con diabetes en tratamiento")
# SALMEN-032 (tope MATIZA)
t = c("BUSCO-MENTAL-DIF-RURAL-NORURAL")
d = "ROMPE" if t[0] >= 0 else "MATIZA"
fila("ASTRA5-U0-SALMEN-032", "afirmacion", "RURAL_INDIGENA", d, P + "BUSCO-MENTAL-DIF-RURAL-NORURAL-P", CALC, t,
     f"Spec §3 (proxy: cualquier atención, no especialista; tope MATIZA): {txt('BUSCO-MENTAL-DIF-RURAL-NORURAL')} → {d}; "
     f"{txt('BUSCO-MENTAL-RURAL')} (n={V[P + 'BUSCO-MENTAL-RURAL-N']}).",
     "diferencia de proporciones RURAL−NORURAL, persona con necesidad de salud mental (3 meses)")
# JUV-009 (E.5, tope MATIZA)
def sel(conducta):
    b = f"RESULT-ENSANUT-PISOS-SALUD-{conducta}-2024-TOTAL-TODOS-"
    return S[b + "P"], S[b + "IC-LO"], S[b + "IC-HI"], b + "P"


partes = []
for con, cifra in (("IDEACION-SUICIDA-ADOLESCENTES", 0.076), ("IDEACION-SUICIDA-ADULTOS", 0.077)):
    p, lo, hi, rid = sel(con)
    dd = "CONFIRMA" if lo <= cifra <= hi else ("MATIZA" if abs(p - cifra) <= 0.10 else "ROMPE")
    partes.append((dd, f"{con} 2024 {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {dd}", (p, lo, hi), rid))
d = max((x[0] for x in partes), key=ORD.get)
d = "MATIZA" if d == "CONFIRMA" else d
fila("ASTRA5-U0-JUV-009", "afirmacion", "SALUD_MENTAL", d + "-PARCIAL", partes[0][3], SEL, partes[0][2],
     "Spec §3, cita E.5 de " + SEL + " (reactivos d0817/a1211; ola 2024 vs 2022 del report; tope MATIZA): "
     + " · ".join(x[1] for x in partes) + ". Intento de suicidio no medido aquí.",
     "proporción ponderada, adolescente 10-19")
fila("ASTRA5-U0-RURAL-021", "afirmacion", "SALUD", "NO-CONSTRUIBLE", "", "", (float("nan"),) * 3,
     "Spec §3: «lógica interna coherente» no observable; presencia de curandero como lugar de atención citada de "
     + SEL + " (ATENCION-CURANDERO-HIERBERO, E.5).", "—")

cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
out = RAIZ / "forense/analisis/medicion-carriles-2/ENSANUT2024-dictamenes.tsv"
out.write_text("\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3])
# control: marginales BUSCO por estrato contra lo sellado (punto)
for mio, suyo in (("RURAL", "RURAL"), ("URBANO", "URBANO"), ("METRO", "METROPOLITANO")):
    a = V[P + f"BUSCO-{mio}-P"]
    b = S.get(f"RESULT-ENSANUT-PISOS-SALUD-BUSCO-ATENCION-2024-ESTRATO-{suyo}-P")
    print(f"CONTROL BUSCO {mio}: MC2 {a:.6f} · sellado {b if b is None else round(b, 6)}")
