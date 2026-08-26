# HITO D · `R10.1` — corrida de la spec sucesora v2.0: `κ`, consenso y recuento

### `hitoD-R10.1-corrida-v2_1` · Fase B de `ACTO CORRE-R10.1-v2` · 26 de agosto de 2026 · ENTORNO UBUNTU

> | | |
> |---|---|
> | **QUÉ ES** | La corrida completa de `hitoD-R10.1-spec-v2_0-propuesta` (SELLADA, `FP-128`) sobre las 12 transcripciones mexicanas del corpus Brasdefer: revela la codificación 1 sellada en la Fase A, ingesta verbatim la codificación 2 de **Jonatan Guadarrama**, calcula **Cohen's `κ`** en dos niveles, aplica el gate de `§3.4`, resuelve por consenso las tres discrepancias, cuenta las tasas por brazo excluyendo `NO-RECHAZO` (`§2.5`) y recorre el árbol de `§4.1`. |
> | **QUÉ NO ES** | No adjudica nada fuera de la escala `§6`. No toca `PRESEEA`. No edita la spec ni los tres documentos `v1` de `R10.1` (append-only, `ADR-40`). No corre dos veces: **el primer resultado que produjo el procedimiento es el que se reporta**. |
> | **VERIFICAS ASÍ** | `python3 tests/hitod_r10_1_kappa_v2_1.py` — cómputo puro, sin corpus ni red; salida cruda íntegra en `forense/notas/2026-08-26-r10-1-corrida-v2_1-salida.txt`. |

**Resultado, dicho primero: fila `C`.** `κ`(Nivel 1, 12) = **0.7209** — el gate aprueba. Diferencia
entre brazos = **66.67 pp**, y los dos intervalos al 95% **cruzan** el umbral de 15 pp. Rama 4 del
árbol → fila `C`, con registro simultáneo de *"no adjudica"* bajo `A-bis`. **Es exactamente el
desenlace que `§5.2` predijo por escrito antes de correr.**

---

## 1 · El sello de la Fase A se abre y coincide

La codificación 1 se comprometió por `sha256` el 25/ago/2026, **antes** de que existiera la
codificación 2. Hoy se revela el texto en claro y se re-mide:

| objeto | `sha256` sellado en `hitoD-R10_1-codificacion1-v2_1.md §1` | re-medido hoy | |
|---|---|---|---|
| tabla de los 12 códigos | `dae1048d…33ec90` | `dae1048d…33ec90` | **COINCIDE** |
| razonamiento unidad por unidad | `c380f81e…2605d2` | `c380f81e…2605d2` | **COINCIDE** |
| paquete entregado al codificador 2 | `15e1a594…fda1bd` | `15e1a594…fda1bd` | **COINCIDE** |
| material de origen | `c5d39e81…9ca59d` | `c5d39e81…9ca59d` | **COINCIDE** |

Los dos primeros viven fuera del repositorio, en `/home/pc0/mm-corre-r10-1-SELLO/`, por la razón
que la Fase A declaró: el segundo codificador es una persona con acceso plausible a este
repositorio, y publicar los códigos durante el interludio habría abierto el canal de
contaminación que anula el `κ`.

## 2 · Ingesta verbatim de la codificación 2

Mesa adjuntó la tabla al relanzamiento del 26/ago/2026 con la línea de compuerta que `F0-B` exige,
verbatim: *«Códigos del codificador 2 adjuntos, transcritos sin edición.»* Se transcribe **sin
edición**, incluida la columna de notas del codificador:

