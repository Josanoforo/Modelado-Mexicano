"""Prueba sintética del conducto (D-22 (2)-(3)) para CALC-*-SERIE-DICTAMEN-0001:
fabrica resultados.json con valores aleatorios en la forma que el mapa cita
(ids planos y celdas de tabla), corre `medir` y pasa la salida por
`corrida0._fallas_run`. No lee ningún valor real.

Uso: PYTHONPATH=. python3 tools/series/sintetico_conducto.py [semilla] [escenario]
escenario: aleatorio | constante | cero-validas
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

import yaml

from tools import corrida0 as C0
from tools.series import calc_serie as S, dictamen as D

RAIZ = Path(__file__).resolve().parents[2]


def fabrica(filas, rng, escenario):
    planos, tablas = defaultdict(dict), defaultdict(dict)
    for f in filas:
        base_p = rng.uniform(.05, .95) if escenario != "constante" else .4
        for col in ("result_p", "result_lo", "result_hi"):
            i = f[col]
            if not i:
                continue
            v = {"result_p": base_p, "result_lo": base_p - .01, "result_hi": base_p + .01}[col]
            if escenario == "cero-validas":
                v = 1.5
            if "#" not in i:
                planos[f["calc"]][i] = v
                continue
            base, resto = i.split("#", 1)
            bloque, campo = resto.rsplit("/", 1)
            llave = tuple((k, unquote(x)) for k, x in (p.split("=", 1) for p in bloque.split("&")))
            celda = tablas[(f["calc"], base)].setdefault(llave, dict(llave))
            if "[" in campo:
                n, j = campo[:-1].split("[")
                celda.setdefault(n, [None, None])[int(j)] = v
            else:
                celda[campo] = v
    out = defaultdict(dict)
    for c, d in planos.items():
        out[c].update(d)
    for (c, base), celdas in tablas.items():
        out[c][base] = json.dumps(list(celdas.values()))
    return out


def corre(calc, seed, escenario):
    d = RAIZ / "data/corrida0" / calc
    spec = yaml.safe_load((d / "spec.yaml").read_text(encoding="utf-8"))
    par = spec["parametros"]
    insts = set(par["instrumento"]) if isinstance(par["instrumento"], list) else {par["instrumento"]}
    ent = {e["id"]: e for e in spec["inputs"]}
    mapa_b = (RAIZ / ent["MAPA"]["ruta"]).read_bytes()
    filas = [f for f in D.lee_mapa(mapa_b.decode("utf-8")) if f["instrumento"] in insts]
    fab = fabrica(filas, random.Random(seed), escenario)
    inputs = {"MAPA": {"bytes": mapa_b}}
    for i in ent:
        if i.startswith("SRC-"):
            inputs[i] = {"bytes": json.dumps({"resultados": fab.get(i[4:], {})}).encode()}
    if "TAU2-SELLADO" in ent:
        ejes = {f["eje"] for f in filas}
        if par["instrumento"] == "ENIF":
            r = {f"RESULT-ENIFPIC-G-D9-{e}-TAU2-LOGIT": .05 for e in ejes}
        else:
            r = {f"RESULT-ENCIGPIC-DIGITAL-{e}-TAU2-FINAL": .05 for e in ejes}
        inputs["TAU2-SELLADO"] = {"bytes": json.dumps({"resultados": r}).encode()}
    valores = S.medir(inputs, C0.contrato_ejecutable(spec))
    fallas = C0._fallas_run(spec, valores, 0, None)
    return valores, fallas


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    esc = sys.argv[2] if len(sys.argv) > 2 else "aleatorio"
    mal = 0
    for d in sorted((RAIZ / "data/corrida0").glob("CALC-*-SERIE-DICTAMEN-0001")):
        v, f = corre(d.name, seed, esc)
        n = {k.rsplit("-N-", 1)[1]: x for k, x in v.items() if "-N-" in k and k.rsplit("-N-", 1)[1] in D.VOCAB}
        print(d.name, "FALLAS" if f else "OK", len(v), n, f[:2])
        mal += bool(f)
    sys.exit(1 if mal else 0)
