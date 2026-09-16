"""`CALC-TRIADA-B-PISO-0001` -- la tabla comun de la triada con `B` de
persistencia como piso, DERIVADA celda a celda y no heredada.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE `ACTO GEN2-F5-CIERRE-Y-PANEL-1`.

Lo que hace, y nada mas. Toma los errores absolutos por celda que
`celdas.tsv` del sucesor ya trae para `L_SOLO`, `L_CORPUS` y `M`, y el
`err_pp` de `B` bajo el brazo `PERSISTENCIA` que `CALC-B-MARCO-MAE-0001`
sello; recorta al universo donde los CUATRO corredores tienen punto
(`U_COMUN` = `U3` ∩ celdas con `B`), y promedia `|err_pp|` sobre ese
universo, en orden fijo de `id`. Reporta el `n` y la lista de celdas junto
a cada `MAE` (A-bis.4: jamas se compara un MAE contra otro universo sin
decirlo) y la razon nominal de cada celda excluida.

Antes de eso corre el CONTROL DE DERIVACION, que es la razon de ser de este
CALC: recalcula desde `celdas.tsv` los tres `MAE` de `CALC-TRIADA-0002`
sobre `U3` y los enfrenta a los sellados. Si los tres no reproducen al
centesimo, la tabla comun NO se emite y el veredicto es
`NO-DERIVA-CONTROL-FALLA`: el acto deriva, no hereda, y una derivacion que
no reproduce su origen no es una derivacion.

Lo que NO hace: no corre pareadas, no calcula IC, no adjudica, no corona,
no imputa, no re-corre la triada y no toca su veredicto vigente
(`SIN-GANADOR-UNICO` se cita tal cual desde `CALC-TRIADA-0002`). No abre
microdato, no llama a ningun modelo y no adopta nada al motor.
"""
from __future__ import annotations

import csv
import io
import json

PRE = "RESULT-TBP"


def _num(v):
    if v is None or v == "":
        return None
    f = float(v)
    return None if (f != f or f in (float("inf"), float("-inf"))) else f


def _json_de(inputs, iid):
    return json.loads(inputs[iid]["bytes"].decode("utf-8"))


def _tsv_de(inputs, iid):
    txt = inputs[iid]["bytes"].decode("utf-8")
    return list(csv.DictReader(io.StringIO(txt), delimiter="\t"))


def _valores_de(doc):
    """`resultados.json` de un CALC sellado por `corrida0 run`:
    `{"resultados": {RESULT-id: valor, …}, "spec_id": …}`."""
    if isinstance(doc, dict) and isinstance(doc.get("resultados"), dict):
        vals = dict(doc["resultados"])
    else:
        vals = {}
    if not vals:
        raise RuntimeError("resultados.json sin RESULT legibles")
    return vals


def _media(xs):
    return sum(xs) / len(xs)


