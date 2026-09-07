#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_sella_sha256.py -- tools/sella_sha256.py --verifica.

Prueba dirigida permanente, justificada por un defecto real (encargo
`forense/encargos/2026-09-07-AUTOMATIZA-2-D-COSTURAS-FINALES.md`):
`--verifica` leía solo `f.readline()` -- un sidecar con una primera línea
correcta y basura después de esa línea se aceptaba igual, contradiciendo
el contrato de una sola línea exacta que el propio módulo documenta.

Corre solo:
    python3 tests/test_sella_sha256.py
"""
import hashlib
import os
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO_ROOT, "tools", "sella_sha256.py")


def _sha256_hex(contenido_bytes):
    return hashlib.sha256(contenido_bytes).hexdigest()


def _correr_verifica(fuente):
    r = subprocess.run(
        [sys.executable, TOOL, "--verifica", fuente],
        capture_output=True, text=True,
    )
    return r.returncode, r.stdout


def _prepara_fuente_y_sidecar(tmp, contenido_sidecar):
    """Escribe `fuente.md` (bytes fijos) + `fuente.sha256` con el
    contenido EXACTO que el llamador pida (sin normalizar), para poder
    fabricar sidecars deliberadamente mal formados."""
    fuente = os.path.join(tmp, "fuente.md")
    with open(fuente, "wb") as f:
        f.write(b"contenido de prueba\n")
    sidecar = os.path.join(tmp, "fuente.sha256")
    with open(sidecar, "w", encoding="utf-8") as f:
        f.write(contenido_sidecar)
    return fuente


def test_sidecar_valido_coincide():
    with tempfile.TemporaryDirectory() as tmp:
        fuente = os.path.join(tmp, "fuente.md")
        with open(fuente, "wb") as f:
            f.write(b"contenido de prueba\n")
        hash_real = _sha256_hex(b"contenido de prueba\n")
        with open(os.path.join(tmp, "fuente.sha256"), "w", encoding="utf-8") as f:
            f.write(f"{hash_real}  fuente.md\n")
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 0, salida
        assert "SELLO_COINCIDE" in salida


def test_segunda_linea_basura_rechazada():
    """El defecto real: primera línea correcta, segunda línea basura --
    `f.readline()` la aceptaba; el contrato exige rechazarla."""
    with tempfile.TemporaryDirectory() as tmp:
        hash_real = _sha256_hex(b"contenido de prueba\n")
        fuente = _prepara_fuente_y_sidecar(
            tmp, f"{hash_real}  fuente.md\nBASURA\n"
        )
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 3, salida
        assert "SELLO_NO_COINCIDE" in salida


def test_sin_newline_final_rechazado():
    with tempfile.TemporaryDirectory() as tmp:
        hash_real = _sha256_hex(b"contenido de prueba\n")
        fuente = _prepara_fuente_y_sidecar(tmp, f"{hash_real}  fuente.md")
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 3, salida
        assert "SELLO_NO_COINCIDE" in salida


def test_basename_distinto_rechazado():
    with tempfile.TemporaryDirectory() as tmp:
        hash_real = _sha256_hex(b"contenido de prueba\n")
        fuente = _prepara_fuente_y_sidecar(tmp, f"{hash_real}  otro.md\n")
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 3, salida
        assert "SELLO_NO_COINCIDE" in salida
        assert "basename no coincide" in salida


def test_hash_distinto_rechazado():
    with tempfile.TemporaryDirectory() as tmp:
        hash_falso = "0" * 64
        fuente = _prepara_fuente_y_sidecar(tmp, f"{hash_falso}  fuente.md\n")
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 3, salida
        assert "SELLO_NO_COINCIDE" in salida


def test_sidecar_ausente():
    with tempfile.TemporaryDirectory() as tmp:
        fuente = os.path.join(tmp, "fuente.md")
        with open(fuente, "wb") as f:
            f.write(b"contenido de prueba\n")
        codigo, salida = _correr_verifica(fuente)
        assert codigo == 2, salida
        assert "SIDECAR_AUSENTE" in salida


def main():
    casos = [
        test_sidecar_valido_coincide,
        test_segunda_linea_basura_rechazada,
        test_sin_newline_final_rechazado,
        test_basename_distinto_rechazado,
        test_hash_distinto_rechazado,
        test_sidecar_ausente,
    ]
    fallos = 0
    for caso in casos:
        try:
            caso()
            print("OK   {}".format(caso.__name__))
        except AssertionError as e:
            fallos += 1
            print("FAIL {}: {}".format(caso.__name__, e))
    print("---")
    if fallos:
        print("{} de {} casos FALLARON".format(fallos, len(casos)))
        return 1
    print("{} casos OK".format(len(casos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
