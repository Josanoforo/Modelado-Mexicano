#!/usr/bin/env python3
"""Derivador de cifras compartido para documentos del programa.

ACTO GEN2-CIERRE-SEMANAL-1 (§1: «un solo derivador de cifras compartido»).
Generaliza `tools/readme_derivado.py` a cualquier documento: toda cifra
escrita como `N <!-- deriva: <comando> -->` se re-deriva ejecutando el
comando y tomando el último entero de su salida — la misma lectura que
`tests/test_frente_publico_2.py`. `corrida0.py status | rg '^clave='` se
resuelve con UNA corrida de status por invocación (≈75 s).

Defecto que atrapa: cifras publicadas que se quedaron atrás del árbol
(`docs/one-pager.md` decía 246 corridas selladas con el comando dando 285).

Uso:
    python3 tools/deriva_cifras.py ARCHIVO...             # 1 si hay desfase
    python3 tools/deriva_cifras.py --escribe ARCHIVO...   # refresca en su sitio
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[1]
PATRON = re.compile(r"(\d[\d ]*?)(\s*<!--\s*deriva:\s*(.+?)\s*-->)")
STATUS = re.compile(r"^python3 tools/corrida0\.py status \| rg '\^([A-Za-z0-9_]+)='$")
_status: list[str] = []


def _miles(n: int, muestra: str) -> str:
    return f"{n:,}".replace(",", " ") if " " in muestra.strip() or n >= 10000 else str(n)


def corre(comando: str) -> int:
    m = STATUS.match(comando)
    if m:
        if not _status:
            _status.append(subprocess.check_output(
                [sys.executable, "tools/corrida0.py", "status"], cwd=RAIZ, text=True))
        v = re.search(rf"(?m)^{re.escape(m.group(1))}=(\d+)$", _status[0])
        if not v:
            raise SystemExit(f"{m.group(1)} no aparece en corrida0.py status")
        return int(v.group(1))
    salida = subprocess.run(["bash", "-o", "pipefail", "-c", comando], cwd=RAIZ,
                            capture_output=True, text=True, timeout=300)
    if salida.returncode != 0:
        raise SystemExit(f"comando falló ({salida.returncode}): {comando}\n{salida.stderr[:300]}")
    n = re.search(r"(\d+)\s*\Z", salida.stdout.strip())
    if not n:
        raise SystemExit(f"comando sin número al final: {comando!r}")
    return int(n.group(1))


def main(argv: list[str]) -> int:
    escribe = "--escribe" in argv
    archivos = [a for a in argv if not a.startswith("--")]
    desfase = 0
    for nombre in archivos:
        ruta = RAIZ / nombre
        texto = ruta.read_text(encoding="utf-8")
        cambios: list[str] = []

        def sustituye(m: re.Match) -> str:
            nuevo = corre(m.group(3))
            viejo = int(m.group(1).replace(" ", ""))
            if viejo != nuevo:
                cambios.append(f"{nombre}: {viejo} -> {nuevo}  [{m.group(3)[:90]}]")
                return _miles(nuevo, m.group(1)) + m.group(2)
            return m.group(0)

        nuevo_texto = PATRON.sub(sustituye, texto)
        for c in cambios:
            print(c)
        desfase += len(cambios)
        if escribe and cambios:
            ruta.write_text(nuevo_texto, encoding="utf-8")
    print(f"cifras_desfasadas={desfase}")
    return 0 if escribe or not desfase else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
