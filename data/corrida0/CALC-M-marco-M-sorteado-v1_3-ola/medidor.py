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

  · si la conducta de la celda trae `serie_olas`, el punto usa la **ola mas
    cercana DISTINTA de la del arbitro** (leave-one-out; empate -> la
    anterior), y se declara `SERIE-LOO · <ola>`;
  · si no la trae, se declara `NO` -- no se inventa una serie.

El leave-one-out no es decoracion: usar la MISMA ola que el arbitro haria
que M y R leyeran el mismo numero, y el duelo dejaria de ser un duelo. Es la
razon de que la regla sea «distinta a la del arbitro» y no «la mas cercana».

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

import yaml

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


def _ola_entera(valor: str) -> int | None:
    """El anio de una ola escrita como `2002 (ola 1)` o `2013`. Sin anio
    legible, `None` -- y entonces la celda no modula, se declara."""
    digitos = ""
    for ch in str(valor):
        if ch.isdigit():
            digitos += ch
            if len(digitos) == 4:
                return int(digitos)
        else:
            digitos = ""
    return None


def _loo(ola_arbitro: int, serie: list) -> dict | None:
    """La entrada de la serie mas cercana a `ola_arbitro` y DISTINTA de ella.

    Empate -> la ANTERIOR (la de anio menor). Es una regla de desempate
    declarada, no el orden en que el YAML las trajo.
    """
    candidatas = [e for e in serie
                  if isinstance(e, dict) and _ola_entera(e.get("ola")) is not None
                  and _ola_entera(e.get("ola")) != ola_arbitro]
    if not candidatas:
        return None
    return min(candidatas,
               key=lambda e: (abs(_ola_entera(e["ola"]) - ola_arbitro),
                              _ola_entera(e["ola"])))


def medir(inputs: dict, contrato: dict) -> dict:
    marco = list(csv.DictReader(
        io.StringIO(_texto(inputs["IN-MARCO-M-SORTEADO-V1-3"])), delimiter="\t"))
    tramite = yaml.safe_load(_texto(inputs["IN-TRAMITE"]))
    reglas = {r["id"]: r for r in tramite["reglas"]}

    salida: dict = {}
    con_serie = sin_serie = 0
    for fila in marco:
        if (fila.get(COLUMNA_ELEGIBLE) or "").strip().upper() != "SI":
            continue
        cid = fila["id"]
        regla = reglas.get(fila["regla"]) or {}
        donde, serie = _series_de_regla(regla)
        ola_arbitro = _ola_entera(fila.get("ola"))
        elegida = _loo(ola_arbitro, serie) if (serie and ola_arbitro is not None) else None

        if elegida is None:
            sin_serie += 1
            salida[f"RESULT-MOLA-{cid}-MODELA-OLA"] = "NO"
            continue

        con_serie += 1
        ola_usada = _ola_entera(elegida["ola"])
        salida[f"RESULT-MOLA-{cid}-MODELA-OLA"] = (
            f"SERIE-LOO · ola_usada={ola_usada} · fuente={fila['regla']}:{donde} "
            f"· ola_arbitro={ola_arbitro} · distancia={abs(ola_usada - ola_arbitro)}")
        salida[f"RESULT-MOLA-{cid}-P-LOO"] = float(elegida["p"])
        # F-DD contra la OLA USADA, no contra la del arbitro: si el punto
        # viene de 2013, la dependencia declarativa que le toca es la de
        # 2013. Anclarlo a la ola del arbitro seria puntuar un numero con el
        # ancla de otro.
        salida[f"RESULT-MOLA-{cid}-ANCLA-F-DD"] = str(ola_usada)

    salida["RESULT-MOLA-N-CELDAS"] = sum(
        1 for f in marco if (f.get(COLUMNA_ELEGIBLE) or "").strip().upper() == "SI")
    salida["RESULT-MOLA-N-CON-SERIE"] = con_serie
    salida["RESULT-MOLA-N-SIN-SERIE"] = sin_serie
    salida["RESULT-MOLA-REGLAS-CON-SERIE"] = ";".join(sorted(
        rid for rid, r in reglas.items() if _series_de_regla(r)[1]))
    salida["RESULT-MOLA-NO-COLAPSA"] = (
        "las 14 celdas del marco siguen siendo 14; ninguna ola se promedia, "
        "se funde ni se descarta -- D-2, firma de mesa 8/sep/2026")
    return salida
