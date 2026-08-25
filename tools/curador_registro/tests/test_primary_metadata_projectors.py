from __future__ import annotations

import hashlib
import io
import json
import struct
import tempfile
import unittest
import zipfile
from pathlib import Path

import pandas as pd
from openpyxl import Workbook

from tools.curador_registro.autoridad_semantica_productiva import (
    _load_profiles,
    _specific_blocker,
    _universe_semantics_reason,
    _variable_universe,
)
from tools.curador_registro.primary_metadata_projectors import (
    DTA_PROJECTOR,
    NOT_PROJECTABLE,
    PROJECTED,
    SOURCE_NOT_PRESENT,
    MetadataProjection,
    PrimaryMetadataRegistry,
    _archive_suffix_candidates,
    _read_sav_dictionary,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PrimaryMetadataProjectorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def _registry(self, payload_id: str, path: Path) -> PrimaryMetadataRegistry:
        return PrimaryMetadataRegistry(
            corpus_root=self.root,
            manifest=[
                {
                    "id": payload_id,
                    "archivo": path.name,
                    "sha256": _sha256(path),
                }
            ],
            design_text="",
        )

    def test_dta_projector_reads_primary_labels_and_missing(self) -> None:
        path = self.root / "source.dta"
        pd.DataFrame({"Q1": [1, 2, 9]}).to_stata(
            path,
            write_index=False,
            variable_labels={"Q1": "Respuesta documentada"},
            value_labels={"Q1": {1: "Sí", 2: "No", 9: "No responde"}},
        )
        projection = self._registry("dta", path).project(
            {
                "payload_id": "dta",
                "objeto_tipo": "VARIABLE-DTA",
                "nombre": "Q1",
                "localizador": "",
            }
        )

        self.assertEqual(PROJECTED, projection.status)
        self.assertEqual(2, projection.code_label_pairs)
        self.assertEqual(1, projection.user_missing)
        self.assertIn("codigo_etiqueta", projection.recovered_fields)
        self.assertIn("user_missing", projection.recovered_fields)

    def test_xlsx_projector_uses_exact_sheet_and_structural_row(self) -> None:
        path = self.root / "dictionary.xlsx"
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "TABLA"
        sheet.append(["Variable", "Etiqueta", "Código", "Concepto"])
        sheet.append(["Q1", "Pregunta", 1, "Sí"])
        sheet.append([None, None, 2, "No"])
        workbook.save(path)
        workbook.close()
        projection = self._registry("xlsx", path).project(
            {
                "payload_id": "xlsx",
                "objeto_tipo": "VARIABLE-DICCIONARIO-XLSX",
                "objeto_padre_id": "SCOPE",
                "hoja": "TABLA",
                "nombre": "Q1",
                "categorias": ["1", "Sí", "2", "No"],
                "localizador": "hoja=TABLA#diccionario-fila=2:variable=Q1",
            }
        )

        self.assertEqual(PROJECTED, projection.status)
        self.assertIn("dominio_declarado", projection.recovered_fields)

    def test_csv_dictionary_projector_validates_row_catalog_and_title(self) -> None:
        path = self.root / "package.zip"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr(
                "pkg/diccionario_de_datos/dictionary.csv",
                "NOMBRE,NEMONICO,CATALOGO\nPregunta,Q1,Q1\n",
            )
            archive.writestr(
                "pkg/catalogos/Q1.csv",
                "CODIGO,ETIQUETA\n1,Sí\n2,No\n9,No responde\n",
            )
            archive.writestr("pkg/metadatos/meta.txt", "Title: Encuesta oficial\n")
        projection = self._registry("csv", path).project(
            {
                "payload_id": "csv",
                "objeto_tipo": "VARIABLE-DICCIONARIO",
                "nombre": "Q1",
                "localizador": (
                    "zip!/miembro=1:pkg/diccionario_de_datos/dictionary.csv"
                    "#/contenido-tabla#diccionario-fila=1:variable=Q1"
                ),
            }
        )

        self.assertEqual(PROJECTED, projection.status)
        self.assertEqual(2, projection.code_label_pairs)
        self.assertEqual(1, projection.user_missing)
        self.assertTrue(projection.survey_title_documented)

    def test_nested_zip_is_traversed_by_registered_ordinals(self) -> None:
        inner_buffer = io.BytesIO()
        with zipfile.ZipFile(inner_buffer, "w") as inner:
            inner.writestr("metadata.dta", b"primary")
        source = self.root / "outer.zip"
        with zipfile.ZipFile(source, "w") as outer:
            outer.writestr("inner.zip", inner_buffer.getvalue())

        candidates = _archive_suffix_candidates(source, ".dta")
        registry = self._registry("nested", source)
        name, payload = registry._zip_member(
            source,
            {
                "localizador": (
                    "zip!/miembro=1:inner.zip!/miembro=1:metadata.dta"
                )
            },
        )

        self.assertEqual(1, len(candidates))
        self.assertEqual(b"primary", candidates[0][1])
        self.assertIn("!/1:inner.zip!/1:metadata.dta", candidates[0][0])
        self.assertEqual("metadata.dta", name)
        self.assertEqual(b"primary", payload)

    def test_sav_dictionary_reads_value_labels_and_user_missing(self) -> None:
        path = self.root / "source.sav"
        header = bytearray(176)
        header[:4] = b"$FL2"
        header[64:68] = struct.pack("<i", 2)
        variable = (
            struct.pack("<i", 2)
            + struct.pack("<iiiii", 0, 1, 1, 0, 0)
            + b"Q1      "
            + struct.pack("<i", 8)
            + b"Pregunta"
            + struct.pack("<d", 9)
        )

        def label(code: float, text: bytes) -> bytes:
            body = struct.pack("<d", code) + bytes([len(text)]) + text
            return body + (b"\0" * (-(len(text) + 1) % 8))

        value_labels = (
            struct.pack("<ii", 3, 3)
            + label(1, b"Si")
            + label(2, b"No")
            + label(9, b"No responde")
            + struct.pack("<iii", 4, 1, 1)
        )
        path.write_bytes(
            bytes(header)
            + variable
            + value_labels
            + struct.pack("<ii", 999, 0)
        )

        metadata = _read_sav_dictionary(path)["Q1"]

        self.assertEqual([("1", "Si"), ("2", "No")], metadata["pairs"])
        self.assertEqual(["9"], metadata["missing"])

    def test_blocker_depends_on_projection_result_not_object_type(self) -> None:
        record = {"objeto_tipo": "VARIABLE-DTA"}
        unavailable = MetadataProjection(
            projector=DTA_PROJECTOR,
            status=SOURCE_NOT_PRESENT,
            technical_reason="ARTEFACTO_PRIMARIO_AUSENTE:raiz=descargas_mx",
        )
        unreadable = MetadataProjection(
            projector=DTA_PROJECTOR,
            status=NOT_PROJECTABLE,
            technical_reason="FORMATO_NO_SOPORTADO",
        )
        projected = MetadataProjection(
            projector=DTA_PROJECTOR,
            status=PROJECTED,
            recovered_fields=("tipo_almacenamiento",),
        )

        self.assertEqual(
            "FUENTE_PRIMARIA_NO_PRESENTE",
            _specific_blocker(record, projection=unavailable),
        )
        self.assertEqual(
            "METADATA_PRIMARIA_NO_PROYECTABLE",
            _specific_blocker(record, projection=unreadable),
        )
        self.assertEqual(
            "TIPO_ESTADISTICO_NO_DOCUMENTADO",
            _specific_blocker(record, projection=projected),
        )

    def test_mociba_profile_fails_closed_for_eligibility_variable(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        profiles = _load_profiles(
            repo
            / "data/curacion-universo/perfiles-autoridad-semantica-marco-v1_0.json"
        )["profiles_by_payload"]
        table = profiles["mociba2024_fd_xlsx"]["tables"]["TMociba"]

        self.assertEqual(
            "UNIVERSO_REACTIVO_NO_RESUELTO",
            _universe_semantics_reason(table, "P7_1"),
        )
        self.assertIsNone(_variable_universe(table, "P7_1"))
        population, unit = _variable_universe(table, "P1") or ("", "")
        self.assertIn("usaron internet", population)
        self.assertIn("tres meses", population)
        self.assertIn("persona de 12 años o más", unit)
        citations = json.dumps(table["context_citations"], ensure_ascii=False)
        self.assertIn("presentacionData.js", citations)
        self.assertNotIn("inventario-fuentes-tecnologia-digital-mexico.md", citations)


if __name__ == "__main__":
    unittest.main()
