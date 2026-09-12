"""Medidor congelado de valoración declarada de seguridad social, MOTRAL 2015.

Lee los DBF directamente dentro de sus ZIP, une MOTRAL con el
sociodemográfico ENOE 2015-T2 por la llave estándar y devuelve puntos e
incertidumbre de diseño. No usa el último empleo retrospectivo como empleo
actual y no interpreta P17 como una comparación explícita de salarios.
"""
from __future__ import annotations

import json
import math
import struct
import zipfile
from collections import Counter, defaultdict


MOTRAL_ID = "motral2015_bases_datos_dbf"
ENOE_ID = "enoe_2015_trim2_dbf"
PREFIX = "RESULT-MOTRAL15-"
KEY = ("CD_A", "ENT", "CON", "V_SEL", "N_HOG", "H_MUD", "N_REN")
RANK_FIELDS = ("P16_1", "P16_2", "P16_3", "P16_4", "P16_5")
BENEFITS = ("MEDICO", "VIDA", "ACCIDENTES", "PENSION", "VIVIENDA")
SEGMENTS = (
    ("TOTAL", lambda row: True),
    ("HOMBRE", lambda row: row["SEX"] == "1"),
    ("MUJER", lambda row: row["SEX"] == "2"),
    ("EDAD18_34", lambda row: 18 <= int(row["EDA"]) <= 34),
    ("EDAD35_54", lambda row: 35 <= int(row["EDA"]) <= 54),
)


def _member(zf, basename):
    matches = [n for n in zf.namelist() if n.rsplit("/", 1)[-1].upper() == basename.upper()]
    if len(matches) != 1:
        raise ValueError(f"MIEMBRO-NO-UNIVOCO:{basename}:{matches}")
    return matches[0]


def _read_dbf(zip_path, basename, required):
    """Lector DBF mínimo y determinista para campos C/N sin extraer payloads."""
    with zipfile.ZipFile(zip_path) as zf:
        if zf.testzip() is not None:
            raise ValueError(f"ZIP-CORRUPTO:{basename}")
        with zf.open(_member(zf, basename)) as fh:
            header = fh.read(32)
            if len(header) != 32:
                raise ValueError(f"DBF-CABECERA-TRUNCADA:{basename}")
            n_records = struct.unpack_from("<I", header, 4)[0]
            header_len = struct.unpack_from("<H", header, 8)[0]
            record_len = struct.unpack_from("<H", header, 10)[0]
            fields, offset = [], 1
            consumed = 32
            while True:
                first = fh.read(1)
                consumed += 1
                if first == b"\r":
                    break
                rest = fh.read(31)
                consumed += 31
                if len(rest) != 31:
                    raise ValueError(f"DBF-DESCRIPTOR-TRUNCADO:{basename}")
                desc = first + rest
                name = desc[:11].split(b"\0", 1)[0].decode("ascii").upper()
                kind = chr(desc[11])
                length = desc[16]
                fields.append((name, kind, offset, length))
                offset += length
            if consumed < header_len:
                fh.read(header_len - consumed)
            elif consumed > header_len:
                raise ValueError(f"DBF-HEADER-LEN-INVALIDO:{basename}")
            if offset != record_len:
                raise ValueError(f"DBF-RECORD-LEN-INVALIDO:{basename}:{offset}:{record_len}")
            by_name = {name: (kind, start, length) for name, kind, start, length in fields}
            missing = sorted(set(required) - set(by_name))
            if missing:
                raise ValueError(f"COLUMNAS-AUSENTES:{basename}:{missing}")
            selected = {name: by_name[name] for name in required}
            rows = []
            deleted = 0
            for _ in range(n_records):
                raw = fh.read(record_len)
                if len(raw) != record_len:
                    raise ValueError(f"DBF-REGISTRO-TRUNCADO:{basename}")
                if raw[:1] == b"*":
                    deleted += 1
                    continue
                row = {}
                for name, (_kind, start, length) in selected.items():
                    row[name] = raw[start:start + length].decode("latin-1").strip()
                rows.append(row)
    return rows, {"records_header": n_records, "records_deleted": deleted,
                  "fields": len(fields), "record_len": record_len}


def _weight(value):
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) and result > 0 else None


def _eligible(row):
    try:
        age = int(row["EDA"])
    except (TypeError, ValueError):
        return False
    return row["R_DEF"] == "00" and 18 <= age <= 54 and row["C_TRA"] in {"1", "2"}


