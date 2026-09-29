"""Lector DBF por columnas autorizadas.

La cabecera (lista de campos) se lee con dbfread (load=False, no toca registros).
Los registros se leen como bytes y solo se cortan los rangos de las columnas
autorizadas; ninguna otra columna se decodifica. Filas marcadas como borradas
('*') se descartan ("filas vivas").
"""
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "paquete/lib")
from dbfread import DBF  # noqa: E402

COMUNES = ["SEXO", "EDAD", "CAUSA_DEF", "ANIO_OCUR", "ANIO_REGIS",
           "ENT_RESID", "TLOC_RESID", "ESCOLARIDA"]
AUTORIZADAS = {
    **{y: COMUNES + ["PRESUNTO"] for y in range(2015, 2022)},
    **{y: COMUNES + ["TIPO_DEFUN"] for y in (2022, 2023)},
}


def ruta(ola):
    return f"paquete/datos/defun{ola % 100:02d}.dbf"


def cabecera(ola):
    t = DBF(ruta(ola), load=False)
    campos = [(f.name.upper(), f.type, f.length) for f in t.fields]
    return t.header, campos


def lee(ola):
    """Devuelve (DataFrame de strings sin espacios, info)."""
    header, campos = cabecera(ola)
    reclen = header.recordlen
    nrec = header.numrecords
    assert 1 + sum(c[2] for c in campos) == reclen, "offsets de campos no secuenciales"
    offs = {}
    pos = 1
    for nombre, _tipo, largo in campos:
        offs[nombre] = (pos, largo)
        pos += largo
    raw = np.fromfile(ruta(ola), dtype=np.uint8, count=nrec * reclen,
                      offset=header.headerlen)
    assert raw.size == nrec * reclen, "archivo truncado"
    raw = raw.reshape(nrec, reclen)
    vivas = raw[:, 0] != ord("*")
    out = {}
    for col in AUTORIZADAS[ola]:
        ini, largo = offs[col]
        b = np.ascontiguousarray(raw[vivas, ini:ini + largo]).view(f"S{largo}").ravel()
        out[col] = pd.Series(b).str.decode("latin-1").str.strip()
    info = {"registros_cabecera": int(nrec), "filas_vivas": int(vivas.sum()),
            "filas_borradas": int((~vivas).sum()),
            "campos": [c[0] for c in campos]}
    return pd.DataFrame(out), info
