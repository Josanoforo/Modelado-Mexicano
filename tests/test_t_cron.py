#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de T31 · T-CRON (`tests/check.py`) -- ACTO MAESTRA38-CRON-2 ·
REGISTRO-Y-HUELLA (dirección, 6/sep/2026,
`forense/cron/REGISTRO-CRON-v1_0.md` §4), endurecido por
ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE (P1, 7/sep/2026).

Cuatro pruebas, sin tocar el árbol real ni la red:
- `prueba_ultimo_habil` -- aritmética de calendario.
- `prueba_positivo_censo_local` -- un `tmp_path` con
  `forense/censo-raiz/<fecha>.txt` (positivo, sin señal).
- `prueba_negativo_sin_censo` -- ninguno de los dos y CERO llamada de red
  real: `subprocess.run` se reemplaza por un doble (`unittest.mock.patch`,
  que sí alcanza al `import subprocess` local de `_t_cron_existe_huella`
  porque ambos resuelven al mismo objeto módulo en `sys.modules`) y la
  prueba exige, como control positivo, que el doble se haya invocado --
  si algún día `_t_cron_existe_huella` deja de llamar a `git ls-remote`,
  esta prueba debe notarlo, no pasar por casualidad con la red real.
  Defecto corregido: antes de este acto, la prueba comentaba que "el
  remoto real puede o no responder" y dejaba pasar tráfico real.
- `prueba_senal_no_genera_delta_baseline` -- P1: T31 dispara con
  `senal()`, no `warn()`, así que una huella ausente nueva no debe
  sobrevivir a la resta `- set(SENAL)` que `--baseline`/`--freeze`
  aplican. Ejercita `check._baseline_compare()` real, contra un
  `tests/baseline.json` temporal (nunca el real).

Corre sola, mismo patrón que `tests/test_censo_derivado.py`:

    python3 tests/test_t_cron.py
"""
import datetime
import glob
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check as C  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_ultimo_habil():
    # lunes 2026-09-07 -> viernes 2026-09-04 (3 días antes)
    afirma(C.t_cron_ultimo_habil(datetime.date(2026, 9, 7)) == datetime.date(2026, 9, 4),
           "lunes debe contar el viernes anterior")
    # martes..viernes -> día anterior
    for dow_date in (datetime.date(2026, 9, 8), datetime.date(2026, 9, 9),
                      datetime.date(2026, 9, 10), datetime.date(2026, 9, 11)):
        esperado = dow_date - datetime.timedelta(days=1)
        afirma(C.t_cron_ultimo_habil(dow_date) == esperado,
               f"{dow_date} debe contar el día anterior ({esperado})")
    # domingo 2026-09-06 -> viernes 2026-09-04
    afirma(C.t_cron_ultimo_habil(datetime.date(2026, 9, 6)) == datetime.date(2026, 9, 4),
           "domingo debe contar el viernes previo")


def prueba_positivo_censo_local():
    """Positivo: existe `forense/censo-raiz/<fecha>*.txt` -> sin señal."""
    fecha = datetime.date(2026, 9, 10)
    with tempfile.TemporaryDirectory() as td:
        censo_dir = os.path.join(td, "forense", "censo-raiz")
        os.makedirs(censo_dir)
        io.open(os.path.join(censo_dir, f"{fecha.isoformat()}.txt"),
                "w", encoding="utf-8").write("Total en disco: 1\n")
        root_orig = C.ROOT
        C.ROOT = td
        try:
            afirma(C._t_cron_existe_huella(fecha) is True,
                   "con censo local presente, la huella debe existir")
        finally:
            C.ROOT = root_orig


def prueba_negativo_sin_censo():
    """Negativo: fecha hábil sin censo local ni rama remota -> huella
    ausente (senal esperada en T31), sin tocar la red real."""
    fecha = datetime.date(2026, 9, 10)
    llamadas = []

    class _RFalso:
        returncode = 0
        stdout = ""  # git ls-remote sin coincidencias -> stdout vacío

    def _run_falso(*a, **kw):
        llamadas.append(a[0] if a else kw.get("args"))
        return _RFalso()

    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "forense", "censo-raiz"))
        root_orig = C.ROOT
        C.ROOT = td
        try:
            with unittest.mock.patch.object(subprocess, "run", _run_falso):
                existe = C._t_cron_existe_huella(fecha)
        finally:
            C.ROOT = root_orig

    afirma(len(llamadas) >= 1,
           "el doble de `subprocess.run` no fue invocado -- la prueba no "
           "aisló nada y no demuestra el caso negativo (control positivo "
           "de la propia prueba)")
    if llamadas:
        afirma(llamadas[0][:3] == ["git", "ls-remote", "--heads"],
               f"se esperaba `git ls-remote --heads ...`, se llamó {llamadas[0]!r}")
    afirma(existe is False,
           "sin censo local ni rama remota `censo/2026-09-10`, la "
           "huella no debe existir (señal T-CRON esperada)")


def prueba_senal_no_genera_delta_baseline():
    """P1 · ACTO ADQ-CRON-V2: una huella T-CRON ausente, registrada por
    `senal()`, no debe volver ROJA una `--baseline` que no la conocía --
    exactamente la regresión que `warn()` producía antes de este acto.
    Ejercita `check._baseline_compare()` real contra un
    `tests/baseline.json` temporal (nunca el archivo real del repo)."""
    fails_bak, warns_bak, senal_bak = C.FAILS[:], C.WARNS[:], C.SENAL[:]
    baseline_path_bak = C.BASELINE_PATH
    C.FAILS.clear()
    C.WARNS.clear()
    C.SENAL.clear()
    try:
        with tempfile.TemporaryDirectory() as td:
            baseline_tmp = os.path.join(td, "baseline.json")
            with io.open(baseline_tmp, "w", encoding="utf-8") as f:
                json.dump({"head": "0000000", "fails": [], "warns": [],
                           "nota": "fixture de prueba, sin T-CRON conocido"}, f)
            C.BASELINE_PATH = baseline_tmp

            # Simula exactamente lo que t31_cron() hace en el caso "huella
            # ausente", sin depender de datetime.date.today() ni de la red.
            C.senal("T-CRON",
                    "sin censo del 2026-09-10 (último hábil); cron no dejó "
                    "huella -- ver forense/cron/REGISTRO-CRON-v1_0.md §5")

            afirma(any(t == "T-CRON" for t, _ in C.WARNS),
                   "la señal debe seguir visible en WARNS (A.12: nunca calla)")

            salida = io.StringIO()
            sys_stdout_bak = sys.stdout
            sys.stdout = salida
            try:
                codigo = C._baseline_compare()
            finally:
                sys.stdout = sys_stdout_bak

            afirma(codigo == 0,
                   "una señal T-CRON nueva no debe hacer que --baseline "
                   f"salga ROJO (código {codigo}); salida:\n{salida.getvalue()}")
            afirma("LÍNEA BASE: VERDE" in salida.getvalue(),
                   f"se esperaba VERDE; salida:\n{salida.getvalue()}")
            afirma("T-CRON" not in salida.getvalue(),
                   "T-CRON no debe aparecer como entrada nueva del delta -- "
                   f"salida:\n{salida.getvalue()}")
    finally:
        C.FAILS[:] = fails_bak
        C.WARNS[:] = warns_bak
        C.SENAL[:] = senal_bak
        C.BASELINE_PATH = baseline_path_bak


def main():
    prueba_ultimo_habil()
    prueba_positivo_censo_local()
    prueba_negativo_sin_censo()
    prueba_senal_no_genera_delta_baseline()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_t_cron.py: 4 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
