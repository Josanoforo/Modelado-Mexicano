# -*- coding: utf-8 -*-
"""Lector de `milpa/estimadores-por-segmento.yaml` (DERIVADO por
`tools/marcador_segmento.py`).

ACTO GEN2-MARCADOR-REDISENO-1 (adenda de dirección, 19/sep/2026), P2.

Este módulo NO calibra, NO adopta y NO escribe nada: consulta un YAML ya
derivado y devuelve la emisión exacta que trae, o `None` si la celda pedida
no está ahí. La adopción por celda ocurre en `tools/marcador_segmento.py`
(qué entra al YAML) y en `decisiones.tsv` (objeto
`adopcion:piso-C2-20-celdas`, firma de mesa) -- este módulo es solo la
ranura de consulta que `milpa/src/motor.py::estimar_segmento` expone.
"""
from __future__ import annotations

from pathlib import Path

import yaml

RUTA_ESTIMADORES = (Path(__file__).resolve().parents[2]
                     / "milpa" / "estimadores-por-segmento.yaml")


def _carga(ruta: Path | None = None) -> dict:
    ruta = ruta or RUTA_ESTIMADORES
    if not ruta.exists():
        return {}
    crudo = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    return crudo.get("celdas") or {}


def estimador_de_celda(celda_id: str, *, ruta: Path | None = None) -> dict | None:
    """Devuelve `{punto, ic95_inf, ic95_sup, unidad_dato, tipo_incertidumbre,
    resultado_id, regla_origen}` para `celda_id`, o `None` si esa celda no
    tiene estimador adoptado en el YAML derivado (p. ej. una celda marginal
    SIN-PISO). `celda_id` es el mismo id que trae `marcador-segmento.tsv`
    en su columna `celda_id` (p. ej. `CRUCE::DIN...::L1xE1`)."""
    celdas = _carga(ruta)
    entrada = celdas.get(celda_id)
    if entrada is None:
        return None
    return dict(entrada)


__all__ = ["estimador_de_celda", "RUTA_ESTIMADORES"]
