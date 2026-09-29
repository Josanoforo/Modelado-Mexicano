#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENSANUT 2024 · CALC-MC2-ENSANUT2024-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENSANUT 2024 (ola vista; 2025 RESERVADA y
no es input) para la regla RG-41d71be87f (deferencia al experto según acceso)
y las afirmaciones SALUD-032 y SALMEN-032 del mapa v1.1:
  · integrantes (todas las edades): necesidad de salud en 3 meses (h0401),
    búsqueda de atención (h0404) y motivo de no búsqueda (H0405A-C);
  · adultos 20+: diabetes diagnosticada (a0301), tratamiento (a0307), gasto
    mensual en tratamiento (a0310a), suspensión (a0313) y su causa (a0314).
Contrato humano: forense/prereg-caja/MC2-ENSANUT2024-spec-v1_0.md.

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor escalar}.
"""
from __future__ import annotations

import os
import tempfile
import zipfile

import numpy as np
import pandas as pd

P_INTE = "integrantes_ensanut2024_w_icb_stata_stata__v2026_09_01"
P_ADUL = "adultos_ensanut2024_w_stata_stata__v2026_09_01"
PFX = "RESULT-MC2-ENSANUT2024"

DISENO = ["ponde_f", "est_sel", "upm", "estrato"]
COLS_INTE = DISENO + ["h0302", "h0303", "h0401", "h0402", "h0404", "H0405A", "H0405B", "H0405C"]
COLS_ADUL = DISENO + ["sexo", "edad", "a0301", "a0307", "a0310a", "a0313", "a0314"]

EDADES_INTE = [("0-19", 0, 19), ("20-59", 20, 59), ("60-MAS", 60, 130)]
SALUD_MENTAL = {47, 48, 50, 59}          # h0402: depresión, ansiedad, estrés, otro de salud mental
ACCESO = {2, 3, 4}                        # H0405: no hay dónde, muy lejos, caro/no tenía dinero
NO_GRAVE = {1}                            # H0405: decidió que no era necesario (no tan grave)
ECON_ACCESO = {5, 6, 7, 10}               # a0314: no surtieron, no encontró, sin dinero, se terminó
A0314_VALIDOS = {1, 2, 4, 5, 6, 7, 8, 9, 10}
MONTO_NS = 99999                          # a0310a ≥ este valor = no sabe/no responde (fuera)


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara (miembro/columna ausente)."""


# ── lectura ────────────────────────────────────────────────────────────────
def _lee_dta(ruta: str, cols: list[str]) -> pd.DataFrame:
    import pyreadstat
    with zipfile.ZipFile(ruta) as zf:
        dtas = [n for n in zf.namelist() if n.lower().endswith(".dta")]
        if len(dtas) != 1:
            raise ReservaRota(f"miembro .dta no único: {dtas}")
        with tempfile.TemporaryDirectory() as t:
            p = zf.extract(dtas[0], t)
            _, meta = pyreadstat.read_dta(p, metadataonly=True)
            por_min = {c.lower(): c for c in meta.column_names}
            faltan = [c for c in cols if c.lower() not in por_min]
            if faltan:
                raise ReservaRota(f"variables ausentes en {dtas[0]}: {faltan}")
            d, _ = pyreadstat.read_dta(p, usecols=[por_min[c.lower()] for c in cols],
                                       apply_value_formats=False)
            os.remove(p)
    d.columns = [c.lower() for c in d.columns]
    return d


