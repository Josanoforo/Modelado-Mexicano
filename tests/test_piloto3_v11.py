#!/usr/bin/env python3
"""Piloto 3 · COMMIT-1 v1.1 · validación de «congelado» (ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1).

Un COMMIT-1 no está congelado si su punto de entrada nunca corrió. Aquí corre:
  (a) sintética: `medir()` de punta a punta sobre un fixture chico → cinco
      emisiones por celda con IC; `adjudicacion.medir()` sobre un R sintético.
  (b) de oro, sobre ENCIG 2023 (ola NO reservada): el mismo código con ola=2023
      reproduce p(a,b), n, δ e IC sellados en CALC-ENCIG2023-CRUCES-HISTORICOS-0002.
      Control, no medición: no se sella. Se salta si el corpus no está montado.
  (c) reserva: ENCIG 2025 no se abrió — ningún producto derivado de encig25* en el
      árbol; las guardias S1/S2/sello paran como deben.
  (d) λ se re-deriva de los DELTA/DELTA-EE sellados y coincide con la congelada.
"""
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import zipfile

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMI = os.path.join(ROOT, "data", "corrida0", "CALC-GOB-DIGITAL-EXE-EMISIONES-0002")
ADJ = os.path.join(ROOT, "data", "corrida0", "CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001")
SELL21 = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG2021-CRUCES-HISTORICOS-0003", "resultados.json")
SELL23 = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG2023-CRUCES-HISTORICOS-0002", "resultados.json")
CTL = os.path.join(ROOT, "data", "corrida0", "CALC-C2-COMPUESTO-RESERVADAS-0001", "resultados.json")
FIRMAS = os.path.join(ROOT, "forense", "firmas-pendientes.tsv")
ZIP23 = os.path.join(ROOT, "data", "raw", "encig23_base_datos_csv.zip")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load(os.path.join(EMI, "medidor.py"), "p3_medidor")
A = _load(os.path.join(ADJ, "adjudicacion.py"), "p3_adjudicacion")


def _repo(path):
    return {"ruta_absoluta": path, "bytes": open(path, "rb").read()}


def _contrato(ola, payload_id, replicas, seed, s1="CAMBIO-MENOR"):
    return {"parametros": {"ola": ola, "payload_id": payload_id, "bootstrap_replicas": replicas,
                           "s1_veredicto": s1}, "seed": {"aplica": True, "valor": seed}}


# ────────────────────────────── fixture sintético ──────────────────────────────

def _fixture_zip(tmp_path, ola="2099", n_personas=7000, seed=7):
    rng = np.random.default_rng(seed)
    filas_p, filas_t = [], []
    for i in range(n_personas):
        est = f"{1 + i % 3:02d}"
        upm = f"{i % 24:03d}"
        edad = int(rng.choice([22, 35, 50, 70, 97, 98, 99], p=[.22, .28, .25, .21, .015, .02, .005]))
        niv = str(int(rng.choice([1, 3, 5, 8])))
        idp = f"P{i:05d}"
        filas_p.append(f"{idp},{edad},{niv},{est},{upm}")
        p = 0.35 + 0.15 * (niv == "8") + 0.1 * (edad < 45)
        canal = str(int(rng.choice([1, 2, 4, 5, 6, 3, 9], p=[.25, .15, p * .6, p * .4, .05, .03, .02] / np.sum([.25, .15, p * .6, p * .4, .05, .03, .02]))))
        ntra = "01" if rng.random() < 0.9 else "03"
        filas_t.append(f"{idp},{ntra},{canal},{100 + int(rng.integers(0, 50))},{est},{upm}")
    sec7 = "ID_PER,N_TRA,P7_3,FAC_TRA,EST_DIS,UPM_DIS\n" + "\n".join(filas_t) + "\n"
    res = "ID_PER,EDAD,NIV,EST_DIS,UPM_DIS\n" + "\n".join(filas_p) + "\n"
    z = tmp_path / f"encig{ola}_sintetico.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(f"conjunto_de_datos_encig{ola}_04_sec_7.csv", sec7)
        zf.writestr(f"conjunto_de_datos_encig{ola}_02_residentes_sec_2.csv", res)
    return str(z)


