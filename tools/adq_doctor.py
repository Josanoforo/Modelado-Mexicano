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
import re
import shutil
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
sys.path.insert(0, os.path.join(RAIZ, "tests"))


def _calendario_resuelto():
    import adq_config
    return adq_config.calendario_resuelto()


def check_configuracion_operativa():
    """Valores efectivos y procedencia; separa calendario, timeout y KILL."""
    import adq_config
    cal = _calendario_resuelto()
    proxima = adq_config.proxima_ejecucion(
        datetime.datetime.now(datetime.timezone.utc), cal=cal)
    timeout = adq_config.entero_resuelto(
        "claude_timeout_segundos", "CLAUDE_TIMEOUT_SEGUNDOS", 1800)
    kill_after = adq_config.entero_resuelto(
        "claude_kill_after_segundos", "CLAUDE_KILL_AFTER_SEGUNDOS", 60)
    return {
        "calendario": cal,
        "proxima_ejecucion": proxima.isoformat(timespec="minutes"),
        "timeout_proceso": timeout,
        "gracia_term_kill": kill_after,
        "ventana_observacion_minutos": cal["ventana_observacion_minutos"],
    }


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
    calendario = _calendario_resuelto()
    ahora_local = datetime.datetime.now().astimezone()
    tz_sistema = None
    try:
        with open("/etc/timezone", encoding="utf-8") as f:
            tz_sistema = f.read().strip()
    except OSError:
        pass
    try:
        from zoneinfo import ZoneInfo
        ahora_mx = datetime.datetime.now(ZoneInfo(calendario["zona_iana"]))
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
        "zona_iana_configurada": calendario["zona_iana"],
        "zona_windows_configurada": calendario["zona_windows"],
        "config_degradada": calendario["degradada"],
        "tz_sistema_etc_timezone": tz_sistema or "NO-LEGIBLE",
        "offset_local_actual": ahora_local.strftime("%z"),
        "zoneinfo_america_mexico_city_disponible": zoneinfo_ok,
        "ahora_america_mexico_city": ahora_mx.isoformat(timespec="seconds") if ahora_mx else None,
        "tz_windows_host_tzutil": tz_windows,
        "zonas_coinciden": (tz_windows == calendario["zona_windows"]
                             if not tz_windows.startswith("NO-VERIFICABLE") else "NO-VERIFICABLE"),
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
        f"State=$t.State.ToString(); TaskName=$t.TaskName; TaskPath=$t.TaskPath; "
        f"UserId=$t.Principal.UserId; LogonType=$t.Principal.LogonType.ToString(); "
        f"Execute=$t.Actions[0].Execute; Arguments=$t.Actions[0].Arguments; "
        f"StartBoundary=$t.Triggers[0].StartBoundary; DaysOfWeek=[int]$t.Triggers[0].DaysOfWeek; "
        f"TriggerEnabled=$t.Triggers[0].Enabled; StartWhenAvailable=$t.Settings.StartWhenAvailable; "
        f"MultipleInstances=$t.Settings.MultipleInstances.ToString(); "
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
    calendario = _calendario_resuelto()
    mascara_esperada = sum(2 << d for d in calendario["weekdays"])
    accion_esperada = "ADQ_DISPARADOR=windows-task-scheduler" in (campos.get("Arguments") or "")
    return {"estado": "INSTALADA", "tarea": nombre_tarea, **campos,
            "calendario_esperado": {
                "hora": calendario["hora"], "dias_mascara": mascara_esperada,
                "zona_iana": calendario["zona_iana"],
                "zona_windows": calendario["zona_windows"],
            },
            "dias_coinciden": campos.get("DaysOfWeek") == mascara_esperada,
            "hora_coincide": calendario["hora"] in (campos.get("StartBoundary") or ""),
            "disparador_atribuible": accion_esperada}


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
    calendario, calendario_degradado = C.t_cron_calendario_declarado()
    ahora_mx, zona_real = C._t_cron_ahora_mx()
    hoy = ahora_mx.date()
    fecha = C._t_cron_fecha_a_evaluar(hoy, calendario["weekdays"])
    if fecha < C._T_CRON_INSTALACION:
        return {"estado": "ANTES-DE-INSTALACION", "fecha_evaluada": fecha.isoformat()}
    gracia_degradada = False
    if fecha == hoy:
        gracia, gracia_degradada = C.t_cron_gracia_minutos_declarada()
        hh, mm = map(int, calendario["hora"].split(":"))
        limite = (datetime.datetime.combine(fecha, datetime.time(hh, mm), tzinfo=ahora_mx.tzinfo)
                  + datetime.timedelta(minutes=gracia))
        if ahora_mx < limite:
            return {"estado": "PENDIENTE", "fecha_evaluada": fecha.isoformat(),
                    "limite_gracia": limite.isoformat(timespec="minutes")}
    # H1 (ACTO GEN2-SONDA-ADQ-CABLEADO, 9/sep/2026): la evidencia del día
    # YA FUSIONADA es primaria y no depende de que censo/<fecha> sobreviva
    # al merge; la rama viva entra como contraste. `resultado is None`
    # significa "no se pudo leer el remoto", no "no existe".
    evidencia = C._t_cron_evidencia_fusionada(fecha)
    resultado = C._t_cron_commits_censo(fecha)
    remoto_legible = resultado is not None
    prefijos, cuerpo_adq = resultado if remoto_legible else (set(), None)
    if C._t_cron_existe_censo_local(fecha):
        prefijos = prefijos | {"[CENSO]"}
    estado, detalle = C.t_cron_estado(fecha, prefijos, cuerpo_adq,
                                      evidencia_fusionada=evidencia,
                                      remoto_legible=remoto_legible)
    salida = {"estado": estado, "fecha_evaluada": fecha.isoformat(),
              "detalle": detalle, "remoto_legible": remoto_legible,
              "evidencia_fusionada_presente": evidencia is not None,
              "calendario": calendario,
              "zona_real": zona_real}
    if gracia_degradada:
        salida["gracia_config"] = ("DEGRADADA-A-DEFAULT-45: t_cron_gracia_minutos "
                                   "no se pudo leer de data/adq-config.yaml")
    if calendario_degradado:
        salida["calendario_config"] = (
            f"DEGRADADA: {calendario.get('causa')}; valor aplicado="
            f"{calendario['hora']} {calendario['zona_iana']} "
            f"días={','.join(calendario['dias_semana'])}")
    return salida


