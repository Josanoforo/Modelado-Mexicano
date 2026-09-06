#!/usr/bin/env bash
# tools/adquiere_cron.sh — cron de mesa para el agente de adquisición.
#
# ACTO MAESTRA34-N7 · SKILLS-COLA-Y-ADQ
# (forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md).
# Este script SE ESCRIBE aquí; su instalación en crontab (línea sugerida
# en forense/agente-adquisicion-v1_0.md) es tarea de mesa, no de este
# acto — no se instala solo, y no se corre desde una sesión de nube.
#
# Uso: cd /ruta/al/clon && ./tools/adquiere_cron.sh
# (o vía cron, ver la línea sugerida en el runbook)

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

FECHA="$(date +%Y-%m-%d)"
LOGDIR="forense/adq-log"
mkdir -p "$LOGDIR"
LOGFILE="$LOGDIR/${FECHA}.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S%z')] $*" | tee -a "$LOGFILE"
}

log "=== adquiere_cron.sh arrancando en $REPO_DIR ==="

# 1 · clon al día
log "git fetch && git checkout main && git pull"
git fetch origin >>"$LOGFILE" 2>&1
git checkout main >>"$LOGFILE" 2>&1
git pull origin main >>"$LOGFILE" 2>&1
log "HEAD tras pull: $(git log -1 --format='%h %s')"

# 2 · corpus montado (A.2, tercera parte)
if [ -d data/raw ] && [ -n "$(ls -A data/raw 2>/dev/null | head -1)" ]; then
  PRIMERA="$(ls data/raw | head -1)"
  log "corpus montado: ls data/raw | head -1 -> ${PRIMERA}"
else
  log "PARO: data/raw ausente o vacío (corpus no montado en esta caja). No se invoca claude -p."
  exit 1
fi

# 2.5 · censo diario de la raíz manual (ADR-326, MAESTRA37-N6)
#   Corre ANTES de claude -p y no depende de que el corpus (paso 2) esté
#   montado -- descargas_mx es una raíz externa, gitignorada por máquina
#   (data/raices.local.yaml), no data/raw. Si esa raíz no está configurada
#   en esta máquina, es PARO-RAIZ (una línea) y el resto del cron sigue.
CENSO_DIR="forense/censo-raiz"
CENSO_FILE=""  # fijado en el paso 2.5 si la raíz resuelve; el paso 2.6
                # (D-c) lo consulta con `set -u` activo, así que necesita
                # existir vacío cuando 2.5 corrió en PARO-RAIZ.
RAIZ_RESUELTA="$(python3 -c "
import sys
sys.path.insert(0, 'tests')
import manifiesto
print(manifiesto.resolver_raiz('descargas_mx', '.', 'data/raw') or '')
" 2>/dev/null || true)"

