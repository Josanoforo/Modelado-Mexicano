# CAL-CONF Fase B — posición 4 de la cola: intento de medir `exposicion_violencia` (G4, C1), ENVIPE 2025

*4 de agosto de 2026. Enmendada in situ el mismo 4/ago/2026 (mismo día,
misma rama sin fusionar — I-12): el título original decía simplemente
"mide `exposicion_violencia`". No la mide — ver §4.0. Los números de §3 no
cambiaron; el rótulo sí.*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada para esta sesión.** Esta sesión
abre microdato de **ENVIPE 2025** — tabla `TMod_Vic`, no abierta por ninguna
sesión anterior de Fase B (la ola 1 abrió ENCIG/ENCUCI/ENIF; la ola 2 abrió
`TPer_Vic1` de ENVIPE 2025 y `SEC_4_5` de ENCUCI). `TMod_Vic` es una tabla
distinta con su propia unidad de análisis (ver §0.2) — queda contaminada
para pre-registrar contra ella cualquier acto posterior que no se haya
escrito ya en otra sesión.

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta
sesión (diccionario de datos, cuestionario, microdato, manifiesto,
`forense/hitoE-campana-medicion-v2_0.md`, las dos notas de Fase B
anteriores, `forense/notas/2026-08-01-p2-momentos-atributos.md`,
`canon/modelo-decision-v4_0.md`, `milpa/procedencia.yaml`) — todo contra
`origin/main` en `53fb810`, verificado con `git fetch`/`pull --ff-only`
antes de congelar la especificación de §1. La premisa del encargo sobre
"posición 4 de una cola en `hitoE` §14.3, línea ~1073" es tipo (3) hasta
contrastarla — ver §0.1: **se sostiene, exacta**, después de que esta
misma sesión corrigiera un primer intento de verificación hecho contra un
checkout desactualizado.

---

## 0 · Verificación de premisas antes de obedecer

### 0.1 · La cita de la cola — falsa alarma propia, corregida en la misma sesión

El encargo afirma: *"La cola vive en `forense/hitoE-campana-medicion-v2_0.md`
§14.3 (línea ~1073) ... posición 4 ... exposicion_violencia ... contador →
7/14."*

