"""PDR1 · pieza ENSU2024 · ACTO GEN2-PISOS-DOMINIOS-Y-REGLAS-1.

Afirmación ASTRA5-U0-SANC-007 (dominio SANCION_SOCIAL): proporción de personas
18+ de las ciudades ENSU que, por temor al delito, cambiaron sus hábitos respecto
a llevar cosas de valor (joyas, dinero, tarjetas), ENSU 2024 primer trimestre
(marzo 2024, tabla CB `ENSU_CB_0324.csv`). Spec humana:
forense/prereg-caja/PDR1-ENSU2024-spec-v1_0.md (congelada en COMMIT-1).

Sólo lee el miembro `ensu_bd_marzo_2024_csv.zip!ENSU_CB_0324.csv`; cualquier otro
trimestre de 2024 del payload no se abre (guardia). Autocontenido (numpy, pandas).

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}.
"""
from __future__ import annotations

import io
import math
import re
import zipfile

import numpy as np
import pandas as pd

PAYLOAD_ID = "ensu2024_bd_csv_zip"
MIEMBRO_EXTERNO = "ensu_bd_marzo_2024_csv.zip"
MIEMBRO_CB = "ensu_cb_0324.csv"
REACTIVO = "BP1_5_1"
COLUMNAS = ["CD", "EST_DIS", "UPM_DIS", "FAC_SEL", "SEXO", "EDAD", REACTIVO]
PREF = "RESULT-PDR1-ENSU2024-SANC007"
EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 96))
CELDAS = ([("TOTAL", "TODOS")] + [("SEXO", s) for s in ("HOMBRE", "MUJER")]
          + [("EDAD", e) for e, _, _ in EDADES])
# Estimandos (spec §3): (sufijo, códigos «sí», códigos del denominador, con IC y segmentos)
ESTIMANDOS = (
    ("PRINCIPAL", (1,), (1, 2), True),        # sí / (sí + no): NA y NS/NR fuera
    ("CON-NSNR", (1,), (1, 2, 9), False),      # sí / (sí + no + NS/NR): NA fuera
    ("ORO", (1,), (1, 2, 3, 9), False),        # universo de CALC-ENSU-PISOS-0001
)
Q = ("P", "IC-LO", "IC-HI", "N")


class ParoDeGuardia(RuntimeError):
    pass


# ─────────────────────────── lectura ───────────────────────────

def lee_csv(b: bytes) -> pd.DataFrame:
    for enc in ("utf-8-sig", "latin-1"):
        try:
            t = b.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    t = t.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(t), dtype=str, keep_default_na=False)
    df.columns = [c.strip().strip('"').lstrip("﻿").upper() for c in df.columns]
    faltan = [c for c in COLUMNAS if c not in df.columns]
    if faltan:
        raise ParoDeGuardia(f"columnas ausentes en {MIEMBRO_CB}: {faltan}")
    return df[COLUMNAS].apply(lambda s: s.str.strip())


def cb_de_payload(zbytes: bytes) -> pd.DataFrame:
    z = zipfile.ZipFile(io.BytesIO(zbytes))
    ext = [n for n in z.namelist() if n.rsplit("/", 1)[-1].lower() == MIEMBRO_EXTERNO]
    if len(ext) != 1:
        raise ParoDeGuardia(f"{MIEMBRO_EXTERNO}: coincidencias={len(ext)}")
    zi = zipfile.ZipFile(io.BytesIO(z.read(ext[0])))
    cb = [n for n in zi.namelist() if n.rsplit("/", 1)[-1].lower() == MIEMBRO_CB]
    if len(cb) != 1:
        raise ParoDeGuardia(f"{MIEMBRO_CB}: coincidencias={len(cb)}")
    return lee_csv(zi.read(cb[0]))


def num(s: pd.Series) -> np.ndarray:
    return pd.to_numeric(s.where(s.str.fullmatch(r"-?\d+(\.\d+)?"), None), errors="coerce").to_numpy(dtype=float)


def marco(df: pd.DataFrame):
    w = num(df["FAC_SEL"])
    est_raw = df["EST_DIS"].astype(str).str.strip()
    upm_raw = df["UPM_DIS"].astype(str).str.strip()
    ok = np.isfinite(w) & (w > 0) & est_raw.ne("").to_numpy() & upm_raw.ne("").to_numpy()
    cd = df["CD"].astype(str).str.strip().str.lstrip("0").replace("", "0").str.zfill(2)
    est = (cd + "-" + est_raw).to_numpy()
    upm = (cd + "-" + est_raw + "|" + upm_raw).to_numpy()
    sexo = num(df["SEXO"])
    edad = num(df["EDAD"])
    v = num(df[REACTIVO])
    f = pd.DataFrame({"w": w, "est": est, "upm": upm, "v": v, "sexo": sexo, "edad": edad})
    return f[ok].reset_index(drop=True), int(len(df)), int(ok.sum())


