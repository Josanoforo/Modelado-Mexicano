#!/usr/bin/env bash
# tools/deriva_cron.sh — rutina diaria que re-deriva por script tres
# líneas base que hoy se recongelaban a mano (el defecto real que
# ACTO GEN2-RUTINA-DERIVADOS-1 mide: T0 sin refrescar un mes/1178 PRs,
# tablero 50 PRs atrás, suite recongelada cuatro veces a mano).
#
# ACTO GEN2-RUTINA-DERIVADOS-1
# (forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md).
#
# Uso: cd /ruta/al/clon && ./tools/deriva_cron.sh
#
# Una corrida = cuatro derivaciones, todas por script, ninguna por
# juicio: este runner NUNCA invoca un modelo de lenguaje (a diferencia de
# tools/adquiere_cron.sh, que sí invoca un ejecutor sobre un prompt para
# caminar la cola de adquisición). Por eso no reproduce el patrón
# lanzador/runner de tools/adquiere_launcher.sh: esa separación existe
# ahí para fijar una revisión y recuperar presupuesto ANTES de una
# invocación larga y no determinista (tools/adquiere_launcher.sh:130-175,
# clon dedicado `/home/pc0/mm-adq`, forense/cron/REGISTRO-CRON-v1_0.md
# §1/§9/§10); las cuatro derivaciones de aquí son deterministas y cortas,
# así que ese acoplamiento no aplica y este script es su propio lanzador.
#
# Hallazgo A.7 de este acto, declarado explícitamente (verificado contra
# el árbol, no asumido de la redacción del encargo): "colgado del mismo
# scheduler y launcher" no sobrevive el examen del árbol tal cual —
# tools/adquiere_launcher.sh resuelve presupuesto/revisión específicos de
# adquisición y corre contra un clon distinto (`/home/pc0/mm-adq`);
# engancharse ahí acoplaría el disparo diario de esta rutina a semántica
# de adquisición sin necesidad real. Este script toma su PROPIO lock
# (nunca forense/adq-log/, que es de adquisición) y se registra como
# entrada nueva e independiente del mismo Windows Task Scheduler en
# forense/cron/REGISTRO-CRON-v1_0.md §11 — "mismo scheduler", entrada
# propia, sin tocar tools/adquiere_launcher.sh ni tools/adquiere_cron.sh.
#
# Lock/heartbeat/checkout-o-crea-rama siguen el patrón que
# ACTO ADQ-CRON-V2 / GEN2-SONDA-ADQ-CABLEADO endurecieron en
# tools/adquiere_cron.sh (flock no bloqueante, run_id, heartbeat atómico
# por temporal+rename, cambia de rama ANTES de escribir/commitear —
# nunca `checkout -B` sobre una rama del día que ya tiene commits, eso
# fue el non-fast-forward real del 6/sep documentado ahí). Reimplementado
# aquí, no importado: no existe una librería compartida entre cron
# scripts (tools/adq_config.py es de un solo propósito, confirmado contra
# el árbol) y tocar tools/adquiere_cron.sh está fuera del perímetro de
# este acto.
#
# Orden de ejecución DISTINTO del orden de enumeración del encargo: la
# suite (d) corre PRIMERO, no último. Mismo criterio que
# forense/agente-tramite-v1_0.md §0 P2 ("ROJO -> PARA. Termina con cero
# commits... un agente que commitea sobre una línea base rota mete su
# ruido encima del hallazgo de otro"). Enumerar cuatro derivaciones no
# fija su orden de ejecución, y correr la compuerta de salud del árbol
# antes de escribir cualquier sucesión nueva evita apilar un universo
# fechado o un tablero actualizado sobre una línea base ya rota.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

FECHA="$(date +%Y-%m-%d)"
LOGDIR="forense/deriva-log"
mkdir -p "$LOGDIR"
LOGFILE="${LOGDIR}/${FECHA}.log"
ESTADO_DIR="${LOGDIR}/estado"
mkdir -p "$ESTADO_DIR"
HEARTBEAT="${ESTADO_DIR}/heartbeat.json"
LOCKFILE="${ESTADO_DIR}/deriva_cron.lock"
RUN_ID="${FECHA}T$(date +%H%M%S)-$$"
DISPARADOR="${DERIVA_DISPARADOR:-manual}"
case "$DISPARADOR" in
  windows-task-scheduler|manual|prueba-programada|fixture) ;;
  *) DISPARADOR="desconocido" ;;
