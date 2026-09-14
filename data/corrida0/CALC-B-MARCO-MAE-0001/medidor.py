"""`CALC-B-MARCO-MAE-0001` -- el asiento de `B` sobre el marco de 14 celdas:
cobertura, `err_pp` frente al arbitro `R`, control positivo y `MAE_pp(B)`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-B-MARCO`. Su `spec.yaml`
se instancia DESPUES de que los tres CALC de serie sellen, porque declara
sus `resultados.json` como insumos por sha256 (mismo patron que
`CALC-C0D-MARCADOR-v3` con `IN-V2-RESULTADOS`); la REGLA de este medidor no
cambia entre el COMMIT-1 y ese momento: es este archivo.

Es el UNICO CALC de la familia `B-MARCO` que lee `corridas-R/*.json` (el
arbitro GEN1 de cada celda). Por la regla E.1 del registro eso lo hace
`envuelto_legacy = SI`, y se declara asi: la comparacion contra `R` es, por
construccion, una comparacion contra un numero GEN1. Los tres CALC de serie
no lo leen y quedan GEN2 limpios.

Lo que hace, y nada mas: por celda del marco, cita la prediccion de `B`
(sellada por el CALC de su serie, o por `CALC-B-0001` en las dos celdas
originales), lee `R`, calcula `err_pp = 100·(P_B − R)` (A-bis.3: puntos
porcentuales de una proporcion ponderada) y el control positivo (la
observada propia del CALC de serie frente a `R`, tres ramas pre-declaradas).
Agrega `MAE_pp(B)` por brazo SOBRE LAS CELDAS CUBIERTAS y lo reporta CON su
`n` y con la lista de celdas (A-bis.4: jamas se compara contra un MAE de
otro universo sin decirlo). No lee `M` ni `L`, no ordena corredores, no
adjudica nada: el veredicto de la triada no se toca.
"""
from __future__ import annotations

import csv
import io
import json


def _num(v):
    if v is None:
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _json_de(inputs, iid):
    return json.loads(inputs[iid]["bytes"].decode("utf-8"))


def _valores_de(doc):
    """`resultados.json` de un CALC sellado por `corrida0 run`: la forma que el
    runner escribe es `{"resultados": {RESULT-id: valor, …}, "spec_id": …}`
    (verificado sobre `CALC-B-0001/resultados.json`). Se asevera que la
    salida no quede vacia."""
    if isinstance(doc, dict) and isinstance(doc.get("resultados"), dict):
        vals = dict(doc["resultados"])
    else:
        vals = {}
    if not vals:
        raise RuntimeError("resultados.json sin RESULT legibles")
    return vals


def medir(inputs, contrato):
    p = contrato["parametros"]
    brazos = list(p["brazos"])
    ctrl = p["control_r"]
    out: dict[str, object] = {}

    # guardia de identidad: las celdas declaradas son EXACTAMENTE las 14 del marco
    marco = inputs[p["input_marco"]]["bytes"].decode("utf-8")
    ids_marco = [r["id"] for r in csv.DictReader(io.StringIO(marco), delimiter="\t")]
    ids_decl = [str(c["celda"]) for c in p["celdas"]]
    if sorted(ids_marco) != sorted(ids_decl) or len(ids_marco) != int(p["n_celdas_marco"]):
        raise RuntimeError(f"celdas declaradas {ids_decl} != marco {ids_marco}")
    out["RESULT-BM-MAE-N-CELDAS-MARCO"] = len(ids_marco)

    cache: dict[str, dict] = {}
    err: dict[str, dict[str, float]] = {b: {} for b in brazos}
    n_no_constr = 0
    for c in p["celdas"]:
        cel = str(c["celda"])
        pre = f"RESULT-BM-MAE-{cel}"
        if not c.get("fuente"):
            n_no_constr += 1
            out[f"{pre}-ORIGEN-B"] = str(c["razon_sin_b"])
            out[f"{pre}-R"] = None
            out[f"{pre}-CONTROL-R-DELTA"] = None
            out[f"{pre}-CONTROL-R-RAMA"] = "SIN-B"
            for b in brazos:
                out[f"{pre}-{b}-P-B"] = None
                out[f"{pre}-{b}-ERR-PP"] = None
                out[f"{pre}-{b}-ESTADO"] = "SIN-B"
            continue
        fuente = str(c["fuente"])
        if fuente not in cache:
            cache[fuente] = _valores_de(_json_de(inputs, fuente))
        vals = cache[fuente]
        out[f"{pre}-ORIGEN-B"] = str(c["origen_b"])
        r_doc = _json_de(inputs, c["input_r"])
        if str(r_doc.get("id_celda")) != cel or str(r_doc.get("estado")) != "COMPUTADO":
            raise RuntimeError(f"corridas-R de {cel}: id_celda={r_doc.get('id_celda')!r} "
                               f"estado={r_doc.get('estado')!r}")
        R = _num(r_doc.get("R"))
        out[f"{pre}-R"] = R
        # control positivo: la observada propia del CALC de serie vs. R de la celda
        po = _num(vals.get(c["obs"]))
        if po is None or R is None:
            out[f"{pre}-CONTROL-R-DELTA"] = None
            out[f"{pre}-CONTROL-R-RAMA"] = "SIN-OBSERVADA"
        else:
            d = po - R
            out[f"{pre}-CONTROL-R-DELTA"] = _num(d)
            if abs(d) <= float(ctrl["umbral_exacto"]):
                rama = "REPRODUCE-EXACTO"
            elif abs(d) < float(ctrl["umbral_grano"]):
                rama = "REPRODUCE-AL-GRANO"
            else:
                rama = "NO-REPRODUCE"
            out[f"{pre}-CONTROL-R-RAMA"] = rama
        for b in brazos:
            rid = c["b"][b]
            if rid not in vals:
                raise RuntimeError(f"{fuente}: falta {rid}")
            pb = _num(vals.get(rid))
            out[f"{pre}-{b}-P-B"] = pb
            if pb is None or R is None:
                out[f"{pre}-{b}-ERR-PP"] = None
                out[f"{pre}-{b}-ESTADO"] = "SIN-BASELINE"
            else:
                e = 100.0 * (pb - R)
                out[f"{pre}-{b}-ERR-PP"] = _num(e)
                out[f"{pre}-{b}-ESTADO"] = "EMITE"
                err[b][cel] = e
    out["RESULT-BM-MAE-N-NO-CONSTRUIBLES"] = int(n_no_constr)
    out["RESULT-BM-MAE-COBERTURA-ANTES"] = int(p["cobertura_antes"])

    for b in brazos:
        pre = f"RESULT-BM-MAE-{b}"
        e = err[b]
        n = len(e)
        out[f"{pre}-N-CELDAS"] = n
        out[f"{pre}-COBERTURA-DESPUES"] = n
        out[f"{pre}-CELDAS"] = ",".join(sorted(e)) if n else "NINGUNA"
        if n == 0:
            out[f"{pre}-MAE-PP"] = None
            out[f"{pre}-MAX-ABS-ERR-PP"] = None
            out[f"{pre}-CELDA-MAX-ABS"] = "NINGUNA"
            continue
        # suma en orden fijo (ids ordenados) para replay determinista
        out[f"{pre}-MAE-PP"] = _num(sum(abs(e[k]) for k in sorted(e)) / n)
        kmax = max(sorted(e), key=lambda k: abs(e[k]))
        out[f"{pre}-MAX-ABS-ERR-PP"] = _num(abs(e[kmax]))
        out[f"{pre}-CELDA-MAX-ABS"] = kmax
    return out
