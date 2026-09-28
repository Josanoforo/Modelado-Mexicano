"""PDR1 pieza ENADID2023: afirmación ASTRA5-U0-TEC-010 (RURAL_INDIGENA).

No sabe leer y escribir un recado (P3_23=2) entre residentes de 15+ por
autoadscripción indígena (P3_12=1 vs 2), con cortes por sexo, edad y
urbano/rural. Spec humana: forense/prereg-caja/PDR1-ENADID2023-spec-v1_0.md.

Interfaz GEN2: medir(inputs, contrato) -> {RESULT-...: valor}. Todos los
RESULT son escalares (ninguno texto > 1024 bytes).
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD_ID = "enadid2023_base_datos_csv"
MEMBER = "TSDEM.csv"
COLS = ["SEXO", "EDAD", "P3_12", "P3_23", "T_LOC_UR", "FAC_VIV", "EST_DIS", "UPM_DIS"]
PFX = "RESULT-PDR1-ENADID2023"

IND = (("IND", "1"), ("NOIND", "2"))
SEXOS = (("H", "1"), ("M", "2"))
EDADES = (("15_29", 15, 29), ("30_44", 30, 44), ("45_59", 45, 59), ("60M", 60, 120))
LOCS = (("URB", "1"), ("RUR", "2"), ("LOCDESC", None))
# celda = ((((ind*2+sexo)*4+edad)*3+loc)*2+analfabeta)
NCELL = 2 * 2 * 4 * 3 * 2

# cifras publicadas por la afirmación (proporción, no porcentaje)
CIFRA_IND = 0.19
CIFRA_NOIND = 0.028
CIFRA_IND_M = 0.242


def read_frame(fileobj) -> pd.DataFrame:
    frame = pd.read_csv(fileobj, dtype=str, encoding="utf-8-sig", low_memory=False,
                        usecols=lambda n: n.strip().upper() in COLS)
    frame.columns = [c.strip().upper() for c in frame.columns]
    faltan = sorted(set(COLS) - set(frame.columns))
    if faltan:
        raise ValueError("COLUMNAS-AUSENTES:" + ",".join(faltan))
    for c in COLS:
        frame[c] = frame[c].fillna("").astype(str).str.strip()
    return frame


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Conserva el marco completo (toda fila con peso y diseño) para sortear UPM;
    las filas fuera del universo llevan _cell = -1 y no aportan masa."""
    edad = pd.to_numeric(df["EDAD"], errors="coerce")
    peso = pd.to_numeric(df["FAC_VIV"], errors="coerce")
    marco = np.isfinite(peso) & (peso > 0) & df["EST_DIS"].ne("") & df["UPM_DIS"].ne("")
    out = df.loc[marco].copy()
    e = edad[marco]
    out["_w"] = peso[marco].astype(float)
    univ = (e.between(15, 120) & out["SEXO"].isin(["1", "2"])
            & out["P3_12"].isin(["1", "2"]) & out["P3_23"].isin(["1", "2"])).to_numpy()
    ind = np.where(out["P3_12"].eq("1"), 0, 1)
    sx = np.where(out["SEXO"].eq("1"), 0, 1)
    ed = np.zeros(len(out), dtype=int)
    for i, (_, lo, hi) in enumerate(EDADES):
        ed[(e >= lo).to_numpy() & (e <= hi).to_numpy()] = i
    lc = np.where(out["T_LOC_UR"].eq("1"), 0, np.where(out["T_LOC_UR"].eq("2"), 1, 2))
    an = np.where(out["P3_23"].eq("2"), 1, 0)
    cell = ((((ind * 2 + sx) * 4 + ed) * 3 + lc) * 2 + an).astype(int)
    out["_cell"] = np.where(univ, cell, -1)
    out["_univ"] = univ
    return out


def _cells(ind=None, sx=None, ed=None, lc=None, an=None):
    r = []
    for a in range(2):
        for b in range(2):
            for c in range(4):
                for d in range(3):
                    for f in range(2):
                        if ((ind is None or a == ind) and (sx is None or b == sx)
                                and (ed is None or c == ed) and (lc is None or d == lc)
                                and (an is None or f == an)):
                            r.append(((((a * 2 + b) * 4 + c) * 3 + d) * 2 + f))
    return r


def bootstrap(data: pd.DataFrame, replicas: int, seed: int):
    psus = data[["EST_DIS", "UPM_DIS"]].drop_duplicates().sort_values(["EST_DIS", "UPM_DIS"])
    psus = psus.reset_index(drop=True)
    psus["_pi"] = np.arange(len(psus))
    d = data.merge(psus, on=["EST_DIS", "UPM_DIS"], how="left", validate="many_to_one")
    mat = np.zeros((len(psus), NCELL))
    d = d.loc[d["_cell"] >= 0]
    np.add.at(mat, (d["_pi"].to_numpy(int), d["_cell"].to_numpy(int)), d["_w"].to_numpy(float))
    rng = np.random.Generator(np.random.PCG64(seed))
    grupos = [g["_pi"].to_numpy(int) for _, g in psus.groupby("EST_DIS", sort=True)]
    singleton = sum(1 for g in grupos if len(g) == 1)
    reps = np.zeros((replicas, NCELL))
    bloque = 200
    for start in range(0, replicas, bloque):
        k = min(bloque, replicas - start)
        mult = np.ones((k, len(psus)))
        for idx in grupos:
            m = len(idx)
            if m == 1:
                continue  # singleton: autorremuestreo, varianza cero
            mult[:, idx] = rng.multinomial(m, np.full(m, 1.0 / m), size=k)
        reps[start:start + k] = mult @ mat
    punto = mat.sum(axis=0)
    return punto, reps, len(grupos), len(psus), singleton


