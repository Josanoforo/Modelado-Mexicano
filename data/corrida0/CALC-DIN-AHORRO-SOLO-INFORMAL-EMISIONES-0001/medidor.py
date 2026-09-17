#!/usr/bin/env python3
"""Medidor de `CALC-DIN-AHORRO-SOLO-INFORMAL-EMISIONES-0001` (`COMMIT-2`).

ACTO `GEN2-CELDA-D-PILOTO-1`. Contrato humano:
`forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md`, congelado
antes de abrir microdato. Firma vigente: **`FP-379 · ENMIENDA`** (mesa,
16/sep/2026) — `D9` (los NUEVE tipos de cuenta) es el desenlace **primario**
en `C1`, `C2`, `C3` y `R`; `D7` (siete) se emite como **sensibilidad que NO
adjudica**.

Interfaz estable del plan v2.0 §4 (B-1): `medir(inputs, contrato) -> dict`.
El medidor **no abre `spec.yaml`**: recibe el contrato normalizado.

QUÉ ABRE, Y QUÉ NO
------------------
  · **ENIF 2021, entera** — es la ola de desarrollo. De ahí sale `C1` (el cruce
    `localidad × edad`) y el `n` de soporte.
  · **ENIF 2024, SÓLO marginales de UN EJE** — `localidad`, `edad` y nacional.
    Alimentan el IC de `C2` por réplicas compartidas (`FP-379 D3`) y el control
    de reproducción del árbitro marginal sellado.

GUARDIA DE RESERVA, mecánica y no promesa
-----------------------------------------
Sobre ENIF 2024 este archivo **nunca** construye la llave `(localidad, edad)`.
La guardia no es un comentario: `_marginales_2024()` recibe una lista de
agrupaciones de **un solo eje** y `_GUARDIA.cruce_2024` se pondría en `SI` si
alguien intentara pasar dos ejes a la vez. El resultado se emite como
`RESULT-…-G-C2-CRUCE-2024-DERIVADO`. Derivar el cruce de 2024 es `COMMIT-3`.

`C2` NO REIMPLEMENTA SU FÓRMULA
-------------------------------
Importa `piso_log_aditivo` de `tests/test_celda_d_c2.py`, donde el contrato
está pinado con fixtures sintéticos (rango `(0,1)`, rechazo explícito si algún
marginal es `0` o `1`, identidad de desenlace). Contrato y ejecutable no pueden
divergir porque son el mismo objeto.
"""
from __future__ import annotations

import importlib.util
import io
import json
import statistics
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[3]
CORRIDAS_L = RAIZ / "forense" / "prereg-duelo-v2" / "corridas-L"

# ── la función de referencia de C2, importada, nunca reimplementada ─────────
_spec = importlib.util.spec_from_file_location(
    "test_celda_d_c2", RAIZ / "tests" / "test_celda_d_c2.py")
_c2 = importlib.util.module_from_spec(_spec)
sys.modules["test_celda_d_c2"] = _c2
_spec.loader.exec_module(_c2)
piso_log_aditivo = _c2.piso_log_aditivo
MarginalDegenerado = _c2.MarginalDegenerado

# ── la regla congelada de extracción de L ──────────────────────────────────
_spec_x = importlib.util.spec_from_file_location(
    "extrae_l_v1_1", RAIZ / "tools" / "extrae_l_v1_1.py")
_x = importlib.util.module_from_spec(_spec_x)
sys.modules["extrae_l_v1_1"] = _x
_spec_x.loader.exec_module(_x)
extraer_valor = _x.extraer_valor

P = "RESULT-DIN-LXE8"
CELDAS = ["L1xE1", "L1xE2", "L1xE3", "L1xE4", "L2xE1", "L2xE2", "L2xE3", "L2xE4"]
DESENLACE_D9 = "ahorra_solo_informal::P5_6_{1..9}"
ROTULO_SUPUESTO = "ausencia de interaccion en escala logit"


class _Guardia:
    """Estado observable de la reserva. No es prosa: se emite como RESULT."""

    def __init__(self):
        self.cruce_2024 = "NO"

    def registra_agrupacion_2024(self, ejes):
        if len(ejes) > 1:
            self.cruce_2024 = "SI"


_GUARDIA = _Guardia()


