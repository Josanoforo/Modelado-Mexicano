#!/usr/bin/env python3
"""Lectores de payload · ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1.

Los consumen los medidores del acto (CALC-ENADID-FAMILIA-HOGARES-0001,
CALC-ENASIC-CUIDADOS-VEJEZ-0001, CALC-PEW-MIGRACION-MEX-0001) como input `origen: repo`
fijado por sha256 y ejecutado desde sus bytes. La estimación (bootstrap, resumen,
persistencia, IC calibrado) NO vive aquí: es la receta común
`tools/dominios/salud/pisos_diseno.py`, también por sha256.

QUÉ HACE, y nada más: lee columnas pedidas (nombres exactos, sin distinguir mayúsculas)
de un miembro DBF, CSV o SAV dentro de un ZIP y las devuelve como texto en MINÚSCULAS de
columna. Una columna pedida que no existe levanta KeyError con su nombre. No filtra
filas, no recodifica, no elige universos — salvo `lee_sav_zip(..., filtro=(col, valor))`,
que devuelve sólo las filas con `col == valor` (el país de una encuesta multinacional),
aplicado antes de devolver nada.
"""
from __future__ import annotations

import io
import tempfile
import zipfile
from pathlib import Path

import pandas as pd


def _miembro(z, nombre):
    """Nombre real del miembro `nombre` (sin distinguir mayúsculas, con o sin carpeta)."""
    cand = [n for n in z.namelist()
            if not n.startswith("__MACOSX") and Path(n).name.lower() == nombre.lower()]
    if len(cand) != 1:
        raise ValueError(f"se esperaba 1 miembro {nombre}, hay {len(cand)}: {cand}")
    return cand[0]


def _mapea(reales, columnas, miembro):
    faltan = [c for c in columnas if c.lower() not in reales]
    if faltan:
        raise KeyError(f"columnas ausentes en {miembro}: {faltan}")
    return [reales[c.lower()] for c in columnas]


def lee_csv_zip(ruta_zip, miembro, columnas):
    with zipfile.ZipFile(ruta_zip) as z:
        raw = z.read(_miembro(z, miembro))
    try:
        texto = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = raw.decode("latin-1")
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    cab = pd.read_csv(io.StringIO(texto), nrows=0)
    reales = {str(c).strip().lower(): c for c in cab.columns}
    usar = _mapea(reales, columnas, miembro)
    df = pd.read_csv(io.StringIO(texto), usecols=usar, dtype=str, keep_default_na=False)
    df = df[usar]
    df.columns = [c.lower() for c in columnas]
    return df


def lee_dbf_zip(ruta_zip, miembro, columnas, encoding="latin-1"):
    from dbfread import DBF

    with zipfile.ZipFile(ruta_zip) as z, tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp) / "t.dbf"
        destino.write_bytes(z.read(_miembro(z, miembro)))
        tabla = DBF(str(destino), encoding=encoding, load=False, char_decode_errors="replace")
        reales = {f.lower(): f for f in tabla.field_names}
        usar = _mapea(reales, columnas, miembro)
        filas = [[("" if r[c] is None else str(r[c])) for c in usar] for r in tabla]
    return pd.DataFrame(filas, columns=[c.lower() for c in columnas], dtype=str)


def lee_sav_zip(ruta_zip, columnas, filtro=None):
    import pyreadstat

    with zipfile.ZipFile(ruta_zip) as z, tempfile.TemporaryDirectory() as tmp:
        sav = [n for n in z.namelist() if n.lower().endswith(".sav") and not n.startswith("__MACOSX")]
        if len(sav) != 1:
            raise ValueError(f"se esperaba 1 .sav, hay {len(sav)}")
        destino = Path(tmp) / "t.sav"
        destino.write_bytes(z.read(sav[0]))
        _, meta = pyreadstat.read_sav(str(destino), metadataonly=True)
        reales = {c.lower(): c for c in meta.column_names}
        pedidas = list(columnas) + ([filtro[0]] if filtro and filtro[0] not in columnas else [])
        usar = _mapea(reales, pedidas, sav[0])
        df, _ = pyreadstat.read_sav(str(destino), usecols=usar, apply_value_formats=False)
    df = df[usar]
    df.columns = [c.lower() for c in pedidas]
    if filtro:
        df = df[pd.to_numeric(df[filtro[0].lower()], errors="coerce") == float(filtro[1])]
        df = df.reset_index(drop=True)
    return df[[c.lower() for c in columnas]]
