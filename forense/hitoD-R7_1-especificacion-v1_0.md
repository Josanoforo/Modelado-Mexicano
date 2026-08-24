# HITO D · Falsador `R7.1` — especificación pre-registrada, congelada antes de leer el microdato electoral

### `hitoD-R7.1-especificacion` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_1-especificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.1-especificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada (COMMIT A) del falsador de `R7.1`: variables, universo, ponderador y diseño, dicotomización, escala con precedencia, y qué significa que el falsador NO refute. |
> | **QUÉ NO ES** | **No trae ni una cifra producida por este acto.** No adjudica, no emite y no retira ningún veredicto `RX.Y`. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | ninguna cantidad estimada aparece en este documento; el árbol de decisión está completo antes de la corrida; la precedencia entre filas está fijada aquí y no después. |

**Acto:** `ACTO RETRIAGE-4`, 20/ago/2026, entorno **UBUNTU** (`sin_variable` · sonda INEGI `200` · corpus montado), sobre `origin/main = 54da215`.
**Encargo:** `forense/encargos/2026-08-20-RETRIAGE-4.md` (`FP-86`, firma de mesa «A1»).

---

## 0 · Ficha bajo prueba, verbatim (`hitoD-preregistro-v2_0.md:168-176`)

> **R7.1 · Peso del acto → participación diferencial `[FUERTE]`**
> SI es elección presidencial de alto envío simbólico ENTONCES participación ~60%; SI es elección técnica/judicial percibida como decidida ENTONCES abstención >85% — PORQUE cálculo del peso del acto
>
> **Riesgo declarado: es una predicción histórica.** Dos elecciones no falsan un mecanismo. **Debe refutarse al nivel donde se usa:** el driver declarado es **el peso percibido del acto**, no el tipo de elección.
>
> **Falsador.** Una elección **técnica o de bajo perfil** con participación alta, o una **presidencial** con abstención alta, donde el peso percibido explique la diferencia mejor que el tipo de comicio. *Candidato: elecciones locales concurrentes vs. no concurrentes — mismo votante, mismo año, distinto peso percibido.*
> **Umbral.** Diferencia de participación entre concurrente y no concurrente **<15 puntos** para el mismo electorado → el tipo de acto no está haciendo el trabajo.
>
> **A** <15 puntos con electorado pareado · **B** diferencia grande sin controlar movilización partidista · **C** exigiría serie municipal pareada — **granularidad municipal es hueco declarado** · **D** posible por ese hueco.

Y el defecto de redacción que el propio pre-registro le adjudicó (`:321`): **`D-05` · `R7.1` · Predicción histórica: dos elecciones no falsan un mecanismo. Reescrita contra *peso percibido*, no contra tipo de comicio.**

---

## 1 · Lo que este ejecutor ya vio del instrumento antes de congelar, declarado y no oculto

Esto **no es un pre-registro ciego** y decirlo es obligación, no adorno. La pre-registración real de `R7.1` es del 28/jul/2026 y está arriba, verbatim; lo que este documento congela es la **operacionalización**, y para escribirla hubo que abrir la envoltura del instrumento. Se declara exactamente qué se miró:

1. **La lista de nombres de columna** de `Final Data/all_states_final.zip → all_states_final.csv` (44 nombres, leídos de la línea de encabezado).
2. **Los nombres de carpeta** de `Data/Raw Electoral Data/`, que codifican en su propio nombre el calendario de años de elección municipal por estado (p. ej. `Aguascalientes - 2004, 2007, 2010, 2013,2016,2019`). Es documentación del paquete, no dato.
3. **Tres filas de muestra** impresas al identificar el archivo, todas de Aguascalientes 2004. **Sus valores no se reproducen aquí y no juegan ningún papel en esta spec**; aparecerán en la salida cruda de COMMIT B como cualquier otra fila.

**Lo que NO se hizo:** no se calculó ninguna participación agregada, ninguna diferencia entre regímenes, ningún `n` analítico, ningún estadístico de ninguna clase. Este documento no contiene una sola cantidad producida por este acto.

---

## 2 · Construibilidad del Umbral — adjudicada antes de estimar

El Umbral pide tres piezas: **(i)** participación, **(ii)** una partición concurrente / no concurrente, **(iii)** *"el mismo electorado"*.

