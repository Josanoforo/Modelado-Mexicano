# Encargo X — ¿sobreviven los tres al condicionar, y qué forma tiene la relación?

*4 de agosto de 2026. Mesa #19. Continúa el Encargo W (`forense/notas/
2026-08-04-w-coeficientes-generador-paso1.md`, `PR #89`, fusionado —
verificado: `gh pr view 89` → `MERGED`, `mergedAt` 2026-08-04T18:06:54Z;
`main` local sincronizado a `bfd7fcc`). Worktree nuevo
`mm-encargo-x-condicionamiento-forma`, rama
`sesion/encargo-x-condicionamiento-forma`, creada desde `origin/main` en
`bfd7fcc` (incluye `PR #89`).*

**Procedencia.** Tipo (1) para todo lo citado de `forense/notas/2026-08-04-
w-coeficientes-generador-paso1.md`, de `canon/modelo-decision-v4_0.md`, de
`forense/notas/2026-08-01-p2-momentos-atributos.md` ("P2"), de
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` y de
`forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md`, todo
verificado contra archivo en esta sesión (no aceptado de la nota sola).
Tipo (3) para el resto del encargo hasta contrastarlo — ninguna cita del
encargo resultó no sostenerse (a diferencia de otras sesiones de esta
mesa); no hay PARO por esta vía.

---

## 0 · Declaración de contaminación (ADR-46), antes de congelar §1-§2

Esta sesión abrió, antes de escribir la especificación:

- `BD_ENCUCI2020_dbf.zip`: nombres de campo de `ENCUCI_2020_SD.dbf` y
  `ENCUCI_2020_SEC_4_5.dbf` (estructura, ya conocida de Fase B); de
  `ENCUCI_2020_SEC_9_10.dbf` (estructura, nueva en este acto) — **y una
  frecuencia marginal univariada** de `AP10_14` (conteo por código, para
  confirmar los nueve códigos 1-9 documentados en `forense/notas/2026-08-
  03-cal-conf-faseb-medicion.md` §1.2). No se cruzó `AP10_14` contra
  ninguna otra variable.
- `encig23_base_datos_csv.zip`: cabeceras de columna de
  `encig2023_02_residentes_sec_2.csv`, `encig2023_01_sec_11.csv` y
  `encig2023_01_sec1_A_3_4_5_8_9_10.csv` (estructura) — **y una
  verificación de integridad de join** por `ID_PER` (38 966 de 38 966
  filas de `sec_11` encuentran fila en `residentes_sec_2`, cero pérdida) y
  **una frecuencia marginal univariada** de `EDAD` sobre esas 38 966 filas
  (rango 18-98, sin valores <18, código `98` como tope agregado "98 años o
  más" — sin `99` en este subconjunto). Ninguna relación reactivo↔desenlace
  vista: no se tocó `P11_1_23` ni `P8_3_*` en esta exploración.
- `enif2024_csv.zip`: listado completo de archivos (estructura del ZIP,
  ya con precedente de W3 §0 de su propia sesión); cabeceras de columna de
  `TVIVIENDA` y `TMODULO`; filas del diccionario de datos de `TMODULO`
  para `p3_14`, `p3_15_epc`, `p3_11a`, `p3_13`, `tloc`, `edad_v`
  (definiciones de campo, no filas de respondiente); catálogos completos
  `p3_14.csv` y `p3_15_epc.csv` (etiquetas de categoría). Ninguna fila de
  respondiente leída fuera de estas exploraciones de estructura, ninguna
  relación reactivo↔desenlace calculada.

**Con o sin este matiz, el Acto ya se declaraba contaminado** para
pre-registrar contra ENCUCI, ENCIG y ENIF, igual que W — esta declaración
la hace precisa, no cambia la conclusión.

⚠️ **Hallazgo de corrección, no de fondo, encontrado en esta exploración:**
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §1.3 declaró
"Acceso digital: NO DISPONIBLE" para ENIF, con la salvedad explícita de
que era "no verificado, no ausente confirmado" (`TVIVIENDA`/`TSDEM` no se
habían abierto en ese acto). Esta sesión sí abrió el diccionario de
`TMODULO` completo y encuentra `p3_14` ("¿Usted tiene un celular
inteligente (smartphone)?", catálogo `1` Sí / `2` No), que **vive en la
misma tabla `TMODULO`, sin join adicional** — coincide, además, con lo que
`forense/notas/2026-07-31-inventario-segmentacion.md` línea 105 ya tenía
registrado para el eje 5 de ENIF ("Sí (fuerte)... `P3_14` (smartphone)...")
y que la sesión de médicion del 03/ago no cruzó contra ese inventario antes
de declarar NO DISPONIBLE. **Se corrige aquí, explícito:** ENIF sí tiene
acceso digital disponible en régimen estricto, dentro de `TMODULO`. Esta
sesión lo usa (§1.3 abajo); no se edita la nota de 03/ago (perímetro de
esta sesión no la toca), pero queda declarado para que quien la lea después
no repita el NO DISPONIBLE.

**Ningún eje declarado estricto por C4 (P2 §1.c) resultó ausente del
instrumento real en esta verificación — no hay PARO por esta vía en
ninguno de los tres coeficientes.** (Ver además el hallazgo de arriba,
que va en la dirección contraria: un eje que P2 ya daba por estricto y
que una sesión posterior había marcado erróneamente NO DISPONIBLE.)

---

## 1 · X1 — Especificación de la estratificación, congelada antes de calcular

**Estimador, dentro de cada celda, para los tres coeficientes:** el mismo
de `forense/notas/2026-08-04-w-coeficientes-generador-paso1.md` §1 —
diferencia de proporciones ponderada entre el grupo `θ=1` y el grupo `θ=0`
**dentro de la celda**, cada proporción vía
`tests/svystat.py::prop_ultimate_cluster` (sin modificar) sobre las filas
de esa celda, `β̂_celda = p̂(θ=1|celda) − p̂(θ=0|celda)`,
`se(β̂_celda) = sqrt(se₁² + se₂²)`, IC95% con 1.96 unidades de
`se(β̂_celda)`. No es un estimador nuevo: es la misma diferencia de
proporciones de W, aplicada al subconjunto de filas que cae en cada nivel
de un eje, un eje a la vez — nunca todos los ejes de un coeficiente
cruzados entre sí.

**n mínimo por celda: 30 sin ponderar, en cada uno de los dos grupos
(`θ=1` y `θ=0`) de la celda** — mismo umbral que toda Fase B
(`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §1.0). Si algún
grupo cae debajo, la celda se reporta **SIN SOPORTE** con su `n`, no se
colapsa con celdas vecinas ni se omite.

