#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/l0_vista.py -- vista completa de la línea L0 (histórico congelado +
fragmentos por acto), por comando (`ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-1`,
21/sep/2026, P-A.5).

Desde ese acto, `canon/estado-programa-v1_15.md` deja de cargar la L0
completa a mano: su línea `L0` es un puntero corto a
`canon/L0/HISTORICO.md` (congelado, hash fijado por `T49`) más un
fragmento nuevo por acto en `canon/L0/<ADR-raíz-del-acto>.md`. Este
comando es la única forma soportada de ver el conjunto: nunca se escribe
a un archivo compartido.

Uso:
    python3 tools/l0_vista.py           # imprime histórico + fragmentos,
                                          # en orden: histórico primero,
                                          # fragmentos por orden alfabético
                                          # de archivo (= orden de ADR-raíz)
    python3 tools/l0_vista.py --conteo   # sólo el conteo (líneas: histórico
                                          # + N fragmentos)
"""
import glob
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORICO = os.path.join(RAIZ, "canon", "L0", "HISTORICO.md")
DIR_FRAGMENTOS = os.path.join(RAIZ, "canon", "L0")


def fragmentos():
    """Todo `.md` bajo `canon/L0/` salvo `HISTORICO.md`, orden alfabético
    (= orden de `ADR-raíz`, que empieza por AAMMDD)."""
    rutas = sorted(glob.glob(os.path.join(DIR_FRAGMENTOS, "*.md")))
    return [p for p in rutas if os.path.basename(p) != "HISTORICO.md"]


def main():
    frags = fragmentos()
    if "--conteo" in sys.argv:
        print(f"histórico: {'presente' if os.path.exists(HISTORICO) else 'AUSENTE'} "
              f"· fragmentos: {len(frags)}")
        for f in frags:
            print(f"  {os.path.relpath(f, RAIZ)}")
        return 0

    if os.path.exists(HISTORICO):
        with open(HISTORICO, encoding="utf-8") as f:
            print(f.read())
    else:
        print("HISTORICO.md AUSENTE", file=sys.stderr)

    for f in frags:
        print(f"\n--- {os.path.relpath(f, RAIZ)} ---")
        with open(f, encoding="utf-8") as fh:
            print(fh.read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
