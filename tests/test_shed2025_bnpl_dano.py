#!/usr/bin/env python3
"""Falsadores dirigidos del medidor SHED 2025."""
from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data/corrida0/CALC-SHED2025-BNPL-DANO-0001/medidor.py"
SPEC = importlib.util.spec_from_file_location("shed_bnpl_medidor_test", PATH)
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def row(i, *, bank="Yes", overdraft="Yes", use="Yes", late="No", fee="", nsf="No", afford="No", weight=1):
    return {
        "shedid": str(i), "weight": str(weight), "weight_pop": str(weight * 100),
        "BK1": bank, "BK2_f": overdraft, "BNPL1": use, "BNPL3": late,
        "BNPL3A": fee, "BNPL1A": nsf, "BNPL4_e": afford,
    }


def test_nsf_denominator_is_route_not_all_users():
    rows = [
        row(1, overdraft="Yes", nsf="Yes", late="Yes", fee="No", weight=2),
        row(2, overdraft="Yes", nsf="No", weight=1),
        row(3, overdraft="No", nsf="", afford="Yes", weight=7),
    ]
    out = M.calculate(rows, width=10, expected_rows=3)
    assert out["RESULT-SHED-BNPL-SOBREGIRO-N-VALIDO"] == 2
    assert out["RESULT-SHED-BNPL-SOBREGIRO-PUNTO"] == round(2 / 3, 12)
    assert out["RESULT-SHED-BNPL-ATRASO-N-VALIDO"] == 3


def test_numeric_code_is_rejected_in_labeled_csv():
    rows = [row(1)]
    rows[0]["BNPL1"] = "1"
    try:
        M.calculate(rows, width=10, expected_rows=1)
    except ValueError as exc:
        assert "CODIFICACION-NO-TEXTUAL:BNPL1" in str(exc)
    else:
        raise AssertionError("un código numérico se aceptó como etiqueta CSV")


def test_refused_bnpl3_route_never_enters_fee_rate():
    rows = [
        row(1, late="Yes", fee="No", nsf="No"),
        row(2, late="Refused", fee="Yes", nsf="No", afford="Yes"),
        row(3, late="No", fee="", nsf="No", afford="Yes"),
    ]
    out = M.calculate(rows, width=10, expected_rows=3)
    assert out["RESULT-SHED-BNPL-CARGO-N-VALIDO"] == 1
    assert out["RESULT-SHED-BNPL-CARGO-PUNTO"] == 0
    assert out["RESULT-SHED-BNPL-CARGO-RUTA-RECHAZO-N-VALIDO"] == 1
    assert out["RESULT-SHED-BNPL-CARGO-RUTA-RECHAZO-N-POSITIVOS"] == 1


if __name__ == "__main__":
    test_nsf_denominator_is_route_not_all_users()
    test_numeric_code_is_rejected_in_labeled_csv()
    test_refused_bnpl3_route_never_enters_fee_rate()
    print("OK test_shed2025_bnpl_dano: 3 falsadores")
