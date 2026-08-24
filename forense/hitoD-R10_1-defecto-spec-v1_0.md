# HITO D · `R10.1` — dos defectos de la spec congelada, declarados y NO corregidos hacia atrás

### `hitoD-R10.1-defecto-spec` · **v1.0** · 20 de agosto de 2026 · TERCER COMMIT

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R10_1-defecto-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R10.1-defecto-spec`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | El tercer commit que el encargo de `RETRIAGE-4` prescribe para cuando la spec sale mal: *"Spec mal → tercer commit que lo dice. Nunca se corrige hacia atrás."* |
> | **QUÉ NO ES** | **No corrige la spec, no re-corre nada, no cambia el desenlace.** `R10.1` sigue en *"no adjudica"* (rama 4) y el contador sigue sin moverse por ella. **No reporta ninguna tasa corregida** — la razón está en §3 y es la más importante de este documento. |
> | **VERIFICAS ASÍ** | los dos defectos se sostienen citando la salida cruda ya commiteada (`forense/notas/2026-08-20-r10-1-rechazo-poder-salida.txt`), que trae las 12 transcripciones íntegras precisamente para esto. |

---

## 1 · Defecto 1 — la operacionalización léxica no mide el constructo que la ficha nombra

`hitoD-R10.1-especificacion §4.1` congeló: *"un rechazo se cuenta **indirecto** si el acto de rechazo se realiza sin una negación explícita (excusa, aplazamiento, alternativa, evasión); **directo** si contiene una negación explícita"*, y COMMIT B la operacionalizó como una **lista cerrada de cabezas de negación**. La auditoría a mano de las 12 transcripciones —que la spec obligó a imprimir para que fuera auditable— muestra que **la lista falla en las dos direcciones**.

### 1.1 · Cuenta como directas excusas mitigadas, que el marco del ancla codifica como indirectas

**`Rechazo 1` del escenario `Rechazos 3-4` (`+P`), marcado DIRECTO por la cabeza `no, no`.** El turno completo, verbatim de la salida cruda:

> **Empleado:** *"Pero, es que no me puedo quedar porque tengo otra otra este, cita, otra una cita digamos, y este tengo que llegar allá a las siete y media y no, pues no, no me puedo quedar."*

Es un rechazo **con excusa, mitigado, precedido de `pero` y `es que` y sostenido por una razón externa**. En la taxonomía de actos de habla que usa el propio estudio del que sale el ancla de la ficha (el 64% de Tlaxcala), **una excusa es una estrategia indirecta**; la cabeza directa es un `no` que funciona como negativa desnuda, no un `no puedo` incrustado en una justificación. Lo mismo ocurre con `Rechazo 5` (*"discúlpeme, pero yo no puedo ir porque tengo otro compromiso"*) y `Rechazo 6` (*"le voy a pedir que me disculpe porque no puedo… pero tengo planes con la familia"*), ambos `+P`, ambos marcados DIRECTO.

### 1.2 · Empareja negaciones que no son la cabeza del rechazo — y una donde ni siquiera hay rechazo

**`Rechazo 10` del escenario `Rechazos 9-10` (`−P`), marcado DIRECTO por la cabeza `No puedo`.** El turno que disparó la coincidencia:

> **Omar:** *"No puedo, lo que pasa es que son tres veces que la retraso."*

**Ese `No puedo` no se refiere a la invitación: se refiere a cambiar la cita con el dentista**, en respuesta a *"cambia la cita, no seas así"*. Y el desenlace de la interacción no es un rechazo en absoluto — Omar termina en *"si salgo antes, pues llego por allá"* y el anfitrión cierra con *"te espero, ¿eh?"*. **La transcripción está clasificada como rechazo directo por una negación que pertenece a otro objeto y en una interacción que quizá no contiene rechazo.**

### 1.3 · Qué queda de la medición

Las dos fallas van en direcciones opuestas y **no se cancelan de forma conocida**. Lo que se puede decir con certeza es lo único que se dice: **la cifra `3/6` contra `3/6` de COMMIT B no mide la tasa de rechazo indirecto en el sentido en que la ficha usa esa expresión.** El desenlace de COMMIT B —rama 4, no adjudica— **no cambia**, porque no dependía de la codificación sino del `n`: con seis observaciones por brazo, el IC95% de la diferencia mide ±56.58 pp y ninguna codificación imaginable lo habría llevado por debajo de 15.

---

## 2 · Defecto 2 — el árbol no tiene ruta de la rama 4 a la fila `C`

`hitoD-R10.1-especificacion §4.2` enruta cuatro ramas: dos a `A`/`B`, una a `D` y la cuarta a *"no adjudica"*. La corrida cayó en la cuarta. Pero la fila `C` de la ficha —*"exigiría replicación fuera de población universitaria — el ancla actual es Tlaxcala, universitarios"*— **describe exactamente lo que la corrida estableció por medición**: que el único instrumento mexicano en disco es universitario, elicitado, y con seis casos por brazo. **El árbol la dejó inalcanzable.**

**Precedente exacto, no invención:** `ADR-55` registró el mismo modo de falla el 4/ago/2026 con `R1.2` — *"ninguna fila de la escala propia (`A`-`D`) nombra 'el falsador corrió limpio y no se satisfizo, la regla sobrevive'… se declara como patrón, sin inventar fila nueva ni tocar la ficha"*. Y `ADR-58` nació de ahí: la escala ganó su fila `E` porque un registro que solo puede anotar refutaciones e inejecutables describe el estado de validación sesgado hacia abajo. **Este es el mismo defecto una versión más adentro: no falta una fila en la escala, falta una arista en el árbol que lleva a ella.**

---

## 3 · Lo que este commit deliberadamente NO hace, y es lo más importante que dice

**No recodifica las 12 transcripciones y no reporta ninguna tasa corregida.**

La razón no es falta de tiempo ni de competencia. Es que **quien recodificara ahora sería un codificador único, que ya vio el resultado bajo la regla equivocada, que conoce la hipótesis, y que sabe qué número haría quedar mejor al acto.** Un número producido en esas condiciones es exactamente lo que el pre-registro existe para impedir, y publicarlo con la etiqueta *"corregido"* sería peor que no publicarlo: llevaría la autoridad de una corrección sin ninguna de sus garantías.

**El precedente del programa manda en la misma dirección.** `A-bis` regla 2 lo dice para el condicionamiento — *"la corrección de la regla 1 no es 'el estratificado es el bueno'"* —, y la disciplina de `forense/` append-only lo dice para los archivos. Aquí la traducción es: **una spec mal escrita se sucede, no se parchea en caliente.**

---

## 4 · El sucesor, especificado para que no haya que re-derivarlo

`hitoD-R10.1-especificacion-v2_0` — **no escrita en este acto**, y con estos cuatro requisitos:

1. **Esquema de codificación pragmática, no léxico**: acto nuclear (*head act*) separado de sus adjuntos, con la taxonomía del marco del que sale el ancla de la ficha (directo / indirecto por excusa, aplazamiento, alternativa, evasión), y **la regla de qué hacer con las interacciones que no terminan en rechazo** — que `Rechazo 10` demuestra que existen en el corpus.
2. **Segundo codificador independiente**, con acuerdo entre codificadores reportado. Con 12 unidades es barato, y sin él ninguna tasa de este corpus es defendible.
3. **Arista explícita de "medido pero sin potencia" a la fila `C`**, para que el desenlace tenga dónde anotarse.
4. **Declaración de techo, escrita antes**: con `n`=6 por brazo, **ninguna codificación puede resolver una diferencia de 15 pp**. La spec v2.0 debe decir eso en su primera página, o repetirá este acto con mejor coloración y el mismo resultado. **Si el objetivo es adjudicar `R10.1`, el camino no es recodificar 12 transcripciones: es conseguir más rechazos mexicanos con los dos brazos** — y la candidata sigue siendo PRESEEA, `NO-ACCESIBLE` desde el 5/ago/2026 y ausente del corpus, verificado en `T0` de este acto.

---

## 5 · Contabilidad de este commit

No mueve el contador. No propone fila. No toca `hitoD-preregistro`. No toca `milpa/` ni el tier de `R10.1`. No edita `hitoD-R10.1-especificacion` ni `hitoD-R10.1-veredicto`: los dos quedan como se escribieron, que es lo que los hace prueba de qué se supo y cuándo.

---

**el primer resultado que produjo este procedimiento es el que se reportó, y este documento dice por qué ese procedimiento estaba mal — sin sustituir el resultado.**
