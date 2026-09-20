"""Pruebas sintéticas baratas del contrato ENCUCI exposición/respuesta."""
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "data/corrida0/CALC-ENCUCI2020-RESPUESTA-POR-CONTACTO-0001-v1_1/medidor.py"
SPEC = importlib.util.spec_from_file_location("medidor_encuci_er", SCRIPT)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def row(contact, request="2", delivery="2", domain="U", ident="1"):
    out = {f"AP5_16_{i}": str(contact[i - 1]) if contact[i - 1] is not None else ""
           for i in range(1, 11)}
    out.update({"AP5_17": request, "AP5_18": delivery, "DOMINIO": domain,
                "FAC_SEL": "1", "EST_DIS": "001", "UPM_DIS": ident,
                "ID_PER": ident})
    return out


def test_unknown_vector_and_multiple_authorities():
    assert M.classify_contacts([2] * 9 + [None]) == (None, None)
    assert M.classify_contacts([1, 1] + [2] * 8) == (1, 2)
    assert M.classify_contacts([1, None] + [2] * 8) == (1, None)


def test_partitions_and_empty_conditional_denominator():
    rows = [
        row([1] + [2] * 9, "2", "2", ident="1"),
        row([1] + [2] * 9, "1", "2", ident="2"),
        row([1, 1] + [2] * 8, "2", "1", ident="3"),
        row([1, 1, 1] + [2] * 7, "1", "1", domain="R", ident="4"),
        row([2] * 9 + [None], "", "", ident="5"),
    ]
    result = M.measure_rows(rows, replicas=20, seed=7)
    validations = json.loads(result["RESULT-ENCUCI2020-RPCV11-VALIDACIONES-POR-CONTACTO"])
    assert len(validations) == 10
    assert all(abs(x["particion_cuatro_celdas_menos_uno"]) < 1e-12 for x in validations[:3])
    assert all(abs(x["union_menos_solicitud_mas_entrega_menos_ambas"]) < 1e-12 for x in validations[:3])
    profile = {x["variable"]: x for x in json.loads(
        result["RESULT-ENCUCI2020-RPCV11-PERFIL-POR-CONTACTO"])}
    assert profile["AP5_16_10"]["p_entrega_dado_solicitud"]["p"] is None
    assert profile["AP5_16_1"]["distribucion"]["ambas"]["p"] == 0.25
    overlap = json.loads(result["RESULT-ENCUCI2020-RPCV11-SOLAPAMIENTO-OTROS-CONTACTOS"])
    assert overlap[0]["distribucion_numero_otros_tipos"]["0"]["p"] == 0.5


if __name__ == "__main__":
    test_unknown_vector_and_multiple_authorities()
    test_partitions_and_empty_conditional_denominator()
    print("OK: test_medidor.py")
