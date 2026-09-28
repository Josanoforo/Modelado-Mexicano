"""CALC de GEN2-CALC-ALTERNOS-LOTE-1: los nueve medidores sobre datos sintéticos.

Defectos que atrapa: (1) un medidor que lee otro payload que el fijado (E.6)
o un cargador distinto del fijado por sha256; (2) una salida cuyas llaves no
son exactamente los RESULT de su spec.yaml (D-22(2)); (3) un estimador que no
responde a su código (prueba por mutación: cambiar el evento cambia la
cifra); (4) copias divergentes del medidor genérico entre CALC. Sin corpus.
"""
import csv
import hashlib
import importlib.util
import io
import json
import types
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
C0 = ROOT / "data/corrida0"
GENERICOS = ["CALC-ALT-M05-LAPOP2021-0001", "CALC-ALT-M05-LAPOP2019-0001", "CALC-ALT-M19-ENCUCI2020-0001",
             "CALC-ALT-M22-ENVIPE2025-0001", "CALC-ALT-M23-ENSAFI2023-0001", "CALC-ALT-M13-CIDECSES2015-0001"]
WVS = "CALC-ALT-M19-WVS2018-REPRO-0001"
TABS = ["CALC-ALT-R03-ENCRIGE2020-0001", "CALC-ALT-R03-ENVE2024-0001"]


