"""Razones por dominio geográfico con un plan común de UPM por ola.

El adaptador usa la interfaz Ola de marginales_reproduccion.py por su hash.
ID_DEL es una clave sintética de filas para la guarda de esa interfaz; nunca
sale en resultados. Ninguna fila se filtra antes de formar las réplicas.
"""
from __future__ import annotations

import hashlib
import math
from pathlib import Path

import numpy as np
import pandas as pd

from tools.celda_d import marginales_reproduccion as compartidas

SHA_COMPARTIDAS = "4df2c630179c194345594d959d012b7dd18d94ac93fab3f48b8f6683753dafd6"
ESTADOS = ("PUBLICABLE", "SUPRIMIDA-N", "NO-REPRESENTATIVA",
           "VARIANZA-NO-ESTIMABLE", "SIN-COMPARABILIDAD")


def verifica_import() -> None:
    ruta = Path(compartidas.__file__)
    actual = hashlib.sha256(ruta.read_bytes()).hexdigest()
    if actual != SHA_COMPARTIDAS:
        raise RuntimeError(f"replicas_compartidas cambió: {actual}")


def _texto(col: pd.Series) -> pd.Series:
    return col.astype(str).str.strip().str.strip('"')


def estima_dominios(
    df: pd.DataFrame, geografia: pd.Series, denominador: pd.Series,
    numerador: pd.Series, *, factor: str, estrato: str, upm: str,
    dominios: list[str], representativos: set[str], semilla: int,
    replicas: int = 1000, n_min: int = 200,
) -> tuple[list[dict], dict]:
    """Punto = suma(w*y*D*G)/suma(w*D*G); IC percentil de réplicas.

    La máscara D conserva la unidad declarada por el llamador. `n` cuenta
    sus filas, no UPM, hogares ni eventos independientes. Todos los dominios
    de la ola comparten las mismas réplicas del marco completo.
    """
    verifica_import()
    if not (len(df) == len(geografia) == len(denominador) == len(numerador)):
        raise ValueError("longitudes discordantes")
    if replicas < 2 or n_min < 1:
        raise ValueError("réplicas o n_min inválidos")
    d = df.reset_index(drop=True).copy()
    d["EST_DIS"] = _texto(d[estrato])
    d["UPM_DIS"] = _texto(d[upm])
    d["_w"] = pd.to_numeric(d[factor], errors="coerce")
    if d["_w"].isna().any() or (d["_w"] <= 0).any():
        raise ValueError("factor no positivo o inválido")
    if d["EST_DIS"].eq("").any() or d["UPM_DIS"].eq("").any():
        raise ValueError("estrato o UPM vacío")
    d["ID_DEL"] = [str(i) for i in range(len(d))]
    d["_y"] = 0.0  # la interfaz pide esta columna; cada conducta usa su y.
    ola = compartidas.Ola(0, d, compartidas._huella(d), False, {})
    rep = compartidas.replicas_compartidas(ola, semilla, replicas)
    geo = _texto(geografia.reset_index(drop=True)).to_numpy()
    den = denominador.reset_index(drop=True).fillna(False).astype(bool).to_numpy()
    num = numerador.reset_index(drop=True).fillna(False).astype(bool).to_numpy()
    if np.any(num & ~den):
        raise ValueError("numerador fuera del denominador")
    w = d["_w"].to_numpy(dtype=float)
    filas = []
    for nombre in dominios:
        mascara = den & (geo == nombre)
        n = int(mascara.sum())
        fila = {"geografia": nombre, "n": n, "n_numerador": int((num & mascara).sum()),
                "punto": None, "ic_inf": None, "ic_sup": None,
                "n_efectivo_kish": None, "upm_dominio": 0, "estado": None,
                "replicas_p": None}
        if nombre not in representativos:
            fila["estado"] = "NO-REPRESENTATIVA"
        elif n < n_min:
            fila["estado"] = "SUPRIMIDA-N"
        if n:
            pesos = w[mascara]
            fila["n_efectivo_kish"] = float(pesos.sum() ** 2 / np.square(pesos).sum())
            fila["upm_dominio"] = int(np.unique(rep.pos_fila[mascara]).size)
        if fila["estado"]:
            filas.append(fila)
            continue
        wd = w * mascara
        wy = wd * num
        total_d = float(wd.sum())
        if total_d <= 0:
            fila["estado"] = "VARIANZA-NO-ESTIMABLE"
            filas.append(fila)
            continue
        p = float(wy.sum() / total_d)
        td = np.bincount(rep.pos_fila, weights=wd, minlength=rep.n_upm)
        ty = np.bincount(rep.pos_fila, weights=wy, minlength=rep.n_upm)
        den_rep = rep.counts @ td
        num_rep = rep.counts @ ty
        if np.any(den_rep <= 0) or fila["upm_dominio"] < 2:
            fila["estado"] = "VARIANZA-NO-ESTIMABLE"
        else:
            p_rep = num_rep / den_rep
            if not np.all(np.isfinite(p_rep)) or np.std(p_rep, ddof=1) <= 0:
                fila["estado"] = "VARIANZA-NO-ESTIMABLE"
            else:
                fila.update(punto=p, ic_inf=float(np.quantile(p_rep, .025)),
                            ic_sup=float(np.quantile(p_rep, .975)), estado="PUBLICABLE",
                            replicas_p=p_rep.tolist())
        filas.append(fila)
    meta = {"semilla": semilla, "replicas": replicas, "upm_marco": rep.n_upm,
            "estratos_upm_unica": rep.estratos_upm_unica,
            "metodo": "bootstrap UPM con reposición dentro de estrato; percentiles 2.5/97.5",
            "sha_modulo_compartido": SHA_COMPARTIDAS}
    return filas, meta
