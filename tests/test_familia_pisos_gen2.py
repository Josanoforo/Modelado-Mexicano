"""D-22 de ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 (25/sep/2026): pisos por segmento
ENADID 2009/2014/2018, ENASIC 2022 y Pew GAS México 2013–2023.

Specs: forense/prereg-caja/FAMILIA-{ENADID,ENASIC,PEW}-PISOS-spec-v1_0.md §5. Sintético sin
microdato: se fabrican ZIP con los mismos miembros y columnas que declara cada spec (DBF,
CSV con BOM y `\\r`, SAV), se corre `medir()` de punta a punta con la receta y los
lectores leídos como bytes, y todas las ramas terminales (con soporte, categoría vacía,
fuera de universo, llave no pareada, conducta no preguntada en una ola, menos de 3 olas)
pasan el conducto que sella (`corrida0._valida_outputs`) sin NaN ni inf; `resultados:` del
spec.yaml es exactamente `esquema_resultados()`; la guardia de reserva PARA si un id de la
ola reservada llega como input.
"""
from __future__ import annotations

import hashlib
import importlib.util
import io
import math
import os
import struct
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import corrida0  # noqa: E402

RECETA = "tools/dominios/salud/pisos_diseno.py"
LECTORES = "tools/dominios/familia/lectores.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ENADID = _load("data/corrida0/CALC-ENADID-FAMILIA-HOGARES-0001/medidor.py", "m_enadid_familia")
ENASIC = _load("data/corrida0/CALC-ENASIC-CUIDADOS-VEJEZ-0001/medidor.py", "m_enasic_cuidados")
PEW = _load("data/corrida0/CALC-PEW-MIGRACION-MEX-0001/medidor.py", "m_pew_migracion")


def _repo_input(path):
    b = open(os.path.join(ROOT, path), "rb").read()
    return {"bytes": b, "sha256": hashlib.sha256(b).hexdigest()}


def _inputs_repo():
    return {"receta_pisos_salud": _repo_input(RECETA), "lectores_familia": _repo_input(LECTORES)}


def _contrato(calc, replicas=20):
    return {"parametros": {"bootstrap_replicas": replicas}, "seed": {"valor": 20260925}}


def _spec(calc):
    with open(os.path.join(ROOT, "data", "corrida0", calc, "spec.yaml")) as f:
        return yaml.safe_load(f)


def _conducto(M, out):
    esq = M.esquema_resultados()
    assert corrida0._valida_outputs({"resultados": esq}, out) == []
    for k, v in out.items():
        if isinstance(v, float):
            assert math.isfinite(v), k
    assert set(out) == {r["id"] for r in esq}


# ═══════════════════════════ fabricantes ═══════════════════════════

def _dbf(df):
    cols = list(df.columns)
    s = df.astype(str)
    lens = [max(1, int(s[c].str.len().max() or 1)) for c in cols]
    hl, rl = 32 + 32 * len(cols) + 1, 1 + sum(lens)
    h = struct.pack("<BBBBIHH20x", 3, 126, 1, 1, len(df), hl, rl)
    for c, ln in zip(cols, lens):
        h += struct.pack("<11sc4xBB14x", c.upper().encode()[:11], b"C", ln, 0)
    h += b"\r"
    body = b"".join(b" " + b"".join(str(v).ljust(ln)[:ln].encode("latin-1") for v, ln in zip(r, lens))
                    for r in s.itertuples(index=False))
    return h + body + b"\x1a"


def _csv(df, bom=True, cr=True):
    t = df.to_csv(index=False)
    if cr:
        t = t.replace("\n", "\r\n")
    return ("﻿" if bom else "").encode("utf-8") + t.encode("utf-8")


def _zip(tmp, nombre, miembros):
    ruta = os.path.join(tmp, nombre)
    with zipfile.ZipFile(ruta, "w") as z:
        for m, data in miembros.items():
            z.writestr(m, data)
    return ruta


