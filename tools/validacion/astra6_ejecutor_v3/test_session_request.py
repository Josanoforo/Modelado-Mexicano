"""Synthetic broker protocol proof; no provider account or network is used."""
import hashlib
import io
import json
from pathlib import Path
import struct
import tarfile
import tempfile
import unittest

from tools.validacion.astra6_ejecutor_v3 import runtime, session_request


class SessionRequestTest(unittest.TestCase):
    def source_fixture(self, root):
        data = b"1,2,3\n"
        with tarfile.open(root / "source.tar", "w") as archive:
            item = tarfile.TarInfo("entrada.csv")
            item.size = len(data)
            archive.addfile(item, io.BytesIO(data))
        source = {"version": 1, "input_files": [{"path": "entrada.csv", "sha256": hashlib.sha256(data).hexdigest()}],
                  "output_files": [{"path": "resultado.json", "max_bytes": 1024}],
                  "max_total_output_bytes": 1024}
        (root / "source.json").write_text(json.dumps(source))
        (root / "prompt.txt").write_text("Use only entrada.csv.")
        request = session_request.prepare_source(root / "source.tar", root / "source.json", root / "prompt.txt")
        response = {"protocol": request["protocol"], "request_id": request["request_id"],
                    "session_id": "fresh-synthetic", "new_session": True,
                    "accepted_files": [{"path": "entrada.csv", "sha256": source["input_files"][0]["sha256"]}],
                    "tools": request["tools"], "provider": "synthetic-provider", "model": "synthetic-model",
                    "attestation": {"issuer": "synthetic-broker", "scope": session_request.ATTESTATION_SCOPE},
                    "response": "from pathlib import Path\nPath('/salida/resultado.json').write_text('{\"n\":3}')\n"}
        receipt = session_request.make_receipt(request, response, root / "source.tar", root / "source.json")
        receipt_path = root / "receipt.json"
        receipt_path.write_text(json.dumps(receipt))
        return request, response, receipt_path, hashlib.sha256(receipt_path.read_bytes()).hexdigest()

    def test_source_to_attested_code_to_execution_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request, response, receipt_path, receipt_sha = self.source_fixture(root)
            self.assertEqual([x["path"] for x in request["files"]], ["entrada.csv"])
            session_request.assemble(root / "source.tar", root / "source.json", receipt_path, root / "assembly",
                                     prompt_file=root / "prompt.txt", expected_receipt_sha256=receipt_sha)
            runtime.build(root / "assembly/input.tar", root / "assembly/manifest.json", root / "bundle")
            runtime.run(root / "bundle", root / "output", "namespace")
            self.assertEqual(json.loads((root / "output/resultado.json").read_text()), {"n": 3})
            self.assertTrue(runtime.verify_export_consistency(root / "output"))

    def test_external_receipt_sha_prompt_replay_and_code_tamper(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            request, response, receipt_path, receipt_sha = self.source_fixture(root)
            kwargs = {"prompt_file": root / "prompt.txt", "expected_receipt_sha256": receipt_sha}
            with self.assertRaises(ValueError):
                session_request.assemble(root / "source.tar", root / "source.json", receipt_path,
                                         root / "bad-sha", prompt_file=root / "prompt.txt",
                                         expected_receipt_sha256="0" * 64)
            (root / "prompt.txt").write_text("A different prompt")
            with self.assertRaises(ValueError):
                session_request.assemble(root / "source.tar", root / "source.json", receipt_path,
                                         root / "replayed", **kwargs)
            (root / "prompt.txt").write_text("Use only entrada.csv.")
            receipt = json.loads(receipt_path.read_text())
            receipt["request_sha256"] = "0" * 64
            receipt_path.write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):
                session_request.assemble(root / "source.tar", root / "source.json", receipt_path,
                                         root / "invalid-request-sha", prompt_file=root / "prompt.txt",
                                         expected_receipt_sha256=hashlib.sha256(receipt_path.read_bytes()).hexdigest())
            receipt["request_sha256"] = session_request._sha(session_request._canonical(request))
            receipt["response"]["response"] += "\n# tampered after receipt\n"
            receipt_path.write_text(json.dumps(receipt))
            with self.assertRaises(ValueError):
                session_request.assemble(root / "source.tar", root / "source.json", receipt_path,
                                         root / "code-tampered", **kwargs)

    def test_fresh_session_only_receives_allowlisted_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            code = b"from pathlib import Path\nPath('/salida/resultado.json').write_text('{}')\n"
            with tarfile.open(root / "input.tar", "w") as archive:
                info = tarfile.TarInfo("reconstructor.py")
                info.size = len(code)
                archive.addfile(info, io.BytesIO(code))
            manifest = {"version": 1, "entrypoint": "reconstructor.py",
                        "input_files": [{"path": "reconstructor.py", "sha256": hashlib.sha256(code).hexdigest()}],
                        "output_files": [{"path": "resultado.json", "max_bytes": 1024}],
                        "max_total_output_bytes": 1024}
            (root / "manifest.json").write_text(json.dumps(manifest))
            runtime.build(root / "input.tar", root / "manifest.json", root / "bundle")
            (root / "prompt.txt").write_text("Recalculate only the supplied synthetic input.")
            request = session_request.prepare(root / "bundle", root / "prompt.txt")
            self.assertEqual(set(request), {"protocol", "request_id", "session", "prompt", "files", "tools", "max_response_bytes"})
            self.assertEqual(request["session"], "new")
            self.assertEqual(request["files"][0]["path"], "reconstructor.py")
            self.assertNotIn("history", json.dumps(request))

            class SyntheticBroker:
                def __enter__(self):
                    return self

                def __exit__(self, *_):
                    return None

                def settimeout(self, _):
                    return None

                def connect(self, _):
                    return None

                def sendall(self, packet):
                    length = struct.unpack("!I", packet[:4])[0]
                    received = json.loads(packet[4:])
                    assert length == len(packet) - 4 and received == request
                    response = {"protocol": received["protocol"], "request_id": received["request_id"],
                                "session_id": "synthetic-fresh-001", "new_session": True,
                                "accepted_files": [{"path": x["path"], "sha256": x["sha256"]} for x in received["files"]],
                                "tools": received["tools"], "provider": "synthetic-provider", "model": "synthetic-model",
                                "attestation": {"issuer": "synthetic-broker", "scope": session_request.ATTESTATION_SCOPE},
                                "response": "synthetic-only"}
                    encoded = json.dumps(response).encode()
                    self.packet = struct.pack("!I", len(encoded)) + encoded

                def recv(self, length):
                    result, self.packet = self.packet[:length], self.packet[length:]
                    return result

            receipt = session_request.send(request, root / "broker.sock", connection_factory=SyntheticBroker)
            self.assertEqual(receipt["session_id"], "synthetic-fresh-001")


if __name__ == "__main__":
    unittest.main()
