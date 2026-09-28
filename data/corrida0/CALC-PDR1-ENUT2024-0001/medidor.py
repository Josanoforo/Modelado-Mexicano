#!/usr/bin/env python3
"""GEN2-PISOS-DOMINIOS-Y-REGLAS-1 · pieza P-ENUT2024 · CALC-PDR1-ENUT2024-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENUT 2024 (y ENUT 2019 como ola previa
sólo para el trabajo comunitario gratuito, RURAL-002) para las afirmaciones
ASTRA5-U0-TIME-002, -TIME-020, -VEJEZ-009, -RURAL-002, -VEJEZ-032(a) y la
regla RG-3920de961d. Contrato humano:
forense/prereg-caja/PDR1-ENUT2024-spec-v1_0.md (manda sobre este código).

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor escalar}.
Todos los RESULT son escalares (flotante/entero); ningún texto > 1024 bytes.
"""
from __future__ import annotations

import zipfile

import numpy as np
import pandas as pd

P24 = "enut2024_bd_csv"
P19 = "enut2019_bd_csv"
PFX = "RESULT-PDR1-ENUT2024"
EDADES = [("12-17", 12, 17), ("18-29", 18, 29), ("30-39", 30, 39), ("40-59", 40, 59), ("60-MAS", 60, 97)]

# ítems (sufijos) de los bloques del cuestionario 2024 (FD TMODULO)
CONV_ITEMS = ["1", "2", "3", "4"]            # 6.21 convivencia (filas FD 1342-1381)
MED_ITEMS = ["1", "2", "3", "4", "5", "6"]   # 6.22 medios / entretenimiento (filas FD 1382-1441)

COLS_M24 = (["LLAVEMOD", "SEXO", "EDAD_V", "P4_1", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER",
             "P6_17_3"]
            + [f"P6_17A_3_{k}" for k in (1, 2, 3, 4)]
            + [f"P6_21_{i}" for i in CONV_ITEMS]
            + [f"P6_21A_{i}_{k}" for i in CONV_ITEMS for k in (1, 2, 3, 4)]
            + [f"P6_22_{i}" for i in MED_ITEMS]
            + [f"P6_22A_{i}_{k}" for i in MED_ITEMS for k in (1, 2, 3, 4)])
COLS_V24 = ["LLAVEMOD", "TRAB_NO_REM_VOL", "TRAB_NO_REM_CON_CP", "ACTIV_PROD_CON_CP",
            "MENOR10", "COND_IND"]
