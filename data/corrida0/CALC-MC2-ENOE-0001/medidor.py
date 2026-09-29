#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENOE · CALC-MC2-ENOE-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENOE (SDEMT, población de 15 a 98 años
residente, r_def = 00, c_res ∈ {1, 3}) en olas VISTAS: 2025T4 (participación por
sexo, brecha de ingreso mensual por sexo, peso de menores de 25 en la población
ocupada) y 2023T3 (estado conyugal). 2026T1 y 2026T2 están RESERVADAS y no son
input. Contrato humano: forense/prereg-caja/MC2-ENOE-spec-v1_0.md.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

P25 = "enoe_2025_4t_microdatos"
P23 = "enoe_2023_3t_microdatos"
MIEMBRO = {P25: "ENOE_SDEMT425.csv", P23: "ENOE_SDEMT323.csv"}
PFX = "RESULT-MC2-ENOE"
COLS = ["r_def", "c_res", "eda", "sex", "e_con", "clase1", "clase2", "ingocup", "fac_tri", "est_d_tri", "upm"]
ING_NE = 999998                           # ingocup ≥ 999998 = no especificado (fuera)
ECON = {"UNION-LIBRE": {"1"}, "CASADO": {"5"}, "SOLTERO": {"6"}, "SEPARADO-DIVORCIADO-VIUDO": {"2", "3", "4"}}


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara."""


def _lee(ruta, miembro, cols):
    with zipfile.ZipFile(ruta) as zf:
        n = [x for x in zf.namelist() if x.lower() == miembro.lower()]
        if len(n) != 1:
            raise ReservaRota(f"miembro no único: {miembro}: {n}")
        raw = zf.read(n[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    quiero = {c.lower() for c in cols}
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: c.strip().strip('"').lower() in quiero)
    d.columns = [c.strip().strip('"').lower() for c in d.columns]
    faltan = sorted(quiero - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes en {miembro}: {faltan}")
    return d


def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _frame(ruta, miembro):
    d = _lee(ruta, miembro, COLS)
    eda = pd.to_numeric(d["eda"], errors="coerce")
    u = _code(d["r_def"]).eq("0") & _code(d["c_res"]).isin(["1", "3"]) & (eda >= 15) & (eda <= 98)
    diag = {"FILAS": len(d), "UNIVERSO-15-98": int(u.sum())}
    d = d.loc[u].copy()
    d["_eda"] = eda[u]
    d["_w"] = pd.to_numeric(d["fac_tri"], errors="coerce")
    d["_est"] = d["est_d_tri"].str.strip()
    d["_upm"] = d["upm"].str.strip()
    sx = _code(d["sex"])
    d["_hombre"], d["_mujer"] = sx.eq("1"), sx.eq("2")
    return d, diag


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
        if len(dif) > 3 and dif[3] == "brecha":          # 1 − a/b en la misma réplica
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
    out = {}
    # 2025T4
    d, diag = _frame(inputs[P25]["ruta_absoluta"], MIEMBRO[P25])
    T = pd.Series(True, index=d.index)
    c1 = _code(d["clase1"])
    pea = pd.Series(np.where(c1.eq("1"), 1.0, np.where(c1.eq("2"), 0.0, np.nan)), index=d.index)
    ocup = _code(d["clase2"]).eq("1")
    ing = pd.to_numeric(d["ingocup"], errors="coerce")
    ing_ok = ocup & (ing > 0) & (ing < ING_NE)
    menor25 = ((d["_eda"] >= 15) & (d["_eda"] <= 24)).astype(float).where(ocup)
    C = []
    for s, m in (("NAC", T), ("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"])):
        C.append((f"{PFX}-2025T4-PARTICIPA-{s}", m, pea))
        C.append((f"{PFX}-2025T4-INGRESO-MEDIO-{s}", m & ing_ok, ing.where(ing_ok)))
        C.append((f"{PFX}-2025T4-OCUPADO-MENOR25-{s}", m, menor25))
    F = [(f"{PFX}-2025T4-PARTICIPA-DIF-MUJER-HOMBRE", f"{PFX}-2025T4-PARTICIPA-MUJER", f"{PFX}-2025T4-PARTICIPA-HOMBRE"),
         (f"{PFX}-2025T4-INGRESO-BRECHA-MUJER-HOMBRE", f"{PFX}-2025T4-INGRESO-MEDIO-MUJER",
          f"{PFX}-2025T4-INGRESO-MEDIO-HOMBRE", "brecha")]
    r, dis = _estima(d, C, F, reps, seed)
    out.update(r)
    diag["OCUPADOS"] = int(ocup.sum())
    diag["OCUPADOS-SIN-INGRESO-VALIDO"] = int((ocup & ~ing_ok).sum())
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-2025T4-{k}"] = int(v)
    del d
    # 2023T3
    d, diag = _frame(inputs[P23]["ruta_absoluta"], MIEMBRO[P23])
    T = pd.Series(True, index=d.index)
    ec = _code(d["e_con"])
    valido = ec.isin(["1", "2", "3", "4", "5", "6"])
    joven = (d["_eda"] >= 15) & (d["_eda"] <= 29)
    C = []
    for k, cods in ECON.items():
        y = pd.Series(np.where(ec.isin(cods), 1.0, 0.0), index=d.index).where(valido)
        for s, m in (("15MAS", T), ("15-29", joven)):
            C.append((f"{PFX}-2023T3-ECON-{k}-{s}", m, y))
    r, dis = _estima(d, C, [], reps, seed)
    out.update(r)
    diag["ECON-NO-ESPECIFICADO"] = int((~valido).sum())
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-2023T3-{k}"] = int(v)
    return out
