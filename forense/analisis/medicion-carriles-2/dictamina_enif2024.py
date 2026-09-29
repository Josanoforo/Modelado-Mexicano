#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 · dictámenes por la regla B-bis §3
de forense/prereg-caja/MC2-ENIF2024-spec-v1_0.md, aplicada mecánicamente a los
RESULT sellados de CALC-MC2-ENIF2024-0001. Escribe ENIF2024-dictamenes.tsv."""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CALC = "CALC-MC2-ENIF2024-0001"
P = "RESULT-MC2-ENIF2024-"
R = json.loads((RAIZ / f"data/corrida0/{CALC}/resultados.json").read_text())["resultados"]
V = {x["id"]: x.get("valor") for x in R} if isinstance(R, list) else R
ORD = {"CONFIRMA": 0, "MATIZA": 1, "ROMPE": 2}


def c(k):
    return V[P + k + "-P"], V[P + k + "-IC95-INF"], V[P + k + "-IC95-SUP"]


def nivel(k, cifra, ref=None):
    p, lo, hi = ref if ref else c(k)
    if lo <= cifra <= hi:
        d = "CONFIRMA"
    elif abs(p - cifra) <= 0.10:
        d = "MATIZA"
    else:
        d = "ROMPE"
    return d, f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}] vs {cifra} → {d}"


def rango(k, a, b):
    p, lo, hi = c(k)
    if a <= p <= b:
        return "CONFIRMA", f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}] ∈ [{a}, {b}] → CONFIRMA"
    return nivel(k, a if p < a else b)


def signo_neg(k):  # el report afirma MUJER < HOMBRE: ROMPE si punto ≥ 0
    p, lo, hi = c(k)
    d = "ROMPE" if p >= 0 else "CONFIRMA"
    return d, f"{k} {p:.4f} [{lo:.4f}, {hi:.4f}] (afirma < 0) → {d}"


def peor(partes):
    return max((x[0] for x in partes), key=ORD.get), " · ".join(x[1] for x in partes)


D = []


def fila(i, dom, dic, rid, det, parcial=False, unidad="proporción ponderada, persona elegida 18+"):
    p, lo, hi = c(rid)
    D.append([f"ASTRA5-U0-{i}", "afirmacion", dom, dic + ("-PARCIAL" if parcial else ""), P + rid + "-P", CALC,
              f"{p:.6f}", f"{lo:.6f}", f"{hi:.6f}", unidad, det + " RETROSPECTIVA."])


d, t = peor([nivel("CUENTA-MUJER", 0.586), nivel("CUENTA-HOMBRE", 0.680), nivel("AFORE-MUJER", 0.342),
             nivel("AFORE-HOMBRE", 0.514), signo_neg("CUENTA-BRECHA-MUJER-HOMBRE"), signo_neg("AFORE-BRECHA-MUJER-HOMBRE")])
fila("FIN-003", "DINERO", d, "CUENTA-BRECHA-MUJER-HOMBRE", "Spec §3 peor componente: " + t,
     unidad="diferencia de proporciones MUJER−HOMBRE, persona elegida 18+")
d, t = peor([nivel("AFORE-NAC", 0.422), nivel("AFORE-VOL-NAC", 0.079)])
fila("FIN-004", "DINERO", d, "AFORE-NAC", "Spec §3: " + t)
seg = c("SEGURO-NAC")[0]
otros = {k: c(k + "-NAC")[0] for k in ("CUENTA", "CRED-FORMAL", "AFORE")}
o = ("CONFIRMA", f"SEGURO-NAC {seg:.4f} menor que {', '.join(f'{k} {v:.4f}' for k, v in otros.items())} → CONFIRMA") \
    if all(seg < v for v in otros.values()) else ("ROMPE", "SEGURO-NAC no es el menor → ROMPE")
d, t = peor([nivel("SEGURO-NAC", 0.229), o])
fila("FIN-005", "DINERO", d, "SEGURO-NAC", "Spec §3: " + t)
d, t = peor([nivel("VEJEZ-GOB-NAC", 0.682), nivel("VEJEZ-TRAB-NAC", 0.673)])
fila("FIN-006", "DINERO", d, "VEJEZ-GOB-NAC", "Spec §3 (universo 18–70 por el pase): " + t)
d, t = nivel("NUNCACRED-RAZON-7-NAC", 0.384)
fila("FIN-009", "DINERO", d, "NUNCACRED-RAZON-7-NAC", "Spec §3: " + t + "; «aversión al riesgo» no observable.")
d, t = nivel("CUENTA-NAC", 0.630)
fila("FIN-010", "DINERO", d, "CUENTA-NAC", "Spec §3: " + t + "; la ola 2015 (44.1 %) no es input.", parcial=True)
td, tb = c("TC-DEPTO-NAC")[0], c("TC-BANC-NAC")[0]
o = ("CONFIRMA", f"TC-DEPTO {td:.4f} > TC-BANC {tb:.4f}") if td > tb else ("ROMPE", "TC-DEPTO ≤ TC-BANC → ROMPE")
d, t = peor([nivel("CUENTA-NAC", 0.630), nivel("CRED-FORMAL-NAC", 0.373), nivel("SEGURO-NAC", 0.229),
             nivel("AFORE-NAC", 0.422), nivel("TC-DEPTO-NAC", 0.226), nivel("TC-BANC-NAC", 0.157), o])
fila("FIN-034", "DINERO", d, "CRED-FORMAL-NAC", "Spec §3 peor componente: " + t)
d, t = peor([nivel("PRODUCTO-FORMAL-MUJER", 0.728), nivel("PRODUCTO-FORMAL-HOMBRE", 0.809),
             signo_neg("PRODUCTO-FORMAL-BRECHA-MUJER-HOMBRE")])
fila("CONS-039", "CONSUMO", d, "PRODUCTO-FORMAL-BRECHA-MUJER-HOMBRE", "Spec §3: " + t,
     unidad="diferencia de proporciones MUJER−HOMBRE, persona elegida 18+")
d, t = rango("TC-BANC-NAC", 0.10, 0.15)
fila("CONS-011", "CONSUMO", d, "TC-BANC-NAC", "Spec §3 rango: " + t)
d, t = nivel("CUENTA-NAC", 0.24)
fila("FAM-017", "FAMILIA_CUIDADOS", d, "CUENTA-NAC", "Spec §3: " + t +
     "; «36.6 % solo informal» y «la mitad» se citan del catálogo (E.5, ahorra_solo_informal), no se re-miden.", parcial=True)
p, lo, hi = c("TANDA-NAC")
d = "CONFIRMA" if lo >= 0.10 else ("ROMPE" if p < 0.05 else "MATIZA")
fila("FIN-002", "DINERO", d, "TANDA-NAC", f"Spec §3 umbral fijado ex ante: TANDA-NAC {p:.4f} [{lo:.4f}, {hi:.4f}]; IC95-INF ≥ 0.10 → {d}. Consume M23 como GASTABLE-COMO-PISO.")
d, t = nivel("TANDA-NAC", 0.30)
if d == "CONFIRMA":
    d = "MATIZA"
fila("CRPOP-056", "DINERO", d, "TANDA-NAC", "Spec §3 (ola del report 2012/2015, medida 2024; tope MATIZA): " + t)
p, lo, hi = c("CRED-FORMAL-NAC")
d, t = nivel("CRED-FORMAL-NAC", 0.495, ref=(1 - p, 1 - hi, 1 - lo))
fila("APUEST-015", "DINERO", d, "CRED-FORMAL-NAC",
     f"Spec §3: sin crédito formal = 1 − CRED-FORMAL-NAC = {1 - p:.4f} [{1 - hi:.4f}, {1 - lo:.4f}] vs 0.495 → {d}; "
     f"cifras Kueski/Aplazo no son de ENIF. RECHAZO-SINHISTORIAL-NAC {c('RECHAZO-SINHISTORIAL-NAC')[0]:.4f} (reportado).", parcial=True)
d, t = nivel("METAS-SIEMPRE-NAC", 0.40)
fila("TIME-001", "TIEMPO", d, "METAS-SIEMPRE-NAC", "Spec §3: " + t + "; «depende de la estabilidad del ingreso» no se contrasta aquí.")
dif = [c(k) for k in ("AFORE-DIF-CONSS-SINSS", "SEGURO-DIF-CONSS-SINSS", "CRED-VIV-DIF-CONSS-SINSS")]
d = "CONFIRMA" if all(x[1] > 0 for x in dif) else ("ROMPE" if any(x[0] <= 0 for x in dif) else "MATIZA")
fila("TIME-006", "TIEMPO", d, "AFORE-DIF-CONSS-SINSS",
     "Spec §3: CON-SS − SIN-SS afore/seguro/crédito vivienda = " + "; ".join(f"{x[0]:.4f} [{x[1]:.4f}, {x[2]:.4f}]" for x in dif)
     + f" → {d}. Oferta institucional ligada al empleo formal, no «previsión» como rasgo.",
     unidad="diferencia de proporciones CON-SS−SIN-SS, persona elegida 18+")
p, lo, hi = c("NOAFORE-RAZON-DIF-VEHICULO-SINTRAB-NAC")
g = c("NOAFORE-RAZON-G-SINTRAB-INGRESO-NAC")[0]
d = "CONFIRMA" if lo > 0 else ("ROMPE" if g >= 0.5 else "MATIZA")
fila("TIME-014", "TIEMPO", d, "NOAFORE-RAZON-DIF-VEHICULO-SINTRAB-NAC",
     f"Spec §3: G-VEHICULO − G-SINTRAB-INGRESO {p:.4f} [{lo:.4f}, {hi:.4f}]; G-SINTRAB-INGRESO {g:.4f} → {d}.",
     unidad="diferencia de proporciones entre razones, persona sin afore y sin cotización")
d, t = nivel("CUBRE-MES-NAC", 0.43)
fila("TIME-032", "TIEMPO", d, "CUBRE-MES-NAC", "Spec §3: " + t)
r4 = c("EFECTIVO-RAZON-4-NAC")
resto = {i: c(f"EFECTIVO-RAZON-{i}-NAC")[0] for i in (1, 2, 3, 5, 6, 7)}
d = "CONFIRMA" if all(r4[0] > v for v in resto.values()) else ("ROMPE" if r4[0] < 0.10 else "MATIZA")
moda = max(resto, key=resto.get)
fila("TRUST-019", "CONFIANZA", d, "EFECTIVO-RAZON-4-NAC",
     f"Spec §3: desconfianza en débito {r4[0]:.4f} [{r4[1]:.4f}, {r4[2]:.4f}]; moda = código {moda} ({resto[moda]:.4f}) → {d}. "
     "Mecanismo (crisis 1994/2008) no observable; la parte P7_9 queda DIFERIDA por R06.", parcial=True,
     unidad="proporción entre quienes prefieren efectivo (5.13 válido)")

cab = ["id", "clase", "dominio", "dictamen", "resultado_id", "calc", "punto", "ic95_inf", "ic95_sup", "unidad", "detalle"]
out = RAIZ / "forense/analisis/medicion-carriles-2/ENIF2024-dictamenes.tsv"
out.write_text("\t".join(cab) + "\n" + "".join("\t".join(x) + "\n" for x in D), encoding="utf-8")
for x in D:
    print(x[0], x[3])
