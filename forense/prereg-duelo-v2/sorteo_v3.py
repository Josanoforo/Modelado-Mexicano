#!/usr/bin/env python3
"""Sorteo v3 — cierra la brecha prosa-vs-mecanismo de la regla 3 que
``FP-213``/``ADR-248`` encontró (``forense/prereg-duelo-v2/sorteo-marco-M-resultados-v1_1.md``,
sección «Hallazgo»).

``sorteo-act-pil-3-v2-PROPUESTA.md`` §2 («Reglas duras») dice, verbatim:

    3. Todo estrato con al menos una fila en `marco` recibe **al menos una**
    fila en `resultado` si `n_sorteo >= n_estratos_no_vacios` (asignación
    proporcional con piso 1, resto por remanente más grande — método de
    Hamilton/mayor resto); si `n_sorteo < n_estratos_no_vacios`, se sortea
    sin reposición **cuáles** estratos entran...

Pero ``sorteo_v2.asignar_asientos_proporcional`` (§2.2, el mecanismo que esa
misma regla 3 cita) implementa ``floor(cuota_exacta)`` puro + mayor-resto,
SIN piso 1 — matemáticamente puede dejar en cero a un estrato no vacío
(cuota exacta baja, pierde el desempate del remanente). No es un defecto de
código: el código coincide exacto con su propio pseudocódigo de §2.2: la
divergencia es entre la prosa de la regla 3 y el mecanismo que ella misma
nombra. Este módulo hace la letra de la regla 3 ejecutable.

``sorteo_v2.py`` NO se edita (`ADR-178`, sellado; `sorteo_v2.py` intacto,
verificado por este acto). Este archivo es sucesor, no reemplazo: reutiliza
de ``sorteo_v2.py`` todo lo que no cambia (``Fila``/``Skip``/``Exclusion``/
``ResultadoSorteo``, ``cargar_marco``, ``_agrupar_por_estrato``, ``_frac``,
``semilla_desde_sha_merge``) sin reimportar ni reinventar, y sólo sustituye
el reparto de asientos (``asignar_asientos_proporcional`` → función v3 de
abajo) y, por lo tanto, el cuerpo de ``sortear`` que la invoca — el resto
del pseudocódigo de §2.1 (fallback de infactibilidad §2.3, sorteo sin
reposición, presupuesto de cuota, postcondiciones) es idéntico línea a
línea a ``sorteo_v2.sortear``, con el fallback de infactibilidad recalculado
también bajo piso 1 (misma regla 3, aplicada consistente en cada punto de
reparto — no sólo en el reparto inicial).

Alcance declarado (ver LO QUE NO HACE al final): sólo cubre el caso
``n_sorteo >= n_estratos_no_vacios`` de la regla 3 (primera cláusula). La
segunda cláusula («si `n_sorteo < n_estratos_no_vacios`, se sortea sin
reposición cuáles estratos entran») NO está implementada — ningún acto la
ha necesitado todavía (ni B′, ni B″/v1_1); se declara ``NotImplementedError``
explícito si el caso se presenta, no una aproximación silenciosa.

Hallazgo adicional, verificado por cómputo en ``tests_sorteo_v3.py``
(``test_piso_uno_no_es_solo_un_parche_cuando_v2_ya_daba_al_menos_1``): "piso
1 + Hamilton sobre el resto" NO es un parche que sólo actúa cuando el
método puro (``asignar_asientos_proporcional``) deja a algún estrato en
cero — es un método de reparto distinto en general. Dar 1 asiento "gratis"
a cada estrato antes de repartir proporcionalmente el resto favorece
sistemáticamente a los estratos chicos frente al Hamilton puro, incluso en
casos donde el piso no estaba en riesgo (ej. cuotas 6.0/3.6/2.4 sobre
``n_sorteo=12``: v2 da 6/4/2, v3 da 5/4/3 — ningún estrato en cero bajo v2,
y aun así el reparto cambia). Se declara aquí porque cambia el resultado de
sorteos futuros más allá de los casos límite que motivaron este archivo —
mesa lo revisa en ``reglamento-sorteo-v1_1-PROPUESTA.md`` antes de sellar.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from random import Random

DIR = Path(__file__).resolve().parent

_SPEC = importlib.util.spec_from_file_location("sorteo_v2", DIR / "sorteo_v2.py")
_SORTEO_V2 = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _SORTEO_V2
_SPEC.loader.exec_module(_SORTEO_V2)

Fila = _SORTEO_V2.Fila
Skip = _SORTEO_V2.Skip
Exclusion = _SORTEO_V2.Exclusion
ResultadoSorteo = _SORTEO_V2.ResultadoSorteo
cargar_marco = _SORTEO_V2.cargar_marco
semilla_desde_sha_merge = _SORTEO_V2.semilla_desde_sha_merge
_agrupar_por_estrato = _SORTEO_V2._agrupar_por_estrato
_frac = _SORTEO_V2._frac


def asignar_asientos_proporcional_v3(estratos: dict[str, list], n_sorteo: int) -> dict[str, int]:
    """Regla 3 completa, primera cláusula: piso 1 por estrato no vacío,
    Hamilton/mayor-resto sobre `resto = n_sorteo - n_estratos_no_vacios`.

    Cada valor de `estratos` ya es no vacío por construcción de
    `_agrupar_por_estrato` (agrupa filas reales; no hay llave con lista
    vacía) — el piso 1 aplica a todas las llaves presentes, sin filtrar.
    """
    n_estratos = len(estratos)
    if n_sorteo < n_estratos:
        raise NotImplementedError(
            f"n_sorteo={n_sorteo} < n_estratos_no_vacios={n_estratos}: la regla 3 "
            "(sorteo-act-pil-3-v2-PROPUESTA.md Sec.2, segunda cláusula) exige sorteo "
            "sin reposición de qué estratos entran -- no implementado en sorteo_v3.py "
            "(ver LO QUE NO HACE del docstring del módulo), no aproximado en silencio."
        )

    asientos = {e: 1 for e in estratos}  # piso 1 por estrato no vacío
    resto = n_sorteo - n_estratos
    if resto == 0:
        return asientos

    total = sum(len(filas) for filas in estratos.values())
    cuota_exacta_resto = {e: resto * len(filas) / total for e, filas in estratos.items()}
    asientos_resto = {e: int(q) for e, q in cuota_exacta_resto.items()}  # floor
    restantes = resto - sum(asientos_resto.values())
    orden = sorted(estratos, key=lambda e: (-_frac(cuota_exacta_resto[e]), e))
    for e in orden[:restantes]:
        asientos_resto[e] += 1

    return {e: asientos[e] + asientos_resto[e] for e in estratos}


def sortear_v3(marco: list[Fila], n_sorteo: int, cuota_max: int, semilla: int) -> ResultadoSorteo:
    """Idéntico a ``sorteo_v2.sortear`` (§2.1) salvo la función de reparto de
    asientos (piso 1 + Hamilton sobre el resto, arriba) — usada tanto en el
    reparto inicial como en el fallback de infactibilidad de §2.3, para que
    la regla 3 se cumpla en cada punto donde se reparten asientos, no sólo
    en el primero."""
    estratos = _agrupar_por_estrato(marco)
    publicadas = {e: [f for f in filas if f.publicada == "SI"] for e, filas in estratos.items()}
    no_publicadas = {e: [f for f in filas if f.publicada == "NO"] for e, filas in estratos.items()}

    asientos = asignar_asientos_proporcional_v3(estratos, n_sorteo)

    infactibles = [e for e in estratos if asientos.get(e, 0) > 0 and len(no_publicadas[e]) == 0]
    estratos_excluidos: list[str] = []
    exclusiones: list[Exclusion] = []
    skips: list[Skip] = []

    if infactibles:
        factibles = [e for e in estratos if e not in infactibles]
        for e in infactibles:
            estratos_excluidos.append(e)
            exclusiones.append(
                Exclusion(estrato=e, asientos_liberados=asientos.get(e, 0))
            )  # ESTRATO EXCLUIDO POR INFACTIBILIDAD DE CUOTA -- no es una segunda clase de SKIP (§2 regla 3)
        n_realojar = sum(asientos.get(e, 0) for e in infactibles)
        for e in infactibles:
            asientos[e] = 0
        if factibles:
            estratos_factibles = {e: estratos[e] for e in factibles}
            asientos_factibles = asignar_asientos_proporcional_v3(
                estratos_factibles, n_realojar + sum(asientos[e] for e in factibles)
            )
            for e in factibles:
                asientos[e] = asientos_factibles[e]
        if not factibles and n_realojar > 0:
            raise RuntimeError("INFACTIBLE GLOBAL: todos los estratos con asiento son infactibles")

    rng = Random(semilla)
    resultado: list[Fila] = []

    orden_estable = sorted(estratos)

    for e in orden_estable:
        k = min(asientos.get(e, 0), len(no_publicadas[e]))
        elegidas = rng.sample(no_publicadas[e], k) if k else []
        resultado.extend(elegidas)
        asientos[e] = asientos.get(e, 0) - len(elegidas)

    presupuesto_publicadas = cuota_max
    for e in orden_estable:
        if asientos.get(e, 0) > 0:
            k = min(asientos[e], len(publicadas[e]), presupuesto_publicadas)
            elegidas = rng.sample(publicadas[e], k) if k else []
            resultado.extend(elegidas)
            presupuesto_publicadas -= len(elegidas)
            asientos[e] -= len(elegidas)
            if asientos[e] > 0:
                skips.append(
                    Skip(
                        estrato=e,
                        motivo="cuota global agotada o publicadas insuficientes",
                        faltan=asientos[e],
                    )
                )

    assert len(resultado) <= n_sorteo
    assert sum(1 for f in resultado if f.publicada == "SI") <= cuota_max

    return ResultadoSorteo(
        resultado=resultado,
        skips=skips,
        estratos_excluidos=estratos_excluidos,
        exclusiones=exclusiones,
    )


if __name__ == "__main__":
    raise SystemExit(
        "sorteo_v3.py no se ejecuta como CLI -- es un módulo de mecanismo,"
        " igual que sorteo_v2.py. Ver forense/notas/2026-09-01-sorteo-v3-regresion-v1_1.md"
        " para la regresión contra B' y el reporte informativo sobre la semilla de v1_1"
        " (ninguno de los dos escribe un sorteado nuevo)."
    )
