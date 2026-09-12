#!/usr/bin/env python3
"""Publica un overlay incremental de texto acreditado para reactivos.

Lee únicamente metadatos ya indexados y documentación pública. Nunca abre
valores de microdatos. Las tablas históricas conservan orden y citas por fila;
cada fila del overlay apunta a su ``id_origen`` estable (fuente + posición).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
import tempfile
import unicodedata
import zipfile
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = REPO_ROOT / "data" / "raw"
OUT_PATH = REPO_ROOT / "data" / "inventario-reactivos-contexto-v1_0.tsv"
SOURCES_PATH = REPO_ROOT / "data" / "reactivos-contexto-fuentes-v1_0.tsv"
VERIFIED_PATH = REPO_ROOT / "data" / "reactivos-contexto-verificados-v1_0.tsv"
FD_EXT_PATH = REPO_ROOT / "data" / "inventario-fd-ext-v1_0.tsv"
CACHE_DIR = REPO_ROOT / "data" / ".reactivos-contexto-cache"
EXTRACTOR_VERSION = "reactivos-contexto-1.0.0"

METADATA_SOURCES = {
    "v1_2": REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv",
    "ext": REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv",
}
PRIORITY = ("envipe", "ennvih", "encuci", "enif", "ensafi")

OUT_FIELDS = [
    "id_origen", "payload_id", "sha256_12", "instrumento", "ola",
    "archivo_miembro", "variable_id", "texto_reactivo", "texto_tipo",
    "contexto_busqueda", "metodo", "universo_declarado", "fuente_texto",
    "fuente_sha256_12", "referencia_fuente",
]

ID_LABELS = {"mnemonico", "nemonico", "nombre de la columna", "nombre", "clave", "variable"}
TEXT_LABELS = {"pregunta y categoria", "pregunta", "descripcion del contenido del campo",
               "descripcion", "etiqueta", "observaciones"}
TABLE_TOKENS = ("tmodulo", "tmodvic", "tpervic", "tvivienda", "tviviend",
                "thogar", "tsdem", "tmodulo1", "tmodulo2", "tmodulo3")


def sanitize(value) -> str:
    return " ".join(str(value or "").replace("\t", " ").split())


def fold(value) -> str:
    text = unicodedata.normalize("NFKD", sanitize(value).lower())
    return "".join(char for char in text if not unicodedata.combining(char))


def compact(value) -> str:
    return re.sub(r"[^a-z0-9]", "", fold(value))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader((line for line in handle if not line.startswith("#")), delimiter="\t"))


def instrument_for(row: dict) -> str:
    current = row["instrumento"].lower()
    payload = row["payload_id"].lower()
    if payload.startswith("ennvih/"):
        match = re.search(r"(?:ehh|eloc)(02|05|09)", payload)
        return f"ennvih20{match.group(1)}" if match else "ennvih"
    return current


def year_for(instrument: str, current: str) -> str:
    match = re.search(r"(19|20)\d{2}", instrument)
    return match.group(0) if match else current


def selected(instrument: str, payload: str, objects: list[str]) -> bool:
    haystack = fold(f"{instrument} {payload}")
    return any(fold(obj) in haystack for obj in objects)


def find_header(values: tuple) -> tuple[int | None, int | None]:
    normalized = [fold(v).rstrip(":.") for v in values]
    id_col = next((i for i, value in enumerate(normalized) if value in ID_LABELS), None)
    text_col = next((i for i, value in enumerate(normalized) if value in TEXT_LABELS), None)
    return id_col, text_col


def extract_sheet(sheet, source: str, member: str) -> list[dict]:
    result = []
    id_col = text_col = None
    pending_text = ""
    for row_number, values in enumerate(sheet.iter_rows(values_only=True), 1):
        new_id, new_text = find_header(values)
        if new_id is not None and new_text is not None:
            id_col, text_col, pending_text = new_id, new_text, ""
            continue
        if id_col is None or text_col is None:
            continue
        variable = sanitize(values[id_col] if id_col < len(values) else "")
        text = sanitize(values[text_col] if text_col < len(values) else "")
        if text and not variable:
            if not re.fullmatch(r"[\(\[]\d+[\)\]]", text):
                pending_text = text
            continue
        if not variable or re.fullmatch(r"[\(\[]\d+[\)\]]", variable):
            continue
        accredited = text or pending_text
        pending_text = ""
        if accredited:
            result.append({
                "variable_id": variable,
                "texto_reactivo": accredited,
                "texto_tipo": "PREGUNTA_DICCIONARIO",
                "contexto_busqueda": "",
                "fuente_texto": source,
                "referencia_fuente": f"miembro={member};hoja={sheet.title};fila={row_number}",
                "tabla_documental": sheet.title,
            })
    return result


def extract_xlsx(content_or_path, source: str, member: str | None = None) -> list[dict]:
    from openpyxl import load_workbook
    workbook = load_workbook(content_or_path, read_only=True, data_only=True)
    try:
        return [item for sheet in workbook.worksheets
                for item in extract_sheet(sheet, source, member or source)]
    finally:
        workbook.close()


def extract_xls(path: Path, source: str) -> list[dict]:
    import xlrd
    workbook = xlrd.open_workbook(str(path))
    result = []
    for raw_sheet in workbook.sheets():
        class SheetAdapter:
            title = raw_sheet.name

            @staticmethod
            def iter_rows(values_only=True):
                return (tuple(raw_sheet.row_values(index)) for index in range(raw_sheet.nrows))

        result.extend(extract_sheet(SheetAdapter(), source, source))
    return result


def page_map(path: Path, member: str | None, variables: set[str]) -> dict[str, int]:
    import pdfplumber
    if member:
        with zipfile.ZipFile(path) as archive:
            handle = io.BytesIO(archive.read(member))
        pdf_context = pdfplumber.open(handle)
    else:
        pdf_context = pdfplumber.open(str(path))
    found = {}
    with pdf_context as pdf:
        for page_number, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            for variable in variables - found.keys():
                if re.search(rf"(?<![A-Za-z0-9_]){re.escape(variable)}(?![A-Za-z0-9_])", text, re.I):
                    found[variable] = page_number
    return found


def extract_fd_pdf_index(path: Path, source: str, instrument: str) -> list[dict]:
    indexed = [row for row in read_tsv(FD_EXT_PATH)
               if row["payload_id"] == source and row["instrumento"].lower() == instrument.lower()]
    by_member: dict[str, list[dict]] = defaultdict(list)
    for row in indexed:
        by_member[row["archivo_miembro"]].append(row)
    result = []
    for member, rows in by_member.items():
        zip_member = member if path.suffix.lower() == ".zip" else None
        located = page_map(path, zip_member, {row["variable_id"] for row in rows})
        for row in rows:
            page = located.get(row["variable_id"])
            if not page:
                continue
            result.append({
                "variable_id": row["variable_id"],
                "texto_reactivo": row["texto_reactivo"],
                "texto_tipo": "PREGUNTA_DICCIONARIO",
                "contexto_busqueda": "",
                "fuente_texto": source,
                "referencia_fuente": f"miembro={member};pagina={page}",
                "tabla_documental": member,
            })
    return result


def extract_source(path: Path, row: dict) -> list[dict]:
    fmt = row["formato"]
    source = row["fuente_texto"]
    if fmt == "xlsx":
        return extract_xlsx(path, source)
    if fmt == "xls":
        return extract_xls(path, source)
    if fmt == "zip_xlsx":
        result = []
        with zipfile.ZipFile(path) as archive:
            for member in archive.namelist():
                if member.lower().endswith(".xlsx"):
                    result.extend(extract_xlsx(io.BytesIO(archive.read(member)), source, member))
        return result
    if fmt == "fd_pdf_index":
        return extract_fd_pdf_index(path, source, row["instrumento"])
    raise ValueError(f"formato no soportado: {fmt}")


def cached_extract(path: Path, row: dict, cache_dir: Path) -> tuple[list[dict], bool, str]:
    digest = sha256_file(path)
    key_material = f"{EXTRACTOR_VERSION}\0{row['formato']}\0{digest}".encode()
    key = hashlib.sha256(key_material).hexdigest()
    cache_path = cache_dir / f"{key}.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8")), True, digest
    extracted = extract_source(path, row)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(extracted, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return extracted, False, digest


def compatible_table(member: str, documented: str) -> bool:
    left, right = compact(member), compact(documented)
    return any(token in left and token in right for token in TABLE_TOKENS)


def choose_candidate(candidates: list[dict], member: str) -> dict | None:
    compatible = [item for item in candidates if compatible_table(member, item["tabla_documental"])]
    pool = compatible or candidates
    distinct = {(item["texto_reactivo"], item["fuente_texto"], item["referencia_fuente"]): item
                for item in pool}
    if len(distinct) == 1:
        return next(iter(distinct.values()))
    same_text = {item["texto_reactivo"] for item in pool}
    return pool[0] if len(same_text) == 1 else None


def verified_candidates(path: Path) -> list[dict]:
    result = []
    for row in read_tsv(path):
        source_path = RAW_ROOT / row["fuente_texto"]
        if not source_path.exists():
            raise FileNotFoundError(source_path)
        reference = (f"pagina={row['pagina']};seccion={row['seccion']}"
                     if row["pagina"] else row["seccion"])
        result.append({
            **row,
            "tabla_documental": row["seccion"],
            "referencia_fuente": reference,
            "fuente_sha256_12": sha256_file(source_path)[:12],
            "manual": True,
        })
    return result


def write_output(path: Path, rows: list[dict], summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", newline="", dir=path.parent,
                prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            tmp_path = Path(handle.name)
            handle.write("# data/inventario-reactivos-contexto-v1_0.tsv -- sucesor overlay; no reordena fuentes historicas\n")
            handle.write("# " + json.dumps(summary, ensure_ascii=False, sort_keys=True) + "\n")
            handle.write("\t".join(OUT_FIELDS) + "\n")
            for row in rows:
                handle.write("\t".join(sanitize(row.get(field, "")) for field in OUT_FIELDS) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--objeto", action="append", help="Instrumento/familia o payload; repetible")
    parser.add_argument("--salida", type=Path, default=OUT_PATH)
    parser.add_argument("--fuentes", type=Path, default=SOURCES_PATH)
    parser.add_argument("--verificados", type=Path, default=VERIFIED_PATH)
    parser.add_argument("--cache-dir", type=Path, default=CACHE_DIR)
    args = parser.parse_args(argv)
    objects = args.objeto or list(PRIORITY)

    metadata = []
    for source_key, path in METADATA_SOURCES.items():
        for position, row in enumerate(read_tsv(path), 1):
            instrument = instrument_for(row)
            if selected(instrument, row["payload_id"], objects):
                metadata.append((source_key, position, instrument, row))

    candidates: dict[tuple[str, str], list[dict]] = defaultdict(list)
    cache_hits = cache_misses = 0
    source_hashes = {}
    for source in read_tsv(args.fuentes):
        if not selected(source["instrumento"], source["fuente_texto"], objects):
            continue
        path = RAW_ROOT / source["fuente_texto"]
        if not path.exists():
            continue
        extracted, hit, digest = cached_extract(path, source, args.cache_dir)
        cache_hits += int(hit)
        cache_misses += int(not hit)
        source_hashes[source["fuente_texto"]] = digest[:12]
        for item in extracted:
            item["fuente_sha256_12"] = digest[:12]
            candidates[(source["instrumento"].lower(), item["variable_id"].lower())].append(item)

    for item in verified_candidates(args.verificados):
        if selected(item["instrumento"], item["fuente_texto"], objects):
            key = (item["instrumento"].lower(), item["variable_id"].lower())
            candidates[key].insert(0, item)

    output = []
    unresolved = 0
    for source_key, position, instrument, row in metadata:
        native_text = sanitize(row["texto_reactivo"])
        candidate = None
        if native_text:
            candidate = {
                "texto_reactivo": native_text,
                "texto_tipo": "ETIQUETA_VARIABLE",
                "contexto_busqueda": "",
                "fuente_texto": row["payload_id"],
                "fuente_sha256_12": row["sha256_12"],
                "referencia_fuente": f"miembro={row['archivo_miembro']};metadato_nativo",
            }
        else:
            pool = candidates.get((instrument.lower(), row["variable_id"].lower()), [])
            manual = [item for item in pool if item.get("manual")]
            candidate = manual[0] if manual else choose_candidate(pool, row["archivo_miembro"])
        if candidate is None:
            unresolved += 1
            continue
        output.append({
            "id_origen": f"{source_key}:{position}",
            "payload_id": row["payload_id"],
            "sha256_12": row["sha256_12"],
            "instrumento": instrument,
            "ola": year_for(instrument, row["ola"]),
            "archivo_miembro": row["archivo_miembro"],
            "variable_id": row["variable_id"],
            "metodo": row["metodo"],
            "universo_declarado": row["universo_declarado"],
            **{key: candidate.get(key, "") for key in (
                "texto_reactivo", "texto_tipo", "contexto_busqueda", "fuente_texto",
                "fuente_sha256_12", "referencia_fuente")},
        })

    output.sort(key=lambda row: (row["id_origen"].split(":")[0], int(row["id_origen"].split(":")[1])))
    summary = {
        "extractor_version": EXTRACTOR_VERSION,
        "objetos": objects,
        "filas_metadato_perimetro": len(metadata),
        "filas_con_texto_publicadas": len(output),
        "filas_sin_texto_residual": unresolved,
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
        "fuentes": source_hashes,
    }
    write_output(args.salida, output, summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
