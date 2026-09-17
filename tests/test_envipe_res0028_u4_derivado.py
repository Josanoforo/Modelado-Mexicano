#!/usr/bin/env python3
"""Pruebas focales del complemento U4 para RES-0028."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "data/corrida0/CALC-ENVIPE-RES0028-U4-DERIVADO-0001"
PADRE = ROOT / "data/corrida0/CALC-ENVIPE-0001"
modspec = importlib.util.spec_from_file_location("res0028_u4_derivado", CALC / "medidor.py")
M = importlib.util.module_from_spec(modspec)
sys.modules[modspec.name] = M
modspec.loader.exec_module(M)


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _contrato() -> dict:
    return yaml.safe_load((CALC / "spec.yaml").read_text(encoding="utf-8"))


def _inputs(resultados: dict | None = None) -> dict:
    resultados_b = (
        (PADRE / "resultados.json").read_bytes()
        if resultados is None
        else (json.dumps(resultados, sort_keys=True) + "\n").encode()
    )
    spec_b = (PADRE / "spec.yaml").read_bytes()
    sello = {
        "ejecucion.json": "fixture-no-usado",
        "medidor.py": "fixture-no-usado",
        "resultados.json": _sha(resultados_b),
        "spec.yaml": _sha(spec_b),
    }
    sello_b = (json.dumps(sello, sort_keys=True) + "\n").encode()
    sidecar_b = f"{_sha(sello_b)}  sello.json\n".encode()
    return {
        M.IN_RESULTADOS: {"bytes": resultados_b},
        M.IN_SPEC: {"bytes": spec_b},
        M.IN_SELLO: {"bytes": sello_b},
        M.IN_SELLO_SHA: {"bytes": sidecar_b},
    }


def _doc_sintetico(*, p=0.30, lo=0.20, hi=0.40) -> dict:
    return {
        "spec_id": "CALC-ENVIPE-0001",
        "resultados": {
            "RESULT-ENVIPE-DEN-P-C2-U4": p,
            "RESULT-ENVIPE-DEN-IC-LO-C2-U4": lo,
            "RESULT-ENVIPE-DEN-IC-HI-C2-U4": hi,
            "RESULT-ENVIPE-DEN-N-PERSONAS-U4": 100,
            "RESULT-ENVIPE-DEN-MASA-FAC-ELE-U4": 1234.0,
            "RESULT-ENVIPE-DEN-METODO-IC": "IC-CON-ESTRATOS-DE-UPM-UNICA",
            "RESULT-ENVIPE-DEN-VEREDICTO": "TASA-REPORTADA",
        },
    }


def _rechaza(doc: dict, contrato: dict | None = None) -> str:
    try:
        M.medir(_inputs(doc), contrato or _contrato())
    except RuntimeError as exc:
        return str(exc)
    raise AssertionError("el padre invalido no fue rechazado")


def test_complemento_suma_uno_e_invierte_extremos():
    out = M.medir(_inputs(_doc_sintetico()), _contrato())
    assert out["RESULT-ENVIPE-RES0028-Q-C2-U4"] == 0.70
    assert out["RESULT-ENVIPE-RES0028-SUMA-P-Q-C2-U4"] == 1.0
    assert out["RESULT-ENVIPE-RES0028-IC-LO-Q-C2-U4"] == 0.60
    assert out["RESULT-ENVIPE-RES0028-IC-HI-Q-C2-U4"] == 0.80


def test_rechaza_limites_invertidos_o_fuera_de_escala():
    assert "LIMITES-INVERTIDOS" in _rechaza(_doc_sintetico(lo=0.4, hi=0.2))
    assert "FUERA-DE-ESCALA" in _rechaza(_doc_sintetico(lo=-0.1, hi=0.4))


def test_rechaza_padre_no_estimable_sin_convertirlo_en_cero():
    doc = _doc_sintetico(p=None)
    assert "NO-NUMERICO" in _rechaza(doc)
    doc = _doc_sintetico()
    doc["resultados"]["RESULT-ENVIPE-DEN-VEREDICTO"] = "NO-ESTIMABLE-UNIVERSO-VACIO"
    assert "VEREDICTO" in _rechaza(doc)


def test_rechaza_unidad_erronea_y_referencia_u1():
    contrato = _contrato()
    contrato["parametros"]["padre"]["unidad"] = "delito"
    assert "UNIDAD-O-POBLACION" in _rechaza(_doc_sintetico(), contrato)
    contrato = _contrato()
    contrato["parametros"]["padre"]["p_id"] = "RESULT-ENVIPE-DEN-P-C2-U1"
    assert "REFERENCIA-U1" in _rechaza(_doc_sintetico(), contrato)


def test_resultado_real_contra_claves_publicadas_y_padre_inmutable():
    rutas = [PADRE / n for n in ("spec.yaml", "resultados.json", "sello.json", "sello.sha256")]
    antes = {p: _sha(p.read_bytes()) for p in rutas}
    entradas = {
        M.IN_RESULTADOS: {"bytes": (PADRE / "resultados.json").read_bytes()},
        M.IN_SPEC: {"bytes": (PADRE / "spec.yaml").read_bytes()},
        M.IN_SELLO: {"bytes": (PADRE / "sello.json").read_bytes()},
        M.IN_SELLO_SHA: {"bytes": (PADRE / "sello.sha256").read_bytes()},
    }
    out = M.medir(entradas, _contrato())
    assert out["RESULT-ENVIPE-RES0028-P-PADRE-C2-U4"] == 0.29431298745731216
    assert out["RESULT-ENVIPE-RES0028-Q-C2-U4"] == 0.7056870125426878
    assert out["RESULT-ENVIPE-RES0028-IC-LO-Q-C2-U4"] == 0.6942008049952509
    assert out["RESULT-ENVIPE-RES0028-IC-HI-Q-C2-U4"] == 0.7169802491746927
    assert out["RESULT-ENVIPE-RES0028-COMPATIBILIDAD-RES0028"] == "COINCIDE-AL-GRANO-U4"
    despues = {p: _sha(p.read_bytes()) for p in rutas}
    assert despues == antes


if __name__ == "__main__":
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    fallos = []
    for prueba in pruebas:
        try:
            prueba()
        except Exception as exc:
            fallos.append(f"{prueba.__name__}: {type(exc).__name__}: {exc}")
    print(f"{Path(__file__).name} · {len(pruebas)} casos · {len(pruebas)-len(fallos)} ok · {len(fallos)} FALLOS")
    for fallo in fallos:
        print("  FAIL", fallo)
    raise SystemExit(1 if fallos else 0)
