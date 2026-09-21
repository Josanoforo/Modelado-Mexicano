#!/usr/bin/env python3
"""Piloto 3 · COMMIT-1 v1.3 · el conducto que sella acepta la salida de cada rama
(ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_3, 21/sep/2026).

`#951` probó que un CALC con preflight VERDE y pytest 7/7 puede no sellar:
`corrida0._valida_outputs` rechaza todo `null` sin `permite_no_estimable: true`.
Aquí, con el `spec.yaml` ya declarado (P1), se pasa por ESE validador —no por una
copia— la salida de cada camino terminal del código congelado:

  1. EMISIONES sobre sintético;
  2. EMISIONES sobre oro 2023 (se salta si el corpus no está montado);
  3. ADJUDICACION, todas las celdas con soporte;
  4. ADJUDICACION, soporte parcial (dos celdas FUERA-DE-SOPORTE por n sellado);
  5. ADJUDICACION, FUERA-DE-SOPORTE global con celdas puntuadas;
  6. ADJUDICACION, cero celdas puntuadas;
  7. ADJUDICACION, celda rara: pocos trámites en 3 UPM, réplicas suficientes para
     que alguna la vacíe (se verifica `-R-B-VALIDAS` < réplicas, o la rama no se
     ejercitó);
  8. ADJUDICACION sobre oro 2023 como R (el código lo admite; se salta sin corpus).

Aserción en cada uno: `_valida_outputs` vacía y cero valores no finitos (NaN, ±inf)
—un nulo declarado es aceptable; un no finito nunca (PARO c del encargo)—.
Los fixtures del control C2 se construyen desde los ids REALES del `resultados.json`
sellado de CALC-C2-COMPUESTO-RESERVADAS-0001, no desde la clave del medidor.
"""
import hashlib
import importlib.util
import json
import math
import os
import sys
import zipfile

import numpy as np
import pytest
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_piloto3_v11 as T  # noqa: E402  (fixtures sintéticos y módulos M/A ya cargados)

M, A = T.M, T.A
ROOT = T.ROOT
_spec = importlib.util.spec_from_file_location("corrida0_conducto", os.path.join(ROOT, "tools", "corrida0.py"))
C0 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C0)

SPEC_E = yaml.safe_load(open(os.path.join(T.EMI, "spec.yaml"), encoding="utf-8"))
SPEC_A = yaml.safe_load(open(os.path.join(T.ADJ, "spec.yaml"), encoding="utf-8"))
PE25, PA25 = M.prefijo("2025"), A.prefijo("2025")


def _remap(out, ola):
    """Los ids del spec.yaml llevan la ola 2025; la salida sintética/oro lleva otra."""
    pe, pa = M.prefijo(ola), A.prefijo(ola)
    return {k.replace(pe, PE25, 1).replace(pa, PA25, 1): v for k, v in out.items()}


def _no_finitos(out):
    return sorted(k for k, v in out.items()
                  if isinstance(v, (float, np.floating)) and not math.isfinite(v))


def _acepta(spec, out, ola):
    """El validador que sella, contra el spec declarado. Devuelve los ids nulos."""
    problemas = C0._valida_outputs(spec, _remap(out, ola))
    assert problemas == [], problemas
    assert _no_finitos(out) == [], _no_finitos(out)
    return sorted(k for k, v in out.items() if v is None)


def _control_desde_sellado(tmp_path):
    """Fixture del control con los ids REALES del CALC sellado (no la clave del
    medidor): así el rótulo `-60-X-` de la casa entra tal cual y el medidor
    emite None en la banda 60-96, como sobre el dato real (#951)."""
    real = json.load(open(T.CTL, encoding="utf-8"))["resultados"]
    ctl = {k: v for k, v in real.items() if k.startswith(M.PREFIJO_CONTROL + "-")}
    assert len(ctl) == 16, len(ctl)
    p = tmp_path / "control_real_ids.json"
    p.write_text(json.dumps({"resultados": ctl}), encoding="utf-8")
    return str(p)


def _inputs(tmp_path, n_bajo=()):
    """Inputs sintéticos; `n_bajo` = celdas cuyo n sellado de 2021 baja de 200
    (FUERA-DE-SOPORTE por historia)."""
    inp = T._inputs_sinteticos(tmp_path)
    inp["c2_compuesto_resultados"] = T._repo(_control_desde_sellado(tmp_path))
    if n_bajo:
        doc = json.loads(inp["encig2021_cruces_resultados"]["bytes"])
        for a, b in n_bajo:
            doc["resultados"][f"{M.PREFIJO_SELLADO['2021']}-{a}-{b}-N"] = 150
        p = tmp_path / "sellado2021_bajo.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        inp["encig2021_cruces_resultados"] = T._repo(str(p))
    return inp


