from __future__ import annotations

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.curador_registro.baseline import ARCHIVOS_TSV, validar_baseline
from tools.curador_registro.sync_bootstrap import _freeze_manifest, _write_tsv, synchronize


ROOT = Path(__file__).resolve().parents[3]
REGISTRY = ROOT / "data/curacion-registro"
UNIVERSE = ROOT / "data/curacion-universo"


class BootstrapSynchronizationTests(unittest.TestCase):
    def test_complete_derivation_matches_versioned_registry_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_name:
            base = Path(temporary_name)
            registry = base / "registry"; registry.mkdir()
            for filename in [*ARCHIVOS_TSV.values(), "baseline.json", "bootstrap-semantico.tsv", "trabajo-semantico.tsv"]:
                shutil.copy2(REGISTRY / filename, registry / filename)
            manifest = json.loads((registry / "baseline.json").read_text())
            with (registry / "relaciones.tsv").open(encoding="utf-8", newline="") as handle:
                relations = list(csv.DictReader(handle, delimiter="\t"))
            relation_ids = {row["relacion_id"] for row in relations}
            for filename in ("evidencias.tsv", "utilidad-modelo.tsv"):
                with (registry / filename).open(encoding="utf-8", newline="") as handle:
                    reader = csv.DictReader(handle, delimiter="\t")
                    fields = list(reader.fieldnames or [])
                    rows = [row for row in reader if row["relacion_id"] in relation_ids]
                _write_tsv(registry / filename, fields, rows)
            _freeze_manifest(registry, manifest)
            self.assertTrue(validar_baseline(registry)["ok"])
            recovery = (registry / "relaciones.tsv").read_bytes()
            fields = list(relations[0])
            removed = next(row for row in relations if row["clasificacion_relacion"] == "CANDIDATA")
            _write_tsv(
                registry / "relaciones.tsv", fields,
                [row for row in relations if row["relacion_id"] != removed["relacion_id"]],
            )
            journal = base / "journal.json"
            first = synchronize(
                registry,
                REGISTRY / "necesidad-objeto-modelo.tsv",
                UNIVERSE / "declaraciones-activos-t0.tsv",
                UNIVERSE / "universo-declarado-t0.tsv",
                UNIVERSE / "estado-activos.tsv",
                REGISTRY / "reglas-clasificacion-trabajo.json",
                recovery,
                "TEST-RECOVERY",
                journal,
                apply=True,
            )
            self.assertTrue(first["ok"])
            self.assertTrue(validar_baseline(registry)["ok"])
            second = synchronize(
                registry,
                REGISTRY / "necesidad-objeto-modelo.tsv",
                UNIVERSE / "declaraciones-activos-t0.tsv",
                UNIVERSE / "universo-declarado-t0.tsv",
                UNIVERSE / "estado-activos.tsv",
                REGISTRY / "reglas-clasificacion-trabajo.json",
                recovery,
                "TEST-RECOVERY",
                journal,
                apply=False,
            )
            self.assertEqual([], second["changed"])
            self.assertEqual(first["relations"], second["bootstrap_rows"])


if __name__ == "__main__":
    unittest.main()
