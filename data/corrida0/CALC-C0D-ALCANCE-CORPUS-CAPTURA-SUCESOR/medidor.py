#!/usr/bin/env python3
"""Medidor de CALC-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR -- censo real sobre las
648 capturas de `corridas-L`, no muestreo de una sola (NC-0078/NC-0242).

`RESULT-C0D-ALCANCE-CORPUS-CAPTURA`, sellado en `CALC-C0D-MARCADOR` (y
heredado byte-idéntico por `-v2`/`-v3`), describe el alcance del corpus
muestreando UNA captura: `fecha_congelacion=sin-params · modelo=None`.
`NC-0078` supuso que ese `modelo=None` era artefacto del muestreo. `ACTO
GEN2-MARCADOR-C0-D` (15/sep/2026, `forense/notas/2026-09-15-GEN2-MARCADOR-
C0-D-A8-hueco.md` §4) derivó el metadato real sobre las 648 y lo dejó en
prosa, abriendo `NC-0242` porque el RESULT sellado está fuera de perímetro
(no se retoca, E.3) y ningún RESULT sucesor llegó a emitirse. Este CALC es
ese sucesor: re-deriva mecánicamente (no transcribe) los mismos conteos.

## Las tres familias de esquema

Cada captura trae, o no, dos llaves de nivel superior independientes:
`params` (metadatos del modelo que generó la réplica) y `modelo_real`
(siempre `None` donde existe). Tres familias posibles: sólo `params`, sólo
`modelo_real`, ambas. Ninguna captura carece de las dos.

## El subuniverso que el marcador consume

`CALC-C0D-MARCADOR` no lee las 648: las que traen la llave `estado_captura`
quedan fuera de su consumo (224 de 648). El subuniverso real es **424**, y
es sobre ese subuniverso -- no sobre las 648 -- que se cuenta
`modelo_id`/`fecha_congelacion`/`variante`.

## `modelo_real`

Censado aparte, sobre las 648: cuántas traen la llave y, de ésas, cuántas
NO son `None`. El hallazgo de `GEN2-MARCADOR-C0-D`: cero. `modelo_real`
vale `None` en el 100% de las capturas que lo declaran -- no es un
artefacto de muestreo, es el valor real en todo el árbol.
"""
from __future__ import annotations

import json


def _texto(entrada: dict) -> str:
    crudo = entrada.get("bytes")
    if crudo is None:
        raise RuntimeError(f"input {entrada.get('id')!r} llego sin `bytes`")
    return crudo.decode("utf-8") if isinstance(crudo, (bytes, bytearray)) else str(crudo)


def medir(inputs: dict, contrato: dict) -> dict:
    capturas = [json.loads(_texto(entrada)) for entrada in inputs.values()]
    n_total = len(capturas)

    consumidas = [c for c in capturas if "estado_captura" not in c]
    n_consumidas = len(consumidas)

    def familia(c: dict) -> str:
        tiene_params = "params" in c
        tiene_mr = "modelo_real" in c
        if tiene_params and tiene_mr:
            return "ambas"
        if tiene_params:
            return "solo_params"
        if tiene_mr:
            return "solo_modelo_real"
        return "ninguna"

    fam_648 = {"solo_params": 0, "solo_modelo_real": 0, "ambas": 0, "ninguna": 0}
    for c in capturas:
        fam_648[familia(c)] += 1

    fam_424 = {"solo_params": 0, "solo_modelo_real": 0, "ambas": 0, "ninguna": 0}
    n_modelo_id_declarado = 0
    n_modelo_id_ausente = 0
    n_fecha_0826 = 0
    n_fecha_0901 = 0
    n_fecha_ausente = 0
    n_variante_l_solo = 0
    n_variante_l_corpus = 0
    for c in consumidas:
        fam_424[familia(c)] += 1
        params = c.get("params") or {}
        modelo_id = params.get("modelo_id")
        if modelo_id == "claude-opus-4-6":
            n_modelo_id_declarado += 1
        else:
            n_modelo_id_ausente += 1
        if "params" not in c:
            n_fecha_ausente += 1
        else:
            fecha = params.get("fecha_congelacion")
            if fecha == "2026-08-26":
                n_fecha_0826 += 1
            elif fecha == "2026-09-01":
                n_fecha_0901 += 1
        variante = c.get("variante")
        if variante == "L-solo":
            n_variante_l_solo += 1
        elif variante == "L+corpus":
            n_variante_l_corpus += 1

    n_con_modelo_real = sum(1 for c in capturas if "modelo_real" in c)
    n_modelo_real_no_nulo = sum(
        1 for c in capturas if "modelo_real" in c and c["modelo_real"] is not None)

    return {
        "RESULT-C0D-ALCANCE-N-CAPTURAS-TOTAL": n_total,
        "RESULT-C0D-ALCANCE-N-CONSUMIDAS-MARCADOR": n_consumidas,
        "RESULT-C0D-ALCANCE-N-SOLO-PARAMS-648": fam_648["solo_params"],
        "RESULT-C0D-ALCANCE-N-SOLO-MODELO-REAL-648": fam_648["solo_modelo_real"],
        "RESULT-C0D-ALCANCE-N-AMBAS-648": fam_648["ambas"],
        "RESULT-C0D-ALCANCE-N-SOLO-PARAMS-424": fam_424["solo_params"],
        "RESULT-C0D-ALCANCE-N-SOLO-MODELO-REAL-424": fam_424["solo_modelo_real"],
        "RESULT-C0D-ALCANCE-N-AMBAS-424": fam_424["ambas"],
        "RESULT-C0D-ALCANCE-N-MODELO-ID-DECLARADO": n_modelo_id_declarado,
        "RESULT-C0D-ALCANCE-N-MODELO-ID-AUSENTE": n_modelo_id_ausente,
        "RESULT-C0D-ALCANCE-N-FECHA-2026-08-26": n_fecha_0826,
        "RESULT-C0D-ALCANCE-N-FECHA-2026-09-01": n_fecha_0901,
        "RESULT-C0D-ALCANCE-N-FECHA-AUSENTE": n_fecha_ausente,
        "RESULT-C0D-ALCANCE-N-VARIANTE-L-SOLO": n_variante_l_solo,
        "RESULT-C0D-ALCANCE-N-VARIANTE-L-CORPUS": n_variante_l_corpus,
        "RESULT-C0D-ALCANCE-N-CON-MODELO-REAL": n_con_modelo_real,
        "RESULT-C0D-ALCANCE-N-MODELO-REAL-NO-NULO": n_modelo_real_no_nulo,
        "RESULT-C0D-ALCANCE-CORPUS-CAPTURA-SUCESOR": (
            f"modelo_real=None en todas ({n_modelo_real_no_nulo}/{n_con_modelo_real} no nulas) · "
            f"modelo_id declarado en {n_modelo_id_declarado}/{n_consumidas} (claude-opus-4-6) · "
            f"ausente en {n_modelo_id_ausente}/{n_consumidas} -- NC-0078/NC-0242, sucesora "
            "informativa de RESULT-C0D-ALCANCE-CORPUS-CAPTURA (CALC-C0D-MARCADOR, sellado, "
            "no se retoca)"),
    }
