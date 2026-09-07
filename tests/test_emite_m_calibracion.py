#!/usr/bin/env python3
"""Prueba dirigida del resolver de `ola_calibracion` POR CONDUCTA.

ACTO MAESTRA38-M13 · M-POR-CELDA v1.3, §5 del encargo
(`forense/encargos/2026-09-07-MAESTRA38-M13-M-POR-CELDA-v1_3.md`).

Por que existe (§5, verbatim): "Este defecto es material porque puede cambiar
F-DD y decidir si una celda puntua." Antes de este acto,
`tools/emite_m.py::cita_ola_calibracion` resolvia por REGLA: para
`tramite.mordida.discrecional` devolvia siempre el fijo historico
`ENCIG 2023`, que es la calibracion del ASIGNADO `paga_mordida` y NO la de
las conductas MEDIDAS que despues convivieron dentro de la misma regla.

Lo que esta prueba protege:
  (a) los TRES mapeos que §4 manda demostrar sobre esa regla;
  (b) que el camino historico (`paga_mordida`) NO cambio de valor;
  (c) que la cita apunta a una linea REAL de `milpa/tramite.yaml` (§4:
      "La cita debe seguir apuntando al texto real"), no a una tecleada;
  (d) que la ambiguedad (>1 enmienda para la misma conducta) es PARO y no
      una eleccion silenciosa (§3.4 / §25.4);
  (e) que el match es EXACTO -- ni prefijos, ni fuzzy, ni "primera MEDIDO";
  (f) que la regresion P2 de M-TRA-M-01/M-TRA-M-02 sigue PASANDO (§5, §25.5).

Uso:  python3 tests/test_emite_m_calibracion.py
(`tests/check.py` NO auto-descubre `tests/test_*.py` -- su lista de pruebas
es cableada en `main()`; esta prueba se corre por su cuenta, igual que
`tests/test_scoring_adv1_m3.py`, y con el mismo arnes `unittest` porque
`pytest` no esta instalado en este entorno.)
"""
from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools import emite_m  # noqa: E402

REGLA = "tramite.mordida.discrecional"
CON_REGISTRO = "tramite.mordida.con_registro"


def _lineas() -> list[str]:
    return emite_m.RUTA_TRAMITE.read_text(encoding="utf-8").splitlines()


