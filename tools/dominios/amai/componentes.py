"""Componentes AMAI por hogar, un adaptador por instrumento.

Contrato: `forense/prereg-caja/AMAI-NSE-spec-v1_0.md` §3-§4. Cada adaptador
devuelve un DataFrame con UNA fila por hogar, las seis columnas de
`regla.COMPONENTES` (NaN = componente ausente o no válido; el hogar sale del
NSE, como en el Anexo de AMAI), la llave de hogar, el factor de hogar y el
diseño (EST_DIS, UPM_DIS). Ningún adaptador calcula puntos ni niveles: eso es
de `regla.py`. Ningún adaptador lee conducta alguna.
"""
from __future__ import annotations

import io
import sys
import tempfile
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT / "tests") not in sys.path:
    sys.path.insert(0, str(ROOT / "tests"))
from dbfmini import field_names, read_dbf  # noqa: E402


# --------------------------------------------------------------- lectura

def csv_zip(ruta, sufijo: str, columnas: list[str]) -> pd.DataFrame:
    """Un miembro CSV del zip, por sufijo exacto; todo como texto."""
    with zipfile.ZipFile(ruta) as z:
        nombres = [n for n in z.namelist() if n.lower().endswith(sufijo.lower())]
        if len(nombres) != 1:
            raise RuntimeError(f"{sufijo}: {len(nombres)} miembros")
        payload = z.read(nombres[0])
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            texto = payload.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    texto = texto.replace("\r\n", "\n").replace("\r", "\n")
    df = pd.read_csv(io.StringIO(texto), dtype=str, keep_default_na=False,
                     na_filter=False, low_memory=False)
    df.columns = [c.strip().strip('"').lstrip("﻿").lstrip("ï»¿") for c in df.columns]
    faltan = set(columnas) - set(df.columns)
    if faltan:
        raise RuntimeError(f"{nombres[0]}: faltan {sorted(faltan)}")
    return df[list(columnas)].apply(lambda s: s.astype(str).str.strip().str.strip('"'))


def dbf_zip(ruta, miembro: str, columnas: tuple[str, ...]) -> pd.DataFrame:
    with zipfile.ZipFile(ruta) as z:
        if miembro not in z.namelist():
            raise RuntimeError(f"miembro ausente: {miembro}")
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(z.extract(miembro, tmp))
            hay = {n for n, _, _ in field_names(p)}
            faltan = set(columnas) - hay
            if faltan:
                raise RuntimeError(f"{miembro}: faltan {sorted(faltan)}")
            filas = list(read_dbf(p, wanted_fields=columnas))
    df = pd.DataFrame(filas, columns=list(columnas))
    return df.apply(lambda s: s.astype(str).str.strip())


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce")


def _unica(df: pd.DataFrame, llave: list[str], que: str) -> None:
    if df.duplicated(llave).any():
        raise RuntimeError(f"{que}: llave {llave} no única")


# ------------------------------------------------- escolaridad de la jefatura

