#!/usr/bin/env bash
# tools/adquiere_cron.sh — runner de mesa para el agente de adquisición.
#
# ACTO MAESTRA34-N7 · SKILLS-COLA-Y-ADQ
# (forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md).
# Este script SE ESCRIBE aquí; su instalación en el disparador (línea
# sugerida en forense/agente-adquisicion-v1_0.md, hoy Windows Task
# Scheduler -- ver forense/cron/REGISTRO-CRON-v1_0.md §2) es tarea de
# mesa, no de este acto.
#
# Uso: cd /ruta/al/clon && ./tools/adquiere_cron.sh
#
# ACTO ADQ-CRON-V2 · DISPARO-PERSISTENTE-Y-RUNNER-IDEMPOTENTE (P3/P6,
# 7/sep/2026). Endurece el runner tras el incidente del 7/sep (el WSL de
# mesa estuvo suspendido en la ventana 07:30 -- ver
# forense/notas/2026-09-07-ADQ-CRON-V2-diagnostico.md) y el defecto real
# medido el 6/sep (non-fast-forward al reintentar censo/<fecha> el mismo
# día -- hechos 8/9 del encargo, forense/encargos/2026-09-07-ADQ-CRON-V2.md):
#   - lock exclusivo de una sola instancia (`flock`, no bloqueante).
#   - run_id único por invocación, heartbeat local en
#     forense/adq-log/estado/heartbeat.json (gitignorado, igual que el
#     resto de forense/adq-log/), escrito al arrancar y `trap EXIT`
#     siempre lo actualiza con fase/exit/fin, incluso si `git fetch` falla.
#   - timeout configurable de `claude -p` (`CLAUDE_TIMEOUT_SEGUNDOS` o
#     `data/adq-config.yaml:claude_timeout_segundos`, vía `timeout(1)`).
#   - `checkout_o_crea_censo()` reemplaza los dos sitios que hacían
#     `checkout -B censo/<fecha>` a ciegas: ahora reutiliza la rama si ya
#     existe (local o remota) y solo la crea si es nueva de verdad -- eso
#     era lo que producía el non-fast-forward. El commit `[CENSO]` (paso
#     2.5) ahora cambia de rama ANTES de escribir/añadir/commitear, nunca
#     después -- antes de este acto se commiteaba sobre `main` (checked
#     out desde el paso 1) y solo luego se creaba/reseteaba censo/<fecha>,
#     dejando `main` local un commit adelante de `origin/main` cada
#     corrida.
#   - PDN (paso 2.6): URLs, claves físicas/lógicas e ids de manifiesto ya
#     no están cableados aquí -- vienen de `data/adq-config.yaml` vía
#     `tools/adq_config.py` (P6). Antes de `--compara-sha`: la descarga no
#     puede quedar en 0 bytes y el ZIP debe ser legible
#     (`zipfile.testzip()`) -- `--compara-sha` detecta identidad de bytes,
#     no legibilidad del contenedor, y no adjudica un cambio de bytes por
#     sí solo (Enmienda 4, sigue vigente).

# ACTO GEN2-SONDA-ADQ-CABLEADO · EL VIGILANTE DEJA DE MENTIR EN AMBOS
# SENTIDOS (P1, 9/sep/2026,
# forense/encargos/2026-09-09-GEN2-SONDA-ADQ-CABLEADO.md; casos congelados
# en tests/test_adq_cableado.py; revisión de origen en
# forense/notas/2026-09-09-REVISION-CABLEADO-SONDA-ADQUISICION-astra.md).
# Cuatro defectos reproducidos, todos de la misma familia: el runner
# reportaba éxito por caminos que no lo acreditaban.
#   - H4 · `curl -w '%{http_code}' ... || echo 'sin-respuesta'` concatena:
#     un transporte fallido daba la cadena `000sin-respuesta`, que NO es
#     igual a `sin-respuesta`, así que la compuerta PARO-RED no entraba y
#     el runner gastaba la invocación de Claude. Ahora el código de salida
#     de curl, el HTTP y la causa se capturan POR SEPARADO (sonda_red).
#   - H5 · `commit_censo_linea()` registraba `PARO-CENSO-PUSH` y seguía;
#     con un doble que hacía fallar solo `git push`, la función terminaba
#     en 0. Ahora devuelve fallo operativo, conserva el recibo local y el
#     runner cierra con un resultado COMPUESTO (trabajo + publicación),
#     no solo con el exit de Claude.
#   - H6 · `timeout` sin `--kill-after`: un proceso que ignora TERM
#     sobrevivía al límite. Y la instancia rechazada por `flock` escribía
#     en el heartbeat del DUEÑO, borrando su estado. Ahora hay gracia
#     finita con escalamiento, y solo el dueño del lock toca el heartbeat
#     (por temporal + rename); el rechazo se apendiza al log con su
#     propio run_id.
#   - Prompt · el `awk` recogía TODOS los bloques ```text del runbook y
#     los concatenaba en silencio. Ahora se exige bloque único.
# NO se construye aquí: servidor, scheduler duplicado ni reintentos
# ilimitados. El horario del cron NO cambia (cualquier cambio futuro se
# propaga a TODOS los consumidores -- runner, T31, instalador --, no solo
# al instalador; queda escrito, no ejecutado).

set -euo pipefail

RUNNER_VERSION="adq-codex-1"

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

# La fecha y todas las llamadas posteriores a `date` usan la zona del
# calendario versionado, aunque la zona local del proceso/host sea otra.
ADQ_ZONA_INICIAL="$(python3 tools/adq_config.py --calendario-json |
  python3 -c 'import json,sys; print(json.load(sys.stdin)["zona_iana"])')"
export TZ="$ADQ_ZONA_INICIAL"
FECHA="$(date +%Y-%m-%d)"
LOGDIR="forense/adq-log"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/${FECHA}.log"
CENSO_DIR="forense/censo-raiz"
ESTADO_DIR="${LOGDIR}/estado"
mkdir -p "$ESTADO_DIR"
HEARTBEAT="${ESTADO_DIR}/heartbeat.json"
LOCKFILE="${ESTADO_DIR}/adquiere_cron.lock"
RUN_ID="${FECHA}T$(date +%H%M%S)-$$"
INICIO_ISO="$(date --iso-8601=seconds)"
DISPARADOR="${ADQ_DISPARADOR:-manual}"
case "$DISPARADOR" in
  windows-task-scheduler|puesta-en-marcha-programada|manual|prueba-programada|fixture) ;;
  *) DISPARADOR="desconocido" ;;
esac
CAUSA_DISPARO="${ADQ_CAUSA_DISPARO:-$DISPARADOR}"
FASE="INICIO"
EJECUTOR="desconocido"
CLI_VERSION="desconocida"
MODELO_CONFIGURADO="no-configurado"
MODELO_EFECTIVO="no-observable"
RESULTADO_SUSTANTIVO="no-invocado"
SELECCION_ELEGIDOS="-"
SELECCION_EXCLUIDOS="-"
SELECCION_JSON="null"
RESULTADO_PUBLICO="null"
PUBLICACION_ESTADO="pendiente"
# Dueño del lock: 0 hasta que `flock` lo conceda. Solo el dueño escribe el
# heartbeat activo (H6) -- una segunda invocación rechazada no puede
# borrar el estado de la que sigue trabajando.
SOY_DUENO_DEL_LOCK=0
# Resultado COMPUESTO (H5): el runner no cierra con el exit de Claude a
# secas. `PUBLICACION_FALLIDA` cuenta los recibos que quedaron locales.
PUBLICACION_FALLIDA=0
CIERRE_ESCRITO=0

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S%z')] $*" | tee -a "$LOGFILE"
}

