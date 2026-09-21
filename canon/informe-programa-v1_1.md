# Informe del programa · v1.1

**Modelado Mexicano — «Psicología del Mexicano Contemporáneo».**
Documento del programa, escrito para mesa y para un comprador escéptico.
21 de septiembre de 2026.

### `informe-programa` · **v1.1** · DOCUMENTO DEL PROGRAMA

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_1.md` |
> | **REEMPLAZA A** | `informe-programa-v1_0.md` (15/sep/2026), que **no se edita** — E.3: una pieza sellada es evidencia histórica. La v1.0 es anterior a los tres pilotos y queda **VENCIDA EN ALCANCE** (A.10): su universo creció, no fue refutada. |
> | **VERIFICAS ASÍ** | cada cifra del cuerpo trae, en su propia línea o en el pie de su tabla, **el comando que la produce o el `RESULT` sellado que la contiene**. Las cifras de los tres pilotos salen todas de `python3 tools/informe_pilotos.py --json`, que además **se verifica a sí mismo**: cada MAE derivado se compara contra el MAE sellado de la corrida correspondiente y la salida trae la columna `check` (hoy: **COINCIDE en los 12 candidatos de los tres pilotos**). |
> | **NOMBRE ESTABLE** | **`informe-programa`** — cítalo así, **nunca por nombre de archivo** |

> **Estampa de universo (A.10), global.** Derivado contra `origin/main = 55c8d57`
> (merge de `PR #961`, el piloto 3, 21/sep/2026), en un acto de **NUBE sin corpus
> montado** (`tools/entorno.py --arranque`: `senal-corpus: montado=NO
> archivos_examinados=0`; `data-raw-en-este-worktree: NO`; red
> `DENEGADA-POR-POLITICA`). **Fuentes: sólo el registro derivado y las corridas
> selladas que ya viven en el repo.** Este documento no abre microdato, no llama
> a ningún modelo, no sella ninguna corrida y **no adjudica nada**.
>
> **Lo que este documento NO es.** No es SALIDA para cliente: es su insumo. No
> re-abre ningún veredicto. No adopta ningún candidato. El veredicto del piloto 3
> sigue siendo `FALSADOR-DEBIL` con `champion_actual: NINGUNO`, y nada de lo que
> se lee abajo lo mueve.

---

## 0 · En una página

El programa mide conducta en México con encuestas públicas (INEGI y afines) y
construye, sobre esa medición, un modelo de decisión segmentado. Lo que lo
distingue no es el modelo: es el aparato que obliga a que **toda cifra declare
antes de verse** contra qué se va a comparar, y a que el resultado se selle sin
poder reescribirse.

**La pregunta que este informe contesta es una sola: ¿el motor sabe predecir una
celda que no ha visto, y sabe cuánto se equivoca?** La respuesta honesta, hoy:

- **Sí, en cruces, tres veces, con 35 celdas.** El piso C2 (marginales de la
  misma ola sin interacción) erró **1.47 pp** en el piloto 1, **1.57 pp** en el
  piloto 2 y **3.41 pp** en el piloto 3 — cada uno en su propia unidad, que no
  es la misma (§2).
- **Su intervalo atrapa la verdad 26 de 35 veces** (74%), y ese 74% es peor de
  lo que parecía con dos pilotos (18/20 = 90%): el tercer dominio lo bajó (§2.3).
- **No sabe cuánto se equivoca fuera de cruces**, y por decisión de mesa del
  21/sep no lo promete.
- **No le gana a un modelo de lenguaje en el nivel nacional**, y la corrida que
  lo midió está sellada (§4).
- **El primer indicio de valor añadido apareció en el piloto 3** — la interacción
  *encogida* erró 1.95 pp contra los 3.41 pp del piso — **y no adjudica nada**
  (§3).

**Contadores que movió el trabajo que produjo este informe** (v2.3 del módulo de
auditoría): **uno**. `celdas_validadas` pasó de **73 a 88** al dejar de contarse
desde una lista escrita a mano. Ninguna corrida nueva se selló, ningún candidato
se adoptó.

---

## 1 · El marcador, en dos columnas que nunca se mezclan

Firma de mesa, 21/sep/2026, verbatim: **«Rótulo PROSPECTIVA/RETROSPECTIVA en
todo marcador»** (`forense/firmas-pendientes.tsv`,
`FP-260921-GEN2-MARCADOR-E-INFORME-1-48d4-01`).

