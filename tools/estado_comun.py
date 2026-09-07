#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/estado_comun.py -- primitivas de estado operativo compartidas entre
`tools/digesto_tramite.py`, `tools/tablero_programa.py` y `tests/check.py`
(T22), para dejar de tener implementaciones divergentes de conceptos
puramente mecánicos.

ACTO AUTOMATIZA-1-E2 · ESTADO-COMUN, 7/sep/2026
(`forense/encargos/2026-09-07-AUTOMATIZA-1-E1-PERIMETRO-FISICO.md`,
ELEMENTO 2). Defecto real medido antes de esta pieza: `tools/tablero_programa.py`
comparaba `estado == "ABIERTA"` (ciego a la glosa `ABIERTA -- pendiente...`)
mientras `tools/digesto_tramite.py` ya usaba `^ABIERTA(\\s|$)` -- sobre el
árbol real del 7/sep/2026, el digesto contaba 4 filas `ABIERTA`
(`FP-263, FP-288, FP-303, FP-326`) y el tablero sólo 2 (`FP-288, FP-326`):
`FP-263`/`FP-303` traen glosa y el tablero las perdía.

Sin clases, sin estado global: funciones puras con argumentos explícitos
(`raiz`, la ruta del clon). No es un framework ni una capa de gobernanza --
es exactamente las cinco primitivas que el encargo autoriza, movidas desde
donde ya vivían (mayormente `tools/digesto_tramite.py`), no reinventadas.

`tests/check.py::t15_adr_count()` NO usa `adr_max()` de aquí: es el vigía
de duplicados/huecos/secuencia de ADR y conserva su propia derivación --
duplicación deliberada de verificación, no deuda (T15 verificaría este
mismo módulo si `adr_max()` tuviera un defecto, y un vigía que comparte
implementación con lo que vigila deja de vigilar nada).
"""
import os
import re
import subprocess


def es_abierta(estado):
    """`estado` es `ABIERTA` con o sin glosa (`ABIERTA -- pendiente de...`).
    Comparar con `==` es ciego a la glosa y subcuenta las filas `ABIERTA`
    del tablero -- defecto real, medido (ver cabecera de este módulo).
    `estado.split()[0]` no basta (colisiona con la exactitud de otros
    estados de una sola palabra que empiecen igual, si los hubiera); el
    ancla `^ABIERTA(\\s|$)` es la comparación correcta, movida sin
    reinterpretar desde `tools/digesto_tramite.py`. No usa `startswith`:
    `ABIERTA-RECIBO` no es `ABIERTA`."""
    return bool(re.match(r"^ABIERTA(\s|$)", estado or ""))


def lee_tablero(raiz):
    """(ruta, filas, n_lineas). TSV con cabecera, sin comillas -- el
    tablero se lee, no se parsea con `csv`, porque sus celdas ya traen
    comillas literales de firmas verbatim (semántica CSV cambiaría ese
    contenido). Movido sin reinterpretar desde
    `tools/digesto_tramite.py::lee_tablero`."""
    ruta = os.path.join(raiz, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(ruta):
        return ruta, None, 0
    with open(ruta, encoding="utf-8") as fh:
        lineas = [l.rstrip("\n") for l in fh if l.strip()]
    if not lineas:
        return ruta, [], 0
    cab = lineas[0].split("\t")
    filas = [dict(zip(cab, l.split("\t"))) for l in lineas[1:]]
    return ruta, filas, len(lineas)


def _corre(cmd, raiz, timeout=60):
    """Ejecuta y devuelve (rc, salida). Nunca lanza: un comando que no
    corre es un hallazgo, no una caída. Mismo contrato que
    `tools/digesto_tramite.py::corre`, reimplementado aquí (no importado
    de digesto) para que digesto pueda importar DE este módulo sin crear
    un ciclo."""
    try:
        p = subprocess.run(cmd, cwd=raiz, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError as e:
        return 127, f"comando no encontrado: {e}"
    except subprocess.TimeoutExpired:
        return 124, f"tiempo agotado ({timeout}s)"


def ramas_remotas_presentes(raiz):
    """(ramas, fuente). Todas las ramas remotas presentes en `origin`
    (incluida `main`, sin filtrar -- el filtro es decisión de cada
    llamador). Nombre `presentes`, no `vivas`: una rama en origin no
    implica PR abierto ni trabajo sin fusionar; esta función informa lo
    que sabe, no lo que eso significa. Estrategia movida sin reinterpretar
    desde `tools/digesto_tramite.py::seccion_c`: `git ls-remote --heads
    origin`; si no responde, `git for-each-ref refs/remotes/origin`
    (refleja el último `fetch` de este clon, no necesariamente el remoto
    de ahora)."""
    rc, salida = _corre(["git", "ls-remote", "--heads", "origin"], raiz)
    if rc == 0 and salida.strip():
        fuente = "git ls-remote --heads origin (estado vivo del remoto)"
        ramas = sorted({l.split("refs/heads/", 1)[1].strip()
                        for l in salida.splitlines() if "refs/heads/" in l})
    else:
        rc2, salida2 = _corre(["git", "for-each-ref", "--format=%(refname:short)",
                               "refs/remotes/origin"], raiz)
        fuente = (f"git for-each-ref refs/remotes/origin (RESPALDO: ls-remote no "
                  f"respondió, rc={rc}) -- refleja el último fetch de este clon, "
                  f"no necesariamente el remoto de ahora")
        ramas = sorted({l.strip().split("origin/", 1)[-1]
                        for l in salida2.splitlines() if l.strip()
                        and not l.strip().endswith("/HEAD")})
    return ramas, fuente


def adr_max(raiz):
    """Máximo ADR actual, derivado de `canon/gobernanza-v1_15.md` -- mismo
    comando de la casa que ya usan `tools/tablero_programa.py` y la
    cascada de `/acto`, reimplementado en Python en vez de `grep`
    encadenado. Para tablero, E3 y consumidores productivos -- NO para
    T15 (ver cabecera del módulo)."""
    ruta = os.path.join(raiz, "canon", "gobernanza-v1_15.md")
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    nums = [int(n) for n in re.findall(r"^\*\*ADR-(\d+)", texto, re.M)]
    return max(nums) if nums else 0


def fp_max(raiz):
    """Máximo FP actual, primera columna de
    `forense/firmas-pendientes.tsv`. E3 la necesita y no debe crear una
    segunda implementación."""
    ruta = os.path.join(raiz, "forense", "firmas-pendientes.tsv")
    if not os.path.exists(ruta):
        return 0
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    nums = [int(n) for n in re.findall(r"^FP-(\d+)", texto, re.M)]
    return max(nums) if nums else 0
