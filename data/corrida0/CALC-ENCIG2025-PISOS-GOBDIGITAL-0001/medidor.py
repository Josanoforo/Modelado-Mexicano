#!/usr/bin/env python3
"""CALC-ENCIG2025-PISOS-GOBDIGITAL-0001 · piso C2 re-medido desde microdato (P2).

ACTO GEN2-ENCIG-PISOS-GEN2-1 (24/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/ENCIG2025-PISOS-GOBDIGITAL-spec-v1_0.md, congelado en el
COMMIT-1 antes de ejecutar este archivo sobre ENCIG 2025.

QUÉ ESTIMA. El piso C2 del duelo ENCIG 2025 (spec del -0001 §3, sin cambiar la
definición): por celda c = (a, b) de `edad × sexo` y `escolaridad × sexo`,
C2(c) = expit(logit p25(a) + logit p25(b) − logit p25), con p25 los marginales
de UNA variable de ENCIG 2025 sobre su propio denominador y el total. Unidad =
TRÁMITE (pago ordinario de luz, N_TRA = 01). Lo único que cambia respecto del
C2 del -0001 es de dónde salen los números: aquí se miden del payload del
manifiesto con la receta ENCIG; allá se copiaban, a seis decimales, de
`milpa/tramite-ola5-propuesta-v0.yaml` y `milpa/tramite.yaml` (cadena legacy).

GUARDIA. Este archivo NUNCA agrupa por dos variables: toda máscara sale de
`_mascara1(frame, eje, valor)`, que admite cero o un eje; `auditoria()` lo
comprueba sobre los bytes de este archivo en cada corrida y PARA si no sale
limpia. El cruce de 2025 ya fue visto por el -0001 (E.6: se usa en
retrospectiva, rotulado); este CALC no lo necesita y no lo toca.

Lo heredado se ejecuta desde los bytes hasheados de su input: la receta ENCIG
(`tools/encig_cruces_historicos.py`: `_load_wave`, `_bootstrap`, `_summary`).
"""
from __future__ import annotations

import ast
import json
import math
import types
from pathlib import Path

import numpy as np
import pandas as pd

P = "RESULT-ENCIG2025-PISOS-GOBDIGITAL"

