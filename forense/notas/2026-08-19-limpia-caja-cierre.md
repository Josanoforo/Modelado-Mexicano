# ACTO LIMPIA-CAJA — la caja queda con un clon, el corpus y dos worktrees vivos; `FP-59` ejecutada

`PR #278` · `ADR-113` · Base: `origin/main` = `470fa57` (`PR #277`) · Sesión **UBUNTU**, dueña única · Modelo: Opus · Sin `--freeze`.

Ejecuta lo que `ADR-112` §5 dejó adjudicado y explícitamente no ejecutó: *"Worktrees `PURGA-ARTIFACT`: no se borran en este acto. Limpieza física es acto aparte, con el bundle como red."*

## §0 · Arranque — el encargo predijo bien el movimiento, y su espejo estaba vencido en dos cifras

`origin/main` **se movió** respecto al `2d08d7a` del encargo, como éste anticipaba: `470fa57`, tras fusionar `PR #276` (`REFIRMA-OPACA`) y `PR #277` (`ADQ-15`) — ambos el mismo día. `2d08d7a` verificado ancestro. No es PARO.

Entorno (`A.2`, tres partes, valores crudos): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **sin_variable** · sonda INEGI → **`200`** · `ls data/raw/ | head -1` → **`20260813130000.export.CSV.zip`**. `pgrep` de procesos del proyecto → **ninguno**, al arranque y al cierre.

**Corrección al encargo (`data/raw`).** El encargo declara el corpus en `/home/pc0/Modelado-Mexicano-barrido2`. Falso por comando: `barrido2/data/raw` es **él mismo un symlink** a `/home/pc0/mm-corpus/raw` (284 entradas), que es el corpus real. `mm-corpus/` no estaba en el perímetro declarado y **cae dentro del glob `/home/pc0/mm-*`** que el encargo manda barrer — se trató como intocable y jamás se usó un glob para borrar, sólo listas explícitas.

**Corrección al espejo (`A.10`).** Las cifras del encargo se re-derivaron del disco: **780 archivos ✓** (coincide; `git status --porcelain` colapsa a 7 entradas de directorio, el conteo real exige `-uall`) pero **5.1M en disco / 2.37MB de bytes reales**, no los 6.5MB citados. Y **24 ramas** era el universo de `ADR-112` §5, no el de la caja: ver §1.

## §1 · El inventario real — 56 worktrees, no 26; y un segundo clon que ningún barrido había visto

`git worktree list` desde el clon principal dio **56 entradas**. `w-limpieza §4` (13/ago) conocía 26; `ADR-112` §5 adjudicó 24. **Los 30 restantes nacieron después del 13/ago** y entran por la cláusula de cobertura retroactiva del encargo, que exige inventariarlos aparte y no borrarlos si su rama no está fusionada.

Clasificación derivada por comando (`merge-base --is-ancestor` + `log origin/main..` + `status --porcelain`), no de la nota:

| clase | n | criterio | destino |
|---|---:|---|---|
| `PURGA-ARTIFACT` de `ADR-112` §5 | 21 | `merge-base` `9301e59` (29/jul), HEAD en `remapeo-shas` | podado |
| `SIN-CONTENIDO-ÚNICO` (`mesa/s-svystat`) | 1 | estancamiento post-purga, 0 añadidos | podado |
| `curador` | 1 | 101 no-trackeados **verificados byte-idénticos** en `main` | podado |
| `barrido-completo` | 1 | `FP-59`, rescatado en este PR (§3) | podado |
| `map-b/crosswalk` | 1 | ancestro; script rescatado antes (§5) | podado |
| post-13/ago **fusionados** | 28 | ancestro de `origin/main`, 0 sin empujar, 0 no-trackeado | podado |
| **vivos / protegidos** | 4 | clon base · corpus `barrido2` · `reconcilia-puertas` · este acto | conservados |

