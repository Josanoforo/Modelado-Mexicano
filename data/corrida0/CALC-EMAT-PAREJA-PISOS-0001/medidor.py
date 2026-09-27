#!/usr/bin/env python3
"""CALC-EMAT-PAREJA-PISOS-0001 · pisos de nupcialidad registrada por segmento, EMAT 2010-2023.

ACTO GEN2-COLA-LOTE-1 (25/sep/2026, CAJA), pieza P-EMAT. Contrato humano:
forense/prereg-caja/EMAT-PAREJA-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre microdato EMAT.

QUÉ ESTIMA. EMAT = Estadística de Matrimonios de INEGI: REGISTRO ADMINISTRATIVO, no encuesta.
Unidad MATRIMONIO REGISTRADO (una fila de MATRIyy.dbf) y, para las conductas C-*, CONTRAYENTE
(cada matrimonio aporta dos: campos *_CON1 y *_CON2). Es un conteo completo del registro: no hay
diseño muestral ni error de muestreo, así que cada piso es P (proporción o media exacta del
registro), N (universo) y CONTEO (numerador); sin EE ni IC de diseño. Catorce olas abiertas
(año de registro 2010-2023); 2024 es la más reciente y queda RESERVADA (E.6): la guardia rechaza
toda ruta con 2024. ≥ 3 olas → IC calibrado de persistencia sobre el piso 2023 con ee de diseño
nulo: expit(logit p ± z·√τ²), τ² = media de Δ² en logit entre olas consecutivas (receta común,
`tau2`), por conducta × eje × categoría.

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (input `receta_pisos`), sin editarla.
"""
from __future__ import annotations

import math
import struct
import types
import zipfile

import numpy as np
import pandas as pd

P = "RESULT-EMAT-PAREJA-PISOS"
OLAS = tuple(str(a) for a in range(2010, 2024))
PISO = "2023"
ZIPS = {"emat2010_2014_bd_dbf_zip": ("2010", "2011", "2012", "2013", "2014"),
        "emat2015_2019_bd_dbf_zip": ("2015", "2016", "2017", "2018", "2019"),
        "emat2020_bd_dbf_zip": ("2020",), "emat2021_bd_dbf_zip": ("2021",),
        "emat2022_bd_dbf_zip": ("2022",), "emat2023_bd_dbf_zip": ("2023",)}
INPUTS_REPO = frozenset({"receta_pisos"})
CAMPOS = ("ENT_REGIS", "TAM_LOC_RE", "ANIO_REGIS", "GENERO", "SEXO_CON1", "EDAD_CON1", "ESCOL_CON1",
          "CONACTCON1", "SEXO_CON2", "EDAD_CON2", "ESCOL_CON2", "CONACTCON2")
ENTS = tuple(f"{i:02d}" for i in range(1, 33))
TLOC = {"MENOS-2500": (1, 2, 3), "2500-14999": (4, 5, 6), "15MIL-99MIL": tuple(range(7, 13)),
        "100MIL-MAS": tuple(range(13, 18))}
ESCOL = {"PRIMARIA-O-MENOS": (1, 2, 3, 4), "SECUNDARIA": (5,), "PREPARATORIA": (6,), "PROFESIONAL": (7,)}
EDADES = (("12-19", 12, 19), ("20-24", 20, 24), ("25-29", 25, 29), ("30-34", 30, 34), ("35-39", 35, 39),
          ("40-MAS", 40, 98))
M_CONDUCTAS = ("M-MISMO-SEXO", "M-CON-MENOR-18", "M-AMBOS-TRABAJAN", "M-MISMA-ESCOLARIDAD")
C_CONDUCTAS = ("C-EDAD-MEDIA",) + tuple(f"C-EDAD-{c}" for c, _, _ in EDADES) + ("C-TRABAJA",)
MEDIAS = frozenset({"C-EDAD-MEDIA"})
EJES_M = {"ENT": ENTS, "TLOC": tuple(TLOC)}
EJES_C = {"SEXO": ("HOMBRE", "MUJER"), "ESCOLARIDAD": tuple(ESCOL), "TLOC": tuple(TLOC)}
Z95 = 1.959964
_DIAG = ("FILAS", "ANIO-REGIS-DISTINTO", "GENERO-FUERA-CATALOGO", "EDAD-NE", "SEXO-FUERA-CATALOGO")


