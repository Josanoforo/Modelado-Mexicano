#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/nc_por_razon.py -- cuenta NC de `forense/no-corrido.tsv` por token de
razon (A.14) en una ventana de fechas.

Linea base del falsador de `PLANTILLA-ENCARGO-v2_0.md` (ACTO GEN2-V215, P5):
la plantilla se revisa si `PARO-PREMISA` + `PARO-ENTORNO` + `FUERA-DE-PERIMETRO`
no bajan a menos de un tercio de las NC nuevas en los tres meses siguientes a su
sello. Se mide aqui, no a mano.

A.16: el token se reconoce por PREFIJO EXACTO de la columna `razon`, sin cortar
por espacio ni por dos puntos, y con variantes con y sin tilde -- un parser que
corta por espacio pierde `DIFERIDO-A: ACTO ...` y uno sin tildes pierde
`FUERA-DE-PERIMETRO`. Lo que no empieza con token cuenta como `SIN-TOKEN`, que
es un estado reportable, no un cero.

Uso:
    python3 tools/nc_por_razon.py --desde 2026-09-16 --hasta 2026-09-20
    python3 tools/nc_por_razon.py                      # todo el archivo
"""
from __future__ import annotations

import argparse
import csv
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TSV = RAIZ / "forense" / "no-corrido.tsv"

# Los siete tokens de A.14, en su forma canonica (con tilde donde la lleva).
TOKENS = [
    "PARO-ENTORNO",
    "PARO-PREMISA",
    "FUERA-DE-PERÍMETRO",
    "SUSTITUIDO-POR",
    "DIFERIDO-A",
    "NO-VERIFICABLE-AQUÍ",
    "DECISIÓN-DE-MESA-PENDIENTE",
]
# Los tres que el falsador suma.
FALSADOR = {"PARO-PREMISA", "PARO-ENTORNO", "FUERA-DE-PERÍMETRO"}


def _plano(s: str) -> str:
    """Mayusculas sin tildes: `FUERA-DE-PERIMETRO` casa con `FUERA-DE-PERÍMETRO`."""
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").upper().strip()


_TOKENS_PLANOS = [(t, _plano(t)) for t in TOKENS]


def clasifica(razon: str) -> str:
    """Token canonico cuyo texto plano prefija a `razon` plana; el mas largo gana."""
    r = _plano(razon)
    casa = [t for t, tp in _TOKENS_PLANOS if r.startswith(tp)]
    return max(casa, key=len) if casa else "SIN-TOKEN"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--desde", help="fecha ISO inclusive (columna `fecha`)")
    ap.add_argument("--hasta", help="fecha ISO inclusive")
    ap.add_argument("--tsv", default=str(TSV))
    args = ap.parse_args(argv)

    ruta = Path(args.tsv)
    if not ruta.exists():
        print(f"NO-ENCONTRADO: {ruta}", file=sys.stderr)
        return 2

    with ruta.open(encoding="utf-8", newline="") as fh:
        filas = list(csv.DictReader(fh, delimiter="\t"))

    examinadas = len(filas)
    sel = [f for f in filas
           if (not args.desde or (f.get("fecha") or "") >= args.desde)
           and (not args.hasta or (f.get("fecha") or "") <= args.hasta)]

    cuenta: dict[str, int] = {}
    for f in sel:
        cuenta[clasifica(f.get("razon", ""))] = cuenta.get(clasifica(f.get("razon", "")), 0) + 1

    ventana = f"{args.desde or 'INICIO'}..{args.hasta or 'FIN'}"
    # A.13: todo negativo declara cuantas filas examino.
    print(f"universo: {ruta.relative_to(RAIZ) if ruta.is_relative_to(RAIZ) else ruta} · "
          f"filas examinadas={examinadas} · ventana={ventana} · NC en ventana={len(sel)}")
    if not sel:
        print("NC en ventana = 0 — sin denominador, no hay porcentaje que reportar.")
        return 0
    for t in TOKENS + ["SIN-TOKEN"]:
        n = cuenta.get(t, 0)
        marca = " *" if t in FALSADOR else ""
        print(f"  {t:<28} {n:>4}  {100.0 * n / len(sel):5.1f}%{marca}")
    # Cuantos actos distintos aportan los PARO-*: el TSV trae campos citados con
    # saltos de linea dentro, asi que esto se cuenta con el lector csv y nunca con
    # awk/cut, que parten por \n y subcuentan en silencio (20/27 filas, 12/18 actos).
    paro = [f for f in sel if clasifica(f.get("razon", "")) in ("PARO-PREMISA", "PARO-ENTORNO")]
    actos = {(f.get("acto") or "(vacio)").strip() for f in paro}
    print(f"  PARO-* aportados por {len(actos)} actos distintos ({len(paro)} filas)")

    tres = sum(cuenta.get(t, 0) for t in FALSADOR)
    print(f"  {'(*) suma del falsador':<28} {tres:>4}  {100.0 * tres / len(sel):5.1f}%"
          f"   umbral de revision: < 33.3%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
