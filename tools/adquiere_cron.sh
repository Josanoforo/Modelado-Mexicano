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

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

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
FASE="INICIO"

CLAUDE_TIMEOUT_SEGUNDOS="${CLAUDE_TIMEOUT_SEGUNDOS:-$(python3 tools/adq_config.py claude_timeout_segundos 2>/dev/null || echo 1800)}"
RUNBOOK="$(python3 tools/adq_config.py runbook 2>/dev/null || echo 'forense/agente-adquisicion-v1_0.md')"
SONDA_URL="$(python3 tools/adq_config.py sonda_red_url 2>/dev/null || echo 'https://www.inegi.org.mx/')"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S%z')] $*" | tee -a "$LOGFILE"
}

# escribe_heartbeat <estado> [codigo]
# JSON pequeño en $HEARTBEAT -- tools/adq_doctor.py (P4) lo lee tal cual.
# Escritura simple (no atómica con temp+rename como cierre_acto.py): un
# heartbeat truncado a medio escribir es, en el peor caso, un dato de
# diagnóstico perdido de ESTA corrida, no un archivo canónico del corpus.
escribe_heartbeat() {
  local estado="$1" codigo="${2:-}"
  python3 - "$HEARTBEAT" "$RUN_ID" "$$" "$estado" "$FASE" "$FECHA" "$codigo" <<'PYEOF'
import json, sys, datetime
ruta, run_id, pid, estado, fase, fecha, codigo = sys.argv[1:8]
doc = {
    "run_id": run_id,
    "pid": int(pid),
    "estado": estado,
    "fase": fase,
    "fecha": fecha,
    "codigo_salida": (int(codigo) if codigo not in ("", "-") else None),
    "actualizado": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}
with open(ruta, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)
    f.write("\n")
PYEOF
}

log "=== adquiere_cron.sh arrancando en $REPO_DIR (run_id=${RUN_ID}) ==="

# Lock de instancia única. No bloqueante: una segunda invocación mientras
# la primera sigue viva no espera ni encola, se retira de inmediato -- el
# reintento del mismo día (permitido, P3) es responsabilidad de quien
# dispara el runner (scheduler o mano), no de esperar aquí.
exec 200>"$LOCKFILE"
if ! flock -n 200; then
  FASE="PARO-LOCK"
  log "PARO-LOCK: ya hay una instancia de adquiere_cron.sh corriendo (${LOCKFILE} tomado). Esta invocación (run_id=${RUN_ID}) no toca git ni el corpus, termina de inmediato."
  escribe_heartbeat "PARO-LOCK" "-"
  exit 3
fi

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
  log "=== adquiere_cron.sh terminado (run_id=${RUN_ID} fase=${FASE} exit=${codigo}) ==="
  escribe_heartbeat "$estado" "$codigo" 2>>"$LOGFILE" || true
  # Restauración segura del contexto: best-effort, nunca deja que un
  # checkout fallido dispare un segundo trap ni cambie el código de salida
  # que ya se reportó arriba.
  git checkout main >>"$LOGFILE" 2>&1 || true
}
trap finalizar EXIT

escribe_heartbeat "STARTED" "-"

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

# 1 · clon al día
FASE="CLON-AL-DIA"
log "git fetch && git checkout main && git pull"
git fetch origin >>"$LOGFILE" 2>&1
git checkout main >>"$LOGFILE" 2>&1
git pull origin main >>"$LOGFILE" 2>&1
log "HEAD tras pull: $(git log -1 --format='%h %s')"

# ACTO MAESTRA38-CRON-3 · HUELLA-REAL-Y-PRUEBA-EN-CAJA. Estado ANTES,
# capturado apenas el clon queda al día y antes de cualquier PARO posible
# -- es el punto de referencia para medir lo que ESTA corrida produjo
# (D-b: [ADQ] deja huella siempre, con lo que pasó de verdad, nunca una
# constante). commits_nuevos/ramas_nuevas/archivos_modificados de la
# línea [ADQ] se miden contra esto, no se asumen ni se derivan de la cola.
HEAD_ANTES="$(git rev-parse HEAD)"
RAMAS_ANTES="$(git ls-remote --heads origin | wc -l)"
T0="$(date +%s)"

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
commit_censo_linea() {
  local contenido="$1" resumen="$2" mensaje="$3"
  local rama_censo="censo/${FECHA}"
  local archivo="${CENSO_DIR}/${FECHA}.txt"
  mkdir -p "$CENSO_DIR"

  checkout_o_crea_censo

  {
    echo
    echo "$contenido"
  } >>"$archivo"
  git add "$archivo" >>"$LOGFILE" 2>&1
  git commit -m "${mensaje}

${resumen}" >>"$LOGFILE" 2>&1
  if ! git push -u origin "$rama_censo" >>"$LOGFILE" 2>&1; then
    log "PARO-CENSO-PUSH: el commit de ${rama_censo} (${mensaje}) quedó local, no se pudo empujar."
  fi
  git checkout main >>"$LOGFILE" 2>&1
}

