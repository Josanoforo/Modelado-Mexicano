#!/usr/bin/env python3
"""Descriptivo preespecificado de ISSP México 2017, Q7a-e / v21-v25."""
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


CALC_ID = "CALC-ISSP2017-REDES-APOYO-COTIDIANO-0001"
ANALYSIS = "forense/analisis/issp2017-redes-apoyo-cotidiano-cli-1"
PRECISION = "EE-IC-NO-DISPONIBLES-DISENO-NO-ACREDITADO"
UNIVERSE = "Personas de 18 años o más, muestra nacional de México"
VERSION = "ZA6980 v2.0.0; DOI 10.4232/1.13322"
EXPECTED_SHA256 = {
    "za6980_q_mx": "61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed",
    "za6980_backgroundvar_mx": "6004c300ca1331bfd15f163c4deaa726c71b66b46ae9e05361f40ae8cc26ca5f",
    "za6980_v2_0_0_dta": "aa3bfcbcc1dc20a2735e8e9d2d3d47a72d909dade66e8c4623b910965dc227de",
    "za6980_v2_0_0_sav": "20a1420f4aa8f8dcb30f7de61879796d20b7c3042805e7925e56c30b4ae97ca5",
}
DTA_MEMBER = "ZA6980_v2-0-0.dta"
SAV_MEMBER = "ZA6980_v2-0-0.sav"
ITEMS = (
    ("v21", "Q7a", "Hogar o jardín", "household or garden"),
    ("v22", "Q7b", "Hogar durante enfermedad", "household when ill"),
    ("v23", "Q7c", "Hablar al sentirse deprimido", "feeling depressed"),
    ("v24", "Q7d", "Consejo sobre problemas familiares", "family problems advice"),
    ("v25", "Q7e", "Ocasión social agradable", "pleasant social occasion"),
)
CATEGORIES = (
    (1, "Close family member", "Familiar cercano"),
    (2, "More distant family member", "Familiar más lejano"),
    (3, "Close friend", "Amigo cercano"),
    (4, "Neighbour", "Vecino"),
    (5, "Someone I work with", "Alguien con quien trabajo"),
    (6, "Someone else", "Alguien más"),
    (7, "No one", "Ninguno"),
)
DOMAINS = (("TOTAL", "México, personas adultas", None), ("HOMBRES", "Hombres", 1), ("MUJERES", "Mujeres", 2))
AUTHORIZED_COLUMNS = ["studyno", "doi", "version", "country", "c_alphan", "CASEID", "SEX", "AGE", "WEIGHT", *[x[0] for x in ITEMS]]

COMMON = ["tipo", "calc_id", "version", "pais", "universo", "precision", "estado"]
DISTRIBUTION_COLUMNS = COMMON + ["variable", "item", "situacion", "dominio_id", "dominio", "codigo", "texto_integrado", "texto_mexico", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "porcentaje", "unidad"]
COVERAGE_COLUMNS = COMMON + ["variable", "item", "situacion", "dominio_id", "dominio", "clasificacion", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "unidad"]
FAMILY_COLUMNS = COMMON + ["variable", "item", "situacion", "dominio_id", "dominio", "codigos_agregados", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "porcentaje", "unidad"]
CONTRAST_COLUMNS = COMMON + ["variable", "item", "situacion", "contraste", "n_denominador_mujeres", "masa_denominador_mujeres", "n_numerador_mujeres", "masa_numerador_mujeres", "proporcion_mujeres", "n_denominador_hombres", "masa_denominador_hombres", "n_numerador_hombres", "masa_numerador_hombres", "proporcion_hombres", "diferencia", "diferencia_puntos_porcentuales", "unidad"]
COUNT_COLUMNS = COMMON + ["conteo_ninguno", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "porcentaje", "unidad"]
SUMMARY_COLUMNS = COMMON + ["indicador", "descripcion", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "porcentaje", "unidad"]
MATRIX_COLUMNS = COMMON + ["variable_fila", "item_fila", "variable_columna", "item_columna", "n_denominador", "masa_denominador", "n_numerador", "masa_numerador", "proporcion", "porcentaje", "unidad"]


