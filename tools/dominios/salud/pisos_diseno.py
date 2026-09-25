#!/usr/bin/env python3
"""Receta común de pisos por segmento con IC de diseño · ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1.

La consumen los tres medidores del acto (CALC-ENSANUT-PISOS-SALUD-0001,
CALC-ENCODAT-PISOS-SUSTANCIAS-0001, CALC-ENBIARE-PISOS-BIENESTAR-0001) como input
`origen: repo` fijado por sha256 y ejecutado desde sus bytes: ningún medidor la
importa por ruta viva.

QUÉ HACE, y nada más:
  · lee un .dta dentro de un ZIP (o un CSV dentro de un ZIP) con las columnas pedidas;
  · estima razones ponderadas Σw·y / Σw por máscara (proporción si y ∈ {0,1};
    media si y es una escala);
  · bootstrap de conglomerados: UPM con reposición dentro de estrato, UPM única del
    estrato = de certeza (multiplicidad 1 en toda réplica), PCG64(semilla), bloques de
    50 réplicas — el mismo contrato que la receta ENCIG (`tools/encig_cruces_historicos.py`
    `_bootstrap`/`_summary`), reescrito aquí porque aquella fija nombres de columna ENCIG;
  · resumen conservador: si alguna réplica degenera, no se publica EE ni IC;
  · IC calibrado de persistencia (método de CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001,
    spec §4): τ²_g = media de Δ² en logit sin centrar ni restar ruido; IC =
    expit(logit p ± z·√(ee_m² + τ²_g)).

No elige reactivos, no recodifica, no decide universos: eso vive en cada medidor y en
su spec humana.
"""
from __future__ import annotations

import io
import math
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

Z95 = 1.959964


# ═══════════════════════════ lectura ═══════════════════════════

def miembro_unico(ruta_zip, sufijo):
    """Nombre del único miembro del ZIP que termina en `sufijo` (sin distinguir mayúsculas)."""
    with zipfile.ZipFile(ruta_zip) as z:
        cand = [n for n in z.namelist() if n.lower().endswith(sufijo.lower()) and not n.startswith("__MACOSX")]
    if len(cand) != 1:
        raise ValueError(f"{Path(ruta_zip).name}: se esperaba 1 miembro *{sufijo}, hay {len(cand)}: {cand}")
    return cand[0]


def lee_dta(ruta_zip, columnas, miembro=None, encoding=None):
    """Lee `columnas` (nombres exactos, sin distinguir mayúsculas) del .dta del ZIP.

    Devuelve un DataFrame con las columnas en MINÚSCULAS. Una columna pedida que no
    existe levanta KeyError con su nombre: el medidor la convierte en NO-ESTIMABLE.
    """
    import pyreadstat

    miembro = miembro or miembro_unico(ruta_zip, ".dta")
    with zipfile.ZipFile(ruta_zip) as z, tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "m.dta"
        destino.write_bytes(z.read(miembro))
        kw = {"encoding": encoding} if encoding else {}
        _, meta = pyreadstat.read_dta(str(destino), metadataonly=True, **kw)
        reales = {c.lower(): c for c in meta.column_names}
        faltan = [c for c in columnas if c.lower() not in reales]
        if faltan:
            raise KeyError(f"columnas ausentes en {miembro}: {faltan}")
        df, _ = pyreadstat.read_dta(str(destino), usecols=[reales[c.lower()] for c in columnas],
                                    apply_value_formats=False, **kw)
    df.columns = [c.lower() for c in df.columns]
    return df


