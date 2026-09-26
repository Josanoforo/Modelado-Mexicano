#!/usr/bin/env python3
"""CALC-ENADID-FAMILIA-HOGARES-0001 · pisos por segmento ENADID 2009/2014/2018 con IC de diseño.

ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 (25/sep/2026, CAJA). Contrato humano:
forense/prereg-caja/FAMILIA-ENADID-PISOS-spec-v1_0.md, congelado en el COMMIT-1 antes de
ejecutar este archivo sobre ENADID.

QUÉ ESTIMA. Proporciones ponderadas (`FAC_VIV`) de hogares (tabla de hogares) y de
personas residentes (tabla sociodemográfica, con diseño, tamaño y clase de hogar tomados
del hogar por llave), total y por UN eje a la vez; nunca cruces. Diseño público
estrato/UPM de diseño (llaves opacas). Tres olas abiertas (2009, 2014, 2018) → IC calibrado
de persistencia sobre el piso 2018. ENADID 2023 RESERVADA (E.6): no es input, ningún id
suyo se nombra aquí.

Lo heredado se ejecuta desde bytes hasheados: receta común de estimación
`tools/dominios/salud/pisos_diseno.py` (`receta_pisos_salud`) y lectores del acto
`tools/dominios/familia/lectores.py` (`lectores_familia`).
"""
from __future__ import annotations

import math
import types

import numpy as np

P = "RESULT-ENADID-FAMILIA-HOGARES"
OLAS = ("2009", "2014", "2018")
OLA_PISO = "2018"
INPUTS_REPO = frozenset({"receta_pisos_salud", "lectores_familia"})
PAYLOADS = {
    "2009": "cc1_inegi_enadid_2009__base_datos_enadid09_dbf",
    "2014": "cc1_inegi_enadid_2014__base_datos_enadid14_dbf",
    "2018": "enadid2018_bd_csv_zip",
}
_RESERVADA = "enadid2023"  # prefijo de todo id de la ola reservada: nunca input

# Nombres por ola. Hogar: llave, factor, estrato, UPM, tamaño de localidad, clase de hogar,
# sexo/edad/escolaridad del jefe, migración internacional en el hogar, total de integrantes.
HOG = {
    "2009": dict(miembro="tr_viv_hog.dbf", llave=("control", "viv_sel", "hogar"), fac="fac_viv",
                 est="estdis", upm="upm_dis", tloc="tam_loc", cls="cls_hog", sexo_j="sexo_jef",
                 edad_j="edad_jef", niv_j="niv_jef", mig=None, tam="pers_hog"),
    "2014": dict(miembro="thogar.DBF", llave=("llave_hog",), fac="fac_viv", est="est_dis",
                 upm="upm_dis", tloc="tloc", cls="cls_hog", sexo_j="sexo_jefe", edad_j="edad_jefe",
                 niv_j="niv_jefe", mig="mig_hog", tam="tot_per"),
    "2018": dict(miembro="THogar.csv", llave=("llave_hog",), fac="fac_viv", est="est_dis",
                 upm="upm_dis", tloc="tam_loc", cls="cls_hog", sexo_j="sexo_jefe", edad_j="edad_jefe",
                 niv_j="niv_jefe", mig="migra_ho", tam="p2_5"),
}
PER = {
    "2009": dict(miembro="tr_sdem.dbf", llave=("control", "viv_sel", "hogar"), sexo="sexo", edad="edad",
                 paren="par_agrup", niv="niv", conyu="p3_19"),
    "2014": dict(miembro="TSDem.dbf", llave=("llave_hog",), sexo="sexo", edad="edad", paren="paren",
                 niv="niv", conyu="p3_20"),
    "2018": dict(miembro="TSdem.csv", llave=("llave_hog",), sexo="sexo", edad="edad", paren="paren",
                 niv="niv", conyu="p3_21"),
}
# Tamaño de localidad: 2014/2018 1=100 mil+ … 4=<2 500; 2009 INVERTIDO (1=<2 500 … 4=100 mil+).
TLOC = {"2009": {"100MIL-MAS": (4,), "15MIL-99MIL": (3,), "2500-14999": (2,), "MENOS-2500": (1,)},
        "2014": {"100MIL-MAS": (1,), "15MIL-99MIL": (2,), "2500-14999": (3,), "MENOS-2500": (4,)},
        "2018": {"100MIL-MAS": (1,), "15MIL-99MIL": (2,), "2500-14999": (3,), "MENOS-2500": (4,)}}
