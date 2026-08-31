#!/usr/bin/env python3
"""ACTO MAESTRA32-E12 · EXTRACTOR-FD — genera data/inventario-fd-ext-v1_0.tsv.

Rama (b) de FP-175. Extiende data/inventario-fd-v1_1.tsv (29 instrumentos,
.xlsx unicamente) al perimetro de 46 payloads con nombre de ficha
descriptiva/diccionario en formatos que tools/inventario_reactivos.py:50
manda a FORMATOS_SIN_CAMPOS (.pdf, .xls, .html) mas .zip que envuelve esos
miembros. Regla y perimetro congelados en COMMIT-1:
forense/notas/2026-08-30-fd-ext-spec.md -- no se edita ese regex/reglas
despues de correr el control positivo (falsador pre-registrado).

Importa (no reimplementa): sha256_file_12 de tools/inventario_reactivos.py;
aplica_v1_1/aplica_v1_2/familias_canonicas/carga_manifiesto de
tools/etiqueta_v1_2.py. tools/inventario_fd.py NO se importa ni edita (su
perimetro es .xlsx, disjunto del de este acto).
"""

from __future__ import annotations

import re
import sys
import unicodedata
import warnings
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.inventario_reactivos import sha256_file_12  # noqa: E402
from tools.etiqueta_v1_2 import (  # noqa: E402
    aplica_v1_1, aplica_v1_2, familias_canonicas, carga_manifiesto,
)

RAW_ROOT = REPO_ROOT / "data" / "raw"
OUT_PATH = REPO_ROOT / "data" / "inventario-fd-ext-v1_0.tsv"
REACTIVOS_V1_1 = REPO_ROOT / "data" / "inventario-reactivos-v1_1.tsv"
REACTIVOS_V1_0 = REPO_ROOT / "data" / "inventario-reactivos-v1_0.tsv"
REACTIVOS_EXT_V1_0 = REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv"
MANIFIESTO = REPO_ROOT / "data" / "manifiesto.yaml"

FIELDS = [
    "payload_id", "sha256_12", "instrumento", "ola", "archivo_miembro",
    "variable_id", "texto_reactivo", "metodo", "universo_declarado",
]

ID_LABELS = ["mnemonico", "nemonico", "nombre de la columna", "nombre", "clave", "variable"]
TEXT_LABELS = ["pregunta y categoria", "pregunta",
               "descripcion del contenido del campo", "descripcion",
               "etiqueta", "observaciones"]

MNEMONICO_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,19}$")

FORMATOS_PERIMETRO = {".pdf", ".xls", ".html", ".zip"}


def sanitiza_celda(valor) -> str:
    if valor is None:
        return ""
    return " ".join(str(valor).replace("\t", " ").split())


def normaliza_rotulo(valor) -> str:
    if valor is None:
        return ""
    s = unicodedata.normalize("NFKD", str(valor))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s.strip().lower()).rstrip(":.")


def casa_patron_nombre(nombre: str) -> bool:
    """Misma regla que tools/inventario_fd.py::casa_patron_nombre()."""
    low = nombre.lower()
    if "diccionario" in low or "glosario" in low or "descriptor" in low:
        return True
    if re.search(r"(^|[_\-.])fd([_\-.]|$)", low):
        return True
    return False


def enumerar_universo() -> list[Path]:
    """Misma logica anti-bucle que tools/inventario_reactivos.py."""
    vistos: set[Path] = set()
    resultado: list[Path] = []
    for p in sorted(RAW_ROOT.rglob("*")):
        if not p.is_file():
            continue
        try:
            resolved = p.resolve()
        except OSError:
            continue
        if "raw/raw" in str(p.relative_to(RAW_ROOT)).replace("\\", "/"):
            continue
        if resolved in vistos:
            continue
        vistos.add(resolved)
        resultado.append(p)
    return resultado


def perimetro() -> list[Path]:
    """Perimetro re-derivado por comando (no lista congelada) -- union de
    causa-B/.pdf de cobertura-composicion y patron-de-nombre no-xlsx."""
    causa_b_pdf: set[str] = set()
    cobertura = REPO_ROOT / "data" / "cobertura-composicion-v1_0.tsv"
    with cobertura.open(encoding="utf-8") as f:
        next(f)
        for linea in f:
            campos = linea.rstrip("\n").split("\t")
            if len(campos) >= 4 and campos[3] == "B" and campos[1] == ".pdf":
                causa_b_pdf.add(campos[0])

    resultado = []
    for p in enumerar_universo():
        if p.suffix.lower() == ".xlsx":
            continue
        rel = p.relative_to(RAW_ROOT).as_posix()
        if rel in causa_b_pdf or casa_patron_nombre(p.name):
            if p.suffix.lower() in FORMATOS_PERIMETRO:
                resultado.append(p)
    return sorted(set(resultado))


