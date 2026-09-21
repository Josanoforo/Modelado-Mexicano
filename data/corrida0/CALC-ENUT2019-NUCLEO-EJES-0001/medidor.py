#!/usr/bin/env python3
"""Medidor de `CALC-ENUT2019-NUCLEO-EJES-0001` (P2 del acto
GEN2-ENUT-PISOS-Y-SERIE-1, 21/sep/2026, CAJA).

El primer resultado que produzca este procedimiento es el que se reporta.

Piso t−1 de ENUT 2019 por UNA variable de agrupación (nacional · sexo · edad ·
escolaridad · localidad) para dos variantes de horas de cuidado: NUCLEO (C2)
y MIN (C3). El código que mide
es `tools/enut_nucleo.py`, declarado como input `IN-NUCLEO-MODULO` con
sha256: este archivo comprueba que el módulo en disco es exactamente ese
antes de importarlo, corre su auditoría AST (guardia de una sola variable,
3D) y sólo entonces abre el zip. Contrato humano:
`forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md`.

ORO (D-22 ampliada): el mismo módulo, apuntado a 2024 en
`CALC-ENUT2024-NUCLEO-EJES-0001`, reproduce la razón sellada de
`CALC-ENUT-0001` y la fórmula de tvar_crea; ese CALC corre y se verifica
ANTES de abrir 2019 (compuerta §8 del encargo). Aquí no hay oro propio:
2019 no tiene sellado previo.
"""
from __future__ import annotations

import hashlib
import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
OLA = "2019"
PAYLOAD = "enut2019_bd_csv"


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
    out = n.medir_ola(OLA, inputs[PAYLOAD]["ruta_absoluta"],
                      int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]))
    out[f"RESULT-ENUT{OLA}-AUDITORIA-AST"] = "PASA"
    return out
