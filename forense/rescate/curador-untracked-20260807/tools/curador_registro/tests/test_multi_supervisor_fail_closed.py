import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from multi_supervisor import EXPECTED_HEAD, validate_contract


def candidate(source="SRC", obj="OE-1"):
    return {"necesidad_id": "N1", "fuente_id_canonico": source, "objeto_evidencia_id": obj, "clasificacion_relacion": "CANDIDATA"}


def proposal(source="SRC", obj="OE-1", state="CANDIDATA", ref="MAIN:evidence.tsv:L1", locator="L1"):
    return {
        "worker_id": "worker-1", "necesidad_id": "N1", "fuente_canonica": source,
        "objeto_evidencia_id": obj, "estado_anterior": "CANDIDATA", "estado_propuesto": state,
        "tipo_resultado": "CANDIDATA_CON_FRONTERA", "evidencia_ref": ref,
        "evidencia_localizador": locator, "evidencia_explicita": "texto", "razon": "razón",
        "reserva_incertidumbre": "reserva", "requiere_decision_humana": "NO", "siguiente_accion": "acción",
    }


class MultiSupervisorFailClosedTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "evidence.tsv").write_text("variable\ttexto\n", encoding="utf-8")
        self.assignments = [{"worker_id": "worker-1", "fuente_id_canonico": "SRC"}]

    def tearDown(self):
        self.tmp.cleanup()

    def test_worker_esperado_ausente_falla(self):
        errors, _ = validate_contract([candidate()], self.assignments, {}, self.repo, EXPECTED_HEAD)
        self.assertTrue(any("worker esperado ausente" in e for e in errors))

    def test_candidata_sin_asignar_falla(self):
        errors, _ = validate_contract([candidate()], [], {}, self.repo, EXPECTED_HEAD)
        self.assertTrue(any("fuente candidata" in e for e in errors))

    def test_adjudicacion_con_referencia_inexistente_falla(self):
        row = proposal(state="CONFIRMADA", ref="MAIN:no-existe.tsv:L1")
        errors, _ = validate_contract([candidate()], self.assignments, {"worker-1": [row]}, self.repo, EXPECTED_HEAD)
        self.assertTrue(any("no verificable" in e for e in errors))

    def test_estado_adjudicado_es_protegido(self):
        base = candidate(); base["clasificacion_relacion"] = "NEGATIVA"
        errors, _ = validate_contract([base], self.assignments, {"worker-1": [proposal()]}, self.repo, EXPECTED_HEAD)
        self.assertTrue(any("estado protegido" in e for e in errors))

    def test_union_conserva_exactamente_claves(self):
        errors, metrics = validate_contract([candidate()], self.assignments, {"worker-1": [proposal()]}, self.repo, EXPECTED_HEAD)
        self.assertEqual(errors, [])
        self.assertEqual((metrics["claves_faltantes"], metrics["claves_duplicadas"], metrics["claves_nuevas"]), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
