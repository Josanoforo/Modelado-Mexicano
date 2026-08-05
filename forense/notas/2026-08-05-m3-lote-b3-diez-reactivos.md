Contadores movidos: 0.

# Encargo M-3 — El lote del barrido B-3: diez instrumentos, cero reactivos leídos (hasta hoy)

Sesión Sonnet, Ubuntu con red, worktree nuevo `/home/pc0/mm-encargo-m3-b3-lote`,
rama `sesion/encargo-m3-b3-lote-reactivos` desde `origin/main` = `16d9dbd`
(cabeza de main al arrancar, confirmado ancestro con
`git merge-base --is-ancestor`).

Este acto no produce una medición ni mueve ningún contador de falsación o de
coeficiente — es auditoría documental: abre el descriptor de los diez
instrumentos que Encargo B-3 (`forense/notas/2026-08-04-b3-cierre-barrido-alcanzabilidad.md`)
descargó "sin leer reactivo", y por cada uno busca el reactivo específico que
el manifiesto declaraba como pendiente. El contador es cero y se declara
aquí, no al final.

## 0 · Arranque (Bloque D)

```
$ git fetch origin
(ya al día)
$ git merge-base --is-ancestor 16d9dbd origin/main && echo ancestro
ancestro
$ git worktree add /home/pc0/mm-encargo-m3-b3-lote -b sesion/encargo-m3-b3-lote-reactivos origin/main
error: could not write config file .git/config: Device or resource busy   (x2, transitorio,
mismo patrón ya documentado en B-3 §0 — contención de escritura concurrente
entre sesiones que comparten `.git/`; verificado `git worktree list` y
`git status --branch` desde el nuevo worktree, ambos correctos, sin
corrupción)
$ echo "${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}"
sin_variable
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
200
```

Firma correcta (Ubuntu con red, ADR-59b) — coincide con el entorno asignado
por el encargo. `data/raw` ausente al crear el worktree (como espera Bloque
D), enlazada a `/home/pc0/mm-corpus/raw`.

**Concurrencia derivada:** `gh pr list --state open` → dos PR abiertos, #131
(`b4b-alpha`, toca `data/manifiesto.yaml`/`forense/hallazgos.md`) y #132
(`barrido-publico-17-condiciones-no-existe`, solo toca un archivo de
`forense/notas/`). Verificado por `gh pr diff 131 --name-only` + grep de los
17 ids de manifiesto de este acto: **cero traslape** — PR #131 tocó CLUES,
AGROASEMEX, ESTAD/SESTAD, ENSANUT, ENCIG, ninguno de los diez de este acto.
Traslape esperado y no evitable: ambos actos escriben a `forense/hallazgos.md`
(append-only) — se resuelve en el cierre con el criterio ya establecido
(`origin/main` primero, esta rama después, sin reordenar).

## 1 · Método: dos sub-agentes ("fork"), lectura pura, sin escritura

Declaración de procedencia obligatoria (esta es información nueva de método,
no vista en actos anteriores de este corpus — se declara con detalle
completo). El trabajo de leer diez descriptores (PDF/XLSX/XLS) se dividió en
dos sub-agentes ejecutados en paralelo, cada uno heredando el contexto
completo de esta sesión coordinadora (mismo modelo, mismo hilo de
conversación — no una sesión nueva en frío). Instrucción explícita dada a
ambos: **prohibido editar, `git add`, commit o push de cualquier archivo del
repo; prohibido abrir microdato (ningún ZIP/DBF/CSV de base de datos
extraído o leído); prohibido adivinar URLs de archivo por analogía de
sufijo/año.** Cada uno devolvió su hallazgo como texto a esta sesión, que es
quien escribió `data/manifiesto.yaml` y esta nota — ninguna escritura al
repo ocurrió fuera de esta sesión coordinadora.

**Tratamiento de contaminación (ADR-46):** por el criterio "la unidad de
contaminación es la sesión — su contexto de lectura acumulado", y dado que
ambos sub-agentes heredan y reportan de vuelta al mismo contexto de
conversación, esta nota declara la contaminación de estructura de **ambas
mitades como propia de esta sesión**, sin intentar separar "lo que leyó el
fork A" de "lo que leyó el fork B" — declarar de más, no de menos (ver §5).

**Herramientas:** `pdftotext -layout` (PDF), `openpyxl` (XLSX, ya
disponible), `xlrd` para el único `.xls` legado (ELCOS) — instalado vía
`pip install --target <scratchpad>/pylibs xlrd` + `PYTHONPATH`, sin tocar
paquetes de sistema (el entorno es Python 3.14 externally-managed; se evitó
`--break-system-packages`).

## 2 · Tabla instrumento × constructo × ¿reactivo?

