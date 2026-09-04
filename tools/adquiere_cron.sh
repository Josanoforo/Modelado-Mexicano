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
RAIZ_RESUELTA="$(python3 -c "
import sys
sys.path.insert(0, 'tests')
import manifiesto
print(manifiesto.resolver_raiz('descargas_mx', '.', 'data/raw') or '')
" 2>/dev/null || true)"

if [ -n "$RAIZ_RESUELTA" ] && [ -d "$RAIZ_RESUELTA" ]; then
  mkdir -p "$CENSO_DIR"
  CENSO_FILE="${CENSO_DIR}/${FECHA}.txt"
  SALIDA_CENSO="$(python3 tests/manifiesto.py --escanea descargas_mx 2>&1 || true)"
  RESUMEN="$(echo "$SALIDA_CENSO" | grep -m1 '^Total en disco:' || echo 'Total en disco: (sin resumen -- ver salida cruda abajo)')"
  {
    echo "$RESUMEN"
    echo
    echo "$SALIDA_CENSO"
  } >"$CENSO_FILE"
  log "[CENSO] ${FECHA}: ${RESUMEN}"

  # Commit propio, separado del [ADQ] que produce claude -p más abajo --
  # misma vía que ADR-281: el merge de mesa es la autorización, así que
  # empuja directo a main igual que [ADQ]. data/manifiesto-staging.yaml
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
    if git push origin main >>"$LOGFILE" 2>&1; then
      log "[CENSO] ${FECHA} commiteado y empujado a main"
    else
      log "PARO-CENSO-PUSH: el commit [CENSO] ${FECHA} quedó local, no se pudo empujar."
    fi
  else
    log "[CENSO] ${FECHA}: sin cambios respecto al censo previo, no se commitea de nuevo."
  fi
else
  log "PARO-RAIZ: descargas_mx no resuelve en esta máquina (data/raices.local.yaml). Censo omitido, sigue con /adquiere."
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

log "invocando: claude -p \"\$PROMPT\""
claude -p "$PROMPT" >>"$LOGFILE" 2>&1
CODIGO_SALIDA=$?
log "claude -p terminó con código ${CODIGO_SALIDA}"

log "=== adquiere_cron.sh terminado ==="
exit "$CODIGO_SALIDA"
