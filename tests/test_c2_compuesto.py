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

# ACTO GEN2-CONTADORES-CONSUMO-2 (23/sep/2026): las aserciones de estado
# del marcador se evalúan contra el marcador RE-DERIVADO por
# `tools/marcador_segmento.py` en un directorio temporal, no contra el TSV
# publicado. El marcador lo publica sólo el job de derivados de verify.yml
# (el PR no puede llevarlo: `derivados_protegidos --toca`), así que entre el
# merge de un cambio de decisiones y el PR `[deriva]` el TSV publicado
# describe el estado anterior; un test sobre ese TSV no pasa en los dos.
# Se deriva hasta el punto fijo: `emitidas_sin_evaluar` sale de
# `c2_compuesto.emisiones()`, que lee las RESERVADA del TSV publicado, y
# con el TSV viejo la primera pasada da 206 emitidas y la segunda 174.
_DERIVADO: dict = {}


def _marcador_derivado() -> dict:
    """Rutas a `marcador-segmento.tsv` y `estimadores-por-segmento.yaml`
    re-derivados hasta su punto fijo (una vez por proceso) fuera del
    árbol."""
    if not _DERIVADO:
        import atexit
        import contextlib
        import io
        import shutil
        import tempfile
        import marcador_segmento as MS
        tmp = Path(tempfile.mkdtemp(prefix="c2-compuesto-marcador-"))
        atexit.register(shutil.rmtree, tmp, True)
        rutas = {"tsv": tmp / "marcador-segmento.tsv",
                 "yaml": tmp / "estimadores-por-segmento.yaml"}
        viejo = (MS.RAIZ, MS.MARCADOR_TSV, MS.ESTIMADORES_YAML, C2.MARCADOR)
        antes = None
        try:
            for _ in range(4):
                v = MS.deriva()
                MS.RAIZ, MS.MARCADOR_TSV, MS.ESTIMADORES_YAML = (
                    tmp, rutas["tsv"], rutas["yaml"])
                with contextlib.redirect_stdout(io.StringIO()):
                    MS.escribe_tsv(v["filas"])
                    MS.escribe_estimadores_yaml(v["filas"])
                MS.RAIZ = viejo[0]
                C2.MARCADOR = rutas["tsv"]
                ahora = (rutas["tsv"].read_bytes(), rutas["yaml"].read_bytes())
                if ahora == antes:
                    break
                antes = ahora
            else:
                raise AssertionError(
                    "marcador_segmento no llega a punto fijo en 4 pasadas")
        finally:
            MS.RAIZ, MS.MARCADOR_TSV, MS.ESTIMADORES_YAML, C2.MARCADOR = viejo
        _DERIVADO.update(rutas)
    return _DERIVADO


_MARCADOR_PUBLICADO = C2.MARCADOR


def setUpModule():
    C2.MARCADOR = _marcador_derivado()["tsv"]


def tearDownModule():
    C2.MARCADOR = _MARCADOR_PUBLICADO


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

    def test_examina_los_19_pares_reservados(self):
        # 22 -> 19 (ACTO GEN2-CONTADORES-CONSUMO-2, 23/sep/2026): las tres
        # celdas-D de GOB.gobierno_digital.encig2025.* (edad_x_escolaridad,
        # edad_x_sexo, escolaridad_x_sexo) se adoptaron por firma
        # (decisiones.tsv: adopcion:piso-C2-20-celdas) y dejaron de estar
        # RESERVADA en el marcador re-derivado; no queda ninguna reservada
        # de ENCIG en el TSV.
        pares = {f["celda_id_marcador"] for f in self.d}
        self.assertEqual(len(pares), 19,
                         "A.13: el dictamen debe cubrir los 19 `RESERVADA` "
                         "del marcador, ni uno menos")
        self.assertEqual(len(C2.pares_reservados()), 19)

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

    def test_la_unidad_la_pone_el_arbitro(self):
        """La emisión hereda la unidad del ÁRBITRO, no la del marcador.

        Historia, porque explica por qué este caso sigue aquí: cuando se
        escribió (base `8e455bd6`) el marcador publicaba `unidad_dato =
        persona` para ENCIG mientras el árbitro declaraba `TRÁMITE`, y el
        dictamen conservaba las dos columnas para no resolver la
        discrepancia en silencio. `GEN2-MARCADOR-PISOS-ENLACE-1` (`PR
        #883`) la corrigió aguas arriba: `_unidad_dato()` ahora lee el
        `payload` del árbitro y normaliza a `tramite`/`delito`.

        El caso NO se borra al desaparecer la discrepancia: lo que fija es
        de QUIÉN se hereda la unidad, y eso vale igual ahora que
        coinciden. Si el marcador volviera a divergir, aquí se ve.
        """
        encig = [f for f in self.d if "encig" in f["regla"]]
        envipe = [f for f in self.d if "envipe" in f["regla"]]
        # ACTO GEN2-CONTADORES-CONSUMO-2 (23/sep/2026): las tres celdas-D de
        # GOB.gobierno_digital.encig2025.* eran el único caso ENCIG de este
        # dictamen; al adoptarse por firma salen de RESERVADA y `encig`
        # queda vacío aquí (no es que el caso se borre: si un ENCIG vuelve a
        # aparecer entre los RESERVADA, este bloque sigue vigilando su
        # unidad; hoy no hay ninguno que vigilar). ENVIPE sigue presente y
        # se exige como antes.
        self.assertTrue(envipe, "ENVIPE debe seguir presente en RESERVADAS")
        for f in encig:
            self.assertIn("TRÁMITE", f["unidad_dato_arbitro"])
        for f in envipe:
            self.assertIn("DELITO", f["unidad_dato_arbitro"])
        # Post-#883 coinciden; se afirma la concordancia, no una igualdad
        # literal (el árbitro trae la glosa, el marcador el token normalizado).
        for f in encig:
            self.assertEqual(f["unidad_dato_marcador"], "tramite")
        for f in envipe:
            self.assertEqual(f["unidad_dato_marcador"], "delito")

    def test_la_emision_lleva_la_unidad_del_arbitro_no_la_del_marcador(self):
        """Lo que viaja en el RESULT es la del árbitro, con su glosa."""
        for f in C2.emisiones():
            self.assertEqual(f["unidad_dato"],
                             next(d["unidad_dato_arbitro"] for d in self.d
                                  if d["celda_id_marcador"] == f["celda_id_marcador"]
                                  and d["desenlace_id"] == f["desenlace_id"]))

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
        # 22 -> 19, mismo motivo que test_examina_los_19_pares_reservados
        # (ACTO GEN2-CONTADORES-CONSUMO-2, 23/sep/2026).
        self.assertEqual(len(C2.pares_reservados()), 19)

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