COLS_M19 = ["SEXO", "EDAD_V", "P4_1", "P6_17_2", "TLOC", "EST_DIS", "UPM_DIS", "FAC_PER"]


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara (miembro/columna ausente)."""


# ── lectura ────────────────────────────────────────────────────────────────
def _lee(ruta: str, miembro: str, cols: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as zf:
        nombres = [n for n in zf.namelist() if n.lower() == miembro.lower()]
        if len(nombres) != 1:
            raise ReservaRota(f"miembro no único: {miembro}: {nombres}")
        raw = zf.read(nombres[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ReservaRota(f"codificación no reconocida: {miembro}")
    del raw
    import io
    quiero = {c.upper() for c in cols}
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: str(c).strip().upper() in quiero)
    d.columns = [str(c).strip().upper() for c in d.columns]
    faltan = sorted(quiero - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes en {miembro}: {faltan}")
    return d


def _code(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _num0(s: pd.Series) -> pd.Series:
    """Tiempo de ítem: blanco ('blanco por secuencia') o no numérico = 0."""
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce").fillna(0.0)


def _numnan(s: pd.Series) -> pd.Series:
    """Variable creada de tvar_crea: blanco/no numérico/negativo = inválido (NaN)."""
    x = pd.to_numeric(s.astype(str).str.strip(), errors="coerce")
    return x.where(x >= 0)


def _horas_bloque(d: pd.DataFrame, bloque: str, items: list[str]) -> tuple[pd.Series, pd.Series]:
    """(horas semanales sumadas, participó = algún ítem 'Sí' (=1))."""
    h = pd.Series(0.0, index=d.index)
    part = pd.Series(False, index=d.index)
    for i in items:
        pref = f"P{bloque.replace('.', '_')}A_{i}_"
        h = h + _num0(d[pref + "1"]) + _num0(d[pref + "2"]) / 60.0 \
              + _num0(d[pref + "3"]) + _num0(d[pref + "4"]) / 60.0
        part = part | _code(d[f"P{bloque.replace('.', '_')}_{i}"]).eq("1")
    return h, part


def _edad(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s.astype(str).str.strip(), errors="coerce")
    out = pd.Series(None, index=s.index, dtype="object")
    for et, lo, hi in EDADES:
        out[(x >= lo) & (x <= hi)] = et
    return out


# ── estimador: razones ponderadas con bootstrap de UPM dentro de estrato ───
def _estima(d: pd.DataFrame, celdas: list[tuple], difs: list[tuple], reps: int, seed: int) -> tuple[dict, dict]:
    """celdas: (id, mask, y). Punto = Σw·y/Σw sobre mask∧finito(y).
    difs: (id, id_a, id_b) = celda a − celda b en la MISMA réplica.
    Devuelve (resultados, diseño)."""
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


# ── frames ─────────────────────────────────────────────────────────────────
def frame_2024(ruta: str) -> tuple[pd.DataFrame, dict]:
    m = _lee(ruta, "tmodulo.csv", COLS_M24)
    v = _lee(ruta, "tvar_crea.csv", COLS_V24)
    diag = {"FILAS-TMODULO": len(m), "FILAS-TVAR-CREA": len(v)}
    m["LLAVEMOD"] = m["LLAVEMOD"].str.strip()
    v["LLAVEMOD"] = v["LLAVEMOD"].str.strip()
    diag["LLAVEMOD-DUPLICADAS"] = int(m["LLAVEMOD"].duplicated().sum() + v["LLAVEMOD"].duplicated().sum())
    v = v.drop_duplicates("LLAVEMOD")
    d = m.merge(v, on="LLAVEMOD", how="left", indicator=True)
    diag["SIN-PAREJA-TVAR"] = int(d["_merge"].ne("both").sum())
    d = d.drop(columns="_merge")
    d["_w"] = pd.to_numeric(d["FAC_PER"].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].astype(str).str.strip()
    d["_upm"] = d["UPM_DIS"].astype(str).str.strip()
    sx = _code(d["SEXO"])
    d["_mujer"], d["_hombre"] = sx.eq("2"), sx.eq("1")
    d["_edad"] = _edad(d["EDAD_V"])
    tl = _code(d["TLOC"])
    d["_rural"], d["_urbano"] = tl.eq("4"), tl.isin(["1", "2", "3"])
    d["_menor10"] = _code(d["MENOR10"].fillna("")).eq("1")
    d["_mayor10"] = ~d["_menor10"] & tl.isin(["1", "2", "3", "4"])
    hl = _code(d["P4_1"])
    d["_habl"], d["_nohabl"] = hl.eq("1"), hl.eq("2")
    ci = _code(d["COND_IND"].fillna(""))
    d["_ind"], d["_noind"] = ci.eq("1"), ci.eq("2")
    d["_tnr"] = _numnan(d["TRAB_NO_REM_VOL"].fillna(""))
    d["_cuid"] = _numnan(d["TRAB_NO_REM_CON_CP"].fillna(""))
    d["_ttt"] = _numnan(d["ACTIV_PROD_CON_CP"].fillna(""))
    d["_conv_h"], d["_conv_p"] = _horas_bloque(d, "6.21", CONV_ITEMS)
    d["_med_h"], d["_med_p"] = _horas_bloque(d, "6.22", MED_ITEMS)
    c = _code(d["P6_17_3"])
    d["_comun"] = np.where(c.eq("1"), 1.0, np.where(c.eq("2"), 0.0, np.nan))
    d["_comun_h"] = (_num0(d["P6_17A_3_1"]) + _num0(d["P6_17A_3_2"]) / 60.0
                     + _num0(d["P6_17A_3_3"]) + _num0(d["P6_17A_3_4"]) / 60.0)
    diag["TNR-INVALIDOS"] = int(d["_tnr"].isna().sum())
    diag["COMUN-FUERA-1-2"] = int(np.isnan(d["_comun"]).sum())
    diag["N-SIN-PONDERADOR"] = int((~(d["_w"] > 0)).sum())
    return d, diag


def frame_2019(ruta: str) -> tuple[pd.DataFrame, dict]:
    d = _lee(ruta, "enut_2019/TMODULO.csv", COLS_M19)
    diag = {"FILAS-TMODULO": len(d)}
    d["_w"] = pd.to_numeric(d["FAC_PER"].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].astype(str).str.strip()
    d["_upm"] = d["UPM_DIS"].astype(str).str.strip()
    tl = _code(d["TLOC"])
    d["_rural"], d["_urbano"] = tl.eq("4"), tl.isin(["1", "2", "3"])
    hl = _code(d["P4_1"])
    d["_habl"], d["_nohabl"] = hl.eq("1"), hl.eq("2")
    c = _code(d["P6_17_2"])
    d["_comun"] = np.where(c.eq("1"), 1.0, np.where(c.eq("2"), 0.0, np.nan))
    diag["COMUN-FUERA-1-2"] = int(np.isnan(d["_comun"]).sum())
    return d, diag


# ── celdas (el catálogo; los ids del spec.yaml salen de aquí) ─────────────
def celdas_2024(d: pd.DataFrame) -> tuple[list, list]:
    T = pd.Series(True, index=d.index)
    tnr, pos_tnr = d["_tnr"], d["_tnr"] > 0
    seg = [("NAC", T), ("MUJER", d["_mujer"]), ("HOMBRE", d["_hombre"])] \
        + [(f"EDAD-{e}", d["_edad"].eq(e)) for e, _, _ in EDADES] \
        + [("RURAL", d["_rural"]), ("URBANO", d["_urbano"])]
    C, F = [], []
    # TIME-002 / VEJEZ-009 / VEJEZ-032a: TRAB_NO_REM_VOL
    for s, m in seg:
        C.append((f"{PFX}-TNR-INT-{s}", m & pos_tnr, tnr))          # E(h | h>0)
        C.append((f"{PFX}-TNR-MEDIA-{s}", m, tnr))                  # E(h), ceros incluidos
        C.append((f"{PFX}-TNR-PART-{s}", m, (tnr > 0).astype(float).where(tnr.notna())))
    for s, m in [("MENOR10", d["_menor10"]), ("MAYOR10", d["_mayor10"]),
                 ("HABL", d["_habl"]), ("NOHABL", d["_nohabl"])]:
        for sx in ("MUJER", "HOMBRE"):
            C.append((f"{PFX}-TNR-INT-{s}-{sx}", m & d[f"_{sx.lower()}"] & pos_tnr, tnr))
            C.append((f"{PFX}-TNR-MEDIA-{s}-{sx}", m & d[f"_{sx.lower()}"], tnr))
    F.append((f"{PFX}-TNR-INT-BRECHA-SEXO", f"{PFX}-TNR-INT-MUJER", f"{PFX}-TNR-INT-HOMBRE"))
    F.append((f"{PFX}-TNR-MEDIA-BRECHA-SEXO", f"{PFX}-TNR-MEDIA-MUJER", f"{PFX}-TNR-MEDIA-HOMBRE"))
    for s in ("MENOR10", "MAYOR10", "HABL", "NOHABL"):
        for k in ("INT", "MEDIA"):
            F.append((f"{PFX}-TNR-{k}-BRECHA-SEXO-{s}", f"{PFX}-TNR-{k}-{s}-MUJER", f"{PFX}-TNR-{k}-{s}-HOMBRE"))
    # VEJEZ-009: participación en cuidado a integrantes del hogar (con pasivos)
    cu = (d["_cuid"] > 0).astype(float).where(d["_cuid"].notna())
    for s, m in seg[:3]:
        C.append((f"{PFX}-CUID-PART-{s}", m, cu))
    # TIME-020: convivencia (6.21), medios (6.22), tiempo total de trabajo
    for nom, h, p in (("CONV", d["_conv_h"], d["_conv_p"]), ("MED", d["_med_h"], d["_med_p"])):
        for s, m in seg[:3]:
            C.append((f"{PFX}-{nom}-INT-{s}", m & p, h))
            C.append((f"{PFX}-{nom}-PART-{s}", m, p.astype(float)))
    ttt = d["_ttt"]
    for s, m in seg[:3]:
        C.append((f"{PFX}-TTT-INT-{s}", m & (ttt > 0), ttt))
        C.append((f"{PFX}-TTT-MEDIA-{s}", m, ttt))
    F.append((f"{PFX}-TTT-INT-BRECHA-SEXO", f"{PFX}-TTT-INT-MUJER", f"{PFX}-TTT-INT-HOMBRE"))
    F.append((f"{PFX}-TTT-MEDIA-BRECHA-SEXO", f"{PFX}-TTT-MEDIA-MUJER", f"{PFX}-TTT-MEDIA-HOMBRE"))
    # RURAL-002 / RG-3920de961d: trabajo comunitario gratuito (6.17, P6_17_3)
    com = pd.Series(d["_comun"], index=d.index)
    for s, m in seg + [("HABL", d["_habl"]), ("NOHABL", d["_nohabl"]),
                       ("IND", d["_ind"]), ("NOIND", d["_noind"])]:
        C.append((f"{PFX}-COMUN-PART-{s}", m, com))
    C.append((f"{PFX}-COMUN-INT-NAC", T & com.eq(1.0) & (d["_comun_h"] > 0), d["_comun_h"]))
    for a, b in (("RURAL", "URBANO"), ("HABL", "NOHABL"), ("IND", "NOIND")):
        F.append((f"{PFX}-COMUN-PART-DIF-{a}-{b}", f"{PFX}-COMUN-PART-{a}", f"{PFX}-COMUN-PART-{b}"))
    return C, F


def celdas_2019(d: pd.DataFrame) -> tuple[list, list]:
    T = pd.Series(True, index=d.index)
    com = pd.Series(d["_comun"], index=d.index)
    P = f"{PFX}-OLA2019-COMUN-PART"
    C = [(f"{P}-{s}", m, com) for s, m in (("NAC", T), ("RURAL", d["_rural"]), ("URBANO", d["_urbano"]),
                                           ("HABL", d["_habl"]), ("NOHABL", d["_nohabl"]))]
    F = [(f"{P}-DIF-RURAL-URBANO", f"{P}-RURAL", f"{P}-URBANO"),
         (f"{P}-DIF-HABL-NOHABL", f"{P}-HABL", f"{P}-NOHABL")]
    return C, F


def medir(inputs: dict, contrato: dict) -> dict:
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    out = {}
    d, diag = frame_2024(inputs[P24]["ruta_absoluta"])
    C, F = celdas_2024(d)
    r, dis = _estima(d, C, F, reps, seed)
    out.update(r)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(v)
    del d
    d, diag = frame_2019(inputs[P19]["ruta_absoluta"])
    C, F = celdas_2019(d)
    r, dis = _estima(d, C, F, reps, seed)
    out.update(r)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-OLA2019-DIAG-{k}"] = int(v)
    return out
