"""IC predictivo regional heredado; evaluación exclusivamente RETROSPECTIVA."""
from __future__ import annotations

import json
import math

Z = 1.959964
SERIES = {
    "ENVIPE": ((2023, 2024, 2025), ("HIST", "BASE", "HIST")),
    "ENCIG": ((2017, 2019, 2021, 2023, 2025),
              ("HIST", "HIST", "HIST", "BASE", "CONSUMIDORES")),
    "ENIF": ((2018, 2021, 2024), ("HIST", "HIST", "HIST")),
}


def _open(x):
    return isinstance(x, (float, int)) and math.isfinite(x) and 0 < x < 1


def _logit(x):
    return math.log(x / (1 - x))


def _expit(x):
    return 1 / (1 + math.exp(-x)) if x >= 0 else math.exp(x) / (1 + math.exp(x))


def _source(inputs, instrument, year, kind):
    raw = json.loads(open(inputs[f"FUENTE-{instrument}-{year}"]["ruta_absoluta"], encoding="utf-8").read())
    result = raw["resultados"]
    if kind == "CONSUMIDORES":
        rid = "RESULT-REGION-ENCIG-2025-adopta_encig2025_luz-JSON"
    else:
        rid = f"RESULT-REGION-{'HIST-' if kind == 'HIST' else ''}{instrument}-{year}-JSON"
    return {r["geografia"]: r for r in json.loads(result[rid])["filas"]}


def _eligible(row):
    return row["estado"] == "PUBLICABLE" and all(_open(row[k]) for k in ("punto", "ic_inf", "ic_sup")) and row["ic_inf"] <= row["punto"] <= row["ic_sup"]


def _tau(sources):
    """Media de medias de Δ² logit; peso igual por transición y geografía elegible."""
    means = []
    counts = []
    for a, b in zip(sources, sources[1:]):
        vals = [(_logit(b[g]["punto"]) - _logit(a[g]["punto"])) ** 2
                for g in a if _eligible(a[g]) and _eligible(b[g])]
        if vals:
            means.append(sum(vals) / len(vals))
            counts.append(len(vals))
    return (sum(means) / len(means) if means else None), counts


def _interval(row, tau):
    if tau is None or not _eligible(row):
        return None
    se = (_logit(row["ic_sup"]) - _logit(row["ic_inf"])) / (2 * Z)
    half = Z * math.sqrt(se * se + tau)
    return _expit(_logit(row["punto"]) - half), _expit(_logit(row["punto"]) + half)


def medir(inputs, contrato):
    if contrato["parametros"]["series"] != {k: list(v[0]) for k, v in SERIES.items()}:
        raise RuntimeError("calendario distinto del freeze")
    out = {}
    for instrument, (years, kinds) in SERIES.items():
        # El último RESULT no se abre hasta que tau e intervalos estén congelados.
        history = [_source(inputs, instrument, y, kind)
                   for y, kind in zip(years[:-1], kinds[:-1])]
        geos = set(history[0])
        if any(set(x) != geos for x in history):
            raise RuntimeError(f"geografías históricas incompatibles: {instrument}")
        tau, counts = _tau(history)
        floor = history[-1]
        intervals = {g: _interval(floor[g], tau) for g in sorted(geos)}
        observed = _source(inputs, instrument, years[-1], kinds[-1])
        if set(observed) != geos:
            raise RuntimeError(f"geografías observadas incompatibles: {instrument}")
        rows = []
        for g in sorted(geos):
            interval, obs = intervals[g], observed[g]
            comparable = interval is not None and obs["estado"] == "PUBLICABLE" and obs["punto"] is not None
            lo, hi = interval if interval else (None, None)
            row = {"geografia": g, "ola_piso": years[-2], "ola_observada": years[-1],
                   "piso_punto": floor[g]["punto"], "observado_punto": obs["punto"],
                   "ic_predictivo_inf": lo, "ic_predictivo_sup": hi,
                   "cubierta": int(lo <= obs["punto"] <= hi) if comparable else None,
                   "estado": "RETROSPECTIVA-COMPARABLE" if comparable else "SIN-COMPARABILIDAD"}
            rows.append(row)
            base = f"RESULT-REGION-ICP-{instrument}-{g}"
            out[base + "-IC-LO"] = lo
            out[base + "-IC-HI"] = hi
            out[base + "-CUBIERTA"] = row["cubierta"]
        prefix = f"RESULT-REGION-ICP-{instrument}"
        out[prefix + "-JSON"] = json.dumps({"filas": rows, "tau2": tau,
            "n_delta_por_transicion": counts, "transiciones_ajuste":
            [[a, b] for a, b in zip(years[:-2], years[1:-1])],
            "regla": "logit piso ± 1.959964*sqrt(ee_m^2+tau2)",
            "temporalidad": "RETROSPECTIVA"}, ensure_ascii=False, sort_keys=True,
            separators=(",", ":"))
        flags = [r["cubierta"] for r in rows if r["cubierta"] is not None]
        out[prefix + "-N-COMPARABLE"] = len(flags)
        out[prefix + "-N-CUBIERTA"] = sum(flags)
        out[prefix + "-TAU2"] = tau
    return out
