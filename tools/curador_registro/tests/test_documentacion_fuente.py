from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.curador_registro.prepare_production import FORBIDDEN, canonical_analyst_spec, sha256
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


class DocumentacionFuenteBlindedFromAnalystTests(unittest.TestCase):
    """G3: documentacion_fuente es metadato de supervisión -- el analista
    cegado no lo necesita, así que prepare_production.py lo excluye del
    input opaco aunque el expediente maestro lo declare y valide.

    Maestra sintética, autocontenida (microdato/evidencia propios en un
    tempdir con su hash real) -- no depende de data/raw, que este acto
    no descarga ni requiere."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        microdato = root / "microdato.csv"
        microdato.write_bytes(b"col_a,col_b\n1,2\n")
        evidencia = root / "evidencia-neutral.md"
        evidencia.write_bytes(b"# evidencia neutral de prueba\n")

        self.full = {
            "especificacion_id": "ESP-NUEVA-TEST-DOC-FUENTE",
            "estimando": "prueba", "poblacion": "prueba", "dominio": "TEST",
            "unidad_observacion": "persona", "variables": ["col_a"],
            "codificacion": {"col_a": [{"codigo": "1", "etiqueta": "Sí"}, {"codigo": "2", "etiqueta": "No"}]},
            "faltantes": {}, "direccion": "NO-APLICA", "ponderador": "NO-APLICA",
            "diseno_muestral": "NO-APLICA", "transformacion": "NO-APLICA",
            "incertidumbre": "NO-APLICA", "tipo_inferencia": "NO-APLICA",
            "criterio_parada": "NO-APLICA",
            "periodo_referencia_por_variable": {"col_a": "2026"},
            "edicion": "2026", "periodo_levantamiento": "2026",
            "input_path": str(microdato), "input_member": "NO-APLICA",
            "hash_microdato": sha256(microdato),
            "evidencia_ref": str(evidencia), "evidencia_neutral_ref": str(evidencia),
            "hash_evidencia_neutral": sha256(evidencia),
            "supervisor_link": {
                "relacion_id": "REL-test", "objeto_modelo_origen": "OBJ-test",
                "requiere_decision": "NO",
            },
            "documentacion_fuente": [
                {"url": "https://www.inegi.org.mx/rnm/index.php/catalog/922",
                 "fecha_consulta": "2026-08-12", "campos_resueltos": ["periodo_levantamiento"]},
            ],
        }
        self.snapshot_hash = "0" * 64
        self.baseline_hash = "0" * 64

    def test_documentacion_fuente_is_in_forbidden(self) -> None:
        self.assertIn("documentacion_fuente", FORBIDDEN)

    def test_blinded_spec_omits_documentacion_fuente_and_master_validates(self) -> None:
        sanitized = canonical_analyst_spec(self.full, self.snapshot_hash, self.baseline_hash, REPO)
        self.assertNotIn("documentacion_fuente", sanitized)
        self.assertEqual(
            [], documentacion_fuente_errors({"specifications": [self.full]}),
            "el expediente maestro, con documentacion_fuente declarado, valida sin error",
        )


if __name__ == "__main__":
    unittest.main()
