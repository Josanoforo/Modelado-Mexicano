"""PDR1 · pieza ENVIPE2025 · regla RG-b91375cbd5 (CAPITAL_SOCIAL).

Organización con vecinos por inseguridad × estrato socioeconómico (ESTRATO) ×
percepción de inseguridad en la colonia (AP4_3_1), ENVIPE 2025, persona elegida
18+, ponderador FAC_ELE, bootstrap de UPM_DIS dentro de EST_DIS (2000, semilla 42).
Spec humana: forense/prereg-caja/PDR1-ENVIPE2025-spec-v1_0.md.
Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor escalar}.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD_ID = "envipe2025_csv"
MEMBER = "conjunto_de_datos_tper_vic1_envipe2025.csv"
COLUMNS = ["ID_PER", "SEXO", "EDAD", "AP4_3_1", "AP4_8_5", "AP4_9_5",
           "AP4_11_06", "FAC_ELE", "DOMINIO", "ESTRATO", "EST_DIS", "UPM_DIS"]
SEP = "␟"
P = "RESULT-PDR1-ENVIPE2025-RGB913"
ESTRATOS = {"E1": (1,), "E2": (2,), "E3": (3,), "E4": (4,), "ALTO34": (3, 4)}
DESENLACES = ("Y1", "Y2")
SEGMENTOS = {
    "SEXO-H": ("SEXO", (1,)), "SEXO-M": ("SEXO", (2,)),
    "EDAD-18A29": ("EDADG", (1,)), "EDAD-30A44": ("EDADG", (2,)),
    "EDAD-45A59": ("EDADG", (3,)), "EDAD-60MAS": ("EDADG", (4,)),
    "DOM-U": ("DOMINIO", ("U",)), "DOM-C": ("DOMINIO", ("C",)),
    "DOM-R": ("DOMINIO", ("R",)),
}


def _lee(buf: bytes, columns):
    for enc in ("utf-8-sig", "latin-1"):
        try:
            text = buf.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    text = text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")
    head = [c.strip().strip('"').lstrip("﻿") for c in text.split("\n", 1)[0].split(",")]
    missing = [c for c in columns if c not in head]
    if missing:
        raise ValueError("columnas ausentes: " + ",".join(missing))
    df = pd.read_csv(io.StringIO(text), dtype=str, keep_default_na=False,
                     na_filter=False, usecols=lambda c: c.strip().strip('"').lstrip("﻿") in columns)
    df.columns = [c.strip().strip('"').lstrip("﻿") for c in df.columns]
    return df[list(columns)].apply(lambda s: s.astype(str).str.strip().str.strip('"'))


def _code(s):
    return pd.to_numeric(s, errors="coerce").to_numpy()


def _pct(series):
    good = series[np.isfinite(series)]
    if not len(good):
        return None, None
    return float(np.percentile(good, 2.5)), float(np.percentile(good, 97.5))


class Survey:
    """Bootstrap de UPM dentro de estrato con reemplazo (plantilla ARBITRO-MARGINALES-2)."""

    def __init__(self, w, est, upm, replicas, seed):
        self.w = w
        self.n = len(w)
        self.design_ok = bool(self.n) and bool((est != "").all() and (upm != "").all())
        self.n_strata = self.n_psu = self.n_singleton = 0
        self.inv = None
        self.draws = None
        if self.design_ok:
            keys = np.char.add(np.char.add(est.astype(str), SEP), upm.astype(str))
            psus, self.inv = np.unique(keys, return_inverse=True)
            psu_strata = np.asarray([x.split(SEP, 1)[0] for x in psus])
            strata = np.unique(psu_strata)
            self.n_strata, self.n_psu = len(strata), len(psus)
            self.draws = np.zeros((int(replicas), self.n_psu), dtype=np.float64)
            rng = np.random.Generator(np.random.PCG64(int(seed)))
            for st in strata:
                pos = np.flatnonzero(psu_strata == st)
                k = len(pos)
                if k == 1:
                    self.n_singleton += 1
                    self.draws[:, pos[0]] = 1
                else:
                    self.draws[:, pos] = rng.multinomial(k, np.full(k, 1.0 / k), size=int(replicas))

    def ratio(self, num, den):
        num = np.asarray(num, bool)
        den = np.asarray(den, bool)
        dw = self.w * den
        mass = float(dw.sum())
        point = None if mass <= 0 else float((self.w * (num & den)).sum() / mass)
        series = None
        lo = hi = None
        if point is not None and self.design_ok:
            dp = np.bincount(self.inv, weights=dw, minlength=self.n_psu)
            np_ = np.bincount(self.inv, weights=self.w * (num & den), minlength=self.n_psu)
            dr = self.draws @ dp
            nr = self.draws @ np_
            with np.errstate(divide="ignore", invalid="ignore"):
                series = np.where(dr > 0, nr / dr, np.nan)
            lo, hi = _pct(series)
        return {"n": int(den.sum()), "p": point, "lo": lo, "hi": hi}, series


def _diff(a, b):
    (ap, as_), (bp, bs) = a, b
    point = None if ap["p"] is None or bp["p"] is None else (ap["p"] - bp["p"]) * 100.0
    lo = hi = None
    series = None
    if as_ is not None and bs is not None:
        series = (as_ - bs) * 100.0
        lo, hi = _pct(series)
    return {"p": point, "lo": lo, "hi": hi}, series


def dictamen(d, lo, hi, umbral_pp):
    """B-bis congelado (spec §B-bis): CONFIRMA si d >= umbral y lo > 0; ROMPE si d < 0 y hi < 0; MATIZA en otro caso."""
    if d is None or lo is None or hi is None:
        return "NO-ESTIMABLE"
    if d >= umbral_pp and lo > 0:
        return "CONFIRMA"
    if d < 0 and hi < 0:
        return "ROMPE"
    return "MATIZA"


def measure_frame(df, replicas, seed, umbral_pp):
    w = pd.to_numeric(df["FAC_ELE"], errors="coerce").to_numpy(dtype=float)
    keep = np.isfinite(w) & (w > 0)
    df = df.loc[keep].reset_index(drop=True)
    w = w[keep]
    s = Survey(w, df["EST_DIS"].to_numpy(dtype=str), df["UPM_DIS"].to_numpy(dtype=str), replicas, seed)
    out = {}
    out[f"{P}-N-FILAS"] = int(len(df))
    out[f"{P}-N-ESTRATOS"] = s.n_strata
    out[f"{P}-N-UPM"] = s.n_psu
    out[f"{P}-N-SINGLETON"] = s.n_singleton
    out[f"{P}-METODO-IC"] = ("BOOTSTRAP-UPM-EN-ESTRATO-SEED42" if s.design_ok
                            else "IC-NO-DISPONIBLE-DISENO-INCOMPLETO")
    estr = _code(df["ESTRATO"])
    col = _code(df["AP4_3_1"])
    col = np.where(np.isfinite(col), col, -1)
    y1c = _code(df["AP4_11_06"])
    r5 = _code(df["AP4_8_5"])
    y2c = _code(df["AP4_9_5"])
    edad = _code(df["EDAD"])
    edadg = np.select([(edad >= 18) & (edad <= 29), (edad >= 30) & (edad <= 44),
                       (edad >= 45) & (edad <= 59), (edad >= 60) & (edad < 98)], [1, 2, 3, 4], 0)
    seg = {"SEXO": _code(df["SEXO"]), "EDADG": edadg, "DOMINIO": df["DOMINIO"].to_numpy(dtype=str)}
    ys = {
        "Y1": (np.isin(y1c, (1, 2)), y1c == 1),
        "Y2": ((r5 == 1) & np.isin(y2c, (1, 2)), y2c == 1),
    }
    amen = {"INSEGURA": col == 2, "SEGURA": col == 1, "TOTAL": np.ones(len(df), bool)}
    for yk, (base, pos) in ys.items():
        diffs = {}
        for ak, am in amen.items():
            cells = {}
            for ek, codes in ESTRATOS.items():
                den = base & am & np.isin(estr, codes)
                st, ser = s.ratio(pos, den)
                cells[ek] = (st, ser)
                k = f"{P}-{yk}-{ak}-{ek}"
                out[k + "-P"], out[k + "-LO"], out[k + "-HI"], out[k + "-N"] = st["p"], st["lo"], st["hi"], st["n"]
            d, dser = _diff(cells["ALTO34"], cells["E1"])
            diffs[ak] = (d, dser)
            k = f"{P}-{yk}-{ak}-D34M1"
            out[k + "-PP"], out[k + "-LO"], out[k + "-HI"] = d["p"], d["lo"], d["hi"]
        dd, _ = _diff(({"p": None if diffs["INSEGURA"][0]["p"] is None or diffs["SEGURA"][0]["p"] is None
                        else (diffs["INSEGURA"][0]["p"] - diffs["SEGURA"][0]["p"]) / 100.0},
                       None if diffs["INSEGURA"][1] is None else diffs["INSEGURA"][1] / 100.0),
                      ({"p": 0.0}, None if diffs["SEGURA"][1] is None else diffs["SEGURA"][1] / 100.0))
        k = f"{P}-{yk}-DID-INS-SEG"
        out[k + "-PP"], out[k + "-LO"], out[k + "-HI"] = dd["p"], dd["lo"], dd["hi"]
    base, pos = ys["Y1"]
    for gk, (var, codes) in SEGMENTOS.items():
        m = base & amen["INSEGURA"] & np.isin(seg[var], codes)
        a = s.ratio(pos, m & np.isin(estr, (3, 4)))
        b = s.ratio(pos, m & (estr == 1))
        d, _ = _diff(a, b)
        k = f"{P}-Y1-INSEGURA-D34M1-{gk}"
        out[k + "-PP"], out[k + "-LO"], out[k + "-HI"] = d["p"], d["lo"], d["hi"]
        out[k + "-NA"], out[k + "-NB"] = a[0]["n"], b[0]["n"]
    k = f"{P}-Y1-INSEGURA-D34M1"
    out[f"{P}-DICTAMEN"] = dictamen(out[k + "-PP"], out[k + "-LO"], out[k + "-HI"], umbral_pp)
    return out


def medir(inputs, contrato):
    path = inputs[PAYLOAD_ID]["ruta_absoluta"]
    with zipfile.ZipFile(path) as z:
        ms = [x for x in z.namelist() if x.rsplit("/", 1)[-1] == MEMBER]
        if len(ms) != 1:
            raise ValueError(f"miembro {MEMBER}: coincidencias={len(ms)}")
        df = _lee(z.read(ms[0]), COLUMNS)
    par = contrato["parametros"]
    return measure_frame(df, int(par["bootstrap_replicas"]), int(contrato["seed"]["valor"]),
                         float(par["umbral_confirma_pp"]))
