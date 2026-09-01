#!/usr/bin/env python3
"""Regenera data/cola-adquisicion-v1_0.tsv como VISTA (P3, MAESTRA33-A5).

Fuente de verdad: data/curacion-registro/cola-adquisicion-registro.tsv.
Este script NUNCA se corre "y ya" a mano sobre la cola -- cualquier cambio
de contenido pasa por el registro (tools/curador_registro/
registra_cola_adquisicion.py) y esta vista solo proyecta las 7 columnas
que /adquiere y /arbitra ya conocen, en el mismo orden y esquema, para no
romper ningun consumidor existente.

tests/check.py::test_vista_cola_adquisicion falla si el archivo en disco
difiere de lo que esta funcion produce -- esa es la garantia de "no
editar a mano" (P3).
"""

from __future__ import annotations

import csv
from pathlib import Path

REGISTRO = Path("data/curacion-registro/cola-adquisicion-registro.tsv")
VISTA = Path("data/cola-adquisicion-v1_0.tsv")

CABECERA_COMENTARIO = (
    "# GENERADO -- no editar a mano. Fuente: "
    "data/curacion-registro/cola-adquisicion-registro.tsv. "
    "Regenerar con: python3 tools/vista_cola_adquisicion.py "
    "(ACTO MAESTRA33-A5 · RECONCILIA-ADQUISICION-CON-CURADOR, P3)."
)

COLUMNAS_VISTA = [
    "fuente_canonica",
    "estado_A4A5",
    "prioridad",
    "url_conocida",
    "ids_manifiesto",
    "origen",
    "nota",
]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def render(registro_rows: list[dict[str, str]]) -> str:
    lines = [CABECERA_COMENTARIO, "\t".join(COLUMNAS_VISTA)]
    for row in registro_rows:
        lines.append("\t".join(row[col] for col in COLUMNAS_VISTA))
    return "\n".join(lines) + "\n"


def build(registro_path: Path = REGISTRO) -> str:
    return render(read_tsv(registro_path))


def main() -> int:
    contenido = build()
    VISTA.write_text(contenido, encoding="utf-8")
    filas = contenido.count("\n") - 2
    print(f"vista regenerada: {VISTA} ({filas} filas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
