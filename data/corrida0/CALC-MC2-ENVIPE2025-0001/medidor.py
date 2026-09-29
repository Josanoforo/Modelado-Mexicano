#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENVIPE 2025 · CALC-MC2-ENVIPE2025-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENVIPE 2025 (delitos de 2024, módulo de
victimización; ola abierta) y ENVIPE 2024 (percepción, ola vista) para las
afirmaciones del mapa v1.1 sin RESULT: cifra negra y denuncia (delito,
FAC_DEL), extorsión por llamada telefónica, preocupaciones (AP4_2), espacios
inseguros (AP4_4), dejó de salir de noche (AP4_10_01) y percepción de
inseguridad en el estado para Sinaloa 2024→2025 (AP4_3_3). ENVIPE 2026 está
RESERVADA y no es input. Contrato humano:
forense/prereg-caja/MC2-ENVIPE2025-spec-v1_0.md.

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor escalar}.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

P25 = "envipe2025_csv"
P24 = "envipe2024_csv"
PFX = "RESULT-MC2-ENVIPE2025"

DIS = ["EST_DIS", "UPM_DIS", "DOMINIO"]
COLS_DEL = DIS + ["FAC_DEL", "SEXO", "BPCOD", "BP1_20", "BP1_21", "BP1_24", "BP1_5A_2"]
COLS_PER25 = DIS + ["FAC_ELE", "SEXO", "EDAD", "CVE_ENT", "AP4_3_3"]
AP42 = [f"AP4_2_{i:02d}" for i in range(1, 14)] + ["AP4_2_99"]
AP44 = {"CALLE": "AP4_4_03", "BANCO": "AP4_4_07", "CAJERO": "AP4_4_08", "TRANSPORTE": "AP4_4_09",
        "CARRETERA": "AP4_4_11"}
COLS_PER24 = DIS + ["FAC_ELE", "SEXO", "EDAD", "CVE_ENT", "AP4_3_3", "AP4_10_01"] + AP42 + list(AP44.values())
PREOC = {"POBREZA": "01", "DESEMPLEO": "02", "NARCOTRAFICO": "03", "PRECIOS": "04", "INSEGURIDAD": "05",
         "DESASTRES": "06", "AGUA": "07", "CORRUPCION": "08", "EDUCACION": "09", "SALUD": "10",
         "IMPUNIDAD": "11"}
