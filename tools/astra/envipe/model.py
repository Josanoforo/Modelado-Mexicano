"""C-ASTRA: historical interaction forecast. No evaluation microdata entry point."""
from __future__ import annotations

import hashlib
import importlib.util
import math
import textwrap
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[3]
GUARD = ROOT / "tools/celda_d/marginales_reproduccion.py"
GUARD_SHA = "4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6"
TRANSITIVE = {
    "tools/ejes_maestra35_l1.py": "502f5a4138c6733677f9472947cfe8c112dd04618e6ac325dd816758f7206c4d",
    "tools/calibracion_mordida_encig_serie.py": "b2e636b059538e43c57f4f1a288e028c796ef34965186c5bbb771bea5a462bd3",
}
PAIRS = {
    "EDADXSEXO": ("edad", "sexo"),
    "ESCOLARIDADPROXYXSEXO": ("escolaridad_proxy", "sexo"),
    "DOMINIOXSEXO": ("dominio_urbano_rural", "sexo"),
    "EDADXESCOLARIDADPROXY": ("edad", "escolaridad_proxy"),
}
ORDER = {
    "edad": ["18-29", "30-44", "45-59", "60+"],
    "sexo": ["1 Hombre", "2 Mujer"],
    "escolaridad_proxy": ["hasta primaria", "secundaria", "media superior", "superior"],
    "dominio_urbano_rural": ["Rural", "Complemento urbano", "Urbano"],
    "nacional": ["NAC"],
}


def logit(p):
    p = np.asarray(p, dtype=float)
    if np.any(~np.isfinite(p)) or np.any((p <= 0) | (p >= 1)):
        raise ValueError("probability outside (0,1)")
    return np.log(p) - np.log1p(-p)


def expit(x):
    x = np.asarray(x, dtype=float)
    return np.where(x >= 0, 1 / (1 + np.exp(-np.clip(x, -700, 700))),
                    np.exp(np.clip(x, -700, 700)) / (1 + np.exp(np.clip(x, -700, 700))))


def guarded_history(path, year):
    path = Path(path)
    if year not in (2023, 2024) or path.name != f"envipe{year}_csv.zip":
        raise ValueError("only named ENVIPE 2023/2024 historical payloads allowed")
    if hashlib.sha256(GUARD.read_bytes()).hexdigest() != GUARD_SHA:
        raise ValueError("historical reader dependency hash changed")
    for name, expected in TRANSITIVE.items():
        if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f"historical reader transitive dependency changed: {name}")
    spec = importlib.util.spec_from_file_location("astra_historical_guard", GUARD)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.carga_ola(path, year, reservada=False), module


def public_marginals(raw: bytes):
    """Extract only the named, already sealed entry, without parsing other entries."""
    text = raw.decode("utf-8")
    marker = "  - id: tramite.evasion_norma_ejes_envipe2025\n"
    if text.count(marker) != 1:
        raise ValueError("public marginal entry absent or duplicated")
    block = text.split(marker, 1)[1].split("\n  - id: ", 1)[0]
    entry = yaml.safe_load(textwrap.dedent(marker + block))[0]
    out = {"nacional": {"NAC": 0.562774}}
    for axis in entry["ejes"]:
        out[axis["eje"]] = {c["celda"]: float(c["p"]) for c in axis["celdas"]}
    return out


def historical_interactions(ola, guard, pair, seed, n_rep):
    """One shared stratified UPM draw per year for every overlapping cell."""
    a, b = PAIRS[pair]
    df = ola.df
    reps = guard.replicas_compartidas(ola, seed, n_rep)
    masks = {("nacional", "NAC"): np.ones(len(df), dtype=bool)}
    for axis in (a, b):
        for category in ORDER[axis]:
            masks[(axis, category)] = df[axis].to_numpy() == category
    for ca in ORDER[a]:
        for cb in ORDER[b]:
            masks[("cross", ca, cb)] = masks[(a, ca)] & masks[(b, cb)]
    weights = df["_w"].to_numpy(dtype=float)
    outcomes = df["_y"].to_numpy(dtype=float)
    keys = list(masks)
    W = np.column_stack([np.bincount(reps.pos_fila, weights=weights * masks[k],
                                     minlength=reps.n_upm) for k in keys])
    Y = np.column_stack([np.bincount(reps.pos_fila, weights=weights * outcomes * masks[k],
                                     minlength=reps.n_upm) for k in keys])
    point_den, point_num = W.sum(axis=0), Y.sum(axis=0)
    p0 = np.divide(point_num, point_den, out=np.full_like(point_num, np.nan),
                   where=point_den > 0)
    rep_den = reps.counts.astype(float) @ W
    rep_num = reps.counts.astype(float) @ Y
    pr = np.divide(rep_num, rep_den, out=np.full_like(rep_num, np.nan),
                   where=rep_den > 0)
    # Fixed boundary rule: empirical proportions clipped before logit.
    eps = 1e-6
    p0 = np.clip(p0, eps, 1 - eps)
    pr = np.clip(pr, eps, 1 - eps)
    idx = {key: i for i, key in enumerate(keys)}
    out = {}
    for ca in ORDER[a]:
        for cb in ORDER[b]:
            cell = (ca, cb)
            relevant = [idx[("cross", ca, cb)], idx[(a, ca)],
                        idx[(b, cb)], idx[("nacional", "NAC")]]
            if not np.all(np.isfinite(p0[relevant])) or not np.all(np.isfinite(pr[:, relevant])):
                out[cell] = None
                continue
            def interaction(p):
                return (logit(p[..., idx[("cross", ca, cb)]])
                        - logit(p[..., idx[(a, ca)]])
                        - logit(p[..., idx[(b, cb)]])
                        + logit(p[..., idx[("nacional", "NAC")]]))
            out[cell] = (float(interaction(p0)), np.asarray(interaction(pr)))
    return out, ola.meta