esac
FASE="INICIO"
# Dueño del lock: 0 hasta que flock lo conceda. Solo el dueño escribe el
# heartbeat -- una segunda invocación rechazada no puede borrar el
# estado de la que sigue trabajando (mismo H6 de GEN2-SONDA-ADQ-CABLEADO).
SOY_DUENO_DEL_LOCK=0
CIERRE_ESCRITO=0
DERIVADOS_DIR="data/curacion-universo/derivados"
RAMA="derivados/${FECHA}"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S%z')] $*" | tee -a "$LOGFILE"
}

# escribe_heartbeat <estado> [codigo] -- JSON pequeño, temporal+rename
# (atómico: nadie lee un heartbeat a medio escribir).
escribe_heartbeat() {
  local estado="$1" codigo="${2:-}"
  if [ "${SOY_DUENO_DEL_LOCK:-0}" != "1" ]; then
    log "heartbeat NO escrito por run_id=${RUN_ID} (estado=${estado}): esta invocación no es dueña del lock."
    return 0
  fi
  python3 - "$HEARTBEAT" "$RUN_ID" "$$" "$estado" "$FASE" "$FECHA" "$codigo" "$DISPARADOR" <<'PYEOF'
import json, os, sys, datetime, tempfile
ruta, run_id, pid, estado, fase, fecha, codigo, disparador = sys.argv[1:9]
doc = {
    "run_id": run_id,
    "pid": int(pid),
    "estado": estado,
    "fase": fase,
    "fecha": fecha,
    "disparador": disparador,
    "codigo_salida": (int(codigo) if codigo not in ("", "-") else None),
    "actualizado": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}
d = os.path.dirname(os.path.abspath(ruta)) or "."
fd, tmp = tempfile.mkstemp(dir=d, prefix=".heartbeat-", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, ruta)
except BaseException:
    try:
        os.unlink(tmp)
    except OSError:
        pass
    raise
PYEOF
}

transicion() {
  FASE="$1"
  escribe_heartbeat "EN-CURSO" "-" 2>>"$LOGFILE" || true
}

# checkout_o_crea_derivados -- mismo patrón que checkout_o_crea_censo()
# de tools/adquiere_cron.sh (líneas 262-279 de ese archivo): reutiliza
# derivados/${FECHA} si ya existe (local o remota) y solo la crea si es
# nueva de verdad, para no reescribir un puntero que ya tiene commits
# propios (eso fue el non-fast-forward real que ese acto midió).
checkout_o_crea_derivados() {
  if git show-ref --verify --quiet "refs/heads/${RAMA}"; then
    git checkout "$RAMA" >>"$LOGFILE" 2>&1
  elif git ls-remote --exit-code --heads origin "$RAMA" >/dev/null 2>&1; then
    git fetch origin "${RAMA}:${RAMA}" >>"$LOGFILE" 2>&1
    git checkout "$RAMA" >>"$LOGFILE" 2>&1
  else
    git checkout -b "$RAMA" >>"$LOGFILE" 2>&1
  fi
}

# huella_deriva <invocado:si|no> <motivo:-|PARO-...> <exit:codigo|->
# Se llama en cada PARO y una vez al terminar. Solo escribe al log local
# (a diferencia de [ADQ], esta rutina no tiene un artefacto de censo
# diario independiente del commit -- cuando hay commit, la huella vive
# en su mensaje; cuando no lo hay (NADA-QUE-HACER o un PARO), vive aquí).
huella_deriva() {
  local invocado="$1" motivo="$2" exit_cod="$3"
  local hhmm t1 duracion linea
  hhmm="$(date +%H:%M)"
  t1="$(date +%s)"
  duracion=$((t1 - T0))
  linea="[DERIVADOS] ${FECHA} ${hhmm}: invocado=${invocado} motivo=${motivo} exit=${exit_cod} duracion=${duracion}s disparador=${DISPARADOR} run_id=${RUN_ID}"
  log "$linea"
  CIERRE_ESCRITO=1
  HUELLA_LINEA="$linea"
}

# (d) tests/check.py --baseline -- corre PRIMERO (ver comentario de
# cabecera). Reporta solo el bloque LÍNEA BASE (FAIL/WARN nuevos contra
# tests/baseline.json): eso ES la firma de hoy, no la lista plana
# completa que --baseline también imprime antes de ese bloque.
deriva_suite() {
  set +e
  SALIDA_SUITE="$(python3 tests/check.py --baseline 2>&1)"
  EXIT_SUITE=$?
  set -e
  echo "$SALIDA_SUITE" >>"$LOGFILE"
  DELTA_SUITE="$(printf '%s\n' "$SALIDA_SUITE" | grep -A 30 "LÍNEA BASE:" || true)"
  if [ -z "$DELTA_SUITE" ]; then
    DELTA_SUITE="(no se encontró el bloque LÍNEA BASE en la salida; exit=${EXIT_SUITE}, ver ${LOGFILE})"
  fi
}

