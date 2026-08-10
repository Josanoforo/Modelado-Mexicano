#!/usr/bin/env python3
"""Conserva en datos versionables los inputs validados de inspectores T0."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

try:
    from .inspect_assets import FORBIDDEN_TASK_FIELDS
except ImportError:
    from inspect_assets import FORBIDDEN_TASK_FIELDS


REQUIRED = {
    "tarea_observacion_id", "run_id", "snapshot_t0_sha256", "activo_id",
    "objeto_logico_id", "rutas_localizadores", "grado_inspeccion", "criterio_parada",
}

EXCEPTION_FIELDS = [
    "excepcion_cegamiento_id", "tarea_observacion_id", "campo_revelado",
    "razon_indispensable", "autoridad", "alcance", "riesgo_sesgo", "fecha",
    "run_id", "snapshot_t0_sha256", "activo_id", "contrato_input_ref",
    "contrato_input_sha256", "reporte_inspeccion_ref", "reporte_filas_sha256",
    "estado",
]

HISTORY_FIELDS = [
    "excepcion_cegamiento_id", "tarea_observacion_id", "campo_revelado",
    "razon_indispensable", "autoridad", "alcance", "riesgo_sesgo", "fecha",
    "run_id_historico", "snapshot_t0_sha256_historico", "activos_historicos",
    "reporte_inspeccion_ref_historico", "reporte_inspeccion_sha256_historico",
    "resumen_sha256_historico", "estado_historia", "razon_historia",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=fields, delimiter="\t", lineterminator="\n",
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)


def canonical_sha(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def reconcile_exceptions(
    exceptions_path: Path,
    history_path: Path,
    contracts: list[dict[str, object]],
    reports_path: Path,
    legacy_output_root: Path | None,
) -> tuple[int, int]:
    """Conserva activas solo excepciones con referencialidad vigente completa."""
    if not exceptions_path.exists():
        write_tsv(exceptions_path, EXCEPTION_FIELDS, [])
        write_tsv(history_path, HISTORY_FIELDS, [])
        return 0, 0
    old_active = read_tsv(exceptions_path)
    old_history = read_tsv(history_path) if history_path.exists() else []
    contract_by_task = {str(row["tarea_observacion_id"]): row for row in contracts}
    reports_by_task: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_tsv(reports_path):
        reports_by_task[row["tarea_observacion_id"]].append(row)
    active: list[dict[str, str]] = []
    historical = {row["excepcion_cegamiento_id"]: row for row in old_history}
    for exception in old_active:
        task = exception["tarea_observacion_id"]
        contract = contract_by_task.get(task)
        report_rows = reports_by_task.get(task, [])
        if contract is not None and report_rows:
            report_rows.sort(key=lambda row: (row["reporte_id"], row["afirmacion_tipo"], canonical_sha(row)))
            report_ids = sorted({row["reporte_id"] for row in report_rows})
            assets = sorted({row["activo_id"] for row in report_rows})
            if len(report_ids) != 1 or len(assets) != 1:
                raise ValueError(f"EXCEPCION_REPORTE_NO_UNIVOCO:{task}")
            active.append({
                **exception,
                "run_id": str(contract["run_id"]),
                "snapshot_t0_sha256": str(contract["snapshot_t0_sha256"]),
                "activo_id": assets[0],
                "contrato_input_ref": (
                    "data/curacion-universo/contratos-inspeccion.jsonl#tarea_observacion_id=" + task
                ),
                "contrato_input_sha256": canonical_sha(contract),
                "reporte_inspeccion_ref": (
                    "data/curacion-universo/reportes-inspeccion.tsv#reporte_id=" + report_ids[0]
                ),
                "reporte_filas_sha256": canonical_sha(report_rows),
                "estado": "ACTIVA_REFERENCIALIDAD_COMPLETA",
            })
            continue

        # La excepción pertenecía al snapshot anterior y ya no alimenta el
        # expediente vigente. Se conserva explícitamente, con hashes si el
        # output histórico todavía está disponible, y se retira de activas.
        legacy_dirs = (
            sorted(legacy_output_root.glob(f"*/inspector/{task}"))
            if legacy_output_root and legacy_output_root.exists() else []
        )
        directory = legacy_dirs[0] if len(legacy_dirs) == 1 else None
        run_id = "NO_DETERMINADO"
        snapshot = "NO_DETERMINADO"
        assets: list[str] = []
        report_ref = "NO_VERSIONADO;OUTPUT_HISTORICO_FUERA_DEL_REPO"
        report_hash = "NO_DETERMINADO"
        summary_hash = "NO_DETERMINADO"
        if directory:
            summary_path = directory / "resumen.json"
            report_path = directory / "reporte-inspeccion.tsv"
            if summary_path.is_file():
                summary = json.loads(summary_path.read_text(encoding="utf-8"))
                run_id = str(summary.get("run_id", "NO_DETERMINADO"))
                snapshot = str(summary.get("snapshot_t0_sha256", "NO_DETERMINADO"))
                summary_hash = sha256(summary_path)
            if report_path.is_file():
                historical_reports = read_tsv(report_path)
                assets = sorted({row["activo_id"] for row in historical_reports})
                report_hash = sha256(report_path)
                report_ids = sorted({row["reporte_id"] for row in historical_reports})
                if len(report_ids) == 1:
                    report_ref = f"reporte_id={report_ids[0]};sha256={report_hash}"
        historical[exception["excepcion_cegamiento_id"]] = {
            **exception,
            "run_id_historico": run_id,
            "snapshot_t0_sha256_historico": snapshot,
            "activos_historicos": ";".join(assets) if assets else "NO_DETERMINADO",
            "reporte_inspeccion_ref_historico": report_ref,
            "reporte_inspeccion_sha256_historico": report_hash,
            "resumen_sha256_historico": summary_hash,
            "estado_historia": "HISTORICA_NO_ACTIVA",
            "razon_historia": (
                "La tarea no pertenece al plan/contratos/reportes del snapshot vigente; "
                "la evidencia consumida vigente usa los reportes estructurales actuales"
            ),
        }
    active.sort(key=lambda row: row["excepcion_cegamiento_id"])
    history_rows = [historical[key] for key in sorted(historical)]
    write_tsv(exceptions_path, EXCEPTION_FIELDS, active)
    write_tsv(history_path, HISTORY_FIELDS, history_rows)
    return len(active), len(history_rows)


def collect(
    plan_path: Path, output_root: Path, output_path: Path,
    exceptions_path: Path | None = None,
    history_path: Path | None = None,
    reports_path: Path | None = None,
    legacy_output_root: Path | None = None,
) -> dict[str, object]:
    plans = read_tsv(plan_path)
    contracts: list[dict[str, object]] = []
    for plan in plans:
        matches = sorted(output_root.glob(f"{plan['run_id']}/inspector/{plan['tarea_observacion_id']}"))
        if len(matches) != 1:
            raise ValueError(f"EXPEDIENTE_INSPECTOR_NO_UNICO:{plan['tarea_observacion_id']}")
        directory = matches[0]
        hashes = json.loads((directory / "hashes.json").read_text(encoding="utf-8"))
        for name, expected in hashes.items():
            path = directory / name
            if not path.is_file() or sha256(path) != expected:
                raise ValueError(f"HASH_EXPEDIENTE_INVALIDO:{path}")
        payload = json.loads((directory / "input.json").read_text(encoding="utf-8"))
        missing = REQUIRED - set(payload)
        forbidden = FORBIDDEN_TASK_FIELDS.intersection(payload)
        if missing or forbidden:
            raise ValueError(
                f"CONTRATO_INSPECTOR_INVALIDO:{plan['tarea_observacion_id']}:"
                f"faltantes={sorted(missing)}:prohibidos={sorted(forbidden)}"
            )
        for field in ("tarea_observacion_id", "run_id", "snapshot_t0_sha256", "activo_id", "objeto_logico_id"):
            if str(payload[field]) != plan[field]:
                raise ValueError(f"CONTRATO_PLAN_NO_RECONCILIA:{plan['tarea_observacion_id']}:{field}")
        payload["expediente_worker_sha256"] = sha256(directory / "hashes.json")
        contracts.append(payload)
    contracts.sort(key=lambda row: str(row["tarea_observacion_id"]))
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        for payload in contracts:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
    manifest = {
        "contratos": len(contracts),
        "contratos_jsonl_sha256": sha256(output_path),
        "plan_inspeccion_sha256": sha256(plan_path),
        "run_ids": sorted({str(row["run_id"]) for row in contracts}),
        "schema_ref": "tools/curador_registro/schemas/inspector-task.schema.json",
    }
    if exceptions_path is not None:
        if history_path is None or reports_path is None:
            raise ValueError("EXCEPCIONES_REQUIEREN_HISTORIA_Y_REPORTES")
        active_count, history_count = reconcile_exceptions(
            exceptions_path, history_path, contracts, reports_path, legacy_output_root,
        )
        manifest.update({
            "excepciones_cegamiento_activas": active_count,
            "excepciones_cegamiento_historicas": history_count,
            "excepciones_cegamiento_sha256": sha256(exceptions_path),
            "historia_cegamiento_sha256": sha256(history_path),
        })
    manifest_path = output_path.with_name(output_path.stem + "-hashes.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--exceptions", type=Path)
    parser.add_argument("--exception-history", type=Path)
    parser.add_argument("--reports", type=Path)
    parser.add_argument("--legacy-output-root", type=Path)
    args = parser.parse_args()
    result = collect(
        args.plan.resolve(), args.output_root.resolve(), args.output.resolve(),
        args.exceptions.resolve() if args.exceptions else None,
        args.exception_history.resolve() if args.exception_history else None,
        args.reports.resolve() if args.reports else None,
        args.legacy_output_root.resolve() if args.legacy_output_root else None,
    )
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
