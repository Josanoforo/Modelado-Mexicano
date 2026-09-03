#!/usr/bin/env python3
"""Paso adicional de d1 (`FP-249`) para `DIN-M-01` — dos `z`, un veredicto cada una.

`ENMIENDA 5` (`forense/encargos/cola/2026-09-01-MAESTRA34-N3-AGREGA-2.md`)
implementa la reserva de la firma de mesa `d1` sobre `FP-249`, verbatim en
`forense/prereg-duelo-v2/exclusiones-v1_2.md:36-42`: una `R` con
`DISEÑO-APROXIMADO` sí puntúa, pero el scoreboard debe reportar `z` con las
DOS `EE` (`EE_R`, la aproximada, y `EE_R_sin_diseno`) y declarar si el
veredicto de banda cambia entre ambas. Si cambia, la celda es
AMBIGUA-POR-DISEÑO y no cuenta como puntuada; si no cambia, cuenta.

Este script **no edita** `tools/score_marco_m.py` (que solo lee `EE_R`,
líneas 80-87) ni `procedimiento-scoring-v1_1.md` ni `agregado_v1_1.py` —
es un paso aparte, acotado a la única celda que trae `EE_R_sin_diseno`
(`corridas-R/DIN-M-01.json`). Reutiliza la misma unidad de medición sellada
(`z = dif/EE(R)`, `procedimiento-scoring-v1_1.md` §1) y el mismo criterio de
banda (`-0.5 <= z <= 0.5`, `delta = 0.5`) que `agregado_v1_1.py` ya aplica a
las demás celdas, adaptado a `dif_pareada_z = z_L - z_M` (§3 del
procedimiento) para dar UN veredicto por celda, no uno por corredor.

Uso::

    python3 forense/prereg-duelo-v2/din_m_01_doble_ee.py [--json salida.json]
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[2]
PREREG = RAIZ / "forense" / "prereg-duelo-v2"
CORRIDAS_R = PREREG / "corridas-R"
CORRIDAS_M = PREREG / "corridas-M"
L_EXTRAIDO_V1_2 = PREREG / "L-extraido-v1_2.tsv"

ID_CELDA = "DIN-M-01"
DELTA = 0.5


def _leer_r() -> dict[str, Any]:
    return json.loads((CORRIDAS_R / f"{ID_CELDA}.json").read_text(encoding="utf-8"))


def _leer_m() -> dict[str, Any]:
    return json.loads((CORRIDAS_M / f"M-{ID_CELDA}__v1_2.json").read_text(encoding="utf-8"))


def _leer_l_solo() -> float:
    """Media de `valor` sobre las réplicas EXTRAIBLE de (`DIN-M-01`, `L-solo`).

    Misma regla de colapso que `agregado_v1_1.py:_leer_l_variante` (media de
    las réplicas con valor disponible), leída aquí sobre
    `L-extraido-v1_2.tsv` en vez de los JSON individuales de `corridas-L/`
    porque ese TSV ya es el colapso plano de esas réplicas para v1.2.
    """
    valores: list[float] = []
    with L_EXTRAIDO_V1_2.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter="\t"):
            if fila["id_celda"] != ID_CELDA or fila["variante"] != "L-solo":
                continue
            if fila["estado"] != "EXTRAIBLE":
                continue
            valores.append(float(fila["valor"]))
    if not valores:
        raise ValueError(f"sin réplicas EXTRAIBLE de L-solo para {ID_CELDA}")
    return statistics.fmean(valores)


def _banda(z: float) -> str:
    return "DENTRO-DE-BANDA" if -DELTA <= z <= DELTA else "FUERA-DE-BANDA"


def calcular() -> dict[str, Any]:
    r_datos = _leer_r()
    m_datos = _leer_m()
    r = r_datos["R"]
    ee_aproximada = r_datos["EE_R"]
    ee_sin_diseno = r_datos["EE_R_sin_diseno"]
    m = m_datos["valor_punto"]
    l_solo = _leer_l_solo()

    resultados = {}
    for etiqueta, ee in (("aproximada", ee_aproximada), ("sin_diseno", ee_sin_diseno)):
        z_l = (l_solo - r) / ee
        z_m = (m - r) / ee
        dif_pareada_z = z_l - z_m
        resultados[etiqueta] = {
            "EE_usada": ee,
            "z_L": z_l,
            "z_M": z_m,
            "dif_pareada_z": dif_pareada_z,
            "veredicto_banda": _banda(dif_pareada_z),
        }

    veredicto_cambia = (
        resultados["aproximada"]["veredicto_banda"]
        != resultados["sin_diseno"]["veredicto_banda"]
    )

    return {
        "id_celda": ID_CELDA,
        "firma_mesa": "d1/FP-249 (mesa, 2/sep/2026), implementado por ENMIENDA 5",
        "insumos": {"R": r, "M": m, "L_solo": l_solo},
        "resultados": resultados,
        "veredicto_cambia_entre_EE": veredicto_cambia,
        "cuenta_como_puntuada": not veredicto_cambia,
        "estado_celda": "AMBIGUA-POR-DISEÑO" if veredicto_cambia else "PUNTUADA",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", dest="salida_json", help="ruta de salida (default: stdout)")
    argumentos = parser.parse_args(argv)

    documento = calcular()
    salida = json.dumps(documento, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if argumentos.salida_json:
        Path(argumentos.salida_json).write_text(salida, encoding="utf-8")
    else:
        sys.stdout.write(salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
