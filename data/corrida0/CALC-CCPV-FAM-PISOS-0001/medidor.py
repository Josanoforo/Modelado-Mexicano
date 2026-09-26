#!/usr/bin/env python3
"""CALC-CCPV-FAM-PISOS-0001 · pisos de estructura del hogar por segmento, Censo 2010 (muestra).

ACTO GEN2-COLA-LOTE-1 (25/sep/2026, CAJA), pieza P-CCPV. Contrato humano:
forense/prereg-caja/CCPV-FAM-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de ejecutar
este archivo sobre microdato censal.

QUÉ ESTIMA. Muestra censal 2010 (cuestionario ampliado), 32 ZIP estatales `MC2010_<ee>_dta`
con `viviendas_<ee>.dta` y `personas_<ee>.dta`. Unidad HOGAR CENSAL (vivienda particular
habitada de la tabla VIVIENDAS, `TIPOHOG` de INEGI) con `factor`; diseño `estrato`/`upm`
(llaves opacas, prefijadas con la entidad). Unidad PERSONA sólo para las conductas PER60-*,
con el `factor` de PERSONAS. Proporciones (y una media) ponderadas por UN eje a la vez,
nunca cruces. La ola 2020 es la más reciente del programa y queda RESERVADA (E.6): ninguna
ruta de input puede resolver a una carpeta 2020. Una ola abierta: sin IC de persistencia.

Lo heredado se ejecuta desde los bytes hasheados de la receta común
`tools/dominios/salud/pisos_diseno.py` (input `receta_pisos`), sin editarla.
"""
from __future__ import annotations

import math
import types

import numpy as np
import pandas as pd

P = "RESULT-CCPV-FAM-PISOS"
OLA = "2010"
ENTS = tuple(f"{i:02d}" for i in range(1, 33))
PAY = {e: f"cc1_inegi_ccpv_2010__mc2010_{e}_dta" for e in ENTS}
INPUTS_REPO = frozenset({"receta_pisos"})
COLS_VIV = ["ent", "id_viv", "tipohog", "numpers", "factor", "estrato", "upm", "tam_loc"]
COLS_PER = ["ent", "id_viv", "sexo", "edad", "parent", "nivacad", "factor", "estrato", "upm", "tam_loc"]

# Códigos por texto (Vivienda.do / Personas.do del propio ZIP, spec §2).
TIPOHOG_VALIDOS = (1, 2, 3, 4, 5, 6)          # 9 = No especificado, fuera del universo
PARENT_VALIDOS = (1, 2, 3, 4, 5, 6, 7, 8, 9)  # 99 = No especificado
HOMBRE, MUJER = 1, 3                          # SEXO2: 1 "Hombre" 3 "Mujer"
EDAD_NE = 999

HOGAR = ("HOG-NUCLEAR", "HOG-AMPLIADO", "HOG-COMPUESTO", "HOG-UNIPERSONAL", "HOG-CORRESIDENTES",
         "HOG-CON-60MAS", "HOG-CON-MENOR-18", "HOG-60MAS-Y-MENOR-18", "HOG-TRES-GENERACIONES",
         "HOG-JEFA-MUJER", "HOG-TAMANO-MEDIO", "AM-HOG-NUCLEAR-O-AMPLIADO", "AM-HOG-UNIPERSONAL")
PERSONA = ("PER60-VIVE-SOLO",)
CONDUCTAS = HOGAR + PERSONA
MEDIAS = frozenset({"HOG-TAMANO-MEDIO"})

