"""Shim congelado de CALC-ENOE-PISOS-0003."""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


def medir(inputs: dict, contrato: dict) -> dict:
    ruta = RAIZ / "tools" / "dominios" / "enoe" / "pisos_v1_2.py"
    esperado = inputs["IN-ENOE-MEDIDOR"]["sha256"]
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != esperado:
        raise RuntimeError(f"medidor ENOE mutable: {real} != {esperado}")
    spec = importlib.util.spec_from_file_location("enoe_pisos_sellado", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.medir(inputs, contrato)
