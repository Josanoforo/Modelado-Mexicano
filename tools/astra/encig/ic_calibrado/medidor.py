"""Intervalo de persistencia ENCIG; el primer resultado se reporta.

Sólo consume RESULT sellados de 2017, 2019, 2021 y el piso 2023.
La secuencia dentro de ``medir`` impide usar 2023 al construir la regla de
evaluación retrospectiva. No abre 2025 ni microdatos de ninguna ola.
"""
from __future__ import annotations

import csv
import io
import json
import math
from collections import defaultdict

Z = 1.959964
PREF = "RESULT-ENCIGPIC"
YEARS = (2017, 2019, 2021, 2023)
TRAIN_PAIRS = ((2017, 2019), (2019, 2021))
FINAL_PAIRS = TRAIN_PAIRS + ((2021, 2023),)
AXES = ("SEXO", "EDAD", "ESCOLARIDAD")
CATS = {
    "SEXO": ("1", "2"),
    "EDAD": ("18-29", "30-44", "45-59", "60-MAS"),
    "ESCOLARIDAD": ("HASTA-PRIMARIA", "SECUNDARIA", "MEDIA-SUPERIOR", "SUPERIOR"),
}
SRC_SHA = {
    2017: "9bbe13c04dc7273d0253a23a63db8e07c1f28022483af9332a357a4a1ebcc340",
    2019: "3e4d5bda11dcfba16013a16a42edb3ebc8149d022e98abb00c9d19f916db9bf0",
    2021: "0db4eda8ad7754e7432a8f23e9e41f5d7c575bcf8fed203e1da69357173f4b53",
    2023: "bd13a97b01f2d1251c54ddd3ff8c2d1ab5d16f68bc77f2b4041c1b617ee78568",
}
TABLE_SHA = "1715da9303957dac11146bd14e5498d11c554671edcdfb9c6ea7230845433a95"
COMP_SHA = "0f8a718050f42d09c6694baa2deecba58d03e5f298f50f280d2e6542aac965aa"


def _bytes(ent):
    b = ent.get("bytes")
    if b is not None:
        return b
    from pathlib import Path
    return Path(ent["ruta_absoluta"]).read_bytes()


def _load(ent):
    return json.loads(_bytes(ent).decode("utf-8"))["resultados"]


def _finite_open(x):
    return isinstance(x, (int, float)) and math.isfinite(x) and 0 < x < 1


def _logit(x):
    return math.log(x / (1 - x))


def _expit(x):
    if x >= 0:
        return 1 / (1 + math.exp(-x))
    y = math.exp(x)
    return y / (1 + y)


def _wilson(k, n):
    if not n:
        return None, None
    p = k / n
    den = 1 + Z * Z / n
    mid = (p + Z * Z / (2 * n)) / den
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / den
    return mid - half, mid + half


def _interval(source, stem, tau):
    p, lo, hi = (source.get(stem + suffix) for suffix in ("-P", "-IC-LO", "-IC-HI"))
    if tau is None or not all(_finite_open(x) for x in (p, lo, hi)) or lo > hi:
        return None
    ee = (_logit(hi) - _logit(lo)) / (2 * Z)
    half = Z * math.sqrt(ee * ee + tau)
    return _expit(_logit(p) - half), _expit(_logit(p) + half)


def _tau(series, cells, pairs):
    """Equal weight to transitions; equal weight to eligible cells within each."""
    by_axis = defaultdict(list)
    for axis, cat in cells:
        by_axis[axis].append(cat)
    result = {}
    counts = {}
    for axis in AXES:
        transition_means = []
        total = 0
        for start, end in pairs:
            sq = []
            for cat in by_axis[axis]:
                stem_a = f"RESULT-ENCIG-SERIE-{start}-DIGITAL-{axis}-{cat}-P"
                stem_b = f"RESULT-ENCIG-SERIE-{end}-DIGITAL-{axis}-{cat}-P"
                # The 2023 series is supplied by the adjudicated floor with a different stem.
                if end == 2023:
                    stem_b = f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{axis}-{cat}-P"
                a, b = series[start].get(stem_a), series[end].get(stem_b)
                if _finite_open(a) and _finite_open(b):
                    sq.append((_logit(b) - _logit(a)) ** 2)
            if sq:
                transition_means.append(sum(sq) / len(sq))
                total += len(sq)
        result[axis] = sum(transition_means) / len(transition_means) if transition_means else None
        counts[axis] = total
    return result, counts


def _cells_from_identity(ent):
    rows = list(csv.DictReader(io.StringIO(_bytes(ent).decode("utf-8")), delimiter="\t"))
    cells = [(r["axis"].upper(), r["cell_id"].removeprefix("RESULT-PISOS-ENCIG2023-V2-DIGITAL-").removesuffix("-P"))
             for r in rows if r["source_instrument"] == "ENCIG" and r["status"] == "CONSTRUIBLE"]
    parsed = []
    for axis, tail in cells:
        prefix = axis + "-"
        if not tail.startswith(prefix):
            raise RuntimeError(f"identidad de celda inesperada: {tail}")
        parsed.append((axis, tail[len(prefix):]))
    expected = [(axis, cat) for axis in AXES for cat in CATS[axis]]
    if parsed != expected:
        raise RuntimeError(f"rejilla ENCIG distinta: {parsed}")
    return parsed