def _sellados_sinteticos(tmp_path, seed=3):
    rng = np.random.default_rng(seed)
    docs = {}
    for ola, pre in (("2021", M.PREFIJO_SELLADO["2021"]), ("2023", M.PREFIJO_SELLADO["2023"])):
        r = {}
        for a, b in M.CELDAS:
            k = f"{pre}-{a}-{b}"
            p = float(rng.uniform(0.3, 0.8))
            r[k + "-N"] = 60 if (a, b) == ("18-29", "HASTA-PRIMARIA") else int(rng.integers(250, 900))
            r[k + "-P"] = p
            r[k + "-P-IC-LO"] = p - 0.03
            r[k + "-P-IC-HI"] = p + 0.03
            r[k + "-DELTA"] = float(rng.normal(0, 0.15))
            r[k + "-DELTA-EE"] = 0.06
        path = tmp_path / f"sellado{ola}.json"
        path.write_text(json.dumps({"resultados": r}), encoding="utf-8")
        docs[ola] = str(path)
    ctl = {f"{M.PREFIJO_CONTROL}-{a}-X-{b}": 0.55 for a, b in M.CELDAS}
    cpath = tmp_path / "control.json"
    cpath.write_text(json.dumps({"resultados": ctl}), encoding="utf-8")
    return docs, str(cpath)


def _firmas(tmp_path, estado="FIRMADA"):
    t = "id\tqué_se_firma\tdónde\tcreado\tgatea\testado\tfirmada_en\tejecutada_en\tencargo\n"
    t += f"FP-399\tS2\tnota\t2026-09-20\tCOMMIT-1 v1.1\t{estado}\t\t\tencargo\n"
    p = tmp_path / "firmas.tsv"
    p.write_text(t, encoding="utf-8")
    return str(p)


def _inputs_sinteticos(tmp_path, estado_fp="FIRMADA"):
    z = _fixture_zip(tmp_path)
    docs, ctl = _sellados_sinteticos(tmp_path)
    return {
        "sintetico_csv": {"ruta_absoluta": z},
        "encig2021_cruces_resultados": _repo(docs["2021"]),
        "encig2023_cruces_resultados": _repo(docs["2023"]),
        "c2_compuesto_resultados": _repo(ctl),
        "firmas_pendientes_tsv": _repo(_firmas(tmp_path, estado_fp)),
    }


# ────────────────────────────── (a) sintética ──────────────────────────────

def test_a_medir_punta_a_punta_sintetico(tmp_path):
    inputs = _inputs_sinteticos(tmp_path)
    out = M.medir(inputs, _contrato("2099", "sintetico_csv", 300, 11))
    P = M.prefijo("2099")
    assert out[f"{P}-N-UNIVERSO"] > 500
    assert out[f"{P}-S2-EDAD-97-N"] > 0 and out[f"{P}-S2-RESERVA"] in ("RESERVA-S2", "SIN-RESERVA")
    for a, b in M.CELDAS:
        base = f"{P}-{a}-{b}"
        for cid in ("C2", "S-MEDIO", "S-LAMBDA"):
            assert 0.0 < out[f"{base}-{cid}-P"] < 1.0
            assert out[f"{base}-{cid}-P-IC-LO"] <= out[f"{base}-{cid}-P"] <= out[f"{base}-{cid}-P-IC-HI"]
            assert out[f"{base}-{cid}-B-VALIDAS"] == 300
        assert 0.0 < out[f"{base}-C1A-P"] < 1.0 and 0.0 < out[f"{base}-C1B-P"] < 1.0
    assert out[f"{P}-18-29-HASTA-PRIMARIA-SOPORTE-HISTORICO"] == "FUERA-DE-SOPORTE-EX-ANTE"
    # la lista `resultados:` de la spec se deriva del mismo esquema que emite
    ids = {r["id"] for r in M.esquema_resultados("2099")}
    assert ids == set(out), (ids ^ set(out))


