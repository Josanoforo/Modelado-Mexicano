"""Cobertura y saldos completos Afore por CAT_POS, ENFIH 2019."""
from __future__ import annotations

import io, json, math, zipfile
import numpy as np
import pandas as pd

PREFIX = "RESULT-ENFIH2019-COBERTURA-SALDOS-CATPOS-"
KEY = ["FOLIO", "VIV_SEL", "HOGAR"]
CONC = KEY + ["C_AFORE", "V_AFORE", "FAC_HOG", "EDIS", "UPM_DIS", "CAT_POS"]
MOD = KEY + ["N_REN", "P9_10", "P9_11"]
NATIVE = ["0", "1", "2", "3", "4", "5"]
SPECIAL = {"999999888", "999999999"}


def _member(zf, wanted):
    got = [n for n in zf.namelist() if n.rsplit("/", 1)[-1].upper() == wanted.upper()]
    if len(got) != 1: raise ValueError(f"miembro {wanted}: {len(got)}")
    return got[0]


def _read(zf, wanted, cols):
    raw = zf.read(_member(zf, wanted)).replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    x = pd.read_csv(io.BytesIO(raw), encoding="latin-1", dtype=str, keep_default_na=False)
    x.columns = [str(c).lstrip("\ufeff").lstrip("ï»¿").strip() for c in x.columns]
    missing = [c for c in cols if c not in x]
    if missing: raise ValueError(f"{wanted}: faltan {missing}")
    return x[cols].apply(lambda s: s.astype(str).str.strip())


def weighted_quantile(x, w, q):
    x, w = np.asarray(x, float), np.asarray(w, float)
    keep = np.isfinite(x) & np.isfinite(w) & (w > 0)
    if not keep.any(): return float("nan")
    order = np.argsort(x[keep], kind="stable"); x, w = x[keep][order], w[keep][order]
    return float(x[np.searchsorted(np.cumsum(w), q * math.fsum(w.tolist()), side="left")])


def _mass(w, m): return float(math.fsum(np.asarray(w, float)[m].tolist()))
def _mean(x, w):
    x, w = np.asarray(x, float), np.asarray(w, float); keep = np.isfinite(x) & np.isfinite(w) & (w > 0)
    den = math.fsum(w[keep].tolist())
    return float(math.fsum((x[keep] * w[keep]).tolist()) / den) if den else float("nan")


def classify(conc, mod):
    if conc.duplicated(KEY).any() or mod.duplicated(KEY + ["N_REN"]).any():
        raise ValueError("llave de hogar o persona no unica")
    h = mod.loc[mod.P9_10.eq("1"), KEY + ["P9_11"]].copy(); raw = h.P9_11
    amount = pd.to_numeric(raw, errors="coerce"); known = amount.between(0, 108264000, inclusive="both")
    if (~(known | raw.isin(SPECIAL))).any(): raise ValueError("P9_11 fuera de catalogo")
    h["known"] = known; h["amount"] = amount.where(known, 0.0)
    a = h.groupby(KEY, sort=False).agg(n_holders=("P9_11", "size"), n_known=("known", "sum"),
                                       sum_known=("amount", "sum")).reset_index()
    d = conc.merge(a, on=KEY, how="left", validate="one_to_one")
    d[["n_holders", "n_known", "sum_known"]] = d[["n_holders", "n_known", "sum_known"]].fillna(0)
    d["c"] = pd.to_numeric(d.C_AFORE, errors="coerce"); d["v"] = pd.to_numeric(d.V_AFORE, errors="coerce")
    if d.c.isna().any() or not set(d.c).issubset({0, 1}) or d.v.isna().any() or (d.v < 0).any():
        raise ValueError("C_AFORE/V_AFORE invalido")
    if not np.array_equal(d.c.to_numpy(int), (d.n_holders > 0).to_numpy(int)): raise ValueError("C_AFORE no coincide")
    if not np.allclose(d.v, d.sum_known, rtol=0, atol=0): raise ValueError("V_AFORE no coincide")
    d["state"] = "NO-TENEDOR"; holder = d.c.eq(1); complete = holder & d.n_known.eq(d.n_holders)
    d.loc[complete & d.v.eq(0), "state"] = "COMPLETO-CERO"
    d.loc[complete & d.v.gt(0), "state"] = "COMPLETO-POSITIVO"
    d.loc[holder & d.n_known.eq(0), "state"] = "DESCONOCIDO-TOTAL"
    d.loc[holder & d.n_known.gt(0) & ~complete, "state"] = "PARCIAL"
    d["complete"] = complete; d["cat"] = d.CAT_POS.where(d.CAT_POS.isin(NATIVE), "DESCONOCIDO")
    return d


