#!/usr/bin/env python3
"""Pruebas unitarias del extractor GEN2 20, sin red ni corpus."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

import extrae_fuentes_financieras as F  # noqa: E402


def prueba_periodo_y_unidad_imor() -> None:
    assert F.periodo_cnbv(202112.0) == "2021-12"
    assert F.periodo_inventario("clausulas_3trimestre_2025.csv", [], []) == "corte_en_nombre:2025T3"
    filas = [{
        "fecha": "2021-12",
        "producto_universo": "Tarjeta de Crédito",
        "valor": "3.5",
        "unidad": "porcentaje",
        "notas": "valor observado",
    }, {
        "fecha": "2021-12",
        "producto_universo": "Arrendamiento",
        "valor": "",
        "unidad": "porcentaje",
        "notas": "faltante en el original; no es cero",
    }]
    F.valida_filas_imor(filas)
    try:
        F.valida_filas_imor([dict(filas[0]), dict(filas[0])])
    except ValueError as exc:
        assert "duplicada" in str(exc)
    else:
        raise AssertionError("debió rechazar periodo/producto duplicado")


def prueba_registro_separa_fuentes_con_origen_compartido() -> None:
    filas = [{
        "fila_origen": "mismo-encargo.md",
        "fuente_canonica": "CNBV_PORTAFOLIO_INFORMACION_IMOR_CONSUMO",
    }, {
        "fila_origen": "mismo-encargo.md",
        "fuente_canonica": "ENCRIGE_2020_FD_COMPLETO_MAS_CONDUSEF",
    }]
    indice = F.filas_por_fuente_adquisicion(filas)
    assert len(indice) == 2
    try:
        F.filas_por_fuente_adquisicion([filas[0], dict(filas[0])])
    except ValueError as exc:
        assert "duplicada" in str(exc)
    else:
        raise AssertionError("debió rechazar fuente canónica duplicada")


def prueba_conteos_no_admiten_fracciones() -> None:
    assert F.entero_conteo("7.0") == 7
    for invalido in ("1.5", "-1", "texto"):
        try:
            F.entero_conteo(invalido)
        except ValueError:
            pass
        else:
            raise AssertionError(f"debió rechazar {invalido!r}")


def prueba_porcentaje_conserva_denominador() -> None:
    assert F.porcentaje(Decimal("1"), Decimal("4")) == "25"
    assert F.porcentaje(1, 0) == ""
    # La función recibe el denominador: no fabrica prevalencia a partir de un
    # conteo aislado ni rellena un cero cuando éste falta.


def prueba_encrige_contrasta_porcentaje_publicado() -> None:
    fila = F.registro_encrige(
        "tabla_fixture", "reactivo_fixture", "universo_fixture",
        "indicador_fixture", "4", "1", "25", "nota_fixture",
    )
    assert fila["porcentaje_publicado"] == "25"
    try:
        F.registro_encrige(
            "tabla_fixture", "reactivo_fixture", "universo_fixture",
            "indicador_fixture", "4", "1", "24", "nota_fixture",
        )
    except ValueError as exc:
        assert "inconsistente" in str(exc)
    else:
        raise AssertionError("debió rechazar el porcentaje discordante")


def main() -> int:
    pruebas = [
        prueba_periodo_y_unidad_imor,
        prueba_registro_separa_fuentes_con_origen_compartido,
        prueba_conteos_no_admiten_fracciones,
        prueba_porcentaje_conserva_denominador,
        prueba_encrige_contrasta_porcentaje_publicado,
    ]
    for prueba in pruebas:
        prueba()
        print(f"OK {prueba.__name__}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
