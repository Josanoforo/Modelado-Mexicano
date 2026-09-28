"""Portable v3 blind executor. No host fallback when an isolation backend fails.

The namespace backend needs working unprivileged user, mount, network and PID
namespaces. OCI backends need an image named by its immutable sha256 digest.
Only the explicit input bundle is mounted; selected output is returned as TAR.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import selectors
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time

MAX_INPUT = 64 * 1024 * 1024
MAX_OUTPUT = 128 * 1024 * 1024
SHA = re.compile(r"^[0-9a-f]{64}$")
IMAGE = re.compile(r"^[^\s]+@sha256:[0-9a-f]{64}$")


def safe_path(value):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("invalid path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in ("", ".", "..") for part in value.split("/")):
        raise ValueError("noncanonical path")
    banned = {".git", ".ssh", ".aws", ".codex", ".env", "medidor.py", "resultados.json"}
    if any(part.lower() in banned or part.lower().startswith(".env.") for part in path.parts):
        raise ValueError("forbidden input/output path")
    return path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def runtime_inventory():
    """Pin every staged runtime byte, including transitive ELF dependencies."""
    python = Path(sys.executable).resolve(strict=True)
    stdlib = Path(subprocess.check_output([str(python), "-I", "-c", "import sysconfig;print(sysconfig.get_path('stdlib'))"], text=True).strip())
    numpy = Path("/usr/lib/python3/dist-packages/numpy")
    if not python.is_relative_to(Path("/usr/bin")) or not stdlib.is_relative_to(Path("/usr/lib")) or not numpy.is_dir():
        raise RuntimeError("unapproved system Python/NumPy layout")
    selected = {python, Path("/usr/bin/setpriv")}
    for directory in (stdlib, numpy):
        for source in directory.rglob("*"):
            if source.is_file() and not any(part in {"__pycache__", "test", "tests"} for part in source.relative_to(directory).parts):
                selected.add(source)
    binaries = [path for path in selected if path in (python, Path("/usr/bin/setpriv")) or path.suffix == ".so"]
    for binary in binaries:
        report = subprocess.run(["/usr/bin/ldd", str(binary)], capture_output=True, text=True, check=True)
        if "not found" in report.stdout:
            raise RuntimeError("unresolved runtime shared library")
        for item in re.findall(r"/[A-Za-z0-9_+./-]+", report.stdout):
            source = Path(item)
            if source.is_file() and any(source.is_relative_to(Path(prefix)) for prefix in ("/usr/lib", "/lib", "/lib64")):
                selected.add(source)
    numpy_version = subprocess.check_output([str(python), "-I", "-c", "import numpy;print(numpy.__version__)"], text=True).strip()
    return {"python_version": sys.version.split()[0], "numpy_version": numpy_version,
            "files": {str(path): digest(path.read_bytes()) for path in sorted(selected)}}


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or set(manifest) != {
        "version", "entrypoint", "input_files", "output_files", "max_total_output_bytes"
    } or manifest["version"] != 1:
        raise ValueError("manifest v1 keys required")
    inputs, outputs = manifest["input_files"], manifest["output_files"]
    if not isinstance(inputs, list) or not inputs or not isinstance(outputs, list) or not outputs:
        raise ValueError("nonempty explicit file lists required")
    seen = set()
    for item in inputs:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("input requires path and sha256")
        path = str(safe_path(item["path"]))
        if path in seen or not isinstance(item["sha256"], str) or not SHA.fullmatch(item["sha256"]):
            raise ValueError("duplicate input or invalid sha256")
        seen.add(path)
    entry = str(safe_path(manifest["entrypoint"]))
    if entry not in seen or not entry.endswith(".py"):
        raise ValueError("entrypoint must be an allowed Python file")
    seen = set()
    for item in outputs:
        if not isinstance(item, dict) or set(item) != {"path", "max_bytes"}:
            raise ValueError("output requires path and max_bytes")
        path = str(safe_path(item["path"]))
        if path in seen or not isinstance(item["max_bytes"], int) or isinstance(item["max_bytes"], bool) or not 0 < item["max_bytes"] <= MAX_OUTPUT:
            raise ValueError("duplicate output or invalid byte limit")
        seen.add(path)
    maximum = manifest["max_total_output_bytes"]
    if not isinstance(maximum, int) or isinstance(maximum, bool) or not 0 < maximum <= MAX_OUTPUT:
        raise ValueError("invalid aggregate output limit")
    if sum(item["max_bytes"] for item in outputs) > maximum:
        raise ValueError("aggregate cap smaller than declared files")
    return manifest


def _new_directory(path):
    path = Path(path).absolute()
    if path.exists() or path.is_symlink() or path.parent.resolve(strict=True) != path.parent:
        raise ValueError("destination must be new, with real parent")
    path.mkdir(mode=0o700)
    return path


def build(archive, manifest_file, output):
    manifest = validate_manifest(json.loads(Path(manifest_file).read_text()))
    archive = Path(archive).absolute()
    if archive.is_symlink() or not archive.is_file():
        raise ValueError("archive must be a regular file")
    expected = {item["path"]: item["sha256"] for item in manifest["input_files"]}
    contents = {}
    total = 0
    with tarfile.open(archive, "r:*") as tar:
        seen = set()
        for member in tar:
            path = str(safe_path(member.name.rstrip("/") if member.isdir() else member.name))
            if path in seen or not (member.isdir() or member.isfile()):
                raise ValueError("duplicate, link or special TAR member")
            seen.add(path)
            if member.isdir():
                continue
            if path not in expected or member.size < 0:
                raise ValueError("TAR member absent from input allowlist")
            total += member.size
            if total > MAX_INPUT:
                raise ValueError("input byte limit exceeded")
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError("TAR file without content")
            data = stream.read(member.size + 1)
            if len(data) != member.size or digest(data) != expected[path]:
                raise ValueError("input length or sha256 mismatch")
            contents[path] = data
    if set(contents) != set(expected):
        raise ValueError("incomplete input TAR")
    bundle = _new_directory(output)
    input_root = bundle / "input"
    input_root.mkdir(mode=0o755)
    for path, data in contents.items():
        target = input_root / path
        target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
        target.write_bytes(data)
        target.chmod(0o444)
    (bundle / "manifest.json").write_text(json.dumps(manifest, sort_keys=True, separators=(",", ":")))
    (bundle / "manifest.json").chmod(0o444)
    (bundle / "runtime-lock.json").write_text(json.dumps(runtime_inventory(), sort_keys=True, separators=(",", ":")))
    (bundle / "runtime-lock.json").chmod(0o444)
    (bundle / "seal.json").write_text(json.dumps({"manifest_sha256": digest((bundle / "manifest.json").read_bytes()),
                                            "runtime_lock_sha256": digest((bundle / "runtime-lock.json").read_bytes())}, sort_keys=True))
    (bundle / "seal.json").chmod(0o444)
    return {"bundle": str(bundle), "manifest_sha256": digest((bundle / "manifest.json").read_bytes()), "runtime_lock_sha256": digest((bundle / "runtime-lock.json").read_bytes()), "input_count": len(contents)}


def verify_bundle(bundle):
    bundle = Path(bundle).absolute()
    if bundle.is_symlink() or bundle.resolve(strict=True) != bundle:
        raise ValueError("bundle root must be real")
    seal = json.loads((bundle / "seal.json").read_text())
    if seal != {"manifest_sha256": digest((bundle / "manifest.json").read_bytes()),
                "runtime_lock_sha256": digest((bundle / "runtime-lock.json").read_bytes())}:
        raise ValueError("bundle seal mismatch")
    manifest = validate_manifest(json.loads((bundle / "manifest.json").read_text()))
    expected = {x["path"]: x["sha256"] for x in manifest["input_files"]}
    root = bundle / "input"
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError("unsafe input member")
        if path.is_file():
            relative = path.relative_to(root).as_posix()
            safe_path(relative)
            actual.add(relative)
            if relative not in expected or digest(path.read_bytes()) != expected[relative]:
                raise ValueError("input bundle was altered")
    if actual != set(expected):
        raise ValueError("input bundle incomplete")
    lock_file = bundle / "runtime-lock.json"
    if lock_file.is_symlink() or not lock_file.is_file():
        raise ValueError("runtime lock missing")
    lock = json.loads(lock_file.read_text())
    if lock != runtime_inventory():
        raise ValueError("host Python/NumPy runtime differs from pinned lock")
    return manifest


# This code runs only after a fresh namespace/chroot or digest-pinned OCI start.
# The reconstruction sees only /entrada, /salida and the runtime, not the host.
RUNNER = r'''import hashlib, io, json, os, runpy, sys, tarfile, traceback
from pathlib import Path
m=json.loads(Path('/entrada-manifest.json').read_text())
class Limited(io.TextIOBase):
 def __init__(self,path): self.f=open(path,'w'); self.n=0
 def write(self,s):
  s=str(s); self.n+=len(s.encode('utf-8'))
  if self.n>1048576: raise RuntimeError('diagnostic limit')
  return self.f.write(s)
 def flush(self): self.f.flush()
oldout,olderr=sys.stdout,sys.stderr
sys.stdout,sys.stderr=Limited('/salida/stdout.txt'),Limited('/salida/stderr.txt')
ok=True
try: runpy.run_path('/entrada/'+m['entrypoint'],run_name='__main__')
except BaseException:
 ok=False; traceback.print_exc(file=sys.stderr)
finally:
 sys.stdout.flush();sys.stderr.flush();sys.stdout=oldout;sys.stderr=olderr
files=[]
if ok:
 for item in m['output_files']:
  p=Path('/salida')/item['path']
  if p.is_symlink() or not p.is_file() or p.stat().st_size>item['max_bytes']:
   ok=False;break
  files.append((item['path'],p))
for name in ('stdout.txt','stderr.txt'):
 p=Path('/salida')/name
 if p.is_file() and p.stat().st_size<=1048576: files.append((name,p))
if not ok: sys.exit(44)
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|',format=tarfile.USTAR_FORMAT) as t:
 for name,p in files:
  info=tarfile.TarInfo(name);info.size=p.stat().st_size;info.mode=0o444
  with p.open('rb') as stream:t.addfile(info,stream)
'''


def _namespace_child(bundle, rootfs):
    # Bind mounts are denied on some hosts even inside user namespaces. Stage
    # only the selected interpreter/runtime, then remount that tmpfs read-only.
    # The host mount table is never modified.
    subprocess.run(["mount", "--make-rprivate", "/"], check=True)
    root = Path(rootfs)
    subprocess.run(["mount", "-t", "tmpfs", "-o", "size=536870912,nosuid,nodev", "tmpfs", str(root)], check=True)
    for name in ("usr", "lib", "lib64", "entrada", "salida", "tmp"):
        (root / name).mkdir(exist_ok=True)
    (root / "usr/bin").mkdir(parents=True, exist_ok=True)
    python = Path(sys.executable).resolve(strict=True)
    stdlib = Path(subprocess.check_output([str(python), "-I", "-c", "import sysconfig;print(sysconfig.get_path('stdlib'))"], text=True).strip())
    if not python.is_relative_to(Path("/usr/bin")) or not stdlib.is_relative_to(Path("/usr/lib")):
        raise RuntimeError("unapproved system Python layout")
    runtime_paths = [python, Path("/usr/bin/setpriv")]
    shutil.copy2(python, root / "usr/bin" / python.name)
    shutil.copy2("/usr/bin/setpriv", root / "usr/bin/setpriv")
    (root / "usr/bin/python3").symlink_to(python.name)
    shutil.copytree(stdlib, root / stdlib.relative_to("/"), symlinks=False,
                    ignore=shutil.ignore_patterns("__pycache__", "test", "tests"))
    numpy = Path("/usr/lib/python3/dist-packages/numpy")
    if not numpy.is_dir():
        raise RuntimeError("NumPy runtime unavailable")
    (root / "usr/lib/python3/dist-packages").mkdir(parents=True, exist_ok=True)
    shutil.copytree(numpy, root / numpy.relative_to("/"), symlinks=False,
                    ignore=shutil.ignore_patterns("__pycache__", "test", "tests"))
    runtime_paths += list(stdlib.rglob("*.so")) + list(numpy.rglob("*.so"))
    dependencies = set()
    for binary in runtime_paths:
        report = subprocess.run(["/usr/bin/ldd", str(binary)], capture_output=True, text=True, check=True)
        if "not found" in report.stdout:
            raise RuntimeError("unresolved runtime shared library")
        for item in re.findall(r"/[A-Za-z0-9_+./-]+", report.stdout):
            source = Path(item)
            if source.is_file() and any(source.is_relative_to(Path(prefix)) for prefix in ("/usr/lib", "/lib", "/lib64")):
                dependencies.add(source)
    for source in dependencies:
        destination = root / source.relative_to("/")
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source.resolve(), destination)
    shutil.copytree(Path(bundle) / "input", root / "entrada", dirs_exist_ok=True)
    subprocess.run(["mount", "-t", "tmpfs", "-o", "size=134217728,nosuid,nodev", "tmpfs", str(root / "salida")], check=True)
    subprocess.run(["mount", "-t", "tmpfs", "-o", "size=16777216,nosuid,nodev", "tmpfs", str(root / "tmp")], check=True)
    shutil.copyfile(Path(bundle) / "manifest.json", root / "entrada-manifest.json")
    (root / "entrada-manifest.json").chmod(0o444)
    lock = json.loads((Path(bundle) / "runtime-lock.json").read_text())
    for source, expected_sha in lock["files"].items():
        target = root / source.lstrip("/")
        if not target.is_file() or digest(target.read_bytes()) != expected_sha:
            raise RuntimeError("staged runtime differs from pinned lock: " + source)
    subprocess.run(["mount", "-t", "tmpfs", "-o", "remount,ro", "tmpfs", str(root)], check=True)
    os.chroot(root)
    os.chdir("/")
    resource.setrlimit(resource.RLIMIT_AS, (1024 * 1024 * 1024, 1024 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_FSIZE, (128 * 1024 * 1024, 128 * 1024 * 1024))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
    os.environ.clear()
    os.environ.update({"PATH": "/usr/bin:/bin", "HOME": "/tmp", "LANG": "C.UTF-8", "PYTHONNOUSERSITE": "1", "OPENBLAS_NUM_THREADS": "1"})
    os.execv("/usr/bin/setpriv", ["setpriv", "--bounding-set=-all", "--inh-caps=-all", "--ambient-caps=-all", "/usr/bin/python3", "-I", "-c", RUNNER])


def _capture_limited(command, limit, timeout):
    process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8"}, close_fds=True)
    streams = {process.stdout: (bytearray(), limit), process.stderr: (bytearray(), 1048576)}
    selector = selectors.DefaultSelector()
    for stream in streams:
        selector.register(stream, selectors.EVENT_READ)
    deadline = time.monotonic() + timeout
    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RuntimeError("isolated runtime timed out")
            for key, _ in selector.select(remaining):
                chunk = os.read(key.fd, 65536)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                data, cap = streams[key.fileobj]
                if len(data) + len(chunk) > cap:
                    raise RuntimeError("isolated output exceeds transport limit")
                data.extend(chunk)
        remaining = deadline - time.monotonic()
        process.wait(timeout=max(0.01, remaining))
        if process.returncode:
            raise RuntimeError("isolated runtime failed: " + bytes(streams[process.stderr][0]).decode("utf-8", "replace")[:1000])
        return bytes(streams[process.stdout][0])
    finally:
        selector.close()
        if process.poll() is None:
            process.kill()
            process.wait()
        process.stdout.close()
        process.stderr.close()


def _extract(output_tar, manifest, output):
    if len(output_tar) < 1024 or len(output_tar) % 512 or output_tar[-1024:] != b"\0" * 1024:
        raise ValueError("truncated output TAR")
    expected = {x["path"]: x["max_bytes"] for x in manifest["output_files"]}
    expected.update({"stdout.txt": 1048576, "stderr.txt": 1048576})
    extracted = {}
    with tarfile.open(fileobj=io.BytesIO(output_tar), mode="r:") as tar:
        for member in tar:
            path = str(safe_path(member.name))
            if path in extracted or path not in expected or not member.isfile() or member.size > expected[path]:
                raise ValueError("unsafe or oversized output TAR member")
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError("incomplete output member")
            data = stream.read(member.size + 1)
            if len(data) != member.size:
                raise ValueError("truncated output member")
            extracted[path] = data
    if not set(x["path"] for x in manifest["output_files"]).issubset(extracted):
        raise ValueError("incomplete output TAR")
    if sum(len(data) for data in extracted.values()) > manifest["max_total_output_bytes"] + 2 * 1048576:
        raise ValueError("aggregate output limit exceeded")
    destination = _new_directory(output)
    rows = []
    for path, data in extracted.items():
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o444)
        rows.append({"path": path, "sha256": digest(data), "bytes": len(data)})
    export = {"version": 1, "files": sorted(rows, key=lambda x: x["path"]), "input_manifest_sha256": digest(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode())}
    (destination / "export-manifest.json").write_text(json.dumps(export, indent=2, sort_keys=True) + "\n")
    return export


def verify_export_consistency(output):
    """Check an export's internal file hashes; this is not a trusted seal."""
    root = Path(output).absolute()
    if root.is_symlink() or root.resolve(strict=True) != root:
        raise ValueError("export root changed")
    manifest_file = root / "export-manifest.json"
    if manifest_file.is_symlink() or not manifest_file.is_file():
        raise ValueError("missing export manifest")
    manifest = json.loads(manifest_file.read_text())
    if (not isinstance(manifest, dict) or set(manifest) != {"version", "files", "input_manifest_sha256"}
            or manifest["version"] != 1 or not isinstance(manifest["input_manifest_sha256"], str)
            or not SHA.fullmatch(manifest["input_manifest_sha256"]) or not isinstance(manifest["files"], list)):
        raise ValueError("invalid export manifest")
    expected = set()
    for item in manifest["files"]:
        if not isinstance(item, dict) or set(item) != {"path", "sha256", "bytes"}:
            raise ValueError("invalid export file record")
        relative = str(safe_path(item["path"]))
        if (relative in expected or not isinstance(item["sha256"], str) or not SHA.fullmatch(item["sha256"])
                or type(item["bytes"]) is not int or item["bytes"] < 0):
            raise ValueError("invalid export file identity")
        expected.add(relative)
        path = root / relative
        if path.is_symlink() or not path.is_file() or path.stat().st_size != item["bytes"] or digest(path.read_bytes()) != item["sha256"]:
            raise ValueError("export changed after seal")
    actual = set()
    for path in root.rglob("*"):
        if path.is_symlink() or not (path.is_dir() or path.is_file()):
            raise ValueError("unsafe export member")
        if path.is_file() and path != manifest_file:
            actual.add(path.relative_to(root).as_posix())
    if actual != expected:
        raise ValueError("export has missing or extra files")
    return manifest