def point_table(d, w):
    out = {}; allmask = np.ones(len(d), dtype=bool)
    for cat in NATIVE + ["DESCONOCIDO"]:
        m = d.cat.eq(cat).to_numpy(); holder = m & d.c.eq(1).to_numpy(); complete = m & d.complete.to_numpy(bool)
        positive = complete & d.v.gt(0).to_numpy(); hm = _mass(w, holder); cm = _mass(w, complete)
        states = {s: {"n": int((holder & d.state.eq(s).to_numpy()).sum()), "masa": _mass(w, holder & d.state.eq(s).to_numpy()),
                      "p_tenedores": (_mass(w, holder & d.state.eq(s).to_numpy()) / hm if hm else None)}
                  for s in ["COMPLETO-CERO", "COMPLETO-POSITIVO", "PARCIAL", "DESCONOCIDO-TOTAL"]}
        x = d.v.to_numpy(float)
        out[cat] = {"n_marco": int(m.sum()), "masa_marco": _mass(w, m), "p_tenencia": _mass(w, holder)/_mass(w, m) if _mass(w,m) else None,
                    "n_tenedores": int(holder.sum()), "masa_tenedores": hm, "cobertura_completa": cm/hm if hm else None,
                    "estados": states, "n_completos": int(complete.sum()), "masa_completos": cm,
                    "media": _mean(x[complete], w[complete]), "p25": weighted_quantile(x[complete], w[complete], .25),
                    "mediana": weighted_quantile(x[complete], w[complete], .5), "p75": weighted_quantile(x[complete], w[complete], .75),
                    "p90": weighted_quantile(x[complete], w[complete], .9), "n_positivos": int(positive.sum()),
                    "masa_positivos": _mass(w, positive), "media_positivos": _mean(x[positive], w[positive]),
                    "mediana_positivos": weighted_quantile(x[positive], w[positive], .5)}
    return out


def contrasts(d, w):
    x = d.v.to_numpy(float); cats = d.cat.to_numpy(); native = np.isin(cats, NATIVE); out = {}
    for cat in NATIVE:
        a = cats == cat; b = native & ~a
        def stats(m):
            h = m & d.c.eq(1).to_numpy(); c = m & d.complete.to_numpy(bool); hm = _mass(w,h)
            return (_mass(w,c)/hm if hm else float("nan"), _mean(x[c],w[c]), weighted_quantile(x[c],w[c],.5))
        sa, sb = stats(a), stats(b)
        out[cat] = {"cobertura_categoria": sa[0], "cobertura_resto": sb[0], "delta_cobertura": sa[0]-sb[0],
                    "media_categoria": sa[1], "media_resto": sb[1], "delta_media": sa[1]-sb[1],
                    "mediana_categoria": sa[2], "mediana_resto": sb[2], "delta_mediana": sa[2]-sb[2],
                    "sin_solapamiento": bool(not np.any(a & b))}
    return out


