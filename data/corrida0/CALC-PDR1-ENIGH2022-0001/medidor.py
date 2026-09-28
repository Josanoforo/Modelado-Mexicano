#!/usr/bin/env python3
"""CALC-PDR1-ENIGH2022-0001 · regla RG-cc1c9ab8f1 (escuela privada de la clase media urbana), ENIGH 2022.

ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1, pieza P-ENIGH2022 (CAJA). Contrato humano:
forense/prereg-caja/PDR1-ENIGH2022-spec-v1_0.md, congelado en COMMIT-1 antes de abrir el dato.

QUÉ ESTIMA. Unidad HOGAR; ponderador `factor` (CONCENTRADOHOGAR); diseño `est_dis`/`upm`
(llaves opacas). Universo: hogares con al menos un integrante que asiste a la escuela
(POBLACION.asis_esc = 1). Conducta observable (el motivo «miedo a caer» NO es observable):

  · PRIV   hogar con gasto monetario (tipo_gasto G1) en inscripción o colegiatura
           (GASTOSPERSONA claves E001-E007, inscrip>0 o colegia>0) de un integrante que
           asiste a escuela «Privada o de paga» (POBLACION.tipoesc = 2).
  · ASIPRIV hogar con al menos un integrante que asiste a escuela privada (tipoesc = 2).
  · CARGA  razón de totales Σw·gasto_tri(PRIV) / Σw·ing_cor entre hogares PRIV con ing_cor>0.

Celdas: decil de ingreso corriente (deciles de TODOS los hogares, factor) × ámbito
(TOTAL, URBANO tam_loc 1-3, RURAL tam_loc 4); bloques I-IV, V-VIII, IX-X; diferencias
con IC de las MISMAS réplicas. Segmentación mínima: TLOC, SEXO-JEFE, EDAD-JEFE (PRIV).
Bootstrap: receta común `tools/dominios/salud/pisos_diseno.py` (input `receta_pisos`)
ejecutada desde sus bytes hasheados, sin editarla.
"""
from __future__ import annotations

import io
import math
import types
import zipfile

import numpy as np
import pandas as pd