El marcador del programa tiene 214 filas. Antes de esta versión, todas se leían
igual. El defecto que eso produce es concreto: 89 de esas 214 filas tienen un
valor emitido **y** un valor de realidad, y son **el mismo número copiado** —
el emisor y el árbitro son la misma fuente. Un lector que sume «filas con M y R»
entiende 109 predicciones donde hay 20.

La columna `prospectividad` del marcador se **deriva** (`tools/prospectividad.py`),
no se teclea: el orden sale del campo `fecha` del `ejecucion.json` sellado de cada
corrida. **`git` no se usa como fuente de orden**, y la razón es medible: el clon
de trabajo es `shallow`, y ahí la fecha de alta de
`milpa/tramite-ola5-propuesta-v0.yaml` cae *después* de una corrida sellada que
ya declara ese archivo como input. Una fecha posterior a la corrida que leyó el
archivo no es una fecha de nacimiento: es el borde del clon.

| clase | n | qué es |
|---|---:|---|
| **PROSPECTIVA** | **20** | la emisión se selló **antes** de que existiera la R contra la que se compara, y las dos fechas salen de dos `ejecucion.json` distintos |
| **RETROSPECTIVA** | **59** | la R ya existía cuando la emisión se selló |
| `IDENTICO-EMISOR-ES-ARBITRO` | 89 | M y R son el mismo número copiado. No es predicción: ni acertada ni fallada |
| `SIN-EMISION` | 30 | nada emitido que contrastar (reservada, sin piso, o diagnóstica) |
| `EMITIDA-SIN-R` | 16 | emitida y todavía sin R: reserva de evaluación viva (E.6) |
| `ORDEN-NO-DERIVABLE` | 0 | hay emisión y R, pero el orden no sale de dos sellos |

*Escala: **conteo de filas del marcador**, unidad = celda del marcador. No hay
cifra que sume PROSPECTIVA + RETROSPECTIVA, y no la habrá: son dos preguntas
distintas y sumarlas es el defecto que el rótulo existe para evitar.*
**Comando:** `python3 tools/marcador_segmento.py` (bloque `resumen.prospectividad`)
· **columna publicada:** `data/corrida0/marcador-segmento.tsv`, campos
`prospectividad` y `prospectividad_cita` (la cita nombra los dos sellos).

### 1.1 · La métrica rectora, `celdas_validadas` = **88**

Una celda cuenta como **validada** si su predicción se emitió antes de ver el
dato y se comparó contra R con error sellado. **Validada no quiere decir
acertada**: un piloto que termina en «nadie vence» o en «falsador débil» validó
exactamente tantas celdas como uno que termina en «vence».

| clase | n | escala / unidad |
|---|---:|---|
| cruce vs R (los tres pilotos) | **35** | celdas de cruce; persona (8), delito (12), trámite (15) |
| persistencia t−1 vs R | **53** | celdas marginales; persona, delito y trámite según instrumento |
| **total** | **88** | celdas validadas |
| *(no cuenta)* duelo de tres, nacional | 12 | es RETROSPECTIVO para sus tres contendientes |

*No cuentan, y se declara con su universo:* las **89** filas `IDENTICO` y las
**6** celdas de `formalidad` con piso y sin error medido.
**Comando:** `python3 tools/tablero_programa.py` → clave `celdas_validadas`.

**Qué cambió y por qué importa.** El 21/sep el piloto 3 adjudicó 15 celdas en un
tercer dominio y esta métrica no se movió: se calculaba desde una lista de **dos**
celdas-D escritas a mano dentro del código del tablero. Una métrica rectora que
hay que editar a mano cada vez que el programa avanza mide al editor, no al
programa. Ahora se deriva de **toda** celda-D con veredicto sellado, y la escala
de cada una (proporción o puntos porcentuales — un factor 100 de diferencia) se
deriva contra el `margen_material` sellado de la propia celda-D, no se teclea.
Si la escala no se deriva, **la celda no cuenta**: la métrica no sube por una
escala adivinada.

Desglose por tipo: **35 cruce · 53 marginal**. Por instrumento: ENIF 2024 (8
cruce + 28 marginal) · ENVIPE 2025 (12 cruce + 15 marginal) · ENCIG 2025 (15
cruce + 10 marginal). *Escala: conteo de celdas.*

---

## 2 · Los tres pilotos: 35 celdas, error y cobertura por candidato

