# CAL-CONF Fase B, segunda ola — medición de la condicional para los tres componentes recién ascendidos a INSTRUMENTADO

*3 de agosto de 2026.*

⚠️ **CONTAMINACIÓN DE MICRODATO, declarada.** Esta sesión abre microdato de
**ENVIPE 2025** (registros, no solo `fd_envipe2025.pdf`/cuestionarios — la
fuente que la primera ola de Fase B **no** abrió), **ENCUCI 2020** y **ENCIG
2021** (candidata, revisada pero no usada — ver §1.4). Queda **contaminada
para pre-registrar** contra ENVIPE, ENCUCI y ENCIG. No es un costo evitable:
es el precio de medir. Cualquier pre-registro que dependa de estas tres
fuentes y no se haya escrito ya en otra sesión queda bloqueado por esta
apertura.

**Procedencia.** Tipo (1) para todo lo verificado contra archivo en esta
sesión (diccionarios de datos, cuestionarios, microdato, manifiesto). La
premisa de qué tres componentes están hoy INSTRUMENTADO es tipo (3) hasta
contrastarla — ver §0.

---

## 0 · Verificación de premisas antes de obedecer

**Premisa del encargo:** *"los tres componentes recién ascendidos a
INSTRUMENTADO: seguridad-FFAA, justicia-policía, electoral-partidos."*

**Verificación.** `git fetch origin` trae `f6bcaaa` (`Merge pull request #52
from Josanoforo/claude/verify-phase-a-premises-h9cm32`) — PR #52 existe y
está fusionado. Su contenido es `forense/hitoE-campana-medicion-v2_0.md`
§13 ("Adenda 03/ago/2026 — la nota 'queda anotado, sin actuar' de §12 se
resuelve"), leído completo — **no** el §4 de
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md`, que la propia adenda
señala como desactualizado en su §6 ("esa frase ya no describe lo que Fase
A trae"). §13.2 da la tabla corregida:

| Componente | Veredicto | Candidata (Fase A, `§13.1`) |
|---|---|---|
| seguridad-FFAA | INSTRUMENTADO | ENVIPE `AP5_4_04/08/09/10` · ENCUCI `AP5_3_4/AP5_3_5` · ENCIG ítem 20/21 |
| justicia-policía | INSTRUMENTADO | ENVIPE `AP5_4_01/02/03/05/06/07/11` · ENCUCI `AP5_3_1/AP5_3_3` · ENCIG ítem 2/17/22 |
| electoral-partidos | INSTRUMENTADO | ENCUCI `AP5_2_5/AP5_3_6/7/8` · ENCIG ítem 12/14/19 |

**Veredicto: la premisa se sostiene**, con la misma exigencia de detalle
—variable, archivo, página— que ya se aplicó en la primera ola. Verificado
además, no solo citado: los 11 códigos ENVIPE/ENCUCI de arriba se
contrastaron contra el diccionario de datos real
(`fd_envipe2025.pdf` y `FD_ENCUCI2020.pdf`, ambos leídos página por página
para este acto, no solo grep) — ver §1 para el detalle exacto, con una
corrección menor: `§13.1` describe `AP5_3_6` como "Senadores federales" y
`AP5_3_7` como "Diputados"; el diccionario real dice `AP5_3_6` = "Senadores
y diputados federales" (una sola pregunta que agrega ambas cámaras) y
`AP5_3_7` = "Diputados **locales**" (no federales). El código y el
componente que mide (confianza legislativa) no cambian; la etiqueta sí se
corrige aquí porque esta sesión leyó el diccionario directo (procedencia
tipo 1), no la paráfrasis de `§13.1` (procedencia tipo 3 para ese detalle
puntual).

**Microdato en disco, verificado — no supuesto.** `tests/manifiesto.py
--verifica` corrido en esta sesión sobre los tres ids de payload (no solo
los FD/cuestionario que `§13.5` ya había verificado AUSENTE del lado del
manifiesto en la sesión anterior):

```
envipe2025_csv    [data_raw]: COINCIDE -- sha256 y tamaño (17600019 bytes) verificados
encuci2020_bd_dbf [data_raw]: COINCIDE -- sha256 y tamaño (6913684 bytes) verificados
encig2021_csv     [data_raw]: COINCIDE -- sha256 y tamaño (27752363 bytes) verificados
```

Los tres **COINCIDEN** contra `data/manifiesto.yaml` — el microdato 2025 de
ENVIPE (no solo el FD que `§13.5` reportó AUSENTE) está registrado y
coincide con lo que declara el manifiesto. "AUSENTE" de la sesión anterior
era sobre `envipe2025_fd_pdf`/`encuci2020_fd_pdf` en un contexto donde no se
habían buscado los ids del *payload* de datos; esta sesión sí los busca y
los encuentra.

**Pieza de la premisa que NO se sostiene sin matiz — heredada de la primera
ola, re-verificada aquí para los tres instrumentos nuevos:** los seis ejes
de `x` de `canon` §1.1.A (variables de ENIGH) siguen sin estar disponibles
como condicionantes directos. Igual que la primera ola razonó
(`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §0), si el reactivo
de `θ_k` vive en ENVIPE/ENCUCI y el desenlace vive en el mismo instrumento,
los condicionantes deben salir de ese mismo instrumento. Esta sesión usa
las variables análogas que cada instrumento sí trae, declaradas y
verificadas contra su propio diccionario en §1 — **no heredadas de las que
uso ENCIG para salud** (instrucción explícita del encargo).

