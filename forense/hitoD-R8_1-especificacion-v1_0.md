# HITO D · Falsador `R8.1` — especificación pre-registrada, congelada antes de abrir instrumento

### `hitoD-R8.1-especificacion` · **v1.0** · 20 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R8_1-especificacion-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R8.1-especificacion`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La spec congelada (COMMIT A) del falsador de `R8.1`: las cuatro piezas que exige, universo, ponderador y diseño, dicotomización, escala con precedencia, y qué significa que el falsador NO refute. |
> | **QUÉ NO ES** | **No trae ni una cifra producida por este acto.** No adjudica. No mueve el contador `13 de 27`. |
> | **VERIFICAS ASÍ** | el árbol de decisión y la precedencia están completos antes de la corrida; y el defecto de redacción que esta spec propone está declarado **antes** de saber si la corrida lo confirma. |

**Acto:** `ACTO RETRIAGE-4`, 20/ago/2026, entorno **UBUNTU**, sobre `origin/main = 54da215`.

---

## 0 · Ficha bajo prueba, verbatim (`hitoD-preregistro-v2_0.md:216-224`)

> **R8.1 · Monitoreo + sanción → contribuye `[FUERTE]`**
> SI hay comité con liderazgo confiable + monitoreo + sanción visible ENTONCES contribuye; SI no hay monitoreo ni sanción ENTONCES free-riding racional
>
> **Falsador.** Bien público mexicano con contribución alta y sostenida **sin monitoreo ni sanción**.
> **Umbral.** Tasa de contribución **≥60%** durante ≥2 años sin mecanismo de sanción identificable ni liderazgo con capacidad de excluir.
>
> 🚫 **Frontera obligatoria:** la **faena/tequio bajo usos y costumbres** queda **fuera del modelo** (ADR-10). No es un caso de este dominio: es obligación institucional de otro orden. **Usarla como contraejemplo sería error categorial** y el veredicto no contaría. El falsador debe buscarse en **pueblo mestizo o urbano**.
>
> **A** ≥60% sostenido sin sanción, fuera del sistema comunal · **B** contribución alta con sanción informal no registrada (presión vecinal cuenta como sanción) · **C** exigiría inventario de comités con y sin mecanismo · **D** posible.

---

## 1 · Lo que este ejecutor ya vio antes de congelar, declarado y no oculto

1. El campo `formato` de `r8_1_contraloria_social_2019_2025_csv` en `data/manifiesto.yaml` (metadato commiteado: 8 filas, 9 columnas, nombres de columna) y el apartado `Ficha 10 (R8.1)` de `forense/notas/2026-08-05-conf17-fetch-corrida-B.md`, ya archivado.
2. **Los nombres de campo de primer nivel** de `data/raw/ADQ15_OMCA_conflictos_agua/omca_conflictos_base_completa.json` y su número de registros.
3. **Las etiquetas de variable** de LAPOP México 2021 y 2023 (§1 de `hitoD-R7.3-especificacion` ya declaró esta lectura), filtradas por `cp*`/comunidad/comité/agua.

No se calculó ninguna tasa, ningún conteo cruzado, ningún `n` analítico.

---

## 2 · Qué exige el falsador, desarmado en piezas verificables

| # | pieza | por qué es indispensable |
|---|---|---|
| **Q1** | **Un bien público identificado con TASA de contribución**: numerador (quien contribuye) sobre denominador (quien podría) | el Umbral es un porcentaje; sin denominador no hay porcentaje |
| **Q2** | **Sostenida ≥2 años**: la misma unidad-bien observada en al menos dos años | el Umbral lo pide literal |
| **Q3** | **Ausencia identificable de sanción y de liderazgo con capacidad de excluir** | es el brazo del contraste; sin él no hay falsador, hay descripción |
| **Q4** | **Fuera del sistema comunal** (`ADR-10`): identificable como pueblo mestizo o urbano | la ficha lo declara frontera obligatoria y un contraejemplo comunal **no contaría** |