def lee_csv_zip(ruta_zip, columnas, miembro=None, encoding="utf-8"):
    miembro = miembro or miembro_unico(ruta_zip, ".csv")
    with zipfile.ZipFile(ruta_zip) as z:
        raw = z.read(miembro)
    try:
        texto = raw.decode(encoding)
    except UnicodeDecodeError:
        texto = raw.decode("latin-1")
    cab = pd.read_csv(io.StringIO(texto), nrows=0)
    reales = {c.strip().lower(): c for c in cab.columns}
    faltan = [c for c in columnas if c.lower() not in reales]
    if faltan:
        raise KeyError(f"columnas ausentes en {miembro}: {faltan}")
    df = pd.read_csv(io.StringIO(texto), usecols=[reales[c.lower()] for c in columnas],
                     dtype=str, keep_default_na=False)
    df.columns = [c.strip().lower() for c in df.columns]
    return df


def num(serie):
    """Numérico; blanco, 'NA' y no numérico → NaN (cero nunca sustituye falta de dato)."""
    return pd.to_numeric(serie.astype(str).str.strip().replace({"": None, "NA": None}), errors="coerce")


# ═══════════════════════════ estimación ═══════════════════════════

def _razon(num_, den_):
    with np.errstate(divide="ignore", invalid="ignore"):
        r = num_ / den_
    return np.where(den_ > 0, r, np.nan)


def matriz_por_upm(frame, y, w, estrato, upm, mascaras):
    """Sumas Σw·y y Σw por (estrato, UPM) y máscara. `mascaras`: lista de arrays bool."""
    clave = frame[estrato].astype(str).str.strip() + "\t" + frame[upm].astype(str).str.strip()
    codigos, llaves = pd.factorize(clave, sort=True)
    k = len(llaves)
    yv = np.asarray(y, dtype=float)
    wv = np.asarray(w, dtype=float)
    nume = np.zeros((k, len(mascaras)))
    deno = np.zeros((k, len(mascaras)))
    for j, m in enumerate(mascaras):
        m = np.asarray(m, dtype=bool)
        nume[:, j] = np.bincount(codigos[m], weights=(wv * yv)[m], minlength=k)
        deno[:, j] = np.bincount(codigos[m], weights=wv[m], minlength=k)
    return list(llaves), nume, deno


def bootstrap(frame, y, w, estrato, upm, mascaras, replicas, semilla):
    """(puntos, réplicas[R×M], n_sin_ponderar[M]) — contrato de la receta ENCIG."""
    llaves, nume, deno = matriz_por_upm(frame, y, w, estrato, upm, mascaras)
    estratos = {}
    for pos, llave in enumerate(llaves):
        estratos.setdefault(llave.split("\t", 1)[0], []).append(pos)
    puntos = _razon(nume.sum(axis=0), deno.sum(axis=0))
    out = np.full((replicas, len(mascaras)), np.nan)
    rng = np.random.Generator(np.random.PCG64(semilla))
    for ini in range(0, replicas, 50):
        t = min(50, replicas - ini)
        mult = np.zeros((t, len(llaves)))
        for e in sorted(estratos):
            idx = np.asarray(estratos[e], dtype=int)
            if len(idx) == 1:
                mult[:, idx[0]] = 1.0  # UPM de certeza
                continue
            sorteo = rng.integers(0, len(idx), size=(t, len(idx)))
            filas = np.repeat(np.arange(t), len(idx))
            np.add.at(mult, (filas, idx[sorteo.ravel()]), 1.0)
        out[ini:ini + t] = _razon(mult @ nume, mult @ deno)
    n = np.array([int(np.asarray(m, dtype=bool).sum()) for m in mascaras])
    return puntos, out, n


def resumen(punto, reps):
    """(ee, ic_lo, ic_hi, validas). Contrato conservador: réplica degenerada → sin IC."""
    reps = np.asarray(reps, dtype=float)
    validas = int(np.isfinite(reps).sum())
    if not np.isfinite(punto) or validas != len(reps):
        return None, None, None, validas
    lo, hi = np.percentile(reps, [2.5, 97.5])
    return float(np.std(reps, ddof=1)), float(lo), float(hi), validas


# ═══════════════════════════ persistencia ═══════════════════════════

