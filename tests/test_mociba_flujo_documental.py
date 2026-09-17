from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import unittest

import yaml

from tools import f6_factibilidad_prepara as F6


ROOT = Path(__file__).resolve().parents[1]
PRODUCTO = ROOT / "forense" / "produccion" / "mociba-flujo-documental-1"
SCRIPT = PRODUCTO / "clasifica_elegibilidad.py"
FIXTURE = PRODUCTO / "fixtures" / "SINTETICO-NO-MEDICION-MOCIBA-FLUJO-1.json"
CARDS = PRODUCTO / "tarjetas-sucesoras.yaml"

SPEC = importlib.util.spec_from_file_location("mociba_flujo", SCRIPT)
MOCIBA = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOCIBA)


class TestClasificadorSintetico(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.datos = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_rotulo_y_todos_los_casos(self):
        self.assertEqual(self.datos["naturaleza"], "SINTETICO-NO-MEDICION")
        salida = MOCIBA.ejecutar_fixtures(FIXTURE)
        self.assertTrue(salida["ok"])
        self.assertEqual(salida["casos"], 10)
        self.assertFalse(salida["microdatos_abiertos"])
        self.assertEqual(salida["llamadas_realizadas"], 0)

    def test_si_basta_aunque_falten_otros_p4(self):
        fila = {"EDAD": 21, "P7_1": 1, "P4_08": 1, "P12_5": 1}
        self.assertEqual(MOCIBA.clasificar_fila(fila, 2021)["estado"], "ELEGIBLE")

    def test_mezcla_dos_nueve_completa_salta_e_incompleta_no_se_infiere(self):
        completa = {"EDAD": 21, "P7_1": 1, **{
            campo: 2 if i % 2 else 9 for i, campo in enumerate(MOCIBA.P4)
        }}
        self.assertEqual(MOCIBA.clasificar_fila(completa, 2022)["estado"], "NO-ELEGIBLE")
        incompleta = copy.deepcopy(completa)
        incompleta.pop("P4_13")
        self.assertEqual(MOCIBA.clasificar_fila(incompleta, 2022)["estado"], "INDETERMINADO")

    def test_blanco_dentro_no_es_no_y_fuera_es_no_aplica(self):
        dentro = {"EDAD": 21, "P7_1": 1, "P4_01": 1, "P12_5": "b"}
        salida = MOCIBA.clasificar_fila(dentro, 2022)
        self.assertEqual(salida["estado"], "ELEGIBLE")
        self.assertEqual(salida["respuesta_estado"], "AUSENTE-DENTRO-UNIVERSO")
        self.assertIsNone(salida["evento"])
        fuera = {"EDAD": 21, "P7_1": 2, "P12_5": "b"}
        self.assertEqual(
            MOCIBA.clasificar_fila(fuera, 2022)["respuesta_estado"],
            "NO-APLICA-ESTRUCTURAL",
        )

    def test_codigo_invalido_falla_cerrado(self):
        fila = {"EDAD": 21, "P7_1": 1, "P4_01": "X"}
        self.assertEqual(MOCIBA.clasificar_fila(fila, 2021)["estado"], "INDETERMINADO")


class TestFronteraPreflight(unittest.TestCase):
    def test_definicion_mejora_sin_habilitar_m_firma_llamadas_o_r(self):
        datos = yaml.safe_load(CARDS.read_text(encoding="utf-8"))
        mociba = [x for x in datos["celdas"] if x["candidata_id"] == "R01"]
        self.assertEqual({x["definicion"]["estado"] for x in mociba}, {"ACREDITADA"})
        self.assertEqual(
            {x["enlace_M"]["estado"] for x in mociba}, {"CANDIDATO-NO-ELEGIBLE"}
        )
        self.assertFalse(datos["llamadas_autorizadas"])
        self.assertFalse(datos["apertura_R_autorizada"])
        self.assertEqual(datos["firma"]["estado"], "PENDIENTE-DE-MESA")
        salida = F6.preflight(datos)
        self.assertEqual(
            {x["estado"] for x in salida["detalle"] if x["familia_id"].startswith("R01")},
            {"DEFINICION_O_CANDIDATO_INSUFICIENTE"},
        )
        self.assertFalse(salida["autorizado_para_llamadas"])
        self.assertFalse(salida["microdatos_abiertos"])


if __name__ == "__main__":
    unittest.main()
