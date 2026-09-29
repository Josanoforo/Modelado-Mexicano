#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENDUTIH · CALC-MC2-ENDUTIH2024-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENDUTIH 2024 (ola vista; ENDUTIH 2025 está
RESERVADA por R05 y no es input): uso de internet en 18-24, 25-54, 55-64 y 65+,
horas diarias de uso y uso diario entre usuarios, y WhatsApp entre usuarios de
redes sociales y de internet. Tabla `tic_2024_usuarios.DBF` (persona elegida de
6+), leída con el lector sellado `tests/dbfmini.py` (input de código con sha256).
Contrato humano: forense/prereg-caja/MC2-ENDUTIH2024-spec-v1_0.md.
"""
from __future__ import annotations

import importlib.util
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

PAYLOAD = "endutih2024_bd_dbf_zip"
LECTOR = "ENDUTIH-DBFMINI"
MIEMBRO = "tic_2024_usuarios.DBF"
PFX = "RESULT-MC2-ENDUTIH2024"
CAMPOS = ("EDAD", "FAC_PER", "EST_DIS", "UPM_DIS", "P7_1", "P7_3", "P7_4", "P7_15", "P7_16_6")
EDADES = [("18-24", 18, 24), ("25-54", 25, 54), ("55-64", 55, 64), ("65-MAS", 65, 96)]


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara."""


def _lector(ruta):
    s = importlib.util.spec_from_file_location("dbfmini_mc2", ruta)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _lee(ruta_zip, ruta_lector):
    L = _lector(ruta_lector)
    with zipfile.ZipFile(ruta_zip) as z:
        if MIEMBRO not in z.namelist():
            raise ReservaRota(f"miembro ausente: {MIEMBRO}")
        with tempfile.TemporaryDirectory() as t:
            p = Path(z.extract(MIEMBRO, t))
            faltan = set(CAMPOS) - {f[0] for f in L.field_names(p)}
            if faltan:
                raise ReservaRota(f"columnas ausentes {sorted(faltan)}")
            return pd.DataFrame(list(L.read_dbf(p, wanted_fields=CAMPOS)))


def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


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
    d = _lee(inputs[PAYLOAD]["ruta_absoluta"], inputs[LECTOR]["ruta_absoluta"])
    diag = {"FILAS": len(d)}
    d["_w"] = pd.to_numeric(d["FAC_PER"], errors="coerce")
    d["_est"], d["_upm"] = d["EST_DIS"].astype(str).str.strip(), d["UPM_DIS"].astype(str).str.strip()
    ed = pd.to_numeric(d["EDAD"], errors="coerce")
    p71 = _code(d["P7_1"])
    usa = p71.eq("1")
    internet = pd.Series(np.where(usa, 1.0, np.where(p71.eq("2"), 0.0, np.nan)), index=d.index)
    horas = pd.to_numeric(d["P7_4"], errors="coerce").where(usa)
    horas = horas.where((horas >= 1) & (horas <= 24))
    p73 = _code(d["P7_3"])
    diario = pd.Series(np.where(p73.eq("1"), 1.0, 0.0), index=d.index).where(usa & p73.isin(list("12345")))
    p715, p716 = _code(d["P7_15"]), _code(d["P7_16_6"])
    wa_redes = pd.Series(np.where(p716.eq("1"), 1.0, np.where(p716.eq("2"), 0.0, np.nan)), index=d.index).where(usa & p715.eq("1"))
    wa_usuarios = pd.Series(np.where(p716.eq("1"), 1.0, 0.0), index=d.index).where(usa & p715.isin(["1", "2"]))
    T = pd.Series(True, index=d.index)
    seg = [("NAC", T)] + [(f"EDAD-{e}", (ed >= lo) & (ed <= hi)) for e, lo, hi in EDADES]
    C = []
    for s, mm in seg:
        C += [(f"{PFX}-INTERNET-{s}", mm, internet), (f"{PFX}-HORAS-DIA-{s}", mm, horas),
              (f"{PFX}-USO-DIARIO-{s}", mm, diario), (f"{PFX}-WHATSAPP-USUARIOS-REDES-{s}", mm, wa_redes),
              (f"{PFX}-WHATSAPP-USUARIOS-INTERNET-{s}", mm, wa_usuarios)]
    out, dis = _estima(d, C, [], reps, seed)
    diag["USUARIOS"] = int(usa.sum())
    diag["HORAS-FUERA-1-24"] = int((usa & horas.isna()).sum())
    for k, x in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(x)
    return out
