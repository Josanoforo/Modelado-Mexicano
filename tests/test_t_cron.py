#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de T31 · T-CRON v2 (`tests/check.py`) -- ACTO MAESTRA38-CRON-2 ·
REGISTRO-Y-HUELLA (dirección, 6/sep/2026,
`forense/cron/REGISTRO-CRON-v1_0.md` §4), reemplazado por
ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE (7/sep/2026).

Sin tocar el árbol real, la red ni el reloj real:
- `prueba_ultimo_habil` / `prueba_fecha_a_evaluar` -- aritmética de
  calendario (hoy mismo si es día hábil, si no el último hábil).
- `prueba_t_cron_estado_*` -- las cinco ramas de la función PURA
  `t_cron_estado(fecha, prefijos, cuerpo_adq)` (P5): SIN-HUELLA,
  CENSO-SIN-CIERRE, ARRANCO-FALLO (PARO y exit != 0), COMPLETO. Cero
  mocks: es una función de datos a estado, se ejercita directo.
- `prueba_negativo_sin_censo_sin_red_real` -- control de aislamiento:
  `subprocess.run` se reemplaza por un doble (`unittest.mock.patch`, que
  sí alcanza al `import subprocess` local de `_t_cron_ref_censo` porque
  ambos resuelven al mismo objeto módulo en `sys.modules`) que simula
  "la rama no existe en ningún lado" -- con control positivo (cuenta de
  llamadas) para que la prueba no pase por casualidad con la red real.
  Defecto corregido (hecho 6 del encargo): antes de este acto la prueba
  dejaba pasar tráfico real hacia `git ls-remote`.
- `prueba_gracia_pendiente_no_es_senal` -- P5: antes de las 07:30+gracia
  del día en curso, `t31_cron()` no debe llamar a `senal()` en absoluto
  (PENDIENTE no es una señal).
- `prueba_senal_no_genera_delta_baseline` -- P1: una vez pasada la
  gracia, T31 dispara con `senal()`, no `warn()`, así que una huella
  ausente nueva no debe sobrevivir a la resta `- set(SENAL)` que
  `--baseline`/`--freeze` aplican. Ejercita `check._baseline_compare()`
  real, contra un `tests/baseline.json` temporal (nunca el real).

Corre sola:

    python3 tests/test_t_cron.py
