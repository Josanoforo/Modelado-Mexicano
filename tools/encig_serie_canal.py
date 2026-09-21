#!/usr/bin/env python3
"""Serie ENCIG 2015-2023 del pago ordinario de luz por canal digital útil.

ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026), pieza P2. Un medidor, una
ola por CALC (`parametros.ola`, `parametros.payload_id`). El estimando, el
universo, los ejes, el remuestreo y la semilla son los del piso adjudicado
`CALC-PISOS-ENCIG2023-EJES-0002/medidor.py`, copiados verbatim donde importa
(`_estimate`, `_age`, `_school`, `_slug`): sobre ENCIG 2023 este medidor debe
reproducir las diez celdas del piso a 1e-10 -- ese es su oro. Añade la celda
nacional `ALL-ALL` (mismo plan bootstrap: las réplicas no dependen de la lista
de celdas) y la llave de 2015, que no trae `ID_PER`.

El primer resultado que produzca este procedimiento es el que se reporta.
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

EDADES = ("18-29", "30-44", "45-59", "60+")
ESCOLARIDAD = ("hasta_primaria", "secundaria", "media_superior", "superior")
CODIGOS_DENOMINADOR = ("1", "2", "4", "5", "6")
CODIGOS_DIGITAL = ("4", "5")

# Llave sec_7 -> residentes por ola. 2015 no trae ID_PER: la llave es la
# vivienda + hogar y el renglón del elegido (R_ELE en sec_7 = N_REN en
# residentes), como declara el FD 2015 (llaves primarias pdf-págs 35 y 44).
LLAVES = {
    "2015": (["ENT", "UPM", "V_SEL", "N_HOG", "R_ELE"],
             ["ENT", "UPM", "V_SEL", "N_HOG", "N_REN"]),
}
LLAVE_ID_PER = (["ID_PER"], ["ID_PER"])


def _miembro_csv(archive: str, suffix: str, cols: list[str]) -> pd.DataFrame:
    """Miembro único por nombre base (con o sin prefijo `conjunto_de_datos_`),
    excluyendo `diccionario_de_datos/` -- 2015 trae un CSV homónimo ahí."""
    wanted = suffix.lower()
    with zipfile.ZipFile(archive) as zf:
        names = [n for n in zf.namelist()
                 if Path(n).name.lower() in (wanted, "conjunto_de_datos_" + wanted)
                 and "diccionario_de_datos" not in n.lower()
                 and "/catalogos/" not in n.lower()]
        if len(names) != 1:
            raise RuntimeError(f"miembro CSV no único: {suffix}: {names}")
        raw = zf.read(names[0])
    for enc in ("utf-8-sig", "latin-1"):
        try:
            d = pd.read_csv(io.StringIO(raw.decode(enc)), dtype=str,
                            keep_default_na=False, na_filter=False)
        except UnicodeDecodeError:
            continue
        d.columns = [str(x).strip() for x in d.columns]
        missing = sorted(set(cols) - set(d.columns))
        if missing:
            raise RuntimeError(f"variables ausentes en {suffix}: {missing}")
        return d[cols].copy()
    raise RuntimeError(f"codificación no reconocida: {suffix}")


def _code(s):
    return s.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def _age(s):
    x = pd.to_numeric(s, errors="coerce")
    out = pd.Series(pd.NA, index=s.index, dtype="object")
    out[(x >= 18) & (x <= 29)] = "18-29"; out[(x >= 30) & (x <= 44)] = "30-44"
    out[(x >= 45) & (x <= 59)] = "45-59"; out[(x >= 60) & (x <= 96)] = "60+"
    return out


def _school(s):
    return _code(s).map({"0": "hasta_primaria", "1": "hasta_primaria",
        "2": "hasta_primaria", "3": "secundaria", "4": "media_superior",
        "5": "media_superior", "6": "media_superior", "7": "media_superior",
        "8": "superior", "9": "superior"})


def _slug(v):
    return (str(v).upper().replace("Á", "A").replace("É", "E").replace("Í", "I")
            .replace("Ó", "O").replace("Ú", "U").replace("+", "-MAS")
            .replace("_", "-").replace(" ", "-"))


def _cells(prefix, outcome, axes):
    cells = [{"base": f"RESULT-{prefix}-ALL-ALL",
              "mask": outcome.notna(), "y": outcome}]
    cells += [{"base": f"RESULT-{prefix}-{_slug(axis)}-{_slug(cat)}",
               "mask": groups.eq(cat) & outcome.notna(), "y": outcome}
              for axis, (groups, cats) in axes.items() for cat in cats]
    return cells


def _estimate(d, cells, reps=10000, seed=42):
    # Verbatim de CALC-PISOS-ENCIG2023-EJES-0002/medidor.py: un plan bootstrap
    # de UPM dentro de estrato, compartido por todas las celdas.
    design = d["_w"].notna() & (d["_w"] > 0) & d["_est"].ne("") & d["_upm"].ne("")
    w = d.loc[design].copy(); w["_key"] = w["_est"].astype(str) + "\t" + w["_upm"].astype(str)
    keys = sorted(w["_key"].unique()); pos = {k: i for i, k in enumerate(keys)}
    denm = np.zeros((len(keys), len(cells))); num = np.zeros_like(denm)
    counts = np.zeros(len(cells), dtype=np.int64)
    for j, cell in enumerate(cells):
        chosen = w.loc[cell["mask"].reindex(w.index, fill_value=False)]
        y = cell["y"].reindex(chosen.index); counts[j] = len(chosen)
        for key, weight, value in zip(chosen["_key"], chosen["_w"], y):
            i = pos[key]; denm[i, j] += float(weight); num[i, j] += float(weight) * float(value)
    den = denm.sum(0)
    point = np.divide(num.sum(0), den, out=np.full(len(cells), np.nan), where=den > 0)
    strata = {}
    for key in keys: strata.setdefault(key.split("\t", 1)[0], []).append(pos[key])
    rng = np.random.Generator(np.random.PCG64(seed))
    boot = np.full((reps, len(cells)), np.nan)
    for start in range(0, reps, 50):
        size = min(50, reps - start); mult = np.zeros((size, len(keys)), dtype=np.int16)
        for h in sorted(strata):
            ix = np.asarray(strata[h], dtype=int)
            draws = rng.integers(0, len(ix), size=(size, len(ix)))
            for row in range(size):
                mult[row] += np.bincount(ix[draws[row]], minlength=len(keys)).astype(np.int16)
        den_b = mult @ denm
        boot[start:start + size] = np.divide(mult @ num, den_b,
            out=np.full_like(den_b, np.nan), where=den_b > 0)
    out = {}
    for j, cell in enumerate(cells):
        valid = np.isfinite(boot[:, j])
        if np.isfinite(point[j]) and valid.any():
            lo, hi = np.percentile(boot[valid, j], [2.5, 97.5]); vals = (float(point[j]), float(lo), float(hi))
        else: vals = (None, None, None)
        rid = cell["base"]
        out[rid + "-P"], out[rid + "-IC-LO"], out[rid + "-IC-HI"] = vals
        out[rid + "-N"] = int(counts[j]); out[rid + "-DEN-W"] = float(den[j])
        out[rid + "-B-VALIDAS"] = int(valid.sum())
    return out


def ids_resultado(ola: str) -> list[dict]:
    """Los outputs que `medir` emite para una ola, con tipo y unidad -- de
    aquí salen los `resultados:` de cada spec.yaml, no a mano."""
    prefix = f"ENCIG-SERIE-{ola}-DIGITAL"
    bases = [f"RESULT-{prefix}-ALL-ALL"]
    bases += [f"RESULT-{prefix}-SEXO-{c}" for c in ("1", "2")]
    bases += [f"RESULT-{prefix}-EDAD-{_slug(c)}" for c in EDADES]
    bases += [f"RESULT-{prefix}-ESCOLARIDAD-{_slug(c)}" for c in ESCOLARIDAD]
    out = []
    for b in bases:
        out += [
            {"id": b + "-P", "tipo": "proporcion", "unidad": "proporción ponderada [0,1]", "permite_no_estimable": True},
            {"id": b + "-IC-LO", "tipo": "proporcion", "unidad": "límite inferior IC95", "permite_no_estimable": True},
            {"id": b + "-IC-HI", "tipo": "proporcion", "unidad": "límite superior IC95", "permite_no_estimable": True},
            {"id": b + "-N", "tipo": "entero", "unidad": "n sin ponderar"},
            {"id": b + "-DEN-W", "tipo": "flotante", "unidad": "denominador ponderado"},
            {"id": b + "-B-VALIDAS", "tipo": "entero", "unidad": "réplicas bootstrap definidas"},
        ]
    out += [
        {"id": f"RESULT-ENCIG-SERIE-{ola}-FILAS-EVENTOS", "tipo": "entero", "unidad": "filas de sec_7 leídas"},
        {"id": f"RESULT-ENCIG-SERIE-{ola}-JOIN-SIN-DEMOGRAFIA", "tipo": "entero", "unidad": "filas del universo sin match en residentes"},
        {"id": f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-N-UNIVERSO", "tipo": "entero", "unidad": "filas del universo N_TRA=01 con P7_3 en {1,2,4,5,6}"},
        {"id": f"RESULT-ENCIG-SERIE-{ola}-P7-3-EXCLUIDAS", "tipo": "entero", "unidad": "N_TRA=01 excluidas por P7_3 en {3,7,8,9,blanco}"},
        {"id": f"RESULT-ENCIG-SERIE-{ola}-LLAVE-JOIN", "tipo": "texto", "unidad": "llave sec_7 -> residentes usada"},
    ]
    return out


def medir(inputs: dict, contrato: dict) -> dict:
    ola = str(contrato["parametros"]["ola"])
    payload_id = str(contrato["parametros"]["payload_id"])
    z = inputs[payload_id]["ruta_absoluta"]
    llave_ev, llave_pe = LLAVES.get(ola, LLAVE_ID_PER)
    events = _miembro_csv(z, f"encig{ola}_04_sec_7.csv",
        ["N_TRA", "P7_3", "FAC_TRA", "EST_DIS", "UPM_DIS"] + llave_ev)
    people = _miembro_csv(z, f"encig{ola}_02_residentes_sec_2.csv",
        llave_pe + ["SEXO", "EDAD", "NIV"])
    for col in llave_ev: events[col] = events[col].str.strip()
    for col in llave_pe: people[col] = people[col].str.strip()
    if people.duplicated(llave_pe).any():
        raise RuntimeError(f"llave de residentes no única en {ola}: {llave_pe}")
    joined = events.merge(people, left_on=llave_ev, right_on=llave_pe,
                          how="left", validate="m:1", indicator=True)
    ntra = _code(joined["N_TRA"]); p73 = _code(joined["P7_3"])
    universe = ntra.eq("1") & p73.isin(list(CODIGOS_DENOMINADOR)); d = joined.loc[universe].copy()
    d["_w"] = pd.to_numeric(d["FAC_TRA"], errors="coerce")
    d["_est"] = d["EST_DIS"].str.strip(); d["_upm"] = d["UPM_DIS"].str.strip()
    y = _code(d["P7_3"]).isin(list(CODIGOS_DIGITAL)).astype(float)
    cells = _cells(f"ENCIG-SERIE-{ola}-DIGITAL", y, {
        "sexo": (_code(d["SEXO"]), ("1", "2")), "edad": (_age(d["EDAD"]), EDADES),
        "escolaridad": (_school(d["NIV"]), ESCOLARIDAD)})
    out = _estimate(d, cells, int(contrato["parametros"]["bootstrap_replicas"]),
                    int(contrato["seed"]["valor"]))
    out.update({
        f"RESULT-ENCIG-SERIE-{ola}-FILAS-EVENTOS": int(len(events)),
        f"RESULT-ENCIG-SERIE-{ola}-JOIN-SIN-DEMOGRAFIA": int(d["_merge"].ne("both").sum()),
        f"RESULT-ENCIG-SERIE-{ola}-DIGITAL-N-UNIVERSO": int(universe.sum()),
        f"RESULT-ENCIG-SERIE-{ola}-P7-3-EXCLUIDAS":
            int((ntra.eq("1") & ~p73.isin(list(CODIGOS_DENOMINADOR))).sum()),
        f"RESULT-ENCIG-SERIE-{ola}-LLAVE-JOIN": "+".join(llave_ev) + "->" + "+".join(llave_pe),
    })
    return out
