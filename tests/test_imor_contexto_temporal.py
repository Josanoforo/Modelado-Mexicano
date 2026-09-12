"""Pruebas dirigidas del análisis IMOR por régimen."""
import csv
import importlib.util
import json
import math
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "data/corrida0/CALC-IMOR-CONTEXTO-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_imor_contexto", MODULE_PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class ImorContextoTemporalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = ROOT / "data/fuentes-financieras-20/banxico-imor-consumo-mensual.csv"
        cls.levels, cls.changes, cls.summaries = M.calcular(source.read_bytes())

    def test_llaves_corte_y_conteos(self):
        self.assertEqual(len(self.levels), 615)
        self.assertEqual(len({(r["fecha"], r["producto"]) for r in self.levels}), 615)
        self.assertEqual(len({r["fecha"] for r in self.levels}), 123)
        self.assertEqual(sum(r["cambio_mensual_pp_num"] is not None for r in self.changes), 605)
        self.assertEqual(sum(r["cambio_interanual_pp_num"] is not None for r in self.changes), 495)

    def test_no_cruza_regimen(self):
        starts = [r for r in self.changes if r["fecha"] in {"2016-01", "2022-01"}]
        self.assertEqual(len(starts), 10)
        self.assertTrue(all(r["cambio_mensual_pp_num"] is None for r in starts))
        self.assertTrue(all(r["cambio_interanual_pp_num"] is None for r in starts))

    def test_operaciones_de_referencia(self):
        by_key = {(r["fecha"], r["producto"]): r for r in self.changes}
        self.assertTrue(math.isclose(by_key[("2022-02", "Tarjetas de crédito")]["cambio_mensual_pp_num"], 0.14, abs_tol=1e-12))
        self.assertTrue(math.isclose(by_key[("2023-01", "Tarjetas de crédito")]["cambio_interanual_pp_num"], 0.22, abs_tol=1e-12))
        summaries = {(r["producto"], r["regimen_definicion"]): r for r in self.summaries}
        self.assertTrue(math.isclose(summaries[("Consumo total", "PRE_IFRS9_CARTERA_VENCIDA")]["media_temporal_pct"], 4.210833333333333, abs_tol=1e-12))
        self.assertEqual(summaries[("ABCD", "IFRS9_ETAPA_3")]["fechas_minimo"], "2024-05")

    def test_tablas_conservan_vacios_y_unidades(self):
        path = ROOT / "data/analisis-imor-contexto-temporal/cambios-mensuales-e-interanuales.csv"
        with path.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        jan22 = [r for r in rows if r["fecha"] == "2022-01"]
        self.assertEqual(len(jan22), 5)
        self.assertTrue(all(r["cambio_mensual_pp"] == "" and r["cambio_interanual_pp"] == "" for r in jan22))
        self.assertIn("cambio_mensual_rel_pct", rows[0])

    def test_figuras_declaran_regimen_unidad_y_fuente(self):
        for name in ("niveles-por-producto-y-regimen.svg", "cambios-mensuales-por-producto-y-regimen.svg"):
            root = ET.parse(ROOT / "data/analisis-imor-contexto-temporal" / name).getroot()
            text = " ".join("".join(node.itertext()) for node in root.iter())
            self.assertIn("PRE_IFRS9_CARTERA_VENCIDA", text)
            self.assertIn("IFRS9_ETAPA_3", text)
            self.assertIn("Banxico", text)
            self.assertIn("no R16 CNBV", text)

    def test_sello_y_control_independiente(self):
        evidence = json.loads((ROOT / "data/corrida0/CALC-IMOR-CONTEXTO-0001/control-independiente.json").read_text())
        self.assertEqual(evidence["estado"], "VALIDACION-INDEPENDIENTE-COINCIDE")
        self.assertEqual(evidence["controles"]["cambios_mensuales"], 605)


if __name__ == "__main__":
    unittest.main()
