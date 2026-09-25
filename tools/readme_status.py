#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/readme_status.py -- reescribe en README.md las cifras de la tabla
de portada que se derivan de `python3 tools/corrida0.py status`.

Cada fila derivada lleva el comentario
`<!-- deriva: python3 tools/corrida0.py status | rg '^<clave>=' -->`; la
cifra impresa es la celda anterior. `tests/test_readme_derivado.py` las
compara con `status`. El canal `[deriva]` (verify.yml) cambia la vista y con
ella esas cifras: este comando es su único productor dentro del PR
automático, y `derivados_protegidos.py --solo-derivados` sólo acepta en
README.md líneas con esa forma (`ES_FILA_STATUS`).

Uso:
    python3 tools/readme_status.py            # 1 si README está desfasado
    python3 tools/readme_status.py --escribe  # reescribe las cifras
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
README = RAIZ / "README.md"

FILA_STATUS = re.compile(
    r"(?m)^(\|[^\n]+?\| )([\d ]+)( \| <!-- deriva: "
    r"python3 tools/corrida0\.py status \| rg '\^([A-Za-z0-9_]+)=' -->[^\n]*)$"
)


def es_fila_status(linea: str) -> bool:
    return FILA_STATUS.fullmatch(linea.rstrip("\n")) is not None


def _formatea(valor: int, impreso: str) -> str:
    # Conserva la convención de la portada: miles separados por espacio
    # (`78 747`) sólo donde la cifra ya venía agrupada o pasa de 9 999.
    if " " in impreso or valor >= 10000:
        return f"{valor:,}".replace(",", " ")
    return str(valor)


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    salida = subprocess.check_output(
        [sys.executable, "tools/corrida0.py", "status"], cwd=RAIZ, text=True)
    valores = {k: int(v) for k, v in
               re.findall(r"(?m)^([A-Za-z0-9_]+)=(\d+)$", salida)}
    texto = README.read_text(encoding="utf-8")
    cambios = []

    def sustituye(m: re.Match) -> str:
        clave, impreso = m.group(4), m.group(2)
        nuevo = _formatea(valores[clave], impreso)
        if int(impreso.replace(" ", "")) != valores[clave]:
            cambios.append(f"{clave}: {impreso} -> {nuevo}")
        return m.group(1) + nuevo + m.group(3)

    nuevo_texto = FILA_STATUS.sub(sustituye, texto)
    for c in cambios:
        print(c)
    if "--escribe" in argv:
        if nuevo_texto != texto:
            README.write_text(nuevo_texto, encoding="utf-8")
        return 0
    return 1 if cambios else 0


if __name__ == "__main__":
    sys.exit(main())
