# ENCARGO `REGISTRA-17AGO` · las cinco firmas de mesa del 17/ago, los dos benchmarks, y las filas que faltaban

- **SHA de redacción:** `1282ae3` (`origin/main`, merge #247) · **Fecha:** 17/ago/2026 · **Estado:** `CONSUMIDO` — `PR #248` (rama `claude/new-session-wk4z60`), detalle en `forense/notas/2026-08-17-registra-17ago-comandos.md`.
- **Entorno asignado: NUBE**, repo-only, sin red, sin corpus. **NO en la caja** — ahí corre BARRIDO-2 y este acto no necesita microdato.
- **Modelo: Sonnet 4.6.** Es registro, no adjudicación: los textos van verbatim y las derivaciones son de una línea.
- **Archívese en `forense/encargos/`** con su lanzamiento (A.3).

**Por qué existe.** Mesa firmó cinco decisiones en conversación el 17/ago y **ninguna llegó al repo**. Las cinco filas siguen `ABIERTA` con `firmada_en` vacío, y los dos benchmarks que sostienen dos de ellas viven fuera del árbol. Por `ADR-91` el tablero es la fuente única: *"toda decisión pendiente tiene fila ahí o no existe"*. Ahora mismo, para el programa, estas decisiones no ocurrieron.

---

════════ ARRANQUE ════════
1 · **REPO.** Clon existente; si no hay, clona y dilo. Reporta ruta absoluta · `git log -1 --format="%h %s"` · `git status`. **No arranques desde el home.** Corre `git rev-parse --is-shallow-repository`; si `true`, `git fetch --unshallow` **antes** de cualquier veredicto (precedente E-HIG).
2 · **SHA.** Base `1282ae3`. Si main avanzó **no es PARO**: clasifica la deriva (¿tocó `firmas-pendientes.tsv` o `gobernanza`?) y repórtala antes de editar.
3 · **data/raw.** Este acto no toca microdato — dilo y salta.
4 · **ENTORNO.** Reporta `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` crudo y la sonda a `https://github.com/`. No toca red de datos.
5 · **ESPEJO.** Prohibido para cifras. Todo sale del clon, con el comando a la vista.
══════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por dirección contra `1282ae3` ═══

**1 · ESTRUCTURA.** Gobiernan `forense/firmas-pendientes.tsv` (7 columnas: `id · qué_se_firma · dónde · creado · gatea · estado · firmada_en`; convención A.12, ADR-85, `gobernanza:1369`) y `canon/gobernanza-v1_15.md` §4 (ADR, máx hoy **91**, cero huecos). Dominio 7 del índice de infraestructura. **Nada de `data/` se escribe.**

**2 · CONTENIDO.** Derivado, con comando:

```
$ python3 -c "...firmas-pendientes.tsv..." | grep -E 'FP-(22|25|27|28|36)'
FP-22: ABIERTA  firmada_en=(vacío)
FP-25: ABIERTA  firmada_en=(vacío)
FP-27: ABIERTA  firmada_en=(vacío)
FP-28: ABIERTA  firmada_en=(vacío)
FP-36: ABIERTA  firmada_en=(vacío)

$ ls forense/ | grep -i "benchmark.*conf"
(cero — los dos benchmarks no están en el repo)
```
Resultado A.4: las cinco filas **`EXISTE-NO-SATISFACE`** (existen, les falta la firma). Los dos benchmarks **`NO-ENCONTRADO`** en `forense/`, buscados por nombre y por patrón.

**3 · COBERTURA RETROACTIVA.** El tablero nació el 14/ago (`6e0f2a1`); las cinco filas son posteriores o fueron dadas de alta por `ADR-91`. **Sin brecha retroactiva.**

═══════════════════════════════════════════════════════════════════

**PERÍMETRO Y CONCURRENCIA.** Escribe **exactamente**: `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` (append de **UN** ADR) · `forense/BENCHMARK-conf02-policronia-2026-08-17.md` (nuevo) · `forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md` (nuevo) · `forense/notas/2026-08-17-registra-17ago.md` · `forense/hallazgos.md` (una entrada, `merge=union`) · `forense/encargos/2026-08-17-REGISTRA-17AGO.md` (este texto, A.3).

**NO escribe:** `data/**` · `tools/**` · `canon/estado-programa-v1_10.md` · `canon/glosario-v5_6.md` · `canon/integrador-*` · `corpus/**` · `tests/**` · `instrucciones-proyecto-*`.

⚠️ **BARRIDO-2 corre en la caja** (`origin/codex/barrido-2`, 10 commits por delante, PR #244 borrador) y **escribe `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md`**. Colisión esperada en el ADR: **renumera al fusionar, T15 arbitra**, precedente `TABLERO-FIRMAS c5`. `firmas-pendientes.tsv` **no** lo toca — verificado con `git diff --name-only origin/main...origin/codex/barrido-2`.

*"Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo."*

---

## COMMIT 1 · Las cinco firmas, verbatim

Formato de `firmada_en`, idéntico al que `ADR-91` ya usó: `ADR-<n>, PR #<n>, 17/ago — firma de mesa verbatim: '<cita>' sobre el texto adoptado: '<texto>'`.

**Las citas son EXACTAMENTE éstas. No las parafrasees, no las corrijas, no les añadas puntuación.**

**FP-25 → `FIRMADA`.** Cita: *"Listo instrucciones actualizadas con versión V2.10"*. Texto adoptado: "`instrucciones-proyecto-v2_10.md` pegada en el proyecto de Claude el 17/ago/2026. A.9 satisfecha: la versión está en los dos lados."

> **Y registra el hallazgo de procedencia que la acompaña, porque corrige a A.9 sobre sí misma.** A.9 declara que el pegado *"ocurre a mano, fuera de este repositorio"* y que ninguna sesión puede verificarlo. **Es cierto para un acto de Claude Code y falso para una sesión de chat del proyecto**, que sí lee las instrucciones cargadas. La confirmación del 17/ago fue de ese tipo: la sesión de dirección leyó `A.9`, `A.10` y `A.12` en su propio contexto. **Procedencia tipo (1) por esa vía, no tipo (3).** Mismo mecanismo que destrabó M6 — el espejo es visible desde el chat y no desde el CLI.

**FP-22 → `FIRMADA` por contención.** Misma cita. Texto: "v2.9 queda contenida en v2.10." **Deriva la contención tú, no la heredes:**
```sh
python3 -c "
a=open('instrucciones-proyecto-v2_9.md',encoding='utf-8').read()
b=open('instrucciones-proyecto-v2_10.md',encoding='utf-8').read()
for k in ['A.9','A.10','A.12']: print(k, k in a, k in b)
print(a.count(chr(10)), b.count(chr(10)))
"
```
Contra `1282ae3` da `True True` en las tres y `356` contra `384` líneas. **Si te da otra cosa, PARA y repórtalo.**

**FP-36 → `FIRMADA`.** Cita: *"No caducan. No en este caso."* Texto adoptado: "Un acto bloqueado por entorno NO gasta vida de caducidad: el reloj se pausa y se reanuda cuando el entorno lo permite. La prueba del bloqueo es la firma de entorno de tres partes (A.2) registrada por el acto que paró." Resuelve lo que `ADR-54` y su enmienda in situ dejaron *"sin decidir aquí"* **dos veces**, desde el 4/ago.

**FP-27 → `FIRMADA`.** Cita: *"FP-27 tercera opción"*. Texto adoptado:
> "`conf.02` se adjudica por una **tercera vía**, no por las dos que la fila ofrecía: **se adopta el mecanismo de `El Mexicano y el Tiempo`** —norma social contextual más estructura, con las mismas personas operando monocrónicamente cuando el entorno lo exige— **y se conserva el desenlace de `Psicología del Trabajo`**: *'la cultura del mañana significa poca fiabilidad'* sigue siendo falso. La policronía sobrevive como **preferencia individual medible**, sin adscripción nacional; no sobrevive como **rasgo cultural mexicano**. Razón escrita: `forense/BENCHMARK-conf02-policronia-2026-08-17.md`."

**FP-28 → `FIRMADA`.** Cita: *"Fp28: partir en 2"*. Texto adoptado:
> "`conf.05` se parte en dos constructos con tier propio, porque no son dos lecturas de un hallazgo sino dos hallazgos con desenlace y mecanismo distintos: **`consumo_compensatorio.estatus`** (desenlace: gasto en bienes posicionales; mecanismo: beneficio simbólico) y **`consumo_compensatorio.recompensa`** (desenlace: ingesta de comida y alcohol; mecanismo: beneficio hedónico). `No promediar` deja de ser prohibición sin contraparte: no había una sola cosa que promediar. Razón escrita: `forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md`."

**Los dos benchmarks van adjuntos al lanzamiento.** Verifica por hash **antes** de commitear, **una invocación por archivo** (A.1), salida cruda pegada en la nota. Discordante ⇒ **PARA**.

| Archivo destino | sha256 |
|---|---|
| `forense/BENCHMARK-conf02-policronia-2026-08-17.md` | `30588ca05b31b9df774aa7309cce9d99aac8fc26cad9a46bdb8fba131dbc7064` |
| `forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md` | `c39aa4b675c62163e908dc0217d0103c1559adaee2ff8ac3067b982512934a72` |

Van **verbatim, cero ediciones**: son la razón escrita que la adjudicación de FP-27 exige, y editarlos rompería su propio hash. La procedencia va en el mensaje de commit, no dentro del archivo.

**El ADR va en este commit.** Registra las cinco firmas y **declara explícitamente lo que NO hace**: no ejecuta la cascada al corpus de `conf.02` ni de `conf.05`. Número derivado al sellar con la receta de T15 (`^\*\*ADR-(\d+)`), contra el `main` real del momento, **sin dejar hueco**. Contra `1282ae3` da `91`; **si te da otra cosa, ése es tu número.**

**Cascada del conteo de ADR:** `gobernanza-v1_15.md:2` y `estado-programa-v1_10.md` (las dos citas, no solo el cierre del listado). ⚠️ `estado-programa` está **fuera de tu perímetro** por BARRIDO-2 — **no lo edites**: deja la línea de cascada redactada en tu nota bajo el encabezado `CASCADA NO ESCRITA — colisión de perímetro con BARRIDO-2`, y repórtalo en el PR. **Precedente exacto:** es lo mismo que hizo `R5.1-D3-LANZA` con la fila de FP-19.

## COMMIT 2 · Las filas que faltaban

Ninguna adjudica nada: hacen visible lo que hoy no tiene fila. Ids derivados desde `FP-38` (verificado libre contra `1282ae3`). Estado `ABIERTA`, `gatea` según se indica.

| Qué | `gatea` | Origen |
|---|---|---|
| **La procedencia de `glosario:136` está mal marcada.** Dice `(a)+(c)` —incluye dato primario mexicano— y la cita que sostiene el tier `Fuerte` es un experimento del CIMCYC, Universidad de Granada, con un resultado nulo declarado adentro. Corresponde `(c)`. **Afecta el tier, no es cosmético.** | ninguno | BENCHMARK conf.05 §1(d) |
| **El integrador adjudica contradicciones abiertas sin ADR.** `:245` y `:351` toman partido en `conf.02`; en `conf.05` **se contradice a sí mismo** — `:255` separa las dos ramas, `:36` y `:204` las tratan como una. ¿Se audita el integrador completo contra el casillero §S5, o se corrigen solo estos dos y se anota? | ninguno | los dos benchmarks |
| **`El Mexicano y el Tiempo`:49 infringe A.4.** Dice *"No hay medición nacional reciente de policronía mexicana"* sin universo declarado, y sí hay dato viejo (Carraher et al. 2004, incluye México). Corresponde `NO-ENCONTRADO` con universo. | ninguno | BENCHMARK conf.02 §1(f) |
| **`CANONICO` de `tests/check.py:286` se desvió del Bloque A sin ADR.** El Bloque A admite *fuerte · media · hipótesis razonable · narrativa popular*; el test admite `{FUERTE, MEDIA, MEDIA-FUERTE, HIPÓTESIS}` — **añadió `MEDIA-FUERTE` y borró `narrativa popular`** por su cuenta. Segundo defecto: T07 compara con `.upper()` pero cuenta con `tok.strip()`, así que `Moderada` y `MODERADA` se reportan como dos vocabularios cuando el propio test los trata como uno. **El "7" de FP-30 es en parte artefacto de conteo.** | ninguno | barrido de repo 17/ago |
| **Dos filas del tablero necesitan texto que vive fuera del repo (A.3).** `FP-24`: su regla propuesta está en `PLAN-MULTIFASE-F0-F6-2026-08-13.md:94`, verificado **fuera del árbol**. `FP-33`: cita *"las cuatro preguntas del transfer"* y **no hay ningún TRANSFER en el árbol** — `grep -rn "cuatro preguntas"` solo devuelve las de M-1/ENSANUT, que son otras. **Las dos son inejecutables como están escritas.** | ninguno | barrido de repo 17/ago |

**Y corrige tres filas que el barrido encontró mal descritas** — solo el campo `gatea` y/o `qué_se_firma`, **sin cambiar el estado**:

- **`FP-15`** — su `gatea` dice "el sello del motor". `ADR-79(c)` lo confirma, pero **`MOTOR-1 §4` ya derivó todo su contenido**: qué debe citar E5 en su universo, el veredicto sobre `57(c)` (**`SIN CAMBIO`**) y el hallazgo de la cifra que E5 no debe copiar (`1` llave ejercida de `2` filas, `0` compuertas abiertas). **No falta decisión de mesa: falta un número de ADR.** Anótalo en `gatea`.
- **`FP-31`** — **ya está resuelta y la fila no lo dice.** `propuesta-motor-adaptativo-celda-v0_4.md:122` declara *"Preguntas para mesa — resueltas, 12/ago/2026"*, y la única que esa versión responde ya la adjudicó **`ADR-71(d)`**; **`ADR-68`** adoptó el contrato celda-D v0.3 como formato del registro. Lo pendiente es **rotular el documento por referencia a esos dos ADR**, no decidir. Anótalo en `qué_se_firma`. **No la cierres tú** — el rótulo es acto propio.
- **`FP-29`** — su `gatea` no dice lo que bloquea. `hitoD-preregistro:322` (D-06) dice, verbatim: *"R8.3 depende de `conf.06`, abierto: ninguna cifra de confianza interpersonal es usable. Cualquier veredicto apoyado en ellas no cuenta."* Y la escala de `R8.3` ya declara **`D` pre-registrado como probable mientras `conf.06` siga abierto**, con `C` = *"exigiría reconciliar conf.06 primero"*. **Anótalo: FP-29 gatea la ficha R8.3 del Hito D.**

## Lo que este acto NO hace

- **No ejecuta la cascada al corpus.** Las adjudicaciones de `conf.02` y `conf.05` tocan entre siete y ocho archivos de `corpus/reports/`, `glosario` e `integrador`. Va en **acto sucesor**, y este acto le abre fila. Meter esa cascada aquí, con BARRIDO-2 escribiendo `canon/`, es cómo se producen las colisiones que llevan cinco.
- **No toca `FP-30`.** Mesa dijo *"a"* y el dato del repo dice que no hay siete escalas sino cuatro conceptos con siete grafías. **Sigue `ABIERTA`, sin cambio**, esperando la reformulación.
- **No cierra `FP-24`, `FP-31` ni `FP-33`.** Solo corrige cómo están descritas.
- **No adjudica ninguna fila nueva del Commit 2.**
- **No edita `canon/estado-programa-v1_10.md`** aunque le toque cascada. Perímetro de BARRIDO-2.

## Cierre

`python3 tests/check.py --baseline` **antes y después**, cifra en ambas. **T-FIRMAS va a imprimir las filas nuevas y las firmas: eso es señal, no defecto.** Al redactar: congelado `6f78d06`. Si sale ROJO por otra causa, **decláralo, no recongeles** — `--freeze` exige ADR de mesa (ADR-76(f)) y este acto no lo trae firmado.

Nota en `forense/notas/2026-08-17-registra-17ago.md` con cada comando y su salida cruda · una entrada en `forense/hallazgos.md` · este encargo marcado `CONSUMIDO` con su PR al cerrar · **merge local**, `origin/main` hacia la rama, editor web de conflictos **prohibido** · `git diff --check` · **jamás te auto-fusionas**.

**Contadores del programa que mueve: 0.** Mueve el tablero de 11 a 16 `FIRMADA` y abre cinco filas. Ningún contador de medición sobre México. **Dilo así, sin justificarlo.**
