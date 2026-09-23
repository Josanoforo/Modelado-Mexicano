#!/usr/bin/env python3
"""ACTO GEN2-DUELO-ENCIG2025-CIERRE-1 · COMMIT-1 · validación de «congelado» (D-22).

Spec: forense/prereg-caja/ENCIG-DUELO-2025-cierre-spec-v1_0.md §6.
  (a) sintética: emisiones y árbitro de punta a punta; `corrida0._valida_outputs`
      vacío en todas las ramas terminales.
  (b) oro (sólo CAJA): la maquinaria del árbitro sobre ENCIG 2023 reproduce los
      CALC sellados.
  (c) reserva y guardias.  (d) λ.  (e) mutación.  (f) identidad.
"""
import copy
import hashlib
import importlib.util
import io
import json
import os
import zipfile

import numpy as np
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUELO = os.path.join(ROOT, "tools", "encig", "duelo_2025", "duelo.py")
CALCS = {c: os.path.join(ROOT, "data", "corrida0", f"CALC-ENCIG-DUELO-2025-{c}-EMISIONES-0001")
         for c in ("EDADXSEXO", "ESCOLARIDADXSEXO")}
ARB = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001")
P4_MED = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001", "medidor.py")
P4_ADJ = os.path.join(ROOT, "data", "corrida0", "CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001", "adjudicacion.py")
RECETA = os.path.join(ROOT, "tools", "encig_cruces_historicos.py")
FIRMAS_CONGELADAS = os.path.join(ROOT, "tools", "encig", "duelo_2025", "constancia-firma-657c-01.tsv")
FIRMAS_VIVAS = os.path.join(ROOT, "forense", "firmas-pendientes.tsv")
RAW = os.path.join(ROOT, "data", "raw")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


D = _load(DUELO, "duelo_encig2025")
C0 = _load(os.path.join(ROOT, "tools", "corrida0.py"), "corrida0_para_test_duelo_encig")
RECETA_MOD = _load(RECETA, "receta_para_test_duelo_encig")


