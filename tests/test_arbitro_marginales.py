#!/usr/bin/env python3
"""ACTO GEN2-ARBITRO-MARGINALES-1 · COMMIT-1 de las tres piezas (21/sep/2026).

«Congelado» es D-22 ampliada, demostrada aquí para cada CALC
(`CALC-ARBITRO-MARGINALES-{ENIF2024,ENVIPE2025,ENCIG2025}-0001`):

  1. GUARDIA · la auditoría AST del medidor PASA sobre el archivo real y cada
     regla tiene su control positivo (mutación que la dispara); la guardia de
     tiempo de corrida rechaza una lista de ejes, un eje fuera de lista y un
     insumo de la ola reservada con `ola` distinta.
  2. SINTÉTICO · con un zip fabricado con la forma de la ola NUEVA (miembros y
     nemónicos de 2024/2025) `medir()` devuelve exactamente los ids declarados
     en `spec.yaml`, `corrida0._valida_outputs` sale vacía y no hay no finitos;
     la rama de categoría vacía (`None` en -P/-IC-LO/-IC-HI) también pasa por
     el validador.
  3. ORO · el mismo punto de entrada con `ola` = ola anterior reproduce el piso
     sellado (Δ = 0 en cada RESULT compartido, IC incluidos). Se salta si el
     corpus no está montado.
  4. IDENTIDAD · `ARBITRO-MARGINALES-metadatos-v1_0.tsv` enlaza 1:1 las 57 filas
     `SOLO-PISO` del marcador con ids que cada spec declara.

Defecto real que atrapa: #941/#951 (preflight VERDE + pytest verde y `run` no
sella por `null` no declarado y por ids que el spec no lista) y el de
`feedback_bootstrap_marco_entero` (IC que se van 2e-3 si el marco se recorta
antes de sortear: sólo el oro sobre la ola anterior lo delata).
"""
from __future__ import annotations

import importlib.util
import io
import json
import math
import os
import sys
import zipfile

import numpy as np
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C0DIR = os.path.join(ROOT, "data", "corrida0")
RAW = os.path.join(ROOT, "data", "raw")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


C0 = _load(os.path.join(ROOT, "tools", "corrida0.py"), "corrida0_arbitro_test")

PIEZAS = {
    "ENIF2024": dict(
        calc="CALC-ARBITRO-MARGINALES-ENIF2024-0001", piso="CALC-PISOS-ENIF2021-EJES-0003",
        piso_input="MEDIDOR-PISO-EJES-0003", ola_oro="2021", ola="2024",
        payload_oro="enif2021_csv", zip_oro="enif2021_csv.zip", payload="enif_2024_enif_2024_bd_csv",
        pref_oro="RESULT-PISOS-ENIF2021-V2-", pref_R="RESULT-ARBITRO-ENIF",
        oro_extra=("CALC-PISOS-ENIF2021-FORMALIDAD-0001", "RESULT-PISOS-ENIF2021-FORMALIDAD-", "-FORMALIDAD-"),
    ),
    "ENVIPE2025": dict(
        calc="CALC-ARBITRO-MARGINALES-ENVIPE2025-0001", piso="CALC-PISOS-ENVIPE2024-EJES-0002",
        piso_input="MEDIDOR-PISO-EJES-0002", ola_oro="2024", ola="2025",
        payload_oro="envipe2024_csv", zip_oro="envipe2024_csv.zip", payload="envipe2025_csv",
        pref_oro="RESULT-PISOS-ENVIPE2024-V2-", pref_R="RESULT-ARBITRO-ENVIPE", oro_extra=None,
    ),
    "ENCIG2025": dict(
        calc="CALC-ARBITRO-MARGINALES-ENCIG2025-0001", piso="CALC-PISOS-ENCIG2023-EJES-0002",
        piso_input="MEDIDOR-PISO-EJES-0002", ola_oro="2023", ola="2025",
        payload_oro="encig23_base_datos_csv", zip_oro="encig23_base_datos_csv.zip", payload="encig25_base_datos_csv",
        pref_oro="RESULT-PISOS-ENCIG2023-V2-", pref_R="RESULT-ARBITRO-ENCIG", oro_extra=None,
    ),
}
MODS = {k: _load(os.path.join(C0DIR, p["calc"], "medidor.py"), f"medidor_arbitro_{k}") for k, p in PIEZAS.items()}
SPECS = {k: yaml.safe_load(open(os.path.join(C0DIR, p["calc"], "spec.yaml"), encoding="utf-8"))
         for k, p in PIEZAS.items()}