# huella_adq <invocado:si|no> <motivo:-|PARO-RAIZ|PARO-RED|PARO-PROMPT|PARO-CORPUS> <exit:codigo|->
# Formato congelado en forense/notas/2026-09-06-MAESTRA38-CRON-3-spec.md.
# Se llama en CADA PARO (exit 1) y una vez al terminar con éxito o con
# fallo de claude -p -- nunca calla, y si invocado=no los tres últimos
# campos se miden igual (deben dar 0 porque no hubo tiempo de producir
# nada, no se asumen en 0).
huella_adq() {
  local invocado="$1" motivo="$2" exit_cod="$3"
  local hhmm t1 duracion head_despues commits_nuevos ramas_despues ramas_nuevas archivos_modificados linea
  hhmm="$(date +%H:%M)"
  t1="$(date +%s)"
  duracion=$((t1 - T0))
  head_despues="$(git rev-parse HEAD 2>/dev/null || echo "$HEAD_ANTES")"
  commits_nuevos="$(git rev-list --count "${HEAD_ANTES}..${head_despues}" 2>/dev/null || echo 0)"
  ramas_despues="$(git ls-remote --heads origin 2>/dev/null | wc -l || echo "$RAMAS_ANTES")"
  ramas_nuevas=$((ramas_despues - RAMAS_ANTES))
  archivos_modificados="$(git status --short 2>/dev/null | wc -l)"

  linea="[ADQ] ${FECHA} ${hhmm}: invocado=${invocado} motivo=${motivo} exit=${exit_cod} duracion=${duracion}s commits_nuevos=${commits_nuevos} ramas_nuevas=${ramas_nuevas} archivos_modificados=${archivos_modificados} run_id=${RUN_ID}"
  log "${linea}"
  commit_censo_linea "$linea" "$linea" "[ADQ] ${FECHA}"
}

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
  mkdir -p "$CENSO_DIR"
  RAMA_CENSO="censo/${FECHA}"
  # ACTO ADQ-CRON-V2 (P3): cambia de rama ANTES de decidir el nombre del
  # archivo o escribir nada. Antes de este acto el add/commit ocurría
  # mientras el árbol seguía en `main` (checked out desde el paso 1) y
  # censo/${FECHA} se creaba/reseteaba DESPUÉS con `checkout -B` -- eso
  # dejaba `main` local contaminado con el commit [CENSO] cada corrida
  # (hecho 8) y, en un reintento el mismo día, reescribía censo/${FECHA}
  # desde ese `main` ya adelantado en vez de continuar lo que el remoto
  # ya tenía (hecho 9, el non-fast-forward real del 6/sep).
  checkout_o_crea_censo
  CENSO_FILE="${CENSO_DIR}/${FECHA}.txt"
  if [ -e "$CENSO_FILE" ]; then
    CENSO_FILE="${CENSO_DIR}/${FECHA}-cron-$(date +%H%M).txt"
  fi
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
      log "PARO-CENSO-PUSH: el commit [CENSO] ${FECHA} quedó local, no se pudo empujar ${RAMA_CENSO}."
    fi
  else
    log "[CENSO] ${FECHA}: sin cambios respecto al censo previo, no se commitea de nuevo."
  fi
  git checkout main >>"$LOGFILE" 2>&1 || true
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
PDN_VENTANA_INICIO="$(python3 tools/adq_config.py pdn.ventana_dia_inicio 2>/dev/null || echo 1)"
PDN_VENTANA_FIN="$(python3 tools/adq_config.py pdn.ventana_dia_fin 2>/dev/null || echo 3)"
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
FASE="SONDA-RED"
CODIGO_HTTP="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$SONDA_URL" || echo 'sin-respuesta')"
log "sonda ${SONDA_URL}: curl -s -o /dev/null -w '%{http_code}' --max-time 10 ${SONDA_URL} -> ${CODIGO_HTTP}"
if [ "$CODIGO_HTTP" = "sin-respuesta" ]; then
  FASE="PARO-RED"
  log "PARO: sonda de red sin respuesta. No se invoca claude -p."
  huella_adq "no" "PARO-RED" "-"
  exit 1
fi

# 4 · lanza claude -p con el prompt exacto de §1 del runbook.
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

PROMPT="$(awk '/^```text$/{flag=1; next} /^```$/{if(flag){flag=0}} flag' "$RUNBOOK")"

if [ -z "$PROMPT" ]; then
  FASE="PARO-PROMPT"
  log "PARO: no se pudo extraer el bloque de prompt (\`\`\`text ... \`\`\`) de ${RUNBOOK}. No se invoca claude -p a ciegas con el archivo entero."
  huella_adq "no" "PARO-PROMPT" "-"
  exit 1
fi

log "prompt extraído (§1 de ${RUNBOOK}), $(echo "$PROMPT" | wc -l) líneas:"
echo "$PROMPT" >>"$LOGFILE"

FASE="CLAUDE"
log "invocando: timeout ${CLAUDE_TIMEOUT_SEGUNDOS}s claude --add-dir /home/pc0/mm-corpus -p \"\$PROMPT\""
# set +e/-e: la huella [ADQ] tiene que capturar el código real de salida
# incluso cuando claude -p falla -- bajo `set -e` (activo desde la línea
# 13) un `cmd; CODIGO=$?` normal aborta el script en `cmd` mismo, antes
# de llegar a leer `$?`, y huella_adq() nunca se llamaría. Ventana
# mínima, solo alrededor de esta invocación (necesario para que la
# huella de ACTO MAESTRA38-CRON-3 funcione, no un cambio de lógica de
# negocio). `timeout(1)` envuelve la invocación (P3): un `claude -p`
# colgado ya no puede dejar la instancia con el lock tomado
# indefinidamente -- exit 124 si lo mató por timeout.
set +e
timeout "${CLAUDE_TIMEOUT_SEGUNDOS}s" claude --add-dir /home/pc0/mm-corpus -p "$PROMPT" >>"$LOGFILE" 2>&1
CODIGO_SALIDA=$?
set -e
if [ "$CODIGO_SALIDA" -eq 124 ]; then
  log "claude -p agotó el timeout de ${CLAUDE_TIMEOUT_SEGUNDOS}s (timeout(1) lo mató, exit 124)"
fi
log "claude -p terminó con código ${CODIGO_SALIDA}"

FASE="HUELLA-FINAL"
huella_adq "si" "-" "${CODIGO_SALIDA}"

FASE="FIN"
exit "$CODIGO_SALIDA"
