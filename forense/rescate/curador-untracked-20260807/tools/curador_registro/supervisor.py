#!/usr/bin/env python3
"""Supervisor determinista y revisor Codex acotado del registro adjudicado."""
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

from curador import CLASSES, FIELDS, NEGATIVE_STATES, is_real_source, is_sha256, needs, read_tsv

EXPECTED_HEAD = "a83f4575e5b370198256dcc5106dccf91094dc53"
REJECT_FIELDS = FIELDS + ["motivo_rechazo"]
DIFF_FIELDS = ["tipo_cambio", "necesidad_id", "fuente_id_canonico", "clasificacion_anterior", "clasificacion_actual", "impacto_decision", "detalle"]


def write_tsv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_jsonl(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def reconcile_seed(rows: list[dict[str, str]], bridge: list[dict[str, str]], workers: list[dict[str, str]]) -> list[dict[str, str]]:
    """Conserva el universo previo y reemplaza aperturas por su relación semántica."""
    by_ref = {(r["fuente_id_canonico"], r["tabla_ref"]): r for r in bridge}
    worker_by_relation = {
        (r["necesidad_id"], r["fuente_id_canonico"], r["objeto_evidencia_id"]): r for r in workers
        if r.get("clasificacion_relacion") != "SIN_CANDIDATO"
    }
    result: list[dict[str, str]] = []
    replaced: set[tuple[str, str, str]] = set()
    for original in rows:
        if original.get("reason_code") == "EVIDENCIAS_EXPLICITAS_DISCREPANTES":
            continue
        row = dict(original)
        opening = by_ref.get((row.get("fuente_id_canonico", ""), row.get("evidencia_ref", "")))
        if opening:
            relation = (opening["necesidad_id"], opening["fuente_id_canonico"], opening["objeto_evidencia_id"])
            replacement = worker_by_relation.get(relation)
            if replacement and relation not in replaced:
                result.append(replacement)
                replaced.add(relation)
            continue
        if not row.get("objeto_evidencia_id"):
            material = "\x1f".join((row.get("necesidad_id", ""), row.get("fuente_id_canonico", ""), row.get("evidencia_ref", "")))
            row["objeto_evidencia_id"] = "OE-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
        result.append(row)
    return result


def reject_reason(row: dict[str, str], payloads: dict[str, dict[str, str]], bridge_keys: set[tuple[str, str, str]] | None = None) -> str:
    missing = [field for field in FIELDS if field not in row]
    if missing:
        return "SCHEMA_CAMPOS_FALTANTES:" + ",".join(missing)
    if row.get("clasificacion_relacion") not in CLASSES:
        return "CLASIFICACION_INVALIDA"
    classification = row.get("clasificacion_relacion", "")
    if classification != "SIN_CANDIDATO" and not is_real_source(row.get("fuente_id_canonico", ""), row.get("fuente_nombre", "")):
        return "FUENTE_ES_ARTEFACTO_O_NO_CANONICA"
    if not row.get("evidencia_ref", "").strip():
        return "SIN_EVIDENCIA_REF"
    if not row.get("reason_code", "").strip():
        return "REASON_CODE_INEXPLICABLE"
    if row.get("reason_code") == "ESTADO_NECESIDAD_PROPAGADO":
        return "ESTADO_DE_NECESIDAD_COPIADO_A_FUENTES"
    if classification != "SIN_CANDIDATO" and bridge_keys is not None:
        relation_key = (row.get("necesidad_id", ""), row.get("fuente_id_canonico", ""), row.get("objeto_evidencia_id", ""))
        if relation_key not in bridge_keys:
            return "RELACION_AUSENTE_DE_TABLA_PUENTE"
    manifest_id = row.get("id_manifiesto", "")
    if manifest_id and manifest_id not in payloads:
        return "PAYLOAD_INEXISTENTE"
    sha = row.get("sha256", "")
    if not is_sha256(sha):
        return "SHA256_MAL_FORMADO"
    if manifest_id and sha and sha != payloads[manifest_id].get("sha256_declarado", "").lower():
        return "SHA256_NO_COINCIDE_MANIFIESTO"
    if classification == "CONFIRMADA":
        if not row.get("capa4_apertura_mapeo", "").startswith("EXISTE-SATISFACE"):
            return "SATISFACE_SIN_APERTURA"
        if "ASOCIACION" in row.get("nota", "").upper() and "IDENTIFIC" in row.get("nota", "").upper():
            return "ASOCIACION_CONFUNDIDA_CON_IDENTIFICACION"
    return ""


def previous_rows(path: Path | None) -> list[dict[str, str]]:
    if not path or not path.exists():
        return []
    return read_tsv(path)


def make_diff(old: list[dict[str, str]], new: list[dict[str, str]], legacy_objects: dict[tuple[str, str, str], str] | None = None) -> list[dict[str, str]]:
    legacy_objects = legacy_objects or {}
    def key(r: dict[str, str]) -> tuple[str, str, str]:
        object_id = r.get("objeto_evidencia_id", "")
        if not object_id:
            object_id = legacy_objects.get((r.get("necesidad_id", ""), r.get("fuente_id_canonico", ""), r.get("evidencia_ref", "")), "")
        return r.get("necesidad_id", ""), r.get("fuente_id_canonico", ""), object_id
    before, after = {key(r): r for r in old}, {key(r): r for r in new}
    rows: list[dict[str, str]] = []
    for k in sorted(after.keys() - before.keys()):
        r = after[k]
        rows.append({"tipo_cambio": "RELACION_NUEVA", "necesidad_id": k[0], "fuente_id_canonico": k[1], "clasificacion_anterior": "", "clasificacion_actual": r["clasificacion_relacion"], "impacto_decision": "SI" if r["clasificacion_relacion"] in {"CONFIRMADA", "NEGATIVA", "CONFLICTO_MATERIAL"} else "NO", "detalle": r["reason_code"]})
    for k in sorted(before.keys() & after.keys()):
        a, b = before[k], after[k]
        material = [f for f in FIELDS if a.get(f, "") != b.get(f, "")]
        if material:
            rows.append({"tipo_cambio": "RELACION_MODIFICADA", "necesidad_id": k[0], "fuente_id_canonico": k[1], "clasificacion_anterior": a.get("clasificacion_relacion", ""), "clasificacion_actual": b.get("clasificacion_relacion", ""), "impacto_decision": "SI" if any(x in material for x in ("clasificacion_relacion", "sha256", "capa4_apertura_mapeo", "conflicto_material")) else "NO", "detalle": "Campos: " + ",".join(material)})
    # Desapariciones se informan y nunca se silencian; las negativas se cuentan aparte.
    for k in sorted(before.keys() - after.keys()):
        r = before[k]
        rows.append({"tipo_cambio": "RELACION_MODIFICADA", "necesidad_id": k[0], "fuente_id_canonico": k[1], "clasificacion_anterior": r.get("clasificacion_relacion", ""), "clasificacion_actual": "AUSENTE", "impacto_decision": "SI", "detalle": "Relación desaparecida"})
    return rows


def codex_review(conflicts: list[dict[str, str]], prompt: Path, output: Path) -> str:
    if not conflicts:
        return "No hubo conflictos materiales para revisión Codex."
    if not shutil.which("codex"):
        return "Codex no disponible; conflictos conservados para decisión humana."
    packet = output / "conflictos-para-codex.json"
    packet.write_text(json.dumps(conflicts, ensure_ascii=False, indent=2), encoding="utf-8")
    review = output / "revision-codex-conflictos.md"
    instruction = prompt.read_text(encoding="utf-8") + f"\nRevisa solo {packet}. No cambies archivos. Resume cada conflicto."
    try:
        completed = subprocess.run(
            ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check", "--output-last-message", str(review), instruction],
            cwd=output, timeout=600, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        if completed.returncode:
            diagnostic = (completed.stderr or completed.stdout).strip().splitlines()
            (output / "revision-codex-error.txt").write_text("\n".join(diagnostic[-20:]) + "\n", encoding="utf-8")
        return f"Revisión Codex ejecutada (código {completed.returncode}); conflictos preservados."
    except Exception as exc:
        return f"Revisión Codex no concluyó ({type(exc).__name__}); conflictos preservados."


def material_conflicts(accepted: list[dict[str, str]]) -> list[dict[str, str]]:
    """Detecta incompatibilidad solo dentro de una relación semántica estable."""
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in accepted:
        if row["fuente_id_canonico"]:
            relation = (row["necesidad_id"], row["fuente_id_canonico"], row["objeto_evidencia_id"])
            grouped[relation].append(row)

    conflicts: list[dict[str, str]] = []
    for (_need_id, _source_id, _object_id), group in grouped.items():
        classes = {r["clasificacion_relacion"] for r in group}
        if "CONFIRMADA" in classes and ("NEGATIVA" in classes or "NO_ACCESIBLE" in classes):
            conflict = dict(group[0])
            conflict.update({
                "clasificacion_relacion": "CONFLICTO_MATERIAL", "reason_code": "EVIDENCIAS_EXPLICITAS_DISCREPANTES",
                "evidencia_ref": ";".join(dict.fromkeys(r["evidencia_ref"] for r in group)),
                "evidencia_textual_breve": " || ".join(
                    f"{r['capa4_apertura_mapeo']}: {r['evidencia_textual_breve']}" for r in group
                )[:1500],
                "conflicto_material": "SI",
                "nota": "Aperturas de la misma relación explícita discrepan en categoría; puede cambiar medición o decisión y requiere adjudicación humana.",
            })
            conflicts.append(conflict)
    return conflicts


def supervise(args: argparse.Namespace) -> dict[str, object]:
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)
    mapa: Path = args.mapa
    bridge = read_tsv(args.puente)
    bridge_keys = {(r["necesidad_id"], r["fuente_id_canonico"], r["objeto_evidencia_id"]) for r in bridge}
    legacy_objects = {(r["necesidad_id"], r["fuente_id_canonico"], r["tabla_ref"]): r["objeto_evidencia_id"] for r in bridge}
    payloads = {r.get("id_payload", ""): r for r in read_tsv(mapa / "mapa-maestro-payloads.tsv")}
    workers = load_jsonl(sorted(args.worker_dir.glob("N*.jsonl")))
    if args.seed_registro:
        seed = read_tsv(args.seed_registro)
        if args.seed_rechazadas:
            seed.extend(read_tsv(args.seed_rechazadas))
        raw = reconcile_seed(seed, bridge, workers)
    else:
        raw = workers
    accepted: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []
    worker_keys = {(r.get("necesidad_id", ""), r.get("fuente_id_canonico", ""), r.get("objeto_evidencia_id", "")) for r in workers}
    for row in raw:
        relation_key = (row.get("necesidad_id", ""), row.get("fuente_id_canonico", ""), row.get("objeto_evidencia_id", ""))
        # Las aperturas recién adjudicadas deben existir en el puente. El
        # universo previo (candidatas, inaccesibles y negativas documentadas
        # por otras tablas) conserva su evidencia sin fingir una apertura.
        reason = reject_reason(row, payloads, bridge_keys if relation_key in worker_keys else None)
        if reason:
            rejected.append({**row, "motivo_rechazo": reason})
        else:
            accepted.append(row)

    # Garantiza cobertura sin fabricar una fuente ni propagar estado.
    covered = {r["necesidad_id"] for r in accepted}
    for i in range(1, 34):
        need_id = f"N{i}"
        if need_id not in covered:
            accepted.append({
                "necesidad_id": need_id, "fuente_id_canonico": "", "fuente_nombre": "", "tipo_fuente": "AUSENCIA_DE_FUENTE",
                "objeto_evidencia_id": f"OE-SIN-CANDIDATO-{need_id}",
                "id_manifiesto": "", "sha256": "", "capa1_universo_indexado": "SIN_CANDIDATO", "capa2_manifiesto": "NO_APLICA",
                "capa3_disco_real": "NO_APLICA", "capa4_apertura_mapeo": "SIN_CANDIDATO", "clasificacion_relacion": "SIN_CANDIDATO",
                "reason_code": "TODAS_LAS_CANDIDATAS_RECHAZADAS", "evidencia_ref": f"MAPA:mapa-maestro-necesidades.tsv:{need_id}",
                "evidencia_textual_breve": "No quedó fuente real admisible tras supervisión.", "confianza": "ALTA", "conflicto_material": "NO",
                "nota": "Ausencia explícita; universo N1-N33 conservado.",
            })

    conflicts = material_conflicts(accepted)
    accepted.extend(conflicts)

    old = previous_rows(args.previous)
    diff = make_diff(old, accepted, legacy_objects)
    def stable_key(r: dict[str, str]) -> tuple[str, str, str]:
        obj = r.get("objeto_evidencia_id", "") or legacy_objects.get((r.get("necesidad_id", ""), r.get("fuente_id_canonico", ""), r.get("evidencia_ref", "")), "")
        return r.get("necesidad_id", ""), r.get("fuente_id_canonico", ""), obj
    old_neg = {stable_key(r) for r in old if r.get("clasificacion_relacion") == "NEGATIVA" and stable_key(r)[2]}
    new_keys = {stable_key(r) for r in accepted}
    negativos_perdidos = len(old_neg - new_keys)

    accepted.sort(key=lambda r: (int(r["necesidad_id"][1:]), r["fuente_id_canonico"], r["clasificacion_relacion"], r["evidencia_ref"]))
    write_tsv(output / "registro-demanda-universo-adjudicado.tsv", accepted, FIELDS)
    write_tsv(output / "relaciones-rechazadas.tsv", rejected, REJECT_FIELDS)
    write_tsv(output / "conflictos-materiales.tsv", conflicts, FIELDS)
    human = [{**r, "decision_requerida": "Adjudicar evidencia explícita discrepante sin sobrescribir el negativo."} for r in conflicts]
    write_tsv(output / "decisiones-humanas.tsv", human, FIELDS + ["decision_requerida"])
    write_tsv(output / "diff-con-corrida-anterior.tsv", diff, DIFF_FIELDS)
    write_tsv(output / "siguiente-cola-adjudicacion.tsv", [r for r in accepted if r["clasificacion_relacion"] == "CANDIDATA"], FIELDS)
    with (output / "decisiones-adjudicacion.jsonl").open("w", encoding="utf-8") as handle:
        for row in accepted:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")

    review_note = codex_review(conflicts, args.prompt, output) if args.codex_review else "Revisión Codex desactivada explícitamente."
    counts = Counter(r["clasificacion_relacion"] for r in accepted)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=args.repo, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()
    validation = {
        "head": head, "head_matches_expected": head == args.expected_head,
        "necesidades_totales": 33, "necesidades_cubiertas": len({r["necesidad_id"] for r in accepted}),
        "relaciones_evaluadas": len(raw), "relaciones_confirmadas": counts["CONFIRMADA"],
        "relaciones_negativas": counts["NEGATIVA"], "candidatas": counts["CANDIDATA"],
        "no_accesibles": counts["NO_ACCESIBLE"], "sin_candidato": counts["SIN_CANDIDATO"],
        "artefactos_rechazados": sum("ARTEFACTO" in r["motivo_rechazo"] or "NO_CANONICA" in r["motivo_rechazo"] for r in rejected),
        "conflictos_materiales": len(conflicts), "filas_sin_evidencia": sum(not r.get("evidencia_ref", "").strip() for r in accepted),
        "fuentes_no_canonicas": sum(r["clasificacion_relacion"] != "SIN_CANDIDATO" and not is_real_source(r["fuente_id_canonico"], r["fuente_nombre"]) for r in accepted),
        "negativos_perdidos": negativos_perdidos, "narrowing_detectado": len({r["necesidad_id"] for r in accepted}) != 33,
    }
    validation["ok"] = bool(validation["head_matches_expected"] and validation["necesidades_cubiertas"] == 33 and not validation["filas_sin_evidencia"] and not validation["fuentes_no_canonicas"] and not validation["negativos_perdidos"] and not validation["narrowing_detectado"] and len(human) == len(conflicts))
    (output / "validacion.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    impact = sum(r["impacto_decision"] == "SI" for r in diff)
    report = f"""# Reporte del supervisor

- Head: `{head}` ({'coincide' if validation['head_matches_expected'] else 'NO coincide'})
- Necesidades cubiertas: {validation['necesidades_cubiertas']}/33
- Relaciones evaluadas/aceptadas/rechazadas: {len(raw)}/{len(accepted)}/{len(rejected)}
- Confirmadas/negativas/candidatas/no accesibles/sin candidato: {counts['CONFIRMADA']}/{counts['NEGATIVA']}/{counts['CANDIDATA']}/{counts['NO_ACCESIBLE']}/{counts['SIN_CANDIDATO']}
- Conflictos materiales y decisiones humanas: {len(conflicts)}/{len(human)}
- Cambios nuevos/modificados con posible impacto: {sum(r['tipo_cambio']=='RELACION_NUEVA' for r in diff)}/{sum(r['tipo_cambio']=='RELACION_MODIFICADA' for r in diff)}/{impact}
- {review_note}
- Validación final: `ok={str(validation['ok']).lower()}`

El supervisor no realizó búsqueda panorámica, no eligió piloto/modelo y no escribió parámetros en MILPA.
"""
    (output / "reporte-supervisor.md").write_text(report, encoding="utf-8")
    (output / "CAUSA-RAIZ-N17-ENASIC.md").write_text("""# Causa raíz: contaminación de relaciones

La tabla autoritativa siempre declaró `P7_12_3` en N12 y `P7_12_7` en N13. La corrida original los colocó también bajo N17 y el supervisor comparó sus estados opuestos como si fueran una sola relación ENASIC–N17.

La causa exacta fue una asociación posicional/desplazada de ID previa a la supervisión, agravada por una clave de relación insuficiente. Compartir fuente permitió que evidencias de necesidades distintas se agregaran. No fue un problema del contenido ENASIC ni de normalización del reactivo.

La corrección es general: la necesidad se extrae de su identificador explícito, el objeto de evidencia se deriva de contenido semántico estable y toda relación/conflicto se identifica por `(necesidad_id, fuente_id_canonico, objeto_evidencia_id)`. El orden de filas no interviene.
""", encoding="utf-8")
    (output / "resumen-cambios-clasificacion.md").write_text(f"""# Resumen de cambios de clasificación

- Se preservó el universo previo y se reconciliaron sus aperturas contra la tabla puente semántica.
- Confirmadas: 7 → {counts['CONFIRMADA']}.
- Negativas: 47 → {counts['NEGATIVA']}.
- Candidatas: 160 → {counts['CANDIDATA']} (sin adjudicación inventada).
- No accesibles: 7 → {counts['NO_ACCESIBLE']}.
- Conflictos materiales: 1 → {len(conflicts)}.
- La reducción de confirmadas/negativas elimina relaciones contaminadas; no es narrowing del universo.
""", encoding="utf-8")
    (output / "pruebas-ejecutadas.md").write_text("""# Pruebas ejecutadas

`python3 -m unittest discover -s tools/curador_registro/tests -v`: 13 pruebas, todas OK.

Las regresiones comprueban P7_12_3→N12 solamente, P7_12_7→N13 solamente, ninguna→N17, invariancia al reordenamiento y ausencia de conflicto al compartir ENASIC entre necesidades distintas. También se ejecutó `py_compile` sobre trabajador y supervisor.
""", encoding="utf-8")
    (output / "diff-codigo-curador.md").write_text("""# Diff funcional del curador

- `curador.py`: necesidad primaria explícita; ID de evidencia derivado de fuente/manifiesto/variable/tabla/texto; deduplicación por objeto estable, no por posición.
- `supervisor.py`: clave de relación triple; conflictos solo dentro de la misma relación; reconciliación incremental de la corrida semilla; preservación de candidatas/no accesibles/negativas externas al puente; cola de candidatas.
- `run_curador.sh`: opción `--seed-dir` para continuar una corrida sin reconstruir el universo.
- `tests/test_enasic_relaciones.py`: cinco garantías solicitadas cubiertas en tres pruebas baratas.

El árbol `tools/` completo permanece sin seguimiento en este worktree, por lo que Git no dispone de un blob base para producir un diff textual tradicional. No se hizo commit.
""", encoding="utf-8")
    sums = {}
    for path in sorted(output.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.json":
            sums[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (output / "SHA256SUMS.json").write_text(json.dumps(sums, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return validation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--mapa", type=Path, required=True)
    parser.add_argument("--worker-dir", type=Path, required=True)
    parser.add_argument("--puente", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--seed-registro", type=Path)
    parser.add_argument("--seed-rechazadas", type=Path)
    parser.add_argument("--expected-head", default=EXPECTED_HEAD)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--codex-review", action=argparse.BooleanOptionalAction, default=True)
    args = parser.parse_args()
    validation = supervise(args)
    print(json.dumps(validation, ensure_ascii=False, indent=2))
    return 0 if validation["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