def _adjudica(tmp_path, inp, con):
    emis = M.medir(inp, con)
    rp = tmp_path / "resultados.json"
    rp.write_text(json.dumps({"resultados": emis}), encoding="utf-8")
    sp = tmp_path / "sello.json"
    sp.write_text(json.dumps({"resultados.json": hashlib.sha256(rp.read_bytes()).hexdigest()}), encoding="utf-8")
    adj = A.medir(dict(inp, emisiones_resultados=T._repo(str(rp)), emisiones_sello=T._repo(str(sp))), con)
    return emis, adj


# ────────────────────────────── 1 · EMISIONES sintético ──────────────────────────────

def test_1_emisiones_sintetico_sella(tmp_path):
    out = M.medir(_inputs(tmp_path), T._contrato("2099", "sintetico_csv", 300, 11))
    nulos = _acepta(SPEC_E, out, "2099")
    # con el control REAL: 32 C1A-IC + 4 controles 60-96 + 4 |C2−control| = 40, como en #951
    assert len(nulos) == 40, nulos
    assert all(("C1A-P-IC" in k) or ("-60-96-" in k and ("CONTROL" in k)) for k in nulos), nulos


# ────────────────────────────── 3..6 · ADJUDICACION, ramas de soporte ──────────────────────────────

def test_3_adjudicacion_todas_con_soporte(tmp_path):
    inp = _inputs(tmp_path)
    con = T._contrato("2099", "sintetico_csv", 300, 11)
    emis, adj = _adjudica(tmp_path, inp, con)
    _acepta(SPEC_E, emis, "2099")
    nulos = _acepta(SPEC_A, adj, "2099")
    assert adj[f"{A.prefijo('2099')}-PUNTUADAS-N"] == 15 and adj[f"{A.prefijo('2099')}-SOPORTE-GLOBAL"] == "CON-SOPORTE"
    assert nulos == [], nulos


def test_4_adjudicacion_soporte_parcial(tmp_path):
    bajas = [("30-44", "SUPERIOR"), ("45-59", "SECUNDARIA")]
    inp = _inputs(tmp_path, n_bajo=bajas)
    con = T._contrato("2099", "sintetico_csv", 300, 11)
    emis, adj = _adjudica(tmp_path, inp, con)
    _acepta(SPEC_E, emis, "2099")
    nulos = _acepta(SPEC_A, adj, "2099")
    P = A.prefijo("2099")
    assert adj[f"{P}-PUNTUADAS-N"] == 13 and adj[f"{P}-SOPORTE-FALLAN"] == 2 and adj[f"{P}-SOPORTE-GLOBAL"] == "CON-SOPORTE"
    for a, b in bajas:
        assert adj[f"{P}-{a}-{b}-SOPORTE"] == "FUERA-DE-SOPORTE"
        assert adj[f"{P}-{a}-{b}-S-MEDIO-VS-C2"] == "NO-PUNTUADA"
    assert nulos == [], nulos


def test_5_adjudicacion_fuera_de_soporte_global_con_puntuadas(tmp_path):
    bajas = [c for c in M.CELDAS if c not in M.FUERA_DE_SOPORTE_EX_ANTE][:5]
    inp = _inputs(tmp_path, n_bajo=bajas)
    con = T._contrato("2099", "sintetico_csv", 300, 11)
    emis, adj = _adjudica(tmp_path, inp, con)
    _acepta(SPEC_E, emis, "2099")
    nulos = _acepta(SPEC_A, adj, "2099")
    P = A.prefijo("2099")
    assert adj[f"{P}-SOPORTE-GLOBAL"] == "FUERA-DE-SOPORTE-GLOBAL" and adj[f"{P}-PUNTUADAS-N"] == 10
    assert adj[f"{P}-B-BIS"].startswith("FUERA-DE-SOPORTE-GLOBAL")
    assert nulos == [], nulos


def test_6_adjudicacion_cero_puntuadas(tmp_path):
    bajas = [c for c in M.CELDAS if c not in M.FUERA_DE_SOPORTE_EX_ANTE]
    inp = _inputs(tmp_path, n_bajo=bajas)
    con = T._contrato("2099", "sintetico_csv", 300, 11)
    emis, adj = _adjudica(tmp_path, inp, con)
    _acepta(SPEC_E, emis, "2099")
    nulos = _acepta(SPEC_A, adj, "2099")
    P = A.prefijo("2099")
    assert adj[f"{P}-PUNTUADAS-N"] == 0 and adj[f"{P}-UMBRAL-VENCER-N"] is None
    # 14 nulos: MAE/ΔMAE de retadores y C2 (11), MAE de C1A/C1B (2), umbral (1)
    assert len(nulos) == 14, nulos
    assert all("MAE" in k or k.endswith("UMBRAL-VENCER-N") for k in nulos), nulos


# ────────────────────────────── 7 · celda rara ──────────────────────────────

