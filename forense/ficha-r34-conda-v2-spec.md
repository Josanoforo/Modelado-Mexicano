# Ficha · condición A de `R3.4`, re-especificada — spec v2

> | | |
> |---|---|
> | **QUÉ ES** | La condición A de `R3.4` re-especificada sobre **pares que difieren en una sola variable**, con variable dependiente declarada. Sustituye la A de `ADR-25`/`ADR-37`, que compara canales completos. |
> | **ESTADO** | **CONGELADA antes de abrir payload.** Ninguna cifra de resultado vive en esta ficha: el resultado va en la nota de cierre del acto, y el primer resultado que produzca este procedimiento es el que se reporta. |
> | **QUIÉN LA SELLA** | Nadie aquí. `FP-104` queda ABIERTA; la condición A es gate del programa y **no se auto-adjudica**. |
> | **ACTO** | `ACTO R34-CONDA-V2`, 24/ago/2026. Firma que ejecuta: `ADR-145` (D3, reformulación de `FP-104`) + `ADR-146` (vocabulario de `EMISOR-M-2`). |

---

## 1 · Por qué la A vieja no sirve

`ADR-37` corrigió la v0.1 del gate porque el criterio estaba escrito **en términos de canal**, y la corrección
no llegó a la condición A: la A vigente sigue comparando CoDi contra «el canal retail-efectivo tipo OXXO Pay»
(`forense/COERCION-Y-ADOPCION-rediseno-2026-08-20.md:16`). Un canal completo difiere en muchas variables a la vez,
así que un resultado no dice **cuál** de ellas lo produjo — que es exactamente lo que el Bloque C existe para impedir.

`rediseño:103`: «Re-especificar la condición A para que compare pares que difieran en **una** variable.
Con la tabla de §4 hay al menos cuatro pares así, **y ninguno es el que la spec fijó**.»

Los cuatro pares (`rediseño:74-75`, `v0_1:44`):
`PANAUT ↔ Registro-2026` (dato_sensible) · `DiMo ↔ CoDi` (friccion_uso) · `Pix ↔ CoDi` (lado_obligado) · `CoDi ↔ SPEI` (utilidad_marginal_sobre_sustituto).

---

## 2 · Par primario — `CoDi ↔ SPEI`

**Variable aislada:** `utilidad_marginal_sobre_sustituto`.
**Por qué aísla:** `rediseño:74` — «CoDi contra SPEI aísla **utilidad marginal**, no riesgo fiscal — porque
**SPEI también es trazable al SAT** y aun así se adoptó.»

Verificado contra la tabla de casos (`rediseño:60-61`), fila por fila:

| variable | SPEI | CoDi | ¿difiere? |
|---|---|---|---|
| Coerción | no | no | = |
| Sanción | — | — | = |
| Dato sensible | no | no | = |
| Lado obligado | — | ninguno efectivo | = *(ver nota)* |
| **Sustituto previo** | **—** *(es el incumbente)* | **SPEI, fuerte** | **← la variable aislada** |

*Nota sobre `lado_obligado`:* la tabla escribe «—» para SPEI y «ninguno efectivo» para CoDi. Es la misma sustancia
—nadie quedó obligado— con distinta redacción; el «efectivo» alude a que el diseño de CoDi sí contemplaba
obligar a la banca y no mordió. Esa es precisamente la variable del par `Pix ↔ CoDi`, **no la de éste**, y por eso
aquí se trata como constante.

### ⚠️ Confusor NO listado en las cinco columnas de la tabla: el tiempo en mercado

La tabla no tiene columna de antigüedad, y los dos lados están separados por **quince años**: SPEI **2004–**,
CoDi **2019–** (`rediseño:60-61`). El «sustituto previo» de SPEI figura como `—` **porque SPEI llegó primero**,
no porque no lo tuviera. Entonces, comparar quién usó cada servicio en 4T-2024 mezcla dos cosas:

- la **utilidad marginal sobre un sustituto** (la variable que el par dice aislar), y
- el **tiempo disponible para acumular usuarios** (≈20 años contra ≈5).

