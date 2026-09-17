"""Medidor prospectivo de U4 histórico (persona) para ENVIPE 2013/2015.

La configuración física vive en cada ``spec.yaml``. El lector abre sólo el ZIP
declarado por corrida y conserva el marco observado completo de personas para
la sensibilidad de varianza de dominio.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import math
import struct
import zipfile

import numpy as np


def _member(archive: zipfile.ZipFile, wanted: str) -> str:
    matches = [n for n in archive.namelist() if n.replace("\\", "/").casefold() == wanted.casefold()]
    if len(matches) != 1:
        raise RuntimeError(f"MIEMBRO:{wanted}:COINCIDENCIAS={len(matches)}")
    return matches[0]


def _dbf(raw: bytes, columns: list[str]) -> tuple[list[dict[str, str]], str]:
    if len(raw) < 32:
        raise RuntimeError("DBF-CABECERA-TRUNCADA")
    nrec, hlen, rlen = struct.unpack("<IHH", raw[4:12])
    codepage = raw[29]
    fields, offset, pos = [], 1, 32
    while pos + 32 <= hlen and raw[pos] != 0x0D:
        desc = raw[pos:pos + 32]
        name = desc[:11].split(b"\x00", 1)[0].decode("ascii").upper()
        fields.append((name, offset, desc[16]))
        offset += desc[16]
        pos += 32
    if offset != rlen:
        raise RuntimeError(f"DBF-RLEN:{rlen}!={offset}")
    mapping = {name: (start, size) for name, start, size in fields}
    missing = [c for c in columns if c.upper() not in mapping]
    if missing:
        raise RuntimeError("COLUMNAS-AUSENTES:" + ",".join(missing))
    rows, deleted, truncated = [], 0, 0
    for i in range(nrec):
        start = hlen + i * rlen
        record = raw[start:start + rlen]
        if len(record) != rlen:
            truncated += 1
            break
        if record[:1] == b"*":
            deleted += 1
            continue
        row = {}
        for column in columns:
            field_start, size = mapping[column.upper()]
            row[column.upper()] = record[field_start:field_start + size].decode("latin-1").strip()
        rows.append(row)
    profile = (
        f"nrec_cabecera={nrec};rlen={rlen};hlen={hlen};n_campos={len(fields)};"
        f"codepage=0x{codepage:02x};borrados={deleted};truncados={truncated};leidos={len(rows)}"
    )
    return rows, profile


def _integer(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return int(number) if math.isfinite(number) and number == int(number) else None


def _weight(value):
    text = "" if value is None else str(value).strip()
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if math.isfinite(number) and number > 0 else None


def _key(row, columns):
    values = tuple(row[c].strip() for c in columns)
    return values if all(values) else None


def _bootstrap(frame, replicas: int, seed: int, outcome: str):
    """Bootstrap de UPM por estrato sobre el marco observado, no sólo U4."""
    by_psu = defaultdict(lambda: [0.0, 0.0])
    for row in frame:
        key = (row["stratum"], row["psu"])
        by_psu[key][0] += row["weight"] * row["domain"]
        by_psu[key][1] += row["weight"] * row["domain"] * row[outcome]
    by_stratum = defaultdict(list)
    for (stratum, _), pair in by_psu.items():
        by_stratum[stratum].append(pair)
    rng = np.random.Generator(np.random.PCG64(seed))
    denominator = np.zeros(replicas)
    numerator = np.zeros(replicas)
    singleton = 0
    for pairs in by_stratum.values():
        values = np.asarray(pairs, dtype=float)
        n_psu = len(values)
        if n_psu == 1:
            singleton += 1
            denominator += values[0, 0]
            numerator += values[0, 1]
            continue
        selected = rng.integers(0, n_psu, size=(replicas, n_psu))
        sampled = values[selected].sum(axis=1)
        denominator += sampled[:, 0]
        numerator += sampled[:, 1]
    valid = denominator > 0
    if not valid.any():
        return None, None, len(by_stratum), len(by_psu), singleton, 0
    ratios = numerator[valid] / denominator[valid]
    lo, hi = np.percentile(ratios, [2.5, 97.5])
    return float(lo), float(hi), len(by_stratum), len(by_psu), singleton, int(valid.sum())


def medir(inputs, contrato):
    p = contrato["parametros"]
    prefix = p["result_prefix"]
    payload = inputs[p["payload_id"]]["ruta_absoluta"]
    module_columns = list(dict.fromkeys(
        p["join_columns"] + ["BPCOD", "BP1_20", "BP1_23", "FAC_DEL"]
    ))
    person_columns = list(dict.fromkeys(
        p["join_columns"] + [p["identity_field"], "FAC_ELE", p["stratum_field"], p["psu_field"]]
        if p.get("identity_field") else
        p["join_columns"] + ["FAC_ELE", p["stratum_field"], p["psu_field"]]
    ))
    with zipfile.ZipFile(payload) as archive:
        module_name = _member(archive, p["module_member"])
        person_name = _member(archive, p["person_member"])
        module_rows, module_profile = _dbf(archive.read(module_name), module_columns)
        person_rows, person_profile = _dbf(archive.read(person_name), person_columns)

    excluded = Counter()
    events = defaultdict(lambda: {"c1": 0, "c2": 0, "n": 0})
    n_u1 = 0
    for row in module_rows:
        bpcod = _integer(row["BPCOD"])
        if bpcod not in p["personal_codes"]:
            excluded["BPCOD"] += 1
            continue
        if _integer(row["BP1_20"]) != 2:
            excluded["NO_DENUNCIA"] += 1
            continue
        reason = _integer(row["BP1_23"])
        if reason not in range(1, 9):
            raw_reason = row["BP1_23"].strip()
            excluded["RAZON_BLANCA" if not raw_reason else "RAZON_09" if reason == 9 else "RAZON_99" if reason == 99 else "RAZON_OTRA"] += 1
            continue
        if _weight(row["FAC_DEL"]) is None:
            excluded["FAC_DEL"] += 1
            continue
        n_u1 += 1
        key = _key(row, p["join_columns"])
        if key is None:
            excluded["LLAVE_EVENTO"] += 1
            continue
        events[key]["n"] += 1
        events[key]["c1"] = max(events[key]["c1"], int(reason in {1, 2, 6}))
        events[key]["c2"] = max(events[key]["c2"], int(reason in {1, 2, 6, 8}))

    persons_by_key = defaultdict(list)
    for row in person_rows:
        key = _key(row, p["join_columns"])
        if key is not None:
            persons_by_key[key].append(row)

    identity_collision = set()
    identity_field = p.get("identity_field")
    if identity_field:
        identity_keys = defaultdict(set)
        for key, rows in persons_by_key.items():
            for row in rows:
                identity = row[identity_field].strip()
                if identity:
                    identity_keys[identity].add(key)
        identity_collision = {key for keys in identity_keys.values() if len(keys) > 1 for key in keys}

    candidate_status = {}
    u4 = {}
    for key, event in events.items():
        rows = persons_by_key.get(key, [])
        if not rows:
            candidate_status[key] = "SIN_VINCULO"
            continue
        if len(rows) != 1:
            candidate_status[key] = "VINCULO_MULTI"
            continue
        row = rows[0]
        if identity_field and not row[identity_field].strip():
            candidate_status[key] = "ID_INVALIDA"
            continue
        if key in identity_collision:
            candidate_status[key] = "ID_COLISION"
            continue
        weight = _weight(row["FAC_ELE"])
        if weight is None:
            candidate_status[key] = "FAC_ELE"
            continue
        candidate_status[key] = "U4"
        u4[key] = {
            "weight": weight,
            "c1": event["c1"],
            "c2": event["c2"],
            "events": event["n"],
        }

    frame = []
    frame_keys = set()
    frame_duplicate = 0
    for key, rows in persons_by_key.items():
        if len(rows) != 1 or key in identity_collision:
            frame_duplicate += len(rows)
            continue
        row = rows[0]
        if identity_field and not row[identity_field].strip():
            continue
        weight = _weight(row["FAC_ELE"])
        stratum = row[p["stratum_field"]].strip()
        psu = row[p["psu_field"]].strip()
        if weight is None or not stratum or not psu:
            continue
        domain = int(key in u4)
        frame.append({
            "stratum": stratum,
            "psu": psu,
            "weight": weight,
            "domain": domain,
            "c1": u4.get(key, {}).get("c1", 0),
            "c2": u4.get(key, {}).get("c2", 0),
        })
        frame_keys.add(key)

    weights = np.asarray([v["weight"] for v in u4.values()], dtype=float)
    c1 = np.asarray([v["c1"] for v in u4.values()], dtype=float)
    c2 = np.asarray([v["c2"] for v in u4.values()], dtype=float)
    denominator = float(weights.sum()) if len(weights) else 0.0
    if denominator <= 0:
        raise RuntimeError("UNIVERSO-U4-VACIO")
    numerator_c1 = float(np.sum(weights * c1))
    numerator_c2 = float(np.sum(weights * c2))
    point_c1 = numerator_c1 / denominator
    point_c2 = numerator_c2 / denominator

    replicas = int(p["bootstrap_replicas"])
    seed = int(contrato["seed"]["valor"])
    lo2, hi2, n_strata, n_psu, n_singleton, valid2 = _bootstrap(frame, replicas, seed, "c2")
    lo1, hi1, _, _, _, valid1 = _bootstrap(frame, replicas, seed, "c1")
    method = (
        "SENSIBILIDAD-BOOTSTRAP-UPM-EN-ESTRATO-MARCO-PERSONAS-OBSERVADO;"
        "FUERA-U4-CERO;SINGLETON-FIJA;NO-APROBADA-INFERENCIA"
    )
    status_counts = Counter(candidate_status.values())
    out = {
        f"{prefix}-N-FILAS-MODULO": len(module_rows),
        f"{prefix}-N-FILAS-PERSONAS": len(person_rows),
        f"{prefix}-PERFIL-DBF-MODULO": module_profile,
        f"{prefix}-PERFIL-DBF-PERSONAS": person_profile,
        f"{prefix}-N-EXCL-BPCOD": excluded["BPCOD"],
        f"{prefix}-N-EXCL-NO-DENUNCIA": excluded["NO_DENUNCIA"],
        f"{prefix}-N-EXCL-RAZON-BLANCA": excluded["RAZON_BLANCA"],
        f"{prefix}-N-EXCL-RAZON-09": excluded["RAZON_09"],
        f"{prefix}-N-EXCL-RAZON-99": excluded["RAZON_99"],
        f"{prefix}-N-EXCL-RAZON-OTRA": excluded["RAZON_OTRA"],
        f"{prefix}-N-EXCL-FAC-DEL": excluded["FAC_DEL"],
        f"{prefix}-N-EVENTOS-U1": n_u1,
        f"{prefix}-N-EVENTOS-U1-LLAVE-INVALIDA": excluded["LLAVE_EVENTO"],
        f"{prefix}-N-PERSONAS-CANDIDATAS": len(events),
        f"{prefix}-N-PERSONAS-SIN-VINCULO": status_counts["SIN_VINCULO"],
        f"{prefix}-N-PERSONAS-VINCULO-MULTI": status_counts["VINCULO_MULTI"],
        f"{prefix}-N-PERSONAS-ID-INVALIDA": status_counts["ID_INVALIDA"],
        f"{prefix}-N-PERSONAS-ID-COLISION": status_counts["ID_COLISION"],
        f"{prefix}-N-PERSONAS-FAC-ELE-INVALIDO": status_counts["FAC_ELE"],
        f"{prefix}-N-PERSONAS-U4": len(u4),
        f"{prefix}-N-EVENTOS-EN-U4": sum(v["events"] for v in u4.values()),
        f"{prefix}-N-PERSONAS-U4-SIN-DISENO": len(set(u4) - frame_keys),
        f"{prefix}-COBERTURA-VINCULO": len(u4) / len(events) if events else None,
        f"{prefix}-MASA-FAC-ELE-U4": denominator,
        f"{prefix}-NUMERADOR-FAC-ELE-C2-U4": numerator_c2,
        f"{prefix}-NUMERADOR-FAC-ELE-C1-U4": numerator_c1,
        f"{prefix}-P-C2-U4": point_c2,
        f"{prefix}-Q-C2-U4": 1.0 - point_c2,
        f"{prefix}-P-C1-U4": point_c1,
        f"{prefix}-N-MARCO-PERSONAS-DISENO": len(frame),
        f"{prefix}-N-MARCO-FILAS-DESCARTADAS-AMBIGUAS": frame_duplicate,
        f"{prefix}-N-ESTRATOS": n_strata,
        f"{prefix}-N-UPM": n_psu,
        f"{prefix}-N-ESTRATOS-SINGLETON": n_singleton,
        f"{prefix}-N-REPLICAS-VALIDAS-C2": valid2,
        f"{prefix}-N-REPLICAS-VALIDAS-C1": valid1,
        f"{prefix}-IC95-SENS-LO-C2-U4": lo2,
        f"{prefix}-IC95-SENS-HI-C2-U4": hi2,
        f"{prefix}-IC95-SENS-LO-Q-C2-U4": None if hi2 is None else 1.0 - hi2,
        f"{prefix}-IC95-SENS-HI-Q-C2-U4": None if lo2 is None else 1.0 - lo2,
        f"{prefix}-IC95-SENS-LO-C1-U4": lo1,
        f"{prefix}-IC95-SENS-HI-C1-U4": hi1,
        f"{prefix}-METODO-IC": method,
        f"{prefix}-ESTADO-PRECISION": "SENSIBILIDAD-NO-APROBADA-INFERENCIA",
        f"{prefix}-ESTADO": "CALCULADO-PUNTO-DESCRIPTIVO",
    }
    return out
