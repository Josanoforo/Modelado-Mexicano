#!/usr/bin/env python3
"""
Corredor `E` — combinación mecánica pre-registrada del operador `⊕`.

ACTO: SELLA-OPLUS (nube, Opus). Escrito 21/ago/2026. Gate: `#3` (`ADR-140`,
`PR #307`) fusionado.

*** ESTE SCRIPT NO SE EJECUTA EN ESTE ACTO. *** Spec de pre-registro.

*** DEFINICIÓN SELLADA DE `⊕` (deja de ser propuesta; ver
forense/prereg-duelo-v2/mesa-pendientes.md §3, RESUELTA 2026-08-21,
`canon/gobernanza-v1_15.md` `ADR-141`): ***

    `E = mediana_por_cuantil({L-solo, L+corpus, M})`

`E` combina TRES corredores — `L-solo`, `L+corpus` y `M` (no dos; `L-solo`
y `L+corpus` son las dos variantes de `L` que `ADV1-M2` ya exige correr
por separado, `pipeline-L-adv1-m2.py` §1) — con peso igual, sin entrenar,
tomando la mediana por cuantil (para continuas: mediana punto a punto de
los tres valores puntuales y, cuantil a cuantil, de sus tres intervalos;
para categóricas/ordinales: moda de las tres categorías, con la misma
regla de empate que la propuesta anterior).

Las tres razones de la firma de mesa, benchmark del 20/ago, ninguna de
preferencia (verbatim, `forense/prereg-duelo-v2/mesa-pendientes.md` §3
tras el sello):

* Peso igual, no óptimo -- forecast combination puzzle: la combinación con
  pesos óptimos estimados típicamente no supera a la media/mediana con
  peso fijo, porque el ruido de estimar el peso introduce una penalización
  que tapa la ganancia teórica del peso óptimo.
* Mediana, no media -- de las opciones de ensamble evaluadas, la más
  influyente fue usar la mediana en vez de la media, sin importar el
  método de ponderación: pronósticos anómalos en un ensamble de media
  producen incertidumbre extremadamente ancha.
* Tres, no dos -- con dos corredores la mediana degenera en la media y se
  pierde la robustez; con tres (`L-solo`, `L+corpus`, `M`) la mediana está
  bien definida y un corredor descarrilado no arrastra al ensamble.
* Sin entrenar, con razón escrita -- los ensambles entrenados con
  selección de componentes superaron al de mediana con peso igual, pero
  exigen historial de desempeño que este piloto (el primero) no tiene.

Este script SUSTITUYE la PROPUESTA anterior (promedio simple L-M, voto por
mayoría) documentada hasta el sello en este mismo archivo. La propuesta
anterior combinaba dos corredores (`L`, `M`); esta definición sellada
combina tres (`L-solo`, `L+corpus`, `M`) -- no es una reformulación de la
misma fórmula, es la fórmula que mesa eligió en su lugar.
"""
from __future__ import annotations

import dataclasses
import statistics
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
# SELLADA (ADR-141): mediana por cuantil de los tres corredores para
# continuas; moda de las tres categorías (con desempate por confianza
# declarada) para categóricas/ordinales.
# --------------------------------------------------------------------------


