#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""`tools/recibo/cifras_sin_result.py` -- por PR, archivos con cifras nuevas
bajo `canon/`/`forense/analisis/` que no trazan a un RESULT sellado.

ACTO GEN2-AUDITORIA-POST-HOC-ASTRA-1, pieza P1.

QUE ES. Para un commit de merge dado (o un rango explicito `base..merge`):
1. Lista los archivos `.md`/`.tsv`/`.yaml` añadidos o modificados bajo
   `canon/` o `forense/analisis/` (`git diff --diff-filter=AM --name-only`),
   excluyendo `forense/analisis/ci-guardias/` (censo de infraestructura de
   pruebas, no evidencia sustantiva sobre México).
2. Para cada uno, cuenta las "cifras" (tokens numericos de 2+ digitos, o
   con separador decimal/millar o `%`, que no sean parte de un
   identificador `CALC-...-0001`/`ADR-...`/`RESULT-...`/fecha ISO/`#1085`)
   añadidas en el diff de ESE archivo.
3. Revisa si el archivo COMPLETO en el commit de merge (`git show
   <merge>:<ruta>`) trae CUALQUIERA de dos trazas: (a) una cita literal
   `RESULT-<algo>` en algun lugar del archivo (convencion de `canon/`), o
   (b) un `CALC-<algo>` que SÍ tenga fila en `forense/replay-evidencia.tsv`
   (E.7 -- convencion real de los productos de `forense/analisis/`,
   verificada contra `CALC-ENDIREH-PISOS-2021-AYUDA-0001`: sus cifras no
   citan "RESULT-" en prosa, pero el CALC está asentado con
   `resultado_replay=REPRODUCE`). Buscar solo "RESULT-" habría marcado ese
   archivo como defecto siendo en realidad un RESULT sellado y registrado
   bajo otra convencion de nombre -- ese falso positivo es exactamente el
   costo que esta pieza (a) evita.
4. Un archivo con cifras nuevas y NINGUNA de las dos trazas -> `SIN-TRAZA`.
   Imprime conteo de archivos con cifras nuevas, cuantos son `SIN-TRAZA`,
   y el total de cifras nuevas (dato secundario, no el criterio de conteo).

QUE NO ES. No decide si la traza es la correcta para ESA cifra puntual
(eso es P2: perimetro y olas); solo si existe alguna traza verificable en
el archivo. No abre microdato. No decide veredicto.

Por que `merge^1..merge` y no `base...merge` del encargo. El encargo
sugiere `git diff <base>...<merge>`; con un `<base>` global (el SHA previo
a las catorce fusiones) esa forma acumula TODAS las fusiones intermedias
para un PR que fusiono tarde en la cadena -- no aisla la contribucion de
ese PR. `<merge>^1..<merge>` es exactamente lo que esa fusion cambio en
`main` en ese momento (su primer padre ES el estado de main justo antes),
lo que aisla el PR sin importar cuantas veces sincronizo con main antes de
fusionar. `--base` queda disponible para reproducir la forma literal del
encargo cuando se pida.

Verificacion de la receta (procedencia, §2): `--autoprueba` corre el
detector de cifras contra lineas sinteticas conocidas y falla en voz alta
si no distingue cifra de ruido de enumeracion; y prueba el detector de
cita RESULT contra un archivo sintetico con y sin la cita en otra linea
del archivo (no en la misma linea que la cifra), que es exactamente el
patron real que este script tiene que reconocer.

Uso::

    python3 tools/recibo/cifras_sin_result.py <merge-sha> [--base <sha>] [--json]
    python3 tools/recibo/cifras_sin_result.py --autoprueba

`CIFRAS_SIN_RESULT_RAIZ` (variable de entorno, solo para pruebas):
apunta el script a un repo git sintetico en vez de este repo -- así
`tests/test_cifras_sin_result.py` prueba el detector sin tocar ni depender
del contenido real de `forense/replay-evidencia.tsv`.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import os

