#!/usr/bin/env python3
"""Pruebas de ``sorteo_marco_m.py``: cargador propio (verificación de sha256
+ ``N_elegibles``) y la regla de tamaño de
``forense/notas/2026-08-31-marco-M-spec.md`` §e. No reimplementa ni vuelve
a probar ``sorteo_v2.sortear`` (ya cubierto por ``tests_sorteo_v2.py``);
solo prueba lo nuevo de este acto."""
from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUTA_MODULO = ROOT / "forense" / "prereg-duelo-v2" / "sorteo_marco_m.py"
SPEC = importlib.util.spec_from_file_location("sorteo_marco_m", RUTA_MODULO)
MARCO_M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MARCO_M
SPEC.loader.exec_module(MARCO_M)

Fila = MARCO_M.Fila


class TestReglaDeTamano(unittest.TestCase):
    """§e: N>=30 -> 15; 15<=N<30 -> ceil(N/2); N<15 -> n_sorteo=N (identidad)."""

    def test_n_grande(self):
        self.assertEqual(MARCO_M.regla_de_tamano(60), (15, 3))

    def test_n_frontera_30(self):
        self.assertEqual(MARCO_M.regla_de_tamano(30), (15, 3))

    def test_n_medio(self):
        self.assertEqual(MARCO_M.regla_de_tamano(19), (10, 2))

    def test_n_frontera_15(self):
        self.assertEqual(MARCO_M.regla_de_tamano(15), (8, 1))

    def test_n_pequeno_identidad(self):
        self.assertEqual(MARCO_M.regla_de_tamano(2), (2, 0))

    def test_n_cero(self):
        self.assertEqual(MARCO_M.regla_de_tamano(0), (0, 0))


class TestSortearMarcoMIdentidad(unittest.TestCase):
    """N < 15 -> identidad, sin invocar el PRNG (mismo resultado con
    cualquier semilla)."""

    def setUp(self):
        self.marco = [
            Fila(id="TRA-M-02", estrato="tramite|P1|MEDIA", publicada="NO"),
            Fila(id="TRA-M-01", estrato="tramite|P1|MEDIA", publicada="NO"),
        ]

    def test_entran_todas_ordenadas_por_id(self):
        r = MARCO_M.sortear_marco_m(self.marco, n_sorteo=2, cuota_max=0, semilla=999)
        self.assertEqual([f.id for f in r.resultado], ["TRA-M-01", "TRA-M-02"])
        self.assertEqual(r.skips, [])
        self.assertEqual(r.estratos_excluidos, [])

    def test_semilla_no_importa_bajo_el_piso(self):
        r1 = MARCO_M.sortear_marco_m(self.marco, n_sorteo=2, cuota_max=0, semilla=1)
        r2 = MARCO_M.sortear_marco_m(self.marco, n_sorteo=2, cuota_max=0, semilla=2)
        self.assertEqual([f.id for f in r1.resultado], [f.id for f in r2.resultado])


class TestCargarMarcoM(unittest.TestCase):
    """Cargador verifica sha256 contra el archivo declarado y PARA si no
    coincide o si el conteo de filas no calza con ``N_elegibles``."""

    def _escribir_tsv(self, dir_: Path, filas: list[str]) -> Path:
        encabezado = "id\testrato\tpublicada\n"
        ruta = dir_ / "marco.tsv"
        ruta.write_text(encabezado + "\n".join(filas) + "\n", encoding="utf-8")
        return ruta

    def test_carga_ok(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            ruta_tsv = self._escribir_tsv(d, ["X-01\ta|P1|MEDIA\tNO", "X-02\ta|P1|MEDIA\tNO"])
            sha_real = hashlib.sha256(ruta_tsv.read_bytes()).hexdigest()
            ruta_sha = d / "hash.sha256"
            ruta_sha.write_text(f"{sha_real}  marco.tsv\nN_elegibles=2\n", encoding="utf-8")
            filas = MARCO_M.cargar_marco_m(ruta=ruta_tsv, ruta_sha=ruta_sha)
            self.assertEqual([f.id for f in filas], ["X-01", "X-02"])

    def test_sha_no_coincide_para(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            ruta_tsv = self._escribir_tsv(d, ["X-01\ta|P1|MEDIA\tNO"])
            ruta_sha = d / "hash.sha256"
            ruta_sha.write_text("0" * 64 + "  marco.tsv\nN_elegibles=1\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                MARCO_M.cargar_marco_m(ruta=ruta_tsv, ruta_sha=ruta_sha)

    def test_n_elegibles_no_coincide_para(self):
        with tempfile.TemporaryDirectory() as td:
            d = Path(td)
            ruta_tsv = self._escribir_tsv(d, ["X-01\ta|P1|MEDIA\tNO", "X-02\ta|P1|MEDIA\tNO"])
            sha_real = hashlib.sha256(ruta_tsv.read_bytes()).hexdigest()
            ruta_sha = d / "hash.sha256"
            ruta_sha.write_text(f"{sha_real}  marco.tsv\nN_elegibles=99\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                MARCO_M.cargar_marco_m(ruta=ruta_tsv, ruta_sha=ruta_sha)

    def test_marco_m_real_carga_contra_sha_real(self):
        filas = MARCO_M.cargar_marco_m()
        self.assertEqual(len(filas), 2)
        self.assertEqual([f.id for f in filas], ["TRA-M-01", "TRA-M-02"])


if __name__ == "__main__":
    unittest.main()