def mascara(f, eje, cat):
    if eje == "TOTAL":
        return np.ones(len(f), dtype=bool)
    if eje == "SEXO":
        return (f["sexo"] == {"HOMBRE": 1, "MUJER": 2}[cat]).to_numpy()
    lo, hi = next((a, b) for e, a, b in EDADES if e == cat)
    e = f["edad"].to_numpy()
    return (e >= lo) & (e <= hi)


# ─────────────────────────── bootstrap ───────────────────────────

def bootstrap(f, nums, dens, replicas, semilla):
    """nums/dens: listas de arrays por persona (Σ por celda). Remuestrea UPM con
    reposición dentro de estrato (n_h de n_h); estrato con una UPM: se remuestrea a
    sí misma (varianza cero). Devuelve matriz R×M de razones."""
    upm_ids, inv = np.unique(f["upm"].to_numpy(), return_inverse=True)
    U = len(upm_ids)
    Nu = np.stack([np.bincount(inv, weights=x, minlength=U) for x in nums], axis=1)
    Du = np.stack([np.bincount(inv, weights=x, minlength=U) for x in dens], axis=1)
    est_de_upm = pd.Series(f["est"].to_numpy()).groupby(inv).first().reindex(range(U)).to_numpy()
    rng = np.random.Generator(np.random.PCG64(semilla))
    peso = np.zeros((replicas, U))
    for e in sorted(set(est_de_upm)):
        idx = np.flatnonzero(est_de_upm == e)
        n = len(idx)
        peso[:, idx] = rng.multinomial(n, np.full(n, 1.0 / n), size=replicas)
    Rn = peso @ Nu
    Rd = peso @ Du
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(Rd > 0, Rn / Rd, np.nan), U, len(set(est_de_upm)), int(
            sum(1 for e in set(est_de_upm) if (est_de_upm == e).sum() == 1))


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def dictamen(p, lo, hi, cifra, umbral):
    """B-bis (spec §5): CONFIRMA si la cifra cae en el IC95; MATIZA si fuera pero a
    ≤ umbral del punto; ROMPE si fuera a > umbral. Sin punto o IC: NO-CONSTRUIBLE."""
    if p is None or lo is None or hi is None:
        return "NO-CONSTRUIBLE"
    if lo <= cifra <= hi:
        return "CONFIRMA"
    return "MATIZA" if abs(p - cifra) <= umbral else "ROMPE"


def mide(df, replicas, semilla, cifra, umbral):
    f, n_filas, n_diseno = marco(df)
    v = f["v"].to_numpy()
    w = f["w"].to_numpy()
    out = {f"{PREF}-G-FILAS-CB": n_filas, f"{PREF}-G-PERSONAS-DISENO-VALIDO": n_diseno}
    # composición del universo completo (códigos 1,2,3,9) — descriptivo
    den_all = np.isin(v, (1, 2, 3, 9))
    wt = float(w[den_all].sum())
    for cod, nom in ((3, "NO-APLICA"), (9, "NSNR"), (None, "FUERA-DE-CODIGOS")):
        if cod is None:
            m = ~den_all
            out[f"{PREF}-G-N-{nom}"] = int(m.sum())
            continue
        m = v == cod
        out[f"{PREF}-G-P-{nom}"] = _fin(w[m].sum() / wt) if wt > 0 else None
        out[f"{PREF}-G-N-{nom}"] = int(m.sum())
    nums, dens, llaves = [], [], []
    for suf, si, univ, con_seg in ESTIMANDOS:
        celdas = CELDAS if con_seg else [("TOTAL", "TODOS")]
        u = np.isin(v, univ)
        y = np.isin(v, si)
        for eje, cat in celdas:
            m = mascara(f, eje, cat) & u
            nums.append(np.where(m & y, w, 0.0))
            dens.append(np.where(m, w, 0.0))
            llaves.append((suf, eje, cat, int(m.sum())))
    reps, n_upm, n_est, n_single = bootstrap(f, nums, dens, replicas, semilla)
    out[f"{PREF}-G-N-UPM"] = n_upm
    out[f"{PREF}-G-N-ESTRATOS"] = n_est
    out[f"{PREF}-G-N-ESTRATOS-SINGLETON"] = n_single
    for j, (suf, eje, cat, n) in enumerate(llaves):
        d = dens[j].sum()
        p = _fin(nums[j].sum() / d) if d > 0 else None
        col = reps[:, j]
        col = col[np.isfinite(col)]
        lo = hi = None
        if p is not None and len(col) == replicas:
            lo, hi = _fin(np.percentile(col, 2.5)), _fin(np.percentile(col, 97.5))
        base = f"{PREF}-{suf}-{eje}-{cat}"
        out[f"{base}-P"], out[f"{base}-IC-LO"], out[f"{base}-IC-HI"], out[f"{base}-N"] = p, lo, hi, n
    for suf, _, _, _ in ESTIMANDOS:
        b = f"{PREF}-{suf}-TOTAL-TODOS"
        out[f"{PREF}-{suf}-DICTAMEN"] = dictamen(out[f"{b}-P"], out[f"{b}-IC-LO"], out[f"{b}-IC-HI"], cifra, umbral)
    out[f"{PREF}-DICTAMEN"] = out[f"{PREF}-PRINCIPAL-DICTAMEN"]
    return out


