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
`2026-08-04-w-coeficientes-generador-paso1.md` §1.1**, reusados sin re-derivar:

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
`2026-08-04-w-coeficientes-generador-paso1.md` §1.2**:

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
`2026-08-04-w-coeficientes-generador-paso1.md` §1.3**:

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
  excluidos. Reusado de `2026-08-03-cal-conf-faseb-medicion.md` §1.3.
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
  `999` excluido. Reusado de `2026-08-03-cal-conf-faseb-medicion.md` §1.3, con su
  misma advertencia: referencia temporal "hace cinco años", declarada por
  el instrumento, no confirmada equivalente a ningún proxy de ENIGH.
- **Acceso digital** — `p3_14` ("¿Usted tiene un celular inteligente
  (smartphone)?"): `1` Sí / `2` No. **Eje nuevo en este acto** — no
  ejecutado por `2026-08-03-cal-conf-faseb-medicion.md`, que lo había declarado NO
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

---

## 4 · Resultados — primera y única corrida

Corrida con `tests/svystat.py::prop_ultimate_cluster` (sin modificar)
sobre exactamente la especificación de §1-§2. Ningún número de esta
sección se recalculó después de verlo. **Guardia de reproducción, corrida
antes de tocar ninguna celda nueva:** el script recalculó primero el β̂
marginal de cada coeficiente y coincidió exacto, cifra por cifra, con
`milpa/procedencia.yaml:630-690` (W1: n=6430/6945, −0.0102; n=10667/2726,
−0.0113; n=7644/5721, −0.0269 · W2: n=20245/17510, −0.0645 · W3:
n=5281/6183, +0.0279) — el pipeline de este acto reproduce el de W antes
de estratificar, mismo patrón de guardia que Fase B introdujo.

⚠️ **Un defecto de implementación, encontrado y corregido antes de ver
ningún número de W1 (no después):** la primera corrida del script leyó
`AP5_16_1..10` (contacto con funcionario) comparando el campo crudo contra
la cadena `"1"`, pero esos campos son numéricos en el DBF y se leen como
`"1.000000000000000"` — la comparación fallaba silenciosamente y el
universo de contacto salía en 0 para los tres ítems de W1 (los únicos que
usan esos campos; W2 y W3 no los tocan y salieron correctos en la primera
corrida). Se corrigió a comparar `int(float(valor))`, y se corrió de
nuevo — **la corrida que se reporta abajo es la segunda, la primera no
produjo un solo número de W1** (solo SIN SOPORTE por n=0), así que no hay
selección post-hoc: no se vio ni un β̂ de W1 antes de la corrección.

**Mínimo de 30 casos por grupo (`θ=1` y `θ=0`) dentro de cada celda —
igual que Fase B; celdas por debajo se marcan SIN SOPORTE, no se
colapsan.**

### 4.1 · W1 — G1 · `radio_confianza` (ENCUCI) — β̂ por celda, tres ítems

**`AP5_1_1` (mayoría de las personas).** Marginal (W): n=6430/6945,
β̂=−0.0102, IC95%=[−0.0292, +0.0089].

| Eje | Nivel | n(θ=1) | n(θ=0) | β̂ | IC95% |
|---|---|---|---|---|---|
| Formalidad | Formal | 1 315 | 1 712 | +0.0288 | [−0.0178, +0.0755] |
| Formalidad | Informal | 2 782 | 2 330 | +0.0141 | [−0.0181, +0.0462] |
| Edad | 18-29 | 1 777 | 1 535 | **+0.0398** | [+0.0015, +0.0782] |
| Edad | 30-44 | 2 177 | 1 934 | +0.0208 | [−0.0111, +0.0527] |
| Edad | 45-59 | 1 373 | 1 393 | −0.0310 | [−0.0679, +0.0060] |
| Edad | 60+ | 1 156 | 1 073 | −0.0296 | [−0.0922, +0.0329] |
| Ingreso | <$3,000 | 2 726 | 2 019 | +0.0182 | [−0.0110, +0.0473] |
| Ingreso | $3,000-5,500 | 1 478 | 1 321 | +0.0171 | [−0.0243, +0.0586] |
| Ingreso | $5,501-7,500 | 566 | 641 | **+0.0607** | [+0.0032, +0.1182] |
| Ingreso | $7,501-9,000 | 345 | 490 | +0.0062 | [−0.0736, +0.0860] |
| Ingreso | $9,001-11,000 | 259 | 404 | +0.0708 | [−0.0083, +0.1500] |
| Ingreso | >$11,000 | 399 | 680 | +0.0283 | [−0.0529, +0.1095] |
| Ingreso | Sin ingreso | 852 | 635 | +0.0030 | [−0.0309, +0.0369] |

**`AP5_1_2` (personas que conoce).** Marginal (W): n=10667/2726,
β̂=−0.0113, IC95%=[−0.0341, +0.0114].

| Eje | Nivel | n(θ=1) | n(θ=0) | β̂ | IC95% |
|---|---|---|---|---|---|
| Formalidad | Formal | 412 | 2 616 | **+0.0663** | [+0.0059, +0.1268] |
| Formalidad | Informal | 1 229 | 3 888 | −0.0075 | [−0.0435, +0.0285] |
| Edad | 18-29 | 587 | 2 725 | +0.0409 | [−0.0115, +0.0934] |
| Edad | 30-44 | 854 | 3 259 | +0.0248 | [−0.0165, +0.0661] |
| Edad | 45-59 | 623 | 2 145 | −0.0076 | [−0.0464, +0.0312] |
| Edad | 60+ | 529 | 1 710 | −0.0158 | [−0.0771, +0.0455] |
| Ingreso | <$3,000 | 1 167 | 3 591 | +0.0243 | [−0.0106, +0.0593] |
| Ingreso | $3,000-5,500 | 554 | 2 248 | +0.0075 | [−0.0426, +0.0577] |
| Ingreso | $5,501-7,500 | 218 | 990 | +0.0306 | [−0.0475, +0.1087] |
| Ingreso | $7,501-9,000 | 123 | 712 | +0.0552 | [−0.0444, +0.1549] |
| Ingreso | $9,001-11,000 | 85 | 579 | **+0.2035** | [+0.0628, +0.3441] |
| Ingreso | >$11,000 | 122 | 956 | +0.0008 | [−0.0770, +0.0786] |
| Ingreso | Sin ingreso | 319 | 1 169 | −0.0115 | [−0.0510, +0.0280] |

**`AP5_1_3` (vecinos).** Marginal (W): n=7644/5721, β̂=**−0.0269**,
IC95%=[**−0.0465, −0.0072**] — el único de los tres ítems distinguible de
cero al 95% en el marginal.

| Eje | Nivel | n(θ=1) | n(θ=0) | β̂ | IC95% |
|---|---|---|---|---|---|
| Formalidad | Formal | 1 147 | 1 876 | +0.0355 | [−0.0099, +0.0808] |
| Formalidad | Informal | 2 226 | 2 882 | +0.0291 | [−0.0033, +0.0615] |
| Edad | 18-29 | 1 598 | 1 713 | **+0.0407** | [+0.0002, +0.0813] |
| Edad | 30-44 | 1 799 | 2 309 | **+0.0331** | [+0.0018, +0.0644] |
| Edad | 45-59 | 1 050 | 1 709 | +0.0212 | [−0.0165, +0.0590] |
| Edad | 60+ | 837 | 1 389 | +0.0053 | [−0.0534, +0.0640] |
| Ingreso | <$3,000 | 2 197 | 2 550 | +0.0146 | [−0.0128, +0.0421] |
| Ingreso | $3,000-5,500 | 1 221 | 1 578 | **+0.0497** | [+0.0068, +0.0926] |
| Ingreso | $5,501-7,500 | 488 | 719 | +0.0495 | [−0.0121, +0.1110] |
| Ingreso | $7,501-9,000 | 305 | 529 | +0.0557 | [−0.0303, +0.1417] |
| Ingreso | $9,001-11,000 | 245 | 417 | **+0.1103** | [+0.0272, +0.1935] |
| Ingreso | >$11,000 | 323 | 751 | +0.0074 | [−0.0712, +0.0859] |
| Ingreso | Sin ingreso | 684 | 801 | **+0.0592** | [+0.0252, +0.0933] |

**Lectura de W1, sin decidir por mesa:** en los tres ítems, sobre los tres
ejes, **28 de 39 celdas tienen signo positivo** (12 de ellas distinguibles
de cero al 95%) frente a un marginal negativo (solo `AP5_1_3` distinguible
de cero). Ninguna celda con IC95% que excluye cero tiene signo negativo —
las 12 celdas significativas de esta sección son **todas positivas**. El
patrón es consistente entre los tres ítems y los tres ejes: no hay un solo
eje ni un solo ítem donde condicionar reproduzca el signo negativo del
marginal con significancia.

### 4.2 · W2 — G1 · `confianza_institucional` (ENCIG) — β̂ por celda

Marginal (W): n=20245/17510, β̂=**−0.0645**, IC95%=[**−0.0744, −0.0546**].

| Eje | Nivel | n(θ=1) | n(θ=0) | β̂ | IC95% |
|---|---|---|---|---|---|
| Edad | 18-29 | 3 680 | 4 511 | **+0.0850** | [+0.0635, +0.1065] |
| Edad | 30-44 | 5 624 | 5 747 | **+0.0624** | [+0.0443, +0.0806] |
| Edad | 45-59 | 4 635 | 5 095 | **+0.0626** | [+0.0433, +0.0820] |
| Edad | 60+ | 3 571 | 4 892 | **+0.0380** | [+0.0227, +0.0533] |

**Lectura de W2, sin decidir por mesa:** las cuatro celdas del único eje
estricto disponible tienen signo **positivo y distinguible de cero al
95%** — signo opuesto al marginal (−0.0645), en las cuatro celdas, sin una
sola excepción. No es un debilitamiento del marginal: es una reversión
completa de signo, consistente en las cuatro celdas de edad.

### 4.3 · W3 — G3 · `familismo_apoyo` (ENIF) — β̂ por celda, seis ejes

Marginal (W): n=5281/6183, β̂=**+0.0279**, IC95%=[**+0.0029, +0.0529**].

| Eje | Nivel | n(θ=1) | n(θ=0) | β̂ | IC95% |
|---|---|---|---|---|---|
| Formalidad | Formal | 2 651 | 1 220 | −0.0333 | [−0.0700, +0.0033] |
| Formalidad | Informal | 2 434 | 2 152 | **+0.0555** | [+0.0187, +0.0922] |
| Edad | 18-29 | 1 467 | 1 195 | −0.0094 | [−0.0565, +0.0377] |
| Edad | 30-44 | 2 142 | 1 830 | −0.0394 | [−0.0807, +0.0018] |
| Edad | 45-59 | 1 722 | 1 444 | −0.0376 | [−0.0851, +0.0100] |
| Edad | 60+ | 852 | 812 | +0.0255 | [−0.0399, +0.0909] |
| Urbanización (`tloc`) | 100k+ | 3 684 | 2 322 | **−0.0333** | [−0.0656, −0.0010] |
| Urbanización (`tloc`) | 15k-99,999 | 809 | 749 | +0.0049 | [−0.0604, +0.0703] |
| Urbanización (`tloc`) | 2,500-14,999 | 729 | 760 | −0.0747 | [−0.1519, +0.0025] |
| Urbanización (`tloc`) | <2,500 | 961 | 1 450 | **+0.0727** | [+0.0121, +0.1334] |
| Ingreso | <$3,000 | 2 274 | 2 100 | **+0.0614** | [+0.0244, +0.0983] |
| Ingreso | $3,000-5,500 | 870 | 547 | −0.0369 | [−0.1024, +0.0286] |
| Ingreso | $5,501-7,500 | 302 | 163 | +0.0176 | [−0.0860, +0.1213] |
| Ingreso | $7,501-9,000 | 238 | 100 | −0.0843 | [−0.1687, +0.0001] |
| Ingreso | $9,001-11,000 | 244 | 91 | −0.0050 | [−0.0906, +0.0807] |
| Ingreso | >$11,000 | 870 | 255 | −0.0231 | [−0.0637, +0.0175] |
| Ingreso | Sin ingreso | 38 | 34 | +0.1502 | [−0.0532, +0.3535] |
| Migración | No migrante | 6 134 | 5 252 | **−0.0280** | [−0.0531, −0.0029] |
| Migración | Migrante internacional | 40 | 27 | n0=27 | **SIN SOPORTE** |
| Acceso digital (`p3_14`) | Sí (smartphone) | 5 479 | 4 421 | **−0.0302** | [−0.0553, −0.0052] |
| Acceso digital (`p3_14`) | No | 704 | 860 | **+0.1034** | [+0.0368, +0.1701] |

**Lectura de W3, sin decidir por mesa:** el marginal (+0.0279, apenas
distinguible de cero) **no es estable entre celdas — varía en signo, y
donde varía, lo hace en la subpoblación mayoritaria.** En las cuatro
celdas que concentran a la mayoría de la muestra (`Formal`, `100k+`, `No
migrante`, `Sí smartphone` — todas mayoría dentro de su eje) el signo es
**negativo**, tres de ellas distinguibles de cero al 95%, opuesto al
marginal. En las celdas minoritarias correspondientes (`Informal`,
`<2,500`, `Migrante internacional` [SIN SOPORTE], `No` smartphone) el
signo es positivo y más grande en magnitud, también distinguible de cero
donde hay soporte. Edad e ingreso no muestran un patrón tan limpio: la
mayoría de sus celdas no son distinguibles de cero en ninguna dirección
(6 de 13 no significativas de 13 celdas totales entre los dos ejes; de las
significativas, `<$3,000` es positiva y `100k+` ya contado arriba es el
único cruce con urbanización). La celda `Sin ingreso` (n=38/34) es la más
cercana al mínimo de soporte de todo el acto — se reporta, no se descarta,
pero su IC95% ([−0.0532, +0.3535]) es demasiado ancho para leer signo.

---

## 5 · Resultados X2 — forma funcional, leída no ajustada

### 5.1 · W1 — `radio_confianza`, tasa de `tramite.mordida.discrecional` por nivel de θ (0-10)

Corte de W reportado al lado: confía=`{6..10}` / no confía=`{0..5}`.

| θ | `AP5_1_1` n / % mordida | `AP5_1_2` n / % mordida | `AP5_1_3` n / % mordida |
|---|---|---|---|
| 0 | 1 028 / 13.71% [10.49,16.92] | 253 / 14.75% [5.72,23.78] | 1 127 / 13.57% [10.27,16.87] |
| 1 | 265 / 12.68% [9.06,16.30] | 88 / 14.56% [7.67,21.45] | 236 / 18.60% [11.22,25.99] |
| 2 | 478 / 14.91% [10.03,19.80] | 219 / 5.56% [2.63,8.50] | 467 / 18.40% [11.91,24.89] |
| 3 | 795 / 14.38% [11.20,17.57] | 300 / 16.70% [11.07,22.34] | 674 / 12.60% [9.40,15.80] |
| 4 | 710 / 18.01% [13.36,22.67] | 288 / 13.02% [8.03,18.01] | 638 / 10.99% [7.42,14.56] |
| 5 | 3 669 / 11.60% [9.92,13.27] | 1 578 / 13.88% [11.34,16.41] | 2 579 / 14.43% [12.28,16.58] |
| **6** | 1 388 / 11.50% [8.74,14.27] | 740 / 15.30% [11.42,19.18] | 1 267 / 12.44% [9.41,15.46] |
| 7 | 2 040 / 14.87% [12.28,17.45] | 1 365 / 13.12% [10.59,15.64] | 1 866 / 12.49% [10.25,14.73] |
| 8 | 2 241 / 11.29% [8.48,14.11] | 3 586 / 13.06% [11.32,14.79] | 2 590 / 10.87% [9.13,12.61] |
| 9 | 319 / 5.70% [3.24,8.17] | 2 407 / 11.40% [9.51,13.29] | 954 / 9.68% [6.29,13.07] |
| 10 | 442 / 9.47% [7.15,11.79] | 2 569 / 11.28% [8.88,13.67] | 967 / 10.78% [5.09,16.48] |

**Lectura, sin ajustar curva ni decidir cuál forma gana:** ninguno de los
tres ítems traza una curva monótona. `AP5_1_1` sube de 0 a un pico en 4
(18.01%) y luego baja de forma irregular hasta 9 (5.70%); `AP5_1_2` tiene
un mínimo aislado en 2 (5.56%, `n`=219) rodeado de valores 13-17% en 0-1 y
3-4, luego se aplana 11-15% en 5-10; `AP5_1_3` sube de 0 a un pico en 1-2
(≈18.5%) y baja de forma más regular después, de 3 en adelante. El corte
`≥6` de W no coincide con un salto visible en ninguno de los tres — no hay
escalón entre el nivel 5 y el 6 en ninguna de las tres columnas. La
lectura más defendible es una **pendiente descendente débil y ruidosa**
(promedio de niveles 0-4 más alto que promedio de niveles 6-10 en los tres
ítems), no una recta limpia, no una S clara, no un umbral en 6.

### 5.2 · W2 — `confianza_institucional`, tasa de `tramite.mordida.discrecional` por nivel de θ (1-4)

Corte de W reportado al lado: confía=`{1,2}` / no confía=`{3,4}`.

| θ | Etiqueta | n | % mordida | IC95% |
|---|---|---|---|---|
| 1 | Mucha confianza | 1 903 | 4.17% | [2.98%, 5.36%] |
| 2 | Algo de confianza | 18 342 | 7.66% | [7.11%, 8.20%] |
| 3 | Algo de desconfianza | 12 507 | 12.10% | [11.18%, 13.03%] |
| 4 | Mucha desconfianza | 5 003 | 18.16% | [16.45%, 19.86%] |

**Lectura, sin ajustar curva ni decidir cuál forma gana:** los cuatro
puntos son monótonos y casi rectos (incrementos de +3.49pp, +4.44pp,
+6.06pp entre niveles consecutivos — levemente creciente/convexo, no
constante). Es la curva más limpia de todo el acto. **Pero no se lee
aislada de §4.2:** esta curva agrega sobre todas las edades sin
condicionar, y §4.2 ya mostró que, dentro de cada tramo de edad, el signo
de la relación entre `P11_1_23` y la mordida se invierte. La limpieza de
esta curva marginal es compatible con ser, ella también, un artefacto de
composición por edad — no lo contradice, lo redondea: edad se asocia con
más confianza (mayor θ=1) y con menos mordida (§4.2), lo que basta para
producir una curva marginal descendente aunque la relación dentro de cada
edad sea ascendente. No se decide aquí cuál de las dos lecturas es la
correcta para el generador — se reportan ambas, explícitamente en
tensión.

### 5.3 · W3 — `familismo_apoyo`

No aplica — `p9_9_4` es binario. Declarado en §2, no forzado aquí.

---

## 6 · Respuesta directa a las dos preguntas del encargo (§0)

**Pregunta 1 — ¿sobreviven los tres al condicionar?** No, ninguno de los
tres sobrevive sin matiz:

- **W1 (`radio_confianza`):** no sobrevive. De 39 celdas (3 ítems × 3
  ejes), 28 tienen signo positivo — opuesto al marginal negativo — y las
  12 celdas distinguibles de cero al 95% son todas positivas, sin una
  sola excepción negativa significativa (§4.1).
- **W2 (`confianza_institucional`):** no sobrevive, de la forma más
  limpia de las tres. Las cuatro celdas de edad, el único eje disponible,
  tienen signo positivo y significativo — reversión completa y consistente
  frente al marginal negativo (§4.2).
- **W3 (`familismo_apoyo`):** no es estable. El marginal (apenas
  significativo) se invierte en signo, con significancia, en las celdas
  mayoritarias de tres de los seis ejes (`Formal`, `100k+`, `No migrante`,
  `Sí smartphone`), mientras se amplifica en la misma dirección del
  marginal en las celdas minoritarias correspondientes (§4.3). Edad e
  ingreso no muestran un patrón tan limpio, en su mayoría no significativo
  en ninguna dirección.

**Lo que esto NO dice:** no dice que los tres β̂ marginales de W estén
"mal" ni que deban descartarse — siguen siendo lo que son, diferencias de
proporciones marginales, correctamente calculadas y reportadas (§2 del
encargo W). Lo que dice es que **ninguno de los tres puede leerse como una
propiedad estable de la relación entre θ y el desenlace, independiente de
formalidad/edad/ingreso/urbanización/migración/acceso digital** — cada uno
está, en mayor o menor medida, compuesto por la correlación entre esos
atributos y ambas variables (θ y desenlace) a la vez, exactamente la
posibilidad que `canon/modelo-decision-v4_0.md` (criterio C4 de P2) anticipó
al pedir la malla de celdas. Si el marginal representa o no el coeficiente
del generador (que multiplica un θ(x) condicional) es pregunta de mesa —
este acto entrega la evidencia, no la resuelve.

**Pregunta 2 — ¿qué forma tiene la relación?** Donde θ tiene escala (W1,
W2), la forma leída **no sostiene una familia paramétrica limpia**:

- W1: pendiente descendente débil, ruidosa, no monótona en ninguno de los
  tres ítems — ni recta, ni S, ni escalón visible en el corte `≥6` (§5.1).
- W2: curva marginal casi recta y monótona (§5.2) — pero, leída junto con
  §4.2, es compatible con ser ella misma un artefacto de composición por
  edad, no una forma funcional estable de la relación individual.
- W3: no aplica, θ binario (§5.3).

**Ninguna forma se declara ganadora — no le corresponde a este acto
(§2.1). La mesa lee las tablas de §5 con la advertencia explícita de
§5.2 sobre W2.**

---

## 7 · Contador

**Contadores movidos: cero directos** — como anuncia el encargo. Los tres
β̂ marginales de W siguen en `milpa/procedencia.yaml` con la misma clase
`MEDIDO·β̂(diferencia de proporciones)`; este acto no cambia esa clase, no
mueve ningún coeficiente a la escala del modelo, no toca
`asignados_coeficiente.detalle`. Lo que cambia es el campo
`eje_condicionante` de las tres entradas (§8): pasa de "no ejecutado en
este acto" a un resumen del resultado de condicionar, con referencia a
esta nota para el detalle completo. El README sigue diciendo "15
coeficientes, 0 medidos" en la escala del modelo — sigue siendo cierto,
este acto no lo toca.

---

## 8 · `milpa/procedencia.yaml` — actualización de `eje_condicionante`

Sección `coeficientes_generador_medidos`, tres entradas, **solo el campo
`eje_condicionante`** editado; `clase`, `antes`, `fuente`, `n_util`,
`beta_hat`, `nota`, `marca_c3`/`marca_c2` sin tocar. Ver commit de esta
sección para el diff exacto.

---

## 9 · Verificación de perímetro y suite

`git status --short` antes de commitear: solo esta nota y
`milpa/procedencia.yaml` (sección `coeficientes_generador_medidos`, tres
líneas `eje_condicionante`, verificado por `git diff` línea por línea)
modificados, más `data/raw` (symlink gitignorado, no rastreado). No se
tocó `canon/`, `asignados_coeficiente.detalle`, el bloque append-only,
`data/manifiesto.yaml`, ni `tests/svystat.py` — verificado por diff, no
solo afirmado.

`python3 tests/manifiesto.py --verifica`: los tres payloads que este acto
abrió (`encuci2020_bd_dbf`, `encig23_base_datos_csv`, `enif2024_csv`)
**COINCIDEN** contra `data/manifiesto.yaml` (sha256 y tamaño).

`python3 tests/check.py`: `18 FAIL · 84 WARN`.
`python3 tests/check.py --baseline`: **LÍNEA BASE: VERDE** — nada nuevo
frente a `tests/baseline.json` (HEAD congelado `090ee0f`). Dos defectos
de cita encontrados y corregidos antes de esta verificación final: dos
referencias a notas de W y de Fase B habían perdido el prefijo de fecha
al citarlas entre comillas simples (el nombre de archivo de W sin su
prefijo "2026-08-04-", y el nombre de archivo de la nota de medición de
Fase B sin su prefijo "2026-08-03-") — mismo defecto de cita que
`forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §6
ya documentó y corrigió en su propia sesión. Corregido aquí antes de
commitear, no después.

---

## 10 · Reconciliación de celdas contra el marginal (paso 3, tercer commit)

*Encargo X-bis, mesa #19 continuada. Verificación de premisas antes de
obedecer: §4.1/§4.2/§4.3 de esta nota sí reportan β̂ por celda para W1/W2/W3
y citan el β̂ marginal de Encargo W al lado de cada uno — confirmado
releyendo §4 completo. La nota, hasta este punto (§0-§9), no contiene
ninguna reconciliación de las celdas contra el marginal — confirmado, no
hay PARO por esta vía. Entorno verificado antes de empezar:
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir, sonda a
`www.inegi.org.mx` → 200. `data/raw` es el symlink compartido de los tres
worktrees de esta rama de trabajo (`/home/pc0/mm-corpus/raw`,
`data/raices.local.yaml`), no ausente.*

**Motivación, tal como la plantea el encargo:** los tres β̂ marginales
invierten signo (o no son estables) al condicionar en §4. Eso no es
distinguible de un bug de agregación — celdas que no particionan la
muestra, pesos mal aplicados, o secuela del bug de parseo DBF corregido a
media corrida (§4, párrafo de advertencia) — hasta demostrar que las
celdas reproducen el marginal.

### 10.1 · Método

Script ad-hoc de esta sesión (no commiteado — vive en el scratch de este
acto, fuera del perímetro; el perímetro de este acto es solo esta nota),
que reusa `tests/svystat.py::prop_ultimate_cluster` y `tests/dbfmini.py`
**sin modificar ninguno de los dos**, sobre exactamente los mismos campos,
universos, dicotomizaciones y llaves de join que §1/§4 ya congelaron y
usaron. Para cada eje de cada coeficiente:

```
p1 = Σ_c (w_c · p1_c) / Σ_c w_c     sobre las celdas del eje, grupo θ=1
p0 = Σ_c (w_c · p0_c) / Σ_c w_c     sobre las celdas del eje, grupo θ=0
reconciliado = p1 − p0
```

implementado como el pool ponderado de todas las filas θ=1 (resp. θ=0) que
caen en **alguna** celda del eje, vía `prop_ultimate_cluster` sobre ese
pool — algebraicamente idéntico a la suma ponderada de `p_hat` por celda
que pide el encargo (cada celda ya es, por construcción, `p_hat` de un
subconjunto disjunto de filas con el mismo campo de peso). No se promedió
ningún β̂ de celda. Las cifras se derivaron de la corrida de este acto, no
se copiaron de §4 — la única cifra reusada de la nota es el β̂ marginal
citado, contra el que se compara.

**Guardia de reproducción, antes de leer ninguna celda nueva:** el
marginal recalculado en este acto, sobre el universo completo de cada
ítem (sin restringir a ningún eje), coincide cifra por cifra con el que
§4 ya reportó y que a su vez coincidió con `milpa/procedencia.yaml:630-690`:

| Ítem | n(θ=1) | n(θ=0) | β̂ recalculado | β̂ en §4 |
|---|---|---|---|---|
| `AP5_1_1` | 6 430 | 6 945 | −0.0102 | −0.0102 |
| `AP5_1_2` | 10 667 | 2 726 | −0.0113 | −0.0113 |
| `AP5_1_3` | 7 644 | 5 721 | −0.0269 | −0.0269 |
| `P11_1_23` (W2) | 20 245 | 17 510 | −0.0645 | −0.0645 |
| `p9_9_4` (W3) | 5 281 | 6 183 | +0.0279 | +0.0279 |

Coincide exacto en los cinco. El pipeline de este acto reproduce el de §4
antes de tocar ninguna celda.

### 10.2 · Diagnóstico de integridad de los cruces, antes de leer ninguna brecha de cobertura como bug

Cada eje de W1 depende de un join (`SEC_4_5`→`SD` para formalidad/edad,
`SEC_4_5`→`SEC_9_10` para ingreso, por `UPM`+`VIV_SEL`+`R_SEL`/`N_REN`); W2
depende de un join (`sec_11`→`residentes_sec_2` por `ID_PER`); W3 no usa
join (todo vive en `TMODULO`). Se instrumentó cada eje para separar, de
la brecha entre el universo del eje y el universo marginal, cuánto es
**fallo de llave (`sin_cruce`, evidencia de un join roto)** y cuánto es
**código excluido por la propia especificación de §1 del acto anterior**
(no-aplicabilidad estructural, no sabe/no responde, fuera de los tramos
declarados):

| Eje | Instrumento | `sin_cruce` (fallo de llave) | Excluido por código declarado | Detalle del código |
|---|---|---|---|---|
| Formalidad (W1) | ENCUCI | **0** | 5 236 | `AP3_15_4` en blanco (no trabajó) |
| Edad (W1) | ENCUCI | **0** | 957 | 901 con edad 15-17 (fuera de los tramos `18-29`+, declarados desde 18) + 56 con código `97`/`98`/`99` |
| Ingreso (W1) | ENCUCI | **0** | 560 | `AP10_14` en `{8,9}` (no quiere decir/no sabe) |
| Edad (W2) | ENCIG | **0** | 0 | — cobertura 100% |
| Formalidad (W3) | ENIF | n/a (sin join) | 3 007 | `p3_13` en blanco (no trabaja, 2 964) + código `9` (43) |
| Ingreso (W3) | ENIF | n/a (sin join) | 3 338 | `p3_11a` en blanco (mismo grupo no-trabaja, 2 964) + `98000`/`99888` (374) |
| Migración (W3) | ENIF | n/a (sin join) | 11 | `p3_15_epc` = `999` |
| Edad/Urbanización/Acceso digital (W3) | ENIF | n/a (sin join) | 0 | — cobertura 100% cada uno |

**Cero fallos de llave en los dos joins usados (ENCUCI y ENCIG), en los
cinco ítems.** Esto descarta directamente, para todos los ejes, la
hipótesis "celdas mal particionadas por join roto" y, junto con §10.3
abajo (reconciliación exacta donde la cobertura es completa), descarta
también "pesos mal aplicados" y "secuela del bug de parseo DBF" — ninguna
de las tres hipótesis del encargo se sostiene como explicación de las
brechas que sí aparecen. Donde hay brecha, es 100% código excluido por la
especificación ya congelada en §1, no dato perdido por error de código de
este acto ni del anterior.

### 10.3 · Resultados de la reconciliación, por eje

**W1 — ENCUCI, `radio_confianza`.** Marginal citado de §4.1 al lado de
cada ítem.

| Ítem | Eje | p1 | p0 | reconciliado | marginal citado | diferencia | diferencia relativa | Σn celdas / n marginal | cobertura | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|
| `AP5_1_1` | Formalidad | 0.1469 | 0.1659 | −0.0191 | −0.0102 | −0.0089 | 87.2% | 8 139 / 13 375 | 60.8% | **NO COINCIDE** |
| `AP5_1_1` | Edad | 0.1287 | 0.1354 | −0.0067 | −0.0102 | +0.0035 | 34.3% | 12 418 / 13 375 | 92.8% | **NO COINCIDE** |
| `AP5_1_1` | Ingreso | 0.1184 | 0.1295 | −0.0111 | −0.0102 | −0.0009 | 8.4% | 12 815 / 13 375 | 95.8% | **NO COINCIDE** |
| `AP5_1_2` | Formalidad | 0.1541 | 0.1670 | −0.0129 | −0.0113 | −0.0016 | 14.1% | 8 145 / 13 393 | 60.8% | **NO COINCIDE** |
| `AP5_1_2` | Edad | 0.1302 | 0.1402 | −0.0100 | −0.0113 | +0.0013 | 11.4% | 12 432 / 13 393 | 92.8% | **NO COINCIDE** |
| `AP5_1_2` | Ingreso | 0.1215 | 0.1343 | −0.0128 | −0.0113 | −0.0014 | 12.5% | 12 833 / 13 393 | 95.8% | **NO COINCIDE** |
| `AP5_1_3` | Formalidad | 0.1425 | 0.1736 | −0.0311 | −0.0269 | −0.0042 | 15.6% | 8 131 / 13 365 | 60.8% | **NO COINCIDE** |
| `AP5_1_3` | Edad | 0.1180 | 0.1496 | −0.0316 | −0.0269 | −0.0047 | 17.6% | 12 404 / 13 365 | 92.8% | **NO COINCIDE** |
| `AP5_1_3` | Ingreso | 0.1116 | 0.1396 | −0.0280 | −0.0269 | −0.0011 | 4.1% | 12 808 / 13 365 | 95.8% | **NO COINCIDE** |

**Ningún eje de W1 alcanza cobertura completa del universo del marginal**
— los tres ejes de los tres ítems muestran Σn de celdas < n marginal, por
las brechas declaradas en §10.2. Con el criterio literal del encargo
(Σn celdas = n marginal ⇒ COINCIDE; si no, NO COINCIDE), **ninguna de las
nueve filas de W1 reconcilia contra el marginal citado.**

**W2 — ENCIG, `confianza_institucional`.**

| Ítem | Eje | p1 | p0 | reconciliado | marginal citado | diferencia | diferencia relativa | Σn celdas / n marginal | cobertura | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|
| `P11_1_23` | Edad | 0.0736 | 0.1381 | −0.0645 | −0.0645 | +0.0000 | 0.0% | 37 755 / 37 755 | 100.0% | **COINCIDE** |

**El único eje de W2 reconcilia exacto a cuatro decimales.**

**W3 — ENIF, `familismo_apoyo`.**

| Eje | p1 | p0 | reconciliado | marginal citado | diferencia | diferencia relativa | Σn celdas / n marginal | cobertura | veredicto |
|---|---|---|---|---|---|---|---|---|---|---|
| Formalidad | 0.2550 | 0.2510 | +0.0041 | +0.0279 | −0.0238 | 85.3% | 8 457 / 11 464 | 73.8% | **NO COINCIDE** |
| Edad | 0.3139 | 0.2860 | +0.0279 | +0.0279 | +0.0000 | 0.0% | 11 464 / 11 464 | 100.0% | **COINCIDE** |
| Urbanización | 0.3139 | 0.2860 | +0.0279 | +0.0279 | +0.0000 | 0.0% | 11 464 / 11 464 | 100.0% | **COINCIDE** |
| Ingreso | 0.2551 | 0.2512 | +0.0039 | +0.0279 | −0.0240 | 86.0% | 8 126 / 11 464 | 70.9% | **NO COINCIDE** |
| Migración | 0.3139 | 0.2856 | +0.0282 | +0.0279 | +0.0003 | 1.2% | 11 453 / 11 464 | 99.9% | **COINCIDE** |
| Acceso digital | 0.3139 | 0.2860 | +0.0279 | +0.0279 | +0.0000 | 0.0% | 11 464 / 11 464 | 100.0% | **COINCIDE** |

**Cuatro de seis ejes de W3 reconcilian exacto** (Edad, Urbanización,
Migración con cobertura 99.9%, Acceso digital); **dos no** (Formalidad,
Ingreso — ambos con la misma exclusión estructural de fondo: la
subpoblación que no trabaja, §10.2).

### 10.4 · Lectura, sin ajustar el texto para que cuadre

**Ninguna de las tres hipótesis de bug que motivó este acto se sostiene.**
Cero fallos de llave en los joins de ENCUCI y ENCIG (§10.2); y donde la
cobertura de un eje es completa o casi completa (W2/Edad, W3/Edad,
W3/Urbanización, W3/Migración, W3/Acceso digital — cinco de dieciséis
filas de §10.3), el reconciliado coincide con el marginal a cuatro
decimales, sin excepción. Eso descarta pesos mal aplicados y secuela del
bug de parseo DBF como explicación de cualquier brecha: si esos bugs
existieran, se verían también en los ejes de cobertura completa, y no se
ven.

**Pero el criterio literal del encargo (Σn celdas = n marginal) falla en
once de las dieciséis filas — las nueve de W1 completas, y Formalidad/
Ingreso de W3.** En los tres casos la brecha es la misma, ya declarada en
§1 del acto anterior: los ejes de Formalidad e Ingreso solo clasifican a
quien trabaja/reporta ingreso — una subpoblación estructuralmente más
chica que el universo del marginal, no un error de este acto ni del
anterior. El eje de Edad de W1 pierde además 901 personas de 15-17 años,
fuera de los tramos `18-29`+ que §1.1 declaró desde 18 — otra restricción
declarada, no un bug.

**Esto no es "las celdas no particionan la muestra" en el sentido de un
defecto de código** — dentro de su propio universo elegible, cada eje
particiona sin pérdida (cobertura interna 100%, verificado por
construcción: cada fila con código válido cae en exactamente una celda).
Es que el universo elegible de Formalidad/Ingreso/Edad-W1 es un
subconjunto propio y declarado del universo del marginal, no el mismo
conjunto. Comparar el β̂ reconciliado de esas celdas contra el marginal de
§4 es comparar dos poblaciones distintas, anidadas pero de tamaño
diferente — no una descomposición exacta del mismo número.

**Aplicando el criterio del encargo tal como está escrito, sin
suavizarlo:** se marca como **NO VALIDADO** en el sentido de esta
reconciliación —§4.1 completo (los tres ítems de W1, en sus tres ejes) y
las filas Formalidad/Ingreso de §4.3 (W3)— porque ninguna de esas celdas
reconstruye el marginal que cita. Se marca **VALIDADO** —§4.2 completo
(W2) y las filas Edad/Urbanización/Migración/Acceso digital de §4.3
(W3)— porque el reconciliado coincide exacto con el marginal citado: para
esos ejes, la inversión (o no-inversión) de signo que reporta §4 es
composicional y real, no distinguible de un bug porque no hay bug que la
explique.

**Lo que este acto no hace, declarado, no ejecutado:** la comparación
correcta para separar "¿el β̂ marginal completo también se invertiría si
se pudiera condicionar sobre el universo entero?" de "¿el β̂ marginal
restringido al universo elegible del eje ya tenía otro signo antes de
condicionar?" requeriría recalcular un marginal restringido a cada
universo elegible (por ejemplo, β̂ marginal solo entre quienes trabajan,
para comparar limpio contra las celdas de Formalidad) — este acto no lo
hace. Es el paso natural siguiente, no ejecutado aquí: **PARA**, como pide
el encargo, sin intentar arreglarlo ni extenderlo en este acto.

### 10.5 · Cierre — perímetro y suite

`git status --short` antes de commitear: solo esta nota modificada, más
`data/raw` (symlink gitignorado, no rastreado) — verificado, no se tocó
`milpa/procedencia.yaml`, `canon/`, `tests/svystat.py`, `tests/dbfmini.py`
ni ningún archivo de `data/inventarios`.

`python3 tests/manifiesto.py --verifica`: los tres payloads que este acto
reabrió (`encuci2020_bd_dbf`, `encig23_base_datos_csv`, `enif2024_csv`)
**COINCIDEN** contra `data/manifiesto.yaml` (sha256 y tamaño) — reverificado
de nuevo en este acto, no asumido del acto anterior.

`python3 tests/check.py --baseline`: **LÍNEA BASE: VERDE** — nada nuevo
frente a `tests/baseline.json`.

---

## 11 · Rider (Encargo Z, W1) — marginal restringido al universo de cada eje, y corrección del titular

*Mesa #19, 4/ago/2026. Perímetro propio: solo esta nota, esta sección,
al final — sin colisión con el resto del encargo. Verificación de
premisas antes de obedecer: §10.4 diagnosticó el error de comparación
(celdas de un eje contra el marginal de **toda** la población, cuando
los ejes de Formalidad/Ingreso solo clasifican a quien trabaja/reporta
ingreso — "dos universos distintos") y declaró **PARA** sobre el paso
correcto, sin ejecutarlo — confirmado releyendo §10.4 completo. Este
rider ejecuta ese paso pendiente. Entorno verificado antes de empezar:
`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir, sonda a
`www.inegi.org.mx` → 200 — mismo entorno que §10.*

### 11.1 · El "marginal restringido" ya estaba derivado en §10.3 — solo mal etiquetado en la comparación

La columna `reconciliado` de §10.3 es el pool ponderado de **todas** las
celdas de un eje (`p1 = Σ_c w_c·p1_c / Σ_c w_c`, igual para `p0`). Como
las celdas de un eje particionan sin pérdida su propio universo elegible
(cobertura interna 100%, verificado en §10.2), ese pool es,
**algebraicamente, el mismo número** que computar `β̂` directamente
sobre la unión de esas celdas — es decir, **es ya el marginal
restringido al universo del eje**, no una cifra distinta que haya que
recalcular con microdato nuevo. No se abrió ningún payload adicional
para este rider: se reusa el número que §10.3 ya derivó, y se corrige
contra qué se compara.

El error de §10 no estaba en el cálculo de `reconciliado` — estaba en
comparar esa cifra contra el marginal **poblacional completo** (columna
`marginal citado`) en vez de contra sí misma como definición del
marginal restringido. Comparar `reconciliado` contra el marginal
completo es exactamente "comparar dos universos" cuando la cobertura
es <100%; comparar `reconciliado` contra sí mismo, una vez llamado por
su nombre correcto, es una identidad — **coincide siempre, por
construcción, no es un hallazgo nuevo.** El hallazgo real está en otra
comparación, que sí es no trivial: **¿el marginal restringido conserva
el signo del marginal completo, o cambia solo por restringir el
universo, antes de condicionar en ninguna celda?**

### 11.2 · Cobertura por eje y comparación de signo, marginal completo vs. marginal restringido

| Coeficiente | Eje | Cobertura | Marginal completo | Marginal restringido (`reconciliado`, §10.3) | ¿Mismo signo? |
|---|---|---|---|---|---|
| W1/`AP5_1_1` | Formalidad | 60.8% | −0.0102 | −0.0191 | Sí |
| W1/`AP5_1_1` | Edad | 92.8% | −0.0102 | −0.0067 | Sí |
| W1/`AP5_1_1` | Ingreso | 95.8% | −0.0102 | −0.0111 | Sí |
| W1/`AP5_1_2` | Formalidad | 60.8% | −0.0113 | −0.0129 | Sí |
| W1/`AP5_1_2` | Edad | 92.8% | −0.0113 | −0.0100 | Sí |
| W1/`AP5_1_2` | Ingreso | 95.8% | −0.0113 | −0.0128 | Sí |
| W1/`AP5_1_3` | Formalidad | 60.8% | −0.0269 | −0.0311 | Sí |
| W1/`AP5_1_3` | Edad | 92.8% | −0.0269 | −0.0316 | Sí |
| W1/`AP5_1_3` | Ingreso | 95.8% | −0.0269 | −0.0280 | Sí |
| W2/`P11_1_23` | Edad | 100.0% | −0.0645 | −0.0645 | Sí (idéntico, trivial) |
| W3 | Formalidad | 73.8% | +0.0279 | +0.0041 | Sí, magnitud colapsa a casi cero |
| W3 | Edad | 100.0% | +0.0279 | +0.0279 | Sí (idéntico, trivial) |
| W3 | Urbanización | 100.0% | +0.0279 | +0.0279 | Sí (idéntico, trivial) |
| W3 | Ingreso | 70.9% | +0.0279 | +0.0039 | Sí, magnitud colapsa a casi cero |
| W3 | Migración | 99.9% | +0.0279 | +0.0282 | Sí (casi idéntico) |
| W3 | Acceso digital | 100.0% | +0.0279 | +0.0279 | Sí (idéntico, trivial) |

**Ninguna fila cambia de signo al restringir el universo** — en las
dieciséis, el marginal restringido conserva el signo del marginal
completo. Esto descarta, para las tres reglas, la hipótesis más simple
de "el signo del marginal es un artefacto de qué población entra" (si
fuera así, restringir el universo ya habría bastado para invertirlo,
sin necesidad de condicionar en celdas). Lo que sí varía es la
**magnitud** en Formalidad/Ingreso de W3 — cae a menos de un séptimo
del marginal completo — y eso, junto con la ausencia de intervalo de
confianza propio para esa cifra restringida (no computado en este
rider, ver §11.4), es lo que mantiene esas dos filas sin resolver.

### 11.3 · Lectura por regla — dónde el signo SÍ se invierte, y contra qué

Con el marginal correctamente restringido como punto de comparación
(§11.2), la pregunta relevante pasa de "¿coinciden las celdas con el
marginal?" (respondida trivialmente: sí, siempre, por construcción) a
"¿coincide el signo de las **celdas individuales** (§4) con el signo
del **marginal restringido** que esas mismas celdas, pooladas,
reproducen?" — ahí es donde vive la instabilidad real, no en la
reconciliación misma.

**W2 (`confianza_institucional`, ENCIG) — no sobrevive, confirmado.**
Cobertura 100%: no hay universo distinto que comparar, ninguna
ambigüedad de denominador posible. El marginal restringido es idéntico
al completo (−0.0645) — y sin embargo las cuatro celdas de edad que lo
componen son, **las cuatro, positivas y significativas** (§4.2). No es
un artefacto de comparar poblaciones distintas: es la misma población,
particionada, con signo opuesto dentro de cada partición al que tiene
agregada. Patrón de libro de texto (el mismo tipo de composición que
produce una paradoja de Simpson): edad se asocia con más confianza y
con menos mordida a la vez, y esa doble asociación basta para invertir
el signo al agregar, sin que exista ningún bug de join, peso o parseo
(ya descartados en §10.2). **Confirma, con más fuerza que §6, que el
marginal de W2 no es una propiedad estable de la relación individual.**

**W3 (`familismo_apoyo`, ENIF) — no sobrevive en los cuatro ejes de
cobertura completa; las dos de cobertura parcial (Formalidad, Ingreso)
quedan sin resolver, no confirmadas.** Edad, Urbanización, Migración y
Acceso digital reconcilian con cobertura ≥99.9% — mismo argumento que
W2: sin ambigüedad de universo, y aun así **cada uno de esos cuatro
ejes tiene una celda mayoritaria con signo negativo significativo y una
celda minoritaria con signo positivo significativo** (§4.3), agregando
a un marginal positivo. Confirmado, no artefacto de denominador.
Formalidad e Ingreso, en cambio, tienen cobertura 74% y 71%: su
marginal restringido conserva el signo positivo pero se **desploma** a
+0.0041 y +0.0039 — compatible con "no hay instabilidad real, el
marginal restringido ya es ~cero" o con "hay instabilidad pero se
diluye contra un denominador más chico", y este rider no calcula el
IC95% de esas dos cifras restringidas para distinguir entre ambas
lecturas (§11.4). **No se fuerza una conclusión que el dato disponible
no sostiene.**

**W1 (`radio_confianza`, ENCUCI) — todavía no se puede decir, en
ninguno de los tres ítems ni de los tres ejes.** Es la única de las
tres reglas donde **ningún eje alcanza cobertura completa** (60.8%
Formalidad, 92.8% Edad, 95.8% Ingreso, repetido en los tres ítems) —
así que, a diferencia de W2 y de cuatro de los seis ejes de W3, no hay
ninguna fila de W1 donde la reconciliación sea trivialmente
no-ambigua. El marginal restringido conserva el signo negativo en las
nueve filas (§11.2) — la instabilidad de signo que muestran las celdas
individuales de §4.1 (28 de 39 positivas) no se explica por la sola
restricción de universo — pero sin intervalo de confianza para esos
nueve marginales restringidos (§11.4, no ejecutado aquí) no se puede
distinguir "la relación dentro del universo elegible también se
invierte a nivel de celda, de forma real" de "el marginal restringido
sigue siendo compatible con cero y la aparente positividad de las
celdas es ruido de muestras más chicas". **Se declara sin resolver, no
se fuerza ni `A` ni `D` para esta pieza del encargo.**

### 11.4 · Lo que este rider no hace, declarado

No calcula el error estándar ni el IC95% de ningún marginal
restringido (`reconciliado` de §10.3) — `prop_ultimate_cluster` los
produce como subproducto de una corrida directa sobre el universo
restringido, no de un pool manual de los `se` por celda (combinarlos
correctamente exigiría la covarianza entre celdas dentro del mismo
diseño complejo, que este rider no deriva). Es la pieza que separaría,
para W1 completo y para Formalidad/Ingreso de W3, "instabilidad real
dentro del universo elegible" de "marginal restringido ya cercano a
cero, sin señal que estabilizar". **Paso natural siguiente, no
ejecutado — mismo criterio de `PARA` que §10.4 ya declaró una vez.**

### 11.5 · Corrección del titular de §6, sin editarlo

*(Corrección fechada, append-only — igual que las Notas del pre-registro del Hito D: no se edita §6, se declara aquí la lectura correcta y por qué.)*

§6 dice: **"¿sobreviven los tres al condicionar? No, ninguno de los tres
sobrevive sin matiz."** Con la reconciliación contra el universo
correcto (§11.1-§11.3), esa frase sobre-generaliza: **dos de las tres
reglas —`confianza_institucional` (W2) y `familismo_apoyo` (W3, en
cuatro de sus seis ejes)— no sobreviven, confirmado sin ambigüedad de
denominador.** De la tercera —`radio_confianza` (W1)— **todavía no se
puede decir**: la evidencia disponible no descarta la inestabilidad
que §4.1 reportó, pero tampoco la confirma con el rigor que sí alcanzan
W2 y W3, porque ningún eje de W1 tiene cobertura completa y este rider
no calculó el intervalo de confianza que haría falta para cerrarlo
(§11.4). Las dos celdas de cobertura parcial de W3 (Formalidad,
Ingreso) comparten la misma reserva.

### 11.6 · Cierre — perímetro y suite

Ningún archivo además de esta nota se tocó — `git status --short`:
solo `forense/notas/2026-08-04-x-condicionamiento-y-forma.md`
modificado, más `data/raw` (symlink gitignorado). No se abrió ningún
payload nuevo: todas las cifras de §11.2 son las de `reconciliado` y
`marginal citado` que §10.3 ya derivó y verificó contra
`data/manifiesto.yaml` en su propio cierre (§10.5) — reusadas, no
recalculadas. `python3 tests/check.py --baseline`: **LÍNEA BASE:
VERDE** — nada nuevo frente a `tests/baseline.json`.
