#!/usr/bin/env python3
"""El duelo prospectivo ENVIPE 2026 se ejecutó en el orden sellado, y las
emisiones abrieron 2026 sólo por la guardia — leído del historial y de los
RESULT sellados, no de la prosa.

`ACTO GEN2-DUELO-ENVIPE2026-EJECUCION-1` (22/sep/2026). Lo que el encargo
pide: *«Test que asierta desde el historial que el directorio de emisiones
no contiene ninguna lectura de 2026 (precedente piloto 2)»*.

La spec sellada (`DUELO-PROSPECTIVO-ENVIPE2026-spec-v1_0.md` §9) hace que
las emisiones carguen la ola nueva con `reservada=True` (marginales de un eje
para C2, autorizados por F7); respuesta de mesa del 22/sep: «Correr según la
spec». Así que «ninguna lectura de 2026» se prueba como: la ola se cargó
reservada, la guardia lanzó `ReservaRota` sobre el cruce, las emisiones no
emiten R (ni nacional ni cruce de 2026), y el orden
COMMIT-2 → COMMIT-3a → COMMIT-3 sale del historial.

Huérfano en CI: necesita historia completa y los CALC sellados; en un clon
shallow los tests de orden se saltan (NC-0273).

Correr:  python3 tests/test_duelo_envipe2026_ejecucion.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
EM = "data/corrida0/CALC-DUELO-ENVIPE2026-EMISIONES-0001"
ADJ = "data/corrida0/CALC-DUELO-ENVIPE2026-ADJUDICACION-0001"
PE = "RESULT-DUELO26-EM"


def _git(*args):
    return subprocess.run(["git", "-C", str(RAIZ), *args],
                          capture_output=True, text=True, check=False)


def _historia_truncada():
    r = _git("rev-parse", "--is-shallow-repository")
    return r.returncode == 0 and r.stdout.strip() == "true"


def _resultados(calc):
    p = RAIZ / calc / "resultados.json"
    if not p.exists():
        raise unittest.SkipTest(f"{calc} sin resultados.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    return d.get("resultados", d)


def _nace(ruta):
    r = _git("log", "--diff-filter=A", "--format=%H", "--", ruta)
    shas = r.stdout.split()
    return shas[-1] if r.returncode == 0 and shas else None


class LasEmisionesAbrieron2026SoloPorLaGuardia(unittest.TestCase):

    def test_la_ola_nueva_se_cargo_reservada_y_la_guardia_lanzo(self):
        r = _resultados(EM)
        self.assertEqual(r[f"{PE}-G-OLA-NUEVA"], "2026")
        self.assertEqual(r[f"{PE}-G-RESERVA-OLA-CARGADA-RESERVADA"], "SI")
        self.assertEqual(r[f"{PE}-G-RESERVA-CRUCE-OLA-NUEVA-DERIVADO"], "NO")
        self.assertTrue(str(r[f"{PE}-G-RESERVA-GUARDIA-PROBADA"]).startswith("ReservaRota"))
        self.assertTrue(str(r[f"{PE}-G-VETO-EXD-2025-PROBADO"]).startswith("ReservaRota"))

    def test_las_emisiones_no_emiten_r_de_2026(self):
        r = _resultados(EM)
        fugas = [k for k in r if f"{PE}-R-" in k or "SERIE-2026" in k
                 or k.startswith(f"{PE}-NAC-EN-SERIE-2026")]
        self.assertEqual(fugas, [], "las emisiones emiten algo que es R de 2026")


class ElOrdenSaleDelHistorial(unittest.TestCase):

    def setUp(self):
        if _historia_truncada():
            self.skipTest("clon shallow (NC-0273)")
        self.sha_em = _nace(f"{EM}/resultados.json")
        self.sha_adj = _nace(f"{ADJ}/resultados.json")
        if not self.sha_em or not self.sha_adj:
            self.skipTest("sin historia de los dos CALC sellados")

    def test_commit_2_antes_de_commit_3a_antes_de_commit_3(self):
        r = _git("log", "--format=%H", "-S", "sha256: PENDIENTE-COMMIT-3a",
                 "--", f"{ADJ}/spec.yaml")
        shas = r.stdout.split()
        self.assertTrue(shas, "no hay commit que retire PENDIENTE-COMMIT-3a")
        sha_3a = shas[0]  # el más reciente: el que lo retira
        self.assertNotEqual(self.sha_em, sha_3a)
        self.assertNotEqual(sha_3a, self.sha_adj)
        self.assertEqual(_git("merge-base", "--is-ancestor", self.sha_em, sha_3a).returncode, 0)
        self.assertEqual(_git("merge-base", "--is-ancestor", sha_3a, self.sha_adj).returncode, 0)

    def test_commit_3a_solo_toca_una_linea(self):
        r = _git("log", "--format=%H", "-S", "sha256: PENDIENTE-COMMIT-3a",
                 "--", f"{ADJ}/spec.yaml")
        sha_3a = r.stdout.split()[0]
        d = _git("show", "--numstat", "--format=", sha_3a)
        filas = [x.split("\t") for x in d.stdout.strip().splitlines()]
        self.assertEqual(filas, [["1", "1", f"{ADJ}/spec.yaml"]])

    def test_al_sellar_emisiones_no_existia_r(self):
        ls = _git("ls-tree", "--name-only", self.sha_em, f"{ADJ}/")
        self.assertNotIn("resultados.json", ls.stdout)

    def test_el_sha_fijado_es_el_de_las_emisiones_selladas(self):
        spec = yaml.safe_load((RAIZ / ADJ / "spec.yaml").read_text(encoding="utf-8"))
        fijado = next(i for i in spec["inputs"] if i["id"] == "emisiones_selladas")["sha256"]
        real = hashlib.sha256((RAIZ / EM / "resultados.json").read_bytes()).hexdigest()
        self.assertEqual(fijado, real)


if __name__ == "__main__":
    unittest.main(verbosity=2)