def combinar_continua(
    pred_L_solo: PrediccionCorredor,
    pred_L_corpus: PrediccionCorredor,
    pred_M: PrediccionCorredor,
) -> PrediccionCorredor:
    """Mediana por cuantil de los tres corredores. El punto de `E` es la
    mediana de los tres puntos; el intervalo de `E`, si los tres traen
    intervalo, es la mediana punto a punto de los `lo` y de los `hi` -- no
    la envolvente (esa regla era de la propuesta de dos corredores, donde
    la envolvente evitaba asumir independencia entre solo L y M; con tres
    corredores la mediana por cuantil ya hereda la robustez que se buscaba
    sin ensanchar artificialmente el intervalo)."""
    puntos = [pred_L_solo.valor_punto, pred_L_corpus.valor_punto, pred_M.valor_punto]
    if any(p is None for p in puntos):
        raise ValueError("combinar_continua exige punto en los tres corredores (L-solo, L+corpus, M).")
    punto_E = statistics.median(puntos)

    intervalo_lo = intervalo_hi = None
    los = [pred_L_solo.intervalo_lo, pred_L_corpus.intervalo_lo, pred_M.intervalo_lo]
    his = [pred_L_solo.intervalo_hi, pred_L_corpus.intervalo_hi, pred_M.intervalo_hi]
    if all(v is not None for v in los + his):
        intervalo_lo = statistics.median(los)
        intervalo_hi = statistics.median(his)

    return PrediccionCorredor(
        tipo_escala="continua", valor_punto=punto_E,
        intervalo_lo=intervalo_lo, intervalo_hi=intervalo_hi,
    )


def combinar_categorica(
    pred_L_solo: PrediccionCorredor,
    pred_L_corpus: PrediccionCorredor,
    pred_M: PrediccionCorredor,
) -> PrediccionCorredor:
    """Moda de las tres categorías -- con tres votantes la moda siempre
    existe salvo empate a tres bandas distintas (0-0-0 imposible con tres
    votos y como máximo tres categorías: o hay mayoría de 2/3, o los tres
    difieren). Mayoría 2/3: `E` hereda esa categoría, confianza = máxima
    de las dos que coinciden. Los tres difieren: SIN DECISIÓN, declarado
    (no se elige arbitrariamente uno de los tres) -- se reporta el empate
    para que el scoring lo trate como corresponda (posible `INDECIDIBLE`,
    `ADV1-M3`), mismo criterio que la propuesta de dos corredores usaba
    para su caso de empate."""
    votos = [pred_L_solo, pred_L_corpus, pred_M]
    conteo: dict[str, list[PrediccionCorredor]] = {}
    for v in votos:
        conteo.setdefault(v.valor_categoria, []).append(v)

    moda_categoria, moda_votantes = max(conteo.items(), key=lambda kv: len(kv[1]))
    if len(moda_votantes) >= 2:
        conf = max((v.confianza_declarada or 0.0 for v in moda_votantes), default=0.0)
        return PrediccionCorredor(
            tipo_escala=pred_L_solo.tipo_escala,
            valor_categoria=moda_categoria,
            confianza_declarada=conf or None,
        )

    # Los tres difieren -- empate real, no se decide arbitrariamente.
    return PrediccionCorredor(
        tipo_escala=pred_L_solo.tipo_escala,
        valor_categoria=None,  # SIN DECISIÓN, declarado
        confianza_declarada=None,
    )


def combinar_E(
    pred_L_solo: PrediccionCorredor,
    pred_L_corpus: PrediccionCorredor,
    pred_M: PrediccionCorredor,
) -> PrediccionCorredor:
    """Punto de entrada único del corredor E. Enruta por tipo de escala.
    Definición SELLADA por `ADR-141` (ver docstring del módulo) -- ya no es
    sustituible sin volver a mesa, a diferencia de la PROPUESTA anterior."""
    if not (pred_L_solo.tipo_escala == pred_L_corpus.tipo_escala == pred_M.tipo_escala):
        raise ValueError("L-solo, L+corpus y M deben responder en la misma escala declarada por la spec de la celda.")
    if pred_L_solo.tipo_escala == "continua":
        return combinar_continua(pred_L_solo, pred_L_corpus, pred_M)
    return combinar_categorica(pred_L_solo, pred_L_corpus, pred_M)


if __name__ == "__main__":
    raise SystemExit(
        "corredor-E-combinacion-LM.py es spec de pre-registro (definición "
        "SELLADA del operador ⊕, ADR-141, ver mesa-pendientes.md §3), no se "
        "ejecuta en este acto (SELLA-OPLUS, NUBE, repo-only)."
    )
