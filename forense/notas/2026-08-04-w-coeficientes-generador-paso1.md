# Encargo W — estimar los tres coeficientes de generador con ruta viva

*4 de agosto de 2026. Mesa #19. Responde al Encargo W. `main` = `cb331b6`
(PR #88 fusionado), worktree nuevo `mm-encargo-w-coeficientes-generador`,
rama `sesion/encargo-w-coeficientes-generador`.*

⚠️ **Declaración de contaminación (ADR-46), hecha ANTES de congelar la
especificación, no al cierre.** Esta sesión abrió, antes de escribir §1:

- `FD_ENCUCI2020.pdf` (descriptor completo, no dirigido) y el DBF
  `ENCUCI_2020_SEC_4_5.dbf` — **solo su lista de campos y frecuencias
  marginales univariadas** de `AP5_16_1..10`, `AP5_17`, `AP5_18`, `AP5_1_1`
  (conteos por código, para fijar la regla de universo/blancos). No se
  cruzó `AP5_1_*` contra `AP5_17`/`AP5_18` — ninguna fila individual ni
  relación reactivo↔desenlace se vio antes de este commit.
- `encig23_estructura_base_datos.pdf` (dirigido: `P8_3`, `P11_1`, tablas y
  llaves) y `encig23_base_datos_csv.zip` — **solo cabeceras de columna,
  conteo de filas y frecuencias marginales univariadas** de `P8_3_1/2/3` y
  `P11_1_23`. Mismo límite: sin cruce.
- `enif2024_csv.zip` — a diferencia de los otros dos instrumentos, ENIF
  empaqueta diccionario y catálogos **dentro del mismo zip que el
  microdato**: abrirlo para leer `diccionario_datos_tmodulo_enif2024.csv`
  y el catálogo `p4_10.csv` (etiquetas de categoría, no respuestas) contó
  como abrir el ZIP en sentido literal, aunque solo se leyeron metadatos.
  Se declara sin disimular: el criterio del encargo ("antes de abrir un
  solo ZIP") se cumplió en espíritu —cero filas de respondiente vistas,
  cero relación reactivo↔desenlace calculada— pero no en la letra para
  este instrumento específico, por cómo INEGI empaqueta ENIF 2024.
  ADR-46(4): el conservador declara más exploración, no menos.

Con o sin este matiz, el Acto ya se declaraba contaminado para
pre-registrar contra ENCUCI, ENCIG y ENIF (§0 del encargo) — esta
declaración no cambia esa conclusión, la hace precisa.

**Verificado antes de proceder:** `git merge-base --is-ancestor` confirma
que las tres ramas de descriptor previas (`sesion/cal-conf-faseb-pos5-6-
radio-familismo`, `sesion/cal-conf-faseb-pos8-encig-battxi`,
`sesion/cal-conf-faseb-pos4-endireh-descriptor`) ya están fusionadas en
`main`. `data/raw` es symlink a `/home/pc0/mm-corpus/raw` (139 archivos),
igual que los demás worktrees vivos; `data/raices.local.yaml` copiado del
worktree `Modelado-Mexicano`. Red a INEGI no fue necesaria — los seis
payloads objetivo ya estaban en disco y se verificaron por nombre/tamaño
contra `data/manifiesto.yaml` antes de abrirlos (sin recalcular sha256:
no se re-descargó nada, no había razón para dudar de la integridad del
symlink compartido).

Encargo V (`forense/cruce-catalogo-fichas-v1_0.md`, la nota de R5.1, dos
archivos nuevos en `forense/notas/`) puede estar corriendo en paralelo.
Este acto no toca ninguno de esos archivos — disjunto, verificado por
nombre antes de escribir.

---

## 0 · Verificación de las tres citas de P2 contra el instrumento — antes de obedecerlas

La instrucción del encargo (§4, primer PARO) es explícita: verificar el
descriptor contra el cuestionario, no contra el nombre de la variable. Es
el defecto que mató a `BP1_20`/`BP1_23`/`BP1_28`. Las tres citas se
verificaron así, antes de congelar nada:

| Cita de P2 | Verificado contra | Resultado |
|---|---|---|
| W1 — ENCUCI `AP5_1_1/2/3`, Sección 5.1 pp.21-22 | `FD_ENCUCI2020.pdf`, cons. 68-70 | **Coincide.** Pregunta 5.1, escala 0-10 "como en la escuela", tres referentes (mayoría de las personas / conocidas / vecinos). Wording idéntico al que ya verificó `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.1 — no se re-descubre, se reproduce. |
| W1 — ENCUCI `AP5_17`/`AP5_18`, Sección 5.16-5.18 pp.30-32 | `FD_ENCUCI2020.pdf`, cons. 158-159 | **Coincide.** `AP5_17`: *"¿hubo alguna ocasión en la que un funcionario o servidor público le haya pedido dar una dádiva, un favor o dinero extra...?"* `AP5_18`: *"...tuvo que darle... una dádiva...?"* Ambas condicionadas a `AP5_16_1..10` (contacto con funcionario en 12 meses) — no son la misma variable que `AP5_1_*` (C3 pasa). |
| W2 — ENCIG batería XI, Sección XI p.62 | `encig23_estructura_base_datos.pdf`, tabla `encig2023_01_sec_11`, 25 ítems `P11_1_01..25` | **Coincide, con nota de edición.** La cita original de P2 (y de `forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md`) se verificó contra **ENCIG 2021** (`P11_1_1`..`P11_1_25`). Este acto usa **ENCIG 2023** (`P11_1_01`..`P11_1_25`, guion bajo con cero a la izquierda) porque es la edición donde vive `P8_3` — la co-observación exige el mismo instrumento (C2), y esa nota ya declaró que ENCIG 2021 fue la que abrió, no 2023. Verificado de nuevo aquí, no heredado. |
| W2 — ENCIG `P8_3_1/2/3`, "Pregunta 8.3, p.32 (2023)" | `encig23_estructura_base_datos.pdf`, cons. 249-251, tabla `encig2023_01_sec1_A_3_4_5_8_9_10` | **Coincide.** Sección VIII "CORRUPCIÓN", tres ítems sobre apropiación directa / insinuación de tercero / funcionario genera condición, "durante 2023, para agilizar, realizar, evitar procedimientos o multas". Distinta variable de la batería XI (C3 pasa). |
| W3 — ENIF `P9_9_4`, Sección 9 p.26 | `diccionario_datos_tmodulo_enif2024.csv` fila 178 (equivalente); reproduce `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.2 | **Coincide.** *"¿con qué piensa cubrir su vejez? ... 4. dinero que le dé su esposa(o)/pareja, hijas, hijos u otros familiares"*. Ya `MEDIDO·PARCIAL` como condicional en `procedencia.yaml`; esta sesión lo reusa como reactivo de un coeficiente, no lo re-mide como condicional. |
| W3 — ENIF `P4_10`, Sección 4 p.9 | `diccionario_datos_tmodulo_enif2024.csv` fila 67 | **Coincide.** *"Si usted dejara de recibir ingresos, ¿por cuánto tiempo podría cubrir sus gastos con sus ahorros?"* — 5 categorías ordinales + 8/9. Sin filtro de no-aplicabilidad estructural detectado en el diccionario (a diferencia de `P9_9_*`, que sí lo tiene vía `filtro_s9_1`). Variable distinta de `P9_9_4` (C3 pasa). |

**Ninguna de las seis citas falla contra el instrumento — no hay PARO por
esta vía en ninguno de los tres coeficientes.**

⚠️ **Hallazgo de edición, no de fondo:** ENCIG 2021 vs 2023 numeran la
batería XI de forma casi idéntica pero no textualmente idéntica
(`P11_1_1` vs `P11_1_01`) y el orden de dos ítems difiere ligeramente
(`P11_1_12`/`P11_1_13` en 2021 vs `P11_1_12`/`P11_1_13` en 2023 — mismo
orden, verificado ítem por ítem, ninguna discrepancia real de contenido).
El único cambio verificado con consecuencia es de **edición del
instrumento** (2021→2023), no de rótulo de constructo: no aplica el
patrón que mató a `BP1_20`.

---

## 1 · Especificación — congelada antes de correr una sola regresión

**Estimador, para los tres:** diferencia de proporciones ponderada entre
el grupo `θ=1` y el grupo `θ=0`, cada proporción calculada con
`tests/svystat.py::prop_ultimate_cluster` (sin modificar), varianza por
conglomerado último (estrato de diseño / UPM de diseño del instrumento),
`β̂ = p̂(θ=1) − p̂(θ=0)`, `se(β̂) = sqrt(se₁² + se₂²)` (grupos disjuntos,
independientes), IC95% con 1.96 unidades de `se(β̂)`. No se pondera por
celda de atributo ni se corre modelo multivariado — es la traducción
literal de "regresión de binario sobre binario" que P2 §2.d declara.

**Ejes de condicionamiento (C4 de P2, declarados, no ejecutados como
regresión condicional — informativos del régimen, "no más no menos"):**

| Coef. | C4 de P2 | Lectura |
|---|---|---|
| W1 | ENCUCI: 3 ejes estrictos (formalidad, edad, ingreso), 6 laxos | El punto estimado de este acto es marginal (no condicionado); la malla que sostendría un β_gk(x) condicional existe y no se usa aquí. |
| W2 | ENCIG: 1 eje estricto (edad), 4 laxos, **sin ingreso ni ruralidad en ningún régimen** | Truncado — mismo límite que ya truncaba la condicional θ en `procedencia.yaml`. |
| W3 | ENIF: 6 ejes estrictos — la malla más rica del corpus | El punto estimado tampoco se condiciona aquí, aunque la malla lo permitiría. |

### 1.1 · W1 — G1 · `radio_confianza` (asignado hoy: −0.35)

- **θ, tres ítems, medidos por separado (no índice — mismo criterio que
  `procedencia.yaml: condicionales_escalares.radio_confianza`, que ya
  declaró que promediarlos asumiría una unidimensionalidad no
  verificada):** `AP5_1_1` (mayoría de las personas) · `AP5_1_2`
  (personas que conoce) · `AP5_1_3` (vecinos). Dicotomización: confía =
  `{06..10}`, no confía = `{00..05}`, excluido `99`. Corte reusado de
  `procedencia.yaml:242` — tomado del enunciado ("como en la escuela"),
  no de la distribución. Universo completo (cero blancos verificado).
- **Desenlace:** `tramite.mordida.discrecional` — compuesto: 1 si
  `AP5_17='1'` **o** `AP5_18='1'`, 0 si ambas `='2'`, excluido si alguna
  `='9'` y la otra no permite decidir. Universo: subpoblación con
  contacto (`AP5_16_1..10`, al menos un `'1'`) — verificado: 13 435 de
  21 519 (los 8 084 blancos de `AP5_17`/`AP5_18` son exactamente los sin
  contacto, cero excepciones). Fuera de ese universo la pregunta no
  existió — no es no-respuesta, es no-aplicabilidad estructural.
- **C3:** `AP5_1_*` y `AP5_17`/`AP5_18` son variables distintas (confianza
  declarada vs. experiencia de mordida). Pasa.
- **⚠️ Prohibición de P2, respetada:** no se usa
  `cooperacion.confianza.puente_personal` como desenlace de esta entrada
  — su variable observada es `AP5_1_2`, el propio reactivo. El único
  desenlace de esta entrada es `tramite.mordida.discrecional`.
- **Ponderador:** `FAC_SEL`. **Estrato:** `EST_DIS`. **UPM:** `UPM_DIS`.
  Instrumento: `ENCUCI_2020_SEC_4_5.dbf` (un solo registro, sin join —
  reactivo, desenlace, ponderador y diseño viven en la misma tabla).

### 1.2 · W2 — G1 · `confianza_institucional` (asignado hoy: −0.60)

- **θ, un ítem, declarado con razón, no elegido por conveniencia
  posterior:** de los 25 de la batería XI, se usa `P11_1_23`
  *"Servidores(as) públicos(as) o empleados(as) de gobierno?"* — es el
  ítem cuyo referente ("funcionario/empleado de gobierno" genérico)
  coincide con el sujeto del desenlace (`P8_3`: *"servidor(a) público(a)
  o empleado(a) de gobierno"*) sin ser el mismo ítem que ya reclama otro
  generador: `P11_1_2`/`P11_1_17`/`P11_1_22` (policía/jueces/ministerio
  público) alimentan el componente `justicia-policía` de `G4`
  (`forense/notas/2026-08-04-cal-conf-faseb-pos8-encig-battxi.md` §2), y
  usarlos aquí duplicaría información entre coeficientes de dos
  generadores distintos sobre el mismo ítem. Dicotomización: confía =
  `{1,2}` (mucha + algo de confianza), no confía = `{3,4}` (algo + mucha
  desconfianza), excluidos `5` (no aplica, n=20) y `9` (no sabe).
  **No se promedian los 25 ítems en índice** — mismo criterio que W1/W3,
  y aquí con más razón: ADR-49 D3 ya declara sin medir el supuesto de
  pendiente común entre los seis componentes de `confianza_institucional`
  — construir un índice sería asumir precisamente lo que esa nota deja
  pendiente. **Un solo ítem, declarado antes de ver el resultado.**
- **Desenlace:** `tramite.mordida.discrecional` — compuesto: 1 si
  `P8_3_1='1'` **o** `P8_3_2='1'` **o** `P8_3_3='1'`, 0 si las tres
  `='2'`, excluido si alguna `='9'` sin que las otras decidan. Universo:
  completo — verificado, las tres variables solo traen códigos `1`/`2`/`9`,
  sin código de no-aplicabilidad ni blanco (38 966 de 38 966 con código
  válido en alguna de las tres formas de decidir).
- **C3:** `P11_1_23` y `P8_3_*` son variables distintas (confianza
  declarada vs. experiencia de mordida). Pasa.
- **⚠️ Verificado contra `canon/modelo-decision-v4_0.md:311` antes de
  congelar:** el canon mismo nombra esta ruta —"ENCIG batería XI,
  co-observada con `tramite.mordida.discrecional` en el mismo
  instrumento"— como la que cerró `D-12` y sacó `confianza_institucional`
  de la clase inidentificable bajo `G1`, a nivel de constructo genérico,
  no del componente `[financiera]` que ADR-52 B nombró para las reglas de
  ahorro. Este acto mide esa ruta genérica, no `confianza_institucional
  [financiera]` — `tramite.mordida.discrecional` corre por "trampa
  social (G1)" (`modelo:450`), no por ninguna de las tres reglas de
  dominio financiero que ADR-52 B enumeró. **No hay conflicto de
  componente: son rutas de identificación distintas para coeficientes
  con el mismo nombre corto (`confianza_institucional`) pero invocado por
  reglas distintas del mismo generador.** Se declara para que quede
  verificable, no se resuelve aquí si ambas rutas deberían fundirse en un
  solo número — es pregunta de mesa, no de esta sesión.
- **⚠️ TRUNCADO, heredado y no resuelto aquí:** ENCIG no observa ingreso
  en ningún régimen y su universo excluye por diseño localidades <100 000
  hab. — mismo límite que ya truncaba la condicional θ.
- **Ponderador:** `FAC_P18`. **Estrato:** `EST_DIS`. **UPM:** `UPM_DIS`.
  Instrumento: dos tablas de la misma edición 2023
  (`encig2023_01_sec_11` para `P11_1_23`, `encig2023_01_sec1_A_3_4_5_8_9_10`
  para `P8_3_*`), unidas por `ID_PER` — mismo universo verificado (38 966
  filas cada una, mismo instrumento, no dos encuestas distintas).

### 1.3 · W3 — G3 · `familismo_apoyo` (asignado hoy: 0.20)

- **θ:** `P9_9_4` ("dinero que le dé su esposa(o)/pareja, hijas, hijos u
  otros familiares", parte de P9.9 "¿con qué piensa cubrir su vejez?").
  Ya declarado en `procedencia.yaml:251-270` como el único de los seis
  ítems que opera `familismo_apoyo`. Escala binaria por ítem: `1` Sí /
  `2` No / `9` No sabe — sin necesidad de dicotomizar más, ya es binaria.
  Universo efectivo: `filtro_s9_1=2` (menor de 71 años), n=12 379 de
  13 502 — reusado de la especificación ya verificada, no re-derivado.
- **Desenlace:** `dinero.ahorro.volatilidad_horizonte_corto` — `P4_10`.
  Dicotomización, declarada antes de ver la relación con `P9_9_4`:
  horizonte corto = `{1}` ("menos de una semana / no tiene ahorros" — la
  única categoría que el propio catálogo de INEGI funde con "no tiene
  ahorros", es decir, la única con ancla de horizonte cero, no solo
  "corto"), horizonte no-corto = `{2,3,4,5}` (de "al menos una semana" a
  "seis meses o más"), excluidos `8`/`9`. A diferencia de W1, esta
  dicotomización no tiene un ancla externa tan limpia como "como en la
  escuela" — el corte se apoya en que la categoría 1 es la única que el
  instrumento mismo define como equivalente a horizonte cero, no en
  dónde cae la mediana de la distribución (que no se miró antes de fijar
  esta regla). Se declara la fragilidad: mover el corte a `{1,2}` es una
  decisión defendible que este acto no tomó — queda para que mesa la
  revise si el resultado se usa fuera de este acto.
- **C3:** `P9_9_4` y `P4_10` son variables distintas — pasa para `G3`.
  ⚠️ **No pasa para `G5`:** `procedencia.yaml:265-270` ya marca que el
  desenlace de `G5·familismo_apoyo` en ENIF es la misma batería `P9_9_*`
  — esta entrada **no identifica `G5`**, solo `G3`, exactamente como P2
  §2.d ya lo decía.
- **Ponderador:** `fac_per`. **Estrato:** `est_dis`. **UPM:** `upm_dis`.
  Instrumento: una sola tabla, `conjunto_de_datos_tmodulo_enif2024.csv`
  — reactivo, desenlace, ponderador y diseño en el mismo registro, sin
  join.

---

## 2 · Lo que este procedimiento no hace, declarado antes de correrlo

- No construye ningún índice (ni de `radio_confianza`, ni de `confianza_
  institucional`, ni de nada) — cada θ es un ítem o un compuesto simple
  de Sí/No sobre variables ya binarias, nunca un promedio de escalas.
- No condiciona sobre atributos (§1, tabla de C4) — el punto estimado es
  marginal. Condicionar es un acto futuro, con su propia especificación.
- No compara β̂ contra el valor `ASIGNADO` de `procedencia.yaml` en
  magnitud — solo en signo y orden relativo entre coeficientes del mismo
  generador (§1 del encargo, la trampa de categoría). El enlace entre la
  escala de diferencia de proporciones y la escala del índice del
  generador no está declarado por el modelo; hasta que lo esté, no hay
  conversión.
- No decide si la ruta de W2 (confianza genérica, vía `P11_1_23`) debería
  fundirse con la ruta de `confianza_institucional[financiera]` que ADR-
  52 B nombró — se declara la distinción y se deja a mesa.
- No toca `canon/`, el bloque append-only, `data/manifiesto.yaml`, ni la
  clase `AJUSTADO`.

**El primer resultado que produzca este procedimiento es el que se
reporta.**