# Escolaridad (NIV). 2014/2018: 00-02 | 03, 05 | 04, 06, 07 | 08-11. 2009: 00-02 | 03 | 04-06 | 07-09.
ESCOL = {"2009": {"HASTA-PRIMARIA": (0, 1, 2), "SECUNDARIA": (3,), "MEDIA-SUPERIOR": (4, 5, 6),
                  "SUPERIOR": (7, 8, 9)},
         "2014": {"HASTA-PRIMARIA": (0, 1, 2), "SECUNDARIA": (3, 5), "MEDIA-SUPERIOR": (4, 6, 7),
                  "SUPERIOR": (8, 9, 10, 11)},
         "2018": {"HASTA-PRIMARIA": (0, 1, 2), "SECUNDARIA": (3, 5), "MEDIA-SUPERIOR": (4, 6, 7),
                  "SUPERIOR": (8, 9, 10, 11)}}
# Situación conyugal → UNIDO (casado o unión libre) / NO-UNIDO; UL = unión libre, CAS = casado.
CONYU = {"2009": {"UL": (1,), "CAS": (5,), "NO": (2, 3, 4, 6)},
         "2014": {"UL": (1,), "CAS": (6,), "NO": (2, 3, 4, 5, 7)},
         "2018": {"UL": (1,), "CAS": (6,), "NO": (2, 3, 4, 5, 7)}}
HIJO = 3  # PAREN (2014/2018) y PAR_AGRUP (2009): 3 = Hija(o)
PAREN_VALIDO = {"2009": (1, 2, 3, 4, 5, 6, 7, 8), "2014": (1, 2, 3, 4, 5, 6, 7, 8),
                "2018": (1, 2, 3, 4, 5, 6, 7, 8)}