def _ranking_status(row):
    ranks = [row[field] for field in RANK_FIELDS]
    valid = [value for value in ranks if value in {"1", "2", "3", "4", "5"}]
    first = [i for i, value in enumerate(ranks) if value == "1"]
    if len(first) > 1 or len(valid) != len(set(valid)):
        return "INCONSISTENTE", None
    if len(first) == 1 and sorted(valid) == ["1", "2", "3", "4", "5"]:
        return "COMPLETO", first[0]
    if len(first) == 1:
        return "INCOMPLETO-CON-PRIMERO", first[0]
    if any(value not in {"", "9"} for value in ranks):
        return "INCONSISTENTE", None
    return "INCOMPLETO-SIN-PRIMERO", None


def _estimate(all_rows, domain, outcome):
    eligible = [row for row in all_rows if domain(row)]
    valid = [(row, _weight(row["FAC_MOTRAL"])) for row in eligible if outcome(row) is not None]
    invalid_weight = sum(weight is None for _, weight in valid)
    valid = [(row, weight) for row, weight in valid if weight is not None]
    unknown = [row for row in eligible if outcome(row) is None]
    denominator = math.fsum(weight for _, weight in valid)
    numerator_rows = [(row, weight) for row, weight in valid if outcome(row)]
    numerator = math.fsum(weight for _, weight in numerator_rows)
    unknown_mass = math.fsum(_weight(row["FAC_MOTRAL"]) or 0.0 for row in unknown)
    base = {
        "n_expuesto": len(eligible), "n_valido": len(valid), "n_desconocido": len(unknown),
        "masa_desconocido": unknown_mass, "n_numerador": len(numerator_rows),
        "masa_numerador": numerator, "masa_denominador": denominator,
        "n_peso_invalido": invalid_weight,
    }
    if denominator <= 0:
        return {**base, "p": None, "ee": None, "ic95_lo": None, "ic95_hi": None,
                "gl": 0, "precision_estado": "NO-DISPONIBLE:DENOMINADOR-NULO"}
    p_hat = numerator / denominator
    psu_z = defaultdict(float)
    psus = defaultdict(set)
    missing_design = 0
    for row in all_rows:
        weight = _weight(row["FAC_MOTRAL"])
        if weight is None:
            continue
        h = (row["CD_A"], row["EST_D"])
        u = row["UPM"]
        if not all(h) or not u:
            missing_design += 1
            continue
        psus[h].add(u)
        value = outcome(row) if domain(row) else None
        if value is not None:
            psu_z[h, u] += weight * ((1.0 if value else 0.0) - p_hat) / denominator
        else:
            psu_z[h, u] += 0.0
    df = sum(max(0, len(items) - 1) for items in psus.values())
    singleton = 0
    terms = []
    for h, items in psus.items():
        values = [psu_z[h, u] for u in items]
        if len(values) < 2:
            singleton += 1
            continue
        center = math.fsum(values) / len(values)
        terms.append(len(values) / (len(values) - 1) * math.fsum((v - center) ** 2 for v in values))
    if missing_design or df <= 0:
        return {**base, "p": p_hat, "ee": None, "ic95_lo": None, "ic95_hi": None,
                "gl": df, "precision_estado": "NO-DISPONIBLE:DISENO-INCOMPLETO"}
    se = math.sqrt(max(0.0, math.fsum(terms)))
    return {
        **base, "p": p_hat, "ee": se,
        "ic95_lo": max(0.0, p_hat - 1.96 * se),
        "ic95_hi": min(1.0, p_hat + 1.96 * se), "gl": df,
        "precision_estado": f"DISPONIBLE:NORMAL95-LINEALIZACION-RAZON;SINGLETON={singleton};FPC-NO-APLICADA",
    }


def _rounded(record):
    return {key: (round(value, 12) if isinstance(value, float) else value)
            for key, value in record.items()}


