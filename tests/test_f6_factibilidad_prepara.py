from __future__ import annotations

import copy
import json
import pathlib
import unittest
from unittest import mock

import yaml

from tools import f6_factibilidad_prepara as F6


ROOT = pathlib.Path(__file__).resolve().parents[1]
CARDS = (
    ROOT / "forense" / "prereg-duelo-v2"
    / "F6-factibilidad-preparacion-v1_0" / "tarjetas.yaml"
)
FIXTURE = CARDS.parent / "fixtures" / "SINTETICO-NO-MEDICION.json"


class TestTransformacionesSinteticas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        if cls.fixture.get("naturaleza") != "SINTETICO-NO-MEDICION":
            raise AssertionError("fixture no está rotulado SINTETICO-NO-MEDICION")

    def test_filtro_missing_y_salto_fuera_del_denominador(self):
        punto = F6.proporcion_ponderada(
            self.fixture["mociba"], evento={1}, missing={"b"}
        )
        self.assertAlmostEqual(punto, 2.0 / 3.0)

    def test_peso_invalido_y_denominador_vacio_se_rechazan(self):
        with self.assertRaisesRegex(F6.ContratoInvalido, "peso_no_positivo"):
            F6.proporcion_ponderada(
                [{"elegible": True, "respuesta": 1, "peso": 0}],
                evento={1},
            )
        with self.assertRaisesRegex(F6.ContratoInvalido, "denominador_vacio"):
            F6.proporcion_ponderada(
                [{"elegible": False, "respuesta": None, "peso": 1}],
                evento={1},
            )

    def test_categoria_issp_permanece_compuesta(self):
        self.assertIs(F6.evento_issp_compuesto(1), True)
        self.assertIs(F6.evento_issp_compuesto(2), False)
        self.assertIsNone(F6.evento_issp_compuesto(8))
        # La interfaz sólo produce el evento conjunto; no devuelve una parte
        # "familia" ni "amistad" que el cuestionario no observó.
        self.assertIsInstance(F6.evento_issp_compuesto(1), bool)

    def test_escala_comun_y_rechazo_de_indice(self):
        self.assertEqual(F6.a_puntos_porcentuales(0.25, "proporcion_0_1"), 25)
        self.assertEqual(F6.a_puntos_porcentuales(25, "porcentaje_0_100"), 25)
        self.assertEqual(
            F6.error_absoluto_pp(
                0.2, 25, escala_prediccion="proporcion_0_1",
                escala_realidad="porcentaje_0_100",
            ),
            5,
        )
        with self.assertRaisesRegex(F6.ContratoInvalido, "escala_incompatible"):
            F6.a_puntos_porcentuales(0.5, "indice_sin_enlace")

    def test_abstencion_no_es_cero_y_celdas_no_inflan_familias(self):
        self.assertIsNone(
            F6.error_absoluto_pp(
                None, 0.4, escala_prediccion="proporcion_0_1",
                escala_realidad="proporcion_0_1",
            )
        )
        agregado = F6.agregar_errores_por_familia(self.fixture["familias"])
        self.assertEqual(set(agregado), {"R01", "R09"})
        self.assertEqual(agregado["R01"]["n_celdas"], 2)
        self.assertEqual(agregado["R01"]["error_medio_pp"], 3)
        self.assertEqual(agregado["R09"]["abstenciones"], 1)
        self.assertEqual(agregado["R09"]["error_medio_pp"], 3)


class TestPreflight(unittest.TestCase):
    def setUp(self):
        self.datos = yaml.safe_load(CARDS.read_text(encoding="utf-8"))

    def test_tarjetas_parseables_siguen_rechazadas_y_no_autorizadas(self):
        resultado = F6.preflight(self.datos)
        self.assertEqual(resultado["familias"], 2)
        self.assertEqual(resultado["celdas"], 4)
        self.assertEqual(
            resultado["conteos"],
            {"DEFINICION_O_CANDIDATO_INSUFICIENTE": 4},
        )
        self.assertFalse(resultado["autorizado_para_llamadas"])
        self.assertFalse(resultado["microdatos_abiertos"])
        self.assertFalse(resultado["modelos_llamados"])
        self.assertFalse(resultado["resultados_canonicos_escritos"])

    def test_sin_firma_caso_tecnicamente_completo_queda_pendiente(self):
        datos = copy.deepcopy(self.datos)
        datos["celdas"] = [datos["celdas"][0]]
        celda = datos["celdas"][0]
        celda["definicion"]["estado"] = "ACREDITADA"
        celda["enlace_M"]["estado"] = "ELEGIBLE"
        celda["reserva"]["estado"] = "LIMPIA"
        resultado = F6.preflight(datos)
        self.assertEqual(
            resultado["detalle"][0]["estado"], "AUTORIZACION_PENDIENTE"
        )
        self.assertIn("FIRMA:PENDIENTE-DE-MESA",
                      resultado["detalle"][0]["bloqueos"])
        self.assertFalse(resultado["autorizado_para_llamadas"])

    def test_preflight_no_resuelve_payload_ref(self):
        datos = copy.deepcopy(self.datos)
        datos["celdas"][0]["payload_ref"] = "/ruta/SENTINELA-NO-ABRIR.dta"
        with mock.patch("pathlib.Path.read_bytes",
                        side_effect=AssertionError("abrió un payload")):
            resultado = F6.preflight(datos)
        self.assertTrue(all(not x["payload_abierto"] for x in resultado["detalle"]))

    def test_estado_protector_y_limites_son_fail_closed(self):
        datos = copy.deepcopy(self.datos)
        datos["estado"] = "LISTA-PARA-CORRER"
        with self.assertRaisesRegex(F6.ContratoInvalido,
                                    "estado_spec_no_protege"):
            F6.preflight(datos)
        datos = copy.deepcopy(self.datos)
        datos["celdas"].append(copy.deepcopy(datos["celdas"][0]))
        with self.assertRaisesRegex(F6.ContratoInvalido,
                                    "mas_de_cuatro_celdas"):
            F6.preflight(datos)


if __name__ == "__main__":
    unittest.main()
