#!/usr/bin/env python3
"""CALC-ENPECYT-CONOC-PISOS-0001 · pisos de actitudes hacia la ciencia por segmento, ENPECYT 2011-2015.

ACTO GEN2-COLA-LOTE-1 (25/sep/2026, CAJA), pieza P-ENPECYT. Contrato humano:
forense/prereg-caja/ENPECYT-CONOC-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre microdato ENPECYT.

QUÉ ESTIMA. Persona elegida de 18+ en viviendas de las ciudades autorrepresentadas (universo de la
encuesta: áreas urbanas de 100 000+ habitantes). Ponderador `FAC` de la tabla CB1 (las tres olas);
diseño `EST_DIS`/`UPM_DIS` de CS en 2013 y 2015, anidados en la ciudad (llaves opacas). 2011 no trae
estrato ni UPM de diseño: su piso es P ponderada y N, sin EE ni IC (declarado, no inventado).
Proporciones ponderadas por UN eje a la vez. Olas 2011, 2013, 2015 abiertas; 2017 es la más
reciente del programa y queda RESERVADA (E.6): la guardia rechaza toda ruta con 2017. 2005-2009
fuera (estructura y factor distintos; spec §0). Tres olas → IC calibrado de persistencia sobre el
piso 2015: expit(logit p ± z·√(ee² + τ²)) con la receta común (`ic_calibrado`).

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

P = "RESULT-ENPECYT-CONOC-PISOS"
OLAS = ("2011", "2013", "2015")
PISO = "2015"
PAY = {"2011": "cc1_inegi_enpecyt_2011__enpecyt2011_bd_dbf",
       "2013": "cc1_inegi_enpecyt_2013__enpecyt2013_bd_dbf",
       "2015": "cc1_inegi_enpecyt_2015__enpecyt2015_bd_dbf"}
INPUTS_REPO = frozenset({"receta_pisos"})
CIUDAD = {"2011": "CD", "2013": "CD_A", "2015": "CD_A"}
LLAVE = ("PER", "CON", "V_SEL", "N_HOG", "N_REN")
# Reactivo → (tabla, campo) por ola, por texto de pregunta (spec §0/§2).
ITEMS = {
    "2011": {"INTERES": ("cb1", "S4P1_3"), "GOB": ("cb2", "S4P26_1"), "FE": ("cb2", "S4P33_2_1"),
             "BOMBERO": ("cb1", "S4P14_13"), "ENFERMERA": ("cb1", "S4P14_14"), "INVESTIGADOR": ("cb1", "S4P14_4")},
    "2013": {"INTERES": ("cb1", "S4P1_3"), "GOB": ("cb2", "S4P26_1"), "FE": ("cb2", "S4P33_2_1"),
             "BOMBERO": ("cb1", "S4P14_13"), "ENFERMERA": ("cb1", "S4P14_14"), "INVESTIGADOR": ("cb1", "S4P14_4")},
    "2015": {"INTERES": ("cb1", "S4P1_3"), "GOB": ("cb2", "S4P25_1"), "FE": ("cb2", "S4P31_1_1"),
             "BOMBERO": ("cb1", "S4P14_12"), "ENFERMERA": ("cb1", "S4P14_13"), "INVESTIGADOR": ("cb1", "S4P14_16"),
             "INVENTOR": ("cb1", "S4P14_17")},
}
CONDUCTAS = ("INTERES-AL-MENOS-MODERADO", "INTERES-GRANDE-O-MAS", "GOB-INVERTIR-ACUERDO",
             "GOB-INVERTIR-ACUERDO-SIN-NS", "FE-CIENCIA-ACUERDO", "FE-CIENCIA-ACUERDO-SIN-NS",
             "RESPETA-10-BOMBERO", "RESPETA-10-ENFERMERA", "RESPETA-10-INVESTIGADOR", "RESPETA-10-INVENTOR")
SOLO_2015 = frozenset({"RESPETA-10-INVENTOR"})
ESCOL = {"BASICA-O-MENOS": (0, 1, 2, 3), "MEDIA": (4, 5, 6), "SUPERIOR": (7, 8, 9, 10)}
EDADES = (("18-29", 18, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 120))
EJES = {"SEXO": ("HOMBRE", "MUJER"), "EDAD": tuple(c for c, _, _ in EDADES), "ESCOLARIDAD": tuple(ESCOL)}
_DIAG = ("CB1", "CB2", "CS", "JOIN-SIN-CB2", "JOIN-SIN-CS", "LLAVE-DUPLICADA", "FAC-INVALIDO",
         "DISENO-VALIDO")


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
    esperados = INPUTS_REPO | set(PAY.values())
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for ola, pid in PAY.items():
        ruta = str(inputs[pid].get("ruta_absoluta") or "")
        if not ruta:
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
        if "2017" in ruta or f"enpecyt{ola}_bd_dbf" not in ruta:
            raise ParoDeGuardia(f"`{pid}` no resuelve a la ola {ola} (2017 RESERVADA, E.6)")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def lee_dbf(datos: bytes, campos) -> pd.DataFrame:
    """DBF (dBase III) de ancho fijo → DataFrame de texto con `campos`; borrados fuera."""
    nrec, lcab, lreg = struct.unpack("<IHH", datos[4:12])
    pos, off, meta = 32, 1, {}
    while datos[pos] != 0x0D:
        nombre = datos[pos:pos + 11].split(b"\x00", 1)[0].decode("ascii").upper()
        meta[nombre] = (off, datos[pos + 16])
        off += datos[pos + 16]
        pos += 32
    faltan = [c for c in campos if c not in meta]
    if faltan:
        raise KeyError(f"campos ausentes en el DBF: {faltan}")
    reg = np.frombuffer(datos, dtype=np.uint8, count=nrec * lreg, offset=lcab).reshape(nrec, lreg)
    vivos = reg[:, 0] != 0x2A
    out = {}
    for c in dict.fromkeys(campos):
        o, n = meta[c]
        out[c] = pd.Series(reg[vivos, o:o + n].copy().view(f"S{n}").ravel()).str.decode("latin-1").str.strip()
    return pd.DataFrame(out)


def miembro(nombres, ola, tabla):
    cand = [n for n in nombres if n.lower() == f"enpecyt{ola}_{tabla}.dbf"]
    if len(cand) != 1:
        raise ParoDeGuardia(f"ola {ola}: se esperaba 1 enpecyt{ola}_{tabla}.dbf, hay {cand}")
    return cand[0]


def campos_de(ola):
    llave = (CIUDAD[ola],) + LLAVE
    cb1 = llave + tuple(c for t, c in ITEMS[ola].values() if t == "cb1") + ("FAC",)
    cb2 = llave + tuple(c for t, c in ITEMS[ola].values() if t == "cb2")
    cs = llave + ("SEX", "EDA", "NIV") + (("EST_DIS", "UPM_DIS") if ola != "2011" else ())
    return {"cb1": cb1, "cb2": cb2, "cs": cs}


def _num(s):
    return pd.to_numeric(pd.Series(s), errors="coerce").to_numpy(dtype=float)


def _k(df, cols):
    return df[list(cols)].astype(str).apply(lambda s: s.str.strip()).agg("|".join, axis=1)


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, cods in mapa.items():
        out[np.isin(v, cods)] = c
    return out


def _bin(cond, universo):
    y = np.where(cond, 1.0, 0.0)
    y[~np.asarray(universo, dtype=bool)] = np.nan
    return y


def prepara(tablas, ola):
    cd = CIUDAD[ola]
    llave = (cd,) + LLAVE
    cb1, cb2, cs = (tablas[t].copy() for t in ("cb1", "cb2", "cs"))
    diag = {"CB1": int(len(cb1)), "CB2": int(len(cb2)), "CS": int(len(cs))}
    for df in (cb1, cb2, cs):
        df["_k"] = _k(df, llave)
    diag["LLAVE-DUPLICADA"] = int(cb1["_k"].duplicated(keep=False).sum())
    f = cb1.drop_duplicates("_k", keep=False).reset_index(drop=True)
    c2 = cb2.drop_duplicates("_k", keep=False).set_index("_k")
    s = cs.drop_duplicates("_k", keep=False).set_index("_k")
    diag["JOIN-SIN-CB2"] = int((~f["_k"].isin(c2.index)).sum())
    diag["JOIN-SIN-CS"] = int((~f["_k"].isin(s.index)).sum())
    for t, c in ITEMS[ola].values():
        if t == "cb2":
            f[c] = f["_k"].map(c2[c]).to_numpy()
    for c in ("SEX", "EDA", "NIV") + (("EST_DIS", "UPM_DIS") if ola != "2011" else ()):
        f[c] = f["_k"].map(s[c]).to_numpy()
    w = _num(f["FAC"])
    okw = np.isfinite(w) & (w > 0)
    diag["FAC-INVALIDO"] = int((~okw).sum())
    if ola == "2011":
        ok = okw
        f["_est"], f["_upm"] = "", ""
    else:
        est, upm = f["EST_DIS"].astype(str).str.strip(), f["UPM_DIS"].astype(str).str.strip()
        ok = okw & f["EST_DIS"].notna().to_numpy() & f["UPM_DIS"].notna().to_numpy() & est.ne("").to_numpy() \
            & upm.ne("").to_numpy()
        f["_est"] = f[cd].astype(str).str.strip() + "|" + est
        f["_upm"] = f["_est"] + "|" + upm
    diag["DISENO-VALIDO"] = int(ok.sum())
    f = f[ok].reset_index(drop=True)
    f["_w"] = w[ok]
    edad = _num(f["EDA"])
    ecat = np.full(len(f), None, dtype=object)
    for c, lo, hi in EDADES:
        ecat[(edad >= lo) & (edad <= hi)] = c
    ejes = {"SEXO": (_serie_map(_num(f["SEX"]), {"HOMBRE": (1,), "MUJER": (2,)}), EJES["SEXO"]),
            "EDAD": (ecat, EJES["EDAD"]),
            "ESCOLARIDAD": (_serie_map(_num(f["NIV"]), ESCOL), EJES["ESCOLARIDAD"])}
    return f, ejes, diag


def conducta_y(nombre, f, ola):
    it = ITEMS[ola]

    def v(k):
        return _num(f[it[k][1]])
    if nombre == "INTERES-AL-MENOS-MODERADO":
        x = v("INTERES")
        return _bin(np.isin(x, (1, 2, 3)), np.isin(x, (1, 2, 3, 4)))
    if nombre == "INTERES-GRANDE-O-MAS":
        x = v("INTERES")
        return _bin(np.isin(x, (1, 2)), np.isin(x, (1, 2, 3, 4)))
    for pre, k in (("GOB-INVERTIR", "GOB"), ("FE-CIENCIA", "FE")):
        if nombre == f"{pre}-ACUERDO":
            x = v(k)
            return _bin(np.isin(x, (1, 2)), np.isin(x, (1, 2, 3, 4, 5)))
        if nombre == f"{pre}-ACUERDO-SIN-NS":
            x = v(k)
            return _bin(np.isin(x, (1, 2)), np.isin(x, (1, 2, 3, 4)))
    for prof in ("BOMBERO", "ENFERMERA", "INVESTIGADOR", "INVENTOR"):
        if nombre == f"RESPETA-10-{prof}":
            if prof not in it:
                return np.full(len(f), np.nan)
            x = v(prof)
            return _bin(x == 10, (x >= 1) & (x <= 10))
    raise KeyError(nombre)


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def rid_p(conducta, eje, cat, q):
    return f"{P}-{conducta}-{eje}-{cat}-{q}"


def _olas_de(c):
    return ("2015",) if c in SOLO_2015 else OLAS


def _celdas_sin_diseno(f, conds, ejes):
    """Ola sin estrato/UPM (2011): P ponderada y N; sin EE ni IC."""
    w = f["_w"].to_numpy(dtype=float)
    out = {}
    for c, y in conds.items():
        y = np.asarray(y, dtype=float)
        base = np.isfinite(y)
        grupos = [("TOTAL", "TODOS", base)] + [(e, k, base & (np.asarray(s, dtype=object) == k))
                                              for e, (s, cats) in ejes.items() for k in cats]
        for e, k, m in grupos:
            n = int(m.sum())
            den = float(w[m].sum())
            out[(c, e, k)] = {"p": float((w[m] * y[m]).sum() / den) if n and den > 0 else None, "n": n}
    return out


def _todas():
    for eje, cats in [("TOTAL", ("TODOS",))] + list(EJES.items()):
        for cat in cats:
            yield eje, cat


def mide(por_ola, R, replicas, semilla):
    out, series = {}, {}
    for ola in OLAS:
        f, ejes, diag = prepara(por_ola[ola], ola)
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diag[k])
        conds = {c: conducta_y(c, f, ola) for c in CONDUCTAS if ola in _olas_de(c)}
        if ola == "2011":
            res = _celdas_sin_diseno(f, conds, ejes)
        else:
            res = R.marginales(f, conds, ejes, f["_w"].to_numpy(dtype=float), "_est", "_upm", replicas, semilla)
        for c in conds:
            for eje, cat in _todas():
                r = res.get((c, eje, cat)) or {}
                for q, key in (("P", "p"), ("EE", "ee"), ("IC-LO", "lo"), ("IC-HI", "hi")):
                    out[rid(c, ola, eje, cat, q)] = _fin(r.get(key))
                out[rid(c, ola, eje, cat, "N")] = int(r.get("n", 0))
                series.setdefault((c, eje, cat), {})[ola] = (_fin(r.get("p")), _fin(r.get("lo")), _fin(r.get("hi")))
    for c in CONDUCTAS:
        if c in SOLO_2015:
            continue
        for eje, cat in _todas():
            s = series[(c, eje, cat)]
            ps = [s[o][0] for o in OLAS]
            deltas = [R.logit(b) - R.logit(a) for a, b in zip(ps, ps[1:]) if R.abierto(a) and R.abierto(b)]
            t2 = R.tau2(deltas)
            lo, hi = R.ic_calibrado(*s[PISO], t2)
            out[rid_p(c, eje, cat, "TAU2")] = _fin(t2)
            out[rid_p(c, eje, cat, "ICC-LO")] = _fin(lo)
            out[rid_p(c, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    por_ola = {}
    for ola, pid in PAY.items():
        with zipfile.ZipFile(inputs[pid]["ruta_absoluta"]) as z:
            nombres = z.namelist()
            por_ola[ola] = {t: lee_dbf(z.read(miembro(nombres, ola, t)), cols) for t, cols in campos_de(ola).items()}
    out = mide(por_ola, R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENPECYT 2017 -- RESERVADA (E.6), no es input; se abren 2011, 2013, 2015"
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
        for c in CONDUCTAS:
            if ola not in _olas_de(c):
                continue
            for eje, cat in _todas():
                f += [_fila(rid(c, ola, eje, cat, "P"), "proporcion", "proporción ponderada de personas 18+"),
                      _fila(rid(c, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                      _fila(rid(c, ola, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                      _fila(rid(c, ola, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                      _fila(rid(c, ola, eje, cat, "N"), "entero", "personas sin ponderar")]
    for c in CONDUCTAS:
        if c in SOLO_2015:
            continue
        for eje, cat in _todas():
            f += [_fila(rid_p(c, eje, cat, "TAU2"), "flotante", "τ² logit entre olas consecutivas 2011-2015"),
                  _fila(rid_p(c, eje, cat, "ICC-LO"), "proporcion", "IC95 calibrado de persistencia, piso 2015"),
                  _fila(rid_p(c, eje, cat, "ICC-HI"), "proporcion", "IC95 calibrado de persistencia, piso 2015")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
