#!/usr/bin/env python3
"""ACTO MAESTRA32-E3 · EXTRACTOR-DTA (v2) — genera
data/inventario-reactivos-ext-v1_0.tsv.

Rama (a) de FP-175: formatos estadísticos .dta/.sav/.por/.sas7bdat/.xpt
(Stata/SPSS/SAS, vía `pyreadstat`), .dbf (dBase, vía `dbfread`) y
.rdata/.rds (R, vía `pyreadr`), sueltos o como miembros de zip, sobre el
perímetro re-derivado de `data/cobertura-composicion-v1_0.tsv` causa B
(125 .zip + 8 .dta sueltos = 133 payloads — ver
forense/notas/2026-08-30-extractor-ext-spec.md, COMMIT-1).

Reutiliza sin editar: `sha256_file_12`, `sanitiza_celda` de
`tools/inventario_reactivos.py`, y `aplica_v1_1`, `aplica_v1_2`,
`familias_canonicas`, `carga_manifiesto` de `tools/etiqueta_v1_2.py`.
Metadato puro: nombres (y etiquetas donde el formato las tenga) de
variable — NUNCA se carga un valor de dato (`metadataonly=True` /
`load=False` / `list_objects` en todas las llamadas).

Fallos por payload se documentan como fila de error (variable_id=ERROR),
nunca se parchan ni se reintenta con otra heurística.
"""

from __future__ import annotations

import csv
import sys
import tempfile
import time
import traceback
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.inventario_reactivos import sha256_file_12, sanitiza_celda  # noqa: E402
from tools.etiqueta_v1_2 import (  # noqa: E402
    aplica_v1_1,
    aplica_v1_2,
    familias_canonicas,
    carga_manifiesto,
)

RAW_ROOT = REPO_ROOT / "data" / "raw"
COBERTURA_PATH = REPO_ROOT / "data" / "cobertura-composicion-v1_0.tsv"
REACTIVOS_V1_1 = REPO_ROOT / "data" / "inventario-reactivos-v1_1.tsv"
MANIFIESTO = REPO_ROOT / "data" / "manifiesto.yaml"
OUT_PATH = REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv"

FIELDS = [
    "payload_id", "sha256_12", "instrumento", "ola", "archivo_miembro",
    "variable_id", "texto_reactivo", "metodo", "universo_declarado",
]

EXT_STATA_SPSS_SAS = {
    ".dta": "INSPECT_STATA",
    ".sav": "INSPECT_SPSS",
    ".por": "INSPECT_SPSS",
    ".sas7bdat": "INSPECT_SAS",
    ".xpt": "INSPECT_SAS",
}
EXT_DBF = {".dbf"}
EXT_RDATA = {".rdata", ".rds"}
EXT_DESPACHADAS = set(EXT_STATA_SPSS_SAS) | EXT_DBF | EXT_RDATA


def derivar_perimetro() -> list[str]:
    """Rama (a): 125 .zip + 8 .dta sueltos de causa B en cobertura-composicion."""
    with COBERTURA_PATH.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    causa_b = [r for r in rows if r["causa"] == "B"]
    zips = sorted(r["payload_id"] for r in causa_b if r["formato"] == ".zip")
    dtas = sorted(r["payload_id"] for r in causa_b if r["formato"] == ".dta")
    return zips + dtas


def instrumento_para(payload_id: str, manifiesto: dict, familias: list[str]) -> str:
    nuevo = aplica_v1_1(payload_id)
    if nuevo:
        return nuevo
    nuevo, _campo = aplica_v1_2(payload_id, manifiesto, familias)
    if nuevo:
        return nuevo
    return "(sin-instrumento-derivable)"


def inspect_stata_spss_sas(path: Path, metodo: str) -> tuple[list[str], list[str]]:
    import pyreadstat
    lector = {
        "INSPECT_STATA": pyreadstat.read_dta,
        "INSPECT_SPSS": pyreadstat.read_sav if path.suffix.lower() == ".sav" else pyreadstat.read_por,
        "INSPECT_SAS": pyreadstat.read_sas7bdat if path.suffix.lower() == ".sas7bdat" else pyreadstat.read_xport,
    }[metodo]
    _df, meta = lector(str(path), metadataonly=True)
    nombres = list(meta.column_names)
    etiquetas_map = dict(getattr(meta, "column_names_to_labels", {}) or {})
    etiquetas = [etiquetas_map.get(n, "") or "" for n in nombres]
    return nombres, etiquetas


def inspect_dbf(path: Path) -> tuple[list[str], list[str]]:
    from dbfread import DBF
    tabla = DBF(str(path), load=False, char_decode_errors="replace")
    nombres = list(tabla.field_names)
    return nombres, ["" for _ in nombres]


