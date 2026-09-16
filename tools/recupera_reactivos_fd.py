#!/usr/bin/env python3
"""ACTO GEN2-RESIDUAL-81-1 — recupera enunciados de reactivo desde la capa FD ya indexada.

Qué resuelve. `ACTO GEN2-REACTIVOS-RESIDUALES-2` (`ADR-519`) midió que 18 de los
81 grupos históricamente ciegos de `NC-0136` (16 815 filas) tienen su texto
publicado DENTRO del repositorio, en `data/inventario-fd-v1_1.tsv`. Lo que no
pudo hacer —y este acto sí— es **cruzarlo por identidad exacta**: el cruce crudo
por `(archivo_miembro, variable_id)` daba **CERO** emparejamientos.

La causa, medida y no supuesta: las dos capas usan vocabularios distintos para
`archivo_miembro`. El índice de reactivos nombra el **miembro del payload**
(`thogar.csv`, `mod_2017_ciberacoso.dbf`); la capa FD nombra la **hoja del
descriptor** (`THOGAR`, `MOD_2017_CIBERACOSO`). Y en ENASEM la hoja viene
**truncada a 31 caracteres**, que es el límite de nombre de hoja de Excel
(`tr_enasem24_master_follow_up_file.csv` ↔ `TR_ENASEM24_MASTER_FOLLOW_UP_FI`).

El puente, en dos pasos, cada uno con su causa nombrada:

  (a) plegar a minúsculas y quitar la extensión conocida del miembro;
  (b) si (a) no empareja, aceptar **prefijo de 31 caracteres** (el límite de
      Excel) **sólo cuando la tabla candidata es única** en ese instrumento.

Lo que este tool NO hace, por doctrina explícita de
`ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL` («no hay propagación entre olas ni
fallback cruzado por el mero nombre de variable»):

  - no empareja por `variable_id` cuando la tabla no resuelve — 10 765 filas
    emparejarían así y **ninguna se publica**;
  - no propaga texto entre olas de un mismo instrumento;
  - no resuelve una tabla ambigua por cercanía de nombre.

Todo lo no publicado sale, con su motivo, al residual: el denominador no se
maquilla. Cero microdato: las dos capas son metadato puro.

Uso:
    python3 tools/recupera_reactivos_fd.py            # resumen a stdout
    python3 tools/recupera_reactivos_fd.py --escribe  # además publica los dos TSV
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

UNIVERSO = {
    "v1_2": REPO_ROOT / "data" / "inventario-reactivos-v1_2.tsv",
    "ext": REPO_ROOT / "data" / "inventario-reactivos-ext-v1_0.tsv",
}
CAPA_FD = REPO_ROOT / "data" / "inventario-fd-v1_1.tsv"
CENSO = REPO_ROOT / "data" / "reactivos-ciegos-81-v1_0.tsv"

SALIDA = REPO_ROOT / "data" / "inventario-reactivos-fd-recuperado-v1_0.tsv"
RESIDUAL = REPO_ROOT / "data" / "reactivos-fd-recuperado-residual-v1_0.tsv"

# Extensiones de miembro que el índice de reactivos trae y el FD nunca lleva.
EXTENSIONES = {".csv", ".dbf", ".sav", ".dta", ".xlsx", ".xls", ".rdata", ".rds", ".txt", ".por"}
LIMITE_HOJA_EXCEL = 31

COLUMNAS = ["id_origen", "payload_id", "sha256_12", "instrumento", "ola", "archivo_miembro",
            "variable_id", "texto_reactivo", "texto_tipo", "contexto_busqueda", "metodo",
            "universo_declarado", "fuente_texto", "fuente_sha256_12", "referencia_fuente"]
COLUMNAS_RESIDUAL = ["instrumento", "archivo_miembro", "variable_id", "motivo", "detalle"]


def lee_filas(path: Path) -> list[dict]:
    """TSV plano sin comillas CSV: líneas `#` fuera, luego csv.DictReader.
    Mismo convenio de lectura que tools/busca_reactivos.py::lee_filas."""
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader((l for l in f if not l.startswith("#")), delimiter="\t"))


def pliega_miembro(miembro: str) -> str:
    """Paso (a) del puente: minúsculas, sin ruta interna del zip y sin extensión conocida.

    La ruta se quita porque el índice a veces guarda el camino DENTRO del
    paquete (`enut_2019/THOGAR.csv`) y el descriptor nunca lo lleva: es una
    diferencia de cómo se escribió el miembro, no de qué tabla es. La extensión,
    igual. Ninguno de los dos pasos decide identidad — sólo normaliza ortografía.
    """
    m = (miembro or "").strip().lower()
    m = m.rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    raiz, ext = os.path.splitext(m)
    return raiz if ext in EXTENSIONES else m


def texto_tipo(texto: str) -> str:
    """PREGUNTA_DICCIONARIO si el texto trae interrogación; ETIQUETA_VARIABLE si no.

    Mismo vocabulario que `data/inventario-reactivos-contexto-v1_1.tsv`; nunca
    `PREGUNTA_COMPLETA`, que ese overlay reserva para el enunciado íntegro leído
    del cuestionario y no del descriptor.
    """
    return "PREGUNTA_DICCIONARIO" if "¿" in (texto or "") else "ETIQUETA_VARIABLE"


def grupos_con_fd_limpio() -> set[str]:
    """Los instrumentos que el censo de ADR-519 rotuló CABLEAR-CAPA-FD-YA-EN-REPO.

    Se lee del censo en vez de re-derivarlo: ese archivo es el objeto que NC-0235
    nombra, y re-derivar aquí crearía una segunda definición del mismo conjunto.
    """
    if not CENSO.exists():
        return set()
    return {r["instrumento"] for r in lee_filas(CENSO)
            if r.get("ruta_recuperacion") == "CABLEAR-CAPA-FD-YA-EN-REPO"}


def indexa_fd() -> tuple[dict, dict]:
    """instrumento -> tabla_plegada -> variable_plegada -> fila FD; y tablas por instrumento."""
    por_tabla: dict = defaultdict(lambda: defaultdict(dict))
    tablas: dict = defaultdict(set)
    for r in lee_filas(CAPA_FD):
        if not (r.get("texto_reactivo") or "").strip():
            continue
        ins = r["instrumento"]
        tabla = pliega_miembro(r["archivo_miembro"])
        por_tabla[ins][tabla][(r["variable_id"] or "").strip().lower()] = r
        tablas[ins].add(tabla)
    return por_tabla, tablas


def recupera() -> dict:
    ciegos = grupos_con_fd_limpio()
    fd, tablas = indexa_fd()

    publicadas: list[dict] = []
    residual: list[dict] = []
    motivos: dict = defaultdict(int)
    examinados = 0

    for clave, path in UNIVERSO.items():
        if not path.exists():
            continue
        examinados += 1
        for n, r in enumerate(lee_filas(path), start=1):
            ins = r.get("instrumento")
            if ins not in ciegos:
                continue
            tabla = pliega_miembro(r.get("archivo_miembro"))
            var = (r.get("variable_id") or "").strip().lower()

            destino = None
            via = ""
            if tabla in fd[ins] and var in fd[ins][tabla]:
                destino = fd[ins][tabla][var]
                via = "EXACTO"
            else:
                candidatas = [t for t in tablas[ins]
                              if t[:LIMITE_HOJA_EXCEL] == tabla[:LIMITE_HOJA_EXCEL]]
                if len(candidatas) > 1:
                    motivos["TABLA_AMBIGUA"] += 1
                    residual.append({"instrumento": ins, "archivo_miembro": r.get("archivo_miembro"),
                                     "variable_id": r.get("variable_id"), "motivo": "TABLA_AMBIGUA",
                                     "detalle": f"{len(candidatas)} hojas FD comparten el prefijo de {LIMITE_HOJA_EXCEL}"})
                    continue
                if len(candidatas) == 1 and var in fd[ins][candidatas[0]]:
                    destino = fd[ins][candidatas[0]][var]
                    via = "EXACTO_PREFIJO_31"

            if destino is None:
                if tabla not in fd[ins] and not [t for t in tablas[ins]
                                                 if t[:LIMITE_HOJA_EXCEL] == tabla[:LIMITE_HOJA_EXCEL]]:
                    motivo, detalle = "TABLA_SIN_FD", "la hoja no existe en el descriptor indexado"
                else:
                    motivo, detalle = "VARIABLE_SIN_FD", "la hoja empareja; la variable no aparece en ella"
                motivos[motivo] += 1
                residual.append({"instrumento": ins, "archivo_miembro": r.get("archivo_miembro"),
                                 "variable_id": r.get("variable_id"), "motivo": motivo,
                                 "detalle": detalle})
                continue

            motivos[via] += 1
            publicadas.append({
                "id_origen": f"{clave}:{n}",
                "payload_id": r.get("payload_id", ""),
                "sha256_12": r.get("sha256_12", ""),
                "instrumento": ins,
                "ola": r.get("ola", ""),
                "archivo_miembro": r.get("archivo_miembro", ""),
                "variable_id": r.get("variable_id", ""),
                "texto_reactivo": destino.get("texto_reactivo", ""),
                # El FD mezcla, en la MISMA columna, etiquetas de variable
                # («Condición de actividad») y preguntas literales del
                # cuestionario («6.33.1 En promedio, ¿cuántas horas…?»). Rotular
                # todo como etiqueta subdeclararía, y rotular todo como pregunta
                # sobredeclararía. Se separa por un rasgo observable —la marca de
                # interrogación— y se declara el criterio en la cabecera: es una
                # heurística de rotulado, no una afirmación sobre la fuente.
                "texto_tipo": texto_tipo(destino.get("texto_reactivo", "")),
                "contexto_busqueda": "",
                "metodo": r.get("metodo", ""),
                "universo_declarado": r.get("universo_declarado", ""),
                "fuente_texto": destino.get("payload_id", ""),
                "fuente_sha256_12": destino.get("sha256_12", ""),
                "referencia_fuente": (f"capa=fd;miembro={destino.get('payload_id','')};"
                                      f"hoja={destino.get('archivo_miembro','')};via={via}"),
            })

    tipos: dict = defaultdict(int)
    for f in publicadas:
        tipos[f["texto_tipo"]] += 1
    return {"publicadas": publicadas, "residual": residual, "motivos": dict(motivos),
            "texto_tipos": dict(tipos),
            "grupos": len(ciegos), "archivos_examinados": examinados + 1}


CABECERA = """# {ruta} -- DERIVADO por tools/recupera_reactivos_fd.py
# ACTO GEN2-RESIDUAL-81-1 (16/sep/2026, NUBE, sin corpus). NO se edita a mano: se re-genera.
#   python3 tools/recupera_reactivos_fd.py --escribe
# {que}
# IDENTIDAD: instrumento + tabla + variable, EXACTA. La tabla se empareja plegando el miembro
# (minusculas, sin extension) y, si eso no basta, por prefijo de 31 caracteres -- el limite de
# nombre de hoja de Excel que trunca las hojas del descriptor -- y SOLO cuando la hoja candidata
# es unica. NUNCA se empareja por variable_id con la tabla sin resolver (10765 filas emparejarian
# asi y ninguna se publica), NUNCA se propaga texto entre olas y una tabla ambigua nunca se
# resuelve por cercania: doctrina de ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL, no aflojada aqui.
# ROTULADO: el FD mezcla en una sola columna etiquetas de variable y preguntas literales. Se separan
# por un rasgo observable -- la marca de interrogacion -- en ETIQUETA_VARIABLE / PREGUNTA_DICCIONARIO.
# Es una heuristica de rotulado declarada, no una afirmacion sobre la fuente. Nunca PREGUNTA_COMPLETA:
# ese rotulo lo reserva contexto-v1_1 para el enunciado integro leido del cuestionario, no del
# descriptor. ALCANCE (A.15): recuperar texto
# no acredita suficiencia cientifica, ni existencia de un constructo, ni comparabilidad entre olas.
"""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--escribe", action="store_true", help="publica los dos TSV derivados")
    args = ap.parse_args(argv)

    c = recupera()
    total = len(c["publicadas"]) + len(c["residual"])

    if args.escribe:
        for ruta, filas, cols, que in (
            (SALIDA, c["publicadas"], COLUMNAS,
             "Una fila por identidad ciega del indice que la capa FD resuelve por identidad EXACTA."),
            (RESIDUAL, c["residual"], COLUMNAS_RESIDUAL,
             "Una fila por identidad ciega que la capa FD NO resuelve, con su motivo acreditado."),
        ):
            with ruta.open("w", encoding="utf-8", newline="") as f:
                f.write(CABECERA.format(ruta=ruta.relative_to(REPO_ROOT), que=que))
                w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", lineterminator="\n")
                w.writeheader()
                for fila in filas:
                    w.writerow(fila)

    print(f"GRUPOS · {c['grupos']} con capa FD limpia (censo de ADR-519) · "
          f"archivos examinados = {c['archivos_examinados']} (A.13)")
    print(f"FILAS CIEGAS EXAMINADAS · {total}")
    print(f"  RECUPERADAS por identidad exacta · {len(c['publicadas'])}")
    for k in ("EXACTO", "EXACTO_PREFIJO_31"):
        if c["motivos"].get(k):
            print(f"      {k:<20} {c['motivos'][k]}")
    for k, v in sorted(c["texto_tipos"].items()):
        print(f"      texto_tipo {k:<22} {v}")
    print(f"  RESIDUAL · {len(c['residual'])}")
    for k in ("TABLA_SIN_FD", "VARIABLE_SIN_FD", "TABLA_AMBIGUA"):
        if c["motivos"].get(k):
            print(f"      {k:<20} {c['motivos'][k]}")
    if args.escribe:
        print(f"ESCRITO · {SALIDA.relative_to(REPO_ROOT)} · {RESIDUAL.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
