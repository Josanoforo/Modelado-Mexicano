#!/usr/bin/env python3
"""Integra capa 4 BARRIDO-2 desde propuestas supervisadas, fail-closed.

Este modulo no decide semantica ni consume el cableado.  Solo comprueba el
expediente propuesta -> tarea -> reporte -> baseline material y proyecta en
una copia completa del registro los cambios de capa 4 ya supervisados.
"""

from __future__ import annotations

import csv
import fcntl
import hashlib
import json
import os
import tempfile
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .baseline import ARCHIVOS_TSV, leer_tsv, validar_baseline
    from .bootstrap import build_bootstrap
    from .classify_work import classify
    from .sync_bootstrap import _freeze_manifest
    from .tareas_barrido2 import TASK_FIELDS
except ImportError:
    from baseline import ARCHIVOS_TSV, leer_tsv, validar_baseline
    from bootstrap import build_bootstrap
    from classify_work import classify
    from sync_bootstrap import _freeze_manifest
    from tareas_barrido2 import TASK_FIELDS


PROPOSAL_FIELDS = [
    "propuesta_id", "tarea_id", "reporte_id", "payload_id",
    "representacion_id", "sha256", "objeto_logico_id", "necesidad_id",
    "reactivo_id", "accion_propuesta", "relacion_id_actual", "veredicto_a4",
    "evidencia_ref", "frontera_semantica", "confianza",
    "requiere_decision_mesa", "decision_mesa_id", "dependencia_fp24",
    "razon_gate", "estado_supervision", "supervisor_id", "fecha",
]
DECISION_FIELDS = PROPOSAL_FIELDS + [
    "estado_integracion", "razon_integracion", "journal_id",
]
INTEGRABLE_ACTIONS = {"CAMBIO", "SIN_CAMBIO", "TERMINAL"}
INTEGRATION_STATES = {
    "INTEGRADA", "RECHAZADA_FAIL_CLOSED", "CONFLICTO_MATERIAL",
    "REQUIERE_DECISION_FP24", "NO_APLICA_TERMINAL", "PROPUESTA_ALTA",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return prefix + hashlib.sha256(payload).hexdigest()


def read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader.fieldnames or []), list(reader)


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    """Escribe TSV plano.

    No usa ``csv.DictWriter``: este repositorio guarda tabuladores sin comillas
    y el escritor estándar entrecomilla cualquier celda que contenga `"`, lo que
    reescribía bytes de filas que nadie tocó y hacía que una corrida sin
    integraciones apareciera como cambio.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["\t".join(fields)]
    for row in rows:
        cells = []
        for field in fields:
            value = str(row.get(field, ""))
            if "\t" in value or "\n" in value or "\r" in value:
                raise ValueError(f"celda con separador crudo en {field}: {value[:60]!r}")
            cells.append(value)
        lines.append("\t".join(cells))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tsv_preservando(
    path: Path, fields: list[str], rows: list[dict[str, str]],
    original_bytes: bytes, original_rows: list[dict[str, str]],
) -> None:
    """Reescribe sólo si el contenido cambió de verdad.

    La idempotencia del integrador es un criterio de cierre (§28.16): una
    segunda corrida sin propuestas nuevas debe dejar el registro byte a byte
    igual.  Reserializar es suficiente para romperlo aunque ninguna celda haya
    cambiado, así que cuando las filas son las mismas se devuelven los bytes
    originales en lugar de volver a escribirlas.
    """
    if rows == original_rows:
        path.write_bytes(original_bytes)
    else:
        write_tsv(path, fields, rows)


def registry_hashes(registry: Path) -> dict[str, str]:
    names = [*ARCHIVOS_TSV.values(), "baseline.json", "bootstrap-semantico.tsv", "trabajo-semantico.tsv"]
    return {name: sha256(registry / name) for name in names}


def _schema_errors(row: dict[str, str], schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    return [error.message for error in Draft202012Validator(schema).iter_errors(row)]


def _material_task_hash(task_root: Path, task_id: str) -> str | None:
    path = task_root / f"{task_id}.json"
    return sha256(path) if path.is_file() else None


def _row_key(row: dict[str, str]) -> tuple[str, ...]:
    return (
        row.get("reporte_id", ""), row.get("record_id", ""),
        row.get("record_sha256", ""), row.get("payload_id", ""),
        row.get("representacion_id", ""), row.get("sha256", ""),
    )


def preflight(
    registry: Path,
    material_baseline_path: Path,
    proposals_path: Path,
    tasks_path: Path,
    reports_path: Path,
    ledger_path: Path,
    material_task_root: Path,
) -> dict[str, Any]:
    """Valida el expediente sin confiar en estados declarados."""
    baseline_validation = validar_baseline(registry)
    errors: list[str] = []
    if not baseline_validation["ok"]:
        errors.extend(f"BASELINE_INVALIDO:{value}" for value in baseline_validation["errores"])
    material_baseline = json.loads(material_baseline_path.read_text(encoding="utf-8"))
    if material_baseline.get("network_habilitada") is not False:
        errors.append("BASELINE_MATERIAL_RED_NO_ES_FALSE")
    if material_baseline.get("reports", {}).get("durable_sha256") != sha256(reports_path):
        errors.append("REPORTE_DURABLE_HASH_DIVERGENTE")
    if material_baseline.get("ledger_sha256") != sha256(ledger_path):
        errors.append("LEDGER_MATERIAL_HASH_DIVERGENTE")

    proposal_fields, proposals = read_tsv(proposals_path)
    task_fields, tasks = read_tsv(tasks_path)
    report_fields, reports = read_tsv(reports_path)
    _, ledger = read_tsv(ledger_path)
    if proposal_fields != PROPOSAL_FIELDS:
        errors.append("PROPUESTAS_CABECERA_INVALIDA")
    if task_fields != TASK_FIELDS:
        errors.append("TAREAS_CABECERA_INVALIDA")
    if not reports or not report_fields:
        errors.append("REPORTES_DURABLES_VACIOS")

    schema_path = Path(__file__).with_name("schemas") / "barrido2-semantic-proposal.schema.json"
    for row in proposals:
        if _schema_errors(row, schema_path):
            errors.append(f"PROPUESTA_SCHEMA_INVALIDO:{row.get('propuesta_id', '')}")
    proposal_ids = Counter(row.get("propuesta_id", "") for row in proposals)
    if any(not key or count != 1 for key, count in proposal_ids.items()):
        errors.append("PROPUESTA_ID_NO_UNICO")
    task_ids = Counter(row.get("tarea_id", "") for row in tasks)
    if any(not key or count != 1 for key, count in task_ids.items()):
        errors.append("TAREA_ID_NO_UNICO")

    tasks_by_id = {row["tarea_id"]: row for row in tasks}
    reports_by_key = {_row_key(row): row for row in reports}
    if len(reports_by_key) != len(reports):
        errors.append("REPORTE_DURABLE_CLAVE_AMBIGUA")
    ledger_by_rep = {row.get("representacion_id", ""): row for row in ledger}
    relations = {row["relacion_id"]: row for row in leer_tsv(registry / "relaciones.tsv")}
    material_baseline_hash = sha256(material_baseline_path)

    for task in tasks:
        task_id = task.get("tarea_id", "")
        if task.get("material_baseline_sha256") != material_baseline_hash:
            errors.append(f"TAREA_BASELINE_MATERIAL_OBSOLETO:{task_id}")
        # El descriptor material lo nombra `material_tarea_id`, no `tarea_id`:
        # dos relaciones pueden apoyarse en la misma representación y la tarea
        # semántica necesita identidad propia para no colisionar.
        if _material_task_hash(material_task_root, task.get("material_tarea_id", "")) != task.get("material_task_sha256"):
            errors.append(f"TAREA_MATERIAL_HASH_INVALIDO:{task_id}")
        ledger_row = ledger_by_rep.get(task.get("representacion_id", ""))
        if ledger_row is None or any(
            ledger_row.get(field, "") != task.get(field, "")
            for field in ("payload_id", "representacion_id", "sha256")
        ):
            errors.append(f"TAREA_LEDGER_JOIN_INVALIDO:{task_id}")
        report_key = (
            task.get("reporte_id", ""), task.get("reporte_record_id", ""),
            task.get("reporte_record_sha256", ""), task.get("payload_id", ""),
            task.get("representacion_id", ""), task.get("sha256", ""),
        )
        if report_key not in reports_by_key:
            errors.append(f"TAREA_REPORTE_JOIN_INVALIDO:{task_id}")
        relation = relations.get(task.get("relacion_id", ""))
        if relation is None:
            errors.append(f"TAREA_RELACION_INEXISTENTE:{task_id}")
        elif relation.get("necesidad_id") != task.get("necesidad_id"):
            errors.append(f"TAREA_NECESIDAD_DIVERGENTE:{task_id}")

    for proposal in proposals:
        pid = proposal.get("propuesta_id", "")
        task = tasks_by_id.get(proposal.get("tarea_id", ""))
        if task is None:
            errors.append(f"PROPUESTA_TAREA_INEXISTENTE:{pid}")
            continue
        joins = {
            "reporte_id": "reporte_id", "payload_id": "payload_id",
            "representacion_id": "representacion_id", "sha256": "sha256",
            "objeto_logico_id": "objeto_logico_id", "necesidad_id": "necesidad_id",
            "reactivo_id": "reactivo_id", "relacion_id_actual": "relacion_id",
            "frontera_semantica": "frontera_semantica",
        }
        if any(proposal.get(left, "") != task.get(right, "") for left, right in joins.items()):
            errors.append(f"PROPUESTA_TAREA_JOIN_INVALIDO:{pid}")
        expected_evidence = f"{task.get('e2_record_id', '')}:{task.get('e2_record_sha256', '')}"
        if proposal.get("evidencia_ref") != expected_evidence:
            errors.append(f"PROPUESTA_E2_REF_INVALIDA:{pid}")
        if proposal.get("dependencia_fp24") == "SI" and proposal.get("estado_supervision") != "REQUIERE_DECISION_FP24":
            errors.append(f"FP24_ESTADO_INCONSISTENTE:{pid}")
        if proposal.get("dependencia_fp24") == "NO" and (
            proposal.get("requiere_decision_mesa") != "NO"
            or proposal.get("decision_mesa_id") != "NO-APLICA"
        ):
            errors.append(f"FP24_CAMPOS_INCONSISTENTES:{pid}")
        if proposal.get("accion_propuesta") in INTEGRABLE_ACTIONS and proposal.get("dependencia_fp24") == "NO":
            if proposal.get("estado_supervision") != "VALIDADA":
                errors.append(f"PROPUESTA_NO_SUPERVISADA:{pid}")
        # Una ALTA validada NO es un error de expediente: preflight solo
        # verifica joins/hashes, y esta fila ya los pasó arriba. Si construir
        # el high path procede es decisión de acto (encargo madre §19/§21),
        # no de preflight -- _apply_layer4 la emite como PROPUESTA_ALTA.

    return {
        "ok": not errors,
        "errors": sorted(set(errors)),
        "proposals": proposals,
        "tasks": tasks,
        "relations": relations,
        "material_baseline_sha256": material_baseline_hash,
        "registry_hashes": registry_hashes(registry),
        "high_path_built": False,
    }


def _compact(value: str, limit: int = 160) -> str:
    clean = " ".join(value.split()) or "NO-APLICA"
    return clean if len(clean) <= limit else clean[: limit - 1] + "…"


def _apply_layer4(
    candidate: Path,
    proposals: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Proyecta solo decisiones unanimemente supervisadas por relacion."""
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in proposals:
        grouped[row["relacion_id_actual"]].append(row)
    decisions: list[dict[str, str]] = []
    accepted: dict[str, list[dict[str, str]]] = {}
    journal_id = stable_id("JRN-B2-", *sorted(row["propuesta_id"] for row in proposals))
    for relation_id, rows in sorted(grouped.items()):
        verdicts = {row["veredicto_a4"] for row in rows}
        fp24 = any(row["dependencia_fp24"] == "SI" for row in rows)
        supervised = all(row["estado_supervision"] == "VALIDADA" for row in rows)
        if fp24:
            state, reason = "REQUIERE_DECISION_FP24", "FP-24 abierta; la propuesta declara dependencia material específica"
        elif any(row["accion_propuesta"] == "ALTA" for row in rows):
            if supervised:
                # Validada pero sin high path en esta corrida: no es error ni
                # rechazo, queda pendiente de que exista al menos una ALTA
                # validada para que un acto la construya (encargo madre §19).
                state, reason = "PROPUESTA_ALTA", "WARN: ALTA validada sin high path construido; pendiente de decisión de acto, no se integra ni se rechaza"
            else:
                state, reason = "RECHAZADA_FAIL_CLOSED", "High path ausente: la corrida no puede inventar identidad de alta"
        elif len(verdicts) != 1:
            state, reason = "CONFLICTO_MATERIAL", "Representaciones supervisadas producen veredictos A4 incompatibles"
        elif not supervised:
            state, reason = "RECHAZADA_FAIL_CLOSED", "La propuesta no está supervisada como VALIDADA"
        else:
            state, reason = "INTEGRADA", "Capa 4 proyectada desde propuestas supervisadas y joins verificados"
            accepted[relation_id] = rows
        for row in rows:
            decision = dict(row)
            decision.update({
                "estado_integracion": state,
                "razon_integracion": _compact(reason),
                "journal_id": journal_id,
            })
            decisions.append(decision)

    relation_fields, relation_rows = read_tsv(candidate / "relaciones.tsv")
    evidence_fields, evidence_rows = read_tsv(candidate / "evidencias.tsv")
    utility_fields, utility_rows = read_tsv(candidate / "utilidad-modelo.tsv")
    originales = {
        name: ((candidate / name).read_bytes(), deepcopy(rows))
        for name, rows in (
            ("relaciones.tsv", relation_rows),
            ("evidencias.tsv", evidence_rows),
            ("utilidad-modelo.tsv", utility_rows),
        )
    }
    relation_by_id = {row["relacion_id"]: row for row in relation_rows}
    evidence_by_relation: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in evidence_rows:
        evidence_by_relation[row["relacion_id"]].append(row)
    utility_by_id = {row["relacion_id"]: row for row in utility_rows}
    for relation_id, rows in accepted.items():
        first = sorted(rows, key=lambda row: row["propuesta_id"])[0]
        verdict = first["veredicto_a4"]
        refs = ";".join(sorted({row["evidencia_ref"] for row in rows}))
        objects = ";".join(sorted({row["objeto_logico_id"] for row in rows}))
        relation = relation_by_id[relation_id]
        relation["capa4_apertura_mapeo"] = verdict
        relation["reason_code"] = "BARRIDO2_E2_SUPERVISADO"
        relation["evidencia_ref"] = _compact(refs)
        relation["evidencia_textual_breve"] = _compact(f"{verdict}; objetos={objects}")
        relation["confianza"] = first["confianza"]
        note = relation.get("nota", "")
        marker = "[BARRIDO-2 2026-08-17] capa4 por integración fail-closed."
        relation["nota"] = _compact(note if marker in note else f"{note} {marker}", 1000)
        for evidence in evidence_by_relation[relation_id]:
            evidence["tipo_evidencia"] = "E2_BARRIDO2_SUPERVISADO"
            evidence["evidencia_ref"] = _compact(refs)
            evidence["evidencia_localizador"] = _compact(objects)
            evidence["variable_reactivo_tabla"] = _compact(";".join(sorted({row["reactivo_id"] for row in rows})))
            evidence["texto_evidencia"] = _compact(f"{verdict}; expediente={journal_id}")
            evidence["incertidumbre"] = _compact(first["frontera_semantica"])
        # `siguiente_accion` NO se toca, ni en evidencias ni en utilidad. Es la
        # acción original de la cola residual y su preservación es invariante
        # comprobado en dos sitios: `classify_work.py:62` exige que evidencia y
        # utilidad la declaren idéntica, y `semantic_run` la vuelve a verificar
        # como ACCION_O_CRITERIO_NO_PRESERVADO. Capa 4 vive en `relaciones`.
        utility = utility_by_id[relation_id]
        utility["evidencia_disponible"] = verdict
        utility["reserva"] = _compact(first["frontera_semantica"])
        utility["verificacion_requerida"] = "NO-APLICA: E2 y supervisión BARRIDO-2 verificadas"
        utility["requiere_decision"] = first["requiere_decision_mesa"]
        utility["decision_id"] = first["decision_mesa_id"]

    for name, fields, rows in (
        ("relaciones.tsv", relation_fields, sorted(relation_rows, key=lambda row: row["relacion_id"])),
        ("evidencias.tsv", evidence_fields, evidence_rows),
        ("utilidad-modelo.tsv", utility_fields, sorted(utility_rows, key=lambda row: row["relacion_id"])),
    ):
        original_bytes, original_rows = originales[name]
        write_tsv_preservando(candidate / name, fields, rows, original_bytes, original_rows)
    return decisions, sorted(accepted.values(), key=lambda rows: rows[0]["relacion_id_actual"])


