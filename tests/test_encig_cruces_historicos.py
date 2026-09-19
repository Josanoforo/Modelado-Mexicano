#!/usr/bin/env python3
"""Pruebas sintéticas del contrato de cruces ENCIG."""
from __future__ import annotations

import importlib.util
import tempfile
import zipfile
from pathlib import Path
import unittest

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/encig_cruces_historicos.py"
SPEC = importlib.util.spec_from_file_location("encig_cruces", PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


class CrucesHistoricosTest(unittest.TestCase):
    def test_personas_evento_y_no_evento_pueden_solaparse(self):
        frame = pd.DataFrame({"ID_PER": ["A", "A", "B"], "_y": [0.0, 1.0, 1.0]})
        persons, event, no_event, overlap = M._people_counts(frame)
        self.assertEqual((persons, event, no_event, overlap), (2, 2, 1, 1))

    def test_incertidumbre_no_condiciona_en_replicas_degeneradas(self):
        ee, lo, hi, valid = M._summary(0.5, np.array([0.4, np.nan, 0.6]))
        self.assertEqual(valid, 2)
        self.assertIsNone(ee)
        self.assertIsNone(lo)
        self.assertIsNone(hi)

    def test_delta_usa_cuatro_terminos_en_la_misma_replica(self):
        # Aditividad exacta en logit: cuatro probabilidades .5 => delta=0.
        values = np.array([0.5, 0.5, 0.5, 0.5])
        delta = M._logit(values[:1])[0] - M._logit(values[1:2])[0]
        delta -= M._logit(values[2:3])[0]
        delta += M._logit(values[3:])[0]
        self.assertAlmostEqual(delta, 0.0)

    def test_seleccion_para_si_un_cruce_es_incoherente(self):
        prefix = M._prefix("2023")
        outputs = {}
        for cross, _a, _b in M.CROSSES:
            outputs[f"{prefix}-{cross}-COHERENCIA"] = "COHERENTE"
            outputs[f"{prefix}-{cross}-ELEGIBLE"] = "SI"
            outputs[f"{prefix}-{cross}-PUNTAJE"] = 1.0
        outputs[f"{prefix}-SEXO-EDAD-COHERENCIA"] = "PARO-COHERENCIA-UNIVERSO"
        M._selection_2023(outputs, prefix)
        self.assertEqual(outputs[f"{prefix}-SELECCION-RESULTADO"],
                         "SELECCION-PENDIENTE-DE-DEFINICION")

    def test_declaraciones_son_unicas_y_guardia_no_menciona_2025(self):
        for wave in ("2021", "2023"):
            ids = [row[0] for row in M.declared_results(wave)]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertFalse(any("2025" in result_id for result_id in ids))

    def test_guardia_rechaza_payload_2025_y_alias_no_autorizado(self):
        contract = {"parametros": {"payload_id": "encig2021_csv"}}
        with self.assertRaisesRegex(RuntimeError, "GUARDIA-ENCIG2025"):
            M._guard_inputs({"encig25_base_datos_csv": {}}, contract)
        with self.assertRaisesRegex(RuntimeError, "GUARDIA-ALLOWLIST"):
            M._guard_inputs({"encig2023_datosabiertos_csv": {}}, contract)
        M._guard_inputs({"encig2021_csv": {}}, contract)

    def test_lector_elige_conjunto_y_no_diccionario(self):
        with tempfile.TemporaryDirectory() as directory:
            archive = Path(directory) / "fixture.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("x/conjunto_de_datos/conjunto_de_datos_encig2021_04_sec_7.csv", "A,B\n1,dato\n")
                zf.writestr("x/diccionario_de_datos/diccionario_de_datos_encig2021_04_sec_7.csv", "A,B\n2,diccionario\n")
            frame = M._member_csv(str(archive), "encig2021_04_sec_7.csv", ["A", "B"])
        self.assertEqual(frame.iloc[0].to_dict(), {"A": "1", "B": "dato"})


if __name__ == "__main__":
    unittest.main()
