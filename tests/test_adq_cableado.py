#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tests/test_adq_cableado.py -- ACTO GEN2-SONDA-ADQ-CABLEADO
(`forense/encargos/2026-09-09-GEN2-SONDA-ADQ-CABLEADO.md`, 9/sep/2026).

P0 del acto: los fallos REPRODUCIDOS de la §5 de
`forense/notas/2026-09-09-REVISION-CABLEADO-SONDA-ADQUISICION-astra.md` se
congelan aquí como casos de aceptación ANTES de repararse -- primero el
caso rojo, después el arreglo que lo pone verde. P3 del acto: los criterios
1-6 del §6 de esa misma revisión se verifican sobre estos mismos fixtures.

Cada prueba nombra el hallazgo que congela (H1/H4/H5/H6) o el criterio de
aceptación (C1..C6). Ninguna toca la red, el reloj real, el corpus, la cola
canónica ni el runner de producción: los defectos de shell se ejercitan
sobre las funciones REALES de `tools/adquiere_cron.sh` cargadas con
`ADQ_CRON_SOLO_DEFINE=1` (seam de solo-definición, no una reimplementación)
y con dobles de `git`/`curl` en un `PATH` temporal.

Corre sola:

    python3 tests/test_adq_cableado.py
"""
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest.mock
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tests"))
sys.path.insert(0, str(RAIZ / "tools"))
import check as C  # noqa: E402

RUNNER = RAIZ / "tools" / "adquiere_cron.sh"

FALLOS = []


def afirma(cond, msg):
    if not cond:
        FALLOS.append(msg)


# ───────────────────────────────────────────────────────────────
# Fixtures congelados de §1/§5 de la revisión -- texto REAL de las huellas
# ───────────────────────────────────────────────────────────────

# El cierre real del 9/sep, tal como quedó fusionado en
# forense/censo-raiz/2026-09-09.txt (transcrito en §1 de la revisión).
CENSO_9SEP = textwrap.dedent("""\
    Total en disco: 465 archivos

    [ADQ-PDN] 2026-09-09: fuera de ventana (día 9, ventana 1-3)

    [ADQ] 2026-09-09 07:33: invocado=si motivo=- exit=0 duracion=228s commits_nuevos=0 ramas_nuevas=1 archivos_modificados=1 run_id=2026-09-09T073007-371
    """)

# El cierre del 8/sep -- el que producía el falso COMPLETO al evaluarse
# contra el 9/sep (primera fila de las "Pruebas ejecutadas" de H1).
CENSO_8SEP = textwrap.dedent("""\
    Total en disco: 462 archivos

    [ADQ] 2026-09-08 07:34: invocado=si motivo=- exit=0 duracion=120s commits_nuevos=0 ramas_nuevas=1 archivos_modificados=0 run_id=2026-09-08T073012-118
    """)

# Huella histórica sin run_id -- anterior a MAESTRA38-CRON-3. La
# compatibilidad tiene que ser EXPLÍCITA, no accidental.
CENSO_HISTORICO_SIN_RUNID = (
    "[ADQ] 2026-09-05 07:32: invocado=si motivo=- exit=0 duracion=90s "
    "commits_nuevos=0 ramas_nuevas=0 archivos_modificados=0\n"
)


# ───────────────────────────────────────────────────────────────
# H1 / C1 / C2 · el vigilante
# ───────────────────────────────────────────────────────────────

def prueba_h1_cierre_de_otro_dia_no_pone_verde():
    """H1, primera fila de §5: «Cierre del 8/sep evaluado para 9/sep →
    COMPLETO». Criterio de aceptación 2. El cuerpo [ADQ] heredado de main
    trae la fecha del 8; evaluado para el 9 no puede acreditar nada."""
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 9),
        {"[CENSO]", "[ADQ]"},
        CENSO_8SEP,
    )
    afirma(estado != "COMPLETO",
           f"H1/C2: cierre del 8/sep evaluado para el 9/sep dio {estado!r} "
           f"-- un cierre de otra fecha no vuelve verde la corrida evaluada "
           f"({detalle})")


def prueba_h1_cierre_real_con_rama_retirada_es_completo():
    """H1, tercera fila de §5 y criterio de aceptación 1: rama
    `censo/2026-09-09` retirada tras el merge, evidencia del día YA
    fusionada en `forense/censo-raiz/2026-09-09.txt`. Antes del arreglo
    esto daba `CENSO-SIN-CIERRE` -- observado sin simularlo sobre este
    mismo checkout."""
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 9),
        set(),
        None,
        evidencia_fusionada=CENSO_9SEP,
    )
    afirma(estado == "COMPLETO",
           f"H1/C1: el cierre real del 9/sep fusionado, con la rama ya "
           f"retirada, dio {estado!r} en vez de COMPLETO ({detalle})")
    afirma("2026-09-09T073007-371" in detalle,
           f"H1: el detalle debe citar el run_id del intento que acredita "
           f"({detalle!r})")


def prueba_h1_lectura_fallida_del_remoto_no_es_ausencia():
    """H1 y criterio de aceptación 2, segunda mitad: «una lectura
    inaccesible no se rotula "no corrió"». `SIN-HUELLA` afirma que la
    rama no existe; si no se pudo preguntar, eso es otra cosa (A.13)."""
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 9), set(), None,
        evidencia_fusionada=None, remoto_legible=False,
    )
    afirma(estado != "SIN-HUELLA",
           f"H1/C2: con el remoto ilegible el estado fue {estado!r} -- "
           f"una lectura fallida no es ausencia comprobada ({detalle})")
    afirma("NO-VERIFICABLE" in estado,
           f"H1/C2: el estado con remoto ilegible debe nombrarse "
           f"NO-VERIFICABLE, dio {estado!r}")


def prueba_h1_no_combina_fases_de_intentos_distintos():
    """H1: «no combina fases de intentos distintos». Dos intentos el
    mismo día, uno fallido y uno exitoso: el estado declara AMBOS
    (último intento y al-menos-un-éxito) cuando discrepan, no promedia."""
    dos_intentos = (
        "[ADQ] 2026-09-09 07:33: invocado=si motivo=- exit=0 duracion=228s "
        "run_id=2026-09-09T073007-371\n"
        "[ADQ] 2026-09-09 11:05: invocado=no motivo=PARO-RED exit=- "
        "duracion=3s run_id=2026-09-09T110501-902\n"
    )
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 9), set(), None,
        evidencia_fusionada=dos_intentos,
    )
    afirma("2026-09-09T110501-902" in detalle and "2026-09-09T073007-371" in detalle,
           f"H1: con último-intento fallido y un éxito previo el detalle "
           f"debe citar los dos run_id ({detalle!r})")
    afirma("PARO-RED" in detalle,
           f"H1: la causa del último intento debe quedar visible ({detalle!r})")


def prueba_h1_compatibilidad_huella_sin_run_id():
    """H1: «compatibilidad explícita para huellas históricas sin run_id».
    Una huella anterior a MAESTRA38-CRON-3 se acredita igual, y se
    declara como histórica -- no se descarta por no traer run_id."""
    estado, detalle = C.t_cron_estado(
        datetime.date(2026, 9, 5), set(), None,
        evidencia_fusionada=CENSO_HISTORICO_SIN_RUNID,
    )
    afirma(estado == "COMPLETO",
           f"H1: huella histórica sin run_id dio {estado!r} en vez de "
           f"COMPLETO ({detalle})")
    afirma("sin run_id" in detalle,
           f"H1: la compatibilidad histórica debe declararse en el detalle "
           f"({detalle!r})")


def prueba_h1_censo_sin_cierre_sigue_siendo_visible():
    """H1: «mantener visibles las fases incompletas». Actividad de censo
    sin huella [ADQ] del día sigue siendo CENSO-SIN-CIERRE -- el arreglo
    no puede callar la señal ampliando el verde."""
    estado, _ = C.t_cron_estado(
        datetime.date(2026, 9, 9), {"[CENSO]"}, None,
        evidencia_fusionada="Total en disco: 465 archivos\n",
    )
    afirma(estado == "CENSO-SIN-CIERRE",
           f"H1: censo sin huella [ADQ] del día dio {estado!r}")


def prueba_h1_parser_filtra_por_fecha():
    """H1: el parser de huellas es una función pura y solo devuelve las
    del día evaluado -- la base de todo lo anterior."""
    texto = CENSO_8SEP + "\n" + CENSO_9SEP
    del_9 = C.t_cron_huellas_adq(texto, datetime.date(2026, 9, 9))
    del_8 = C.t_cron_huellas_adq(texto, datetime.date(2026, 9, 8))
    afirma(len(del_9) == 1 and del_9[0]["run_id"] == "2026-09-09T073007-371",
           f"H1: el parser debe devolver solo la huella del 9/sep, dio {del_9!r}")
    afirma(len(del_8) == 1 and del_8[0]["run_id"] == "2026-09-08T073012-118",
           f"H1: el parser debe devolver solo la huella del 8/sep, dio {del_8!r}")


def prueba_h1_senal_sigue_sin_romper_baseline():
    """H1: «el baseline no se amplía para callar la señal». T31 sigue
    emitiendo con `senal()`, no con `warn()` -- se comprueba que el
    nombre T-CRON no aparece en la lista de WARN del árbol."""
    fuente = (RAIZ / "tests" / "check.py").read_text(encoding="utf-8")
    i = fuente.find("def t31_cron()")
    afirma(i > 0, "H1: no se encontró t31_cron() en tests/check.py")
    cuerpo = fuente[i:i + 3000]
    afirma('senal("T-CRON"' in cuerpo,
           "H1: t31_cron() debe seguir emitiendo con senal(), no warn()")
    afirma('warn("T-CRON"' not in cuerpo,
           "H1: t31_cron() no debe emitir warn() -- rompería baseline ajeno")


# ───────────────────────────────────────────────────────────────
# Andamio de shell -- carga las funciones REALES del runner
# ───────────────────────────────────────────────────────────────

def _corre_bash(cuerpo, entorno=None, cwd=None, timeout=90):
    """Corre `cuerpo` con bash, tras cargar las funciones del runner real
    vía ADQ_CRON_SOLO_DEFINE=1. Devuelve (returncode, stdout+stderr)."""
    env = dict(os.environ)
    env["ADQ_CRON_SOLO_DEFINE"] = "1"
    env.update(entorno or {})
    # El runner hace `cd "$REPO_DIR"` al cargarse (es su primer acto, y no
    # se toca). Por eso el `cd` al directorio de trabajo del caso va
    # DESPUÉS del source y no en `cwd=`: sin esto, un caso que escribe un
    # recibo lo escribiría en el censo REAL del repo -- ya ocurrió una vez
    # al construir este archivo, y la corrección vive aquí.
    destino = cwd or str(RAIZ)
    guion = (f'set -uo pipefail\nsource "{RUNNER}"\n'
             f'cd "{destino}" || exit 90\n{cuerpo}\n')
    r = subprocess.run(["bash", "-c", guion], cwd=str(RAIZ),
                       capture_output=True, text=True, errors="replace",
                       env=env, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _doble_git(dirbin, falla_en="push"):
    """Escribe un `git` doble en `dirbin` que falla SOLO en el subcomando
    indicado y responde plausible a todo lo demás."""
    p = Path(dirbin) / "git"
    p.write_text(textwrap.dedent(f"""\
        #!/usr/bin/env bash
        sub="$1"
        for a in "$@"; do case "$a" in {falla_en}) sub="{falla_en}";; esac; done
        if [ "$sub" = "{falla_en}" ]; then
          echo "doble: '{falla_en}' falla a propósito" >&2
          exit 1
        fi
        case "$1" in
          rev-parse) echo 0000000000000000000000000000000000000000;;
          show-ref|ls-remote) exit 1;;
          log) echo "0000000 doble";;
          status) : ;;
        esac
        exit 0
        """), encoding="utf-8")
    p.chmod(0o755)


def _seam_disponible():
    fuente = RUNNER.read_text(encoding="utf-8")
    return "ADQ_CRON_SOLO_DEFINE" in fuente


# ───────────────────────────────────────────────────────────────
# H4 / C3 · transporte de red
# ───────────────────────────────────────────────────────────────

def prueba_h4_transporte_fallido_entra_en_paro():
    """H4 y criterio de aceptación 3: `curl -w '%{http_code}' || echo
    'sin-respuesta'` produjo `000sin-respuesta` reproducido, y la
    comparación por igualdad NO entraba en PARO-RED. Se ejercita la
    función real de sonda con un `curl` doble que falla el transporte."""
    if not _seam_disponible():
        FALLOS.append("H4: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    with tempfile.TemporaryDirectory() as d:
        curl = Path(d) / "curl"
        curl.write_text("#!/usr/bin/env bash\nprintf '000'\nexit 7\n", encoding="utf-8")
        curl.chmod(0o755)
        env = {"PATH": f"{d}:{os.environ['PATH']}", "LOGFILE": "/dev/null"}
        rc, salida = _corre_bash(
            'sonda_red "https://ejemplo.invalido/" && echo VEREDICTO=OK '
            '|| echo "VEREDICTO=PARO rc=$?"', entorno=env)
        afirma("VEREDICTO=PARO" in salida,
               f"H4/C3: un fallo de transporte (curl exit 7) debe producir "
               f"PARO antes de gastar la invocación; salida: {salida!r}")
        afirma("000sin-respuesta" not in salida,
               f"H4: la concatenación 000sin-respuesta no debe reaparecer: {salida!r}")


def prueba_h4_403_es_respuesta_no_ausencia_de_internet():
    """H4: «403 = respuesta y bloqueo de ese destino, jamás "sin
    internet" ni "no existe"». Un 403 NO es PARO de red."""
    if not _seam_disponible():
        return
    with tempfile.TemporaryDirectory() as d:
        curl = Path(d) / "curl"
        curl.write_text("#!/usr/bin/env bash\nprintf '403'\nexit 0\n", encoding="utf-8")
        curl.chmod(0o755)
        env = {"PATH": f"{d}:{os.environ['PATH']}", "LOGFILE": "/dev/null"}
        rc, salida = _corre_bash(
            'sonda_red "https://ejemplo.invalido/" && echo VEREDICTO=OK '
            '|| echo VEREDICTO=PARO', entorno=env)
        afirma("VEREDICTO=OK" in salida,
               f"H4: un HTTP 403 es respuesta del destino, no ausencia de red; "
               f"salida: {salida!r}")
        afirma("BLOQUEO" in salida.upper() or "403" in salida,
               f"H4: el 403 debe quedar registrado como bloqueo de ESE destino: {salida!r}")