P = "RESULT-PDR1-ENIGH2022"
PAYLOAD = "enigh2022_nc_csv"
INPUTS_REPO = frozenset({"receta_pisos"})
LLAVE = ["folioviv", "foliohog"]
COLS_CONC = LLAVE + ["tam_loc", "est_dis", "upm", "factor", "sexo_jefe", "edad_jefe", "ing_cor"]
COLS_POB = LLAVE + ["numren", "asis_esc", "tipoesc"]
COLS_GP = LLAVE + ["numren", "clave", "tipo_gasto", "inscrip", "colegia", "gasto_tri"]
CLAVES_COLEG = tuple(f"E{i:03d}" for i in range(1, 8))  # catálogo de gastos, «Gastos en educación básica, media o superior»
DECILES = tuple(f"D{i:02d}" for i in range(1, 11))
BLOQUES = {"B1-IV": DECILES[0:4], "B2-VIII": DECILES[4:8], "B3-X": DECILES[8:10]}
AMBITOS = ("TOTAL", "URBANO", "RURAL")
AMB_CARGA = ("TOTAL", "URBANO")
EDADES = (("HASTA-29", 0, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
SEGMENTOS = {
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": tuple(c for c, _, _ in EDADES),
}
Q = ("P", "IC-LO", "IC-HI", "N")
DIFS = {  # id -> (conducta, ámbito, bloque minuendo, bloque sustraendo)
    "DIF-PRIV-URBANO-B2-MENOS-B1": ("PRIV", "URBANO", "B2-VIII", "B1-IV"),
    "DIF-PRIV-TOTAL-B2-MENOS-B1": ("PRIV", "TOTAL", "B2-VIII", "B1-IV"),
    "DIF-PRIV-RURAL-B2-MENOS-B1": ("PRIV", "RURAL", "B2-VIII", "B1-IV"),
    "DIF-ASIPRIV-URBANO-B2-MENOS-B1": ("ASIPRIV", "URBANO", "B2-VIII", "B1-IV"),
    "DIF-CARGA-URBANO-B2-MENOS-B3": ("CARGA", "URBANO", "B2-VIII", "B3-X"),
    "DIF-CARGA-TOTAL-B2-MENOS-B3": ("CARGA", "TOTAL", "B2-VIII", "B3-X"),
}
DICTAMENES = ("CONFIRMA", "MATIZA", "ROMPE", "NO-CONSTRUIBLE")
_DIAG = ("HOGARES", "HOGARES-DISENO-VALIDO", "HOGARES-UNIVERSO", "HOGARES-PRIV", "HOGARES-ASIPRIV",
         "FILAS-GP-COLEG", "FILAS-GP-COLEG-PRIVADA", "FILAS-GP-SIN-PERSONA", "POB-SIN-HOGAR")


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
    esperados = INPUTS_REPO | {PAYLOAD}
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    if not inputs[PAYLOAD].get("ruta_absoluta"):
        raise ParoDeGuardia("payload sin ruta resuelta")
    if "2024" in str(inputs[PAYLOAD]["ruta_absoluta"]):
        raise ParoDeGuardia("ENIGH 2024 RESERVADA (E.6): no es input")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


# ─────────────────────────────── lectura ───────────────────────────────

def _miembro(z, tabla):
    base = f"conjunto_de_datos_{tabla}_enigh2022_ns.csv"
    cand = [x for x in z.namelist() if x.split("/")[-1] == base]
    if len(cand) != 1:
        raise ParoDeGuardia(f"{base}: se esperaba 1 miembro, hay {len(cand)}")
    return cand[0]


def _lee(ruta, tabla, cols, filtro=None, chunk=200_000):
    """Lectura por chunks con usecols (memoria compartida); `filtro(df)->bool mask` por chunk."""
    partes = []
    with zipfile.ZipFile(ruta) as z:
        with z.open(_miembro(z, tabla)) as fb:
            f = io.TextIOWrapper(fb, encoding="utf-8-sig", newline="")
            for df in pd.read_csv(f, usecols=lambda c: c.strip().lower() in cols, dtype=str,
                                  keep_default_na=False, chunksize=chunk):
                df.columns = [c.strip().lower() for c in df.columns]
                if filtro is not None:
                    df = df[filtro(df)]
                partes.append(df)
    df = pd.concat(partes, ignore_index=True) if partes else pd.DataFrame(columns=cols)
    faltan = [c for c in cols if c not in df.columns]
    if faltan:
        raise ParoDeGuardia(f"columnas ausentes en {tabla}: {faltan}")
    return df[cols]


def _filtro_gp(df):
    return df["clave"].astype(str).str.strip().str.upper().isin(CLAVES_COLEG).to_numpy()


def lee(ruta):
    return {"conc": _lee(ruta, "concentradohogar", COLS_CONC),
            "pob": _lee(ruta, "poblacion", COLS_POB),
            "gp": _lee(ruta, "gastospersona", COLS_GP, filtro=_filtro_gp)}


# ─────────────────────────────── preparación ───────────────────────────────

def _llave(df):
    fv = df["folioviv"].astype(str).str.strip().str.zfill(10)
    fh = df["foliohog"].astype(str).str.strip()
    return fv + "|" + fh


def _llave_p(df):
    return _llave(df) + "|" + df["numren"].astype(str).str.strip().str.zfill(2)


def deciles(ing, w):
    """Idéntico a CALC-ENIGH-CONSUMO-PISOS-0002: orden estable por ing_cor, participación
    acumulada del factor; decil = ceil(10·acumulada) acotado a 1..10."""
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


def prepara(fr, R):
    n = R.num
    conc = fr["conc"].copy()
    diag = {"HOGARES": int(len(conc))}
    conc["_k"] = _llave(conc)
    w = n(conc["factor"])
    ok = (w.gt(0) & conc["est_dis"].astype(str).str.strip().ne("")
          & conc["upm"].astype(str).str.strip().ne("")).to_numpy()
    diag["HOGARES-DISENO-VALIDO"] = int(ok.sum())
    f = conc[ok].reset_index(drop=True)
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = f["est_dis"].astype(str).str.strip()
    f["_upm"] = f["upm"].astype(str).str.strip()
    f["_ing"] = n(f["ing_cor"]).to_numpy()
    f["_dec"] = deciles(f["_ing"].to_numpy(), f["_w"].to_numpy())

    pob = fr["pob"].copy()
    pob["_k"] = _llave(pob)
    pob["_kp"] = _llave_p(pob)
    diag["POB-SIN-HOGAR"] = int((~pob["_k"].isin(set(conc["_k"]))).sum())
    asis = n(pob["asis_esc"]).to_numpy() == 1
    priv = asis & (n(pob["tipoesc"]).to_numpy() == 2)
    k_asis = set(pob.loc[asis, "_k"])
    k_asipriv = set(pob.loc[priv, "_k"])
    kp_priv = set(pob.loc[priv, "_kp"])
    kp_todos = set(pob["_kp"])

    gp = fr["gp"].copy()
    gp = gp[gp["tipo_gasto"].astype(str).str.strip().str.upper() == "G1"]
    ins = n(gp["inscrip"]).fillna(0.0).to_numpy()
    col = n(gp["colegia"]).fillna(0.0).to_numpy()
    gp = gp[(ins > 0) | (col > 0)].copy()
    gp["_kp"] = _llave_p(gp)
    gp["_k"] = _llave(gp)
    diag["FILAS-GP-COLEG"] = int(len(gp))
    diag["FILAS-GP-SIN-PERSONA"] = int((~gp["_kp"].isin(kp_todos)).sum())
    gpp = gp[gp["_kp"].isin(kp_priv)]
    diag["FILAS-GP-COLEG-PRIVADA"] = int(len(gpp))
    monto = gpp.assign(_g=n(gpp["gasto_tri"]).fillna(0.0).to_numpy()).groupby("_k")["_g"].sum()

    f["_univ"] = f["_k"].isin(k_asis).to_numpy()
    f["_priv"] = f["_k"].isin(set(monto.index)).to_numpy() & f["_univ"].to_numpy()
    f["_asipriv"] = f["_k"].isin(k_asipriv).to_numpy() & f["_univ"].to_numpy()
    f["_gpriv"] = f["_k"].map(monto).fillna(0.0).to_numpy()
    diag["HOGARES-UNIVERSO"] = int(f["_univ"].sum())
    diag["HOGARES-PRIV"] = int(f["_priv"].sum())
    diag["HOGARES-ASIPRIV"] = int(f["_asipriv"].sum())

    tl = n(f["tam_loc"]).to_numpy()
    amb = {"TOTAL": np.isin(tl, (1, 2, 3, 4)), "URBANO": np.isin(tl, (1, 2, 3)), "RURAL": tl == 4}
    seg = {"TLOC": {c: tl == v for c, v in zip(SEGMENTOS["TLOC"], (1, 2, 3, 4))}}
    sx = n(f["sexo_jefe"]).to_numpy()
    seg["SEXO-JEFE"] = {"HOMBRE": sx == 1, "MUJER": sx == 2}
    ed = n(f["edad_jefe"]).to_numpy()
    seg["EDAD-JEFE"] = {c: (ed >= lo) & (ed <= hi) for c, lo, hi in EDADES}
    return f, amb, seg, diag


# ─────────────────────────────── estimación ───────────────────────────────

def _celdas(f, amb, ambitos):
    """[(nombre, máscara)] para decil×ámbito y bloque×ámbito (sin el filtro de universo)."""
    dec = f["_dec"].to_numpy()
    out = []
    for a in ambitos:
        out.append((("TODOS", a), amb[a]))
        for d in DECILES:
            out.append(((d, a), amb[a] & (dec == d)))
        for b, ds in BLOQUES.items():
            out.append(((b, a), amb[a] & np.isin(dec, ds)))
    return out


def _corre(R, f, y, w, universo, celdas, replicas, semilla):
    mascaras = [universo & np.isfinite(y) & m for _, m in celdas]
    pts, reps, nn = R.bootstrap(f, y, w, "_est", "_upm", mascaras, replicas, semilla)
    return {nom: (pts[j], reps[:, j], int(nn[j])) for j, (nom, _) in enumerate(celdas)}


def mide(f, amb, seg, R, replicas, semilla):
    w = f["_w"].to_numpy()
    univ = f["_univ"].to_numpy()
    res = {}
    cel = _celdas(f, amb, AMBITOS)
    for c, col in (("PRIV", "_priv"), ("ASIPRIV", "_asipriv")):
        y = f[col].to_numpy().astype(float)
        res[c] = _corre(R, f, y, w, univ, cel, replicas, semilla)
    segcel = [((cat, eje), m) for eje, d in seg.items() for cat, m in d.items()]
    res["PRIV-SEG"] = _corre(R, f, f["_priv"].to_numpy().astype(float), w, univ, segcel, replicas, semilla)
    ing = f["_ing"].to_numpy()
    okc = f["_priv"].to_numpy() & np.isfinite(ing) & (ing > 0)
    y = np.full(len(f), np.nan)
    y[okc] = f["_gpriv"].to_numpy()[okc] / ing[okc]
    wc = np.where(okc, w * np.where(okc, ing, 0.0), 0.0)
    res["CARGA"] = _corre(R, f, y, wc, okc, _celdas(f, amb, AMB_CARGA), replicas, semilla)
    return res


def _q(R, p, reps):
    ee, lo, hi, _ = R.resumen(p, reps)
    return _fin(p), _fin(lo), _fin(hi)


def rid(conducta, ambito, cat, q):
    return f"{P}-{conducta}-{ambito}-{cat}-{q}"


def dictamen(d_priv_lo, d_carga_p):
    """B-bis (spec §5), mecánico. Parte 1: IC95 inferior de DIF-PRIV-URBANO-B2-MENOS-B1 > 0.
    Parte 2: punto de DIF-CARGA-URBANO-B2-MENOS-B3 >= 0. Manda la parte 1."""
    if d_priv_lo is None:
        return "NO-CONSTRUIBLE"
    if not d_priv_lo > 0:
        return "ROMPE"
    if d_carga_p is None:
        return "NO-CONSTRUIBLE"
    return "CONFIRMA" if d_carga_p >= 0 else "MATIZA"


def calcula(res, diag, R):
    out = {f"{P}-G-{k}": int(diag[k]) for k in _DIAG}
    for c, ambs in (("PRIV", AMBITOS), ("ASIPRIV", AMBITOS), ("CARGA", AMB_CARGA)):
        for a in ambs:
            for cat in ("TODOS",) + DECILES + tuple(BLOQUES):
                p, reps, nn = res[c][(cat, a)]
                pp, lo, hi = _q(R, p, reps)
                out[rid(c, a, cat, "P")] = pp
                out[rid(c, a, cat, "IC-LO")] = lo
                out[rid(c, a, cat, "IC-HI")] = hi
                out[rid(c, a, cat, "N")] = nn
    for eje, cats in SEGMENTOS.items():
        for cat in cats:
            p, reps, nn = res["PRIV-SEG"][(cat, eje)]
            pp, lo, hi = _q(R, p, reps)
            for q, v in zip(Q, (pp, lo, hi, nn)):
                out[f"{P}-PRIV-{eje}-{cat}-{q}"] = v
    for k, (c, a, b1, b2) in DIFS.items():
        p1, r1, _ = res[c][(b1, a)]
        p2, r2, _ = res[c][(b2, a)]
        pp, lo, hi = _q(R, p1 - p2, r1 - r2)
        out[f"{P}-{k}-P"], out[f"{P}-{k}-IC-LO"], out[f"{P}-{k}-IC-HI"] = pp, lo, hi
    out[f"{P}-DICTAMEN-RG-cc1c9ab8f1"] = dictamen(out[f"{P}-DIF-PRIV-URBANO-B2-MENOS-B1-IC-LO"],
                                                  out[f"{P}-DIF-CARGA-URBANO-B2-MENOS-B3-P"])
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    fr = lee(inputs[PAYLOAD]["ruta_absoluta"])
    f, amb, seg, diag = prepara(fr, R)
    del fr
    out = calcula(mide(f, amb, seg, R, replicas, semilla), diag, R)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENIGH 2024 -- RESERVADA (E.6), no es input"
    out[f"{P}-G-MOTIVO-NO-OBSERVABLE"] = ("«miedo a caer» no es observable en ENIGH: se contrasta solo la "
                                         "conducta (gasto en colegiatura privada y su carga)")
    return out


# ══════════════════════════════ esquema ══════════════════════════════

def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


_U = {"PRIV": "proporción ponderada de hogares (universo: hogares con integrante que asiste a la escuela)",
      "ASIPRIV": "proporción ponderada de hogares (universo: hogares con integrante que asiste a la escuela)",
      "CARGA": "razón de totales gasto_tri colegiatura privada / ing_cor (hogares PRIV)"}


def esquema_resultados():
    f = [_fila(f"{P}-G-{k}", "entero", "filas u hogares sin ponderar") for k in _DIAG]
    for c, ambs in (("PRIV", AMBITOS), ("ASIPRIV", AMBITOS), ("CARGA", AMB_CARGA)):
        for a in ambs:
            for cat in ("TODOS",) + DECILES + tuple(BLOQUES):
                f += [_fila(rid(c, a, cat, "P"), "flotante", _U[c]),
                      _fila(rid(c, a, cat, "IC-LO"), "flotante", "IC95 diseño, inferior"),
                      _fila(rid(c, a, cat, "IC-HI"), "flotante", "IC95 diseño, superior"),
                      _fila(rid(c, a, cat, "N"), "entero", "hogares sin ponderar")]
    for eje, cats in SEGMENTOS.items():
        for cat in cats:
            f += [_fila(f"{P}-PRIV-{eje}-{cat}-P", "flotante", _U["PRIV"]),
                  _fila(f"{P}-PRIV-{eje}-{cat}-IC-LO", "flotante", "IC95 diseño, inferior"),
                  _fila(f"{P}-PRIV-{eje}-{cat}-IC-HI", "flotante", "IC95 diseño, superior"),
                  _fila(f"{P}-PRIV-{eje}-{cat}-N", "entero", "hogares sin ponderar")]
    for k in DIFS:
        f += [_fila(f"{P}-{k}-P", "flotante", "diferencia de bloques, misma unidad"),
              _fila(f"{P}-{k}-IC-LO", "flotante", "IC95 de la diferencia (mismas réplicas)"),
              _fila(f"{P}-{k}-IC-HI", "flotante", "IC95 de la diferencia (mismas réplicas)")]
    f += [_fila(f"{P}-DICTAMEN-RG-cc1c9ab8f1", "texto", "vocabulario cerrado CONFIRMA|MATIZA|ROMPE|NO-CONSTRUIBLE"),
          _fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración"),
          _fila(f"{P}-G-MOTIVO-NO-OBSERVABLE", "texto", "declaración")]
    return f
