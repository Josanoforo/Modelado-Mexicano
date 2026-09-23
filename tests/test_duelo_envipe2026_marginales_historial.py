#!/usr/bin/env python3
"""El orden COMMIT-1 -> COMMIT-2 -> COMMIT-3a -> COMMIT-3 sale del
historial, no de la prosa -- lo que el encargo pide en su §1: *«ningún
acceso a envipe2026_csv antes del commit de COMMIT-3 (test desde el
historial, precedente piloto 2 y duelo 1)»*.

Huérfano en CI: necesita historia completa y los CALC sellados; en un
clon shallow los tests de orden se saltan (mismo precedente que
test_duelo_envipe2026_ejecucion.py, NC-0273).
"""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
EM = "data/corrida0/CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001"
ADJ = "data/corrida0/CALC-DUELO-ENVIPE2026-MARGINALES-ADJUDICACION-0001"


def _git(*args):
    return subprocess.run(["git", "-C", str(RAIZ), *args],
                          capture_output=True, text=True, check=False)


def _historia_truncada():
    r = _git("rev-parse", "--is-shallow-repository")
    return r.returncode == 0 and r.stdout.strip() == "true"


def _nace(ruta):
    r = _git("log", "--diff-filter=A", "--format=%H", "--", ruta)
    shas = r.stdout.split()
    return shas[-1] if r.returncode == 0 and shas else None


class ElOrdenSaleDelHistorial(unittest.TestCase):
    def setUp(self):
        if _historia_truncada():
            self.skipTest("clon shallow (NC-0273)")
        self.sha_c2 = _nace(f"{EM}/resultados.json")
        self.sha_c3a = _nace(f"{ADJ}/spec.yaml")
        self.sha_c3 = _nace(f"{ADJ}/resultados.json")
        if not (self.sha_c2 and self.sha_c3a and self.sha_c3):
            self.skipTest("sin historia de los tres commits")

    def test_commit_2_antes_de_commit_3a_antes_de_commit_3(self):
        self.assertNotEqual(self.sha_c2, self.sha_c3a)
        self.assertNotEqual(self.sha_c3a, self.sha_c3)
        self.assertEqual(_git("merge-base", "--is-ancestor",
                              self.sha_c2, self.sha_c3a).returncode, 0)
        self.assertEqual(_git("merge-base", "--is-ancestor",
                              self.sha_c3a, self.sha_c3).returncode, 0)

    def test_al_congelar_adjudicacion_no_existia_su_resultado(self):
        """En el commit que congela ADJUDICACION-0001/spec.yaml (COMMIT-3a),
        resultados.json de esa misma carpeta todavía no existe -- la spec
        se congeló antes de correr, no después."""
        ls = _git("ls-tree", "--name-only", self.sha_c3a, f"{ADJ}/")
        self.assertNotIn("resultados.json", ls.stdout)

    def test_emisiones_no_puede_abrir_microdato(self):
        """COMMIT-2 (EMISIONES) es aritmética entre sellados: su medidor no
        importa zipfile ni cita el payload 'envipe2026_csv' -- el título del
        docstring sí menciona el acto ('envipe2026' a secas no basta como
        señal), pero no hay mecanismo de E/S sobre microdato posible."""
        texto = (RAIZ / EM / "medidor.py").read_text(encoding="utf-8")
        self.assertNotIn("import zipfile", texto)
        self.assertNotIn("envipe2026_csv", texto)
        self.assertNotIn("conjunto_de_datos_tmod_vic", texto.lower())

    def test_adjudicacion_es_el_unico_que_abre_envipe2026(self):
        texto = (RAIZ / ADJ / "medidor.py").read_text(encoding="utf-8")
        self.assertIn("envipe2026_csv", texto)
        self.assertIn("conjunto_de_datos_tmod_vic", texto.lower())


if __name__ == "__main__":
    unittest.main()