def _package_identity(identity):
    if (not isinstance(identity, dict) or set(identity) != {"paquete", "version_entrada", "sha256_entrada"}
            or any(not isinstance(identity[key], str) or not identity[key] for key in identity)
            or not SHA.fullmatch(identity["sha256_entrada"])):
        raise ValueError("invalid package identity")
    return identity


def freeze_export(output, anchor_path, *, package_identity, expected_input_manifest_sha256):
    """Commit an export to a separate, new anchor before revealing references.

    The caller supplies the previously approved package identity and input
    manifest hash. Neither is inferred from the mutable export directory.
    The anchor itself must be retained by the trusted orchestrator.
    """
    identity = _package_identity(package_identity)
    if not isinstance(expected_input_manifest_sha256, str) or not SHA.fullmatch(expected_input_manifest_sha256):
        raise ValueError("invalid expected input manifest sha256")
    root = Path(output).absolute()
    anchor_path = Path(anchor_path).absolute()
    if anchor_path.is_relative_to(root):
        raise ValueError("anchor must be outside export directory")
    manifest = verify_export_consistency(root)
    if manifest["input_manifest_sha256"] != expected_input_manifest_sha256:
        raise ValueError("export belongs to a different input manifest")
    if "resultado.json" not in {item["path"] for item in manifest["files"]}:
        raise ValueError("export lacks resultado.json")
    result = json.loads((root / "resultado.json").read_text())
    if not isinstance(result, dict) or result.get("identidad") != identity:
        raise ValueError("result belongs to a different package")
    if anchor_path.exists() or anchor_path.is_symlink() or anchor_path.parent.resolve(strict=True) != anchor_path.parent:
        raise ValueError("anchor destination must be new, with real parent")
    anchor = {"version": 1, "package_identity": dict(identity),
              "input_manifest_sha256": expected_input_manifest_sha256,
              "export_manifest_sha256": digest((root / "export-manifest.json").read_bytes())}
    with anchor_path.open("x", encoding="utf-8") as stream:
        json.dump(anchor, stream, sort_keys=True, separators=(",", ":"))
        stream.write("\n")
    anchor_path.chmod(0o400)
    return anchor