# Regresa al árbol que el launcher resolvió. En el camino heredado conserva
# `main`; en despliegue fijado nunca permite que un checkout auxiliar a
# censo/<fecha> rebaje el árbol a una versión anterior del ejecutor.
restaura_arbol_operativo() {
  if [ -n "${ADQ_DEPLOY_SHA:-}" ]; then
    git checkout --detach "$ADQ_DEPLOY_SHA" >>"$LOGFILE" 2>&1
  else
    git checkout main >>"$LOGFILE" 2>&1
  fi
}

# ── H4 · sonda de red con transporte y HTTP SEPARADOS ────────────
# Devuelve 0 si el destino RESPONDIÓ (cualquier código HTTP, 403
# incluido) y 1 si el transporte falló. Exporta CODIGO_HTTP,
# CURL_SALIDA y CAUSA_RED para que el llamador registre la causa exacta.
# Un 403 es una respuesta y un bloqueo de ESE destino: jamás «sin
# internet» ni «no existe», y no contagia paro a fuentes independientes.
sonda_red() {
  local url="$1" salida_curl codigo
  set +e
  codigo="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" 2>/dev/null)"
  salida_curl=$?
  set -e
  CURL_SALIDA="$salida_curl"
  CODIGO_HTTP="$codigo"
  if [ "$salida_curl" -ne 0 ]; then
    CAUSA_RED="TRANSPORTE-FALLIDO: curl salió ${salida_curl} sobre ${url} (http='${codigo}')"
    log "sonda ${url}: PARO-RED -- ${CAUSA_RED}"
    return 1
  fi
  case "$codigo" in
    000|"")
      CAUSA_RED="TRANSPORTE-FALLIDO: curl salió 0 pero sin código HTTP sobre ${url}"
      log "sonda ${url}: PARO-RED -- ${CAUSA_RED}"
      return 1
      ;;
    403)
      CAUSA_RED="BLOQUEO-DEL-DESTINO: HTTP 403 en ${url} -- es una respuesta, no ausencia de red ni de objeto; no se extiende a fuentes independientes"
      log "sonda ${url}: http=403 -- ${CAUSA_RED}"
      return 0
      ;;
    *)
      CAUSA_RED="RESPUESTA: HTTP ${codigo} en ${url}"
      log "sonda ${url}: curl salió 0, http=${codigo}"
      return 0
      ;;
  esac
}

# ── P1 · extracción del prompt con bloque ```text ÚNICO ──────────
# El awk anterior recogía TODOS los bloques ```text del archivo y los
# concatenaba sin avisar; un runbook con dos bloques producía un prompt
# que nadie escribió. Ahora se cuentan primero: != 1 es PARO-PROMPT.
extrae_prompt() {
  local archivo="$1" cuantos
  cuantos="$(grep -c '^```text$' "$archivo" || true)"
  if [ "${cuantos:-0}" -ne 1 ]; then
    log "PARO-PROMPT: ${archivo} tiene ${cuantos:-0} bloques \`\`\`text; se exige exactamente 1. No se concatena a ciegas ni se invoca claude -p con el archivo entero."
    return 1
  fi
  awk '/^```text$/{flag=1; next} /^```$/{if(flag){flag=0}} flag' "$archivo"
}

# ── H4/config · la configuración se valida DESPUÉS de sincronizar ─
# Antes, las tres claves se leían al arrancar el script (antes del `git
# pull` del paso 1) y cada una caía a un default con `|| echo` en
# silencio: una config rota se sustituía sin que nadie lo supiera, y
# encima se leía la versión vieja del clon. Ahora se leen tras el pull y
# la degradación se DECLARA en el log y en la huella.
CONFIG_DEGRADADA=""
lee_config() {
  local clave="$1" respaldo="$2" valor
  if valor="$(python3 tools/adq_config.py "$clave" 2>&1)"; then
    printf '%s' "$valor"
    return 0
  fi
  CONFIG_DEGRADADA="${CONFIG_DEGRADADA}${clave} "
  log "CONFIG-DEGRADADA: no se pudo leer '${clave}' de data/adq-config.yaml (${valor}); se usa el respaldo '${respaldo}' -- declarado, no silencioso."
  printf '%s' "$respaldo"
}

# Resuelve override > YAML > respaldo sin que un log emitido desde una
# sustitución de comando contamine el valor numérico aplicado.
lee_entero_resuelto() {
  local clave="$1" env_var="$2" respaldo="$3" json
  json="$(python3 tools/adq_config.py --entero-json "$clave" "$env_var" "$respaldo")"
  VALOR_CONFIG_RESUELTO="$(printf '%s' "$json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["valor"])')"
  FUENTE_CONFIG_RESUELTA="$(printf '%s' "$json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["fuente"])')"
  DEGRADADA_CONFIG_RESUELTA="$(printf '%s' "$json" | python3 -c 'import json,sys; print("si" if json.load(sys.stdin)["degradada"] else "no")')"
  CAUSA_CONFIG_RESUELTA="$(printf '%s' "$json" | python3 -c 'import json,sys; print(json.load(sys.stdin)["causa"] or "-")')"
  if [ "$DEGRADADA_CONFIG_RESUELTA" = "si" ]; then
    CONFIG_DEGRADADA="${CONFIG_DEGRADADA}${clave} "
    log "CONFIG-DEGRADADA: ${clave}; causa=${CAUSA_CONFIG_RESUELTA}; valor_aplicado=${VALOR_CONFIG_RESUELTO}; fuente=${FUENTE_CONFIG_RESUELTA}."
  else
    log "CONFIG: ${clave}=${VALOR_CONFIG_RESUELTO}; fuente=${FUENTE_CONFIG_RESUELTA}."
  fi
}

# escribe_heartbeat <estado> [codigo]
# JSON pequeño en $HEARTBEAT -- tools/adq_doctor.py (P4) lo lee tal cual.
#
# H6 (GEN2-SONDA-ADQ-CABLEADO, 9/sep/2026). Dos correcciones:
#
#   1. SOLO EL DUEÑO DEL LOCK ESCRIBE. Reproducido con el bloque real de
#      arranque: `RUN-A / STARTED` era reemplazado por `RUN-B / PARO-LOCK`
#      cuando una segunda invocación era rechazada por `flock`, aunque A
#      seguía siendo dueño y seguía trabajando. Una segunda invocación
#      podía así ocultar el estado del trabajo en curso. Ahora la
#      instancia rechazada NO toca el heartbeat: se apendiza al LOG con su
#      propio run_id, que es donde su rechazo es información y no ruido.
#   2. TEMPORAL + RENAME. `os.replace` sobre el mismo directorio es
#      atómico: el doctor nunca lee un heartbeat truncado a medio
#      escribir. Y se actualiza en las TRANSICIONES de fase, no solo al
#      arrancar y al morir.
escribe_heartbeat() {
  local estado="$1" codigo="${2:-}"
  if [ "${SOY_DUENO_DEL_LOCK:-0}" != "1" ]; then
    log "heartbeat NO escrito por run_id=${RUN_ID} (estado=${estado}): esta invocación no es dueña del lock y no puede pisar el estado de la que trabaja."
    return 0
  fi
  python3 - "$HEARTBEAT" "$RUN_ID" "$$" "$estado" "$FASE" "$FECHA" "$codigo" "$DISPARADOR" "${HEAD_USADO:-desconocido}" "$CAUSA_DISPARO" "$EJECUTOR" "$CLI_VERSION" "$MODELO_CONFIGURADO" "$MODELO_EFECTIVO" "$RUNNER_VERSION" "$INICIO_ISO" "$RESULTADO_SUSTANTIVO" "$PUBLICACION_ESTADO" "${ADQ_DEPLOY_MODE:-legacy}" "$SELECCION_ELEGIDOS" "$SELECCION_EXCLUIDOS" <<'PYEOF'
import json, os, sys, datetime, tempfile
(ruta, run_id, pid, estado, fase, fecha, codigo, disparador, sha, causa,
 ejecutor, cli_version, modelo_configurado, modelo_efectivo, runner_version,
 inicio, resultado, publicacion, despliegue, elegidos, excluidos) = sys.argv[1:22]
doc = {
    "run_id": run_id,
    "pid": int(pid),
    "estado": estado,
    "fase": fase,
    "fecha": fecha,
    "disparador": disparador,
    "causa_disparo": causa,
    "ejecutor": ejecutor,
    "cli_version": cli_version,
    "modelo_configurado": modelo_configurado,
    "modelo_efectivo": modelo_efectivo,
    "runner_version": runner_version,
    "despliegue": despliegue,
    "sha": sha,
    "inicio": inicio,
    "resultado_sustantivo": resultado,
    "seleccion_elegidos": elegidos,
    "seleccion_excluidos": excluidos,
    "publicacion": publicacion,
    "codigo_salida": (int(codigo) if codigo not in ("", "-") else None),
    "actualizado": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}
if estado in ("TERMINADO", "FAILED", "INCOMPLETO"):
    doc["fin"] = doc["actualizado"]
d = os.path.dirname(os.path.abspath(ruta)) or "."
fd, tmp = tempfile.mkstemp(dir=d, prefix=".heartbeat-", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, ruta)   # atómico: nadie lee un heartbeat a medio escribir
except BaseException:
    try:
        os.unlink(tmp)
    except OSError:
        pass
    raise
PYEOF
}

