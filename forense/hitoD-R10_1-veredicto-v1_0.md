# HITO D · `R10.1` — el falsador corrido, y por qué no adjudica

### `hitoD-R10.1-veredicto` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R10_1-veredicto-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R10.1-veredicto`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT B) de `hitoD-R10.1-especificacion`, ejecutada sin desviación: los dos brazos de poder contados, codificados por la regla congelada, y la decisión contra el árbol. |
> | **QUÉ NO ES** | **No propone ninguna fila.** Cae en la rama 4 del propio árbol: no adjudica. No mueve el contador. |
> | **VERIFICAS ASÍ** | `python3 tests/hitod_r10_1_rechazo_poder.py`; salida cruda con **las 12 transcripciones íntegras** en `forense/notas/2026-08-20-r10-1-rechazo-poder-salida.txt`, para que la codificación se audite a mano y no se crea bajo palabra. |

**ESTAMPA DE UNIVERSO (`A.10`).** Sello tomado sobre `origin/main = 54da215`, 20/ago/2026, entorno **UBUNTU**. Universo examinado: las **tres** páginas del corpus Brasdefer en disco, verificadas `COINCIDE`. Dentro de ellas, la sección `Rechazos` de `actos_de_habla.html` (líneas 145–708 del texto plano, **563 líneas**), y dentro de ella el bloque de **México** (**197 líneas**). Denominador del universo de instrumentos: **no existe** — PRESEEA, la otra candidata que `CONF-17` nombró, no está en el corpus (`command grep -ic preseea data/manifiesto.yaml` → **0**, con control positivo `ENIF` → **95**).

---

## 1 · Lo primero que hay que reportar: el reconocimiento de COMMIT A era falso

`hitoD-R10.1-especificacion §1` declaró, antes de congelar: *"los rechazos mexicanos del corpus **parecen ser pocos y llevar un solo código de poder**"*. **La corrida lo refuta.**

El corpus documenta rechazos de **cuatro** países (México, Costa Rica, República Dominicana, España), y el bloque de México tiene **seis escenarios** y **doce transcripciones**, repartidas **exactamente mitad y mitad** entre los dos brazos:

| escenario | código de poder | interacción |
|---|:---:|---|
| Rechazos 1-2 | **+P** | Estudiante y asesor: rechaza la sugerencia del asesor de tomar una clase |
| Rechazos 3-4 | **+P** | Jefe y empleado: rechaza la petición del jefe de quedarse más tiempo |
| Rechazos 5-6 | **+P** | Jefe y empleado: rechaza la invitación del jefe a una cena |
| Rechazos 7-8 | **−P** | Amigos: rechaza la petición de prestar los apuntes |
| Rechazos 9-10 | **−P** | Amigos: rechaza la invitación al cumpleaños |
| Rechazos 11-12 | **−P** | Amigos: rechaza la sugerencia de ir a un bar |

**Seis transcripciones por brazo.** `W2` —la pieza que la spec llamó *"la pieza dura"*— **está cubierta**. La rama 3 del árbol (brazo vacío → `D`) **no aplica**, y con ella cae la lectura que este ejecutor traía del reconocimiento.

**Por eso la declaración de §1 no era adorno.** Si el reconocimiento se hubiera dado por bueno sin correr, esta ficha habría archivado un `D` falso y el contador se habría movido con una cifra inventada. **El acto que lo evitó fue escribir lo que se creía saber, y después medirlo.**

---

## 2 · La codificación, y el resultado bajo la regla congelada

Regla de COMMIT A §4.1, operacionalizada como lista cerrada de cabezas de negación explícita (`no puedo` · `no voy a` · `no quiero` · `no me interesa` · `no gracias` · `no, no` · `imposible` · `me niego` · `no podré` · `no va a poder` · `no cuentes conmigo` · `no voy` · `no la voy` · `no lo voy`):

| brazo | indirectos / total | tasa | IC95% Jeffreys |
|---|---|---|---|
| **+P** (interlocutor superior) | **3 / 6** | **50.00 pp** | [16.68, 83.32] |
| **−P** (interlocutor par) | **3 / 6** | **50.00 pp** | [16.68, 83.32] |

| | valor |
|---|---|
| **diferencia (+P − −P)** | **0.00 pp** |
| **EE Wald** | **28.87 pp** |
| **IC95%** | **[−56.58 pp, +56.58 pp]** |
| **Fisher exacto 2×2** | **p = 1.0000** |
| tabla [indirecto, directo] | +P `[3, 3]` · −P `[3, 3]` |

**Diseño aplicado: ninguno, y está declarado desde COMMIT A §3.** No hay `FAC_*`, `EST_DIS` ni `UPM_DIS` porque el corpus es una colección de interacciones elicitadas sin marco muestral. **Las dos tasas son proporciones muestrales no probabilísticas** y así se rotulan; el IC es binomial (Jeffreys por brazo, Wald para la diferencia) e informa sobre incertidumbre de conteo, **no** sobre generalización.

