#!/usr/bin/env python3
"""Regresion de la decision acotada NC-0254 sobre RES-0043/0044."""

import importlib.util
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "relevo_usos_nc0254_bajo_prueba", RAIZ / "tools" / "relevo_usos.py")
R = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R)


def test_res0043_0044_quedan_sin_candidato_con_sucesor_enadid():
    filas = {f["resultado_id"]: f for f in R.deriva()[0]}
    for resultado_id in ("RES-0043", "RES-0044"):
        fila = filas[resultado_id]
        assert fila["veredicto"] == "SIN-CANDIDATO"
        assert fila["resolucion_vigente"] == "DECISION-NC-0254"
        assert fila["sucesor"] == "GEN2-ENADID-2023-SITUACION-CONYUGAL"
        assert fila["veredicto_sellado_ref"].startswith("CALC-EDER-0003/")
        assert "tipo de primera union" in fila["razon"]
