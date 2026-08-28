#!/usr/bin/env python3
"""ACTO MAESTRA31-E6 · DICCIONARIOS-FD — genera data/inventario-fd-v1_0.tsv.

COMMIT-1 (especificación congelada, escrita ANTES de correr este extractor
sobre el perímetro completo; el archivo se commitea solo, sin la tabla, y
el commit que agrega data/inventario-fd-v1_0.tsv es COMMIT-2 aparte).

────────────────────────────────────────────────────────────────────────
QUÉ ES ESTO
────────────────────────────────────────────────────────────────────────
Tabla HERMANA de data/inventario-reactivos-v1_0.tsv (ADR-213), no
sustituta. tools/inventario_reactivos.py (E4) puebla variable_id leyendo
solo la PRIMERA FILA de cada hoja XLSX (ver inspect_xlsx en
tools/curador_registro/inspect_assets.py). En los archivos de ficha
descriptiva / diccionario de datos de INEGI y otras instituciones, esa
primera fila no es un encabezado: es la primera línea de un BLOQUE DE
TÍTULO (varias filas de metadatos — título de la encuesta, "ESTRUCTURA
DEL ARCHIVO", nombre de tabla, una leyenda que explica qué significa cada
columna) que antecede a la tabla real de variables. Por eso las 178,246
filas de la tabla hermana tienen texto_reactivo vacío en el 100% de los
casos (awk -F'\t' 'NR>1 && length($7)>0' | wc -l → 0): el extractor de
referencia nunca llega a la tabla real en NINGÚN archivo, no solo en los
30 que E4 identificó por síntoma.

Este script NO toca tools/inventario_reactivos.py ni
tools/curador_registro/**. Es un extractor propio, para un patrón (el
bloque de título de ficha descriptiva/diccionario), sobre un conjunto
acotado (perímetro derivado abajo). Cero red, cero modelo, cero
clasificación semántica del texto extraído (FP-165): el texto se copia
tal como el archivo lo declara.

────────────────────────────────────────────────────────────────────────
PERÍMETRO (derivado por comando en el paso 1 del encargo, NO heredado)
────────────────────────────────────────────────────────────────────────
La cifra "30" de E4 salía de un SÍNTOMA (variable_id > 60 caracteres vía
INSPECT_XLSX), no de un censo por nombre. Al derivar el perímetro por
patrón de nombre (variantes: `diccionario`, `glosario`, `descriptor`, o
el token `fd` delimitado por `_`/`.`/`-` o los límites del nombre, en
cualquier posición — cubre `*_fd.xlsx`, `fd_*.xlsx`, `FD_*.xlsx`,
`Diccionario_*`, `Glosario_*`, `*_descriptor_*`, etc.) restringido a
`.xlsx`, salen **33** payloads, no 30/31. Cruce contra el síntoma de E4
(recalculado aquí, no heredado — 31 payloads con >60 chars vía
INSPECT_XLSX, no 30: el número de E4 estaba subcontado en 1):

  - 23 casan AMBOS (nombre Y síntoma).
  - 10 casan el NOMBRE pero NO el síntoma (Diccionario_DGPASF,
    Glosario_Datos_Abiertos_DGASF, Censo2020_CAAS/CEU_descriptor_bd,
    diccionario_cuestionario_ampliado_cpv2020, enasic_2022_fd,
    enfih_2019_fd, enif_2024_fd, enut2019_fd, enut2024_fd). Verificado
    abriendo 5 de los 10 (Censo2020_CAAS, Diccionario_DGPASF,
    diccionario_cuestionario_ampliado_cpv2020, enasic_2022_fd,
    enfih_2019_fd, enut2024_fd — 6 de 10): SÍ tienen el mismo bloque de
    título; su primera fila simplemente mide ≤60 caracteres (a veces
    está en blanco y el título real cae en la fila 2), así que el
    síntoma de E4 subestima el hueco, no lo sobreestima, en este eje.
  - 8 presentan el SÍNTOMA pero NO casan el nombre: 6 archivos
    `Base_Ahorro_Financiero_y_Financiamiento_*.xlsx` de CNBV (series de
    tiempo con un rótulo de eje largo en la fila 1 — dato, no
    diccionario), `cuestionario_supervision_en_campo.xlsx` (formulario
    XLSForm de Banco Mundial: fila 1 ya es el encabezado real
    type/name/label/…, sin bloque de título), y
    `encup_2012_base_datos_xlsx.xlsx` (microdatos crudos en la hoja
    principal; una hoja secundaria con preguntas sueltas sin columna de
    mnemónico separada). Los tres se abrieron y NINGUNO tiene el patrón
    de este acto — confirma que el síntoma de E4 sí sobreestimaba en
    este otro eje. Quedan FUERA del perímetro: no son ficha
    descriptiva/diccionario, y forzarlos exigiría un extractor distinto
    por archivo (justo lo que la regla de tope prohíbe).

Perímetro final de este acto = **33** (nombre, no síntoma), todos
`.xlsx`. Ver `PERIMETRO_XLSX` abajo para la función que lo deriva por
comando en cada corrida (no una lista congelada a mano: si el corpus
cambia, este número se recalcula solo).

Fuera de xlsx (medido en el paso 1, NO tocado por este extractor — la
regla de tope prohíbe generalizar a otro formato en esta misma vuelta):
34 PDF, 6 XLS (formato binario legado), 4 HTML, 2 ZIP que envuelven un
PDF o un XLSX de ficha descriptiva (`enif_2021_fd_pdf.zip`,
`ensafi2023/ensafi_2023_fd_xlsx.zip`) — 46 payloads adicionales con
nombre de diccionario/ficha descriptiva. CERO en .txt/.doc/.docx. Los
46 no-xlsx contribuyen HOY cero filas a data/inventario-reactivos-v1_0.tsv
(confirmado por payload_id sobre 3 muestras, una por formato no-zip): esos
formatos están en FORMATOS_SIN_CAMPOS de tools/inventario_reactivos.py,
que nunca intenta leer columnas ahí sin importar el contenido. El bloque
de título SÍ es convención de INEGI, no del formato xlsx — así que el
hueco real es más ancho que este acto. Queda medido y declarado, no
resuelto: extraer de PDF/XLS/HTML exige una librería distinta por
formato (pdf: texto/tablas; xls binario: xlrd; html: parser de marcado),
lo que ya no es "un extractor, para un patrón" — es la generalización que
la regla de tope ordena parar. Candidato natural a acto sucesor, igual
que este acto fue el sucesor que E4 reveló y no podía ejecutar.

────────────────────────────────────────────────────────────────────────
CÓMO SE DETECTA EL BLOQUE DE TÍTULO Y EL INICIO DE LA TABLA DE VARIABLES
────────────────────────────────────────────────────────────────────────
Observado abriendo 14 archivos de al menos 10 instituciones/familias
distintas (CNBV ×2 plantillas, ENASEM, MOCIBA, ENDUTIH, ENIF ×2 años,
ENVIPE, ENASIC, ENFIH, Censo de Población y Vivienda ×2 plantillas,
ENADID, ENUT) ANTES de escribir esta regla — no es la regla de un solo
archivo. La forma exacta del bloque de título varía muchísimo entre
instituciones (de 6 a 21 filas; con o sin leyenda numerada; leyenda en
formato "(1)"/"[1]"; con o sin fila de sección repetida a media hoja) y
NO es uniforme (ver B-bis en el cierre) — pero un rasgo SÍ es constante
en las 14 muestras: la tabla real de variables siempre empieza en una
fila que declara, en alguna de sus celdas, un rótulo de columna
reconocible para "identificador de la variable" (Mnemónico/Nemónico/
Nombre/Nombre de la columna/Clave) Y, en otra celda de la MISMA fila, un
rótulo reconocible para "texto de la variable" (Pregunta/Pregunta y
categoría/Descripción/Observaciones). Esto reemplaza "primera fila de
cada hoja" (la regla que falla) por "primera fila que declara AMBOS
rótulos", y se re-evalúa en cada fila porque varias instituciones
(ENASIC, censo) repiten el encabezado a media hoja al iniciar una nueva
sección — una sola detección al principio de la hoja perdería esas
secciones.

No se busca ninguna palabra en el CONTENIDO de las variables (eso sería
semántica); se hace correspondencia EXACTA (tras normalizar acentos,
mayúsculas y espacios) contra los RÓTULOS DE COLUMNA que el propio
archivo declara — es lectura estructural, la misma operación que hace
csv.DictReader al usar la primera fila como encabezado, aplicada aquí a
la fila correcta en vez de siempre la primera.

Fila de leyenda numerada inmediatamente relevante ("[1]" "[2]" "[3]"…, o
"(0)" "(1)" "(2)"…, una bajo cada columna del encabezado, vista en
ENASIC/ENIF/ENFIH/ENUT/ENADID/censo): se reconoce y se salta (no es una
variable). Filas en blanco y filas de sección con una sola celda no
vacía (p. ej. "SECCIÓN 1. CARACTERÍSTICAS DE LA VIVIENDA") nunca
producen fila porque exigimos AMBAS celdas objetivo (id y texto) no
vacías para emitir.

QUÉ SE HACE CON LOS QUE NO CASAN LA REGLA: si una hoja nunca declara una
fila con ambos rótulos (p. ej. las hojas "Índice"/"ÍNDICE" que solo
listan tablas, o cualquier hoja con plantilla no reconocida), esa hoja
aporta CERO filas y se registra en NO_EXTRAIDO con razón
SIN_ENCABEZADO_RECONOCIDO. Esa lista se imprime en el resumen de
ejecución (stdout) y se traslada íntegra a la nota de cierre — es
entregable, no se descarta.

────────────────────────────────────────────────────────────────────────
ESQUEMA (hermano de data/inventario-reactivos-v1_0.tsv, misma forma)
────────────────────────────────────────────────────────────────────────
payload_id · sha256_12 · instrumento · ola · archivo_miembro ·
variable_id · texto_reactivo · metodo · universo_declarado

- payload_id: ruta relativa a data/raw, posix (idéntico a la tabla
  hermana).
- sha256_12: sha256 del archivo, 12 hex (mismo algoritmo, calculado de
  nuevo aquí — no se importa de tools/inventario_reactivos.py para que
  el código nuevo viva en su propio archivo sin acoplarse al que la
  regla de tope prohíbe tocar).
- instrumento: primer segmento de payload_id, o "(raiz)" (idéntico).
- ola: "NO_DETERMINADO" — mismo valor que las 178,246 filas existentes;
  este acto no infiere año/ola (sería clasificar, fuera de tope).
- archivo_miembro: nombre de la hoja (sheet.title).
- variable_id: contenido de la celda bajo el rótulo id (Mnemónico/
  Nombre/…), saneado.
- texto_reactivo: contenido de la celda bajo el rótulo texto (Pregunta/
  Descripción/…), saneado. ESTA es la columna que la tabla hermana deja
  vacía en el 100% de sus 178,246 filas.
- metodo: "INSPECT_FD_XLSX" — deliberadamente distinto de
  "INSPECT_XLSX" (el método de la tabla hermana): el mecanismo es otro
  (regla de encabezado re-evaluada por fila, no primera fila de la
  hoja) y no debe leerse como si fuera la misma pasada.
- universo_declarado: "PRESENTE_EN_DATA_RAW" para las filas extraídas.

────────────────────────────────────────────────────────────────────────
DENOMINADOR DE COBERTURA Y QUÉ CUENTA COMO CUBIERTO
────────────────────────────────────────────────────────────────────────
Denominador = 33 (perímetro xlsx derivado arriba, recalculado por
PERIMETRO_XLSX() en cada corrida). Un payload cuenta como CUBIERTO si
aporta 1 o más filas a data/inventario-fd-v1_0.tsv (mismo criterio que
"payloads_cubiertos" en tools/inventario_reactivos.py: al menos una fila,
no todas sus hojas). El CONTADOR de este acto (variables con texto
recuperado) es el conteo total de filas de la tabla nueva.

────────────────────────────────────────────────────────────────────────
B-bis — ANTES de ver el dato: qué significa cubrir casi todos / pocos
────────────────────────────────────────────────────────────────────────
La regla NO resultó uniforme entre instituciones (ver arriba: de 6 a 21
filas de bloque de título, tres formatos de leyenda distintos, con y sin
hoja Índice, con y sin sección repetida) — así que NO se declara aquí un
resultado de uniformidad; ese resultado más generalizable que dirección
anticipaba como posible NO se dio. Lo que sí es uniforme, en las 14
muestras observadas, es el punto de enganche (rótulo de columna dual) que
esta regla usa. Cubrir CASI TODOS los 33 (≥90%) significaría que el
enganche por rótulo dual generaliza también fuera de la muestra de 14 —
un resultado fuerte y reusable para cualquier ficha descriptiva futura de
estas mismas instituciones. Cubrir POCOS (<50%, el falsador de la regla
de tope) significaría que las fichas descriptivas de INEGI/CNBV/censo NO
comparten estructura suficiente para una sola regla mecánica, y que
recuperar su texto exige leer archivo por archivo — un resultado también
real, que se declara con esa palabra si ocurre, y no se itera para
subirlo.

Frase de sello verbatim: «El primer resultado que produzca este
procedimiento es el que se reporta.»

Falsador (regla de tope núm. 5): si payloads_cubiertos / 33 < 0.5, se
conserva lo producido, se anota en hallazgos.md como vía abandonada, y no
se ajusta la regla para subir el número.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import unicodedata
import warnings
from pathlib import Path

import openpyxl

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = REPO_ROOT / "data" / "raw"
OUT_PATH = REPO_ROOT / "data" / "inventario-fd-v1_0.tsv"

FIELDS = [
    "payload_id", "sha256_12", "instrumento", "ola", "archivo_miembro",
    "variable_id", "texto_reactivo", "metodo", "universo_declarado",
]

# Rótulos de columna reconocidos, en orden de prioridad (el primero que
# aparezca en la fila, exacto tras normalizar, gana). Derivados de las 14
# muestras abiertas — no se añaden sinónimos especulativos no observados.
ID_LABELS = ["mnemonico", "nemonico", "nombre de la columna", "nombre", "clave"]
TEXT_LABELS = ["pregunta y categoria", "pregunta",
               "descripcion del contenido del campo", "descripcion",
               "observaciones"]

_LEGEND_CELL = re.compile(r"^[\(\[]\s*\d+\s*[\)\]]$")


def normaliza_rotulo(valor) -> str:
    """minusculas, sin acentos, espacios colapsados, sin ':'/'.' final —
    para comparar RÓTULOS DE COLUMNA (no el texto_reactivo extraído)."""
    if valor is None:
        return ""
    s = unicodedata.normalize("NFKD", str(valor))
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s.strip().lower())
    return s.rstrip(":.")


def sanitiza_celda(valor) -> str:
    """Colapsa tab/CR/LF a espacio — misma convención que
    tools/inventario_reactivos.py (TSV plano de una línea por fila, sin
    comillas CSV)."""
    if valor is None:
        return ""
    return " ".join(str(valor).replace("\t", " ").split())


def sha256_file_12(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()[:12]


def enumerar_universo() -> list[Path]:
    """Payloads bajo data/raw, evitando el bucle de symlink data/raw/raw
    (misma lógica que enumerar_universo() en tools/inventario_reactivos.py,
    reimplementada aquí para que este archivo no importe de allá)."""
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


def casa_patron_nombre(nombre: str) -> bool:
    """Patrón de nombre derivado en el paso 1: diccionario/glosario/
    descriptor en cualquier posición, o 'fd' como token delimitado por
    '_'/'.'/'-' o los límites del nombre."""
    low = nombre.lower()
    if "diccionario" in low or "glosario" in low or "descriptor" in low:
        return True
    if re.search(r"(^|[_\-.])fd([_\-.]|$)", low):
        return True
    return False


def perimetro_xlsx() -> list[Path]:
    """El perímetro de este acto: derivado por patrón de NOMBRE (no por
    síntoma), restringido a .xlsx. Se recalcula en cada corrida sobre el
    universo real de data/raw — no es una lista congelada a mano."""
    return sorted(
        p for p in enumerar_universo()
        if p.suffix.lower() == ".xlsx" and casa_patron_nombre(p.name)
    )


def encuentra_rotulos(fila: tuple) -> tuple[int | None, int | None]:
    """Dada una fila (tupla de valores), busca la primera coincidencia de
    ID_LABELS y de TEXT_LABELS (por prioridad, no por posición). Devuelve
    (col_id, col_texto) o None donde no haya coincidencia."""
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


def es_fila_leyenda(fila: tuple) -> bool:
    no_vacias = [str(v).strip() for v in fila if v is not None and str(v).strip() != ""]
    if not no_vacias:
        return False
    return all(_LEGEND_CELL.match(v) for v in no_vacias)


def procesar_hoja(sheet) -> tuple[list[dict], bool]:
    """Recorre una hoja fila por fila, re-evaluando el encabezado en cada
    fila (varias instituciones repiten el encabezado a media hoja).
    Devuelve (filas_extraidas, hubo_encabezado_alguna_vez)."""
    filas_out: list[dict] = []
    col_id, col_texto = None, None
    hubo_encabezado = False
    for fila in sheet.iter_rows(values_only=True):
        nid, ntexto = encuentra_rotulos(fila)
        if nid is not None and ntexto is not None:
            col_id, col_texto = nid, ntexto
            hubo_encabezado = True
            continue
        if es_fila_leyenda(fila):
            continue
        if col_id is None or col_texto is None:
            continue
        if col_id >= len(fila) or col_texto >= len(fila):
            continue
        val_id = sanitiza_celda(fila[col_id])
        val_texto = sanitiza_celda(fila[col_texto])
        if not val_id or not val_texto:
            continue
        filas_out.append({"variable_id": val_id, "texto_reactivo": val_texto})
    return filas_out, hubo_encabezado


def procesar_payload(path: Path) -> tuple[list[dict], list[str]]:
    """Devuelve (filas_tsv, no_extraido) para un payload. no_extraido es
    una lista de 'hoja: razon' para las hojas que no aportaron filas."""
    rel = path.relative_to(RAW_ROOT).as_posix()
    instrumento = rel.split("/", 1)[0] if "/" in rel else "(raiz)"
    sha12 = sha256_file_12(path)

    filas_tsv: list[dict] = []
    no_extraido: list[str] = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # avisos de metadata (área de impresión) de openpyxl, irrelevantes para lectura de celdas
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            for sheet in wb.worksheets:
                filas_hoja, hubo_encabezado = procesar_hoja(sheet)
                if not filas_hoja:
                    razon = "SIN_ENCABEZADO_RECONOCIDO" if not hubo_encabezado else "ENCABEZADO_SIN_FILAS_DE_DATOS"
                    no_extraido.append(f"{sheet.title}: {razon}")
                    continue
                for f in filas_hoja:
                    filas_tsv.append({
                        "payload_id": rel,
                        "sha256_12": sha12,
                        "instrumento": instrumento,
                        "ola": "NO_DETERMINADO",
                        "archivo_miembro": sanitiza_celda(sheet.title),
                        "variable_id": f["variable_id"],
                        "texto_reactivo": f["texto_reactivo"],
                        "metodo": "INSPECT_FD_XLSX",
                        "universo_declarado": "PRESENTE_EN_DATA_RAW",
                    })
        finally:
            wb.close()
    return filas_tsv, no_extraido


def main() -> int:
    perimetro = perimetro_xlsx()
    todas_las_filas: list[dict] = []
    no_extraido_global: dict[str, list[str]] = {}
    payloads_cubiertos = 0
    payloads_error: list[str] = []

    for i, path in enumerate(perimetro, 1):
        rel = path.relative_to(RAW_ROOT).as_posix()
        start = time.monotonic()
        try:
            filas, no_extraido = procesar_payload(path)
        except Exception as exc:  # noqa: BLE001 — se documenta, no se enmascara
            payloads_error.append(f"{rel}: ERROR:{type(exc).__name__}:{str(exc)[:200]}")
            continue
        elapsed = time.monotonic() - start
        if filas:
            payloads_cubiertos += 1
        todas_las_filas.extend(filas)
        if no_extraido:
            no_extraido_global[rel] = no_extraido
        print(f"... {i}/{len(perimetro)} {rel} -> {len(filas)} filas ({elapsed:.1f}s)", file=sys.stderr)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(FIELDS) + "\n")
        for fila in sorted(todas_las_filas, key=lambda r: (r["payload_id"], r["archivo_miembro"], r["variable_id"])):
            handle.write("\t".join(fila[f] for f in FIELDS) + "\n")

    cobertura = payloads_cubiertos / len(perimetro) if perimetro else 0.0
    resumen = {
        "universo_declarado": (
            f"{len(perimetro)} payloads .xlsx bajo data/raw cuyo nombre casa "
            "el patron diccionario_/glosario_/descriptor/fd-token, derivado "
            "por comando en ACTO MAESTRA31-E6 paso 1 (no heredado del sintoma "
            "de 30/31 de E4)."
        ),
        "denominador_perimetro": len(perimetro),
        "payloads_cubiertos": payloads_cubiertos,
        "cobertura_fraccion": round(cobertura, 4),
        "filas_totales": len(todas_las_filas),
        "payloads_con_hojas_no_extraidas": no_extraido_global,
        "payloads_error": payloads_error,
        "falsador_regla_tope_5": "cobertura < 0.5 -> abandonar la via, no iterar la regla",
        "falsador_disparado": cobertura < 0.5,
    }
    print(json.dumps(resumen, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
