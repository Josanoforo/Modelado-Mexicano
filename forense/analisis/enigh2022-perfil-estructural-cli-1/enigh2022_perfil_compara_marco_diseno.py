#!/usr/bin/env python3
"""Compara agregadamente el marco estrato–UPM con el dominio principal.

No emite estratos, UPM ni llaves persona; solo conteos y huellas de conjuntos.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import zipfile


PAYLOAD_SHA256 = "3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06"
POBLACION = (
    "conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/"
    "conjunto_de_datos_poblacion_enigh2022_ns.csv"
)
COLUMNAS = ("parentesco", "edad", "factor", "est_dis", "upm")
PREFIJOS_INTEGRANTE = {"1", "2", "3", "5", "6"}


def texto(valor: object) -> str:
    return str(valor or "").lstrip("\ufeff").lstrip("ï»¿").strip().strip('"')


def peso_valido(valor: object) -> bool:
    try:
        peso = float(texto(valor))
    except ValueError:
        return False
    return math.isfinite(peso) and peso > 0


def edad_entera(valor: object) -> int | None:
    valor_limpio = texto(valor)
    return int(valor_limpio) if valor_limpio.isdigit() else None


def sha_archivo(ruta: Path) -> str:
    digest = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            digest.update(bloque)
    return digest.hexdigest()


def huella_pares(pares: set[tuple[str, str]]) -> str:
    canon = json.dumps(sorted(pares), ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canon.encode("utf-8")).hexdigest()


def resumen_claves(filas: list[dict[str, str]]) -> dict[str, int]:
    ambos = sum(not fila["est_dis"] and not fila["upm"] for fila in filas)
    sin_estrato = sum(not fila["est_dis"] and bool(fila["upm"]) for fila in filas)
    sin_upm = sum(bool(fila["est_dis"]) and not fila["upm"] for fila in filas)
    return {
        "faltante_alguna_n": ambos + sin_estrato + sin_upm,
        "faltante_ambas_n": ambos,
        "faltante_solo_estrato_n": sin_estrato,
        "faltante_solo_upm_n": sin_upm,
    }


def pares_validos(filas: list[dict[str, str]]) -> set[tuple[str, str]]:
    return {(fila["est_dis"], fila["upm"]) for fila in filas if fila["est_dis"] and fila["upm"]}


def estratos_singleton(pares: set[tuple[str, str]]) -> tuple[int, int]:
    por_estrato: dict[str, set[str]] = {}
    for estrato, upm in pares:
        por_estrato.setdefault(estrato, set()).add(upm)
    return len(por_estrato), sum(len(upms) == 1 for upms in por_estrato.values())


def comparar(payload: Path) -> dict[str, object]:
    payload_sha = sha_archivo(payload)
    if payload_sha != PAYLOAD_SHA256:
        raise ValueError(f"hash de payload distinto: {payload_sha}")

    filas: list[dict[str, str]] = []
    with zipfile.ZipFile(payload) as zf, zf.open(POBLACION) as bruto:
        lector = csv.DictReader(io.TextIOWrapper(bruto, encoding="latin-1", newline=""))
        if lector.fieldnames is None:
            raise ValueError("poblacion: cabecera ausente")
        mapa = {texto(columna).lower(): columna for columna in lector.fieldnames}
        faltan = [columna for columna in COLUMNAS if columna not in mapa]
        if faltan:
            raise ValueError(f"poblacion: columnas ausentes {faltan}")
        for raw in lector:
            fila = {columna: texto(raw.get(mapa[columna], "")) for columna in COLUMNAS}
            filas.append(fila)

    marco_peso_valido = [fila for fila in filas if peso_valido(fila["factor"])]
    principales = []
    for fila in filas:
        edad = edad_entera(fila["edad"])
        if (
            peso_valido(fila["factor"])
            and fila["parentesco"][:1] in PREFIJOS_INTEGRANTE
            and edad is not None
            and 18 <= edad <= 96
        ):
            principales.append(fila)

    pares_marco = pares_validos(marco_peso_valido)
    pares_principal = pares_validos(principales)
    estratos_marco, singleton_marco = estratos_singleton(pares_marco)
    estratos_principal, singleton_principal = estratos_singleton(pares_principal)
    fuera_dominio = len(marco_peso_valido) - len(principales)

    return {
        "alcance": "comparacion agregada; no publica identificadores de estrato, UPM, hogar o persona",
        "definicion_marco": "todas las filas de poblacion con factor finito y positivo",
        "definicion_principal": "prefijo parentesco 1/2/3/5/6, edad entera 18-96 y factor finito y positivo",
        "payload": {
            "bytes": payload.stat().st_size,
            "sha256": payload_sha,
        },
        "filas_poblacion_n": len(filas),
        "marco_peso_valido": {
            "filas_n": len(marco_peso_valido),
            "claves_diseno": resumen_claves(marco_peso_valido),
            "estratos_n": estratos_marco,
            "pares_estrato_upm_n": len(pares_marco),
            "estratos_upm_unica_n": singleton_marco,
            "huella_conjunto_pares_sha256": huella_pares(pares_marco),
        },
        "universo_principal": {
            "filas_n": len(principales),
            "claves_diseno": resumen_claves(principales),
            "estratos_n": estratos_principal,
            "pares_estrato_upm_n": len(pares_principal),
            "estratos_upm_unica_n": singleton_principal,
            "huella_conjunto_pares_sha256": huella_pares(pares_principal),
        },
        "comparacion": {
            "filas_peso_valido_fuera_dominio_n": fuera_dominio,
            "pares_en_marco_no_en_principal_n": len(pares_marco - pares_principal),
            "pares_en_principal_no_en_marco_n": len(pares_principal - pares_marco),
            "conjuntos_pares_identicos": pares_marco == pares_principal,
            "estratos_en_marco_no_en_principal_n": len({p[0] for p in pares_marco} - {p[0] for p in pares_principal}),
            "estratos_en_principal_no_en_marco_n": len({p[0] for p in pares_principal} - {p[0] for p in pares_marco}),
            "singleton_cambia": singleton_marco != singleton_principal,
        },
        "tratamiento_claves_faltantes": (
            "Las filas con est_dis o upm vacío no forman pares. En el medidor sellado, cualquier clave "
            "faltante dentro del universo principal desactiva toda precisión; no se imputa ni se crea una UPM."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("payload", type=Path)
    parser.add_argument("--salida", type=Path)
    args = parser.parse_args()
    resultado = comparar(args.payload)
    serializado = json.dumps(resultado, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.salida:
        args.salida.write_text(serializado, encoding="utf-8")
    print(serializado, end="")


if __name__ == "__main__":
    main()
