#!/usr/bin/env python3
"""CALC-EDR-SUICIDIO-PISOS-0001 · pisos de mortalidad por suicidio registrada, EDR 2015-2023.

ACTO GEN2-COLA-LOTE-1 (25/sep/2026, CAJA), pieza P-EDR. Contrato humano:
forense/prereg-caja/EDR-SUICIDIO-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre microdato EDR.

QUÉ ESTIMA. EDR = Estadística de Defunciones Registradas de INEGI: REGISTRO ADMINISTRATIVO.
Unidad DEFUNCIÓN REGISTRADA (una fila de DEFUNyy.dbf), nunca persona encuestada (encargo §2,
§4). Ola = año de registro del archivo. Conteo completo: sin diseño ni error de muestreo; cada
celda es P exacta, N (universo) y CONTEO. Sin población en corpus: NO hay tasas por habitante.
Nueve olas abiertas (2015-2023); 2024 es la más reciente y queda RESERVADA (E.6): la guardia
rechaza toda ruta con 2024. ≥ 3 olas → IC calibrado de persistencia sobre el piso 2023 con ee
nulo: expit(logit p ± z·√τ²).

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

P = "RESULT-EDR-SUICIDIO-PISOS"
OLAS = tuple(str(a) for a in range(2015, 2024))
PISO = "2023"
ZIPS = {"edr2015_2019_bd_dbf_zip": ("2015", "2016", "2017", "2018", "2019"),
        "cc1_inegi_mortalidad_2020__defunciones_base_datos_2020_dbf": ("2020",),
        "cc1_inegi_edr_2021__defunciones_base_datos_2021_dbf": ("2021",),
        "edr2022_bd_dbf_zip": ("2022",),
        "cc1_inegi_edr_2023__defunciones_base_datos_2023_dbf": ("2023",)}
INPUTS_REPO = frozenset({"receta_pisos"})
CAMPOS_BASE = ("ENT_RESID", "TLOC_RESID", "CAUSA_DEF", "SEXO", "EDAD", "ANIO_OCUR", "ANIO_REGIS", "ESCOLARIDA")
PRESUNTO = {o: ("PRESUNTO" if int(o) <= 2021 else "TIPO_DEFUN") for o in OLAS}  # 3 = Suicidio en ambos
ENTS = tuple(f"{i:02d}" for i in range(1, 33))
TLOC = {"MENOS-2500": (1, 2, 3), "2500-14999": (4, 5, 6), "15MIL-99MIL": tuple(range(7, 13)),
        "100MIL-MAS": tuple(range(13, 18))}
ESCOL = {"PRIMARIA-O-MENOS": (1, 2, 3, 4), "SECUNDARIA": (5, 6), "MEDIA-SUPERIOR": (7, 8), "SUPERIOR": (9, 10)}
EDADES = (("0-9", 0, 9), ("10-14", 10, 14), ("15-19", 15, 19), ("20-24", 20, 24), ("25-29", 25, 29),
          ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 120))
CONDUCTAS = ("SUICIDIO-CIE", "SUICIDIO-PRESUNTO", "SUIC-HOMBRE", "SUIC-15-44", "SUIC-15-29",
             "SUIC-OCURRIDO-EN-OLA")
EJES = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": tuple(c for c, _, _ in EDADES), "ENT": ENTS,
        "TLOC": tuple(TLOC), "ESCOLARIDAD": tuple(ESCOL)}
Z95 = 1.959964
_DIAG = ("FILAS", "CAUSA-VACIA", "EDAD-NE", "SEXO-NE", "SUICIDIOS-CIE", "SUICIDIOS-PRESUNTO",
         "CIE-Y-PRESUNTO", "CIE-NO-PRESUNTO", "PRESUNTO-NO-CIE")


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
            raise ParoDeGuardia(f"`{pid}` resuelve a una ruta de 2024: EDR 2024 RESERVADA (E.6)")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def lee_dbf(datos: bytes, campos) -> pd.DataFrame:
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
    yy = ola[2:]
    cand = [n for n in nombres if n.lower().rsplit("/", 1)[-1] == f"defun{yy}.dbf"]
    if len(cand) != 1:
        raise ParoDeGuardia(f"ola {ola}: se esperaba 1 DEFUN{yy}.dbf, hay {cand}")
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


def es_suicidio_cie(causa):
    """CIE-10 X60–X84 (lesiones autoinfligidas intencionalmente), 3 o 4 caracteres."""
    c = pd.Series(causa).astype(str).str.upper().str.strip()
    return c.str.match(r"^X(6[0-9]|7[0-9]|8[0-4])").to_numpy(dtype=bool)


def años(edad):
    """EDAD N(4): 1xxx horas, 2xxx días, 3xxx meses → 0 años; 4001–4120 → años; x098, 4998 y resto → NaN."""
    e = np.asarray(edad, dtype=float)
    out = np.full(len(e), np.nan)
    out[(e >= 1001) & (e <= 3098) & ~np.isin(e, (1098, 2098, 3098))] = 0.0
    anios = (e >= 4001) & (e <= 4120)
    out[anios] = e[anios] - 4000
    return out


def prepara(df, ola):
    causa = df["CAUSA_DEF"]
    cie = es_suicidio_cie(causa)
    pres = _num(df[PRESUNTO[ola]]) == 3
    sexo = _num(df["SEXO"])
    edad = años(_num(df["EDAD"]))
    diag = {"FILAS": int(len(df)), "CAUSA-VACIA": int((causa.astype(str).str.strip() == "").sum()),
            "EDAD-NE": int(np.isnan(edad).sum()), "SEXO-NE": int((~np.isin(sexo, (1, 2))).sum()),
            "SUICIDIOS-CIE": int(cie.sum()), "SUICIDIOS-PRESUNTO": int(pres.sum()),
            "CIE-Y-PRESUNTO": int((cie & pres).sum()), "CIE-NO-PRESUNTO": int((cie & ~pres).sum()),
            "PRESUNTO-NO-CIE": int((~cie & pres).sum())}
    causa_ok = causa.astype(str).str.strip().ne("").to_numpy()
    edad_ok = np.isfinite(edad)
    ys = {
        "SUICIDIO-CIE": _bin(cie, causa_ok),
        "SUICIDIO-PRESUNTO": _bin(pres, np.ones(len(df), dtype=bool)),
        "SUIC-HOMBRE": _bin(sexo == 1, cie & np.isin(sexo, (1, 2))),
        "SUIC-15-44": _bin((edad >= 15) & (edad <= 44), cie & edad_ok),
        "SUIC-15-29": _bin((edad >= 15) & (edad <= 29), cie & edad_ok),
        "SUIC-OCURRIDO-EN-OLA": _bin(_num(df["ANIO_OCUR"]) == int(ola), cie),
    }
    ecat = np.full(len(df), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ejes = {"SEXO": _serie_map(sexo, {"HOMBRE": (1,), "MUJER": (2,)}), "EDAD": ecat,
            "ENT": pd.Series(df["ENT_RESID"]).astype(str).str.zfill(2).to_numpy(dtype=object),
            "TLOC": _serie_map(_num(df["TLOC_RESID"]), TLOC),
            "ESCOLARIDAD": _serie_map(_num(df["ESCOLARIDA"]), ESCOL)}
    return ys, ejes, diag


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def rid_p(conducta, eje, cat, q):
    return f"{P}-{conducta}-{eje}-{cat}-{q}"


def _ejes_de(conducta):
    """Un eje no se cruza consigo mismo: SUIC-HOMBRE no va por SEXO; SUIC-15-* no van por EDAD."""
    if conducta == "SUIC-HOMBRE":
        return {k: v for k, v in EJES.items() if k != "SEXO"}
    if conducta in ("SUIC-15-44", "SUIC-15-29"):
        return {k: v for k, v in EJES.items() if k != "EDAD"}
    return EJES


def _todas():
    for c in CONDUCTAS:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(_ejes_de(c).items()):
            for cat in cats:
                yield c, eje, cat


def _celdas(ys, ejes):
    out = {}
    for c in CONDUCTAS:
        y = np.asarray(ys[c], dtype=float)
        base = np.isfinite(y)
        grupos = [("TOTAL", "TODOS", base)]
        for eje, cats in _ejes_de(c).items():
            s = np.asarray(ejes[eje], dtype=object)
            grupos += [(eje, k, base & (s == k)) for k in cats]
        for eje, cat, m in grupos:
            n = int(m.sum())
            tot = float(y[m].sum()) if n else 0.0
            out[(c, eje, cat)] = (tot / n if n else None, n, tot)
    return out


def persistencia(R, serie):
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
    out, series = {}, {}
    for ola in OLAS:
        ys, ejes, diag = prepara(por_ola[ola], ola)
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diag[k])
        celdas = _celdas(ys, ejes)
        for c, eje, cat in _todas():
            p, n, tot = celdas[(c, eje, cat)]
            out[rid(c, ola, eje, cat, "P")] = _fin(p)
            out[rid(c, ola, eje, cat, "N")] = int(n)
            out[rid(c, ola, eje, cat, "CONTEO")] = int(round(tot))
            series.setdefault((c, eje, cat), {})[ola] = _fin(p)
    for c, eje, cat in _todas():
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
                por_ola[ola] = lee_dbf(z.read(miembro_ola(nombres, ola)), CAMPOS_BASE + (PRESUNTO[ola],))
    out = mide(por_ola, R)
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "EDR 2024 -- RESERVADA (E.6), no es input; se abren 2015-2023"
    out[f"{P}-G-NATURALEZA"] = ("registro administrativo completo de defunciones: unidad defuncion, sin diseno, "
                                "sin EE ni IC de diseno, sin tasas (no hay poblacion en corpus)")
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
        for c, eje, cat in _todas():
            f += [_fila(rid(c, ola, eje, cat, "P"), "proporcion", "proporción exacta de defunciones registradas"),
                  _fila(rid(c, ola, eje, cat, "N"), "entero", "defunciones en el universo"),
                  _fila(rid(c, ola, eje, cat, "CONTEO"), "entero", "defunciones con la condición")]
    for c, eje, cat in _todas():
        f += [_fila(rid_p(c, eje, cat, "TAU2"), "flotante", "τ² logit entre olas consecutivas 2015-2023"),
              _fila(rid_p(c, eje, cat, "ICC-LO"), "proporcion", "IC95 calibrado de persistencia, piso 2023"),
              _fila(rid_p(c, eje, cat, "ICC-HI"), "proporcion", "IC95 calibrado de persistencia, piso 2023")]
    f += [_fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración"),
          _fila(f"{P}-G-NATURALEZA", "texto", "declaración")]
    return f
