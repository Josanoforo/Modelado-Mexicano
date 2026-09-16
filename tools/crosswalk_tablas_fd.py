#!/usr/bin/env python3
"""Publica el crosswalk de tablas entre el payload y su descriptor (FD).

`NC-0245` (`ACTO GEN2-RESIDUAL-81-1`, `PR #803`) dejó 7 620 filas ciegas que el
puente por nombre de `archivo_miembro` no resuelve: `TABLA_SIN_FD` (la hoja no
existe en el descriptor indexado) y `VARIABLE_SIN_FD` (la hoja empareja, la
variable no aparece en ella). Ese residual NO es de ortografía. Este tool lo
acredita leyendo el **FD real** desde la raíz montada y publicando, como tabla,
qué miembro de payload corresponde a qué hoja del descriptor, con el método y
la evidencia literal de cada emparejamiento.

Reglas que no se aflojan:

* Un emparejamiento que el FD no sostiene **no se publica**: se conserva en el
  residual con su motivo. La identidad se acredita por una de dos vías, en este
  orden, y el método viaja en cada fila:
  - ``FD-DECLARA-TABLA`` — el FD real **nombra** la tabla dentro de la hoja
    (celda ``TABLA: X`` / ``Tabla: X``, columna ``Nombre de la BD``, rótulo
    ``N. Sección``) y ese nombre normaliza al miembro del payload. Es la
    evidencia más fuerte y gana siempre que exista.
  - ``FD-NOMBRE-DE-HOJA`` — el FD no declara nada dentro de la hoja, pero el
    **título** de la hoja normaliza al miembro. Más débil que la anterior: se
    publica con el método a la vista, nunca confundido con una declaración.
  - ``IDENTIDAD-DE-VARIABLES`` — el conjunto de variables del miembro y el de
    la hoja coinciden por arriba de ``--cobertura-minima`` con margen
    ``--margen-minimo`` sobre la segunda candidata, y el emparejamiento es
    **mutuo** (cada lado es el mejor del otro).
* Ambigüedad nunca se resuelve por cercanía: se conserva como residual.
* Cero microdato. Se abren descriptores (xlsx/xls) y tablas de metadato ya
  indexadas; nunca un valor de payload.

Normalizaciones de clave de variable, ambas declaradas y medidas (son de
vocabulario, no de contenido — misma clase que el truncado a 31 caracteres que
`ACTO GEN2-RESIDUAL-81-1` documentó):

* ``casefold`` — MOCIBA escribe ``upm``/``p1`` en el ``.sav`` y ``UPM``/``P1``
  en el ``.dbf`` y en el FD.
* sufijo de ola — ENASEM escribe ``A13A_18`` en el payload donde el FD escribe
  ``A13A``; el sufijo es el año de la ola (2 o 4 dígitos) tomado del nombre del
  instrumento, nunca adivinado.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = REPO_ROOT / "data" / "raw"

INVENTARIOS = (
    REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv",
    REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv",
)
CAPAS_FD = (
    REPO_ROOT / "data" / "inventario-fd-v1_1.tsv",
    REPO_ROOT / "data" / "inventario-fd-ext-v1_0.tsv",
)
RESIDUAL_ENTRADA = REPO_ROOT / "data" / "reactivos-fd-recuperado-residual-v1_0.tsv"

SALIDA = REPO_ROOT / "data" / "crosswalk-tablas-fd-v1_0.tsv"
SALIDA_RESIDUAL = REPO_ROOT / "data" / "crosswalk-tablas-fd-residual-v1_0.tsv"

VERSION = "crosswalk-tablas-fd-1.0.0"

CAMPOS = [
    "instrumento", "archivo_miembro", "payload_id", "hoja_fd", "payload_id_fd",
    "sha256_12_fd", "metodo", "evidencia_fd", "clave_variable",
    "variables_miembro", "variables_hoja", "variables_comunes", "cobertura",
    "margen", "filas_ciegas_cubiertas",
]
CAMPOS_RESIDUAL = [
    "instrumento", "archivo_miembro", "motivo", "detalle",
    "variables_miembro", "filas_ciegas", "mejor_candidata", "mejor_cobertura",
]

EXTENSIONES = (".csv", ".dbf", ".sav", ".dta", ".txt", ".xlsx", ".xls", ".zip")
# Sello de publicación que CNBV antepone al nombre de la tabla en el miembro
# (`52Sep2022_BD_Acceso_Edo.csv`); el FD nombra la tabla sin él.
SELLO_PUBLICACION = re.compile(r"^\d{1,3}[a-z]{3}\d{4}_", re.IGNORECASE)
# Sufijo de corte del Censo 2020 (`TR_ALO_CAAS_00.csv` ↔ hoja `TR_ALO_CAAS`).
SUFIJO_CORTE = re.compile(r"_\d{2}$")

# Hojas y miembros que NO son tabla de datos: índices, diagramas y catálogos.
# Se reconocen por nombre porque eso es lo que son en el propio descriptor.
NO_ES_TABLA = re.compile(
    r"^(indice|índice|diagrama\s|modelo\s+de\s+datos|catálogo|catalogo|"
    r"indicadores|cod_tc_|tc_cve_|nota_)", re.IGNORECASE)


def fold(value: str) -> str:
    """Pliega a minúsculas sin acentos y sin separadores."""
    texto = unicodedata.normalize("NFKD", str(value))
    texto = texto.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "", texto.lower())


def normaliza_tabla(nombre: str) -> str:
    """Clave de tabla: sin extensión, sin sello de publicación, sin corte."""
    texto = str(nombre).strip()
    texto = texto.rsplit("/", 1)[-1]
    for ext in EXTENSIONES:
        if texto.lower().endswith(ext):
            texto = texto[: -len(ext)]
            break
    texto = SELLO_PUBLICACION.sub("", texto)
    texto = SUFIJO_CORTE.sub("", texto)
    return fold(texto)


def olas_de(instrumento: str) -> tuple[str, ...]:
    """Sufijos de ola derivados del nombre del instrumento, no adivinados."""
    m = re.search(r"(19|20)(\d{2})\b", instrumento)
    if not m:
        return ()
    return (m.group(0), m.group(2))


def claves_variable(valor: str, olas: tuple[str, ...]) -> tuple[str, ...]:
    """Claves candidatas de una variable: exacta, plegada, y sin sufijo de ola.

    Son variantes de LA MISMA variable: la cobertura cuenta variables que
    emparejan, nunca claves — contar claves infla el denominador y hunde en
    falso la cobertura de todo instrumento con sufijo de ola (defecto medido
    en ENASEM 2018: 0.50 en vez de 1.00).
    """
    base = fold(valor)
    claves = [base]
    for ola in olas:
        sufijo = fold("_" + ola)
        if base.endswith(sufijo) and len(base) > len(sufijo):
            claves.append(base[: -len(sufijo)])
    return tuple(dict.fromkeys(claves))


PERIODO = re.compile(r"^(19|20)\d{2}[-/]\d{1,2}([-/]\d{1,2})?")


def es_periodo(valor: str) -> bool:
    """¿La 'variable' es en realidad un periodo? (tabla con el eje transpuesto)"""
    return bool(PERIODO.match(str(valor).strip()))


def lee_tsv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        lineas = [l for l in fh if not l.startswith("#")]
    return list(csv.DictReader(lineas, delimiter="\t"))


# ── lectura del FD real ────────────────────────────────────────────────────

ETIQUETA_TABLA = re.compile(r"^\s*tablas?\s*:\s*(.+)$", re.IGNORECASE)
ETIQUETA_SECCION = re.compile(r"^\s*\d+\.\s*secci[oó]n\s*$", re.IGNORECASE)
COLUMNA_BD = re.compile(r"^\s*nombre\s+de\s+la\s+bd\s*$", re.IGNORECASE)


def declaraciones_de_hoja(filas: list[tuple]) -> list[tuple[str, str]]:
    """Nombres de tabla que la hoja DECLARA, con la evidencia literal.

    Tres sondas, las tres medidas sobre descriptores reales de este corpus:
      1. celda `TABLA: X` / `Tabla: X`      (Censo 2020, ENDUTIH, CPV 2020)
      2. rótulo `N. Sección` + celda vecina (CNBV Ahorro/Financiamiento)
      3. columna `Nombre de la BD`          (CNBV BDIF)
    """
    encontrados: list[tuple[str, str]] = []
    col_bd = None
    for indice, fila in enumerate(filas):
        celdas = [("" if c is None else str(c).strip()) for c in fila]
        for pos, celda in enumerate(celdas):
            if not celda:
                continue
            if indice < 16:
                m = ETIQUETA_TABLA.match(celda)
                if m and m.group(1).strip():
                    encontrados.append((m.group(1).strip(), f"celda «{celda}»"))
                if ETIQUETA_SECCION.match(celda):
                    vecina = next((c for c in celdas[pos + 1:] if c), "")
                    if vecina:
                        encontrados.append((vecina, f"«{celda}» → «{vecina}»"))
            if col_bd is None and COLUMNA_BD.match(celda):
                col_bd = pos
                continue
        if col_bd is not None and indice > 0 and col_bd < len(celdas):
            valor = celdas[col_bd]
            if valor and not COLUMNA_BD.match(valor):
                encontrados.append((valor, f"columna «Nombre de la BD» = «{valor}»"))
    # Deduplica conservando el primer testimonio de cada nombre.
    vistos: dict[str, str] = {}
    for nombre, evidencia in encontrados:
        vistos.setdefault(nombre, evidencia)
    return list(vistos.items())


def abre_descriptor(path: Path, filas_max: int = 400) -> dict[str, list[tuple]]:
    """Devuelve {hoja: primeras filas} del FD real. Nunca abre microdato."""
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        from openpyxl import load_workbook
        libro = load_workbook(path, read_only=True, data_only=True)
        try:
            salida = {}
            for hoja in libro.worksheets:
                filas = []
                for indice, fila in enumerate(hoja.iter_rows(values_only=True)):
                    filas.append(fila)
                    if indice >= filas_max:
                        break
                salida[hoja.title] = filas
            return salida
        finally:
            libro.close()
    if path.suffix.lower() == ".xls":
        import xlrd
        libro = xlrd.open_workbook(str(path))
        return {h.name: [tuple(h.row_values(i)) for i in range(min(h.nrows, filas_max))]
                for h in libro.sheets()}
    raise ValueError(f"formato de descriptor no soportado: {path.suffix}")


# ── armado ─────────────────────────────────────────────────────────────────

def construye(objetos: list[str] | None, cobertura_min: float, margen_min: float):
    inventario = [r for p in INVENTARIOS for r in lee_tsv(p)]
    capa_fd = [r for p in CAPAS_FD for r in lee_tsv(p)]
    residual = lee_tsv(RESIDUAL_ENTRADA)

    if objetos:
        pedidos = {fold(o) for o in objetos}
        def pedido(inst: str) -> bool:
            f = fold(inst)
            return any(p in f for p in pedidos)
    else:
        def pedido(inst: str) -> bool:
            return True

    # Filas ciegas por (instrumento, miembro) — el denominador que se mueve.
    ciegas: dict[tuple[str, str], int] = defaultdict(int)
    for fila in residual:
        ciegas[(fila["instrumento"], fila["archivo_miembro"])] += 1

    vars_miembro: dict[tuple[str, str], set[str]] = defaultdict(set)
    payload_de: dict[tuple[str, str], str] = {}
    for fila in inventario:
        llave = (fila["instrumento"], fila["archivo_miembro"])
        vars_miembro[llave].add(fila["variable_id"])
        payload_de.setdefault(llave, fila["payload_id"])

    vars_hoja: dict[tuple[str, str], set[str]] = defaultdict(set)
    fuente_hoja: dict[tuple[str, str], tuple[str, str]] = {}
    payloads_fd: set[str] = set()
    for fila in capa_fd:
        llave = (fila["instrumento"], fila["archivo_miembro"])
        vars_hoja[llave].add(fila["variable_id"])
        fuente_hoja.setdefault(llave, (fila["payload_id"], fila["sha256_12"]))
        payloads_fd.add(fila["payload_id"])

    # Declaraciones leídas del FD REAL, por (instrumento, hoja).
    declarado: dict[tuple[str, str], list[tuple[str, str]]] = {}
    descriptores: dict[str, str] = {}
    fallos_descriptor: dict[str, str] = {}
    for (inst, _hoja), (payload_id, _sha) in list(fuente_hoja.items()):
        if not pedido(inst) or payload_id in descriptores or payload_id in fallos_descriptor:
            continue
        ruta = RAW_ROOT / payload_id
        if not ruta.exists():
            fallos_descriptor[payload_id] = "no está en la raíz montada"
            continue
        try:
            hojas = abre_descriptor(ruta)
        except Exception as exc:                                    # noqa: BLE001
            fallos_descriptor[payload_id] = f"{type(exc).__name__}: {exc}"
            continue
        descriptores[payload_id] = str(ruta)
        for titulo, filas in hojas.items():
            declarado[(inst, titulo)] = declaraciones_de_hoja(filas)

    filas_salida: list[dict] = []
    filas_residual: list[dict] = []

    instrumentos = sorted({i for (i, _m) in ciegas if pedido(i)})
    for inst in instrumentos:
        olas = olas_de(inst)
        hojas = {h: v for (i, h), v in vars_hoja.items() if i == inst}
        if not hojas:
            for (i, miembro), n in sorted(ciegas.items()):
                if i != inst:
                    continue
                filas_residual.append({
                    "instrumento": inst, "archivo_miembro": miembro,
                    "motivo": "SIN-CAPA-FD",
                    "detalle": "el instrumento no tiene ninguna hoja en la capa FD indexada",
                    "variables_miembro": len(vars_miembro[(inst, miembro)]),
                    "filas_ciegas": n, "mejor_candidata": "", "mejor_cobertura": "",
                })
            continue

        # Índice de claves por hoja (exacta / plegada / sin sufijo de ola).
        claves_hoja = {h: {c for v in vs for c in claves_variable(v, olas)}
                       for h, vs in hojas.items()}
        # Qué hoja declara qué nombre de tabla, con el RANGO de la evidencia:
        # 0 = el FD lo declara dentro de la hoja; 1 = sólo el título de la hoja.
        por_nombre: dict[str, list[tuple[int, str, str]]] = defaultdict(list)
        for hoja in hojas:
            por_nombre[normaliza_tabla(hoja)].append((1, hoja, "título de la hoja del FD"))
            for nombre, evidencia in declarado.get((inst, hoja), []):
                por_nombre[normaliza_tabla(nombre)].append((0, hoja, evidencia))

        candidatas_por_hoja: dict[str, list[tuple[float, str]]] = defaultdict(list)
        pendientes = []
        for (i, miembro), n_ciegas in sorted(ciegas.items()):
            if i != inst:
                continue
            vs = vars_miembro[(inst, miembro)]
            payload_miembro = payload_de.get((inst, miembro), "")
            if payload_miembro in payloads_fd:
                filas_residual.append({
                    "instrumento": inst, "archivo_miembro": miembro,
                    "motivo": "MIEMBRO-ES-EL-PROPIO-FD",
                    "detalle": f"el 'miembro' vive dentro de un descriptor ({payload_miembro}), "
                               "no dentro de un payload de datos: sus 'variables' son los "
                               "rótulos de columna del FD, no variables de la encuesta",
                    "variables_miembro": len(vs), "filas_ciegas": n_ciegas,
                    "mejor_candidata": "", "mejor_cobertura": "",
                })
                continue
            if NO_ES_TABLA.match(miembro.rsplit("/", 1)[-1]):
                filas_residual.append({
                    "instrumento": inst, "archivo_miembro": miembro,
                    "motivo": "NO-ES-TABLA-DE-DATOS",
                    "detalle": "índice, diagrama, catálogo o nota del descriptor: "
                               "no es una tabla de reactivos y no tiene enunciado que recuperar",
                    "variables_miembro": len(vs), "filas_ciegas": n_ciegas,
                    "mejor_candidata": "", "mejor_cobertura": "",
                })
                continue
            claves_por_var = {v: claves_variable(v, olas) for v in vs}
            marcador = []
            for hoja, ch in claves_hoja.items():
                # Cobertura por VARIABLE del miembro, no por clave: las claves
                # son variantes de la misma variable.
                comunes = sum(1 for cs in claves_por_var.values()
                              if any(c in ch for c in cs))
                if comunes:
                    marcador.append((comunes / max(1, len(vs)), comunes, hoja))
            marcador.sort(reverse=True)
            for cob, _c, hoja in marcador:
                candidatas_por_hoja[hoja].append((cob, miembro))
            pendientes.append((miembro, vs, claves_por_var, marcador, n_ciegas))

        for miembro, vs, claves_por_var, marcador, n_ciegas in pendientes:
            clave_m = normaliza_tabla(miembro)
            declaraciones = por_nombre.get(clave_m, [])
            mejor_rango = min((d[0] for d in declaraciones), default=None)
            declaraciones = [d for d in declaraciones if d[0] == mejor_rango]
            hojas_declaradas = {h for _r, h, _e in declaraciones}
            mejor = marcador[0] if marcador else (0.0, 0, "")
            segunda = marcador[1][0] if len(marcador) > 1 else 0.0
            cobertura = mejor[0]
            margen = cobertura - segunda

            metodo = evidencia = hoja_elegida = ""
            if len(hojas_declaradas) == 1:
                hoja_elegida = next(iter(hojas_declaradas))
                metodo = "FD-DECLARA-TABLA" if mejor_rango == 0 else "FD-NOMBRE-DE-HOJA"
                evidencia = next(e for _r, h, e in declaraciones if h == hoja_elegida)
            elif len(hojas_declaradas) > 1:
                filas_residual.append({
                    "instrumento": inst, "archivo_miembro": miembro,
                    "motivo": "TABLA-AMBIGUA",
                    "detalle": "más de una hoja del FD declara este nombre: "
                               + ", ".join(sorted(hojas_declaradas)),
                    "variables_miembro": len(vs), "filas_ciegas": n_ciegas,
                    "mejor_candidata": mejor[2], "mejor_cobertura": f"{cobertura:.4f}",
                })
                continue
            elif mejor[2]:
                hoja = mejor[2]
                mutuo = max(candidatas_por_hoja[hoja])[1] == miembro
                if cobertura >= cobertura_min and margen >= margen_min and mutuo:
                    hoja_elegida = hoja
                    metodo = "IDENTIDAD-DE-VARIABLES"
                    evidencia = (f"{mejor[1]}/{len(vs)} variables del miembro emparejan; "
                                 f"margen {margen:.2f} sobre la segunda candidata; "
                                 f"emparejamiento mutuo")
                else:
                    razon = []
                    if cobertura < cobertura_min:
                        razon.append(f"cobertura {cobertura:.2f} < {cobertura_min:.2f}")
                    if margen < margen_min:
                        razon.append(f"margen {margen:.2f} < {margen_min:.2f}")
                    if not mutuo:
                        razon.append("la hoja tiene un miembro mejor")
                    filas_residual.append({
                        "instrumento": inst, "archivo_miembro": miembro,
                        "motivo": "IDENTIDAD-INSUFICIENTE",
                        "detalle": "; ".join(razon),
                        "variables_miembro": len(vs), "filas_ciegas": n_ciegas,
                        "mejor_candidata": hoja, "mejor_cobertura": f"{cobertura:.4f}",
                    })
                    continue
            else:
                periodos = sum(1 for v in vs if es_periodo(v))
                if periodos >= 0.8 * max(1, len(vs)):
                    motivo = "EJE-TRANSPUESTO"
                    detalle = (f"{periodos}/{len(vs)} 'variables' del miembro son PERIODOS "
                               f"(p. ej. {', '.join(sorted(vs)[:2])}): la tabla está "
                               "transpuesta respecto del descriptor — los conceptos son "
                               "filas y los periodos columnas. No hay enunciado de reactivo "
                               "que recuperar para una columna que es una fecha")
                else:
                    motivo = "EJE-SIN-SOLAPE"
                    detalle = ("ninguna hoja del FD comparte una sola clave de variable "
                               "con este miembro: el eje del miembro no es el del descriptor")
                filas_residual.append({
                    "instrumento": inst, "archivo_miembro": miembro,
                    "motivo": motivo, "detalle": detalle,
                    "variables_miembro": len(vs), "filas_ciegas": n_ciegas,
                    "mejor_candidata": "", "mejor_cobertura": "0.0000",
                })
                continue

            comunes = sum(1 for cs in claves_por_var.values()
                          if any(c in claves_hoja[hoja_elegida] for c in cs))
            payload_fd, sha_fd = fuente_hoja[(inst, hoja_elegida)]
            filas_salida.append({
                "instrumento": inst,
                "archivo_miembro": miembro,
                "payload_id": payload_de.get((inst, miembro), ""),
                "hoja_fd": hoja_elegida,
                "payload_id_fd": payload_fd,
                "sha256_12_fd": sha_fd,
                "metodo": metodo,
                "evidencia_fd": evidencia,
                "clave_variable": "casefold+sufijo-de-ola" if olas else "casefold",
                "variables_miembro": len(vs),
                "variables_hoja": len(hojas[hoja_elegida]),
                "variables_comunes": comunes,
                "cobertura": f"{comunes / max(1, len(vs)):.4f}",
                "margen": f"{margen:.4f}",
                "filas_ciegas_cubiertas": n_ciegas,
            })

    resumen = {
        "version": VERSION,
        "instrumentos": len(instrumentos),
        "emparejamientos": len(filas_salida),
        "por_metodo": {m: sum(1 for f in filas_salida if f["metodo"] == m)
                       for m in sorted({f["metodo"] for f in filas_salida})},
        "filas_ciegas_cubiertas": sum(int(f["filas_ciegas_cubiertas"]) for f in filas_salida),
        "filas_ciegas_residuales": sum(int(f["filas_ciegas"]) for f in filas_residual),
        "por_motivo": {m: sum(int(f["filas_ciegas"]) for f in filas_residual if f["motivo"] == m)
                       for m in sorted({f["motivo"] for f in filas_residual})},
        "descriptores_abiertos": len(descriptores),
        "descriptores_no_abiertos": fallos_descriptor,
    }
    return filas_salida, filas_residual, resumen


def escribe(path: Path, campos: list[str], filas: list[dict], cabecera: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        for linea in cabecera:
            fh.write(f"# {linea}\n")
        escritor = csv.DictWriter(fh, fieldnames=campos, delimiter="\t",
                                  lineterminator="\n", extrasaction="ignore")
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--objeto", action="append",
                        help="Instrumento o familia; repetible. Por defecto, todos los "
                             "instrumentos con filas en el residual de entrada.")
    parser.add_argument("--salida", type=Path, default=SALIDA)
    parser.add_argument("--residual", type=Path, default=SALIDA_RESIDUAL)
    parser.add_argument("--cobertura-minima", type=float, default=0.95)
    parser.add_argument("--margen-minimo", type=float, default=0.30)
    parser.add_argument("--json", action="store_true", help="Sólo el resumen, sin escribir")
    args = parser.parse_args(argv)

    filas, residual, resumen = construye(args.objeto, args.cobertura_minima,
                                         args.margen_minimo)
    if args.json:
        print(json.dumps(resumen, indent=1, ensure_ascii=False, sort_keys=True))
        return 0

    cabecera_comun = [
        f"DERIVADO por tools/{Path(__file__).name} ({VERSION}). NO se edita a mano: se re-genera.",
        "ACTO GEN2-CAJA-REACTIVOS-FD-1 (15/sep/2026, CAJA). Acredita NC-0245 leyendo el FD REAL",
        "desde la raíz montada. Cero microdato abierto: sólo descriptores y metadato indexado.",
        f"umbrales: cobertura>={args.cobertura_minima} margen>={args.margen_minimo}",
    ]
    escribe(args.salida, CAMPOS, filas, cabecera_comun + [
        "Un emparejamiento que el FD no sostiene NO está aquí: está en el residual, con motivo.",
    ])
    escribe(args.residual, CAMPOS_RESIDUAL, residual, cabecera_comun + [
        "Lo que NO entra al crosswalk, por motivo acreditado. No se retira del denominador.",
    ])
    print(json.dumps(resumen, indent=1, ensure_ascii=False, sort_keys=True))
    print(f"CROSSWALK · {len(filas)} emparejamientos → {args.salida.relative_to(REPO_ROOT)} · "
          f"{len(residual)} residuales → {args.residual.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