def medir(inputs, contrato):
    p = contrato["parametros"]
    out: dict[str, object] = {}

    corredores = list(p["corredores"])          # orden de reporte, fijo
    col_err = dict(p["columnas_err"])           # corredor -> columna de celdas.tsv
    brazo_b = str(p["brazo_b"])
    patron_b = str(p["patron_b"])
    tol_exacto = float(p["control"]["umbral_exacto"])
    tol_cent = float(p["control"]["umbral_centesimo"])

    # ---- guardia de identidad: celdas.tsv es EXACTAMENTE el marco de 14 ----
    ids_marco = [r["id"] for r in _tsv_de(inputs, p["input_marco"])]
    filas = _tsv_de(inputs, p["input_celdas"])
    ids_celdas = [r["id_celda"] for r in filas]
    if sorted(ids_marco) != sorted(ids_celdas) or len(ids_marco) != int(p["n_celdas_marco"]):
        raise RuntimeError(f"celdas.tsv {ids_celdas} != marco {ids_marco}")
    out[f"{PRE}-N-CELDAS-MARCO"] = len(ids_marco)
    orden = sorted(ids_celdas)
    por_id = {r["id_celda"]: r for r in filas}

    # ---- U3 re-derivado de celdas.tsv, no citado ----
    u3 = [c for c in orden if por_id[c]["en_u3"] == "SI"]
    out[f"{PRE}-U3-N"] = len(u3)
    out[f"{PRE}-U3-IDS"] = ",".join(u3)

    # ---- CONTROL DE DERIVACION contra los MAE sellados de CALC-TRIADA-0002 ----
    sellados = _valores_de(_json_de(inputs, p["input_triada_0002"]))
    ramas = []
    for corr in corredores:
        rid_sellado = p["control"]["sellado"].get(corr)
        if rid_sellado is None:      # B no corrio en la 0002: no hay que controlar
            continue
        if rid_sellado not in sellados:
            raise RuntimeError(f"CALC-TRIADA-0002: falta {rid_sellado}")
        derivado = _media([_num(por_id[c][col_err[corr]]) for c in u3])
        sello = _num(sellados[rid_sellado])
        d = derivado - sello
        if abs(d) <= tol_exacto:
            rama = "REPRODUCE-EXACTO"
        elif abs(d) < tol_cent:
            rama = "REPRODUCE-AL-CENTESIMO"
        else:
            rama = "NO-REPRODUCE"
        ramas.append(rama)
        out[f"{PRE}-U3-CONTROL-{corr}-DERIVADO-PP"] = derivado
        out[f"{PRE}-U3-CONTROL-{corr}-SELLADO-PP"] = sello
        out[f"{PRE}-U3-CONTROL-{corr}-DELTA-PP"] = d
        out[f"{PRE}-U3-CONTROL-{corr}-RAMA"] = rama
    out[f"{PRE}-U3-CONTROL-N-RAMAS"] = len(ramas)
    control_ok = bool(ramas) and all(r != "NO-REPRODUCE" for r in ramas)
    out[f"{PRE}-U3-CONTROL-VEREDICTO"] = "DERIVA" if control_ok else "NO-DERIVA"

    # ---- `B` de persistencia, celda a celda, desde el asiento sellado ----
    bm = _valores_de(_json_de(inputs, p["input_b_mae"]))
    err_b: dict[str, float] = {}
    for c in orden:
        v = _num(bm.get(patron_b.format(celda=c, brazo=brazo_b)))
        if v is not None:
            err_b[c] = abs(v)
    out[f"{PRE}-COBERTURA-B-{brazo_b}"] = len(err_b)
    out[f"{PRE}-COBERTURA-B-IDS"] = ",".join(c for c in orden if c in err_b)

    # ---- U_COMUN: donde los CUATRO corredores tienen punto ----
    comun = [c for c in u3 if c in err_b]
    out[f"{PRE}-UCOMUN-N"] = len(comun)
    out[f"{PRE}-UCOMUN-IDS"] = ",".join(comun)

    for c in orden:
        pc = f"{PRE}-{c}"
        en = c in comun
        out[f"{pc}-EN-UCOMUN"] = "SI" if en else "NO"
        # se emite para LAS 14: el conjunto de llaves de salida no puede
        # depender de los valores (`P3` compara el set EXACTO contra la spec).
        out[f"{pc}-RAZON-EXCLUSION"] = (
            "EN-UCOMUN" if en
            else ("FUERA-DE-U3-Y-SIN-B" if (c not in u3 and c not in err_b)
                  else ("FUERA-DE-U3" if c not in u3 else f"SIN-B-{brazo_b}")))
        for corr in corredores:
            v = err_b.get(c) if corr == "B" else _num(por_id[c][col_err[corr]])
            out[f"{pc}-ERR-ABS-{corr}-PP"] = v

    # ---- la tabla comun. Solo si el control dejo derivar Y hay universo. ----
    # `U_COMUN` vacio no es un MAE de cero celdas: es una tabla que no existe.
    if not control_ok or not comun:
        for corr in corredores:
            out[f"{PRE}-UCOMUN-MAE-{corr}-PP"] = None
        out[f"{PRE}-UCOMUN-ORDEN-DESCRIPTIVA"] = "NO-EMITIDA"
        out[f"{PRE}-UCOMUN-N-CELDAS-B-MENOR-QUE-M"] = None
        out[f"{PRE}-VEREDICTO"] = ("NO-DERIVA-CONTROL-FALLA" if not control_ok
                                   else "NO-EMITE-UCOMUN-VACIO")
    else:
        mae = {}
        for corr in corredores:
            xs = [err_b[c] if corr == "B" else _num(por_id[c][col_err[corr]])
                  for c in comun]
            if any(x is None for x in xs):
                raise RuntimeError(f"{corr}: celda sin punto dentro de U_COMUN")
            mae[corr] = _media(xs)
            out[f"{PRE}-UCOMUN-MAE-{corr}-PP"] = mae[corr]
        # ordenacion DESCRIPTIVA por MAE ascendente; desempate por orden declarado
        orden_desc = sorted(corredores, key=lambda k: (mae[k], corredores.index(k)))
        out[f"{PRE}-UCOMUN-ORDEN-DESCRIPTIVA"] = " < ".join(orden_desc)
        out[f"{PRE}-UCOMUN-N-CELDAS-B-MENOR-QUE-M"] = sum(
            1 for c in comun if err_b[c] < _num(por_id[c][col_err["M"]]))
        out[f"{PRE}-VEREDICTO"] = "NO-ADJUDICA-POR-DISENO"

    # ---- lo que este CALC deja exactamente como estaba ----
    out[f"{PRE}-TRIADA-VEREDICTO-VIGENTE"] = str(
        sellados[p["rid_veredicto_0002"]])
    out[f"{PRE}-PAREADAS-NUEVAS"] = 0
    out[f"{PRE}-IC-NUEVOS"] = 0
    out[f"{PRE}-ADOPCIONES"] = 0
    out[f"{PRE}-LLAMADAS-A-MODELO"] = 0
    return out
