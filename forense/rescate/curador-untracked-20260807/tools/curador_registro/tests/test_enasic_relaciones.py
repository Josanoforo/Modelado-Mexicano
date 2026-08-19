import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from curador import build_opening_bridge
from supervisor import material_conflicts


def write_tsv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


class EnasicRelacionesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mapa = Path(self.tmp.name)
        write_tsv(
            self.mapa / "mapa-maestro-fuentes.tsv",
            ["fuente_id", "nombres"],
            [{"fuente_id": "ENASIC", "nombres": "ENASIC 2022"}],
        )
        self.rows = [
            {
                "necesidad_cruda": "12 familismo_apoyo (no-ENIF)", "fuente_cruda": "ENASIC 2022",
                "estado_crudo": "EXISTE-NO-SATISFACE", "tabla_ref": "MAIN:abrir4:L19",
                "detalle_json": json.dumps({"variable_encontrada": "P7_12_3", "texto_del_reactivo": "responsabilidad de cuidar"}),
            },
            {
                "necesidad_cruda": "13 familismo_obligacion", "fuente_cruda": "ENASIC 2022",
                "estado_crudo": "EXISTE-SATISFACE", "tabla_ref": "MAIN:abrir4:L20",
                "detalle_json": json.dumps({"variable_encontrada": "P7_12_7", "texto_del_reactivo": "deber de cuidar"}),
            },
        ]

    def tearDown(self):
        self.tmp.cleanup()

    def bridge(self, rows):
        write_tsv(
            self.mapa / "mapa-maestro-aperturas.tsv",
            ["necesidad_cruda", "fuente_cruda", "estado_crudo", "tabla_ref", "detalle_json"],
            rows,
        )
        return build_opening_bridge(self.mapa)

    def test_reactivos_alimentan_solo_su_necesidad(self):
        rows = self.bridge(self.rows)
        by_variable = {r["variable"]: r["necesidad_id"] for r in rows}
        self.assertEqual(by_variable["P7_12_3"], "N12")
        self.assertEqual(by_variable["P7_12_7"], "N13")
        self.assertNotIn("N17", by_variable.values())

    def test_reordenar_filas_no_cambia_relaciones(self):
        normal = {(r["necesidad_id"], r["fuente_id_canonico"], r["objeto_evidencia_id"]) for r in self.bridge(self.rows)}
        reversed_rows = {(r["necesidad_id"], r["fuente_id_canonico"], r["objeto_evidencia_id"]) for r in self.bridge(list(reversed(self.rows)))}
        self.assertEqual(normal, reversed_rows)

    def test_necesidades_distintas_de_enasic_no_conflictuan(self):
        base = {
            "fuente_id_canonico": "ENASIC", "evidencia_ref": "MAIN:abrir4", "evidencia_textual_breve": "reactivo",
            "conflicto_material": "NO", "nota": "",
        }
        rows = [
            {**base, "necesidad_id": "N12", "objeto_evidencia_id": "OE-P7_12_3", "clasificacion_relacion": "NEGATIVA", "capa4_apertura_mapeo": "EXISTE-NO-SATISFACE"},
            {**base, "necesidad_id": "N13", "objeto_evidencia_id": "OE-P7_12_7", "clasificacion_relacion": "CONFIRMADA", "capa4_apertura_mapeo": "EXISTE-SATISFACE"},
        ]
        self.assertEqual(material_conflicts(rows), [])


if __name__ == "__main__":
    unittest.main()
