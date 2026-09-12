#!/usr/bin/env python3
"""Pruebas materiales del contrato de emisión GEN2 explícita."""
from __future__ import annotations

import hashlib
import json
import unittest
from copy import deepcopy
from dataclasses import replace
from datetime import date
from pathlib import Path

from milpa.src.emisor import (
    MODO_GEN2,
    IndiceLinajeEmision,
    cargar_indice_linaje_emision,
    cargar_reglas,
    emitir_binaria_contrato,
)
from tools.baseline_temporal import (
    Objetivo,
    Observacion,
    Serie,
    seleccionar_baseline,
)
from tools.snapshot_motor_gen2 import construir_snapshot


RAIZ = Path(__file__).resolve().parents[1]


class MotorGen2Explicito(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.indice = cargar_indice_linaje_emision()
        cls.reglas = {r.id: r for r in cargar_reglas()}

    @staticmethod
    def _partes(consumidor):
        _, regla_id, conducta = consumidor.split(":", 2)
        return regla_id, conducta

    def _emite(self, regla_id, conducta, *, contexto=None,
               uso="MEDICION-GEN2", indice=None):
        regla = self.reglas[regla_id]
        salida = next(s for s in regla.entonces if s.conducta == conducta)
        return emitir_binaria_contrato(
            regla, conducta,
            dict(salida.dominio_elegible) if contexto is None else contexto,
            modo=MODO_GEN2, proposito="consulta", uso_solicitado=uso,
            indice=indice or self.indice)

    def test_01_parametro_nuevo_apto_emite_result_completo(self):
        directos = [u for u in self.indice.usos.values()
                    if u.corrida0_generacion == "GEN2"]
        self.assertTrue(directos)
        for uso in directos:
            with self.subTest(consumidor=uso.consumidor):
                regla_id, conducta = self._partes(uso.consumidor)
                regla = self.reglas[regla_id]
                salida = next(s for s in regla.entonces
                              if s.conducta == conducta)
                uso_solicitado = (
                    "DESCRIPTIVO" if salida.rol_uso == "proxy_descriptivo"
                    else "MEDICION-GEN2")
                r = self._emite(
                    regla_id, conducta, uso=uso_solicitado)
                evidencia = self.indice.resultados[
                    uso.corrida0_resultado_id]
                self.assertEqual(r.estado, "EMITE")
                self.assertEqual(r.valor_punto, evidencia.valor)
                self.assertEqual(r.resultado_id, evidencia.resultado_id)
                self.assertEqual(r.aptitud_uso, "APTA-POR-LINAJE")

    def test_02_legacy_puro_no_se_cuela_a_gen2(self):
        r = self._emite(
            "tramite.mordida.discrecional", "paga_mordida")
        self.assertEqual(r.estado, "NO_COVERAGE")
        self.assertIsNone(r.valor_punto)
        self.assertIn("no declara RESULT", r.detalle)

    def test_03_regla_mixta_expone_componentes_estructurales(self):
        r = self._emite(
            "tramite.gobierno_digital.util_sin_coercion",
            "adopta_encig2025_luz")
        self.assertEqual(r.estado, "EMITE")
        self.assertTrue(any("palancas" in x
                            for x in r.dependencias_estructurales))
        self.assertTrue(any("generadores:G1" == x
                            for x in r.dependencias_estructurales))
        self.assertTrue(any("tier:FUERTE" == x
                            for x in r.dependencias_estructurales))

    def test_04_falta_result_o_dominio_produce_no_coverage(self):
        consumidor = (
            "milpa/tramite.yaml:tramite.mordida.discrecional:"
            "paga_mordida_encig2025")
        uso = self.indice.usos[consumidor]
        resultados = dict(self.indice.resultados)
        resultados.pop(uso.corrida0_resultado_id)
        sin_result = IndiceLinajeEmision(
            resultados=resultados, usos=self.indice.usos)
        r1 = self._emite(
            "tramite.mordida.discrecional", "paga_mordida_encig2025",
            indice=sin_result)
        self.assertEqual(r1.estado, "NO_COVERAGE")
        self.assertIn("RESULT inexistente", r1.detalle)

        r2 = self._emite(
            "tramite.mordida.discrecional",
            "solicitud_o_entrega_mordida_encuci2020", contexto={})
        self.assertEqual(r2.estado, "NO_COVERAGE")
        self.assertIn("fuera del dominio elegible", r2.detalle)

    def test_05_complemento_reutiliza_padre_sin_nueva_independencia(self):
        padre = self._emite(
            "tramite.mordida.discrecional",
            "solicitud_o_entrega_mordida_encuci2020")
        q = self._emite(
            "tramite.mordida.discrecional",
            "sin_solicitud_y_sin_entrega_encuci2020")
        self.assertEqual(q.estado, "EMITE")
        self.assertEqual(q.resultado_id, padre.resultado_id)
        self.assertEqual(q.valor_punto, 1.0 - padre.valor_punto)
        self.assertEqual(
            q.derivado_de, "solicitud_o_entrega_mordida_encuci2020")
        self.assertIn("NO IMPLICA MUESTRA INDEPENDIENTE", q.camino_linaje)
        self.assertIn("transformacion:1-p", q.dependencias_estructurales)
        self.assertIn(
            "padre:tramite.mordida.discrecional:"
            "solicitud_o_entrega_mordida_encuci2020",
            q.dependencias_estructurales)

    def test_06_ola_futura_falla_en_transferencia(self):
        serie = Serie(
            encuesta="E", reactivo="R", universo="U", codificacion="C",
            segmento="S", unidad="proporcion")
        objetivo = Objetivo(
            serie, date(2022, 1, 1), date(2022, 12, 31),
            date(2021, 12, 31))
        futura = Observacion(
            serie, date(2024, 1, 1), date(2024, 12, 31),
            date(2025, 1, 1), True, 0.4, "RESULT-FUTURO", "fuente")
        r = seleccionar_baseline(objetivo, [futura])
        self.assertEqual(r["estado"], "SIN_BASELINE")
        self.assertEqual(r["excluidas"][0]["motivo"], "OLA_NO_ANTERIOR")

    def test_07_reetiquetar_generacion_no_borra_origen_heredado(self):
        consumidor = (
            "milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:"
            "recibe_remesas")
        uso = self.indice.usos[consumidor]
        evidencia = self.indice.resultados[uso.corrida0_resultado_id]
        resultados = dict(self.indice.resultados)
        resultados[evidencia.resultado_id] = replace(
            evidencia, generacion="GEN2", origen_numerico="HEREDADO")
        reetiquetado = IndiceLinajeEmision(
            resultados=resultados, usos=self.indice.usos)
        r = self._emite(
            "familia.seguro.volatilidad_ausencia_estado", "recibe_remesas",
            indice=reetiquetado)
        self.assertEqual(r.estado, "NO_COVERAGE")
        self.assertEqual(r.origen_numerico, "HEREDADO")
        self.assertEqual(r.aptitud_uso, "NO-APTA")

    def test_08_transferencia_operativa_legitima_sigue_funcionando(self):
        actual = construir_snapshot()
        esperado = json.loads((
            RAIZ / "forense" / "prereg-duelo-v2" /
            "snapshot-M-gen2-explicito-v1_2.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual(
            json.loads(json.dumps(actual, ensure_ascii=False)), esperado)
        self.assertEqual(len(actual["salidas_gen2_directas"]), 16)
        self.assertTrue(all(
            x["validacion_independiente"] == "PASA"
            for x in actual["salidas_gen2_directas"]))
        self.assertEqual(
            actual["cobertura"]["antes"]["registro_activo_total"],
            len(self.indice.usos))
        self.assertEqual(
            actual["cobertura"]["despues_modo_gen2_explicito"]
                  ["consumidores_directos_evaluados"],
            sum(u.corrida0_generacion == "GEN2"
                for u in self.indice.usos.values()))
        r = actual["transferencia_temporal_operativa"]
        self.assertEqual(r["selector"]["estado"], "EMITE")
        self.assertEqual(
            r["selector"]["resultado_id"], "RESULT-B-ENIGH-2020-P")
        self.assertEqual(r["emision"]["estado"], "EMITE")
        self.assertEqual(r["evaluacion"], "NO-EVALUACION-INDEPENDIENTE")
        self.assertEqual(
            r["emision"]["rol_seleccion"], "OBSERVACION-SERIE-PREVIA")

    def test_09_envipe_no_se_convierte_en_remesas_por_parametros_sueltos(self):
        regla = self.reglas["familia.seguro.volatilidad_ausencia_estado"]
        resultado_id = "RESULT-R-CIV-M-01-P-C1-U1"
        valor = self.indice.resultados[resultado_id].valor
        for proposito in ("consulta", "transferencia"):
            with self.subTest(proposito=proposito):
                r = emitir_binaria_contrato(
                    regla, "recibe_remesas", {}, modo=MODO_GEN2,
                    proposito=proposito, uso_solicitado="MEDICION-GEN2",
                    indice=self.indice,
                    resultado_id_seleccionado=resultado_id,
                    valor_seleccionado=valor)
                self.assertEqual(r.estado, "NO_COVERAGE")
                self.assertIsNone(r.valor_punto)
        self.assertIn("consulta no acepta selección externa", (
            emitir_binaria_contrato(
                regla, "recibe_remesas", {}, modo=MODO_GEN2,
                proposito="consulta", indice=self.indice,
                resultado_id_seleccionado=resultado_id,
                valor_seleccionado=valor).detalle))

    def test_10_consulta_no_activa_transferencia_estructurada(self):
        transferencia = construir_snapshot()["transferencia_temporal_operativa"]
        regla = self.reglas["familia.seguro.volatilidad_ausencia_estado"]
        r = emitir_binaria_contrato(
            regla, "recibe_remesas", {}, modo=MODO_GEN2,
            proposito="consulta", uso_solicitado="MEDICION-GEN2",
            indice=self.indice,
            seleccion_transferencia=transferencia["selector"])
        self.assertEqual(r.estado, "NO_COVERAGE")
        self.assertIn("consulta no acepta selección externa", r.detalle)

    def test_11_transferencia_rechaza_incompatibilidad_corte_valor_y_rol(self):
        transferencia = construir_snapshot()["transferencia_temporal_operativa"]
        seleccion = transferencia["selector"]
        regla = self.reglas["familia.seguro.volatilidad_ausencia_estado"]

        casos = []
        incompatible = deepcopy(seleccion)
        incompatible["seleccion"]["serie"]["encuesta"] = "ENVIPE"
        casos.append((incompatible, "serie seleccionada incompatible"))

        posterior = deepcopy(seleccion)
        posterior["seleccion"]["disponibilidad"] = "2022-01-01"
        casos.append((posterior, "posterior al corte temporal"))

        valor_falso = deepcopy(seleccion)
        valor_falso["seleccion"]["evidencia_procedencia"]["valor"] += 0.01
        casos.append((valor_falso, "valor seleccionado no coincide"))

        operativo = deepcopy(seleccion)
        rid_operativo = "RESULT-B-OPERATIVO-2022-P"
        operativo["resultado_id"] = rid_operativo
        operativo["seleccion"]["evidencia_procedencia"][
            "resultado_id"] = rid_operativo
        casos.append((operativo, "rol no está acreditado"))

        for contrato, causa in casos:
            with self.subTest(causa=causa):
                r = emitir_binaria_contrato(
                    regla, "recibe_remesas", {}, modo=MODO_GEN2,
                    proposito="transferencia",
                    uso_solicitado="MEDICION-GEN2", indice=self.indice,
                    seleccion_transferencia=contrato)
                self.assertEqual(r.estado, "NO_COVERAGE")
                self.assertIsNone(r.valor_punto)
                self.assertIn(causa, r.detalle)

    def test_12_cambio_de_p_sin_result_correspondiente_se_detecta(self):
        regla = self.reglas["tramite.mordida.discrecional"]
        alteradas = tuple(
            replace(s, p=s.p + 0.01)
            if s.conducta == "paga_mordida_encig2025" else s
            for s in regla.entonces)
        alterada = replace(regla, entonces=alteradas)
        r = emitir_binaria_contrato(
            alterada, "paga_mordida_encig2025", {}, modo=MODO_GEN2,
            proposito="consulta", uso_solicitado="MEDICION-GEN2",
            indice=self.indice)
        self.assertEqual(r.estado, "NO_COVERAGE")
        self.assertIn("p materializado no identifica al RESULT", r.detalle)

    def test_13_congelados_historicos_y_snapshots_previos_no_cambian(self):
        esperados = {
            "forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_0.json":
                "05350667baa245c79c3ed487aeb1403d74b4612fcae69e16845b8d42f1a5eaa8",
            "forense/prereg-duelo-v2/snapshot-M-gen2-explicito-v1_1.json":
                "95d36cef4735f85a22f0346bc04dabdab2f13724c96e9a19179996cb93bca3bb",
            "forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json":
                "b53ac6d51d1b50ce929fdf1b3e14b124c11db39fb216a15d7073a287ed3f065c",
            "data/corrida0/CALC-TRIADA-0002/resultados.json":
                "e2d0adc2a9fb9722d50a9479916129b3524cb87ce9021359ebfe755ec0e9e22a",
            "forense/prereg-duelo-v2/F5-completa-resultado-v1_0.json":
                "e1ec8765f769f76c7f649958f46b72b34fcef786bcc113f5c3cbc997c4ed0079",
        }
        for ruta, esperado in esperados.items():
            with self.subTest(ruta=ruta):
                observado = hashlib.sha256((RAIZ / ruta).read_bytes()).hexdigest()
                self.assertEqual(observado, esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
