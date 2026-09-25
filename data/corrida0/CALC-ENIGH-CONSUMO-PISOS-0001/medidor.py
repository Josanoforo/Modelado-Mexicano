#!/usr/bin/env python3
"""CALC-ENIGH-CONSUMO-PISOS-0001 · pisos de consumo y gasto por segmento, ENIGH 2016-2022.

ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/CONSUMO-ENIGH-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENIGH.

QUÉ ESTIMA. Unidad HOGAR, nunca persona; ponderador `factor` de CONCENTRADOHOGAR; diseño
`est_dis`/`upm` (llaves opacas). Cuatro olas abiertas (2016, 2018, 2020, 2022; ENIGH 2024
RESERVADA, E.6, no es input). Tres clases de conducta:

  · PART-*  participación en un total = razón de totales Σw·num / Σw·den sobre los hogares
    con den > 0. Se obtiene con la receta común pasando peso w·den e y = num/den: la receta
    estima Σ(w·den)(num/den) / Σ(w·den) = Σw·num / Σw·den con las MISMAS réplicas bootstrap.
  · HOG-*   proporción de hogares (0/1).
  · MEDIA-* media ponderada por hogar (pesos corrientes de cada ola; no deflactada).

Pisos por UN eje a la vez (TOTAL, SEXO-JEFE, EDAD-JEFE, ESCOLARIDAD-JEFE, TLOC, DECIL y,
sólo para las conductas marcadas, ENTIDAD); nunca cruces. Sobre el piso 2022, IC calibrado
de persistencia (τ² por conducta × eje, 2016→2018→2020→2022) para PART-* y HOG-*.

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (input `receta_pisos`), sin editarla.
"""
from __future__ import annotations

import math
import types

import numpy as np
import pandas as pd

P = "RESULT-ENIGH-CONSUMO-PISOS"
OLAS = ("2016", "2018", "2020", "2022")
OLA_PISO = "2022"
PAYLOADS = {o: f"enigh{o}_nc_csv" for o in OLAS}
INPUTS_REPO = frozenset({"receta_pisos"})


def _m(ola, tabla):
    sep = "" if ola == "2022" else "_"
    return f"conjunto_de_datos_{tabla}_enigh{sep}{ola}_ns.csv"


LLAVE = ["folioviv", "foliohog"]
RUBROS = ("alimentos", "vesti_calz", "vivienda", "limpieza", "salud", "transporte", "educa_espa",
          "personales", "transf_gas")
COLS_CONC = LLAVE + ["tam_loc", "est_dis", "upm", "factor", "sexo_jefe", "edad_jefe", "educa_jefe",
                     "ing_cor", "gasto_mon", "ali_fuera", "bebidas", "comunica", "prestamos",
                     "pago_tarje", "deudas"] + list(RUBROS)
COLS_HOG = LLAVE + ["celular", "conex_inte", "tarjeta", "pagotarjet"]
COLS_GAS = LLAVE + ["clave", "tipo_gasto", "forma_pag1", "forma_pag2", "forma_pag3", "lugar_comp", "gasto_tri"]

ESCOL = {"HASTA-PRIMARIA": (1, 2, 3, 4), "SECUNDARIA": (5, 6), "MEDIA-SUPERIOR": (7, 8),
         "SUPERIOR": (9, 10, 11)}
