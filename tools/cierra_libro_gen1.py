#!/usr/bin/env python3
"""`tools/cierra_libro_gen1.py` -- cierra el libro GEN1 de un solo golpe y
**sin juicio**. Script de UN USO.

ACTO GEN2-E7 · pieza D · D1. Decisión de dirección **D13**, firmada por el
merge: *no hay retrofit 2*. Los encargos GEN1 sin marca **no se clasifican
uno por uno**; se cierra el libro con un rótulo mecánico y no se reabre.

## Por qué no se clasifican

`E.1` — GEN1 es **historia, no autoridad**. Un encargo GEN1 no ejecutado no
puede colarse a GEN2, porque **GEN2 no lee encargos: lee demanda**
(`corrida0.py demanda` deriva el perímetro de los **consumidores activos**,
`E.2`). Clasificar 61 encargos a mano es la jornada del 30/jul con otro
nombre, y produciría exactamente el mismo resultado: una tabla que nadie
consulta.

## Qué hace, exactamente

Para cada archivo de `forense/encargos/*.md` (NO de `cola/`) que cumpla las
CUATRO condiciones:

  1. tiene prefijo de fecha `AAAA-MM-DD-` (la convención lo exige;
     `convencion.md` y `PLANTILLA-LOTE-v1_0.md` no son encargos);
  2. no trae encabezado `## CONSUMIDO`, `## SUSTITUIDO` ni `## HISTÓRICO*`;
  3. está fechado **antes** del cierre de GEN1 (`2026-09-07`, merge de
     `#597`);
  4. **no lo cita ningún `NC-` ABIERTA** de `forense/no-corrido.tsv` —
     un encargo con deuda viva asentada no es historia todavía;

añade al final, **verbatim** y una sola vez, el rótulo `ROTULO`.

No reescribe nada más: no toca el cuerpo, no marca `CONSUMIDO` (sería una
falsedad: estos encargos no se ejecutaron), no toca los `## SUSTITUIDO`
existentes y no borra un archivo.

## Idempotente

Un archivo que ya trae el rótulo se salta. Correrlo dos veces no duplica
nada; correrlo después de que un encargo gane `## CONSUMIDO` tampoco lo
toca.

Uso:
    python3 tools/cierra_libro_gen1.py            # dry-run: lista y no escribe
    python3 tools/cierra_libro_gen1.py --aplica   # escribe
    python3 tools/cierra_libro_gen1.py --tsv      # la lista para la nota
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_ENCARGOS = RAIZ / "forense" / "encargos"
NO_CORRIDO = RAIZ / "forense" / "no-corrido.tsv"

# Fecha del cierre de GEN1 -- merge de `PR #597`.
CIERRE_GEN1 = "2026-09-07"

ROTULO = ("## HISTÓRICO-GEN1 — sin marca al cierre de GEN1 (7/sep/2026, "
          "PR #597). No se reabre: GEN2 deriva su perímetro de consumidores "
          "activos (E.2), no de encargos. Registrado por GEN2-E7 pieza D.")

_RE_FECHA = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
_RE_MARCAS = re.compile(r"^## (CONSUMIDO|SUSTITUIDO|HIST[OÓ]RICO)", re.M)

# El mismo patrón que `tools/digesto_tramite.py` ya usa para detectar un
# encargo que el ÁRBOL declara no consumido en prosa (sin encabezado). No
# excluye del rótulo -- `HISTÓRICO-GEN1` no afirma que se consumió, afirma
# que no tenía marca -- pero SÍ se reporta, para que la lista de la nota
# distinga los dos casos en vez de aplanarlos.
_RE_NO_CONSUMIDO = re.compile(
    r"SUSTITUID[OA]|DEVUELT[OA]-POR-MESA|no ejecutado|no consumido|"
    r"queda como historia", re.I)


def nc_abiertas_citan() -> set[str]:
    """Los basename de encargo que cita alguna fila `NC-` en estado ABIERTA.
    Un encargo con deuda viva asentada NO se cierra como historia."""
    citados: set[str] = set()
    if not NO_CORRIDO.exists():
        return citados
    with NO_CORRIDO.open(encoding="utf-8", newline="") as fh:
        for fila in csv.DictReader(fh, delimiter="\t"):
            if (fila.get("estado") or "").strip().upper() != "ABIERTA":
                continue
            crudo = "\t".join(v or "" for v in fila.values())
            for m in re.findall(r"[\w.\-]+\.md", crudo):
                citados.add(os.path.basename(m))
    return citados


def candidatos() -> list[dict]:
    """Las filas de la decisión, con la razón de cada una a la vista. Nada
    se decide en silencio: un archivo excluido dice por qué."""
    citados = nc_abiertas_citan()
    fuera = []
    for ruta in sorted(DIR_ENCARGOS.glob("*.md")):
        nombre = ruta.name
        m = _RE_FECHA.match(nombre)
        texto = ruta.read_text(encoding="utf-8", errors="replace")
        if m is None:
            estado, razon = "EXCLUIDO", "sin prefijo de fecha -- no es un encargo"
        elif ROTULO in texto:
            estado, razon = "YA-ROTULADO", "ya trae HISTÓRICO-GEN1"
        elif _RE_MARCAS.search(texto):
            marca = _RE_MARCAS.search(texto).group(1)
            estado, razon = "EXCLUIDO", f"ya trae encabezado ## {marca}"
        elif m.group(1) >= CIERRE_GEN1:
            estado, razon = "EXCLUIDO", (f"fechado {m.group(1)}, en o después "
                                          f"del cierre de GEN1 ({CIERRE_GEN1})")
        elif nombre in citados:
            estado, razon = "EXCLUIDO", "citado por un NC- ABIERTA -- deuda viva"
        elif _RE_NO_CONSUMIDO.search(texto):
            estado, razon = "ROTULA", ("⚠️ NO MARCAR -- el árbol lo declara no "
                                        "consumido en prosa; el rótulo NO dice "
                                        "que se consumió, dice que no tenía marca")
        else:
            estado, razon = "ROTULA", "sin PR que lo cite"
        fuera.append({"archivo": nombre, "fecha": m.group(1) if m else "",
                      "estado": estado, "razon": razon})
    return fuera


def aplica(filas: list[dict]) -> int:
    escritos = 0
    for fila in filas:
        if fila["estado"] != "ROTULA":
            continue
        ruta = DIR_ENCARGOS / fila["archivo"]
        texto = ruta.read_text(encoding="utf-8")
        if not texto.endswith("\n"):
            texto += "\n"
        ruta.write_text(texto + "\n" + ROTULO + "\n", encoding="utf-8")
        escritos += 1
    return escritos


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--aplica", action="store_true",
                   help="escribe el rótulo (por defecto: dry-run)")
    p.add_argument("--tsv", action="store_true",
                   help="la lista completa en TSV, para pegar en la nota")
    args = p.parse_args()

    filas = candidatos()
    if args.tsv:
        w = csv.DictWriter(sys.stdout, fieldnames=["archivo", "fecha", "estado",
                                                    "razon"], delimiter="\t",
                           lineterminator="\n")
        w.writeheader()
        for fila in filas:
            w.writerow(fila)
        return 0

    por_estado: dict[str, int] = {}
    for fila in filas:
        por_estado[fila["estado"]] = por_estado.get(fila["estado"], 0) + 1
    print(f"forense/encargos/*.md examinados: {len(filas)} (A.13)")
    for estado in sorted(por_estado):
        print(f"  {estado:12s} {por_estado[estado]}")
    n_no_marcar = sum(1 for f in filas
                      if f["estado"] == "ROTULA" and "NO MARCAR" in f["razon"])
    print(f"\n  de los ROTULA: {por_estado.get('ROTULA', 0) - n_no_marcar} "
          f"«sin PR que lo cite» · {n_no_marcar} «⚠️ NO MARCAR»")

    if not args.aplica:
        print("\nDRY-RUN -- no se escribio nada. `--aplica` para escribir.")
        return 0
    escritos = aplica(filas)
    print(f"\nAPLICADO: {escritos} encargo(s) rotulados HISTÓRICO-GEN1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
