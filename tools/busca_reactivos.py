#!/usr/bin/env python3
"""ACTO MAESTRA33-E7 · MAPEADOR-1 — P1. Buscador genérico de reactivos.

A.8 midió (contra `a6d8504`) que ningún `tools/*.py` existente es genérico
ni reutilizable por celda: `etiqueta_v1_2.py`/`censo_r34_bc.py` derivan
columnas fijas, `barrido_enoe_*` trae listas de término congeladas en el
propio código. Este script es el primero pensado para consulta ad hoc,
repetida con formulaciones distintas (`mapea.md`, P2, corre ≥3 por celda).

Universo: las DOS capas de texto que A.8 confirmó existentes —
`data/inventario-reactivos-v1_2.tsv` (sucesor de v1_1 citado por el
encargo; mismas 178 246 filas / mismo payload_id·sha256_12·archivo_miembro·
variable_id·texto_reactivo·metodo·universo_declarado byte a byte, columna
`instrumento` más resuelta — ADR-216) y
`data/inventario-reactivos-ext-v1_0.tsv` (formatos estadísticos .dta/.sav/
.rdata, 63 345 filas, ADR-228). `--fuente` elige una o ambas (por defecto
ambas). Nunca se abre microdato: las dos tablas son metadato puro,
producido por actos anteriores.

Consulta: por palabras (`--palabra`, repetible, OR entre sí — mismo
convenio que `barrido_enoe_constructos.py::FILAS`, substring plegado a
minúsculas sin diacríticos) o por regex (`--regex`, `re.IGNORECASE`, sin
plegar acentos — el operador controla el patrón). Exactamente uno de los
dos modos, o ninguno si la invocación es solo de filtro. La búsqueda
corre sobre `texto_reactivo` + `variable_id` — un acierto en cualquiera
de los dos cuenta.

Filtros: `--encuesta` (substring plegado sobre `instrumento`), `--ola`
(substring plegado sobre `ola` **y** sobre `payload_id` — la columna
`ola` del inventario es hoy constante `NO_DETERMINADO` en las dos tablas,
así que el filtro solo es útil si también mira el nombre del payload,
donde el año/trimestre real suele vivir, p.ej. `2005trim1_csv.zip`,
`envipe2023_csv.zip`; declarado, no inventado), `--tipo` (substring
plegado sobre `metodo` — valores vistos: `INSPECT_ZIP/XLSX/CSV/XML` en
la tabla base, `INSPECT_STATA/SPSS/RDATA` en `-ext`; el .dta se reporta
como `INSPECT_STATA`, no `INSPECT_DTA` — vocabulario real, no traducido).

Salida: TSV con columnas `id encuesta ola tabla variable texto tipo
en_corpus`, escrito a mano por `'\t'.join(...)` — el módulo `csv` para
ESCRITURA corrompe los TSV de este proyecto cuando un campo trae tabs o
comillas (`ADR-123(h)`); para LECTURA sí se usa `csv.DictReader` sobre
las líneas sin `#`, mismo convenio que `tools/etiqueta_v1_2.py`.

  id        `<fuente>:<n>` — `n` = posición 1-indexada de la fila de dato
            (sin comentarios `#` ni cabecera) dentro de su archivo fuente;
            reproducible con
            `grep -v '^#' <archivo> | tail -n +2 | sed -n '<n>p'`.
  encuesta  columna `instrumento`.
  ola       columna `ola` (ver nota de arriba — casi siempre
            `NO_DETERMINADO`).
  tabla     columna `archivo_miembro`.
  variable  columna `variable_id`.
  texto     columna `texto_reactivo` (a menudo vacía — el extractor de
            metadato no siempre produce texto, ver cabecera de las
            tablas fuente; un candidato con `texto` vacío se identifica
            solo por `variable`/nombre de tabla, declarado en la salida).
  tipo      columna `metodo`.
  en_corpus `SI`/`NO` — cruce de `payload_id` contra el campo `archivo:`
            de `data/manifiesto.yaml` (mismo cruce que
            `tools/etiqueta_v1_2.py::carga_manifiesto`, misma clave).

A.13 — todo negativo declara cuántas filas examinó: la cabecera `#` de
la salida trae el universo (archivo por archivo, con conteo) SIEMPRE,
incluso con cero candidatos — un `NO-ENCONTRADO` sin esa línea no es un
`NO-ENCONTRADO`, es un comando que no se sabe si corrió.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

FUENTES = {
    "v1_2": REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv",
    "ext": REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv",
}
MANIFIESTO = REPO_ROOT / "data" / "manifiesto.yaml"

COLUMNAS_SALIDA = ["id", "encuesta", "ola", "tabla", "variable", "texto", "tipo", "en_corpus"]


def plegar(s: str) -> str:
    """Minúsculas sin diacríticos — mismo convenio que barrido_enoe_constructos.py::plegar."""
    s = unicodedata.normalize("NFD", s or "")
    return "".join(c for c in s.lower() if unicodedata.category(c) != "Mn")


def lee_filas(path: Path) -> list[dict]:
    """TSV plano sin comillas CSV: líneas `#` fuera, luego csv.DictReader.
    Mismo convenio de lectura que tools/etiqueta_v1_2.py::lee_filas."""
    with path.open(encoding="utf-8") as f:
        sin_comentario = (l for l in f if not l.startswith("#"))
        return list(csv.DictReader(sin_comentario, delimiter="\t"))


def carga_manifiesto(path: Path) -> dict[str, dict]:
    """payload_id (== campo `archivo:`) -> entrada. Mismo cruce que
    tools/etiqueta_v1_2.py::carga_manifiesto."""
    with path.open(encoding="utf-8") as f:
        entradas = yaml.safe_load(f)
    return {e["archivo"]: e for e in entradas if isinstance(e, dict) and e.get("archivo")}


def construye_filtro(args: argparse.Namespace):
    palabras_plegadas = [plegar(p) for p in (args.palabra or [])]
    regex = re.compile(args.regex, re.IGNORECASE) if args.regex else None
    encuesta_f = plegar(args.encuesta) if args.encuesta else None
    ola_f = plegar(args.ola) if args.ola else None
    tipo_f = plegar(args.tipo) if args.tipo else None

    def coincide(row: dict) -> bool:
        if encuesta_f and encuesta_f not in plegar(row["instrumento"]):
            return False
        if ola_f and ola_f not in plegar(row["ola"]) and ola_f not in plegar(row["payload_id"]):
            return False
        if tipo_f and tipo_f not in plegar(row["metodo"]):
            return False
        texto, variable = row["texto_reactivo"] or "", row["variable_id"] or ""
        if palabras_plegadas:
            tp, vp = plegar(texto), plegar(variable)
            return any(p in tp or p in vp for p in palabras_plegadas)
        if regex:
            return bool(regex.search(texto) or regex.search(variable))
        return True  # solo filtros, sin consulta de texto

    return coincide


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Busca reactivos por palabras/regex sobre texto_reactivo + variable_id, "
                    "con filtros encuesta/ola/tipo. Ver docstring del módulo para el vocabulario "
                    "real de cada filtro (A.4).")
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--palabra", action="append",
                      help="Término a buscar (repetible; OR entre varios). Plegado: "
                          "minúsculas, sin acentos, substring.")
    modo.add_argument("--regex", help="Patrón regex (re.IGNORECASE, sin plegar acentos).")
    ap.add_argument("--encuesta", help="Substring plegado sobre la columna instrumento.")
    ap.add_argument("--ola", help="Substring plegado sobre ola y payload_id (ver docstring).")
    ap.add_argument("--tipo", help="Substring plegado sobre metodo (INSPECT_ZIP/XLSX/CSV/XML/"
                                   "STATA/SPSS/RDATA).")
    ap.add_argument("--fuente", choices=["v1_2", "ext", "ambas"], default="ambas",
                    help="Qué tabla(s) examinar (por defecto ambas).")
    ap.add_argument("--limite", type=int, default=500,
                    help="Máximo de candidatas a listar (por defecto 500; el total real de "
                        "aciertos se declara aparte, nunca se trunca en silencio).")
    ap.add_argument("--salida", type=Path, default=None,
                    help="Ruta de archivo TSV de salida (por defecto: stdout).")
    args = ap.parse_args(argv)

    if not any([args.palabra, args.regex, args.encuesta, args.ola, args.tipo]):
        ap.error("da al menos un modo de consulta (--palabra/--regex) o un filtro "
                 "(--encuesta/--ola/--tipo) -- sin ninguno, el comando volcaría el corpus entero.")

    fuentes = list(FUENTES) if args.fuente == "ambas" else [args.fuente]
    for f in fuentes:
        if not FUENTES[f].exists():
            print(f"ERROR: falta {FUENTES[f]} -- 0 filas examinadas no es un NO-ENCONTRADO (A.13), "
                 f"es un comando que no corrió.", file=sys.stderr)
            return 2

    coincide = construye_filtro(args)
    manifiesto = carga_manifiesto(MANIFIESTO) if MANIFIESTO.exists() else {}

    universo_partes = []
    candidatas = []
    for f in fuentes:
        filas = lee_filas(FUENTES[f])
        universo_partes.append(f"{f}={len(filas)}")
        for n, row in enumerate(filas, start=1):
            if coincide(row):
                candidatas.append((f, n, row))

    total_candidatas = len(candidatas)
    mostradas = candidatas[: args.limite]

    banner = [
        f"# tools/busca_reactivos.py -- {date.today().isoformat()}",
        f"# comando: {' '.join(['busca_reactivos.py'] + (argv if argv is not None else sys.argv[1:]))}",
        f"# universo examinado (A.13): {', '.join(universo_partes)} -- "
        f"total {sum(int(p.split('=')[1]) for p in universo_partes)} filas",
        f"# candidatas: {total_candidatas} total, mostrando {len(mostradas)} "
        f"(--limite {args.limite})",
    ]

    salida = args.salida.open("w", encoding="utf-8") if args.salida else sys.stdout
    try:
        for linea in banner:
            salida.write(linea + "\n")
        salida.write("\t".join(COLUMNAS_SALIDA) + "\n")
        for fuente, n, row in mostradas:
            en_corpus = "SI" if row["payload_id"] in manifiesto else "NO"
            fila_salida = [
                f"{fuente}:{n}",
                row["instrumento"],
                row["ola"],
                row["archivo_miembro"],
                row["variable_id"],
                row["texto_reactivo"],
                row["metodo"],
                en_corpus,
            ]
            salida.write("\t".join(fila_salida) + "\n")
    finally:
        if args.salida:
            salida.close()

    for linea in banner:
        print(linea, file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
