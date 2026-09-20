"""`CALC-C2-COMPUESTO-RESERVADAS-0001` — C2 compuesto sobre los cruces
`RESERVADA` del marcador de segmento.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ACTO GEN2-C2-COMPUESTO-RESERVADAS-1 · 19/sep/2026.
Spec congelada: `forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md`
(COMMIT-1, anterior a esta corrida).

CERO MICRODATO. Todos los `inputs` son `origen: repo`: marginales ya
sellados y publicados por el árbitro. Este medidor no abre ningún payload
de ninguna ola, no deriva ni mira `R` de ningún cruce, y no adopta nada.

LA FORMA NO SE REINVENTA. `tools/c2_compuesto.py` importa
`tests/test_celda_d_c2.py::piso_log_aditivo` — la función de referencia
que los dos CALC ya sellados citan — y este medidor la usa a través de él.
De ahí heredan las dos guardias que no se relajan: mismo `desenlace_id` en
los tres marginales, y rechazo explícito de `p ∈ {0,1}` (SIN-DEFINIR, sin
recorte y sin sustitución).

LA INCERTIDUMBRE NO SE FABRICA. Los marginales de una misma ola salen de
la misma muestra y su covarianza no está sellada: cero IC. El rango
`DIAG-*` es diagnóstico, no intervalo de confianza (spec §5).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[3]
for _p in (str(_RAIZ), str(_RAIZ / "tools")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import c2_compuesto as C2  # noqa: E402


def medir(inputs, contrato):
    p = contrato["parametros"]
    out: dict[str, object] = {}

    dictamen = C2.dictamen()
    emisiones = C2.emisiones()

    # ── el dictamen, como número y no como prosa ───────────────────────
    pares = {d["celda_id_marcador"] for d in dictamen}
    emitibles = [d for d in dictamen if d["veredicto"] == "EMITIBLE"]
    out["RESULT-C2COMP-N-PARES-RESERVADA-EXAMINADOS"] = len(pares)
    out["RESULT-C2COMP-N-FILAS-DICTAMEN"] = len(dictamen)
    out["RESULT-C2COMP-N-FILAS-EMITIBLES"] = len(emitibles)
    out["RESULT-C2COMP-N-FILAS-NO-EMITIBLES"] = len(dictamen) - len(emitibles)
    out["RESULT-C2COMP-N-PARES-EMITIBLES"] = len(
        {d["celda_id_marcador"] for d in emitibles})
    out["RESULT-C2COMP-N-PARES-NO-EMITIBLES-EN-NINGUN-DESENLACE"] = len(
        pares - {d["celda_id_marcador"] for d in emitibles})
    out["RESULT-C2COMP-N-CELDAS-EMITIDAS"] = len(emisiones)
    out["RESULT-C2COMP-N-CELDAS-CON-IC"] = sum(
        1 for f in emisiones if f["ic95_inf"] != "" or f["ic95_sup"] != "")
    out["RESULT-C2COMP-TIPO-INCERTIDUMBRE"] = p["tipo_incertidumbre"]
    out["RESULT-C2COMP-SUPUESTO"] = p["supuesto"]
    out["RESULT-C2COMP-ESTADO-DE-EMISION"] = p["estado_de_emision"]

    # ── control de reproducción contra el C2 YA SELLADO (spec §7) ──────
    # El par `localidad × edad` de ENIF ya fue piloteado -- por eso NO
    # está en la lista RESERVADA -- y sus ocho puntos C2 están sellados.
    # Rama negativa explícita: NO-REPRODUCE con el delta con signo, sin
    # ajustar nada.
    sellados = json.loads(
        Path(inputs[p["input_control"]]["ruta_absoluta"]).read_text(
            encoding="utf-8"))["resultados"]
    marg = p["marginales_control"]
    peor, comparadas = 0.0, 0
    for l in p["celdas_control_a"]:
        for e in p["celdas_control_b"]:
            clave = f"{p['prefijo_control']}{l}x{e}"
            if clave not in sellados:
                out["RESULT-C2COMP-CONTROL-ARBITRO"] = "NO-EJECUTABLE"
                out["RESULT-C2COMP-CONTROL-DELTA-MAX-ABS"] = None
                out["RESULT-C2COMP-CONTROL-N-CELDAS"] = comparadas
                return out
            mio = C2.piso_log_aditivo(
                {"desenlace_id": p["desenlace_control"], "p": marg[l]},
                {"desenlace_id": p["desenlace_control"], "p": marg[e]},
                {"desenlace_id": p["desenlace_control"],
                 "p": p["nacional_control"]})["p"]
            peor = max(peor, abs(sellados[clave] - mio))
            comparadas += 1
    out["RESULT-C2COMP-CONTROL-N-CELDAS"] = comparadas
    out["RESULT-C2COMP-CONTROL-DELTA-MAX-ABS"] = peor
    out["RESULT-C2COMP-CONTROL-ARBITRO"] = (
        "REPRODUCE" if peor <= float(p["umbral_control"]) else "NO-REPRODUCE")

    # ── un RESULT por celda emitible ───────────────────────────────────
    for f in emisiones:
        rid = f["resultado_id"]
        out[rid] = f["p_c2"]
        # Diagnóstico, NO intervalo de confianza. Nombre distinto a
        # propósito para que ningún lector lo tome por un IC.
        out[rid.replace("RESULT-C2COMP-", "RESULT-C2COMP-DIAG-INF-", 1)] = (
            None if f["diagnostico_rango_inf"] == "" else f["diagnostico_rango_inf"])
        out[rid.replace("RESULT-C2COMP-", "RESULT-C2COMP-DIAG-SUP-", 1)] = (
            None if f["diagnostico_rango_sup"] == "" else f["diagnostico_rango_sup"])
    return out
