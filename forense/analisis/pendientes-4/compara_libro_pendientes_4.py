#!/usr/bin/env python3
"""compara_libro_pendientes_4.py -- ACTO GEN2-PENDIENTES-4, P4: comprueba por lector CSV que el acto sólo tocó donde el
encargo lo autoriza (§9), comparando el árbol contra una referencia de git (por defecto `origin/main`):

  * `forense/no-corrido.tsv`: mismo conjunto de ids (ninguna fila añadida ni borrada) y, en las filas que cambian, sólo
    los campos `sucesor`, `estado`, `cerrado_por` y `fecha_cierre`;
  * `forense/firmas-pendientes.tsv`: sólo filas añadidas, ninguna modificada ni borrada.

Defecto real que atrapa: un aplicador de dictamen que reescribe un campo ajeno o borra una fila sellada (el libro y el
tablero de firmas son la memoria del programa: A.14, A.12). Sale con código 1 si algo se sale de lo autorizado.

    python3 forense/analisis/pendientes-4/compara_libro_pendientes_4.py [<ref-git>]
"""
import csv
import io
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CAMPOS_AUTORIZADOS = {"sucesor", "estado", "cerrado_por", "fecha_cierre"}


def desde_git(ref, ruta):
    txt = subprocess.run(["git", "show", f"{ref}:{ruta}"], cwd=RAIZ, capture_output=True, text=True, check=True).stdout
    return {r["id"]: r for r in csv.DictReader(io.StringIO(txt, newline=""), delimiter="\t")}


def desde_arbol(ruta):
    with open(os.path.join(RAIZ, ruta), newline="", encoding="utf-8") as fh:
        return {r["id"]: r for r in csv.DictReader(fh, delimiter="\t")}


def main():
    ref = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    mal = []
    a, b = desde_git(ref, "forense/no-corrido.tsv"), desde_arbol("forense/no-corrido.tsv")
    cambian = [i for i in a if i in b and a[i] != b[i]]
    ajenos = [i for i in cambian if any(a[i][k] != b[i][k] for k in a[i] if k not in CAMPOS_AUTORIZADOS)]
    print(f"no-corrido.tsv · {ref} {len(a)} filas · árbol {len(b)} filas · ids añadidos {len(set(b) - set(a))} · "
          f"ids quitados {len(set(a) - set(b))} · filas con algún campo distinto {len(cambian)} · "
          f"con un campo fuera de {'/'.join(sorted(CAMPOS_AUTORIZADOS))} distinto {len(ajenos)}")
    if set(b) - set(a) or set(a) - set(b) or ajenos:
        mal.append("no-corrido.tsv")
    fa, fb = desde_git(ref, "forense/firmas-pendientes.tsv"), desde_arbol("forense/firmas-pendientes.tsv")
    mod = [i for i in fa if i in fb and fa[i] != fb[i]]
    print(f"firmas-pendientes.tsv · {ref} {len(fa)} filas · árbol {len(fb)} filas · ids añadidos {len(set(fb) - set(fa))} · "
          f"ids quitados {len(set(fa) - set(fb))} · filas modificadas {len(mod)}")
    if set(fa) - set(fb) or mod:
        mal.append("firmas-pendientes.tsv")
    if mal:
        print("FUERA DE LO AUTORIZADO:", ", ".join(mal))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