class ResolverPorConducta(unittest.TestCase):
    """§4 -- los tres casos que deben quedar demostrados."""

    def setUp(self):
        self.lineas = _lineas()

    def _resuelve(self, conducta):
        return emite_m.cita_ola_calibracion(REGLA, conducta, self.lineas)

    # --- (a) y (b): los tres mapeos de §4 -------------------------------

    def test_paga_mordida_conserva_el_camino_historico(self):
        """§4: paga_mordida -> ENCIG 2023, "sin cambio respecto del
        comportamiento historico"."""
        valor, _ = self._resuelve("paga_mordida")
        self.assertEqual("ENCIG 2023", valor)

    def test_paga_mordida_encuci2020_usa_su_propia_enmienda(self):
        """§4: paga_mordida_encuci2020 -> ENCUCI 2020."""
        valor, _ = self._resuelve("paga_mordida_encuci2020")
        self.assertTrue(valor.startswith("ENCUCI 2020"), valor)

    def test_paga_mordida_encig2025_usa_su_propia_enmienda(self):
        """§4: paga_mordida_encig2025 -> ENCIG 2025. Es el enlace que este
        acto materializa en TRA-M-02/03/07."""
        valor, _ = self._resuelve("paga_mordida_encig2025")
        self.assertTrue(valor.startswith("ENCIG 2025"), valor)

    def test_las_tres_conductas_no_comparten_calibracion(self):
        """El defecto que motivo el acto: las tres devolvian ENCIG 2023."""
        valores = {c: self._resuelve(c)[0] for c in
                   ("paga_mordida", "paga_mordida_encuci2020", "paga_mordida_encig2025")}
        self.assertEqual(3, len(set(valores.values())), valores)

    # --- (c): la cita apunta a texto REAL del YAML ----------------------

    def test_la_cita_apunta_a_una_linea_real_del_yaml(self):
        """§4: "La cita debe seguir apuntando al texto real de
        milpa/tramite.yaml". Se verifica que el numero de linea citado
        existe y que la linea trae lo que la cita dice traer."""
        casos = {
            "paga_mordida": "fuente:",
            "paga_mordida_encuci2020": "ola_calibracion:",
            "paga_mordida_encig2025": "ola_calibracion:",
        }
        for conducta, ancla in casos.items():
            with self.subTest(conducta=conducta):
                _, cita = self._resuelve(conducta)
                ruta, resto = cita.split(":", 1)
                lineno = int(resto.split(" -- ", 1)[0])
                self.assertEqual("milpa/tramite.yaml", ruta)
                self.assertIn(ancla, self.lineas[lineno - 1])

    def test_la_cita_de_encig2025_no_es_la_del_fallback_ni_la_de_encuci(self):
        """§12: cita_ola_calibracion debe citar la enmienda ENCIG2025, no el
        fallback ENCIG2023 -- y tampoco la PRIMERA `ola_calibracion:` del
        bloque de la regla, que es la de ENCUCI 2020."""
        _, cita_2025 = self._resuelve("paga_mordida_encig2025")
        _, cita_hist = self._resuelve("paga_mordida")
        _, cita_2020 = self._resuelve("paga_mordida_encuci2020")
        self.assertNotEqual(cita_hist, cita_2025)
        self.assertNotEqual(cita_2020, cita_2025)
        self.assertIn("ENCIG 2025", cita_2025)

    def test_el_valor_se_lee_del_yaml_y_no_se_teclea(self):
        """§4: el valor exacto se lee del YAML vigente. Se compara contra
        `yaml.safe_load` del mismo archivo, no contra una copia."""
        import yaml
        doc = yaml.safe_load("\n".join(self.lineas))
        regla = next(r for r in doc["reglas"] if r["id"] == REGLA)
        esperado = regla["enmienda_encig2025"]["ola_calibracion"]
        valor, _ = self._resuelve("paga_mordida_encig2025")
        self.assertEqual(esperado, valor)

    # --- (d) y (e): PARO por ambiguedad y match exacto ------------------

    def test_mas_de_una_enmienda_es_paro_no_eleccion(self):
        """§3.4 / §25.4. Se inyecta una segunda enmienda que calibra la MISMA
        conducta sobre una copia EN MEMORIA de las lineas -- milpa/tramite.yaml
        no se toca (§26)."""
        lineas = list(self.lineas)
        i = next(k for k, l in enumerate(lineas)
                 if l.strip() == "enmienda_encig2025:")
        lineas[i:i] = [
            "    enmienda_duplicada_de_prueba:",
            "      aplica_a: [paga_mordida_encig2025]",
            '      ola_calibracion: "ENCIG 2019 (inyectada por la prueba)"',
        ]
        with self.assertRaises(emite_m.CalibracionAmbigua):
            emite_m.cita_ola_calibracion(REGLA, "paga_mordida_encig2025", lineas)

    def test_match_exacto_sin_prefijos(self):
        """§3: "No fuzzy matching. No prefijos." `paga_mordida` es prefijo de
        `paga_mordida_encig2025` y NO debe heredar su calibracion; y una
        conducta inventada que extiende el nombre tampoco calza."""
        self.assertEqual("ENCIG 2023", self._resuelve("paga_mordida")[0])
        self.assertEqual([], emite_m.enmiendas_que_calibran(
            REGLA, "paga_mordida_encig2025_inventada", self.lineas))

    def test_conducta_sin_enmienda_cae_al_mecanismo_historico(self):
        """§3.3: cero enmiendas -> se conserva el mecanismo historico."""
        self.assertEqual([], emite_m.enmiendas_que_calibran(
            REGLA, "tramite_normal", self.lineas))
        self.assertEqual("ENCIG 2023", self._resuelve("tramite_normal")[0])

    def test_enmienda_sin_ola_calibracion_no_cuenta(self):
        """Una enmienda que NO declara `ola_calibracion` no es candidata
        (§3.1 exige "y que declare ola_calibracion")."""
        self.assertEqual([], emite_m.enmiendas_que_calibran(
            "tramite.evasion_norma", "evade_norma_envipe2025", self.lineas))

    def test_sub_mapa_correcto_en_regla_con_dos_enmiendas(self):
        """`tramite.mordida.con_registro` tiene DOS enmiendas que calibran;
        cada conducta debe recibir la SUYA, no la primera del bloque."""
        v1, _ = emite_m.cita_ola_calibracion(
            CON_REGISTRO, "paga_mordida_encig2025_presencial", self.lineas)
        v2, _ = emite_m.cita_ola_calibracion(
            CON_REGISTRO, "paga_mordida_encig2025_presencial_r2", self.lineas)
        self.assertNotEqual(v1, v2)
        self.assertIn("sin deduplicar", v2)


