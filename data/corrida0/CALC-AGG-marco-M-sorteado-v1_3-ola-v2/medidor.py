#!/usr/bin/env python3
"""Medidor de CALC-AGG-marco-M-sorteado-v1_3-ola-v2 -- dos vistas, cero colapso.

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, P3(d)/(e), mas la ADENDA DE MESA del
8/sep/2026.

Sucesora de `CALC-AGG-marco-M-sorteado-v1_3-ola` (`repite_de`): consume los
`RESULT` de `CALC-M-marco-M-sorteado-v1_3-ola-v2`, cuyo rotulo de modulacion
es `SERIE-PREVIA` (la predecesora emitia `SERIE-LOO`, regla derogada). La
predecesora queda SUPERADA y sus bytes intactos.

## La metrica sellada NO se toca

`procedimiento-scoring-v1_2.md` y `agregado-v1_3-resultado.json` quedan
exactamente como estan. Este agregado **añade** dos vistas INFORMATIVAS --
por regla y por segmento -- y no sustituye ninguna cifra de veredicto. Una
vista informativa que se cuela al veredicto es como se pierde un
pre-registro.

## Vista 1 · por regla

Agrupa las celdas del marco por su `regla` de `tramite.yaml` y reporta
cuantas modulan por ola y cuantas no. NO promedia los puntos de las celdas
de una regla: reportar una mediana por regla seria colapsar por la puerta de
atras. Se cuentan celdas, no se funden numeros.

## Vista 2 · por segmento -- y por que sale vacia

La celda del marcador es, por decision de este acto,
`regla x segmento (x, sobre los seis ejes del modelo) x ola x instrumento`.
Las 14 celdas de hoy son el caso `x = vacio`. La dimension que falta es el
SEGMENTO, y la vista lo reporta con su cifra: **cero** celdas del marcador
con `x != vacio`.

Lo que hace informativa a esa vista vacia es el otro lado del conteo: la
propuesta `milpa/tramite-ola5-propuesta-v0.yaml` SI trae puntos por eje con
IC95 -- entradas `_ejes_`, todas `SELLADA` -- que NINGUNA celda del marcador
consume. El hueco no es falta de dato: es falta de cableado, y esta corrida
lo mide en vez de describirlo.

## Por que `cuenta_gen2: NO`

Cadena: consume los RESULT de `CALC-M-marco-M-sorteado-v1_3-ola`, que es
corredor envuelto LEGACY. La regla E.1 es transitiva por construccion.
"""
from __future__ import annotations

import csv
import io
import json

import yaml

COLUMNA_ELEGIBLE = "elegible_v1_1"


def _texto(entrada: dict) -> str:
    crudo = entrada.get("bytes")
    if crudo is None:
        raise RuntimeError(f"input {entrada.get('id')!r} llego sin `bytes`")
    return crudo.decode("utf-8") if isinstance(crudo, (bytes, bytearray)) else str(crudo)


def _results_de(entrada: dict) -> dict:
    return json.loads(_texto(entrada)).get("resultados", {})