def _inputs(k, ola, ruta_zip):
    p = PIEZAS[k]
    payload = p["payload"] if ola == p["ola"] else p["payload_oro"]
    return {payload: {"ruta_absoluta": str(ruta_zip)},
            p["piso_input"]: {"ruta_absoluta": os.path.join(C0DIR, p["piso"], "medidor.py")}}


def _contrato(k, ola, reps=200):
    c = C0.contrato_ejecutable(SPECS[k])
    c["parametros"] = dict(c["parametros"], ola=ola, bootstrap_replicas=reps)
    return c


def _remap(k, out, ola):
    p = PIEZAS[k]
    return {key.replace(f"{p['pref_R']}{ola}-", f"{p['pref_R']}{p['ola']}-", 1): v for key, v in out.items()}


def _no_finitos(out):
    return sorted(key for key, v in out.items()
                  if isinstance(v, (float, np.floating)) and not math.isfinite(v))


def _acepta(k, out, ola):
    problemas = C0._valida_outputs(SPECS[k], _remap(k, out, ola))
    assert problemas == [], problemas
    assert _no_finitos(out) == []
    return sorted(key for key, v in out.items() if v is None)


# ═══════════════════════════ sintéticos con la forma de la ola nueva ══════

def _csv_bytes(cols, rows):
    buf = io.StringIO()
    buf.write(",".join(cols) + "\n")
    for r in rows:
        buf.write(",".join(str(r[c]) for c in cols) + "\n")
    return buf.getvalue().encode("utf-8")


def _diseno(rng, n, n_est=4, upm_por_est=6):
    est = rng.integers(1, n_est + 1, n)
    upm = est * 100 + rng.integers(1, upm_por_est + 1, n)
    w = rng.uniform(50, 800, n).round(2)
    return est, upm, w


def _zip_enif2024(path, n=900, seed=1, sin_mujeres=False):
    rng = np.random.default_rng(seed)
    est, upm, w = _diseno(rng, n)
    rows = []
    for i in range(n):
        r = {}
        for j in range(1, 7):
            r[f"P5_1_{j}"] = rng.choice(["1", "2", "2", "2", "9", ""], p=[.3, .4, .1, .1, .05, .05])
        for j in range(1, 10):
            tiene = rng.choice(["1", "2", "2", ""], p=[.4, .3, .2, .1])
            r[f"P5_4_{j}"] = tiene
            r[f"P5_6_{j}"] = rng.choice(["1", "2"]) if tiene == "1" else ""
        r["SEXO"] = "1" if sin_mujeres else rng.choice(["1", "2"])
        r["EDAD_V"] = str(int(rng.integers(18, 99)))
        r["NIV"] = f"{int(rng.integers(0, 12)):02d}"
        r["TLOC"] = rng.choice(["1", "2", "3", "4"])
        r["P3_13"] = rng.choice(["1", "2", "3", "4", "5", "6", "7", "9", ""], p=[.2, .05, .05, .05, .05, .05, .25, .05, .25])
        r["FAC_PER"] = w[i]; r["EST_DIS"] = f"{est[i]:03d}"; r["UPM_DIS"] = f"{upm[i]:06d}"
        rows.append(r)
    cols = list(rows[0].keys())
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("TMODULO.csv", _csv_bytes(cols, rows))
        zf.writestr("catalogos/dummy.txt", b"x")
    return path


