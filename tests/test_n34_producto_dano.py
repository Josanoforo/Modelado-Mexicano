#!/usr/bin/env python3
from __future__ import annotations

import csv
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import extrae_n34_producto_dano as n34


class N34ProductoDanoTest(unittest.TestCase):
    def test_tabla_candidatos_separa_niveles_y_barreras(self):
        rows = list(csv.DictReader(io.StringIO(n34.tabla_candidatos())))
        self.assertEqual(len(rows), 6)
        por_id = {r["candidato"]: r for r in rows}
        self.assertEqual(
            por_id["Compartamos_AEJ_RCT"]["nivel"],
            "causal_acreditado_estrecho_con_reservas",
        )
        self.assertEqual(
            por_id["CFPB_Making_Ends_Meet_PUF"]["estado_bytes"],
            "NO_OBTENIDO_ACEPTACION_TOS_REQUERIDA",
        )
        self.assertNotIn("causal", por_id["Federal_Reserve_SHED_2025"]["decision"].lower())

    def test_parsea_tabla_cfpb_con_denominador(self):
        fixture = """
TABLE 3:      ORIGINATIONS AND DEFAULTS BY CREDIT SCORE CATEGORY, 2021-2022
 Score Categories Share of Originations Default Rate
 No Score 3.9% 4.1%
 Deep Subprime 45.0% 3.5%
 Subprime 16.0% 1.1%
 Near Prime 12.7% 0.8%
 Prime 13.2% 0.7%
 Super-prime 9.1% 0.8%
 Observations 892,668
Note: agregado oficial.
"""
        rows = n34._parsear_tabla_cfpb(fixture)
        self.assertEqual(len(rows), 6)
        self.assertEqual(rows[0]["observaciones_tabla"], 892668)
        self.assertEqual(rows[1]["tasa_default_pct"], "3.5")
        self.assertAlmostEqual(
            sum(float(r["participacion_originaciones_pct"]) for r in rows),
            99.9,
        )

    def test_validez_excluye_no_aplica_y_no_respuesta(self):
        self.assertTrue(n34._valido(0, set(range(11))))
        self.assertTrue(n34._valido(10, set(range(11))))
        self.assertFalse(n34._valido(-1, set(range(11))))
        self.assertFalse(n34._valido(99, set(range(11))))
        self.assertFalse(n34._valido(None, {1, 2, 3, 4}))

    def test_columna_xlsx(self):
        self.assertEqual(n34._columna_xlsx("A1"), 0)
        self.assertEqual(n34._columna_xlsx("Z9"), 25)
        self.assertEqual(n34._columna_xlsx("AA2"), 26)


if __name__ == "__main__":
    unittest.main()