Todo este apartado sale de **un** comando:
`python3 tools/informe_pilotos.py --json`. Cada MAE que aparece abajo fue
recalculado desde los `RESULT` por celda y **comparado contra el MAE sellado de
su corrida**; los 12 candidatos dan `check = COINCIDE`.

**Qué es la cobertura aquí.** Es **R dentro del IC95 del candidato**: ¿el
intervalo que el candidato emitió atrapa la verdad? El piloto 2 selló un campo
llamado `ARB-DENTRO-IC-R-C2-<celda>` que mide **lo contrario** — el punto del
candidato dentro del IC de R — y este informe **no lo usa**. Son dos preguntas
distintas y sólo la primera es cobertura.

**Intervalo binomial: Wilson (score), z = 1.959964.** No es Clopper-Pearson:
`scipy` no está en este entorno y un exacto mal implementado a mano sería peor
que un Wilson correcto. Se declara, no se esconde.

> **ADVERTENCIA QUE VIAJA CON TODO INTERVALO DE ABAJO.** Las celdas de una misma
> ola comparten marco muestral, estratos, UPM y réplicas de bootstrap. **No son
> ensayos independientes**, que es justo lo que el intervalo binomial supone.
> **Todos estos intervalos son demasiado angostos.** Se publican porque una
> cobertura sin intervalo invita a leer 7/8 como «87.5%» a secas, y eso es peor.

### 2.1 · Piloto 1 · `DIN.ahorro_solo_informal.enif2024.localidad_x_edad`
ENIF 2024 · **unidad = persona** · 8 celdas puntuadas · veredicto
`SIN-CANDIDATO-SUPERIOR`

| candidato | MAE (pp) | error máx (pp) | cobertura IC95 | Wilson 95% |
|---|---:|---:|---:|---|
| C1 · piso 2021 | 2.644 | 4.950 | 4/8 | [0.215, 0.785] |
| **C2 · piso marginal 2024** | **1.467** | 4.375 | **7/8** | [0.529, 0.978] |
| C3 · modelo de lenguaje | 10.639 | 19.103 | — *(no emitió IC)* | — |

*Escala de la tabla: **puntos porcentuales**, unidad **persona**. Las emisiones
crudas de este piloto están en proporción `[0,1]` y se convierten con factor 100,
verificado contra `margen_material = 1.466786` de la celda-D.*

### 2.2 · Piloto 2 · `TRA.evade_norma.envipe2025.escolaridad_x_dominio`
ENVIPE 2025 · **unidad = delito** · 12 celdas puntuadas · veredicto
`SIN-CANDIDATO-SUPERIOR`

| candidato | MAE (pp) | error máx (pp) | cobertura IC95 | Wilson 95% |
|---|---:|---:|---:|---|
| C1 · piso histórico | 4.315 | 12.250 | 6/12 | [0.254, 0.746] |
| **C2 · piso marginal 2025** | **1.568** | 5.436 | **11/12** | [0.646, 0.985] |
| C6 | 2.853 | 10.993 | 11/12 | [0.646, 0.985] |
| C7 | 2.665 | 9.316 | 9/12 | [0.468, 0.911] |

*Escala: **puntos porcentuales**, unidad **delito**. Un delito no es una persona:
quien sufrió tres delitos contribuye tres veces. Estos MAE **no se promedian**
con los del piloto 1.*

### 2.3 · Piloto 3 · `GOB.gobierno_digital.encig2025.edad_x_escolaridad`
ENCIG 2025 · **unidad = trámite** · 15 celdas puntuadas (de 16; una
`FUERA-DE-SOPORTE-EX-ANTE`) · veredicto **`FALSADOR-DEBIL`** ·
`champion_actual: NINGUNO`

| candidato | MAE (pp) | error máx (pp) | cobertura IC95 | Wilson 95% | vs piso C2 |
|---|---:|---:|---:|---|---|
| C1A · referencia 2021 | 10.654 | 18.569 | — *(punto sin IC, declarado)* | — | — |
| C1B · referencia 2023 | 10.519 | 16.499 | 2/15 | [0.037, 0.379] | — |
| **C2 · piso marginal 2025** | **3.411** | 12.282 | **8/15** | [0.301, 0.752] | — |
| S-MEDIO · interacción a medias | 2.310 | 9.372 | 11/15 | [0.480, 0.891] | VENCE 3 · INDECIDIBLE 12 |
| **S-LAMBDA · interacción encogida** | **1.946** | 7.168 | **14/15** | [0.702, 0.988] | VENCE 3 · INDECIDIBLE 12 |

