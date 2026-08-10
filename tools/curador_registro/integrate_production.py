#!/usr/bin/env python3
"""Reproduce y enlaza producción sin confiar en firmas del analista.

El supervisor reconstruye el contrato cegado desde la especificación maestra,
recalcula los hashes de las fuentes y ejecuta el motor versionado en un
directorio temporal limpio. ``hashes.json`` del analista no participa en
ninguna decisión de aceptación.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.curador_registro.prepare_production import (
    FORBIDDEN,
    canonical_analyst_spec,
    canonical_json_bytes,
)
from tools.curador_registro.produce import execute, stable_json


def stable_id(prefix: str, *parts: str) -> str:
    return prefix + hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:24]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def artifact_ref(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def resolve_ref(repo_root: Path, ref: str) -> Path:
    path = Path(ref.split("#", 1)[0])
    return path if path.is_absolute() else repo_root / path


def verify_neutral_evidence_sources(evidence_path: Path) -> None:
    """Rehash every local source declared by the neutral evidence document."""
    document = json.loads(evidence_path.read_text(encoding="utf-8"))
    verified = 0

    def walk(value: Any) -> None:
        nonlocal verified
        if isinstance(value, dict):
            for path_key, hash_key in (
                ("ruta", "hash_sha256"),
                ("descriptor_ruta", "descriptor_hash_sha256"),
            ):
                if path_key in value and hash_key in value:
                    source = Path(value[path_key])
                    if not source.is_file() or sha256(source) != value[hash_key]:
                        raise ValueError(f"fuente de evidencia neutral ausente o alterada: {source}")
                    verified += 1
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)
    if verified == 0:
        raise ValueError("evidencia neutral sin fuentes locales verificables")


PRODUCTION_FIELDS = [
    "produccion_id", "especificacion_id", "relacion_id", "objeto_modelo_origen",
    "tipo_producto", "estimando", "estimacion", "incertidumbre", "poblacion",
    "dominio", "unidad", "periodo", "periodo_referencia", "edicion",
    "periodo_levantamiento", "n", "suma_pesos", "ponderacion_diseno",
    "transformacion", "tipo_inferencia", "input_path", "input_member",
    "hash_microdato", "snapshot_t0_sha256", "snapshot_ref", "hash_snapshot_archivo",
    "baseline_ref", "baseline_sha256",
    "especificacion_input_ref", "hash_especificacion_input",
    "especificacion_fuente_ref", "hash_especificacion_fuente", "resultado_ref",
    "hash_resultado", "resumen_ref", "hash_resumen", "script_ref",
    "hash_script_reproducible", "motor_produccion_ref", "hash_motor_produccion",
    "integrador_produccion_ref", "hash_integrador_produccion",
    "evidencia_neutral_ref", "hash_evidencia_neutral", "evidencia_ref", "estado",
    "estado_calculo_descriptivo", "estado_uso_modelo", "verificacion_supervisor",
    "reserva", "requiere_decision",
]


def production_bytes(rows: list[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=PRODUCTION_FIELDS, delimiter="\t", lineterminator="\n"
    )
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda row: row["produccion_id"]))
    return stream.getvalue().encode("utf-8")


def _validate_inspection_link(
    result: dict[str, str], inspection_reports: dict[str, list[dict[str, str]]]
) -> None:
    report_refs = [ref for ref in result["evidencia_ref"].split(";") if ref.startswith("RINS-")]
    if not report_refs:
        raise ValueError(
            f"resultado sin reporte neutral: {result['especificacion_id']}:{result['variable']}"
        )
    input_path = Path(result["input_path"])
    for report_ref in report_refs:
        candidates = inspection_reports.get(report_ref, [])
        if not any(
            report.get("afirmacion_tipo") == "HECHO_OBSERVADO"
            and report.get("evidencia_ref") == f"sha256:{result['hash_microdato']}"
            and Path(report.get("localizador", "")).resolve() == input_path.resolve()
            for report in candidates
        ):
            raise ValueError(
                f"reporte neutral no enlaza ruta+hash: {result['especificacion_id']}:{report_ref}"
            )


def _verify_one(
    full: dict[str, Any],
    snapshot_hash: str,
    baseline_hash: str,
    analyst_root: Path,
    repo_root: Path,
    schema: dict[str, Any],
    relations: set[str],
    inspection_reports: dict[str, list[dict[str, str]]],
) -> tuple[list[dict[str, str]], dict[str, str]]:
    spec_id = full["especificacion_id"]
    directory = analyst_root / spec_id
    received_path = directory / "especificacion-recibida.json"
    result_path = directory / "resultado.tsv"
    summary_path = directory / "resumen.json"
    launcher_path = directory / "analisis-reproducible.py"
    required_artifacts = (received_path, result_path, summary_path, launcher_path)
    if not all(path.is_file() for path in required_artifacts):
        raise ValueError(f"expediente de analista incompleto: {spec_id}")

    canonical = canonical_analyst_spec(full, snapshot_hash, baseline_hash, repo_root)
    Draft202012Validator(schema).validate(canonical)
    expected_spec_bytes = canonical_json_bytes(canonical)
    if received_path.read_bytes() != expected_spec_bytes:
        raise ValueError(f"especificación recibida difiere de maestra canónica: {spec_id}")
    received = json.loads(received_path.read_text(encoding="utf-8"))
    if FORBIDDEN.intersection(received):
        raise ValueError(f"input no cegado: {spec_id}")

    input_path = Path(full["input_path"])
    actual_micro_hash = sha256(input_path)
    if actual_micro_hash != full["hash_microdato"]:
        raise ValueError(f"hash de microdato incorrecto: {spec_id}")
    evidence_path = resolve_ref(repo_root, full["evidencia_neutral_ref"])
    if not evidence_path.is_file() or sha256(evidence_path) != full["hash_evidencia_neutral"]:
        raise ValueError(f"evidencia neutral ausente o alterada: {spec_id}")
    verify_neutral_evidence_sources(evidence_path)

    # La reproducción usa exclusivamente la maestra y el motor versionado. No
    # lee ni valida hashes.json del analista, incluso si éste lo vuelve a firmar.
    with tempfile.TemporaryDirectory(prefix=f"produccion-supervisor-{spec_id}-") as temp_name:
        temp_root = Path(temp_name)
        clean_spec = temp_root / "especificacion-recibida.json"
        clean_spec.write_bytes(expected_spec_bytes)
        reproduced = temp_root / "reproducido"
        execute(clean_spec, reproduced)
        for filename, analyst_path in (
            ("resultado.tsv", result_path),
            ("resumen.json", summary_path),
            ("analisis-reproducible.py", launcher_path),
        ):
            if analyst_path.read_bytes() != (reproduced / filename).read_bytes():
                raise ValueError(f"artefacto no coincide con reproducción supervisora: {spec_id}:{filename}")

    results = read_tsv(result_path)
    if sorted(row["variable"] for row in results) != sorted(full["variables"]):
        raise ValueError(f"filas esperadas faltantes o duplicadas: {spec_id}")
    if len({row["variable"] for row in results}) != len(results):
        raise ValueError(f"variable duplicada en resultado: {spec_id}")
    link = full["supervisor_link"]
    if link["relacion_id"] not in relations:
        raise ValueError(f"relación inexistente: {spec_id}")

    received_hash = sha256(received_path)
    design_text = stable_json(full["diseno_muestral"])
    for result in results:
        variable = result["variable"]
        exact_material = {
            "especificacion_id": full["especificacion_id"],
            "estimando": full["estimando"],
            "poblacion": full["poblacion"],
            "dominio": full["dominio"],
            "unidad": full["unidad_observacion"],
            "periodo": full["periodo_referencia_por_variable"][variable],
            "periodo_referencia": full["periodo_referencia_por_variable"][variable],
            "edicion": full["edicion"],
            "periodo_levantamiento": full["periodo_levantamiento"],
            "ponderacion_diseno": design_text,
            "transformacion": full["transformacion"],
            "tipo_inferencia": full["tipo_inferencia"],
            "input_path": full["input_path"],
            "input_member": full["input_member"],
            "hash_microdato": actual_micro_hash,
            "hash_especificacion_input": received_hash,
            "evidencia_ref": full["evidencia_ref"],
        }
        for field, expected in exact_material.items():
            if result.get(field) != expected:
                raise ValueError(f"campo material no enlaza maestra: {spec_id}:{variable}:{field}")
        _validate_inspection_link(result, inspection_reports)

    hashes = {
        "received": received_hash,
        "result": sha256(result_path),
        "summary": sha256(summary_path),
        "launcher": sha256(launcher_path),
        "microdata": actual_micro_hash,
        "evidence": sha256(evidence_path),
    }
    return results, hashes


def _derive_rows(
    config_path: Path,
    snapshot_path: Path,
    baseline_dir: Path,
    analyst_root: Path,
    repo_root: Path,
) -> list[dict[str, str]]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    snapshot_hash = json.loads(snapshot_path.read_text(encoding="utf-8"))["snapshot_t0_sha256"]
    baseline_hash = sha256(baseline_dir / "baseline.json")
    config_hash = sha256(config_path)
    relations = {row["relacion_id"] for row in read_tsv(baseline_dir / "relaciones.tsv")}
    inspection_reports: dict[str, list[dict[str, str]]] = {}
    report_path = baseline_dir.parent / "curacion-universo" / "reportes-inspeccion.tsv"
    for report in read_tsv(report_path):
        inspection_reports.setdefault(report["reporte_id"], []).append(report)
    schema_path = repo_root / "tools/curador_registro/schemas/production-spec.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    production_engine = repo_root / "tools/curador_registro/produce.py"
    integration_engine = repo_root / "tools/curador_registro/integrate_production.py"

    output: list[dict[str, str]] = []
    seen_specs: set[str] = set()
    for full in config["specifications"]:
        spec_id = full["especificacion_id"]
        if spec_id in seen_specs:
            raise ValueError(f"especificación duplicada: {spec_id}")
        seen_specs.add(spec_id)
        results, hashes = _verify_one(
            full, snapshot_hash, baseline_hash, analyst_root, repo_root, schema,
            relations, inspection_reports,
        )
        link = full["supervisor_link"]
        directory = analyst_root / spec_id
        for result in results:
            descriptive_state = (
                "CALCULO_DESCRIPTIVO_DISPONIBLE"
                if result["estado"] == "CALCULO_REPRODUCIBLE" else "NO_DETERMINADO"
            )
            if result["estado"] != "CALCULO_REPRODUCIBLE":
                model_state = "NO_LISTA_CALCULO_NO_DETERMINADO"
            elif link["requiere_decision"] == "NO":
                model_state = "LISTA_PARA_USO_MODELO"
            else:
                model_state = "NO_LISTA_DECISION_HUMANA_PENDIENTE"
            output.append({
                "produccion_id": stable_id("PROD-", spec_id, result["variable"]),
                "especificacion_id": spec_id,
                "relacion_id": link["relacion_id"],
                "objeto_modelo_origen": link["objeto_modelo_origen"],
                "tipo_producto": result["tipo_producto"],
                "estimando": f"{result['estimando']}:{result['variable']}",
                "estimacion": result["estimacion"],
                "incertidumbre": result["incertidumbre"],
                "poblacion": result["poblacion"],
                "dominio": result["dominio"],
                "unidad": result["unidad"],
                "periodo": result["periodo"],
                "periodo_referencia": result["periodo_referencia"],
                "edicion": result["edicion"],
                "periodo_levantamiento": result["periodo_levantamiento"],
                "n": result["n"],
                "suma_pesos": result["suma_pesos"],
                "ponderacion_diseno": result["ponderacion_diseno"],
                "transformacion": result["transformacion"],
                "tipo_inferencia": result["tipo_inferencia"],
                "input_path": result["input_path"],
                "input_member": result["input_member"],
                "hash_microdato": hashes["microdata"],
                "snapshot_t0_sha256": snapshot_hash,
                "snapshot_ref": artifact_ref(snapshot_path, repo_root),
                "hash_snapshot_archivo": sha256(snapshot_path),
                "baseline_ref": artifact_ref(baseline_dir / "baseline.json", repo_root),
                "baseline_sha256": baseline_hash,
                "especificacion_input_ref": artifact_ref(directory / "especificacion-recibida.json", repo_root),
                "hash_especificacion_input": hashes["received"],
                "especificacion_fuente_ref": artifact_ref(config_path, repo_root),
                "hash_especificacion_fuente": config_hash,
                "resultado_ref": artifact_ref(directory / "resultado.tsv", repo_root),
                "hash_resultado": hashes["result"],
                "resumen_ref": artifact_ref(directory / "resumen.json", repo_root),
                "hash_resumen": hashes["summary"],
                "script_ref": artifact_ref(directory / "analisis-reproducible.py", repo_root),
                "hash_script_reproducible": hashes["launcher"],
                "motor_produccion_ref": artifact_ref(production_engine, repo_root),
                "hash_motor_produccion": sha256(production_engine),
                "integrador_produccion_ref": artifact_ref(integration_engine, repo_root),
                "hash_integrador_produccion": sha256(integration_engine),
                "evidencia_neutral_ref": full["evidencia_neutral_ref"],
                "hash_evidencia_neutral": hashes["evidence"],
                "evidencia_ref": result["evidencia_ref"],
                "estado": result["estado"],
                "estado_calculo_descriptivo": descriptive_state,
                "estado_uso_modelo": model_state,
                "verificacion_supervisor": "REPRODUCIDA_EN_TEMP_Y_COMPARADA_BYTE_A_BYTE",
                "reserva": result["reserva"],
                "requiere_decision": link["requiere_decision"],
            })
    return output


def verify_production_bundle(
    config_path: Path,
    snapshot_path: Path,
    baseline_dir: Path,
    analyst_root: Path,
    production_table_path: Path | None = None,
    repo_root: Path | None = None,
) -> list[dict[str, str]]:
    """Independently reproduce a complete bundle and optionally its final TSV.

    This is the entry point intended for ``validate.py``. Every path is reread;
    analyst ``hashes.json`` files are deliberately ignored.
    """
    config_path = config_path.resolve()
    snapshot_path = snapshot_path.resolve()
    baseline_dir = baseline_dir.resolve()
    analyst_root = analyst_root.resolve()
    repo_root = repo_root.resolve() if repo_root else config_path.parents[2]
    snapshot_hash = json.loads(snapshot_path.read_text(encoding="utf-8"))["snapshot_t0_sha256"]
    # Acepta tanto el directorio de un run como la raíz versionada que lo
    # contiene. La selección es exacta por hash T0, nunca "el último" run.
    run_root = analyst_root / f"t0-{snapshot_hash[:16]}"
    if run_root.is_dir():
        analyst_root = run_root
    rows = _derive_rows(config_path, snapshot_path, baseline_dir, analyst_root, repo_root)
    expected = production_bytes(rows)
    if production_table_path is not None:
        production_table_path = production_table_path.resolve()
        if not production_table_path.is_file() or production_table_path.read_bytes() != expected:
            raise ValueError("produccion-modelo.tsv difiere de la reproducción supervisora")
        # Todos los *_ref del producto integrado deben resolver y su hash
        # asociado debe coincidir con los bytes actuales.
        ref_hash_pairs = {
            "especificacion_input_ref": "hash_especificacion_input",
            "especificacion_fuente_ref": "hash_especificacion_fuente",
            "resultado_ref": "hash_resultado",
            "resumen_ref": "hash_resumen",
            "script_ref": "hash_script_reproducible",
            "motor_produccion_ref": "hash_motor_produccion",
            "integrador_produccion_ref": "hash_integrador_produccion",
            "evidencia_neutral_ref": "hash_evidencia_neutral",
            "snapshot_ref": "hash_snapshot_archivo",
            "baseline_ref": "baseline_sha256",
        }
        for row in read_tsv(production_table_path):
            for ref_field, hash_field in ref_hash_pairs.items():
                path = resolve_ref(repo_root, row[ref_field])
                if not path.is_file() or sha256(path) != row[hash_field]:
                    raise ValueError(f"referencia/hash inválido: {row['produccion_id']}:{ref_field}")
    return rows


def integrate(
    config_path: Path,
    snapshot_path: Path,
    baseline_dir: Path,
    analyst_root: Path,
    output_path: Path,
) -> list[dict[str, str]]:
    rows = verify_production_bundle(config_path, snapshot_path, baseline_dir, analyst_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(production_bytes(rows))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--analyst-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-existing", action="store_true")
    args = parser.parse_args()
    if args.validate_existing:
        if args.output is None:
            parser.error("--validate-existing requiere --output")
        rows = verify_production_bundle(
            args.config, args.snapshot, args.baseline, args.analyst_root,
            production_table_path=args.output,
        )
    else:
        if args.output is None:
            parser.error("integración requiere --output")
        rows = integrate(args.config, args.snapshot, args.baseline, args.analyst_root, args.output)
    descriptive_relations = {
        row["relacion_id"] for row in rows
        if row["estado_calculo_descriptivo"] == "CALCULO_DESCRIPTIVO_DISPONIBLE"
    }
    model_ready_relations = {
        row["relacion_id"] for row in rows if row["estado_uso_modelo"] == "LISTA_PARA_USO_MODELO"
    }
    print(json.dumps({
        "ok": True,
        "productos": len(rows),
        "reproducibles": sum(row["estado"] == "CALCULO_REPRODUCIBLE" for row in rows),
        "no_determinado": sum(row["estado"] == "NO_DETERMINADO" for row in rows),
        "RELACIONES_CON_CALCULO_DESCRIPTIVO": len(descriptive_relations),
        "RELACIONES_LISTAS_PARA_USO_MODELO": len(model_ready_relations),
        "hashes_analista_confiados": False,
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
