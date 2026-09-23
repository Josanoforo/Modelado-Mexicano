"""Pruebas sintéticas del contrato MOCIBA temprano."""
from tools.dominios.mociba.pisos import _measure, _response, _victim


def _row(i: int) -> dict[str, str]:
    row = {"EDAD": "25", "SEXO": "1", "NIVEL": "08", "FAC_MOCIBA": "1",
           "UPM": str(i // 10)}
    row.update({f"P3_{j}": "2" for j in range(1, 11)})
    row.update({f"P7_{j}_{k}": "" for j in range(1, 11) for k in (1, 5)})
    return row


def test_salto_y_blanco_no_equivalen_a_no():
    row = _row(0)
    assert _victim(row, "2015") == "NO"
    assert _response(row, "2015", "denuncia") == "SALTO"
    row["P3_1"] = "1"
    assert _response(row, "2015", "denuncia") == "NR"
    row["P7_1_5"] = "1"
    row["P7_1_1"] = "1"
    assert _response(row, "2015", "denuncia") == "SI"
    assert _response(row, "2015", "bloqueo") == "SI"


def test_no_estimable_por_diseno_2015():
    rows = [_row(i) for i in range(120)]
    for row in rows[:60]:
        row["P3_1"] = "1"
        row["P7_1_1"] = "2"
        row["P7_1_5"] = "2"
    result = _measure(rows, "2015")
    total = next(c for c in result["celdas"] if c["medida"] == "ciberacoso"
                 and c["dominio"] == "TOTAL")
    assert total["estado"] == "NO-ESTIMABLE-SIN-EST_DIS"
    assert "punto" not in total
    assert total["n"] == 120
