#!/usr/bin/env python3
"""Control positivo externo de `prereg-caja-R-ENVIPE-SERIE` — GEN2 contra GEN1.

`ACTO GEN2-R-SERIE-CSV`, 9/sep/2026. Congelado en el COMMIT-1 junto con la
spec y los tres medidores, **antes de abrir un solo byte de microdato** y
antes de leer un solo JSON de `corridas-R/`.

## Por qué es un archivo aparte y no un `RESULT` del medidor

El encargo manda: «DESPUES de sellar, y solo entonces, el script de control
calcula el delta del punto contra el JSON GEN1 de cada celda». Si el delta
fuera un `RESULT`, el medidor tendria que abrir el dictamen GEN1 y el valor
GEN1 entraria a la corrida sellada por una via que no hace falta. Aqui no
entra: los tres `medidor.py` no abren `corridas-R/` y no reciben el valor GEN1
por ningun parametro (spec sellada, §0.3 y §6.1).

## Que compara, y que NO

Compara el **punto**: `RESULT-R-<celda>-PUNTO` de
`data/corrida0/CALC-R-<celda>/resultados.json` contra el campo del punto del
dictamen GEN1 `forense/prereg-duelo-v2/corridas-R/<celda>.json`.

**NO compara el IC.** El bootstrap de GEN1 no fijo semilla comparable, asi que
los extremos no son comparables dígito a dígito y compararlos seria fabricar
un desacuerdo que no significa nada.

## Las cuatro ramas, pre-declaradas (spec sellada §6.1)

  REPRODUCE                 |delta| <= 1.0e-9
  REPRODUCE-CON-TOLERANCIA  1.0e-9 < |delta| <= 1.0e-6
  NO-REPRODUCE              |delta| > 1.0e-6
  NO-COMPARABLE             la celda salio NO-ESTIMABLE, o el JSON GEN1 no
                            trae punto legible

`NO-REPRODUCE` **no invalida la corrida, no autoriza tocar el medidor y no
cambia el estimando**: se reporta con signo, junto al embudo de esa ola, y
abre una fila `NC` para reconciliar universos.

Este script **no escribe nada**: imprime. Lo que se conserva es su salida,
pegada en la nota del lote.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CELDAS = ["CIV-M-10", "CIV-M-12", "CIV-M-13"]
TOL_EXACTA = 1.0e-9
TOL_FLOTANTE = 1.0e-6

# Nombres bajo los que un dictamen R de GEN1 puede guardar su punto. Se
# declaran ANTES de abrir ninguno: el script no "encuentra" el campo que le
# conviene, busca en una lista cerrada y, si no esta, dice NO-COMPARABLE.
CAMPOS_PUNTO_GEN1 = ["R", "punto", "R_hat", "p_hat", "valor", "estimacion"]


def _punto_gen1(doc: dict):
    """(valor, ruta_del_campo) o (None, motivo). Busca en la raiz y un nivel
    de anidamiento, sobre la lista cerrada de arriba."""
    for k in CAMPOS_PUNTO_GEN1:
        v = doc.get(k)
        if isinstance(v, (int, float)):
            return float(v), k
    for padre, hijo in doc.items():
        if isinstance(hijo, dict):
            for k in CAMPOS_PUNTO_GEN1:
                v = hijo.get(k)
                if isinstance(v, (int, float)):
                    return float(v), f"{padre}.{k}"
    return None, ("ningun campo de " + "/".join(CAMPOS_PUNTO_GEN1)
                  + " es numerico en la raiz ni a un nivel")


def rama(delta: float) -> str:
    a = abs(delta)
    if a <= TOL_EXACTA:
        return "REPRODUCE"
    if a <= TOL_FLOTANTE:
        return "REPRODUCE-CON-TOLERANCIA"
    return "NO-REPRODUCE"


def main() -> int:
    print("CONTROL POSITIVO EXTERNO · prereg-caja-R-ENVIPE-SERIE · GEN2 vs GEN1")
    print("  compara el PUNTO, nunca el IC (el bootstrap de GEN1 no fijo semilla comparable)")
    print("  ramas: REPRODUCE (<=1e-9) · REPRODUCE-CON-TOLERANCIA (<=1e-6) · "
          "NO-REPRODUCE · NO-COMPARABLE")
    print()
    veredictos = {}
    examinados = 0
    for celda in CELDAS:
        p_gen2 = RAIZ / "data" / "corrida0" / f"CALC-R-{celda}" / "resultados.json"
        p_gen1 = RAIZ / "forense" / "prereg-duelo-v2" / "corridas-R" / f"{celda}.json"
        print(f"=== {celda} ===")
        if not p_gen2.exists():
            print(f"  NO-COMPARABLE -- ausente {p_gen2.relative_to(RAIZ)} "
                  f"(la corrida GEN2 no esta sellada todavia)")
            veredictos[celda] = "NO-COMPARABLE"
            continue
        if not p_gen1.exists():
            print(f"  NO-COMPARABLE -- ausente {p_gen1.relative_to(RAIZ)}")
            veredictos[celda] = "NO-COMPARABLE"
            continue
        examinados += 2
        g2 = json.loads(p_gen2.read_text(encoding="utf-8"))
        vals = g2.get("resultados", g2)
        punto = vals.get(f"RESULT-R-{celda}-PUNTO")
        estado = vals.get(f"RESULT-R-{celda}-ESTADO")
        g1 = json.loads(p_gen1.read_text(encoding="utf-8"))
        ref, campo = _punto_gen1(g1)
        print(f"  GEN2  {p_gen2.relative_to(RAIZ)}")
        print(f"        RESULT-R-{celda}-PUNTO  = {punto!r}   (ESTADO = {estado!r})")
        print(f"  GEN1  {p_gen1.relative_to(RAIZ)}")
        print(f"        campo `{campo}`            = {ref!r}")
        if punto is None or not isinstance(punto, (int, float)):
            print(f"  VEREDICTO: NO-COMPARABLE -- la corrida GEN2 no dio punto "
                  f"(ESTADO = {estado!r})")
            veredictos[celda] = "NO-COMPARABLE"
            continue
        if ref is None:
            print(f"  VEREDICTO: NO-COMPARABLE -- {campo}")
            veredictos[celda] = "NO-COMPARABLE"
            continue
        delta = float(punto) - ref
        v = rama(delta)
        print(f"  DELTA (GEN2 - GEN1) = {delta:+.17g}")
        print(f"  VEREDICTO: {v}")
        if v == "NO-REPRODUCE":
            print("             NO invalida la corrida. NO se toca el medidor. "
                  "Se reporta con su embudo y abre NC de reconciliacion de universo.")
        veredictos[celda] = v
    print()
    print("RESUMEN · " + " · ".join(f"{c}={veredictos.get(c, 'SIN-CORRER')}"
                                    for c in CELDAS))
    print(f"A.13 · archivos examinados por este comando: {examinados}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
