import io
import json
import struct
import zipfile
from pathlib import Path

import pytest
import yaml

from tools.enco_reserva_prepara import (
    ESTADO,
    inspect_zip,
    parse_dbf_header,
    preflight,
    synthetic_summary,
    to_percentage_points,
)


def _dbf_bytes(fields=(("P10", "C", 1, 0), ("FACTOR", "N", 8, 2))):
    header_length = 32 + 32 * len(fields) + 1
    record_length = 1 + sum(field[2] for field in fields)
    prefix = bytearray(32)
    prefix[0] = 3
    prefix[4:8] = struct.pack("<I", 1)
    prefix[8:10] = struct.pack("<H", header_length)
    prefix[10:12] = struct.pack("<H", record_length)
    descriptors = bytearray()
    for name, kind, length, decimals in fields:
        descriptor = bytearray(32)
        encoded = name.encode("ascii")
        descriptor[:len(encoded)] = encoded
        descriptor[11] = ord(kind)
        descriptor[16] = length
        descriptor[17] = decimals
        descriptors.extend(descriptor)
    return bytes(prefix + descriptors + b"\r" + b" SECRET-ROW-MUST-NOT-BE-READ")


class HeaderBoundary(io.BytesIO):
    def __init__(self, payload, header_length):
        super().__init__(payload)
        self.header_length = header_length

    def read(self, size=-1):
        if size < 0 or self.tell() + size > self.header_length:
            raise AssertionError("intento_de_lectura_de_respuesta")
        return super().read(size)


def test_parse_dbf_header_never_crosses_into_rows():
    payload = _dbf_bytes()
    header_length = int.from_bytes(payload[8:10], "little")
    fields = parse_dbf_header(
        HeaderBoundary(payload, header_length), member_size=len(payload)
    )
    assert [field["nombre"] for field in fields] == ["P10", "FACTOR"]


def test_inspect_zip_reports_structure_without_records(tmp_path):
    archive = tmp_path / "wave.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("encocb_0000.DBF", _dbf_bytes())
    result = inspect_zip(archive)
    assert result["respondentes_leidos"] is False
    assert result["registros_leidos"] == 0
    assert result["miembros"][0]["campos"][0]["nombre"] == "P10"


def test_special_codes_and_no_income_denominator():
    rows = [
        {"elegible": True, "p10": "1", "peso": 2.5},
        {"elegible": True, "p10": "2", "peso": 1.75},
        {"elegible": True, "p10": "4", "peso": 0.8},
        {"elegible": True, "p10": "3", "peso": 3.3},
        {"elegible": True, "p10": None, "peso": 1.1},
    ]
    result = synthetic_summary(rows)
    assert result["peso_denominador"] == pytest.approx(5.05)
    assert result["proporcion"] == pytest.approx(2.5 / 5.05)
    assert result["no_sabe_filas"] == 1
    assert result["faltante_filas"] == 1
    assert result["codigo_4_en_denominador"] is True


def test_empty_denominator_is_rejected():
    with pytest.raises(ValueError, match="denominador_sustantivo_vacio"):
        synthetic_summary([
            {"elegible": True, "p10": "3", "peso": 1},
            {"elegible": True, "p10": None, "peso": 1},
        ])


@pytest.mark.parametrize("weight", [0, -1, float("nan"), float("inf"), "x"])
def test_invalid_weights_are_rejected(weight):
    with pytest.raises(ValueError, match="peso_invalido"):
        synthetic_summary([{"elegible": True, "p10": "1", "peso": weight}])


def test_scale_conversion_and_bounds():
    assert to_percentage_points(0.125, "proporcion_0_1") == 12.5
    assert to_percentage_points(12.5, "porcentaje_0_100") == 12.5
    with pytest.raises(ValueError, match="proporcion_fuera_de_escala"):
        to_percentage_points(12.5, "proporcion_0_1")
    with pytest.raises(ValueError, match="escala_desconocida"):
        to_percentage_points(0.5, "fraccion")


def test_repository_cards_remain_non_authorizing():
    cards_path = Path("forense/produccion/enco-dos-olas-reservadas-1/04-tarjetas.yaml")
    cards = yaml.safe_load(cards_path.read_text(encoding="utf-8"))
    result = preflight(cards)
    assert result["estado"] == ESTADO
    assert result["respuestas_abiertas"] is False
    assert result["emisiones_autorizadas"] is False
    assert result["elegibilidad_experimental"] is False


def test_fixture_is_explicitly_synthetic():
    fixture = json.loads(Path(
        "forense/produccion/enco-dos-olas-reservadas-1/fixtures/"
        "SINTETICO-NO-MEDICION.json"
    ).read_text(encoding="utf-8"))
    assert fixture["naturaleza"] == "SINTETICO-NO-MEDICION"
    assert synthetic_summary(fixture["filas"])["naturaleza"] == fixture["naturaleza"]
