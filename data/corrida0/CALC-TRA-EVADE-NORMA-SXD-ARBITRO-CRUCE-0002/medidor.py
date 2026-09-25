#!/usr/bin/env python3
"""Re-adjudicación -0002 de `TRA.evade_norma.envipe2025.escolaridad_x_dominio`.

ACTO GEN2-PISOS-GEN2-2 (24/sep/2026, CAJA), P3. Contrato humano:
`forense/prereg-caja/TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002-spec-v1_0.md`.

HEREDA POR SHA el medidor de `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0001`
(input `medidor_0001`, `funcion: CODIGO`) y lo EJECUTA sin editarlo: misma R,
mismo criterio, mismos umbrales, mismos contendientes (C1, C2 pisos; C6, C7
retadores), mismos parámetros (copiados verbatim en el `spec.yaml`). Cambia SOLO
la fuente de C2: el `-C2-P-{celda}` y su `-C2-IC95INF/SUP-{celda}` que el -0001
lee de las emisiones (compuestos con marginales de `milpa/`) se sustituyen, antes
de llamarlo, por los de `CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001`, citados por
id. El -0001 lee las emisiones por ruta: la copia sustituida se escribe en un
directorio temporal que se borra al salir. Todo lo demás pasa intacto.

Los ids del -0001 (`RESULT-TRA-SXD12-ARB-*`) se renombran a `RESULT-TRA-SXD12-ARB2-*`.
Se añaden: punto e IC del piso por celda, el C2 de la emisión como descriptivo,
`G-FUENTE-C2` y el control de oro del -0001 (todo id que no depende de C2
reproduce el sellado a `tol_oro_0001`).
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path

P1 = "RESULT-TRA-SXD12-ARB"
P = "RESULT-TRA-SXD12-ARB2"
PE = "RESULT-TRA-SXD12"
PISO = "RESULT-ENVIPE2025-PISOS-EVADE-NORMA-SXD"
INPUTS = frozenset({"envipe2025_csv", "emisiones_selladas", "emisiones_sello",
                    "medidor_0001", "receta_marginales", "ejes_l1", "calibracion_ic",
                    "adjudicacion_0001_resultados", "adjudicacion_0001_sello",
                    "piso_c2_resultados", "piso_c2_sello"})
# Ids del -0001 que dependen del punto o del IC de C2 (por construcción de su `medir`).
DEPENDE_DE_C2 = ("-D-C2-", "-DENTRO-IC-R-C2-", "-SIGNO-C2-", "-VS-C2-",
                 "-VEREDICTO-CELDA-", "-GANA-A-AMBOS-PISOS", "-INDECIDIBLES",
                 "-G-SIGNO-ESTABLE-C2", "-G-MAE-C2", "-G-MEJOR-CANDIDATO-POR-MAE",
                 "-G-CHALLENGER-GANADOR", "-VENCE-A-C2-EN-CELDAS", "-G-B-BIS-LEIDO")


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
                        (f"{PISO}-G-CTRL-ARBITRO-VEREDICTO", "REPRODUCE"),
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

    _importa("marginales_reproduccion", inputs["receta_marginales"]["ruta_absoluta"])
    A1 = _importa("medidor_adjudicacion_0001", inputs["medidor_0001"]["ruta_absoluta"])
    celdas = list(A1.CELDAS)

    raw = json.loads(inputs["emisiones_selladas"]["bytes"].decode("utf-8"))
    emis = raw["resultados"]
    c2_emision = {c: emis[f"{PE}-C2-P-{c}"] for c in celdas}
    for c in celdas:
        for suf in ("P", "IC95INF", "IC95SUP"):
            emis[f"{PE}-C2-{suf}-{c}"] = piso[f"{PISO}-C2-{suf}-{c}"]

    with tempfile.TemporaryDirectory(prefix="tra-arb2-") as tmp:
        ruta = Path(tmp) / "resultados.json"
        ruta.write_text(json.dumps(raw), encoding="utf-8")
        sustituido = dict(inputs)
        sustituido["emisiones_selladas"] = {**inputs["emisiones_selladas"],
                                            "ruta_absoluta": str(ruta)}
        base = A1.medir(sustituido, contrato)
    out = {P + k[len(P1):]: v for k, v in base.items()}

    for c in celdas:
        for suf in ("P", "IC95INF", "IC95SUP"):
            out[f"{P}-C2-{suf}-{c}"] = piso[f"{PISO}-C2-{suf}-{c}"]
        out[f"{P}-C2-P-EMISION-0001-{c}"] = c2_emision[c]
    out[f"{P}-G-FUENTE-C2"] = (
        "CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001 (" + PISO + "-C2-P/IC95*-*, por id; "
        "marginales ENVIPE 2025 medidos del manifiesto) -- RETROSPECTIVA: sellado despues de R")
    out[f"{P}-G-PISO-C2-SHA256"] = str(inputs["piso_c2_resultados"]["sha256"])

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