# transicion <fase> -- H6: el heartbeat se actualiza en las transiciones
# relevantes, no solo al arrancar y al morir; si el proceso muere en
# medio, el último estado publicado dice DÓNDE murió.
transicion() {
  FASE="$1"
  escribe_heartbeat "EN-CURSO" "-" 2>>"$LOGFILE" || true
}

# checkout_o_crea_censo -- cambia a censo/${FECHA}, creándola SOLO si no
# existe todavía (local o remota). Nunca `checkout -B`: reiniciar el
# puntero de una rama del día que YA tiene commits (locales o empujados)
# es exactamente lo que produjo el non-fast-forward real del 6/sep --
# `censo/2026-09-06` divergió 9 commits locales contra 1 remoto porque
# cada llamada reescribía la rama desde el HEAD de `main` en vez de
# continuarla.
checkout_o_crea_censo() {
  local rama_censo="censo/${FECHA}"
  if git show-ref --verify --quiet "refs/heads/${rama_censo}"; then
    git checkout "$rama_censo" >>"$LOGFILE" 2>&1
  elif git ls-remote --exit-code --heads origin "$rama_censo" >/dev/null 2>&1; then
    git fetch origin "${rama_censo}:${rama_censo}" >>"$LOGFILE" 2>&1
    git checkout "$rama_censo" >>"$LOGFILE" 2>&1
  else
    git checkout -b "$rama_censo" >>"$LOGFILE" 2>&1
  fi
}

# commit_censo_linea <contenido> <resumen> <mensaje>
# Ritual único de checkout/append/commit/push/checkout-main contra
# censo/${FECHA} (crea la rama solo si no existe todavía, local o
# remota -- ver checkout_o_crea_censo). Usado por huella_adq() y por el
# paso 2.6 ([ADQ-PDN]) -- antes de MAESTRA38-CRON-3 el append de 2.6
# quedaba huérfano en el árbol de trabajo tras el checkout-main de 2.5 y
# nunca se commiteaba (defecto de #558, corregido ahí). <contenido> es lo
# que se anexa al archivo del censo (puede ser multilínea); <resumen> es
# la línea corta que va en el cuerpo del commit; <mensaje> es el asunto
# ("[ADQ] <fecha>" / "[ADQ-PDN] <fecha>").
# H5 (GEN2-SONDA-ADQ-CABLEADO, 9/sep/2026): esta función registraba
# `PARO-CENSO-PUSH` y CONTINUABA con `git checkout main`, terminando en 0.
# Con el cuerpo real y un doble que hacía fallar únicamente `git push`, el
# resultado era éxito: `exit=0` del proceso no garantizaba que el recibo
# hubiera llegado al repo. Ahora:
#   - el recibo LOCAL se conserva siempre (el append y el commit ocurren
#     antes del push y no se deshacen);
#   - la fase y el error de publicación quedan en el log;
#   - la función devuelve FALLO OPERATIVO (2) y sube PUBLICACION_FALLIDA,
#     que el cierre del runner lee para componer su resultado;
#   - el reintento reconcilia con `--no-rebase` sin reescribir historia y
#     DECLARA la divergencia si la hay. Sin force-push, nunca.
commit_censo_linea() {
  local contenido="$1" resumen="$2" mensaje="$3"
  local rama_censo="censo/${FECHA}"
  local archivo="${CENSO_DIR}/${FECHA}.txt"
  local publicado=0
  mkdir -p "$CENSO_DIR"

  checkout_o_crea_censo

  {
    echo
    echo "$contenido"
  } >>"$archivo"
  git add "$archivo" >>"$LOGFILE" 2>&1
  git commit -m "${mensaje}

${resumen}" >>"$LOGFILE" 2>&1

  if git push -u origin "$rama_censo" >>"$LOGFILE" 2>&1; then
    publicado=1
  else
    # Un push rechazado puede ser divergencia (otra corrida del mismo día
    # ya empujó) o red caída. Se intenta reconciliar UNA vez, sin
    # reescribir historia; si sigue fallando, se declara y se conserva el
    # recibo local -- no se fuerza.
    log "PUBLICACION-FALLIDA (intento 1): ${mensaje} no se pudo empujar a ${rama_censo}; se intenta reconciliar sin reescribir historia."
    if git pull --no-rebase --no-edit origin "$rama_censo" >>"$LOGFILE" 2>&1; then
      log "reconciliado con origin/${rama_censo} por merge (sin force-push); reintentando push."
      if git push origin "$rama_censo" >>"$LOGFILE" 2>&1; then
        publicado=1
        log "publicado tras reconciliar: ${mensaje} en ${rama_censo}."
      fi
    else
      log "DIVERGENCIA-DECLARADA: no se pudo reconciliar ${rama_censo} con el remoto. NO se hace force-push."
    fi
  fi

  restaura_arbol_operativo || true

  if [ "$publicado" -ne 1 ]; then
    PUBLICACION_FALLIDA=$((PUBLICACION_FALLIDA + 1))
    log "PARO-CENSO-PUSH: el commit de ${rama_censo} (${mensaje}) quedó LOCAL. El recibo existe en ${archivo}; la publicación NO ocurrió. Esto es fallo operativo, no éxito."
    return 2
  fi

  # Reutiliza el PR diario abierto de esta rama si ya existe -- eso no es
  # un fallo de creación, y distinguirlo evita leer "gh pr create falló"
  # como si el recibo no hubiera llegado (H5).
  if command -v gh >/dev/null 2>&1; then
    local pr_abierto
    pr_abierto="$(gh pr list --head "$rama_censo" --state open --json number \
                  --jq '.[0].number' 2>/dev/null || true)"
    if [ -n "$pr_abierto" ]; then
      log "PR diario ya abierto para ${rama_censo}: #${pr_abierto} -- se REUTILIZA (no es fallo de gh pr create)."
    fi
  fi
  return 0
}

