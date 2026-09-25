#!/usr/bin/env python3
"""CALC-PEW-MIGRACION-MEX-0001 · pisos por segmento de percepciones y lazos migratorios, Pew GAS México.

ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/FAMILIA-PEW-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre los datos de Pew.

QUÉ ESTIMA. Proporciones ponderadas (`weight`) de adultos 18+ ENTREVISTADOS EN MÉXICO
(filtro por el código de país de cada ola, leído de la etiqueta de valor «Mexico»), total y
por UN eje a la vez (SEXO, EDAD); nunca cruces. Olas abiertas: 2013, 2015, 2017, 2018, 2023;
Spring 2025 RESERVADA (E.6): no es input. Diseño: PSU/estrato de México donde el archivo
los trae (2015, 2017, 2018); en 2013 y 2023 no hay PSU publicada y el bootstrap remuestrea
entrevistas (un solo estrato, cada entrevista su propia UPM) — IC sin efecto de diseño,
declarado. IC calibrado de persistencia por conducta sobre las olas en que se preguntó
(≥ 3), piso = última ola con la pregunta.
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-PEW-MIGRACION-MEX"
OLAS = ("2013", "2015", "2017", "2018", "2023")
INPUTS_REPO = frozenset({"receta_pisos_salud", "lectores_familia"})
PAYLOADS = {o: f"pew_gas_spring{o}" for o in OLAS}
_RESERVADA = "pew_gas_spring2025"

# Por ola: variable de país y código de México; sexo; edad; peso; PSU/estrato (None si no hay).
OLA_CFG = {
    "2013": dict(pais=("country", 25), sexo="q164", edad="q165", w="weight", psu=None, est=None),
    "2015": dict(pais=("country", 21), sexo="q145", edad="q146", w="weight", psu="psu", est="stratum_mex"),
    "2017": dict(pais=("country", 20), sexo="sex", edad="age", w="weight", psu="psu_mex", est="stratum_mex"),
    "2018": dict(pais=("country", 15), sexo="sex", edad="age", w="weight", psu="psu_mex", est="stratum_mex"),
    "2023": dict(pais=("country", 24), sexo="sex", edad="age", w="weight", psu=None, est=None),
}
# conducta -> {ola: (variable, códigos 1, códigos 0)}; fuera = cualquier otro código.
CONDUCTAS = {
    "IRIA-A-VIVIR-A-EEUU": {
        "2013": ("q151", (1,), (2,)), "2015": ("q127", (1,), (2,)),
        "2017": ("mex_live_us", (1,), (2,)), "2018": ("mex_live_us", (1,), (2,))},
    "IRIA-SIN-AUTORIZACION-ENTRE-QUIENES-IRIAN": {
        "2013": ("q152", (1,), (2,)), "2015": ("q128", (1,), (2,)), "2017": ("mex_wo_auth", (1,), (2,))},
    "EN-EEUU-SE-VIVE-MEJOR": {
        "2013": ("q54", (1,), (2, 3)), "2015": ("q101", (1,), (2, 3)), "2023": ("us_better_life", (1,), (2, 3))},
    "CONTACTO-REGULAR-CON-PARIENTES-O-AMIGOS-EN-EL-EXTRANJERO": {
        "2013": ("q167", (1,), (2,)), "2015": ("q147", (1,), (2,)), "2017": ("friends_abroad", (1,), (2,))},
    "RECIBE-DINERO-DE-PARIENTES-EN-EL-EXTRANJERO": {
        "2013": ("q169", (1, 2), (3,)), "2017": ("receive_money", (1, 2), (3,)),
        "2018": ("receive_money", (1, 2), (3,))},
    "BUENO-PARA-MEXICO-QUE-VIVAN-EN-EEUU": {
        "2013": ("q153", (1,), (2,)), "2018": ("good_live_us", (1,), (2,))},
}
# universo condicional: sólo quienes irían a EEUU (1 en IRIA-A-VIVIR-A-EEUU de la misma ola)
CONDICIONAL = {"IRIA-SIN-AUTORIZACION-ENTRE-QUIENES-IRIAN": "IRIA-A-VIVIR-A-EEUU"}
EJES = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": ("18-29", "30-44", "45-59", "60-MAS")}
EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97))
_DIAG = ("FILAS-MEXICO", "FILAS-DISENO-VALIDO")


class ParoDeGuardia(RuntimeError):
    pass


def olas_de(c):
    return tuple(o for o in OLAS if o in CONDUCTAS[c])


def piso_de(c):
    return olas_de(c)[-1]


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    if _RESERVADA in inputs or any("2025" in str(k) for k in inputs):
        raise ParoDeGuardia("Pew Spring 2025 llegó como input: PARO (a)")
    esperados = INPUTS_REPO | set(PAYLOADS.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in PAYLOADS.values():
        if not inputs[pid].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
    for r in INPUTS_REPO:
        if inputs[r].get("bytes") is None:
            raise ParoDeGuardia(f"{r} sin bytes: se exige origen repo")


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def _bin(v, si, no):
    out = np.full(len(v), np.nan)
    out[np.isin(v, si)] = 1.0
    out[np.isin(v, no)] = 0.0
    return out


def columnas(ola):
    c = OLA_CFG[ola]
    cols = [c["sexo"], c["edad"], c["w"]] + [x for x in (c["psu"], c["est"]) if x]
    cols += [CONDUCTAS[k][ola][0] for k in CONDUCTAS if ola in CONDUCTAS[k]]
    return list(dict.fromkeys(cols))


def mide_ola(ola, df, R, replicas, semilla):
    c = OLA_CFG[ola]
    n = R.num
    diag = {"FILAS-MEXICO": int(len(df))}
    w = n(df[c["w"]])
    ok = w.gt(0).to_numpy()
    f = df[ok].reset_index(drop=True)
    diag["FILAS-DISENO-VALIDO"] = int(ok.sum())
    f["_w"] = np.asarray(w[ok], dtype=float)
    if c["psu"]:
        f["_est"] = f[c["est"]].astype(str).str.strip()
        f["_upm"] = f[c["psu"]].astype(str).str.strip()
    else:
        f["_est"] = "UNICO"
        f["_upm"] = np.arange(len(f)).astype(str)
    edad = n(f[c["edad"]]).to_numpy()
    edad = np.where((edad >= 18) & (edad <= 97), edad, np.nan)
    y = {}
    for k in CONDUCTAS:
        if ola not in CONDUCTAS[k]:
            continue
        var, si, no = CONDUCTAS[k][ola]
        y[k] = np.where(np.isfinite(edad), _bin(n(f[var]).to_numpy(), si, no), np.nan)
    for k, base in CONDICIONAL.items():
        if k in y:
            var, si, _ = CONDUCTAS[base][ola]
            y[k] = np.where(np.isin(n(f[var]).to_numpy(), si), y[k], np.nan)
    sexo = np.full(len(f), None, dtype=object)
    sx = n(f[c["sexo"]]).to_numpy()
    sexo[sx == 1] = "HOMBRE"
    sexo[sx == 2] = "MUJER"
    ecat = np.full(len(f), None, dtype=object)
    for cat, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = cat
    ejes = {"SEXO": (sexo, EJES["SEXO"]), "EDAD": (ecat, EJES["EDAD"])}
    res = R.marginales(f, y, ejes, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla) if y else {}
    return res, diag


def calcula(por_ola, diags, R):
    out = {}
    for ola in OLAS:
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diags[ola][k])
    for c in CONDUCTAS:
        olas = olas_de(c)
        piso = piso_de(c)
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            serie = {}
            for ola in olas:
                serie[ola] = {}
                for cat in cats:
                    r = por_ola[ola].get((c, eje, cat)) or {}
                    pv = _fin(r.get("p"))
                    serie[ola][cat] = pv
                    out[rid(c, ola, eje, cat, "P")] = pv
                    out[rid(c, ola, eje, cat, "EE")] = _fin(r.get("ee"))
                    out[rid(c, ola, eje, cat, "IC-LO")] = _fin(r.get("lo"))
                    out[rid(c, ola, eje, cat, "IC-HI")] = _fin(r.get("hi"))
                    out[rid(c, ola, eje, cat, "N")] = int(r.get("n", 0))
            t2, nd = R.persistencia(serie, list(olas), cats)
            if len(olas) < 3:  # spec §4: IC calibrado sólo con ≥ 3 olas
                t2 = None
            out[f"{P}-{c}-{eje}-TAU2"] = _fin(t2)
            out[f"{P}-{c}-{eje}-N-DELTAS"] = int(nd)
            for cat in cats:
                lo, hi = R.ic_calibrado(out[rid(c, piso, eje, cat, "P")], out[rid(c, piso, eje, cat, "IC-LO")],
                                        out[rid(c, piso, eje, cat, "IC-HI")], t2)
                out[rid(c, piso, eje, cat, "ICC-LO")] = _fin(lo)
                out[rid(c, piso, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    L = _modulo_desde_bytes("lectores_familia", inputs["lectores_familia"]["bytes"])
    por_ola, diags = {}, {}
    for ola in OLAS:
        df = L.lee_sav_zip(inputs[PAYLOADS[ola]]["ruta_absoluta"], columnas(ola), filtro=OLA_CFG[ola]["pais"])
        por_ola[ola], diags[ola] = mide_ola(ola, df, R, replicas, semilla)
    out = calcula(por_ola, diags, R)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-INPUT-LECTORES-SHA256"] = str(inputs["lectores_familia"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "Pew GAS Spring 2025 -- RESERVADA (E.6), no es input"
    out[f"{P}-G-EVIDENCIA"] = "(a) -- entrevistas en Mexico a residentes de Mexico; no es diaspora"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = []
    for ola in OLAS:
        f += [_fila(f"{P}-G-{ola}-{k}", "entero", "filas") for k in _DIAG]
    for c in CONDUCTAS:
        piso = piso_de(c)
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            for ola in olas_de(c):
                for cat in cats:
                    f += [_fila(rid(c, ola, eje, cat, "P"), "proporcion", "proporción ponderada"),
                          _fila(rid(c, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                          _fila(rid(c, ola, eje, cat, "IC-LO"), "proporcion", "IC95, inferior"),
                          _fila(rid(c, ola, eje, cat, "IC-HI"), "proporcion", "IC95, superior"),
                          _fila(rid(c, ola, eje, cat, "N"), "entero", "entrevistas sin ponderar")]
            f += [_fila(f"{P}-{c}-{eje}-TAU2", "flotante", "varianza logit entre olas"),
                  _fila(f"{P}-{c}-{eje}-N-DELTAS", "entero", "deltas definidos")]
            for cat in cats:
                f += [_fila(rid(c, piso, eje, cat, "ICC-LO"), "proporcion", "IC calibrado persistencia, inferior"),
                      _fila(rid(c, piso, eje, cat, "ICC-HI"), "proporcion", "IC calibrado persistencia, superior")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-INPUT-LECTORES-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración"),
          _fila(f"{P}-G-EVIDENCIA", "texto", "declaración")]
    return f
