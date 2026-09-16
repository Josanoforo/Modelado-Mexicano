#!/usr/bin/env python3
"""Medidor de CALC-AGG-marco-M-sorteado-v1_3-ola-v3 -- dos vistas, cero colapso,
mas el filtro de IC95 que su nombre promete (NC-0241).

`ACTO GEN2-T9 · EL MOTOR ES LA MATRIZ`, P3(d)/(e), mas la ADENDA DE MESA del
8/sep/2026.

Sucesora de `CALC-AGG-marco-M-sorteado-v1_3-ola-v2` (`repite_de`, sellada,
bytes intactos, NO se toca): mismos tres inputs, mismo universo. Unica
diferencia mecanica, medida por `ACTO GEN2-MARCADOR-C0-D` (15/sep/2026,
`NC-0241`) sobre el RESULT de v2: `RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC`
contaba `len(e["celdas"])` de cada entrada `_ejes_` sin mirar si esa celda
trae `ic95` -- su propio nombre («CON-IC») prometia un filtro que el codigo
no aplicaba. De las 74 celdas de v2, 64 SI traen `ic95` y 10 NO (una sola
entrada, un solo eje: `familia.cuidado.reparto_mujeres40_ejes_enut2024`,
eje `sexo_edad`, descriptivo por diseno -- ver `nota` de esa entrada en
`milpa/tramite-ola5-propuesta-v0.yaml`). Este medidor filtra de verdad y
publica las tres cifras por separado, para que la proxima cita no vuelva a
tener que elegir cual de las tres quiso decir «puntos con IC».

Sucesora original, dos niveles atras, de `CALC-AGG-marco-M-sorteado-v1_3-ola`:
consume los `RESULT` de `CALC-M-marco-M-sorteado-v1_3-ola-v2`, cuyo rotulo de
modulacion es `SERIE-PREVIA` (la predecesora emitia `SERIE-LOO`, regla
derogada). Las dos predecesoras quedan SUPERADAS y sus bytes intactos.

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
    n_puntos_eje_total = 0
    n_puntos_eje_con_ic = 0
    n_puntos_eje_sin_ic = 0
    ejes_sin_ic: set[str] = set()
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
                celdas = e.get("celdas") or []
                n_puntos_eje_total += len(celdas)
                for c in celdas:
                    # NC-0241: el filtro que el nombre RESULT promete -- sin
                    # el `is not None`, `ic95: null` (YAML/JSON) pasaba igual
                    # que un IC real. `[lo, hi]` cuenta; `null` no.
                    if isinstance(c, dict) and c.get("ic95") is not None:
                        n_puntos_eje_con_ic += 1
                    else:
                        n_puntos_eje_sin_ic += 1
                        eje_id = f"{r.get('id')}/{e.get('eje')}"
                        ejes_sin_ic.add(eje_id)

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
        # NC-0241: ahora SI filtra por `ic95 is not None` -- v2 contaba las
        # 74 sin mirar el campo; aqui son 64. `-TOTAL`/`-SIN-IC` publicados
        # aparte para que ninguna cita futura tenga que adivinar cual de las
        # tres cifras quiso decir "puntos con IC".
        "RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC": n_puntos_eje_con_ic,
        "RESULT-AGGOLA-PUNTOS-POR-EJE-SIN-IC": n_puntos_eje_sin_ic,
        "RESULT-AGGOLA-PUNTOS-POR-EJE-TOTAL": n_puntos_eje_total,
        "RESULT-AGGOLA-EJES-SIN-IC": ";".join(sorted(ejes_sin_ic)),
        "RESULT-AGGOLA-METRICA-SELLADA": (
            "INTACTA -- procedimiento-scoring-v1_2.md y agregado-v1_3-resultado.json "
            "no se leen ni se reescriben aqui; estas dos vistas son informativas y "
            "no entran a ningun veredicto"),
        "RESULT-AGGOLA-HUECO": (
            f"{n_puntos_eje_con_ic} puntos por eje CON ic95 (de {n_puntos_eje_total} "
            f"totales; {n_puntos_eje_sin_ic} sin ic95, descriptivos por diseno: "
            f"{';'.join(sorted(ejes_sin_ic)) or 'ninguno'}) existen del lado del "
            f"arbitro (en {len(entradas_ejes)} entradas `_ejes_` SELLADAS de la "
            f"propuesta) y {celdas_con_segmento} celdas del marcador los consumen: "
            f"el hueco es de cableado, no de dato -- NC-0020"),
        "RESULT-AGGOLA-CORRECCION-NC-0241": (
            "v2 (RESULT-AGGOLA-PUNTOS-POR-EJE-CON-IC=74, sellado, no se toca) contaba "
            "len(celdas) de cada entrada _ejes_ sin mirar `ic95` -- su propio nombre "
            "prometia un filtro que el codigo no aplicaba (medido por ACTO "
            "GEN2-MARCADOR-C0-D, 15/sep/2026). Este CALC (v3) filtra: 64 CON ic95, "
            "10 SIN (familia.cuidado.reparto_mujeres40_ejes_enut2024/sexo_edad, "
            "descriptivo por diseno, sin signo pre-registrado). El RESULT sellado "
            "de v2 no se retoca (E.3); este es el sucesor que NC-0241 pedia."),
    }
