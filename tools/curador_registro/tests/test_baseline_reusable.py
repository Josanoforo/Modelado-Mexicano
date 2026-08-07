import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.baseline import ARCHIVOS_TSV, relacion_id, validar_baseline
from tools.curador_registro.derive_queue import derivar


class BaselineReusableTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        rid = relacion_id("N1", "FUENTE", "OBJETO")
        self.relacion = {
            "relacion_id": rid,
            "necesidad_id": "N1",
            "fuente_canonica_normalizada": "FUENTE",
            "objeto_evidencia_id_canonico": "OBJETO",
            "clasificacion_relacion": "CANDIDATA",
        }
        tablas = {
            "relaciones": [self.relacion],
            "evidencias": [{"procedencia_id": "PROV-1", "relacion_id": rid}],
            "artefactos_rechazados": [],
            "decisiones_humanas": [],
            "utilidad_modelo": [{"relacion_id": rid, "requiere_decision": "NO", "decision_id": "NO_APLICA"}],
            "aliases_fuentes": [],
            "fusiones_relaciones": [],
        }
        archivos = {}
        for nombre, archivo in ARCHIVOS_TSV.items():
            filas = tablas[nombre]
            campos = list(filas[0]) if filas else ["vacio"]
            with (self.root / archivo).open("w", encoding="utf-8", newline="") as h:
                w = csv.DictWriter(h, fieldnames=campos, delimiter="\t", lineterminator="\n")
                w.writeheader(); w.writerows(filas)
            data = (self.root / archivo).read_bytes()
            archivos[archivo] = {"sha256": hashlib.sha256(data).hexdigest(), "filas": len(filas)}
        self.manifest = {
            "archivos": archivos,
            "conteos": {
                "relaciones_activas": 1, "procedencias_aceptadas": 1,
                "artefactos_rechazados": 0, "decisiones_pendientes": 0,
                "familias_alias": 0, "fusiones_declaradas": 0,
                "confirmadas": 0, "negativas": 0, "candidatas": 1, "no_accesibles": 0,
            },
        }
        self._guardar_manifest()

    def tearDown(self):
        self.tmp.cleanup()

    def _guardar_manifest(self):
        (self.root / "baseline.json").write_text(json.dumps(self.manifest), encoding="utf-8")

    def test_valida_contrato_y_deriva_cola(self):
        self.assertTrue(validar_baseline(self.root)["ok"])
        self.assertEqual([self.relacion["relacion_id"]], [f["relacion_id"] for f in derivar(self.root)])

    def test_detecta_procedencia_huerfana(self):
        path = self.root / "evidencias.tsv"
        text = path.read_text(encoding="utf-8").replace(self.relacion["relacion_id"], "REL-AJENA")
        path.write_text(text, encoding="utf-8")
        self.manifest["archivos"]["evidencias.tsv"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        self._guardar_manifest()
        resultado = validar_baseline(self.root)
        self.assertFalse(resultado["ok"])
        self.assertTrue(any("huérfana" in e for e in resultado["errores"]))

    def test_relacion_id_es_semantico_y_estable(self):
        self.assertEqual(relacion_id("N1", "F", "O"), relacion_id("N1", "F", "O"))
        self.assertNotEqual(relacion_id("N1", "F", "O"), relacion_id("N2", "F", "O"))


if __name__ == "__main__":
    unittest.main()