Tres categorías, nunca colapsadas: **EXISTE** (variable + redacción literal)
· **NO EXISTE** (descriptor completo revisado, ausente) · **NO ALCANZA**
(no hay documento que abrir, o el documento no trae redacción completa —
nunca se resolvió abriendo microdato).

| Instrumento | Constructo | ¿Reactivo? | Variable / razón |
|---|---|---|---|
| ENBIARE 2021 | `familismo_apoyo` | **EXISTE** (parcial) | `PB2_1` (Apartado B): *"¿considera usted que siempre contará con la ayuda de personas de su familia?"* + `PC1_1`/`PC1_5` (Apartado C, conducta de cuidado/visita a familiares) |
| ENBIARE 2021 | `familismo_obligacion` | **NO EXISTE** | Descriptor completo (10 apartados) revisado; cero ítem de creencia de deber/sacrificio familiar |
| ENASIC 2022 | `familismo_apoyo` | **EXISTE** | `P4_2_1`/`P4_2_2` (Sección 4): cuidado intrahogar efectivamente ejercido |
| ENASIC 2022 | `familismo_obligacion` | **EXISTE** — mejor candidato (a) del lote | Sección 7 "Percepción cultural de los cuidados", batería Likert `P7_12_1`-`P7_12_8`: *"Cuidar a las personas del hogar es solo su responsabilidad"*, *"se debe enseñar... que su deber es cuidar a los padres, cónyuge, hijas e hijos"* |
| ENSU 2025 | `confianza_institucional[seguridad]` | **NO ALCANZA** | Sin documento: FD soft-404 reproducible en 5 ediciones (4 de B-3 + 2025 reconfirmado vía listado JSON de 268 títulos); ningún título "Cuestionario" en ese listado |
| ENSU 2025 | `exposicion_violencia` | **NO ALCANZA** | Misma razón |
| ELCOS 2012 | R2.1 (jerarquía→deferencia/iniciativa) | **NO EXISTE** | Hoja "Mujer elegida" íntegra (1312 filas, Secc. IV-X); cero iniciativa/disenso/reporte de errores/canal anónimo |
| ELCOS 2012 | R2.2 (liderazgo benévolo→lealtad) | **EXISTE**, proxy estrecho | `P7_25`/`P8_8`: jefe "comprensivo" ante necesidad personal/familiar — mide solo conciliación trabajo-familia, corte transversal individual, sin rotación/desempeño pareado; **no satisface el falsador** de R2.2 tal como está escrito |
| ELCOS 2012 | R10.2 (retro pública/privada→rotación) | **NO EXISTE** | Cero retroalimentación/evaluación de desempeño/rotación voluntaria en toda la hoja |
| ENFIH 2019 | R1.2 (planeación larga) | **EXISTE** | `P9_10`/`P9_11A` (Afore + aportación voluntaria), `P9_12_1` (seguro de vida), `P9_12_7` (plan privado de retiro), `P5_12` (crédito hipotecario) |
| ENFIH 2019 | R1.4 (consumo compensatorio, prima de marca) | **NO EXISTE** | 16 hojas revisadas íntegras; cero ítem de elección de marca |
| ENSAFI 2023 | `aversion_riesgo` | **NO ALCANZA** | Sin documento: portal SPA sin listado estático, WebFetch solo recupera `<title>` |
| ENSAFI 2023 | `horizonte_temporal` | **NO ALCANZA** | Misma razón |
| ENSAFI 2023 | R1.3 (canal de confianza→adopción) | **NO ALCANZA** | Misma razón |
| ENPOL 2021 | R10.3 ("ver, oír y callar") | **EXISTE**, universo no coincidente | `P8_4`/`P8_5` (Secc. VIII, corrupción interna del Centro): *"¿denunció ante alguna autoridad?"* / razón de no denunciar, opción *"por miedo a represalias, incluso jurídicas"* — mecanismo real, pero universo es corrupción sufrida por la propia persona privada de la libertad, no testigo de delito en población general |
| ENTI 2022 | (sin constructo asignado) | — | Revisado trabajo/negocio familiar no remunerado: es economía informal, no la creencia normativa de `familismo_obligacion`/`familismo_apoyo`; sin candidato forzado |
| EDER 2025 | R4.1 — **diseño** (panel/evento fechado) | **EXISTE** | Tabla `HISTORIAVIDA` indexada por `anio_retro`/`edad_retro` — **contradice la premisa vigente del manifiesto** ("hoy NO EXISTE ninguna con diseño panel/evento fechado"); ver §4 |
| EDER 2025 | R4.1 — reactivo específico (adulto, padecimiento leve→farmacia) | **NO EXISTE** | Sección Salud solo trae año de inicio de padecimiento (`*_a`), no lugar de atención |
| EDER 2025 | R4.1 — candidato adyacente | **EXISTE**, universo distinto | `hij_ate_N`: *"¿En dónde fue atendido el parto de (NOMBRE)?"*, opción **"07 — Consultorio de una farmacia"**, fechado vía `hij_vid_N` — es parto, no automedicación por padecimiento leve |
| EDR 2024 | (sin constructo asignado) | **NO ALCANZA** | Sin documento descriptivo alguno accesible (ya cerrado por B-3: 43 archivos listados, ninguno "Descriptor de archivos"; este acto además probó el portal, SPA sin listado estático) |