RAIZ = Path(os.environ["CIFRAS_SIN_RESULT_RAIZ"]) if os.environ.get("CIFRAS_SIN_RESULT_RAIZ") else Path(__file__).resolve().parents[2]
RUTAS_GOBERNADAS = ("canon/", "forense/analisis/")
# ci-guardias/: censo de infraestructura de pruebas, no evidencia sobre
# México. canon/L0/: fragmentos de ADR (narrativa de gobernanza sobre el
# ACTO -- conteos de NC/FP/tests/celdas del propio cierre), no afirmaciones
# sustantivas que requieran trazar cada cifra a un RESULT; citan "RESULT"
# o "CALC" en prosa (sin el guion+id que este script exige) precisamente
# porque narran cuantos hubo, no el contenido de cada uno. Verificado
# contra ADR-260923-ASTRA5-U4-TECNOLOGIA-1f30-01.md: "Seis RESULT sellados"
# es prosa administrativa, no una cifra sustantiva sin trazar.
RUTAS_EXCLUIDAS = ("forense/analisis/ci-guardias/", "canon/L0/")
EXTENSIONES = (".md", ".tsv", ".yaml", ".yml")
REPLAY_EVIDENCIA = RAIZ / "forense" / "replay-evidencia.tsv"

_CIFRA = re.compile(
    r"(?<![\w#-])"
    r"\d{1,3}(?:[.,\s]\d{3})*(?:[.,]\d+)?%?"
    r"(?![\w-])"
)
_RESULT_CITA = re.compile(r"\bRESULT-[A-Za-z0-9_.-]+")
_CALC_CITA = re.compile(r"\bCALC-[A-Za-z0-9_.-]+")


def _calc_ids_sellados() -> set[str]:
    """Lee forense/replay-evidencia.tsv con un lector de CSV (no awk por
    linea fisica -- §2 de las instrucciones del proyecto), devuelve el
    conjunto de calc_id con al menos una fila asentada."""
    if not REPLAY_EVIDENCIA.exists():
        return set()
    with REPLAY_EVIDENCIA.open(newline="", encoding="utf-8") as fh:
        lector = csv.DictReader(fh, delimiter="\t")
        return {fila["calc_id"] for fila in lector if fila.get("calc_id")}


def _es_ruido(token: str) -> bool:
    limpio = token.rstrip("%")
    return limpio.isdigit() and len(limpio) == 1


def cifras_en_linea(linea: str) -> list[str]:
    return [
        m.group(0)
        for m in _CIFRA.finditer(linea)
        if not _es_ruido(m.group(0))
    ]


def _git(*args: str) -> str:
    r = subprocess.run(
        ["git", *args], cwd=RAIZ, capture_output=True, text=True, check=False
    )
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.returncode}: {r.stderr.strip()}")
    return r.stdout


def _archivos_relevantes(base: str, merge: str) -> list[str]:
    salida = _git(
        "diff", "--diff-filter=AM", "--name-only", "--no-color", base, merge,
        "--", *RUTAS_GOBERNADAS,
    )
    return [
        ruta for ruta in salida.splitlines()
        if ruta.endswith(EXTENSIONES) and not ruta.startswith(RUTAS_EXCLUIDAS)
    ]


def _cifras_nuevas_de_archivo(base: str, merge: str, ruta: str) -> list[str]:
    diff = _git("diff", "-U0", "--no-color", base, merge, "--", ruta)
    cifras: list[str] = []
    for renglon in diff.splitlines():
        if not renglon.startswith("+") or renglon.startswith("+++"):
            continue
        cifras.extend(cifras_en_linea(renglon[1:]))
    return cifras


def _traza_de_archivo(merge: str, ruta: str, calc_sellados: set[str]) -> dict:
    try:
        contenido = _git("show", f"{merge}:{ruta}")
    except RuntimeError:
        return {"tiene_traza": False, "via": None, "calc_citados": []}
    if _RESULT_CITA.search(contenido):
        return {"tiene_traza": True, "via": "RESULT-*", "calc_citados": []}
    calc_citados = sorted(set(_CALC_CITA.findall(contenido)))
    calc_sellados_citados = [c for c in calc_citados if c in calc_sellados]
    if calc_sellados_citados:
        return {"tiene_traza": True, "via": "CALC-sellado-en-replay-evidencia", "calc_citados": calc_sellados_citados}
    return {"tiene_traza": False, "via": None, "calc_citados": calc_citados}


def analiza_rango(base: str, merge: str) -> dict:
    calc_sellados = _calc_ids_sellados()
    archivos = _archivos_relevantes(base, merge)
    detalle = []
    for ruta in archivos:
        cifras = _cifras_nuevas_de_archivo(base, merge, ruta)
        if not cifras:
            continue
        traza = _traza_de_archivo(merge, ruta, calc_sellados)
        detalle.append({
            "archivo": ruta,
            "cifras_nuevas": len(cifras),
            "tiene_traza": traza["tiene_traza"],
            "via_traza": traza["via"],
            "calc_sin_sellar_citados": traza["calc_citados"] if not traza["tiene_traza"] else [],
            "muestra_cifras": cifras[:8],
        })
    sin_traza = [d for d in detalle if not d["tiene_traza"]]
    return {
        "base": base,
        "merge": merge,
        "archivos_con_cifras_nuevas": len(detalle),
        "archivos_sin_result": len(sin_traza),
        "total_cifras_nuevas": sum(d["cifras_nuevas"] for d in detalle),
        "detalle_sin_result": sin_traza,
        "detalle_completo": detalle,
    }