class ParoDeGuardia(RuntimeError):
    pass


def _fin(x):
    if x is None:
        return None
    x = float(x)
    return x if math.isfinite(x) else None


def _modulo_desde_bytes(nombre, fuente):
    mod = types.ModuleType(nombre)
    mod.__file__ = f"<{nombre}>"
    exec(compile(fuente, mod.__file__, "exec"), mod.__dict__)
    return mod


def _guardia_inputs(inputs):
    esperados = INPUTS_REPO | set(ZIPS)
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in ZIPS:
        ruta = str(inputs[pid].get("ruta_absoluta") or "")
        if not ruta:
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
        if "2024" in ruta:
            raise ParoDeGuardia(f"`{pid}` resuelve a una ruta de 2024: EMAT 2024 RESERVADA (E.6)")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def lee_dbf(datos: bytes, campos=CAMPOS) -> pd.DataFrame:
    """DBF (dBase III) de ancho fijo → DataFrame de texto con `campos`; borrados fuera."""
    nrec, lcab, lreg = struct.unpack("<IHH", datos[4:12])
    pos, off, meta = 32, 1, {}
    while datos[pos] != 0x0D:
        nombre = datos[pos:pos + 11].split(b"\x00", 1)[0].decode("ascii").upper()
        largo = datos[pos + 16]
        meta[nombre] = (off, largo)
        off += largo
        pos += 32
    faltan = [c for c in campos if c not in meta]
    if faltan:
        raise KeyError(f"campos ausentes en el DBF: {faltan}")
    reg = np.frombuffer(datos, dtype=np.uint8, count=nrec * lreg, offset=lcab).reshape(nrec, lreg)
    vivos = reg[:, 0] != 0x2A
    out = {}
    for c in campos:
        o, n = meta[c]
        col = reg[vivos, o:o + n].copy().view(f"S{n}").ravel()
        out[c] = pd.Series(col).str.decode("latin-1").str.strip()
    return pd.DataFrame(out)


def miembro_ola(nombres, ola):
    """Único MATRIyy.dbf de la ola dentro del ZIP (sin distinguir mayúsculas)."""
    yy = ola[2:]
    cand = [n for n in nombres if n.lower().rsplit("/", 1)[-1] == f"matri{yy}.dbf"]
    if len(cand) != 1:
        raise ParoDeGuardia(f"ola {ola}: se esperaba 1 MATRI{yy}.dbf, hay {cand}")
    return cand[0]


def _num(s):
    return pd.to_numeric(s, errors="coerce").to_numpy(dtype=float)


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, cods in mapa.items():
        out[np.isin(v, cods)] = c
    return out


def _bin(cond, universo):
    y = np.where(cond, 1.0, 0.0)
    y[~np.asarray(universo, dtype=bool)] = np.nan
    return y