### 1.1 · W1 — G1 · `radio_confianza` (ENCUCI 2020)

Reactivo, desenlace, dicotomización y universo: **idénticos a
`w-coeficientes-generador-paso1.md` §1.1**, reusados sin re-derivar:

- θ (tres ítems, medidos por separado): `AP5_1_1`/`AP5_1_2`/`AP5_1_3`,
  confía=`{06..10}` / no confía=`{00..05}`, excluido `99`.
- Desenlace: `tramite.mordida.discrecional` — 1 si `AP5_17='1'` o
  `AP5_18='1'`, 0 si ambas `='2'`, excluido en otro caso. Universo: contacto
  (`AP5_16_1..10`, al menos un `'1'`).
- Ponderador `FAC_SEL`, estrato `EST_DIS`, UPM `UPM_DIS` — de
  `ENCUCI_2020_SEC_4_5.dbf`, la misma tabla que trae reactivo y desenlace.

**Ejes, uno a la vez (C4 de P2: ENCUCI 3 ejes estrictos — formalidad, edad,
ingreso):**

- **Formalidad** — `AP3_15_4` (`ENCUCI_2020_SD.dbf`): `1`=Formal,
  `0`=Informal, blanco excluido (no trabajó la semana de referencia,
  no-aplicabilidad estructural). Join `SEC_4_5.R_SEL` = `SD.N_REN` sobre
  `UPM`+`VIV_SEL` — mismo join que Fase B verificó y que W1 no necesitó
  usar por ser marginal.
- **Edad** — `EDAD` (`ENCUCI_2020_SD.dbf`), mismo join. Tramos: `18-29` ·
  `30-44` · `45-59` · `60+` (mismo corte que toda Fase B, declarado, no
  derivado de los datos); código `96` incluido en `60+`; `97`/`98`/`99`
  excluidos (no-respuesta/no aplica).
- **Ingreso** — `AP10_14` (`ENCUCI_2020_SEC_9_10.dbf`): seis tramos
  nativos del instrumento (`1` `<$3,000` … `6` `>$11,000`), `7` ("No
  recibe ingresos") como celda propia, `8`/`9` excluidos (no
  quiere decir / no sabe). Join `SEC_4_5.R_SEL` = `SEC_9_10.R_SEL` sobre
  `UPM`+`VIV_SEL` — mismo patrón de llave que el eje anterior, verificado
  en esta sesión (§0) contra la frecuencia marginal real.

