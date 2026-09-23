#!/usr/bin/env python3
"""Clasifica los 45 IDs INE del manifiesto por objeto, sin abrir payloads."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]


def classify(identifier):
    if identifier == "ine_conteos_censales_participacion_2024":
        return "conteo_censal", "MEDIDO:CALC-INE-PISOS-2024-0001"
    if identifier.startswith("ine_conteos_censales_"):
        return "modalidad_especial", "DICTAMINADO:universo_separado_no_sumar_a_cuadernillos"
    if identifier.startswith("ine_fiscalizacion_"):
        return "fiscalizacion_campana", "DICTAMINADO:agenda_gasto_no_es_participacion"
    if identifier.startswith("ine_prep2024_"):
        return "prep_preliminar", "DICTAMINADO:PREP_no_es_computo_definitivo"
    if identifier.startswith("ine_mge_"):
        return "cartografia_version_2016", "DICTAMINADO:llaves_geograficas_no_son_voto"
    if identifier.startswith("ine_deoe_"):
        return "catalogo_casillas_2024", "DICTAMINADO:padron_lista_nominal_no_es_marca_de_voto"
    if identifier.startswith("ine_cg_"):
        return "calendario_o_acuerdo", "DICTAMINADO:fecha_de_eleccion_no_es_participacion"
    raise ValueError(f"ID INE sin dictamen: {identifier}")


def main():
    entries = yaml.safe_load((ROOT / "data/manifiesto.yaml").read_text())
    rows = []
    for entry in entries:
        identifier = entry.get("id", "")
        if not identifier.startswith("ine_"):
            continue
        objeto, dictamen = classify(identifier)
        rows.append((identifier, entry.get("archivo", ""), objeto, dictamen))
    if len(rows) != 45:
        raise ValueError(f"universo INE cambió: {len(rows)}; revisar clasificación")
    writer = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    writer.writerow(("id_manifiesto", "archivo", "objeto", "dictamen"))
    writer.writerows(rows)


if __name__ == "__main__":
    main()
