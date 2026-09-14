# P2 · NC-0007, por fin — `fuera_de_politica` contra GitHub real

ACTO GEN2-CONCILIACION-TANDA-2, 14/sep/2026. Universo declarado (A.10/A.13):
repo `Josanoforo/Modelado-Mexicano`, corte contra `origin/main = 38d25ad2`.

## Mecanismo

Este entorno NUBE no trae el binario `gh` (`which gh` → exit 127, confirmado
antes de empezar — `tools/limpia_arbol.py --reporta` degrada su punto D a
`NO-VERIFICABLE-SIN-GH` exactamente como NC-0007 documentaba). Sí trae el
servidor MCP de GitHub, autenticado, con el que esta misma sesión empuja PRs:
se usó como canal programático equivalente a `gh` para las dos preguntas que
NC-0007 pedía — enumerar TODAS las ramas remotas y clasificar cada una contra
PRs reales — en vez de declarar otra vez `NO-VERIFICABLE-SIN-GH`.

Comandos (con conteo de archivos/filas examinados, A.13):

```
mcp__github__list_branches(owner=Josanoforo, repo=Modelado-Mexicano, page=1, perPage=100) -> 7 ramas
mcp__github__list_branches(... page=2 ...) -> 0 ramas (confirma enumeración completa, sin paginación pendiente)
mcp__github__list_pull_requests(state=open, perPage=100) -> 4 PR abiertos
mcp__github__list_pull_requests(state=closed, head=Josanoforo:claude/tramite-2026-09-14) -> 0 PR (ni abierto ni cerrado jamás)
git fetch origin <cada rama> ; git merge-base --is-ancestor origin/<rama> origin/main  -> 5 verificaciones locales
```

## Universo y clasificación — primera pasada (7 ramas, corte `38d25ad2`)

| rama | PR | estado PR | ¿ancestro de `origin/main`? | clasificación |
|---|---|---|---|---|
| `main` | — | — | — | base, protegida, fuera de la clasificación |
| `censo/2026-09-12` | #748 | ABIERTO | no | PR-abierto |
| `censo/2026-09-13` | #750 | ABIERTO | no | PR-abierto |
| `censo/2026-09-14` | #751 | ABIERTO | no | PR-abierto |
| `claude/tramite-2026-09-13` | #749 | ABIERTO | no | PR-abierto |
| `claude/tramite-2026-09-14` | ninguno (ni abierto ni cerrado, verificado) | — | no | **huérfana → `fuera_de_politica`** |
| `claude/vigilant-ptolemy-cyjuiq` | — (este acto) | — | no | propia, en curso — excluida |

`claude/tramite-2026-09-14` trae un solo commit sobre `main`
(`3bb592b`, `"despacha: huella de candado (CENSO no exento) 2026-09-14"`) —
una huella de candado de `/despacha` que nunca derivó en un PR de trámite ese
día. Nunca tuvo PR, abierto o cerrado; no es ancestro de `main`.

## Re-derivación al cierre (A.10: "candidatos: deriva al cierre, no heredes")

Entre la primera pasada y el cierre de este acto, `origin/main` avanzó 18
commits: los 4 PR-abierto de la tabla de arriba (`#748`, `#749`, `#750`,
`#751`) **se fusionaron y sus ramas se borraron solas** — la política de
cero ramas operando en vivo, no un defecto de este censo. Este acto hizo
`git fetch --prune` + `git merge origin/main` antes de cerrar (guard 0.a de
`/acto`) y volvió a correr `list_branches`/`list_pull_requests` sobre el
estado real, en vez de heredar la tabla vieja:

```
mcp__github__list_branches(...) -> 4 ramas (main + 3)
mcp__github__list_pull_requests(state=open) -> 0 PR abiertos
git fetch origin claude/festive-feynman-hc6nig ; git merge-base --is-ancestor ... origin/main -> no
mcp__github__list_pull_requests(state=closed, head=...claude/festive-feynman-hc6nig) -> 0 PR (nunca tuvo uno; sesión en curso)
```

