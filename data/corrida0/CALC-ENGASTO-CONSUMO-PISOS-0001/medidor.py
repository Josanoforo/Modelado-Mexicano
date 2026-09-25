#!/usr/bin/env python3
"""CALC-ENGASTO-CONSUMO-PISOS-0001 · pisos de canal de compra y conectividad, ENGASTO 2012.

ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONSUMO-ENGASTO-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENGASTO.

QUÉ ESTIMA. Unidad HOGAR; ponderador `factor_hog` (tabla HOGAR); diseño `est_dis`/`upm`
(tabla VIVIENDA, llaves opacas). Ola ENGASTO 2012 = archivos cuyo trazado casa con la
Descripción de la base de datos 2012 (`engasto12_fd.pdf`: HOGAR de 161 campos con
`num_cel`). La ola 2013 (HOGAR de 173 campos, `recurso_*`) es la más reciente y queda
RESERVADA (E.6): sus bytes no son input. Proporciones ponderadas de hogares, total y por UN
eje a la vez (SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC); nunca cruces. Una ola abierta:
sin IC de persistencia.

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (input `receta_pisos`), sin editarla.
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENGASTO-CONSUMO-PISOS"
OLA = "2012"
PAY = {"hogar": "engasto2012_hogar_dta", "vivienda": "engasto_2012_vivienda_dta",
       "lugar": "engasto_2012_lugar_compra_dta", "ajustado": "engasto2012_gasto_de_consumo_ajustado_dta"}
INPUTS_REPO = frozenset({"receta_pisos"})
LLAVE_HOG = ["anio_reg", "trimestre", "folio", "hog_ent_1", "hog_ent_2"]
LLAVE_VIV = ["anio_reg", "trimestre", "folio"]

LC = ["lc_granc", "lc_desecha", "lc_velas", "lc_alimasc", "lc_copias", "lc_tarjtel", "lc_t_aire", "lc_j_azar",
      "lc_peines", "lc_cosmeti", "lc_papel", "lc_graba", "lc_matconf", "lc_prendas", "lc_accvest", "lc_hilo",
      "lc_alropa", "lc_zapato", "lc_rep_zap", "lc_plasti", "lc_herram", "lc_escobas", "lc_medicam", "lc_matcura",
      "lc_accvehi", "lc_aceites", "lc_juegos", "lc_globos", "lc_plantas", "lc_accmasc", "lc_utiles", "lc_joyeria",
      "lc_pipas", "lc_lentes", "lc_vesesc", "lc_paqutil", "lc_muebles", "lc_alfombr", "lc_telas", "lc_blancos",
      "lc_apgran", "lc_apelect", "lc_eqtera", "lc_eqtelef", "lc_eqsonid", "lc_tv_dvd", "lc_eqfoto", "lc_opticos",
      "lc_eproinf", "lc_insmusi", "lc_recreac", "lc_arbnavi", "lc_libros", "lc_mapas", "lc_artcuip", "lc_maletas",
      "lc_jardin", "lc_eqdepo", "lc_repara", "lc_pan", "lc_carne", "lc_pescado", "lc_leche", "lc_aceite",
      "lc_fruta", "lc_verdura", "lc_azucar", "lc_cafe", "lc_agua", "lc_licor", "lc_vino", "lc_cerveza",
      "lc_tabaco", "lc_periodi", "lc_limpie", "lc_higper"]
COLS = {
    "hogar": LLAVE_HOG + ["num_cel", "conex_inte", "factor_hog"],
    "vivienda": LLAVE_VIV + ["tam_loc", "est_dis", "upm"],
    "lugar": LLAVE_HOG + LC,
    "ajustado": LLAVE_HOG + ["sexo_je", "edad_je", "ned_je"],
}

GRAN_COMPRA = {
    "SUPER-MEMBRESIA": (6, 9),
    "MERCADO": (1,),
    "TIANGUIS-AMBULANTE": (2, 3),
    "ABARROTES": (4,),
    "CONVENIENCIA": (10,),
    "DEPARTAMENTAL": (7,),
    "INTERNET": (18,),
    "OTRO": (5, 8, 11, 12, 13, 14, 15, 16, 17),
}
PRODUCTOS = {"CARNE": "lc_carne", "FRUTA": "lc_fruta", "VERDURA": "lc_verdura", "PAN": "lc_pan", "LECHE": "lc_leche"}
FORMATOS = {"SUPER-MEMBRESIA": (6, 9), "MERCADO-TIANGUIS-AMBULANTE": (1, 2, 3)}
CONDUCTAS = tuple(
    [f"GRAN-COMPRA-{c}" for c in GRAN_COMPRA]
    + [f"{p}-EN-{fmt}" for p in PRODUCTOS for fmt in FORMATOS]
    + ["COMPRA-INTERNET-ALGUN-RUBRO", "COMPRA-INTERNET-SI-CONEXION", "TIENE-CELULAR", "CONEX-INTERNET"]
)
ESCOL = {"PRIMARIA-INCOMPLETA": (1,), "PRIMARIA-COMPLETA": (2,), "SECUNDARIA-COMPLETA": (3,),
         "MEDIA-SUPERIOR-Y-SUPERIOR": (4,)}
EDADES = (("HASTA-29", 0, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
EJES = {
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": tuple(c for c, _, _ in EDADES),
    "ESCOLARIDAD-JEFE": tuple(ESCOL),
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
}
Q = ("P", "EE", "IC-LO", "IC-HI", "N")
_DIAG = ("HOGARES", "JOIN-SIN-VIVIENDA", "JOIN-SIN-LUGAR-COMPRA", "JOIN-SIN-JEFE", "JEFE-INCONSISTENTE",
         "HOGARES-DISENO-VALIDO")
VALIDOS = np.arange(1, 19)  # catálogo 01-18; 97 = no especificado; nulo = no compró


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
    esperados = INPUTS_REPO | set(PAY.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in PAY.values():
        ruta = inputs[pid].get("ruta_absoluta")
        if not ruta:
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
        if "engasto2013" in str(ruta):
            raise ParoDeGuardia(f"`{pid}` resuelve a la carpeta de la ola 2013 RESERVADA (E.6)")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def rid(conducta, eje, cat, q):
    return f"{P}-{conducta}-{OLA}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _k(df, cols):
    return df[cols].astype(str).apply(lambda s: s.str.strip()).agg("|".join, axis=1)


def prepara(fr, R):
    n = R.num
    hog = fr["hogar"].copy()
    diag = {"HOGARES": int(len(hog))}
    hog["_kh"] = _k(hog, LLAVE_HOG)
    hog["_kv"] = _k(hog, LLAVE_VIV)
    viv = fr["vivienda"].copy()
    viv["_kv"] = _k(viv, LLAVE_VIV)
    v = viv.drop_duplicates("_kv", keep=False).set_index("_kv")
    diag["JOIN-SIN-VIVIENDA"] = int((~hog["_kv"].isin(v.index)).sum())
    for c in ("tam_loc", "est_dis", "upm"):
        hog[c] = hog["_kv"].map(v[c]).to_numpy()
    lug = fr["lugar"].copy()
    lug["_kh"] = _k(lug, LLAVE_HOG)
    lg = lug.drop_duplicates("_kh", keep=False).set_index("_kh")
    diag["JOIN-SIN-LUGAR-COMPRA"] = int((~hog["_kh"].isin(lg.index)).sum())
    for c in LC:
        hog[c] = hog["_kh"].map(lg[c]).to_numpy()
    aj = fr["ajustado"].copy()
    aj["_kh"] = _k(aj, LLAVE_HOG)
    jefe = aj[["_kh", "sexo_je", "edad_je", "ned_je"]].astype(str).drop_duplicates()
    inconsistentes = jefe["_kh"].duplicated(keep=False)
    diag["JEFE-INCONSISTENTE"] = int(jefe.loc[inconsistentes, "_kh"].nunique())
    j = jefe[~inconsistentes].set_index("_kh")
    diag["JOIN-SIN-JEFE"] = int((~hog["_kh"].isin(j.index)).sum())
    for c in ("sexo_je", "edad_je", "ned_je"):
        hog[c] = hog["_kh"].map(j[c]).to_numpy()
    w = n(hog["factor_hog"])
    ok = (w.gt(0) & hog["est_dis"].astype(str).str.strip().ne("") & hog["est_dis"].notna()
          & hog["upm"].astype(str).str.strip().ne("") & hog["upm"].notna()).to_numpy()
    diag["HOGARES-DISENO-VALIDO"] = int(ok.sum())
    f = hog[ok].reset_index(drop=True)
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = f["est_dis"].astype(str).str.strip()
    f["_upm"] = f["upm"].astype(str).str.strip()
    edad = n(f["edad_je"]).to_numpy()
    ecat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ejes = {
        "SEXO-JEFE": (_serie_map(n(f["sexo_je"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES["SEXO-JEFE"]),
        "EDAD-JEFE": (ecat, EJES["EDAD-JEFE"]),
        "ESCOLARIDAD-JEFE": (_serie_map(n(f["ned_je"]).to_numpy(), ESCOL), EJES["ESCOLARIDAD-JEFE"]),
        "TLOC": (_serie_map(n(f["tam_loc"]).to_numpy(), dict(zip(EJES["TLOC"], ((1,), (2,), (3,), (4,))))),
                 EJES["TLOC"]),
    }
    return f, ejes, diag


def _bin(cond, universo):
    y = np.where(cond, 1.0, 0.0)
    y[~universo] = np.nan
    return y


def conducta_y(nombre, f, R):
    n = R.num
    for c, cods in GRAN_COMPRA.items():
        if nombre == f"GRAN-COMPRA-{c}":
            v = n(f["lc_granc"]).to_numpy()
            return _bin(np.isin(v, cods), np.isin(v, VALIDOS))
    for p, col in PRODUCTOS.items():
        for fmt, cods in FORMATOS.items():
            if nombre == f"{p}-EN-{fmt}":
                v = n(f[col]).to_numpy()
                return _bin(np.isin(v, cods), np.isin(v, VALIDOS))
    if nombre in ("COMPRA-INTERNET-ALGUN-RUBRO", "COMPRA-INTERNET-SI-CONEXION"):
        m = np.column_stack([n(f[c]).to_numpy() for c in LC])
        alguno = np.any(np.isin(m, VALIDOS), axis=1)
        inter = np.any(m == 18, axis=1)
        if nombre == "COMPRA-INTERNET-ALGUN-RUBRO":
            return _bin(inter, alguno)
        return _bin(inter, alguno & (n(f["conex_inte"]).to_numpy() == 1))
    if nombre == "TIENE-CELULAR":
        v = n(f["num_cel"]).to_numpy()
        return _bin(v >= 1, (v >= 0) & (v <= 50))
    if nombre == "CONEX-INTERNET":
        v = n(f["conex_inte"]).to_numpy()
        return _bin(v == 1, np.isin(v, (1, 2)))
    raise KeyError(nombre)


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


def mide(fr, R, replicas, semilla):
    f, ejes, diag = prepara(fr, R)
    cond = {c: conducta_y(c, f, R) for c in CONDUCTAS}
    res = R.marginales(f, cond, ejes, f["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    return calcula(res, diag)


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    fr = {k: R.lee_dta(inputs[pid]["ruta_absoluta"], COLS[k]) for k, pid in PAY.items()}
    out = mide(fr, R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENGASTO 2013 -- RESERVADA (E.6), no es input; se abre sólo 2012"
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
                f += [_fila(rid(c, eje, cat, "P"), "proporcion", "proporción ponderada de hogares"),
                      _fila(rid(c, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      _fila(rid(c, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                      _fila(rid(c, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                      _fila(rid(c, eje, cat, "N"), "entero", "hogares sin ponderar")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
