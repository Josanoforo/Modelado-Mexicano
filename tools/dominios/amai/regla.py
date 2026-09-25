"""Regla NSE AMAI 2024 · puntos y cortes, transcritos del Anexo de la nota.

Fuente única: «Nivel Socioeconómico AMAI 2024 · Nota Metodológica», Comité
de NSE AMAI, octubre 2023, Anexo «Códigos de Análisis en R», pp. 16-18
(`https://www.amai.org/descargas/NOTA_METODOLOGICA_NSE_AMAI_2024_v6.pdf`,
sha256 `c268c3dc9f39bcc9b4de573429806fb787b141e2219501684e8bd566b87d89d1`,
copia en `data/raw/amai/`). La nota ratifica sin cambios la regla AMAI 2022
bajo el nombre AMAI 2024 (p. 15).

Cada constante de abajo es la del código R del Anexo; no hay una sola cifra
tecleada de otra fuente. Este módulo no lee microdato: recibe los seis
componentes ya construidos por el adaptador de cada instrumento.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

SHA_NOTA = "c268c3dc9f39bcc9b4de573429806fb787b141e2219501684e8bd566b87d89d1"

# Escolaridad del jefe, códigos educa_jefe de ENIGH 01..11 (Anexo p. 16-17).
# 01 sin instrucción y 02 preescolar quedan en 0 (valor inicial del Anexo).
CATEGORIAS_EDUCA = (
    "01-sin-instruccion", "02-preescolar", "03-primaria-incompleta",
    "04-primaria-completa", "05-secundaria-incompleta", "06-secundaria-completa",
    "07-preparatoria-incompleta", "08-preparatoria-completa",
    "09-profesional-incompleta", "10-profesional-completa", "11-posgrado",
)
PUNTOS_EDUCA = {1: 0, 2: 0, 3: 6, 4: 11, 5: 12, 6: 18, 7: 23, 8: 27,
                9: 36, 10: 59, 11: 85}
# Tope superior: el Anexo asigna el valor inicial a todo lo no enumerado.
PUNTOS_BANOS = {0: 0, 1: 24}, 47          # 2 o más -> 47
PUNTOS_AUTOS = {0: 0, 1: 22}, 43          # 2 o más -> 43
PUNTOS_INTERNET = {0: 0, 1: 32}
PUNTOS_OCUPADOS = {0: 0, 1: 15, 2: 31, 3: 46}, 61   # 4 o más -> 61
PUNTOS_DORMITORIOS = {0: 0, 1: 8, 2: 16, 3: 24}, 32  # 4 o más -> 32

# cut(breaks=c(0,47,94,115,140,167,201,300)), intervalos (a,b] (Anexo p. 17).
CORTES = (47, 94, 115, 140, 167, 201)
NIVELES = ("E", "D", "D+", "C-", "C", "C+", "A/B")
# Agrupación primaria de este acto (spec §2, congelada en COMMIT-1).
GRUPOS = {"E": "BAJO", "D": "BAJO", "D+": "BAJO",
          "C-": "MEDIO", "C": "MEDIO",
          "C+": "ALTO", "A/B": "ALTO"}
ORDEN_GRUPOS = ("BAJO", "MEDIO", "ALTO")
COMPONENTES = ("educa_jefe", "banos", "autos", "internet", "ocupados", "dormitorios")

# Distribución nacional publicada de hogares, ENIGH 2022 con la regla vigente:
# nota AMAI 2024, p. 4, Figura 1 (texto extraído con `pdftotext -layout`,
# líneas 125-139 del volcado). Porcentaje de hogares con información completa.
AMAI_2022_PCT = {"E": 8.7, "D": 25.4, "D+": 14.9, "C-": 16.4, "C": 15.3,
                 "C+": 12.0, "A/B": 7.3}


def _tope(valores: pd.Series, tabla: tuple[dict, int]) -> pd.Series:
    mapa, tope = tabla
    v = pd.to_numeric(valores, errors="coerce")
    out = v.map(lambda x: np.nan if pd.isna(x) else mapa.get(int(x), tope))
    if (v < 0).any():
        raise ValueError("conteo negativo")
    return out.astype(float)


def puntos(comp: pd.DataFrame) -> pd.DataFrame:
    """Puntos por componente; NaN si el componente falta (no se imputa aquí)."""
    faltan = set(COMPONENTES) - set(comp.columns)
    if faltan:
        raise ValueError(f"componentes ausentes: {sorted(faltan)}")
    e = pd.to_numeric(comp["educa_jefe"], errors="coerce")
    if not e.dropna().isin(PUNTOS_EDUCA).all():
        raise ValueError("educa_jefe fuera de 1..11")
    i = pd.to_numeric(comp["internet"], errors="coerce")
    if not i.dropna().isin([0, 1]).all():
        raise ValueError("internet fuera de {0,1}")
    return pd.DataFrame({
        "educa_jefe": e.map(PUNTOS_EDUCA).astype(float),
        "banos": _tope(comp["banos"], PUNTOS_BANOS),
        "autos": _tope(comp["autos"], PUNTOS_AUTOS),
        "internet": i.map(PUNTOS_INTERNET).astype(float),
        "ocupados": _tope(comp["ocupados"], PUNTOS_OCUPADOS),
        "dormitorios": _tope(comp["dormitorios"], PUNTOS_DORMITORIOS),
    }, index=comp.index)


def nivel(puntaje: pd.Series) -> pd.Series:
    """Nivel AMAI por intervalos (a,b]. Puntaje 0 -> E (spec §2, INTERPRETACIÓN
    declarada: el `cut` del Anexo deja 0 fuera de (0,47]; aquí se asigna a E y
    la masa con puntaje 0 se reporta aparte). NaN -> NaN."""
    p = pd.to_numeric(puntaje, errors="coerce")
    idx = np.searchsorted(np.array(CORTES), p.to_numpy(), side="left")
    out = pd.Series([NIVELES[k] if k < len(NIVELES) else NIVELES[-1] for k in idx],
                    index=p.index, dtype=object)
    out[p.isna()] = np.nan
    return out


def grupo(niv: pd.Series) -> pd.Series:
    return niv.map(GRUPOS)