def _read(entry: dict) -> bytes:
    return entry["bytes"] if entry.get("bytes") is not None else Path(entry["ruta_absoluta"]).read_bytes()


def _sha(raw: bytes) -> str:
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
    return out.getvalue().encode()


def _zip_member(raw: bytes, expected: list[str], member: str) -> bytes:
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if archive.testzip() is not None:
            raise ValueError("ZIP-CORRUPTO")
        names = [x.filename for x in archive.infolist() if not x.is_dir()]
        if names != expected:
            raise ValueError(f"MIEMBROS-ZIP-INESPERADOS:{names}")
        return archive.read(member)


def _metadata(raw: bytes, suffix: str):
    with tempfile.NamedTemporaryFile(suffix=suffix) as handle:
        handle.write(raw)
        handle.flush()
        reader = pyreadstat.read_dta if suffix == ".dta" else pyreadstat.read_sav
        _, meta = reader(handle.name, metadataonly=True)
    return meta


def verify_metadata(dta_raw: bytes, sav_raw: bytes) -> dict:
    dta, sav = _metadata(dta_raw, ".dta"), _metadata(sav_raw, ".sav")
    for meta, kind in ((dta, "DTA"), (sav, "SAV")):
        if (meta.number_rows, meta.number_columns) != (44492, 356):
            raise ValueError(f"DIMENSION-{kind}-INESPERADA")
        for variable, _, _, _ in ITEMS:
            expected = {float(code): english for code, english, _ in CATEGORIES} | {8.0: "Can't choose", 9.0: "No answer"}
            actual = meta.value_labels[meta.variable_to_label[variable]]
            if actual != expected:
                raise ValueError(f"ETIQUETAS-{variable}-{kind}-INESPERADAS:{actual}")
    for variable in AUTHORIZED_COLUMNS:
        if dta.column_names_to_labels.get(variable) != sav.column_names_to_labels.get(variable):
            raise ValueError(f"ETIQUETA-DTA-SAV-DISCREPA:{variable}")
    return {"filas_fuente": 44492, "columnas_fuente": 356, "metadatos_dta_sav": True}


def _num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def validate_and_select(frame: pd.DataFrame) -> pd.DataFrame:
    if list(frame.columns) != AUTHORIZED_COLUMNS:
        raise ValueError(f"COLUMNAS-NO-AUTORIZADAS:{list(frame.columns)}")
    mx = frame.loc[frame["c_alphan"].astype(str).eq("MX")].copy()
    if len(mx) != 1002 or not _num(mx["country"]).eq(484).all():
        raise ValueError("IDENTIDAD-MEXICO-DISCREPA")
    if not _num(mx["studyno"]).eq(6980).all() or set(mx["doi"].astype(str)) != {"doi:10.4232/1.13322"}:
        raise ValueError("IDENTIDAD-ESTUDIO-DISCREPA")
    if set(mx["version"].astype(str)) != {"2.0.0 (2019-08-19)"}:
        raise ValueError("VERSION-DISCREPA")
    if mx["CASEID"].isna().any() or mx["CASEID"].duplicated().any():
        raise ValueError("CASEID-NO-UNICO-O-FALTANTE")
    mx["SEX"], mx["AGE"], mx["WEIGHT"] = _num(mx["SEX"]), _num(mx["AGE"]), _num(mx["WEIGHT"])
    if not mx["SEX"].dropna().isin([1, 2, 9]).all():
        raise ValueError("SEX-FUERA-DE-CATALOGO")
    observed_age = mx.loc[mx["AGE"].notna() & mx["AGE"].ne(999), "AGE"]
    if (observed_age < 18).any():
        raise ValueError("EDAD-MENOR-DE-18")
    for variable, _, _, _ in ITEMS:
        mx[variable] = _num(mx[variable])
        if not mx[variable].dropna().isin(range(1, 10)).all():
            raise ValueError(f"{variable}-FUERA-DE-CATALOGO")
    return mx