EDADES = [("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97)]
SINALOA = "25"
EXTORSION = "9"


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara (miembro/columna ausente)."""


# ── lectura (fin de línea \r solo en estos CSV; se normaliza antes de parsear) ─
def _lee(ruta: str, tabla: str, cols: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as zf:
        n = [x for x in zf.namelist() if x.lower().endswith(f"conjunto_de_datos_{tabla}.csv")]
        if len(n) != 1:
            raise ReservaRota(f"miembro no único: {tabla}: {n}")
        buf = zf.read(n[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = buf.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ReservaRota(f"codificación no reconocida: {tabla}")
    del buf
    txt = txt.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    quiero = set(cols)
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: c.strip().strip('"') in quiero)
    d.columns = [c.strip().strip('"') for c in d.columns]
    faltan = sorted(quiero - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes en {tabla}: {faltan}")
    return d.apply(lambda s: s.astype(str).str.strip().str.strip('"'))


def _c(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _bin(s: pd.Series, si: set, no: set) -> pd.Series:
    c = _c(s)
    return pd.Series(np.where(c.isin(si), 1.0, np.where(c.isin(no), 0.0, np.nan)), index=s.index)


def _diseno(d: pd.DataFrame, fac: str, ola: str) -> pd.DataFrame:
    d["_w"] = pd.to_numeric(d[fac], errors="coerce")
    d["_est"] = ola + "|" + d["EST_DIS"]            # estratos de olas distintas nunca se mezclan
    d["_upm"] = d["UPM_DIS"]
    dom = d["DOMINIO"].str.upper()
    d["_dom_u"], d["_dom_c"], d["_dom_r"] = dom.eq("U"), dom.eq("C"), dom.eq("R")
    sx = _c(d["SEXO"])
    d["_hombre"], d["_mujer"] = sx.eq("1"), sx.eq("2")
    d["_ola"] = ola
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


# ── delitos 2024 (ENVIPE 2025, módulo de victimización) ───────────────────
def frame_del(ruta: str) -> tuple[pd.DataFrame, dict]:
    d = _diseno(_lee(ruta, "tmod_vic_envipe2025", COLS_DEL), "FAC_DEL", "2025")
    b20 = _c(d["BP1_20"])
    valido = b20.isin(["1", "2"])
    den = b20.eq("1") | _c(d["BP1_21"]).eq("1")
    carpeta = _c(d["BP1_24"]).eq("1")
    d["DENUNCIA"] = den.astype(float).where(valido)
    d["CARPETA-DADA-DENUNCIA"] = carpeta.astype(float).where(valido & den)
    d["CIFRA-NEGRA"] = (~(den & carpeta)).astype(float).where(valido)
    ext = _c(d["BPCOD"]).eq(EXTORSION)
    d["_ext"] = ext
    d["EXT-TELEFONICA"] = _bin(d["BP1_5A_2"], {"1"}, {"0"}).where(ext)
    diag = {"FILAS": len(d), "DENUNCIA-SIN-BP1_20-VALIDO": int((~valido).sum()), "EXTORSIONES": int(ext.sum()),
            "N-SIN-PONDERADOR": int((~(d["_w"] > 0)).sum())}
    return d, diag


def celdas_del(d: pd.DataFrame) -> tuple[list, list]:
    T = pd.Series(True, index=d.index)
    seg = [("NAC", T), ("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"]),
           ("DOM-U", d["_dom_u"]), ("DOM-C", d["_dom_c"]), ("DOM-R", d["_dom_r"])]
    C = []
    for ind in ("CIFRA-NEGRA", "DENUNCIA", "CARPETA-DADA-DENUNCIA"):
        for s, m in seg:
            C.append((f"{PFX}-DEL-{ind}-{s}", m, d[ind]))
    for s, m in seg[:3]:
        C.append((f"{PFX}-DEL-EXT-TELEFONICA-{s}", m, d["EXT-TELEFONICA"]))
    return C, []


# ── personas 18+: ENVIPE 2024 (percepción) y ENVIPE 2025 (AP4_3_3) ─────────
def _edades(d: pd.DataFrame) -> None:
    ed = pd.to_numeric(d["EDAD"], errors="coerce")
    for et, lo, hi in EDADES:
        d[f"_edad_{et}"] = (ed >= lo) & (ed <= hi)


def frame_per(r24: str, r25: str) -> tuple[pd.DataFrame, dict]:
    a = _diseno(_lee(r24, "tper_vic1_envipe2024", COLS_PER24), "FAC_ELE", "2024")
    b = _diseno(_lee(r25, "tper_vic1_envipe2025", COLS_PER25), "FAC_ELE", "2025")
    d = pd.concat([a, b], ignore_index=True, sort=False)
    _edades(d)
    o24, o25 = d["_ola"].eq("2024"), d["_ola"].eq("2025")
    d["_o24"], d["_o25"] = o24, o25
    d["_sinaloa"] = _c(d["CVE_ENT"]).eq(SINALOA)
    d["EDO-INSEGURO"] = _bin(d["AP4_3_3"], {"2"}, {"1"})
    d["DEJO-SALIR-NOCHE"] = _bin(d["AP4_10_01"].fillna(""), {"1"}, {"2"}).where(o24)
    contesto = o24 & _c(d["AP4_2_99"].fillna("")).ne("1")
    for k, cod in PREOC.items():
        d[f"PREOC-{k}"] = _c(d[f"AP4_2_{cod}"].fillna("")).eq("1").astype(float).where(contesto)
    for k, col in AP44.items():
        d[f"INSEGURO-{k}"] = _bin(d[col].fillna(""), {"2"}, {"1"}).where(o24)
    diag = {"FILAS-2024": int(o24.sum()), "FILAS-2025": int(o25.sum()),
            "PREOC-NO-CONTESTO-2024": int((o24 & ~contesto).sum()),
            "SINALOA-2024": int((o24 & d["_sinaloa"]).sum()), "SINALOA-2025": int((o25 & d["_sinaloa"]).sum())}
    return d, diag


def celdas_per(d: pd.DataFrame) -> tuple[list, list]:
    C, F = [], []
    for ola, m0 in (("2024", d["_o24"]), ("2025", d["_o25"])):
        seg = [("NAC", m0), ("SINALOA", m0 & d["_sinaloa"])]
        if ola == "2025":
            seg += [("HOMBRE", m0 & d["_hombre"]), ("MUJER", m0 & d["_mujer"]),
                    ("DOM-U", m0 & d["_dom_u"]), ("DOM-C", m0 & d["_dom_c"]), ("DOM-R", m0 & d["_dom_r"])] \
                + [(f"EDAD-{e}", m0 & d[f"_edad_{e}"]) for e, _, _ in EDADES]
        for s, m in seg:
            C.append((f"{PFX}-EDO-INSEGURO-{ola}-{s}", m, d["EDO-INSEGURO"]))
    F.append((f"{PFX}-EDO-INSEGURO-SINALOA-DIF-2025-2024",
              f"{PFX}-EDO-INSEGURO-2025-SINALOA", f"{PFX}-EDO-INSEGURO-2024-SINALOA"))
    o = d["_o24"]
    seg24 = [("NAC", o), ("HOMBRE", o & d["_hombre"]), ("MUJER", o & d["_mujer"]),
             ("DOM-U", o & d["_dom_u"]), ("DOM-C", o & d["_dom_c"]), ("DOM-R", o & d["_dom_r"])] \
        + [(f"EDAD-{e}", o & d[f"_edad_{e}"]) for e, _, _ in EDADES]
    ind24 = ["DEJO-SALIR-NOCHE"] + [f"PREOC-{k}" for k in PREOC] + [f"INSEGURO-{k}" for k in AP44]
    for ind in ind24:
        for s, m in seg24:
            C.append((f"{PFX}-{ind}-2024-{s}", m, d[ind]))
    return C, F


def medir(inputs: dict, contrato: dict) -> dict:
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    out = {}
    d, diag = frame_del(inputs[P25]["ruta_absoluta"])
    C, F = celdas_del(d)
    r, dis = _estima(d, C, F, reps, seed)
    out.update(r)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-DEL-{k}"] = int(v)
    del d
    d, diag = frame_per(inputs[P24]["ruta_absoluta"], inputs[P25]["ruta_absoluta"])
    C, F = celdas_per(d)
    r, dis = _estima(d, C, F, reps, seed)
    out.update(r)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-PER-{k}"] = int(v)
    return out
