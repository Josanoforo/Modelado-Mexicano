"""Evaluación retrospectiva de persistencia trimestral, sin datos individuales."""
from __future__ import annotations

import json
from collections import defaultdict


def _t(ola):
    return int(ola[:4]) * 4 + int(ola[-1]) - 1


def derivar(filas):
    grupos = defaultdict(list)
    for f in filas:
        if f["conducta"] == "ingreso_ocupado_nominal":
            continue  # pesos corrientes no son comparables entre olas
        grupos[(f["era"], f["conducta"], f["eje"], f["segmento"])].append(f)
    salida = []
    for (era, conducta, eje, segmento), serie in sorted(grupos.items()):
        serie.sort(key=lambda f: _t(f["ola"]))
        for i in range(1, len(serie)):
            piso, destino = serie[i - 1], serie[i]
            if _t(destino["ola"]) - _t(piso["ola"]) != 1:
                continue
            if piso["punto"] is None or destino["punto"] is None:
                continue
            tendencia = None
            if i >= 2 and _t(piso["ola"]) - _t(serie[i - 2]["ola"]) == 1:
                anterior = serie[i - 2]["punto"]
                if anterior is not None:
                    tendencia = 2 * piso["punto"] - anterior
                    if piso["unidad"] == "proporcion":
                        tendencia = min(1.0, max(0.0, tendencia))
            salida.append({
                "era": era, "conducta": conducta, "eje": eje, "segmento": segmento,
                "ola_origen": piso["ola"], "ola_destino": destino["ola"],
                "unidad": piso["unidad"], "piso": piso["punto"],
                "ic_diseno_piso_lo": piso["ic95_lo"],
                "ic_diseno_piso_hi": piso["ic95_hi"],
                "destino": destino["punto"],
                "error_persistencia": destino["punto"] - piso["punto"],
                "error_abs_persistencia": abs(destino["punto"] - piso["punto"]),
                "piso_ic_contiene_destino": (piso["ic95_lo"] <= destino["punto"] <= piso["ic95_hi"]
                                              if piso["ic95_lo"] is not None and
                                              piso["ic95_hi"] is not None else None),
                "pronostico_tendencia": tendencia,
                "error_abs_tendencia": (abs(destino["punto"] - tendencia)
                                         if tendencia is not None else None),
                "ic_predictivo": None,
                "calibracion": "SIN-COVARIANZA-LONGITUDINAL-PARA-CALIBRAR",
            })
    return salida


def medir(inputs, contrato):
    registro = json.loads(inputs["IN-ENOE-PISOS-RESULT"]["bytes"].decode())
    filas = json.loads(registro["resultados"]["RESULT-ENOE-PISOS-TABLA"])
    salida = derivar(filas)
    return {
        "RESULT-ENOE-PERSISTENCIA-TABLA": json.dumps(salida, ensure_ascii=False,
                                                       sort_keys=True, separators=(",", ":")),
        "RESULT-ENOE-PERSISTENCIA-PARES": len(salida),
        "RESULT-ENOE-PERSISTENCIA-SIN-IC-PREDICTIVO": len(salida),
    }
