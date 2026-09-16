## HISTÓRICO — ARCHIVADO DESDE COLA (CONSUMIDO)
Movido de `forense/encargos/cola/` a `forense/encargos/` por `ACTO GEN2-MANTENIMIENTO-3` (2026-09-16), `NC-0248`/`NC-0249`: uno de los 18 `LANZADO-COMO` que `ACTO GEN2-VIGENCIA-DEUDA-1` confirmó ya ejecutados y fusionados (PR #604, según la propia cabecera/`## CONSUMIDO` de este archivo, verificado sin homónimo archivado en `forense/encargos/` fuera de `cola/` antes de este movimiento) pero cuya copia de cola era el único registro -- patrón A.14, mismo criterio que `2026-09-02-MAESTRA35-L10-OLA6-SALUD-L1.md` (el CADUCO que `GEN2-VIGENCIA-DEUDA-1` ya movió). A diferencia de ese caso, este SÍ se ejecutó: el movimiento es de ubicación (cola -> archivo), no una reclasificación de estado. Cuerpo verbatim y cabecera existentes se conservan sin editar debajo (A.3).

ESTADO: CONSUMIDO — PR #604 (`acto/gen2-e4-limpieza-c2-poda`). Sincronizado por `ACTO GEN2-E7` pieza D (D2a): seguía `GATEADO` con el PR ya fusionado.
ENTORNO: CAJA (UBUNTU)
ENCOLADO: 2026-09-07 · ACTO GEN2-E0 · ENCOLA, skill `/encola`, PR [COLA]. Gesto de encolado: precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026).
BITACORA:
- 2026-09-07 · GATEADO · encolado por PR [COLA] encola GEN2 (plan + GEN2-E1…GEN2-E6). COMPUERTA propia: GEN2-E1 fusionado Y la lista de poda de su nota FIRMADA por mesa (fila FIRMADA en el tablero, o el merge de un PR que la marque). `/despacha` NO lo ejecuta (es de caja). Si falta cualquiera, cero commits.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

## E4 · ACTO GEN2-E4 · LIMPIEZA-C2 PODA — con la lista firmada de E1

Cabecera: **UBUNTU (caja)** · **Sonnet** · COMPUERTA: E1 fusionado **y** la lista de poda de su nota lleva la firma de mesa (fila FIRMADA en el tablero, o el merge de un PR que la marque). NO se lanza en NUBE.
Qué hace, solo lo que la lista firmada diga y en este orden: (1) ramas remotas fusionadas/consumidas/PARO → `git push origin --delete` (hoy `sello-3-6y5e0z`); (2) ramas locales fusionadas → `git branch -d`; con commits únicos → **empujar o reportar, nunca borrar**; (3) worktrees de actos CONSUMIDO → antes: `git status`, commits únicos, `barrido_descargas_vs_manifiesto.py` sobre su `data/raw` si es real; lo no registrado se mueve al corpus compartido y se registra en el manifiesto **antes** de `git worktree remove` + `prune`; (4) clones extra con 0 commits únicos, 0 payloads únicos, 0 trabajo útil → borrar; (5) en GitHub: activar *Automatically delete head branches* (mesa lo hace; el acto lo verifica en una rama de prueba). Salida cruda de cada comando en la nota; `limpia_arbol.py --reporta` antes y después, pegado.
Perímetro: sistema de archivos local y remoto según la lista; en el repo solo `forense/notas/` (1), manifiesto **solo si aparece un payload huérfano** (append), tablero, cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: `arboles_fuera_de_politica → 0`; `ramas_consumidas_vivas → 0`. Lo que NO hace: C-4 íntegro.