if [ -n "$RAIZ_RESUELTA" ] && [ -d "$RAIZ_RESUELTA" ]; then
  mkdir -p "$CENSO_DIR"
  CENSO_FILE="${CENSO_DIR}/${FECHA}.txt"
  if [ -e "$CENSO_FILE" ]; then
    CENSO_FILE="${CENSO_DIR}/${FECHA}-cron-$(date +%H%M).txt"
  fi
  SALIDA_CENSO="$(python3 tests/manifiesto.py --escanea descargas_mx 2>&1 || true)"
  RESUMEN="$(echo "$SALIDA_CENSO" | grep -m1 '^Total en disco:' || echo 'Total en disco: (sin resumen -- ver salida cruda abajo)')"

  # D-b (ACTO MAESTRA38-CRON-2 · REGISTRO-Y-HUELLA, forense/cron/
  # REGISTRO-CRON-v1_0.md §6): el trabajo [ADQ] SIEMPRE deja huella en el
  # censo del día, incluso con 0 objetivos -- nunca calla. n/m se leen de
  # la cola de adquisición si existe (fila por fila que el paso siguiente
  # de /adquiere procesaría); ante cualquier duda o ausencia de la cola,
  # se deja 0/0 explícito en vez de omitir la línea.
  ADQ_N_INTENTADOS=0
  ADQ_M_OBTENIDOS=0
  COLA_ADQ="data/cola-adquisicion-v1_0.tsv"
  if [ -f "$COLA_ADQ" ]; then
    ADQ_N_INTENTADOS="$(tail -n +2 "$COLA_ADQ" 2>/dev/null | grep -c . || echo 0)"
  fi
  LINEA_ADQ="[ADQ] ${FECHA}: ${ADQ_N_INTENTADOS} objetivos intentados / ${ADQ_M_OBTENIDOS} obtenidos"
  {
    echo "$RESUMEN"
    echo
    echo "$LINEA_ADQ"
    echo
    echo "$SALIDA_CENSO"
  } >"$CENSO_FILE"
  log "[CENSO] ${FECHA}: ${RESUMEN}"
  log "${LINEA_ADQ}"

  # Commit propio, separado del [ADQ] que produce claude -p más abajo.
  # main está protegida (status check "check" requerido) -- no se puede
  # empujar directo. En vez de eso: rama censo/${FECHA} + PR (--fill si
  # gh está disponible, si no se deja logueada la URL de compare) para
  # que el check corra y mesa firme. data/manifiesto-staging.yaml
  # (escrito por --escanea arriba) NO se commitea aquí -- este paso solo
  # hace `git add` de $CENSO_FILE. El archivo SÍ está trackeado en git
  # (no está en .gitignore -- corregido MAESTRA37-INFRA-1, ver B3: la
  # afirmación anterior de que sí lo estaba era falsa, `git ls-files
  # data/manifiesto-staging.yaml` lo confirma); sus cambios quedan sin
  # comitear por este cron hasta que un acto los recoja explícitamente.
  git add "$CENSO_FILE" >>"$LOGFILE" 2>&1
  if ! git diff --cached --quiet -- "$CENSO_FILE"; then
    git commit -m "[CENSO] ${FECHA}

${RESUMEN}" >>"$LOGFILE" 2>&1
    RAMA_CENSO="censo/${FECHA}"
    if git checkout -B "$RAMA_CENSO" >>"$LOGFILE" 2>&1 && git push -u origin "$RAMA_CENSO" >>"$LOGFILE" 2>&1; then
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
      git checkout main >>"$LOGFILE" 2>&1
    else
      log "PARO-CENSO-PUSH: el commit [CENSO] ${FECHA} quedó local, no se pudo empujar ${RAMA_CENSO}."
      git checkout main >>"$LOGFILE" 2>&1 || true
    fi
  else
    log "[CENSO] ${FECHA}: sin cambios respecto al censo previo, no se commitea de nuevo."
  fi
else
  log "PARO-RAIZ: descargas_mx no resuelve en esta máquina (data/raices.local.yaml). Censo omitido, sigue con /adquiere."
fi

