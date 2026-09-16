#!/usr/bin/env bash
# Rutina determinista diaria de derivados. Comparte el launcher/scheduler de
# adquisición, pero usa lock y worktree propios y nunca invoca un modelo.

set -euo pipefail

SOURCE_REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_DIR="$SOURCE_REPO_DIR"
FECHA="${DERIVA_FECHA:-$(TZ=America/Mexico_City date +%Y-%m-%d)}"
RUN_ID="${DERIVA_RUN_ID:-${FECHA}T$(TZ=America/Mexico_City date +%H%M%S)-$$}"
DISPARADOR="${DERIVA_DISPARADOR:-manual}"
case "$DISPARADOR" in
  windows-task-scheduler|manual|prueba-programada|fixture) ;;
  *) DISPARADOR="desconocido" ;;
esac

LOGROOT="${DERIVA_LOG_ROOT:-$SOURCE_REPO_DIR/forense/deriva-log}"
ESTADO_DIR="$LOGROOT/estado"
LOGFILE="$LOGROOT/${FECHA}.log"
HEARTBEAT="$ESTADO_DIR/heartbeat.json"
LOCKFILE="$ESTADO_DIR/deriva_cron.lock"
ULTIMA_EXITOSA="$ESTADO_DIR/ultima-exitosa.json"
DERIVADOS_DIR="data/curacion-universo/derivados"
RAMA="derivados/${FECHA}"
FASE="INICIO"
SOY_DUENO_DEL_LOCK=0
CIERRE_ESCRITO=0
WORKTREE_TEMP=""
CONSERVA_WORKTREE=0
T0="$(date +%s)"

mkdir -p "$ESTADO_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S%z')" "$*" | tee -a "$LOGFILE"
}

escribe_heartbeat() {
  local estado="$1" codigo="${2:--}"
  [ "${SOY_DUENO_DEL_LOCK:-0}" = 1 ] || return 0
  python3 - "$HEARTBEAT" "$RUN_ID" "$$" "$estado" "$FASE" "$FECHA" \
    "$codigo" "$DISPARADOR" "${SHA_EFECTIVO:-}" <<'PYEOF'
import datetime, json, os, sys, tempfile
(ruta, run_id, pid, estado, fase, fecha, codigo, disparador, sha) = sys.argv[1:10]
doc = {
    "run_id": run_id, "pid": int(pid), "estado": estado, "fase": fase,
    "fecha": fecha, "disparador": disparador, "sha_efectivo": sha or None,
    "codigo_salida": None if codigo in ("", "-") else int(codigo),
    "actualizado": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
}
d = os.path.dirname(os.path.abspath(ruta))
fd, tmp = tempfile.mkstemp(dir=d, prefix=".heartbeat-", suffix=".tmp")
try:
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2); f.write("\n")
        f.flush(); os.fsync(f.fileno())
    os.replace(tmp, ruta)
except BaseException:
    try: os.unlink(tmp)
    except OSError: pass
    raise
PYEOF
}

transicion() {
  FASE="$1"
  escribe_heartbeat "EN-CURSO" "-" 2>>"$LOGFILE" || true
}

huella_deriva() {
  local motivo="$1" codigo="$2" invocado="${3:-si}"
  local duracion=$(( $(date +%s) - T0 ))
  HUELLA_LINEA="[DERIVADOS] ${FECHA} $(date +%H:%M): invocado=${invocado} motivo=${motivo} exit=${codigo} duracion=${duracion}s disparador=${DISPARADOR} run_id=${RUN_ID} sha=${SHA_EFECTIVO:--}"
  log "$HUELLA_LINEA"
  CIERRE_ESCRITO=1
}

calcula_firma_entrada() {
  local corpus="$1" main_sha="$2"
  python3 - "$corpus" "$main_sha" <<'PYEOF'
import hashlib, os, sys
root, main = sys.argv[1:3]
h = hashlib.sha256((main + "\0").encode())
for base, dirs, files in os.walk(root):
    dirs.sort(); files.sort()
    for name in files:
        p = os.path.join(base, name)
        try: st = os.stat(p, follow_symlinks=True)
        except OSError: continue
        rel = os.path.relpath(p, root)
        h.update(f"{rel}\0{st.st_size}\0{st.st_mtime_ns}\0".encode())
print(h.hexdigest())
PYEOF
}