Tres ejes × tres ítems de θ = 9 tablas, cada una con 2 (formalidad), 4
(edad) o 7 (ingreso) celdas.

### 1.2 · W2 — G1 · `confianza_institucional` (ENCIG 2023)

Reactivo, desenlace, dicotomización y universo: **idénticos a
`w-coeficientes-generador-paso1.md` §1.2**:

- θ: `P11_1_23` (`encig2023_01_sec_11.csv`), confía=`{1,2}` / no
  confía=`{3,4}`, excluidos `5` (no aplica) y `9` (no sabe).
- Desenlace: `tramite.mordida.discrecional` — 1 si `P8_3_1='1'` o
  `P8_3_2='1'` o `P8_3_3='1'` (`encig2023_01_sec1_A_3_4_5_8_9_10.csv`), 0
  si las tres `='2'`, excluido en otro caso. Universo: completo (38 966
  filas, sin código de no-aplicabilidad).
- Ponderador `FAC_P18`, estrato `EST_DIS`, UPM `UPM_DIS` — ambas tablas,
  misma edición 2023, unidas por `ID_PER` (cero pérdida, verificado de
  nuevo en §0).

**Eje único (C4 de P2: ENCIG 1 eje estricto — edad; sin ingreso ni
ruralidad en ningún régimen, truncado, heredado y no resuelto aquí):**

- **Edad** — `EDAD` (`encig2023_02_residentes_sec_2.csv`), unida por
  `ID_PER` directo (mismo patrón que la fila de salud de `cal-conf-faseb-
  medicion.md` §1.1 usó para ENCIG 2021; verificado en esta sesión con
  ENCIG 2023: 38 966 de 38 966 filas de `sec_11` encuentran `ID_PER` en
  `residentes_sec_2`, cero pérdida — §0). Tramos: `18-29` · `30-44` ·
  `45-59` · `60+`; código `98` incluido en `60+` (tope agregado, sin
  registros <18 en este subconjunto adulto — §0); ningún código adicional
  que excluir en esta población.

Un eje × un ítem de θ = 1 tabla, 4 celdas.

### 1.3 · W3 — G3 · `familismo_apoyo` (ENIF 2024)

Reactivo, desenlace, dicotomización y universo: **idénticos a
`w-coeficientes-generador-paso1.md` §1.3**:

- θ: `p9_9_4` (`TMODULO`), binario `1` Sí / `2` No / `9` No sabe. Universo
  efectivo: `filtro_s9_1=2` (<71 años), n=12 379.
- Desenlace: `dinero.ahorro.volatilidad_horizonte_corto` — `p4_10`,
  horizonte-cero=`{1}` / no-cero=`{2,3,4,5}`, excluidos `8`/`9`.
- Ponderador `fac_per`, estrato `est_dis`, UPM `upm_dis` — todo en
  `TMODULO`, sin join.

**Seis ejes, uno a la vez (C4 de P2: ENIF 6 ejes estrictos — la malla más
rica del corpus):**

- **Formalidad** — `p3_13`: `1`-`6` (cualquier derechohabiencia por
  trabajo) = Formal, `7` = Informal; blanco (no trabaja) y `9` (no sabe)
  excluidos. Reusado de `cal-conf-faseb-medicion.md` §1.3.
- **Edad** — `edad_v`, mismos tramos de siempre.
- **Urbanización** — `tloc`: `1` 100,000+ · `2` 15,000–99,999 · `3`
  2,500–14,999 · `4` <2,500. Reusado, idéntico esquema a `tam_loc` de
  ENIGH (única fuente donde el análogo es exacto, `cal-conf-faseb-
  medicion.md` §1.3).
- **Ingreso** — `p3_11a` (monto continuo en pesos): `0` = "Sin ingreso"
  (celda propia, análoga al código `7` de `AP10_14`), recodificado a los
  **mismos seis tramos declarados para `AP10_14`** (`<$3,000` …
  `>$11,000`) por monto — misma recodificación que `cal-conf-faseb-
  medicion.md` §1.3 declaró "para comparabilidad aproximada entre
  componentes, no derivada de los datos de ENIF"; reusada aquí, no
  re-derivada. Códigos `98000`/`99888` excluidos (no sabe/no responde).
- **Migración** — `p3_15_epc`: `001`-`032` (entidad mexicana) = no
  migrante, código ≥`200` (país extranjero) = migrante internacional,
  `999` excluido. Reusado de `cal-conf-faseb-medicion.md` §1.3, con su
  misma advertencia: referencia temporal "hace cinco años", declarada por
  el instrumento, no confirmada equivalente a ningún proxy de ENIGH.