def educa_desde_niv(niv: pd.Series, gra: pd.Series, codigos: str) -> pd.Series:
    """Nivel/grado INEGI -> `educa_jefe` 1..11 con la regla de construcción de
    ENIGH 2022 (Descripción de la base, variable #12 de concentradohogar).
    Estudios técnicos y normal básica van al nivel de su antecedente escolar
    terminado (regla ENIGH `antec_esc`); especialidad cuenta como posgrado.
    `codigos`: 'enif2024-endutih' | 'enif2021'. No sabe / blanco -> NaN."""
    crudo = niv.astype(str).str.strip().str.upper()
    falta = crudo.isin(["", "B", "99", "NAN", "NONE"])
    # zfill sólo sobre lo presente: "".zfill(2) sería "00" (Ninguno).
    n = crudo.where(falta, crudo.str.zfill(2)).where(~falta, "FALTA")
    g = _num(gra)
    out = pd.Series(np.nan, index=niv.index, dtype=float)
    if codigos == "enif2021":
        tecnica_sec, normal, tecnica_prep = {"04"}, {"05"}, {"07"}
        posgrado = {"09"}
        validos = {f"{i:02d}" for i in range(0, 10)}
    elif codigos == "enif2024-endutih":
        tecnica_sec, normal, tecnica_prep = {"05"}, {"04"}, {"07"}
        posgrado = {"09", "10", "11"}
        validos = {f"{i:02d}" for i in range(0, 12)}
    else:
        raise ValueError(codigos)
    raros = set(n.unique()) - validos - {"FALTA"}
    if raros:
        raise RuntimeError(f"NIV fuera del codebook ({codigos}): {sorted(raros)}")
    out[n.eq("00")] = 1
    out[n.eq("01")] = 2
    prim = n.eq("02")
    out[prim & g.lt(6)] = 3
    out[prim & g.ge(6)] = 4
    sec = n.eq("03")
    out[sec & g.lt(3)] = 5
    out[sec & g.ge(3)] = 6
    out[n.isin(tecnica_sec | normal)] = 6
    prep = n.eq("06")
    out[prep & g.lt(3)] = 7
    out[prep & g.ge(3)] = 8
    out[n.isin(tecnica_prep)] = 8
    lic = n.eq("08")
    out[lic & g.lt(4)] = 9
    out[lic & g.ge(4)] = 10
    out[n.isin(posgrado)] = 11
    # grado no numérico donde el nivel lo exige -> NaN (no se imputa)
    exige = prim | sec | prep | lic
    out[exige & g.isna()] = np.nan
    return out


def _jefatura(personas: pd.DataFrame, llave: list[str], paren: str) -> pd.DataFrame:
    jefes = personas[personas[paren].astype(str).str.strip().eq("1")]
    _unica(jefes, llave, "jefatura")
    return jefes


# --------------------------------------------------------------- ENIGH 2022

ENIGH_MIEMBROS = {
    "hogares": "conjunto_de_datos_hogares_enigh2022_ns.csv",
    "concentrado": "conjunto_de_datos_concentradohogar_enigh2022_ns.csv",
    "viviendas": "conjunto_de_datos_viviendas_enigh2022_ns.csv",
}


def enigh2022(ruta) -> pd.DataFrame:
    """Réplica del Anexo AMAI (pp. 16-17): HOGARES ⋈ CONCENTRADO por
    (folioviv, foliohog) ⋈ VIVIENDAS por folioviv. Diseño: upm, est_dis y
    factor de concentradohogar. Trae `remesas` para la conducta del §6."""
    h = csv_zip(ruta, ENIGH_MIEMBROS["hogares"],
                ["folioviv", "foliohog", "conex_inte", "num_auto", "num_van", "num_pickup"])
    c = csv_zip(ruta, ENIGH_MIEMBROS["concentrado"],
                ["folioviv", "foliohog", "educa_jefe", "ocupados", "upm", "est_dis",
                 "factor", "remesas"])
    v = csv_zip(ruta, ENIGH_MIEMBROS["viviendas"], ["folioviv", "cuart_dorm", "bano_comp"])
    for df, ll, q in ((h, ["folioviv", "foliohog"], "hogares"),
                      (c, ["folioviv", "foliohog"], "concentrado"),
                      (v, ["folioviv"], "viviendas")):
        _unica(df, ll, q)
    d = c.merge(h, on=["folioviv", "foliohog"], how="left", validate="1:1")
    d = d.merge(v, on="folioviv", how="left", validate="m:1")
    autos = _num(d["num_auto"]) + _num(d["num_van"]) + _num(d["num_pickup"])
    conex = _num(d["conex_inte"])
    out = pd.DataFrame({
        "llave": d["folioviv"] + "-" + d["foliohog"],
        "educa_jefe": _num(d["educa_jefe"]),
        "banos": _num(d["bano_comp"]),
        "autos": autos,
        "internet": np.where(conex.isna(), np.nan, (conex == 1).astype(float)),
        "ocupados": _num(d["ocupados"]),
        "dormitorios": _num(d["cuart_dorm"]),
        "factor": _num(d["factor"]),
        "EST_DIS": d["est_dis"], "UPM_DIS": d["upm"],
        "remesas": _num(d["remesas"]),
    })
    return out


