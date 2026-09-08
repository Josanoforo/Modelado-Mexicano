#!/usr/bin/env python3
"""Medidor de CALC-M-marco-M-sorteado-v1_3-ola -- modulacion por ola.

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, P3(c)/(e).

Firma de mesa D-2, 8/sep/2026, verbatim: *«revisa el whitepaper, esto es una
matriz, no colapsamos a menos que la literatura y benchmark de lo que
queremos lograr lo demanden, podemos modular por ola si es lo mas
practico»*.

## Que hace, exactamente

**No colapsa olas.** Las 14 celdas del marco vigente siguen siendo 14. Lo
que esta corrida DEMUESTRA es el aparato de la modulacion por ola, celda por
celda:

  · si la conducta de la celda trae `serie_olas`, el punto usa la **ultima
    ola ESTRICTAMENTE ANTERIOR** a la del arbitro, y se declara
    `SERIE-PREVIA · <ola>`;
  · si la serie no trae ninguna ola anterior, `SIN-PREVIA`: la celda NO
    modula -- no se usa una posterior y no se promedia;
  · si no hay serie, `NO` -- no se inventa una.

ADENDA DE MESA, 8/sep/2026 (recibida en vuelo, precision 1). La regla
original de este acto era «ola mas cercana DISTINTA de la del arbitro
(empate -> anterior)». Con una serie que no trae ninguna ola anterior, «mas
cercana» elige una POSTERIOR: informacion que no existia en el momento que
se predice, es decir FUGA TEMPORAL. Una demostracion que la ensene ensena el
patron equivocado aunque el numero salga bien. La regla nueva es el mismo
corte que la evaluacion clasica de series hace al partir por tiempo y no al
azar.

Sigue siendo leave-one-out por construccion: la ola del arbitro queda fuera
por ser estrictamente anterior lo exigido. Usar la MISMA ola que el arbitro
haria que M y R leyeran el mismo numero, y el duelo dejaria de ser un duelo.

**ORIGEN-ARBITRO** (precision 2). Tres entradas de la serie de ENCIG traen
`metodo: "R-json (TRA-M-0X, ya publico)"`: su valor viene del `R-json` de un
duelo ya arbitrado. `F-DD` (`ADR-237`) cubre el par misma-encuesta-misma-ola
y NO cubre esa reutilizacion cruzada. Toda celda cuya ola modulada consuma
una de esas entradas queda `VERIFICACION-NO-PUNTUA`, con el rotulo en el
propio `RESULT`.

## Lo que NO hace

No promedia. No ajusta tendencias. No toca la metrica sellada de
`procedimiento-scoring-v1_2.md`. El punto de la ola LOO se emite como
DEMOSTRACION del aparato -- es modelo nuevo y va a `C0-B` con spec propia
antes de que ninguna cifra suya entre a un veredicto.

## Por que `cuenta_gen2: NO`

D-1 + regla E.1: los insumos son `milpa/tramite.yaml` (aparato GEN1) y el
marco vigente. Por completa que sea la cadena, el numero viene de GEN1.
"""
from __future__ import annotations

import csv
import io
import os
import sys

import yaml

# CUATRO `dirname`, no tres: este archivo vive en
# `data/corrida0/<CALC>/medidor.py`, asi que tres niveles llegan a `data/`
# y no a la raiz. Con tres funcionaba solo por accidente -- `corrida0` se
# invoca desde la raiz y el CWD ya estaba en `sys.path`; el dia que se
# invocara desde otro sitio, el import del motor habria reventado.
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
for _ruta in (RAIZ, os.path.join(RAIZ, "tools")):
    if _ruta not in sys.path:
        sys.path.insert(0, _ruta)

# Las dos reglas de la ADENDA viven en `tools/emite_m.py` -- donde vivira la
# envoltura por celda que las consuma en C0-D -- y se IMPORTAN, no se
# recopian: dos copias de una regla de mesa se separan en cuanto una cambia.
from emite_m import (  # noqa: E402
    ORIGEN_ARBITRO,
    SIN_PREVIA,
    VERIFICACION_NO_PUNTUA,
    anio_de_ola,
    ola_previa_estricta,
    origen_de_entrada_serie,
)

COLUMNA_ELEGIBLE = "elegible_v1_1"


def _texto(entrada: dict) -> str:
    crudo = entrada.get("bytes")
    if crudo is None:
        raise RuntimeError(f"input {entrada.get('id')!r} llego sin `bytes`")
    return crudo.decode("utf-8") if isinstance(crudo, (bytes, bytearray)) else str(crudo)


def _series_de_regla(regla: dict) -> tuple[str, list]:
    """`(donde, serie)` de una regla. La serie puede colgar de la regla o de
    una `enmienda_*` suya; se busca en las dos, en orden estable, y se
    devuelve DONDE se encontro -- no se funden dos series distintas."""
    if isinstance(regla.get("serie_olas"), list):
        return "regla", regla["serie_olas"]
    for clave in sorted(regla):
        sub = regla[clave]
        if isinstance(sub, dict) and isinstance(sub.get("serie_olas"), list):
            return clave, sub["serie_olas"]
    return "", []


