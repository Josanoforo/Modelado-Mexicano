"""ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-2 · reconstruye la fila completa de
`resultados.tsv` tras la normalizacion de COMMIT-A (y COMMIT-B para
`camino_linaje`).

`tolerancia`, `funciones_dependencia` y `fuente_replay` salieron de
`resultados.tsv`: son identicas para todo RESULT de la misma corrida
(verificado por comando en #1109 -- 0/313 corridas con valor no
constante), asi que viven una vez por corrida en `corridas.tsv`. Un
consumidor que necesite esos tres campos por RESULT los recupera con
`join_resultado`, que hace exactamente el `join` por `corrida_id` que la
firma de mesa de `GEN2-TUBERIA-VISTA-NORMALIZADA-2` describe -- no
reinventa el dato, lo busca donde vive ahora.

No lee microdato, no mide, no adopta: es lectura pura sobre las vistas ya
derivadas.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

# Mismo patron que tools/corrida0.py:102 -- corridas.tsv/resultados.tsv
# tienen campos (camino_linaje, funciones_dependencia) mas largos que el
# limite por defecto de 131072 bytes del modulo csv.
csv.field_size_limit(sys.maxsize)

RAIZ = Path(__file__).resolve().parent.parent
CORRIDAS = RAIZ / "data" / "corrida0"
VISTA_CORRIDAS = CORRIDAS / "corridas.tsv"
VISTA_RESULTADOS = CORRIDAS / "resultados.tsv"

# Campos que COMMIT-A movio de resultados.tsv a corridas.tsv (constantes
# por corrida_id). Un cambio a este conjunto es tambien un cambio a
# COLS_VISTA_RESULTADOS/COLS_VISTA_CORRIDAS en tools/corrida0.py -- ambos
# se editan juntos, nunca uno sin el otro.
CAMPOS_MOVIDOS_A_CORRIDA = ("tolerancia", "funciones_dependencia", "fuente_replay")


def _leer_tsv_derivado(ruta: Path) -> list[dict]:
    with ruta.open(encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


def corridas_por_id(ruta: Path = VISTA_CORRIDAS) -> dict[str, dict]:
    """`{corrida_id: fila}` de `corridas.tsv`, para pasar a `join_resultado`.
    `{}` si el archivo no existe (fixture sintetico de un solo TSV, o un
    consumidor que solo necesita camino_linaje): `join_resultado` cae al
    valor propio de la fila cuando lo tiene."""
    if not ruta.exists():
        return {}
    return {f["corrida_id"]: f for f in _leer_tsv_derivado(ruta)}


def join_resultado(fila_resultado: dict, corridas: dict[str, dict]) -> dict:
    """Devuelve una copia de `fila_resultado` con `tolerancia`,
    `funciones_dependencia` y `fuente_replay` completos. No muta
    `fila_resultado`.

    Regla: si la propia fila YA trae el campo (formato previo a COMMIT-A,
    o un fixture sintetico que lo declara a mano), ese valor manda -- no
    se pisa con el de la corrida. Solo se busca en `corridas` cuando el
    campo esta AUSENTE de la fila (el caso real tras COMMIT-A). Si tampoco
    esta en `corridas` (vista desincronizada, o `corridas` vino vacio por
    archivo ausente), el campo se llena con `SIN-CORRIDA-EN-VISTA` en vez
    de lanzar `KeyError`."""
    completa = dict(fila_resultado)
    corrida = corridas.get(fila_resultado.get("corrida_id"), {})
    for campo in CAMPOS_MOVIDOS_A_CORRIDA:
        if campo not in completa:
            completa[campo] = corrida.get(campo, "SIN-CORRIDA-EN-VISTA")
    return completa


def leer_resultados_join(
    ruta_resultados: Path = VISTA_RESULTADOS,
    ruta_corridas: Path = VISTA_CORRIDAS,
) -> list[dict]:
    """`resultados.tsv` con los tres campos de corrida ya reconstruidos por
    fila -- el punto de entrada normal para un consumidor que no quiera
    hacer el join a mano."""
    corridas = corridas_por_id(ruta_corridas)
    return [join_resultado(f, corridas) for f in _leer_tsv_derivado(ruta_resultados)]
