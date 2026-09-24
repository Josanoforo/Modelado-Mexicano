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
from urllib.parse import unquote

from tools.series import dictamen as D

TAU_ENIF = re.compile(r"^RESULT-ENIFPIC-G-(D9|INFORMAL-CUALQUIERA)-([A-Z]+)-TAU2-LOGIT$")
TAU_ENCIG = re.compile(r"^RESULT-ENCIGPIC-DIGITAL-([A-Z]+)-TAU2-FINAL$")


def _bytes(ent):
    b = ent.get("bytes")
    return b if b is not None else Path(ent["ruta_absoluta"]).read_bytes()


def _res(ent):
    return json.loads(_bytes(ent).decode("utf-8"))["resultados"]


def _celdas(tabla):
    """RESULT-*-TABLA sellado: string-JSON o lista/dict con lista `celdas`."""
    if isinstance(tabla, str):
        tabla = json.loads(tabla)
    if isinstance(tabla, dict):
        tabla = tabla["celdas"]
    return tabla


def resuelve_celdas(ids, valores):
    """Direcciones `<RESULT-ID>#k1=v1&.../<campo>` (mapa/ESQUEMA, CELDA-DE-TABLA):
    v percent-encoded; campo `nombre` o `nombre[i]`. `valores` son los RESULT
    del CALC de la fila (un mismo RESULT-ID puede existir en dos CALC).
    Devuelve {direccion: valor}; una dirección que no resuelve a exactamente
    una celda es error."""
    indices, out = {}, {}
    for d in sorted(i for i in ids if "#" in i):
        base, resto = d.split("#", 1)
        bloque, campo = resto.rsplit("/", 1)
        pares_kv = [p.split("=", 1) for p in bloque.split("&")]
        nombres = tuple(k for k, _ in pares_kv)
        clave = (base, nombres)
        if clave not in indices:
            idx = {}
            for c in _celdas(valores[base]):
                idx.setdefault(tuple(str(c.get(k)) for k in nombres), []).append(c)
            indices[clave] = idx
        hits = indices[clave].get(tuple(unquote(v) for _, v in pares_kv), [])
        assert len(hits) == 1, f"{d}: {len(hits)} celdas"
        m = re.fullmatch(r"(\w+)(?:\[(\d)\])?", campo)
        v = hits[0][m.group(1)]
        out[d] = v[int(m.group(2))] if m.group(2) is not None else v
    return out


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
    por_calc = {k[4:]: _res(ent) for k, ent in inputs.items() if k.startswith("SRC-")}
    valores = {}
    for res in por_calc.values():
        valores.update({k: v for k, v in res.items() if not k.endswith("-TABLA")})
    for calc, res in por_calc.items():
        ids_c = {f[c] for f in filas if f["calc"] == calc
                 for c in ("result_p", "result_lo", "result_hi") if f[c]}
        # la dirección de celda se prefija con su CALC para no colisionar
        for d, v in resuelve_celdas(ids_c, res).items():
            valores[f"{calc}::{d}"] = v
    for f in filas:
        for c in ("result_p", "result_lo", "result_hi"):
            if "#" in f[c]:
                f[c] = f"{f['calc']}::{f[c]}"
    ids = {f[c] for f in filas for c in ("result_p", "result_lo", "result_hi") if f[c]}
    faltan = {i for i in ids if i not in valores}
    assert not faltan, f"ids del mapa sin RESULT: {sorted(faltan)[:5]}"
    tau_s = tau_sellado(inst, _res(inputs["TAU2-SELLADO"])) if inst in D.TAU2_SELLADO else None
    out_s, tau, fuente = D.evalua(filas, valores, tau_s, inst)
    out = {}
    for eje in sorted({f["eje"] for f in filas}):
        out[f"{pref}-TAU2-{eje}"] = D.tau2_para(eje, tau)
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
