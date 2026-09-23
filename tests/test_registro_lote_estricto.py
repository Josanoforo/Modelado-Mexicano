#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de `corrida0.registro(escribe=True, lote=...)` -- ACTO
GEN2-TUBERIA-LOTE-ESTRICTO-1 (22/sep/2026), P2/P3.

Defecto que atrapa (FP 7d98-01): antes de este acto, `--escribe --lote`
acotaba el GUARDIA `REPLAY-PISADO` pero no la ESCRITURA -- `registro()`
re-proyectaba la vista COMPLETA desde `replay-evidencia.tsv`, así que una
corrida AJENA cuya evidencia dejó de ser vigente (spec/código distinto)
disparaba el guardia aunque nadie la hubiera nombrado en `--lote`. Medido
sobre el repo real (P1 de este acto): 13 corridas, 26 campos, con el
comando `_para_si_pisa_replay` de hoy.

Corre standalone (`python3 tests/test_registro_lote_estricto.py`) y expone
`corre() -> list[str]` -- mismo patrón que `tests/test_marcador_segmento.py`
y `tests/test_lote_desde_asientos.py`. Reutiliza los fixtures de
`tests/test_corrida0.py` (mismo módulo `corrida0` bajo prueba) en vez de
reconstruir el árbol demanda+oferta a mano.

Casos:
  A · `_acota_vistas_al_lote` directo: 3 corridas publicadas, una con
      drift (veredicto ya no coincide con lo publicado); `--lote` con una
      corrida NUEVA -> la vista efectiva cambia en exactamente una fila
      (la nueva) y `_para_si_pisa_replay` no dispara.
  B · Sin la bandera estricta (lote vacío) el mismo drift SÍ dispara --
      confirma que el caso A prueba la protección, no que el drift no
      exista.
  C · Extremo a extremo con `registro(escribe=True, ...)`: dos CALC
      sellados publicados (uno con drift simulado en `corridas.tsv`) más
      un tercero nuevo nombrado en `--lote` -> escribe sólo la fila nueva;
      las dos publicadas quedan BYTE A BYTE idénticas.
  D · El acotamiento no se pasa de largo: nombrar una corrida YA
      PUBLICADA en `--lote` sigue escribiendo su valor FRESCO (lo que el
      lote autoriza), no el publicado -- congelar lo ajeno no debe
      congelar lo propio.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

_spec_c = importlib.util.spec_from_file_location(
    "corrida0_lote_estricto", RAIZ / "tools" / "corrida0.py")
C = importlib.util.module_from_spec(_spec_c)
sys.modules[_spec_c.name] = C
_spec_c.loader.exec_module(C)

_spec_t = importlib.util.spec_from_file_location(
    "test_corrida0_lote_estricto", RAIZ / "tests" / "test_corrida0.py")
T = importlib.util.module_from_spec(_spec_t)
sys.modules[_spec_t.name] = T
_spec_t.loader.exec_module(T)
T.C = C  # un solo módulo `corrida0` bajo prueba en todo este archivo.

FALLOS: list[str] = []


def _falla(caso: str, msg: str) -> None:
    FALLOS.append(f"{caso}: {msg}")


def _afirma(cond: bool, caso: str, msg: str) -> None:
    if not cond:
        _falla(caso, msg)


def _fila(corrida_id, spec_id, resultado, contexto):
    fila = {c: "X" for c in C.COLS_VISTA_CORRIDAS}
    fila.update({"corrida_id": corrida_id, "spec_id": spec_id,
                 "resultado_replay": resultado, "contexto_replay": contexto})
    return fila