EJES_HOG = {
    "SEXO-JEFE": ("HOMBRE", "MUJER"),
    "EDAD-JEFE": ("12-29", "30-44", "45-59", "60-MAS"),
    "ESCOLARIDAD-JEFE": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
}
EJES_PER = {
    "SEXO": ("HOMBRE", "MUJER"),
    "EDAD": ("00-14", "15-29", "30-44", "45-59", "60-74", "75-MAS"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
    "TLOC": ("100MIL-MAS", "15MIL-99MIL", "2500-14999", "MENOS-2500"),
    "TAMANO-HOGAR": ("1", "2", "3-4", "5-MAS"),
    "CONDICION-PAREJA": ("UNIDO", "NO-UNIDO"),
}
EDAD_JEFE = (("12-29", 12, 29), ("30-44", 30, 44), ("45-59", 45, 59), ("60-MAS", 60, 130))
EDAD_PER = (("00-14", 0, 14), ("15-29", 15, 29), ("30-44", 30, 44), ("45-59", 45, 59),
            ("60-74", 60, 74), ("75-MAS", 75, 130))
TAM = (("1", 1, 1), ("2", 2, 2), ("3-4", 3, 4), ("5-MAS", 5, 99))

# conducta -> unidad
CONDUCTAS = {
    "HOGAR-UNIPERSONAL": "HOGAR",
    "HOGAR-NUCLEAR": "HOGAR",
    "HOGAR-AMPLIADO": "HOGAR",
    "HOGAR-JEFATURA-FEMENINA": "HOGAR",
    "HOGAR-CON-MIGRANTE-INTERNACIONAL-5A": "HOGAR",
    "PERSONA-60MAS": "PERSONA",
    "AM60-VIVE-SOLO": "PERSONA",
    "AM60-EN-HOGAR-AMPLIADO": "PERSONA",
    "JOVEN-25-34-HIJO-DEL-JEFE": "PERSONA",
    "PERSONA-15MAS-UNIDA": "PERSONA",
    "UNIDO-15MAS-EN-UNION-LIBRE": "PERSONA",
}
# conductas preguntadas en menos de 3 olas: sin IC calibrado (spec §4)
MENOS_DE_3_OLAS = {"HOGAR-CON-MIGRANTE-INTERNACIONAL-5A": ("2014", "2018")}
_DIAG = ("FILAS-HOGAR", "FILAS-HOGAR-DISENO-VALIDO", "FILAS-PERSONA", "PERSONA-SIN-HOGAR",
         "FILAS-PERSONA-DISENO-VALIDO")


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
    esperados = INPUTS_REPO | set(PAYLOADS.values())
    if any(str(k).lower().startswith(_RESERVADA) for k in inputs):
        raise ParoDeGuardia("un id de la ola reservada ENADID 2023 llegó como input: PARO (a)")
    if set(inputs) != esperados:
        raise ParoDeGuardia(f"inputs fuera de la lista: {sorted(set(inputs) ^ esperados)}")
    for pid in PAYLOADS.values():
        if not inputs[pid].get("ruta_absoluta"):
            raise ParoDeGuardia(f"payload `{pid}` sin ruta resuelta")
    for rid_ in INPUTS_REPO:
        if inputs[rid_].get("bytes") is None:
            raise ParoDeGuardia(f"{rid_} sin bytes: se exige origen repo")


def ejes_de(unidad):
    return EJES_HOG if unidad == "HOGAR" else EJES_PER


def rid(conducta, ola, eje, cat, q):
    return f"{P}-{conducta}-{ola}-{eje}-{cat}-{q}"


def _serie_map(v, mapa):
    out = np.full(len(v), None, dtype=object)
    for c, codigos in mapa.items():
        out[np.isin(v, codigos)] = c
    return out


def _rango(v, tramos):
    out = np.full(len(v), None, dtype=object)
    for c, lo, hi in tramos:
        out[(v >= lo) & (v <= hi)] = c
    return out


def _bin(v, si, no):
    out = np.full(len(v), np.nan)
    out[np.isin(v, si)] = 1.0
    out[np.isin(v, no)] = 0.0
    return out


def _llave(df, cols):
    return df[list(cols)].astype(str).apply(lambda s: s.str.strip()).agg("|".join, axis=1)


def _cls(serie, R):
    """CLS_HOG como entero; tolera la forma 'H1' del FD 2009."""
    s = serie.astype(str).str.strip().str.upper().str.lstrip("H")
    return R.num(s).to_numpy()


def columnas_hog(ola):
    h = HOG[ola]
    cols = list(h["llave"]) + [h[k] for k in ("fac", "est", "upm", "tloc", "cls", "sexo_j", "edad_j",
                                               "niv_j", "tam")]
    if h["mig"]:
        cols.append(h["mig"])
    return cols


def columnas_per(ola):
    p = PER[ola]
    return list(p["llave"]) + [p[k] for k in ("sexo", "edad", "paren", "niv", "conyu")]


def prepara_hogar(ola, hog, R):
    h = HOG[ola]
    n = R.num
    diag = {"FILAS-HOGAR": int(len(hog))}
    w = n(hog[h["fac"]])
    est = hog[h["est"]].astype(str).str.strip()
    upm = hog[h["upm"]].astype(str).str.strip()
    ok = (w.gt(0) & est.ne("") & upm.ne("")).to_numpy()
    diag["FILAS-HOGAR-DISENO-VALIDO"] = int(ok.sum())
    f = hog[ok].reset_index(drop=True)
    f["_key"] = _llave(f, h["llave"]).to_numpy()
    f["_w"] = np.asarray(w[ok], dtype=float)
    f["_est"] = est[ok].to_numpy()
    f["_upm"] = upm[ok].to_numpy()
    f["_cls"] = _cls(f[h["cls"]], R)
    f["_tam"] = n(f[h["tam"]]).to_numpy()
    f["_tloc"] = _serie_map(n(f[h["tloc"]]).to_numpy(), TLOC[ola])
    return f, diag


def conductas_hogar(ola, f, R):
    h = HOG[ola]
    n = R.num
    cls = f["_cls"].to_numpy()
    validas = (1, 2, 3, 4, 5, 6)
    y = {
        "HOGAR-UNIPERSONAL": _bin(cls, (5,), tuple(c for c in validas if c != 5)),
        "HOGAR-NUCLEAR": _bin(cls, (1,), tuple(c for c in validas if c != 1)),
        "HOGAR-AMPLIADO": _bin(cls, (2,), tuple(c for c in validas if c != 2)),
        "HOGAR-JEFATURA-FEMENINA": _bin(n(f[h["sexo_j"]]).to_numpy(), (2,), (1,)),
    }
    if h["mig"]:
        y["HOGAR-CON-MIGRANTE-INTERNACIONAL-5A"] = _bin(n(f[h["mig"]]).to_numpy(), (1,), (2,))
    else:  # 2009: MIGRA_HO es «migrantes a EUA», no internacional — fuera por spec §2
        y["HOGAR-CON-MIGRANTE-INTERNACIONAL-5A"] = np.full(len(f), np.nan)
    edad_j = n(f[h["edad_j"]]).to_numpy()
    ejes = {
        "SEXO-JEFE": (_serie_map(n(f[h["sexo_j"]]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}),
                      EJES_HOG["SEXO-JEFE"]),
        "EDAD-JEFE": (_rango(edad_j, EDAD_JEFE), EJES_HOG["EDAD-JEFE"]),
        "ESCOLARIDAD-JEFE": (_serie_map(n(f[h["niv_j"]]).to_numpy(), ESCOL[ola]),
                             EJES_HOG["ESCOLARIDAD-JEFE"]),
        "TLOC": (f["_tloc"].to_numpy(), EJES_HOG["TLOC"]),
    }
    return y, ejes


def prepara_persona(ola, per, fh, R, diag):
    p = PER[ola]
    n = R.num
    diag["FILAS-PERSONA"] = int(len(per))
    kp = _llave(per, p["llave"])
    hidx = fh.drop_duplicates("_key", keep=False).set_index("_key")
    enl = kp.isin(hidx.index).to_numpy()
    diag["PERSONA-SIN-HOGAR"] = int((~enl).sum())
    f = per[enl].reset_index(drop=True)
    k = kp[enl].to_numpy()
    for c in ("_w", "_est", "_upm", "_cls", "_tam", "_tloc"):
        f[c] = hidx.loc[k, c].to_numpy()
    diag["FILAS-PERSONA-DISENO-VALIDO"] = int(len(f))
    return f


def conductas_persona(ola, f, R):
    p = PER[ola]
    n = R.num
    edad = n(f[p["edad"]]).to_numpy()
    edad = np.where((edad >= 0) & (edad <= 130), edad, np.nan)
    cls = f["_cls"].to_numpy().astype(float)
    tam = f["_tam"].to_numpy().astype(float)
    paren = n(f[p["paren"]]).to_numpy()
    cy = n(f[p["conyu"]]).to_numpy()
    cm = CONYU[ola]
    unido = _bin(cy, cm["UL"] + cm["CAS"], cm["NO"])
    ul = _bin(cy, cm["UL"], cm["CAS"])
    am = edad >= 60
    y = {}
    y["PERSONA-60MAS"] = np.where(np.isfinite(edad), (edad >= 60).astype(float), np.nan)
    v = np.where(tam >= 1, (tam == 1).astype(float), np.nan)
    y["AM60-VIVE-SOLO"] = np.where(am, v, np.nan)
    v = _bin(cls, (2,), (1, 3, 4, 5, 6))
    y["AM60-EN-HOGAR-AMPLIADO"] = np.where(am, v, np.nan)
    v = _bin(paren, (HIJO,), tuple(c for c in PAREN_VALIDO[ola] if c != HIJO))
    y["JOVEN-25-34-HIJO-DEL-JEFE"] = np.where((edad >= 25) & (edad <= 34), v, np.nan)
    y["PERSONA-15MAS-UNIDA"] = np.where(edad >= 15, unido, np.nan)
    y["UNIDO-15MAS-EN-UNION-LIBRE"] = np.where(edad >= 15, ul, np.nan)
    ejes = {
        "SEXO": (_serie_map(n(f[p["sexo"]]).to_numpy(), {"HOMBRE": (1,), "MUJER": (2,)}), EJES_PER["SEXO"]),
        "EDAD": (_rango(np.nan_to_num(edad, nan=-1), EDAD_PER), EJES_PER["EDAD"]),
        "ESCOLARIDAD": (_serie_map(n(f[p["niv"]]).to_numpy(), ESCOL[ola]), EJES_PER["ESCOLARIDAD"]),
        "TLOC": (f["_tloc"].to_numpy(), EJES_PER["TLOC"]),
        "TAMANO-HOGAR": (_rango(np.nan_to_num(tam, nan=-1), TAM), EJES_PER["TAMANO-HOGAR"]),
        "CONDICION-PAREJA": (_serie_map(cy, {"UNIDO": cm["UL"] + cm["CAS"], "NO-UNIDO": cm["NO"]}),
                             EJES_PER["CONDICION-PAREJA"]),
    }
    return y, ejes


def mide_ola(ola, hog, per, R, replicas, semilla):
    fh, diag = prepara_hogar(ola, hog, R)
    yh, eh = conductas_hogar(ola, fh, R)
    res = R.marginales(fh, yh, eh, fh["_w"].to_numpy(), "_est", "_upm", replicas, semilla)
    fp = prepara_persona(ola, per, fh, R, diag)
    yp, ep = conductas_persona(ola, fp, R)
    res.update(R.marginales(fp, yp, ep, fp["_w"].to_numpy(dtype=float), "_est", "_upm", replicas, semilla))
    return res, diag


def calcula(por_ola, diags, R):
    out = {}
    for ola in OLAS:
        for k in _DIAG:
            out[f"{P}-G-{ola}-{k}"] = int(diags[ola][k])
    for c, unidad in CONDUCTAS.items():
        grupos = [("TOTAL", ("TODOS",))] + list(ejes_de(unidad).items())
        for eje, cats in grupos:
            serie = {}
            for ola in OLAS:
                serie[ola] = {}
                for cat in cats:
                    r = por_ola[ola].get((c, eje, cat)) or {}
                    pv = _fin(r.get("p"))
                    serie[ola][cat] = pv
                    out[rid(c, ola, eje, cat, "P")] = pv
                    out[rid(c, ola, eje, cat, "EE")] = _fin(r.get("ee"))
                    out[rid(c, ola, eje, cat, "IC-LO")] = _fin(r.get("lo"))
                    out[rid(c, ola, eje, cat, "IC-HI")] = _fin(r.get("hi"))
                    out[rid(c, ola, eje, cat, "N")] = int(r.get("n", 0))
            t2, nd = R.persistencia(serie, list(OLAS), cats)
            if c in MENOS_DE_3_OLAS:
                t2 = None
            out[f"{P}-{c}-{eje}-TAU2"] = _fin(t2)
            out[f"{P}-{c}-{eje}-N-DELTAS"] = int(nd)
            for cat in cats:
                lo, hi = R.ic_calibrado(out[rid(c, OLA_PISO, eje, cat, "P")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-LO")],
                                        out[rid(c, OLA_PISO, eje, cat, "IC-HI")], t2)
                out[rid(c, OLA_PISO, eje, cat, "ICC-LO")] = _fin(lo)
                out[rid(c, OLA_PISO, eje, cat, "ICC-HI")] = _fin(hi)
    return out


def lee_ola(ola, ruta, L):
    h, p = HOG[ola], PER[ola]
    if ola == "2018":
        hog = L.lee_csv_zip(ruta, h["miembro"], columnas_hog(ola))
        per = L.lee_csv_zip(ruta, p["miembro"], columnas_per(ola))
    else:
        hog = L.lee_dbf_zip(ruta, h["miembro"], columnas_hog(ola))
        per = L.lee_dbf_zip(ruta, p["miembro"], columnas_per(ola))
    return hog, per


def medir(inputs, contrato):
    _guardia_inputs(inputs)
    replicas = int(contrato["parametros"]["bootstrap_replicas"])
    semilla = int(contrato["seed"]["valor"])
    R = _modulo_desde_bytes("receta_pisos_salud", inputs["receta_pisos_salud"]["bytes"])
    L = _modulo_desde_bytes("lectores_familia", inputs["lectores_familia"]["bytes"])
    por_ola, diags = {}, {}
    for ola in OLAS:
        hog, per = lee_ola(ola, inputs[PAYLOADS[ola]]["ruta_absoluta"], L)
        por_ola[ola], diags[ola] = mide_ola(ola, hog, per, R, replicas, semilla)
    out = calcula(por_ola, diags, R)
    out[f"{P}-G-BOOTSTRAP-REPLICAS"] = replicas
    out[f"{P}-G-SEED"] = semilla
    out[f"{P}-G-INPUT-RECETA-SHA256"] = str(inputs["receta_pisos_salud"].get("sha256"))
    out[f"{P}-G-INPUT-LECTORES-SHA256"] = str(inputs["lectores_familia"].get("sha256"))
    out[f"{P}-G-OLA-RESERVADA"] = "ENADID 2023 -- RESERVADA (E.6), no es input"
    return out


# ══════════════════════════════ esquema ══════════════════════════════

def _fila(i, tipo, unidad):
    f = {"id": i, "tipo": tipo, "unidad": unidad}
    if tipo in ("flotante", "proporcion"):
        f["permite_no_estimable"] = True
    return f


def esquema_resultados():
    f = []
    for ola in OLAS:
        f += [_fila(f"{P}-G-{ola}-{k}", "entero", "filas") for k in _DIAG]
    for c, unidad in CONDUCTAS.items():
        u = "hogares sin ponderar" if unidad == "HOGAR" else "personas sin ponderar"
        grupos = [("TOTAL", ("TODOS",))] + list(ejes_de(unidad).items())
        for eje, cats in grupos:
            for ola in OLAS:
                for cat in cats:
                    f += [_fila(rid(c, ola, eje, cat, "P"), "proporcion", "proporción ponderada"),
                          _fila(rid(c, ola, eje, cat, "EE"), "flotante", "error estándar bootstrap"),
                          _fila(rid(c, ola, eje, cat, "IC-LO"), "proporcion", "IC95 diseño, inferior"),
                          _fila(rid(c, ola, eje, cat, "IC-HI"), "proporcion", "IC95 diseño, superior"),
                          _fila(rid(c, ola, eje, cat, "N"), "entero", u)]
            f += [_fila(f"{P}-{c}-{eje}-TAU2", "flotante", "varianza logit entre olas"),
                  _fila(f"{P}-{c}-{eje}-N-DELTAS", "entero", "deltas definidos")]
            for cat in cats:
                f += [_fila(rid(c, OLA_PISO, eje, cat, "ICC-LO"), "proporcion", "IC calibrado persistencia, inferior"),
                      _fila(rid(c, OLA_PISO, eje, cat, "ICC-HI"), "proporcion", "IC calibrado persistencia, superior")]
    f += [_fila(f"{P}-G-BOOTSTRAP-REPLICAS", "entero", "réplicas"),
          _fila(f"{P}-G-SEED", "entero", "semilla"),
          _fila(f"{P}-G-INPUT-RECETA-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-INPUT-LECTORES-SHA256", "texto", "sha256"),
          _fila(f"{P}-G-OLA-RESERVADA", "texto", "declaración")]
    return f