# publica_censo_manual -- paso 2.5: censo diario de la raíz manual +
# commit + push a censo/${FECHA}, dado que $CENSO_DIR ya existe y la raíz
# ya resolvió (comprobado por el llamador, cuerpo principal). Extraída a
# función (GEN2-ADQ-CONTRATO-FIX, P4) para que sea ejercitable con el seam
# de solo-definición igual que commit_censo_linea, y para que su fallo de
# publicación alimente PUBLICACION_FALLIDA igual que ésa -- antes de este
# acto un push fallido aquí se logueaba como PARO-CENSO-PUSH SIN tocar el
# contador, así que una publicación de censo que nunca llegó al remoto
# podía cerrar la corrida con publicacion=OK (H5 de la revisión del 9/sep).
publica_censo_manual() {
  mkdir -p "$CENSO_DIR"
  local RAMA_CENSO="censo/${FECHA}"
  # ACTO ADQ-CRON-V2 (P3): cambia de rama ANTES de decidir el nombre del
  # archivo o escribir nada. Antes de este acto el add/commit ocurría
  # mientras el árbol seguía en `main` (checked out desde el paso 1) y
  # censo/${FECHA} se creaba/reseteaba DESPUÉS con `checkout -B` -- eso
  # dejaba `main` local contaminado con el commit [CENSO] cada corrida
  # (hecho 8) y, en un reintento el mismo día, reescribía censo/${FECHA}
  # desde ese `main` ya adelantado en vez de continuar lo que el remoto
  # ya tenía (hecho 9, el non-fast-forward real del 6/sep).
  checkout_o_crea_censo
  local CENSO_FILE="${CENSO_DIR}/${FECHA}.txt"
  if [ -e "$CENSO_FILE" ]; then
    CENSO_FILE="${CENSO_DIR}/${FECHA}-cron-$(date +%H%M).txt"
  fi
  local SALIDA_CENSO RESUMEN
  SALIDA_CENSO="$(python3 tests/manifiesto.py --escanea descargas_mx 2>&1 || true)"
  RESUMEN="$(echo "$SALIDA_CENSO" | grep -m1 '^Total en disco:' || echo 'Total en disco: (sin resumen -- ver salida cruda abajo)')"

  {
    echo "$RESUMEN"
    echo
    echo "$SALIDA_CENSO"
  } >"$CENSO_FILE"
  log "[CENSO] ${FECHA}: ${RESUMEN}"

  # main está protegida (status check "check" requerido) -- no se puede
  # empujar directo. En vez de eso: rama censo/${FECHA} (ya activa arriba)
  # + PR (--fill si gh está disponible, si no se deja logueada la URL de
  # compare) para que el check corra y mesa firme. data/manifiesto-
  # staging.yaml (escrito por --escanea arriba) NO se commitea aquí --
  # este paso solo hace `git add` de $CENSO_FILE; sus cambios quedan sin
  # comitear por este cron hasta que un acto los recoja explícitamente.
  git add "$CENSO_FILE" >>"$LOGFILE" 2>&1
  if ! git diff --cached --quiet -- "$CENSO_FILE"; then
    git commit -m "[CENSO] ${FECHA}

${RESUMEN}" >>"$LOGFILE" 2>&1
    if git push -u origin "$RAMA_CENSO" >>"$LOGFILE" 2>&1; then
      log "[CENSO] ${FECHA} commiteado y empujado a ${RAMA_CENSO}"
      # H5 (GEN2-ADQ-CONTRATO-FIX): "push-sin-PR" -- rama empujada, PR NO
      # creado (gh ausente o `gh pr create` falló) -- NO es publicación
      # fallida. El recibo SÍ llegó al remoto; abrir el PR es trámite de
      # mesa, no parte de esta señal, así que esto nunca toca
      # PUBLICACION_FALLIDA.
      if command -v gh >/dev/null 2>&1; then
        if gh pr create --fill >>"$LOGFILE" 2>&1; then
          log "[CENSO] ${FECHA}: PR abierto para ${RAMA_CENSO}"
        else
          log "[CENSO] ${FECHA}: gh pr create falló, ver arriba. Compara manualmente: https://github.com/Josanoforo/Modelado-Mexicano/compare/main...${RAMA_CENSO}"
        fi
      else
        log "[CENSO] ${FECHA}: gh no disponible. Compara manualmente: https://github.com/Josanoforo/Modelado-Mexicano/compare/main...${RAMA_CENSO}"
      fi
    else
      PUBLICACION_FALLIDA=$((PUBLICACION_FALLIDA + 1))
      log "PARO-CENSO-PUSH: el commit [CENSO] ${FECHA} quedó local, no se pudo empujar ${RAMA_CENSO}. Fallo operativo, no éxito -- alimenta PUBLICACION_FALLIDA."
    fi
  else
    log "[CENSO] ${FECHA}: sin cambios respecto al censo previo, no se commitea de nuevo."
  fi
  restaura_arbol_operativo || true
}

