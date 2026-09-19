#!/usr/bin/env python3
"""Control puntual independiente con microdatos para los pisos GEN2.

No importa los medidores: relee cuatro estimandos desde los ZIP crudos y
los contrasta con los sellos. Se ejecuta aparte porque el corpus no forma
parte del repositorio.
"""
from __future__ import annotations

import io
import json
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"


def csv_zip(name: str, suffix: str, columns: list[str]) -> pd.DataFrame:
    with zipfile.ZipFile(RAW / name) as archive:
        members = [item for item in archive.namelist() if item.lower().endswith(suffix)]
        if len(members) != 1:
            raise AssertionError(f"miembro no único para {suffix}: {members}")
        payload = archive.read(members[0])
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            frame = pd.read_csv(
                io.StringIO(payload.decode(encoding)),
                dtype=str,
                keep_default_na=False,
                na_filter=False,
            )
            frame.columns = frame.columns.str.strip()
            return frame[columns].copy()
        except UnicodeDecodeError:
            continue
    raise AssertionError(f"codificación no reconocida para {suffix}")


def code(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().str.replace(r"^0+(?=\d)", "", regex=True)


def weighted_mean(y: pd.Series, weights: pd.Series, mask: pd.Series) -> float:
    values = y.loc[mask].astype(float).to_numpy()
    w = pd.to_numeric(weights.loc[mask], errors="raise").to_numpy()
    return float(np.dot(values, w) / w.sum())


def sealed(calc_id: str) -> dict[str, object]:
    path = ROOT / "data" / "corrida0" / calc_id / "resultados.json"
    return json.loads(path.read_text(encoding="utf-8"))["resultados"]


def controls() -> list[dict[str, object]]:
    # ENVIPE: el estimando por sexo está íntegramente en la tabla de delitos.
    victim = csv_zip(
        "envipe2024_csv.zip",
        "conjunto_de_datos_tmod_vic_envipe2024.csv",
        ["BP1_20", "BP1_23", "FAC_DEL", "SEXO"],
    )
    reported = code(victim["BP1_20"])
    reason = code(victim["BP1_23"])
    evasion = (reported.eq("2") & reason.isin(["4", "5", "6", "8"])).astype(float)
    mask = reported.isin(["1", "2"]) & code(victim["SEXO"]).eq("1")
    checks = [(
        "CALC-PISOS-ENVIPE2024-EJES-0002",
        "RESULT-PISOS-ENVIPE2024-V2-EVASION-SEXO-1-P",
        weighted_mean(evasion, victim["FAC_DEL"], mask),
    )]

    # ENCIG: reconstrucción explícita del cruce persona-trámite.
    events = csv_zip(
        "encig23_base_datos_csv.zip",
        "encig2023_04_sec_7.csv",
        ["N_TRA", "P7_3", "FAC_TRA", "ID_PER"],
    )
    people = csv_zip(
        "encig23_base_datos_csv.zip",
        "encig2023_02_residentes_sec_2.csv",
        ["ID_PER", "SEXO"],
    )
    digital = events.merge(people, on="ID_PER", how="left", validate="m:1")
    response = code(digital["P7_3"])
    mask = (
        code(digital["N_TRA"]).eq("1")
        & response.isin(["1", "2", "4", "5", "6"])
        & code(digital["SEXO"]).eq("1")
    )
    checks.append((
        "CALC-PISOS-ENCIG2023-EJES-0002",
        "RESULT-PISOS-ENCIG2023-V2-DIGITAL-SEXO-1-P",
        weighted_mean(response.isin(["4", "5"]).astype(float), digital["FAC_TRA"], mask),
    ))

    # ENIF: dos desenlaces separados; la negación formal usa posiciones,
    # no alineación de etiquetas entre las columnas P5_4 y P5_7.
    informal_columns = [f"P5_1_{index}" for index in range(1, 7)]
    account_columns = [f"P5_4_{index}" for index in range(1, 10)]
    saving_columns = [f"P5_7_{index}" for index in range(1, 10)]
    enif = csv_zip(
        "enif2021_csv.zip",
        "conjunto_de_datos_tmodulo_enif_2021.csv",
        informal_columns + account_columns + saving_columns + ["FAC_ELE", "SEXO"],
    )
    informal = enif[informal_columns].apply(code)
    account = enif[account_columns].apply(code).to_numpy()
    saving = enif[saving_columns].apply(code).to_numpy()
    has_informal = informal.eq("1").any(axis=1)
    known_informal = has_informal | informal.eq("2").all(axis=1)
    has_formal = (saving == "1").any(axis=1)
    known_no_formal = ((account == "2") | (saving == "2")).all(axis=1) & ~has_formal
    d9_known = known_informal & (has_formal | known_no_formal)
    d9 = (has_informal & known_no_formal).astype(float)
    sex_one = code(enif["SEXO"]).eq("1")
    checks.extend([
        (
            "CALC-PISOS-ENIF2021-EJES-0003",
            "RESULT-PISOS-ENIF2021-V2-D9-SEXO-1-P",
            weighted_mean(d9, enif["FAC_ELE"], sex_one & d9_known),
        ),
        (
            "CALC-PISOS-ENIF2021-EJES-0003",
            "RESULT-PISOS-ENIF2021-V2-INFORMAL-CUALQUIERA-SEXO-1-P",
            weighted_mean(has_informal.astype(float), enif["FAC_ELE"], sex_one & known_informal),
        ),
    ])

    output = []
    for calc_id, result_id, observed in checks:
        expected = float(sealed(calc_id)[result_id])
        delta = abs(observed - expected)
        if delta > 1e-12:
            raise AssertionError(f"{result_id}: {observed} != {expected}; delta={delta}")
        output.append({
            "calc_id": calc_id,
            "result_id": result_id,
            "recalculado": observed,
            "sellado": expected,
            "delta_absoluta": delta,
            "veredicto": "COINCIDE",
        })
    return output


if __name__ == "__main__":
    print(json.dumps({"controles": controls()}, ensure_ascii=False, indent=2))
