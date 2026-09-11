#!/usr/bin/env python3
"""Sello corrida0 del cálculo prospectivo GEN2-F5-COMPLETA."""
from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CALCULADOR = ROOT / "tools/calcula_f5_completa.py"


def _cargar_calculador():
    spec = importlib.util.spec_from_file_location("calcula_f5_completa_calc_0002", CALCULADOR)
    modulo = importlib.util.module_from_spec(spec)
    assert spec.loader
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def medir(inputs: dict, contrato: dict) -> dict:
    modulo = _cargar_calculador()
    resultado, filas = modulo.calcular()
    if len(filas) != 224:
        raise RuntimeError(f"se esperaban 224 posiciones; hay {len(filas)}")
    estados = Counter(f["estado"] for f in filas)
    if estados["PENDIENTE"] or estados["ERROR_IDENTIDAD"]:
        raise RuntimeError(f"capturas incompletas o con identidad rota: {dict(estados)}")

    salida = {
        "RESULT-F5C-POSICIONES": len(filas),
        "RESULT-F5C-VALIDAS": estados["VALIDA"],
        "RESULT-F5C-ABSTENCIONES": estados["ABSTENCION"],
        "RESULT-F5C-MALFORMADAS": estados["MALFORMADA"],
        "RESULT-F5C-ERRORES-TECNICOS": estados["ERROR_TECNICO"],
        "RESULT-F5C-ERRORES-IDENTIDAD": estados["ERROR_IDENTIDAD"],
        "RESULT-F5C-U3-N": resultado["u3_n"],
        "RESULT-F5C-U3-IDS": ",".join(resultado["u3_ids"]),
        "RESULT-F5C-COBERTURA-L-SOLO": resultado["cobertura_celdas_con_punto"]["L_SOLO"],
        "RESULT-F5C-COBERTURA-L-CORPUS": resultado["cobertura_celdas_con_punto"]["L_CORPUS"],
        "RESULT-F5C-COBERTURA-M": resultado["cobertura_celdas_con_punto"]["M"],
        "RESULT-F5C-MAE-L-SOLO-PP": resultado["mae_pp"]["L_SOLO"],
        "RESULT-F5C-MAE-L-CORPUS-PP": resultado["mae_pp"]["L_CORPUS"],
        "RESULT-F5C-MAE-M-PP": resultado["mae_pp"]["M"],
        "RESULT-F5C-VEREDICTO-GLOBAL": resultado["veredicto_global"],
    }
    nombres = {
        "L_CORPUS_vs_L_SOLO": "LCORPUS-LSOLO",
        "M_vs_L_SOLO": "M-LSOLO",
        "M_vs_L_CORPUS": "M-LCORPUS",
    }
    for clave, corto in nombres.items():
        comp = resultado["comparaciones"][clave]
        prefijo = f"RESULT-F5C-DELTA-{corto}"
        salida[f"{prefijo}-PUNTO-PP"] = comp["delta_mae_pp"]
        salida[f"{prefijo}-IC95-LO-PP"] = comp["ic95_lo"]
        salida[f"{prefijo}-IC95-HI-PP"] = comp["ic95_hi"]
        salida[f"{prefijo}-VEREDICTO"] = comp["veredicto"]
    return salida
