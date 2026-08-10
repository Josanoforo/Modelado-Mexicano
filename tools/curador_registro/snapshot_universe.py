#!/usr/bin/env python3
"""Construye un T0 determinista de declaraciones y activos únicos.

La lista de inputs y los mapeos de columnas viven en datos. Este módulo no
contiene nombres de fuentes reales ni conclusiones semánticas. La identidad de
contenido se establece por SHA-256 verificado; una URL es únicamente evidencia
de declaración/localización y puede agrupar activos en una familia lógica sin
fusionarlos.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


URL_RE = re.compile(r"https?://[^\s<>\]\[\)\(\"']+")
HASH_RE = re.compile(r"^[0-9a-fA-F]{64}$")


def sha256_file(path: Path, cache: dict[Path, str] | None = None) -> str:
    path = path.resolve()
    if cache is not None and path in cache:
        return cache[path]
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    value = digest.hexdigest()
    if cache is not None:
        cache[path] = value
    return value


def stable_id(prefix: str, *parts: str, size: int = 20) -> str:
    payload = "\x1f".join(parts).encode("utf-8")
    return prefix + hashlib.sha256(payload).hexdigest()[:size]


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def clean_url(url: str) -> str:
    return url.rstrip(".,;:")


def urls_in(text: str) -> list[str]:
    return [clean_url(value) for value in URL_RE.findall(text or "")]


def first_value(record: dict[str, Any], columns: Iterable[str]) -> str:
    for column in columns:
        value = str(record.get(column, "") or "").strip()
        if value:
            return value
    return ""


def infer_format(localizer: str, declared: str = "") -> str:
    if declared.strip():
        return declared.strip()
    path = localizer.split("?", 1)[0]
    suffix = Path(path).suffix.lower().lstrip(".")
    return suffix.upper() if suffix else "NO_DETERMINADO"


@dataclass
class Declaration:
    input_id: str
    localizador: str
    identificador: str
    fingerprint: str
    url: str = ""
    local_path: str = ""
    sha256: str = ""
    hash_declarado: str = ""
    hash_observado: str = ""
    fuente_programa: str = "NO_DETERMINADO"
    edicion_periodo: str = "NO_DETERMINADO"
    objeto_logico: str = "NO_DETERMINADO"
    formato: str = "NO_DETERMINADO"
    declaration_id: str = ""
    activo_id: str = ""
    metodo_reconciliacion: str = "SIN_RECONCILIACION"
    evidencia_reconciliacion: str = "NO_DETERMINADO"
    estado_reconciliacion: str = "NO_DETERMINADO"


@dataclass
class InputResult:
    input_id: str
    path: Path
    display_path: str
    tipo: str
    parser: str
    hash_input: str
    found: int
    parsed: int
    errors: list[str] = field(default_factory=list)
    reserve: str = "NINGUNA"
    declarations: list[Declaration] = field(default_factory=list)


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[max(a, b)] = min(a, b)


def _declaration(
    input_id: str,
    raw: Any,
    discriminator: str,
    localizador: str,
    identificador: str,
    **kwargs: str,
) -> Declaration:
    fingerprint = hashlib.sha256(
        (canonical_json(raw) + "\x1f" + discriminator).encode("utf-8")
    ).hexdigest()
    return Declaration(
        input_id=input_id,
        localizador=localizador or "NO_DETERMINADO",
        identificador=identificador or "NO_DETERMINADO",
        fingerprint=fingerprint,
        **kwargs,
    )


def parse_manifest(path: Path, input_id: str, corpus_root: Path, cache: dict[Path, str]) -> tuple[int, list[Declaration], list[str]]:
    errors: list[str] = []
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    except Exception as exc:  # pragma: no cover - defensive boundary
        return 0, [], [f"YAML:{type(exc).__name__}:{exc}"]
    if not isinstance(payload, list):
        return 0, [], ["YAML_RAIZ_NO_LISTA"]
    declarations: list[Declaration] = []
    found = 0
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        identifier = str(entry.get("id", "") or "").strip()
        declared_path = str(entry.get("archivo", "") or "").strip()
        url_values = urls_in(str(entry.get("url_origen", "") or ""))
        if not declared_path and not url_values:
            continue
        found += 1
        local_hash = str(entry.get("sha256", "") or "").strip().lower()
        if local_hash and not HASH_RE.fullmatch(local_hash):
            errors.append(f"HASH_INVALIDO:{identifier}")
            local_hash = ""
        actual = corpus_root / declared_path if declared_path else None
        if actual and actual.is_file() and not local_hash:
            local_hash = sha256_file(actual, cache)
        url = url_values[0] if url_values else ""
        localizer = url or (f"data_raw:{declared_path}" if declared_path else "")
        declarations.append(_declaration(
            input_id, entry, "manifest", localizer, identifier,
            url=url,
            local_path=declared_path,
            sha256=local_hash,
            fuente_programa=identifier or "NO_DETERMINADO",
            edicion_periodo=str(entry.get("fecha_descarga", "") or "NO_DETERMINADO"),
            objeto_logico=identifier or declared_path or "NO_DETERMINADO",
            formato=infer_format(declared_path or url, str(entry.get("formato", "") or "")),
        ))
    return found, declarations, errors


def parse_corpus_tree(path: Path, input_id: str, cache: dict[Path, str]) -> tuple[int, list[Declaration], list[str], str]:
    declarations: list[Declaration] = []
    merkle: list[str] = []
    files = sorted((item for item in path.rglob("*") if item.is_file()), key=lambda p: p.relative_to(path).as_posix())
    for item in files:
        relative = item.relative_to(path).as_posix()
        digest = sha256_file(item, cache)
        merkle.append(f"{relative}\t{item.stat().st_size}\t{digest}")
        top = relative.split("/", 1)[0]
        declarations.append(_declaration(
            input_id, {"ruta": relative, "sha256": digest}, "corpus",
            f"data_raw:{relative}", relative,
            local_path=relative,
            sha256=digest,
            fuente_programa=top,
            objeto_logico=relative,
            formato=infer_format(relative),
        ))
    tree_hash = hashlib.sha256("\n".join(merkle).encode("utf-8")).hexdigest()
    return len(files), declarations, [], tree_hash


def parse_xml_urls(path: Path, input_id: str) -> tuple[int, list[Declaration], list[str]]:
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        return 0, [], [f"XML:{type(exc).__name__}:{exc}"]
    declarations: list[Declaration] = []
    nodes = list(root.findall(".//Archivo"))
    for node in nodes:
        url = clean_url((node.text or "").strip())
        if not url:
            continue
        program_match = re.search(r"/programas/([^/]+)/", url)
        edition_match = re.search(r"/(19|20)\d{2}(?:[_/-]|$)", url)
        basename = Path(url.split("?", 1)[0]).name
        declarations.append(_declaration(
            input_id, {"url": url}, "xml", url, basename,
            url=url,
            fuente_programa=program_match.group(1) if program_match else "NO_DETERMINADO",
            edicion_periodo=edition_match.group(0).strip("_/-") if edition_match else "NO_DETERMINADO",
            objeto_logico=basename or "NO_DETERMINADO",
            formato=infer_format(url),
        ))
    return len(nodes), declarations, []


def parse_tsv(path: Path, input_id: str, options: dict[str, Any], corpus_root: Path, cache: dict[Path, str]) -> tuple[int, list[Declaration], list[str]]:
    errors: list[str] = []
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
    except Exception as exc:
        return 0, [], [f"TSV:{type(exc).__name__}:{exc}"]
    declarations: list[Declaration] = []
    url_columns = options.get("url_columns", [])
    id_columns = options.get("identifier_columns", [])
    program_columns = options.get("program_columns", [])
    edition_columns = options.get("edition_columns", [])
    object_columns = options.get("object_columns", [])
    format_columns = options.get("format_columns", [])
    path_columns = options.get("local_path_columns", [])
    hash_columns = options.get("hash_columns", [])
    root_column = options.get("root_column", "")
    local_root_value = options.get("local_root_value", "")
    unparsed_rows = 0
    for row in rows:
        before = len(declarations)
        identifier = first_value(row, id_columns)
        program = first_value(row, program_columns) or "NO_DETERMINADO"
        edition = first_value(row, edition_columns) or "NO_DETERMINADO"
        object_name = first_value(row, object_columns) or identifier or "NO_DETERMINADO"
        declared_format = first_value(row, format_columns)
        path_value = first_value(row, path_columns)
        if root_column and str(row.get(root_column, "")).strip() != local_root_value:
            path_value = ""
        digest = first_value(row, hash_columns).lower()
        if digest and not HASH_RE.fullmatch(digest):
            digest = ""
        url_values: list[str] = []
        for column in url_columns:
            url_values.extend(urls_in(str(row.get(column, "") or "")))
        # Preserve every distinct delivery/localizer declared in the row.
        for position, url in enumerate(url_values):
            declarations.append(_declaration(
                input_id, row, f"tsv-url:{position}:{url}", url, identifier or Path(url.split("?", 1)[0]).name,
                url=url,
                fuente_programa=program,
                edicion_periodo=edition,
                objeto_logico=object_name,
                formato=infer_format(url, declared_format),
            ))
        if path_value or digest:
            actual = corpus_root / path_value if path_value else None
            actual_digest = digest
            if actual and actual.is_file() and not actual_digest:
                actual_digest = sha256_file(actual, cache)
            declarations.append(_declaration(
                input_id, row, "tsv-local", f"data_raw:{path_value}" if path_value else f"sha256:{actual_digest}", identifier or path_value,
                local_path=path_value,
                sha256=actual_digest,
                fuente_programa=program,
                edicion_periodo=edition,
                objeto_logico=object_name,
                formato=infer_format(path_value, declared_format),
            ))
        if not url_values and not path_value and not digest and identifier:
            declarations.append(_declaration(
                input_id, row, "tsv-declarative", f"declaracion:{input_id}:{identifier}", identifier,
                fuente_programa=program,
                edicion_periodo=edition,
                objeto_logico=object_name,
                formato=declared_format or "DECLARACION",
            ))
        if len(declarations) == before:
            unparsed_rows += 1
    if unparsed_rows:
        errors.append(f"FILAS_SIN_DECLARACION_PARSEABLE:{unparsed_rows}")
    return len(declarations) + unparsed_rows, declarations, errors


def parse_text_urls(path: Path, input_id: str, parser: str) -> tuple[int, list[Declaration], list[str]]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return 0, [], [f"TEXTO:{type(exc).__name__}:{exc}"]
    declarations: list[Declaration] = []
    heading = "NO_DETERMINADO"
    occurrences = 0
    lines = text.splitlines()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip() or heading
            numbered = re.match(r"^\d+\.\s+(.+)$", heading)
            if numbered:
                name = numbered.group(1).strip()
                occurrences += 1
                declarations.append(_declaration(
                    input_id, {"encabezado": heading}, f"{parser}:heading:{name}",
                    f"declaracion:{input_id}:{name}", name,
                    fuente_programa=name,
                    objeto_logico=name,
                    formato="DECLARACION_CATALOGO",
                ))
        for position, url in enumerate(urls_in(line)):
            occurrences += 1
            declarations.append(_declaration(
                input_id, {"linea": stripped, "contexto": heading}, f"{parser}:{position}:{url}", url,
                Path(url.split("?", 1)[0]).name or heading,
                url=url,
                fuente_programa=heading,
                objeto_logico=heading,
                formato=infer_format(url),
            ))
    # Horizontal catalog tables can declare sources even without a URL.
    for index in range(len(lines) - 2):
        header = lines[index].strip()
        separator = lines[index + 1].strip()
        if not (header.startswith("|") and separator.startswith("|") and "---" in separator):
            continue
        columns = [cell.strip().casefold() for cell in header.strip("|").split("|")]
        source_positions = [position for position, value in enumerate(columns) if value in {"fuente", "nombre"}]
        if not source_positions:
            continue
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].strip().startswith("|"):
            cells = [cell.strip().strip("*") for cell in lines[cursor].strip().strip("|").split("|")]
            for position in source_positions:
                if position >= len(cells):
                    continue
                name = cells[position].strip()
                if not name or name.casefold() in {"fuente", "nombre"}:
                    continue
                occurrences += 1
                declarations.append(_declaration(
                    input_id, {"tabla": header, "fila": lines[cursor].strip()},
                    f"{parser}:table:{position}:{name}", f"declaracion:{input_id}:{name}", name,
                    fuente_programa=name,
                    objeto_logico=name,
                    formato="DECLARACION_CATALOGO",
                ))
            cursor += 1
    return occurrences, declarations, []


def assign_declaration_ids(declarations: list[Declaration]) -> None:
    groups: dict[tuple[str, str], list[Declaration]] = defaultdict(list)
    for declaration in declarations:
        groups[(declaration.input_id, declaration.fingerprint)].append(declaration)
    for (input_id, fingerprint), values in sorted(groups.items()):
        for ordinal, declaration in enumerate(sorted(values, key=lambda d: (d.localizador, d.identificador)), 1):
            declaration.declaration_id = stable_id("DEC-", input_id, fingerprint, str(ordinal), size=24)


def reconcile(declarations: list[Declaration], corpus_root: Path) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    # Toda representación local se reconcilia primero contra sus bytes. Así una
    # ruta nunca hereda silenciosamente un hash declarado incorrecto y toda
    # identidad local posterior descansa en el contenido observado.
    for declaration in declarations:
        if not declaration.local_path:
            continue
        relative = Path(declaration.local_path).as_posix()
        actual = corpus_root / relative
        if not actual.is_file():
            continue
        observed = sha256_file(actual)
        declared = declaration.sha256.lower() if HASH_RE.fullmatch(declaration.sha256) else ""
        declaration.hash_declarado = declared or "NO_DECLARADO"
        declaration.hash_observado = observed
        declaration.sha256 = observed

    union = UnionFind(len(declarations))
    key_members: dict[str, list[int]] = defaultdict(list)
    url_members: dict[str, list[int]] = defaultdict(list)
    for index, declaration in enumerate(declarations):
        if declaration.sha256 and HASH_RE.fullmatch(declaration.sha256):
            key_members[f"hash:{declaration.sha256.lower()}"].append(index)
        if declaration.url:
            url_members[declaration.url].append(index)
        if declaration.local_path:
            key_members[f"path:data_raw:{Path(declaration.local_path).as_posix()}"].append(index)
    for members in key_members.values():
        for other in members[1:]:
            union.union(members[0], other)
    components: dict[int, list[int]] = defaultdict(list)
    for index in range(len(declarations)):
        components[union.find(index)].append(index)

    assets: list[dict[str, str]] = []
    families: list[dict[str, str]] = []
    for members in components.values():
        values = [declarations[index] for index in members]
        hashes = sorted({d.sha256.lower() for d in values if HASH_RE.fullmatch(d.sha256)})
        urls = sorted({d.url for d in values if d.url})
        paths = sorted({Path(d.local_path).as_posix() for d in values if d.local_path})
        if len(hashes) > 1:
            raise AssertionError("COMPONENTE_CON_HASHES_INCOMPATIBLES:" + ";".join(hashes))
        identity = f"hash:{hashes[0]}" if hashes else f"declaration:{min(d.declaration_id for d in values)}"
        activo_id = stable_id("ACT-", identity, size=24)
        actual_paths = [relative for relative in paths if (corpus_root / relative).is_file()]
        duplicate_local = len(actual_paths) > 1 and len(hashes) == 1
        object_id = stable_id("OBJ-", activo_id, size=24)
        family_id = stable_id("FAM-", f"hash:{hashes[0]}", size=24) if duplicate_local else "NO_DETERMINADO"
        for declaration in values:
            declaration.activo_id = activo_id
            shared: list[str] = []
            for key, label in (
                (f"hash:{declaration.sha256.lower()}" if declaration.sha256 else "", "HASH_IDENTICO"),
                (f"path:data_raw:{Path(declaration.local_path).as_posix()}" if declaration.local_path else "", "RUTA_EXACTA"),
            ):
                if key and len(key_members.get(key, [])) > 1:
                    shared.append(label)
            if declaration.url and len(url_members[declaration.url]) > 1:
                shared.append("URL_EXACTA_SOLO_LOCALIZACION")
            if (
                declaration.hash_declarado not in {"", "NO_DECLARADO"}
                and declaration.hash_declarado != declaration.hash_observado
            ):
                shared.append("HASH_DECLARADO_DIFIERE_DE_BYTES")
            declaration.metodo_reconciliacion = ";".join(shared) if shared else "SIN_RECONCILIACION"
            declaration.evidencia_reconciliacion = ";".join(shared) if shared else declaration.localizador
            if any(value in shared for value in ("HASH_IDENTICO", "RUTA_EXACTA")):
                declaration.estado_reconciliacion = "IDENTIDAD_VERIFICADA"
            elif "URL_EXACTA_SOLO_LOCALIZACION" in shared:
                declaration.estado_reconciliacion = "LOCALIZACION_COMPARTIDA_SIN_IDENTIDAD"
            elif declaration.url or declaration.local_path or declaration.sha256:
                declaration.estado_reconciliacion = "ACTIVO_UNICO"
            else:
                declaration.estado_reconciliacion = "NO_DETERMINADO"
        select = lambda attr, default="NO_DETERMINADO": sorted({getattr(d, attr) for d in values if getattr(d, attr) and getattr(d, attr) != "NO_DETERMINADO"})[0] if any(getattr(d, attr) and getattr(d, attr) != "NO_DETERMINADO" for d in values) else default
        assets.append({
            "activo_id": activo_id,
            "fuente_programa": select("fuente_programa"),
            "edicion_periodo": select("edicion_periodo"),
            "objeto_logico_id": object_id,
            "objeto_logico": select("objeto_logico"),
            "formato": select("formato"),
            "url_localizador_principal": urls[0] if urls else "NO_DETERMINADO",
            "estado_adquisicion": "ADQUIRIDO" if actual_paths else "DECLARADO_NO_ADQUIRIDO",
            "ruta_local": actual_paths[0] if actual_paths else "NO_DETERMINADO",
            "hash_local": hashes[0] if actual_paths and hashes else "NO_DETERMINADO",
            "estado_inspeccion": "ADQUIRIDO_NO_INSPECCIONADO" if actual_paths else "NO_INSPECCIONADO",
            "reporte_inspeccion_ref": "NO_DETERMINADO",
            "familia_logica_id": family_id,
            "observaciones": (
                f"declaraciones={len(values)};rutas_locales={len(actual_paths)};"
                f"duplicado_verificado={'SI' if duplicate_local else 'NO'}"
            ),
        })
        families.append({
            "activo_id": activo_id,
            "objeto_logico_id": object_id,
            "familia_logica_id": family_id,
            "tipo_relacion": "DUPLICADO_VERIFICADO" if duplicate_local else "NO_DETERMINADO",
            "evidencia_estructural": f"sha256:{hashes[0]}" if duplicate_local else "NO_DETERMINADO",
            "reserva": "Identidad de familia no inferida por nombre" if not duplicate_local else "NINGUNA",
        })

    # Una landing común puede agrupar activos lógicamente, pero nunca altera su
    # identidad. La proyección sigue siendo 1:1 activo→fila de familia; si un
    # activo participa en varias landings se conserva la primera canónica y el
    # detalle completo permanece en las declaraciones/candidatos.
    assets_by_url: dict[str, set[str]] = defaultdict(set)
    for declaration in declarations:
        if declaration.url:
            assets_by_url[declaration.url].add(declaration.activo_id)
    shared_url_by_asset: dict[str, list[str]] = defaultdict(list)
    for url, active_ids in assets_by_url.items():
        if len(active_ids) > 1:
            for activo_id in active_ids:
                shared_url_by_asset[activo_id].append(url)
    asset_rows = {row["activo_id"]: row for row in assets}
    family_rows = {row["activo_id"]: row for row in families}
    for activo_id, urls_shared in shared_url_by_asset.items():
        if family_rows[activo_id]["tipo_relacion"] == "DUPLICADO_VERIFICADO":
            continue
        canonical_url = sorted(urls_shared)[0]
        family_id = stable_id("FAM-", f"url-localizacion:{canonical_url}", size=24)
        asset_rows[activo_id]["familia_logica_id"] = family_id
        family_rows[activo_id].update({
            "familia_logica_id": family_id,
            "tipo_relacion": "LOCALIZADOR_COMPARTIDO",
            "evidencia_estructural": f"url:{canonical_url}",
            "reserva": "La URL agrupa declaraciones; no prueba identidad de contenido",
        })

    # Candidates never change identity. They flag exact basenames/identifiers shared
    # by separate assets when no structural key joined them.
    candidate_groups: dict[str, set[str]] = defaultdict(set)
    for declaration in declarations:
        basename = Path(declaration.url.split("?", 1)[0]).name if declaration.url else Path(declaration.local_path).name if declaration.local_path else ""
        if basename:
            candidate_groups[basename.casefold()].add(declaration.activo_id)
    candidates: list[dict[str, str]] = []
    for basename, active_ids in sorted(candidate_groups.items()):
        if 1 < len(active_ids) <= 25:
            ids = sorted(active_ids)
            candidates.append({
                "candidato_reconciliacion_id": stable_id("CREC-", basename, *ids, size=24),
                "activos_implicados": ";".join(ids),
                "declaraciones_implicadas": ";".join(sorted(d.declaration_id for d in declarations if d.activo_id in active_ids and ((Path(d.url.split('?', 1)[0]).name if d.url else Path(d.local_path).name if d.local_path else '').casefold() == basename))),
                "similitud_observada": f"nombre_archivo_exacto:{basename}",
                "razon_candidata": "Coincidencia nominal sin join estructural suficiente",
                "evidencia_pendiente": "Hash idéntico verificado, identificador oficial inequívoco o vínculo catálogo-entrega con contenido",
                "estado_revision": "PENDIENTE",
            })
    return sorted(assets, key=lambda row: row["activo_id"]), sorted(families, key=lambda row: row["activo_id"]), candidates


def write_tsv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def expand_specs(spec_path: Path, repo_root: Path, corpus_root: Path) -> list[dict[str, Any]]:
    payload = json.loads(spec_path.read_text(encoding="utf-8"))
    expanded: list[dict[str, Any]] = []
    for spec in payload.get("inputs", []):
        root = repo_root if spec.get("root", "repo") == "repo" else corpus_root
        if "glob" in spec:
            for path in sorted(root.glob(spec["glob"]), key=lambda p: p.as_posix()):
                if path.is_file():
                    item = dict(spec)
                    item.pop("glob")
                    item["path"] = path.relative_to(root).as_posix()
                    expanded.append(item)
        else:
            expanded.append(dict(spec))
    return expanded


def build_snapshot(spec_path: Path, repo_root: Path, corpus_root: Path, output_dir: Path) -> dict[str, Any]:
    cache: dict[Path, str] = {}
    input_results: list[InputResult] = []
    all_declarations: list[Declaration] = []
    for spec in expand_specs(spec_path, repo_root, corpus_root):
        root_name = spec.get("root", "repo")
        root = repo_root if root_name == "repo" else corpus_root
        path = (root / spec.get("path", ".")).resolve()
        parser = spec["parser"]
        display = path.as_posix() if root_name == "corpus" else path.relative_to(repo_root).as_posix()
        input_id = stable_id("INP-", root_name, display, parser, size=20)
        if not path.exists():
            input_results.append(InputResult(input_id, path, display, spec.get("tipo", parser), parser, "NO_DETERMINADO", 0, 0, ["INPUT_NO_EXISTE"], "Input declarado faltante"))
            continue
        if parser == "corpus_tree":
            found, declarations, errors, input_hash = parse_corpus_tree(path, input_id, cache)
        else:
            input_hash = sha256_file(path, cache)
            if parser == "manifest_yaml":
                found, declarations, errors = parse_manifest(path, input_id, corpus_root, cache)
            elif parser == "xml_urls":
                found, declarations, errors = parse_xml_urls(path, input_id)
            elif parser == "tsv":
                found, declarations, errors = parse_tsv(path, input_id, spec.get("options", {}), corpus_root, cache)
            elif parser in {"markdown_urls", "html_urls", "yaml_urls"}:
                found, declarations, errors = parse_text_urls(path, input_id, parser)
            else:
                found, declarations, errors = 0, [], [f"PARSER_NO_SOPORTADO:{parser}"]
        if errors:
            reserve = "Errores concretos conservados; no se inventaron declaraciones"
        elif found and not declarations:
            reserve = "INPUT_CON_REGISTROS_SIN_LOCALIZADOR_O_IDENTIFICADOR_PARSEABLE"
        elif not found:
            reserve = "INPUT_SIN_DECLARACIONES_DE_ACTIVOS_PARSEABLES"
        else:
            reserve = "NINGUNA"
        result = InputResult(input_id, path, display, spec.get("tipo", parser), parser, input_hash, found, len(declarations), errors, reserve, declarations)
        input_results.append(result)
        all_declarations.extend(declarations)

    assign_declaration_ids(all_declarations)
    assets, families, candidates = reconcile(all_declarations, corpus_root)
    local_files = sorted(
        (path for path in corpus_root.rglob("*") if path.is_file()),
        key=lambda path: path.relative_to(corpus_root).as_posix(),
    )
    local_digests = [sha256_file(path, cache) for path in local_files]
    for asset in assets:
        if asset["ruta_local"] == "NO_DETERMINADO":
            continue
        observed = sha256_file(corpus_root / asset["ruta_local"], cache)
        if asset["hash_local"] != observed:
            raise AssertionError(
                f"HASH_ACTIVO_NO_COINCIDE:{asset['activo_id']}:{asset['ruta_local']}"
            )
    input_rows = [{
        "input_id": value.input_id,
        "ruta": value.display_path,
        "tipo": value.tipo,
        "hash_input": value.hash_input,
        "parser": value.parser,
        "declaraciones_encontradas": value.found,
        "declaraciones_parseadas": value.parsed,
        "errores": ";".join(value.errors) if value.errors else "NINGUNO",
        "reserva": value.reserve,
    } for value in sorted(input_results, key=lambda item: item.input_id)]
    declaration_rows = [{
        "declaracion_id": value.declaration_id,
        "input_id": value.input_id,
        "localizador_declarado": value.localizador,
        "identificador_declarado": value.identificador,
        "activo_id": value.activo_id,
        "metodo_reconciliacion": value.metodo_reconciliacion,
        "evidencia_reconciliacion": value.evidencia_reconciliacion,
        "estado_reconciliacion": value.estado_reconciliacion,
    } for value in sorted(all_declarations, key=lambda item: item.declaration_id)]
    hash_discrepancy_rows = [{
        "declaracion_id": value.declaration_id,
        "input_id": value.input_id,
        "ruta_local": Path(value.local_path).as_posix(),
        "hash_declarado": value.hash_declarado,
        "hash_observado": value.hash_observado,
        "resolucion_t0": "IDENTIDAD_POR_BYTES_OBSERVADOS",
        "reserva": "El hash declarado se conserva como discrepancia; no se usó para fusionar activos",
    } for value in sorted(all_declarations, key=lambda item: item.declaration_id) if (
        value.hash_declarado not in {"", "NO_DECLARADO"}
        and value.hash_declarado != value.hash_observado
    )]

    write_tsv(output_dir / "fuentes-t0.tsv", list(input_rows[0]) if input_rows else ["input_id"], input_rows)
    write_tsv(output_dir / "declaraciones-activos-t0.tsv", [
        "declaracion_id", "input_id", "localizador_declarado", "identificador_declarado",
        "activo_id", "metodo_reconciliacion", "evidencia_reconciliacion", "estado_reconciliacion",
    ], declaration_rows)
    write_tsv(output_dir / "universo-declarado-t0.tsv", [
        "activo_id", "fuente_programa", "edicion_periodo", "objeto_logico_id", "objeto_logico",
        "formato", "url_localizador_principal", "estado_adquisicion", "ruta_local", "hash_local",
        "estado_inspeccion", "reporte_inspeccion_ref", "familia_logica_id", "observaciones",
    ], assets)
    write_tsv(output_dir / "familias-activos.tsv", [
        "activo_id", "objeto_logico_id", "familia_logica_id", "tipo_relacion", "evidencia_estructural", "reserva",
    ], families)
    write_tsv(output_dir / "candidatos-reconciliacion-activos.tsv", [
        "candidato_reconciliacion_id", "activos_implicados", "declaraciones_implicadas",
        "similitud_observada", "razon_candidata", "evidencia_pendiente", "estado_revision",
    ], candidates)
    write_tsv(output_dir / "discrepancias-hash-local.tsv", [
        "declaracion_id", "input_id", "ruta_local", "hash_declarado",
        "hash_observado", "resolucion_t0", "reserva",
    ], hash_discrepancy_rows)
    for filename, fields in {
        "activos-descubiertos-durante-ronda.tsv": ["activo_descubierto_id", "fecha", "origen", "localizador", "estado", "reserva"],
        "excepciones-cegamiento.tsv": ["excepcion_cegamiento_id", "tarea_observacion_id", "campo_revelado", "razon_indispensable", "autoridad", "alcance", "riesgo_sesgo", "fecha"],
    }.items():
        path = output_dir / filename
        if not path.exists():
            write_tsv(path, fields, [])

    core = {
        "version_contrato": "1.0",
        "inputs": input_rows,
        "declaraciones": declaration_rows,
        "activos": assets,
        "familias": families,
        "candidatos_reconciliacion": candidates,
    }
    snapshot_hash = hashlib.sha256(canonical_json(core).encode("utf-8")).hexdigest()
    local_unique_contents = len(set(local_digests))
    conservative_components = len(assets)
    acquired_verified = sum(row["estado_adquisicion"] == "ADQUIRIDO" for row in assets)
    snapshot = {
        "snapshot_t0_sha256": snapshot_hash,
        "t0_congelado": True,
        "routing_modelos_verificado": False,
        "modelo_efectivo": "NO_OBSERVABLE",
        "effort_efectivo": "NO_OBSERVABLE",
        "corpus_root": corpus_root.as_posix(),
        "conteos": {
            "inputs": len(input_rows),
            "declaraciones_parseadas": len(declaration_rows),
            "representaciones_locales": len(local_files),
            "contenidos_locales_sha256_unicos": local_unique_contents,
            "identidades_locales_verificadas": acquired_verified,
            "duplicados_locales_reales": len(local_digests) - local_unique_contents,
            "hashes_representaciones_locales_verificados": len(local_files),
            "componentes_declarados_conservadores": conservative_components,
            "cota_superior_activos_declarados": conservative_components,
            "denominador_activos_declarados": "NO_DETERMINADO",
            "numerador_adquirido_identidades_locales_verificadas": acquired_verified,
            "cobertura_adquisicion_puntual": "NO_DETERMINADO",
            "candidatos_reconciliacion": len(candidates),
            "inputs_con_error": sum(row["errores"] != "NINGUNO" for row in input_rows),
            "discrepancias_hash_local": len(hash_discrepancy_rows),
        },
        "rotulacion_denominadores": {
            "declaraciones_parseadas": "filas de procedencia conservadas; no son activos",
            "representaciones_locales": "archivos regulares enumerados directamente en corpus_root",
            "contenidos_locales_sha256_unicos": "valores SHA-256 distintos observados en las representaciones locales",
            "identidades_locales_verificadas": "identidades de contenido local sustentadas por SHA-256 observado",
            "componentes_declarados_conservadores": (
                "componentes tras aplicar solo joins estructurales; conservan por separado "
                "declaraciones cuya identidad no pudo verificarse"
            ),
            "cota_superior_activos_declarados": (
                "máximo conservador compatible con las declaraciones parseadas; no es una "
                "estimación puntual de activos únicos"
            ),
            "denominador_activos_declarados": (
                "NO_DETERMINADO mientras existan candidatos de reconciliación sin evidencia estructural"
            ),
            "cobertura_adquisicion_puntual": (
                "NO_DETERMINADO: el numerador local verificado no se divide entre la cota superior"
            ),
        },
        "hashes_outputs": {
            name: sha256_file(output_dir / name)
            for name in (
                "fuentes-t0.tsv", "declaraciones-activos-t0.tsv", "universo-declarado-t0.tsv",
                "familias-activos.tsv", "candidatos-reconciliacion-activos.tsv",
                "discrepancias-hash-local.tsv",
            )
        },
        "core_componentes_sha256": {
            "inputs": hashlib.sha256(canonical_json(input_rows).encode("utf-8")).hexdigest(),
            "declaraciones": hashlib.sha256(canonical_json(declaration_rows).encode("utf-8")).hexdigest(),
            "activos": hashlib.sha256(canonical_json(assets).encode("utf-8")).hexdigest(),
            "familias": hashlib.sha256(canonical_json(families).encode("utf-8")).hexdigest(),
            "candidatos_reconciliacion": hashlib.sha256(canonical_json(candidates).encode("utf-8")).hexdigest(),
        },
    }
    (output_dir / "snapshot-t0.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--corpus-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    snapshot = build_snapshot(args.spec.resolve(), args.repo_root.resolve(), args.corpus_root.resolve(), args.output_dir.resolve())
    print(json.dumps({"ok": True, **snapshot["conteos"], "snapshot_t0_sha256": snapshot["snapshot_t0_sha256"]}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
