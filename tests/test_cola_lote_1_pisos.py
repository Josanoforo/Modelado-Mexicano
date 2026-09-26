"""D-22 de ACTO GEN2-COLA-LOTE-1 (25/sep/2026): pisos de la cola v1.1, lote 1.

Specs: forense/prereg-caja/{CCPV-FAM,EMAT-PAREJA,ENPECYT-CONOC,EDR-SUICIDIO}-PISOS-spec-v1_0.md §5.
Sintético sin microdato: las ramas terminales de cada medidor (con soporte, fuera de universo,
código no especificado, categoría vacía, llave sin jefe o con dos, UPM única de estrato, ola
reservada rechazada por la guardia) pasan el conducto que sella (`corrida0._valida_outputs`)
sin NaN ni inf, y `resultados:` del spec.yaml es exactamente `esquema_resultados()`.
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


R = _load("tools/dominios/salud/pisos_diseno.py", "receta_pisos_cola_lote_1_test")
RECETA_BYTES = open(os.path.join(ROOT, "tools/dominios/salud/pisos_diseno.py"), "rb").read()


def _spec(calc):
    with open(os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")) as f:
        return yaml.safe_load(f)


def _sin_no_finitos(out):
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k


def _cierra(M, out, extra):
    for k, v in extra.items():
        out[f"{M.P}-G-{k}"] = v
    assert corrida0._valida_outputs({"resultados": M.esquema_resultados()}, out) == []
    _sin_no_finitos(out)
    return out


# ═══════════════════════════ CCPV ═══════════════════════════

CCPV = _load("data/corrida0/CALC-CCPV-FAM-PISOS-0001/medidor.py", "m_ccpv_fam")


def _ccpv_marco():
    viv, per = [], []
    rng = np.random.default_rng(7)
    for i in range(120):
        ent = f"{1 + i % 5:02d}"
        est = "9" if i == 0 else str(1 + i % 3)  # estrato 9: UPM única (certeza)
        th = (1, 2, 3, 4, 5, 6, 9)[i % 7]
        viv.append({"ent": ent, "id_viv": str(i), "tipohog": th, "numpers": 0 if i == 3 else 1 + i % 6,
                    "factor": 0 if i == 4 else int(rng.integers(10, 90)), "estrato": est,
                    "upm": f"{est}{i % 4}", "tam_loc": 1 + i % 4})
        if i == 5:
            continue  # vivienda sin personas
        miembros = [1] if th == 5 else [1, 2, 3, 4, 6][: 2 + i % 4]
        if i == 6:
            miembros = [2, 3]  # sin jefe
        if i == 7:
            miembros = [1, 1, 3]  # dos jefes
        for j, par in enumerate(miembros):
            edad = (70 if th == 5 and i % 2 else 35 + 3 * j) if par != 4 else 8
            if i == 8 and j == 1:
                edad = 999
            per.append({"ent": ent, "id_viv": str(i), "sexo": (1, 3, 2)[(i + j) % 3] if i == 9 else (1, 3)[(i + j) % 2],
                        "edad": edad, "parent": 99 if (i == 10 and j == 1) else par, "nivacad": (0, 4, 10, 99)[j % 4],
                        "factor": int(rng.integers(10, 90)), "estrato": est, "upm": f"{est}{i % 4}",
                        "tam_loc": 1 + i % 4})
    return pd.DataFrame(viv), pd.DataFrame(per)


def test_ccpv_ramas_terminales_pasan_el_conducto():
    viv, per = _ccpv_marco()
    out = CCPV.mide(viv, per, R, 20, 1)
    out = _cierra(CCPV, out, {"BOOTSTRAP-REPLICAS": 20, "SEED": 1, "INPUT-RECETA-SHA256": "x",
                              "OLA-RESERVADA": "x"})
    assert out[f"{CCPV.P}-G-VIV-SIN-JEFE"] == 1
    assert out[f"{CCPV.P}-G-VIV-JEFE-MULTIPLE"] == 1
    assert out[f"{CCPV.P}-G-VIV-SIN-PERSONAS"] == 1
    assert out[f"{CCPV.P}-G-PER-SEXO-FUERA-CATALOGO"] >= 1
    # la proporción total de tipos de hogar suma 1 sin el 4 (familiar no especificado) ni el 9
    s = sum(out[CCPV.rid(c, "TOTAL", "TODOS", "P")] for c in
            ("HOG-NUCLEAR", "HOG-AMPLIADO", "HOG-COMPUESTO", "HOG-UNIPERSONAL", "HOG-CORRESIDENTES"))
    assert 0.0 < s < 1.0
    assert out[CCPV.rid("HOG-TAMANO-MEDIO", "TOTAL", "TODOS", "P")] > 1.0
    assert out[CCPV.rid("HOG-NUCLEAR", "ENT", "32", "N")] == 0


def test_ccpv_mujer_es_3():
    assert (CCPV.HOMBRE, CCPV.MUJER) == (1, 3)


def test_ccpv_guardia_rechaza_2020():
    inputs = {pid: {"ruta_absoluta": f"/x/ccpv/2010/MC2010_{e}_dta.zip"} for e, pid in CCPV.PAY.items()}
    inputs["receta_pisos"] = {"bytes": RECETA_BYTES}
    CCPV._guardia_inputs(inputs)
    inputs[CCPV.PAY["09"]] = {"ruta_absoluta": "/x/ccpv/2020/MC2010_09_dta.zip"}
    with pytest.raises(CCPV.ParoDeGuardia):
        CCPV._guardia_inputs(inputs)


def test_ccpv_spec_yaml_es_el_esquema():
    assert _spec("CALC-CCPV-FAM-PISOS-0001")["resultados"] == CCPV.esquema_resultados()


# ═══════════════════════════ registros: EMAT y EDR ═══════════════════════════

def _dbf(filas, campos):
    """DBF dBase III mínimo (todos C) para probar el lector de ancho fijo; una fila extra borrada."""
    import struct
    largos = {c: max([len(str(f.get(c, ""))) for f in filas] + [1]) for c in campos}
    lreg = 1 + sum(largos.values())
    cab = bytearray(struct.pack("<BBBBIHH20x", 3, 126, 9, 25, len(filas) + 1, 32 + 32 * len(campos) + 1, lreg))
    for c in campos:
        cab += struct.pack("<11sc4xB15x", c.encode()[:11], b"C", largos[c])
    cab += b"\x0d"
    cuerpo = bytearray()
    for f in filas + [{c: "9" for c in campos}]:
        cuerpo += b" "
        for c in campos:
            cuerpo += str(f.get(c, "")).ljust(largos[c]).encode()[: largos[c]]
    cuerpo[-lreg] = 0x2A  # la última fila está borrada
    return bytes(cab + cuerpo)


EMAT = _load("data/corrida0/CALC-EMAT-PAREJA-PISOS-0001/medidor.py", "m_emat_pareja")


def _emat_ola(ola, k):
    filas = []
    for i in range(60):
        filas.append({"ENT_REGIS": f"{1 + i % 4:02d}", "TAM_LOC_RE": ("1", "5", "9", "15", "99")[i % 5],
                      "ANIO_REGIS": ola if i != 1 else "2009", "GENERO": ("1", "2", "1", "7")[i % 4],
                      "SEXO_CON1": "1", "EDAD_CON1": ("17", "25", "33", "99", "70")[(i + k) % 5],
                      "ESCOL_CON1": str(1 + i % 9), "CONACTCON1": ("1", "2", "9")[i % 3],
                      "SEXO_CON2": ("2", "1")[i % 4 == 1], "EDAD_CON2": ("23", "41", "12")[i % 3],
                      "ESCOL_CON2": str(1 + (i * 2) % 9), "CONACTCON2": ("1", "2")[i % 2]})
    return filas


def test_emat_lector_dbf_y_ramas_pasan_el_conducto():
    por_ola = {o: EMAT.lee_dbf(_dbf(_emat_ola(o, j), EMAT.CAMPOS)) for j, o in enumerate(EMAT.OLAS)}
    assert all(len(df) == 60 for df in por_ola.values())  # la fila borrada no entra
    out = EMAT.mide(por_ola, R)
    for k in ("INPUT-RECETA-SHA256", "OLA-RESERVADA", "NATURALEZA"):
        out[f"{EMAT.P}-G-{k}"] = "x"
    assert corrida0._valida_outputs({"resultados": EMAT.esquema_resultados()}, out) == []
    _sin_no_finitos(out)
    assert out[f"{EMAT.P}-G-2010-ANIO-REGIS-DISTINTO"] == 1
    assert out[f"{EMAT.P}-G-2010-GENERO-FUERA-CATALOGO"] == 15
    assert out[EMAT.rid("M-MISMO-SEXO", "2023", "ENT", "32", "N")] == 0
    assert out[EMAT.rid_p("M-CON-MENOR-18", "TOTAL", "TODOS", "TAU2")] is not None


def test_emat_guardia_rechaza_2024():
    inputs = {pid: {"ruta_absoluta": f"/x/EMAT/{pid}.zip"} for pid in EMAT.ZIPS}
    inputs["receta_pisos"] = {"bytes": RECETA_BYTES}
    EMAT._guardia_inputs(inputs)
    inputs["emat2023_bd_dbf_zip"] = {"ruta_absoluta": "/x/INEGI/EMAT/2024/matrimonios_base_datos_2024_dbf.zip"}
    with pytest.raises(EMAT.ParoDeGuardia):
        EMAT._guardia_inputs(inputs)


def test_emat_spec_yaml_es_el_esquema():
    assert _spec("CALC-EMAT-PAREJA-PISOS-0001")["resultados"] == EMAT.esquema_resultados()


EDR = _load("data/corrida0/CALC-EDR-SUICIDIO-PISOS-0001/medidor.py", "m_edr_suicidio")


def _edr_ola(ola, k):
    pres = EDR.PRESUNTO[ola]
    filas = []
    for i in range(80):
        filas.append({"ENT_RESID": f"{1 + i % 3:02d}", "TLOC_RESID": ("2", "5", "8", "14", "99")[i % 5],
                      "CAUSA_DEF": ("X700", "X84", "I219", "", "X600", "Y870")[(i + k) % 6],
                      "SEXO": ("1", "2", "9")[i % 3], "EDAD": ("4017", "4035", "4998", "2005", "4070")[i % 5],
                      "ANIO_OCUR": (ola, "2012")[i % 7 == 0], "ANIO_REGIS": ola,
                      "ESCOLARIDA": ("1", "6", "8", "10", "88")[i % 5], pres: ("3", "1", "8")[i % 3]})
    return filas


def test_edr_ramas_pasan_el_conducto():
    por_ola = {o: EDR.lee_dbf(_dbf(_edr_ola(o, j), EDR.CAMPOS_BASE + (EDR.PRESUNTO[o],)),
                              EDR.CAMPOS_BASE + (EDR.PRESUNTO[o],)) for j, o in enumerate(EDR.OLAS)}
    out = EDR.mide(por_ola, R)
    for k in ("INPUT-RECETA-SHA256", "OLA-RESERVADA", "NATURALEZA"):
        out[f"{EDR.P}-G-{k}"] = "x"
    assert corrida0._valida_outputs({"resultados": EDR.esquema_resultados()}, out) == []
    _sin_no_finitos(out)
    assert out[f"{EDR.P}-G-2015-CAUSA-VACIA"] > 0
    assert out[EDR.rid("SUICIDIO-CIE", "2023", "ENT", "32", "N")] == 0


def test_edr_cie_y_edad():
    assert list(EDR.es_suicidio_cie(["X60", "X849", "X85", "Y870", "x700", "X59"])) == [True, True, False, False,
                                                                                      True, False]
    a = EDR.años([4017, 4998, 2005, 1098, 4120, 5000])
    assert a[0] == 17 and np.isnan(a[1]) and a[2] == 0 and np.isnan(a[3]) and a[4] == 120 and np.isnan(a[5])


def test_edr_guardia_rechaza_2024():
    inputs = {pid: {"ruta_absoluta": f"/x/EDR/{pid}.zip"} for pid in EDR.ZIPS}
    inputs["receta_pisos"] = {"bytes": RECETA_BYTES}
    EDR._guardia_inputs(inputs)
    inputs["edr2022_bd_dbf_zip"] = {"ruta_absoluta": "/x/edr2024/defunciones_base_datos_2024_dbf.zip"}
    with pytest.raises(EDR.ParoDeGuardia):
        EDR._guardia_inputs(inputs)


def test_edr_spec_yaml_es_el_esquema():
    assert _spec("CALC-EDR-SUICIDIO-PISOS-0001")["resultados"] == EDR.esquema_resultados()


