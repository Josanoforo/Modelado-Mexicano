#!/usr/bin/env python3
"""Pruebas focales del medidor U4 histórico en unidad persona."""
from __future__ import annotations

import datetime as dt
import importlib.util
from pathlib import Path
import struct
import sys
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "forense/analisis/envipe-u4-2013-2015-1/medidor.py"
loaded = importlib.util.spec_from_file_location("medidor_envipe_u4_historico", SCRIPT)
M = importlib.util.module_from_spec(loaded)
sys.modules[loaded.name] = M
loaded.loader.exec_module(M)


def _dbf(fields, rows):
    header_length = 32 + 32 * len(fields) + 1
    record_length = 1 + sum(width for _, width in fields)
    today = dt.date(2026, 9, 16)
    header = bytearray(32)
    header[0] = 0x03
    header[1:4] = bytes((today.year - 1900, today.month, today.day))
    header[4:12] = struct.pack("<IHH", len(rows), header_length, record_length)
    descriptors = bytearray()
    for name, width in fields:
        desc = bytearray(32)
        encoded = name.encode("ascii")
        desc[:len(encoded)] = encoded
        desc[11] = ord("C")
        desc[16] = width
        descriptors += desc
    body = bytearray()
    for row in rows:
        record = bytearray(b" ")
        for name, width in fields:
            value = str(row.get(name, "")).encode("latin-1")[:width]
            record += value.ljust(width, b" ")
        body += record
    return bytes(header + descriptors + b"\r" + body + b"\x1a")


def _contract(year):
    path = ROOT / f"data/corrida0/CALC-ENVIPE-U4-{year}-0001/spec.yaml"
    spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    return {k: spec[k] for k in ("variables", "universo", "filtros", "ponderador", "transformacion", "estimando", "parametros", "seed")}


def _run(tmp_path, year, module_rows, person_rows, *, person_fields=None):
    contract = _contract(year)
    p = contract["parametros"]
    module_fields = [(name, width) for name, width in (
        ("CONTROL", 6), ("UPM", 7), ("VIV_SEL", 2), ("HOGAR", 2), ("R_SEL", 2),
        ("BPCOD", 2), ("BP1_20", 1), ("BP1_23", 2), ("FAC_DEL", 6),
    ) if name in set(p["join_columns"]) | {"BPCOD", "BP1_20", "BP1_23", "FAC_DEL"}]
    if person_fields is None:
        person_fields = [(name, width) for name, width in (
            ("CONTROL", 6), ("ID_PER", 16), ("UPM", 7), ("VIV_SEL", 2), ("HOGAR", 2),
            ("R_SEL", 2), ("FAC_ELE", 6), ("EST", 3), ("UPM_DIS", 5), ("EST_DIS", 3),
        ) if name in set(p["join_columns"]) | {p.get("identity_field"), "FAC_ELE", p["stratum_field"], p["psu_field"]}]
    archive = tmp_path / f"wave-{year}.zip"
    with zipfile.ZipFile(archive, "w") as zf:
        zf.writestr(p["module_member"], _dbf(module_fields, module_rows))
        zf.writestr(p["person_member"], _dbf(person_fields, person_rows))
    inputs = {p["payload_id"]: {"ruta_absoluta": str(archive)}}
    return M.medir(inputs, contract)


def _row13(control, hogar, rsel, **extra):
    row = {"CONTROL": control, "VIV_SEL": "01", "HOGAR": hogar, "R_SEL": rsel}
    row.update(extra)
    return row


def test_persona_cuenta_una_vez_y_fac_ele_no_fac_del(tmp_path):
    persons = [
        _row13("000001", "01", "01", FAC_ELE="10", EST="001", UPM="00001"),
        _row13("000001", "01", "02", FAC_ELE="30", EST="001", UPM="00002"),
        _row13("000002", "01", "01", FAC_ELE="20", EST="001", UPM="00001"),
    ]
    events = [
        _row13("000001", "01", "01", BPCOD="05", BP1_20="2", BP1_23="01", FAC_DEL="999"),
        _row13("000001", "01", "01", BPCOD="06", BP1_20="2", BP1_23="03", FAC_DEL="1"),
        _row13("000001", "01", "02", BPCOD="05", BP1_20="2", BP1_23="03", FAC_DEL="100"),
        _row13("000002", "01", "01", BPCOD="05", BP1_20="2", BP1_23="09", FAC_DEL="100"),
    ]
    out = _run(tmp_path, 2013, events, persons)
    p = "RESULT-ENVIPE-U4-2013-"
    assert out[p + "N-PERSONAS-U4"] == 2
    assert out[p + "N-EVENTOS-U1"] == 3
    assert out[p + "N-EXCL-RAZON-09"] == 1
    assert out[p + "MASA-FAC-ELE-U4"] == 40.0
    assert out[p + "P-C2-U4"] == 0.25
    assert out[p + "P-C1-U4"] == 0.25
    assert out[p + "Q-C2-U4"] == 0.75
    assert out[p + "IC95-SENS-LO-Q-C2-U4"] == 1 - out[p + "IC95-SENS-HI-C2-U4"]
    assert out[p + "IC95-SENS-HI-Q-C2-U4"] == 1 - out[p + "IC95-SENS-LO-C2-U4"]