def medir(inputs, contrato):
    p = contrato["parametros"]
    ruta = str(inputs[PAYLOAD_ID]["ruta_absoluta"])
    if re.search(r"(^|/)(2025|2026)(/|$)", ruta) or "2025" in ruta.rsplit("/", 1)[-1] or "2026" in ruta.rsplit("/", 1)[-1]:
        raise ParoDeGuardia(f"payload resuelve a una ola fuera de 2024: {ruta}")
    with open(ruta, "rb") as fh:
        df = cb_de_payload(fh.read())
    out = mide(df, int(p["bootstrap_replicas"]), int(contrato["seed"]["valor"]),
               float(p["cifra_afirmacion"]), float(p["umbral_matiza"]))
    out[f"{PREF}-G-BOOTSTRAP-REPLICAS"] = int(p["bootstrap_replicas"])
    out[f"{PREF}-G-SEED"] = int(contrato["seed"]["valor"])
    out[f"{PREF}-G-MIEMBRO"] = f"{MIEMBRO_EXTERNO}!{MIEMBRO_CB.upper()}"
    return out


# ─────────────────────────── esquema ───────────────────────────

def esquema_resultados():
    fl = []

    def fila(i, tipo, unidad, nulo=False):
        d = {"id": i, "tipo": tipo, "unidad": unidad}
        if nulo:
            d["permite_no_estimable"] = True
        fl.append(d)

    fila(f"{PREF}-G-FILAS-CB", "entero", "filas de ENSU_CB_0324")
    fila(f"{PREF}-G-PERSONAS-DISENO-VALIDO", "entero", "personas con FAC_SEL>0, EST_DIS y UPM_DIS")
    for nom in ("NO-APLICA", "NSNR"):
        fila(f"{PREF}-G-P-{nom}", "proporcion", "proporción ponderada del código sobre 1,2,3,9", True)
        fila(f"{PREF}-G-N-{nom}", "entero", "personas sin ponderar")
    fila(f"{PREF}-G-N-FUERA-DE-CODIGOS", "entero", "personas con código fuera de 1,2,3,9 o blanco")
    fila(f"{PREF}-G-N-UPM", "entero", "UPM de diseño (CD+EST_DIS+UPM_DIS)")
    fila(f"{PREF}-G-N-ESTRATOS", "entero", "estratos (CD+EST_DIS)")
    fila(f"{PREF}-G-N-ESTRATOS-SINGLETON", "entero", "estratos con una UPM")
    for suf, _, _, con_seg in ESTIMANDOS:
        for eje, cat in (CELDAS if con_seg else [("TOTAL", "TODOS")]):
            b = f"{PREF}-{suf}-{eje}-{cat}"
            fila(f"{b}-P", "proporcion", "proporción ponderada de personas 18+", True)
            fila(f"{b}-IC-LO", "proporcion", "IC95 bootstrap de diseño, inferior", True)
            fila(f"{b}-IC-HI", "proporcion", "IC95 bootstrap de diseño, superior", True)
            fila(f"{b}-N", "entero", "personas sin ponderar en el denominador")
        fila(f"{PREF}-{suf}-DICTAMEN", "texto", "CONFIRMA/MATIZA/ROMPE/NO-CONSTRUIBLE (B-bis spec §5)")
    fila(f"{PREF}-DICTAMEN", "texto", "dictamen que manda (PRINCIPAL)")
    fila(f"{PREF}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas")
    fila(f"{PREF}-G-SEED", "entero", "semilla")
    fila(f"{PREF}-G-MIEMBRO", "texto", "miembro leído")
    return fl
