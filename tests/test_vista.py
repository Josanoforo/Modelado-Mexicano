"""ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2 · COMMIT-A -- tools/vista.py.

`join_resultado` reconstruye `tolerancia`/`funciones_dependencia`/
`fuente_replay` para una fila de `resultados.tsv` que ya no los trae: la
regla es "el propio valor manda si esta presente; si no, se busca en la
corrida; si tampoco esta ahi, `SIN-CORRIDA-EN-VISTA`", nunca un
`KeyError`. Sintetico, sin tocar `data/corrida0/`.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import vista  # noqa: E402


class JoinResultado(unittest.TestCase):
    def test_campo_ausente_se_completa_desde_la_corrida(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1", "valor": "1"}
        corridas = {"CORR-1": {"corrida_id": "CORR-1", "tolerancia": '{"abs": 0.01}',
                                "funciones_dependencia": "f(x)", "fuente_replay": "NO-CORRIDA"}}
        j = vista.join_resultado(fila, corridas)
        self.assertEqual(j["tolerancia"], '{"abs": 0.01}')
        self.assertEqual(j["funciones_dependencia"], "f(x)")
        self.assertEqual(j["fuente_replay"], "NO-CORRIDA")
        # la fila original no se muta
        self.assertNotIn("tolerancia", fila)

    def test_campo_propio_manda_sobre_el_de_la_corrida(self):
        """Formato previo a COMMIT-A, o un fixture sintetico que ya lo
        declara: el valor de la propia fila no se pisa."""
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-1",
                "tolerancia": "PENDIENTE"}
        corridas = {"CORR-1": {"corrida_id": "CORR-1", "tolerancia": '{"abs": 0.01}'}}
        j = vista.join_resultado(fila, corridas)
        self.assertEqual(j["tolerancia"], "PENDIENTE")

    def test_corrida_ausente_no_revienta(self):
        fila = {"resultado_id": "RES-1", "corrida_id": "CORR-DESCONOCIDA"}
        j = vista.join_resultado(fila, {})
        self.assertEqual(j["tolerancia"], "SIN-CORRIDA-EN-VISTA")
        self.assertEqual(j["funciones_dependencia"], "SIN-CORRIDA-EN-VISTA")
        self.assertEqual(j["fuente_replay"], "SIN-CORRIDA-EN-VISTA")

    def test_corridas_por_id_archivo_ausente_da_diccionario_vacio(self):
        self.assertEqual(vista.corridas_por_id(Path("/no/existe/corridas.tsv")), {})


if __name__ == "__main__":
    unittest.main()
