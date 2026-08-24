# HITO D · Falsador `R7.3` — especificación pre-registrada, congelada antes de abrir microdato

### `hitoD-R7.3-especificacion` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_3-especificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.3-especificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada (COMMIT A) del falsador de `R7.3`: qué exige un RDD, qué instrumento tendría que traerlo, la escala con precedencia, y qué significa que el falsador NO refute. |
> | **QUÉ NO ES** | **No trae ni una cifra producida por este acto.** No adjudica, no emite y no retira ningún veredicto. No mueve el contador `13 de 27`. **No autoriza ningún diseño sustituto**: ver §5.3. |
> | **VERIFICAS ASÍ** | el árbol de decisión está completo antes de la corrida; la precedencia está fijada aquí; y la prohibición de sustituir el diseño está escrita antes de saber si el original corre. |

**Acto:** `ACTO RETRIAGE-4`, 20/ago/2026, entorno **UBUNTU**, sobre `origin/main = 54da215`.

---

## 0 · Ficha bajo prueba, verbatim (`hitoD-preregistro-v2_0.md:190-198`)

> **R7.3 · Transferencia sin monitoreo → conserva autonomía del voto `[FUERTE]`**
> SI hay transferencia directa universal no condicionada Y NO hay proximidad/focalización Y NO hay monitoreo percibido ENTONCES conserva autonomía de la **ELECCIÓN** de voto
>
> **Es la única regla del corpus con identificación causal.** Y ahora lleva sus **condiciones de cesión** (P-02) y la distinción **turnout vs. vote-choice** (P-03).
>
> **Falsador — ya pre-registrado por el forense V2, se adopta literal:** *un RDD sobre la Pensión del Bienestar que muestre efecto electoral **independiente de la aprobación presidencial***.
> **Umbral (del propio forense):** efectos de compra **grandes (>5–10 puntos) y persistentes a escala nacional**, no solo locales.
>
> **A** RDD con efecto independiente que cruce el umbral · **B** **ya obtenido** en la corrida previa — correlacional, **CONFUNDIDO** con aprobación e identidad · **C** exigiría el RDD, que no existe en fuentes públicas · **D** no aplica: el diseño es concebible, solo no se ha hecho.

---

## 1 · Lo que este ejecutor ya vio antes de congelar, declarado y no oculto

1. Los campos `formato` y `nota` de las entradas `r7_3_pub_beneficiarios_bienestar_csv` y `zenodo_electoral_precinct_level_mexico_municipal` de `data/manifiesto.yaml` (metadato commiteado, no microdato).
2. **La lista de nombres y etiquetas de variable** de `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta` (195) y `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta` (262), leída del encabezado Stata. **Estructura, no contenido**: no se leyó una sola fila.
3. El apartado `Ficha 8 (R7.3)` de `forense/notas/2026-08-05-conf17-fetch-corrida-B.md`, ya archivado.

No se calculó ningún estadístico, ningún conteo de celda, ningún `n`.

---

## 2 · Qué exige el falsador, desarmado en piezas verificables

Un RDD que sostenga la afirmación del Umbral necesita **cuatro** piezas **en el mismo instrumento y a la misma unidad de observación**:

| # | pieza | por qué es indispensable |
|---|---|---|
| **P1** | **Variable de asignación continua con corte conocido** que determine la elegibilidad al programa | sin corte no hay discontinuidad que explotar |
| **P2** | **El programa nombrado**: Pensión del Bienestar, no "ayuda del gobierno" en general | el falsador nombra el programa; una transferencia genérica mide otra cosa |
| **P3** | **Desenlace electoral** (elección de voto, no solo participación — la ficha trae la distinción `turnout` vs. `vote-choice` de `P-03`) | es el desenlace de la regla |
| **P4** | **Aprobación presidencial** medida en la misma unidad | el falsador exige el efecto ***independiente de la aprobación presidencial***; sin ella no se puede separar |

