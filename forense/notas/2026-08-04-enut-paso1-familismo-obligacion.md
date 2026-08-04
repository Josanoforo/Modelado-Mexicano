<!-- PROCEDENCIA — leer antes que el cuerpo.

Contadores movidos: 0. Sin módulo de auditoría (v2.3).

Este documento responde al Encargo N (mesa #18, 4/ago/2026). Régimen: ENUT
paso 1 — ¿qué miden las series `6.11`/`6.11a`, y qué contaría medirlas? El
encargo prohíbe explícitamente medir el parámetro o decidir si el resultado
mueve el contador; ambas decisiones quedan para el paso 2 y para mesa,
respectivamente.

Sesión: worktree dedicado, rama de trabajo derivada de `origin/main` en
`821dbbf` (PR #80 fusionado — verificado con `git log origin/main --oneline
--grep="#80"`, sin discrepancia con la base declarada por el encargo).

Por ADR-46: esta sesión abre ENUT (diccionario y microdato) a propósito —
es su objeto — y por tanto queda **inhabilitada para pre-registrar** contra
ENUT. Puede seguir trabajando la fuente.
-->

# ENUT paso 1 — `familismo_obligacion`: qué miden 6.11/6.11a, y qué contaría medirlo

## 0 · Entorno

- `HEAD` == `origin/main` == `821dbbfc9f9474d0309e42c077a010faf7ab01ae` (PR #80 fusionado). Sin discrepancia — no aplica documentar divergencia.
- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE`: `sin_variable`.
- `curl -o /dev/null -w '%{http_code}' https://www.inegi.org.mx/` → `200`.
- `data/raw` nació ausente en este worktree (worktree fresco). Reparado con el wiring estándar de esta línea de sesiones: `data/raw -> /home/pc0/mm-corpus/raw` (symlink, no directorio local — el patrón que el registro `I-15`/nota de ENCUP paso 1 pide para no repetir el defecto de PR #77, seis payloads que se quedaron en un `data/raw` local sin copiar al corpus compartido).
- `tests/manifiesto.py --verifica` para los ocho ids relevantes de ENUT 2019/2024 (bd, fd, diccionario, der) tras el symlink: **COINCIDE** en los seis verificados directamente (`enut2024_bd_csv`, `enut2019_bd_csv`, `enut2024_fd_xlsx`, `enut2019_fd_xlsx`, `enut2024_diccionario_variables_html`, `enut2019_diccionario_variables_html`) — sha256 y tamaño contra `data/manifiesto.yaml`. Detalle en §3.0.
- Suite: `check.py --baseline` → LÍNEA BASE VERDE (nada nuevo frente a `tests/baseline.json`, HEAD congelado `090ee0f`). `validador_registro_ids.py` → OK, 49 IDs verificados.
- Ruta real del worktree: redactada (no se cita aquí ni en el PR), por instrucción del encargo.

## 1 · Premisas

| # | Premisa | Verificación |
|---|---|---|
| PN-1 | Encargo C dictaminó ENUT 6.11/6.11a como PROXY CON SUPUESTO DECLARADO, "carga de cuidado a nivel persona", hueco de cobertura no permanente | Confirmado — `forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` §0, §2.3 |
| PN-2 | ENUT registrada con cinco olas (2002 DBF, 2009 DBF, 2014 DBF, 2019 CSV, 2024 CSV), FD y diccionario de variables por ola | Confirmado — `data/manifiesto.yaml:2646-2936`, 16 entradas (`enut2002_bd_dbf`…`enut2024_diccionario_variables_html`) |
| PN-3 | `familismo_obligacion` en fila "Proxy declarado, pendiente de medición"; reparto cierra en 14 (9+0+2+3) | Confirmado — `canon/modelo-decision-v4_0.md:271-272` |
| PN-4 | H-11: `E[familismo_obligacion \| informal, ingreso bajo] > E[... \| formal, ingreso medio-alto]`, ejes `segsoc`×`est_socio`, `[HIPÓTESIS]`, forma PENDIENTE y sin magnitud | Confirmado — `canon/modelo-decision-v4_0.md:224` |
| PN-5 | ADR-30: check obligatorio — configuración donde `familismo_obligacion` alto mejora todos los desenlaces se rechaza; entra a G5 con signo negativo o no monotónico, SIN MAGNITUD | Confirmado — `milpa/procedencia.yaml:599-600`; ADR-30 vigente en `canon/gobernanza-v1_15.md:226` |

Las cinco premisas (1) se sostienen. Sin discrepancia. No hay PARO en esta sección.

## 2 · La frase-criterio (escrita antes de abrir el diccionario)

**`familismo_obligacion`** = obligación percibida de destinar recursos propios —tiempo, dinero, decisiones— a miembros de la familia, con costo para el proyecto individual; distinta de (a) apoyo familiar recibido o esperado (`familismo_apoyo`, ya medido vía ENIF `P9_9_4`, y ADR-30 exige que no sea doble conteo), (b) conducta de cuidado observada sin componente de obligación, y (c) composición del hogar (tener a quién cuidar no es sentirse obligado).

Escrita antes de tocar `enut2019_diccionario_variables.html` / `enut2024_diccionario_variables.html` / `enut2019_fd.xlsx` / `enut2024_fd.xlsx`. Lo que sigue en §3 en adelante es posterior a esta línea.

## 3 · El acto

### 3.0 · Método

`enut2024_diccionario_variables.html` / `enut2019_diccionario_variables.html` son la página de catálogo del RNM (landing del proyecto, estructura de tablas y conteos por sección) — **no** listan reactivo por reactivo; ese detalle vive en el FD (`enut2024_fd.xlsx` / `enut2019_fd.xlsx`), workbook con una hoja por tabla (`TVIVIENDA`, `THOGAR`, `TSDEM`, `TMODULO`, `TVAR_CREA`). Sin `openpyxl`/`pandas` en este entorno (no instalables, sin `pip`; confirmado — mismo límite que dejó registrado `forense/notas/2026-07-31-inventario-segmentacion.md`): se parseó `xl/worksheets/sheetN.xml` + `xl/sharedStrings.xml` a mano (script ad hoc, scratchpad de la sesión, no en el repo) reconstruyendo fila/columna, no solo texto plano. Columnas del FD: `B` Pregunta (wording literal) · `C` Nemónico (variable) · `D` Tipo · `E` Tamaño · `F` Códigos válidos · `G` Concepto (etiqueta del código). Microdato: `enut2024_bd_csv.zip` → `tmodulo.csv`/`tsdem.csv`/`thogar.csv`; `enut2019_bd_csv.zip` → `enut_2019/TMODULO.csv` (más una carpeta `enut_2019_indigena/` aparte, no tocada — ver §3.9).

### 3.1 · Descriptor — series 6.11/6.11a (2024, principal)

Universo base: tabla `TMODULO`, persona informante elegida de 12 años y más, `n = 74 053` (cifra de la página RNM y confirmada por conteo directo de filas del CSV).

**Filtro de universo — `FILTRO_S6_11`** ("FILTRO 6.11. VERIFIQUE SI HAY INTEGRANTES QUE NECESITARON CUIDADOS ESPECIALES (3.7 = CÓDIGO 1 O 3.8 = CÓDIGO 1 O 2)"), condicionado a `P3_7` (TSDEM, "La semana pasada, [NOMBRE] por la dificultad que tiene para [3.6], ¿necesitó de los cuidados de otra persona?") y `P3_8` (TSDEM, "¿necesitó cuidados por enfermedad crónica o temporal?"). Catálogo: `1` Sí, otra(s) persona(s) [y quizá también el informante] necesitaron cuidados · `2` Sí, solo el/la informante necesitó cuidados · `3` No. **n por código, microdato 2024:** `3`→62 781 (84.79%) · `1`→8 943 (12.08%) · `2`→2 329 (3.15%).

**Ítems `P6_11_01`…`P6_11_14`** (14 tareas, no 11 — corrección frente a `forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` §2.2, que citó "11 tareas" con wording de la ola 2019; ver §3.9). Wording literal (ítem 1, patrón idéntico en los 14): *"6.11 (NOMBRE(S)) necesitó(aron) cuidados de otra persona. Durante la semana pasada, sea en la casa, hospital u otro lugar, ¿usted le(s) dio de comer o ayudó a hacerlo?"* — variable `P6_11_01`, catálogo `1` Sí / `2` No / `b` Blanco por secuencia. Los 14 ítems (dar de comer · bañar/vestir · cargar/acostar · remedios/alimento especial · medicamentos/síntomas · acompañar a la atención de salud · llevar/recoger de la atención de salud · dar terapia/ejercicios · esperar de clases/trabajo · llevar/recoger de clases/trabajo · ayudar en tareas escolares · asistir a juntas/festivales escolares · jugar/leer/escuchar/orientar/consolar · vigilar/estar al pendiente) están todos **condicionados** a `FILTRO_S6_11 = 1`: n de respuesta válida (no blanco) por ítem = **8 943 exacto**, igual al conteo del filtro — cero missing dentro del universo condicionado, todo el resto es blanco por secuencia. Ejemplo de extremos: `P6_11_01` (dar de comer) — Sí 2 142 (23.9% del denominador) · No 6 801. `P6_11_14` (vigilar/estar al pendiente) — Sí 4 133 (46.2% del denominador) · No 4 810.

**Ítems `P6_11A_XX_1..4`** (horas/minutos lunes-viernes y sábado-domingo, por cada uno de los 14 ítems). Wording: *"6.11a ¿Cuánto tiempo le dedicó de lunes a viernes? - Horas/Minutos"* (y su par de fin de semana). Tipo numérico, rango declarado por ítem (p. ej. `P6_11A_01_1` "00-48" horas semana). **Condicionados a `P6_11_XX = 1`** (blanco si la tarea fue "No" o si el ítem base ya era blanco por secuencia): `P6_11A_01_1` no-blanco = 2 142, exacto al n de "Sí" de `P6_11_01`.

**Contraste 6.16** (ya señalado por Encargo C, reverificado con n): `P6_16_1`/`P6_16_3`/`P6_16_4` ("¿usted ayudó de manera gratuita a **otro hogar** [de un familiar]...?") — **no condicionado** a `FILTRO_S6_11`: universo pleno, `n = 74 053`, sin blanco por secuencia (`P6_16_1`: Sí 6 429 · No 67 624). Confirma la distinción intra-hogar (6.11, condicionado, n=8 943) vs. inter-hogar (6.16, universo completo).

### 3.2 · Denominador, cuantificado

El reactivo candidato (`P6_11_01`…`P6_11_14`, y sus `P6_11A_*`) **no existe para la población de informantes** (74 053): existe solo para el **12.08%** (8 943/74 053) cuyo hogar tiene, al menos, un integrante distinto del informante que necesitó cuidados por discapacidad o enfermedad en la semana de referencia (`FILTRO_S6_11 = 1`). El 3.15% adicional (`FILTRO_S6_11 = 2`, 2 329 casos) son informantes que **ellos mismos** necesitaron cuidados — tampoco responden 6.11 (no hay "otra persona" a quien referir la conducta). El 84.79% restante (62 781) no tiene a quién referir la pregunta y queda fuera del universo por diseño del instrumento, no por no-respuesta.

Esto confirma, cuantificado, la advertencia del encargo: **el reactivo solo puede hablar de intensidad de conducta entre quienes ya cuidan** (el 12.08%), no de "obligación" como disposición en la población general de informantes. Cualquier uso del reactivo como condicional base de `familismo_obligacion` hereda esta restricción de universo — no es un parámetro poblacional, es un parámetro condicional sobre "tener a un dependiente intra-hogar", y el denominador de esa condición **no puede separarse** de la de "necesitar cuidado" en sí (que es, además, un rasgo del hogar/persona cuidada, no de quien eventualmente cuida — el filtro está definido sobre el receptor de cuidado, no sobre el cuidador).

### 3.3 · Doble conteo — ADR-30, contra `familismo_apoyo`

`familismo_apoyo` está `MEDIDO·PARCIAL(formalidad,edad,urbanización)` vía **ENIF 2024, `P9_9_4`** ("¿con qué piensa cubrir su vejez?" → "dinero de familiares"), n_útil 8 221 sobre universo `filtro_s9_1=2, <71 años` (`milpa/procedencia.yaml:251-264`). Comparación directa con el candidato de esta sesión:

| | `familismo_apoyo` (asignado) | `familismo_obligacion` (candidato) |
|---|---|---|
| Fuente | ENIF 2024 | ENUT 2019/2024 |
| Ítem | `P9_9_4` | `P6_11_01..14` / `P6_11A_*` |
| Dirección | **Recibir** (dinero esperado de la familia) | **Dar** (horas de cuidado dedicadas a un dependiente) |
| Marco temporal | Expectativa a futuro (vejez, hipotética) | Conducta declarada de **la semana pasada** |
| Objeto | Dinero (transferencia monetaria esperada) | Tiempo (tareas de cuidado, no dinero) |
| Universo | Población `<71` años que planea su vejez | Hogares con dependiente que necesitó cuidado la semana pasada |

No comparten variable, encuesta, muestra, dirección del intercambio ni marco temporal — no hay manera de que la **misma conducta** aparezca contada en ambos (no son ni siquiera las mismas personas encuestadas: ENIF y ENUT son muestras independientes). El riesgo de doble conteo que ADR-30 pide vigilar es del tipo que **sí** aplica al par G3/G5 de `familismo_apoyo` consigo mismo (resuelto en `milpa/procedencia.yaml:597`, "mecanismo distinto, no es doble conteo") — no aplica aquí por falta de solapamiento de conducta. **No se reporta como riesgo abierto.**

### 3.4 · La pregunta central — ¿(1), (2) o (3)?

**Respuesta: (2) — conducta de cuidado, no obligación declarada.**

El glosario define `familismo_obligacion` como **"creencia internalizada de que uno debe sacrificarse por la familia"** (`canon/glosario-v5_6.md:120`, base Zeiders 2013 / Fuligni 1999 / Calzada 2012 — escalas psicométricas de **actitud**). Las series 6.11/6.11a no preguntan una creencia ni una actitud: preguntan, para quien ya tiene un dependiente que necesitó cuidado la semana pasada, si **hizo** cada una de 14 tareas concretas y **cuánto tiempo** le dedicó. Es wording de conducta observada ("¿usted le dio de comer o ayudó a hacerlo?"), no de disposición ("¿cree que debe...?", "¿está de acuerdo con...?"). No hay en la Sección VI de ENUT (ni en ninguna otra sección revisada del FD) un ítem de actitud/creencia sobre el deber de cuidar a la familia — el barrido de la Sección VI completa (`6.1`–`6.23`) es, sin excepción, tiempo dedicado a actividades, no percepción sobre ellas (la única sección actitudinal de ENUT es la VII, "Percepción sobre el uso del tiempo y bienestar subjetivo", y no menciona familia ni cuidado como objeto).

Esto coincide con — y ahora queda verificado contra microdato real, no solo contra diccionario — el veredicto del Encargo C: **PROXY CON SUPUESTO DECLARADO**, no medición directa. El supuesto que hay que declarar para usarlo (sin cambios de fondo respecto al de Encargo C, ahora con los n's que antes faltaban): **una carga de cuidado intra-hogar alta y asimétrica, en el 12.08% de informantes con dependiente, es conducta consistente con obligación internalizada — no la prueba, y no distingue motivo** (obligación / afecto / ausencia de alternativa económica para pagar cuidado de mercado). El instrumento no puede refutar la lectura alternativa ("esta persona cuida porque quiere, no porque se sienta obligada") ni la de "cuida porque no hay otra opción económica" — ninguna de las tres es observable con este reactivo.

**No se determina aquí si esto mueve el contador.** Queda para mesa, con el hecho — y el supuesto exacto — ya escritos.

### 3.5 · Viabilidad de H-11

H-11: `E[familismo_obligacion | informal, ingreso bajo] > E[... | formal, ingreso medio-alto]`, ejes `segsoc` × `est_socio` (`canon/modelo-decision-v4_0.md:224`). **`segsoc` y `est_socio` son variables de ENIGH** (`§1.1.A`, línea 116 y 120: `segsoc` 1 Sí/2 No derechohabiencia, módulo `poblacion`; `est_socio` catálogo de 4 categorías sobre `ing_cor` de hogar, módulo `concentradohogar`) — **no existen literalmente en ENUT**. ENUT trae proxies propios, no verificados como equivalentes:

- **Formalidad:** `P5_6_1..8` (Sección V, "aunque no las use, ¿en su trabajo tiene derecho a...?"), en particular `P5_6_7` ("servicio médico, IMSS/ISSSTE") — derechohabiencia vía prestación laboral, mismo espíritu que `segsoc` pero no la misma variable ni el mismo catálogo. `n` no-blanco = 30 148 (16 678 "Sí" + 13 470 "No"), **condicionado a haber trabajado** (`P5_1=1`, n=41 787 de 74 053).
- **Ingreso:** `P5_10` ("¿cuánto gana o recibe por trabajar?") — ingreso **individual** del trabajo, no `ing_cor` de **hogar** (que es lo que define `est_socio`). `n` no-blanco = 42 863 de 74 053, también condicionado a trabajar.

**Disponibilidad conjunta** (candidato de obligación **∧** proxy de formalidad **∧** proxy de ingreso, misma persona): de los 8 943 informantes con `FILTRO_S6_11=1` (denominador del reactivo de obligación), solo **3 496** (39.1%) tienen también respuesta en `P5_6_7` y `P5_10` — porque ambos exigen haber trabajado la semana de referencia, y una parte sustancial de quienes cuidan (5 447, 60.9%) no trabajó. Esto **no es solo un problema de tamaño de muestra**: la condición de empleo de H-11 excluye estructuralmente a la mayoría de quienes muestran la conducta de cuidado — precisamente la población (cuidadoras sin empleo remunerado) donde la hipótesis de "obligación como sustituto de mercado" sería más relevante de probar. H-11 sería evaluable en ENUT solo sobre ese 39.1%, con proxies declarados de `segsoc`/`est_socio`, no las variables canónicas — **no se adjudica aquí** si eso basta para identificar H-11; se deja el hecho y el n.

### 3.6 · Ejes de atributos en ENUT 2024

De los seis ejes de `§1.1.A` (todos definidos originalmente sobre ENIGH 2022):

| Eje canónico (ENIGH) | ¿Existe en ENUT 2024? | Variable | n |
|---|---|---|---|
| 1 Formalidad (`segsoc`) | Proxy, no la variable | `P5_6_7` (derechohabiencia IMSS/ISSSTE vía trabajo) | 30 148 de 74 053 (condicionado a trabajar) |
| 2 Edad (`edad`) | **Sí**, directa | `EDAD` (derivada, TSDEM) | 94 565 (TSDEM completo) / 74 053 vía llave a TMODULO |
| 3 Urbanización (`tam_loc`) | **Sí**, análoga | `TLOC` (4 categorías) + `MENOR10` | 29 181 hogares (`THOGAR`): 1→13 165 · 2→4 005 · 3→4 899 · 4→7 112 |
| 4 Ingreso (`ing_cor`+`est_socio`) | Proxy parcial, no hogar | `P5_10` (individual, no hogar) | 42 863 de 74 053 (condicionado a trabajar); sin ingreso total de hogar |
| 5 Acceso digital (`celular`/`conex_inte`) | **Sí**, directa | `P2_4_12` (celular/smartphone hogar) + `P2_4_13` (internet hogar) | 29 181 hogares: celular Sí 27 096/No 2 085; internet Sí 20 843/No 8 338 |
| 6 Migración (`residencia`) | **No** | — | Barrido de FD (TVIVIENDA/THOGAR/TSDEM/TMODULO) sin variable de lugar de nacimiento, entidad de residencia previa, ni catálogo `residencia.csv`; solo `P3_20_3`/`P3_20_4` (remesas de familiares/amistades), que es flujo monetario, no migración propia |

Cuatro de seis ejes tienen algún análogo en ENUT (2 limpio, 3 y 5 con catálogo propio pero razonable, 1 y 4 con proxy parcial condicionado a empleo); el eje 6 no tiene análogo. Ninguno de los seis es, literalmente, la variable canónica de `§1.1.A` — mismo patrón de "proxy rugoso" ya declarado para ENVIPE (`forense/hallazgos.md`, 2026-08-04, "formalidad... proxy rugoso vía posición en la ocupación, marginal").

### 3.7 · C2 — ¿ENUT observa un desenlace de G5?

Reglas de `§3.B` con `PORQUE` citando `G5` explícitamente (`grep -n "PORQUE.*G5" canon/modelo-decision-v4_0.md`): exactamente **dos** — `familia.seguro.volatilidad_ausencia_estado` (§3.5) y `salud.adherencia.desabasto_vs_cuidadora` (§3.4).

- `familia.seguro.volatilidad_ausencia_estado` — en Tabla B, ENUT = **"Parcial (débil)"**, vía `P3_20_3`/`P3_20_4` (remesas de familiares **mezcladas con amistades**, "no volatilidad ni ausencia estatal") — no la misma variable que el candidato de esta sesión (`P6_11_*`), así que no hay circularidad directa tipo C3 aquí (a diferencia de `familismo_apoyo`/ENIF, donde el reactivo y el desenlace **sí** son la misma batería — `milpa/procedencia.yaml:265-270`).
- `salud.adherencia.desabasto_vs_cuidadora` — en Tabla B (`forense/notas/2026-07-31-inventario-segmentacion.md:346-347`), solo aparecen filas para ENIGH y ENSANUT; **ENUT no fue evaluado para esta regla** (ausente de la tabla, no "No" explícito).

**Hallazgo que no se resuelve aquí, y que hay que dejar escrito porque es el más cercano a un problema:** Tabla B **sí** registra a ENUT como **"Sí"** para una regla distinta, `familia.cuidado.recae_mujeres_40mas` (§3.5, `forense/notas/2026-07-31-inventario-segmentacion.md:185`), y la variable con la que lo hace es **la misma familia del candidato de esta sesión** — `P6_11_01..14` (+ `P6_12`/`P6_13`, derivadas `CUID_INT_*`). Esa regla, sin embargo, **no** cita `PORQUE G5` en su texto (cita "estructura + guion marianista", `canon/modelo-decision-v4_0.md:468`); la definición de G5 (línea 375: "Familia como seguro ante Estado ausente | Pooling, corresidencia, **carga de cuidado**") sí nombra "carga de cuidado" como uno de sus mecanismos. Si mesa en algún momento retiquetara `familia.cuidado.recae_mujeres_40mas` como desenlace de G5 (no lo es hoy, por el texto vigente), usar `P6_11_*` para identificar `familismo_obligacion` en G5 caería en el mismo tipo de circularidad que ya inhabilitó a `P9_9_*` para `familismo_apoyo`·G5. **Con el etiquetado vigente, C2 no falla** — pero queda a un paso de fallar, y ese paso es una decisión de mesa (retiquetar o no la regla), no un hecho de este acto.

### 3.8 · C3 — ¿ENUT está en Tabla B?

Verificado por grep, no de memoria: `forense/notas/2026-07-31-inventario-segmentacion.md:4` — *"Ocho fuentes en disco: ENIGH, ENIF, ENVIPE, ENOE, ENCUCI, ENCIG, ENSANUT, ENUT"* — **ENUT es una de las ocho fuentes de Tabla B.** Esto es distinto e independiente de que ENUT aparezca en posición 7 de la cola de `hitoE` (aviso del encargo, correcto): la cola de `hitoE` es un orden de trabajo, Tabla B es el inventario de qué fuente observa qué desenlace. Verificado aparte, como pidió el aviso.

### 3.9 · Serie — 2019 vs. 2024

Las variables persisten entre olas con el mismo tema y estructura general, **no con el mismo nombre de filtro ni el mismo número de ítems**. 2019: filtro `FP6_11` (no `FILTRO_S6_11`), condicionado a una sola variable ("PREGUNTA 3.11 = 1"); ítems `P6_11_01`…`P6_11_11` (**11**, no 14), mismo patrón de wording y catálogo (`1` Sí/`2` No), mismos `P6_11A_XX_1..4` de horas/minutos entre semana y fin de semana. 2024: filtro `FILTRO_S6_11`, condicionado a la disyunción de **dos** variables (`P3_7 = 1` o `P3_8 ∈ {1,2}`); ítems `P6_11_01`…`P6_11_14` (**14**) — tres ítems nuevos frente a 2019 (`_12` asistir a juntas/festivales escolares, `_13` jugar/leer/escuchar/orientar/consolar, `_14` vigilar/estar al pendiente — que en 2019 vivían comprimidos en el ítem `_11` "cuidó o estuvo al pendiente"). `n` del universo condicionado: 2019 = 6 082/71 404 (8.52%); 2024 = 8 943/74 053 (12.08%) — proporción más alta en 2024, no analizado aquí (sería pre-registro, fuera de alcance de este acto). 2019 trae además una carpeta paralela `enut_2019_indigena/` (mismo esquema de tablas) no explorada en este acto. Esto es **insumo para un acto de medición o de serie**, no un análisis ni un pre-registro — misma disciplina que dejó `forense/notas/2026-08-04-...` sobre ENVIPE en actos previos.

## 4 · Desenlace de este acto

**CANDIDATO VÁLIDO COMO PROXY, CONDUCTA DE CUIDADO** (§3.4). El supuesto exacto que habría que declarar para usarlo está escrito en §3.4. Riesgos abiertos para que mesa los pese junto con la decisión de mover o no el contador: el denominador estrecho de §3.2 (12.08% de la población de informantes), la brecha de cobertura de H-11 por condicionamiento a empleo (§3.5, solo 39.1% del denominador de obligación es evaluable), y el C2 "a un paso de fallar" de §3.7 si `familia.cuidado.recae_mujeres_40mas` se retiqueta a G5. **Esta sesión no adjudica ninguno de los tres.**

## 5 · Límite de lectura declarado (ADR-46)

Esta sesión leyó: `forense/notas/2026-07-31-encargo-c-familismo-deferencia-reactivo.md` completo; `canon/modelo-decision-v4_0.md` (secciones §1.1.A, §1.1.E/H-09..H-12, §1.6/reparto, §2/coeficientes, §3.4-3.5, completas); `canon/glosario-v5_6.md` (entrada `familismo_obligacion` y contexto de deudas/ADR-30); `milpa/procedencia.yaml` (bloques `familismo_apoyo`, coeficientes de generador, check ADR-30); `canon/gobernanza-v1_15.md` (entrada ADR-30); `forense/notas/2026-07-31-inventario-segmentacion.md` completo (Tabla B); `forense/notas/2026-08-01-p2-momentos-atributos.md` (extracto, filas G3/G4/G5); `forense/hallazgos.md` (entradas 2026-08-04 relevantes a C2/C3/ejes de ENVIPE, para contraste de patrón). Microdato abierto: `enut2024_fd.xlsx`, `enut2019_fd.xlsx` (íntegros, vía parseo XML propio); `enut2024_diccionario_variables.html`, `enut2019_diccionario_variables.html` (páginas RNM); `tmodulo.csv`, `tsdem.csv`, `thogar.csv` de `enut2024_bd_csv.zip` (columnas citadas, conteos de frecuencia — no fila por fila, no cruces más allá de los declarados en §3.2/§3.5); `TMODULO.csv` de `enut2019_bd_csv.zip/enut_2019/` (mismo alcance). **No se abrió** `enut2019_der_zip`/`enut2024_der_zip` (diseño de la muestra, no necesario para este acto), ni `enut_2019_indigena/`, ni `tvar_crea.csv` más allá de confirmar su existencia. Por ADR-46, esta sesión queda **inhabilitada para pre-registrar** contra ENUT.
