from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from tools.curador_registro.autoridad_semantica_productiva import (
    _response_semantics_reason,
    parse_inegi_fd_7col,
)


class AutoridadSemanticaProductivaTests(unittest.TestCase):
    def _descriptor(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name) / "fd.xlsx"
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "TABLA"
        header = [
            "Pregunta",
            "Nemónico",
            "Tipo",
            "Tamaño",
            "Códigos válidos",
            "Concepto",
        ]
        sheet.append(header)
        sheet.append(["1. Pregunta completa", "Q_OK", "N", 1, 1, "Sí"])
        sheet.append([None, None, None, None, 2, "No"])
        sheet.append([None, None, None, None, 9, "No responde"])
        # Los FD reales repiten cabecera entre secciones.
        sheet.append(header)
        sheet.append(["2. Pregunta filtrada", "Q_SKIP", "N", 1, 1, "Sí"])
        sheet.append([None, None, None, None, 2, "No"])
        sheet.append([None, None, None, None, "b", "Blanco por secuencia"])
        sheet.append(["3. Mención múltiple", "Q_MULTI", "N", 1, 0, "No se mencionó"])
        sheet.append([None, None, None, None, 1, "Sí se mencionó"])
        sheet.append(["4. No aplica explícito", "Q_NA", "N", 1, 1, "Sí"])
        sheet.append([None, None, None, None, 2, "No"])
        sheet.append([None, None, None, None, 3, "No aplica (solo opción 1 y 2)"])
        sheet.append(["5. Rango", "Q_RANGE", "N", 3, "1 - 100", "Valor"])
        workbook.save(path)
        workbook.close()
        return temporary, path

    def test_projector_separates_missing_skip_and_multiple_response(self) -> None:
        temporary, path = self._descriptor()
        self.addCleanup(temporary.cleanup)
        parsed = parse_inegi_fd_7col(path, ["TABLA"])

        self.assertIsNone(parsed[("TABLA", "Q_OK")].reason)
        self.assertEqual((("1", "Sí"), ("2", "No")), parsed[("TABLA", "Q_OK")].coding)
        self.assertEqual(("9",), parsed[("TABLA", "Q_OK")].missing)
        self.assertEqual(
            "UNIVERSO_REACTIVO_CONDICIONADO",
            parsed[("TABLA", "Q_SKIP")].reason,
        )
        self.assertEqual(
            "RESPUESTA_MULTIPLE_DOCUMENTADA",
            parsed[("TABLA", "Q_MULTI")].reason,
        )

    def test_no_aplica_is_fail_closed_and_ranges_are_not_categories(self) -> None:
        temporary, path = self._descriptor()
        self.addCleanup(temporary.cleanup)
        parsed = parse_inegi_fd_7col(path, ["TABLA"])

        self.assertEqual(
            "NO_APLICA_SEMANTICA_NO_RESUELTA",
            parsed[("TABLA", "Q_NA")].reason,
        )
        self.assertEqual(
            (
                ("1", "Sí"),
                ("2", "No"),
                ("3", "No aplica (solo opción 1 y 2)"),
            ),
            parsed[("TABLA", "Q_NA")].coding,
        )
        self.assertEqual((), parsed[("TABLA", "Q_NA")].missing)
        self.assertEqual(
            "DOMINIO_NO_ENUMERADO_O_SIN_ETIQUETA",
            parsed[("TABLA", "Q_RANGE")].reason,
        )

    def test_response_semantics_is_exact_per_variable(self) -> None:
        table = {
            # Estos defaults históricos no autorizan ninguna variable.
            "respuesta_multiple": False,
            "categorias_excluyentes": True,
            "response_semantics": {
                "scalar_exclusive_variables": ["Q_SCALAR"],
                "multiple_response_variables": ["Q_MULTI"],
                "unresolved_variables": ["Q_UNRESOLVED"],
            },
        }

        self.assertIsNone(_response_semantics_reason(table, "Q_SCALAR"))
        self.assertEqual(
            "RESPUESTA_MULTIPLE_DOCUMENTADA",
            _response_semantics_reason(table, "Q_MULTI"),
        )
        self.assertEqual(
            "EXCLUSIVIDAD_MULTIPLICIDAD_NO_RESUELTA",
            _response_semantics_reason(table, "Q_UNRESOLVED"),
        )
        self.assertEqual(
            "EXCLUSIVIDAD_MULTIPLICIDAD_NO_RESUELTA",
            _response_semantics_reason(table, "Q_NOT_DECLARED"),
        )

    def test_two_row_classes_header_is_a_reusable_projector(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        path = Path(temporary.name) / "fd-clases.xlsx"
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "TABLA"
        sheet.append(["Pregunta", "Mnemónico", "Clases", None])
        sheet.append([None, None, "Valor", "Etiqueta"])
        sheet.append(["Pregunta escalar", "Q_OK", 1, "Sí"])
        sheet.append([None, None, 2, "No"])
        sheet.append(["Pregunta filtrada", "Q_SKIP", 1, "Sí"])
        sheet.append([None, None, 2, "No"])
        sheet.append([None, None, "b", "Blanco por secuencia"])
        workbook.save(path)
        workbook.close()

        parsed = parse_inegi_fd_7col(path, ["TABLA"])
        self.assertEqual((("1", "Sí"), ("2", "No")), parsed[("TABLA", "Q_OK")].coding)
        self.assertIsNone(parsed[("TABLA", "Q_OK")].reason)
        self.assertEqual(
            "UNIVERSO_REACTIVO_CONDICIONADO",
            parsed[("TABLA", "Q_SKIP")].reason,
        )

    def test_structural_scalar_rule_still_honors_variable_exceptions(self) -> None:
        table = {
            "response_semantics": {
                "rule": "CAMPO_ESCALAR_CON_DOMINIO_ESTRUCTURADO",
                "scalar_exclusive_variables": [],
                "multiple_response_variables": ["Q_MULTI"],
                "unresolved_variables": ["Q_UNRESOLVED"],
            }
        }

        self.assertIsNone(_response_semantics_reason(table, "Q_SCALAR"))
        self.assertEqual(
            "RESPUESTA_MULTIPLE_DOCUMENTADA",
            _response_semantics_reason(table, "Q_MULTI"),
        )
        self.assertEqual(
            "EXCLUSIVIDAD_MULTIPLICIDAD_NO_RESUELTA",
            _response_semantics_reason(table, "Q_UNRESOLVED"),
        )


if __name__ == "__main__":
    unittest.main()