def instrumento_de(payload_id: str, manifiesto: dict, familias: list[str]) -> str:
    inst = aplica_v1_1(payload_id)
    if inst:
        return inst
    inst, _campo = aplica_v1_2(payload_id, manifiesto, familias)
    if inst:
        return inst
    return "(sin-instrumento-derivable)"


# ---------------------------------------------------------------------------
# Extraccion por formato
# ---------------------------------------------------------------------------

def encuentra_rotulos_fila(fila: list) -> tuple[int | None, int | None]:
    normalizadas = [normaliza_rotulo(v) for v in fila]
    col_id = None
    for etiqueta in ID_LABELS:
        for i, val in enumerate(normalizadas):
            if val == etiqueta:
                col_id = i
                break
        if col_id is not None:
            break
    col_texto = None
    for etiqueta in TEXT_LABELS:
        for i, val in enumerate(normalizadas):
            if val == etiqueta:
                col_texto = i
                break
        if col_texto is not None:
            break
    return col_id, col_texto


def extrae_xls(path_bytes_or_path, nombre_miembro: str) -> list[dict]:
    import xlrd
    if isinstance(path_bytes_or_path, (bytes, bytearray)):
        wb = xlrd.open_workbook(file_contents=path_bytes_or_path)
    else:
        wb = xlrd.open_workbook(str(path_bytes_or_path))
    filas_out: list[dict] = []
    for sheet in wb.sheets():
        col_id, col_texto = None, None
        for r in range(sheet.nrows):
            fila = sheet.row_values(r)
            nid, ntexto = encuentra_rotulos_fila(fila)
            if nid is not None and ntexto is not None:
                col_id, col_texto = nid, ntexto
                continue
            if col_id is None or col_texto is None:
                continue
            if col_id >= len(fila) or col_texto >= len(fila):
                continue
            val_id = sanitiza_celda(fila[col_id])
            val_texto = sanitiza_celda(fila[col_texto])
            if not val_id or not val_texto:
                continue
            filas_out.append({
                "archivo_miembro": nombre_miembro, "variable_id": val_id,
                "texto_reactivo": val_texto,
            })
    return filas_out


def extrae_html(contenido: bytes, nombre_miembro: str) -> list[dict]:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(contenido, "lxml")
    filas_out: list[dict] = []
    for tabla in soup.find_all("table"):
        col_id, col_texto = None, None
        for tr in tabla.find_all("tr"):
            celdas = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            if not celdas:
                continue
            nid, ntexto = encuentra_rotulos_fila(celdas)
            if nid is not None and ntexto is not None:
                col_id, col_texto = nid, ntexto
                continue
            if col_id is None or col_texto is None:
                continue
            if col_id >= len(celdas) or col_texto >= len(celdas):
                continue
            val_id = sanitiza_celda(celdas[col_id])
            val_texto = sanitiza_celda(celdas[col_texto])
            if not val_id or not val_texto:
                continue
            filas_out.append({
                "archivo_miembro": nombre_miembro, "variable_id": val_id,
                "texto_reactivo": val_texto,
            })
    return filas_out


