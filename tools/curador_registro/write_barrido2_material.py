#!/usr/bin/env python3
"""Congela productos materiales finales de BARRIDO-2 desde expedientes E2.

El índice neutral completo permanece privado. El reporte versionable agrupa
registros homogéneos y conserva un record_id de muestra dereferenciable, los
hashes de lote y el conteo; no vuelve a interpretar contenido.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

try:
    from .barrido2_material import (
        MATERIAL_BUILD_VERSION,
        PRIVACY_CONTRACT,
        REPORT_FIELDS,
        canonical_sha,
        material_build_sha256,
        safe_text,
        sha256_file,
        validate_material_files,
        validate_material_snapshot,
    )
    from .write_barrido2_w0 import CENSUS_SUFFIX, FUERA_HEADER, LEDGER_HEADER
except ImportError:
    from barrido2_material import (
        MATERIAL_BUILD_VERSION,
        PRIVACY_CONTRACT,
        REPORT_FIELDS,
        canonical_sha,
        material_build_sha256,
        safe_text,
        sha256_file,
        validate_material_files,
        validate_material_snapshot,
    )
    from write_barrido2_w0 import CENSUS_SUFFIX, FUERA_HEADER, LEDGER_HEADER


ABSOLUTE_RE = re.compile(r"^(?:/|[A-Za-z]:[/\\])")


def _atomic_stream(path: Path, callback: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            callback(handle)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_text(path: Path, text: str) -> None:
    _atomic_stream(path, lambda handle: handle.write(text.encode("utf-8")))


def _read_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            raise ValueError(f"TSV_SIN_CABECERA:{path.name}")
        return list(reader.fieldnames), list(reader)


def _write_tsv(path: Path, fields: list[str], rows: list[dict[str, Any]]) -> None:
    def emit(binary: Any) -> None:
        import io

        text = io.TextIOWrapper(binary, encoding="utf-8", newline="", write_through=True)
        writer = csv.DictWriter(text, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            projected = {
                field: (
                    "NO-APLICA"
                    if row.get(field) is None or row.get(field) == ""
                    else str(row.get(field))
                )
                for field in fields
            }
            if any(value == "" or len(value) > 160 for value in projected.values()):
                raise ValueError("TSV_DURABLE_CELDA_INVALIDA")
            if any("\t" in value or "\r" in value or "\n" in value for value in projected.values()):
                raise ValueError("TSV_DURABLE_CONTROL_INVALIDO")
            if any(ABSOLUTE_RE.match(value) for value in projected.values()):
                raise ValueError("TSV_DURABLE_RUTA_ABSOLUTA")
            writer.writerow(projected)
        text.detach()

    _atomic_stream(path, emit)


def _compact_reports(
    summaries: list[dict[str, Any]], staging_root: Path
) -> list[dict[str, str]]:
    compact: list[dict[str, str]] = []
    for summary in sorted(summaries, key=lambda row: row["representacion_id"]):
        report_path = staging_root / summary["tarea_id"] / "reportes-durables.tsv"
        groups: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        with report_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            if reader.fieldnames != REPORT_FIELDS:
                raise ValueError(f"REPORTE_CABECERA_INVALIDA:{summary['tarea_id']}")
            for row in reader:
                key = (
                    row["objeto_tipo"], row["estado"], row["privacidad"],
                    row["frontera_inspeccion"],
                )
                group = groups.setdefault(key, {"count": 0, "first": row})
                group["count"] += 1
        for key, group in sorted(groups.items()):
            first = group["first"]
            count = int(group["count"])
            report_id = "RPTC-B2-" + hashlib.sha256(
                (summary["representacion_id"] + "\0" + "\0".join(key)).encode("utf-8")
            ).hexdigest()
            description, _ = safe_text(
                f"{first['objeto_tipo']}; objetos={count}; muestra={first['record_id']}",
                durable=True,
            )
            row = {
                **first,
                "reporte_id": report_id,
                "afirmacion_tipo": "RESUMEN-NEUTRAL-COMPACTO",
                "descripcion_neutral": description,
            }
            if any(value == "" or len(str(value)) > 160 for value in row.values()):
                raise ValueError(f"REPORTE_COMPACTO_INVALIDO:{report_id}")
            compact.append({field: str(row[field]) for field in REPORT_FIELDS})
    return sorted(compact, key=lambda row: row["reporte_id"])


def _ruta_relativa(path: Path, base: Path) -> str:
    """Ruta relativa al repo cuando se puede; nunca una ruta absoluta durable."""
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        return path.name


def _prisma(
    snapshot: dict[str, Any], summaries: list[dict[str, Any]], report_count: int,
    date: str, invocacion: dict[str, str],
) -> str:
    declarations = snapshot["declarations"]
    representations = snapshot["representations"]
    declaration_states = Counter(row["estado_e0"] for row in declarations)
    representation_states = Counter(row["estado_e0"] for row in representations)
    waves = Counter(row["wave_initial"] for row in representations)
    total_e1 = sum(int(row["objetos_e1"]) for row in summaries)
    total_e2 = sum(int(row["objetos_e2"]) for row in summaries)
    total_exceptions = sum(int(row["excepciones"]) for row in summaries)
    metrics = [
        ("declaraciones_totales", len(declarations), "declaraciones del manifiesto"),
        ("declaraciones_con_archivo_sha", snapshot["counts"]["declaraciones_con_archivo_sha"], "declaraciones del manifiesto"),
        ("declaraciones_sin_archivo_sha", snapshot["counts"]["declaraciones_sin_archivo_sha"], "declaraciones del manifiesto"),
        ("representaciones_fisicas", len(representations), "archivos de las dos raíces configuradas"),
        ("sha_unicos", snapshot["counts"]["contenidos_sha_unicos"], "representaciones físicas"),
        ("representaciones_declaradas", snapshot["counts"]["representaciones_declaradas"], "representaciones físicas"),
        ("representaciones_no_declaradas", snapshot["counts"]["representaciones_no_declaradas"], "representaciones físicas"),
        ("fuera_de_disco", snapshot["counts"]["fuera_de_disco"], "declaraciones con archivo+sha"),
        ("divergentes_hash_o_tamano", sum(v for k, v in declaration_states.items() if "DIVERGENTE" in k), "declaraciones con archivo+sha"),
        ("corruptas_E0", representation_states["CORRUPTO"], "representaciones físicas"),
        ("cifradas_E0", representation_states["CIFRADO"], "representaciones físicas"),
        ("no_soportadas_E0", representation_states["FORMATO-NO-SOPORTADO"], "representaciones físicas"),
        ("reutilizadas", sum(row["reutilizada_desde_representacion_id"] != "NO-APLICA" for row in summaries), "representaciones E2"),
        ("abiertas_E1", len(summaries), "representaciones físicas"),
        ("caracterizadas_E2_o_excepcion", len(summaries), "representaciones físicas"),
        ("representaciones_con_excepcion", sum(int(row["excepciones"]) > 0 for row in summaries), "representaciones E2"),
        ("excepciones_por_objeto", total_exceptions, "objetos E1"),
        ("objetos_logicos_E1", total_e1, "objetos enumerados"),
        ("objetos_caracterizados_E2", total_e2, "objetos E1"),
        ("reportes_durables_compactos", report_count, "grupos representación/tipo/estado/privacidad/frontera"),
        ("ola_W1", waves["W1"], "representaciones físicas"),
        ("ola_W2", waves["W2"], "representaciones físicas"),
        ("ola_W3", waves["W3"], "representaciones físicas"),
        ("ola_W4", waves["W4"], "representaciones físicas"),
        ("ola_W5_reintentos", 0, "referencias a representaciones ya asignadas"),
    ]
    lines = [
        "# PRISMA material BARRIDO-2", "",
        f"Fecha: {date}. Estado: CERRADO-E2. Red material: deshabilitada.", "",
        "| Métrica | Cifra | Denominador | Comando de derivación |",
        "|---|---:|---|---|",
    ]
    lines.extend(f"| {name} | {value} | {denominator} | `CMD-MATERIAL` |" for name, value, denominator in metrics)
    lines.extend([
        # El comando se DERIVA de la invocación real, no se teclea. La versión
        # anterior estaba cableada a la generación `v2` y publicaba cifras que
        # salían de otra: 0 de 672 `tarea_id` derivaban de v2 y 672 de 672 de la
        # generación vigente. Un comando que no corre no es procedencia.
        "", "Comando `CMD-MATERIAL` (derivado de la invocación que produjo estas cifras):", "", "```sh",
        "unshare -Urn -- python3 tools/curador_registro/write_barrido2_material.py \\",
        f"  --snapshot {invocacion['snapshot']} \\",
        f"  --task-ledger {invocacion['task_ledger']} \\",
        f"  --task-root {invocacion['task_root']} --staging-root {invocacion['staging_root']} \\",
        f"  --contract {invocacion['contract']} \\",
        f"  --contract-hashes {invocacion['contract_hashes']} \\",
        f"  --output-root . --private-index {invocacion['private_index']} --date {date}",
        "```", "",
        "Partición: W1∪W2∪W3∪W4=universo físico; intersecciones vacías; W5 sin reintentos.", "",
    ])
    return "\n".join(lines)


def write_final(
    snapshot_path: Path, task_ledger_path: Path, task_root: Path,
    staging_root: Path, contract_path: Path, contract_hashes_path: Path,
    output_root: Path, private_index_path: Path, date: str,
) -> dict[str, Any]:
    gate = validate_material_files(
        snapshot_path,
        contract_path,
        task_root,
        task_ledger_path,
        staging_root,
        require_complete=True,
    )
    if not gate["ok"]:
        raise ValueError("GATE_MATERIAL_INVALIDO:" + ";".join(gate["errors"][:200]))
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    errors = validate_material_snapshot(snapshot)
    if errors:
        raise ValueError("SNAPSHOT_INVALIDO:" + ";".join(errors))
    contract_hash = sha256_file(contract_path)
    frozen = json.loads(contract_hashes_path.read_text(encoding="utf-8"))
    if frozen["files"].get("data/curacion-universo/contrato-barrido2-v1_0.json") != contract_hash:
        raise ValueError("CONTRATO_NO_CONGELADO")
    _, ledger = _read_tsv(task_ledger_path)
    if len(ledger) != len(snapshot["representations"]) or any(row["estado_terminal"] != "SI" for row in ledger):
        raise ValueError("LEDGER_NO_TERMINAL_1A1")
    task_by_rep: dict[str, dict[str, Any]] = {}
    summaries: list[dict[str, Any]] = []
    for row in ledger:
        task_path = task_root / f"{row['tarea_id']}.json"
        summary_path = staging_root / row["tarea_id"] / "resumen.json"
        task = json.loads(task_path.read_text(encoding="utf-8"))
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        if not (
            task["representacion_id"] == row["representacion_id"] == summary["representacion_id"]
            and task["contrato_sha256"] == summary["contrato_sha256"] == contract_hash
            and summary["build_sha256"] == material_build_sha256()
            and summary["parser_version"] == MATERIAL_BUILD_VERSION
            and summary["network_habilitada"] is False
            and summary["privacidad"] == PRIVACY_CONTRACT
        ):
            raise ValueError(f"EXPEDIENTE_NO_EXACTO:{row['tarea_id']}")
        task_by_rep[row["representacion_id"]] = {**task, **summary}
        summaries.append(summary)

    def emit_index(handle: Any) -> None:
        for summary in sorted(summaries, key=lambda row: row["tarea_id"]):
            source = staging_root / summary["tarea_id"] / "e2-neutral-index.jsonl"
            with source.open("rb") as incoming:
                while block := incoming.read(1024 * 1024):
                    handle.write(block)

    _atomic_stream(private_index_path, emit_index)
    compact = _compact_reports(summaries, staging_root)
    universe = output_root / "data/curacion-universo"
    report_path = universe / "reportes-inspeccion-barrido2-v1_0.tsv"
    _write_tsv(report_path, REPORT_FIELDS, compact)

    representations = {row["representacion_id"]: row for row in snapshot["representations"]}
    durable_ledger: list[dict[str, Any]] = []
    for row in sorted(ledger, key=lambda item: item["representacion_id"]):
        rep = representations[row["representacion_id"]]
        summary = task_by_rep[row["representacion_id"]]
        durable_ledger.append({
            "ledger_id": "LED-B2-" + hashlib.sha256(f"{row['representacion_id']}\0{contract_hash}".encode()).hexdigest(),
            "representacion_id": row["representacion_id"], "payload_id": row["payload_id"],
            "root_id": row["root_id"],
            "ruta_relativa": safe_text(row["ruta_relativa"], durable=True)[0],
            "sha256": row["sha256"],
            "wave_initial": row["wave_initial"], "wave_retry_ref": row["wave_retry_ref"],
            "estado_e0": rep["estado_e0"], "grado_inspeccion": "E2",
            "objetos_e1": summary["objetos_e1"], "objetos_e2": summary["objetos_e2"],
            "excepciones": summary["excepciones"], "reporte_neutral_ref": "E2B-" + summary["batch_sha256"],
            "contrato_sha256": contract_hash, "reporte_sha256": summary["report_sha256"],
            "parser": summary["parser"], "parser_version": summary["parser_version"],
            "network_habilitada": "false", "estado_terminal": "SI", "fecha": date,
        })
    ledger_path = universe / "ledger-inspecciones-barrido2.tsv"
    _write_tsv(ledger_path, LEDGER_HEADER, durable_ledger)

    census_path = output_root / f"data/censo-explotacion-{date}.tsv"
    census_header, census = _read_tsv(census_path)
    if census_header[-len(CENSUS_SUFFIX):] != CENSUS_SUFFIX:
        raise ValueError("CENSO_CABECERA_INVALIDA")
    for row in census:
        rep_id = row["representacion_id"]
        if rep_id == "NO-APLICA" or rep_id not in task_by_rep:
            continue
        summary = task_by_rep[rep_id]
        row.update({
            "grado_inspeccion": "E2", "objetos_logicos": str(summary["objetos_e1"]),
            "frontera_inspeccion": summary["frontera_inspeccion"],
            "reporte_neutral_ref": "E2B-" + summary["batch_sha256"],
            "contrato_sha256": contract_hash, "reporte_sha256": summary["report_sha256"],
        })
    _write_tsv(census_path, census_header, census)

    prisma_path = universe / "prisma-material-barrido2.md"
    _atomic_text(prisma_path, _prisma(snapshot, summaries, len(compact), date, {
        key: _ruta_relativa(value, output_root)
        for key, value in (
            ("snapshot", snapshot_path), ("task_ledger", task_ledger_path),
            ("task_root", task_root), ("staging_root", staging_root),
            ("contract", contract_path), ("contract_hashes", contract_hashes_path),
            ("private_index", private_index_path),
        )
    }))
    inventory = [{"representacion_id": row["representacion_id"], "sha256": row["sha256"]} for row in sorted(snapshot["representations"], key=lambda item: item["representacion_id"])]
    parser_counts = Counter(summary["parser"] for summary in summaries)
    baseline = {
        "schema_version": "BARRIDO2-MATERIAL-BASELINE-1.0",
        "base_sha": json.loads(contract_path.read_text(encoding="utf-8"))["base_sha"],
        "manifest_sha": snapshot["manifest_sha"], "roots_config_sha256": snapshot["roots_config_sha256"],
        "inventory_sha256": canonical_sha(inventory),
        "parsers": {"build_version": MATERIAL_BUILD_VERSION, "build_sha256": material_build_sha256(), "counts": dict(sorted(parser_counts.items())), "writer_sha256": sha256_file(Path(__file__))},
        "contracts": frozen["files"],
        "reports": {"estado": "CERRADO-E2", "durable_rows": len(compact), "durable_sha256": sha256_file(report_path), "snapshot_sha256": snapshot["snapshot_sha256"]},
        "exceptions": {"objetos_con_excepcion": sum(int(row["excepciones"]) for row in summaries), "representaciones_con_excepcion": sum(int(row["excepciones"]) > 0 for row in summaries)},
        "counts": {**snapshot["counts"], "waves": dict(sorted(Counter(row["wave_initial"] for row in snapshot["representations"]).items())), "representaciones_e2_terminales": len(summaries), "objetos_e1": sum(int(row["objetos_e1"]) for row in summaries), "objetos_e2": sum(int(row["objetos_e2"]) for row in summaries), "reportes_durables": len(compact)},
        "network_habilitada": False, "e2_index_sha256": sha256_file(private_index_path),
        "ledger_sha256": sha256_file(ledger_path), "prisma_material_sha256": sha256_file(prisma_path), "fecha": date,
    }
    schema = json.loads((Path(__file__).with_name("schemas") / "barrido2-material-baseline.schema.json").read_text(encoding="utf-8"))
    schema_errors = list(Draft202012Validator(schema).iter_errors(baseline))
    if schema_errors:
        raise ValueError("BASELINE_SCHEMA_INVALIDO:" + schema_errors[0].message)
    baseline_path = universe / "baseline-material-barrido2.json"
    _atomic_text(baseline_path, json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return {"ok": True, "representations": len(summaries), "e2_records": baseline["counts"]["objetos_e1"], "durable_reports": len(compact), "index_sha256": baseline["e2_index_sha256"], "report_sha256": baseline["reports"]["durable_sha256"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--task-ledger", type=Path, required=True)
    parser.add_argument("--task-root", type=Path, required=True)
    parser.add_argument("--staging-root", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--contract-hashes", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--private-index", type=Path, required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    result = write_final(
        args.snapshot.resolve(), args.task_ledger.resolve(), args.task_root.resolve(),
        args.staging_root.resolve(), args.contract.resolve(), args.contract_hashes.resolve(),
        args.output_root.resolve(), args.private_index.resolve(), args.date,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
