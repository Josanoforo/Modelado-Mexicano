import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from supervisor import reject_reason


def row(**changes):
    base = {
        "necesidad_id": "N1", "fuente_id_canonico": "ENCIG", "fuente_nombre": "ENCIG", "tipo_fuente": "FUENTE_DATOS",
        "objeto_evidencia_id": "OE-PRUEBA-N1-ENCIG",
        "id_manifiesto": "p1", "sha256": "a" * 64, "capa1_universo_indexado": "SI", "capa2_manifiesto": "SI",
        "capa3_disco_real": "EXISTE", "capa4_apertura_mapeo": "EXISTE-SATISFACE", "clasificacion_relacion": "CONFIRMADA",
        "reason_code": "APERTURA_EXPLICITA_SATISFACE", "evidencia_ref": "MAIN:data/abrir4.tsv:L2", "evidencia_textual_breve": "reactivo",
        "confianza": "ALTA", "conflicto_material": "NO", "nota": "",
    }
    base.update(changes)
    return base


class EstadosConEvidenciaTest(unittest.TestCase):
    def setUp(self):
        self.payloads = {"p1": {"sha256_declarado": "a" * 64}}

    def test_satisface_sin_evidencia(self):
        self.assertEqual(reject_reason(row(evidencia_ref=""), self.payloads), "SIN_EVIDENCIA_REF")

    def test_satisface_sin_apertura(self):
        self.assertEqual(reject_reason(row(capa4_apertura_mapeo="SI"), self.payloads), "SATISFACE_SIN_APERTURA")

    def test_payload_inventado(self):
        self.assertEqual(reject_reason(row(id_manifiesto="inventado"), self.payloads), "PAYLOAD_INEXISTENTE")

    def test_sha_mal_formado(self):
        self.assertEqual(reject_reason(row(sha256="abc"), self.payloads), "SHA256_MAL_FORMADO")


if __name__ == "__main__":
    unittest.main()
