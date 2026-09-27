#!/bin/sh
set -eu
cd "$(dirname "$0")"
export LD_LIBRARY_PATH="/usr/lib/x86_64-linux-gnu/blas:/usr/lib/x86_64-linux-gnu/lapack${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
exec python3 reconstruir.py
