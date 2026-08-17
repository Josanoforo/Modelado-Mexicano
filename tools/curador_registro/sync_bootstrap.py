#!/usr/bin/env python3
"""Sincroniza baseline, bootstrap y trabajo desde el registro vigente.

La recuperación opcional no interpreta semántica: únicamente repone filas de
``relaciones.tsv`` ya comprometidas por el SHA del baseline aceptado cuando
sus proyecciones de evidencia/utilidad sobrevivieron. Todo se valida en una
copia candidata antes del reemplazo y se conserva un journal de hashes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .baseline import ARCHIVOS_TSV, leer_tsv, relacion_id, sha256, validar_baseline
    from .bootstrap import build_bootstrap
    from .classify_work import classify
except ImportError:
    from baseline import ARCHIVOS_TSV, leer_tsv, relacion_id, sha256, validar_baseline
    from bootstrap import build_bootstrap
    from classify_work import classify


RELATION_FILE = "relaciones.tsv"
BASELINE_FILE = "baseline.json"
BOOTSTRAP_FILE = "bootstrap-semantico.tsv"
WORK_FILE = "trabajo-semantico.tsv"


def _digest_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _read_tsv_bytes(payload: bytes) -> tuple[list[str], list[dict[str, str]]]:
    text = payload.decode("utf-8-sig")
    reader = csv.DictReader(text.splitlines(), delimiter="\t")
    if not reader.fieldnames:
        raise ValueError("RECUPERACION_RELACIONES_SIN_CABECERA")
    return list(reader.fieldnames), list(reader)


def _write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _freeze_manifest(registry: Path, template: dict[str, Any]) -> dict[str, Any]:
    tables = {name: leer_tsv(registry / filename) for name, filename in ARCHIVOS_TSV.items()}
    relations = tables["relaciones"]
    decisions = tables["decisiones_humanas"]
    state_counts = Counter(row["clasificacion_relacion"] for row in relations)
    counts = {
        "relaciones_activas": len(relations),
        "procedencias_aceptadas": len(tables["evidencias"]),
        "artefactos_rechazados": len(tables["artefactos_rechazados"]),
        "decisiones_pendientes": sum(row.get("estado_decision") == "PENDIENTE" for row in decisions),
        "familias_alias": len(tables["aliases_fuentes"]),
        "fusiones_declaradas": len(tables["fusiones_relaciones"]),
        "confirmadas": state_counts["CONFIRMADA"],
        "negativas": state_counts["NEGATIVA"],
        "candidatas": state_counts["CANDIDATA"],
        "no_accesibles": state_counts["NO_ACCESIBLE"],
    }
    manifest = {**template, "conteos": counts, "archivos": {}}
    for filename in ARCHIVOS_TSV.values():
        manifest["archivos"][filename] = {
            "filas": len(leer_tsv(registry / filename)),
            "sha256": sha256(registry / filename),
        }
    (registry / BASELINE_FILE).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def _recover_missing_relations(
    candidate: Path,
    recovery_payload: bytes,
    expected_recovery_sha256: str,
) -> list[str]:
    current_fields, current_rows = _read_tsv_bytes((candidate / RELATION_FILE).read_bytes())
    current = {row["relacion_id"]: row for row in current_rows}
    if len(current) != len(current_rows):
        raise ValueError("RECUPERACION_RELACIONES_IDS_NO_UNICOS")
    evidence_ids = {row["relacion_id"] for row in leer_tsv(candidate / "evidencias.tsv")}
    utility_ids = {row["relacion_id"] for row in leer_tsv(candidate / "utilidad-modelo.tsv")}
    missing = sorted((evidence_ids & utility_ids) - set(current))
    if not missing:
        return []
    if _digest_bytes(recovery_payload) != expected_recovery_sha256:
        raise ValueError("RECUPERACION_RELACIONES_HASH_NO_COMPROMETIDO")
    recovery_fields, recovery_rows = _read_tsv_bytes(recovery_payload)
    if recovery_fields != current_fields:
        raise ValueError("RECUPERACION_RELACIONES_SCHEMA_DIVERGENTE")
    recovered = {row["relacion_id"]: row for row in recovery_rows}
    if len(recovered) != len(recovery_rows):
        raise ValueError("RECUPERACION_RELACIONES_IDS_NO_UNICOS")
    if any(identifier not in recovered for identifier in missing):
        raise ValueError("RECUPERACION_RELACION_SIN_FILA_COMPROMETIDA")
    if (evidence_ids - set(current)) != set(missing) or (utility_ids - set(current)) != set(missing):
        raise ValueError("RECUPERACION_PROYECCIONES_NO_COINCIDEN")
    for identifier in missing:
        row = recovered[identifier]
        if relacion_id(
            row["necesidad_id"], row["fuente_canonica_normalizada"],
            row["objeto_evidencia_id_canonico"],
        ) != identifier:
            raise ValueError(f"RECUPERACION_RELACION_ID_NO_DETERMINISTA:{identifier}")
        current[identifier] = row
    _write_tsv(candidate / RELATION_FILE, current_fields, [current[key] for key in sorted(current)])
    return missing


def _atomic_replace_many(outputs: dict[Path, bytes]) -> None:
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


def synchronize(
    registry: Path,
    mapping: Path,
    declarations: Path,
    universe: Path,
    asset_states: Path,
    rules: Path,
    recovery_payload: bytes,
    recovery_ref: str,
    journal_path: Path,
    *,
    apply: bool,
) -> dict[str, Any]:
    template = json.loads((registry / BASELINE_FILE).read_text(encoding="utf-8"))
    expected_recovery_sha = template["archivos"][RELATION_FILE]["sha256"]
    with tempfile.TemporaryDirectory(prefix=".bootstrap-sync-", dir=registry.parent) as temporary_name:
        candidate = Path(temporary_name) / "registry"
        candidate.mkdir()
        for filename in [*ARCHIVOS_TSV.values(), BASELINE_FILE]:
            shutil.copy2(registry / filename, candidate / filename)
        recovered_ids = _recover_missing_relations(
            candidate, recovery_payload, expected_recovery_sha
        )
        _freeze_manifest(candidate, template)
        validation = validar_baseline(candidate)
        if not validation["ok"]:
            raise ValueError("BASELINE_CANDIDATO_INVALIDO:" + ";".join(validation["errores"]))
        bootstrap_path = candidate / BOOTSTRAP_FILE
        build_bootstrap(candidate, mapping, declarations, universe, asset_states, bootstrap_path)
        work_path = candidate / WORK_FILE
        classify(bootstrap_path, candidate, rules, work_path)
        relation_ids = {row["relacion_id"] for row in leer_tsv(candidate / RELATION_FILE)}
        bootstrap_ids = {row["relacion_id"] for row in leer_tsv(bootstrap_path)}
        candidate_ids = {
            row["relacion_id"] for row in leer_tsv(candidate / RELATION_FILE)
            if row["clasificacion_relacion"] == "CANDIDATA"
        }
        work_ids = {row["relacion_id"] for row in leer_tsv(work_path)}
        if relation_ids != bootstrap_ids or candidate_ids != work_ids:
            raise ValueError("DERIVADOS_NO_CUBREN_REGISTRO_1A1")
        names = [RELATION_FILE, BASELINE_FILE, BOOTSTRAP_FILE, WORK_FILE]
        before = {
            name: _digest_bytes((registry / name).read_bytes())
            if (registry / name).exists() else "NO-EXISTE"
            for name in names
        }
        after = {name: _digest_bytes((candidate / name).read_bytes()) for name in names}
        changed = [name for name in names if before[name] != after[name]]
        result = {
            "ok": True,
            "apply": apply,
            "changed": changed,
            "recovered_relation_ids": recovered_ids,
            "relations": len(relation_ids),
            "bootstrap_rows": len(bootstrap_ids),
            "work_rows": len(work_ids),
            "before_sha256": before,
            "after_sha256": after,
            "recovery_ref": recovery_ref,
            "recovery_sha256": _digest_bytes(recovery_payload),
        }
        if apply and changed:
            outputs = {registry / name: (candidate / name).read_bytes() for name in names}
            _atomic_replace_many(outputs)
            journal_path.parent.mkdir(parents=True, exist_ok=True)
            journal_path.write_text(
                json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            final = validar_baseline(registry)
            if not final["ok"]:
                raise ValueError("BASELINE_POST_REEMPLAZO_INVALIDO")
        return result


def _git_payload(repo: Path, ref: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{ref}:{relative}"], cwd=repo,
        check=True, stdout=subprocess.PIPE,
    ).stdout


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--declarations", type=Path, required=True)
    parser.add_argument("--universe", type=Path, required=True)
    parser.add_argument("--asset-states", type=Path, required=True)
    parser.add_argument("--rules", type=Path, required=True)
    parser.add_argument("--recovery-ref", required=True)
    parser.add_argument("--journal", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    registry = args.registry.resolve()
    relative = str((registry / RELATION_FILE).relative_to(repo))
    if validar_baseline(registry)["ok"]:
        payload = (registry / RELATION_FILE).read_bytes()
        effective_recovery_ref = "NO-APLICA-BASELINE-YA-VALIDO"
    else:
        payload = _git_payload(repo, args.recovery_ref, relative)
        effective_recovery_ref = args.recovery_ref
    result = synchronize(
        registry, args.mapping.resolve(), args.declarations.resolve(),
        args.universe.resolve(), args.asset_states.resolve(), args.rules.resolve(),
        payload, effective_recovery_ref, args.journal.resolve(), apply=args.apply,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
