"""Aproximación declarada para ENDUTIH: puntos esperados de lo no preguntado.

Contrato: `forense/prereg-caja/AMAI-NSE-spec-v1_0.md` §4.3. ENDUTIH no pregunta
baños ni dormitorios y sólo pregunta auto sí/no. Los puntos de esos tres
componentes se sustituyen por su media ponderada en ENIGH 2022 (la base de la
propia regla AMAI) dentro de la celda de lo que ENDUTIH sí observa:
(educa_jefe 1..11, internet 0/1, ocupados 0..4+, con_auto 0/1). Celda con
menos de `N_CELDA` hogares donantes: se cae a (educa_jefe, internet, con_auto)
y luego a (con_auto). Imputación determinista; no hay azar.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tools.dominios.amai import regla

N_CELDA = 30
NIVELES_CELDA = (
    ("educa_jefe", "internet", "ocup4", "con_auto"),
    ("educa_jefe", "internet", "con_auto"),
    ("con_auto",),
)


def _claves(comp: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "educa_jefe": comp["educa_jefe"],
        "internet": comp["internet"],
        "ocup4": np.minimum(comp["ocupados"], 4),
        "con_auto": (comp["autos"] > 0).astype(float).where(comp["autos"].notna()),
    }, index=comp.index)


def tabla_donante(enigh: pd.DataFrame) -> dict:
    """Media ponderada (factor de hogar) de puntos baños+dormitorios+autos por
    celda, sobre hogares ENIGH 2022 con los seis componentes válidos."""
    pts = regla.puntos(enigh[list(regla.COMPONENTES)])
    completo = pts.notna().all(axis=1)
    faltante = (pts["banos"] + pts["dormitorios"] + pts["autos"])[completo]
    claves = _claves(enigh[list(regla.COMPONENTES)])[completo]
    w = enigh.loc[completo, "factor"].astype(float)
    tabla = {}
    for nivel in NIVELES_CELDA:
        g = pd.DataFrame({"k": list(map(tuple, claves[list(nivel)].to_numpy())),
                          "wy": w * faltante, "w": w})
        agg = g.groupby("k").agg(wy=("wy", "sum"), w=("w", "sum"), n=("w", "size"))
        tabla[nivel] = {k: (float(r.wy / r.w), int(r.n)) for k, r in agg.iterrows()}
    return {"tabla": tabla, "n_donantes": int(completo.sum())}


def imputa(comp: pd.DataFrame, donante: dict) -> tuple[pd.Series, pd.Series]:
    """Puntos imputados de baños+dormitorios+autos por hogar y el nivel de
    celda usado (0, 1, 2; -1 = sin celda). NaN si falta una llave."""
    claves = _claves(comp)
    valor = pd.Series(np.nan, index=comp.index)
    usado = pd.Series(-1, index=comp.index, dtype=int)
    for i, nivel in enumerate(NIVELES_CELDA):
        t = donante["tabla"][nivel]
        pendiente = valor.isna() & claves[list(nivel)].notna().all(axis=1)
        for idx in claves.index[pendiente]:
            k = tuple(claves.loc[idx, list(nivel)].to_numpy())
            v = t.get(k)
            if v is not None and v[1] >= N_CELDA:
                valor[idx] = v[0]
                usado[idx] = i
    return valor, usado


def puntos_observados_endutih(comp: pd.DataFrame) -> pd.Series:
    """Puntos de educación, internet y ocupados (lo que ENDUTIH sí observa)."""
    base = comp.copy()
    for c in ("banos", "autos", "dormitorios"):
        base[c] = 0
    p = regla.puntos(base[list(regla.COMPONENTES)])
    return p["educa_jefe"] + p["internet"] + p["ocupados"]