# (a) snapshot del universo declarado, como sucesión fechada.
# tools/curador_registro/snapshot_universe.py no tiene hoy noción de
# fecha ni de sucesión (confirmado contra el árbol: su único modo T0
# escribe siempre a rutas fijas bajo --output-dir, incluido el
# `snapshot-t0.json` cuyo hash `integrate_production.py::
# canonical_analyst_spec()` verifica contra tres expedientes ya sellados
# -- regenerarlo in situ rompería esa verificación). Por eso esta función
# corre el mismo script, sin tocarlo, hacia un directorio efímero
# (mktemp -d, nunca data/curacion-universo/), y solo persiste un resumen
# compacto nuevo bajo data/curacion-universo/derivados/ -- T0 queda
# intacto porque nunca se escribe ahí, y "solo sucesiones nuevas" (el
# perímetro del encargo) se cumple porque lo único que se añade es este
# archivo fechado, nunca los TSV de decenas de MB que el script también
# produce.
deriva_universo() {
  local scratch anterior
  scratch="$(mktemp -d)"
  set +e
  SALIDA_UNIVERSO="$(python3 tools/curador_registro/snapshot_universe.py \
    --spec data/curacion-universo/inputs-t0.json \
    --repo-root . \
    --corpus-root data/raw \
    --output-dir "$scratch" 2>&1)"
  local exit_universo=$?
  set -e
  echo "$SALIDA_UNIVERSO" >>"$LOGFILE"
  if [ "$exit_universo" -ne 0 ]; then
    DELTA_UNIVERSO="PARO-UNIVERSO: snapshot_universe.py salió ${exit_universo}. Ver ${LOGFILE}."
    rm -rf "$scratch"
    return 1
  fi
  mkdir -p "$DERIVADOS_DIR"
  anterior="$(ls -1 "${DERIVADOS_DIR}"/universo-*.json 2>/dev/null | sort | tail -1 || true)"
  if [ -z "$anterior" ]; then
    anterior="data/curacion-universo/snapshot-t0.json"
  fi
  DELTA_UNIVERSO="$(python3 - "$scratch/snapshot-t0.json" "$anterior" "$FECHA" "${DERIVADOS_DIR}/universo-${FECHA}.json" <<'PYEOF'
import json, sys

nuevo_p, anterior_p, fecha, salida_p = sys.argv[1:5]
nuevo = json.load(open(nuevo_p, encoding="utf-8"))
anterior = json.load(open(anterior_p, encoding="utf-8"))
c_nuevo = nuevo["conteos"]
c_anterior = anterior["conteos"]

# Campos de "activos" que en un universo sano solo crecen (nuevas
# declaraciones/adquisiciones se acumulan) -- una BAJADA en cualquiera de
# éstos es "activos que desaparecen" (P3 del encargo). El hash compuesto
# NO se usa como señal de materialidad por sí solo: crece por construcción
# cada vez que se declara un activo nuevo (52->81 inputs ya en la primera
# corrida, T1), así que tratarlo como material lo volvería ruido diario y
# ACTO GEN2-RUTINA-DERIVADOS-1 no crea una alarma que no atrape un defecto
# real (regla de señal del programa). `discrepancias_hash_local` es la
# métrica que sí nombra un hash que cambió sobre un activo ya declarado
# -- ahí SUBIR es la mala noticia, no bajar.
CRECE_SIEMPRE = {
    "componentes_declarados_conservadores",
    "cota_superior_activos_declarados",
    "contenidos_locales_sha256_unicos",
    "identidades_locales_verificadas",
    "representaciones_locales",
    "hashes_representaciones_locales_verificados",
    "numerador_adquirido_identidades_locales_verificadas",
    "declaraciones_parseadas",
    "candidatos_reconciliacion",
    "inputs",
}
ALARMA_SI_SUBE = {"discrepancias_hash_local"}

deltas = {}
material = False
motivo_material = []
for k, v in c_nuevo.items():
    va = c_anterior.get(k)
    if isinstance(v, (int, float)) and isinstance(va, (int, float)) and not isinstance(v, bool) and not isinstance(va, bool):
        d = v - va
        if d != 0:
            deltas[k] = {"anterior": va, "nuevo": v, "delta": d}
            if k in CRECE_SIEMPRE and d < 0:
                material = True
                motivo_material.append(f"{k} bajó ({va}->{v}): activos que desaparecen")
            if k in ALARMA_SI_SUBE and d > 0:
                material = True
                motivo_material.append(f"{k} subió ({va}->{v}): hashes que cambian sobre activos ya declarados")

hash_nuevo = nuevo.get("snapshot_t0_sha256")
hash_anterior = anterior.get("snapshot_t0_sha256")
hash_cambio = hash_nuevo != hash_anterior

if not deltas and not hash_cambio:
    print(f"sin cambios frente a {anterior_p} (hash idéntico {hash_nuevo}).")
else:
    reporte = {
        "fecha": fecha,
        "comparado_contra": anterior_p,
        "conteos": c_nuevo,
        "snapshot_sha256_del_dia": hash_nuevo,
        "hash_anterior": hash_anterior,
        "hash_cambio": hash_cambio,
        "deltas": deltas,
        "material": material,
        "motivo_material": motivo_material,
    }
    with open(salida_p, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")
    resumen_cambios = ", ".join(
        f"{k}: {v['anterior']}->{v['nuevo']}" for k, v in sorted(deltas.items())
    ) or "(solo cambió el hash compuesto)"
    linea = (
        f"escrito {salida_p}; comparado contra {anterior_p}; "
        f"hash {hash_anterior}->{hash_nuevo}; {resumen_cambios}."
    )
    if material:
        linea += (
            " HALLAZGO A.7: " + "; ".join(motivo_material) +
            " -- reportado, no resuelto por esta rutina (P3 del encargo)."
        )
    print(linea)
PYEOF
)"
  rm -rf "$scratch"
}

