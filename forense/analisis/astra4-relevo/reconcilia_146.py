#!/usr/bin/env python3
"""Una fila por lectura del censo, sin confundir estado de pin con consumo."""
import csv
from collections import Counter
from pathlib import Path

DIR = Path(__file__).resolve().parent


def load(name):
    with (DIR / name).open(newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


inv = load("inventario-operativo.tsv")
proc = {r["slot"]: r for r in load("uso-efectivo-procedencia.tsv")}
cat = {r["slot"]: r for r in load("plan-catalogo-23.tsv")}
hist = {r["slot"]: r for r in load("dictamen-historicas.tsv")}
rows = []
for item in inv:
    slot = item["slot"]
    path = item["consumidor"].split(":", 1)[0]
    if slot in proc:
        group = "procedencia"
        outcome = proc[slot]["consulta_efectiva"]
        pending = proc[slot]["siguiente_operacion"]
        evidence = "uso-efectivo-procedencia.tsv"
    elif slot in cat:
        group = "catalogo"
        outcome = "PLAN-FECHADO; SIN-NUEVA-MEDIDA"
        pending = cat[slot]["dependencia"] + "; " + cat[slot]["operacion"]
        evidence = "plan-catalogo-23.tsv"
    elif path.startswith("forense/prereg-duelo-v2/"):
        group = "marco"
        outcome = "HISTORICO-SIN-RELEVO-PROPUESTO; NO-FIRMADO"
        pending = hist[slot]["siguiente_operacion"]
        evidence = "dictamen-historicas.tsv"
    elif item["tipo_uso"] == "celda_D":
        group = "celda_D"
        outcome = "LEGACY-ACTIVA; ESCRITOR-PROPIO-PENDIENTE"
        pending = "cotejar contrato y reserva de la celda; escritor y sello específicos; no editar YAML sellado"
        evidence = "contratos-otros-consumidores.md"
    else:
        group = "motor"
        outcome = "LEGACY-ACTIVA; NO-ADOPTADA"
        pending = item["siguiente_operacion"]
        evidence = "inventario-operativo.tsv"
        if slot in {"RES-0001", "RES-0002", "RES-0007", "RES-0008"}:
            outcome = "NO-EQUIVALENTE-PAGO; LEGACY-ACTIVA"
            pending = "P8_3/P8_4 no miden pago o normalidad; nueva pregunta/estimando y CALC propio"
            evidence = "lote-encig23-p83.md"
        elif slot in {"RES-0029", "RES-0030"}:
            outcome = "LEGACY-HISTORICA-ENNViH; NO-EQUIVALENTE-ENIF2024"
            pending = "firma de mesa de historia o CALC misma fuente/ola/acervo; ENIF 2024 mide flujo distinto"
            evidence = "forense/prereg-caja/ENIF-TIENE-AHORROS-spec-v1_0.md"
    rows.append(dict(slot=slot, grupo=group, consumidor=item["consumidor"],
                     generacion_censada=item["generacion_actual"], valor_legacy=item["valor_actual"],
                     estado_efectivo=outcome, trazabilidad="PIN-NO-ACREDITA-CONSUMO",
                     evidencia=evidence, dependencia_y_operacion=pending))

assert len(rows) == 146 and len({r["slot"] for r in rows}) == 146
assert Counter(r["grupo"] for r in rows) == {"motor": 34, "celda_D": 6,
    "catalogo": 23, "procedencia": 40, "marco": 43}
fields = list(rows[0])
with (DIR / "reconciliacion-146.tsv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(dict(Counter(r["grupo"] for r in rows)))
