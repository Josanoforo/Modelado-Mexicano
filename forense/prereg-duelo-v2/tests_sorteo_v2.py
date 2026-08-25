#!/usr/bin/env python3
"""Pruebas de ``sorteo_v2.py`` contra los tres casos de §5 del reglamento
(``forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md``) más un test de
determinismo. No toca el congelado real ni corre sobre datos de producción:
cada caso construye su propio marco de ejemplo en memoria, tal como los
describe §5."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUTA_MODULO = ROOT / "forense" / "prereg-duelo-v2" / "sorteo_v2.py"
SPEC = importlib.util.spec_from_file_location("sorteo_v2", RUTA_MODULO)
SORTEO = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SORTEO
SPEC.loader.exec_module(SORTEO)

Fila = SORTEO.Fila


def _filas(estrato: str, publicadas: list[str], prefijo: str) -> list[Fila]:
    return [
        Fila(id=f"{prefijo}-{i:02d}", estrato=estrato, publicada=pub)
        for i, pub in enumerate(publicadas)
    ]


class TestCaso1Normal(unittest.TestCase):
    """§5 Caso 1 — cuota se cumple sin fallback, n_sorteo=12, cuota_max=2."""

    def setUp(self):
        self.marco = (
            _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "A")
            + _filas("dinero|P2|MEDIA", ["NO"] * 4 + ["SI"] * 2, "B")
            + _filas("trabajo|P1|MEDIA", ["NO"] * 3 + ["SI"] * 1, "C")
        )

    def test_asientos_hamilton(self):
        estratos = SORTEO._agrupar_por_estrato(self.marco)
        asientos = SORTEO.asignar_asientos_proporcional(estratos, 12)
        self.assertEqual(asientos["dinero|P2|DIFICIL"], 6)
        self.assertEqual(asientos["dinero|P2|MEDIA"], 4)
        self.assertEqual(asientos["trabajo|P1|MEDIA"], 2)

    def test_resultado_12_filas_cero_publicadas(self):
        r = SORTEO.sortear(self.marco, n_sorteo=12, cuota_max=2, semilla=1)
        self.assertEqual(len(r.resultado), 12)
        self.assertEqual(sum(1 for f in r.resultado if f.publicada == "SI"), 0)
        self.assertEqual(r.estratos_excluidos, [])
        self.assertEqual(r.skips, [])
        ids = [f.id for f in r.resultado]
        self.assertEqual(len(ids), len(set(ids)))  # sin reposición


class TestCaso2Infactibilidad(unittest.TestCase):
    """§5 Caso 2 — infactibilidad por estrato + fallback, n_sorteo=12, cuota_max=2."""

    def setUp(self):
        self.marco = (
            _filas("tiempo|P2|MEDIA", ["SI", "SI"], "T")
            + _filas("familia|P2|DIFICIL", ["SI"], "F")
            + _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "D")
        )

    def test_estratos_excluidos(self):
        r = SORTEO.sortear(self.marco, n_sorteo=12, cuota_max=2, semilla=7)
        self.assertCountEqual(r.estratos_excluidos, ["tiempo|P2|MEDIA", "familia|P2|DIFICIL"])

    def test_resultado_9_filas_7no_2si_3skip(self):
        r = SORTEO.sortear(self.marco, n_sorteo=12, cuota_max=2, semilla=7)
        self.assertEqual(len(r.resultado), 9)
        self.assertEqual(sum(1 for f in r.resultado if f.publicada == "NO"), 7)
        self.assertEqual(sum(1 for f in r.resultado if f.publicada == "SI"), 2)
        self.assertEqual(sum(s.faltan for s in r.skips), 3)
        self.assertTrue(all(f.estrato == "dinero|P2|DIFICIL" for f in r.resultado))

    def test_cuota_al_limite_no_excedida(self):
        r = SORTEO.sortear(self.marco, n_sorteo=12, cuota_max=2, semilla=7)
        self.assertLessEqual(sum(1 for f in r.resultado if f.publicada == "SI"), 2)


class TestCaso3LimiteCuota(unittest.TestCase):
    """§5 Caso 3 — caso límite de la cuota del 20%, n_sorteo=15, cuota_max=3."""

    def setUp(self):
        self.marco = (
            _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "A")
            + _filas("tramite|P0|MEDIA", ["NO"] * 2, "X")  # nota: P0 excluido del universo real, aquí solo NO extra
            + _filas("tiempo|P1|MEDIA", ["NO"] * 2, "Y")
            + _filas("civico|P1|MEDIA", ["NO"] * 1, "Z")
        )

    def test_total_elegible_igual_n_sorteo(self):
        r = SORTEO.sortear(self.marco, n_sorteo=15, cuota_max=3, semilla=13)
        self.assertEqual(len(r.resultado), 15)

    def test_cuota_saturada_exacta_valida(self):
        r = SORTEO.sortear(self.marco, n_sorteo=15, cuota_max=3, semilla=13)
        n_si = sum(1 for f in r.resultado if f.publicada == "SI")
        n_no = sum(1 for f in r.resultado if f.publicada == "NO")
        self.assertEqual(n_si, 3)
        self.assertEqual(n_no, 12)
        self.assertEqual(r.skips, [])
        self.assertEqual(r.estratos_excluidos, [])


class TestDeterminismo(unittest.TestCase):
    def test_misma_semilla_mismo_marco_mismo_resultado(self):
        marco = (
            _filas("dinero|P2|DIFICIL", ["NO"] * 7 + ["SI"] * 3, "A")
            + _filas("dinero|P2|MEDIA", ["NO"] * 4 + ["SI"] * 2, "B")
            + _filas("trabajo|P1|MEDIA", ["NO"] * 3 + ["SI"] * 1, "C")
        )
        r1 = SORTEO.sortear(marco, n_sorteo=12, cuota_max=2, semilla=42)
        r2 = SORTEO.sortear(marco, n_sorteo=12, cuota_max=2, semilla=42)
        self.assertEqual([f.id for f in r1.resultado], [f.id for f in r2.resultado])
        self.assertEqual(r1.skips, r2.skips)
        self.assertEqual(r1.estratos_excluidos, r2.estratos_excluidos)


class TestCargaCongelado(unittest.TestCase):
    def test_universo_50_filas(self):
        marco = SORTEO.cargar_marco()
        self.assertEqual(len(marco), 50)
        self.assertTrue(all(f.publicada in ("SI", "NO") for f in marco))

    def test_orden_estable_por_id(self):
        marco = SORTEO.cargar_marco()
        ids = [f.id for f in marco]
        self.assertEqual(ids, sorted(ids))


class TestSemillaDesdeSha(unittest.TestCase):
    def test_deterministico_y_entero_no_negativo(self):
        s1 = SORTEO.semilla_desde_sha_merge("a" * 40)
        s2 = SORTEO.semilla_desde_sha_merge("a" * 40)
        self.assertEqual(s1, s2)
        self.assertIsInstance(s1, int)
        self.assertGreaterEqual(s1, 0)

    def test_distinto_sha_distinta_semilla(self):
        s1 = SORTEO.semilla_desde_sha_merge("a" * 40)
        s2 = SORTEO.semilla_desde_sha_merge("b" * 40)
        self.assertNotEqual(s1, s2)


if __name__ == "__main__":
    unittest.main()
