#!/usr/bin/env python3
"""Proyecta el snapshot privado BARRIDO-2 a productos versionables de W0.

No abre material. Consume únicamente el snapshot y el ledger de tareas ya
validados, conserva el esquema del censo anterior y aplica el límite durable de
160 caracteres con redacción explícita. Todos los conteos se rederivan; ninguna
cifra del encargo funciona como constante de aceptación.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

try:
    from .barrido2_material import (
        MATERIAL_BUILD_VERSION,
        canonical_sha,
        material_build_sha256,
        safe_text,
        sha256_file,
        validate_material_snapshot,
    )
except ImportError:
    from barrido2_material import (
        MATERIAL_BUILD_VERSION,
        canonical_sha,
        material_build_sha256,
        safe_text,
        sha256_file,
        validate_material_snapshot,
    )


CENSUS_SUFFIX = [
    "sha256_observado", "representacion_id", "estado_e0", "grado_inspeccion",
    "objetos_logicos", "frontera_inspeccion", "reporte_neutral_ref",
    "contrato_sha256", "reporte_sha256",
]
FUERA_HEADER = [
    "id_manifiesto", "raiz", "archivo", "sha256_declarado",
    "tamano_declarado", "estado_observado", "universo_busqueda", "mecanismo",
    "fecha", "razon",
]
LEDGER_HEADER = [
    "ledger_id", "representacion_id", "payload_id", "root_id",
    "ruta_relativa", "sha256", "wave_initial", "wave_retry_ref", "estado_e0",
    "grado_inspeccion", "objetos_e1", "objetos_e2", "excepciones",
    "reporte_neutral_ref", "contrato_sha256", "reporte_sha256", "parser",
    "parser_version", "network_habilitada", "estado_terminal", "fecha",
]
STRUCTURAL_FIELDS = {
    "id_manifiesto", "payload_id", "representacion_id", "sha256",
    "sha256_observado", "sha256_declarado", "contrato_sha256",
    "reporte_sha256", "ledger_id", "raiz", "root_id", "wave_initial",
    "wave_retry_ref", "estado", "estado_e0", "estado_observado",
    "grado_inspeccion", "objetos_logicos", "objetos_e1", "objetos_e2",
    "excepciones", "reporte_neutral_ref", "parser", "parser_version",
    "network_habilitada", "estado_terminal", "fecha", "tamano_bytes",
    "tamano_declarado",
}


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_bytes(payload)
    temporary.replace(path)


def _tsv_bytes(header: list[str], rows: Iterable[dict[str, object]]) -> bytes:
    import io

    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=header, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    for source in rows:
        row: dict[str, str] = {}
        for field in header:
            value = source.get(field, "NO-APLICA")
            if field in STRUCTURAL_FIELDS:
                text = str(value or "NO-APLICA")
                if len(text) > 160 or any(character in text for character in "\t\r\n"):
                    raise ValueError(f"CAMPO_ESTRUCTURAL_DURABLE_INVALIDO:{field}")
            else:
                text, _ = safe_text(value, durable=True)
            row[field] = text
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def _load_tsv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if not reader.fieldnames:
            raise ValueError(f"TSV_SIN_CABECERA:{path}")
        return list(reader.fieldnames), list(reader)


def _predecessor_defaults(declaration: dict[str, Any], manifest_sha: str) -> dict[str, str]:
    state = str(declaration["estado_e0"])
    return {
        "usado_para_declara_uso": "NO-DETERMINADO-W0",
        "necesidades_que_lo_citan": "NO-DETERMINADO-W0",
        "tsv_de_apertura_que_lo_toca": "NO-APLICA",
        "estado": state,
        "universo_declarado": f"manifiesto.yaml@{manifest_sha[:12]}",
        "consumo_detectado": "NO-DETERMINADO-W0",
        "consumo_universo_declarado": "W0 material; semántica no evaluada",
    }


def _prisma_markdown(snapshot: dict[str, Any], date: str) -> str:
    declarations = snapshot["declarations"]
    representations = snapshot["representations"]
    counts = snapshot["counts"]
    declaration_states = Counter(row["estado_e0"] for row in declarations)
    representation_states = Counter(row["estado_e0"] for row in representations)
    waves = Counter(row["wave_initial"] for row in representations)
    metrics = [
        ("declaraciones_totales", counts["declaraciones_totales"], "declaraciones del manifiesto"),
        ("declaraciones_con_archivo_sha", counts["declaraciones_con_archivo_sha"], "declaraciones del manifiesto"),
        ("declaraciones_sin_archivo_sha", counts["declaraciones_sin_archivo_sha"], "declaraciones del manifiesto"),
        ("representaciones_fisicas", counts["representaciones_fisicas"], "archivos de las dos raíces configuradas"),
        ("sha_unicos", counts["contenidos_sha_unicos"], "representaciones físicas"),
        ("representaciones_declaradas", counts["representaciones_declaradas"], "representaciones físicas"),
        ("representaciones_no_declaradas", counts["representaciones_no_declaradas"], "representaciones físicas"),
        ("fuera_de_disco", counts["fuera_de_disco"], "declaraciones con archivo+sha"),
        ("divergentes_hash_o_tamano", sum(value for key, value in declaration_states.items() if "DIVERGENTE" in key), "declaraciones con archivo+sha"),
        ("corruptas_E0", representation_states["CORRUPTO"], "representaciones físicas"),
        ("cifradas_E0", representation_states["CIFRADO"], "representaciones físicas"),
        ("no_soportadas_E0", representation_states["FORMATO-NO-SOPORTADO"], "representaciones físicas"),
        ("reutilizadas", 0, "representaciones físicas; W0 no abre"),
        ("abiertas_E1", 0, "representaciones físicas; W0 no abre"),
        ("caracterizadas_E2", 0, "representaciones físicas; W0 no abre"),
        ("excepciones_de_apertura", 0, "representaciones físicas; W0 no abre"),
        ("objetos_logicos", 0, "objetos enumerados; W0 no abre"),
        ("reportes", 0, "registros E2; W0 no abre"),
        ("ola_W1", waves["W1"], "representaciones físicas"),
        ("ola_W2", waves["W2"], "representaciones físicas"),
        ("ola_W3", waves["W3"], "representaciones físicas"),
        ("ola_W4", waves["W4"], "representaciones físicas"),
        ("ola_W5_reintentos", 0, "referencias a representaciones ya asignadas"),
    ]
    lines = [
        "# PRISMA material BARRIDO-2 · W0",
        "",
        f"Fecha: {date}. Estado: PRELIMINAR-W0. Red material: deshabilitada.",
        "",
        "| Métrica | Cifra | Denominador | Comando de derivación |",
        "|---|---:|---|---|",
    ]
    for metric, value, denominator in metrics:
        lines.append(f"| {metric} | {value} | {denominator} | `CMD-W0` |")
    lines.extend([
        "", "Comando `CMD-W0`:", "", "```sh",
        "unshare -Urn -- python3 tools/curador_registro/snapshot_universe.py \\",
        "  --barrido2 --manifest data/manifiesto.yaml \\",
        "  --roots-config data/raices.local.yaml \\",
        "  --snapshot-output .barrido2/private/t0/snapshot.json",
        "```", "",
        "La partición inicial es disjunta y exhaustiva:",
        "W1∪W2∪W3∪W4=universo físico; W5 permanece vacío en W0.", "",
    ])
    return "\n".join(lines)


def write_w0(
    snapshot_path: Path,
    task_ledger_path: Path,
    contract_path: Path,
    contract_hashes_path: Path,
    previous_census_path: Path,
    output_root: Path,
    date: str,
) -> dict[str, Any]:
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    errors = validate_material_snapshot(snapshot)
    if errors:
        raise ValueError("SNAPSHOT_MATERIAL_INVALIDO:" + ";".join(errors))
    if snapshot.get("network_habilitada") is not False:
        raise ValueError("SNAPSHOT_NETWORK_NO_FALSE")
    contract_hash = sha256_file(contract_path)
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    frozen = json.loads(contract_hashes_path.read_text(encoding="utf-8"))
    if frozen.get("files", {}).get("data/curacion-universo/contrato-barrido2-v1_0.json") != contract_hash:
        raise ValueError("CONTRATO_NO_COINCIDE_CONGELACION")
    old_header, old_rows = _load_tsv(previous_census_path)
    expected_prefix = [
        "id_manifiesto", "archivo", "raiz", "tamano_bytes",
        "usado_para_declara_uso", "necesidades_que_lo_citan",
        "tsv_de_apertura_que_lo_toca", "estado", "universo_declarado",
        "consumo_detectado", "consumo_universo_declarado",
    ]
    if old_header != expected_prefix:
        raise ValueError("CENSO_PREDECESOR_CABECERA_INESPERADA")
    old_by_id = {row["id_manifiesto"]: row for row in old_rows}
    exploitable = [
        row for row in snapshot["declarations"]
        if row["ruta_relativa"] != "NO-APLICA" and row["sha256_declarado"] != "NO-APLICA"
    ]
    census_rows: list[dict[str, object]] = []
    for declaration in sorted(exploitable, key=lambda row: row["payload_id"]):
        payload_id = declaration["payload_id"]
        previous = old_by_id.get(payload_id, {})
        row: dict[str, object] = {
            **_predecessor_defaults(declaration, snapshot["manifest_sha"]),
            **previous,
            "id_manifiesto": payload_id,
            "archivo": declaration["ruta_relativa"],
            "raiz": declaration["root_id"],
            "tamano_bytes": declaration["tamano_declarado"],
            "sha256_observado": declaration["sha256_observado"],
            "representacion_id": declaration["representacion_id"],
            "estado_e0": declaration["estado_e0"],
            "grado_inspeccion": "E0",
            "objetos_logicos": "0",
            "frontera_inspeccion": "W0-CONTABILIZACION-E-INTEGRIDAD",
            "reporte_neutral_ref": "NO-APLICA",
            "contrato_sha256": contract_hash,
            "reporte_sha256": "NO-APLICA",
        }
        census_rows.append(row)

    missing = [row for row in exploitable if row["estado_e0"] == "FUERA-DE-DISCO"]
    fuera_rows = [{
        "id_manifiesto": row["payload_id"], "raiz": row["root_id"],
        "archivo": row["ruta_relativa"], "sha256_declarado": row["sha256_declarado"],
        "tamano_declarado": row["tamano_declarado"], "estado_observado": row["estado_e0"],
        "universo_busqueda": "data_raw+descargas_mx (raíces configuradas)",
        "mecanismo": "JOIN-EXACTO-RAIZ-RUTA+INVENTARIO-SHA256-W0", "fecha": date,
        "razon": "NO-LOCALIZADO-EN-UNIVERSO-CONFIGURADO",
    } for row in sorted(missing, key=lambda item: item["payload_id"])]

    task_header, tasks = _load_tsv(task_ledger_path)
    required_task = {"representacion_id", "payload_id", "root_id", "ruta_relativa", "sha256", "wave_initial", "wave_retry_ref", "contrato_sha256"}
    if not required_task.issubset(task_header) or len(tasks) != len(snapshot["representations"]):
        raise ValueError("LEDGER_TAREAS_NO_RECONCILIA_W0")
    reps = {row["representacion_id"]: row for row in snapshot["representations"]}
    ledger_rows: list[dict[str, object]] = []
    for task in sorted(tasks, key=lambda row: row["representacion_id"]):
        representation = reps.get(task["representacion_id"])
        if not representation or task["sha256"] != representation["sha256"] or task["contrato_sha256"] != contract_hash:
            raise ValueError("LEDGER_TAREA_JOIN_INVALIDO_W0")
        ledger_rows.append({
            "ledger_id": "LED-B2-" + hashlib.sha256(f"{task['representacion_id']}\0{contract_hash}".encode()).hexdigest(),
            "representacion_id": task["representacion_id"], "payload_id": task["payload_id"],
            "root_id": task["root_id"], "ruta_relativa": task["ruta_relativa"],
            "sha256": task["sha256"], "wave_initial": task["wave_initial"],
            "wave_retry_ref": task["wave_retry_ref"], "estado_e0": representation["estado_e0"],
            "grado_inspeccion": "E0", "objetos_e1": "0", "objetos_e2": "0",
            "excepciones": "0", "reporte_neutral_ref": "NO-APLICA",
            "contrato_sha256": contract_hash, "reporte_sha256": "NO-APLICA",
            "parser": "NO-APLICA", "parser_version": "NO-APLICA",
            "network_habilitada": "false", "estado_terminal": "NO", "fecha": date,
        })

    data_root = output_root / "data"
    universe_root = data_root / "curacion-universo"
    census_path = data_root / f"censo-explotacion-{date}.tsv"
    fuera_path = data_root / "fuera-de-disco-v1_0.tsv"
    ledger_path = universe_root / "ledger-inspecciones-barrido2.tsv"
    prisma_path = universe_root / "prisma-material-barrido2.md"
    baseline_path = universe_root / "baseline-material-barrido2.json"
    _atomic_bytes(census_path, _tsv_bytes(expected_prefix + CENSUS_SUFFIX, census_rows))
    _atomic_bytes(fuera_path, _tsv_bytes(FUERA_HEADER, fuera_rows))
    _atomic_bytes(ledger_path, _tsv_bytes(LEDGER_HEADER, ledger_rows))
    prisma = _prisma_markdown(snapshot, date)
    _atomic_bytes(prisma_path, prisma.encode("utf-8"))

    inventory = [
        {"representacion_id": row["representacion_id"], "sha256": row["sha256"]}
        for row in sorted(snapshot["representations"], key=lambda item: item["representacion_id"])
    ]
    empty_sha = hashlib.sha256(b"").hexdigest()
    baseline = {
        "schema_version": "BARRIDO2-MATERIAL-BASELINE-1.0",
        "base_sha": contract["base_sha"], "manifest_sha": snapshot["manifest_sha"],
        "roots_config_sha256": snapshot["roots_config_sha256"],
        "inventory_sha256": canonical_sha(inventory),
        "parsers": {
            "estado": "PRELIMINAR-W0", "build_version": MATERIAL_BUILD_VERSION,
            "build_sha256": material_build_sha256(),
            "w0_writer_sha256": sha256_file(Path(__file__)),
        },
        "contracts": frozen["files"],
        "reports": {"estado": "PENDIENTE-E2", "durable_rows": 0, "snapshot_sha256": snapshot["snapshot_sha256"]},
        "exceptions": {"estado": "NO-EVALUADAS-W0", "materiales_abiertas": 0},
        "counts": {**snapshot["counts"], "waves": dict(sorted(Counter(row["wave_initial"] for row in snapshot["representations"]).items())), "objetos_e2": 0, "reportes": 0},
        "network_habilitada": False, "e2_index_sha256": empty_sha,
        "ledger_sha256": sha256_file(ledger_path),
        "prisma_material_sha256": sha256_file(prisma_path), "fecha": date,
    }
    _atomic_bytes(baseline_path, (json.dumps(baseline, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return {
        "ok": True, "censo": len(census_rows), "fuera_de_disco": len(fuera_rows),
        "ledger": len(ledger_rows), "snapshot_sha256": snapshot["snapshot_sha256"],
        "outputs": [str(path.relative_to(output_root)) for path in (census_path, fuera_path, ledger_path, prisma_path, baseline_path)],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--task-ledger", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--contract-hashes", type=Path, required=True)
    parser.add_argument("--previous-census", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--date", required=True)
    args = parser.parse_args()
    result = write_w0(
        args.snapshot.resolve(), args.task_ledger.resolve(), args.contract.resolve(),
        args.contract_hashes.resolve(), args.previous_census.resolve(),
        args.output_root.resolve(), args.date,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
