import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from test_estados_con_evidencia import row
from curador import explicit_need_id
from supervisor import make_diff, reject_reason


class NegativosConservadosTest(unittest.TestCase):
    def test_necesidad_secundaria_no_se_propaga(self):
        self.assertEqual(explicit_need_id("12 familismo_apoyo (no-ENIF)"), "N12")
        self.assertEqual(explicit_need_id("13 familismo_obligacion"), "N13")
        self.assertNotEqual(explicit_need_id("12 familismo_apoyo (no-ENIF)"), "N17")

    def test_negativa_desaparecida_se_reporta(self):
        old = [{"necesidad_id": "N4", "fuente_id_canonico": "ENSAFI", "evidencia_ref": "MAIN:x:L1", "clasificacion_relacion": "NEGATIVA"}]
        diff = make_diff(old, [])
        self.assertEqual(diff[0]["tipo_cambio"], "RELACION_MODIFICADA")
        self.assertEqual(diff[0]["clasificacion_actual"], "AUSENTE")
        self.assertEqual(diff[0]["impacto_decision"], "SI")

    def test_estado_no_se_copia_a_todas_las_fuentes(self):
        copied = row(reason_code="ESTADO_NECESIDAD_PROPAGADO")
        payloads = {"p1": {"sha256_declarado": "a" * 64}}
        self.assertEqual(
            reject_reason(copied, payloads),
            "ESTADO_DE_NECESIDAD_COPIADO_A_FUENTES",
        )


if __name__ == "__main__":
    unittest.main()