gate_diario_ya_completo() {
  [ "${DERIVA_FORZAR:-0}" != 1 ] || return 1
  [ -f "$ULTIMA_EXITOSA" ] || return 1
  python3 - "$ULTIMA_EXITOSA" "$FECHA" "$FIRMA_ENTRADA" <<'PYEOF'
import json, sys
try: d=json.load(open(sys.argv[1], encoding="utf-8"))
except (OSError, ValueError): raise SystemExit(1)
raise SystemExit(0 if d.get("fecha")==sys.argv[2] and d.get("firma_entrada")==sys.argv[3] else 1)
PYEOF
}

marca_exitosa() {
  python3 - "$ULTIMA_EXITOSA" "$FECHA" "$FIRMA_ENTRADA" "$RUN_ID" "${SHA_EFECTIVO:-}" <<'PYEOF'
import json, os, sys, tempfile
p, fecha, firma, run_id, sha = sys.argv[1:6]
d=os.path.dirname(os.path.abspath(p)); fd,tmp=tempfile.mkstemp(dir=d,prefix=".ultima-",suffix=".tmp")
with os.fdopen(fd,"w",encoding="utf-8") as f:
    json.dump({"fecha":fecha,"firma_entrada":firma,"run_id":run_id,"sha_efectivo":sha},f,indent=2); f.write("\n")
    f.flush(); os.fsync(f.fileno())
os.replace(tmp,p)
PYEOF
}

sincroniza_rama_diaria() {
  local objetivo="$1" existe_rc
  set +e
  git ls-remote --exit-code --heads origin "$RAMA" >>"$LOGFILE" 2>&1
  existe_rc=$?
  set -e
  if [ "$existe_rc" -eq 0 ]; then
    git fetch origin "+refs/heads/${RAMA}:refs/remotes/origin/${RAMA}" >>"$LOGFILE" 2>&1 || return 1
    git checkout --detach "origin/${RAMA}" >>"$LOGFILE" 2>&1 || return 1
    git merge --no-edit "$objetivo" >>"$LOGFILE" 2>&1 || return 1
  elif [ "$existe_rc" -eq 2 ]; then
    git checkout --detach "$objetivo" >>"$LOGFILE" 2>&1 || return 1
  else
    return "$existe_rc"
  fi
  RAMA_REMOTA_EXISTE="$([ "$existe_rc" -eq 0 ] && echo si || echo no)"
}

prepara_worktree_aislado() {
  local corpus objetivo
  transicion "SINCRONIZA"
  git -C "$SOURCE_REPO_DIR" fetch origin main >>"$LOGFILE" 2>&1 || return 1
  MAIN_SHA="$(git -C "$SOURCE_REPO_DIR" rev-parse origin/main)"
  objetivo="${DERIVA_DEPLOY_REVISION:-$MAIN_SHA}"
  git -C "$SOURCE_REPO_DIR" cat-file -e "${objetivo}^{commit}" 2>/dev/null || {
    log "PARO-REVISION: no existe ${objetivo}."; return 1;
  }
  git -C "$SOURCE_REPO_DIR" merge-base --is-ancestor "$MAIN_SHA" "$objetivo" || {
    log "PARO-REVISION: ${objetivo} no contiene origin/main=${MAIN_SHA}."; return 1;
  }
  corpus="${DERIVA_CORPUS_ROOT:-$(readlink -f "$SOURCE_REPO_DIR/data/raw" 2>/dev/null || true)}"
  [ -d "$corpus" ] && [ -n "$(find "$corpus" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ] || {
    log "PARO-CORPUS: raíz ausente o vacía (${corpus:-sin ruta})."; return 1;
  }
  FIRMA_ENTRADA="$(calcula_firma_entrada "$corpus" "$MAIN_SHA")"
  if gate_diario_ya_completo; then
    SHA_EFECTIVO="$objetivo"
    huella_deriva "NADA-QUE-HACER-YA-COMPLETADO" 0
    return 10
  fi

  WORKTREE_TEMP="$(mktemp -d "/tmp/modelado-deriva-${FECHA}-XXXXXX")"
  git -C "$SOURCE_REPO_DIR" worktree add --detach "$WORKTREE_TEMP" "$objetivo" >>"$LOGFILE" 2>&1 || return 1
  REPO_DIR="$WORKTREE_TEMP"
  ln -s "$corpus" "$REPO_DIR/data/raw"
  cd "$REPO_DIR"

  if ! sincroniza_rama_diaria "$objetivo"; then
    CONSERVA_WORKTREE=1
    log "PARO-SINCRONIZACION: no se pudo combinar ${RAMA} con ${objetivo}; worktree conservado en ${WORKTREE_TEMP}."
    return 1
  fi
  SHA_EFECTIVO="$(git rev-parse HEAD)"
  log "árbol efectivo: origin/main=${MAIN_SHA} revisión=${objetivo} HEAD=${SHA_EFECTIVO} rama_remota=${RAMA_REMOTA_EXISTE}"
}

