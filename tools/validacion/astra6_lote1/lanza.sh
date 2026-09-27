#!/usr/bin/env bash
# Sesión nueva por paquete. --prueba comprueba separación sin recalcular.
set -euo pipefail
modo=${1:?Uso: lanza.sh --prueba|--ejecuta carpeta-materializada}
carpeta=$(realpath "${2:?Falta carpeta-materializada}")
test "$modo" = --prueba || test "$modo" = --ejecuta
test -f "$carpeta/recibo-entrada.json"
test -d "$carpeta/entrada"
test -d "$carpeta/raw"
test ! -L "$carpeta/entrada"
test ! -L "$carpeta/raw"
# Guard: solo se monta una carpeta de trabajo nueva y las dos entradas.
mkdir -p "$carpeta/trabajo" "$carpeta/config-nueva"
args=(--unshare-user --unshare-pid --unshare-ipc --unshare-uts --die-with-parent
      --clearenv --setenv PATH /usr/bin:/bin --setenv HOME /config
      --setenv CODEX_HOME /config --setenv LANG C.UTF-8
      --setenv LD_LIBRARY_PATH /usr/lib/x86_64-linux-gnu/blas:/usr/lib/x86_64-linux-gnu/lapack
      --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib
      --ro-bind /lib64 /lib64 --proc /proc --dev /dev --tmpfs /tmp
      --ro-bind "$carpeta/entrada" /entrada --ro-bind "$carpeta/raw" /raw
      --bind "$carpeta/trabajo" /work --bind "$carpeta/config-nueva" /config
      --chdir /work)
guard='test ! -e /home && test ! -e /mnt && test ! -e /root && test ! -e /work/.git && test -r /entrada/manifiesto.json && test -d /raw'
if test "$modo" = --prueba; then
    bwrap "${args[@]}" /bin/sh -c "$guard && printf 'SEPARACION-EFECTIVA: solo /entrada /raw /work; sin clon, reservas ajenas ni historial.\n'"
    exit
fi
# Credenciales solamente; nunca config, historial, skills ni conversaciones.
codex_bin=$(readlink -f "$(command -v codex)")
auth_file=${CODEX_HOME:-"$HOME/.codex"}/auth.json
test -f "$auth_file"
test -z "$(find "$carpeta/config-nueva" -mindepth 1 -print -quit)"
args+=(--ro-bind "$(dirname "$codex_bin")/codex-code-mode-host" /codex-code-mode-host --ro-bind "$codex_bin" /codex --ro-bind "$auth_file" /config/auth.json
       --dir /etc --ro-bind /etc/resolv.conf /etc/resolv.conf
       --ro-bind /etc/ssl /etc/ssl)
# No resume: exec inicia una sesión sin historial; requiere acceso de API.
bwrap "${args[@]}" /bin/sh -c "$guard && exec /codex exec --ignore-user-config --ignore-rules --sandbox workspace-write --cd /work --skip-git-repo-check 'Lee /entrada/encargo.md. Recibiste solo /entrada y /raw. Conserva el SHA de /entrada/manifiesto.json en tu recibo. Implementa el método sin acceso a resultados esperados, congela código y números en un commit antes de revelación y termina. No solicites resultados al preparador durante la reconstrucción. En reconstruccion.tsv usa estado RECONSTRUIDO si hay números, NO-RECALCULABLE-DESDE-SPEC si el método o la identidad no basta, BLOQUEADO-POR-ACCESO si falta acceso, o NO-EVALUADO si no se intentó; incluye columna motivo para los estados sin cifras. No adivines ninguna asignación de identidad. No incluyas raw ni documentación PDF en el commit; conserva sus hashes y entradas. Git puede inicializarse en un subdirectorio de /work si la raíz está protegida.' </dev/null"