- **Acceso digital** — `p3_14` ("¿Usted tiene un celular inteligente
  (smartphone)?"): `1` Sí / `2` No. **Eje nuevo en este acto** — no
  ejecutado por `cal-conf-faseb-medicion.md`, que lo había declarado NO
  DISPONIBLE sin haber visto el diccionario completo de `TMODULO` (§0,
  hallazgo de corrección). Vive en `TMODULO`, sin join.

Seis ejes × un ítem de θ = 6 tablas, con 2 (formalidad, migración, digital),
4 (edad, urbanización) o 7 (ingreso) celdas cada una.

### 1.4 · Lo que X1 no hace, declarado antes de correrlo

- No cruza más de un eje a la vez, para ningún coeficiente — ni siquiera
  el conjunto formalidad×edad que Fase B sí cruzó para la condicional
  θ(x). Aquí el objeto condicionado es β̂, no θ, y el encargo (§2) pide
  explícitamente "un eje a la vez, no todos cruzados".
- No produce un β̂ "ajustado" único que sustituya al marginal de W —
  combinar celdas en un solo número es una decisión de ponderación que
  este acto no toma (§2 del encargo).
- No re-elige ningún corte de dicotomización de W (`≥6/10`, `{1,2}` de
  confianza institucional, `{1}` de horizonte-corto) — se heredan tal
  cual.
- No colapsa celdas SIN SOPORTE con celdas vecinas.

---

## 2 · X2 — Especificación de la forma funcional, leída no ajustada

**Aplica solo donde θ tiene escala de más de dos niveles** (§3 del
encargo):

- **W1 — `radio_confianza`:** los tres ítems `AP5_1_1`/`AP5_1_2`/`AP5_1_3`
  viven en escala 0-10 (11 niveles, excluido `99`). X2 aplica a los tres.
- **W2 — `confianza_institucional`:** `P11_1_23` vive en escala ordinal de
  4 niveles (`1` mucha confianza … `4` mucha desconfianza, excluidos `5`/
  `9`) — verificado contra el descriptor en §1.2/W paso1 §1.2: más de dos
  niveles. X2 aplica.
- **W3 — `familismo_apoyo`:** `p9_9_4` es binario (`1`/`2`) — verificado en
  §1.3. **X2 no aplica a W3 y no se fuerza**, como pide el encargo.

**Método, para cada nivel de θ donde aplica:** tasa ponderada del
desenlace correspondiente (mismo desenlace, misma dicotomización, mismo
universo, mismo ponderador/estrato/UPM que en X1/W) vía
`tests/svystat.py::prop_ultimate_cluster` sobre las filas de ese nivel —
una fila de tabla por nivel de θ, con `n`, `p̂`, `se`, IC95%. Ningún ajuste
de curva, ninguna familia paramétrica, ninguna decisión sobre cuál forma
"gana" — eso lo hace mesa, leyendo la tabla.

**El corte de W se reporta al lado de la curva, no se re-elige:**
`≥6/10` para W1 (los tres ítems), `{1,2}` vs `{3,4}` para W2.

### 2.1 · Prohibido en X2, declarado antes de correrlo

- Ajustar una logística, probit, lineal, o cualquier familia paramétrica
  sobre las tasas por nivel.
- Escribir cuál forma (recta, S, umbral) "gana" — se reporta la curva.
- Proponer que se declare una forma en `canon/` — sigue prohibido por
  `canon/modelo-decision-v4_0.md:149` hasta que mesa decida que esta
  evidencia basta.

---

## 3 · Lo que este procedimiento no hace, en conjunto — declarado antes de correrlo

- No mide un coeficiente nuevo — los tres β̂ marginales de W siguen siendo
  lo que `milpa/procedencia.yaml:630-690` ya reporta; este acto solo
  añade evidencia de condicionamiento y de forma sobre esos mismos tres.
- No compara ningún β̂ (marginal ni por celda) contra el valor `ASIGNADO`
  en magnitud — mismo límite permanente que W §1 del encargo declaró.
- No decide si el marginal de W "aguanta" — reporta si β̂ es estable o
  varía entre celdas, con esas palabras; la lectura de qué implica eso
  para el generador es de mesa.
- No toca `canon/`, `asignados_coeficiente.detalle`, el bloque
  append-only, `data/manifiesto.yaml`, ni `tests/svystat.py`.

**El primer resultado que produzca este procedimiento es el que se
reporta.**