def _n(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def _bin(s: pd.Series, si: set, no: set) -> pd.Series:
    x = _n(s)
    return pd.Series(np.where(x.isin(si), 1.0, np.where(x.isin(no), 0.0, np.nan)), index=s.index)


def _diseno(d: pd.DataFrame) -> pd.DataFrame:
    d["_w"] = _n(d["ponde_f"])
    d["_est"] = d["est_sel"].astype(str).str.strip().replace({"nan": ""})
    d["_upm"] = d["upm"].astype(str).str.strip().replace({"nan": ""})
    e = _n(d["estrato"])
    d["_rural"], d["_urbano"], d["_metro"] = e.eq(1), e.eq(2), e.eq(3)
    d["_norural"] = e.isin([2, 3])
    return d


# ── estimador: razones ponderadas con bootstrap de UPM dentro de estrato ───
def _estima(d: pd.DataFrame, celdas: list[tuple], difs: list[tuple], reps: int, seed: int) -> tuple[dict, dict]:
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
    for rid, a, b in difs:
        ja, jb = idx[a], idx[b]
        emite(rid, punto[ja] - punto[jb], boot[:, ja] - boot[:, jb], min(cnt[ja], cnt[jb]))
    diseno = {"N-ESTRATOS": len(estratos), "N-UPM": nk,
              "N-ESTRATOS-UPM-UNICA": sum(1 for v in estratos.values() if len(v) == 1)}
    return out, diseno


# ── integrantes: necesidad, búsqueda, motivo de no búsqueda ───────────────
def frame_inte(ruta: str) -> tuple[pd.DataFrame, dict]:
    d = _diseno(_lee_dta(ruta, COLS_INTE))
    diag = {"FILAS": len(d)}
    nec = _n(d["h0401"]).eq(1)
    d["_nec"] = nec
    d["_nec_mental"] = nec & _n(d["h0402"]).isin(SALUD_MENTAL)
    d["BUSCO"] = _bin(d["h0404"], {1}, {2}).where(nec)
    no_busco = nec & _n(d["h0404"]).eq(2)
    mot = pd.concat([_n(d[c]) for c in ("h0405a", "h0405b", "h0405c")], axis=1)
    valido = mot.isin(range(1, 14)).any(axis=1)          # algún motivo 01-13 (99 «no sabe» no cuenta)
    d["_no_busco_mot"] = no_busco & valido
    d["ACCESO"] = mot.isin(ACCESO).any(axis=1).astype(float).where(d["_no_busco_mot"])
    d["NO-GRAVE"] = mot.isin(NO_GRAVE).any(axis=1).astype(float).where(d["_no_busco_mot"])
    sx = _n(d["h0302"])
    d["_hombre"], d["_mujer"] = sx.eq(1), sx.eq(2)
    ed = _n(d["h0303"])
    for et, lo, hi in EDADES_INTE:
        d[f"_edad_{et}"] = (ed >= lo) & (ed <= hi)
    diag["NECESIDAD-SI"] = int(nec.sum())
    diag["NO-BUSCO"] = int(no_busco.sum())
    diag["NO-BUSCO-SIN-MOTIVO-VALIDO"] = int((no_busco & ~valido).sum())
    diag["NECESIDAD-SALUD-MENTAL"] = int(d["_nec_mental"].sum())
    return d, diag


def celdas_inte(d: pd.DataFrame) -> tuple[list, list]:
    T = pd.Series(True, index=d.index)
    est = [("NAC", T), ("RURAL", d["_rural"]), ("URBANO", d["_urbano"]), ("METRO", d["_metro"]),
           ("NORURAL", d["_norural"])]
    seg = est + [("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"])] \
        + [(f"EDAD-{e}", d[f"_edad_{e}"]) for e, _, _ in EDADES_INTE]
    C, F = [], []
    for s, m in est:
        C.append((f"{PFX}-BUSCO-{s}", m, d["BUSCO"]))
    for ind in ("ACCESO", "NO-GRAVE"):
        for s, m in seg:
            C.append((f"{PFX}-{ind}-{s}", m, d[ind]))
    for s, m in [("NAC", T), ("RURAL", d["_rural"]), ("NORURAL", d["_norural"])]:
        C.append((f"{PFX}-BUSCO-MENTAL-{s}", m & d["_nec_mental"], d["BUSCO"]))
    F.append((f"{PFX}-BUSCO-DIF-RURAL-METRO", f"{PFX}-BUSCO-RURAL", f"{PFX}-BUSCO-METRO"))
    F.append((f"{PFX}-BUSCO-DIF-RURAL-NORURAL", f"{PFX}-BUSCO-RURAL", f"{PFX}-BUSCO-NORURAL"))
    F.append((f"{PFX}-ACCESO-DIF-RURAL-METRO", f"{PFX}-ACCESO-RURAL", f"{PFX}-ACCESO-METRO"))
    F.append((f"{PFX}-ACCESO-DIF-RURAL-NORURAL", f"{PFX}-ACCESO-RURAL", f"{PFX}-ACCESO-NORURAL"))
    F.append((f"{PFX}-ACCESO-MENOS-NOGRAVE-NAC", f"{PFX}-ACCESO-NAC", f"{PFX}-NO-GRAVE-NAC"))
    F.append((f"{PFX}-BUSCO-MENTAL-DIF-RURAL-NORURAL", f"{PFX}-BUSCO-MENTAL-RURAL", f"{PFX}-BUSCO-MENTAL-NORURAL"))
    return C, F


