#!/usr/bin/env python3
"""Materializa y valida el ledger inmutable de inspecciones del T0 corregido.

El ledger fija la condición histórica de cada identidad local. Una repetición
valida las filas existentes contra bytes, contratos y reportes; no reclasifica
las 509 inspecciones vigentes como reutilizadas solo porque ya existan.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path


REUTILIZADA = "REUTILIZADA_PRE_T0_CORREGIDO"
PRIMERA = "INSPECCIONADA_POR_PRIMERA_VEZ_EN_CORRECCION"
LEDGER_FIELDS = [
    "ledger_id", "run_origen", "snapshot_origen_sha256", "tarea_original_id",
    "tarea_observacion_id", "activo_id", "objeto_logico_id", "ruta_local",
    "sha256", "condicion", "reporte_inspeccion_ref", "reporte_filas_sha256",
    "contrato_input_ref", "contrato_input_sha256", "expediente_origen_sha256",
    "join_auditable",
]
RECOVERED_FIELDS = [
    "activo_id", "objeto_logico_id", "ruta_local", "hash_local",
    "tarea_observacion_id", "reporte_inspeccion_ref", "resultado_inspeccion",
    "afirmaciones_emitidas", "resultado_estructural", "frontera_inspeccion",
    "origen_recuperacion",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha(value: object) -> str:
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def stable_id(prefix: str, *parts: str) -> str:
    return prefix + hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]


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


def _unique(rows: list[dict[str, str]], key: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if not value or value in result:
            raise ValueError(f"{label}_NO_UNICO:{value}")
        result[value] = row
    return result


def _contracts(path: Path) -> dict[str, tuple[dict[str, object], str]]:
    result: dict[str, tuple[dict[str, object], str]] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            payload = json.loads(line)
            task = str(payload["tarea_observacion_id"])
            if task in result:
                raise ValueError(f"CONTRATO_TAREA_DUPLICADO:{task}")
            result[task] = (payload, canonical_sha(payload))
    return result


def _report_groups(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        groups.setdefault(row["tarea_observacion_id"], []).append(row)
    for values in groups.values():
        values.sort(key=lambda row: (row["reporte_id"], row["afirmacion_tipo"], canonical_sha(row)))
    return groups


def _origin_metadata(reuse: dict[str, str]) -> tuple[str, str, str]:
    """Lee procedencia antigua una sola vez; el ledger guarda solo hashes estables."""
    directory = Path(reuse["expediente_origen"])
    match = re.search(r"/(RUN-[^/]+)/inspector/", directory.as_posix())
    run_id = match.group(1) if match else "NO_DETERMINADO"
    snapshot = "NO_DETERMINADO"
    input_path = directory / "input.json"
    if input_path.is_file():
        payload = json.loads(input_path.read_text(encoding="utf-8"))
        run_id = str(payload.get("run_id", run_id))
        snapshot = str(payload.get("snapshot_t0_sha256", snapshot))
    hashes_path = directory / "hashes.json"
    evidence_hash = sha256(hashes_path) if hashes_path.is_file() else "NO_DETERMINADO"
    return run_id, snapshot, evidence_hash


def build_ledger(universe_dir: Path, corpus_root: Path) -> list[dict[str, str]]:
    assets = _unique(
        [row for row in read_tsv(universe_dir / "universo-declarado-t0.tsv")
         if row["estado_adquisicion"] == "ADQUIRIDO"],
        "activo_id", "ACTIVO_ADQUIRIDO",
    )
    states = _unique(
        [row for row in read_tsv(universe_dir / "estado-activos.tsv")
         if row["activo_id"] in assets],
        "activo_id", "ESTADO_ACTIVO",
    )
    plans = _unique(read_tsv(universe_dir / "plan-inspeccion.tsv"), "activo_id", "PLAN_ACTIVO")
    reuse = _unique(
        read_tsv(universe_dir / "reutilizacion-inspecciones.tsv"),
        "activo_id", "REUTILIZACION_ACTIVO",
    )
    if not set(reuse).issubset(assets):
        raise ValueError("REUTILIZACION_FUERA_DE_ACTIVOS_ADQUIRIDOS")
    contracts_path = universe_dir / "contratos-inspeccion.jsonl"
    contracts = _contracts(contracts_path)
    reports = _report_groups(read_tsv(universe_dir / "reportes-inspeccion.tsv"))
    rows: list[dict[str, str]] = []
    for activo_id, asset in sorted(assets.items()):
        state = states[activo_id]
        plan = plans[activo_id]
        task = state["tarea_observacion_id"]
        if task != plan["tarea_observacion_id"]:
            raise ValueError(f"TAREA_ESTADO_PLAN_DIFIERE:{activo_id}")
        if task not in contracts:
            raise ValueError(f"CONTRATO_FALTANTE:{task}")
        contract, contract_hash = contracts[task]
        for field in ("activo_id", "objeto_logico_id", "snapshot_t0_sha256", "run_id"):
            if str(contract[field]) != plan[field]:
                raise ValueError(f"CONTRATO_PLAN_DIFIERE:{task}:{field}")
        report_rows = reports.get(task, [])
        if not report_rows:
            raise ValueError(f"REPORTE_FALTANTE:{task}")
        if {row["activo_id"] for row in report_rows} != {activo_id}:
            raise ValueError(f"REPORTE_ACTIVO_DIFIERE:{task}")
        relative = asset["ruta_local"]
        path = corpus_root / relative
        observed = sha256(path)
        if observed != asset["hash_local"]:
            raise ValueError(f"HASH_LOCAL_DIFIERE_DE_BYTES:{activo_id}:{relative}")
        report_ids = sorted({row["reporte_id"] for row in report_rows})
        if len(report_ids) != 1 or report_ids[0] != state["reporte_inspeccion_ref"]:
            raise ValueError(f"REPORTE_ESTADO_DIFIERE:{task}")
        if activo_id in reuse:
            reused = reuse[activo_id]
            condition = REUTILIZADA
            original_task = reused["tarea_origen_id"]
            run_origin, snapshot_origin, origin_hash = _origin_metadata(reused)
        else:
            condition = PRIMERA
            original_task = task
            run_origin = plan["run_id"]
            snapshot_origin = plan["snapshot_t0_sha256"]
            # Para inspecciones nuevas, el contrato y reporte versionados son
            # la evidencia de origen; no se conserva una ruta efímera a /tmp.
            origin_hash = canonical_sha({
                "contrato": contract_hash,
                "reporte": canonical_sha(report_rows),
            })
        rows.append({
            "ledger_id": stable_id("LED-T0-", relative, observed),
            "run_origen": run_origin,
            "snapshot_origen_sha256": snapshot_origin,
            "tarea_original_id": original_task,
            "tarea_observacion_id": task,
            "activo_id": activo_id,
            "objeto_logico_id": asset["objeto_logico_id"],
            "ruta_local": relative,
            "sha256": observed,
            "condicion": condition,
            "reporte_inspeccion_ref": (
                "data/curacion-universo/reportes-inspeccion.tsv#reporte_id=" + report_ids[0]
            ),
            "reporte_filas_sha256": canonical_sha(report_rows),
            "contrato_input_ref": (
                "data/curacion-universo/contratos-inspeccion.jsonl#tarea_observacion_id=" + task
            ),
            "contrato_input_sha256": contract_hash,
            "expediente_origen_sha256": origin_hash,
            "join_auditable": "RUTA_LOCAL+SHA256+ACTIVO+TAREA+CONTRATO+REPORTE",
        })
    return sorted(rows, key=lambda row: row["ledger_id"])


def validate_ledger(
    ledger: list[dict[str, str]], universe_dir: Path, corpus_root: Path
) -> list[dict[str, str]]:
    expected = build_ledger(universe_dir, corpus_root)
    existing = _unique(ledger, "ledger_id", "LEDGER")
    expected_by_id = _unique(expected, "ledger_id", "LEDGER_ESPERADO")
    if set(existing) != set(expected_by_id):
        raise ValueError("LEDGER_COBERTURA_DIFIERE_DE_IDENTIDADES_LOCALES")
    # La condición y procedencia histórica son inmutables. Los demás campos
    # deben poder reconstruirse exactamente desde archivos versionables.
    immutable = {
        "run_origen", "snapshot_origen_sha256", "tarea_original_id", "condicion",
        "expediente_origen_sha256",
    }
    derived = set(LEDGER_FIELDS) - immutable
    for ledger_id in sorted(existing):
        old = existing[ledger_id]
        new = expected_by_id[ledger_id]
        for field in derived:
            if old.get(field) != new.get(field):
                raise ValueError(f"LEDGER_DERIVADO_DIFIERE:{ledger_id}:{field}")
        if old["condicion"] not in {REUTILIZADA, PRIMERA}:
            raise ValueError(f"LEDGER_CONDICION_INVALIDA:{ledger_id}")
    return [existing[key] for key in sorted(existing)]


def recovered_projection(
    ledger: list[dict[str, str]], universe_dir: Path
) -> list[dict[str, str]]:
    states = _unique(read_tsv(universe_dir / "estado-activos.tsv"), "activo_id", "ESTADO")
    report_rows = read_tsv(universe_dir / "reportes-inspeccion.tsv")
    reports = _report_groups(report_rows)
    rows: list[dict[str, str]] = []
    for item in ledger:
        if item["condicion"] != PRIMERA:
            continue
        task = item["tarea_observacion_id"]
        assertions = reports[task]
        facts = [row for row in assertions if row["afirmacion_tipo"] == "HECHO_OBSERVADO"]
        if len(facts) != 1:
            raise ValueError(f"HECHO_ESTRUCTURAL_NO_UNICO:{task}")
        state = states[item["activo_id"]]
        rows.append({
            "activo_id": item["activo_id"],
            "objeto_logico_id": item["objeto_logico_id"],
            "ruta_local": item["ruta_local"],
            "hash_local": item["sha256"],
            "tarea_observacion_id": task,
            "reporte_inspeccion_ref": state["reporte_inspeccion_ref"],
            "resultado_inspeccion": state["estado_descriptivo"],
            "afirmaciones_emitidas": str(len(assertions)),
            "resultado_estructural": facts[0]["valor_o_descripcion"],
            "frontera_inspeccion": facts[0]["limitacion"],
            "origen_recuperacion": "FALSO_COLAPSO_URL_T0_CORREGIDO",
        })
    return sorted(rows, key=lambda row: row["activo_id"])


def derive(
    universe_dir: Path, output: Path, ledger_path: Path | None = None,
    corpus_root: Path | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    ledger_path = ledger_path or universe_dir / "ledger-inspecciones-t0.tsv"
    if corpus_root is None:
        snapshot = json.loads((universe_dir / "snapshot-t0.json").read_text(encoding="utf-8"))
        corpus_root = Path(snapshot["corpus_root"])
    if ledger_path.exists():
        ledger = validate_ledger(read_tsv(ledger_path), universe_dir, corpus_root)
    else:
        ledger = build_ledger(universe_dir, corpus_root)
    write_tsv(ledger_path, LEDGER_FIELDS, ledger)
    recovered = recovered_projection(ledger, universe_dir)
    write_tsv(output, RECOVERED_FIELDS, recovered)
    counts = Counter(row["condicion"] for row in ledger)
    summary = {
        "ledger_sha256": sha256(ledger_path),
        "identidades_locales_en_ledger": len(ledger),
        "condiciones": dict(sorted(counts.items())),
        "objetos_recuperados": len(recovered),
        "regla_idempotencia": (
            "la condición histórica se lee del ledger y se valida contra filas derivadas; "
            "nunca se reclasifica por existencia del expediente vigente"
        ),
    }
    ledger_path.with_name(ledger_path.stem + "-resumen.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return recovered, ledger


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--universe-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--corpus-root", type=Path)
    args = parser.parse_args()
    recovered, ledger = derive(
        args.universe_dir.resolve(), args.output.resolve(),
        args.ledger.resolve() if args.ledger else None,
        args.corpus_root.resolve() if args.corpus_root else None,
    )
    print(json.dumps({
        "ok": True,
        "identidades_en_ledger": len(ledger),
        "condiciones": dict(Counter(row["condicion"] for row in ledger)),
        "objetos_recuperados": len(recovered),
        "resultados": dict(Counter(row["resultado_inspeccion"] for row in recovered)),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
