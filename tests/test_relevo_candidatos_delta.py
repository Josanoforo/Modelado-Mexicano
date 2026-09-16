#!/usr/bin/env python3
"""Regresiones materiales del envoltorio de candidatos delta."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "relevo_candidatos_delta_bajo_prueba",
    RAIZ / "tools" / "relevo_candidatos_delta.py",
)
R = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = R
spec.loader.exec_module(R)


def _par(*, delta=0.0, comparabilidad="DEMOSTRADA", a=0.5, b=0.5):
    return {
        "comparabilidad": {"estado": comparabilidad},
        "diferencia": {"delta": delta},
        "referencias": {"a": {"valor": a}, "b": {"valor": b}},
    }


def test_contrato_cubre_todo_candidato_vigente_exactamente_una_vez():
    _universo, seleccion, _contadores = R.seleccion_actual()
    contrato, familias = R.construye_contrato(seleccion)
    esperados = {f["resultado_id"] for f in seleccion}
    observados = [R._slot_del_par(p) for p in contrato["pares"]]
    assert set(observados) == esperados
    assert len(observados) == len(set(observados))
    assert set(familias) == esperados


def test_p_medida_es_bin_2_aunque_delta_sea_cero():
    fila = {"resultado_id": "RES-9991", "tipo_uso": "conducta_p_medido"}
    assert R.clasifica(fila, _par(delta=0.0))[0] == "2"


def test_incompatibilidad_es_bin_3_sin_delta_interpretado():
    fila = {"resultado_id": "RES-0028", "tipo_uso": "conducta_p_derivado"}
    assert R.clasifica(
        fila, _par(delta=None, comparabilidad="INCOMPATIBILIDAD"))[0] == "3"


def test_via_sin_ic_ni_dependencia_es_bin_3_y_no_bin_1_por_redondeo():
    fila = {"resultado_id": "RES-0055", "tipo_uso": "conducta_p_asignado"}
    assert R.clasifica(fila, _par(delta=0.0))[0] == "3"


def test_via_que_alimenta_agregado_es_bin_2():
    fila = {"resultado_id": "RES-0053", "tipo_uso": "conducta_p_asignado"}
    assert R.clasifica(fila, _par(delta=0.0))[0] == "2"


def test_horizonte_es_bin_2_por_ser_insumo_de_agregado_aunque_cumpla_ic():
    fila = {"resultado_id": "RES-0066", "tipo_uso": "conducta_p_asignado"}
    assert R.clasifica(
        fila, _par(delta=5.55e-17, a=0.367218, b=0.36721800000000004))[0] == "2"


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallos = []
    for prueba in pruebas:
        try:
            prueba()
        except Exception as exc:
            fallos.append(f"{prueba.__name__}: {type(exc).__name__}: {exc}")
    print(f"tests/test_relevo_candidatos_delta.py · {len(pruebas)} casos · "
          f"{len(pruebas)-len(fallos)} ok · {len(fallos)} FALLOS")
    for fallo in fallos:
        print("  FAIL", fallo)
    raise SystemExit(1 if fallos else 0)