def extrae_pdf(path_or_bytes, nombre_miembro: str) -> list[dict]:
    import io
    import pdfplumber
    filas_out: list[dict] = []
    if isinstance(path_or_bytes, (bytes, bytearray)):
        fh = io.BytesIO(path_or_bytes)
    else:
        fh = str(path_or_bytes)
    with pdfplumber.open(fh) as pdf:
        for page in pdf.pages:
            hubo_tabla_con_columnas = False
            for tabla in page.extract_tables() or []:
                if not tabla:
                    continue
                col_id, col_texto = None, None
                for fila in tabla:
                    if fila is None:
                        continue
                    normalizadas = [normaliza_rotulo(v) for v in fila]
                    if col_id is None:
                        for i, val in enumerate(normalizadas):
                            if any(tok in val for tok in ("nemonico", "mnemonico", "nombre", "variable")):
                                col_id = i
                                break
                    if col_texto is None:
                        for i, val in enumerate(normalizadas):
                            if any(tok in val for tok in ("descripcion", "pregunta", "etiqueta")):
                                col_texto = i
                                break
                    if col_id is not None and col_texto is not None:
                        hubo_tabla_con_columnas = True
                        break
                if col_id is None or col_texto is None:
                    continue
                for fila in tabla:
                    if fila is None:
                        continue
                    if col_id >= len(fila) or col_texto >= len(fila):
                        continue
                    val_id = sanitiza_celda(fila[col_id])
                    val_texto = sanitiza_celda(fila[col_texto])
                    if not val_id or not val_texto:
                        continue
                    filas_out.append({
                        "archivo_miembro": nombre_miembro, "variable_id": val_id,
                        "texto_reactivo": val_texto,
                    })
            if hubo_tabla_con_columnas:
                continue
            texto = page.extract_text() or ""
            lineas = [l.strip() for l in texto.split("\n")]
            i = 0
            while i < len(lineas):
                l = lineas[i]
                if MNEMONICO_RE.match(l):
                    texto_adj = lineas[i + 1] if i + 1 < len(lineas) else ""
                    if texto_adj:
                        filas_out.append({
                            "archivo_miembro": nombre_miembro, "variable_id": l,
                            "texto_reactivo": texto_adj,
                        })
                i += 1
    return filas_out


def procesar_zip(path: Path) -> tuple[list[dict], list[str]]:
    filas: list[dict] = []
    no_extraido: list[str] = []
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            miembro = info.filename
            suf = Path(miembro).suffix.lower()
            try:
                contenido = zf.read(info)
            except (zipfile.BadZipFile, OSError, RuntimeError) as exc:
                no_extraido.append(f"{miembro}: ERROR:{type(exc).__name__}")
                continue
            if suf == ".pdf":
                filas.extend(extrae_pdf(contenido, miembro))
            elif suf == ".xls":
                try:
                    filas.extend(extrae_xls(contenido, miembro))
                except Exception as exc:  # xlrd sobre binario corrupto/legado
                    no_extraido.append(f"{miembro}: ERROR:{type(exc).__name__}")
            elif suf in (".html", ".htm"):
                filas.extend(extrae_html(contenido, miembro))
            elif suf == ".xlsx":
                no_extraido.append(f"{miembro}: NO-EXTRAIDO:zip-miembro-xlsx-fuera-de-perimetro")
            else:
                no_extraido.append(f"{miembro}: NO-EXTRAIDO:{suf.lstrip('.') or 'SIN_EXTENSION'}")
    return filas, no_extraido


def procesar_payload(path: Path, manifiesto: dict, familias: list[str]) -> tuple[list[dict], str]:
    """Devuelve (filas_tsv, estado). estado en {OK, SIN-CAMPOS-EXTRAIBLES,
    ERROR:<tipo>}."""
    rel = path.relative_to(RAW_ROOT).as_posix()
    sha12 = sha256_file_12(path)
    inst = instrumento_de(rel, manifiesto, familias)
    suf = path.suffix.lower()
    metodo_map = {".pdf": "INSPECT_PDF_FD", ".xls": "INSPECT_XLS_FD", ".html": "INSPECT_HTML_FD"}

    crudo: list[dict] = []
    try:
        if suf == ".pdf":
            crudo = extrae_pdf(path, rel)
        elif suf == ".xls":
            crudo = extrae_xls(path, rel)
        elif suf == ".html":
            crudo = extrae_html(path.read_bytes(), rel)
        elif suf == ".zip":
            crudo, _no_extraido = procesar_zip(path)
        else:
            return [], f"NO-EXTRAIDO:{suf.lstrip('.') or 'SIN_EXTENSION'}"
    except Exception as exc:
        return [], f"ERROR:{type(exc).__name__}:{exc}"

    if not crudo:
        return [], "SIN-CAMPOS-EXTRAIBLES"

    filas = []
    for f in crudo:
        metodo = "INSPECT_ZIP_FD" if suf == ".zip" else metodo_map.get(suf, "INSPECT_DESCONOCIDO")
        filas.append({
            "payload_id": sanitiza_celda(rel),
            "sha256_12": sha12,
            "instrumento": sanitiza_celda(inst),
            "ola": "NO_DETERMINADO",
            "archivo_miembro": sanitiza_celda(f["archivo_miembro"]),
            "variable_id": sanitiza_celda(f["variable_id"]),
            "texto_reactivo": sanitiza_celda(f["texto_reactivo"]),
            "metodo": metodo,
            "universo_declarado": "PRESENTE_EN_DATA_RAW",
        })
    return filas, "OK"