**(i) Participación: presente en el instrumento.** El archivo trae `turnout`, `total`, `valid` y `registered_voters` a nivel de casilla/sección. La spec **no hereda** `turnout`: lo recalcula como `total / registered_voters` y verifica en COMMIT B que reproduce la columna publicada — control de canalización, mismo espíritu que `hitoD-R1.3-especificacion §5` y `hitoD-R3.1-especificacion` fijaron.

**(ii) Partición concurrente / no concurrente: construible sin dato externo.** El calendario federal mexicano es público y fijo: hay elección federal (diputados) cada tres años — **1994, 1997, 2000, 2003, 2006, 2009, 2012, 2015, 2018, 2021, 2024** —, de las cuales **1994, 2000, 2006, 2012, 2018 y 2024** son además presidenciales. La identidad aritmética equivalente, para que la regla sea auditable en una línea y no por lista tecleada: **`year % 3 == 2`**. Se define `concurrente = 1` si el año de la elección municipal es año federal, `0` si no.

**(iii) *"El mismo electorado"*: construible, y aquí es donde este acto corrige a la propia ficha.** La fila `C` de la escala dice *"granularidad municipal es hueco declarado"*. **Ese hueco ya no existe**: el instrumento identifica la unidad `precinct` (sección electoral) dentro de `mun_code` dentro de `state_code`, más fina que municipio, y la observa repetidamente a lo largo del calendario municipal de su estado. `forense/cruce-catalogo-fichas-v2_0.md:87` ya lo había anticipado en agosto (*"INEGI/INE libera casilla/sección, más fino que municipio... se registra como mejora de granularidad, no como variable confirmada"*); este acto lo confirma **contra el instrumento en disco**, no contra un catálogo.

**Conclusión de este punto, declarada antes de estimar:** las tres piezas del Umbral son construibles. `R7.1` **no es inejecutable por hueco de dato**, que es exactamente lo que su fila `D` predecía.

---

## 3 · Variables — citadas literal contra el encabezado del instrumento

**Instrumento único.** `data/raw/zenodo_electoral_precinct_level_mexico_municipal.zip`, entrada `zenodo_electoral_precinct_level_mexico_municipal` de `data/manifiesto.yaml`, verificada `COINCIDE` en este acto (`sha256 8998b4dc…`, `739952144` bytes — cifras del manifiesto, no de este acto). Archivo interno: `Final Data/all_states_final.zip → all_states_final.csv`.

| rol | variable | nota |
|---|---|---|
| llave de electorado | `state_code` · `mun_code` · `precinct` | la terna identifica la sección electoral dentro de su municipio |
| tiempo | `year` | año de la elección municipal |
| numerador de participación | `total` | votos totales emitidos en la casilla/sección |
| denominador de participación | `registered_voters` | lista nominal de la casilla/sección |
| control publicado | `turnout` | se recalcula y se compara; no se hereda |

**Desenlace `y`:** `y = total / registered_voters`, en puntos porcentuales.
**Tratamiento `w`:** `w = 1` si `year % 3 == 2` (concurrente), `w = 0` si no.

---

## 4 · Universo, ponderador y diseño

**Universo pre-registrado.** Todas las filas de `all_states_final.csv` con `registered_voters > 0`, `total` no ausente, y `precinct` no ausente. Su tamaño **no se escribe aquí**: se deriva y se reporta en COMMIT B. Si el universo real difiere del pre-registrado por cualquier exclusión no anticipada aquí, **se declara `ACOTADO` (A-bis r4)** y el resultado no se compara contra ningún marginal de participación de otra población.

**Ponderador: NO HAY, y la razón importa.** El encargo pide declarar `FAC_*`, `EST_DIS`, `UPM_DIS`. **Ninguno existe ni debe existir en este instrumento**: no es una encuesta por muestreo probabilístico de INEGI sino un **censo administrativo** de cómputos por casilla/sección. No hay factor de expansión porque no hay muestra que expandir; no hay estrato ni UPM de diseño porque no hay diseño muestral. Escribir `FAC_SEL` aquí sería importar el vocabulario de otro tipo de instrumento — el error de categoría que `A-bis r3` nombra.

**Lo que ocupa su lugar.** La incertidumbre no es de muestreo sino de **conglomerados**: el tratamiento (concurrencia) se asigna al nivel **estado × año**, porque el calendario electoral local es una decisión de estado, no de sección. Por eso:

