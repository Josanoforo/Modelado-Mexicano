# Nota del acto · CI-CATEGORÍA — devolver el significado al CI

18/ago/2026. Sesión repo-only, nube (`cloud_default`), clon existente en
`/home/user/Modelado-Mexicano`, rama `claude/ci-categoria-significado-wspwwn`.
Redactado contra `997482b` (verificado, sin deriva de `main` al arrancar).

**Exclusión T22(b), declarada.** Esta nota cita, verbatim, la palabra
`RANURA` al describir el control C2 del commit 1 (que crea a propósito un
archivo con ese marcador para probar la auto-protección de T22). No es una
ranura real sin fila -- es la documentación del propio control. Sumada a
`_T22_ARCHIVOS_CONOCIDOS` en el mismo commit que introduce esta nota,
mismo criterio que ya usaron las notas de `ACTO TABLERO-FIRMAS` para el
mismo autocaptura.

## ARRANQUE — lo reportado antes de tocar nada

1. Repo: clon existente, no se clonó ninguno nuevo. `git log -1` → `997482b
   Merge pull request #244 from Josanoforo/codex/barrido-2`. `git status`
   limpio.
2. SHA: coincide con 997482b, sin deriva.
3. `data/raw`: ausente (`test -d data/raw` falla). No es paro, este acto no
   la usa.
4. Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`. `curl` a
   INEGI → `000` (exit 56, sin conexión, confirmado dos veces) — hecho
   sobre la allowlist de esta caja, no sobre INEGI. `ls data/raw/` vacío.
5. Espejo: no usado; toda cifra de esta nota sale del clon anterior, con
   comando a la vista.

Verificación de existencia (contra 997482b): los cuatro comandos del §2 del
encargo dieron exactamente lo declarado (`require-cableado` → 0; `warn("T22"`
→ 1292,1311; `fail("T22"` → 1277,1333; `SENAL`/`def senal` → sin resultados).
ADR máximo re-derivado: `grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md`
→ 95 únicos, max 95, sin huecos → el ADR nuevo de este acto es **ADR-96**.
Tablero: 48 filas de datos, llega hasta FP-48, cabecera con 9 columnas
(`id qué_se_firma dónde creado gatea estado firmada_en ejecutada_en encargo`).

## COMMIT 1 · Arreglo de categoría de T22 (SENAL)

Mecanismo implementado tal como lo especifica el encargo: tercer buffer
`SENAL = []` junto a `FAILS, WARNS`; función `senal(test, msg)` que sigue
alimentando `FAILS`/`WARNS` (la corrida cruda no cambia) y además registra
`(test, _baseline_key(msg))` en `SENAL`. Los dos `warn("T22", …)` de la rama
(a) — ABIERTA (`:1292`) y FIRMADA sin ejecutar (`:1311`) — pasan a
`senal("T22", …)`. Los dos `fail("T22", …)` de la rama (b) — tablero
ausente (`:1277`) y marcador sin fila (`:1333`) — quedan intactos. Se resta
`set(SENAL)` en los tres sitios que consumen las claves: `_freeze_baseline`
(`:1600`/`:1601`, ahora `... - set(SENAL)`) y `_baseline_compare`
(`:1618`, ídem).

### Los cuatro controles — salida cruda, corridos y revertidos antes del commit

**C1 · fila ABIERTA ficticia (`FP-99`) en el tablero.**
```
$ python3 tests/check.py            # T22 WARN 19→20 (FP-99 sí se imprime)
$ python3 tests/check.py --baseline
  LÍNEA BASE: ROJO — 3 entradas nuevas frente a tests/baseline.json
  · T16: canon/estado-programa-v1_10.md: declara 132 WARN vigente; la corrida real da N WARN
  · T16: canon/estado-programa-v1_10.md: declara 19 FAIL · 132 WARN vigente; la corrida real da N WARN
  · T16: canon/gobernanza-v1_15.md: declara 19 FAIL · 132 WARN vigente; la corrida real da N WARN
```
Las 3 entradas nuevas son **T16, cero T22** — la propiedad bajo prueba
(que la clave de T22 quede fuera de la comparación) se sostiene: ningún
`(T22, …)` aparece en "nuevos". La línea base sí sale ROJA, pero por un
mecanismo ajeno a este arreglo y preexistente: `senal()` sigue alimentando
`WARNS` igual que `warn()` (la corrida cruda no puede dejar de reportar
T22(a), A.12 lo exige) — así que cualquier fila ABIERTA nueva, de la
categoría que sea, mueve el WARN real de 132 a 133, y T16 (que compara
citas fijas de `gobernanza`/`estado-programa` contra ese real) empieza a
fallar donde antes coincidía. Este acoplamiento ya existía antes del
arreglo de T22 (`senal()` y `warn()` alimentan el mismo buffer) y es
exactamente el objeto del COMMIT 2. No se declara como defecto de este
commit.

**C2 · archivo nuevo en `forense/` con marcador `RANURA`, sin fila.**
```
$ python3 tests/check.py
  [FAIL]  T22 T-FIRMAS  (3 fail, 19 warn)   # 2→3: nuevo fail en :1333
$ python3 tests/check.py --baseline
  LÍNEA BASE: ROJO — 3 entradas nuevas
```
Protección intacta.

**C3 · `forense/firmas-pendientes.tsv` renombrado.**
```
$ python3 tests/check.py
  [FAIL]  T22 T-FIRMAS  (1 fail)            # solo :1277, "no existe"
$ python3 tests/check.py --baseline
  LÍNEA BASE: ROJO — 4 entradas nuevas
```
Protección intacta.

**C4 · fecha simulada 2027-03-01** (sin `faketime` disponible en la caja;
monkeypatch de `datetime.date.today` vía `importlib`, sin tocar el árbol):
```
LÍNEA BASE: VERDE — nada nuevo. exit_code=0
```
El arreglo de ADR-88 (`_T22_EDAD_VARIABLE`) no se regresa.

Los cuatro escenarios se revirtieron antes de continuar (`git status`
limpio salvo `tests/check.py`, verificado tras cada control).

### Recongelado — el único de este acto

```
$ python3 tests/check.py --freeze
[--freeze] escrito tests/baseline.json — HEAD 997482bbda18b52621e24909eedbed0630c7a111 · 21 fail · 102 warn congelados
$ python3 tests/check.py --baseline
LÍNEA BASE: VERDE
```
`T22` aporta 2 fail / 0 warn al congelado (verificado con
`json.load`) — los 19 warn de la rama (a) quedan fuera vía `SENAL`, los 2
fail de la rama (b) siguen siendo regresión real y siguen congelados.
Commit `485a32d`, declarado en su mensaje como el último recongelado
autorizado bajo el régimen viejo.

## COMMIT 2 · Punto fijo de T16 — hallazgo que cambia el alcance

**Verificación del punto fijo (paso 1, tal como lo pide el encargo):**
antes de resincronizar nada, se probó la hipótesis con una edición
temporal (editada y revertida, nunca commiteada) sobre UNA de las tres
citas que hoy no matchean el núcleo, `gobernanza-v1_15.md:1658`
(`**24 FAIL · 126 WARN**` → `**19 FAIL · 132 WARN**`):

```
$ python3 tests/check.py                       # con la edición temporal
  [FAIL]  T16 T-SUITE-SELF-CHECK  (2 fail)      # 3→2: la línea editada deja de fallar
  21 FAIL · 132 WARN                            # 22→21, exactamente -1
$ CHECK_SELFCHECK_CHILD=1 python3 tests/check.py
  19 FAIL · 132 WARN                            # subproceso sin cambio
```
Cierra: cada FAIL de T16 que desaparece de una cita resta exactamente 1 del
total de la corrida completa, y el subproceso (que excluye a T16 de sí
mismo) permanece en 19 FAIL · 132 WARN sin moverse — no por casualidad de
esta corrida, sino **por construcción**: como T16 nunca corre dentro de su
propio subproceso, `real_fail`/`real_warn` jamás puede incluir la
contribución de T16, así que es estructuralmente inmune a cuántas citas de
`gobernanza` estén desincronizadas. Edición revertida de inmediato
(`cp` desde backup, `git status` limpio confirmado antes de seguir).

**Por qué el commit no toca `gobernanza-v1_15.md` — el hallazgo que
reduce el alcance.** El encargo asume que existen "tres citas vigentes"
(`:1106`, `:1136`, `:1658`) que se pueden resincronizar a `19 FAIL · 132
WARN`. Verificado leyendo el texto real de las tres:

- `:1106` y `:1136` (dentro de `ADR-76(f)` y `ADR-77`, ambos sellados)
  narran lo que esa corrida midió **al sellarse** (`18 FAIL · 104 WARN`).
  `ADR-90` ya las declaró **permanentes**, verbatim (`gobernanza:1106`):
  *"nunca debe seguir al real"*. Reescribirlas violaría esa decisión de
  mesa ya sellada, no solo el principio general de no falsear el pasado.
- `:1658` (dentro de `ADR-94`, también sellado) narra el estado **antes**
  del acto (`"commit inicial, d0019a2"`), la misma clase de snapshot
  histórico que `:1106`/`:1136` — solo que sin el bloque `> **vX.Y —
  DD/mon.**` que `_CAMBIO_FECHADO` exige para reconocerla como histórica.
  Es el mismo límite que el propio docstring de `t16_suite_self_check` ya
  declara ("si un canónico narra un cambio pasado con cualquier otra
  forma... este test NO lo reconocerá como histórico").

Ninguna de las tres es, narrativamente, una "cita vigente" desincronizada
que corresponda actualizar — las tres son historia ya sellada que el test
no sabe leer como tal. Sobreescribirlas sería exactamente lo que el propio
encargo prohíbe ("falsear el pasado para poner verde un vigía es peor que
el rojo"). Las citas genuinamente vigentes que sí existen en el archivo
(`gobernanza:764` y `:856`) **ya dicen** `19 FAIL · 132 WARN` — no
necesitan tocarse.

Las tres quedan protegidas por el mecanismo que ya existe, sin código
nuevo: `_T16_REAL_SUFIJO` (dentro de `_baseline_key`, ADR-90) normaliza el
sufijo volátil `"la corrida real da… WARN"` para **cualquier** mensaje de
T16 que lo lleve — el regex no está acotado a `:1106`/`:1136` — así que
`:1658` hereda la misma protección contra recongelados espurios sin que
nadie lo declarara por nombre hasta ahora. Los tres FAIL de T16 ya están
capturados en el congelado de COMMIT 1 (`tests/baseline.json`), como
deuda conocida y aceptada, igual que las otras 21 entradas.

**Consecuencia sobre el alcance del commit:** ningún archivo de canon se
edita. El commit consiste en el comentario de aclaración en `_suite_real()`
(fecha y derivación: ACTO CI-CATEGORIA, 18/ago/2026) que documenta el punto
fijo verificado arriba y nombra las tres citas protegidas, para que la
próxima sesión que tropiece con el mismo "T16 rojo para siempre" no
repita la investigación desde cero.

`tests/baseline.json` no cambia en este commit (ningún FAIL/WARN se mueve,
comentario-only) — verificado, `--baseline` sigue VERDE contra el
congelado de COMMIT 1.

## COMMIT 3 · La regla del recongelado — redactada, no sellada

Per instrucción explícita del encargo ("Redáctala, no la selles solo"),
el texto de abajo se propone como fila `ABIERTA` de
`forense/firmas-pendientes.tsv` (insertada en COMMIT 4, junto con las
otras dos filas de este acto — el perímetro de este acto restringe los
cambios al tablero a las filas de §4, así que ningún commit anterior lo
toca) y **no** se sella en `canon/gobernanza-v1_15.md` — eso queda para
cuando mesa firme.

**Texto propuesto:**

> Un recongelado de `tests/baseline.json` no es la vía rutinaria al
> verde. Si un test obliga a recongelar más de una vez, está mal
> categorizado: o es señal permanente (sale de la comparación de línea
> base, como `T22(a)` vía `SENAL`, `ACTO CI-CATEGORIA` commit 1) o es
> regresión real (se arregla en el corpus, no en el congelado). El
> recongelado queda reservado al caso único, con ADR de mesa que declare
> qué se congela y por qué — mismo criterio que `ADR-76(f)` ya fijó para
> autorizar cada recongelado individual, generalizado aquí a una regla
> sobre *cuántas veces* es aceptable invocarlo para el mismo test.
>
> **Falsador y caducidad** (impuesto de v2.3, obligatorio para toda regla
> nueva): si en tres meses desde su firma ningún recongelado se evita por
> esta regla — es decir, si en ese plazo nadie se topa con "este test ya
> se recongeló antes, hay que categorizarlo, no recongelarlo de nuevo" —
> se retira, y el retiro se anota en la propia fila de este tablero (no
> se borra, per convención de `forense/firmas-pendientes.tsv`).
>
> **Qué le habría costado a un lector, medido y no hipotético:** durante
> toda la jornada del 17-18/ago (7 recongelados en 10 h — ver la enmienda
> de este mismo acto al hallazgo de `9941adf`, más abajo), `--baseline`
> no distinguía regresión de señal, así que la única señal de "algo
> cambió" era un ROJO indiferenciado que se resolvía recongelando. En ese
> mismo tramo, la corrida cruda (no el congelado) sí traía hallazgos
> reales: `T02` cazó una colisión de nombre, `T03` una cita a un archivo
> inexistente, `T15` un hueco de numeración de ADR. Los tres eran
> visibles en la salida de la suite — pero bajo un régimen donde recongelar
> es la respuesta por defecto a cualquier rojo, cualquiera de los tres
> pudo pasar inadvertido, tratado como "ruido de línea base" en vez de
> como el hallazgo real que era. Esta regla no afirma que eso haya
> ocurrido con estos tres — afirma que el régimen viejo no daba forma de
> distinguirlo, y ésa es la falla de categoría exacta que `SENAL` (commit
> 1) empieza a cerrar para `T22`, generalizada aquí a un principio para
> cualquier test futuro con el mismo defecto.

Fila propuesta (contenido exacto, para copiar en COMMIT 4):
`qué_se_firma` = el texto de arriba (colapsado a una línea, sin markdown
de blockquote); `dónde` = `canon/gobernanza-v1_15.md` (ADR propuesto, sin
sellar) y `tests/check.py` (`SENAL`, precedente ya implementado que esta
regla generaliza); `creado` = `2026-08-18`; `gatea` = que mesa firme el
ADR antes de sellarlo — mientras tanto sigue vigente el criterio caso por
caso de `ADR-76(f)`; `estado` = `ABIERTA`; `encargo` =
`forense/encargos/2026-08-18-CI-CATEGORIA-devolver-significado-ci.md`.
