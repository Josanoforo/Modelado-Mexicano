#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardia de ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1 (21/sep/2026).

Defectos reales que atrapa, los dos medidos en ese acto:
  1. `mm-corpus/raw/raw -> mm-corpus/raw` es un symlink en bucle: un
     recorrido con followlinks=True infló el índice a 51 641 «archivos»
     (1 291 reales). El índice del juego de respaldo debe omitir symlinks.
  2. El ciclo indexa -> copia -> verifica -> restaura es la instrucción de
     una página para repetir el respaldo; si una edición lo rompe, el
     siguiente respaldo «verifica» en falso. Se prueba de ida y vuelta
     sobre un corpus sintético (sin corpus real: CORRE-EN-CI).

Invocación: python3 -m pytest tests/test_corpus_integridad_respaldo.py -q
            o python3 tests/test_corpus_integridad_respaldo.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "forense", "analisis", "corpus-integridad-1", "respaldo_corpus.py")


def _carga():
    spec = importlib.util.spec_from_file_location("respaldo_corpus", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestRespaldoCorpus(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="t-respaldo-")
        self.raiz = os.path.join(self.tmp, "raiz")
        os.makedirs(os.path.join(self.raiz, "ENIF", "2024"))
        self.contenido = {"suelto.pdf": b"pdf" * 100, "ENIF/2024/a.zip": b"zip" * 1000,
                          "ENIF/b.csv": b"1,2,3\n"}
        for rel, data in self.contenido.items():
            with open(os.path.join(self.raiz, rel), "wb") as f:
                f.write(data)
        os.symlink(self.raiz, os.path.join(self.raiz, "raiz"))  # el bucle real
        with open(os.path.join(self.raiz, ".manifiesto.lock"), "w") as f:
            f.write("lock")
        self.destino = os.path.join(self.tmp, "juego")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_caminar_omite_symlink_en_bucle_y_lock(self):
        mod = _carga()
        rels = mod.caminar(self.raiz)
        self.assertEqual(sorted(rels), sorted(self.contenido))

    def test_ciclo_indexa_copia_verifica_restaura(self):
        if shutil.which("rsync") is None:
            self.skipTest("rsync ausente")
        base = [sys.executable, SCRIPT, "--destino", self.destino, "--raiz", f"r={self.raiz}"]
        # --raiz sólo AÑADE a las tres raíces por defecto: en CI no existen.
        # Se pasan las tres apuntando a la raíz sintética para que el
        # script no pare por «raíz no accesible».
        for n in ("data_raw", "descargas_mx", "reserva_respondentes"):
            base += ["--raiz", f"{n}={self.raiz}"]
        r = subprocess.run(base + ["--indexa"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        with open(os.path.join(self.destino, "indice.tsv"), encoding="utf-8") as f:
            filas = [ln.split("\t") for ln in f.read().splitlines()[1:]]
        # 4 raíces lógicas x 3 archivos; ningún symlink ni lock
        self.assertEqual(len(filas), 12)
        self.assertNotIn("raiz/suelto.pdf", {f[1] for f in filas})
        sha_zip = hashlib.sha256(self.contenido["ENIF/2024/a.zip"]).hexdigest()
        self.assertIn(("r", "ENIF/2024/a.zip", "3000", sha_zip), {tuple(f) for f in filas})

        r = subprocess.run(base + ["--copia"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        r = subprocess.run(base + ["--verifica"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("coincide=12 no_coincide=0 falta=0", r.stdout)

        # corrupción en destino -> ROJO
        with open(os.path.join(self.destino, "r", "ENIF", "b.csv"), "ab") as f:
            f.write(b"x")
        r = subprocess.run(base + ["--verifica"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertIn("NO-COINCIDE r/ENIF/b.csv", r.stdout)
        with open(os.path.join(self.destino, "r", "ENIF", "b.csv"), "wb") as f:
            f.write(self.contenido["ENIF/b.csv"])

        r = subprocess.run(base + ["--restaura", "2", "--tmp", os.path.join(self.tmp, "rt")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("no_coincide=0", r.stdout)
        self.assertIn("-> VERDE", r.stdout)


if __name__ == "__main__":
    unittest.main()
