#!/usr/bin/env python3
"""Pruebas dirigidas de la entrada operativa GEN2."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import adq_suficiencia
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

    def _con_estado_nc0126(self, estado):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            ruta = (raiz / "data" / "curacion-registro" /
                    "investigacion-estado" / "NC-0126.json")
            ruta.parent.mkdir(parents=True)
            ruta.write_text(
                json.dumps(estado, ensure_ascii=False), encoding="utf-8")
            for evidencia in estado.get("decision_emision", {}).get("evidencias", []):
                path_evidencia = raiz / evidencia.split("#", 1)[0]
                path_evidencia.parent.mkdir(parents=True, exist_ok=True)
                path_evidencia.write_text("evidencia sintética", encoding="utf-8")
            with mock.patch.object(adq_suficiencia, "RAIZ", raiz):
                return consultar({
                    "consumidor": (
                        "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:"
                        "horizonte_corto"),
                    "proposito": "consulta",
                    "contexto": {},
                    "uso": "MEDICION-GEN2",
                })

    def _estado_nc0126(self):
        return json.loads((
            RAIZ / "data" / "curacion-registro" /
            "investigacion-estado" / "NC-0126.json"
        ).read_text(encoding="utf-8"))

    def test_01c_apta_reportada_sin_adopcion_no_habilita_resultado_viejo(self):
        estado = self._estado_nc0126()
        estado["suficiencia"]["uso_habilitado"] = "APTA_USO_DECLARADO"
        estado["suficiencia"]["pregunta_original"] = "CUBIERTA"
        r = self._con_estado_nc0126(estado)
        self.assertEqual(r["estado"], "NO_COVERAGE")
        self.assertNotIn("valor", r)
        self.assertEqual(
            r["resultado"]["id"], "RESULT-ENIF-AHO-A-P-CORTO-SIN-P")
        guardia = r["contrato"]["guardia_suficiencia_efectiva"]
        self.assertEqual(
            guardia["estado_efectivo"], "BLOQUEADA_SIN_DECISION_APLICABLE")
        self.assertTrue(guardia["integridad_estado"]["identidad_valida"])
        self.assertTrue(guardia["integridad_estado"]["sha256_observado"])

    def test_01d_estado_de_otra_necesidad_o_version_se_descarta(self):
        for campo, valor in (
            ("version_pregunta", "2026-09-09-horizonte-ahorro-descolapsado-v0"),
            ("necesidad_id", "NC-0122"),
        ):
            with self.subTest(campo=campo):
                estado = self._estado_nc0126()
                estado[campo] = valor
                estado["suficiencia"]["uso_habilitado"] = "APTA_USO_DECLARADO"
                estado["evidencias"].append("forense/decision-sintetica.md")
                estado["decision_emision"] = {
                    "clase": "AUTORIZA_RESULTADO_EXISTENTE",
                    "necesidad_id": "NC-0126",
                    "version_pregunta": "2026-09-09-horizonte-ahorro-descolapsado-v1",
                    "consumidor": (
                        "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:"
                        "horizonte_corto"),
                    "resultado_id": "RESULT-ENIF-AHO-A-P-CORTO-SIN-P",
                    "uso_aprobado": "MEDICION-GEN2",
                    "evidencias": ["forense/decision-sintetica.md"],
                }
                r = self._con_estado_nc0126(estado)
                self.assertEqual(r["estado"], "NO_COVERAGE")
                self.assertNotIn("valor", r)
                guardia = r["contrato"]["guardia_suficiencia_efectiva"]
                self.assertFalse(guardia["integridad_estado"]["identidad_valida"])
                self.assertIn(
                    "estado descartado", guardia["integridad_estado"]["descarte"])

    def test_01e_alcance_menor_sin_vinculo_no_emite_el_result_viejo(self):
        estado = self._estado_nc0126()
        estado["suficiencia"]["uso_habilitado"] = "APTA_ALCANCE_MENOR"
        r = self._con_estado_nc0126(estado)
        self.assertEqual(r["estado"], "NO_COVERAGE")
        self.assertNotIn("valor", r)
        self.assertEqual(
            r["resultado"]["id"], "RESULT-ENIF-AHO-A-P-CORTO-SIN-P")
        self.assertNotEqual(r.get("valor", {}).get("punto"), 0.541343)
        self.assertEqual(
            r["suficiencia_uso"]["estado_efectivo"],
            "BLOQUEADA_SIN_VINCULO_ALCANCE_MENOR")

    def test_01f_decision_exacta_es_la_unica_excepcion_para_resultado_viejo(self):
        estado = self._estado_nc0126()
        estado["suficiencia"]["uso_habilitado"] = "APTA_USO_DECLARADO"
        estado["evidencias"].append("forense/decision-sintetica.md")
        estado["decision_emision"] = {
            "clase": "AUTORIZA_RESULTADO_EXISTENTE",
            "necesidad_id": "NC-0126",
            "version_pregunta": estado["version_pregunta"],
            "consumidor": (
                "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:"
                "horizonte_corto"),
            "resultado_id": "RESULT-ENIF-AHO-A-P-CORTO-SIN-P",
            "uso_aprobado": "MEDICION-GEN2",
            "evidencias": ["forense/decision-sintetica.md"],
        }
        r = self._con_estado_nc0126(estado)
        self.assertEqual(r["estado"], "EMITE")
        self.assertEqual(r["valor"]["punto"], 0.541343)
        self.assertEqual(
            r["suficiencia_uso"]["estado_efectivo"],
            "HABILITADA_POR_DECISION_APLICABLE")

    def test_01g_sucesor_exige_calculo_y_adopcion(self):
        estado = self._estado_nc0126()
        estado["suficiencia"]["uso_habilitado"] = "APTA_USO_DECLARADO"
        estado["evidencias"].append("forense/sucesor-sintetico.md")
        estado["decision_emision"] = {
            "clase": "ADOPTA_SUCESOR_CALCULADO",
            "necesidad_id": "NC-0126",
            "version_pregunta": estado["version_pregunta"],
            "consumidor": (
                "milpa/tramite.yaml:dinero.ahorro.horizonte_corto:"
                "horizonte_corto"),
            "resultado_id": "RESULT-SUCESOR-SINTETICO",
            "uso_aprobado": "MEDICION-GEN2",
            "calculada": True,
            "adoptada": False,
            "evidencias": ["forense/sucesor-sintetico.md"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            ruta = (raiz / "data" / "curacion-registro" /
                    "investigacion-estado" / "NC-0126.json")
            ruta.parent.mkdir(parents=True)
            ruta.write_text(json.dumps(estado), encoding="utf-8")
            evidencia = raiz / "forense" / "sucesor-sintetico.md"
            evidencia.parent.mkdir(parents=True)
            evidencia.write_text("evidencia sintética", encoding="utf-8")
            bloqueada = adq_suficiencia.proyecta_consumidor(
                estado["decision_emision"]["consumidor"], raiz=raiz,
                resultado_id="RESULT-SUCESOR-SINTETICO",
                uso_solicitado="MEDICION-GEN2")
            self.assertEqual(
                bloqueada["accion_consumidor"],
                "NO_EMITIR_RESULTADO_SOLICITADO")
            estado["decision_emision"]["adoptada"] = True
            ruta.write_text(json.dumps(estado), encoding="utf-8")
            habilitada = adq_suficiencia.proyecta_consumidor(
                estado["decision_emision"]["consumidor"], raiz=raiz,
                resultado_id="RESULT-SUCESOR-SINTETICO",
                uso_solicitado="MEDICION-GEN2")
            self.assertEqual(
                habilitada["accion_consumidor"],
                "PUEDE_EMITIR_USO_DECLARADO")

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
        self.assertEqual(r["contrato"]["version"], "CONSULTA-GEN2-v2")
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