# (b) tablero_programa.py --actualiza -- reescribe SOLO el bloque
# <!-- TABLERO-DERIVADO:BEGIN/END --> de forense/tablero/TABLERO-PROGRAMA.md
# (nunca TABLERO-PROGRAMA-v1_1.md, que es histórico superado). Ya es
# idempotente por sí mismo (no escribe si el bloque no cambió) -- esta
# función solo mide el hash antes/después para la huella.
deriva_tablero() {
  local antes despues salida exit_tablero
  antes="$(git hash-object forense/tablero/TABLERO-PROGRAMA.md 2>/dev/null || echo -)"
  set +e
  salida="$(python3 tools/tablero_programa.py --actualiza 2>&1)"
  exit_tablero=$?
  set -e
  echo "$salida" >>"$LOGFILE"
  if [ "$exit_tablero" -ne 0 ]; then
    DELTA_TABLERO="PARO-TABLERO: tools/tablero_programa.py --actualiza salió ${exit_tablero}. Ver ${LOGFILE}."
    return 1
  fi
  despues="$(git hash-object forense/tablero/TABLERO-PROGRAMA.md 2>/dev/null || echo -)"
  if [ "$antes" = "$despues" ]; then
    DELTA_TABLERO="sin cambios en el bloque <!-- TABLERO-DERIVADO -->."
  else
    DELTA_TABLERO="bloque derivado actualizado ($(git diff --stat -- forense/tablero/TABLERO-PROGRAMA.md | tail -1 | sed 's/^ *//'))."
  fi
}

# (c) corrida0.py registro --verifica (en seco: sin --escribe, el propio
# script solo deriva e imprime el diff que escribiría, no toca ningún
# TSV -- FP-359) y corrida0.py status (siempre de solo lectura). Ninguna
# de las dos escribe nada: la "delta" es el reporte mismo, no un archivo.
deriva_registro() {
  local salida_verifica salida_status exit_verifica exit_status
  set +e
  salida_verifica="$(python3 tools/corrida0.py registro --verifica 2>&1)"
  exit_verifica=$?
  salida_status="$(python3 tools/corrida0.py status 2>&1)"
  exit_status=$?
  set -e
  echo "$salida_verifica" >>"$LOGFILE"
  echo "$salida_status" >>"$LOGFILE"
  DELTA_REGISTRO="registro --verifica (en seco, exit=${exit_verifica}): $(printf '%s' "$salida_verifica" | tail -6 | tr '\n' ' ' | cut -c1-500) | status (exit=${exit_status}): $(printf '%s' "$salida_status" | tail -10 | tr '\n' ' ' | cut -c1-500)"
}