def test_a_adjudicacion_sobre_r_sintetico(tmp_path):
    inputs = _inputs_sinteticos(tmp_path)
    con = _contrato("2099", "sintetico_csv", 300, 11)
    emis = M.medir(inputs, con)
    res_path = tmp_path / "resultados.json"
    res_path.write_text(json.dumps({"resultados": emis}), encoding="utf-8")
    sello = {"resultados.json": hashlib.sha256(res_path.read_bytes()).hexdigest()}
    sello_path = tmp_path / "sello.json"
    sello_path.write_text(json.dumps(sello), encoding="utf-8")
    inputs2 = dict(inputs, emisiones_resultados=_repo(str(res_path)), emisiones_sello=_repo(str(sello_path)))
    out = A.medir(inputs2, con)
    P = A.prefijo("2099")
    assert out[f"{P}-B-BIS"].split("+")[0] in ("CORROBORADA", "FALSADOR-DEBIL", "LIMITA-C2",
                                               "LIMITA-C2-SOBRE-CUANTO-ENCOGER", "FUERA-DE-SOPORTE-GLOBAL")
    assert out[f"{P}-C2-REPRODUCE-MAX-ABS"] <= A.TOL_C2
    assert out[f"{P}-PUNTUADAS-N"] >= 12, out[f"{P}-PUNTUADAS-N"]   # el fixture ejercita la adjudicación de verdad
    assert out[f"{P}-SOPORTE-GLOBAL"] == "CON-SOPORTE"
    for j in A.RETADORES:
        assert out[f"{P}-{j}-GANA"] in ("SI", "NO")
        if out[f"{P}-PUNTUADAS-N"]:
            assert out[f"{P}-{j}-DELTA-MAE-IC-LO"] <= out[f"{P}-{j}-DELTA-MAE-PP"] <= out[f"{P}-{j}-DELTA-MAE-IC-HI"]
    ids = {r["id"] for r in A.esquema_resultados("2099")}
    assert ids == set(out), (ids ^ set(out))
    # sin sello → no corre; con sello alterado → no corre
    with pytest.raises(A.ParoDeGuardia):
        A.medir(inputs, con)
    inputs3 = dict(inputs2, emisiones_sello=_repo(str(_firmas(tmp_path))))
    with pytest.raises((A.ParoDeGuardia, ValueError, KeyError)):
        A.medir(inputs3, con)


# ────────────────────────────── (c) guardias y reserva ──────────────────────────────

def test_c_guardias_paran(tmp_path):
    inputs = _inputs_sinteticos(tmp_path, estado_fp="ABIERTA")
    with pytest.raises(M.ParoDeGuardia, match="FP-399"):
        M.medir(inputs, _contrato("2099", "sintetico_csv", 50, 1))
    inputs = _inputs_sinteticos(tmp_path)
    with pytest.raises(M.ParoDeGuardia, match="S1"):
        M.medir(inputs, _contrato("2099", "sintetico_csv", 50, 1, s1="CAMBIO-DE-INSTRUMENTO"))
    inputs["encig25_base_datos_csv"] = {"ruta_absoluta": "/dev/null"}
    with pytest.raises(M.ParoDeGuardia, match="RESERVA"):
        M.medir(inputs, _contrato("2099", "sintetico_csv", 50, 1))


def test_c_fp399_firmada_en_el_repo():
    assert M._fp_estado(open(FIRMAS, "rb").read(), "FP-399") == "FIRMADA"


def test_c_reserva_encig2025_no_abierta():
    for d in (EMI, ADJ):
        for f in ("ejecucion.json", "resultados.json", "sello.json", "sello.sha256"):
            assert not os.path.exists(os.path.join(d, f)), f"{d}/{f} existe: COMMIT-1 no emite"
    # ningún archivo versionado trae un RESULT de este piloto sobre 2025
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.split(b"\0")
    for rel in tracked:
        if not rel or not rel.endswith((b".json", b".tsv", b".yaml", b".md")):
            continue
        if b"forense/encargos/" in rel or rel.endswith(b"test_piloto3_v11.py"):
            continue
        try:
            data = open(os.path.join(ROOT, rel.decode()), "rb").read()
        except FileNotFoundError:
            continue
        assert b"RESULT-GOB-EXE15-2025-MARGINAL" not in data and b"RESULT-GOB-EXE15-ADJ-2025-" not in data, rel
    src = open(os.path.join(EMI, "medidor.py"), encoding="utf-8").read()
    assert "encig25_base_datos_csv.zip" not in src and "data/raw" not in src