"""
import datetime
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
    for dow_date in (datetime.date(2026, 9, 8), datetime.date(2026, 9, 9),
                      datetime.date(2026, 9, 10), datetime.date(2026, 9, 11)):
        esperado = dow_date - datetime.timedelta(days=1)
        afirma(C.t_cron_ultimo_habil(dow_date) == esperado,
               f"{dow_date} debe contar el día anterior ({esperado})")
    afirma(C.t_cron_ultimo_habil(datetime.date(2026, 9, 6)) == datetime.date(2026, 9, 4),
           "domingo debe contar el viernes previo")


def prueba_fecha_a_evaluar():
    """P5: un día hábil se evalúa a sí mismo; fin de semana cae al último
    hábil (viernes)."""
    martes = datetime.date(2026, 9, 8)
    afirma(C._t_cron_fecha_a_evaluar(martes) == martes,
           "un día hábil debe evaluarse a sí mismo, no 'ayer'")
    sabado = datetime.date(2026, 9, 12)
    domingo = datetime.date(2026, 9, 13)
    viernes = datetime.date(2026, 9, 11)
    afirma(C._t_cron_fecha_a_evaluar(sabado) == viernes,
           "sábado debe caer al viernes")
    afirma(C._t_cron_fecha_a_evaluar(domingo) == viernes,
           "domingo debe caer al viernes")


def prueba_t_cron_estado_sin_huella():
    estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 10), set(), None)
    afirma(estado == "SIN-HUELLA", f"prefijos vacíos debe dar SIN-HUELLA, dio {estado}")
    afirma("censo/2026-09-10" in detalle, f"detalle debe citar la rama, dio {detalle!r}")


def prueba_t_cron_estado_censo_sin_cierre():
    estado, _ = C.t_cron_estado(datetime.date(2026, 9, 10), {"[CENSO]"}, None)
    afirma(estado == "CENSO-SIN-CIERRE",
           f"[CENSO] sin [ADQ] debe dar CENSO-SIN-CIERRE, dio {estado}")
    estado2, _ = C.t_cron_estado(datetime.date(2026, 9, 10), {"[CENSO]", "[ADQ-PDN]"}, None)
    afirma(estado2 == "CENSO-SIN-CIERRE",
           f"[CENSO]+[ADQ-PDN] sin [ADQ] debe dar CENSO-SIN-CIERRE, dio {estado2}")


def prueba_t_cron_estado_arranco_fallo_paro():
    cuerpo = ("[ADQ] 2026-09-10\n\n"
              "[ADQ] 2026-09-10 07:31: invocado=no motivo=PARO-CORPUS exit=- "
              "duracion=0s commits_nuevos=0 ramas_nuevas=0 archivos_modificados=0")
    estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 10), {"[ADQ]"}, cuerpo)
    afirma(estado == "ARRANCO-FALLO",
           f"invocado=no (PARO) debe dar ARRANCO-FALLO, dio {estado}")
    afirma("PARO-CORPUS" in detalle, f"detalle debe citar el motivo, dio {detalle!r}")


def prueba_t_cron_estado_arranco_fallo_exit_no_cero():
    cuerpo = ("[ADQ] 2026-09-10\n\n"
              "[ADQ] 2026-09-10 07:45: invocado=si motivo=- exit=1 "
              "duracion=120s commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1")
    estado, _ = C.t_cron_estado(datetime.date(2026, 9, 10), {"[ADQ]", "[CENSO]", "[ADQ-PDN]"}, cuerpo)
    afirma(estado == "ARRANCO-FALLO",
           f"invocado=si con exit=1 debe dar ARRANCO-FALLO, dio {estado}")


def prueba_t_cron_estado_completo():
    cuerpo = ("[ADQ] 2026-09-10\n\n"
              "[ADQ] 2026-09-10 07:33: invocado=si motivo=- exit=0 "
              "duracion=179s commits_nuevos=1 ramas_nuevas=0 archivos_modificados=1 "
              "run_id=2026-09-10T073000-1234")
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 10), {"[CENSO]", "[ADQ-PDN]", "[ADQ]"}, cuerpo)
    afirma(estado == "COMPLETO", f"invocado=si exit=0 debe dar COMPLETO, dio {estado}")
    afirma("exit=0" in detalle, f"detalle debe citar exit=0, dio {detalle!r}")


def prueba_negativo_sin_censo_sin_red_real():
    """SIN-HUELLA de punta a punta, sin tocar la red real: `subprocess.run`
    se reemplaza por un doble que simula 'la rama no existe en ningún
    lado' (ni local, ni `git ls-remote` con coincidencias)."""
    fecha = datetime.date(2026, 9, 10)
    llamadas = []

    class _RFalso:
        returncode = 1
        stdout = ""
        stderr = ""

    def _run_falso(cmd, **kw):
        llamadas.append(cmd)
        return _RFalso()

    with tempfile.TemporaryDirectory() as td:
        os.makedirs(os.path.join(td, "forense", "censo-raiz"))
        root_orig = C.ROOT
        C.ROOT = td
        try:
            with unittest.mock.patch.object(subprocess, "run", _run_falso):
                resultado = C._t_cron_commits_censo(fecha)
        finally:
            C.ROOT = root_orig

    afirma(len(llamadas) >= 1,
           "el doble de `subprocess.run` no fue invocado -- la prueba no "
           "aisló nada y no demuestra el caso negativo (control positivo "
           "de la propia prueba)")
    afirma(any(c[:2] == ["git", "show-ref"] for c in llamadas),
           f"se esperaba al menos un `git show-ref ...`, se llamó {llamadas!r}")
    afirma(resultado is None,
           "sin rama local, remota ni respuesta de `git ls-remote`, "
           "_t_cron_commits_censo debe devolver None (SIN-HUELLA en t31_cron)")


def prueba_gracia_pendiente_no_es_senal():
    """P5: antes de 07:30+gracia del día en curso, t31_cron() no debe
    emitir ninguna señal -- PENDIENTE no es una señal."""
    fails_bak, warns_bak, senal_bak = C.FAILS[:], C.WARNS[:], C.SENAL[:]
    C.FAILS.clear()
    C.WARNS.clear()
    C.SENAL.clear()
    ahora_temprano = datetime.datetime(2026, 9, 8, 7, 0,
                                        tzinfo=datetime.timezone(datetime.timedelta(hours=-6)))
    try:
        with unittest.mock.patch.object(C, "_t_cron_ahora_mx", lambda: (ahora_temprano, True)):
            C.t31_cron()
        afirma(not C.WARNS and not C.SENAL,
               f"antes de la gracia no debe haber señal, dio WARNS={C.WARNS} SENAL={C.SENAL}")
    finally:
        C.FAILS[:] = fails_bak
        C.WARNS[:] = warns_bak
        C.SENAL[:] = senal_bak


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

            estado, detalle = C.t_cron_estado(datetime.date(2026, 9, 10), set(), None)
            C.senal("T-CRON", f"{estado} -- {detalle} -- ver forense/cron/REGISTRO-CRON-v1_0.md §5")

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
    prueba_fecha_a_evaluar()
    prueba_t_cron_estado_sin_huella()
    prueba_t_cron_estado_censo_sin_cierre()
    prueba_t_cron_estado_arranco_fallo_paro()
    prueba_t_cron_estado_arranco_fallo_exit_no_cero()
    prueba_t_cron_estado_completo()
    prueba_negativo_sin_censo_sin_red_real()
    prueba_gracia_pendiente_no_es_senal()
    prueba_senal_no_genera_delta_baseline()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_t_cron.py: 10 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
