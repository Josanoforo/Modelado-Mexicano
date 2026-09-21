#!/usr/bin/env python3
"""Núcleo común de cuidado en ENUT (2009 · 2014 · 2019 · 2024) — un solo
procedimiento, parametrizado por ola, que consumen los tres CALC del acto
`GEN2-ENUT-PISOS-Y-SERIE-1` (21/sep/2026, CAJA):

    CALC-ENUT2024-NUCLEO-EJES-0001            (P3 · R 2024 por eje + oro)
    CALC-ENUT2019-NUCLEO-EJES-0001            (P2 · piso 2019 por eje)
    CALC-ENUT-SERIE-2009-2014-NUCLEO-0001     (P4 · serie)

Contrato humano: `forense/prereg-caja/ENUT-NUCLEO-ejes-spec-v1_0.md`, sellado
en el COMMIT-1 junto con este archivo, ANTES de abrir un solo registro. La
tabla `data/enut-comparabilidad-texto-v1_0.tsv` (P1) fija, ola por ola, qué
ítems forman cada variante; este módulo la transcribe en `ITEMS` y el test
`tests/test_enut_nucleo_conducto.py` coteja ambas.

QUÉ MIDE
--------
Horas semanales de cuidado a integrantes del hogar, por persona de 12 años y
más, sumando ítems crudos del módulo: h = h_LV + min_LV/60 + h_SD + min_SD/60
por ítem, sin tope. Tres variantes de contenido (P1):
  NUCLEO  común 2014/2019/2024 (C2)   MIN  común 2009-2024 (C3)
  CONCP   sólo 2024, la definición sellada (C1) leída de tvar_crea *_CON_CP,
          más su reconstrucción desde TMODULO (validación de la fórmula).
Por variante: media ponderada (FAC_PER) por UNA variable de agrupación
(nacional · sexo · edad · escolaridad · localidad) con IC95 bootstrap de UPM
dentro de estrato (10 000, PCG64(42), plan de réplicas compartido por todas
las celdas de la ola), y la razón de hogar C4 (horas de mujeres 40+ / total)
con el ponderador de hogar de cada ola.

GUARDIA DE UNA SOLA VARIABLE — código, no prosa (3D, firma de mesa 21/sep)
---------------------------------------------------------------------------
`celdas_de_eje(frame, eje)`: `eje` es UN `str` posicional, dentro de `EJES`;
una lista o dos argumentos lanzan `TypeError`; no existe `cruce()`.
`auditoria_ast()` recorre el AST de ESTE archivo al arrancar `medir()` (y en
el test, con controles positivos por mutación): R1 imports en lista blanca ·
R2 nombres prohibidos (crosstab, pivot, MultiIndex, eval…) · R3 `groupby`
sólo en `_por_llave` y con una sola llave literal · R4 ningún nodo combina
dos comparaciones (`a & b`, `a * b`, `a and b`, tampoco `.eq()/.isin()`) ·
R5 toda lectura de archivo (`ZipFile`, `open`, `read_csv`, `DBF`) sólo en
funciones `_lee_*` · R6 ningún token de otro instrumento en las constantes.
Si falla, `medir()` PARA antes de abrir el zip. El cruce reservado del
marcador (`reparto_hogar × sexo_edad`) no se ve, no se deriva ni se imprime.
"""
from __future__ import annotations

import ast
import io
import os
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from dbfread import DBF

# ── vocabulario fijo ────────────────────────────────────────────────────────
EJES = ("nacional", "sexo", "edad", "escolaridad", "localidad")
CATS = {
    "nacional": ("NAC",),
    "sexo": ("hombre", "mujer"),
    "edad": ("12-17", "18-29", "30-39", "40-59", "60+"),
    "escolaridad": ("hasta_primaria", "secundaria", "media_superior", "superior"),
    "localidad": ("urbano", "rural"),
}
VARIANTES = {"2009": ("MIN",), "2014": ("NUCLEO", "MIN"), "2019": ("NUCLEO", "MIN"),
             "2024": ("NUCLEO", "MIN", "CONCP")}
BOOT_REPS = 10000
SEED = 42
EDAD_CORTES = np.array([12, 18, 30, 40, 60, 10 ** 6])  # digitize → 12-17 … 60+

# Ítems por bloque y variante (transcripción de P1; el test la coteja).
# Clave del bloque = número de pregunta; valor = lista de sufijos de ítem.
ITEMS = {
    "2024": {
        "NUCLEO": {"6.11": ["01", "02", "03", "04", "05", "06", "07", "08", "10", "11", "12", "14"],
                   "6.12": ["01", "02", "03", "05", "06", "07", "08", "09", "10", "12"],
                   "6.13": ["2", "3", "4", "5", "6", "7", "9"],
                   "6.15": ["1", "2", "3", "5", "7"]},
        "MIN": {"6.11": ["01", "02", "05", "06", "07", "08", "14"],
                "6.12": ["01", "02", "03", "05", "06", "07", "08", "09", "12"],
                "6.13": ["2", "3", "4", "5", "6", "9"],
                "6.15": ["2", "3", "7"]},
        # reconstrucción completa de *_CON_CP, bloque por bloque (validación)
        "TODOS": {"6.11": [f"{i:02d}" for i in range(1, 15)],
                  "6.12": [f"{i:02d}" for i in range(1, 13)],
                  "6.13": [str(i) for i in range(1, 10)],
                  "6.15": [str(i) for i in range(1, 8)]},
    },
    "2019": {
        "NUCLEO": {"6.11": [f"{i:02d}" for i in range(1, 12)], "6.12": ["1", "2", "3"],
                   "6.13": ["1", "2", "3", "4", "5", "6"], "6.15": ["1", "2", "3", "4"]},
        "MIN": {"6.11": ["01", "02", "05", "06", "07", "11"], "6.12": ["1", "2", "3"],
                "6.13": ["1", "3", "4", "5", "6"], "6.15": ["2", "4"]},
    },
    "2009": {
        "MIN": {"5.10": ["1", "2", "3", "4", "5", "6"], "5.11": ["1", "2", "3"],
                "5.12": ["1", "2", "3", "4", "5"], "5.13": ["1", "2"]},
    },
}
ITEMS["2014"] = ITEMS["2019"]  # 2014 ≡ 2019 ítem por ítem (P1)