# huella_adq <invocado:si|no> <motivo:-|PARO-RAIZ|PARO-RED|PARO-PROMPT|PARO-CORPUS> <exit:codigo|->
# Formato congelado en forense/notas/2026-09-06-MAESTRA38-CRON-3-spec.md.
# Se llama en CADA PARO (exit 1) y una vez al terminar con éxito o con
# fallo de claude -p -- nunca calla, y si invocado=no los tres últimos
# campos se miden igual (deben dar 0 porque no hubo tiempo de producir
# nada, no se asumen en 0).
#
# GEN2-SONDA-ADQ-CABLEADO añade dos campos y una advertencia:
#   - `sha=` -- el SHA REALMENTE USADO por esta corrida (HEAD tras el pull
#     del paso 1), para poder correlacionar la huella con el árbol contra
#     el que se trabajó. Antes la huella no lo decía y no había forma de
#     saberlo desde el recibo.
#   - `publicacion=` -- OK / FALLIDA(n): separa "el agente terminó" de
#     "la huella se publicó" (H5).
# ADVERTENCIA VIGENTE, verbatim de la revisión del 9/sep: los contadores
# NO son payloads adquiridos ni fuentes obtenidas. `ramas_nuevas` incluye
# la propia rama del censo y se calcula sobre TODAS las refs remotas, así
# que cuenta trabajo ajeno; `commits_nuevos`/`archivos_modificados` miden
# movimiento del árbol. `invocado=si` con `exit=0` acredita que el agente
# corrió y cerró limpio -- no cuántas fuentes bajó. Quien quiera esa cifra
# la lee de data/manifiesto.yaml y de la cola, no de aquí.
huella_adq() {
  local invocado="$1" motivo="$2" exit_cod="$3"
  local hhmm t1 duracion head_despues commits_nuevos ramas_despues ramas_nuevas archivos_modificados linea publicacion contenido fin_iso cli_token
  hhmm="$(date +%H:%M)"
  t1="$(date +%s)"
  duracion=$((t1 - T0))
  head_despues="$(git rev-parse HEAD 2>/dev/null || echo "$HEAD_ANTES")"
  commits_nuevos="$(git rev-list --count "${HEAD_ANTES}..${head_despues}" 2>/dev/null || echo 0)"
  # GEN2-ADQ-CONTRATO-FIX: bajo `pipefail` (activo desde la línea 73),
  # `git ls-remote ... | wc -l || echo "$RAMAS_ANTES"` es la trampa que su
  # propio nombre sugiere que evita: si `git ls-remote` falla, `wc -l`
  # sobre su entrada vacía SIGUE imprimiendo "0" y sale 0 -- pero
  # `pipefail` hace que la CANALIZACIÓN completa reporte el fallo de
  # `git ls-remote`, así que el `|| echo` TAMBIÉN se dispara, y el
  # resultado capturado son DOS líneas ("0" de `wc -l` más el respaldo),
  # no una -- lo que revienta la aritmética de abajo. Se separa la
  # captura del respaldo con `set +e/-e` para leer el código de salida
  # real de la canalización, no el de `wc -l` a secas.
  set +e
  ramas_despues="$(git ls-remote --heads origin 2>/dev/null | wc -l)"
  codigo_ramas=$?
  set -e
  if [ "$codigo_ramas" -ne 0 ]; then
    ramas_despues="$RAMAS_ANTES"
  fi
  ramas_nuevas=$((ramas_despues - RAMAS_ANTES))
  archivos_modificados="$(git status --short 2>/dev/null | wc -l)"

  # GEN2-ADQ-CONTRATO-FIX (H5): la publicación de ESTA MISMA huella no se
  # conoce hasta que commit_censo_linea intenta su propio push -- así que
  # `publicacion=` no puede escribirse con la verdad todavía cuando la
  # línea se arma. Antes de este acto se escribía aquí, ANTES de llamar a
  # commit_censo_linea, leyendo PUBLICACION_FALLIDA como estaba en ese
  # instante: solo podía cargar fallos ANTERIORES de la misma corrida
  # (2.5, PDN), nunca el fallo del propio push de esta huella -- que es
  # justo el caso que el vigilante necesita distinguir. Se escribe
  # primero en tentativa (arrastrando solo lo YA conocido) y, si ESTE
  # push falla, se corrige el commit local recién hecho -- nunca
  # empujado todavía, así que corregirlo no reescribe nada compartido --
  # antes de declarar cerrada la corrida.
  local fallidas_antes="${PUBLICACION_FALLIDA:-0}"
  if [ "$fallidas_antes" -eq 0 ]; then
    publicacion="OK"
  else
    publicacion="FALLIDA(${fallidas_antes})"
  fi

  fin_iso="$(date --iso-8601=seconds)"
  cli_token="${CLI_VERSION// /_}"
  linea="[ADQ] ${FECHA} ${hhmm}: invocado=${invocado} motivo=${motivo} exit=${exit_cod} duracion=${duracion}s commits_nuevos=${commits_nuevos} ramas_nuevas=${ramas_nuevas} archivos_modificados=${archivos_modificados} sha=${HEAD_USADO:-${HEAD_ANTES:-desconocido}} launcher_sha=${ADQ_DEPLOY_SHA:-legacy} runner_version=${RUNNER_VERSION} ejecutor=${EJECUTOR} cli_version=${cli_token} modelo_configurado=${MODELO_CONFIGURADO} modelo_efectivo=${MODELO_EFECTIVO} resultado=${RESULTADO_SUSTANTIVO} seleccion_elegidos=${SELECCION_ELEGIDOS} seleccion_excluidos=${SELECCION_EXCLUIDOS} inicio=${INICIO_ISO} fin=${fin_iso} publicacion=${publicacion} disparador=${DISPARADOR} causa=${CAUSA_DISPARO} run_id=${RUN_ID}"
  log "${linea}"
  CIERRE_ESCRITO=1
  printf -v contenido '[ADQ-SELECCION] run_id=%s %s\n[ADQ-RESULTADO] run_id=%s %s\n%s' \
    "$RUN_ID" "$SELECCION_JSON" "$RUN_ID" "$RESULTADO_PUBLICO" "$linea"
  if commit_censo_linea "$contenido" "$linea" "[ADQ] ${FECHA}"; then
    PUBLICACION_ESTADO="OK"
  else
    PUBLICACION_ESTADO="FALLIDA"
    if [ "${PUBLICACION_FALLIDA:-0}" -gt "$fallidas_antes" ]; then
      # commit_censo_linea ya volvió a `main` antes de devolver el fallo
      # -- hay que regresar a censo/${FECHA} para corregir el commit que
      # de verdad quedó mal etiquetado, nunca amendar lo que sea que HEAD
      # de main tenga en ese momento.
      local archivo="${CENSO_DIR}/${FECHA}.txt" linea_corregida
      local rama_censo="censo/${FECHA}"
      linea_corregida="${linea/publicacion=${publicacion}/publicacion=FALLIDA(${PUBLICACION_FALLIDA})}"
      if git checkout "$rama_censo" >>"$LOGFILE" 2>&1; then
        if [ -f "$archivo" ]; then
          sed -i "\$ s/publicacion=${publicacion}/publicacion=FALLIDA(${PUBLICACION_FALLIDA})/" \
            "$archivo" 2>>"$LOGFILE" || true
          git add "$archivo" >>"$LOGFILE" 2>&1 || true
        fi
        git commit --amend -m "[ADQ] ${FECHA}

${linea_corregida}" >>"$LOGFILE" 2>&1 || true
        log "HUELLA-CORREGIDA: el push de esta huella falló; se corrigió el commit local (nunca empujado, en ${rama_censo}) para declarar: ${linea_corregida}"
        restaura_arbol_operativo || true
      else
        log "HUELLA-NO-CORREGIDA: no se pudo volver a ${rama_censo} para corregir el commit local; el log ya declaró FALLIDA(${PUBLICACION_FALLIDA}) aunque el commit quedó con publicacion=${publicacion}."
      fi
    fi
  fi
}

# ── Seam de solo-definición (ADQ_CRON_SOLO_DEFINE=1) ─────────────
# Con la variable puesta, este archivo define sus funciones y RETORNA sin
# ejecutar un solo paso: es lo que permite que tests/test_adq_cableado.py
# ejercite las funciones REALES (sonda_red, commit_censo_linea,
# escribe_heartbeat, extrae_prompt) con dobles de curl/git, en vez de
# reimplementarlas en el test y probar una copia que puede divergir. No
# cambia nada del camino de producción: el runner sin la variable corre
# exactamente igual que antes de este acto.
if [ -n "${ADQ_CRON_SOLO_DEFINE:-}" ]; then
  return 0 2>/dev/null || exit 0
fi

log "=== adquiere_cron.sh arrancando en $REPO_DIR (run_id=${RUN_ID} disparador=${DISPARADOR}) ==="

# Lock de instancia única. No bloqueante: una segunda invocación mientras
# la primera sigue viva no espera ni encola, se retira de inmediato -- el
# reintento del mismo día (permitido, P3) es responsabilidad de quien
# dispara el runner (scheduler o mano), no de esperar aquí.
if [ "${ADQ_LOCK_FD_INHERITED:-0}" != "1" ]; then
  exec 200>"$LOCKFILE"
fi
if [ "${ADQ_LOCK_FD_INHERITED:-0}" != "1" ] && ! flock -n 200; then
  FASE="PARO-LOCK"
  # H6: el rechazo se apendiza al LOG con su propio run_id -- NUNCA al
  # heartbeat, que sigue siendo del dueño que está trabajando. Antes de
  # este acto esta línea llamaba a escribe_heartbeat() y borraba el
  # STARTED de la instancia activa (reproducido: RUN-A/STARTED sustituido
  # por RUN-B/PARO-LOCK con A todavía dueño del lock).
  log "PARO-LOCK: ya hay una instancia de adquiere_cron.sh corriendo (${LOCKFILE} tomado). Esta invocación (run_id=${RUN_ID}) no toca git, ni el corpus, ni el heartbeat del dueño; termina de inmediato."
  exit 3
fi
SOY_DUENO_DEL_LOCK=1

# A partir de aquí sí tenemos el lock: instala el trap que SIEMPRE deja
# huella local (heartbeat + línea de log), pase lo que pase después --
# incluido un `git fetch` que falle bajo `set -e` antes de llegar a
# cualquier otro paso. `trap ... EXIT` de bash corre también cuando
# `set -e` mata el script por un comando que falló, no solo en un `exit`
# explícito.
finalizar() {
  local codigo=$?
  local estado="TERMINADO"
  [ "$codigo" -ne 0 ] && estado="FAILED"
  # H6: un proceso muerto sin haber escrito su cierre queda INCOMPLETO --
  # no se inventa un éxito ni una causa de muerte. `CIERRE_ESCRITO` solo
  # vale 1 si huella_adq() llegó a componer y registrar su línea.
  if [ "${CIERRE_ESCRITO:-0}" -ne 1 ]; then
    estado="INCOMPLETO"
    log "INCOMPLETO: run_id=${RUN_ID} terminó en fase=${FASE} sin haber escrito su huella [ADQ]. No se infiere ni éxito ni causa de muerte."
  fi
  log "=== adquiere_cron.sh terminado (run_id=${RUN_ID} fase=${FASE} exit=${codigo}) ==="
  escribe_heartbeat "$estado" "$codigo" 2>>"$LOGFILE" || true
  # Restauración segura del contexto: best-effort, nunca deja que un
  # checkout fallido dispare un segundo trap ni cambie el código de salida
  # que ya se reportó arriba.
  restaura_arbol_operativo || true
}
trap finalizar EXIT