**Y una quinta que no es del instrumento sino del estimando:** el Umbral pide efectos *"grandes (>5–10 puntos) y **persistentes a escala nacional**, no solo locales"*. Un diseño que solo pueda hablar de una ventana estrecha alrededor de un corte de edad, con precisión de encuesta, **no habla de escala nacional** aunque las cuatro piezas existan.

---

## 3 · Los candidatos, y qué se verifica de cada uno en COMMIT B

| instrumento | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| `r7_3_pub_beneficiarios_bienestar_csv` (Padrón Único, agregado entidad×trimestre) | a verificar | a verificar | a verificar | a verificar |
| `zenodo_electoral_precinct_level_mexico_municipal` (sección×año) | a verificar | a verificar | a verificar | a verificar |
| `mex_2023_lapop_americasbarometer_v1_0_w` / `mex_2021_…_v1_2_w` | a verificar | a verificar | a verificar | a verificar |
| `latinobarometro2024_bd_stata` | a verificar | a verificar | a verificar | a verificar |

La tabla se llena **en COMMIT B, por lectura del instrumento**, no aquí. Se deja en blanco a propósito: llenarla ahora sería escribir el resultado en la spec.

---

## 4 · Universo, ponderador y diseño

**Si alguna vía sobrevive a §3**, el diseño aplicable queda fijado desde ahora y no se improvisa:

- **Padrón / electoral (registro administrativo):** censo, **sin ponderador** — no hay `FAC_*`, `EST_DIS` ni `UPM_DIS`; conglomerado al nivel de asignación.
- **LAPOP (encuesta con diseño complejo):** el análogo mexicano de `FAC_*`/`EST_DIS`/`UPM_DIS` en este instrumento son **`wt`** (peso de la muestra), **`strata`** (peso estandarizado) / **`estratopri`** (región) / **`estratosec`** (tamaño de municipalidad), y **`upm`** (unidad de muestreo primaria) / **`cluster`** (lugar de muestreo) — presentes en el encabezado, verificado en §1. Ninguna estimación se reporta sin ellos.
- **Latinobarómetro:** a verificar en COMMIT B; sin ponderador declarado no se estima.

**Universo pre-registrado:** el que declare la vía que sobreviva. Si difiere del pre-registrado se declara `ACOTADO` (`A-bis r4`) y no se compara contra ningún marginal poblacional.

---

## 5 · Escala, dicotomización, árbol y precedencia — fijados al sellar

### 5.1 · Dicotomización

El Umbral es un corte sobre el **efecto electoral estimado por el RDD**: *"grandes (>5–10 puntos)"*. Se fija el borde **conservador** del rango que la propia ficha escribe: **≥10 puntos porcentuales**, no 5. Razón declarada antes de ver nada: elegir 5 haría más fácil satisfacer el falsador y refutar la regla; se elige el corte que **le pone la prueba más difícil al falsador y más fácil a la regla**, que es la dirección honesta cuando la ficha da un rango y no un número.

### 5.2 · Árbol de decisión

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Ningún instrumento en disco reúne P1+P2+P3+P4 a la misma unidad | **`C`** |
| **2** | Los reúne, pero la precisión alcanzable no puede hablar de *"escala nacional"* en el sentido del Umbral | **`C`**, con la razón medida |
| **3** | Los reúne y el RDD es corrible con esa precisión | **PARO por ficha**: este acto lo declara, no lo corre — correr un RDD es un acto propio, y hacerlo aquí sería improvisar un diseño causal dentro de un acto de triaje |
| **4** | El RDD corre en un acto futuro y el efecto independiente cruza ≥10 pp | `A` (fuera del alcance de este acto) |

### 5.3 · La prohibición de sustituir, escrita antes de saber si el original corre

**Este acto NO correrá ningún diseño sustituto del RDD**, y lo declara ahora para que no parezca una salida cómoda después. En concreto, quedan **prohibidos** en este acto: (a) un RDD por edad sobre una variable de *ayuda genérica del gobierno* en lugar del programa nombrado; (b) una correlación ecológica entre padrón por entidad y voto por sección; (c) una diferencia-en-diferencias entre entidades. Los tres son concebibles y los tres miden **otra cosa** que lo que la ficha pre-registró. Sustituir el diseño pre-registrado por uno más débil y reportar el resultado como si fuera el falsador es el defecto que este programa lleva dos meses evitando; no se comete aquí por conveniencia de mover un contador.