**El par difiere en una variable *declarada*, pero no en una variable *real*.** Esta ficha lo declara antes de
correr en vez de descubrirlo después: cualquier razón entre los dos lados hereda este confusor, y ninguna lectura
puede atribuir la brecha entera a la utilidad marginal. Es una razón adicional —independiente del hueco de escala
del §3— por la que este par **no adjudica solo**.

Mitigación posible, **no ejecutada aquí** (exige serie histórica que el corpus no tiene materializada): comparar
las dos series **a la misma edad de servicio** (CoDi a los 5 años contra SPEI a los 5 años, es decir 4T-2024 contra
≈2009) en vez de en el mismo año calendario. Queda nombrada para el sucesor con red.

**Variable dependiente declarada: `adopcion`.**
Justificación: `adopcion` = conducta de **elección**; `cumplimiento` = conducta bajo **mandato con sanción**
(`v0_1:13-14`). Ni CoDi ni SPEI son obligatorios para el usuario (`lado_obligado = ninguno` en ambos), así que lo
que se observa es elección, no cumplimiento. Declararlo importa: bajo mandato la literatura dice que medir «uso»
como si fuera elección es engañoso (`rediseño:33`), y `R3.4` confundía las dos en una.

---

## 3 · Serie y unidad por lado — declaradas ANTES de abrir payload

### Lado CoDi — hay TRES constructos y esta spec elige uno

| # | constructo | qué es | dónde vive |
|---|---|---|---|
| (i) | **cuentas validadas** | stock acumulado, monótono creciente | `banxico_codi_cuentas_validadas_x_mil_hab_trimestral.xlsx`, hojas `Cifras_Estatales` / `Fuente_LADA`, 17 trimestres 2022-T1→2026-T1 |
| (ii) | **cuentas con pago/cobro** | uso: transaccionó ≥1 vez | Cuadro A 10 de los Informes IdMF (2022 pág. 70 trimestral; 2023 pág. 72 mensual) · `CF882` (sólo 3 días) |
| (iii) | **cuentas activas trimestrales** | — | **NO EXISTE** como serie propia distinta de (i) o (ii) |

**Elegido: (ii), uso — «cuentas que utilizaron CoDi durante el trimestre».**

**Por qué (i) NO sirve.** Es un stock acumulado y monótono: nunca baja, porque una cuenta validada en 2022 sigue
contando en 2026 aunque jamás se haya usado. La regla que `R3.4` prueba es sobre **adopción**, es decir conducta;
un stock de registros mide **acceso**, no uso. Regla ya adoptada por el programa: «**acceso ≠ uso**» (Findex,
`rediseño`), y la definición se impone antes de medir (GSMA/CGAP: registrado vs. activo a 30/90 días; globalmente
~75 % de las cuentas registradas está inactivo cada mes — elegir mal cambia la respuesta por un factor de ~4).

**Por qué (iii) NO sirve.** No existe. Verificado sobre los 20/20 archivos del directorio CoDi/SPEI. La palabra
«activas» colisiona en el corpus con **≥3 sentidos** incompatibles: stock vigente (hoja `Metadatos` del xlsx),
transaccionó-alguna-vez (nota al pie del Cuadro A 10) y variable-aún-sin-fijar (`hitoD-preregistro-v2_0.md:834`).
Una spec que dijera «cuentas activas» sin más heredaría la ambigüedad en vez de cerrarla.

**Serie exacta del lado CoDi:** Informe Anual IdMF 2024, pág. impresa 18 (física 28/95) —
25.0 mil cobradores + 216.4 mil pagadores + 16.4 mil combinada = **257.8 mil cuentas**, ventana **4T-2024**.

⚠️ **Dos reservas que van pegadas a esta cifra, no en una nota al pie:**
1. **El informe NO la llama «activas».** La palabra no aparece: 0 coincidencias en 5,698 líneas del volcado
   completo del informe 2024 (control positivo en el mismo comando: «CoDi» = 45). El texto dice «cuentas que
   **utilizaron** CoDi». Cualquier equivalencia «usó en el trimestre» = «cuenta activa» es **firma de mesa**, no
   una lectura que esta spec pueda tomarse.
