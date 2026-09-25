"""D-22 de ACTO GEN2-PISOS-GEN2-2 (24/sep/2026): pisos C2 de cadena limpia de ENIF 2024 y
ENVIPE 2025 y re-adjudicaciones -0002 de las dos celdas-D con C2 legacy.

Specs: forense/prereg-caja/{ENIF2024-PISOS-AHORRO-INFORMAL-LXE,ENVIPE2025-PISOS-EVADE-NORMA-SXD,
DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002,TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002}-spec-v1_0.md.

Todo sobre payloads FABRICADOS (cero microdato real): (a) ramas terminales -- cadena
completa con los controles REPRODUCE, control que no reproduce (el piso no emite IC y el
-0002 PARA), sello falso; (b) guardias (inputs fuera de lista, cruce en la ola reservada);
(c) el -0002 ejecuta los bytes del -0001 y sólo cambia la fuente de C2 (oro del -0001
REPRODUCE sobre el mismo payload); (d) `resultados:` de cada `spec.yaml` = ids emitidos.

Las funciones `cadena_din` y `cadena_tra` también las usa
`forense/analisis/pisos-gen2/genera_esquemas.py` para escribir el `resultados:` de los
cuatro `spec.yaml` desde una corrida sintética (nunca desde el dato).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import random
import sys
import zipfile
from pathlib import Path

import numpy as np
import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
C0 = ROOT / "data" / "corrida0"
PISO_DIN = C0 / "CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001"
PISO_TRA = C0 / "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001"
ADJ2_DIN = C0 / "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002"
ADJ2_TRA = C0 / "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002"
EMIS_DIN = C0 / "CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001"
EMIS_TRA = C0 / "CALC-TRA-EVADE-NORMA-SXD-EMISIONES-0001"
ADJ1_DIN = C0 / "CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001"
ADJ1_TRA = C0 / "CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001"
ARB_ENIF = C0 / "CALC-ARBITRO-MARGINALES-ENIF2024-0001"
ARB_ENVIPE = C0 / "CALC-ARBITRO-MARGINALES-ENVIPE2025-0001"
REPS = 40


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


_C0 = _load(ROOT / "tools" / "corrida0.py", "corrida0_para_pisos_gen2_2")
_MUV = _load(ROOT / "tests" / "test_marginales_una_variable.py", "fixtures_envipe_para_pisos_gen2_2")


def _spec(d):
    return yaml.safe_load((d / "spec.yaml").read_text(encoding="utf-8"))


def _repo(ruta):
    ruta = Path(ruta)
    b = ruta.read_bytes()
    return {"ruta_absoluta": str(ruta), "sha256": hashlib.sha256(b).hexdigest(), "bytes": b}


def _manif(ruta):
    b = Path(ruta).read_bytes()
    return {"ruta_absoluta": str(ruta), "sha256": hashlib.sha256(b).hexdigest(), "bytes": None}


def _sella(tmp, nombre, res):
    rp = Path(tmp) / f"{nombre}_resultados.json"
    rp.write_text(json.dumps({"resultados": res}), encoding="utf-8")
    sp = Path(tmp) / f"{nombre}_sello.json"
    sp.write_text(json.dumps({"resultados.json": hashlib.sha256(rp.read_bytes()).hexdigest()}),
                  encoding="utf-8")
    return _repo(rp), _repo(sp)


def _contrato(d, reps=REPS):
    s = _spec(d)
    par = dict(s["parametros"])
    par["bootstrap_replicas"] = reps
    return {"parametros": par, "seed": s["seed"]}


def _real(d):
    return json.loads((d / "resultados.json").read_text(encoding="utf-8"))["resultados"]


# ─────────────────────────── payloads fabricados ───────────────────────────

def fabrica_enif2024(ruta, n=4000, seed=11):
    rng = random.Random(seed)
    inf = [f"p5_1_{i}" for i in range(1, 7)]
    f9 = [f"p5_6_{i}" for i in range(1, 10)]
    cab = inf + f9 + ["tloc", "edad_v", "fac_per", "est_dis", "upm_dis"]
    filas = []
    for _ in range(n):
        fila = [rng.choice(["1", "2", "2"]) for _ in inf]
        fila += [rng.choice(["1", "2", "2", "2", ""]) for _ in f9]
        fila += [rng.choice(["1", "2", "3", "4"]),
                 rng.choice([str(rng.randrange(18, 98))] * 6 + ["98", "15"]),
                 str(rng.randrange(1, 900)),
                 f"{1 + rng.randrange(5):03d}", f"{1 + rng.randrange(6):05d}"]
        filas.append(fila)
    lineas = [",".join(cab)] + [",".join(f) for f in filas]
    with zipfile.ZipFile(ruta, "w") as zf:
        zf.writestr("conjunto_de_datos_tmodulo_enif2024/conjunto_de_datos/"
                    "conjunto_de_datos_tmodulo_enif2024.csv", "\n".join(lineas) + "\n")


def _con_oro(base, reemplazos):
    d = dict(base)
    d.update(reemplazos)
    return d


# ─────────────────────────── cadenas (piso -> -0001 -> -0002) ───────────────────────────

def cadena_din(tmp, reproduce=True, reps=REPS):
    PISO = _load(PISO_DIN / "medidor.py", "piso_din_pisos_gen2_2")
    ADJ2 = _load(ADJ2_DIN / "medidor.py", "adj2_din_pisos_gen2_2")
    A1 = _load(ADJ1_DIN / "medidor.py", "adj1_din_pisos_gen2_2")
    z = Path(tmp) / "enif2024.zip"
    fabrica_enif2024(z)
    emis_real, arb_real = _real(EMIS_DIN), _real(ARB_ENIF)
    codigo = {"medidor_emisiones": _repo(EMIS_DIN / "medidor.py"),
              "funcion_c2": _repo(ROOT / "tests" / "test_celda_d_c2.py"),
              "extrae_l": _repo(ROOT / "tools" / "extrae_l_v1_1.py")}

    def inputs_piso(emis, arb):
        er, es = _sella(tmp, "emis_din", emis)
        ar, as_ = _sella(tmp, "arb_enif", arb)
        return {"enif2024_csv": _manif(z), **codigo, "emisiones_resultados": er,
                "emisiones_sello": es, "arbitro_enif2024_resultados": ar,
                "arbitro_enif2024_sello": as_}

    ctr = _contrato(PISO_DIN, reps)
    p0 = PISO.medir(inputs_piso(emis_real, arb_real), ctr)
    emis, arb = emis_real, arb_real
    if reproduce:   # el oro fabricado = la propia corrida (mismo payload, misma semilla)
        P, PE = PISO.P, PISO.PE
        rep = {}
        for g in PISO.GRUPOS:
            rep[f"{PE}-G-C2-MARG-{g}-D9-N"] = p0[f"{P}-MARG-{g}-N"]
            for s in ("P", "IC95INF", "IC95SUP"):
                rep[f"{PE}-G-C2-MARG-{g}-D9-{s}"] = p0[f"{P}-MARG-{g}-{s}"]
        # el IC de las emisiones sale de su propio medidor: re-derivado aquí con los mismos bytes
        emis_sint = _sint_emisiones_din(z, reps, ctr["seed"]["valor"])
        for c in PISO.CELDAS:
            rep[f"{PE}-C2-P-REDERIVADO-{c}"] = emis_sint[f"{PE}-C2-P-REDERIVADO-{c}"]
            rep[f"{PE}-C2-IC95INF-{c}"] = emis_sint[f"{PE}-C2-IC95INF-{c}"]
            rep[f"{PE}-C2-IC95SUP-{c}"] = emis_sint[f"{PE}-C2-IC95SUP-{c}"]
        emis = _con_oro(emis_real, rep)
        arep = {}
        for g in ("E1", "E2", "E3"):
            arep[f"{PISO.PA}-{PISO.ARBITRO[g]}-P"] = p0[f"{P}-MARG-{g}-P"]
            arep[f"{PISO.PA}-{PISO.ARBITRO[g]}-N"] = p0[f"{P}-MARG-{g}-N"]
        arb = _con_oro(arb_real, arep)
    inp = inputs_piso(emis, arb)
    piso = PISO.medir(inp, ctr)

    # -0001 sintético sobre el mismo payload y las mismas emisiones fabricadas
    er, es = inp["emisiones_resultados"], inp["emisiones_sello"]
    inp1 = {"enif2024_csv": _manif(z), "emisiones_selladas": er}
    ctr1 = _contrato(ADJ1_DIN, reps)
    out1 = A1.medir(inp1, ctr1)
    a1r, a1s = _sella(tmp, "adj0001_din", out1)
    pr, ps = _sella(tmp, "piso_din", piso)
    inp2 = {"enif2024_csv": _manif(z), "emisiones_selladas": er, "emisiones_sello": es,
            "medidor_0001": _repo(ADJ1_DIN / "medidor.py"), **codigo,
            "adjudicacion_0001_resultados": a1r, "adjudicacion_0001_sello": a1s,
            "piso_c2_resultados": pr, "piso_c2_sello": ps}
    return {"PISO": PISO, "ADJ2": ADJ2, "piso": piso, "out1": out1, "inp2": inp2,
            "ctr2": _contrato(ADJ2_DIN, reps), "inp_piso": inp, "ctr_piso": ctr}


def _sint_emisiones_din(z, reps, semilla):
    """Las emisiones del -0001 son el oro del piso: se re-ejecuta su bloque ENIF 2024 con
    sus propios bytes sobre el payload fabricado (medir completo exige ENIF 2021)."""
    E = _load(EMIS_DIN / "medidor.py", "emis_din_sint_pisos_gen2_2")
    par = _spec(EMIS_DIN)["parametros"]
    inf, f9 = list(par["codigos_informal_2024"]), list(par["codigos_formal_D9_2024"])
    df, _m, _e = E._lee_miembro(z, "conjunto_de_datos_tmodulo_enif2024.csv",
                                inf + f9 + ["tloc", "edad_v", "fac_per", "est_dis", "upm_dis"])
    u = E._universo(df, "edad_v", "tloc", "fac_per", inf + f9)["u"]
    des = E._desenlaces(u, inf, f9, f9)
    tloc, edad = u["tloc"].str.strip().to_numpy(), u["_edad"].to_numpy()
    g = [("L1", np.isin(tloc, par["localidad_L1_tloc"])), ("L2", np.isin(tloc, par["localidad_L2_tloc"])),
         ("E1", (edad >= 18) & (edad <= 29)), ("E2", (edad >= 30) & (edad <= 44)),
         ("E3", (edad >= 45) & (edad <= 59)), ("E4", (edad >= 60) & (edad <= 97)),
         ("NAC", np.ones(len(u), dtype=bool))]
    est, upm = u["est_dis"].str.strip().to_numpy(), u["upm_dis"].str.strip().to_numpy()
    claves = np.array([f"{a}\t{b}" for a, b in zip(est, upm)])
    counts, unicas, _n, _uu = E._replicas(est, upm, semilla, reps)
    W, Y = E._agrega_por_upm(claves, unicas, u["_w"].to_numpy(), E._matriz(g, [("D9", des["D9"])]))
    pt, _lo, _hi, rp = E._punto_e_ic(counts, W, Y)
    ix = {n: i for i, (n, _mk) in enumerate(g)}
    out = {}
    mg = lambda p: {"desenlace_id": E.DESENLACE_D9, "p": float(p)}  # noqa: E731
    for c in E.CELDAS:
        l, e = c.split("x")
        out[f"{E.P}-C2-P-REDERIVADO-{c}"] = E.piso_log_aditivo(
            mg(pt[ix[l], 0]), mg(pt[ix[e], 0]), mg(pt[ix["NAC"], 0]))["p"]
        vals = [E.piso_log_aditivo(mg(a), mg(b), mg(d))["p"]
                for a, b, d in zip(rp[:, ix[l], 0], rp[:, ix[e], 0], rp[:, ix["NAC"], 0])
                if 0 < a < 1 and 0 < b < 1 and 0 < d < 1]
        out[f"{E.P}-C2-IC95INF-{c}"] = float(np.percentile(vals, 2.5))
        out[f"{E.P}-C2-IC95SUP-{c}"] = float(np.percentile(vals, 97.5))
    return out


def cadena_tra(tmp, reproduce=True, reps=REPS):
    PISO = _load(PISO_TRA / "medidor.py", "piso_tra_pisos_gen2_2")
    ADJ2 = _load(ADJ2_TRA / "medidor.py", "adj2_tra_pisos_gen2_2")
    A1 = _load(ADJ1_TRA / "medidor.py", "adj1_tra_pisos_gen2_2")
    z = Path(tmp) / "envipe2025.zip"
    _MUV.fabrica_zip(z, 2025, n_delitos=900)
    emis_real, arb_real = _real(EMIS_TRA), _real(ARB_ENVIPE)
    codigo = {"receta_marginales": _repo(ROOT / "tools" / "celda_d" / "marginales_reproduccion.py"),
              "ejes_l1": _repo(ROOT / "tools" / "ejes_maestra35_l1.py"),
              "calibracion_ic": _repo(ROOT / "tools" / "calibracion_mordida_encig_serie.py")}

    def inputs_piso(emis, arb):
        er, es = _sella(tmp, "emis_tra", emis)
        ar, as_ = _sella(tmp, "arb_envipe", arb)
        return {"envipe2025_csv": _manif(z), **codigo,
                "funcion_c2": _repo(ROOT / "tests" / "test_celda_d_c2.py"),
                "emisiones_resultados": er, "emisiones_sello": es,
                "arbitro_envipe2025_resultados": ar, "arbitro_envipe2025_sello": as_}

    ctr = _contrato(PISO_TRA, reps)
    p0 = PISO.medir(inputs_piso(emis_real, arb_real), ctr)
    emis, arb = emis_real, arb_real
    if reproduce:
        P, PE = PISO.P, PISO.PE
        rep = {f"{PE}-G-M25-P-NACIONAL": p0[f"{P}-MARG-NAC-P"]}
        for g in PISO.GRUPOS:
            rep[f"{PE}-G-M25-MARG-{g}-N"] = p0[f"{P}-MARG-{g}-N"]
            for s in ("P", "IC95INF", "IC95SUP"):
                rep[f"{PE}-G-M25-MARG-{g}-{s}"] = p0[f"{P}-MARG-{g}-{s}"]
        # IC de C2 de las emisiones: misma composición réplica a réplica (su código, líneas 299-308)
        mr = sys.modules["marginales_reproduccion"]
        ola = mr.carga_ola(z, 2025, reservada=True)
        rp = mr.replicas_compartidas(ola, ctr["seed"]["valor"], reps)
        mg = {e: mr.marginal(ola, e, replicas=rp) for e in ("escolaridad_proxy", "dominio_urbano_rural", "nacional")}
        cel = {s: mg["escolaridad_proxy"]["celdas"][mr.ESC_ROTULO[s]] for s in ("S1", "S2", "S3", "S4")}
        cel.update({d: mg["dominio_urbano_rural"]["celdas"][mr.DOM_ROTULO[d]] for d in ("D1", "D2", "D3")})
        cel["NAC"] = mg["nacional"]["celdas"]["NAC"]
        for c in mr.CELDAS:
            s, d = c.split("x")
            rep[f"{PE}-C2-P-REDERIVADO-{c}"] = p0[f"{P}-C2-P-{c}"]
            a, b, n = cel[s]["replicas"], cel[d]["replicas"], cel["NAC"]["replicas"]
            ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(n) & (a > 0) & (a < 1) & (b > 0) & (b < 1) & (n > 0) & (n < 1)
            v = 1 / (1 + np.exp(-(np.log(a[ok] / (1 - a[ok])) + np.log(b[ok] / (1 - b[ok])) - np.log(n[ok] / (1 - n[ok])))))
            rep[f"{PE}-C2-IC95INF-{c}"] = float(np.percentile(v, 2.5))
            rep[f"{PE}-C2-IC95SUP-{c}"] = float(np.percentile(v, 97.5))
        emis = _con_oro(emis_real, rep)
        arb = _con_oro(arb_real, {f"{PISO.PA}-{PISO.ARBITRO[g]}-{s}": p0[f"{P}-MARG-{g}-{s}"]
                                  for g in PISO.GRUPOS + ["NAC"] for s in ("P", "N")})
    inp = inputs_piso(emis, arb)
    piso = PISO.medir(inp, ctr)

    er, es = inp["emisiones_resultados"], inp["emisiones_sello"]
    inp1 = {"envipe2025_csv": _manif(z), "emisiones_selladas": er}
    ctr1 = _contrato(ADJ1_TRA, reps)
    out1 = A1.medir(inp1, ctr1)
    a1r, a1s = _sella(tmp, "adj0001_tra", out1)
    pr, ps = _sella(tmp, "piso_tra", piso)
    inp2 = {"envipe2025_csv": _manif(z), "emisiones_selladas": er, "emisiones_sello": es,
            "medidor_0001": _repo(ADJ1_TRA / "medidor.py"), **codigo,
            "adjudicacion_0001_resultados": a1r, "adjudicacion_0001_sello": a1s,
            "piso_c2_resultados": pr, "piso_c2_sello": ps}
    return {"PISO": PISO, "ADJ2": ADJ2, "piso": piso, "out1": out1, "inp2": inp2,
            "ctr2": _contrato(ADJ2_TRA, reps), "inp_piso": inp, "ctr_piso": ctr}


def valida(calc_dir, out):
    problemas = _C0._valida_outputs(_spec(calc_dir), out)
    assert problemas == [], problemas[:10]
    for k, v in out.items():
        if isinstance(v, float):
            assert np.isfinite(v), (k, v)


CADENAS = {"din": (cadena_din, PISO_DIN, ADJ2_DIN), "tra": (cadena_tra, PISO_TRA, ADJ2_TRA)}


# ─────────────────────────── (a) ramas terminales ───────────────────────────

@pytest.mark.parametrize("k", sorted(CADENAS))
def test_a_cadena_completa_reproduce(tmp_path, k):
    cad, pdir, adir = CADENAS[k]
    r = cad(tmp_path)
    P = r["PISO"].P
    assert r["piso"][f"{P}-G-CTRL-EMISIONES-VEREDICTO"] == "REPRODUCE"
    assert r["piso"][f"{P}-G-C2-IC-ESTADO"] == "EMITIDO"
    assert r["piso"][f"{P}-G-GUARDIA-CRUCE-DERIVADO"] == "NO"
    valida(pdir, r["piso"])
    out2 = r["ADJ2"].medir(r["inp2"], r["ctr2"])
    valida(adir, out2)
    A = r["ADJ2"].P
    assert out2[f"{A}-G-CTRL-ORO-0001-VEREDICTO"] == "REPRODUCE", out2[f"{A}-G-CTRL-ORO-0001-DISCORDAN"]
    assert out2[f"{A}-G-CTRL-ORO-0001-COMPARADOS"] > 0
    for c in (r["PISO"].CELDAS if hasattr(r["PISO"], "CELDAS") else []):
        assert out2[f"{A}-C2-P-{c}"] == r["piso"][f"{P}-C2-P-{c}"]


@pytest.mark.parametrize("k", sorted(CADENAS))
def test_a_control_no_reproduce_no_emite_ic_y_el_0002_para(tmp_path, k):
    cad, pdir, _adir = CADENAS[k]
    r = cad(tmp_path, reproduce=False)
    P = r["PISO"].P
    assert r["piso"][f"{P}-G-CTRL-EMISIONES-VEREDICTO"] == "NO-REPRODUCE"
    assert r["piso"][f"{P}-G-C2-IC-ESTADO"].startswith("NO-EMITIDO")
    valida(pdir, r["piso"])
    with pytest.raises(r["ADJ2"].ParoDeGuardia):
        r["ADJ2"].medir(r["inp2"], r["ctr2"])


# ─────────────────────────── (b) guardias ───────────────────────────

@pytest.mark.parametrize("k", sorted(CADENAS))
def test_b_inputs_fuera_de_lista_y_sello_falso(tmp_path, k):
    cad, _p, _a = CADENAS[k]
    r = cad(tmp_path)
    extra = dict(r["inp_piso"], intruso=r["inp_piso"]["emisiones_resultados"])
    with pytest.raises(r["PISO"].ParoDeGuardia):
        r["PISO"].medir(extra, r["ctr_piso"])
    falso = dict(r["inp2"], piso_c2_sello=r["inp2"]["emisiones_sello"])
    with pytest.raises(r["ADJ2"].ParoDeGuardia):
        r["ADJ2"].medir(falso, r["ctr2"])


def test_b_piso_din_rechaza_agrupacion_de_dos_ejes():
    PISO = _load(PISO_DIN / "medidor.py", "piso_din_guardia_pisos_gen2_2")
    g = PISO._Guardia()
    g.registra(["edad"])
    with pytest.raises(PISO.ParoDeGuardia):
        g.registra(["localidad", "edad"])


# ─────────────────────────── (c) herencia ───────────────────────────

@pytest.mark.parametrize("adir,a1", [(ADJ2_DIN, ADJ1_DIN), (ADJ2_TRA, ADJ1_TRA)])
def test_c_el_0002_hereda_por_sha_los_bytes_y_parametros_del_0001(adir, a1):
    s2, s1 = _spec(adir), _spec(a1)
    med = next(i for i in s2["inputs"] if i["id"] == "medidor_0001")
    assert med["ruta"] == str((a1 / "medidor.py").relative_to(ROOT))
    assert med["sha256"] == hashlib.sha256((a1 / "medidor.py").read_bytes()).hexdigest()
    p2 = {k: v for k, v in s2["parametros"].items() if k != "tol_oro_0001"}
    assert p2 == s1["parametros"]
    assert s2["seed"] == s1["seed"]


# ─────────────────────────── (d) esquema ───────────────────────────

def test_d_inputs_de_repo_existen_con_su_sha():
    for d in (PISO_DIN, PISO_TRA, ADJ2_DIN, ADJ2_TRA):
        for i in _spec(d)["inputs"]:
            if i.get("origen") != "repo":
                continue
            ruta = ROOT / i["ruta"]
            if not ruta.exists():           # piso aún no sellado (antes del COMMIT-3a)
                assert i["id"].startswith("piso_c2_"), i["id"]
                continue
            assert hashlib.sha256(ruta.read_bytes()).hexdigest() == i["sha256"], i["id"]
