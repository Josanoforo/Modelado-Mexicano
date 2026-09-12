#!/usr/bin/env python3
"""Reconstruye las matrices crudas sin importar el medidor sellado."""
from __future__ import annotations

import io
import json
import re
import sys
import zipfile
from pathlib import Path

import pandas as pd
import yaml


HERE = Path(__file__).resolve().parent
PID10 = re.compile(r"^[0-9]{10}$")
PID12 = re.compile(r"^[0-9]{6}(?:AP|BP|CP|CH)[0-9]{4}$")


def read_member(path: str, member: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as archive:
        return pd.read_stata(
            io.BytesIO(archive.read(member)),
            convert_categoricals=False,
            preserve_dtypes=False,
        )


def integer_text(value, width: int) -> str:
    number = float(value)
    if not number.is_integer():
        raise ValueError(f"identificador no entero: {value!r}")
    text = str(int(number))
    if len(text) > width:
        raise ValueError(f"identificador excede ancho {width}: {value!r}")
    return text.zfill(width)


def key_w1(row) -> str:
    return integer_text(row.folio, 8) + integer_text(row.ls, 2)


def key_w2(value) -> str:
    text = str(value).strip()
    if not PID10.fullmatch(text):
        raise ValueError(f"pid ENNViH-2 invalido: {value!r}")
    return text


def key_w3(value) -> str:
    text = str(value).strip().replace(" ", "")
    if not PID12.fullmatch(text):
        raise ValueError(f"pid ENNViH-3 invalido: {value!r}")
    return text


def expand_w2(value) -> str:
    text = key_w2(value)
    origin = "AP" if text[:8].endswith("00") else "BP"
    return text[:6] + origin + text[6:]


def raw_matrix(initial: pd.DataFrame, follow: pd.DataFrame) -> dict[str, int]:
    pair = initial.merge(follow, on="pid", how="inner", validate="one_to_one")
    pair = pair[pair.initial.isin([1, 3]) & pair.follow.isin([1, 3])]
    labels = {1: "SI", 3: "NO"}
    return {
        f"{labels[a]}_A_{labels[b]}": int(((pair.initial == a) & (pair.follow == b)).sum())
        for a in (3, 1)
        for b in (3, 1)
    }


def main() -> int:
    result = json.loads((HERE / "resultados.json").read_text())["resultados"]
    root = HERE.parents[2]
    manifest = yaml.safe_load((root / "data/manifiesto.yaml").read_text())
    wanted = {
        "ennvih1_2002_hogar_dta",
        "ennvih2_2005_hogar_dta",
        "ennvih3_2009_hogar_dta",
    }
    paths = {
        row["id"]: str(root / "data/raw" / row["archivo"])
        for row in manifest
        if isinstance(row, dict) and row.get("id") in wanted
    }
    if set(paths) != wanted:
        raise ValueError(f"faltan insumos en manifiesto: {sorted(wanted - set(paths))}")

    w1 = read_member(paths["ennvih1_2002_hogar_dta"], "ehh02dta_all/ehh02dta_b3b/iiib_cr.dta")
    w2 = read_member(paths["ennvih2_2005_hogar_dta"], "ehh05dta_b3b/iiib_cr.dta")
    w3 = read_member(paths["ennvih3_2009_hogar_dta"], "ehh09dta_all/ehh09dta_b3b/iiib_cr.dta")
    r2 = read_member(paths["ennvih2_2005_hogar_dta"], "ehh05dta_bc/c_ls.dta")
    r3 = read_member(paths["ennvih3_2009_hogar_dta"], "ehh09dta_all/ehh09dta_bc/c_ls.dta")

    i12 = pd.DataFrame({"pid": [key_w1(x) for x in w1.itertuples()], "initial": pd.to_numeric(w1.cr04, errors="coerce")})
    f12 = pd.DataFrame({"pid": w2.pid_link.map(key_w2), "follow": pd.to_numeric(w2.cr04, errors="coerce")})
    i23 = pd.DataFrame({"pid": w2.pid_link.map(expand_w2), "initial": pd.to_numeric(w2.cr04, errors="coerce")})
    f23 = pd.DataFrame({"pid": w3.pid_link.map(key_w3), "follow": pd.to_numeric(w3.cr04, errors="coerce")})
    for label, frame in (("w1", i12), ("w2-follow", f12), ("w2-initial", i23), ("w3", f23)):
        if frame.pid.duplicated().any():
            raise ValueError(f"{label}: pid duplicado")

    observed = {"1A2": raw_matrix(i12, f12), "2A3": raw_matrix(i23, f23)}
    expected = {}
    for pair in ("1A2", "2A3"):
        matrix = json.loads(result[f"RESULT-TANDAS-PANEL-ENNVIH-{pair}-MATRIZ-JSON"])
        expected[pair] = {key: value["n"] for key, value in matrix["celdas"].items()}

    raw2 = r2.pid_link.fillna("").astype(str).str.strip()
    fallback2 = [integer_text(f, 8) + integer_text(ls, 2) for f, ls in zip(r2.folio, r2.ls)]
    roster2 = [key_w2(pid if pid else fallback) for pid, fallback in zip(raw2, fallback2)]
    roster3 = r3.pid_link.map(key_w3)
    identity = {
        "1A2": {
            "filas_roster": int(len(r2)),
            "personas_roster": int(pd.Series(roster2).nunique()),
            "ids_roster_duplicados": int(pd.Series(roster2).value_counts().gt(1).sum()),
        },
        "2A3": {
            "filas_roster": int(len(r3)),
            "personas_roster": int(roster3.nunique()),
            "ids_roster_duplicados": int(roster3.value_counts().gt(1).sum()),
        },
    }
    identity_expected = {
        pair: {
            key: json.loads(result[f"RESULT-TANDAS-PANEL-ENNVIH-{pair}-IDENTIDAD-JSON"])[key]
            for key in values
        }
        for pair, values in identity.items()
    }
    ok = observed == expected and identity == identity_expected
    report = {
        "calc_id": "CALC-TANDAS-ENNVIH-PANEL-0001",
        "control": "RECONSTRUCCION-INDEPENDIENTE-SIN-IMPORTAR-MEDIDOR",
        "matrices_crudas_observadas": observed,
        "matrices_crudas_selladas": expected,
        "cardinalidad_roster_observada": identity,
        "cardinalidad_roster_sellada": identity_expected,
        "veredicto": "REPRODUCE" if ok else "NO-REPRODUCE",
    }
    (HERE / "control-independiente.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    print(report["veredicto"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
