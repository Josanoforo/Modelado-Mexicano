#!/usr/bin/env python3
"""Resuelve una cita por NOMBRE de archivo a su ruta actual, vía archivo/INDICE.md.

ACTO GEN2-FRONT-3-PORTADA-1 (P1). Firma de mesa 26/sep/2026: «Los archivos
históricos y normativos salen de la raíz con git mv; una cita por nombre en
texto sellado no se edita: la resuelve archivo/INDICE.md y
tools/resuelve_cita.py.»

No confundir con `tools/resuelve_citas.py` (plural), que resuelve citas
`RES-####`/`CORR-####` contra la demanda histórica: otro objeto.

Uso:
  python3 tools/resuelve_cita.py <nombre>          # imprime la ruta actual (exit 1 si no resuelve)
  python3 tools/resuelve_cita.py --genera <commit> # imprime las filas del índice para los
                                                   # renombres de ese commit (git show -M)

La tabla del índice se deriva con `--genera` sobre el commit de movimiento;
nunca se teclea a mano.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
INDICE = RAIZ / "archivo" / "INDICE.md"
FILA = re.compile(r"^\| `([^`]+)` \| `([^`]+)` \| `([0-9a-f]{7,40})` \|$", re.M)


def tabla() -> dict[str, tuple[str, str]]:
    """nombre citado -> (ruta actual, commit del movimiento)."""
    if not INDICE.exists():
        return {}
    return {n: (r, c) for n, r, c in FILA.findall(INDICE.read_text(encoding="utf-8"))}


def resuelve(nombre: str) -> str | None:
    nombre = nombre.strip().lstrip("./")
    fila = tabla().get(pathlib.PurePosixPath(nombre).name)
    if fila:
        return fila[0]
    if (RAIZ / nombre).is_file():
        return nombre
    return None


def genera(commit: str) -> list[str]:
    salida = subprocess.check_output(
        ["git", "-C", str(RAIZ), "show", "-M", "--name-status", "--format=", commit], text=True)
    corto = subprocess.check_output(
        ["git", "-C", str(RAIZ), "rev-parse", "--short=8", commit], text=True).strip()
    filas = []
    for linea in salida.splitlines():
        partes = linea.split("\t")
        if partes[0].startswith("R") and len(partes) == 3 and "/" not in partes[1]:
            filas.append(f"| `{partes[1]}` | `{partes[2]}` | `{corto}` |")
    return sorted(filas, key=str.lower)


def main(argv: list[str]) -> int:
    if len(argv) == 2 and argv[0] == "--genera":
        print("\n".join(genera(argv[1])))
        return 0
    if len(argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    ruta = resuelve(argv[0])
    if ruta is None:
        print(f"NO-RESUELVE: {argv[0]} (ni en {INDICE.relative_to(RAIZ)} ni en la raíz)", file=sys.stderr)
        return 1
    print(ruta)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