## 3 · Módulos por instrumento (del propio descriptor, listado completo)

- **ENBIARE 2021** (`enbiare_2021_fd.pdf`, 4 tablas): `TVIVIENDA` (vivienda, hogares en la vivienda, servicio doméstico) · `THOGAR`/`TSDEM` (sociodemográficas) · `TENBIARE` — Apartado A Bienestar subjetivo · B Confianza y redes de apoyo · C Uso del tiempo y redes · D Salud · E Fuerza de trabajo · F Eventos y situaciones · G Participación social y comunitaria · H Aspectos biográficos · I Movilidad intergeneracional · J Estratificación.
- **ENASIC 2022** (`enasic_2022_fd.xlsx`, 6 hojas): `TVIVIENDA`, `THOGAR`, `TCSDemPO`, `TPOB_CUI` (Secc. 1-7, culmina en "Percepción cultural de los cuidados"), `THOG_UNIP`, `TPER_ELE`.
- **ENSU 2025**: sin descriptor accesible.
- **ELCOS 2012** (`elcos_fd.xls`, 7 hojas): `Vivienda`, `Hogar`, `Residente`, `Mujer elegida` (Secc. IV Apoyo y cuidado a integrantes del hogar · V Apoyo y cuidado a otros hogares · VI Decisiones en el hogar · VII Contexto laboral · VIII Caracterización del último trabajo · IX Satisfacción en el trabajo · X Expectativas laborales), + 3 hojas de catálogos de codificación.
- **ENFIH 2019** (`enfih_2019_fd.xlsx`, 16 hojas): `TVivienda`, `THogar`, `TSDem`, `TModulo` (Secc. 4a Características personales · 5 Segundas propiedades · 6 Negocios y activos no financieros · 7 Vehículos y crédito automotriz · 8 Deudas no hipotecarias · 9 Activos financieros, seguros y pensiones · 10 Otros ingresos · 11 Imprevistos y percepción de carga financiera · 12 Exclusivo entrevistador), + 9 hojas derivadas/auxiliares.
- **ENSAFI 2023**: sin descriptor accesible.
- **ENPOL 2021** (`fd_enpol2021.pdf`, 7 tablas): `ENPOL2021_SOC` (I. Sociodemográfico) · `ENPOL2021_2_3` (II-III. Antecedentes y detención) · `ENPOL2021_4` (IV. Estancia en Ministerio Público) · `ENPOL2021_5` (V. Proceso jurídico) · `ENPOL2021_6` (VI. Condiciones de vida en el Centro) · `ENPOL2021_7` (VII. Vida intracarcelaria) · `ENPOL2021_8_9_10_11` (VIII-XI. Corrupción interna, antecedentes jurídicos/penales/familiares, expectativas de salida, condición de entrevista).
- **ENTI 2022** (`enti_2022_fd.pdf`, 7 tablas): Vivienda · Hogar · Sociodemográfico · Ocupación y empleo parte I · parte II · Cuestionario básico 5-11 años · Cuestionario básico 12-17 años.
- **EDER 2025** (`eder2025_descripcion_bd.pdf`, 8 tablas): Vivienda · Hogar · Persona · Informante (sociodemo/ocupacional/satisfacción con la vida) · `Historiavida` (longitudinal, `anio_retro`/`edad_retro`) · Salud (discapacidad, autopercepción, padecimientos crónicos fechados) · Antecedentes (familiares, uniones, hijos) · Doméstico.
- **EDR 2024**: sin descriptor accesible.

## 4 · Hallazgo fuera de perímetro: EDER 2025 contradice la premisa de diseño de R4.1

El encargo (y el manifiesto vigente antes de este acto) afirmaba que "hoy NO
EXISTE ninguna fuente con diseño panel/evento fechado" para R4.1. La tabla
`HISTORIAVIDA` de EDER 2025 indexa eventos por `anio_retro`/`edad_retro` —
es, estructuralmente, diseño de evento fechado. Esto **no cierra R4.1**: el
reactivo específico que el falsador necesita (adulto sin IMSS con
padecimiento leve que elige farmacia-con-consultorio, antes/después de una
mejora de acceso público) **no existe** en la Sección Salud de EDER (solo
año de inicio del padecimiento, no lugar de atención). Lo que sí cambia es
la premisa de diseño — declarado aquí para que la adjudicación de mesa lo
tenga a la vista; **esta sesión no adjudica si R4.1 se reabre**, eso excede
su perímetro.

