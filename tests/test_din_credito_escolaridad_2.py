#!/usr/bin/env python3
"""Falsadores de CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002
(ACTO GEN2-DIN-CREDITO-ESCOLARIDAD-2, COMMIT-1: spec congelada sin abrir
microdato).

NUNCA abre `data/raw/enif2024_csv.zip`: fabrica ZIP sintéticos con la forma
de columnas de TMODULO 2024. Los insumos sellados que lee (medidor y
resultados del `-0001`, emisiones del `-EMISIONES-0001`, el adjudicador del
commit_3 y `cruces_familia.py`) son archivos del repo, no microdato.

Defecto real que atrapa (el del `-0001`): `_code()` le quitaba el cero a
`niv` y tres cubos de escolaridad salían vacíos; el test del `-0001` sólo
exigía que las categorías vistas fueran un SUBCONJUNTO de la rejilla, y un
cubo vacío lo satisface. Aquí se exigen los cuatro cubos y el mapa código
por código.

1. Mapa por texto: `NIV_A_ESCOLARIDAD_POR_TEXTO` == `NIV_A_ESCOLARIDAD` del
   `-0001` (el mapa era correcto; el defecto era `_code`), 12 códigos, sin 99.
2. D-22: `niv=01` -> hasta_primaria y `niv=10` -> superior, con dos dígitos
   y con uno solo ("1").
3. La guardia sellada sigue parando (ReservaRota) antes de abrir el ZIP.
4. `medir()` sobre sintético: `_valida_outputs == []`, los cuatro cubos con
   N>0, N-SIN-CUBO == filas 99, sin no-finitos; un sintético con `niv` de un
   dígito da la MISMA salida que el de dos dígitos.
5. Ramas terminales: cubo con masa cero (sin `03`), celda rara (P=0),
   cero puntuadas (R vacío) -- el conducto acepta las tres.
6. Oro del conducto: la regla importada, con la exclusión original, sobre el
   R real del `-0001`, reproduce `duelo-credito-prediccion-2024.json`.
7. `_oro()`: idéntico -> REPRODUCE-ORO; un valor a 1e-9 -> NO-REPRODUCE-ORO.
8. `resultados:` del spec.yaml == `esquema_resultados()` del medidor.

Corre standalone y expone `corre()`.
"""
from __future__ import annotations

import io
import json
import math
import sys
import tempfile
import types
import zipfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import corrida0 as C  # noqa: E402

CALC = ROOT / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ESCOLARIDAD-0002"
CALC_0001 = ROOT / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-ADJUDICACION-0001"
EMIS = ROOT / "data/corrida0/CALC-DIN-CREDITO-PREDICCION-2024-EMISIONES-0001/resultados.json"
DUELO = ROOT / "data/corrida0/duelo-credito-prediccion-2024.json"
MIEMBRO = "conjunto_de_datos_tmodulo_enif2024.csv"
NIV = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "99"]
REPOS = {
    "MEDIDOR-EJES-0003": ROOT / "data/corrida0/CALC-PISOS-ENIF2021-EJES-0003/medidor.py",
    "MEDIDOR-ADJ-0001": CALC_0001 / "medidor.py",
    "R-ADJ-0001": CALC_0001 / "resultados.json",
    "EMISIONES-0001": EMIS,
    "ADJUDICADOR-0001": ROOT / "tools/duelo/credito_prediccion_2024.py",
    "CRUCES-FAMILIA": ROOT / "tools/duelo/cruces_familia.py",
}
CONTRATO = {"parametros": {"bootstrap_replicas": 60, "oro_tolerancia_abs": 1.0e-10},
            "seed": {"valor": 42}}


def _modulo():
    src = (CALC / "medidor.py").read_bytes()
    mod = types.ModuleType("medidor_escolaridad_0002")
    exec(compile(src, str(CALC / "medidor.py"), "exec"), mod.__dict__)
    return mod


