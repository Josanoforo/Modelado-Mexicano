#!/usr/bin/env python3
"""Intento real de `ejecutar_scoring` bajo el contrato F1 (`ACTO MAESTRA30-E9`).

Construye el documento mas honesto posible con lo que el pre-registro
efectivamente fija (corredores activos, comparacion principal, e_id) y
deja `delta`/`nivel_ic`/`seed` fuera a proposito -- ninguno tiene cita en
`forense/prereg-duelo-v2/` ni en `canon/` como escalar unico de corrida
(ver `procedimiento-scoring-v1_0.md` S3). `mediciones` va vacio por celda:
sin `B` (`SIN_BASELINE` en las 15, `corridas-R/_corredor-B.json`) no hay
una `skill` normalizada legitima que poblar para ningun corredor (S4).

Uso::

    python3 forense/prereg-duelo-v2/corridas-M/intento_scoring_e9.py

Escribe `_intento-scoring-v1_1.json` en el mismo directorio, determinista.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
RUTA_SCORING = RAIZ / "forense" / "prereg-duelo-v2" / "scoring-adv1-m3.py"

CELDAS_15 = [
    "CIV-08", "DIN-03", "DIN-05", "DIN-07", "DIN-11", "DOC-06", "EMP-02",
    "EMP-04", "EMP-05", "SFT-04", "SFT-06", "TIC-01", "TIC-06", "TIC-08",
    "TIC-12",
]


def _cargar_scoring():
    spec = importlib.util.spec_from_file_location("scoring_adv1_m3", RUTA_SCORING)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def construir_documento() -> dict:
    configuracion = {
        "corredores_activos": [
            {"id": "L_SOLO", "familia": "L", "variante": "solo"},
            {"id": "M", "familia": "M", "variante": "principal"},
        ],
        "comparaciones_l_m": [
            {"id": "L_SOLO_vs_M", "l_id": "L_SOLO", "m_id": "M"},
        ],
        "comparacion_principal_id": "L_SOLO_vs_M",
        "e_id": None,
        # delta / nivel_ic / seed deliberadamente ausentes -- ver docstring.
    }
    celdas = [{"id_celda": c, "estado": "EVALUABLE", "mediciones": {}} for c in CELDAS_15]
    return {"configuracion": configuracion, "celdas": celdas}


def intentar(documento: dict, scoring) -> dict:
    try:
        resultado = scoring.ejecutar_scoring(documento)
        return {"resultado": "EXITO", "salida": resultado}
    except scoring.ErrorScoring as error:
        return {"resultado": "ErrorScoring", "codigo": error.codigo, "mensaje": error.mensaje}


def main() -> int:
    scoring = _cargar_scoring()
    documento = construir_documento()
    intento = intentar(documento, scoring)
    print(json.dumps(intento, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
