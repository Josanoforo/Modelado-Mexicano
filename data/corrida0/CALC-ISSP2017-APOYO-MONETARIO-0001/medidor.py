#!/usr/bin/env python3
"""Descriptivo preespecificado de ISSP México 2017, ZA6980 v2.0.0, v26."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import tempfile
import zipfile
from pathlib import Path

import pandas as pd
import pyreadstat


CALC_ID = "CALC-ISSP2017-APOYO-MONETARIO-0001"
INPUT_Q = "za6980_q_mx"
INPUT_BACKGROUND = "za6980_backgroundvar_mx"
INPUT_DTA = "za6980_v2_0_0_dta"
INPUT_SAV = "za6980_v2_0_0_sav"
INPUT_CODEBOOK = "za6980_codebook_integrado_evidencia"
EXPECTED_SHA256 = {
    INPUT_Q: "61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed",
    INPUT_BACKGROUND: "6004c300ca1331bfd15f163c4deaa726c71b66b46ae9e05361f40ae8cc26ca5f",
    INPUT_DTA: "aa3bfcbcc1dc20a2735e8e9d2d3d47a72d909dade66e8c4623b910965dc227de",
    INPUT_SAV: "20a1420f4aa8f8dcb30f7de61879796d20b7c3042805e7925e56c30b4ae97ca5",
    INPUT_CODEBOOK: "de18929fc4aa638e458b191d103d9a19f766121291d758f77a65268106cfe356",
}
DTA_MEMBER = "ZA6980_v2-0-0.dta"
DTA_MEMBERS = [DTA_MEMBER, "ZA6980_v2-0-0_missing.txt"]
SAV_MEMBER = "ZA6980_v2-0-0.sav"
AUTHORIZED_COLUMNS = [
    "studyno", "doi", "version", "country", "c_alphan",
    "CASEID", "SEX", "AGE", "WEIGHT", "v26",
]
CATEGORIES = (
    (1, "Family members or close friends", "Familiares o amigos cercanos"),
    (2, "Other persons", "Otras personas"),
    (3, "Private companies", "Compañías privadas"),
    (4, "Public services", "Servicios públicos"),
    (5, "Non-profit or religious organisations", "Organizaciones sin fines de lucro o religiosas"),
    (6, "Other organisations", "Otras organizaciones"),
    (7, "No person or organisation", "Ninguna persona u organización"),
)
DOMAINS = (
    ("TOTAL", "México, personas adultas", None),
    ("HOMBRES", "Hombres", 1),
    ("MUJERES", "Mujeres", 2),
)
PRECISION = "EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO"
INSTRUMENT = "ISSP 2017 Social Networks and Social Resources, México, Q8a"
VERSION = "ZA6980 v2.0.0; DOI 10.4232/1.13322"
UNIVERSE = "Personas de 18 años o más, muestra nacional de México"

DISTRIBUTION_COLUMNS = [
    "tipo", "calc_id", "instrumento", "version", "pais", "universo",
    "dominio_id", "dominio", "codigo", "texto_integrado", "texto_mexico",
    "n_denominador_valido", "masa_denominador_valido", "n_categoria",
    "masa_categoria", "proporcion", "porcentaje", "precision", "estado",
]
COVERAGE_COLUMNS = [
    "tipo", "calc_id", "instrumento", "version", "pais", "universo",
    "dominio_id", "dominio", "clasificacion", "n_elegible",
    "masa_elegible_peso_utilizable", "n", "masa", "cobertura_ponderada_valida",
    "precision", "estado",
]
CONTRAST_COLUMNS = [
    "tipo", "calc_id", "instrumento", "version", "pais", "universo",
    "contraste", "codigo", "texto_integrado", "texto_mexico",
    "n_denominador_mujeres", "masa_denominador_mujeres", "p_mujeres",
    "n_denominador_hombres", "masa_denominador_hombres", "p_hombres",
    "diferencia_menos_mas", "diferencia_puntos_porcentuales", "precision", "estado",
]


def _read_input(entry: dict) -> bytes:
    raw = entry.get("bytes")
    return raw if raw is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _fmt(value) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ""
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return f"{value:.12f}"
    return str(value)


def _serialize(rows: list[dict], columns: list[str]) -> bytes:
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: _fmt(row.get(key)) for key in columns} for row in rows)
    return out.getvalue().encode("utf-8")


def _zip_member(raw: bytes, expected: list[str], member: str) -> bytes:
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP-CORRUPTO")
        names = [info.filename for info in archive.infolist() if not info.is_dir()]
        if names != expected:
            raise ValueError(f"MIEMBROS-ZIP-INESPERADOS:{names}")
        return archive.read(member)


def _metadata(raw: bytes, suffix: str):
    with tempfile.NamedTemporaryFile(suffix=suffix) as handle:
        handle.write(raw)
        handle.flush()
        if suffix == ".dta":
            _, meta = pyreadstat.read_dta(handle.name, metadataonly=True)
        else:
            _, meta = pyreadstat.read_sav(handle.name, metadataonly=True)
    return meta


def verify_metadata(raw_dta: bytes, raw_sav: bytes) -> dict:
    dta = _metadata(raw_dta, ".dta")
    sav = _metadata(raw_sav, ".sav")
    if (dta.number_rows, dta.number_columns) != (44492, 356):
        raise ValueError("DIMENSION-DTA-INESPERADA")
    if (sav.number_rows, sav.number_columns) != (44492, 356):
        raise ValueError("DIMENSION-SAV-INESPERADA")
    for var in AUTHORIZED_COLUMNS:
        if dta.column_names_to_labels.get(var) != sav.column_names_to_labels.get(var):
            raise ValueError(f"ETIQUETA-DTA-SAV-DISCREPA:{var}")
    expected_v26 = {float(code): english for code, english, _ in CATEGORIES}
    expected_v26.update({8.0: "Can't choose", 9.0: "No answer"})
    expected_sex = {1.0: "Male", 2.0: "Female", 9.0: "No answer"}
    for meta, kind in ((dta, "DTA"), (sav, "SAV")):
        v26 = meta.value_labels[meta.variable_to_label["v26"]]
        sex = meta.value_labels[meta.variable_to_label["SEX"]]
        if v26 != expected_v26:
            raise ValueError(f"ETIQUETAS-V26-{kind}-INESPERADAS:{v26}")
        if sex != expected_sex:
            raise ValueError(f"ETIQUETAS-SEX-{kind}-INESPERADAS:{sex}")
    return {"filas": 44492, "columnas": 356, "etiquetas_v26_coinciden": True}


def _numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def validate_and_select(frame: pd.DataFrame) -> pd.DataFrame:
    if list(frame.columns) != AUTHORIZED_COLUMNS:
        raise ValueError(f"COLUMNAS-NO-AUTORIZADAS:{list(frame.columns)}")
    mx = frame.loc[frame["c_alphan"].astype(str).eq("MX")].copy()
    if len(mx) != 1002:
        raise ValueError(f"N-MEXICO-INESPERADO:{len(mx)}")
    if not _numeric(mx["country"]).eq(484).all():
        raise ValueError("PAIS-MEXICO-DISCREPA")
    if not _numeric(mx["studyno"]).eq(6980).all():
        raise ValueError("ESTUDIO-DISCREPA")
    if set(mx["version"].astype(str)) != {"2.0.0"}:
        raise ValueError("VERSION-DISCREPA")
    if set(mx["doi"].astype(str)) != {"10.4232/1.13322"}:
        raise ValueError("DOI-DISCREPA")
    if mx["CASEID"].isna().any() or mx["CASEID"].duplicated().any():
        raise ValueError("CASEID-NO-UNICO-O-FALTANTE")
    sex = _numeric(mx["SEX"])
    if not sex.dropna().isin([1, 2, 9]).all():
        raise ValueError("SEX-FUERA-DE-CATALOGO")
    age = _numeric(mx["AGE"])
    observed_age = age[age.notna() & age.ne(999)]
    if (observed_age < 18).any():
        raise ValueError("EDAD-MENOR-DE-18")
    response = _numeric(mx["v26"])
    if not response.dropna().isin(range(1, 10)).all():
        raise ValueError("V26-FUERA-DE-CATALOGO")
    mx["SEX"] = sex
    mx["AGE"] = age
    mx["WEIGHT"] = _numeric(mx["WEIGHT"])
    mx["v26"] = response
    return mx


def _domain(frame: pd.DataFrame, sex_code: int | None) -> pd.DataFrame:
    return frame if sex_code is None else frame.loc[frame["SEX"].eq(sex_code)]


def _weight_valid(frame: pd.DataFrame) -> pd.Series:
    return frame["WEIGHT"].notna() & frame["WEIGHT"].map(math.isfinite) & frame["WEIGHT"].gt(0)


def calculate(frame: pd.DataFrame) -> tuple[list[dict], list[dict], list[dict], dict]:
    distributions: list[dict] = []
    coverage: list[dict] = []
    points: dict[tuple[str, int], tuple] = {}
    domain_summary = {}
    for domain_id, domain_label, sex_code in DOMAINS:
        part = _domain(frame, sex_code)
        weight_ok = _weight_valid(part)
        valid = weight_ok & part["v26"].isin(range(1, 8))
        cant = weight_ok & part["v26"].eq(8)
        noanswer = weight_ok & (part["v26"].eq(9) | part["v26"].isna())
        invalid_weight = ~weight_ok
        if not (valid | cant | noanswer | invalid_weight).all():
            raise ValueError(f"PARTICION-INCOMPLETA:{domain_id}")
        denom_n = int(valid.sum())
        denom_mass = float(part.loc[valid, "WEIGHT"].sum())
        eligible_mass = float(part.loc[weight_ok, "WEIGHT"].sum())
        cover = None if eligible_mass <= 0 else denom_mass / eligible_mass
        base = {
            "tipo": "RESULT", "calc_id": CALC_ID, "instrumento": INSTRUMENT,
            "version": VERSION, "pais": "México", "universo": UNIVERSE,
            "dominio_id": domain_id, "dominio": domain_label, "precision": PRECISION,
        }
        for code, english, spanish in CATEGORIES:
            selected = valid & part["v26"].eq(code)
            n = int(selected.sum())
            mass = float(part.loc[selected, "WEIGHT"].sum())
            point = None if denom_mass <= 0 else mass / denom_mass
            points[(domain_id, code)] = (point, denom_n, denom_mass)
            distributions.append({
                **base, "codigo": code, "texto_integrado": english, "texto_mexico": spanish,
                "n_denominador_valido": denom_n, "masa_denominador_valido": denom_mass,
                "n_categoria": n, "masa_categoria": mass, "proporcion": point,
                "porcentaje": None if point is None else point * 100,
                "estado": "OK" if point is not None else "DENOMINADOR-NULO",
            })
        classes = (
            ("VALIDA", valid), ("NO_PUEDE_ELEGIR", cant),
            ("NO_RESPUESTA", noanswer), ("PESO_INVALIDO", invalid_weight),
        )
        for label, mask in classes:
            coverage.append({
                **base, "clasificacion": label, "n_elegible": len(part),
                "masa_elegible_peso_utilizable": eligible_mass, "n": int(mask.sum()),
                "masa": None if label == "PESO_INVALIDO" else float(part.loc[mask, "WEIGHT"].sum()),
                "cobertura_ponderada_valida": cover,
                "estado": "OK" if eligible_mass > 0 else "MASA-ELEGIBLE-NULA",
            })
        domain_summary[domain_id] = {
            "n": len(part), "mass": eligible_mass, "valid_n": denom_n,
            "valid_mass": denom_mass, "class_n": {label: int(mask.sum()) for label, mask in classes},
        }

    women, wn, wm = points[("MUJERES", 1)]
    men, mn, mm = points[("HOMBRES", 1)]
    delta = None if women is None or men is None else women - men
    contrasts = [{
        "tipo": "RESULT", "calc_id": CALC_ID, "instrumento": INSTRUMENT,
        "version": VERSION, "pais": "México", "universo": UNIVERSE,
        "contraste": "MUJERES-MENOS-HOMBRES", "codigo": 1,
        "texto_integrado": CATEGORIES[0][1], "texto_mexico": CATEGORIES[0][2],
        "n_denominador_mujeres": wn, "masa_denominador_mujeres": wm, "p_mujeres": women,
        "n_denominador_hombres": mn, "masa_denominador_hombres": mm, "p_hombres": men,
        "diferencia_menos_mas": delta,
        "diferencia_puntos_porcentuales": None if delta is None else delta * 100,
        "precision": PRECISION, "estado": "OK" if delta is not None else "DENOMINADOR-NULO",
    }]

    classified = frame["SEX"].isin([1, 2])
    unclassified = frame.loc[~classified]
    if domain_summary["TOTAL"]["n"] != domain_summary["HOMBRES"]["n"] + domain_summary["MUJERES"]["n"] + len(unclassified):
        raise ValueError("RECONSTRUCCION-N-TOTAL-FALLA")
    unclassified_mass = float(unclassified.loc[_weight_valid(unclassified), "WEIGHT"].sum())
    rebuilt_mass = domain_summary["HOMBRES"]["mass"] + domain_summary["MUJERES"]["mass"] + unclassified_mass
    if not math.isclose(rebuilt_mass, domain_summary["TOTAL"]["mass"], abs_tol=1e-10):
        raise ValueError("RECONSTRUCCION-MASA-TOTAL-FALLA")
    controls = {
        "particiones_suman_uno": all(
            math.isclose(sum(float(row["proporcion"]) for row in distributions if row["dominio_id"] == did), 1.0, abs_tol=1e-10)
            for did in ("TOTAL", "HOMBRES", "MUJERES")
            if domain_summary[did]["valid_mass"] > 0
        ),
        "reconciliacion_elegibles": all(sum(s["class_n"].values()) == s["n"] for s in domain_summary.values()),
        "reconstruccion_total_n": True,
        "reconstruccion_total_masa": True,
        "sexo_no_clasificable_n": len(unclassified),
        "sexo_no_clasificable_masa_peso_utilizable": unclassified_mass,
    }
    if not all(value is True for key, value in controls.items() if key.startswith(("particiones", "reconciliacion", "reconstruccion"))):
        raise ValueError(f"CONTROL-MATERIAL-FALLA:{controls}")
    return distributions, coverage, contrasts, controls


def _write(relative: str, raw: bytes) -> Path:
    root = Path(__file__).resolve().parents[3]
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def medir(inputs: dict, contrato: dict) -> dict:
    raw_inputs = {key: _read_input(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        actual = _sha256(raw_inputs[key])
        if actual != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{actual}")
    if not raw_inputs[INPUT_Q].startswith(b"%PDF") or not raw_inputs[INPUT_BACKGROUND].startswith(b"%PDF"):
        raise ValueError("DOCUMENTACION-NACIONAL-NO-PDF")
    evidence = raw_inputs[INPUT_CODEBOOK].decode("utf-8")
    for token in ("ZA6980 Version 2.0.0", "v26 - Q8a", "Family members or close friends", "9 No answer"):
        if token not in evidence:
            raise ValueError(f"EVIDENCIA-CODEBOOK-INCOMPLETA:{token}")

    dta = _zip_member(raw_inputs[INPUT_DTA], DTA_MEMBERS, DTA_MEMBER)
    sav = _zip_member(raw_inputs[INPUT_SAV], [SAV_MEMBER], SAV_MEMBER)
    metadata = verify_metadata(dta, sav)
    frame = pd.read_stata(io.BytesIO(dta), columns=AUTHORIZED_COLUMNS, convert_categoricals=False)
    mx = validate_and_select(frame)
    distributions, coverage, contrasts, controls = calculate(mx)
    raw_distribution = _serialize(distributions, DISTRIBUTION_COLUMNS)
    raw_coverage = _serialize(coverage, COVERAGE_COLUMNS)
    raw_contrast = _serialize(contrasts, CONTRAST_COLUMNS)
    raw_controls = (json.dumps({"calc_id": CALC_ID, **metadata, **controls}, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    _write("forense/analisis/issp-apoyo-monetario-cli-1/distribucion-total-sexo.csv", raw_distribution)
    _write("forense/analisis/issp-apoyo-monetario-cli-1/cobertura-total-sexo.csv", raw_coverage)
    _write("forense/analisis/issp-apoyo-monetario-cli-1/contraste-mujeres-menos-hombres.csv", raw_contrast)
    _write("forense/analisis/issp-apoyo-monetario-cli-1/controles-medidor.json", raw_controls)
    return {
        "RESULT-ISSP-APOYO-G-N-MEXICO": len(mx),
        "RESULT-ISSP-APOYO-G-N-FILAS-DISTRIBUCION": len(distributions),
        "RESULT-ISSP-APOYO-G-N-FILAS-COBERTURA": len(coverage),
        "RESULT-ISSP-APOYO-G-DISTRIBUCION-SHA256": _sha256(raw_distribution),
        "RESULT-ISSP-APOYO-G-COBERTURA-SHA256": _sha256(raw_coverage),
        "RESULT-ISSP-APOYO-G-CONTRASTE-SHA256": _sha256(raw_contrast),
        "RESULT-ISSP-APOYO-G-PRECISION": PRECISION,
        "RESULT-ISSP-APOYO-P1-TOTAL": points_from_rows(distributions, "TOTAL", 1),
        "RESULT-ISSP-APOYO-P1-HOMBRES": points_from_rows(distributions, "HOMBRES", 1),
        "RESULT-ISSP-APOYO-P1-MUJERES": points_from_rows(distributions, "MUJERES", 1),
        "RESULT-ISSP-APOYO-DELTA-P1-MUJERES-MENOS-HOMBRES": contrasts[0]["diferencia_menos_mas"],
    }


def points_from_rows(rows: list[dict], domain: str, code: int) -> float | None:
    return next(row["proporcion"] for row in rows if row["dominio_id"] == domain and row["codigo"] == code)
