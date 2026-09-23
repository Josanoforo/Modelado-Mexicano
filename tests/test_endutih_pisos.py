"""Guardias materiales de ASTRA5 U4 sobre datos sintéticos."""
from tools.dominios.endutih.pisos import _calculate, _merge, _status


def _row(i: int) -> dict[str, str]:
    return {
        "UPM": str(i // 10), "VIV_SEL": str(i), "HOGAR": "1", "NUM_REN": "1",
        "EDAD": "20", "SEXO": "1", "NIVEL": "08", "TLOC": "1", "ENT": "01",
        "FAC_PER": "1", "EST_DIS": str((i // 10) % 2), "UPM_DIS": str(i // 10),
        "P7_1": "1", "P7_2": "", "P7_10_2": "2", "P7_12_3": "1",
        "P7_35_4": "2", "P8_1": "1", "P8_2": "",
    }


def test_saltos_y_blancos_no_son_ceros():
    row = _row(0)
    assert _status(row, "no_internet_costo") == "SALTO"
    row["P7_1"] = "2"
    assert _status(row, "actividad_mensajes") == "SALTO"
    assert _status(row, "no_internet_costo") == "NR"
    row["P7_2"] = "4"
    assert _status(row, "no_internet_costo") == "SI"
    assert _status(row, "no_internet_preferencia") == "NO"


def test_llave_duplicada_impide_join():
    first = [_row(0), _row(1)]
    second = [{k: first[0][k] for k in ("UPM", "VIV_SEL", "HOGAR", "NUM_REN")}] * 2
    try:
        _merge(first, second)
    except ValueError as exc:
        assert "duplicada" in str(exc)
    else:
        raise AssertionError("join ambiguo aceptado")


def test_sintetico_ejercita_estimable_y_no_estimable():
    rows = [_row(i) for i in range(200)]
    rows[0]["P7_1"] = "2"
    rows[0]["P7_2"] = "4"
    result = _calculate(rows, "ENT")
    cells = {(x["medida"], x["dominio"]): x for x in result["celdas"]}
    assert cells["internet", "TOTAL"]["estado"] == "ESTIMABLE"
    assert cells["internet", "TOTAL"]["punto"] == 199 / 200
    assert cells["actividad_mensajes", "TOTAL"]["estados"]["SALTO"] == 1
    assert cells["no_internet_costo", "TOTAL"]["estado"] == "SUPRIMIDA-N-MENOR-100"
