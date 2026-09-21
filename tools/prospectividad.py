#!/usr/bin/env python3
"""Rótulo PROSPECTIVA / RETROSPECTIVA del marcador -- ACTO GEN2-MARCADOR-E-INFORME-1 · P2.

Firma de mesa (21/sep/2026, decisiones de mesa a MOTOR, verbatim):
«Rótulo PROSPECTIVA/RETROSPECTIVA en todo marcador».

QUÉ DEFECTO ATRAPA (§1, «el aparato tiene costo»). El marcador publica en la
misma columna `estado` celdas que predijeron antes de ver el dato y celdas que
se compararon contra un número que ya estaba sobre la mesa. Un lector de
producto -- mesa, o un comprador escéptico -- lee «N celdas con error medido» y
entiende «N predicciones acertadas». Las 89 filas `IDENTICO` del marcador tienen
M y R porque `emisor_vs_arbitro = EMISOR=ARBITRO`: son EL MISMO NÚMERO copiado.
Sin este rótulo, el informe del programa no puede escribir una sola frase
honesta sobre qué sabe hacer el motor.

LA COLUMNA SE DERIVA, NO SE TECLEA. El orden sale de los SELLOS: el campo
`fecha` del `ejecucion.json` de cada CALC, que es parte de la corrida sellada y
no se reescribe (E.3). `git` NO se usa como fuente de orden, y la razón es
medible en este mismo repo: el clon de trabajo es `shallow` (`.git/shallow`
presente), y ahí `git log --diff-filter=A -- milpa/tramite-ola5-propuesta-v0.yaml`
devuelve 2026-09-20T01:46:10Z para un archivo que
`CALC-PISO-PERSISTENCIA-ERROR-0001` ya declara como input `TRAMITE-OLA5-PROPUESTA`
en una corrida sellada a las 2026-09-19T21:37:26Z. Una fecha de `git` que llega
DESPUÉS de la corrida que leyó el archivo no es una fecha de nacimiento: es el
borde del clon. Los sellos no tienen ese problema.

CINCO VALORES QUE NUNCA SE COLAPSAN (A.4: ninguna clasificación negativa sin
universo, y ningún negativo que se degrade a otro):

  PROSPECTIVA               la emisión está sellada ANTES de que existiera la R
                            contra la que se compara, y las dos fechas salen de
                            dos `ejecucion.json` distintos.
  RETROSPECTIVA             la R ya existía cuando la emisión se selló.
  IDENTICO-EMISOR-ES-ARBITRO  `emisor_vs_arbitro = EMISOR=ARBITRO`: M y R son el
                            mismo número copiado. No es predicción de nada, ni
                            acertada ni fallada. Se rotula como lo que es.
  SIN-EMISION               no hay nada emitido que contrastar (celda reservada,
                            sin piso, o diagnóstica).
  EMITIDA-SIN-R             hay emisión sellada y NO hay R todavía. Es el estado
                            de una reserva de evaluación viva (E.6): candidata a
                            PROSPECTIVA el día que su R se derive, y hoy nada.
                            No se colapsa con SIN-EMISION -- «no emitió» y «emitió
                            y nadie la ha contrastado» son dos hechos distintos.
  ORDEN-NO-DERIVABLE        hay emisión y hay R, pero el orden no se deriva de
                            dos sellos. NO se degrada a RETROSPECTIVA (serían
                            dos hallazgos distintos colapsados en uno) y NUNCA
                            cuenta como PROSPECTIVA.

DIRECCIÓN DEL ERROR, DELIBERADA. Cuando el orden no se establece con dos sellos,
la celda NO sube a PROSPECTIVA. Es el PARO (d) del encargo leído al derecho: la
métrica no sube contando algo que no tuvo emisión sellada antes de su R.
"""
from __future__ import annotations

import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRIDA0_DIR = os.path.join(RAIZ, "data", "corrida0")

PROSPECTIVA = "PROSPECTIVA"
RETROSPECTIVA = "RETROSPECTIVA"
IDENTICO = "IDENTICO-EMISOR-ES-ARBITRO"
SIN_EMISION = "SIN-EMISION"
EMITIDA_SIN_R = "EMITIDA-SIN-R"
NO_DERIVABLE = "ORDEN-NO-DERIVABLE"

#: El orden en que se listan en toda vista. `PROSPECTIVA` primero porque es la
#: única clase que sostiene una frase de producto; las otras son, cada una, una
#: razón distinta por la que no la sostiene.
VALORES = (PROSPECTIVA, RETROSPECTIVA, IDENTICO, SIN_EMISION, EMITIDA_SIN_R,
           NO_DERIVABLE)

#: Las dos clases que una vista NUNCA suma en una sola cifra (firma de mesa
#: 21/sep/2026). Quien quiera un total, que publique las cinco celdas.
NO_SE_SUMAN = (PROSPECTIVA, RETROSPECTIVA)


def _sin_sufijo_de_corrida(calc_ref: str) -> str:
    """`CALC-X-0001--39bf1af3cdac` -> `CALC-X-0001`.

    Las referencias de holdout citan la CORRIDA (con su hash), y el directorio
    en `data/corrida0/` lleva el id de la SPEC. Es el mismo objeto con dos
    nombres, y aquí se normaliza al del directorio.
    """
    ref = (calc_ref or "").strip()
    return ref.split("--", 1)[0]