def verify_export(output, anchor):
    """Verify export against the external anchor before opening a reference."""
    root = Path(output).absolute()
    anchor_path = Path(anchor).absolute()
    if anchor_path.is_relative_to(root) or anchor_path.is_symlink() or not anchor_path.is_file():
        raise ValueError("trusted anchor must be a separate regular file")
    trusted = json.loads(anchor_path.read_text())
    if (not isinstance(trusted, dict) or set(trusted) != {"version", "package_identity", "input_manifest_sha256", "export_manifest_sha256"}
            or trusted["version"] != 1 or not isinstance(trusted["input_manifest_sha256"], str)
            or not SHA.fullmatch(trusted["input_manifest_sha256"])
            or not isinstance(trusted["export_manifest_sha256"], str)
            or not SHA.fullmatch(trusted["export_manifest_sha256"])):
        raise ValueError("invalid trusted anchor")
    _package_identity(trusted["package_identity"])
    manifest_file = root / "export-manifest.json"
    if manifest_file.is_symlink() or not manifest_file.is_file() or digest(manifest_file.read_bytes()) != trusted["export_manifest_sha256"]:
        raise ValueError("export manifest differs from trusted anchor")
    manifest = verify_export_consistency(root)
    if manifest["input_manifest_sha256"] != trusted["input_manifest_sha256"]:
        raise ValueError("export input differs from trusted anchor")
    if "resultado.json" not in {item["path"] for item in manifest["files"]}:
        raise ValueError("export lacks resultado.json")
    result = json.loads((root / "resultado.json").read_text())
    if not isinstance(result, dict) or result.get("identidad") != trusted["package_identity"]:
        raise ValueError("result package differs from trusted anchor")
    return {"export": manifest, "anchor": trusted}