def inspect_rdata(path: Path) -> tuple[list[str], list[str]]:
    import pyreadr
    objetos = pyreadr.list_objects(str(path))
    nombres: list[str] = []
    for entrada in objetos:
        nombres.extend(entrada.get("columns", []))
    return nombres, ["" for _ in nombres]


def metodo_y_extractor(ext: str):
    ext = ext.lower()
    if ext in EXT_STATA_SPSS_SAS:
        metodo = EXT_STATA_SPSS_SAS[ext]
        return metodo, lambda p: inspect_stata_spss_sas(p, metodo)
    if ext in EXT_DBF:
        return "INSPECT_DBF", inspect_dbf
    if ext in EXT_RDATA:
        return "INSPECT_RDATA", inspect_rdata
    return None, None


def filas_para_archivo(payload_id: str, sha12: str, archivo_miembro: str,
                        path: Path, instrumento: str) -> list[dict]:
    ext = path.suffix.lower()
    metodo, extractor = metodo_y_extractor(ext)
    if metodo is None:
        return []
    try:
        nombres, etiquetas = extractor(path)
    except Exception as exc:  # noqa: BLE001 - fallo por payload se documenta, no se parcha
        msg = f"{type(exc).__name__}: {exc}"[:200]
        return [{
            "payload_id": sanitiza_celda(payload_id),
            "sha256_12": sha12,
            "instrumento": sanitiza_celda(instrumento),
            "ola": "NO_DETERMINADO",
            "archivo_miembro": sanitiza_celda(archivo_miembro),
            "variable_id": "ERROR",
            "texto_reactivo": sanitiza_celda(msg),
            "metodo": metodo,
            "universo_declarado": "PRESENTE_EN_DATA_RAW",
        }]
    filas = []
    for nombre, etiqueta in zip(nombres, etiquetas):
        if not str(nombre).strip():
            continue
        filas.append({
            "payload_id": sanitiza_celda(payload_id),
            "sha256_12": sha12,
            "instrumento": sanitiza_celda(instrumento),
            "ola": "NO_DETERMINADO",
            "archivo_miembro": sanitiza_celda(archivo_miembro),
            "variable_id": sanitiza_celda(nombre),
            "texto_reactivo": sanitiza_celda(etiqueta),
            "metodo": metodo,
            "universo_declarado": "PRESENTE_EN_DATA_RAW",
        })
    return filas


def procesar_payload(payload_id: str, manifiesto: dict, familias: list[str]) -> tuple[list[dict], dict]:
    """Devuelve (filas, stats) donde stats trae conteos de miembros ignorados."""
    path = RAW_ROOT / payload_id
    sha12 = sha256_file_12(path)
    instrumento = instrumento_para(payload_id, manifiesto, familias)
    stats = {"miembros_despachados": 0, "miembros_ignorados": 0}

    if path.suffix.lower() == ".dta":
        filas = filas_para_archivo(payload_id, sha12, payload_id, path, instrumento)
        if filas:
            stats["miembros_despachados"] = 1
        return filas, stats

    filas: list[dict] = []
    with zipfile.ZipFile(path) as zf:
        nombres = zf.namelist()
        for nombre_miembro in nombres:
            ext = Path(nombre_miembro).suffix.lower()
            if ext not in EXT_DESPACHADAS:
                stats["miembros_ignorados"] += 1
                continue
            stats["miembros_despachados"] += 1
            with tempfile.TemporaryDirectory() as tmpdir:
                try:
                    extraido = zf.extract(nombre_miembro, path=tmpdir)
                except Exception as exc:  # noqa: BLE001
                    msg = f"EXTRACT_{type(exc).__name__}: {exc}"[:200]
                    metodo, _ = metodo_y_extractor(ext)
                    filas.append({
                        "payload_id": sanitiza_celda(payload_id),
                        "sha256_12": sha12,
                        "instrumento": sanitiza_celda(instrumento),
                        "ola": "NO_DETERMINADO",
                        "archivo_miembro": sanitiza_celda(nombre_miembro),
                        "variable_id": "ERROR",
                        "texto_reactivo": sanitiza_celda(msg),
                        "metodo": metodo or "DESCONOCIDO",
                        "universo_declarado": "PRESENTE_EN_DATA_RAW",
                    })
                    continue
                filas.extend(filas_para_archivo(
                    payload_id, sha12, nombre_miembro, Path(extraido), instrumento,
                ))
    return filas, stats


