import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ROOT / ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


calc = cargar("calcula_f5_completa", "tools/calcula_f5_completa.py")
runner = cargar("runner_l_completa", "forense/prereg-duelo-v2/runner_l_completa.py")


class TestExtraccion(unittest.TestCase):
    def test_punto_y_abstencion(self):
        self.assertEqual(calc.extraer("texto\nESTIMACION_PUNTUAL=12.5%")[:2], ("VALIDA", .125))
        self.assertEqual(calc.extraer("texto\nABSTENCION")[:2], ("ABSTENCION", None))

    def test_malformada_no_fuerza_numero(self):
        self.assertEqual(calc.extraer("Contexto 94%, pero no sé")[0], "MALFORMADA")
        self.assertEqual(calc.extraer("ESTIMACION_PUNTUAL=101%")[0], "MALFORMADA")


class TestTolerancia(unittest.TestCase):
    def test_borde_exacto_es_empate(self):
        self.assertEqual(calc.adjudicar_ic(-.5, .5), "EMPATE-PRACTICO")

    def test_residuo_numerico_es_empate(self):
        self.assertEqual(calc.adjudicar_ic(-.5 - 5e-10, .5 + 5e-10), "EMPATE-PRACTICO")

    def test_diferencia_material(self):
        self.assertEqual(calc.adjudicar_ic(-.8, -.6, "X", "Y"), "X-GANA")

    def test_simetria(self):
        self.assertEqual(calc.adjudicar_ic(.6, .8, "X", "Y"), "Y-GANA")
        self.assertEqual(calc.adjudicar_ic(-.8, -.6, "Y", "X"), "Y-GANA")


class TestPlan(unittest.TestCase):
    def test_224_posiciones_unicas(self):
        ps = runner.construir_posiciones("cliente-prueba")
        self.assertEqual(len(ps), 224)
        self.assertEqual(len({p["ruta"] for p in ps}), 224)
        self.assertEqual(len({p["identidad"] for p in ps}), 224)


if __name__ == "__main__":
    unittest.main()
