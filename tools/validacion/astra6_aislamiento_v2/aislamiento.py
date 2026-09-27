"""Allowlist verificada y frontera de proceso Linux; falla cerrada sin namespaces."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import socket
import stat
import subprocess
import tempfile
import tarfile
import re

STATUS_OK = "APTO-TECNICAMENTE"
STATUS_BLOCKED = "NO-LANZAR-COMO-CIEGA"


def _is_clone(path):
    marker = path / ".git"
    return marker.is_file() or (marker / "HEAD").is_file()


def _path(value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise ValueError("ruta inválida")
    path = PurePosixPath(value)
    if path.is_absolute() or any(p in ("", ".", "..") for p in value.split("/")):
        raise ValueError("ruta absoluta/ascendente/no canónica")
    banned = {".git", ".ssh", ".aws", ".codex", ".env", "medidor.py", "resultados.json"}
    if any(p.lower() in banned or p.lower().startswith(".env.") for p in path.parts):
        raise ValueError("archivo excluido de entrada ciega")
    return path


def _read_regular(root, relative):
    """openat con NOFOLLOW en cada componente: no sigue enlaces ni carreras."""
    fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in relative.parts[:-1]:
            next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        leaf = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        try:
            if not stat.S_ISREG(os.fstat(leaf).st_mode):
                raise ValueError("solo archivos regulares")
            with os.fdopen(leaf, "rb", closefd=False) as stream:
                return stream.read()
        finally:
            os.close(leaf)
    finally:
        os.close(fd)


def materialize(source_root, destination, allowlist):
    """Copia solamente archivos explícitos con SHA previo; nunca extrae archivos."""
    source = Path(source_root).absolute()
    if source.is_symlink():
        raise ValueError("raíz fuente enlazada")
    source = source.resolve(strict=True)
    destination = Path(destination).absolute()
    parent = destination.parent.resolve(strict=True)
    if parent != destination.parent or destination.exists() or destination.is_symlink():
        raise ValueError("destino debe ser nuevo y sin enlaces")
    clone = next((p for p in (source, *source.parents) if _is_clone(p)), source)
    if destination.is_relative_to(clone):
        raise ValueError("destino dentro del clon/fuente")
    if not isinstance(allowlist, list) or not allowlist:
        raise ValueError("allowlist explícita no vacía requerida")
    contents, seen = [], set()
    for item in allowlist:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ValueError("entrada requiere exclusivamente path y sha256")
        relative = _path(item["path"])
        if str(relative) in seen:
            raise ValueError("ruta duplicada")
        seen.add(str(relative))
        data = _read_regular(source, relative)
        digest = hashlib.sha256(data).hexdigest()
        if digest != item["sha256"]:
            raise ValueError("SHA de entrada no coincide")
        contents.append((relative, data, digest))
    # Toda validación precede a la creación; los bytes de archivos contenedores
    # no se descomprimen: miembros ZIP/TAR no pueden crear rutas o enlaces.
    destination.mkdir(mode=0o700)
    for relative, data, _ in contents:
        target = destination / str(relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o400)
    return {"root": str(destination), "files": [
        {"path": str(path), "sha256": digest} for path, _, digest in contents]}


def materialize_archive(archive, destination, allowlist, max_bytes=64 * 1024 * 1024):
    """TAR validado entero antes de copiar; ningún extract/extractall permisivo."""
    archive = Path(archive).absolute()
    if archive.is_symlink() or archive.parent != archive.parent.resolve(strict=True):
        raise ValueError("contenedor enlazado")
    if not isinstance(allowlist, list) or not allowlist or any(
        not isinstance(item, dict) or set(item) != {"path", "sha256"} for item in allowlist
    ):
        raise ValueError("allowlist explícita con path y sha256 requerida")
    clone = next((p for p in archive.parents if _is_clone(p)), None)
    if clone is not None and Path(destination).absolute().is_relative_to(clone):
        raise ValueError("destino dentro del clon/fuente")
    with tarfile.open(archive, "r:*") as container:
        members, seen, total = [], set(), 0
        for member in container:
            relative = _path(member.name.rstrip("/") if member.isdir() else member.name)
            if str(relative) in seen or not (member.isdir() or member.isfile()):
                raise ValueError("miembro TAR duplicado/enlace/especial")
            seen.add(str(relative))
            total += member.size
            if total > max_bytes:
                raise ValueError("contenedor supera límite explícito de bytes")
            members.append((member, relative))
        requested = {str(_path(item["path"])) for item in allowlist}
        with tempfile.TemporaryDirectory(prefix="astra6-tar-") as temporary:
            stage = Path(temporary)
            for member, relative in members:
                if member.isfile() and str(relative) in requested:
                    target = stage / str(relative)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with container.extractfile(member) as stream:
                        target.write_bytes(stream.read())
            return materialize(stage, destination, allowlist)


def sandbox_command(root, argv):
    root = Path(root).absolute()
    if root.is_symlink() or root != root.resolve(strict=True) or not root.is_dir():
        raise ValueError("raíz debe ser directorio real sin enlaces")
    if any(_is_clone(parent) for parent in (root, *root.parents)):
        raise ValueError("raíz de ejecución dentro del clon")
    for member in root.rglob("*"):
        _path(member.relative_to(root).as_posix())
        if member.is_symlink() or not (member.is_file() or member.is_dir()):
            raise ValueError("miembro peligroso en raíz de ejecución")
    backend = shutil.which("bwrap")
    if not backend:
        raise RuntimeError(STATUS_BLOCKED + ": bubblewrap no disponible")
    if not argv or not all(isinstance(arg, str) for arg in argv):
        raise ValueError("argv explícito requerido")
    command = [backend, "--unshare-all", "--die-with-parent", "--new-session", "--cap-drop", "ALL"]
    for source, target in runtime_allowlist():
        command += ["--ro-bind", source, target]
    command += ["--proc", "/proc", "--dev", "/dev", "--tmpfs", "/tmp",
                "--dir", "/salida", "--ro-bind", str(root), "/entrada",
                "--chdir", "/entrada", "--clearenv", "--setenv", "PATH", "/usr/bin:/bin",
                "--setenv", "HOME", "/tmp", "--setenv", "LANG", "C.UTF-8", "--", *argv]
    return command


def runtime_allowlist():
    """Python stdlib y cierre dinámico explícito; sin árboles /usr o /lib."""
    python = Path("/usr/bin/python3").resolve(strict=True)
    clean_env = {"PATH": "/usr/bin:/bin", "LC_ALL": "C"}
    metadata = subprocess.run(
        [str(python), "-I", "-c", "import sysconfig; print(sysconfig.get_path('stdlib'))"],
        env=clean_env, stdin=subprocess.DEVNULL, capture_output=True, text=True,
        check=True, timeout=10)
    stdlib = Path(metadata.stdout.strip()).resolve(strict=True)
    if not stdlib.is_relative_to(Path("/usr/lib")):
        raise RuntimeError("runtime requiere stdlib Python del sistema en /usr/lib")
    bindings = {"/usr/bin/python3": str(python)}
    for member in sorted(stdlib.iterdir()):
        if member.name in ("site-packages", "dist-packages", "__pycache__"):
            continue
        if member.is_file() and member.suffix == ".py" or (
            member.is_dir() and ((member / "__init__.py").is_file() or member.name == "lib-dynload")
        ):
            bindings[str(member)] = str(member.resolve(strict=True))
    binaries = [python, *sorted((stdlib / "lib-dynload").glob("*.so"))]
    for binary in binaries:
        report = subprocess.run(["/usr/bin/ldd", str(binary)], env=clean_env,
                                stdin=subprocess.DEVNULL, capture_output=True,
                                text=True, check=True, timeout=10)
        if "not found" in report.stdout:
            raise RuntimeError("biblioteca dinámica ausente en runtime")
        for dependency in re.findall(r"/[^\s()]+", report.stdout):
            resolved = Path(dependency).resolve(strict=True)
            if not resolved.is_file() or not resolved.is_relative_to(Path("/usr/lib")):
                raise RuntimeError("dependencia dinámica fuera del runtime permitido")
            bindings[dependency] = str(resolved)
    return [(source, target) for target, source in sorted(bindings.items())]


def _execute(root, argv, timeout):
    return subprocess.run(sandbox_command(root, argv), env={"PATH": "/usr/bin:/bin"},
                          stdin=subprocess.DEVNULL, text=True, capture_output=True,
                          timeout=timeout, close_fds=True)


def _probe_environment():
    """Canarios propios: lectura entrada, escritura denegada, exterior y TCP/UDP."""
    evidence = {"status": STATUS_BLOCKED, "backend": "bubblewrap", "canaries": {}}
    with tempfile.TemporaryDirectory(prefix="astra6-canary-") as temporary:
        base = Path(temporary)
        root = base / "input"
        root.mkdir()
        (root / "allowed.txt").write_text("SYNTHETIC-ALLOWED")
        outside = base / "outside.txt"
        outside.write_text("SYNTHETIC-OUTSIDE")
        try:
            startup = _execute(root, ["/usr/bin/python3", "-I", "-c", "print('namespace-started')"], 10)
            if startup.returncode:
                evidence["reason"] = startup.stderr.strip()[:1000]
                return evidence
        except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
            evidence["reason"] = str(error)[:1000]
            return evidence
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            port = listener.getsockname()[1]
            code = '''import json, socket
from pathlib import Path
r={"input_read": Path("/entrada/allowed.txt").read_text()=="SYNTHETIC-ALLOWED"}
try: Path("/entrada/allowed.txt").write_text("CHANGED"); r["input_write_denied"]=False
except OSError: r["input_write_denied"]=True
try: Path(OUTSIDE).read_text(); r["outside_read_denied"]=False
except OSError: r["outside_read_denied"]=True
for kind, target in [(socket.SOCK_STREAM,("127.0.0.1",PORT)),(socket.SOCK_DGRAM,("192.0.2.1",9))]:
 s=socket.socket(socket.AF_INET,kind); s.settimeout(.3)
 try:
  if kind==socket.SOCK_STREAM: s.connect(target)
  else: s.sendto(b"synthetic",target)
  r["tcp_denied" if kind==socket.SOCK_STREAM else "udp_denied"]=False
 except OSError: r["tcp_denied" if kind==socket.SOCK_STREAM else "udp_denied"]=True
 finally: s.close()
print(json.dumps(r))
'''.replace("OUTSIDE", repr(str(outside))).replace("PORT", str(port))
            try:
                result = _execute(root, ["/usr/bin/python3", "-I", "-c", code], 10)
                if result.returncode:
                    evidence["reason"] = result.stderr.strip()[:1000]
                else:
                    evidence["canaries"] = json.loads(result.stdout)
                    if len(evidence["canaries"]) == 5 and all(evidence["canaries"].values()):
                        evidence["status"] = STATUS_OK
                    else:
                        evidence["reason"] = "canario de frontera falló"
            except (OSError, RuntimeError, subprocess.TimeoutExpired, ValueError) as error:
                evidence["reason"] = str(error)[:1000]
    return evidence


def probe_environment():
    try:
        proof = _probe_environment()
    except (OSError, RuntimeError, subprocess.SubprocessError, ValueError) as error:
        proof = {"status": STATUS_BLOCKED, "backend": "bubblewrap", "canaries": {},
                 "reason": "preparación de canario/namespace: " + str(error)[:1000]}
    proof["estado"] = proof["status"]
    return proof


def run_isolated(root, argv, timeout=30):
    proof = probe_environment()
    if proof["status"] != STATUS_OK:
        raise RuntimeError(STATUS_BLOCKED + ": " + proof.get("reason", "sin prueba"))
    return _execute(root, argv, timeout)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("probe")
    material = sub.add_parser("materialize")
    material.add_argument("--source", required=True)
    material.add_argument("--destination", required=True)
    material.add_argument("--allowlist", required=True)
    run = sub.add_parser("run")
    run.add_argument("--root", required=True)
    run.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.action == "probe":
            proof = probe_environment()
            print(json.dumps(proof, ensure_ascii=False, sort_keys=True))
            return 0 if proof["status"] == STATUS_OK else 2
        if args.action == "materialize":
            operation = materialize_archive if Path(args.source).is_file() else materialize
            print(json.dumps(operation(args.source, args.destination,
                                      json.loads(Path(args.allowlist).read_text()))))
            return 0
        result = run_isolated(args.root, args.argv[1:] if args.argv[:1] == ["--"] else args.argv)
        print(result.stdout, end="")
        print(result.stderr, end="", file=__import__("sys").stderr)
        return result.returncode
    except (OSError, ValueError, RuntimeError, tarfile.TarError) as error:
        parser.exit(2, str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