def fecha_de_sello(calc_ref: str) -> str | None:
    """Fecha UTC del `ejecucion.json` sellado de un CALC, o None si no hay.

    Nunca estima ni infiere: si el `ejecucion.json` no está, o no trae `fecha`,
    devuelve None y el llamador cae a `ORDEN-NO-DERIVABLE`.
    """
    calc_id = _sin_sufijo_de_corrida(calc_ref)
    if not calc_id:
        return None
    ruta = os.path.join(CORRIDA0_DIR, calc_id, "ejecucion.json")
    if not os.path.exists(ruta):
        return None
    try:
        with open(ruta, encoding="utf-8") as fh:
            return json.load(fh).get("fecha") or None
    except (OSError, ValueError):
        return None


def clasifica(fila: dict, calc_emision: str = "", calc_r: str = "") -> tuple[str, str]:
    """(rótulo, cita) para una fila del marcador.

    `calc_emision` / `calc_r` son los dos CALC que el llamador ya resolvió desde
    la celda-D (`adjudicacion_por_celda[*].calc` y `momentos_holdout_refs`).
    Cuando la fila no es de cruce se dejan vacíos y deciden los campos de la
    propia fila, que son derivados y están en el TSV a la vista.
    """
    if (fila.get("emisor_vs_arbitro") or "") == "EMISOR=ARBITRO":
        return IDENTICO, ("emisor_vs_arbitro=EMISOR=ARBITRO -- M y R son el mismo "
                          "número copiado; no hay predicción que fechar")

    hay_m = str(fila.get("M") or "").strip() != ""
    hay_piso = str(fila.get("piso") or "").strip() != ""
    hay_emision_declarada = str(fila.get("emision") or "").strip() != ""
    if not hay_m and not hay_piso:
        if hay_emision_declarada:
            return EMITIDA_SIN_R, (
                f"emision={fila.get('emision', '')}; estado={fila.get('estado', '')} "
                "-- emitida y todavía sin R contra la cual fecharla")
        return SIN_EMISION, (f"estado={fila.get('estado', '')} -- fila sin M y sin "
                             "piso: no hay emisión que contrastar")

    hay_r = str(fila.get("R") or "").strip() != ""
    hay_error = str(fila.get("error_piso_pp") or "").strip() != ""
    if not hay_r and not hay_error and not (calc_emision and calc_r):
        return EMITIDA_SIN_R, (
            f"estado={fila.get('estado', '')} -- hay emisión pero la fila no trae R "
            "ni error contra el cual fecharla")

    if calc_emision and calc_r:
        f_emision = fecha_de_sello(calc_emision)
        f_r = fecha_de_sello(calc_r)
        if f_emision and f_r:
            cita = (f"{_sin_sufijo_de_corrida(calc_emision)}/ejecucion.json:fecha="
                    f"{f_emision} vs {_sin_sufijo_de_corrida(calc_r)}/"
                    f"ejecucion.json:fecha={f_r}")
            return (PROSPECTIVA if f_emision < f_r else RETROSPECTIVA), cita
        faltan = [n for n, f in ((calc_emision, f_emision), (calc_r, f_r)) if not f]
        return NO_DERIVABLE, ("sin `fecha` sellada en: " + ", ".join(
            _sin_sufijo_de_corrida(n) for n in faltan))

    if hay_piso and not hay_m:
        # A-bis 6: el piso es la ola anterior por eje y «no identifica nada:
        # acota a los retadores». Su R es la marginal ya PUBLICADA de la ola
        # siguiente del mismo instrumento -- el marcador la lee de
        # `milpa/tramite-ola5-propuesta-v0.yaml`, no de un CALC sellado después
        # del piso. Un número que ya estaba publicado cuando el piso se selló es,
        # por definición, retrospectivo, y el propio derivador lo dice al dejar
        # M vacía en toda fila marginal.
        return RETROSPECTIVA, (
            f"piso_tipo={fila.get('piso_tipo', '')}; R leída de "
            f"{fila.get('fuente', '')} (marginal ya publicada de la ola t), no de "
            "un CALC sellado después del piso -- A-bis 6")

    return NO_DERIVABLE, ("hay emisión y R pero el llamador no aportó los dos CALC "
                          "con los que fechar el orden")


def anota(filas: list[dict], calcs_por_fila: dict | None = None) -> list[dict]:
    """Añade `prospectividad` y `prospectividad_cita` a cada fila, en sitio.

    `calcs_por_fila` mapea `celda_id -> (calc_emision, calc_r)` para las filas
    de cruce, donde el orden se fecha con dos sellos.
    """
    calcs_por_fila = calcs_por_fila or {}
    for f in filas:
        emision, r = calcs_por_fila.get(f.get("celda_id"), ("", ""))
        f["prospectividad"], f["prospectividad_cita"] = clasifica(f, emision, r)
    return filas


def resumen(filas: list[dict]) -> dict:
    """Conteo por rótulo. Las cinco claves SIEMPRE salen, incluso en cero.

    No hay clave de total: `PROSPECTIVA` y `RETROSPECTIVA` no se suman (firma de
    mesa 21/sep/2026), y un total las sumaría por la puerta de atrás.
    """
    cuenta = {v: 0 for v in VALORES}
    for f in filas:
        cuenta[f.get("prospectividad", NO_DERIVABLE)] = cuenta.get(
            f.get("prospectividad", NO_DERIVABLE), 0) + 1
    cuenta["_nota"] = ("PROSPECTIVA y RETROSPECTIVA no se suman en una sola cifra "
                       "(firma de mesa 21/sep/2026); no hay clave de total a "
                       "propósito. `_universo` es len(filas), no una validación.")
    cuenta["_universo"] = len(filas)
    return cuenta