class GradoDDDeLasTresCeldas(unittest.TestCase):
    """§12/§25.6 -- las tres celdas deben quedar P1 PUNTUA, y la conducta que
    §10 prohibe debe quedar P0 (razon por la que se prohibe)."""

    def setUp(self):
        self.lineas = _lineas()
        self.cal_2025, _ = emite_m.cita_ola_calibracion(
            REGLA, "paga_mordida_encig2025", self.lineas)
        self.cal_2020, _ = emite_m.cita_ola_calibracion(
            REGLA, "paga_mordida_encuci2020", self.lineas)

    def test_las_tres_celdas_puntuan_con_encig2025(self):
        casos = [("TRA-M-02", "ENCUCI", "2020", "transferencia de instrumento"),
                 ("TRA-M-03", "ENCIG", "2013", "transferencia de ola"),
                 ("TRA-M-07", "ENCIG", "2021", "transferencia de ola")]
        for celda, encuesta, ola, tipo in casos:
            with self.subTest(celda=celda):
                grado, razon = emite_m.calcula_grado_DD(
                    encuesta, ola, REGLA, "paga_mordida_encig2025", self.cal_2025)
                self.assertEqual("P1 PUNTUA", grado)
                self.assertIn(tipo, razon)

    def test_encuci2020_daria_P0_en_TRA_M_02(self):
        """§10: por esto NO se usa `paga_mordida_encuci2020` para TRA-M-02."""
        grado, _ = emite_m.calcula_grado_DD(
            "ENCUCI", "2020", REGLA, "paga_mordida_encuci2020", self.cal_2020)
        self.assertEqual("P0 VERIFICACION", grado)

    def test_el_punto_y_coma_dentro_de_parentesis_no_parte_el_segmento(self):
        """La cadena de ENCIG 2025 trae un `;` DENTRO de parentesis: la
        gramatica F-DD parte por `;` solo a profundidad 0."""
        self.assertIn(";", self.cal_2025)
        self.assertEqual(1, len(emite_m._parte_segmentos(self.cal_2025)))
        self.assertEqual("ENCIG 2025",
                         emite_m._cabecera_segmento(self.cal_2025))


class RegresionHistoricaP2(unittest.TestCase):
    """§5/§25.5 -- la regresion vigente de M-TRA-M-01/M-TRA-M-02 sobre el
    camino historico debe seguir PASANDO tras el cambio de resolver."""

    def test_regresion_p2_pasa(self):
        with redirect_stdout(io.StringIO()):
            ok = emite_m.regresion()
        self.assertTrue(ok, "la regresion P2 no pasa -> PARO (§5): cero M-v1_3")


if __name__ == "__main__":
    unittest.main(verbosity=2)