def check_ultimo_censo_local():
    import glob
    archivos = sorted(glob.glob(os.path.join(RAIZ, "forense", "censo-raiz", "*.txt")))
    if not archivos:
        return {"existe": False}
    ultimo = archivos[-1]
    return {"existe": True, "archivo": os.path.relpath(ultimo, RAIZ),
             "modificado": datetime.datetime.fromtimestamp(os.path.getmtime(ultimo)).isoformat(timespec="seconds")}


# ═══════════════════════════════════════════════════════════════
# P2 · CONTRATO ÚNICO DE ELEGIBILIDAD Y ORDEN
# ACTO GEN2-SONDA-ADQ-CABLEADO (9/sep/2026), H2 de la revisión del 9/sep.
#
# Antes de este acto había DOS reglas de selección que nadie había
# reconciliado: el prompt del runbook pedía «las 5 filas más antiguas con
# último intento >= 7 días», y `.claude/commands/adquiere.md` §1 ordenaba
# primero por prioridad. Ninguna de las dos emitía una lista auditable de
# IDs elegidos y excluidos, así que una caminata vacía era indistinguible
# de una selección equivocada.
#
# Esto NO es una segunda cola ni una rutina nueva: es una función pequeña
# y pura, expuesta como opción de una herramienta existente y de solo
# lectura (`adq_doctor.py --selecciona`). No escribe la cola, no descarga,
# no decide por mesa: proyecta lo que la caminata TOMARÍA, con razones.
# El escritor canónico de la cola sigue siendo
# `tools/curador_registro/tsv_crudo.py::upsert_fila`.
# ═══════════════════════════════════════════════════════════════

DIAS_REINTENTO = 7

