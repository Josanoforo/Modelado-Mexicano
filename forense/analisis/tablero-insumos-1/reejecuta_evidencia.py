#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-ejecuta la evidencia de los dictámenes de GEN2-TUBERIA-TABLERO-INSUMOS-1 (P3 y P4).

    python3 forense/analisis/tablero-insumos-1/reejecuta_evidencia.py forense/analisis/tablero-insumos-1/dictamen-p3-*.tsv \\
        forense/analisis/tablero-insumos-1/resultado-p4-*.tsv

Cada fila de esos TSV trae `comando` (un comando de shell, desde la raíz del repo, sin red) y
`esperado_en_salida` (una subcadena literal que su salida debe contener). Este script corre cada
comando y comprueba la subcadena: es la receta de un minuto para que quien lea un cierre de NC
(`cerrado_por`) reproduzca la cita sin creerle al que la escribió (A.5, E.2: reproducir no es
validar, pero un cierre por producto que no se reproduce no es un cierre).

No escribe nada: rechaza cualquier comando que contenga una operación de escritura conocida
(rm, mv, cp, tee, sed -i, git commit/push/checkout/reset/clean/stash/fetch) y, además, compara
`git status --porcelain` antes y después de cada comando: si el árbol cambió, la fila falla. Sale
con código 1 si alguna fila falla. Una fila cuyo `esperado_en_salida` ya no aparece no prueba que el cierre
fuera falso: dice que el objeto cambió desde el 29/sep/2026 (por ejemplo, la vista publicada ya
trae CALC que ese día faltaban) y que la fila hay que volver a dictaminarla.
"""
import csv
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ESCRIBE = re.compile(r"\brm\b|\bmv\b|\bcp\b|\btee\b|sed\s+-i|git\s+(commit|push|checkout|reset|clean|stash|fetch|merge|rebase)")


def arbol():
    return subprocess.run(["git", "status", "--porcelain"], cwd=RAIZ, capture_output=True, text=True).stdout


def filas(ruta):
    csv.field_size_limit(10**9)
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main(argv):
    if not argv:
        sys.exit(__doc__)
    fallas = total = 0
    for ruta in argv:
        for r in filas(ruta):
            total += 1
            cmd, esperado = r.get("comando", ""), r.get("esperado_en_salida", "")
            causa = None
            if not cmd or not esperado:
                causa = "comando o esperado_en_salida vacío"
            elif ESCRIBE.search(cmd):
                causa = "el comando contiene una operación de escritura: no se ejecuta"
            else:
                antes = arbol()
                try:
                    p = subprocess.run(["bash", "-c", cmd], cwd=RAIZ, capture_output=True, text=True, timeout=60)
                    if esperado not in p.stdout + p.stderr:
                        causa = f"{esperado!r} no está en la salida (rc={p.returncode})"
                except subprocess.TimeoutExpired:
                    causa = "TIMEOUT 60 s"
                if arbol() != antes:
                    causa = "el comando MODIFICÓ el árbol de trabajo"
            fallas += bool(causa)
            print(("FALLA " if causa else "OK    ") + os.path.basename(ruta) + " · " + r["id"][-46:] + ((" · " + causa) if causa else ""))
    print(f"--- {total} filas, {fallas} con falla")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
