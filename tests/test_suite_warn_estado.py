#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de `suite:WARN-nuevos-son-estado` (`data/corrida0/decisiones.tsv`,
firma de mesa 16/sep/2026, ADR-534, ACTO GEN2-MANTENIMIENTO-4) --
`tests/check.py --baseline` adjudica ROJO/VERDE solo por FAIL nuevos; un
WARN nuevo se lista aparte (estado, no adjudica) y nunca vuelve ROJA una
corrida que antes era VERDE.

- `prueba_warn_nuevo_no_pone_rojo` -- ejercita `check._baseline_compare()`
  real contra un `tests/baseline.json` temporal (nunca el real): un FAIL
  ya conocido se repite (VERDE por FAIL), y aparece un WARN nuevo que no
  estaba congelado. El veredicto debe seguir VERDE, y el WARN nuevo debe
  aparecer bajo el rótulo separado "WARN NUEVOS (estado, no adjudican)".
- `prueba_fail_nuevo_si_pone_rojo` -- control positivo: un FAIL nuevo
  frente a la línea base sí debe volver ROJA la comparación, para que la
  prueba anterior no pase por construcción (adjudicar solo por FAIL no es
  lo mismo que no adjudicar nunca).
- `prueba_archivo_neutro_no_mueve_veredicto` -- huella P3: añadir un
  archivo neutro a `forense/digesto/` (un directorio que ningún test de
  `check.py` escanea hoy) no cambia qué entra a FAILS/WARNS, así que no
  puede mover el veredicto de `--baseline`. Corrida antes/después
  contra la misma línea base temporal, con el archivo creado y borrado
  dentro de la propia prueba (nunca deja rastro en el árbol real).

Corre sola:

    python3 tests/test_suite_warn_estado.py
"""
import io
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check as C  # noqa: E402

ROOT = C.ROOT
FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def _con_estado_limpio(fn):
    """Corre `fn()` con FAILS/WARNS/SENAL/BASELINE_PATH de `check` vacíos y
    apuntando a un fixture temporal, y los restaura al terminar -- el mismo
    patrón que `tests/test_t_cron.py::prueba_senal_no_genera_delta_baseline`
    usa para no tocar el `tests/baseline.json` real."""
    fails_bak, warns_bak, senal_bak = C.FAILS[:], C.WARNS[:], C.SENAL[:]
    baseline_path_bak = C.BASELINE_PATH
    C.FAILS.clear()
    C.WARNS.clear()
    C.SENAL.clear()
    try:
        fn()
    finally:
        C.FAILS[:] = fails_bak
        C.WARNS[:] = warns_bak
        C.SENAL[:] = senal_bak
        C.BASELINE_PATH = baseline_path_bak


def _corre_baseline_compare():
    salida = io.StringIO()
    sys_stdout_bak = sys.stdout
    sys.stdout = salida
    try:
        codigo = C._baseline_compare()
    finally:
        sys.stdout = sys_stdout_bak
    return codigo, salida.getvalue()


def prueba_warn_nuevo_no_pone_rojo():
    def cuerpo():
        with tempfile.TemporaryDirectory() as td:
            baseline_tmp = os.path.join(td, "baseline.json")
            with io.open(baseline_tmp, "w", encoding="utf-8") as f:
                json.dump({
                    "head": "0000000",
                    "fails": [["T-X", "fallo ya conocido"]],
                    "warns": [],
                    "nota": "fixture de prueba, sin WARN conocido",
                }, f)
            C.BASELINE_PATH = baseline_tmp

            C.fail("T-X", "fallo ya conocido")
            C.warn("T-Y", "warn nuevo, no congelado")

            codigo, salida = _corre_baseline_compare()

            afirma(codigo == 0,
                   f"un WARN nuevo no debe volver ROJO --baseline (código {codigo}); "
                   f"salida:\n{salida}")
            afirma("LÍNEA BASE: VERDE" in salida,
                   f"se esperaba VERDE (el único FAIL ya estaba congelado); salida:\n{salida}")
            afirma("WARN NUEVOS (estado, no adjudican): 1" in salida,
                   f"el WARN nuevo debe listarse bajo el rótulo separado; salida:\n{salida}")
            afirma("T-Y" in salida,
                   f"el WARN nuevo debe nombrar su test de origen; salida:\n{salida}")
    _con_estado_limpio(cuerpo)


def prueba_fail_nuevo_si_pone_rojo():
    def cuerpo():
        with tempfile.TemporaryDirectory() as td:
            baseline_tmp = os.path.join(td, "baseline.json")
            with io.open(baseline_tmp, "w", encoding="utf-8") as f:
                json.dump({"head": "0000000", "fails": [], "warns": [],
                           "nota": "fixture de prueba, sin FAIL conocido"}, f)
            C.BASELINE_PATH = baseline_tmp

            C.fail("T-Z", "fallo nuevo, no congelado")

            codigo, salida = _corre_baseline_compare()

            afirma(codigo == 1,
                   f"un FAIL nuevo sí debe volver ROJO --baseline (código {codigo}); "
                   f"salida:\n{salida}")
            afirma("LÍNEA BASE: ROJO" in salida, f"se esperaba ROJO; salida:\n{salida}")
    _con_estado_limpio(cuerpo)


def prueba_archivo_neutro_no_mueve_veredicto():
    digesto_dir = os.path.join(ROOT, "forense", "digesto")
    neutro = os.path.join(digesto_dir, "_prueba_suite_warn_estado_neutro.tmp")
    afirma(not os.path.exists(neutro),
           f"el fixture no debe preexistir -- limpieza previa incompleta: {neutro}")

    def cuerpo():
        with tempfile.TemporaryDirectory() as td:
            baseline_tmp = os.path.join(td, "baseline.json")
            with io.open(baseline_tmp, "w", encoding="utf-8") as f:
                json.dump({"head": "0000000", "fails": [], "warns": [],
                           "nota": "fixture de prueba, arbol sin el archivo neutro"}, f)
            C.BASELINE_PATH = baseline_tmp

            codigo_antes, salida_antes = _corre_baseline_compare()

            os.makedirs(digesto_dir, exist_ok=True)
            with io.open(neutro, "w", encoding="utf-8") as f:
                f.write("archivo neutro de prueba -- P3 GEN2-MANTENIMIENTO-4\n")
            try:
                codigo_despues, salida_despues = _corre_baseline_compare()
            finally:
                os.remove(neutro)

            afirma(codigo_antes == codigo_despues == 0,
                   f"el veredicto no debe cambiar por un archivo neutro en forense/digesto/: "
                   f"antes={codigo_antes} despues={codigo_despues}")
            afirma("LÍNEA BASE: VERDE" in salida_antes and "LÍNEA BASE: VERDE" in salida_despues,
                   f"ambas corridas deben ser VERDE; antes:\n{salida_antes}\ndespues:\n{salida_despues}")
    try:
        _con_estado_limpio(cuerpo)
    finally:
        if os.path.exists(neutro):
            os.remove(neutro)


def main():
    prueba_warn_nuevo_no_pone_rojo()
    prueba_fail_nuevo_si_pone_rojo()
    prueba_archivo_neutro_no_mueve_veredicto()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_suite_warn_estado.py: 3 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
