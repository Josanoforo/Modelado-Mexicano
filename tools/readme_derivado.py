#!/usr/bin/env python3
"""Refresca las cifras de `corrida0.py status` en la tabla derivada de README.md.

El canal de derivados (verify.yml, job guardias) re-deriva las vistas que
mueven esas cifras; sin este paso cada PR `derivados/auto-*` rompe
`tests/test_readme_derivado.py`. Sólo toca celdas dentro del bloque
TABLERO-DERIVADO, que `derivados_protegidos.py --solo-derivados` acepta.

Uso: python3 tools/readme_derivado.py [--escribe]   (sin flag: 1 si hay desfase)
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"
FILA = re.compile(
    r"(?m)^(\|[^\n]+?\| )([\d ]+)( \| <!-- deriva: "
    r"python3 tools/corrida0.py status \| rg '\^([A-Za-z0-9_]+)=' -->)")


def _miles(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def main(argv: list[str]) -> int:
    salida = subprocess.check_output(
        [sys.executable, "tools/corrida0.py", "status"], cwd=RAIZ, text=True)
    valores = {k: int(v) for k, v in re.findall(r"(?m)^([A-Za-z0-9_]+)=(\d+)$", salida)}
    texto = README.read_text(encoding="utf-8")
    cambios = []

    def sustituye(m: re.Match) -> str:
        clave = m.group(4)
        nuevo = _miles(valores[clave])
        if m.group(2) != nuevo:
            cambios.append(f"{clave}: {m.group(2)} -> {nuevo}")
        return m.group(1) + nuevo + m.group(3)

    nuevo_texto = FILA.sub(sustituye, texto)
    for c in cambios:
        print(c)
    if "--escribe" in argv:
        if cambios:
            README.write_text(nuevo_texto, encoding="utf-8")
        return 0
    return 1 if cambios else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
