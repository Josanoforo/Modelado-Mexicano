"""Medidor congelado de CALC-ENIF-0002: población y horizonte, ENIF 2024."""
from __future__ import annotations

import csv
import io
import json
import zipfile

import numpy as np

ZIP_ID = "enif_2024_enif_2024_bd_csv"
REUSO_ID = "IN-CALC-ENIF-0001-RESULTADOS"
M_MOD = "TMODULO.csv"
P = "RESULT-ENIF-POB-"
COLS = ["P3_8", "P3_9", "P3_10", "P3_13", "P4_10",
        "FAC_PER", "EST_DIS", "UPM_DIS"]
DOMINIO = {
    "P3_8": set("123456789"),
    "P3_9": set("1234567"),
    "P3_10": set("123456"),
    "P3_13": set("12345679"),
    "P4_10": set("1234589"),
}
P410_VALIDO = set("12345")
CORTO = {"1", "2"}
NOCORTO = {"3", "4", "5"}
CON_SS = set("1234")
SIN_SS = {"7"}
ACT_38 = {"1", "2"}
ACT_39 = set("123456")
NO_ACT_38 = {"8"}
NO_ACT_39 = {"7"}
REPLICAS = 1000
SEED = 20260910
GRANO = 6

REUSO_ESPERADO = {
    "RESULT-ENIF-AHO-A-P-CORTO-SIN-P": 0.541343,
    "RESULT-ENIF-AHO-A-P-NOCORTO-SIN-P": 0.458657,
    "RESULT-ENIF-AHO-A-P-CORTO-CON-P": 0.373130,
    "RESULT-ENIF-AHO-A-P-NOCORTO-CON-P": 0.626870,
}


def _norm(s):
    return str(s).lstrip("﻿").lstrip("ï»¿").strip().upper()


def _cod(s):
    return "" if s is None else str(s).strip()


def _peso(s):
    try:
        v = float(str(s).strip().replace(",", ""))
    except (TypeError, ValueError):
        return None
    return v if np.isfinite(v) and v > 0 else None


def _llave(s):
    v = _cod(s)
    return v or None


def _abre(zf):
    crudo = zf.read(M_MOD)
    try:
        texto, enc = crudo.decode("utf-8-sig"), "utf-8-sig"
    except UnicodeDecodeError:
        texto, enc = crudo.decode("latin-1"), "latin-1"
    lector = csv.reader(io.StringIO(texto, newline=""))
    try:
        cab = [_norm(c) for c in next(lector)]
    except StopIteration:
        return [], list(COLS), enc
    idx = {c: cab.index(c) for c in COLS if c in cab}
    faltan = [c for c in COLS if c not in idx]
    filas = []
    for row in lector:
        if row:
            filas.append({c: row[idx[c]] if c in idx and idx[c] < len(row)
                          else None for c in COLS})
    return filas, faltan, enc


def _trabaja(r):
    return _cod(r["P3_8"]) in ACT_38 or _cod(r["P3_9"]) in ACT_39


def _no_trabaja(r):
    return _cod(r["P3_8"]) in NO_ACT_38 or _cod(r["P3_9"]) in NO_ACT_39


def _celda(r):
    """Partición de filas con P4_10 válido; None activa la guardia de paro."""
    trabaja, no_trabaja = _trabaja(r), _no_trabaja(r)
    if trabaja == no_trabaja:
        return None
    if no_trabaja:
        return "NO-TRABAJA"
    p313 = _cod(r["P3_13"])
    if p313 in CON_SS:
        return "TRABAJA-CON-SS"
    if p313 in SIN_SS:
        return "TRABAJA-SIN-SS"
    return "TRABAJA-RESIDUAL"


def _punto(w, d):
    sw = sum(w)
    return (sum(wi for wi, di in zip(w, d) if di) / sw, sw)


def _ic(w, d, est, upm):
    n_sin = sum(e is None or u is None for e, u in zip(est, upm))
    grupos = {}
    for i, (e, u) in enumerate(zip(est, upm)):
        if e is not None and u is not None:
            grupos.setdefault(e, {}).setdefault(u, []).append(i)
    if not grupos:
        return None, None, 0, 0, 0, "NO-ESTIMABLE-DISENO-INCOMPLETO", n_sin
    rng = np.random.default_rng(SEED)
    reps = []
    for _ in range(REPLICAS):
        sw = swd = 0.0
        for unidades in grupos.values():
            ks = list(unidades)
            for j in rng.integers(0, len(ks), size=len(ks)):
                for i in unidades[ks[int(j)]]:
                    sw += w[i]
                    if d[i]:
                        swd += w[i]
        if sw > 0:
            reps.append(swd / sw)
    n_unica = sum(len(x) == 1 for x in grupos.values())
    metodo = ("IC-CON-ESTRATOS-DE-UPM-UNICA" if n_unica else
              "BOOTSTRAP-UPM-EN-ESTRATO")
    a = np.asarray(reps)
    return (float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5)),
            len(grupos), sum(len(x) for x in grupos.values()), n_unica,
            metodo, n_sin)


