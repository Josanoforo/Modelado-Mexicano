#!/usr/bin/env python3
"""Deriva canon/tabla-de-piso-v1_1.tsv desde canon/catalogo-del-mexicano-v1_2.tsv.

ACTO GEN2-CIERRE-SEMANAL-1 (P4). Sucesora de la tabla v1.0 (GEN2-FRONT-2), que
queda intacta con su propio generador (`tools/genera_tabla_piso.py`, E.1).

La tabla de piso es la línea que un retador de `docs/reto.md` tiene que
vencer: SOLO lo adoptado. En el catálogo v1.2 toda fila es adopción firmada
citada por id (`firma_fp`); aquí se proyecta con los hashes de su CALC
(`forense/analisis/catalogo/v1_2/calcs.tsv`) y el área de consulta pública.
El eje NSE (A4, FIRMAS-16) y el regional (`ENTIDAD`) entran donde el catálogo
los trae; `eje_nse_o_region` lo marca para filtrar sin leer el catálogo.

Filtro y proyección, no medición nueva: cero cifras tecleadas, cero
contadores movidos. Uso:

    python3 tools/genera_tabla_piso_v1_1.py            # cuenta; no escribe (D-23)
    python3 tools/genera_tabla_piso_v1_1.py --escribe  # escribe la tabla
    python3 tools/genera_tabla_piso_v1_1.py --verifica # 1 si la tabla difiere
"""
from __future__ import annotations

import csv
import io
import pathlib
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CATALOGO = ROOT / "canon/catalogo-del-mexicano-v1_2.tsv"
CALCS = ROOT / "forense/analisis/catalogo/v1_2/calcs.tsv"
SALIDA = ROOT / "canon/tabla-de-piso-v1_1.tsv"

ESTADOS_ADOPTADOS = {"ADOPTADO", "ADOPTADO-CON-RESERVA-DE-ANCHO"}

# Áreas de consulta pública (mismas etiquetas que v1.0, por dominio del mapa U0).
AREA = {
    "DINERO": "Dinero y crédito",
    "CONSUMO": "Ingreso y gasto",
    "CONFIANZA": "Trámites y Estado",
    "POLITICA": "Seguridad y norma",
    "VIOLENCIA": "Seguridad y norma",
    "CAPITAL_SOCIAL": "Confianza, religión y vínculos",
    "RELIGIOSIDAD": "Confianza, religión y vínculos",
    "FAMILIA_CUIDADOS": "Tiempo, cuidado y vínculos",
    "MIGRACION": "Tiempo, cuidado y vínculos",
    "TRABAJO": "Trabajo",
    "GENERO": "Violencia contra las mujeres",
    "TECNOLOGIA": "Tecnología",
    "SALUD": "Salud y bienestar",
    "SALUD_MENTAL": "Salud y bienestar",
}

COLUMNAS = [
    "area_consulta", "llave", "dominio", "conducta", "instrumento", "ola", "eje",
    "segmento", "eje_nse_o_region", "unidad", "punto", "ic95_inf", "ic95_sup",
    "naturaleza_ic", "estado_adopcion", "temporalidad", "firma_fp", "result_id",
    "celda", "calc", "sha256_resultados", "sha256_sello", "reserva",
]


def lee(path: pathlib.Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as s:
        return list(csv.DictReader(s, delimiter="\t"))


def filas() -> list[dict[str, str]]:
    hashes = {r["calc"]: r for r in lee(CALCS)}
    out = []
    for r in lee(CATALOGO):
        if r["estado_adopcion"] not in ESTADOS_ADOPTADOS:
            continue
        if r["dominio"] not in AREA:
            raise SystemExit(f"dominio sin área de consulta: {r['dominio']} ({r['llave']})")
        eje = r["eje"].upper()
        marca = "NSE" if eje == "NSE" else "REGION" if eje in ("ENTIDAD", "REGION") else ""
        out.append({**r, "area_consulta": AREA[r["dominio"]], "eje_nse_o_region": marca,
                    "sha256_resultados": hashes[r["calc"]]["sha256_resultados"],
                    "sha256_sello": hashes[r["calc"]]["sha256_sello"]})
    if not out:
        raise SystemExit("cero filas adoptadas: no se escribe una tabla de piso vacía")
    return out


def texto(rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUMNAS, delimiter="\t", extrasaction="ignore",
                       lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main(argv: list[str]) -> int:
    rows = filas()
    nuevo = texto(rows)
    if "--verifica" in argv:
        igual = SALIDA.exists() and SALIDA.read_text(encoding="utf-8") == nuevo
        print("COINCIDE" if igual else "DIFIERE")
        return 0 if igual else 1
    if "--escribe" in argv:
        SALIDA.write_text(nuevo, encoding="utf-8")
    print(f"filas_adoptadas={len(rows)}")
    for k, n in sorted(Counter(r["area_consulta"] for r in rows).items()):
        print(f"  area:{k}={n}")
    for k, n in sorted(Counter(r["eje_nse_o_region"] or "OTRO-EJE" for r in rows).items()):
        print(f"  eje:{k}={n}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