# --------------------------------------------------------------- ENIF

ENIF = {
    "2024": {"llave_hog": ["LLAVEHOG"], "llave_viv": ["LLAVEVIV"], "paren": "PAREN",
             "codigos": "enif2024-endutih", "fac_per": "FAC_PER"},
    "2021": {"llave_hog": ["FOLIO", "VIV_SEL", "HOGAR"], "llave_viv": ["FOLIO", "VIV_SEL"],
             "paren": "P2_3", "codigos": "enif2021", "fac_per": "FAC_ELE"},
}


def enif(ruta, ola: str) -> pd.DataFrame:
    """ENIF: vivienda (dormitorios P0_1, baños P0_3, autos P0_4_1/P0_4_1A,
    internet fijo P0_4_2/P0_4_2A) compartida por sus hogares, como el
    merge por folioviv del Anexo; jefatura de TSDEM; ocupados = P2_8
    («personas que trabajan» / «con trabajo remunerado»: APROXIMACIÓN)."""
    k = ENIF[ola]
    lh, lv = k["llave_hog"], k["llave_viv"]
    viv = csv_zip(ruta, "TVIVIENDA.csv",
                  lv + ["P0_1", "P0_3", "P0_4_1", "P0_4_1A", "P0_4_2", "P0_4_2A"])
    hog = csv_zip(ruta, "THOGAR.csv", sorted(set(lh + lv)) + ["P2_8", "EST_DIS",
                                                              "UPM_DIS", "FAC_HOG"])
    sdem = csv_zip(ruta, "TSDEM.csv", sorted(set(lh)) + [k["paren"], "NIV", "GRA"])
    _unica(viv, lv, "TVIVIENDA")
    _unica(hog, lh, "THOGAR")
    jefe = _jefatura(sdem, lh, k["paren"])
    d = hog.merge(viv, on=lv, how="left", validate="m:1")
    d = d.merge(jefe[lh + ["NIV", "GRA"]], on=lh, how="left", validate="1:1")
    tiene_auto = d["P0_4_1"].str.strip()
    autos = pd.Series(np.nan, index=d.index)
    autos[tiene_auto.eq("2")] = 0
    autos[tiene_auto.eq("1")] = _num(d.loc[tiene_auto.eq("1"), "P0_4_1A"])
    tiene_int = d["P0_4_2"].str.strip()
    fija = d["P0_4_2A"].str.strip()
    internet = pd.Series(np.nan, index=d.index)
    internet[tiene_int.eq("2")] = 0
    internet[tiene_int.eq("1") & fija.eq("2")] = 0
    internet[tiene_int.eq("1") & fija.eq("1")] = 1
    ocup = _num(d["P2_8"])
    ocup[ocup.gt(90)] = np.nan
    out = pd.DataFrame({
        "llave": d[lh].agg("|".join, axis=1),
        "educa_jefe": educa_desde_niv(d["NIV"].fillna(""), d["GRA"].fillna(""), k["codigos"]),
        "banos": _num(d["P0_3"]),
        "autos": autos,
        "internet": internet,
        "ocupados": ocup,
        "dormitorios": _num(d["P0_1"]),
        "factor": _num(d["FAC_HOG"]),
        "EST_DIS": d["EST_DIS"], "UPM_DIS": d["UPM_DIS"],
    })
    return out


# --------------------------------------------------------------- ENDUTIH

