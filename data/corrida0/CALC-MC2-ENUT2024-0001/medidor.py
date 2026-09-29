#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENUT 2024 · CALC-MC2-ENUT2024-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENUT 2024 (ola vista; persona de 12+,
tmodulo unida 1:1 por LLAVEMOD a tvar_crea): cuidado a dependientes (enfermedad,
discapacidad o 60+) por sexo, participación de los hombres en cuidados por edad,
tamaño de localidad y escolaridad, participación de las mujeres en el total de
horas de trabajo no remunerado, y trabajo comunitario gratuito mujer − hombre.
Contrato humano: forense/prereg-caja/MC2-ENUT2024-spec-v1_0.md.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD = "enut2024_bd_csv"
PFX = "RESULT-MC2-ENUT2024"
COLS_M = ["LLAVEMOD", "SEXO", "EDAD_V", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER", "P6_17_3"]
COLS_V = ["LLAVEMOD", "TRAB_NO_REM_VOL", "TRAB_NO_REM_CON_CP", "CUID_ESP_INT_HOG_CON_CP", "CUID_INT_60MAS_CON_CP",
          "ESCOLARIDAD"]
EDADES = [("12-17", 12, 17), ("18-29", 18, 29), ("30-39", 30, 39), ("40-59", 40, 59), ("60-MAS", 60, 97)]
ESC = [("HASTA-BASICA", {"1", "2"}), ("MEDIA-SUPERIOR", {"3"}), ("SUPERIOR", {"4", "5"})]


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara."""


def _lee(ruta, miembro, cols):
    with zipfile.ZipFile(ruta) as zf:
        n = [x for x in zf.namelist() if x.lower() == miembro]
        if len(n) != 1:
            raise ReservaRota(f"miembro no único: {miembro}")
        raw = zf.read(n[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    quiero = {c.upper() for c in cols}
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: str(c).strip().upper() in quiero)
    d.columns = [str(c).strip().upper() for c in d.columns]
    if quiero - set(d.columns):
        raise ReservaRota(f"variables ausentes en {miembro}: {sorted(quiero - set(d.columns))}")
    return d


def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _num(s):
    x = pd.to_numeric(s.astype(str).str.strip(), errors="coerce")
    return x.where(x >= 0)


# ── estimador: razones ponderadas con bootstrap de UPM dentro de estrato ───
def _estima(d: pd.DataFrame, celdas: list[tuple], difs: list[tuple], reps: int, seed: int) -> tuple[dict, dict]:
    """celdas: (id, mask, y). Punto = Σw·y/Σw sobre mask∧finito(y).
    difs: (id, id_a, id_b) = celda a − celda b en la MISMA réplica."""
    ok = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    w = d.loc[ok]
    key = w["_est"] + "\t" + w["_upm"]
    keys = sorted(key.unique())
    pos = {k: i for i, k in enumerate(keys)}
    kidx = key.map(pos).to_numpy()
    wv = w["_w"].to_numpy(dtype=float)
    nk, nc = len(keys), len(celdas)
    den = np.zeros((nk, nc))
    num = np.zeros((nk, nc))
    cnt = np.zeros(nc, dtype=np.int64)
    for j, (_, m, y) in enumerate(celdas):
        mm = m.reindex(w.index, fill_value=False).to_numpy(dtype=bool)
        yy = y.reindex(w.index).to_numpy(dtype=float)
        mm = mm & np.isfinite(yy)
        cnt[j] = int(mm.sum())
        den[:, j] = np.bincount(kidx[mm], weights=wv[mm], minlength=nk)
        num[:, j] = np.bincount(kidx[mm], weights=wv[mm] * yy[mm], minlength=nk)
    D, N = den.sum(0), num.sum(0)
    punto = np.divide(N, D, out=np.full(nc, np.nan), where=D > 0)
    estratos: dict[str, list[int]] = {}
    for k in keys:
        estratos.setdefault(k.split("\t", 1)[0], []).append(pos[k])
    rng = np.random.Generator(np.random.PCG64(seed))
    boot = np.full((reps, nc), np.nan)
    for start in range(0, reps, 50):
        size = min(50, reps - start)
        mult = np.zeros((size, nk))
        for h in sorted(estratos):
            ix = np.asarray(estratos[h], dtype=int)
            draws = rng.integers(0, len(ix), size=(size, len(ix)))
            for r in range(size):
                mult[r] += np.bincount(ix[draws[r]], minlength=nk)
        Db = mult @ den
        boot[start:start + size] = np.divide(mult @ num, Db, out=np.full_like(Db, np.nan), where=Db > 0)
    out = {}
    idx = {c[0]: j for j, c in enumerate(celdas)}

    def emite(rid, p, b, n):
        v = np.isfinite(b)
        if np.isfinite(p) and v.sum() > 0:
            lo, hi = np.percentile(b[v], [2.5, 97.5])
            out[f"{rid}-P"], out[f"{rid}-IC95-INF"], out[f"{rid}-IC95-SUP"] = float(p), float(lo), float(hi)
        else:
            out[f"{rid}-P"] = out[f"{rid}-IC95-INF"] = out[f"{rid}-IC95-SUP"] = None
        out[f"{rid}-N"] = int(n)

    for j, (rid, _, _) in enumerate(celdas):
        emite(rid, punto[j], boot[:, j], cnt[j])
    for dif in difs:
        rid, a, b = dif[:3]
        ja, jb = idx[a], idx[b]
        if len(dif) > 3 and dif[3] == "razon":           # a/b en la misma réplica
            with np.errstate(divide="ignore", invalid="ignore"):
                emite(rid, punto[ja] / punto[jb], boot[:, ja] / boot[:, jb], min(cnt[ja], cnt[jb]))
        elif len(dif) > 3 and dif[3] == "brecha":          # 1 − a/b en la misma réplica
            with np.errstate(divide="ignore", invalid="ignore"):
                emite(rid, 1 - punto[ja] / punto[jb], 1 - boot[:, ja] / boot[:, jb], min(cnt[ja], cnt[jb]))
        else:
            emite(rid, punto[ja] - punto[jb], boot[:, ja] - boot[:, jb], min(cnt[ja], cnt[jb]))
    diseno = {"N-ESTRATOS": len(estratos), "N-UPM": nk,
              "N-ESTRATOS-UPM-UNICA": sum(1 for v in estratos.values() if len(v) == 1)}
    return out, diseno





def medir(inputs, contrato):
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    ruta = inputs[PAYLOAD]["ruta_absoluta"]
    m, v = _lee(ruta, "tmodulo.csv", COLS_M), _lee(ruta, "tvar_crea.csv", COLS_V)
    diag = {"FILAS-TMODULO": len(m), "LLAVEMOD-DUPLICADAS": int(v["LLAVEMOD"].duplicated().sum())}
    d = m.merge(v.drop_duplicates("LLAVEMOD"), on="LLAVEMOD", how="left", indicator=True)
    diag["SIN-PAREJA-TVAR"] = int(d["_merge"].ne("both").sum())
    d["_w"] = pd.to_numeric(d["FAC_PER"], errors="coerce")
    d["_est"], d["_upm"] = d["EST_DIS"].str.strip(), d["UPM_DIS"].str.strip()
    sx = _code(d["SEXO"])
    muj, hom = sx.eq("2"), sx.eq("1")
    ed = pd.to_numeric(d["EDAD_V"], errors="coerce")
    tl = _code(d["TLOC"])
    rural, urbano = tl.eq("4"), tl.isin(["1", "2", "3"])
    es = _code(d["ESCOLARIDAD"].fillna(""))
    tnr, cuid = _num(d["TRAB_NO_REM_VOL"].fillna("")), _num(d["TRAB_NO_REM_CON_CP"].fillna(""))
    esp, may = _num(d["CUID_ESP_INT_HOG_CON_CP"].fillna("")), _num(d["CUID_INT_60MAS_CON_CP"].fillna(""))
    valido_dep = esp.notna() & may.notna()
    dep_h = (esp.fillna(0) + may.fillna(0)).where(valido_dep)
    cuidador_dep = valido_dep & (dep_h > 0)
    cuidador = cuid > 0
    T = pd.Series(True, index=d.index)
    C, F = [], []
    # FAM-007: proporción de mujeres entre quienes cuidan a dependientes
    C.append((f"{PFX}-CUIDADOR-DEP-MUJER-PROP", cuidador_dep, muj.astype(float)))
    C.append((f"{PFX}-CUIDADOR-TOTAL-MUJER-PROP", cuidador, muj.astype(float)))
    # FAM-008: horas semanales entre quienes cuidan, por sexo
    for s, mm in (("MUJER", muj), ("HOMBRE", hom), ("NAC", T)):
        C.append((f"{PFX}-CUID-INT-{s}", mm & cuidador, cuid))
        C.append((f"{PFX}-CUID-DEP-INT-{s}", mm & cuidador_dep, dep_h))
    # GEN-012: participación de las mujeres en el total de horas de TNR
    C.append((f"{PFX}-TNR-MEDIA-MUJERES-SOBRE-TODOS", T, tnr.where(muj, 0.0).where(tnr.notna())))
    C.append((f"{PFX}-TNR-MEDIA-TODOS", T, tnr))
    F.append((f"{PFX}-TNR-PROPORCION-HORAS-MUJERES", f"{PFX}-TNR-MEDIA-MUJERES-SOBRE-TODOS", f"{PFX}-TNR-MEDIA-TODOS", "razon"))
    # GEN-018: participación masculina en cuidados por edad, localidad y escolaridad
    part = cuidador.astype(float).where(cuid.notna())
    seg = [(f"EDAD-{e}", (ed >= lo) & (ed <= hi)) for e, lo, hi in EDADES] \
        + [("RURAL", rural), ("URBANO", urbano)] + [(f"ESC-{e}", es.isin(c)) for e, c in ESC]
    for s, mm in seg:
        C.append((f"{PFX}-HOMBRES-CUID-PART-{s}", hom & mm, part))
    F += [(f"{PFX}-HOMBRES-CUID-PART-DIF-18-29-MENOS-60MAS", f"{PFX}-HOMBRES-CUID-PART-EDAD-18-29", f"{PFX}-HOMBRES-CUID-PART-EDAD-60-MAS"),
          (f"{PFX}-HOMBRES-CUID-PART-DIF-URBANO-RURAL", f"{PFX}-HOMBRES-CUID-PART-URBANO", f"{PFX}-HOMBRES-CUID-PART-RURAL"),
          (f"{PFX}-HOMBRES-CUID-PART-DIF-SUPERIOR-BASICA", f"{PFX}-HOMBRES-CUID-PART-ESC-SUPERIOR", f"{PFX}-HOMBRES-CUID-PART-ESC-HASTA-BASICA")]
    # RURAL-038: trabajo comunitario gratuito mujer − hombre
    c6 = _code(d["P6_17_3"])
    com = pd.Series(np.where(c6.eq("1"), 1.0, np.where(c6.eq("2"), 0.0, np.nan)), index=d.index)
    for s, mm in (("MUJER", muj), ("HOMBRE", hom)):
        C.append((f"{PFX}-COMUN-PART-{s}", mm, com))
    F.append((f"{PFX}-COMUN-PART-DIF-MUJER-HOMBRE", f"{PFX}-COMUN-PART-MUJER", f"{PFX}-COMUN-PART-HOMBRE"))
    out, dis = _estima(d, C, F, reps, seed)
    diag["CUIDADORES-DEP"] = int(cuidador_dep.sum())
    diag["ESCOLARIDAD-FUERA-1-5"] = int((~es.isin(["1", "2", "3", "4", "5"])).sum())
    for k, x in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(x)
    return out
