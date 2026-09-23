#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/lote_desde_asientos.py -- el lote de `registro --escribe --lote`
se DERIVA del diff de `forense/replay-evidencia.tsv`, nunca se teclea
(ACTO GEN2-TUBERIA-CANAL-PUBLICACION-1, 22/sep/2026, P1; firmas de mesa
`…PENDIENTES-CAJA-1-c09b-02` y `…ESCOLARIDAD-2-0af9-01`, opción (a)).

Qué hace: dado un rango de dos refs de git (`<antes> <despues>`), calcula
`git diff -- forense/replay-evidencia.tsv` entre ellas, toma las LÍNEAS
AÑADIDAS (asientos nuevos -- las quitadas o editadas en su sitio no
cuentan: el registro es append-only y una línea que cambia de contenido en
su sitio no es un asiento nuevo, es una edición que ya vigila T50), y
devuelve el `calc_id` (primera columna) de cada una -- filtrado a los que
tienen `sello.json` (SELLADA, `_verifica_sello() == COINCIDE`) bajo
`data/corrida0/<calc_id>/`. Un asiento que cita un CALC sin sello, o
directamente ausente del árbol, no entra al lote: nombrarlo en `--lote`
sin sello sería justo lo que `RESULT-SIN-SELLO`/`HASH-AUSENTE` de
`corrida0.py` ya existen para atrapar más adelante en el propio
`registro()` -- este derivador no duplica esa validación, sólo no ofrece
como candidato algo que `registro()` de todos modos rechazaría, para que
el mensaje de error sea el de `registro()` y no un lote ruidoso.

Cero juicio: no decide SI un asiento debe entrar, sólo LEE cuáles entraron
en el push. El juicio (qué transición de replay puede cambiar) sigue
siendo de quien escribió `forense/replay-evidencia.tsv` -- este comando no
lo repite ni lo cuestiona.

Uso:
    python3 tools/lote_desde_asientos.py <antes> <despues>
        # una línea por calc_id, orden determinista (orden de aparición
        # en el diff, sin duplicados)
    python3 tools/lote_desde_asientos.py <antes> <despues> --csv
        # la misma lista, una sola línea separada por comas -- lista para
        # `--lote`
    python3 tools/lote_desde_asientos.py <antes> <despues> --json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
REPLAY_EVIDENCIA_REL = "forense/replay-evidencia.tsv"
CORRIDAS = RAIZ / "data" / "corrida0"


def _git_diff(antes: str, despues: str, cwd: Path) -> str:
    r = subprocess.run(
        ["git", "diff", "--unified=0", "--no-color", antes, despues, "--",
         REPLAY_EVIDENCIA_REL],
        cwd=cwd, capture_output=True, text=True)
    if r.returncode not in (0, 1):
        # `git diff` sale 1 cuando SÍ hay diferencias -- no es error; sólo
        # un código distinto de 0/1 es un fallo real del comando.
        raise RuntimeError(
            f"git diff {antes} {despues} -- {REPLAY_EVIDENCIA_REL} "
            f"terminó con código {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def calc_ids_anadidos(diff_texto: str) -> list[str]:
    """`calc_id` de cada línea AÑADIDA (`+`, no `+++`) del diff unified=0,
    en orden de aparición, sin duplicados. La cabecera (`calc_id\t...`) se
    descarta si aparece como añadida (archivo nuevo desde cero)."""
    vistos: list[str] = []
    vistos_set: set[str] = set()
    for linea in diff_texto.splitlines():
        if not linea.startswith("+") or linea.startswith("+++"):
            continue
        cuerpo = linea[1:]
        if not cuerpo.strip():
            continue
        calc_id = cuerpo.split("\t", 1)[0].strip()
        if not calc_id or calc_id == "calc_id":
            continue
        if calc_id not in vistos_set:
            vistos_set.add(calc_id)
            vistos.append(calc_id)
    return vistos


# Import perezoso, SIEMPRE desde el árbol real de `tools/` -- nunca desde
# un `cwd`/`corridas_dir` que un llamador (o un test) haya redirigido. El
# diff de git y la carpeta de CALC sí pueden apuntar a un repo temporal
# (pruebas con git de verdad); el propio código de `corrida0.py` no se
# sustituye por eso.
sys.path.insert(0, str(RAIZ / "tools"))
import corrida0  # noqa: E402


def _tiene_sello(calc_id: str, corridas_dir: Path) -> bool:
    """SELLADA de verdad -- `sello.json` presente Y `_verifica_sello()`
    dice COINCIDE, la misma verificación que `corrida0.py::_lee_oferta`
    usa para decidir si un RESULT tiene respaldo."""
    d = corridas_dir / calc_id
    if not (d / "sello.json").exists():
        return False
    estado, _razon = corrida0._verifica_sello(d)
    return estado == "COINCIDE"


def lote_desde_diff(antes: str, despues: str, cwd: Path | None = None,
                    corridas_dir: Path | None = None) -> dict:
    """Devuelve `{"calc_ids": [...], "descartados": [{"calc_id", "razon"}]}`.
    `descartados` es lo que un asiento nuevo citó pero no calificó para el
    lote -- se reporta, no se silencia (A.13: un negativo declara qué
    examinó). `cwd` (dónde corre `git diff`) y `corridas_dir` (dónde viven
    los `CALC-*/`) son opcionales -- por defecto el árbol real (`RAIZ`,
    `CORRIDAS`); una prueba con git de verdad en un repo temporal los pasa
    explícitos, sin tocar el módulo global."""
    cwd = cwd or RAIZ
    corridas_dir = corridas_dir or CORRIDAS
    diff_texto = _git_diff(antes, despues, cwd)
    candidatos = calc_ids_anadidos(diff_texto)
    lote, descartados = [], []
    for calc_id in candidatos:
        d = corridas_dir / calc_id
        if not d.is_dir():
            descartados.append({"calc_id": calc_id,
                                "razon": f"CALC-AUSENTE: no existe {d}"})
            continue
        if not _tiene_sello(calc_id, corridas_dir):
            descartados.append({"calc_id": calc_id,
                                "razon": "SIN-SELLO: sello.json ausente o "
                                         "_verifica_sello() != COINCIDE"})
            continue
        lote.append(calc_id)
    return {"calc_ids": lote, "descartados": descartados,
            "examinados": len(candidatos)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("antes", help="ref/commit ANTES del push")
    ap.add_argument("despues", help="ref/commit DESPUÉS del push")
    ap.add_argument("--csv", action="store_true",
                    help="una línea, separada por comas -- lista para --lote")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    salida = lote_desde_diff(args.antes, args.despues)

    if args.json:
        print(json.dumps(salida, ensure_ascii=False, indent=2))
    elif args.csv:
        print(",".join(salida["calc_ids"]))
    else:
        for calc_id in salida["calc_ids"]:
            print(calc_id)

    for d in salida["descartados"]:
        print(f"DESCARTADO · {d['calc_id']}: {d['razon']}", file=sys.stderr)
    print(f"asientos nuevos examinados: {salida['examinados']} · "
          f"lote: {len(salida['calc_ids'])} · "
          f"descartados: {len(salida['descartados'])}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
