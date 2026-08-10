#!/usr/bin/env python3
"""Construye una vista semántica enriquecida sin modificar el baseline."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from .baseline import leer_tsv, validar_baseline
except ImportError:
    from baseline import leer_tsv, validar_baseline


EVIDENCE_STATES = {
    "INDEXADO_NO_DESCARGADO", "DESCARGADO_NO_ABIERTO", "ABIERTO_SIN_MAPEO",
    "MAPEADO_PARCIAL", "MAPEADO_COMPLETO", "NO_ACCESIBLE",
    "MECANISMO_NO_EJECUTADO", "NO_REPRODUCIBLE",
}
ADJUDICATIONS = {"CONFIRMADA", "NEGATIVA", "CANDIDATA", "CONFLICTO_MATERIAL"}
CAPACITIES = {
    "MEDIBLE_AHORA", "PARAMETRIZABLE_AHORA", "REQUIERE_ANALISIS", "REQUIERE_DATO",
    "REQUIERE_DECISION", "SIN_RUTA_VIABLE_ACTUAL", "NO_USAR_PARA_RELACION",
}


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader(); writer.writerows(rows)


def derive_evidence_state(relation: dict[str, str], report_ref: str) -> tuple[str, str]:
    legacy = relation.get("clasificacion_relacion", "")
    layer3 = relation.get("capa3_disco_real", "")
    layer4 = relation.get("capa4_apertura_mapeo", "")
    if legacy == "NO_ACCESIBLE":
        return "NO_ACCESIBLE", "legacy NO_ACCESIBLE preservado"
    if legacy == "NEGATIVA":
        return "MAPEADO_COMPLETO", "negativa legacy con procedencia aceptada"
    if legacy == "CONFIRMADA":
        return "MAPEADO_COMPLETO", "confirmada legacy con procedencia aceptada"
    combined = f"{layer3};{layer4}".upper()
    if "ABIERTO-SIN-MAPEO" in combined:
        return "ABIERTO_SIN_MAPEO", "estado explícito de apertura"
    if "EXISTE" in layer4.upper() or "MAPE" in layer4.upper():
        return "MAPEADO_PARCIAL", "apertura/mapeo parcial explícito"
    if report_ref != "NO_DETERMINADO":
        return "DESCARGADO_NO_ABIERTO", "reporte neutral estructural, sin mapeo semántico automático"
    if any(token in combined for token in ("INDEXADO", "NO_REFERENCIADO")):
        return "INDEXADO_NO_DESCARGADO", "indexación declarada sin apertura exacta vinculada"
    if any(token in layer3.upper() for token in ("EXISTE", "COINCIDE", "INTEGRO")):
        return "DESCARGADO_NO_ABIERTO", "presencia en disco sin reporte exacto vinculado"
    return "MECANISMO_NO_EJECUTADO", "sin mecanismo exacto ejecutado"


def derive_capacity(legacy: str, evidence_state: str, utility: dict[str, str]) -> tuple[str, str]:
    if legacy == "NEGATIVA":
        return "NO_USAR_PARA_RELACION", "negativa legacy preservada"
    if legacy == "NO_ACCESIBLE":
        return "SIN_RUTA_VIABLE_ACTUAL", "acceso bloqueado explícitamente; no se convierte en negativa"
    if utility.get("requiere_decision") == "SI":
        return "REQUIERE_DECISION", "decisión humana vinculada"
    if legacy == "CONFIRMADA":
        return "MEDIBLE_AHORA", "medición descriptiva posible; parametrización sigue separada"
    if evidence_state in {"MAPEADO_PARCIAL", "ABIERTO_SIN_MAPEO"}:
        return "REQUIERE_ANALISIS", "contenido abierto requiere especificación/análisis"
    if evidence_state in {"NO_REPRODUCIBLE", "NO_ACCESIBLE"}:
        return "SIN_RUTA_VIABLE_ACTUAL", "bloqueo verificable"
    return "REQUIERE_DATO", "falta adquisición, apertura o evidencia exacta"


def build_bootstrap(
    baseline_dir: Path,
    mapping_path: Path,
    declarations_path: Path,
    universe_path: Path,
    asset_states_path: Path,
    output_path: Path,
) -> list[dict[str, str]]:
    result = validar_baseline(baseline_dir)
    if not result["ok"]:
        raise ValueError(f"baseline inválido: {result['errores']}")
    relations = leer_tsv(baseline_dir / "relaciones.tsv")
    evidence = leer_tsv(baseline_dir / "evidencias.tsv")
    utilities = {row["relacion_id"]: row for row in leer_tsv(baseline_dir / "utilidad-modelo.tsv")}
    mappings = read_tsv(mapping_path)
    declarations = read_tsv(declarations_path)
    universe = {row["activo_id"]: row for row in read_tsv(universe_path)}
    states = {row["activo_id"]: row for row in read_tsv(asset_states_path)}

    mapping_by_need: dict[str, set[str]] = defaultdict(set)
    for row in mappings:
        mapping_by_need[row["necesidad_id"]].add(row["objeto_modelo_origen"])
    evidence_by_relation: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence:
        evidence_by_relation[row["relacion_id"]].append(row)
    assets_by_manifest: dict[str, set[str]] = defaultdict(set)
    for row in declarations:
        identifier = row.get("identificador_declarado", "")
        if identifier and identifier != "NO_DETERMINADO":
            assets_by_manifest[identifier].add(row["activo_id"])

    rows: list[dict[str, str]] = []
    for relation in sorted(relations, key=lambda row: row["relacion_id"]):
        rid = relation["relacion_id"]
        need = relation["necesidad_id"]
        permitted_objects = mapping_by_need.get(need, set())
        structured_objects = {
            row.get("objeto_modelo_origen", "") for row in evidence_by_relation[rid]
            if row.get("objeto_modelo_origen", "") in permitted_objects
        }
        model_object = next(iter(structured_objects)) if len(structured_objects) == 1 else (next(iter(permitted_objects)) if len(permitted_objects) == 1 else "NO_DETERMINADO")
        linked_assets: list[str] = []
        manifest_id = relation.get("id_manifiesto", "")
        expected_hash = relation.get("sha256_fuente", "").lower()
        if manifest_id not in {"", "NO_DETERMINADO"}:
            for active_id in sorted(assets_by_manifest.get(manifest_id, set())):
                asset_hash = universe.get(active_id, {}).get("hash_local", "").lower()
                if expected_hash not in {"", "no_determinado"} and asset_hash == expected_hash:
                    linked_assets.append(active_id)
        report_refs = sorted({states[active_id]["reporte_inspeccion_ref"] for active_id in linked_assets if active_id in states and states[active_id]["reporte_inspeccion_ref"] not in {"", "NO_APLICA", "NO_DETERMINADO"}})
        report_ref = ";".join(report_refs) if report_refs else "NO_DETERMINADO"
        evidence_state, evidence_rule = derive_evidence_state(relation, report_ref)
        legacy = relation["clasificacion_relacion"]
        adjudication = legacy if legacy in {"CONFIRMADA", "NEGATIVA", "CANDIDATA"} else "CANDIDATA"
        capacity, capacity_rule = derive_capacity(legacy, evidence_state, utilities[rid])
        if not ({evidence_state} <= EVIDENCE_STATES and {adjudication} <= ADJUDICATIONS and {capacity} <= CAPACITIES):
            raise AssertionError(f"taxonomía inválida: {rid}")
        rows.append({
            "relacion_id": rid,
            "necesidad_id": need,
            "fuente_canonica_normalizada": relation["fuente_canonica_normalizada"],
            "objeto_evidencia_id_canonico": relation["objeto_evidencia_id_canonico"],
            "objeto_modelo_origen": model_object,
            "objetos_modelo_permitidos": ";".join(sorted(permitted_objects)) or "NO_DETERMINADO",
            "universo_declarado": "SI",
            "universo_adquirido": "SI" if linked_assets else "NO_DETERMINADO",
            "universo_inspeccionado": "SI" if report_ref != "NO_DETERMINADO" else "NO_DETERMINADO",
            "universo_semantico": "SI",
            "universo_productivo": "SI" if capacity in {"MEDIBLE_AHORA", "PARAMETRIZABLE_AHORA"} else "NO",
            "estado_evidencia": evidence_state,
            "adjudicacion_semantica": adjudication,
            "capacidad_productiva": capacity,
            "clasificacion_relacion_legacy": legacy,
            "estado_productivo_legacy": utilities[rid]["estado_productivo"],
            "activo_id_vinculado": ";".join(linked_assets) if linked_assets else "NO_DETERMINADO",
            "reporte_inspeccion_ref": report_ref,
            "regla_derivacion": f"{evidence_rule};{capacity_rule}",
            "reserva": "Reporte neutral no cambia adjudicación; identidad solo por id_manifiesto+hash exactos",
            "destino_procesamiento": "CLASIFICAR_TRABAJO" if legacy == "CANDIDATA" else ("BLOQUEO_ACCESO_PRESERVADO" if legacy == "NO_ACCESIBLE" else "TERMINAL_LEGACY_PRESERVADO"),
        })
    fields = list(rows[0]) if rows else ["relacion_id"]
    write_tsv(output_path, rows, fields)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--declarations", type=Path, required=True)
    parser.add_argument("--universe", type=Path, required=True)
    parser.add_argument("--asset-states", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build_bootstrap(args.baseline.resolve(), args.mapping.resolve(), args.declarations.resolve(), args.universe.resolve(), args.asset_states.resolve(), args.output.resolve())
    print(json.dumps({"ok": True, "relaciones": len(rows)}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