# ══ lectura ════════════════════════════════════════════════════════════════

def _lee_miembro(zip_path, sufijo_miembro, usecols):
    """Lee UN miembro del zip. Los .zip de INEGI mezclan UTF-8 y latin-1 entre
    catálogos y microdato: se intenta utf-8 y se cae a latin-1 DECLARANDO la
    caída, nunca en silencio."""
    with zipfile.ZipFile(zip_path) as zf:
        nombre = next(n for n in zf.namelist()
                      if n.endswith(sufijo_miembro))
        crudo = zf.read(nombre)
    for enc in ("utf-8", "latin-1"):
        try:
            texto = crudo.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:                                            # pragma: no cover
        raise RuntimeError(f"{sufijo_miembro}: ni utf-8 ni latin-1")
    df = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False,
                     na_filter=False)
    df.columns = [c.strip() for c in df.columns]
    faltan = [c for c in usecols if c not in df.columns]
    if faltan:
        raise RuntimeError(f"{sufijo_miembro}: columnas ausentes {faltan} "
                           f"(hay {len(df.columns)})")
    return df, nombre, enc


def _universo(df, col_edad, col_tloc, col_w, cols_codigo):
    """Los tres filtros de la spec §3.1, en orden, con sus conteos."""
    n_archivo = len(df)
    edad_txt = df[col_edad].str.strip()
    centinela = edad_txt.isin(["98", "99"])
    edad_num = pd.to_numeric(edad_txt, errors="coerce")
    f_edad = (~centinela) & edad_num.between(18, 97)
    f_tloc = df[col_tloc].str.strip().isin(["1", "2", "3", "4"])
    w_num = pd.to_numeric(df[col_w].str.strip(), errors="coerce")
    f_w = w_num.notna() & (w_num > 0)
    keep = f_edad & f_tloc & f_w

    fuera_dominio = pd.Series(False, index=df.index)
    for c in cols_codigo:
        fuera_dominio |= ~df[c].str.strip().isin(["1", "2", ""])

    u = df.loc[keep].copy()
    u["_w"] = w_num.loc[keep].astype(float)
    u["_edad"] = edad_num.loc[keep].astype(int)
    peso_total = float(w_num.fillna(0).clip(lower=0).sum())
    return {
        "u": u,
        "n_archivo": n_archivo,
        "n_universo": int(keep.sum()),
        "n_centinela": int(centinela.sum()),
        "cobertura_sin_ponderar": float(keep.sum()) / n_archivo if n_archivo else 0.0,
        "cobertura_ponderada": (float(u["_w"].sum()) / peso_total) if peso_total else 0.0,
        "filas_fuera_de_dominio": int((fuera_dominio & keep).sum()),
    }


def _si(serie):
    return serie.str.strip().eq("1")


def _desenlaces(u, cols_inf, cols_f9, cols_f7):
    informal = np.zeros(len(u), dtype=bool)
    for c in cols_inf:
        informal |= _si(u[c]).to_numpy()
    f9 = np.zeros(len(u), dtype=bool)
    for c in cols_f9:
        f9 |= _si(u[c]).to_numpy()
    f7 = np.zeros(len(u), dtype=bool)
    for c in cols_f7:
        f7 |= _si(u[c]).to_numpy()
    return {"D9": informal & ~f9, "D7": informal & ~f7}


# ══ bootstrap de conglomerados estratificado ═══════════════════════════════