*Escala: **puntos porcentuales**, unidad **trámite** — quien pagó la luz doce
veces contribuye doce veces. **No se promedia con persona ni con delito.***

ΔMAE sellado del retador contra el piso: **S-LAMBDA 1.465 pp, IC95
[0.439, 2.115]** (`RESULT-GOB-EXE15-ADJ-2025-S-LAMBDA-DELTA-MAE-PP` y sus
`-IC-LO`/`-IC-HI`); **S-MEDIO 1.101 pp, IC95 [0.256, 1.484]**.

### 2.4 · Los tres juntos — sólo lo que sí es la misma pregunta

Se suma **la cobertura**, que es un conteo de «cuántas veces el intervalo atrapó
la verdad» y es la misma pregunta en los tres dominios. **No se suman ni se
promedian los errores**: persona, delito y trámite son tres escalas (§4.3/§4.4).

| piso C2 | cobertura | Wilson 95% |
|---|---:|---|
| piloto 1 (persona) | 7/8 | [0.529, 0.978] |
| piloto 2 (delito) | 11/12 | [0.646, 0.985] |
| piloto 3 (trámite) | 8/15 | [0.301, 0.752] |
| **los tres** | **26/35 = 0.743** | **[0.579, 0.858]** |

**Lo que el tercer piloto le hizo a esta cifra es el hallazgo más útil del
trimestre.** Con dos pilotos la cobertura del piso era 18/20 = 0.90 y parecía una
propiedad del método. Con el tercero es 0.74, y el intervalo nominal del piso
resultó ser optimista en el dominio nuevo. Un aparato que sólo hubiera reportado
los dos primeros habría vendido una garantía que el tercero no sostiene.

---

## 3 · Qué enseñó el piloto 3

**(a) La interacción cruda es PEOR que el piso, y por mucho.** Las dos
referencias que llevan la interacción tal como la miden olas anteriores
(C1A 10.654 pp, C1B 10.519 pp) erran **tres veces más** que el piso de marginales
de la misma ola (3.411 pp). Extrapolar una interacción medida en 2021 o 2023 a
2025 costó más que no modelar la interacción en absoluto.

**(b) La interacción ENCOGIDA es la primera señal de valor añadido del programa,
y no adjudica nada.** S-LAMBDA —la misma interacción, encogida hacia cero—
erró 1.946 pp contra los 3.411 del piso, con ΔMAE 1.465 pp e IC95 [0.439, 2.115]
que no toca el cero, y su intervalo cubrió 14 de 15 celdas contra 8 de 15 del
piso. Es la primera vez en el programa que algo mejora al piso de forma medida.

**Y aun así no vence.** El criterio de adjudicación pide que el retador gane al
piso en **≥ ¾ de las celdas puntuadas** (≥ 12 de 15). Ganó en **3**; las otras
**12 son INDECIDIBLES** y **ninguna es derrota**. El veredicto sellado es
`FALSADOR-DEBIL`: la prueba no pudo decidir, no que el retador fallara. Por eso
`champion_actual` es `NINGUNO` y **el piso sigue siendo el estimador adjudicado
de sus celdas** donde lo era (A-bis 6). Un ΔMAE favorable con un criterio por
celda que no se satisface es exactamente el caso que §4 nombra: *un punto que
satisface un umbral con un IC que no lo despeja no adjudica*.

**(c) La lectura que NO se debe hacer.** «La encogida es mejor» es una frase
sobre **una celda-D, un dominio, una ola**: gobierno digital / pago de luz,
edad × escolaridad, ENCIG 2025. El propio árbitro lo selló:
`RESULT-GOB-EXE15-ADJ-2025-ALCANCE` = *«C2 sigue adoptado en DIN y TRA (A.10);
este veredicto limita sólo a gobierno_digital/luz, edad×escolaridad, ENCIG 2025»*.

---

## 4 · Qué puede afirmar el producto hoy, y qué no

**Puede afirmar, con corrida sellada detrás:**

1. Que predice celdas de cruce que no ha visto, **tres veces, en tres dominios,
   con 35 celdas**, y que el error del piso queda entre 1.5 y 3.4 pp según el
   dominio (§2).
2. Que **sabe cuánto se equivoca en cruces**, y que su intervalo acierta 26 de
   35 veces (§2.4) — con el intervalo binomial y su advertencia de dependencia.
