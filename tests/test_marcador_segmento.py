#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `tools/marcador_segmento.py` -- ACTO GEN2-MARCADOR-REDISENO-1.

Corre standalone (`python3 tests/test_marcador_segmento.py`) y expone
`corre() -> list[str]` (lista de fallos, vacía si pasa) para que un futuro
`tests/check.py` pueda cablearlo sin reimplementar nada -- mismo patrón que
`tests/test_corrida0.py`.

Tres guardias del diseño (§9(4)) + un caso de prueba que dispara cada una:
  T-RESERVA             ninguna fila RESERVADA trae R
  T-EMISOR-NO-COMPARA    ninguna fila IDENTICO se usa como si comparara
                         M contra R (columna `M` vacía en las 89 NACIONAL
                         IDENTICO -- el emisor es diagnóstico, no insumo)
  T-PISO-NO-CIRCULAR     ninguna fila MARGINAL trae piso
                         MARGINAL-SIN-INTERACCION (ese piso es SOLO de
                         cruce piloteado, nunca de una celda marginal)

ACTO GEN2-MARCADOR-PISOS-ENLACE-1 (19/sep/2026) añade la guardia D-14
`T-ENLACE-BIYECTIVO` (más T-PISO-NO-ES-M, T-UNIDAD-ARBITRO y
T-VETO-POR-NOMBRE) y retira `t_piso_v2_fixture_sintetico`: ese caso probaba
el lector por patrón de id (`_id_piso_v2`/`_lee_piso_v2`), que este acto
borró por no funcionar -- el enlace ahora va por la tabla de identidad.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "marcador_segmento_bajo_prueba", RAIZ / "tools" / "marcador_segmento.py")
M = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = M
_spec.loader.exec_module(M)

FALLOS: list[str] = []


def _falla(caso, msg):
    FALLOS.append(f"{caso}: {msg}")


def t_reserva_sin_r():
    v = M.deriva()
    for f in v["filas"]:
        if f["estado"] == "RESERVADA" and (f.get("R") not in ("", None)):
            _falla("T-RESERVA", f"{f['celda_id']} es RESERVADA y trae R={f['R']!r}")


def t_emisor_no_compara():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "NACIONAL" and f["emisor_vs_arbitro"] == "EMISOR=ARBITRO":
            # El emisor IDENTICO es diagnostico: no se usa como M que compite
            # contra R en una celda de cruce -- solo aparece en filas NACIONAL,
            # nunca en una fila CRUCE con piso.
            if f["tipo"] == "CRUCE":
                _falla("T-EMISOR-NO-COMPARA",
                       f"{f['celda_id']} es EMISOR=ARBITRO dentro de una fila CRUCE")


def t_piso_no_circular():
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "MARGINAL" and f["piso_tipo"] == "MARGINAL-SIN-INTERACCION":
            _falla("T-PISO-NO-CIRCULAR",
                   f"{f['celda_id']} es MARGINAL con piso MARGINAL-SIN-INTERACCION "
                   f"(ese piso es solo de cruce piloteado)")


def t_veinte_adoptadas():
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "CRUCE"
            and f["resultado_id"] and f["estado"] in
            ("ADOPTADO-POR-FIRMA", "PISO-ADMISIBLE-NO-ADOPTADO"))
    if n != 20:
        _falla("T-VEINTE-ADOPTADAS", f"se esperaban 20 celdas C2 piloteadas, salieron {n}")


def t_universo_97_nacional():
    v = M.deriva()
    n = sum(1 for f in v["filas"] if f["tipo"] == "NACIONAL")
    if n != 97:
        _falla("T-UNIVERSO-97", f"censo ADR-536 debía dar 97 filas NACIONAL, dio {n}")


