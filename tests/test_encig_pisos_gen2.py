"""D-22 de ACTO GEN2-ENCIG-PISOS-GEN2-1 (24/sep/2026): piso C2 de cadena limpia
(CALC-ENCIG2025-PISOS-GOBDIGITAL-0001) y re-adjudicación -0002.

Specs: forense/prereg-caja/ENCIG2025-PISOS-GOBDIGITAL-spec-v1_0.md §5 y
forense/prereg-caja/ENCIG-DUELO-2025-ADJUDICACION-0002-spec-v1_0.md §2. Reutiliza los
fixtures sintéticos de tests/test_encig_duelo_2025.py (cargado por ruta, sin re-coleccionar
sus tests) para que el -0001 sintético, el piso y el -0002 corran sobre el mismo payload.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os

import numpy as np
import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C0001 = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG-DUELO-2025-ADJUDICACION-0001")
PISO_DIR = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG2025-PISOS-GOBDIGITAL-0001")
ADJ2_DIR = os.path.join(ROOT, "data", "corrida0", "CALC-ENCIG-DUELO-2025-ADJUDICACION-0002")
RAW = os.path.join(ROOT, "data", "raw")


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


T = _load(os.path.join(ROOT, "tests", "test_encig_duelo_2025.py"), "fixtures_duelo_para_pisos_gen2")
D = T.D
PISO = _load(os.path.join(PISO_DIR, "medidor.py"), "piso_gen2_encig2025")
ADJ2 = _load(os.path.join(ADJ2_DIR, "medidor.py"), "adj2_duelo_encig2025")


def _spec(d):
    with open(os.path.join(d, "spec.yaml"), encoding="utf-8") as f:
        return yaml.safe_load(f)


def contrato_piso(reps=40, ola="2025"):
    par = dict(_spec(PISO_DIR)["parametros"])
    par["bootstrap_replicas"], par["ola"] = reps, ola
    return {"parametros": par, "seed": {"aplica": True, "valor": 20260919, "rng": "numpy.PCG64"}}


def contrato_adj2(reps=40):
    par = dict(_spec(ADJ2_DIR)["parametros"])
    par["bootstrap_replicas"] = reps
    return {"parametros": par, "seed": {"aplica": True, "valor": 20260919, "rng": "numpy.PCG64"}}


def _sella_json(tmp_path, nombre, res):
    rp = tmp_path / f"{nombre}_resultados.json"
    rp.write_text(json.dumps({"resultados": res}), encoding="utf-8")
    sp = tmp_path / f"{nombre}_sello.json"
    sp.write_text(json.dumps({"resultados.json": hashlib.sha256(rp.read_bytes()).hexdigest()}), encoding="utf-8")
    return T._repo(str(rp)), T._repo(str(sp))


def cadena(tmp_path, reps=40, **kw):
    """-0001 sintético -> piso -> -0002, sobre el mismo payload sintético."""
    emis, arb = T.escenario(tmp_path, reps=reps, **kw)
    emitidas = T.corre_emisiones(tmp_path, emis)
    arb1 = T.sella(tmp_path, arb, emitidas)
    out1 = D.medir(arb1, T.contrato_arbitro(reps))
    adj0001, _ = _sella_json(tmp_path, "adj0001", out1)
    inp_piso = {"encig25_base_datos_csv": arb["encig25_base_datos_csv"],
                "receta_cruce_encig": T._repo(T.RECETA),
                "marginales_2025_resultados": arb["marginales_2025_resultados"],
                "adjudicacion_0001_resultados": adj0001}
    piso = PISO.medir(inp_piso, contrato_piso(reps))
    return arb1, out1, adj0001, inp_piso, piso


def corre_adj2(tmp_path, arb1, adj0001, piso, reps=40):
    pr, ps = _sella_json(tmp_path, "piso", piso)
    arb2 = dict(arb1, piso_c2_resultados=pr, piso_c2_sello=ps, adjudicacion_0001_resultados=adj0001)
    return ADJ2.medir(arb2, contrato_adj2(reps))


def valida(calc_dir, out):
    problemas = T.C0._valida_outputs(_spec(calc_dir), out)
    assert problemas == [], problemas[:10]
    for k, v in out.items():
        if isinstance(v, float):
            assert np.isfinite(v), (k, v)


# ─────────────────────────── (a) sintética: ramas terminales ───────────────────────────

def test_a_cadena_completa_con_soporte(tmp_path):
    arb1, out1, adj0001, _, piso = cadena(tmp_path)
    valida(PISO_DIR, piso)
    P = PISO.P
    assert piso[f"{P}-G-CTRL-MARGINALES-VEREDICTO"] == "REPRODUCE"
    assert piso[f"{P}-G-CTRL-0001-VEREDICTO"] == "REPRODUCE"      # misma composición y réplicas que el árbitro
    assert piso[f"{P}-G-CTRL-C2-SELLADO-VEREDICTO"] == "REPRODUCE"  # C2 sintético a 6 decimales
    assert piso[f"{P}-G-ORIGEN"].startswith("NUEVO")
    out2 = corre_adj2(tmp_path, arb1, adj0001, piso)
    valida(ADJ2_DIR, out2)
    assert out2[f"{ADJ2.PA}-G-CTRL-ORO-0001-VEREDICTO"] == "REPRODUCE"
    assert out2[f"{ADJ2.PA}-G-CTRL-ORO-0001-N"] == 16 * 13 + 22   # 13 sufijos por celda + 11 marginales × (P, N)
    for cruce in D.CRUCES:
        for ka, kb in D.celdas(cruce):
            b2 = f"{ADJ2.PA}-{cruce}-{D.rotulo(ka, kb)}"
            b1 = f"{D.PA}-{cruce}-{D.rotulo(ka, kb)}"
            assert out2[f"{b2}-C2-P"] == piso[PISO.id_c2(cruce, ka, kb, "C2-P")]
            assert out2[f"{b2}-C2-P-EMISION-0001"] == out1[f"{b1}-C2-P"]
            assert out2[f"{b2}-R-P"] == out1[f"{b1}-R-P"]
        assert out2[f"{ADJ2.PA}-{cruce}-G-CTRL-C2-VEREDICTO"] == "REPRODUCE"


def test_a_categoria_con_masa_cero(tmp_path):
    arb1, _, adj0001, _, piso = cadena(tmp_path, zip_kw={"sin_60": True})
    valida(PISO_DIR, piso)
    assert piso[PISO.id_c2("EDADXSEXO", "60-96", "1", "C2-P")] is None
    # un marginal vacío no tiene par sellado: el control no reproduce y el árbitro PARA
    # (spec -0002 §2, `_guardia_piso`) -- rama terminal declarada, no un defecto
    assert piso[f"{PISO.P}-G-CTRL-MARGINALES-VEREDICTO"] == "NO-REPRODUCE"
    with pytest.raises(ADJ2.ParoDeGuardia, match="CTRL-MARGINALES"):
        corre_adj2(tmp_path, arb1, adj0001, piso)


def test_a_celda_vaciada_en_una_replica(tmp_path):
    arb1, _, adj0001, _, piso = cadena(tmp_path, zip_kw={"rara": True})
    valida(PISO_DIR, piso)
    out2 = corre_adj2(tmp_path, arb1, adj0001, piso)
    valida(ADJ2_DIR, out2)


def test_a_control_no_reproduce_no_emite_ic_y_el_arbitro_para(tmp_path):
    arb1, _, adj0001, _, piso = cadena(tmp_path, perturba_marg=True)
    valida(PISO_DIR, piso)
    assert piso[f"{PISO.P}-G-CTRL-MARGINALES-VEREDICTO"] == "NO-REPRODUCE"
    assert piso[PISO.id_c2("EDADXSEXO", "18-29", "1", "C2-IC-LO")] is None
    with pytest.raises(ADJ2.ParoDeGuardia, match="CTRL-MARGINALES"):
        corre_adj2(tmp_path, arb1, adj0001, piso)


# ─────────────────────────── (b) oro sobre 2023 (CAJA) ───────────────────────────

@pytest.mark.skipif(not os.path.isdir(RAW), reason="corpus no montado (NUBE): el oro solo corre en CAJA")
def test_b_oro_encig2023_reproduce_pisos_ejes_sellados(tmp_path):
    z23 = T._zip_2023()
    assert z23, "encig23_base_datos_csv no COINCIDE en el manifiesto"
    vacio = T._json_input(tmp_path, "vacio.json", {})
    inp = {"encig25_base_datos_csv": {"origen": "manifiesto", "ruta_absoluta": z23, "sha256": "oro-2023"},
           "receta_cruce_encig": T._repo(T.RECETA), "marginales_2025_resultados": vacio,
           "adjudicacion_0001_resultados": vacio}
    out = PISO.medir(inp, contrato_piso(200, ola="2023"))
    valida(PISO_DIR, out)
    pisos = json.load(open(os.path.join(ROOT, "data", "corrida0", "CALC-PISOS-ENCIG2023-EJES-0002",
                                        "resultados.json")))["resultados"]
    peor = max(abs(out[PISO.id_marginal(eje, v, "P")] - pisos[D.id_piso_2023(eje, v)])
               for eje, valores in PISO.EJES.items() for v in valores)
    assert peor < 1e-10, peor


# ─────────────────────────── (c) guardias ───────────────────────────

def test_c_mascara_de_dos_ejes_rompe(tmp_path):
    frame, _ = T._frame(T.fabrica_zip(tmp_path, "2025", n_personas=400), "2025")
    with pytest.raises(PISO.ReservaRota):
        PISO._mascara1(frame, ("EDAD", "SEXO"), ("18-29", "1"))
    with pytest.raises(PISO.ReservaRota):
        PISO._mascara1(frame, "OTRO", "x")


def test_c_piso_inputs_fuera_de_lista(tmp_path):
    _, _, _, inp, _ = cadena(tmp_path, reps=10)
    mal = dict(inp, emisiones_edadxsexo_resultados=inp["marginales_2025_resultados"])
    with pytest.raises(PISO.ParoDeGuardia, match="fuera de la lista"):
        PISO.medir(mal, contrato_piso(10))


def test_c_arbitro_para_con_sello_de_piso_falso_o_sin_origen_nuevo(tmp_path):
    arb1, _, adj0001, _, piso = cadena(tmp_path, reps=10)
    pr, _ = _sella_json(tmp_path, "piso", piso)
    _, falso = _sella_json(tmp_path, "otro", {"x": 1})
    with pytest.raises(ADJ2.ParoDeGuardia, match="sello del piso"):
        ADJ2.medir(dict(arb1, piso_c2_resultados=pr, piso_c2_sello=falso, adjudicacion_0001_resultados=adj0001),
                   contrato_adj2(10))
    sin = dict(piso)
    sin[f"{PISO.P}-G-ORIGEN"] = "HEREDADO"
    with pytest.raises(ADJ2.ParoDeGuardia, match="origen NUEVO"):
        corre_adj2(tmp_path, arb1, adj0001, sin, reps=10)


# ─────────────────────────── (d) mutación ───────────────────────────

MUTANTES_PISO = {
    "eq fuera de _mascara1": ("    masks.append(_mascara1(frame, None, None))\n",
                              "    masks.append(frame['EDAD'].eq('18-29') & frame['SEXO'].eq('1'))\n"),
    "_mascara1 con otra firma": ("def _mascara1(frame, eje, valor):", "def _mascara1(frame, eje, valor, otro=None):"),
    "_mascara1 sin guardia": ('        raise ReservaRota(f"agrupacion no autorizada: {eje!r}")', "        pass"),
    "bootstrap fuera de _marginales": ("    res = _marginales(receta, frame, repeticiones, semilla)\n",
                                       "    res = _marginales(receta, frame, repeticiones, semilla)\n"
                                       "    receta._bootstrap(frame, [], 1, 1)\n"),
    "medir sin guardia": ("    payload = _guardia_inputs(inputs, contrato)\n",
                          '    payload = str(contrato["parametros"]["payload_id"])\n'),
}


def test_d_mutantes_del_piso_atrapados():
    fuente = open(os.path.join(PISO_DIR, "medidor.py"), encoding="utf-8").read()
    assert PISO.auditoria(fuente) == []
    for nombre, (viejo, nuevo) in MUTANTES_PISO.items():
        assert fuente.count(viejo) == 1, nombre
        assert PISO.auditoria(fuente.replace(viejo, nuevo)) != [], nombre


def test_d_mutantes_del_duelo_atrapados_en_el_0002():
    fuente = open(os.path.join(ADJ2_DIR, "medidor.py"), encoding="utf-8").read()
    assert ADJ2.auditoria(fuente) == []
    for nombre, (viejo, nuevo) in T.MUTANTES.items():
        assert fuente.count(viejo) == 1, nombre
        mutante = fuente.replace(viejo, nuevo)
        if nombre == "mascara sin guardia":
            mutante = mutante.replace('        raise ReservaRota(f"universo de par no autorizado: {par_universo}")', '        pass')
        assert ADJ2.auditoria(mutante) != [], nombre
    sin_piso = fuente.replace("    piso = _guardia_piso(inputs)\n", "    piso = {}\n")
    assert ADJ2.auditoria(sin_piso) != []


# ─────────────────────────── (e) herencia por sha: sólo el diff declarado ───────────────────────────

CAMBIADAS = {"adjudicar", "adjudicacion", "esquema_adjudicacion", "_fila",
             "_guardia_piso", "_control_oro_0001", "id_piso_c2",
             "PA", "PA0001", "PISO", "INPUTS_ADJUDICACION_REPO", "_GUARDIAS_DE_ENTRADA"}


def _nodos(fuente):
    out = {}
    for n in ast.parse(fuente).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out[n.name] = ast.dump(n)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = ast.dump(n.value)
    return out


def test_e_el_0002_hereda_el_0001_salvo_el_diff_declarado():
    m1 = open(os.path.join(C0001, "medidor.py"), "rb").read()
    assert hashlib.sha256(m1).hexdigest() == "74e8aa49938616299f7464e4a7cf8a94a46b83a3550ec52552587510debf86d4"
    a, b = _nodos(m1.decode("utf-8")), _nodos(open(os.path.join(ADJ2_DIR, "medidor.py"), encoding="utf-8").read())
    distintas = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
    assert distintas == CAMBIADAS, sorted(distintas ^ CAMBIADAS)


# ─────────────────────────── (f) identidad de esquema e inputs ───────────────────────────

def test_f_resultados_del_spec_son_el_esquema():
    assert _spec(PISO_DIR)["resultados"] == PISO.esquema_resultados()
    assert _spec(ADJ2_DIR)["resultados"] == ADJ2.esquema_adjudicacion()


def test_f_c2_del_0002_depende_solo_del_piso():
    for r in _spec(ADJ2_DIR)["resultados"]:
        if r["id"].endswith("-C2-P"):
            assert r.get("dependencias_numericas") == ["piso_c2_resultados"], r["id"]
    for r in _spec(PISO_DIR)["resultados"]:
        if r["id"].endswith("-C2-P"):
            assert r.get("dependencias_numericas") == ["encig25_base_datos_csv"], r["id"]


def test_f_inputs_de_los_spec_existen_con_su_sha():
    for d in (PISO_DIR, ADJ2_DIR):
        for ent in _spec(d)["inputs"]:
            if ent.get("origen") != "repo" or "sha256" not in ent:
                continue
            raw = open(os.path.join(ROOT, ent["ruta"]), "rb").read()
            assert hashlib.sha256(raw).hexdigest() == ent["sha256"], (d, ent["id"])
