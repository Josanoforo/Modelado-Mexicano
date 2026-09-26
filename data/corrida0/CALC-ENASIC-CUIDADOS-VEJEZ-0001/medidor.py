#!/usr/bin/env python3
"""CALC-ENASIC-CUIDADOS-VEJEZ-0001 · pisos por segmento ENASIC 2022 con IC de diseño.

ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/FAMILIA-ENASIC-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENASIC.

QUÉ ESTIMA. Una sola ola en corpus (2022; E.6: no hay historia que reservar, se abre y se
declara): proporciones ponderadas (`FAC_HOG`) de hogares (THOGAR) y de personas de 60+
residentes (TCSDEMPO, con diseño y factor del hogar por `LLAVEHOG`), total y por UN eje a
la vez; nunca cruces. Diseño `EST_DIS`/`UPM_DIS` (llaves opacas). Sin IC de persistencia.
«Quién cuida a quién»: el sexo del cuidador principal (P4_44, número de renglón) se toma
del renglón del mismo hogar (`LLAVESDE` = `LLAVEHOG` + renglón de 2 dígitos).
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENASIC-CUIDADOS-VEJEZ"
OLA = "2022"
PAY = "enasic2022_bd_csv_zip"
INPUTS_REPO = frozenset({"receta_pisos_salud", "lectores_familia"})

COLS_HOG = ["llavehog", "fac_hog", "est_dis", "upm_dis", "hn_c", "hn_c60ma", "sexo_jefe", "edad_jefe"]
COLS_PER = ["llavesde", "llavehog", "paren", "sexo", "edad", "niv", "p4_42", "p4_44", "p4_44a", "p4_45"]

ESCOL = {"HASTA-PRIMARIA": (0, 1, 2), "SECUNDARIA": (3, 5), "MEDIA-SUPERIOR": (4, 6, 7),
         "SUPERIOR": (8, 9, 10, 11)}
EJES_HOG = {
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": ("18-29", "30-44", "45-59", "60-MAS"),
    "TAMANO-HOGAR": ("1", "2", "3-4", "5-MAS"),
}
EJES_PER = {
    "SEXO": ("HOMBRE", "MUJER"),
    "EDAD": ("60-69", "70-79", "80-MAS"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
    "TAMANO-HOGAR": ("1", "2", "3-4", "5-MAS"),
    "CONDICION-PAREJA": ("CON-PAREJA-EN-HOGAR", "SIN-PAREJA-EN-HOGAR"),
}
EDAD_JEFE = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97))
EDAD_AM = (("60-69", 60, 69), ("70-79", 70, 79), ("80-MAS", 80, 97))
TAM = (("1", 1, 1), ("2", 2, 2), ("3-4", 3, 4), ("5-MAS", 5, 99))

CONDUCTAS = {
    "HOGAR-NECESITA-CUIDADOS": "HOGAR",
    "HOGAR-CON-60MAS-QUE-NECESITA-CUIDADOS": "HOGAR",
    "AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR": "PERSONA",
    "AM60-CUIDADOR-PRINCIPAL-MUJER": "PERSONA",
    "AM60-CUIDADOR-PRINCIPAL-HIJA": "PERSONA",
    "AM60-CUIDADOR-PRINCIPAL-CONYUGE": "PERSONA",
    "AM60-CUIDADO-POR-PERSONA-DE-OTRO-HOGAR": "PERSONA",
}
_DIAG = ("FILAS-HOGAR", "FILAS-HOGAR-DISENO-VALIDO", "FILAS-PERSONA", "PERSONA-SIN-HOGAR",
         "FILAS-60MAS", "CUIDADOR-RENGLON-SIN-PAREO")


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
    for r in INPUTS_REPO:
        if inputs[r].get("bytes") is None:
            raise ParoDeGuardia(f"{r} sin bytes: se exige origen repo")


def ejes_de(unidad):
    return EJES_HOG if unidad == "HOGAR" else EJES_PER


def rid(conducta, eje, cat, q):
    return f"{P}-{conducta}-{OLA}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _rango(v, tramos):
    out = np.full(len(v), None, dtype=object)
    for c, lo, hi in tramos:
        out[(v >= lo) & (v <= hi)] = c
    return out


def _bin(v, si, no):
    out = np.full(len(v), np.nan)
    out[np.isin(v, si)] = 1.0
    out[np.isin(v, no)] = 0.0
    return out


def prepara(hog, per, R):
    n = R.num
    diag = {"FILAS-HOGAR": int(len(hog)), "FILAS-PERSONA": int(len(per))}
    w = n(hog["fac_hog"])
    est = hog["est_dis"].astype(str).str.strip()
    upm = hog["upm_dis"].astype(str).str.strip()
    ok = (w.gt(0) & est.ne("") & upm.ne("")).to_numpy()
    diag["FILAS-HOGAR-DISENO-VALIDO"] = int(ok.sum())
    fh = hog[ok].reset_index(drop=True)
    fh["_key"] = fh["llavehog"].astype(str).str.strip()
    fh["_w"] = np.asarray(w[ok], dtype=float)
    fh["_est"] = est[ok].to_numpy()
    fh["_upm"] = upm[ok].to_numpy()
    # integrantes por hogar = renglones de TCSDEMPO; pareja corresidente = hay PAREN 2 en el hogar
    kp = per["llavehog"].astype(str).str.strip()
    paren = n(per["paren"]).to_numpy()
    tam = kp.value_counts()
    con_conyuge = set(kp[paren == 2])
    fh["_tam"] = fh["_key"].map(tam).fillna(0).to_numpy(dtype=float)
    hidx = fh.drop_duplicates("_key", keep=False).set_index("_key")
    enl = kp.isin(hidx.index).to_numpy()
    diag["PERSONA-SIN-HOGAR"] = int((~enl).sum())
    fp = per[enl].reset_index(drop=True)
    k = kp[enl].to_numpy()
    for c in ("_w", "_est", "_upm", "_tam"):
        fp[c] = hidx.loc[k, c].to_numpy()
    fp["_key"] = k
    pr = n(fp["paren"]).to_numpy()
    fp["_pareja"] = np.where((pr == 2) | ((pr == 1) & np.isin(k, list(con_conyuge))),
                             "CON-PAREJA-EN-HOGAR", np.where(np.isin(pr, (3, 4, 5, 6, 7, 8, 9)) | (pr == 1),
                                                              "SIN-PAREJA-EN-HOGAR", None))
    # sexo por renglón del hogar
    sexo_idx = dict(zip(per["llavesde"].astype(str).str.strip(), n(per["sexo"]).to_numpy()))
    return fh, fp, diag, sexo_idx


def conductas_hogar(fh, R):
    n = R.num
    y = {"HOGAR-NECESITA-CUIDADOS": _bin(n(fh["hn_c"]).to_numpy(), (1,), (2,)),
         "HOGAR-CON-60MAS-QUE-NECESITA-CUIDADOS": _bin(n(fh["hn_c60ma"]).to_numpy(), (1,), (2,))}
    ej = n(fh["edad_jefe"]).to_numpy()
    ejes = {"SEXO-JEFE": (_serie_map(n(fh["sexo_jefe"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}),
                          EJES_HOG["SEXO-JEFE"]),
            "EDAD-JEFE": (_rango(np.where(ej <= 97, ej, -1), EDAD_JEFE), EJES_HOG["EDAD-JEFE"]),
            "TAMANO-HOGAR": (_rango(fh["_tam"].to_numpy(dtype=float), TAM), EJES_HOG["TAMANO-HOGAR"])}
    return y, ejes


def conductas_persona(fp, sexo_idx, R, diag):
    n = R.num
    edad = n(fp["edad"]).to_numpy()
    am = (edad >= 60) & (edad <= 97)
    diag["FILAS-60MAS"] = int(am.sum())
    p442 = n(fp["p4_42"]).to_numpy()
    p444 = n(fp["p4_44"]).to_numpy()
    p444a = n(fp["p4_44a"]).to_numpy()
    p445 = n(fp["p4_45"]).to_numpy()
    y = {}
    y["AM60-CUIDADO-POR-ALGUIEN-DEL-HOGAR"] = np.where(am, _bin(p442, (1,), (2,)), np.nan)
    # cuidador principal en el hogar: P4_44 ∈ 01-07 (renglón); 00 y 99 fuera
    tiene = am & (p444 >= 1) & (p444 <= 7)
    claves = [f"{k}{int(r):02d}" if t else "" for k, r, t in
              zip(fp["_key"].to_numpy(), np.nan_to_num(p444, nan=0), tiene)]
    sx = np.array([sexo_idx.get(c, np.nan) if c else np.nan for c in claves], dtype=float)
    diag["CUIDADOR-RENGLON-SIN-PAREO"] = int((tiene & ~np.isfinite(sx)).sum())
    y["AM60-CUIDADOR-PRINCIPAL-MUJER"] = np.where(tiene, _bin(sx, (2,), (1,)), np.nan)
    rel_ok = tiene & (p444a >= 1) & (p444a <= 11)
    y["AM60-CUIDADOR-PRINCIPAL-HIJA"] = np.where(rel_ok, (p444a == 4).astype(float), np.nan)
    y["AM60-CUIDADOR-PRINCIPAL-CONYUGE"] = np.where(rel_ok, (p444a == 1).astype(float), np.nan)
    y["AM60-CUIDADO-POR-PERSONA-DE-OTRO-HOGAR"] = np.where(am, _bin(p445, (1,), (2,)), np.nan)
    ejes = {
        "SEXO": (_serie_map(n(fp["sexo"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES_PER["SEXO"]),
        "EDAD": (_rango(np.where(am, edad, -1), EDAD_AM), EJES_PER["EDAD"]),
        "ESCOLARIDAD": (_serie_map(n(fp["niv"]).to_numpy(), ESCOL), EJES_PER["ESCOLARIDAD"]),
        "TAMANO-HOGAR": (_rango(fp["_tam"].to_numpy(dtype=float), TAM), EJES_PER["TAMANO-HOGAR"]),
        "CONDICION-PAREJA": (fp["_pareja"].to_numpy(), EJES_PER["CONDICION-PAREJA"]),
    }
    return y, ejes


def mide(hog, per, R, replicas, semilla):
    fh, fp, diag, sexo_idx = prepara(hog, per, R)
    yh, eh = conductas_hogar(fh, R)
    res = R.marginales(fh, yh, eh, fh["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    yp, ep = conductas_persona(fp, sexo_idx, R, diag)
    res.update(R.marginales(fp, yp, ep, fp["_w"].to_numpy(dtype=float), "_est", "_upm", replicas, semilla))
    return calcula(res, diag)


def calcula(res, diag):
    out = {f"{P}-G-{k}": int(diag[k]) for k in _DIAG}
    for c, unidad in CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_de(unidad).items()):
            for cat in cats:
                r = res.get((c, eje, cat)) or {}
                for q, key in (("P", "p"), ("EE", "ee"), ("IC-LO", "lo"), ("IC-HI", "hi")):
                    out[rid(c, eje, cat, q)] = _fin(r.get(key))
                out[rid(c, eje, cat, "N")] = int(r.get("n", 0))
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    L = _modulo_desde_bytes("lectores_familia", inputs["lectores_familia"]["bytes"])
    ruta = inputs[PAY]["ruta_absoluta"]
    hog = L.lee_csv_zip(ruta, "THOGAR.csv", COLS_HOG)
    per = L.lee_csv_zip(ruta, "TCSDEMPO.csv", COLS_PER)
    out = mide(hog, per, R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-INPUT-LECTORES-SHA256"] = str(inputs["lectores_familia"].get("sha256"))
    out[f"{P}-G-OLA-UNICA"] = "ENASIC 2022 -- unica ola en corpus; se abre (E.6), sin IC de persistencia"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = [_fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    for c, unidad in CONDUCTAS.items():
        u = "hogares sin ponderar" if unidad == "HOGAR" else "personas sin ponderar"
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_de(unidad).items()):
            for cat in cats:
                f += [_fila(rid(c, eje, cat, "P"), "proporcion", "proporción ponderada"),
                      _fila(rid(c, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      _fila(rid(c, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                      _fila(rid(c, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                      _fila(rid(c, eje, cat, "N"), "entero", u)]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-INPUT-LECTORES-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-UNICA", "texto", "declaración")]
    return f