# Estados que NUNCA se activan en bloque (P2 verbatim: «NO se activan en
# bloque los SIN-FETCH/parciales/negativos»). Cada uno con la razón que
# se emite, para que la exclusión sea legible sin abrir el código.
# `SIN-FETCH` NO vive aquí (ver H3, `ACTO GEN2-ADQ-CONTRATO-FIX`): tiene su
# propia rama, siempre excluyente incluso con `pedida`, porque saltarlo por
# invocación nominal es exactamente el defecto que esa pieza cierra --
# la transformación canónica (`transforma_sin_fetch_autorizada`) es la
# única puerta hacia PENDIENTE.
_RAZON_POR_ESTADO = {
    "OBTENIDO": "OBTENIDO: A.8 ya resuelto, un objeto completo conserva OBTENIDO",
    "NO-ACCESIBLE": ("NO-ACCESIBLE: barrera declarada; solo camina si el operador "
                     "la nombra por ID"),
    "OBTENIDO-PARCIAL": ("OBTENIDO-PARCIAL: el residual necesita cobertura y sucesor "
                         "explícitos; no se activa en bloque"),
}

_RAZON_SIN_FETCH = ("SIN-FETCH: vía localizada pero no abierta; no se activa en bloque, "
                    "requiere autorización de mesa citada en la nota")
_RAZON_SONDA_SIN_AUTORIZAR = ("recomendación de /sonda sin autorización citada: "
                              "permanece propuesta, no habilita adquisición")
_RAZON_FECHA_INDETERMINADA = ("FECHA-INDETERMINADA: la nota trae «intento efectivo» "
                              "con fecha inválida o indecidible; va a conciliación de "
                              "mesa, nunca se infiere una fecha")

# Centinela (H2, `ACTO GEN2-ADQ-CONTRATO-FIX`): distinto de `None` (sin
# intento) y de cualquier `datetime.date` real -- una nota histórica cuyo
# «intento efectivo» trae una fecha inválida o indecidible no se descarta
# ni se infiere: se marca así, explícitamente, para que el llamador la
# mande a conciliación en vez de tratarla como "sin intento previo" (que
# la volvería urgente) o inventarle una fecha (que la volvería medible).
FECHA_INDETERMINADA = object()

_RE_INTENTO_EFECTIVO = re.compile(r"intento efectivo (\d{4}-\d{2}-\d{2})")


def fecha_intento_efectivo(nota):
    """El ÚLTIMO INTENTO DE DESCARGA registrado en la nota, por VALOR de
    fecha -- no el primero que aparece en el texto (H2, revisión del
    9/sep). Solo cuentan entradas explícitamente marcadas `intento
    efectivo <fecha>`; fechas en nombres de archivo, citas documentales,
    enlaces o `descubrimiento de vía <fecha>` (la que escribe `/sonda`)
    NUNCA entran al cómputo -- por construcción, porque el regex no las
    busca fuera de esa etiqueta explícita.

    Devuelve `None` si no hay ningún `intento efectivo` en la nota,
    `FECHA_INDETERMINADA` si hay uno o más pero NINGUNO trae una fecha de
    calendario válida (nota histórica indecidible -- va a conciliación de
    mesa, nunca se presenta una fecha inferida como medida), o la fecha
    máxima entre las válidas si hay al menos una."""
    nota = nota or ""
    crudos = _RE_INTENTO_EFECTIVO.findall(nota)
    if not crudos:
        return None
    validas = []
    for crudo in crudos:
        try:
            validas.append(datetime.date.fromisoformat(crudo))
        except ValueError:
            continue
    if validas:
        return max(validas)
    return FECHA_INDETERMINADA


# A.16: token, no prosa. Una autorización afirmativa e inequívoca se cita
# como `AUTORIZADA:<quién>/<AAAA-MM-DD>/<objeto>` -- el objeto tiene que
# ser la `fuente_canonica` de la fila que se está evaluando, para que una
# cita ajena a otra fila nunca autorice ésta.
_RE_TOKEN_AUTORIZADA = re.compile(
    r"AUTORIZADA:(?P<quien>[^/\s]+)/(?P<fecha>\d{4}-\d{2}-\d{2})/(?P<objeto>[^\s/]+)"
)
# Negación explícita, con guion o con espacio -- se comprueba ANTES que el
# token y manda sobre cualquier coincidencia de éste. H1 (revisión del
# 9/sep): un regex con límites de palabra no basta por sí solo --
# "NO-AUTORIZADA" contiene "AUTORIZADA" como palabra completa igual que
# una autorización afirmativa; lo que distingue el caso es la negación
# explícita, comprobada aparte y con prioridad, no un límite de palabra
# más fino.
_RE_NEGACION_AUTORIZADA = re.compile(r"\bNO[-\s]+AUTORIZAD[AO]S?\b", re.IGNORECASE)