| unidad | Nivel 1 | Nivel 2 | nota (verbatim de Jonatan Guadarrama) |
|---|---|---|---|
| U01 | NO-RECHAZO | NO-RECHAZO | No cierra con rechazo consumado; termina en acuerdo de analizar conjuntamente. El estudiante pospone sin resolver hacia el rechazo. |
| U02 | NO-RECHAZO | NO-RECHAZO | Pregunta sobre posibilidad de aplazamiento ("¿qué posibilidades hay de que la pueda yo posponer?") pero no rechaza; cierra con aceptación de discutir después. |
| U03 | INDIRECTO | EXCUSA | "no me puedo quedar porque tengo otra cita" — negación + razón externa en la misma cláusula. Aplica regla 2.3. |
| U04 | INDIRECTO | ALTERNATIVA | Propone hacer la mitad hoy y continuar el lunes: "¿qué le parece si nos quedamos a hacer, digamos, la mitad y el lunes tempranísimo estaría yo aquí para continuar?" |
| U05 | INDIRECTO | EXCUSA | "no puedo ir porque tengo otro compromiso" — negación + razón externa. Rechazo justificado mediante obstáculo externo. |
| U06 | INDIRECTO | EXCUSA | "no puedo, no voy a poder asistir...tengo planes con la familia" — negación + razón externa (planes previos con familia). |
| U07 | NO-RECHAZO | NO-RECHAZO | No tiene los apuntes ahora, pero ofrece traerlos mañana. Cierra con aceptación: acuerdan hora y lugar de encuentro. |
| U08 | NO-RECHAZO | NO-RECHAZO | Propone estudiar juntos o que copie las notas; Omar acepta con "Pos órale". Cierra en aceptación, no rechazo. |
| U09 | DIRECTO | DIRECTO | "de todas maneras te voy a decir que no, la verdad que no puedo, así te digo que no voy a poder ir" — negación explícita y performativa en el turno final, sin razón externa acompañándola en ese turno. |
| U10 | NO-RECHAZO | NO-RECHAZO | "si salgo antes, pues llego por allá" — cierra con incertidumbre condicional ("maybe si salgo temprano"), no con rechazo identificable. |
| U11 | INDIRECTO | EXCUSA | "No...no acabo de comer, y la clase empieza en diez minutos" + "no puedo...no me gusta salir de mi clase" — negaciones + razones externas/personales. |
| U12 | INDIRECTO | EXCUSA | Rejection realizado mediante razones: "voy retrasado en esta materia" y "primero los deberes" — el rechazo es implícito en la razón externa que lo justifica. |

**`sha256` de la ingesta, en forma canónica de tres columnas** (`unidad·nivel1·nivel2`, TSV, el
mismo formato en que se selló la codificación 1, sin la columna de notas):
`9aea0aed1371ae4eb0c6730b6e0c6751d2c497b5820015032d1739669d9955f9`.
El de la codificación 1 en ese mismo formato canónico es
`911f995d3e619bd988915e3ad37451d3517c69f3b6ec0e07f0f8def9482add62`; `diff` entre ambos devuelve
**3 filas distintas** — `U02`, `U11`, `U12` —, control que coincide con el conteo de discrepancias
de `§3`.

**Preguntas del codificador antes de entregar:** mesa dejó esa ranura del relanzamiento **sin
llenar** (ni texto ni «ninguna»). No condiciona ninguna compuerta; se declara aquí como hueco de
procedencia, no se rellena por inferencia.

## 3 · `κ` de Cohen, dos niveles (spec `§3.3`)

| universo | nivel | `κ` | `Po` | `Pe` |
|---|---|---|---|---|
| **12 — el gate** | **Nivel 1** (directo · indirecto · `NO-RECHAZO`) | **0.7209** | 0.8333 (10/12) | 0.4028 |
| 12 | Nivel 2 (los cuatro subtipos + `NO-RECHAZO`) | 0.6571 | 0.7500 (9/12) | 0.2708 |
| 11 — diagnóstico, sin `U10` | Nivel 1 | 0.6901 | 0.8182 (9/11) | 0.4132 |
| 11 — diagnóstico, sin `U10` | Nivel 2 | 0.6333 | 0.7273 (8/11) | 0.2562 |

**Matriz de confusión, Nivel 1** (filas codificador 1, columnas codificador 2):

