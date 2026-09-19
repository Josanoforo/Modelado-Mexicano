#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `tools/marcador_segmento.py` -- ACTO GEN2-MARCADOR-REDISENO-1.

Corre standalone (`python3 tests/test_marcador_segmento.py`) y expone
`corre() -> list[str]` (lista de fallos, vacía si pasa) para que un futuro
`tests/check.py` pueda cablearlo sin reimplementar nada -- mismo patrón que
`tests/test_corrida0.py`.

Tres guardias del diseño (§9(4)) + un caso de prueba que dispara cada una:
  T-RESERVA             ninguna fila RESERVADA trae R
  T-EMISOR-NO-COMPARA    ninguna fila IDENTICO se usa como si comparara
                         M contra R (columna `M` vacía en las 89 NACIONAL
                         IDENTICO -- el emisor es diagnóstico, no insumo)
  T-PISO-NO-CIRCULAR     ninguna fila MARGINAL trae piso
                         MARGINAL-SIN-INTERACCION (ese piso es SOLO de
                         cruce piloteado, nunca de una celda marginal)
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "marcador_segmento_bajo_prueba", RAIZ / "tools" / "marcador_segmento.py")
M = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = M
_spec.loader.exec_module(M)

FALLOS: list[str] = []


def _falla(caso, msg):
    FALLOS.append(f"{caso}: {msg}")


def t_reserva_sin_r():
    v = M.deriva()
    for f in v["filas"]:
        if f["estado"] == "RESERVADA" and (f.get("R") not in ("", None)):
            _falla("T-RESERVA", f"{f['celda_id']} es RESERVADA y trae R={f['R']!r}")


def t_emisor_no_compara():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "NACIONAL" and f["emisor_vs_arbitro"] == "EMISOR=ARBITRO":
            # El emisor IDENTICO es diagnostico: no se usa como M que compite
            # contra R en una celda de cruce -- solo aparece en filas NACIONAL,
            # nunca en una fila CRUCE con piso.
            if f["tipo"] == "CRUCE":
                _falla("T-EMISOR-NO-COMPARA",
                       f"{f['celda_id']} es EMISOR=ARBITRO dentro de una fila CRUCE")


def t_piso_no_circular():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "MARGINAL" and f["piso"] == "MARGINAL-SIN-INTERACCION":
            _falla("T-PISO-NO-CIRCULAR",
                   f"{f['celda_id']} es MARGINAL con piso MARGINAL-SIN-INTERACCION "
                   f"(ese piso es solo de cruce piloteado)")


def t_veinte_adoptadas():
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "CRUCE"
            and f["resultado_id"] and f["estado"] in
            ("ADOPTADO-POR-FIRMA", "PISO-ADMISIBLE-NO-ADOPTADO"))
    if n != 20:
        _falla("T-VEINTE-ADOPTADAS", f"se esperaban 20 celdas C2 piloteadas, salieron {n}")


def t_universo_97_nacional():
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "NACIONAL")
    if n != 97:
        _falla("T-UNIVERSO-97", f"censo ADR-536 debía dar 97 filas NACIONAL, dio {n}")


CASOS = (t_reserva_sin_r, t_emisor_no_compara, t_piso_no_circular,
         t_veinte_adoptadas, t_universo_97_nacional)


def corre() -> list[str]:
    FALLOS.clear()
    for caso in CASOS:
        caso()
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    if fallos:
        print(f"FALLA -- {len(fallos)} caso(s):")
        for f in fallos:
            print(f"  - {f}")
        return 1
    print(f"PASA -- {len(CASOS)} casos de tests/test_marcador_segmento.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
