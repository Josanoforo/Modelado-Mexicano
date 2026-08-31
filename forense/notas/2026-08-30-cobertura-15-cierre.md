# Nota de cierre · ACTO MAESTRA32-E10 · COBERTURA-15 — el acto no arranca: el GATE que su propio encargo declara está incumplido

Fecha de ejecución: 2026-08-31. Clon `/home/user/Modelado-Mexicano`, rama `claude/maestra32-e10-cobertura-0xqj0k` (ya existía localmente al lanzar la sesión; no se clonó ni se creó de nuevo). Esta nota sustituye a `forense/notas/2026-08-30-cobertura-15-spec.md` (COMMIT-1) y a `forense/prereg-duelo-v2/cobertura-15-v1_0.tsv` (COMMIT-2), que el encargo original preveía: ninguno de los dos se produce, porque el ARRANQUE del propio acto (antes de leer el resto del encargo, tal como el encargo mismo instruye) encontró que el GATE declarado en su primera línea — *"Estado: GATED a que `MAESTRA32-E9 · PROPAGA-2` fusione (mismo carril NUBE; E9 registra la firma D1=(i) que este acto ejecuta). Sin ranuras."* — está incumplido: `MAESTRA32-E9 · PROPAGA-2` no existe en ningún estado verificable del repositorio.

---

## Los cinco puntos del ARRANQUE

