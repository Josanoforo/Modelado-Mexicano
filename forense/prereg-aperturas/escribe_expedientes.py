#!/usr/bin/env python3
"""Escribe o verifica el contrato `corrida0` y la receta de cada expediente de apertura.

ACTO GEN2-APERTURAS-PREREGISTRADAS-1 (28/sep/2026).

    python3 forense/prereg-aperturas/escribe_expedientes.py             # lista expedientes (no escribe; D-23)
    python3 forense/prereg-aperturas/escribe_expedientes.py --escribe   # APERTURA-<X>-spec.yaml + RECETA-APERTURA-<X>.md
    python3 forense/prereg-aperturas/escribe_expedientes.py --verifica  # 0 si ambos casan byte a byte con la derivación
    ... --solo X[,Y]                                                    # limita a esos expedientes

Un expediente completo es una carpeta `forense/prereg-aperturas/<X>/` con `medidor_apertura_*.py`.
"""
from __future__ import annotations

import glob
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import expediente_apertura as E  # noqa: E402


def expedientes(solo=None):
    out = []
    for p in sorted(glob.glob(os.path.join(AQUI, "*", "medidor_apertura_*.py"))):
        if solo and os.path.basename(os.path.dirname(p)) not in solo:
            continue
        rel = os.path.relpath(p, E.RAIZ)
        M = E.carga(p, "med_" + os.path.basename(p)[:-3])
        out.append((rel, M))
    return out


def main(argv):
    solo = set(argv[argv.index("--solo") + 1].split(",")) if "--solo" in argv else None
    exps = expedientes(solo)
    if "--escribe" in argv:
        for rel, M in exps:
            print(E.escribe_contrato(rel, M), E.escribe_receta(M))
        return 0
    if "--verifica" in argv:
        malos = 0
        for rel, M in exps:
            x = M.CONTRATO["x"]
            for r, t in ((E.ruta_contrato(x), E.texto_contrato(rel, M)), (E.ruta_receta(x), E.texto_receta(M))):
                ruta = os.path.join(E.RAIZ, r)
                ok = os.path.exists(ruta) and open(ruta, encoding="utf-8").read() == t
                malos += not ok
                print(f"{r}: {'CASA' if ok else 'NO-CASA'}")
        return 1 if malos else 0
    for rel, M in exps:
        print(M.CONTRATO["x"], rel)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