def _autorizada(nota, fuente):
    """Un handoff de `/sonda` habilita adquisición solo con los cuatro
    elementos que P2 exige: objeto faltante + vía nueva + autorización/cita
    + invocación por ID. Esta función resuelve el que falta más a menudo y
    el único mecánicamente legible: la AUTORIZACIÓN citada, explícita e
    inequívoca (A.16: token, no prosa), con referencia verificable a
    quién/cuándo/objeto -- el objeto tiene que ser ESTA fila (`fuente`).

    Ausencia, negación (`NO-AUTORIZADA` / `NO AUTORIZADA`, con guion o con
    espacio) o una cita que nombra otra fila -> `False`. Una
    `SONDA-LATERAL-RECOMENDADA` sin esto permanece propuesta."""
    nota = nota or ""
    if _RE_NEGACION_AUTORIZADA.search(nota):
        return False
    m = _RE_TOKEN_AUTORIZADA.search(nota)
    if not m:
        return False
    return m.group("objeto") == fuente


def _clave_orden(fila):
    """Orden determinista y único (P2: «un solo contrato de elegibilidad y
    orden»). Reconcilia las dos reglas que divergían:

      1. antigüedad primero -- el criterio del runbook: sin intento previo
         antes que con intento, y entre los que tienen intento, el más
         viejo primero;
      2. prioridad después -- el criterio de la skill, como desempate;
      3. `fuente_canonica` al final, para que el orden sea total y la
         misma entrada produzca siempre la misma salida.

    La prioridad numérica ordena antes que la prefijada por tabla de
    origen (`academico-N`, `civil-N`, …), que no comparte escala."""
    fuente, _estado, prioridad, nota = fila
    intento = fecha_intento_efectivo(nota)
    es_fecha = isinstance(intento, datetime.date)
    sin_intento = 0 if (intento is None or not es_fecha) else 1
    orden_intento = intento.toordinal() if es_fecha else 0
    try:
        prio = (0, float(prioridad))
    except (TypeError, ValueError):
        prio = (1, 0.0)
    return (sin_intento, orden_intento, prio, fuente)