**Contaminación del instrumento ENVIPE, hallazgo no anticipado por la
plantilla de la primera ola:** la batería `AP5_4` ("¿Cuánta confianza le
inspira...?") **no se aplica a todos los entrevistados** — está condicionada
a `AP5_3_XX` ("de las autoridades que le mencionaré, dígame a cuáles
identifica"), la pregunta de identificación inmediatamente anterior en el
mismo cuestionario (`fd_envipe2025.pdf`, secciones 5.3 y 5.4, contiguas).
Verificado por cruce completo, no supuesto: para `AP5_3_04`/`AP5_4_04`
(Guardia Nacional), de 91 182 casos, **71 742** con `AP5_3_04=1` (identifica)
tienen siempre `AP5_4_04` respondido; **19 323** con `AP5_3_04=2` (no
identifica) tienen siempre `AP5_4_04` en blanco; **117** con `AP5_3_04=9`
(no sabe si identifica) también en blanco. Cruce perfecto — cero
excepciones. Esto **no** es la misma estructura que ENCIG/ENCUCI (donde la
batería de confianza se pregunta directo, sin filtro de identificación
previo): el universo efectivo de cada reactivo `AP5_4_XX` de ENVIPE es
"quienes identifican esa institución", declarado como no-aplicabilidad
estructural (mismo tipo de tratamiento que `AP3_15_4` de ENCUCI para
formalidad — blanco = no aplica, no no-respuesta) — **no** se imputa, no se
trata como universo completo. Ver §1.1-§1.2 para el detalle por
institución (la tasa de identificación varía mucho entre instituciones: de
82.5% para Ejército y 78.7% para Guardia Nacional, hasta 23.7% para la FGR
y 20.2% para Jueces — las once tasas exactas se reportan en §3, no aquí).

---

## 1 · Especificación de la medición — congelada antes de calcular

*Misma regla de la primera ola: nada de lo que sigue se toca después de ver
una tabla de resultados (`canon` §1.1.B, propiedad 3).*

### 1.0 Declaración que decide la pregunta abierta del encargo: ¿un reactivo nombrado o cada uno por separado?

`justicia-policía` trae 7 reactivos ENVIPE y `seguridad-FFAA` trae 4;
`electoral-partidos` trae 4 de ENCUCI. **Decisión: cada reactivo se mide
por separado — no se construye un índice ni un promedio entre
instituciones dentro del componente.** Razón, declarada antes de calcular:

- La primera ola sí construyó un índice para `financiera` (`P11_1_1`-`P11_1_5`),
  pero esos 5 ítems son **repeticiones del mismo escenario hipotético**
  ("si usted tuviera que solicitar los servicios de un banco...") aplicadas
  como batería de un único constructo — un índice ahí agrega repeticiones
  de una sola pregunta, no impone una unidimensionalidad sin verificar.
- Los reactivos de `AP5_4`/`AP5_2`/`AP5_3` son, en cambio, **preguntas
  distintas sobre instituciones nombradas y distintas** (Ejército ≠ Marina
  ≠ Guardia Nacional; Jueces ≠ Fiscalía ≠ Policía Estatal). Promediarlos en
  un índice asumiría una unidimensionalidad de confianza institucional
  entre instituciones heterogéneas que nadie verificó — el mismo error de
  fondo que `canon` §1.1.C prohíbe para condicionantes ("fabricaría una
  conjunta que nadie midió"), aplicado aquí a la variable de desenlace en
  vez de al condicionante.
- Es además la práctica de la propia fuente: INEGI publica ENVIPE
  desagregada por institución ("percepción sobre desempeño institucional"),
  nunca como índice agregado de confianza en "las instituciones de
  seguridad" en conjunto.
- `canon` §1.3 dice *"G1 opera sobre el componente relevante al dominio, no
  sobre un promedio"* — eso prohíbe promediar **entre los seis componentes**
  del vector (salud vs. justicia vs. ...), no decide si promediar **dentro**
  de un componente entre instituciones. Esta nota no resuelve esa pregunta
  por `canon`: la deja **medida por institución, sin colapsar**, y declara
  explícitamente que elegir *cuál* institución (o qué combinación) alimenta
  el escalar único que pide `G1`/`G4` es una decisión de la capa de
  modelado, no de esta sesión de medición — mismo principio de alcance que
  la nota anterior aplicó a la elección de escala.

**Consecuencia declarada:** esta ola entrega más filas por componente que
la primera (una tabla por institución, no una sola), y dos de los tres
componentes (`seguridad-FFAA`, `justicia-policía`) quedan **MEDIDO·PARCIAL(x)
por institución**, no como un único par (proporción, IC) por componente —
hueco de traducción hacia el escalar que el vector de `canon` pide, dejado
anotado, no resuelto aquí (ver §4).

### 1.1 Declaraciones comunes a los tres componentes

- **Tramos de edad:** idénticos a la primera ola — **18–29 · 30–44 · 45–59
  · 60+** — mismo corte declarado, no derivado de los datos.
- **n mínimo por celda para reportar estimación puntual: 30 casos sin
  ponderar**, igual que la primera ola. Por debajo: **SIN SOPORTE**, con su
  `n`.
- **No-respuesta:** excluida de numerador y denominador. En ENVIPE, además
  de `9` (No sabe/no responde), el blanco estructural de `AP5_4_XX` (no
  identifica la institución en `AP5_3_XX`) se excluye por la misma razón
  que `AP3_15_4` de ENCUCI (no-aplicabilidad, no no-respuesta) — declarado
  en §0. En ENCUCI, `5` (No aplica) se trata igual que `9`.
- **Dispersión:** mismo estimador de conglomerado último (UPM/estrato de
  diseño) que la primera ola, reimplementado esta sesión en
  `tests/svystat.py` — el de la primera ola no estaba commiteado y vivía en
  su scratch. Validado en §2 antes de usarse, con el mismo caso conocido.
- **No se invierte forma funcional; no se extrapola a la cola alta A/B**:
  mismas prohibiciones permanentes de `canon` §1.1.C-i, sin excepción.
- **Edad, códigos de tope declarados por instrumento** (verificado contra
  diccionario, no asumido): ENVIPE `EDAD=97` = "97 años o más" (edad real,
  entra a `60+`); `EDAD=98` = "no especificada" (excluida del eje, no
  imputada). ENCUCI `EDAD=96` = "97 y más años" (entra a `60+`); `EDAD∈{97,98,99}`
  = variantes de "no especificada"/"no sabe" (excluidas). Los dos
  instrumentos usan códigos de tope **distintos** para el mismo concepto —
  verificado por instrumento, no heredado del otro.

### 1.2 Seguridad-FFAA — ENVIPE `AP5_4_04` (Guardia Nacional) · `AP5_4_08` (Ejército) · `AP5_4_09` (Fuerza Aérea) · `AP5_4_10` (Marina)

- **Instrumento:** tabla única `conjunto_de_datos_tper_vic1_envipe2025.csv`
  — reactivo, `EDAD`, `DOMINIO`, ponderador `FAC_ELE` y diseño
  `EST_DIS`/`UPM_DIS` viven todos en el mismo registro (`ID_PER` ya es la
  llave de persona; confirmado contra `fd_envipe2025.pdf`, Tabla TPer_Vic1,
  cons. 1-20: no hace falta cruzar con `TSDem`, a diferencia de ENCIG y
  ENCUCI en la primera ola).
- **Escala:** ordinal de 4 (`1` Mucha confianza · `2` Algo de confianza ·
  `3` Algo de desconfianza · `4` Mucha desconfianza), idéntica a la que usó
  ENCIG para salud — verificada contra `fd_envipe2025.pdf` p. 29-31 (cons.
  153, 166, 169, 172) y contra `cuest_principal_envipe2025.pdf` sección
  5.4. `9` No sabe/no responde y blanco (no identifica, `AP5_3_XX≠1`)
  excluidos — ver §0.
- **Dicotomización:** confía = `{1,2}`; no confía = `{3,4}` — mismo corte
  de punto medio que salud/educación en la primera ola.
- **Condicionante primario:** edad (tramos de §1.1). **Formalidad: NO
  DISPONIBLE** — `TPer_Vic1` no trae ninguna variable ocupacional (verificado
  contra las 240 columnas de la tabla; la ocupación vive en otra tabla,
  `TSDem`, y cruzarla no es necesario para el eje que ya se puede armar sin
  join — declarado como límite de alcance, no de disponibilidad del dato en
  otra tabla).
- **Marginal:** urbanización vía `DOMINIO` (`U` Urbano · `C` Complemento
  urbano · `R` Rural) — mismo esquema categórico que usó ENCUCI en la
  primera ola, verificado como variable propia de esta tabla (no heredada).
- **Ponderador:** `FAC_ELE` (factor de expansión de la persona elegida,
  población 18 años y más — coincide con la unidad de análisis: el
  elegido de ENVIPE siempre tiene 18+ por diseño, `EDAD` va de 18 a 98).
- **Base de cada reactivo, declarada por adelantado (no después de
  correr):** el universo de `AP5_4_XX` es "quienes identifican la
  institución" (`AP5_3_XX=1`) — un subconjunto distinto para cada una de
  las cuatro instituciones, no el total de la tabla. Se reporta el `n` de
  identificación junto a cada tabla.

### 1.3 Justicia-policía — ENVIPE `AP5_4_01` (Tránsito) · `AP5_4_02` (Preventiva) · `AP5_4_03` (Estatal) · `AP5_4_05` (Ministerial/Judicial) · `AP5_4_06` (MP y Fiscalías Estatales) · `AP5_4_07` (FGR) · `AP5_4_11` (Jueces)

- **Instrumento, escala, dicotomización, ponderador, base:** idénticos a
  §1.2 — misma tabla `TPer_Vic1`, mismo filtro de identificación previo
  (`AP5_3_01/02/03/05/06/07/11`), mismo `FAC_ELE`/`EST_DIS`/`UPM_DIS`.
- **Condicionante primario:** edad. **Marginal:** `DOMINIO`. Mismas
  ausencias declaradas que §1.2 (formalidad no disponible en esta tabla).

### 1.4 Electoral-partidos — ENCUCI `AP5_2_5` (Partidos políticos) · `AP5_3_6` (Senadores y diputados federales) · `AP5_3_7` (Diputados locales) · `AP5_3_8` (Instituto Nacional Electoral)

- **Instrumento:** tabla `ENCUCI_2020_SEC_4_5` (reactivo, ponderador
  `FAC_SEL`, `DOMINIO`, diseño `EST_DIS`/`UPM_DIS`) unida a `ENCUCI_2020_SD`
  (`EDAD`, `AP3_15_4`) por `UPM`+`VIV_SEL`+`R_SEL`=`N_REN` — **mismo join
  que educación en la primera ola**, reutilizado y re-verificado en esta
  sesión: reprodujo exactamente `n=21519`/`no_respuesta=1483`/`sin_cruce=1265`/
  `útiles=18771` y las ocho celdas de `educación` de la primera ola antes
  de tocar los reactivos nuevos (ver §2, verificación de pipeline).
- **Escala:** ordinal de 4 (`1` Mucha · `2` Algo · `3` Poca · `4` Nada de
  confianza) + `5` No aplica + `9` No sabe/no responde — verificada contra
  `FD_ENCUCI2020.pdf` p. 23-24 (cons. 76, 85-87). Distinta redacción que
  ENVIPE/ENCIG ("poca/nada" vs. "algo/mucha desconfianza") pero mismo
  ordinal de 4 puntos sin categoría neutra — mismo corte de punto medio.
  **A diferencia de ENVIPE, esta batería no tiene filtro de identificación
  previo**: se pregunta directo a todo entrevistado (verificado: no existe
  pregunta `identifica` antes de `AP5_2`/`AP5_3` en el cuestionario ni en
  el diccionario).
- **Dicotomización:** confía = `{1,2}`; no confía = `{3,4}`.
- **Condicionante primario (conjunto):** formalidad (`AP3_15_4`) × edad —
  mismo eje que educación en la primera ola, mismo instrumento, misma
  tabla.
- **Marginal:** `DOMINIO` (urbanización).
- **Ponderador:** `FAC_SEL`.

### 1.5 Lo que esta especificación decide no hacer, declarado

- No se cruza formalidad×edad para `seguridad-FFAA`/`justicia-policía`: no
  disponible en `TPer_Vic1` sin un join a `TSDem` que esta sesión no abre
  (límite de alcance, declarado, no de disponibilidad del dato en otra
  tabla — igual estilo que declaró la primera ola para migración en
  salud/educación).
- No se construye índice ni escalar único por componente (§1.0) — cada
  institución se mide por separado.
- No se compara entre instituciones ni entre componentes (mismo límite que
  la primera ola, mismo motivo: universos y años distintos, comparar sería
  inventar una conjunta no medida).
- No se usa ENCIG como fuente para estos tres componentes en esta ola,
  aunque `§13.1` la cita como candidata para los tres: ENVIPE y ENCUCI ya
  dan reactivo específico con microdato verificado en disco; abrir un
  tercer instrumento por componente sin necesidad sería re-priorizar
  cobertura de la campaña sin instrucción para hacerlo. Declarado, no
  ejecutado.

---

## 2 · El estimador y el pipeline, probados contra casos conocidos

**El estimador.** `tests/svystat.py` de la primera ola no está commiteado —
vivía en el scratch de aquella sesión. Se reimplementó esta sesión en
Python puro (mismo límite de entorno: no hay `numpy`/`scipy` instalados) y
se validó contra el mismo caso degenerado que usó la primera ola (SRS,
pesos uniformes, un conglomerado por observación, n=200, k=80):

```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.
```

Coincide exactamente con lo que reportó la primera ola para el mismo caso
— misma fórmula, misma precisión.

**El pipeline (lector DBF y join).** Esta sesión también reimplementa el
lector de `.dbf` (no hay `dbfread` ni `pandas` instalados) — `tests/dbfmini.py`,
mínimo, Python puro. Antes de tocar los reactivos nuevos de electoral, el
pipeline completo (lector DBF + join `UPM+VIV_SEL+R_SEL=N_REN` + tramos de
edad + estimador) se corrió sobre `AP5_2_6` (educación, primera ola) como
segunda prueba de caso conocido — esta vez con datos reales, no
sintéticos:

```
n_filas=21519 no_respuesta=1483 sin_cruce=1265 utiles=18771
(esperado de la primera ola: n_filas=21519 no_respuesta=1483 sin_cruce=1265 utiles=18771)
  ('Formal', '18-29'): n=1035 p=82.4% se=1.41pp
  ('Formal', '30-44'): n=1855 p=79.6% se=1.45pp
  ('Formal', '45-59'): n=1084 p=79.2% se=1.64pp
  ('Formal', '60+'): n=210 p=85.5% se=2.66pp
  ('Informal', '18-29'): n=1844 p=78.4% se=1.17pp
  ('Informal', '30-44'): n=2657 p=75.1% se=1.15pp
  ('Informal', '45-59'): n=2082 p=67.2% se=1.49pp
  ('Informal', '60+'): n=1185 p=62.0% se=1.88pp
```

Las ocho celdas coinciden con las publicadas en
`forense/notas/2026-08-03-cal-conf-faseb-medicion.md` §3.2 — mismo `n`,
mismo `%` (a la décima), mismo `SE` (a la centésima de punto porcentual).
El primer intento de este pipeline **no** coincidía (`sin_cruce=1163` en
vez de `1265`): el lector de `EDAD` de ENCUCI trataba los códigos `98`
("edad no especificada en 18+") y `99` ("edad no especificada en 14 o
menos") como edades literales ≥60 en vez de excluirlos del eje — corregido
antes de aceptar el pipeline como válido, exactamente el tipo de error que
esta prueba existe para atrapar. El script queda commiteado en
`tests/cal_conf_faseb_ola2.py`, con el assert de esta reproducción como
guardia: si alguien lo vuelve a correr y el pipeline diverge de estos
cuatro números, el script se detiene antes de calcular nada nuevo.

**Ponderadores, verificados por orden de magnitud contra universo
declarado** (suma de la columna de peso sobre toda la tabla, sin ningún
filtro de esta sesión):

| Instrumento | Ponderador | Suma sobre toda la tabla | Universo declarado | ¿Coherente? |
|---|---|---|---|---|
| ENVIPE 2025 | `FAC_ELE` | 95 795 780 | Población 18+ de México (`EDAD` va de 18 a 98 por diseño; el elegido de ENVIPE es siempre adulto) | Sí — del orden de la población adulta nacional 2025, consistente con el 94 221 441 que dio `fac_per` de ENIF 2024 en la primera ola para el mismo universo |
| ENCUCI 2020 | `FAC_SEL` | 96 427 583 (reutilizado de la primera ola — mismo instrumento, mismo ponderador, no se recalculó) | Población 15+ de México | Sí — ya verificado en la primera ola contra Censo 2020 (~97 millones de 15+) |

No es una cifra tecleada: `FAC_ELE` se sumó sobre las 91 182 filas de
`TPer_Vic1` completas, antes de cualquier filtro de identificación o de
edad de esta sesión.

---

## 3 · Resultados por componente

*Todas las tablas: `n` sin ponderar · proporción ponderada · SE por
conglomerado último (`EST_DIS`/`UPM_DIS`, ENVIPE; `EST_DIS`/`UPM_DIS`,
ENCUCI) · IC95%. Celdas con `n<30` → SIN SOPORTE. Ninguna celda de esta
sesión cayó bajo el mínimo — ver nota al final de §3.3.*

### 3.1 Seguridad-FFAA — ENVIPE 2025, `TPer_Vic1` (91 182 filas)

Cada institución mide sobre su propia base: **quienes identifican esa
institución** (`AP5_3_XX=1`) — no el total de la tabla (§0, §1.2).

**Guardia Nacional (`AP5_4_04`).** Identifica: 71 742 (78.7% de la tabla) ·
no identifica/NS: 19 440 · sin respuesta de confianza entre quienes
identifican: 911.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 16 620 | 82.2% | 0.43pp | [81.4%, 83.1%] |
| 30–44 | 23 905 | 80.2% | 0.37pp | [79.5%, 80.9%] |
| 45–59 | 17 659 | 79.6% | 0.43pp | [78.8%, 80.5%] |
| 60+ | 12 352 | 81.8% | 0.51pp | [80.8%, 82.8%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 41 835 | 78.1% | 0.30pp | [77.5%, 78.7%] |
| Complemento urbano | 16 260 | 84.6% | 0.42pp | [83.7%, 85.4%] |
| Rural | 12 736 | 85.6% | 0.48pp | [84.6%, 86.5%] |

**Ejército (`AP5_4_08`).** Identifica: 75 260 (82.5%) · no identifica/NS:
15 922 · sin respuesta: 681.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 16 758 | 88.4% | 0.35pp | [87.8%, 89.1%] |
| 30–44 | 24 444 | 87.8% | 0.30pp | [87.2%, 88.4%] |
| 45–59 | 18 529 | 86.8% | 0.36pp | [86.1%, 87.5%] |
| 60+ | 14 516 | 87.4% | 0.43pp | [86.5%, 88.2%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 44 312 | 85.9% | 0.25pp | [85.4%, 86.4%] |
| Complemento urbano | 16 889 | 89.8% | 0.34pp | [89.1%, 90.5%] |
| Rural | 13 378 | 90.9% | 0.34pp | [90.2%, 91.6%] |

**Fuerza Aérea (`AP5_4_09`).** Identifica: 31 963 (35.1%) — la tasa de
identificación más baja de las cuatro de FFAA · no identifica/NS: 59 219 ·
sin respuesta: 1 410.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 7 814 | 94.3% | 0.35pp | [93.6%, 95.0%] |
| 30–44 | 10 882 | 92.9% | 0.37pp | [92.2%, 93.6%] |
| 45–59 | 7 485 | 91.9% | 0.44pp | [91.0%, 92.7%] |
| 60+ | 4 226 | 92.9% | 0.61pp | [91.7%, 94.1%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 20 085 | 92.4% | 0.28pp | [91.9%, 93.0%] |
| Complemento urbano | 6 328 | 94.3% | 0.51pp | [93.3%, 95.3%] |
| Rural | 4 140 | 94.0% | 0.47pp | [93.1%, 94.9%] |

**Marina (`AP5_4_10`).** Identifica: 56 181 (61.6%) · no identifica/NS:
35 001 · sin respuesta: 958.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 13 169 | 93.6% | 0.30pp | [93.0%, 94.2%] |
| 30–44 | 18 862 | 92.1% | 0.30pp | [91.5%, 92.7%] |
| 45–59 | 13 621 | 91.8% | 0.33pp | [91.1%, 92.4%] |
| 60+ | 9 330 | 93.4% | 0.34pp | [92.7%, 94.0%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 33 718 | 92.0% | 0.22pp | [91.6%, 92.5%] |
| Complemento urbano | 12 365 | 93.8% | 0.34pp | [93.1%, 94.4%] |
| Rural | 9 140 | 93.4% | 0.37pp | [92.7%, 94.1%] |

Todas las celdas de las cuatro instituciones superan el mínimo de 30 —
ninguna SIN SOPORTE. La institución con menor tasa de identificación
(Fuerza Aérea, 35.1%) sigue con miles de casos por celda: el filtro de
identificación reduce la base, no la vuelve frágil, para este componente.

### 3.2 Justicia-policía — ENVIPE 2025, `TPer_Vic1` (misma tabla)

**Policía de Tránsito (`AP5_4_01`).** Identifica: 58 292 (63.9%) · no
identifica/NS: 30 514 · sin respuesta: 414.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 13 933 | 44.6% | 0.58pp | [43.5%, 45.7%] |
| 30–44 | 20 006 | 40.5% | 0.49pp | [39.5%, 41.4%] |
| 45–59 | 14 319 | 42.3% | 0.58pp | [41.2%, 43.4%] |
| 60+ | 9 348 | 49.8% | 0.75pp | [48.3%, 51.3%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 36 765 | 39.6% | 0.38pp | [38.8%, 40.3%] |
| Complemento urbano | 12 607 | 49.1% | 0.71pp | [47.7%, 50.5%] |
| Rural | 8 506 | 53.0% | 0.83pp | [51.4%, 54.7%] |

**Policía Preventiva (`AP5_4_02`).** Identifica: 52 996 (58.1%) · no
identifica/NS: 32 480 · sin respuesta: 324.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 11 290 | 57.5% | 0.66pp | [56.2%, 58.8%] |
| 30–44 | 18 053 | 51.6% | 0.57pp | [50.4%, 52.7%] |
| 45–59 | 13 538 | 51.2% | 0.63pp | [50.0%, 52.4%] |
| 60+ | 9 609 | 60.9% | 0.78pp | [59.4%, 62.4%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 28 349 | 50.7% | 0.49pp | [49.7%, 51.7%] |
| Complemento urbano | 13 658 | 56.7% | 0.70pp | [55.4%, 58.1%] |
| Rural | 10 665 | 62.2% | 0.72pp | [60.8%, 63.6%] |

**Policía Estatal (`AP5_4_03`).** Identifica: 59 383 (65.1%) · no
identifica/NS: 31 799 · sin respuesta: 573.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 14 710 | 61.9% | 0.59pp | [60.8%, 63.1%] |
| 30–44 | 20 452 | 54.9% | 0.49pp | [54.0%, 55.9%] |
| 45–59 | 14 200 | 54.3% | 0.58pp | [53.2%, 55.4%] |
| 60+ | 9 179 | 60.1% | 0.76pp | [58.6%, 61.6%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 35 371 | 53.4% | 0.40pp | [52.6%, 54.2%] |
| Complemento urbano | 13 316 | 62.4% | 0.55pp | [61.4%, 63.5%] |
| Rural | 10 123 | 66.4% | 0.75pp | [64.9%, 67.9%] |

**Policía Ministerial/Judicial/de Investigación (`AP5_4_05`).** Identifica:
29 256 (32.1%) · no identifica/NS: 61 926 · sin respuesta: 517.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 7 116 | 68.9% | 0.78pp | [67.4%, 70.4%] |
| 30–44 | 10 663 | 57.7% | 0.66pp | [56.4%, 59.0%] |
| 45–59 | 7 221 | 55.1% | 0.76pp | [53.6%, 56.6%] |
| 60+ | 3 612 | 58.0% | 1.04pp | [56.0%, 60.1%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 18 292 | 56.5% | 0.53pp | [55.4%, 57.5%] |
| Complemento urbano | 6 214 | 65.2% | 0.84pp | [63.6%, 66.9%] |
| Rural | 4 233 | 70.5% | 1.01pp | [68.5%, 72.5%] |

**Ministerio Público y Fiscalías Estatales (`AP5_4_06`).** Identifica:
30 383 (33.3%) · no identifica/NS: 60 799 · sin respuesta: 442.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 8 116 | 66.3% | 0.77pp | [64.8%, 67.8%] |
| 30–44 | 11 152 | 55.2% | 0.65pp | [53.9%, 56.5%] |
| 45–59 | 7 097 | 52.4% | 0.84pp | [50.8%, 54.1%] |
| 60+ | 3 446 | 52.9% | 1.12pp | [50.7%, 55.1%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 18 895 | 52.3% | 0.54pp | [51.2%, 53.4%] |
| Complemento urbano | 6 671 | 65.4% | 0.88pp | [63.7%, 67.1%] |
| Rural | 4 375 | 71.2% | 0.89pp | [69.4%, 72.9%] |

**Fiscalía General de la República (`AP5_4_07`).** Identifica: 21 611
(23.7%) · no identifica/NS: 69 571 · sin respuesta: 399.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 5 675 | 70.7% | 0.88pp | [69.0%, 72.4%] |
| 30–44 | 7 849 | 63.1% | 0.79pp | [61.5%, 64.6%] |
| 45–59 | 5 113 | 62.5% | 0.93pp | [60.6%, 64.3%] |
| 60+ | 2 479 | 66.4% | 1.23pp | [64.0%, 68.8%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 14 534 | 62.5% | 0.59pp | [61.4%, 63.7%] |
| Complemento urbano | 4 224 | 70.9% | 1.06pp | [68.9%, 73.0%] |
| Rural | 2 454 | 74.8% | 1.20pp | [72.4%, 77.1%] |

**Jueces (`AP5_4_11`).** Identifica: 18 398 (20.2%) — la tasa de
identificación más baja de las once instituciones de FFAA+justicia · no
identifica/NS: 72 784 · sin respuesta: 269.

| Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|
| 18–29 | 5 005 | 61.7% | 0.94pp | [59.8%, 63.5%] |
| 30–44 | 6 358 | 55.6% | 0.91pp | [53.9%, 57.4%] |
| 45–59 | 4 348 | 52.4% | 0.97pp | [50.5%, 54.3%] |
| 60+ | 2 328 | 53.4% | 1.47pp | [50.5%, 56.3%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 12 131 | 52.7% | 0.66pp | [51.4%, 54.0%] |
| Complemento urbano | 3 621 | 63.2% | 1.15pp | [60.9%, 65.4%] |
| Rural | 2 377 | 66.9% | 1.47pp | [64.0%, 69.8%] |

Todas las celdas de las siete instituciones superan el mínimo de 30 — la
celda más pequeña de todo el acto es Jueces × 60+ con 2 328 casos, casi
dos órdenes de magnitud por encima del mínimo.

### 3.3 Electoral-partidos — ENCUCI 2020, `SEC_4_5` (21 519 filas, mismo join que educación en la primera ola)

**Partidos políticos (`AP5_2_5`).** No-respuesta (`5`/`9`): 453 · sin cruce
de edad válido: 1 274 · útiles: 19 792.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 047 | 19.9% | 1.71pp | [16.5%, 23.2%] |
| Formal | 30–44 | 1 865 | 18.8% | 1.30pp | [16.3%, 21.4%] |
| Formal | 45–59 | 1 120 | 16.0% | 1.36pp | [13.4%, 18.7%] |
| Formal | 60+ | 219 | 16.5% | 2.72pp | [11.1%, 21.8%] |
| Informal | 18–29 | 1 893 | 25.2% | 1.55pp | [22.2%, 28.2%] |
| Informal | 30–44 | 2 756 | 20.7% | 1.10pp | [18.5%, 22.8%] |
| Informal | 45–59 | 2 217 | 19.4% | 1.15pp | [17.2%, 21.7%] |
| Informal | 60+ | 1 362 | 24.9% | 1.56pp | [21.8%, 28.0%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 563 | 19.6% | 0.61pp | [18.4%, 20.8%] |
| Complemento urbano | 4 862 | 22.5% | 0.91pp | [20.8%, 24.3%] |
| Rural | 5 367 | 24.1% | 0.98pp | [22.1%, 26.0%] |

**Senadores y diputados federales (`AP5_3_6`).** No-respuesta: 825 · sin
cruce: 1 263 · útiles: 19 431.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 042 | 20.2% | 1.60pp | [17.0%, 23.3%] |
| Formal | 30–44 | 1 865 | 18.1% | 1.35pp | [15.5%, 20.8%] |
| Formal | 45–59 | 1 107 | 22.5% | 1.78pp | [19.0%, 26.0%] |
| Formal | 60+ | 215 | 22.9% | 3.29pp | [16.4%, 29.3%] |
| Informal | 18–29 | 1 891 | 24.3% | 1.37pp | [21.7%, 27.0%] |
| Informal | 30–44 | 2 731 | 22.3% | 1.12pp | [20.1%, 24.5%] |
| Informal | 45–59 | 2 179 | 23.6% | 1.33pp | [21.0%, 26.2%] |
| Informal | 60+ | 1 295 | 23.9% | 1.80pp | [20.4%, 27.5%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 446 | 21.7% | 0.63pp | [20.4%, 22.9%] |
| Complemento urbano | 4 779 | 23.8% | 0.91pp | [22.0%, 25.6%] |
| Rural | 5 206 | 26.2% | 0.98pp | [24.3%, 28.1%] |

**Diputados locales (`AP5_3_7`).** No-respuesta: 854 · sin cruce: 1 267 ·
útiles: 19 398.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 041 | 19.8% | 1.63pp | [16.6%, 23.0%] |
| Formal | 30–44 | 1 862 | 18.3% | 1.34pp | [15.7%, 21.0%] |
| Formal | 45–59 | 1 106 | 21.4% | 1.66pp | [18.2%, 24.7%] |
| Formal | 60+ | 215 | 29.8% | 8.89pp | [12.3%, 47.2%] |
| Informal | 18–29 | 1 885 | 24.7% | 1.36pp | [22.0%, 27.3%] |
| Informal | 30–44 | 2 731 | 20.9% | 1.07pp | [18.8%, 23.0%] |
| Informal | 45–59 | 2 180 | 22.4% | 1.36pp | [19.7%, 25.0%] |
| Informal | 60+ | 1 289 | 22.7% | 1.56pp | [19.6%, 25.7%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 415 | 21.2% | 0.65pp | [20.0%, 22.5%] |
| Complemento urbano | 4 773 | 23.0% | 0.88pp | [21.3%, 24.7%] |
| Rural | 5 210 | 26.2% | 0.95pp | [24.3%, 28.1%] |

⚠️ La celda Formal×60+ (n=215) tiene el SE más grande de todo el acto
(8.89pp, IC95% [12.3%, 47.2%]) — supera el mínimo de 30 por un margen
amplio, pero es, con mucho, la celda más frágil de esta ola: un solo
estrato/UPM con pocos casos formales de edad avanzada domina la varianza.
No es SIN SOPORTE — se reporta tal cual, con su fragilidad declarada, no
suavizada.

**Instituto Nacional Electoral (`AP5_3_8`).** No-respuesta: 391 · sin
cruce: 1 269 · útiles: 19 859.

| Formalidad | Edad | n | % confía | SE | IC95% |
|---|---|---|---|---|---|
| Formal | 18–29 | 1 048 | 63.9% | 1.98pp | [60.0%, 67.8%] |
| Formal | 30–44 | 1 868 | 57.4% | 1.53pp | [54.3%, 60.4%] |
| Formal | 45–59 | 1 123 | 55.4% | 2.32pp | [50.8%, 59.9%] |
| Formal | 60+ | 219 | 54.9% | 5.62pp | [43.8%, 65.9%] |
| Informal | 18–29 | 1 901 | 64.7% | 1.57pp | [61.6%, 67.8%] |
| Informal | 30–44 | 2 768 | 58.5% | 1.37pp | [55.8%, 61.1%] |
| Informal | 45–59 | 2 228 | 57.5% | 1.50pp | [54.5%, 60.4%] |
| Informal | 60+ | 1 362 | 54.6% | 1.92pp | [50.9%, 58.4%] |

| Dominio | n | % confía | SE | IC95% |
|---|---|---|---|---|
| Urbano | 9 591 | 57.7% | 0.79pp | [56.1%, 59.2%] |
| Complemento urbano | 4 877 | 61.7% | 1.06pp | [59.6%, 63.8%] |
| Rural | 5 391 | 62.2% | 1.14pp | [60.0%, 64.5%] |

**Ningún componente, en ningún cruce de esta ola, produjo una celda por
debajo del mínimo de 30.** Igual que la primera ola: consecuencia de
muestras fuente grandes y de limitar el condicionamiento a como mucho dos
ejes cruzados — no un resultado buscado.

**Contraste entre instituciones, declarado explícitamente como NO
comparación causal (§1.5):** dentro de `seguridad-FFAA`, la confianza
puntual va de ~80% (Guardia Nacional/Ejército) a ~92-94% (Fuerza
Aérea/Marina); dentro de `justicia-policía`, de ~40-55% (policías,
Tránsito el más bajo) a ~55-70% (Jueces/FGR/MP, con más incertidumbre por
menor identificación); en `electoral-partidos`, Partidos políticos y el
Congreso rondan 16-30% (los más bajos de todo el acto) mientras el INE
ronda 55-65%. Esto **describe la dispersión que ya observó `canon` §1.1.F
paso 5 (nota de G1a: "Marina 89% vs. partidos 23.9%")** — no la contradice:
los números de esta ola (Marina ~92-94%, Partidos ~16-25%) son del mismo
orden que esa nota anticipó, con metodología distinta (proporción
condicional por edad/dominio, no cifra nacional puntual). Se reporta el
contraste porque es observable en los datos, no porque esta sesión decida
comparar componentes para un juicio causal — la instrucción de §1.5 sigue
vigente: no se calibra un componente contra otro.

---

## 4 · Qué queda MEDIDO, con procedencia — y qué no

| Componente | Estado | Fuente | Año | Variables | Método |
|---|---|---|---|---|---|
| `confianza_institucional[seguridad-FFAA]` | **MEDIDO·PARCIAL(x), por institución** (4 instituciones separadas, no un escalar único; 1 eje conjunto de 6 + 1 marginal) | ENVIPE | 2025 | `AP5_4_04/08/09/10`, cada una condicionada a identificar la institución (`AP5_3_XX=1`) | Proporción ponderada (`FAC_ELE`) + IC95% por conglomerado último (`UPM_DIS`/`EST_DIS`), condicionada a edad; marginal por `DOMINIO` |
| `confianza_institucional[justicia-policía]` | **MEDIDO·PARCIAL(x), por institución** (7 instituciones separadas) | ENVIPE | 2025 | `AP5_4_01/02/03/05/06/07/11`, cada una condicionada a identificar la institución | Ídem |
| `confianza_institucional[electoral-partidos]` | **MEDIDO·PARCIAL(x), por institución** (4 ítems separados; 2 ejes conjuntos + 1 marginal) | ENCUCI | 2020 | `AP5_2_5`, `AP5_3_6/7/8` | Proporción ponderada (`FAC_SEL`) + IC95% por conglomerado último; conjunto formalidad×edad + marginal `DOMINIO` |

**Clase `MEDIDO·PARCIAL(x)` (sellada en `milpa/procedencia.yaml` por el `PR
#51` de la ola anterior) aplica a los tres, con la misma reserva que ya
llevaba salud/educación/financiera:** ninguno cruza los seis ejes de `x`
simultáneamente, y estos tres además no colapsan en un escalar único por
componente (§1.0) — quedan medidos **por institución**, un nivel de
desagregación más fino que salud/educación/financiera, que sí tenían un
solo reactivo (o índice) por componente. Esta nota **no edita**
`milpa/procedencia.yaml` — esa edición es el acto de propagación posterior
que ya usó el `PR #51` para la ola anterior; aquí solo se declara qué
clase correspondería:

- `confianza_institucional[seguridad-FFAA]` → **MEDIDO·PARCIAL(x)**
  (ejes efectivos: edad, dominio — por institución, sin escalar único)
- `confianza_institucional[justicia-policía]` → **MEDIDO·PARCIAL(x)**
  (ejes efectivos: edad, dominio — por institución, sin escalar único)
- `confianza_institucional[electoral-partidos]` → **MEDIDO·PARCIAL(x)**
  (ejes efectivos: formalidad×edad, dominio — por ítem, sin escalar único)

**Hueco de traducción declarado, no resuelto aquí:** `G1`/`G4` de `canon`
§2.2 piden un escalar por componente (`confianza_institucional[justicia]`,
`confianza_institucional[dominio]`); esta ola entrega distribuciones por
institución dentro de cada componente, no un escalar. Qué institución (o
qué combinación) representa el escalar que esos generadores multiplican es
una decisión de la capa de modelado — declarada en §1.0, no tomada aquí.

**Financiera, educación y salud** siguen medidos como reportó la primera
ola — esta nota no los toca ni los recalcula.

**Los ocho parámetros escalares** (`horizonte_temporal`, `radio_confianza`,
`aversion_riesgo`, `sens_estatus`, `deferencia`, `familismo_apoyo`,
`familismo_obligacion`, `exposicion_violencia`) — fuera de alcance, no
tocados.

### 4.1 Auditoría contra `canon` §1.1.B, propiedad por propiedad

- **Propiedad 1 (es una distribución, no una media).** Cumplida: cada celda
  de §3 reporta `n`, proporción ponderada, SE e IC95% — nunca un solo
  número nacional. Ninguna tabla de esta ola colapsa a un punto.
- **Propiedad 2 (la restricción de nivel hogar viaja con la condicional).**
  No aplica ningún conflicto en esta ola: los condicionantes usados —edad
  (persona), formalidad vía `AP3_15_4` (persona, mismo tratamiento que
  educación en la primera ola), `DOMINIO` (UPM/localidad, compartido por
  construcción por todos los miembros de un mismo hogar — no hay manera de
  separar a dos miembros del mismo hogar en esa coordenada porque la
  variable ya vive al nivel de conglomerado, no de persona)— no mezclan
  una coordenada de hogar con una de persona de forma que pudiera partir a
  dos miembros del mismo hogar en ejes contradictorios.
- **Propiedad 3 (la forma funcional no se inventa).** Cumplida por
  construcción: ninguna celda usa suavizado, curva, ni forma paramétrica;
  la decisión de §1.0 (medir cada institución por separado, no un índice)
  es precisamente la aplicación de esta propiedad a la variable de
  desenlace — invertir un índice sin evidencia de unidimensionalidad
  habría sido la forma funcional que esta propiedad prohíbe.

---

## 5 · El contador

**condicionales medidas sobre atributos: 6 de 14**

Los seis son los tres de la primera ola (`confianza_institucional[salud/
educación/financiera]`) más los tres de esta ola
(`confianza_institucional[seguridad-FFAA/justicia-policía/electoral-partidos]`)
— los seis componentes del vector `confianza_institucional` (`canon` §1.3,
6 de 6). Cada uno medido como distribución condicional empírica (no media
puntual), con `n` sin ponderar, estimación ponderada por el factor de
expansión del diseño muestral correspondiente, y dispersión por
conglomerado último, sobre un subconjunto declarado de `x` (nunca los seis
ejes a la vez). Los tres de esta ola, además, quedan medidos **por
institución** dentro del componente, no como escalar único (§1.0, §4) —
matiz que el contador de una sola línea no captura y que esta nota deja
explícito para quien lo propague a `milpa/procedencia.yaml`. Los 8
escalares restantes están fuera de alcance de este acto, no medidos aquí,
y el contador no los infla. `D`=14 derivado en `canon` §1.1.F.
