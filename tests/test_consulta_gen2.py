#!/usr/bin/env python3
"""Pruebas dirigidas de la entrada operativa GEN2."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from tools.consulta_gen2 import consultar, listar_consumidores


RAIZ = Path(__file__).resolve().parents[1]
EJEMPLOS = (
    RAIZ / "forense" / "ejemplos" /
    "GEN2-CONSULTA-OPERATIVA-CON-CONTRATO"
)


class ConsultaGen2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.peticiones = json.loads(
            (EJEMPLOS / "peticiones.json").read_text(encoding="utf-8"))
        cls.respuestas = {r["peticion"]["id"]: r
                          for r in map(consultar, cls.peticiones)}

    def test_01_cada_familia_directa_emite_su_valor_vigente(self):
        esperados = {
            "01-CIV-valida": 0.29431298745731216,
            "03-FAM-valida": 0.04569409956405095,
            "04-TRA-valida": 0.08511814556534456,
        }
        for identidad, valor in esperados.items():
            with self.subTest(identidad=identidad):
                r = self.respuestas[identidad]
                self.assertEqual(r["estado"], "EMITE")
                self.assertEqual(r["valor"]["punto"], valor)
                self.assertEqual(r["resultado"]["generacion"], "GEN2")
                self.assertEqual(r["aptitud"]["estado"], "APTA-POR-LINAJE")

        directos = [
            fila for fila in listar_consumidores()
            if (fila["generacion"] == "GEN2" and not
                fila["consumidor"].startswith(
                    "milpa/tramite.yaml:dinero.ahorro.horizonte"))
        ]
        self.assertEqual(len(directos), 13)
        for fila in directos:
            uso = (
                "DESCRIPTIVO"
                if fila["rol_uso"] == "proxy_descriptivo"
                else "MEDICION-GEN2"
            )
            with self.subTest(consumidor=fila["consumidor"]):
                r = consultar({
                    "consumidor": fila["consumidor"],
                    "proposito": "consulta",
                    "contexto": fila["campos_dominio"],
                    "uso": uso,
                })
                self.assertEqual(r["estado"], "EMITE")
                self.assertEqual(
                    r["resultado"]["id"], fila["resultado_id"])
                self.assertEqual(
                    r["aptitud"]["validacion_independiente"], "PASA")

    def test_01b_guardia_suficiencia_protege_horizonte_colapsado(self):
        identidades = [
            fila for fila in listar_consumidores()
            if (fila["generacion"] == "GEN2" and fila["consumidor"].startswith(
                "milpa/tramite.yaml:dinero.ahorro.horizonte"))
        ]
        self.assertEqual(len(identidades), 3)
        for fila in identidades:
            with self.subTest(consumidor=fila["consumidor"]):
                r = consultar({
                    "consumidor": fila["consumidor"],
                    "proposito": "consulta",
                    "contexto": fila["campos_dominio"],
                    "uso": "MEDICION-GEN2",
                })
                self.assertEqual(r["estado"], "NO_COVERAGE")
                self.assertNotIn("valor", r)
                self.assertEqual(r["suficiencia_uso"]["necesidad_id"], "NC-0126")
                self.assertEqual(
                    r["suficiencia_uso"]["accion_consumidor"],
                    "NO_EMITIR_RESULTADO_SOLICITADO")
                self.assertIn("no puede distinguir", r["motivo_no_cobertura"])

    def test_02_fallos_cerrados_no_exponen_valor(self):
        causas = {
            "02-DIN-valida": "no puede distinguir horizonte corto",
            "05-dominio-falso": "fuera del dominio elegible",
            "06-legacy-en-GEN2": "no se usa el p viejo",
            "08-ENVIPE-a-remesas-parametros-sueltos": "campos no permitidos",
            "09-seleccion-posterior-al-corte": "posterior al corte temporal",
            "11-proxy-uso-no-permitido": "no permitido",
        }
        for identidad, causa in causas.items():
            with self.subTest(identidad=identidad):
                r = self.respuestas[identidad]
                self.assertEqual(r["estado"], "NO_COVERAGE")
                self.assertNotIn("valor", r)
                self.assertIn(causa, r["motivo_no_cobertura"])

    def test_03_transferencia_enigh_reautenticada(self):
        r = self.respuestas["07-transferencia-ENIGH-previa"]
        self.assertEqual(r["estado"], "EMITE")
        self.assertEqual(r["resultado"]["id"], "RESULT-B-ENIGH-2020-P")
        self.assertEqual(r["valor"]["punto"], 0.04377543852935772)
        self.assertEqual(
            r["dependencia"]["rol_seleccion"],
            "OBSERVACION-SERIE-PREVIA")
        self.assertEqual(
            r["estimando"]["periodo"]["corte_temporal"], "2021-12-31")

    def test_04_complemento_conserva_padre_y_transformacion(self):
        r = self.respuestas["10-complemento-adoptado"]
        self.assertEqual(r["estado"], "EMITE")
        self.assertEqual(r["valor"]["punto"], 0.8739943899100835)
        self.assertEqual(
            r["dependencia"]["padre"],
            "solicitud_o_entrega_mordida_encuci2020")
        self.assertEqual(
            r["estimando"]["transformacion"],
            "1-p(solicitud_o_entrega_mordida_encuci2020)")
        self.assertIn(
            "transformacion:1-p", r["dependencia"]["estructurales"])

    def test_05_contexto_desconocido_conserva_causa(self):
        r = consultar({
            "consumidor": (
                "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:"
                "horizonte_corto"),
            "proposito": "consulta",
            "contexto": {"edad_inferida": 37},
            "uso": "MEDICION-GEN2",
        })
        self.assertEqual(r["estado"], "NO_COVERAGE")
        self.assertNotIn("valor", r)
        self.assertIn("campos de dominio desconocidos", r["motivo_no_cobertura"])

    def test_06_listado_publica_identidad_y_campos_de_dominio(self):
        filas = listar_consumidores()
        por_id = {f["consumidor"]: f for f in filas}
        identidad = (
            "milpa/tramite.yaml:civico.denuncia.miedo_desconfianza:"
            "denuncia_con_miedo_o_desconfianza")
        self.assertEqual(por_id[identidad]["campos_dominio"], {
            "bp1_23_en_01_08": True,
            "delito_no_denunciado": True,
            "victima_18_mas": True,
        })

    def test_07_salida_declara_contrato_fuente_y_limite(self):
        r = self.respuestas["03-FAM-valida"]
        self.assertEqual(r["contrato"]["version"], "CONSULTA-GEN2-v1")
        self.assertEqual(len(r["contrato"]["sha256"]), 64)
        self.assertTrue(r["resultado"]["fuente"])
        self.assertTrue(r["estimando"]["poblacion"])
        self.assertTrue(r["estimando"]["unidad"])
        self.assertIn("no es diagnóstico", r["advertencia_interpretacion"])

    def test_08_cli_verifica_respuestas_reproducibles(self):
        respuestas = EJEMPLOS / "respuestas.json"
        if not respuestas.is_file():
            self.skipTest("respuesta dorada se añade después de fijar el contrato")
        corrida = subprocess.run(
            [
                sys.executable,
                "tools/consulta_gen2.py",
                "--lote", str(EJEMPLOS / "peticiones.json"),
                "--verifica", str(respuestas),
            ],
            cwd=RAIZ,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(corrida.returncode, 0, corrida.stderr)
        self.assertIn("OK respuestas reproducibles", corrida.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
