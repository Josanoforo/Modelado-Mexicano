#!/usr/bin/env python3
"""`tools/duelo/tendencia_serie.py` reproduce, byte a byte (tolerancia
1e-9), el piso TENDENCIA-SERIE sellado de `CALC-ENCIG-ORIGEN-MOVIL-0001`
para la celda nacional (`ALL-ALL`), en las cuatro olas donde ese piso es
construible (2019, 2021, 2023, 2025). Insumos leídos del árbol, no
retipeados (A.13, `spec-v1_0.md` §2). Defecto real que atrapa: una
extracción que reordena, redondea o cambia el signo de la ventana de
`pesos()` sin que ningún test lo note.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest

import yaml

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _carga(nombre, rel):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


TS = _carga("tendencia_serie", "tools/duelo/tendencia_serie.py")

OLAS_CANAL = ("2015", "2017", "2019", "2021", "2023")
ID_NACIONAL_2025 = "tramite.gobierno_digital.util_sin_coercion_encig2025"


def _serie_nacional() -> list[tuple[float, float, float, float]]:
    pts = []
    for ola in OLAS_CANAL:
        r = json.load(open(os.path.join(
            RAIZ, f"data/corrida0/CALC-ENCIG-SERIE-CANAL-{ola}/resultados.json")))
        r = r.get("resultados", r)
        b = f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-ALL-ALL"
        pts.append((float(ola), r[b + "-P"], r[b + "-IC-LO"], r[b + "-IC-HI"]))
    y = yaml.safe_load(open(os.path.join(RAIZ, "milpa/tramite-ola5-propuesta-v0.yaml")))
    reglas = {x["id"]: x for x in y["reglas_propuestas"]}
    nac = reglas[ID_NACIONAL_2025]
    p = [e["p"] for e in nac["entonces"] if e["conducta"] == "adopta_canal_digital_encig2025"][0]
    pts.append((2025.0, float(p), float(nac["ic95"][0]), float(nac["ic95"][1])))
    return pts


def _sellado() -> dict:
    d = json.load(open(os.path.join(
        RAIZ, "data/corrida0/CALC-ENCIG-ORIGEN-MOVIL-0001/resultados.json")))
    return d.get("resultados", d)


class ReproduceSellado(unittest.TestCase):
    def test_cuatro_olas_nacionales(self):
        pts = _serie_nacional()
        sellado = _sellado()
        for objetivo in (2019, 2021, 2023, 2025):
            anteriores = [p for p in pts if p[0] < objetivo]
            r = TS.tendencia_serie(anteriores, float(objetivo))
            esperado = sellado[f"RESULT-ENCIG-OM-{objetivo}-ALL-ALL-TENDENCIA-SERIE-P"]
            self.assertIsNotNone(r, f"objetivo={objetivo}: TENDENCIA-SERIE dio None")
            self.assertAlmostEqual(r["p"], esperado, delta=1e-9)

    def test_menos_de_dos_olas_es_no_construible(self):
        self.assertIsNone(TS.tendencia_serie([], 2020.0))
        self.assertIsNone(TS.tendencia_serie([(2015.0, 0.5, 0.4, 0.6)], 2020.0))


if __name__ == "__main__":
    unittest.main()