def _zip_envipe2025(path, n=1200, seed=2, sin_rural=False):
    rng = np.random.default_rng(seed)
    est, upm, w = _diseno(rng, n)
    vic, dem = [], []
    for i in range(n):
        pid = f"P{i // 2:05d}"           # dos delitos por persona (m:1)
        vic.append({"BP1_20": rng.choice(["1", "2", "2", "9"], p=[.3, .3, .3, .1]),
                    "BP1_23": f"{int(rng.integers(1, 10)):02d}",
                    "BP2_1": rng.choice(["1", "2", ""], p=[.2, .3, .5]),
                    "BPCOD": rng.choice(["01", "02", "05"], p=[.3, .4, .3]),
                    "FAC_DEL": w[i], "EST_DIS": f"{est[i]:03d}", "UPM_DIS": f"{upm[i]:06d}",
                    "ID_PER": pid, "SEXO": rng.choice(["1", "2"]), "EDAD": str(int(rng.integers(18, 99))),
                    "DOMINIO": "U" if sin_rural else rng.choice(["R", "C", "U"])})
    for i in range(0, n, 2):
        dem.append({"ID_PER": f"P{i // 2:05d}", "NIV": f"{int(rng.integers(0, 10)):02d}"})
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("conjunto_de_datos/conjunto_de_datos_tmod_vic_envipe2025.csv", _csv_bytes(list(vic[0]), vic))
        zf.writestr("conjunto_de_datos/conjunto_de_datos_tsdem_envipe2025.csv", _csv_bytes(list(dem[0]), dem))
    return path


def _zip_encig2025(path, n=1500, seed=3, sin_superior=False):
    rng = np.random.default_rng(seed)
    est, upm, w = _diseno(rng, n)
    ev, pe = [], []
    for i in range(n):
        pid = f"P{i // 3:05d}"           # tres trámites por persona (m:1)
        ev.append({"N_TRA": rng.choice(["01", "01", "02", "07"]),
                   "P7_3": rng.choice(["1", "2", "3", "4", "5", "6", "7", ""], p=[.2, .2, .05, .2, .1, .1, .05, .1]),
                   "FAC_TRA": w[i], "EST_DIS": f"{est[i]:03d}", "UPM_DIS": f"{upm[i]:06d}", "ID_PER": pid})
    for i in range(0, n, 3):
        pe.append({"ID_PER": f"P{i // 3:05d}", "SEXO": rng.choice(["1", "2"]),
                   "EDAD": str(int(rng.choice([25, 40, 50, 70, 97, 98, 99], p=[.3, .25, .2, .15, .05, .03, .02]))),
                   "NIV": str(int(rng.integers(0, 8))) if sin_superior else str(int(rng.integers(0, 10)))})
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("conjunto_de_datos/encig2025_04_sec_7.csv", _csv_bytes(list(ev[0]), ev))
        zf.writestr("conjunto_de_datos/encig2025_02_residentes_sec_2.csv", _csv_bytes(list(pe[0]), pe))
    return path


SINTETICOS = {"ENIF2024": _zip_enif2024, "ENVIPE2025": _zip_envipe2025, "ENCIG2025": _zip_encig2025}
VACIA = {"ENIF2024": dict(sin_mujeres=True), "ENVIPE2025": dict(sin_rural=True), "ENCIG2025": dict(sin_superior=True)}
ID_VACIO = {"ENIF2024": "RESULT-ARBITRO-ENIF2024-D9-SEXO-2-P",
            "ENVIPE2025": "RESULT-ARBITRO-ENVIPE2025-EVASION-DOMINIO-RURAL-P",
            "ENCIG2025": "RESULT-ARBITRO-ENCIG2025-DIGITAL-ESCOLARIDAD-SUPERIOR-P"}


# ═══════════════════════════ 1 · guardia ═══════════════════════════════════

@pytest.mark.parametrize("k", list(PIEZAS))
def test_auditoria_pasa_sobre_el_archivo_real(k):
    assert MODS[k].auditoria_ast() == []


MUTACIONES = {
    "R1": ("import numpy as np", "import numpy as np\nimport subprocess"),
    "R2": ("    out = m._estimate(d, cells, reps, seed)", "    out = m._estimate(d, cells, reps, seed)\n    d.groupby('_est')"),
    "R3-lista": ('def marginal(m, prefijo: str, y, eje, grupos, categorias):',
                 'def marginal(m, prefijo: str, y, eje, grupos, categorias):\n    pass\n\n\ndef _x(m, y, g):\n    return marginal(m, "p", y, ["sexo", "edad"], g, ("1",))'),
    "R3-cells": ('def marginal(m, prefijo: str, y, eje, grupos, categorias):',
                 'def _y(m, y, g):\n    return m._cells("p", y, {"sexo": (g, ("1",)), "edad": (g, ("1",))})\n\n\ndef marginal(m, prefijo: str, y, eje, grupos, categorias):'),
    "R4": ("def marginal(", "def cruce(m, a, b):\n    return None\n\n\ndef marginal("),
    "R5": ("def _eje_total(m, d", "def _eje_par(m, d):\n    return d['SEXO'].eq('1') & d['EDAD'].eq('30')\n\n\ndef _eje_total(m, d"),
    "R6": ("OLA_OBJETIVO = ", "OTRO = 'conjunto_de_datos_tsdem_enut2024.csv'\nOLA_OBJETIVO = "),
}


