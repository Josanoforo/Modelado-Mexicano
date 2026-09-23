"""Contratos sintéticos de CALC-LAPOP-PISOS-{2004-0002,2006,2019-0002,2021,2023}.

2004-0001 falló antes del sello (diagnóstico wt NaN); su medidor sigue congelado
e idéntico a los otros cuatro de la v1_0; 2004-0002 es el sucesor activo.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

import pandas as pd
import pyreadstat
import yaml

ROOT = Path(__file__).resolve().parents[1]
CALCS = ["2004-0001", "2006-0001", "2019-0002", "2021-0001", "2023-0001"]
ACTIVOS = ["2004-0002", "2006-0001", "2019-0002", "2021-0001", "2023-0001"]
MODULE = ROOT / "data/corrida0/CALC-LAPOP-PISOS-2023-0001/medidor.py"
spec = importlib.util.spec_from_file_location("lapop_pisos_olas", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def _datos():
    return pd.DataFrame({
        "b18": [7, 6, 1, 2] * 8 + [888888, float("nan")],
        "b21": [1, 1, 1, 7] * 8 + [2, 3],
        "wt": [2.0, 1.0, 1.0, 1.0] * 8 + [1.0, 1.0],
        "estratopri": [101] * 16 + [102] * 18,
        "upm": [1, 2, 3, 4] * 8 + [4, 4],
    })


def test_ponderacion_y_no_respuesta():
    df = _datos()
    got = mod.estimate(df["b18"], df["wt"], df["estratopri"], df["upm"],
                       tuple(range(1, 8)), (6, 7), (888888,), 42, 50, 30)
    assert got["estado"] == "ESTIMADA"
    assert got["n"] == 32 and got["n_no_sustantivo"] == 2
    assert got["p"] == 24 / 40
    assert got["replicas_validas"] == 50


def test_escala_discrepante_no_recodifica():
    df = _datos()
    df.loc[0, "b18"] = 9
    got = mod.estimate(df["b18"], df["wt"], df["estratopri"], df["upm"],
                       tuple(range(1, 8)), (6, 7), (888888,), 42, 10, 30)
    assert got["estado"] == "ESCALA-DISCREPANTE" and got["p"] is None
    assert got["n_fuera_de_escala"] == 1


def test_n_minimo():
    df = _datos().head(20)
    got = mod.estimate(df["b18"], df["wt"], df["estratopri"], df["upm"],
                       tuple(range(1, 8)), (6, 7), (888888,), 42, 10, 30)
    assert got["estado"] == "NO-ESTIMABLE"


def test_medir_separa_pol001_y_upm_compuesta(tmp_path):
    df = _datos().fillna(888888)
    df["prov"] = [1, 2] * 17
    ruta = tmp_path / "sint.dta"
    pyreadstat.write_dta(df, str(ruta))
    it = lambda c, v, o: {"clave": c, "variable": v, "validos": list(range(1, 8)),
                          "evento": [6, 7], "faltantes": [888888], "semilla_desplazamiento": o}
    contrato = {"seed": {"valor": 42}, "parametros": {
        "payload_id": "x", "diseno": {"estrato": "estratopri", "upm": ["prov", "upm"], "peso": "wt"},
        "items": [it("pol", "b18", 0), it("par", "b21", 1)], "bootstrap_replicas": 20, "n_minimo": 30,
        "result_filas": "R-FILAS", "result_tablas": {"R-POL001": ["pol"], "R-TABLA": ["par"]}}}
    out = mod.medir({"x": {"ruta_absoluta": str(ruta)}}, contrato)
    assert out["R-FILAS"] == 34
    assert set(json.loads(out["R-POL001"])) == {"pol"}
    tabla = json.loads(out["R-TABLA"])["par"]
    assert tabla["n_upm"] == 9 and tabla["p"] == 8 / 42


def test_cinco_medidores_identicos_y_hash_declarado():
    hashes = set()
    for c in CALCS:
        d = ROOT / f"data/corrida0/CALC-LAPOP-PISOS-{c}"
        h = hashlib.sha256((d / "medidor.py").read_bytes()).hexdigest()
        s = yaml.safe_load((d / "spec.yaml").read_text(encoding="utf-8"))
        assert s["parametros"]["hash_medidor_sha256"] == h
        assert s["etiquetas"]["adopta"] == "NO"
        hashes.add(h)
    assert len(hashes) == 1


def _corrida0():
    s = importlib.util.spec_from_file_location("corrida0_conducto", ROOT / "tools/corrida0.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def test_conducto_acepta_las_tres_ramas_terminales_por_calc(tmp_path):
    """D-22(2): la salida de cada rama terminal pasa `_valida_outputs` con la spec real."""
    c0 = _corrida0()
    for c in ACTIVOS:
        d = ROOT / f"data/corrida0/CALC-LAPOP-PISOS-{c}"
        s = yaml.safe_load((d / "spec.yaml").read_text(encoding="utf-8"))
        par = s["parametros"]
        med = importlib.util.spec_from_file_location(f"m_{c}", d / "medidor.py")
        m = importlib.util.module_from_spec(med)
        med.loader.exec_module(m)
        dis, n = par["diseno"], 40
        df = pd.DataFrame({dis["estrato"]: [1] * 20 + [2] * 20})
        for i, u in enumerate(dis["upm"]):
            df[u] = [(k % 4) + i for k in range(n)]
        for peso in (dis.get("peso"), dis.get("peso_diagnostico")):
            if peso:
                df[peso] = 1.0
        for j, it in enumerate(par["items"]):
            if j % 3 == 0:
                df[it["variable"]] = [it["validos"][k % len(it["validos"])] for k in range(n)]
            elif j % 3 == 1:
                df[it["variable"]] = [it["faltantes"][0]] * n
            else:
                df[it["variable"]] = [max(it["validos"]) + 1] + [it["validos"][0]] * (n - 1)
        ruta = tmp_path / f"{c}.dta"
        pyreadstat.write_dta(df, str(ruta))
        par_s = dict(par, bootstrap_replicas=5)
        contrato = c0.contrato_ejecutable(dict(s, parametros=par_s))
        out = m.medir({par["payload_id"]: {"ruta_absoluta": str(ruta)}}, contrato)
        assert c0._valida_outputs(s, out) == [], c
        estados = set()
        for rid in par["result_tablas"]:
            estados |= {v["estado"] for k, v in json.loads(out[rid]).items() if not k.startswith("_")}
        esperados = {"ESTIMADA", "NO-ESTIMABLE", "ESCALA-DISCREPANTE"} if len(par["items"]) >= 3 else {"ESTIMADA", "NO-ESTIMABLE"}
        assert estados == esperados, (c, estados)


def test_sucesor_2004_diagnostico_de_peso_vacio_es_null(tmp_path):
    d = ROOT / "data/corrida0/CALC-LAPOP-PISOS-2004-0002"
    med = importlib.util.spec_from_file_location("m2004b", d / "medidor.py")
    m = importlib.util.module_from_spec(med)
    med.loader.exec_module(m)
    df = _datos().fillna(888888)
    df["wt_diag"] = float("nan")
    ruta = tmp_path / "w.dta"
    pyreadstat.write_dta(df, str(ruta))
    it = {"clave": "par", "variable": "b21", "validos": list(range(1, 8)), "evento": [6, 7],
          "faltantes": [888888], "semilla_desplazamiento": 0}
    contrato = {"seed": {"valor": 42}, "parametros": {
        "payload_id": "x", "diseno": {"estrato": "estratopri", "upm": ["upm"], "peso": None,
                                      "peso_diagnostico": "wt_diag"},
        "items": [it], "bootstrap_replicas": 5, "n_minimo": 30,
        "result_filas": "F", "result_tablas": {"T": ["par"]}}}
    out = m.medir({"x": {"ruta_absoluta": str(ruta)}}, contrato)
    diag = json.loads(out["T"])["_diagnostico_peso"]
    assert diag["min"] is None and diag["max"] is None and diag["n_vacios"] == 34