def _multipliers(d, reps, seed):
    clu = (d.EDIS + "\x1f" + d.UPM_DIS).to_numpy(); unique, inv = np.unique(clu, return_inverse=True)
    strata = np.array([v.split("\x1f",1)[0] for v in unique]); rng = np.random.Generator(np.random.PCG64(seed))
    pos = [np.flatnonzero(strata == s) for s in np.unique(strata)]
    for _ in range(reps):
        counts = np.zeros(len(unique));
        for p in pos: counts += np.bincount(rng.choice(p, size=len(p), replace=True), minlength=len(unique))
        yield counts[inv]


def _ci(v):
    v = np.asarray(v, float); v = v[np.isfinite(v)]
    return [float(z) for z in np.percentile(v,[2.5,97.5])] if len(v) else [None,None]


def medir(inputs, contrato):
    p = contrato["parametros"]
    with zipfile.ZipFile(inputs["enfih2019_bd_csv_zip"]["ruta_absoluta"]) as z:
        d = classify(_read(z,p["tabla_concentradora"],CONC), _read(z,p["tabla_modulo"],MOD))
    d = d.sort_values(KEY,kind="stable").reset_index(drop=True); d["w"] = pd.to_numeric(d.FAC_HOG,errors="coerce")
    d = d.loc[np.isfinite(d.w) & d.w.gt(0)].copy().reset_index(drop=True)
    if d.empty or (d.EDIS.eq("")|d.UPM_DIS.eq("")).any(): raise ValueError("marco o diseno invalido")
    w = d.w.to_numpy(float); table, con = point_table(d,w), contrasts(d,w)
    keys = [(c,k) for c in NATIVE+["DESCONOCIDO"] for k in ["cobertura_completa","media","mediana"]]
    ckeys = [(c,k) for c in NATIVE for k in ["delta_cobertura","delta_media","delta_mediana"]]
    samples = {("t",)+k: [] for k in keys} | {("c",)+k: [] for k in ckeys}
    for mult in _multipliers(d,int(p["bootstrap_replicas"]),int(contrato["seed"]["valor"])):
        rt, rc = point_table(d,w*mult), contrasts(d,w*mult)
        for c,k in keys: samples[("t",c,k)].append(rt[c][k])
        for c,k in ckeys: samples[("c",c,k)].append(rc[c][k])
    for c,k in keys: table[c][k+"_ic95"] = _ci(samples[("t",c,k)])
    for c,k in ckeys: con[c][k+"_ic95"] = _ci(samples[("c",c,k)])
    nat = np.isin(d.cat.to_numpy(),NATIVE); holder=d.c.eq(1).to_numpy(); complete=d.complete.to_numpy(bool)
    national = {"n_marco":int(len(d)),"masa_marco":_mass(w,np.ones(len(d),bool)),"cobertura_completa":_mass(w,complete)/_mass(w,holder),
                "media_completos":_mean(d.v.to_numpy(float)[complete],w[complete]),"mediana_completos":weighted_quantile(d.v.to_numpy(float)[complete],w[complete],.5),
                "reconstruye_marco":bool(int(sum(v["n_marco"] for v in table.values()))==len(d)),
                "reconstruye_masa":bool(np.isclose(sum(v["masa_marco"] for v in table.values()),_mass(w,np.ones(len(d),bool)))),
                "nativo_masa":_mass(w,nat),"desconocido_masa":_mass(w,~nat)}
    out={"TABLA-CATEGORIAS-JSON":table,"TABLA-CONTRASTES-JSON":con,"CONTROL-NACIONAL-JSON":national,
         "REPLICAS-VALIDAS-JSON":{":".join(map(str,k)):int(np.isfinite(np.asarray(v, dtype=float)).sum()) for k,v in samples.items()},
         "METODO-IC":"BOOTSTRAP-UPM-EN-EDIS-PERCENTIL;CONTRASTES-REPLICAS-COMPARTIDAS",
         "CONTROL-RECONCILIACION":"SI" if national["reconstruye_marco"] and national["reconstruye_masa"] else "NO"}
    return {PREFIX+k:(json.dumps(v,sort_keys=True,separators=(",",":")) if isinstance(v,(dict,list)) else v) for k,v in out.items()}