---

## 3 · El defecto de redacción que esta spec propone, declarado ANTES de correr

**El falsador de `R8.1` pide evidencia de una ausencia, y las ausencias no generan registro.** Un inventario de comités es, por construcción, un inventario del brazo **monitoreado**: el bien público que nadie vigila no produce acta, ni padrón, ni comité constituido, ni fila en ninguna base administrativa. La fila `C` de la ficha (*"exigiría inventario de comités con y sin mecanismo"*) pide una lista que incluya a quienes, por definición de lo que se está midiendo, no están en ninguna lista.

**Esto no es un hueco de dato mexicano: es un defecto de diseño del falsador**, y por eso se declara aquí y no después de que la corrida "no encuentre nada" — que es cuando dejaría de ser predicción y pasaría a ser excusa. Si la corrida lo confirma, **se propone a mesa como `D-07`**, séptimo defecto de redacción del Paso 1, en la tabla de `hitoD-preregistro:313` que hoy tiene seis y **ninguno sobre `R8.1`** (verificado: `D-01` R1.2 · `D-02` R4.2/R5.2 · `D-03` R2.2/R10.2 · `D-04` R4.1/R9.1 · `D-05` R7.1 · `D-06` R8.3). **Se propone, no se numera**: rotular `D-07` sin firma sería el ejecutor decidiendo en vez de propagar (`ADR-76`/`ADR-79`).

**Y la salida que el propio falsador deja abierta, para no exagerar el defecto:** una **encuesta a hogares** sí puede medir contribución a un bien público sin pasar por ningún registro de comités — pregunta por la conducta, no por la organización. Si algún instrumento de encuesta en disco construye Q1+Q3 a la vez, el defecto es menos grave de lo que este apartado dice, y la corrida lo dirá. Es la mitad del valor de declararlo antes.

---

## 4 · Candidatos, y qué se verifica de cada uno en COMMIT B

| instrumento | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| `r8_1_contraloria_social_2019_2025_csv` (Contraloría Social, agregado nacional×año) | a verificar | a verificar | a verificar | a verificar |
| `ADQ15_OMCA_conflictos_agua` (registro de conflictos por el agua) | a verificar | a verificar | a verificar | a verificar |
| LAPOP México 2021 / 2023 (`cp*`, participación comunitaria) | a verificar | a verificar | a verificar | a verificar |
| `encup_2012_base_datos_xlsx` (ENCUP 2012) | a verificar | a verificar | a verificar | a verificar |

Se deja en blanco a propósito: llenarla aquí sería escribir el resultado en la spec.

---

## 5 · Universo, ponderador y diseño

- **Contraloría Social y OMCA:** registros administrativos / hemerográficos, **sin ponderador**. No hay `FAC_*`, `EST_DIS` ni `UPM_DIS`.
- **LAPOP:** `wt` · `strata`/`estratopri`/`estratosec` · `upm`/`cluster` — el análogo de `FAC_*`/`EST_DIS`/`UPM_DIS`. Ninguna tasa se reporta sin ellos.
- **ENCUP 2012:** ponderador y estratos a verificar en COMMIT B contra el propio archivo; **si no trae ponderador declarado, no se estima ninguna tasa poblacional con él** y se dice.
- **Universo pre-registrado:** el que declare la vía que sobreviva a §4. Si difiere, se declara `ACOTADO` (`A-bis r4`).

---

## 6 · Dicotomización, árbol y precedencia — fijados al sellar

### 6.1 · Dicotomización

**Contribución alta = tasa ≥ 60%**, literal del Umbral. **Sostenida = la misma unidad-bien con tasa ≥60% en ≥2 años distintos.** Ambas condiciones **conjuntas**: una tasa de 60% en un solo año no satisface el falsador.

### 6.2 · Árbol de decisión