def _payload(n=1500, semilla=11, niv_pool=NIV, un_digito=False, rara_superior=False) -> bytes:
    rng = np.random.default_rng(semilla)
    cols = ([f"p6_2_{k}" for k in range(1, 10)] + [f"p6_3_{k}" for k in range(1, 10)]
            + [f"p6_1_{k}" for k in range(1, 6)]
            + ["p6_13", "p6_14", "p6_16", "p3_10", "sexo", "edad_v", "tloc", "niv",
               "fac_per", "est_dis", "upm_dis"])
    filas = []
    for i in range(n):
        est = 1 + i % 10
        upm = est * 10 + rng.integers(0, 4)
        niv = str(rng.choice(niv_pool))
        prod = ["1" if rng.random() < p else "2" for p in
                (0.20, 0.08, 0.06, 0.05, 0.02, 0.10, 0.02, 0.01, 0.01)]
        if rara_superior and NIV.index(niv) in range(8, 12):
            prod[4] = "2"   # K2-AUTOMOTRIZ: P=0 en ESCOLARIDAD-SUPERIOR -> celda rara
        tenedor = "1" in prod
        atr = ["" if pk != "1" else rng.choice(["1", "2", "2", "2"]) for pk in prod]
        inf = [rng.choice(["1", "2"], p=[q, 1 - q]) for q in (.05, .04, .15, .2, .01)]
        p13 = "" if tenedor else rng.choice(["1", "2"], p=[.3, .7])
        p14 = str(rng.integers(1, 10)) if (not tenedor and p13 == "2") else ""
        p16 = rng.choice(["1", "2", "3"], p=[.12, .38, .5])
        p310 = rng.choice(list("1234569"), p=[.35, .05, .02, .03, .02, .5, .03])
        if un_digito and niv != "99":
            niv = str(int(niv))
        filas.append(prod + atr + inf + [
            p13, p14, p16, p310, str(rng.integers(1, 3)),
            str(rng.integers(18, 99)), str(rng.integers(1, 5)), niv,
            str(rng.integers(500, 5000)), f"{est:03d}", f"{upm:07d}"])
    csv = ",".join(cols) + "\n" + "\n".join(",".join(f) for f in filas) + "\n"
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(MIEMBRO, csv.encode("utf-8"))
    return buf.getvalue()


def _inputs(zip_path: str) -> dict:
    d = {"enif2024_csv": {"ruta_absoluta": zip_path, "bytes": None}}
    for k, p in REPOS.items():
        d[k] = {"ruta_absoluta": str(p), "bytes": p.read_bytes()}
    return d


def _spec():
    import yaml
    return yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))


def _medir(mod, td, nombre, **kw):
    zp = Path(td) / nombre
    zp.write_bytes(_payload(**kw))
    return mod.medir(_inputs(str(zp)), CONTRATO)


def _no_finitos(out):
    return [k for k, v in out.items() if isinstance(v, float) and not math.isfinite(v)]


def _falsa_mapa(mod, errores):
    src = (CALC_0001 / "medidor.py").read_bytes()
    m1 = types.ModuleType("m1")
    exec(compile(src, "m1", "exec"), m1.__dict__)
    if mod.NIV_A_ESCOLARIDAD_POR_TEXTO != m1.NIV_A_ESCOLARIDAD:
        errores.append("el mapa por texto difiere del NIV_A_ESCOLARIDAD del -0001")
    if sorted(mod.NIV_A_ESCOLARIDAD_POR_TEXTO) != NIV[:-1]:
        errores.append("el mapa no cubre exactamente 00..11")
    import pandas as pd
    s = pd.Series(["01", "10", "1", "99", "", " 08", "9"])
    v = mod._niv_dos_digitos(s)
    if list(v) != ["01", "10", "01", "99", "", "08", "09"]:
        errores.append(f"_niv_dos_digitos: {list(v)}")
    cubo = v.map(mod.NIV_A_ESCOLARIDAD_POR_TEXTO)
    if cubo[0] != "hasta_primaria" or cubo[1] != "superior" or cubo[2] != "hasta_primaria":
        errores.append(f"D-22 niv=01/10: {list(cubo)}")
    if not (pd.isna(cubo[3]) and pd.isna(cubo[4])):
        errores.append("niv 99/vacío recibió cubo")


