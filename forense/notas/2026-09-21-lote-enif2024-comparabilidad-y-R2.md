# Qué olas de ENIF pueden alimentar a R2, y cuáles no

**Acto** `GEN2-DIN-LOTE-ENIF2024-A` · 21/sep/2026 · entorno NUBE (`milpa-inegi`,
sonda a INEGI `http_code=200`) · rama `acto/gen2-din-lote-enif2024-a` ·
**cero microdato abierto** · contadores movidos: **cero** (`cuenta_gen2 = NO-APLICA`;
este acto no mide, escribe la propuesta y la tabla que el COMMIT-1 va a necesitar).

## 1 · La pregunta, en una línea

`R2` es la interacción histórica **encogida** hacia el piso. Encoger con `λ` **estimada**
exige medir cuánto se repite la interacción entre olas; eso sólo se puede hacer con olas
en las que **el desenlace y los ejes se pregunten igual**. Antes de este acto se sabía
para 2021↔2024 (piloto 1) y no se sabía para 2012, 2015 y 2018.

## 2 · Lo que se leyó, y cuánto

10 payloads del manifiesto (descriptores de archivo y cuestionarios de las cinco olas),
bajados con `tests/manifiesto.py --descarga` y verificados por sha256:
**10/10 `DESCARGADO-AHORA`**, ninguno discordante. Se recorrieron **todas** las hojas de
los cinco FD (7 929 filas de catálogo en total) y los cinco cuestionarios completos.
Los cuestionarios de 2012 y 2015 entraron al corpus el 21/sep (`PR #960`): **es la
primera vez que la casa puede contestar esta pregunta sin un `NO-VERIFICABLE-AQUÍ`**.
El resultado, fila por fila, está en `data/ahorro-comparabilidad-texto-v1_0.tsv`
(40 filas = 2 componentes del desenlace + 6 ejes, × 5 olas) con su `.meta` y su test.

## 3 · La respuesta, sin adjetivos

**Para la interacción histórica del desenlace `ahorra_solo_informal`, sólo 2021 sirve.**

| ola | componente informal | componente formal | ¿alimenta la interacción histórica? |
|---|---|---|---|
| **2021** | MISMO-INSTRUMENTO (ancla) | MISMO-INSTRUMENTO (ancla, 9 vías) | **SÍ — es la única** |
| 2018 | MISMO-INSTRUMENTO | CAMBIO-MENOR — **8 de 9 vías** | **NO** para `D9`. Sí para un `D8` armonizado, si mesa lo autoriza (§5) |
| 2015 | CAMBIO-MENOR (otro orden de índice) | CAMBIO-DE-INSTRUMENTO — 6 posiciones, nómina y pensión colapsadas, sin apoyos de gobierno | **NO** |
| 2012 | CAMBIO-DE-INSTRUMENTO — 5 vías y ventana de ~3 meses | CAMBIO-DE-INSTRUMENTO — 6 posiciones y ventana de ~12 meses | **NO** |

Las tres razones, que **no se colapsan** entre sí:

1. **2012 no tiene el desenlace, ni siquiera mal.** Sus dos componentes usan **ventanas
   de referencia distintas**: «de febrero a la fecha» (~3 meses) el informal y «de abril
   de 2011 a la fecha» (~12 meses) el formal. `informal ∧ ¬formal` mezclaría dos
   periodos: el número no sería el estimando, sería un artefacto del cuestionario.
   Además le falta la vía «ahorró comprando animales o bienes» (texto buscado en las
   1 594 filas del FD y en las 1 733 líneas del cuestionario: NO-ENCONTRADO).
2. **2015 tiene el lado informal y no el formal.** La batería informal es la misma de
   2021 en otro orden (mapa por texto 1→3, 2→4, 3→6, 4→5, 5→1, 6→2). La formal sólo
   tiene seis posiciones, con **nómina y pensión en una sola casilla** y sin «apoyos de
   gobierno» como posición propia: la partición no se recupera desagregando, porque la
   información no está en el archivo.
3. **2018 se queda a una vía.** Tiene las ocho primeras del ancla con el mismo verbo y
   el mismo gate de tenencia; le falta la novena del ancla por índice, «cuenta
   contratada por Internet o aplicación», que no tiene casilla en esa ola. Lo
   construible en 2018 es `D8 = informal ∧ ¬formal_8`, y por construcción **`D9 ⊆ D8`**
   — la misma desigualdad que la spec del piloto 1 ya usa como falsador entre `D9` y
   `D7`. Emitir `D9` en 2021 contra `D8` en 2018 sería comparar dos escalas sin función
   de enlace (A-bis 3).

**Y hay un límite que aplica a las tres olas históricas a la vez, no sólo al desenlace:**
la persona elegida de 2012, 2015 y 2018 es de **18 a 70 años**; la de 2021 y 2024 es de
**18 y más** (FD: `EDAD` 18-70 en el módulo de 2015 y 2018; cuestionario 2012:
«PARA PERSONAS DE 18 A 70 AÑOS»). A-bis 4: un estimando restringido a una subpoblación
no se compara contra uno poblacional sin recalcular al mismo universo o declararlo
acotado. Cualquier uso de 2018 arrastra este recorte **además** del de la vía 8.

## 4 · Consecuencia para R2, por par — escrita antes de que nadie mida

La regla que aplica es la de la **firma F2 de mesa (21/sep)**, verbatim: «si solo una
[ola] lo es, R2 es solo λ = ½ y se declara antes de abrir». **Una sola lo es.** Por lo
tanto, y para los catorce pares sin excepción:

| grupo | pares | ejes construibles en 2018 | olas que alimentan la interacción | **R2** |
|---|---|---|---|---|
| **primarios (5)** | sexo×edad · sexo×escolaridad · sexo×localidad · edad×escolaridad · escolaridad×localidad | los cuatro ejes, acotados a 18-70 | **sólo 2021** | **λ = ½** |
| **formalidad, secundarios (4)** | formalidad×{sexo, edad, escolaridad, localidad} | sí — `P3_11` de 2018 es idéntico a `P3_10` de 2021, código por código | **sólo 2021** | **λ = ½** |
| **cuenta_formal, aparte (5)** | cuenta_formal×{sexo, edad, escolaridad, localidad, formalidad} | sí, sobre 8 tipos y no 9 | **sólo 2021** | **λ = ½** |

**Ningún par cae en `NO-CONSTRUIBLE`**: la rama «si ninguna [ola histórica es
comparable], P2, R1, R2 y R3 son NO-CONSTRUIBLE» no se dispara, porque 2021 sí lo es y
es la ola de la que `P2` (persistencia), `R1` (interacción cruda), `R2` (encogida) y
`R3` (ajuste proporcional iterativo) toman su historia. Lo que se pierde no es el
retador: es la **λ estimada**. `R2` entra al lote con **λ = ½ fija y declarada**, que es
exactamente el `S½` que el piloto 3 midió.

**El silencio no es un valor, así que se dice también lo que no cambia:** `P2`, `R1` y
`R3` se construyen igual que en los pilotos 1 y 3, sobre 2021, sin tocar nada de esta
nota.

## 5 · La bifurcación, con opciones y recomendación — para mesa

Hay **una** decisión que cambia el entregable y no es del ejecutor. Se pregunta aquí y
el acto sigue con todo lo demás (D-19).

> **¿Se admite 2018 como segunda ola histórica, bajo un desenlace armonizado `D8`?**

- **Opción A — no (lo que esta nota aplica hoy).** `R2 = λ = ½` para los catorce pares.
  Cuesta: se renuncia a estimar cuánto se repite la interacción; `R2` entra con el
  mismo encogimiento fijo que ya se midió en el piloto 3.
- **Opción B — sí, armonizando en las dos olas.** Se define `D8` quitando la vía 8
  **también de 2021**, se restringe **2021 a 18-70** para igualar el universo, se
  estima `λ` de la estabilidad de la interacción `2018 ↔ 2021` **en `D8`**, y esa `λ`
  se aplica a la interacción `2021 → 2024` que se emite en `D9`. Cuesta: dos aperturas
  más (2018 y un segundo pase de 2021), un estimando auxiliar que hay que declarar
  entero, y una `λ` estimada sobre un universo que no es el de emisión.
- **Opción C — sí, sin armonizar.** Estimar `λ` con `D9`(2021) contra `D8`(2018).
  **No se recomienda y se nombra para descartarla por escrito**: es exactamente comparar
  dos escalas sin enlace y dos universos distintos.

**Recomendación de este acto: la A.** Tres razones. (i) Es lo que la firma F2 ya
dictamina para el caso «solo una ola comparable», y el caso se cumple. (ii) El costo de
B es real y su beneficio es incierto: `λ` se estimaría con **una sola** pareja de olas,
que es el mínimo posible, sobre un desenlace auxiliar y un universo truncado. (iii) El
piloto 3 ya midió que lo que importa es **encoger**, no el valor fino de `λ`: la
interacción cruda erró 10.6 pp, la encogida 1.9 y el piso 3.4 — la distancia entre
`λ = ½` y una `λ` estimada con ruido es pequeña frente a la distancia entre encoger y no
encoger.

Si mesa toma B, lo que cambia es la spec: `R2` pasaría a llevar dos miembros (`S½` y
`Sλ`) y el COMMIT-1 tendría que congelar el `D8` armonizado y el recorte a 18-70 antes
de abrir 2018. La tabla de comparabilidad ya trae todo lo que esa decisión necesita y no
habría que releer un solo reactivo.

## 6 · Lo que este acto **no** hizo, y por qué

No abrió microdato de ninguna ola (PARO a del encargo), no congeló nada (la spec sale
como **PROPUESTA**), no corrió los LLM (el paquete queda listo para que mesa lo corra
por CLI, `FP-228`) y no movió ningún contador numérico.

## 7 · Módulo de auditoría (§5 de las instrucciones)

Este artefacto **no afirma nada sobre México**: es una nota de procedencia sobre
instrumentos de captación. Las afirmaciones sobre México viven en la spec del lote, que
trae su propio módulo. Aun así, tres cosas que esta nota sí debe dejar dichas:

- **¿Cuántos contadores movió este trabajo?** **Cero.** Se dice en la primera línea.
- **¿Qué afirmación sobre el estado del corpus fue escrita a mano y no derivada?**
  Ninguna cifra de esta nota se tecleó: los conteos de filas salen de la lectura de los
  archivos, los sha256 del manifiesto, y los tres números del piloto 3 (10.6 · 1.9 ·
  3.4 pp; 1.47 pp con IC95 [0.44, 2.12]) se citan del encargo, que a su vez los toma de
  la rama de `PR #961` — **procedencia de tipo (3), reportada**, y así se rotula: no
  entran al canon por esta nota.
- **¿En qué escala está cada cantidad?** Todo lo de esta nota es conteo de reactivos y
  de filas de catálogo. Los `pp` citados son del piloto 3 y no se comparan contra nada
  de aquí.
