#!/usr/bin/env python3
"""Piloto 4 (`GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`) · COMMIT-1 · validación de
«congelado» (D-22), cuatro cruces reservados de `evasion_norma`.

Un COMMIT-1 no está congelado si su punto de entrada nunca corrió. Aquí corre:
  (a) sintética: `medir()` de punta a punta sobre un fixture chico (los
      tres años, los cuatro ejes) -> emisiones por celda con IC en los
      cuatro cruces; `adjudicacion.medir()` sobre un R sintético.
  (b) de control (no hay "oro" propio -- ningún CALC previo midió estos
      cuatro cruces): se reproduce `escolaridad_proxy x dominio_urbano_rural`
      (piloto 2, YA sellado) llamando la misma maquinaria compartida
      (`mr.carga_ola`/`mr.cruce`) que este medidor usa.
  (c) reserva: ENVIPE 2025 no se cruzó -- ningún producto derivado en el
      árbol; las guardias de firma paran como deben.
  (d) λ, por cada uno de los cuatro cruces: se re-deriva por fuera de
      cualquier función del medidor, de los `I23`/`I24`/`EE` que el propio
      `medir()` sintético produjo, y coincide con la `λ_cruce` emitida.
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
EMI = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001")
ARB = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001")
SXD_EMI = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001")
SXD_ARB = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001")
MARG2025 = os.path.join(ROOT, "data", "corrida0", "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001", "resultados.json")
FIRMAS = os.path.join(ROOT, "forense", "firmas-pendientes.tsv")
ZIP23 = os.path.join(ROOT, "data", "raw", "envipe2023_csv.zip")
ZIP24 = os.path.join(ROOT, "data", "raw", "envipe2024_csv.zip")
ZIP25 = os.path.join(ROOT, "data", "raw", "envipe2025_csv.zip")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = _load(os.path.join(EMI, "medidor.py"), "p4_medidor")
A = _load(os.path.join(ARB, "adjudicacion.py"), "p4_adjudicacion")


def _repo(path):
    return {"ruta_absoluta": path, "bytes": open(path, "rb").read(),
           "sha256": hashlib.sha256(open(path, "rb").read()).hexdigest()}


def _contrato(ola_reservada, replicas, seed):
    return {"parametros": {"ola_reservada": ola_reservada, "bootstrap_replicas": replicas,
                           "n_minimo_celda": 200, "control_arbitro_tol_p": 1e-6,
                           "control_arbitro_tol_ic": 1e-6,
                           "umbral_celdas_gana_fraccion": 0.75,
                           "delta_mae_umbral_pp": 0.5,
                           "criterio_indecidible_verbatim": ("INDECIDIBLE si ambos caen dentro del "
                                                             "IC de R o si |d_L-d_M| < 0.5*EE(R)"),
                           "criterio_indecidible_fuente": "forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38"},
           "seed": {"aplica": True, "valor": seed}}


# ────────────────────────────── fixture sintético ──────────────────────────────

def _fixture_zip(tmp_path, anio, n_delitos=2600, seed=7):
    """`tmod_vic`+`tsdem` sintéticos con los cuatro ejes representados y BP1_20/
    BP1_23 dentro del universo, para que `_y` (evade_norma) tenga variación
    real por celda de los cuatro cruces."""
    rng = np.random.default_rng(seed + int(anio))
    filas_t, filas_p = [], []
    n_personas = n_delitos // 2 + 50
    edades = rng.choice([22, 35, 50, 70, 97], size=n_personas, p=[.24, .27, .24, .22, .03])
    nivs = rng.choice(["01", "03", "05", "08"], size=n_personas)
    sexos = rng.choice(["1", "2"], size=n_personas)
    dominios = rng.choice(["U", "C", "R"], size=n_personas, p=[.55, .25, .20])
    for i in range(n_personas):
        idp = f"P{i:05d}"
        est = f"{1 + i % 4:02d}"
        upm = f"{i % 30:03d}"
        filas_p.append(f"{idp},{edades[i]},{nivs[i]},{est},{upm}")
    for j in range(n_delitos):
        i = j % n_personas
        idp = f"P{i:05d}"
        idd = f"D{j:05d}"
        est = f"{1 + i % 4:02d}"
        upm = f"{i % 30:03d}"
        bp1_20 = "2" if rng.random() < 0.75 else "1"
        # sesga bp1_23 por NIV/edad para que haya variacion de celda real
        p_inutil = 0.35 + 0.10 * (nivs[i] == "08") + 0.08 * (edades[i] < 45)
        bp1_23 = rng.choice(["04", "05", "06", "08", "01", "09"],
                            p=np.array([p_inutil * .3, p_inutil * .25, p_inutil * .25,
                                       p_inutil * .2, (1 - p_inutil) * .6,
                                       (1 - p_inutil) * .4]) / 1.0) if bp1_20 == "2" else "b"
        fac = 100 + int(rng.integers(0, 80))
        filas_t.append(f"{idd},{idp},{bp1_20},{bp1_23},{fac},{est},{upm},"
                       f"{dominios[i]},{sexos[i]},{edades[i]}")
    tmod = ("ID_DEL,ID_PER,BP1_20,BP1_23,FAC_DEL,EST_DIS,UPM_DIS,DOMINIO,SEXO,EDAD\n"
           + "\n".join(filas_t) + "\n")
    tsdem = "ID_PER,NIV\n" + "\n".join(f"{f'P{i:05d}'},{nivs[i]}" for i in range(n_personas)) + "\n"
    z = tmp_path / f"envipe{anio}_sintetico.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(f"conjunto_de_datos_tmod_vic_envipe{anio}.csv", tmod)
        zf.writestr(f"conjunto_de_datos_tsdem_envipe{anio}.csv", tsdem)
    return str(z)


def _marginales_2025_sinteticos(tmp_path, seed=11):
    """Un JSON sellado sintético con los 13 marginales + nacional, con el
    mismo esquema de ids que `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`."""
    rng = np.random.default_rng(seed)
    r = {}
    for (eje, cat), rid in M.IDS_MARGINALES_2025.items():
        p = float(rng.uniform(0.35, 0.65))
        r[f"{rid}-P"] = p
        r[f"{rid}-IC-LO"] = max(0.001, p - 0.03)
        r[f"{rid}-IC-HI"] = min(0.999, p + 0.03)
        r[f"{rid}-N"] = int(rng.integers(500, 3000))
        r[f"{rid}-DEN-W"] = float(rng.integers(1_000_000, 9_000_000))
        r[f"{rid}-B-VALIDAS"] = 200
    r[f"{M.NACIONAL_ID}-P"] = 0.5
    r[f"{M.NACIONAL_ID}-IC-LO"] = 0.48
    r[f"{M.NACIONAL_ID}-IC-HI"] = 0.52
    r[f"{M.NACIONAL_ID}-N"] = 8000
    path = tmp_path / "marginales2025.json"
    path.write_text(json.dumps({"resultados": r}), encoding="utf-8")
    return str(path)


def _firmas(tmp_path, estado_a="FIRMADA", estado_b="FIRMADA"):
    t = "id\tqué_se_firma\tdónde\tcreado\tgatea\testado\tfirmada_en\tejecutada_en\tencargo\n"
    t += f"{M.FP_A}\t§2\tnota\t2026-09-22\tCOMMIT-1\t{estado_a}\t\t\tencargo\n"
    t += f"{M.FP_B}\t§6\tnota\t2026-09-22\tCOMMIT-1\t{estado_b}\t\t\tencargo\n"
    p = tmp_path / "firmas.tsv"
    p.write_text(t, encoding="utf-8")
    return str(p)


def _inputs_sinteticos(tmp_path, estado_a="FIRMADA", estado_b="FIRMADA"):
    z23 = _fixture_zip(tmp_path, 2023, seed=101)
    z24 = _fixture_zip(tmp_path, 2024, seed=202)
    z25 = _fixture_zip(tmp_path, 2025, seed=303)
    marg = _marginales_2025_sinteticos(tmp_path)
    firmas = _firmas(tmp_path, estado_a, estado_b)
    return {
        "envipe2023_csv": {"ruta_absoluta": z23, "sha256": hashlib.sha256(open(z23, "rb").read()).hexdigest()},
        "envipe2024_csv": {"ruta_absoluta": z24, "sha256": hashlib.sha256(open(z24, "rb").read()).hexdigest()},
        "envipe2025_csv": {"ruta_absoluta": z25, "sha256": hashlib.sha256(open(z25, "rb").read()).hexdigest()},
        "marginales_2025_resultados": _repo(marg),
        "firmas_pendientes_tsv": _repo(firmas),
    }


# ────────────────────────────── (a) sintética ──────────────────────────────

def test_a_medir_punta_a_punta_sintetico(tmp_path):
    inputs = _inputs_sinteticos(tmp_path)
    con = _contrato(2025, 300, 13)
    out = M.medir(inputs, con)
    ids = {f["id"] for f in M.esquema_resultados()}
    faltan, sobran = ids - set(out), set(out) - ids
    assert not faltan and not sobran, (faltan, sobran)
    for cruce_id in M.CRUCES:
        pre = M.prefijo(cruce_id)
        assert 0.0 <= out[f"{pre}-G-LAMBDA"] <= 1.0, cruce_id
        for ka, kb in M.celdas(cruce_id):
            base = f"{pre}-{M.celda_corta(cruce_id, ka, kb)}"
            for cid in ("C2", "C7", "C-ENCOGIDA"):
                p = out[f"{base}-{cid}-P"]
                if p is not None:
                    assert 0.0 < p < 1.0, (base, cid, p)


def test_a_adjudicacion_sobre_r_sintetico(tmp_path):
    inputs = _inputs_sinteticos(tmp_path)
    con = _contrato(2025, 300, 13)
    emis = M.medir(inputs, con)
    res_path = tmp_path / "resultados.json"
    res_path.write_text(json.dumps({"resultados": emis}), encoding="utf-8")
    sello = {"resultados.json": hashlib.sha256(res_path.read_bytes()).hexdigest()}
    sello_path = tmp_path / "sello.json"
    sello_path.write_text(json.dumps(sello), encoding="utf-8")
    # R sintetico: mismo zip de 2025 pero abierto SIN reserva por el arbitro
    inputs2 = dict(inputs, emisiones_resultados=_repo(str(res_path)),
                  emisiones_sello=_repo(str(sello_path)))
    out = A.medir(inputs2, con)
    for cruce_id in A.M.CRUCES:
        pre = A.prefijo(cruce_id)
        assert out[f"{pre}-G-B-BIS"].split("+")[0] in (
            "CORROBORADA", "FALSADOR-DEBIL", "LIMITA-C2", "LIMITA-C2-SOBRE-CUANTO-ENCOGER",
            "FUERA-DE-SOPORTE-GLOBAL", "INDECIDIBLE"), cruce_id
    ids = {f["id"] for f in A.esquema_resultados()}
    faltan, sobran = ids - set(out), set(out) - ids
    assert not faltan and not sobran, (faltan, sobran)
    with pytest.raises(A.ParoDeGuardia):
        A.medir(inputs, con)


# ────────────────────────────── (c) guardias y reserva ──────────────────────────────

def test_c_guardias_paran(tmp_path):
    con = _contrato(2025, 50, 1)
    inputs = _inputs_sinteticos(tmp_path, estado_a="ABIERTA")
    with pytest.raises(M.ParoDeGuardia, match="a5a0-01"):
        M.medir(inputs, con)
    inputs2 = _inputs_sinteticos(tmp_path, estado_b="ABIERTA")
    with pytest.raises(M.ParoDeGuardia, match="a5a0-02"):
        M.medir(inputs2, con)


def test_c_fp_firmadas_en_el_repo():
    assert M._fp_estado(open(FIRMAS, "rb").read(), M.FP_A) == "FIRMADA"
    assert M._fp_estado(open(FIRMAS, "rb").read(), M.FP_B) == "FIRMADA"


def test_c_reserva_envipe2025_cruce_no_abierto():
    for d in (EMI, ARB):
        for f in ("ejecucion.json", "resultados.json", "sello.json", "sello.sha256"):
            assert not os.path.exists(os.path.join(d, f)), f"{d}/{f} existe: COMMIT-1 no emite"
    tracked = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout.split(b"\0")
    for rel in tracked:
        if not rel or not rel.endswith((b".json", b".tsv")):
            continue
        if b"forense/encargos/" in rel or rel.endswith(b"test_piloto4_v1_0.py"):
            continue
        try:
            data = open(os.path.join(ROOT, rel.decode()), "rb").read()
        except FileNotFoundError:
            continue
        assert b"RESULT-TRA-ENCOGIDA-" not in data or b"marcador-segmento" in rel, rel
    src = open(os.path.join(EMI, "medidor.py"), encoding="utf-8").read()
    assert "envipe2025_csv.zip" not in src


# ────────────────────────────── (d) λ, por cada cruce ──────────────────────────────

def test_d_lambda_se_rederiva_por_cruce(tmp_path):
    inputs = _inputs_sinteticos(tmp_path)
    con = _contrato(2025, 300, 13)
    out = M.medir(inputs, con)
    for cruce_id in M.CRUCES:
        pre = M.prefijo(cruce_id)
        dbar, var = [], []
        for ka, kb in M.celdas(cruce_id):
            base = f"{pre}-{M.celda_corta(cruce_id, ka, kb)}"
            i23, i24 = out[f"{base}-I23"], out[f"{base}-I24"]
            ee23, ee24 = out[f"{base}-I23-EE"], out[f"{base}-I24-EE"]
            if None in (i23, i24, ee23, ee24):
                continue
            dbar.append((i23 + i24) / 2.0)
            var.append((ee23 ** 2 + ee24 ** 2) / 4.0)
        if len(dbar) < 2:
            continue
        var_entre = float(np.var(dbar, ddof=1))
        sigma2 = float(np.mean(var))
        tau2 = max(0.0, var_entre - sigma2)
        lam = tau2 / (tau2 + sigma2) if (tau2 + sigma2) > 0 else 0.0
        assert abs(lam - out[f"{pre}-G-LAMBDA"]) < 1e-12, (cruce_id, lam, out[f"{pre}-G-LAMBDA"])
        assert abs(tau2 - out[f"{pre}-G-LAMBDA-TAU2"]) < 1e-12, cruce_id
        assert abs(sigma2 - out[f"{pre}-G-LAMBDA-SIGMA-BAR2"]) < 1e-12, cruce_id


# ────────────────────────────── (b) control sobre el cruce ya sellado del piloto 2 ──────────────────────────────

@pytest.mark.skipif(not os.path.exists(ZIP23), reason="corpus no montado (NUBE): control solo en CAJA")
def test_b_control_reproduce_piloto2_escolaridad_x_dominio():
    sel_emi = json.load(open(os.path.join(SXD_EMI, "resultados.json")))["resultados"]
    sel_arb = json.load(open(os.path.join(SXD_ARB, "resultados.json")))["resultados"]
    ola24 = M.mr.carga_ola(ZIP24, 2024, reservada=False)
    x24 = M.mr.cruce(ola24, "escolaridad_proxy", "dominio_urbano_rural")
    S_ROT_INV = {v: k for k, v in M.mr.ESC_ROTULO.items()}
    D_ROT_INV = {v: k for k, v in M.mr.DOM_ROTULO.items()}
    peor = 0.0
    for (esc, dom), cel in x24["celdas"].items():
        c = f"{S_ROT_INV[esc]}x{D_ROT_INV[dom]}"
        assert cel["n"] == sel_emi[f"RESULT-TRA-SXD12-C1-N-{c}"], c
        peor = max(peor, abs(cel["p"] - sel_emi[f"RESULT-TRA-SXD12-C1-P-{c}"]))
    assert peor < 1e-10, peor
    ola25 = M.mr.carga_ola(ZIP25, 2025, reservada=False)
    x25 = M.mr.cruce(ola25, "escolaridad_proxy", "dominio_urbano_rural")
    peor25 = 0.0
    for (esc, dom), cel in x25["celdas"].items():
        c = f"{S_ROT_INV[esc]}x{D_ROT_INV[dom]}"
        peor25 = max(peor25, abs(cel["n"] - sel_arb[f"RESULT-TRA-SXD12-ARB-R-N-{c}"]))
    assert peor25 < 1, peor25
