#!/usr/bin/env python3
"""Dictamen por fila, sin editar fuentes selladas ni inferir que todo es historia."""
import csv
from pathlib import Path

BASE = Path(__file__).parent
rows = list(csv.DictReader((BASE / "inventario-operativo.tsv").open(), delimiter="\t"))
columns = ("slot", "consumidor", "tipo_uso", "dictamen_propuesto", "razon_individual", "siguiente_operacion")
with (BASE / "dictamen-historicas.tsv").open("w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=columns, delimiter="\t")
    writer.writeheader()
    for row in rows:
        if "HISTORICO" not in row["siguiente_operacion"]:
            continue
        consumer = row["consumidor"]
        if consumer.startswith("forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:"):
            verdict = "HISTORICO-SIN-RELEVO-PROPUESTO"
            reason = (
                f"{row['tipo_uso']} de la celda retrospectiva sellada {consumer.split(':', 1)[1]}; "
                "el marco congelado se conserva y no es parámetro de consumo nuevo del motor. "
                "No se reescribe ni se simula cita GEN2."
            )
            next_op = "FIRMA-DE-MESA-DEL-DICTAMEN; conservar marco y sello"
        elif consumer.startswith("milpa/procedencia.yaml:"):
            verdict = "NO-HISTORICO-CONSUMO-POTENCIAL"
            reason = (
                f"{row['tipo_uso']} en {consumer.split(':', 1)[1]}; "
                "milpa/src/procedencia.py carga este archivo y consumibles() solo excluye "
                "PENDIENTE, GATE_ID y REFUTADO_POR_COTA. Sin prueba por llave de exclusión "
                "no procede llamarlo histórico."
            )
            next_op = "COTEJAR-CLASE-Y-CONSULTA-POR-LLAVE; CALC-O-DICTAMEN-ESPECIFICO"
        else:
            raise ValueError(consumer)
        writer.writerow(dict(slot=row["slot"], consumidor=consumer,
                             tipo_uso=row["tipo_uso"], dictamen_propuesto=verdict,
                             razon_individual=reason, siguiente_operacion=next_op))
