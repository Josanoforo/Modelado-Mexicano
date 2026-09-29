#!/bin/sh
# Uso: lanza-vc1.sh <cwd> <archivo-prompt> <max-turns>
# Receta de catalogo-1-lote3/lanzamiento/lanza-aislado.sh con settings en /home/pc0/vyc27-rec:
# claude -p nuevo en namespace de montaje propio con /tmp tmpfs vacío, herramientas cerradas,
# sin memoria ni settings de usuario/proyecto, sandbox de Bash sin red ni lecturas fuera del cwd.
set -eu
CWD="$1"; PROMPT_FILE="$2"; TURNS="$3"
SETTINGS=/home/pc0/vyc27-rec/settings-reconstructor.json
exec unshare --user --map-root-user --mount -- sh -c "mount -t tmpfs tmpfs /tmp && exec unshare --user --map-user=1000 --map-group=1000 -- sh -c 'cd \"$CWD\" && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude -p \"\$(cat \"$PROMPT_FILE\")\" --model claude-opus-5-5 --restricted --settings $SETTINGS --tools Bash,Read,Write,Edit,Glob,Grep --allowedTools Bash,Read,Write,Edit,Glob,Grep --permission-mode acceptEdits --permission-prompts none --strict-mcp-config --output-format stream-json --verbose --max-turns $TURNS < /dev/null'"