def _spec(calc_dir):
    with open(os.path.join(calc_dir, "spec.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def _repo(path, origen="repo", ruta=None):
    raw = open(path, "rb").read()
    return {"origen": origen, "ruta": ruta or os.path.basename(path), "ruta_absoluta": str(path),
            "bytes": raw, "sha256": hashlib.sha256(raw).hexdigest()}


def _json_input(tmp_path, nombre, resultados):
    p = tmp_path / nombre
    p.write_text(json.dumps({"resultados": resultados}), encoding="utf-8")
    return _repo(str(p))


# ─────────────────────────── fixtures sintéticos ───────────────────────────

EDADES = {"18-29": 24, "30-44": 37, "45-59": 52, "60-96": 70}
NIVS = {"HASTA-PRIMARIA": "1", "SECUNDARIA": "3", "MEDIA-SUPERIOR": "5", "SUPERIOR": "8"}


def fabrica_zip(tmp_path, ola, n_personas=9000, seed=1, sin_60=False, rara=False, nombre=None):
    """ENCIG sintética con la forma que lee la receta: sec_7 (trámites) y residentes.
    `sin_60`: ninguna persona 60-96 (categoría con masa cero).
    `rara`: la celda 60-96 x mujer vive en una sola UPM de un estrato con dos UPM
    (una réplica que no la sortea la vacía)."""
    rng = np.random.default_rng(seed)
    per, tra = ["ID_PER,SEXO,EDAD,NIV"], ["N_TRA,P7_3,FAC_TRA,EST_DIS,UPM_DIS,ID_PER"]
    edades = [e for e in EDADES if not (sin_60 and e == "60-96")]
    for i in range(n_personas):
        sexo = "1" if i % 2 else "2"
        edad = edades[(i // 2) % len(edades)]
        niv = list(NIVS)[(i // 7) % 4]
        if rara and edad == "60-96" and sexo == "2":
            if i % 40:
                edad = "45-59"
        est, upm = f"{1 + i % 12:02d}", f"U{i % 300:04d}"
        if rara and edad == "60-96" and sexo == "2":
            est, upm = "99", "U9999"
        idp = f"P{i:06d}"
        edad_num = 97 if (i % 997 == 0) else EDADES[edad]
        per.append(f"{idp},{sexo},{edad_num},{NIVS[niv]}")
        p = 0.35 + 0.25 * (niv in ("MEDIA-SUPERIOR", "SUPERIOR")) + 0.1 * (edad in ("18-29", "30-44"))
        canal = "4" if rng.random() < p else rng.choice(["1", "2", "6"])
        tra.append(f"01,{canal},{100 + int(rng.integers(0, 60))},{est},{upm},{idp}")
        if i % 5 == 0:
            tra.append(f"02,1,{120},{est},{upm},{idp}")
    if rara:
        per.append("PX,1,24,1")
        tra.append("01,1,110,99,U9998,PX")
    z = tmp_path / (nombre or f"encig{ola}_sintetico.zip")
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr(f"encig{ola}_04_sec_7.csv", "\n".join(tra) + "\n")
        zf.writestr(f"encig{ola}_02_residentes_sec_2.csv", "\n".join(per) + "\n")
    return str(z)


def _frame(zpath, ola):
    return D._frame_ola(RECETA_MOD, {"payload": {"ruta_absoluta": zpath}}, ola, "payload")


def _marginales_ola(zpath, ola, reps=30, seed=5):
    frame, _ = _frame(zpath, ola)
    res = D._r_y_marginales(RECETA_MOD, frame, reps, seed)
    return {k: float(res["points"][i]) for k, i in res["idx_m"].items()}, {k: res["n"][i] for k, i in res["idx_m"].items()}


def historico_sintetico(ola, n_celda=800, causa="OK", n_bajas=(), seed=3):
    rng = np.random.default_rng(seed + int(ola))
    r = {}
    for cruce in D.CRUCES:
        for i, (ka, kb) in enumerate(D.celdas(cruce)):
            g = lambda q: D.id_historico(ola, cruce, ka, kb, q)
            p = float(rng.uniform(0.3, 0.8))
            r[g("N")] = 150 if (cruce, i) in n_bajas else n_celda
            r[g("P")], r[g("P-IC-LO")], r[g("P-IC-HI")] = p, p - 0.03, p + 0.03
            r[g("DELTA")] = float(rng.normal(0, 0.2))
            r[g("DELTA-EE")] = float(rng.uniform(0.03, 0.08))
            r[g("CAUSA")] = causa
    return r


def c2compuesto_sintetico(marg):
    r = {}
    nac = round(marg[("TOTAL", "TODOS")], 6)
    for cruce, (A, B) in D.CRUCES.items():
        for ka, kb in D.celdas(cruce):
            pa, pb = round(marg[(A, ka)], 6), round(marg[(B, kb)], 6)
            r[D.id_c2compuesto(cruce, ka, kb)] = D._expit(D._logit(pa) + D._logit(pb) - D._logit(nac))
    return r


def astra_sintetico(c2c, cruce, completo=True):
    r = {}
    for ka, kb in D.celdas(cruce):
        p = D._expit(D._logit(c2c[D.id_c2compuesto(cruce, ka, kb)]) + 0.02)
        r[D.id_astra(cruce, ka, kb, "P")] = p
        r[D.id_astra(cruce, ka, kb, "IC-LO")] = p - 0.04
        r[D.id_astra(cruce, ka, kb, "IC-HI")] = p + 0.04
        r[D.id_astra(cruce, ka, kb, "NIVEL")] = 0.95
        r[D.id_astra(cruce, ka, kb, "TIPO")] = "PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS"
    if not completo:
        r.pop(D.id_astra(cruce, *D.celdas(cruce)[0], "TIPO"))
    return r


def marg25_sellados(marg, n):
    r = {}
    for (eje, v), p in marg.items():
        r[D.id_marginal_2025(eje, v, "P")] = p
        r[D.id_marginal_2025(eje, v, "N")] = int(n[(eje, v)])
    return r


def firmas(tmp_path, estado="FIRMADA", incluir=True):
    t = "id\tqué_se_firma\tdónde\tcreado\tgatea\testado\tfirmada_en\tejecutada_en\tencargo\n"
    if incluir:
        t += f"{D.FP_FIRMA}\t§2\tencargo\t2026-09-23\tabrir dato\t{estado}\t\t\tencargo\n"
    p = tmp_path / "firmas.tsv"
    p.write_text(t, encoding="utf-8")
    return _repo(str(p))


def contrato_emisiones(cruce):
    return {"parametros": {"punto_de_entrada": "emisiones", "cruce": cruce, "n_minimo_celda": 200,
                           "z": D.Z, "c_astra_b": "SI -- sintético"}, "seed": {"aplica": False}}


def contrato_arbitro(reps=40):
    par = dict(_spec(ARB)["parametros"])
    par["bootstrap_replicas"] = reps
    return {"parametros": par, "seed": {"aplica": True, "valor": 20260919, "rng": "numpy.PCG64"}}


def escenario(tmp_path, *, hist_kw=None, astra_completo=True, zip_kw=None, perturba_marg=False,
              firma_estado="FIRMADA", reps=40):
    """Devuelve (inputs_emisiones_por_cruce, inputs_arbitro)."""
    z25 = fabrica_zip(tmp_path, "2025", **(zip_kw or {}))
    marg, n = _marginales_ola(z25, "2025")
    c2c = c2compuesto_sintetico(marg) if all(np.isfinite(list(marg.values()))) else {
        D.id_c2compuesto(c, ka, kb): 0.5 for c in D.CRUCES for ka, kb in D.celdas(c)}
    h21 = historico_sintetico("2021", **(hist_kw or {}))
    h23 = historico_sintetico("2023", **(hist_kw or {}))
    m25 = marg25_sellados({k: (v if np.isfinite(v) else 0.5) for k, v in marg.items()}, n)
    if perturba_marg:
        k0 = D.id_marginal_2025("SEXO", "1", "P")
        m25[k0] += 1e-3
    emis = {}
    for cruce in D.CRUCES:
        emis[cruce] = {
            "firmas_congeladas": firmas(tmp_path, firma_estado),
            "c2_compuesto_resultados": _json_input(tmp_path, f"c2c_{cruce}.json", c2c),
            "historico_2021_resultados": _json_input(tmp_path, f"h21_{cruce}.json", h21),
            "historico_2023_resultados": _json_input(tmp_path, f"h23_{cruce}.json", h23),
            "astra_resultados": _json_input(tmp_path, f"astra_{cruce}.json", astra_sintetico(c2c, cruce, astra_completo)),
            "medidor_piloto4": _repo(P4_MED),
        }
    arb = {
        "encig25_base_datos_csv": {"origen": "manifiesto", "ruta_absoluta": z25,
                                   "sha256": hashlib.sha256(open(z25, "rb").read()).hexdigest()},
        "receta_cruce_encig": _repo(RECETA),
        "adjudicacion_piloto4": _repo(P4_ADJ),
        "marginales_2025_resultados": _json_input(tmp_path, "marg25.json", m25),
    }
    return emis, arb


def corre_emisiones(tmp_path, emis):
    out = {}
    for cruce, inputs in emis.items():
        out[cruce] = D.medir(inputs, contrato_emisiones(cruce))
    return out


def sella(tmp_path, arb, emitidas):
    arb = dict(arb)
    for cruce, res in emitidas.items():
        k = cruce.lower()
        rp = tmp_path / f"emis_{k}_resultados.json"
        rp.write_text(json.dumps({"resultados": res}), encoding="utf-8")
        sp = tmp_path / f"emis_{k}_sello.json"
        sp.write_text(json.dumps({"resultados.json": hashlib.sha256(rp.read_bytes()).hexdigest()}), encoding="utf-8")
        arb[f"emisiones_{k}_resultados"] = _repo(str(rp))
        arb[f"emisiones_{k}_sello"] = _repo(str(sp))
    return arb


def valida(calc_dir, out):
    problemas = C0._valida_outputs(_spec(calc_dir), out)
    assert problemas == [], problemas[:10]
    for k, v in out.items():
        if isinstance(v, float):
            assert np.isfinite(v), (k, v)


def corre_todo(tmp_path, **kw):
    emis, arb = escenario(tmp_path, **kw)
    emitidas = corre_emisiones(tmp_path, emis)
    for cruce, res in emitidas.items():
        valida(CALCS[cruce], res)
    out = D.medir(sella(tmp_path, arb, emitidas), contrato_arbitro(kw.get("reps", 40)))
    valida(ARB, out)
    return emitidas, out


# ─────────────────────────── (a) sintética: ramas terminales ───────────────────────────

def test_a_todo_con_soporte(tmp_path):
    emitidas, out = corre_todo(tmp_path)
    for cruce in D.CRUCES:
        pc = f"{D.PA}-{cruce}"
        assert out[f"{pc}-G-SOPORTE-GLOBAL"] == "CON-SOPORTE"
        assert out[f"{pc}-G-PUNTUADAS-N"] == 8
        assert out[f"{pc}-G-CTRL-C2-VEREDICTO"] == "REPRODUCE"
        assert out[f"{pc}-G-B-BIS"] in D.PRECEDENCIA
        assert out[f"{pc}-G-C-ASTRA-ESTADO"] == "ENTRA"
    assert out[f"{D.PA}-G-CTRL-MARGINALES-VEREDICTO"] == "REPRODUCE"
    assert out[f"{D.PA}-G-AUDITORIA-CODIGO"] == "LIMPIA"


def test_a_soporte_parcial(tmp_path):
    _, out = corre_todo(tmp_path, hist_kw={"n_bajas": {("EDADXSEXO", 0)}})
    pc = f"{D.PA}-EDADXSEXO"
    assert out[f"{pc}-G-FALLAN-N"] == 1 and out[f"{pc}-G-SOPORTE-GLOBAL"] == "CON-SOPORTE"
    assert out[f"{pc}-G-PUNTUADAS-N"] == 7


def test_a_fuera_de_soporte_global(tmp_path):
    _, out = corre_todo(tmp_path, hist_kw={"n_bajas": {("ESCOLARIDADXSEXO", i) for i in range(3)}})
    pc = f"{D.PA}-ESCOLARIDADXSEXO"
    assert out[f"{pc}-G-SOPORTE-GLOBAL"] == "FUERA-DE-SOPORTE-GLOBAL"
    assert out[f"{pc}-G-B-BIS"] == "FUERA-DE-SOPORTE-GLOBAL"
    assert out[f"{pc}-G-CHAMPION-PROPUESTO"] == "NINGUNO"


def test_a_cero_puntuadas_y_lambda_k_insuficiente(tmp_path):
    emitidas, out = corre_todo(tmp_path, hist_kw={"causa": "REPLICA-DEGENERADA"})
    for cruce in D.CRUCES:
        assert emitidas[cruce][f"{D.P}-{cruce}-G-LAMBDA-ESTADO"] == "K-INSUFICIENTE"
        pc = f"{D.PA}-{cruce}"
        assert out[f"{pc}-G-PUNTUADAS-N"] == 0
        assert out[f"{pc}-G-B-BIS"] == "FUERA-DE-SOPORTE-GLOBAL"
    assert out[f"{D.PA}-G-B-BIS-AGREGADO"] == "SIN-CRUCES-CON-SOPORTE"


def test_a_celda_vaciada_en_una_replica(tmp_path):
    _, out = corre_todo(tmp_path, zip_kw={"rara": True})
    base = f"{D.PA}-EDADXSEXO-{D.rotulo('60-96', '2')}"
    assert out[f"{base}-R-IC-LO"] is None and out[f"{base}-SOPORTE"] != "PUNTUADA"


def test_a_categoria_con_masa_cero(tmp_path):
    _, out = corre_todo(tmp_path, zip_kw={"sin_60": True})
    base = f"{D.PA}-EDADXSEXO-{D.rotulo('60-96', '1')}"
    assert out[f"{base}-R-P"] is None and out[f"{base}-N-2025"] == 0
    assert out[f"{D.PA}-M-EDAD-60-MAS-P"] is None
    assert out[f"{D.PA}-G-CTRL-MARGINALES-VEREDICTO"] == "NO-REPRODUCE"
    assert out[f"{D.PA}-EDADXSEXO-G-CHAMPION-PROPUESTO"] == "NINGUNO"


def test_a_control_no_reproduce_no_emite_ic_de_c2(tmp_path):
    _, out = corre_todo(tmp_path, perturba_marg=True)
    assert out[f"{D.PA}-G-CTRL-MARGINALES-VEREDICTO"] == "NO-REPRODUCE"
    for cruce in D.CRUCES:
        assert out[f"{D.PA}-{cruce}-G-C2-IC-ESTADO"].startswith("NO-EMITIDO")
        assert out[f"{D.PA}-{cruce}-G-CHAMPION-PROPUESTO"] == "NINGUNO"


def test_a_astra_no_entra(tmp_path):
    emitidas, out = corre_todo(tmp_path, astra_completo=False)
    for cruce in D.CRUCES:
        assert emitidas[cruce][f"{D.P}-{cruce}-G-C-ASTRA-ESTADO"] == "NO-ENTRA"
        assert out[f"{D.PA}-{cruce}-G-C-ASTRA-GANA"] == "NO-ENTRA"


# ─────────────────────────── (b) oro: ENCIG 2023 ───────────────────────────

def _zip_2023():
    try:
        import sys
        sys.path.insert(0, os.path.join(ROOT, "tests"))
        from payload_resolver import resolver_payload
        r = resolver_payload("encig23_base_datos_csv")
        return r["ruta_absoluta"] if r["estado"] == "COINCIDE" else None
    except Exception:
        return None


@pytest.mark.skipif(not os.path.isdir(RAW), reason="corpus no montado (NUBE): el oro solo corre en CAJA")
def test_b_oro_encig2023_reproduce_cruces_y_marginales_sellados(tmp_path):
    z23 = _zip_2023()
    assert z23, "encig23_base_datos_csv no COINCIDE en el manifiesto"
    frame, diag = _frame(z23, "2023")
    res = D._r_y_marginales(RECETA_MOD, frame, 10000, 20260919)
    hist = json.load(open(os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG2023-CRUCES-HISTORICOS-0002",
                                       "resultados.json")))["resultados"]
    pisos = json.load(open(os.path.join(ROOT, "data", "corrida0", "CALC-PISOS-ENCIG2023-EJES-0002",
                                        "resultados.json")))["resultados"]
    assert diag["N-DISENO-VALIDO"] == hist["RESULT-ENCIG2023-CRUCES-HISTORICOS-N-DISENO-VALIDO"]
    peor = 0.0
    for cruce in D.CRUCES:
        for ka, kb in D.celdas(cruce):
            i = res["idx"][(cruce, ka, kb)]
            g = lambda q: hist[D.id_historico("2023", cruce, ka, kb, q)]
            assert res["n"][i] == g("N")
            ee, lo, hi, validas = RECETA_MOD._summary(float(res["points"][i]), res["boot"][:, i])
            dl = (D._logit(res["points"][i]) - D._logit(res["points"][i + 1])
                  - D._logit(res["points"][i + 2]) + D._logit(res["points"][i + 3]))
            reps = (RECETA_MOD._logit(res["boot"][:, i]) - RECETA_MOD._logit(res["boot"][:, i + 1])
                    - RECETA_MOD._logit(res["boot"][:, i + 2]) + RECETA_MOD._logit(res["boot"][:, i + 3]))
            dee = float(np.std(reps, ddof=1))
            for a, b in ((res["points"][i], g("P")), (lo, g("P-IC-LO")), (hi, g("P-IC-HI")),
                         (ee, g("P-EE")), (dl, g("DELTA")), (dee, g("DELTA-EE"))):
                peor = max(peor, abs(float(a) - float(b)))
    assert peor < 1e-10, peor
    peor_m = max(abs(float(res["points"][i]) - pisos[D.id_piso_2023(eje, v)])
                 for (eje, v), i in res["idx_m"].items() if eje != "TOTAL")
    assert peor_m < 1e-10, peor_m
    # el conducto del árbitro acepta la salida sobre datos reales (2023 hace de ola)
    marg = {k: float(res["points"][i]) for k, i in res["idx_m"].items()}
    n = {k: res["n"][i] for k, i in res["idx_m"].items()}
    c2c = c2compuesto_sintetico(marg)
    emitidas = {}
    for cruce in D.CRUCES:
        # históricos SINTÉTICOS a propósito: con los reales esto calcularía la λ
        # real antes del COMMIT-2 (spec §7); el oro de este test es el microdato 2023.
        inputs = {
            "firmas_congeladas": firmas(tmp_path),
            "c2_compuesto_resultados": _json_input(tmp_path, f"c2c_{cruce}.json", c2c),
            "historico_2021_resultados": _json_input(tmp_path, f"h21_{cruce}.json", historico_sintetico("2021")),
            "historico_2023_resultados": _json_input(tmp_path, f"h23_{cruce}.json", historico_sintetico("2023")),
            "astra_resultados": _json_input(tmp_path, f"astra_{cruce}.json", astra_sintetico(c2c, cruce)),
            "medidor_piloto4": _repo(P4_MED),
        }
        emitidas[cruce] = D.medir(inputs, contrato_emisiones(cruce))
    arb = sella(tmp_path, {
        "encig25_base_datos_csv": {"origen": "manifiesto", "ruta_absoluta": z23, "sha256": "oro-2023"},
        "receta_cruce_encig": _repo(RECETA), "adjudicacion_piloto4": _repo(P4_ADJ),
        "marginales_2025_resultados": _json_input(tmp_path, "m.json", marg25_sellados(marg, n))}, emitidas)
    con = contrato_arbitro(200)
    con["parametros"]["ola"] = "2023"
    out = D.medir(arb, con)
    valida(ARB, out)
    assert out[f"{D.PA}-G-CTRL-MARGINALES-VEREDICTO"] == "REPRODUCE"


# ─────────────────────────── (c) reserva y guardias ───────────────────────────

def test_c_emision_para_sin_firma_o_con_input_de_2025(tmp_path):
    emis, _ = escenario(tmp_path, firma_estado="ABIERTA")
    with pytest.raises(D.ParoDeGuardia, match="657c-01"):
        D.medir(emis["EDADXSEXO"], contrato_emisiones("EDADXSEXO"))
    emis, _ = escenario(tmp_path)
    mal = dict(emis["EDADXSEXO"])
    mal["encig25_base_datos_csv"] = {"origen": "manifiesto", "ruta_absoluta": "/x", "sha256": "0"}
    with pytest.raises(D.ParoDeGuardia):
        D.medir(mal, contrato_emisiones("EDADXSEXO"))
    mal = dict(emis["EDADXSEXO"])
    mal["astra_resultados"] = dict(mal["astra_resultados"], ruta="data/raw/encig2025_04_sec_7.csv")
    with pytest.raises(D.ParoDeGuardia, match="ENCIG 2025"):
        D.medir(mal, contrato_emisiones("EDADXSEXO"))


def test_c_arbitro_para_sin_sello_o_sello_falso(tmp_path):
    emis, arb = escenario(tmp_path)
    emitidas = corre_emisiones(tmp_path, emis)
    with pytest.raises(D.ParoDeGuardia):
        D.medir(arb, contrato_arbitro())
    sellado = sella(tmp_path, arb, emitidas)
    falso = dict(sellado)
    falso["emisiones_edadxsexo_resultados"] = dict(falso["emisiones_edadxsexo_resultados"],
                                                   bytes=falso["emisiones_edadxsexo_resultados"]["bytes"] + b" ")
    with pytest.raises(D.ParoDeGuardia, match="no coincide"):
        D.medir(falso, contrato_arbitro())


def test_c_guardia_de_pares(tmp_path):
    frame, _ = _frame(fabrica_zip(tmp_path, "2025", n_personas=400), "2025")
    D._mascara(frame, (("EDAD", "18-29"), ("SEXO", "1")), ("EDAD", "SEXO"))
    for ejes, par in (((("EDAD", "18-29"), ("ESCOLARIDAD", "SUPERIOR")), None),
                      ((("SEXO", "1"), ("EDAD", "18-29")), None),
                      ((("EDAD", "18-29"),), ("EDAD", "ESCOLARIDAD")),
                      ((("EDAD", "18-29"), ("SEXO", "1"), ("ESCOLARIDAD", "SUPERIOR")), None)):
        with pytest.raises(D.ReservaRota):
            D._mascara(frame, ejes, par)


def test_c_firma_asentada_y_congelada():
    for ruta in (FIRMAS_VIVAS, FIRMAS_CONGELADAS):
        filas = [l.split("\t") for l in open(ruta, encoding="utf-8").read().splitlines()]
        fila = [f for f in filas if f[0] == D.FP_FIRMA]
        assert len(fila) == 1 and fila[0][5] == "FIRMADA", ruta


def test_c_reserva_en_los_calc():
    for cruce, d in CALCS.items():
        r = os.path.join(d, "resultados.json")
        if os.path.exists(r):
            res = json.load(open(r))["resultados"]
            assert res[f"{D.P}-{cruce}-G-RESERVA-ENCIG2025-LEIDA"] == "NO"
            assert res[f"{D.P}-{cruce}-G-AUDITORIA-CODIGO"] == "LIMPIA"
    if os.path.exists(os.path.join(ARB, "resultados.json")):
        for d in CALCS.values():
            assert os.path.exists(os.path.join(d, "sello.json")), "R sellado sin emisiones selladas"


# ─────────────────────────── (d) λ ───────────────────────────

def test_d_lambda_se_rederiva_y_es_la_del_piloto4(tmp_path):
    emis, _ = escenario(tmp_path)
    p4 = _load(P4_MED, "p4_medidor_para_test_duelo_encig")
    for cruce, inputs in emis.items():
        out = D.medir(inputs, contrato_emisiones(cruce))
        pre = f"{D.P}-{cruce}"
        dbar, var, d21, e21, d23, e23 = [], [], {}, {}, {}, {}
        for ka, kb in D.celdas(cruce):
            b = f"{pre}-{D.rotulo(ka, kb)}"
            c = D.rotulo(ka, kb)
            d21[c], e21[c], d23[c], e23[c] = out[f"{b}-D21"], out[f"{b}-D21-EE"], out[f"{b}-D23"], out[f"{b}-D23-EE"]
            dbar.append((d21[c] + d23[c]) / 2.0)
            var.append((e21[c] ** 2 + e23[c] ** 2) / 4.0)
        var_entre = float(np.var(dbar, ddof=1))
        s2 = float(np.mean(var))
        tau2 = max(0.0, var_entre - s2)
        lam = tau2 / (tau2 + s2) if tau2 + s2 > 0 else 0.0
        assert abs(lam - out[f"{pre}-G-LAMBDA"]) < 1e-12
        assert abs(tau2 - out[f"{pre}-G-LAMBDA-TAU2"]) < 1e-12
        assert abs(s2 - out[f"{pre}-G-LAMBDA-SIGMA-BAR2"]) < 1e-12
        assert p4._lambda_cruce(d21, e21, d23, e23, set())["lambda"] == out[f"{pre}-G-LAMBDA"]
        for ka, kb in D.celdas(cruce):
            b = f"{pre}-{D.rotulo(ka, kb)}"
            esperado = D._expit(D._logit(out[f"{b}-C2-P"]) + lam * out[f"{b}-DBAR"])
            assert abs(esperado - out[f"{b}-C-ENCOGIDA-P"]) < 1e-15


# ─────────────────────────── (e) mutación ───────────────────────────

MUTANTES = {
    "sin guardia de emisiones": ("    _guardia_emisiones(inputs)\n    firma = _guardia_firma(inputs)\n",
                                 "    firma = _guardia_firma(inputs)\n"),
    "sin guardia de sellos": ("    emis = _guardia_sellos(inputs)\n", "    emis = {}\n"),
    "par consumido autorizado": ('PARES_AUTORIZADOS = frozenset({("EDAD", "SEXO"), ("ESCOLARIDAD", "SEXO")})',
                                 'PARES_AUTORIZADOS = frozenset({("EDAD", "SEXO"), ("ESCOLARIDAD", "SEXO"), ("EDAD", "ESCOLARIDAD")})'),
    "emision lee 2025": ('    umbral = int(par["n_minimo_celda"])\n    pre = f"{P}-{cruce}"\n',
                         '    umbral = int(par["n_minimo_celda"])\n    _frame_ola(None, inputs, 2025, "encig25_base_datos_csv")\n    pre = f"{P}-{cruce}"\n'),
    "mascara sin guardia": ('        raise ReservaRota(f"agrupacion no autorizada: {nombres}")',
                            '        pass'),
}


def test_e_mutantes_atrapados():
    fuente = open(DUELO, encoding="utf-8").read()
    assert D.auditoria(fuente) == []
    for nombre, (viejo, nuevo) in MUTANTES.items():
        assert fuente.count(viejo) == 1, nombre
        mutante = fuente.replace(viejo, nuevo)
        if nombre == "mascara sin guardia":
            mutante = mutante.replace('        raise ReservaRota(f"universo de par no autorizado: {par_universo}")', '        pass')
        assert D.auditoria(mutante) != [], nombre


# ─────────────────────────── (f) identidad ───────────────────────────

def test_f_medidores_byte_a_byte():
    canon = open(DUELO, "rb").read()
    for d in list(CALCS.values()) + [ARB]:
        assert open(os.path.join(d, "medidor.py"), "rb").read() == canon, d


def test_f_resultados_del_spec_son_el_esquema():
    for cruce, d in CALCS.items():
        assert _spec(d)["resultados"] == D.esquema_resultados("emisiones", cruce), cruce
    assert _spec(ARB)["resultados"] == D.esquema_resultados("adjudicacion")


def test_f_estado_gana_es_la_del_piloto4():
    p4 = _load(P4_ADJ, "p4_adj_para_test_duelo_encig")
    extraida = D._extrae_funcion(open(P4_ADJ, "rb").read(), "_estado_gana", {})
    for lo in (None, -1.0, -0.01, 0.0, 0.01, 0.25, 0.5, 0.5000001, 1.0, 3.0):
        ic = None if lo is None else (lo, lo + 1.0)
        assert extraida(ic, 0.5) == p4._estado_gana(ic, 0.5), ic


def test_f_inputs_de_los_spec_existen_con_su_sha():
    for d in list(CALCS.values()) + [ARB]:
        for ent in _spec(d)["inputs"]:
            if ent.get("origen") != "repo" or "sha256" not in ent:
                continue
            raw = open(os.path.join(ROOT, ent["ruta"]), "rb").read()
            assert hashlib.sha256(raw).hexdigest() == ent["sha256"], (d, ent["id"])