CONCP_COLS = {"6.11": "CUID_ESP_INT_HOG_CON_CP", "6.12": "CUID_INT_0A5_CON_CP",
              "6.13": "CUID_INT_6A14_CON_CP", "6.15": "CUID_INT_60MAS_CON_CP"}

_AUDIT_OTROS_INSTRUMENTOS = ("enif", "envipe", "encig", "enigh", "enoe", "ensanut", "endutih",
                             "encuci", "endireh", "enasem", "mociba", "eder", "lapop", "enadid")


class ReservaRota(RuntimeError):
    """El dato dejó de ser el que la spec declara."""


# ── columnas de tiempo por ola ──────────────────────────────────────────────
def _cols_item(ola: str, bloque: str, suf: str) -> tuple[str, list[str]]:
    """(columna Sí, [h_LV, min_LV, h_SD, min_SD]) del ítem en el esquema de la ola."""
    q = bloque.replace(".", "_")           # "6.11" → "6_11"
    if ola in ("2019", "2024"):
        return f"P{q}_{suf}", [f"P{q}A_{suf}_{k}" for k in (1, 2, 3, 4)]
    return f"P{q}_{suf}_1", [f"P{q}_{suf}_{k}" for k in (2, 3, 4, 5)]


def columnas_de(ola: str, variante: str) -> list[str]:
    out = []
    for bloque, sufs in ITEMS[ola][variante].items():
        for s in sufs:
            si, ts = _cols_item(ola, bloque, s)
            out.append(si)
            out.extend(ts)
    return out


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce").fillna(0.0)


def horas_bloque(df: pd.DataFrame, ola: str, bloque: str, sufs: list[str]) -> tuple[pd.Series, int]:
    """Suma de horas de los ítems listados de un bloque y conteo de ítems «Sí»
    sin ningún tiempo declarado (A.13: el cero no sustituye dato faltante;
    se cuenta y se declara)."""
    total = pd.Series(0.0, index=df.index)
    si_sin_tiempo = 0
    for s in sufs:
        si, (h1, m1, h2, m2) = _cols_item(ola, bloque, s)
        horas = _num(df[h1]) + _num(df[m1]) / 60.0 + _num(df[h2]) + _num(df[m2]) / 60.0
        total = total + horas
        flag_si = df[si].astype(str).str.strip().eq("1")
        sin_tiempo = horas.eq(0.0)
        si_sin_tiempo += int(flag_si[sin_tiempo].sum())
    return total, si_sin_tiempo


