# ACTO W′ (addendum) · Inventario de clones, con universo declarado — 2026-08-13

## §0 · Universo declarado, antes de barrer (A.4)

Mecanismo: `find /home/pc0 -maxdepth 6 \( -name "*.git" -o -type d -name ".git" \) 2>/dev/null` (clones) + `find /home/pc0 -maxdepth 6 -name ".git" -type f 2>/dev/null` (worktrees, cuyo `.git` es archivo). Alcance: **solo `/home/pc0`, profundidad 6, 2026-08-13**. Terminó en 0.13s, sin error de permisos — no hubo NO OBTENIDO. **Este barrido no ve nada fuera de `/home/pc0`** — en particular no ve `/mnt/c/Users/PC0/` (donde vive `Descargas MX`, ya sabido) ni ningún otro punto de montaje. No se afirma "no hay más clones"; se afirma qué se examinó.

## §1 · Los 4 repositorios de Modelado-Mexicano encontrados, más 2 ajenos declarados y descartados

| # | ruta | tipo | HEAD/remoto | worktrees de su familia |
|---|---|---|---|---|
| 1 | `/home/pc0/Modelado-Mexicano` | clon de trabajo | `main`, `origin`=GitHub real | 28 (1 principal + 27 enlazados) |
| 2 | `/home/pc0/proyectos/Modelado-Mexicano` | clon de trabajo | `main`, `origin`=GitHub real | 9 (1 principal + 8 enlazados) |
| 3 | `/home/pc0/BACKUP-mm-mirror-2026-08-10.git` | **repo bare** (`git rev-parse --is-bare-repository` → `true`) | sin worktrees propios verificados en este acto (fuera de perímetro de escritura; no se le corrió `git worktree list`) | — |
| 4 | `/home/pc0/mm-purga.git` | **repo bare** (`is-bare-repository` → `true`) | ídem | — |

Ajenos a Modelado-Mexicano, vistos por el mismo barrido y descartados por contenido, no por nombre: `/home/pc0/.codex-app/.tmp/plugins/.git` y `/home/pc0/.codex/.tmp/plugins/.git` — cachés de plugins de otra herramienta, no tocados, no investigados más allá de confirmar que no son este proyecto.

**Los repos #3 y #4 no se investigaron a fondo** (perímetro de este acto: lectura de filesystem, no auditoría de contenido de cada repo bare) — se declaran encontrados y sin examinar en detalle, no se afirma qué contienen.

## §2 · Ficha por clon de trabajo (PASO 2)

| clon | HEAD | commit más reciente | worktrees | commits sin empujar a ningún remote |
|---|---|---|---|---|
| `/home/pc0/Modelado-Mexicano` | `302ac5a` (rama `sesion/cal-conf-faseb-pos4-envipe-paso1`) | 2026-08-03 22:08:31 -0600 (la propia HEAD; el resto de la familia tiene commits mucho más recientes, ver ACTO W) | 28 | **596** (repartidas en las ~19 ramas `wt-*`/`sesion/*` ya inventariadas y dejadas intactas por ACTO W — no se recuentan aquí una por una, ver `forense/notas/2026-08-13-w-limpieza-worktrees.md` §4) |
| `/home/pc0/proyectos/Modelado-Mexicano` | `f542c93` (rama `main`, 2026-08-06 18:22:52 -0600 — **una semana atrás de `origin/main` real**) | ver tabla de abajo | 9 | 4 según `--not --remotes=origin` cruda, **pero esa cifra es engañosa** — ver §3 |

**`git status --short` de ambos clones, en su propio directorio raíz (no un worktree enlazado):** clon 1 solo tiene `data/raw` y `data/secretos.local.yaml` sin trackear (higiene esperada). Clon 2 tiene `data/raw` y **un `descargas_mx` sin trackear en la raíz del propio clon** (no en un worktree) — no investigado más a fondo, fuera de perímetro; se declara, no se limpia.

## §3 · Preservación — el entregable real de este acto

`git log --oneline --all --not --remotes=origin` en el clon 2 dio solo 4 commits porque cachés locales de `origin/*` (ramas ya borradas en GitHub pero aún referenciadas localmente) ocultaban otros 2. **Verificado contra GitHub real** (`git ls-remote origin | grep -iE "mapa-ext|revalida|med-r3-4"` → vacío), los **6** tips distintos de la familia del clon 2 son, todos, ausentes de GitHub:

| worktree | rama local | commit | preservado en |
|---|---|---|---|
| `Modelado-Mexicano-mapa-ext-1` | `agent/mapa-ext-1` | `87ae19a` | `mapa-ext-1-huerfana-20260813` |
| `mm-mapa-ext-academico-20260806-182642` | `mapa-ext-academico-...` | `1524a44` | `mapa-ext-academico-huerfana-20260813` |
| `mm-mapa-ext-civil-20260806-182642` | `mapa-ext-civil-...` | `34a50b1` | `mapa-ext-civil-huerfana-20260813` |
| `mm-mapa-ext-integracion-20260806-184619` | `mapa-ext-integracion-...` | `0be9bb5` | `mapa-ext-integracion-huerfana-20260813` |
| `mm-mapa-ext-oficial-20260806-182642` | `mapa-ext-oficial-...` | `9c85f5e` | `mapa-ext-oficial-huerfana-20260813` |
| `mm-med-r3-4-...` / `mm-revalida-1-...` (mismo commit) | `codex/med-r3-4-...` / `revalida-1-...` | `bd0259c` | `med-r3-4-revalida-1-huerfana-20260813` |