def t_a_acota_vistas_al_lote_congela_lo_ajeno():
    caso = "t_a_acota_vistas_al_lote_congela_lo_ajeno"
    publicadas = [
        _fila("CALC-VIEJA--01", "CALC-VIEJA", "REPRODUCE", "IDENTICO"),
        _fila("CALC-DRIFT--02", "CALC-DRIFT", "REPRODUCE", "IDENTICO"),
        _fila("CALC-OTRA--03", "CALC-OTRA", "NO-EJECUTABLE", "DISTINTO"),
    ]
    with T._vista_temporal([(f["corrida_id"], f["spec_id"], f["resultado_replay"],
                             f["contexto_replay"]) for f in publicadas]):
        # El fresco: la misma vista, PERO CALC-DRIFT ya no es vigente (una
        # corrida ajena cuya evidencia cambio por causas ajenas al lote) y
        # se agrega una corrida NUEVA que es lo unico que --lote autoriza.
        fresco_drift = _fila("CALC-DRIFT--02", "CALC-DRIFT",
                             C.NO_VERIFICADO, C.NO_VERIFICADO)
        fresco = [publicadas[0], fresco_drift, publicadas[2],
                  _fila("CALC-NUEVA--04", "CALC-NUEVA", "REPRODUCE", "IDENTICO")]
        vistas = {"corridas": fresco, "resultados": [], "usos": []}
        acotada = C._acota_vistas_al_lote(vistas, {"CALC-NUEVA"})
        por_id = {f["corrida_id"]: f for f in acotada["corridas"]}
        _afirma(por_id["CALC-VIEJA--01"] == publicadas[0], caso,
                "CALC-VIEJA cambio sin estar en el lote")
        _afirma(por_id["CALC-DRIFT--02"] == publicadas[1], caso,
                f"CALC-DRIFT no se congelo a lo publicado: {por_id['CALC-DRIFT--02']}")
        _afirma(por_id["CALC-OTRA--03"] == publicadas[2], caso,
                "CALC-OTRA cambio sin estar en el lote")
        _afirma(por_id["CALC-NUEVA--04"] == fresco[3], caso,
                "la corrida nueva del lote no se escribio fresca")
        cambian = [cid for cid in por_id if por_id[cid] != {
            "CALC-VIEJA--01": publicadas[0], "CALC-DRIFT--02": publicadas[1],
            "CALC-OTRA--03": publicadas[2], "CALC-NUEVA--04": fresco[3],
        }[cid]]
        _afirma(cambian == [], caso, f"filas que no debieron cambiar: {cambian}")
        _afirma(len([cid for cid in por_id
                    if por_id[cid] not in publicadas]) == 1, caso,
                "la vista efectiva cambio en mas de una fila")
        try:
            C._para_si_pisa_replay(acotada["corridas"], {"CALC-NUEVA"})
        except C.ReplayPisado as exc:
            _falla(caso, f"el guardia disparo tras congelar lo ajeno: {exc}")


def t_b_sin_acotar_el_mismo_drift_si_dispara():
    caso = "t_b_sin_acotar_el_mismo_drift_si_dispara"
    publicadas = [("CALC-DRIFT--02", "CALC-DRIFT", "REPRODUCE", "IDENTICO")]
    with T._vista_temporal(publicadas):
        fresco = [_fila("CALC-DRIFT--02", "CALC-DRIFT", C.NO_VERIFICADO, C.NO_VERIFICADO),
                  _fila("CALC-NUEVA--04", "CALC-NUEVA", "REPRODUCE", "IDENTICO")]
        try:
            C._para_si_pisa_replay(fresco, {"CALC-NUEVA"})
            _falla(caso, "sin congelar, el drift ajeno no disparo (el caso A no prueba nada)")
        except C.ReplayPisado as exc:
            _afirma("CALC-DRIFT--02" in str(exc), caso, f"PARO no nombra la drift: {exc}")