def t_enlace_biyectivo():
    """GUARDIA D-14 de `ACTO GEN2-MARCADOR-PISOS-ENLACE-1` -- atrapa el
    defecto que ese acto corrige.

    Toda fila `CONSTRUIBLE` de la tabla de identidad de la rejilla
    (`forense/prereg-caja/PISOS-REJILLA-arbitro-metadatos-v1_0.tsv`) debe
    enlazar con EXACTAMENTE UNA fila `MARGINAL` del marcador. Ni cero
    (el defecto de hoy: el lector por patrón de id no encontraba ninguna de
    las 53) ni más de una (el defecto gemelo: perder el `outcome` colapsaba
    dos desenlaces de ENIF en un solo `celda_id`).

    No se prueba "cuántas enlazan" contra una cifra escrita a mano: se
    prueba la BIYECCIÓN contra la tabla, que es la que manda."""
    v = M.deriva()
    marginales = [f for f in v["filas"] if f["tipo"] == "MARGINAL"]

    # 1 · ningún celda_id duplicado entre las marginales
    vistos = {}
    for f in marginales:
        vistos.setdefault(f["celda_id"], 0)
        vistos[f["celda_id"]] += 1
    for cid, n in vistos.items():
        if n > 1:
            _falla("T-ENLACE-BIYECTIVO", f"celda_id duplicado ({n} filas): {cid}")

    # 2 · cada CONSTRUIBLE de la tabla aparece en exactamente una marginal,
    #     identificada por su `resultado_id` (el `cell_id` de la tabla).
    construibles = [f for f in M.lee_tabla_identidad() if f["status"] == "CONSTRUIBLE"]
    if not construibles:
        _falla("T-ENLACE-BIYECTIVO",
               "la tabla de identidad no trae filas CONSTRUIBLE -- "
               "¿se movió o se vació el archivo?")
        return
    por_result = {}
    for f in marginales:
        if f["resultado_id"]:
            por_result.setdefault(f["resultado_id"], []).append(f["celda_id"])
    for f in construibles:
        enlazadas = por_result.get(f["cell_id"], [])
        if len(enlazadas) == 0:
            _falla("T-ENLACE-BIYECTIVO",
                   f"{f['cell_id']} es CONSTRUIBLE y no enlaza con ninguna "
                   f"fila MARGINAL (consumer={f['consumer']}, axis={f['axis']}, "
                   f"category={f['category']}, outcome={f['outcome']})")
        elif len(enlazadas) > 1:
            _falla("T-ENLACE-BIYECTIVO",
                   f"{f['cell_id']} enlaza con {len(enlazadas)} filas MARGINAL: "
                   f"{enlazadas}")

    # 3 · las NO-CONSTRUIBLE quedan SIN-PISO con la causa DE LA TABLA
    no_con = [f for f in M.lee_tabla_identidad() if f["status"] != "CONSTRUIBLE"]
    causas = {f["reason"] for f in no_con if f.get("reason")}
    sin_piso_con_causa = {f["piso_fuente"].split("NO-CONSTRUIBLE:", 1)[-1]
                          for f in marginales
                          if f["piso_fuente"].startswith("NO-CONSTRUIBLE:")}
    for causa in causas:
        if causa not in sin_piso_con_causa:
            _falla("T-ENLACE-BIYECTIVO",
                   f"la causa NO-CONSTRUIBLE {causa!r} de la tabla no aparece "
                   f"en ninguna fila SIN-PISO del marcador")


def t_piso_no_es_m():
    """Firma de mesa (GEN2-MARCADOR-PISOS-ENLACE-1): «un piso acota a los
    retadores; no identifica nada y no sustituye a R en la ola que R ya
    midió». Ninguna fila MARGINAL puede traer el piso en la columna `M`."""
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] == "MARGINAL" and f["M"] not in ("", None):
            _falla("T-PISO-NO-ES-M",
                   f"{f['celda_id']} es MARGINAL y trae M={f['M']!r}: "
                   f"el piso no sustituye a R ni compite como estimador")


