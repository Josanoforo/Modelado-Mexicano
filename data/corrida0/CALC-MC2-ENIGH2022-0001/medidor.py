#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIGH · CALC-MC2-ENIGH2022-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENIGH 2022 (Nueva Serie, ola VISTA;
concentradohogar, unidad hogar, factor de expansión `factor`) para
afirmaciones que citan ENIGH 2024 —ola RESERVADA salvo seis columnas AMAI y no
input aquí (regla de mesa, ADENDA-2: se miden olas vistas y se declara)—:
brechas regionales de gasto e ingreso, composición del decil I, participación
del decil X y Gini con y sin transferencias.
Contrato humano: forense/prereg-caja/MC2-ENIGH2022-spec-v1_0.md.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD = "enigh2022_nc_csv"
MIEMBRO = "conjunto_de_datos_concentradohogar_enigh2022_ns.csv"
PFX = "RESULT-MC2-ENIGH2022"
COLS = ["folioviv", "foliohog", "ubica_geo", "est_dis", "upm", "factor", "ing_cor", "transfer", "gasto_mon", "alimentos"]
ENT = {"CDMX": "09", "CHIAPAS": "07", "NUEVO-LEON": "19"}


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara."""


def _lee(ruta):
    with zipfile.ZipFile(ruta) as zf:
        n = [x for x in zf.namelist() if x.endswith(MIEMBRO)]
        if len(n) != 1:
            raise ReservaRota(f"miembro no único: {n}")
        raw = zf.read(n[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    txt = txt.replace("\r\n", "\n").replace("\r", "\n")
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: c.strip().strip('"').lower() in set(COLS))
    d.columns = [c.strip().strip('"').lower() for c in d.columns]
    faltan = sorted(set(COLS) - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes: {faltan}")
    return d


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




def deciles(y, w):
    """Decil (1..10) de hogares por ingreso corriente, con cortes ponderados de la muestra completa."""
    o = np.argsort(y, kind="mergesort")
    cw = np.cumsum(w[o]) / w.sum()
    dec = np.empty(len(y), dtype=int)
    dec[o] = np.minimum(np.floor(cw * 10 - 1e-12).astype(int) + 1, 10)
    return dec


def _gini(ys, ws):
    """Gini ponderado; ys ordenado ascendente; ws matriz (r, n) o vector."""
    ws = np.atleast_2d(ws)
    wy = ws * ys
    W, Y = ws.sum(1, keepdims=True), wy.sum(1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        L = np.where(Y > 0, np.cumsum(wy, 1) / np.where(Y > 0, Y, 1), np.nan)
    Lprev = np.concatenate([np.zeros((ws.shape[0], 1)), L[:, :-1]], 1)
    return 1 - ((ws / W) * (L + Lprev)).sum(1)


def gini_boot(d, y, reps, seed):
    ok = np.isfinite(y) & (d["_w"].to_numpy() > 0)
    y, w = y[ok], d["_w"].to_numpy()[ok]
    key = (d["_est"] + "\t" + d["_upm"]).to_numpy()[ok]
    keys = sorted(set(key))
    pos = {k: i for i, k in enumerate(keys)}
    kidx = np.array([pos[k] for k in key])
    o = np.argsort(y, kind="mergesort")
    ys, ws, kidx = y[o], w[o], kidx[o]
    punto = float(_gini(ys, ws)[0])
    estr = {}
    for k in keys:
        estr.setdefault(k.split("\t", 1)[0], []).append(pos[k])
    rng = np.random.Generator(np.random.PCG64(seed))
    b = np.empty(reps)
    for start in range(0, reps, 50):
        size = min(50, reps - start)
        mult = np.zeros((size, len(keys)))
        for h in sorted(estr):
            ix = np.asarray(estr[h], dtype=int)
            dr = rng.integers(0, len(ix), size=(size, len(ix)))
            for r in range(size):
                mult[r] += np.bincount(ix[dr[r]], minlength=len(keys))
        b[start:start + size] = _gini(ys, mult[:, kidx] * ws)
    b = b[np.isfinite(b)]
    if not np.isfinite(punto) or not len(b):
        return None, None, None, int(ok.sum())                # ingreso total nulo: no estimable
    lo, hi = np.percentile(b, [2.5, 97.5])
    return punto, float(lo), float(hi), int(ok.sum())


def medir(inputs, contrato):
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    d = _lee(inputs[PAYLOAD]["ruta_absoluta"])
    diag = {"FILAS": len(d), "LLAVE-HOGAR-DUPLICADA": int(d.duplicated(["folioviv", "foliohog"]).sum())}
    for c in ("ing_cor", "transfer", "gasto_mon", "alimentos", "factor"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["_w"] = d["factor"]
    d["_est"] = d["est_dis"].str.strip()
    d["_upm"] = d["upm"].str.strip()
    ent = d["ubica_geo"].str.strip().str.zfill(5).str[:2]
    ing = d["ing_cor"]
    d["_dec"] = deciles(ing.to_numpy(float), d["_w"].to_numpy(float))
    T = pd.Series(True, index=d.index)
    C, F = [], []
    for k, e in ENT.items():
        m = ent.eq(e)
        C.append((f"{PFX}-GASTO-MON-MENSUAL-{k}", m, d["gasto_mon"] / 3))
        C.append((f"{PFX}-ING-COR-TRIM-{k}", m, ing))
    F.append((f"{PFX}-GASTO-RAZON-CDMX-CHIAPAS", f"{PFX}-GASTO-MON-MENSUAL-CDMX", f"{PFX}-GASTO-MON-MENSUAL-CHIAPAS", "razon"))
    F.append((f"{PFX}-ING-RAZON-NUEVO-LEON-CHIAPAS", f"{PFX}-ING-COR-TRIM-NUEVO-LEON", f"{PFX}-ING-COR-TRIM-CHIAPAS", "razon"))
    d1 = pd.Series(d["_dec"] == 1, index=d.index)
    C += [(f"{PFX}-D1-ALIMENTOS-MEDIA", d1, d["alimentos"]), (f"{PFX}-D1-TRANSFER-MEDIA", d1, d["transfer"]),
          (f"{PFX}-D1-ING-MEDIA", d1, ing), (f"{PFX}-ING-X-MEDIA-TODOS", T, ing.where(d["_dec"] == 10, 0.0)),
          (f"{PFX}-ING-MEDIA-TODOS", T, ing)]
    F += [(f"{PFX}-D1-ALIMENTOS-SOBRE-INGRESO", f"{PFX}-D1-ALIMENTOS-MEDIA", f"{PFX}-D1-ING-MEDIA", "razon"),
          (f"{PFX}-D1-TRANSFER-SOBRE-INGRESO", f"{PFX}-D1-TRANSFER-MEDIA", f"{PFX}-D1-ING-MEDIA", "razon"),
          (f"{PFX}-D10-PARTICIPACION-INGRESO", f"{PFX}-ING-X-MEDIA-TODOS", f"{PFX}-ING-MEDIA-TODOS", "razon")]
    out, dis = _estima(d, C, F, reps, seed)
    for nom, y in (("GINI-CON-TRANSFERENCIAS", ing.to_numpy(float)),
                   ("GINI-SIN-TRANSFERENCIAS", (ing - d["transfer"]).clip(lower=0).to_numpy(float))):
        p, lo, hi, n = gini_boot(d, y, reps, seed + 1)
        out[f"{PFX}-{nom}-P"], out[f"{PFX}-{nom}-IC95-INF"], out[f"{PFX}-{nom}-IC95-SUP"] = p, lo, hi
        out[f"{PFX}-{nom}-N"] = n
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(v)
    return out