def _enadid_frames(ola, rng, nh=300):
    H, Pm = ENADID.HOG[ola], ENADID.PER[ola]
    hog = {}
    llaves = [f"{i:06d}" for i in range(nh)]
    if len(H["llave"]) == 3:
        hog["control"] = llaves
        hog["viv_sel"] = ["01"] * nh
        hog["hogar"] = ["1"] * nh
    else:
        hog["llave_hog"] = llaves
    est = rng.integers(1, 6, nh)
    hog[H["fac"]] = rng.integers(50, 500, nh)
    hog[H["est"]] = [f"{e:03d}" for e in est]
    upm = [f"{e:03d}{rng.integers(0, 3)}" for e in est]
    upm[0] = "999999"  # estrato con UPM única posible
    hog[H["upm"]] = upm
    hog[H["tloc"]] = rng.integers(1, 5, nh)
    cls = rng.choice([1, 2, 3, 4, 5, 6, 9], nh)
    hog[H["cls"]] = [f"H{c}" if ola == "2009" else str(c) for c in cls]
    hog[H["sexo_j"]] = rng.integers(1, 3, nh)
    hog[H["edad_j"]] = rng.integers(15, 95, nh)
    hog[H["niv_j"]] = [f"{v:02d}" for v in rng.choice([0, 2, 3, 4, 6, 8, 99], nh)]
    tam = np.where(cls == 5, 1, rng.integers(2, 8, nh))
    hog[H["tam"]] = tam
    if H["mig"]:
        hog[H["mig"]] = rng.choice([1, 2, 9], nh)
    hog = pd.DataFrame(hog)[ENADID.columnas_hog(ola)]
    hog.iloc[5, hog.columns.get_loc(H["fac"])] = 0  # diseño inválido
    filas = []
    for i in range(nh):
        for r in range(int(tam[i])):
            filas.append((llaves[i], r))
    filas.append(("NOPAREA", 0))  # persona sin hogar
    per = {}
    if len(Pm["llave"]) == 3:
        per["control"] = [k for k, _ in filas]
        per["viv_sel"] = ["01"] * len(filas)
        per["hogar"] = ["1"] * len(filas)
    else:
        per["llave_hog"] = [k for k, _ in filas]
    n = len(filas)
    per[Pm["sexo"]] = rng.integers(1, 3, n)
    per[Pm["edad"]] = rng.choice(list(range(0, 99)) + [999], n)
    per[Pm["paren"]] = [1 if r == 0 else int(rng.choice([2, 3, 4, 8, 9])) for _, r in filas]
    per[Pm["niv"]] = [f"{v:02d}" for v in rng.choice([0, 2, 3, 6, 8, 99], n)]
    per[Pm["conyu"]] = rng.choice([1, 2, 3, 4, 5, 6, 7, 9], n)
    per = pd.DataFrame(per)[ENADID.columnas_per(ola)]
    return hog, per


def _enadid_payloads(tmp, rng):
    rutas = {}
    for ola in ENADID.OLAS:
        hog, per = _enadid_frames(ola, rng)
        H, Pm = ENADID.HOG[ola], ENADID.PER[ola]
        if ola == "2018":
            m = {H["miembro"]: _csv(hog), Pm["miembro"]: _csv(per, bom=False)}
        else:
            m = {H["miembro"]: _dbf(hog), Pm["miembro"]: _dbf(per)}
        rutas[ENADID.PAYLOADS[ola]] = {"ruta_absoluta": _zip(tmp, f"enadid{ola}.zip", m)}
    return rutas


def _enasic_payload(tmp, rng, nh=250):
    llaves = [f"{i:05d}1" for i in range(nh)]
    est = rng.integers(1, 5, nh)
    tam = rng.integers(1, 7, nh)
    hog = pd.DataFrame({
        "LLAVEHOG": llaves, "FAC_HOG": rng.integers(700, 3000, nh), "EST_DIS": [f"{e:04d}" for e in est],
        "UPM_DIS": [f"{e:03d}{rng.integers(0, 3):02d}" for e in est], "HN_C": rng.integers(1, 3, nh),
        "HN_C60MA": rng.integers(1, 3, nh), "SEXO_JEFE": rng.integers(1, 3, nh),
        "EDAD_JEFE": rng.integers(18, 99, nh)})
    filas = []
    for i in range(nh):
        for r in range(1, int(tam[i]) + 1):
            filas.append((llaves[i], r))
    n = len(filas)
    edad = rng.integers(0, 98, n)
    p444 = rng.choice([0, 1, 2, 3, 7, 99], n)
    per = pd.DataFrame({
        "LLAVESDE": [f"{k}{r:02d}" for k, r in filas], "LLAVEHOG": [k for k, _ in filas],
        "PAREN": [1 if r == 1 else int(rng.choice([2, 3, 4, 5])) for _, r in filas],
        "SEXO": rng.integers(1, 3, n), "EDAD": edad, "NIV": [f"{v:02d}" for v in rng.choice([0, 2, 3, 6, 8, 99], n)],
        "P4_42": np.where(edad >= 60, rng.choice([1, 2, 3], n), 0),
        "P4_44": np.where(edad >= 60, p444, 0), "P4_44A": rng.integers(1, 12, n),
        "P4_45": np.where(edad >= 60, rng.choice([1, 2], n), 0)}).astype(str)
    per.loc[per["EDAD"].astype(int) < 60, ["P4_42", "P4_44", "P4_44A", "P4_45"]] = ""
    ruta = _zip(tmp, "enasic.zip", {"TCSDEMPO.csv": _csv(per), "THOGAR.csv": _csv(hog.astype(str)),
                                     "TVIVIENDA.csv": _csv(pd.DataFrame({"LLAVEVIV": ["00101"]}))})
    return {ENASIC.PAY: {"ruta_absoluta": ruta}}