def run(bundle, output, backend, image=None, timeout=60):
    manifest = verify_bundle(bundle)
    bundle = Path(bundle).absolute()
    if backend == "namespace":
        if not shutil.which("unshare") or not shutil.which("mount") or not shutil.which("setpriv"):
            raise RuntimeError("namespace utilities unavailable")
        with tempfile.TemporaryDirectory(prefix="astra6-rootfs-") as temporary:
            command = ["unshare", "--user", "--map-root-user", "--mount", "--net", "--pid", "--ipc", "--uts", "--fork", sys.executable, str(Path(__file__).resolve()), "_namespace_child", "--bundle", str(bundle), "--rootfs", temporary]
            payload = _capture_limited(command, manifest["max_total_output_bytes"] + 3 * 1048576 + 65536, timeout)
    elif backend in ("podman", "docker"):
        if not isinstance(image, str) or not IMAGE.fullmatch(image):
            raise ValueError("OCI image must be named by sha256 digest")
        if not shutil.which(backend):
            raise RuntimeError("requested OCI backend unavailable")
        command = [backend, "run", "--rm", "--network=none", "--read-only", "--cap-drop=ALL", "--security-opt=no-new-privileges", "--pids-limit=64", "--memory=1g", "--user=65534:65534", "--tmpfs", "/salida:rw,nosuid,nodev,size=134217728", "--tmpfs", "/tmp:rw,nosuid,nodev,size=16777216", "--mount", f"type=bind,src={bundle / 'input'},dst=/entrada,readonly", "--mount", f"type=bind,src={bundle / 'manifest.json'},dst=/entrada-manifest.json,readonly", "-e", "HOME=/tmp", "-e", "PYTHONNOUSERSITE=1", "-e", "OPENBLAS_NUM_THREADS=1", image, "python3", "-I", "-c", RUNNER]
        payload = _capture_limited(command, manifest["max_total_output_bytes"] + 3 * 1048576 + 65536, timeout)
    else:
        raise ValueError("backend must be namespace, podman or docker")
    return _extract(payload, manifest, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    build_parser = sub.add_parser("build")
    for key in ("archive", "manifest", "output"):
        build_parser.add_argument("--" + key, required=True)
    run_parser = sub.add_parser("run")
    for key in ("bundle", "output"):
        run_parser.add_argument("--" + key, required=True)
    run_parser.add_argument("--backend", choices=("namespace", "podman", "docker"), required=True)
    run_parser.add_argument("--image")
    run_parser.add_argument("--timeout", type=int, default=60)
    freeze_parser = sub.add_parser("freeze-export")
    freeze_parser.add_argument("--export", required=True)
    freeze_parser.add_argument("--anchor", required=True)
    freeze_parser.add_argument("--identity", required=True)
    freeze_parser.add_argument("--input-manifest-sha256", required=True)
    verify_parser = sub.add_parser("verify-export")
    verify_parser.add_argument("--export", required=True)
    verify_parser.add_argument("--anchor", required=True)
    child = sub.add_parser("_namespace_child")
    child.add_argument("--bundle", required=True)
    child.add_argument("--rootfs", required=True)
    args = parser.parse_args()
    try:
        if args.action == "_namespace_child":
            _namespace_child(args.bundle, args.rootfs)
        if args.action == "build":
            result = build(args.archive, args.manifest, args.output)
        elif args.action == "run":
            result = run(args.bundle, args.output, args.backend, args.image, args.timeout)
        elif args.action == "freeze-export":
            identity = json.loads(Path(args.identity).read_text())
            result = freeze_export(args.export, args.anchor, package_identity=identity,
                                   expected_input_manifest_sha256=args.input_manifest_sha256)
        else:
            result = verify_export(args.export, args.anchor)
        print(json.dumps(result, sort_keys=True))
        return 0
    except (OSError, ValueError, RuntimeError, tarfile.TarError, subprocess.CalledProcessError) as exc:
        parser.exit(2, str(exc) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
