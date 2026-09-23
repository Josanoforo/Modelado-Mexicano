#!/usr/bin/env python3
"""D-22 de `CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001`: el medidor
corre sobre insumos SINTÉTICOS antes que sobre los sellados reales ("oro"),
y `_valida_outputs` de `corrida0` acepta la salida completa. Cero microdato:
este CALC es aritmética entre sellados (`spec-v1_0.md` §3).

Defectos reales que atrapa: un output que el medidor puede emitir `None`
sin `permite_no_estimable` revienta `run` después de congelar (mismo
defecto que `test_encig_serie_canal.py` documenta); un cambio silencioso
en `tools/duelo/tendencia_serie.py` que la guardia de hash no note.
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))


def _carga(nombre, rel):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MED = _carga("medidor_duelo_marginales",
             "data/corrida0/CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001/medidor.py")
C0 = _carga("corrida0", "tools/corrida0.py")


def _bytes_inputs(punto_aseg_24, punto_aseg_25, punto_noaseg_24, punto_noaseg_25):
    def _res_2025():
        r = {}
        for celda, (p, lo, hi, n) in (("ASEGURADO", punto_aseg_25), ("NO-ASEGURADO", punto_noaseg_25)):
            b = f"RESULT-ARBITRO-ENVIPE2025-DENUNCIA-COBERTURA-SEGURO-{celda}"
            r[b + "-P"], r[b + "-IC-LO"], r[b + "-IC-HI"], r[b + "-N"] = p, lo, hi, n
        return json.dumps({"resultados": r}).encode("utf-8")

    def _res_2024():
        r = {}
        for celda, (p, lo, hi, n) in (("ASEGURADO", punto_aseg_24), ("NO-ASEGURADO", punto_noaseg_24)):
            b = f"RESULT-PISOS-ENVIPE2024-V2-DENUNCIA-COBERTURA-SEGURO-{celda}"
            r[b + "-P"], r[b + "-IC-LO"], r[b + "-IC-HI"], r[b + "-N"] = p, lo, hi, n
        return json.dumps({"resultados": r}).encode("utf-8")

    return {
        "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001": {"bytes": _res_2025()},
        "CALC-PISOS-ENVIPE2024-EJES-0002": {"bytes": _res_2024()},
    }


class Sintetico(unittest.TestCase):
    """Puntos inventados, lejos de cualquier cifra real, antes del oro."""

    def test_medir_y_valida_outputs(self):
        inputs = _bytes_inputs((0.60, 0.55, 0.65, 300), (0.62, 0.57, 0.67, 310),
                                (0.40, 0.35, 0.45, 400), (0.41, 0.36, 0.46, 410))
        out = MED.medir(inputs, {})
        ruta_spec, spec = C0._carga_spec("CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001")
        problemas = C0._valida_outputs(spec, out)
        self.assertEqual(problemas, [], f"_valida_outputs encontró: {problemas}")
        self.assertAlmostEqual(out["RESULT-DUELO-MARGINALES-ASEGURADO-PISO-P"], 0.62)
        self.assertEqual(out["RESULT-DUELO-MARGINALES-ASEGURADO-RETADOR-CONSTRUIBLE"], "SI")

    def test_nacional_sexo_edad_demas_reglas_declarados(self):
        inputs = _bytes_inputs((0.6, 0.5, 0.7, 10), (0.6, 0.5, 0.7, 10),
                                (0.4, 0.3, 0.5, 10), (0.4, 0.3, 0.5, 10))
        out = MED.medir(inputs, {})
        self.assertEqual(out["RESULT-DUELO-MARGINALES-NACIONAL-RETADOR-CONSTRUIBLE"], "NO")
        self.assertEqual(out["RESULT-DUELO-MARGINALES-SEXO-CONSTRUIBLE"], "NO")
        self.assertEqual(out["RESULT-DUELO-MARGINALES-EDAD-CONSTRUIBLE"], "NO")
        self.assertEqual(out["RESULT-DUELO-MARGINALES-DEMAS-REGLAS-ENVIPE-SERIE-N"], 0)


class Guardia(unittest.TestCase):
    def test_dependencia_mutada_para(self):
        real = MED.SHA256_TENDENCIA_SERIE_CONGELADO
        MED.SHA256_TENDENCIA_SERIE_CONGELADO = "0" * 64
        try:
            with self.assertRaises(SystemExit):
                MED._verifica_dependencia_congelada()
        finally:
            MED.SHA256_TENDENCIA_SERIE_CONGELADO = real


class Oro(unittest.TestCase):
    """Contra los RESULT sellados reales, sólo para confirmar que el medidor
    corre sobre el insumo verdadero -- no sustituye a la validación
    independiente ni cuenta como control positivo por sí sola."""

    def test_oro_reproduce_lo_citado_en_la_spec_humana(self):
        ruta_2025 = os.path.join(
            RAIZ, "data/corrida0/CALC-ARBITRO-MARGINALES-ENVIPE2025-0001/resultados.json")
        ruta_2024 = os.path.join(
            RAIZ, "data/corrida0/CALC-PISOS-ENVIPE2024-EJES-0002/resultados.json")
        inputs = {
            "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001": {"bytes": open(ruta_2025, "rb").read()},
            "CALC-PISOS-ENVIPE2024-EJES-0002": {"bytes": open(ruta_2024, "rb").read()},
        }
        out = MED.medir(inputs, {})
        self.assertAlmostEqual(out["RESULT-DUELO-MARGINALES-ASEGURADO-PISO-P"],
                                0.7909064453831163, delta=1e-9)
        self.assertAlmostEqual(out["RESULT-DUELO-MARGINALES-NO-ASEGURADO-PISO-P"],
                                0.6720144369290082, delta=1e-9)
        self.assertEqual(out["RESULT-DUELO-MARGINALES-ASEGURADO-RETADOR-CONSTRUIBLE"], "SI")
        self.assertEqual(out["RESULT-DUELO-MARGINALES-NO-ASEGURADO-RETADOR-CONSTRUIBLE"], "SI")
        ruta_spec, spec = C0._carga_spec("CALC-DUELO-ENVIPE2026-MARGINALES-EMISIONES-0001")
        problemas = C0._valida_outputs(spec, out)
        self.assertEqual(problemas, [])


if __name__ == "__main__":
    unittest.main()
