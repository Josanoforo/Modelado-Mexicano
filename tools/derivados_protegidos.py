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
_EXT = (".tsv", ".md", ".yaml", ".yml", ".json", ".txt")

# Directorios fuera de perímetro que nunca se examinan aunque tuvieran un
# TSV con esa cabecera (payloads de terceros, corpus crudo, .git): A.13 --
# el universo examinado se declara explícito, no es "todo el disco".
_EXCLUYE_PREFIJOS = (
    os.path.join(RAIZ, ".git") + os.sep,
    os.path.join(RAIZ, "data", "raw") + os.sep,
)


def _es_tabla_de_valor(rel: str) -> bool:
    """ACTO GEN2-TUBERIA-VISTA-NORMALIZADA-4: `data/corrida0/<CALC>/valores-vista/*`
    es derivado por RUTA (lo escribe `registro --escribe`, byte a byte del
    `valor` sellado: no admite cabecera sin cambiar el valor)."""
    partes = rel.split("/")
    return len(partes) == 5 and partes[:2] == ["data", "corrida0"] and partes[3] == "valores-vista"


MARCA_BLOQUE = ("<!-- TABLERO-DERIVADO:BEGIN -->", "<!-- TABLERO-DERIVADO:END -->")


def _fuera_del_bloque(texto: str) -> str | None:
    """Texto sin el bloque TABLERO-DERIVADO; `None` si no trae el par de marcas."""
    ini, fin = MARCA_BLOQUE
    a, b = texto.find(ini), texto.find(fin)
    if a < 0 or b < a:
        return None
    return texto[:a] + texto[b + len(fin):]


def _solo_cambia_bloque(base: str, cabeza: str, rel: str) -> bool:
    """ACTO GEN2-TUBERIA-TABLERO-EN-CANAL-1 publica el tablero en el PR
    automático: el archivo es derivado sólo dentro del bloque marcado."""
    def lee(ref):
        r = subprocess.run(["git", "-C", RAIZ, "show", f"{ref}:{rel}"],
                           capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    antes, despues = lee(base), lee(cabeza)
    if antes is None or despues is None:
        return False
    fuera = _fuera_del_bloque(antes)
    return fuera is not None and fuera == _fuera_del_bloque(despues)


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
        if primera.startswith(CABECERA) or _es_tabla_de_valor(rel):
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
        base = subprocess.run(
            ["git", "-C", RAIZ, "merge-base", argv[1], argv[2]],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        ajenos = sorted(r for r in cambiados - set(rutas)
                        if not _solo_cambia_bloque(base, argv[2], r))
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
