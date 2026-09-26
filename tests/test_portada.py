#!/usr/bin/env python3
"""tests/test_portada.py -- raíz limpia, citas resueltas por índice, enlaces vivos.

ACTO GEN2-FRONT-3-PORTADA-1 (P1). Defecto que atrapa: FRONT-1 aplazó el
movimiento de 35 archivos de la raíz porque moverlos rompía citas selladas
(`archivo/INDICE.md`, 23/sep); sin esta guardia, el movimiento o un archivo
nuevo en la raíz vuelven a dejar citas sin resolver o la portada con 46
archivos, y nadie lo ve hasta que un lector externo cae en un enlace roto.

Cuatro grupos:
1. La raíz tiene <= 12 archivos de primer nivel (directorios y ocultos aparte).
2. Cada fila de `archivo/INDICE.md` apunta a un archivo que existe, y su
   nombre ya no está en la raíz.
3. Toda cita por nombre en `canon/` y `forense/` a un archivo que estaba en
   la raíz antes del commit de movimiento resuelve con `tools/resuelve_cita.py`.
4. Cero enlaces relativos rotos en README.md, CONTRIBUTING.md y docs/.

Corre sola:  python3 tests/test_portada.py
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import resuelve_cita as RC  # noqa: E402

MAX_RAIZ = 12
FAILS: list[str] = []
CITA = re.compile(
    r"(?<![\w/.-])((?:instrucciones-proyecto-v|propuesta-|PROPUESTA-|revision-)[\w.\-]+?\.md(?:\.sha256)?|requirements-dev\.txt)(?![\w.-])")
ENLACE = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")


def _falla(nombre: str, msg: str) -> None:
    FAILS.append(f"{nombre}: {msg}")


def archivos_raiz() -> list[str]:
    return sorted(p.name for p in RAIZ.iterdir() if p.is_file() and not p.name.startswith("."))


def prueba_raiz_limpia():
    raiz = archivos_raiz()
    if len(raiz) > MAX_RAIZ:
        _falla("raiz_limpia", f"{len(raiz)} archivos de primer nivel (> {MAX_RAIZ}): {raiz}")


def prueba_indice_apunta_a_archivos_vivos():
    t = RC.tabla()
    if not t:
        _falla("indice", "archivo/INDICE.md no trae filas `nombre` | `ruta` | `commit`")
        return
    for nombre, (ruta, _c) in t.items():
        if not (RAIZ / ruta).is_file():
            _falla("indice", f"{nombre} -> {ruta}, que no existe")
        if (RAIZ / nombre).exists():
            _falla("indice", f"{nombre} sigue en la raíz y además está en el índice")


def _estaba_en_raiz(commit: str, nombre: str) -> bool:
    r = subprocess.run(["git", "-C", str(RAIZ), "cat-file", "-e", f"{commit}^:{nombre}"],
                       capture_output=True)
    return r.returncode == 0


def prueba_citas_selladas_resuelven():
    t = RC.tabla()
    commits = {c for _r, c in t.values()}
    citados: set[str] = set()
    examinados = 0
    for base in ("canon", "forense"):
        for p in (RAIZ / base).rglob("*.md"):
            examinados += 1
            citados.update(CITA.findall(p.read_text(encoding="utf-8", errors="replace")))
    if examinados == 0:
        _falla("citas", "0 archivos examinados en canon/ y forense/ (A.13)")
        return
    for nombre in sorted(citados):
        if RC.resuelve(nombre):
            continue
        if any(_estaba_en_raiz(c, nombre) for c in commits):
            _falla("citas", f"`{nombre}` estaba en la raíz y no resuelve por el índice")


def _enlaces_rotos(path: Path) -> list[str]:
    rotos = []
    texto = path.read_text(encoding="utf-8")
    texto = re.sub(r"`[^`\n]*`", "", texto)  # código en línea no es enlace
    for destino in ENLACE.findall(texto):
        if destino.startswith(("http:", "https:", "#", "{{", "mailto:")):
            continue
        destino = destino.split("#", 1)[0]
        if destino and not (path.parent / destino).exists():
            rotos.append(f"{path.relative_to(RAIZ)}: {destino}")
    return rotos


def prueba_enlaces_relativos():
    docs = [RAIZ / "README.md", RAIZ / "CONTRIBUTING.md"] + sorted((RAIZ / "docs").rglob("*.md"))
    rotos = [r for p in docs for r in _enlaces_rotos(p)]
    if rotos:
        _falla("enlaces", f"{len(rotos)} rotos de {len(docs)} documentos: {rotos}")


def prueba_resolvedor():
    t = RC.tabla()
    if t:
        nombre, (ruta, _c) = next(iter(sorted(t.items())))
        r = subprocess.run([sys.executable, str(RAIZ / "tools" / "resuelve_cita.py"), nombre],
                           capture_output=True, text=True)
        if r.returncode != 0 or r.stdout.strip() != ruta:
            _falla("resolvedor", f"{nombre}: dio {r.stdout.strip()!r} rc={r.returncode}, esperaba {ruta!r}")
    r = subprocess.run([sys.executable, str(RAIZ / "tools" / "resuelve_cita.py"), "no-existe-jamas.md"],
                       capture_output=True, text=True)
    if r.returncode != 1:
        _falla("resolvedor", f"un nombre inexistente debe salir con 1, salió con {r.returncode}")


def main() -> int:
    for nombre, f in sorted(globals().items()):
        if nombre.startswith("prueba_") and callable(f):
            f()
    if FAILS:
        for x in FAILS:
            print("FAIL", x)
        return 1
    print(f"OK test_portada: raíz {len(archivos_raiz())} archivos, índice {len(RC.tabla())} filas, enlaces sin rotos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
