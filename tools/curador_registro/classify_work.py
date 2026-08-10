#!/usr/bin/env python3
"""Clasifica trabajo pendiente con reglas explícitas almacenadas en datos."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


WORK_TYPES = {
    "CURADURIA_FUENTE", "APERTURA_EXTRACCION", "ANALISIS_MEDICION", "PARAMETRIZACION",
    "BUSQUEDA_DIRIGIDA", "ESCALAMIENTO_SEMANTICO", "DECISION_HUMANA", "BLOQUEO",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def matches(row: dict[str, str], conditions: dict[str, Any]) -> bool:
    for field, expected in conditions.items():
        actual = row.get(field, "")
        if isinstance(expected, list) and actual not in expected:
            return False
        if isinstance(expected, str) and actual != expected:
            return False
    return True


def classify(bootstrap_path: Path, baseline_dir: Path, rules_path: Path, output_path: Path) -> list[dict[str, str]]:
    bootstrap = {row["relacion_id"]: row for row in read_tsv(bootstrap_path)}
    relations = read_tsv(baseline_dir / "relaciones.tsv")
    utilities = {row["relacion_id"]: row for row in read_tsv(baseline_dir / "utilidad-modelo.tsv")}
    candidate_evidence: dict[str, dict[str, str]] = {}
    for row in read_tsv(baseline_dir / "evidencias.tsv"):
        if row.get("clasificacion_relacion") != "CANDIDATA":
            continue
        rid = row["relacion_id"]
        if rid in candidate_evidence:
            raise ValueError(f"más de una evidencia candidata para {rid}")
        candidate_evidence[rid] = row
    rules = json.loads(rules_path.read_text(encoding="utf-8"))["rules"]
    output: list[dict[str, str]] = []
    for relation in sorted((row for row in relations if row["clasificacion_relacion"] == "CANDIDATA"), key=lambda row: row["relacion_id"]):
        rid = relation["relacion_id"]
        context = {**relation, **bootstrap[rid], **{f"utilidad_{key}": value for key, value in utilities[rid].items()}}
        selected = next((rule for rule in rules if matches(context, rule.get("when", {}))), None)
        if selected is None:
            raise ValueError(f"sin regla de clasificación: {rid}")
        work_type = selected["tipo_trabajo"]
        if work_type not in WORK_TYPES:
            raise ValueError(f"tipo de trabajo inválido: {work_type}")
        evidence = candidate_evidence.get(rid)
        if evidence is None:
            raise ValueError(f"sin evidencia original para {rid}")
        original_action = evidence.get("siguiente_accion", "")
        utility = utilities[rid]
        if not original_action or utility.get("siguiente_accion") != original_action:
            raise ValueError(f"acción original no reconcilia evidencia/utilidad: {rid}")
        output.append({
            "relacion_id": rid,
            "tipo_trabajo": work_type,
            "siguiente_accion": original_action,
            "siguiente_accion_original": original_action,
            "evidencia_ref_accion_original": utility.get("evidencia_ref", ""),
            "evidencia_ref_evidencia_original": evidence.get("evidencia_ref", ""),
            "input_requerido": utility.get("verificacion_requerida", ""),
            "input_requerido_original": utility.get("verificacion_requerida", ""),
            "reserva": utility.get("reserva", ""),
            "reserva_original": utility.get("reserva", ""),
            "siguiente_accion_tipificada": selected["siguiente_accion"].format(**context),
            "input_requerido_clasificacion": selected["input_requerido"].format(**context),
            "criterio_cierre": selected["criterio_cierre"].format(**context),
            "prioridad_operativa": selected["prioridad_operativa"],
            "regla_clasificacion_id": selected["rule_id"],
            "reserva_clasificacion": selected["reserva"],
        })
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        fields = list(output[0]) if output else ["relacion_id"]
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(output)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = classify(args.bootstrap.resolve(), args.baseline.resolve(), args.rules.resolve(), args.output.resolve())
    counts: dict[str, int] = {}
    for row in rows: counts[row["tipo_trabajo"]] = counts.get(row["tipo_trabajo"], 0) + 1
    print(json.dumps({"ok": True, "relaciones_clasificadas": len(rows), "tipos": counts}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