def _corrida0():
    s = importlib.util.spec_from_file_location("corrida0_alternos", ROOT / "tools/corrida0.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


C = _corrida0()


def _mod(calc):
    s = importlib.util.spec_from_file_location(calc.replace("-", "_"), C0 / calc / "medidor.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _spec(calc):
    return yaml.safe_load((C0 / calc / "spec.yaml").read_text())


def _ids(spec):
    return {r["id"] for r in spec["resultados"]}


def test_medidor_generico_identico_en_los_seis():
    shas = {hashlib.sha256((C0 / c / "medidor.py").read_bytes()).hexdigest() for c in GENERICOS}
    assert len(shas) == 1
    shas_t = {hashlib.sha256((C0 / c / "medidor.py").read_bytes()).hexdigest() for c in TABS}
    assert len(shas_t) == 1


@pytest.mark.parametrize("calc", GENERICOS + [WVS] + TABS)
def test_spec_declara_payload_unico_y_sha(calc):
    sp = _spec(calc)
    man = [i["id"] for i in sp["inputs"] if i.get("origen") == "manifiesto"]
    assert man == [sp["parametros"]["payload_id"]]
    assert len(sp["parametros"]["hash_payload_sha256"]) == 64
    assert sp["etiquetas"]["adopta"] == "NO" and sp["etiquetas"]["marca_temporal"] == "RETROSPECTIVA"
    assert "holdout_gastado" in sp["etiquetas"]


def _sintetico_generico(par, n=2400, seed=3):
    """DataFrame con las columnas que la spec pide, códigos dentro de validos."""
    rng = np.random.default_rng(seed)
    cols = {}
    dis = par["diseno"]
    cols[dis["peso"]] = rng.uniform(0.5, 2.0, n).round(4).astype(str)
    cols[dis["estrato"]] = (np.arange(n) % 8).astype(str)
    for u in dis["upm"]:
        cols[u] = (np.arange(n) % 96).astype(str)
    for f in par.get("universo_filtros", []):
        cols[f["variable"]] = rng.choice([str(v) for v in f["validos"]], n)
    for it in par["items"]:
        cols.setdefault(it["variable"], rng.choice([str(v) for v in it["validos"]], n))
    for g in par.get("grupos", []):
        cods = [str(c) for cs in g["niveles"].values() for c in cs]
        cols.setdefault(g["variable"], rng.choice(cods, n))
    for dv in par.get("derivadas", []):
        for v in dv.get("variables", []):
            cols.setdefault(v, rng.choice(["1", "2"], n))
        for comp in dv.get("componentes", []):
            if comp["variable"] not in {d["nombre"] for d in par["derivadas"]}:
                cols.setdefault(comp["variable"], rng.choice(["1", "2"], n))
    for dv in par.get("derivadas", []):
        cols.pop(dv["nombre"], None)
    aux = None
    if par.get("union"):
        u = par["union"]
        cols[u["llave"]] = np.arange(n).astype(str)
        aux = pd.DataFrame({u["llave"]: np.arange(n).astype(str)})
        for c in u["columnas"]:
            g = next(x for x in par["grupos"] if x["variable"] == c)
            aux[c] = rng.choice([str(v) for vs in g["niveles"].values() for v in vs], n)
            cols.pop(c, None)
    return pd.DataFrame(cols), aux


def _corre_generico(calc, par_mod=None):
    M = _mod(calc)
    sp = _spec(calc)
    par = json.loads(json.dumps(sp["parametros"]))
    if par_mod:
        par_mod(par)
    df, aux = _sintetico_generico(par)

    def cargar(pid, tabla, columnas=None):
        assert pid == par["payload_id"]
        base = df if tabla == par["tabla"] else aux
        out = base[columnas].copy()
        out.attrs["fuente"] = "SINTETICO"
        return out

    M._loader = lambda sha: types.SimpleNamespace(cargar=cargar)
    M._sha = lambda p: par["hash_payload_sha256"]
    par["bootstrap_replicas"] = 40
    return M.medir({par["payload_id"]: {"ruta_absoluta": "/dev/null"}},
                   {"parametros": par, "seed": sp["seed"]}), sp


@pytest.mark.parametrize("calc", GENERICOS)
def test_generico_salida_igual_a_resultados(calc):
    out, sp = _corre_generico(calc)
    assert set(out) == _ids(sp)
    assert C._valida_outputs(sp, out) == []
    t = json.loads(out[sp["parametros"]["result_tabla"]])
    primero = sp["parametros"]["items"][0]["clave"]
    assert t[primero]["NACIONAL"]["estado"] == "ESTIMADA"
    assert 0.0 <= t[primero]["NACIONAL"]["p"] <= 1.0


@pytest.mark.parametrize("calc", GENERICOS)
def test_generico_mutacion_del_evento_cambia_la_cifra(calc):
    out, sp = _corre_generico(calc)
    clave = sp["parametros"]["items"][0]["clave"]

    def muta(par):
        it = par["items"][0]
        it["evento"] = [v for v in it["validos"] if v not in it["evento"]][:1]

    out2, _ = _corre_generico(calc, muta)
    rt = sp["parametros"]["result_tabla"]
    assert json.loads(out[rt])[clave]["NACIONAL"]["p"] != json.loads(out2[rt])[clave]["NACIONAL"]["p"]


@pytest.mark.parametrize("calc", GENERICOS)
def test_generico_guardia_de_cargador(calc):
    M = _mod(calc)
    sp = _spec(calc)
    with pytest.raises(ValueError, match="GUARDIA"):
        M._loader("0" * 64)


def test_wvs_reproduce_sobre_sintetico_con_referencia_propia():
    M = _mod(WVS)
    sp = _spec(WVS)
    par = json.loads(json.dumps(sp["parametros"]))
    rng = np.random.default_rng(5)
    n = 1200
    ent = np.array([f"MX-{e:02d}" for e in rng.integers(1, 26, n)])
    df = pd.DataFrame({"Q60": rng.integers(1, 5, n).astype(str), "Q61": rng.integers(1, 5, n).astype(str),
                       "Q70": rng.integers(1, 5, n).astype(str), "W_WEIGHT": rng.uniform(.6, 1.5, n).astype(str),
                       "N_REGION_ISO": ent, "I_PSU": (np.arange(n) % 300).astype(str)})
    cargar = lambda pid, tabla, columnas=None: df[columnas].copy()
    reales = M._mod
    M._mod = lambda rel, sha, nombre: (types.SimpleNamespace(cargar=cargar) if "corpus_loader" in rel
                                      else reales(rel, sha, nombre))
    sha_real = M._sha
    M._sha = lambda p: par["hash_payload_sha256"] if str(p) == "/dev/null" else sha_real(p)
    out = M.medir({par["payload_id"]: {"ruta_absoluta": "/dev/null"}}, {"parametros": par})
    assert set(out) == _ids(sp)
    assert C._valida_outputs(sp, out) == []
    assert out[par["result_veredicto"]] == "NO-REPRODUCE"  # la referencia es la del abridor, no la del sintético
    t = json.loads(out[par["result_tabla"]])
    ref = {"entidades_elegibles": t["entidades_elegibles"], "mediana": t["mediana_enforcement_alto"],
           "p_alto": t["principal_sin_puente"]["p_T"], "p_bajo": t["principal_sin_puente"]["p_C"],
           "d": t["principal_sin_puente"]["d_hat"]}
    par["referencia_abridor"] = ref
    out2 = M.medir({par["payload_id"]: {"ruta_absoluta": "/dev/null"}}, {"parametros": par})
    assert out2[par["result_veredicto"]] == "REPRODUCE"
    assert t["entidades_alto"] + t["entidades_bajo"] == t["entidades_elegibles"]


def _zip_tabs(tmp_path, par):
    p = tmp_path / "tab.zip"
    with zipfile.ZipFile(p, "w") as z:
        for t in par["tablas"]:
            cab = ["Dominio", t["denominador"]]
            for ind in t["indicadores"]:
                cab += [ind["numerador"], ind["publicado"]]
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(cab)
            for dom in t["dominios"]:
                fila = [dom, "1000"]
                for ind in t["indicadores"]:
                    fila += ["37", str(37 / 1000 * ind["escala_publicado"])]
                w.writerow(fila)
            z.writestr(f"x/{t['archivo']}", buf.getvalue().encode(par["encoding"]))
    return p


@pytest.mark.parametrize("calc", TABS)
def test_tabulados_extraen_y_controlan(calc, tmp_path):
    M = _mod(calc)
    sp = _spec(calc)
    par = json.loads(json.dumps(sp["parametros"]))
    ruta = _zip_tabs(tmp_path, par)
    par["hash_payload_sha256"] = hashlib.sha256(ruta.read_bytes()).hexdigest()
    out = M.medir({par["payload_id"]: {"ruta_absoluta": str(ruta)}}, {"parametros": par})
    assert set(out) == _ids(sp)
    assert C._valida_outputs(sp, out) == []
    assert out[par["result_control"]] == "PASA"
    t = json.loads(out[par["result_tabla"]])
    celdas = [v for k, v in t.items() if not k.startswith("_")]
    assert celdas and all(abs(c["p"] - 0.037) < 1e-12 for c in celdas)
    par["hash_payload_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="GUARDIA"):
        M.medir({par["payload_id"]: {"ruta_absoluta": str(ruta)}}, {"parametros": par})