escribe_heartbeat "STARTED" "-"

# 1 · árbol coherente. El launcher actualiza ANTES de cargar este archivo.
FASE="CLON-AL-DIA"
if [ -n "${ADQ_DEPLOY_SHA:-}" ]; then
  HEAD_REAL="$(git rev-parse HEAD)"
  if [ "$HEAD_REAL" != "$ADQ_DEPLOY_SHA" ]; then
    log "PARO-REVISION: launcher declaró $ADQ_DEPLOY_SHA pero el árbol está en $HEAD_REAL"
    exit 5
  fi
  log "árbol resuelto por launcher antes de cargar runner: sha=$HEAD_REAL modo=${ADQ_DEPLOY_MODE:-desconocido}"
else
  log "camino compatible sin launcher: git fetch && git checkout main && git pull"
  git fetch origin >>"$LOGFILE" 2>&1
  git checkout main >>"$LOGFILE" 2>&1
  git pull --ff-only origin main >>"$LOGFILE" 2>&1
fi
log "HEAD operativo: $(git log -1 --format='%h %s')"

# P1 (GEN2-SONDA-ADQ-CABLEADO): la configuración se lee y se valida AQUÍ,
# DESPUÉS de sincronizar -- antes se leía al arrancar el script, es decir
# contra la versión vieja del clon, y cada default entraba en silencio.
transicion "CONFIG"
EJECUTOR_JSON="$(python3 tools/adq_config.py --ejecutor-json)"
EJECUTOR="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["nombre"])')"
TIMEOUT_EJECUTOR="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["timeout"]["valor"])')"
KILL_AFTER_EJECUTOR="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["kill_after"]["valor"])')"
MAXIMO_FILAS="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["maximo_filas"])')"
log "CONFIG: ejecutor=$EJECUTOR timeout=${TIMEOUT_EJECUTOR}s kill_after=${KILL_AFTER_EJECUTOR}s maximo_filas=$MAXIMO_FILAS"
CALENDARIO_JSON="$(python3 tools/adq_config.py --calendario-json)"
ADQ_ZONA_HORARIA="$(printf '%s' "$CALENDARIO_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["zona_iana"])')"
CALENDARIO_DEGRADADO="$(printf '%s' "$CALENDARIO_JSON" | python3 -c 'import json,sys; print("si" if json.load(sys.stdin)["degradada"] else "no")')"
CALENDARIO_CAUSA="$(printf '%s' "$CALENDARIO_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["causa"] or "-")')"
export TZ="$ADQ_ZONA_HORARIA"
if [ "$CALENDARIO_DEGRADADO" = "si" ]; then
  CONFIG_DEGRADADA="${CONFIG_DEGRADADA}calendario "
  log "CONFIG-DEGRADADA: calendario; causa=${CALENDARIO_CAUSA}; valor_aplicado=$(printf '%s' "$CALENDARIO_JSON" | python3 -c 'import json,sys; c=json.load(sys.stdin); print(c["hora"]+" "+c["zona_iana"]+" dias="+",".join(c["dias_semana"]))'); fuente=respaldo-compatible."
fi
RUNBOOK="$(lee_config runbook 'forense/agente-adquisicion-v1_0.md')"
SONDA_URL="$(lee_config sonda_red_url 'https://www.inegi.org.mx/')"
if [ -n "$CONFIG_DEGRADADA" ]; then
  log "CONFIG-DEGRADADA (resumen): claves no leídas de data/adq-config.yaml -> ${CONFIG_DEGRADADA}. La corrida SIGUE con respaldos, pero queda declarado: una config rota no se sustituye en silencio."
fi

# ACTO MAESTRA38-CRON-3 · HUELLA-REAL-Y-PRUEBA-EN-CAJA. Estado ANTES,
# capturado apenas el clon queda al día y antes de cualquier PARO posible
# -- es el punto de referencia para medir lo que ESTA corrida produjo
# (D-b: [ADQ] deja huella siempre, con lo que pasó de verdad, nunca una
# constante). commits_nuevos/ramas_nuevas/archivos_modificados de la
# línea [ADQ] se miden contra esto, no se asumen ni se derivan de la cola.
HEAD_ANTES="$(git rev-parse HEAD)"
RAMAS_ANTES="$(git ls-remote --heads origin | wc -l)"
# SHA realmente usado por esta corrida -- va en la huella (P1).
HEAD_USADO="$HEAD_ANTES"
T0="$(date +%s)"

# 2 · corpus montado (A.2, tercera parte)
FASE="CORPUS"
if [ -d data/raw ] && [ -n "$(ls -A data/raw 2>/dev/null | head -1)" ]; then
  PRIMERA="$(ls data/raw | head -1)"
  log "corpus montado: ls data/raw | head -1 -> ${PRIMERA}"
else
  FASE="PARO-CORPUS"
  log "PARO: data/raw ausente o vacío (corpus no montado en esta caja). No se invoca claude -p."
  huella_adq "no" "PARO-CORPUS" "-"
  exit 1
fi

# 2.5 · censo diario de la raíz manual (ADR-326, MAESTRA37-N6)
#   Corre ANTES de claude -p y no depende de que el corpus (paso 2) esté
#   montado -- descargas_mx es una raíz externa, gitignorada por máquina
#   (data/raices.local.yaml), no data/raw. Si esa raíz no está configurada
#   en esta máquina, es PARO-RAIZ (una línea) y el resto del cron sigue
#   -- no es uno de los cuatro PARO que cortan antes de claude -p (ver
#   forense/notas/2026-09-06-MAESTRA38-CRON-3-spec.md, "desviación
#   declarada en P1(b)": PARO-RAIZ no tiene su propio exit 1).
FASE="CENSO-RAIZ"
CENSO_FILE=""  # fijado abajo si la raíz resuelve; el paso 2.6 (D-c) lo
                # consulta con `set -u` activo, así que necesita existir
                # vacío cuando 2.5 corrió en PARO-RAIZ.
RAIZ_RESUELTA="$(python3 -c "
import sys
sys.path.insert(0, 'tests')
import manifiesto
print(manifiesto.resolver_raiz('descargas_mx', '.', 'data/raw') or '')
" 2>/dev/null || true)"

if [ -n "$RAIZ_RESUELTA" ] && [ -d "$RAIZ_RESUELTA" ]; then
  publica_censo_manual
else
  log "PARO-RAIZ: descargas_mx no resuelve en esta máquina (data/raices.local.yaml). Censo omitido, sigue con /adquiere."
fi

