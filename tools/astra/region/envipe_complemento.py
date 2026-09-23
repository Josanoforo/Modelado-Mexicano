"""Complemento regional ENVIPE desde RESULT sellados, sin microdatos."""
from __future__ import annotations

import json

OLAS = (2023, 2024, 2025)


def complemento(fila):
    n = fila["n"]
    out = dict(fila)
    out["n_numerador"] = n - fila["n_numerador"]
    if fila["estado"] == "PUBLICABLE":
        p, lo, hi = fila["punto"], fila["ic_inf"], fila["ic_sup"]
        if p is None or lo is None or hi is None:
            raise RuntimeError("fuente PUBLICABLE sin estimación")
        out.update(punto=1-p, ic_inf=1-hi, ic_sup=1-lo,
                   replicas_p=[1-x for x in fila["replicas_p"]])
    else:
        if any(fila[k] is not None for k in ("punto", "ic_inf", "ic_sup", "replicas_p")):
            raise RuntimeError("fuente suprimida expone cifra")
    return out


def medir(inputs, contrato):
    if tuple(contrato["parametros"]["olas"]) != OLAS:
        raise RuntimeError("olas distintas de la spec")
    resultados = {}
    for ola in OLAS:
        src = json.loads(open(inputs[f"FUENTE-{ola}"]["ruta_absoluta"], encoding="utf-8").read())["resultados"]
        pref0 = (f"RESULT-REGION-ENVIPE-{ola}" if ola == 2024 else
                 f"RESULT-REGION-HIST-ENVIPE-{ola}")
        fuente = json.loads(src[pref0 + "-JSON"])
        filas = [complemento(f) for f in fuente["filas"]]
        pref = f"RESULT-REGION-ENVIPE-CUMPLE-{ola}"
        resultados[pref + "-JSON"] = json.dumps({"filas": filas, "diseno": fuente["diseno"],
                                                 "derivacion": "1-p; IC invertido; réplicas 1-r"},
                                                ensure_ascii=False, sort_keys=True,
                                                separators=(",", ":"))
        for fila in filas:
            base = pref + "-" + fila["geografia"]
            resultados.update({base + "-P": fila["punto"],
                               base + "-IC-LO": fila["ic_inf"],
                               base + "-IC-HI": fila["ic_sup"],
                               base + "-N": fila["n"],
                               base + "-ESTADO": fila["estado"],
                               base + "-N-EFECTIVO-KISH": fila["n_efectivo_kish"]})
    return resultados
