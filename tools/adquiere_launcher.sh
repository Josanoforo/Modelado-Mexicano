#!/usr/bin/env bash
# Launcher estable: resuelve la revisión antes de cargar la lógica mutable.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"
mkdir -p forense/adq-log/estado
LOCKFILE="forense/adq-log/estado/adquiere_cron.lock"
LAUNCH_LOG="forense/adq-log/launcher.log"
HEARTBEAT="forense/adq-log/estado/heartbeat.json"

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
FECHA="$(TZ=America/Mexico_City date +%Y-%m-%d)"
RUN_ID="${FECHA}T$(TZ=America/Mexico_City date +%H%M%S)-$$"
INICIO_ISO="$(TZ=America/Mexico_City date --iso-8601=seconds)"
DISPARADOR="${ADQ_DISPARADOR:-manual}"
CAUSA_DISPARO="${ADQ_CAUSA_DISPARO:-$DISPARADOR}"
MM_TRAMO="${MM_TRAMO:-ambos}"
case "$MM_TRAMO" in
  ambos|adquisicion|derivacion) ;;
  *)
    launcher_log "PARO-TRAMO: MM_TRAMO=${MM_TRAMO} no es ambos|adquisicion|derivacion"
    exit 6
    ;;
esac
FASE="LAUNCHER-INICIO"
MOTIVO_CIERRE="-"
SHA_PREVIO="$(git rev-parse HEAD 2>/dev/null || printf desconocido)"
SHA_RESUELTO="desconocido"

# El launcher debe poder explicar incluso un fallo ocurrido antes de cargar la
# revisión nueva del runner. Por eso este escritor es autocontenido y existe en
# la versión estable que la tarea ya invocó. Sólo el dueño del lock llega aquí.
launcher_heartbeat() {
  local estado="$1" codigo="${2:--}"
  python3 - "$HEARTBEAT" "$RUN_ID" "$$" "$estado" "$FASE" "$codigo" \
    "$DISPARADOR" "$CAUSA_DISPARO" "$INICIO_ISO" "$REVISION_SOLICITADA" \
    "$SHA_PREVIO" "$SHA_RESUELTO" "$MOTIVO_CIERRE" <<'PYEOF'
import datetime, json, os, sys, tempfile
(ruta, run_id, pid, estado, fase, codigo, disparador, causa, inicio,
 revision, sha_previo, sha_resuelto, motivo) = sys.argv[1:14]
ahora = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
doc = {
    "run_id": run_id, "pid": int(pid), "estado": estado, "fase": fase,
    "componente": "launcher", "disparador": disparador,
    "causa_disparo": causa, "inicio": inicio, "actualizado": ahora,
    "revision_solicitada": revision or None, "sha_previo": sha_previo,
    "sha": sha_resuelto, "motivo": motivo,
    "codigo_salida": None if codigo in ("", "-") else int(codigo),
}
if estado in ("FAILED", "TERMINADO", "INCOMPLETO"):
    doc["fin"] = ahora
directorio = os.path.dirname(os.path.abspath(ruta)) or "."
fd, temporal = tempfile.mkstemp(dir=directorio, prefix=".heartbeat-launcher-", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporal, ruta)
except BaseException:
    try:
        os.unlink(temporal)
    except OSError:
        pass
    raise
PYEOF
}

finaliza_launcher() {
  local codigo=$?
  local estado="TERMINADO"
  [ "$codigo" -ne 0 ] && estado="FAILED"
  [ "$MOTIVO_CIERRE" = "-" ] && MOTIVO_CIERRE="salida-inesperada-en-${FASE}"
  launcher_log "CIERRE: run_id=$RUN_ID fase=$FASE exit=$codigo motivo=$MOTIVO_CIERRE sha=$SHA_RESUELTO"
  launcher_heartbeat "$estado" "$codigo" || launcher_log "PARO-HEARTBEAT: no se pudo escribir cierre local para run_id=$RUN_ID"
}
trap finaliza_launcher EXIT

