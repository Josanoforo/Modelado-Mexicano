#!/usr/bin/env python3
"""Adaptador fail-closed para el índice E2 privado de BARRIDO-2.

El reporte durable E2 es un compacto de control y procedencia: no contiene el
universo de objetos. Este módulo abre en streaming el índice privado declarado
por el contrato, calcula su SHA-256 sobre los bytes leídos y exige que coincida
con el baseline material antes de aceptar el resultado de una corrida.

Las uniones se hacen únicamente por identificadores y hashes. Ningún nombre de
archivo, descripción neutral, tipo físico o fecha de incorporación se interpreta
como encuesta, ola o tipo estadístico.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping


EVIDENCE_STATES = (
    "EXISTE_ESTRUCTURADO",
    "DERIVABLE_EXACTO",
    "AUSENTE_EN_CONTRATO",
    "CONFLICTIVO",
    "NO_SEMANTICAMENTE_APTO",
)

VARIABLE_OBJECT_TYPES = frozenset(
    {
        "VARIABLE-DTA",
        "VARIABLE-SAV",
        "VARIABLE-DICCIONARIO",
        "VARIABLE-DICCIONARIO-XLS",
        "VARIABLE-DICCIONARIO-XLSX",
    }
)

E2_REQUIRED_FIELDS = (
    "schema_version",
    "record_id",
    "record_sha256",
    "batch_id",
    "batch_sha256",
    "payload_id",
    "representacion_id",
    "sha256",
    "objeto_logico_id",
    "root_id",
    "ruta_relativa",
    "format",
    "depth",
    "localizador",
    "objeto_tipo",
    "nombre",
    "etiqueta",
    "texto_reactivo",
    "definicion",
    "categorias",
    "value_labels",
    "unidad",
    "periodo",
    "poblacion",
    "pagina",
    "hoja",
    "tabla",
    "objeto_padre_id",
    "relacion_estructural",
    "frontera_inspeccion",
    "parser",
    "parser_version",
    "estado",
    "privacidad",
    "fecha",
)

NOT_APPLICABLE = frozenset(
    {
        "",
        "NO-APLICA",
        "NO_APLICA",
        "NO-DETERMINADO",
        "NO_DETERMINADO",
        "[REDACTADO-PRIVACIDAD]",
    }
)


class E2AdapterError(ValueError):
    """Fallo cerrado del contrato o de la procedencia E2."""


@dataclass(frozen=True)
class Provenance:
    manifest_id: str
    representacion_id: str
    batch_id: str
    payload_id: str
    hash_local: str
    objeto_logico_id: str
    record_id: str
    tabla: str
    objeto_padre_id: str


@dataclass(frozen=True)
class JoinResolution:
    status: str
    provenance: Provenance | None
    reason: str


def _text(value: Any) -> str:
    return str(value or "").strip()


def is_meaningful(value: Any) -> bool:
    return _text(value).upper() not in NOT_APPLICABLE


def is_variable_seed(record: Mapping[str, Any]) -> bool:
    """Selecciona únicamente tipos VARIABLE-* con un ``nombre`` concreto."""

    kind = _text(record.get("objeto_tipo")).upper()
    name = _text(record.get("nombre"))
    return bool(
        (kind in VARIABLE_OBJECT_TYPES or kind.startswith("VARIABLE-"))
        and is_meaningful(name)
        and not name.upper().startswith("OBJ-B2-")
        and not name.isdigit()
    )


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise E2AdapterError(f"{label}_AUSENTE:{path}") from exc
    except json.JSONDecodeError as exc:
        raise E2AdapterError(f"{label}_JSON_INVALIDO:{path}:{exc}") from exc
    if not isinstance(payload, dict):
        raise E2AdapterError(f"{label}_NO_ES_OBJETO:{path}")
    return payload


def resolve_private_index(
    repo: Path,
    contract_path: Path,
    explicit_path: Path | None = None,
) -> tuple[Path, dict[str, Any]]:
    """Resuelve la ruta declarada; un override solo cambia su ubicación física."""

    contract = load_json_object(contract_path, "CONTRATO_BARRIDO2")
    declared = _text(contract.get("private_e2_index"))
    if not declared:
        raise E2AdapterError("CONTRATO_SIN_PRIVATE_E2_INDEX")
    path = explicit_path if explicit_path is not None else repo / declared
    if path.name != Path(declared).name:
        raise E2AdapterError(
            f"INDICE_E2_NO_CORRESPONDE_AL_CONTRATO:{path.name}!={Path(declared).name}"
        )
    if not path.is_file():
        raise E2AdapterError(f"INDICE_E2_AUSENTE:{path}")
    return path, contract


def expected_index_sha(baseline_path: Path) -> str:
    baseline = load_json_object(baseline_path, "BASELINE_MATERIAL_BARRIDO2")
    expected = _text(baseline.get("e2_index_sha256")).lower()
    if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
        raise E2AdapterError("BASELINE_SIN_E2_INDEX_SHA256_VALIDO")
    return expected


class E2IndexReader(Iterable[dict[str, Any]]):
    """Iterador de una sola pasada que hashea exactamente los bytes del JSONL."""

    def __init__(self, path: Path):
        self.path = path
        self.sha256 = ""
        self.records_read = 0
        self._consumed = False

    def __iter__(self) -> Iterator[dict[str, Any]]:
        if self._consumed:
            raise E2AdapterError("INDICE_E2_ITERADO_MAS_DE_UNA_VEZ")
        self._consumed = True
        digest = hashlib.sha256()
        try:
            handle = self.path.open("rb")
        except FileNotFoundError as exc:
            raise E2AdapterError(f"INDICE_E2_AUSENTE:{self.path}") from exc
        with handle:
            for line_number, raw_line in enumerate(handle, 1):
                digest.update(raw_line)
                if not raw_line.strip():
                    raise E2AdapterError(f"INDICE_E2_LINEA_VACIA:{line_number}")
                try:
                    record = json.loads(raw_line)
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise E2AdapterError(
                        f"INDICE_E2_JSON_INVALIDO:linea={line_number}:{exc}"
                    ) from exc
                self._validate_record(record, line_number)
                self.records_read = line_number
                yield record
        self.sha256 = digest.hexdigest()

    @staticmethod
    def _validate_record(record: Any, line_number: int) -> None:
        if not isinstance(record, dict):
            raise E2AdapterError(f"INDICE_E2_REGISTRO_NO_OBJETO:linea={line_number}")
        missing = [field for field in E2_REQUIRED_FIELDS if field not in record]
        if missing:
            raise E2AdapterError(
                f"INDICE_E2_SCHEMA_INCOMPLETO:linea={line_number}:"
                + ",".join(missing)
            )
        if record.get("schema_version") != "BARRIDO2-E2-1.0":
            raise E2AdapterError(
                f"INDICE_E2_SCHEMA_VERSION_INVALIDA:linea={line_number}"
            )
        for field in ("categorias", "value_labels"):
            if not isinstance(record.get(field), list):
                raise E2AdapterError(
                    f"INDICE_E2_{field.upper()}_NO_ES_LISTA:linea={line_number}"
                )

    def require_sha(self, expected: str) -> None:
        if not self._consumed or not self.sha256:
            raise E2AdapterError("INDICE_E2_NO_CONSUMIDO_COMPLETAMENTE")
        if self.sha256 != expected.lower():
            raise E2AdapterError(
                f"INDICE_E2_SHA256_DIVERGENTE:esperado={expected.lower()}:"
                f"observado={self.sha256}"
            )


class ProvenanceIndex:
    """Índice de la cadena manifiesto→censo→ledger→E2→hash_local."""

    def __init__(
        self,
        manifest: Iterable[Mapping[str, Any]],
        census: Iterable[Mapping[str, Any]],
        ledger: Iterable[Mapping[str, Any]],
        declared_universe: Iterable[Mapping[str, Any]],
    ):
        manifest_ids = {_text(row.get("id")) for row in manifest if _text(row.get("id"))}
        census_routes: dict[tuple[str, str], list[dict[str, str]]] = {}
        for raw in census:
            manifest_id = _text(raw.get("id_manifiesto"))
            representation = _text(raw.get("representacion_id"))
            batch = _text(raw.get("reporte_neutral_ref"))
            if manifest_id in manifest_ids and representation and batch:
                census_routes.setdefault((representation, batch), []).append(
                    {
                        "manifest_id": manifest_id,
                        "sha256": _text(raw.get("sha256_observado")).lower(),
                    }
                )

        ledger_routes: dict[tuple[str, str], list[dict[str, str]]] = {}
        for raw in ledger:
            key = (
                _text(raw.get("representacion_id")),
                _text(raw.get("reporte_neutral_ref")),
            )
            if all(key):
                ledger_routes.setdefault(key, []).append(
                    {
                        "payload_id": _text(raw.get("payload_id")),
                        "sha256": _text(raw.get("sha256")).lower(),
                    }
                )

        t0_by_hash: dict[str, list[dict[str, str]]] = {}
        for raw in declared_universe:
            local_hash = _text(raw.get("hash_local")).lower()
            if is_meaningful(local_hash):
                t0_by_hash.setdefault(local_hash, []).append(
                    {
                        "fuente_programa": _text(raw.get("fuente_programa")),
                        "edicion_periodo": _text(raw.get("edicion_periodo")),
                    }
                )
        self._census_routes = census_routes
        self._ledger_routes = ledger_routes
        self._t0_by_hash = t0_by_hash

    def component_cardinalities(self, record: Mapping[str, Any]) -> dict[str, int]:
        """Expone cardinalidades de la unión sin atribuirles semántica."""

        representation = _text(record.get("representacion_id"))
        batch = _text(record.get("batch_id"))
        content_hash = _text(record.get("sha256")).lower()
        payload = _text(record.get("payload_id"))
        key = (representation, batch)
        census_routes = [
            row
            for row in self._census_routes.get(key, [])
            if not row["sha256"] or row["sha256"] == content_hash
        ]
        ledger_routes = [
            row
            for row in self._ledger_routes.get(key, [])
            if row["sha256"] == content_hash and row["payload_id"] == payload
        ]
        return {
            "censo": len(census_routes),
            "ledger": len(ledger_routes),
            "t0": len(self._t0_by_hash.get(content_hash, [])),
        }

    def resolve_repaired(self, record: Mapping[str, Any]) -> JoinResolution:
        """Repara sólo T0 ausente cuando censo y ledger son 1:1 exactos.

        Hash, representación, batch y payload deben coincidir. Una ruta de
        censo ausente nunca se adjudica por nombre o semejanza.
        """

        strict = self.resolve(record)
        if strict.status != "AUSENTE":
            return strict
        cardinalities = self.component_cardinalities(record)
        if cardinalities != {"censo": 1, "ledger": 1, "t0": 0}:
            return strict
        representation = _text(record.get("representacion_id"))
        batch = _text(record.get("batch_id"))
        content_hash = _text(record.get("sha256")).lower()
        payload = _text(record.get("payload_id"))
        census_route = next(
            row
            for row in self._census_routes[(representation, batch)]
            if not row["sha256"] or row["sha256"] == content_hash
        )
        provenance = Provenance(
            manifest_id=census_route["manifest_id"],
            representacion_id=representation,
            batch_id=batch,
            payload_id=payload,
            hash_local=content_hash,
            objeto_logico_id=_text(record.get("objeto_logico_id")),
            record_id=_text(record.get("record_id")),
            tabla=_text(record.get("tabla")),
            objeto_padre_id=_text(record.get("objeto_padre_id")),
        )
        return JoinResolution(
            "EXACTA_REPARADA",
            provenance,
            "T0_AUSENTE_RECONSTRUIDO_POR_CENSO_LEDGER_HASH",
        )

    def resolve(self, record: Mapping[str, Any]) -> JoinResolution:
        representation = _text(record.get("representacion_id"))
        batch = _text(record.get("batch_id"))
        content_hash = _text(record.get("sha256")).lower()
        payload = _text(record.get("payload_id"))
        key = (representation, batch)
        census_routes = self._census_routes.get(key, [])
        ledger_routes = [
            row
            for row in self._ledger_routes.get(key, [])
            if row["sha256"] == content_hash and row["payload_id"] == payload
        ]
        t0_routes = self._t0_by_hash.get(content_hash, [])
        census_routes = [
            row for row in census_routes if not row["sha256"] or row["sha256"] == content_hash
        ]
        cardinalities = (len(census_routes), len(ledger_routes), len(t0_routes))
        if any(count > 1 for count in cardinalities):
            return JoinResolution("AMBIGUA", None, "UNION_PROCEDENCIA_AMBIGUA")
        if any(count == 0 for count in cardinalities):
            return JoinResolution("AUSENTE", None, "UNION_PROCEDENCIA_AUSENTE")
        provenance = Provenance(
            manifest_id=census_routes[0]["manifest_id"],
            representacion_id=representation,
            batch_id=batch,
            payload_id=payload,
            hash_local=content_hash,
            objeto_logico_id=_text(record.get("objeto_logico_id")),
            record_id=_text(record.get("record_id")),
            tabla=_text(record.get("tabla")),
            objeto_padre_id=_text(record.get("objeto_padre_id")),
        )
        return JoinResolution("EXACTA", provenance, "")

    def t0_semantic_fields(self, content_hash: str) -> dict[str, str]:
        """Expone controladamente T0; sus campos nunca se consideran semánticos."""

        matches = self._t0_by_hash.get(content_hash.lower(), [])
        return dict(matches[0]) if len(matches) == 1 else {}
