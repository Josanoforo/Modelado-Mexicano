# CAL-CONF Fase B, posiciones 5 y 6 — mide `radio_confianza` (ENCUCI) y `familismo_apoyo` (ENIF)

*3 de agosto de 2026.*

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta
sesión (diccionarios de datos, catálogos, cuestionario, microdato,
`data/manifiesto.yaml`, historial git). El encargo que origina esta sesión
es tipo (3) hasta contrastarlo — ver §0. No se abre microdato nuevo:
`encuci2020_bd_dbf` (Fase B ola 1/2) y `enif2024_csv` (Fase B ola 1) ya
estaban abiertos antes de esta sesión — sin contaminación nueva que
declarar.

**Entorno.** `data/raw` no existe por defecto en un worktree nuevo (está en
`.gitignore`, igual que `data/raices.local.yaml`) — se recreó el symlink a
mano (`data/raw -> /home/pc0/mm-corpus/raw`) y se copió
`raices.local.yaml` desde `/home/pc0/Modelado-Mexicano` antes de empezar.
Sin esto, `tests/manifiesto.py --verifica` habría reportado AUSENTE para
todo, no porque falte el payload sino porque el entorno no monta la raíz —
la misma advertencia que dejó `§14.6` de `hitoE`.

---

## 0 · Verificación de premisas antes de obedecer

**Premisa del encargo:** *"la posición 4 (`exposicion_violencia`, ENVIPE) ya
fusionó y el contador dice 7 de 14 en la nota de esa sesión."*

**Verificación, no aceptación.** `git fetch origin` + `git log --oneline
origin/main` confirma que `PR #57` está fusionado (`2a218a1`, mergeado
2026-08-03T21:13:45Z) — la primera mitad de la premisa se sostiene: la
posición 4 sí fusionó, y su commit inicial (`d936a9b`) sí llevaba el rótulo
"(7 de 14)" en el título.

