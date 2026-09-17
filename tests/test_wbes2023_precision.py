"""Guardias sintéticas de CALC-WBES2023-PRECISION-0001."""
from __future__ import annotations

import csv
import importlib.util
import io
import os
import unittest
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-WBES2023-PRECISION-0001"
SPEC = importlib.util.spec_from_file_location("wbes2023_precision", CALC / "medidor.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MOD)


def frame_for_design(rows):
    defaults = {column: 2 for column in MOD.PARENT.REQUIRED_COLUMNS}
    defaults[MOD.PARENT.IDENTIFIER] = 0
    defaults[MOD.PARENT.WEIGHT] = 1.0
    defaults[MOD.PARENT.SIZE] = 1
    out = []
    for index, values in enumerate(rows):
        row = dict(defaults)
        row[MOD.PARENT.IDENTIFIER] = index + 1
        row.update(values)
        out.append(row)
    return pd.DataFrame(out)


class Wbes2023PrecisionTest(unittest.TestCase):
    def test_razon_ponderada_y_varianza_analitica(self):
        frame = frame_for_design([
            {"strata": "A", "wmedian": 1.0},
            {"strata": "A", "wmedian": 3.0},
            {"strata": "B", "wmedian": 2.0},
            {"strata": "B", "wmedian": 4.0},
        ])
        x = pd.Series([1.0, 1.0, 1.0, 1.0])
        y = pd.Series([1.0, 0.0, 1.0, 0.0])
        point = 3.0 / 10.0
        variance, profile = MOD.linearized_variance(
            frame, x, y, point, 10.0, "SINGLETON-CERTEZA"
        )
        z = [0.07, -0.09, 0.14, -0.12]
        expected = 2 * ((z[0] - sum(z[:2]) / 2) ** 2 + (z[1] - sum(z[:2]) / 2) ** 2)
        expected += 2 * ((z[2] - sum(z[2:]) / 2) ** 2 + (z[3] - sum(z[2:]) / 2) ** 2)
        self.assertAlmostEqual(variance, expected)
        self.assertEqual(profile["df"], 2)
        self.assertNotAlmostEqual(point, 2 / 4)  # mismo n, pesos desiguales gobiernan

    def test_dominio_conserva_contribuciones_cero(self):
        frame = frame_for_design([
            {"strata": "A", "wmedian": 2.0},
            {"strata": "A", "wmedian": 4.0},
            {"strata": "B", "wmedian": 1.0},
            {"strata": "B", "wmedian": 3.0},
        ])
        x = pd.Series([1.0, 0.0, 1.0, 0.0])
        y = pd.Series([1.0, 0.0, 0.0, 0.0])
        _, profile = MOD.linearized_variance(frame, x, y, 2 / 3, 3.0, "SINGLETON-CERTEZA")
        self.assertEqual(profile["n_units"], 4)
        self.assertEqual(profile["n_strata"], 2)
        self.assertEqual(profile["n_filter_created_singleton"], 2)
        self.assertEqual(profile["n_singleton"], 0)

    def test_singleton_real_y_creado_por_filtro_no_se_confunden(self):
        frame = frame_for_design([
            {"strata": "A"},
            {"strata": "B"},
            {"strata": "B"},
            {"strata": "C"},
            {"strata": "C"},
        ])
        classified = pd.Series([True, True, False, False, False])
        profile = MOD._stratum_profile(frame, classified)
        self.assertEqual(profile["n_singleton"], 1)
        self.assertEqual(profile["n_singleton_with_domain"], 1)
        self.assertEqual(profile["n_filter_created_singleton"], 1)

    def test_average_no_se_elige_por_ser_menor(self):
        frame = frame_for_design([
            {"strata": "A"}, {"strata": "B"}, {"strata": "B"},
        ])
        x = pd.Series([0.0, 1.0, 1.0])
        y = pd.Series([0.0, 1.0, 0.0])
        v_zero, _ = MOD.linearized_variance(frame, x, y, 0.5, 2.0, "SINGLETON-CERTEZA")
        v_average, _ = MOD.linearized_variance(frame, x, y, 0.5, 2.0, "SINGLETON-AVERAGE")
        self.assertAlmostEqual(v_average, 2 * v_zero)

    def test_rechaza_campo_diseno_ausente(self):
        frame = frame_for_design([{"strata": "A"}, {"strata": "B"}]).drop(columns="strata")
        with self.assertRaisesRegex(ValueError, "CAMPO-DISENO-AUSENTE:strata"):
            MOD.validate_design(frame)

    def test_frontera_no_produce_ic_cero(self):
        lo, hi, status = MOD.logit_interval(0.0, 0.0, 10)
        self.assertIsNone(lo)
        self.assertIsNone(hi)
        self.assertEqual(status, "PRECISION-NO-ESTIMABLE-FRONTERA")

    def test_limites_faltantes_no_se_rotulan_ic(self):
        self.assertNotIn("limite_inferior_faltantes", "ic95_inferior")
        self.assertEqual(MOD.PRECISION_TYPE, "IC-APROXIMADO-CONDICIONAL-A-SUPUESTOS")

    @unittest.skipUnless(os.environ.get("WBES_REAL") == "1", "integración real sólo después del COMMIT 1")
    def test_reproduce_cinco_puntos_y_denominadores_del_padre(self):
        with zipfile.ZipFile(ROOT / "data/raw/WBES_Mexico2023_Data.zip") as zf:
            frame = pd.read_stata(
                io.BytesIO(zf.read(MOD.MICRODATA_MEMBER)),
                columns=sorted(MOD.REQUIRED_COLUMNS), convert_categoricals=False,
            )
        rows = MOD.calculate(frame)
        certainty = {row["dominio_id"]: row for row in rows if row["escenario_singleton"] == "SINGLETON-CERTEZA"}
        parent_path = ROOT / "forense/analisis/wbes2023-descriptiva-1/wbes2023-solicitud-expectativa-pago-informal.csv"
        with parent_path.open(encoding="utf-8", newline="") as handle:
            parent = {
                row["dominio_id"]: row for row in csv.DictReader(handle)
                if row["indicador_id"] == "COMPUESTO-SEIS-INTERACCIONES"
            }
        self.assertEqual(set(certainty), set(parent))
        for domain_id in parent:
            self.assertAlmostEqual(certainty[domain_id]["punto_sucesor"], float(parent[domain_id]["proporcion_observada"]), places=12)
            self.assertEqual(certainty[domain_id]["n_clasificables"], int(parent[domain_id]["n_denominador_observado"]))


if __name__ == "__main__":
    unittest.main()
