#!/usr/bin/env python3
"""ACTO MAESTRA31-E4 · ORDEN-SUPERIOR — genera data/inventario-reactivos-v1_0.tsv.

Consumidor delgado FUERA de tools/curador_registro/: no reimplementa ningún
parser. Importa `inspect_one` (y las funciones de bajo nivel que usa) de
`tools/curador_registro/inspect_assets.py` sin editar ese módulo, y lo invoca
sobre el universo conocido = payloads presentes hoy en data/raw.

Regla de tope: cero extractores nuevos. Un formato que `inspect_one` no
despacha (ver dispatch en inspect_assets.py: zip/pdf/xlsx/xls/html/csv-tsv-txt/
json/xml) produce una fila NO-EXTRAIDO:<extension>, no un intento de parseo.

CERO emparejamiento contra tablas de variables ni contra milpa/. CERO red/API.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.curador_registro.inspect_assets import inspect_one  # noqa: E402

RAW_ROOT = REPO_ROOT / "data" / "raw"
OUT_PATH = REPO_ROOT / "data" / "inventario-reactivos-v1_0.tsv"

# ACTO MAESTRA37-L1: mapa de raíces conocidas -> (ruta absoluta, archivo de
# salida). "raw" preserva el comportamiento anterior a este acto byte a byte
# (RAW_ROOT, OUT_PATH); toda otra raíz se resuelve contra
# data/raices.local.yaml (gitignorada) y escribe a un archivo NUEVO, nunca
# sobre inventario-reactivos-v1_0.tsv.
RAICES_LOCAL_PATH = REPO_ROOT / "data" / "raices.local.yaml"


def _carga_raices_local() -> dict[str, str]:
    if not RAICES_LOCAL_PATH.exists():
        return {}
    raices: dict[str, str] = {}
    for linea in RAICES_LOCAL_PATH.read_text(encoding="utf-8").splitlines():
        despojada = linea.split("#", 1)[0].strip()
        if not despojada or ":" not in despojada:
            continue
        clave, _, valor = despojada.partition(":")
        raices[clave.strip()] = valor.strip()
    return raices


def resuelve_raiz(nombre: str) -> tuple[Path, Path]:
    """Devuelve (root_dir, out_path) para --raiz. 'raw' (default) es
    exactamente RAW_ROOT/OUT_PATH de antes de este acto -- no cambia."""
    if nombre == "raw":
        return RAW_ROOT, OUT_PATH
    raices = _carga_raices_local()
    if nombre not in raices:
        raise SystemExit(
            f"--raiz {nombre!r} no está en {RAICES_LOCAL_PATH} "
            f"(claves disponibles: {sorted(raices) or '(archivo ausente o vacío)'})"
        )
    root_dir = Path(raices[nombre]).expanduser()
    out_path = REPO_ROOT / "data" / f"inventario-reactivos-{nombre.replace('_', '-')}-v1_0.tsv"
    return root_dir, out_path

FIELDS = [
    "payload_id", "sha256_12", "instrumento", "ola", "archivo_miembro",
    "variable_id", "texto_reactivo", "metodo", "universo_declarado",
]


def sanitiza_celda(valor: str) -> str:
    """Colapsa tab/CR/LF a espacio — este repo escribe TSV plano de una línea
    por fila (sin comillas CSV; verificado contra las 4 tablas existentes),
    y csv.DictWriter con QUOTE_MINIMAL rompería esa convención al citar
    campos con salto de línea embebido (diccionarios .xlsx traen celdas
    multilínea)."""
    return " ".join(str(valor).replace("\t", " ").split())

# Formatos con soporte de columnas/campos en inspect_one (ver COMMIT-1 spec).
FORMATOS_CON_CAMPOS = {".zip", ".xlsx", ".csv", ".tsv", ".txt"}
# Formatos que inspect_one despacha pero sin columnas/campos extraíbles.
FORMATOS_SIN_CAMPOS = {".xls", ".html", ".json", ".pdf", ".xml"}

# Tope de tiempo por archivo (segundos) — documentado en COMMIT-2 meta.
LIMITE_SEGUNDOS_POR_ARCHIVO = 90


def sha256_file_12(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()[:12]


def enumerar_universo(root_dir: Path = RAW_ROOT) -> list[Path]:
    """Payloads bajo root_dir, excluyendo el bucle de symlink raw/raw (el
    único bucle conocido, específico de RAW_ROOT; otras raíces no lo tienen
    pero la guardia es inocua si no aplica)."""
    vistos: set[Path] = set()
    resultado: list[Path] = []
    for p in sorted(root_dir.rglob("*")):
        if not p.is_file():
            continue
        try:
            resolved = p.resolve()
        except OSError:
            continue
        # excluye el ciclo data/raw/raw -> data/raw (auto-referencia)
        if "raw/raw" in str(p.relative_to(root_dir)).replace("\\", "/"):
            continue
        if resolved in vistos:
            continue
        vistos.add(resolved)
        resultado.append(p)
    return resultado


def filas_desde_objetos(payload_id: str, sha12: str, instrumento: str, metodo: str,
                         objetos: list[dict]) -> list[dict]:
    filas = []
    for obj in objetos:
        tipo = obj.get("tipo", "")
        try:
            campos = json.loads(obj.get("campos", "[]"))
        except (json.JSONDecodeError, TypeError):
            campos = []
        if not campos:
            continue
        if tipo not in {"HOJA_XLSX", "TABLA_DELIMITADA"} and not isinstance(campos, list):
            continue
        # objetos de ZIP con campos vienen de miembros CSV/TSV/TXT/DBF; el
        # nombre del miembro es obj["objeto"]. Para XLSX top-level, obj["objeto"]
        # es el nombre de hoja. Para CSV/TSV/TXT top-level, obj["objeto"] es el
        # nombre del propio archivo.
        archivo_miembro = obj.get("objeto", "NO_APLICA")
        for variable_id in campos:
            if not str(variable_id).strip():
                continue
            filas.append({
                "payload_id": sanitiza_celda(payload_id),
                "sha256_12": sha12,
                "instrumento": sanitiza_celda(instrumento),
                "ola": "NO_DETERMINADO",
                "archivo_miembro": sanitiza_celda(archivo_miembro),
                "variable_id": sanitiza_celda(variable_id),
                "texto_reactivo": "",
                "metodo": metodo,
                "universo_declarado": "PRESENTE_EN_DATA_RAW",
            })
    return filas


def procesar(path: Path, root_dir: Path = RAW_ROOT) -> tuple[list[dict], str]:
    """Devuelve (filas, estado) para un payload. estado en {OK, NO-EXTRAIDO:<ext>,
    SIN-CAMPOS-EXTRAIBLES, ERROR:<tipo>}."""
    rel = path.relative_to(root_dir).as_posix()
    payload_id = rel
    instrumento = rel.split("/", 1)[0] if "/" in rel else "(raiz)"
    suffix = path.suffix.lower()
    sha12 = sha256_file_12(path)

    if suffix not in FORMATOS_CON_CAMPOS | FORMATOS_SIN_CAMPOS:
        return [], f"NO-EXTRAIDO:{suffix.lstrip('.') or 'SIN_EXTENSION'}"

    metodo_map = {
        ".zip": "INSPECT_ZIP", ".xlsx": "INSPECT_XLSX", ".csv": "INSPECT_CSV",
        ".tsv": "INSPECT_CSV", ".txt": "INSPECT_CSV", ".xls": "INSPECT_XLS",
        ".html": "INSPECT_HTML", ".json": "INSPECT_JSON", ".pdf": "INSPECT_PDF",
        ".xml": "INSPECT_XML",
    }
    metodo = metodo_map.get(suffix, "INSPECT_DESCONOCIDO")

    start = time.monotonic()
    try:
        structure, objects, boundary = inspect_one(path)
    except NotImplementedError as exc:
        return [], f"NO-EXTRAIDO:{exc}"
    except Exception as exc:  # noqa: BLE001 — se documenta, no se enmascara
        return [], f"ERROR:{type(exc).__name__}:{str(exc)[:200]}"
    elapsed = time.monotonic() - start

    filas = filas_desde_objetos(payload_id, sha12, instrumento, metodo, objects)
    estado = "OK" if filas else "SIN-CAMPOS-EXTRAIBLES"
    if elapsed > LIMITE_SEGUNDOS_POR_ARCHIVO:
        estado += f":LENTO={elapsed:.1f}s"
    return filas, estado


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raiz", default="raw",
        help="Clave de raíz a indexar. 'raw' (default) = comportamiento previo "
             "a MAESTRA37-L1, byte a byte (data/raw, escribe inventario-reactivos-v1_0.tsv). "
             "Cualquier otra clave se resuelve contra data/raices.local.yaml y "
             "escribe inventario-reactivos-<raiz>-v1_0.tsv, nunca sobre v1_0.tsv.",
    )
    args = parser.parse_args()
    root_dir, out_path = resuelve_raiz(args.raiz)

    universo = enumerar_universo(root_dir)
    todas_las_filas: list[dict] = []
    conteo_estado: dict[str, int] = {}
    payloads_cubiertos = 0

    for i, path in enumerate(universo, 1):
        filas, estado = procesar(path, root_dir)
        clave_estado = estado.split(":LENTO")[0]
        conteo_estado[clave_estado] = conteo_estado.get(clave_estado, 0) + 1
        cubierto = not (clave_estado.startswith("NO-EXTRAIDO") or clave_estado.startswith("ERROR"))
        if cubierto:
            payloads_cubiertos += 1
        todas_las_filas.extend(filas)
        if i % 100 == 0:
            print(f"... {i}/{len(universo)} payloads procesados", file=sys.stderr)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Escritura manual, TSV plano sin comillas CSV — convención de este repo
    # (las 4 tablas de variables existentes no usan comillas). Los valores ya
    # vienen saneados (sin tab/CR/LF) por sanitiza_celda(); metodo/universo
    # nunca traen esos caracteres.
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(FIELDS) + "\n")
        for fila in sorted(todas_las_filas, key=lambda r: (r["payload_id"], r["archivo_miembro"], r["variable_id"])):
            handle.write("\t".join(fila[f] for f in FIELDS) + "\n")

    resumen = {
        "raiz": args.raiz,
        "root_dir": str(root_dir),
        "out_path": str(out_path),
        "denominador_payloads": len(universo),
        "payloads_cubiertos": payloads_cubiertos,
        "filas_totales": len(todas_las_filas),
        "conteo_por_estado": conteo_estado,
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