def _replicas(estratos, upms, semilla, n_rep):
    """Índices de UPM re-muestreadas, `n_h` con reemplazo dentro de cada
    estrato. UN generador, estratos en orden lexicográfico de `EST_DIS` y UPM
    en orden lexicográfico de `UPM_DIS`: dos corridas del mismo código sobre
    los mismos bytes dan los mismos 10 000 vectores.

    Devuelve `counts` (n_rep × n_upm, int32): cuántas veces entra cada UPM en
    cada réplica. Con eso, `counts @ Y` da los totales de golpe."""
    orden = np.lexsort((upms,))                      # UPM lexicográfico
    est_ord, upm_ord = estratos[orden], upms[orden]
    claves = np.array([f"{e}\t{u}" for e, u in zip(est_ord, upm_ord)])
    unicas, primeras = np.unique(claves, return_index=True)
    # posiciones de cada UPM única, en orden (EST_DIS, UPM_DIS)
    upm_est = est_ord[primeras]
    pos_por_estrato = {}
    for pos, e in enumerate(upm_est):
        pos_por_estrato.setdefault(e, []).append(pos)
    n_upm = len(unicas)
    rng = np.random.Generator(np.random.PCG64(semilla))
    bloques = []
    for e in sorted(pos_por_estrato):                # estratos lexicográficos
        pos = np.asarray(pos_por_estrato[e], dtype=np.int32)
        bloques.append(pos[rng.integers(0, len(pos), size=(n_rep, len(pos)))])
    idx = np.concatenate(bloques, axis=1)
    counts = np.empty((n_rep, n_upm), dtype=np.int32)
    for r in range(n_rep):
        counts[r] = np.bincount(idx[r], minlength=n_upm)
    estratos_upm_unica = sum(1 for e in pos_por_estrato
                             if len(pos_por_estrato[e]) == 1)
    return counts, unicas, n_upm, estratos_upm_unica


def _agrega_por_upm(claves_upm, unicas, w, matriz_y):
    """`W[u, g]` y `Y[u, g, d]` — suma de pesos y de peso×indicador por UPM."""
    pos = np.searchsorted(unicas, claves_upm)
    n_upm = len(unicas)
    W = np.zeros((n_upm, matriz_y.shape[1]))
    Y = np.zeros((n_upm, matriz_y.shape[1], matriz_y.shape[2]))
    for g in range(matriz_y.shape[1]):
        np.add.at(W, (pos, g), w * matriz_y[:, g, -1])   # última col = pertenencia
        for d in range(matriz_y.shape[2] - 1):
            np.add.at(Y, (pos, g, d), w * matriz_y[:, g, d])
    return W, Y


def _punto_e_ic(counts, W, Y, pct=(2.5, 97.5), bloque=1000):
    """Devuelve (punto, ic_inf, ic_sup, replicas) por (grupo, desenlace)."""
    n_rep = counts.shape[0]
    n_g, n_d = Y.shape[1], Y.shape[2]
    reps = np.empty((n_rep, n_g, n_d))
    for a in range(0, n_rep, bloque):
        b = min(a + bloque, n_rep)
        c = counts[a:b].astype(np.float64)
        den = c @ W                                   # (bloque, n_g)
        for d in range(n_d):
            num = c @ Y[:, :, d]
            with np.errstate(invalid="ignore", divide="ignore"):
                reps[a:b, :, d] = np.where(den > 0, num / den, np.nan)
    punto = np.empty((n_g, n_d))
    for g in range(n_g):
        for d in range(n_d):
            den_g = W[:, g].sum()
            punto[g, d] = (Y[:, g, d].sum() / den_g) if den_g > 0 else np.nan
    inf = np.nanpercentile(reps, pct[0], axis=0)
    sup = np.nanpercentile(reps, pct[1], axis=0)
    return punto, inf, sup, reps


def _matriz(grupos, desenlaces):
    """Construye `matriz_y[fila, grupo, d]` con una columna extra de
    pertenencia al grupo (la última), que es el denominador."""
    n = len(grupos[0][1])
    n_g, n_d = len(grupos), len(desenlaces)
    m = np.zeros((n, n_g, n_d + 1))
    for g, (_nombre, mask) in enumerate(grupos):
        m[:, g, -1] = mask.astype(float)
        for d, (_dn, y) in enumerate(desenlaces):
            m[:, g, d] = (mask & y).astype(float)
    return m


# ══ el medidor ═════════════════════════════════════════════════════════════

