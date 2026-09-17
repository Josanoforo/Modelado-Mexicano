#!/usr/bin/env python3
"""Regresiones de la resolucion condicionada F-2 para RES-0005."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
import sys


RAIZ = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "relevo_usos_f2_bajo_prueba", RAIZ / "tools" / "relevo_usos.py")
R = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = R
spec.loader.exec_module(R)


def _insumos():
    corridas = R._lee_tsv(R.C0 / "corridas.tsv")
    oferta = {f["spec_id"]: f for f in corridas
              if f["origen"] == "OFERTA" and f["spec_id"] == R.F2_CALC}
    resultados = R._lee_tsv(R.C0 / "resultados.tsv")
    punto = next(
        f for f in resultados
        if f["origen"] == "OFERTA"
        and f["corrida_id"] == R.F2_CORRIDA
        and f["resultado_id"] == R.F2_RESULT)
    return {
        "res": R.F2_RES,
        "consumidor": R.F2_CONSUMIDOR,
        "ramas": [R.F2_HISTORICO],
        "oferta": oferta,
        "ejecucion": R._evidencia_ejecucion_f3(R.F2_CALC),
        "punto": punto,
        "resultados_sellados": R._resultados_sellados(R.F2_CALC),
        "uso": R.corrida0._ids_corrida0_declarados()[R.F2_CONSUMIDOR],
        "spec": R._specs()[R.F2_CALC],
        "firma_acreditada": R._firma_f2_acreditada(),
    }


def _resuelve(**cambios):
    insumos = copy.deepcopy(_insumos())
    insumos.update(cambios)
    return R._resuelve_f2_encuci(**insumos)


def test_pareja_real_valor_vigente_y_firma_hacen_efectiva_f2():
    filas = R.deriva()[0]
    fila = next(f for f in filas if f["resultado_id"] == R.F2_RES)
    assert fila["veredicto"] == "YA-ADOPTADO"
    assert fila["resolucion_vigente"] == "SUPERADO-POR-F2"
    assert fila["veredicto_sellado"] == "NO-ADOPTABLE-POR-DISCREPANCIA"
    assert fila["veredicto_sellado_ref"] == (
        "CALC-ENCUCI-0001/RESULT-ENCUCI-A-ADOPCION-P3")
    assert fila["result_gen2_candidato"] == R.F2_RESULT
    assert fila["valor_gen2"] == "0.12600561008991654"
    assert fila["valor_legacy"] == "0.126006"
    assert "grano del consumidor = 6 decimales" in fila["razon"]
    assert all(not f["resolucion_vigente"] for f in filas
               if f["resultado_id"] != R.F2_RES)


def test_delta_menor_a_1e_6_no_basta_si_discrepa_al_grano():
    uso = copy.deepcopy(_insumos()["uso"])
    uso["valor"] = 0.126005
    resultado = _resuelve(uso=uso)
    assert resultado["delta"] < 1e-6
    assert not resultado["aplica"]
    assert resultado["resolucion"] == "CITA-PENDIENTE-DE-RETIRO-POR-F2"
    assert resultado["modo"] == "grano del consumidor = 6 decimales"


def test_sello_identidad_firma_o_grano_ausentes_no_acreditan():
    ejecucion = copy.deepcopy(_insumos()["ejecucion"])
    ejecucion["__sello_archivos__"] = "AUSENTE"
    assert _resuelve(ejecucion=ejecucion)["causa"].startswith(
        "ARTEFACTOS-NO-SELLADOS")

    oferta = copy.deepcopy(_insumos()["oferta"])
    oferta[R.F2_CALC]["corrida_id"] = "OTRA-CORRIDA"
    assert _resuelve(oferta=oferta)["causa"].startswith(
        "IDENTIDAD-SELLADA-DISTINTA")

    assert _resuelve(firma_acreditada=False)["causa"] == (
        "FIRMA-F1-F2-AUSENTE-O-INVALIDA")

    uso = copy.deepcopy(_insumos()["uso"])
    uso["valor"] = "0.126006"
    assert _resuelve(uso=uso)["causa"].startswith(
        "F1-GRANO-NO-ACREDITADO")


def test_cambio_vigente_reevalua_una_resolucion_anterior():
    assert _resuelve()["resolucion"] == "SUPERADO-POR-F2"
    original = R.corrida0._ids_corrida0_declarados

    def declarado_con_cambio():
        declarado = copy.deepcopy(original())
        declarado[R.F2_CONSUMIDOR]["valor"] = 0.126005
        return declarado

    R.corrida0._ids_corrida0_declarados = declarado_con_cambio
    try:
        fila = next(f for f in R.deriva()[0]
                    if f["resultado_id"] == R.F2_RES)
    finally:
        R.corrida0._ids_corrida0_declarados = original
    assert fila["valor_legacy"] == "0.126006"  # copia historica, no gobierna
    assert fila["veredicto"] == "CITA-PENDIENTE-DE-RETIRO-POR-F2"
    assert fila["resolucion_vigente"] == (
        "CITA-PENDIENTE-DE-RETIRO-POR-F2")
    assert "valor vigente del consumidor=0.126005" in fila["razon"]


def test_otro_consumidor_result_o_veredicto_no_heredan_f2():
    assert _resuelve(consumidor="otro:consumidor") is None
    distinto = [(R.F2_CALC, "RESULT-OTRO", R.F2_HISTORICO[2])]
    resultado = _resuelve(ramas=distinto)
    assert not resultado["aplica"]
    assert resultado["causa"] == (
        "CALC-RESULT-VEREDICTO-HISTORICO-DISTINTO")


def test_f3_de_res_0035_conserva_su_salida():
    fila = next(f for f in R.deriva()[0] if f["resultado_id"] == "RES-0035")
    assert fila["veredicto_sellado"] == "LISTADO-PARA-MESA-REPRODUCE"
    assert fila["veredicto_sellado_ref"] == (
        "CALC-B-0001/RESULT-B-ADOPCION-P3=SUPERADO->"
        "CALC-ENIGH-0001/RESULT-ENIGH-A-ADOPCION")
    assert fila["resolucion_vigente"] == ""


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for prueba in pruebas:
        prueba()
    print(f"tests/test_relevo_encuci_f2.py · {len(pruebas)} casos · todos ok")