# 2.6 · re-baja mensual de los cuatro bulk oficiales de la PDN (ACTO MAESTRA38-A5,
#   FP-321/nota fila 28 de cola-adquisicion-registro.tsv). Los bulk se regeneran
#   con el tiempo (S3 lleva fecha 9/may/2025 congelada desde hace meses, sin
#   garantía de que siga así); gate día 1-3 del mes para no bajar ~3.9 GB a diario.
#   URLs estáticas del bundle React (ADENDA-A4-rutas-PDN, .env REACT_APP_S1_BULK/
#   _BULK_S2/_S3_SERVIDORES/_S6) -- si Google Drive cambia el id, este paso falla
#   con log, no rompe el resto del cron (no lleva set -e local, se aísla con `|| true`).
DIA_MES_A5="$(date +%-d)"
if [ "$DIA_MES_A5" -ge 1 ] && [ "$DIA_MES_A5" -le 3 ]; then
  ADQ_PDN_DIR="data/raw/pdn_bulk_$(date +%Y_%m)"
  mkdir -p "$ADQ_PDN_DIR"
  for PAR in \
    "s1:https://drive.google.com/uc?export=download&id=1RSYOwWabsWqtxt7VNHIjf-yt1P5bPSbE" \
    "s2:https://drive.google.com/uc?export=download&id=1KWcst_YLI5YVlKnzmd3Xm5prAP4NVhAD" \
    "s3P:https://drive.google.com/uc?export=download&id=1i-HjNju04xdKThHgGDAzHb97GdF_cqS8" \
    "s6:https://drive.google.com/uc?export=download&id=1OM-P1JAp7PKeGL_InRYOQ1UO5Vpcs9Oi"; do
    SIS="${PAR%%:*}"; URL="${PAR#*:}"
    DEST="${ADQ_PDN_DIR}/pdn_${SIS}_$(date +%Y-%m-%d).zip"
    if curl -sS -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36" --max-time 300 -L -o "$DEST" "$URL" 2>>"$LOGFILE"; then
      SHA_NUEVO="$(sha256sum "$DEST" | cut -d' ' -f1)"
      log "[ADQ-PDN] ${SIS}: re-bajado a ${DEST}, sha256=${SHA_NUEVO} (comparar a mano contra data/manifiesto.yaml; este paso no re-registra automáticamente)"
    else
      log "[ADQ-PDN] ${SIS}: PARO-RED, no se pudo re-bajar desde ${URL}"
      rm -f "$DEST"
    fi
    sleep 1
  done
  # D-c (ACTO MAESTRA38-CRON-2 · REGISTRO-Y-HUELLA, forense/cron/
  # REGISTRO-CRON-v1_0.md §6): tras la re-baja de los 4 bulk, re-escanea
  # descargas_mx para que aparezcan en el censo del día en vez de quedar
  # visibles solo en este log -- mismo comando que el paso 2.5, aislado
  # con `|| true` igual que el resto de este bloque (no rompe el cron si
  # el escaneo falla).
  SALIDA_ESCANEO_PDN="$(python3 tests/manifiesto.py --escanea descargas_mx 2>&1 || true)"
  RESUMEN_PDN="$(echo "$SALIDA_ESCANEO_PDN" | grep -m1 '^Total en disco:' || echo 'Total en disco: (sin resumen -- ver salida cruda abajo)')"
  if [ -f "$CENSO_FILE" ]; then
    {
      echo
      echo "[ADQ-PDN] re-escaneo tras re-baja mensual: ${RESUMEN_PDN}"
      echo
      echo "$SALIDA_ESCANEO_PDN"
    } >>"$CENSO_FILE"
  fi
  log "[ADQ-PDN] re-escaneo post-re-baja: ${RESUMEN_PDN}"
else
  log "[ADQ-PDN] ${FECHA}: fuera de ventana mensual (día ${DIA_MES_A5}, ventana 1-3), no se re-baja el bulk PDN hoy."
fi

# 3 · sonda de red real, valor crudo (nunca curl -I)
CODIGO_HTTP="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 https://www.inegi.org.mx/ || echo 'sin-respuesta')"
log "sonda inegi.org.mx: curl -s -o /dev/null -w '%{http_code}' --max-time 10 https://www.inegi.org.mx/ -> ${CODIGO_HTTP}"
if [ "$CODIGO_HTTP" = "sin-respuesta" ]; then
  log "PARO: sonda de red sin respuesta. No se invoca claude -p."
  exit 1
fi

# 4 · lanza claude -p con el prompt exacto de §1 del runbook.
#   Extrae solo el bloque ```text ... ``` de §1, no el archivo entero:
#   el runbook trae prosa de mesa (firmas, razones, línea de crontab) que
#   no es parte del prompt de la tarea recurrente.
RUNBOOK="forense/agente-adquisicion-v1_0.md"
if [ ! -f "$RUNBOOK" ]; then
  log "PARO: no se encuentra ${RUNBOOK}."
  exit 1
fi

PROMPT="$(awk '/^```text$/{flag=1; next} /^```$/{if(flag){flag=0}} flag' "$RUNBOOK")"

if [ -z "$PROMPT" ]; then
  log "PARO: no se pudo extraer el bloque de prompt (\`\`\`text ... \`\`\`) de ${RUNBOOK}. No se invoca claude -p a ciegas con el archivo entero."
  exit 1
fi

log "prompt extraído (§1 de ${RUNBOOK}), $(echo "$PROMPT" | wc -l) líneas:"
echo "$PROMPT" >>"$LOGFILE"

log "invocando: claude --add-dir /home/pc0/mm-corpus -p \"\$PROMPT\""
claude --add-dir /home/pc0/mm-corpus -p "$PROMPT" >>"$LOGFILE" 2>&1
CODIGO_SALIDA=$?
log "claude -p terminó con código ${CODIGO_SALIDA}"

log "=== adquiere_cron.sh terminado ==="
exit "$CODIGO_SALIDA"