def _prop(punto, reps, sel):
    num = _cells(an=1, **sel)
    den = _cells(**sel)
    D = punto[den].sum()
    if D <= 0:
        return None, None
    p = punto[num].sum() / D
    Dr = reps[:, den].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pr = np.where(Dr > 0, reps[:, num].sum(axis=1) / Dr, np.nan)
    return float(p), pr


def _ic(r):
    if r is None:
        return None, None
    g = r[np.isfinite(r)]
    if len(g) < 2:
        return None, None
    return float(np.percentile(g, 2.5)), float(np.percentile(g, 97.5))


def dominios():
    doms = [("TOTAL", {})]
    for s, (sn, _) in enumerate(SEXOS):
        doms.append((sn, {"sx": s}))
    for e, (en, _, _) in enumerate(EDADES):
        doms.append((en, {"ed": e}))
    for l, (ln, _) in enumerate(LOCS[:2]):
        doms.append((ln, {"lc": l}))
    for s, (sn, _) in enumerate(SEXOS):
        for e, (en, _, _) in enumerate(EDADES):
            doms.append((f"{sn}-{en}", {"sx": s, "ed": e}))
    return doms


def estima(data: pd.DataFrame, replicas: int, seed: int) -> dict:
    punto, reps, nest, nupm, nsing = bootstrap(data, replicas, seed)
    u = data.loc[data["_univ"]]
    out = {
        f"{PFX}-N-MARCO": int(len(data)),
        f"{PFX}-N-UNIVERSO": int(len(u)),
        f"{PFX}-N-IND": int((u["P3_12"] == "1").sum()),
        f"{PFX}-N-NOIND": int((u["P3_12"] == "2").sum()),
        f"{PFX}-N-IND-M": int(((u["P3_12"] == "1") & (u["SEXO"] == "2")).sum()),
        f"{PFX}-N-ESTRATOS": int(nest),
        f"{PFX}-N-UPM": int(nupm),
        f"{PFX}-N-ESTRATOS-SINGLETON": int(nsing),
        f"{PFX}-REPLICAS": int(replicas),
        f"{PFX}-SEMILLA": int(seed),
    }
    est = {}
    for dn, sel in dominios():
        pr = {}
        for i, (gn, _) in enumerate(IND):
            p, r = _prop(punto, reps, dict(sel, ind=i))
            lo, hi = _ic(r)
            out[f"{PFX}-P-{gn}-{dn}"] = p
            out[f"{PFX}-P-{gn}-{dn}-IC95INF"] = lo
            out[f"{PFX}-P-{gn}-{dn}-IC95SUP"] = hi
            pr[gn] = (p, r)
            est[(gn, dn)] = (p, lo, hi)
        (pi, ri), (pn, rn) = pr["IND"], pr["NOIND"]
        if pi is None or pn is None:
            b, lo, hi = None, None, None
        else:
            b = pi - pn
            lo, hi = _ic(ri - rn)
        out[f"{PFX}-BRECHA-{dn}"] = b
        out[f"{PFX}-BRECHA-{dn}-IC95INF"] = lo
        out[f"{PFX}-BRECHA-{dn}-IC95SUP"] = hi
        est[("BRECHA", dn)] = (b, lo, hi)
    out.update(dictamen(est))
    return out


def _dentro(cifra, t):
    p, lo, hi = t
    if lo is None or hi is None:
        return None
    return lo <= cifra <= hi


def dictamen(est) -> dict:
    b = est[("BRECHA", "TOTAL")][0]
    c1 = _dentro(CIFRA_IND, est[("IND", "TOTAL")])
    c2 = _dentro(CIFRA_NOIND, est[("NOIND", "TOTAL")])
    c3 = _dentro(CIFRA_IND_M, est[("IND", "M")])
    f = lambda x: "NA" if x is None else ("SI" if x else "NO")
    if b is None:
        d = "NO-CONSTRUIBLE"
    elif b <= 0:
        d = "ROMPE"
    elif c1 is True and c2 is True and c3 is True:
        d = "CONFIRMA"
    else:
        d = "MATIZA"
    return {
        f"{PFX}-CIFRA19-EN-IC": f(c1),
        f"{PFX}-CIFRA2_8-EN-IC": f(c2),
        f"{PFX}-CIFRA24_2-EN-IC": f(c3),
        f"{PFX}-DICTAMEN-BBIS": d,
    }


def medir(inputs, contrato):
    path = inputs[PAYLOAD_ID]["ruta_absoluta"]
    with zipfile.ZipFile(path) as z:
        hits = [n for n in z.namelist() if n.rsplit("/", 1)[-1] == MEMBER]
        if len(hits) != 1:
            raise ValueError(f"miembro {MEMBER}: coincidencias={len(hits)}")
        with z.open(hits[0]) as fh:
            df = read_frame(io.TextIOWrapper(fh, encoding="utf-8-sig", newline=""))
    data = prepare(df)
    par, seed = contrato["parametros"], contrato["seed"]
    return estima(data, int(par["bootstrap_replicas"]), int(seed["valor"]))
