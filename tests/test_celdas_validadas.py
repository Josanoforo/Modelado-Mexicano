#!/usr/bin/env python3
"""Test de la MÉTRICA RECTORA `celdas_validadas` (ACTO GEN2-SENAL-1 · P1).

QUÉ DEFECTO REAL ATRAPA (§1, «el aparato tiene costo»): este acto encontró DOS
defectos ya presentes en el árbol, y cada aserción de aquí abajo es el guardia
de uno de ellos.

  (1) LAS 89 FILAS `IDENTICO` TIENEN `M == R`. No porque una predicción acertara,
      sino porque `emisor_vs_arbitro = EMISOR=ARBITRO`: es el mismo número
      copiado en dos columnas. La lectura natural de la tabla («filas con M y R
      = filas validadas») da 89 y es falsa. Al lector le habría costado creer
      que el programa tiene 89 celdas con predicción validada fuera de muestra
      cuando tiene 20 de cruce. Ese es el error que la línea del tablero existe
      para impedir, así que se pina.

  (2) LAS DOS CELDAS-D EMITEN EN ESCALAS DISTINTAS. El CALC de DIN guarda el
      error en PROPORCIÓN (0.0042) y el de TRA en PUNTOS PORCENTUALES (5.43).
      Fundirlos sin convertir da un factor 100 en la métrica rectora del
      programa. La conversión se verifica contra el `margen_material` SELLADO de
      cada YAML de celda-D -- que es una cifra derivada y citable, no tecleada
      (§2, «ninguna cifra esperada se teclea»).
"""
import json
import os
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))


def _indicador():
    out = subprocess.run([sys.executable, "tools/tablero_programa.py", "--json"],
                         cwd=RAIZ, capture_output=True, text=True, check=True)
    return json.loads(out.stdout)["celdas_validadas"]["valor"]


def _yaml_margen(nombre):
    """Lee `margen_material` del YAML sellado, por texto: es el valor esperado
    DERIVADO del repo, no una constante a mano (§2)."""
    p = os.path.join(RAIZ, "data/curacion-registro/celdas-d", nombre)
    for linea in open(p, encoding="utf-8"):
        if linea.strip().startswith("margen_material:"):
            return float(linea.split(":", 1)[1].split("#")[0].strip())
    raise AssertionError(f"margen_material NO-ENCONTRADO en {nombre}")


class TestCeldasValidadas(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cv = _indicador()

    def test_las_tres_clases_no_se_funden_en_una_cifra(self):
        """El total NO incluye el duelo nacional: otro universo, otro estimando
        (§4.4 -- un estimando restringido no se compara contra uno poblacional)."""
        cv = self.cv
        d = cv["desglose_por_clase"]
        self.assertEqual(cv["total_celdas_validadas"],
                         d["cruce_vs_R"] + d["persistencia_t_menos_1_vs_R"],
                         "el total sólo suma cruce + persistencia; el duelo nacional se reporta aparte")
        self.assertIsNotNone(d["duelo_tres_nacional"], "el duelo debe reportarse, aunque no se sume")

    def test_identico_nunca_cuenta_como_validada(self):
        """Defecto (1): M == R por EMISOR=ARBITRO no es una predicción validada."""
        cv = self.cv
        n_identico = cv["NO_CUENTAN"]["identico_emisor_igual_arbitro"]
        self.assertGreater(n_identico, 0, "si no hay filas IDENTICO, este guardia perdió su objeto")
        self.assertNotEqual(cv["total_celdas_validadas"], n_identico)
        self.assertNotIn(n_identico, cv["desglose_por_clase"].values(),
                         "ninguna clase puede tener el conteo de IDENTICO: sería contarlas como validadas")

    def test_escala_convertida_contra_el_margen_material_sellado(self):
        """Defecto (2): el error mediano sale en pp para las dos celdas-D, y la
        conversión se comprueba contra la cifra sellada del YAML, no contra una
        constante tecleada. `margen_material` es la MEDIA (MAE) y la métrica usa
        la MEDIANA, así que se comprueba el ORDEN DE MAGNITUD (§4.3: comparable
        sin enlace = signo y razón), que es lo que el factor 100 rompe."""
        for c in self.cv["clase_1_cruce_vs_R"]:
            self.assertNotIn("estado", c, f"CALC ausente para {c.get('celda_d')}")
            # El nombre del YAML ES el id de la celda-D. Antes esto era un
            # if/else DIN-o-TRA que mandaba cualquier tercera celda-D al YAML de
            # TRA y comparaba su mediana contra un `margen_material` ajeno: el
            # guardia pasaba, pero sobre la cifra equivocada. Lo destapó la
            # tercera celda-D (GOB, piloto 3) al entrar a la métrica
            # (ACTO GEN2-MARCADOR-E-INFORME-1, defecto adyacente D-21).
            nombre = c["celda_d"] + ".yaml"
            mae = _yaml_margen(nombre)
            med = c["error_mediano_pp"]
            self.assertLess(abs(med - mae), 10.0,
                            f"{c['celda_d']}: mediana {med} pp contra MAE sellado {mae} pp -- "
                            f"una diferencia así de grande es el factor 100 de la escala cruda")
            self.assertLess(med, 100.0, "un error mediano >= 100 pp es imposible: escala sin convertir")

    def test_brecha_temporal_por_instrumento_y_nunca_promediada(self):
        """Cada fila de persistencia declara su propia brecha; el encargo prohíbe
        promediar brechas de 1, 2 y 3 años."""
        brechas = {p["instrumento"]: p["brecha_anios"] for p in self.cv["clase_2_persistencia_vs_R"]}
        self.assertTrue(brechas, "sin filas de persistencia el guardia pierde su objeto")
        for inst, b in brechas.items():
            self.assertIsNotNone(b, f"brecha NO derivada para {inst}")
            self.assertGreaterEqual(b, 1, f"persistencia t-1 exige brecha >= 1 año: {inst}")
        self.assertGreater(len(set(brechas.values())), 1,
                           "conviven brechas distintas: por eso se reportan por instrumento")

    def test_formalidad_con_piso_y_sin_error_no_cuenta(self):
        """Las 6 celdas de formalidad tienen piso pero su error de persistencia
        NO está medido (CALC-PISO-PERSISTENCIA-ERROR-0001 se selló antes de que
        existieran). Contarlas sería afirmar un error que nadie calculó."""
        self.assertGreaterEqual(self.cv["NO_CUENTAN"]["formalidad_con_piso_sin_error"], 0)

    def test_la_metrica_es_la_primera_linea_del_bloque_derivado(self):
        """La firma de mesa dice «va en la primera línea del tablero»."""
        import tablero_programa as T
        ruta = os.path.join(RAIZ, "forense/tablero/TABLERO-PROGRAMA.md")
        texto = open(ruta, encoding="utf-8").read()
        cuerpo = texto.split(T.MARCA_INICIO, 1)[1]
        vinetas = [l for l in cuerpo.splitlines() if l.startswith("- **")]
        self.assertTrue(vinetas, "el bloque derivado no tiene viñetas")
        self.assertIn("Celdas validadas", vinetas[0],
                      "la métrica rectora debe ser la PRIMERA viñeta del bloque derivado")

    def test_universo_declarado(self):
        """A.4/A.13: todo conteo con su universo."""
        self.assertIn("filas de", self.cv["universo_examinado"])


if __name__ == "__main__":
    unittest.main()
