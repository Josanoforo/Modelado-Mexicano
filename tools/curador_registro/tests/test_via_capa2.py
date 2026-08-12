import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

import yaml

from tools.curador_registro.via_capa2 import derivar, aplicar_diffs


class ViaCapa2Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "data" / "raw").mkdir(parents=True)
        (self.root / "data" / "curacion-registro").mkdir(parents=True)
        (self.root / "data" / "inventarios").mkdir(parents=True)

        # payload real para la fila que sí debe verificar SI
        payload = self.root / "data" / "raw" / "fuente_ok.xlsx"
        payload.write_bytes(b"contenido de prueba")
        sha_ok = hashlib.sha256(payload.read_bytes()).hexdigest()

        self.campos = [
            "relacion_id", "necesidad_id", "fuente_canonica_normalizada",
            "objeto_evidencia_id_canonico", "fuente_nombre", "tipo_fuente",
            "id_manifiesto", "sha256_fuente", "capa1_universo_indexado",
            "capa2_manifiesto", "capa3_disco_real", "capa4_apertura_mapeo",
            "clasificacion_relacion", "reason_code", "evidencia_ref",
            "evidencia_textual_breve", "confianza", "conflicto_material", "nota",
        ]
        filas = [
            {  # id_manifiesto real, payload íntegro -> debe derivar SI
                "relacion_id": "REL-A", "necesidad_id": "N1",
                "fuente_canonica_normalizada": "FUENTE_OK",
                "id_manifiesto": "fuente_ok_xlsx", "capa2_manifiesto": "SI_O_REFERENCIADO",
            },
            {  # id_manifiesto apunta a una entrada cuyo payload no coincide -> NO promueve
                "relacion_id": "REL-B", "necesidad_id": "N2",
                "fuente_canonica_normalizada": "FUENTE_ROTA",
                "id_manifiesto": "fuente_rota_xlsx", "capa2_manifiesto": "SI_O_REFERENCIADO",
            },
            {  # sin id_manifiesto, pero el nombre aparece en el manifiesto -> diagnostico, no escribe
                "relacion_id": "REL-C", "necesidad_id": "N3",
                "fuente_canonica_normalizada": "FUENTE_CANDIDATA",
                "id_manifiesto": "NO_DETERMINADO", "capa2_manifiesto": "NO_REFERENCIADO",
            },
            {  # sin id_manifiesto y sin ninguna presencia -> ni diff ni diagnostico
                "relacion_id": "REL-D", "necesidad_id": "N4",
                "fuente_canonica_normalizada": "FUENTE_AUSENTE",
                "id_manifiesto": "NO_DETERMINADO", "capa2_manifiesto": "NO_REFERENCIADO",
            },
        ]
        for f in filas:
            for c in self.campos:
                f.setdefault(c, "")
        self.relaciones_path = self.root / "data" / "curacion-registro" / "relaciones.tsv"
        with self.relaciones_path.open("w", encoding="utf-8", newline="") as h:
            w = csv.DictWriter(h, fieldnames=self.campos, delimiter="\t", lineterminator="\n")
            w.writeheader(); w.writerows(filas)

        manifiesto = [
            {
                "id": "fuente_ok_xlsx", "usado_para": "Fuente OK de prueba",
                "archivo": "fuente_ok.xlsx", "sha256": sha_ok,
                "tamano_bytes": payload.stat().st_size,
            },
            {
                "id": "fuente_rota_xlsx", "usado_para": "Fuente rota de prueba",
                "archivo": "no_existe.xlsx", "sha256": "0" * 64, "tamano_bytes": 999,
            },
            {
                "id": "otra_entrada_candidata", "usado_para": "Documento de FUENTE_CANDIDATA, sin id propio",
                "archivo": "otra.pdf", "sha256": "1" * 64, "tamano_bytes": 1,
            },
        ]
        (self.root / "data" / "manifiesto.yaml").write_text(
            yaml.dump(manifiesto, allow_unicode=True, sort_keys=False), encoding="utf-8")
        (self.root / "data" / "inventarios" / "alias-fuentes.yaml").write_text(
            yaml.dump([{"canonico": "FUENTE_CANDIDATA", "alias": ["fuente candidata"]}],
                      allow_unicode=True), encoding="utf-8")

    def test_deriva_si_solo_con_payload_verificado(self):
        resultado = derivar(self.root)
        diffs_por_id = {d["relacion_id"]: d for d in resultado["diffs_propuestos"]}
        self.assertIn("REL-A", diffs_por_id)
        self.assertEqual(diffs_por_id["REL-A"]["derivado"], "SI")
        self.assertNotIn("REL-B", diffs_por_id, "payload no-coincide no debe promoverse a SI")

    def test_diagnostico_no_promueve(self):
        resultado = derivar(self.root)
        diag_ids = {d["relacion_id"] for d in resultado["diagnostico_candidatas_sin_id"]}
        self.assertIn("REL-C", diag_ids)
        self.assertNotIn("REL-D", diag_ids)
        diff_ids = {d["relacion_id"] for d in resultado["diffs_propuestos"]}
        self.assertNotIn("REL-C", diff_ids, "diagnostico nunca debe generar un diff")

    def test_escribe_solo_toca_filas_con_diff_y_preserva_orden(self):
        resultado = derivar(self.root)
        aplicar_diffs(self.relaciones_path, resultado["diffs_propuestos"])
        with self.relaciones_path.open(encoding="utf-8-sig", newline="") as h:
            filas = list(csv.DictReader(h, delimiter="\t"))
        self.assertEqual([f["relacion_id"] for f in filas], ["REL-A", "REL-B", "REL-C", "REL-D"])
        por_id = {f["relacion_id"]: f for f in filas}
        self.assertEqual(por_id["REL-A"]["capa2_manifiesto"], "SI")
        self.assertEqual(por_id["REL-B"]["capa2_manifiesto"], "SI_O_REFERENCIADO")
        self.assertEqual(por_id["REL-C"]["capa2_manifiesto"], "NO_REFERENCIADO")
        self.assertEqual(por_id["REL-D"]["capa2_manifiesto"], "NO_REFERENCIADO")

    def test_no_escribe_sin_diffs(self):
        antes = self.relaciones_path.read_bytes()
        aplicar_diffs(self.relaciones_path, [])
        self.assertEqual(self.relaciones_path.read_bytes(), antes)


if __name__ == "__main__":
    unittest.main()
