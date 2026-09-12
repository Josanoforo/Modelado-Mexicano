#!/usr/bin/env python3
"""Guardia de uso: expone cobertura por dimensión sin fabricar un puntaje."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import adq_investigacion

RAIZ = Path(__file__).resolve().parent.parent


def proyecta(necesidad_id: str, cfg: dict | None = None,
             raiz: Path = RAIZ) -> dict:
    cfg = cfg or adq_investigacion.cargar_config()
    contratos = {x["id"]: x for x in cfg.get("necesidades", [])}
    if necesidad_id not in contratos:
        raise KeyError(f"{necesidad_id}: sin contrato operativo de suficiencia")
    contrato = contratos[necesidad_id]
    estado = adq_investigacion._lee_json(
        raiz / cfg["estado_dir"] / f"{necesidad_id}.json")
    suficiencia = estado.get("suficiencia") or contrato.get("suficiencia_actual")
    if not suficiencia:
        suficiencia = {
            **{x: "NO_ACREDITADA" for x in ("identidad", "conceptual", "poblacional",
                                               "seleccion_no_respuesta", "unidad",
                                               "temporalidad", "diseno", "identificacion")},
            "uso_habilitado": "INCOMPATIBLE", "pregunta_original": "ABIERTA",
        }
    accion = {
        "APTA_USO_DECLARADO": "PUEDE_EMITIR_USO_DECLARADO",
        "APTA_ALCANCE_MENOR": "SOLO_EMITIR_ALCANCE_MENOR_ROTULADO",
        "INCOMPATIBLE": "NO_EMITIR_RESULTADO_SOLICITADO",
    }[suficiencia["uso_habilitado"]]
    return {
        "necesidad_id": necesidad_id, "version_pregunta": contrato["version_pregunta"],
        "consumidor": contrato["consumidor"], "uso_solicitado": contrato["uso"],
        "accion_consumidor": accion, "suficiencia": suficiencia,
        "brecha": contrato["brecha"], "evidencias": estado.get("evidencias", []),
        "fuente_estado": ("investigacion-estado" if estado.get("suficiencia")
                          else "contrato-operativo-inicial"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--prepara-uso", metavar="NC_ID")
    ap.add_argument("--todas", action="store_true")
    args = ap.parse_args()
    cfg = adq_investigacion.cargar_config()
    if args.prepara_uso:
        print(json.dumps(proyecta(args.prepara_uso, cfg), ensure_ascii=False, indent=2))
        return 0
    if args.todas:
        print(json.dumps([proyecta(x["id"], cfg) for x in cfg["necesidades"]],
                         ensure_ascii=False, indent=2))
        return 0
    ap.error("elige --prepara-uso NC_ID o --todas")


if __name__ == "__main__":
    raise SystemExit(main())