class GuardiaD14(unittest.TestCase):
    """(6) P3 · D-14 — la guardia única.

    Falla si una celda `EMITIDA-SIN-EVALUAR` sale por la vía por defecto
    del lector, o si cuenta como `ADOPTADO_ACTIVO`.

    El defecto que atrapa ya ocurrió hoy en pequeño: 8 celdas adoptadas
    por firma que el contador no veía porque dos compuertas distintas se
    leían como una. Aquí el riesgo es el simétrico y peor — que una
    emisión sin evaluar se lea como adoptada — y por eso la separación es
    estructural (clave distinta en el YAML, espacio de nombres de id
    distinto) y no una bandera dentro de un mismo diccionario.
    """

    @classmethod
    def setUpClass(cls):
        import importlib.util as _iu
        ruta = RAIZ / "milpa" / "src" / "estimadores_segmento.py"
        spec = _iu.spec_from_file_location("estimadores_segmento_d14", ruta)
        cls.E = _iu.module_from_spec(spec)
        spec.loader.exec_module(cls.E)
        cls.E.RUTA_ESTIMADORES = _marcador_derivado()["yaml"]
        cls.emitidas = cls.E.celdas_emitidas_sin_evaluar()
        cls.adoptadas = _yaml_estimadores().get("celdas") or {}

    def test_hay_algo_que_guardar(self):
        """A.13: una guardia sobre cero celdas no prueba nada."""
        # 206/20 -> 174/52 (ACTO GEN2-CONTADORES-CONSUMO-2, 23/sep/2026): las
        # 32 celdas de GOB.gobierno_digital.encig2025.* (16 edad_x_escolaridad
        # + 8 edad_x_sexo + 8 escolaridad_x_sexo) pasan de EMITIDA-SIN-EVALUAR
        # a ADOPTADO-POR-FIRMA al re-derivar el marcador tras la adopción por
        # firma de 17/sep/2026 (adopcion:piso-C2-20-celdas).
        self.assertEqual(len(self.emitidas), 174)
        self.assertEqual(len(self.adoptadas), 52)

    def test_ninguna_emitida_sale_por_la_via_por_defecto(self):
        fugas = [cid for cid in self.emitidas
                 if self.E.estimador_de_celda(cid) is not None]
        self.assertFalse(fugas, f"{len(fugas)} celdas EMITIDA-SIN-EVALUAR "
                                f"salieron sin `incluir_no_evaluadas=True`: "
                                f"{fugas[:5]}")

    def test_ninguna_emitida_cuenta_como_ADOPTADO_ACTIVO(self):
        for cid in self.emitidas:
            e = self.E.estimador_de_celda(cid, incluir_no_evaluadas=True)
            self.assertIsNotNone(e, cid)
            self.assertEqual(e["estado"], self.E.EMITIDA_SIN_EVALUAR, cid)
            self.assertNotEqual(e["estado"], self.E.ADOPTADO_ACTIVO, cid)

    def test_los_dos_espacios_de_id_no_se_tocan(self):
        self.assertFalse(set(self.emitidas) & set(self.adoptadas))
        for cid in self.emitidas:
            self.assertTrue(cid.startswith("CRUCE-EMITIDA::"), cid)
        for cid in self.adoptadas:
            self.assertFalse(cid.startswith("CRUCE-EMITIDA::"), cid)

    def test_el_flag_no_afecta_a_las_adoptadas(self):
        for cid in self.adoptadas:
            a = self.E.estimador_de_celda(cid)
            b = self.E.estimador_de_celda(cid, incluir_no_evaluadas=True)
            self.assertEqual(a, b, cid)
            self.assertEqual(a["estado"], self.E.ADOPTADO_ACTIVO, cid)

    def test_una_emitida_nunca_FABRICA_IC(self):
        """`ACTO GEN2-MARCADOR-ENLACE-2` (20/sep/2026, P3) sustituye el
        supuesto de este caso, no lo relaja.

        Se escribió cuando NINGÚN CALC había sellado el IC de una emisión
        compuesta, y entonces «nunca trae IC» y «nunca fabrica IC» eran la
        misma frase. Desde `#911`/`#916` ya no lo son: los dos CALC de IC
        traen IC réplica por réplica, y exigir el campo vacío obligaría al
        marcador a esconder una medición que el repo ya selló. Lo que la
        guardia protege -- que ningún IC nazca aquí -- se prueba ahora
        contra los RESULT sellados, que es más fuerte que probarlo contra
        la cadena vacía:

          (a) un IC presente es EXACTAMENTE el del CALC, por identidad de
              celda, y nombra su CALC en `ic95_fuente`;
          (b) una emisión que ningún CALC cubre sigue con los dos campos
              vacíos y `NO-PROPAGADA-COVARIANZA-NO-SELLADA`;
          (c) el rango diagnóstico NUNCA se deja leer como IC, con IC o sin
              él.

        Tener IC no la vuelve adoptada: eso lo guardan los otros casos de
        esta clase, intactos. El IC mide el ruido muestral de un estimador
        que SUPONE no-interacción; no mide el error de ese supuesto.
        """
        import importlib.util as _iu
        spec = _iu.spec_from_file_location(
            "marcador_segmento_ic", RAIZ / "tools" / "marcador_segmento.py")
        MS = _iu.module_from_spec(spec)
        spec.loader.exec_module(MS)
        sellados = MS.ic_de_emisiones()
        self.assertTrue(sellados, "ningún CALC de IC legible (A.13)")

        n_con_ic = 0
        for cid, e in self.emitidas.items():
            self.assertEqual(e["diagnostico_rango_es_ic"], "NO", cid)   # (c)
            rid = e["resultado_id"]
            sello = sellados.get(rid)
            if sello is None:                                            # (b)
                self.assertIn(e["ic95_inf"], ("", None), cid)
                self.assertIn(e["ic95_sup"], ("", None), cid)
                self.assertEqual(e["tipo_incertidumbre"],
                                 MS.IC_NO_PROPAGADO, cid)
                continue
            n_con_ic += 1                                                # (a)
            self.assertEqual(e["ic95_inf"], sello["ic95_inf"], cid)
            self.assertEqual(e["ic95_sup"], sello["ic95_sup"], cid)
            self.assertEqual(e["ic95_fuente"], sello["calc"], cid)
            self.assertEqual(e["tipo_incertidumbre"], MS.IC_PROPAGADO, cid)
        self.assertTrue(n_con_ic,
                        "ninguna emisión trae IC sellado: el enlace del P3 "
                        "no está haciendo nada")

    def test_emitir_no_consume_la_reserva(self):
        """Las dos cosas a la vez, en columnas distintas."""
        # 16/22 -> 13/19, mismo motivo que test_examina_los_19_pares_reservados
        # (ACTO GEN2-CONTADORES-CONSUMO-2, 23/sep/2026).
        filas = _filas_marcador()
        emitidos = [f for f in filas if f.get("emision") == "EMITIDA-SIN-EVALUAR"]
        self.assertEqual(len(emitidos), 13,
                         "13 de los 19 pares RESERVADA son emitibles")
        for f in emitidos:
            self.assertEqual(f["estado"], "RESERVADA", f["celda_id"])
        self.assertEqual(
            sum(1 for f in filas if f["estado"] == "RESERVADA"), 19,
            "emitir no consume: los 19 cruces siguen RESERVADA")


def _yaml_estimadores() -> dict:
    import yaml
    return yaml.safe_load(
        _marcador_derivado()["yaml"].read_text(
            encoding="utf-8")) or {}


def _filas_marcador() -> list[dict]:
    import csv
    ruta = _marcador_derivado()["tsv"]
    with ruta.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


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
    # Cargado por `check.py` fuera de `sys.modules`, unittest no llama a
    # los fixtures de módulo: se llaman aquí.
    setUpModule()
    try:
        with open(os.devnull, "w") as nulo:
            res = unittest.TextTestRunner(stream=nulo, verbosity=0).run(suite)
    finally:
        tearDownModule()
    if res.testsRun == 0:
        return ["`tests/test_c2_compuesto.py` no expuso ningun caso"]
    return [f"{caso}: {traza.strip().splitlines()[-1][:220]}"
            for caso, traza in list(res.failures) + list(res.errors)]


if __name__ == "__main__":
    unittest.main(verbosity=2)
