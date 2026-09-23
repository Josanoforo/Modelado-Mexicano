#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/derivados_protegidos.py -- lista por COMANDO los archivos
"# DERIVADO — NO EDITAR" del repo (P4, ACTO GEN2-TUBERIA-EFICIENCIA-1,
firma de mesa 21/sep/2026 §2(2): «Los archivos derivados no viajan en los
PR: un job del push a main los re-deriva y commitea»).

CERO RUTAS TECLEADAS: la lista se deriva grep-eando la cabecera literal
`# DERIVADO — NO EDITAR` (la misma que `tools/corrida0.py:CABECERA_DERIVADO`
y `tools/resuelve_citas.py:CABECERA_DERIVADO` ya escriben) sobre los TSV/MD
versionados del árbol -- nunca una lista a mano que se desactualiza el día
que un derivador nuevo nace (ese es justo el defecto de un archivo
compartido que D-21 prohíbe editar a mano).

Uso:
    python3 tools/derivados_protegidos.py            # una ruta por línea
    python3 tools/derivados_protegidos.py --json      # lista JSON
    python3 tools/derivados_protegidos.py --toca <refA> <refB>
        # 1 si algún archivo derivado cambió entre dos refs de git
        # (`git diff --name-only refA refB`), 0 si ninguno -- lo que
        # `verify.yml` usa para el guardia de PR.
    python3 tools/derivados_protegidos.py --solo-derivados <base> <cabeza>
        # 0 sólo si hay cambios y TODOS tienen cabecera DERIVADO; habilita
        # el PR automático del publicador sin abrir el guardia a otros PR.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CABECERA = "# DERIVADO — NO EDITAR"

# Extensiones de texto donde tiene sentido buscar la cabecera; evita abrir
# binarios o payloads del corpus (data/raw, etc.) que grep -r igual saltaría
# por ser binarios, pero así queda declarado y no es un accidente de grep.
_EXT = (".tsv", ".md", ".yaml", ".yml", ".json")

# Directorios fuera de perímetro que nunca se examinan aunque tuvieran un
# TSV con esa cabecera (payloads de terceros, corpus crudo, .git): A.13 --
# el universo examinado se declara explícito, no es "todo el disco".
_EXCLUYE_PREFIJOS = (
    os.path.join(RAIZ, ".git") + os.sep,
    os.path.join(RAIZ, "data", "raw") + os.sep,
)


def _candidatos() -> list[str]:
    out = subprocess.run(
        ["git", "-C", RAIZ, "ls-files"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    return [f for f in out if f.endswith(_EXT)]


def lista_derivados() -> list[str]:
    """Universo examinado: todo archivo versionado (`git ls-files`) con
    extensión de texto conocida, cuya PRIMERA línea no vacía es exactamente
    la cabecera `# DERIVADO — NO EDITAR` (con o sin paréntesis de atribución
    a continuación en la misma línea)."""
    hallados = []
    examinados = 0
    for rel in _candidatos():
        ruta = os.path.join(RAIZ, rel)
        if any(ruta.startswith(p) for p in _EXCLUYE_PREFIJOS):
            continue
        examinados += 1
        try:
            with open(ruta, "rb") as fh:
                primera = fh.readline().decode("utf-8", "replace").rstrip("\n")
        except OSError:
            continue
        if primera.startswith(CABECERA):
            hallados.append(rel)
    return sorted(hallados), examinados


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    rutas, examinados = lista_derivados()
    if argv[:1] == ["--solo-derivados"]:
        if len(argv) != 3:
            print("uso: --solo-derivados <base> <cabeza>", file=sys.stderr)
            return 2
        cambiados = set(subprocess.run(
            ["git", "-C", RAIZ, "diff", "--name-only",
             f"{argv[1]}...{argv[2]}"],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines())
        ajenos = sorted(cambiados - set(rutas))
        if not cambiados or ajenos:
            print("PR automático de derivados inválido: "
                  + (", ".join(ajenos) if ajenos else "sin cambios"),
                  file=sys.stderr)
            return 1
        print(f"PR automático: {len(cambiados)} archivos DERIVADO")
        return 0
    if argv[:1] == ["--toca"]:
        if len(argv) != 3:
            print("uso: --toca <refA> <refB>", file=sys.stderr)
            return 2
        ref_a, ref_b = argv[1], argv[2]
        cambiados = set(subprocess.run(
            ["git", "-C", RAIZ, "diff", "--name-only", ref_a, ref_b],
            capture_output=True, text=True, check=True,
        ).stdout.splitlines())
        tocados = sorted(set(rutas) & cambiados)
        for t in tocados:
            print(t)
        return 1 if tocados else 0
    if "--json" in argv:
        print(json.dumps({"derivados": rutas, "archivos_examinados": examinados},
                          ensure_ascii=False, indent=2))
        return 0
    for r in rutas:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