def forecast(h23, h24, base, seed, n_draw=2048):
    """Pooled moment EB with two historical waves and cell specific sampling noise."""
    excluded = {c for c in h23 if h23[c] is None or h24[c] is None}
    cells = [c for c in h23 if c not in excluded]
    if not cells:
        return {c: None for c in h23}, {"tau2": None, "q": None}
    x = np.array([h23[c][0] for c in cells])
    y = np.array([h24[c][0] for c in cells])
    v23 = np.array([np.var(h23[c][1], ddof=1) for c in cells])
    v24 = np.array([np.var(h24[c][1], ddof=1) for c in cells])
    tau2 = max(0., float(np.median(x * y)))
    q = max(0.0004, float(np.median((y - x)**2 - v23 - v24)) / 2)
    rng = np.random.Generator(np.random.PCG64(seed))
    ix = rng.integers(0, len(h23[cells[0]][1]), n_draw)
    iy = rng.integers(0, len(h24[cells[0]][1]), n_draw)
    xdraw = np.stack([h23[c][1][ix] for c in cells], axis=1)
    ydraw = np.stack([h24[c][1][iy] for c in cells], axis=1)
    tau_draw = np.maximum(0, np.median(xdraw * ydraw, axis=1))
    q_draw = np.maximum(0.0004, np.median((ydraw - xdraw)**2 - v23 - v24, axis=1) / 2)
    out = {}
    for i, cell in enumerate(cells):
        pa, pb, pn = base[cell]
        c2log = float(logit(pa) + logit(pb) - logit(pn))
        if tau2 == 0:
            mean, postvar = 0., 0.
        else:
            precision = 1 / tau2 + 1 / (v23[i] + q) + 1 / v24[i]
            postvar = 1 / precision
            mean = postvar * (x[i] / (v23[i] + q) + y[i] / v24[i])
        positive = tau_draw > 0
        draw_var = np.zeros(n_draw)
        draw_mean = np.zeros(n_draw)
        draw_var[positive] = 1 / (1 / tau_draw[positive]
            + 1 / (v23[i] + q_draw[positive]) + 1 / v24[i])
        draw_mean[positive] = draw_var[positive] * (
            xdraw[positive, i] / (v23[i] + q_draw[positive])
            + ydraw[positive, i] / v24[i])
        draws = expit(c2log + draw_mean
            + rng.normal(0, np.sqrt(draw_var + q_draw), n_draw))
        point = float(expit(c2log + mean))
        out[cell] = (point, float(np.quantile(draws, .025)), float(np.quantile(draws, .975)),
                     float(mean), float(v23[i]), float(v24[i]))
    out.update({c: None for c in excluded})
    return out, {"tau2": tau2, "q": q}


def run(pair, paths, public_bytes, seed=20260922, n_rep=256):
    if pair not in PAIRS or len(paths) != 2:
        raise ValueError("invalid pair/history")
    public = public_marginals(public_bytes)
    a, b = PAIRS[pair]
    h = {}
    meta = {}
    for year, path in zip((2023, 2024), paths):
        ola, guard = guarded_history(path, year)
        h[year], meta[year] = historical_interactions(ola, guard, pair, seed + year, n_rep)
    base = {(ca, cb): (public[a][ca], public[b][cb], public["nacional"]["NAC"])
            for ca in ORDER[a] for cb in ORDER[b]}
    return forecast(h[2023], h[2024], base, seed), meta