@pytest.mark.parametrize("k", list(PIEZAS))
@pytest.mark.parametrize("regla", list(MUTACIONES))
def test_auditoria_control_positivo_por_regla(k, regla):
    fuente = open(os.path.join(C0DIR, PIEZAS[k]["calc"], "medidor.py"), encoding="utf-8").read()
    viejo, nuevo = MUTACIONES[regla]
    assert viejo in fuente, (k, regla)
    mutado = fuente.replace(viejo, nuevo, 1)
    viol = MODS[k].auditoria_ast_fuente(mutado)
    assert any(v.startswith(regla.split("-")[0]) for v in viol), (k, regla, viol)


@pytest.mark.parametrize("k", list(PIEZAS))
def test_auditoria_R2b_merge_solo_por_id_per(k):
    if k == "ENIF2024":
        pytest.skip("ENIF no une tablas; `merge` está prohibido del todo (R2)")
    fuente = open(os.path.join(C0DIR, PIEZAS[k]["calc"], "medidor.py"), encoding="utf-8").read()
    mutado = fuente.replace('on="ID_PER", how="left", validate="m:1"', 'on="EST_DIS", how="left", validate="m:1"', 1)
    assert mutado != fuente
    assert any(v.startswith("R2b") for v in MODS[k].auditoria_ast_fuente(mutado))


@pytest.mark.parametrize("k", list(PIEZAS))
def test_guardia_en_corrida_rechaza_lista_y_reserva(k, tmp_path):
    M = MODS[k]
    import pandas as pd
    g = pd.Series(["1", "2"])
    with pytest.raises(ValueError):
        M.marginal(None, "p", g, ["sexo", "edad"], g, ("1",))
    with pytest.raises(ValueError):
        M.marginal(None, "p", g, "escolaridad_x_sexo", g, ("1",))
    # insumo de la ola reservada con `ola` = ola anterior -> PARO antes de abrir nada
    z = SINTETICOS[k](tmp_path / "s.zip")
    inp = _inputs(k, PIEZAS[k]["ola_oro"], z)
    inp[PIEZAS[k]["payload"]] = {"ruta_absoluta": str(z)}
    with pytest.raises(M.ParoDeGuardia):
        M.medir(inp, _contrato(k, PIEZAS[k]["ola_oro"]))
    with pytest.raises(M.ParoDeGuardia):
        M.medir(_inputs(k, "2019", z), _contrato(k, "2019"))


# ═══════════════════════════ 2 · sintético por el validador que sella ═══════

@pytest.mark.parametrize("k", list(PIEZAS))
def test_sintetico_ola_nueva_ids_exactos_y_valida_outputs(k, tmp_path):
    z = SINTETICOS[k](tmp_path / "nueva.zip")
    out = MODS[k].medir(_inputs(k, PIEZAS[k]["ola"], z), _contrato(k, PIEZAS[k]["ola"]))
    declarados = {r["id"] for r in SPECS[k]["resultados"]}
    assert set(out) == declarados
    nulos = _acepta(k, out, PIEZAS[k]["ola"])
    assert nulos == [], nulos            # sintético con todas las categorías pobladas
    assert out[f"{PIEZAS[k]['pref_R']}{PIEZAS[k]['ola']}-G-OLA"] == PIEZAS[k]["ola"]
    assert all(isinstance(r.get("permite_no_estimable"), bool) or "permite_no_estimable" not in r
               for r in SPECS[k]["resultados"])


