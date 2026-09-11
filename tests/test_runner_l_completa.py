import importlib.util
import json
import unittest
from pathlib import Path


RUTA = Path(__file__).resolve().parents[1] / "forense/prereg-duelo-v2/runner_l_completa.py"
SPEC = importlib.util.spec_from_file_location("runner_l_completa", RUTA)
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(runner)


class IdentidadModeloYCuota(unittest.TestCase):
    def test_deriva_opus_del_sobre_actual(self):
        sobre = {
            "modelUsage": {
                "claude-haiku-4-5-20251001": {"canonicalModel": "claude-haiku-4-5"},
                "claude-opus-5": {"canonicalModel": "claude-opus-5"},
            }
        }
        self.assertEqual(runner.modelo_competidor(sobre), "claude-opus-5")
        self.assertEqual(runner.modelos_reales(sobre), ["claude-haiku-4-5", "claude-opus-5"])

    def test_no_infiere_identidad_si_falta_opus(self):
        self.assertIsNone(runner.modelo_competidor({"modelUsage": {}}))

    def test_reconoce_limite_semanal_nuevo(self):
        mensaje = json.dumps({"result": "You've hit your weekly limit · resets Sep 12, 11am"})
        self.assertTrue(runner.error_sistemico(mensaje))

    def test_error_ordinario_no_es_sistemico(self):
        self.assertFalse(runner.error_sistemico("temporary upstream failure"))


if __name__ == "__main__":
    unittest.main()