ENDUTIH = {
    "2023": ("tic_2023_viviendas.DBF", "tic_2023_hogares.DBF", "tic_2023_residentes.DBF"),
    "2024": ("tic_2024_viviendas.DBF", "tic_2024_hogares.DBF", "tic_2024_residentes.DBF"),
    "2025": ("ti25viv.dbf", "ti25hog.dbf", "ti25res.dbf"),
}
LLAVE_HOG_ENDUTIH = ["UPM", "VIV_SEL", "HOGAR"]


def endutih(ruta, ola: str) -> pd.DataFrame:
    """ENDUTIH: educación de la jefatura (PAREN=1, NIVEL/GRADO), ocupados 14+
    (P3_10 ∈ {1,2} o P3_11 ∈ {1,2,3}, EDAD 14..97), internet fijo (P4_4=1 y
    P4_5 ∈ {1,3}), auto sí/no (P1_5_3, vivienda). Baños y dormitorios no
    existen en el cuestionario: quedan NaN y los completa `imputacion.py`.
    `autos` lleva 0/1 = sin/con al menos uno (el conteo no existe)."""
    fviv, fhog, fres = ENDUTIH[ola]
    viv = dbf_zip(ruta, fviv, ("UPM", "VIV_SEL", "P1_5_3"))
    hog = dbf_zip(ruta, fhog, ("UPM", "VIV_SEL", "HOGAR", "P4_4", "P4_5",
                               "FAC_HOG", "EST_DIS", "UPM_DIS"))
    res = dbf_zip(ruta, fres, ("UPM", "VIV_SEL", "HOGAR", "NUM_REN", "PAREN", "EDAD",
                               "NIVEL", "GRADO", "P3_10", "P3_11"))
    _unica(viv, ["UPM", "VIV_SEL"], "viviendas")
    _unica(hog, LLAVE_HOG_ENDUTIH, "hogares")
    _unica(res, LLAVE_HOG_ENDUTIH + ["NUM_REN"], "residentes")
    edad = _num(res["EDAD"])
    ocupa = res["P3_10"].isin(["1", "2"]) | res["P3_11"].isin(["1", "2", "3"])
    res = res.assign(_ocup=(ocupa & edad.between(14, 97)).astype(int))
    n_ocup = res.groupby(LLAVE_HOG_ENDUTIH)["_ocup"].sum().rename("ocupados").reset_index()
    jefe = _jefatura(res, LLAVE_HOG_ENDUTIH, "PAREN")
    d = hog.merge(viv, on=["UPM", "VIV_SEL"], how="left", validate="m:1")
    d = d.merge(n_ocup, on=LLAVE_HOG_ENDUTIH, how="left", validate="1:1")
    d = d.merge(jefe[LLAVE_HOG_ENDUTIH + ["NIVEL", "GRADO"]], on=LLAVE_HOG_ENDUTIH,
                how="left", validate="1:1")
    p44, p45 = d["P4_4"].str.strip(), d["P4_5"].str.strip()
    internet = pd.Series(np.nan, index=d.index)
    internet[p44.eq("2")] = 0
    internet[p44.eq("1") & p45.isin(["2"])] = 0
    internet[p44.eq("1") & p45.isin(["1", "3"])] = 1
    auto = d["P1_5_3"].str.strip()
    autos = pd.Series(np.nan, index=d.index)
    autos[auto.eq("2")] = 0
    autos[auto.eq("1")] = 1
    out = pd.DataFrame({
        "llave": d[LLAVE_HOG_ENDUTIH].agg("|".join, axis=1),
        "educa_jefe": educa_desde_niv(d["NIVEL"].fillna(""), d["GRADO"].fillna(""),
                                      "enif2024-endutih"),
        "banos": np.nan, "autos": autos, "internet": internet,
        "ocupados": d["ocupados"].astype(float), "dormitorios": np.nan,
        "factor": _num(d["FAC_HOG"]),
        "EST_DIS": d["EST_DIS"], "UPM_DIS": d["UPM_DIS"],
    })
    return out
