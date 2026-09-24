"""Entrada corrida0 de `CALC-<INST>-SERIE-DICTAMEN-0001` (DONDE-CAMBIO spec v1.0).

Interfaz `medir(inputs, contrato)`. Entradas del spec.yaml:
  MAPA            fragmento TSV del mapa (sólo ids), filtrado por `contrato`
  SRC-<CALC>      resultados.json sellado de cada CALC que el mapa cita
  TAU2-SELLADO    (sólo ENIF/ENCIG) resultados.json del CALC de IC calibrado
Parámetros (en `contrato["parametros"]`): `instrumento`, `prefijo`.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from tools.series import dictamen as D

TAU_ENIF = re.compile(r"^RESULT-ENIFPIC-G-(D9|INFORMAL-CUALQUIERA)-([A-Z]+)-TAU2-LOGIT$")
TAU_ENCIG = re.compile(r"^RESULT-ENCIGPIC-DIGITAL-([A-Z]+)-TAU2-FINAL$")


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _res(ent):
    return json.loads(_bytes(ent).decode("utf-8"))["resultados"]


def tau_sellado(instrumento, res):
    """spec §3.1-2: τ² por eje desde el CALC sellado."""
    por_eje = {}
    if instrumento == "ENIF":
        for k, v in res.items():
            m = TAU_ENIF.match(k)
            if m and isinstance(v, (int, float)):
                por_eje.setdefault(m.group(2), []).append(v)
        return {e: sum(v) / len(v) for e, v in por_eje.items()}
    if instrumento == "ENCIG":
        for k, v in res.items():
            m = TAU_ENCIG.match(k)
            if m and isinstance(v, (int, float)):
                por_eje[m.group(1)] = v
        return por_eje
    raise ValueError(instrumento)


def medir(inputs, contrato):
    par = contrato.get("parametros", contrato)
    inst, pref = par["instrumento"], par["prefijo"]
    filas = [f for f in D.lee_mapa(_bytes(inputs["MAPA"]).decode("utf-8"))
             if f["instrumento"] == inst]
    assert filas, f"mapa sin filas de {inst}"
    valores = {}
    for k, ent in inputs.items():
        if k.startswith("SRC-"):
            valores.update(_res(ent))
    faltan = {f[c] for f in filas for c in ("result_p", "result_lo", "result_hi")
              if f[c] and f[c] not in valores}
    assert not faltan, f"ids del mapa sin RESULT: {sorted(faltan)[:5]}"
    tau_s = tau_sellado(inst, _res(inputs["TAU2-SELLADO"])) if inst in D.TAU2_SELLADO else None
    out_s, tau, fuente = D.evalua(filas, valores, tau_s, inst)
    out = {}
    for eje, t in sorted(tau.items()):
        out[f"{pref}-TAU2-{eje}"] = t
    out[f"{pref}-TAU2-FUENTE"] = fuente
    cuenta = Counter()
    for sid, r in out_s.items():
        b = f"{pref}-{sid}"
        out[b + "-K"] = r["k"]
        out[b + "-N-FUERA"] = r["n_fuera"]
        out[b + "-DICTAMEN"] = r["dictamen"]
        out[b + "-DIRECCION"] = r["direccion"] or "NINGUNA"
        out[b + "-OLAS"] = ",".join(r["olas"]) or "NINGUNA"
        out[b + "-DELTA-PP"] = r["delta_pp"]
        out[b + "-PARES-FUERA"] = ";".join(
            f'{p["a"]["ola"]}>{p["b"]["ola"]}:{p["estado"]}:{"SUBE" if p["delta"] > 0 else "BAJA"}'
            f':2020={p["marca_2020"]}' for p in r["fuera"]) or "NINGUNO"
        cuenta[r["dictamen"]] += 1
    for v in D.VOCAB:
        out[f"{pref}-N-{v}"] = cuenta[v]
    out[f"{pref}-N-SERIES"] = len(out_s)
    return out