# ── adultos: diabetes, gasto, suspensión y causa ──────────────────────────
def frame_adul(ruta: str) -> tuple[pd.DataFrame, dict]:
    d = _diseno(_lee_dta(ruta, COLS_ADUL))
    diag = {"FILAS": len(d)}
    ed = _n(d["edad"])
    dm = _n(d["a0301"]).eq(1) & (ed >= 20)
    trat = dm & _n(d["a0307"]).isin([1, 2, 3])
    monto = _n(d["a0310a"])
    mval = monto.notna() & (monto >= 0) & (monto < MONTO_NS)
    d["_paga"], d["_nopaga"] = trat & mval & (monto > 0), trat & mval & monto.eq(0)
    d["SUSPENDE"] = _bin(d["a0313"], {1}, {2}).where(trat)
    c = _n(d["a0314"])
    susp = trat & _n(d["a0313"]).eq(1) & c.isin(A0314_VALIDOS)
    d["_susp"] = susp
    d["ECON-ACCESO"] = c.isin(ECON_ACCESO).astype(float).where(susp)
    sx = _n(d["sexo"])
    d["_hombre"], d["_mujer"] = sx.eq(1), sx.eq(2)
    d["_trat"] = trat
    diag["DIABETES-20MAS"] = int(dm.sum())
    diag["CON-TRATAMIENTO"] = int(trat.sum())
    diag["MONTO-FUERA"] = int((trat & ~mval).sum())
    diag["SUSPENDE-CON-CAUSA"] = int(susp.sum())
    return d, diag


def celdas_adul(d: pd.DataFrame) -> tuple[list, list]:
    T = pd.Series(True, index=d.index)
    C, F = [], []
    for s, m in [("NAC", T), ("PAGA", d["_paga"]), ("NOPAGA", d["_nopaga"]), ("RURAL", d["_rural"]),
                 ("NORURAL", d["_norural"]), ("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"])]:
        C.append((f"{PFX}-DM-SUSPENDE-{s}", m, d["SUSPENDE"]))
    for s, m in [("NAC", T), ("RURAL", d["_rural"]), ("NORURAL", d["_norural"])]:
        C.append((f"{PFX}-DM-ECON-ACCESO-{s}", m, d["ECON-ACCESO"]))
    C.append((f"{PFX}-DM-PAGA-NAC", d["_trat"], d["_paga"].astype(float).where(d["_paga"] | d["_nopaga"])))
    F.append((f"{PFX}-DM-SUSPENDE-DIF-PAGA-NOPAGA", f"{PFX}-DM-SUSPENDE-PAGA", f"{PFX}-DM-SUSPENDE-NOPAGA"))
    return C, F


def medir(inputs: dict, contrato: dict) -> dict:
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    out = {}
    for pid, fr, ce, tag in ((P_INTE, frame_inte, celdas_inte, "INTE"), (P_ADUL, frame_adul, celdas_adul, "ADUL")):
        d, diag = fr(inputs[pid]["ruta_absoluta"])
        C, F = ce(d)
        r, dis = _estima(d, C, F, reps, seed)
        out.update(r)
        for k, v in {**diag, **dis}.items():
            out[f"{PFX}-DIAG-{tag}-{k}"] = int(v)
        del d
    return out
