#!/usr/bin/env python3
"""Guardias del COMMIT-1 del piloto 3 · `ACTO GEN2-CELDA-D-PILOTO-3-P0` (20/sep/2026).

Pinan el contrato congelado de `CALC-GOB-DIGITAL-EXE-EMISIONES-0001` para que el
`COMMIT-2` no pueda desviarse de él en silencio. **Cero microdato**: ninguna prueba
de este archivo abre ENCIG 2025, y todos los números son o bien constantes
congeladas del pre-registro, o bien fixtures sintéticos elegidos para ejercer un
caso límite. Ninguno describe a México.

Qué guardan, y por qué cada una:

  G1  Las DOS condiciones suspensivas son mecánicas, no sólo prosa: el medidor
      REHÚSA correr si S1 no cerró habilitante, y rehúsa si S2 encontró edad real
      censurada. Un `CAMBIO-DE-INSTRUMENTO` retira la spec en vez de adaptarla.
  G2  `lambda` está congelada con el valor DERIVADO (no tecleado) y coincide con
      el que la spec humana y el `spec.yaml` declaran. Los tres tienen que decir
      lo mismo o el pre-registro no vale.
  G3  La rejilla es IDÉNTICA a la congelada en las dos olas históricas. Si alguien
      la mueve, el piloto deja de ser comparable con sus propios insumos.
  G4  `18-29 x HASTA-PRIMARIA` está declarada FUERA-DE-SOPORTE **ex ante**, y el
      conteo de celdas puntuables es 15 de 16.
  G5  El C2 preserva el rango [0,1] por construcción (forma log-aditiva), que es
      justamente lo que la forma multiplicativa no hacía (FP-379 D2).
  G6  El COMMIT-1 se congeló SIN resultados: el directorio del CALC no trae
      `resultados.json` ni `sello.json`.
"""
from __future__ import annotations

import math
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CALC = os.path.join(ROOT, "data", "corrida0", "CALC-GOB-DIGITAL-EXE-EMISIONES-0001")
MEDIDOR = os.path.join(CALC, "medidor.py")
SPEC_YAML = os.path.join(CALC, "spec.yaml")
SPEC_MD = os.path.join(ROOT, "forense", "prereg-caja",
                       "GOB-gobierno-digital-exe15-spec-v1_0.md")

LAMBDA_CONGELADA = 0.8937949410086089
EDADES = ["18-29", "30-44", "45-59", "60-96"]
ESCOLARIDADES = ["HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"]

# El medidor importa numpy/pandas, ausentes en la nube. Las guardias que no
# necesitan ejecutarlo leen la FUENTE: el contrato se pina igual, y el archivo
# sigue siendo verificable en un entorno sin materiales.
with open(MEDIDOR, encoding="utf-8") as fh:
    FUENTE = fh.read()
with open(SPEC_YAML, encoding="utf-8") as fh:
    YAML_TXT = fh.read()
with open(SPEC_MD, encoding="utf-8") as fh:
    MD_TXT = fh.read()

try:  # pragma: no cover - depende del entorno
    import numpy  # noqa: F401
    import pandas  # noqa: F401
    MATERIALES = True
except ImportError:  # pragma: no cover
    MATERIALES = False


