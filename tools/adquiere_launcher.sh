#!/usr/bin/env bash
# Launcher estable: resuelve la revisión antes de cargar la lógica mutable.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"
mkdir -p forense/adq-log/estado
LOCKFILE="forense/adq-log/estado/adquiere_cron.lock"
LAUNCH_LOG="forense/adq-log/launcher.log"

launcher_log() {
  printf '[%s] %s\n' "$(date --iso-8601=seconds)" "$*" >>"$LAUNCH_LOG"
}

# El mismo lock llega abierto al runner; no existe ventana entre despliegue y
# ejecución en la que otra instancia pueda cambiar el árbol.
exec 200>"$LOCKFILE"
if ! flock -n 200; then
  launcher_log "PARO-LOCK: otra adquisición posee $LOCKFILE"
  exit 3
fi

REVISION_SOLICITADA="${ADQ_DEPLOY_REVISION:-}"
git fetch origin main >>"$LAUNCH_LOG" 2>&1
OBJETIVO="origin/main"
MODO="main"
if [ -n "$REVISION_SOLICITADA" ]; then
  if git merge-base --is-ancestor "$REVISION_SOLICITADA" origin/main 2>/dev/null; then
    MODO="main-contiene-revision"
  else
    git cat-file -e "${REVISION_SOLICITADA}^{commit}" 2>/dev/null || {
      launcher_log "PARO-REVISION: no existe el commit autorizado $REVISION_SOLICITADA"
      exit 5
    }
    OBJETIVO="$REVISION_SOLICITADA"
    MODO="revision-fijada"
  fi
fi

# Checkout normal, nunca reset/clean: si una modificación ajena entra en
# conflicto, Git aborta y el launcher preserva el árbol tal cual.
git checkout --detach "$OBJETIVO" >>"$LAUNCH_LOG" 2>&1
SHA_RESUELTO="$(git rev-parse HEAD)"
launcher_log "DESPLIEGUE: modo=$MODO solicitado=${REVISION_SOLICITADA:--} resuelto=$SHA_RESUELTO"

export ADQ_DEPLOY_SHA="$SHA_RESUELTO"
export ADQ_DEPLOY_MODE="$MODO"
export ADQ_LOCK_FD_INHERITED=1
exec bash "$REPO_DIR/tools/adquiere_cron.sh"
