"""Minimal broker wire protocol for a fresh blind reconstruction session.

The broker is an independently provisioned Unix-socket service. It owns any
provider credentials. This client sends only the prompt and explicitly hashed
input bytes and accepts a bounded attested response. No provider is embedded.
"""
import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import socket
import struct
import tarfile
import uuid

try:
    from . import runtime
except ImportError:  # direct CLI invocation
    import runtime

MAX_PROMPT = 1024 * 1024
MAX_REQUEST = 96 * 1024 * 1024
MAX_RESPONSE = 4 * 1024 * 1024
RESPONSE_FIELDS = {"protocol", "request_id", "session_id", "new_session",
                   "accepted_files", "tools", "provider", "model", "attestation", "response"}
ATTESTATION_SCOPE = "broker-asserted-new-session-without-history-or-memory"


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("utf-8")


def _digest(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def _check_response(request, response):
    if not isinstance(response, dict) or set(response) != RESPONSE_FIELDS:
        raise ValueError("invalid broker response schema")
    if response["protocol"] != request["protocol"] or response["request_id"] != request["request_id"]:
        raise ValueError("broker response request mismatch")
    if response["new_session"] is not True or not isinstance(response["session_id"], str) or not response["session_id"]:
        raise ValueError("broker did not attest a new session")
    for field in ("provider", "model"):
        if not isinstance(response[field], str) or not response[field].strip():
            raise ValueError("broker provider/model identity required")
    attestation = response["attestation"]
    if (not isinstance(attestation, dict) or set(attestation) != {"issuer", "scope"}
            or not isinstance(attestation["issuer"], str) or not attestation["issuer"].strip()
            or attestation["scope"] != ATTESTATION_SCOPE):
        raise ValueError("broker attestation issuer and scope required")
    allowed = [{"path": x["path"], "sha256": x["sha256"]} for x in request["files"]]
    if response["accepted_files"] != allowed or response["tools"] != request["tools"]:
        raise ValueError("broker accepted a different input/tool set")
    code = response["response"]
    if not isinstance(code, str) or not code or len(code.encode("utf-8")) > MAX_PROMPT:
        raise ValueError("broker did not return bounded Python code")


def make_receipt(request, response, archive_file, manifest_file):
    """Preserve the exact request needed to verify the broker reply later."""
    _check_response(request, response)
    return {"request": request, "request_sha256": _sha(_canonical(request)),
            "source_archive_sha256": _sha(Path(archive_file).read_bytes()),
            "source_manifest_sha256": _sha(Path(manifest_file).read_bytes()),
            "response": response}


def prepare(bundle, prompt_file):
    manifest = runtime.verify_bundle(bundle)
    prompt = Path(prompt_file).read_bytes()
    if not prompt or len(prompt) > MAX_PROMPT:
        raise ValueError("prompt byte limit")
    prompt_text = prompt.decode("utf-8")
    files = []
    for item in manifest["input_files"]:
        data = (Path(bundle) / "input" / item["path"]).read_bytes()
        if _sha(data) != item["sha256"]:
            raise ValueError("input changed before session request")
        files.append({"path": item["path"], "sha256": item["sha256"],
                      "base64": base64.b64encode(data).decode("ascii")})
    request = {"protocol": "astra6-blind-session-v1", "request_id": str(uuid.uuid4()),
               "session": "new", "prompt": prompt_text, "files": files,
               "tools": [{"name": "isolated_executor_v3", "input_manifest_sha256":
                          _sha((Path(bundle) / "manifest.json").read_bytes())}],
               "max_response_bytes": MAX_RESPONSE}
    encoded = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    if len(encoded) > MAX_REQUEST:
        raise ValueError("request byte limit")
    return request


def read_source(archive_file, manifest_file):
    """Read a pre-handoff package that contains no reconstructor code."""
    manifest = json.loads(Path(manifest_file).read_text())
    if not isinstance(manifest, dict) or set(manifest) != {"version", "input_files", "output_files", "max_total_output_bytes"} or manifest["version"] != 1:
        raise ValueError("source manifest schema")
    if not isinstance(manifest["input_files"], list) or not manifest["input_files"]:
        raise ValueError("source input allowlist required")
    if any(not isinstance(x, dict) or set(x) != {"path", "sha256"} or
           not isinstance(x["sha256"], str) or not runtime.SHA.fullmatch(x["sha256"])
           for x in manifest["input_files"]):
        raise ValueError("invalid source input record")
    expected = {str(runtime.safe_path(x["path"])): x["sha256"] for x in manifest["input_files"]}
    if len(expected) != len(manifest["input_files"]) or "reconstructor.py" in expected:
        raise ValueError("duplicate source file or pre-handoff reconstructor")
    # Reuse the runtime manifest checks for output limits with a synthetic
    # entrypoint identity. It is not put into the source package.
    runtime.validate_manifest({**manifest, "entrypoint": "reconstructor.py",
                               "input_files": manifest["input_files"] + [{"path": "reconstructor.py", "sha256": "0" * 64}]})
    contents = {}
    total = 0
    with tarfile.open(archive_file, "r:*") as archive:
        seen = set()
        for member in archive:
            name = str(runtime.safe_path(member.name.rstrip("/") if member.isdir() else member.name))
            if name in seen or not (member.isdir() or member.isfile()):
                raise ValueError("unsafe source TAR member")
            seen.add(name)
            if member.isdir():
                continue
            if name not in expected or member.size < 0:
                raise ValueError("unlisted source TAR file")
            total += member.size
            if total > runtime.MAX_INPUT:
                raise ValueError("source byte limit")
            data = archive.extractfile(member).read(member.size + 1)
            if len(data) != member.size or _sha(data) != expected[name]:
                raise ValueError("source input SHA or length mismatch")
            contents[name] = data
    if set(contents) != set(expected):
        raise ValueError("incomplete source TAR")
    return manifest, contents


def prepare_source(archive_file, manifest_file, prompt_file):
    manifest, contents = read_source(archive_file, manifest_file)
    prompt = Path(prompt_file).read_bytes()
    if not prompt or len(prompt) > MAX_PROMPT:
        raise ValueError("prompt byte limit")
    request = {"protocol": "astra6-blind-session-v1", "request_id": str(uuid.uuid4()),
               "session": "new", "prompt": prompt.decode("utf-8"),
               "files": [{"path": path, "sha256": _sha(data), "base64": base64.b64encode(data).decode("ascii")}
                         for path, data in sorted(contents.items())],
               "tools": [{"name": "isolated_executor_v3", "input_manifest_sha256": _sha(Path(manifest_file).read_bytes())}],
               "max_response_bytes": MAX_RESPONSE}
    if len(json.dumps(request).encode()) > MAX_REQUEST:
        raise ValueError("request byte limit")
    return request


def assemble(archive_file, manifest_file, receipt_file, output, *, prompt_file,
             expected_receipt_sha256):
    if not _digest(expected_receipt_sha256):
        raise ValueError("expected receipt SHA-256 required from outside receipt")
    receipt_bytes = Path(receipt_file).read_bytes()
    if _sha(receipt_bytes) != expected_receipt_sha256:
        raise ValueError("receipt differs from external SHA-256")
    manifest, contents = read_source(archive_file, manifest_file)
    receipt = json.loads(receipt_bytes)
    if not isinstance(receipt, dict) or set(receipt) != {"request", "request_sha256", "source_archive_sha256", "source_manifest_sha256", "response"}:
        raise ValueError("invalid session receipt")
    if not _digest(receipt["request_sha256"]) or not _digest(receipt["source_archive_sha256"]) or not _digest(receipt["source_manifest_sha256"]):
        raise ValueError("invalid receipt SHA-256")
    if receipt["source_archive_sha256"] != _sha(Path(archive_file).read_bytes()) or receipt["source_manifest_sha256"] != _sha(Path(manifest_file).read_bytes()):
        raise ValueError("source changed since broker request")
    request = receipt["request"]
    if (not isinstance(request, dict) or set(request) != {"protocol", "request_id", "session", "prompt", "files", "tools", "max_response_bytes"}
            or request["protocol"] != "astra6-blind-session-v1"
            or not isinstance(request["request_id"], str)
            or request["request_id"] != str(uuid.UUID(request["request_id"]))
            or request["session"] != "new" or request["max_response_bytes"] != MAX_RESPONSE):
        raise ValueError("invalid preserved request")
    prompt_bytes = Path(prompt_file).read_bytes()
    if not prompt_bytes or len(prompt_bytes) > MAX_PROMPT or request["prompt"] != prompt_bytes.decode("utf-8"):
        raise ValueError("request prompt mismatch")
    expected_files = [{"path": path, "sha256": _sha(data),
                       "base64": base64.b64encode(data).decode("ascii")}
                      for path, data in sorted(contents.items())]
    expected_tools = [{"name": "isolated_executor_v3", "input_manifest_sha256": receipt["source_manifest_sha256"]}]
    if request["files"] != expected_files or request["tools"] != expected_tools:
        raise ValueError("request differs from source files or tools")
    if receipt["request_sha256"] != _sha(_canonical(request)):
        raise ValueError("request SHA-256 mismatch")
    response = receipt["response"]
    _check_response(request, response)
    code = response["response"]
    contents["reconstructor.py"] = code.encode("utf-8")
    target = Path(output)
    if target.exists() or target.is_symlink():
        raise ValueError("assembly destination must be new")
    target.mkdir(mode=0o700)
    with tarfile.open(target / "input.tar", "w", format=tarfile.USTAR_FORMAT) as archive:
        for name, data in sorted(contents.items()):
            item = tarfile.TarInfo(name)
            item.size = len(data)
            item.mode = 0o444
            archive.addfile(item, io.BytesIO(data))
    execution_manifest = {**manifest, "entrypoint": "reconstructor.py",
                          "input_files": [{"path": name, "sha256": _sha(data)} for name, data in sorted(contents.items())]}
    (target / "manifest.json").write_text(json.dumps(execution_manifest, sort_keys=True, separators=(",", ":")))
    provenance = {"source_archive_sha256": receipt["source_archive_sha256"],
                  "source_manifest_sha256": receipt["source_manifest_sha256"],
                  "broker_receipt_sha256": expected_receipt_sha256,
                  "request_sha256": receipt["request_sha256"],
                  "request_id": request["request_id"],
                  "session_id": response["session_id"],
                  "provider": response["provider"], "model": response["model"],
                  "attestation": response["attestation"],
                  "execution_manifest_sha256": _sha((target / "manifest.json").read_bytes())}
    (target / "provenance.json").write_text(json.dumps(provenance, sort_keys=True, indent=2) + "\n")
    return provenance


def send(request, socket_path, connection_factory=None):
    encoded = _canonical(request)
    if len(encoded) > MAX_REQUEST:
        raise ValueError("request byte limit")
    factory = connection_factory or (lambda: socket.socket(socket.AF_UNIX, socket.SOCK_STREAM))
    with factory() as connection:
        connection.settimeout(120)
        connection.connect(str(socket_path))
        connection.sendall(struct.pack("!I", len(encoded)) + encoded)
        header = _read_exact(connection, 4)
        size = struct.unpack("!I", header)[0]
        if not 0 < size <= MAX_RESPONSE:
            raise ValueError("broker response byte limit")
        response = json.loads(_read_exact(connection, size))
    _check_response(request, response)
    return response


def _read_exact(connection, length):
    chunks = []
    remaining = length
    while remaining:
        chunk = connection.recv(remaining)
        if not chunk:
            raise ValueError("truncated broker response")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    request_parser = sub.add_parser("request")
    for name in ("source-archive", "source-manifest", "prompt", "socket", "receipt"):
        request_parser.add_argument("--" + name, required=True)
    assembly_parser = sub.add_parser("assemble")
    for name in ("source-archive", "source-manifest", "receipt", "output"):
        assembly_parser.add_argument("--" + name, required=True)
    assembly_parser.add_argument("--prompt", required=True)
    assembly_parser.add_argument("--expected-receipt-sha256", required=True)
    args = parser.parse_args()
    if args.action == "assemble":
        print(json.dumps(assemble(args.source_archive, args.source_manifest, args.receipt, args.output,
                                  prompt_file=args.prompt, expected_receipt_sha256=args.expected_receipt_sha256), sort_keys=True))
        return
    request = prepare_source(args.source_archive, args.source_manifest, args.prompt)
    output = Path(args.receipt)
    if output.exists() or output.is_symlink():
        raise ValueError("response destination must be new")
    response = send(request, args.socket)
    receipt = make_receipt(request, response, args.source_archive, args.source_manifest)
    receipt_bytes = (json.dumps(receipt, indent=2, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    output.write_bytes(receipt_bytes)
    print(json.dumps({"session_id": response["session_id"], "receipt": str(output),
                      "receipt_sha256": _sha(receipt_bytes), "request_id": request["request_id"]}))


if __name__ == "__main__":
    main()