def _replace_with_rollback(outputs: dict[Path, bytes], registry: Path) -> None:
    originals = {path: path.read_bytes() if path.exists() else None for path in outputs}
    temporaries: dict[Path, Path] = {}
    try:
        for path, payload in outputs.items():
            descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
            temporary = Path(name)
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            temporaries[path] = temporary
        for path in outputs:
            os.replace(temporaries[path], path)
        final = validar_baseline(registry)
        if not final["ok"]:
            raise ValueError("BASELINE_POST_REEMPLAZO_INVALIDO:" + ";".join(final["errores"]))
    except Exception:
        for path, payload in originals.items():
            if payload is None:
                path.unlink(missing_ok=True)
            else:
                path.write_bytes(payload)
        raise
    finally:
        for temporary in temporaries.values():
            temporary.unlink(missing_ok=True)


def integrate_barrido2(
    registry: Path,
    material_baseline: Path,
    proposals: Path,
    tasks: Path,
    reports: Path,
    ledger: Path,
    material_task_root: Path,
    mapping: Path,
    declarations: Path,
    universe: Path,
    asset_states: Path,
    rules: Path,
    output_dir: Path,
    *,
    apply: bool,
) -> dict[str, Any]:
    checked = preflight(
        registry, material_baseline, proposals, tasks, reports, ledger,
        material_task_root,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    if not checked["ok"]:
        result = {
            "ok": False, "applied": False, "errors": checked["errors"],
            "high_path_built": False, "propuestas_altas_validadas": sum(
                row.get("accion_propuesta") == "ALTA" and row.get("estado_supervision") == "VALIDADA"
                for row in checked["proposals"]
            ),
        }
        (output_dir / "integracion-validada-barrido2.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return result

    before = checked["registry_hashes"]
    with tempfile.TemporaryDirectory(prefix=".integrate-barrido2-", dir=registry.parent) as temp_name:
        candidate = Path(temp_name) / "registry"
        candidate.mkdir()
        for filename in [*ARCHIVOS_TSV.values(), "baseline.json"]:
            (candidate / filename).write_bytes((registry / filename).read_bytes())
        decisions, accepted_groups = _apply_layer4(candidate, checked["proposals"])
        _freeze_manifest(candidate, json.loads((registry / "baseline.json").read_text(encoding="utf-8")))
        validation = validar_baseline(candidate)
        if not validation["ok"]:
            raise ValueError("BASELINE_CANDIDATO_INVALIDO:" + ";".join(validation["errores"]))
        build_bootstrap(candidate, mapping, declarations, universe, asset_states, candidate / "bootstrap-semantico.tsv")
        classify(candidate / "bootstrap-semantico.tsv", candidate, rules, candidate / "trabajo-semantico.tsv")
        relation_ids = {row["relacion_id"] for row in leer_tsv(candidate / "relaciones.tsv")}
        bootstrap_ids = {row["relacion_id"] for row in leer_tsv(candidate / "bootstrap-semantico.tsv")}
        if relation_ids != bootstrap_ids:
            raise ValueError("BOOTSTRAP_POST_INTEGRACION_NO_1A1")
        names = [*ARCHIVOS_TSV.values(), "baseline.json", "bootstrap-semantico.tsv", "trabajo-semantico.tsv"]
        after = {name: sha256(candidate / name) for name in names}
        changed = sorted(name for name in names if before.get(name) != after.get(name))
        journal_id = decisions[0]["journal_id"] if decisions else stable_id("JRN-B2-", "VACIO")
        result = {
            "ok": True,
            "applied": bool(apply and changed),
            "journal_id": journal_id,
            "propuestas": len(checked["proposals"]),
            "propuestas_altas_validadas": sum(
                row.get("accion_propuesta") == "ALTA" and row.get("estado_supervision") == "VALIDADA"
                for row in checked["proposals"]
            ),
            "high_path_built": False,
            "relaciones_integradas": len(accepted_groups),
            "decisiones": Counter(row["estado_integracion"] for row in decisions),
            "changed": changed,
            "before_sha256": before,
            "after_sha256": after,
            "material_baseline_sha256": checked["material_baseline_sha256"],
            "proposals_sha256": sha256(proposals),
            "tasks_sha256": sha256(tasks),
            "reports_sha256": sha256(reports),
        }
        write_tsv(output_dir / "decisiones-integracion-barrido2.tsv", DECISION_FIELDS, decisions)
        lock_path = registry / ".barrido2-integrate.lock"
        if apply and changed:
            with lock_path.open("w") as lock_handle:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
                if registry_hashes(registry) != before:
                    raise ValueError("BASELINE_CAMBIO_DURANTE_TRANSACCION")
                outputs = {registry / name: (candidate / name).read_bytes() for name in names}
                _replace_with_rollback(outputs, registry)
                if registry_hashes(registry) != after:
                    raise ValueError("RELECTURA_POST_INTEGRACION_DIVERGENTE")
        (output_dir / "journal-integracion-barrido2.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=dict) + "\n",
            encoding="utf-8",
        )
        result["journal_sha256"] = sha256(output_dir / "journal-integracion-barrido2.json")
        (output_dir / "integracion-validada-barrido2.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True, default=dict) + "\n",
            encoding="utf-8",
        )
        return result
