#!/usr/bin/env python3
"""Medidor de `CALC-ENUT2024-NUCLEO-EJES-0001` (P3 del acto
GEN2-ENUT-PISOS-Y-SERIE-1, 21/sep/2026, CAJA).

El primer resultado que produzca este procedimiento es el que se reporta.

R de ENUT 2024 por UNA variable de agrupación (nacional · sexo · edad ·
escolaridad · localidad) para tres variantes de horas de cuidado: NUCLEO (C2),
MIN (C3) y CONCP (C1, la definición sellada, secundaria). El código que mide
es `tools/enut_nucleo.py`, declarado como input `IN-NUCLEO-MODULO` con
sha256: este archivo comprueba que el módulo en disco es exactamente ese
antes de importarlo, corre su auditoría AST (guardia de una sola variable,
3D) y sólo entonces abre el zip. Contrato humano:
`forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md`.

ORO (D-22 ampliada): la razón `RESULT-ENUT-A-R` de `CALC-ENUT-0001` (input
`IN-ORO-CALC-ENUT-0001`, sellado) se recalcula con la misma álgebra desde
tvar_crea y se reporta `ORO-A-R-DELTA`; y la suma de TODOS los ítems crudos
de TMODULO se coteja persona por persona contra `*_CON_CP` de tvar_crea
(`VALIDACION-CONCP-*`). Ninguno de los dos se parcha: son RESULT.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
OLA = "2024"
PAYLOAD = "enut2024_bd_csv"


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
    oro_json = json.loads(inputs["IN-ORO-CALC-ENUT-0001"]["bytes"])
    a_r = float(oro_json["resultados"]["RESULT-ENUT-A-R"])
    out = n.medir_ola(OLA, inputs[PAYLOAD]["ruta_absoluta"],
                      int(contrato["parametros"]["bootstrap_replicas"]),
                      int(contrato["seed"]["valor"]), oro={"A_R": a_r})
    out[f"RESULT-ENUT{OLA}-AUDITORIA-AST"] = "PASA"
    return out
