#!/usr/bin/env python3
"""Sorteo determinista de ``ACT-PIL-3``, implementación exacta de §2-§2.3 de
``forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md`` (reglamento
sellado por ``ADR-178``/``FP-150``).

Lee el congelado ``marco-congelado-piloto-v1_0.tsv`` (no el marco vivo — el
congelado es el compromiso). Universo elegible: ``grado_dependencia`` ∈
{P1, P2} con ``publicada`` ∈ {SI, NO} — 50 filas, verificado por ``assert``
contra el congelado en tiempo de carga.

La semilla no se deriva ni se corre el PRNG en ``ACTO A`` — este módulo solo
se importa y se prueba contra los casos de §5 (``tests_sorteo_v2.py``). El
sorteo real corre en ``ACTO B``, después de fusionar, con
``semilla = derivar_seed_scope(int(sha256(SHA_A_hex).hexdigest(), 16) % 2**63, "ACT-PIL-3-v1")``
(§3.2: reutiliza ``derivar_seed_scope`` de ``scoring-adv1-m3.py:685``, no
reinventa el hash).

PRNG: ``random.Random(semilla)`` de la librería estándar, no
``numpy.random.Generator(PCG64(...))`` — el reglamento cita PCG64 como
ejemplo ("p.ej."), no como mandato, y numpy no está disponible en este
entorno. ``random.Random`` es determinista por semilla entera y su método
``sample`` es sorteo sin reposición, que es la propiedad que §2 regla 4
exige; se documenta aquí porque es una elección, no una casualidad.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from dataclasses import dataclass, field
from pathlib import Path
from random import Random
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONGELADO = Path(__file__).resolve().parent / "marco-congelado-piloto-v1_0.tsv"

_RUTA_SCORING = ROOT / "forense" / "prereg-duelo-v2" / "scoring-adv1-m3.py"
_SPEC = importlib.util.spec_from_file_location("scoring_adv1_m3", _RUTA_SCORING)
_SCORING = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _SCORING
_SPEC.loader.exec_module(_SCORING)
derivar_seed_scope = _SCORING.derivar_seed_scope

GRADOS_ELEGIBLES = ("P1", "P2")
PUBLICADA_ELEGIBLE = ("SI", "NO")


@dataclass
class Fila:
    id: str
    estrato: str
    publicada: str  # "SI" o "NO"


@dataclass
class Skip:
    estrato: str
    motivo: str
    faltan: int


@dataclass
class Exclusion:
    estrato: str
    asientos_liberados: int


@dataclass
class ResultadoSorteo:
    resultado: list[Fila] = field(default_factory=list)
    skips: list[Skip] = field(default_factory=list)
    estratos_excluidos: list[str] = field(default_factory=list)
    exclusiones: list[Exclusion] = field(default_factory=list)


def _publicada_de(celda: str) -> str:
    """La columna ``publicada`` del marco trae anotaciones largas tras ``::``
    o espacio; solo el primer token (``SI``/``NO``/``PENDIENTE-...``) importa."""
    return celda.split(None, 1)[0].split("::", 1)[0].strip()


def cargar_marco(ruta: Path = CONGELADO) -> list[Fila]:
    with ruta.open(encoding="utf-8", newline="") as fh:
        lector = csv.DictReader(fh, delimiter="\t")
        filas = []
        for renglon in lector:
            grado = renglon["grado_dependencia"].strip()
            if grado not in GRADOS_ELEGIBLES:
                continue
            pub = _publicada_de(renglon["publicada"])
            if pub not in PUBLICADA_ELEGIBLE:
                continue
            filas.append(Fila(id=renglon["id"], estrato=renglon["estrato"].strip(), publicada=pub))
    filas.sort(key=lambda f: f.id)
    assert len(filas) == 50, f"universo elegible (P1/P2, SI/NO) = {len(filas)}, se esperaban 50"
    return filas


def _agrupar_por_estrato(marco: list[Fila]) -> dict[str, list[Fila]]:
    estratos: dict[str, list[Fila]] = {}
    for fila in marco:
        estratos.setdefault(fila.estrato, []).append(fila)
    return estratos


def _frac(x: float) -> float:
    return x - int(x)


def asignar_asientos_proporcional(estratos: dict[str, list[Fila]], n_sorteo: int) -> dict[str, int]:
    total = sum(len(filas) for filas in estratos.values())
    cuota_exacta = {e: n_sorteo * len(filas) / total for e, filas in estratos.items()}
    asientos = {e: int(q) for e, q in cuota_exacta.items()}  # floor (q >= 0)
    restantes = n_sorteo - sum(asientos.values())
    orden = sorted(estratos, key=lambda e: (-_frac(cuota_exacta[e]), e))
    for e in orden[:restantes]:
        asientos[e] += 1
    return asientos


def sortear(marco: list[Fila], n_sorteo: int, cuota_max: int, semilla: int) -> ResultadoSorteo:
    estratos = _agrupar_por_estrato(marco)
    publicadas = {e: [f for f in filas if f.publicada == "SI"] for e, filas in estratos.items()}
    no_publicadas = {e: [f for f in filas if f.publicada == "NO"] for e, filas in estratos.items()}

    asientos = asignar_asientos_proporcional(estratos, n_sorteo)

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
            asientos_factibles = asignar_asientos_proporcional(estratos_factibles, n_realojar + sum(asientos[e] for e in factibles))
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


def semilla_desde_sha_merge(sha_merge_hex: str, scope_id: str = "ACT-PIL-3-v1") -> int:
    """§3.2: semilla = derivar_seed_scope(int(sha256(SHA_A_hex).hexdigest(), 16) % 2**63, scope_id)."""
    import hashlib

    base = int(hashlib.sha256(sha_merge_hex.encode("utf-8")).hexdigest(), 16) % (2**63)
    return derivar_seed_scope(base, scope_id)


if __name__ == "__main__":
    raise SystemExit(
        "sorteo_v2.py no se ejecuta como CLI en ACTO A -- el PRNG no corre hasta que exista"
        " el SHA de merge (ver §3 del reglamento y forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md)."
    )