def _falsa_guardia(mod, errores):
    m1 = mod._modulo_0001(_inputs("/no/existe/nada.zip"))
    for malo in ("K1-NO-EXISTE", ["K1"], "*", "", None, "k1"):
        try:
            m1.abre_conducta_2024(_inputs("/no/existe/nada.zip"), malo, {})
            errores.append(f"la guardia dejó pasar {malo!r}")
        except m1.ReservaRota:
            pass
        except Exception as exc:  # noqa: BLE001
            errores.append(f"{malo!r} reventó con {exc!r} en vez de ReservaRota")


def _falsa_medir(mod, spec, td, errores):
    out = _medir(mod, td, "normal.zip")
    prob = C._valida_outputs(spec, out)
    if prob:
        errores.append(f"normal: _valida_outputs: {prob[:5]}")
    if _no_finitos(out):
        errores.append(f"normal: no finitos {_no_finitos(out)[:3]}")
    b = f"RESULT-{mod.PREFIJO}-K1"
    for c in mod.CUBOS:
        if not out[f"{b}-ESCOLARIDAD-{c}-N"] > 0:
            errores.append(f"normal: cubo {c} vacío")
    suma = sum(out[f"{b}-ESCOLARIDAD-{c}-N"] for c in mod.CUBOS)
    if suma + out[f"{b}-ESCOLARIDAD-N-SIN-CUBO"] != out[f"{b}-NACIONAL-TODOS-N"]:
        errores.append("normal: N por cubo + sin cubo != nacional")
    if out[f"{b}-ESCOLARIDAD-N-SIN-CUBO"] <= 0:
        errores.append("normal: el sintético trae 99 y N-SIN-CUBO salió 0")

    uno = _medir(mod, td, "un_digito.zip", un_digito=True)
    dif = sorted(k for k in out if out[k] != uno.get(k)
                 and not (isinstance(out[k], float) and isinstance(uno.get(k), float)
                          and math.isnan(out[k]) and math.isnan(uno[k])))
    dif = [k for k in dif if "-ORO-" not in k]
    if dif:
        errores.append(f"niv de un dígito cambia la salida: {dif[:5]}")

    sin03 = _medir(mod, td, "sin03.zip", niv_pool=[x for x in NIV if x != "03"])
    prob = C._valida_outputs(spec, sin03)
    if prob:
        errores.append(f"masa cero: _valida_outputs: {prob[:5]}")
    if sin03[f"{b}-ESCOLARIDAD-SECUNDARIA-N"] != 0 or sin03[f"{b}-ESCOLARIDAD-SECUNDARIA-P"] is not None:
        errores.append("masa cero: SECUNDARIA no quedó N=0/P=None")

    rara = _medir(mod, td, "rara.zip", rara_superior=True)
    prob = C._valida_outputs(spec, rara)
    if prob:
        errores.append(f"celda rara: _valida_outputs: {prob[:5]}")
    if rara[f"RESULT-{mod.PREFIJO}-K2-AUTOMOTRIZ-ESCOLARIDAD-SUPERIOR-P"] != 0.0:
        errores.append("celda rara: K2-AUTOMOTRIZ SUPERIOR no salió P=0")


def _r_0001_como_esc2(mod):
    r = json.loads((CALC_0001 / "resultados.json").read_text())["resultados"]
    a, b = f"RESULT-{mod.PREFIJO_0001}-", f"RESULT-{mod.PREFIJO}-"
    return {(b + k[len(a):] if k.startswith(a) else k): v for k, v in r.items()}