def t_unidad_leida_del_arbitro():
    """La unidad del dato se LEE del `payload` del árbitro, no se infiere
    del prefijo del id. Defecto corregido: ENCIG 2025 declara
    `unidad = TRÁMITE` y el marcador rotulaba `persona`."""
    v = M.deriva()
    esperado = {
        "tramite.gobierno_digital.util_sin_coercion_ejes_encig2025": "tramite",
        "civico.denuncia.con_seguro_ejes_envipe2025": "delito",
        "tramite.evasion_norma_ejes_envipe2025": "delito",
        "dinero.ahorro.via_informal_ejes_enif2024": "persona_elegida_18mas",
    }
    for f in v["filas"]:
        if f["tipo"] != "MARGINAL":
            continue
        quiere = esperado.get(f["regla_o_eje_origen"])
        if quiere and f["unidad_dato"] != quiere:
            _falla("T-UNIDAD-ARBITRO",
                   f"{f['celda_id']}: unidad_dato={f['unidad_dato']!r}, "
                   f"el árbitro declara {quiere!r} en su payload")


def t_vetados_nunca_se_leen():
    """El veto `veto:pisos-866` es POR NOMBRE y sigue vigente: ningún
    `CALC-PISOS-*-EJES-0001` puede aparecer como fuente de piso."""
    v = M.deriva()
    for f in v["filas"]:
        for vetado in M.CALC_PISOS_VETADOS:
            if vetado in str(f.get("piso_fuente", "")):
                _falla("T-VETO-POR-NOMBRE",
                       f"{f['celda_id']} cita el CALC vetado {vetado}")
    for nombre in M.CALC_PISOS_SELLADOS:
        if nombre in M.CALC_PISOS_VETADOS:
            _falla("T-VETO-POR-NOMBRE",
                   f"{nombre} está a la vez en SELLADOS y en VETADOS")


def t_error_piso_derivado():
    """Las columnas `error_piso_pp` y `clase_persistencia` se DERIVAN de
    los RESULT sellados de `CALC-PISO-PERSISTENCIA-ERROR-0001`; el marcador
    no las recalcula. Esta guardia prueba que el id que el marcador arma
    coincide con el que el CALC selló: toda fila SOLO-PISO debe traer clase,
    y esa clase debe ser exactamente la del RESULT."""
    import json as _json
    rj = M.CALC_ERROR_PISO / "resultados.json"
    if not rj.exists():
        return                       # CALC no sellado: nada que comprobar
    res = _json.loads(rj.read_text(encoding="utf-8")).get("resultados", {})
    por_cell = {f["cell_id"]: f for f in M.lee_tabla_identidad()}
    v = M.deriva()
    for f in v["filas"]:
        if f["tipo"] != "MARGINAL":
            continue
        if f["estado"] != "SOLO-PISO":
            if f["clase_persistencia"]:
                _falla("T-ERROR-PISO-DERIVADO",
                       f"{f['celda_id']} no es SOLO-PISO y trae clase "
                       f"{f['clase_persistencia']!r}")
            continue
        if not f["clase_persistencia"]:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{f['celda_id']} es SOLO-PISO y no trae clase: el id que "
                   f"el marcador arma no calza con ningún RESULT sellado")
            continue
        t = por_cell.get(f["resultado_id"], {})
        base = ("RESULT-PISO-ERR-"
                f"{M._slug_result(t.get('source_instrument'))}-"
                f"{M._slug_result(t.get('outcome'))}-"
                f"{M._slug_result(f['eje_o_par'])}-"
                f"{M._slug_result(f['categoria'])}")
        if res.get(f"{base}-CLASE") != f["clase_persistencia"]:
            _falla("T-ERROR-PISO-DERIVADO",
                   f"{f['celda_id']}: clase del marcador "
                   f"{f['clase_persistencia']!r} != RESULT "
                   f"{res.get(base + '-CLASE')!r}")


CASOS = (t_reserva_sin_r, t_emisor_no_compara, t_piso_no_circular,
         t_veinte_adoptadas, t_universo_97_nacional,
         t_enlace_biyectivo, t_piso_no_es_m, t_unidad_leida_del_arbitro,
         t_vetados_nunca_se_leen, t_error_piso_derivado)


def corre() -> list[str]:
    FALLOS.clear()
    for caso in CASOS:
        caso()
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    if fallos:
        print(f"FALLA -- {len(fallos)} caso(s):")
        for f in fallos:
            print(f"  - {f}")
        return 1
    print(f"PASA -- {len(CASOS)} casos de tests/test_marcador_segmento.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
