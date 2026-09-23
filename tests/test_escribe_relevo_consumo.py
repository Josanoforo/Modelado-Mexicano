"""Guardas de mutación del primer escritor de consumo GEN2."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import escribe_relevo_consumo as writer  # noqa: E402


class WriterTest(unittest.TestCase):
    def setUp(self):
        self.source = (
            '  - {conducta: denuncia_por_otra_razon, p: 0.705687, '
            'clase: "DERIVADO", rol_uso: complemento_dependiente, '
            'uso_motor: "PROPUESTA-NO-ADOPTADA-NC-0085: complemento"}\n'
        )

    def test_exact_single_structural_change_and_idempotence(self):
        changed = writer.transform(self.source, "0.705687")
        self.assertIn("corrida0_resultado_id: " + writer.RESULT, changed)
        self.assertIn("corrida0_generacion: GEN2", changed)
        self.assertIn("p: 0.705687", changed)
        self.assertIn("GEN2-RELEVADO-POR-PIN", changed)
        self.assertEqual(changed, writer.transform(changed, "0.705687"))

    def test_rejects_prior_value_or_partial_citation(self):
        with self.assertRaises(ValueError):
            writer.transform(self.source.replace("0.705687", "0.705688"), "0.705687")
        with self.assertRaises(ValueError):
            writer.transform(self.source.replace("clase:", "corrida0_generacion: GEN2, clase:"), "0.705687")

    def test_rejects_nonunique_consumer(self):
        with self.assertRaises(ValueError):
            writer.transform(self.source + self.source, "0.705687")


if __name__ == "__main__":
    unittest.main()
