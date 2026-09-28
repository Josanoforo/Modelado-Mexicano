"""CALC-ENCIG2023-CONFIANZA-PISOS-0001 · pisos de confianza institucional, ENCIG 2023, por eje.

ACTO GEN2-PISOS-Y-ADENDAS-1 (P1, firma H4 (a), 28/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/ENCIG2023-CONFIANZA-PISOS-spec-v1_0.md, congelado en el COMMIT-1 junto con
este archivo, antes de abrir el microdato. Autocontenido: no importa nada de tools/.

Unidad persona 18+ (informante seleccionado, sección XI). Estimando por institución y celda:
proporción ponderada (FAC_P18) de «mucha» o «algo de confianza» (11.1 = 1 ó 2) entre quienes
respondieron 1–4; 5 (no aplica) y 9 (no sabe / no responde) fuera del denominador y contados
aparte. IC: bootstrap de UPM con reposición dentro de estrato sobre el marco entero.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd

PAYLOAD = "encig23_base_datos_csv"
M_SEC11 = "encig2023_01_sec_11.csv"
M_RES = "encig2023_02_residentes_sec_2.csv"
P = "RESULT-ENCIG2023-CONF"
ITEMS = [f"{i:02d}" for i in range(1, 26)]
EJES = (
    ("NACIONAL", ("MX",)),
    ("ENTIDAD", tuple(f"{i:02d}" for i in range(1, 33))),
    ("SEXO", ("HOMBRE", "MUJER")),
    ("EDAD", ("18-29", "30-44", "45-59", "60-MAS")),
    ("ESCOLARIDAD", ("NINGUNA", "BASICA", "MEDIA-SUPERIOR", "SUPERIOR")),
)
ESTADISTICOS = ("P", "IC-LO", "IC-HI", "EE", "N")
GLOBALES = ("FILAS-SEC11", "FILAS-MARCO", "FILAS-SIN-ENLACE-RESIDENTES", "UPM", "ESTRATOS")


def _entero(serie):
    """Texto recortado -> entero; lo no convertible queda NaN (sin código)."""
    return pd.to_numeric(serie.astype(str).str.strip(), errors="coerce")


def _csv(zip_path, miembro, cols):
    with zipfile.ZipFile(zip_path) as z:
        nombres = [n for n in z.namelist() if n.rsplit("/", 1)[-1] == miembro]
        if len(nombres) != 1:
            raise ValueError(f"miembro {miembro}: {len(nombres)} coincidencias")
        crudo = z.read(nombres[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            texto = crudo.decode(enc)
        except UnicodeDecodeError:
            continue
        d = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False, na_filter=False)
        d.columns = [c.strip().lstrip("﻿") for c in d.columns]
        faltan = [c for c in cols if c not in d.columns]
        if faltan:
            raise ValueError(f"{miembro}: faltan columnas {faltan}")
        return d[cols].copy()
    raise ValueError(f"{miembro}: sin codificación útil")


def ejes_de(d):
    """Categoría de cada eje por fila (None = sin categoría en ese eje)."""
    ent = _entero(d["CVE_ENT"])
    sexo = _entero(d["SEXO"])
    edad = _entero(d["EDAD"])
    niv = _entero(d["NIV"])
    out = {"NACIONAL": pd.Series("MX", index=d.index)}
    out["ENTIDAD"] = ent.map(lambda x: f"{int(x):02d}" if x == x and 1 <= x <= 32 and x == int(x) else None)
    out["SEXO"] = sexo.map({1: "HOMBRE", 2: "MUJER"})
    out["EDAD"] = edad.map(lambda x: None if x != x else "18-29" if 18 <= x <= 29 else
                           "30-44" if 30 <= x <= 44 else "45-59" if 45 <= x <= 59 else
                           "60-MAS" if 60 <= x <= 97 else None)
    out["ESCOLARIDAD"] = niv.map({0: "NINGUNA", 1: "NINGUNA", 2: "BASICA", 3: "BASICA",
                                  4: "MEDIA-SUPERIOR", 5: "MEDIA-SUPERIOR", 6: "MEDIA-SUPERIOR",
                                  7: "SUPERIOR", 8: "SUPERIOR", 9: "SUPERIOR"})
    return {k: v.where(v.notna(), None) for k, v in out.items()}


def multiplicadores(est, upm, replicas, seed):
    """Matriz R x K de conteos de remuestreo de UPM dentro de estrato (claves ordenadas)."""
    claves = sorted(set(zip(est, upm)))
    pos = {k: i for i, k in enumerate(claves)}
    por_estrato = {}
    for k in claves:
        por_estrato.setdefault(k[0], []).append(pos[k])
    rng = np.random.Generator(np.random.PCG64(seed))
    M = np.zeros((replicas, len(claves)), dtype=np.float64)
    filas = np.arange(replicas)[:, None]
    for h in sorted(por_estrato):
        ix = np.asarray(por_estrato[h])
        sorteo = rng.integers(0, len(ix), size=(replicas, len(ix)))
        np.add.at(M, (np.broadcast_to(filas, sorteo.shape), ix[sorteo]), 1.0)
    return claves, pos, M


def esquema_resultados():
    ids = [f"{P}-{g}" for g in GLOBALES]
    ids += [f"{P}-EJE-{e}-N-SIN-CATEGORIA" for e, _ in EJES]
    for it in ITEMS:
        ids += [f"{P}-I{it}-N-NO-APLICA", f"{P}-I{it}-N-NSNR", f"{P}-I{it}-N-OTRO"]
        for e, cats in EJES:
            for c in cats:
                ids += [f"{P}-I{it}-{e}-{c}-{s}" for s in ESTADISTICOS]
    return ids


def medir(inputs, contrato):
    zp = inputs[PAYLOAD]["ruta_absoluta"]
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    items = [f"P11_1_{i}" for i in ITEMS]
    a = _csv(zp, M_SEC11, ["ID_PER", "CVE_ENT", "EST_DIS", "UPM_DIS", "FAC_P18"] + items)
    r = _csv(zp, M_RES, ["ID_PER", "SEXO", "EDAD", "NIV"])
    a["ID_PER"] = a["ID_PER"].str.strip()
    r["ID_PER"] = r["ID_PER"].str.strip()
    out = {f"{P}-FILAS-SEC11": int(len(a))}
    d = a.merge(r, on="ID_PER", how="left", validate="m:1", indicator=True)
    d["_w"] = pd.to_numeric(d["FAC_P18"].str.strip(), errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip()
    d["_upm"] = d["UPM_DIS"].str.strip()
    ok = np.isfinite(d["_w"]) & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    d = d.loc[ok].reset_index(drop=True)
    for c in ("SEXO", "EDAD", "NIV"):
        d[c] = d[c].fillna("")
    out[f"{P}-FILAS-MARCO"] = int(len(d))
    out[f"{P}-FILAS-SIN-ENLACE-RESIDENTES"] = int((d["_merge"] != "both").sum())
    claves, pos, M = multiplicadores(d["_est"].tolist(), d["_upm"].tolist(), replicas, seed)
    out[f"{P}-UPM"] = len(claves)
    out[f"{P}-ESTRATOS"] = len({k[0] for k in claves})
    kidx = np.fromiter((pos[k] for k in zip(d["_est"], d["_upm"])), dtype=np.int64, count=len(d))
    K = len(claves)
    w = d["_w"].to_numpy(dtype=np.float64)
    ejes = ejes_de(d)
    for e, cats in EJES:
        out[f"{P}-EJE-{e}-N-SIN-CATEGORIA"] = int(ejes[e].isna().sum())
    for it in ITEMS:
        cod = _entero(d[f"P11_1_{it}"])
        valido = cod.isin([1, 2, 3, 4]).to_numpy()
        y = cod.isin([1, 2]).to_numpy().astype(np.float64)
        out[f"{P}-I{it}-N-NO-APLICA"] = int((cod == 5).sum())
        out[f"{P}-I{it}-N-NSNR"] = int((cod == 9).sum())
        out[f"{P}-I{it}-N-OTRO"] = int((~cod.isin([1, 2, 3, 4, 5, 9])).sum())
        for e, cats in EJES:
            cat = ejes[e].to_numpy(dtype=object)
            NUM = np.zeros((K, len(cats)))
            DEN = np.zeros((K, len(cats)))
            nval = []
            for j, c in enumerate(cats):
                m = valido & (cat == c)
                nval.append(int(m.sum()))
                NUM[:, j] = np.bincount(kidx[m], weights=(w * y)[m], minlength=K)
                DEN[:, j] = np.bincount(kidx[m], weights=w[m], minlength=K)
            RN, RD = M @ NUM, M @ DEN
            for j, c in enumerate(cats):
                base = f"{P}-I{it}-{e}-{c}"
                den = DEN[:, j].sum()
                out[f"{base}-N"] = nval[j]
                out[f"{base}-P"] = float(NUM[:, j].sum() / den) if den > 0 else None
                if den > 0 and np.all(RD[:, j] > 0):
                    rep = RN[:, j] / RD[:, j]
                    lo, hi = np.percentile(rep, [2.5, 97.5])
                    out[f"{base}-IC-LO"], out[f"{base}-IC-HI"] = float(lo), float(hi)
                    out[f"{base}-EE"] = float(rep.std(ddof=1))
                else:
                    out[f"{base}-IC-LO"] = out[f"{base}-IC-HI"] = out[f"{base}-EE"] = None
    return out