3. Que **todo lo anterior se emitió antes de ver el dato** y se puede auditar
   commit por commit: la spec se congela en un commit y los resultados llegan en
   otro, y el orden del diff es el sello.

**No puede afirmar, y este informe lo dice antes de que lo pregunten:**

- **No le gana a un modelo de lenguaje en el nivel nacional.** El duelo de tres
  (`CALC-TRIADA-0002`, 12 celdas nacionales) da MAE del motor **4.987 pp** contra
  **3.957 pp** del modelo solo y **3.889 pp** del modelo con corpus; veredicto
  sellado `SIN-GANADOR-UNICO`. Además ese duelo es **RETROSPECTIVO para sus tres
  contendientes** — ninguno emitió antes de que existiera la R.
- **No predice el nivel nacional.** Lo que mide son celdas de cruce dentro de una
  ola, y el punto nacional de una ola no se adjudica con eso.
- **No conoce su error fuera de cruces.** Decisión de mesa, 21/sep, verbatim:
  *«"Error conocido" no se promete fuera de cruces»*. Las 53 celdas marginales
  validadas tienen error de persistencia medido, pero contra un piso t−1 y con
  brechas de 1, 2 y 3 años que **no se promedian entre sí**; y las 39 emisiones
  del motor **no tienen IC en absoluto**.
- **No compone por segmento.** La matriz **compone** y **compite como candidato**
  (ADR-91/ADR-531); no es el estimador por defecto de ninguna celda que no lo
  haya adjudicado bajo el contrato celda-D.
- **No explica por qué los segmentos difieren.** Todo lo de arriba es
  **asociación medida**, no identificación. El programa sabe que la evasión de
  norma es más alta en lo urbano que en lo rural; **no** sabe por qué, y su
  propio registro guarda la corazonada de dirección que apuntaba al revés,
  marcada EQUIVOCADA.

---

## 5 · Lo que viene

- **Lote ENIF 2024** — 14 cruces reservados de `ahorra_solo_informal`, una sola
  spec, contendientes cerrados antes de abrir, comparación primaria C2 contra la
  familia encogida con regla de ¾ e IC que despeje 0.5 pp. Firmado
  (`FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01/-02`), no lanzado.
- **Duelo prospectivo ENVIPE 2026** — la ola queda RESERVADA entera; entra la
  misma familia del lote sobre los dos pares cuyo cruce de 2025 ya está abierto.
  Fecha límite del COMMIT-2: **31/oct/2026** (`…-8a1f-07`).
- **Regla de salida de θ** (`…-8a1f-06`, verbatim): si **ni** en el piloto 3,
  **ni** en la familia R2 del lote ENIF 2024, **ni** en los cruces de ENVIPE 2026
  un retador con interacción vence al piso, se retiran `g()` y `Theta.valor`.
  **El piloto 3 ya entregó su fila: ningún retador con interacción venció al
  piso.** Falta una de tres pruebas negativa para que θ salga; faltan dos por
  correr y ninguna de las dos está lanzada.

---

## 6 · Módulo de auditoría de rigor extremo

*Obligatorio en todo artefacto que afirme algo sobre México (§5 de las
instrucciones). Contestado, no rellenado.*

**¿Se confunde pobreza, violencia o informalidad con cultura?** En este
documento, no: no hay ninguna afirmación causal sobre conducta. Pero el riesgo
está **dentro del objeto medido**, y hay que decirlo: `tramite.evasion_norma`
mide que se evade más en lo urbano (0.5927) que en lo rural (0.4033), y el propio
motor guarda la advertencia de no fundir dos evasiones distintas —la de
**subsistencia**, donde cumplir es inviable con el ingreso disponible, y la de
**cinismo de clase alta**, donde la sanción no aplica a uno—. Tratarlas como una
sola produce la lectura esencialista que el modelo existe para evitar.

**¿Se sobregeneraliza desde la clase media urbana formal?** Sí, estructuralmente,
y el aparato no lo arregla: **ENCIG** —de donde salen las 15 celdas del piloto 3—
tiene como universo la población de 18+ **en ciudades de 100 mil habitantes o
más**. El piloto 3 no dice nada sobre México rural. Su unidad, además, es el
**trámite**: quien pagó la luz doce veces pesa doce veces, y quien no tiene
servicio formal no aparece.

**¿Hay sesgo de marcos o de muestras estadounidenses/europeas?** En este informe,
no: las tres clases de procedencia (datos primarios en México / diáspora / marcos
importados) sólo aparecen en la (a). Los tres pilotos son microdato INEGI.