# ── lectura (R5: sólo aquí se abre un archivo) ─────────────────────────────
def _lee_csv_zip(ruta: str, miembro: str, cols: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as zf:
        nombres = [n for n in zf.namelist() if n.lower() == miembro.lower()]
        if len(nombres) != 1:
            raise ReservaRota(f"miembro no único en el zip: {miembro}: {nombres}")
        raw = zf.read(nombres[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str,
                            keep_default_na=False, na_filter=False)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ReservaRota(f"codificación no reconocida: {miembro}")
    d.columns = [str(c).strip().upper() for c in d.columns]
    faltan = sorted(set(c.upper() for c in cols) - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes en {miembro}: {faltan}")
    return d[[c.upper() for c in cols]].copy()


def _lee_dbf_zip(ruta: str, miembro: str, cols: list[str], interior: str | None = None) -> pd.DataFrame:
    """DBF dentro de un zip (2009) o dentro de un zip anidado (2014,
    `interior` = nombre del zip interno). Los campos se leen del descriptor
    del DBF (no del FD) como texto crudo; dbfread exige ruta en disco."""
    with zipfile.ZipFile(ruta) as zf:
        fuente = zf
        buf = None
        if interior is not None:
            buf = zipfile.ZipFile(io.BytesIO(zf.read(interior)))
            fuente = buf
        nombres = [n for n in fuente.namelist() if n.lower() == miembro.lower()]
        if len(nombres) != 1:
            raise ReservaRota(f"miembro no único: {miembro}: {nombres}")
        raw = fuente.read(nombres[0])
        if buf is not None:
            buf.close()
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as d:
        p = os.path.join(d, "t.dbf")
        with open(p, "wb") as f:
            f.write(raw)
        tabla = DBF(p, load=False, encoding="latin-1", char_decode_errors="replace",
                    raw=False, ignore_missing_memofile=True)
        campos = [f.name.upper() for f in tabla.fields]
        quiero = [c.upper() for c in cols]
        faltan = sorted(set(quiero) - set(campos))
        if faltan:
            raise ReservaRota(f"variables ausentes en {miembro}: {faltan}")
        filas = [[("" if r[c] is None else str(r[c])) for c in quiero] for r in tabla]
    return pd.DataFrame(filas, columns=quiero, dtype=str)


# ── ejes: cada uno UNA columna derivada ────────────────────────────────────
def _code(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def eje_sexo(s: pd.Series) -> pd.Series:
    return _code(s).map({"1": "hombre", "2": "mujer"})


def eje_edad(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s.astype(str).str.strip(), errors="coerce")
    pos = np.digitize(x.fillna(-1).to_numpy(), EDAD_CORTES)   # 0 = <12 (fuera)
    etiquetas = np.array([None, "12-17", "18-29", "30-39", "40-59", "60+", None], dtype=object)
    out = pd.Series(etiquetas[pos], index=s.index, dtype="object")
    out[x.isna()] = None
    return out


def eje_escolaridad(s: pd.Series, ola: str) -> pd.Series:
    if ola == "2009":
        mapa = {"0": "hasta_primaria", "1": "hasta_primaria", "2": "hasta_primaria", "3": "secundaria",
                "4": "media_superior", "5": "media_superior", "6": "media_superior",
                "7": "superior", "8": "superior", "9": "superior"}
    else:
        mapa = {"0": "hasta_primaria", "1": "hasta_primaria", "2": "hasta_primaria", "3": "secundaria",
                "4": "media_superior", "5": "media_superior", "6": "media_superior", "7": "media_superior",
                "8": "superior", "9": "superior", "10": "superior", "11": "superior"}
    return _code(s).map(mapa)


def eje_localidad(s: pd.Series, ola: str) -> pd.Series:
    if ola == "2009":
        return _code(s).map({"1": "urbano", "2": "rural"})
    return _code(s).map({"1": "urbano", "2": "urbano", "3": "urbano", "4": "rural"})


def celdas_de_eje(frame: pd.DataFrame, eje: str) -> pd.Series:
    """La guardia: UN eje por llamada, `str` posicional único, en `EJES`.
    Devuelve la columna de grupo ya derivada (`_eje_<eje>`); no combina."""
    if not isinstance(eje, str):
        raise TypeError(f"eje debe ser UN str, llegó {type(eje).__name__}: "
                        "una sola variable de agrupación por firma")
    if eje not in EJES:
        raise ValueError(f"eje {eje!r} no es uno de {EJES}")
    if eje == "nacional":
        return pd.Series("NAC", index=frame.index, dtype="object")
    return frame[f"_eje_{eje}"]


# ── agregación por llave (R3: sólo aquí, una llave literal) ────────────────
def _por_llave(df: pd.DataFrame, columnas: dict[str, str]) -> pd.DataFrame:
    """Agrega por `_llave` (una sola columna de texto) con las funciones
    indicadas: {"columna": "sum" | "first"}."""
    return df.groupby("_llave", sort=True).agg(columnas).reset_index()


# ── estimador (molde CALC-PISOS-ENVIPE2024-EJES-0002) ──────────────────────
def _slug(v: str) -> str:
    return (str(v).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
            .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
            .replace("_", "-").replace(" ", "-"))


def celdas_media(prefijo: str, frame: pd.DataFrame, y: pd.Series) -> list[dict]:
    out = []
    for eje in EJES:
        grupo = celdas_de_eje(frame, eje)
        for cat in CATS[eje]:
            out.append({"base": f"{prefijo}-{_slug(eje)}-{_slug(cat)}",
                        "mask": grupo.eq(cat), "y": y})
    return out


def estimar(d: pd.DataFrame, cells: list[dict], reps: int = BOOT_REPS, seed: int = SEED) -> dict:
    """Σw·y/Σw por celda con IC95 por bootstrap de UPM dentro de estrato; un
    único plan de réplicas para todas las celdas del frame. `d` trae `_w`,
    `_est`, `_upm`. Sin soporte → punto/IC nulos, N/DEN-W/B-VALIDAS se
    conservan (D-22: el camino de la celda rara existe y se prueba)."""
    design = d["_w"].notna()
    design = design.mul(d["_w"].gt(0))
    design = design.mul(d["_est"].ne(""))
    design = design.mul(d["_upm"].ne("")).astype(bool)
    w = d.loc[design].copy()
    w["_key"] = w["_est"].astype(str) + "\t" + w["_upm"].astype(str)
    keys = sorted(w["_key"].unique())
    pos = {k: i for i, k in enumerate(keys)}
    denm = np.zeros((len(keys), len(cells)))
    num = np.zeros_like(denm)
    counts = np.zeros(len(cells), dtype=np.int64)
    kidx = w["_key"].map(pos).to_numpy()
    wv = w["_w"].to_numpy(dtype=float)
    for j, cell in enumerate(cells):
        m = cell["mask"].reindex(w.index, fill_value=False).to_numpy(dtype=bool)
        y = cell["y"].reindex(w.index).to_numpy(dtype=float)
        m = m & np.isfinite(y)
        counts[j] = int(m.sum())
        denm[:, j] = np.bincount(kidx[m], weights=wv[m], minlength=len(keys))
        num[:, j] = np.bincount(kidx[m], weights=wv[m] * y[m], minlength=len(keys))
    den = denm.sum(0)
    point = np.divide(num.sum(0), den, out=np.full(len(cells), np.nan), where=den > 0)
    strata: dict[str, list[int]] = {}
    for key in keys:
        strata.setdefault(key.split("\t", 1)[0], []).append(pos[key])
    rng = np.random.Generator(np.random.PCG64(seed))
    boot = np.full((reps, len(cells)), np.nan)
    for start in range(0, reps, 50):
        size = min(50, reps - start)
        mult = np.zeros((size, len(keys)), dtype=np.int16)
        for h in sorted(strata):
            ix = np.asarray(strata[h], dtype=int)
            draws = rng.integers(0, len(ix), size=(size, len(ix)))
            for row in range(size):
                mult[row] += np.bincount(ix[draws[row]], minlength=len(keys)).astype(np.int16)
        den_b = mult @ denm
        boot[start:start + size] = np.divide(mult @ num, den_b, out=np.full_like(den_b, np.nan),
                                             where=den_b > 0)
    out = {}
    for j, cell in enumerate(cells):
        valid = np.isfinite(boot[:, j])
        if np.isfinite(point[j]) and valid.any():
            lo, hi = np.percentile(boot[valid, j], [2.5, 97.5])
            vals = (float(point[j]), float(lo), float(hi))
        else:
            vals = (None, None, None)
        rid = cell["base"]
        out[rid + "-P"], out[rid + "-IC-LO"], out[rid + "-IC-HI"] = vals
        out[rid + "-N"] = int(counts[j])
        out[rid + "-DEN-W"] = float(den[j])
        out[rid + "-B-VALIDAS"] = int(valid.sum())
    return out


# ── carga por ola: un frame de PERSONAS 12+ con ejes, diseño y horas ───────
def _frame_2024(ruta: str) -> tuple[pd.DataFrame, dict]:
    base = ["LLAVEMOD", "LLAVEHOG", "SEXO", "EDAD_V", "NIV", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER"]
    cols = base + columnas_de("2024", "TODOS")
    m = _lee_csv_zip(ruta, "tmodulo.csv", cols)
    tv = _lee_csv_zip(ruta, "tvar_crea.csv", ["LLAVEMOD", "LLAVEHOG", "SEXO", "EDAD", "FAC_PER",
                                                "EST_DIS", "UPM_DIS"] + list(CONCP_COLS.values()) + ["CUID_INT_15A59"])
    ts = _lee_csv_zip(ruta, "tsdem.csv", ["LLAVEHOG", "FAC_HOG"])
    diag = {"FILAS-MODULO": int(len(m)), "FILAS-TVAR-CREA": int(len(tv)), "FILAS-TSDEM": int(len(ts))}
    m["_llave"] = m["LLAVEMOD"].str.strip()
    tv["_llave"] = tv["LLAVEMOD"].str.strip()
    d = m.merge(tv[["_llave"] + list(CONCP_COLS.values()) + ["CUID_INT_15A59", "EDAD", "SEXO", "FAC_PER"]]
                .rename(columns={"EDAD": "_EDAD_TV", "SEXO": "_SEXO_TV", "FAC_PER": "_FAC_TV"}),
                on="_llave", how="left", validate="1:1", indicator=True)
    diag["JOIN-SIN-TVAR-CREA"] = int(d["_merge"].ne("both").sum())
    d = d.drop(columns="_merge")
    # ponderador de hogar: FAC_HOG constante dentro de LLAVEHOG (guarda)
    ts["_llave"] = ts["LLAVEHOG"].str.strip()
    ts["_fh"] = pd.to_numeric(ts["FAC_HOG"], errors="coerce")
    h = _por_llave(ts[["_llave", "_fh"]], {"_fh": "first"})
    h2 = _por_llave(ts[["_llave", "_fh"]].assign(_fh=ts["_fh"].astype(float)), {"_fh": "nunique"})
    diag["HOGARES-FAC-HOG-NO-CONSTANTE"] = int(h2["_fh"].gt(1).sum())
    d["_hog"] = d["LLAVEHOG"].str.strip()
    d = d.merge(h.rename(columns={"_llave": "_hog", "_fh": "_w_hog"}), on="_hog", how="left", validate="m:1")
    return _completa(d, "2024", "EDAD_V", "NIV", "TLOC"), diag


def _frame_2019(ruta: str) -> tuple[pd.DataFrame, dict]:
    base = ["UPM", "VIV_SEL", "HOGAR", "N_REN", "SEXO", "EDAD_V", "NIV", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER"]
    m = _lee_csv_zip(ruta, "enut_2019/TMODULO.csv", base + columnas_de("2019", "NUCLEO"))
    hg = _lee_csv_zip(ruta, "enut_2019/THOGAR.csv", ["UPM", "VIV_SEL", "HOGAR", "FAC_HOG"])
    diag = {"FILAS-MODULO": int(len(m)), "FILAS-THOGAR": int(len(hg))}
    m["_hog"] = m["UPM"].str.strip() + "|" + m["VIV_SEL"].str.strip() + "|" + m["HOGAR"].str.strip()
    hg["_hog"] = hg["UPM"].str.strip() + "|" + hg["VIV_SEL"].str.strip() + "|" + hg["HOGAR"].str.strip()
    hg["_w_hog"] = pd.to_numeric(hg["FAC_HOG"], errors="coerce")
    hg = hg.drop_duplicates("_hog")
    d = m.merge(hg[["_hog", "_w_hog"]], on="_hog", how="left", validate="m:1")
    return _completa(d, "2019", "EDAD_V", "NIV", "TLOC"), diag


def _frame_2014(ruta: str) -> tuple[pd.DataFrame, dict]:
    interior = "Enut2014.zip"
    llave = ["CONTROL", "VIV_SEL", "HOGAR", "N_REN"]
    it = ITEMS["2014"]["NUCLEO"]
    c2 = [c for b in ("6.11", "6.12", "6.13") for s in it[b] for c in
          [_cols_item("2014", b, s)[0]] + _cols_item("2014", b, s)[1]]
    c3 = [c for s in it["6.15"] for c in [_cols_item("2014", "6.15", s)[0]] + _cols_item("2014", "6.15", s)[1]]
    m2 = _lee_dbf_zip(ruta, "TMODULO2.dbf", llave + ["TLOC", "UPM_DIS", "EDIS", "FAC_PER"] + c2, interior)
    m3 = _lee_dbf_zip(ruta, "TMODULO3.dbf", llave + c3, interior)
    m1 = _lee_dbf_zip(ruta, "TMODULO1.dbf", llave + ["NIV"], interior)
    sd = _lee_dbf_zip(ruta, "TSDem.dbf", llave + ["SEXO", "EDAD"], interior)
    hg = _lee_dbf_zip(ruta, "THOGAR.dbf", ["CONTROL", "VIV_SEL", "HOGAR", "FAC_VIV"], interior)
    diag = {"FILAS-MODULO": int(len(m2)), "FILAS-MODULO3": int(len(m3)), "FILAS-TSDEM": int(len(sd)),
            "FILAS-THOGAR": int(len(hg))}
    for t in (m2, m3, m1, sd):
        t["_llave"] = t["CONTROL"].str.strip() + "|" + t["VIV_SEL"].str.strip() + "|" + \
            t["HOGAR"].str.strip() + "|" + t["N_REN"].str.strip()
    d = m2.merge(m3.drop(columns=llave), on="_llave", how="left", validate="1:1", indicator=True)
    diag["JOIN-SIN-MODULO3"] = int(d["_merge"].ne("both").sum())
    d = d.drop(columns="_merge").merge(m1.drop(columns=llave), on="_llave", how="left", validate="1:1")
    d = d.merge(sd.drop(columns=llave), on="_llave", how="left", validate="1:1", indicator=True)
    diag["JOIN-SIN-TSDEM"] = int(d["_merge"].ne("both").sum())
    d = d.drop(columns="_merge")
    d["_hog"] = d["CONTROL"].str.strip() + "|" + d["VIV_SEL"].str.strip() + "|" + d["HOGAR"].str.strip()
    hg["_hog"] = hg["CONTROL"].str.strip() + "|" + hg["VIV_SEL"].str.strip() + "|" + hg["HOGAR"].str.strip()
    hg["_w_hog"] = pd.to_numeric(hg["FAC_VIV"], errors="coerce")
    hg = hg.drop_duplicates("_hog")
    d = d.merge(hg[["_hog", "_w_hog"]], on="_hog", how="left", validate="m:1")
    d = d.rename(columns={"EDIS": "EST_DIS"})
    return _completa(d, "2014", "EDAD", "NIV", "TLOC"), diag


def _frame_2009(ruta: str) -> tuple[pd.DataFrame, dict]:
    llave = ["CONTROL", "VIV_SEL", "HOGAR", "N_REN"]
    it = ITEMS["2009"]["MIN"]
    cm = [c for b in ("5.11", "5.12", "5.13") for s in it[b] for c in
          [_cols_item("2009", b, s)[0]] + _cols_item("2009", b, s)[1]]
    cc = [c for s in it["5.10"] for c in [_cols_item("2009", "5.10", s)[0]] + _cols_item("2009", "5.10", s)[1]]
    m2 = _lee_dbf_zip(ruta, "TModulo2.dbf", llave + ["LOC", "EST_DIS", "UPM_DIS", "FAC_PER"] + cm)
    tc = _lee_dbf_zip(ruta, "TCuidados.dbf", llave + ["N_REF"] + cc)
    sd = _lee_dbf_zip(ruta, "TSDem.dbf", llave + ["SEXO", "EDAD", "NIV"])
    hg = _lee_dbf_zip(ruta, "THogar.dbf", ["CONTROL", "VIV_SEL", "HOGAR", "FAC_VIV"])
    diag = {"FILAS-MODULO": int(len(m2)), "FILAS-TCUIDADOS": int(len(tc)), "FILAS-TSDEM": int(len(sd)),
            "FILAS-THOGAR": int(len(hg))}
    for t in (m2, tc, sd):
        t["_llave"] = t["CONTROL"].str.strip() + "|" + t["VIV_SEL"].str.strip() + "|" + \
            t["HOGAR"].str.strip() + "|" + t["N_REN"].str.strip()
    # 5.10 se capta por persona cuidada (N_REF): se suma por cuidador
    h510, sin_t = horas_bloque(tc, "2009", "5.10", it["5.10"])
    tc["_h510"] = h510
    agg = _por_llave(tc[["_llave", "_h510"]], {"_h510": "sum"})
    d = m2.merge(agg, on="_llave", how="left", validate="1:1")
    d["_h510"] = d["_h510"].fillna(0.0)
    diag["SI-SIN-TIEMPO-5-10"] = sin_t
    d = d.merge(sd.drop(columns=llave), on="_llave", how="left", validate="1:1", indicator=True)
    diag["JOIN-SIN-TSDEM"] = int(d["_merge"].ne("both").sum())
    d = d.drop(columns="_merge")
    d["_hog"] = d["CONTROL"].str.strip() + "|" + d["VIV_SEL"].str.strip() + "|" + d["HOGAR"].str.strip()
    hg["_hog"] = hg["CONTROL"].str.strip() + "|" + hg["VIV_SEL"].str.strip() + "|" + hg["HOGAR"].str.strip()
    hg["_w_hog"] = pd.to_numeric(hg["FAC_VIV"], errors="coerce")
    hg = hg.drop_duplicates("_hog")
    d = d.merge(hg[["_hog", "_w_hog"]], on="_hog", how="left", validate="m:1")
    return _completa(d, "2009", "EDAD", "NIV", "LOC"), diag


def _completa(d: pd.DataFrame, ola: str, col_edad: str, col_niv: str, col_loc: str) -> pd.DataFrame:
    d["_w"] = pd.to_numeric(d["FAC_PER"].astype(str).str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].astype(str).str.strip()
    d["_upm"] = d["UPM_DIS"].astype(str).str.strip()
    d["_eje_sexo"] = eje_sexo(d["SEXO"])
    d["_eje_edad"] = eje_edad(d[col_edad])
    d["_eje_escolaridad"] = eje_escolaridad(d[col_niv], ola)
    d["_eje_localidad"] = eje_localidad(d[col_loc], ola)
    d["_mujer40"] = _mujer40(d["_eje_sexo"], d[col_edad])
    return d


def _mujer40(sexo_eje: pd.Series, edad: pd.Series) -> pd.Series:
    """Numerador de la razón C4 (CALC-ENUT-0001): mujer y 40+. Es una
    SUBPOBLACIÓN dentro del hogar, no una celda de salida: la razón se emite
    sólo NACIONAL. Se escribe aquí, en su propia función, para que la
    auditoría R4 la vea como lo que es y no como un cruce disfrazado."""
    m = sexo_eje.eq("mujer")
    m = m.mul(pd.to_numeric(edad.astype(str).str.strip(), errors="coerce").ge(40))
    return m.astype(float)


CARGADORES = {"2024": _frame_2024, "2019": _frame_2019, "2014": _frame_2014, "2009": _frame_2009}


def horas_variante(d: pd.DataFrame, ola: str, variante: str) -> tuple[pd.Series, int]:
    if ola == "2009":
        h, sin_t = pd.Series(0.0, index=d.index), 0
        for b in ("5.11", "5.12", "5.13"):
            hb, st = horas_bloque(d, ola, b, ITEMS[ola][variante][b])
            h = h + hb
            sin_t += st
        return h + d["_h510"], sin_t
    h, sin_t = pd.Series(0.0, index=d.index), 0
    for b, sufs in ITEMS[ola][variante].items():
        hb, st = horas_bloque(d, ola, b, sufs)
        h = h + hb
        sin_t += st
    return h, sin_t


def razon_hogar(d: pd.DataFrame, y: pd.Series, prefijo: str, reps: int, seed: int) -> tuple[dict, dict]:
    """C4: Σ_h w_h·num_h / Σ_h w_h·den_h sobre hogares (0/0 dentro), como razón
    ponderada de la media Σ(w_h·den_h)·(num_h/den_h) / Σ(w_h·den_h) — misma
    álgebra, mismo bootstrap de UPM dentro de estrato."""
    t = d[["_hog", "_w_hog", "_est", "_upm"]].copy()
    t["_llave"] = t["_hog"]
    t["_den"] = y.to_numpy(dtype=float)
    t["_num"] = (y * d["_mujer40"]).to_numpy(dtype=float)
    hog = _por_llave(t, {"_w_hog": "first", "_est": "first", "_upm": "first", "_den": "sum", "_num": "sum"})
    est_nun = _por_llave(t[["_llave", "_est"]], {"_est": "nunique"})
    diag = {f"{prefijo}-HOGARES": int(len(hog)),
            f"{prefijo}-HOGARES-SIN-PONDERADOR": int(hog["_w_hog"].isna().sum()),
            f"{prefijo}-HOGARES-CON-CARGA": int(hog["_den"].gt(0).sum()),
            f"{prefijo}-HOGARES-DISENO-NO-CONSTANTE": int(est_nun["_est"].gt(1).sum())}
    hog["_w"] = hog["_w_hog"] * hog["_den"]
    hog["_y"] = np.divide(hog["_num"].to_numpy(), hog["_den"].to_numpy(),
                          out=np.zeros(len(hog)), where=hog["_den"].to_numpy() > 0)
    cells = [{"base": f"{prefijo}-NACIONAL", "mask": pd.Series(True, index=hog.index), "y": hog["_y"]}]
    res = estimar(hog, cells, reps, seed)
    # N = hogares del universo (incluidos los 0/0), no los de peso > 0
    res[f"{prefijo}-NACIONAL-N"] = int(hog["_w_hog"].notna().sum())
    return res, diag


def medir_ola(ola: str, ruta_zip: str, reps: int = BOOT_REPS, seed: int = SEED,
              oro: dict | None = None) -> dict:
    """Todos los RESULT de una ola. `oro` (sólo 2024): {"A_R": valor sellado
    de CALC-ENUT-0001} para el cotejo. Los ids llevan el prefijo
    RESULT-ENUT<ola>-…; el catálogo lo enumera `catalogo_resultados`."""
    P = f"RESULT-ENUT{ola}"
    d, diag = CARGADORES[ola](ruta_zip)
    out = {f"{P}-{k}": v for k, v in diag.items()}
    out[f"{P}-N-UNIVERSO"] = int(len(d))
    out[f"{P}-N-SIN-PONDERADOR"] = int((~(d["_w"].notna().mul(d["_w"].gt(0)))).sum())
    for eje in EJES[1:]:
        out[f"{P}-FUERA-{_slug(eje)}"] = int(d[f"_eje_{eje}"].isna().sum())
    cells, yv = [], {}
    for v in VARIANTES[ola]:
        if v == "CONCP":
            y = sum(pd.to_numeric(d[c], errors="coerce") for c in CONCP_COLS.values())
            out[f"{P}-CONCP-NULOS"] = int(y.isna().sum())
            y = y.fillna(0.0)
            # validación de la fórmula: suma de TODOS los ítems crudos vs tvar_crea, por bloque
            peor = 0.0
            for b, col in CONCP_COLS.items():
                hb, _ = horas_bloque(d, ola, b, ITEMS[ola]["TODOS"][b])
                dif = (hb - pd.to_numeric(d[col], errors="coerce").fillna(0.0)).abs()
                out[f"{P}-VALIDACION-CONCP-{_slug(b)}-MAX-ABS"] = float(dif.max())
                out[f"{P}-VALIDACION-CONCP-{_slug(b)}-N-DISCORDANTES"] = int(dif.gt(1e-6).sum())
                peor = max(peor, float(dif.max()))
            out[f"{P}-VALIDACION-CONCP-MAX-ABS"] = peor
            sin_t = 0
        else:
            y, sin_t = horas_variante(d, ola, v)
        out[f"{P}-{v}-SI-SIN-TIEMPO"] = int(sin_t)
        out[f"{P}-{v}-MEDIA-HORAS-CRUDA"] = float(y.mean())
        yv[v] = y
        cells += celdas_media(f"{P}-{v}", d, y)
    out.update(estimar(d, cells, reps, seed))
    for v in VARIANTES[ola]:
        r, dg = razon_hogar(d, yv[v], f"{P}-RAZON-{v}", reps, seed)
        out.update(r)
        out.update(dg)
    if ola == "2024":
        # oro: la razón sellada de CALC-ENUT-0001 se recalcula EXACTAMENTE como
        # allí (tvar_crea: SEXO/EDAD de tvar_crea, FAC_HOG de tsdem, todos los hogares)
        t = d[["_hog", "_w_hog", "_est", "_upm"]].copy()
        t["_llave"] = t["_hog"]
        yy = yv["CONCP"]
        muj = _mujer40(eje_sexo(d["_SEXO_TV"]), d["_EDAD_TV"])
        t["_den"] = yy.to_numpy(dtype=float)
        t["_num"] = (yy * muj).to_numpy(dtype=float)
        hog = _por_llave(t, {"_w_hog": "first", "_den": "sum", "_num": "sum"})
        ok = hog["_w_hog"].notna()
        a_r = float((hog.loc[ok, "_w_hog"] * hog.loc[ok, "_num"]).sum() /
                    (hog.loc[ok, "_w_hog"] * hog.loc[ok, "_den"]).sum())
        out[f"{P}-ORO-A-R-RECALCULADA"] = a_r
        out[f"{P}-ORO-A-R-SELLADA"] = float(oro["A_R"]) if oro else None
        out[f"{P}-ORO-A-R-DELTA"] = (abs(a_r - float(oro["A_R"])) if oro else None)
        out[f"{P}-ORO-HOGARES"] = int(ok.sum())
    return out


def catalogo_resultados(ola: str) -> list[dict]:
    """Ids que `medir_ola` emite para la ola, con tipo y unidad; el
    `spec.yaml` de cada CALC se coteja contra esto en el test."""
    P = f"RESULT-ENUT{ola}"
    cat: list[dict] = []

    def add(rid, tipo, unidad, nulo=False):
        r = {"id": rid, "tipo": tipo, "unidad": unidad}
        if nulo:
            r["permite_no_estimable"] = True
        cat.append(r)

    diag_por_ola = {
        "2024": ["FILAS-MODULO", "FILAS-TVAR-CREA", "FILAS-TSDEM", "JOIN-SIN-TVAR-CREA",
                 "HOGARES-FAC-HOG-NO-CONSTANTE"],
        "2019": ["FILAS-MODULO", "FILAS-THOGAR"],
        "2014": ["FILAS-MODULO", "FILAS-MODULO3", "FILAS-TSDEM", "FILAS-THOGAR", "JOIN-SIN-MODULO3",
                 "JOIN-SIN-TSDEM"],
        "2009": ["FILAS-MODULO", "FILAS-TCUIDADOS", "FILAS-TSDEM", "FILAS-THOGAR", "SI-SIN-TIEMPO-5-10",
                 "JOIN-SIN-TSDEM"],
    }
    for k in diag_por_ola[ola]:
        add(f"{P}-{k}", "entero", "conteo de filas")
    add(f"{P}-N-UNIVERSO", "entero", "personas 12+ del módulo")
    add(f"{P}-N-SIN-PONDERADOR", "entero", "personas sin FAC_PER válido")
    for eje in EJES[1:]:
        add(f"{P}-FUERA-{_slug(eje)}", "entero", f"personas sin categoría en {eje}")
    for v in VARIANTES[ola]:
        if v == "CONCP":
            add(f"{P}-CONCP-NULOS", "entero", "personas con algún *_CON_CP nulo")
            for b in CONCP_COLS:
                add(f"{P}-VALIDACION-CONCP-{_slug(b)}-MAX-ABS", "flotante", "horas, |suma crudos − tvar_crea| máx")
                add(f"{P}-VALIDACION-CONCP-{_slug(b)}-N-DISCORDANTES", "entero", "personas con |dif| > 1e-6")
            add(f"{P}-VALIDACION-CONCP-MAX-ABS", "flotante", "horas, peor bloque")
        add(f"{P}-{v}-SI-SIN-TIEMPO", "entero", "ítems Sí sin tiempo declarado")
        add(f"{P}-{v}-MEDIA-HORAS-CRUDA", "flotante", "horas/semana, media sin ponderar (diagnóstico)")
        for eje in EJES:
            for c in CATS[eje]:
                base = f"{P}-{v}-{_slug(eje)}-{_slug(c)}"
                add(base + "-P", "flotante", "horas/semana, media ponderada FAC_PER", nulo=True)
                add(base + "-IC-LO", "flotante", "límite inferior IC95 bootstrap", nulo=True)
                add(base + "-IC-HI", "flotante", "límite superior IC95 bootstrap", nulo=True)
                add(base + "-N", "entero", "n sin ponderar")
                add(base + "-DEN-W", "flotante", "suma de FAC_PER en la celda")
                add(base + "-B-VALIDAS", "entero", "réplicas bootstrap definidas")
    for v in VARIANTES[ola]:
        base = f"{P}-RAZON-{v}-NACIONAL"
        add(base + "-P", "proporcion", "razón horas mujeres 40+ / total del hogar [0,1]", nulo=True)
        add(base + "-IC-LO", "proporcion", "límite inferior IC95 bootstrap", nulo=True)
        add(base + "-IC-HI", "proporcion", "límite superior IC95 bootstrap", nulo=True)
        add(base + "-N", "entero", "hogares del universo con ponderador")
        add(base + "-DEN-W", "flotante", "Σ w_h·den_h")
        add(base + "-B-VALIDAS", "entero", "réplicas bootstrap definidas")
        add(f"{P}-RAZON-{v}-HOGARES", "entero", "hogares agregados")
        add(f"{P}-RAZON-{v}-HOGARES-SIN-PONDERADOR", "entero", "hogares sin ponderador de hogar")
        add(f"{P}-RAZON-{v}-HOGARES-CON-CARGA", "entero", "hogares con alguna hora")
        add(f"{P}-RAZON-{v}-HOGARES-DISENO-NO-CONSTANTE", "entero", "hogares con más de un estrato")
    if ola == "2024":
        add(f"{P}-ORO-A-R-RECALCULADA", "proporcion", "razón CON_CP como CALC-ENUT-0001")
        add(f"{P}-ORO-A-R-SELLADA", "proporcion", "A-R de CALC-ENUT-0001/resultados.json", nulo=True)
        add(f"{P}-ORO-A-R-DELTA", "flotante", "|recalculada − sellada|", nulo=True)
        add(f"{P}-ORO-HOGARES", "entero", "hogares con FAC_HOG en el oro")
    add(f"{P}-AUDITORIA-AST", "texto", "PASA o lista de violaciones")
    return cat


# ── auditoría del AST de este archivo (la guardia como código) ─────────────
_AUDIT_IMPORTS = ("__future__", "ast", "io", "os", "tempfile", "zipfile", "pathlib", "numpy",
                  "pandas", "dbfread")
_AUDIT_PROHIBIDOS = ("crosstab", "pivot", "pivot_table", "unstack", "stack", "MultiIndex", "query",
                     "eval", "exec", "getattr", "setattr", "globals", "locals", "vars", "compile",
                     "__import__", "cruce", "read_excel", "read_table", "read_sav", "read_dta",
                     "read_stata", "read_spss")
_AUDIT_LECTORES = ("ZipFile", "open", "read_csv", "DBF")
_AUDIT_COMPARADORES = ("eq", "ne", "lt", "le", "gt", "ge", "isin", "between")


def _nombre_llamado(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _tiene_comparacion(nodo: ast.AST) -> bool:
    for sub in ast.walk(nodo):
        if isinstance(sub, ast.Compare):
            return True
        if isinstance(sub, ast.Call) and _nombre_llamado(sub) in _AUDIT_COMPARADORES:
            return True
    return False


def auditoria_ast_fuente(fuente: str) -> list[str]:
    arbol = ast.parse(fuente)
    viol: list[str] = []
    exentos: set[int] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            cuerpo = nodo.body
            if cuerpo and isinstance(cuerpo[0], ast.Expr) and isinstance(cuerpo[0].value, ast.Constant):
                exentos.add(id(cuerpo[0].value))
        if isinstance(nodo, ast.Assign):
            nombres = [t.id for t in nodo.targets if isinstance(t, ast.Name)]
            if any(n.startswith("_AUDIT_") for n in nombres):
                for sub in ast.walk(nodo.value):
                    if isinstance(sub, ast.Constant):
                        exentos.add(id(sub))
    padre_fn: dict[int, str] = {}

    def _marca(nodo, fn):
        for hijo in ast.iter_child_nodes(nodo):
            nombre = fn
            if isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nombre = hijo.name
            padre_fn[id(hijo)] = nombre
            _marca(hijo, nombre)
    _marca(arbol, "<modulo>")

    for nodo in ast.walk(arbol):
        fn = padre_fn.get(id(nodo), "<modulo>")
        if isinstance(nodo, ast.Import):
            for a in nodo.names:
                if a.name not in _AUDIT_IMPORTS:
                    viol.append(f"R1 import prohibido: {a.name}")
        elif isinstance(nodo, ast.ImportFrom):
            if (nodo.module or "") not in _AUDIT_IMPORTS:
                viol.append(f"R1 import prohibido: from {nodo.module}")
        if isinstance(nodo, ast.Attribute) and nodo.attr in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 atributo prohibido `.{nodo.attr}` en {fn}")
        if isinstance(nodo, ast.Name) and nodo.id in _AUDIT_PROHIBIDOS:
            viol.append(f"R2 nombre prohibido `{nodo.id}` en {fn}")
        if isinstance(nodo, ast.Call):
            nom = _nombre_llamado(nodo)
            if nom in _AUDIT_PROHIBIDOS:
                viol.append(f"R2 llamada prohibida `{nom}()` en {fn}")
            if nom == "groupby":
                if fn != "_por_llave":
                    viol.append(f"R3 `groupby` fuera de _por_llave: {fn}")
                llaves = [a.value for a in nodo.args if isinstance(a, ast.Constant)]
                if llaves != ["_llave"]:
                    viol.append(f"R3 `groupby` con llave distinta de la única literal `_llave` en {fn}")
            if nom in _AUDIT_LECTORES and not fn.startswith("_lee_"):
                viol.append(f"R5 lectura `{nom}()` fuera de _lee_*: {fn}")
        if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, (ast.BitAnd, ast.BitOr, ast.BitXor, ast.Mult)):
            if _tiene_comparacion(nodo.left) and _tiene_comparacion(nodo.right):
                viol.append(f"R4 dos comparaciones combinadas por operador en {fn} (línea {nodo.lineno})")
        if isinstance(nodo, ast.BoolOp):
            con = [v for v in nodo.values if _tiene_comparacion(v)]
            if len(con) >= 2:
                viol.append(f"R4 dos comparaciones combinadas por and/or en {fn} (línea {nodo.lineno})")
        if isinstance(nodo, ast.Call) and _nombre_llamado(nodo) == "mul":
            objetivo = nodo.func.value if isinstance(nodo.func, ast.Attribute) else None
            if objetivo is not None and _tiene_comparacion(objetivo) and nodo.args and _tiene_comparacion(nodo.args[0]):
                viol.append(f"R4 dos comparaciones combinadas por .mul() en {fn} (línea {nodo.lineno})")
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str) and id(nodo) not in exentos:
            bajo = nodo.value.lower()
            for tok in _AUDIT_OTROS_INSTRUMENTOS:
                if tok in bajo:
                    viol.append(f"R6 token de otro instrumento `{tok}` en {fn}")
    return viol


def auditoria_ast() -> list[str]:
    return auditoria_ast_fuente(Path(__file__).read_text(encoding="utf-8"))