**La segunda mitad no se sostiene.** El mismo `PR #57` se autocorrigió el
mismo día, antes de fusionar (`8ea94c3`, *"Corrige rótulo del PR #57:
BP1_20/23/28 no miden exposicion_violencia"*), y `forense/hitoE-campana-
medicion-v2_0.md` §15 (adenda 04/ago/2026, ya mergeada, leída completa en
esta sesión) documenta por qué: la sesión que ejecutó la posición 4
verificó `BP1_20`/`BP1_23`/`BP1_28` contra `fd_envipe2025.pdf` y encontró
que el trío **no mide** `exposicion_violencia` — mide conducta de denuncia
condicionada por construcción a ya haber sido víctima (`TMod_Vic` es la
subpoblación de víctimas al 100%). Cita literal de `§15`: *"el contador no
se movió (`PR #57` lo corrigió de vuelta a 6/14)"*, y `§15.1`: *"No se
movió ningún contador (sigue en 6/14, `PR #57`)"*. `forense/hallazgos.md`,
entrada 2026-08-04, lo confirma con el mismo número: *"el contador vuelve a
**6 de 14**, sin cambio"*. `canon/modelo-decision-v4_0.md:275,619,723`
(este checkout, post-merge de `PR #57`) sigue mostrando **"~~3~~ 6 de 14"**
— nunca se propagó un 7.

⚠️ La fila 4 de la tabla `§14.3`, tal como quedó tras la adenda, conserva en
su columna "Qué mueve" el texto **"Contador → 7/14, sin cambio de
destino"** — la adenda declara explícitamente que esa columna **no se
edita** (solo se marca vencida la columna "Fuente · variable"), así que ese
`7/14` es texto histórico congelado, no el estado actual. El estado actual
es el que dicen la prosa de `§15`/`§15.1`, `forense/hallazgos.md` y
`canon` — los tres coinciden en **6/14**, y son las tres fuentes que
efectivamente se movieron después de la autocorrección.

**Veredicto: la premisa del encargo no se sostiene.** Contador real, previo
a esta sesión: **6 de 14**, no 7. Instrucción del encargo aplicada
literalmente (*"no bloquea la medición — mide igual y declara en tu nota el
contador que corresponda al estado real que verifiques"*): esta sesión mide
igual, y parte de 6, no de 7, en su §5. Ningún "8" ni "9" se tecleó por
instrucción del encargo — ver §5 para la aritmética.

---

## 1 · Especificación de la medición — congelada antes de calcular

*Misma regla que las olas anteriores: nada de lo que sigue se toca después
de ver una tabla de resultados (`canon` §1.1.B, propiedad 3).*

### 1.0 Chequeo C3, hecho antes de congelar la especificación — para los dos reactivos

C3 (`P2` §2.b) exige variables distintas entre el reactivo que identifica
un coeficiente (C1) y el desenlace que lo verifica (C2); si son la misma
variable, la identificación es circular. Se verificó contra
`forense/notas/2026-08-01-p2-momentos-atributos.md` §2.d y contra
`forense/notas/2026-07-31-inventario-segmentacion.md` (la fuente de Tabla B
que `§14.3` cita como `inventario l.264`/`l.171`) para **ambos** generadores
que tocan cada reactivo, no solo el que nombra la cola:

- **`radio_confianza` (ENCUCI `AP5_1_1/2/3`).** Para `G1·radio_confianza`
  (la fila que `§14.3` posición 5 cita): C1 = `AP5_1_1/2/3`, C2 = desenlace
  `tramite.mordida.discrecional` (`AP5_17`/`AP5_18`) — **variables
  distintas, C3 pasa limpio**. Pero `inventario:264` es también la fila de
  Tabla B para la regla `cooperacion.confianza.puente_personal`
  (`canon/modelo-decision-v4_0.md:496`, generador **G1**, la misma malla),
  cuyo desenlace observado **es** `AP5_1_2` — el propio reactivo. `P2`
  §2.d lo marca explícito: *"⚠️ no usar `cooperacion.confianza.puente_
  personal` como desenlace: su variable observada es `AP5_1_2`, el propio
  reactivo — sería circular"*. **Se mide igual — compra la condicional. No
  se usa (aquí ni después) para identificar `cooperacion.confianza.puente_
  personal`.**
- **`familismo_apoyo` (ENIF `P9_9_1..6`).** Para `G3·familismo_apoyo` (la
  fila que `§14.3` posición 6 cita): C1 = `P9_9_4` (`P2` cita el ítem
  puntual, no la batería completa — ver §1.2 abajo), C2 = desenlace
  `dinero.ahorro.volatilidad_horizonte_corto` (`P4_10`) — **variables
  distintas, C3 pasa limpio para G3**. Pero para **`G5·familismo_apoyo`**
  (mismo constructo, generador distinto), `P2` §2.d lo marca **FALLA**:
  *"el reactivo (ENIF `P9_9_*`) y el desenlace G5 en ENIF
  (`familia.seguro.volatilidad_ausencia_estado`, `Sí`) son la misma
  variable — Tabla B `l.171` observa esa regla precisamente con
  `P9_9_1..6`. Falla C3."* — y `inventario:171` es, verificado aquí letra
  por letra, exactamente esa fila (`canon/modelo-decision-v4_0.md:465`
  confirma el id). **Se mide igual — compra la condicional, no el
  coeficiente: el número que sale de esta sesión no puede usarse para
  identificar `G5·familismo_apoyo`** (sí puede seguir usándose para
  `G3·familismo_apoyo`, donde C3 no falla).

### 1.1 Radio_confianza — ENCUCI `AP5_1_1` (mayoría de las personas) · `AP5_1_2` (personas que conoce) · `AP5_1_3` (vecinos de su colonia/localidad)

- **Instrumento:** tabla `ENCUCI_2020_SEC_4_5` — reactivo, `FAC_SEL`,
  `DOMINIO`, `UPM_DIS`/`EST_DIS` viven en el mismo registro; `EDAD` y
  `AP3_15_4` (formalidad) requieren join a `ENCUCI_2020_SD` por
  `UPM+VIV_SEL+R_SEL=N_REN` — **mismo join que educación/electoral en las
  olas anteriores**, reutilizado y re-verificado en esta sesión (ver §2,
  reproduce exactamente `n=21519`/`no_respuesta=1483`/`sin_cruce=1265`/
  `útiles=18771` antes de tocar `AP5_1_*`).
- **Pregunta, verificada contra `FD_ENCUCI2020.pdf` p.21 (cons. 68-70,
  Sección V):** *"5.1 En una escala de cero a diez, como en la escuela,
  donde cero es nada y diez es completamente, en general ¿cuánto confía
  en…"* — 1. la mayoría de las personas (`AP5_1_1`) · 2. la mayoría de las
  personas que conoce personalmente (`AP5_1_2`) · 3. la mayoría de las
  personas que viven en su colonia y localidad (`AP5_1_3`). `AP5_1_4`
  (servidores públicos) existe en el mismo bloque pero **no** lo pide el
  encargo — no se mide aquí.
- **Universo efectivo, verificado contra FD y contra la distribución cruda
  de los tres campos (21 519 filas, cero blancos en los tres):** **completo
  — se pregunta a todo entrevistado, sin filtro de identificación previo**.
  A diferencia de `AP5_4_XX` de ENVIPE (ola 2) o de `TMod_Vic` de ENVIPE
  (posición 4), aquí no hay no-aplicabilidad estructural que declarar: los
  únicos códigos observados son `00`-`10` y `99` (No sabe/no responde).
  Dicho con las palabras que pide el encargo: **el universo es completo.**
- **Escala y recodificación, declarada:** ordinal 0-10, `99` = no sabe/no
  responde (excluido, no imputado). **Dicotomización:** confía = `{6..10}`
  (aprobatorio), no confía = `{0..5}` (no aprobatorio) — corte tomado del
  propio enunciado de la pregunta (*"como en la escuela"*, y en el sistema
  de calificación de la SEP 6 es la calificación mínima aprobatoria), no
  derivado de la distribución de los datos. Es la traducción de "mismo
  corte de punto medio" que las olas anteriores aplicaron a escalas
  ordinales de 4 puntos, adaptada a una escala de 11 puntos con ancla
  externa declarada, no inventada aquí para que cuadre.
- **Los tres ítems se miden por separado, no como índice** — mismo
  criterio que ola 2 aplicó a `confianza_institucional` por institución:
  son tres referentes distintos (desconocidos en general / conocidos
  personalmente / vecinos), no repeticiones del mismo escenario
  hipotético — promediarlos asumiría una unidimensionalidad de "radio de
  confianza" entre círculos sociales que nadie verificó.
- **Condicionante primario (conjunto):** formalidad (`AP3_15_4`) × edad
  (tramos 18-29/30-44/45-59/60+, mismos de siempre) — mismo eje que
  educación/electoral en las olas anteriores, mismo instrumento, misma
  tabla, mismo join.
- **Marginal:** `DOMINIO` (Urbano/Complemento urbano/Rural).
- **Ponderador:** `FAC_SEL` — verificado por orden de magnitud: suma sobre
  las 21 519 filas de `SEC_4_5` = 96 427 583, idéntico al que ola 2 ya
  verificó contra Censo 2020 (población 15+, ~97 millones) — no recalculado
  desde cero, sí reproducido en esta sesión antes de aceptar la cifra.
- **n mínimo por celda: 30 sin ponderar**, igual que siempre. Por debajo:
  SIN SOPORTE.
- **Dispersión:** conglomerado último (`EST_DIS`/`UPM_DIS`), `tests/
  svystat.py`, revalidado en §2.

### 1.2 Familismo_apoyo — ENIF `P9_9_1..6` ("¿con qué piensa cubrir su vejez?")

- **Instrumento:** tabla única `conjunto_de_datos_tmodulo_enif2024` —
  reactivos, `edad_v`, `p3_13`, `tloc`, `est_dis`, `upm_dis`, `fac_per`
  viven en el mismo registro; no hace falta join (mismo instrumento y
  mismas variables de condicionamiento que la primera ola usó para
  financiera).
- **Pregunta, verificada contra el diccionario de datos real
  (`diccionario_datos_tmodulo_enif2024.csv`, filas 334-339) y contra el
  cuestionario (`enif_2024_cuestionario.pdf`):** *"P9.9 En su vejez, ¿piensa
  cubrir sus gastos con lo que reciba de…"* — 1. apoyos del gobierno para
  adultos mayores (`p9_9_1`) · 2. pensión/jubilación/Afore/plan privado
  (`p9_9_2`) · 3. venta o renta de bienes o propiedades (`p9_9_3`) · **4.
  dinero que le dé su esposa(o)/pareja, hijas, hijos u otros familiares
  (`p9_9_4`)** · 5. seguir trabajando (`p9_9_5`) · 6. otro (`p9_9_6`).
  Escala binaria por ítem: `1` Sí / `2` No / `9` No sabe (verificado contra
  `p9_9_1.csv`…`p9_9_6.csv`, catálogos idénticos entre los seis).
- **⚠️ Hallazgo de composición, verificado contra dato real — no un fallo
  tipo posición 4, pero sí una imprecisión que el encargo pide declarar:**
  la propia fila de `inventario:171` que originó esta posición ya lo decía
  ("piensa cubrir su vejez con: gobierno/pensión/venta de bienes/**familia**
  /trabajo/otro"), y esta sesión lo confirma contra el diccionario: **de
  los seis ítems, sólo `p9_9_4` pregunta por dinero de familiares.** Los
  otros cinco (`p9_9_1/2/3/5/6`) son estrategias alternativas de ingreso en
  la vejez —Estado, mercado financiero, venta de activos, trabajo, otro—
  que **no son `familismo_apoyo`**; son, si acaso, sus competidoras dentro
  del mismo menú de opción múltiple. Esto es distinto del fallo de la
  posición 4 (ahí **ninguno** de los tres ítems medía el constructo); aquí
  **uno de seis sí lo mide directamente** (`p9_9_4`, el mismo C1 puntual
  que `P2` §2.d cita para `G3·familismo_apoyo`, no la batería completa). La
  razón por la que `inventario:171`/`§14.3` fila 6 citan los seis juntos es
  que Tabla B registra la fila completa como una sola celda de "Sí" para
  `familia.seguro.volatilidad_ausencia_estado` — no porque los seis midan
  lo mismo. **Se miden los seis por separado** (§1.0 y precedente de ola
  2: reactivos con referente distinto no se promedian en índice), marcando
  explícitamente cuál es el que opera `familismo_apoyo` y reportando los
  otros cinco como contexto del mismo menú — no como parte del constructo.
- **Universo efectivo — verificado contra dato real, filtro estructural
  encontrado y confirmado, no supuesto:** las seis columnas tienen
  exactamente **1 123 blancos cada una, en las mismas 1 123 filas** (de
  13 502). Cruce contra `filtro_s9_1` (*"¿Tiene 71 años o más?"*,
  diccionario fila 333, justo antes de `P9.9.1` en el cuestionario):
  cruce **perfecto, cero excepciones** — `filtro_s9_1=1` (71+) → 100%
  blanco en las seis columnas (1 123 de 1 123); `filtro_s9_1=2` (<71) →
  100% código válido (12 379 de 12 379). Es la misma figura que ola 2
  encontró en `AP5_4_XX` de ENVIPE y que la posición 4 encontró en
  `TMod_Vic`: **no-aplicabilidad estructural por diseño del cuestionario**
  (quien ya tiene 71+ años no recibe una pregunta prospectiva sobre "su
  vejez" — el cuestionario salta a la Sección 10), **blanco ≠
  no-respuesta**. **Universo efectivo declarado: `filtro_s9_1=2`, n=12 379
  (91.7% de `TMODULO`)** — no las 13 502 filas completas. `9` (No sabe)
  dentro de ese universo sí es no-respuesta genuina y se excluye aparte.
- **Condicionante primario (conjunto):** formalidad (`p3_13`: `1`-`6` =
  Formal, `7` = Informal, blanco/`9` excluidos — misma recodificación que
  la primera ola declaró para financiera, mismo instrumento) × edad
  (`edad_v`, mismos tramos).
- **Marginal:** `tloc` (tamaño de localidad, mismo esquema que `tam_loc` de
  ENIGH: 100k+ / 15k-99,999 / 2,500-14,999 / <2,500).
- **No se cruza migración (`p3_15_epc`) ni ingreso (`p3_11a`) en este
  acto** — subconjunto declarado de `x`, no los cinco ejes que la primera
  ola usó para financiera; limitar a formalidad×edad + urbanización
  mantiene el acto comparable a lo que radio_confianza mide en §1.1 sin
  inflar el alcance. Declarado, no derivado después de ver resultados.
- **Ponderador:** `fac_per` — verificado: suma sobre las 13 502 filas de
  `TMODULO` = 94 221 441, idéntico al que la primera ola ya verificó
  (población 18+ de México).
- **n mínimo, dispersión:** idénticos a §1.1.

### 1.3 Lo que esta especificación decide no hacer, declarado

- No se construye índice de `radio_confianza` ni de `familismo_apoyo` —
  cada ítem se mide por separado (§1.0/§1.1/§1.2).
- No se usa el resultado de `familismo_apoyo` para identificar
  `G5·familismo_apoyo` (§1.0, C3 falla ahí) ni el de `radio_confianza` para
  la regla `cooperacion.confianza.puente_personal` (§1.0, mismo motivo).
- No se cruzan migración ni ingreso para `familismo_apoyo` en este acto
  (§1.2).
- No se compara `radio_confianza` contra `familismo_apoyo` ni contra
  ningún componente de `confianza_institucional` ya medido — instrumentos,
  escalas y universos distintos; comparar sería inventar una conjunta no
  medida (mismo límite permanente de `canon` §1.1.C-i que todas las olas
  anteriores citan).
- No se propaga el contador a `milpa/procedencia.yaml` ni a
  `canon/modelo-decision-v4_0.md` — acto de canon aparte (§5).

---

## 2 · El estimador y el pipeline, revalidados en este entorno

**El estimador — revalidado, no heredado.** `tests/svystat.py` no se
modificó desde la ola 2, pero esta sesión lo vuelve a correr contra su caso
conocido en **este** entorno, no asume que sigue validado por haberlo
estado antes:

```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.
```

**El pipeline — revalidado por reproducción de resultados publicados, con
código escrito de nuevo en esta sesión** (`tests/cal_conf_faseb_pos5_6.py`,
no una copia de `cal_conf_faseb_ola2.py`; extrae a un directorio temporal
propio con `tempfile.mkdtemp()`, no hereda la ruta de scratch de otra
sesión como sí hace el script de ola 2 — defecto de portabilidad de ese
script, no repetido aquí):

- **ENCUCI**, join `SEC_4_5`+`SD`, reproduce educación de la primera ola
  antes de tocar `AP5_1_*`: `n_filas=21519 no_respuesta=1483 sin_cruce=1265
  utiles=18771` — coincide exacto con lo publicado en
  `cal-conf-faseb-medicion.md` y ya reproducido una vez por
  `cal_conf_faseb_ola2.py`. Las ocho celdas formalidad×edad también
  coinciden a la décima de punto porcentual.
- **ENIF**, tabla `TMODULO`, reproduce el índice financiero de la primera
  ola antes de tocar `P9_9_*`: `n_filas=13502 sin_indice_valido=3238` —
  coincide exacto con lo publicado. Las ocho celdas formalidad×edad
  también coinciden.

Ambas reproducciones llevan `assert` duro en el script: si el pipeline
diverge, se detiene antes de calcular los reactivos nuevos — mismo patrón
de guardia que introdujo la posición 4.

**Ponderadores, verificados por orden de magnitud contra universo
declarado** (suma de la columna de peso sobre toda la tabla, sin ningún
filtro de esta sesión, calculado aparte del script principal):

| Instrumento | Ponderador | Suma sobre toda la tabla | Universo declarado | ¿Coherente? |
|---|---|---|---|---|
| ENCUCI 2020 | `FAC_SEL` | 96 427 583 | Población 15+ (21 519 filas) | Sí — idéntico al valor que ola 2 ya verificó contra Censo 2020 |
| ENIF 2024 | `fac_per` | 94 221 441 | Población 18+ (13 502 filas) | Sí — idéntico al valor que la primera ola ya verificó |

Comando exacto de la corrida completa: `python3 tests/cal_conf_faseb_pos5_6.py`.

---

## 3 · Resultados

*Todas las tablas: `n` sin ponderar · proporción ponderada · SE por
conglomerado último · IC95%. Ninguna celda de este acto cayó bajo el
mínimo de 30 — la celda más pequeña de todo el acto es `radio_confianza`
Formal×60+ con n=220, muy por encima del mínimo.*

### 3.1 `radio_confianza` — ENCUCI 2020, `SEC_4_5` (universo completo, n=21 519)

**Confía "aprobatorio" (≥6/10) en la mayoría de las personas (`AP5_1_1`).**
No-respuesta (99): 110 · sin cruce edad/formalidad: 1 307 · útiles: 20 102.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 052 | 49.8% | 1.91pp | [46.1%, 53.6%] |
| Formal | 30–44 | 1 876 | 52.2% | 1.58pp | [49.1%, 55.3%] |
| Formal | 45–59 | 1 128 | 54.5% | 2.20pp | [50.1%, 58.8%] |
| Formal | 60+ | 220 | 64.8% | 4.91pp | [55.1%, 74.4%] |
| Informal | 18–29 | 1 914 | 43.6% | 1.64pp | [40.4%, 46.8%] |
| Informal | 30–44 | 2 790 | 41.8% | 1.34pp | [39.1%, 44.4%] |
| Informal | 45–59 | 2 253 | 43.1% | 1.51pp | [40.2%, 46.1%] |
| Informal | 60+ | 1 380 | 44.4% | 1.94pp | [40.6%, 48.2%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 703 | 49.0% | 0.78pp | [47.5%, 50.5%] |
| Complemento urbano | 4 928 | 43.1% | 1.11pp | [40.9%, 45.3%] |
| Rural | 5 471 | 40.3% | 1.14pp | [38.0%, 42.5%] |

**Confía "aprobatorio" en personas que conoce personalmente (`AP5_1_2`).**
No-respuesta: 74 · sin cruce: 1 314 · útiles: 20 131.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 052 | 87.4% | 1.27pp | [84.9%, 89.9%] |
| Formal | 30–44 | 1 876 | 84.1% | 1.14pp | [81.9%, 86.3%] |
| Formal | 45–59 | 1 128 | 83.8% | 1.42pp | [81.0%, 86.6%] |
| Formal | 60+ | 221 | 85.0% | 2.75pp | [79.6%, 90.4%] |
| Informal | 18–29 | 1 914 | 77.8% | 1.46pp | [74.9%, 80.6%] |
| Informal | 30–44 | 2 790 | 73.4% | 1.16pp | [71.1%, 75.6%] |
| Informal | 45–59 | 2 254 | 72.5% | 1.26pp | [70.0%, 75.0%] |
| Informal | 60+ | 1 385 | 71.4% | 1.75pp | [68.0%, 74.8%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 707 | 80.3% | 0.59pp | [79.1%, 81.5%] |
| Complemento urbano | 4 941 | 74.7% | 0.99pp | [72.7%, 76.6%] |
| Rural | 5 483 | 72.6% | 0.94pp | [70.8%, 74.4%] |

**Confía "aprobatorio" en vecinos de su colonia/localidad (`AP5_1_3`).**
No-respuesta: 116 · sin cruce: 1 313 · útiles: 20 090.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 051 | 55.7% | 1.87pp | [52.0%, 59.4%] |
| Formal | 30–44 | 1 874 | 59.0% | 1.55pp | [55.9%, 62.0%] |
| Formal | 45–59 | 1 124 | 64.6% | 2.30pp | [60.1%, 69.1%] |
| Formal | 60+ | 221 | 72.3% | 3.79pp | [64.9%, 79.7%] |
| Informal | 18–29 | 1 913 | 49.4% | 1.65pp | [46.1%, 52.6%] |
| Informal | 30–44 | 2 786 | 51.4% | 1.38pp | [48.7%, 54.1%] |
| Informal | 45–59 | 2 251 | 57.7% | 1.50pp | [54.7%, 60.6%] |
| Informal | 60+ | 1 381 | 59.3% | 1.93pp | [55.5%, 63.1%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 681 | 55.1% | 0.78pp | [53.6%, 56.6%] |
| Complemento urbano | 4 929 | 56.4% | 0.99pp | [54.5%, 58.4%] |
| Rural | 5 480 | 56.7% | 1.18pp | [54.4%, 59.0%] |

**Patrón observado, descrito sin comparar componentes distintos (mismo
límite de §1.3):** dentro de `radio_confianza`, la confianza cae con la
distancia social del referente para el grupo Formal en el tramo joven
(49.8% desconocidos → 87.4% conocidos → 55.7% vecinos no es monótono en
distancia — vecinos rebasa a desconocidos), y sube con la edad en los tres
ítems.

### 3.2 `familismo_apoyo` — ENIF 2024, `TMODULO` (universo `filtro_s9_1=2`, n=12 379)

**`p9_9_4` — dinero de familiares en la vejez — el ítem que opera
`familismo_apoyo` (§1.2).** No-respuesta (9/blanco dentro del universo
efectivo): 484 · sin cruce formalidad/edad: 3 190 · útiles: 8 221.

| Formalidad | Edad | n | % sí | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 898 | 34.5% | 2.60pp | [29.4%, 39.6%] |
| Formal | 30–44 | 1 736 | 32.1% | 1.72pp | [28.7%, 35.5%] |
| Formal | 45–59 | 1 121 | 24.2% | 1.73pp | [20.8%, 27.6%] |
| Formal | 60+ | 217 | 33.5% | 3.28pp | [27.1%, 40.0%] |
| Informal | 18–29 | 1 108 | 41.0% | 2.10pp | [36.9%, 45.2%] |
| Informal | 30–44 | 1 623 | 47.1% | 1.68pp | [43.8%, 50.4%] |
| Informal | 45–59 | 1 415 | 49.0% | 1.97pp | [45.1%, 52.8%] |
| Informal | 60+ | 587 | 46.9% | 2.90pp | [41.2%, 52.6%] |

| Urbanización (`tloc`) | n | % sí | SE | IC95% |
|---|---|---|---|---|
| 100k+ | 6 211 | 38.7% | 0.93pp | [36.8%, 40.5%] |
| 15k–99,999 | 1 618 | 50.1% | 2.04pp | [46.1%, 54.0%] |
| 2,500–14,999 | 1 540 | 48.8% | 2.25pp | [44.3%, 53.2%] |
| <2,500 | 2 526 | 58.5% | 1.45pp | [55.6%, 61.3%] |

**Los otros cinco ítems del mismo menú — reportados como contexto, no como
`familismo_apoyo` (§1.2):**

| Ítem | n útil | % sí (agregado no ponderado por celda, ver script para desagregado) | Nota |
|---|---|---|---|
| `p9_9_1` gobierno adultos mayores | 11 676 | de 60.6% (Informal 18-29) a 88.8% (Informal 60+) | Sube fuerte con edad e informalidad |
| `p9_9_2` pensión/Afore | 11 869 | de 22.9% (Informal 60+) a 86.7% (Formal 30-44/45-59) | Brecha formal/informal, la más marcada de las seis |
| `p9_9_3` venta de bienes | 11 982 | de 16.2% (Informal 60+) a 41.6% (Informal 18-29) | Cae con edad |
| `p9_9_5` seguir trabajando | 12 059 | de 69.8% (Formal 60+) a 86.1% (Informal 30-44) | Alto en todas las celdas |
| `p9_9_6` otro | 12 053 | ~0.0%–0.6% | Categoría residual, casi vacía — no confundir con SIN SOPORTE: todas las celdas superan n=30, la proporción es genuinamente cercana a cero |

**Contraste declarado, no comparación causal entre componentes distintos:**
`p9_9_2` (pensión/Afore, mercado/Estado formal) y `p9_9_4` (familia) se
mueven en direcciones opuestas por formalidad — quien tiene empleo formal
espera pensión (86.7%) mucho más que dinero familiar (24-34%); quien está
en la informalidad espera lo inverso, con `familismo_apoyo` subiendo hasta
~47-49% y pensión cayendo hasta ~23-35%. Esto es descriptivo de los datos
medidos aquí, no una regla causal — mismo límite que todas las olas
anteriores declararon para contrastes entre ítems de un mismo menú.

Salida cruda completa (las 8 celdas formalidad×edad y las 4 celdas de
urbanización para cada uno de los 9 reactivos de esta sesión): `python3
tests/cal_conf_faseb_pos5_6.py`.

---

## 4 · Qué queda MEDIDO, con procedencia — y qué no

| Condicional | Estado | Fuente | Año | Variables | Universo efectivo | Método |
|---|---|---|---|---|---|---|
| `radio_confianza` | **MEDIDO·PARCIAL(x)**, por ítem (3 ítems separados, no escalar único) | ENCUCI | 2020 | `AP5_1_1/2/3`, dicotomizado ≥6/10 | Completo (todo entrevistado) | Proporción ponderada (`FAC_SEL`) + IC95% por conglomerado último; conjunto formalidad×edad + marginal `DOMINIO` |
| `familismo_apoyo` | **MEDIDO·PARCIAL(x)**, por ítem (6 ítems del menú, uno —`p9_9_4`— operacionaliza el constructo; los otros cinco son contexto) | ENIF | 2024 | `P9_9_1..6`, binario Sí/No | `filtro_s9_1=2` (<71 años) — 91.7% de `TMODULO`; 71+ años queda fuera por no-aplicabilidad estructural | Proporción ponderada (`fac_per`) + IC95% por conglomerado último; conjunto formalidad×edad + marginal `tloc` |

**Ejes efectivos declarados, uno por uno (clase `MEDIDO·PARCIAL(x)`,
sellada en `milpa/procedencia.yaml` por `PR #51`):**

- `radio_confianza` → ejes efectivos: formalidad, edad (conjunto) + dominio
  (marginal) — 2 de los 6 ejes de `canon` §1.1.A, sin escalar único (3
  ítems separados).
- `familismo_apoyo` → ejes efectivos: formalidad, edad (conjunto) +
  urbanización (marginal) — 2 de los 6 ejes, sin escalar único (6 ítems del
  menú, uno operacionaliza el constructo).

**No se cruzaron los seis ejes de `x` a la vez en ningún caso** — mismo
límite que toda Fase B anterior. **Compra la condicional, no el
coeficiente**, aplica a ambos reactivos con generadores específicos donde
C3 falla (§1.0): `familismo_apoyo` no identifica `G5`; `radio_confianza`
no identifica `cooperacion.confianza.puente_personal`.

### 4.1 Auditoría contra `canon` §1.1.B, propiedad por propiedad

- **Propiedad 1 (distribución, no media).** Cumplida: cada celda de §3
  reporta `n`, proporción ponderada, SE e IC95% — nunca un punto nacional
  único.
- **Propiedad 2 (restricción de nivel hogar viaja con la condicional).** No
  aplica conflicto: los condicionantes usados (formalidad y edad, nivel
  persona; dominio/`tloc`, nivel UPM/localidad, compartido por
  construcción por los miembros del mismo hogar) no mezclan una coordenada
  de hogar con una de persona de forma que parta a dos miembros del mismo
  hogar en ejes contradictorios.
- **Propiedad 3 (forma funcional no se inventa).** Cumplida: ninguna celda
  usa suavizado ni curva; medir los ítems por separado (§1.0/§1.1/§1.2), en
  vez de forzar un índice sobre referentes o fuentes de ingreso
  heterogéneas, es la aplicación de esta propiedad.

**`horizonte_temporal` (posición 10, `ENIF P4_10`) no se toca en este
acto** — sigue NO DETERMINABLE por C3 (`P2` §2.d), sin relación con lo
medido aquí salvo que vive en el mismo instrumento.

**Ni ENIGH, ni ENUT, ni Latinobarómetro se abrieron** — fuera de
perímetro de este encargo (§2 del encargo).

---

## 5 · El contador

**Condicionales medidas sobre atributos, previo a esta sesión: 6 de 14**
(verificado en §0 contra `canon/modelo-decision-v4_0.md:275,619,723`,
`forense/hitoE-campana-medicion-v2_0.md` §15/§15.1 y
`forense/hallazgos.md` 2026-08-04 — la posición 4 no aportó, `PR #57` lo
dejó en 6, no en 7).

**Esta sesión mide dos condicionales adicionales, ambas con reactivo
verificado y universo efectivo declarado (§1, §3):**

- `radio_confianza` — MEDIDO·PARCIAL(x), C1 de `G1` (C3 limpio para `G1`,
  falla solo para `cooperacion.confianza.puente_personal`, no usado aquí).
- `familismo_apoyo` — MEDIDO·PARCIAL(x), C1 de `G3` (C3 limpio para `G3`
  vía `P4_10` como desenlace; falla para `G5`, no usado aquí).

**Contador que corresponde al estado real verificado en esta sesión: 8 de
14** (6 + 2). No 9, no 7 — el número sale de contar lo efectivamente
medido y verificado en §0/§1/§3 de esta nota, no de lo que el encargo
sugería como destino de cada fila. Esta nota **no propaga** el 8 a
`milpa/procedencia.yaml` ni a `canon/modelo-decision-v4_0.md` — ese es el
acto de canon aparte que el encargo prohíbe explícitamente hacer aquí (§2
del encargo). Quien haga ese acto de canon deberá partir de este 8, no del
7 que el encargo asumía, y deberá decidir además si junta esta propagación
con la de la posición 4 (que sigue pendiente de reactivo, `§15` de
`hitoE`) en un solo paso, como el encargo mismo sugiere que sale más
barato.

`D`=14 derivado en `canon` §1.1.F. Los 6 parámetros escalares restantes
(`horizonte_temporal`, `aversion_riesgo`, `sens_estatus`, `deferencia`,
`familismo_obligacion`, `exposicion_violencia`) siguen fuera de alcance de
este acto, no medidos aquí — el contador no los infla.

---

## 6 · Suite y verificación de payload

`python3 tests/manifiesto.py --verifica` (corrido en este entorno, con
`data/raw` montado):

```
enif2024_csv [data_raw]: COINCIDE -- sha256 y tamaño (3086077 bytes) verificados contra data/manifiesto.yaml
encuci2020_bd_dbf [data_raw]: COINCIDE -- sha256 y tamaño (6913684 bytes) verificados contra data/manifiesto.yaml
```

`python3 tests/check.py` — salida cruda, sin editar, tal como pide el
encargo:

```
19 FAIL · 84 WARN
```

**Ninguno de los 19 FAIL ni 84 WARN lo introduce esta sesión.** `git
status --short` antes de este acto muestra únicamente `data/raw`
(symlink recreado, gitignorado) y `tests/cal_conf_faseb_pos5_6.py` (nuevo)
como no rastreados — esta sesión no tocó `canon/`, `corpus/reports/`,
`milpa/`, ni ningún archivo que la suite audite. Los 19/84 son
preexistentes al estado de `main` en `2a218a1`, ajenos a `radio_confianza`
y `familismo_apoyo` (glosario de constructos del motor, vocabulario de
tiers, marcos importados sin marca `(c)`, referencias colgantes en
documentos no relacionados, etc.) — no se investigan ni se corrigen aquí,
fuera de perímetro de este encargo.

---

## 7 · Límite de lectura declarado (ADR-46)

Esta sesión leyó completos: `forense/hitoE-campana-medicion-v2_0.md`
§14-§15; `forense/notas/2026-08-01-p2-momentos-atributos.md` §2.c-§2.d;
`forense/notas/2026-07-31-inventario-segmentacion.md` (filas de
`radio_confianza`/`familismo_apoyo`/`cooperacion.confianza.puente_
personal`); `forense/notas/2026-08-03-cal-conf-faseb-medicion.md` (ENIF
financiera, §1.3, §3.3); `forense/notas/2026-08-03-cal-conf-faseb-
medicion-ola2.md` completa (plantilla de protocolo y join ENCUCI);
`forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md` §0.2, §4.0-§4.2
(modo de falla, precedente C3); `forense/hallazgos.md` (entradas
2026-08-03/04); `canon/modelo-decision-v4_0.md:275,346,465,496,619,723`
(grep dirigido, no completo); `data/manifiesto.yaml` (entradas
`encuci2020_bd_dbf`, `encuci2020_fd_pdf`, `enif2024_csv`).

Microdato abierto y leído: `FD_ENCUCI2020.pdf` p.15-27 (páginas
completas, no solo grep); `ENCUCI_2020_SD.dbf` y `ENCUCI_2020_SEC_4_5.dbf`
(campos `AP5_1_1..4`, `AP5_2_6`, `UPM`/`VIV_SEL`/`R_SEL`/`N_REN`,
`EDAD`, `AP3_15_4`, `FAC_SEL`, `DOMINIO`, `EST_DIS`, `UPM_DIS`);
`diccionario_datos_tmodulo_enif2024.csv` completo (búsqueda por patrón,
filas 317-339 leídas en detalle); catálogos `p9_9_1.csv`…`p9_9_6.csv`,
`filtro_s9_1.csv`, `tloc.csv`; `conjunto_de_datos_tmodulo_enif2024.csv`
(columnas `p9_9_1..6`, `filtro_s9_1`, `p11_1_1..5`, `edad_v`, `p3_13`,
`tloc`, `est_dis`, `upm_dis`, `fac_per`).

**No se tocó** `canon/`, `milpa/`, `corpus/` (más allá de lectura dirigida
de `canon/modelo-decision-v4_0.md` para verificar ids de Tabla B). No se
abrió ENIGH, ENUT, ni Latinobarómetro. No se movió ningún contador en
archivo — el 8/14 de §5 es lo que esta nota declara como estado real
verificado, no una edición a `canon`.