def _weight_ok(frame: pd.DataFrame) -> pd.Series:
    return frame["WEIGHT"].notna() & frame["WEIGHT"].map(math.isfinite) & frame["WEIGHT"].gt(0)


def _base(state="OK") -> dict:
    return {"tipo": "RESULT", "calc_id": CALC_ID, "version": VERSION, "pais": "México", "universo": UNIVERSE, "precision": PRECISION, "estado": state}


def _ratio(numerator: float, denominator: float):
    return None if denominator <= 0 else numerator / denominator


def calculate(frame: pd.DataFrame):
    frame = frame.copy()
    for col in ["SEX", "WEIGHT", *[x[0] for x in ITEMS]]:
        frame[col] = _num(frame[col])
    distributions, coverage, families, contrasts = [], [], [], []
    family_points = {}
    domain_summaries = {}
    for variable, item, situation, _ in ITEMS:
        for domain_id, domain, sex_code in DOMAINS:
            part = frame if sex_code is None else frame.loc[frame["SEX"].eq(sex_code)]
            wok = _weight_ok(part)
            valid = wok & part[variable].isin(range(1, 8))
            cant = wok & part[variable].eq(8)
            noanswer = wok & (part[variable].eq(9) | part[variable].isna())
            invalid = ~wok
            if not (valid | cant | noanswer | invalid).all():
                raise ValueError(f"PARTICION-INCOMPLETA:{variable}:{domain_id}")
            dn, dm = int(valid.sum()), float(part.loc[valid, "WEIGHT"].sum())
            en, em = len(part), float(part.loc[wok, "WEIGHT"].sum())
            domain_summaries[(variable, domain_id)] = (en, em, {"VALIDA": int(valid.sum()), "NO_PUEDE_ELEGIR": int(cant.sum()), "NO_RESPUESTA": int(noanswer.sum()), "PESO_INVALIDO": int(invalid.sum())})
            for code, english, spanish in CATEGORIES:
                mask = valid & part[variable].eq(code)
                nn, nm = int(mask.sum()), float(part.loc[mask, "WEIGHT"].sum())
                point = _ratio(nm, dm)
                distributions.append({**_base("OK" if point is not None else "DENOMINADOR-NULO"), "variable": variable, "item": item, "situacion": situation, "dominio_id": domain_id, "dominio": domain, "codigo": code, "texto_integrado": english, "texto_mexico": spanish, "n_denominador": dn, "masa_denominador": dm, "n_numerador": nn, "masa_numerador": nm, "proporcion": point, "porcentaje": None if point is None else 100 * point, "unidad": "proporcion-de-respuestas-validas"})
            for label, mask in (("VALIDA", valid), ("NO_PUEDE_ELEGIR", cant), ("NO_RESPUESTA", noanswer), ("PESO_INVALIDO", invalid)):
                nn = int(mask.sum())
                nm = None if label == "PESO_INVALIDO" else float(part.loc[mask, "WEIGHT"].sum())
                point = _ratio(float(nn if nm is None else nm), float(en if nm is None else em))
                coverage.append({**_base("OK" if (en if nm is None else em) > 0 else "DENOMINADOR-NULO"), "variable": variable, "item": item, "situacion": situation, "dominio_id": domain_id, "dominio": domain, "clasificacion": label, "n_denominador": en, "masa_denominador": em, "n_numerador": nn, "masa_numerador": nm, "proporcion": point, "unidad": "proporcion-de-elegibles"})
            family = valid & part[variable].isin([1, 2])
            fn, fm = int(family.sum()), float(part.loc[family, "WEIGHT"].sum())
            fp = _ratio(fm, dm)
            family_points[(variable, domain_id)] = (dn, dm, fn, fm, fp)
            families.append({**_base("OK" if fp is not None else "DENOMINADOR-NULO"), "variable": variable, "item": item, "situacion": situation, "dominio_id": domain_id, "dominio": domain, "codigos_agregados": "1+2", "n_denominador": dn, "masa_denominador": dm, "n_numerador": fn, "masa_numerador": fm, "proporcion": fp, "porcentaje": None if fp is None else 100 * fp, "unidad": "proporcion-familia"})
        wn, wm, wnn, wnm, wp = family_points[(variable, "MUJERES")]
        mn, mm, mnn, mnm, mp = family_points[(variable, "HOMBRES")]
        delta = None if wp is None or mp is None else wp - mp
        contrasts.append({**_base("OK" if delta is not None else "DENOMINADOR-NULO"), "variable": variable, "item": item, "situacion": situation, "contraste": "MUJERES-MENOS-HOMBRES", "n_denominador_mujeres": wn, "masa_denominador_mujeres": wm, "n_numerador_mujeres": wnn, "masa_numerador_mujeres": wnm, "proporcion_mujeres": wp, "n_denominador_hombres": mn, "masa_denominador_hombres": mm, "n_numerador_hombres": mnn, "masa_numerador_hombres": mnm, "proporcion_hombres": mp, "diferencia": delta, "diferencia_puntos_porcentuales": None if delta is None else 100 * delta, "unidad": "puntos-porcentuales"})

    wok = _weight_ok(frame)
    complete = wok.copy()
    for variable, _, _, _ in ITEMS:
        complete &= frame[variable].isin(range(1, 8))
    comp = frame.loc[complete].copy()
    comp["conteo"] = sum(comp[v].eq(7).astype(int) for v, _, _, _ in ITEMS)
    cn, cm = len(comp), float(comp["WEIGHT"].sum())
    count_rows = []
    for k in range(6):
        mask = comp["conteo"].eq(k)
        nn, nm = int(mask.sum()), float(comp.loc[mask, "WEIGHT"].sum())
        p = _ratio(nm, cm)
        count_rows.append({**_base("OK" if p is not None else "DENOMINADOR-NULO"), "conteo_ninguno": k, "n_denominador": cn, "masa_denominador": cm, "n_numerador": nn, "masa_numerador": nm, "proporcion": p, "porcentaje": None if p is None else 100 * p, "unidad": "proporcion-casos-completos"})
    summary_rows = []
    for indicator, description, mask in (
        ("NINGUNA_SITUACION", "Cero situaciones con ninguno", comp["conteo"].eq(0)),
        ("ALGUNA_SITUACION", "Una o más situaciones con ninguno", comp["conteo"].ge(1)),
        ("TODAS_SITUACIONES", "Cinco situaciones con ninguno", comp["conteo"].eq(5)),
    ):
        nn, nm = int(mask.sum()), float(comp.loc[mask, "WEIGHT"].sum())
        p = _ratio(nm, cm)
        summary_rows.append({**_base("OK" if p is not None else "DENOMINADOR-NULO"), "indicador": indicator, "descripcion": description, "n_denominador": cn, "masa_denominador": cm, "n_numerador": nn, "masa_numerador": nm, "proporcion": p, "porcentaje": None if p is None else 100 * p, "unidad": "proporcion-casos-completos"})
    eligible_n, eligible_mass = int(wok.sum()), float(frame.loc[wok, "WEIGHT"].sum())
    p = _ratio(cm, eligible_mass)
    summary_rows.append({**_base("OK" if p is not None else "DENOMINADOR-NULO"), "indicador": "COBERTURA_CASOS_COMPLETOS", "descripcion": "Cinco respuestas válidas respecto de entrevistados con peso utilizable", "n_denominador": eligible_n, "masa_denominador": eligible_mass, "n_numerador": cn, "masa_numerador": cm, "proporcion": p, "porcentaje": None if p is None else 100 * p, "unidad": "proporcion-entrevistados-peso-utilizable"})

    matrix = []
    for vr, ir, _, _ in ITEMS:
        for vc, ic, _, _ in ITEMS:
            mask = comp[vr].eq(7) & comp[vc].eq(7)
            nn, nm = int(mask.sum()), float(comp.loc[mask, "WEIGHT"].sum())
            p = _ratio(nm, cm)
            matrix.append({**_base("OK" if p is not None else "DENOMINADOR-NULO"), "variable_fila": vr, "item_fila": ir, "variable_columna": vc, "item_columna": ic, "n_denominador": cn, "masa_denominador": cm, "n_numerador": nn, "masa_numerador": nm, "proporcion": p, "porcentaje": None if p is None else 100 * p, "unidad": "proporcion-casos-completos"})

    classified = frame["SEX"].isin([1, 2])
    residual = frame.loc[~classified]
    residual_ok = _weight_ok(residual)
    matrix_map = {(r["variable_fila"], r["variable_columna"]): r for r in matrix}
    controls = {
        "particiones_distribucion": all(abs(sum((r["proporcion"] or 0) for r in distributions if r["variable"] == v and r["dominio_id"] == d) - 1) < 1e-10 for v, _, _, _ in ITEMS for d, _, _ in DOMAINS if family_points[(v, d)][1] > 0),
        "reconciliacion_cobertura": all(sum(s[2].values()) == s[0] for s in domain_summaries.values()),
        "agregado_familia_coincide": all(abs((family_points[(v, d)][4] or 0) - sum((r["proporcion"] or 0) for r in distributions if r["variable"] == v and r["dominio_id"] == d and r["codigo"] in (1, 2))) < 1e-10 for v, _, _, _ in ITEMS for d, _, _ in DOMAINS),
        "reconstruccion_total_n": len(frame) == int(frame["SEX"].eq(1).sum()) + int(frame["SEX"].eq(2).sum()) + len(residual),
        "reconstruccion_total_masa": math.isclose(float(frame.loc[wok, "WEIGHT"].sum()), float(frame.loc[wok & frame["SEX"].eq(1), "WEIGHT"].sum()) + float(frame.loc[wok & frame["SEX"].eq(2), "WEIGHT"].sum()) + float(residual.loc[residual_ok, "WEIGHT"].sum()), abs_tol=1e-10),
        "conteo_exhaustivo": sum(r["n_numerador"] for r in count_rows) == cn and math.isclose(sum(r["masa_numerador"] for r in count_rows), cm, abs_tol=1e-10),
        "matriz_simetrica": all(matrix_map[(a, b)]["n_numerador"] == matrix_map[(b, a)]["n_numerador"] and math.isclose(matrix_map[(a, b)]["masa_numerador"], matrix_map[(b, a)]["masa_numerador"], abs_tol=1e-10) for a, _, _, _ in ITEMS for b, _, _, _ in ITEMS),
        "diagonal_marginal": all(matrix_map[(v, v)]["n_numerador"] == int(comp[v].eq(7).sum()) for v, _, _, _ in ITEMS),
        "sexo_no_clasificable_n": len(residual),
        "sexo_no_clasificable_masa": float(residual.loc[residual_ok, "WEIGHT"].sum()),
        "n_casos_completos": cn,
        "masa_casos_completos": cm,
    }
    for key, value in controls.items():
        if isinstance(value, bool) and not value:
            raise ValueError(f"CONTROL-MATERIAL-FALLA:{key}")
    return distributions, coverage, families, contrasts, count_rows, summary_rows, matrix, controls


