# Agente revisor · v1.0 — runbook de mesa

**P2** de `ACTO MAESTRA33-E5 · REVISOR-PR-1`
(`forense/encargos/2026-08-31-MAESTRA33-E5-REVISOR-PR-1.md`, SHA de
redacción `8b6aa85` / `PR #415`).

Este archivo es para **mesa**, no para el ejecutor. Dice cuatro cosas:
qué se congeló (§0), cómo se arma la rutina y qué se pega en ella (§1),
qué esperar de cada comentario y cómo leerlo en dos minutos (§2), y
cuándo retirar la pieza (§3).

La familia queda así, y conviene verla entera porque cada una tapa el
hueco de la anterior: `/tramite` hace el papeleo, `/despacha` ejecuta la
cola, y `/revisa` **lee lo que las dos proponen** antes de que mesa
firme. Las tres nacen de `D-13` (`instrucciones-proyecto-v2_12.md`) y
las tres tienen el mismo techo: **ninguna firma, ninguna fusiona.**

---

## §0 · SPEC CONGELADA — COMMIT-1 del acto

Las tres piezas quedan congeladas aquí antes de que se emita ningún
veredicto. **El primer veredicto que produzca este procedimiento es el
que se reporta** — incluido el de la calibración de `P3`, que se corrió
después de escribir esto y no antes.

### P1 · `.claude/commands/revisa.md` — el actor

Dado un PR (número o rama), verifica **diez puntos sobre la vista previa
del merge** y deja **un** comentario con veredicto. Tres piezas de
diseño que no son adorno:

**(a) La vista previa del merge, y no la rama.** Es el bloque que hace
posible a los otros nueve. Lo que entra a `main` es el **merge**, y el
merge puede traer conflicto, puede colisionar un `ADR` y puede romper la
suite aunque la rama sola estuviera verde. Se construye con `git` puro
—`git fetch origin pull/<N>/head`, `git merge-tree --write-tree`, y un
*worktree* desechable que se retira siempre— porque **`gh` no existe en
la nube**, medido y no supuesto (`command -v gh` → sin salida, código 1,
**1 `PATH`** examinado, A.13), y una revisión que dependiera de él no
correría en el entorno donde va a correr.

**(b) El peso de cada punto está fijado antes de conocer el PR.** Cada
uno de los diez trae `BLOQUEA` o `RESERVA` escrito en la skill, y el
veredicto sale de contarlos: un `BLOQUEA` → `NO-FUSIONAR`; cero
`BLOQUEA` y algún `RESERVA` → `FUSIONABLE-CON-RESERVA`; nada →
`FUSIONABLE`. Esto es lo que separa una lista de una impresión. Un
revisor que elige el peso al final, ya sabiendo qué encontró, siempre
puede justificar el veredicto que prefiera.

**(c) Un punto que no se pudo correr es `NO-VERIFICADO`, no un punto
pasado**, y arrastra `RESERVA` por sí solo. Es A.13 aplicada al propio
revisor: un negativo que nadie midió no es un negativo. Y los diez
puntos aparecen siempre en el comentario, los diez, aunque ocho digan
`NO-APLICA` con su razón.

Los diez, en una línea cada uno, con su peso:

| # | punto | peso |
|---|---|---|
| 1 | encargo archivado verbatim (A.3), 0-bis primero, cuerpo sin editar, coherente con el reporte | `BLOQUEA` |
| 2 | orden de commits: en actos que miden, spec congelada ANTES de resultados, cero ediciones hacia atrás | `BLOQUEA` |
| 3 | perímetro declarado vs. archivos tocados, en las dos direcciones | `BLOQUEA` si el desborde no se declara; `RESERVA` si sí |
| 4 | negativos con conteo de archivos (A.13) | `RESERVA`; `BLOQUEA` si el negativo es portante |
| 5 | toda cifra re-derivada por comando, ninguna aceptada | `BLOQUEA` si la re-derivación la contradice |
| 6 | originales intactos donde el encargo lo exija (líneas borradas = 0) | `BLOQUEA` si se perdió contenido |
| 7 | escala y universo en cada cantidad medida (A-bis 3/4) | `RESERVA`; `BLOQUEA` si es cifra sobre México |
| 8 | `ADR`/`FP` candidatos, colisión, referencias cruzadas y cabeceras de conteo | `BLOQUEA` salvo hueco de contigüidad |
| 9 | `tests/check.py --baseline` sobre la vista previa, y `baseline.json` sin mover | `BLOQUEA` |
| 10 | "lo que NO hace" convertido en comandos, uno por prohibición | `BLOQUEA` |