def main() -> int:
    t0 = time.time()
    perimetro = derivar_perimetro()
    assert len(perimetro) == 133, f"perimetro re-derivado = {len(perimetro)}, esperado 133"

    manifiesto = carga_manifiesto(MANIFIESTO)
    familias = familias_canonicas(REACTIVOS_V1_1)

    todas_filas: list[dict] = []
    payloads_con_fila = set()
    payloads_con_error_solo = set()
    fallos_crudos: list[str] = []
    por_familia_miembros_despachados = 0
    por_familia_miembros_ignorados = 0

    for payload_id in perimetro:
        filas, stats = procesar_payload(payload_id, manifiesto, familias)
        por_familia_miembros_despachados += stats["miembros_despachados"]
        por_familia_miembros_ignorados += stats["miembros_ignorados"]
        todas_filas.extend(filas)
        no_error = [f for f in filas if f["variable_id"] != "ERROR"]
        if no_error:
            payloads_con_fila.add(payload_id)
        errores = [f for f in filas if f["variable_id"] == "ERROR"]
        for e in errores:
            fallos_crudos.append(f"{payload_id}\t{e['archivo_miembro']}\t{e['metodo']}\t{e['texto_reactivo']}")
        if errores and not no_error:
            payloads_con_error_solo.add(payload_id)

    n_perimetro = len(perimetro)
    n_con_fila = len(payloads_con_fila)
    pct_cobertura = 100 * n_con_fila / n_perimetro if n_perimetro else 0.0
    falsador_disparado = pct_cobertura < 50.0

    total_filas = len([f for f in todas_filas if f["variable_id"] != "ERROR"])
    filas_con_texto = len([f for f in todas_filas if f["variable_id"] != "ERROR" and f["texto_reactivo"]])
    pct_texto = 100 * filas_con_texto / total_filas if total_filas else 0.0

    por_metodo: dict[str, int] = {}
    for f in todas_filas:
        if f["variable_id"] == "ERROR":
            continue
        por_metodo[f["metodo"]] = por_metodo.get(f["metodo"], 0) + 1

    cabecera = [
        f"# data/inventario-reactivos-ext-v1_0.tsv -- ACTO MAESTRA32-E3 · EXTRACTOR-DTA (v2), COMMIT-2",
        f"# Rama (a) de FP-175 (mesa, 30/ago/2026): formatos estadisticos .dta/.sav/.por/.sas7bdat/.xpt (pyreadstat"
        f" metadataonly=True), .dbf (dbfread, load=False) y .rdata/.rds (pyreadr list_objects), sueltos o miembros"
        f" de zip, sobre el perimetro re-derivado de data/cobertura-composicion-v1_0.tsv causa B: 125 .zip + 8 .dta"
        f" sueltos = 133 payloads. Metadato puro: NUNCA se carga un valor de dato.",
        f"# Cobertura: payloads con >=1 fila = {n_con_fila}/{n_perimetro} ({pct_cobertura:.1f}%); "
        f"falsador COMMIT-1(e) <50% {'DISPARADO' if falsador_disparado else 'no disparado'}. "
        f"Filas con texto_reactivo no vacio = {filas_con_texto}/{total_filas} ({pct_texto:.1f}%) "
        f"-- .dbf/.rdata solo dan nombres, por diseno de biblioteca.",
        f"# Reutiliza sin editar: tools/inventario_reactivos.py (sha256_file_12, sanitiza_celda), "
        f"tools/etiqueta_v1_2.py (aplica_v1_1, aplica_v1_2, familias_canonicas, carga_manifiesto). "
        f"Fallos por payload documentados como fila ERROR, no parchados.",
    ]

    with OUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        for linea in cabecera:
            handle.write(linea + "\n")
        handle.write("\t".join(FIELDS) + "\n")
        for fila in todas_filas:
            handle.write("\t".join(fila[c] for c in FIELDS) + "\n")

    print(f"perimetro: {n_perimetro}")
    print(f"payloads con >=1 fila: {n_con_fila}/{n_perimetro} ({pct_cobertura:.2f}%)")
    print(f"falsador <50%: {'DISPARADO' if falsador_disparado else 'no disparado'}")
    print(f"filas totales (sin ERROR): {total_filas}")
    print(f"filas con texto_reactivo no vacio: {filas_con_texto}/{total_filas} ({pct_texto:.2f}%)")
    print(f"por metodo: {por_metodo}")
    print(f"miembros de zip despachados: {por_familia_miembros_despachados}, ignorados: {por_familia_miembros_ignorados}")
    print(f"payloads con SOLO error (0 filas utiles): {len(payloads_con_error_solo)}")
    if fallos_crudos:
        print(f"--- {len(fallos_crudos)} fallos crudos ---")
        for linea in fallos_crudos:
            print(linea)
    print(f"tiempo total: {time.time()-t0:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