2. **No es un techo.** El propio informe dice que esas cuentas **cayeron** contra el mismo trimestre del año
   anterior, por una dificultad operativa de una institución participante (nota 17: tres participantes no ofrecían
   el servicio). Usarla como «techo» tergiversa la fuente.

### Lado SPEI

**Serie exacta:** Informe Anual IdMF 2024, pág. impresa 9 (física 19/95) — **73.5 millones de personas físicas**
que realizaron operaciones durante el **4T-2024** (+23.6 % interanual; ≈72.8 % de la población mayor a 15 años).
Misma ventana temporal que el lado CoDi, mismo constructo (usó el servicio en el trimestre), misma fuente primaria.

### Escala — y el hueco que esta spec NO cierra

| lado | cantidad | **unidad** |
|---|---|---|
| CoDi | 257.8 mil | **cuentas** |
| SPEI | 73.5 millones | **personas físicas** |

**Son escalas distintas.** `instrucciones-proyecto-v2_11.md:85` (A-bis regla 3), verbatim:

> «Toda cantidad medida entra con su escala declarada, y **no se compara contra otra escala**. […] Está
> **prohibido** escribir "el medido es X, el asignado era Y, difiere en Z%" entre escalas distintas: es un
> **error de categoría, no una medición**.»

**⛔ HUECO DECLARADO — la función de enlace `cuenta ↔ persona` no está firmada.**
Sin ella, la razón entre los dos lados **no se computa** en este acto. No es una omisión de esfuerzo: es la regla.
El par tiene mismo constructo y misma ventana; lo único que falta es la función de enlace, y esa es **firma de mesa**.

**Lo que está en juego, escrito por adelantado para que nadie lo descubra después:** las dos lecturas disponibles
dan veredictos opuestos sobre el mismo umbral.

| lectura | razón | vs. umbral `A < 10 %` | veredicto que implicaría |
|---|---|---|---|
| 257.8 mil cuentas / 73.5 M personas | **0.35 %** | `<10 %` | A **pasaría** |
| 0.09 / 0.71 (capa máquina, pre-D3) | **12.7 %** | `≥10 %` | A **fallaría** |

La primera es justo la comparación que A-bis 3 prohíbe. La segunda es el diagnóstico **pre-D3**, que esta spec
**no hereda** — `ADR-146` declara expresamente que no re-especifica la condición A, y el vocabulario nuevo no
adjudica ningún caso. **Ninguna de las dos se adopta aquí.**

---

## 4 · Par de control — `DiMo ↔ CoDi`

**Variable aislada:** `friccion_uso` — el componente que la Nota 3 declara sin disparador.
`rediseño:75`: «mismos rieles, mismo emisor, misma trazabilidad, **distinta fricción de UX** (alias telefónico contra QR)».

**NO corre en este acto.** Razón medida, no presumida: **no hay ninguna serie primaria de DiMo en el corpus.**
La única cifra disponible (~7 M cuentas) es de terceros, en la tabla del documento de mesa, y tiene **prohibida**
la entrada al motor sin acto de verificación propio (`rediseño:9`; `v0_1:29,48`). Correrlo con esa cifra violaría
la misma regla que este acto existe para respetar.

Queda para sucesor **CON red**, nombrado: adquirir la serie primaria de DiMo (Banxico) y sólo entonces computar el par.

---

## 5 · Umbral, escala de lectura y precedencia

**Umbral heredado, sin recalibrar:** `A < 10 %` — `ADR-37`, `canon/gobernanza-v1_15.md:269`, `emisor.py:56`.
Rotulado **ASIGNADO, no medido** (`gobernanza:277`, `hitoD:825-829`). Esta spec **no lo mueve**: cambiar el umbral
en el mismo acto que cambia el comparador haría inseparables los dos efectos.

**Escala de lectura de la condición A re-especificada** — cuatro filas mutuamente excluyentes:

| fila | condición | lectura |
|---|---|---|
| **A1** | razón computada con enlace firmado, y `< 10 %` | A **satisfecha** — propuesta, no sellada |
| **A2** | razón computada con enlace firmado, y `≥ 10 %` | A **no satisfecha** — el par refuta la reproducción |
| **A3** | par bien formado (mismo constructo, misma ventana) pero **enlace de escala sin firmar** | **no se puede evaluar** — no es fallo del par, es firma faltante |
| **A4** | el par no se puede formar con fuente primaria (falta serie, ventana o constructo) | **inejecutable** — sube a adquisición |

**Regla de precedencia (declarada al sellar, no después):** se leen en orden **A1 → A2 → A3 → A4**, y cada fila
exige el estado de las previas ya resuelto. **A3 y A2 son disjuntos por definición**: «no se pudo evaluar» y
«se evaluó y no cruzó» no son el mismo estado, y confundirlos es exactamente el defecto que la escala de la ficha
`R3.4` ya declara (`hitoD:869`). Si aparece un caso intermedio no previsto, se declara en nota fechada aparte
**sin editar esta fila** — mismo precedente que R7.2 (Notas 11-13).

**Fila de no-refutación (B-bis, `instrucciones-proyecto-v2_11.md:113`)** — declarada antes de correr:
si el par **no** refuta la regla, eso deja la regla **acotada**, no corroborada. Un solo par que no refuta no
corrobora la regla general: aísla una variable de seis, en un caso, en una ventana. La lectura «CoDi fracasó por
falta de utilidad marginal» **no** se autoriza por este par. `falsador débil` se declara si el enlace no se firma
(fila A3), porque entonces el par no llegó a probar nada.

**Reserva de intervalo (A-bis contraparte, `:89`):** ninguna de las cifras disponibles trae intervalo de confianza
— son puntos de informe anual y agregados de un xlsx. Por tanto, aun con el enlace firmado, **un punto que cruce
el umbral sin IC que lo despeje no adjudica solo**: se reporta como propuesta con la reserva escrita, y adjudica mesa.

---

## 6 · Universo y ventana

**Universo:** México, cuentas/personas físicas de los dos servicios de pago, sin desagregación estatal
(existe a nivel estatal para CoDi (i), pero el lado SPEI sólo está disponible nacional — desagregar un lado y no
el otro sería otra asimetría de escala).
**Ventana:** **4T-2024**, cerrada y común a los dos lados. Elegida porque es la única ventana en que ambos lados
tienen cifra publicada del mismo constructo en la misma fuente primaria.

---

## 7 · Limitaciones pre-declaradas

1. **El gate no separa coerción de fricción** (`hitoD:803-805`, `gobernanza:278`). Aun si A se satisficiera, la
   lectura «el mecanismo **ES** riesgo fiscal y no fricción» queda **PROHIBIDA**. Este par aísla utilidad marginal,
   que es un **tercer** componente — y no autoriza tampoco la lectura simétrica.
2. **Las series vivas `CF881-CF885` cubren 3 días** (25-27/jul/2026), en las 290 series-hoja de los 5 cuadros, sin
   excepción. Rol declarado: **verificación cruzada puntual, NO serie**. El histórico sale del xlsx y de los Informes.
3. **Dos series homónimas «cuentas validadas»** conviven sin reconciliar: la diaria `SF335591` (Flujos, no monótona,
   altas del día) y la trimestral del xlsx (Acumulado histórico, monótona). Esta spec usa **ninguna de las dos**
   (elige el constructo (ii)), pero la colisión de nombre queda declarada para quien vuelva.
4. **La granularidad del Cuadro A 10 cambia entre ediciones** (trimestral en el informe 2022, mensual en el 2023),
   sin reconciliación publicada. Por eso la ventana se fija en 4T-2024 y no en una serie larga.
5. **Cinco de los seis disparadores de `EMISOR-M-2` no están cableados** a ninguna regla de `milpa/tramite.yaml`
   (`ADR-146(c)`). Esta spec los usa como **vocabulario declarativo** del par, no como cantidades medidas por el motor.
6. **`gate_r3_4()` no consume celdas-D.** La unión «celda de `EMISOR-M-2` validada → gate R3.4» **no existe en el código**
   (0 llamadas cruzadas sobre 136 archivos `.py`). Esta spec la nombra como **diseño nuevo**, no la da por existente.