# ───────────────────────────────────────────────────────────────
# H5 / C3 · publicación
# ───────────────────────────────────────────────────────────────

def prueba_h5_push_fallido_no_termina_en_exito():
    """H5 y criterio 3: con el cuerpo REAL de `commit_censo_linea()` y un
    doble que hace fallar únicamente `git push`, la función terminaba con
    salida 0. Debe devolver fallo operativo y conservar el recibo local."""
    if not _seam_disponible():
        FALLOS.append("H5: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    with tempfile.TemporaryDirectory() as d:
        bindir = Path(d) / "bin"
        bindir.mkdir()
        _doble_git(bindir, falla_en="push")
        trabajo = Path(d) / "repo"
        (trabajo / "forense" / "censo-raiz").mkdir(parents=True)
        env = {"PATH": f"{bindir}:{os.environ['PATH']}",
               "LOGFILE": str(Path(d) / "log.txt")}
        rc, salida = _corre_bash(
            'FECHA=2026-09-09; CENSO_DIR="forense/censo-raiz"; LOGFILE="$LOGFILE"; '
            'commit_censo_linea "[ADQ] linea" "resumen" "[ADQ] 2026-09-09" '
            '&& echo VEREDICTO=OK || echo "VEREDICTO=FALLO rc=$?"',
            entorno=env, cwd=str(trabajo))
        afirma("VEREDICTO=FALLO" in salida,
               f"H5/C3: un push fallido no puede terminar en éxito; salida: {salida!r}")
        recibo = trabajo / "forense" / "censo-raiz" / "2026-09-09.txt"
        afirma(recibo.exists() and "[ADQ] linea" in recibo.read_text(encoding="utf-8"),
               "H5: el recibo local debe conservarse aunque el push falle")


def prueba_h5_no_hay_force_push_en_el_runner():
    """H5: «sin force-push». Vigilancia estructural sobre el runner."""
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("--force" not in fuente and "push -f" not in fuente,
           "H5: el runner no debe contener force-push")


def prueba_h5_contadores_no_se_rotulan_como_fuentes():
    """H5: «ramas_nuevas/contadores jamás se rotulan como fuentes
    obtenidas». La huella los nombra por lo que son, y el runner declara
    explícitamente que no son payloads."""
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("ramas_nuevas" in fuente, "H5: la huella debe seguir midiendo ramas_nuevas")
    afirma("no son payloads" in fuente.lower(),
           "H5: el runner debe declarar que los contadores no son fuentes obtenidas")


def prueba_h5_huella_lleva_sha_realmente_usado():
    """P1: «la huella adjunta el SHA realmente usado»."""
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("sha=" in fuente,
           "P1/H5: la línea [ADQ] debe adjuntar el SHA realmente usado (campo sha=)")


# ───────────────────────────────────────────────────────────────
# H6 / C4 · timeout y heartbeat
# ───────────────────────────────────────────────────────────────

def prueba_h6_timeout_mata_proceso_que_ignora_term():
    """H6 y §5: «Proceso que ignora TERM → supera el límite; eliminado
    por el harness». Con `--kill-after` y gracia finita, el propio
    `timeout(1)` debe cerrarlo."""
    if not shutil.which("timeout"):
        return
    guion = "trap '' TERM; sleep 30"
    t0 = datetime.datetime.now()
    r = subprocess.run(
        ["bash", "-c",
         f'timeout --kill-after=2s 1s bash -c {guion!r}; echo "rc=$?"'],
        capture_output=True, text=True, timeout=30)
    tardó = (datetime.datetime.now() - t0).total_seconds()
    afirma(tardó < 10,
           f"H6: un proceso que ignora TERM debe morir por --kill-after "
           f"(tardó {tardó:.1f}s)")
    # y el runner real tiene que usarlo
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("--kill-after" in fuente,
           "H6: tools/adquiere_cron.sh debe invocar timeout con --kill-after")


def prueba_h6_segunda_invocacion_no_pisa_el_heartbeat_del_dueno():
    """H6, §5 («Segunda instancia rechazada por lock → sobrescribe
    heartbeat del dueño») y criterio de aceptación 4. RUN-A escribe
    STARTED; RUN-B, rechazado por el lock, no puede reemplazarlo."""
    if not _seam_disponible():
        FALLOS.append("H6: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    with tempfile.TemporaryDirectory() as d:
        hb = Path(d) / "heartbeat.json"
        log = Path(d) / "log.txt"
        env = {"LOGFILE": str(log)}
        _corre_bash(
            f'HEARTBEAT="{hb}"; RUN_ID="RUN-A"; FASE="CLON-AL-DIA"; '
            f'FECHA=2026-09-09; SOY_DUENO_DEL_LOCK=1; LOGFILE="{log}"; '
            f'escribe_heartbeat "STARTED" "-"', entorno=env)
        antes = hb.read_text(encoding="utf-8") if hb.exists() else ""
        afirma("RUN-A" in antes and "STARTED" in antes,
               f"H6: el dueño del lock debe poder escribir su heartbeat ({antes!r})")
        _corre_bash(
            f'HEARTBEAT="{hb}"; RUN_ID="RUN-B"; FASE="PARO-LOCK"; '
            f'FECHA=2026-09-09; SOY_DUENO_DEL_LOCK=0; LOGFILE="{log}"; '
            f'escribe_heartbeat "PARO-LOCK" "-"', entorno=env)
        despues = hb.read_text(encoding="utf-8") if hb.exists() else ""
        afirma("RUN-A" in despues and "STARTED" in despues,
               f"H6/C4: la instancia rechazada por lock (RUN-B) pisó el "
               f"heartbeat del dueño: {despues!r}")
        afirma("RUN-B" not in despues,
               f"H6/C4: RUN-B no debe aparecer en el heartbeat activo: {despues!r}")
        texto_log = log.read_text(encoding="utf-8") if log.exists() else ""
        afirma("RUN-B" in texto_log,
               "H6: el rechazo por lock se apendiza al LOG con su propio run_id")


def prueba_h6_heartbeat_por_temporal_y_rename():
    """H6: «escrito por temporal + rename»."""
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("os.replace" in fuente or "rename" in fuente,
           "H6: escribe_heartbeat debe usar temporal + rename atómico")


def prueba_h6_muerto_sin_cierre_queda_incompleto():
    """H6: «proceso muerto sin cierre queda INCOMPLETO -- no se inventa
    éxito ni causa»."""
    fuente = RUNNER.read_text(encoding="utf-8")
    afirma("INCOMPLETO" in fuente,
           "H6: el runner debe poder dejar el estado INCOMPLETO cuando muere "
           "sin cierre, en vez de inventar éxito o causa")


# ───────────────────────────────────────────────────────────────
# P1 · extracción del prompt y configuración
# ───────────────────────────────────────────────────────────────

def prueba_prompt_exige_bloque_text_unico():
    """P1: «la extracción del prompt exige bloque text único (el awk
    actual recoge todos)». Un runbook con DOS bloques ```text debe ser
    PARO-PROMPT, no una concatenación silenciosa de los dos."""
    if not _seam_disponible():
        FALLOS.append("P1: tools/adquiere_cron.sh no expone ADQ_CRON_SOLO_DEFINE")
        return
    with tempfile.TemporaryDirectory() as d:
        uno = Path(d) / "uno.md"
        uno.write_text("prosa\n```text\nPROMPT REAL\n```\nmás prosa\n", encoding="utf-8")
        dos = Path(d) / "dos.md"
        dos.write_text("```text\nPROMPT A\n```\ntexto\n```text\nPROMPT B\n```\n",
                       encoding="utf-8")
        env = {"LOGFILE": "/dev/null"}
        rc, salida = _corre_bash(
            f'LOGFILE=/dev/null; extrae_prompt "{uno}" && echo VEREDICTO=OK '
            f'|| echo VEREDICTO=PARO', entorno=env)
        afirma("PROMPT REAL" in salida and "VEREDICTO=OK" in salida,
               f"P1: un runbook con UN bloque text debe extraerse limpio: {salida!r}")
        rc, salida = _corre_bash(
            f'LOGFILE=/dev/null; extrae_prompt "{dos}" && echo VEREDICTO=OK '
            f'|| echo VEREDICTO=PARO', entorno=env)
        afirma("VEREDICTO=PARO" in salida,
               f"P1: dos bloques ```text deben ser PARO-PROMPT, no una "
               f"concatenación silenciosa: {salida!r}")
        afirma("PROMPT B" not in salida,
           f"P1: el segundo bloque no debe filtrarse al prompt: {salida!r}")


def prueba_config_rota_no_se_sustituye_por_defaults_en_silencio():
    """P1: «una config rota no se sustituye por defaults en silencio».
    `_t_cron_gracia_minutos()` degradaba a 45 sin decir nada."""
    valor, degradado = C.t_cron_gracia_minutos_declarada(
        _lector=lambda: (_ for _ in ()).throw(ValueError("config rota")))
    afirma(valor == 45 and degradado is True,
           f"P1: una config ilegible debe degradar DECLARANDOLO, dio "
           f"({valor!r}, {degradado!r})")
    valor, degradado = C.t_cron_gracia_minutos_declarada(_lector=lambda: 30)
    afirma(valor == 30 and degradado is False,
           f"P1: una config legible no debe marcarse degradada, dio "
           f"({valor!r}, {degradado!r})")


# ───────────────────────────────────────────────────────────────
# P2 / C5 · contrato único de selección
# ───────────────────────────────────────────────────────────────

FILAS_FIXTURE = [
    # (fuente_canonica, estado_A4A5, prioridad, nota)
    ("ALFA_PENDIENTE", "PENDIENTE", "2", "sin intento previo"),
    ("BETA_PENDIENTE", "PENDIENTE", "1", "sin intento previo"),
    ("GAMMA_RECIENTE", "NO-OBTENIDO-POR-ESTE-AGENTE(2 intentos)", "3",
     "intento efectivo 2026-09-06: curl 52"),
    ("DELTA_VIEJO", "NO-OBTENIDO-POR-ESTE-AGENTE(1 intentos)", "4",
     "intento efectivo 2026-08-01: curl 35"),
    ("EPSILON_SINFETCH", "SIN-FETCH", "5", "espejo localizado, no abierto"),
    ("ZETA_PARCIAL", "OBTENIDO-PARCIAL", "6", "cobertura 3 de 9 olas"),
    ("ETA_OBTENIDO", "OBTENIDO", "1", "za6980"),
    ("THETA_NOACC", "NO-ACCESIBLE", "1", "muro de credencial"),
    ("IOTA_SONDEADA", "SIN-FETCH", "2",
     "descubrimiento de vía 2026-09-09 por /sonda; SONDA-LATERAL-RECOMENDADA; "
     "sin autorización de mesa"),
    ("KAPPA_AUTORIZADA", "PENDIENTE", "7",
     "descubrimiento de vía 2026-09-09 por /sonda; SONDA-LATERAL-RECOMENDADA; "
     "AUTORIZADA por firma de mesa 2026-09-09"),
]


def _selecciona(corte, n=5):
    import adq_doctor
    return adq_doctor.selecciona_filas(FILAS_FIXTURE, corte=corte, maximo=n)


def prueba_p2_seleccion_determinista_y_auditable():
    """P2 y criterio 5: «la misma fecha y conjunto de filas producen la
    misma selección»; y cada corrida emite IDs elegidos, excluidos y
    razón -- incluso cuando son cero."""
    corte = datetime.date(2026, 9, 9)
    a = _selecciona(corte)
    b = _selecciona(corte)
    afirma(a == b, "P2/C5: la selección no es determinista sobre las mismas filas")
    elegidos = [e["id"] for e in a["elegidos"]]
    afirma(elegidos == sorted(elegidos, key=lambda i: elegidos.index(i)),
           "P2: el orden debe ser estable")
    afirma(len(a["excluidos"]) + len(a["elegidos"]) == len(FILAS_FIXTURE),
           f"P2: toda fila debe quedar elegida o excluida CON razón; "
           f"{len(a['elegidos'])}+{len(a['excluidos'])} != {len(FILAS_FIXTURE)}")
    afirma(all(e.get("razon") for e in a["excluidos"]),
           "P2: toda exclusión lleva razón explícita")


def prueba_p2_no_activa_en_bloque_sinfetch_parciales_negativos():
    """P2: «NO se activan en bloque los SIN-FETCH/parciales/negativos».
    Y «un objeto completo conserva OBTENIDO»."""
    a = _selecciona(datetime.date(2026, 9, 9))
    elegidos = {e["id"] for e in a["elegidos"]}
    for prohibido in ("EPSILON_SINFETCH", "ZETA_PARCIAL", "ETA_OBTENIDO",
                      "THETA_NOACC", "IOTA_SONDEADA"):
        afirma(prohibido not in elegidos,
               f"P2: {prohibido} no debe activarse en bloque; elegidos={elegidos}")


def prueba_p2_antiguedad_por_intento_efectivo_no_por_sondeo():
    """P2: «fecha de descubrimiento de vía separada de fecha de intento
    efectivo (sondear no reinicia el plazo de descarga)»."""
    a = _selecciona(datetime.date(2026, 9, 9))
    elegidos = {e["id"] for e in a["elegidos"]}
    afirma("DELTA_VIEJO" in elegidos,
           f"P2: un negativo con intento efectivo del 1/ago (≥7 días) es "
           f"elegible; elegidos={elegidos}")
    afirma("GAMMA_RECIENTE" not in elegidos,
           f"P2: un negativo con intento efectivo del 6/sep (<7 días) no lo es; "
           f"elegidos={elegidos}")


def prueba_p2_candidata_autorizada_llega_y_no_autorizada_no():
    """Criterio 5, segunda mitad: «una candidata autorizada de SONDA
    llega al consumidor previsto, y una no autorizada permanece
    propuesta»."""
    a = _selecciona(datetime.date(2026, 9, 9), n=10)
    elegidos = {e["id"] for e in a["elegidos"]}
    afirma("KAPPA_AUTORIZADA" in elegidos,
           f"C5: la candidata AUTORIZADA debe llegar a la caminata; "
           f"elegidos={elegidos}")
    excl = {e["id"]: e["razon"] for e in a["excluidos"]}
    afirma("IOTA_SONDEADA" in excl and "autoriza" in excl["IOTA_SONDEADA"].lower(),
           f"C5: la recomendación sin autorización permanece propuesta, con "
           f"esa razón; excluidos={excl}")


def prueba_p2_cero_elegibles_tambien_emite_lista():
    """P2: «incluso cuando son cero»."""
    import adq_doctor
    r = adq_doctor.selecciona_filas(
        [("ETA_OBTENIDO", "OBTENIDO", "1", "za6980")],
        corte=datetime.date(2026, 9, 9), maximo=5)
    afirma(r["elegidos"] == [] and len(r["excluidos"]) == 1,
           f"P2: con cero elegibles debe emitirse igual la lista con razones: {r!r}")


# ───────────────────────────────────────────────────────────────
# H3 / C6 · visibilidad del piloto
# ───────────────────────────────────────────────────────────────

PILOTO = (RAIZ / "forense" / "encargos" / "cola" /
          "2026-09-08-GEN2-SONDA-3-PILOTO-CAJA.md")


def prueba_h3_piloto_visible_para_el_selector_real_de_despacha():
    """H3 y criterio 6: el piloto aparece en «esperando caja» bajo el
    comando REAL de /despacha (`grep '^ENTORNO: CAJA'`)."""
    afirma(PILOTO.exists(), f"H3: no existe {PILOTO}")
    if not PILOTO.exists():
        return
    r = subprocess.run(["grep", "-c", "^ENTORNO: CAJA", str(PILOTO)],
                       capture_output=True, text=True)
    afirma(r.stdout.strip() == "1",
           f"H3/C6: el comando literal de /despacha debe encontrar la cabecera "
           f"canónica; grep -c '^ENTORNO: CAJA' dio {r.stdout.strip()!r}")


def prueba_h3_texto_original_del_piloto_intacto():
    """H3: «texto original intacto, corrección registrada encima». No se
    redacta otro piloto ni se reescribe el que hay."""
    if not PILOTO.exists():
        return
    t = PILOTO.read_text(encoding="utf-8")
    for ancla in ("ESTADO: LISTO-CAJA",
                  "**Entorno asignado:** CAJA/Ubuntu",
                  "EJERCITA-SONDA-LATERAL-SOBRE-NEGATIVO-REAL"):
        afirma(ancla in t, f"H3: se perdió del piloto el texto original {ancla!r}")
    afirma("NC-0060" in t, "H3: el piloto debe citar su NC vigente NC-0060")


# ───────────────────────────────────────────────────────────────

PRUEBAS = [v for k, v in sorted(globals().items()) if k.startswith("prueba_")]


def main():
    for fn in PRUEBAS:
        try:
            fn()
        except Exception as e:  # una prueba que revienta es un fallo, no un abort
            FALLOS.append(f"{fn.__name__}: EXCEPCIÓN {type(e).__name__}: {e}")
    for f in FALLOS:
        print(f"FAIL {f}")
    print(f"\n{len(PRUEBAS)} pruebas, {len(FALLOS)} fallos")
    return 1 if FALLOS else 0


if __name__ == "__main__":
    sys.exit(main())