| # | Punto | Comando | Resultado |
|---|---|---|---|
| 1 | REPO | `pwd`; `git log -1 --format="%h %s"`; `git status` | `/home/user/Modelado-Mexicano` — clon ya existente, no se clonó ninguno nuevo. `1f455ea Merge pull request #395 from Josanoforo/claude/maestra32-e6-cloud-launch-8qu0hw`. `git status`: rama `claude/maestra32-e10-cobertura-0xqj0k`, sin cambios pendientes al arrancar. |
| 2 | SHA | `git fetch origin --prune`; `git log --oneline -1 origin/main` vs `HEAD` | `main` = `1f455ea`, exactamente el SHA que el encargo declara (`merge PR #395 / ADR-223`) — sin drift, no hace falta refrescar nada. `git fetch --prune` reporta además que la rama remota `origin/claude/maestra32-e10-cobertura-0xqj0k` fue borrada en algún momento anterior a esta sesión (`[deleted] (none) -> origin/...`) mientras la copia local sobrevivía; observación, no bloqueante — se restablece al primer `push -u` de este acto. |
| 3 | `data/raw` | `ls -la data/raw` | `No such file or directory` — ausente, esperado. No se crea ni se enlaza: el encargo mismo declara que este acto "lee tablas versionadas; no abre payloads; no mide nada", así que no hay ninguna operación en este cierre que la necesite. |
| 4 | ENTORNO | `echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-<sin_variable>}"`; `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (coincide con "ENTORNO ASIGNADO: NUBE (`cloud_default`)" del propio encargo). `curl` → `000` (sin conectividad / timeout). Por A.13/v2.11: este comando examinó **0 archivos** — es una sonda de red, no una búsqueda sobre el árbol, así que su resultado negativo no es una medición de cobertura de nada; se reporta crudo y no se usa para ninguna conclusión, porque este acto no toca microdato ni red (declarado por el propio encargo). |
| 5 | ESPEJO | — | No se derivó ninguna cifra del espejo del proyecto. Todas las cifras de este cierre salen del clon confirmado en el punto 1, con el comando a la vista en cada fila de la tabla siguiente. |

`command grep -c "duelo\|prereg" data/INFRAESTRUCTURA-v1_0.md` → **5** (no 0): la familia `forense/prereg-duelo-v2/` ya está indexada en `data/INFRAESTRUCTURA-v1_0.md`; no aplica la regla de conducto `ADR-70(c)`, no se añade entrada.

---

## El hallazgo: `MAESTRA32-E9 · PROPAGA-2` no existe

El encargo condiciona su ejecución, en su primera línea, a que un acto llamado `MAESTRA32-E9 · PROPAGA-2` haya fusionado en el mismo carril NUBE, y declara explícitamente **"Sin ranuras"** — sin excepción ni vía parcial para adelantar el trabajo. La sección "FIRMA DE MESA QUE ESTE ACTO EJECUTA" cita, verbatim y entre comillas, el texto de la firma `D1 = (i)` que ese acto E9 supuestamente registra en su propio ADR. Verificado exhaustivamente contra el árbol real, ninguna pieza de `MAESTRA32-E9 · PROPAGA-2` existe:

| # | Afirmación verificada | Comando | Resultado (archivos/entradas examinados) |
|---|---|---|---|
| 1 | No hay encargo archivado para `MAESTRA32-E9` en `forense/encargos/` | `ls forense/encargos/ \| grep -i maestra32` | 5 archivos `MAESTRA32-*` (`E1`, `E2`, `E3`, `E5`, `E6`); ninguno `E9`. Todos los 26 archivos de `forense/encargos/` listados y filtrados. |
| 2 | La cadena `PROPAGA-2` no aparece en ningún archivo `.md`/`.tsv` del árbol | `grep -rn "PROPAGA-2" --include="*.md" --include="*.tsv" -l .` | 0 coincidencias, árbol completo (`canon/`, `forense/`, `data/`, `milpa/`, `tests/`). |
| 3 | La cadena `MAESTRA32-E9` no aparece en ningún archivo `.md`/`.tsv`/`.yaml` (excluidas las falsas coincidencias `MAESTRA31-E9`/`MAESTRA30-E9`, que son actos distintos de un espacio de nombres anterior) | `grep -rn "MAESTRA32-E9" --include="*.md" --include="*.tsv" --include="*.yaml" -i . \| grep -v "MAESTRA31-E9\|MAESTRA30-E9"` | 0 coincidencias reales; las únicas ocurrencias de la subcadena bare `E9`/`ACTO E9` en el árbol son menciones a actos ya censados de ciclos anteriores (`MAESTRA31-E9 · ESTIMA-RUTAC`, `MAESTRA30-E9 · SCORING-V2`, y la frase recurrente "no repetir el defecto ya visto en el acto E9" que cita a este último), verificado leyendo cada ocurrencia. |
| 4 | `main` no se movió desde que se redactó el encargo, y no hay ninguna otra rama remota además de `origin/main` | `git fetch origin --prune`; `git branch -r` | `main` sigue en `1f455ea` (mismo SHA que el encargo declara). Única rama remota: `origin/main`. No es un caso de "main avanzó, refresca y continúa" (ARRANQUE punto 2) — es el caso contrario: nada avanzó, y lo que el encargo asume que ya avanzó (la fusión de E9) nunca ocurrió. |
| 5 | Ningún PR de GitHub, abierto o cerrado, corresponde a `MAESTRA32-E9`/`PROPAGA-2` | MCP `github.list_pull_requests` (owner=`Josanoforo`, repo=`Modelado-Mexicano`, state=`all`, 30 más recientes, orden por creación descendente) | 30 PRs listados, del más reciente (`#395`, `MAESTRA32-E6`, mergeado en `1f455ea`) hasta `#366` (26/ago/2026, antes de que se redactara este encargo). Ninguno trae `E9` ni `PROPAGA` en título o rama de cabeza — salvo `#390`/`acto/maestra31-e9-estima-rutac`, que es el acto `MAESTRA31-E9` de un ciclo anterior, no `MAESTRA32-E9`. |
| 6 | Ningún ADR de `canon/gobernanza-v1_15.md` registra la firma `D1 = (i)` que este encargo cita verbatim ("Mesa autoriza crecimiento acotado del motor antes del GO... enlaces regla→desenlace... pre-registro de dos commits") | `grep -n "D1 *= *(i)\|D1=(i)\|firma D1\|D1 ="` sobre `.md`/`.tsv` del árbol | Dos usos previos de la etiqueta "D1", ninguno coincide: (a) `ADR-49` (31/jul/2026) — "D1: se retira `unico_calibrable_hoy`", una decisión distinta sobre elasticidades del generador; (b) fila `A.12` de `forense/firmas-pendientes.tsv` — firma D1 de mesa del 24/ago/2026 sobre "Generador de candidatas del marco" (`PR codex/generador-marco`), también distinta. El texto de la firma D1 que este encargo ejecuta no está registrado en ningún ADR existente. |

