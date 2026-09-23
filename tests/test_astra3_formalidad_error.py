"""Fixture sintético; no lee resultados de las olas reservadas."""

import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/astra/enif/formalidad_error/formalidad_error.py"
spec = importlib.util.spec_from_file_location("formalidad_error", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class FormalidadErrorTest(unittest.TestCase):
    def setUp(self):
        self.rows = []
        self.source = {}
        self.target = {}
        for i, (outcome, category) in enumerate(
            (o, c) for o in sorted(mod.OUTCOMES) for c in sorted(mod.CATEGORIES)
        ):
            source_id, target_id = f"S{i}-P", f"T{i}-P"
            self.rows.append({"input_id": f"{outcome}::formalidad::{category}",
                              "outcome": outcome, "category": category,
                              "source_universe": "PERSONA ELEGIDA 18-70",
                              "target_universe": "PERSONA ELEGIDA 18-70",
                              "source_id": source_id, "target_id": target_id})
            for result, result_id, p in ((self.source, source_id, .5),
                                         (self.target, target_id, [.5, .8, .2, .5, .5, .5][i])):
                result[result_id] = p
                result[result_id[:-2] + "-IC-LO"] = p - .02
                result[result_id[:-2] + "-IC-HI"] = p + .02

    def test_six_pairs_zero_positive_negative_missing_ci(self):
        missing = self.rows[4]["target_id"][:-2] + "-IC-HI"
        del self.target[missing]
        values = mod.measure(self.rows, self.source, self.target)
        ordered = [values[row["input_id"]] for row in self.rows]
        self.assertEqual(ordered[0]["d_pp"], 0)
        self.assertEqual(ordered[0]["clase"], "PERSISTE")
        self.assertAlmostEqual(ordered[1]["d_pp"], 30)
        self.assertEqual(ordered[1]["clase"], "CAMBIA")
        self.assertAlmostEqual(ordered[2]["d_pp"], -30)
        self.assertEqual(ordered[2]["clase"], "CAMBIA")
        self.assertIsNone(ordered[4]["d_pp"])
        self.assertEqual(ordered[4]["clase"], "NO-COMPARABLE")

    def test_identity_rejects_universe_and_duplicate(self):
        fieldnames = list(self.rows[0])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "identity.tsv"
            def write():
                with path.open("w", encoding="utf-8", newline="") as stream:
                    writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
                    writer.writeheader()
                    writer.writerows(self.rows)
                return mod.sha256(path)
            self.rows[0]["target_universe"] = "PERSONA ELEGIDA 18+"
            with self.assertRaisesRegex(ValueError, "universos despareados"):
                mod.read_identity(path, write())
            self.rows[0]["target_universe"] = "PERSONA ELEGIDA 18-70"
            self.rows[1]["category"] = self.rows[0]["category"]
            with self.assertRaisesRegex(ValueError, "llave duplicada"):
                mod.read_identity(path, write())


if __name__ == "__main__":
    unittest.main()