@pytest.mark.parametrize("k", list(PIEZAS))
def test_sintetico_categoria_vacia_null_declarado(k, tmp_path):
    z = SINTETICOS[k](tmp_path / "vacia.zip", **VACIA[k])
    out = MODS[k].medir(_inputs(k, PIEZAS[k]["ola"], z), _contrato(k, PIEZAS[k]["ola"]))
    nulos = _acepta(k, out, PIEZAS[k]["ola"])
    base = ID_VACIO[k][:-2]
    assert {f"{base}-P", f"{base}-IC-LO", f"{base}-IC-HI"} <= set(nulos), nulos
    assert out[f"{base}-N"] == 0 and out[f"{base}-DEN-W"] == 0.0 and out[f"{base}-B-VALIDAS"] == 0
    # todo nulo está declarado con permite_no_estimable en el spec
    permitidos = {r["id"] for r in SPECS[k]["resultados"] if r.get("permite_no_estimable")}
    assert set(nulos) <= permitidos


# ═══════════════════════════ 3 · oro sobre la ola anterior ══════════════════

@pytest.mark.parametrize("k", list(PIEZAS))
def test_oro_reproduce_el_piso_sellado(k):
    p = PIEZAS[k]
    z = os.path.join(RAW, p["zip_oro"])
    if not os.path.exists(z):
        pytest.skip(f"corpus no montado: {z}")
    reps = int(SPECS[k]["parametros"]["bootstrap_replicas"])
    out = MODS[k].medir(_inputs(k, p["ola_oro"], z), _contrato(k, p["ola_oro"], reps))
    refs = [(p["pref_oro"], json.load(open(os.path.join(C0DIR, p["piso"], "resultados.json"), encoding="utf-8"))["resultados"], None)]
    if p["oro_extra"]:
        calc2, pref2, marca = p["oro_extra"]
        refs.append((pref2, json.load(open(os.path.join(C0DIR, calc2, "resultados.json"), encoding="utf-8"))["resultados"], marca))
    comparados, maxd = 0, 0.0
    for key, v in out.items():
        if "-G-" in key or "-TOTAL-" in key:
            continue
        for pref, ref, marca in refs:
            if marca is not None and marca not in key:
                continue
            if marca is None and p["oro_extra"] and p["oro_extra"][2] in key:
                continue
            kk = key.replace(f"{p['pref_R']}{p['ola_oro']}-", pref, 1)
            assert kk in ref, kk
            comparados += 1
            if v is None:
                assert ref[kk] is None
            else:
                maxd = max(maxd, abs(float(v) - float(ref[kk])))
    assert comparados == {"ENIF2024": 192, "ENVIPE2025": 90, "ENCIG2025": 60}[k], comparados
    assert maxd == 0.0, maxd
    _acepta(k, out, p["ola_oro"])


# ═══════════════════════════ 4 · tabla de identidad ═════════════════════════

def test_tabla_identidad_57_solo_piso_enlazadas_a_ids_declarados():
    ruta = os.path.join(ROOT, "forense", "prereg-caja", "ARBITRO-MARGINALES-metadatos-v1_0.tsv")
    filas = [l.rstrip("\n").split("\t") for l in open(ruta, encoding="utf-8")]
    cab, cuerpo = filas[0], filas[1:]
    rows = [dict(zip(cab, r)) for r in cuerpo]
    assert len(rows) == 57
    assert len({r["cell_id_R"] for r in rows}) == 57 and len({r["cell_id_piso"] for r in rows}) == 57
    declarados = {r["id"] for s in SPECS.values() for r in s["resultados"]}
    faltan = [r["cell_id_R"] for r in rows if r["cell_id_R"] not in declarados]
    assert faltan == [], faltan
    # el piso citado existe sellado
    for r in rows:
        res = json.load(open(os.path.join(C0DIR, r["calc_piso"], "resultados.json"), encoding="utf-8"))["resultados"]
        assert r["cell_id_piso"] in res, r["cell_id_piso"]
    # y el marcador vigente sigue diciendo SOLO-PISO (o ya EVALUADA tras este acto) de esas mismas celdas
    M = _load(os.path.join(ROOT, "tools", "marcador_segmento.py"), "marcador_segmento_arbitro_test")
    v = M.deriva()
    ids = {f["celda_id"] for f in v["filas"] if f["tipo"] == "MARGINAL" and f["estado"] in ("SOLO-PISO", "EVALUADA")}
    assert {r["marcador_celda_id"] for r in rows} == ids
