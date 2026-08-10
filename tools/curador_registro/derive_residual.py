#!/usr/bin/env python3
"""Deriva una cola residual accionable sin crear una segunda verdad semántica."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


FIELDS = [
    "cola_id", "capa", "entidad_id", "relacion_id", "tipo_trabajo",
    "semantic_run_id", "estado_ejecucion", "reporte_ejecucion_ref",
    "intentos_reales", "objetos_abiertos", "siguiente_accion_original",
    "siguiente_accion", "siguiente_accion_tipificada",
    "input_requerido", "input_requerido_original", "criterio_cierre",
    "prioridad_operativa", "reserva", "reserva_original",
    "evidencia_ref_accion_original", "evidencia_ref_evidencia_original",
]


def stable_id(*parts: str) -> str:
    return "CRES-" + hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def derive(
    work_path: Path,
    decisions_path: Path,
    production_path: Path,
    semantic_results_path: Path | None = None,
    semantic_run_id: str = "NO_APLICA",
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    semantic_results = {
        row["relacion_id"]: row for row in read_tsv(semantic_results_path)
    } if semantic_results_path is not None else {}
    for item in read_tsv(work_path):
        rid = item["relacion_id"]
        execution = semantic_results.get(rid)
        if semantic_results and execution is None:
            raise ValueError(f"resultado semántico faltante: {rid}")
        rows.append({
            "cola_id": stable_id("SEMANTICO", rid), "capa": "UNIVERSO_SEMANTICO",
            "entidad_id": rid, "relacion_id": rid, "tipo_trabajo": item["tipo_trabajo"],
            "semantic_run_id": semantic_run_id,
            "estado_ejecucion": execution["estado_cierre"] if execution else "NO_CORRIDA",
            "reporte_ejecucion_ref": execution["reporte_neutral_ref"] if execution else "NO_DETERMINADO",
            "intentos_reales": execution["intentos_reales"] if execution else "0",
            "objetos_abiertos": execution["objetos_abiertos"] if execution else "0",
            "siguiente_accion_original": item["siguiente_accion_original"],
            "siguiente_accion": execution["receta_continuacion"] if execution else item["siguiente_accion"],
            "input_requerido": item["input_requerido"],
            "siguiente_accion_tipificada": item["siguiente_accion_tipificada"],
            "input_requerido_original": item["input_requerido_original"],
            "criterio_cierre": item["criterio_cierre"], "prioridad_operativa": item["prioridad_operativa"],
            "reserva": item["reserva"], "reserva_original": item["reserva_original"],
            "evidencia_ref_accion_original": item["evidencia_ref_accion_original"],
            "evidencia_ref_evidencia_original": item["evidencia_ref_evidencia_original"],
        })
    for decision in read_tsv(decisions_path):
        if decision.get("estado_decision") != "PENDIENTE":
            continue
        decision_id, rid = decision["decision_id"], decision["relacion_id"]
        rows.append({
            "cola_id": stable_id("DECISION", decision_id), "capa": "DECISION_HUMANA",
            "entidad_id": decision_id, "relacion_id": rid, "tipo_trabajo": "DECISION_HUMANA",
            "semantic_run_id": "NO_APLICA", "estado_ejecucion": "REQUIERE_DECISION_HUMANA",
            "reporte_ejecucion_ref": "NO_APLICA", "intentos_reales": "0", "objetos_abiertos": "0",
            "siguiente_accion_original": "Resolver literalmente la pregunta registrada sin inventar una alternativa adicional.",
            "siguiente_accion": "Resolver literalmente la pregunta registrada sin inventar una alternativa adicional.",
            "siguiente_accion_tipificada": "Resolver decisión humana pendiente.",
            "input_requerido": decision["pregunta_decision"] + " | alternativas=" + decision["alternativas"],
            "input_requerido_original": decision["pregunta_decision"] + " | alternativas=" + decision["alternativas"],
            "criterio_cierre": "Decisión humana explícita con efecto sobre el modelo y procedencia conservada.",
            "prioridad_operativa": "P1_DECISION_PENDIENTE", "reserva": decision["procedencia"],
            "reserva_original": decision["procedencia"],
            "evidencia_ref_accion_original": decision["procedencia"],
            "evidencia_ref_evidencia_original": decision["procedencia"],
        })
    for product in read_tsv(production_path):
        if product.get("estado") != "NO_DETERMINADO":
            continue
        product_id, rid = product["produccion_id"], product["relacion_id"]
        rows.append({
            "cola_id": stable_id("PRODUCCION", product_id), "capa": "UNIVERSO_PRODUCTIVO",
            "entidad_id": product_id, "relacion_id": rid, "tipo_trabajo": "ESCALAMIENTO_SEMANTICO",
            "semantic_run_id": "NO_APLICA", "estado_ejecucion": "BLOQUEADA_INPUT_FALTANTE",
            "reporte_ejecucion_ref": "NO_APLICA", "intentos_reales": "0", "objetos_abiertos": "0",
            "siguiente_accion_original": "Fijar población, tabla, unidad y ponderador de la especificación; después emitir una nueva especificación opaca.",
            "siguiente_accion": "Fijar población, tabla, unidad y ponderador de la especificación; después emitir una nueva especificación opaca.",
            "siguiente_accion_tipificada": "Completar especificación productiva material.",
            "input_requerido": product["reserva"],
            "input_requerido_original": product["reserva"],
            "criterio_cierre": "Elección explícita de denominador y campos materiales, o decisión de no calcular.",
            "prioridad_operativa": "P1_BLOQUEO_MATERIAL", "reserva": "El analista no puede elegir el universo ni redefinir el estimando.",
            "reserva_original": product["reserva"],
            "evidencia_ref_accion_original": product.get("evidencia_ref", "NO_DETERMINADO"),
            "evidencia_ref_evidencia_original": product.get("evidencia_ref", "NO_DETERMINADO"),
        })
    return sorted(rows, key=lambda row: row["cola_id"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--production", type=Path, required=True)
    parser.add_argument("--semantic-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    semantic_manifest_path = args.semantic_manifest.resolve()
    semantic_manifest = json.loads(semantic_manifest_path.read_text(encoding="utf-8"))
    semantic_results = (
        semantic_manifest_path.parent / "runs" / semantic_manifest["run_id"] / "resultados-acciones.tsv"
    )
    rows = derive(
        args.work.resolve(), args.decisions.resolve(), args.production.resolve(),
        semantic_results, semantic_manifest["run_id"],
    )
    with args.output.resolve().open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader(); writer.writerows(rows)
    print(f"residuales={len(rows)} semanticas={sum(row['capa'] == 'UNIVERSO_SEMANTICO' for row in rows)} decisiones={sum(row['capa'] == 'DECISION_HUMANA' for row in rows)} productivas={sum(row['capa'] == 'UNIVERSO_PRODUCTIVO' for row in rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
