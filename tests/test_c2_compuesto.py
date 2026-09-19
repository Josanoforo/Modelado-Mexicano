#!/usr/bin/env python3
"""Falsadores del C2 compuesto sobre los cruces `RESERVADA`.

ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 (19/sep/2026).
Spec congelada: `forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md`.

Cinco cosas, ninguna de ellas "el código corre":

  (1) CONTROL DE REPRODUCCIÓN, externo y gratuito (spec §7). El par
      `localidad × edad` de ENIF ya fue piloteado -- por eso NO está en la
      lista `RESERVADA` -- y `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001`
      trae sus ocho puntos C2 sellados. Este procedimiento, con los mismos
      marginales citados y el mismo nacional, debe reproducirlos al bit
      (|delta| <= 1e-12). Es la única prueba del archivo que compara
      contra un número del árbol y no contra un fixture.
  (2) La incertidumbre NO se fabrica: cero IC en las emisiones, y el rango
      diagnóstico no se deja leer como IC.
  (3) Los casos que dirección nombró salen NO-EMITIBLE, por la causa que
      les corresponde y no por otra.
  (4) La emisión no consume la reserva ni adopta nada.
  (5) La forma se IMPORTA de `tests/test_celda_d_c2.py`; si alguien la
      reimplementa en `tools/c2_compuesto.py`, este archivo lo dice.

CERO MICRODATO. Los únicos números que este archivo toca son marginales
ya sellados y publicados por el árbitro.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
import sys

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "tools"))

import c2_compuesto as C2  # noqa: E402  (`tools/` va en sys.path; no se
# añade `tools/__init__.py`: convertir `tools/` en paquete cambiaría los
# imports de todo el árbol y está fuera del perímetro de este acto)

CALC_SELLADO = (RAIZ / "data" / "corrida0"
                / "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
                / "resultados.json")

# Marginales sellados del par YA PILOTEADO (spec §7). Se citan, no se
# recalculan: `CALC-…-0001/spec.yaml:marginales_sellados_D9`.
MARG_PILOTEADO = {
    "E1": 0.432063, "E2": 0.375709, "E3": 0.327505, "E4": 0.277317,
    "L1": 0.409255, "L2": 0.329868,
}
NAC_PILOTEADO = 0.357153
UMBRAL_REPRODUCCION = 1e-12


class ControlDeReproduccion(unittest.TestCase):
    """(1) spec §7 -- rama negativa explícita, sin ajustar nada."""

    def test_reproduce_los_ocho_C2_ya_sellados(self):
        if not CALC_SELLADO.exists():
            self.skipTest(f"NO-EJECUTABLE: falta {CALC_SELLADO.relative_to(RAIZ)} "
                          f"-- no es un NO-REPRODUCE piadoso")
        sellados = json.loads(CALC_SELLADO.read_text(encoding="utf-8"))["resultados"]
        comparadas, deltas = 0, []
        for l in ("L1", "L2"):
            for e in ("E1", "E2", "E3", "E4"):
                # Las claves `…-REDERIVADO-…` quedan FUERA a propósito
                # (spec §7): re-derivan los marginales desde microdato en
                # vez de citarlos.
                clave = f"RESULT-DIN-LXE8-C2-P-{l}x{e}"
                self.assertIn(clave, sellados)
                mio = C2.piso_log_aditivo(
                    {"desenlace_id": "ahorra_solo_informal", "p": MARG_PILOTEADO[l]},
                    {"desenlace_id": "ahorra_solo_informal", "p": MARG_PILOTEADO[e]},
                    {"desenlace_id": "ahorra_solo_informal", "p": NAC_PILOTEADO},
                )["p"]
                deltas.append((clave, sellados[clave] - mio))
                comparadas += 1
        self.assertEqual(comparadas, 8, "A.13: el control debe examinar las 8 celdas")
        malas = [(k, d) for k, d in deltas if abs(d) > UMBRAL_REPRODUCCION]
        self.assertFalse(
            malas,
            "NO-REPRODUCE (no se ajusta nada; invalida la afirmación de que "
            "este procedimiento ejecuta la receta sellada, no las emisiones): "
            + "; ".join(f"{k} delta={d:+.3e}" for k, d in malas))

    def test_el_nacional_del_acto_es_el_del_CALC_sellado(self):
        self.assertEqual(C2.NACIONALES["ahorra_solo_informal"]["p"], NAC_PILOTEADO)
        self.assertEqual(C2.NACIONALES["ahorra_solo_informal"]["n"], 13502)
        self.assertIsNone(C2.NACIONALES["ahorra_solo_informal"]["ic95"],
                          "es DERIVADO y no tiene IC propio; inventarle uno "
                          "es fabricar incertidumbre")


class IncertidumbreNoFabricada(unittest.TestCase):
    """(2) spec §5."""

    @classmethod
    def setUpClass(cls):
        cls.filas = C2.emisiones()

    def test_cero_IC_en_todas_las_emisiones(self):
        self.assertGreater(len(self.filas), 0, "A.13: 0 filas no prueba nada")
        con_ic = [f for f in self.filas if f["ic95_inf"] != "" or f["ic95_sup"] != ""]
        self.assertFalse(con_ic, f"{len(con_ic)} emisiones traen IC; la "
                                 f"covarianza no está sellada")

    def test_el_tipo_de_incertidumbre_es_el_declarado(self):
        tipos = {f["tipo_incertidumbre"] for f in self.filas}
        self.assertEqual(tipos, {"NO-PROPAGADA-COVARIANZA-NO-SELLADA"})

    def test_el_rango_diagnostico_no_se_deja_leer_como_IC(self):
        for f in self.filas:
            self.assertEqual(f["diagnostico_rango_es_ic"], "NO")

    def test_el_rango_diagnostico_contiene_al_punto(self):
        """Si no lo contuviera, sería otra cosa mal nombrada."""
        for f in self.filas:
            if f["diagnostico_rango_inf"] == "":
                continue
            self.assertLessEqual(f["diagnostico_rango_inf"], f["p_c2"] + 1e-12,
                                 f["resultado_id"])
            self.assertGreaterEqual(f["diagnostico_rango_sup"], f["p_c2"] - 1e-12,
                                    f["resultado_id"])

    def test_todo_punto_cae_estrictamente_dentro_de_cero_uno(self):
        for f in self.filas:
            self.assertTrue(0.0 < f["p_c2"] < 1.0, f["resultado_id"])

    def test_el_supuesto_viaja_en_cada_emision(self):
        for f in self.filas:
            self.assertEqual(f["supuesto"], "sin-interaccion")
            self.assertNotIn("independencia", json.dumps(f, ensure_ascii=False),
                             "rótulo prohibido (spec §2)")


class DictamenDeEmisibilidad(unittest.TestCase):
    """(3) spec §4 -- la causa correcta, no cualquier causa."""

    @classmethod
    def setUpClass(cls):
        cls.d = C2.dictamen()

    def test_examina_los_22_pares_reservados(self):
        pares = {f["celda_id_marcador"] for f in self.d}
        self.assertEqual(len(pares), 22,
                         "A.13: el dictamen debe cubrir los 22 `RESERVADA` "
                         "del marcador, ni uno menos")
        self.assertEqual(len(C2.pares_reservados()), 22)

    def test_ningun_veredicto_queda_sin_causa(self):
        for f in self.d:
            if f["veredicto"] == "NO-EMITIBLE":
                self.assertTrue(f["causa"].strip(), f["celda_id_marcador"])
            else:
                self.assertEqual(f["causa"], "", f["celda_id_marcador"])

    def test_formalidad_de_ENIF_sale_por_A_bis_4(self):
        filas = [f for f in self.d if "formalidad" in f["par"]
                 and "enif" in f["regla"]]
        self.assertTrue(filas)
        for f in filas:
            self.assertEqual(f["veredicto"], "NO-EMITIBLE")
            self.assertIn("A-BIS-4 UNIVERSO-RESTRINGIDO", f["causa"])

    def test_ENUT_reparto_por_sexo_edad_sale_por_falta_de_desenlace_comun(self):
        filas = [f for f in self.d if "enut" in f["regla"]]
        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["veredicto"], "NO-EMITIBLE")
        self.assertIn("SIN-DESENLACE-BINARIO-COMUN", filas[0]["causa"])

    def test_ningun_marginal_degenerado_pasa(self):
        """p = 0 o 1 se RECHAZA, no se recorta ni se sustituye."""
        with self.assertRaises(Exception):
            C2.piso_log_aditivo({"desenlace_id": "d", "p": 0.0},
                                {"desenlace_id": "d", "p": 0.5},
                                {"desenlace_id": "d", "p": 0.5})

    def test_el_par_se_parte_contra_los_ejes_y_no_contra_la_letra_x(self):
        """`escolaridad_proxyxsexo` tiene una `x` adentro del nombre."""
        self.assertEqual(
            C2._parte_el_par("escolaridad_proxyxsexo",
                             {"escolaridad_proxy", "sexo", "edad"}),
            ("escolaridad_proxy", "sexo"))

    def test_la_unidad_la_pone_el_arbitro_no_el_marcador(self):
        """ENCIG: el árbitro dice TRÁMITE, el marcador dice persona."""
        encig = [f for f in self.d if "encig" in f["regla"]]
        self.assertTrue(encig)
        for f in encig:
            self.assertIn("TRÁMITE", f["unidad_dato_arbitro"])
            self.assertEqual(f["unidad_dato_marcador"], "persona")

    def test_todo_emitible_trae_nacional_del_mismo_desenlace(self):
        for f in self.d:
            if f["veredicto"] != "EMITIBLE":
                continue
            self.assertIn(f["desenlace_id"], C2.NACIONALES)
            self.assertEqual(f["nacional_p"],
                             C2.NACIONALES[f["desenlace_id"]]["p"])


class EmitirNoConsumeNiAdopta(unittest.TestCase):
    """(4) spec §6 -- la firma es explícita: una emisión no pasa a
    adoptada por uso."""

    def test_toda_emision_nace_EMITIDA_SIN_EVALUAR(self):
        estados = {f["estado"] for f in C2.emisiones()}
        self.assertEqual(estados, {"EMITIDA-SIN-EVALUAR"})

    def test_ninguna_emision_reclama_estado_de_adopcion(self):
        prohibidos = ("ADOPTADO", "ADOPTADA", "IDENTICO")
        for f in C2.emisiones():
            texto = json.dumps(f, ensure_ascii=False).upper()
            for p in prohibidos:
                self.assertNotIn(p, texto, f["resultado_id"])

    def test_los_cruces_siguen_RESERVADA_en_el_marcador(self):
        """Emitir no consume: el marcador no se toca en P1/P2."""
        self.assertEqual(len(C2.pares_reservados()), 22)

    def test_ninguna_emision_trae_R_del_cruce(self):
        """Este acto no deriva ni mira `R` de ningún cruce (spec §8)."""
        for f in C2.emisiones():
            self.assertNotIn("R", set(f.keys()))


class LaFormaSeImportaNoSeReimplementa(unittest.TestCase):
    """(5) spec §2."""

    def test_c2_compuesto_importa_la_funcion_sellada(self):
        fuente = (RAIZ / "tools" / "c2_compuesto.py").read_text(encoding="utf-8")
        self.assertIn("from test_celda_d_c2 import piso_log_aditivo", fuente)
        self.assertIsNone(
            re.search(r"^def piso_log_aditivo", fuente, re.M),
            "la forma de C2 se cita, no se reinventa")

    def test_es_la_misma_funcion_objeto(self):
        import test_celda_d_c2 as sellado
        self.assertIs(C2.piso_log_aditivo, sellado.piso_log_aditivo)


def corre() -> list[str]:
    """Arnés para `tests/check.py`: devuelve la lista de errores."""
    # `check.py` carga este archivo con `spec_from_file_location` bajo otro
    # nombre y SIN registrarlo en `sys.modules`, así que
    # `sys.modules[__name__]` da KeyError. Se recogen las clases de
    # `globals()`, que existe en las dos formas de ejecución.
    cargador = unittest.TestLoader()
    suite = unittest.TestSuite(
        cargador.loadTestsFromTestCase(obj)
        for obj in list(globals().values())
        if isinstance(obj, type) and issubclass(obj, unittest.TestCase)
        and obj is not unittest.TestCase)
    import os
    with open(os.devnull, "w") as nulo:
        res = unittest.TextTestRunner(stream=nulo, verbosity=0).run(suite)
    if res.testsRun == 0:
        return ["`tests/test_c2_compuesto.py` no expuso ningun caso"]
    return [f"{caso}: {traza.strip().splitlines()[-1][:220]}"
            for caso, traza in list(res.failures) + list(res.errors)]


if __name__ == "__main__":
    unittest.main(verbosity=2)
