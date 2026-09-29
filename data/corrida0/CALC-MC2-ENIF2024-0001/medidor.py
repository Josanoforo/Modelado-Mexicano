#!/usr/bin/env python3
"""GEN2-MEDICION-CARRILES-2 · hija ENIF 2024 · CALC-MC2-ENIF2024-0001.

El primer resultado que produzca este procedimiento es el que se reporta.

Pisos descriptivos RETROSPECTIVOS de ENIF 2024 (persona elegida 18+) para las
afirmaciones MEDIBLE-EN-CORPUS sin RESULT del mapa v1.1 que nombran ENIF 2024
en módulos abiertos (3, 4, 5, 6, 8, 9), con la segmentación de §3 (sexo, edad,
escolaridad, tamaño de localidad, región, formalidad). El módulo 7 (pagos)
está RESERVADO (R06, TRAMITE-FIRMAS-21-ADENDA-1): ninguna columna P7_* se lee;
`_lee` se niega si la lista pide una. Contrato humano:
forense/prereg-caja/MC2-ENIF2024-spec-v1_0.md (manda sobre este código).

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor escalar}.
Todos los RESULT son escalares (flotante/entero); ningún texto.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD = "enif_2024_enif_2024_bd_csv"
MIEMBRO = "TMODULO.csv"
PFX = "RESULT-MC2-ENIF2024"

P54 = [f"P5_4_{i}" for i in range(1, 10)]
P62 = [f"P6_2_{i}" for i in range(1, 10)]
COLS = (["EDAD_V", "NIV", "SEXO", "TLOC", "REGION", "EST_DIS", "UPM_DIS", "FAC_PER", "P3_13",
         "P4_6_4", "P4_10", "P5_1_5", "P5_13", "P6_14", "P6_17_4", "P8_1", "P9_1", "P9_2", "P9_3",
         "P9_9_1", "P9_9_5"] + P54 + P62)

EDADES = [("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 97)]
ESCOLARIDAD = [("HASTA-PRIMARIA", {"0", "1", "2"}), ("SECUNDARIA", {"3", "4", "5"}),
               ("MEDIA-SUPERIOR", {"6", "7"}), ("SUPERIOR", {"8", "9", "10", "11"})]
REGIONES = ["1", "2", "3", "4", "5", "6"]


class ReservaRota(RuntimeError):
    """El dato no es el que la spec declara, o se pidió una columna reservada."""


# ── lectura ────────────────────────────────────────────────────────────────
def _lee(ruta: str, cols: list[str]) -> pd.DataFrame:
    if any(c.upper().startswith("P7") for c in cols):
        raise ReservaRota("módulo 7 (pagos) RESERVADO (R06): ninguna columna P7_* es input")
    with zipfile.ZipFile(ruta) as zf:
        nombres = [n for n in zf.namelist() if n.lower() == MIEMBRO.lower()]
        if len(nombres) != 1:
            raise ReservaRota(f"miembro no único: {MIEMBRO}: {nombres}")
        raw = zf.read(nombres[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            txt = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ReservaRota("codificación no reconocida")
    del raw
    quiero = {c.upper() for c in cols}
    d = pd.read_csv(io.StringIO(txt), dtype=str, keep_default_na=False, na_filter=False,
                    usecols=lambda c: str(c).strip().upper() in quiero)
    d.columns = [str(c).strip().upper() for c in d.columns]
    faltan = sorted(quiero - set(d.columns))
    if faltan:
        raise ReservaRota(f"variables ausentes: {faltan}")
    return d


def _code(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _bin(s: pd.Series, si: set[str], no: set[str]) -> pd.Series:
    """1.0 si código ∈ si, 0.0 si ∈ no, NaN en otro caso (fuera del denominador)."""
    c = _code(s)
    return pd.Series(np.where(c.isin(si), 1.0, np.where(c.isin(no), 0.0, np.nan)), index=s.index)


def _cat(s: pd.Series, validos: set[str], objetivo: set[str]) -> pd.Series:
    """Proporción de `objetivo` entre los códigos `validos`; el resto NaN."""
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


# ── frame ──────────────────────────────────────────────────────────────────
def frame(ruta: str) -> tuple[pd.DataFrame, dict]:
    d = _lee(ruta, COLS)
    diag = {"FILAS-TMODULO": len(d)}
    d["_w"] = pd.to_numeric(d["FAC_PER"].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].astype(str).str.strip()
    d["_upm"] = d["UPM_DIS"].astype(str).str.strip()
    sx = _code(d["SEXO"])
    d["_hombre"], d["_mujer"] = sx.eq("1"), sx.eq("2")
    ed = pd.to_numeric(d["EDAD_V"].astype(str).str.strip(), errors="coerce")
    d["_edad_n"] = ed
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
    ss = _code(d["P3_13"])
    d["_con_ss"], d["_sin_ss"] = ss.isin(["1", "2", "3", "4", "5", "6"]), ss.eq("7")

    # indicadores binarios (spec §1)
    si, no = {"1"}, {"2"}
    c54 = pd.DataFrame({c: _code(d[c]) for c in P54})
    c62 = pd.DataFrame({c: _code(d[c]) for c in P62})
    v54, v62 = c54.isin(["1", "2"]).all(axis=1), c62.isin(["1", "2"]).all(axis=1)
    d["CUENTA"] = np.where(v54, c54.eq("1").any(axis=1).astype(float), np.nan)
    d["CRED-FORMAL"] = np.where(v62, c62.eq("1").any(axis=1).astype(float), np.nan)
    d["CTA-AHORRO"] = _bin(d["P5_4_4"], si, no)
    d["CTA-APP"] = _bin(d["P5_4_8"], si, no)
    d["TC-DEPTO"] = _bin(d["P6_2_1"], si, no)
    d["TC-BANC"] = _bin(d["P6_2_2"], si, no)
    d["CRED-VIV"] = _bin(d["P6_2_6"], si, no)
    d["SEGURO"] = _bin(d["P8_1"], si, no)
    d["AFORE"] = _bin(d["P9_1"], si, no)
    d["AFORE-VOL"] = _bin(d["P9_3"], si, no).where(_code(d["P9_1"]).eq("1"))
    seg1, afo1 = _code(d["P8_1"]).eq("1"), _code(d["P9_1"]).eq("1")
    pf = (d["CUENTA"].eq(1.0) | d["CRED-FORMAL"].eq(1.0) | seg1 | afo1).astype(float)
    d["PRODUCTO-FORMAL"] = pf.where(v54 & v62)
    d["TANDA"] = _bin(d["P5_1_5"], si, no)
    d["METAS-SIEMPRE"] = _cat(d["P4_6_4"], {"1", "2", "3"}, {"1"})
    d["CUBRE-MES"] = _cat(d["P4_10"], {"1", "2", "3", "4", "5"}, {"3", "4", "5"})
    d["VEJEZ-GOB"] = _bin(d["P9_9_1"], si, no)
    d["VEJEZ-TRAB"] = _bin(d["P9_9_5"], si, no)

    diag["CUENTA-INVALIDA"] = int((~v54).sum())
    diag["CRED-FORMAL-INVALIDA"] = int((~v62).sum())
    diag["SEGURO-NO-SABE"] = int(_code(d["P8_1"]).eq("9").sum())
    diag["AFORE-NO-SABE"] = int(_code(d["P9_1"]).eq("9").sum())
    diag["EDAD-FUERA-18-97"] = int((~((ed >= 18) & (ed <= 97))).sum())
    diag["NIV-NO-SABE"] = int(nv.eq("99").sum())
    diag["N-SIN-PONDERADOR"] = int((~(d["_w"] > 0)).sum())
    return d, diag


INDICADORES = ["CUENTA", "CTA-AHORRO", "CTA-APP", "CRED-FORMAL", "TC-DEPTO", "TC-BANC", "CRED-VIV",
               "SEGURO", "AFORE", "AFORE-VOL", "PRODUCTO-FORMAL", "TANDA", "METAS-SIEMPRE",
               "CUBRE-MES", "VEJEZ-GOB", "VEJEZ-TRAB"]
RAZONES = [  # (prefijo, columna, válidos, códigos a reportar uno por uno)
    ("NUNCACRED-RAZON", "P6_14", [str(i) for i in range(1, 10)]),
    ("NOAFORE-RAZON", "P9_2", [str(i) for i in range(1, 10)]),
    ("EFECTIVO-RAZON", "P5_13", [str(i) for i in range(1, 8)]),
]
GRUPOS_NOAFORE = [("G-SINTRAB-INGRESO", {"1", "3"}), ("G-VEHICULO", {"2", "4", "6", "8"})]
BRECHAS_SEXO = ["CUENTA", "CTA-AHORRO", "CRED-FORMAL", "SEGURO", "AFORE", "PRODUCTO-FORMAL", "TANDA"]
BRECHAS_SS = ["AFORE", "SEGURO", "CRED-VIV", "CUENTA", "CRED-FORMAL"]


def segmentos(d: pd.DataFrame) -> list[tuple[str, pd.Series]]:
    T = pd.Series(True, index=d.index)
    s = [("NAC", T), ("HOMBRE", d["_hombre"]), ("MUJER", d["_mujer"])]
    s += [(f"EDAD-{e}", d[f"_edad_{e}"]) for e, _, _ in EDADES]
    s += [(f"ESC-{e}", d[f"_esc_{e}"]) for e, _ in ESCOLARIDAD]
    s += [("LOC-15MIL-Y-MAS", d["_loc_mas"]), ("LOC-MENOS-15MIL", d["_loc_menos"])]
    s += [(f"REGION-{r}", d[f"_reg_{r}"]) for r in REGIONES]
    s += [("CON-SS", d["_con_ss"]), ("SIN-SS", d["_sin_ss"])]
    return s


# ── celdas (el catálogo; los ids del spec.yaml salen de aquí) ─────────────
def celdas(d: pd.DataFrame) -> tuple[list, list]:
    C, F = [], []
    seg = segmentos(d)
    for ind in INDICADORES:
        for s, m in seg:
            C.append((f"{PFX}-{ind}-{s}", m, d[ind]))
    for ind in BRECHAS_SEXO:
        F.append((f"{PFX}-{ind}-BRECHA-MUJER-HOMBRE", f"{PFX}-{ind}-MUJER", f"{PFX}-{ind}-HOMBRE"))
    for ind in BRECHAS_SS:
        F.append((f"{PFX}-{ind}-DIF-CONSS-SINSS", f"{PFX}-{ind}-CON-SS", f"{PFX}-{ind}-SIN-SS"))
    # distribuciones de razón principal: nacional y por sexo
    for pref, col, validos in RAZONES:
        V = set(validos)
        for cod in validos:
            y = _cat(d[col], V, {cod})
            for s, m in seg[:3]:
                C.append((f"{PFX}-{pref}-{cod}-{s}", m, y))
        if col == "P9_2":
            for g, cods in GRUPOS_NOAFORE:
                y = _cat(d[col], V, cods)
                for s, m in seg[:3]:
                    C.append((f"{PFX}-{pref}-{g}-{s}", m, y))
            F.append((f"{PFX}-{pref}-DIF-VEHICULO-SINTRAB-NAC",
                      f"{PFX}-{pref}-G-VEHICULO-NAC", f"{PFX}-{pref}-G-SINTRAB-INGRESO-NAC"))
    y = _bin(d["P6_17_4"], {"1"}, {"0"})
    for s, m in seg[:3]:
        C.append((f"{PFX}-RECHAZO-SINHISTORIAL-{s}", m, y))
    return C, F


def medir(inputs: dict, contrato: dict) -> dict:
    reps = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    d, diag = frame(inputs[PAYLOAD]["ruta_absoluta"])
    C, F = celdas(d)
    out, dis = _estima(d, C, F, reps, seed)
    for k, v in {**diag, **dis}.items():
        out[f"{PFX}-DIAG-{k}"] = int(v)
    return out