**Control de que no se dejó nada fuera:** las otras dos páginas del corpus no contienen ni una marca de rechazo — `encuentros_de_servicio.html` (3,096 líneas) → **0**; `convelic_conversaciones.html` (198 líneas) → **0**; con **control positivo del mismo patrón** sobre `actos_de_habla.html` → **51** marcas. El negativo se declara con su control al lado.

---

## 3 · Decisión contra el árbol congelado

**Rama 4 → NO ADJUDICA.** El punto (0.00 pp) **satisface** la condición de la fila `A` (*"<15 puntos en muestra mexicana"*), y el IC95% **no la despeja**: cruza el umbral de 15 pp por ambos lados y por un margen enorme. Es exactamente el caso que la contraparte del Bloque `A-bis` gobierna — *"un punto estimado que satisface un umbral con un intervalo de confianza que no lo despeja no adjudica; se reporta como propuesta con la reserva escrita"* — y que la propia spec pre-registró como rama 4 antes de ver el dato.

**Ninguna fila se propone.** Ni `A` (el IC no la sostiene), ni `B` (exige diferencia presente; la diferencia medida es exactamente cero), ni `C` ni `D` (el árbol no las enruta desde esta rama — ver §5). **`R10.1` sigue abierta**, ahora con una corrida archivada en vez de un hueco.

**Y hay que decir lo que un cero no dice.** Una diferencia de 0.00 pp con `n`=6 por brazo **no es evidencia de que `face` no opere**: es la ausencia de precisión para detectar nada. Con estos tamaños, ni una diferencia real de 30 puntos habría salido significativa. Leer este cero como *"el driver no es `face` situado"* —que es lo que la fila `A` afirmaría— sería el error que la contraparte de `A-bis` existe para impedir.

**No se compara contra el 64% del ancla, y la razón es de regla, no de prudencia.** La ficha cita *"64% de rechazo indirecto en universitarios de Tlaxcala"*, de un estudio publicado con su propio esquema de codificación pragmática. Las tasas de arriba salen de un proxy léxico aplicado a 12 transcripciones. **Son escalas distintas del mismo constructo y compararlas está prohibido por `A-bis r3`.** No se escribe *"medimos 50% contra el 64% publicado"*: sería un error de categoría, no una medición.

---

## 4 · Lo que la ficha apostó, y cómo salió

La fila `D` de `R10.1` dice *"improbable: el diseño es replicable"*. **La apuesta acertó, y por una razón distinta de la que suponía.** No hubo `D`: no porque alguien replicara el estudio, sino porque **el corpus del propio autor del ancla ya tenía los dos brazos en disco desde el 18/ago/2026**, adquirido por `ACTO ADQ-15` para otra palanca (`N15,N31`), y nadie lo había cruzado con `R10.1`.

Lo que la ficha **no** anticipó es que el instrumento existiera y aun así **no alcanzara**: `W1`, `W2`, `W3` y `W4` están cubiertas las cuatro, y el falsador de todos modos no puede decidir. **La pieza que falta no es un brazo ni una variable: es `n`.**

---

## 5 · Un hueco del árbol de esta spec, nombrado aquí y tratado en commit propio

La rama 4 envía este desenlace a *"no adjudica"* y ahí lo deja. Pero la fila `C` de la ficha —*"exigiría replicación fuera de población universitaria — el ancla actual es Tlaxcala, universitarios"*— **describe con precisión lo que esta corrida acaba de establecer por medición**, y el árbol congelado **no tiene ninguna ruta que lleve de la rama 4 a `C`**. Es un hueco de la spec, no del dato.

**No se corrige hacia atrás.** El árbol se aplicó como estaba y el desenlace es el que dice. El hueco se declara en un **tercer commit propio** de este acto, con el precedente que la doctrina ya fijó para esta situación (`ADR-55`, `R1.2`/Nota 19: *"ninguna fila de la escala propia nombra este desenlace… se declara como patrón, sin inventar fila nueva ni tocar la ficha"*).

---

## 6 · Módulo de auditoría de rigor extremo

**¿Qué sobregeneraliza desde clases medias urbanas?** Todo el instrumento, y no se disimula: seis escenarios de role-play entre universitarios y empleados de oficina en Tlaxcala. La fila `C` de la ficha ya lo decía del ancla; ahora también es cierto del único instrumento en disco.

**¿Qué parece psicológico pero es un incentivo racional?** La indirección hacia arriba. Rechazar al jefe con una excusa en lugar de un "no" protege el empleo, no solo el *face*. El falsador de esta ficha no puede separar esos dos, y con `n`=6 no podría aunque el diseño fuera perfecto.

**¿Qué evidencia es débil pero con intuición social fuerte?** Exactamente esta. *"El mexicano no dice que no"* es una de las creencias más firmes del corpus popular, y el único dato mexicano en disco para probarla son **12 conversaciones**.

**¿Qué afirmación describe el estado del corpus y no fue derivada?** Ninguna. Y una que **sí** estaba escrita a mano y resultó falsa se corrige en §1: el reconocimiento de COMMIT A §1 sobre "un solo código de poder", refutado por la corrida en el mismo acto que lo declaró.

---

**el primer resultado que produjo este procedimiento es el que se reporta.**