deriva_suite() {
  set +e
  SALIDA_SUITE="$(python3 tests/check.py --baseline 2>&1)"; EXIT_SUITE=$?
  set -e
  printf '%s\n' "$SALIDA_SUITE" >>"$LOGFILE"
  DELTA_SUITE="$(printf '%s\n' "$SALIDA_SUITE" | grep -A 30 'LÍNEA BASE:' || true)"
  [ "$EXIT_SUITE" -eq 0 ] || return "$EXIT_SUITE"
}

siguiente_salida_universo() {
  local base="${DERIVADOS_DIR}/universo-${FECHA}.json" n=2
  if [ ! -e "$base" ]; then printf '%s\n' "$base"; return; fi
  while [ -e "${DERIVADOS_DIR}/universo-${FECHA}-r$(printf '%02d' "$n").json" ]; do n=$((n+1)); done
  printf '%s\n' "${DERIVADOS_DIR}/universo-${FECHA}-r$(printf '%02d' "$n").json"
}

deriva_universo() {
  local scratch anterior salida rc
  scratch="$(mktemp -d)"
  set +e
  python3 tools/curador_registro/snapshot_universe.py \
    --spec data/curacion-universo/inputs-t0.json --repo-root . \
    --corpus-root data/raw --output-dir "$scratch" >>"$LOGFILE" 2>&1
  rc=$?
  set -e
  if [ "$rc" -ne 0 ]; then
    DELTA_UNIVERSO="PARO-UNIVERSO: snapshot_universe.py salió ${rc}; scratch=${scratch}."
    CONSERVA_WORKTREE=1
    return "$rc"
  fi
  mkdir -p "$DERIVADOS_DIR"
  anterior="$(find "$DERIVADOS_DIR" -maxdepth 1 -type f -name 'universo-*.json' -print | sort | tail -1)"
  [ -n "$anterior" ] || anterior="data/curacion-universo/snapshot-t0.json"
  salida="$(siguiente_salida_universo)"
  set +e
  DELTA_UNIVERSO="$(python3 "$SOURCE_REPO_DIR/tools/deriva_resumen.py" \
    --nuevo "$scratch/snapshot-t0.json" --anterior "$anterior" \
    --universo-tsv "$scratch/universo-declarado-t0.tsv" \
    --ledger data/curacion-universo/ledger-inspecciones-t0.tsv \
    --ledger data/curacion-universo/ledger-inspecciones-barrido2.tsv \
    --fecha "$FECHA" --salida "$salida" 2>&1)"
  rc=$?
  set -e
  printf '%s\n' "$DELTA_UNIVERSO" >>"$LOGFILE"
  rm -rf -- "$scratch"
  [ "$rc" -eq 0 ] || return "$rc"
}

deriva_tablero() {
  local antes despues salida rc
  antes="$(git hash-object forense/tablero/TABLERO-PROGRAMA.md 2>/dev/null || printf '-')"
  set +e
  salida="$(python3 tools/tablero_programa.py --actualiza 2>&1)"; rc=$?
  set -e
  printf '%s\n' "$salida" >>"$LOGFILE"
  [ "$rc" -eq 0 ] || { DELTA_TABLERO="PARO-TABLERO: exit=${rc}"; return "$rc"; }
  despues="$(git hash-object forense/tablero/TABLERO-PROGRAMA.md 2>/dev/null || printf '-')"
  if [ "$antes" = "$despues" ]; then DELTA_TABLERO="sin cambios"; else DELTA_TABLERO="bloque derivado actualizado"; fi
}

