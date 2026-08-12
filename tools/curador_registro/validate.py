#!/usr/bin/env python3
"""Valida capas y denominadores del barrido sin adjudicar semántica."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .baseline import validar_baseline
    from .integrate import validate_integration_dossier
    from .integrate_production import verify_production_bundle
except ImportError:
    from baseline import validar_baseline
    from integrate import validate_integration_dossier
    from integrate_production import verify_production_bundle


FORBIDDEN_LEVEL1 = {
    "necesidad_id", "relacion_id", "adjudicacion_vigente", "constructo_esperado",
    "objeto_modelo_origen", "decision_humana_pendiente", "hipotesis",
    "interpretacion_deseada", "resultado_favorable", "signo_esperado",
    "clasificacion_deseada", "supervisor_link",
}
ALLOWED_ASSERTIONS = {
    "HECHO_OBSERVADO", "NO_OBSERVADO_EN_UNIVERSO_INSPECCIONADO",
    "NO_DETERMINADO", "NO_INSPECCIONADO", "NO_ACCESIBLE",
    "CALCULO_REPRODUCIBLE", "INFERENCIA_PROPUESTA",
}
MATERIAL_EXCEPTION_CAUSES = {
    "RESTRICCION_LEGAL_O_ACCESO", "CORRUPCION", "CIFRADO",
    "FORMATO_NO_SOPORTADO", "COSTO_COMPUTACIONAL_EXTRAORDINARIO",
    "RIESGO_PRIVACIDAD_ETICA", "DEPENDENCIA_EXTERNA_INACCESIBLE",
}
SEMANTIC_TERMINALS = {
    "EJECUTADA_CON_RESULTADO", "NO_ALCANZO_TRAS_INTENTOS",
    "FUENTE_ABIERTA_SIN_OBJETO_REQUERIDO", "BLOQUEADA_INPUT_FALTANTE",
    "REQUIERE_DECISION_HUMANA", "NO_CORRIDA",
}
DIRECT_SEMANTIC_CONTENT = (
    "application/pdf", "application/zip", "application/x-zip",
    "application/vnd.openxmlformats", "text/csv", "application/csv",
    "application/octet-stream",
)
# ADR-70(b): documentacion_fuente es obligatorio para specs nuevas; las ya
# selladas al momento del ADR no se editan retroactivamente. Lista cerrada,
# no heurística de fecha.
ESPECIFICACIONES_SELLADAS_SIN_DOCUMENTACION_FUENTE = {
    "ESP-OPACA-A-7baf278d", "ESP-OPACA-B-d13ec4fe", "ESP-OPACA-C-9ecb5c61",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def unique_nonempty(rows: list[dict[str, str]], field: str) -> set[str]:
    return {row.get(field, "") for row in rows if row.get(field, "")}


def documentacion_fuente_errors(production_config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for spec in production_config.get("specifications", []):
        spec_id = spec.get("especificacion_id", "")
        if spec_id in ESPECIFICACIONES_SELLADAS_SIN_DOCUMENTACION_FUENTE:
            continue
        if not spec.get("documentacion_fuente"):
            errors.append(f"ESPECIFICACION_SIN_DOCUMENTACION_FUENTE:{spec_id}")
    return errors


def corpus_inventory(corpus_root: Path) -> tuple[list[tuple[str, str]], Counter[str]]:
    """Enumera bytes del corpus; no usa conteos ni hashes declarados por T0."""
    representations = [
        (path.relative_to(corpus_root).as_posix(), sha256(path))
        for path in sorted(corpus_root.rglob("*"))
        if path.is_file()
    ]
    return representations, Counter(digest for _, digest in representations)


def validate_level1_input(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if forbidden := sorted(FORBIDDEN_LEVEL1.intersection(payload)):
        errors.append("campos_semanticos_prohibidos:" + ",".join(forbidden))
    required = {"tarea_observacion_id", "run_id", "snapshot_t0_sha256", "activo_id", "objeto_logico_id", "criterio_parada"}
    if missing := sorted(required - set(payload)):
        errors.append("campos_operativos_faltantes:" + ",".join(missing))
    return errors


def material_exception(cause: str) -> bool:
    return cause in MATERIAL_EXCEPTION_CAUSES


def inspectable_coverage(states: list[dict[str, str]], reports: list[dict[str, str]], exceptions: list[dict[str, str]]) -> tuple[int, int, set[str]]:
    acquired_objects = {
        row["objeto_logico_id"] for row in states
        if row.get("adquirido") == "SI" and row.get("inspeccionable") == "SI"
    }
    reported_objects = unique_nonempty(reports, "objeto_logico_id")
    excepted_objects = {
        row["objeto_logico_id"] for row in exceptions
        if row.get("estado") in {"VIGENTE", "ACEPTADA"} and material_exception(row.get("causa", ""))
    }
    missing = acquired_objects - reported_objects - excepted_objects
    return len(acquired_objects - excepted_objects), len((acquired_objects - excepted_objects) & reported_objects), missing


def _repo_ref(repo_root: Path, value: str) -> Path | None:
    path = Path(value)
    candidate = path if path.is_absolute() else repo_root / path
    try:
        resolved = candidate.resolve()
        resolved.relative_to(repo_root.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def _independent_semantic_state(
    work_type: str,
    report: dict[str, Any],
    action: str,
    evidence: dict[str, str],
) -> str:
    """Recalcula el terminal sin usar código ni booleanos del productor."""
    attempts = report.get("intentos", [])
    openings = report.get("objetos_abiertos", [])
    local_assets = [
        row for row in openings
        if str(row.get("resultado", "")).startswith("ABIERTO_")
        and not str(row.get("resultado", "")).endswith("REFERENCIA_MAIN")
    ]
    successes = [
        row for row in attempts
        if str(row.get("resultado_http_archivo_error", "")).startswith("HTTP_2")
    ]
    direct = any(
        row.get("objeto_completo") == "SI"
        and any(str(row.get("content_type", "")).startswith(prefix) for prefix in DIRECT_SEMANTIC_CONTENT)
        for row in successes
    )
    if work_type == "ANALISIS_MEDICION":
        return "BLOQUEADA_INPUT_FALTANTE"
    if any(term in action.casefold() for term in ("autorización", "autorizacion", "solicitar acceso", "licencia aplicable")) and not direct and not local_assets:
        return "REQUIERE_DECISION_HUMANA"
    if attempts and not successes:
        return "NO_ALCANZO_TRAS_INTENTOS"
    if direct or local_assets:
        return "EJECUTADA_CON_RESULTADO"
    if successes or any(row.get("resultado") == "ABIERTO_REFERENCIA_MAIN" for row in openings):
        return "FUENTE_ABIERTA_SIN_OBJETO_REQUERIDO"
    material = ("variable_reactivo_tabla", "unidad_observacion", "periodo", "universo_muestra", "codificacion")
    if any(evidence.get(field, "") in {"", "NO_DETERMINADO", "NO_APLICA", "—"} for field in material):
        return "BLOQUEADA_INPUT_FALTANTE"
    return "NO_CORRIDA"


def validate_semantic_execution(
    repo_root: Path,
    registry_dir: Path,
    snapshot_hash: str,
    baseline_hash: str,
    candidate_ids: set[str],
    work_rows: list[dict[str, str]],
) -> tuple[list[str], dict[str, int], Counter[str]]:
    """Relee el run completo y recalcula hashes, joins, estados y cobertura."""
    errors: list[str] = []
    execution_root = registry_dir / "ejecucion-semantica"
    manifest_path = execution_root / "manifest.json"
    if not manifest_path.is_file():
        return ["EJECUCION_SEMANTICA_SIN_MANIFEST"], {"numerador": 0, "denominador": len(candidate_ids)}, Counter()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    run_id = str(manifest.get("run_id", ""))
    run_dir = execution_root / "runs" / run_id
    if not run_id or not run_dir.is_dir():
        return ["EJECUCION_SEMANTICA_RUN_INEXISTENTE"], {"numerador": 0, "denominador": len(candidate_ids)}, Counter()
    if manifest.get("snapshot_t0_sha256") != snapshot_hash:
        errors.append("EJECUCION_SEMANTICA_SNAPSHOT_OBSOLETO")
    if manifest.get("baseline_sha256") != baseline_hash:
        errors.append("EJECUCION_SEMANTICA_BASELINE_OBSOLETO")
    if manifest.get("network_habilitada") is not True:
        errors.append("EJECUCION_SEMANTICA_BUSQUEDA_SIN_RED_REAL")

    observed_artifacts = {
        str(path.relative_to(repo_root)): sha256(path)
        for path in sorted(run_dir.rglob("*")) if path.is_file()
    }
    if manifest.get("artefactos_run_sha256") != observed_artifacts:
        errors.append("EJECUCION_SEMANTICA_MAPA_HASHES_INCOMPLETO_O_INVALIDO")

    schemas: dict[str, dict[str, Any]] = {}
    for name in (
        "inspector-contract.schema.json", "neutral-report.schema.json",
        "curator-input.schema.json", "semantic-run-proposal.schema.json",
        "semantic-supervision.schema.json",
    ):
        path = execution_root / "schemas" / name
        if not path.is_file():
            errors.append(f"EJECUCION_SEMANTICA_SCHEMA_INEXISTENTE:{name}")
        else:
            schemas[name] = json.loads(path.read_text(encoding="utf-8"))

    work = {row.get("relacion_id", ""): row for row in work_rows}
    evidence = {row.get("relacion_id", ""): row for row in read_tsv(registry_dir / "evidencias.tsv") if row.get("relacion_id") in candidate_ids}
    utilities = {row.get("relacion_id", ""): row for row in read_tsv(registry_dir / "utilidad-modelo.tsv") if row.get("relacion_id") in candidate_ids}
    results = read_tsv(run_dir / "resultados-acciones.tsv")
    proposals = read_tsv(run_dir / "propuestas-curador.tsv")
    supervision = read_tsv(run_dir / "supervision.tsv")
    integration = read_tsv(run_dir / "expediente-integracion.tsv")
    private_map = read_tsv(run_dir / "mapa-privado-supervisor.tsv")
    partitions = read_tsv(run_dir / "particiones.tsv")
    tables = {
        "RESULTADOS": results,
        "PROPUESTAS": proposals,
        "SUPERVISION": supervision,
        "EXPEDIENTE_INTEGRACION": integration,
        "MAPA_PRIVADO": private_map,
    }
    for label, rows in tables.items():
        ids = [row.get("relacion_id", "") for row in rows]
        if len(rows) != len(candidate_ids) or set(ids) != candidate_ids or len(ids) != len(set(ids)):
            errors.append(f"EJECUCION_SEMANTICA_{label}_NO_1A1")
    partitioned: list[str] = []
    for row in partitions:
        declared = [value for value in row.get("relaciones", "").split(";") if value]
        partitioned.extend(declared)
        if int(row.get("numero_relaciones", "-1")) != len(declared):
            errors.append(f"EJECUCION_SEMANTICA_PARTICION_CONTEO_INVALIDO:{row.get('particion_id', '')}")
    if set(partitioned) != candidate_ids or len(partitioned) != len(set(partitioned)):
        errors.append("EJECUCION_SEMANTICA_PARTICIONES_NO_DISJUNTAS_1A1")

    result_by_relation = {row.get("relacion_id", ""): row for row in results}
    proposal_by_relation = {row.get("relacion_id", ""): row for row in proposals}
    supervision_by_relation = {row.get("relacion_id", ""): row for row in supervision}
    integration_by_relation = {row.get("relacion_id", ""): row for row in integration}
    private_by_relation = {row.get("relacion_id", ""): row for row in private_map}
    independently_derived_states: Counter[str] = Counter()
    executed = 0
    forbidden_level1 = {"relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen"}

    for rid in sorted(candidate_ids):
        result = result_by_relation.get(rid, {})
        proposal = proposal_by_relation.get(rid, {})
        supervisor = supervision_by_relation.get(rid, {})
        integration_row = integration_by_relation.get(rid, {})
        private = private_by_relation.get(rid, {})
        task_id = result.get("tarea_observacion_id", "")
        input_path = _repo_ref(repo_root, private.get("input_inspector_ref", ""))
        report_path = _repo_ref(repo_root, result.get("reporte_neutral_ref", ""))
        curator_path = _repo_ref(repo_root, private.get("input_curador_ref", ""))
        contract_path = run_dir / "contratos-inspector" / f"{task_id}.json"
        if not all(path is not None and path.is_file() for path in (input_path, report_path, curator_path)) or not contract_path.is_file():
            errors.append(f"EJECUCION_SEMANTICA_EXPEDIENTE_INCOMPLETO:{rid}")
            continue
        assert input_path is not None and report_path is not None and curator_path is not None
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        inspector_input = json.loads(input_path.read_text(encoding="utf-8"))
        report = json.loads(report_path.read_text(encoding="utf-8"))
        curator_input = json.loads(curator_path.read_text(encoding="utf-8"))
        for name, payload in (
            ("inspector-contract.schema.json", contract),
            ("inspector-contract.schema.json", inspector_input),
            ("neutral-report.schema.json", report),
            ("curator-input.schema.json", curator_input),
        ):
            if name in schemas and list(Draft202012Validator(schemas[name]).iter_errors(payload)):
                errors.append(f"EJECUCION_SEMANTICA_SCHEMA_INVALIDO:{rid}:{name}")
        if forbidden_level1.intersection(inspector_input) or forbidden_level1.intersection(report):
            errors.append(f"EJECUCION_SEMANTICA_NIVEL1_NO_CEGADO:{rid}")
        if inspector_input.get("contrato_sha256") != sha256(contract_path):
            errors.append(f"EJECUCION_SEMANTICA_CONTRATO_HASH_INVALIDO:{rid}")
        if report.get("input_sha256") != sha256(input_path) or proposal.get("input_inspector_sha256") != sha256(input_path):
            errors.append(f"EJECUCION_SEMANTICA_INPUT_HASH_INVALIDO:{rid}")
        if curator_input.get("reporte_neutral_sha256") != sha256(report_path) or proposal.get("reporte_neutral_sha256") != sha256(report_path):
            errors.append(f"EJECUCION_SEMANTICA_REPORTE_HASH_INVALIDO:{rid}")
        if proposal.get("input_curador_sha256") != sha256(curator_path):
            errors.append(f"EJECUCION_SEMANTICA_CURADOR_HASH_INVALIDO:{rid}")
        if any(payload.get("run_id") != run_id for payload in (contract, inspector_input, report, curator_input)):
            errors.append(f"EJECUCION_SEMANTICA_RUN_JOIN_INVALIDO:{rid}")
        if any(payload.get("tarea_observacion_id") != task_id for payload in (contract, inspector_input, report)):
            errors.append(f"EJECUCION_SEMANTICA_TAREA_JOIN_INVALIDO:{rid}")
        if curator_input.get("relacion_id") != rid or proposal.get("tarea_observacion_id") != task_id:
            errors.append(f"EJECUCION_SEMANTICA_CURADOR_JOIN_INVALIDO:{rid}")

        original_action = evidence.get(rid, {}).get("siguiente_accion", "")
        original_criterion = work.get(rid, {}).get("criterio_cierre", "")
        original_input = utilities.get(rid, {}).get("verificacion_requerida", "")
        original_reserve = utilities.get(rid, {}).get("reserva", "")
        if not original_action or any(value != original_action for value in (
            work.get(rid, {}).get("siguiente_accion_original", ""),
            result.get("siguiente_accion_original", ""), proposal.get("accion_original", ""),
            curator_input.get("siguiente_accion_original", ""),
        )):
            errors.append(f"EJECUCION_SEMANTICA_ACCION_ORIGINAL_NO_PRESERVADA:{rid}")
        if any(value != original_criterion for value in (
            result.get("criterio_cierre_individual", ""),
            proposal.get("criterio_cierre_individual", ""),
            curator_input.get("criterio_cierre_individual", ""),
        )):
            errors.append(f"EJECUCION_SEMANTICA_CRITERIO_INDIVIDUAL_NO_PRESERVADO:{rid}")
        if proposal.get("input_requerido_original") != original_input or proposal.get("reserva_original") != original_reserve:
            errors.append(f"EJECUCION_SEMANTICA_CONTEXTO_ORIGINAL_NO_PRESERVADO:{rid}")

        attempts = report.get("intentos", [])
        if len(attempts) > 2 or int(result.get("intentos_reales", "-1")) != len(attempts):
            errors.append(f"EJECUCION_SEMANTICA_INTENTOS_INVALIDOS:{rid}")
        for index, attempt in enumerate(attempts, start=1):
            required_attempt = {
                "orden", "localizador", "resultado_http_archivo_error", "url_final",
                "content_type", "bytes_observados", "objeto_completo",
                "sha256_objeto", "sha256_fragmento", "resultado_literal",
            }
            if required_attempt - set(attempt) or attempt.get("orden") != index or not attempt.get("localizador"):
                errors.append(f"EJECUCION_SEMANTICA_INTENTO_NO_AUDITABLE:{rid}:{index}")
            if attempt.get("resultado_http_archivo_error") == "NO_CORRIDA_RED_DESHABILITADA":
                errors.append(f"EJECUCION_SEMANTICA_INTENTO_NO_REAL:{rid}:{index}")
            if attempt.get("objeto_completo") == "SI" and attempt.get("sha256_objeto") in {"", "NO_DETERMINADO"}:
                errors.append(f"EJECUCION_SEMANTICA_OBJETO_REMOTO_SIN_HASH:{rid}:{index}")
            if attempt.get("objeto_completo") == "NO" and int(attempt.get("bytes_observados", 0)) > 0 and attempt.get("sha256_fragmento") in {"", "NO_DETERMINADO"}:
                errors.append(f"EJECUCION_SEMANTICA_FRAGMENTO_REMOTO_SIN_HASH:{rid}:{index}")
        for opened in report.get("objetos_abiertos", []):
            path_value = opened.get("ruta", "")
            path = Path(path_value)
            path = path if path.is_absolute() else repo_root / path
            if path.is_file() and opened.get("sha256") != sha256(path):
                errors.append(f"EJECUCION_SEMANTICA_OBJETO_LOCAL_HASH_INVALIDO:{rid}:{path_value}")

        derived_state = _independent_semantic_state(work.get(rid, {}).get("tipo_trabajo", ""), report, original_action, evidence.get(rid, {}))
        independently_derived_states[derived_state] += 1
        if derived_state != "NO_CORRIDA":
            executed += 1
        if derived_state not in SEMANTIC_TERMINALS or any(value != derived_state for value in (
            report.get("resultado_operativo", ""), result.get("estado_cierre", ""),
            proposal.get("estado_cierre", ""), supervisor.get("estado_recalculado", ""),
        )):
            errors.append(f"EJECUCION_SEMANTICA_ESTADO_NO_RECALCULIA:{rid}")
        if any(supervisor.get(field) != "SI" for field in ("accion_preservada", "joins_validos", "hashes_validos", "cegamiento_validado")):
            errors.append(f"EJECUCION_SEMANTICA_SUPERVISION_RECHAZADA:{rid}")
        if proposal.get("expediente_integrable") != "NO" or proposal.get("modifica_baseline") != "NO":
            errors.append(f"EJECUCION_SEMANTICA_PROPUESTA_INTEGRABLE_NO_DEMOSTRADA:{rid}")
        if integration_row.get("expediente_integrable") != "NO" or integration_row.get("modifica_baseline") != "NO":
            errors.append(f"EJECUCION_SEMANTICA_DESTINO_INTEGRACION_INVALIDO:{rid}")

    if "semantic-run-proposal.schema.json" in schemas:
        validator = Draft202012Validator(schemas["semantic-run-proposal.schema.json"])
        for row in proposals:
            if list(validator.iter_errors(row)):
                errors.append(f"EJECUCION_SEMANTICA_PROPUESTA_SCHEMA_INVALIDO:{row.get('relacion_id', '')}")
    if "semantic-supervision.schema.json" in schemas:
        validator = Draft202012Validator(schemas["semantic-supervision.schema.json"])
        for row in supervision:
            if list(validator.iter_errors(row)):
                errors.append(f"EJECUCION_SEMANTICA_SUPERVISION_SCHEMA_INVALIDO:{row.get('relacion_id', '')}")
    coverage = {"numerador": executed, "denominador": len(candidate_ids)}
    return errors, coverage, independently_derived_states


def validate(repo_root: Path, output_root: Path | None = None) -> dict[str, Any]:
    data = repo_root / "data"
    universe_dir = data / "curacion-universo"
    registry_dir = data / "curacion-registro"
    errors: list[str] = []
    reserves: list[str] = []

    snapshot_path = universe_dir / "snapshot-t0.json"
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    for name, expected in snapshot.get("hashes_outputs", {}).items():
        path = universe_dir / name
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"T0_HASH_INVALIDO:{name}")

    sources = read_tsv(universe_dir / "fuentes-t0.tsv")
    declarations = read_tsv(universe_dir / "declaraciones-activos-t0.tsv")
    assets = read_tsv(universe_dir / "universo-declarado-t0.tsv")
    families = read_tsv(universe_dir / "familias-activos.tsv")
    candidates = read_tsv(universe_dir / "candidatos-reconciliacion-activos.tsv")
    states = read_tsv(universe_dir / "estado-activos.tsv")
    plans = read_tsv(universe_dir / "plan-inspeccion.tsv")
    reports = read_tsv(universe_dir / "reportes-inspeccion.tsv")
    inspection_exceptions = read_tsv(universe_dir / "excepciones-inspeccion.tsv")
    blinding_exceptions = read_tsv(universe_dir / "excepciones-cegamiento.tsv")
    new_objects = read_tsv(universe_dir / "objetos-observados-no-representados.tsv")

    source_ids = [row.get("input_id", "") for row in sources]
    declaration_ids = [row.get("declaracion_id", "") for row in declarations]
    asset_ids = [row.get("activo_id", "") for row in assets]
    if len(source_ids) != len(set(source_ids)) or "" in source_ids:
        errors.append("INPUT_IDS_NO_UNICOS")
    if len(declaration_ids) != len(set(declaration_ids)) or "" in declaration_ids:
        errors.append("DECLARACION_IDS_NO_UNICOS")
    if len(asset_ids) != len(set(asset_ids)) or "" in asset_ids:
        errors.append("ACTIVO_IDS_NO_UNICOS")
    corpus_root = Path(snapshot.get("corpus_root", ""))
    representations, content_hash_counts = corpus_inventory(corpus_root)
    observed_representation_count = len(representations)
    observed_unique_content_count = len(content_hash_counts)
    observed_duplicate_count = sum(count - 1 for count in content_hash_counts.values())
    snapshot_counts = snapshot.get("conteos", {})
    independently_observed = {
        "representaciones_locales": observed_representation_count,
        "contenidos_locales_sha256_unicos": observed_unique_content_count,
        "identidades_locales_verificadas": observed_unique_content_count,
        "duplicados_locales_reales": observed_duplicate_count,
        "hashes_representaciones_locales_verificados": observed_representation_count,
    }
    for field, observed in independently_observed.items():
        if snapshot_counts.get(field) != observed:
            errors.append(f"T0_CONTEO_CORPUS_INVALIDO:{field}")
    if snapshot_counts.get("denominador_activos_declarados") != "NO_DETERMINADO":
        errors.append("T0_DENOMINADOR_DECLARADO_PRESENTADO_COMO_PUNTUAL")
    if snapshot_counts.get("cobertura_adquisicion_puntual") != "NO_DETERMINADO":
        errors.append("T0_COBERTURA_ADQUISICION_PRESENTADA_COMO_PUNTUAL")
    if snapshot_counts.get("componentes_declarados_conservadores") != len(assets):
        errors.append("T0_COMPONENTES_CONSERVADORES_NO_RECONCILIAN")
    if snapshot_counts.get("cota_superior_activos_declarados") != len(assets):
        errors.append("T0_COTA_SUPERIOR_NO_RECONCILIA")
    acquired_rows = [row for row in assets if row.get("estado_adquisicion") == "ADQUIRIDO"]
    verified_local_hashes = 0
    for asset in acquired_rows:
        local_path = corpus_root / asset.get("ruta_local", "")
        if not local_path.is_file() or asset.get("hash_local") != sha256(local_path):
            errors.append(f"HASH_LOCAL_NO_COINCIDE_RUTA:{asset.get('activo_id', '')}")
        else:
            verified_local_hashes += 1
    if snapshot_counts.get("identidades_locales_verificadas") != verified_local_hashes:
        errors.append("CONTEO_HASHES_LOCALES_VERIFICADOS_INVALIDO")

    ledger = read_tsv(universe_dir / "ledger-inspecciones-t0.tsv")
    ledger_keys = {(row.get("ruta_local", ""), row.get("sha256", "")) for row in ledger}
    if len(ledger) != observed_unique_content_count or len(ledger_keys) != len(ledger):
        errors.append("LEDGER_INSPECCIONES_NO_CUBRE_CONTENIDOS_1A1")
    if {row.get("sha256", "") for row in ledger} != set(content_hash_counts):
        errors.append("LEDGER_INSPECCIONES_HASHES_NO_RECONCILIAN_CORPUS")
    allowed_ledger_conditions = {
        "REUTILIZADA_PRE_T0_CORREGIDO",
        "INSPECCIONADA_POR_PRIMERA_VEZ_EN_CORRECCION",
    }
    if {row.get("condicion", "") for row in ledger} - allowed_ledger_conditions:
        errors.append("LEDGER_INSPECCIONES_CONDICION_INVALIDA")
    for row in ledger:
        local_path = corpus_root / row.get("ruta_local", "")
        if not local_path.is_file() or sha256(local_path) != row.get("sha256"):
            errors.append(f"LEDGER_RUTA_HASH_INVALIDO:{row.get('ledger_id', '')}")
        if row.get("join_auditable") != "RUTA_LOCAL+SHA256+ACTIVO+TAREA+CONTRATO+REPORTE":
            errors.append(f"LEDGER_JOIN_NO_AUDITABLE:{row.get('ledger_id', '')}")
    ledger_summary_path = universe_dir / "ledger-inspecciones-t0-resumen.json"
    if not ledger_summary_path.is_file():
        errors.append("LEDGER_RESUMEN_INEXISTENTE")
    else:
        ledger_summary = json.loads(ledger_summary_path.read_text(encoding="utf-8"))
        derived_conditions = dict(Counter(row.get("condicion", "") for row in ledger))
        if ledger_summary.get("condiciones") != derived_conditions:
            errors.append("LEDGER_RESUMEN_NO_DERIVADO")
        if ledger_summary.get("ledger_sha256") != sha256(universe_dir / "ledger-inspecciones-t0.tsv"):
            errors.append("LEDGER_RESUMEN_HASH_INVALIDO")
    if unique_nonempty(declarations, "activo_id") - set(asset_ids):
        errors.append("DECLARACION_APUNTA_ACTIVO_INEXISTENTE")
    if sum(int(row["declaraciones_parseadas"]) for row in sources) != len(declarations):
        errors.append("INPUTS_NO_RECONCILIAN_DECLARACIONES")
    for row in sources:
        if int(row["declaraciones_encontradas"]) != int(row["declaraciones_parseadas"]) and row.get("errores") == "NINGUNO" and row.get("reserva") == "NINGUNA":
            errors.append(f"INPUT_SIN_ERROR_CONCRETO:{row['input_id']}")
    if set(asset_ids) != unique_nonempty(states, "activo_id") or len(states) != len(assets):
        errors.append("COBERTURA_ESTADO_ACTIVOS_INCOMPLETA")
    if len(families) != len(assets) or unique_nonempty(families, "activo_id") != set(asset_ids):
        errors.append("FAMILIAS_NO_PROYECTAN_ACTIVOS_1A1")
    for family in families:
        if family.get("tipo_relacion") == "DUPLICADO_VERIFICADO" and not (
            family.get("evidencia_estructural", "").startswith("sha256:")
            or "IDENTIFICADOR_OFICIAL" in family.get("evidencia_estructural", "")
        ):
            errors.append(f"DUPLICADO_SIN_EVIDENCIA_FUERTE:{family['activo_id']}")
        if family.get("tipo_relacion") == "VARIANTE_DE_ENTREGA" and family.get("evidencia_estructural") in {"", "NO_DETERMINADO"}:
            errors.append(f"VARIANTE_SIN_EVIDENCIA_ESTRUCTURAL:{family['activo_id']}")
    for candidate in candidates:
        if candidate.get("estado_revision") == "IDENTIDAD_VERIFICADA":
            errors.append(f"FUZZY_PROMOVIDO_A_IDENTIDAD:{candidate.get('candidato_reconciliacion_id', '')}")

    invalid_exception_causes = sorted({row.get("causa", "") for row in inspection_exceptions if not material_exception(row.get("causa", ""))})
    if invalid_exception_causes:
        errors.append("EXCEPCION_INSPECCION_NO_MATERIAL:" + ",".join(invalid_exception_causes))
    inspection_denominator, inspection_numerator, missing_objects = inspectable_coverage(states, reports, inspection_exceptions)
    if missing_objects:
        errors.append("OBJETOS_INSPECCIONABLES_SIN_REPORTE:" + ",".join(sorted(missing_objects)))
    plan_assets = unique_nonempty(plans, "activo_id")
    acquired_assets = {row["activo_id"] for row in states if row.get("adquirido") == "SI" and row.get("inspeccionable") == "SI"}
    if plan_assets != acquired_assets:
        errors.append("PLAN_NO_CUBRE_ACTIVOS_ADQUIRIDOS_INSPECCIONABLES")
    report_task_ids = unique_nonempty(reports, "tarea_observacion_id")
    planned_task_ids = unique_nonempty(plans, "tarea_observacion_id")
    if planned_task_ids - report_task_ids:
        errors.append("TAREAS_PLANIFICADAS_SIN_REPORTE")
    contracts_path = universe_dir / "contratos-inspeccion.jsonl"
    contracts_manifest_path = universe_dir / "contratos-inspeccion-hashes.json"
    if not contracts_path.is_file() or not contracts_manifest_path.is_file():
        errors.append("CONTRATOS_INSPECCION_INEXISTENTES")
    else:
        contract_manifest = json.loads(contracts_manifest_path.read_text(encoding="utf-8"))
        if contract_manifest.get("contratos_jsonl_sha256") != sha256(contracts_path):
            errors.append("CONTRATOS_INSPECCION_HASH_INVALIDO")
        if contract_manifest.get("plan_inspeccion_sha256") != sha256(universe_dir / "plan-inspeccion.tsv"):
            errors.append("CONTRATOS_INSPECCION_PLAN_OBSOLETO")
        contract_rows = [json.loads(line) for line in contracts_path.read_text(encoding="utf-8").splitlines() if line]
        contract_task_ids = {str(row.get("tarea_observacion_id", "")) for row in contract_rows}
        if len(contract_rows) != len(contract_task_ids) or contract_task_ids != planned_task_ids:
            errors.append("CONTRATOS_INSPECCION_NO_CUBREN_TAREAS_1A1")
        for payload in contract_rows:
            for error in validate_level1_input(payload):
                errors.append(f"CONTRATO_INSPECCION:{payload.get('tarea_observacion_id', '')}:{error}")
    for report in reports:
        assertion = report.get("afirmacion_tipo", "")
        if assertion not in ALLOWED_ASSERTIONS:
            errors.append(f"AFIRMACION_INVALIDA:{assertion}")
        if "adjudicacion" in report or "necesidad_id" in report or "relacion_id" in report:
            errors.append(f"REPORTE_OPERATIVO_CON_JUICIO:{report.get('reporte_id', '')}")
        if assertion == "NO_OBSERVADO_EN_UNIVERSO_INSPECCIONADO" and not all(
            report.get(field, "") for field in ("objeto_inspeccionado", "universo_inspeccionado", "metodo", "limitacion")
        ):
            errors.append(f"NO_OBSERVADO_SIN_FRONTERA:{report.get('reporte_id', '')}")
    for row in new_objects:
        if row.get("posible_necesidad") != "NO_DETERMINADO" or row.get("razon_inferencia") != "NO_DETERMINADO":
            errors.append(f"OBJETO_NIVEL1_RETROAJUSTADO:{row.get('objeto_observado_id', '')}")

    exception_tasks = unique_nonempty(blinding_exceptions, "tarea_observacion_id")
    if output_root and output_root.is_dir():
        for input_path in output_root.rglob("input.json"):
            payload = json.loads(input_path.read_text(encoding="utf-8"))
            for error in validate_level1_input(payload):
                errors.append(f"{input_path}:{error}")
        for spec_path in output_root.rglob("especificacion-recibida.json"):
            payload = json.loads(spec_path.read_text(encoding="utf-8"))
            if forbidden := sorted(FORBIDDEN_LEVEL1.intersection(payload)):
                errors.append(f"ANALISTA_NO_CEGADO:{spec_path}:{','.join(forbidden)}")
    if len(exception_tasks) != len(blinding_exceptions):
        errors.append("EXCEPCION_CEGAMIENTO_NO_1A1")

    baseline_result = validar_baseline(registry_dir)
    if not baseline_result["ok"]:
        errors.extend("BASELINE:" + error for error in baseline_result["errores"])
    errors.extend(validate_integration_dossier(repo_root))
    baseline_relations = read_tsv(registry_dir / "relaciones.tsv")
    relation_ids = unique_nonempty(baseline_relations, "relacion_id")
    bootstrap = read_tsv(registry_dir / "bootstrap-semantico.tsv")
    if len(bootstrap) != len(relation_ids) or unique_nonempty(bootstrap, "relacion_id") != relation_ids:
        errors.append("BOOTSTRAP_NO_PROCESA_UNIVERSO_SEMANTICO_1A1")
    for row in bootstrap:
        if row.get("clasificacion_relacion_legacy") == "NO_ACCESIBLE" and (
            row.get("estado_evidencia") != "NO_ACCESIBLE" or row.get("adjudicacion_semantica") == "NEGATIVA"
        ):
            errors.append(f"NO_ACCESIBLE_CONVERTIDO_NEGATIVA:{row['relacion_id']}")
        if not row.get("destino_procesamiento"):
            errors.append(f"RELACION_SIN_DESTINO:{row['relacion_id']}")
    candidates_baseline = {row["relacion_id"] for row in baseline_relations if row.get("clasificacion_relacion") == "CANDIDATA"}
    work = read_tsv(registry_dir / "trabajo-semantico.tsv")
    if len(work) != len(candidates_baseline) or unique_nonempty(work, "relacion_id") != candidates_baseline:
        errors.append("CANDIDATAS_NO_CLASIFICADAS_EXACTAMENTE_UNA_VEZ")
    if any("investigar más" in row.get("siguiente_accion", "").casefold() for row in work):
        errors.append("ACCION_NO_OPERATIVA_INVESTIGAR_MAS")

    production = read_tsv(registry_dir / "produccion-modelo.tsv")
    reproducible = [row for row in production if row.get("estado") == "CALCULO_REPRODUCIBLE"]
    for row in reproducible:
        for field in ("especificacion_id", "estimacion", "incertidumbre", "unidad", "n", "suma_pesos", "ponderacion_diseno", "script_ref", "evidencia_ref"):
            if row.get(field) in {"", "NO_DETERMINADO"}:
                errors.append(f"PRODUCCION_SIN_CAMPO_MATERIAL:{row.get('produccion_id', '')}:{field}")
    production_config = json.loads((registry_dir / "especificaciones-produccion.json").read_text(encoding="utf-8"))
    errors.extend(documentacion_fuente_errors(production_config))
    independently_reproduced_production: list[dict[str, str]] = []
    try:
        independently_reproduced_production = verify_production_bundle(
            registry_dir / "especificaciones-produccion.json",
            snapshot_path,
            registry_dir,
            registry_dir / "expedientes-produccion",
            registry_dir / "produccion-modelo.tsv",
            repo_root,
        )
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        errors.append(f"PRODUCCION_NO_REPRODUCIBLE_INDEPENDIENTEMENTE:{exc}")
    productive_route_relations = {
        spec["supervisor_link"]["relacion_id"] for spec in production_config.get("specifications", [])
    }
    descriptive_relations = {
        row["relacion_id"] for row in production
        if row.get("estado_calculo_descriptivo") == "CALCULO_DESCRIPTIVO_DISPONIBLE"
    }
    model_ready_relations = {
        row["relacion_id"] for row in production
        if row.get("estado_uso_modelo") == "LISTA_PARA_USO_MODELO"
    }

    semantic_errors, semantic_execution, semantic_states = validate_semantic_execution(
        repo_root,
        registry_dir,
        snapshot.get("snapshot_t0_sha256", ""),
        sha256(registry_dir / "baseline.json"),
        candidates_baseline,
        work,
    )
    errors.extend(semantic_errors)
    semantic_manifest_for_queue = json.loads(
        (registry_dir / "ejecucion-semantica" / "manifest.json").read_text(encoding="utf-8")
    )
    semantic_run_id = semantic_manifest_for_queue.get("run_id", "")
    semantic_results_for_queue = {
        row.get("relacion_id", ""): row
        for row in read_tsv(
            registry_dir / "ejecucion-semantica" / "runs" / semantic_run_id / "resultados-acciones.tsv"
        )
    }
    residual = read_tsv(registry_dir / "cola-residual.tsv")
    residual_semantic = {
        row.get("relacion_id", ""): row for row in residual
        if row.get("capa") == "UNIVERSO_SEMANTICO"
    }
    if set(residual_semantic) != candidates_baseline or len(residual_semantic) != len(candidates_baseline):
        errors.append("COLA_RESIDUAL_SEMANTICA_NO_1A1")
    for rid, row in residual_semantic.items():
        result_row = semantic_results_for_queue.get(rid, {})
        if (
            row.get("semantic_run_id") != semantic_run_id
            or row.get("estado_ejecucion") != result_row.get("estado_cierre")
            or row.get("reporte_ejecucion_ref") != result_row.get("reporte_neutral_ref")
            or row.get("siguiente_accion") != result_row.get("receta_continuacion")
        ):
            errors.append(f"COLA_RESIDUAL_SEMANTICA_NO_ENLAZADA:{rid}")

    conservative_components_accounted = len(unique_nonempty(states, "activo_id"))
    conservative_components_total = len(set(asset_ids))
    acquired_numerator = len({row["activo_id"] for row in states if row.get("adquirido") == "SI"})
    semantic_numerator = len(unique_nonempty(bootstrap, "relacion_id"))
    semantic_denominator = len(relation_ids)
    coverage = {
        "COBERTURA_DECLARADA": {
            "numerador": conservative_components_accounted,
            "denominador": "NO_DETERMINADO",
            "estado": "NO_DETERMINADO",
            "reserva": "No existe identidad puntual defendible para todos los componentes declarados conservadores.",
        },
        "COMPONENTES_DECLARADOS_CONSERVADORES_CONTABILIZADOS": {
            "numerador": conservative_components_accounted,
            "denominador": conservative_components_total,
            "rotulo_denominador": "COTA_SUPERIOR_NO_RECONCILIADA",
        },
        "COBERTURA_ADQUIRIDA": {
            "numerador": acquired_numerator,
            "denominador": "NO_DETERMINADO",
            "estado": "NO_DETERMINADO",
        },
        "COBERTURA_INSPECCIONADA": {"numerador": inspection_numerator, "denominador": inspection_denominator},
        "COBERTURA_BOOTSTRAP_RUTEO": {"numerador": semantic_numerator, "denominador": semantic_denominator},
        "COBERTURA_SEMANTICA_EJECUTADA_COLA": semantic_execution,
        "RELACIONES_CON_CALCULO_DESCRIPTIVO": {"numerador": len(descriptive_relations), "denominador": len(productive_route_relations)},
        "RELACIONES_LISTAS_PARA_USO_MODELO": {"numerador": len(model_ready_relations), "denominador": len(productive_route_relations)},
    }
    diagnostics = {
        "afirmaciones_observadas": Counter(row.get("afirmacion_tipo", "") for row in reports),
        "objetos_no_representados": len(new_objects),
        "hallazgos_semanticos_potenciales": len(read_tsv(universe_dir / "hallazgos-semanticos-potenciales.tsv")),
        "excepciones_inspeccion": len(inspection_exceptions),
        "excepciones_cegamiento": len(blinding_exceptions),
        "calculos_reproducibles": len(reproducible),
        "filas_produccion_reproducidas_independientemente": len(independently_reproduced_production),
        "producciones_no_determinadas": sum(row.get("estado") == "NO_DETERMINADO" for row in production),
        "clasificacion_trabajo": Counter(row.get("tipo_trabajo", "") for row in work),
        "adjudicacion_legacy": Counter(row.get("clasificacion_relacion", "") for row in baseline_relations),
        "activos_descubiertos_despues_t0": len(read_tsv(universe_dir / "activos-descubiertos-durante-ronda.tsv")),
        "estados_semanticos_recalculados_independientemente": semantic_states,
        "terminales_semanticos_sin_expediente_integrable": sum(semantic_states.values()),
    }
    # No se halló una especificación local exacta que reproduzca el ~0.9%.
    historical_metric = {
        "metrica_anterior": "~0.9%",
        "numerador_anterior": "NO_DETERMINADO",
        "denominador_anterior": "NO_DETERMINADO",
        "definicion_anterior": "NO_DETERMINADO",
        "metrica_actual_comparable": "NO_COMPARABLE_DIRECTAMENTE",
        "reserva": "No existe una definición local exacta verificable de unidad, join y denominador para reproducirla.",
    }
    if snapshot.get("routing_modelos_verificado") is not False:
        reserves.append("routing_modelos_verificado no quedó en false pese a runtime no observable")
    return {
        "ok": not errors,
        "snapshot_t0_sha256": snapshot["snapshot_t0_sha256"],
        "baseline": baseline_result,
        "coberturas": coverage,
        "diagnosticos": diagnostics,
        "metrica_historica": historical_metric,
        "reservas": reserves,
        "errores": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--write-dashboard", type=Path)
    args = parser.parse_args()
    result = validate(args.repo_root.resolve(), args.output_root.resolve() if args.output_root else None)
    if args.write_dashboard:
        path = args.write_dashboard.resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