def selecciona_filas(filas, corte, maximo=5, nombradas=None):
    """Contrato único de selección. `filas` = iterable de
    `(fuente_canonica, estado_A4A5, prioridad, nota)`; `corte` = la fecha
    contra la que se mide la antigüedad; `nombradas` = IDs que el operador
    pidió explícitamente (los únicos que pueden saltarse la regla de
    antigüedad o un estado que no se activa en bloque).

    Devuelve `{"corte", "maximo", "elegidos", "excluidos"}`. TODA fila cae
    en una de las dos listas y toda exclusión lleva razón -- incluso
    cuando `elegidos` es la lista vacía: una caminata vacía tiene que ser
    distinguible de una selección equivocada."""
    nombradas = set(nombradas or ())
    candidatas, excluidos = [], []
    for fila in filas:
        fuente, estado, prioridad, nota = fila
        base = (estado or "").split("(")[0].strip()
        pedida = fuente in nombradas

        # H3 (ACTO GEN2-ADQ-CONTRATO-FIX): SIN-FETCH NUNCA entra a
        # candidatas desde aquí, ni siquiera con `pedida` -- "no hay rama
        # de excepción que salte estados en el selector". La única puerta
        # hacia PENDIENTE es la transformación canónica
        # (`transforma_sin_fetch_autorizada`, vía el escritor
        # `tsv_crudo.py::upsert_fila`); la invocación nominal solo
        # selecciona sobre estados YA transformados.
        if base == "SIN-FETCH":
            razon = _RAZON_SIN_FETCH
            if "SONDA-LATERAL-RECOMENDADA" in (nota or ""):
                razon = _RAZON_SONDA_SIN_AUTORIZAR
            if pedida:
                razon += (" -- la invocación nominal no salta estados en el "
                          "selector: requiere transformación canónica previa "
                          "(transforma_sin_fetch_autorizada)")
            excluidos.append({"id": fuente, "estado": estado, "razon": razon})
            continue

        if base in _RAZON_POR_ESTADO and not pedida:
            excluidos.append({"id": fuente, "estado": estado,
                              "razon": _RAZON_POR_ESTADO[base]})
            continue

        if base == "PENDIENTE":
            # P1: la invocación nominal NO sustituye la autorización
            # cuando el contrato (handoff de /sonda) exige ambas -- por
            # eso esta comprobación ya no se salta con `pedida`.
            if ("SONDA-LATERAL-RECOMENDADA" in (nota or "")
                    and not _autorizada(nota, fuente)):
                excluidos.append({"id": fuente, "estado": estado,
                                  "razon": _RAZON_SONDA_SIN_AUTORIZAR})
                continue
            intento = fecha_intento_efectivo(nota)
            if intento is FECHA_INDETERMINADA and not pedida:
                excluidos.append({"id": fuente, "estado": estado,
                                  "razon": _RAZON_FECHA_INDETERMINADA})
                continue
            candidatas.append(fila)
            continue

        if base == "NO-OBTENIDO-POR-ESTE-AGENTE":
            intento = fecha_intento_efectivo(nota)
            if intento is FECHA_INDETERMINADA and not pedida:
                excluidos.append({"id": fuente, "estado": estado,
                                  "razon": _RAZON_FECHA_INDETERMINADA})
                continue
            if pedida or intento is None:
                candidatas.append(fila)
                continue
            dias = (corte - intento).days
            if dias >= DIAS_REINTENTO:
                candidatas.append(fila)
            else:
                excluidos.append({
                    "id": fuente, "estado": estado,
                    "razon": (f"reintento demasiado pronto: intento efectivo "
                              f"{intento.isoformat()}, {dias} días < "
                              f"{DIAS_REINTENTO}")})
            continue
        excluidos.append({"id": fuente, "estado": estado,
                          "razon": f"estado {estado!r} fuera del contrato de elegibilidad"})

    candidatas.sort(key=_clave_orden)
    elegidos = []
    for fila in candidatas:
        fuente, estado, prioridad, nota = fila
        if len(elegidos) >= maximo:
            excluidos.append({"id": fuente, "estado": estado,
                              "razon": f"elegible, fuera del tope de esta caminata "
                                       f"(maximo={maximo})"})
            continue
        intento = fecha_intento_efectivo(nota)
        es_fecha = isinstance(intento, datetime.date)
        if es_fecha:
            razon = f"último intento efectivo {intento.isoformat()}, {(corte - intento).days} días"
        elif intento is FECHA_INDETERMINADA:
            razon = _RAZON_FECHA_INDETERMINADA + " (seleccionada por invocación nominal)"
        else:
            razon = "sin intento previo registrado"
        elegidos.append({
            "id": fuente, "estado": estado, "prioridad": prioridad,
            "intento_efectivo": intento.isoformat() if es_fecha else None,
            "razon": razon})
    return {"corte": corte.isoformat(), "maximo": maximo,
            "elegidos": elegidos, "excluidos": excluidos}


RUTA_COLA = os.path.join(RAIZ, "data", "curacion-registro",
                         "cola-adquisicion-registro.tsv")


def lee_cola(ruta=RUTA_COLA):
    """Lee la cola CANÓNICA en solo lectura y proyecta las cuatro columnas
    que el contrato usa. No escribe nada: el escritor sigue siendo
    `tsv_crudo.py::upsert_fila`."""
    import csv
    filas = []
    with open(ruta, encoding="utf-8", newline="") as f:
        for d in csv.DictReader(f, delimiter="\t"):
            filas.append((d.get("fuente_canonica", ""), d.get("estado_A4A5", ""),
                          d.get("prioridad", ""), d.get("nota", "")))
    return filas


