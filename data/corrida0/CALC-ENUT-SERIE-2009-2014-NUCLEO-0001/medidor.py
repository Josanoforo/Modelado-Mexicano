#!/usr/bin/env python3
"""Medidor de `CALC-ENUT-SERIE-2009-2014-NUCLEO-0001` (P4 del acto
GEN2-ENUT-PISOS-Y-SERIE-1, 21/sep/2026, CAJA).

El primer resultado que produzca este procedimiento es el que se reporta.

Las dos olas que completan la serie: ENUT 2014 (variantes NUCLEO y MIN) y
ENUT 2009 (sólo MIN; P1 dictamina C2 NO construible en 2009), con el mismo
módulo `tools/enut_nucleo.py` (input `IN-NUCLEO-MODULO`, sha256 comprobado
en disco antes de importar; auditoría AST antes de abrir un zip). Ambas
olas son DBF: 2009 directo en el zip, 2014 en el zip anidado `Enut2014.zip`
(la base nacional; `Enut2014_PoblacionIndigena.zip` es extracción y no
entra). Contrato humano: `forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md`.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
PAYLOADS = {"2014": "enut2014_bd_dbf", "2009": "enut2009_bd_dbf"}


def _modulo(inputs: dict):
    ruta = RAIZ / "tools" / "enut_nucleo.py"
    declarado = inputs["IN-NUCLEO-MODULO"]["sha256"]
    real = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if real != declarado:
        raise SystemExit(f"PARO · tools/enut_nucleo.py en disco ({real[:12]}) no es el "
                         f"declarado en la spec ({declarado[:12]})")
    spec = importlib.util.spec_from_file_location("enut_nucleo", ruta)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["enut_nucleo"] = mod
    spec.loader.exec_module(mod)
    viol = mod.auditoria_ast()
    if viol:
        raise SystemExit("PARO · guardia AST: " + " | ".join(viol[:10]))
    return mod


def medir(inputs: dict, contrato: dict) -> dict:
    n = _modulo(inputs)
    out = {}
    for ola, pid in PAYLOADS.items():
        out.update(n.medir_ola(ola, inputs[pid]["ruta_absoluta"],
                               int(contrato["parametros"]["bootstrap_replicas"]),
                               int(contrato["seed"]["valor"])))
        out[f"RESULT-ENUT{ola}-AUDITORIA-AST"] = "PASA"
    return out
