#!/usr/bin/env python3
"""Supervisor fail-closed para rondas multiagente de candidatas existentes."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from curador import CLASSES, FIELDS, is_real_source, read_tsv

WORKER_FIELDS = [
    "worker_id", "necesidad_id", "fuente_canonica", "objeto_evidencia_id",
    "estado_anterior", "estado_propuesto", "tipo_resultado", "evidencia_ref",
    "evidencia_localizador", "evidencia_explicita", "razon",
    "reserva_incertidumbre", "requiere_decision_humana", "siguiente_accion",
]
EVIDENCE_FIELDS = [
    "necesidad_id", "fuente_canonica", "objeto_evidencia_id", "tipo_evidencia",
    "evidencia_ref", "evidencia_localizador", "variable_reactivo_tabla",
    "texto_evidencia", "unidad_observacion", "periodo", "universo_muestra",
    "codificacion", "parte_necesidad_cubierta", "parte_necesidad_no_cubierta",
    "uso_potencial_modelo", "transformacion_requerida", "incertidumbre",
    "traza_revision", "siguiente_accion",
]
SUMMARY_FIELDS = [
    "fuentes_asignadas", "candidatas_asignadas", "candidatas_devuelta",
    "confirmadas_nuevas", "negativas_nuevas", "candidatas_intactas",
    "no_accesibles_nuevas", "conflictos", "decisiones_humanas",
    "referencias_verificadas", "bloqueos",
]
EXPECTED_HEAD = "a83f4575e5b370198256dcc5106dccf91094dc53"


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("necesidad_id", ""),
        row.get("fuente_id_canonico", row.get("fuente_canonica", "")),
        row.get("objeto_evidencia_id", ""),
    )


def resolve_reference(repo: Path, reference: str, locator: str) -> tuple[bool, str]:
    """Comprueba ruta MAIN local y que línea/localizador existan realmente."""
    match = re.fullmatch(r"MAIN:([^;]+?)(?::L(\d+))?", (reference or "").strip())
    if not match or not locator.strip():
        return False, "referencia o localizador ausente/no local"
    path = repo / match.group(1)
    if not path.is_file():
        return False, f"ruta inexistente: {path}"
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    line_no = int(match.group(2)) if match.group(2) else None
    if line_no and not (1 <= line_no <= len(lines)):
        return False, f"línea inexistente: L{line_no}"
    material = lines[line_no - 1] if line_no else "\n".join(lines)
    loc = locator.strip()
    if line_no and loc == f"L{line_no}":
        return True, material
    if loc not in material:
        return False, f"localizador no encontrado: {loc}"
    return True, material


def derive_summary(rows: list[dict[str, str]], sources: set[str], refs_ok: int) -> dict[str, int]:
    proposed = Counter(r["estado_propuesto"] for r in rows)
    changes = [r for r in rows if r["estado_propuesto"] != r["estado_anterior"]]
    return {
        "fuentes_asignadas": len(sources), "candidatas_asignadas": len(rows),
        "candidatas_devuelta": len(rows),
        "confirmadas_nuevas": sum(r["estado_propuesto"] == "CONFIRMADA" for r in changes),
        "negativas_nuevas": sum(r["estado_propuesto"] == "NEGATIVA" for r in changes),
        "candidatas_intactas": proposed["CANDIDATA"],
        "no_accesibles_nuevas": sum(r["estado_propuesto"] == "NO_ACCESIBLE" for r in changes),
        "conflictos": proposed["CONFLICTO_MATERIAL"],
        "decisiones_humanas": sum(r["requiere_decision_humana"].upper() == "SI" for r in rows),
        "referencias_verificadas": refs_ok,
        "bloqueos": sum(r["tipo_resultado"] in {"BLOQUEO", "NO_ACCESIBLE"} for r in rows),
    }


def validate_contract(
    baseline: list[dict[str, str]], assignments: list[dict[str, str]],
    worker_rows: dict[str, list[dict[str, str]]], repo: Path, head: str,
) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    baseline_by_key = {key(r): r for r in baseline}
    if len(baseline_by_key) != len(baseline):
        errors.append("baseline contiene claves duplicadas")
    candidates = {k: r for k, r in baseline_by_key.items() if r["clasificacion_relacion"] == "CANDIDATA"}
    candidate_sources = {r["fuente_id_canonico"] for r in candidates.values()}

    source_workers: dict[str, list[str]] = defaultdict(list)
    expected_workers: set[str] = set()
    for row in assignments:
        source_workers[row["fuente_id_canonico"]].append(row["worker_id"])
        expected_workers.add(row["worker_id"])
    assigned_sources = set(source_workers)
    for source in sorted(candidate_sources | assigned_sources):
        n = len(source_workers.get(source, []))
        if source in candidate_sources and n != 1:
            errors.append(f"fuente candidata debe tener exactamente un worker: {source} ({n})")
        if n > 1:
            errors.append(f"fuente dividida o duplicada: {source}")
    for source in sorted(assigned_sources - candidate_sources):
        errors.append(f"fuente sin candidatas asignada: {source}")

    received_workers = set(worker_rows)
    for worker in sorted(expected_workers - received_workers):
        errors.append(f"worker esperado ausente: {worker}")
    for worker in sorted(received_workers - expected_workers):
        errors.append(f"worker no enumerado: {worker}")

    seen: Counter[tuple[str, str, str]] = Counter()
    invalid_refs: list[str] = []
    protected_changes: list[str] = []
    for worker, rows in worker_rows.items():
        for row in rows:
            missing = [f for f in WORKER_FIELDS if f not in row]
            if missing:
                errors.append(f"{worker}: campos faltantes {','.join(missing)}")
                continue
            relation = key(row)
            seen[relation] += 1
            original = baseline_by_key.get(relation)
            if not original:
                errors.append(f"relación ajena al baseline: {relation}")
                continue
            if source_workers.get(row["fuente_canonica"], []) != [worker]:
                errors.append(f"fuente tocada por worker incorrecto: {worker} {row['fuente_canonica']}")
            if original["clasificacion_relacion"] != "CANDIDATA":
                protected_changes.append(str(relation))
                errors.append(f"estado protegido incluido/modificado: {relation}")
            if row["estado_anterior"] != "CANDIDATA" or row["estado_propuesto"] not in CLASSES:
                errors.append(f"transición inválida: {relation}")
            if row["estado_propuesto"] in {"CONFIRMADA", "NEGATIVA"}:
                valid, detail = resolve_reference(repo, row["evidencia_ref"], row["evidencia_localizador"])
                if not valid or not row["evidencia_explicita"].strip() or not row["razon"].strip():
                    invalid_refs.append(f"{relation}: {detail}")
                    errors.append(f"evidencia adjudicada no verificable: {relation}: {detail}")
    duplicate_keys = sorted(k for k, n in seen.items() if n > 1)
    missing_keys = sorted(set(candidates) - set(seen))
    new_keys = sorted(set(seen) - set(candidates))
    if duplicate_keys:
        errors.append(f"candidatas duplicadas/colisión: {len(duplicate_keys)}")
    if missing_keys:
        errors.append(f"candidatas faltantes: {len(missing_keys)}")
    if new_keys:
        errors.append(f"claves nuevas: {len(new_keys)}")
    if head != EXPECTED_HEAD:
        errors.append(f"HEAD no autoritativo: {head}")
    metrics = {
        "workers_esperados": len(expected_workers), "workers_recibidos": len(received_workers),
        "candidatas_asignadas": sum(1 for r in candidates.values() if r["fuente_id_canonico"] in assigned_sources),
        "candidatas_recibidas": sum(seen.values()), "fuentes_candidatas": len(candidate_sources),
        "fuentes_asignadas": len(assigned_sources), "claves_faltantes": len(missing_keys),
        "claves_duplicadas": len(duplicate_keys), "claves_nuevas": len(new_keys),
        "referencias_invalidas": len(invalid_refs),
        "estados_protegidos_modificados": len(protected_changes),
    }
    return errors, metrics


def integrate(args: argparse.Namespace) -> dict[str, object]:
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)
    baseline = read_tsv(args.baseline)
    rejected = read_tsv(args.rejected)
    assignments = read_tsv(args.assignments)
    worker_rows: dict[str, list[dict[str, str]]] = {}
    worker_evidence: dict[str, list[dict[str, str]]] = {}
    for worker_dir in args.worker_dirs:
        worker = worker_dir.name
        relations_path = worker_dir / f"{worker}-relaciones.tsv"
        evidence_path = worker_dir / f"{worker}-evidencia.tsv"
        if relations_path.exists():
            worker_rows[worker] = read_tsv(relations_path)
        if evidence_path.exists():
            worker_evidence[worker] = read_tsv(evidence_path)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.repo, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    errors, metrics = validate_contract(baseline, assignments, worker_rows, args.repo, head)

    by_key = {key(r): dict(r) for r in baseline}
    changes: list[dict[str, str]] = []
    all_evidence: list[dict[str, str]] = []
    summaries: dict[str, dict[str, int]] = {}
    source_by_worker: dict[str, set[str]] = defaultdict(set)
    for row in assignments:
        source_by_worker[row["worker_id"]].add(row["fuente_id_canonico"])
    for worker, rows in worker_rows.items():
        refs_ok = 0
        for row in rows:
            original = by_key.get(key(row))
            if not original or original["clasificacion_relacion"] != "CANDIDATA":
                continue
            if row["estado_propuesto"] != "CANDIDATA":
                if row["estado_propuesto"] in {"CONFIRMADA", "NEGATIVA"}:
                    valid, _ = resolve_reference(args.repo, row["evidencia_ref"], row["evidencia_localizador"])
                    refs_ok += int(valid)
                original["clasificacion_relacion"] = row["estado_propuesto"]
                original["reason_code"] = "CURADURIA_SEMANTICA_MULTI2"
                original["evidencia_ref"] = row["evidencia_ref"]
                original["evidencia_textual_breve"] = row["evidencia_explicita"][:500]
                original["nota"] = f"{row['razon']} | Reserva: {row['reserva_incertidumbre']} | Siguiente: {row['siguiente_accion']}"
                changes.append(row)
        all_evidence.extend(worker_evidence.get(worker, []))
        summaries[worker] = derive_summary(rows, source_by_worker[worker], refs_ok)
        summary_path = next((d / f"{worker}-resumen.json" for d in args.worker_dirs if d.name == worker), None)
        if summary_path and summary_path.exists():
            declared = json.loads(summary_path.read_text(encoding="utf-8"))
            for field in SUMMARY_FIELDS:
                if declared.get(field) != summaries[worker].get(field):
                    errors.append(f"resumen no deriva de TSV: {worker} {field}")

    integrated = list(by_key.values())
    baseline_keys, result_keys = {key(r) for r in baseline}, {key(r) for r in integrated}
    if baseline_keys != result_keys:
        errors.append("el conjunto de claves activas cambió")
    old_neg = {key(r) for r in baseline if r["clasificacion_relacion"] == "NEGATIVA"}
    new_neg = {key(r) for r in integrated if r["clasificacion_relacion"] == "NEGATIVA"}
    negativos_perdidos = len(old_neg - new_neg)
    if negativos_perdidos:
        errors.append(f"negativos perdidos: {negativos_perdidos}")
    counts0, counts1 = Counter(r["clasificacion_relacion"] for r in baseline), Counter(r["clasificacion_relacion"] for r in integrated)
    conflicts = [r for r in integrated if r["clasificacion_relacion"] == "CONFLICTO_MATERIAL"]
    human_rows = [r for rows in worker_rows.values() for r in rows if r.get("requiere_decision_humana", "").upper() == "SI"]
    noncanonical = sum(not is_real_source(r["fuente_id_canonico"], r["fuente_nombre"]) for r in integrated if r["clasificacion_relacion"] != "SIN_CANDIDATO")
    baseline_summary = {
        "relaciones_semanticas_activas": len(baseline), "artefactos_rechazados": len(rejected),
        "universo_contable": len(baseline) + len(rejected), "confirmadas": counts0["CONFIRMADA"],
        "negativas": counts0["NEGATIVA"], "candidatas": counts0["CANDIDATA"],
        "no_accesibles": counts0["NO_ACCESIBLE"], "conflictos_materiales": counts0["CONFLICTO_MATERIAL"],
        "decisiones_humanas": 0,
    }
    result_summary = {
        "relaciones_semanticas_activas": len(integrated), "artefactos_rechazados": len(rejected),
        "universo_contable": len(integrated) + len(rejected), "confirmadas": counts1["CONFIRMADA"],
        "negativas": counts1["NEGATIVA"], "candidatas": counts1["CANDIDATA"],
        "no_accesibles": counts1["NO_ACCESIBLE"], "conflictos_materiales": len(conflicts),
        "decisiones_humanas": len(human_rows),
    }
    validation = {
        "head": head, "execution_mode": args.execution_mode,
        "baseline": baseline_summary, "resultado": result_summary, **metrics,
        "negativos_perdidos": negativos_perdidos, "fuentes_no_canonicas": noncanonical,
        "narrowing_detectado": baseline_keys != result_keys,
        "errores_integracion": errors,
    }
    validation["ok"] = not errors and head == EXPECTED_HEAD and len(baseline) == 200 and len(rejected) == 111

    write_tsv(output / "registro-demanda-universo-curado.tsv", integrated, FIELDS)
    write_tsv(output / "evidencia-relaciones.tsv", all_evidence, EVIDENCE_FIELDS)
    write_tsv(output / "cambios-clasificacion.tsv", changes, WORKER_FIELDS)
    pending = [r for rows in worker_rows.values() for r in rows if r.get("estado_propuesto") in {"CANDIDATA", "NO_ACCESIBLE"}]
    write_tsv(output / "pendientes-siguiente-accion.tsv", pending, WORKER_FIELDS)
    write_tsv(output / "conflictos-materiales.tsv", conflicts, FIELDS)
    write_tsv(output / "decisiones-humanas.tsv", human_rows, WORKER_FIELDS)
    shutil.copy2(args.assignments, output / "asignacion-workers.tsv")
    for worker_dir in args.worker_dirs:
        for path in worker_dir.glob("worker-*-*"):
            shutil.copy2(path, output / path.name)
    (output / "validacion.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = ["# Reporte supervisor Multi2", "", f"- Integración aceptada: `{str(validation['ok']).lower()}`", f"- Modo: `{args.execution_mode}`", f"- Candidatas inspeccionadas: {metrics['candidatas_recibidas']}", f"- Cambios: {len(changes)}", f"- Candidatas restantes: {counts1['CANDIDATA']}", f"- Errores: {len(errors)}"]
    (output / "reporte-supervisor.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    (output / "diff-curador.patch").write_text("""Corrección fail-closed de multi_supervisor.py:
- workers recibidos deben coincidir exactamente con asignación;
- cada fuente candidata se asigna exactamente una vez;
- cada candidata aparece exactamente una vez y ninguna clave nueva/protegida entra;
- solo CANDIDATA es modificable;
- CONFIRMADA/NEGATIVA nueva exige referencia MAIN existente y localizador presente;
- claves activas, negativos, resúmenes y conteos se reconcilian antes de ok=true.
""", encoding="utf-8")
    sums = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file() and p.name != "SHA256SUMS.json"}
    (output / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, required=True)
    parser.add_argument("--rejected", type=Path, required=True)
    parser.add_argument("--assignments", type=Path, required=True)
    parser.add_argument("--worker-dirs", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--execution-mode", choices=["parallel_subagents", "sequential_workers"], required=True)
    args = parser.parse_args()
    validation = integrate(args)
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0 if validation["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