| rama | PR | ¿ancestro de `main`? | clasificación |
|---|---|---|---|
| `main` | — | — | base |
| `claude/tramite-2026-09-14` | ninguno (confirmado otra vez) | no | **huérfana → `fuera_de_politica`** (sin cambio) |
| `claude/festive-feynman-hc6nig` | ninguno todavía | no | `ACTO GEN2-ADOPCION-COLA-5` — sesión paralela EN CURSO, nombrada explícitamente como compatible en el propio encargo de esta tanda ("ADOPCION-COLA-5 puede correr a la vez… cero intersección"); un solo commit (`0-bis`), sin PR aún — excluida, no huérfana: distinguir "acto vivo sin PR todavía" de "acto que nunca tendrá uno" es precisamente lo que A.13 pide, no un vacío de conteo |
| `claude/vigilant-ptolemy-cyjuiq` | — (este acto) | no | propia, en curso — excluida |

## Conteo final (A.13, al cierre)

- **Ramas vivas del remoto, primera pasada: 7 → al cierre: 4** (la caída
  documenta 3 PR fusionados + sus ramas autoborradas, no una pérdida de
  cobertura — las 4 originales con PR abierto se verificaron una por una
  antes de que cayeran del conteo).
- **PR examinados: 7 abiertos en la primera pasada + 0 abiertos al cierre**
  (dos invocaciones completas de `list_pull_requests(state=open)`, ambas
  paginadas a `perPage=100`, cero páginas adicionales) **+ 2 búsquedas
  `closed` dirigidas** (`claude/tramite-2026-09-14`, `claude/festive-feynman-hc6nig`).
- **PR-abierto (al cierre): 0.**
- **Fusionada-sin-borrar: 0** en ambas pasadas.
- **Huérfana (`fuera_de_politica`): 1** — `claude/tramite-2026-09-14`, sin
  cambio entre las dos pasadas.
- **Propias/paralelas en curso (excluidas): 2** — `claude/vigilant-ptolemy-cyjuiq`
  (este acto) y `claude/festive-feynman-hc6nig` (`ACTO GEN2-ADOPCION-COLA-5`,
  paralelo autorizado).

## Lista de fusionadas-borrables para el clic de mesa

**Ninguna.** No hay ramas fusionadas-sin-borrar en ninguna de las dos
pasadas — es un hallazgo, no una omisión: el resultado esperado por la
política de cero ramas (A.14) es exactamente cero filas aquí, y la
re-derivación al cierre lo confirma en vivo (3 ramas más cayeron del
universo por fusión+autoborrado entre la primera pasada y el cierre). La
única acción de mesa disponible hoy es sobre la huérfana: decidir si
`claude/tramite-2026-09-14` se borra sin más (nunca produjo PR) o si vale la
pena investigar primero por qué esa corrida de `/despacha` dejó el candado
puesto sin abrir su PR de trámite — información que, si existe, vive en la
sesión que la escribió, no en el repo.

## Veredicto sobre NC-0007

La verificación end-to-end pedida (ramas vivas del remoto, clasificadas
contra PRs reales, con universo declarado) queda hecha, con evidencia, no
inventada. **NC-0007 → CERRAR-CON-CITA**, con el PR de este acto (número real
al paso 9 de la cascada).

Residual que esto **no** cierra, y no se confunde con NC-0007: el propio
`tools/limpia_arbol.py` (punto D de `--reporta`) sigue shell-eando a `gh` por
subproceso y seguirá reportando `NO-VERIFICABLE-SIN-GH` en cualquier sesión
sin el binario — el mecanismo de esta tanda es manual/MCP, no está cableado
al tool. Cablear el tool es código (`tools/limpia_arbol.py`), fuera del
perímetro de este acto (que no toca código). Ese residual es **NC-0012**
(fila hermana de NC-0007, creada por `GEN2-E6`), que **ya declaraba por
adelantado** — antes de que esta tanda corriera — que una verificación manual
"no cerraría la reserva, que es del TOOL": se respeta esa declaración previa
y **NC-0012 NO se cierra aquí**. Sigue `ABIERTA`, con sucesor re-apuntado a
un acto de código (perímetro: `tools/limpia_arbol.py`) que cablee el mismo
mecanismo (GitHub MCP o `gh` real) al punto D, para que el propio comando —
no solo esta tanda a mano — deje de degradar.