launcher_log "INICIO: run_id=$RUN_ID disparador=$DISPARADOR sha_previo=$SHA_PREVIO revision_solicitada=${REVISION_SOLICITADA:--}"
launcher_heartbeat "STARTED" "-" || launcher_log "PARO-HEARTBEAT: no se pudo escribir inicio local para run_id=$RUN_ID"

FASE="LAUNCHER-FETCH"
launcher_heartbeat "EN-CURSO" "-" || true
set +e
git fetch origin main >>"$LAUNCH_LOG" 2>&1
CODIGO_FETCH=$?
set -e
if [ "$CODIGO_FETCH" -ne 0 ]; then
  MOTIVO_CIERRE="git-fetch-origin-main"
  exit "$CODIGO_FETCH"
fi
OBJETIVO="origin/main"
MODO="main"
if [ -n "$REVISION_SOLICITADA" ]; then
  if git merge-base --is-ancestor "$REVISION_SOLICITADA" origin/main 2>/dev/null; then
    MODO="main-contiene-revision"
  else
    git cat-file -e "${REVISION_SOLICITADA}^{commit}" 2>/dev/null || {
      FASE="PARO-REVISION"
      MOTIVO_CIERRE="revision-autorizada-no-existe"
      launcher_log "PARO-REVISION: no existe el commit autorizado $REVISION_SOLICITADA"
      exit 5
    }
    OBJETIVO="$REVISION_SOLICITADA"
    MODO="revision-fijada"
  fi
fi

# Checkout normal, nunca reset/clean: si una modificación ajena entra en
# conflicto, Git aborta y el launcher preserva el árbol tal cual.
FASE="LAUNCHER-CHECKOUT"
launcher_heartbeat "EN-CURSO" "-" || true
set +e
git checkout --detach "$OBJETIVO" >>"$LAUNCH_LOG" 2>&1
CODIGO_CHECKOUT=$?
set -e
if [ "$CODIGO_CHECKOUT" -ne 0 ]; then
  MOTIVO_CIERRE="git-checkout-${OBJETIVO}"
  exit "$CODIGO_CHECKOUT"
fi
SHA_RESUELTO="$(git rev-parse HEAD)"
launcher_log "DESPLIEGUE: modo=$MODO solicitado=${REVISION_SOLICITADA:--} resuelto=$SHA_RESUELTO"

# El mismo scheduler y el mismo launcher disparan el tramo determinista, pero
# éste conserva lock y worktree propios. Va antes de cualquier decisión de
# presupuesto/despacho: una cola de adquisición vacía nunca puede impedir la
# derivación diaria. MM_TRAMO=derivacion permite una activación controlada sin
# modelo, descarga ni escritura en el ledger de adquisición.
CODIGO_DERIVA=0
if [ "$MM_TRAMO" != "adquisicion" ]; then
  FASE="DERIVACION-DIARIA"
  launcher_heartbeat "EN-CURSO" "-" || true
  set +e
  env DERIVA_DISPARADOR="$DISPARADOR" \
      DERIVA_DEPLOY_REVISION="$SHA_RESUELTO" \
      bash "$REPO_DIR/tools/deriva_cron.sh" >>"$LAUNCH_LOG" 2>&1
  CODIGO_DERIVA=$?
  set -e
  launcher_log "DERIVACION-DIARIA: exit=${CODIGO_DERIVA} sha=${SHA_RESUELTO}"
fi
if [ "$MM_TRAMO" = "derivacion" ]; then
  MOTIVO_CIERRE="tramo-derivacion-exit-${CODIGO_DERIVA}"
  exit "$CODIGO_DERIVA"
fi

# El launcher ya posee el lock único y ya cargó el SHA que entiende el ledger.
# Recuperar aquí, antes de la comprobación ligera, evita el ciclo muerto
# «reserva huérfana agota presupuesto → no despacho → nunca llega al runner».
FASE="RECUPERA-PRESUPUESTO"
launcher_heartbeat "EN-CURSO" "-" || true
RECUPERACION_LOG="forense/adq-log/estado/${RUN_ID}-recuperacion-presupuesto.json"
set +e
python3 tools/adq_investigacion.py --recupera-presupuesto --owner "$RUN_ID" \
  --corte "$FECHA" --lock-exclusivo >"$RECUPERACION_LOG" 2>>"$LAUNCH_LOG"
