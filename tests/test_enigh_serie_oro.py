#!/usr/bin/env python3
"""ORO de `ACTO GEN2-ENIGH2024-SERIE-Y-COMMIT-1`, P1.

Prueba que el código YA CONGELADO de los tres CALC nuevos de la serie
(`CALC-ENIGH{2016,2018,2020}-{PERFIL-ESTRUCTURAL,INTENSIDAD-REMESAS,
REMESAS-CONTEXTO}-0001`) -- el mismo `medidor.py` que sella cada ola nueva,
sin copiar ni reescribir su lógica -- reproduce byte a byte (JSON canónica,
sha256, y para INTENSIDAD-REMESAS también el bootstrap completo bit a bit)
los tres `resultados.json` ya sellados de ENIGH 2022
(`CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003`,
`CALC-ENIGH2022-INTENSIDAD-REMESAS-0001`,
`CALC-ENIGH2022-REMESAS-CONTEXTO-0001`) cuando se apunta, por los mismos
tres atributos de módulo que cada `medidor.py` ya expone (`ZIP_ID`,
`MIEMBROS`/`MIEMBRO`, y para PERFIL además `FUENTES`), al zip de 2022.

Esto NO es una segunda implementación paralela que pudiera divergir: es el
código congelado de 2016 (cualquiera de los tres bastaría -- las tres olas
comparten exactamente la misma función `calcular`/`medir`, solo cambian las
rutas de módulo) reconfigurado en caliente para leer 2022 en vez de 2016. Si
alguien edita el medidor congelado de una ola después de este commit, este
test lo detecta -- no reconstruye una tolerancia, exige coincidencia exacta.

Se salta con `SALTADO-SIN-PAYLOAD` (A.13: 0 archivos examinados) si
`data/raw/enigh2022_nc_csv.zip` no está montado -- nunca declara ROJO por un
corpus ausente.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIP_2022 = os.path.join(RAIZ, "data", "raw", "enigh2022_nc_csv.zip")

MIEMBROS_2022 = {
    "poblacion": "conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh2022_ns.csv",
    "concentrado": "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv",
    "hogares": "conjunto_de_datos_hogares_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_hogares_enigh2022_ns.csv",
}
MIEMBRO_CONCENTRADO_2022 = (
    "conjunto_de_datos_concentradohogar_enigh2022_ns/conjunto_de_datos/"
    "conjunto_de_datos_concentradohogar_enigh2022_ns.csv"
)
FUENTES_2022 = {
    "segsoc": "ENIGH 2022 Descripción de la base, p. 75",
    "tramo_edad": "ENIGH 2022 Descripción de la base, p. 65; corte operativo 18–96",
    "tam_loc": "ENIGH 2022 Descripción de la base, pp. 45 y 186",
    "est_socio": "ENIGH 2022 Descripción de la base, pp. 46 y 186",
    "conex_inte": "ENIGH 2022 Descripción de la base, p. 54",
    "celular": "ENIGH 2022 Descripción de la base, p. 54",
}
CONTROLES_2022 = {
    "prevalencia": 0.04569409956405095, "remesas_media": 14455.429835947132,
    "remesas_mediana": 8310.32, "participacion_media": 0.30492285849567624,
    "participacion_agregada": 0.2746879872958264, "ge50": 0.24146058093220438,
}


def _carga(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _resultados_sellados(calc_id):
    ruta = os.path.join(RAIZ, "data", "corrida0", calc_id, "resultados.json")
    with open(ruta, encoding="utf-8") as fh:
        return json.load(fh)["resultados"]


def _payload_montado():
    return os.path.isfile(ZIP_2022)


@unittest.skipUnless(_payload_montado(), "SALTADO-SIN-PAYLOAD: data/raw/enigh2022_nc_csv.zip no montado (0 archivos examinados)")
class OroPerfilEstructural(unittest.TestCase):
    """Usa el medidor congelado de 2016 -- comparte código con 2018/2020."""

    def test_reproduce_2022_byte_a_byte(self):
        m = _carga(os.path.join(RAIZ, "data/corrida0/CALC-ENIGH2016-PERFIL-ESTRUCTURAL-0001/medidor.py"))
        m.ZIP_ID = "enigh2022_nc_csv"
        m.MIEMBROS = MIEMBROS_2022
        m.FUENTES = FUENTES_2022
        inputs = {"enigh2022_nc_csv": {"ruta_absoluta": ZIP_2022}}
        contrato = {"parametros": {"bootstrap_replicas": 1000}, "seed": {"valor": 20260919}}
        r = m.medir(inputs, contrato)
        sellado = _resultados_sellados("CALC-ENIGH2022-PERFIL-ESTRUCTURAL-0003")
        for sufijo in ("P1-MARGINALES-SHA256", "P2-CONJUNTA-SHA256", "P2-MARGINALES-COMPLETOS-SHA256"):
            self.assertEqual(r[f"RESULT-ENIGH16-PERFIL-{sufijo}"], sellado[f"RESULT-ENIGH22-PERFIL-{sufijo}"], sufijo)
        self.assertEqual(r["RESULT-ENIGH16-PERFIL-UNIVERSO-N"], sellado["RESULT-ENIGH22-PERFIL-UNIVERSO-N"])
        self.assertEqual(r["RESULT-ENIGH16-PERFIL-UNIVERSO-MASA"], sellado["RESULT-ENIGH22-PERFIL-UNIVERSO-MASA"])
        self.assertEqual(r["RESULT-ENIGH16-PERFIL-CONTROL-MAX-DELTA-PUNTOS"], sellado["RESULT-ENIGH22-PERFIL-CONTROL-MAX-DELTA-PUNTOS"])


@unittest.skipUnless(_payload_montado(), "SALTADO-SIN-PAYLOAD: data/raw/enigh2022_nc_csv.zip no montado (0 archivos examinados)")
class OroIntensidadRemesas(unittest.TestCase):

    def test_reproduce_2022_bit_a_bit(self):
        m = _carga(os.path.join(RAIZ, "data/corrida0/CALC-ENIGH2016-INTENSIDAD-REMESAS-0001/medidor.py"))
        m.ZIP_ID = "enigh2022_nc_csv"
        m.MIEMBRO = MIEMBRO_CONCENTRADO_2022
        inputs = {"enigh2022_nc_csv": {"ruta_absoluta": ZIP_2022}}
        contrato = {"parametros": {
            "bootstrap_replicas": 2000, "tolerancia_componente_pesos": 0.01,
            "prevalencia_padre": 0.04569409956405095, "tolerancia_prevalencia": 1e-10,
        }, "seed": {"valor": 20260916}}
        r = m.medir(inputs, contrato)
        sellado = _resultados_sellados("CALC-ENIGH2022-INTENSIDAD-REMESAS-0001")
        for sufijo in (
            "ESTADO", "N-FILAS", "UNIVERSO-VALIDO-N", "RECEPTORES-N", "RECEPTORES-MASA",
            "PREVALENCIA", "REMESAS-MEDIA", "REMESAS-MEDIANA",
            "PARTICIPACION-MEDIA-HOGAR", "PARTICIPACION-AGREGADA", "PARTICIPACION-GE50",
            "PARTICIPACION-MEDIA-HOGAR-IC-LO", "PARTICIPACION-MEDIA-HOGAR-IC-HI",
            "PARTICIPACION-AGREGADA-IC-LO", "PARTICIPACION-AGREGADA-IC-HI",
            "PARTICIPACION-GE50-IC-LO", "PARTICIPACION-GE50-IC-HI",
        ):
            self.assertEqual(r[f"RESULT-ENIGH16-REMINT-{sufijo}"], sellado[f"RESULT-ENIGH22-REMINT-{sufijo}"], sufijo)


@unittest.skipUnless(_payload_montado(), "SALTADO-SIN-PAYLOAD: data/raw/enigh2022_nc_csv.zip no montado (0 archivos examinados)")
class OroRemesasContexto(unittest.TestCase):

    def test_reproduce_2022_exacto(self):
        m = _carga(os.path.join(RAIZ, "data/corrida0/CALC-ENIGH2016-REMESAS-CONTEXTO-0001/medidor.py"))
        m.ZIP_ID = "enigh2022_nc_csv"
        m.MIEMBRO = MIEMBRO_CONCENTRADO_2022
        inputs = {"enigh2022_nc_csv": {"ruta_absoluta": ZIP_2022}}
        contrato = {"parametros": {
            "bootstrap_replicas": 2000, "tolerancia_componente_pesos": 0.01,
            "controles_nacionales": CONTROLES_2022, "tolerancia_controles": 1e-10,
        }, "seed": {"valor": 20260919}}
        r = m.medir(inputs, contrato)
        sellado = _resultados_sellados("CALC-ENIGH2022-REMESAS-CONTEXTO-0001")
        for sufijo in ("ESTADO", "N-FILAS", "TABLA-JSON", "CONTRASTES-JSON"):
            self.assertEqual(r[f"RESULT-ENIGH16-REMCTX-{sufijo}"], sellado[f"RESULT-ENIGH22-REMCTX-{sufijo}"], sufijo)


if __name__ == "__main__":
    if not _payload_montado():
        print("SALTADO-SIN-PAYLOAD: data/raw/enigh2022_nc_csv.zip no montado -- 0 archivos examinados (A.13)")
        sys.exit(0)
    sys.exit(0 if unittest.main(exit=False).result.wasSuccessful() else 1)
