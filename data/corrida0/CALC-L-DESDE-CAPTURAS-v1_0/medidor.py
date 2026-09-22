#!/usr/bin/env python3
"""Sello corrida0 de GEN2-L-DESDE-CAPTURAS-1 (P2/P3/P4 del encargo)."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CALCULADOR = ROOT / "tools/calcula_l_desde_capturas.py"


def _cargar_calculador():
    spec = importlib.util.spec_from_file_location("calcula_l_desde_capturas_calc", CALCULADOR)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def medir(inputs: dict, contrato: dict) -> dict:
    modulo = _cargar_calculador()
    resultado = modulo.calcular()
    if resultado["n_posiciones"] != 224:
        raise RuntimeError(f"se esperaban 224 posiciones; hay {resultado['n_posiciones']}")
    if resultado["n_slots"] != 28:
        raise RuntimeError(f"se esperaban 28 slots (14 celdas x 2 variantes); hay {resultado['n_slots']}")
    if resultado["errores_identidad"]:
        raise RuntimeError(f"capturas con identidad rota: {resultado['errores_identidad']}")

    return {
        "RESULT-LDESC-N-POSICIONES": resultado["n_posiciones"],
        "RESULT-LDESC-N-SLOTS": resultado["n_slots"],
        "RESULT-LDESC-N-SLOTS-CON-MEDIANA": resultado["n_celdas_con_mediana"],
        "RESULT-LDESC-N-SLOTS-SIN-MEDIANA": resultado["n_celdas_sin_mediana"],
        "RESULT-LDESC-TABLA-JSON": json.dumps(resultado["tabla_l_por_celda_variante"],
                                               ensure_ascii=False, sort_keys=True),
        "RESULT-LDESC-DIFERENCIAS-VS-GEN1-JSON": json.dumps(resultado["diferencias_vs_gen1"],
                                                              ensure_ascii=False, sort_keys=True),
    }