def medir(inputs: dict, contrato: dict) -> dict:
    marco = list(csv.DictReader(
        io.StringIO(_texto(inputs["IN-MARCO-M-SORTEADO-V1-3"])), delimiter="\t"))
    tramite = yaml.safe_load(_texto(inputs["IN-TRAMITE"]))
    reglas = {r["id"]: r for r in tramite["reglas"]}

    salida: dict = {}
    con_serie = sin_serie = sin_previa = con_origen_arbitro = 0
    for fila in marco:
        if (fila.get(COLUMNA_ELEGIBLE) or "").strip().upper() != "SI":
            continue
        cid = fila["id"]
        regla = reglas.get(fila["regla"]) or {}
        donde, serie = _series_de_regla(regla)
        ola_arbitro = anio_de_ola(fila.get("ola"))

        if not serie or ola_arbitro is None:
            sin_serie += 1
            salida[f"RESULT-MOLA-{cid}-MODELA-OLA"] = "NO"
            continue

        elegida = ola_previa_estricta(ola_arbitro, serie)
        if elegida is None:
            # Hay serie, pero ninguna ola ANTERIOR. No se cae a la posterior:
            # eso seria fuga temporal. La celda no modula, y se dice por que.
            sin_previa += 1
            salida[f"RESULT-MOLA-{cid}-MODELA-OLA"] = (
                f"{SIN_PREVIA} · la serie de {fila['regla']}:{donde} no trae "
                f"ninguna ola anterior a {ola_arbitro}; no se usa una "
                f"posterior y no se promedia")
            continue

        con_serie += 1
        ola_usada = anio_de_ola(elegida["ola"])
        origen = origen_de_entrada_serie(elegida)
        salida[f"RESULT-MOLA-{cid}-MODELA-OLA"] = (
            f"SERIE-PREVIA · ola_usada={ola_usada} · fuente={fila['regla']}:{donde} "
            f"· ola_arbitro={ola_arbitro} · distancia={ola_arbitro - ola_usada} "
            f"· origen={origen}")
        salida[f"RESULT-MOLA-{cid}-P-LOO"] = float(elegida["p"])
        # F-DD contra la OLA USADA, no contra la del arbitro: si el punto
        # viene de 2013, la dependencia declarativa que le toca es la de
        # 2013. Anclarlo a la ola del arbitro seria puntuar un numero con el
        # ancla de otro.
        salida[f"RESULT-MOLA-{cid}-ANCLA-F-DD"] = str(ola_usada)
        # ADENDA precision 2: una entrada cuyo valor viene del R-json de un
        # duelo ya arbitrado NO puede puntuar. F-DD cubre misma-encuesta-
        # misma-ola; no cubre esta reutilizacion cruzada.
        if origen == ORIGEN_ARBITRO:
            con_origen_arbitro += 1
            salida[f"RESULT-MOLA-{cid}-GRADO-DD"] = (
                f"{VERIFICACION_NO_PUNTUA} · la ola {ola_usada} de la serie trae "
                f"metodo R-json (valor ya visto por el arbitro); F-DD (ADR-237) "
                f"no cubre la reutilizacion cruzada")
        else:
            salida[f"RESULT-MOLA-{cid}-GRADO-DD"] = "P1-PUNTUA · origen de medicion propia"

    salida["RESULT-MOLA-N-CELDAS"] = sum(
        1 for f in marco if (f.get(COLUMNA_ELEGIBLE) or "").strip().upper() == "SI")
    salida["RESULT-MOLA-N-CON-SERIE"] = con_serie
    salida["RESULT-MOLA-N-SIN-SERIE"] = sin_serie
    salida["RESULT-MOLA-N-SIN-PREVIA"] = sin_previa
    salida["RESULT-MOLA-N-ORIGEN-ARBITRO"] = con_origen_arbitro
    salida["RESULT-MOLA-ENTRADAS-ORIGEN-ARBITRO-EN-SERIES"] = ";".join(sorted(
        f"{rid}:{anio_de_ola(e['ola'])}"
        for rid, r in reglas.items()
        for e in _series_de_regla(r)[1]
        if origen_de_entrada_serie(e) == ORIGEN_ARBITRO
        and anio_de_ola(e.get("ola")) is not None)) or "ninguna"
    salida["RESULT-MOLA-REGLAS-CON-SERIE"] = ";".join(sorted(
        rid for rid, r in reglas.items() if _series_de_regla(r)[1]))
    salida["RESULT-MOLA-NO-COLAPSA"] = (
        "las 14 celdas del marco siguen siendo 14; ninguna ola se promedia, "
        "se funde ni se descarta -- D-2, firma de mesa 8/sep/2026")
    return salida
