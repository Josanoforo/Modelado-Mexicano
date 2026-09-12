#!/usr/bin/env python3
"""Da de alta o cierra idempotentemente la NC de demanda preadopción."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "tools"))

from curador_registro.tsv_crudo import leer_lineas, upsert_fila  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cierra", action="store_true")
    args = parser.parse_args()
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
            "el valor GEN1 queda histórico y no se reactiva; los 207 elementos "
            "conservan identidad, propósito, contrato, estado, ejecutor y acción"),
        "sucesor": (
            "data/adq-demanda-activa-v1_0.json#elementos_gen2; cada pendiente "
            "continúa por su contrato_id, primer_faltante y ejecutor_siguiente"),
        "estado": "CERRADA" if args.cierra else "ABIERTA",
        "cerrado_por": (
            "ACTO GEN2-DEMANDA-CONCILIADA-Y-EJECUCION-NC0165"
            if args.cierra else "NO-APLICA-MIENTRAS-ABIERTA"),
        "fecha_cierre": "2026-09-11" if args.cierra else
        "NO-APLICA-MIENTRAS-ABIERTA",
    }, campos, clave="id")
    print("NC-0165 cerrada por conciliación total" if args.cierra else
          "NC-0165 enlazada idempotentemente a la demanda activa preadopción")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