# Seam de solo-definición (DERIVA_CRON_SOLO_DEFINE=1), mismo mecanismo
# que ADQ_CRON_SOLO_DEFINE en tools/adquiere_cron.sh: define las
# funciones y retorna sin ejecutar ningún paso real, para que una suite
# futura pueda ejercitarlas con dobles sin correr esta rutina en serio.
# No añadido aquí: el test correspondiente (tests/test_adq_cableado.py
# es el precedente a replicar) queda fuera del perímetro declarado de
# este encargo (solo nombra tools/deriva_cron.sh, deriva.md, launcher,
# runbook, data/curacion-universo/, tablero -- no tests/); se deja el
# seam listo y se declara como NO-CORRIDO.
if [ -n "${DERIVA_CRON_SOLO_DEFINE:-}" ]; then
  return 0 2>/dev/null || exit 0
fi

log "=== deriva_cron.sh arrancando en $REPO_DIR (run_id=${RUN_ID} disparador=${DISPARADOR}) ==="

exec 200>"$LOCKFILE"
if ! flock -n 200; then
  FASE="PARO-LOCK"
  log "PARO-LOCK: ya hay una instancia de deriva_cron.sh corriendo (${LOCKFILE} tomado). run_id=${RUN_ID} no toca git ni el heartbeat del dueño; termina de inmediato."
  exit 3
fi
SOY_DUENO_DEL_LOCK=1

finalizar() {
  local codigo=$?
  local estado="TERMINADO"
  [ "$codigo" -ne 0 ] && estado="FAILED"
  if [ "${CIERRE_ESCRITO:-0}" -ne 1 ]; then
    estado="INCOMPLETO"
    log "INCOMPLETO: run_id=${RUN_ID} terminó en fase=${FASE} sin haber escrito su huella [DERIVADOS]. No se infiere éxito ni causa de muerte."
  fi
  log "=== deriva_cron.sh terminado (run_id=${RUN_ID} fase=${FASE} exit=${codigo}) ==="
  escribe_heartbeat "$estado" "$codigo" 2>>"$LOGFILE" || true
  git checkout main >>"$LOGFILE" 2>&1 || true
}
trap finalizar EXIT

escribe_heartbeat "STARTED" "-"

# 1 · entorno -- esta rutina deriva el universo declarado del corpus
# compartido; la propia cabecera del encargo lo dice: "la caja es el
# único entorno que puede derivar el universo". PARO-ENTORNO si corre en
# NUBE, antes de tocar nada.
FASE="ENTORNO"
if [ -n "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-}" ]; then
  FASE="PARO-ENTORNO"
  T0="$(date +%s)"
  log "PARO-ENTORNO: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE='${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE}' (se esperaba sin variable / CAJA). Esta rutina no deriva el universo desde NUBE."
  huella_deriva "no" "PARO-ENTORNO" "-"
  exit 1
fi

# 2 · corpus montado (mismo criterio que tools/adquiere_cron.sh paso 2).
FASE="CORPUS"
T0="$(date +%s)"
if [ -d data/raw ] && [ -n "$(ls -A data/raw 2>/dev/null | head -1)" ]; then
  log "corpus montado: ls data/raw | head -1 -> $(ls data/raw | head -1)"
else
  FASE="PARO-CORPUS"
  log "PARO-CORPUS: data/raw ausente o vacío en esta caja. No se deriva nada."
  huella_deriva "no" "PARO-CORPUS" "-"
  exit 1
fi

# 3 · clon al día
FASE="CLON-AL-DIA"
log "git fetch && git checkout main && git pull"
git fetch origin >>"$LOGFILE" 2>&1
git checkout main >>"$LOGFILE" 2>&1
git pull origin main >>"$LOGFILE" 2>&1
log "HEAD tras pull: $(git log -1 --format='%h %s')"
T0="$(date +%s)"

# 4 · (d) suite en línea base -- PRIMERO. ROJO = PARO, cero commits.
FASE="SUITE"
transicion "SUITE"
deriva_suite
if [ "$EXIT_SUITE" -ne 0 ]; then
  FASE="PARO-SUITE-ROJA"
  log "PARO-SUITE-ROJA: tests/check.py --baseline salió ${EXIT_SUITE} (entradas nuevas). Cero commits -- no se apila universo/tablero sobre una línea base rota."
  log "$DELTA_SUITE"
  huella_deriva "si" "PARO-SUITE-ROJA" "$EXIT_SUITE"
  exit 1
