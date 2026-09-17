#!/usr/bin/env python3
"""Regresiones de la adjudicacion acotada F-3 para RES-0035."""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "relevo_usos_f3_bajo_prueba", RAIZ / "tools" / "relevo_usos.py")
R = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = R
spec.loader.exec_module(R)


def _insumos():
    oferta = {
        calc: {
            "corrida_id": corrida,
            "spec_id": calc,
            "estado": "SELLADA",
            "sello": "COINCIDE",
            "cuenta_gen2": "SI",
            "fecha": fecha,
            "codigo_commit": commit,
            "script_path": f"data/corrida0/{calc}/medidor.py",
            "script_blob_sha256": f"script-{calc}",
            "spec_yaml_sha256": R.F3_SPEC_SHA256[calc],
        }
        for calc, corrida, fecha, commit in (
            ("CALC-B-0001", R.F3_CORRIDAS["CALC-B-0001"],
             "2026-09-09T02:01:48Z", "b" * 40),
            ("CALC-ENIGH-0001", R.F3_CORRIDAS["CALC-ENIGH-0001"],
             "2026-09-15T16:23:22Z", "e" * 40),
        )
    }
    evidencias = {}
    for calc, fila in oferta.items():
        evidencias[calc] = {
            "corrida_id": fila["corrida_id"],
            "spec_id": calc,
            "fecha": fila["fecha"],
            "git_commit": fila["codigo_commit"],
            "script_path": fila["script_path"],
            "script_blob_sha256": fila["script_blob_sha256"],
            "spec_yaml_sha256": fila["spec_yaml_sha256"],
            "exit_code": 0,
            "error": None,
            "__sello_archivos__": "COINCIDE",
        }
    return oferta, evidencias


def _resuelve(ramas=None):
    oferta, evidencias = _insumos()
    return R._resuelve_f3_remesas(
        R.F3_RES, R.F3_CONSUMIDOR,
        ramas or [R.F3_ANTERIOR, R.F3_VIGENTE], oferta, evidencias,
        True, "grano del consumidor = 6 decimales")


def test_pareja_real_aplica_f3_y_conserva_ambas_referencias():
    fila = next(f for f in R.deriva()[0] if f["resultado_id"] == "RES-0035")
    assert fila["veredicto_sellado"] == "LISTADO-PARA-MESA-REPRODUCE"
    assert fila["veredicto_sellado_ref"] == (
        "CALC-B-0001/RESULT-B-ADOPCION-P3=SUPERADO->"
        "CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION")
    assert fila["result_gen2_candidato"] == "RESULT-B-ENIGH-2022-P"
    assert fila["valor_gen2"] == "0.04569409956405095"
    assert fila["valor_legacy"] == "0.045694"


def test_sello_ausente_fecha_ilegible_y_pareja_distinta_no_aplican():
    oferta, evidencias = _insumos()
    oferta["CALC-ENIGH-0001"]["sello"] = "AUSENTE"
    assert not R._resuelve_f3_remesas(
        R.F3_RES, R.F3_CONSUMIDOR, [R.F3_ANTERIOR, R.F3_VIGENTE],
        oferta, evidencias, True,
        "grano del consumidor = 6 decimales")["aplica"]

    oferta, evidencias = _insumos()
    evidencias["CALC-ENIGH-0001"]["fecha"] = "NO-ACREDITABLE"
    oferta["CALC-ENIGH-0001"]["fecha"] = "NO-ACREDITABLE"
    assert not R._resuelve_f3_remesas(
        R.F3_RES, R.F3_CONSUMIDOR, [R.F3_ANTERIOR, R.F3_VIGENTE],
        oferta, evidencias, True,
        "grano del consumidor = 6 decimales")["aplica"]

    distinto = [("CALC-X", "RESULT-X", "LISTADO-PARA-MESA-REPRODUCE"),
                R.F3_ANTERIOR]
    assert not _resuelve(ramas=distinto)["aplica"]


def test_misma_fecha_no_se_resuelve_por_nombre():
    oferta, evidencias = _insumos()
    fecha = oferta["CALC-B-0001"]["fecha"]
    oferta["CALC-ENIGH-0001"]["fecha"] = fecha
    evidencias["CALC-ENIGH-0001"]["fecha"] = fecha
    resultado = R._resuelve_f3_remesas(
        R.F3_RES, R.F3_CONSUMIDOR, [R.F3_ANTERIOR, R.F3_VIGENTE],
        oferta, evidencias, True, "grano del consumidor = 6 decimales")
    assert not resultado["aplica"]
    assert resultado["causa"] == "ORDEN-SELLADO-NO-ACREDITADO"


def test_f3_no_alcanza_otros_consumidores_ni_res_0047_0049():
    oferta, evidencias = _insumos()
    assert R._resuelve_f3_remesas(
        "RES-9999", "otro:consumidor", [R.F3_ANTERIOR, R.F3_VIGENTE],
        oferta, evidencias, True, "grano del consumidor = 6 decimales") is None
    filas = {f["resultado_id"]: f for f in R.deriva()[0]}
    for res in ("RES-0047", "RES-0049"):
        assert filas[res]["veredicto"] == "CONFLICTO-ENTRE-CANALES"


def test_grano_de_adopcion_no_afloja_tolerancia_de_reproduccion():
    punto, publicado = 0.04569409956405095, 0.045694
    decl, tol = {"tipo": "proporcion"}, {"abs": 1e-10}
    reproduce, _ = R.corrida0._compara_result(punto, publicado, decl, tol)
    adopta, _, modo = R.corrida0._compara_adopcion(
        punto, publicado, decl, tol)
    assert reproduce is False
    assert adopta is True
    assert modo == "grano del consumidor = 6 decimales"


def test_bytes_de_los_calc_sellados_permanecen_intactos():
    esperados = {
        "CALC-B-0001/spec.yaml":
            "7feed075d55bf795f921bc7bd0d75ac8bffa60b205822cf1333364a2c67efe16",
        "CALC-B-0001/resultados.json":
            "87e20e5aa2923fcc4b206734fa13ec321d3b036d61edd48eb0efd5bd369f263d",
        "CALC-ENIGH-0001/spec.yaml":
            "1555d052cf0c9ebbf91d1080c6be976b64191fb932dfa04083d7804bc0ce4566",
        "CALC-ENIGH-0001/resultados.json":
            "26394edc6ae16808de8efa16c1be662cbe920fc9485863d0a7ababd4d9d23c34",
    }
    for rel, esperado in esperados.items():
        obtenido = hashlib.sha256((R.C0 / rel).read_bytes()).hexdigest()
        assert obtenido == esperado


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for prueba in pruebas:
        prueba()
    print(f"tests/test_relevo_remesas_f3.py · {len(pruebas)} casos · todos ok")
