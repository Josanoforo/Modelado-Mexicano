#!/bin/sh
# Uso: lanza-aislado.sh <cwd> <archivo-prompt> <max-turns>
# Lanza una sesión nueva de Claude Code (claude -p) en un namespace de montaje propio con /tmp vacío (tmpfs),
# herramientas cerradas, sin memoria, sin settings de usuario/proyecto, sandbox de Bash sin red ni lecturas fuera del cwd.
set -eu
CWD="$1"; PROMPT_FILE="$2"; TURNS="$3"
SETTINGS=/home/pc0/c1-lote3-rec/settings-reconstructor.json
exec unshare --user --map-root-user --mount -- sh -c "mount -t tmpfs tmpfs /tmp && exec unshare --user --map-user=1000 --map-group=1000 -- sh -c 'cd \"$CWD\" && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p \"\$(cat \"$PROMPT_FILE\")\" --model claude-opus-5-5 --restricted --settings $SETTINGS --tools Bash,Read,Write,Edit,Glob,Grep --allowedTools Bash,Read,Write,Edit,Glob,Grep --permission-mode acceptEdits --permission-prompts none --strict-mcp-config --output-format stream-json --verbose --max-turns $TURNS'"
