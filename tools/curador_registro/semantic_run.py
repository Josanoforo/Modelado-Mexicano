#!/usr/bin/env python3
"""Ejecuta materialmente la cola semántica candidata, sin integrar por defecto.

La ejecución mantiene tres expedientes separados:

* observación cegada: abre referencias/activos/localizadores sin conocer N ni relación;
* curaduría: contrasta el reporte neutral con la relación y su acción original;
* supervisión: relee todos los archivos y deriva el estado sin aceptar booleanos del worker.

Los payloads de red se mantienen en memoria; solo se versionan resultados descriptivos,
hashes completos cuando fue posible obtener el objeto completo y hashes de fragmentos
claramente rotulados cuando el servidor no permitió una descarga acotada.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import subprocess
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

import yaml

try:
    from .pdf_extract import extract_pdf
except ImportError:
    from pdf_extract import extract_pdf

# resolver_raiz/RAIZ_INTEGRADA se reutilizan de tests/manifiesto.py -- no se
# reimplementa la resolución de raíces aquí. El módulo se localiza por la
# ubicación real de este archivo (no por un `repo` de ejecución, que en una
# prueba puede ser un fixture sintético sin tests/manifiesto.py propio).
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tests"))
import manifiesto  # noqa: E402


ENGINE_VERSION = "2.0.0"
UNKNOWN = {"", "NO_DETERMINADO", "NO_APLICA", "—"}
TERMINAL_STATES = {
    "EJECUTADA_CON_RESULTADO",
    "NO_ALCANZO_TRAS_INTENTOS",
    "FUENTE_ABIERTA_SIN_OBJETO_REQUERIDO",
    "BLOQUEADA_INPUT_FALTANTE",
    "REQUIERE_DECISION_HUMANA",
    "NO_CORRIDA",
}
SEMANTIC_TYPES = {"BUSQUEDA_DIRIGIDA", "CURADURIA_FUENTE", "ANALISIS_MEDICION"}
DIRECT_CONTENT = (
    "application/pdf", "application/zip", "application/x-zip",
    "application/vnd.openxmlformats", "text/csv", "application/csv",
    "application/octet-stream",
)
LINK_TERMS = re.compile(
    r"codebook|questionnaire|cuestionario|dictionary|diccionario|manual|microdat|download|descarg|data",
    re.I,
)


class SemanticRunError(ValueError):
    pass


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def stable_id(prefix: str, *parts: Any) -> str:
    return prefix + "-" + sha256_bytes(canonical_bytes(list(parts)))[:24]


def read_tsv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise SemanticRunError(f"input inexistente: {path}")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def index_unique(rows: Iterable[dict[str, str]], field: str, label: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row.get(field, "")
        if not key or key in result:
            raise SemanticRunError(f"{label}: {field} vacío o duplicado: {key!r}")
        result[key] = row
    return result


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^A-Z0-9]+", "_", value.upper()).strip("_")


def baseline_hashes(registry: Path) -> dict[str, str]:
    manifest_path = registry / "baseline.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    result = {"baseline.json": sha256(manifest_path)}
    for filename, declaration in manifest.get("archivos", {}).items():
        path = registry / filename
        if not path.is_file() or sha256(path) != declaration.get("sha256"):
            raise SemanticRunError(f"baseline inválido: {filename}")
        if len(read_tsv(path)) != declaration.get("filas"):
            raise SemanticRunError(f"conteo baseline inválido: {filename}")
        result[filename] = sha256(path)
    return result


def snapshot_hash(universe: Path) -> str:
    snapshot = json.loads((universe / "snapshot-t0.json").read_text(encoding="utf-8"))
    result = snapshot.get("snapshot_t0_sha256", "")
    if not result:
        raise SemanticRunError("snapshot sin hash")
    for filename, expected in snapshot.get("hashes_outputs", {}).items():
        path = universe / filename
        if not path.is_file() or sha256(path) != expected:
            raise SemanticRunError(f"output T0 no reconcilia: {filename}")
    return result


def main_ref_parts(value: str) -> tuple[Path, int | None, int | None]:
    spec = value.removeprefix("MAIN:")
    match = re.search(r":L(\d+)(?:-L?(\d+))?$", spec)
    if not match:
        return Path(spec), None, None
    return Path(spec[: match.start()]), int(match.group(1)), int(match.group(2) or match.group(1))


def trim_text(value: str, limit: int = 1200) -> str:
    return re.sub(r"\s+", " ", value).strip()[:limit]


def exact_ref_excerpt(path: Path, start: int | None, end: int | None) -> tuple[str, str]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig", errors="replace")
    lines = text.splitlines()
    if start is None:
        excerpt = "\n".join(lines[: min(len(lines), 40)])
        frontier = f"primeras {min(len(lines), 40)} de {len(lines)} líneas; hash del objeto completo"
    else:
        excerpt = "\n".join(lines[max(0, start - 1): min(len(lines), end or start)])
        frontier = f"líneas {start}-{end} de {len(lines)}; hash del objeto completo"
    return trim_text(excerpt), frontier


def html_links(body: bytes, base_url: str) -> list[str]:
    text = body.decode("utf-8", errors="replace")
    result: list[str] = []
    for href, label in re.findall(r"(?is)<a[^>]+href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", text):
        label = re.sub(r"<[^>]+>", " ", html.unescape(label))
        absolute = urllib.parse.urljoin(base_url, html.unescape(href))
        if absolute.startswith(("http://", "https://")) and LINK_TERMS.search(absolute + " " + label):
            result.append(absolute)
    return sorted(dict.fromkeys(result))


def fetch_once(url: str, order: int, max_bytes: int = 500_000) -> tuple[dict[str, Any], bytes]:
    request = urllib.request.Request(url, headers={"User-Agent": "ModeladoMexicano-SemanticAudit/2.0", "Range": f"bytes=0-{max_bytes}"})
    try:
        with urllib.request.urlopen(request, timeout=8) as response:
            body = response.read(max_bytes + 1)
            truncated = len(body) > max_bytes
            if truncated:
                body = body[:max_bytes]
            content_type = response.headers.get("Content-Type", "NO_DETERMINADO").split(";", 1)[0].strip().lower()
            declared_length = response.headers.get("Content-Length", "NO_DETERMINADO")
            content_range = response.headers.get("Content-Range", "")
            total_match = re.search(r"/(\d+)$", content_range)
            if response.status == 206:
                complete = bool(total_match and int(total_match.group(1)) <= len(body))
            else:
                complete = not truncated and (
                    declared_length == "NO_DETERMINADO" or
                    (declared_length.isdigit() and int(declared_length) <= len(body))
                )
            record = {
                "orden": order,
                "localizador": url,
                "resultado_http_archivo_error": f"HTTP_{response.status}",
                "url_final": response.geturl(),
                "content_type": content_type or "NO_DETERMINADO",
                "bytes_observados": len(body),
                "objeto_completo": "SI" if complete else "NO",
                "sha256_objeto": sha256_bytes(body) if complete else "NO_DETERMINADO",
                "sha256_fragmento": "NO_APLICA" if complete else sha256_bytes(body),
                "resultado_literal": trim_text(body.decode("utf-8", errors="replace"), 800),
            }
            return record, body
    except urllib.error.HTTPError as exc:
        body = exc.read(8192)
        return ({
            "orden": order, "localizador": url,
            "resultado_http_archivo_error": f"HTTP_{exc.code}", "url_final": exc.geturl(),
            "content_type": exc.headers.get("Content-Type", "NO_DETERMINADO").split(";", 1)[0],
            "bytes_observados": len(body), "objeto_completo": "NO",
            "sha256_objeto": "NO_DETERMINADO", "sha256_fragmento": sha256_bytes(body) if body else "NO_DETERMINADO",
            "resultado_literal": trim_text(body.decode("utf-8", errors="replace"), 800) or str(exc),
        }, body)
    except Exception as exc:
        return ({
            "orden": order, "localizador": url,
            "resultado_http_archivo_error": f"ERROR_{type(exc).__name__}", "url_final": "NO_DETERMINADO",
            "content_type": "NO_DETERMINADO", "bytes_observados": 0, "objeto_completo": "NO",
            "sha256_objeto": "NO_DETERMINADO", "sha256_fragmento": "NO_DETERMINADO",
            "resultado_literal": trim_text(str(exc)),
        }, b"")


def fetch_declared(url: str) -> list[dict[str, Any]]:
    first, body = fetch_once(url, 1)
    attempts = [first]
    if first["resultado_http_archivo_error"].startswith("ERROR_") or first["resultado_http_archivo_error"].startswith("HTTP_4") or first["resultado_http_archivo_error"].startswith("HTTP_5"):
        second, _ = fetch_once(url, 2)
        attempts.append(second)
        return attempts
    if first["content_type"] in {"text/html", "application/xhtml+xml"}:
        links = html_links(body, first.get("url_final") or url)
        if links:
            second, _ = fetch_once(links[0], 2)
            second["vinculo_explicito_desde_intento"] = 1
            attempts.append(second)
    return attempts


def xlsx_structure(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        texts: list[str] = []
        if "xl/sharedStrings.xml" in names:
            raw = archive.read("xl/sharedStrings.xml").decode("utf-8", errors="replace")
            texts.extend(html.unescape(re.sub(r"<[^>]+>", " ", raw)).split())
        sheets = [name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")]
        return trim_text(f"miembros={len(names)}; hojas_xml={';'.join(sheets)}; cadenas_compartidas={' '.join(texts[:120])}", 1800)


def zip_structure(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        headers: list[str] = []
        for name in names:
            if len(headers) >= 5 or not name.lower().endswith((".csv", ".txt")):
                continue
            try:
                with archive.open(name) as handle:
                    first = handle.readline(65536).decode("utf-8-sig", errors="replace")
                headers.append(f"{name}: {trim_text(first, 500)}")
            except Exception as exc:
                headers.append(f"{name}: ERROR_APERTURA_{type(exc).__name__}")
        return trim_text(f"miembros={len(names)}; nombres={';'.join(names[:80])}; encabezados={' | '.join(headers)}", 3000)


def open_local_object(path: Path, label: str, pdf_mode: str = "union", ruta_declarada: str | None = None) -> dict[str, str]:
    if not path.is_file():
        return {"objeto": label, "ruta": ruta_declarada or str(path), "resultado": "ARCHIVO_NO_EXISTE", "sha256": "NO_DETERMINADO", "descripcion": ""}
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            extraction = extract_pdf(path, mode=pdf_mode)
            description = trim_text(extraction.text, 3000)
            result = "ABIERTO_PDF_TEXTO"
        elif suffix == ".xlsx":
            description, result = xlsx_structure(path), "ABIERTO_XLSX_ESTRUCTURA"
        elif suffix == ".zip":
            description, result = zip_structure(path), "ABIERTO_ZIP_ESTRUCTURA"
        elif suffix in {".md", ".txt", ".tsv", ".csv", ".html", ".json", ".yaml", ".yml"}:
            description = trim_text(path.read_text(encoding="utf-8-sig", errors="replace"), 3000)
            result = "ABIERTO_TEXTO"
        else:
            description = f"formato={suffix or 'SIN_EXTENSION'} tamaño={path.stat().st_size}"
            result = "ABIERTO_BINARIO_CARACTERIZADO"
    except Exception as exc:
        description, result = trim_text(str(exc)), f"ERROR_APERTURA_{type(exc).__name__}"
    opened = {"objeto": label, "ruta": ruta_declarada or str(path), "resultado": result, "sha256": sha256(path), "descripcion": description}
    if suffix == ".pdf" and result == "ABIERTO_PDF_TEXTO":
        opened["extractores_pdf"] = ";".join(extraction.extractors)
        opened["advertencias_pdf"] = ";".join(extraction.warnings) or "NINGUNA"
    return opened


def parse_manifest(path: Path, corpus: Path, repo: Path) -> list[dict[str, Any]]:
    records = yaml.safe_load(path.read_text(encoding="utf-8"))
    result = []
    for row in records if isinstance(records, list) else []:
        if not isinstance(row, dict) or not row.get("id") or not row.get("archivo"):
            continue
        nombre_raiz = row.get("raiz") or "data_raw"
        ruta_logica = f"{nombre_raiz}:{row['archivo']}"
        base = manifiesto.resolver_raiz(nombre_raiz, repo, corpus)
        ruta_resuelta = str(Path(base) / str(row["archivo"])) if base is not None else None
        result.append({**row, "ruta_logica": ruta_logica, "ruta_resuelta": ruta_resuelta})
    return result


def manifest_candidates(source: str, manifest: list[dict[str, Any]], action: str) -> list[dict[str, Any]]:
    token = normalized(source)
    exact: list[dict[str, Any]] = []
    for row in manifest:
        identifier = normalized(str(row.get("id", "")))
        if identifier == token or identifier.startswith(token + "_") or re.match(rf"^{re.escape(token)}\d", identifier):
            exact.append(row)
    def rank(row: dict[str, Any]) -> tuple[int, str]:
        name = str(row.get("archivo", "")).lower()
        wants_doc = bool(re.search(r"diccionario|cuestionario|codebook|manual|instrumento|reactivo", action, re.I))
        doc = name.endswith((".pdf", ".xlsx", ".xls")) or any(term in name for term in ("fd", "cuest", "manual", "modelo"))
        return (0 if wants_doc and doc else 1 if doc else 2, name)
    return sorted(exact, key=rank)[:3]


def source_url_index(repo: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    by_name: dict[str, list[str]] = defaultdict(list)
    by_id: dict[str, list[str]] = defaultdict(list)
    for relative in ("data/mapa-ext-general-2026-08-06.tsv", "data/mapa-ext-academico-2026-08-06.tsv"):
        for row in read_tsv(repo / relative):
            name = row.get("nombre_fuente") or row.get("fuente") or ""
            identifier = row.get("id_candidata") or row.get("id") or ""
            url = row.get("URL_primaria") or row.get("url_primaria") or ""
            if url.startswith(("http://", "https://")):
                by_name[normalized(name)].append(url)
                by_id[identifier].append(url)
    return by_name, by_id


def exact_reference_rows(repo: Path, refs: list[str], source: str, by_id: dict[str, list[str]]) -> tuple[list[dict[str, str]], list[str]]:
    openings: list[dict[str, str]] = []
    urls: list[str] = []
    for ref in refs:
        path_rel, start, end = main_ref_parts(ref)
        path = repo / path_rel
        if not path.is_file():
            openings.append({"objeto": ref, "ruta": str(path_rel), "resultado": "ARCHIVO_NO_EXISTE", "sha256": "NO_DETERMINADO", "descripcion": "", "frontera": "archivo no disponible"})
            continue
        excerpt, frontier = exact_ref_excerpt(path, start, end)
        openings.append({"objeto": ref, "ruta": str(path_rel), "resultado": "ABIERTO_REFERENCIA_MAIN", "sha256": sha256(path), "descripcion": excerpt, "frontera": frontier})
        if path.suffix.lower() == ".tsv":
            rows = read_tsv(path)
            selected: list[dict[str, str]] = []
            if start is not None:
                lo, hi = max(0, start - 2), max(0, (end or start) - 1)
                selected = rows[lo:hi]
            else:
                for row in rows:
                    names = [row.get(field, "") for field in ("fuente", "nombre_fuente", "fuente_canonica", "nombre")]
                    if normalized(source) in {normalized(name) for name in names if name}:
                        selected.append(row)
            for row in selected:
                for key, value in row.items():
                    if "url" in key.lower() and value.startswith(("http://", "https://")):
                        urls.append(value)
                evidence = " ".join((row.get("evidencia", ""), row.get("evidencia_revisada", "")))
                for identifier in re.findall(r"(?:MAPA-EXT-\d+|[A-Z][A-Z0-9_]{4,})", evidence):
                    urls.extend(by_id.get(identifier, []))
    return openings, sorted(dict.fromkeys(urls))


def schema_documents() -> dict[str, dict[str, Any]]:
    base = "https://json-schema.org/draft/2020-12/schema"
    return {
        "inspector-contract.schema.json": {"$schema": base, "type": "object", "required": ["schema_version", "tarea_observacion_id", "run_id", "snapshot_t0_sha256", "rutas_localizadores", "objetos_a_abrir", "criterio_parada"], "not": {"anyOf": [{"required": [field]} for field in ("relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen")]}},
        "neutral-report.schema.json": {"$schema": base, "type": "object", "required": ["schema_version", "reporte_id", "tarea_observacion_id", "input_sha256", "objetos_abiertos", "intentos", "universo_inspeccionado", "metodo", "resultado_operativo", "frontera"], "not": {"anyOf": [{"required": [field]} for field in ("relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen")]}},
        "curator-input.schema.json": {"$schema": base, "type": "object", "required": ["schema_version", "tarea_curaduria_id", "run_id", "relacion_id", "siguiente_accion_original", "criterio_cierre_individual", "reporte_neutral_ref", "reporte_neutral_sha256"]},
        "semantic-run-proposal.schema.json": {"$schema": base, "type": "object", "required": ["propuesta_id", "run_id", "relacion_id", "tarea_observacion_id", "input_inspector_ref", "input_inspector_sha256", "reporte_neutral_ref", "reporte_neutral_sha256", "input_curador_ref", "input_curador_sha256", "estado_cierre", "accion_original", "criterio_cierre_individual", "expediente_integrable", "modifica_baseline"]},
        "semantic-supervision.schema.json": {"$schema": base, "type": "object", "required": ["supervision_id", "run_id", "relacion_id", "propuesta_id", "estado_recalculado", "accion_preservada", "joins_validos", "hashes_validos", "destino"]},
    }


def choose_state(work_type: str, report: dict[str, Any], action: str, material_missing: list[str]) -> tuple[str, str]:
    openings = report["objetos_abiertos"]
    attempts = report["intentos"]
    local_assets = [row for row in openings if row["resultado"].startswith("ABIERTO_") and not row["resultado"].endswith("REFERENCIA_MAIN")]
    direct = any(
        any(str(attempt.get("content_type", "")).startswith(prefix) for prefix in DIRECT_CONTENT)
        and str(attempt.get("resultado_http_archivo_error", "")).startswith("HTTP_2")
        and attempt.get("objeto_completo") == "SI"
        for attempt in attempts
    )
    successes = [attempt for attempt in attempts if str(attempt.get("resultado_http_archivo_error", "")).startswith("HTTP_2")]
    if work_type == "ANALISIS_MEDICION":
        needed = ["estimando", "poblacion", "unidad", "variables", "codificacion", "ponderacion", "diseno", "transformacion", "incertidumbre"]
        return "BLOQUEADA_INPUT_FALTANTE", "No existe especificación ejecutable: faltan " + ",".join(needed)
    if re.search(r"autorizaci[oó]n|solicitar acceso|licencia aplicable", action, re.I) and not direct and not local_assets:
        return "REQUIERE_DECISION_HUMANA", "La acción exige autorización/licencia y no apareció un objeto descargable abierto en los intentos permitidos."
    if attempts and not successes:
        return "NO_ALCANZO_TRAS_INTENTOS", "Los intentos reales terminaron sin HTTP 2xx; continuar solo con acceso alternativo autorizado o localizador corregido."
    if direct or local_assets:
        return "EJECUTADA_CON_RESULTADO", "Se abrió al menos un objeto de datos/documentación y se registró su estructura literal; el juicio semántico permanece separado."
    if successes or any(row["resultado"] == "ABIERTO_REFERENCIA_MAIN" for row in openings):
        return "FUENTE_ABIERTA_SIN_OBJETO_REQUERIDO", "Se abrió la fuente/referencia, pero no un objeto que cierre literalmente la acción individual; usar la receta y frontera registradas."
    if material_missing:
        return "BLOQUEADA_INPUT_FALTANTE", "No existe localizador u objeto exacto ejecutable y faltan campos materiales: " + ",".join(material_missing)
    return "NO_CORRIDA", "No se observó una operación material verificable."


def execute(repo: Path, output: Path, network: bool) -> dict[str, Any]:
    registry, universe = repo / "data/curacion-registro", repo / "data/curacion-universo"
    baseline_before = baseline_hashes(registry)
    snapshot = snapshot_hash(universe)
    relations = index_unique(read_tsv(registry / "relaciones.tsv"), "relacion_id", "relaciones")
    candidate_ids = {rid for rid, row in relations.items() if row.get("clasificacion_relacion") == "CANDIDATA"}
    evidence = index_unique((row for row in read_tsv(registry / "evidencias.tsv") if row.get("relacion_id") in candidate_ids), "relacion_id", "evidencias candidatas")
    utility = index_unique(read_tsv(registry / "utilidad-modelo.tsv"), "relacion_id", "utilidad")
    work = index_unique(read_tsv(registry / "trabajo-semantico.tsv"), "relacion_id", "trabajo")
    if set(evidence) != candidate_ids or set(work) != candidate_ids:
        raise SemanticRunError("la cola no cubre exactamente las candidatas derivadas del baseline")
    invalid_types = {row.get("tipo_trabajo", "") for row in work.values()} - SEMANTIC_TYPES
    if invalid_types:
        raise SemanticRunError(f"tipos no ejecutables en esta pasada: {sorted(invalid_types)}")

    preserved: list[dict[str, str]] = []
    for rid in sorted(candidate_ids):
        ev, util, classified = evidence[rid], utility[rid], work[rid]
        if ev.get("siguiente_accion", "") != util.get("siguiente_accion", ""):
            raise SemanticRunError(f"acción original divergente: {rid}")
        row = {
            "relacion_id": rid,
            "fuente_canonica_normalizada": relations[rid]["fuente_canonica_normalizada"],
            "tipo_trabajo": classified["tipo_trabajo"],
            "siguiente_accion_original": ev["siguiente_accion"],
            "siguiente_accion_original_sha256": sha256_bytes(ev["siguiente_accion"].encode("utf-8")),
            "input_requerido_original": util.get("verificacion_requerida", ""),
            "reserva_original": util.get("reserva", ""),
            "evidencia_ref_original": ev.get("evidencia_ref", ""),
            "criterio_cierre_individual": classified.get("criterio_cierre", ""),
        }
        if classified.get("siguiente_accion_original", classified.get("siguiente_accion")) != row["siguiente_accion_original"]:
            raise SemanticRunError(f"clasificación sustituyó acción original: {rid}")
        preserved.append(row)
    write_tsv(output / "acciones-originales-preservadas.tsv", preserved, list(preserved[0]))

    seed = {"engine_version": ENGINE_VERSION, "snapshot": snapshot, "baseline": baseline_before["baseline.json"], "acciones": sha256(output / "acciones-originales-preservadas.tsv")}
    run_id = stable_id("SEMRUN", seed)
    run_dir = output / "runs" / run_id
    schemas = schema_documents()
    for name, document in schemas.items():
        write_json(output / "schemas" / name, document)

    corpus = repo / "data" / "raw"
    manifest = parse_manifest(repo / "data/manifiesto.yaml", corpus, repo)
    by_name, by_map_id = source_url_index(repo)
    families = index_unique(read_tsv(universe / "familias-activos.tsv"), "activo_id", "familias")
    bootstrap = index_unique(read_tsv(registry / "bootstrap-semantico.tsv"), "relacion_id", "bootstrap")

    supervisor_map: list[dict[str, str]] = []
    partition_map: dict[tuple[str, str], list[str]] = defaultdict(list)
    results: list[dict[str, str]] = []
    proposals: list[dict[str, str]] = []
    paths_by_relation: dict[str, dict[str, Path]] = {}
    # Una apertura de localizador pertenece a la partición fuente/familia y se
    # reutiliza para relaciones que declaran exactamente el mismo URL. Esto
    # evita convertir relaciones hermanas en discovery o tráfico duplicado.
    url_attempt_cache: dict[str, list[dict[str, Any]]] = {}

    for original in preserved:
        rid, source = original["relacion_id"], original["fuente_canonica_normalizada"]
        ev, classified = evidence[rid], work[rid]
        linked_assets = [value for value in bootstrap[rid].get("activo_id_vinculado", "").split(";") if value not in UNKNOWN]
        family_values = sorted({families[asset].get("familia_logica_id", "NO_DETERMINADO") for asset in linked_assets if asset in families})
        family = ";".join(family_values) if family_values else "SIN_ACTIVO_EXACTO:" + source
        task_id = stable_id("TOBS-SEM", run_id, rid)
        refs = sorted(dict.fromkeys(
            ref
            for collection in (ev["evidencia_ref"], utility[rid].get("evidencia_ref", ""))
            for ref in collection.split(";")
            if ref.startswith("MAIN:")
        ))
        ref_openings, declared_urls = exact_reference_rows(repo, refs, source, by_map_id)
        if not declared_urls:
            declared_urls = sorted(dict.fromkeys(by_name.get(normalized(source), [])))
        asset_rows = manifest_candidates(source, manifest, ev["siguiente_accion"])
        asset_specs = [{"id_manifiesto": row["id"], "ruta": row["ruta_logica"], "sha256_declarado": row.get("sha256", "NO_DETERMINADO")} for row in asset_rows]
        contract = {
            "schema_version": ENGINE_VERSION, "tarea_observacion_id": task_id, "run_id": run_id,
            "snapshot_t0_sha256": snapshot, "rutas_localizadores": declared_urls,
            "objetos_a_abrir": [ref for ref in refs] + asset_specs,
            "grado_inspeccion": "APERTURA_LITERAL_ACOTADA",
            "campos_descriptivos": ["formato", "estructura", "unidad_si_observable", "periodo_si_observable", "variables_o_secciones", "frontera"],
            "criterio_parada": original["criterio_cierre_individual"],
            "prohibiciones": ["No adjudicar", "No inferir necesidad", "No declarar ausencia general", "No hacer discovery panorámico"],
        }
        contract_path = run_dir / "contratos-inspector" / f"{task_id}.json"
        write_json(contract_path, contract)
        inspector_input = {**contract, "contrato_ref": str(contract_path.relative_to(repo)), "contrato_sha256": sha256(contract_path)}
        input_path = run_dir / "inputs-inspector" / f"{task_id}.json"
        write_json(input_path, inspector_input)
        forbidden = {"relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen"}.intersection(inspector_input)
        if forbidden:
            raise SemanticRunError(f"input inspector no cegado {task_id}: {sorted(forbidden)}")

        openings: list[dict[str, Any]] = list(ref_openings)
        for asset in asset_rows:
            if asset["ruta_resuelta"] is None:
                observed = {
                    "objeto": f"MANIFEST:{asset['id']}",
                    "ruta": asset["ruta_logica"],
                    "resultado": "RAIZ_NO_CONFIGURADA",
                    "sha256": "NO_DETERMINADO",
                    "descripcion": "",
                }
                observed["sha256_declarado"] = asset.get("sha256", "NO_DETERMINADO")
                observed["hash_reconcilia"] = "NO_VERIFICADO"
            else:
                observed = open_local_object(Path(asset["ruta_resuelta"]), f"MANIFEST:{asset['id']}", ruta_declarada=asset["ruta_logica"])
                observed["sha256_declarado"] = asset.get("sha256", "NO_DETERMINADO")
                observed["hash_reconcilia"] = "SI" if observed["sha256"] == asset.get("sha256") else "NO"
            openings.append(observed)
        attempts: list[dict[str, Any]] = []
        if classified["tipo_trabajo"] == "BUSQUEDA_DIRIGIDA" and network:
            for url in declared_urls[:1]:
                if url not in url_attempt_cache:
                    prior_report_path = run_dir / "reportes-neutrales" / f"{task_id}.json"
                    cached: list[dict[str, Any]] = []
                    if prior_report_path.is_file():
                        prior_report = json.loads(prior_report_path.read_text(encoding="utf-8"))
                        prior_attempts = prior_report.get("intentos", [])
                        if (
                            prior_attempts
                            and prior_attempts[0].get("localizador") == url
                            and all(item.get("orden") in {1, 2} for item in prior_attempts)
                            and all(item.get("resultado_http_archivo_error") != "NO_CORRIDA_RED_DESHABILITADA" for item in prior_attempts)
                        ):
                            cached = prior_attempts
                    if not cached:
                        cached = fetch_declared(url)
                    shared_id = stable_id("INTENTO", run_id, url)
                    for item in cached:
                        item["intento_compartido_id"] = shared_id
                    url_attempt_cache[url] = cached
                attempts.extend(json.loads(json.dumps(url_attempt_cache[url])))
        elif classified["tipo_trabajo"] == "BUSQUEDA_DIRIGIDA" and declared_urls:
            attempts.append({"orden": 0, "localizador": declared_urls[0], "resultado_http_archivo_error": "NO_CORRIDA_RED_DESHABILITADA", "url_final": "NO_DETERMINADO", "content_type": "NO_DETERMINADO", "bytes_observados": 0, "objeto_completo": "NO", "sha256_objeto": "NO_DETERMINADO", "sha256_fragmento": "NO_DETERMINADO", "resultado_literal": "Ejecutar nuevamente con --network."})

        material_missing = [field for field in ("variable_reactivo_tabla", "unidad_observacion", "periodo", "universo_muestra", "codificacion") if ev.get(field, "") in UNKNOWN]
        preliminary_report = {"objetos_abiertos": openings, "intentos": attempts}
        state, recipe = choose_state(classified["tipo_trabajo"], preliminary_report, ev["siguiente_accion"], material_missing)
        report = {
            "schema_version": ENGINE_VERSION,
            "reporte_id": stable_id("RNEU", task_id, sha256(input_path), state),
            "tarea_observacion_id": task_id, "run_id": run_id, "snapshot_t0_sha256": snapshot,
            "input_ref": str(input_path.relative_to(repo)), "input_sha256": sha256(input_path),
            "objetos_abiertos": openings, "intentos": attempts,
            "universo_inspeccionado": {"referencias_main": refs, "activos_manifest": asset_specs, "localizadores_declarados": declared_urls},
            "metodo": "Lectura de bytes de referencias MAIN; apertura estructural de activos exactos por id de manifiesto; para búsqueda, GET acotado del localizador exacto y como máximo un vínculo explícito de documentación.",
            "resultado_operativo": state,
            "resultado_literal": " | ".join(trim_text(str(row.get("descripcion") or row.get("resultado_literal") or row.get("resultado")), 350) for row in openings + attempts[:2]),
            "frontera": "No se buscaron fuentes adicionales; HTML de landing no equivale a codebook; un fragmento de red no equivale al objeto completo.",
            "bloqueo": recipe if state in {"NO_ALCANZO_TRAS_INTENTOS", "BLOQUEADA_INPUT_FALTANTE", "REQUIERE_DECISION_HUMANA"} else "NINGUNO",
            "siguiente_receta_concreta": recipe,
            "afirmaciones_semanticas_como_hecho": 0,
        }
        report_path = run_dir / "reportes-neutrales" / f"{task_id}.json"
        write_json(report_path, report)
        curator_id = stable_id("TCUR", run_id, rid)
        curator_input = {
            "schema_version": ENGINE_VERSION, "tarea_curaduria_id": curator_id, "run_id": run_id,
            "snapshot_t0_sha256": snapshot, "baseline_sha256": baseline_before["baseline.json"],
            "relacion_id": rid, "necesidad_id": relations[rid]["necesidad_id"],
            "fuente_canonica_normalizada": source,
            "siguiente_accion_original": original["siguiente_accion_original"],
            "input_requerido_original": original["input_requerido_original"],
            "reserva_original": original["reserva_original"], "evidencia_ref_original": original["evidencia_ref_original"],
            "evidencia_ref_accion_original": utility[rid].get("evidencia_ref", ""),
            "evidencia_ref_evidencia_original": ev.get("evidencia_ref", ""),
            "criterio_cierre_individual": original["criterio_cierre_individual"],
            "evidencia_estructurada_previa": {field: ev.get(field, "") for field in ("variable_reactivo_tabla", "texto_evidencia", "unidad_observacion", "periodo", "universo_muestra", "codificacion", "parte_necesidad_cubierta", "parte_necesidad_no_cubierta")},
            "reporte_neutral_ref": str(report_path.relative_to(repo)), "reporte_neutral_sha256": sha256(report_path),
        }
        curator_input_path = run_dir / "inputs-curador" / f"{curator_id}.json"
        write_json(curator_input_path, curator_input)

        action = "ESCALAR" if state == "REQUIERE_DECISION_HUMANA" else "NO_DETERMINADO"
        integrable = "NO"
        proposal = {
            "propuesta_id": stable_id("SEMPROP", curator_id, sha256(curator_input_path), state),
            "run_id": run_id, "relacion_id": rid, "tarea_observacion_id": task_id,
            "input_inspector_ref": str(input_path.relative_to(repo)), "input_inspector_sha256": sha256(input_path),
            "reporte_neutral_ref": str(report_path.relative_to(repo)), "reporte_neutral_sha256": sha256(report_path),
            "input_curador_ref": str(curator_input_path.relative_to(repo)), "input_curador_sha256": sha256(curator_input_path),
            "activo_id": ";".join(linked_assets) or "NO_DETERMINADO", "fuente": source,
            "snapshot_t0_sha256": snapshot, "baseline_sha256": baseline_before["baseline.json"],
            "accion_curador": action, "adjudicacion_propuesta": relations[rid]["clasificacion_relacion"],
            "estado_cierre": state, "accion_original": original["siguiente_accion_original"],
            "accion_original_sha256": original["siguiente_accion_original_sha256"],
            "input_requerido_original": original["input_requerido_original"], "reserva_original": original["reserva_original"],
            "evidencia_ref_original": original["evidencia_ref_original"], "criterio_cierre_individual": original["criterio_cierre_individual"],
            "evidencia_ref_accion_original": utility[rid].get("evidencia_ref", ""),
            "evidencia_ref_evidencia_original": ev.get("evidencia_ref", ""),
            "resultado_contrastado": recipe,
            "expediente_integrable": integrable, "modifica_baseline": "NO",
            "reserva_curador": "La ejecución produjo un terminal operativo, no evidencia suficiente para cambiar adjudicación; el baseline se conserva.",
        }
        proposals.append(proposal)
        results.append({
            "relacion_id": rid, "tipo_trabajo": classified["tipo_trabajo"], "fuente": source,
            "tarea_observacion_id": task_id, "reporte_neutral_ref": str(report_path.relative_to(repo)),
            "estado_cierre": state, "intentos_reales": str(len([a for a in attempts if a.get("orden", 0) > 0])),
            "objetos_abiertos": str(sum(str(row.get("resultado", "")).startswith("ABIERTO_") for row in openings)),
            "siguiente_accion_original": original["siguiente_accion_original"], "criterio_cierre_individual": original["criterio_cierre_individual"],
            "receta_continuacion": recipe,
        })
        supervisor_map.append({
            "tarea_observacion_id": task_id, "relacion_id": rid, "necesidad_id": relations[rid]["necesidad_id"],
            "activo_id": ";".join(linked_assets) or "NO_DETERMINADO", "input_inspector_ref": str(input_path.relative_to(repo)),
            "reporte_neutral_ref": str(report_path.relative_to(repo)), "input_curador_ref": str(curator_input_path.relative_to(repo)),
        })
        partition_map[(source, family)].append(rid)
        paths_by_relation[rid] = {"input": input_path, "report": report_path, "curator": curator_input_path}

    write_tsv(run_dir / "mapa-privado-supervisor.tsv", supervisor_map, list(supervisor_map[0]))
    partition_rows = [{"particion_id": stable_id("PART", run_id, source, family), "fuente": source, "familia_logica_id": family, "relaciones": ";".join(sorted(ids)), "numero_relaciones": str(len(ids))} for (source, family), ids in sorted(partition_map.items())]
    write_tsv(run_dir / "particiones.tsv", partition_rows, list(partition_rows[0]))
    write_tsv(run_dir / "resultados-acciones.tsv", results, list(results[0]))
    write_tsv(run_dir / "propuestas-curador.tsv", proposals, list(proposals[0]))

    # Supervisión independiente: todo se relee desde disco y el estado se deriva
    # del reporte; no se acepta el estado copiado en la propuesta.
    proposal_disk = index_unique(read_tsv(run_dir / "propuestas-curador.tsv"), "relacion_id", "propuestas")
    result_disk = index_unique(read_tsv(run_dir / "resultados-acciones.tsv"), "relacion_id", "resultados")
    supervision: list[dict[str, str]] = []
    for rid in sorted(candidate_ids):
        proposal = proposal_disk[rid]
        original = next(row for row in preserved if row["relacion_id"] == rid)
        paths = paths_by_relation[rid]
        inspector = json.loads(paths["input"].read_text(encoding="utf-8"))
        report = json.loads(paths["report"].read_text(encoding="utf-8"))
        curator = json.loads(paths["curator"].read_text(encoding="utf-8"))
        hash_valid = all((proposal["input_inspector_sha256"] == sha256(paths["input"]), proposal["reporte_neutral_sha256"] == sha256(paths["report"]), proposal["input_curador_sha256"] == sha256(paths["curator"]), report["input_sha256"] == sha256(paths["input"]), curator["reporte_neutral_sha256"] == sha256(paths["report"])))
        blinded = not {"relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen"}.intersection(inspector) and not {"relacion_id", "necesidad_id", "adjudicacion_vigente", "objeto_modelo_origen"}.intersection(report)
        action_preserved = all((proposal["accion_original"] == original["siguiente_accion_original"], proposal["accion_original_sha256"] == original["siguiente_accion_original_sha256"], proposal["criterio_cierre_individual"] == original["criterio_cierre_individual"], result_disk[rid]["siguiente_accion_original"] == original["siguiente_accion_original"], result_disk[rid]["criterio_cierre_individual"] == original["criterio_cierre_individual"]))
        derived_state = report.get("resultado_operativo", "NO_CORRIDA") if report.get("objetos_abiertos") or report.get("intentos") else "NO_CORRIDA"
        joins = all((curator["relacion_id"] == rid, curator["reporte_neutral_ref"] == proposal["reporte_neutral_ref"], inspector["tarea_observacion_id"] == report["tarea_observacion_id"] == proposal["tarea_observacion_id"]))
        errors = []
        if derived_state not in TERMINAL_STATES: errors.append("ESTADO_INVALIDO")
        if derived_state != proposal["estado_cierre"]: errors.append("ESTADO_PROPUESTA_NO_RECONCILIA")
        if not hash_valid: errors.append("HASH_INVALIDO")
        if not blinded: errors.append("CEGAMIENTO_ROTO")
        if not action_preserved: errors.append("ACCION_O_CRITERIO_NO_PRESERVADO")
        if not joins: errors.append("JOIN_INVALIDO")
        if proposal["expediente_integrable"] == "SI": errors.append("INTEGRACION_NO_DEMOSTRADA")
        supervision.append({
            "supervision_id": stable_id("SUPSEM", run_id, rid), "run_id": run_id, "relacion_id": rid,
            "propuesta_id": proposal["propuesta_id"], "estado_recalculado": derived_state,
            "accion_preservada": "SI" if action_preserved else "NO", "joins_validos": "SI" if joins else "NO",
            "hashes_validos": "SI" if hash_valid else "NO", "cegamiento_validado": "SI" if blinded else "NO",
            "destino": "COLA_RESIDUAL" if not errors else "RECHAZADA_FAIL_CLOSED",
            "errores": ";".join(errors) if errors else "NINGUNO",
        })
    write_tsv(run_dir / "supervision.tsv", supervision, list(supervision[0]))
    if any(row["errores"] != "NINGUNO" for row in supervision):
        raise SemanticRunError("supervisión semántica independiente rechazó el run")

    integration = [{"run_id": run_id, "propuesta_id": row["propuesta_id"], "relacion_id": row["relacion_id"], "destino_integracion": "NO_ENVIAR", "expediente_integrable": "NO", "modifica_baseline": "NO", "razon": row["estado_cierre"] + ": " + row["resultado_contrastado"]} for row in proposals]
    write_tsv(run_dir / "expediente-integracion.tsv", integration, list(integration[0]))

    # Entrada explícita para integrate.py: el expediente sustantivo demuestra
    # uno a uno por qué ninguna propuesta es integrable; por eso la interfaz
    # del integrador contiene solo el header canónico y una tarea curadora
    # válida con asignaciones vacías. No se traduce una reserva a propuesta.
    integrate_fields = [
        "propuesta_id", "snapshot_t0_sha256", "baseline_sha256",
        "reporte_inspeccion_ref", "tarea_observacion_id", "activo_id",
        "objeto_logico_id", "procedencia_ref", "relacion_id", "accion",
        "afirmacion_origen_tipo", "tratar_como_hecho",
        "adjudicacion_propuesta", "evidencia_nueva_material",
        "cegamiento_roto", "excepcion_cegamiento_ref", "reserva",
    ]
    compatible_path = run_dir / "propuestas-integrate-compatibles.tsv"
    write_tsv(compatible_path, [], integrate_fields)
    compatible_input_path = run_dir / "input.json"
    write_json(compatible_input_path, {
        "tarea_curacion_id": stable_id("TCUR-INTEGRATE", run_id),
        "run_id": run_id,
        "snapshot_t0_sha256": snapshot,
        "baseline_sha256": baseline_before["baseline.json"],
        "asignaciones": [],
        "criterio_parada": "Cero propuestas integrables según expediente-integracion.tsv 1:1; validar baseline sin cambios.",
        "expediente_semantico_ref": str((run_dir / "expediente-integracion.tsv").relative_to(repo)),
        "expediente_semantico_sha256": sha256(run_dir / "expediente-integracion.tsv"),
    })
    write_json(run_dir / "hashes.json", {
        "files": {
            compatible_path.name: sha256(compatible_path),
            compatible_input_path.name: sha256(compatible_input_path),
        },
        "run_id": run_id,
    })
    baseline_after = baseline_hashes(registry)
    if baseline_before != baseline_after:
        raise SemanticRunError("baseline cambió durante la ejecución")

    state_counts = Counter(row["estado_recalculado"] for row in supervision)
    type_counts = Counter(row["tipo_trabajo"] for row in results)
    executed = sum(state != "NO_CORRIDA" for state in (row["estado_recalculado"] for row in supervision))
    artifacts = {str(path.relative_to(repo)): sha256(path) for path in sorted(run_dir.rglob("*")) if path.is_file()}
    manifest_out = {
        "schema_version": ENGINE_VERSION, "run_id": run_id, "snapshot_t0_sha256": snapshot,
        "baseline_sha256": baseline_before["baseline.json"], "motor_ref": str(Path(__file__).resolve().relative_to(repo)),
        "motor_sha256": sha256(Path(__file__)), "denominador_candidatas_derivado": len(candidate_ids),
        "tipos_trabajo_derivados": dict(sorted(type_counts.items())),
        "estados_recalculados_desde_supervision": dict(sorted(state_counts.items())),
        "coberturas": {
            "EXPEDIENTES_ADMINISTRATIVOS_MATERIALIZADOS": {"numerador": len(result_disk), "denominador": len(candidate_ids)},
            "COBERTURA_SEMANTICA_EJECUTADA_COLA": {"numerador": executed, "denominador": len(candidate_ids)},
            "PROPUESTAS_INTEGRABLES": {"numerador": 0, "denominador": len(candidate_ids)},
        },
        "particiones_fuente_familia": len(partition_rows), "network_habilitada": network,
        "artefactos_run_sha256": artifacts,
        "derivacion": "Los conteos se obtienen de resultados-acciones.tsv y supervision.tsv; validate debe releerlos, no confiar en este manifest.",
    }
    write_json(output / "manifest.json", manifest_out)
    return manifest_out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--network", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    output = args.output.resolve() if args.output else repo / "data/curacion-registro/ejecucion-semantica"
    result = execute(repo, output, args.network)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