def medir(inputs, contrato):
    out = {}

    def put(suf, valor):
        out[P + suf] = valor

    with zipfile.ZipFile(inputs[ZIP_ID]["ruta_absoluta"]) as zf:
        filas, faltan, enc = _abre(zf)
    put("G-N-FILAS-TMODULO", len(filas))
    put("G-ENCODING-USADO", enc)
    put("G-COLUMNAS-AUSENTES", ";".join(faltan) if faltan else "NINGUNA")
    if faltan:
        raise ValueError("NO-ESTIMABLE-COLUMNAS-AUSENTES:" + ";".join(faltan))

    malos = []
    for c, validos in DOMINIO.items():
        cuenta = {}
        for r in filas:
            v = _cod(r[c])
            if v not in validos and v not in {"", "b"}:
                cuenta[v] = cuenta.get(v, 0) + 1
        if cuenta:
            malos.append(c + ":" + ",".join(f"{k}={v}" for k, v in sorted(cuenta.items())))
    put("G-DOMINIOS", ";".join(malos) if malos else "OK")

    con_peso = [(r, _peso(r["FAC_PER"])) for r in filas]
    validas = [(r, w) for r, w in con_peso
               if w is not None and _cod(r["P4_10"]) in P410_VALIDO]
    solape = sum(_trabaja(r) and _no_trabaja(r) for r, _ in validas)
    sin_clase = sum((not _trabaja(r)) and (not _no_trabaja(r)) for r, _ in validas)
    put("G-PARTICION-ACTIVIDAD-SOLAPE-N", solape)
    put("G-PARTICION-ACTIVIDAD-SIN-CLASE-N", sin_clase)
    if solape or sin_clase:
        put("G-PARTICION-ACTIVIDAD", "NO-ESTIMABLE-PARTICION-ACTIVIDAD")
        raise ValueError("NO-ESTIMABLE-PARTICION-ACTIVIDAD")
    put("G-PARTICION-ACTIVIDAD", "EXHAUSTIVA-Y-DISJUNTA")
    put("G-P410-PREGUNTA-A-TODOS", "SI" if all(_cod(r["P4_10"]) not in {"", "b"}
                                                  for r in filas) else "NO")

    with open(inputs[REUSO_ID]["ruta_absoluta"], encoding="utf-8") as fh:
        previos = json.load(fh)["resultados"]
    discordias = {k: previos.get(k) for k, v in REUSO_ESPERADO.items()
                  if previos.get(k) != v}
    put("G-REUSO-CALC-ENIF-0001", "COINCIDE" if not discordias else
        "DISCORDA:" + ",".join(sorted(discordias)))
    if discordias:
        raise ValueError("REUSO-CALC-ENIF-0001-DISCORDA")

    total = sum(w for _, w in con_peso if w is not None)
    put("M-PESO-TOTAL-18MAS", round(total, 3))
    categorias = ["TRABAJA-CON-SS", "TRABAJA-SIN-SS", "NO-TRABAJA",
                  "TRABAJA-RESIDUAL"]
    suma_pesos = 0.0
    for categoria in categorias:
        sub = [(r, w) for r, w in validas if _celda(r) == categoria]
        peso = sum(w for _, w in sub)
        suma_pesos += peso
        put(f"M-{categoria}-N", len(sub))
        put(f"M-{categoria}-PESO", round(peso, 3))
        put(f"M-{categoria}-FRACCION", round(peso / total, GRANO))
    faltante = [(r, w) for r, w in con_peso
                if w is not None and _cod(r["P4_10"]) not in P410_VALIDO]
    peso_faltante = sum(w for _, w in faltante)
    put("M-P410-FALTANTE-N", len(faltante))
    put("M-P410-FALTANTE-PESO", round(peso_faltante, 3))
    put("M-P410-FALTANTE-FRACCION", round(peso_faltante / total, GRANO))
    put("M-COBERTURA-P410-VALIDO", round(suma_pesos / total, GRANO))
    put("G-PARTICION-PESO-DELTA", round(total - suma_pesos - peso_faltante, 3))

    def emite(nombre, seleccion):
        sub = [(r, w) for r, w in validas if seleccion(r)]
        put(f"P-{nombre}-N-DENOMINADOR", len(sub))
        if not sub:
            put(f"P-{nombre}-P", "NO-ESTIMABLE-UNIVERSO-VACIO")
            for suf in ("IC-LO", "IC-HI"):
                put(f"P-{nombre}-{suf}", None)
            put(f"P-{nombre}-METODO-IC", "NO-ESTIMABLE-UNIVERSO-VACIO")
            return
        w = [x[1] for x in sub]
        d = [_cod(x[0]["P4_10"]) in CORTO for x in sub]
        est = [_llave(x[0]["EST_DIS"]) for x in sub]
        upm = [_llave(x[0]["UPM_DIS"]) for x in sub]
        p, sw = _punto(w, d)
        lo, hi, ne, nu, n1, metodo, nsd = _ic(w, d, est, upm)
        put(f"P-{nombre}-P", round(p, GRANO))
        put(f"P-{nombre}-IC-LO", None if lo is None else round(lo, GRANO))
        put(f"P-{nombre}-IC-HI", None if hi is None else round(hi, GRANO))
        put(f"P-{nombre}-METODO-IC", metodo)
        put(f"P-{nombre}-PESO-DENOMINADOR", round(sw, 3))
        put(f"P-{nombre}-N-ESTRATOS", ne)
        put(f"P-{nombre}-N-UPM", nu)
        put(f"P-{nombre}-N-ESTRATOS-UPM-UNICA", n1)
        put(f"P-{nombre}-N-SIN-DISENO", nsd)

    emite("CORTO-NO-TRABAJA", lambda r: _celda(r) == "NO-TRABAJA")
    emite("CORTO-TRABAJA-RESIDUAL", lambda r: _celda(r) == "TRABAJA-RESIDUAL")
    emite("CORTO-POBLACION-18MAS", lambda r: True)
    put("G-NOTA-P410-1", "MENOS-DE-UNA-SEMANA/O-NO-TIENE-AHORROS;NO-DESAGREGABLE")
    put("G-NOTA-TOTAL", "RAZON-DIRECTA-CON-IC-DE-LAS-MISMAS-REPLICAS;NO-PROMEDIO-DE-TASAS")
    return out