ESCOL = {"BASICA-O-MENOS": (0, 1, 2, 3, 5, 6, 7), "MEDIA-SUPERIOR": (4, 8), "SUPERIOR": (9, 10, 11, 12)}
EDADES_JEFE = (("HASTA-29", 0, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
EDADES_AM = (("60-69", 60, 69), ("70-79", 70, 79), ("80-MAS", 80, 130))
TLOC = {"MENOS-2500": (1,), "2500-14999": (2,), "15MIL-99MIL": (3,), "100MIL-MAS": (4,)}
EJES_HOG = {
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": tuple(c for c, _, _ in EDADES_JEFE),
    "ESCOLARIDAD-JEFE": tuple(ESCOL),
    "TLOC": tuple(TLOC),
    "ENT": ENTS,
}
EJES_PER = {
    "SEXO": ("HOMBRE", "MUJER"),
    "EDAD": tuple(c for c, _, _ in EDADES_AM),
    "TLOC": tuple(TLOC),
    "ENT": ENTS,
}
Q = ("P", "EE", "IC-LO", "IC-HI", "N")
_DIAG = ("VIVIENDAS", "PERSONAS", "VIV-DISENO-VALIDO", "PER-DISENO-VALIDO", "VIV-SIN-PERSONAS",
         "VIV-SIN-JEFE", "VIV-JEFE-MULTIPLE", "PER-SEXO-FUERA-CATALOGO", "PER-PARENT-FUERA-CATALOGO",
         "PER-EDAD-NE", "VIV-TIPOHOG-NE")


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
    for e, pid in PAY.items():
        ruta = str(inputs[pid].get("ruta_absoluta") or "")
        if not ruta:
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
        if "2020" in ruta or "/ccpv/2010/" not in ruta or not ruta.endswith(f"MC2010_{e}_dta.zip"):
            raise ParoDeGuardia(f"`{pid}` no resuelve a la muestra 2010 de la entidad {e} (2020 RESERVADA, E.6)")
    if inputs["receta_pisos"].get("bytes") is None:
        raise ParoDeGuardia("receta sin bytes: se exige origen repo")


def rid(conducta, eje, cat, q):
    return f"{P}-{conducta}-{OLA}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _rangos(v, rangos):
    out = np.full(len(v), None, dtype=object)
    for c, lo, hi in rangos:
        out[(v >= lo) & (v <= hi)] = c
    return out


def _diseno(df, R):
    e = df["ent"].astype(str).str.strip().str.zfill(2)
    df["_est"] = e + "|" + df["estrato"].astype(str).str.strip()
    df["_upm"] = df["_est"] + "|" + df["upm"].astype(str).str.strip()
    w = R.num(df["factor"])
    ok = (w.gt(0) & df["estrato"].notna() & df["upm"].notna()
          & df["estrato"].astype(str).str.strip().ne("") & df["upm"].astype(str).str.strip().ne(""))
    df["_w"] = w
    return ok.to_numpy()


def prepara(viv, per, R):
    n = R.num
    diag = {"VIVIENDAS": int(len(viv)), "PERSONAS": int(len(per))}
    viv = viv.copy()
    per = per.copy()
    viv["_kv"] = viv["ent"].astype(str).str.strip().str.zfill(2) + "|" + viv["id_viv"].astype(str).str.strip()
    per["_kv"] = per["ent"].astype(str).str.strip().str.zfill(2) + "|" + per["id_viv"].astype(str).str.strip()
    sexo, edad, par = n(per["sexo"]), n(per["edad"]), n(per["parent"])
    diag["PER-SEXO-FUERA-CATALOGO"] = int((~sexo.isin((HOMBRE, MUJER))).sum())
    diag["PER-PARENT-FUERA-CATALOGO"] = int((~par.isin(PARENT_VALIDOS + (99,))).sum())
    diag["PER-EDAD-NE"] = int((edad.eq(EDAD_NE) | edad.isna()).sum())
    edad_ok = edad.where(edad.between(0, 130))
    per["_edad"] = edad_ok
    per["_par"] = par
    per["_sexo"] = sexo
    ind = pd.DataFrame({
        "_kv": per["_kv"],
        "n60": (edad_ok >= 60).astype(int),
        "nmen": (edad_ok < 18).astype(int),
        "edad_ne": edad_ok.isna().astype(int),
        "par_ne": (~par.isin(PARENT_VALIDOS)).astype(int),
        "hijo": (par == 3).astype(int),
        "nieto": (par == 4).astype(int),
        "ascend": par.isin((6, 7)).astype(int),
        "jefes": (par == 1).astype(int),
    })
    agg = ind.groupby("_kv", sort=False).sum()
    jefes = per[per["_par"] == 1].drop_duplicates("_kv", keep=False).set_index("_kv")
    viv = viv.join(agg, on="_kv")
    diag["VIV-SIN-PERSONAS"] = int(viv["jefes"].isna().sum())
    diag["VIV-JEFE-MULTIPLE"] = int((viv["jefes"] > 1).sum())
    diag["VIV-SIN-JEFE"] = int((viv["jefes"] == 0).sum())
    for c, src in (("sexo_je", "_sexo"), ("edad_je", "_edad"), ("niv_je", "nivacad")):
        viv[c] = viv["_kv"].map(jefes[src]).to_numpy()
    th = n(viv["tipohog"])
    diag["VIV-TIPOHOG-NE"] = int((~th.isin(TIPOHOG_VALIDOS)).sum())
    viv["_th"] = th
    okv = _diseno(viv, R)
    okp = _diseno(per, R)
    diag["VIV-DISENO-VALIDO"] = int(okv.sum())
    diag["PER-DISENO-VALIDO"] = int(okp.sum())
    fv = viv[okv].reset_index(drop=True)
    fp = per[okp].reset_index(drop=True)
    fp["_th"] = fp["_kv"].map(viv.set_index("_kv")["_th"]).to_numpy()
    ejes_h = {
        "SEXO-JEFE": (_serie_map(n(fv["sexo_je"]).to_numpy(), {"HOMBRE": (HOMBRE,), "MUJER": (MUJER,)}),
                      EJES_HOG["SEXO-JEFE"]),
        "EDAD-JEFE": (_rangos(n(fv["edad_je"]).to_numpy(), EDADES_JEFE), EJES_HOG["EDAD-JEFE"]),
        "ESCOLARIDAD-JEFE": (_serie_map(n(fv["niv_je"]).to_numpy(), ESCOL), EJES_HOG["ESCOLARIDAD-JEFE"]),
        "TLOC": (_serie_map(n(fv["tam_loc"]).to_numpy(), TLOC), EJES_HOG["TLOC"]),
        "ENT": (fv["ent"].astype(str).str.strip().str.zfill(2).to_numpy(dtype=object), ENTS),
    }
    ejes_p = {
        "SEXO": (_serie_map(fp["_sexo"].to_numpy(), {"HOMBRE": (HOMBRE,), "MUJER": (MUJER,)}), EJES_PER["SEXO"]),
        "EDAD": (_rangos(fp["_edad"].to_numpy(), EDADES_AM), EJES_PER["EDAD"]),
        "TLOC": (_serie_map(n(fp["tam_loc"]).to_numpy(), TLOC), EJES_PER["TLOC"]),
        "ENT": (fp["ent"].astype(str).str.strip().str.zfill(2).to_numpy(dtype=object), ENTS),
    }
    return fv, fp, ejes_h, ejes_p, diag


def _bin(cond, universo):
    y = np.where(cond, 1.0, 0.0)
    y[~np.asarray(universo, dtype=bool)] = np.nan
    return y


def conducta_hogar(nombre, f, R):
    th = f["_th"].to_numpy()
    tv = np.isin(th, TIPOHOG_VALIDOS)
    edad_ok = (f["edad_ne"].to_numpy() == 0)
    par_ok = (f["par_ne"].to_numpy() == 0)
    n60, nmen = f["n60"].to_numpy(), f["nmen"].to_numpy()
    con60 = n60 > 0
    uni60 = con60 | edad_ok  # se sabe si hay 60+: hay uno, o todas las edades conocidas
    unimen = (nmen > 0) | edad_ok
    simple = {"HOG-NUCLEAR": 1, "HOG-AMPLIADO": 2, "HOG-COMPUESTO": 3, "HOG-UNIPERSONAL": 5,
              "HOG-CORRESIDENTES": 6}
    if nombre in simple:
        return _bin(th == simple[nombre], tv)
    if nombre == "HOG-CON-60MAS":
        return _bin(con60, uni60)
    if nombre == "HOG-CON-MENOR-18":
        return _bin(nmen > 0, unimen)
    if nombre == "HOG-60MAS-Y-MENOR-18":
        return _bin(con60 & (nmen > 0), edad_ok | (con60 & (nmen > 0)))
    if nombre == "HOG-TRES-GENERACIONES":
        tres = (f["nieto"].to_numpy() > 0) | ((f["ascend"].to_numpy() > 0) & (f["hijo"].to_numpy() > 0))
        return _bin(tres, par_ok | tres)
    if nombre == "HOG-JEFA-MUJER":
        s = R.num(f["sexo_je"]).to_numpy()
        return _bin(s == MUJER, np.isin(s, (HOMBRE, MUJER)))
    if nombre == "HOG-TAMANO-MEDIO":
        v = R.num(f["numpers"]).to_numpy().astype(float)
        v[~((v >= 1) & (v <= 60))] = np.nan
        return v
    if nombre == "AM-HOG-NUCLEAR-O-AMPLIADO":
        return _bin(np.isin(th, (1, 2)), tv & con60)
    if nombre == "AM-HOG-UNIPERSONAL":
        return _bin(th == 5, tv & con60)
    raise KeyError(nombre)


def conducta_persona(nombre, f, R):
    if nombre == "PER60-VIVE-SOLO":
        e = f["_edad"].to_numpy()
        th = f["_th"].to_numpy()
        return _bin(th == 5, (e >= 60) & np.isin(th, TIPOHOG_VALIDOS))
    raise KeyError(nombre)


def _vacia(res, conductas, ejes):
    for c in conductas:
        for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes.items()):
            for cat in cats:
                res.setdefault((c, eje, cat), {})


def calcula(res, diag, extra):
    out = {f"{P}-G-{k}": int(diag[k]) for k in _DIAG}
    for conds, ejes in ((HOGAR, EJES_HOG), (PERSONA, EJES_PER)):
        for c in conds:
            for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes.items()):
                for cat in cats:
                    r = res.get((c, eje, cat)) or {}
                    for q, key in (("P", "p"), ("EE", "ee"), ("IC-LO", "lo"), ("IC-HI", "hi")):
                        out[rid(c, eje, cat, q)] = _fin(r.get(key))
                    out[rid(c, eje, cat, "N")] = int(r.get("n", 0))
    out.update(extra)
    return out