def matrimonios(df, ola):
    diag = {"FILAS": int(len(df)), "ANIO-REGIS-DISTINTO": int((_num(df["ANIO_REGIS"]) != int(ola)).sum()),
            "GENERO-FUERA-CATALOGO": int((~np.isin(_num(df["GENERO"]), (1, 2))).sum())}
    e1, e2 = _num(df["EDAD_CON1"]), _num(df["EDAD_CON2"])
    ok1, ok2 = (e1 >= 12) & (e1 <= 98), (e2 >= 12) & (e2 <= 98)
    s1, s2 = _num(df["SEXO_CON1"]), _num(df["SEXO_CON2"])
    diag["EDAD-NE"] = int((~ok1).sum() + (~ok2).sum())
    diag["SEXO-FUERA-CATALOGO"] = int((~np.isin(s1, (1, 2))).sum() + (~np.isin(s2, (1, 2))).sum())
    gen = _num(df["GENERO"])
    menor = (ok1 & (e1 < 18)) | (ok2 & (e2 < 18))
    c1, c2 = _num(df["CONACTCON1"]), _num(df["CONACTCON2"])
    k1, k2 = _num(df["ESCOL_CON1"]), _num(df["ESCOL_CON2"])
    kv = np.isin(k1, range(1, 8)) & np.isin(k2, range(1, 8))
    ys = {
        "M-MISMO-SEXO": _bin(gen == 2, np.isin(gen, (1, 2))),
        "M-CON-MENOR-18": _bin(menor, (ok1 & ok2) | menor),
        "M-AMBOS-TRABAJAN": _bin((c1 == 1) & (c2 == 1), np.isin(c1, (1, 2)) & np.isin(c2, (1, 2))),
        "M-MISMA-ESCOLARIDAD": _bin(k1 == k2, kv),
    }
    ent = pd.Series(df["ENT_REGIS"]).str.zfill(2).to_numpy(dtype=object)
    ejes = {"ENT": ent, "TLOC": _serie_map(_num(df["TAM_LOC_RE"]), TLOC)}
    return ys, ejes, diag


def contrayentes(df):
    tl = _serie_map(_num(df["TAM_LOC_RE"]), TLOC)
    partes = []
    for k in ("1", "2"):
        partes.append(pd.DataFrame({"sexo": _num(df[f"SEXO_CON{k}"]), "edad": _num(df[f"EDAD_CON{k}"]),
                                    "escol": _num(df[f"ESCOL_CON{k}"]), "conact": _num(df[f"CONACTCON{k}"]),
                                    "tloc": tl}))
    c = pd.concat(partes, ignore_index=True)
    e = c["edad"].to_numpy()
    eok = (e >= 12) & (e <= 98)
    ys = {"C-EDAD-MEDIA": np.where(eok, e, np.nan)}
    for cat, lo, hi in EDADES:
        ys[f"C-EDAD-{cat}"] = _bin((e >= lo) & (e <= hi), eok)
    ca = c["conact"].to_numpy()
    ys["C-TRABAJA"] = _bin(ca == 1, np.isin(ca, (1, 2)))
    ejes = {"SEXO": _serie_map(c["sexo"].to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}),
            "ESCOLARIDAD": _serie_map(c["escol"].to_numpy(), ESCOL),
            "TLOC": c["tloc"].to_numpy(dtype=object)}
    return ys, ejes


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def rid_p(conducta, eje, cat, q):
    return f"{P}-{conducta}-{eje}-{cat}-{q}"


def _celdas(ys, ejes_def, ejes):
    """{(conducta, eje, cat): (p, n, conteo)} exactos del registro, un eje a la vez."""
    out = {}
    for nom, y in ys.items():
        y = np.asarray(y, dtype=float)
        base = np.isfinite(y)
        grupos = [("TOTAL", "TODOS", base)]
        for eje, cats in ejes_def.items():
            s = np.asarray(ejes[eje], dtype=object)
            grupos += [(eje, c, base & (s == c)) for c in cats]
        for eje, cat, m in grupos:
            n = int(m.sum())
            tot = float(y[m].sum()) if n else 0.0
            out[(nom, eje, cat)] = (tot / n if n else None, n, tot)
    return out


def _todas(conds, ejes_def):
    for c in conds:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes_def.items()):
            for cat in cats:
                yield c, eje, cat


def persistencia(R, serie):
    """τ² (media de Δ² en logit entre olas consecutivas con p en (0,1)) e IC calibrado del piso."""
    ps = [serie.get(o) for o in OLAS]
    deltas = [R.logit(b) - R.logit(a) for a, b in zip(ps, ps[1:]) if R.abierto(a) and R.abierto(b)]
    t2 = R.tau2(deltas)
    p = serie.get(PISO)
    if t2 is None or not R.abierto(p):
        return t2, None, None
    s = math.sqrt(t2)
    c = R.logit(p)
    return t2, R.expit(c - Z95 * s), R.expit(c + Z95 * s)