**¿Qué cambiaría con foco rural, indígena o popular?** El piloto 3 desaparecería
(universo urbano). El piloto 1 (ENIF) y el 2 (ENVIPE) conservan cobertura rural y
el piloto 1 **segmenta por tamaño de localidad** — es su eje. El sistema
indígena-comunal vivo está **fuera por diseño** y ninguna cifra de aquí habla de
él.

**¿Qué parece psicológico y es incentivo racional?** Casi todo lo del §4: lo que
el motor predice son **proporciones de conducta declarada**, no rasgos. Que la
adopción de canal digital suba con escolaridad es, antes que nada, acceso.

**¿Dónde hay evidencia débil e intuición fuerte?** En la lectura de que «la
encogida funciona». La intuición es fuerte (ΔMAE 1.465 pp con IC que no toca
cero, cobertura 14/15) y la evidencia es **una celda-D, un dominio, una ola, 15
celdas, 3 victorias y 12 indecidibles**. Por eso el veredicto sellado es
`FALSADOR-DEBIL` y no «vence», y por eso §3 lo declara sin adjudicar.

**¿Qué sería peligroso leído en simple?** Tres frases: (1) «el modelo predice
conducta en México con 1.5 pp de error» — es el piso, en cruces, dentro de una
ola, en un dominio; (2) «74% de cobertura» leído como garantía — los intervalos
de §2 son **demasiado angostos** por dependencia entre celdas; (3) «88 celdas
validadas» leído como 88 aciertos — validada quiere decir **predicha antes y
comparada después**, y 59 de las filas rotuladas del marcador son
**RETROSPECTIVAS**.

**[v2.1] ¿Qué afirmación sobre el estado del corpus fue escrita a mano y no
derivada?** Ninguna cifra. Las de §2 salen de `tools/informe_pilotos.py`, las de
§1 y §1.1 de `tools/marcador_segmento.py` y `tools/tablero_programa.py`. Las
**citas de firma** de §5 se transcriben verbatim de `forense/firmas-pendientes.tsv`
y son texto, no cifra. Lo único escrito a mano es la **interpretación**, que es
el trabajo de este documento y va marcada como tal.

**[v2.2] ¿Qué deuda «asumida a propósito» caducó al cambiar la función del
programa?** La lista de dos celdas-D escrita a mano dentro de `tablero_programa.py`:
era aceptable cuando había dos pilotos y la métrica rectora no existía; dejó de
serlo el día que la métrica se declaró rectora (firma 20/sep) y el programa
adquirió un tercer dominio. Caducó, y este acto la pagó.

**[v2.3] ¿Cuántos contadores movió este trabajo?** **Uno**: `celdas_validadas`,
73 → 88. Ninguna corrida sellada, ninguna adopción, ningún veredicto tocado.

**[v2.4] ¿En qué escala está cada cantidad y contra qué se compara?** Declarado
al pie de cada tabla. Resumen: §1 y §1.1 son **conteos de celdas**; §2.1 está en
**pp, unidad persona**; §2.2 en **pp, unidad delito**; §2.3 en **pp, unidad
trámite**; §2.4 es una **proporción binomial de conteos**, comparable entre los
tres porque cuenta la misma pregunta. **Los MAE de §2.1, §2.2 y §2.3 no se
promedian entre sí ni con los de persistencia, y en este documento no se
promedian en ningún sitio.**

---

## 7 · Lo que este informe deja abierto

- **Las 15 celdas del piloto 3 cuentan en la métrica pero no tienen fila en el
  marcador.** El derivador sólo publica cruces con `champion_actual: C2` y el
  piloto 3 cerró en `NINGUNO`. Es `DECISIÓN-DE-MESA-PENDIENTE` heredada de
  `PR #961` (`NC-260921-…-3619-01`), no un hueco de conteo: la métrica las cuenta
  porque se emitieron antes y se compararon después, que es la definición.
- **La cobertura de persistencia no está en este informe.** Por la firma MOTOR-M2, el
  error fuera de cruces no se promete; las 53 celdas marginales validadas tienen
  error medido pero su cobertura por candidato no se deriva aquí.
- **El intervalo binomial correcto sigue pendiente.** Wilson es lo que hay sin
  `scipy`; el exacto de Clopper-Pearson y, sobre todo, un intervalo que **no**
  suponga independencia entre celdas de la misma ola, son trabajo de otro acto.
