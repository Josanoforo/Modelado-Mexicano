#!/usr/bin/env python3
"""Test propio de tools/agrega_l_v1_0.py -- oro sintético + ramas terminales.

Cablea como huérfano vía `tools/ci_guardias.py --ejecuta-huerfanos` (el
encargo que lo trae, GEN2-L-DESDE-CAPTURAS-1, no toca `.github/workflows/
verify.yml` ni `tools/ci_guardias.py`: TUBERÍA en vuelo).

Defecto real que atrapa: un agregador de L escrito por segunda vez (o
tercera, para ENIF/ENVIPE/ENIGH) con una regla de inválidas distinta,
silenciosamente, porque nadie corrió el módulo compartido contra un caso
con respuesta conocida antes de usarlo en un duelo real.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from agrega_l_v1_0 import agregar_celda, extraer  # noqa: E402


class TestExtraer(unittest.TestCase):
    """La regla sellada (F5-completa-spec-v1_0.md §4), sin copiarla."""

    def test_valida(self):
        estado, valor, _ = extraer("algo de contexto\nESTIMACION_PUNTUAL=25%")
        self.assertEqual(estado, "VALIDA")
        self.assertAlmostEqual(valor, 0.25)

    def test_abstencion(self):
        estado, valor, _ = extraer("no lo sé con certeza\nABSTENCION")
        self.assertEqual(estado, "ABSTENCION")
        self.assertIsNone(valor)

    def test_malformada_fuera_de_rango(self):
        estado, valor, _ = extraer("ESTIMACION_PUNTUAL=150%")
        self.assertEqual(estado, "MALFORMADA")

    def test_malformada_texto_libre(self):
        estado, valor, _ = extraer("no puedo estimar esto con precisión")
        self.assertEqual(estado, "MALFORMADA")

    def test_error_tecnico_captura_no_ok(self):
        estado, valor, _ = extraer("ESTIMACION_PUNTUAL=10%", estado_captura="TIMEOUT")
        self.assertEqual(estado, "ERROR_TECNICO")


class TestAgregarCeldaOro(unittest.TestCase):
    """Caso oro con respuesta conocida a mano (TRA-M-02:L-solo, P6)."""

    def test_ocho_replicas_conocidas(self):
        # [0.12, 0.12, 0.15, 0.15, 0.15, 0.15, 0.17, 0.20] -> mediana=0.15
        estados = [("VALIDA", v) for v in (0.12, 0.12, 0.15, 0.15, 0.15, 0.15, 0.17, 0.20)]
        r = agregar_celda(estados, n_programadas=8, bootstrap_n=2000)
        self.assertEqual(r.n_validas, 8)
        self.assertAlmostEqual(r.mediana, 0.15)
        # |v-0.15| = [.03,.03,0,0,0,0,.02,.05] -> orden [0,0,0,0,.02,.03,.03,.05] -> mediana=(0+.02)/2
        self.assertAlmostEqual(r.dispersion_mad, 0.01)
        self.assertLessEqual(r.ic_lo, r.mediana)
        self.assertGreaterEqual(r.ic_hi, r.mediana)

    def test_determinismo_misma_semilla(self):
        estados = [("VALIDA", v) for v in (0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80)]
        r1 = agregar_celda(estados, n_programadas=8, bootstrap_seed=42, bootstrap_n=500)
        r2 = agregar_celda(estados, n_programadas=8, bootstrap_seed=42, bootstrap_n=500)
        self.assertEqual((r1.ic_lo, r1.ic_hi), (r2.ic_lo, r2.ic_hi))


class TestRamasTerminales(unittest.TestCase):
    """D-22 ampliada: celda con todas inválidas, celda con una sola válida."""

    def test_todas_las_replicas_invalidas(self):
        estados = [("ABSTENCION", None)] * 4 + [("MALFORMADA", None)] * 4
        r = agregar_celda(estados, n_programadas=8)
        self.assertEqual(r.n_validas, 0)
        self.assertIsNone(r.mediana)
        self.assertIsNone(r.dispersion_mad)
        self.assertIsNone(r.ic_lo)
        self.assertIsNone(r.ic_hi)
        self.assertEqual(r.n_abstenciones, 4)
        self.assertEqual(r.n_malformadas, 4)

    def test_una_sola_replica_valida(self):
        estados = [("VALIDA", 0.30)] + [("ABSTENCION", None)] * 7
        r = agregar_celda(estados, n_programadas=8)
        self.assertEqual(r.n_validas, 1)
        self.assertEqual(r.mediana, 0.30)
        self.assertEqual(r.dispersion_mad, 0.0)
        self.assertEqual(r.ic_lo, 0.30)
        self.assertEqual(r.ic_hi, 0.30)

    def test_pendientes_no_cuentan_como_ejecutadas(self):
        estados = [("VALIDA", 0.5), ("VALIDA", 0.6)] + [("PENDIENTE", None)] * 6
        r = agregar_celda(estados, n_programadas=8)
        self.assertEqual(r.n_ejecutadas, 2)
        self.assertEqual(r.n_validas, 2)


if __name__ == "__main__":
    unittest.main()
