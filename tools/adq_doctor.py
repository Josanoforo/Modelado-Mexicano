#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/adq_doctor.py -- diagnóstico de solo lectura del sistema de
adquisición programada (P4, ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-
RUNNER-IDEMPOTENTE, 7/sep/2026).

NO corrige nada: reporta. Reutiliza `tests/check.py` (T-CRON v2, P5) para
el estado del cron en vez de reimplementar esa lógica -- la fuente de
verdad de "¿corrió el cron?" es una sola.

Uso:
    python3 tools/adq_doctor.py            # reporte de texto
    python3 tools/adq_doctor.py --json      # mismo contenido, JSON

Nunca lanza por un chequeo individual que falle: cada sección atrapa sus
propios errores y los reporta como NO-VERIFICABLE, para que un doctor que
se cuelga a la mitad no oculte los diagnósticos que sí alcanzó a hacer.
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.path.insert(0, os.path.join(RAIZ, "tests"))


def _seguro(fn, *a, **kw):
    """Corre `fn`, nunca lanza: un chequeo que falla se reporta como error,
    no tumba al resto del doctor."""
    try:
        return fn(*a, **kw), None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def _corre(cmd, timeout=10, cwd=None):
    # `errors="replace"`, no `text=True` a secas: los binarios de Windows
    # invocados bajo /mnt/c (schtasks.exe, tzutil.exe) devuelven su salida
    # en la codepage de consola del sistema (vista aquí: bytes no-UTF-8
    # con acentos españoles), no UTF-8 -- decodificar a ciegas revienta
    # con UnicodeDecodeError y tumba TODO el doctor si no se atrapa
    # aparte. `_seguro()` ya envuelve cada sección, pero esto evita perder
    # el contenido legible del resto de la línea por un solo byte.
    try:
        r = subprocess.run(cmd, cwd=cwd or RAIZ, capture_output=True,
                            text=True, errors="replace", timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except FileNotFoundError:
        return 127, "", "comando no encontrado"
    except subprocess.TimeoutExpired:
        return 124, "", f"tiempo agotado ({timeout}s)"
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


def check_entorno():
    """CAJA/WSL esperado -- convención del programa (ver .claude/commands/
    acto.md A.2): CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE sin fijar = CAJA."""
    tipo = os.environ.get("CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE")
    es_wsl = False
    version = ""
    try:
        with open("/proc/version", encoding="utf-8", errors="replace") as f:
            version = f.read().strip()
            es_wsl = "microsoft" in version.lower() or "wsl" in version.lower()
    except OSError:
        pass
    return {
        "CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE": tipo or "(sin fijar -- CAJA)",
        "es_wsl_detectado": es_wsl,
        "proc_version": version[:160],
    }


def check_zona_horaria():
    ahora_local = datetime.datetime.now().astimezone()
    tz_sistema = None
    try:
        with open("/etc/timezone", encoding="utf-8") as f:
            tz_sistema = f.read().strip()
    except OSError:
        pass
    try:
        from zoneinfo import ZoneInfo
        ahora_mx = datetime.datetime.now(ZoneInfo("America/Mexico_City"))
        zoneinfo_ok = True
    except Exception:
        ahora_mx = None
        zoneinfo_ok = False
    # P2: el trigger de Windows Task Scheduler dispara en hora LOCAL del
    # sistema, sin campo de zona horaria explícito como cron -- si el
    # reloj de Windows no está en America/Mexico_City, la tarea de
    # tools/windows/instala-tarea-adquisicion.ps1 dispara a una hora de
    # mesa distinta de la que dice. `tzutil.exe /g` corre bajo /mnt/c
    # (mismo límite de sandbox que schtasks.exe -- NO-VERIFICABLE, nunca
    # un desajuste inventado, si no es legible desde este proceso).
    tzutil = "/mnt/c/Windows/System32/tzutil.exe"
    if os.path.exists(tzutil):
        codigo, out, err = _corre([tzutil, "/g"], timeout=10)
        tz_windows = out.strip() if codigo == 0 else f"NO-VERIFICABLE: {(err or out).strip()[:120]}"
    else:
        tz_windows = "NO-VERIFICABLE: tzutil.exe no es legible desde este proceso"
    return {
        "tz_sistema_etc_timezone": tz_sistema or "NO-LEGIBLE",
        "offset_local_actual": ahora_local.strftime("%z"),
        "zoneinfo_america_mexico_city_disponible": zoneinfo_ok,
        "ahora_america_mexico_city": ahora_mx.isoformat(timespec="seconds") if ahora_mx else None,
        "tz_windows_host_tzutil": tz_windows,
    }


def check_scheduler_windows():
    """Windows Task Scheduler (P2), consultado vía PowerShell bajo
    /mnt/c. `Get-ScheduledTask*` en vez de `schtasks.exe /FO LIST`: los
    nombres de propiedad de PowerShell son estables en cualquier locale,
    las etiquetas de `schtasks.exe` NO -- medido en esta caja (Windows en
    español): "Last Run Time" no existe, es "Último tiempo de ejecución",
    y parsear por etiqueta habría dado "?" en todos los campos en
    silencio. NO-VERIFICABLE si /mnt/c o powershell.exe no son legibles
    desde este proceso (p.ej. dentro de un sandbox que deniega /mnt) --
    nunca se asume "no instalado" por eso."""
    nombre_tarea = os.environ.get("ADQ_TASK_SCHEDULER_NOMBRE", "\\ModeladoMexicano\\AdquiereCron")
    partes = nombre_tarea.strip("\\").split("\\")
    task_name = partes[-1]
    task_path = "\\" + "\\".join(partes[:-1]) + "\\" if len(partes) > 1 else "\\"
    powershell = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"
    if not os.path.exists(powershell):
        return {"estado": "NO-VERIFICABLE", "razon": f"{powershell} no es legible desde este proceso"}
    script_ps = (
        f"$ErrorActionPreference='Stop'; "
        f"$t = Get-ScheduledTask -TaskName '{task_name}' -TaskPath '{task_path}'; "
        f"$i = Get-ScheduledTaskInfo -TaskName '{task_name}' -TaskPath '{task_path}'; "
        f"[pscustomobject]@{{"
        f"State=$t.State.ToString(); LogonType=$t.Principal.LogonType.ToString(); "
        f"LastRunTime=$i.LastRunTime.ToString('o'); LastTaskResult=$i.LastTaskResult; "
        f"NextRunTime=$i.NextRunTime.ToString('o')"
        f"}} | ConvertTo-Json"
    )
    codigo, out, err = _corre([powershell, "-NoProfile", "-Command", script_ps], timeout=20)
    if codigo != 0:
        return {"estado": "NO-INSTALADO-O-NO-VERIFICABLE", "detalle": (err or out).strip()[:400],
                "tarea_buscada": nombre_tarea}
    try:
        campos = json.loads(out)
    except json.JSONDecodeError:
        return {"estado": "NO-VERIFICABLE", "razon": f"salida de PowerShell no fue JSON: {out.strip()[:200]}"}
    return {"estado": "INSTALADA", "tarea": nombre_tarea, **campos}


def check_crontab_legado():
    """cron clásico de WSL -- se sigue reportando (P2 dice "evitar un
    segundo scheduler diario activo", no "ocultar si sigue instalado"):
    esta caja tuvo un incidente real (7/sep) por depender solo de cron.

    `crontab -l` sin crontab real sale con "no crontab for <user>" -- una
    ejecución de verdad. Un entorno restringido (p.ej. este mismo tool
    corriendo dentro del sandbox de Claude Code) da en cambio
    "fopen: ... Permission denied": eso NO es "sin crontab", es "no se
    pudo preguntar" -- reportarlo como `instalado: False` sería el mismo
    falso negativo A.13 que el resto del programa ya vigila."""
    codigo, out, err = _corre(["crontab", "-l"], timeout=10)
    if codigo != 0:
        salida = (err or out or "").strip()
        if "no crontab for" in salida.lower():
            return {"instalado": False, "detalle": salida[:200]}
        return {"instalado": "NO-VERIFICABLE", "detalle": salida[:200]}
    tiene_adquiere = "adquiere_cron.sh" in out
    return {"instalado": tiene_adquiere, "lineas_relevantes": [l for l in out.splitlines() if "adquiere_cron" in l]}


def check_binarios():
    return {b: (shutil.which(b) or "AUSENTE") for b in ("git", "curl", "python3", "gh", "claude")}


def check_corpus():
    ruta_raw = os.path.join(RAIZ, "data", "raw")
    existe = os.path.islink(ruta_raw) or os.path.isdir(ruta_raw)
    destino = os.readlink(ruta_raw) if os.path.islink(ruta_raw) else None
    primero = None
    if existe:
        try:
            hijos = sorted(os.listdir(ruta_raw))
            primero = hijos[0] if hijos else "(vacío)"
        except OSError as e:
            primero = f"NO-LEGIBLE: {e}"
    return {"data_raw_existe": existe, "es_symlink": os.path.islink(ruta_raw),
            "symlink_destino": destino, "primer_hijo": primero}


def check_descargas_mx():
    try:
        import manifiesto
        raiz = manifiesto.resolver_raiz("descargas_mx", RAIZ, os.path.join(RAIZ, "data", "raw"))
    except Exception as e:
        return {"estado": "NO-VERIFICABLE", "razon": f"{type(e).__name__}: {e}"}
    if not raiz:
        return {"estado": "NO-CONFIGURADA", "razon": "sin entrada en data/raices.local.yaml en esta máquina"}
    if not os.path.isdir(raiz):
        return {"estado": "AUSENTE", "ruta_configurada": raiz}
    return {"estado": "OK", "ruta": raiz}


def check_red():
    try:
        import adq_config
        url = adq_config.obten("sonda_red_url")
    except Exception:
        url = "https://www.inegi.org.mx/"
    codigo, out, err = _corre(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                                "--max-time", "10", url], timeout=15)
    return {"url": url, "codigo_http": out.strip() if codigo == 0 else "sin-respuesta"}