EJES = {
    "SEXO": ("1", "2"),
    "EDAD": ("18-29", "30-44", "45-59", "60-96"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
}
CRUCES = {"EDADXSEXO": ("EDAD", "SEXO"), "ESCOLARIDADXSEXO": ("ESCOLARIDAD", "SEXO")}
INPUTS_REPO = frozenset({"receta_cruce_encig", "marginales_2025_resultados",
                         "adjudicacion_0001_resultados"})
PA0001 = "RESULT-ENCIG-DUELO-2025-ADJ"
_DIAG = ("FILAS-EVENTOS", "JOIN-SIN-DEMOGRAFIA", "N-UNIVERSO", "N-DISENO-VALIDO", "P7-3-EXCLUIDAS")


class ParoDeGuardia(RuntimeError):
    pass


class ReservaRota(RuntimeError):
    pass


# ══════════════════════════════ utilidades ══════════════════════════════

def celdas(cruce):
    a, b = CRUCES[cruce]
    return [(ka, kb) for ka in EJES[a] for kb in EJES[b]]


def rotulo(ka, kb):
    return f"{ka}-X-{kb}"


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _abierto(p):
    return p is not None and math.isfinite(p) and 0.0 < p < 1.0


def _logit(p):
    return math.log(p / (1.0 - p))


def _expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def _pct(v, q):
    return float(np.percentile(v, q)) if len(v) else None


def _bytes(inputs, iid):
    ent = inputs.get(iid)
    if ent is None:
        raise ParoDeGuardia(f"falta el input `{iid}`")
    raw = ent.get("bytes")
    if raw is None:
        raise ParoDeGuardia(f"input `{iid}` sin bytes: se exige origen repo")
    return raw


def _resultados(raw):
    doc = json.loads(raw.decode("utf-8"))
    r = doc.get("resultados", doc) if isinstance(doc, dict) else doc
    if isinstance(r, list):
        r = {x["id"]: x["valor"] for x in r}
    return r


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _cat_publica(eje, v):
    return "60-MAS" if (eje == "EDAD" and v == "60-96") else v


def id_marginal(eje, v, q):
    """Id de un marginal de ESTE CALC."""
    if eje == "TOTAL":
        return f"{P}-M-TOTAL-TODOS-{q}"
    return f"{P}-M-{eje}-{_cat_publica(eje, v)}-{q}"


def id_c2(cruce, ka, kb, q):
    """Id de una celda C2 de ESTE CALC (lo cita el -0002 por id)."""
    return f"{P}-{cruce}-{rotulo(ka, kb)}-{q}"


def id_marginal_arbitro(eje, v, q):
    if eje == "TOTAL":
        return f"RESULT-ARBITRO-ENCIG2025-DIGITAL-TOTAL-TODOS-{q}"
    return f"RESULT-ARBITRO-ENCIG2025-DIGITAL-{eje}-{_cat_publica(eje, v)}-{q}"


def id_0001(cruce, ka, kb, q):
    return f"{PA0001}-{cruce}-{rotulo(ka, kb)}-{q}"


# ══════════════════════════════ auditoría del código ══════════════════════════════

def _llamadas(nodo):
    fuera = set()
    for n in ast.walk(nodo):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                fuera.add(f.id)
            elif isinstance(f, ast.Attribute):
                fuera.add(f.attr)
    return fuera


def auditoria(fuente):
    """Lista de problemas del código (vacía = limpio). Spec §4."""
    arbol = ast.parse(fuente.decode("utf-8") if isinstance(fuente, bytes) else fuente)
    funciones = {n.name: n for n in arbol.body if isinstance(n, ast.FunctionDef)}
    grafo = {nombre: _llamadas(nodo) for nombre, nodo in funciones.items()}
    problemas = []
    # (1) `.eq(` sólo vive en `_mascara1`, y `_mascara1` recibe exactamente un eje
    for nombre in grafo:
        if nombre != "_mascara1" and "eq" in grafo[nombre]:
            problemas.append(f"`{nombre}` construye mascaras fuera de _mascara1")
    m = funciones.get("_mascara1")
    if m is None:
        problemas.append("falta _mascara1")
    else:
        args = [a.arg for a in m.args.args]
        if args != ["frame", "eje", "valor"] or m.args.vararg or m.args.kwarg:
            problemas.append(f"_mascara1 admite otra firma: {args}")
        nombres_m = {n.id for n in ast.walk(m) if isinstance(n, ast.Name)}
        if "ReservaRota" not in nombres_m or "EJES" not in nombres_m:
            problemas.append("_mascara1 no aplica la guardia de un eje")
    # (2) `_bootstrap` sólo desde `_marginales`, y `_marginales` sólo usa `_mascara1`
    llaman = sorted(n for n, g in grafo.items() if "_bootstrap" in g)
    if llaman != ["_marginales"]:
        problemas.append(f"_bootstrap llamado desde {llaman}")
    if "_marginales" in grafo and "_mascara1" not in grafo["_marginales"]:
        problemas.append("_marginales no usa _mascara1")
    # (3) la guardia de inputs se llama al entrar
    if "medir" not in grafo or "_guardia_inputs" not in grafo["medir"]:
        problemas.append("medir no llama _guardia_inputs")
    return problemas


# ══════════════════════════════ guardias ══════════════════════════════

def _guardia_inputs(inputs, contrato):
    payload = str(contrato["parametros"]["payload_id"])
    esperados = INPUTS_REPO | {payload}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for iid in INPUTS_REPO:
        _bytes(inputs, iid)
    if not inputs[payload].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{payload}` sin ruta resuelta")
    return payload


def _mascara1(frame, eje, valor):
    """Única constructora de máscaras: cero ejes (total) o UNO. Nunca dos."""
    if eje is None:
        return pd.Series(True, index=frame.index)
    if not isinstance(eje, str) or eje not in EJES:
        raise ReservaRota(f"agrupacion no autorizada: {eje!r}")
    return frame[eje].eq(valor)


# ══════════════════════════════ medición ══════════════════════════════

def _marginales(receta, frame, repeticiones, semilla):
    """11 marginales de un eje sobre su propio denominador + total; UN bootstrap
    (misma receta y semilla que el árbitro -0001: la receta sortea sobre las UPM
    del marco entero, así que las réplicas no dependen de qué máscaras se piden)."""
    masks, idx = [], {}
    for eje, valores in EJES.items():
        for v in valores:
            idx[(eje, v)] = len(masks)
            masks.append(_mascara1(frame, eje, v))
    idx[("TOTAL", "TODOS")] = len(masks)
    masks.append(_mascara1(frame, None, None))
    points, boot, _den = receta._bootstrap(frame, masks, repeticiones, semilla)
    n = [int(m.sum()) for m in masks]
    return {"idx": idx, "points": points, "boot": boot, "n": n}


def _compone(ra, rb, rn):
    with np.errstate(all="ignore"):
        z = np.log(ra / (1 - ra)) + np.log(rb / (1 - rb)) - np.log(rn / (1 - rn))
        return 1.0 / (1.0 + np.exp(-z))


def calcula(res, resumen, marg_arb, adj0001, par, diag):
    tol_m, tol_0001 = float(par["tol_marginales"]), float(par["tol_0001"])
    tol_sellado = float(par["tol_c2_sellado"])
    pts, boot, n, idx = res["points"], res["boot"], res["n"], res["idx"]
    out = {f"{P}-G-{k}": int(v) for k, v in diag.items()}

    # marginales, con control contra CALC-ARBITRO-MARGINALES-ENCIG2025-0001
    peor, n_disc = 0.0, 0
    for (eje, v), i in idx.items():
        p = _fin(pts[i])
        ee, lo, hi, validas = resumen(p, boot[:, i])
        out[id_marginal(eje, v, "P")], out[id_marginal(eje, v, "N")] = p, int(n[i])
        out[id_marginal(eje, v, "IC-LO")], out[id_marginal(eje, v, "IC-HI")] = lo, hi
        out[id_marginal(eje, v, "EE")], out[id_marginal(eje, v, "B-VALIDAS")] = ee, int(validas)
        s_p = _fin(marg_arb.get(id_marginal_arbitro(eje, v, "P")))
        s_n = marg_arb.get(id_marginal_arbitro(eje, v, "N"))
        peor = math.inf if (p is None or s_p is None) else max(peor, abs(p - s_p))
        n_disc += s_n is None or int(s_n) != int(n[i])
    ctrl_m = "REPRODUCE" if (peor <= tol_m and n_disc == 0) else "NO-REPRODUCE"
    out[f"{P}-G-CTRL-MARGINALES-MAX-ABS-P"] = peor if math.isfinite(peor) else None
    out[f"{P}-G-CTRL-MARGINALES-N-DISCORDA"] = int(n_disc)
    out[f"{P}-G-CTRL-MARGINALES-VEREDICTO"] = ctrl_m

    # C2 por celda: punto, IC por réplica, y los dos cotejos contra el -0001
    peor_rec, peor_ic, peor_leg, n_ic = 0.0, 0.0, 0.0, 0
    for cruce, (A, B) in CRUCES.items():
        for ka, kb in celdas(cruce):
            xa, xb, xn = idx[(A, ka)], idx[(B, kb)], idx[("TOTAL", "TODOS")]
            p_a, p_b, p_n = _fin(pts[xa]), _fin(pts[xb]), _fin(pts[xn])
            c2 = (_expit(_logit(p_a) + _logit(p_b) - _logit(p_n))
                  if all(_abierto(x) for x in (p_a, p_b, p_n)) else None)
            rep = _compone(boot[:, xa], boot[:, xb], boot[:, xn])
            validas = int(np.isfinite(rep).sum())
            ok_ic = ctrl_m == "REPRODUCE" and c2 is not None and validas == len(rep)
            lo, hi = (_pct(rep, 2.5), _pct(rep, 97.5)) if ok_ic else (None, None)
            n_ic += ok_ic
            out[id_c2(cruce, ka, kb, "C2-P")] = c2
            out[id_c2(cruce, ka, kb, "C2-IC-LO")], out[id_c2(cruce, ka, kb, "C2-IC-HI")] = lo, hi
            out[id_c2(cruce, ka, kb, "C2-B-VALIDAS")] = validas
            rec = _fin(adj0001.get(id_0001(cruce, ka, kb, "C2-P-RECALCULADO")))
            leg = _fin(adj0001.get(id_0001(cruce, ka, kb, "C2-P")))
            i_lo = _fin(adj0001.get(id_0001(cruce, ka, kb, "C2-IC-LO")))
            i_hi = _fin(adj0001.get(id_0001(cruce, ka, kb, "C2-IC-HI")))
            peor_rec = math.inf if (c2 is None or rec is None) else max(peor_rec, abs(c2 - rec))
            if lo is None or i_lo is None or hi is None or i_hi is None:
                peor_ic = math.inf
            else:
                peor_ic = max(peor_ic, abs(lo - i_lo), abs(hi - i_hi))
            dif = (c2 - leg) if (c2 is not None and leg is not None) else None
            out[id_c2(cruce, ka, kb, "C2-P-MENOS-C2-0001")] = dif
            peor_leg = math.inf if dif is None else max(peor_leg, abs(dif))
    total = sum(len(celdas(c)) for c in CRUCES)
    out[f"{P}-G-C2-IC-ESTADO"] = (f"EMITIDO -- {n_ic}/{total} celdas con IC por replica" if ctrl_m == "REPRODUCE"
                                  else "NO-EMITIDO -- control de marginales NO-REPRODUCE")
    out[f"{P}-G-CTRL-0001-RECALCULADO-MAX-ABS"] = peor_rec if math.isfinite(peor_rec) else None
    out[f"{P}-G-CTRL-0001-IC-MAX-ABS"] = peor_ic if math.isfinite(peor_ic) else None
    out[f"{P}-G-CTRL-0001-VEREDICTO"] = ("REPRODUCE" if (peor_rec <= tol_0001 and peor_ic <= tol_0001)
                                         else "NO-REPRODUCE")
    out[f"{P}-G-C2-MENOS-C2-0001-MAX-ABS"] = peor_leg if math.isfinite(peor_leg) else None
    out[f"{P}-G-CTRL-C2-SELLADO-VEREDICTO"] = "REPRODUCE" if peor_leg <= tol_sellado else "NO-REPRODUCE"
    out[f"{P}-G-UNIDAD"] = "TRAMITE (pago ordinario de luz, N_TRA=01); no se promedia con cifras por persona"
    out[f"{P}-G-INCERTIDUMBRE"] = (
        "bootstrap UPM con reposicion dentro de estrato, singleton de certeza, PCG64, percentiles 2.5/97.5, "
        "contrato conservador de la receta; IC de C2 por composicion replica a replica de los marginales")
    out[f"{P}-G-MARCA"] = ("RETROSPECTIVA -- el piso se sella despues de que el -0001 derivo R (cruce visto, E.6); "
                           "formula fija sin seleccion de variante y sin leer R")
    out[f"{P}-G-ORIGEN"] = "NUEVO -- marginales medidos de encig25_base_datos_csv (manifiesto); ningun numero de milpa/"
    return out


def medir(inputs, contrato):
    problemas = auditoria(Path(__file__).read_bytes())
    if problemas:
        raise ParoDeGuardia(f"auditoria del codigo: {problemas}")
    payload = _guardia_inputs(inputs, contrato)
    par = contrato["parametros"]
    repeticiones = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    receta = _modulo_desde_bytes("receta_cruce_encig", _bytes(inputs, "receta_cruce_encig"))
    marg_arb = _resultados(_bytes(inputs, "marginales_2025_resultados"))
    adj0001 = _resultados(_bytes(inputs, "adjudicacion_0001_resultados"))

    def resumen(point, replicas):
        ee, lo, hi, validas = receta._summary(float("nan") if point is None else point, replicas)
        return _fin(ee), _fin(lo), _fin(hi), validas

    frame, diag = receta._load_wave(inputs, {"parametros": {"ola": str(par["ola"]), "payload_id": payload}})
    res = _marginales(receta, frame, repeticiones, semilla)
    out = calcula(res, resumen, marg_arb, adj0001, par, diag)
    out[f"{P}-G-AUDITORIA-CODIGO"] = "LIMPIA"
    out[f"{P}-G-INPUT-PAYLOAD-SHA256"] = str(inputs[payload].get("sha256"))
    for iid in sorted(INPUTS_REPO):
        out[f"{P}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256"] = str(inputs[iid].get("sha256"))
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = repeticiones
    out[f"{P}-G-SEED"] = semilla
    return out


# ══════════════════════════════ esquema ══════════════════════════════

def _fila(rid, tipo, unidad, deps=None, origen=None):
    f = {"id": rid, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    if deps is not None:
        f["dependencias_numericas"] = list(deps)
    if origen is not None:
        f["origen_numerico"] = origen
    return f


def esquema_resultados():
    dato = ["encig25_base_datos_csv"]
    f = [_fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    f += [_fila(f"{P}-G-{s}", t, u) for s, t, u in (
        ("CTRL-MARGINALES-MAX-ABS-P", "flotante", "diferencia de proporción"),
        ("CTRL-MARGINALES-N-DISCORDA", "entero", "marginales"),
        ("CTRL-MARGINALES-VEREDICTO", "texto", "categoría"),
        ("C2-IC-ESTADO", "texto", "categoría"),
        ("CTRL-0001-RECALCULADO-MAX-ABS", "flotante", "diferencia de proporción"),
        ("CTRL-0001-IC-MAX-ABS", "flotante", "diferencia de proporción"),
        ("CTRL-0001-VEREDICTO", "texto", "categoría"),

        ("UNIDAD", "texto", "unidad"), ("INCERTIDUMBRE", "texto", "descripción del método"),
        ("MARCA", "texto", "categoría"), ("ORIGEN", "texto", "categoría"),
        ("AUDITORIA-CODIGO", "texto", "categoría"), ("INPUT-PAYLOAD-SHA256", "texto", "hash sha256"),
        ("BOOTSTRAP-REPLICAS", "entero", "réplicas"), ("SEED", "entero", "semilla"))]
    # resta un número de cadena legacy (el C2 del -0001): se declara MIXTO, no NUEVO
    f.append(_fila(f"{P}-G-C2-MENOS-C2-0001-MAX-ABS", "flotante", "diferencia de proporción (descriptiva)",
                   origen="MIXTO"))
    f.append(_fila(f"{P}-G-CTRL-C2-SELLADO-VEREDICTO", "texto", "categoría", origen="MIXTO"))
    f += [_fila(f"{P}-G-INPUT-{iid.upper().replace('_', '-')}-SHA256", "texto", "hash sha256")
          for iid in sorted(INPUTS_REPO)]
    for eje, valores in list(EJES.items()) + [("TOTAL", ("TODOS",))]:
        for v in valores:
            f += [_fila(id_marginal(eje, v, "P"), "proporcion", "proporción de trámites [0,1]", dato),
                  _fila(id_marginal(eje, v, "N"), "entero", "trámites"),
                  _fila(id_marginal(eje, v, "IC-LO"), "proporcion", "límite inferior IC95", dato),
                  _fila(id_marginal(eje, v, "IC-HI"), "proporcion", "límite superior IC95", dato),
                  _fila(id_marginal(eje, v, "EE"), "flotante", "error estándar por réplica", dato),
                  _fila(id_marginal(eje, v, "B-VALIDAS"), "entero", "réplicas definidas")]
    for cruce in CRUCES:
        for ka, kb in celdas(cruce):
            f += [_fila(id_c2(cruce, ka, kb, "C2-P"), "proporcion",
                        "proporción de trámites [0,1] (piso C2, punto adoptable)", dato),
                  _fila(id_c2(cruce, ka, kb, "C2-IC-LO"), "proporcion", "límite inferior IC95 por réplica", dato),
                  _fila(id_c2(cruce, ka, kb, "C2-IC-HI"), "proporcion", "límite superior IC95 por réplica", dato),
                  _fila(id_c2(cruce, ka, kb, "C2-B-VALIDAS"), "entero", "réplicas definidas"),
                  _fila(id_c2(cruce, ka, kb, "C2-P-MENOS-C2-0001"), "flotante",
                        "C2 nuevo menos C2 del -0001 (descriptiva)", origen="MIXTO")]
    return f
