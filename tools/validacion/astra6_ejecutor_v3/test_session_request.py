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
    def test_source_to_attested_code_to_execution_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
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
            self.assertEqual([x["path"] for x in request["files"]], ["entrada.csv"])
            response = {"protocol": request["protocol"], "request_id": request["request_id"],
                        "session_id": "fresh-synthetic", "new_session": True,
                        "accepted_files": [{"path": "entrada.csv", "sha256": source["input_files"][0]["sha256"]}],
                        "tools": request["tools"],
                        "response": "from pathlib import Path\nPath('/salida/resultado.json').write_text('{\"n\":3}')\n"}
            receipt = {"request_sha256": hashlib.sha256(json.dumps(request, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
                       "source_archive_sha256": hashlib.sha256((root / "source.tar").read_bytes()).hexdigest(),
                       "source_manifest_sha256": hashlib.sha256((root / "source.json").read_bytes()).hexdigest(),
                       "response": response}
            (root / "receipt.json").write_text(json.dumps(receipt))
            session_request.assemble(root / "source.tar", root / "source.json", root / "receipt.json", root / "assembly")
            runtime.build(root / "assembly/input.tar", root / "assembly/manifest.json", root / "bundle")
            runtime.run(root / "bundle", root / "output", "namespace")
            self.assertEqual(json.loads((root / "output/resultado.json").read_text()), {"n": 3})
            self.assertTrue(runtime.verify_export(root / "output"))

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
                                "tools": received["tools"], "response": "synthetic-only"}
                    encoded = json.dumps(response).encode()
                    self.packet = struct.pack("!I", len(encoded)) + encoded

                def recv(self, length):
                    result, self.packet = self.packet[:length], self.packet[length:]
                    return result

            receipt = session_request.send(request, root / "broker.sock", connection_factory=SyntheticBroker)
            self.assertEqual(receipt["session_id"], "synthetic-fresh-001")


if __name__ == "__main__":
    unittest.main()