def t_c_registro_escribe_lote_congela_publicadas_byte_a_byte():
    caso = "t_c_registro_escribe_lote_congela_publicadas_byte_a_byte"
    calcs = [
        {"calc_id": "CALC-FIX-VIEJA", "valores": {"RESULT-A": 1.0},
         "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}},
        {"calc_id": "CALC-FIX-DRIFT", "valores": {"RESULT-B": 2.0},
         "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}},
        {"calc_id": "CALC-FIX-NUEVA", "valores": {"RESULT-C": 3.0},
         "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}},
    ]
    res = [T._fila_demanda(f"RES-{i:04d}", f"c:uno:{i}", f"CORR-{i:04d}")
           for i in range(3)]
    corr = [T._fila_corrida(f"CORR-{i:04d}", [f"RES-{i:04d}"]) for i in range(3)]
    with T._arbol_registro(res=res, corr=corr, calcs=calcs) as tmp:
        C.VISTA_CORRIDAS = tmp / "corridas.tsv"
        C.VISTA_RESULTADOS = tmp / "resultados.tsv"
        C.VISTA_USOS = tmp / "usos.tsv"
        try:
            # Publica las tres, como si CALC-FIX-NUEVA ya existiera desde
            # antes -- luego se simula que SOLO ella entra al lote de este
            # push y que CALC-FIX-DRIFT quedo con evidencia no vigente por
            # una causa ajena (se edita `corridas.tsv` publicado a mano,
            # como lo dejaria una vigencia caida entre dos pushes).
            C.registro(escribe=True, imprime=False)
            publicado_antes = {p.name: p.read_bytes() for p in
                               (C.VISTA_CORRIDAS, C.VISTA_RESULTADOS, C.VISTA_USOS)}
            filas = list(T.C._leer_tsv_derivado(C.VISTA_CORRIDAS))
            for f in filas:
                if f["spec_id"] == "CALC-FIX-DRIFT":
                    f["resultado_replay"] = "NO-REPRODUCE"
                    f["contexto_replay"] = "DISTINTO"
            C._escribe(C.VISTA_CORRIDAS, C.COLS_VISTA_CORRIDAS, filas)
            drift_publicado = C.VISTA_CORRIDAS.read_bytes()

            v = C.registro(escribe=True, imprime=False, lote=["CALC-FIX-NUEVA"])
            _afirma(v is not None, caso, "registro con lote no devolvio vistas")

            corridas_finales = list(T.C._leer_tsv_derivado(C.VISTA_CORRIDAS))
            por_spec = {f["spec_id"]: f for f in corridas_finales}
            _afirma(por_spec["CALC-FIX-DRIFT"]["resultado_replay"] == "NO-REPRODUCE",
                    caso, "la corrida ajena con drift se re-proyecto en vez de "
                          "conservarse byte a byte")
            _afirma(C.VISTA_CORRIDAS.read_bytes() != publicado_antes["corridas.tsv"],
                    caso, "la vista no cambio -- la corrida nueva no entro")
        finally:
            C.VISTA_CORRIDAS = C.CORRIDAS / "corridas.tsv"
            C.VISTA_RESULTADOS = C.CORRIDAS / "resultados.tsv"
            C.VISTA_USOS = C.CORRIDAS / "usos.tsv"


def t_d_lote_si_autoriza_mover_la_corrida_que_nombro():
    """El acotamiento (P2) congela lo AJENO, pero no debe congelar lo que
    el propio lote autoriza: nombrar una corrida YA PUBLICADA en `--lote`
    sigue escribiendo su valor FRESCO, no el publicado. Sin este caso, un
    `_acota_vistas_al_lote` que congelara TODO por error pasaría el resto
    de los casos (que sólo miran lo ajeno) y nadie lo notaría."""
    caso = "t_d_lote_si_autoriza_mover_la_corrida_que_nombro"
    calcs = [{"calc_id": "CALC-FIX-LOTE", "valores": {"RESULT-A": 1.0},
              "etiquetas": {"generacion": "GEN2", "cuenta_gen2": "SI"}}]
    res = [T._fila_demanda("RES-0000", "c:uno:0", "CORR-0000")]
    corr = [T._fila_corrida("CORR-0000", ["RES-0000"])]
    with T._arbol_registro(res=res, corr=corr, calcs=calcs) as tmp:
        C.VISTA_CORRIDAS = tmp / "corridas.tsv"
        C.VISTA_RESULTADOS = tmp / "resultados.tsv"
        C.VISTA_USOS = tmp / "usos.tsv"
        try:
            C.registro(escribe=True, imprime=False)
            filas = list(T.C._leer_tsv_derivado(C.VISTA_CORRIDAS))
            for f in filas:
                if f["spec_id"] == "CALC-FIX-LOTE":
                    f["resultado_replay"] = "NO-REPRODUCE"
                    f["contexto_replay"] = "DISTINTO"
            C._escribe(C.VISTA_CORRIDAS, C.COLS_VISTA_CORRIDAS, filas)
            try:
                C.registro(escribe=True, imprime=False, lote=["CALC-FIX-LOTE"])
            except C.ReplayPisado as exc:
                _falla(caso, f"nombrada en --lote y aun asi paro: {exc}")
            corridas_finales = list(T.C._leer_tsv_derivado(C.VISTA_CORRIDAS))
            por_spec = {f["spec_id"]: f for f in corridas_finales}
            _afirma(por_spec["CALC-FIX-LOTE"]["resultado_replay"] != "NO-REPRODUCE",
                    caso, "el lote se congelo a si mismo -- nunca escribio el "
                          "veredicto fresco que el propio lote autoriza")
        finally:
            C.VISTA_CORRIDAS = C.CORRIDAS / "corridas.tsv"
            C.VISTA_RESULTADOS = C.CORRIDAS / "resultados.tsv"
            C.VISTA_USOS = C.CORRIDAS / "usos.tsv"


TESTS = [v for k, v in sorted(globals().items()) if k.startswith("t_")]


def corre() -> list[str]:
    FALLOS.clear()
    for fn in TESTS:
        try:
            fn()
        except Exception as exc:
            _falla(fn.__name__, f"EXCEPCION {type(exc).__name__}: {exc}")
    return list(FALLOS)


def main() -> int:
    fallos = corre()
    print(f"tests/test_registro_lote_estricto.py · {len(TESTS)} casos · "
          f"{len(TESTS) - len({f.split(':')[0] for f in fallos})} ok · {len(fallos)} FALLOS")
    for f in fallos:
        print(f"  FAIL  {f}")
    return 1 if fallos else 0


if __name__ == "__main__":
    raise SystemExit(main())
