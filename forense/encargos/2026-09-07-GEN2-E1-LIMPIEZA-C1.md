# ACTO GEN2-E1 · LIMPIEZA-C1 — inventario de árboles, ramas y raíces (solo lectura)

Archivado verbatim por A.3 (0-bis). Texto tal como llegó de mesa, 7/sep/2026.

---

Cabecera: UBUNTU (caja) · Sonnet · COMPUERTA: ninguna. NO se lanza en NUBE: el terreno que inventaría es la máquina local. Firmas: mesa 7/sep «quiero un plan de limpieza de worktrees o cualquier rama o branch que pueda quedar volando localmente, no me gustaría que se jalara info o data de otros trabajos en la máquina local». Qué hace, sin ninguna acción de borrado:

Clones: find "$HOME" -maxdepth 4 -type d -name .git 2>/dev/null (declara $HOME, profundidad, directorios examinados). Por clon: git worktree list --porcelain; por árbol: ruta · rama · HEAD · git merge-base HEAD origin/main y cuántos commits atrás · git status --porcelain | wc -l · git log --branches --not --remotes --oneline | wc -l (commits no empujados) · data/raw: symlink (a dónde) o directorio real (tamaño, n archivos).
Raíces: data/raices.local.yaml de cada clon (raíces lógicas y si están configuradas; no pegar rutas físicas en la nota, solo raiz_logica · configurada · sha256 del archivo de config). Por cada raíz real: python3 tools/barrido_descargas_vs_manifiesto.py → presentes-no-registrados (candidatos PR #77) y registrados-ausentes, con conteo.
Remoto: git ls-remote --heads origin; por rama: fusionada en main (git branch -r --merged origin/main) · PR abierto · trabajo vivo · PARO · sin utilidad aparente. Hoy se espera una: claude/encargo-maestra38-sello-3-6y5e0z (PARO).
Entregable: forense/notas/2026-09-07-GEN2-E1-limpieza-arboles.md con las tres tablas y la lista propuesta de poda para firma de mesa (E4), cada fila con su evidencia. Recibo RECIBO — no requiere firma; fila ABIERTA solo si aparece un payload no registrado o un commit no empujado (eso sí es decisión). Perímetro: forense/notas/ (1) · forense/firmas-pendientes.tsv · cascada. No borra, no mueve, no empuja nada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo. Contador: cero directo; nace arboles_fuera_de_politica con su primer valor medido.
