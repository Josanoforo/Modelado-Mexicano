#!/usr/bin/env python3
"""
Corredor `B` — baseline tonto obligatorio.

ACTO: DUELO-PREREG-V2 (nube, Opus). Escrito 20/ago/2026. Gate: T-SELLO + ACT-PIL-2 fusionados.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Spec de pre-registro.

Fuente normativa, verbatim (CAREO-ADV-DUELO-diseno-v2-2026-08-19.md §B,
línea de corredores): "B (baseline tonto obligatorio: tasa base de la
última ola pública o persistencia)".

B es uno de los "cuatro corredores comprometidos por hash antes de que R
exista" (ADV1-M2). Su spec es deliberadamente mecánica: NO requiere modelo
de lenguaje ni motor de decisión, solo lectura de la ola anterior publicada
del mismo reactivo -- si existe -- o persistencia del valor de la ola
inmediatamente anterior de la misma serie si el reactivo se repite.
"""
from __future__ import annotations

import dataclasses


@dataclasses.dataclass(frozen=True)
class ObservacionOlaPrevia:
    """Un valor ya publicado de una ola anterior del MISMO reactivo (misma
    encuesta, mismo mnemónico o su equivalente documentado entre olas)."""

    encuesta: str
    ola: str
    valor: float
    fuente_publicada: str  # cita del tabulado oficial de esa ola, verbatim


def baseline_ultima_ola_publica(historial: list[ObservacionOlaPrevia]) -> ObservacionOlaPrevia | None:
    """Regla mecánica: toma la ola pública MÁS RECIENTE anterior a la ola
    que el piloto va a arbitrar. No promedia entre olas, no ajusta
    tendencia -- es "tonto" por diseño (CAREO §A: "Baseline B obligatorio",
    5/5 corridas adversariales lo exigen exactamente por ser trivial de
    vencer). Si `historial` está vacío, devuelve None -- la celda queda
    SIN BASELINE, se declara, no se sustituye por un supuesto."""
    if not historial:
        return None
    return max(historial, key=lambda obs: obs.ola)


def baseline_persistencia(valor_ola_inmediatamente_anterior: float | None) -> float | None:
    """Persistencia pura: el corredor B predice, para la ola nueva,
    exactamente el mismo valor que la ola inmediatamente anterior de la
    misma serie -- sin importar si esa ola es "pública" en el sentido
    estricto del filtro M1(i) (no-publicada). Se usa cuando NO hay una
    ola pública previa del mismo reactivo pero sí existe una medición
    previa cualquiera de la misma serie temporal (p.ej. otra ola de la
    misma encuesta, con otro corte muestral)."""
    return valor_ola_inmediatamente_anterior


def elegir_baseline(
    historial_publico: list[ObservacionOlaPrevia],
    valor_ola_inmediatamente_anterior: float | None,
) -> dict:
    """Precedencia mecánica y declarada: (1) tasa base de la última ola
    PÚBLICA si existe; (2) si no, persistencia de la ola inmediatamente
    anterior de la serie; (3) si ninguna existe, SIN BASELINE -- la celda
    no se puntúa contra B (afecta directamente ADV1-M5 casilla (4), que
    exige comparar contra B para decidir "ninguno utilizable v1")."""
    ultima_publica = baseline_ultima_ola_publica(historial_publico)
    if ultima_publica is not None:
        return {
            "metodo": "ultima_ola_publica",
            "valor": ultima_publica.valor,
            "fuente": ultima_publica.fuente_publicada,
            "ola_origen": ultima_publica.ola,
        }
    persistencia = baseline_persistencia(valor_ola_inmediatamente_anterior)
    if persistencia is not None:
        return {"metodo": "persistencia", "valor": persistencia, "fuente": None, "ola_origen": None}
    return {"metodo": "SIN_BASELINE", "valor": None, "fuente": None, "ola_origen": None}


if __name__ == "__main__":
    raise SystemExit(
        "corredor-B-tasa-base.py es spec de pre-registro, no se ejecuta "
        "en este acto (DUELO-PREREG-V2, NUBE, repo-only)."
    )