| rama | condición | fila propuesta |
|---|---|---|
| **1** | Existe un bien público con tasa ≥60% sostenida ≥2 años, con ausencia de sanción **verificada** y fuera del sistema comunal | **`A`** |
| **2** | Tasa alta y sostenida, pero hay sanción informal registrable (presión vecinal) o liderazgo con capacidad de excluir | **`B`** |
| **3** | Ningún instrumento en disco construye Q1+Q2+Q3+Q4 | **`D`** |
| **4** | Algún instrumento construye Q1+Q2 pero **ninguno** Q3, y la razón es la estructural de §3 | **`D`**, con `D-07` propuesto a mesa |

### 6.3 · Precedencia, fijada al sellar y no después

1. **`A` y `B` mandan sobre `C` y `D`** si la tasa se construye. Son mutuamente excluyentes entre sí por el estado de Q3 (sanción ausente verificada contra sanción presente).
2. **`D` manda sobre `C`.** Las dos pueden leerse a la vez —`C` nombra el inventario que haría falta, `D` registra que no lo hay—, y manda `D`. **Precedente directo, no invención:** `R4.1`, `R4.3` (ambas mitades), `R9.1` y `R9.2` se archivaron `D` teniendo su propia fila `C` describiendo un diseño más fino que tampoco existía (`ADR-56`, 4/ago/2026). Un `D` archivado es una afirmación medida sobre nuestro instrumental; un `C` sin medir es una lista de deseos.
3. **La frontera de `ADR-10` no se cruza por conveniencia.** Si el único caso mexicano con tasa ≥60% sostenida sin sanción resultara ser faena o tequio bajo usos y costumbres, **no cuenta**, el veredicto no se mueve, y se dice — la propia ficha lo declara error categorial.

---

## 7 · Qué significa que el falsador NO refute (Bloque B-bis)

**`corroborada` — NO está disponible, y por la misma asimetría que `R7.3`.** El falsador de `R8.1` busca un **contraejemplo**. No encontrarlo no corrobora que monitoreo y sanción sean necesarios: puede ser que el contraejemplo exista y no esté registrado —que es justo lo que §3 predice— o que nadie lo haya buscado donde vive. **Ausencia de contraejemplo no es evidencia de la regla**, y se escribe antes de correr para que el desenlace no se lea al revés.

**`acotada` — solo en un caso, y se nombra ahora:** si algún instrumento construyera Q1+Q2+Q3 sobre **un** bien público concreto (digamos, agua entubada en una colonia urbana) y no se hallara el contraejemplo ahí, `R8.1` quedaría acotada **a ese bien y a ese contexto**, nunca a "los bienes públicos mexicanos".

**`falsador demasiado débil` — es el desenlace vivo**, y su razón está pre-declarada en §3: no es debilidad de potencia, es que el brazo de control del contraste no deja rastro documental. Su fila es `D`.

**Lo interesante bajo no-refutación, dicho antes de verlo.** Si la corrida confirma §3, `R8.1` se une a `R7.3` en una clase que este acto está encontrando y que el programa no tenía nombrada: **reglas cuyo falsador es inejecutable no por falta de dato mexicano, sino por cómo está escrito el falsador**. Distinguir *"México no lo publica"* de *"esta prueba no se puede hacer con ninguna publicación"* cambia qué acto sucesor tiene sentido: en el primer caso se adquiere; en el segundo se reescribe el falsador, y adquirir sería tirar el dinero.

---

## 8 · Qué NO hace este acto

No adjudica. No numera `D-07` (lo propone). No toca `milpa/` ni el tier `[FUERTE]` de `R8.1`. No cruza la frontera de `ADR-10`. No toca las otras 26 fichas.

---

## 9 · Declaración `ADR-46`

Al abrir contenido de `contraloria_social_2019_2025.csv`, del JSON de OMCA y de `encup_2012_base_datos_xlsx.xlsx` en COMMIT B, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra esos tres instrumentos. LAPOP ya quedó declarado en `hitoD-R7.3-especificacion §8`.

---

**el primer resultado que produzca este procedimiento es el que se reporta.**
