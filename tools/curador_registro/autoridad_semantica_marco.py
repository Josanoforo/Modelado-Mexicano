#!/usr/bin/env python3
"""Loader fail-closed de autoridades semanticas del marco candidato.

La clave de autoridad es material: representacion, scope y variable. La
identidad conceptual de una candidata se resuelve aparte en ``generar_marco``.
Los identificadores de semilla y registro E2 son aserciones anti-deriva, nunca
sustitutos de la clave material.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

try:
    from .marco_e2_adapter import is_meaningful
except ImportError:
    from marco_e2_adapter import is_meaningful


SCHEMA_VERSION = "AUTORIDAD-SEMANTICA-MARCO-1.0"
SCOPE_TYPES = frozenset({"OBJETO_PADRE_ID", "TABLA"})
STATISTICAL_TYPES = frozenset(
    {"BINARIA", "CATEGORICA", "NUMERICA_CONTINUA", "ADMINISTRATIVA", "CENSAL"}
)
ROW_FIELDS = frozenset(
    {
        "schema_version",
        "autoridad_id",
        "representacion_id",
        "semilla_objeto_logico_id",
        "e2_record_id",
        "payload_id",
        "sha256_contenido",
        "scope_tipo",
        "scope_id",
        "variable",
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
        "cita_procedencia",
    }
)
BASE_CITABLE_FIELDS = frozenset(
    {
        "encuesta",
        "ola",
        "universo_poblacional",
        "unidad_observacion",
        "tipo_estadistico",
        "respuesta_multiple",
        "categorias_excluyentes",
        "codificacion",
        "missing",
        "ponderador",
        "ponderador_exacto",
        "ponderador_fuente_ola_tabla",
        "ponderador_fuente",
        "ponderador_ola",
        "ponderador_scope_tipo",
        "ponderador_scope_id",
    }
)
OPTIONAL_CITABLE_FIELDS = frozenset(
    {
        "unidad_medida",
        "rango_valido",
        "operacion_estimador",
        "no_aplica_ponderador_documentado",
    }
)
ALL_CITABLE_FIELDS = BASE_CITABLE_FIELDS | OPTIONAL_CITABLE_FIELDS


class AutoridadSemanticaError(ValueError):
    """Fallo cerrado del contrato de autoridad semantica."""


@dataclass(frozen=True, order=True)
class AuthorityKey:
    representacion_id: str
    scope_tipo: str
    scope_id: str
    variable: str

    def as_dict(self) -> dict[str, str]:
        return {
            "representacion_id": self.representacion_id,
            "scope_tipo": self.scope_tipo,
            "scope_id": self.scope_id,
            "variable": self.variable,
        }


def _text(value: Any) -> str:
    return str(value or "").strip()


def _canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def authority_key_from_e2(record: Mapping[str, Any]) -> AuthorityKey:
    """Construye la clave material; el padre significativo tiene precedencia."""

    representation = _text(record.get("representacion_id"))
    variable = _text(record.get("nombre"))
    parent = _text(record.get("objeto_padre_id"))
    table = _text(record.get("tabla"))
    if not representation or not variable:
        raise AutoridadSemanticaError("CLAVE_E2_IDENTIDAD_INCOMPLETA")
    if is_meaningful(parent):
        return AuthorityKey(representation, "OBJETO_PADRE_ID", parent, variable)
    if is_meaningful(table):
        return AuthorityKey(representation, "TABLA", table, variable)
    raise AutoridadSemanticaError(
        f"CLAVE_E2_SCOPE_AUSENTE:record_id={_text(record.get('record_id'))}"
    )


def authority_key_from_row(row: Mapping[str, Any]) -> AuthorityKey:
    scope_type = _text(row.get("scope_tipo"))
    if scope_type not in SCOPE_TYPES:
        raise AutoridadSemanticaError(f"AUTORIDAD_SCOPE_TIPO_INVALIDO:{scope_type}")
    key = AuthorityKey(
        _text(row.get("representacion_id")),
        scope_type,
        _text(row.get("scope_id")),
        _text(row.get("variable")),
    )
    if not all((key.representacion_id, key.scope_id, key.variable)):
        raise AutoridadSemanticaError("AUTORIDAD_CLAVE_INCOMPLETA")
    return key


def authority_id_from_row(row: Mapping[str, Any]) -> str:
    material = dict(row)
    material.pop("autoridad_id", None)
    digest = hashlib.sha256(_canonical_json(material).encode("utf-8")).hexdigest()
    return f"ASM-{digest[:24]}"


def with_authority_id(row: Mapping[str, Any]) -> dict[str, Any]:
    material = dict(row)
    material["autoridad_id"] = authority_id_from_row(material)
    return material


def canonical_authority_line(row: Mapping[str, Any]) -> str:
    return _canonical_json(dict(row))


def _require_string(row: Mapping[str, Any], field: str) -> str:
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AutoridadSemanticaError(f"AUTORIDAD_CAMPO_TEXTO_INVALIDO:{field}")
    return value.strip()


def _validate_sha(value: Any, label: str) -> None:
    text = _text(value).lower()
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise AutoridadSemanticaError(f"AUTORIDAD_SHA256_INVALIDO:{label}")


def _validate_prefixed_hex(value: Any, prefix: str, label: str, length: int = 64) -> None:
    text = _text(value)
    suffix = text.removeprefix(prefix)
    if (
        not text.startswith(prefix)
        or len(suffix) != length
        or any(character not in "0123456789abcdef" for character in suffix)
    ):
        raise AutoridadSemanticaError(f"AUTORIDAD_IDENTIFICADOR_INVALIDO:{label}")


def _validate_coding(row: Mapping[str, Any], kind: str) -> None:
    coding = row.get("codificacion")
    if not isinstance(coding, list) or not coding:
        raise AutoridadSemanticaError("AUTORIDAD_CODIFICACION_INVALIDA")
    codes: list[str] = []
    for item in coding:
        if not isinstance(item, dict) or set(item) != {"codigo", "etiqueta"}:
            raise AutoridadSemanticaError("AUTORIDAD_CODIFICACION_ITEM_INVALIDO")
        codes.append(_require_string(item, "codigo"))
        _require_string(item, "etiqueta")
    if len(codes) != len(set(codes)) or codes != sorted(codes):
        raise AutoridadSemanticaError("AUTORIDAD_CODIFICACION_NO_CANONICA")
    if kind == "BINARIA" and len(codes) != 2:
        raise AutoridadSemanticaError("AUTORIDAD_BINARIA_NO_TIENE_DOS_CODIGOS")

    missing = row.get("missing")
    if not isinstance(missing, dict) or set(missing) != {
        "codigos",
        "ausencia_documentada",
    }:
        raise AutoridadSemanticaError("AUTORIDAD_MISSING_INVALIDO")
    missing_codes = missing.get("codigos")
    if not isinstance(missing_codes, list) or any(
        not isinstance(code, str) or not code.strip() for code in missing_codes
    ):
        raise AutoridadSemanticaError("AUTORIDAD_MISSING_CODIGOS_INVALIDOS")
    if len(missing_codes) != len(set(missing_codes)) or missing_codes != sorted(missing_codes):
        raise AutoridadSemanticaError("AUTORIDAD_MISSING_NO_CANONICO")
    if set(codes) & set(missing_codes):
        raise AutoridadSemanticaError("AUTORIDAD_CODIGOS_VALIDOS_Y_MISSING_SOLAPADOS")
    absence_documented = missing.get("ausencia_documentada")
    if not isinstance(absence_documented, bool):
        raise AutoridadSemanticaError("AUTORIDAD_MISSING_AUSENCIA_NO_BOOLEANA")
    if not missing_codes and not absence_documented:
        raise AutoridadSemanticaError("AUTORIDAD_MISSING_VACIO_NO_DOCUMENTADO")


def _validate_citations(row: Mapping[str, Any]) -> None:
    citations = row.get("cita_procedencia")
    if not isinstance(citations, list) or not citations:
        raise AutoridadSemanticaError("AUTORIDAD_CITAS_AUSENTES")
    canonical_citations: list[str] = []
    covered: set[str] = set()
    for citation in citations:
        if not isinstance(citation, dict) or set(citation) != {
            "fuente_id",
            "ruta_o_uri",
            "sha256",
            "localizador",
            "campos_autorizados",
        }:
            raise AutoridadSemanticaError("AUTORIDAD_CITA_INVALIDA")
        for field in ("fuente_id", "ruta_o_uri", "localizador"):
            _require_string(citation, field)
        _validate_sha(citation.get("sha256"), _text(citation.get("fuente_id")))
        fields = citation.get("campos_autorizados")
        if (
            not isinstance(fields, list)
            or not fields
            or any(field not in ALL_CITABLE_FIELDS for field in fields)
            or len(fields) != len(set(fields))
            or fields != sorted(fields)
        ):
            raise AutoridadSemanticaError("AUTORIDAD_CITA_CAMPOS_INVALIDOS")
        covered.update(fields)
        canonical_citations.append(_canonical_json(citation))
    if canonical_citations != sorted(canonical_citations):
        raise AutoridadSemanticaError("AUTORIDAD_CITAS_NO_CANONICAS")

    required = set(BASE_CITABLE_FIELDS)
    for field in OPTIONAL_CITABLE_FIELDS:
        value = row.get(field)
        if value not in (None, "", False):
            required.add(field)
    missing = sorted(required - covered)
    if missing:
        raise AutoridadSemanticaError(
            "AUTORIDAD_CITAS_COBERTURA_INCOMPLETA:" + ",".join(missing)
        )


def validate_authority_row(row: Mapping[str, Any]) -> None:
    if not isinstance(row, Mapping):
        raise AutoridadSemanticaError("AUTORIDAD_FILA_NO_OBJETO")
    fields = set(row)
    if fields != ROW_FIELDS:
        missing = sorted(ROW_FIELDS - fields)
        extra = sorted(fields - ROW_FIELDS)
        raise AutoridadSemanticaError(
            "AUTORIDAD_CAMPOS_INVALIDOS:"
            f"faltan={','.join(missing)}:sobran={','.join(extra)}"
        )
    if row.get("schema_version") != SCHEMA_VERSION:
        raise AutoridadSemanticaError("AUTORIDAD_SCHEMA_VERSION_INVALIDA")
    key = authority_key_from_row(row)
    _validate_prefixed_hex(key.representacion_id, "REP-", "representacion_id")
    if key.scope_tipo == "OBJETO_PADRE_ID":
        _validate_prefixed_hex(key.scope_id, "OBJ-B2-", "scope_id")
    _validate_prefixed_hex(row.get("autoridad_id"), "ASM-", "autoridad_id", length=24)
    _validate_prefixed_hex(
        row.get("semilla_objeto_logico_id"), "OBJ-B2-", "semilla_objeto_logico_id"
    )
    _validate_prefixed_hex(row.get("e2_record_id"), "E2R-", "e2_record_id")
    for field in (
        "payload_id",
        "encuesta",
        "ola",
        "universo_poblacional",
        "unidad_observacion",
        "ponderador",
        "ponderador_fuente",
        "ponderador_ola",
        "ponderador_scope_tipo",
        "ponderador_scope_id",
    ):
        _require_string(row, field)
    _validate_sha(row.get("sha256_contenido"), "sha256_contenido")
    expected_id = authority_id_from_row(row)
    if row.get("autoridad_id") != expected_id:
        raise AutoridadSemanticaError(
            f"AUTORIDAD_ID_DIVERGENTE:{row.get('autoridad_id')}!={expected_id}"
        )

    kind = _text(row.get("tipo_estadistico"))
    if kind not in STATISTICAL_TYPES:
        raise AutoridadSemanticaError(f"AUTORIDAD_TIPO_ESTADISTICO_INVALIDO:{kind}")
    for field in (
        "respuesta_multiple",
        "categorias_excluyentes",
        "ponderador_exacto",
        "ponderador_fuente_ola_tabla",
        "no_aplica_ponderador_documentado",
    ):
        if not isinstance(row.get(field), bool):
            raise AutoridadSemanticaError(f"AUTORIDAD_CAMPO_NO_BOOLEANO:{field}")

    _validate_coding(row, kind)
    if kind in {"BINARIA", "CATEGORICA"}:
        if row.get("respuesta_multiple") or not row.get("categorias_excluyentes"):
            raise AutoridadSemanticaError("AUTORIDAD_CATEGORICA_NO_EXCLUYENTE")
    if kind == "NUMERICA_CONTINUA":
        if not isinstance(row.get("unidad_medida"), str) or not isinstance(
            row.get("rango_valido"), dict
        ):
            raise AutoridadSemanticaError("AUTORIDAD_CONTINUA_SIN_UNIDAD_O_RANGO")
    if kind in {"ADMINISTRATIVA", "CENSAL"}:
        if not isinstance(row.get("operacion_estimador"), str) or not _text(
            row.get("operacion_estimador")
        ):
            raise AutoridadSemanticaError("AUTORIDAD_ADMIN_SIN_OPERACION")
        if (
            _text(row.get("ponderador")).replace("_", " ").upper() != "NO APLICA"
            or not row.get("no_aplica_ponderador_documentado")
        ):
            raise AutoridadSemanticaError("AUTORIDAD_ADMIN_PONDERADOR_INVALIDO")
    else:
        if (
            not row.get("ponderador_exacto")
            or not row.get("ponderador_fuente_ola_tabla")
            or row.get("no_aplica_ponderador_documentado")
        ):
            raise AutoridadSemanticaError("AUTORIDAD_PONDERADOR_SCOPE_NO_EXACTO")
        if row.get("ponderador_ola") != row.get("ola"):
            raise AutoridadSemanticaError("AUTORIDAD_PONDERADOR_OLA_DIVERGENTE")
        scope_type = _text(row.get("ponderador_scope_tipo"))
        if scope_type not in SCOPE_TYPES:
            raise AutoridadSemanticaError("AUTORIDAD_PONDERADOR_SCOPE_TIPO_INVALIDO")
        if scope_type == "OBJETO_PADRE_ID":
            _validate_prefixed_hex(
                row.get("ponderador_scope_id"), "OBJ-B2-", "ponderador_scope_id"
            )
    _validate_citations(row)


class SemanticAuthorityIndex:
    """Indice O(1) con aserciones anti-deriva y control de orfandad."""

    def __init__(self, rows: Iterable[Mapping[str, Any]]):
        self._rows: dict[AuthorityKey, dict[str, Any]] = {}
        self._matched: set[AuthorityKey] = set()
        for raw in rows:
            row = dict(raw)
            validate_authority_row(row)
            key = authority_key_from_row(row)
            if key in self._rows:
                raise AutoridadSemanticaError(
                    "AUTORIDAD_CLAVE_DUPLICADA:" + _canonical_json(key.as_dict())
                )
            self._rows[key] = row
        if not self._rows:
            raise AutoridadSemanticaError("AUTORIDAD_ARCHIVO_VACIO")

    @property
    def row_count(self) -> int:
        return len(self._rows)

    @property
    def matched_count(self) -> int:
        return len(self._matched)

    def lookup(self, record: Mapping[str, Any]) -> dict[str, Any] | None:
        try:
            key = authority_key_from_e2(record)
        except AutoridadSemanticaError as exc:
            if str(exc).startswith("CLAVE_E2_SCOPE_AUSENTE:"):
                return None
            raise
        row = self._rows.get(key)
        if row is None:
            return None
        assertions = {
            "semilla_objeto_logico_id": _text(record.get("objeto_logico_id")),
            "e2_record_id": _text(record.get("record_id")),
            "payload_id": _text(record.get("payload_id")),
            "sha256_contenido": _text(record.get("sha256")).lower(),
        }
        divergent = [
            field for field, observed in assertions.items() if row.get(field) != observed
        ]
        if divergent:
            raise AutoridadSemanticaError(
                f"AUTORIDAD_IDENTIDAD_E2_DIVERGENTE:{row['autoridad_id']}:"
                + ",".join(divergent)
            )
        self._matched.add(key)
        return dict(row)

    def assert_no_orphans(self) -> None:
        orphan_ids = sorted(
            row["autoridad_id"]
            for key, row in self._rows.items()
            if key not in self._matched
        )
        if orphan_ids:
            raise AutoridadSemanticaError(
                "AUTORIDAD_HUERFANA:" + ",".join(orphan_ids)
            )


def load_semantic_authority(path: Path) -> SemanticAuthorityIndex:
    try:
        raw_lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise AutoridadSemanticaError(f"AUTORIDAD_ARCHIVO_AUSENTE:{path}") from exc
    if not raw_lines or any(not line.strip() for line in raw_lines):
        raise AutoridadSemanticaError(f"AUTORIDAD_ARCHIVO_VACIO_O_LINEA_VACIA:{path}")

    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(raw_lines, 1):
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AutoridadSemanticaError(
                f"AUTORIDAD_JSON_INVALIDO:linea={line_number}:{exc}"
            ) from exc
        if not isinstance(row, dict):
            raise AutoridadSemanticaError(
                f"AUTORIDAD_FILA_NO_OBJETO:linea={line_number}"
            )
        if line != canonical_authority_line(row):
            raise AutoridadSemanticaError(
                f"AUTORIDAD_JSON_NO_CANONICO:linea={line_number}"
            )
        rows.append(row)
    keys = [authority_key_from_row(row) for row in rows]
    if keys != sorted(keys):
        raise AutoridadSemanticaError("AUTORIDAD_FILAS_NO_ORDENADAS")
    return SemanticAuthorityIndex(rows)