### 5.4 · Precedencia, fijada al sellar y no después

1. **`A` manda sobre todas** si el RDD corre y cruza el corte de §5.1.
2. **`C` manda sobre `B`.** Razón: `B` (*"ya obtenido en la corrida previa — correlacional, CONFUNDIDO con aprobación e identidad"*) **no es un desenlace de este falsador** — es el registro de un resultado que ya existía *antes* de que la ficha se escribiera, y archivarlo como veredicto del Hito D sería archivar como producto del Paso 2 algo que el Paso 2 no produjo. `C` sí es un desenlace de este falsador: nombra la pieza que falta, y este acto la mide.
3. **`D` está excluida por la letra de la propia ficha** (*"no aplica: el diseño es concebible, solo no se ha hecho"*). No se propondrá bajo ninguna lectura, ni siquiera si el hueco resulta más grande de lo esperado.

---

## 6 · Qué significa que el falsador NO refute (Bloque B-bis) — y el caso raro de esta ficha

Esta ficha tiene una asimetría que hay que escribir antes de correr: **su falsador solo puede refutar.** Un RDD con efecto de compra grande e independiente refutaría `R7.3`; la **ausencia** de ese RDD no dice nada sobre la regla. Por eso, de las tres palabras del Bloque B-bis:

**`corroborada` — NO está disponible, y su indisponibilidad es estructural, no circunstancial.** Que nadie haya corrido el RDD no corrobora que la transferencia conserve la autonomía del voto. **`R7.3` es hoy la única regla del perímetro rotulada *"la única regla del corpus con identificación causal"* cuya identificación causal nunca ha sido puesta a prueba en este programa.** Se dice aquí, antes de correr, para que el desenlace no se lea como respaldo.

**`acotada` — tampoco.** Acotar exige una prueba que corrió sobre parte del territorio. Aquí no corre ninguna.

**`falsador demasiado débil` — es el desenlace vivo, con una precisión importante.** No es débil por falta de potencia estadística de una corrida: es que **nunca llega a ser corrible** con fuentes públicas. Ese desenlace tiene nombre propio en la escala de esta ficha y es la fila `C`. Que el resultado más probable sea `C` **no lo hace un no-resultado**: convierte *"nadie lo ha hecho"* en *"medimos qué pieza falta y en qué instrumento"*, que es lo que un acto de triaje puede aportar y lo que la fila `C` existe para anotar.

**Lo interesante bajo no-refutación, dicho antes de verlo.** Si sale `C`, el aporte no es el veredicto: es **el mapa de qué falta**. La pieza que se identifique como faltante (P1, P2, P3 o P4) es la lista de la compra de quien quiera desbloquear la única regla causal del corpus — y hasta hoy nadie la ha escrito.

---

## 7 · Qué NO hace este acto

No adjudica. No corre ningún RDD. No corre ningún sustituto (§5.3). No toca `milpa/` ni el tier `[FUERTE]` de `R7.3`. No reabre `P-02` ni `P-03`. No toca las otras 26 fichas.

---

## 8 · Declaración `ADR-46`

Al leer el encabezado de variables de los dos `.dta` de LAPOP (§1), esta sesión ya tiene **contaminación de estructura** sobre LAPOP México 2021 y 2023. Si COMMIT B abre **contenido** de esos archivos —conteos de celda alrededor de un corte de edad—, la contaminación pasa a **total** para LAPOP en esta sesión, y **esta sesión queda inhabilitada para pre-registrar `R8.3`**, cuya ficha depende de LAPOP/Latinobarómetro (`CONF-17`, Ficha 12). `R8.3` es una de las nueve pre-registradas como probable `D` y está **fuera del perímetro de este acto** por instrucción del encargo, así que la inhabilitación no cuesta nada aquí — pero se declara, no se descubre después.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