deriva_registro() {
  local verifica status rv rs
  set +e
  verifica="$(python3 tools/corrida0.py registro --verifica 2>&1)"; rv=$?
  status="$(python3 tools/corrida0.py status 2>&1)"; rs=$?
  set -e
  printf '%s\n%s\n' "$verifica" "$status" >>"$LOGFILE"
  DELTA_REGISTRO="registro --verifica exit=${rv}; status exit=${rs}; $(printf '%s\n%s' "$verifica" "$status" | tail -12 | tr '\n' ' ' | cut -c1-900)"
  [ "$rv" -eq 0 ] && [ "$rs" -eq 0 ]
}

paso_obligatorio() {
  local nombre="$1" funcion="$2" rc
  transicion "$nombre"
  set +e; "$funcion"; rc=$?; set -e
  if [ "$rc" -ne 0 ]; then
    log "PARO-${nombre}: ${funcion} salió ${rc}; no se publican salidas parciales."
    return "$rc"
  fi
}

asegura_pr() {
  local abierto merged
  command -v gh >/dev/null 2>&1 || { log "PARO-PR: gh no disponible."; return 4; }
  abierto="$(gh pr list --head "$RAMA" --state open --json number --jq '.[0].number' 2>>"$LOGFILE")" || return 4
  if [ -n "$abierto" ]; then log "PR diario reutilizado: #${abierto}."; return 0; fi
  merged="$(gh pr list --head "$RAMA" --state merged --json number --jq '.[0].number' 2>>"$LOGFILE")" || return 4
  if [ -n "$merged" ]; then
    log "PUBLICACION-DIFERIDA: el PR diario #${merged} ya fue fusionado; cambios sustantivos posteriores se publicarán en la siguiente fecha."
    return 20
  fi
  gh pr create --title "[DERIVADOS] ${FECHA}" --body "$CUERPO" --base main --head "$RAMA" >>"$LOGFILE" 2>&1 || return 4
  log "PR diario abierto."
}

publica_cambios() {
  local commit_sha pr_rc
  git add -- "$DERIVADOS_DIR" forense/tablero/TABLERO-PROGRAMA.md >>"$LOGFILE" 2>&1
  if git diff --cached --quiet; then
    if git show-ref --verify --quiet "refs/remotes/origin/${RAMA}" && \
       ! git merge-base --is-ancestor "origin/${RAMA}" origin/main; then
      CUERPO="[DERIVADOS] ${FECHA}: sin cambios nuevos; publicación previa pendiente."
      asegura_pr || return $?
      RESULTADO_PUBLICACION="SIN-CAMBIOS-NUEVOS-PUBLICACION-PENDIENTE"
    else
      RESULTADO_PUBLICACION="NADA-QUE-HACER-SIN-PENDIENTES"
    fi
    return 0
  fi

  CUERPO="[DERIVADOS] ${FECHA}: disparador=${DISPARADOR} run_id=${RUN_ID} sha_efectivo=${SHA_EFECTIVO}

(a) universo: ${DELTA_UNIVERSO}
(b) tablero: ${DELTA_TABLERO}
(c) registro: ${DELTA_REGISTRO}
(d) suite: ${DELTA_SUITE}"

  set +e; asegura_pr; pr_rc=$?; set -e
  if [ "$pr_rc" -eq 20 ]; then
    git restore --staged -- "$DERIVADOS_DIR" forense/tablero/TABLERO-PROGRAMA.md
    RESULTADO_PUBLICACION="CAMBIOS-DIFERIDOS-PR-DIARIO-YA-FUSIONADO"
    return 0
  fi
  # rc=4 puede ser simplemente que la rama todavía no existe; después del
  # push se exige de nuevo y entonces sí determina el resultado.

  git commit -m "[DERIVADOS] ${FECHA}" -m "$CUERPO" >>"$LOGFILE" 2>&1 || return 2
  commit_sha="$(git rev-parse HEAD)"
  if ! git push origin "HEAD:refs/heads/${RAMA}" >>"$LOGFILE" 2>&1; then
    git -C "$SOURCE_REPO_DIR" branch "derivados-pendientes/${RUN_ID}" "$commit_sha" >>"$LOGFILE" 2>&1 || true
    log "PARO-PUSH: commit ${commit_sha} conservado en derivados-pendientes/${RUN_ID}; receta: git push origin derivados-pendientes/${RUN_ID}:refs/heads/${RAMA}."
    return 2
  fi
  set +e; asegura_pr; pr_rc=$?; set -e
  if [ "$pr_rc" -ne 0 ]; then
    git -C "$SOURCE_REPO_DIR" branch "derivados-pendientes/${RUN_ID}" "$commit_sha" >>"$LOGFILE" 2>&1 || true
    log "PARO-PR: commit ${commit_sha} ya está en origin/${RAMA}; receta: gh pr create --base main --head ${RAMA}."
    return 4
  fi
  RESULTADO_PUBLICACION="PUBLICADO:${commit_sha}"
}

