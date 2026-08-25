#!/usr/bin/env python3
"""Deriva un universo candidato del marco ADV1 desde evidencia E2 concreta.

La entrada es ``data/manifiesto.yaml`` completa. Cada entrada se enlaza por
``id_manifiesto`` al censo y, desde ``reporte_neutral_ref``, por ``batch_id``
al reporte E2 neutral. ``objetos_logicos`` es solo un conteo de control.

Una fila se emite únicamente si encuesta, ola, universo, variable,
estimador, ponderador y escala están resueltos con evidencia estructurada. Los
registros N1–N33 pueden enriquecer una observación E2 ya existente, pero nunca
son puerta de entrada ni crean candidatas por sí mismos.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import yaml


MARCO_FIELDS = (
    "id", "encuesta", "ola", "universo", "variable", "estimador",
    "ponderador", "escala", "grado_dependencia", "publicada", "cv_arbitro",
    "n_no_ponderado", "frase_discriminacion", "post_corte_u_ola_retenida",
    "dominio", "dificultad", "estrato", "origen_manifiesto_id",
)

SEED_TYPES = {
    "VARIABLE-DTA", "VARIABLE-SAV", "VARIABLE-DICCIONARIO",
    "VARIABLE-DICCIONARIO-XLS", "VARIABLE-DICCIONARIO-XLSX",
}
INSUFFICIENT = "OBSERVACION_INSUFICIENTE"
PENDING = "PENDIENTE-FILTRO"
UNKNOWN = {"", "NO-DETERMINADO", "NO_DETERMINADO", "[REDACTADO-PRIVACIDAD]"}
HEX64 = re.compile(r"^[0-9a-f]{64}$", re.I)
LOCATOR_VARIABLE = re.compile(r"(?:^|[#:/])variable=([^#!:/]*)", re.I)

ALIASES = {
    "survey": "encuesta", "wave": "ola", "population": "universo",
    "variable_code": "variable", "codigo_variable": "variable",
    "variable_type": "tipo_variable", "weight": "ponderador",
    "weight_exact": "ponderador_exacto", "categories": "categorias",
    "coding": "codificacion", "range": "rango", "unit": "unidad",
    "missing_values": "missing", "published": "publicada",
    "dependency_grade": "grado_dependencia", "unweighted_n": "n_no_ponderado",
}


class MarcoError(ValueError):
    pass


@dataclass(frozen=True)
class GenerationResult:
    rows: tuple[dict[str, str], ...]
    insufficient: tuple[dict[str, str], ...]
    conflicts: tuple[dict[str, str], ...]
    summary: dict[str, int]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise MarcoError(f"TSV_SIN_CABECERA:{path}")
        return [{str(key): str(value or "") for key, value in row.items()} for row in reader]


def read_manifest(path: Path) -> list[dict[str, str]]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise MarcoError("MANIFIESTO_NO_ES_LISTA")
    result: list[dict[str, str]] = []
    for raw in payload:
        if not isinstance(raw, dict):
            continue
        result.append({str(key): _scalar(value) for key, value in raw.items()})
    return result


def _scalar(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value).strip()


def _meaningful(value: Any) -> bool:
    return _scalar(value).strip().upper() not in UNKNOWN


def _canonical_record(record: dict[str, str]) -> dict[str, str]:
    canonical: dict[str, str] = {}
    for raw_key, raw_value in record.items():
        key = ALIASES.get(raw_key.strip(), raw_key.strip())
        value = _scalar(raw_value)
        if _meaningful(value):
            canonical[key] = value
    description = canonical.get("descripcion_neutral", "").strip()
    if description.startswith("{"):
        try:
            embedded = json.loads(description)
        except json.JSONDecodeError:
            embedded = None
        if isinstance(embedded, dict):
            for raw_key, raw_value in embedded.items():
                key = ALIASES.get(str(raw_key), str(raw_key))
                value = _scalar(raw_value)
                if _meaningful(value):
                    canonical.setdefault(key, value)
    return canonical


def _index_unique(rows: Iterable[dict[str, str]], field: str, label: str) -> dict[str, dict[str, str]]:
    index: dict[str, dict[str, str]] = {}
    duplicates: set[str] = set()
    for row in rows:
        key = row.get(field, "").strip()
        if not key:
            continue
        if key in index:
            duplicates.add(key)
        else:
            index[key] = row
    if duplicates:
        raise MarcoError(f"{label}_ID_DUPLICADO:{','.join(sorted(duplicates))}")
    return index


def _evidence_matches(observation: dict[str, str], evidence: dict[str, str]) -> bool:
    for key in ("record_id", "objeto_logico_id", "union_evidencia_id"):
        if _meaningful(observation.get(key)) and observation.get(key) == evidence.get(key):
            return True
    if (
        _meaningful(observation.get("id_manifiesto"))
        and observation.get("id_manifiesto") == evidence.get("id_manifiesto")
    ):
        return True
    left_variable = observation.get("variable") or _variable_from_locator(observation.get("localizador", ""))
    right_variable = evidence.get("variable") or _variable_from_locator(evidence.get("localizador", ""))
    same_source = any(
        _meaningful(observation.get(key)) and observation.get(key) == evidence.get(key)
        for key in ("batch_id", "payload_id")
    )
    return bool(same_source and _real_variable(left_variable) and left_variable == right_variable)


def _resolve(records: Iterable[dict[str, str]], field: str) -> tuple[str | None, tuple[str, ...]]:
    values = sorted({_canonical_record(record).get(field, "").strip() for record in records if _meaningful(_canonical_record(record).get(field, ""))})
    if len(values) == 1:
        return values[0], ()
    if len(values) > 1:
        return None, tuple(values)
    return None, ()


def _variable_from_locator(locator: str) -> str | None:
    match = LOCATOR_VARIABLE.search(locator or "")
    return match.group(1).strip() if match and match.group(1).strip() else None


def _real_variable(code: str | None) -> bool:
    if not code:
        return False
    normalized = code.strip()
    return bool(
        normalized
        and not normalized.upper().startswith("OBJ-B2-")
        and not HEX64.fullmatch(normalized)
        and not normalized.isdigit()
        and any(character.isalpha() for character in normalized)
    )


def _seed_variable(observation: dict[str, str]) -> str | None:
    record = _canonical_record(observation)
    kind = record.get("objeto_tipo", record.get("type", "")).upper()
    variable = record.get("variable") or _variable_from_locator(record.get("localizador", ""))
    if not _real_variable(variable):
        return None
    if kind in SEED_TYPES or kind.startswith("VARIABLE-"):
        return variable
    if kind == "COLUMNA" and record.get("codigo_documentado", "").upper() == "SI":
        return variable
    if kind == "REACTIVO-PDF" and record.get("union_reactivo_variable", "").upper() == "SI":
        return variable
    return None


def _normal_type(value: str | None) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", (value or "").strip().upper()).strip("_")


def _derive_estimator(records: list[dict[str, str]]) -> tuple[str | None, str | None]:
    raw_type, conflict = _resolve(records, "tipo_variable")
    if conflict:
        return None, "TIPO_VARIABLE_CONFLICTIVO"
    kind = _normal_type(raw_type)
    if kind in {"BINARIA", "BINARIO", "BINARY"}:
        return "PROPORCION_PONDERADA", None
    if kind in {"CATEGORICA", "CATEGORICA_EXCLUYENTE", "CATEGORICAL"}:
        exclusive, _ = _resolve(records, "categorias_excluyentes")
        if (exclusive or "").upper() != "SI":
            return None, "CATEGORIAS_NO_DOCUMENTADAS_COMO_EXCLUYENTES"
        return "DISTRIBUCION_PONDERADA", None
    if kind in {"NUMERICA_CONTINUA", "CONTINUA", "CONTINUOUS"}:
        unit, _ = _resolve(records, "unidad")
        if not unit:
            return None, "NUMERICA_SIN_UNIDAD"
        return "MEDIA_PONDERADA", None
    if kind in {"ADMINISTRATIVA", "CENSAL", "ADMINISTRATIVO"}:
        operation, operation_conflict = _resolve(records, "operacion_estimador")
        if operation_conflict or not operation:
            return None, "OPERACION_ADMINISTRATIVA_NO_DOCUMENTADA"
        return operation, None
    if kind in {"MULTIRRESPUESTA", "INDICE", "TEXTO", "TRANSFORMACION_AMBIGUA"}:
        return None, f"TIPO_NO_DERIVABLE:{kind}"
    return None, "TIPO_VARIABLE_NO_DOCUMENTADO"


def _derive_scale(records: list[dict[str, str]]) -> tuple[str | None, str | None]:
    raw_type, conflict = _resolve(records, "tipo_variable")
    if conflict:
        return None, "TIPO_VARIABLE_CONFLICTIVO"
    kind = _normal_type(raw_type)
    coding, coding_conflict = _resolve(records, "codificacion")
    missing, missing_conflict = _resolve(records, "missing")
    if coding_conflict or missing_conflict or not coding or not missing:
        return None, "ESCALA_SIN_CODIFICACION_O_MISSING"
    if kind in {"BINARIA", "BINARIO", "BINARY", "CATEGORICA", "CATEGORICA_EXCLUYENTE", "CATEGORICAL"}:
        categories, categories_conflict = _resolve(records, "categorias")
        if categories_conflict or not categories:
            return None, "ESCALA_SIN_CATEGORIAS"
        return f"tipo={kind};codificacion={coding};categorias={categories};missing={missing}", None
    if kind in {"NUMERICA_CONTINUA", "CONTINUA", "CONTINUOUS"}:
        range_value, range_conflict = _resolve(records, "rango")
        unit, unit_conflict = _resolve(records, "unidad")
        if range_conflict or unit_conflict or not range_value or not unit:
            return None, "ESCALA_NUMERICA_SIN_RANGO_O_UNIDAD"
        return f"tipo={kind};codificacion={coding};rango={range_value};unidad={unit};missing={missing}", None
    if kind in {"ADMINISTRATIVA", "CENSAL", "ADMINISTRATIVO"}:
        range_value, range_conflict = _resolve(records, "rango")
        unit, unit_conflict = _resolve(records, "unidad")
        if range_conflict or unit_conflict or not range_value or not unit:
            return None, "ESCALA_ADMINISTRATIVA_SIN_RANGO_O_UNIDAD"
        return f"tipo={kind};codificacion={coding};rango={range_value};unidad={unit};missing={missing}", None
    return None, "ESCALA_TIPO_NO_DOCUMENTADO"


def _derive_weight(records: list[dict[str, str]]) -> tuple[str | None, str | None]:
    raw_type, _ = _resolve(records, "tipo_variable")
    kind = _normal_type(raw_type)
    weight, conflict = _resolve(records, "ponderador")
    if conflict:
        return None, "PONDERADOR_CONFLICTIVO"
    if kind in {"ADMINISTRATIVA", "CENSAL", "ADMINISTRATIVO"}:
        documented, _ = _resolve(records, "no_aplica_ponderador_documentado")
        if (weight or "").replace("_", " ").upper() == "NO APLICA" and (documented or "").upper() == "SI":
            return "NO APLICA", None
        return None, "NO_APLICA_PONDERADOR_NO_DOCUMENTADO"
    exact, _ = _resolve(records, "ponderador_exacto")
    exact_scope, _ = _resolve(records, "ponderador_fuente_ola_tabla")
    if weight and (exact or "").upper() == "SI" and (exact_scope or "").upper() == "SI":
        return weight, None
    return None, "PONDERADOR_EXACTO_NO_DOCUMENTADO"


def _published(records: list[dict[str, str]]) -> str:
    value, conflict = _resolve(records, "publicada")
    if not conflict and (value or "").upper() in {"SI", "NO"}:
        return (value or "").upper()
    return f"{PENDING}-i"


def _dependency(records: list[dict[str, str]]) -> str:
    value, conflict = _resolve(records, "grado_dependencia")
    if not conflict and (value or "").upper() in {"P0", "P1", "P2"}:
        return (value or "").upper()
    return f"{PENDING}-ii"


def _cv(records: list[dict[str, str]], kind: str) -> tuple[str, bool]:
    value, conflict = _resolve(records, "cv")
    if not value:
        value, conflict = _resolve(records, "cv_arbitro")
    if kind in {"ADMINISTRATIVA", "CENSAL", "ADMINISTRATIVO"}:
        return "NO APLICA", True
    if conflict or not value:
        return f"{PENDING}-iii-CV", True
    match = re.search(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)", value.replace(",", "."))
    if not match:
        return f"{PENDING}-iii-CV", True
    number = float(match.group(0))
    if number < 0:
        return f"{PENDING}-iii-CV", True
    ratio = number / 100.0 if "%" in value or number > 1 else number
    if ratio >= 0.30:
        return f"EXCLUIDA-ADR-135-CV={ratio:.6g}", False
    return f"ADMISIBLE-ADR-135-CV={ratio:.6g}", True


def _n_report(records: list[dict[str, str]]) -> str:
    value, conflict = _resolve(records, "n_no_ponderado")
    if value and not conflict:
        return f"{value} :: REPORTADO-NO-EXCLUYENTE-ADR-135"
    return "POR_MEDIR :: NO-EXCLUYENTE-ADR-135"


def _explicit_or_pending(records: list[dict[str, str]], field: str, suffix: str) -> str:
    value, conflict = _resolve(records, field)
    return value if value and not conflict else f"{PENDING}-{suffix}"


def _candidate_id(identity: tuple[str, ...]) -> str:
    payload = "\x1f".join(identity).encode("utf-8")
    return "CAND-" + hashlib.sha256(payload).hexdigest()[:20]


def _build_candidate(
    manifest_id: str,
    observation: dict[str, str],
    records: list[dict[str, str]],
) -> tuple[dict[str, str] | None, list[str]]:
    reasons: list[str] = []
    variable = _seed_variable(observation)
    if not variable:
        return None, ["SIN_CODIGO_VARIABLE_REAL"]

    resolved: dict[str, str] = {"variable": variable}
    for field in ("encuesta", "ola", "universo"):
        value, conflict = _resolve(records, field)
        if conflict:
            reasons.append(f"{field.upper()}_CONFLICTIVO")
        elif not value:
            reasons.append(f"{field.upper()}_NO_DOCUMENTADO")
        else:
            resolved[field] = value
    estimator, estimator_error = _derive_estimator(records)
    scale, scale_error = _derive_scale(records)
    weight, weight_error = _derive_weight(records)
    for value, error, field in (
        (estimator, estimator_error, "estimador"),
        (scale, scale_error, "escala"),
        (weight, weight_error, "ponderador"),
    ):
        if error or not value:
            reasons.append(error or f"{field.upper()}_NO_DOCUMENTADO")
        else:
            resolved[field] = value
    if reasons:
        return None, reasons

    raw_type, _ = _resolve(records, "tipo_variable")
    cv_text, cv_admissible = _cv(records, _normal_type(raw_type))
    if not cv_admissible:
        return None, [cv_text]
    grade = _dependency(records)
    domain = _explicit_or_pending(records, "dominio", "ESTRATIFICACION-DOMINIO")
    difficulty = _explicit_or_pending(records, "dificultad", "ESTRATIFICACION-DIFICULTAD")
    stratum = (
        f"{domain}|{grade}|{difficulty}"
        if not domain.startswith(PENDING) and not grade.startswith(PENDING) and not difficulty.startswith(PENDING)
        else f"{PENDING}-ESTRATIFICACION"
    )
    identity = (resolved["encuesta"], resolved["ola"], resolved["variable"])
    return {
        "id": _candidate_id(identity),
        "encuesta": resolved["encuesta"], "ola": resolved["ola"],
        "universo": resolved["universo"], "variable": resolved["variable"],
        "estimador": resolved["estimador"], "ponderador": resolved["ponderador"],
        "escala": resolved["escala"], "grado_dependencia": grade,
        "publicada": _published(records), "cv_arbitro": cv_text,
        "n_no_ponderado": _n_report(records),
        "frase_discriminacion": _explicit_or_pending(records, "frase_discriminacion", "iv"),
        "post_corte_u_ola_retenida": _explicit_or_pending(records, "post_corte_u_ola_retenida", "v"),
        "dominio": domain, "dificultad": difficulty, "estrato": stratum,
        "origen_manifiesto_id": manifest_id,
    }, []


def generate(
    manifest: list[dict[str, str]],
    census: list[dict[str, str]],
    reports: list[dict[str, str]],
    *,
    enrichments: Iterable[dict[str, str]] = (),
) -> GenerationResult:
    manifest_index = _index_unique(manifest, "id", "MANIFIESTO")
    census_index = _index_unique(census, "id_manifiesto", "CENSO")
    reports_by_batch: dict[str, list[dict[str, str]]] = {}
    for report in reports:
        reports_by_batch.setdefault(report.get("batch_id", ""), []).append(report)
    extra = list(enrichments)

    rows_by_identity: dict[tuple[str, str, str], dict[str, str]] = {}
    rejected_identities: set[tuple[str, str, str]] = set()
    insufficient: list[dict[str, str]] = []
    conflicts: list[dict[str, str]] = []
    joined_batches: set[str] = set()
    entries_with_e2: set[str] = set()
    observations_examined = 0
    duplicate_count = 0

    for manifest_id in sorted(manifest_index):
        censo = census_index.get(manifest_id)
        if censo is None:
            continue
        batch = censo.get("reporte_neutral_ref", "").strip()
        observations = reports_by_batch.get(batch, [])
        if observations:
            entries_with_e2.add(manifest_id)
            joined_batches.add(batch)
        for observation in sorted(observations, key=lambda row: (row.get("record_id", ""), row.get("objeto_logico_id", ""))):
            observations_examined += 1
            variable = _seed_variable(observation)
            if not variable:
                continue
            manifest_evidence = _canonical_record(manifest_index[manifest_id])
            manifest_evidence["id_manifiesto"] = manifest_id
            observation_evidence = _canonical_record(observation)
            observation_evidence["id_manifiesto"] = manifest_id
            records = [manifest_evidence, observation_evidence]
            records.extend(
                _canonical_record(row) for row in observations
                if row is not observation and _evidence_matches(observation_evidence, _canonical_record(row))
            )
            records.extend(
                _canonical_record(row) for row in extra
                if _evidence_matches(observation_evidence, _canonical_record(row))
            )
            candidate, reasons = _build_candidate(manifest_id, observation, records)
            if candidate is None:
                insufficient.append({
                    "estado": INSUFFICIENT, "origen_manifiesto_id": manifest_id,
                    "batch_id": batch, "record_id": observation.get("record_id", ""),
                    "objeto_logico_id": observation.get("objeto_logico_id", ""),
                    "variable": variable, "motivos": ";".join(sorted(set(reasons))),
                })
                if any("CONFLICT" in reason for reason in reasons):
                    conflicts.append({
                        "estado": "CONFLICTO", "identidad": f"{manifest_id}|{variable}",
                        "motivo": ";".join(sorted(set(reasons))),
                    })
                continue
            identity = (
                candidate["encuesta"], candidate["ola"], candidate["variable"],
            )
            if identity in rejected_identities:
                continue
            previous = rows_by_identity.get(identity)
            if previous is None:
                rows_by_identity[identity] = candidate
            elif all(
                previous[field] == candidate[field]
                for field in MARCO_FIELDS if field not in {"id", "origen_manifiesto_id"}
            ):
                duplicate_count += 1
            else:
                duplicate_count += 1
                conflicts.append({
                    "estado": "CONFLICTO", "identidad": "|".join(identity),
                    "motivo": "DOS_SPECS_DISTINTAS_PARA_IDENTIDAD",
                })
                rejected_identities.add(identity)
                rows_by_identity.pop(identity, None)

    rows = tuple(sorted(rows_by_identity.values(), key=lambda row: tuple(row[field] for field in ("encuesta", "ola", "variable", "origen_manifiesto_id"))))
    insufficient_sorted = tuple(sorted(insufficient, key=lambda row: (row["origen_manifiesto_id"], row["record_id"], row["variable"])))
    unique_conflicts = {
        (row["identidad"], row["motivo"]): row for row in conflicts
    }
    conflicts_sorted = tuple(sorted(unique_conflicts.values(), key=lambda row: (row["identidad"], row["motivo"])))
    summary = {
        "manifiestos_examinados": len(manifest_index),
        "entradas_con_e2": len(entries_with_e2),
        "entradas_sin_e2": len(manifest_index) - len(entries_with_e2),
        "lotes_unidos": len(joined_batches),
        "observaciones_examinadas": observations_examined,
        "candidatas_emitidas": len(rows),
        "observaciones_insuficientes": len(insufficient_sorted),
        "duplicados": duplicate_count,
        "conflictos": len(conflicts_sorted),
    }
    return GenerationResult(rows, insufficient_sorted, conflicts_sorted, summary)


def tsv_bytes(rows: Iterable[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream, fieldnames=MARCO_FIELDS, delimiter="\t", lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def diagnostics_bytes(result: GenerationResult) -> bytes:
    payload = {
        "conflictos": result.conflicts,
        "observaciones_insuficientes": result.insufficient,
        "resumen": result.summary,
    }
    return (json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def generate_from_paths(
    manifest_path: Path,
    census_path: Path,
    reports_path: Path,
    *,
    relations_path: Path | None = None,
    evidence_path: Path | None = None,
) -> GenerationResult:
    enrichments: list[dict[str, str]] = []
    for path in (relations_path, evidence_path):
        if path is not None:
            enrichments.extend(read_tsv(path))
    return generate(
        read_manifest(manifest_path), read_tsv(census_path), read_tsv(reports_path),
        enrichments=enrichments,
    )


def main(argv: list[str] | None = None) -> int:
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=repo / "data/manifiesto.yaml")
    parser.add_argument("--censo", type=Path, default=repo / "data/censo-explotacion-2026-08-17.tsv")
    parser.add_argument("--reportes", type=Path, default=repo / "data/curacion-universo/reportes-inspeccion-barrido2-v1_0.tsv")
    parser.add_argument("--relaciones", type=Path)
    parser.add_argument("--evidencias", type=Path)
    parser.add_argument("--output", type=Path, help="TSV de salida; sin este flag se escribe a stdout")
    parser.add_argument("--diagnostico", type=Path, help="JSON opcional de conteos e insuficiencias")
    args = parser.parse_args(argv)
    result = generate_from_paths(
        args.manifest, args.censo, args.reportes,
        relations_path=args.relaciones, evidence_path=args.evidencias,
    )
    output = tsv_bytes(result.rows)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output)
    else:
        sys.stdout.buffer.write(output)
    if args.diagnostico:
        args.diagnostico.parent.mkdir(parents=True, exist_ok=True)
        args.diagnostico.write_bytes(diagnostics_bytes(result))
    else:
        sys.stderr.buffer.write(diagnostics_bytes(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
