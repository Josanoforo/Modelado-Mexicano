#!/usr/bin/env python3
"""Deriva la muestra adversarial de BARRIDO-2 bajo la regla del §12 del encargo madre.

Se ejecuta y se COMMITEA **antes** de re-inspeccionar nada, que es el punto: una
muestra sorteada después de ver los resultados no es adversarial, es una selección.
La generación anterior murió por lo contrario y peor — sus 41 tareas venían de
`snapshot-v2`, y como `tarea_id = sha256(snapshot ‖ representacion ‖ contrato)`,
ninguna existía en la generación sellada; no es que los hashes difirieran, es que
las tareas no estaban. Por eso aquí la lista se deriva del **ledger vigente** y
queda congelada con su semilla antes de que exista el dato con el que se compara.

Regla del §12, aplicada sin adornos:
  por ola, max(3, ceil(5 % de las representaciones de la ola)), tope 20;
  si una ola tiene menos de 3, se revisan todas.

Prioridades del §12, en este orden y declaradas: primer lote de la ola, excepciones,
formato complejo. Lo que sobra se completa por sorteo determinista con la semilla
declarada abajo — determinista para que cualquiera reproduzca la misma muestra desde
el mismo ledger, y no una cómoda.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

REPO = Path("/home/pc0/Modelado-Mexicano-barrido2")
LEDGER = REPO / ".barrido2/private/t0/ledger-v7.tsv"
SALIDA = REPO / "data/curacion-universo/muestra-adversarial-barrido2.tsv"

# Semilla declarada. No es aleatoria: es el SHA de redacción del encargo de este
# acto, para que la muestra sea reproducible desde el propio expediente forense y
# nadie pueda alegar que se eligió después de ver los resultados.
SEMILLA = "3e4c9f7"

# Formatos que el §12 llama complejos: contenedor, binario con diccionario, o
# documento paginado. Prioridad sobre el resto dentro de la misma ola.
COMPLEJOS = {".zip", ".sav", ".dta", ".xls", ".xlsx", ".pdf"}

CAMPOS = ["ola", "orden_en_muestra", "tarea_id", "representacion_id", "payload_id",
          "sha256_12", "formato", "razon_de_seleccion"]


def orden_determinista(tarea_id: str) -> str:
    """Sorteo reproducible: hash de (semilla ‖ tarea_id). No usa random."""
    return hashlib.sha256(f"{SEMILLA}\x00{tarea_id}".encode("utf-8")).hexdigest()


def main() -> int:
    with LEDGER.open(encoding="utf-8-sig", newline="") as handle:
        filas = list(csv.DictReader(handle, delimiter="\t"))

    por_ola: dict[str, list[dict[str, str]]] = {}
    for fila in filas:
        por_ola.setdefault(fila["wave_initial"], []).append(fila)

    seleccion: list[list[str]] = []
    resumen: dict[str, dict[str, int]] = {}
    for ola in ("W1", "W2", "W3", "W4"):
        pobla = por_ola.get(ola, [])
        if not pobla:
            continue
        cupo = min(20, max(3, math.ceil(0.05 * len(pobla))))
        if len(pobla) < 3:
            cupo = len(pobla)

        # El "primer lote de la ola" es el que el driver corre primero, y el driver
        # ordena por `tarea_id` (`sorted(tareas)` en correr-olas-v7.py). Se deriva
        # de ahí, no se teclea.
        en_orden = sorted(pobla, key=lambda f: f["tarea_id"])
        primer_lote = {f["tarea_id"] for f in en_orden[:3]}

        def prioridad(f: dict[str, str]) -> tuple[int, str]:
            extension = Path(f["ruta_relativa"]).suffix.lower()
            if f["tarea_id"] in primer_lote:
                return (0, orden_determinista(f["tarea_id"]))
            if extension in COMPLEJOS:
                return (1, orden_determinista(f["tarea_id"]))
            return (2, orden_determinista(f["tarea_id"]))

        elegidas = sorted(pobla, key=prioridad)[:cupo]
        for indice, f in enumerate(elegidas, 1):
            extension = Path(f["ruta_relativa"]).suffix.lower()
            razon = ("PRIMER-LOTE-DE-LA-OLA" if f["tarea_id"] in primer_lote
                     else "FORMATO-COMPLEJO" if extension in COMPLEJOS
                     else "SORTEO-DETERMINISTA")
            seleccion.append([ola, str(indice), f["tarea_id"], f["representacion_id"],
                              f["payload_id"], f["sha256"][:12], extension or "SIN-EXTENSION", razon])
        resumen[ola] = {"poblacion": len(pobla), "cupo": cupo, "elegidas": len(elegidas)}

    for fila in seleccion:
        assert len(fila) == len(CAMPOS)
        assert all(celda and "\t" not in celda and "\n" not in celda for celda in fila)
    SALIDA.write_text("\n".join("\t".join(f) for f in [CAMPOS, *seleccion]) + "\n", encoding="utf-8")

    print(json.dumps({
        "semilla": SEMILLA,
        "por_ola": resumen,
        "total": len(seleccion),
        "razones": {r: sum(1 for f in seleccion if f[7] == r)
                    for r in sorted({f[7] for f in seleccion})},
        "muestra_sha256": hashlib.sha256(SALIDA.read_bytes()).hexdigest(),
    }, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