def transforma_sin_fetch_autorizada(fuente, ruta=RUTA_COLA):
    """Transformación CANÓNICA (P3/H3, `ACTO GEN2-ADQ-CONTRATO-FIX`): una
    fila `SIN-FETCH` con autorización afirmativa e inequívoca
    (`_autorizada`) pasa a su estado accionable (`PENDIENTE`), con la cita
    conservada en `nota` -- ANTES de que el selector la considere, nunca al
    revés. El escritor sigue siendo
    `tools/curador_registro/tsv_crudo.py::upsert_fila`; esta función solo
    decide y arma la fila nueva, no reimplementa el TSV.

    Es la ÚNICA puerta hacia PENDIENTE para una fila `SIN-FETCH`: el
    selector (`selecciona_filas`) nunca salta ese estado por invocación
    nominal, con o sin autorización -- ver H3.

    Devuelve `(ok: bool, razon: str)`. No transforma nada si la fila no
    existe, si su estado actual no es `SIN-FETCH`, o si su autorización no
    es afirmativa e inequívoca para ESTA fila."""
    ruta_tsv_crudo = os.path.join(RAIZ, "tools", "curador_registro")
    if ruta_tsv_crudo not in sys.path:
        sys.path.insert(0, ruta_tsv_crudo)
    import tsv_crudo
    from pathlib import Path

    ruta_p = Path(ruta)
    lineas = tsv_crudo.leer_lineas(ruta_p)
    if not lineas:
        return False, f"{ruta}: archivo vacío, no se transforma nada"
    campos = lineas[0].split("\t")
    filas = tsv_crudo.leer_dicts(ruta_p)
    fila = next((f for f in filas if f.get("fuente_canonica") == fuente), None)
    if fila is None:
        return False, f"{fuente}: no existe en {ruta}"
    base = (fila.get("estado_A4A5") or "").split("(")[0].strip()
    if base != "SIN-FETCH":
        return False, (f"{fuente}: estado actual {fila.get('estado_A4A5')!r} no es "
                       f"SIN-FETCH, no se transforma")
    nota = fila.get("nota", "")
    if not _autorizada(nota, fuente):
        return False, (f"{fuente}: sin autorización afirmativa e inequívoca citada "
                       f"para esta fila; permanece SIN-FETCH")
    nueva = dict(fila)
    nueva["estado_A4A5"] = "PENDIENTE"
    tsv_crudo.upsert_fila(ruta_p, nueva, campos, clave="fuente_canonica")
    return True, (f"{fuente}: SIN-FETCH -> PENDIENTE (transformación canónica, "
                  f"autorización citada conservada en nota)")


SECCIONES = [
    ("entorno", check_entorno),
    ("configuracion_operativa", check_configuracion_operativa),
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
    ap.add_argument("--selecciona", action="store_true",
                    help="proyecta la selección de la próxima caminata de /adquiere "
                         "sobre la cola canónica (solo lectura): IDs elegidos, "
                         "excluidos y razón -- incluso cuando son cero")
    ap.add_argument("--maximo", type=int, default=5,
                    help="tope de filas de la caminata proyectada (default 5)")
    ap.add_argument("--nombrada", action="append", default=[],
                    help="ID que el operador pide explícitamente; repetible")
    ap.add_argument("--transforma-sin-fetch", metavar="ID",
                    help="transformación canónica (H3): con autorización afirmativa "
                         "e inequívoca ya asentada en la nota de esa fila, la pasa de "
                         "SIN-FETCH a PENDIENTE. Única puerta -- el selector nunca "
                         "salta ese estado por invocación nominal")
    a = ap.parse_args()
    if a.transforma_sin_fetch:
        ok, razon = transforma_sin_fetch_autorizada(a.transforma_sin_fetch)
        if a.json:
            print(json.dumps({"ok": ok, "razon": razon}, ensure_ascii=False))
        else:
            print(("OK: " if ok else "NO: ") + razon)
        return 0 if ok else 1
    if a.selecciona:
        r = selecciona_filas(lee_cola(), corte=datetime.date.today(),
                             maximo=a.maximo, nombradas=a.nombrada)
        if a.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"SELECCIÓN /adquiere · corte {r['corte']} · maximo {r['maximo']}")
            print(f"\nELEGIDOS ({len(r['elegidos'])}):")
            for e in r["elegidos"] or [None]:
                print(f"  {e['id']} [{e['estado']}] -- {e['razon']}" if e
                      else "  (ninguno -- caminata vacía, no selección equivocada)")
            print(f"\nEXCLUIDOS ({len(r['excluidos'])}):")
            for e in r["excluidos"]:
                print(f"  {e['id']} [{e['estado']}] -- {e['razon']}")
        return 0
    reporte = recolecta()
    if a.json:
        print(json.dumps(reporte, ensure_ascii=False, indent=2, default=str))
    else:
        imprime_texto(reporte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
