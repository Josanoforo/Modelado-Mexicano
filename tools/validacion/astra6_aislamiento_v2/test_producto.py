"""Pruebas materiales del adaptador y frontera usando únicamente sintéticos."""
import copy
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

import adaptador
import aislamiento

FIXTURES = Path(__file__).parent / "fixtures"


def document():
    return {"version": 2, "identidad": {"paquete": "SINTETICO-1", "version_entrada": "1",
            "sha256_entrada": "0" * 64}, "filas": [{"llave": "media", "unidad": "proporcion",
            "estado": "RECONSTRUIDO", "punto": "0.75", "ic95_inf": "0.50", "ic95_sup": "1.00"}]}


class AdapterTests(unittest.TestCase):
    def test_duplicate_json_fields_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "duplicate.json"
            path.write_text('{"version":2,"version":2}')
            with self.assertRaises(ValueError):
                adaptador.read_json(path)

    def test_nine_alias_forms(self):
        base = document()
        expected = adaptador.normalize(base)
        for case in json.loads((FIXTURES / "aliases.json").read_text()):
            with self.subTest(case=case["caso"]):
                doc = document()
                row = doc["filas"][0]
                for old, alias in (("punto", case["punto"]), ("ic95_inf", case["inferior"]),
                                   ("ic95_sup", case["superior"])):
                    row[alias] = row.pop(old)
                actual = adaptador.normalize(doc)
                # El mapa conserva el alias original; solo las filas deben ser equivalentes.
                self.assertEqual(actual["filas"], expected["filas"])

    def test_relevant_errors(self):
        for name in ("collision", "duplicate", "missing", "extra", "bool", "nan", "infinite",
                     "string_invalid", "partial_ci", "sin_ic_with_limits"):
            with self.subTest(case=name):
                doc = document()
                row = doc["filas"][0]
                if name == "collision": row["valor"] = row["punto"]
                elif name == "duplicate": doc["filas"].append(copy.deepcopy(row))
                elif name == "missing": row.pop("llave")
                elif name == "extra": row["no_contratado"] = 1
                elif name == "bool": row["punto"] = True
                elif name == "nan": row["punto"] = float("nan")
                elif name == "infinite": row["punto"] = float("inf")
                elif name == "string_invalid": row["punto"] = "75%"
                elif name == "partial_ci": row.pop("ic95_sup")
                elif name == "sin_ic_with_limits": row["estado_ic"] = "SIN-IC"
                with self.assertRaises((ValueError, TypeError)):
                    adaptador.normalize(doc)

    def test_absent_null_and_no_ci_are_distinct(self):
        base = document()
        absent = copy.deepcopy(base)
        absent["filas"][0].pop("ic95_inf")
        absent["filas"][0].pop("ic95_sup")
        null = copy.deepcopy(base)
        null["filas"][0].update(ic95_inf=None, ic95_sup=None)
        no_ci = copy.deepcopy(absent)
        no_ci["filas"][0]["estado_ic"] = "SIN-IC"
        values = [adaptador.normalize(x)["filas"][0] for x in (absent, null, no_ci)]
        self.assertNotEqual(values[0], values[1])
        self.assertNotEqual(values[0], values[2])


class IsolationTests(unittest.TestCase):
    def test_dangerous_archive_members(self):
        for index, kind in enumerate(("traversal", "symlink", "duplicate")):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as source, tempfile.TemporaryDirectory() as dest:
                archive = Path(source) / "danger.tar"
                with tarfile.open(archive, "w") as tar:
                    entry = tarfile.TarInfo("../escape" if kind == "traversal" else "safe")
                    if kind == "symlink":
                        entry.type = tarfile.SYMTYPE
                        entry.linkname = "../outside"
                        tar.addfile(entry)
                    else:
                        entry.size = 1
                        tar.addfile(entry, io.BytesIO(b"a"))
                        if kind == "duplicate": tar.addfile(entry, io.BytesIO(b"a"))
                with self.assertRaises(ValueError):
                    aislamiento.materialize_archive(archive, Path(dest) / "entry", [])

    def test_materialization_rejects_traversal_symlink_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source"
            source.mkdir()
            source.joinpath("safe").write_text("sintetico")
            source.joinpath("link").symlink_to(source / "safe")
            digest = hashlib.sha256(b"sintetico").hexdigest()
            for index, item in enumerate(({"path": "../outside", "sha256": digest},
                                           {"path": "link", "sha256": digest},
                                           {"path": "safe", "sha256": "0" * 64})):
                with self.subTest(item=item), self.assertRaises((ValueError, RuntimeError, OSError)):
                    aislamiento.materialize(source, Path(tmp) / f"dest{index}", [item])

    def test_real_probe_and_fail_closed(self):
        probe = aislamiento.probe_environment()
        self.assertIn(probe["status"], ("APTO-TECNICAMENTE", "NO-LANZAR-COMO-CIEGA"))
        if probe["status"] != "APTO-TECNICAMENTE":
            with tempfile.TemporaryDirectory() as tmp, self.assertRaises(RuntimeError):
                aislamiento.run_isolated(Path(tmp), ["/bin/true"])
        else:
            self.assertTrue(probe["canaries"])


if __name__ == "__main__":
    unittest.main()
