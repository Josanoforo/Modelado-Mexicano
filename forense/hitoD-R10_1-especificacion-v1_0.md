# HITO D · Falsador `R10.1` — especificación pre-registrada, congelada antes de contar nada

### `hitoD-R10.1-especificacion` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R10_1-especificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R10.1-especificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada (COMMIT A) del falsador de `R10.1`: las cuatro piezas que exige, universo, ponderador y diseño, dicotomización, escala con precedencia, y qué significa que el falsador NO refute. |
> | **QUÉ NO ES** | **No trae ni una cifra producida por este acto.** No adjudica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | el árbol y la precedencia están completos antes de la corrida; y el reconocimiento previo del instrumento está declarado en §1, no escondido. |

**Acto:** `ACTO RETRIAGE-4`, 20/ago/2026, entorno **UBUNTU**, sobre `origin/main = 54da215`.

---

## 0 · Ficha bajo prueba, verbatim (`hitoD-preregistro-v2_0.md:279-287`)

> **R10.1 · Rechazo → indirecto `[FUERTE]`**
> SI hay que emitir un rechazo ENTONCES se hace indirecto — PORQUE preservación de face + simpatía *(Félix-Brasdefer, muestra en México)*
>
> **La mejor anclada del dominio:** dato **(a)**, muestra en México, 64% de rechazo indirecto en universitarios de Tlaxcala. ⚠️ **Pero `simpatía` es (b)** — el `PORQUE` mezcla procedencias.
>
> **Falsador — separa los dos drivers.** Si el driver es **face**, la indirección debe **variar con la asimetría de poder** (más hacia arriba, menos hacia abajo). Si es **simpatía** como rasgo, debe ser **constante**. *El propio corpus dice que la asertividad fluye hacia abajo y la indirección hacia arriba* — lo que ya favorece face sobre rasgo.
> **Umbral.** Diferencia en tasa de rechazo indirecto entre interlocutor superior e inferior **<15 puntos** → el driver no es face situado, y `simpatía` **(b)** quedaría sin sustituto **(a)**.
>
> **A** <15 puntos en muestra mexicana · **B** diferencia presente en muestra estudiantil no generalizable · **C** exigiría replicación fuera de población universitaria — **el ancla actual es Tlaxcala, universitarios** · **D** improbable: el diseño es replicable.

---

## 1 · Lo que este ejecutor ya vio antes de congelar — el reconocimiento más invasivo de las cuatro fichas

Aquí la declaración pesa más que en las otras tres, porque **el reconocimiento tocó ya el borde de la medición** y ocultarlo haría de esta spec una ficción:

1. Se extrajo el texto plano de las tres páginas Brasdefer y se contó su longitud.
2. Se listaron los **códigos de distancia y poder** que aparecen en `actos_de_habla.html` (`(+D, +P)`, `(-D, -P)`, …) y se leyó el encabezado del bloque *"México: Transcripción & audios — Rechazos 1-2"*.
3. Se listaron los rótulos `Rechazo N:` y `Petición N:` con su descripción de una línea.

**Lo que eso ya reveló, y por tanto se declara antes de que la corrida lo confirme:** los rechazos mexicanos del corpus parecen ser **pocos** y llevar **un solo código de poder**. Si la corrida lo confirma, **este acto no puede reclamar haberlo descubierto ciegamente** — lo vio en reconocimiento y lo escribe aquí. Lo que la corrida sí aporta es el **conteo exacto por brazo**, que es lo que decide la fila, y ese conteo no se ha hecho.

4. Se verificó que `data/manifiesto.yaml` no contiene la cadena `preseea` (`command grep -ic` → 0, con control positivo `ENIF` → 95). PRESEEA es la candidata que `CONF-17` clasificó `NO-ACCESIBLE`.

---

## 2 · Qué exige el falsador, desarmado en piezas verificables

| # | pieza | por qué es indispensable |
|---|---|---|
| **W1** | **Rechazos codificados por directez** (directo / indirecto) | el desenlace de la regla |
| **W2** | **Asimetría de poder con LOS DOS BRAZOS**: interlocutor superior (`+P`) **e inferior** (`−P`) | el Umbral es una **diferencia** entre dos tasas; con un brazo vacío no hay diferencia que calcular, no importa cuán grande sea el otro |
| **W3** | **Denominador por brazo**: rechazos totales emitidos hacia cada tipo de interlocutor | sin denominador no hay tasa, y el Umbral está en puntos porcentuales |
| **W4** | **Muestra mexicana** | la ficha lo dice literal; los otros países del corpus no cuentan |

**`W2` es la pieza dura, y se dice antes de contar:** una diferencia entre dos tasas exige **dos** tasas. Si el corpus solo documenta rechazos hacia arriba, el falsador no está *"mal medido"* — **no está medido en absoluto**.

---

## 3 · Universo, ponderador y diseño

**Universo pre-registrado:** los rechazos de habla mexicanos documentados en las tres páginas del corpus Brasdefer en disco — `adq15_brasdefer_actos_de_habla`, `adq15_brasdefer_convelic_conversaciones`, `adq15_brasdefer_encuentros_de_servicio` —, los tres verificados `COINCIDE` en `T0` de este acto.

**Ponderador: NO HAY, y no por omisión del corpus sino por su naturaleza.** El encargo pide declarar `FAC_*`, `EST_DIS`, `UPM_DIS`. **Ninguno existe ni podría existir**: el corpus es una colección de **interacciones elicitadas** (role-play) y encuentros grabados, recogidas y transcritas por un autor, sin marco muestral, sin probabilidad de selección conocida y sin diseño complejo. **Ninguna tasa que salga de aquí es poblacional**, y ninguna se reportará como si lo fuera. Lo que se puede calcular es una **proporción muestral no probabilística**, y así se rotula.

