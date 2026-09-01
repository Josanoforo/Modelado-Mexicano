#!/usr/bin/env python3
"""Registra las 6 necesidades de FP-190 como activos descubiertos (P2, MAESTRA33-A5).

Via manual precedentada (Dominio 3, precedente 0e07179): appende filas a
activos-descubiertos-durante-ronda.tsv -- snapshot_universe.py solo la
inicializa vacia, nunca la reescribe (lineas 677-683), asi que este script
tampoco la reescribe: es idempotente, no duplica filas ya presentes por
origen.

Cada fila cita su origen exacto en data/cola-adquisicion-v1_0.tsv (A.13).
No decide adquisicion nueva -- eso lo hace decide_acquisition.py, corrido
por separado sobre el archivo que este script deja escrito.
"""

from __future__ import annotations

import csv
import hashlib
from pathlib import Path

FIELDS = ["activo_descubierto_id", "fecha", "origen", "localizador", "estado", "reserva"]

FP190 = [
    {
        "origen": "FP190_SFT-04",
        "localizador": "https://www.inegi.org.mx/contenidos/programas/enasem/2018/microdatos/enasem_2018_fd.xlsx",
        "estado": "EVIDENCIA_LOCALIZADA",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:75 (fp190-1, ENASEM_ABVD_BANAR_DICCIONARIO_DATOS). "
            "FP-190 SFT-04: payload FD de ENASEM 2018/2021/2024 ya OBTENIDO desde antes de "
            "esta fila (enasem2018_fd_xlsx;enasem2021_fd_xlsx;enasem2024_fd_xlsx en manifiesto.yaml). "
            "Falta confirmar que ABVD_BANAR_* pregunta por ayuda recibida, no dificultad -- tarea "
            "de lectura del diccionario ya adquirido, no de adquisicion nueva. Ver "
            "forense/notas/2026-09-01-mapeo-fp190.md#SFT-04."
        ),
    },
    {
        "origen": "FP190_CIV-08",
        "localizador": "forense/notas/2026-09-01-mapeo-fp190.md#CIV-08",
        "estado": "EVIDENCIA_LOCALIZADA",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:76 (fp190-2, ENVIPE_EXTRACCION_TEXTO_REACTIVO). "
            "FP-190 CIV-08: ENVIPE ya esta en el corpus (en_corpus=SI, v1_2:131370-76) pero sus "
            "filas de inventario son solo titulos de catalogo -- 0% texto de reactivo real. "
            "Requiere extraccion de texto nueva sobre un payload ya OBTENIDO, no una adquisicion. "
            "Fuera del perimetro de /adquiere (declarado explicito: no abre ni analiza contenido "
            "semantico)."
        ),
    },
    {
        "origen": "FP190_TIC-06",
        "localizador": "https://www.inegi.org.mx/contenidos/programas/enti/2022/microdatos/enti_2022_fd.pdf",
        "estado": "EVIDENCIA_LOCALIZADA",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:77 (fp190-3, ENTI_DICCIONARIO_DATOS_DBF). FP-190 TIC-06: "
            "diccionario de datos de ENTI 2022 (enti2022_fd_pdf) ya OBTENIDO desde antes de esta "
            "fila (Encargo B-3, mesa #20). Falta confirmar si P2 captura estacionalidad "
            "('todos los meses') -- lectura del diccionario ya adquirido, no adquisicion nueva. "
            "Ver forense/notas/2026-09-01-mapeo-fp190.md#TIC-06."
        ),
    },
    {
        "origen": "FP190_DIN-07",
        "localizador": "forense/notas/2026-09-01-mapeo-fp190.md#DIN-07",
        "estado": "EVIDENCIA_LOCALIZADA",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:78 (fp190-4, BANXICO_ENCUESTA_COMPETENCIAS_FINANCIERAS_"
            "EXTRACCION_TEXTO). FP-190 DIN-07: payload ya OBTENIDO (cola-adquisicion-v1_0.tsv:33, "
            "ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024). Requiere extraccion de texto "
            "nueva sobre ese .xlsx (306 filas sin texto_reactivo), no una adquisicion. Fuera del "
            "perimetro de /adquiere."
        ),
    },
    {
        "origen": "FP190_DIN-11",
        "localizador": "forense/notas/2026-09-01-mapeo-fp190.md#DIN-11",
        "estado": "NO_LOCALIZADO",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:79 (fp190-5, DIN-11_CONOCIMIENTO_CUENTAS_SIN_COMISION_"
            "SIN_CANDIDATA). FP-190 DIN-11: NO-ENCONTRADO tras 5 formulaciones de busqueda sobre "
            "241591 filas (/mapea, cobertura-15-v1_0.tsv coincide). Hueco real declarado, sin URL "
            "ni instrumento candidato que /adquiere pueda perseguir -- no se inventa via de red "
            "sin destino."
        ),
    },
    {
        "origen": "FP190_SFT-06",
        "localizador": "forense/notas/2026-09-01-mapeo-fp190.md#SFT-06",
        "estado": "NO_LOCALIZADO",
        "reserva": (
            "cola-adquisicion-v1_0.tsv:80 (fp190-6, SFT-06_ACUERDO_CUIDADO_ENTRE_HERMANOS_SIN_"
            "CANDIDATA). FP-190 SFT-06: NO-ENCONTRADO tras 5 formulaciones de busqueda sobre "
            "241591 filas (/mapea, cobertura-15-v1_0.tsv coincide). Hueco real declarado, sin URL "
            "ni instrumento candidato -- no se inventa via de red sin destino."
        ),
    },
]


def stable_id(origen: str) -> str:
    return "ADESC-" + hashlib.sha256(origen.encode("utf-8")).hexdigest()[:24]


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    path = Path("data/curacion-universo/activos-descubiertos-durante-ronda.tsv")
    existing = read_tsv(path)
    existing_origins = {row["origen"] for row in existing}
    added = 0
    for spec in FP190:
        if spec["origen"] in existing_origins:
            continue
        existing.append({
            "activo_descubierto_id": stable_id(spec["origen"]),
            "fecha": "2026-09-01",
            "origen": spec["origen"],
            "localizador": spec["localizador"],
            "estado": spec["estado"],
            "reserva": spec["reserva"],
        })
        added += 1
    write_tsv(path, existing)
    print(f"activos_descubiertos_total={len(existing)} agregados={added}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