**Verificación de seguridad antes de borrar nada** (método de `ACTO Z`, `git diff --diff-filter=A origin/main <rama>`): 21 de 24 candidatos dieron **0 añadidos**. Los 3 con 2 añadidos (`regla-elegibilidad`, `cruce-catalogo-fichas`, y la rama del clon base) resultaron ser **el mismo par superado por versión** — `canon/estado-programa-v1_9.md` y `data/catalogo-fuentes-v1_0.md`, contra `v1_10` y `v2_0` vigentes en `main`. No es contenido único: es el salto de versión.

Los 28 fusionados se revisaron **uno por uno contra su merge de integración** (tabla completa en el PR): cada uno con su `PR #` identificado, de `#192` a `#277`. Dos exigieron segundo comando porque el camino de ancestría devolvió un merge vecino: `inv-descmx` (su HEAD `d55ae72` **es** el merge de `PR #221`) y `w-r/tres-encargos` (`PR #194`, no el `#195` que el camino tocó).

## §2 · `F0` — el mini-respaldo, y tres redes más que el encargo no pedía

El tar de mesa que `ADR-112` §4 declaró *no observado* sigue sin existir; se ejecutó su sustituto:

```
~/respaldo-worktrees/barrido-completo-untracked-20260818.tar.gz
sha256 47dffd1f5218f4fd565a8805af5fb1ff96f0de1235dc523ac6d8d56beb0f4ab3
575,610 bytes · 794 entradas
```

*(El nombre lleva `20260818` porque `date` local va en `-0600`: son las 21:2x del 18/ago en la caja, 19/ago en UTC. El encargo, mesa y esta nota fechan 19/ago.)*

Añadidas por criterio propio, porque la poda iba a ser mucho mayor que la prevista y **una poda irreversible no es una poda auditable**:

| red | qué protege | sha256 |
|---|---|---|
| `limpia-caja-todas-las-ramas-20260818.bundle` | **las 143 ramas locales** — hace reversible toda la poda | `9874adbd…4340` |
| `reconcilia-puertas-20260818.bundle` | la rama con contenido único (§5) | `bffb76a4…18fe` |
| `segundo-clon-proyectos-20260818.bundle` | el 2º clon entero, 28 refs | `5202b179…9b62` |
| `map-b-build_crosswalk-20260812.py` | el script que §5 de `ADR-112` señaló sin fila | `f167c47f…31fa` |

`curador-2026-08-18.bundle` **verificado, no supuesto**: su sha256 en disco es `19dbf51e…9618`, idéntico al que `ADR-112` §3 registró.

Este mini-respaldo **se borra cuando `FP-59` quede fusionada** — su contenido ya vive en `main` por este PR. Los otros cuatro no: son la red de lo que *no* entra al repositorio.

## §3 · `F2` — `FP-59` adjudicada `RESCATE-A-PR`, por comando

Detalle de los cuatro incisos en `ADR-113`. Lo decisorio, en una línea: **`main` cita 211 ids `SEMTSK-*`/`TCUR-*` cuyos cuerpos no viven en ninguna parte del repositorio** (intersección disco ∩ `main` = 211 de 211, cero sin citar). El argumento no es el volumen ni la antigüedad — es que descartarlos convierte 211 citas vivas en citas colgantes.

Contra-argumento considerado y descartado: *"son bitácoras regenerables"*. No lo son en el sentido que importa — re-correr el motor produce ids **nuevos**, y son estos ids los que `main` cita. La regenerabilidad del *tipo* de artefacto no restituye la *identidad* citada.

Copia verbatim preservando ruta relativa (patrón exacto de `PR #274`), **780 de 780 con sha256 idéntico entre disco y copia**, más `MANIFIESTO-RESCATE.tsv` propio (ruta/tamaño/mtime/sha256). Todos los `mtime` caen en **2026-08-07**, lo que confirma el `-20260807` del nombre del directorio en vez de asumirlo.

`T02` disparó, como el encargo anticipó (*"T02 por diseño si colisiona"*): 213 entradas nuevas, **ROJO**. Resuelto por el mecanismo de **grupo** (`EXCEPTED_PREFIXES`), no por `--freeze` — que el encargo prohíbe. `tests/baseline.json` sin tocar. Corrida final: **21 FAIL · 119 WARN, `LÍNEA BASE: VERDE`**, idéntica a la de partida.

