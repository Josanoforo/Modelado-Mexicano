#!/usr/bin/env python3
"""Censo de las seis evaluaciones de la etapa de retadores cerrada el 23/sep
(v2.16 s9, cierre citado en canon/estado-programa-v1_17.md #15). Ninguna cifra
se deriva de microdato aqui: las seis vienen citadas y ya selladas en
canon/informe-programa-v1_3-ANEXO.md (Astra U3, ajeno, no se edita) y las
familias de retador vienen citadas en canon/estado-programa-v1_17.md #15. El
script falla en voz alta si la frase que cita cada numero deja de estar en su
fuente -- no hay numero tecleado sin verificacion de linaje.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ANEXO = ROOT / "canon/informe-programa-v1_3-ANEXO.md"
ESTADO = ROOT / "canon/estado-programa-v1_17.md"

# (etiqueta, instrumento, n_celdas_de_cruce, frase citable verbatim en ANEXO)
# Duelo ENIGH 2024 es un punto nacional sin cruce adjudicable (ANEXO, fila
# "Duelo ENIGH 2024"): cuenta como evaluacion, no como celdas de cruce.
EVALUACIONES = [
    ("Lote ENIF 2024", "ENIF", 44, "44 celdas puntuadas de 96 de diseño"),
    ("Piloto 3 ENCIG 2025", "ENCIG", 15, "Trámite, 15 celdas del cruce"),
    ("Duelo ENIGH 2024", "ENIGH", 0, "punto nacional, sin cruce adjudicable"),
    ("Duelo ENVIPE 2026", "ENVIPE", 24, "12 celdas SXD y 12 EXD"),
    ("Piloto 4 ENVIPE 2025", "ENVIPE", 38, "cuatro cruces y 38 celdas puntuadas"),
    ("Cierre ENCIG 2025", "ENCIG", 16, "dos cruces de 8 celdas"),
]

FAMILIAS_RETADOR = ["encogida", "tendencia", "C1/C7", "suavizados", "AP", "C-ASTRA", "θ sin emitir"]
FRASE_FAMILIAS = "Siete familias de retador"
FRASE_CIERRE = "Se cierra la etapa de retadores"


def _exige_cita(texto: str, frase: str, fuente: Path) -> None:
    if frase not in texto:
        raise SystemExit(f"CITA ROTA: {frase!r} ya no está en {fuente} -- no se puede derivar")


def calcula() -> dict:
    anexo_txt = ANEXO.read_text(encoding="utf-8")
    estado_txt = ESTADO.read_text(encoding="utf-8")
    for _, _, _, frase in EVALUACIONES:
        _exige_cita(anexo_txt, frase, ANEXO)
    _exige_cita(estado_txt, FRASE_FAMILIAS, ESTADO)
    _exige_cita(estado_txt, FRASE_CIERRE, ESTADO)

    instrumentos = sorted({instr for _, instr, _, _ in EVALUACIONES})
    return {
        "n_evaluaciones": len(EVALUACIONES),
        "n_instrumentos": len(instrumentos),
        "instrumentos": ",".join(instrumentos),
        "n_celdas_total": sum(n for _, _, n, _ in EVALUACIONES),
        "n_familias_retador": len(FAMILIAS_RETADOR),
        "familias_retador": ",".join(FAMILIAS_RETADOR),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clave", default=None, help="imprime solo este valor")
    args = ap.parse_args()

    valores = calcula()
    if args.clave:
        if args.clave not in valores:
            raise SystemExit(f"clave desconocida: {args.clave}")
        print(valores[args.clave])
        return 0

    for k, v in valores.items():
        print(f"{k}={v}")
    for label, instr, n, frase in EVALUACIONES:
        print(f"# {label} ({instr}): {n} celdas -- cita {frase!r} verificada en ANEXO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