def medir(inputs, contrato):
    module_required = set(KEY) | {
        "UPM", "EST_D", "R_DEF", "SEX", "EDA", "C_TRA", "P17", "FAC_MOTRAL",
    } | set(RANK_FIELDS)
    enoe_required = set(KEY) | {"CLASE2", "SEG_SOC"}
    rows, module_meta = _read_dbf(
        inputs[MOTRAL_ID]["ruta_absoluta"], "motral2015_cuestionario.dbf", module_required
    )
    enoe_rows, enoe_meta = _read_dbf(
        inputs[ENOE_ID]["ruta_absoluta"], "SDEMT215.DBF", enoe_required
    )
    module_keys = [tuple(row[c] for c in KEY) for row in rows]
    if len(set(module_keys)) != len(module_keys):
        raise ValueError("LLAVE-MOTRAL-NO-UNICA")
    wanted = set(module_keys)
    enoe_map = {}
    enoe_duplicates = 0
    for row in enoe_rows:
        key = tuple(row[c] for c in KEY)
        if key not in wanted:
            continue
        if key in enoe_map:
            enoe_duplicates += 1
        else:
            enoe_map[key] = row
    if enoe_duplicates:
        raise ValueError(f"JOIN-MUCHOS-A-MUCHOS:{enoe_duplicates}")
    for row, key in zip(rows, module_keys):
        linked = enoe_map.get(key)
        row["ENOE_MATCH"] = "1" if linked else "0"
        row["ENOE_CLASE2"] = linked["CLASE2"] if linked else ""
        row["ENOE_SEG_SOC"] = linked["SEG_SOC"] if linked else ""
        status, first = _ranking_status(row)
        row["RANK_STATUS"] = status
        row["RANK_FIRST"] = first

    eligible = [row for row in rows if _eligible(row)]
    matched_eligible = [row for row in eligible if row["ENOE_MATCH"] == "1"]
    occupied = [row for row in matched_eligible if row["ENOE_CLASE2"] == "1"]
    diagnostics = {
        "motral": {**module_meta, "filas": len(rows), "llaves_unicas": len(set(module_keys))},
        "enoe": {**enoe_meta, "filas": len(enoe_rows)},
        "join": {
            "llave": "+".join(KEY), "coincidencias": len(enoe_map),
            "perdidas": len(rows) - len(enoe_map), "duplicados_enoe": enoe_duplicates,
            "elegibles_coincidencias": len(matched_eligible),
            "elegibles_perdidas": len(eligible) - len(matched_eligible),
        },
        "filtros": {
            "elegibles": len(eligible), "no_elegibles": len(rows) - len(eligible),
            "sexo_desconocido": sum(row["SEX"] not in {"1", "2"} for row in eligible),
            "edad_fuera_o_invalida": sum(not _eligible({**row, "R_DEF": "00", "C_TRA": "1"}) for row in rows),
        },
        "ranking": dict(sorted(Counter(row["RANK_STATUS"] for row in eligible).items())),
        "enoe_ocupada": {
            "n": len(occupied),
            "cobertura": dict(sorted(Counter(row["ENOE_SEG_SOC"] or "BLANCO" for row in occupied).items())),
        },
        "peso": "FAC_MOTRAL;FAC_ENOE_NO-USADO",
    }

    estimates = {}
    for segment, predicate in SEGMENTS:
        domain = lambda row, pred=predicate: _eligible(row) and pred(row)
        p17 = _estimate(rows, domain, lambda row: row["P17"] == "1" if row["P17"] in {"1", "2"} else None)
        estimates[f"P17-{segment}"] = _rounded(p17)
        for index, benefit in enumerate(BENEFITS):
            rank = _estimate(
                rows, domain,
                lambda row, idx=index: row["RANK_FIRST"] == idx if row["RANK_FIRST"] is not None else None,
            )
            estimates[f"P16-FIRST-{segment}-{benefit}"] = _rounded(rank)

    for code, value in (("CON-ACCESO", "1"), ("SIN-ACCESO", "2")):
        domain = lambda row, v=value: (
            _eligible(row) and row["ENOE_MATCH"] == "1" and
            row["ENOE_CLASE2"] == "1" and row["ENOE_SEG_SOC"] == v
        )
        estimates[f"ENOE-P17-{code}"] = _rounded(
            _estimate(rows, domain, lambda row: row["P17"] == "1" if row["P17"] in {"1", "2"} else None)
        )

    out = {
        PREFIX + "G-N-ESTIMANDOS": len(estimates),
        PREFIX + "G-DIAGNOSTICOS-JSON": json.dumps(diagnostics, ensure_ascii=False, sort_keys=True),
        PREFIX + "G-ESTIMANDOS-JSON": json.dumps(estimates, ensure_ascii=False, sort_keys=True),
        PREFIX + "G-JOIN-COINCIDENCIAS": diagnostics["join"]["coincidencias"],
        PREFIX + "G-JOIN-PERDIDAS": diagnostics["join"]["perdidas"],
        PREFIX + "G-JOIN-DUPLICADOS": diagnostics["join"]["duplicados_enoe"],
        PREFIX + "G-ELEGIBLES": diagnostics["filtros"]["elegibles"],
        PREFIX + "G-RANKING-COMPLETO": diagnostics["ranking"].get("COMPLETO", 0),
        PREFIX + "G-RANKING-INCOMPLETO-CON-PRIMERO": diagnostics["ranking"].get("INCOMPLETO-CON-PRIMERO", 0),
        PREFIX + "G-RANKING-INCONSISTENTE": diagnostics["ranking"].get("INCONSISTENTE", 0),
    }
    for name, record in estimates.items():
        out[PREFIX + name + "-P"] = record["p"]
    return out