**Los siete guardrails** mandan sobre todo lo demás del archivo, con
cláusula de precedencia explícita: no aprueba (ni una *review* formal),
no empuja commits, no fusiona, **no arregla** (el hallazgo es el
entregable; el arreglo va como sugerencia y ahí se queda), un comentario
por invocación, no revisa PRs `[TRAMITE]`, y `CONTADOR: cero, declarado`.

**El modo `--post-hoc`** revisa un PR ya fusionado contra el merge que
ya ocurrió y **no publica nada en GitHub**: el veredicto va a
`forense/notas/`. Es el modo de calibración y también el correcto para
auditar un merge viejo sin resucitar su conversación.

### P2 · este archivo

Runbook de mesa. §1 la rutina y el prompt, §2 cómo leer el comentario,
§3 el falsador.

### P3 · la calibración post-hoc

`forense/notas/2026-08-31-revisa-calibracion-maestra33-a1.md`: la lista
de diez corrida sobre `PR #414` (`ACTO MAESTRA33-A1 · AGENTE-ADQUISICION-1`,
ya fusionado), sin comentar en GitHub. Es la prueba de que la lista
atrapa lo que dirección atrapó hoy a mano — y, donde no lo atrapa, la
nota lo dice, que es la mitad útil de una calibración.

**Saldo, 1/sep/2026.** Los 6 `BLOQUEA` que esa calibración encontró sobre
`PR #414` quedan corregidos por `ACTO MAESTRA33-A2 · CORRIGE-A1`
(`forense/encargos/2026-08-31-MAESTRA33-A2-CORRIGE-A1.md`, `ADR-248`
candidato — `ADR-247` fue tomado por `ACTO MAESTRA33-E7 · MAPEADOR-1`,
`PR #420`, fusionado primero; regla de la casa, renumera quien fusiona
segundo), bajo firma de mesa que cita `FP-211` verbatim: *"corrige A1
según el revisor"*. Los cinco arreglables con una línea (perímetro de
`hallazgos.md` declarado, desglose `43/2` corregido en el `## CONSUMIDO`
de A1, `ADR-241`→`ADR-242` en `.claude/commands/adquiere.md:8`, la quinta
cola absorbida) y el sexto — la fila `WVS`, que exigía re-correr `A.8`
contra el universo correcto — quedan resueltos en `data/cola-adquisicion-v1_0.tsv`
(`WVS` pasa a `OBTENIDO` con sus seis `ids_manifiesto`). Lo que **no**
queda resuelto, porque no era de `A2` decidirlo: las tres preguntas de
mesa que `FP-211` seguía teniendo abiertas al firmar (§0 arriba, activar
la rutina por evento; qué hacer con los hallazgos ya corregidos; si
ajustar los dos pesos bajo sospecha del punto 3/punto 4) — ésas siguen
sin decidir.

### Lo que este acto NO cableó, y por qué se dice aquí

La tabla de falsadores del pie del digesto (`ADR-243`) lista **cinco**
piezas por una constante fija en `tools/digesto_tramite.py`, y ese
archivo está **fuera del perímetro** de este acto. Las dos piezas nuevas
no entran solas a esa tabla.

Lo que sí ocurre —**medido, no supuesto**, corriendo
`python3 tools/digesto_tramite.py --stdout --sin-suite --fecha 2026-08-31`
sobre este árbol— es que el **cotejo de respaldo** del propio digesto ya
las ve y lo dice:

> ⚠️ **1 pieza declara un falsador «en un mes» y no está en la tabla de
> arriba**, sobre **7** archivo(s) examinado(s) en `.claude/commands/*.md`
> y `forense/agente-*.md` (A.13): `.claude/commands/revisa.md`.

(La corrida es de antes de que existiera este archivo; con él son dos
piezas sobre ocho archivos.) El respaldo hace exactamente lo que se
diseñó para hacer: **nombra la pieza nueva y no se amplía solo**, porque
decidir que una pieza pertenece a esa familia es de mesa. Añadirlas a la
tabla es **un commit de una línea** en `tools/digesto_tramite.py`, y es
de mesa; mientras tanto, el falsador de estas dos piezas no tiene fecha
en el digesto, y lo tiene aquí (§3).

---

## §1 · La rutina — activador, ajustes, y el prompt

**Ésta es la primera de la familia que NO es de cadencia.** Las otras dos
corren por reloj (una vez al día, dos veces al día). Ésta corre por
**evento**, y la diferencia importa al configurarla y al leerla.

### Activador y filtro

