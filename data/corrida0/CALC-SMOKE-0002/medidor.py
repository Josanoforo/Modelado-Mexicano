#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Medidor del SMOKE `CALC-SMOKE-0002` -- interfaz estable `medir(inputs,
contrato)` sobre `forense/prereg-duelo-v2/agregado_v1_3.py`.

ACTO GEN2-E3-1 · READINESS-DEL-RUNNER, P6. `repite_de: CALC-SMOKE-0001`
(declarado en `spec.yaml`): el MISMO calculo que ese smoke midio -- este
archivo es una copia byte-por-byte de la logica de `CALC-SMOKE-0001/
medidor.py`, adaptada solo a la firma nueva del medidor
(`medir(inputs, contrato)` en vez de `medir(inputs, params)`, P2) y no a
otra cosa: el objeto medido sigue siendo el aparato de corrida
(`preflight`/`run`/`verify`), no el duelo. Es un ADAPTADOR y nada mas:
importa `agregado_v1_3.py` POR RUTA y **no le toca ni una linea** -- el
perimetro de este acto excluye `forense/prereg-duelo-v2/`.

`medir(inputs, contrato)` ignora `inputs` y `contrato` a proposito: el
script legacy resuelve sus propias rutas relativas a su directorio, y
falsear eso inyectandole rutas seria justo la clase de adaptacion que
haria que el replay dejara de ser un replay. Los `inputs` de la spec
existen para que `preflight`/`verify` los hasheen -- que es lo que se les
pide (y, desde P1, para que `resolver_payload` los resuelva si alguno
fuera `origen: manifiesto`; este smoke solo trae `origen: repo`, igual
que `CALC-SMOKE-0001`).
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
SCRIPT_LEGACY = RAIZ / "forense" / "prereg-duelo-v2" / "agregado_v1_3.py"

# `agregado-v1_3-resultado.json` -> el punto y los dos extremos del IC de las
# comparaciones que el procedimiento v1.2 declara. Se toman POR NOMBRE, no
# por posicion: un cambio de orden en el JSON no debe mover un RESULT.
EXTRAE = {
    "RESULT-SMOKE-PRINCIPAL-PUNTO": ("comparacion_principal_pareada", "punto"),
    "RESULT-SMOKE-PRINCIPAL-IC-LO": ("comparacion_principal_pareada", "ic_lo"),
    "RESULT-SMOKE-PRINCIPAL-IC-HI": ("comparacion_principal_pareada", "ic_hi"),
    "RESULT-SMOKE-SECUNDARIA-PUNTO": ("comparacion_secundaria_l_corpus_vs_m", "punto"),
    "RESULT-SMOKE-SECUNDARIA-IC-LO": ("comparacion_secundaria_l_corpus_vs_m", "ic_lo"),
    "RESULT-SMOKE-SECUNDARIA-IC-HI": ("comparacion_secundaria_l_corpus_vs_m", "ic_hi"),
}


def _carga_legacy():
    spec = importlib.util.spec_from_file_location(
        "agregado_v1_3_smoke_0002", SCRIPT_LEGACY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def medir(inputs, contrato):
    """`medir(inputs, contrato) -> {"RESULT-…": valor}` (plan v2.0 §4, B-1;
    contrato normalizado por `contrato_ejecutable()`, ACTO GEN2-E3-1 P2)."""
    resultado = _carga_legacy().main()
    fuera = {}
    for rid, (bloque, campo) in EXTRAE.items():
        sub = resultado.get(bloque)
        if not isinstance(sub, dict) or campo not in sub:
            raise KeyError(
                f"{rid}: el agregado v1_3 no trae `{bloque}.{campo}` -- el "
                f"medidor NO inventa un valor por defecto")
        fuera[rid] = sub[campo]
    # Controles de forma, no de valor: si el universo del duelo cambia, esto
    # deja de ser un replay del mismo calculo y hay que decirlo, no callarlo.
    fuera["RESULT-SMOKE-N-CELDAS-UNIVERSO"] = len(resultado["fuente_M_por_celda"])
    fuera["RESULT-SMOKE-REPLICAS"] = resultado["parametros_sellados"]["replicas"]
    fuera["RESULT-SMOKE-SEED"] = resultado["parametros_sellados"]["seed"]
    return fuera
