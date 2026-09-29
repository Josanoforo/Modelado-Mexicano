"""Lectura de microdato limitada a las columnas autorizadas (FIRMAS-Y-ACCESO / encargo)."""
import os
import pickle
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd

DATOS = os.path.join("paquete", "datos")
COLS_VIV = ["ent", "id_viv", "tipohog", "numpers", "factor", "estrato", "upm", "tam_loc"]
COLS_PER = ["ent", "id_viv", "sexo", "edad", "parent", "nivacad", "factor", "estrato", "upm", "tam_loc"]
ENTS = ["%02d" % i for i in range(1, 33)]
CHUNK = 400_000


def ruta(tipo, ee):
    return os.path.join(DATOS, "%s_%s.dta" % (tipo, ee))


def variables(path):
    """Lista completa de variables (solo encabezado)."""
    if _version(path) == 110:
        import sys
        if os.path.join("paquete", "lib") not in sys.path:
            sys.path.insert(0, os.path.join("paquete", "lib"))
        import pyreadstat
        _, meta = pyreadstat.read_dta(path, metadataonly=True)
        return list(meta.column_names)
    with pd.io.stata.StataReader(path) as r:
        return list(r.variable_labels().keys())


def _num(s):
    return pd.to_numeric(s, errors="coerce").astype("float64")


def _str(s):
    return s.astype(str).str.strip()


def _version(path):
    with open(path, "rb") as f:
        return f.read(1)[0]


def _trozos(path, cols):
    """pandas.read_stata; para formato Stata 110 (no soportado por pandas) usa pyreadstat."""
    if _version(path) == 110:
        import sys
        if os.path.join("paquete", "lib") not in sys.path:
            sys.path.insert(0, os.path.join("paquete", "lib"))
        import pyreadstat
        off = 0
        while True:
            ch, _ = pyreadstat.read_dta(path, usecols=cols, row_offset=off, row_limit=CHUNK,
                                        apply_value_formats=False)
            if len(ch) == 0:
                break
            yield ch[cols]
            off += len(ch)
            if len(ch) < CHUNK:
                break
        return
    with pd.read_stata(path, columns=cols, convert_categoricals=False,
                       convert_missing=False, iterator=True, chunksize=CHUNK) as it:
        for ch in it:
            yield ch


def _lee(args):
    tipo, ee = args
    path = ruta(tipo, ee)
    cols = COLS_VIV if tipo == "viv" else COLS_PER
    partes = []
    for ch in _trozos(path, cols):
        if True:
            d = {}
            for c in cols:
                if c == "id_viv":
                    v = _str(ch[c].fillna(""))
                    if not v.str.fullmatch(r"\d+").all():
                        raise ValueError("id_viv no numerico en %s" % path)
                    d[c] = v.astype("int64")
                elif c in ("ent", "estrato", "upm"):
                    d[c] = _str(ch[c].fillna(""))
                else:
                    d[c] = _num(ch[c])
            partes.append(pd.DataFrame(d))
    df = pd.concat(partes, ignore_index=True)
    return tipo, ee, path, df


def carga(cache=None, workers=6):
    """Devuelve (viv, per, rutas_leidas, varlists)."""
    if cache and os.path.exists(cache):
        with open(cache, "rb") as f:
            return pickle.load(f)
    tareas = [(t, e) for e in ENTS for t in ("viv", "per")]
    varlists = {ruta(t, e): variables(ruta(t, e)) for t, e in tareas}
    viv, per, rutas = [], [], []
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("fork")) as ex:
        for tipo, ee, path, df in ex.map(_lee, tareas):
            rutas.append(path)
            (viv if tipo == "viv" else per).append(df)
    viv = pd.concat(viv, ignore_index=True)
    per = pd.concat(per, ignore_index=True)
    for df in (viv, per):
        for c in ("ent", "estrato", "upm"):
            df[c] = df[c].astype("category")
    out = (viv, per, sorted(set(rutas)), varlists)
    if cache:
        with open(cache, "wb") as f:
            pickle.dump(out, f, protocol=4)
    return out
