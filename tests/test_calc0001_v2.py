#!/usr/bin/env python3
"""Prueba dirigida de identidades del estimando de CALC-0001-v2."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("calc0001v2", ROOT / "data/corrida0/CALC-0001-v2/medidor.py")
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def main():
    oferente = np.array([1, 2, 5, 97, np.nan])
    voto = np.array([1, 29, 2, 1, 1])
    y = M._alineado(oferente, voto, {1: 1, 2: 2, 5: 9}, {29: {2, 9}})
    assert y[:3].tolist() == [1.0, 1.0, 0.0]
    assert np.isnan(y[3:]).all()
    w = np.array([1.0, 2.0, 1.0])
    p = M._prop(y[:3], w)
    assert p == 0.75
    assert 2 * p - 1 == 0.5
    print("OK test_calc0001_v2")


if __name__ == "__main__":
    main()
