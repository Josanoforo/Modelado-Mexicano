#!/usr/bin/env python3
"""Pruebas dirigidas de tools/prepara_corpus.py."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepara_corpus.py"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(TOOL), *args], text=True,
                          capture_output=True, check=False)


def fixture(base: Path, *, shared_has_file: bool = True) -> tuple[Path, Path, Path, bytes]:
    root = base / "worktree"
    shared = base / "shared"
    recovery = base / "recovery"
    root.joinpath("data").mkdir(parents=True)
    shared.mkdir()
    recovery.joinpath("lote").mkdir(parents=True)
    payload = b"payload conocido\n"
    recovery.joinpath("lote", "objeto.bin").write_bytes(payload)
    if shared_has_file:
        shared.joinpath("lote").mkdir()
        shared.joinpath("lote", "objeto.bin").write_bytes(payload)
    root.joinpath("data", "manifiesto.yaml").write_text(yaml.safe_dump([{
        "id": "objeto", "archivo": "lote/objeto.bin", "sha256": digest(payload),
        "tamano_bytes": len(payload),
    }], sort_keys=False), encoding="utf-8")
    config = base / "raices.yaml"
    config.write_text(yaml.safe_dump({"data_raw": str(shared)}), encoding="utf-8")
    return root, shared, recovery, payload


def test_preview_no_escribe() -> None:
    with tempfile.TemporaryDirectory() as td:
        root, _shared, _recovery, _payload = fixture(Path(td))
        result = run("--root", str(root), "--config-desde", str(Path(td) / "raices.yaml"), "--id", "objeto")
        assert result.returncode == 0, result.stderr + result.stdout
        assert "modo\tPREVISUALIZA" in result.stdout
        assert "objeto\tdata_raw\t" in result.stdout
        assert "\tDESTINO_IDENTICO" in result.stdout
        assert not root.joinpath("data", "raw").exists()
        assert not root.joinpath("data", "raices.local.yaml").exists()


def test_aplica_e_idempotente() -> None:
    with tempfile.TemporaryDirectory() as td:
        root, shared, _recovery, _payload = fixture(Path(td))
        common = ("--root", str(root), "--config-desde", str(Path(td) / "raices.yaml"), "--id", "objeto", "--aplica")
        first = run(*common)
        assert first.returncode == 0, first.stderr + first.stdout
        assert "objeto\tdata_raw\t" in first.stdout
        assert "\tCOINCIDE" in first.stdout
        assert root.joinpath("data", "raw").is_symlink()
        assert root.joinpath("data", "raw").resolve() == shared.resolve()
        second = run(*common)
        assert second.returncode == 0, second.stderr + second.stdout
        assert "config\tLISTO" in second.stdout
        assert "montaje_data_raw\tLISTO" in second.stdout


def test_recupera_solo_id_validado_y_conserva_origen() -> None:
    with tempfile.TemporaryDirectory() as td:
        root, shared, recovery, payload = fixture(Path(td), shared_has_file=False)
        common = ("--root", str(root), "--config-desde", str(Path(td) / "raices.yaml"),
                  "--recupera-desde", str(recovery), "--id", "objeto")
        preview = run(*common)
        assert preview.returncode == 0, preview.stderr + preview.stdout
        assert "RECUPERARIA" in preview.stdout
        assert not shared.joinpath("lote", "objeto.bin").exists()
        applied = run(*common, "--aplica")
        assert applied.returncode == 0, applied.stderr + applied.stdout
        assert shared.joinpath("lote", "objeto.bin").read_bytes() == payload
        assert recovery.joinpath("lote", "objeto.bin").read_bytes() == payload
        assert "\tCOINCIDE" in applied.stdout


def test_no_sobreescribe_conflicto() -> None:
    with tempfile.TemporaryDirectory() as td:
        root, shared, recovery, _payload = fixture(Path(td), shared_has_file=False)
        shared.joinpath("lote").mkdir()
        target = shared.joinpath("lote", "objeto.bin")
        target.write_bytes(b"distinto\n")
        result = run("--root", str(root), "--config-desde", str(Path(td) / "raices.yaml"),
                     "--recupera-desde", str(recovery), "--id", "objeto", "--aplica")
        assert result.returncode == 1
        assert "CONFLICTO_DESTINO" in result.stdout
        assert target.read_bytes() == b"distinto\n"


if __name__ == "__main__":
    test_preview_no_escribe()
    test_aplica_e_idempotente()
    test_recupera_solo_id_validado_y_conserva_origen()
    test_no_sobreescribe_conflicto()
    print("OK -- test_prepara_corpus.py: 4 pruebas")
