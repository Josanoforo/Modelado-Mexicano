from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.curador_registro.validate import (
    ESPECIFICACIONES_SELLADAS_SIN_DOCUMENTACION_FUENTE,
    documentacion_fuente_errors,
)

REPO = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO / "tools" / "curador_registro" / "schemas" / "production-spec.schema.json"


class DocumentacionFuenteSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.field_schema = {
            "type": "object",
            "properties": {"documentacion_fuente": schema["properties"]["documentacion_fuente"]},
            "required": ["documentacion_fuente"],
            "additionalProperties": False,
        }

    def errors(self, payload: dict) -> list:
        return list(Draft202012Validator(self.field_schema).iter_errors(payload))

    def test_valid_entry_is_accepted(self) -> None:
        payload = {"documentacion_fuente": [
            {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
             "fecha_consulta": "2026-08-12", "campos_resueltos": ["periodo_levantamiento"]},
        ]}
        self.assertEqual([], self.errors(payload))

    def test_missing_subfield_is_rejected(self) -> None:
        payload = {"documentacion_fuente": [
            {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
             "campos_resueltos": ["periodo_levantamiento"]},
        ]}
        self.assertTrue(self.errors(payload))

    def test_malformed_date_is_rejected(self) -> None:
        payload = {"documentacion_fuente": [
            {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
             "fecha_consulta": "12/ago/2026", "campos_resueltos": ["periodo_levantamiento"]},
        ]}
        self.assertTrue(self.errors(payload))

    def test_empty_array_is_rejected(self) -> None:
        self.assertTrue(self.errors({"documentacion_fuente": []}))

    def test_empty_campos_resueltos_is_rejected(self) -> None:
        payload = {"documentacion_fuente": [
            {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
             "fecha_consulta": "2026-08-12", "campos_resueltos": []},
        ]}
        self.assertTrue(self.errors(payload))

    def test_unknown_subfield_is_rejected(self) -> None:
        payload = {"documentacion_fuente": [
            {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
             "fecha_consulta": "2026-08-12", "campos_resueltos": ["periodo_levantamiento"],
             "extra": "no_declarado"},
        ]}
        self.assertTrue(self.errors(payload))


class DocumentacionFuenteRequirementTests(unittest.TestCase):
    def test_sealed_specs_are_exempt_without_the_field(self) -> None:
        config = {"specifications": [
            {"especificacion_id": spec_id}
            for spec_id in ESPECIFICACIONES_SELLADAS_SIN_DOCUMENTACION_FUENTE
        ]}
        self.assertEqual([], documentacion_fuente_errors(config))

    def test_new_spec_without_field_is_rejected(self) -> None:
        config = {"specifications": [{"especificacion_id": "ESP-NUEVA-TEST"}]}
        self.assertEqual(
            ["ESPECIFICACION_SIN_DOCUMENTACION_FUENTE:ESP-NUEVA-TEST"],
            documentacion_fuente_errors(config),
        )

    def test_new_spec_with_valid_field_is_accepted(self) -> None:
        config = {"specifications": [{
            "especificacion_id": "ESP-NUEVA-TEST",
            "documentacion_fuente": [
                {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
                 "fecha_consulta": "2026-08-12", "campos_resueltos": ["periodo_levantamiento"]},
            ],
        }]}
        self.assertEqual([], documentacion_fuente_errors(config))

    def test_empty_documentacion_fuente_on_new_spec_is_rejected(self) -> None:
        config = {"specifications": [
            {"especificacion_id": "ESP-NUEVA-TEST", "documentacion_fuente": []},
        ]}
        self.assertEqual(
            ["ESPECIFICACION_SIN_DOCUMENTACION_FUENTE:ESP-NUEVA-TEST"],
            documentacion_fuente_errors(config),
        )


if __name__ == "__main__":
    unittest.main()
