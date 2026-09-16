## HISTÓRICO — ARCHIVADO DESDE COLA (CONSUMIDO)
Movido de `forense/encargos/cola/` a `forense/encargos/` por `ACTO GEN2-MANTENIMIENTO-3` (2026-09-16), `NC-0248`/`NC-0249`: uno de los 18 `LANZADO-COMO` que `ACTO GEN2-VIGENCIA-DEUDA-1` confirmó ya ejecutados y fusionados (PR #602, según la propia cabecera/`## CONSUMIDO` de este archivo, verificado sin homónimo archivado en `forense/encargos/` fuera de `cola/` antes de este movimiento) pero cuya copia de cola era el único registro -- patrón A.14, mismo criterio que `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md` (el CADUCO que `GEN2-VIGENCIA-DEUDA-1` ya movió). A diferencia de ese caso, este SÍ se ejecutó: el movimiento es de ubicación (cola -> archivo), no una reclasificación de estado. Cuerpo verbatim y cabecera existentes se conservan sin editar debajo (A.3).

ESTADO: CONSUMIDO — PR #602 (`acto/gen2-e1-limpieza-c1`). Sincronizado por `ACTO GEN2-E7` pieza D (D2a): seguía `LISTO-CAJA` con el PR ya fusionado.
ENTORNO: CAJA (UBUNTU)
ENCOLADO: 2026-09-07 · ACTO GEN2-E0 · ENCOLA, skill `/encola`, PR [COLA]. Gesto de encolado: precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026).
BITACORA:
- 2026-09-07 · LISTO-CAJA · encolado por PR [COLA] encola GEN2 (plan + GEN2-E1…GEN2-E6). COMPUERTA propia: ninguna. `/despacha` NO lo ejecuta (es de caja, no de nube): lo nombra y lo deja para una sesión de CAJA. Solo lectura: no borra, no mueve, no empuja.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E1 · ACTO GEN2-E1 · LIMPIEZA-C1 — inventario de árboles, ramas y raíces (solo lectura)

Cabecera: **UBUNTU (caja)** · **Sonnet** · COMPUERTA: ninguna. NO se lanza en NUBE: el terreno que inventaría es la máquina local.
Firmas: mesa 7/sep «quiero un plan de limpieza de worktrees o cualquier rama o branch que pueda quedar volando localmente, no me gustaría que se jalara info o data de otros trabajos en la máquina local».
Qué hace, sin ninguna acción de borrado:
1. Clones: `find "$HOME" -maxdepth 4 -type d -name .git 2>/dev/null` (declara `$HOME`, profundidad, directorios examinados). Por clon: `git worktree list --porcelain`; por árbol: ruta · rama · `HEAD` · `git merge-base HEAD origin/main` y cuántos commits atrás · `git status --porcelain | wc -l` · `git log --branches --not --remotes --oneline | wc -l` (commits no empujados) · `data/raw`: symlink (a dónde) o directorio real (tamaño, n archivos).
2. Raíces: `data/raices.local.yaml` de cada clon (raíces lógicas y si están configuradas; **no pegar rutas físicas en la nota**, solo `raiz_logica · configurada · sha256 del archivo de config`). Por cada raíz real: `python3 tools/barrido_descargas_vs_manifiesto.py` → presentes-no-registrados (candidatos PR #77) y registrados-ausentes, con conteo.
3. Remoto: `git ls-remote --heads origin`; por rama: fusionada en `main` (`git branch -r --merged origin/main`) · PR abierto · trabajo vivo · PARO · sin utilidad aparente. Hoy se espera una: `claude/encargo-maestra38-sello-3-6y5e0z` (PARO).
4. Entregable: `forense/notas/2026-09-07-GEN2-E1-limpieza-arboles.md` con las tres tablas y la **lista propuesta de poda** para firma de mesa (E4), cada fila con su evidencia. Recibo `RECIBO — no requiere firma`; fila `ABIERTA` solo si aparece un payload no registrado o un commit no empujado (eso sí es decisión).
Perímetro: `forense/notas/` (1) · `forense/firmas-pendientes.tsv` · cascada. **No borra, no mueve, no empuja nada.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: cero directo; nace `arboles_fuera_de_politica` con su primer valor medido.