# ────────────────────────────── (d) λ ──────────────────────────────

def test_d_lambda_se_rederiva_de_los_sellados():
    r21 = json.load(open(SELL21))["resultados"]
    r23 = json.load(open(SELL23))["resultados"]
    dbar, var = [], []
    for a, b in M.CELDAS:
        if (a, b) in M.FUERA_DE_SOPORTE_EX_ANTE:
            continue
        k21 = f"{M.PREFIJO_SELLADO['2021']}-{a}-{b}"
        k23 = f"{M.PREFIJO_SELLADO['2023']}-{a}-{b}"
        dbar.append((r21[k21 + "-DELTA"] + r23[k23 + "-DELTA"]) / 2)
        var.append((r21[k21 + "-DELTA-EE"] ** 2 + r23[k23 + "-DELTA-EE"] ** 2) / 4)
    assert len(dbar) == 15
    var_entre = float(np.var(dbar, ddof=1))
    sigma2 = float(np.mean(var))
    tau2 = max(0.0, var_entre - sigma2)
    lam = tau2 / (tau2 + sigma2)
    assert abs(lam - M.LAMBDA) < 1e-12, (lam, M.LAMBDA)
    assert abs(tau2 - 0.02525670198316379) < 1e-15 and abs(sigma2 - 0.003001124084482884) < 1e-15


# ────────────────────────────── (b) oro sobre 2023 ──────────────────────────────

@pytest.mark.skipif(not os.path.exists(ZIP23), reason="corpus no montado (NUBE): control de oro sólo en CAJA")
def test_b_oro_2023_reproduce_los_sellados():
    sel = json.load(open(SELL23))["resultados"]
    pre = M.PREFIJO_SELLADO["2023"]
    inputs = {
        "encig23_base_datos_csv": {"ruta_absoluta": ZIP23},
        "encig2021_cruces_resultados": _repo(SELL21),
        "encig2023_cruces_resultados": _repo(SELL23),
        "c2_compuesto_resultados": _repo(CTL),
        "firmas_pendientes_tsv": _repo(FIRMAS),
    }
    con = _contrato("2023", "encig23_base_datos_csv", 10000, 20260919)
    frame, diag = M.cargar_universo(inputs, con)
    # F1-bis: residuo de edad = 107 trámites, masa 571 754, todo código 98 (PR #924)
    assert diag["RESIDUO-EDAD-N"] == 107 and abs(diag["RESIDUO-EDAD-MASA"] - 571754.0) < 1e-6
    assert diag["S2-EDAD-97-N"] == 0 and diag["S2-EDAD-98-N"] == 107 and diag["S2-EDAD-99-N"] == 0
    cr = A.cruce(frame, 10000, 20260919)
    worst = {"p": 0.0, "d": 0.0, "ic": 0.0}
    for a, b in M.CELDAS:
        k = f"{pre}-{a}-{b}"
        assert cr["n"][(a, b)] == sel[k + "-N"], (a, b)
        worst["p"] = max(worst["p"], abs(cr["R"][(a, b)] - sel[k + "-P"]))
        worst["d"] = max(worst["d"], abs(cr["delta"][(a, b)] - sel[k + "-DELTA"]))
        _, lo, hi, valid = cr["R_ic"][(a, b)]
        assert valid == 10000
        worst["ic"] = max(worst["ic"], abs(lo - sel[k + "-P-IC-LO"]), abs(hi - sel[k + "-P-IC-HI"]))
    assert worst["p"] < 1e-10 and worst["d"] < 1e-10, worst
    assert worst["ic"] < 1e-9, worst
    # el medidor de emisiones, con ola=2023, corre entero y su C2 coincide con el del cruce
    out = M.medir(inputs, con)
    P = M.prefijo("2023")
    assert out[f"{P}-N-COMPLETOS"] == diag["N-COMPLETOS"]
    for a, b in M.CELDAS:
        assert abs(out[f"{P}-{a}-{b}-C2-P"] - cr["C2"][(a, b)]) < 1e-12
