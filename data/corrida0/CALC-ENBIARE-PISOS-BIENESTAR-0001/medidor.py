#!/usr/bin/env python3
"""CALC-ENBIARE-PISOS-BIENESTAR-0001 · pisos por segmento ENBIARE 2021 con IC de diseño.

ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 (24/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/SALUD-ENBIARE-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENBIARE.

QUÉ ESTIMA. Una sola ola en corpus (2021; E.6: no hay historia que reservar, se abre y se
declara): proporciones y medias ponderadas (`FAC_ELE`) de la persona elegida de 18+,
total y por UN eje a la vez (SEXO, EDAD, ESCOLARIDAD, TLOC); nunca cruces. Diseño público
`EST_DIS`/`UPM_DIS` (llaves opacas). Sin IC de persistencia (una ola).

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (`receta_pisos_salud`).
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENBIARE-PISOS-BIENESTAR"
OLA = "2021"
PAY = "enbiare2021_bd_csv_zip"
INPUTS_REPO = frozenset({"receta_pisos_salud"})
LLAVE = ["folio", "viv_sel", "hogar", "n_ren"]

PD2 = [f"pd2_{i}" for i in range(1, 8)]
COLS_ELE = LLAVE + ["fac_ele", "est_dis", "upm_dis", "tloc", "pa1", "pa5", "pb1_01", "pb1_02", "pb1_04",
                    "pb1_11", "pb2_1", "pb2_2", "pd3_1", "pd3_2", "pg6", "pg7"] + PD2
COLS_SDEM = LLAVE + ["sexo", "edad", "nivel"]

ESCOL = {"HASTA-PRIMARIA": (0, 1, 2), "SECUNDARIA": (3, 4), "MEDIA-SUPERIOR": (5, 6, 7), "SUPERIOR": (8, 9, 10)}
EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
EJES = {
    "SEXO": ("HOMBRE", "MUJER"),
    "EDAD": tuple(c for c, _, _ in EDADES),
    "ESCOLARIDAD": tuple(ESCOL),
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
}
# conducta -> tipo ("proporcion" | "media")
CONDUCTAS = {
    "DEPRESION-CESD7": "proporcion",
    "ANSIEDAD-GAD2": "proporcion",
    "CUENTA-APOYO-FAMILIA": "proporcion",
    "CUENTA-APOYO-AMISTADES": "proporcion",
    "TIENE-RELIGION": "proporcion",
    "ASISTE-SERVICIO-RELIGIOSO": "proporcion",
    "SATISFACCION-VIDA": "media",
    "ESCALERA-CANTRIL": "media",
    "CONFIANZA-MAYORIA-GENTE": "media",
    "CONFIANZA-GENTE-CONOCIDA": "media",
    "CONFIANZA-POLICIA-MUNICIPAL": "media",
    "CONFIANZA-PARTIDOS": "media",
}
ESCALA = {"SATISFACCION-VIDA": "pa1", "ESCALERA-CANTRIL": "pa5", "CONFIANZA-MAYORIA-GENTE": "pb1_01",
          "CONFIANZA-GENTE-CONOCIDA": "pb1_02", "CONFIANZA-POLICIA-MUNICIPAL": "pb1_04",
          "CONFIANZA-PARTIDOS": "pb1_11"}
_DIAG = ("FILAS-ELEGIDOS", "JOIN-SIN-SOCIODEMOGRAFICO", "FILAS-DISENO-VALIDO")


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
    esperados = INPUTS_REPO | {PAY}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    if not inputs[PAY].get("ruta_absoluta"):
        raise ParoDeGuardia(f"payload `{PAY}` sin ruta resuelta")
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


def conducta_y(nombre, f, n, edad):
    if nombre in ESCALA:
        v = n(f[ESCALA[nombre]]).to_numpy()
        return np.where((v >= 0) & (v <= 10), v, np.nan)
    if nombre == "DEPRESION-CESD7":
        its = np.column_stack([n(f[c]).to_numpy() for c in PD2])
        ok = np.all(np.isin(its, (0, 1, 2, 3)), axis=1)
        pts = its.copy()
        pts[:, 5] = 3.0 - pts[:, 5]  # PD2_6 «disfrutó de la vida», invertido
        corte = np.where(edad >= 60, 5.0, 9.0)
        y = np.where(pts.sum(axis=1) >= corte, 1.0, 0.0)
        y[~ok] = np.nan
        return y
    if nombre == "ANSIEDAD-GAD2":
        its = np.column_stack([n(f[c]).to_numpy() for c in ("pd3_1", "pd3_2")])
        ok = np.all(np.isin(its, (0, 1, 2, 3)), axis=1)
        y = np.where(its.sum(axis=1) >= 3, 1.0, 0.0)
        y[~ok] = np.nan
        return y
    if nombre == "CUENTA-APOYO-FAMILIA":
        return _bin(n(f["pb2_1"]).to_numpy(), (1,), (2, 3))
    if nombre == "CUENTA-APOYO-AMISTADES":
        return _bin(n(f["pb2_2"]).to_numpy(), (1,), (2, 3))
    if nombre == "TIENE-RELIGION":
        return _bin(n(f["pg6"]).to_numpy(), (1,), (2,))
    if nombre == "ASISTE-SERVICIO-RELIGIOSO":
        y = _bin(n(f["pg7"]).to_numpy(), (1,), (2,))
        y[n(f["pg6"]).to_numpy() == 2] = 0.0  # sin religión: PG7 en blanco por secuencia
        return y
    raise KeyError(nombre)


def prepara(ele, sdem, R):
    n = R.num
    diag = {"FILAS-ELEGIDOS": int(len(ele))}
    k = lambda d: d[LLAVE].astype(str).apply(lambda s: s.str.strip()).agg("|".join, axis=1)  # noqa: E731
    ke, ks = k(ele), k(sdem)
    unicos = ~ks.duplicated(keep=False)
    s = sdem[unicos.to_numpy()].set_index(ks[unicos])
    diag["JOIN-SIN-SOCIODEMOGRAFICO"] = int((~ke.isin(s.index)).sum())
    f = ele.copy()
    for c in ("sexo", "edad", "nivel"):
        f[c] = ke.map(s[c]).to_numpy()
    w = n(f["fac_ele"])
    ok = (w.gt(0) & f["est_dis"].astype(str).str.strip().ne("")
          & f["upm_dis"].astype(str).str.strip().ne("")).to_numpy()
    diag["FILAS-DISENO-VALIDO"] = int(ok.sum())
    f = f[ok].reset_index(drop=True)
    edad = n(f["edad"]).to_numpy()
    ecat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ejes = {
        "SEXO": (_serie_map(n(f["sexo"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES["SEXO"]),
        "EDAD": (ecat, EJES["EDAD"]),
        "ESCOLARIDAD": (_serie_map(n(f["nivel"]).to_numpy(), ESCOL), EJES["ESCOLARIDAD"]),
        "TLOC": (_serie_map(n(f["tloc"]).to_numpy(), dict(zip(EJES["TLOC"], ((1,), (2,), (3,), (4,))))),
                 EJES["TLOC"]),
    }
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = f["est_dis"].astype(str).str.strip()
    f["_upm"] = f["upm_dis"].astype(str).str.strip()
    return f, ejes, diag, edad


def calcula(res, diag):
    out = {f"{P}-G-{k}": int(diag[k]) for k in _DIAG}
    for c in CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            for cat in cats:
                r = res.get((c, eje, cat)) or {}
                for q, key in (("P", "p"), ("EE", "ee"), ("IC-LO", "lo"), ("IC-HI", "hi")):
                    out[rid(c, eje, cat, q)] = _fin(r.get(key))
                out[rid(c, eje, cat, "N")] = int(r.get("n", 0))
    return out


def mide(ele, sdem, R, replicas, semilla):
    f, ejes, diag, edad = prepara(ele, sdem, R)
    cond = {c: conducta_y(c, f, R.num, edad) for c in CONDUCTAS}
    for c in cond:
        cond[c][~(edad >= 18)] = np.nan
    res = R.marginales(f, cond, ejes, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    return calcula(res, diag)


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    ruta = inputs[PAY]["ruta_absoluta"]
    ele = R.lee_csv_zip(ruta, COLS_ELE, miembro="TENBIARE.csv")
    sdem = R.lee_csv_zip(ruta, COLS_SDEM, miembro="TSDEM.csv")
    out = mide(ele, sdem, R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-OLA-UNICA"] = "ENBIARE 2021 -- unica ola en corpus; se abre (E.6), sin IC de persistencia"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = [_fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    for c, tipo in CONDUCTAS.items():
        t = "proporcion" if tipo == "proporcion" else "flotante"
        u = "proporción ponderada" if tipo == "proporcion" else "media ponderada escala 0-10"
        for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
            for cat in cats:
                f += [_fila(rid(c, eje, cat, "P"), t, u),
                      _fila(rid(c, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      _fila(rid(c, eje, cat, "IC-LO"), t, "IC95 diseño, inferior"),
                      _fila(rid(c, eje, cat, "IC-HI"), t, "IC95 diseño, superior"),
                      _fila(rid(c, eje, cat, "N"), "entero", "personas sin ponderar")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-UNICA", "texto", "declaración")]
    return f
