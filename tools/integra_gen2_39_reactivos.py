#!/usr/bin/env python3
"""Concilia NC-0100/NC-0136 y la anotación L0 tras GEN2-39.

La operación es idempotente y usa el escritor byte-preservante canónico:
solamente sustituye las filas identificadas por ``id`` y conserva todas las
demás líneas de ``forense/no-corrido.tsv`` byte a byte.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

from curador_registro.tsv_crudo import (  # noqa: E402
    escribir_texto_atomico,
    leer_lineas,
    upsert_fila,
)


NO_CORRIDO = RAIZ / "forense" / "no-corrido.tsv"
ESTADO = RAIZ / "canon" / "estado-programa-v1_12.md"
ANOTACION_L0 = "*(`ADR-490`, `ACTO GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL`, 11/sep/2026, CAJA Windows/WSL2 -- índice vigente 43,020/55,895 filas con texto acreditado y 20,653 identidades ganadas; buscador conectado; NC-0100 y NC-0136 conservan residuales explícitos; solapamiento accidental de dos sesiones 39 consolidado en PR #742, sin incorporar encargo 40; cero medición o adopción.)* "


def campos(path: Path) -> list[str]:
    return leer_lineas(path)[0].split("\t")


def integra() -> None:
    columnas = campos(NO_CORRIDO)
    filas = [
        {
            "id": "NC-0100",
            "fecha": "2026-09-11",
            "acto": "GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL",
            "pr": "#742",
            "pieza": "P1 (insumo)",
            "que_no_se_corrio": "acreditar texto para las 32 identidades DBF todavía residuales de ENVIPE 2013/2015",
            "razon": "EJECUTADA-PARCIAL-CON-RESIDUAL: GEN2-39 acreditó 791 de las 823 filas que faltaban; no inventa texto para variables ausentes del descriptor ni para correspondencias técnicas o ambiguas",
            "impacto": "El buscador vigente cubre 1272/1304 filas DBF: ENVIPE 2012 400/400, 2013 410/419 y 2015 462/485. Las 32 restantes siguen explícitas y el negativo de búsqueda no demuestra ausencia científica.",
            "sucesor": "NC-0100: acreditar 9 identidades de 2013 (2 EST_SOC técnicas y 7 documentales) y 23 de 2015 (18 técnicas/ambiguas y AP5_3_02, AP5_4_02, AP5_5_02, AP5_6_02, AP5_7_1 no localizadas en el descriptor oficial)",
            "estado": "ABIERTA",
            "cerrado_por": "NO-APLICA-MIENTRAS-ABIERTA",
            "fecha_cierre": "NO-APLICA-MIENTRAS-ABIERTA",
        },
        {
            "id": "NC-0136",
            "fecha": "2026-09-11",
            "acto": "GEN2-REACTIVOS-RESIDUALES-BUSQUEDA-UTIL",
            "pr": "#742",
            "pieza": "P3 (hallazgo ampliado al contestar el gate D-14 de NC-0123)",
            "que_no_se_corrio": "acreditar las 12875 filas residuales del lote prioritario y cubrir los 81 grupos históricamente ciegos que quedan fuera de ese lote",
            "razon": "EJECUTADA-PARCIAL-CON-RESIDUAL: GEN2-39 recorrió las cinco familias, publicó toda correspondencia viable y conservó explícitas las auxiliares, técnicas, ambiguas o no localizadas",
            "impacto": "La cobertura prioritaria sube de 22367/55895 a 43020/55895 filas físicas y de 22350 a 43003 identidades lógicas: gana 20653 identidades exactas. Quedan 12875 filas dentro del lote; los 81 grupos externos no se confundieron con ese residual.",
            "sucesor": "NC-0136: continuar por 81 grupos históricamente ciegos fuera del lote y por sus residuales acreditables; dentro del lote atender 2642 correspondencias ambiguas, 2679 etiquetas técnicas, 7462 filas auxiliares y 92 preguntas no localizadas",
            "estado": "ABIERTA",
            "cerrado_por": "NO-APLICA-MIENTRAS-ABIERTA",
            "fecha_cierre": "NO-APLICA-MIENTRAS-ABIERTA",
        },
    ]
    for fila in filas:
        upsert_fila(NO_CORRIDO, fila, columnas, clave="id")

    estado = ESTADO.read_text(encoding="utf-8")
    if ANOTACION_L0 not in estado:
        patron = re.compile(r"(\*\*L0 · Gobierno — completo y al día\.\*\* \d+ ADR )")
        estado, reemplazos = patron.subn(r"\1" + ANOTACION_L0, estado, count=1)
        if reemplazos != 1:
            raise RuntimeError("no se encontró exactamente el ancla inicial de L0")
        escribir_texto_atomico(ESTADO, estado)
    print("integración GEN2-39 aplicada: NC-0100/NC-0136 ABIERTAS y L0 anotado")


if __name__ == "__main__":
    integra()