| | DIRECTO | INDIRECTO | NO-RECHAZO |
|---|---|---|---|
| **DIRECTO** | 1 | 1 | 0 |
| **INDIRECTO** | 0 | 5 | 1 |
| **NO-RECHAZO** | 0 | 0 | 4 |

**La reserva pre-registrada se resuelve sola.** La Fase A anticipó, sin conocer nada, que `U10`
llega **pre-decidida a ambos codificadores** —la regla `2.5` la nombra dentro del propio esquema, y
el esquema viajó verbatim en el paquete— y ordenó reportar `κ` sobre 12 y sobre 11. **Los cuatro
valores caen del mismo lado de 0.60**, así que la distinción no cambia el veredicto. El acuerdo en
`U10` no es evidencia de acuerdo, y aun descontándolo el gate sigue aprobando.

## 4 · Gate (spec `§3.4`)

`κ`(Nivel 1, 12) = **0.7209 ≥ 0.60** — acuerdo **sustancial** en la escala de Landis & Koch
(0.61–0.80). **El gate aprueba: se habilita el conteo por consenso**, sin tercer codificador. No
hay `D` de instrumento. El Nivel 2 se reporta aunque el Nivel 1 apruebe, y es diagnóstico, no gate.

## 5 · Consenso, unidad por unidad (spec `§3.4`)

Nueve de las doce unidades coinciden en los dos niveles y no requieren consenso: `U01` `U03` `U04`
`U05` `U06` `U07` `U08` `U09` `U10`. Las tres restantes se resuelven con **las dos codificaciones a
la vista**, y **las tres estaban pre-declaradas** por el codificador 1 en el texto sellado como
candidatas a discrepancia (candidatos 1, 3 y 4 de cuatro; el candidato 2, `U05`, no se materializó).