EDADES = (("HASTA-29", 0, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
DECILES = tuple(f"D{i:02d}" for i in range(1, 11))
ENTIDADES = tuple(f"{i:02d}" for i in range(1, 33))
EJES = {
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": tuple(c for c, _, _ in EDADES),
    "ESCOLARIDAD-JEFE": tuple(ESCOL),
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
    "DECIL": DECILES,
}
EJE_ENTIDAD = "ENTIDAD"

# canal (lugar_comp, catálogo idéntico 2016-2022)
CANALES = {
    "MERCADO": (1,),
    "TIANGUIS-AMBULANTE": (2, 3),
    "ABARROTES": (4,),
    "ESPECIFICAS-DEL-RAMO": (5,),
    "SUPER-MEMBRESIA": (6, 9),
    "CONVENIENCIA": (10,),
    "OTRO": (7, 8, 11, 12, 13, 14, 15, 16, 17, 18),
}

# conducta -> (tipo, usa ENTIDAD). tipo: "part" | "hog" | "media"
CONDUCTAS = {
    **{f"PART-{r.upper().replace('_', '-')}": ("part", r == "alimentos") for r in RUBROS},
    "PART-COMUNICA": ("part", False),
    "PART-ALI-FUERA-EN-ALIMENTOS": ("part", False),
    "PART-BEBIDAS-EN-ALIMENTOS": ("part", False),
    "PART-EFECTIVO-EN-GASTO-DIRECTO": ("part", False),
    **{f"PART-CANAL-{c}": ("part", c == "SUPER-MEMBRESIA") for c in CANALES},
    "HOG-ALI-FUERA": ("hog", False),
    "HOG-GASTO-COMUNICA": ("hog", False),
    "HOG-TIENE-CELULAR": ("hog", False),
    "HOG-CONEX-INTERNET": ("hog", False),
    "HOG-TIENE-TARJETA-CREDITO": ("hog", True),
    "HOG-USA-TARJETA-ALIMENTOS-SI-TIENE": ("hog", False),
    "HOG-PAGO-TARJETA-CREDITO": ("hog", False),
    "HOG-PAGO-DEUDAS": ("hog", False),
    "HOG-RECIBE-PRESTAMO": ("hog", False),
    "HOG-GASTO-MAYOR-INGRESO": ("hog", False),
    "HOG-COMPRA-FIADO": ("hog", False),
    "HOG-COMPRA-TARJETA-CREDITO": ("hog", False),
    "HOG-COMPRA-INTERNET": ("hog", True),
    "HOG-COMPRA-INTERNET-SI-CONEXION": ("hog", False),
    "MEDIA-GASTO-MON-MENSUAL": ("media", True),
}
Q = ("P", "EE", "IC-LO", "IC-HI", "N")
_DIAG = ("HOGARES", "JOIN-SIN-HOGARES", "HOGARES-DISENO-VALIDO", "ENTIDAD-FUERA-DE-RANGO",
         "FILAS-GASTO", "FILAS-GASTO-SIN-HOGAR")


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
    esperados = INPUTS_REPO | set(PAYLOADS.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in PAYLOADS.values():
        if not inputs[pid].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
        if "2024" in pid:
            raise ParoDeGuardia("ENIGH 2024 RESERVADA (E.6): no es input")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def ejes_de(conducta):
    ejes = dict(EJES)
    if CONDUCTAS[conducta][1]:
        ejes[EJE_ENTIDAD] = ENTIDADES
    return ejes


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _llave(df):
    fv = df["folioviv"].astype(str).str.strip().str.zfill(10)
    fh = df["foliohog"].astype(str).str.strip()
    return fv + "|" + fh


def deciles(ing, w):
    """Decil de hogares por ingreso corriente: orden estable por ing_cor, participación
    acumulada del factor; decil = ceil(10·acumulada) acotado a 1..10 (spec §3)."""
    ing = np.asarray(ing, dtype=float)
    w = np.asarray(w, dtype=float)
    out = np.full(len(ing), None, dtype=object)
    ok = np.isfinite(ing) & (w > 0)
    idx = np.flatnonzero(ok)
    if len(idx) == 0:
        return out
    orden = idx[np.argsort(ing[idx], kind="mergesort")]
    acum = np.cumsum(w[orden]) / w[orden].sum()
    d = np.clip(np.ceil(acum * 10 - 1e-12), 1, 10).astype(int)
    out[orden] = np.array([DECILES[k - 1] for k in d], dtype=object)
    return out


def agrega_gasto(gas, R, llaves_validas):
    """Por hogar: sumas de gasto_tri de gasto monetario directo (tipo_gasto G1) por canal
    (claves A001-A242), total con canal registrado, total G1 y G1 pagado en efectivo
    (forma_pag1 = 1); indicadores de fiado (2), tarjeta de crédito (5) e internet (18)."""
    n = R.num
    g = gas[gas["tipo_gasto"].astype(str).str.strip().str.upper() == "G1"].copy()
    g["_k"] = _llave(g)
    diag_sin = int((~g["_k"].isin(llaves_validas)).sum())
    monto = n(g["gasto_tri"]).fillna(0.0).to_numpy()
    lugar = n(g["lugar_comp"]).to_numpy()
    fp = np.column_stack([n(g[c]).to_numpy() for c in ("forma_pag1", "forma_pag2", "forma_pag3")])
    clave = g["clave"].astype(str).str.strip().str.upper()
    num_clave = pd.to_numeric(clave.str[1:], errors="coerce").to_numpy()
    es_alim = (clave.str[0] == "A").to_numpy() & (num_clave >= 1) & (num_clave <= 242)
    cols = {"_g1": monto, "_efec": np.where(fp[:, 0] == 1, monto, 0.0)}
    con_canal = es_alim & np.isin(lugar, np.arange(1, 19))
    cols["_canal_den"] = np.where(con_canal, monto, 0.0)
    for c, cods in CANALES.items():
        cols[f"_canal_{c}"] = np.where(con_canal & np.isin(lugar, cods), monto, 0.0)
    cols["_fiado"] = np.any(fp == 2, axis=1).astype(float)
    cols["_tcred"] = np.any(fp == 5, axis=1).astype(float)
    cols["_inter"] = (lugar == 18).astype(float)
    df = pd.DataFrame(cols)
    df["_k"] = g["_k"].to_numpy()
    agg = df.groupby("_k", sort=True).agg({**{k: "sum" for k in cols if not k in ("_fiado", "_tcred", "_inter")},
                                             "_fiado": "max", "_tcred": "max", "_inter": "max"})
    return agg, int(len(g)), diag_sin


def prepara(conc, hog, gas, R):
    n = R.num
    diag = {"HOGARES": int(len(conc))}
    conc = conc.copy()
    conc["_k"] = _llave(conc)
    hog = hog.copy()
    hog["_k"] = _llave(hog)
    h = hog.drop_duplicates("_k", keep=False).set_index("_k")
    diag["JOIN-SIN-HOGARES"] = int((~conc["_k"].isin(h.index)).sum())
    for c in ("celular", "conex_inte", "tarjeta", "pagotarjet"):
        conc[c] = conc["_k"].map(h[c]).to_numpy()
    w = n(conc["factor"])
    ok = (w.gt(0) & conc["est_dis"].astype(str).str.strip().ne("")
          & conc["upm"].astype(str).str.strip().ne("")).to_numpy()
    diag["HOGARES-DISENO-VALIDO"] = int(ok.sum())
    f = conc[ok].reset_index(drop=True)
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = f["est_dis"].astype(str).str.strip()
    f["_upm"] = f["upm"].astype(str).str.strip()
    agg, nfilas, sin = agrega_gasto(gas, R, set(f["_k"]))
    diag["FILAS-GASTO"] = nfilas
    diag["FILAS-GASTO-SIN-HOGAR"] = sin
    for c in agg.columns:
        f[c] = f["_k"].map(agg[c]).fillna(0.0).to_numpy()
    edad = n(f["edad_jefe"]).to_numpy()
    ecat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ent = f["folioviv"].astype(str).str.strip().str.zfill(10).str[:2].to_numpy()
    ent_ok = np.isin(ent, ENTIDADES)
    diag["ENTIDAD-FUERA-DE-RANGO"] = int((~ent_ok).sum())
    ent = np.where(ent_ok, ent, None).astype(object)
    ejes = {
        "SEXO-JEFE": (_serie_map(n(f["sexo_jefe"]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES["SEXO-JEFE"]),
        "EDAD-JEFE": (ecat, EJES["EDAD-JEFE"]),
        "ESCOLARIDAD-JEFE": (_serie_map(n(f["educa_jefe"]).to_numpy(), ESCOL), EJES["ESCOLARIDAD-JEFE"]),
        "TLOC": (_serie_map(n(f["tam_loc"]).to_numpy(), dict(zip(EJES["TLOC"], ((1,), (2,), (3,), (4,))))),
                 EJES["TLOC"]),
        "DECIL": (deciles(n(f["ing_cor"]).to_numpy(), f["_w"].to_numpy()), DECILES),
        EJE_ENTIDAD: (ent, ENTIDADES),
    }
    return f, ejes, diag


def _razon(num, den):
    """(y, peso_multiplicador): y = num/den donde den > 0; NaN fuera del universo."""
    num = np.asarray(num, dtype=float)
    den = np.asarray(den, dtype=float)
    ok = np.isfinite(num) & np.isfinite(den) & (den > 0)
    y = np.full(len(den), np.nan)
    y[ok] = num[ok] / den[ok]
    return y, np.where(ok, den, 0.0)


def _bin(cond, universo):
    y = np.where(cond, 1.0, 0.0)
    y[~universo] = np.nan
    return y


def conducta(nombre, f, R):
    """(y, multiplicador de peso) por texto de la spec §2. Multiplicador 1 salvo PART-*."""
    n = R.num
    uno = np.ones(len(f))
    col = lambda c: n(f[c]).to_numpy()  # noqa: E731
    for r in RUBROS:
        if nombre == f"PART-{r.upper().replace('_', '-')}":
            return _razon(col(r), col("gasto_mon"))
    if nombre == "PART-COMUNICA":
        return _razon(col("comunica"), col("gasto_mon"))
    if nombre == "PART-ALI-FUERA-EN-ALIMENTOS":
        return _razon(col("ali_fuera"), col("alimentos"))
    if nombre == "PART-BEBIDAS-EN-ALIMENTOS":
        return _razon(col("bebidas"), col("alimentos"))
    if nombre == "PART-EFECTIVO-EN-GASTO-DIRECTO":
        return _razon(f["_efec"].to_numpy(), f["_g1"].to_numpy())
    for c in CANALES:
        if nombre == f"PART-CANAL-{c}":
            return _razon(f[f"_canal_{c}"].to_numpy(), f["_canal_den"].to_numpy())
    gm = col("gasto_mon")
    todos = np.ones(len(f), dtype=bool)
    if nombre == "HOG-ALI-FUERA":
        v = col("ali_fuera")
        return _bin(v > 0, np.isfinite(v)), uno
    if nombre == "HOG-GASTO-COMUNICA":
        v = col("comunica")
        return _bin(v > 0, np.isfinite(v)), uno
    si_no = {"HOG-TIENE-CELULAR": "celular", "HOG-CONEX-INTERNET": "conex_inte", "HOG-TIENE-TARJETA-CREDITO": "tarjeta"}
    if nombre in si_no:
        v = col(si_no[nombre])
        return _bin(v == 1, np.isin(v, (1, 2))), uno
    if nombre == "HOG-USA-TARJETA-ALIMENTOS-SI-TIENE":
        t, v = col("tarjeta"), col("pagotarjet")
        return _bin(v == 1, (t == 1) & np.isin(v, (1, 2))), uno
    montos = {"HOG-PAGO-TARJETA-CREDITO": "pago_tarje", "HOG-PAGO-DEUDAS": "deudas", "HOG-RECIBE-PRESTAMO": "prestamos"}
    if nombre in montos:
        v = col(montos[nombre])
        return _bin(v > 0, np.isfinite(v)), uno
    if nombre == "HOG-GASTO-MAYOR-INGRESO":
        ing = col("ing_cor")
        return _bin(gm > ing, np.isfinite(gm) & np.isfinite(ing)), uno
    if nombre == "HOG-COMPRA-FIADO":
        return _bin(f["_fiado"].to_numpy() > 0, todos), uno
    if nombre == "HOG-COMPRA-TARJETA-CREDITO":
        return _bin(f["_tcred"].to_numpy() > 0, todos), uno
    if nombre == "HOG-COMPRA-INTERNET":
        return _bin(f["_inter"].to_numpy() > 0, todos), uno
    if nombre == "HOG-COMPRA-INTERNET-SI-CONEXION":
        return _bin(f["_inter"].to_numpy() > 0, col("conex_inte") == 1), uno
    if nombre == "MEDIA-GASTO-MON-MENSUAL":
        return np.where(np.isfinite(gm), gm / 3.0, np.nan), uno
    raise KeyError(nombre)


def mide_ola(frames, R, replicas, semilla):
    f, ejes, diag = prepara(frames["conc"], frames["hog"], frames["gas"], R)
    w = f["_w"].to_numpy()
    res = {}
    for c in CONDUCTAS:
        y, mult = conducta(c, f, R)
        ej = {e: ejes[e] for e in ejes_de(c)}
        res.update(R.marginales(f, {c: y}, ej, w * mult, "_est", "_upm", replicas, semilla))
    return res, diag


def calcula(por_ola, diags, R):
    out = {}
    for ola in OLAS:
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diags[ola][k])
    for c, (tipo, _) in CONDUCTAS.items():
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_de(c).items()):
            serie = {}
            for ola in OLAS:
                serie[ola] = {}
                for cat in cats:
                    r = por_ola[ola].get((c, eje, cat)) or {}
                    p = _fin(r.get("p"))
                    serie[ola][cat] = p
                    out[rid(c, ola, eje, cat, "P")] = p
                    out[rid(c, ola, eje, cat, "EE")] = _fin(r.get("ee"))
                    out[rid(c, ola, eje, cat, "IC-LO")] = _fin(r.get("lo"))
                    out[rid(c, ola, eje, cat, "IC-HI")] = _fin(r.get("hi"))
                    out[rid(c, ola, eje, cat, "N")] = int(r.get("n", 0))
            if tipo == "media":
                continue
            t2, nd = R.persistencia(serie, list(OLAS), cats)
            out[f"{P}-{c}-{eje}-TAU2"] = _fin(t2)
            out[f"{P}-{c}-{eje}-N-DELTAS"] = int(nd)
            for cat in cats:
                lo, hi = R.ic_calibrado(out[rid(c, OLA_PISO, eje, cat, "P")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-LO")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-HI")], t2)
                out[rid(c, OLA_PISO, eje, cat, "ICC-LO")] = _fin(lo)
                out[rid(c, OLA_PISO, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def lee_ola(ruta, ola, R):
    lee = lambda tabla, cols: R.lee_csv_zip(ruta, cols, miembro=_miembro(ruta, _m(ola, tabla)),  # noqa: E731
                                           encoding="utf-8-sig")
    return {"conc": lee("concentradohogar", COLS_CONC), "hog": lee("hogares", COLS_HOG),
            "gas": lee("gastoshogar", COLS_GAS)}


def _miembro(ruta, base):
    import zipfile
    with zipfile.ZipFile(ruta) as z:
        cand = [x for x in z.namelist() if x.split("/")[-1] == base]
    if len(cand) != 1:
        raise ParoDeGuardia(f"{base}: se esperaba 1 miembro, hay {len(cand)}")
    return cand[0]


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    por_ola, diags = {}, {}
    for ola in OLAS:
        frames = lee_ola(inputs[PAYLOADS[ola]]["ruta_absoluta"], ola, R)
        por_ola[ola], diags[ola] = mide_ola(frames, R, replicas, semilla)
        del frames
    out = calcula(por_ola, diags, R)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENIGH 2024 -- RESERVADA (E.6), no es input"
    return out


# ══════════════════════════════ esquema ══════════════════════════════

def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


_UNIDAD = {"part": "razón de totales ponderada (hogar)", "hog": "proporción ponderada de hogares",
           "media": "media ponderada por hogar, pesos corrientes/mes"}


def esquema_resultados():
    f = []
    for ola in OLAS:
        f += [_fila(f"{P}-G-{ola}-{k}", "entero", "filas") for k in _DIAG]
    for c, (tipo, _) in CONDUCTAS.items():
        tp = "flotante" if tipo == "media" else "proporcion"
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_de(c).items()):
            for ola in OLAS:
                for cat in cats:
                    f += [_fila(rid(c, ola, eje, cat, "P"), tp, _UNIDAD[tipo]),
                          _fila(rid(c, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                          _fila(rid(c, ola, eje, cat, "IC-LO"), tp, "IC95 diseño, inferior"),
                          _fila(rid(c, ola, eje, cat, "IC-HI"), tp, "IC95 diseño, superior"),
                          _fila(rid(c, ola, eje, cat, "N"), "entero", "hogares sin ponderar")]
            if tipo == "media":
                continue
            f += [_fila(f"{P}-{c}-{eje}-TAU2", "flotante", "varianza logit entre olas"),
                  _fila(f"{P}-{c}-{eje}-N-DELTAS", "entero", "deltas definidos")]
            for cat in cats:
                f += [_fila(rid(c, OLA_PISO, eje, cat, "ICC-LO"), "proporcion", "IC calibrado persistencia, inferior"),
                      _fila(rid(c, OLA_PISO, eje, cat, "ICC-HI"), "proporcion", "IC calibrado persistencia, superior")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