**Conclusión.** El GATE de este encargo no está satisfecho, y el acto que lo satisface no existe todavía en ningún estado del repositorio: ni encargo redactado, ni rama, ni PR (abierto o cerrado), ni ADR. Esto no es un caso de "main se movió, refresca y continúa" (ARRANQUE punto 2, que expresamente NO es un paro) — es exactamente el caso que el propio preámbulo del ARRANQUE anticipa como resultado legítimo: *"Si algo no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el encargo supone es entregable, no interrupción."* La frase "Sin ranuras" del encargo no deja lectura alternativa que permita adelantar `COMMIT-1`/`COMMIT-2` bajo una firma D1 que ningún ADR ha registrado todavía.

---

## Decisión de este acto

No corre `COMMIT-1` (la receta de `forense/notas/2026-08-30-cobertura-15-spec.md`) ni `COMMIT-2` (`forense/prereg-duelo-v2/cobertura-15-v1_0.tsv`). Cierra como hallazgo antes de arrancar el objeto del encargo, siguiendo el mismo patrón que `ACTO MAESTRA31-E9 · ESTIMA-RUTAC` (`ADR-218`): un acto archiva su encargo verbatim (`0-bis · A.3`) y cierra sin ejecutar su objeto cuando el terreno verificado no sostiene la premisa que el encargo asume — sin que eso sea un "PARO"; es el entregable que el propio ARRANQUE pide.

`FP-181` nueva, `ABIERTA`: mesa recibe este hallazgo y decide si (a) redacta y lanza `MAESTRA32-E9 · PROPAGA-2` primero y relanza este mismo encargo después, (b) levanta el GATE de `MAESTRA32-E10` con una firma explícita que reconozca que la firma D1 puede registrarse por otra vía, o (c) reconsidera el orden declarado del carril NUBE. `FP-183`/`FP-184`, pre-asignadas por el propio encargo para el resultado de la corrida real (`B-bis`), **quedan reservadas, sin usar**, para cuando el acto se relance tras el merge real de `MAESTRA32-E9`.

---

## Qué NO hizo este acto

No corrió `COMMIT-1` ni `COMMIT-2`. No creó `forense/notas/2026-08-30-cobertura-15-spec.md` ni `forense/prereg-duelo-v2/cobertura-15-v1_0.tsv`. No leyó ninguna columna de valor de las 15 celdas del marco congelado (ni siquiera las columnas que sí estarían permitidas bajo emisión ciega — no llegó a ese paso). No abrió `forense/prereg-duelo-v2/corridas-R/` ni ningún archivo con valores publicados de las celdas. No tocó `milpa/tramite.yaml`, `milpa/procedencia.yaml`, `canon/modelo-decision-v4_0.md`, el marco congelado, `CONGELADO-v1_0.sha256`, `enlace-M-v1_0.md`, `corridas-*` ni `scoring-adv1-m3.py`. No usó `FP-183`/`FP-184` (quedan reservadas, sin consumir). No adjudicó si el GATE debe levantarse: lo declara pendiente en `FP-181`, mesa decide.

Detalle completo, comando por comando: tablas de arriba (A.13). Encargo original archivado verbatim en `forense/encargos/2026-08-30-MAESTRA32-E10-COBERTURA-15.md` (`0-bis · A.3`, sin editar).
