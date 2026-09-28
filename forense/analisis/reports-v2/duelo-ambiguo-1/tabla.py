#!/usr/bin/env python3
"""Deriva la tabla de duelo desde juicios explícitos y comprueba sus trazas.

No decide dictámenes, no lee microdatos y no infiere respaldo por líneas o
palabras del report. --check compara el derivado sin escribir archivos.
"""

import argparse
import collections
import csv
import hashlib
import io
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit


BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
ORIGINAL = ROOT / "corpus/reports/Ausencia_sin_certeza__duelo_y_pérdida_ambigua_en_familias_de_personas_desaparecidas_en_México.md"
REPORT = ROOT / "corpus/reports-v2" / ORIGINAL.name
MAP = ROOT / "canon/mapa-dominios-v1_1.tsv"
DECISIONS = BASE / "decisiones.json"
SOURCES = BASE / "fuentes.md"
TABLE = BASE / "tabla-afirmaciones.tsv"
FIELDS = ("id", "mapa_id", "localizador", "afirmacion", "dictamen", "evidencia", "razon")
VERDICTS = {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
SOURCE_ID = re.compile(r"(?<![\w-])F\d{2,}(?![\w-])")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_links(path):
    """Comprueba destino sintáctico y existencia local; no simula lectura web."""
    for raw in MARKDOWN_LINK.findall(path.read_text(encoding="utf-8")):
        target = raw.strip().split(" ", 1)[0].strip("<>")
        if target.startswith(("https://", "http://")):
            parsed = urlsplit(target)
            require(bool(parsed.netloc), f"{path}: URL incompleta: {target}")
        elif not target.startswith("#"):
            local = unquote(target.split("#", 1)[0])
            require(bool(local) and (path.parent / local).exists(),
                    f"{path}: enlace local inexistente: {target}")


def source_ids():
    require(SOURCES.is_file(), f"Faltan fuentes: {SOURCES}")
    # La primera columna de la tabla humana es el identificador de fuente.
    ids = re.findall(r"^\|\s*(F\d{2,})\s*\|", SOURCES.read_text(encoding="utf-8"), re.M)
    require(len(ids) == len(set(ids)), "ID de fuente repetido")
    return set(ids)


def table_text():
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))
    require(decisions.get("original") == str(ORIGINAL.relative_to(ROOT)), "Ruta v1 incompatible")
    require(decisions.get("mapa") == str(MAP.relative_to(ROOT)), "Ruta de mapa incompatible")
    require(decisions.get("original_sha256") == digest(ORIGINAL), "Cambió el original")
    require(decisions.get("mapa_sha256") == digest(MAP), "Cambió el mapa")

    with MAP.open(encoding="utf-8", newline="") as stream:
        mapped = {r["id_afirmacion"]: r for r in csv.DictReader(stream, delimiter="\t")
                  if r["report"] == decisions["original"]}
    require(len(mapped) == 41, f"Se esperaban 41 filas de mapa, hay {len(mapped)}")
    require(all(r["report_sha256"] == decisions["original_sha256"] for r in mapped.values()),
            "Mapa y v1 no comparten identidad")

    rows = decisions.get("decisiones")
    require(isinstance(rows, list) and rows, "Faltan decisiones explícitas")
    ids = [r.get("id") for r in rows]
    require(len(ids) == len(set(ids)), "ID de decisión repetido")
    linked = [r.get("mapa_id") for r in rows if r.get("mapa_id")]
    require(collections.Counter(linked) == collections.Counter({key: 1 for key in mapped}),
            "Cobertura de mapa: ID ausente, ajeno o duplicado")
    known_sources = source_ids()
    for row in rows:
        require(all(key in row for key in FIELDS), f"Columnas incompletas: {row.get('id')}")
        require(all(str(row[key]).strip() for key in FIELDS if key != "mapa_id"),
                f"Campo vacío: {row.get('id')}")
        require(row["dictamen"] in VERDICTS, f"Dictamen desconocido: {row['id']}")
        if row["mapa_id"]:
            require(re.fullmatch(r"DUEL-\d{3}", row["id"]) is not None,
                    f"Decisión de mapa sin ID local estable: {row['id']}")
        if not row["mapa_id"]:
            require(re.fullmatch(r"DUEL-X\d{2,}", row["id"]) is not None,
                    f"Extra sin ID propio: {row['id']}")
        unknown = set(SOURCE_ID.findall(row["evidencia"])) - known_sources
        require(not unknown, f"Fuente sin ficha en {row['id']}: {sorted(unknown)}")
        # El juicio sigue en decisiones.json; el verificador solo exige traza y razón.
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows({key: "" if row[key] is None else row[key] for key in FIELDS} for row in rows)
    return out.getvalue(), len(mapped), len(rows) - len(mapped)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verifica sin escribir")
    args = parser.parse_args()
    rendered, nmap, nextra = table_text()
    if args.check:
        require(TABLE.is_file() and TABLE.read_text(encoding="utf-8") == rendered,
                "Tabla ausente o desactualizada; ejecute tabla.py")
    else:
        TABLE.write_text(rendered, encoding="utf-8")
    check_links(SOURCES)
    if REPORT.is_file():
        report = REPORT.read_text(encoding="utf-8")
        require("tabla-afirmaciones.tsv" in report and "fuentes.md" in report,
                "Report sin enlaces a tabla y fuentes")
        check_links(REPORT)
        require(set(SOURCE_ID.findall(report)) <= source_ids(), "Report cita Fnn sin ficha")
    print(f"OK: {nmap} filas de mapa, {nextra} extras; tabla {'verificada' if args.check else 'generada'}")


if __name__ == "__main__":
    main()