## §4 · `F3` — la poda

**52 worktrees removidos** (`git worktree remove --force`; el `--force` sólo por el symlink `data/raw` no-trackeado, verificado inofensivo en cada caso antes de forzar — mismo criterio que `w-limpieza §3`). `git worktree prune` retiró además una entrada administrativa huérfana (`worktrees/mm-rescate-curador-cierre`, gitdir inexistente).

**39 ramas locales borradas** con `git branch -d`, **nunca `-D`**, de las 40 fusionadas; `cond-atrib` se conserva por estar activa en el worktree del corpus. Quedan **104** ramas: `main`, `cond-atrib` y **102 no fusionadas** — casi todas población pre-purga, de las que `ADR-112` §5 sólo adjudicó 24. **No se tocaron**: están fuera del mandato ("ramas locales cuyo remoto ya fusionó") y todas viven en el bundle. Son deuda declarada, no residuo.

**Clon base movido a `main`.** Estaba en `sesion/cal-conf-faseb-pos4-envipe-paso1`, **593 commits detrás** y sobre historia pre-purga. Esto no es cosmético: `w-limpieza §2` documentó que un clon base sobre rama vieja hace que `git branch -d` compare contra el `HEAD` equivocado y **rechace por falso negativo** ramas ya fusionadas. Con el clon en `main`, las 39 bajas pasaron a la primera, sin el rodeo de `--set-upstream-to` que aquel acto necesitó. Los no-trackeados (`data/raw`, `data/secretos.local.yaml`) sobrevivieron intactos.

Ningún proceso hubo que matar: no había ninguno vivo.

## §5 · Lo que NO se borró — y por qué la regla lo exigía

**`mm-reconcilia-puertas` tiene contenido único, verificado, no supuesto.** Su rama **nunca existió en `origin`** (`ls-remote` vacío) y sus 5 commits tocan 2 archivos, **ambos distintos de `main`**: su nota trae **122 líneas ausentes** de la versión de `main` — porque la de `main` viene de una **ejecución distinta del mismo encargo** (`PR #208`, hecha en la nube) — más **una línea de `hallazgos.md` sin registrar**. El propio último commit de la rama (*"addendum final — PR #208 ya cerró este encargo"*) es lo que vuelve tentador borrarla: dice que el encargo se cerró, no que **este texto** esté en `main`. Es exactamente el caso que la cláusula de cobertura retroactiva protege, y el `PROHIBIDO` del encargo cubre. Respaldada en bundle, **no adjudicada**: qué se hace con ella es decisión de mesa, no de un acto de higiene.

**`scratch/build_crosswalk.py`** (133 líneas) — el riesgo que `ADR-112` §5 señaló *"para que no se pierda por silencio"* sin abrir fila. Genera `data/crosswalk-fuente-puerta-2026-08-13.tsv`, que **sí** vive en `main`: el producto estaba versionado, el instrumento no. Copiado a `~/respaldo-worktrees/` **antes** de podar su worktree. Sigue sin fila de tablero: abrirla sin marca de mesa es lo que §5 declinó hacer y el perímetro de este acto (`solo FP-59`) repite.

## §6 · Fuera de perímetro — reportado, no tocado

**`~/mm-purga.git` (12M) conserva historia pre-purga.** Espejo *bare* de `PURGA-PRIVACIDAD` (10/ago), 168 refs, con sus artefactos `filter-repo/` completos (`commit-map`, `ref-map`). Contiene `9301e59`: **el estado del repositorio anterior a la purga**, es decir el que todavía tiene las 1,737 filas de datos personales que `filter-repo` retiró de lo público. No se inspeccionó su contenido más allá de comprobar que el objeto existe, y **no se borra aquí**: es una decisión de privacidad con implicaciones forenses (la tabla de remapeo ya vive en `main`, `canon/remapeo-shas-purga-2026-08-10.tsv`), no higiene de worktrees. **Se recomienda a mesa adjudicarlo explícitamente.**