**Primer intento de verificación, con checkout desactualizado — resultado
falso, declarado y corregido, no borrado.** Esta sesión empezó sobre la
rama `sesion/cal-conf-faseb-ola2`, cuyo padre es `f6bcaaa` (un commit
detrás de `origin/main` en ese momento). Ahí, `forense/hitoE-campana-medicion-v2_0.md`
tenía 919 líneas y ningún `§14` — el primer intento de verificar la cita
concluyó, incorrectamente, que la cola citada no existía. Antes de escribir
esa conclusión en esta nota, esta sesión hizo `git fetch`/`git pull
--ff-only origin main` (higiene estándar antes de congelar una rama nueva
de trabajo, §1) y encontró que `origin/main` traía 4 commits más,
incluida la fusión de PR #56 (`53fb810`) y, dentro de ese rango, el commit
`a851fa3` ("adenda hitoE §14 — la cola priorizada de §11 queda REEMPLAZADA
por una cola rederivada"), fusionado directamente a `main` por una sesión
paralela mientras la ola 2 corría en su propia rama — nunca incorporado a
`sesion/cal-conf-faseb-ola2`. **Contra `origin/main` en `53fb810` (estado
usado para todo lo demás de esta nota), la cita se sostiene exacta:**

```
$ wc -l forense/hitoE-campana-medicion-v2_0.md
1199 forense/hitoE-campana-medicion-v2_0.md
$ grep -n "exposicion_violencia.*ENVIPE.*BP1_20" forense/hitoE-campana-medicion-v2_0.md
1073:| **4** | `exposicion_violencia` | **ENVIPE**, `BP1_20`/`BP1_23`/`BP1_28` (P2 §2.c, inventario l.353) | Contador → 7/14. Es además la C1 del coeficiente `G4 · exposicion_violencia`, **IDENTIFICADO·TRUNCADO** (P2 §2.d) | mismos ids que 1–2 — **registrados**. ⚠️ ENVIPE **no** está abierta: `§13.5` la nombra como la que la ola 1 *no* abrió | Ubuntu microdato |
```

Línea 1073, exacta. Posición 4 de una tabla de 12 filas en `§14.3 · "La
cola — doce posiciones"`. Cita, contador de destino (`7/14`) y la marca
`C1 del coeficiente G4` — las tres, correctas.

**Advertencia declarada dentro de la propia cita, y por qué ya no aplica —
verificado, no supuesto (exactamente lo que el encargo pidió comprobar):**
la fila cita `§13.5`, que a su vez dice que la ola 1 no abrió ENVIPE
("uno que esa ola no abrió (ENVIPE 2025)"). `§14.0` de la misma adenda —
escrita, por su propia tabla de premisas, **antes de que la ola 2
existiera** ("La ola 2 no existe: `§13.5` la titula literalmente 'insumo
para la segunda ola, declarado y no ejecutado'" — premisa que ahí mismo se
marca ❌ NO SE SOSTIENE) — hereda la misma advertencia sin descuento:
*"`exposicion_violencia` no cobra descuento de instrumento-ya-abierto en
el orden de abajo."* Esa advertencia quedó rancia exactamente como dijo el
encargo: `forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md` §1
declara que esa sesión **sí** abrió ENVIPE 2025 (`TPer_Vic1`, `AP5_4_*`).
Lo que esta sesión abre nuevo no es ENVIPE 2025 en general — es la tabla
**`TMod_Vic`** de esa misma encuesta, que ni la ola 1 ni la ola 2 habían
leído (§0.2).

**Un matiz que el encargo no mencionó y que esta sesión declara por su
cuenta:** la cabecera de `§14` es explícita — *"CLASE: Propuesta. No es
decisión. No rige sin ADR"* — y la propia adenda se declara heredera de esa
clase completa: *"es una propuesta de orden de trabajo, no un acto de
canon, y no rige sin ADR"*. Esta sesión no trata la cola como mandato
canónico por citarse con línea exacta — la ejecuta porque, además de estar
bien citada, el objetivo es correcto por una ruta independiente (abajo).

**Verificación independiente de que el objetivo es correcto, sin depender
de que la cola sea vinculante:** `exposicion_violencia` es el **único** de
los 8 parámetros escalares restantes con reactivo confirmado.
`forense/hitoE-campana-medicion-v2_0.md:431` y `:667` («sigue 1 de 15 —
`exposicion_violencia` (G4)») ya lo establecían antes de la adenda del 3 de
agosto; `forense/notas/2026-08-01-p2-momentos-atributos.md` §2.c/§2.d
(«P2») confirma con lectura directa del inventario que de los 8 escalares,
6 fallan C1 (ausencia determinable o no determinable en este régimen:
`familismo_obligacion`, `deferencia`, `sens_estatus` ×2, `aversion_riesgo`
×2) y `exposicion_violencia` es el único **IDENTIFICADO · TRUNCADO** con
reactivo directo reportado (`BP1_20`/`BP1_23`/`BP1_28`, ENVIPE, inventario
l.353 — P2:229). Verificado también contra `canon/modelo-decision-v4_0.md:269`,
que cita el mismo trío de reactivos, y contra `milpa/procedencia.yaml:419`
(línea vigente tras la propagación de PR #56), donde `exposicion_violencia`
sigue con `magnitud: asignada` (`0.70`), sin medir.

**Veredicto final: la cita de la cola SÍ se sostiene, contra el estado
correcto del repo (`origin/main` `53fb810`).** El primer intento de
verificación, contra un checkout desactualizado, produjo un falso hallazgo
de "cita inexistente" — se documenta aquí en vez de borrarse, porque el
propio error es información: recordatorio de que "verificar contra
archivo" exige primero verificar que el archivo está al día (`git
fetch`/`pull` antes de congelar la especificación, no después de escribir
una conclusión sobre lo que el archivo dice o no dice).

Nota menor, mismo espíritu: el encargo llama "regla v2.3" a la práctica de
validar el estimador contra un caso conocido. `instrucciones-proyecto-v2.md`
en esta sesión está en **v2.2** — no existe una "regla v2.3" con ese
número en el archivo canónico. La práctica misma sí existe y es correcta
(la aplicaron ola 1 y ola 2, sin nombrarla "v2.3" — ver §2 de ambas notas);
esta sesión la sigue por ser la práctica establecida, no por el número de
regla citado.

### 0.2 · Universo efectivo de `BP1_20`/`BP1_23`/`BP1_28` — verificado contra FD y cuestionario, no supuesto

**Hallazgo estructural, verificado línea por línea contra
`fd_envipe2025.pdf`:** `BP1_20`, `BP1_23` y `BP1_28` **no viven en
`TPer_Vic1`** (la tabla que usó la ola 2 para `AP5_4_*`) sino en **`TMod_Vic`**
("Tabla del módulo sobre victimización" — `fd_envipe2025.pdf` p.1-2,
`1.2.1`). Verificado contra el índice de tablas del propio FD (`Tabla
TMod_Vic`, línea 4417 del texto extraído) y contra el diccionario de datos
(`diccionario_de_datos_tmod_vic_envipe2025.csv`) — `BP1_20`/`BP1_23`/`BP1_28`
aparecen en la lista de columnas de `conjunto_de_datos_tmod_vic_envipe2025.csv`,
no en la de `TPer_Vic1`.

**Esto cambia el universo de forma más fuerte que el hallazgo de la ola 2,
no de la misma forma.** La ola 2 encontró que una batería (`AP5_4_XX`)
dentro de una tabla de población general (`TPer_Vic1`, un renglón por
persona elegida de 18+) estaba condicionada a una pregunta de
identificación previa (`AP5_3_XX`). Aquí el condicionamiento es más
estructural: **la tabla entera `TMod_Vic` ya es, por diseño, la lista de
delitos que un hogar o persona reportó haber sufrido en 2024** — verificado
contra la propia descripción del FD (p.1: *"esta tabla incluye información
sobre los delitos de los que fue víctima la persona elegida y su hogar
durante el año de referencia, es decir, durante 2024"*) y contra la unidad
de análisis real de la tabla: **40 280 renglones, uno por (identificador de
delito `ID_DEL`, tipo de delito `BPCOD`)**, no uno por persona de 18+. Frente
a los **91 182** renglones de `TPer_Vic1` (población elegida completa,
misma encuesta, mismo año — cifra de la ola 2), `TMod_Vic` es **el 44.2%**
de ese tamaño: no es la población general, es la subpoblación de
delitos-tipo efectivamente reportados. `RESUL_H` de las 40 280 filas es
`A` ("Entrevista completa con victimización") en el 100% de los casos —
verificado, no supuesto: confirma que la tabla no mezcla renglones de
no-víctimas.

**Respuesta directa a la instrucción del encargo — ¿aplica el hallazgo de
contaminación de la ola 2 a `BP1_*`? Verificado, no "no pude verificarlo":
aplica, pero con un mecanismo distinto, ya declarado arriba, y con una
segunda capa dentro de la propia tabla:**

- **`BP1_20`** ("¿Acudió... a denunciar el delito?", Sí/No) se pregunta a
  las 40 280 filas sin excepción — verificado (`Counter` sobre la columna:
  solo `{1, 2}`, cero blancos, cero `9`). Su universo es la tabla completa
  de delitos-tipo reportados, no la población general — la restricción
  estructural de §0.2, no una restricción adicional de esta pregunta.
- **`BP1_23`** ("¿Cuál fue la razón... por la que NO denunció?") está
  condicionada a `BP1_20=2`, verificado por el propio texto de la pregunta
  (no hace falta cruce para inferirlo, a diferencia de `AP5_4`/`AP5_3` de
  la ola 2, que si lo exigía). **A diferencia del cruce perfecto que
  encontró la ola 2 para `AP5_4`/`AP5_3` (cero excepciones), aquí el cruce
  NO es perfecto:** de las 36 170 filas con `BP1_20=2`, 36 040 (99.6%)
  tienen código válido de `BP1_23`, pero **98 no tienen ningún código en
  `BP1_23` ni en `BP1_28`** y **32 tienen código válido de `BP1_28`** (la
  pregunta que corresponde a "Sí denunció") **en vez de `BP1_23`** — 130
  filas (0.36% de los "No") que rompen el patrón de salto esperado. No se
  imputan ni se reclasifican: se excluyen del universo de `BP1_23` como
  "inconsistencia de filtro", declarado con su propio `n`, mismo
  tratamiento que la ola 1/2 dieron a la no-aplicabilidad estructural.
- **`BP1_28`** ("¿Cuál fue la razón... por la que denunció?") está
  condicionada a `BP1_20=1`: de las 4 110 filas con `BP1_20=1`, las 4 110
  tienen código válido de `BP1_28` y 0 tienen código en `BP1_23` — cruce
  perfecto de este lado, verificado.

**Ejes de `x` disponibles en `TMod_Vic`, verificados contra las 137
columnas del diccionario de datos (no supuestos):** `EDAD`, `SEXO`,
`DOMINIO`, `AREAM_OCU`, `ESTRATO`. **Formalidad: NO DISPONIBLE** — no hay
variable ocupacional en `TMod_Vic` (mismo límite que `TPer_Vic1` en la ola
2). **Migración: NO DISPONIBLE** — no hay variable de residencia anterior
(mismo hallazgo que ola 1/ola 2 para ENCIG/ENCUCI/ENVIPE). **Ingreso: NO
DISPONIBLE como eje declarado** — `ESTRATO` existe en la tabla, pero
`canon/modelo-decision-v4_0.md:269` y P2 (`§2.d`, fila `G4
exposicion_violencia`) ya declaran esa misma ausencia como parte del
truncamiento C4 del coeficiente ("el ingreso solo entra como `ESTRATO` de
área, no declarado") — esta sesión no lo declara tampoco, mismo principio
de "no fabricar un eje que nadie validó" que ola 1 aplicó a `ENIGH` en su
§0.

**Conector, añadido 04/ago/2026 (§0.2 en sí no se toca):** el mismo hecho
de arriba —`TMod_Vic` es la subpoblación de víctimas, no la población
general— es la razón por la que §4/§5 corrigen el rótulo de lo medido en
esta nota: una condicional estimada sobre esa subpoblación no puede hablar
de cuánta violencia hay en `x`, solo de la conducta posterior a sufrirla.
Ver §4.0.

---

## 1 · Especificación de la medición — congelada antes de calcular

*Misma regla que ola 1/ola 2: nada de lo que sigue se toca después de ver
una tabla de resultados (`canon` §1.1.B, propiedad 3).*

### 1.0 Qué mide esta sesión y por qué, declarado antes de correr nada

P2 (`§2.d`, fila `G4 exposicion_violencia`) descompone el coeficiente en
`C1` (reactivo que mide `θ_k`) `= BP1_20`, `C2` (desenlace de otra regla
que ENVIPE también observa) `= BP1_23` vía `comunicacion.inseguridad.ver_oir_callar`,
`C3` (no-circularidad) y `C4` (truncamiento). El encargo pide medir **el
parámetro** `exposicion_violencia`, cuyo reactivo directo reportado en el
inventario (P2:229) es el trío `BP1_20`/`BP1_23`/`BP1_28` — no solo el
`C1` aislado de la maquinaria de identificación de `β_gk`. Esta sesión mide
los tres, cada uno por separado, sin construir índice: mismo principio que
ola 2 aplicó a las cuatro instituciones de `seguridad-FFAA` (`§1.0` de esa
nota) — son preguntas distintas (denunció sí/no; razón de no denunciar;
razón de sí denunciar), no repeticiones de un mismo escenario.

- **`BP1_20`** (denunció) se mide como distribución condicional — conjunto
  primario edad (tramos de §1.1), marginal `DOMINIO`.
- **`BP1_23`** y **`BP1_28`** se miden como distribución de categorías
  (proporción ponderada de cada razón, dentro de su universo condicionado)
  — **no cruzadas con edad ni dominio en este acto**: son variables
  nominales de 7-10 categorías: cruzarlas fragmentaría celdas, y es
  además una elección de alcance de esta sesión (mismo principio que ola 1
  §1.4 — "el cuello de botella es el tiempo de la sesión", no una
  imposibilidad).

### 1.1 Declaraciones comunes

- **Tramos de edad:** idénticos a ola 1/ola 2 — 18–29 · 30–44 · 45–59 ·
  60+. `EDAD=97` → "97 años o más" entra a 60+; `EDAD=98` → "no
  especificada" excluida del eje (mismo código de tope que `TPer_Vic1` en
  la ola 2, verificado también aquí contra el catálogo `edad.csv` de
  `TMod_Vic`, no heredado sin verificar).
- **n mínimo por celda: 30 casos sin ponderar.** Por debajo: **SIN
  SOPORTE**, con su `n`.
- **No-respuesta:** para `BP1_20`, no existe en los datos (verificado,
  §0.2). Para `BP1_23`/`BP1_28`: el código `99`/`9` ("No sabe/no
  responde") se reporta como categoría propia, no se excluye — es
  respuesta válida a la pregunta, a diferencia del blanco estructural
  (no-aplicabilidad) o de la inconsistencia de filtro (130 filas, §0.2),
  que sí se excluyen del universo correspondiente.
- **Dispersión:** estimador de conglomerado último (`UPM_DIS` anidada en
  `EST_DIS`), reutilizando `tests/svystat.py` (commiteado en la ola 2) sin
  modificarlo — validado en §2.
- **No se invierte forma funcional; no se extrapola a la cola alta A/B:**
  mismas prohibiciones permanentes de `canon` §1.1.C-i.
- **Ponderador:** `FAC_DEL` — el que corresponde a la unidad de análisis
  real de `TMod_Vic` (delito-tipo, no persona): verificado contra
  `fd_envipe2025.pdf` p.2 ("el cuarto expande cada delito captado en el
  módulo sobre victimización"), no `FAC_ELE` (población 18+), que sería el
  ponderador equivocado para esta tabla — un error análogo al que P1
  declaró como riesgo permanente ("ninguna cifra esperada se teclea de
  memoria", aplicado aquí a "ningún ponderador se copia del acto anterior
  sin verificar que es el que corresponde a esta tabla").
- **Formalidad, ingreso, migración:** NO DISPONIBLES — declarado en §0.2,
  no aproximados con otra fuente.

---

## 2 · El estimador, probado contra dos casos conocidos

**Caso 1 — sintético (reutilizado sin modificar).** `tests/svystat.py`
(commiteado en la ola 2) corrido tal cual en esta sesión:

```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.
```

**Caso 2 — dato real, reproducción exacta de la ola 2 (nuevo en esta
sesión: ni ola 1 ni ola 2 habían corrido esta segunda verificación contra
`TPer_Vic1`; ambas solo reprodujeron ENCUCI/educación entre sí).** Antes de
tocar `TMod_Vic`, esta sesión leyó `conjunto_de_datos_tper_vic1_envipe2025.csv`
(la tabla que sí usó la ola 2) y reprodujo Guardia Nacional (`AP5_4_04`) por
edad con el mismo estimador y el mismo filtro de identificación (`AP5_3_04=1`):

```
n_filas_tabla = 91182
Identifica: 71742 -- no identifica/NS: 19440 -- sin respuesta: 911
18-29: n=16620 p=82.2% se=0.43pp
30-44: n=23905 p=80.2% se=0.37pp
45-59: n=17659 p=79.6% se=0.43pp
60+: n=12352 p=81.8% se=0.51pp
```

Coincide exactamente, número por número, con
`forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md` §3.1 (Guardia
Nacional): mismo `n` de identificación (71 742/19 440/911), mismas cuatro
celdas de edad (`n`, `%` a la décima, `SE` a la centésima de punto
porcentual). Valida no solo el estimador de dispersión (caso 1) sino
también la lectura del CSV, el filtro de identificación y los tramos de
edad — antes de aplicar el mismo pipeline a una tabla (`TMod_Vic`) que
ninguna sesión anterior había leído.

**Ponderador, verificado por orden de magnitud (suma de `FAC_DEL` sobre las
40 280 filas completas de `TMod_Vic`, sin ningún filtro de esta sesión):
35 595 875.** No se declara "coherente" ni "incoherente" contra una cifra
nacional de delitos: esta sesión no derivó ni encontró en el repo, en esta
sesión, una cifra oficial de referencia verificada para "número de delitos
estimados, México 2024" contra la cual contrastarla (regla v2.1 —
"ninguna cifra esperada se teclea de memoria" aplica también a no fabricar
un veredicto de coherencia sin cifra de referencia derivada). Se reporta el
total, sin veredicto.

**Microdato verificado contra manifiesto, no solo en disco:**

```
envipe2025_csv [data_raw]: COINCIDE -- sha256 y tamaño (17600019 bytes) verificados contra data/manifiesto.yaml
```

---

## 3 · Resultados

### 3.1 `BP1_20` — ¿Denunció el delito? (universo: `TMod_Vic` completa, 40 280 filas · 91 excluidas por `EDAD=98`)

**Conjunto primario — edad:**

| Edad | n | % denunció | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 11 871 | 8.6% | 0.52pp | [7.6%, 9.7%] |
| 30–44 | 15 214 | 9.8% | 0.43pp | [8.9%, 10.6%] |
| 45–59 | 8 620 | 9.1% | 0.50pp | [8.1%, 10.0%] |
| 60+ | 4 484 | 7.4% | 0.56pp | [6.4%, 8.5%] |

**Marginal — `DOMINIO`:**

| Dominio | n | % denunció | SE | IC95% |
|---|---|---|---|---|
| Urbano | 28 471 | 9.0% | 0.31pp | [8.4%, 9.6%] |
| Complemento urbano | 8 039 | 9.2% | 0.55pp | [8.1%, 10.2%] |
| Rural | 3 770 | 8.9% | 0.76pp | [7.4%, 10.4%] |

Las siete celdas superan el mínimo de 30; ninguna es SIN SOPORTE.

### 3.2 `BP1_23` — razón de NO denunciar (universo: `BP1_20=2` con código válido, n=36 040; excluidas 130 filas de inconsistencia de filtro, §0.2)

| Código | Razón | n | % | SE |
|---|---|---|---|---|
| 04 | Pérdida de tiempo | 12 469 | 34.8% | 0.59pp |
| 06 | Desconfianza en la autoridad | 4 977 | 13.8% | 0.46pp |
| 03 | Delito de poca importancia | 5 416 | 13.5% | 0.35pp |
| 05 | Trámites largos y difíciles | 3 151 | 10.0% | 0.40pp |
| 07 | No tenía pruebas | 3 749 | 9.6% | 0.30pp |
| 09 | Otra | 2 774 | 7.8% | 0.29pp |
| 01 | Miedo al/a la agresor(a) | 1 901 | 5.8% | 0.32pp |
| 08 | Actitud hostil de la autoridad | 1 164 | 3.3% | 0.21pp |
| 02 | Miedo a que lo/la extorsionaran | 264 | 0.8% | 0.11pp |
| 99 | No sabe/no responde | 175 | 0.5% | 0.06pp |

Las diez celdas superan el mínimo de 30. Suma de proporciones = 100% (categorías mutuamente excluyentes por construcción del reactivo).

### 3.3 `BP1_28` — razón de SÍ denunciar (universo: `BP1_20=1` con código válido, n=4 110)

| Código | Razón | n | % | SE |
|---|---|---|---|---|
| 3 | Para que el/la delincuente reciba castigo | 1 506 | 39.3% | 1.25pp |
| 2 | Para recuperar sus cosas | 1 120 | 23.5% | 1.05pp |
| 5 | Para deslindar responsabilidades | 437 | 12.2% | 0.85pp |
| 4 | Para obtener reparación del daño | 446 | 10.2% | 0.68pp |
| 1 | Por el seguro | 275 | 6.6% | 0.57pp |
| 6 | Otra | 309 | 7.8% | 0.62pp |
| 9 | No sabe/no responde | 17 | SIN SOPORTE | -- |

Seis de siete categorías superan el mínimo de 30; la de "No sabe/no
responde" (n=17) se reporta como **SIN SOPORTE**, no se omite ni se
colapsa con otra.

---

## 4 · Qué queda MEDIDO, con procedencia — y qué no

### 4.0 · Corrección de rótulo, 04/ago/2026 — esto NO mide `exposicion_violencia`

**Declarado antes de la tabla, no después: lo que sigue no es
`exposicion_violencia`.** `BP1_20` es *"¿Acudió... a denunciar el
delito?"* — condicionado, por construcción de `TMod_Vic` (§0.2), a **ya
haber sido víctima**. Lo medido en §3 es `P(denunció | ya fue víctima, x)`,
no `P(víctima | x)`. Tres razones, verificadas contra `canon` y `milpa/`
en esta misma corrección:

1. **El universo lo impide por construcción.** `TMod_Vic` (§0.2) es la
   subpoblación de víctimas (`RESUL_H='A'` en el 100%) — el denominador de
   cualquier condicional estimada ahí ya excluyó a quienes no fueron
   víctimas. La exposición a violencia vive un paso antes, en
   `P(víctima | x)`, no en la conducta posterior a serlo.
2. **No sostiene la cláusula falsable de `G4`.** `canon/modelo-decision-v4_0.md:372`
   define `G4` como *"Exposición a violencia + impunidad → Conducta
   defensiva, retracción del espacio público"*, refutable *"si exposición
   alta no produce conducta defensiva"*. Una tasa de denuncia no construye
   el antecedente de esa cláusula. `milpa/procedencia.yaml:441` escala el
   parámetro `exposicion_violencia` entre 0.35 y 0.70 por perfil — una
   tasa de denuncia no puebla esa escala.
3. **Colisión de contenido dentro del mismo generador.** §3.2 de esta nota
   muestra que las razones de no denunciar, en cabeza, son pérdida de
   tiempo (34.8%), desconfianza en la autoridad (13.8%), trámites (10.0%),
   actitud hostil de la autoridad (3.3%) — contenido de
   `confianza_institucional[justicia]`, que ya entra a `G4` con su propio
   coeficiente (`−0.40`, `milpa/procedencia.yaml:368`). Poblar
   `exposicion_violencia` con esto metería el mismo contenido dos veces en
   la misma ecuación. El chequeo `C3` de P2 (`§2.b`, "no-circularidad")
   pasa formalmente — `BP1_20`/`BP1_23`/`BP1_28` no son literalmente la
   misma variable que `confianza_institucional[justicia]` — pero falla en
   sustancia: son la misma información bajo otro nombre.

**Origen del rótulo defectuoso, para que no se repita.**
`forense/notas/2026-08-01-p2-momentos-atributos.md:229` marca el trío como
*"(victimización, denuncia y sus razones)"* con estado **reportado** —no
verificado— y `:264` lo repite como *"C1 ENVIPE `BP1_20` (victimización)"*.
De ahí bajó a `hitoE §14.3` fila 4 y de la cola al encargo original de esta
sesión, que pedía verificar el descriptor pero venía él mismo sin
verificar. Registrado en `forense/hallazgos.md` (entrada 04/ago/2026, este
mismo acto).

### 4.1 · Lo que sí queda MEDIDO: conducta de denuncia condicionada a victimización, no el parámetro `exposicion_violencia`

**Los números de §3 no se tocan — son correctos y sobreviven íntegros.**
Lo que cambia es el rótulo:

| Qué se midió | Estado | Fuente | Año | Variables | n útil | Método |
|---|---|---|---|---|---|---|
| Conducta de denuncia condicionada a victimización (`BP1_20`) | **MEDIDO**, no es `exposicion_violencia` (§4.0) | ENVIPE | 2025 | `BP1_20` | 40 189 (excl. 91 sin edad) | Proporción ponderada (`FAC_DEL`) + IC95% por conglomerado último (`UPM_DIS`/`EST_DIS`); condicionada a edad, marginal `DOMINIO` |
| Razones de no denunciar, entre víctimas que no denunciaron (`BP1_23`) | **MEDIDO**, distribución de categorías, sin cruzar con x | ENVIPE | 2025 | `BP1_23` | 36 040 | Ídem, sin condicionar por edad/dominio (declarado, §1.0) |
| Razones de sí denunciar, entre víctimas que denunciaron (`BP1_28`) | **MEDIDO**, distribución de categorías, sin cruzar con x | ENVIPE | 2025 | `BP1_28` | 4 110 | Ídem |

**No se sugiere ninguna clase nueva para `exposicion_violencia` en
`milpa/procedencia.yaml`.** `milpa/procedencia.yaml:419` sigue con
`magnitud: asignada` (`0.70`) y así se queda — no hay reactivo verificado
en este acto que lo mueva de ahí. La sugerencia de §4 de la versión
anterior de esta nota (`MEDIDO·PARCIAL(x)` para `exposicion_violencia`) se
**retira** — no se ejecutó nunca contra `milpa/` (la nota nunca tocó ese
archivo), así que no hay reversión que hacer ahí, solo retirar la
recomendación escrita aquí.

### 4.2 · Reubicación del hallazgo — dos candidatos señalados, ninguno adjudicado

**`civico.denuncia.con_seguro` (P2:248, `IDENTIFICADO`).** La regla usa
exactamente `BP2_1` (vehículo asegurado) `×` `BP1_20` (denunció) `×`
`BP1_28`, "celdas ENVIPE edad × urbanización" — el mismo instrumento y dos
de las tres variables que mide esta nota (`BP1_20`, `BP1_28`), condicionado
además por edad y `DOMINIO`, los mismos dos ejes que usa §3.1. **Lo que
falta para que la tabla de §3 sirva directamente a esa regla es `BP2_1`**
(vehículo asegurado) como filtro adicional — variable que esta sesión no
leyó ni tocó. Se declara como candidato: la tabla de §3.1/§3.3 es un
insumo cercano, no la medición de `civico.denuncia.con_seguro` — falta
verificar `BP2_1` (universo, no-respuesta, si vive en `TMod_Vic` o en otra
tabla) antes de poder decir que sirve. Si sirve o no, y si merece su propio
acto de medición, es decisión de mesa — no se adjudica aquí.

**`comunicacion.inseguridad.ver_oir_callar` (P2:264, C2 `Parcial` de `G4`
vía `BP1_23`).** P2 ya marca `BP1_23` como el reactivo `Parcial` de esta
regla, distinta de `exposicion_violencia`. La distribución de categorías
de §3.2 de esta nota (razones de no denunciar, con las cuatro que apuntan
a desconfianza institucional/costo de trámite en cabeza) es, por esa misma
cita de P2, un candidato directo para esa regla — no para
`exposicion_violencia`. Se declara, no se adjudica: verificar si la
regla `comunicacion.inseguridad.ver_oir_callar` pide algo más que la
distribución de §3.2 (universo, corte, condicionantes) es trabajo que esta
nota no hace.

**Qué le falta al coeficiente `G4` para salir de TRUNCADO — vigente, con
una corrección.** P2 (`§2.d`) marca `G4 exposicion_violencia` como
`IDENTIFICADO · TRUNCADO` con `C1` = `BP1_20`. Esa marca de P2 hereda el
mismo rótulo que §4.0 corrige aquí — **de qué reactivo es realmente `C1`
de `G4` queda una pregunta abierta, no resuelta por esta nota**: `BP1_20`
mide denuncia, no exposición, así que si `C1` sigue siendo `BP1_20` la
ficha de P2 tiene el mismo defecto que esta sección corrige. Esta nota no
edita P2 (§0.1 y `hallazgos.md`, entrada nueva) ni resuelve cuál es el `C1`
correcto de `G4` — se limita a señalar que la pregunta está abierta.

---

## 5 · El contador

**condicionales medidas sobre atributos: 6 de 14 — sin cambio.**

Este acto no midió `exposicion_violencia`: midió otra cosa (conducta de
denuncia condicionada a victimización, y sus razones — §4) que también
valía la pena medir, pero que no es ninguna de las 14 condicionales
declaradas en `canon` §1.1.F. El contador sigue en los seis componentes de
`confianza_institucional` que propagó `PR #56` (ola 1 + ola 2) —
`milpa/procedencia.yaml:419` sigue con `exposicion_violencia:
magnitud asignada`, sin medir. La posición 4 de `hitoE §14.3` sigue viva
(`exposicion_violencia` sigue sin medir) pero su fuente/variable queda por
determinar — ver `forense/hitoE-campana-medicion-v2_0.md` §15 (adenda que
corrige la fila 4 de §14.3) y `forense/hallazgos.md`.

**Este acto no propaga ningún contador a `milpa/procedencia.yaml` ni a
ningún otro artefacto de canon** — no hay nada que propagar: el número no
se movió.

---

## 6 · Límite de lectura declarado

Esta sesión leyó completos: `forense/hitoE-campana-medicion-v2_0.md`,
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md`,
`forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md`,
`instrucciones-proyecto-v2.md` (Bloque A), las secciones citadas de
`forense/notas/2026-08-01-p2-momentos-atributos.md` (§2.a-§2.d),
`fd_envipe2025.pdf` (índice de tablas completo, sección `TMod_Vic`
completa — preguntas 1.1 a 1.29 —, y las secciones de `TPer_Vic1` ya
citadas por la ola 2 para la reproducción de §2), `cuest_principal_envipe2025.pdf`
no se abrió en este acto (el FD trae la pregunta literal y las categorías
de respuesta completas — verificado suficiente, mismo criterio que usó ola
2 para las bases de cada reactivo). Se corrió `tests/manifiesto.py
--verifica` sobre `envipe2025_csv`. No se editó `milpa/procedencia.yaml`,
`canon/modelo-decision-v4_0.md` ni ningún otro artefacto de canon — todos
se leyeron, ninguno se tocó.

**Adenda de esta sesión, 04/ago/2026 (corrección de rótulo).** Leído
además: `canon/modelo-decision-v4_0.md:365-380` (tabla de generadores y
cláusulas falsables, `G4`) y `:2.2` (coeficientes); `milpa/procedencia.yaml:365-448`
(asignación de coeficientes de `G4` y `riesgos_cruzados`); re-verificado
`forense/notas/2026-08-01-p2-momentos-atributos.md:229,248,264` línea por
línea (no de memoria); `forense/hitoE-campana-medicion-v2_0.md` §14.4-§14.7
(mecanismo de enmienda de la cola); `forense/hallazgos.md` completo (formato
de entrada); `python3 tests/check.py --baseline` corrido en esta sesión.
Sigue sin tocarse `milpa/procedencia.yaml` y sigue sin tocarse P2 — la
corrección de rótulo de P2 se registra en `forense/hallazgos.md`, no se
edita la nota misma (fuera de perímetro de este acto, decisión de mesa si
amerita acto aparte).
