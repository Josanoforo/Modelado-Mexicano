#!/usr/bin/env python3
"""Deriva canon/tabla-de-piso-v1_0.tsv desde canon/catalogo-del-mexicano-v1_0.tsv.

ACTO GEN2-FRONT-2 (reto público, §1 P4): la tabla de piso publicable es
SOLO lo adoptado, nunca un piso histórico de contexto ni una propuesta con
adopción pendiente. "Adoptado" en el catálogo v1.0 son las dos filas de
`estado_adopcion` que representan consumo real u orden de mesa firmada:
`ADOPTADO-POR-FIRMA` y `CONSUMO-GEN2-ACTIVO`. Las demás (piso histórico de
contexto, sellado sin dictaminar, firma-adoptar con consumo pendiente,
en marcador por verificar, vetado) quedan fuera por diseño: no son la línea
que un retador tiene que vencer hoy.

Filtro y proyección, no medición nueva: cero cifras tecleadas, cero
contadores movidos. Uso:

    python3 tools/genera_tabla_piso.py
"""
from __future__ import annotations

import csv
import pathlib
import sys

csv.field_size_limit(sys.maxsize)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "canon/catalogo-del-mexicano-v1_0.tsv"
SALIDA = ROOT / "canon/tabla-de-piso-v1_0.tsv"

ESTADOS_ADOPTADOS = {"ADOPTADO-POR-FIRMA", "CONSUMO-GEN2-ACTIVO"}

COLUMNAS_SALIDA = [
    "area_consulta", "llave", "dominio", "conducta", "instrumento_ola",
    "segmento", "universo_denominador", "unidad_escala", "punto",
    "ic95_inf", "ic95_sup", "naturaleza_ic", "estado_adopcion",
    "result_punto", "calc", "sha256_resultados", "sha256_sello", "reserva",
]


def lee_catalogo() -> list[dict[str, str]]:
    with CATALOGO.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def filtra_adoptadas(filas: list[dict[str, str]]) -> list[dict[str, str]]:
    return [fila for fila in filas if fila["estado_adopcion"] in ESTADOS_ADOPTADOS]


def escribe(filas: list[dict[str, str]]) -> None:
    with SALIDA.open("w", newline="", encoding="utf-8") as stream:
        escritor = csv.DictWriter(
            stream, fieldnames=COLUMNAS_SALIDA, delimiter="\t",
            extrasaction="ignore", lineterminator="\n",
        )
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(fila)


def main() -> None:
    filas = lee_catalogo()
    adoptadas = filtra_adoptadas(filas)
    if not adoptadas:
        raise SystemExit("cero filas adoptadas: no se escribe una tabla de piso vacía")
    escribe(adoptadas)
    print(f"total_catalogo={len(filas)}")
    print(f"filas_adoptadas={len(adoptadas)}")
    for estado in sorted(ESTADOS_ADOPTADOS):
        print(f"  {estado}={sum(1 for f in adoptadas if f['estado_adopcion'] == estado)}")


if __name__ == "__main__":
    main()