# 2.6 · re-baja mensual de los cuatro bulk oficiales de la PDN (ACTO MAESTRA38-A5,
#   FP-321/nota fila 28 de cola-adquisicion-registro.tsv). Los bulk se regeneran
#   con el tiempo (S3 lleva fecha 9/may/2025 congelada desde hace meses, sin
#   garantía de que siga así); gate día 1-3 del mes para no bajar ~3.9 GB a diario.
#   URLs/claves/ids ya no están cableados aquí -- vienen de
#   data/adq-config.yaml vía tools/adq_config.py (ACTO ADQ-CRON-V2, P6).
#   Si Google Drive cambia el id, este paso falla con log, no rompe el
#   resto del cron (no lleva set -e local, se aísla con `|| true`).
#   ACTO AUTOMATIZA-2-E4 · PDN-COMPARA: detecta identidad de bytes -- no
#   decide que el recurso cambió conceptualmente, no reemplaza payload, no
#   actualiza manifiesto ni relaciones, no lanza mediciones.
#   D-c (cumplido desde AUTOMATIZA-2-E4): COMMITEA, por sistema, el
#   resultado real de --compara-sha en censo/${FECHA}. Fuera de ventana
#   también deja una línea commiteada, para que el día 4 no parezca silencio.
FASE="PDN"
DIA_MES_A5="$(date +%-d)"
PDN_VENTANA_INICIO="$(lee_config pdn.ventana_dia_inicio 1)"
PDN_VENTANA_FIN="$(lee_config pdn.ventana_dia_fin 3)"
if [ "$DIA_MES_A5" -ge "$PDN_VENTANA_INICIO" ] && [ "$DIA_MES_A5" -le "$PDN_VENTANA_FIN" ]; then
  ADQ_PDN_DIR="data/raw/pdn_bulk_$(date +%Y_%m)"
  mkdir -p "$ADQ_PDN_DIR"
  LINEAS_PDN=()
  for SIS_LOGICO in s1 s2 s3 s6; do
    URL="$(python3 tools/adq_config.py "pdn.sistemas.${SIS_LOGICO}.url")"
    SIS_DESCARGA="$(python3 tools/adq_config.py "pdn.sistemas.${SIS_LOGICO}.sis_descarga")"
    ID_MANIFIESTO="$(python3 tools/adq_config.py "pdn.sistemas.${SIS_LOGICO}.id_manifiesto")"
    DEST="${ADQ_PDN_DIR}/pdn_${SIS_DESCARGA}_$(date +%Y-%m-%d).zip"
    if curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36" --max-time 300 -L -o "$DEST" "$URL" 2>>"$LOGFILE"; then
      # P6: antes de --compara-sha, verificar que la descarga terminó bien
      # y que el contenedor ZIP es legible. --compara-sha compara bytes,
      # no legibilidad -- no distingue "cambió el contenido" de "la
      # descarga quedó a medias" o "el servidor devolvió un error HTML con
      # nombre .zip". No adjudica un cambio de bytes por sí solo (Enmienda 4).
      if [ ! -s "$DEST" ]; then
        LINEAS_PDN+=("[ADQ-PDN] ${SIS_LOGICO}: PARO-DESCARGA-VACIA, ${DEST} quedó en 0 bytes")
        log "[ADQ-PDN] ${SIS_LOGICO}: PARO-DESCARGA-VACIA, ${DEST} quedó en 0 bytes"
        rm -f "$DEST"
      elif ! python3 -c "
import sys, zipfile
try:
    with zipfile.ZipFile(sys.argv[1]) as z:
        sys.exit(1 if z.testzip() else 0)
except zipfile.BadZipFile:
    sys.exit(1)
" "$DEST" 2>>"$LOGFILE"; then
        LINEAS_PDN+=("[ADQ-PDN] ${SIS_LOGICO}: PARO-ZIP-ILEGIBLE, ${DEST} no es un ZIP válido o falló testzip()")
        log "[ADQ-PDN] ${SIS_LOGICO}: PARO-ZIP-ILEGIBLE, ${DEST} no es un ZIP válido o falló testzip()"
      else
        SALIDA_COMPARA="$(python3 tests/manifiesto.py --compara-sha --id "$ID_MANIFIESTO" --archivo "$DEST" 2>>"$LOGFILE" || true)"
        LINEAS_PDN+=("[ADQ-PDN] ${SIS_LOGICO}: ${SALIDA_COMPARA}")
        log "[ADQ-PDN] ${SIS_LOGICO}: ${SALIDA_COMPARA}"
      fi
    else
      LINEAS_PDN+=("[ADQ-PDN] ${SIS_LOGICO}: PARO-RED, no se pudo re-bajar desde ${URL}")
      log "[ADQ-PDN] ${SIS_LOGICO}: PARO-RED, no se pudo re-bajar desde ${URL}"
      rm -f "$DEST"
    fi
    sleep 1
  done
  CONTENIDO_PDN="$(printf '%s\n' "${LINEAS_PDN[@]}")"
  RESUMEN_PDN="[ADQ-PDN] ${FECHA}: 4 sistemas (s1/s2/s3/s6), ver detalle por sistema arriba"
  commit_censo_linea "${CONTENIDO_PDN}" "${RESUMEN_PDN}" "[ADQ-PDN] ${FECHA}"
else
  LINEA_PDN="[ADQ-PDN] ${FECHA}: fuera de ventana (día ${DIA_MES_A5}, ventana ${PDN_VENTANA_INICIO}-${PDN_VENTANA_FIN})"
  log "${LINEA_PDN}"
  commit_censo_linea "$LINEA_PDN" "$LINEA_PDN" "[ADQ-PDN] ${FECHA}"
fi

# 3 · sonda de red real, valor crudo (nunca curl -I)
transicion "SONDA-RED"
if ! sonda_red "$SONDA_URL"; then
  FASE="PARO-RED"
  log "PARO-RED: ${CAUSA_RED}. No se invoca claude -p -- la compuerta corta ANTES de gastar la invocación."
  huella_adq "no" "PARO-RED" "-"
  exit 1
fi
log "sonda de red superada: ${CAUSA_RED}"

# 4 · ejecuta el procedimiento con el ejecutor seleccionado.
#   Extrae solo el bloque ```text ... ``` de §1, no el archivo entero:
#   el runbook trae prosa de mesa (firmas, razones, línea de crontab) que
#   no es parte del prompt de la tarea recurrente.
FASE="EXTRAE-PROMPT"
if [ ! -f "$RUNBOOK" ]; then
  FASE="PARO-PROMPT"
  log "PARO: no se encuentra ${RUNBOOK}."
  huella_adq "no" "PARO-PROMPT" "-"
  exit 1
fi

PROMPT="$(extrae_prompt "$RUNBOOK" || true)"

if [ -z "$PROMPT" ]; then
  FASE="PARO-PROMPT"
  log "PARO: no se pudo extraer el bloque de prompt (\`\`\`text ... \`\`\`) de ${RUNBOOK}. No se invoca el ejecutor a ciegas con el archivo entero."
  huella_adq "no" "PARO-PROMPT" "-"
  exit 1
fi

log "prompt extraído (§1 de ${RUNBOOK}), $(echo "$PROMPT" | wc -l) líneas:"
echo "$PROMPT" >>"$LOGFILE"

transicion "SELECCION"
SELECCION_JSON="$(python3 tools/adq_doctor.py --selecciona --maximo "$MAXIMO_FILAS" --json | python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), ensure_ascii=False, separators=(",",":")))')"
SELECCION_ELEGIDOS="$(printf '%s' "$SELECCION_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(",".join(x["id"] for x in d["elegidos"]) or "ninguno")')"
SELECCION_EXCLUIDOS="$(printf '%s' "$SELECCION_JSON" | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["excluidos"]))')"
log "selección autoritativa: elegidos=${SELECCION_ELEGIDOS} excluidos=${SELECCION_EXCLUIDOS} máximo=${MAXIMO_FILAS}"

PROMPT_EFECTIVO="${PROMPT}

INSTRUCCIÓN DE EJECUCIÓN PARA CODEX CLI:
Lee completa .claude/commands/adquiere.md y ejecuta ese procedimiento; la frase histórica 'Corre /adquiere' no depende de un slash command registrado. No invoques tools/adquiere_launcher.sh, tools/adquiere_cron.sh, Task Scheduler ni otro agente: ya eres el único hijo de esa corrida. Preserva cualquier modificación ajena, especialmente data/manifiesto-staging.yaml, y nunca la incluyas en un commit. Máximo ${MAXIMO_FILAS} filas.
Esta es la selección proyectada inmediatamente antes de tu arranque; contrástala y reporta todos los elegidos y excluidos con causa:
${SELECCION_JSON}
Tu último mensaje debe cumplir tools/adq-resultado.schema.json. Exit 0 sólo si ejecutaste el recorrido: una cola vacía exige resultado_sustantivo=cola_vacia y la lista completa; no basta dejar un plan o pedir otra sesión."