def logit(p):
    return math.log(p / (1.0 - p))


def expit(z):
    return 1.0 / (1.0 + math.exp(-z))


def abierto(p):
    return p is not None and isinstance(p, (int, float)) and math.isfinite(p) and 0.0 < p < 1.0


def tau2(deltas):
    """Media de Δ² sin centrar (spec ENIF-PERSISTENCIA §4). None si no hay Δ definido."""
    d = [x for x in deltas if x is not None and math.isfinite(x)]
    return (sum(x * x for x in d) / len(d)) if d else None


def ee_logit(lo, hi):
    if not (abierto(lo) and abierto(hi)):
        return None
    return (logit(hi) - logit(lo)) / (2.0 * Z95)


def ic_calibrado(p, lo, hi, t2):
    """expit(logit p ± z·√(ee_m² + τ²)); None si p o su IC no están en (0,1) o τ² es None."""
    em = ee_logit(lo, hi)
    if not abierto(p) or em is None or t2 is None:
        return None, None
    s = math.sqrt(em * em + t2)
    c = logit(p)
    return expit(c - Z95 * s), expit(c + Z95 * s)


def wilson(k, n, z=Z95):
    if n <= 0:
        return None, None
    ph = k / n
    den = 1 + z * z / n
    cen = (ph + z * z / (2 * n)) / den
    mar = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / den
    return cen - mar, cen + mar


# ═══════════════════════════ motor de marginales ═══════════════════════════

def marginales(frame, conductas, ejes, w, estrato, upm, replicas, semilla):
    """Pisos por UN eje a la vez (nunca cruces) para varias conductas.

    `conductas`: {nombre: serie float (0/1 o escala; NaN = fuera del universo o sin dato)}.
    `ejes`: {eje: (serie de categoría como texto, tupla de categorías)}; el eje "TOTAL" no se
    pasa: se añade siempre. Una sola corrida de bootstrap por marco: todas las máscaras
    comparten réplicas (UPM del marco entero).
    Devuelve {(conducta, eje, cat): {"p", "ee", "lo", "hi", "n", "validas"}}.
    """
    claves, mascaras, ys = [], [], []
    for nom, y in conductas.items():
        y = np.asarray(y, dtype=float)
        base = np.isfinite(y)
        claves.append((nom, "TOTAL", "TODOS"))
        mascaras.append(base)
        ys.append(nom)
        for eje, (serie, cats) in ejes.items():
            s = np.asarray(serie, dtype=object)
            for c in cats:
                claves.append((nom, eje, c))
                mascaras.append(base & (s == c))
                ys.append(nom)
    out = {}
    for nom, y in conductas.items():
        idx = [i for i, k in enumerate(ys) if k == nom]
        yv = np.nan_to_num(np.asarray(y, dtype=float), nan=0.0)
        pts, reps, n = bootstrap(frame, yv, w, estrato, upm, [mascaras[i] for i in idx], replicas, semilla)
        for j, i in enumerate(idx):
            ee, lo, hi, val = resumen(pts[j], reps[:, j]) if n[j] > 0 else (None, None, None, 0)
            p = float(pts[j]) if n[j] > 0 and np.isfinite(pts[j]) else None
            out[claves[i]] = {"p": p, "ee": ee, "lo": lo, "hi": hi, "n": int(n[j]), "validas": val}
    return out


def persistencia(series_por_ola, olas, cats):
    """τ² de un grupo (conducta, eje): media de Δ² en logit entre olas consecutivas, sobre
    las categorías `cats`. `series_por_ola[ola][cat]` = p o None."""
    deltas = []
    for a, b in zip(olas[:-1], olas[1:]):
        for c in cats:
            pa, pb = series_por_ola[a].get(c), series_por_ola[b].get(c)
            if abierto(pa) and abierto(pb):
                deltas.append(logit(pb) - logit(pa))
    return tau2(deltas), len(deltas)
