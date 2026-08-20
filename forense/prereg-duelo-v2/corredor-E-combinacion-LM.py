#!/usr/bin/env python3
"""
Corredor `E` — combinación mecánica L⊕M pre-registrada.

ACTO: DUELO-PREREG-V2 (nube, Opus). Escrito 20/ago/2026. Gate: T-SELLO + ACT-PIL-2 fusionados.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Spec de pre-registro.

Fuente normativa, verbatim (CAREO-ADV-DUELO-diseno-v2-2026-08-19.md §B,
línea de corredores): "E (combinación mecánica L⊕M pre-registrada, por
script)". También §A: "Ensemble E = L⊕M como corredor | 3/5 | INCORPORADO
(costo ≈0; responde la pregunta del híbrido) | Corredor E".

*** AMBIGÜEDAD SIN RESOLVER, DOCUMENTADA PARA MESA (ver
forense/prereg-duelo-v2/mesa-pendientes.md §3): *** el operador `⊕` NUNCA
se define formalmente en el corpus -- verificado por comando
(`grep -rn "⊕" forense/ canon/`): las tres apariciones son nominales
("L⊕M"), ninguna trae una fórmula. Este script implementa la combinación
mecánica MÁS SIMPLE posible, explícitamente rotulada como PROPUESTA, no
como definición sellada.
"""
from __future__ import annotations

import dataclasses
from typing import Literal


@dataclasses.dataclass(frozen=True)
class PrediccionCorredor:
    tipo_escala: Literal["continua", "binaria", "ordinal"]
    valor_punto: float | None = None           # continua: nivel; binaria: prob de "sí"
    valor_categoria: str | None = None          # ordinal/binaria: categoría elegida
    intervalo_lo: float | None = None
    intervalo_hi: float | None = None
    confianza_declarada: float | None = None    # 0-1, si el corredor la reporta


# --------------------------------------------------------------------------
# PROPUESTA, NO SELLADA: promedio simple para continuas, voto por mayoría
# con desempate por confianza declarada para categóricas/ordinales.
# --------------------------------------------------------------------------


def combinar_continua_PROPUESTA(pred_L: PrediccionCorredor, pred_M: PrediccionCorredor) -> PrediccionCorredor:
    """PROPUESTA sin sellar (ver mesa-pendientes.md §3): media aritmética
    simple del punto de L (mediana de sus k=5-10 corridas, ya agregada por
    ADV1-M2) y del punto de M. El intervalo combinado, si ambos corredores
    traen intervalo, es la envolvente (mínimo de los lo, máximo de los
    hi) -- una regla conservadora que NO asume independencia entre L y M
    (asumir independencia estrecharía el intervalo de forma injustificada,
    dado que ambos podrían compartir sesgos correlacionados)."""
    if pred_L.valor_punto is None or pred_M.valor_punto is None:
        raise ValueError("combinar_continua_PROPUESTA exige punto en ambos corredores.")
    punto_E = (pred_L.valor_punto + pred_M.valor_punto) / 2.0

    intervalo_lo = intervalo_hi = None
    if None not in (pred_L.intervalo_lo, pred_M.intervalo_lo, pred_L.intervalo_hi, pred_M.intervalo_hi):
        intervalo_lo = min(pred_L.intervalo_lo, pred_M.intervalo_lo)
        intervalo_hi = max(pred_L.intervalo_hi, pred_M.intervalo_hi)

    return PrediccionCorredor(
        tipo_escala="continua", valor_punto=punto_E,
        intervalo_lo=intervalo_lo, intervalo_hi=intervalo_hi,
    )


def combinar_categorica_PROPUESTA(pred_L: PrediccionCorredor, pred_M: PrediccionCorredor) -> PrediccionCorredor:
    """PROPUESTA sin sellar: si L y M coinciden en categoría, E hereda esa
    categoría con la confianza máxima de las dos. Si difieren, desempate
    por confianza declarada más alta; si ninguno declara confianza, E
    queda SIN DECISIÓN (no se elige arbitrariamente uno de los dos) y se
    reporta el empate para que el scoring lo trate como corresponda
    (posible INDECIDIBLE, ADV1-M3)."""
    if pred_L.valor_categoria == pred_M.valor_categoria:
        conf = max(
            pred_L.confianza_declarada or 0.0,
            pred_M.confianza_declarada or 0.0,
        )
        return PrediccionCorredor(
            tipo_escala=pred_L.tipo_escala,
            valor_categoria=pred_L.valor_categoria,
            confianza_declarada=conf or None,
        )

    conf_L = pred_L.confianza_declarada
    conf_M = pred_M.confianza_declarada
    if conf_L is not None and conf_M is not None and conf_L != conf_M:
        ganador = pred_L if conf_L > conf_M else pred_M
        return PrediccionCorredor(
            tipo_escala=pred_L.tipo_escala,
            valor_categoria=ganador.valor_categoria,
            confianza_declarada=ganador.confianza_declarada,
        )

    # Empate real, sin confianza que desempate -- no se decide arbitrariamente.
    return PrediccionCorredor(
        tipo_escala=pred_L.tipo_escala,
        valor_categoria=None,  # SIN DECISIÓN, declarado
        confianza_declarada=None,
    )


def combinar_E_PROPUESTA(pred_L: PrediccionCorredor, pred_M: PrediccionCorredor) -> PrediccionCorredor:
    """Punto de entrada único del corredor E. Enruta por tipo de escala.
    Toda esta función está marcada PROPUESTA -- mesa puede sustituirla
    por ponderación por skill histórico, por inversa de varianza, o por
    cualquier otra regla, siempre que quede pre-registrada ANTES de que
    R exista para la celda que se combine (mismo requisito de hash-antes-
    de-R que L, M y B, ADV1-M2)."""
    if pred_L.tipo_escala != pred_M.tipo_escala:
        raise ValueError("L y M deben responder en la misma escala declarada por la spec de la celda.")
    if pred_L.tipo_escala == "continua":
        return combinar_continua_PROPUESTA(pred_L, pred_M)
    return combinar_categorica_PROPUESTA(pred_L, pred_M)


if __name__ == "__main__":
    raise SystemExit(
        "corredor-E-combinacion-LM.py es spec de pre-registro (PROPUESTA "
        "sin sellar para el operador ⊕, ver mesa-pendientes.md §3), no se "
        "ejecuta en este acto (DUELO-PREREG-V2, NUBE, repo-only)."
    )