def _pew_payloads(tmp, rng, n=400):
    import pyreadstat

    rutas = {}
    for ola in PEW.OLAS:
        c = PEW.OLA_CFG[ola]
        pais_var, mex = c["pais"]
        d = {pais_var: np.where(np.arange(n) < n - 40, mex, mex + 1).astype(float),
             c["sexo"]: rng.integers(1, 3, n).astype(float),
             c["edad"]: rng.choice(list(range(18, 98)) + [98, 99], n).astype(float),
             c["w"]: rng.uniform(0.2, 3.0, n)}
        if c["psu"]:
            d[c["est"]] = rng.integers(1, 5, n).astype(float)
            d[c["psu"]] = rng.integers(1, 40, n).astype(float)
        for k in PEW.CONDUCTAS:
            if ola in PEW.CONDUCTAS[k]:
                var = PEW.CONDUCTAS[k][ola][0]
                d[var] = rng.choice([1, 2, 3, 8, 9], n).astype(float)
        df = pd.DataFrame(d)
        with tempfile.TemporaryDirectory() as t2:
            sav = os.path.join(t2, "d.sav")
            pyreadstat.write_sav(df, sav)
            rutas[PEW.PAYLOADS[ola]] = {"ruta_absoluta": _zip(tmp, f"pew{ola}.zip", {"Dataset.sav": open(sav, "rb").read()})}
    return rutas


# ═══════════════════════════ pruebas ═══════════════════════════

def test_enadid_sintetico_de_punta_a_punta():
    rng = np.random.default_rng(1)
    with tempfile.TemporaryDirectory() as tmp:
        inputs = {**_enadid_payloads(tmp, rng), **_inputs_repo()}
        out = ENADID.medir(inputs, _contrato("ENADID"))
    _conducto(ENADID, out)
    P = ENADID.P
    assert out[f"{P}-G-2018-PERSONA-SIN-HOGAR"] >= 1  # sin hogar o hogar sin diseño válido
    assert out[f"{P}-G-2014-FILAS-HOGAR-DISENO-VALIDO"] == 299
    # 2009: migración internacional fuera por spec (MIGRA_HO es «a EUA»)
    assert out[ENADID.rid("HOGAR-CON-MIGRANTE-INTERNACIONAL-5A", "2009", "TOTAL", "TODOS", "P")] is None
    assert out[ENADID.rid("HOGAR-CON-MIGRANTE-INTERNACIONAL-5A", "2018", "TOTAL", "TODOS", "P")] is not None
    assert out[ENADID.rid("PERSONA-60MAS", "2009", "TOTAL", "TODOS", "P")] is not None
    assert out[f"{P}-HOGAR-CON-MIGRANTE-INTERNACIONAL-5A-TOTAL-TAU2"] is None
    assert out[ENADID.rid("HOGAR-CON-MIGRANTE-INTERNACIONAL-5A", "2018", "TOTAL", "TODOS", "ICC-LO")] is None
    assert out[f"{P}-PERSONA-60MAS-TOTAL-TAU2"] is not None


def test_enasic_sintetico_de_punta_a_punta():
    rng = np.random.default_rng(2)
    with tempfile.TemporaryDirectory() as tmp:
        inputs = {**_enasic_payload(tmp, rng), **_inputs_repo()}
        out = ENASIC.medir(inputs, _contrato("ENASIC"))
    _conducto(ENASIC, out)
    P = ENASIC.P
    assert out[f"{P}-G-CUIDADOR-RENGLON-SIN-PAREO"] > 0  # renglón 7 en hogares de < 7
    assert out[ENASIC.rid("AM60-CUIDADOR-PRINCIPAL-MUJER", "TOTAL", "TODOS", "P")] is not None


def test_pew_sintetico_de_punta_a_punta():
    rng = np.random.default_rng(3)
    with tempfile.TemporaryDirectory() as tmp:
        inputs = {**_pew_payloads(tmp, rng), **_inputs_repo()}
        out = PEW.medir(inputs, _contrato("PEW"))
    _conducto(PEW, out)
    P = PEW.P
    assert out[f"{P}-G-2013-FILAS-MEXICO"] == 360  # filtro de país
    c = "BUENO-PARA-MEXICO-QUE-VIVAN-EN-EEUU"  # 2 olas: sin IC calibrado
    assert out[f"{P}-{c}-TOTAL-TAU2"] is None
    assert out[PEW.rid(c, "2018", "TOTAL", "TODOS", "ICC-LO")] is None
    c = "IRIA-A-VIVIR-A-EEUU"
    assert out[f"{P}-{c}-TOTAL-TAU2"] is not None


@pytest.mark.parametrize("M,intruso", [(ENADID, "enadid2023_base_datos_csv"), (PEW, "pew_gas_spring2025")])
def test_guardia_de_reserva_para(M, intruso):
    inputs = {k: {"ruta_absoluta": "/x"} for k in M.PAYLOADS.values()}
    inputs.update(_inputs_repo())
    inputs[intruso] = {"ruta_absoluta": "/x"}
    with pytest.raises(M.ParoDeGuardia, match="reservada|2025"):
        M.medir(inputs, _contrato("x"))


@pytest.mark.parametrize("M,calc", [(ENADID, "CALC-ENADID-FAMILIA-HOGARES-0001"),
                                    (ENASIC, "CALC-ENASIC-CUIDADOS-VEJEZ-0001"),
                                    (PEW, "CALC-PEW-MIGRACION-MEX-0001")])
def test_resultados_del_spec_yaml_son_el_esquema(M, calc):
    assert _spec(calc)["resultados"] == M.esquema_resultados()