fi
log "suite en línea base VERDE."

# 5 · cambia de rama ANTES de escribir/commitear (mismo orden que
# ACTO ADQ-CRON-V2 fijó para censo/${FECHA} -- nunca al revés).
FASE="RAMA"
transicion "RAMA"
checkout_o_crea_derivados

# 6 · (a) universo, (b) tablero, (c) registro -- ya sobre derivados/${FECHA}.
FASE="UNIVERSO"
transicion "UNIVERSO"
deriva_universo || true
log "(a) universo: ${DELTA_UNIVERSO}"

FASE="TABLERO"
transicion "TABLERO"
deriva_tablero || true
log "(b) tablero: ${DELTA_TABLERO}"

FASE="REGISTRO"
transicion "REGISTRO"
deriva_registro
log "(c) registro: ${DELTA_REGISTRO}"

# 7 · commit solo de lo que de verdad cambió, dentro del perímetro
# (data/curacion-universo/derivados/ y el tablero -- nunca milpa/,
# canon/, ni ninguna decisión).
FASE="COMMIT"
transicion "COMMIT"
git add "$DERIVADOS_DIR" forense/tablero/TABLERO-PROGRAMA.md >>"$LOGFILE" 2>&1 || true

if git diff --cached --quiet; then
  log "NADA-QUE-HACER: ninguna de las cuatro derivaciones produjo un cambio versionable hoy."
  git checkout main >>"$LOGFILE" 2>&1
  git branch -D "$RAMA" >>"$LOGFILE" 2>&1 || true
  huella_deriva "si" "NADA-QUE-HACER" "0"
  exit 0
fi

CUERPO="[DERIVADOS] ${FECHA}: disparador=${DISPARADOR} run_id=${RUN_ID}

(a) universo: ${DELTA_UNIVERSO}
(b) tablero: ${DELTA_TABLERO}
(c) registro: ${DELTA_REGISTRO}
(d) suite: ${DELTA_SUITE}"

git commit -m "[DERIVADOS] ${FECHA}

${CUERPO}" >>"$LOGFILE" 2>&1

PUBLICADO=0
if git push -u origin "$RAMA" >>"$LOGFILE" 2>&1; then
  PUBLICADO=1
else
  log "PUBLICACION-FALLIDA (intento 1): ${RAMA} no se pudo empujar; se intenta reconciliar sin reescribir historia."
  if git pull --no-rebase --no-edit origin "$RAMA" >>"$LOGFILE" 2>&1 && git push origin "$RAMA" >>"$LOGFILE" 2>&1; then
    PUBLICADO=1
    log "publicado tras reconciliar (sin force-push)."
  else
    log "DIVERGENCIA-DECLARADA: no se pudo reconciliar ${RAMA} con el remoto. NO se hace force-push. El commit queda LOCAL."
  fi
fi

git checkout main >>"$LOGFILE" 2>&1 || true

if [ "$PUBLICADO" -ne 1 ]; then
  FASE="PARO-DERIVADOS-PUSH"
  log "PARO-DERIVADOS-PUSH: el commit de ${RAMA} quedó LOCAL. No se abre PR."
  huella_deriva "si" "PARO-PUSH" "2"
  exit 2
fi

FASE="PR"
transicion "PR"
if command -v gh >/dev/null 2>&1; then
  PR_ABIERTO="$(gh pr list --head "$RAMA" --state open --json number --jq '.[0].number' 2>/dev/null || true)"
  if [ -n "$PR_ABIERTO" ]; then
    log "PR diario ya abierto para ${RAMA}: #${PR_ABIERTO} -- se reutiliza (un PR diario es lo máximo que produce esta rutina)."
  elif gh pr create --title "[DERIVADOS] ${FECHA}" --body "${CUERPO}" --base main --head "$RAMA" >>"$LOGFILE" 2>&1; then
    log "PR abierto para ${RAMA}."
  else
    log "gh pr create falló, ver ${LOGFILE}. Compara manualmente: https://github.com/Josanoforo/Modelado-Mexicano/compare/main...${RAMA}"
  fi
else
  log "gh no disponible. Compara manualmente: https://github.com/Josanoforo/Modelado-Mexicano/compare/main...${RAMA}"
fi

FASE="FIN"
huella_deriva "si" "-" "0"
log "RESULTADO: [DERIVADOS] ${FECHA} commiteado y publicado en ${RAMA}."
