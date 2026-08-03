# CAL-CONF Fase B — medición de la condicional para los tres componentes INSTRUMENTADO

*3 de agosto de 2026.*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada.** Esta sesión abre microdato (ENCIG
2021, ENCUCI 2020, ENIF 2024: registros, no solo descriptores/cuestionarios).
Queda **contaminada para pre-registrar** contra estas mismas encuestas
(ENCUCI, ENIF) y, por la misma disciplina, contra ENCIG y ENIGH. No es un
costo evitable: es el precio de medir. Los pre-registros correspondientes
(P3 · LCA de segmentación, y cualquier otro que dependa de estas fuentes) ya
se escribieron antes y en otra sesión (`forense/notas/2026-08-01-p3-*.md` y
similares) — esta nota no los toca ni los reabre.

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta
sesión (dictionaries, cuestionarios, microdato). La premisa de qué componentes
están hoy INSTRUMENTADO es tipo (3) hasta contrastarla — ver §0.

---

## 0 · Verificación de premisas antes de obedecer

**Premisa del encargo:** *"los tres componentes de `confianza_institucional`
hoy INSTRUMENTADO, según la adenda a hitoE fusionada hoy (PR #48): salud,
educación (ENCUCI `AP5_2_6`), financiera (ENIF Sección 11, `P11_1_1`–`P11_1_5`)."*

**Verificación.** `git fetch origin` trae `27fbb93` (`Merge pull request #48
from Josanoforo/claude/hitoe-premisas-adenda-ghzpq6`) — PR #48 existe y está
fusionado hoy. Su contenido, `forense/hitoE-campana-medicion-v2_0.md` §12
("Adenda 03/ago/2026 — `CAL-CONF` Fase A tumba dos veredictos SIN
INSTRUMENTO"), leído completo:

- §12.1 confirma **educación → INSTRUMENTADO** vía `ENCUCI AP5_2_6`
  "Universidades" (`FD_ENCUCI2020.pdf`, pregunta 5.2, p. 26) y **financiera →
  INSTRUMENTADO** vía `ENIF Sección 11, P11_1_1`-`P11_1_5` (`enif_2024_fd.xlsx`,
  hoja `TMODULO`; `enif_2024_cuestionario.pdf`, p. 28), verificado aparte que
  la batería no está condicionada a tenencia de producto financiero.
- **Salud no traía código en el encargo** ("vienen de nota, no de tu
  lectura" — pero el código de salud no estaba en la nota, así que esta
  sesión lo derivó de la fuente que sí la cita: `forense/notas/2026-07-31-cal-conf-fasea.md`,
  tabla "Resultado por componente", fila Salud: *"ENCIG ítem 3 'Hospitales
  públicos' (`encig21_cuestionario.pdf`, sección XI, p. 22)"*. Verificado
  contra el diccionario de datos real (`diccionario_de_datos_encig2021_01_sec_11.csv`):
  el ítem 3 es la variable **`P11_1_3`** ("Confianza en hospitales
  públicos"), confirmado también contra el cuestionario (`encig21_cuestionario.pdf`,
  Sección XI, pregunta 11.1, opción 03 "Hospitales públicos?", p. 22).

**Veredicto: la premisa se sostiene.** Los tres componentes son, en efecto,
salud (ENCIG `P11_1_3`), educación (ENCUCI `AP5_2_6`) y financiera (ENIF
`P11_1_1`-`P11_1_5`) — verificados contra archivo, no aceptados de la nota
sola.

**Pieza de la premisa que NO se sostiene sin matiz:** el encargo asume que
los seis ejes de `x` (§1.1.A de `canon/modelo-decision-v4_0.md`, variables de
`ENIGH`) están disponibles como condicionantes. **No lo están, directamente.**
`canon` §1.1.C es explícito: *"la síntesis amplía la malla de atributos; no
amplía la malla de pares (parámetro, desenlace)"* — si el reactivo de
`θ_k` vive en `ENCIG`/`ENCUCI`/`ENIF` y el desenlace (aquí, la propia
confianza) vive en el mismo instrumento, los condicionantes **también deben
salir de ese mismo instrumento**, no de `ENIGH` vía reponderación (eso
fabricaría una conjunta que nadie midió). Esta sesión, por tanto, no usa las
variables textuales de §1.1.A (`segsoc`, `tam_loc`, `celular`...) sino sus
análogas **dentro de cada instrumento**, declaradas una por una en §1 y
verificadas contra el diccionario de datos correspondiente antes de usarlas.
Donde un instrumento no trae análogo limpio de un eje, el eje se declara
**NO DISPONIBLE** para ese componente — no se rellena, no se aproxima con
`ENIGH`.

---

## 1 · Especificación de la medición — congelada antes de calcular

*Regla de la sesión: nada de lo que sigue se toca después de ver una tabla
de resultados. Un cambio de escala, de corte o de eje después de correr el
script sería exactamente el defecto que el reencuadre existe para impedir
(`canon` §1.1.B, propiedad 3).*

### 1.0 Declaraciones comunes a los tres componentes

- **Tramos de edad** (canon §1.1.F: "edad... no tiene partición canónica" —
  se declara aquí, no se deriva de los datos): **18–29 · 30–44 · 45–59 · 60+**.
  Mismo corte en los tres componentes.
- **n mínimo por celda para reportar estimación puntual: 30 casos sin
  ponderar.** Por debajo: la celda se reporta como **SIN SOPORTE**, con su
  `n` — no se colapsa con celdas vecinas ni se omite.
- **No-respuesta:** excluida del numerador y denominador de toda proporción;
  su `n` se reporta aparte cuando sea material (>0 en la celda).
- **Dispersión:** error estándar e IC95% por el estimador de **"conglomerado
  último" (ultimate cluster)** — UPM (`UPM_DIS`) anidada en estrato de diseño
  (`EST_DIS`) — sobre la proporción ponderada. Es una aproximación de un
  solo nivel de conglomerado (la UPM primaria que cada instrumento declara),
  **no** un cálculo multietápico completo: no hay `numpy`/`scipy`/paquete de
  encuestas complejas instalado en este entorno (mismo límite que declaró
  `forense/notas/2026-07-31-cal-conf-fasea.md` para `pandas`/`openpyxl`), y
  esta sesión no instala dependencias nuevas para evitarlo — implementa el
  estimador en Python puro y lo verifica contra un caso conocido (§2, nota al
  pie de cada tabla).
- **Migración (eje 6 de §1.1.A):** sin variable limpia y universal en ENCIG
  ni en ENCUCI (verificado exhaustivamente: ENCIG no tiene ninguna variable
  de residencia/movilidad en sus 6 tablas; la única variable de ENCUCI
  relacionada, `AP10_2`, está condicionada a haberse mudado de vivienda, no
  aplica al universo general). **NO DISPONIBLE para salud y educación.**
  ENIF sí trae una candidata (`p3_15_epc`, ver §1.3) — se usa ahí, como
  marginal, con su propia advertencia de referencia temporal.
- **No se invierte forma funcional:** todas las celdas abajo son proporciones
  empíricas por celda observada. Ningún ajuste, ninguna curva, ningún
  suavizado.
- **No se extrapola a la cola alta A/B** (límite permanente de `canon`
  §1.1.C-i): ninguna de las tres encuestas fuente permite identificarla, y
  esta nota no lo intenta.

### 1.1 Salud — ENCIG 2021, `P11_1_3` "Confianza en hospitales públicos"

- **Instrumento:** tabla `conjunto_de_datos_encig2021_01_sec_11` (reactivo,
  ponderador `FAC_P18`, diseño `EST_DIS`/`UPM_DIS`), unida por `ID_PER` a
  `conjunto_de_datos_encig2021_02_residentes_sec_2` (única variable
  demográfica limpia disponible: `EDAD`). Join verificado: `ID_PER` codifica
  `ENT.UPM.V_SEL.N_REN`, y el último segmento coincide con `R_ELE`
  ("renglón del elegido") de la propia tabla de sección 11 — no hace falta
  pasar por `R_ELE` como llave separada, `ID_PER` ya es la llave directa.
- **Escala:** ordinal de 4 (`1` Mucha confianza · `2` Algo de confianza ·
  `3` Algo de desconfianza · `4` Mucha desconfianza), verificada contra
  `encig21_cuestionario.pdf` Sección XI, pregunta 11.1. No-respuesta:
  `5` (No aplica) y `9` (No sabe/no responde) excluidos.
- **Dicotomización, declarada:** confía = `{1,2}`; no confía = `{3,4}`. Corte
  en el punto medio de una escala de 4 sin categoría neutra.
- **Condicionantes disponibles en este instrumento:** **solo edad**
  (tramos de §1.0), vía `residentes_sec_2.EDAD`. **Formalidad, urbanización,
  ingreso y acceso digital: NO DISPONIBLES.** Verificado, no supuesto:
  - Formalidad: `POS` ("posición en la ocupación") es la única variable
    ocupacional en `residentes_sec_2`; `forense/notas/2026-07-31-cal-conf-fasea.md`
    ya declaró que ENCIG "no tiene módulo de prestaciones laborales... no
    equivale a formal/informal sin una prestación o afiliación adicional que
    ENCIG no pregunta" — no se usa.
  - Urbanización: los metadatos oficiales (`metadatos_encig_2021.txt`) dicen,
    verbatim, que el objetivo es *"recabar, en ciudades de 100 000 y más
    habitantes, información..."* — el universo de ENCIG es exclusivamente
    urbano de 100k+; no hay gradiente de tamaño de localidad que condicionar
    (`AREAM` identifica área metropolitana específica, no un tamaño).
  - Ingreso, acceso digital: ninguna de las 6 tablas de ENCIG (`sec1_A`,
    `residentes_sec_2`, `sec_6`, `sec_7`, `sec_8`, `sec_11`) trae variable de
    ingreso ni de conectividad general — revisadas las 6 completas, no solo
    la de la confianza.
- **Ponderador:** `FAC_P18` (factor de expansión, población 18 años y más —
  coincide con la unidad de análisis: el elegido de ENCIG es siempre adulto).

### 1.2 Educación — ENCUCI 2020, `AP5_2_6` "Confianza en universidades públicas"

- **Instrumento:** tabla `ENCUCI_2020_SEC_4_5` (reactivo, ponderador
  `FAC_SEL`, `DOMINIO`, diseño `EST_DIS`/`UPM_DIS`) unida a `ENCUCI_2020_SD`
  (`EDAD`, `AP3_15_4`) por `UPM`+`VIV_SEL`+`R_SEL` = `N_REN` (relación
  declarada en `FD_ENCUCI2020.pdf` §1.2.4); a `ENCUCI_2020_SEC_9_10`
  (`AP10_14`) por la misma llave de persona seleccionada; y a
  `ENCUCI_2020_VIV` (`AP1_4_11`, nivel **hogar**) por `UPM`+`VIV_SEL` sin
  `R_SEL` (coordenada de hogar, no de persona — §1.1.B propiedad 2).
- **Escala:** idéntica a salud (4 niveles + `5` No aplica + `9` No sabe/no
  responde), verificada contra `FD_ENCUCI2020.pdf` pregunta 5.2, p. 22.
  Misma dicotomización que salud.
- **Condicionante primario (conjunto):** formalidad (`AP3_15_4`: `1`=formal
  vía derechohabiencia de trabajo, `0`=informal; blanco=no trabajó la semana
  de referencia, excluido del eje — es no-aplicabilidad estructural, no
  no-respuesta) × edad (tramos de §1.0).
- **Marginales adicionales (un eje a la vez, no cruzados con el primario ni
  entre sí — ver límite de alcance en §1.5):**
  - Urbanización: `DOMINIO` (`U` Urbano · `C` Complemento urbano · `R`
    Rural) — no es idéntico al `tam_loc` de 4 tramos de ENIGH, pero es la
    partición de urbanización que ENCUCI sí trae, declarada como tal.
  - Ingreso: `AP10_14`, 6 tramos nativos del instrumento (`<$3,000` ...
    `>$11,000`); `7` (No recibe ingresos) se trata como celda propia, `8`
    (No quiere decir) y `9` (No sabe) como no-respuesta.
  - Acceso digital: `AP1_4_11` ("servicio de internet", hogar): `1` Sí / `2`
    No; `9` No sabe/no responde excluido.
- **Migración:** NO DISPONIBLE (§1.0).
- **Ponderador:** `FAC_SEL` (población 15 años y más, persona seleccionada —
  coincide con la unidad de análisis).

### 1.3 Financiera — ENIF 2024, índice de `P11_1_1`–`P11_1_5`

- **Instrumento:** tabla única `conjunto_de_datos_tmodulo_enif2024` — reactivos,
  `edad_v`, `p3_13`, `tloc`, `p3_15_epc`, `p3_11a`, `est_dis`, `upm_dis`,
  `fac_per` viven todos en el mismo registro; no hace falta join.
- **Escala base:** 5 sub-ítems binarios `1` Sí / `2` No / `9` No sabe, cada
  uno una expectativa hipotética distinta sobre bancos o instituciones
  financieras (verificado contra `enif_2024_cuestionario.pdf` p. 28,
  pregunta 11.1: *"Si usted tuviera que solicitar los servicios de un banco
  o cualquier otra institución financiera, ¿considera que...?"* — aplica a
  todo entrevistado adulto, no condicionado a tenencia de producto
  financiero, verificado en `forense/notas/2026-07-31-cal-conf-fasea.md`
  "De paso").
- **Operacionalización declarada, distinta de salud/educación porque la
  escala de origen es distinta (5 binarios, no 1 ordinal de 4):** índice =
  número de "Sí" entre los 5 ítems, calculado **solo** para quienes
  respondieron válido (`1` o `2`) en los **5**; si falta o es "No sabe" (`9`)
  en cualquiera de los 5, el caso se excluye del índice — no-respuesta a
  nivel de índice, reportada aparte.
- **Dicotomización, declarada:** confía = índice ≥ 3 (mayoría de "Sí" entre
  los 5); no confía = índice ≤ 2.
- **Condicionante primario (conjunto):** formalidad (`p3_13`: `1`-`6`
  (cualquier fuente de derechohabiencia por trabajo) = formal, `7` = "carece
  de derecho... por parte de su trabajo" = informal; blanco = no trabaja,
  `9` = no sabe, ambos excluidos del eje) × edad (`edad_v`, tramos de §1.0).
- **Marginales adicionales:**
  - Urbanización: `tloc` — **idéntico esquema a `tam_loc` de ENIGH** (`1`
    100,000+ · `2` 15,000–99,999 · `3` 2,500–14,999 · `4` <2,500),
    verificado contra el catálogo `tloc.csv`. Es el único de los tres
    componentes donde el eje de ENIGH tiene análogo exacto en el mismo
    instrumento.
  - Migración: `p3_15_epc` (entidad o país donde vivía hace 5 años,
    verificado contra el catálogo — incluye 12 países extranjeros con clave
    de 3 dígitos ≥ 200, y las 32 entidades con clave 001–032). Migrante
    internacional = código de país extranjero; no migrante = código de
    entidad mexicana 001–032; `999` (No especificado) excluido. **Misma
    advertencia que `canon` §1.1.A-ii sobre `residencia` de ENIGH:** no se
    puede confirmar si la variable de ENIGH mide la misma referencia
    temporal (hace 5 años) que `p3_15_epc` declara explícitamente para
    ENIF — se usa el análogo de ENIF por lo que ENIF sí declara, no como
    equivalencia confirmada con ENIGH.
  - Ingreso: `p3_11a` (monto continuo, `00000`=no recibe ingresos por
    trabajo, `99888`=no responde), recodificado a los **mismos 6 tramos
    declarados para ENCUCI** en §1.2 (elección de esta sesión para
    comparabilidad aproximada entre componentes, no derivada de los datos
    de ENIF).
- **Acceso digital:** NO DISPONIBLE — no se localizó variable de
  conectividad general en `TMODULO`; `TVIVIENDA`/`TSDEM` no se abrieron en
  este acto (declarado como **no verificado**, no como ausente confirmado —
  a diferencia de ENCIG, donde sí se revisaron las 6 tablas completas).
- **Ponderador:** `fac_per` (factor de expansión a nivel persona).

### 1.4 Lo que esta especificación decide no hacer, declarado

- No se cruzan las 4–5 marginales entre sí en una malla conjunta completa
  (formalidad × edad × urbanización × ingreso × acceso). El conjunto
  primario (formalidad × edad) sí es una condicional conjunta genuina; el
  resto son marginales de un eje a la vez. Es una elección de alcance de
  esta sesión, no un hallazgo de que la malla completa sea inviable —
  `canon` §1.1.F ya dice que el número de celdas no es el cuello de botella;
  el cuello de botella aquí es el tiempo de la sesión. La malla conjunta
  completa queda para otro acto.
- No se calibra ni compara entre los tres componentes (¿es más alta la
  confianza en salud que en educación?) — cada uno vive en un instrumento,
  año y universo muestral distintos; comparar los números crudos entre
  componentes sería inventar una conjunta que no existe, el mismo error que
  `canon` §1.1.C prohíbe para condicionantes.

---

## 2 · El estimador de dispersión, probado contra un caso conocido

Antes de confiar en el estimador de "conglomerado último" (ultimate
cluster) implementado en Python puro (`svystat.py`), se probó contra un
caso con solución cerrada conocida: muestra aleatoria simple, pesos
uniformes, un conglomerado por observación (n=200, 80 éxitos). Bajo ese
caso degenerado, la fórmula debe coincidir exactamente con la varianza
muestral estándar de una proporción, `p(1-p)/(n-1)`.

**Comando:** `python3 svystat.py`

```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
```

Coincide a 9 decimales. El estimador se usa tal cual sobre los tres
componentes, con `UPM_DIS`/`EST_DIS` (ENCIG, ENCUCI) y `upm_dis`/`est_dis`
(ENIF) como conglomerado y estrato de diseño reales — no el caso degenerado
de la prueba.

**Verificación adicional, por orden de magnitud, sobre cada ponderador**
(no es una cifra tecleada: es la suma de la columna de peso sobre la tabla
completa, antes de cualquier filtro de esta sesión):

| Instrumento | Ponderador | Suma sobre toda la tabla | Universo declarado | ¿Coherente? |
|---|---|---|---|---|
| ENCIG 2021 | `FAC_P18` | 51,302,010 | Población 18+ en ciudades de 100 000+ hab. (único universo de ENCIG, confirmado en metadatos oficiales) | Sí — del orden de la mitad de la población adulta nacional, consistente con que solo una fracción de México vive en ciudades de 100k+ |
| ENCUCI 2020 | `FAC_SEL` | 96,427,583 | Población 15+ de México, urbana y rural | Sí — del orden de la población 15+ de México en 2020 (Censo 2020: ~97 millones de 15 años y más) |
| ENIF 2024 | `fac_per` | 94,221,441 | Población 18+ de México | Sí — del orden de la población adulta de México en 2024 |

---

## 3 · Resultados por componente

### 3.1 Salud — ENCIG 2021, `P11_1_3`

`sec_11`: 39 930 filas totales · 1 472 no-respuesta (`5`/`9`) excluidas ·
0 sin `EDAD` tras el cruce por `ID_PER` (cruce perfecto: la llave directa
funcionó en el 100% de los casos) · **38 458 casos útiles**.

| Edad | n (sin ponderar) | % confía (ponderado) | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 8 661 | 72.8% | 0.81pp | [71.2%, 74.4%] |
| 30–44 | 11 891 | 67.9% | 0.73pp | [66.5%, 69.4%] |
| 45–59 | 9 884 | 70.0% | 0.73pp | [68.5%, 71.4%] |
| 60+ | 8 022 | 71.8% | 0.85pp | [70.2%, 73.5%] |

Las cuatro celdas superan el mínimo de 30 casos; ninguna es SIN SOPORTE.

### 3.2 Educación — ENCUCI 2020, `AP5_2_6`

`SEC_4_5`: 21 519 filas · 1 483 no-respuesta en `AP5_2_6` excluidas · 1 265
sin cruce válido a `SD` (persona seleccionada sin `EDAD` legible, o sin fila
correspondiente) · **18 771 casos útiles**.

**Conjunto primario — formalidad × edad:**

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 035 | 82.4% | 1.41pp | [79.7%, 85.2%] |
| Formal | 30–44 | 1 855 | 79.6% | 1.45pp | [76.8%, 82.5%] |
| Formal | 45–59 | 1 084 | 79.2% | 1.64pp | [76.0%, 82.4%] |
| Formal | 60+ | 210 | 85.5% | 2.66pp | [80.3%, 90.7%] |
| Informal | 18–29 | 1 844 | 78.4% | 1.17pp | [76.1%, 80.7%] |
| Informal | 30–44 | 2 657 | 75.1% | 1.15pp | [72.8%, 77.3%] |
| Informal | 45–59 | 2 082 | 67.2% | 1.49pp | [64.2%, 70.1%] |
| Informal | 60+ | 1 185 | 62.0% | 1.88pp | [58.3%, 65.6%] |

Todas las celdas superan el mínimo de 30. (El resto de la muestra —
`18 771 − Σceldas` — corresponde a personas sin dato válido de `AP3_15_4`,
es decir sin trabajo la semana de referencia: no entran a este cruce por
diseño, no por SIN SOPORTE.)

**Marginal — urbanización (`DOMINIO`):**

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 272 | 78.1% | 0.65pp | [76.8%, 79.3%] |
| Complemento urbano | 4 654 | 70.4% | 1.01pp | [68.4%, 72.4%] |
| Rural | 4 845 | 67.2% | 1.33pp | [64.6%, 69.8%] |

**Marginal — acceso digital (`AP1_4_11`, internet en el hogar):**

| Internet | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Sí | 9 819 | 79.5% | 0.63pp | [78.2%, 80.7%] |
| No | 8 947 | 66.5% | 0.79pp | [65.0%, 68.1%] |

**Marginal — ingreso (`AP10_14`):**

| Ingreso mensual | n | % confía | SE | IC95% |
|---|---|---|---|---|
| <$3,000 | 6 874 | 68.6% | 0.79pp | [67.1%, 70.1%] |
| $3,000–5,500 | 4 018 | 77.3% | 0.93pp | [75.5%, 79.1%] |
| $5,501–7,500 | 1 683 | 75.9% | 1.45pp | [73.1%, 78.7%] |
| $7,501–9,000 | 1 134 | 80.8% | 1.45pp | [78.0%, 83.7%] |
| $9,001–11,000 | 858 | 84.5% | 1.69pp | [81.2%, 87.8%] |
| >$11,000 | 1 342 | 83.0% | 1.60pp | [79.9%, 86.2%] |
| Sin ingreso (código 7) | 1 902 | 70.9% | 1.33pp | [68.3%, 73.5%] |

Todas las celdas de las tres marginales superan el mínimo de 30 — ninguna
SIN SOPORTE en educación.

### 3.3 Financiera — ENIF 2024, índice `P11_1_1`–`P11_1_5`

`TMODULO`: 13 502 filas · 3 238 sin índice válido (no sabe o blanco en al
menos uno de los 5 ítems) · 0 sin tramo de edad válido · **10 264 casos
útiles**.

**Conjunto primario — formalidad × edad:**

| Formalidad | Edad | n | % confía (índice≥3) | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 813 | 79.0% | 2.30pp | [74.5%, 83.5%] |
| Formal | 30–44 | 1 501 | 76.5% | 1.66pp | [73.3%, 79.8%] |
| Formal | 45–59 | 933 | 74.7% | 2.08pp | [70.7%, 78.8%] |
| Formal | 60+ | 213 | 72.4% | 2.54pp | [67.4%, 77.4%] |
| Informal | 18–29 | 938 | 73.9% | 1.93pp | [70.1%, 77.7%] |
| Informal | 30–44 | 1 344 | 65.2% | 1.85pp | [61.6%, 68.8%] |
| Informal | 45–59 | 1 067 | 58.9% | 2.13pp | [54.7%, 63.0%] |
| Informal | 60+ | 529 | 49.1% | 3.02pp | [43.2%, 55.0%] |

Todas las celdas superan el mínimo de 30.

**Marginal — urbanización (`tloc`, idéntico esquema a `tam_loc` de ENIGH):**

| tloc | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 100,000+ hab. | 5 551 | 73.3% | 0.92pp | [71.5%, 75.1%] |
| 15,000–99,999 | 1 408 | 69.6% | 2.02pp | [65.6%, 73.6%] |
| 2,500–14,999 | 1 280 | 60.5% | 1.81pp | [57.0%, 64.1%] |
| <2,500 | 2 025 | 58.1% | 1.55pp | [55.1%, 61.2%] |

**Marginal — migración (`p3_15_epc`, residencia hace 5 años):**

| Migración | n | % confía | SE | IC95% |
|---|---|---|---|---|
| México (misma o distinta entidad) | 10 187 | 68.2% | 0.72pp | [66.8%, 69.6%] |
| Extranjero | 63 | 76.0% | 2.13pp | [71.8%, 80.2%] |

Ambas celdas superan el mínimo de 30 — la de "Extranjero" lo hace por muy
poco (63 casos); es la celda más frágil de todo el acto, aunque formalmente
no es SIN SOPORTE.

**Marginal — ingreso (`p3_11a`, recodificado a los tramos de ENCUCI):**

| Ingreso mensual | n | % confía | SE | IC95% |
|---|---|---|---|---|
| <$3,000 | 3 681 | 64.1% | 1.22pp | [61.7%, 66.5%] |
| $3,000–5,500 | 1 236 | 73.9% | 1.65pp | [70.7%, 77.2%] |
| $5,501–7,500 | 404 | 77.0% | 2.32pp | [72.5%, 81.5%] |
| $7,501–9,000 | 299 | 68.0% | 4.73pp | [58.7%, 77.2%] |
| $9,001–11,000 | 304 | 79.2% | 2.62pp | [74.1%, 84.4%] |
| >$11,000 | 1 033 | 80.8% | 1.49pp | [77.9%, 83.7%] |
| Sin ingreso por trabajo (código 0) | 67 | 55.6% | 5.22pp | [45.3%, 65.8%] |

Todas las celdas superan el mínimo de 30 (la de "sin ingreso" por muy poco,
67 casos) — ninguna SIN SOPORTE, pero dos de las siete son frágiles.

**Ningún componente, en ningún cruce de esta sesión, produjo una celda por
debajo del mínimo de 30.** No es un resultado buscado — es consecuencia de
que las tres encuestas fuente tienen tamaños de muestra grandes (miles a
decenas de miles de casos útiles) y de que esta sesión limitó el
condicionamiento a como mucho dos ejes cruzados (§1.4), precisamente para
mantener las celdas pobladas. Una malla más fina (más ejes cruzados, o
tramos de edad más finos) sí produciría celdas SIN SOPORTE — eso queda
para el acto que retome la malla conjunta completa.

---

## 4 · Qué queda MEDIDO, con procedencia — y qué no

| Componente | Estado | Fuente | Año | Variable | n útil | Método |
|---|---|---|---|---|---|---|
| `confianza_institucional[salud]` | **MEDIDO** (parcial: 1 eje de 6) | ENCIG | 2021 | `P11_1_3` | 38 458 | Proporción ponderada (`FAC_P18`) + IC95% por conglomerado último (`UPM_DIS`/`EST_DIS`), condicionada solo a edad |
| `confianza_institucional[educación]` | **MEDIDO** (parcial: 2 ejes conjuntos + 3 marginales de 6) | ENCUCI | 2020 | `AP5_2_6` | 18 771 | Ídem, ponderador `FAC_SEL`; conjunto formalidad×edad + marginales urbanización/ingreso/acceso digital |
| `confianza_institucional[financiera]` | **MEDIDO** (parcial: 2 ejes conjuntos + 3 marginales de 6) | ENIF | 2024 | Índice de `P11_1_1`–`P11_1_5` | 10 264 | Ídem, ponderador `fac_per`; conjunto formalidad×edad + marginales urbanización/migración/ingreso |

**"MEDIDO (parcial)" se declara así, no como "MEDIDO" a secas, por lo que
§1.4 ya reconoce:** ninguno de los tres cruza los seis ejes de `x`
simultáneamente. Es una condicional genuina — no una media puntual — pero
sobre un subconjunto de `x`, declarado antes de calcular, no descubierto
después.

**Los otros tres componentes de `confianza_institucional`** (seguridad-FFAA,
electoral-partidos, justicia-policía) siguen **PARCIAL** según la adenda de
hitoE §12 (candidata adyacente, no reactivo textual confirmado por
inspección completa como el que sí tienen los tres de este acto) — **no se
tocan en este acto**: están fuera de alcance por instrucción explícita del
encargo.

**Los ocho parámetros escalares** (`horizonte_temporal`, `radio_confianza`,
`aversion_riesgo`, `sens_estatus`, `deferencia`, `familismo_apoyo`,
`familismo_obligacion`, `exposicion_violencia`) — **fuera de alcance,
no tocados.**

**Reclasificación sugerida para `milpa/procedencia.yaml` — declarada, no
ejecutada** (el encargo prohíbe tocar `milpa/` en este acto; esto es
insumo para el acto posterior con el contador):
- Los tres componentes de salud/educación/financiera de
  `confianza_institucional` deberían pasar de lo que hoy tengan asignado a
  una clase que refleje "medido empíricamente, condicional parcial sobre
  `x`, sin forma funcional" — no "MEDIDO" pleno (que implicaría los 6 ejes),
  ni "ASIGNADO"/"PENDIENTE" (que implicaría cero medición). Si
  `procedencia.yaml` no tiene hoy una clase intermedia para esto, es un
  hueco de taxonomía que esta nota señala pero no resuelve.

---

## 5 · El contador

**condicionales medidas sobre atributos: 3 de 14**

Los tres son `confianza_institucional[salud]`, `confianza_institucional[educación]`
y `confianza_institucional[financiera]` — cada uno medido como distribución
condicional empírica (no media puntual), con `n` sin ponderar, estimación
ponderada por el factor de expansión del diseño muestral correspondiente, y
dispersión por conglomerado último, sobre un subconjunto declarado de `x`
(nunca los seis ejes a la vez — ver §1.4 y §4). Los 11 restantes (3
componentes PARCIAL de `confianza_institucional` + 8 escalares) están fuera
de alcance de este acto por instrucción explícita del encargo, no medidos
aquí, y el contador no los infla.

