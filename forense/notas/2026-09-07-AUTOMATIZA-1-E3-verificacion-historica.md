# ACTO AUTOMATIZA-1-E3 · CIERRE-MECANICO — verificación histórica del dry-run

Registro único (manual, no en CI) exigido por el encargo: `tools/cierre_acto.py`
debe proponer el candidato ADR correcto tanto en la base previa a `ADR-355`
como en el árbol actual.

## Corrección de cita contra el árbol

El encargo cita "la base previa a `ADR-355` (padre de `#559`: `3fb0b8a`)".
Verificado contra el árbol real: `3fb0b8a` es la rama de origen fusionada
por `#559` (`693ea23`, `git log -1 --format="%H %P" 693ea23` →
`693ea23... a2c3138... 3fb0b8a...`), no el estado de `main` antes de
fusionar — `3fb0b8a` **ya trae** `**ADR-355` en `canon/gobernanza-v1_15.md`
(confirmado: `git show 3fb0b8a:canon/gobernanza-v1_15.md | grep -oE
'^\*\*ADR-[0-9]+' | tail -1` → `355`). El primer padre del merge,
`a2c3138` (`"Merge pull request #562 from Josanoforo/acto/maestra38-cron-3"`,
main antes de que `#559` entrara), es el que de verdad tiene máximo `354` —
ésa es la base previa a `ADR-355` que el encargo pedía verificar. Corregido
aquí, sin PARO: el propósito de la verificación (que el tool derive
correctamente `real+1` contra un árbol histórico) se cumple igual contra
el commit correcto.

## Corrida 1 — base previa a `ADR-355` (`a2c3138`)

```
$ git worktree add --detach <tmp> a2c31389b0b2f7b59ecd35a7ab7851d377b232c1
$ cp tools/estado_comun.py tools/cierre_acto.py <tmp>/tools/   # el tool no existía en ese commit
$ cd <tmp> && python3 tools/cierre_acto.py --sin-suite
```

Salida (recorte relevante):
```
ADR
  Real (comando de la casa): 354
  Candidato: 355
```

Correcto: propone `355`, igual que el ADR que `#559` efectivamente añadió.

## Corrida 2 — árbol actual (candidato real de `AUTOMATIZA-1-E3`)

```
$ python3 tools/cierre_acto.py --sin-suite
```

Salida (recorte relevante):
```
ADR
  Real (comando de la casa): 365
  Candidato: 366
```

`366` es el siguiente real tras `ADR-365` (`ACTO AUTOMATIZA-1-E2`, PR #569,
fusionado en `4dfb4a5`) — el candidato que este mismo acto (`AUTOMATIZA-1-E3`)
usará al cerrar.

Worktree eliminado tras la verificación (`git worktree remove --force`).

## Diff de `.claude/commands/acto.md` (integración mínima, sólo §4 CIERRE, pasos 1 y 3)

```diff
1. **ADR re-derivado por el comando de la casa** — nunca heredado de
-   prosa ni de lo que "hoy daría":
+   prosa ni de lo que "hoy daría". Preflight mecánico (ACTO
+   AUTOMATIZA-1-E3, 7/sep/2026): `python3 tools/cierre_acto.py` (Fase A,
+   dry-run, nunca escribe) reporta el máximo ADR real y el candidato
+   contiguo (equivalente a
   `grep -oE '^\*\*ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1`
-   → candidato = máximo + 1, contiguo (sin huecos). Declara si hay otro
-   acto en vuelo conocido que pueda tomar el mismo número primero — regla
-   de la casa, renumera quien fusiona segundo.
+   → candidato = máximo + 1), si el candidato ya aparece redactado en
+   alguna rama remota accesible (sin afirmar "PR abierto" sin evidencia),
+   FP máximo/filas abiertas, los conteos de `gobernanza`/L0 contra el
+   real, el rótulo esperado y si ya está en `registro-rotulos.tsv`, y
+   corre `tests/check.py --baseline`. Declara si hay otro acto en vuelo
+   conocido que pueda tomar el mismo número primero — regla de la casa,
+   renumera quien fusiona segundo.
2. **Cabecera.** Entrada nueva en `canon/gobernanza-v1_15.md` §4
   (Registro de decisiones), con el encargo citado (archivado por A.3,
-   SHA de redacción) y, si aplica, el bloque **Gate verificado**.
+   SHA de redacción) y, si aplica, el bloque **Gate verificado**. Esto lo
+   redacta el ejecutor — el tool no entiende semántica de ADR.
3. **Recifrado L0.** La ÚNICA FUENTE DE ESTADO vigente
   (`canon/estado-programa-v1_12.md`; `v1_11` retirada del árbol por `T01`,
-   ver `ADR-339`): el conteo de ADR
-   de la línea `L0` sube (N → N+1), con la anotación nueva insertada
-   antes de la anterior — nunca reescribiendo la que ya estaba. Cabecera
-   de conteo de `gobernanza` (`**N ADR**`, línea 2) recifrada igual.
+   ver `ADR-339`): la anotación nueva se inserta a mano en la línea `L0`,
+   antes de la anterior — nunca reescribiendo la que ya estaba (es
+   semántica, el tool no la escribe). Hecho esto, los dos contadores
+   puramente mecánicos — el conteo de ADR de la propia línea `L0` y la
+   cabecera de conteo de `gobernanza` (`**N ADR**`, línea 2) — se
+   reconcilian con `python3 tools/cierre_acto.py --aplica`: todo-o-nada
+   (aborta con `APLICACION_ABORTADA · 0 archivos escritos` si alguna
+   ancla no es única, nunca reescribe a mano ni a medias), idempotente
+   (una segunda corrida sin cambios en el árbol reporta `sin cambios`).
```

Los nueve conceptos de la cascada se conservan (misma numeración 1-9); sólo
los pasos 1 y 3 cambian, para citar el tool en vez del comando manual/la
reconciliación a mano de los dos contadores. Los pasos 2, 4, 5, 6, 7, 8, 9
quedan intactos -- son juicio humano, no derivación mecánica.
