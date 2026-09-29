#!/bin/bash
# Ciclo E.2 por paquete: archiva y commitea la salida ANTES de abrir el sellado; luego compara y commitea.
set -euo pipefail
cd /home/pc0/mm-gen2-validacion-y-2027-1
V=forense/validacion-independiente/validacion-continua-1; REC=/home/pc0/vyc27-rec; B=acto/GEN2-VALIDACION-Y-2027-1
python3 $V/archiva.py $REC "$@"
git add $V && git commit -qm "GEN2-VALIDACION-Y-2027-1 · P1: salida archivada antes de abrir sellados (E.2): $*

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q origin $B
python3 $V/compara_vc1.py $REC "$@"
git add $V && git commit -qm "GEN2-VALIDACION-Y-2027-1 · P1: auditoría y comparación: $*

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q origin $B
python3 $V/asienta.py "$@"
