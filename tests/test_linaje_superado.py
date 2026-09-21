#!/usr/bin/env python3
"""Los tres caminos del cargador de linaje de emisión, con datos sintéticos.

ACTO MOTOR-LINAJE-1 · 21/sep/2026 ·
`forense/encargos/2026-09-21-motor-linaje-1-nc0401.md` §5-P1.

Defecto real que atrapa (NC-0401 / NC-0400): antes de este acto
`cargar_indice_linaje_emision` colapsaba TRES situaciones distintas en una
sola excepción de carga — «una vigente», «más de una vigente» y «cero
vigentes» —, y la tercera reventaba el índice completo por un
`resultado_id` que nadie consume. Con eso, `tests/test_motor_gen2_
explicito.py` y `tests/test_consulta_gen2.py` no ejecutaban ni una prueba.

Qué le habría costado a un lector: el motor entero era incargable por un
id superado ajeno a su consulta, y el mensaje no decía quién lo sucede.

Condición de la firma de mesa (21/sep/2026): el cargador NO sigue la
sucesión en silencio. Por eso el camino (iii) NOMBRA al sucesor y NO lo
resuelve.

Sin microdato: todo corre contra TSV sintéticos en un directorio temporal.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from milpa.src.emisor import (  # noqa: E402
    SUCESOR_NO_DECLARADO,
    ResultadoIntegramenteSuperado,
    cargar_indice_linaje_emision,
)

COLUMNAS_RESULTADO = [
    "resultado_id", "origen", "corrida_id", "spec_id", "valor", "tipo",
    "unidad", "estado", "generacion", "origen_numerico",
    "validacion_independiente", "rol_evaluacion", "camino_linaje",
    "fuente_replay", "depende_de",
]
COLUMNAS_USO = [
    "resultado_id", "consumidor", "tipo_uso", "activo", "generacion_leida",
    "corrida0_generacion", "corrida0_resultado_id", "uso_solicitado",
    "origen_numerico", "aptitud_uso", "motivo_aptitud", "camino_linaje",
]


def _fila(columnas, **campos):
    return "\t".join(str(campos.get(c, "")) for c in columnas)


class TresCaminosDelCargador(unittest.TestCase):
    """(i) una vigente · (ii) más de una vigente · (iii) cero vigentes."""

    def _indice(self, filas_resultado, filas_uso=()):
        tmp = Path(tempfile.mkdtemp())
        res = tmp / "resultados.tsv"
        usos = tmp / "usos.tsv"
        res.write_text(
            "# DERIVADO — NO EDITAR\n"
            + "\t".join(COLUMNAS_RESULTADO) + "\n"
            + "".join(f + "\n" for f in filas_resultado),
            encoding="utf-8")
        usos.write_text(
            "# DERIVADO — NO EDITAR\n"
            + "\t".join(COLUMNAS_USO) + "\n"
            + "".join(f + "\n" for f in filas_uso),
            encoding="utf-8")
        return cargar_indice_linaje_emision(
            ruta_usos=usos, ruta_resultados=res)

    # (i) -------------------------------------------------------------
    def test_i_una_vigente_se_carga_como_siempre(self):
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-X",
                  valor="0.25", tipo="proporcion", estado="SELLADA",
                  generacion="GEN2"),
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-X",
                  valor="0.10", tipo="proporcion",
                  estado="SUPERADO→CALC-X-v2", generacion="GEN2"),
        ])
        self.assertEqual(indice.resultados["RESULT-X"].valor, 0.25)
        self.assertIn("RESULT-X", indice.resultados)
        self.assertEqual(dict(indice.superados), {})

    # (ii) ------------------------------------------------------------
    def test_ii_dos_vigentes_revientan_al_cargar(self):
        with self.assertRaises(ValueError) as caja:
            self._indice([
                _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Y",
                      valor="0.25", estado="SELLADA"),
                _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Y",
                      valor="0.30", estado="SELLADA"),
            ])
        self.assertIn("hay 2", str(caja.exception))
        # La ambigüedad de (ii) NO es la de (iii): no se colapsan.
        self.assertNotIsInstance(
            caja.exception, ResultadoIntegramenteSuperado)

    # (iii) -----------------------------------------------------------
    def test_iii_cero_vigentes_no_revienta_el_indice_completo(self):
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Z",
                  valor="0.10", estado="SUPERADO→CALC-Z-v2"),
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-VIVO",
                  valor="0.40", estado="SELLADA"),
        ])
        # El id sano sigue disponible: un superado ajeno no tumba el índice.
        self.assertEqual(indice.resultados["RESULT-VIVO"].valor, 0.40)

    def test_iii_la_entrada_no_se_omite_y_nombra_al_sucesor(self):
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Z",
                  valor="0.10", estado="SUPERADO→CALC-Z-v2"),
        ])
        self.assertIn("RESULT-Z", indice.superados)
        self.assertEqual(indice.superados["RESULT-Z"].sucesor, "CALC-Z-v2")

    def test_iii_error_propio_por_corchete_y_por_get(self):
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Z",
                  valor="0.10", estado="SUPERADO→CALC-Z-v2"),
        ])
        for cómo, llamada in (
                ("[]", lambda: indice.resultados["RESULT-Z"]),
                (".get()", lambda: indice.resultados.get("RESULT-Z"))):
            with self.subTest(acceso=cómo):
                with self.assertRaises(
                        ResultadoIntegramenteSuperado) as caja:
                    llamada()
                error = caja.exception
                self.assertEqual(error.resultado_id, "RESULT-Z")
                self.assertEqual(error.sucesor, "CALC-Z-v2")
                # El mensaje nombra id y sucesor (condición de mesa).
                self.assertIn("RESULT-Z", str(error))
                self.assertIn("CALC-Z-v2", str(error))

    def test_iii_no_resuelve_al_sucesor_ni_devuelve_none(self):
        """La adopción por la puerta de atrás es lo que esto impide."""
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Z",
                  valor="0.10", estado="SUPERADO→RESULT-Z-V2"),
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-Z-V2",
                  valor="0.99", estado="SELLADA"),
        ])
        with self.assertRaises(ResultadoIntegramenteSuperado):
            indice.resultados.get("RESULT-Z")
        # ...y el sucesor sigue siendo pedible por su propio id.
        self.assertEqual(indice.resultados["RESULT-Z-V2"].valor, 0.99)

    def test_iii_sin_sucesor_declarado_no_se_inventa(self):
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-W",
                  valor="0.10", estado="SUPERADO"),
        ])
        self.assertEqual(
            indice.superados["RESULT-W"].sucesor, SUCESOR_NO_DECLARADO)

    # ausente ---------------------------------------------------------
    def test_ausente_sigue_siendo_ausente(self):
        """Tercer estado de A.4: «no existe» no es «superado»."""
        indice = self._indice([
            _fila(COLUMNAS_RESULTADO, resultado_id="RESULT-VIVO",
                  valor="0.40", estado="SELLADA"),
        ])
        self.assertIsNone(indice.resultados.get("RESULT-NUNCA-EXISTIO"))
        with self.assertRaises(KeyError):
            indice.resultados["RESULT-NUNCA-EXISTIO"]


if __name__ == "__main__":
    unittest.main(verbosity=2)