def autoprueba() -> int:
    ok = True

    casos_cifra = [
        ("42 celdas utilizables (RESULT-ASTRA-DEMO-0001).", ["42"]),
        ("42 celdas utilizables, sin cita.", ["42"]),
        ("1. primer punto de una lista, 2) segundo punto.", []),
        ("PR #1085 fusionado 2026-09-23, ADR-260923-X-0001.", []),
    ]
    for texto, esperado in casos_cifra:
        obtenido = cifras_en_linea(texto)
        if obtenido != esperado:
            print(f"FALLO autoprueba(cifra): {texto!r} -> {obtenido}, esperado {esperado}")
            ok = False

    # El patron real: la cita RESULT vive en una linea distinta a la cifra.
    archivo_con_cita = "# Encabezado\nResultado sellado RESULT-DEMO-0001.\n\n| fila | 42 |\n"
    archivo_sin_cita = "# Encabezado\nResultado sellado, sin id citable.\n\n| fila | 42 |\n"
    if not _RESULT_CITA.search(archivo_con_cita):
        print("FALLO autoprueba(cita): no reconocio RESULT-DEMO-0001 en archivo multilinea")
        ok = False
    if _RESULT_CITA.search(archivo_sin_cita):
        print("FALLO autoprueba(cita): encontro una cita RESULT- que no existe")
        ok = False

    # El patron ENDIREH: sin "RESULT-" en prosa, pero con un CALC que SÍ
    # tiene fila en replay-evidencia.tsv -- no debe marcarse SIN-TRAZA.
    calc_sellados = {"CALC-DEMO-SELLADO-0001"}
    archivo_calc_sellado = "# Encabezado\n`CALC-DEMO-SELLADO-0001`, verify REPRODUCE.\n\n| fila | 42 |\n"
    archivo_calc_no_sellado = "# Encabezado\n`CALC-DEMO-HUERFANO-0001`, sin asiento.\n\n| fila | 42 |\n"
    if not _RESULT_CITA.search(archivo_calc_sellado):
        calc_citados = sorted(set(_CALC_CITA.findall(archivo_calc_sellado)))
        if not any(c in calc_sellados for c in calc_citados):
            print("FALLO autoprueba(traza-calc): no reconocio CALC-DEMO-SELLADO-0001 como traza valida")
            ok = False
    calc_citados_huerfano = sorted(set(_CALC_CITA.findall(archivo_calc_no_sellado)))
    if any(c in calc_sellados for c in calc_citados_huerfano):
        print("FALLO autoprueba(traza-calc): trato un CALC huerfano como sellado")
        ok = False

    if ok:
        print("AUTOPRUEBA VERDE: detector de cifras y de cita RESULT (por archivo, no por linea) correctos sobre casos conocidos")
        return 0
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("merge", nargs="?", help="SHA del commit de merge del PR")
    ap.add_argument("--base", help="SHA base explicito (default: merge^1)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--autoprueba", action="store_true")
    args = ap.parse_args()

    if args.autoprueba:
        return autoprueba()

    if not args.merge:
        ap.error("falta <merge-sha> (o usa --autoprueba)")

    base = args.base or f"{args.merge}^1"
    resultado = analiza_rango(base, args.merge)

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        print(f"RANGO {resultado['base']}..{resultado['merge']}")
        print(
            f"archivos_con_cifras_nuevas={resultado['archivos_con_cifras_nuevas']} "
            f"archivos_sin_result={resultado['archivos_sin_result']} "
            f"total_cifras_nuevas={resultado['total_cifras_nuevas']}"
        )
        for d in resultado["detalle_sin_result"]:
            calc_extra = f" calc_citados={d['calc_sin_sellar_citados']}" if d["calc_sin_sellar_citados"] else ""
            print(f"  SIN-TRAZA {d['archivo']} cifras_nuevas={d['cifras_nuevas']} muestra={d['muestra_cifras']}{calc_extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