def mide(por_ola, R):
    """`por_ola`: {ola: DataFrame con CAMPOS}. Devuelve el diccionario de RESULT."""
    out, series = {}, {}
    for ola in OLAS:
        df = por_ola[ola]
        ym, em, diag = matrimonios(df, ola)
        yc, ec = contrayentes(df)
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diag[k])
        celdas = _celdas(ym, EJES_M, em)
        celdas.update(_celdas(yc, EJES_C, ec))
        for conds, ejes_def in ((M_CONDUCTAS, EJES_M), (C_CONDUCTAS, EJES_C)):
            for c, eje, cat in _todas(conds, ejes_def):
                p, n, tot = celdas.get((c, eje, cat), (None, 0, 0.0))
                out[rid(c, ola, eje, cat, "P")] = _fin(p)
                out[rid(c, ola, eje, cat, "N")] = int(n)
                if c not in MEDIAS:
                    out[rid(c, ola, eje, cat, "CONTEO")] = int(round(tot))
                series.setdefault((c, eje, cat), {})[ola] = _fin(p)
    for conds, ejes_def in ((M_CONDUCTAS, EJES_M), (C_CONDUCTAS, EJES_C)):
        for c, eje, cat in _todas(conds, ejes_def):
            if c in MEDIAS:
                continue
            t2, lo, hi = persistencia(R, series[(c, eje, cat)])
            out[rid_p(c, eje, cat, "TAU2")] = _fin(t2)
            out[rid_p(c, eje, cat, "ICC-LO")] = _fin(lo)
            out[rid_p(c, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    por_ola = {}
    for pid, olas in ZIPS.items():
        with zipfile.ZipFile(inputs[pid]["ruta_absoluta"]) as z:
            nombres = z.namelist()
            for ola in olas:
                por_ola[ola] = lee_dbf(z.read(miembro_ola(nombres, ola)))
    out = mide(por_ola, R)
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "EMAT 2024 -- RESERVADA (E.6), no es input; se abren 2010-2023"
    out[f"{P}-G-NATURALEZA"] = "registro administrativo completo: sin diseno muestral, sin EE ni IC de diseno"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = []
    for ola in OLAS:
        f += [_fila(f"{P}-G-{ola}-{k}", "entero", "filas") for k in _DIAG]
        for conds, ejes_def, uni in ((M_CONDUCTAS, EJES_M, "matrimonios registrados"),
                                     (C_CONDUCTAS, EJES_C, "contrayentes")):
            for c, eje, cat in _todas(conds, ejes_def):
                if c in MEDIAS:
                    f.append(_fila(rid(c, ola, eje, cat, "P"), "flotante", "edad media (años) del registro"))
                else:
                    f.append(_fila(rid(c, ola, eje, cat, "P"), "proporcion", f"proporción exacta de {uni}"))
                f.append(_fila(rid(c, ola, eje, cat, "N"), "entero", f"{uni} en el universo"))
                if c not in MEDIAS:
                    f.append(_fila(rid(c, ola, eje, cat, "CONTEO"), "entero", f"{uni} con la conducta"))
    for conds, ejes_def in ((M_CONDUCTAS, EJES_M), (C_CONDUCTAS, EJES_C)):
        for c, eje, cat in _todas(conds, ejes_def):
            if c in MEDIAS:
                continue
            f += [_fila(rid_p(c, eje, cat, "TAU2"), "flotante", "τ² logit entre olas consecutivas 2010-2023"),
                  _fila(rid_p(c, eje, cat, "ICC-LO"), "proporcion", "IC95 calibrado de persistencia, piso 2023"),
                  _fila(rid_p(c, eje, cat, "ICC-HI"), "proporcion", "IC95 calibrado de persistencia, piso 2023")]
    f += [_fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración"),
          _fila(f"{P}-G-NATURALEZA", "texto", "declaración")]
    return f
