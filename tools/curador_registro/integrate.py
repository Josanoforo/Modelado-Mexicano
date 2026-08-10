#!/usr/bin/env python3
"""Integra propuestas semánticas solo si su expediente es auditable y consistente."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .baseline import ARCHIVOS_TSV, leer_tsv, validar_baseline
except ImportError:
    from baseline import ARCHIVOS_TSV, leer_tsv, validar_baseline


ALLOWED_ADJUDICATIONS = {"CONFIRMADA", "NEGATIVA", "CANDIDATA", "CONFLICTO_MATERIAL"}
PROPOSAL_SCHEMA = "adjudication-proposal.schema.json"
REPORT_SCHEMA = "inspection-report.schema.json"
TASK_SCHEMA = "inspector-task.schema.json"
CURATOR_TASK_SCHEMA = "semantic-curator-task.schema.json"
DOSSIER_REQUIRED = {
    "integracion-propuestas.tsv",
    "propuestas-recibidas.tsv",
    "reportes-recibidos.tsv",
    "tareas-inspeccion-recibidas.json",
    "tarea-curador-recibida.json",
    "procedencias-vinculadas.tsv",
}
EXPEDIENTE_REASONS = {
    "PROPUESTA_SCHEMA_INVALIDO", "PROPUESTA_ID_DUPLICADA", "RELACION_PROPUESTA_DUPLICADA",
    "WORKER_CURADOR_SIN_HASHES", "WORKER_CURADOR_HASH_INVALIDO", "TAREA_CURADOR_INEXISTENTE",
    "TAREA_CURADOR_SCHEMA_INVALIDO", "PROPUESTA_NO_ASIGNADA_A_CURADOR", "REPORTE_ORIGEN_INEXISTENTE",
    "REPORTE_ID_AMBIGUO", "REPORTE_SCHEMA_INVALIDO", "WORKER_INSPECTOR_SIN_HASHES",
    "WORKER_INSPECTOR_HASH_INVALIDO", "INPUT_TAREA_INEXISTENTE", "INPUT_TAREA_SCHEMA_INVALIDO",
    "JOIN_PROPUESTA_REPORTE_INVALIDO", "JOIN_REPORTE_TAREA_INVALIDO", "ACTIVO_INEXISTENTE",
    "RELACION_NO_ASIGNADA", "RELACION_ACTIVO_NO_ASIGNADO", "SNAPSHOT_OBSOLETO", "BASELINE_OBSOLETO",
    "CEGAMIENTO_SIN_EXCEPCION", "EXCEPCION_CEGAMIENTO_INEXISTENTE", "PROCEDENCIA_INEXISTENTE",
    "PROCEDENCIA_RELACION_INVALIDA",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_fields(path: Path) -> list[str]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t").fieldnames or [])


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def schema_errors(payload: dict[str, Any], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return [error.message for error in Draft202012Validator(schema).iter_errors(payload)]


def manifest_hashes(path: Path) -> dict[str, str] | None:
    if not path.is_file():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    hashes = payload.get("files") or payload.get("salidas") or payload.get("salidas_sha256") or payload
    return hashes if isinstance(hashes, dict) and all(isinstance(k, str) and isinstance(v, str) for k, v in hashes.items()) else None


def worker_file_ok(path: Path) -> tuple[bool, str]:
    hashes = manifest_hashes(path.parent / "hashes.json")
    if hashes is None:
        return False, "SIN_HASHES"
    expected = hashes.get(path.name)
    return (expected == sha256(path), "OK" if expected == sha256(path) else "HASH_INVALIDO")


def baseline_hashes(baseline_dir: Path) -> dict[str, str]:
    names = [*ARCHIVOS_TSV.values(), "baseline.json"]
    return {name: sha256(baseline_dir / name) for name in names if (baseline_dir / name).is_file()}


def report_sources(paths: list[Path]) -> list[tuple[dict[str, str], Path]]:
    result: list[tuple[dict[str, str], Path]] = []
    files: list[Path] = []
    for path in paths:
        files.extend(sorted(path.rglob("reporte-inspeccion.tsv")) if path.is_dir() else [path])
    for path in files:
        result.extend((row, path) for row in read_tsv(path))
    return result


def _json_dump(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def integrate(
    baseline_dir: Path,
    snapshot_path: Path,
    proposal_path: Path,
    report_paths: list[Path],
    output_dir: Path,
) -> dict[str, object]:
    """Valida, copia el expediente y nunca promueve una propuesta incompleta."""
    baseline_validation = validar_baseline(baseline_dir)
    if not baseline_validation["ok"]:
        raise ValueError(f"baseline inicial inválido: {baseline_validation['errores']}")
    before_hashes = baseline_hashes(baseline_dir)
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    snapshot_hash = snapshot["snapshot_t0_sha256"]
    baseline_hash = before_hashes["baseline.json"]
    schema_dir = Path(__file__).resolve().parent / "schemas"
    universe_dir = snapshot_path.parent

    relations = {row["relacion_id"]: row for row in leer_tsv(baseline_dir / "relaciones.tsv")}
    bootstrap = {row["relacion_id"]: row for row in read_tsv(baseline_dir / "bootstrap-semantico.tsv")}
    assets = {row["activo_id"]: row for row in read_tsv(universe_dir / "universo-declarado-t0.tsv")}
    exceptions = {row["excepcion_cegamiento_id"]: row for row in read_tsv(universe_dir / "excepciones-cegamiento.tsv")}
    evidence_rows = read_tsv(baseline_dir / "evidencias.tsv")
    provenance = {row["procedencia_id"]: row for row in evidence_rows}
    proposals = read_tsv(proposal_path)
    sources = report_sources(report_paths)
    reports_by_id: dict[str, list[tuple[dict[str, str], Path]]] = defaultdict(list)
    for report, path in sources:
        reports_by_id[report.get("reporte_id", "")].append((report, path))

    curator_input_path = proposal_path.parent / "input.json"
    curator_hash_ok, curator_hash_state = worker_file_ok(proposal_path)
    curator_input: dict[str, Any] | None = None
    curator_input_errors: list[str] = []
    if curator_input_path.is_file():
        curator_input = json.loads(curator_input_path.read_text(encoding="utf-8"))
        curator_input_errors = schema_errors(curator_input, schema_dir / CURATOR_TASK_SCHEMA)
        input_hash_ok, _ = worker_file_ok(curator_input_path)
        if not input_hash_ok:
            curator_input_errors.append("input.json no está cubierto por hashes.json")
    assignments = {
        (row.get("relacion_id", ""), row.get("reporte_inspeccion_ref", ""))
        for row in (curator_input or {}).get("asignaciones", [])
    }
    global_expediente_errors: list[str] = []
    if not curator_hash_ok:
        global_expediente_errors.append("WORKER_CURADOR_SIN_HASHES" if curator_hash_state == "SIN_HASHES" else "WORKER_CURADOR_HASH_INVALIDO")
    if curator_input is None:
        global_expediente_errors.append("TAREA_CURADOR_INEXISTENTE")
    elif curator_input_errors:
        global_expediente_errors.append("TAREA_CURADOR_SCHEMA_INVALIDO")
    elif curator_input.get("snapshot_t0_sha256") != snapshot_hash:
        global_expediente_errors.append("SNAPSHOT_OBSOLETO")
    elif curator_input.get("baseline_sha256") != baseline_hash:
        global_expediente_errors.append("BASELINE_OBSOLETO")

    proposal_ids = Counter(row.get("propuesta_id", "") for row in proposals)
    proposal_relations = Counter(row.get("relacion_id", "") for row in proposals)
    decisions: list[dict[str, str]] = []
    accepted_changes: list[dict[str, str]] = []
    used_reports: dict[tuple[str, str, str, str], dict[str, str]] = {}
    used_tasks: dict[str, dict[str, Any]] = {}
    used_provenance: dict[str, dict[str, str]] = {}

    for proposal in proposals:
        reasons: list[str] = []
        rid = proposal.get("relacion_id", "")
        report_id = proposal.get("reporte_inspeccion_ref", "")
        task_id = proposal.get("tarea_observacion_id", "")
        asset_id = proposal.get("activo_id", "")
        object_id = proposal.get("objeto_logico_id", "")
        provenance_id = proposal.get("procedencia_ref", "")

        if schema_errors(proposal, schema_dir / PROPOSAL_SCHEMA): reasons.append("PROPUESTA_SCHEMA_INVALIDO")
        if proposal_ids[proposal.get("propuesta_id", "")] != 1: reasons.append("PROPUESTA_ID_DUPLICADA")
        if proposal_relations[rid] != 1: reasons.append("RELACION_PROPUESTA_DUPLICADA")
        reasons.extend(global_expediente_errors)
        if (rid, report_id) not in assignments: reasons.append("PROPUESTA_NO_ASIGNADA_A_CURADOR")
        if proposal.get("snapshot_t0_sha256") != snapshot_hash: reasons.append("SNAPSHOT_OBSOLETO")
        if proposal.get("baseline_sha256") != baseline_hash: reasons.append("BASELINE_OBSOLETO")
        if rid not in relations: reasons.append("RELACION_NO_ASIGNADA")
        if asset_id not in assets: reasons.append("ACTIVO_INEXISTENTE")

        report_entries = reports_by_id.get(report_id, [])
        metadata = {(r.get("tarea_observacion_id", ""), r.get("activo_id", ""), r.get("objeto_logico_id", "")) for r, _ in report_entries}
        if not report_entries:
            reasons.append("REPORTE_ORIGEN_INEXISTENTE")
        elif len(metadata) != 1:
            reasons.append("REPORTE_ID_AMBIGUO")
        else:
            report_path = report_entries[0][1]
            if any(schema_errors(report, schema_dir / REPORT_SCHEMA) for report, _ in report_entries): reasons.append("REPORTE_SCHEMA_INVALIDO")
            report_hash_ok, report_hash_state = worker_file_ok(report_path)
            if not report_hash_ok:
                reasons.append("WORKER_INSPECTOR_SIN_HASHES" if report_hash_state == "SIN_HASHES" else "WORKER_INSPECTOR_HASH_INVALIDO")
            input_path = report_path.parent / "input.json"
            task_payload: dict[str, Any] | None = None
            if not input_path.is_file():
                reasons.append("INPUT_TAREA_INEXISTENTE")
            else:
                task_payload = json.loads(input_path.read_text(encoding="utf-8"))
                input_hash_ok, _ = worker_file_ok(input_path)
                if schema_errors(task_payload, schema_dir / TASK_SCHEMA) or not input_hash_ok:
                    reasons.append("INPUT_TAREA_SCHEMA_INVALIDO")
                if task_payload.get("snapshot_t0_sha256") != snapshot_hash:
                    reasons.append("SNAPSHOT_OBSOLETO")
                used_tasks[task_id] = task_payload
            report_meta = next(iter(metadata))
            if report_meta != (task_id, asset_id, object_id): reasons.append("JOIN_PROPUESTA_REPORTE_INVALIDO")
            if task_payload is not None and (
                task_payload.get("tarea_observacion_id"), task_payload.get("activo_id"), task_payload.get("objeto_logico_id")
            ) != report_meta:
                reasons.append("JOIN_REPORTE_TAREA_INVALIDO")
            for report, _ in report_entries:
                used_reports[(report_id, report.get("afirmacion_tipo", ""), report.get("valor_o_descripcion", ""), report.get("evidencia_ref", ""))] = report

        # La tarea del curador prueba qué se le asignó, pero no puede crear el
        # vínculo epistemológico relación↔activo. Ese vínculo debe existir ya
        # en el bootstrap reconciliado; las candidatas sin activo exacto
        # permanecen no integrables.
        assigned_asset = bootstrap.get(rid, {}).get("activo_id_vinculado", "")
        if not assigned_asset or assigned_asset == "NO_DETERMINADO" or asset_id != assigned_asset:
            reasons.append("RELACION_ACTIVO_NO_ASIGNADO")

        prov = provenance.get(provenance_id)
        if prov is None: reasons.append("PROCEDENCIA_INEXISTENTE")
        elif prov.get("relacion_id") != rid: reasons.append("PROCEDENCIA_RELACION_INVALIDA")
        else: used_provenance[provenance_id] = prov

        exception_ref = proposal.get("excepcion_cegamiento_ref", "")
        if proposal.get("cegamiento_roto") == "SI":
            if not exception_ref.startswith("EXCEG-"): reasons.append("CEGAMIENTO_SIN_EXCEPCION")
            exception = exceptions.get(exception_ref)
            if exception is None or exception.get("tarea_observacion_id") != task_id:
                reasons.append("EXCEPCION_CEGAMIENTO_INEXISTENTE")
        if proposal.get("afirmacion_origen_tipo") == "INFERENCIA_PROPUESTA" and proposal.get("tratar_como_hecho") == "SI":
            reasons.append("INFERENCIA_COMO_HECHO")
        current = relations.get(rid, {}).get("clasificacion_relacion", "")
        proposed = proposal.get("adjudicacion_propuesta", current)
        if proposed not in ALLOWED_ADJUDICATIONS: reasons.append("ADJUDICACION_PROPUESTA_INVALIDA")
        if proposal.get("accion") == "CONSERVAR_ADJUDICACION" and proposed != current: reasons.append("CONSERVACION_NO_COINCIDE_CON_VIGENTE")
        if proposal.get("accion") == "CAMBIAR_ADJUDICACION":
            if current == "NEGATIVA" and proposal.get("evidencia_nueva_material") != "SI": reasons.append("NEGATIVO_SIN_EVIDENCIA_NUEVA")
            if current == "NO_ACCESIBLE" and proposed == "NEGATIVA": reasons.append("NO_ACCESIBLE_A_NEGATIVA")
        reasons = list(dict.fromkeys(reasons))
        status = "RECHAZADA" if reasons else "ACEPTADA"
        decision = dict(proposal)
        decision.update({
            "estado_validacion": status,
            "razones": ";".join(reasons) if reasons else "NINGUNA",
            "adjudicacion_vigente": current,
        })
        decisions.append(decision)
        if not reasons and proposal.get("accion") == "CAMBIAR_ADJUDICACION" and proposed != current:
            accepted_changes.append({"relacion_id": rid, "adjudicacion": proposed})

    with tempfile.TemporaryDirectory(prefix="barrido-integracion-") as tmp:
        candidate = Path(tmp) / "baseline"
        candidate.mkdir()
        for filename in [*ARCHIVOS_TSV.values(), "baseline.json"]:
            shutil.copy2(baseline_dir / filename, candidate / filename)
        # No existe aún un transformador que actualice tablas, procedencia y manifest atómicamente.
        if accepted_changes:
            for decision in decisions:
                if decision["estado_validacion"] == "ACEPTADA" and decision.get("accion") == "CAMBIAR_ADJUDICACION":
                    decision["estado_validacion"] = "RECHAZADA"
                    decision["razones"] = "TRANSFORMADOR_ATOMICO_NO_PROVISTO"
            accepted_changes = []
        candidate_validation = validar_baseline(candidate)
        candidate_hashes = baseline_hashes(candidate)

    after_hashes = baseline_hashes(baseline_dir)
    differences = sorted(name for name in set(before_hashes) | set(after_hashes) if before_hashes.get(name) != after_hashes.get(name))
    baseline_unchanged = {"ok": not differences, "hashes_antes": before_hashes, "hashes_despues": after_hashes, "diferencias": differences}
    expediente_errors = sorted({
        *global_expediente_errors,
        *(reason for row in decisions for reason in row["razones"].split(";") if reason in EXPEDIENTE_REASONS),
    })

    output_dir.mkdir(parents=True, exist_ok=True)
    proposal_fields = tsv_fields(proposal_path)
    decision_fields = proposal_fields + [field for field in ("estado_validacion", "razones", "adjudicacion_vigente") if field not in proposal_fields]
    shutil.copy2(proposal_path, output_dir / "propuestas-recibidas.tsv")
    write_tsv(output_dir / "integracion-propuestas.tsv", decision_fields, decisions)
    report_rows = sorted(used_reports.values(), key=lambda row: (row.get("reporte_id", ""), row.get("afirmacion_tipo", ""), row.get("valor_o_descripcion", "")))
    report_fields = list(report_rows[0]) if report_rows else list(json.loads((schema_dir / REPORT_SCHEMA).read_text(encoding="utf-8"))["required"])
    write_tsv(output_dir / "reportes-recibidos.tsv", report_fields, report_rows)
    _json_dump(output_dir / "tareas-inspeccion-recibidas.json", list(used_tasks.values()))
    _json_dump(output_dir / "tarea-curador-recibida.json", curator_input or {})
    provenance_rows = sorted(used_provenance.values(), key=lambda row: row.get("procedencia_id", ""))
    provenance_fields = list(evidence_rows[0]) if evidence_rows else []
    write_tsv(output_dir / "procedencias-vinculadas.tsv", provenance_fields, provenance_rows)

    contracts = {
        name: {"ruta": f"tools/curador_registro/schemas/{name}", "sha256": sha256(schema_dir / name)}
        for name in (PROPOSAL_SCHEMA, REPORT_SCHEMA, TASK_SCHEMA, CURATOR_TASK_SCHEMA)
    }
    result: dict[str, object] = {
        "ok": bool(candidate_validation["ok"] and baseline_unchanged["ok"] and not expediente_errors),
        "snapshot_t0_sha256": snapshot_hash,
        "baseline_sha256": baseline_hash,
        "propuestas": len(proposals),
        "aceptadas_sin_cambio_estado": sum(row["estado_validacion"] == "ACEPTADA" for row in decisions),
        "rechazadas": sum(row["estado_validacion"] == "RECHAZADA" for row in decisions),
        "cambios_adjudicacion_integrados": 0,
        "expediente_completo": not expediente_errors,
        "errores_expediente": expediente_errors,
        "contratos": contracts,
        "validacion_copia_completa": candidate_validation,
        "hashes_copia_candidata": candidate_hashes,
        "validacion_baseline_original_intacto": baseline_unchanged,
    }
    semantic_run_id = str((curator_input or {}).get("run_id", ""))
    semantic_execution_ref = str((curator_input or {}).get("expediente_semantico_ref", ""))
    semantic_execution_sha = str((curator_input or {}).get("expediente_semantico_sha256", ""))
    if semantic_run_id:
        result["semantic_run_id"] = semantic_run_id
    if semantic_execution_ref:
        result["expediente_semantico_ref"] = semantic_execution_ref
        result["expediente_semantico_sha256"] = semantic_execution_sha
    dossier_files = sorted(DOSSIER_REQUIRED)
    dossier_hashes = {name: sha256(output_dir / name) for name in dossier_files}
    dossier = {
        "version": 1,
        "snapshot_t0_sha256": snapshot_hash,
        "baseline_sha256": baseline_hash,
        "semantic_run_id": semantic_run_id,
        "expediente_semantico_ref": semantic_execution_ref,
        "expediente_semantico_sha256": semantic_execution_sha,
        "contratos": contracts,
        "archivos": dossier_hashes,
    }
    _json_dump(output_dir / "expediente-integracion.json", dossier)
    result["expediente_integracion_sha256"] = sha256(output_dir / "expediente-integracion.json")
    _json_dump(output_dir / "integracion-validada.json", result)
    return result


def validate_integration_dossier(repo_root: Path) -> list[str]:
    """Valida el expediente versionable sin confiar en sus booleanos declarados."""
    registry = repo_root / "data" / "curacion-registro"
    universe = repo_root / "data" / "curacion-universo"
    dossier_dir = registry / "integracion-barrido"
    errors: list[str] = []
    dossier_path = dossier_dir / "expediente-integracion.json"
    result_path = dossier_dir / "integracion-validada.json"
    if not dossier_path.is_file() or not result_path.is_file():
        return ["EXPEDIENTE_INTEGRACION_INEXISTENTE"]
    dossier = json.loads(dossier_path.read_text(encoding="utf-8"))
    result = json.loads(result_path.read_text(encoding="utf-8"))
    for name in DOSSIER_REQUIRED:
        path = dossier_dir / name
        expected = dossier.get("archivos", {}).get(name)
        if not path.is_file() or expected != sha256(path): errors.append(f"EXPEDIENTE_HASH_INVALIDO:{name}")
    snapshot = json.loads((universe / "snapshot-t0.json").read_text(encoding="utf-8"))
    current_baseline = baseline_hashes(registry)
    if dossier.get("snapshot_t0_sha256") != snapshot.get("snapshot_t0_sha256"): errors.append("EXPEDIENTE_SNAPSHOT_OBSOLETO")
    if dossier.get("baseline_sha256") != current_baseline.get("baseline.json"): errors.append("EXPEDIENTE_BASELINE_OBSOLETO")
    integrity = result.get("validacion_baseline_original_intacto", {})
    if not isinstance(integrity, dict) or integrity.get("hashes_antes") != integrity.get("hashes_despues") or integrity.get("diferencias"):
        errors.append("EXPEDIENTE_BASELINE_INTEGRIDAD_NO_COMPROBADA")
    if integrity.get("hashes_despues") != current_baseline: errors.append("EXPEDIENTE_BASELINE_ACTUAL_DIFIERE")
    for name, contract in dossier.get("contratos", {}).items():
        path = repo_root / contract.get("ruta", "")
        if not path.is_file() or sha256(path) != contract.get("sha256"): errors.append(f"EXPEDIENTE_CONTRATO_INVALIDO:{name}")
    proposals = read_tsv(dossier_dir / "propuestas-recibidas.tsv")
    decisions = read_tsv(dossier_dir / "integracion-propuestas.tsv")
    reports = read_tsv(dossier_dir / "reportes-recibidos.tsv")
    tasks_payload = json.loads((dossier_dir / "tareas-inspeccion-recibidas.json").read_text(encoding="utf-8"))
    curator_task = json.loads((dossier_dir / "tarea-curador-recibida.json").read_text(encoding="utf-8"))
    linked_provenance = read_tsv(dossier_dir / "procedencias-vinculadas.tsv")
    semantic_manifest_path = registry / "ejecucion-semantica" / "manifest.json"
    has_semantic_link = bool(dossier.get("expediente_semantico_ref"))
    if has_semantic_link and not semantic_manifest_path.is_file():
        errors.append("EXPEDIENTE_SEMANTICO_MANIFEST_INEXISTENTE")
    elif has_semantic_link:
        semantic_manifest = json.loads(semantic_manifest_path.read_text(encoding="utf-8"))
        semantic_run_id = semantic_manifest.get("run_id", "")
        if dossier.get("semantic_run_id") != semantic_run_id or curator_task.get("run_id") != semantic_run_id:
            errors.append("EXPEDIENTE_SEMANTICO_RUN_NO_VIGENTE")
        semantic_ref = dossier.get("expediente_semantico_ref", "")
        semantic_path = repo_root / semantic_ref
        if (
            not semantic_ref
            or not semantic_path.is_file()
            or dossier.get("expediente_semantico_sha256") != sha256(semantic_path)
            or curator_task.get("expediente_semantico_ref") != semantic_ref
            or curator_task.get("expediente_semantico_sha256") != sha256(semantic_path)
        ):
            errors.append("EXPEDIENTE_SEMANTICO_VINCULO_INVALIDO")
        semantic_rows = read_tsv(semantic_path) if semantic_path.is_file() else []
        baseline_candidates = {
            row.get("relacion_id", "") for row in read_tsv(registry / "relaciones.tsv")
            if row.get("clasificacion_relacion") == "CANDIDATA"
        }
        semantic_relation_ids = [row.get("relacion_id", "") for row in semantic_rows]
        if (
            len(semantic_rows) != len(baseline_candidates)
            or set(semantic_relation_ids) != baseline_candidates
            or len(semantic_relation_ids) != len(set(semantic_relation_ids))
            or any(row.get("expediente_integrable") != "NO" for row in semantic_rows)
        ):
            errors.append("EXPEDIENTE_SEMANTICO_CERO_INTEGRABLES_NO_DEMOSTRADO_1A1")
    if len(proposals) != len(decisions): errors.append("EXPEDIENTE_PROPUESTAS_DECISIONES_NO_1A1")
    if [row.get("propuesta_id") for row in proposals] != [row.get("propuesta_id") for row in decisions]: errors.append("EXPEDIENTE_JOIN_PROPUESTAS_DECISIONES_INVALIDO")
    material = {"propuesta_id", "relacion_id", "reporte_inspeccion_ref", "tarea_observacion_id", "activo_id", "objeto_logico_id", "procedencia_ref", "accion", "adjudicacion_propuesta", "reserva"}
    for proposal, decision in zip(proposals, decisions):
        if material - set(decision) or any(decision.get(field) != proposal.get(field) for field in material):
            errors.append(f"EXPEDIENTE_CAMPOS_MATERIALES_PERDIDOS:{proposal.get('propuesta_id', '')}")
    schema_dir = repo_root / "tools" / "curador_registro" / "schemas"
    for proposal in proposals:
        if schema_errors(proposal, schema_dir / PROPOSAL_SCHEMA):
            errors.append(f"EXPEDIENTE_PROPUESTA_SCHEMA_INVALIDO:{proposal.get('propuesta_id', '')}")
    for report in reports:
        if schema_errors(report, schema_dir / REPORT_SCHEMA):
            errors.append(f"EXPEDIENTE_REPORTE_SCHEMA_INVALIDO:{report.get('reporte_id', '')}")
    if not isinstance(tasks_payload, list):
        errors.append("EXPEDIENTE_TAREAS_FORMATO_INVALIDO")
        tasks_payload = []
    for task in tasks_payload:
        if not isinstance(task, dict) or schema_errors(task, schema_dir / TASK_SCHEMA):
            errors.append(f"EXPEDIENTE_TAREA_SCHEMA_INVALIDO:{task.get('tarea_observacion_id', '') if isinstance(task, dict) else ''}")
    if not isinstance(curator_task, dict) or schema_errors(curator_task, schema_dir / CURATOR_TASK_SCHEMA):
        errors.append("EXPEDIENTE_TAREA_CURADOR_SCHEMA_INVALIDO")

    proposal_ids = Counter(row.get("propuesta_id", "") for row in proposals)
    proposal_relations = Counter(row.get("relacion_id", "") for row in proposals)
    if any(not value or count != 1 for value, count in proposal_ids.items()): errors.append("EXPEDIENTE_PROPUESTAS_NO_UNICAS")
    if any(not value or count != 1 for value, count in proposal_relations.items()): errors.append("EXPEDIENTE_RELACIONES_PROPUESTAS_NO_UNICAS")
    reports_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    for report in reports:
        reports_by_id[report.get("reporte_id", "")].append(report)
    tasks_by_id = {
        task.get("tarea_observacion_id", ""): task for task in tasks_payload if isinstance(task, dict)
    }
    if len(tasks_by_id) != len(tasks_payload) or "" in tasks_by_id: errors.append("EXPEDIENTE_TAREAS_NO_UNICAS")
    assignments = {
        (row.get("relacion_id", ""), row.get("reporte_inspeccion_ref", ""), row.get("activo_id", ""))
        for row in curator_task.get("asignaciones", [])
    } if isinstance(curator_task, dict) else set()
    relations = {row.get("relacion_id", ""): row for row in read_tsv(registry / "relaciones.tsv")}
    bootstrap = {row.get("relacion_id", ""): row for row in read_tsv(registry / "bootstrap-semantico.tsv")}
    assets = {row.get("activo_id", "") for row in read_tsv(universe / "universo-declarado-t0.tsv")}
    provenance = {row.get("procedencia_id", ""): row for row in linked_provenance}
    baseline_provenance = {
        row.get("procedencia_id", ""): row for row in read_tsv(registry / "evidencias.tsv")
    }
    exceptions = {row.get("excepcion_cegamiento_id", ""): row for row in read_tsv(universe / "excepciones-cegamiento.tsv")}
    for proposal in proposals:
        pid = proposal.get("propuesta_id", "")
        rid = proposal.get("relacion_id", "")
        report_id = proposal.get("reporte_inspeccion_ref", "")
        task_id = proposal.get("tarea_observacion_id", "")
        asset_id = proposal.get("activo_id", "")
        object_id = proposal.get("objeto_logico_id", "")
        if proposal.get("snapshot_t0_sha256") != snapshot.get("snapshot_t0_sha256"):
            errors.append(f"EXPEDIENTE_PROPUESTA_SNAPSHOT_OBSOLETO:{pid}")
        if proposal.get("baseline_sha256") != current_baseline.get("baseline.json"):
            errors.append(f"EXPEDIENTE_PROPUESTA_BASELINE_OBSOLETO:{pid}")
        if rid not in relations: errors.append(f"EXPEDIENTE_RELACION_INEXISTENTE:{pid}")
        if asset_id not in assets: errors.append(f"EXPEDIENTE_ACTIVO_INEXISTENTE:{pid}")
        if bootstrap.get(rid, {}).get("activo_id_vinculado") != asset_id:
            errors.append(f"EXPEDIENTE_RELACION_ACTIVO_NO_ASIGNADO:{pid}")
        if (rid, report_id, asset_id) not in assignments:
            errors.append(f"EXPEDIENTE_PROPUESTA_NO_ASIGNADA:{pid}")
        report_rows = reports_by_id.get(report_id, [])
        report_meta = {
            (row.get("tarea_observacion_id", ""), row.get("activo_id", ""), row.get("objeto_logico_id", ""))
            for row in report_rows
        }
        expected_meta = (task_id, asset_id, object_id)
        if not report_rows or report_meta != {expected_meta}:
            errors.append(f"EXPEDIENTE_JOIN_PROPUESTA_REPORTE_INVALIDO:{pid}")
        task = tasks_by_id.get(task_id)
        if task is None or (task.get("tarea_observacion_id"), task.get("activo_id"), task.get("objeto_logico_id")) != expected_meta:
            errors.append(f"EXPEDIENTE_JOIN_REPORTE_TAREA_INVALIDO:{pid}")
        elif task.get("snapshot_t0_sha256") != snapshot.get("snapshot_t0_sha256"):
            errors.append(f"EXPEDIENTE_TAREA_SNAPSHOT_OBSOLETO:{pid}")
        prov = provenance.get(proposal.get("procedencia_ref", ""))
        if prov is None or prov.get("relacion_id") != rid or prov != baseline_provenance.get(proposal.get("procedencia_ref", "")):
            errors.append(f"EXPEDIENTE_PROCEDENCIA_INVALIDA:{pid}")
        if proposal.get("cegamiento_roto") == "SI":
            exception = exceptions.get(proposal.get("excepcion_cegamiento_ref", ""))
            if exception is None or exception.get("tarea_observacion_id") != task_id:
                errors.append(f"EXPEDIENTE_EXCEPCION_CEGAMIENTO_INVALIDA:{pid}")
        decision = next((row for row in decisions if row.get("propuesta_id") == pid), {})
        if decision.get("estado_validacion") == "ACEPTADA":
            if proposal.get("afirmacion_origen_tipo") == "INFERENCIA_PROPUESTA" and proposal.get("tratar_como_hecho") == "SI":
                errors.append(f"EXPEDIENTE_INFERENCIA_ACEPTADA_COMO_HECHO:{pid}")
            current = relations.get(rid, {}).get("clasificacion_relacion", "")
            if proposal.get("accion") == "CONSERVAR_ADJUDICACION" and proposal.get("adjudicacion_propuesta") != current:
                errors.append(f"EXPEDIENTE_CONSERVACION_DIFIERE_BASELINE:{pid}")
    if result.get("expediente_integracion_sha256") != sha256(dossier_path): errors.append("EXPEDIENTE_MANIFEST_NO_VINCULADO")
    if result.get("expediente_completo") is not True or result.get("errores_expediente"):
        errors.append("EXPEDIENTE_INTEGRACION_INCOMPLETO")
    if result.get("ok") is not True: errors.append("EXPEDIENTE_RESULTADO_NO_OK")
    if result.get("propuestas") != len(proposals) or result.get("rechazadas") != sum(row.get("estado_validacion") == "RECHAZADA" for row in decisions):
        errors.append("EXPEDIENTE_CONTEOS_NO_RECONCILIADOS")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--proposals", type=Path, required=True)
    parser.add_argument("--reports", type=Path, action="append", default=[])
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    result = integrate(args.baseline.resolve(), args.snapshot.resolve(), args.proposals.resolve(), [path.resolve() for path in args.reports], args.output_dir.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