Los 6 se empujaron a `origin` (`git push origin <sha>:refs/heads/<nombre>-huerfana-20260813`, sin rama de trabajo nueva, sin PR, sin merge — mismo mecanismo ya usado para `50344ac` → `acto-r2-issp-via-completa-huerfana`). **Ninguno se tocó, borró ni fusionó.** Adjudicar qué de esto es contenido real vale la pena rescatar (vs. ya superseded por trabajo equivalente que sí llegó a `origin/main` desde el clon 1 — los nombres `mapa-ext-*` coinciden con archivos que YA existen en `origin/main`, p. ej. `data/mapa-ext-academico-2026-08-06.tsv`, sugiriendo posible duplicado, no confirmado aquí) es de mesa.

`worktrees/mm-acto-r2prima-20260812-162554` (`50344ac`) ya estaba preservado desde el turno anterior de esta sesión — no se re-preserva, solo se confirma que sigue intacto.

## §4 · `Modelado-Mexicano-curador` — resuelto (PASO 4)

Pertenece a la familia del **clon 1** (`/home/pc0/Modelado-Mexicano/.git/worktrees/Modelado-Mexicano-curador`), no al clon 2. Sus 590 commits sin empujar (declarados por ACTO W, `ancestor_of_origin_main=NO`) son rescatables por cualquiera con acceso al clon base — no dependen del segundo clon ni de sus refs de preservación.

## §5 · La hipótesis de los cierres — evidencia real encontrada, corrige a ACTO W

**ACTO W usó `dmesg -T` (buffer del kernel, puede rotar) + `journalctl --since "24 hours ago" -p err` (filtro de prioridad `err`) y no encontró nada.** Este acto repitió la búsqueda con ventana de 48h y **sin filtro de prioridad** — y **sí hay evidencia real**:

```
$ journalctl --since "48 hours ago" --no-pager | grep -iE "oom|killed|segfault|terminat"
Aug 12 10:44:14 FF-5563 kernel: claude invoked oom-killer: ... Comm: claude ... PID 16639
Aug 12 10:44:14 FF-5563 kernel: Out of memory: Killed process 31510 (2.1.228) ... anon-rss:12816384kB
Aug 12 13:29:57 FF-5563 kernel: systemd invoked oom-killer: ... Comm: systemd
Aug 12 13:29:57 FF-5563 kernel: Out of memory: Killed process 31073 (2.1.228) ... anon-rss:14823168kB
Aug 12 13:32:21 FF-5563 kernel: (mismo proceso 31073/"2.1.228", segundo intento del OOM killer)
```

**Tres eventos reales de OOM-killer el 12/ago**, no cero. El primero (10:44:14) fue **invocado literalmente por un proceso llamado `claude`** (PID 16639) — la asignación de memoria que disparó la condición de OOM vino de un proceso Claude Code. La víctima en los tres casos fue un proceso distinto, `"2.1.228"` (nombre compatible con un binario versionado; no identificado con certeza en este acto — no hay proceso vivo con ese nombre ahora para inspeccionar, `ps aux` actual no lo muestra), con **12.8-14.8 GB de RSS residente** — una fracción enorme de los 15GB totales del sistema, consistente con causar inestabilidad real.

`dmesg -T` sigue sin mostrar nada (buffer del kernel ya rotado; confirma por qué ACTO W tampoco lo vio por esa vía). `/home/pc0/Modelado-Mexicano/.git/config.lock` sigue siendo el mismo nodo-dispositivo del sandbox de este agente ya identificado y retractado por ACTO W (mismo timestamp de creación, `2026-08-12 16:14:48`, sin cambio) — no es evidencia nueva. `/home/pc0/Modelado-Mexicano/.git/testfile.lock` es un archivo vacío, ordinario, fechado **2026-08-04** — debris viejo, no relacionado con los cierres del 12/ago.

**Correlación temporal, no causal-probada:** `git log --all --since="2026-08-12 10:00" --until="2026-08-12 14:00"` muestra actividad de commits casi continua en esa ventana (ACTO P·Lote-1, ACTO M-ADQ, E4c, merges de PR #183/#184, U1/E4b′) — un período de trabajo intenso, consistente con múltiples sesiones/actos corriendo o alternándose. **No se puede probar, con lo mirado en este acto, que dos sesiones distintas estuvieran ejecutando en el mismo segundo exacto del kill** — eso exigiría timestamps de inicio/fin de proceso que ya no existen para procesos terminados. Lo que sí se puede afirmar, con marca de tiempo y comando a la vista: **hay evidencia real de OOM el 12/ago, con un proceso `claude` como disparador de al menos uno de los tres eventos**, en una ventana de actividad de commits intensa — más que "sin evidencia" y menos que "concurrencia entre clones confirmada". Reportado con las tres palabras exactas que pedía el encargo: **evidencia de concurrencia/presión de memoria SÍ existe, con marcas de tiempo — atribución a sesiones específicas, NO EVALUABLE con lo disponible.**
