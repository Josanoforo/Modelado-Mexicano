#!/usr/bin/env python3
"""Genera un marco candidato desde el índice E2 privado real, sin inferir specs.

La vía primaria es manifiesto → censo → ledger → índice E2 → hash local. El
reporte E2 compacto es únicamente un control de procedencia y conteo: nunca
crea semillas. Una observación E2 solo crea una semilla cuando ``objeto_tipo``
es VARIABLE-* y ``nombre`` contiene el código real.

Encuesta, ola, universo poblacional, estimador, ponderador y escala se resuelven
solo con campos estructurados semánticamente aptos. En particular, nombres de
archivo, ``fuente_programa``/``edicion_periodo`` de T0, tipos físicos y prosa
neutral no se promueven. La corrida real puede emitir cero candidatas; el
diagnóstico describe cobertura e insuficiencias y nunca declara saturación.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml

try:
    from .autoridad_semantica_marco import (
        AutoridadSemanticaError,
        SemanticAuthorityIndex,
        load_semantic_authority,
    )
    from .marco_e2_adapter import (
        E2AdapterError,
        E2IndexReader,
        EVIDENCE_STATES,
        JoinResolution,
        Provenance,
        ProvenanceIndex,
        expected_index_sha,
        is_meaningful,
        is_variable_seed,
        resolve_private_index,
    )
except ImportError:
    from autoridad_semantica_marco import (
        AutoridadSemanticaError,
        SemanticAuthorityIndex,
        load_semantic_authority,
    )
    from marco_e2_adapter import (
        E2AdapterError,
        E2IndexReader,
        EVIDENCE_STATES,
        JoinResolution,
        Provenance,
        ProvenanceIndex,
        expected_index_sha,
        is_meaningful,
        is_variable_seed,
        resolve_private_index,
    )


MARCO_FIELDS = (
    "id",
    "encuesta",
    "ola",
    "universo",
    "variable",
    "estimador",
    "ponderador",
    "escala",
    "grado_dependencia",
    "publicada",
    "cv_arbitro",
    "n_no_ponderado",
    "frase_discriminacion",
    "post_corte_u_ola_retenida",
    "dominio",
    "dificultad",
    "estrato",
    "origen_manifiesto_id",
)

REQUIRED_COMPONENTS = (
    "encuesta",
    "ola",
    "universo",
    "variable",
    "estimador",
    "ponderador",
    "escala",
)

SEMANTIC_AUTHORITY_SPEC_FIELDS = (
    "encuesta",
    "ola",
    "universo_poblacional",
    "unidad_observacion",
    "tipo_estadistico",
    "respuesta_multiple",
    "categorias_excluyentes",
    "codificacion",
    "missing",
    "unidad_medida",
    "rango_valido",
    "operacion_estimador",
    "ponderador",
    "ponderador_exacto",
    "ponderador_fuente_ola_tabla",
    "ponderador_fuente",
    "ponderador_ola",
    "ponderador_scope_tipo",
    "ponderador_scope_id",
    "no_aplica_ponderador_documentado",
)

PENDING = "PENDIENTE-FILTRO"


class MarcoError(ValueError):
    """Fallo cerrado en la derivación de una spec."""


@dataclass(frozen=True)
class E2GenerationResult:
    rows: tuple[dict[str, str], ...]
    diagnostics: dict[str, Any]


def _text(value: Any) -> str:
    return str(value or "").strip()


def read_tsv(path: Path) -> list[dict[str, str]]:
    try:
        handle = path.open(encoding="utf-8-sig", newline="")
    except FileNotFoundError as exc:
        raise MarcoError(f"TSV_AUSENTE:{path}") from exc
    with handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames is None:
            raise MarcoError(f"TSV_SIN_CABECERA:{path}")
        return [
            {str(key): _text(value) for key, value in row.items()}
            for row in reader
        ]


def read_manifest(path: Path) -> list[dict[str, str]]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise MarcoError(f"MANIFIESTO_AUSENTE:{path}") from exc
    if not isinstance(payload, list):
        raise MarcoError("MANIFIESTO_NO_ES_LISTA")
    return [
        {str(key): _text(value) for key, value in row.items()}
        for row in payload
        if isinstance(row, dict)
    ]


def _normal_type(value: Any) -> str:
    return re.sub(r"[^A-Z0-9]+", "_", _text(value).upper()).strip("_")


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _semantic_authority_spec(authority: Mapping[str, Any]) -> str:
    """Spec conceptual sin clave material, aserciones E2 ni citas."""

    return _canonical_json(
        {field: authority.get(field) for field in SEMANTIC_AUTHORITY_SPEC_FIELDS}
    )


def _derive_estimator(authority: Mapping[str, Any]) -> tuple[str | None, str | None]:
    kind = _normal_type(authority.get("tipo_estadistico"))
    if kind == "BINARIA":
        return "PROPORCION_PONDERADA", None
    if kind == "CATEGORICA":
        if authority.get("respuesta_multiple") or not authority.get(
            "categorias_excluyentes"
        ):
            return None, "CATEGORIAS_NO_DOCUMENTADAS_COMO_EXCLUYENTES"
        return "DISTRIBUCION_PONDERADA", None
    if kind == "NUMERICA_CONTINUA":
        if not is_meaningful(authority.get("unidad_medida")):
            return None, "NUMERICA_SIN_UNIDAD"
        return "MEDIA_PONDERADA", None
    if kind in {"ADMINISTRATIVA", "CENSAL"}:
        operation = _text(authority.get("operacion_estimador"))
        if not is_meaningful(operation):
            return None, "OPERACION_ADMINISTRATIVA_NO_DOCUMENTADA"
        return operation, None
    return None, "TIPO_ESTADISTICO_AUSENTE_EN_CONTRATO"


def _derive_scale(
    record: Mapping[str, Any], authority: Mapping[str, Any]
) -> tuple[str | None, str | None]:
    kind = _normal_type(authority.get("tipo_estadistico"))
    coding = authority.get("codificacion")
    missing = authority.get("missing")
    if not isinstance(coding, list) or not coding or not isinstance(missing, dict):
        return None, "CODIFICACION_O_MISSING_AUSENTE_EN_CONTRATO"
    if kind in {"BINARIA", "CATEGORICA"}:
        return (
            f"tipo={kind};codificacion={_canonical_json(coding)};"
            f"missing={_canonical_json(missing)}",
            None,
        )
    if kind in {"NUMERICA_CONTINUA", "ADMINISTRATIVA", "CENSAL"}:
        range_value = authority.get("rango_valido")
        unit = _text(authority.get("unidad_medida"))
        if not isinstance(range_value, dict) or not is_meaningful(unit):
            return None, "ESCALA_NUMERICA_SIN_RANGO_O_UNIDAD"
        return (
            f"tipo={kind};codificacion={_canonical_json(coding)};"
            f"rango={_canonical_json(range_value)};unidad={unit};"
            f"missing={_canonical_json(missing)}",
            None,
        )
    return None, "TIPO_ESTADISTICO_AUSENTE_EN_CONTRATO"


def _derive_weight(authority: Mapping[str, Any]) -> tuple[str | None, str | None]:
    kind = _normal_type(authority.get("tipo_estadistico"))
    weight = _text(authority.get("ponderador"))
    if kind in {"ADMINISTRATIVA", "CENSAL"}:
        documented = authority.get("no_aplica_ponderador_documentado")
        if weight.replace("_", " ").upper() == "NO APLICA" and documented is True:
            return "NO APLICA", None
        return None, "NO_APLICA_PONDERADOR_NO_DOCUMENTADO"
    exact = authority.get("ponderador_exacto")
    scope = authority.get("ponderador_fuente_ola_tabla")
    if is_meaningful(weight) and exact is True and scope is True:
        return weight, None
    return None, "PONDERADOR_EXACTO_SCOPE_AUSENTE_EN_CONTRATO"


def _classify_seed(
    record: Mapping[str, Any],
    join: JoinResolution,
    provenance_index: ProvenanceIndex,
    authority: Mapping[str, Any] | None,
) -> tuple[dict[str, str], list[str]]:
    states = {field: "AUSENTE_EN_CONTRATO" for field in REQUIRED_COMPONENTS}
    states["variable"] = "EXISTE_ESTRUCTURADO"
    reasons: list[str] = []

    if join.status != "EXACTA":
        reasons.append(join.reason)
    if authority is None:
        reasons.append("AUTORIDAD_SEMANTICA_AUSENTE")
    material: Mapping[str, Any] = authority or {}
    t0 = (
        provenance_index.t0_semantic_fields(join.provenance.hash_local)
        if join.provenance is not None
        else {}
    )
    for field, t0_field in (("encuesta", "fuente_programa"), ("ola", "edicion_periodo")):
        if is_meaningful(material.get(field)):
            states[field] = "DERIVABLE_EXACTO"
        elif is_meaningful(t0.get(t0_field)):
            states[field] = "NO_SEMANTICAMENTE_APTO"
            reasons.append(f"{field.upper()}_NO_SEMANTICAMENTE_APTA")
        else:
            reasons.append(f"{field.upper()}_AUSENTE_EN_CONTRATO")

    if is_meaningful(material.get("universo_poblacional")):
        states["universo"] = "DERIVABLE_EXACTO"
    elif is_meaningful(record.get("poblacion")):
        states["universo"] = "EXISTE_ESTRUCTURADO"
    else:
        reasons.append("UNIVERSO_POBLACIONAL_AUSENTE_EN_CONTRATO")

    estimator, estimator_error = _derive_estimator(material)
    if estimator:
        states["estimador"] = "DERIVABLE_EXACTO"
    else:
        reasons.append(estimator_error or "ESTIMADOR_AUSENTE_EN_CONTRATO")
    weight, weight_error = _derive_weight(material)
    if weight:
        states["ponderador"] = "DERIVABLE_EXACTO"
    else:
        reasons.append(weight_error or "PONDERADOR_AUSENTE_EN_CONTRATO")
    scale, scale_error = _derive_scale(record, material)
    if scale:
        states["escala"] = "DERIVABLE_EXACTO"
    else:
        reasons.append(scale_error or "ESCALA_AUSENTE_EN_CONTRATO")
    if authority is not None and not material.get("cita_procedencia"):
        reasons.append("CITA_PROCEDENCIA_AUSENTE_EN_CONTRATO")
    return states, sorted(set(reasons))


def _candidate_id(identity: tuple[str, ...]) -> str:
    encoded = "\x1f".join(identity).encode("utf-8")
    return "CAND-" + hashlib.sha256(encoded).hexdigest()[:20]


def _cv(authority: Mapping[str, Any], kind: str) -> tuple[str, bool]:
    if kind in {"ADMINISTRATIVA", "CENSAL"}:
        return "NO APLICA", True
    value = _text(authority.get("cv"))
    if not value:
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


def _pending(authority: Mapping[str, Any], field: str, suffix: str) -> str:
    value = _text(authority.get(field))
    return value if is_meaningful(value) else f"{PENDING}-{suffix}"


def _build_candidate(
    record: Mapping[str, Any],
    provenance: Provenance,
    authority: Mapping[str, Any],
) -> tuple[dict[str, str] | None, list[str]]:
    reasons: list[str] = []
    survey = _text(authority.get("encuesta"))
    wave = _text(authority.get("ola"))
    population = _text(authority.get("universo_poblacional"))
    if not is_meaningful(population):
        population = _text(record.get("poblacion"))
    for field, value in (("ENCUESTA", survey), ("OLA", wave), ("UNIVERSO", population)):
        if not is_meaningful(value):
            reasons.append(f"{field}_AUSENTE_EN_CONTRATO")
    if not authority.get("cita_procedencia"):
        reasons.append("CITA_PROCEDENCIA_AUSENTE_EN_CONTRATO")

    estimator, estimator_error = _derive_estimator(authority)
    weight, weight_error = _derive_weight(authority)
    scale, scale_error = _derive_scale(record, authority)
    reasons.extend(
        error for error in (estimator_error, weight_error, scale_error) if error
    )
    if reasons:
        return None, sorted(set(reasons))

    kind = _normal_type(authority.get("tipo_estadistico"))
    cv_text, admissible = _cv(authority, kind)
    if not admissible:
        return None, [cv_text]
    variable = _text(record.get("nombre"))
    identity = (survey, wave, variable)
    dependency = _pending(authority, "grado_dependencia", "ii")
    domain = _pending(authority, "dominio", "ESTRATIFICACION-DOMINIO")
    difficulty = _pending(authority, "dificultad", "ESTRATIFICACION-DIFICULTAD")
    stratum = (
        f"{domain}|{dependency}|{difficulty}"
        if not any(value.startswith(PENDING) for value in (domain, dependency, difficulty))
        else f"{PENDING}-ESTRATIFICACION"
    )
    unweighted_n = _text(authority.get("n_no_ponderado"))
    n_report = (
        f"{unweighted_n} :: REPORTADO-NO-EXCLUYENTE-ADR-135"
        if is_meaningful(unweighted_n)
        else "POR_MEDIR :: NO-EXCLUYENTE-ADR-135"
    )
    return {
        "id": _candidate_id(identity),
        "encuesta": survey,
        "ola": wave,
        "universo": population,
        "variable": variable,
        "estimador": estimator or "",
        "ponderador": weight or "",
        "escala": scale or "",
        "grado_dependencia": dependency,
        "publicada": _pending(authority, "publicada", "i"),
        "cv_arbitro": cv_text,
        "n_no_ponderado": n_report,
        "frase_discriminacion": _pending(authority, "frase_discriminacion", "iv"),
        "post_corte_u_ola_retenida": _pending(
            authority, "post_corte_u_ola_retenida", "v"
        ),
        "dominio": domain,
        "dificultad": difficulty,
        "estrato": stratum,
        "origen_manifiesto_id": provenance.manifest_id,
    }, []


def generate_from_e2_paths(
    *,
    repo: Path,
    manifest_path: Path,
    census_path: Path,
    ledger_path: Path,
    declared_universe_path: Path,
    contract_path: Path,
    baseline_path: Path,
    index_path: Path | None = None,
    compact_report_path: Path | None = None,
    semantic_authority: (
        Iterable[Mapping[str, Any]] | SemanticAuthorityIndex | None
    ) = None,
) -> E2GenerationResult:
    manifest = read_manifest(manifest_path)
    census = read_tsv(census_path)
    ledger = read_tsv(ledger_path)
    declared_universe = read_tsv(declared_universe_path)
    if isinstance(semantic_authority, SemanticAuthorityIndex):
        authority_index = semantic_authority
    elif semantic_authority is None:
        authority_index = None
    else:
        authority_rows = tuple(semantic_authority)
        authority_index = (
            SemanticAuthorityIndex(authority_rows) if authority_rows else None
        )
    private_index, contract = resolve_private_index(repo, contract_path, index_path)
    expected_sha = expected_index_sha(baseline_path)
    if compact_report_path is None:
        compact_control_rows = 0
        compact_control_status = "NO_CONFIGURADO_NO_GATING"
    elif compact_report_path.is_file():
        compact_control_rows = len(read_tsv(compact_report_path))
        compact_control_status = "PRESENTE_CONTROL"
    else:
        compact_control_rows = 0
        compact_control_status = "AUSENTE_NO_GATING"
    provenance_index = ProvenanceIndex(manifest, census, ledger, declared_universe)

    seeds_by_type: Counter[str] = Counter()
    joins: Counter[str] = Counter()
    structured_e2_evidence: Counter[str] = Counter()
    field_coverage = {
        field: Counter({state: 0 for state in EVIDENCE_STATES})
        for field in REQUIRED_COMPONENTS
    }
    insufficiency_reasons: Counter[str] = Counter()
    rows_by_identity: dict[tuple[str, str, str], dict[str, str]] = {}
    specs_by_identity: dict[tuple[str, str, str], str] = {}
    rejected_identities: set[tuple[str, str, str]] = set()
    conceptual_conflicts: set[tuple[str, str, str]] = set()
    insufficient_count = 0
    duplicates = 0
    conflicts = 0

    reader = E2IndexReader(private_index)
    for record in reader:
        if not is_variable_seed(record):
            continue
        object_type = _text(record.get("objeto_tipo")).upper()
        seeds_by_type[object_type] += 1
        for field in ("categorias", "value_labels"):
            if isinstance(record.get(field), list) and record[field]:
                structured_e2_evidence[field] += 1
        for field in ("unidad", "periodo", "poblacion"):
            if is_meaningful(record.get(field)):
                structured_e2_evidence[field] += 1
        join = provenance_index.resolve(record)
        joins[join.status.lower()] += 1
        authority = authority_index.lookup(record) if authority_index is not None else None
        states, reasons = _classify_seed(record, join, provenance_index, authority)
        for field, state in states.items():
            field_coverage[field][state] += 1

        candidate: dict[str, str] | None = None
        candidate_reasons: list[str] = []
        if join.provenance is not None and authority is not None:
            candidate, candidate_reasons = _build_candidate(
                record, join.provenance, authority
            )
        reasons = sorted(set(reasons + candidate_reasons))
        if candidate is None:
            insufficient_count += 1
            for reason in reasons or ("SPEC_INCOMPLETA",):
                insufficiency_reasons[reason] += 1
            if join.status == "AMBIGUA":
                conflicts += 1
            continue

        identity = (
            candidate["encuesta"],
            candidate["ola"],
            candidate["variable"],
        )
        semantic_spec = _semantic_authority_spec(authority)
        if identity in rejected_identities:
            continue
        previous = rows_by_identity.get(identity)
        if previous is None:
            rows_by_identity[identity] = candidate
            specs_by_identity[identity] = semantic_spec
        elif specs_by_identity[identity] == semantic_spec and all(
            previous[field] == candidate[field]
            for field in MARCO_FIELDS
            if field not in {"id", "origen_manifiesto_id"}
        ):
            duplicates += 1
            if candidate["origen_manifiesto_id"] < previous["origen_manifiesto_id"]:
                rows_by_identity[identity] = candidate
        else:
            duplicates += 1
            conflicts += 1
            rejected_identities.add(identity)
            conceptual_conflicts.add(identity)
            rows_by_identity.pop(identity, None)
            specs_by_identity.pop(identity, None)

    reader.require_sha(expected_sha)
    if authority_index is not None:
        authority_index.assert_no_orphans()
    if conceptual_conflicts:
        identities = ",".join(
            _canonical_json(
                {"encuesta": survey, "ola": wave, "variable": variable}
            )
            for survey, wave, variable in sorted(conceptual_conflicts)
        )
        raise MarcoError(f"CONFLICTO_IDENTIDAD_CONCEPTUAL:{identities}")
    rows = tuple(
        sorted(
            rows_by_identity.values(),
            key=lambda row: (
                row["encuesta"],
                row["ola"],
                row["variable"],
                row["origen_manifiesto_id"],
            ),
        )
    )
    diagnostic = {
        "cobertura_campos": {
            field: {state: field_coverage[field][state] for state in EVIDENCE_STATES}
            for field in REQUIRED_COMPONENTS
        },
        "razones_insuficiencia": dict(sorted(insufficiency_reasons.items())),
        "evidencia_e2_estructurada": {
            field: structured_e2_evidence[field]
            for field in ("categorias", "value_labels", "unidad", "periodo", "poblacion")
        },
        "resumen": {
            "autoridades_declaradas": (
                authority_index.row_count if authority_index is not None else 0
            ),
            "autoridades_enlazadas": (
                authority_index.matched_count if authority_index is not None else 0
            ),
            "candidatas_emitidas": len(rows),
            "conflictos": conflicts,
            "duplicados": duplicates,
            "manifiestos_examinados": len(manifest),
            "observaciones_insuficientes": insufficient_count,
            "registros_e2_leidos": reader.records_read,
            "semillas_reales": sum(seeds_by_type.values()),
            "uniones_ambiguas": joins["ambigua"],
            "uniones_ausentes": joins["ausente"],
            "uniones_exactas": joins["exacta"],
        },
        "semillas_por_objeto_tipo": dict(sorted(seeds_by_type.items())),
        "validacion_indice": {
            "contrato_schema_version": _text(contract.get("schema_version")),
            "registros": reader.records_read,
            "reporte_compacto_estado": compact_control_status,
            "reporte_compacto_filas_control": compact_control_rows,
            "sha256": reader.sha256,
            "sha256_esperado": expected_sha,
        },
    }
    return E2GenerationResult(rows, diagnostic)


def tsv_bytes(rows: Iterable[dict[str, str]]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=MARCO_FIELDS,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="raise",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def diagnostics_bytes(result: E2GenerationResult) -> bytes:
    return (
        json.dumps(
            result.diagnostics,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    repo = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=repo / "data/manifiesto.yaml")
    parser.add_argument(
        "--censo", type=Path, default=repo / "data/censo-explotacion-2026-08-17.tsv"
    )
    parser.add_argument(
        "--ledger",
        type=Path,
        default=repo / "data/curacion-universo/ledger-inspecciones-barrido2.tsv",
    )
    parser.add_argument(
        "--universo-t0",
        type=Path,
        default=repo / "data/curacion-universo/universo-declarado-t0.tsv",
    )
    parser.add_argument(
        "--contrato",
        type=Path,
        default=repo / "data/curacion-universo/contrato-barrido2-v1_0.json",
    )
    parser.add_argument(
        "--baseline-material",
        type=Path,
        default=repo / "data/curacion-universo/baseline-material-barrido2.json",
    )
    parser.add_argument(
        "--reporte-compacto",
        type=Path,
        default=repo / "data/curacion-universo/reportes-inspeccion-barrido2-v1_0.tsv",
        help="Solo conteo de control; nunca crea semillas",
    )
    parser.add_argument(
        "--autoridad-semantica",
        type=Path,
        default=(
            repo
            / "data/curacion-universo/autoridad-semantica-marco-v1_0.jsonl"
        ),
    )
    parser.add_argument("--indice-e2", type=Path)
    parser.add_argument("--output", type=Path, help="TSV; use /tmp para el smoke real")
    parser.add_argument("--diagnostico", type=Path, help="JSON diagnóstico")
    args = parser.parse_args(argv)
    try:
        semantic_authority = load_semantic_authority(args.autoridad_semantica)
        result = generate_from_e2_paths(
            repo=repo,
            manifest_path=args.manifest,
            census_path=args.censo,
            ledger_path=args.ledger,
            declared_universe_path=args.universo_t0,
            contract_path=args.contrato,
            baseline_path=args.baseline_material,
            index_path=args.indice_e2,
            compact_report_path=args.reporte_compacto,
            semantic_authority=semantic_authority,
        )
    except (AutoridadSemanticaError, MarcoError, E2AdapterError) as exc:
        print(f"ERROR:{exc}", file=sys.stderr)
        return 2

    output = tsv_bytes(result.rows)
    if args.output is None:
        sys.stdout.buffer.write(output)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(output)
    diagnostic = diagnostics_bytes(result)
    if args.diagnostico is None:
        sys.stderr.buffer.write(diagnostic)
    else:
        args.diagnostico.parent.mkdir(parents=True, exist_ok=True)
        args.diagnostico.write_bytes(diagnostic)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