**Consecuencia declarada antes de correr:** aunque los dos brazos existieran, **no habría error estándar de diseño**. El IC que se reportaría sería binomial exacto sobre una muestra de conveniencia — informativo sobre la incertidumbre de conteo, mudo sobre generalización. Es exactamente lo que la fila `B` de la ficha ya anticipa.

---

## 4 · Dicotomización, árbol y precedencia — fijados al sellar

### 4.1 · Dicotomización

- **Indirecto / directo:** un rechazo se cuenta **indirecto** si el acto de rechazo se realiza sin una negación explícita (excusa, aplazamiento, alternativa, evasión); **directo** si contiene una negación explícita. Es la dicotomía estándar del propio marco de Félix-Brasdefer y la que la ficha usa al citar el 64%.
- **Superior / inferior:** por el código de poder que el propio corpus asigna a la interacción — **`+P`** cuando el interlocutor tiene más poder que quien rechaza, **`−P`** cuando tiene menos o igual. **No se recodifica a ojo**: se toma el código del corpus.
- **Corte del Umbral:** **|tasa(+P) − tasa(−P)| < 15 puntos porcentuales**.

### 4.2 · Árbol de decisión

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Los dos brazos existen con denominador, y la diferencia es **<15 pp** | **`A`** |
| **2** | Los dos brazos existen con denominador, y la diferencia es **≥15 pp** | **`B`** |
| **3** | Al menos un brazo tiene **cero** rechazos mexicanos, o falta el denominador | **`D`** |
| **4** | Los dos brazos existen pero el `n` deja un IC binomial que cruza 15 pp | **no adjudica** (`A-bis`, contraparte) |

### 4.3 · Precedencia, fijada al sellar y no después

1. **`A` y `B` mandan sobre `C` y `D`** si las dos tasas se construyen; son mutuamente excluyentes por el corte de 15 pp.
2. **`B` manda sobre `C`.** Las dos se leerían ciertas a la vez si la diferencia se midiera en muestra universitaria: `B` (*"diferencia presente en muestra estudiantil no generalizable"*) **ya nombra** la limitación que `C` describe (*"exigiría replicación fuera de población universitaria"*), y una fila que nombra el resultado **y** su límite manda sobre una que solo nombra el límite.
3. **`D` manda sobre `C`** cuando un brazo está vacío. Mismo precedente que `R8.1`: `ADR-56` archivó `D` en `R4.1`, `R4.3`, `R9.1` y `R9.2` teniendo cada una su fila `C` con un diseño más fino inexistente.
4. **La fila `D` de esta ficha NO está excluida por su propio texto, y la distinción importa.** `D` dice *"improbable: el diseño es replicable"* — una **apuesta** sobre la probabilidad de `D`, no una exclusión. Es lo contrario de `R7.3`, cuya `D` dice *"no aplica"* y sí queda excluida por la letra. **Si la corrida cae en la rama 3, `D` se propone, y la apuesta del pre-registro se declara perdida** — con su razón, no como reproche.

---

## 5 · Qué significa que el falsador NO refute (Bloque B-bis)

**`corroborada` — NO está disponible, y esta vez ni siquiera en el mejor caso.** Aunque los dos brazos existieran y la diferencia fuera enorme, el corpus es role-play universitario: la propia ficha lo dice en su fila `B` (*"no generalizable"*) y en su `C` (*"el ancla actual es Tlaxcala, universitarios"*). **El techo de este falsador con este instrumento es `acotada`, y su nombre en la escala es `B`.**

**`acotada` — es la fila `B`,** y su contenido sería: *el driver `face` sobrevive la prueba en muestra estudiantil mexicana, y `simpatía` (b) sigue sin sustituto (a) fuera de esa muestra*. Sería el primer dato de este programa que separa los dos drivers de un `PORQUE` mixto, aunque sea en una población estrecha. **Se dice antes de verlo**, como el Bloque B-bis exige.

**`falsador demasiado débil` — con una precisión que esta ficha necesita.** Si un brazo está vacío, **no es que el falsador sea débil: es que no llega a existir**. Un contraste de dos tasas con una tasa no es un contraste débil, es un no-contraste. Su fila es `D`, y `D` aquí significa *"no hay instrumento que lo mida"*, no *"lo medimos y no dijo nada"*.

**Y la asimetría que hay que escribir antes:** la regla `R10.1` **no se cae ni se sostiene** por este resultado. El 64% de Tlaxcala que la ancla sigue siendo lo que era. Lo que este falsador pone a prueba **no es la regla sino su `PORQUE`** — cuál de los dos drivers, `face` o `simpatía`, hace el trabajo. Que no podamos separarlos deja el `PORQUE` mixto exactamente como estaba, con su marca de procedencia mezclada, y eso es lo que se archivaría.

---

## 6 · Qué NO hace este acto

No adjudica. No recodifica a ojo ninguna transcripción: usa el código de poder del propio corpus. No usa los rechazos de otros países como si fueran mexicanos. No cuenta peticiones como si fueran rechazos — son actos de habla distintos y el falsador nombra rechazos. No toca `milpa/` ni el tier `[FUERTE]` de `R10.1`. No toca las otras 26 fichas.

---

## 7 · Declaración `ADR-46`

Al contar los rechazos por brazo en COMMIT B, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra el corpus Brasdefer. El reconocimiento de §1 ya es contaminación **parcial** y se declara ahí, no aquí.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
