"""Medidor versionado para los sucesores corregidos de pisos por eje.

No modifica ``tools.pisos_ejes`` ni el codigo transitivo de los CALC sellados.
Los datos ya habian sido vistos en la corrida defectuosa de #866; estas reglas
corrigen las definiciones previamente selladas conforme a los catalogos.
"""
from __future__ import annotations

import io
import zipfile

import numpy as np
import pandas as pd


EDADES = ("18-29", "30-44", "45-59", "60+")
ESCOLARIDAD = ("hasta_primaria", "secundaria", "media_superior", "superior")


def _csv(zip_path, suffix, cols):
    with zipfile.ZipFile(zip_path) as z:
        nombres = [n for n in z.namelist() if n.lower().endswith(suffix.lower())]
        if len(nombres) != 1:
            raise RuntimeError(f"miembro no unico para {suffix}: {nombres}")
        raw = z.read(nombres[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str,
                            keep_default_na=False, na_filter=False)
            d.columns = [x.strip() for x in d.columns]
            return d[cols]
        except UnicodeDecodeError:
            continue
    raise RuntimeError("CSV sin codificacion util")


def _codigo(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _edad(s):
    x = pd.to_numeric(s, errors="coerce")
    out = pd.Series(pd.NA, index=s.index, dtype="object")
    out[(x >= 18) & (x <= 29)] = "18-29"
    out[(x >= 30) & (x <= 44)] = "30-44"
    out[(x >= 45) & (x <= 59)] = "45-59"
    out[(x >= 60) & (x <= 96)] = "60+"
    return out


def _escolaridad(s):
    c = _codigo(s)
    mapa = {
        "0": "hasta_primaria", "1": "hasta_primaria", "2": "hasta_primaria",
        "3": "secundaria",
        "4": "media_superior", "5": "media_superior",
        "6": "media_superior", "7": "media_superior",
        "8": "superior", "9": "superior", "10": "superior", "11": "superior",
    }
    return c.map(mapa)


def _slug(texto):
    return texto.upper().replace("+", "-MAS").replace("_", "-")


def _bootstrap(d, categorias, reps=10000, seed=42):
    """Punto e IC percentil remuestreando UPM dentro de estrato."""
    d = d.copy()
    d["_key"] = d["_est"].astype(str) + "\t" + d["_upm"].astype(str)
    keys = sorted(d["_key"].unique())
    pos = {k: i for i, k in enumerate(keys)}
    gpos = {g: i for i, g in enumerate(categorias)}
    w = np.zeros((len(keys), len(categorias)))
    y = np.zeros_like(w)
    n = np.zeros(len(categorias), dtype=int)
    for key, grupo, peso, valor in d[["_key", "_grp", "_w", "_y"]].itertuples(
            index=False, name=None):
        i, j = pos[key], gpos[grupo]
        w[i, j] += peso
        y[i, j] += peso * valor
        n[j] += 1
    den = w.sum(0)
    punto = np.divide(y.sum(0), den, out=np.full(len(categorias), np.nan),
                      where=den > 0)
    por_estrato = {}
    for key in keys:
        por_estrato.setdefault(key.split("\t", 1)[0], []).append(pos[key])
    rng = np.random.Generator(np.random.PCG64(seed))
    valores = []
    for inicio in range(0, reps, 50):
        b = min(50, reps - inicio)
        mult = np.zeros((b, len(keys)), dtype=np.int16)
        for indices in por_estrato.values():
            indices = np.asarray(indices)
            sorteos = rng.integers(0, len(indices), size=(b, len(indices)))
            for fila in range(b):
                mult[fila] += np.bincount(
                    indices[sorteos[fila]], minlength=len(keys)).astype(np.int16)
        den_b = mult @ w
        num_b = mult @ y
        valores.append(np.divide(num_b, den_b,
                                  out=np.full_like(num_b, np.nan),
                                  where=den_b > 0))
    replicas = np.vstack(valores)
    out = {}
    for i, categoria in enumerate(categorias):
        if not np.isfinite(punto[i]):
            raise RuntimeError(f"celda vacia no construible: {categoria}")
        lo, hi = np.nanpercentile(replicas[:, i], [2.5, 97.5])
        out[categoria] = {
            "punto": float(punto[i]), "ic_lo": float(lo), "ic_hi": float(hi),
            "n": int(n[i]), "den_w": float(den[i]),
        }
    return out


def _resultados(d, ejes, prefijo):
    out = {f"RESULT-{prefijo}-N-UNIVERSO": int(len(d))}
    for eje, (grupos, categorias) in ejes.items():
        ok = (grupos.notna() & d["_w"].notna() & (d["_w"] > 0) &
              d["_est"].ne("") & d["_upm"].ne(""))
        x = d.loc[ok].copy()
        x["_grp"] = grupos.loc[ok]
        tabla = _bootstrap(x, categorias)
        for categoria, valores in tabla.items():
            base = f"RESULT-{prefijo}-{_slug(eje)}-{_slug(categoria)}"
            out[base + "-P"] = valores["punto"]
            out[base + "-IC-LO"] = valores["ic_lo"]
            out[base + "-IC-HI"] = valores["ic_hi"]
            out[base + "-N"] = valores["n"]
            out[base + "-DEN-W"] = valores["den_w"]
    return out


def envipe_v2(inputs, contrato):
    z = inputs["envipe2024_csv"]["ruta_absoluta"]
    a = _csv(z, "conjunto_de_datos_tmod_vic_envipe2024.csv", [
        "BP1_20", "BP1_23", "BP2_1", "BPCOD", "FAC_DEL", "EST_DIS",
        "UPM_DIS", "ID_PER", "SEXO", "EDAD", "DOMINIO"])
    b = _csv(z, "conjunto_de_datos_tsdem_envipe2024.csv", ["ID_PER", "NIV"])
    d = a.merge(b, on="ID_PER", how="left", validate="m:1")
    d["_w"] = pd.to_numeric(d.FAC_DEL, errors="coerce")
    d["_est"] = d.EST_DIS.str.strip()
    d["_upm"] = d.UPM_DIS.str.strip()

    bp120 = _codigo(d.BP1_20)
    evasion = d.loc[bp120.isin(["1", "2"])].copy()
    evasion["_y"] = (
        _codigo(evasion.BP1_20).eq("2") &
        _codigo(evasion.BP1_23).isin(["4", "5", "6", "8"])).astype(int)
    out = _resultados(evasion, {
        "sexo": (_codigo(evasion.SEXO), ("1", "2")),
        "edad": (_edad(evasion.EDAD), EDADES),
        "escolaridad": (_escolaridad(evasion.NIV), ESCOLARIDAD),
        "dominio": (evasion.DOMINIO.str.strip(), ("R", "C", "U")),
    }, "PISOS-ENVIPE2024-V2-EVASION")

    denuncia = d.loc[
        _codigo(d.BPCOD).eq("1") & _codigo(d.BP2_1).isin(["1", "2"])
    ].copy()
    denuncia["_y"] = _codigo(denuncia.BP1_20).eq("1").astype(int)
    seguro = _codigo(denuncia.BP2_1).map(
        {"1": "asegurado", "2": "no_asegurado"})
    out.update(_resultados(denuncia, {
        "cobertura_seguro": (seguro, ("no_asegurado", "asegurado")),
    }, "PISOS-ENVIPE2024-V2-DENUNCIA"))
    return out


def encig_v2(inputs, contrato):
    z = inputs["encig23_base_datos_csv"]["ruta_absoluta"]
    a = _csv(z, "encig2023_04_sec_7.csv", [
        "N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS", "ID_PER"])
    b = _csv(z, "encig2023_02_residentes_sec_2.csv", [
        "ID_PER", "SEXO", "EDAD", "NIV"])
    d = a.merge(b, on="ID_PER", how="left", validate="m:1")
    p73 = _codigo(d.P7_3)
    d = d.loc[_codigo(d.N_TRA).eq("1") & p73.isin(["1", "2", "4", "5", "6"])].copy()
    d["_w"] = pd.to_numeric(d.FAC_TRA, errors="coerce")
    d["_est"] = d.EST_DIS.str.strip()
    d["_upm"] = d.UPM_DIS.str.strip()
    d["_y"] = _codigo(d.P7_3).isin(["4", "5"]).astype(int)
    return _resultados(d, {
        "sexo": (_codigo(d.SEXO), ("1", "2")),
        "edad": (_edad(d.EDAD), EDADES),
        "escolaridad": (_escolaridad(d.NIV), ESCOLARIDAD),
    }, "PISOS-ENCIG2023-V2-DIGITAL")


def enif_v2(inputs, contrato):
    z = inputs["enif2021_csv"]["ruta_absoluta"]
    informal = [f"P5_1_{i}" for i in range(1, 7)]
    formal = [f"P5_7_{i}" for i in range(1, 10)]
    cuentas = [f"P5_4_{i}" for i in range(1, 10)]
    cols = informal + formal + cuentas + [
        "SEXO", "EDAD", "TLOC", "P3_1_1", "FAC_ELE", "EST_DIS", "UPM_DIS"]
    d = _csv(z, "conjunto_de_datos_tmodulo_enif_2021.csv", cols)
    d["_w"] = pd.to_numeric(d.FAC_ELE, errors="coerce")
    d["_est"] = d.EST_DIS.str.strip()
    d["_upm"] = d.UPM_DIS.str.strip()
    ahorra_informal = d[informal].apply(
        lambda c: _codigo(c).eq("1")).any(axis=1)
    ahorra_formal = d[formal].apply(
        lambda c: _codigo(c).eq("1")).any(axis=1)
    d["_y"] = (ahorra_informal & ~ahorra_formal).astype(int)
    tiene_cuenta = d[cuentas].apply(
        lambda c: _codigo(c).eq("1")).any(axis=1).map(
            {True: "con_cuenta", False: "sin_cuenta"})
    localidad = _codigo(d.TLOC).map({
        "1": "15000_y_mas", "2": "15000_y_mas",
        "3": "menos_15000", "4": "menos_15000",
    })
    return _resultados(d, {
        "sexo": (_codigo(d.SEXO), ("1", "2")),
        "edad": (_edad(d.EDAD), EDADES),
        "escolaridad": (_escolaridad(d.P3_1_1), ESCOLARIDAD),
        "localidad": (localidad, ("menos_15000", "15000_y_mas")),
        "cuenta_formal": (tiene_cuenta, ("sin_cuenta", "con_cuenta")),
    }, "PISOS-ENIF2021-V2-D9")