def test_vinculo_multiple_se_detecta(tmp_path):
    person = _row13("000001", "01", "01", FAC_ELE="10", EST="001", UPM="00001")
    event = _row13("000001", "01", "01", BPCOD="05", BP1_20="2", BP1_23="01", FAC_DEL="1")
    try:
        _run(tmp_path, 2013, [event], [person, dict(person)])
    except RuntimeError as exc:
        assert "UNIVERSO-U4-VACIO" in str(exc)
    else:
        raise AssertionError("un vínculo múltiple no detuvo el universo vacío")


def test_2015_usa_upm_dis_para_diseno_y_detecta_id_colision(tmp_path):
    def row(hogar, rsel, **extra):
        base = {"UPM": "1000001", "VIV_SEL": "01", "HOGAR": hogar, "R_SEL": rsel}
        base.update(extra)
        return base
    persons = [
        row("01", "01", ID_PER="A", FAC_ELE="10", EST_DIS="001", UPM_DIS="00001"),
        row("01", "02", ID_PER="B", FAC_ELE="30", EST_DIS="001", UPM_DIS="00002"),
        row("02", "01", ID_PER="C", FAC_ELE="20", EST_DIS="001", UPM_DIS="00001"),
    ]
    events = [
        row("01", "01", BPCOD="05", BP1_20="2", BP1_23="01", FAC_DEL="1"),
        row("01", "02", BPCOD="05", BP1_20="2", BP1_23="03", FAC_DEL="1"),
    ]
    out = _run(tmp_path, 2015, events, persons)
    p = "RESULT-ENVIPE-U4-2015-"
    assert out[p + "N-UPM"] == 2
    assert out[p + "P-C2-U4"] == 0.25

    persons[1]["ID_PER"] = "A"
    try:
        _run(tmp_path, 2015, events, persons)
    except RuntimeError as exc:
        assert "UNIVERSO-U4-VACIO" in str(exc)
    else:
        raise AssertionError("una colisión de ID_PER no detuvo el universo vacío")


def test_estrato_generico_no_sustituye_diseno(tmp_path):
    person_fields = [
        ("ID_PER", 16), ("UPM", 7), ("VIV_SEL", 2), ("HOGAR", 2), ("R_SEL", 2),
        ("FAC_ELE", 6), ("ESTRATO", 1), ("EST_DIS", 3),
    ]
    person = {"ID_PER": "A", "UPM": "1000001", "VIV_SEL": "01", "HOGAR": "01", "R_SEL": "01", "FAC_ELE": "10", "ESTRATO": "1", "EST_DIS": "001"}
    event = {"UPM": "1000001", "VIV_SEL": "01", "HOGAR": "01", "R_SEL": "01", "BPCOD": "05", "BP1_20": "2", "BP1_23": "01", "FAC_DEL": "1"}
    try:
        _run(tmp_path, 2015, [event], [person], person_fields=person_fields)
    except RuntimeError as exc:
        assert "COLUMNAS-AUSENTES:UPM_DIS" in str(exc)
    else:
        raise AssertionError("ESTRATO/UPM sustituyeron indebidamente el diseño")


if __name__ == "__main__":
    import tempfile
    failures = []
    for name, test in sorted((n, f) for n, f in globals().items() if n.startswith("test_")):
        try:
            with tempfile.TemporaryDirectory() as directory:
                test(Path(directory))
        except Exception as exc:
            failures.append(f"{name}: {type(exc).__name__}: {exc}")
    print(f"{Path(__file__).name}: {4-len(failures)}/4 ok")
    for failure in failures:
        print("FAIL", failure)
    raise SystemExit(bool(failures))