- **EE primario: cluster-robusto a nivel `state_code`** — el nivel al que se asigna el tratamiento. Con ~32 conglomerados, se declara desde ahora la **reserva de conglomerados pocos**: los EE cluster-robustos son anticonservadores con pocos clusters, y el IC95% se reporta también con corrección de grados de libertad `G−1`.
- **EE de sensibilidad: cluster a nivel municipio** (`state_code`+`mun_code`). Se reporta, y se declara desde aquí que **es anticonservador** respecto al primario, no una alternativa igual de válida.

---

## 5 · Dicotomización, estimador y árbol de decisión — con precedencia fijada al sellar

### 5.1 · Estimador primario: diferencia pareada dentro de sección

Para cada sección `i` observada en **al menos una** elección concurrente y **al menos una** no concurrente:

Δᵢ = (media de `y` en sus años concurrentes) − (media de `y` en sus años no concurrentes)

**Δ̄ = media de Δᵢ sobre las secciones pareadas**, en puntos porcentuales. Es literalmente *"para el mismo electorado"* que el Umbral pide: la sección es su propio control.

### 5.2 · Estimador marginal, obligatorio y no opcional

Se computa **también** la diferencia de medias no pareada sobre todo el universo (concurrentes vs. no concurrentes, sin llave de sección). **Si marginal y pareado discrepan, el resultado se reporta como ASOCIACIÓN y se reportan los dos** — no se «elige el bueno» (`A-bis r1`/`r2`, e instrucción explícita del encargo). Condicionar puede acercar o alejar del estimando; lo único que una discrepancia establece es que el marginal no es robusto.

### 5.3 · Dicotomización de la decisión

El Umbral es un corte sobre Δ̄ **con signo**, no sobre su valor absoluto: la regla predice que el acto de alto peso (concurrente, arrastrado por la federal) moviliza más, es decir Δ̄ grande y positivo. Un Δ̄ negativo refuta con más fuerza aún, no menos.

- **Δ̄ < 15 pp** → el falsador **se satisface**: el tipo de acto no está haciendo el trabajo.
- **Δ̄ ≥ 15 pp** → el falsador **no se satisface**.

### 5.4 · Árbol de decisión, y la precedencia

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Δ̄ < 15 pp, con IC95% **enteramente** por debajo de 15 pp, sobre secciones pareadas | **`A`** — *"<15 puntos con electorado pareado"*, literal de la ficha |
| **2** | Δ̄ ≥ 15 pp, con IC95% **enteramente** por encima de 15 pp | **`B`** — *"diferencia grande sin controlar movilización partidista"*, literal de la ficha |
| **3** | El IC95% **cruza** 15 pp | **ninguna fila; no adjudica** (ver §5.5) |
| **4** | No existen secciones pareadas suficientes para estimar Δ̄ | **`C`**, y solo aquí |

**Regla de precedencia, fijada al sellar y no después.**

1. **`A` y `B` son mutuamente excluyentes por construcción** (particionan Δ̄ en el corte de 15 pp) y **mandan sobre `C`** siempre que la serie pareada exista y se corra. `C` describe un hueco de dato — *"exigiría serie municipal pareada — granularidad municipal es hueco declarado"* — y §2(iii) establece que ese hueco ya no existe: el instrumento da sección, más fino que municipio. Una fila que nombra un hueco no puede ganarle a una fila que nombra un resultado medido cuando el hueco está cerrado.
2. **`D` (*"posible por ese hueco"*) queda subordinada a `C`**: es la predicción de que el hueco de `C` haría la ficha inejecutable. Cerrado el hueco, `D` no puede satisfacerse. **Si la corrida produce un resultado, `D` está excluida por construcción**, y decirlo antes es la mitad del valor de esta sección.
3. **`B` no se propone por «no salió `A`».** `B` exige que la diferencia sea grande **y** que el control de movilización partidista falte. La segunda mitad se cumple por construcción con este instrumento (§6), así que `B` se decide solo por la primera mitad. Se dice aquí para que en COMMIT B no parezca que se eligió `B` por descarte.

### 5.5 · La contraparte de `A-bis`, aplicada antes de ver el dato

**Un punto que satisface el umbral con un IC95% que no lo despeja no adjudica.** Se reporta como propuesta con la reserva escrita — rama 3 de la tabla. No se redondea el IC hacia el lado conveniente, no se sube el nivel de confianza, no se recorta el universo hasta que el intervalo despeje.

---

## 6 · Qué significa que el falsador NO refute — declarado antes de correr (Bloque B-bis)

