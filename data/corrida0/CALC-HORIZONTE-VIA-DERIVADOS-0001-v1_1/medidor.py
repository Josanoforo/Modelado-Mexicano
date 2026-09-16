"""`CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` -- siete derivados deterministas
(complemento e inclusion-exclusion) sobre RESULT ya sellados de ENIF 2024.
Releva `CORR-0015` completa: `RES-0047/0049/0053/0054/0055/0056/0066`.

Interfaz estable: `medir(inputs, contrato) -> {"RESULT-…": v}`.

ESCRITO Y CONGELADO EN EL COMMIT-1 DE LA SUCESION v1.1 (`ACTO
GEN2-MEDICION-DEMANDA-2`, CAJA, 15/sep/2026), DESPUES de sellar el padre
(`CALC-TIENE-AHORROS-0001-v1_1`, `CORR-0009` agotada) y ANTES de correr este
CALC. Spec humana sellada: `forense/prereg-caja/ENIF-HORIZONTE-VIA-DERIVADOS-spec-v1_0.md`
(sha `8c04222f…`), via `spec.md`/`spec.yaml` de esta carpeta.

Cero microdato, cero bootstrap, cero `numpy`/`pandas`: libreria estandar.
Los seis insumos llegan como BYTES de los `resultados.json` sellados que
`preflight` verifico por sha256 (`inputs[...]["bytes"]`, P1: no se reabre el
disco). Ninguno se lee de `milpa/`.

Lo que decide el CODIGO y no la spec, declarado para que se pueda refutar:
  · Guardia NO-ESTIMABLE-INSUMO-CAMBIO (la que la v1_0 declara en `filtros`):
    cada insumo se compara con `parametros.insumos_esperados` dentro de
    `parametros.tolerancia_guardia_insumos` (1e-6). La spec no permite `None`
    en los 7 derivados (sin `permite_no_estimable`), asi que si alguno difiere
    la guardia PARA con `RuntimeError` y el runner registra exit != 0. Un CALC
    sellado que cambio de valor es exactamente lo que E.3 prohibe: se para, no
    se disfraza.
  · `no_ahorra` = `RESULT-TIENEAHORROS-A-P-NO-TIENE` tal cual (complemento
    CONTADO en el padre, no re-contado aqui -- verbatim de la transformacion).
  · `A-SUMA-UNO-VIA` compara la particion con 1 dentro de la misma tolerancia
    (1e-6); si no suma, `NO:<residuo>` y se declara
    `NO-ESTIMABLE-PARTICION-INCONSISTENTE` en el mismo texto -- los 7 valores
    se devuelven igual (son aritmetica sobre sellados, no dejan de existir).
"""
from __future__ import annotations

import json

P = "RESULT-HVD-"
IN_E1 = "IN-CALC-ENIF-0001-RESULTADOS"
IN_E2 = "IN-CALC-ENIF-0002-RESULTADOS"
IN_TA = "IN-CALC-TIENE-AHORROS-0001-V1-1-RESULTADOS"

# de que archivo sale cada insumo (sin ambiguedad, sin busqueda)
FUENTE = {
    "RESULT-ENIF-AHO-A-P-CORTO-SIN-P": IN_E1,
    "RESULT-ENIF-AHO-A-P-CORTO-CON-P": IN_E1,
    "RESULT-ENIF-AHO-B-P-FORMAL-P": IN_E1,
    "RESULT-ENIF-AHO-B-P-INFORMAL-P": IN_E1,
    "RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P": IN_E2,
    "RESULT-TIENEAHORROS-A-P-TIENE": IN_TA,
    "RESULT-TIENEAHORROS-A-P-NO-TIENE": IN_TA,
}


def _resultados(inputs: dict, iid: str) -> dict:
    ent = inputs[iid]
    crudo = ent.get("bytes")
    if crudo is None:                       # P1: solo si el snapshot no trajo bytes
        with open(ent["ruta_absoluta"], "rb") as fh:
            crudo = fh.read()
    doc = json.loads(crudo.decode("utf-8"))
    return doc.get("resultados") or {}


def medir(inputs: dict, contrato: dict) -> dict:
    par = contrato.get("parametros") or {}
    esperados = par["insumos_esperados"]
    tol = float(par.get("tolerancia_guardia_insumos", 1e-6))

    cache = {iid: _resultados(inputs, iid) for iid in (IN_E1, IN_E2, IN_TA)}
    v = {}
    cambios = []
    for rid, iid in FUENTE.items():
        if rid not in cache[iid]:
            raise RuntimeError(f"NO-ESTIMABLE-INSUMO-AUSENTE: {rid} no esta en {iid}")
        val = cache[iid][rid]
        if val is None or not isinstance(val, (int, float)):
            raise RuntimeError(f"NO-ESTIMABLE-INSUMO-NO-NUMERICO: {rid}={val!r}")
        val = float(val)
        if abs(val - float(esperados[rid])) > tol:
            cambios.append(f"{rid}: sellado={val!r} esperado={esperados[rid]!r}")
        v[rid] = val
    if cambios:
        # E.3: un sellado que cambio de valor no se disfraza -- se PARA
        raise RuntimeError("NO-ESTIMABLE-INSUMO-CAMBIO: " + " | ".join(cambios))

    corto_sin = v["RESULT-ENIF-AHO-A-P-CORTO-SIN-P"]
    corto_con = v["RESULT-ENIF-AHO-A-P-CORTO-CON-P"]
    corto_nt = v["RESULT-ENIF-POB-P-CORTO-NO-TRABAJA-P"]
    tiene = v["RESULT-TIENEAHORROS-A-P-TIENE"]
    no_tiene = v["RESULT-TIENEAHORROS-A-P-NO-TIENE"]
    a_formal = v["RESULT-ENIF-AHO-B-P-FORMAL-P"]
    b_informal = v["RESULT-ENIF-AHO-B-P-INFORMAL-P"]

    # transformacion, verbatim de la spec
    ambas = a_formal + b_informal - tiene
    solo_formal = a_formal - ambas
    solo_informal = b_informal - ambas
    no_ahorra = no_tiene
    suma = ambas + solo_formal + solo_informal + no_ahorra
    residuo = abs(suma - 1.0)
    if residuo <= tol:
        suma_txt = f"SI:{residuo:.3e}"
    else:
        suma_txt = f"NO:{residuo:.3e}:NO-ESTIMABLE-PARTICION-INCONSISTENTE"

    return {
        P + "A-HORIZONTE-NO-CORTO-SIN-SS": 1.0 - corto_sin,
        P + "A-HORIZONTE-NO-CORTO-CON-SS": 1.0 - corto_con,
        P + "A-HORIZONTE-NO-CORTO-NO-TRABAJA": 1.0 - corto_nt,
        P + "A-AMBAS-VIAS": ambas,
        P + "A-SOLO-FORMAL": solo_formal,
        P + "A-SOLO-INFORMAL": solo_informal,
        P + "A-NO-AHORRA": no_ahorra,
        P + "A-SUMA-UNO-VIA": suma_txt,
    }
