#!/usr/bin/env python3
"""Pruebas focales de la derivación ENCRIGE carga/intensidad."""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/encrige_carga_intensidad.py"
spec = importlib.util.spec_from_file_location("encrige_carga_intensidad", SCRIPT)
M = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = M
spec.loader.exec_module(M)


def _row(indicator: str, *, domain: str = "Micro", N: str = "100", numerator: str = "10") -> dict[str, str]:
    prevalence = indicator == M.PREVALENCE_ID
    return {
        "indicador_id": indicator,
        "dominio_tipo": "tamaño oficial",
        "dominio": domain,
        "valor_original": str(M.Decimal(numerator) / M.Decimal(N) * M.Decimal(10000)),
        "valor_normalizado": str(M.Decimal(numerator) / M.Decimal(N)),
        "unidad_normalizada": (
            "proporción de unidades económicas expuestas" if prevalence
            else "experiencias por unidad económica expuesta"
        ),
        "numerador_publicado": numerator,
        "denominador_publicado": N,
        "unidad_numerador_denominador": "unidades expandidas",
        "periodo": "Durante 2020 (enero a la fecha de entrevista)",
        "cuadro": "t6_33" if prevalence else "t6_41",
        "localizador": (
            "Participación absoluta" if prevalence
            else "Total de trámites con experiencia de corrupción"
        ),
    }


def _reject(prevalence: dict[str, str], incidence: dict[str, str]) -> str:
    try:
        M.derive_domain(prevalence, incidence)
    except ValueError as exc:
        return str(exc)
    raise AssertionError("el caso inválido no fue rechazado")


def test_a_cero_deja_intensidad_no_estimable():
    result = M.derive_domain(
        _row(M.PREVALENCE_ID, numerator="0"),
        _row(M.INCIDENCE_ID, numerator="0"),
    )
    assert result.r is None
    assert result.p == 0 and result.m == 0


def test_denominadores_incompatibles_se_rechazan():
    message = _reject(
        _row(M.PREVALENCE_ID, N="100", numerator="10"),
        _row(M.INCIDENCE_ID, N="101", numerator="20"),
    )
    assert "INDICADORES-INCOMPATIBLES:denominador_publicado" in message


def test_razon_mayor_que_uno_es_valida():
    result = M.derive_domain(
        _row(M.PREVALENCE_ID, numerator="10"),
        _row(M.INCIDENCE_ID, numerator="25"),
    )
    assert result.r == M.Decimal("2.5")
    assert result.m == result.p * result.r


def test_t_menor_que_a_activa_guarda_semantica():
    message = _reject(
        _row(M.PREVALENCE_ID, numerator="10"),
        _row(M.INCIDENCE_ID, numerator="9"),
    )
    assert "GUARDA-SEMANTICA-T-MENOR-A" in message


def test_resultado_real_reproduce_artefactos_sin_mutar_padre():
    parent = M.PARENT_CSV
    before = hashlib.sha256(parent.read_bytes()).hexdigest()
    derived, artifacts = M.build_artifacts(parent.read_bytes())
    assert len(derived["domains"]) == 5
    assert len(derived["shares"]) == 4
    assert len(derived["contrasts"]) == 3
    assert set(artifacts) == {
        "tabla-ampliada.csv",
        "participaciones-por-tamano.csv",
        "contrastes-vs-micro.csv",
        "controles.json",
        "participaciones-por-tamano.svg",
    }
    assert max(abs(v) for v in derived["residuals"].values()) <= M.MASS_TOLERANCE
    after = hashlib.sha256(parent.read_bytes()).hexdigest()
    assert before == after == M.EXPECTED_PARENT_SHA256


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    failures = []
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures.append(f"{test.__name__}: {type(exc).__name__}: {exc}")
    print(f"{Path(__file__).name} · {len(tests)} casos · {len(tests)-len(failures)} ok · {len(failures)} FALLOS")
    for failure in failures:
        print("  FAIL", failure)
    raise SystemExit(1 if failures else 0)
