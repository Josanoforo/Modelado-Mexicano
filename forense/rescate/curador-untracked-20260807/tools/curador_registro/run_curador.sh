#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO=""
MAPA=""
OUTPUT=""
SEED_DIR=""
EXPECTED_HEAD="a83f4575e5b370198256dcc5106dccf91094dc53"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo) REPO="$2"; shift 2 ;;
    --mapa) MAPA="$2"; shift 2 ;;
    --output) OUTPUT="$2"; shift 2 ;;
    --seed-dir) SEED_DIR="$2"; shift 2 ;;
    *) echo "Argumento desconocido: $1" >&2; exit 64 ;;
  esac
done

[[ -n "$REPO" && -n "$MAPA" && -n "$OUTPUT" ]] || {
  echo "Uso: bash tools/curador_registro/run_curador.sh --repo RUTA --mapa RUTA --output RUTA" >&2
  exit 64
}
REPO="$(cd "$REPO" && pwd)"
MAPA="$(cd "$MAPA" && pwd)"
mkdir -p "$OUTPUT"
OUTPUT="$(cd "$OUTPUT" && pwd)"

HEAD="$(git -C "$REPO" rev-parse HEAD)"
[[ "$HEAD" == "$EXPECTED_HEAD" ]] || {
  echo "HEAD no autoritativo: $HEAD (esperado $EXPECTED_HEAD)" >&2
  exit 65
}
python3 - "$MAPA/validacion.json" <<'PY'
import json,sys
v=json.load(open(sys.argv[1],encoding="utf-8"))
if not v.get("ok") or not v.get("head_matches_expected"):
    raise SystemExit("El mapa de entrada no está validado")
PY

RUN_TMP="$(mktemp -d /tmp/curador-registro.XXXXXX)"
trap 'rm -rf "$RUN_TMP"' EXIT INT TERM
PREVIOUS=""
if [[ -f "$OUTPUT/registro-demanda-universo-adjudicado.tsv" ]]; then
  PREVIOUS="$RUN_TMP/registro-anterior.tsv"
  cp "$OUTPUT/registro-demanda-universo-adjudicado.tsv" "$PREVIOUS"
fi

BRIDGE="$RUN_TMP/tabla-puente-aperturas.tsv"
python3 "$HERE/curador.py" --mapa "$MAPA" --build-bridge --output "$BRIDGE"
cp "$BRIDGE" "$OUTPUT/tabla-puente-aperturas.tsv"

for n in $(seq 1 33); do
  python3 "$HERE/curador.py" \
    --mapa "$MAPA" \
    --puente "$BRIDGE" \
    --necesidad "N$n" \
    --output "$RUN_TMP/N$n.jsonl"
done

SUPERVISOR_ARGS=(
  --repo "$REPO"
  --mapa "$MAPA"
  --worker-dir "$RUN_TMP"
  --puente "$BRIDGE"
  --output "$OUTPUT"
  --expected-head "$EXPECTED_HEAD"
  --prompt "$HERE/prompts/supervisor.md"
)
if [[ -n "$PREVIOUS" ]]; then
  SUPERVISOR_ARGS+=(--previous "$PREVIOUS")
fi
if [[ -n "$SEED_DIR" ]]; then
  SUPERVISOR_ARGS+=(
    --seed-registro "$SEED_DIR/registro-demanda-universo-adjudicado.tsv"
    --seed-rechazadas "$SEED_DIR/relaciones-rechazadas.tsv"
    --previous "$SEED_DIR/registro-demanda-universo-adjudicado.tsv"
  )
fi
python3 "$HERE/supervisor.py" "${SUPERVISOR_ARGS[@]}"

cat "$OUTPUT/validacion.json"
