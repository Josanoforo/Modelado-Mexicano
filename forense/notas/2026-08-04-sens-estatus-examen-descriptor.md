# sens_estatus — examen de descriptor (encargo hitoE §17)

**Sesión-tipo:** lectura de descriptor. No se abrió microdato, no se
estimó nada. Ubuntu (`data/raw/` presente en disco, no se necesitó §1-bis).
Fecha: 04/ago/2026. No mueve el contador de `canon/modelo-decision-v4_0.md`.

**Encargo verificado.** `hitoE §17` (PR #62, `c3b3669`, verificado contra
`origin/main` — el `main` local del worktree estaba desactualizado en PR
#57 y se llevó a `c3b3669` solo para lectura, sin tocar la rama de trabajo
de nadie) — dividió `§14.4`: `aversion_riesgo` es límite verificado (un
candidato, ENIF `P5_23`/`P5_24`, examinado y descartado — mide
conocimiento de protección de depósitos IPAB, no aversión), pero
`sens_estatus` **no tenía ningún candidato examinado** — el veredicto de
P2 (`forense/notas/2026-08-01-p2-momentos-atributos.md` §2.c/§2.d, :234,
:268) es una limitación del instrumento de catalogación ("inventario solo
trae filas sí/parcial, no distingue 'no reportado' de 'no existe'"), no un
hallazgo sobre las fuentes. Este acto va a la fuente.

## 1 · Constructo buscado

Frase-criterio, escrita antes de abrir ningún descriptor: **"disposición
del sujeto a asignar valor a marcadores de estatus, prestigio o imagen
social en su propia decisión de consumo o ahorro"**.

Tres cosas que se confunden con el parámetro, declaradas antes de mirar:

- **Gasto observado en bienes de estatus** (ENIGH `gastotarjetas`, gasto en
  marcas) → es el **desenlace**, no el reactivo. Usarlo como C1 es
  circular: mismo fallo C3 que `horizonte_temporal` (PR #57, posición 4) —
  regresar el desenlace sobre sí mismo.
- **Percepción de desigualdad o movilidad social** → juicio sobre la
  sociedad, no sensibilidad propia. No se encontró ningún reactivo de este
  tipo tampoco (ver §3).
- **Aspiración declarada / satisfacción con el nivel de vida** → adyacente,
  no el mismo constructo. Tampoco se encontró reactivo de este tipo en los
  cinco instrumentos (ver §3).

## 2 · Método

`pdftotext -layout` sobre los cuestionarios/descriptores de los cinco
instrumentos en disco, barrido de vocabulario (`estatus`, `prestigi`,
`aparent`, `ostenta`, `presum`, `imagen social`, `marca reconocida`, `qué
dirán`, `clase social`, `nivel social`, `posición social`, `envidia`,
`admirac`, `comparación social`, `conspicu`, `nivel de vida`,
`desigualdad`, `movilidad social`, `aspiración`, entre otras variantes) más
lectura del listado de módulos/tablas de ENIGH (nombres de tabla vía
`zipfile.namelist()`, sin extraer contenido — ENIGH no tiene cuestionario
en papel, solo diccionarios de datos por tabla). Sin abrir microdato en
ningún caso.

## 3 · Candidatos examinados

| instrumento | edición(es) leídas | código / ubicación | descriptor literal | universo | veredicto |
|---|---|---|---|---|---|
| ENIGH | 2022 (única en disco) | módulo `gastotarjetas` (`tarjeta`/`pagotarjet` + gasto por categoría) | Gasto reportado pagado con tarjeta de crédito/débito, por categoría de bien | Hogares con gasto por tarjeta | **NO SIRVE** — es el desenlace conductual (ya documentado, P2 §2.d, `dinero.consumo.estatus_mediado_por_credito`, IDENTIFICADO como desenlace), no una disposición declarada. Usarlo de C1 sería circular (mismo fallo C3 de PR #57) |
| ENIGH | 2022 | 17 módulos de la edición (agro\*, concentradohogar, erogaciones, gastoshogar, gastospersona, gastotarjetas, hogares, ingresos\*, noagro\*, población, trabajos, viviendas) — listado completo de tablas | — | — | **NO SIRVE (estructural)** — ningún módulo es de opinión/actitud; ENIGH no tiene batería declarativa, solo registro de gasto e ingreso |
| ENIF | 2018, 2021, 2024 (cuestionarios completos) | — (barrido de vocabulario, cero coincidencias) | — | — | **NO SIRVE** — cero reactivo de estatus/prestigio/imagen social en las tres ediciones |
| ENIF | 2018/2021/2024 | `P5_15_5`/`P6_11_5`/`P8_12_5` | "¿Comparó [el producto] con la recomendación de un especialista/analista?", dentro de batería con recomendación de conocidos, publicidad, comparadores | Personas con producto financiero contratado en los últimos 12 meses | **NO SIRVE** — mide fuente de información previa a la compra (ya usado como candidato de `informacion.deferencia`, P2 §3.9), no valoración de marcadores de estatus. Descartado por descriptor, no por parecido de nombre |
| ENVIPE | 2024 (cuestionario principal + módulo) | — (barrido de vocabulario, cero coincidencias) | — | — | **NO SIRVE** — cero reactivo de estatus/prestigio/imagen social |
| ENCIG | 2021 (cuestionario), 2023 (estructura de base de datos con columna "Pregunta" — sin cuestionario en papel independiente en esta edición, mismo límite documentado en `forense/notas/2026-07-31-inventario-segmentacion.md`) | — (barrido de vocabulario, cero coincidencias) | — | — | **NO SIRVE** — cero reactivo de estatus/prestigio/imagen social |
| ENCUCI | 2020 (única edición existente, `FD_ENCUCI2020.pdf`) | ítem 4.1 | "¿Qué tan orgulloso(a) está usted de ser mexicano(a)?" | Población 18+ | **NO SIRVE** — orgullo nacional/cívico, no sensibilidad a marcadores de estatus personal. Constructo distinto (identidad nacional), no adyacente al de §1 |
| ENIGH/ENIF/ENVIPE/ENCIG/ENCUCI | todas las anteriores | — (barrido de "nivel de vida", "desigualdad", "movilidad social", "aspiración") | — | — | **NO SIRVE (nulo)** — tampoco hay reactivo de los dos constructos adyacentes declarados en §1 (percepción de desigualdad/movilidad; aspiración/satisfacción con nivel de vida). Se declara para que quede explícito que no se sustituyó `sens_estatus` por uno de ellos a falta de candidato |

No se abrió microdato en ningún caso. No se resolvió por parecido de
nombre: cada fila cita el descriptor literal leído.

## 4 · Rama de conclusión

**Ninguno sirve.** Los cinco instrumentos permitidos (ENIGH, ENIF, ENCIG,
ENCUCI, ENVIPE), en las ediciones presentes en `data/raw/`, no contienen
ningún reactivo — reportado o no-reportado-pero-existente — que mida
"disposición a asignar valor a marcadores de estatus o prestigio en la
decisión de consumo" según la frase-criterio de §1. Se examinó
explícitamente el módulo de gasto por tarjeta de ENIGH (el desenlace ya
conocido) y se descartó por circularidad, no por no haberlo visto. Se
examinó explícitamente el ítem de "orgullo de ser mexicano" de ENCUCI y la
batería de fuente de información de ENIF, y ambos se descartan por
descriptor, no por intuición.

**`sens_estatus` pasa de "no examinado" a "límite verificado".** El
fundamento ya no es la limitación del instrumento de catalogación (P2
§2.c/§2.d) sino la ausencia confirmada en la fuente misma, en los cinco
instrumentos permitidos. Levantar este límite exigiría un instrumento
fuera del perímetro actual (p. ej. ENASEM, MxFLS/ENNViH, o una encuesta de
valores) — no examinado aquí; ese es encargo de otra sesión.

## 5 · Contaminación declarada (ADR-46(4), conservador)

Esta sesión leyó, y por tanto queda inhabilitada para pre-registrar
contra:

- **ENIF** — cuestionarios 2018, 2021, 2024 (texto completo, `pdftotext`)
- **ENVIPE** — cuestionario principal 2024, cuestionario módulo 2024
- **ENCIG** — cuestionario 2021, estructura de base de datos 2023
- **ENCUCI** — `FD_ENCUCI2020.pdf` (formato/descriptor de base de datos)
- **ENIGH** — únicamente el listado de nombres de tabla/módulo de la
  edición 2022 (vía `zipfile.namelist()`, sin extraer ni leer contenido de
  ningún diccionario de datos ni CSV). Declarado por conservadurismo
  aunque la exposición fue de nombres de tabla, no de reactivos

No se abrió `milpa/procedencia.yaml`, `canon/modelo-decision-v4_0.md`,
`canon/gobernanza-v1_15.md`, ni `data/manifiesto.yaml`. No se movió
ningún contador. No se reclasificó ninguna fila de `hitoE §14.3`/`§14.4`
(ambas quedan íntegras, append-only, por la misma disciplina que usó
`§17`).

## 6 · Constancia de caducidad

Este acto — examen de descriptor sobre `sens_estatus`, con resultado
"ninguno sirve" fundado en descriptor literal, no en supuesto — **cuenta
como el primero de los tres actos de la condición de caducidad**
mencionada en `hitoE §17` para no seguir citando `sens_estatus` como el
mismo tipo de límite que `aversion_riesgo` sin haberlo verificado.

## 7 · Nota sobre procedencia de instrucciones

No apareció en el contexto de esta sesión ninguna instrucción de
procedencia no identificable. Todo lo ejecutado proviene del encargo
recibido y de lo verificado contra `origin/main` (`c3b3669`, PR #62) y los
archivos que ese commit ya trae.
