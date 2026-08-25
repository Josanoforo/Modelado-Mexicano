#!/usr/bin/env python3
"""Pruebas del scoring sintético ADV1-M3; nunca cargan celdas reales."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RUTA_MODULO = ROOT / "forense" / "prereg-duelo-v2" / "scoring-adv1-m3.py"
SPEC = importlib.util.spec_from_file_location("scoring_adv1_m3", RUTA_MODULO)
SCORING = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = SCORING
SPEC.loader.exec_module(SCORING)


def configuracion(principal: str = "L_SOLO_vs_M", **cambios):
    base = {
        "corredores_activos": [
            {"id": "L_SOLO", "familia": "L", "variante": "solo"},
            {"id": "L_CORPUS", "familia": "L", "variante": "corpus"},
            {"id": "M", "familia": "M", "variante": "principal"},
            {"id": "E", "familia": "E", "variante": "combinacion"},
        ],
        "comparaciones_l_m": [
            {"id": "L_SOLO_vs_M", "l_id": "L_SOLO", "m_id": "M"},
            {"id": "L_CORPUS_vs_M", "l_id": "L_CORPUS", "m_id": "M"},
        ],
        "comparacion_principal_id": principal,
        "e_id": "E",
        "delta": 0.10,
        "nivel_ic": 0.80,
        "seed": 20260824,
        "replicas": 200,
    }
    base.update(cambios)
    return base


def celda(id_celda: str, l_solo: float, l_corpus: float, m: float, e: float, **extra):
    resultado = {
        "id_celda": id_celda,
        "estado": "EVALUABLE",
        "mediciones": {
            "L_SOLO": {"skill": l_solo, "cubierto_r": True},
            "L_CORPUS": {"skill": l_corpus, "cubierto_r": False},
            "M": {"skill": m, "cubierto_r": True},
            "E": {"skill": e, "cubierto_r": False},
        },
    }
    resultado.update(extra)
    return resultado


def documento(celdas, principal: str = "L_SOLO_vs_M", **cambios_config):
    return {
        "configuracion": configuracion(principal, **cambios_config),
        "celdas": celdas,
    }


def paquete_para_intervalo(lo: float, hi: float, puntos=None):
    puntos = puntos or {}
    return {
        "a": {"ic_lo": 0.20, "ic_hi": 0.40, "punto": puntos.get("L", 0.30)},
        "a_id": "L_SOLO",
        "b": {"ic_lo": 0.10, "ic_hi": 0.30, "punto": puntos.get("M", 0.20)},
        "b_id": "M",
        "diferencia": {"ic_lo": lo, "ic_hi": hi, "punto": puntos.get("D", 0.0)},
        "n_celdas": 2,
    }


class ConfiguracionTests(unittest.TestCase):
    def test_l_solo_y_l_corpus_permanecen_separados(self):
        resultado = SCORING.ejecutar_scoring(
            documento([celda("C1", 0.1, 0.8, 0.2, 0.4), celda("C2", 0.1, 0.8, 0.2, 0.4)])
        )
        corredores = resultado["agregados"]["corredores"]
        self.assertEqual(0.1, corredores["L_SOLO"]["punto"])
        self.assertEqual(0.8, corredores["L_CORPUS"]["punto"])
        self.assertNotEqual(corredores["L_SOLO"], corredores["L_CORPUS"])

    def test_ambas_comparaciones_l_m_se_calculan(self):
        resultado = SCORING.ejecutar_scoring(documento([celda("C1", 0.4, 0.7, 0.2, 0.5)]))
        comparaciones = resultado["agregados"]["comparaciones"]
        self.assertAlmostEqual(0.2, comparaciones["L_SOLO_vs_M"]["punto"])
        self.assertAlmostEqual(0.5, comparaciones["L_CORPUS_vs_M"]["punto"])
        self.assertIn("E_vs_L_SOLO", comparaciones)
        self.assertIn("E_vs_L_CORPUS", comparaciones)
        self.assertIn("E_vs_M", comparaciones)

    def test_falta_scope_falla_cerrada_sin_default(self):
        for valor in (None, ""):
            datos = configuracion()
            if valor is None:
                del datos["comparacion_principal_id"]
            else:
                datos["comparacion_principal_id"] = valor
            with self.subTest(valor=valor), self.assertRaises(SCORING.ErrorScoring) as captura:
                SCORING.validar_configuracion(datos)
            self.assertEqual("SCOPE_ADJUDICANTE_NO_PREDECLARADO", captura.exception.codigo)
            self.assertNotIn("veredicto", captura.exception.__dict__)

    def test_scope_se_valida_antes_de_las_mediciones(self):
        entrada = {"configuracion": configuracion(), "celdas": "MEDICIONES_INVALIDAS"}
        del entrada["configuracion"]["comparacion_principal_id"]
        with self.assertRaises(SCORING.ErrorScoring) as captura:
            SCORING.ejecutar_scoring(entrada)
        self.assertEqual("SCOPE_ADJUDICANTE_NO_PREDECLARADO", captura.exception.codigo)

    def test_id_inexistente_duplicado_o_familia_incorrecta_falla(self):
        casos = []
        inexistente = configuracion(principal="NO_EXISTE")
        casos.append(inexistente)
        duplicado = configuracion()
        duplicado["corredores_activos"][1]["id"] = "L_SOLO"
        casos.append(duplicado)
        familia = configuracion()
        familia["comparaciones_l_m"][0]["l_id"] = "M"
        casos.append(familia)
        for caso in casos:
            with self.subTest(caso=caso):
                with self.assertRaises(SCORING.ErrorScoring):
                    SCORING.validar_configuracion(caso)

    def test_roles_requeridos_no_se_colapsan(self):
        datos = configuracion()
        datos["corredores_activos"][1]["variante"] = "solo"
        with self.assertRaisesRegex(SCORING.ErrorScoring, "corredor L/"):
            SCORING.validar_configuracion(datos)

    def test_configuracion_y_cli_contradictorias_fallan(self):
        cfg = SCORING.validar_configuracion(configuracion())
        argumentos = argparse.Namespace(
            comparacion_principal_id="L_CORPUS_vs_M",
            delta=None,
            nivel_ic=None,
            replicas=None,
            seed=None,
        )
        with self.assertRaises(SCORING.ErrorScoring) as captura:
            SCORING.validar_aserciones_cli(cfg, argumentos)
        self.assertEqual("CONFIGURACION_CLI_CONTRADICTORIA", captura.exception.codigo)

    def test_replicas_default_tecnico_es_visible_y_reemplazable(self):
        datos = configuracion()
        del datos["replicas"]
        self.assertEqual(10_000, SCORING.validar_configuracion(datos).replicas)
        datos["replicas"] = 17
        self.assertEqual(17, SCORING.validar_configuracion(datos).replicas)

    def test_hash_semantico_no_depende_del_orden_de_listas(self):
        izquierda = SCORING.validar_configuracion(configuracion())
        derecha_datos = configuracion()
        derecha_datos["corredores_activos"].reverse()
        derecha_datos["comparaciones_l_m"].reverse()
        derecha = SCORING.validar_configuracion(derecha_datos)
        self.assertEqual(izquierda.hash_configuracion, derecha.hash_configuracion)


class PareoYBootstrapTests(unittest.TestCase):
    def test_comparacion_reutiliza_indices_para_extremos_y_diferencia(self):
        cfg = SCORING.validar_configuracion(configuracion(replicas=2))
        matriz = SCORING.construir_matriz_mediciones(
            [celda("A", 0.0, 10.0, 1.0, 3.0), celda("B", 2.0, 20.0, 5.0, 7.0)],
            cfg,
        )
        conjunto = SCORING.construir_universo_pareado(
            matriz, "L_SOLO", "M", "L_SOLO_vs_M"
        )
        secuencia = ((0, 0), (1, 1))
        seed_scope = SCORING.derivar_seed_scope(cfg.seed, conjunto.scope_id)
        with mock.patch.object(
            SCORING, "generar_indices_bootstrap", return_value=secuencia
        ) as generador:
            resultado = SCORING.bootstrap_pareado(conjunto, cfg)
        generador.assert_called_once_with(2, 2, seed_scope)
        self.assertTrue(resultado["bootstrap"]["indices_compartidos"])
        self.assertAlmostEqual(-2.0, resultado["diferencia"]["punto"])

    def test_ausencia_auxiliar_no_excluye_scope_principal(self):
        completa = celda("OK", 0.4, 0.5, 0.2, 0.3)
        ausente = celda("FALTA", 0.4, 0.5, 0.2, 0.3)
        del ausente["mediciones"]["E"]
        no_evaluable = celda("NO", 0.4, 0.5, 0.2, 0.3, estado="NO_EVALUABLE")
        resultado = SCORING.ejecutar_scoring(documento([ausente, completa, no_evaluable]))
        self.assertEqual(
            ["FALTA", "OK"],
            [fila["id_celda"] for fila in resultado["celdas"]["incluidas"]],
        )
        self.assertEqual(1, resultado["celdas"]["n_excluidas"])
        self.assertEqual(2, resultado["agregados"]["corredores"]["L_SOLO"]["n_celdas"])

    def test_disponibilidad_no_puede_cambiar_la_l_seleccionada(self):
        cfg = SCORING.validar_configuracion(configuracion("L_SOLO_vs_M"))
        solo_ausente = celda("FALTA_L_SELECCIONADA", 0.4, 9.0, 0.2, 0.3)
        del solo_ausente["mediciones"]["L_SOLO"]
        completa = celda("OK", 0.5, 0.1, 0.2, 0.3)
        conjunto = SCORING.construir_conjunto_pareado([solo_ausente, completa], cfg)
        self.assertEqual("L_SOLO", cfg.l_id_adjudicado)
        self.assertEqual(["OK"], [item.id_celda for item in conjunto.incluidas])

    def test_estado_indecidible_se_distingue_y_no_vota(self):
        indecidible = celda("I", 0.5, 0.4, 0.2, 0.3, estado="INDECIDIBLE")
        resultado = SCORING.ejecutar_scoring(documento([indecidible]))
        self.assertEqual("INDECIDIBLE", resultado["celdas"]["incluidas"][0]["estado"])
        self.assertEqual("GANA_L", resultado["secuencia"]["veredicto"]["codigo"])

    def test_cambiar_scope_no_cambia_agregados(self):
        celdas = [celda("A", 0.2, 0.8, 0.4, 0.5), celda("B", 0.7, 0.1, 0.3, 0.6)]
        solo = SCORING.ejecutar_scoring(documento(celdas, "L_SOLO_vs_M"))
        corpus = SCORING.ejecutar_scoring(documento(celdas, "L_CORPUS_vs_M"))
        self.assertEqual(solo["agregados"], corpus["agregados"])
        self.assertNotEqual(solo["l_id_adjudicado"], corpus["l_id_adjudicado"])

    def test_orden_de_entrada_no_cambia_scope_ni_resultado(self):
        celdas = [celda("Z", 0.6, 0.3, 0.2, 0.4), celda("A", 0.2, 0.8, 0.1, 0.5)]
        directo = SCORING.ejecutar_scoring(documento(celdas))
        inverso = SCORING.ejecutar_scoring(documento(list(reversed(celdas))))
        self.assertEqual(directo["l_id_adjudicado"], inverso["l_id_adjudicado"])
        self.assertEqual(directo, inverso)


class UniversosPorScopeTests(unittest.TestCase):
    def fixture(self):
        return [
            celda("A", 0.8, 0.4, 0.2, 0.5),
            celda("B", 0.2, 0.6, 0.8, 0.7),
            celda("C", 0.5, 0.3, 0.1, 0.4),
        ]

    def test_scope_principal_es_identico_si_falta_e(self):
        completo = SCORING.ejecutar_scoring(documento(self.fixture()))
        sin_e = self.fixture()
        del sin_e[1]["mediciones"]["E"]
        reducido = SCORING.ejecutar_scoring(documento(sin_e))
        self.assertEqual(completo["scope_principal"], reducido["scope_principal"])

    def test_scope_principal_es_identico_si_falta_l_no_seleccionada(self):
        completo = SCORING.ejecutar_scoring(documento(self.fixture()))
        sin_l_auxiliar = self.fixture()
        del sin_l_auxiliar[1]["mediciones"]["L_CORPUS"]
        reducido = SCORING.ejecutar_scoring(documento(sin_l_auxiliar))
        self.assertEqual(completo["scope_principal"], reducido["scope_principal"])

    def test_falta_l_seleccionada_excluye_solo_del_principal(self):
        celdas = self.fixture()
        del celdas[1]["mediciones"]["L_SOLO"]
        resultado = SCORING.ejecutar_scoring(documento(celdas))
        universo = resultado["scope_principal"]["universo"]
        self.assertEqual(["A", "C"], universo["ids_incluidos"])
        exclusion = next(fila for fila in universo["excluidas"] if fila["id_celda"] == "B")
        self.assertEqual(
            ["MEDICION_AUSENTE_O_NO_EVALUABLE:L_SOLO"], exclusion["motivos"]
        )

    def test_falta_m_excluye_solo_del_principal(self):
        celdas = self.fixture()
        del celdas[1]["mediciones"]["M"]
        resultado = SCORING.ejecutar_scoring(documento(celdas))
        universo = resultado["scope_principal"]["universo"]
        self.assertEqual(["A", "C"], universo["ids_incluidos"])
        exclusion = next(fila for fila in universo["excluidas"] if fila["id_celda"] == "B")
        self.assertEqual(["MEDICION_AUSENTE_O_NO_EVALUABLE:M"], exclusion["motivos"])

    def test_cada_comparacion_y_marginal_declara_n_e_ids(self):
        resultado = SCORING.ejecutar_scoring(documento(self.fixture()))
        for agregado in resultado["agregados"]["corredores"].values():
            self.assertEqual(agregado["n_celdas"], len(agregado["ids_incluidos"]))
            self.assertEqual(
                agregado["ids_incluidos"], agregado["universo"]["ids_incluidos"]
            )
        for agregado in resultado["agregados"]["comparaciones"].values():
            self.assertEqual(agregado["n_celdas"], len(agregado["ids_incluidos"]))
            self.assertEqual(
                agregado["ids_incluidos"], agregado["universo"]["ids_incluidos"]
            )

    def test_comparaciones_e_son_pareadas_sin_imputacion(self):
        celdas = self.fixture()
        del celdas[1]["mediciones"]["E"]
        del celdas[2]["mediciones"]["L_SOLO"]
        resultado = SCORING.ejecutar_scoring(documento(celdas))
        comparaciones = resultado["agregados"]["comparaciones"]
        self.assertEqual(["A"], comparaciones["E_vs_L_SOLO"]["ids_incluidos"])
        self.assertEqual(["A", "C"], comparaciones["E_vs_M"]["ids_incluidos"])
        self.assertEqual(
            comparaciones["E_vs_L_SOLO"]["a"]["n_celdas"],
            comparaciones["E_vs_L_SOLO"]["diferencia"]["n_celdas"],
        )
        self.assertEqual(
            comparaciones["E_vs_L_SOLO"]["b"]["n_celdas"],
            comparaciones["E_vs_L_SOLO"]["diferencia"]["n_celdas"],
        )

    def test_seed_determinista_y_composicion_independiente_del_seed(self):
        celdas = self.fixture()
        uno = SCORING.ejecutar_scoring(documento(celdas, seed=11))
        repetido = SCORING.ejecutar_scoring(documento(celdas, seed=11))
        otro = SCORING.ejecutar_scoring(documento(celdas, seed=12))
        self.assertEqual(SCORING.serializar_json(uno), SCORING.serializar_json(repetido))
        self.assertEqual(
            uno["scope_principal"]["universo"], otro["scope_principal"]["universo"]
        )
        self.assertNotEqual(
            uno["scope_principal"]["bootstrap"]["sha256_indices"],
            otro["scope_principal"]["bootstrap"]["sha256_indices"],
        )


class SecuenciaTests(unittest.TestCase):
    def adjudicar(self, lo, hi, puntos=None, principal="L_SOLO_vs_M"):
        cfg = SCORING.validar_configuracion(configuracion(principal))
        paquete = paquete_para_intervalo(lo, hi, puntos)
        if principal == "L_CORPUS_vs_M":
            paquete["a_id"] = "L_CORPUS"
        return SCORING.adjudicar_secuencia(cfg, paquete)

    def test_seleccion_l_solo_gobierna_aunque_l_corpus_sea_mejor(self):
        celdas = [celda("A", -0.4, 5.0, 0.4, 100.0), celda("B", -0.4, 5.0, 0.4, 100.0)]
        resultado = SCORING.ejecutar_scoring(documento(celdas, "L_SOLO_vs_M"))
        self.assertEqual("L_SOLO", resultado["l_id_adjudicado"])
        self.assertEqual("GANA_M", resultado["secuencia"]["veredicto"]["codigo"])
        self.assertEqual(5.0, resultado["resultados_auxiliares"]["l_no_seleccionadas"][0]["agregado"]["punto"])

    def test_seleccion_l_corpus_gobierna_aunque_l_solo_sea_mejor(self):
        celdas = [celda("A", 5.0, 0.5, 0.1, 100.0), celda("B", 5.0, 0.5, 0.1, 100.0)]
        resultado = SCORING.ejecutar_scoring(documento(celdas, "L_CORPUS_vs_M"))
        self.assertEqual("L_CORPUS", resultado["l_id_adjudicado"])
        self.assertEqual("GANA_L", resultado["secuencia"]["veredicto"]["codigo"])
        self.assertEqual(5.0, resultado["resultados_auxiliares"]["l_no_seleccionadas"][0]["agregado"]["punto"])

    def test_punto_positivo_no_adjudica_si_intervalo_no_corresponde(self):
        con_punto_enorme = self.adjudicar(-0.2, 0.3, {"D": 999.0})
        con_punto_opuesto = self.adjudicar(-0.2, 0.3, {"D": -999.0})
        self.assertEqual("INDETERMINADO", con_punto_enorme["veredicto"]["codigo"])
        self.assertEqual(con_punto_enorme, con_punto_opuesto)

    def test_equivalentes_e_indeterminado_son_distintos(self):
        equivalentes = self.adjudicar(-0.05, 0.05)
        indeterminado = self.adjudicar(-0.20, 0.20)
        self.assertEqual("EQUIVALENTES", equivalentes["veredicto"]["codigo"])
        self.assertEqual("INDETERMINADO", indeterminado["veredicto"]["codigo"])

    def test_gana_l_y_gana_m(self):
        self.assertEqual("GANA_L", self.adjudicar(0.11, 0.30)["veredicto"]["codigo"])
        self.assertEqual("GANA_M", self.adjudicar(-0.30, -0.11)["veredicto"]["codigo"])

    def test_ninguno_supera_b_detiene_despues_de_paso_1(self):
        cfg = SCORING.validar_configuracion(configuracion())
        paquete = paquete_para_intervalo(-0.3, 0.3)
        paquete["a"]["ic_lo"] = -0.2
        paquete["b"]["ic_lo"] = 0.0
        resultado = SCORING.adjudicar_secuencia(cfg, paquete)
        self.assertEqual("NINGUNO_SUPERA_B", resultado["veredicto"]["codigo"])
        self.assertIsNone(resultado["paso_2"])
        self.assertIsNone(resultado["veredicto"]["ganador_id"])

    def test_e_permanece_no_gating(self):
        base = [celda("A", 0.5, 0.2, 0.1, -999.0), celda("B", 0.5, 0.2, 0.1, -999.0)]
        alta = [celda("A", 0.5, 0.2, 0.1, 999.0), celda("B", 0.5, 0.2, 0.1, 999.0)]
        resultado_bajo = SCORING.ejecutar_scoring(documento(base))
        resultado_alto = SCORING.ejecutar_scoring(documento(alta))
        self.assertEqual(resultado_bajo["secuencia"], resultado_alto["secuencia"])
        self.assertNotEqual(
            resultado_bajo["resultados_auxiliares"]["e"],
            resultado_alto["resultados_auxiliares"]["e"],
        )

    def test_paso_0_no_altera_veredicto(self):
        cubre = [celda("A", 0.5, 0.2, 0.1, 0.3)]
        no_cubre = [celda("A", 0.5, 0.2, 0.1, 0.3)]
        for medicion in no_cubre[0]["mediciones"].values():
            medicion["cubierto_r"] = not medicion["cubierto_r"]
        uno = SCORING.ejecutar_scoring(documento(cubre))
        otro = SCORING.ejecutar_scoring(documento(no_cubre))
        self.assertNotEqual(uno["paso_0"], otro["paso_0"])
        self.assertEqual(uno["secuencia"], otro["secuencia"])
        self.assertFalse(uno["paso_0"]["gating"])

    def test_posicion_no_definida_por_spec_en_ambos_lados(self):
        for lo, hi in ((0.02, 0.20), (-0.20, -0.02)):
            with self.subTest(lo=lo, hi=hi):
                resultado = self.adjudicar(lo, hi)
                self.assertEqual("FALLO_CERRADO", resultado["estado_adjudicacion"])
                self.assertEqual(
                    "POSICION_NO_DEFINIDA_POR_SPEC", resultado["fallo_cerrado"]["codigo"]
                )
                self.assertIsNone(resultado["veredicto"])


class SalidasTests(unittest.TestCase):
    def test_json_y_tsv_reproducibles_byte_a_byte_utf8_lf_sin_bom(self):
        entrada = documento([celda("A", 0.5, 0.2, 0.1, 0.3), celda("B", 0.4, 0.3, 0.2, 0.5)])
        primero = SCORING.ejecutar_scoring(entrada)
        segundo = SCORING.ejecutar_scoring(json.loads(json.dumps(entrada)))
        for serializador in (SCORING.serializar_json, SCORING.serializar_tsv):
            a, b = serializador(primero), serializador(segundo)
            self.assertEqual(a, b)
            self.assertFalse(a.startswith(b"\xef\xbb\xbf"))
            self.assertNotIn(b"\r\n", a)
            self.assertTrue(a.endswith(b"\n"))
        with tempfile.TemporaryDirectory() as temporal:
            ruta = Path(temporal) / "salida.json"
            SCORING.escribir_salida(ruta, SCORING.serializar_json(primero))
            self.assertEqual(SCORING.serializar_json(primero), ruta.read_bytes())

    def test_salida_registra_scope_parametros_hash_y_auxiliares(self):
        resultado = SCORING.ejecutar_scoring(documento([celda("A", 0.5, 0.2, 0.1, 0.3)]))
        self.assertEqual("L_SOLO_vs_M", resultado["comparacion_principal_id"])
        self.assertEqual("L_SOLO", resultado["l_id_adjudicado"])
        self.assertEqual(["L_CORPUS"], resultado["l_ids_no_seleccionados"])
        self.assertEqual(64, len(resultado["hash_configuracion"]))
        for clave in ("seed", "replicas", "nivel_ic", "delta"):
            self.assertIn(clave, resultado)
        self.assertIn("e", resultado["resultados_auxiliares"])

    def test_no_aparece_empate(self):
        resultado = SCORING.ejecutar_scoring(documento([celda("A", 0.2, 0.7, 0.2, 0.4)]))
        texto = SCORING.serializar_json(resultado).decode("utf-8")
        tsv = SCORING.serializar_tsv(resultado).decode("utf-8")
        self.assertNotIn("EMPATE", texto.upper())
        self.assertNotIn("EMPATE", tsv.upper())


if __name__ == "__main__":
    unittest.main()