def check_lock():
    """Prueba de solo lectura: intenta tomar el lock sin bloquear y lo
    libera de inmediato. Si falla (lock activo), reporta -- NO espera ni
    lo toma para quedárselo."""
    import fcntl
    estado_dir = os.path.join(RAIZ, "forense", "adq-log", "estado")
    lockfile = os.path.join(estado_dir, "adquiere_cron.lock")
    if not os.path.exists(lockfile):
        return {"lock_activo": False, "razon": "el archivo de lock no existe todavía (ninguna corrida lo ha creado)"}
    try:
        with open(lockfile, "r+") as f:
            try:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                return {"lock_activo": False}
            except OSError:
                return {"lock_activo": True, "razon": "flock no bloqueante falló -- una instancia lo tiene tomado"}
    except OSError as e:
        return {"lock_activo": None, "razon": f"no se pudo abrir {lockfile}: {e}"}


def check_heartbeat():
    ruta = os.path.join(RAIZ, "forense", "adq-log", "estado", "heartbeat.json")
    if not os.path.exists(ruta):
        return {"estado": "AUSENTE", "razon": "ninguna corrida ha escrito heartbeat todavía en esta caja"}
    try:
        with open(ruta, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        return {"estado": "NO-LEGIBLE", "razon": str(e)}


def check_t_cron():
    """Reusa tests/check.py -- una sola fuente de verdad para "¿corrió el
    cron?", no una segunda implementación que pueda divergir."""
    import check as C
    ahora_mx, zona_real = C._t_cron_ahora_mx()
    hoy = ahora_mx.date()
    fecha = C._t_cron_fecha_a_evaluar(hoy)
    if fecha < C._T_CRON_INSTALACION:
        return {"estado": "ANTES-DE-INSTALACION", "fecha_evaluada": fecha.isoformat()}
    if fecha == hoy:
        gracia = C._t_cron_gracia_minutos()
        limite = (datetime.datetime.combine(fecha, datetime.time(7, 30), tzinfo=ahora_mx.tzinfo)
                  + datetime.timedelta(minutes=gracia))
        if ahora_mx < limite:
            return {"estado": "PENDIENTE", "fecha_evaluada": fecha.isoformat(),
                    "limite_gracia": limite.isoformat(timespec="minutes")}
    resultado = C._t_cron_commits_censo(fecha)
    prefijos, cuerpo_adq = resultado if resultado is not None else (set(), None)
    if C._t_cron_existe_censo_local(fecha):
        prefijos = prefijos | {"[CENSO]"}
    estado, detalle = C.t_cron_estado(fecha, prefijos, cuerpo_adq)
    return {"estado": estado, "fecha_evaluada": fecha.isoformat(), "detalle": detalle}


def check_ultimo_censo_local():
    import glob
    archivos = sorted(glob.glob(os.path.join(RAIZ, "forense", "censo-raiz", "*.txt")))
    if not archivos:
        return {"existe": False}
    ultimo = archivos[-1]
    return {"existe": True, "archivo": os.path.relpath(ultimo, RAIZ),
             "modificado": datetime.datetime.fromtimestamp(os.path.getmtime(ultimo)).isoformat(timespec="seconds")}


SECCIONES = [
    ("entorno", check_entorno),
    ("zona_horaria", check_zona_horaria),
    ("scheduler_windows", check_scheduler_windows),
    ("crontab_legado", check_crontab_legado),
    ("binarios", check_binarios),
    ("corpus_data_raw", check_corpus),
    ("descargas_mx", check_descargas_mx),
    ("red", check_red),
    ("lock", check_lock),
    ("heartbeat", check_heartbeat),
    ("t_cron", check_t_cron),
    ("ultimo_censo_local", check_ultimo_censo_local),
]


def recolecta():
    reporte = {}
    for nombre, fn in SECCIONES:
        valor, error = _seguro(fn)
        reporte[nombre] = {"error": error} if error else valor
    return reporte


def imprime_texto(reporte):
    print("═" * 72)
    print("  ADQ_DOCTOR — diagnóstico de solo lectura (no corrige nada)")
    print("═" * 72)
    for nombre, _ in SECCIONES:
        print(f"\n[{nombre}]")
        datos = reporte[nombre]
        if isinstance(datos, dict):
            for k, v in datos.items():
                print(f"  {k}: {v}")
        else:
            print(f"  {datos}")
    print()


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--json", action="store_true", help="salida JSON en vez de texto")
    a = ap.parse_args()
    reporte = recolecta()
    if a.json:
        print(json.dumps(reporte, ensure_ascii=False, indent=2, default=str))
    else:
        imprime_texto(reporte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