CODIGO_RECUPERACION=$?
set -e
if [ "$CODIGO_RECUPERACION" -ne 0 ]; then
  MOTIVO_CIERRE="recuperacion-presupuesto-fallida"
  launcher_log "PARO-RECUPERACION: exit=${CODIGO_RECUPERACION}; la reserva se conserva; evidencia=${RECUPERACION_LOG}"
  exit "$CODIGO_RECUPERACION"
fi
PENDIENTES_RECUPERACION="$(python3 -c 'import json,sys; print(",".join(json.load(open(sys.argv[1], encoding="utf-8"))["recuperacion_pendiente"]) or "-")' "$RECUPERACION_LOG")"
launcher_log "RECUPERACION-PRESUPUESTO: pendientes=${PENDIENTES_RECUPERACION}; evidencia=${RECUPERACION_LOG}"

# Las activaciones horarias y de inicio de sesión sólo ejecutan esta
# comprobación determinista.  El mismo launcher continúa al runner únicamente
# cuando hay trabajo atendible, vence la recuperación diaria o cambió una
# entrada pertinente; nunca se crea otro scheduler ni se invoca un modelo para
# preguntar si hay trabajo.
if [ "${ADQ_COMPROBACION_LIGERA:-0}" = "1" ]; then
  FASE="COMPROBACION-LIGERA"
  launcher_heartbeat "EN-CURSO" "-" || true
  COMPROBACION_LOG="forense/adq-log/estado/${RUN_ID}-comprobacion.json"
  set +e
  python3 tools/adq_investigacion.py --comprueba-despacho >"$COMPROBACION_LOG" 2>>"$LAUNCH_LOG"
  CODIGO_COMPROBACION=$?
  set -e
  if [ "$CODIGO_COMPROBACION" -eq 10 ]; then
    MOTIVO_CIERRE="comprobacion-sin-despacho;derivacion-exit-${CODIGO_DERIVA}"
    launcher_log "COMPROBACION: sin despacho; evidencia=${COMPROBACION_LOG}"
    exit "$CODIGO_DERIVA"
  fi
  if [ "$CODIGO_COMPROBACION" -ne 0 ]; then
    MOTIVO_CIERRE="comprobacion-fallida"
    launcher_log "PARO-COMPROBACION: exit=${CODIGO_COMPROBACION}; evidencia=${COMPROBACION_LOG}"
    exit "$CODIGO_COMPROBACION"
  fi
  CAUSA_DISPARO="$(python3 -c 'import json,sys; print(",".join(json.load(open(sys.argv[1], encoding="utf-8"))["razones"]))' "$COMPROBACION_LOG")"
  export ADQ_CAUSA_DISPARO="$CAUSA_DISPARO"
  launcher_log "COMPROBACION: despacho requerido; causa=${CAUSA_DISPARO}; evidencia=${COMPROBACION_LOG}"
fi

FASE="LAUNCHER-HANDOFF"
MOTIVO_CIERRE="handoff-runner"
launcher_heartbeat "EN-CURSO" "-" || true
export ADQ_DEPLOY_SHA="$SHA_RESUELTO"
export ADQ_DEPLOY_MODE="$MODO"
export ADQ_LOCK_FD_INHERITED=1
export ADQ_RUN_ID="$RUN_ID"
export ADQ_INICIO_ISO="$INICIO_ISO"
set +e
bash "$REPO_DIR/tools/adquiere_cron.sh"
CODIGO_ADQUISICION=$?
set -e
if [ "$CODIGO_ADQUISICION" -ne 0 ]; then
  MOTIVO_CIERRE="adquisicion-exit-${CODIGO_ADQUISICION};derivacion-exit-${CODIGO_DERIVA}"
  exit "$CODIGO_ADQUISICION"
fi
if [ "$CODIGO_DERIVA" -ne 0 ]; then
  MOTIVO_CIERRE="adquisicion-exit-0;derivacion-exit-${CODIGO_DERIVA}"
  exit "$CODIGO_DERIVA"
fi
MOTIVO_CIERRE="adquisicion-exit-0;derivacion-exit-0"
exit 0
