# ENCARGO `CONSOLIDA-17AGO` · lo que `CIERRA` no pudo escribir, `FP-38`, y el barrido que deja **un solo lugar** donde vive lo abierto

- **SHA de redacción:** `d0019a2` (`origin/main`, merge #249) · **Fecha:** 17/ago/2026 · **Estado:** VIVO — **no ejecutado**. La compuerta ("PR #250 (CIERRA-17AGO) esté fusionado", con el control positivo declarado — columna `ejecutada_en` en `forense/firmas-pendientes.tsv`, debe dar ≥1) no está satisfecha bajo ninguna lectura verificable al arrancar este acto: `PR #250` fusionó (`4415e04`) con **un solo commit** de un plan que su propio cuerpo declaraba en curso ("No fusionar todavía"), y la columna `ejecutada_en` no existe en ningún punto del árbol ni de su historia completa. Detalle comando por comando, con dos derivaciones independientes del camino de recuperación: `forense/notas/2026-08-17-consolida.md`.
- **Entorno: NUBE**, repo-only, sin red, sin corpus. **NO en la caja** — BARRIDO-2 sigue corriendo y no se toca.
- **Modelo: Opus.** La PARTE 3 es triaje con criterio, no conteo: decidir qué pendiente merece fila y cuál merece una línea es exactamente donde un modelo chico infla el tablero.
- **Archívese en `forense/encargos/`** con su lanzamiento (A.3).

> **ADENDA FECHADA — 18/ago/2026.** `ACTO CONSOLIDA-2` (v2, `forense/encargos/2026-08-18-CONSOLIDA-2.md`) ejecutó, contra `68a3466`: PARTE 2 (`FP-38` → `FIRMADA`, procedencia de `glosario:136` corregida) y PARTE 1(b)/(c)/(d) (propagación de `conf.01` a `milpa/refutations.yaml`, re-derivación de la lista "sin ADR" de `glosario:399`, nota fechada de `R1.4` en `hitoD-preregistro`, cierra `FP-43`) — PARTE 1(a) (`conf.02`/`ADR-92(d)`) ya la había ejecutado `ACTO CIERRA-17AGO` al corpus. **Estado revisado: PARCIALMENTE CONSUMIDO.** Siguen `VIVO`, sin ejecutar: **PARTE 3** (el barrido de las 212 notas de `forense/notas/` + `hallazgos.md` + `modelo-decision` + `milpa/*.yaml`, con su triaje `YA RESUELTO`/`FILA`/`SOLO ANOTADO`) y **PARTE 4** (el ADR que sella `firmas-pendientes.tsv` como único lugar de un pendiente). El cuerpo de abajo, tal como se lanzó, no se edita — A.3. Detalle: `forense/notas/2026-08-18-consolida-2-fp38-propagaciones.md`.

> **ADENDA FECHADA — 18/ago/2026 (II).** `ACTO NOTAS-P3` (`forense/encargos/2026-08-18-NOTAS-P3.md`) ejecutó **PARTE 3** completa contra `290f9a0`: universo re-derivado (225 notas, no 212), patrón re-validado (A.4) contra sus dos controles positivos, 148 líneas en 49 archivos, triaje `YA RESUELTO`/`FILA`/`SOLO ANOTADO` cerrado con PRISMA. Tres filas nuevas (`FP-54`, `FP-55`, `FP-56`), cero duplicadas de las cinco candidatas que dirección ya había localizado, cero columnas de tablero desalineadas. `ADR-103` sella la estampa de universo del cierre — registro puro, ninguna decisión nueva. **Estado revisado: PARCIALMENTE CONSUMIDO.** Sigue `VIVO`, sin ejecutar, únicamente **PARTE 4** (el ADR que sella `firmas-pendientes.tsv` como único lugar de un pendiente — `ADR-103` de este acto registra el cierre de PARTE 3, no adopta esa regla forward-looking, que queda para el acto que ejecute PARTE 4). El cuerpo de abajo, tal como se lanzó, no se edita — A.3. Detalle: `forense/notas/2026-08-18-p3-barrido-final.md`.

## ⛔ GATE — no arranca hasta que **PR #250 (`CIERRA-17AGO`) esté fusionado**

Escribe los mismos archivos y ejecuta lo que `CIERRA` dejó declarado y sin escribir.

```sh
git fetch origin && git log --oneline -1 origin/main
grep -c "ejecutada_en" forense/firmas-pendientes.tsv   # control positivo: debe dar >=1 si CIERRA fusionó
```
**Si la columna `ejecutada_en` no existe, PARA:** `CIERRA` no ha fusionado y este acto no tiene dónde escribir.

**BARRIDO-2 no se toca.** Nada de `data/**` ni `tools/**`.

---

════════ ARRANQUE ════════
1 · **REPO.** Clon existente; si clonas, dilo. Ruta · `git log -1 --format="%h %s"` · `git status`. **No arranques desde el home.** `git rev-parse --is-shallow-repository`; si `true`, `git fetch --unshallow` antes de cualquier veredicto.
2 · **SHA.** Base: `main` posterior a #250. Si avanzó más, no es PARO — clasifica la deriva y repórtala.
3 · **data/raw.** No toca microdato — dilo y salta.
4 · **ENTORNO.** Variable cruda + sonda a `https://github.com/`.
5 · **ESPEJO.** Prohibido para cifras.
══════════════════════════

# ⚠️ MÉTODO — control positivo obligatorio en toda búsqueda

**Cuatro recetas rotas de dirección en esta jornada, todas con el mismo síntoma: un "no existe" que era un "no busqué bien".**
`grep -E "MOTOR-2\|sello"` → cero, porque en ERE `\|` es el carácter `|` literal · `grep "policron"` perdió `Polychronic` (inglés) y `policrónica` (acento) · y un pendiente que traje como abierto **ya estaba resuelto en `glosario:315`**.

**Antes de usar cualquier patrón, córrelo contra un caso donde ya sabes la respuesta.** Si el control no da positivo, la receta está rota y el resultado no se reporta. Pega control y salida en la nota. Para texto en español usa normalización de acentos (`unicodedata.NFKD`) y cubre el inglés cuando el archivo esté en inglés.

---

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección contra `d0019a2` ═══

**1 · ESTRUCTURA.** Dominio 7 (ADR + cascada) y Dominio 1 (corpus). Escribe `canon/`, `milpa/`, `forense/`. **No** `data/`, **no** `tools/`.

**2 · CONTENIDO.** Derivado con control positivo:
- `milpa/refutations.yaml:126` trae la resolución propuesta de `conf.02` con la nota **"Requiere ADR"** — el ADR ya existe (`ADR-92(d)`) y el archivo no se enteró → `EXISTE-NO-SATISFACE`.
- `milpa/refutations.yaml` ~`:108` trae `conf.01.calidad_vs_precio` como `resolucion_propuesta` con `entra: false`. **`glosario:315` la declara `✅ Resuelto por precedencia: segmentado — A/B/C+ sí, D/E no`.** No es decisión pendiente: es **desfase de propagación** → `EXISTE-NO-SATISFACE`.
- `glosario:398` dice *"conf.02, conf.05, conf.07 — sin ADR"*. Con `ADR-92` es falso para las dos primeras, y **no estaba en la lista de sitios de `CIERRA`** → `EXISTE-NO-SATISFACE`.
- `FP-38` sigue `ABIERTA` sin firma registrada → `EXISTE-NO-SATISFACE`.
- Fila para "ocho refutaciones sin objeto" en el tablero → `NO-ENCONTRADO` (`gobernanza:1643` la tiene `Abierta`, el tablero no la tiene).
- Fila para el corte de edad → `NO-ENCONTRADO` (6 sitios en `modelo-decision`, cero ADR).

**3 · COBERTURA RETROACTIVA.** El tablero nació el 14/ago; **todo lo anterior es invisible para él salvo alta manual** — ésa es exactamente la brecha que la PARTE 3 cierra.

**ESTAMPA DE UNIVERSO (A.10).** Todo lo anterior se derivó contra `origin/main = d0019a2`, con `origin/codex/barrido-2` en 14 commits, el 17/ago/2026. **Re-derívalo al arrancar.** Una verificación contra rama viva caduca en minutos; `REGISTRA-17AGO` ya lo pagó.

═══════════════════════════════════════════════════════════════════

**PERÍMETRO.** Escribe **exactamente**: `milpa/refutations.yaml` · `canon/glosario-v5_6.md` · `canon/gobernanza-v1_15.md` (UN ADR) · `forense/firmas-pendientes.tsv` · `forense/hitoD-preregistro-v2_0.md` · `forense/notas/2026-08-17-consolida.md` · `forense/hallazgos.md` · `forense/encargos/2026-08-17-CONSOLIDA-17AGO.md`.

**NO escribe:** `data/**` · `tools/**` · `canon/estado-programa-v1_10.md` (BARRIDO-2) · `corpus/**` (lo hizo `CIERRA`) · `tests/**` · `instrucciones-*`.

⚠️ **`estado-programa:136-137` sigue bloqueado por BARRIDO-2** — tercer acto seguido. Deja las dos líneas redactadas en la nota bajo `CASCADA NO ESCRITA` y **ábrele fila**, para que deje de heredarse de acto en acto.

**Nombra tu nota `2026-08-17-consolida.md`** — no repitas el nombre del encargo: `T02` colisiona por nombre normalizado y ya falló en #248.

---

## PARTE 1 · Las cascadas que `CIERRA` no pudo escribir

**(a) `milpa/refutations.yaml`, entrada `conf.02.policronia` (~`:114`-`:130`).** Su `resolucion_propuesta` dice *"Resolver a favor del report de tiempo… La refutación entra con el mecanismo estructural, no con el cultural. **Requiere ADR**"*, y `entra: "solo con mecanismo estructural"`. **Ese ADR existe: `ADR-92(d)`.** Cita el ADR, marca la resolución como adoptada, y **conserva el texto de la propuesta** — es la prueba de que el motor lo había anticipado. Revisa también `:200` (`ver_conflicto` desde `ref.A.06.impuntualidad_como_rasgo`) y declara si cambia.

**(b) `milpa/refutations.yaml`, entrada `conf.01.calidad_vs_precio` (~`:94`-`:112`).** **No adjudicas nada**: `glosario:315` ya la declaró resuelta por precedencia —segmentada, A/B/C+ sí, D/E no—. Propaga esa resolución al yaml, que sigue con `entra: false` y el texto en modo propuesta. **Verifica primero que `glosario:315` siga diciendo eso; si no, PARA.**

**(c) `glosario:398`.** Reescribe la lista de "sin ADR" contra el estado real tras `ADR-92`. **Deriva cuáles quedan, no las heredes de este encargo.**

**(d) `hitoD-preregistro`, `R1.4` (`:59`-`:60`).** `CIERRA` la dejó redactada en su nota por estar fuera de perímetro. **Es registro maestro de falsación: entra como nota fechada en el bloque append-only, no como edición del cuerpo** — mecanismo que el propio archivo declara en `:892`. Declara que `R1.4` consume la rama **estatus** de `conf.05`. **No toques su veredicto.**

## PARTE 2 · `FP-38` — firmada

Cita de mesa, verbatim: *"El expediente de F38, el experimento no aplica, no es México."* Texto adoptado:

> "La procedencia de la celda de consumo compensatorio en `glosario:136` pasa de `(a)+(c)` a **`(c)`**: Velandia-Morales et al. (2022) es un experimento del CIMCYC, Universidad de Granada, y **no es evidencia sobre población en México**. El tier `Fuerte` de la rama `consumo_compensatorio.estatus` **queda sin sostén por esa cita** y se marca como tal, no se sustituye por otra. El falsador ya está identificado dentro del programa: `recovery-plan`:65 asigna `R1.4` a **ENIGH, 6 olas** — dato mexicano propio, en disco."

**Deriva antes de escribir:** que `glosario:136` siga marcada `(a)+(c)`. Si `CIERRA` ya la desdobló en dos filas, **aplica la corrección a la fila de estatus** y dilo. Si `recovery-plan`:65 no dice ENIGH 6 olas, **PARA**.

## PARTE 3 · El barrido final — un solo lugar para lo abierto

**Esto es lo que mesa pidió, en sus palabras: *"ya no quiero más items abiertos o decisiones pendientes regados por todo el proyecto."***

**Universo, cerrado y declarado:** `forense/notas/*.md` (212 archivos) · `forense/hallazgos.md` · `canon/modelo-decision-v4_0.md` · `milpa/*.yaml`. **Todo lo demás ya fue barrido** por `ADR-91` y por `#248`; no lo repitas.

**Patrón de dirección, validado contra dos controles positivos —** `"**Pendiente de mesa, no ejecutado aquí:**"` y `"RANURA (c): verificada SIN FIRMA"` **— re-válidalo tú antes de usarlo:**

```
queda (a|para) mesa | pendiente de mesa | decisión de mesa pendiente |
sin (sellar|adjudicar) | requiere (ADR|firma|decisión) | RANURA | \[FIRMA |
propuesta sin sello | no se decide aquí | sigue en mesa | pendiente nombrado
```
Contra `d0019a2` daba **135 líneas en 46 archivos**. Reporta tu cifra; si difiere, manda la tuya.

### El triaje, y su criterio — no todo merece fila

**Aplica el criterio que `A.6` ya fijó, verbatim: *"Lo acotado es el disparador, no el tipo… Si un cierre no bloquea ninguna regla, se anota en `forense/hallazgos.md` y se queda como está."***

Tres cubetas, y cada hallazgo va a exactamente una:

1. **`YA RESUELTO`** — el pendiente existe en la nota pero un ADR, el glosario o un acto posterior lo cerró. **Va a la nota con la cita que lo resuelve, no al tablero.** Precedente medido: `conf.01` estaba resuelta en `glosario:315` y dirección la trajo como abierta.
2. **`FILA`** — gatea algo vivo hoy: una ficha del Hito D, un contador, un acto en cola, o un activo en riesgo. **Abre fila.**
3. **`SOLO ANOTADO`** — real pero no gatea nada. **Una línea en `hallazgos.md`. No infla el tablero.**

**Cierra la parte con el conteo por cubeta.** Si la cubeta `FILA` supera **diez**, para y repórtalo antes de escribirlas: más de diez filas nuevas de un barrido es señal de criterio mal calibrado, no de hallazgo.

### Cinco candidatos que dirección ya localizó — verifícalos, no los heredes

| Dónde | Qué | Lectura de dirección |
|---|---|---|
| `2026-08-11-e4c-r5-1-d2-commit3`:59 y :90 | Dos decisiones con los números ya puestos: indexación (`0` real vs `23.16%` citado vs `45` personas) y `1,312`/`2,201` hogares. **Gatean el diseño de `R5.1-D3`**, único acto que puede mover `13 de 27`. | **`FILA`, y de las de arriba** |
| `2026-08-13-w-limpieza-worktrees`:86 | `Modelado-Mexicano-curador`: **590 commits sin empujar**, "la pieza más grande del inventario sin adjudicar". | **`FILA`** — activo real en riesgo |
| `modelo-decision`:189, 215, 219, 220, 457, 482 | **Seis sitios** con `corte PENDIENTE` de `edad`. Cero ADR lo fija. Gatea el perfil 5 y deja `H-02`/`H-06`/`H-07` en `NO DETERMINABLE`, y **dos reglas SI-ENTONCES operativas** (`:457`, `:482`) se disparan sobre él. Ver también `2026-08-04-x-condicionamiento-y-forma`:494. | **`FILA`** |
| `milpa/refutations.yaml`, `decision_pendiente` | **Ocho refutaciones sin objeto**, incluida `ref.A.02` —única `MUY_FUERTE` de las 49—. `gobernanza:1643` la tiene `Abierta`. Consecuencia medida: la batería reporta 49 y solo 30 son ejecutables; *"27 de 49 pasan"* es en realidad **27 de 30**. | **`FILA`** |
| `2026-08-12-acto-sonda1-mapa-barreras`:175 | GDELT·11 y UCDP·16, *"requiere decisión de mesa"*. | **`YA RESUELTO`** — `ADR-76(g)`, firma verbatim *"Bajamos lo necesario para identificar en qué consisten"*, ejecutado en `ACTO GDELT-UCDP-RECON` (#212). **Va a la nota, no al tablero.** |

**Ids nuevos: derívalos al sellar.** BARRIDO-2 reclama su propio `FP-38` y todavía no fusiona: el máximo real puede ser mayor que el del tablero.

## PARTE 4 · La regla que hace que esto no vuelva a pasar

**El ADR de este acto sella, en una frase, lo que mesa pidió:**

> **`forense/firmas-pendientes.tsv` es el único lugar donde vive un pendiente.** Ningún documento del programa —nota, encargo, propuesta, report, ADR o archivo del motor— declara un pendiente, una ranura de firma o una decisión de mesa **sin abrir su fila en el mismo commit**. Los demás documentos **apuntan** al tablero; no lo sustituyen. Un pendiente sin fila es defecto de la misma clase que un encargo sin archivo (`A.3`), y se corrige igual: abriendo la fila, no discutiéndolo.

Es extensión directa de `ADR-91` y de la regla de conducto de `ADR-70(c)`. **No inventes vocabulario nuevo:** los estados son `ABIERTA` · `FIRMADA` · `FIRMADA-CONDICIONAL` · `SIN CAMBIO`, y `CIERRA` añadió `ejecutada_en` y `encargo`.

**Y el ADR declara la fecha de corte:** *"barrido de consolidación corrido el <fecha> contra `<SHA>`, sobre el universo `forense/notas/` + `hallazgos.md` + `modelo-decision` + `milpa/*.yaml`. Desde este acto, todo pendiente anterior a esa fecha que no tenga fila **fue examinado y clasificado**; lo posterior nace con fila por la regla de arriba."* **Sin esa estampa, el barrido no sirve para lo que mesa lo pidió** — que no quede duda de qué se hizo y cuándo.

**Falsador y caducidad:** si en tres meses `T22` nunca dispara por un marcador sin fila, la regla se retira y se anota. **Defecto real que atrapó:** los cinco de la tabla de arriba, ninguno con fila, y uno —el corte de edad— con seis sitios y dos reglas operativas colgando de él.

## Lo que este acto NO hace

No adjudica ninguno de los pendientes que el barrido encuentre — **los hace visibles** · no toca `estado-programa`, `data/`, `tools/`, `corpus/` ni `tests/` · no re-decide `conf.01`, `conf.02` ni `conf.05`: propaga · no toca el veredicto de `R1.4` · no cierra `FP-29`, `FP-33` ni ninguna fila gateada por BARRIDO-2 · **no lanza el acto del curador** aunque abra su fila.

## Cierre

`python3 tests/check.py --baseline` antes y después. **Reporta por test, no agregado** — #248 reportó 8 y la corrida real dio 11 por agregar. Espera `T22` (filas nuevas: señal) y `T15`/`T16` (cascada de ADR que no puedes escribir). **No recongeles** sin ADR de mesa (`ADR-76(f)`).

`git diff --check` · nota con cada comando, **su control positivo** y su salida cruda · una entrada en `hallazgos.md` · este encargo `CONSUMIDO` con su PR · **merge local**, editor web prohibido · **jamás te auto-fusionas**.

**Contadores de medición sobre México: 0.** Este acto no mide: termina de propagar dos adjudicaciones, firma una, y deja el programa con **un solo lugar donde mirar lo que falta**. Dilo así, sin justificarlo.