def _carga_medidor():
    import importlib.util
    spec = importlib.util.spec_from_file_location("piloto3_medidor", MEDIDOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class G1CondicionesSuspensivas(unittest.TestCase):
    """Las dos condiciones son mecánicas: el medidor para solo."""

    def test_las_dos_condiciones_estan_escritas_en_los_tres_artefactos(self):
        for nombre, txt in (("medidor.py", FUENTE), ("spec.yaml", YAML_TXT),
                            ("spec humana", MD_TXT)):
            self.assertIn("NC-0355", txt, f"{nombre}: S1 no cita NC-0355")
            self.assertIn("CAMBIO-DE-INSTRUMENTO", txt, f"{nombre}: S1 incompleta")
            self.assertRegex(txt, r"97.{0,6}98.{0,6}99", f"{nombre}: S2 no nombra los códigos")

    def test_el_medidor_define_la_guardia_y_la_llama_antes_de_medir(self):
        self.assertIn("def _guardia_suspensiva", FUENTE)
        pos_guardia = FUENTE.index("_guardia_suspensiva(contrato[")
        pos_notimpl = FUENTE.index("raise NotImplementedError")
        self.assertLess(pos_guardia, pos_notimpl,
                        "la guardia tiene que correr ANTES de cualquier medición")

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_cambio_de_instrumento_retira_la_spec_en_vez_de_adaptarla(self):
        mod = _carga_medidor()
        ok = {o: {"edad_real_censurada": False} for o in ("2021", "2023", "2025")}
        with self.assertRaises(mod.ParoDeGuardia) as cm:
            mod._guardia_suspensiva("CAMBIO-DE-INSTRUMENTO", ok)
        self.assertIn("RETIRA SIN CORRER", str(cm.exception).upper().replace("Í", "I"))

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_s1_sin_cerrar_no_habilita(self):
        mod = _carga_medidor()
        ok = {o: {"edad_real_censurada": False} for o in ("2021", "2023", "2025")}
        for veredicto in ("", "PENDIENTE", "NO-VERIFICABLE-AQUI", "CASI"):
            with self.assertRaises(mod.ParoDeGuardia):
                mod._guardia_suspensiva(veredicto, ok)
        for veredicto in ("MISMO-INSTRUMENTO", "CAMBIO-MENOR"):
            mod._guardia_suspensiva(veredicto, ok)   # no levanta

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_edad_real_censurada_para_antes_de_emitir(self):
        mod = _carga_medidor()
        con_censura = {o: {"edad_real_censurada": False} for o in ("2021", "2023", "2025")}
        con_censura["2023"]["edad_real_censurada"] = True
        with self.assertRaises(mod.ParoDeGuardia) as cm:
            mod._guardia_suspensiva("MISMO-INSTRUMENTO", con_censura)
        self.assertIn("MESA", str(cm.exception).upper())

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_s2_incompleta_para(self):
        mod = _carga_medidor()
        with self.assertRaises(mod.ParoDeGuardia):
            mod._guardia_suspensiva("MISMO-INSTRUMENTO",
                                    {"2021": {"edad_real_censurada": False}})


class G2LambdaCongelada(unittest.TestCase):
    """El mismo `lambda` en los tres artefactos, y es el derivado."""

    def test_los_tres_artefactos_declaran_el_mismo_lambda(self):
        self.assertIn(f"LAMBDA = {LAMBDA_CONGELADA}", FUENTE)
        self.assertIn(f"lambda_congelada: {LAMBDA_CONGELADA}", YAML_TXT)
        self.assertIn(str(LAMBDA_CONGELADA), MD_TXT)

    def test_lambda_es_consistente_con_sus_propios_momentos(self):
        tau2 = float(re.search(r"lambda_tau2:\s*([0-9.]+)", YAML_TXT).group(1))
        s2 = float(re.search(r"lambda_sigma_bar2:\s*([0-9.]+)", YAML_TXT).group(1))
        var_entre = float(re.search(r"lambda_var_entre:\s*([0-9.]+)", YAML_TXT).group(1))
        self.assertAlmostEqual(tau2, max(0.0, var_entre - s2), places=9,
                               msg="tau2 no es max(0, Var_entre - sigma_bar2)")
        self.assertAlmostEqual(LAMBDA_CONGELADA, tau2 / (tau2 + s2), places=9,
                               msg="lambda no es tau2/(tau2+sigma_bar2)")

    def test_lambda_esta_en_rango(self):
        self.assertGreater(LAMBDA_CONGELADA, 0.0)
        self.assertLess(LAMBDA_CONGELADA, 1.0)


class G3RejillaIdentica(unittest.TestCase):
    """La rejilla del piloto es la de las dos olas históricas, sin mover un borde."""

    REJILLA_SELLADA = '"18-29", "30-44", "45-59", "60-96"'

    def test_la_rejilla_coincide_con_la_de_los_calc_historicos(self):
        for ola, calc in (("2021", "CALC-ENCIG2021-CRUCES-HISTORICOS-0003"),
                          ("2023", "CALC-ENCIG2023-CRUCES-HISTORICOS-0002")):
            ruta = os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")
            with open(ruta, encoding="utf-8") as fh:
                txt = fh.read()
            self.assertIn(self.REJILLA_SELLADA, txt,
                          f"{ola}: la rejilla sellada cambió de forma")
        self.assertIn(self.REJILLA_SELLADA, YAML_TXT,
                      "el piloto no usa la rejilla sellada")

    def test_la_banda_superior_cierra_en_96(self):
        self.assertIn('("60-96", 60, 96)', FUENTE,
                      "si la banda superior deja de cerrar en 96, 97/98/99 dejan de "
                      "caer fuera del universo y F1-bis pierde su objeto")

    def test_escolaridad_agregada_igual_que_en_las_olas_selladas(self):
        for cat in ESCOLARIDADES:
            self.assertIn(cat, FUENTE)
        self.assertIn('{"0", "1", "2"}', FUENTE)
        self.assertIn('{"8", "9"}', FUENTE)


class G4SoporteExAnte(unittest.TestCase):
    """15 de 16, con la celda excluida nombrada antes de ver 2025."""

    def test_la_celda_sin_soporte_esta_declarada_ex_ante(self):
        self.assertIn('("18-29", "HASTA-PRIMARIA")', FUENTE)
        self.assertIn("18-29 x HASTA-PRIMARIA", YAML_TXT)

    def test_el_conteo_es_15_de_16(self):
        self.assertEqual(len(EDADES) * len(ESCOLARIDADES), 16)
        self.assertIn("celdas_puntuadas: 15", YAML_TXT)
        self.assertIn("celdas_total: 16", YAML_TXT)

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_la_celda_ex_ante_no_se_reclasifica_aunque_2025_la_soporte(self):
        mod = _carga_medidor()
        holgado = {ola: {(a, b): 5000 for a in EDADES for b in ESCOLARIDADES}
                   for ola in ("2021", "2023", "2025")}
        estado = mod.clasifica_soporte(holgado)
        self.assertEqual(estado[("18-29", "HASTA-PRIMARIA")], "FUERA-DE-SOPORTE-EX-ANTE",
                         "una declaración ex ante no se revierte con el dato nuevo")
        self.assertEqual(estado["_GLOBAL"], "CON-SOPORTE")

    @unittest.skipUnless(MATERIALES, "numpy/pandas ausentes en este entorno")
    def test_fuera_de_soporte_global_cuando_fallan_cinco(self):
        mod = _carga_medidor()
        n = {ola: {(a, b): 5000 for a in EDADES for b in ESCOLARIDADES}
             for ola in ("2021", "2023", "2025")}
        for a, b in list((a, b) for a in EDADES for b in ESCOLARIDADES)[1:6]:
            n["2025"][(a, b)] = 10
        self.assertEqual(mod.clasifica_soporte(n)["_GLOBAL"], "FUERA-DE-SOPORTE-GLOBAL")


class G5C2PreservaRango(unittest.TestCase):
    """La forma log-aditiva no puede salirse de [0,1]; la multiplicativa sí."""

    @staticmethod
    def _c2_logaditivo(p_a, p_b, p_all):
        lg = lambda p: math.log(p / (1 - p))
        return 1.0 / (1.0 + math.exp(-(lg(p_a) + lg(p_b) - lg(p_all))))

    def test_el_caso_que_rompe_la_forma_multiplicativa(self):
        # .8*.8/.5 = 1.28, fuera de rango. La log-aditiva se queda dentro.
        self.assertGreater(0.8 * 0.8 / 0.5, 1.0)
        v = self._c2_logaditivo(0.8, 0.8, 0.5)
        self.assertTrue(0.0 < v < 1.0, f"C2 fuera de rango: {v}")

    def test_rango_en_una_malla_de_casos_limite(self):
        vals = [0.001, 0.01, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99, 0.999]
        for p_a in vals:
            for p_b in vals:
                for p_all in vals:
                    v = self._c2_logaditivo(p_a, p_b, p_all)
                    self.assertTrue(0.0 < v < 1.0,
                                    f"fuera de rango en {(p_a, p_b, p_all)}: {v}")

    def test_el_medidor_usa_la_forma_logaditiva_y_lo_dice(self):
        self.assertIn("_expit(_logit(m[(\"_edad\", a)]) + _logit(m[(\"_esc\", b)])", FUENTE)
        self.assertIn("NO es independencia", FUENTE)


class G6CongeladoSinResultados(unittest.TestCase):
    """COMMIT-1: spec y código, cero resultados."""

    def test_no_hay_resultados_ni_sello(self):
        for prohibido in ("resultados.json", "sello.json", "sello.sha256", "ejecucion.json"):
            self.assertFalse(os.path.exists(os.path.join(CALC, prohibido)),
                             f"COMMIT-1 no sella nada, y apareció {prohibido}")

    def test_el_spec_yaml_lo_declara(self):
        self.assertIn("medidor_ejecutado_al_congelar: NO", YAML_TXT)
        self.assertIn("resultados_esperados: []", YAML_TXT)

    def test_el_cuerpo_de_medicion_no_esta_implementado(self):
        self.assertIn("raise NotImplementedError", FUENTE)

    def test_el_sidecar_de_la_spec_humana_coincide(self):
        import hashlib
        sidecar = SPEC_MD.replace(".md", ".sha256")
        self.assertTrue(os.path.exists(sidecar), "falta el sidecar de la spec humana")
        with open(sidecar, encoding="utf-8") as fh:
            declarado = fh.read().split()[0]
        real = hashlib.sha256(MD_TXT.encode("utf-8")).hexdigest()
        self.assertEqual(declarado, real, "el sidecar no corresponde a la spec humana")

    def test_el_spec_yaml_apunta_al_sha_de_la_spec_humana(self):
        import hashlib
        real = hashlib.sha256(MD_TXT.encode("utf-8")).hexdigest()
        self.assertIn(f"spec_md_sha256: {real}", YAML_TXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
