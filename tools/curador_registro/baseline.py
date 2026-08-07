#!/usr/bin/env python3
"""Validación reusable de un baseline semántico demanda-universo."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable


NO_DETERMINADO = "NO_DETERMINADO"
ARCHIVOS_TSV = {
    "relaciones": "relaciones.tsv",
    "evidencias": "evidencias.tsv",
    "artefactos_rechazados": "artefactos-rechazados.tsv",
    "decisiones_humanas": "decisiones-humanas.tsv",
    "utilidad_modelo": "utilidad-modelo.tsv",
    "aliases_fuentes": "aliases-fuentes.tsv",
    "fusiones_relaciones": "fusiones-relaciones.tsv",
}
ESTADOS = {"CONFIRMADA", "NEGATIVA", "CANDIDATA", "NO_ACCESIBLE"}
METADATOS_OPERATIVOS = {
    "worker_id",
    "hash_archivo_worker",
    "timestamp",
    "ruta_staging",
    "log",
}


def leer_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relacion_id(necesidad: str, fuente: str, objeto: str) -> str:
    clave = "\x1f".join((necesidad, fuente, objeto)).encode("utf-8")
    return "REL-" + hashlib.sha256(clave).hexdigest()[:24]


def _duplicados(valores: Iterable[str]) -> list[str]:
    conteo = Counter(valores)
    return sorted(valor for valor, cantidad in conteo.items() if cantidad != 1)


def validar_baseline(directorio: Path) -> dict[str, object]:
    errores: list[str] = []
    manifest_path = directorio / "baseline.json"
    if not manifest_path.is_file():
        return {"ok": False, "errores": ["falta baseline.json"]}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    tablas: dict[str, list[dict[str, str]]] = {}
    for nombre, archivo in ARCHIVOS_TSV.items():
        path = directorio / archivo
        if not path.is_file():
            errores.append(f"falta {archivo}")
            tablas[nombre] = []
            continue
        tablas[nombre] = leer_tsv(path)
        esperado = manifest.get("archivos", {}).get(archivo, {}).get("sha256")
        if esperado != sha256(path):
            errores.append(f"hash inválido: {archivo}")

    relaciones = tablas["relaciones"]
    evidencias = tablas["evidencias"]
    decisiones = tablas["decisiones_humanas"]
    utilidad = tablas["utilidad_modelo"]
    fusiones = tablas["fusiones_relaciones"]

    ids = [fila.get("relacion_id", "") for fila in relaciones]
    for fila in relaciones:
        esperado = relacion_id(
            fila.get("necesidad_id", ""),
            fila.get("fuente_canonica_normalizada", ""),
            fila.get("objeto_evidencia_id_canonico", ""),
        )
        if fila.get("relacion_id") != esperado:
            errores.append(f"relacion_id no determinista: {fila.get('relacion_id', '')}")
        if fila.get("clasificacion_relacion") not in ESTADOS:
            errores.append(f"estado inválido: {fila.get('relacion_id', '')}")
    if duplicados := _duplicados(ids):
        errores.append(f"relaciones duplicadas o vacías: {duplicados}")

    conjunto_ids = set(ids)
    por_relacion: dict[str, list[dict[str, str]]] = defaultdict(list)
    for fila in evidencias:
        rid = fila.get("relacion_id", "")
        por_relacion[rid].append(fila)
        if rid not in conjunto_ids:
            errores.append(f"procedencia huérfana: {rid}")
        if METADATOS_OPERATIVOS.intersection(fila):
            errores.append("evidencias.tsv contiene columnas operativas")
        if not fila.get("procedencia_id"):
            errores.append(f"procedencia sin identificador: {rid}")
    faltantes = sorted(conjunto_ids - set(por_relacion))
    if faltantes:
        errores.append(f"relaciones sin procedencia: {faltantes}")
    if duplicados := _duplicados(f.get("procedencia_id", "") for f in evidencias):
        errores.append(f"procedencias duplicadas o vacías: {duplicados}")

    uso_ids = [fila.get("relacion_id", "") for fila in utilidad]
    if set(uso_ids) != conjunto_ids or len(uso_ids) != len(conjunto_ids):
        errores.append("utilidad-modelo.tsv no es una proyección 1:1")

    decisiones_ids = {fila.get("decision_id", "") for fila in decisiones}
    for fila in utilidad:
        if fila.get("requiere_decision") == "SI" and fila.get("decision_id") not in decisiones_ids:
            errores.append(f"decisión no vinculada: {fila.get('relacion_id', '')}")

    exceso = len(evidencias) - len(relaciones)
    if exceso != len(fusiones):
        errores.append("diferencia procedencias-relaciones no explicada por fusiones")
    for fusion in fusiones:
        rid = fusion.get("relacion_id", "")
        if rid not in conjunto_ids or len(por_relacion.get(rid, [])) < 2:
            errores.append(f"fusión sin procedencias conservadas: {rid}")

    conteo_estados = Counter(f.get("clasificacion_relacion", "") for f in relaciones)
    derivados = {
        "relaciones_activas": len(relaciones),
        "procedencias_aceptadas": len(evidencias),
        "artefactos_rechazados": len(tablas["artefactos_rechazados"]),
        "decisiones_pendientes": sum(f.get("estado_decision") == "PENDIENTE" for f in decisiones),
        "familias_alias": len(tablas["aliases_fuentes"]),
        "fusiones_declaradas": len(fusiones),
        "confirmadas": conteo_estados["CONFIRMADA"],
        "negativas": conteo_estados["NEGATIVA"],
        "candidatas": conteo_estados["CANDIDATA"],
        "no_accesibles": conteo_estados["NO_ACCESIBLE"],
    }
    declarados = manifest.get("conteos", {})
    for clave, valor in derivados.items():
        if declarados.get(clave) != valor:
            errores.append(f"conteo no reconciliado: {clave}")

    return {"ok": not errores, "conteos": derivados, "errores": errores}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    args = parser.parse_args()
    resultado = validar_baseline(args.baseline.resolve())
    print(json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if resultado["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