def _write(relative: str, raw: bytes):
    path = Path(__file__).resolve().parents[3] / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def _pick(rows, key, value, field="proporcion"):
    return next(r[field] for r in rows if r[key] == value)


def medir(inputs: dict, contrato: dict) -> dict:
    raw = {key: _read(inputs[key]) for key in EXPECTED_SHA256}
    for key, expected in EXPECTED_SHA256.items():
        if _sha(raw[key]) != expected:
            raise ValueError(f"SHA256-INESPERADO:{key}:{_sha(raw[key])}")
    evidence = _read(inputs["za6980_q7_evidencia"]).decode()
    for token in ("v21 = Q7a", "v25 = Q7e", "página impresa 58", "7 No one", "operación no es ciega"):
        if token not in evidence:
            raise ValueError(f"EVIDENCIA-INCOMPLETA:{token}")
    dta = _zip_member(raw["za6980_v2_0_0_dta"], [DTA_MEMBER, "ZA6980_v2-0-0_missing.txt"], DTA_MEMBER)
    sav = _zip_member(raw["za6980_v2_0_0_sav"], [SAV_MEMBER], SAV_MEMBER)
    metadata = verify_metadata(dta, sav)
    frame = pd.read_stata(io.BytesIO(dta), columns=AUTHORIZED_COLUMNS, convert_categoricals=False)
    mx = validate_and_select(frame)
    outputs = calculate(mx)
    names = [
        ("distribucion-item-sexo.csv", outputs[0], DISTRIBUTION_COLUMNS),
        ("cobertura-item-sexo.csv", outputs[1], COVERAGE_COLUMNS),
        ("agregado-familia-item-sexo.csv", outputs[2], FAMILY_COLUMNS),
        ("contraste-familia-mujeres-menos-hombres.csv", outputs[3], CONTRAST_COLUMNS),
        ("conteo-situaciones-ninguno.csv", outputs[4], COUNT_COLUMNS),
        ("resumen-y-cobertura-casos-completos.csv", outputs[5], SUMMARY_COLUMNS),
        ("matriz-coocurrencia-ninguno.csv", outputs[6], MATRIX_COLUMNS),
    ]
    digests = {}
    for filename, rows, columns in names:
        payload = _serialize(rows, columns)
        _write(f"{ANALYSIS}/{filename}", payload)
        digests[filename] = _sha(payload)
    controls_raw = (json.dumps({"calc_id": CALC_ID, **metadata, **outputs[7]}, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()
    _write(f"{ANALYSIS}/controles-medidor-issp2017-redes-apoyo-cotidiano.json", controls_raw)
    results = {
        "RESULT-ISSP-REDES-G-N-MEXICO": len(mx),
        "RESULT-ISSP-REDES-G-PRECISION": PRECISION,
        "RESULT-ISSP-REDES-G-DISTRIBUCION-SHA256": digests["distribucion-item-sexo.csv"],
        "RESULT-ISSP-REDES-G-COBERTURA-SHA256": digests["cobertura-item-sexo.csv"],
        "RESULT-ISSP-REDES-G-FAMILIA-SHA256": digests["agregado-familia-item-sexo.csv"],
        "RESULT-ISSP-REDES-G-CONTRASTE-SHA256": digests["contraste-familia-mujeres-menos-hombres.csv"],
        "RESULT-ISSP-REDES-G-CONTEO-SHA256": digests["conteo-situaciones-ninguno.csv"],
        "RESULT-ISSP-REDES-G-RESUMEN-SHA256": digests["resumen-y-cobertura-casos-completos.csv"],
        "RESULT-ISSP-REDES-G-MATRIZ-SHA256": digests["matriz-coocurrencia-ninguno.csv"],
    }
    for variable, item, _, _ in ITEMS:
        results[f"RESULT-ISSP-REDES-{item}-FAMILIA-TOTAL"] = next(r["proporcion"] for r in outputs[2] if r["variable"] == variable and r["dominio_id"] == "TOTAL")
        results[f"RESULT-ISSP-REDES-{item}-DELTA-FAMILIA-MUJERES-MENOS-HOMBRES"] = next(r["diferencia"] for r in outputs[3] if r["variable"] == variable)
    results["RESULT-ISSP-REDES-P3-COBERTURA-COMPLETOS"] = _pick(outputs[5], "indicador", "COBERTURA_CASOS_COMPLETOS")
    results["RESULT-ISSP-REDES-P3-ALGUNA-SITUACION-NINGUNO"] = _pick(outputs[5], "indicador", "ALGUNA_SITUACION")
    results["RESULT-ISSP-REDES-P3-TODAS-SITUACIONES-NINGUNO"] = _pick(outputs[5], "indicador", "TODAS_SITUACIONES")
    return results
