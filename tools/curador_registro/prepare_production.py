#!/usr/bin/env python3
"""Genera inputs opacos canónicos desde la especificación maestra.

La función :func:`canonical_analyst_spec` es también la fuente independiente
que usa el supervisor para reconstruir lo que el analista debió recibir.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from copy import deepcopy
from pathlib import Path
from typing import Any


FORBIDDEN = {
    "supervisor_link", "necesidad_id", "relacion_id", "objeto_modelo_origen",
    "decision_pendiente", "interpretacion_deseada", "signo_esperado",
    "resultado_favorable",
}
MASTER_REQUIRED = {
    "especificacion_id", "estimando", "poblacion", "dominio",
    "unidad_observacion", "variables", "codificacion", "faltantes",
    "direccion", "ponderador", "diseno_muestral", "transformacion",
    "incertidumbre", "tipo_inferencia", "criterio_parada",
    "periodo_referencia_por_variable", "edicion", "periodo_levantamiento",
    "input_path", "input_member", "hash_microdato", "evidencia_ref",
    "evidencia_neutral_ref", "hash_evidencia_neutral", "supervisor_link",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _repo_ref(repo_root: Path, ref: str) -> Path:
    path = Path(ref.split("#", 1)[0])
    return path if path.is_absolute() else repo_root / path


def validate_master_spec(full: dict[str, Any], repo_root: Path) -> None:
    missing = sorted(MASTER_REQUIRED - set(full))
    if missing:
        raise ValueError(f"especificación maestra incompleta {full.get('especificacion_id', '')}: {missing}")
    variables = full["variables"]
    if not variables or len(variables) != len(set(variables)):
        raise ValueError(f"variables vacías o duplicadas: {full['especificacion_id']}")
    if set(full["codificacion"]) != set(variables):
        raise ValueError(f"codificación no cubre exactamente variables: {full['especificacion_id']}")
    if set(full["periodo_referencia_por_variable"]) != set(variables):
        raise ValueError(f"periodo de referencia no está fijado por variable: {full['especificacion_id']}")
    for variable, categories in full["codificacion"].items():
        codes = [category.get("codigo") for category in categories]
        if not categories or len(codes) != len(set(codes)) or any(
            set(category) != {"codigo", "etiqueta"} or not category["etiqueta"]
            for category in categories
        ):
            raise ValueError(f"categorías inválidas: {full['especificacion_id']}:{variable}")
    input_path = Path(full["input_path"])
    if not input_path.is_file():
        raise ValueError(f"microdato no existe: {full['especificacion_id']}:{input_path}")
    actual_micro_hash = sha256(input_path)
    if actual_micro_hash != full["hash_microdato"]:
        raise ValueError(
            f"hash de microdato no coincide: {full['especificacion_id']}:"
            f"{full['hash_microdato']}:{actual_micro_hash}"
        )
    evidence_path = _repo_ref(repo_root, full["evidencia_neutral_ref"])
    if not evidence_path.is_file() or sha256(evidence_path) != full["hash_evidencia_neutral"]:
        raise ValueError(f"evidencia neutral ausente o alterada: {full['especificacion_id']}")
    link = full["supervisor_link"]
    if set(link) != {"relacion_id", "objeto_modelo_origen", "requiere_decision"}:
        raise ValueError(f"supervisor_link incompleto o ampliado: {full['especificacion_id']}")
    if link["requiere_decision"] not in {"SI", "NO"}:
        raise ValueError(f"requiere_decision inválido: {full['especificacion_id']}")


def canonical_analyst_spec(
    full: dict[str, Any], snapshot_hash: str, baseline_hash: str, repo_root: Path
) -> dict[str, Any]:
    """Return the exact blinded contract an analyst is authorized to receive."""
    validate_master_spec(full, repo_root)
    sanitized = {
        key: deepcopy(value) for key, value in full.items() if key not in FORBIDDEN
    }
    sanitized["snapshot_t0_sha256"] = snapshot_hash
    sanitized["baseline_sha256"] = baseline_hash
    if FORBIDDEN.intersection(sanitized):
        raise AssertionError("input de analista contiene contexto prohibido")
    return sanitized


def prepare(config_path: Path, snapshot_path: Path, baseline_dir: Path, output_root: Path) -> list[Path]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    snapshot_hash = json.loads(snapshot_path.read_text(encoding="utf-8"))["snapshot_t0_sha256"]
    baseline_hash = sha256(baseline_dir / "baseline.json")
    paths: list[Path] = []
    repo_root = config_path.parents[2]
    for full in config["specifications"]:
        sanitized = canonical_analyst_spec(full, snapshot_hash, baseline_hash, repo_root)
        directory = output_root / sanitized["especificacion_id"]
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "especificacion-recibida.json"
        path.write_bytes(canonical_json_bytes(sanitized))
        paths.append(path)
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    paths = prepare(args.config.resolve(), args.snapshot.resolve(), args.baseline.resolve(), args.output_root.resolve())
    print(json.dumps({"ok": True, "specifications": [str(path) for path in paths]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
