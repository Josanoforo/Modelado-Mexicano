"""Shim congelado para persistencia ENOE."""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]


def medir(inputs: dict, contrato: dict) -> dict:
    ruta = RAIZ / "tools" / "dominios" / "enoe" / "persistencia.py"
    esperado = inputs["IN-ENOE-PERSISTENCIA-MODULO"]["sha256"]
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != esperado:
        raise RuntimeError("módulo persistencia ENOE mutable")
    spec = importlib.util.spec_from_file_location("enoe_persistencia_sellada", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod.medir(inputs, contrato)