def control_positivo(filas: list[dict]) -> dict:
    """Contraste pre-registrado (COMMIT-1 (c)): envipe2025/encuci2020."""
    resultados = {}

    envipe_ids = {f["variable_id"] for f in filas if f["payload_id"] == "fd_envipe2025.pdf"}
    ref_envipe: set[str] = set()
    if REACTIVOS_EXT_V1_0.exists():
        with REACTIVOS_EXT_V1_0.open(encoding="utf-8") as fh:
            next(fh)
            for linea in fh:
                campos = linea.rstrip("\n").split("\t")
                if len(campos) >= 6 and campos[2] == "envipe2025":
                    ref_envipe.add(campos[5])
    solape = len(envipe_ids & ref_envipe)
    pct_envipe = (solape / len(envipe_ids) * 100) if envipe_ids else 0.0
    resultados["fd_envipe2025.pdf"] = {
        "extraidos": len(envipe_ids), "referencia": len(ref_envipe),
        "solape": solape, "pct": round(pct_envipe, 1),
        "validado": pct_envipe >= 60.0,
    }

    encuci_ids = {f["variable_id"] for f in filas if f["payload_id"] == "FD_ENCUCI2020.pdf"}
    ref_encuci: set[str] = set()
    if REACTIVOS_V1_0.exists():
        with REACTIVOS_V1_0.open(encoding="utf-8") as fh:
            next(fh)
            for linea in fh:
                campos = linea.rstrip("\n").split("\t")
                if len(campos) >= 6 and "encuci" in campos[0].lower():
                    ref_encuci.add(campos[5])
    solape2 = len(encuci_ids & ref_encuci)
    pct_encuci = (solape2 / len(encuci_ids) * 100) if encuci_ids else 0.0
    resultados["FD_ENCUCI2020.pdf"] = {
        "extraidos": len(encuci_ids), "referencia": len(ref_encuci),
        "solape": solape2, "pct": round(pct_encuci, 1),
        "validado": pct_encuci >= 60.0,
    }
    return resultados


def escribe_tabla(filas: list[dict]) -> None:
    with OUT_PATH.open("w", encoding="utf-8") as f:
        f.write("# data/inventario-fd-ext-v1_0.tsv -- ACTO MAESTRA32-E12 · EXTRACTOR-FD, COMMIT-2\n")
        f.write("# Extiende data/inventario-fd-v1_1.tsv (.xlsx) al perimetro no-xlsx de FP-173/FP-175(b): "
                "PDF/XLS/HTML sueltos y zip que los envuelve. Mismo esquema de 9 columnas. "
                "Ver forense/notas/2026-08-30-fd-ext-spec.md (COMMIT-1) y "
                "forense/notas/2026-08-30-fd-ext-cierre.md (COMMIT-2).\n")
        f.write("\t".join(FIELDS) + "\n")
        for fila in filas:
            f.write("\t".join(fila[c] for c in FIELDS) + "\n")


def main() -> int:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        manifiesto = carga_manifiesto(MANIFIESTO) if MANIFIESTO.exists() else {}
        familias = familias_canonicas(REACTIVOS_V1_1) if REACTIVOS_V1_1.exists() else []

        payloads = perimetro()
        print(f"Perimetro re-derivado: {len(payloads)} payloads", file=sys.stderr)

        todas_filas: list[dict] = []
        estados: dict[str, str] = {}
        for p in payloads:
            rel = p.relative_to(RAW_ROOT).as_posix()
            filas, estado = procesar_payload(p, manifiesto, familias)
            estados[rel] = estado
            todas_filas.extend(filas)
            print(f"  {rel}: {estado} ({len(filas)} filas)", file=sys.stderr)

        escribe_tabla(todas_filas)

        con_filas = sum(1 for e in estados.values() if e == "OK")
        con_texto = sum(1 for f in todas_filas if f["texto_reactivo"])
        print(f"\nCobertura payloads-con-fila: {con_filas}/{len(payloads)}", file=sys.stderr)
        print(f"Filas totales: {len(todas_filas)} ; con texto: {con_texto}", file=sys.stderr)

        cp = control_positivo(todas_filas)
        for pid, res in cp.items():
            print(f"Control positivo {pid}: {res}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
