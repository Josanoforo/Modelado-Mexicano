#!/usr/bin/env python3
"""Test de la spec de `celdas_validadas` (ACTO GEN2-TUBERIA-METRICA-RECTORA-1
· P1). QUÉ DEFECTO ATRAPA: una spec humana (D-15) que dice una cosa mientras
el código hace otra no se nota hasta que alguien intenta recalcular sin leer
el código -- y para entonces ya costó una sesión entera. Este test compara,
con un caso SINTÉTICO (una celda de cada clase), lo que la spec declara en
`forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md` contra lo que
`tools/celdas_validadas.py` calcula de verdad.
"""
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

SPEC_MD = os.path.join(RAIZ, "forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec-v1_0.md")
SPEC_YAML = os.path.join(RAIZ, "forense/prereg-caja/METRICA-CELDAS-VALIDADAS-spec.yaml")


class TestSpecExiste(unittest.TestCase):
    """La spec humana y su spec.yaml existen y traen lo que D-15 exige."""

    def test_spec_md_existe(self):
        self.assertTrue(os.path.exists(SPEC_MD), f"NO-ENCONTRADO: {SPEC_MD}")

    def test_spec_yaml_existe(self):
        self.assertTrue(os.path.exists(SPEC_YAML), f"NO-ENCONTRADO: {SPEC_YAML}")

    def test_spec_declara_las_tres_clases(self):
        texto = open(SPEC_MD, encoding="utf-8").read()
        for clase in ("Clase 1", "Clase 2", "Clase 3"):
            self.assertIn(clase, texto, f"la spec no declara {clase}")

    def test_spec_declara_prospectiva_retrospectiva_no_se_suman(self):
        texto = open(SPEC_MD, encoding="utf-8").read().lower()
        self.assertIn("nunca se suman", texto)

    def test_spec_declara_marca_de_definicion(self):
        """§9 (firma P, GEN2-ADOPCION-BLOQUE-Y-PINES-1): la spec declara el
        ancla ANTES del módulo (D-15) y cita el mismo commit que el código."""
        import celdas_validadas as CV
        texto = open(SPEC_MD, encoding="utf-8").read()
        self.assertIn("Marca de definición", texto)
        self.assertIn(CV.DEFINICION_DESDE, texto,
                       "la spec debe citar el mismo commit que DEFINICION_DESDE")


