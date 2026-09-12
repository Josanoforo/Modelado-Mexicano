#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test de `tools/adq_doctor.py` (P4, ACTO ADQ-CRON-V2). No ejercita el
reporte completo (mezcla red, `/mnt/c`, `crontab` reales) -- cubre los dos
puntos con lógica real de clasificación:

- `check_crontab_legado`: "sin crontab" (ejecución real, sin credencial)
  no debe confundirse con "no se pudo preguntar" (sandbox/permiso) --
  ambos salen con código != 0 pero significan cosas distintas.
- `check_lock`: detecta un lock realmente tomado por OTRO proceso (se
  lanza un subproceso que toma flock y se queda vivo) sin bloquearse ni
  quedárselo.

Corre sola:

    python3 tests/test_adq_doctor.py
"""
import os
import base64
import json
import subprocess
import sys
import tempfile
import time
import unittest.mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import adq_doctor as D  # noqa: E402

FAILS = []


def afirma(cond, msg):
    if not cond:
        FAILS.append(msg)


def prueba_crontab_sin_credencial_no_es_no_instalado():
    with unittest.mock.patch.object(
            D, "_corre", lambda *a, **kw: (1, "", "crontab: crontabs/pc0/: fopen: Permission denied")):
        r = D.check_crontab_legado()
    afirma(r["instalado"] == "NO-VERIFICABLE",
           f"un fallo de permiso debe ser NO-VERIFICABLE, no False -- dio {r}")


def prueba_crontab_realmente_vacio():
    with unittest.mock.patch.object(
            D, "_corre", lambda *a, **kw: (1, "", "no crontab for pc0")):
        r = D.check_crontab_legado()
    afirma(r["instalado"] is False,
           f"'no crontab for <user>' es una ejecución real, debe dar False -- dio {r}")


def prueba_crontab_instalado_detecta_linea():
    with unittest.mock.patch.object(
            D, "_corre", lambda *a, **kw: (0, "PATH=/usr/bin\n30 7 * * 1-5 cd /x && ./tools/adquiere_cron.sh\n", "")):
        r = D.check_crontab_legado()
    afirma(r["instalado"] is True, f"línea de adquiere_cron.sh presente debe dar True -- dio {r}")


def prueba_crontab_retirado_ignora_comentario_historico():
    crontab = (
        "# tools/adquiere_cron.sh resuelve su propio REPO_DIR\n"
        "PATH=/usr/local/bin:/usr/bin:/bin:/home/pc0/.local/bin\n"
    )
    with unittest.mock.patch.object(
            D, "_corre", lambda *a, **kw: (0, crontab, "")):
        r = D.check_crontab_legado()
    afirma(r["instalado"] is False and r["lineas_relevantes"] == [],
           f"un comentario histórico no reinstala el cron legado -- dio {r}")


def prueba_lock_libre():
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "forense", "adq-log", "estado")
        os.makedirs(ruta)
        lockfile = os.path.join(ruta, "adquiere_cron.lock")
        open(lockfile, "w").close()
        with unittest.mock.patch.object(D, "RAIZ", td):
            r = D.check_lock()
        afirma(r["lock_activo"] is False, f"un lockfile sin tomar debe dar False -- dio {r}")


def prueba_lock_tomado_por_otro_proceso():
    with tempfile.TemporaryDirectory() as td:
        ruta = os.path.join(td, "forense", "adq-log", "estado")
        os.makedirs(ruta)
        lockfile = os.path.join(ruta, "adquiere_cron.lock")
        open(lockfile, "w").close()
        # Sub-proceso que toma flock exclusivo y se queda vivo 3s -- prueba
        # de un lock tomado por OTRO PID, no un self-deadlock del propio
        # proceso de prueba (flock de Linux es por descriptor de archivo,
        # no reentrante dentro del mismo proceso).
        codigo_hijo = (
            "import fcntl, time, sys\n"
            f"f = open({lockfile!r}, 'r+')\n"
            "fcntl.flock(f.fileno(), fcntl.LOCK_EX)\n"
            "sys.stdout.write('LISTO\\n'); sys.stdout.flush()\n"
            "time.sleep(3)\n"
        )
        proc = subprocess.Popen([sys.executable, "-c", codigo_hijo],
                                 stdout=subprocess.PIPE, text=True)
        try:
            linea = proc.stdout.readline()
            afirma(linea.strip() == "LISTO", f"el subproceso no confirmó haber tomado el lock: {linea!r}")
            with unittest.mock.patch.object(D, "RAIZ", td):
                r = D.check_lock()
            afirma(r["lock_activo"] is True,
                   f"un lock tomado por otro proceso vivo debe detectarse True -- dio {r}")
        finally:
            proc.terminate()
            proc.wait(timeout=5)


def prueba_scheduler_contrasta_calendario_y_disparador():
    comando = (
        "& wsl.exe -d Ubuntu -u pc0 -- env "
        "ADQ_DISPARADOR=windows-task-scheduler "
        "bash -lc /home/pc0/mm-adq/tools/adquiere_launcher.sh\n"
        "exit [int]$LASTEXITCODE")
    codificado = base64.b64encode(comando.encode("utf-16-le")).decode("ascii")
    campos = {
        "State": "Ready", "TaskName": "AdquiereCron",
        "TaskPath": "\\ModeladoMexicano\\", "UserId": "PC0",
        "LogonType": "Interactive",
        "Execute": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
        "Arguments": ("-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden "
                      f"-EncodedCommand {codificado}"),
        # Sunday=1 + Monday..Saturday=2..64: los siete días son 127.
        "Triggers": [{"Type": "MSFT_TaskWeeklyTrigger", "Enabled": True,
                      "StartBoundary": "2026-09-07T07:30:00-06:00",
                      "DaysOfWeek": 127}],
        "StartWhenAvailable": True,
        "MultipleInstances": "IgnoreNew", "LastRunTime": "2026-09-10T09:05:41-06:00",
        "LastTaskResult": 0, "NextRunTime": "2026-09-11T07:30:00-06:00",
    }
    snapshot = {"ZoneWindows": "Central Standard Time (Mexico)",
                "EventLog": {"IsEnabled": True}, "Task": campos}
    D._snapshot_windows.cache_clear()
    with unittest.mock.patch.object(D.os.path, "exists", lambda _: True), \
         unittest.mock.patch.object(D, "_corre", lambda *a, **kw: (0, json.dumps(snapshot), "")):
        r = D.check_scheduler_windows()
    D._snapshot_windows.cache_clear()
    afirma(r["dias_coinciden"] is True and r["hora_coincide"] is True,
           f"doctor debe contrastar hora y días de la config común, dio {r}")
    afirma(r["disparador_atribuible"] is True and r["StartWhenAvailable"] is True,
           f"doctor debe exigir acción atribuible y recuperación configurada, dio {r}")
    afirma(r["sin_ventana"] is True and r["espera_y_propaga_resultado"] is True,
           f"doctor debe acreditar envoltura oculta y espera del proceso real, dio {r}")
    afirma(r["triggers_temporales_activos"] == [],
           f"doctor no debe inventar triggers temporales, dio {r}")


def prueba_scheduler_detecta_calendario_divergente():
    campos = {"State": "Ready", "Execute": "wsl.exe", "Arguments": "bash -lc /x",
              "Triggers": [
                  {"Type": "MSFT_TaskWeeklyTrigger", "Enabled": True,
                   "StartBoundary": "2026-09-07T08:00:00-06:00", "DaysOfWeek": 64},
                  {"Type": "MSFT_TaskTimeTrigger", "Enabled": True,
                   "StartBoundary": "2026-09-11T20:00:00-06:00", "DaysOfWeek": 0}]}
    snapshot = {"ZoneWindows": "Central Standard Time (Mexico)",
                "EventLog": {"IsEnabled": True}, "Task": campos}
    D._snapshot_windows.cache_clear()
    with unittest.mock.patch.object(D.os.path, "exists", lambda _: True), \
         unittest.mock.patch.object(D, "_corre", lambda *a, **kw: (0, json.dumps(snapshot), "")):
        r = D.check_scheduler_windows()
    D._snapshot_windows.cache_clear()
    afirma(not r["dias_coinciden"] and not r["hora_coincide"]
           and not r["disparador_atribuible"],
           f"tarea divergente debe quedar explícita, dio {r}")
    afirma(len(r["triggers_temporales_activos"]) == 1 and not r["sin_ventana"],
           f"doctor debe hacer visible trigger temporal y acción con ventana, dio {r}")


def prueba_snapshot_windows_unico_para_tres_secciones():
    comando = "& wsl.exe -d Ubuntu -u pc0 -- env ADQ_DISPARADOR=windows-task-scheduler bash -lc /home/pc0/mm-adq/tools/adquiere_launcher.sh; exit $LASTEXITCODE"
    enc = base64.b64encode(comando.encode("utf-16-le")).decode("ascii")
    snapshot = {
        "ZoneWindows": "Central Standard Time (Mexico)",
        "EventLog": {"LogName": "Operational", "IsEnabled": True},
        "Task": {"Execute": "powershell.exe",
                 "Arguments": f"-NonInteractive -WindowStyle Hidden -EncodedCommand {enc}",
                 "Triggers": [{"Type": "MSFT_TaskWeeklyTrigger", "Enabled": True,
                               "StartBoundary": "2026-09-07T07:30:00-06:00",
                               "DaysOfWeek": 127}]}}
    llamadas = []
    def corre(*a, **kw):
        llamadas.append(a)
        return 0, json.dumps(snapshot), ""
    D._snapshot_windows.cache_clear()
    with unittest.mock.patch.object(D.os.path, "exists", lambda _: True), \
         unittest.mock.patch.object(D, "_corre", corre):
        D.check_zona_horaria()
        D.check_scheduler_windows()
        D.check_eventos_windows()
    D._snapshot_windows.cache_clear()
    afirma(len(llamadas) == 1,
           f"zona/tarea/eventos deben compartir un solo PowerShell, hubo {len(llamadas)}")
    if llamadas:
        cmd = llamadas[0][0]
        afirma("-NonInteractive" in cmd and "-WindowStyle" in cmd and "Hidden" in cmd,
               f"PowerShell diagnóstico debe ser oculto/no interactivo, dio {cmd}")


def main():
    prueba_crontab_sin_credencial_no_es_no_instalado()
    prueba_crontab_realmente_vacio()
    prueba_crontab_instalado_detecta_linea()
    prueba_crontab_retirado_ignora_comentario_historico()
    prueba_lock_libre()
    prueba_lock_tomado_por_otro_proceso()
    prueba_scheduler_contrasta_calendario_y_disparador()
    prueba_scheduler_detecta_calendario_divergente()
    prueba_snapshot_windows_unico_para_tres_secciones()
    if FAILS:
        print(f"FALLÓ ({len(FAILS)}):")
        for m in FAILS:
            print(f"  · {m}")
        return 1
    print("OK -- test_adq_doctor.py: 9 pruebas, 0 fallos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
