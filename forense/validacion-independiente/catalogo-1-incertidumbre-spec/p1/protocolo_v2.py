"""Sucesor del auxiliar sintético: limita cardinalidad antes de enumerar.

Conserva protocolo.py y su congelación inicial. No cambia el diseño inferencial.
"""
from collections import Counter
from itertools import product

from protocolo import SEED, prepare, publicable, reference

MAX_DRAWS = 100000


def exact_law(frame, contributions):
    _, values, strata = prepare(frame, contributions)
    cardinality = 1
    for group in strata:
        # Enteros Python; corte temprano incluso antes de calcular n_h ** n_h.
        for _ in group:
            cardinality *= len(group)
            if cardinality > MAX_DRAWS:
                raise ValueError('solo sintéticos pequeños')

    counts = Counter()
    # Cada posición del sorteo recorre las UPM de su estrato. product recibe
    # solo los grupos pequeños, nunca un iterable de n_h ** n_h tuplas.
    positions = [group for group in strata for _ in group]
    for idx in product(*positions):
        n, d = values[list(idx)].sum(axis=0)
        counts[float(n / d) if d > 0 else 'NO-ESTIMABLE'] += 1
    assert sum(counts.values()) == cardinality
    return {key: count / cardinality for key, count in counts.items()}
