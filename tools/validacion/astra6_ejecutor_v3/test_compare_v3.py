"""P4 synthetic integrity and comparison checks; no real reference is used."""
import copy
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

from tools.validacion.astra6_ejecutor_v3 import compare_v3, runtime


def sha(data):
    return hashlib.sha256(data).hexdigest()


class CompareV3Test(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="astra6-compare-v3-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.identity = {"paquete": "SINTETICO", "version_entrada": "1", "sha256_entrada": "a" * 64}
        self.result = {"version": 3, "identidad": self.identity, "filas": [
            {"llave": "proporcion", "unidad": "proporcion", "estado": "RECONSTRUIDO",
             "punto": "0.75", "estado_ic": "CALCULADO", "ic95_inf": "0.5", "ic95_sup": "0.9"},
            {"llave": "sin_dominio", "unidad": "proporcion", "estado": "DENOMINADOR-CERO",
             "motivo": "Dominio sintético vacío"}]}
        self.input_manifest = {"version": 1, "entrypoint": "reconstructor.py",
            "input_files": [{"path": "reconstructor.py", "sha256": "b" * 64}],
            "output_files": [{"path": "resultado.json", "max_bytes": 1048576}],
            "max_total_output_bytes": 1048576}
        self.input_sha = sha(json.dumps(self.input_manifest, sort_keys=True, separators=(",", ":")).encode())
        self.export = self.root / "export"
        self.anchor = self.root / "anchor.json"
        self.make_export(self.export, self.result)
        runtime.freeze_export(self.export, self.anchor, package_identity=self.identity,
                              expected_input_manifest_sha256=self.input_sha)
        self.tolerance = self.root / "tolerance.json"
        self.tolerance.write_text('{"abs":"0.01","rel":"0"}')
        self.frozen = self.root / "frozen"
        self.frozen_sha = compare_v3.freeze(self.export, self.anchor, self.tolerance, self.frozen)

    def make_export(self, target, result):
        data = (json.dumps(result, sort_keys=True) + "\n").encode()
        payload = io.BytesIO()
        with tarfile.open(fileobj=payload, mode="w") as archive:
            item = tarfile.TarInfo("resultado.json")
            item.size = len(data)
            archive.addfile(item, io.BytesIO(data))
        runtime._extract(payload.getvalue(), self.input_manifest, target)

    def reference(self, value):
        path = self.root / "reference.json"
        path.write_text(json.dumps(value, sort_keys=True) + "\n")
        return path, sha(path.read_bytes())

    def test_positive_and_only_changed_ic_is_discrepancy(self):
        path, expected = self.reference(self.result)
        compared = compare_v3.compare(self.frozen, self.frozen_sha, path, expected)
        self.assertEqual(compared["estado"], "COINCIDE")
        changed = copy.deepcopy(self.result)
        changed["filas"][0]["ic95_sup"] = "0.95"
        path, expected = self.reference(changed)
        compared = compare_v3.compare(self.frozen, self.frozen_sha, path, expected)
        self.assertEqual(compared["estado"], "DISCREPA")
        self.assertEqual(compared["resultados"][0]["causas"], ["ic95_sup"])
        self.assertEqual(compared["resultados"][1]["estado"], "COINCIDE")

    def test_key_unit_and_state_changes_rejected_or_discrepant(self):
        for field, value, error in (("llave", "other", True), ("unidad", "porcentaje", True),
                                    ("estado_ic", "SIN-IC", False),
                                    ("estado", "DENOMINADOR-CERO", False)):
            with self.subTest(field=field):
                changed = copy.deepcopy(self.result)
                changed["filas"][0][field] = value
                if field == "estado_ic":
                    changed["filas"][0].pop("ic95_inf")
                    changed["filas"][0].pop("ic95_sup")
                if field == "estado":
                    changed["filas"][0] = {"llave": "proporcion", "unidad": "proporcion",
                                           "estado": value, "motivo": "Dominio sintético vacío"}
                path, expected = self.reference(changed)
                if error:
                    with self.assertRaises(ValueError):
                        compare_v3.compare(self.frozen, self.frozen_sha, path, expected)
                else:
                    compared = compare_v3.compare(self.frozen, self.frozen_sha, path, expected)
                    self.assertEqual(compared["estado"], "DISCREPA")
                    self.assertIn("estado_ic" if field == "estado_ic" else "estado_fila",
                                  compared["resultados"][0]["causas"])

    def test_coherent_file_and_manifest_mutation_cannot_cross_anchor(self):
        changed = copy.deepcopy(self.result)
        changed["filas"][0]["punto"] = "0.7"
        data = (json.dumps(changed, sort_keys=True) + "\n").encode()
        result = self.export / "resultado.json"
        result.chmod(0o644)
        result.write_bytes(data)
        manifest_path = self.export / "export-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["files"][0].update(sha256=sha(data), bytes=len(data))
        manifest_path.write_text(json.dumps(manifest, sort_keys=True) + "\n")
        self.assertTrue(runtime.verify_export_consistency(self.export))
        with self.assertRaises(ValueError):
            runtime.verify_export(self.export, self.anchor)

    def test_complete_package_swap_and_frozen_code_tamper(self):
        changed = copy.deepcopy(self.result)
        changed["identidad"] = {**self.identity, "paquete": "OTRO-SINTETICO"}
        swapped = self.root / "swapped"
        self.make_export(swapped, changed)
        self.assertTrue(runtime.verify_export_consistency(swapped))
        with self.assertRaises(ValueError):
            runtime.verify_export(swapped, self.anchor)
        path, expected = self.reference(self.result)
        code = self.frozen / "compare_v3.py"
        code.chmod(0o644)
        code.write_bytes(code.read_bytes() + b"\n# tampered\n")
        with self.assertRaises(ValueError):
            compare_v3.compare(self.frozen, self.frozen_sha, path, expected)


if __name__ == "__main__":
    unittest.main()