def medir(inputs: dict, contrato: dict) -> dict:
    marco = list(csv.DictReader(
        io.StringIO(_texto(inputs["IN-MARCO-M-SORTEADO-V1-3"])), delimiter="\t"))
    elegibles = [f for f in marco
                 if (f.get(COLUMNA_ELEGIBLE) or "").strip().upper() == "SI"]
    res_ola = _results_de(inputs["IN-CALC-M-OLA-RESULTADOS"])
    propuesta = yaml.safe_load(_texto(inputs["IN-PROPUESTA-OLA5"]))

    # ── Vista 1 · por regla ───────────────────────────────────────────────
    por_regla: dict[str, dict] = {}
    for fila in elegibles:
        r = por_regla.setdefault(fila["regla"], {"celdas": 0, "modulan": 0, "sin_previa": 0})
        r["celdas"] += 1
        marca = str(res_ola.get(f"RESULT-MOLA-{fila['id']}-MODELA-OLA", "NO"))
        if marca.startswith("SERIE-PREVIA"):
            r["modulan"] += 1
        elif marca.startswith("SIN-PREVIA"):
            r["sin_previa"] = r.get("sin_previa", 0) + 1
    vista_regla = ";".join(
        f"{rid}:celdas={v['celdas']},modulan={v['modulan']},"
        f"sin_previa={v.get('sin_previa', 0)}"
        for rid, v in sorted(por_regla.items()))

    # ── Vista 2 · por segmento ────────────────────────────────────────────
    # El marco vigente no tiene columna de segmento: NINGUNA de sus celdas
    # porta un vector de atributos. Se comprueba contra el esquema, no se
    # supone.
    columnas = set(marco[0]) if marco else set()
    tiene_columna_segmento = bool(columnas & {"segmento", "x", "ejes"})
    celdas_con_segmento = 0  # por construccion, mientras no exista la columna

    # El otro lado del conteo: los puntos por eje que SI existen.
    entradas_ejes = [r for r in (propuesta.get("reglas_propuestas") or [])
                     if "_ejes_" in str(r.get("id", ""))]
    n_ejes = 0
    n_puntos_eje = 0
    for r in entradas_ejes:
        listas = []
        if isinstance(r.get("ejes"), list):
            listas.append(r["ejes"])
        for dv in (r.get("desenlaces") or {}).values():
            if isinstance(dv, dict) and isinstance(dv.get("ejes"), list):
                listas.append(dv["ejes"])
        for lista in listas:
            n_ejes += len(lista)
            for e in lista:
                n_puntos_eje += len(e.get("celdas") or [])

    return {
        "RESULT-AGGOLA-N-CELDAS": len(elegibles),
        "RESULT-AGGOLA-N-MODULAN-OLA": sum(
            1 for f in elegibles
            if str(res_ola.get(f"RESULT-MOLA-{f['id']}-MODELA-OLA", "")).startswith("SERIE-PREVIA")),
        # ADENDA precision 1: las celdas que NO modulan por falta de ola
        # anterior se cuentan aparte de las que no tienen serie. Fundirlas
        # escondería exactamente el caso que la regla existe para marcar.
        "RESULT-AGGOLA-N-SIN-PREVIA": sum(
            1 for f in elegibles
            if str(res_ola.get(f"RESULT-MOLA-{f['id']}-MODELA-OLA", "")).startswith("SIN-PREVIA")),
        # ADENDA precision 2: celdas cuya ola usada es ORIGEN-ARBITRO y por
        # tanto NO puntuan.
        "RESULT-AGGOLA-N-VERIFICACION-NO-PUNTUA": sum(
            1 for f in elegibles
            if "VERIFICACION-NO-PUNTUA" in str(
                res_ola.get(f"RESULT-MOLA-{f['id']}-GRADO-DD", ""))),
        "RESULT-AGGOLA-VISTA-POR-REGLA": vista_regla,
        "RESULT-AGGOLA-N-REGLAS": len(por_regla),
        "RESULT-AGGOLA-CELDAS-CON-SEGMENTO": celdas_con_segmento,
        "RESULT-AGGOLA-MARCO-TIENE-COLUMNA-SEGMENTO": "SI" if tiene_columna_segmento else "NO",
        "RESULT-AGGOLA-ENTRADAS-EJES-EN-PROPUESTA": len(entradas_ejes),
        "RESULT-AGGOLA-EJES-EN-PROPUESTA": n_ejes,
        "RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC": n_puntos_eje,
        "RESULT-AGGOLA-METRICA-SELLADA": (
            "INTACTA -- procedimiento-scoring-v1_2.md y agregado-v1_3-resultado.json "
            "no se leen ni se reescriben aqui; estas dos vistas son informativas y "
            "no entran a ningun veredicto"),
        "RESULT-AGGOLA-HUECO": (
            f"{n_puntos_eje} puntos por eje con IC95 existen del lado del arbitro "
            f"(en {len(entradas_ejes)} entradas `_ejes_` SELLADAS de la propuesta) y "
            f"{celdas_con_segmento} celdas del marcador los consumen: el hueco es de "
            f"cableado, no de dato -- NC-0020"),
    }