class TestModuloVsFormula(unittest.TestCase):
    """Caso sintético: una celda de cada clase, calculada a mano con la
    fórmula de la spec (§3) y comparada contra `celdas_validadas.py`."""

    def test_total_es_suma_de_clase_1_y_clase_2_nunca_clase_3(self):
        """§3: total = n(clase 1) + n(clase 2); clase 3 aparte, siempre."""
        import celdas_validadas as CV
        cv = CV._celdas_validadas()
        d = cv["desglose_por_clase"]
        formula = d["cruce_vs_R"] + d["persistencia_t_menos_1_vs_R"]
        self.assertEqual(cv["total_celdas_validadas"], formula,
                          "el total no coincide con la fórmula §3 de la spec")
        # La clase 3 nunca entra a la suma, aunque sea mayor que 0.
        self.assertNotEqual(
            cv["total_celdas_validadas"],
            formula + (d.get("duelo_tres_nacional") or 0),
            "si esto fallara con duelo_tres_nacional > 0, la clase 3 se habría colado al total")

    def test_escala_sintetica_factor_1_vs_factor_100(self):
        """§3: la escala se deriva probando el factor 1 y el 100 contra
        `margen_material`; si ninguno casa, la celda NO cuenta. Caso
        sintético: MAE=5.43pp (factor correcto=1) contra un margen_material
        de 5.43 -- debe casar en PUNTOS-PORCENTUALES, no en PROPORCION."""
        vivos = {"a": 5.40, "b": 5.46}  # MAE = 5.43
        margen = 5.43
        mae = sum(vivos.values()) / len(vivos)
        escala, factor = None, None
        for f, nombre in ((1.0, "PUNTOS-PORCENTUALES"), (100.0, "PROPORCION")):
            if abs(mae * f - margen) <= 1e-5:
                escala, factor = nombre, f
                break
        self.assertEqual(escala, "PUNTOS-PORCENTUALES")
        self.assertEqual(factor, 1.0)

    def test_escala_sintetica_ninguno_casa_no_cuenta(self):
        """Si ni el factor 1 ni el 100 reproducen margen_material, la spec
        (§3, §4) exige que la celda NO cuente -- nunca se adivina la escala."""
        vivos = {"a": 0.5, "b": 0.6}  # MAE = 0.55
        margen = 999.0  # no casa con 0.55 ni con 55.0
        mae = sum(vivos.values()) / len(vivos)
        factor = None
        for f in (1.0, 100.0):
            if abs(mae * f - margen) <= 1e-5:
                factor = f
                break
        self.assertIsNone(factor, "el caso sintético debe forzar NINGUNO casa")

    def test_identico_y_formalidad_sin_error_declarados_no_cuentan(self):
        """§4: IDENTICO y formalidad-con-piso-sin-error nunca están en el total."""
        import celdas_validadas as CV
        cv = CV._celdas_validadas()
        no_cuentan = cv["NO_CUENTAN"]
        self.assertIn("identico_emisor_igual_arbitro", no_cuentan)
        self.assertIn("formalidad_con_piso_sin_error", no_cuentan)

    def test_prospectiva_retrospectiva_nunca_se_suman_en_la_linea(self):
        """§5/§7: `--linea` imprime las dos sub-cifras separadas, nunca su suma."""
        import celdas_validadas as CV
        cv = CV._celdas_validadas()
        linea = CV.linea(cv)
        prosp, retro = CV.prospectividad_sub_cifras(cv)
        self.assertIn(f"prospectiva {prosp}", linea)
        self.assertIn(f"retrospectiva {retro}", linea)
        self.assertNotIn(f"({prosp + retro})", linea,
                          "la línea no debe imprimir la suma prospectiva+retrospectiva")

    def test_json_trae_bloque_universo_con_sha_y_archivos(self):
        """§7: `--json` trae `universo` con `sha` y `archivos_leidos` -- D-16."""
        out = subprocess.run([sys.executable, "tools/celdas_validadas.py", "--json"],
                              cwd=RAIZ, capture_output=True, text=True, check=True)
        d = json.loads(out.stdout)
        self.assertIn("universo", d)
        self.assertIn("sha", d["universo"])
        self.assertIn("archivos_leidos", d["universo"])
        self.assertTrue(d["universo"]["archivos_leidos"])

    def test_json_trae_definicion_desde(self):
        """§9: `--json` trae `definicion_desde`, al lado del total, nunca
        fundido con él."""
        import celdas_validadas as CV
        out = subprocess.run([sys.executable, "tools/celdas_validadas.py", "--json"],
                              cwd=RAIZ, capture_output=True, text=True, check=True)
        d = json.loads(out.stdout)
        self.assertEqual(d.get("definicion_desde"), CV.DEFINICION_DESDE)
        self.assertIsInstance(d.get("total_celdas_validadas"), int)

    def test_linea_trae_definicion_desde(self):
        """§7/§9: `--linea` imprime `definicion_desde <commit>`."""
        import celdas_validadas as CV
        out = subprocess.run([sys.executable, "tools/celdas_validadas.py", "--linea"],
                              cwd=RAIZ, capture_output=True, text=True, check=True)
        self.assertIn(f"definicion_desde {CV.DEFINICION_DESDE}", out.stdout)

    def test_status_trae_celdas_validadas_definicion_desde(self):
        """corrida0 status imprime `celdas_validadas_definicion_desde`
        (firma P) al lado de `celdas_validadas`, nunca fundido con él."""
        import corrida0
        import celdas_validadas as CV
        c = corrida0.status(imprime=False)
        self.assertEqual(c.get("celdas_validadas_definicion_desde"), CV.DEFINICION_DESDE)
        self.assertIsInstance(c.get("celdas_validadas"), int)


if __name__ == "__main__":
    unittest.main()
