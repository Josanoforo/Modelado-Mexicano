# Nota de cierre · ACTO GEN2-CORPUS-RESPALDO-EJECUCION-1 · 23/sep/2026

Encargo archivado (A.3): `forense/encargos/2026-09-23-GEN2-CORPUS-RESPALDO-EJECUCION-1.md`, 0-bis `a30752e0`, sello de cuerpo `3aca4ca0…`, raíz de acto `a307`. Rama `acto/gen2-corpus-respaldo-ejecucion-1`, una sola sesión, Sonnet 5 (coincide con lo sugerido en la cabecera), sin sub-agentes, MODO ABIERTO, **COMPUERTA: ninguna** (el encargo no trae línea `GATED a…`/`COMPUERTA:`/`Estado: GATED a…` de merge; su §8 son compuertas internas de escritura/verificación, no de lanzamiento).

## 0 · ARRANQUE (salida cruda)

- 0.a `git fetch --prune` + `git rev-list --count HEAD..origin/main`: al abrir el clon base (`/home/pc0/Modelado-Mexicano`) → `129` (clon viejo, no se trabajó ahí). El worktree del acto se creó directo sobre `origin/main` (`73b7f115`, un commit por delante del `f28d1038` que el encargo declara como SHA de redacción — no es PARO, se reporta). Durante la sesión `origin/main` avanzó 4 commits más (`06fe7d19`, PR #1047 de `GEN2-DIN-CREDITO-CELDAS-D-1`); `git merge origin/main` limpio, sin conflictos, sobre el 0-bis ya commiteado.
- 0.b `git status --porcelain` vacío antes del 0-bis.
- 0.c duplicado: `git ls-remote --heads origin | grep -i corpus-respaldo-ejecucion` → nada; `git worktree list | grep -i respaldo-ejecucion` → nada; `gh pr list --search "corpus-respaldo-ejecucion" --state open` → nada. Rótulo libre.
- 0.d `python3 tools/limpia_arbol.py --reporta`: 54 worktrees vivos, 51 ramas locales del clon base ya fusionadas y vivas (ajeno, sólo reporte), base 129 commits atrás en el clon viejo (no en el worktree del acto).
- `data/raw` → ausente en el worktree nuevo (esperado, A.3 del skill: no es PARO); enlazada a `/home/pc0/mm-corpus/raw`. `data/raices.local.yaml` copiada del worktree hermano `mm-corpus-integridad-1` (`data_raw`/`descargas_mx`, mismas rutas).
- `python3 tools/entorno.py` (commit `73b7f115`, antes del merge):
  ```
  ENTORNO · commit=73b7f115b2e9 · git_status=LIMPIO(0) · python=3.14.4 · numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3 pyreadstat=1.3.6 · CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable CHECK_SELFCHECK_CHILD=sin_variable MODELADO_RAICES=sin_variable PYTHONHASHSEED=sin_variable TZ=sin_variable · red=no-ejecutada · raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=438)
  ```
  `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable` + corpus montado (438 archivos de primer nivel examinados) = **CAJA**, lo que el encargo exige (§ENTORNO de la cabecera: «si dice NUBE, PARA» — no aplicó).

## 1 · Premisas del encargo, verificadas antes de tocar nada (§2 EJECUCIÓN de la skill)

| premisa (§3 del encargo) | rótulo | resultado |
|---|---|---|
| FP `…3d56-01` ABIERTA desde 21/sep, pide destino del respaldo | `[LEÍDO]` | **Confirmada**, re-verificada contra `origin/main` fresco (no heredada): `awk` sobre `forense/firmas-pendientes.tsv` → sigue `ABIERTA`, texto verbatim intacto: «El 21/sep mesa contestó "Sin destino por ahora". El juego verificado (1914 archivos, 19.8 GB, índice+SHA256SUMS+restauración VERDE) está en `/home/pc0/mm-respaldo-corpus/2026-09-21/` en el MISMO disco que el corpus y por eso todavía no es un respaldo.» |
| `INSTRUCCION-RESPALDO.md` existe con los cuatro comandos | `[EXISTE]` | Confirmada: `forense/analisis/corpus-integridad-1/INSTRUCCION-RESPALDO.md` en el árbol |
| mesa reportó 23/sep: disco existe, hay que reformatearlo, listo esta semana, vence 27/sep; el acto arranca cuando mesa diga «montado en `<ruta>`» | `[REPORTADO]` | **Verificada por objeto, no heredada**: `ls -la /mnt/` (fuera de sandbox — [[feedback_sandbox_mnt_c_vista_dual]]) → sólo `c`, `d`, `e`, los tres discos internos de Windows ya conocidos (`df -h`: 931G/3.7T/931G, ninguno recién formateado ni con espacio libre sospechosamente vacío). Ningún disco externo nuevo montado. La firma D5 (§2 del encargo, verbatim de mesa 23/sep) es consistente con esto: «Ya tengo un disco duro, necesito reformatearlo … no ahora, esta semana sí; vence el domingo» |
| «Ya hecho»: `ls data/ | grep -i RESPALDO-VERIFICACION` → 0; FP `…3d56-01` ABIERTA | §4 | Repetida por objeto en este worktree: mismo resultado, 0 archivos `RESPALDO-VERIFICACION-*` en `data/`, FP sigue `ABIERTA` |

## 2 · Determinación: EN-ESPERA, no PARO (§7-f del encargo)

El encargo declara explícitamente, como excepción a su propia lista cerrada de PAROS: **«f) el disco no está montado al abrir → no es PARO: EN-ESPERA con fecha, y se reporta.»** Es exactamente la premisa `[REPORTADO]` verificada arriba: el destino que las cuatro piezas (P1-P4) necesitan para escribir no existe todavía. Bajo §2 EJECUCIÓN de la skill (`instrucciones-proyecto-v2_16.md` §2, «cuando toca logística o estado del repo y el objetivo sigue alcanzable, el ejecutor replantea, sigue y lo declara»): el objetivo sigue siendo alcanzable — sólo que no hoy, no por esta sesión, y con fecha (27/sep/2026, D5). No hay rama prevista distinta a "esperar" en el propio encargo para este caso, y §6 LATITUD no ofrece una alternativa de destino (el encargo pide explícitamente `--destino <ruta del disco>`, no un directorio provisional). **Cero commits de P1-P4.**

