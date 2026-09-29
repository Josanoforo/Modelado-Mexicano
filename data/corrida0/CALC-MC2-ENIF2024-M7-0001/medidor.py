#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 módulo 7 · CALC-MC2-ENIF2024-M7-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENIF 2024 (persona elegida 18+) sobre las
CUATRO columnas del módulo 7 que mesa abrió ABIERTA-PARCIAL (ADENDA-1 del
encargo; FP-260928-GEN2-MEDICION-CARRILES-2-8fdf-01 punto 2 (b)): P7_1_1,
P7_1_2, P7_2_1, P7_3_1. Toda otra columna P7_* sigue RESERVADA: `_lee` se
niega a pedirla. Contrato humano: forense/prereg-caja/MC2-ENIF2024-M7-spec-v1_0.md.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD = "enif_2024_enif_2024_bd_csv"
MIEMBRO = "TMODULO.csv"
PFX = "RESULT-MC2-ENIF2024-M7"
P7_ABIERTAS = {"P7_1_1", "P7_1_2", "P7_2_1", "P7_3_1"}
COLS = ["EDAD_V", "NIV", "SEXO", "TLOC", "REGION", "EST_DIS", "UPM_DIS", "FAC_PER"] + sorted(P7_ABIERTAS)
EDADES = [("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97)]
ESCOLARIDAD = [("HASTA-PRIMARIA", {"0", "1", "2"}), ("SECUNDARIA", {"3", "4", "5"}),
               ("MEDIA-SUPERIOR", {"6", "7"}), ("SUPERIOR", {"8", "9", "10", "11"})]
REGIONES = ["1", "2", "3", "4", "5", "6"]


class ReservaRota(RuntimeError):
    """Se pidió una columna del módulo 7 fuera de las cuatro abiertas, o falta una."""


def _lee(ruta: str, cols: list[str]) -> pd.DataFrame:
    fuera = [c for c in cols if c.upper().startswith("P7") and c.upper() not in P7_ABIERTAS]
    if fuera:
        raise ReservaRota(f"módulo 7 RESERVADO salvo {sorted(P7_ABIERTAS)}: {fuera}")
    with zipfile.ZipFile(ruta) as zf:
        n = [x for x in zf.namelist() if x.lower() == MIEMBRO.lower()]
        if len(n) != 1:
            raise ReservaRota(f"miembro no único: {n}")
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
    faltan = sorted(quiero - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes: {faltan}")
    return d


def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _cat(s, validos, objetivo):
    c = _code(s)
    return pd.Series(np.where(c.isin(objetivo), 1.0, np.where(c.isin(validos), 0.0, np.nan)), index=s.index)


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
    for rid, a, b in difs:
        ja, jb = idx[a], idx[b]
        emite(rid, punto[ja] - punto[jb], boot[:, ja] - boot[:, jb], min(cnt[ja], cnt[jb]))
    diseno = {"N-ESTRATOS": len(estratos), "N-UPM": nk,
              "N-ESTRATOS-UPM-UNICA": sum(1 for v in estratos.values() if len(v) == 1)}
    return out, diseno



def frame(ruta):
    d = _lee(ruta, COLS)
    d["_w"] = pd.to_numeric(d["FAC_PER"].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip()
    d["_upm"] = d["UPM_DIS"].str.strip()
    sx = _code(d["SEXO"])
    d["_hombre"], d["_mujer"] = sx.eq("1"), sx.eq("2")
    ed = pd.to_numeric(d["EDAD_V"].str.strip(), errors="coerce")
    for et, lo, hi in EDADES:
        d[f"_edad_{et}"] = (ed >= lo) & (ed <= hi)
    nv = _code(d["NIV"])
    for et, cods in ESCOLARIDAD:
        d[f"_esc_{et}"] = nv.isin(cods)
    tl = _code(d["TLOC"])
    d["_loc_mas"], d["_loc_menos"] = tl.isin(["1", "2"]), tl.isin(["3", "4"])
    rg = _code(d["REGION"])
    for r in REGIONES:
        d[f"_reg_{r}"] = rg.eq(r)
    V = {"1", "2", "3"}
    for tam, col in (("500-O-MENOS", "P7_1_1"), ("501-O-MAS", "P7_1_2")):
        d[f"EFECTIVO-{tam}"] = _cat(d[col], V, {"3"})
        d[f"DIGITAL-{tam}"] = _cat(d[col], V, {"1"})
        d[f"TARJETA-{tam}"] = _cat(d[col], V, {"2"})
    d["CODI-CONOCE"] = _cat(d["P7_2_1"], {"1", "2"}, {"1"})
    d["CODI-USA-SI-CONOCE"] = _cat(d["P7_3_1"], {"1", "2"}, {"1"}).where(_code(d["P7_2_1"]).eq("1"))
    d["CODI-USA-POBLACION"] = np.where(_code(d["P7_2_1"]).eq("2"), 0.0, d["CODI-USA-SI-CONOCE"])
    diag = {"FILAS-TMODULO": len(d), "P7_1_1-FUERA-1-3": int((~_code(d["P7_1_1"]).isin(V)).sum()),
            "P7_1_2-FUERA-1-3": int((~_code(d["P7_1_2"]).isin(V)).sum()),
            "N-SIN-PONDERADOR": int((~(d["_w"] > 0)).sum())}
    return d, diag


INDICADORES = [f"{k}-{t}" for t in ("500-O-MENOS", "501-O-MAS") for k in ("EFECTIVO", "DIGITAL", "TARJETA")] \
    + ["CODI-CONOCE", "CODI-USA-SI-CONOCE", "CODI-USA-POBLACION"]


def celdas(d):
    T = pd.Series(True, index=d.index)
    seg = [("NAC", T), ("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"])]
    seg += [(f"EDAD-{e}", d[f"_edad_{e}"]) for e, _, _ in EDADES]
    seg += [(f"ESC-{e}", d[f"_esc_{e}"]) for e, _ in ESCOLARIDAD]
    seg += [("LOC-15MIL-Y-MAS", d["_loc_mas"]), ("LOC-MENOS-15MIL", d["_loc_menos"])]
    seg += [(f"REGION-{r}", d[f"_reg_{r}"]) for r in REGIONES]
    C = [(f"{PFX}-{i}-{s}", m, pd.Series(d[i], index=d.index)) for i in INDICADORES for s, m in seg]
    F = [(f"{PFX}-EFECTIVO-500-O-MENOS-DIF-LOC-MENOS-MAS", f"{PFX}-EFECTIVO-500-O-MENOS-LOC-MENOS-15MIL",
          f"{PFX}-EFECTIVO-500-O-MENOS-LOC-15MIL-Y-MAS")]
    return C, F


def medir(inputs, contrato):
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    d, diag = frame(inputs[PAYLOAD]["ruta_absoluta"])
    C, F = celdas(d)
    out, dis = _estima(d, C, F, reps, seed)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(v)
    return out
