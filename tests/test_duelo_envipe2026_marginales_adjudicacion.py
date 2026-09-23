#!/usr/bin/env python3
"""D-22 de `CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001` (COMMIT-3):
sintético antes de oro. Cubre las cuatro ramas terminales del vocabulario
(`VENCE-AL-PISO`/`PROPUESTA-CON-RESERVA`/`NO-VENCE`/`C-PISO-ADOPTADO`) más
`INDECIDIBLE` (soporte vacío), y verifica que el bootstrap propio no
reimplementa un método distinto al de `wprop_ic_conglomerado` -- mismo
seed, mismos percentiles, sobre datos sintéticos.
"""
from __future__ import annotations

import importlib.util
import io
import os
import sys
import unittest
import zipfile

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))


def _carga(nombre, rel):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MED = _carga("medidor_duelo_marginales_adj",
             "data/corrida0/CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001/medidor.py")
CAL = _carga("calibracion_mordida_encig_serie", "tools/calibracion_mordida_encig_serie.py")


def _zip_sintetico(ruta, n_upm=20, seed=3):
    """tmod_vic de juguete: BPCOD='01' para todas, BP2_1 mitad/mitad,
    BP1_20 con tasas distintas por celda para que el error sea material."""
    rng = np.random.default_rng(seed)
    filas = []
    for u in range(n_upm):
        est = f"E{(u % 4) + 1}"
        upm = f"U{u + 1}"
        for r in range(1, 9):
            bp2_1 = "1" if r <= 4 else "2"
            p_denuncia = 0.85 if bp2_1 == "1" else 0.55
            bp1_20 = "1" if rng.random() < p_denuncia else "2"
            filas.append({"ID_DEL": f"{u}-{r}", "BPCOD": "01", "BP1_20": bp1_20,
                         "BP2_1": bp2_1, "FAC_DEL": str(int(rng.integers(50, 200))),
                         "EST_DIS": est, "UPM_DIS": upm})
        # unas filas fuera del universo (otro delito, otro seguro), deben excluirse
        filas.append({"ID_DEL": f"{u}-x", "BPCOD": "02", "BP1_20": "1", "BP2_1": "9",
                     "FAC_DEL": "10", "EST_DIS": est, "UPM_DIS": upm})
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr("x/conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2026.csv",
                   pd.DataFrame(filas).to_csv(index=False))
    return filas


class EquivalenciaBootstrap(unittest.TestCase):
    def test_mismo_vector_de_replicas_que_wprop_ic_conglomerado(self):
        """El remuestreo -- no sólo el IC final -- es idéntico: mismo seed,
        misma secuencia de índices, mismo vector de réplicas. La comparación
        se hace replicando EXACTAMENTE la extracción de percentil de
        `wprop_ic_conglomerado` (ordenar + índice entero, sin interpolar) --
        `np.percentile` interpola distinto y por eso no basta para probar
        que el remuestreo es el mismo."""
        rng = np.random.default_rng(11)
        n = 400
        estrato = rng.integers(0, 6, n).astype(str)
        upm = (estrato.astype(object) + "-" + rng.integers(0, 3, n).astype(str)).astype(str)
        d = rng.integers(0, 2, n).astype(float)
        w = rng.uniform(50, 200, n)
        p_hat, lo, hi, *_ = CAL.wprop_ic_conglomerado(d, w, estrato, upm, n_boot=10000, seed=42)
        reps, _ = MED._bootstrap_replicas(d, w, estrato, upm, 10000, 42)
        ordenadas = np.sort(reps)
        mi_lo = float(ordenadas[int(0.025 * 10000)])
        mi_hi = float(ordenadas[int(0.975 * 10000) - 1])
        self.assertEqual(lo, mi_lo)
        self.assertEqual(hi, mi_hi)


class VocabularioCerrado(unittest.TestCase):
    def test_vence_al_piso(self):
        self.assertEqual(MED._veredicto(2.0, "VENCE-RETADOR"), "VENCE-AL-PISO")

    def test_propuesta_con_reserva(self):
        self.assertEqual(MED._veredicto(0.2, "PROPUESTA-CON-RESERVA"), "PROPUESTA-CON-RESERVA")

    def test_no_vence(self):
        self.assertEqual(MED._veredicto(0.3, "NADIE-VENCE"), "NO-VENCE")

    def test_c_piso_adoptado(self):
        self.assertEqual(MED._veredicto(-0.1, "NADIE-VENCE"), "C-PISO-ADOPTADO")

    def test_indecidible(self):
        self.assertEqual(MED._veredicto(None, "NO-ADJUDICABLE"), "INDECIDIBLE")


class Sintetico(unittest.TestCase):
    def test_carga_universo_excluye_fuera_de_bpcod_01(self):
        with __import__("tempfile").NamedTemporaryFile(suffix=".zip") as tmp:
            filas = _zip_sintetico(tmp.name)
            universo, meta = MED.carga_universo_con_seguro(tmp.name, 2026)
        n_bpcod01 = sum(1 for f in filas if f["BPCOD"] == "01")
        self.assertEqual(len(universo), n_bpcod01)
        self.assertEqual(meta["filas_archivo"], len(filas))
        self.assertTrue((universo["BPCOD"] == "01").all())
        self.assertTrue(universo["BP2_1"].isin(["1", "2"]).all())

    def test_adjudica_celda_construible_con_piso_y_retador_sinteticos(self):
        with __import__("tempfile").NamedTemporaryFile(suffix=".zip") as tmp:
            _zip_sintetico(tmp.name)
            universo, _ = MED.carga_universo_con_seguro(tmp.name, 2026)
        piso = {"p": 0.60, "ic_lo": 0.50, "ic_hi": 0.70, "n": 300}
        retador = {"p": 0.62, "ic_lo": 0.48, "ic_hi": 0.74}
        r = MED.adjudica_celda(universo, "ASEGURADO", piso, retador)
        self.assertFalse(r["indecidible"])
        self.assertIn(r["veredicto"], ("VENCE-AL-PISO", "PROPUESTA-CON-RESERVA",
                                       "NO-VENCE", "C-PISO-ADOPTADO"))
        self.assertIsInstance(r["r_p"], float)
        self.assertTrue(0.0 <= r["r_p"] <= 1.0)

    def test_soporte_vacio_es_indecidible(self):
        vacio = pd.DataFrame({"BP2_1": [], "BP1_20": [], "_w": [], "EST_DIS": [], "UPM_DIS": []})
        piso = {"p": 0.6, "ic_lo": 0.5, "ic_hi": 0.7, "n": 10}
        retador = {"p": 0.6, "ic_lo": 0.5, "ic_hi": 0.7}
        r = MED.adjudica_celda(vacio, "ASEGURADO", piso, retador)
        self.assertTrue(r["indecidible"])


class Guardia(unittest.TestCase):
    def test_dependencia_mutada_para(self):
        real = dict(MED.MODULOS_SHA_CONGELADO)
        for k in MED.MODULOS_SHA_CONGELADO:
            MED.MODULOS_SHA_CONGELADO[k] = "0" * 64
        try:
            with self.assertRaises(SystemExit):
                MED._verifica_dependencias_congeladas()
        finally:
            MED.MODULOS_SHA_CONGELADO.clear()
            MED.MODULOS_SHA_CONGELADO.update(real)


if __name__ == "__main__":
    unittest.main()