7. **La fila A de la escala de `R3.4` exige además reconciliar la discrepancia 3.09 M vs 21.8 M/17.8 M**
   (`hitoD:864`), y esa discrepancia **no reconcilia** contra fuente primaria de este corpus. Aun con A satisfecha,
   la ficha `R3.4` no podría declarar fila A por esta vía.
8. **El par difiere en una variable declarada, no en una variable real** (§2): SPEI y CoDi están separados por
   **15 años de mercado**, confusor que las cinco columnas de la tabla de casos no encodan. Aun con el enlace de
   escala firmado, la brecha no es atribuible entera a `utilidad_marginal_sobre_sustituto`. **Dos reservas
   independientes**, entonces, pesan sobre este par: la de escala (§3) y la de antigüedad (§2).

---

## 8 · Cláusula de cierre

**El primer resultado que produzca este procedimiento es el que se reporta.** Esta ficha queda congelada antes de
abrir payload; si la corrida la desmiente, se corrige **hacia adelante**, en un commit que lo diga, nunca editando
esta ficha hacia atrás.

---

## 9 · Enmienda fechada — firma de mesa L3/L4, 25/ago/2026 (`ACTO SELLA-AGO25-F`)

**L4/`FP-130`, opción `a` — «cuentas activas» se retira, queda el término textual.** Mesa confirma: la paráfrasis
«cuentas activas» **no** es el término del corpus fuente y **no** se adopta en ninguna forma — el §3 de esta misma
ficha ya la había apartado por análisis propio (constructo (iii), «NO EXISTE»), y esta firma la sella como decisión,
no como cautela. Grep de `activas` sobre este archivo (`grep -n "activas" forense/ficha-r34-conda-v2-spec.md`,
corrido antes de esta enmienda): **4 coincidencias**, líneas 82, 93, 95, 101 — las cuatro dentro de §3, todas en el
razonamiento que **descarta** el constructo (iii) y elige (ii); ninguna la usa como término operativo. **Cero sitios
vivos que enmendar**: el término sellado que gobierna esta ficha ya era, antes de esta firma, «cuentas que utilizaron
CoDi durante el trimestre» (§3, constructo (ii)) — el mismo que la opción `a` exige. Historia intacta, sin editar
§3 hacia atrás.

**L3/`FP-129`, opción `b` — re-especificar sobre la misma unidad, no declarar enlace ni dejar en A3.** Mesa rechaza
tanto declarar una función de enlace `cuenta ↔ persona` (opción `a`) como dejar la condición A congelada en fila A3
sin veredicto (opción `c`, el estado que esta ficha traía en §5 antes de hoy). En su lugar, ordena **eliminar el
cruce de escalas re-derivando ambos lados en la misma unidad** — no convertir cuentas a personas por una regla de
enlace inventada, sino localizar en los Informes Banxico ya presentes en el corpus (los mismos IdMF que ya citan
§3) una serie que reporte **el mismo constructo, en la misma unidad, para los dos servicios**, en vez de mezclar
«cuentas» (CoDi) con «personas físicas» (SPEI). Esta ficha **no localiza esa serie aquí** — es trabajo de un acto
propio, con perímetro de búsqueda en el corpus ya adquirido, no de adquisición nueva. Fila `FIRMADA` nueva en el
tablero, `FP-136`, nombra ese acto sucesor.

**Efecto sobre `FP-104` y la escala de §5.** La fila `A3` («no se puede evaluar») que el §5 declaraba como estado
vigente **no se retira todavía**: sigue siendo la lectura correcta *hasta que* `FP-136` localice la serie homogénea
y produzca una razón en una sola unidad. Esta enmienda no re-corre el procedimiento ni adjudica `A1`/`A2` por
adelantado — solo cierra la pregunta de **qué camino** toma la ficha (re-especificación por unidad homogénea, no
función de enlace), dejando la ejecución al acto sucesor. `FP-104` se actualiza para citar esta decisión y sigue
`ABIERTA` hasta que `FP-136` corra y la escala de §5 se reevalúe con la serie nueva.

**Perímetro de esta enmienda.** Solo este §9, añadido; ningún párrafo de §1–§8 se edita hacia atrás.