def _check_comparability(ent):
    rows = list(csv.DictReader(io.StringIO(_bytes(ent).decode("utf-8")), delimiter="\t"))
    verdict = {r["ola"]: r["veredicto"] for r in rows if r["conducta"] == "C-LUZ-DIGITAL" and r["ola"] in ("2017", "2019", "2021", "2023")}
    expected = {"2017": "MISMO-INSTRUMENTO", "2019": "MISMO-INSTRUMENTO",
                "2021": "MISMO-INSTRUMENTO", "2023": "CAMBIO-MENOR"}
    if verdict != expected:
        raise RuntimeError(f"comparabilidad documental difiere del freeze: {verdict}")


def medir(inputs, contrato):
    _check_comparability(inputs["ENCIG-COMPARABILIDAD-TEXTO"])
    cells = _cells_from_identity(inputs["PISOS-REJILLA-METADATOS"])
    series = {year: _load(inputs[f"RESULT-ENCIG-{year}"]) for year in YEARS[:3]}
    # First lock training tau and the 2021 intervals. No 2023 input has been read.
    train_tau, train_n = _tau(series, cells, TRAIN_PAIRS)
    frozen_eval = {}
    for axis, cat in cells:
        stem = f"RESULT-ENCIG-SERIE-2021-DIGITAL-{axis}-{cat}"
        frozen_eval[(axis, cat)] = _interval(series[2021], stem, train_tau[axis])

    # Evaluation point is opened only after the training rule and intervals exist.
    series[2023] = _load(inputs["RESULT-ENCIG-2023-PISO"])
    final_tau, final_n = _tau(series, cells, FINAL_PAIRS)
    out = {}
    for axis in AXES:
        base = f"{PREF}-DIGITAL-{axis}"
        out[base + "-TAU2-TRAIN"] = train_tau[axis]
        out[base + "-TAU2-FINAL"] = final_tau[axis]
        out[base + "-N-DELTA-TRAIN"] = train_n[axis]
        out[base + "-N-DELTA-FINAL"] = final_n[axis]
    covered_by_axis = defaultdict(list)
    widths_eval, widths_final, minimums = [], [], []
    n_noncal = 0
    for axis, cat in cells:
        base = f"{PREF}-DIGITAL-{axis}-{cat}"
        floor = f"RESULT-PISOS-ENCIG2023-V2-DIGITAL-{axis}-{cat}"
        eval_ic = frozen_eval[(axis, cat)]
        final_ic = _interval(series[2023], floor, final_tau[axis])
        point23 = series[2023].get(floor + "-P")
        point21 = series[2021].get(f"RESULT-ENCIG-SERIE-2021-DIGITAL-{axis}-{cat}-P")
        eligible = eval_ic is not None and isinstance(point23, (int, float)) and 0 <= point23 <= 1
        covered = int(eval_ic[0] <= point23 <= eval_ic[1]) if eligible else None
        width_eval = 100 * (eval_ic[1] - eval_ic[0]) if eligible else None
        width_final = 100 * (final_ic[1] - final_ic[0]) if final_ic else None
        # Symmetric interval in probability units, clipped to [0,1].
        if eligible and _finite_open(point21):
            distance = abs(point23 - point21)
            min_width = 100 * (min(1.0, point21 + distance) - max(0.0, point21 - distance))
        else:
            min_width = None
        out.update({base + "-EVAL-IC-LO": eval_ic[0] if eligible else None,
                    base + "-EVAL-IC-HI": eval_ic[1] if eligible else None,
                    base + "-EVAL-CUBIERTA": covered,
                    base + "-EVAL-ANCHO-PP": width_eval,
                    base + "-EVAL-ANCHO-MIN-SIM-PP": min_width,
                    base + "-FINAL-IC-LO": final_ic[0] if final_ic else None,
                    base + "-FINAL-IC-HI": final_ic[1] if final_ic else None,
                    base + "-FINAL-ANCHO-PP": width_final})
        if eligible:
            covered_by_axis[axis].append(covered)
            widths_eval.append(width_eval)
            minimums.append(min_width)
        else:
            n_noncal += 1
        if width_final is not None:
            widths_final.append(width_final)
    all_flags = [x for flags in covered_by_axis.values() for x in flags]
    n, k = len(all_flags), sum(all_flags)
    wilson = _wilson(k, n)
    out.update({PREF + "-N-ELEGIBLES": n, PREF + "-N-CUBIERTAS": k,
                PREF + "-N-NO-CALIBRABLES": n_noncal,
                PREF + "-COBERTURA": k / n if n else None,
                PREF + "-WILSON-LO": wilson[0], PREF + "-WILSON-HI": wilson[1],
                PREF + "-ROTULO": "RETROSPECTIVA; Wilson por celda sólo referencia; tres grupos dependientes no bastan para bootstrap fiable"})
    for axis in AXES:
        flags = covered_by_axis[axis]
        base = f"{PREF}-DIGITAL-{axis}"
        out[base + "-N-ELEGIBLES"] = len(flags)
        out[base + "-N-CUBIERTAS"] = sum(flags)
        out[base + "-COBERTURA"] = sum(flags) / len(flags) if flags else None
    import statistics
    for tag, vals in (("EVAL", widths_eval), ("FINAL", widths_final), ("MIN-SIM", minimums)):
        out[PREF + f"-{tag}-ANCHO-MEDIANA-PP"] = statistics.median(vals) if vals else None
        out[PREF + f"-{tag}-ANCHO-MIN-PP"] = min(vals) if vals else None
        out[PREF + f"-{tag}-ANCHO-MAX-PP"] = max(vals) if vals else None
    return out