## 5 · Declaración ADR-46 (contaminación de estructura, declarar de más)

**Descriptores abiertos íntegros** (nunca microdato): `enbiare_2021_fd.pdf`,
`enasic_2022_fd.xlsx`, `elcos_fd.xls`, `enfih_2019_fd.xlsx`,
`fd_enpol2021.pdf`, `enti_2022_fd.pdf`, `eder2025_descripcion_bd.pdf` — los
7 ya presentes en `data/raw`, ningún byte nuevo descargado.

**URLs consultadas sin descarga de archivo nuevo** (solo metadatos de
listado / portal, ningún endpoint no declarado por la propia API):
- `https://www.inegi.org.mx/app/api/.../archivoscompaginacion?idBiinegi=1127...` (ENSU, listado JSON completo, 268 títulos, tipodocto=0 único válido)
- `https://www.inegi.org.mx/programas/ensu/` (SPA, sin contenido)
- `https://www.inegi.org.mx/programas/ensafi/2023/` (SPA, sin contenido)
- `https://www.inegi.org.mx/programas/edr/` (SPA, sin contenido)
- Una prueba de endpoint `archivoscompaginacion` para EDR con `idBiinegi` ya
  conocido (no un parámetro inventado) — soft-404 conocido, no se insistió.

**Cero apertura de microdato.** Ningún `.zip`/`.csv`/`.dbf` de base de datos
de los diez instrumentos fue extraído, abierto ni leído como texto en
ningún momento del acto — verificado por ambos sub-agentes y por esta
sesión coordinadora antes de escribir esta nota.

**Contaminación parcial declarada (ADR-46-2/3):** esta sesión queda
**parcialmente contaminada para pre-registrar** contra ENBIARE 2021, ENASIC
2022, ELCOS 2012, ENFIH 2019, ENPOL 2021, ENTI 2022 y EDER 2025 (estructura
de descriptor leída a nivel de variable/pregunta) — y, en un grado menor
(solo metadatos de listado, sin redacción de reactivo), contra ENSU 2025 y
ENSAFI 2023. **No contaminada respecto a EDR 2024** (solo portal vacío, cero
información de estructura ganada). No se tocó ningún host ni fuente fuera
de los diez de este acto.

## 6 · Prioridad del lote (ELCOS 2012 / EDER 2025) — resultado

El encargo marcó estos dos como el mayor rendimiento posible, por ser la
clase de fuente que tres filas del cruce declaran inexistente. Resultado:

- **ELCOS 2012** — la premisa "ninguna clase trae encuesta de clima
  organizacional" **se sostiene en lo esencial**: dos de tres R-codes (R2.1,
  R10.2) NO EXISTEN; el tercero (R2.2) tiene solo un proxy de un eje
  (conciliación trabajo-familia), no clima organizacional en sentido amplio,
  y no alcanza el diseño pareado que el falsador exige.
- **EDER 2025** — la premisa de diseño **no se sostiene**: sí hay evento
  fechado (`HISTORIAVIDA`). El reactivo específico de R4.1 sigue sin existir,
  pero la razón por la que estaba cerrado ("ninguna con ese diseño") queda
  desactualizada — ver §4.

## 7 · Suite

```
$ python3 tests/check.py --baseline
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Idéntico al resultado de B-3 (misma línea base, mismo HEAD congelado) — este
acto no introdujo ningún FAIL/WARN nuevo.

## Prohibiciones respetadas

No se adivinó ninguna URL de *archivo* por analogía de sufijo/año — todas
las rutas consultadas salieron de un enlace/API ya declarado por el propio
servidor, o son archivos ya presentes en `data/raw` desde B-3. No se abrió
ningún ZIP/CSV/DBF de base de datos de los diez instrumentos. No se editó
`canon/`, `milpa/`, `tests/` ni `forense/hitoD-preregistro`. No se
re-clasificó ninguna ficha del Hito D ni se tocó `canon/gobernanza`/`conf.06`
(ADR-52 sigue vigente sin tocar). No se adjudicó si R4.1 se reabre (§4) ni
si `familismo_obligacion` pasa de (b) a (a) con la batería de ENASIC (§2) —
ambas quedan para mesa. Los dos sub-agentes usados como método de este acto
no escribieron ningún archivo del repo — toda la escritura la hizo esta
sesión coordinadora, declarada en §1.