**`U02` — cod1 `INDIRECTO/APLAZAMIENTO` · cod2 `NO-RECHAZO` → consenso `NO-RECHAZO`, a favor de cod2.**
El estudiante nunca niega: pregunta por la posibilidad de posponer, y la interacción cierra con él
**aceptando** la contrapropuesta del asesor (*"Te parece que lo analicemos con calma y lo platicamos
en otra ocasión"* / *"Me parece bien"*). Satisface dos gatillos literales de `2.5` — *"termina
aceptando"* y *"aplazando sin resolver hacia el rechazo"*. La objeción que el codificador 1 dejó
escrita —que aplicar `2.5` aquí vaciaría al subtipo hermano `APLAZAMIENTO` de `2.2`— es un argumento
de **diseño del esquema**, no evidencia sobre este turno: `2.2` conserva los casos en que el
aplazamiento del rechazante es la última palabra y el peticionario desiste, que no es lo que pasa
aquí. **Esta resolución mueve el denominador:** el brazo `+P` baja de 5 a 4 codificables.

**`U11` — cod1 `DIRECTO` · cod2 `INDIRECTO/EXCUSA` → consenso `DIRECTO`, a favor de cod1.**
Por la prueba de remoción de `2.1`, el acto nuclear es el **último** turno de Lisandro (*"Me cay que
no puedo, guey, por más que intente, no.."*), tras el cual Jorge desiste; su primer turno (*"todavía
no acabo de comer, y la clase empieza en diez minutos"*) **no consuma el rechazo** —Jorge insiste
cuatro turnos más—, así que las razones externas que cod2 cita son adjuntos de un segmento distinto
del acto nuclear. La razón adyacente al acto nuclear sí existe, pero es **interna** (*"yo soy medio
seso, pues no me gusta salir de mi clase"*), y `2.2`/`2.3` exigen razón **externa** para que una
negación deje de contar como directa. La propia nota de cod2 las rotula *"externas/personales"*.
**Reserva:** el veredicto de esta unidad descansa en dos lecturas declarables —que la prueba de
remoción selecciona el último turno, y que la disposición personal no es razón externa—; si
cualquiera de las dos se invirtiera, `−P` pasaría de 1/3 a 2/3 y la diferencia caería a 33.33 pp,
**sin cambiar la fila**, porque el IC seguiría cruzando 15 pp.

**`U12` — cod1 `INDIRECTO/ALTERNATIVA` · cod2 `INDIRECTO/EXCUSA` → consenso `ALTERNATIVA`, a favor de cod1.**
Nivel 1 ya coincidía, así que **esta discrepancia no mueve ni el denominador ni la tasa**. Se
resuelve a `ALTERNATIVA` porque el cierre de Jorge —*"Pues, sale, entons' te espero"*— responde a la
opción que Omar ofreció (*"ve tú y yo te alcanzo, termino mi clase"*), no a la razón. **Reserva:** la
lectura `EXCUSA` de cod2 (*"voy retrasado en esta materia"*, *"primero los deberes"*) es defendible.

**Balance del consenso:** una discrepancia se resuelve a favor del codificador ciego y dos a favor
del codificador 1 —una de ellas sin efecto sobre el conteo—. La única que mueve el número lo mueve
**en contra** de la hipótesis del codificador 1, que había codificado `U02` como rechazo indirecto
en el brazo `+P`.

## 6 · Cobertura del universo y exclusiones por `2.5` (spec `§6`)

Se reportan, no se descartan en silencio:

| brazo | transcripciones | codificables como rechazo | `NO-RECHAZO` excluidas del denominador |
|---|---|---|---|
| `+P` | 6 | **4** | `U01`, `U02` |
| `−P` | 6 | **3** | `U07`, `U08`, `U10` |

- `U01` — `2.5 (a)`, termina aceptando: *"ya si la tengo que tomar, pues la tomo"*.
- `U02` — `2.5` **por consenso** (ver `§5`): cierra aceptando *"lo analicemos con calma"*.
- `U07` — `2.5 (a)`, termina aceptando: acuerdan hora y lugar para los apuntes.
- `U08` — `2.5 (a)`, termina aceptando: *"Pos órale"*.
- `U10` — `2.5` nombrada **en la propia regla** (`Rechazo 10`): *"si salgo antes, pues llego"*.

**Cinco de las doce unidades del universo pre-registrado no son rechazos consumados.** Es el
hallazgo de validez que la Pieza 1 existía para producir: la regla léxica de `COMMIT B` las contaba
todas.

## 7 · Tasas, diferencia, intervalo y rama del árbol (spec `§4.1`)

| brazo | indirectos / codificables | tasa | IC95% Wilson |
|---|---|---|---|
| `+P` | 4 / 4 | **100.00 pp** | [51.01, 100.00] |
| `−P` | 1 / 3 | **33.33 pp** | [6.15, 79.23] |

- **Diferencia (`+P` menos `−P`): 66.67 pp.**
- `IC95%` **Wald**: **[13.32, 120.01]** — **cruza** 15 pp.
- `IC95%` **Newcombe** (híbrido de Wilson): **[−0.47, 93.85]** — **cruza** 15 pp.
- Fisher exacto 2×2, `p = 0.1429`. Tabla `[indirecto, directo]`: `+P [4, 0]` / `−P [1, 2]`.

**Por qué se reportan dos intervalos y no uno.** Con `p̂(+P) = 1.00` el término Wald de ese brazo es
**exactamente cero**, y Wald es conocido por fallar en el borde: el intervalo Wald de arriba está
**estrechado por un artefacto**, no por potencia — de hecho es más angosto que el techo de ±56.58 pp
que `§5.1` declaró. Reportar solo Wald sería reportar una precisión que no existe. Newcombe no
degenera y da el intervalo honesto. **Los dos cruzan el umbral, así que la rama no depende de cuál
se prefiera.**

**RAMA 4 → fila `C`.** Los dos brazos existen con denominador, el `IC95%` cruza 15 pp, y el ancla
del falsador es población **universitaria y elicitada** (role-play, Brasdefer/México).

- `§4.2` — se registra **también** como *"no adjudica"* bajo `A-bis`: son respuestas a preguntas
  distintas. `A-bis` dice **qué hace el número** (no decide); `C` dice **qué haría falta**
  (replicación fuera de población universitaria).
- `§4.3` precedencia 4 — `C` manda sobre *"no adjudica"* puro porque el IC cruza el umbral **y** el
  instrumento es universitario/elicitado. No es rama 5.
- `§6` bloque `B-bis` — `corroborada` está excluida por diseño para este instrumento;
  *"falsador demasiado débil"* (`D`) **no** aplica, porque ningún brazo quedó vacío (4 y 3). No hay
  `D` de instrumento porque el gate de `κ` aprobó.

## 8 · El techo de `n` viaja escrito, y empeoró

`§5.1` declaró **±56.58 pp** suponiendo `n=6` por brazo y las dos tasas en 50%. Los denominadores
**reales**, tras excluir las cinco `NO-RECHAZO` por `2.5`, son **`+P` n=4 y `−P` n=3**. El techo se
cumple y se agrava: la regla que corrigió la **validez** recortó la **potencia**. El semiancho
Newcombe hacia abajo es **67.13 pp**.

`§5.2` lo dijo antes de correr, verbatim: *si la corrida vuelve a caer en rama 4/5 con el mismo
corpus, eso no es una falla de la spec v2.0, es la confirmación de lo que este párrafo ya predijo.*
**Corregir la codificación sube la validez de constructo; no compra `n`.** Adjudicar `R10.1` a `A` o
`B` exige más rechazos mexicanos con los dos brazos de poder — la candidata nombrada es `PRESEEA`,
`NO-ACCESIBLE` desde `CONF-17` (5/ago/2026), heredada sin re-verificar por `§5.3` y no reabierta
aquí.

## 9 · Reservas del veredicto, todas juntas

1. **El techo de `n`** — `+P` n=4, `−P` n=3. Ninguna recodificación cierra ese intervalo.
2. **La asimetría entre codificadores**, declarada en la Fase A y no disimulada: el codificador 2 es
   ciego; el codificador 1 **no** lo es, porque el material de origen trae la codificación `v1` y su
   resultado en el mismo archivo. El `κ` de 0.7209 se lee con esa asimetría pegada.
3. **`U11`** — la resolución descansa en dos lecturas declarables (`§5`). Invertirlas cambia la
   diferencia de 66.67 a 33.33 pp y **no** cambia la fila.
4. **`U12` Nivel 2** — la lectura `EXCUSA` de cod2 es defendible; no afecta el conteo.
5. **El `κ` de Nivel 2 (0.6571)** roza el umbral más de cerca que el de Nivel 1. Es diagnóstico por
   spec, no gate, pero indica que los **subtipos** de indirecto son menos reproducibles que la
   distinción gruesa.
6. **Wald degenera** en `p̂=1`; el intervalo que manda para leer precisión es Newcombe.
7. **La ranura de preguntas del codificador** quedó sin llenar por mesa (`§2`).

## 10 · Desviación de forma en el relanzamiento, declarada

El mensaje de relanzamiento traía la `RANURA-TABLA` **vacía** (doce filas de `___`) y la tabla real
**concatenada al final del mensaje**, fuera del hueco previsto. La compuerta `F0-B` se lee
satisfecha —la línea exigida está presente verbatim y la tabla de 12 filas existe, completa, con
notas por unidad que solo un codificador puede producir—, así que **no** es el caso de
`FP-63`/autocaptura verbatim que hizo parar al `v2` en su primera redacción: allí no había dato
ninguno, aquí lo hay y es inequívoco. Se declara la desviación de forma para que la auditoría la vea
sin tener que reconstruirla.

---

**Instrumento:** `tests/hitod_r10_1_kappa_v2_1.py` (cómputo puro; extiende el patrón de
`tests/hitod_r10_1_rechazo_poder.py` como `B2` ordena). **Salida cruda íntegra:**
`forense/notas/2026-08-26-r10-1-corrida-v2_1-salida.txt`.
