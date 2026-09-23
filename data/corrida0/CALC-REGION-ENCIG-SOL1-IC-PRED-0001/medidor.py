"""IC predictivo retrospectivo ENCIG SOL1, ajuste 2021→23, evaluación 2025."""
from __future__ import annotations

import json

from tools.astra.region.ic_calibrado import _tau, _interval


def _load(inputs, name, rid):
    r = json.loads(open(inputs[name]["ruta_absoluta"], encoding="utf-8").read())["resultados"]
    return {f["geografia"]: f for f in json.loads(r[rid])["filas"]}


def medir(inputs, contrato):
    if contrato["parametros"]["calendario"] != [2021, 2023, 2025]:
        raise RuntimeError("calendario distinto de la spec")
    a = _load(inputs, "FUENTE-2021", "RESULT-REGION-ENCIG-SOL1-2021-JSON")
    b = _load(inputs, "FUENTE-2023", "RESULT-REGION-ENCIG-SOL1-2023-JSON")
    if set(a) != set(b) or len(a) != 32:
        raise RuntimeError("geografías históricas distintas")
    tau, counts = _tau([a, b])
    frozen = {g: _interval(b[g], tau) for g in sorted(a)}
    # La evaluación se abre después de fijar tau y los 32 intervalos.
    c = _load(inputs, "FUENTE-2025", "RESULT-REGION-ENCIG-2025-paga_mordida_encig2025-JSON")
    if set(c) != set(a):
        raise RuntimeError("geografías de evaluación distintas")
    rows = []
    out = {}
    for g in sorted(a):
        interval = frozen[g]
        comparable = interval is not None and c[g]["estado"] == "PUBLICABLE" and c[g]["punto"] is not None
        lo, hi = interval if interval else (None, None)
        covered = int(lo <= c[g]["punto"] <= hi) if comparable else None
        rows.append({"geografia": g, "ola_piso": 2023, "ola_observada": 2025,
                     "piso_punto": b[g]["punto"], "observado_punto": c[g]["punto"],
                     "ic_predictivo_inf": lo, "ic_predictivo_sup": hi,
                     "cubierta": covered,
                     "estado": "RETROSPECTIVA-COMPARABLE" if comparable else "SIN-COMPARABILIDAD"})
        base = f"RESULT-REGION-ENCIG-SOL1-ICP-{g}"
        out.update({base + "-IC-LO": lo, base + "-IC-HI": hi,
                    base + "-CUBIERTA": covered})
    pref = "RESULT-REGION-ENCIG-SOL1-ICP"
    out[pref + "-JSON"] = json.dumps({"filas": rows, "tau2": tau,
        "n_delta_por_transicion": counts, "transiciones_ajuste": [[2021, 2023]],
        "regla": "logit piso ± 1.959964*sqrt(ee_m^2+tau2)",
        "temporalidad": "RETROSPECTIVA"}, ensure_ascii=False, sort_keys=True,
        separators=(",", ":"))
    flags = [r["cubierta"] for r in rows if r["cubierta"] is not None]
    out[pref + "-TAU2"] = tau
    out[pref + "-N-COMPARABLE"] = len(flags)
    out[pref + "-N-CUBIERTA"] = sum(flags)
    return out