def mide(viv, per, R, replicas, semilla):
    fv, fp, ejes_h, ejes_p, diag = prepara(viv, per, R)
    ch = {c: conducta_hogar(c, fv, R) for c in HOGAR}
    cp = {c: conducta_persona(c, fp, R) for c in PERSONA}
    res = R.marginales(fv, ch, ejes_h, fv["_w"].to_numpy(dtype=float), "_est", "_upm", replicas, semilla)
    res.update(R.marginales(fp, cp, ejes_p, fp["_w"].to_numpy(dtype=float), "_est", "_upm", replicas, semilla))
    y = cp["PER60-VIVE-SOLO"]
    tot = float(np.nansum(np.where(y == 1.0, fp["_w"].to_numpy(dtype=float), 0.0)))
    extra = {f"{P}-PER60-VIVE-SOLO-{OLA}-TOTAL-EXPANDIDO": tot}
    return calcula(res, diag, extra)


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos", inputs["receta_pisos"]["bytes"])
    vs, ps = [], []
    for e, pid in PAY.items():
        ruta = inputs[pid]["ruta_absoluta"]
        vs.append(R.lee_dta(ruta, COLS_VIV, miembro=f"viviendas_{e}.dta"))
        ps.append(R.lee_dta(ruta, COLS_PER, miembro=f"personas_{e}.dta"))
    out = mide(pd.concat(vs, ignore_index=True), pd.concat(ps, ignore_index=True), R, replicas, semilla)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "CCPV 2020 -- RESERVADA (E.6), no es input; se abre sólo la muestra 2010"
    return out


def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = [_fila(f"{P}-G-{k}", "entero", "filas") for k in _DIAG]
    for conds, ejes, uni in ((HOGAR, EJES_HOG, "hogares"), (PERSONA, EJES_PER, "personas 60+")):
        for c in conds:
            tipo_p = "flotante" if c in MEDIAS else "proporcion"
            und = "media ponderada de personas por hogar" if c in MEDIAS else f"proporción ponderada de {uni}"
            for eje, cats in [("TOTAL", ("TODOS",))] + list(ejes.items()):
                for cat in cats:
                    lohi = "flotante" if c in MEDIAS else "proporcion"
                    f += [_fila(rid(c, eje, cat, "P"), tipo_p, und),
                          _fila(rid(c, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                          _fila(rid(c, eje, cat, "IC-LO"), lohi, "IC95 diseño, inferior"),
                          _fila(rid(c, eje, cat, "IC-HI"), lohi, "IC95 diseño, superior"),
                          _fila(rid(c, eje, cat, "N"), "entero", f"{uni} sin ponderar")]
    f += [_fila(f"{P}-PER60-VIVE-SOLO-{OLA}-TOTAL-EXPANDIDO", "flotante", "personas 60+ (suma de factor)"),
          _fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
