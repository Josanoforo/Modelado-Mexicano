#!/usr/bin/env python3
"""Re-adjudicación -0002 de `DIN.ahorro_solo_informal.enif2024.localidad_x_edad`.

ACTO GEN2-PISOS-GEN2-2 (24/sep/2026, CAJA), P3. Contrato humano:
`forense/prereg-caja/DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002-spec-v1_0.md`.

HEREDA POR SHA el medidor de `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`
(input `medidor_0001`, `funcion: CODIGO`) y lo EJECUTA sin editarlo: misma R,
mismo criterio, mismos umbrales, mismos contendientes (C1, C2, C3), mismos
parámetros (copiados verbatim en el `spec.yaml`). Cambia SOLO la fuente del punto
C2: el `-C2-P-{celda}` que el -0001 lee de las emisiones (compuesto con
marginales de `milpa/`) se sustituye, antes de llamarlo, por
`RESULT-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-C2-P-{celda}` del piso sellado
`CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001`, citado por id. Todo lo demás de
las emisiones pasa intacto.

Los ids del -0001 (`RESULT-DIN-LXE8-ARB-*`) se renombran a `RESULT-DIN-LXE8-ARB2-*`.
Se añaden: el punto y el IC del piso por celda (lo que cita la celda-D), el C2
de la emisión como descriptivo, `G-FUENTE-C2` y el control de oro del -0001
(todo id que no depende de C2 reproduce el sellado a `tol_oro_0001`).
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys

P1 = "RESULT-DIN-LXE8-ARB"
P = "RESULT-DIN-LXE8-ARB2"
PE = "RESULT-DIN-LXE8"
PISO = "RESULT-ENIF2024-PISOS-AHORRO-INFORMAL-LXE"
CELDAS = ["L1xE1", "L1xE2", "L1xE3", "L1xE4", "L2xE1", "L2xE2", "L2xE3", "L2xE4"]
INPUTS = frozenset({"enif2024_csv", "emisiones_selladas", "emisiones_sello",
                    "medidor_0001", "medidor_emisiones", "funcion_c2", "extrae_l",
                    "adjudicacion_0001_resultados", "adjudicacion_0001_sello",
                    "piso_c2_resultados", "piso_c2_sello"})
# Ids del -0001 que dependen del punto C2 (por construcción de su `medir`).
DEPENDE_DE_C2 = ("-D-C2-", "-VEREDICTO-C3-VS-C2-", "-VEREDICTO-CELDA-",
                 "-G-C3-GANA-A-AMBOS-PISOS", "-G-C3-INDECIDIBLES", "-G-MAE-C2",
                 "-G-SKILL-C3-VS-C2", "-G-VEREDICTO-CELDA-D")


class ParoDeGuardia(RuntimeError):
    pass


def _importa(nombre, ruta):
    s = importlib.util.spec_from_file_location(nombre, ruta)
    m = importlib.util.module_from_spec(s)
    sys.modules[nombre] = m
    s.loader.exec_module(m)
    return m


def _json(inp):
    raw = inp.get("bytes")
    if raw is None:
        with open(inp["ruta_absoluta"], "rb") as fh:
            raw = fh.read()
    d = json.loads(raw.decode("utf-8"))
    return d.get("resultados", d)


def _sello_cubre(sello_inp, resultados_inp):
    return str(resultados_inp["sha256"]) in json.dumps(_json(sello_inp))


def _guardia(inputs):
    fuera, faltan = sorted(set(inputs) - INPUTS), sorted(INPUTS - set(inputs))
    if fuera or faltan:
        raise ParoDeGuardia(f"inputs fuera de la lista {fuera} · faltan {faltan}")
    for s, r in (("emisiones_sello", "emisiones_selladas"),
                 ("adjudicacion_0001_sello", "adjudicacion_0001_resultados"),
                 ("piso_c2_sello", "piso_c2_resultados")):
        if not _sello_cubre(inputs[s], inputs[r]):
            raise ParoDeGuardia(f"{r}: sha256 no registrado en {s}")
    piso = _json(inputs["piso_c2_resultados"])
    for k, esperado in ((f"{PISO}-G-CTRL-EMISIONES-VEREDICTO", "REPRODUCE"),
                        (f"{PISO}-G-C2-IC-ESTADO", "EMITIDO")):
        if piso.get(k) != esperado:
            raise ParoDeGuardia(f"piso: {k}={piso.get(k)!r}, se exige {esperado}")
    if not str(piso.get(f"{PISO}-G-ORIGEN", "")).startswith("NUEVO"):
        raise ParoDeGuardia("piso: G-ORIGEN no es NUEVO")
    return piso


def _igual(a, b, tol):
    if isinstance(a, float) or isinstance(b, float):
        if a is None or b is None:
            return a is None and b is None
        if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
            return True
        return abs(float(a) - float(b)) <= tol
    return a == b


def medir(inputs, contrato):
    piso = _guardia(inputs)
    par = contrato["parametros"]
    tol = float(par["tol_oro_0001"])

    _importa("test_celda_d_c2", inputs["funcion_c2"]["ruta_absoluta"])
    _importa("extrae_l_v1_1", inputs["extrae_l"]["ruta_absoluta"])
    _importa("medidor_emisiones", inputs["medidor_emisiones"]["ruta_absoluta"])
    A1 = _importa("medidor_adjudicacion_0001", inputs["medidor_0001"]["ruta_absoluta"])

    # El único cambio: el punto C2 que el -0001 lee de las emisiones.
    raw = json.loads(inputs["emisiones_selladas"]["bytes"].decode("utf-8"))
    emis = raw["resultados"]
    c2_emision = {c: emis[f"{PE}-C2-P-{c}"] for c in CELDAS}
    for c in CELDAS:
        emis[f"{PE}-C2-P-{c}"] = piso[f"{PISO}-C2-P-{c}"]
    sustituido = dict(inputs)
    sustituido["emisiones_selladas"] = {
        **inputs["emisiones_selladas"],
        "bytes": json.dumps(raw).encode("utf-8")}   # sha256 declarado: el de las emisiones selladas

    base = A1.medir(sustituido, contrato)
    out = {P + k[len(P1):]: v for k, v in base.items()}

    for c in CELDAS:
        out[f"{P}-C2-P-{c}"] = piso[f"{PISO}-C2-P-{c}"]
        out[f"{P}-C2-IC95INF-{c}"] = piso[f"{PISO}-C2-IC95INF-{c}"]
        out[f"{P}-C2-IC95SUP-{c}"] = piso[f"{PISO}-C2-IC95SUP-{c}"]
        out[f"{P}-C2-P-EMISION-0001-{c}"] = c2_emision[c]
    out[f"{P}-G-FUENTE-C2"] = (
        "CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001 (" + PISO + "-C2-P-*, por id; "
        "marginales ENIF 2024 medidos del manifiesto) -- RETROSPECTIVA: sellado despues de R")
    out[f"{P}-G-PISO-C2-SHA256"] = str(inputs["piso_c2_resultados"]["sha256"])

    # Control de oro (E.5): lo que no depende de C2 reproduce el -0001 sellado.
    oro = _json(inputs["adjudicacion_0001_resultados"])
    comparados, discordan, peor = 0, 0, 0.0
    for k, v in oro.items():
        if any(t in k for t in DEPENDE_DE_C2):
            continue
        mio = base.get(k, "__AUSENTE__")
        comparados += 1
        if not _igual(mio, v, tol):
            discordan += 1
        elif isinstance(v, float) and isinstance(mio, float) and not math.isnan(v):
            peor = max(peor, abs(mio - v))
    out[f"{P}-G-CTRL-ORO-0001-COMPARADOS"] = comparados
    out[f"{P}-G-CTRL-ORO-0001-DISCORDAN"] = discordan
    out[f"{P}-G-CTRL-ORO-0001-MAX-ABS"] = float(peor)
    out[f"{P}-G-CTRL-ORO-0001-VEREDICTO"] = "REPRODUCE" if discordan == 0 else "NO-REPRODUCE"
    out[f"{P}-G-DICTAMEN-0001"] = oro[f"{P1}-G-VEREDICTO-CELDA-D"]
    out[f"{P}-G-DICTAMEN-CAMBIA"] = (
        "SI" if out[f"{P}-G-VEREDICTO-CELDA-D"] != oro[f"{P1}-G-VEREDICTO-CELDA-D"] else "NO")
    return out
