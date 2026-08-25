from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.curador_registro.autoridad_semantica_marco import (
    AutoridadSemanticaError,
    SemanticAuthorityIndex,
    authority_key_from_e2,
    canonical_authority_line,
    load_semantic_authority,
    validate_authority_row,
    with_authority_id,
)
from tools.curador_registro.tests.test_generar_marco import complete_authority
from tools.curador_registro.tests.test_marco_e2_adapter import e2_record


class AutoridadSemanticaMarcoTests(unittest.TestCase):
    def test_parent_scope_is_preferred_over_table(self) -> None:
        key = authority_key_from_e2(e2_record())
        self.assertEqual("OBJETO_PADRE_ID", key.scope_tipo)
        self.assertEqual("OBJ-B2-" + "7" * 64, key.scope_id)

    def test_table_scope_is_fallback_only_without_meaningful_parent(self) -> None:
        key = authority_key_from_e2(e2_record(objeto_padre_id="NO-APLICA"))
        self.assertEqual("TABLA", key.scope_tipo)
        self.assertEqual("hogar", key.scope_id)

    def test_seed_and_e2_ids_are_anti_drift_assertions(self) -> None:
        authority = SemanticAuthorityIndex([complete_authority()])
        with self.assertRaisesRegex(
            AutoridadSemanticaError, "AUTORIDAD_IDENTIDAD_E2_DIVERGENTE"
        ):
            authority.lookup(e2_record(record_id="E2R-" + "f" * 64))

    def test_duplicate_material_key_is_rejected(self) -> None:
        row = complete_authority()
        with self.assertRaisesRegex(
            AutoridadSemanticaError, "AUTORIDAD_CLAVE_DUPLICADA"
        ):
            SemanticAuthorityIndex([row, dict(row)])

    def test_missing_field_provenance_is_rejected(self) -> None:
        row = complete_authority()
        material = dict(row)
        material.pop("autoridad_id")
        citations = [dict(material["cita_procedencia"][0])]
        citations[0]["campos_autorizados"] = [
            field
            for field in citations[0]["campos_autorizados"]
            if field != "universo_poblacional"
        ]
        material["cita_procedencia"] = citations
        row = with_authority_id(material)
        with self.assertRaisesRegex(
            AutoridadSemanticaError, "AUTORIDAD_CITAS_COBERTURA_INCOMPLETA"
        ):
            validate_authority_row(row)

    def test_empty_and_noncanonical_files_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "authority.jsonl"
            path.write_text("", encoding="utf-8")
            with self.assertRaisesRegex(AutoridadSemanticaError, "ARCHIVO_VACIO"):
                load_semantic_authority(path)
            path.write_text(str(complete_authority()) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(AutoridadSemanticaError, "JSON_INVALIDO"):
                load_semantic_authority(path)

    def test_canonical_file_loads_and_orphan_check_fails_closed(self) -> None:
        row = complete_authority()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "authority.jsonl"
            path.write_text(canonical_authority_line(row) + "\n", encoding="utf-8")
            authority = load_semantic_authority(path)
        self.assertEqual(1, authority.row_count)
        with self.assertRaisesRegex(AutoridadSemanticaError, "AUTORIDAD_HUERFANA"):
            authority.assert_no_orphans()

    def test_real_product_is_nonempty_and_valid(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        product = repo / "data/curacion-universo/autoridad-semantica-marco-v1_0.jsonl"
        schema_path = (
            repo
            / "data/curacion-universo/autoridad-semantica-marco-v1_0.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        for line in product.read_text(encoding="utf-8").splitlines():
            validator.validate(json.loads(line))
        authority = load_semantic_authority(product)
        self.assertEqual(1, authority.row_count)


if __name__ == "__main__":
    unittest.main()