# set +e/-e: la huella [ADQ] tiene que capturar el código real de salida
# incluso cuando el hijo falla -- bajo `set -e`
# 13) un `cmd; CODIGO=$?` normal aborta el script en `cmd` mismo, antes
# de llegar a leer `$?`, y huella_adq() nunca se llamaría. Ventana
# mínima, solo alrededor de esta invocación (necesario para que la
# huella de ACTO MAESTRA38-CRON-3 funcione, no un cambio de lógica de
# negocio). `timeout(1)` envuelve la invocación (P3): un `claude -p`
# colgado ya no puede dejar la instancia con el lock tomado
# indefinidamente -- exit 124 si lo mató por timeout.
set +e
if [ "$EJECUTOR" = "codex" ]; then
  FASE="CODEX"
  CODEX_BINARIO="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["codex"]["binario"])')"
  MODELO_CONFIGURADO="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["codex"]["modelo"])')"
  CODEX_SANDBOX="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["codex"]["sandbox"])')"
  CODEX_DIR_ADICIONAL="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["codex"]["directorio_adicional"])')"
  CODEX_ESQUEMA="$(printf '%s' "$EJECUTOR_JSON" | python3 -c 'import json,sys; print(json.load(sys.stdin)["codex"]["esquema_resultado"])')"
  if [ ! -x "$CODEX_BINARIO" ]; then
    log "PARO-EJECUTOR: binario Codex no ejecutable: $CODEX_BINARIO"
    CODIGO_SALIDA=127
  elif ! "$CODEX_BINARIO" login status >>"$LOGFILE" 2>&1; then
    log "PARO-AUTENTICACION: codex login status no confirmó una sesión"
    CODIGO_SALIDA=78
  else
    CLI_VERSION="$($CODEX_BINARIO --version 2>&1 | tail -1)"
    MODELO_EFECTIVO="$MODELO_CONFIGURADO"
    EVENTOS_CODEX="$LOGDIR/${RUN_ID}-codex.jsonl"
    STDERR_CODEX="$LOGDIR/${RUN_ID}-codex.stderr.log"
    ULTIMO_MENSAJE="$LOGDIR/${RUN_ID}-codex-final.json"
    PROMPT_LOCAL="$LOGDIR/${RUN_ID}-prompt.txt"
    printf '%s\n' "$PROMPT_EFECTIVO" >"$PROMPT_LOCAL"
    log "invocando: timeout --kill-after=${KILL_AFTER_EJECUTOR}s ${TIMEOUT_EJECUTOR}s codex exec --json --sandbox ${CODEX_SANDBOX} --model ${MODELO_CONFIGURADO} --add-dir ${CODEX_DIR_ADICIONAL} (aprobaciones=never red=true)"
    timeout --kill-after="${KILL_AFTER_EJECUTOR}s" "${TIMEOUT_EJECUTOR}s" \
      "$CODEX_BINARIO" exec --ignore-user-config --ephemeral --json --color never \
      --sandbox "$CODEX_SANDBOX" --model "$MODELO_CONFIGURADO" \
      --add-dir "$CODEX_DIR_ADICIONAL" \
      -c 'approval_policy="never"' \
      -c 'sandbox_workspace_write.network_access=true' \
      --output-schema "$CODEX_ESQUEMA" --output-last-message "$ULTIMO_MENSAJE" \
      - <"$PROMPT_LOCAL" >"$EVENTOS_CODEX" 2>"$STDERR_CODEX"
    CODIGO_SALIDA=$?
    if [ "$CODIGO_SALIDA" -eq 0 ]; then
      if python3 - "$SELECCION_JSON" "$ULTIMO_MENSAJE" <<'PYEOF'
import json, sys
esperada = json.loads(sys.argv[1])
with open(sys.argv[2], encoding="utf-8") as f:
    resultado = json.load(f)
ids = [x["id"] for x in esperada["elegidos"]]
if resultado["ejecutor"] != "codex":
    raise SystemExit("ejecutor final distinto de codex")
if resultado["seleccion"]["elegidos"] != ids:
    raise SystemExit("la selección final no coincide con la proyección")
estado = resultado["resultado_sustantivo"]
if not ids and estado != "cola_vacia":
    raise SystemExit("cero elegidos exige resultado_sustantivo=cola_vacia")
if estado == "fallo":
    raise SystemExit("el hijo declaró fallo sustantivo")
PYEOF
      then
        RESULTADO_PUBLICO="$(python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1], encoding="utf-8")), ensure_ascii=False, separators=(",",":")))' "$ULTIMO_MENSAJE")"
        RESULTADO_SUSTANTIVO="$(printf '%s' "$RESULTADO_PUBLICO" | python3 -c 'import json,sys; print(json.load(sys.stdin)["resultado_sustantivo"])')"
      else
        log "PARO-RESULTADO: exit 0 sin evidencia sustantiva válida en $ULTIMO_MENSAJE"
        RESULTADO_SUSTANTIVO="resultado_invalido"
        CODIGO_SALIDA=65
      fi
    fi
  fi
else
  # Compatibilidad intencional: sólo entra si data/adq-config.yaml selecciona
  # explícitamente `claude`; nunca es fallback de un fallo de Codex.
  FASE="CLAUDE-COMPAT"
  CLI_VERSION="$(claude --version 2>&1 | head -1)"
  log "ejecutor=claude seleccionado explícitamente; invocando compatibilidad"
  timeout --kill-after="${KILL_AFTER_EJECUTOR}s" "${TIMEOUT_EJECUTOR}s" \
    claude --add-dir /home/pc0/mm-corpus -p "$PROMPT"
  CODIGO_SALIDA=$?
  RESULTADO_SUSTANTIVO="compatibilidad_claude"
fi
set -e
if [ "$CODIGO_SALIDA" -ne 0 ] && [ "$RESULTADO_SUSTANTIVO" = "no-invocado" ]; then
  RESULTADO_SUSTANTIVO="fallo_ejecutor"
fi
case "$CODIGO_SALIDA" in
  124) log "TIMEOUT-PROCESO: límite=${TIMEOUT_EJECUTOR}s; terminó durante gracia TERM->KILL=${KILL_AFTER_EJECUTOR}s; exit=124" ;;
  137) log "TIMEOUT-KILL: límite=${TIMEOUT_EJECUTOR}s y gracia TERM->KILL=${KILL_AFTER_EJECUTOR}s agotados; se aplicó KILL; exit=137" ;;
esac
log "${EJECUTOR} terminó con código ${CODIGO_SALIDA}; resultado=${RESULTADO_SUSTANTIVO}"

FASE="HUELLA-FINAL"
huella_adq "si" "-" "${CODIGO_SALIDA}"

# H5 · RESULTADO COMPUESTO: trabajo + publicación. Antes el runner
# devolvía el exit de Claude a secas, así que un recibo que nunca llegó al
# repo se leía como corrida exitosa. «El agente terminó» y «la huella se
# publicó» son dos cosas y ahora se reportan como dos cosas.
FASE="FIN"
if [ "${PUBLICACION_FALLIDA:-0}" -gt 0 ]; then
  log "RESULTADO-COMPUESTO: ${EJECUTOR} cerró con ${CODIGO_SALIDA}, pero ${PUBLICACION_FALLIDA} recibo(s) requerido(s) NO se publicaron (quedan locales en ${CENSO_DIR}/). Fallo operativo: exit 4."
  exit 4
fi
log "RESULTADO-COMPUESTO: trabajo exit=${CODIGO_SALIDA}, publicación OK."
exit "$CODIGO_SALIDA"