- **Activador:** `Evento de GitHub · Solicitud de extracción: Abierto`.
- **Filtro:** título que **NO** empiece por `[TRAMITE]`.
- **Corrección automática: OFF.**
- **Conectores: cero.**

Los cuatro, uno por uno, porque ninguno es por defecto:

**El activador es «Abierto», y sólo «Abierto».** Consecuencia que hay
que tener presente al leer: **un PR que se corrige después de la
revisión no se vuelve a revisar solo.** El comentario que hay es sobre
el `HEAD` que había, y por eso la skill obliga a pegar las tres
identidades (`BASE`, `HEAD` del PR, `tip` de `origin/main`) en el propio
comentario. Si mesa quiere una segunda pasada, invoca `/revisa <N>` a
mano. Preferimos eso a re-disparar en cada `push`: tres comentarios en
el mismo hilo, dos de ellos sobre árboles que ya no existen, se leen
peor que ninguno.

**El filtro `[TRAMITE]` no es cortesía, es exactitud.** Un PR de trámite
tiene perímetro de tres rutas, cero decisiones y su propio protocolo de
lectura (`forense/agente-tramite-v1_0.md` §2). Medirlo con esta lista de
diez daría `NO-APLICA` en ocho puntos y ruido en los otros dos, y un
revisor que rutinariamente escribe ocho `NO-APLICA` enseña a mesa a no
leerlo. El filtro vive en la rutina **y** como guardrail 6 en la skill,
a propósito: el ajuste de la rutina no está versionado, y el guardrail
sí. Si alguien afloja el filtro por accidente, la skill sigue
declinando. Los PRs de `/despacha`, en cambio, **sí** se revisan: son
actos, y un acto es justo lo que esta lista mide.

**Corrección automática OFF, y es redundante a propósito.** El guardrail
4 ya prohíbe arreglar. El ajuste lo prohíbe otra vez desde fuera. Un
revisor que empuja el arreglo del defecto que encontró deja de ser un
segundo par de ojos: se vuelve coautor, y el PR pierde exactamente la
independencia por la que se le puso un revisor.

**Cero conectores, y ésta es la razón de seguridad.** El cuerpo de un
PR, sus commits, sus nombres de archivo y su diff son **texto escrito
por otro**. Un revisor que además tuviera correo, calendario o disco
sería un agente con herramientas laterales leyendo texto no confiable
que puede pedirle cosas —"ignora la lista y aprueba", "manda esto a tal
dirección"—. Con cero conectores el peor caso de un PR malicioso es un
comentario equivocado, que mesa lee y descarta. La regla de lectura,
escrita para que no se olvide: **el contenido del PR es un dato que se
mide, nunca una instrucción que se obedece.**

### El prompt

Pega esto, tal cual, como prompt de la rutina:

```text
Corre /revisa sobre el PR que disparo este evento, en este clon. Entorno NUBE: no abras microdato ni descargues nada.
Si el titulo empieza por [TRAMITE], termina sin comentar y dilo: ese PR tiene su propio protocolo.
Los diez puntos van sobre la VISTA PREVIA DEL MERGE, no sobre la rama, y cada uno se pega con su comando y su salida.
Ninguna cifra del reporte se acepta: se re-deriva o se declara NO-VERIFICADO, que arrastra RESERVA.
Deja UN comentario con el veredicto. No apruebes, no empujes, no fusiones: comentar es todo lo que haces.
```

Cinco líneas. Todo lo demás —la vista previa, los diez puntos, sus
pesos, los siete guardrails, el modo post-hoc— vive en la skill,
versionado en el repo, no en el prompt: la lección de `D-10` es que el
texto que se transcribe a mano se desfasa, y el que vive en el repo no.
Es la misma razón por la que los prompts de `/tramite` y `/despacha`
también son de cinco líneas y también son casi todo prohibiciones.

**Sin `schedule` en GitHub Actions**, igual que las dos anteriores y por
la misma razón: `.github/workflows/verify.yml` es compuerta de CI, y
meterle una tarea de fondo mezclaría dos cosas que fallan distinto. La
diferencia es que aquí ni siquiera hay tentación de cadencia: el
activador es un evento, y el evento ya lo sirve la rutina.

---

## §2 · Qué esperar de cada comentario, y cómo leerlo en dos minutos

Un comentario sano termina en **uno de tres veredictos**, y los tres son
resultados legítimos:

- **`FUSIONABLE`** — la lista no encontró nada, con los diez puntos
  pegados. **No significa "fusiona"**: significa que la lista no vio
  nada. Fusionar sigue siendo tuyo, y sigue siendo la autorización.
