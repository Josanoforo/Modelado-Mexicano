#!/usr/bin/env python3
"""CALC-ENCODAT-PISOS-SUSTANCIAS-0001 · pisos por segmento ENCODAT 2016–2017 con IC de diseño.

ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 (24/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/SALUD-ENCODAT-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENCODAT.

QUÉ ESTIMA. Una sola ola abierta (2016–17; ENCODAT 2025 RESERVADA, E.6, no es input):
proporción ponderada (`ponde_ss`) total y por UN eje a la vez (SEXO, EDAD, ESTRATO,
ESCOLARIDAD) de la lista cerrada P1 de conductas de consumo. Diseño (`est_var`,
`code_upm`, `estrato`) desde el cuestionario de hogar por la llave declarada en la spec
§1: los 20 primeros caracteres de `id_pers` = `id_hogar`. Sin IC de persistencia: una
sola ola no tiene Δ (spec §3). Firewall genético: ningún eje es étnico ni hereditario.

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (`receta_pisos_salud`).
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENCODAT-PISOS-SUSTANCIAS"
OLA = "2016"
PAY_IND = "encodat_2016_2017__encodat_2016_2017_individual_stata_stata_zip"
PAY_HOG = "encodat_2016_2017__encodat_2016_2017_hogar_stata_stata_zip"
INPUTS_REPO = frozenset({"receta_pisos_salud"})
LARGO_HOGAR = 20

DI = ["di1a", "di1b", "di1c", "di1d", "di1e", "di1f", "di1g", "di1h", "di1i"]
DM = ["dm1a", "dm1b", "dm1c", "dm1d"]
COLS_IND = ["id_pers", "ponde_ss", "ds2", "ds3", "ds9", "al1", "al4", "al9", "al11",
            "tb02", "tb05", "tb50", "tp1"] + DI + DM
COLS_HOG = ["id_hogar", "estrato", "est_var", "code_upm"]

ESCOL = {"HASTA-PRIMARIA": (1, 2), "SECUNDARIA": (3, 4), "MEDIA-SUPERIOR": (5, 6), "SUPERIOR": (7, 8, 9)}
EDADES = (("12-17", 12, 17), ("18-34", 18, 34), ("35-65", 35, 65))
EJES = {
    "SEXO": ("HOMBRE", "MUJER"),
    "EDAD": tuple(c for c, _, _ in EDADES),
    "ESTRATO": ("RURAL", "URBANO", "METROPOLITANO"),
    "ESCOLARIDAD": tuple(ESCOL),
}
CONDUCTAS = ("ALCOHOL-12M", "ALCOHOL-30D", "ALCOHOL-EXCESIVO-12M", "FUMA-ACTUAL",
             "CIGARRO-ELECTRONICO-ALGUNA-VEZ", "DROGA-ILEGAL-ALGUNA-VEZ", "MARIGUANA-ALGUNA-VEZ",
             "DROGA-MEDICA-SIN-RECETA-ALGUNA-VEZ", "OPIACEOS-SIN-RECETA-ALGUNA-VEZ",
             "CONSULTO-PROFESIONAL-POR-CONSUMO")
Q = ("P", "EE", "IC-LO", "IC-HI", "N")
_DIAG = ("FILAS", "JOIN-SIN-HOGAR", "FILAS-DISENO-VALIDO", "FILAS-UNIVERSO-12-65")


class ParoDeGuardia(RuntimeError):
    pass


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
    esperados = INPUTS_REPO | {PAY_IND, PAY_HOG}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in (PAY_IND, PAY_HOG):
        if not inputs[pid].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
    if inputs["receta_pisos_salud"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def rid(conducta, eje, cat, q):
    return f"{P}-{conducta}-{OLA}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _bin(v, si, no):
    out = np.full(len(v), np.nan)
    out[np.isin(v, si)] = 1.0
    out[np.isin(v, no)] = 0.0
    return out


def _alguna(cols, f, n):
    m = np.column_stack([n(f[c]).to_numpy() for c in cols])
    y = np.full(len(f), np.nan)
    y[np.all(m == 2, axis=1)] = 0.0
    y[np.any(m == 1, axis=1)] = 1.0
    return y


def conducta_y(nombre, f, n):
    """0/1 por fila; NaN = sin dato. Saltos del cuestionario declarados en spec §2."""
    al1, al4 = n(f["al1"]).to_numpy(), n(f["al4"]).to_numpy()
    no_bebio_12m = (al1 == 2) | (al4 == 2)
    if nombre == "ALCOHOL-12M":
        y = _bin(al4, (1,), (2,))
        y[al1 == 2] = 0.0
        return y
    if nombre == "ALCOHOL-30D":
        y = _bin(n(f["al9"]).to_numpy(), (1,), (2,))
        y[no_bebio_12m] = 0.0
        return y
    if nombre == "ALCOHOL-EXCESIVO-12M":
        a11, sexo = n(f["al11"]).to_numpy(), n(f["ds2"]).to_numpy()
        h = _bin(a11, (1, 2, 3, 4), (5, 6))
        m = _bin(a11, (1, 2, 3, 4, 5), (6,))
        y = np.where(sexo == 1, h, np.where(sexo == 2, m, np.nan))
        y[no_bebio_12m] = 0.0
        return y
    if nombre == "FUMA-ACTUAL":
        y = _bin(n(f["tb02"]).to_numpy(), (1, 2), (3,))
        y[np.isnan(y) & (n(f["tb05"]).to_numpy() == 2)] = 0.0
        return y
    if nombre == "CIGARRO-ELECTRONICO-ALGUNA-VEZ":
        return _bin(n(f["tb50"]).to_numpy(), (1,), (2,))
    if nombre == "DROGA-ILEGAL-ALGUNA-VEZ":
        return _alguna(DI, f, n)
    if nombre == "MARIGUANA-ALGUNA-VEZ":
        return _bin(n(f["di1a"]).to_numpy(), (1,), (2,))
    if nombre == "DROGA-MEDICA-SIN-RECETA-ALGUNA-VEZ":
        return _alguna(DM, f, n)
    if nombre == "OPIACEOS-SIN-RECETA-ALGUNA-VEZ":
        return _bin(n(f["dm1a"]).to_numpy(), (1,), (2,))
    if nombre == "CONSULTO-PROFESIONAL-POR-CONSUMO":
        return _bin(n(f["tp1"]).to_numpy(), (1,), (2,))
    raise KeyError(nombre)


def prepara(ind, hog, R):
    n = R.num
    diag = {"FILAS": int(len(ind))}
    llave = ind["id_pers"].astype(str).str.strip().str[:LARGO_HOGAR]
    kh = hog["id_hogar"].astype(str).str.strip()
    unicos = ~kh.duplicated(keep=False)
    h = hog[unicos.to_numpy()].set_index(kh[unicos])
    diag["JOIN-SIN-HOGAR"] = int((~llave.isin(h.index)).sum())
    f = ind.copy()
    for c in ("estrato", "est_var", "code_upm"):
        f[c] = llave.map(h[c]).to_numpy()
    w = n(f["ponde_ss"])
    ok = (w.gt(0) & f["est_var"].notna() & f["code_upm"].notna()
          & f["code_upm"].astype(str).str.strip().ne("")).to_numpy()
    diag["FILAS-DISENO-VALIDO"] = int(ok.sum())
    f = f[ok].reset_index(drop=True)
    edad = n(f["ds3"]).to_numpy()
    uni = (edad >= 12) & (edad <= 65)
    diag["FILAS-UNIVERSO-12-65"] = int(uni.sum())
    ecat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ejes = {
        "SEXO": (_serie_map(n(f["ds2"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES["SEXO"]),
        "EDAD": (ecat, EJES["EDAD"]),
        "ESTRATO": (_serie_map(n(f["estrato"]).to_numpy(), {"RURAL": (1,), "URBANO": (2,), "METROPOLITANO": (3,)}),
                    EJES["ESTRATO"]),
        "ESCOLARIDAD": (_serie_map(np.where(edad >= 18, n(f["ds9"]).to_numpy(), np.nan), ESCOL), EJES["ESCOLARIDAD"]),
    }
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = f["est_var"].astype(str).str.strip()
    f["_upm"] = f["code_upm"].astype(str).str.strip()
    return f, ejes, diag, uni


def calcula(res, diag):
    out = {f"{P}-G-{k}": int(diag[k]) for k in _DIAG}
    for c in CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            for cat in cats:
                r = res.get((c, eje, cat)) or {}
                out[rid(c, eje, cat, "P")] = _fin(r.get("p"))
                out[rid(c, eje, cat, "EE")] = _fin(r.get("ee"))
                out[rid(c, eje, cat, "IC-LO")] = _fin(r.get("lo"))
                out[rid(c, eje, cat, "IC-HI")] = _fin(r.get("hi"))
                out[rid(c, eje, cat, "N")] = int(r.get("n", 0))
    return out


def mide(ind, hog, R, replicas, semilla):
    f, ejes, diag, uni = prepara(ind, hog, R)
    cond = {}
    for c in CONDUCTAS:
        y = conducta_y(c, f, R.num)
        y[~uni] = np.nan
        cond[c] = y
    res = R.marginales(f, cond, ejes, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    return calcula(res, diag)


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    ind = R.lee_dta(inputs[PAY_IND]["ruta_absoluta"], COLS_IND, encoding="UTF-8")
    hog = R.lee_dta(inputs[PAY_HOG]["ruta_absoluta"], COLS_HOG, encoding="UTF-8")
    out = mide(ind, hog, R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENCODAT 2025 -- RESERVADA (E.6), no es input; sin IC de persistencia (una ola)"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = [_fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    for c in CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            for cat in cats:
                f += [_fila(rid(c, eje, cat, "P"), "proporcion", "proporción ponderada"),
                      _fila(rid(c, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      _fila(rid(c, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                      _fila(rid(c, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                      _fila(rid(c, eje, cat, "N"), "entero", "personas sin ponderar")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