def medir(inputs, contrato):
    par = contrato["parametros"]
    n_rep = int(par["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    umbral_n = int(par["umbral_soporte_n"])
    out = {}

    for iid, clave in (("enif2021_csv", "ENIF2021-CSV"),
                       ("enif2021_fd_zip", "ENIF2021-FD"),
                       ("enif2024_csv", "ENIF2024-CSV"),
                       ("enif2024_fd_xlsx", "ENIF2024-FD")):
        out[f"{P}-G-INPUT-{clave}-SHA256"] = str(inputs[iid]["sha256"])

    # ── C1 · ENIF 2021, el cruce completo (ola de desarrollo) ──────────────
    inf21 = list(par["codigos_informal_2021"])
    f9_21 = list(par["codigos_formal_D9_2021"])
    f7_21 = list(par["codigos_formal_D7_2021"])
    cols21 = inf21 + f9_21 + ["TLOC", "EDAD", "FAC_ELE", "EST_DIS", "UPM_DIS"]
    df21, _m21, _e21 = _lee_miembro(
        inputs["enif2021_csv"]["ruta_absoluta"],
        "conjunto_de_datos_tmodulo_enif_2021.csv", cols21)
    uni21 = _universo(df21, "EDAD", "TLOC", "FAC_ELE", inf21 + f9_21)
    u21 = uni21["u"]
    out[f"{P}-G-C1-FILAS-ARCHIVO"] = uni21["n_archivo"]
    out[f"{P}-G-C1-FILAS-UNIVERSO"] = uni21["n_universo"]
    out[f"{P}-G-C1-FILAS-EDAD-CENTINELA"] = uni21["n_centinela"]
    out[f"{P}-G-C1-COBERTURA-SIN-PONDERAR"] = uni21["cobertura_sin_ponderar"]
    out[f"{P}-G-C1-COBERTURA-PONDERADA"] = uni21["cobertura_ponderada"]
    out[f"{P}-G-C1-FILAS-CODIGO-FUERA-DE-DOMINIO"] = uni21["filas_fuera_de_dominio"]

    des21 = _desenlaces(u21, inf21, f9_21, f7_21)
    tloc21 = u21["TLOC"].str.strip().to_numpy()
    edad21 = u21["_edad"].to_numpy()
    tramos = par["edad_tramos"]
    loc_mask = {"L1": np.isin(tloc21, par["localidad_L1_tloc"]),
                "L2": np.isin(tloc21, par["localidad_L2_tloc"])}
    edad_mask = {e: (edad21 >= tramos[e][0]) & (edad21 <= tramos[e][1])
                 for e in ("E1", "E2", "E3", "E4")}
    grupos21 = [(c, loc_mask[c.split("x")[0]] & edad_mask[c.split("x")[1]])
                for c in CELDAS]
    grupos21.append(("NACIONAL", np.ones(len(u21), dtype=bool)))
    desen21 = [("D9", des21["D9"]), ("D7", des21["D7"])]

    est21 = u21["EST_DIS"].str.strip().to_numpy()
    upm21 = u21["UPM_DIS"].str.strip().to_numpy()
    claves21 = np.array([f"{e}\t{u}" for e, u in zip(est21, upm21)])
    counts21, unicas21, n_upm21, upm_unica21 = _replicas(est21, upm21, semilla, n_rep)
    out[f"{P}-G-C1-ESTRATOS"] = int(len(set(est21)))
    out[f"{P}-G-C1-UPM"] = int(n_upm21)
    out[f"{P}-G-C1-ESTRATOS-UPM-UNICA"] = int(upm_unica21)

    m21 = _matriz(grupos21, desen21)
    W21, Y21 = _agrega_por_upm(claves21, unicas21, u21["_w"].to_numpy(), m21)
    pt21, lo21, hi21, _r21 = _punto_e_ic(counts21, W21, Y21)

    monotonia = "VERIFICADA"
    fuera_soporte = 0
    for g, c in enumerate(CELDAS):
        n_c = int(grupos21[g][1].sum())
        out[f"{P}-C1-D9-N-{c}"] = n_c
        soporte = "SOPORTE-OK" if n_c >= umbral_n else "FUERA-DE-SOPORTE"
        if n_c < umbral_n:
            fuera_soporte += 1
        out[f"{P}-C1-SOPORTE-{c}"] = soporte
        for d, etq in ((0, "D9"), (1, "D7")):
            v, a, b = pt21[g, d], lo21[g, d], hi21[g, d]
            ok = n_c > 0 and np.isfinite(v)
            out[f"{P}-C1-{etq}-P-{c}"] = float(v) if ok else None
            out[f"{P}-C1-{etq}-IC95INF-{c}"] = float(a) if ok and np.isfinite(a) else None
            out[f"{P}-C1-{etq}-IC95SUP-{c}"] = float(b) if ok and np.isfinite(b) else None
        if np.isfinite(pt21[g, 0]) and np.isfinite(pt21[g, 1]) \
                and pt21[g, 1] + 1e-12 < pt21[g, 0]:
            monotonia = "VIOLADA"
    out[f"{P}-G-C1-MONOTONIA-D9-SUBSET-D7"] = monotonia
    out[f"{P}-G-C1-CELDAS-FUERA-DE-SOPORTE"] = fuera_soporte
    gn = len(CELDAS)
    out[f"{P}-G-C1-P-NACIONAL-D9"] = float(pt21[gn, 0])
    out[f"{P}-G-C1-P-NACIONAL-D7"] = float(pt21[gn, 1])

    # ── ENIF 2024 · SÓLO marginales de un eje ──────────────────────────────
    inf24 = list(par["codigos_informal_2024"])
    f9_24 = list(par["codigos_formal_D9_2024"])
    cols24 = inf24 + f9_24 + ["tloc", "edad_v", "fac_per", "est_dis", "upm_dis"]
    df24, _m24, _e24 = _lee_miembro(
        inputs["enif2024_csv"]["ruta_absoluta"],
        "conjunto_de_datos_tmodulo_enif2024.csv", cols24)
    uni24 = _universo(df24, "edad_v", "tloc", "fac_per", inf24 + f9_24)
    u24 = uni24["u"]
    out[f"{P}-G-M24-FILAS-ARCHIVO"] = uni24["n_archivo"]
    out[f"{P}-G-M24-FILAS-UNIVERSO"] = uni24["n_universo"]
    out[f"{P}-G-M24-FILAS-EDAD-CENTINELA"] = uni24["n_centinela"]
    out[f"{P}-G-M24-COBERTURA-SIN-PONDERAR"] = uni24["cobertura_sin_ponderar"]
    out[f"{P}-G-M24-COBERTURA-PONDERADA"] = uni24["cobertura_ponderada"]
    out[f"{P}-G-M24-FILAS-CODIGO-FUERA-DE-DOMINIO"] = uni24["filas_fuera_de_dominio"]

    des24 = _desenlaces(u24, inf24, f9_24, f9_24)     # sólo D9 se usa en 2024
    tloc24 = u24["tloc"].str.strip().to_numpy()
    edad24 = u24["_edad"].to_numpy()
    # GUARDIA: cada agrupación declara SUS ejes. Una sola entrada por grupo.
    agrup = [("L1", ["localidad"], np.isin(tloc24, par["localidad_L1_tloc"])),
             ("L2", ["localidad"], np.isin(tloc24, par["localidad_L2_tloc"])),
             ("E1", ["edad"], (edad24 >= 18) & (edad24 <= 29)),
             ("E2", ["edad"], (edad24 >= 30) & (edad24 <= 44)),
             ("E3", ["edad"], (edad24 >= 45) & (edad24 <= 59)),
             ("E4", ["edad"], (edad24 >= 60) & (edad24 <= 97)),
             ("NAC", [], np.ones(len(u24), dtype=bool))]
    for _n, ejes, _m in agrup:
        _GUARDIA.registra_agrupacion_2024(ejes)
    grupos24 = [(n, m) for n, _e, m in agrup]
    desen24 = [("D9", des24["D9"])]

    est24 = u24["est_dis"].str.strip().to_numpy()
    upm24 = u24["upm_dis"].str.strip().to_numpy()
    claves24 = np.array([f"{e}\t{u}" for e, u in zip(est24, upm24)])
    counts24, unicas24, n_upm24, _uu24 = _replicas(est24, upm24, semilla, n_rep)
    out[f"{P}-G-M24-ESTRATOS"] = int(len(set(est24)))
    out[f"{P}-G-M24-UPM"] = int(n_upm24)

    m24 = _matriz(grupos24, desen24)
    W24, Y24 = _agrega_por_upm(claves24, unicas24, u24["_w"].to_numpy(), m24)
    pt24, lo24, hi24, reps24 = _punto_e_ic(counts24, W24, Y24)

    sellados = par["marginales_sellados_D9"]
    nombres24 = [n for n, _m in grupos24]
    deltas = {}
    for g, nom in enumerate(nombres24):
        out[f"{P}-G-C2-MARG-{nom}-D9-N"] = int(grupos24[g][1].sum())
        out[f"{P}-G-C2-MARG-{nom}-D9-P"] = float(pt24[g, 0])
        out[f"{P}-G-C2-MARG-{nom}-D9-IC95INF"] = float(lo24[g, 0])
        out[f"{P}-G-C2-MARG-{nom}-D9-IC95SUP"] = float(hi24[g, 0])
        d = float(pt24[g, 0]) - float(sellados[nom]["p"])
        deltas[nom] = d
        out[f"{P}-G-CTRL-ARBITRO-{nom}-DELTA"] = d
    con_ic = [n for n in nombres24 if n != "NAC"]
    delta_max = max(abs(deltas[n]) for n in con_ic)
    out[f"{P}-G-CTRL-ARBITRO-DELTA-MAX"] = float(delta_max)
    out[f"{P}-G-CTRL-ARBITRO-VEREDICTO"] = (
        "REPRODUCE" if delta_max <= float(par["control_arbitro_umbral"])
        else "NO-REPRODUCE")

    # ── C2 · piso log-aditivo ──────────────────────────────────────────────
    ix = {n: g for g, n in enumerate(nombres24)}

    def _marg(p):
        return {"desenlace_id": DESENLACE_D9, "p": float(p)}

    no_construibles, mult_fuera, mult_max = 0, 0, float("-inf")
    rep_sin_definir = 0
    for c in CELDAS:
        l, e = c.split("x")
        p_l_s, p_e_s = sellados[l]["p"], sellados[e]["p"]
        p_s = sellados["NAC"]["p"]
        try:
            punto = piso_log_aditivo(_marg(p_l_s), _marg(p_e_s), _marg(p_s))["p"]
        except MarginalDegenerado:
            punto = None
            no_construibles += 1
        out[f"{P}-C2-P-{c}"] = float(punto) if punto is not None else None

        mult = p_l_s * p_e_s / p_s
        mult_max = max(mult_max, mult)
        if not (0.0 <= mult <= 1.0):
            mult_fuera += 1

        try:
            pr = piso_log_aditivo(_marg(pt24[ix[l], 0]), _marg(pt24[ix[e], 0]),
                                  _marg(pt24[ix["NAC"], 0]))["p"]
            out[f"{P}-C2-P-REDERIVADO-{c}"] = float(pr)
        except MarginalDegenerado:
            out[f"{P}-C2-P-REDERIVADO-{c}"] = None

        vals = []
        rl, re_, rn = reps24[:, ix[l], 0], reps24[:, ix[e], 0], reps24[:, ix["NAC"], 0]
        for a, b, d in zip(rl, re_, rn):
            if not (0.0 < a < 1.0 and 0.0 < b < 1.0 and 0.0 < d < 1.0) \
                    or not (np.isfinite(a) and np.isfinite(b) and np.isfinite(d)):
                rep_sin_definir += 1
                continue
            vals.append(piso_log_aditivo(_marg(a), _marg(b), _marg(d))["p"])
        if vals:
            out[f"{P}-C2-IC95INF-{c}"] = float(np.percentile(vals, 2.5))
            out[f"{P}-C2-IC95SUP-{c}"] = float(np.percentile(vals, 97.5))
        else:
            out[f"{P}-C2-IC95INF-{c}"] = None
            out[f"{P}-C2-IC95SUP-{c}"] = None

    out[f"{P}-G-C2-DESENLACE-ID"] = DESENLACE_D9
    out[f"{P}-G-C2-ROTULO-SUPUESTO"] = ROTULO_SUPUESTO
    out[f"{P}-G-C2-INCERTIDUMBRE"] = (
        "IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS")
    out[f"{P}-G-C2-ESTADO"] = ("PISO-ADMISIBLE" if no_construibles == 0
                               else "DIAGNOSTICO-POR-REPLIEGUE")
    out[f"{P}-G-C2-CELDAS-NO-CONSTRUIBLES"] = no_construibles
    out[f"{P}-G-C2-REPLICAS-SIN-DEFINIR"] = rep_sin_definir
    out[f"{P}-G-C2-MULT-FUERA-DE-RANGO"] = mult_fuera
    out[f"{P}-G-C2-MULT-MAX"] = float(mult_max)
    out[f"{P}-G-C2-CRUCE-2024-DERIVADO"] = _GUARDIA.cruce_2024

    # ── C3 · lectura de las capturas congeladas ────────────────────────────
    sufijo = par["c3_spec_sufijo_vigente"]
    capturas, extraibles, rechazos, modelos = 0, 0, 0, set()
    por_celda = {c: [] for c in CELDAS}
    for ruta in sorted(CORRIDAS_L.glob(f"CD-DIN-*__L-solo__*__{sufijo}.json")):
        d = json.loads(ruta.read_text(encoding="utf-8"))
        capturas += 1
        if d.get("estado_captura") != "OK":
            rechazos += 1
            continue
        modelos.add(str(d.get("modelo_real")))
        ex = extraer_valor(d.get("texto_crudo") or "")
        if ex.estado == "EXTRAIBLE" and ex.valor is not None and 0.0 <= ex.valor <= 1.0:
            extraibles += 1
            por_celda[d["celda_cruce"]].append(float(ex.valor))
    for c in CELDAS:
        v = sorted(por_celda[c])
        out[f"{P}-C3-LSOLO-K-EXTRAIBLES-{c}"] = len(v)
        out[f"{P}-C3-LSOLO-P-{c}"] = float(statistics.median(v)) if v else None
        out[f"{P}-C3-LSOLO-MIN-{c}"] = float(v[0]) if v else None
        out[f"{P}-C3-LSOLO-MAX-{c}"] = float(v[-1]) if v else None
        out[f"{P}-C3-LCORPUS-P-{c}"] = None
    out[f"{P}-G-C3-CONTROL-MEMORIA"] = "NO-PUBLICADO-EN-LO-ALCANZADO"
    out[f"{P}-G-C3-LSOLO-ESTADO"] = "EJECUTADA" if capturas else "NO-EJECUTADA"
    out[f"{P}-G-C3-LSOLO-SPEC"] = sufijo
    out[f"{P}-G-C3-LSOLO-CAPTURAS"] = capturas
    out[f"{P}-G-C3-LSOLO-EXTRAIBLES"] = extraibles
    out[f"{P}-G-C3-LSOLO-RECHAZOS"] = rechazos
    out[f"{P}-G-C3-LSOLO-MODELO-REAL"] = (
        "NO-REPORTADO-POR-EL-CLIENTE (FP-239)"
        if modelos <= {"None"} else " | ".join(sorted(modelos - {"None"})))
    out[f"{P}-G-C3-CAPTURAS-SUPERADAS"] = len(list(
        CORRIDAS_L.glob(f"CD-DIN-*__L-solo__*__{par['c3_spec_sufijo_superado']}.json")))
    out[f"{P}-G-C3-LCORPUS-ESTADO"] = (
        "DIFERIDO-A-SUCESOR -- costo y tiempo (FP-379·ENMIENDA); en perimetro y "
        "en la spec; ademas paquete-corpus-F5-v1_0/manifiesto.json no tiene "
        "entrada para ninguna de las 8 celdas")
    out[f"{P}-G-C3-LCORPUS-CAPTURAS"] = len(list(
        CORRIDAS_L.glob("CD-DIN-*__L+corpus__*.json")))

    # ── C4 · INEJECUTABLE · C5 · NO-APLICA · falsador ──────────────────────
    out[f"{P}-G-C4-ESTADO"] = (
        "INEJECUTABLE -- la matriz B*theta(x) -> h_r no puede emitir: cuatro "
        "faltantes con nombre. Bajo ADR-531 compite si puede; no puede.")
    out[f"{P}-G-C4-FALTANTES"] = " | ".join(par["c4_faltantes"])
    out[f"{P}-G-C5-ESTADO"] = (
        "NO-APLICA -- el emisor es el arbitro con otro nombre; " + par["c5_cita"])

    # Falsador: ningun R del cruce puede existir en el arbol al sellar.
    patrones = ["CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001"]
    existe = any((RAIZ / "data" / "corrida0" / p_).exists() for p_ in patrones)
    out[f"{P}-G-R-EXISTE-AL-CERRAR"] = "SI" if existe else "NO"
    return out