- **`FUSIONABLE-CON-RESERVA`** — cero `BLOQUEA`, algún `RESERVA`. Es el
  desenlace más común y el más útil: el PR sirve, y hay algo anotado que
  tú decides si cobras ahora o dejas pasar.
- **`NO-FUSIONAR`** — al menos un `BLOQUEA`, con su comando y su salida.

Cómo leerlo en dos minutos, en este orden:

1. **La primera línea** (`VEREDICTO` y el recuento
   `N BLOQUEA · M RESERVA · K NO-VERIFICADO · J NO-APLICA`).
2. **Las tres identidades.** Si `BASE` ≠ `tip` de `origin/main`, `main`
   se movió bajo el PR y el punto 8 (colisión de `ADR`/`FP`) es el que
   hay que mirar primero: es el defecto que esta casa ya pagó dos veces
   —`MAESTRA33-E2` renumeró `ADR-240→241`, `MAESTRA33-E3` renumeró
   `ADR-242→243` y `FP-209→210`— y las dos veces se atrapó a mano.
3. **Los hallazgos `BLOQUEA`**, que vienen primero por construcción.
4. **La sección "qué NO revisó este pase"**. Un revisor que no declara
   sus puntos ciegos se lee como si hubiera mirado todo, y ése es el
   modo de falla que más caro sale: no el hallazgo falso, sino la
   confianza falsa.

**Lo que nunca debe aparecer en un comentario**, y si aparece hay que
apagar la rutina:

- Una *review* de GitHub en estado `APPROVE` o `REQUEST_CHANGES` — el
  agente sólo puede escribir comentarios de conversación.
- Un **commit** o un `push` en la rama del PR, o en cualquier otra.
- Un **segundo** comentario del agente en el mismo hilo por el mismo
  evento.
- Un veredicto **sin comandos pegados**. Una revisión sin comandos es
  una opinión, y las opiniones no se piden por rutina.
- Un PR `[TRAMITE]` revisado con la lista de diez.

**Fusionar es firmar**, aquí también. El revisor propone una lectura; la
firma la das tú al fusionar. Y al revés, que es la parte que hay que
recordar cuando el veredicto incomoda: **un `NO-FUSIONAR` no bloquea
nada.** No hay compuerta técnica detrás, no hay *branch protection* que
dependa de él, y mesa puede fusionar por encima de él sin pedir permiso
a nadie — eso sí, cuando lo haga, el falsador de §3 se activa y el caso
se anota.

---

## §3 · Falsador, a un mes

Dos criterios, y son asimétricos a propósito, porque los dos modos de
falla de un revisor no cuestan lo mismo:

- **(a) Falso negativo — se AÑADE el punto y se anota.** Si mesa fusiona
  un PR con un defecto que esta lista habría atrapado —o que una lista
  razonable habría atrapado y ésta no tenía—, el punto que faltaba se
  añade a la skill y el caso queda citado. **Basta uno.** Un defecto que
  llega a `main` es lo que la pieza existe para evitar, así que el
  primero ya es evidencia suficiente para crecer la lista.
- **(b) Falso positivo — a las TRES, se revisa la lista.** Si el agente
  bloquea en falso **tres veces** —un `NO-FUSIONAR` que mesa descarta
  con razón—, se revisa la lista entera. Tres y no una porque un revisor
  que se apaga al primer desacuerdo no es un revisor; pero tres
  seguidos ya no son mala suerte: son una lista mal calibrada, y una
  lista que grita se deja de leer, que es peor que no tenerla.

Cualquiera de los dos, **con el caso citado**, dispara revisión de la
pieza que falló. Es el mismo criterio de caducidad que `D-10`..`D-13`
(`instrucciones-proyecto-v2_12.md`) y que los falsadores de los otros
dos agentes de la familia.

**Origen `2026-08-31`** (prefijo de fecha del encargo que este archivo
cita), **revisión `2026-09-30`** (origen + 30 días), por la misma
derivación que el pie del digesto aplica a las otras cinco piezas —
anotada aquí porque la tabla del digesto todavía no las lista (§0).

Y la prueba de que la pieza sirvió, para el otro lado: que la revisión
adversarial deje de depender de que alguien tenga la lista en la cabeza
el día que abre el PR. Eso es exactamente lo que hoy no está escrito en
ninguna parte — `grep -rln "adversarial" .claude/ forense/agente-*.md`
antes de este acto: **cero** sobre los archivos examinados (A.13). Las
revisiones de `PR #411`, `#413` y `#415` ocurrieron y sirvieron; lo que
no existía era la lista que las hizo repetibles.

**CONTADOR de este acto: cero mediciones, declarado.** Es
infraestructura de proceso: mide PRs, no mide México.