**`~/mm-paso5` (25M)**: tercer clon, rama `paso5-remapeo-shas-2026-08-10`, HEAD `f420498` (`PASO 5` de la misma purga) — **ya fusionado** en `origin/main`, 0 no-trackeado. Podable en un acto que lo tenga en perímetro.

**El segundo clon, borrado por firma de mesa en sesión.** `~/proyectos/Modelado-Mexicano` (`main` en `PR #161`, 6/ago — 10 días stale) con **9 worktrees propios** en un tercer directorio, `~/worktrees/`, que ningún barrido había visto: 4 `mapa-ext`, `revalida-1`, `med-r3-4`, `acto-r2prima`, `mapa-ext-1`, más un cascarón vacío de 16K sin entrada en ningún `worktree list`. Presentado a mesa con su evidencia; respondió **"respalda y bórralo"**. Bundle de 28 refs verificado, luego borrado: **179M** liberados.

**Estado vencido corregido de paso:** `50344ac` (`ACTO R″`), que el registro de sesiones tenía como huérfano *sin PR*, **está fusionado en `origin/main`**; y las notas de los cuatro actos `mapa-ext` viven en `main`. Ese árbol era redundante, no trabajo perdido — pero eso **se verificó antes de borrar**, no se asumió.

## §7 · Estado final

```
$ git worktree list
/home/pc0/Modelado-Mexicano            470fa57 [main]           ← clon base, ahora al día
/home/pc0/Modelado-Mexicano-barrido2   387ad82 [cond-atrib]     ← corpus, sólo lectura
/home/pc0/mm-limpia-caja               [limpia-caja]            ← este acto
/home/pc0/mm-reconcilia-puertas        f169abd [reconcilia-puertas] ← vivo, §5

$ df -h /home/pc0
/dev/sdd  1007G  35G  922G  4%     (39G → 35G; +179M del 2º clon ya contados)
```

Directorios del proyecto que sobreviven: los 4 de arriba, más `mm-corpus/` (el corpus), `mm-purga.git/` y `mm-paso5/` (§6). **Worktrees: 56 → 4. Ramas locales: 143 → 104.**

## §8 · Cierre

1. **`FP-59` → `CERRADA`**, `ejecutada_en` = este PR + `ADR-113`, `encargo` poblado. Convención por precedente `FP-55`/`FP-15`: firmada y ejecutada cierra `CERRADA`, no queda en `FIRMADA` indefinidamente.
2. **Ninguna fila nueva.** Máximo del tablero re-derivado al escribir (**60**) y a re-derivar al fusionar. `ADR` re-derivado al escribir (máximo **112** → **113**), a re-derivar al fusionar: hoy ya hubo un doble `FP-58` y `ADR-112` es producto de dos renumeraciones.
3. **Extensión de perímetro declarada**: `tests/check.py`, no listado en el encargo. Sin ella el acto no cierra en verde y la única alternativa era `--freeze`, prohibido. Mecanismo y precedente en `ADR-113`.
4. **Desviación declarada**: el encargo asigna Opus y la sesión arrancó en Sonnet por un `/model` previo; se paró y se pidió el cambio **antes** de tocar disco. Todo el acto corrió en Opus.
5. **La causa de los cierres abruptos de Ubuntu** que motivó el encargo (*"reventó ubuntu por tener items ahí volando"*) **sigue sin identificarse** — igual que en `w-limpieza §1`. Este acto retira la condición sospechada (52 worktrees vivos, un segundo clon oculto), **no prueba la hipótesis**: no se observó ningún cierre durante la sesión, y sin un fallo reproducido no hay medición. Si vuelve a ocurrir con la caja así de limpia, la hipótesis queda refutada y eso vale más que este acto.
6. **Contadores de medición sobre México que mueve este acto: 0.** Es higiene de entorno; no midió ninguna hipótesis del programa.

`encargo` → `CONSUMIDO`.