def _falsa_oro_conducto(mod, spec, errores):
    inputs = _inputs("/no/existe/nada.zip")
    antes_mod, antes_path = sys.modules.get("cruces_familia"), list(sys.path)
    adj = mod._modulo_adjudicador(inputs)
    if sys.modules.get("cruces_familia") is not antes_mod or sys.path != antes_path:
        errores.append("_modulo_adjudicador dejó sys.modules/sys.path alterados")
    emis = json.loads(EMIS.read_text())["resultados"]
    r = _r_0001_como_esc2(mod)
    duelo = json.loads(DUELO.read_text())["conductas"]
    res12 = mod.adjudica_bloque(adj, r, emis, excluye_escolaridad=True)
    for cid, d in duelo.items():
        x = res12[cid]
        if x["retador_primario"] != d["retador_primario"]:
            errores.append(f"oro12 {cid}: retador {x['retador_primario']} != {d['retador_primario']}")
            continue
        ret = d["retador_primario"]
        if ret:
            a, b = x["adjudicacion_por_retador"][ret], d["adjudicacion_por_retador"][ret]
            if (a["veredicto"], a["delta_mae_pp"], list(a["delta_ic95"])) != \
                    (b["veredicto"], b["delta_mae_pp"], list(b["delta_ic95"])):
                errores.append(f"oro12 {cid}: {a['veredicto']} {a['delta_mae_pp']} != "
                               f"{b['veredicto']} {b['delta_mae_pp']}")
        if x["n_celdas_elegibles"] != d["n_celdas_elegibles"]:
            errores.append(f"oro12 {cid}: n_celdas_elegibles distinto")
    # ADJ16 sobre el R roto del -0001 (3 cubos sin R): rama parcial, no revienta
    res16 = mod.adjudica_bloque(adj, r, emis, excluye_escolaridad=False)
    if res16["K1"]["n_celdas_elegibles"] != 13:
        errores.append(f"parcial: K1 elegibles {res16['K1']['n_celdas_elegibles']} != 13")
    # cero puntuadas: R vacío
    vacio = {k: None for k in r}
    res0 = mod.adjudica_bloque(adj, vacio, emis, excluye_escolaridad=False)
    ids = {e["id"]: e for e in spec["resultados"]}
    for etiqueta, resx, completo in (("ADJ16", res16, True), ("ADJ16", res0, True),
                                     ("ORO12", res12, False)):
        plano = mod._aplana(resx, etiqueta, completo)
        sub = {"resultados": [ids[k] for k in plano if k in ids]}
        faltan = [k for k in plano if k not in ids]
        if faltan:
            errores.append(f"{etiqueta}: ids no declarados {faltan[:3]}")
        prob = C._valida_outputs(sub, plano)
        if prob:
            errores.append(f"{etiqueta}: _valida_outputs {prob[:3]}")


def _falsa_oro(mod, errores):
    r1 = json.loads((CALC_0001 / "resultados.json").read_text())["resultados"]
    r = _r_0001_como_esc2(mod)
    o = mod._oro(r, r1, 1e-10)
    p = f"RESULT-{mod.PREFIJO}-ORO"
    if o[f"{p}-VEREDICTO"] != "REPRODUCE-ORO" or o[f"{p}-N-COMPARADOS"] != 666:
        errores.append(f"_oro idéntico: {o}")
    k = f"RESULT-{mod.PREFIJO}-K1-NACIONAL-TODOS-P"
    r2 = dict(r)
    r2[k] = r[k] + 1e-9
    o2 = mod._oro(r2, r1, 1e-10)
    if o2[f"{p}-VEREDICTO"] != "NO-REPRODUCE-ORO" or o2[f"{p}-N-DISCORDANTES"] != 1:
        errores.append(f"_oro perturbado: {o2}")


def _falsa_esquema(mod, spec, errores):
    if spec["resultados"] != mod.esquema_resultados():
        errores.append("resultados: del spec.yaml no es esquema_resultados()")


def corre() -> list[str]:
    errores: list[str] = []
    for p in (CALC / "medidor.py", CALC / "spec.yaml", *REPOS.values(), DUELO):
        if not p.exists():
            errores.append(f"falta {p.relative_to(ROOT)}")
    if errores:
        return errores
    mod = _modulo()
    spec = _spec()
    _falsa_mapa(mod, errores)
    _falsa_guardia(mod, errores)
    _falsa_esquema(mod, spec, errores)
    _falsa_oro(mod, errores)
    _falsa_oro_conducto(mod, spec, errores)
    with tempfile.TemporaryDirectory() as td:
        _falsa_medir(mod, spec, td, errores)
    return errores


def main() -> int:
    errores = corre()
    for e in errores:
        print("FALLA --", e)
    if not errores:
        print("PASA -- tests/test_din_credito_escolaridad_2.py (mapa por texto; niv 01/10 con "
              "dos dígitos y con uno; guardia sellada; medir() sintético con 4 cubos; ramas "
              "masa cero / celda rara / cero puntuadas; oro del conducto reproduce el duelo "
              "del -0001; _oro; esquema)")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
