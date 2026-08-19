from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.integrate_production import verify_production_bundle
from tools.curador_registro.produce import taylor_distribution


REPO = Path(__file__).resolve().parents[3]
CONFIG = REPO / "data/curacion-registro/especificaciones-produccion.json"
SNAPSHOT = REPO / "data/curacion-universo/snapshot-t0.json"
BASELINE = REPO / "data/curacion-registro"
ANALYST = REPO / "data/curacion-registro/expedientes-produccion/t0-89f4c3a49c00c0e1"
PRODUCTION = REPO / "data/curacion-registro/produccion-modelo.tsv"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resign(directory: Path, filename: str) -> None:
    """Simulate a malicious analyst updating its own manifest."""
    manifest_path = directory / "hashes.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[filename] = file_hash(directory / filename)
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


class EmptyCellRegressionTests(unittest.TestCase):
    def test_empty_category_does_not_report_zero_uncertainty_as_population_certainty(self) -> None:
        records = [
            {"respuesta": "1", "peso": "1", "estrato": "A", "upm": "1"},
            {"respuesta": "2", "peso": "1", "estrato": "A", "upm": "1"},
            {"respuesta": "1", "peso": "1", "estrato": "A", "upm": "2"},
            {"respuesta": "2", "peso": "1", "estrato": "A", "upm": "2"},
        ]
        categories = [
            {"codigo": "1", "etiqueta": "Sí"},
            {"codigo": "2", "etiqueta": "No"},
            {"codigo": "3", "etiqueta": "No aplica"},
        ]
        estimates, uncertainties, _, _, reserve = taylor_distribution(
            records, "respuesta", categories, "peso", "estrato", "upm"
        )
        empty_estimate = next(row for row in estimates if row["codigo"] == "3")
        empty_uncertainty = next(row for row in uncertainties if row["codigo"] == "3")
        self.assertEqual(0, empty_estimate["n_categoria"])
        self.assertEqual("NO_ESTIMABLE", empty_estimate["proporcion"])
        self.assertEqual("SIN_OBSERVACIONES_ESTIMACION_NO_SUSTENTADA", empty_estimate["estado_celda"])
        self.assertEqual("NO_ESTIMABLE", empty_uncertainty["error_estandar"])
        self.assertEqual("NO_ESTIMABLE", empty_uncertainty["ic95_inferior"])
        self.assertEqual("NO_ESTIMABLE", empty_uncertainty["ic95_superior"])
        self.assertIn("celdas_sin_observaciones=3", reserve)


class FailClosedProductionTests(unittest.TestCase):
    def _copy_analyst(self, temp_root: Path) -> Path:
        destination = temp_root / "analyst"
        shutil.copytree(ANALYST, destination)
        return destination

    def test_1_result_changed_without_resigning_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            analyst = self._copy_analyst(Path(temp_name))
            result = analyst / "ESP-OPACA-A-7baf278d/resultado.tsv"
            result.write_bytes(result.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "reproducción supervisora"):
                verify_production_bundle(CONFIG, SNAPSHOT, BASELINE, analyst)

    def test_2_result_changed_and_resigned_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            analyst = self._copy_analyst(Path(temp_name))
            directory = analyst / "ESP-OPACA-A-7baf278d"
            result = directory / "resultado.tsv"
            result.write_text(
                result.read_text(encoding="utf-8").replace(
                    "CALCULO_REPRODUCIBLE", "CALCULO_REPRODUCIBLE_FALSO", 1
                ),
                encoding="utf-8",
            )
            resign(directory, "resultado.tsv")
            with self.assertRaisesRegex(ValueError, "reproducción supervisora"):
                verify_production_bundle(CONFIG, SNAPSHOT, BASELINE, analyst)

    def test_3_received_spec_changed_and_resigned_still_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            analyst = self._copy_analyst(Path(temp_name))
            directory = analyst / "ESP-OPACA-C-9ecb5c61"
            spec_path = directory / "especificacion-recibida.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            spec["dominio"] = "Dominio inventado"
            spec_path.write_text(
                json.dumps(spec, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            resign(directory, "especificacion-recibida.json")
            with self.assertRaisesRegex(ValueError, "maestra canónica"):
                verify_production_bundle(CONFIG, SNAPSHOT, BASELINE, analyst)

    def test_4_wrong_microdata_hash_in_master_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            temp_root = Path(temp_name)
            bad_config = temp_root / "especificaciones-produccion.json"
            config = json.loads(CONFIG.read_text(encoding="utf-8"))
            config["specifications"][0]["hash_microdato"] = "0" * 64
            bad_config.write_text(
                json.dumps(config, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "hash de microdato"):
                verify_production_bundle(
                    bad_config, SNAPSHOT, BASELINE, ANALYST, repo_root=REPO
                )

    def test_5_integrated_table_changed_after_integration_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            altered = Path(temp_name) / "produccion-modelo.tsv"
            shutil.copy2(PRODUCTION, altered)
            altered.write_bytes(altered.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "difiere de la reproducción"):
                verify_production_bundle(
                    CONFIG, SNAPSHOT, BASELINE, ANALYST,
                    production_table_path=altered,
                )

    def test_valid_bundle_is_independently_reproduced_without_analyst_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            analyst = self._copy_analyst(Path(temp_name))
            for manifest in analyst.glob("*/hashes.json"):
                manifest.unlink()
            rows = verify_production_bundle(CONFIG, SNAPSHOT, BASELINE, analyst)
            self.assertEqual(12, len(rows))
            self.assertEqual(12, sum(row["estado"] == "CALCULO_REPRODUCIBLE" for row in rows))

    def test_production_semantics_and_periods_are_preserved(self) -> None:
        with PRODUCTION.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        descriptive = {
            row["relacion_id"] for row in rows
            if row["estado_calculo_descriptivo"] == "CALCULO_DESCRIPTIVO_DISPONIBLE"
        }
        model_ready = {
            row["relacion_id"] for row in rows
            if row["estado_uso_modelo"] == "LISTA_PARA_USO_MODELO"
        }
        self.assertEqual(3, len(descriptive))
        self.assertEqual(3, len(model_ready))
        self.assertTrue(all(
            row["periodo_referencia"] == "últimos 12 meses"
            for row in rows if ":PF1_" in row["estimando"]
        ))
        pb22 = next(row for row in rows if row["estimando"].endswith(":PB2_2"))
        category3 = next(item for item in json.loads(pb22["estimacion"]) if item["codigo"] == "3")
        self.assertEqual("NO_ESTIMABLE", category3["proporcion"])
        b_row = next(row for row in rows if row["especificacion_id"].startswith("ESP-OPACA-B"))
        self.assertEqual("CALCULO_REPRODUCIBLE", b_row["estado"])


if __name__ == "__main__":
    unittest.main()