Las tres palabras del Bloque B-bis, aplicadas a esta ficha:

**`corroborada` — no está disponible para esta ficha, y se declara ahora.** Corroborar `R7.1` exigiría mostrar que la diferencia sobrevive al control de **movilización partidista**, que es el confusor que su propia fila `B` nombra. Este instrumento **no trae gasto de campaña, ni esfuerzo de movilización, ni maquinaria territorial**: trae votos y lista nominal. Por tanto, **el techo de este falsador es `acotada`; `corroborada` es inalcanzable con este instrumento por construcción**, y no se propondrá aunque el resultado sea espectacular.

**`acotada` — el desenlace de no-refutación, y es el interesante.** Un Δ̄ ≥ 15 pp dice que el tipo de acto **sí** covaría fuertemente con la participación del mismo electorado, con la sección como su propio control — y eso, si sale, sería **el primer dato mexicano a nivel de sección que sostiene el mecanismo de `R7.1` con electorado pareado**, no con dos elecciones nacionales comparadas de memoria. Se dice antes de verlo, como el Bloque B-bis exige, para que la corroboración no se lea como fracaso. Y se dice también su límite: sigue siendo asociación, no identificación (`A-bis r1`), porque la concurrencia no se asigna al azar y arrastra consigo la campaña federal entera.

**`falsador demasiado débil`.** Aplica si el IC95% es tan ancho que no excluye ni 0 ni 15 pp — es decir, si el pareado deja tan pocas secciones, o tan pocos estados con variación temporal en el régimen, que la prueba no distingue nada. **Es un desenlace registrable, no un fracaso a esconder**, y se anota como tal en COMMIT B junto con el `n` que lo produjo.

---

## 7 · Límites declarados antes de correr, sin maquillar

1. **Concurrencia por año es un proxy de concurrencia por fecha.** Antes de la reforma de 2014, un estado que votaba en año federal no siempre votaba el mismo **día** que la federal. `year % 3 == 2` mide coincidencia de **año**, no de jornada. Se declara como límite de medición, no se corrige silenciosamente. **Sensibilidad pre-declarada S4:** repetir el pareado restringiendo a secciones cuyas dos observaciones caen a partir de 2015, cuando la alineación al primer domingo de junio ya es obligatoria — a costa de perder la mayor parte de la variación temporal.
2. **Las secciones se redistritan.** La terna `state_code`+`mun_code`+`precinct` es estable dentro de una redemarcación, no a través de 25 años. Un pareado de horizonte largo mezcla electorados parcialmente distintos bajo la misma llave. **Sensibilidad pre-declarada S5:** repetir restringiendo a pares de años separados por ≤ 6 años.
3. **Sensibilidades restantes, también pre-declaradas.** **S1**: estimador marginal (§5.2, obligatorio). **S2**: mismo estimador con la unidad agregada a municipio, para verificar que la unidad no conduce el resultado. **S3**: restringir a secciones con ≥2 observaciones en cada brazo.
4. **Ninguna sensibilidad reemplaza al primario.** Se reportan todas; la fila se propone contra el primario de §5.1. Si una sensibilidad invierte la conclusión, eso se reporta como tal y **no se sustituye el primario por ella**.

---

## 8 · Qué NO hace este acto

No adjudica: propone. No toca `milpa/` — falsar una regla no es calibrar un coeficiente (`ADR-47`). No retiquetea el tier `[FUERTE]` de `R7.1` en `modelo §3.B`/`§7`: el tier del motor y el veredicto de Hito D son ejes distintos (`ADR-60(b)`). No toca las otras 26 fichas del pre-registro. No usa `ENCUP`, que `forense/notas/2026-08-06-map2-cruce.md:484` empareja con `R7.1` para la mitad **actitudinal**: el Umbral de esta ficha es de **participación**, no de actitud, y `ENCUP` no aporta ninguna variable al cómputo — declarado, no omitido.

---

## 9 · Declaración `ADR-46`

Al abrir `all_states_final.csv` en COMMIT B, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra la base electoral de Zenodo (`record 14991955`). La exploración declarada en §1 —encabezado de columnas, nombres de carpeta, tres filas de muestra— ya es contaminación **parcial** y queda declarada aquí. El resto del paquete (`Correlation Data/`, `Processed Data/`, `Data/Raw Electoral Data/`, `Data/incumbent data/`) **no se abre**: no aporta variable a este cómputo y abrirlo gastaría contaminación sin producir nada.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
