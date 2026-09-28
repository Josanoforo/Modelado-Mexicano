#!/usr/bin/env python3
"""Comprueba cobertura editorial explícita y produce el índice local del lote.

El juicio de cada fila pertenece al editor. Este programa comprueba referencias,
campos obligatorios y correspondencia entre decisiones, mapa y archivos publicados.
"""
from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
LOTE = Path(__file__).resolve().parent
MAPA = ROOT / "canon/mapa-dominios-v1_1.tsv"
REPORTS = {
    "humor": "Humor_in_Mexican_Psychological_Life__2023-2026_Update.md",
    "interaccion": "La_arquitectura_invisible_de_la_interacción_social_en_México.md",
    "moral": "Moral_Emotions_in_Mexico__Declared_Dignity__Relational_Face__and_Residual_Catholic_Guilt.md",
    "sancion": "Sanción_Social_Horizontal_en_México__Chisme__Envidia_y_Mal_de_Ojo_como_Mecanismos_de_Nivelación.md",
}
ESTADOS = {"CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"}
CAMPOS = {"id", "id_mapa", "afirmacion_original", "dictamen", "razon", "evidencia"}


def filas(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as f:
        lector = csv.DictReader(f, delimiter="\t")
        return list(lector.fieldnames or []), list(lector)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="regenera indice-local.md")
    args = ap.parse_args()
    _, mapa = filas(MAPA)
    problemas: list[str] = []
    resumen: list[tuple[str, int, int, Counter[str]]] = []
    for clave, nombre in REPORTS.items():
        fuente = f"corpus/reports/{nombre}"
        esperados = {f["id_afirmacion"] for f in mapa if f["report"] == fuente}
        tabla = LOTE / clave / "tabla-afirmaciones.tsv"
        report = ROOT / "corpus/reports-v2" / nombre
        if not tabla.is_file():
            problemas.append(f"{clave}: falta tabla {tabla}")
            continue
        if not report.is_file():
            problemas.append(f"{clave}: falta report {report}")
            continue
        cabecera, decisiones = filas(tabla)
        faltantes = CAMPOS - set(cabecera)
        if faltantes:
            problemas.append(f"{clave}: faltan columnas {sorted(faltantes)}")
            continue
        vistos: set[str] = set()
        mapa_visto: set[str] = set()
        conteo: Counter[str] = Counter()
        for n, fila in enumerate(decisiones, 2):
            id_ = fila["id"].strip()
            if not id_ or id_ in vistos:
                problemas.append(f"{clave}:{n}: id vacío o repetido: {id_}")
            vistos.add(id_)
            estado = fila["dictamen"].strip()
            if estado not in ESTADOS:
                problemas.append(f"{clave}:{n}: dictamen inválido: {estado}")
            conteo[estado] += 1
            for campo in ("afirmacion_original", "razon", "evidencia"):
                if not fila[campo].strip():
                    problemas.append(f"{clave}:{n}: {campo} vacío")
            # Este lote declara cero RESULT propios; un valor nuevo necesita
            # contrato numérico completo y revisión editorial antes de entrar.
            if fila.get("result_propio", "").strip() not in ("", "NINGUNO"):
                problemas.append(f"{clave}:{n}: RESULT propio sin contrato de este lote")
            if fila.get("RESULT", "").strip():
                problemas.append(f"{clave}:{n}: RESULT propio sin contrato de este lote")
            if fila.get("adopcion", "").strip() not in ("", "NO_ADOPTA"):
                problemas.append(f"{clave}:{n}: adopción nueva no autorizada")
            for id_mapa in fila["id_mapa"].replace(";", ",").split(","):
                id_mapa = id_mapa.strip()
                if id_mapa:
                    if id_mapa not in esperados:
                        problemas.append(f"{clave}:{n}: id_mapa ajeno: {id_mapa}")
                    mapa_visto.add(id_mapa)
        sin_cubrir = esperados - mapa_visto
        if sin_cubrir:
            problemas.append(f"{clave}: mapa sin cubrir ({len(sin_cubrir)}): {', '.join(sorted(sin_cubrir))}")
        if not decisiones:
            problemas.append(f"{clave}: tabla vacía")
        prosa = report.read_text(encoding="utf-8")
        if len(prosa.split()) < 500:
            problemas.append(f"{clave}: report demasiado breve para Bloque B")
        for enlace in re.findall(r"\]\(([^)]+)\)", prosa):
            if enlace.startswith(("https://", "http://", "#")):
                continue
            ruta = (report.parent / enlace.split("#", 1)[0]).resolve()
            if not ruta.is_file():
                problemas.append(f"{clave}: enlace local roto: {enlace}")
        resumen.append((clave, len(esperados), len(decisiones), conteo))

    lineas = [
        "# Índice local · interacción, emociones morales, humor y sanción horizontal",
        "",
        "Conteos editoriales derivados de las decisiones explícitas. Las cláusulas de una misma tesis pueden ocupar varias filas; estos conteos no son estimadores ni tesis independientes.",
        "",
        "| Report | Mapa cubierto | Registros editoriales | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for clave, n_mapa, n_filas, conteo in resumen:
        lineas.append(
            f"| [{clave}](../../../../corpus/reports-v2/{REPORTS[clave]}) | {n_mapa} | {n_filas} | "
            + " | ".join(str(conteo[estado]) for estado in ("CONFIRMA", "MATIZA", "ROMPE", "SIN-CIFRA"))
            + " |"
        )
    lineas += ["", "Las tablas por report conservan el dictamen, razón y evidencia de cada afirmación; las propuestas de reglas permanecen sujetas a firma de contenido.", ""]
    indice = LOTE / "indice-local.md"
    contenido = "\n".join(lineas)
    if args.write and not problemas:
        indice.write_text(contenido, encoding="utf-8")
    elif indice.exists() and indice.read_text(encoding="utf-8") != contenido:
        problemas.append("indice-local.md no corresponde a las tablas; ejecute --write")
    for documento in LOTE.rglob("*.md"):
        for enlace in re.findall(r"\]\(([^)]+)\)", documento.read_text(encoding="utf-8")):
            if enlace.startswith(("https://", "http://", "#")):
                continue
            ruta = (documento.parent / enlace.split("#", 1)[0]).resolve()
            if not ruta.is_file():
                problemas.append(f"{documento.relative_to(LOTE)}: enlace local roto: {enlace}")
    for p in problemas:
        print("ERROR", p)
    print(f"reportes={len(resumen)}/4; filas={sum(n for _, _, n, _ in resumen)}; errores={len(problemas)}")
    return bool(problemas)


if __name__ == "__main__":
    raise SystemExit(main())