if [ -n "${DERIVA_CRON_SOLO_DEFINE:-}" ]; then
  return 0 2>/dev/null || exit 0
fi

log "=== deriva_cron.sh inicio repo_fuente=${SOURCE_REPO_DIR} run_id=${RUN_ID} disparador=${DISPARADOR} ==="
exec 201>"$LOCKFILE"
if ! flock -n 201; then
  log "PARO-LOCK: otra derivación posee ${LOCKFILE}."
  exit 3
fi
SOY_DUENO_DEL_LOCK=1

finalizar() {
  local codigo=$? estado="TERMINADO"
  [ "$codigo" -eq 0 ] || estado="FAILED"
  if [ "$CIERRE_ESCRITO" -ne 1 ]; then
    estado="INCOMPLETO"
    log "INCOMPLETO: salida en fase=${FASE} sin huella final."
  fi
  escribe_heartbeat "$estado" "$codigo" 2>>"$LOGFILE" || true
  if [ -n "$WORKTREE_TEMP" ] && [ "$CONSERVA_WORKTREE" -eq 0 ]; then
    cd "$SOURCE_REPO_DIR"
    git -C "$SOURCE_REPO_DIR" worktree remove --force "$WORKTREE_TEMP" >>"$LOGFILE" 2>&1 || true
  elif [ -n "$WORKTREE_TEMP" ]; then
    log "evidencia local conservada en ${WORKTREE_TEMP}."
  fi
  log "=== deriva_cron.sh fin fase=${FASE} exit=${codigo} ==="
}
trap finalizar EXIT
escribe_heartbeat "STARTED" "-"

set +e; prepara_worktree_aislado; rc=$?; set -e
if [ "$rc" -eq 10 ]; then exit 0; fi
if [ "$rc" -ne 0 ]; then
  FASE="PARO-SINCRONIZA"; huella_deriva "PARO-SINCRONIZA" "$rc" "no"; exit "$rc"
fi

paso_obligatorio "SUITE" deriva_suite || { rc=$?; FASE="PARO-SUITE"; CONSERVA_WORKTREE=1; huella_deriva "PARO-SUITE" "$rc"; exit "$rc"; }
paso_obligatorio "UNIVERSO" deriva_universo || { rc=$?; FASE="PARO-UNIVERSO"; CONSERVA_WORKTREE=1; huella_deriva "PARO-UNIVERSO" "$rc"; exit "$rc"; }
paso_obligatorio "TABLERO" deriva_tablero || { rc=$?; FASE="PARO-TABLERO"; CONSERVA_WORKTREE=1; huella_deriva "PARO-TABLERO" "$rc"; exit "$rc"; }
paso_obligatorio "REGISTRO" deriva_registro || { rc=$?; FASE="PARO-REGISTRO"; CONSERVA_WORKTREE=1; huella_deriva "PARO-REGISTRO" "$rc"; exit "$rc"; }

transicion "PUBLICACION"
set +e; publica_cambios; rc=$?; set -e
if [ "$rc" -ne 0 ]; then
  FASE="PARO-PUBLICACION"; CONSERVA_WORKTREE=1; huella_deriva "PARO-PUBLICACION" "$rc"; exit "$rc"
fi
FASE="FIN"
marca_exitosa
huella_deriva "$RESULTADO_PUBLICACION" 0
log "RESULTADO: ${RESULTADO_PUBLICACION}."
