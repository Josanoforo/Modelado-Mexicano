#!/usr/bin/env python3
"""ACTO GEN2-MARCADOR-E-INFORME-1 · guardias de P1 y P2.

QUÉ DEFECTO REAL ATRAPAN (§1: el aparato tiene costo y toda guardia declara
cuál paga).

P1 -- el defecto ya ocurrido: el piloto 3 adjudicó 15 celdas en un tercer
dominio el 21/sep/2026 y `celdas_validadas`, la métrica rectora del programa,
se quedó en 73 (`NC-260921-...-3619-02`, PR #961). La causa era que la clase 1
de la métrica era una lista de dos celdas-D escritas a mano. Lo que le habría
costado a un lector: mesa leyó un tablero que decía que el programa no avanzó
el día que avanzó un tercio.

P2 -- el defecto que el rótulo evita: el marcador publica en la misma columna
89 filas `IDENTICO` (M y R son el mismo número copiado) junto a 20 celdas que sí
predijeron antes de ver el dato. Un comprador que lea «celdas con error medido»
sin el rótulo entiende 109 predicciones donde hay 20.

Ninguna de las dos guardia asserta un TOTAL: los totales se mueven cada vez que
el programa avanza, y un test que los congela convierte el avance en rojo. Se
asserta la PROPIEDAD -- que el veredicto no decide el conteo, que la escala se
deriva, que las clases no se colapsan.
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

import prospectividad as P  # noqa: E402
import tablero_programa as T  # noqa: E402

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def _celda_d_sintetica(cid, veredicto, estado, errores, margen, champion="C2",
                       soportes=None, convencion="sufijo"):
    """(calc, celda-D, resultados.json) para un caso de prueba.

    `convencion` elige cuál de las dos formas vivas de nombrar el error por
    celda se siembra: `sufijo` es la del piloto 3 (`...-<celda>-C2-D-PP`),
    `prefijo` la de los pilotos 1 y 2 (`...-ARB-D-C2-<celda>`).
    """
    calc = f"CALC-SINT-{cid}"
    celda = {
        "celda_d": {
            "id": cid,
            "estado_decidibilidad": estado,
            "veredicto": veredicto,
            "champion_actual": champion,
            "dominio": "SINT",
            "unidad_objetivo": "persona",
            "margen_material": margen,
            "momentos_holdout_refs": [f"{calc}--0000deadbeef"],
        }
    }
    if convencion == "sufijo":
        res = {f"RESULT-SINT-{k}-C2-D-PP": v for k, v in errores.items()}
    else:
        res = {f"RESULT-SINT-ARB-D-C2-{k}": v for k, v in errores.items()}
    for k, v in (soportes or {}).items():
        res[f"RESULT-SINT-{k}-SOPORTE"] = v
    return calc, celda, {"resultados": res}


class MetricaRectoraCuentaLoAdjudicado(unittest.TestCase):
    """P1 · `_celdas_d_adjudicadas` sobre celdas-D sintéticas."""

    def setUp(self):
        if yaml is None:
            self.skipTest("PyYAML ausente")
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self._raiz_real = T.RAIZ
        T.RAIZ = self.tmp.name
        self.addCleanup(lambda: setattr(T, "RAIZ", self._raiz_real))
        self.dir_celdas = os.path.join(
            self.tmp.name, "data", "curacion-registro", "celdas-d")
        os.makedirs(self.dir_celdas)

    def _siembra(self, *casos):
        import json
        for calc, celda, res in casos:
            with open(os.path.join(self.dir_celdas, celda["celda_d"]["id"] + ".yaml"),
                      "w", encoding="utf-8") as fh:
                yaml.safe_dump(celda, fh, allow_unicode=True)
            d = os.path.join(self.tmp.name, "data", "corrida0", calc)
            os.makedirs(d, exist_ok=True)
            with open(os.path.join(d, "resultados.json"), "w", encoding="utf-8") as fh:
                json.dump(res, fh)
        return {c["celda_d"]: c for c in T._celdas_d_adjudicadas()}

    def test_cada_veredicto_cuenta_igual(self):
        """El corazón de P1: VALIDADA no quiere decir ACERTADA.

        Tres celdas-D idénticas salvo el veredicto -- una en que el retador
        vence, una en que NADIE vence, una que cierra en FALSADOR-DÉBIL --
        aportan exactamente las mismas 4 celdas cada una.
        """
        err = {"A": 1.0, "B": 2.0, "C": 3.0, "D": 4.0}
        out = self._siembra(
            _celda_d_sintetica("SINT.vence", "VENCE", "PUNTUADA", err, 2.5),
            _celda_d_sintetica("SINT.nadie", "SIN-CANDIDATO-SUPERIOR", "PUNTUADA",
                               err, 2.5),
            _celda_d_sintetica("SINT.debil", "FALSADOR-DEBIL", "PUNTUADA", err, 2.5,
                               champion="NINGUNO"),
        )
        for cid in ("SINT.vence", "SINT.nadie", "SINT.debil"):
            self.assertTrue(out[cid]["cuenta"], cid)
            self.assertEqual(out[cid]["n_celdas"], 4, cid)
        self.assertEqual(
            {out[c]["n_celdas"] for c in out}, {4},
            "un veredicto NO puede cambiar cuántas celdas se validaron")

    def test_sin_veredicto_sellado_no_cuenta(self):
        """Sin veredicto nadie comparó contra R: cero, y con motivo."""
        out = self._siembra(
            _celda_d_sintetica("SINT.abierta", None, None, {"A": 1.0}, 1.0))
        c = out["SINT.abierta"]
        self.assertFalse(c["cuenta"])
        self.assertEqual(c["n_celdas"], 0)
        self.assertIn("veredicto", c["motivo"])

    def test_escala_se_deriva_del_margen_sellado_y_no_se_teclea(self):
        """Los mismos errores en proporción y en pp dan el MISMO n y el MISMO
        MAE en pp, porque el factor sale del `margen_material` sellado."""
        out = self._siembra(
            _celda_d_sintetica("SINT.pp", "VENCE", "PUNTUADA",
                               {"A": 1.0, "B": 3.0}, 2.0),
            _celda_d_sintetica("SINT.prop", "VENCE", "PUNTUADA",
                               {"A": 0.01, "B": 0.03}, 2.0,
                               convencion="prefijo"),
        )
        self.assertEqual(out["SINT.pp"]["n_celdas"], 2)
        self.assertEqual(out["SINT.prop"]["n_celdas"], 2,
                         "las dos convenciones de nombre se leen igual")
        self.assertEqual(out["SINT.pp"]["escala_cruda"], "PUNTOS-PORCENTUALES")
        self.assertEqual(out["SINT.prop"]["escala_cruda"], "PROPORCION")
        self.assertEqual(out["SINT.pp"]["MAE_pp"], out["SINT.prop"]["MAE_pp"])

    def test_escala_indeterminable_no_sube_la_metrica(self):
        """PARO (d) del encargo: si la escala no se deriva, la celda NO cuenta.

        Un `margen_material` que no casa ni con factor 1 ni con 100 es una
        cadena rota, y una métrica rectora nunca sube por una escala adivinada.
        """
        out = self._siembra(
            _celda_d_sintetica("SINT.rara", "VENCE", "PUNTUADA",
                               {"A": 1.0, "B": 3.0}, 77.7))
        self.assertFalse(out["SINT.rara"]["cuenta"])
        self.assertEqual(out["SINT.rara"]["n_celdas"], 0)
        self.assertIn("escala", out["SINT.rara"]["motivo"])

    def test_fuera_de_soporte_ex_ante_no_cuenta(self):
        """Una celda que el árbitro marcó FUERA-DE-SOPORTE no se comparó."""
        out = self._siembra(_celda_d_sintetica(
            "SINT.soporte", "FALSADOR-DEBIL", "PUNTUADA",
            {"A": 1.0, "B": 3.0, "C": 99.0}, 2.0,
            soportes={"A": "PUNTUADA", "B": "PUNTUADA",
                      "C": "FUERA-DE-SOPORTE-EX-ANTE"}))
        c = out["SINT.soporte"]
        self.assertEqual(c["n_celdas"], 2)
        self.assertEqual(c["fuera_de_soporte"], 1)


class RotuloProspectividad(unittest.TestCase):
    """P2 · las clases no se colapsan y el orden sale de los sellos."""

    def test_identico_no_es_prediccion(self):
        v, cita = P.clasifica({"emisor_vs_arbitro": "EMISOR=ARBITRO",
                               "M": "0.5", "R": "0.5", "estado": "IDENTICO"})
        self.assertEqual(v, P.IDENTICO)
        self.assertIn("mismo número copiado", cita)

    def test_sin_emision_y_emitida_sin_r_no_se_colapsan(self):
        sin, _ = P.clasifica({"estado": "RESERVADA", "M": "", "piso": "",
                              "emision": "", "emisor_vs_arbitro": "N/A-CRUCE"})
        emi, _ = P.clasifica({"estado": "RESERVADA", "M": "", "piso": "",
                              "emision": "EMITIDA-SIN-EVALUAR",
                              "emisor_vs_arbitro": "N/A-CRUCE"})
        self.assertEqual(sin, P.SIN_EMISION)
        self.assertEqual(emi, P.EMITIDA_SIN_R)
        self.assertNotEqual(sin, emi)

    def test_orden_sale_de_los_dos_sellos(self):
        """Con dos CALC reales del repo: emisión antes que árbitro -> PROSPECTIVA,
        y el mismo par al revés -> RETROSPECTIVA. Las fechas NO se teclean."""
        emision = "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
        arbitro = "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001"
        f_e, f_a = P.fecha_de_sello(emision), P.fecha_de_sello(arbitro)
        self.assertIsNotNone(f_e)
        self.assertIsNotNone(f_a)
        self.assertLess(f_e, f_a, "premisa del caso: la emisión se selló antes")
        fila = {"emisor_vs_arbitro": "N/A-CRUCE", "M": "0.4", "R": "",
                "estado": "ADOPTADO-POR-FIRMA", "piso": ""}
        self.assertEqual(P.clasifica(fila, emision, arbitro)[0], P.PROSPECTIVA)
        self.assertEqual(P.clasifica(fila, arbitro, emision)[0], P.RETROSPECTIVA)

    def test_sin_sello_no_degrada_a_retrospectiva(self):
        """Tres hallazgos que no se colapsan (§2): «no hay sello» no es
        «la R ya existía»."""
        fila = {"emisor_vs_arbitro": "N/A-CRUCE", "M": "0.4", "R": "0.5",
                "estado": "X", "piso": ""}
        v, cita = P.clasifica(fila, "CALC-QUE-NO-EXISTE-0001",
                              "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001")
        self.assertEqual(v, P.NO_DERIVABLE)
        self.assertIn("CALC-QUE-NO-EXISTE-0001", cita)

    def test_el_resumen_no_trae_total_que_sume_las_dos_clases(self):
        """Firma de mesa: ninguna vista suma PROSPECTIVA + RETROSPECTIVA."""
        r = P.resumen([{"prospectividad": P.PROSPECTIVA},
                       {"prospectividad": P.RETROSPECTIVA}])
        self.assertEqual(r[P.PROSPECTIVA], 1)
        self.assertEqual(r[P.RETROSPECTIVA], 1)
        self.assertNotIn("total", r)
        self.assertEqual(r["_universo"], 2)
        for v in P.VALORES:
            self.assertIn(v, r, "las clases salen siempre, incluso en cero")


class MarcadorPublicadoTraeElRotulo(unittest.TestCase):
    """El TSV derivado ya publicado trae la columna y no la deja vacía."""

    def test_columna_presente_y_completa(self):
        import csv
        ruta = os.path.join(RAIZ, "data", "corrida0", "marcador-segmento.tsv")
        if not os.path.exists(ruta):
            self.skipTest("marcador aún no derivado en este árbol")
        with open(ruta, encoding="utf-8") as fh:
            fh.readline()  # línea de «DERIVADO — NO EDITAR»
            filas = list(csv.DictReader(fh, delimiter="\t"))
        self.assertTrue(filas)
        for f in filas:
            self.assertIn(f["prospectividad"], P.VALORES, f["celda_id"])
            self.assertTrue(f["prospectividad_cita"].strip(), f["celda_id"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
