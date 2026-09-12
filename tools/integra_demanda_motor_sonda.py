#!/usr/bin/env python3
"""Da de alta idempotente la NC que enlaza demanda activa preadopción."""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

from curador_registro.tsv_crudo import leer_lineas, upsert_fila  # noqa: E402


def main() -> int:
    ruta = RAIZ / "forense" / "no-corrido.tsv"
    campos = leer_lineas(ruta)[0].split("\t")
    upsert_fila(ruta, {
        "id": "NC-0165",
        "fecha": "2026-09-11",
        "acto": "GEN2-38-DEMANDA-MOTOR-A-SONDA",
        "pr": "#739",
        "pieza": "alcance activo del motor anterior a adopción",
        "que_no_se_corrio": (
            "contrato GEN2 corriente, preparación, cálculo, validación y "
            "adopción de los elementos activos que aún sólo leen antecedente GEN1"),
        "razon": (
            "la vista anterior entraba por corrida0_generacion=GEN2 y ocultaba "
            "la demanda todavía no adoptada"),
        "impacto": (
            "el valor GEN1 queda histórico y no se reactiva; cada elemento conserva "
            "situación, evidencia, dependencia, responsable y siguiente acción"),
        "sucesor": (
            "MOTOR_GEN2 concilia por RES y completa primero decisión/preparación; "
            "cuando verifique una brecha de fuente o acceso, el proyector la entrega "
            "a SONDA; validación y adopción permanecen en sus ejecutores"),
        "estado": "ABIERTA",
        "cerrado_por": "NO-APLICA-MIENTRAS-ABIERTA",
        "fecha_cierre": "NO-APLICA-MIENTRAS-ABIERTA",
    }, campos, clave="id")
    print("NC-0165 enlazada idempotentemente a la demanda activa preadopción")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
