#!/usr/bin/env python3
"""tools/agrega_l_v1_0.py -- agregador reusable de lecturas L (campo LLM).

Nace en `ACTO GEN2-L-DESDE-CAPTURAS-1` (21/sep/2026). P5 del encargo: el
lote ENIF 2024 y los duelos ENVIPE/ENIGH necesitan UN agregador probado,
no tres. Este módulo es ese UNO: dado el conjunto de (estado, valor) por
réplica de una celda x variante -- ya extraído de sus capturas -- produce
la mediana, su dispersión entre repeticiones (MAD: mediana de las
desviaciones absolutas a la mediana) y un intervalo bootstrap (percentil)
de la mediana.

No abre archivos y no decide la regla de inválidas: la regla de qué cuenta
como VALIDA / ABSTENCION / MALFORMADA / ERROR_TECNICO es la sellada en
`forense/prereg-duelo-v2/F5-completa-spec-v1_0.md` §4 (10/sep/2026, ANTES
de las 224 capturas que este acto mide) y vive en
`tools/calcula_f5_completa.py::extraer`. Este módulo la importa -- no la
copia -- para que la regla de inválidas tenga una sola fuente (D-15: ningún
parámetro vive en dos sitios). Agregar la regla de vuelta después de
contar las réplicas es el PARO (d) del encargo que nace este módulo.

Uso:
    from agrega_l_v1_0 import agregar_celda, extraer_replicas

    estados = [extraer(captura.get("texto_crudo"), captura.get("estado_captura"))
               for captura in capturas_de_una_celda_y_variante]
    r = agregar_celda(estados, n_programadas=len(capturas_de_una_celda_y_variante))
    r.mediana, r.dispersion_mad, r.ic_lo, r.ic_hi
"""
from __future__ import annotations

import random
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

_TOOLS_DIR = Path(__file__).resolve().parent
if str(_TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(_TOOLS_DIR))

from calcula_f5_completa import extraer  # noqa: E402  -- regla sellada, una sola fuente

BOOTSTRAP_N_DEFAULT = 10_000
BOOTSTRAP_SEED_DEFAULT = 42
NIVEL_IC_DEFAULT = 0.95

__all__ = ["extraer", "agregar_celda", "ResultadoCelda",
           "BOOTSTRAP_N_DEFAULT", "BOOTSTRAP_SEED_DEFAULT", "NIVEL_IC_DEFAULT"]


def _percentil(valores: list[float], q: float) -> float:
    if not valores:
        raise ValueError("percentil de lista vacía")
    xs = sorted(valores)
    pos = (len(xs) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


@dataclass(frozen=True)
class ResultadoCelda:
    n_programadas: int
    n_ejecutadas: int
    n_validas: int
    n_abstenciones: int
    n_malformadas: int
    n_errores_tecnicos: int
    valores: tuple
    mediana: float | None
    dispersion_mad: float | None
    ic_lo: float | None
    ic_hi: float | None
    bootstrap_replicas: int
    bootstrap_seed: int


def agregar_celda(
    estados_valores: Iterable[tuple],
    *,
    n_programadas: int,
    bootstrap_n: int = BOOTSTRAP_N_DEFAULT,
    bootstrap_seed: int = BOOTSTRAP_SEED_DEFAULT,
    nivel_ic: float = NIVEL_IC_DEFAULT,
) -> ResultadoCelda:
    """Agrega las réplicas de UNA celda x variante ya extraídas.

    `estados_valores` es una lista de tuplas `(estado, valor)` -- el
    resultado de `extraer(...)` sobre cada captura de esa celda/variante,
    más `("PENDIENTE", None)` por cada réplica programada sin archivo. No
    abre nada: quien llama decide de dónde vienen las capturas (esto
    mantiene el módulo agnóstico del duelo: F5, ENIF, ENVIPE o ENIGH).

    Ramas terminales declaradas por P2 (D-22 ampliada, oro sobre
    sintético): todas las réplicas inválidas -> mediana/dispersión/IC en
    `None`, con los conteos intactos; una sola réplica válida -> mediana =
    ese valor, dispersión = 0.0, IC degenerado (`ic_lo == ic_hi ==
    mediana`) -- un intervalo de un solo punto no es indeterminación, es
    el intervalo real de una muestra de tamaño 1, y se declara así.
    """
    ev = list(estados_valores)
    n_ejecutadas = sum(1 for e, _ in ev if e != "PENDIENTE")
    n_abstenciones = sum(1 for e, _ in ev if e == "ABSTENCION")
    n_malformadas = sum(1 for e, _ in ev if e == "MALFORMADA")
    n_errores = sum(1 for e, _ in ev if e == "ERROR_TECNICO")
    valores = tuple(v for e, v in ev if e == "VALIDA" and v is not None)

    if not valores:
        return ResultadoCelda(n_programadas, n_ejecutadas, 0, n_abstenciones,
                               n_malformadas, n_errores, valores, None, None,
                               None, None, bootstrap_n, bootstrap_seed)

    mediana = statistics.median(valores)

    if len(valores) == 1:
        return ResultadoCelda(n_programadas, n_ejecutadas, 1, n_abstenciones,
                               n_malformadas, n_errores, valores, mediana, 0.0,
                               mediana, mediana, bootstrap_n, bootstrap_seed)

    dispersion_mad = statistics.median(abs(v - mediana) for v in valores)

    rng = random.Random(bootstrap_seed)
    n = len(valores)
    medianas_boot = []
    for _ in range(bootstrap_n):
        muestra = [valores[rng.randrange(n)] for _ in range(n)]
        medianas_boot.append(statistics.median(muestra))
    cola = (1.0 - nivel_ic) / 2.0
    ic_lo = _percentil(medianas_boot, cola)
    ic_hi = _percentil(medianas_boot, 1.0 - cola)

    return ResultadoCelda(n_programadas, n_ejecutadas, len(valores), n_abstenciones,
                           n_malformadas, n_errores, valores, mediana, dispersion_mad,
                           ic_lo, ic_hi, bootstrap_n, bootstrap_seed)
