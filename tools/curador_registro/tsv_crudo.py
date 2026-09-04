#!/usr/bin/env python3
"""Lector/escritor de TSV que preserva bytes -- FP-258, vía (ii).

Medido (`forense/notas/2026-09-03-MAESTRA37-N2-control.md`): un round-trip
`csv.reader`→`csv.writer` (tab, `QUOTE_MINIMAL`) sobre
`data/curacion-registro/cola-adquisicion-registro.tsv` corrompe 4 de sus
112 líneas (29, 47, 63, 94) -- cada una tiene una comilla doble suelta
dentro de una columna `nota` que NO fue escrita con intención de quoting
CSV, y que `csv.writer` reescribe distinto al reinterpretarla.

DISCREPANCIA con la vía descrita en el encargo, medida al implementar:
el encargo pide "split por `\\t`, sin quoting, sin normalizar comillas"
como estrategia única. Esa estrategia funciona para el round-trip pero
**rompe la extracción de valores** de al menos una fila (línea 9,
`WORLD_BANK_ENTERPRISE_SURVEY_MEXICO_2023`): esa fila SÍ está
correctamente citada en CSV (empieza y termina con `"`, las comillas
internas dobladas `""`), y un split naïve por tab deja las comillas
literales dentro del valor de `nota` -- corrompe la vista donde el csv
original no la corrompía. Verificado con
`tools/vista_cola_adquisicion.py`: adoptar un split naïve para leer
valores producía una vista que diferían de la vista de `origin/main` en
esa fila (`diff` no vacío) -- viola la regresión byte a byte que P1 exige.

Por eso este módulo separa las dos funciones que el encargo trataba como
una sola:

* **Preservar bytes (round-trip, para T26-bis)**: `leer_lineas`/
  `escribir_lineas` tratan cada línea del archivo como texto opaco -- no
  la parten en columnas, no la reinterpretan. Reescribir sin modificar
  ninguna línea es, por construcción, la identidad: 0 líneas distintas,
  siempre. Es la única forma de garantizar que un round-trip no corrompa
  NINGUNA fila (ni las 4 con comilla suelta, ni la que sí está bien
  citada) -- no reserializar lo que no se tocó, en vez de reserializarlo
  todo y esperar que coincida.
* **Leer valores (para consumidores como la vista)**: `leer_dicts` sí
  necesita el valor semántico correcto de cada columna, y para eso delega
  en el módulo `csv` estándar (mismo comportamiento que el
  `csv.DictReader` que `vista_cola_adquisicion.py` ya usaba) -- es la
  única forma de que la fila 9 se lea sin comillas de sobra. No escribe
  nada: solo lee.
"""

from __future__ import annotations

import csv
from pathlib import Path


def leer_lineas(path: Path) -> list[str]:
    """Cada línea del archivo, como texto opaco -- sin partir por tab, sin
    interpretar comillas. No se devuelve una línea vacía final (el `\n`
    final habitual del archivo)."""
    texto = path.read_text(encoding="utf-8-sig")
    lineas = texto.split("\n")
    if lineas and lineas[-1] == "":
        lineas = lineas[:-1]
    return lineas


def escribir_lineas(path: Path, lineas: list[str]) -> None:
    """Reescribe `path` a partir de `lineas` (texto opaco, ver `leer_lineas`),
    con un `\n` final. Reescribir la salida de `leer_lineas` sin modificar
    ninguna línea es la identidad byte a byte -- esa es la garantía de
    round-trip que T26-bis mide."""
    path.write_text("\n".join(lineas) + "\n", encoding="utf-8")


def leer_dicts(path: Path) -> list[dict[str, str]]:
    """Primera línea = cabecera; el resto, un dict por fila con esas
    claves -- valores parseados con el módulo `csv` estándar (respeta
    comillas correctamente citadas, igual que `csv.DictReader`). Para
    LEER valores, no para el round-trip -- ver docstring del módulo."""
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def upsert_fila(
    path: Path, fila: dict[str, str], campos: list[str], clave: str = "fila_origen"
) -> None:
    """Inserta o reemplaza una fila en `path`, tocando solo esa línea.

    `fila[c] for c in campos` arma la línea nueva (tab-separada, sin
    quoting -- ver docstring del módulo). Busca entre las líneas de datos
    existentes (índice 1 en adelante; la línea 0 es la cabecera) una cuyo
    valor en la columna `clave` (ubicada vía `campos.index(clave)`) sea
    igual a `fila[clave]`; si la encuentra, reemplaza esa línea in place
    -- toda otra línea, cabecera incluida, queda byte a byte intacta. Si
    no la encuentra, agrega la línea nueva al final. Usa `leer_lineas`/
    `escribir_lineas` (texto opaco) para no reserializar lo que no se
    tocó.

    `raise ValueError` si algún valor de `fila` trae un `\\t` o `\\n`
    literal (corrompería el formato de línea opaca que este módulo
    asume), o si `clave` no está en `campos`.
    """
    if clave not in campos:
        raise ValueError(f"clave {clave!r} no está en campos: {campos!r}")
    for columna, valor in fila.items():
        if "\t" in valor or "\n" in valor:
            raise ValueError(
                f"valor de {columna!r} contiene un \\t o \\n literal: {valor!r}"
            )

    idx = campos.index(clave)
    valor_clave = fila[clave]
    nueva_linea = "\t".join(fila[c] for c in campos)

    lineas = leer_lineas(path)
    for i in range(1, len(lineas)):
        partes = lineas[i].split("\t")
        if idx < len(partes) and partes[idx] == valor_clave:
            lineas[i] = nueva_linea
            break
    else:
        lineas.append(nueva_linea)
    escribir_lineas(path, lineas)