## 3 · Dato de contexto para el sucesor, no ejecutado por este acto

Ya existe una copia STAGING completa y verificada en `/home/pc0/mm-respaldo-corpus/2026-09-21/` (producida por `ACTO GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1`, `PR #974`, ver su nota `forense/notas/2026-09-21-GEN2-CORPUS-INTEGRIDAD-Y-RESPALDO-1-cierre.md` §5): 1914 archivos, 19 817 841 648 B (19.8 GB), índice + `SHA256SUMS` + restauración completa ya probada VERDE. Está en el **mismo disco físico** que el corpus (`/dev/sdd`, según esa nota), por lo que no cuenta como respaldo — pero cuando mesa nombre el destino, el sucesor podría copiar/verificar este staging ya hecho contra `data/manifiesto.yaml` en vez de re-correr `INSTRUCCION-RESPALDO.md` desde el corpus vivo. **No se decide aquí**: el encargo pide los cuatro comandos originales con `--destino`; esto queda declarado como opción para quien retome, no como atajo ya tomado.

## 4 · Cascada

Conteo de ADR vía receta de raíz de acto (D-24): este `ADR` no mueve el espacio numérico cerrado (sigue en `593`). Fragmento L0: `canon/L0/ADR-260923-GEN2-CORPUS-RESPALDO-EJECUCION-1-a307-01.md`. Rótulo `GEN2-CORPUS-RESPALDO-EJECUCION-1` censado en `canon/registro-rotulos.tsv`. `CONTADOR` (cabecera del encargo): cero mediciones, cero corridas, no adopta — cumplido, ningún contador del programa se tocó. **Suite:** `python3 tests/check.py --rapido` → VERDE, 0 FAIL (salida completa en el commit de cierre).

**No tocado:** `data/manifiesto.yaml`, cualquier raíz del corpus, el disco destino (no existe), la FP `…3d56-01` (sigue `ABIERTA`: nadie firmó nada), el candado del agente de adquisición.