def _fixture_rara(tmp_path, n=7000, seed=7, upms_raras=(0, 1, 2), ola="2099"):
    """Como `T._fixture_zip`, pero la celda 18-29 × HASTA-PRIMARIA sólo existe en
    tres UPM: una réplica del bootstrap que no sortea ninguna de las tres la
    vacía (medidor.py:283 → resumen() devuelve None, :291)."""
    rng = np.random.default_rng(seed)
    fp, ft = [], []
    for i in range(n):
        est = f"{1 + i % 3:02d}"
        upm = f"{i % 24:03d}"
        edad = int(rng.choice([22, 35, 50, 70, 97, 98, 99], p=[.22, .28, .25, .21, .015, .02, .005]))
        niv = str(int(rng.choice([1, 3, 5, 8])))
        if edad == 22 and niv == "1" and (i % 24) not in upms_raras:
            niv = "3"
        idp = f"P{i:05d}"
        fp.append(f"{idp},{edad},{niv},{est},{upm}")
        p = 0.35 + 0.15 * (niv == "8") + 0.1 * (edad < 45)
        w = np.array([.25, .15, p * .6, p * .4, .05, .03, .02])
        canal = str(int(rng.choice([1, 2, 4, 5, 6, 3, 9], p=w / w.sum())))
        ntra = "01" if rng.random() < 0.9 else "03"
        ft.append(f"{idp},{ntra},{canal},{100 + int(rng.integers(0, 50))},{est},{upm}")
    z = tmp_path / f"encig{ola}_rara.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(f"conjunto_de_datos_encig{ola}_04_sec_7.csv",
                    "ID_PER,N_TRA,P7_3,FAC_TRA,EST_DIS,UPM_DIS\n" + "\n".join(ft) + "\n")
        zf.writestr(f"conjunto_de_datos_encig{ola}_02_residentes_sec_2.csv",
                    "ID_PER,EDAD,NIV,EST_DIS,UPM_DIS\n" + "\n".join(fp) + "\n")
    return str(z)


def test_7_adjudicacion_celda_rara_vaciada_por_una_replica(tmp_path):
    reps = 2000
    inp = _inputs(tmp_path)
    inp["sintetico_csv"] = {"ruta_absoluta": _fixture_rara(tmp_path)}
    con = T._contrato("2099", "sintetico_csv", reps, 11)
    emis, adj = _adjudica(tmp_path, inp, con)
    _acepta(SPEC_E, emis, "2099")
    nulos = _acepta(SPEC_A, adj, "2099")
    P = A.prefijo("2099")
    rara = f"{P}-18-29-HASTA-PRIMARIA"
    validas = adj[f"{rara}-R-B-VALIDAS"]
    assert validas < reps, f"la rama no se ejercitó: {validas} réplicas válidas de {reps}"
    assert adj[f"{rara}-R-P"] is not None and 0 < adj[f"{rara}-N-2025"] < 200
    assert nulos == [f"{rara}-R-P-EE", f"{rara}-R-P-IC-HI", f"{rara}-R-P-IC-LO"], nulos
    # las marginales de una variable NO se vacían: el resto del cruce sella entero
    assert adj[f"{P}-SOPORTE-GLOBAL"] == "CON-SOPORTE" and adj[f"{P}-PUNTUADAS-N"] == 15


# ────────────────────────────── 2 y 8 · oro 2023 ──────────────────────────────

@pytest.mark.skipif(not os.path.exists(T.ZIP23), reason="corpus no montado (NUBE): oro sólo en CAJA")
def test_2_y_8_oro_2023_emisiones_y_adjudicacion_sellan(tmp_path):
    inp = {
        "encig23_base_datos_csv": {"ruta_absoluta": T.ZIP23},
        "encig2021_cruces_resultados": T._repo(T.SELL21),
        "encig2023_cruces_resultados": T._repo(T.SELL23),
        "c2_compuesto_resultados": T._repo(T.CTL),
        "firmas_pendientes_tsv": T._repo(T.FIRMAS),
    }
    con = T._contrato("2023", "encig23_base_datos_csv", 10000, 20260919)
    emis, adj = _adjudica(tmp_path, inp, con)
    nulos_e = _acepta(SPEC_E, emis, "2023")
    assert len(nulos_e) == 40, nulos_e   # 32 C1A-IC + 8 de la banda 60-96 (control rotulado -60-X-)
    nulos_a = _acepta(SPEC_A, adj, "2023")
    P = A.prefijo("2023")
    assert adj[f"{P}-PUNTUADAS-N"] == 15 and adj[f"{P}-SOPORTE-GLOBAL"] == "CON-SOPORTE"
    for a, b in M.CELDAS:
        assert adj[f"{P}-{a}-{b}-R-B-VALIDAS"] == 10000
    assert nulos_a == [], nulos_a
