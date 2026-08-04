# Bitácora de sesión

*(Generado por `tests/bitacora.py --cierra`, protocolo §2. No se edita a mano salvo las dos líneas declaradas en cada bloque.)*

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `canon/verde-y-t17` · **HEAD inicial (origin/main):** `24df4b31434d70db0122a7ddb41ada0579a462cb` · **HEAD final:** `7dd1c5a77b4a911a992d09788c1a8e79f463cd31`

**Commits de la sesión:**
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)

**Archivos tocados:**
```
.gitignore                                         |  15 ++
 canon/cola.yaml                                    |  75 ++++++
 canon/estado-programa-v1_9.md                      |   6 +-
 canon/{gobernanza-v1_10.md => gobernanza-v1_11.md} |  22 +-
 canon/protocolo-sesion-v1_0.md                     | 107 ++++++++
 forense/historico/TRANSFER-maestra-9.md            | 188 ++++++++++++++
 tests/baseline.json                                |   9 +-
 tests/bitacora.py                                  | 270 +++++++++++++++++++++
 tests/check.py                                     | 106 +++++---
 9 files changed, 750 insertions(+), 48 deletions(-)
```

**ADRs añadidos:** ADR-42, ADR-43
**Líneas de versión modificadas en canon/:** 2
  - ### `gobernanza` · **v1.11** · 29 de julio de 2026 · **43 ADR**
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: 18 FAIL · 81 WARN (congelados en origin/main)
  - Después: 19 FAIL · 82 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-01, D-02, D-03, D-04, E-01, I-01, I-02, I-03
  - Cerrados: (ninguno)

**Qué se decidió:** Se cerró el gate de T17 (deuda congelada en tests/baseline.json, hitoD-preregistro:8 NO se edita) y se aterrizó protocolo-sesion-v1_0, canon/cola.yaml y tests/bitacora.py -- primera vez que el protocolo de apertura/cierre existe en archivo, no solo en dos documentos tipo (3).
**Qué quedó bloqueado:** R3.1 y R3.4 siguen sin ficha -- bloqueadas por D-04 (qué modelo genera el baseline LLM) hasta que se decida. P3 de TRANSFER-9 (4 de 5 'decisiones que requieren firma') sigue sin poder derivarse: el documento nombra la #1 y dice 'las otras cuatro' sin listarlas.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `canon/verde-y-t17` · **HEAD inicial (origin/main):** `24df4b31434d70db0122a7ddb41ada0579a462cb` · **HEAD final:** `b73d1dd9077b1a807aacc8fc061e509d9dc995a6`

**Commits de la sesión:**
  - `b73d1dd` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · cierre del gate (segunda vuelta): bucket propio TRANSFER-9, estado sincronizado, cola +2
  - `c6dd7ee` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: primer bloque de cierre + fix de bitacora.py --cierra
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)

**Archivos tocados:**
```
.gitignore                                         |  15 ++
 canon/cola.yaml                                    |  93 +++++++
 canon/estado-programa-v1_9.md                      |   8 +-
 canon/{gobernanza-v1_10.md => gobernanza-v1_11.md} |  22 +-
 canon/protocolo-sesion-v1_0.md                     | 107 ++++++++
 forense/bitacora.md                                |  46 ++++
 forense/historico/TRANSFER-maestra-9.md            | 188 ++++++++++++++
 tests/baseline.json                                |  18 +-
 tests/bitacora.py                                  | 276 +++++++++++++++++++++
 tests/check.py                                     | 109 +++++---
 10 files changed, 833 insertions(+), 49 deletions(-)
```

**ADRs añadidos:** ADR-42, ADR-43
**Líneas de versión modificadas en canon/:** 2
  - ### `gobernanza` · **v1.11** · 29 de julio de 2026 · **43 ADR**
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: 18 FAIL · 81 WARN (congelados en origin/main)
  - Después: 19 FAIL · 84 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: C-01, D-01, D-02, D-03, D-04, E-01, I-01, I-02, I-03, I-04
  - Cerrados: (ninguno)

**Qué se decidió:** Se resolvió el ROJO que quedó pendiente: TRANSFER-9 disparaba T03 al citarse a sí mismo como ejemplo del falso positivo -v3.2.md/-v3_2.md -- bucket propio en check.py, estado sincronizado, un solo --freeze. Se registraron dos entradas más de cola (C-01, I-04) sin abrirlas.
**Qué quedó bloqueado:** C-01 (aterrizar TRANSFER-maestra-siguiente.md) no se abre hoy -- queda en cola. Los ocho pendientes de la sesión anterior (D-01..D-04, E-01, I-01..I-03) siguen todos abiertos, ninguno se tocó.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/refreeze-baseline-pr1-4zha5w` · **HEAD inicial (origin/main):** `22a7d9dcce2156557bbf70a164cee7679730faf1` · **HEAD final:** `84aaae39f3120a60cf52c726d2804fac0495f14f`

**Commits de la sesión:**
  - `84aaae3` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · cola: I-01 sube a casos=2 — el refreeze post-PR #1 como evidencia para A1
  - `78288a2` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · estado: declaración vigente de la suite a la corrida real (19 FAIL · 87 WARN)
  - `74027d5` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · Refreeze de línea base tras el merge del PR #1 (main 22a7d9d)
  - `a0ae0ad` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · check.py: buckets propios para las 3 entradas del refreeze post-PR #1

**Archivos tocados:**
```
canon/cola.yaml               |  4 ++--
 canon/estado-programa-v1_9.md |  4 ++--
 tests/baseline.json           | 20 +++++++++++++++++---
 tests/check.py                | 24 ++++++++++++++++++++++--
 4 files changed, 43 insertions(+), 9 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 19 FAIL · 83 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: (ninguno)
  - Cerrados: (ninguno)

**Qué se decidió:** Re-congelar la línea base tras el merge del PR #1 (main 22a7d9d): un solo --freeze con bucket propio para las 3 entradas nuevas (1 T03 de revision-publicacion-2026-07-30.md — cita ilustrativa del artefacto LICENSE-CORPUS, descartado por D-05, patrón I-01 — y 2 T16 que son su consecuencia aritmética); declaración vigente de estado a la corrida real que T16 reporta (19 FAIL · 87 WARN); I-01 sube a casos=2 con este caso como evidencia para A1; el borrado de la rama fusionada del PR #1 se intentó y quedó bloqueado (línea siguiente).
**Qué quedó bloqueado:** El borrado remoto de claude/psicologia-mexicano-publication-review-h5h6ic — verificada fusionada (ahead 0, ancestro de main en 22a7d9d), pero el proxy git del entorno devuelve 403 a todo push que borre refs y el MCP de GitHub no expone borrado de ramas; queda para la UI de GitHub o un clon local. Fuera de eso, nada nuevo: A1 (la marca explícita en T03 que distinga mención de referencia) sigue en la cola como I-01, ahora con 2 casos; ningún otro pendiente se abrió ni se tocó.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/f2-f4-portada-adr-7fjpln` · **HEAD inicial (origin/main):** `25abb8390ae0281242c1c2f18e880db56a6e1445` · **HEAD final:** `bdb1b775aa2c15aa637180782a5d553dac6d24b0`

**Commits de la sesión:**
  - `bdb1b77` · Claude · cola: F7.b y F6/T-README entran a la cola, sin abrirlas
  - `2d1d866` · Claude · gobernanza: v1.11 -> v1.12 -- ADR-44 (publicación del repositorio sin ADR previo)
  - `856639c` · Claude · README: corrige README:40 contra el registro de veredictos archivados

**Archivos tocados:**
```
AUTHORSHIP.md                                      |  2 +-
 README.md                                          |  6 ++---
 canon/cola.yaml                                    | 18 +++++++++++++++
 canon/estado-programa-v1_9.md                      |  4 ++--
 canon/{gobernanza-v1_11.md => gobernanza-v1_12.md} | 26 +++++++++++++++++-----
 5 files changed, 44 insertions(+), 12 deletions(-)
```

**ADRs añadidos:** ADR-44
**Líneas de versión modificadas en canon/:** 1
  - ### `gobernanza` · **v1.12** · 30 de julio de 2026 · **44 ADR**

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: I-05, I-06
  - Cerrados: (ninguno)

**Qué se decidió:** F2/F4 del plan maestro: portada y ADR, nada de instrumento. README:40 corregido contra el registro append-only de veredictos (2 de 27, R1.1 → D · R3.2 → B, no 1 de 27 con B mal atribuido a R1.1); Falsos positivos conocidos fechado 30/jul con T03/T10 re-derivados (21/65). ADR-44 sellado en gobernanza (v1.11 -> v1.12): registra retroactivamente la publicación del repo sin ADR previo, capa legal verificada en el árbol (a), re-examen de deuda v2.2 referido a revision-publicacion-2026-07-30.md sin reabrirlo (b), README-sin-test declarado PENDIENTE/F6 (c), regla hacia adelante contra lector interno asumido (d). F7.b y F6/T-README entraron a cola.yaml (I-05, I-06) sin abrirse. check.py --baseline se mantuvo verde en 19 FAIL · 87 WARN durante toda la sesión, ninguna edición fue para callar un test.
**Qué quedó bloqueado:** Ninguno de los cinco encargos se bloqueó. T-README (F6) y A1..A5 quedaron deliberadamente sin tocar por regla de sesión -- solo se registraron en cola/ADR-44(c), no se implementaron. La fila 1.10/1.11 de la bitácora de versiones de gobernanza sigue faltante (mismo hueco que censo-integridad C5-03 para 1.9); se documentó como límite conocido en la fila 1.12 en vez de reconstruirla, para no abrir un pendiente fuera de encargo.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/f2-f4-portada-adr-7fjpln` · **HEAD inicial (origin/main):** `25abb8390ae0281242c1c2f18e880db56a6e1445` · **HEAD final:** `a5286548ed1c08eacef47d2d1a8ed4fdcc35d6f1`

**Commits de la sesión:**
  - `a528654` · Claude · cola: D-05 -- "prueba de falsación corrida" sin referente único, escalado a mesa
  - `46e9cef` · Claude · bitácora: bloque de cierre de la sesión F2/F4 (portada, ADR-44)
  - `bdb1b77` · Claude · cola: F7.b y F6/T-README entran a la cola, sin abrirlas
  - `2d1d866` · Claude · gobernanza: v1.11 -> v1.12 -- ADR-44 (publicación del repositorio sin ADR previo)
  - `856639c` · Claude · README: corrige README:40 contra el registro de veredictos archivados

**Archivos tocados:**
```
AUTHORSHIP.md                                      |  2 +-
 README.md                                          |  6 ++--
 canon/cola.yaml                                    | 36 ++++++++++++++++++++++
 canon/estado-programa-v1_9.md                      |  4 +--
 canon/{gobernanza-v1_11.md => gobernanza-v1_12.md} | 26 ++++++++++++----
 forense/bitacora.md                                | 36 ++++++++++++++++++++++
 6 files changed, 98 insertions(+), 12 deletions(-)
```

**ADRs añadidos:** ADR-44
**Líneas de versión modificadas en canon/:** 1
  - ### `gobernanza` · **v1.12** · 30 de julio de 2026 · **44 ADR**

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-05, I-05, I-06, I-07
  - Cerrados: (ninguno)

**Qué se decidió:** Propagación de F2: al intentar llevar la corrección de README:40 (2 de 27, R1.1 → D · R3.2 → B) al canon, el barrido encontró que 5 líneas (estado-programa:93/:118, modelo-decision:46/:390, gobernanza:359) invocan 'prueba de falsación corrida' sin referente único -- tres poblaciones distintas (Hito D/27 reglas, Hito C/7 generadores, ejercicio suelto de glosario sobre G1a fechado 27/jul) mezcladas sin marca, más una autocontradicción de modelo-decision consigo mismo (línea 164 dice G1a sin falsar, línea 390 describe una corrida con veredicto B que es inconfundiblemente sobre G1a). No se editó ninguna de las 5 líneas -- se escaló a mesa por decisión del usuario. Se registró D-05 (decisión, con toda la evidencia y qué población invoca cada línea) e I-07 (patrón de proceso: el encargo nombró un archivo, no una afirmación, y el defecto sobrevivió en el canon -- mismo patrón que ADR-29 un piso más arriba). README:40 queda como estaba, corregido y verificado: no menciona generadores ni G1a, solo la población inequívoca del bloque append-only. check.py --baseline se mantuvo verde (19 FAIL · 87 WARN) durante toda la sesión.
**Qué quedó bloqueado:** Las 5 líneas ambiguas del canon (estado-programa:93/:118, modelo-decision:46/:390, gobernanza:359) quedan sin corregir a propósito: D-05 las registra pero no las resuelve, es decisión de mesa. I-07 (test candidato: ninguna afirmación de conteo de veredictos fuera del bloque append-only sin derivarse de él) queda bloqueado por D-05 -- no se puede escribir el test hasta decidir qué poblaciones distingue.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/falsacion-vocabulary-zfjvr4` · **HEAD inicial (origin/main):** `9301e59203b01243e76fe2de47eaad93667a9514` · **HEAD final:** `adb3e62010316ae37c7b31e3b796b28c4cbbe8c9`

**Commits de la sesión:**
  - `adb3e62` · Claude · D-05: fija el vocabulario de "prueba de falsación" (ADR-45)
  - `584f806` · Josanoforo · Merge pull request #3 from Josanoforo/claude/f2-f4-portada-adr-7fjpln
  - `7d92f5b` · Claude · bitácora: bloque de cierre — escalada de D-05, sesión F2/F4 completa
  - `a528654` · Claude · cola: D-05 -- "prueba de falsación corrida" sin referente único, escalado a mesa
  - `46e9cef` · Claude · bitácora: bloque de cierre de la sesión F2/F4 (portada, ADR-44)
  - `bdb1b77` · Claude · cola: F7.b y F6/T-README entran a la cola, sin abrirlas
  - `2d1d866` · Claude · gobernanza: v1.11 -> v1.12 -- ADR-44 (publicación del repositorio sin ADR previo)
  - `856639c` · Claude · README: corrige README:40 contra el registro de veredictos archivados
  - `25abb83` · Josanoforo · Merge pull request #2 from Josanoforo/claude/refreeze-baseline-pr1-4zha5w
  - `1ee9f29` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: el borrado de la rama del PR #1 quedó bloqueado, no hecho
  - `902ab75` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: bloque de cierre del refreeze post-PR #1
  - `84aaae3` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · cola: I-01 sube a casos=2 — el refreeze post-PR #1 como evidencia para A1
  - `78288a2` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · estado: declaración vigente de la suite a la corrida real (19 FAIL · 87 WARN)
  - `74027d5` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · Refreeze de línea base tras el merge del PR #1 (main 22a7d9d)
  - `a0ae0ad` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · check.py: buckets propios para las 3 entradas del refreeze post-PR #1
  - `22a7d9d` · Josanoforo · Merge pull request #1 from Josanoforo/claude/psicologia-mexicano-publication-review-h5h6ic
  - `f4bef94` · Josanoforo · Nota de reconciliación: LICENSE-CORPUS.md descartado (D-05)
  - `10239cd` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · revisión estratégica de publicación (propuesta sin sello, ADR-39 aplicado al encargo)
  - `4e174dd` · Josanoforo · Add files via upload
  - `7fa7481` · Josanoforo · Delete USO-ACEPTABLE.md
  - `83db9c9` · Josanoforo · Delete CITATION.cff
  - `5fab073` · Josanoforo · Delete AVISO-DE-ALCANCE.md
  - `29f08b4` · Josanoforo · Delete LICENSE
  - `a946db5` · Josanoforo · Delete AUTHORSHIP.md
  - `acd65af` · Josanoforo · Add files via upload
  - `fb1f333` · Josanoforo · Add files via upload
  - `c3adff8` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: segundo bloque de cierre
  - `b73d1dd` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · cierre del gate (segunda vuelta): bucket propio TRANSFER-9, estado sincronizado, cola +2
  - `c6dd7ee` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: primer bloque de cierre + fix de bitacora.py --cierra
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)
  - `24df4b3` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD: adenda 1 a CAL-G3 -- desenlace primario a cuatro estados con molde ENIF
  - `c9e67bd` · Jonas · co: Claude Fable 5 <noreply@anthropic.com> · hitoD: ficha CAL-G3 -- pre-registro de estimación propia de coeficiente de generador
  - `015af3a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T03 exime citas de renombre; --freeze con conteo derivado (18 FAIL · 82 WARN)
  - `2bf50b2` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.9 -> v1.10 -- ADR-41 (reglas de sesión sin archivo, autoría del repo)
  - `c68feab` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · instrucciones-proyecto-v2.md: v2 -> v2.2 -- procedencia documental y hallazgos de Hito D
  - `afa7c7f` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD-R3.2: veredicto B -- gate inalcanzable por construcción, escala no valor
  - `771ea26` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T18 T-PASO2-EJECUCION -- veredictos en bloque designado (ADR-40)
  - `d26cfde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: newest() por versión no lexicográfico; T17 asevera unicidad
  - `de3f22a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · estado: consolida declaración canónica de cobertura del pre-registro (§4·S2)
  - `1a56210` · Claude · co: Claude <noreply@anthropic.com> · tests: T17 T-FICHAS-COUNT -- declarado en estado == encabezados ## R reales
  - `90eb140` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: revierte prefijo de ruta en 3 citas (T03 no las ve); documenta el hueco
  - `b28b144` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: ficha de R3.2, pre-registrada antes de abrir ENCIG
  - `9fb8473` · Claude · co: Claude <noreply@anthropic.com> · tests: T14/T15/T16 -- convierte en test 4 de las 7 cifras que quedaron a mano
  - `e3d483b` · Claude · co: Claude <noreply@anthropic.com> · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `c377b97` · Claude · co: Claude <noreply@anthropic.com> · tests/baseline.json: congela 18 FAIL / 82 WARN tras la sesion de correcciones
  - `31fff96` · Claude · co: Claude <noreply@anthropic.com> · Censo de integridad: corrige causa raiz A/C, casos B/D/F, mueve documentos muertos, incorpora ADR-38/39
  - `f320550` · Claude · CI: usa el modo linea base en vez de check.py sin banderas
  - `3375a28` · Claude · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `26e7ef4` · Claude · T03: normaliza punto/guion bajo, declara historicos, congela linea base P1
  - `69357d4` · Claude · Censo v1.1: procedencia por commit, denominador eb92d99/9efa61f, cadena del caso pelon
  - `9dbff7a` · Claude · Anade censo-integridad-v1_0: auditoria mecanica completa de canon/ y forense/
  - `9efa61f` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Corrige rotulo del perimetro del Hito D + registro congelado de IDs
  - `eb92d99` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-8.md: cierre de sesion del 29/jul
  - `8254fde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-7.md: documento de traspaso, estaba fuera del repo
  - `7d6535e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · estado v1.8: corrige "cubre las 27" y registra la auditoria de perimetro
  - `a79227e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Nota forense: verificacion del perimetro y cobertura del pre-registro

**Archivos tocados:**
```
.github/workflows/verify.yml                       |   4 +-
 .gitignore                                         |  16 +
 AUTHORSHIP.md                                      |  84 +++
 AVISO-DE-ALCANCE.md                                | 106 ++++
 CITATION.cff                                       |  35 ++
 CONTRIBUTING.md                                    |  12 +-
 LICENSE                                            |  65 +++
 README.md                                          |   6 +-
 USO-ACEPTABLE.md                                   |  92 +++
 canon/cola.yaml                                    | 130 +++++
 ...do-programa-v1_7.md => estado-programa-v1_9.md} |  52 +-
 canon/glosario-v5_6.md                             |   6 +-
 canon/{gobernanza-v1_8.md => gobernanza-v1_13.md}  | 120 +++-
 canon/integrador-psicologia-mexicano.md            |   4 +-
 ...lo-decision-v3_2.md => modelo-decision-v3_4.md} |  94 ++-
 canon/protocolo-sesion-v1_0.md                     | 107 ++++
 ...ayer_of_Decisions__Environment_and_Structure.md |   2 +
 ...ucation_and_Information_as_Decision_Behavior.md |   2 +
 data/manifiesto.yaml                               |  43 ++
 forense/bitacora.md                                | 201 +++++++
 forense/censo-integridad-v1_0.md                   | 313 ++++++++++
 forense/censo-integridad-v1_1.md                   | 156 +++++
 forense/historico/TRANSFER-maestra-7.md            | 169 ++++++
 forense/historico/TRANSFER-maestra-8.md            | 210 +++++++
 forense/historico/TRANSFER-maestra-9.md            | 188 ++++++
 forense/hitoD-R3_2-veredicto-v1_0.md               | 136 +++++
 forense/hitoD-preregistro-v2_0.md                  | 205 +++++++
 forense/notas/2026-07-29-b-correccion-perimetro.md | 217 +++++++
 .../notas/2026-07-29-c-correccion-curaduria-66.md  |  30 +
 forense/notas/2026-07-29-d-bloqueo-encig.md        |  52 ++
 instrucciones-proyecto-v2.md                       |  24 +-
 milpa/milpa-plan-v0_1.md                           |   2 +-
 milpa/procedencia.yaml                             |   7 +-
 revision-publicacion-2026-07-30.md                 | 463 +++++++++++++++
 tests/baseline.json                                | 448 +++++++++++++++
 tests/bitacora.py                                  | 276 +++++++++
 tests/check.py                                     | 631 ++++++++++++++++++++-
 tests/validador_registro_ids.py                    | 242 ++++++++
 38 files changed, 4894 insertions(+), 56 deletions(-)
```

**ADRs añadidos:** ADR-38, ADR-39, ADR-40, ADR-41, ADR-42, ADR-43, ADR-44, ADR-45
**Líneas de versión modificadas en canon/:** 4
  - ### `estado` · **v1.9** · 29 de julio de 2026 · **ÚNICA FUENTE DE ESTADO**
  - ### `gobernanza` · **v1.13** · 30 de julio de 2026 · **45 ADR**
  - ### `modelo` · **v3.4** · CANÓNICO OPERATIVO
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: (tests/baseline.json no existía en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: C-01, D-01, D-02, D-03, D-04, D-05, E-01, I-01, I-02, I-03, I-04, I-05, I-06, I-07
  - Cerrados: (ninguno)

**Qué se decidió:** D-05: vocabulario fijo de 'prueba de falsación' (ADR-45) — denominador 27/49 siempre etiquetado, veredicto D cuenta como corrida, Hito D/Hito C/ejercicio de glosario se reportan como tres poblaciones separadas. Cierra D-05 en cola.yaml.
**Qué quedó bloqueado:** I-07 sigue abierta: sigue siendo un patrón de proceso sin test.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/manifiesto-registra-verifica` · **HEAD inicial (origin/main):** `584f806f7a8ffb9c714dc8f6b3196d4c1ddea91b` · **HEAD final:** `b65f44fc8abf0e1d111eb232231a8611ee704b80`

**Commits de la sesión:**
  - `b65f44f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: tests/manifiesto.py — --registra y --verifica de procedencia de datos

**Archivos tocados:**
```
canon/cola.yaml      |  32 +++++++
 data/manifiesto.yaml |  27 ++++++
 tests/manifiesto.py  | 243 +++++++++++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 302 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-06, E-02, I-08
  - Cerrados: (ninguno)

**Qué se decidió:** C1 resuelto: tests/manifiesto.py (--registra/--verifica, stdlib+PyYAML) verifica encig23_base_datos_csv.zip (COINCIDE, sha256 recomputado independiente del original) y reporta AUSENTE -no error- para el PDF que ya no está en data/raw/. Prueba negativa de dos lados corrida contra una copia temporal (ADR-40.c): payload íntegro pasa, un byte alterado falla (exit 1). Esquema de manifiesto.yaml ampliado con archivo (I-08, cerrada mismo commit) y entorno_descarga (derivado, no pedido por parámetro). ENNViH/MxFLS registrada como dominio público con fuente verificada 30/jul -- D-06 cerrada (C2 del plan maestro era premisa falsa). E-02 registra el alcance de la contaminación de esa verificación (CO/RG/DH nuevas para esa sesión).
**Qué quedó bloqueado:** Nada bloqueado por este trabajo. I-04 sigue abierta a propósito -- cubre artefactos que el chat entrega en general (TRANSFER-*.md), alcance distinto al de este script, que solo verifica payloads de data/raw/.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/manifiesto-registra-verifica` · **HEAD inicial (origin/main):** `4054c35a4ea549d42b676a9552024e75daad980b` · **HEAD final:** `5a9263d9df487ba4c8bc016ec54659106245b1cf`

**Commits de la sesión:**
  - `5a9263d` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: declara desvío de alcance y el hueco de --contrasta
  - `beac5eb` · Josanoforo · Merge origin/main (PR #4: D-05/ADR-45) into C1
  - `7f9fd96` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre de la sesión C1 (manifiesto.py)
  - `b65f44f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: tests/manifiesto.py — --registra y --verifica de procedencia de datos

**Archivos tocados:**
```
canon/cola.yaml      |  53 +++++++++++
 data/manifiesto.yaml |  27 ++++++
 forense/bitacora.md  |  31 ++++++
 tests/manifiesto.py  | 263 +++++++++++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 374 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-06, D-07, E-02, I-08, I-09
  - Cerrados: D-05

**Qué se decidió:** Resueltos los 3 pendientes de revisión de PR #5 (C1): (1) merge con origin/main (PR #4, D-05/ADR-45) resuelto conservando ambos lados en cola.yaml y bitacora.md en orden cronológico -- verificado por conteo de líneas (201 base + 31 mías + 128 de PR#4 = 360) y por unicidad de IDs de cola; D-05 queda cerrada, D-06/E-02/I-08 intactas. (2) Desvío de alcance declarado en el docstring de tests/manifiesto.py y en cola (D-07, cerrada): --registra no descarga desde --url-origen como pedía el encargo, registra un payload ya en data/raw/ -- defendible, pero no estaba declarado. (3) I-09 registra el hueco que eso abre: falta un modo --contrasta que compare un payload nuevo contra una entrada existente sin sobreescribirla (COINCIDE/DISCREPANCIA); no se implementa en esta sesión, queda pendiente a propósito.
**Qué quedó bloqueado:** Nada bloqueado. I-09 (--contrasta) queda abierta deliberadamente -- es la única forma de correr la prueba que se había anticipado (bajar encig23_estructura_base_datos.pdf y contrastarlo contra la entrada ya registrada), pero implementarla ahora alargaría este PR.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/hitod-perimetro-compara` · **HEAD inicial (origin/main):** `dc5fd0fb20137d802af2c6ab4cc0ea6cd13241e0` · **HEAD final:** `feaf38e745c739e30ef225cebae52b49b9f1d701`

**Commits de la sesión:**
  - `feaf38e` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1 (parcial, Pasos 1-3): perímetro de red, tabla de fuentes, --compara

**Archivos tocados:**
```
canon/cola.yaml     |  3 ++-
 tests/manifiesto.py | 76 ++++++++++++++++++++++++++++++++++++++++++++++++-----
 2 files changed, 72 insertions(+), 7 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: (ninguno)
  - Cerrados: D-05, D-06, D-07, I-08, I-09

**Qué se decidió:** Fase 1 de Hito D, Pasos 1-3 (parcial, PR marcado explícitamente como incompleto): (1) perímetro de red de los 6 hosts del encargo medido y diagnosticado por clase (inegi/ennvih alcanzables; banxico.org.mx sin registro A/AAAA en el apex -- www sí resuelve --, amucss.org.mx NXDOMAIN, ambos confirmados vía consulta DNS cruda a 8.8.8.8 y 1.1.1.1; cnbv.gob.mx y datos.gob.mx con cadena TLS incompleta, confirmado con openssl s_client propio). (2) Tabla ficha->fuente->alcanzable derivada de las 25 fichas de hitoD-preregistro-v2_0.md, reportada en el PR -- se detiene ahí, la tanda de descarga (Paso 4) espera aprobación explícita de esa tabla en un turno posterior. (3) I-09 cerrada: --compara en tests/manifiesto.py, con prueba negativa de dos lados verificada.
**Qué quedó bloqueado:** Paso 4 (la tanda de descarga real) bloqueado a propósito -- el encargo exige tabla aprobada antes de bajar nada, y esa aprobación es de un turno posterior a este PR.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/hitod-perimetro-compara` · **HEAD inicial (origin/main):** `dc5fd0fb20137d802af2c6ab4cc0ea6cd13241e0` · **HEAD final:** `33b412f2656d68482bf99e76bd7f70d23730fc6c`

**Commits de la sesión:**
  - `33b412f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · manifiesto.py: pliegue '>' con ancho en vez de literal '|' sin envolver
  - `ce3c284` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1, Paso 4 (ampliación): serie completa de ENCIG/ENIF/ENVIPE/ENIGH
  - `d0d9e07` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — Hito D Fase 1, Pasos 1-3
  - `feaf38e` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1 (parcial, Pasos 1-3): perímetro de red, tabla de fuentes, --compara

**Archivos tocados:**
```
canon/cola.yaml      |  12 ++
 data/manifiesto.yaml | 445 ++++++++++++++++++++++++++++++++++++++++++++++-----
 forense/bitacora.md  |  30 ++++
 tests/manifiesto.py  |  92 ++++++++++-
 4 files changed, 527 insertions(+), 52 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: E-03
  - Cerrados: D-05, D-06, D-07, I-08, I-09

**Qué se decidió:** Ampliación del Paso 4 (Hito D Fase 1), decisión de mesa del autor: se bajó la serie completa disponible de ENCIG (2015/2017/2019/2021/2023-datosabiertos, más la 2023-microdatos ya existente) y de toda encuesta de la tanda con varias ediciones -- ENIF (2018/2021/2024), ENVIPE (serie completa 2018-2025, 8/8), ENIGH nueva-construcción (2012/2014/2016/2018/2020/2022). Lista real derivada de inegi.org.mx, no del encargo (título de página real vs 'Página no encontrada'; Content-Type/Content-Length de un zip real vs el shell de 2263 bytes). encig2023_datosabiertos_csv resultó DISCREPANCIA (--compara) contra la entrada ya existente encig23_base_datos_csv -- dos paquetes distintos de la misma edición, registrados por separado, sin fusionar. ENUT/ENCUCI/ENSANUT: nada se descargó -- las tres existen pero ninguna edición expuso enlace estático sin forzar un mecanismo (SPA/formulario); registradas como 'requiere navegador', no 'no existe' (corolario 2). E-03 declara el alcance exacto de inhabilitación de esta máquina para pre-registrar: R3.1/R1.2/R7.2/R5.1 quedan inhabilitadas (ENCIG/ENIF/ENVIPE/ENIGH); R5.2/R8.3/R4.2 (ENUT/ENCUCI/ENSANUT) NO, porque nada se tocó de esas fuentes. De paso, se corrigió un defecto de legibilidad propio en tests/manifiesto.py: el presentador de YAML volvía literal cualquier prosa que --registra reescribiera, aplastando párrafos ya envueltos a mano en una sola línea -- corregido a plegado con ancho, contenido verificado idéntico.
**Qué quedó bloqueado:** Nada de esta ampliación quedó bloqueado -- todo lo que el sitio de INEGI exponía por script se bajó y registró. Lo que sigue fuera del alcance de esta máquina: ENUT/ENCUCI/ENSANUT (requieren navegador o ingeniería del formulario de ENSANUT, no forzado por directiva), y R3.4/Banxico (fuera de esta ampliación, sigue bloqueada por ADR-37).

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/e03-session-contamination-xb1y55` · **HEAD inicial (origin/main):** `5b7113a17daa5e83d01f1a28f1c9d344e3df12cf` · **HEAD final:** `f8a9962d52929eca579fc0bff175371b31814005`

**Commits de la sesión:**
  - `f8a9962` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.13 -> v1.14 -- ADR-46 (unidad de contaminación es la sesión, no la máquina)

**Archivos tocados:**
```
canon/cola.yaml                                    | 69 +++++++++++++++++++++-
 canon/estado-programa-v1_9.md                      |  4 +-
 canon/{gobernanza-v1_13.md => gobernanza-v1_14.md} | 34 +++++++++--
 3 files changed, 99 insertions(+), 8 deletions(-)
```

**ADRs añadidos:** ADR-46
**Líneas de versión modificadas en canon/:** 1
  - ### `gobernanza` · **v1.14** · 30 de julio de 2026 · **46 ADR**

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: E-04, E-05
  - Cerrados: D-05, D-06, D-07, I-08, I-09

**Qué se decidió:** ADR-46: unidad de contaminación es LA SESIÓN, no la máquina ni el modelo, corrige cola.yaml E-03. Dos niveles (descarga ciega / exploración de estructura) y condición verificable de lectura reemplazan la prohibición de hardware. Aplicado al registro del 30/jul: ninguna encuesta de la tanda fue descarga ciega; ENUT/ENCUCI/ENSANUT (declaradas libres en el E-03 original) también tuvieron exploración de estructura sin descarga. E-02 verificada, sin el mismo defecto. cola.yaml E-04: la corrección la ejecutó una sesión distinta de la que bajó los datos, deliberado. cola.yaml E-05: --compara mostró que ENCIG 2023 datos-abiertos (26MB) y microdatos (38MB) son productos distintos; R3.2 se midió contra el de 38MB, no cambia el veredicto.
**Qué quedó bloqueado:** Nada bloqueado por esta corrección. I-07 y demás pendientes de instrumento no tocados -- fuera de alcance de este encargo (solo canon/cola.yaml y canon/gobernanza-v*.md/estado-programa-v*.md, sin tocar data/raw/, instrumento ni fichas).

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `sesion/encuci` · **HEAD inicial (origin/main):** `5b7113a17daa5e83d01f1a28f1c9d344e3df12cf` · **HEAD final:** `5b7113a17daa5e83d01f1a28f1c9d344e3df12cf`

**Commits de la sesión:** (HEAD == origin/main — nada nuevo que listar)

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-08, E-04 (renumerada a E-06 al fusionar con PR #8/ADR-46, que ya había tomado E-04/E-05 -- ver cola.yaml E-06)
  - Cerrados: D-05, D-06, D-07, I-08, I-09

**Qué se decidió:** Registro de dos paquetes de ENCUCI 2020 (BD_ENCUCI2020_dbf.zip, FD_ENCUCI2020.pdf) bajados por navegador por el autor desde la pestaña Microdatos de inegi.org.mx/programas/encuci/2020/; copiados sin renombrar a data/raw/ y registrados con tests/manifiesto.py --registra (ids encuci2020_bd_dbf, encuci2020_fd_pdf). Corregida la entrada hitoD_fase1_ediciones_requieren_navegador: ENCUCI 2020 deja de estar pendiente; ENUT corrige premisa -- el portal expone 5 ediciones (2002/2009/2014/2019/2024) con base+descriptor+diagrama entidad-relación, ninguna descargada todavía (D-08, mismo patrón que D-06/regla v2.2). Declarado en cola.yaml (E-04, renumerada a E-06 al resolver este merge) el criterio corregido de contaminación de esta sesión: descarga ciega (registrar payload ya bajado por humano, sin tocar la red) vs exploración de estructura (E-02/E-03); R8.3 (ENCUCI) queda inhabilitada por el hecho consumado del registro, R5.2 (ENUT) no, porque nada se descargó de ella esta sesión.
**Qué quedó bloqueado:** ENUT: cinco ediciones confirmadas alcanzables por el autor, ninguna descargada -- queda para otra sesión. ENSANUT: otra sesión la está bajando por script, en curso, no se espera aquí. Se detectó en el checkout un commit ajeno concurrente (rama sesion/calg3, CAL-G3 Fase A, ENNViH) -- no se tocó; esta sesión creó su propia rama sesion/encuci desde origin/main para no mezclarlo.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `sesion/calg3` · **HEAD inicial (origin/main):** `5b7113a17daa5e83d01f1a28f1c9d344e3df12cf` · **HEAD final:** `981c1ea5b7084775e601b5cc659f8c63ecee1fed`

**Commits de la sesión:**
  - `981c1ea` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3: chequeo CAL-X del punto 9a, previo a abrir microdatos
  - `686e377` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3 Fase A: descarga y registro de las tres olas de ENNViH/MxFLS

**Archivos tocados:**
```
data/manifiesto.yaml | 524 +++++++++++++++++++++++++++++++++++++++++++++++++++
 tests/calx_g3.py     | 209 ++++++++++++++++++++
 2 files changed, 733 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-09, D-10, I-10
  - Cerrados: D-05, D-06, D-07, I-08, I-09

**Qué se decidió:** CAL-G3 Fases A y B, sin estimar nada. FASE A: 27 paquetes de ENNViH/MxFLS (tres olas completas: hogar, localidad, ponderadores, codebooks, cuestionarios, guías) descargados de ennvih-mxfls.org y registrados con manifiesto.py --registra, sha256 derivado; --verifica COINCIDE en las 27. FASE B, solo documentación, ningún .dta abierto: (1) las 11 categorías de CRH01 son idénticas en las tres olas y estaban TODAS anticipadas por Adenda 1 (c) -- nada que escalar; 'Apartado' es segunda celda muerta (n=1/1/0) además de la tanda-sola ya declarada caída. (2) CHEQUEO CAL-X del punto 9a (tests/calx_g3.py, solo codebook): CAL-A y CAL-B alcanzables (RR>=1.5 solo exige p<=66.67% contra base de 7-10%, holgura 7x-9x; el modo de falla de R3.2 no se repite), pero CAL-C y 9b NO ALCANZABLES POR CONSTRUCCION -- exigen precisión, no nivel: 1,981 hogares por brazo (3,962 con el contraste) contra un techo duro de 1,457 discordantes, mejor IC95%sup alcanzable 1.445 contra el <1.25 requerido, SE(log RR) disponible 0.1877 contra 0.1139 necesario; la cota es generosa (traslape cero, sin atrición, sin exclusión de EE.UU., sin cambio de formalidad del jefe). El criterio puede CONFIRMAR G3 pero no puede REFUTARLO. (3) La premisa 'el módulo TB es idéntico en las tres olas' es FALSA: 8 opciones en 2002, 9 en 2005, 11 en 2009, y la ola 1 carece de 'Ninguna de las anteriores'; cat3 2002=6,044 vs cat3+cat9 2005=5,570 vs cat3 sola 2005=1,772 (-71%) -- un jefe sin cambio real se codifica informal en 2002 y sale del contraste en 2005; el instrumento fabrica las transiciones con las que el diseño identifica. (4) El confundidor 5 NO está resuelto en la ola 3: el módulo OC está en el codebook de las olas 1-2 y solo en el cuestionario de la ola 3; el FAQ del proyecto declara que hay preguntas no publicadas por confidencialidad -- un cuestionario documenta lo preguntado, el codebook lo liberado. Registrado en Nota 8 del pre-registro (append-only, antes del bloque de emisiones, sin tocar cuerpo/Nota 7/Adenda 1) y en cola.yaml D-09, D-10 (decisiones de mesa, NO resueltas aquí) e I-10 (colisión de IDs 'D-06', registrada sin abrir). Corregida cola.yaml D-06 con nota fechada sin borrar el original: la cita de la portada estaba truncada -- el registro de usuario EXISTE y está publicado, lo verificado es que NO ESTA APLICADO en /assets/ (200 sin sesión); no es lo mismo. Recogidos a forense/notas/ dos .md producidos por la sesión de ENSANUT, con procedencia declarada y sin editar el cuerpo.
**Qué quedó bloqueado:** FASE C de CAL-G3, no corrida a propósito: bloqueada por D-09 y D-10, ambas decisiones de mesa. Estimar contra un criterio que solo admite confirmación produciría un CAL-A o CAL-B que no significaría lo que aparenta. milpa/procedencia.yaml NO se tocó (la ficha lo prohíbe: ninguna de sus cuatro clases admite una estimación propia). Nota 7 y Adenda 1 NO se editaron. Ningún veredicto emitido: CAL-G3 no aparece en el bloque de emisiones. Pendiente de resolver por la mesa, sin recomendación de esta sesión: qué se hace con CAL-C/9b (tres opciones listadas en D-09) y cómo se armoniza la exposición entre olas (dos opciones en D-10). I-10 queda registrada, no abierta, por instrucción explícita. Conflicto de merge previsto y aceptado con sesion/encuci: ambas ramas salen de 5b7113a y tocan data/manifiesto.yaml y canon/cola.yaml, ambos append-only por convención -- se resuelve conservando ambos lados en orden cronológico, como en PR #4.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/siete-hallazgos-cola-86sj9r` · **HEAD inicial (origin/main):** `64a5d7bdb30f44d307a838f96f7536471a87c3c8` · **HEAD final:** `64a5d7bdb30f44d307a838f96f7536471a87c3c8`

**Commits de la sesión:** (HEAD == origin/main — nada nuevo que listar)

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: I-11, I-12, I-13, I-14, I-15
  - Cerrados: D-05, D-06, D-07, D-08, E-04, E-05, E-06, I-08, I-09

**Qué se decidió:** Registrados 5 hallazgos operativos en cola.yaml (I-11..I-15) traídos de memoria de sesión del 30/jul, cada uno con evidencia verificable en PR #9, PR #10 y/o el propio repo (canon/gobernanza-v1_14.md, canon/cola.yaml E-06): worktree por sesión de escritura, colisión de asignación concurrente de IDs, resolver append-only exige conteo Y contenido, residuo de worktree que el sandbox no borra, y gobernanza declarando una versión de cuerpo distinta de su nombre de archivo. Ninguna se resolvió -- registrarlas es el entregable.
**Qué quedó bloqueado:** Dos de los siete hallazgos del encargo NO se escribieron: (1) 'mover el checkout compartido a main al terminar' -- no se encontró evidencia verificable en el repo de que la sesión de CAL-G3 lo hiciera deliberadamente (ni en PR #9/#10 ni en forense/bitacora.md); solo el reflog de este contenedor, que es ambiguo (indistinguible de aprovisionamiento normal). (2) el valor 'registrado' en cola.yaml -- ya está íntegramente documentado en la nota_estado de I-10 (colisión de IDs D-06), incluida la petición de ratificación de mesa; no se duplica.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/sellar-d09-d10-adr-mncope` · **HEAD inicial (origin/main):** `9301e59203b01243e76fe2de47eaad93667a9514` · **HEAD final:** `d391f58b7d08c2e298506c69b3365bb77dd5047e`

**Commits de la sesión:**
  - `d391f58` · Josanoforo · Merge pull request #12 from Josanoforo/sesion/calg3-poder
  - `58f8a54` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3: aritmética de poder sobre el panel completo — apilar dos transiciones no mueve CAL-C
  - `1868045` · Josanoforo · Merge pull request #11 from Josanoforo/claude/siete-hallazgos-cola-86sj9r
  - `16af08a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · cola: registra cinco hallazgos operativos de la jornada del 30/jul (I-11..I-15)
  - `64a5d7b` · Josanoforo · Merge pull request #10 from Josanoforo/sesion/calg3
  - `4a58320` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · Merge origin/main (PR #8 ADR-46, PR #9 ENCUCI) into sesion/calg3
  - `6b54d7c` · Josanoforo · Merge pull request #9 from Josanoforo/sesion/encuci
  - `dcbf6ec` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Merge origin/main (PR #8, ADR-46) into sesion/encuci
  - `7847920` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3 Fase B: chequeo CAL-X, dos premisas falsas y el confundidor 5 sin cerrar
  - `981c1ea` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3: chequeo CAL-X del punto 9a, previo a abrir microdatos
  - `11d9415` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · ENCUCI 2020: registro de BD/FD bajados por navegador; corrige premisa de ENUT/ENCUCI
  - `686e377` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3 Fase A: descarga y registro de las tres olas de ENNViH/MxFLS
  - `0817817` · Josanoforo · Merge pull request #8 from Josanoforo/claude/e03-session-contamination-xb1y55
  - `85f608a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre -- ADR-46 (unidad de contaminación es la sesión)
  - `f8a9962` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.13 -> v1.14 -- ADR-46 (unidad de contaminación es la sesión, no la máquina)
  - `5b7113a` · Josanoforo · Merge pull request #7 from Josanoforo/claude/hitod-perimetro-compara
  - `82b0961` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — Hito D Fase 1, Paso 4 (ampliación)
  - `33b412f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · manifiesto.py: pliegue '>' con ancho en vez de literal '|' sin envolver
  - `ce3c284` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1, Paso 4 (ampliación): serie completa de ENCIG/ENIF/ENVIPE/ENIGH
  - `45be175` · Josanoforo · Merge pull request #6 from Josanoforo/claude/hitod-perimetro-compara
  - `d0d9e07` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — Hito D Fase 1, Pasos 1-3
  - `feaf38e` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1 (parcial, Pasos 1-3): perímetro de red, tabla de fuentes, --compara
  - `dc5fd0f` · Josanoforo · Merge pull request #5 from Josanoforo/claude/manifiesto-registra-verifica
  - `095a2a2` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — resolución de conflictos, D-07, I-09
  - `5a9263d` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: declara desvío de alcance y el hueco de --contrasta
  - `beac5eb` · Josanoforo · Merge origin/main (PR #4: D-05/ADR-45) into C1
  - `7f9fd96` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre de la sesión C1 (manifiesto.py)
  - `b65f44f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: tests/manifiesto.py — --registra y --verifica de procedencia de datos
  - `4054c35` · Josanoforo · Merge pull request #4 from Josanoforo/claude/falsacion-vocabulary-zfjvr4
  - `a217d32` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · bitacora: cierre de sesión D-05/ADR-45
  - `adb3e62` · Claude · D-05: fija el vocabulario de "prueba de falsación" (ADR-45)
  - `584f806` · Josanoforo · Merge pull request #3 from Josanoforo/claude/f2-f4-portada-adr-7fjpln
  - `7d92f5b` · Claude · bitácora: bloque de cierre — escalada de D-05, sesión F2/F4 completa
  - `a528654` · Claude · cola: D-05 -- "prueba de falsación corrida" sin referente único, escalado a mesa
  - `46e9cef` · Claude · bitácora: bloque de cierre de la sesión F2/F4 (portada, ADR-44)
  - `bdb1b77` · Claude · cola: F7.b y F6/T-README entran a la cola, sin abrirlas
  - `2d1d866` · Claude · gobernanza: v1.11 -> v1.12 -- ADR-44 (publicación del repositorio sin ADR previo)
  - `856639c` · Claude · README: corrige README:40 contra el registro de veredictos archivados
  - `25abb83` · Josanoforo · Merge pull request #2 from Josanoforo/claude/refreeze-baseline-pr1-4zha5w
  - `1ee9f29` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: el borrado de la rama del PR #1 quedó bloqueado, no hecho
  - `902ab75` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: bloque de cierre del refreeze post-PR #1
  - `84aaae3` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · cola: I-01 sube a casos=2 — el refreeze post-PR #1 como evidencia para A1
  - `78288a2` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · estado: declaración vigente de la suite a la corrida real (19 FAIL · 87 WARN)
  - `74027d5` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · Refreeze de línea base tras el merge del PR #1 (main 22a7d9d)
  - `a0ae0ad` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · check.py: buckets propios para las 3 entradas del refreeze post-PR #1
  - `22a7d9d` · Josanoforo · Merge pull request #1 from Josanoforo/claude/psicologia-mexicano-publication-review-h5h6ic
  - `f4bef94` · Josanoforo · Nota de reconciliación: LICENSE-CORPUS.md descartado (D-05)
  - `10239cd` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · revisión estratégica de publicación (propuesta sin sello, ADR-39 aplicado al encargo)
  - `4e174dd` · Josanoforo · Add files via upload
  - `7fa7481` · Josanoforo · Delete USO-ACEPTABLE.md
  - `83db9c9` · Josanoforo · Delete CITATION.cff
  - `5fab073` · Josanoforo · Delete AVISO-DE-ALCANCE.md
  - `29f08b4` · Josanoforo · Delete LICENSE
  - `a946db5` · Josanoforo · Delete AUTHORSHIP.md
  - `acd65af` · Josanoforo · Add files via upload
  - `fb1f333` · Josanoforo · Add files via upload
  - `c3adff8` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: segundo bloque de cierre
  - `b73d1dd` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · cierre del gate (segunda vuelta): bucket propio TRANSFER-9, estado sincronizado, cola +2
  - `c6dd7ee` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: primer bloque de cierre + fix de bitacora.py --cierra
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)
  - `24df4b3` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD: adenda 1 a CAL-G3 -- desenlace primario a cuatro estados con molde ENIF
  - `c9e67bd` · Jonas · co: Claude Fable 5 <noreply@anthropic.com> · hitoD: ficha CAL-G3 -- pre-registro de estimación propia de coeficiente de generador
  - `015af3a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T03 exime citas de renombre; --freeze con conteo derivado (18 FAIL · 82 WARN)
  - `2bf50b2` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.9 -> v1.10 -- ADR-41 (reglas de sesión sin archivo, autoría del repo)
  - `c68feab` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · instrucciones-proyecto-v2.md: v2 -> v2.2 -- procedencia documental y hallazgos de Hito D
  - `afa7c7f` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD-R3.2: veredicto B -- gate inalcanzable por construcción, escala no valor
  - `771ea26` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T18 T-PASO2-EJECUCION -- veredictos en bloque designado (ADR-40)
  - `d26cfde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: newest() por versión no lexicográfico; T17 asevera unicidad
  - `de3f22a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · estado: consolida declaración canónica de cobertura del pre-registro (§4·S2)
  - `1a56210` · Claude · co: Claude <noreply@anthropic.com> · tests: T17 T-FICHAS-COUNT -- declarado en estado == encabezados ## R reales
  - `90eb140` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: revierte prefijo de ruta en 3 citas (T03 no las ve); documenta el hueco
  - `b28b144` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: ficha de R3.2, pre-registrada antes de abrir ENCIG
  - `9fb8473` · Claude · co: Claude <noreply@anthropic.com> · tests: T14/T15/T16 -- convierte en test 4 de las 7 cifras que quedaron a mano
  - `e3d483b` · Claude · co: Claude <noreply@anthropic.com> · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `c377b97` · Claude · co: Claude <noreply@anthropic.com> · tests/baseline.json: congela 18 FAIL / 82 WARN tras la sesion de correcciones
  - `31fff96` · Claude · co: Claude <noreply@anthropic.com> · Censo de integridad: corrige causa raiz A/C, casos B/D/F, mueve documentos muertos, incorpora ADR-38/39
  - `f320550` · Claude · CI: usa el modo linea base en vez de check.py sin banderas
  - `3375a28` · Claude · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `26e7ef4` · Claude · T03: normaliza punto/guion bajo, declara historicos, congela linea base P1
  - `69357d4` · Claude · Censo v1.1: procedencia por commit, denominador eb92d99/9efa61f, cadena del caso pelon
  - `9dbff7a` · Claude · Anade censo-integridad-v1_0: auditoria mecanica completa de canon/ y forense/
  - `9efa61f` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Corrige rotulo del perimetro del Hito D + registro congelado de IDs
  - `eb92d99` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-8.md: cierre de sesion del 29/jul
  - `8254fde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-7.md: documento de traspaso, estaba fuera del repo
  - `7d6535e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · estado v1.8: corrige "cubre las 27" y registra la auditoria de perimetro
  - `a79227e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Nota forense: verificacion del perimetro y cobertura del pre-registro

**Archivos tocados:**
```
.github/workflows/verify.yml                       |    4 +-
 .gitignore                                         |   16 +
 AUTHORSHIP.md                                      |   84 ++
 AVISO-DE-ALCANCE.md                                |  106 +++
 CITATION.cff                                       |   35 +
 CONTRIBUTING.md                                    |   12 +-
 LICENSE                                            |   65 ++
 README.md                                          |    6 +-
 USO-ACEPTABLE.md                                   |   92 ++
 canon/cola.yaml                                    |  369 ++++++++
 ...do-programa-v1_7.md => estado-programa-v1_9.md} |   52 +-
 canon/glosario-v5_6.md                             |    6 +-
 canon/gobernanza-v1_14.md                          |  458 +++++++++
 canon/gobernanza-v1_8.md                           |  336 -------
 canon/integrador-psicologia-mexicano.md            |    4 +-
 ...lo-decision-v3_2.md => modelo-decision-v3_4.md} |   94 +-
 canon/protocolo-sesion-v1_0.md                     |  107 +++
 ...ayer_of_Decisions__Environment_and_Structure.md |    2 +
 ...ucation_and_Information_as_Decision_Behavior.md |    2 +
 data/manifiesto.yaml                               | 1001 ++++++++++++++++++++
 forense/bitacora.md                                |  561 +++++++++++
 forense/censo-integridad-v1_0.md                   |  313 ++++++
 forense/censo-integridad-v1_1.md                   |  156 +++
 forense/historico/TRANSFER-maestra-7.md            |  169 ++++
 forense/historico/TRANSFER-maestra-8.md            |  210 ++++
 forense/historico/TRANSFER-maestra-9.md            |  188 ++++
 forense/hitoD-R3_2-veredicto-v1_0.md               |  136 +++
 forense/hitoD-preregistro-v2_0.md                  |  283 ++++++
 forense/notas/2026-07-29-b-correccion-perimetro.md |  217 +++++
 .../notas/2026-07-29-c-correccion-curaduria-66.md  |   30 +
 forense/notas/2026-07-29-d-bloqueo-encig.md        |   52 +
 forense/notas/2026-07-30-calx-g3-salida.txt        |  184 ++++
 ...26-07-30-ensanut2024-salud-post-autodirigido.md |   66 ++
 forense/notas/2026-07-30-fetch-vs-html-crudo.md    |   46 +
 instrucciones-proyecto-v2.md                       |   24 +-
 milpa/milpa-plan-v0_1.md                           |    2 +-
 milpa/procedencia.yaml                             |    7 +-
 revision-publicacion-2026-07-30.md                 |  463 +++++++++
 tests/baseline.json                                |  448 +++++++++
 tests/bitacora.py                                  |  276 ++++++
 tests/calx_g3.py                                   |  420 ++++++++
 tests/check.py                                     |  631 +++++++++++-
 tests/manifiesto.py                                |  339 +++++++
 tests/validador_registro_ids.py                    |  242 +++++
 44 files changed, 7934 insertions(+), 380 deletions(-)
```

**ADRs añadidos:** ADR-01, ADR-02, ADR-03, ADR-04, ADR-05, ADR-06, ADR-07, ADR-08, ADR-09, ADR-10, ADR-11, ADR-12, ADR-13, ADR-14, ADR-15, ADR-16, ADR-17, ADR-18, ADR-19, ADR-20, ADR-21, ADR-22, ADR-23, ADR-24, ADR-25, ADR-26, ADR-27, ADR-28, ADR-29, ADR-30, ADR-31, ADR-32, ADR-33, ADR-34, ADR-35, ADR-36, ADR-37, ADR-38, ADR-39, ADR-40, ADR-41, ADR-42, ADR-43, ADR-44, ADR-45, ADR-46
**Líneas de versión modificadas en canon/:** 5
  - evidencia: "canon/gobernanza-v1_14.md:2 (cabecera: \"### `gobernanza` · **v1.14** · 30 de julio de 2026\") vs :16 (\"**Versión de este documento:** 1.12\"). La misma línea 16 ya trae, entre paréntesis, una nota fechada 29/jul/2026 declarando que esa cifra decía antes '1.1' contradiciendo la cabecera del mismo archivo (que en ese momento ya decía 1.9) -- se corrigió una vez y volvió a quedar desfasada al subir el archivo a v1.14 sin que nadie actualizara el cuerpo."
  - ### `estado` · **v1.9** · 29 de julio de 2026 · **ÚNICA FUENTE DE ESTADO**
  - ### `gobernanza` · **v1.14** · 30 de julio de 2026 · **46 ADR**
  - ### `modelo` · **v3.4** · CANÓNICO OPERATIVO
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: (tests/baseline.json no existía en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: C-01, D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, E-01, E-02, E-03, E-04, E-05, E-06, I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-08, I-09, I-10, I-11, I-12, I-13, I-14, I-15
  - Cerrados: (ninguno)

**Qué se decidió:** D-09/D-10 sellados con ADR-47 (gobernanza v1.15): distingo FALSAR REGLA vs CALIBRAR COEFICIENTE. D-10 opcion 1 (olas 2-3), D-09 opcion 3 (elasticidad descriptiva, sin veredicto). Fase C de CAL-G3 desbloqueada con alcance reducido, no corrida en esta sesion. Nota 9 en hitoD-preregistro-v2_0.md. milpa/procedencia.yaml no se toca.
**Qué quedó bloqueado:** Fase C de CAL-G3 (estimacion real) -- no se corre en esta sesion por instruccion explicita. Revision de las 27 fichas del perimetro por tipo de tarea (D-11 en cola.yaml, abierta sin resolver).

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/sellar-d09-d10-adr-mncope` · **HEAD inicial (origin/main):** `9301e59203b01243e76fe2de47eaad93667a9514` · **HEAD final:** `80739405e3e69360d165540ff2d58abd137638a0`

**Commits de la sesión:**
  - `8073940` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · cola.yaml: nueva entrada I-16 -- gobernanza:16 declara estado de programa falso
  - `e146f30` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza v1.15: corrige version del cuerpo (I-12, tercer caso)
  - `388e3a2` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.14 -> v1.15 -- ADR-47 (falsar regla != calibrar coeficiente), sella D-09/D-10
  - `d391f58` · Josanoforo · Merge pull request #12 from Josanoforo/sesion/calg3-poder
  - `58f8a54` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3: aritmética de poder sobre el panel completo — apilar dos transiciones no mueve CAL-C
  - `1868045` · Josanoforo · Merge pull request #11 from Josanoforo/claude/siete-hallazgos-cola-86sj9r
  - `16af08a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · cola: registra cinco hallazgos operativos de la jornada del 30/jul (I-11..I-15)
  - `64a5d7b` · Josanoforo · Merge pull request #10 from Josanoforo/sesion/calg3
  - `4a58320` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · Merge origin/main (PR #8 ADR-46, PR #9 ENCUCI) into sesion/calg3
  - `6b54d7c` · Josanoforo · Merge pull request #9 from Josanoforo/sesion/encuci
  - `dcbf6ec` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Merge origin/main (PR #8, ADR-46) into sesion/encuci
  - `7847920` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3 Fase B: chequeo CAL-X, dos premisas falsas y el confundidor 5 sin cerrar
  - `981c1ea` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3: chequeo CAL-X del punto 9a, previo a abrir microdatos
  - `11d9415` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · ENCUCI 2020: registro de BD/FD bajados por navegador; corrige premisa de ENUT/ENCUCI
  - `686e377` · Josanoforo · co: Claude Opus 5 (1M context) <noreply@anthropic.com> · CAL-G3 Fase A: descarga y registro de las tres olas de ENNViH/MxFLS
  - `0817817` · Josanoforo · Merge pull request #8 from Josanoforo/claude/e03-session-contamination-xb1y55
  - `85f608a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre -- ADR-46 (unidad de contaminación es la sesión)
  - `f8a9962` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.13 -> v1.14 -- ADR-46 (unidad de contaminación es la sesión, no la máquina)
  - `5b7113a` · Josanoforo · Merge pull request #7 from Josanoforo/claude/hitod-perimetro-compara
  - `82b0961` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — Hito D Fase 1, Paso 4 (ampliación)
  - `33b412f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · manifiesto.py: pliegue '>' con ancho en vez de literal '|' sin envolver
  - `ce3c284` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1, Paso 4 (ampliación): serie completa de ENCIG/ENIF/ENVIPE/ENIGH
  - `45be175` · Josanoforo · Merge pull request #6 from Josanoforo/claude/hitod-perimetro-compara
  - `d0d9e07` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — Hito D Fase 1, Pasos 1-3
  - `feaf38e` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Hito D Fase 1 (parcial, Pasos 1-3): perímetro de red, tabla de fuentes, --compara
  - `dc5fd0f` · Josanoforo · Merge pull request #5 from Josanoforo/claude/manifiesto-registra-verifica
  - `095a2a2` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre — resolución de conflictos, D-07, I-09
  - `5a9263d` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: declara desvío de alcance y el hueco de --contrasta
  - `beac5eb` · Josanoforo · Merge origin/main (PR #4: D-05/ADR-45) into C1
  - `7f9fd96` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: bloque de cierre de la sesión C1 (manifiesto.py)
  - `b65f44f` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · C1: tests/manifiesto.py — --registra y --verifica de procedencia de datos
  - `4054c35` · Josanoforo · Merge pull request #4 from Josanoforo/claude/falsacion-vocabulary-zfjvr4
  - `a217d32` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · bitacora: cierre de sesión D-05/ADR-45
  - `adb3e62` · Claude · D-05: fija el vocabulario de "prueba de falsación" (ADR-45)
  - `584f806` · Josanoforo · Merge pull request #3 from Josanoforo/claude/f2-f4-portada-adr-7fjpln
  - `7d92f5b` · Claude · bitácora: bloque de cierre — escalada de D-05, sesión F2/F4 completa
  - `a528654` · Claude · cola: D-05 -- "prueba de falsación corrida" sin referente único, escalado a mesa
  - `46e9cef` · Claude · bitácora: bloque de cierre de la sesión F2/F4 (portada, ADR-44)
  - `bdb1b77` · Claude · cola: F7.b y F6/T-README entran a la cola, sin abrirlas
  - `2d1d866` · Claude · gobernanza: v1.11 -> v1.12 -- ADR-44 (publicación del repositorio sin ADR previo)
  - `856639c` · Claude · README: corrige README:40 contra el registro de veredictos archivados
  - `25abb83` · Josanoforo · Merge pull request #2 from Josanoforo/claude/refreeze-baseline-pr1-4zha5w
  - `1ee9f29` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: el borrado de la rama del PR #1 quedó bloqueado, no hecho
  - `902ab75` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · bitácora: bloque de cierre del refreeze post-PR #1
  - `84aaae3` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · cola: I-01 sube a casos=2 — el refreeze post-PR #1 como evidencia para A1
  - `78288a2` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · estado: declaración vigente de la suite a la corrida real (19 FAIL · 87 WARN)
  - `74027d5` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · Refreeze de línea base tras el merge del PR #1 (main 22a7d9d)
  - `a0ae0ad` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · check.py: buckets propios para las 3 entradas del refreeze post-PR #1
  - `22a7d9d` · Josanoforo · Merge pull request #1 from Josanoforo/claude/psicologia-mexicano-publication-review-h5h6ic
  - `f4bef94` · Josanoforo · Nota de reconciliación: LICENSE-CORPUS.md descartado (D-05)
  - `10239cd` · Claude · co: Claude Fable 5 <noreply@anthropic.com> · revisión estratégica de publicación (propuesta sin sello, ADR-39 aplicado al encargo)
  - `4e174dd` · Josanoforo · Add files via upload
  - `7fa7481` · Josanoforo · Delete USO-ACEPTABLE.md
  - `83db9c9` · Josanoforo · Delete CITATION.cff
  - `5fab073` · Josanoforo · Delete AVISO-DE-ALCANCE.md
  - `29f08b4` · Josanoforo · Delete LICENSE
  - `a946db5` · Josanoforo · Delete AUTHORSHIP.md
  - `acd65af` · Josanoforo · Add files via upload
  - `fb1f333` · Josanoforo · Add files via upload
  - `c3adff8` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: segundo bloque de cierre
  - `b73d1dd` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · cierre del gate (segunda vuelta): bucket propio TRANSFER-9, estado sincronizado, cola +2
  - `c6dd7ee` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · bitácora: primer bloque de cierre + fix de bitacora.py --cierra
  - `7dd1c5a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 2: aterriza protocolo-sesion, cola.yaml y tests/bitacora.py
  - `c42abc9` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · Parte 1: cierre del gate T17 -- estado sincronizado, deuda congelada, .gitignore
  - `97b9f2b` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T17 ve su propio objeto -- escanea hitoD-preregistro, no solo estado
  - `d123f49` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.10 -> v1.11 -- ADR-42 (qué significa el verde) y ADR-43 (esquema de co-autoría)
  - `24df4b3` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD: adenda 1 a CAL-G3 -- desenlace primario a cuatro estados con molde ENIF
  - `c9e67bd` · Jonas · co: Claude Fable 5 <noreply@anthropic.com> · hitoD: ficha CAL-G3 -- pre-registro de estimación propia de coeficiente de generador
  - `015af3a` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T03 exime citas de renombre; --freeze con conteo derivado (18 FAIL · 82 WARN)
  - `2bf50b2` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · gobernanza: v1.9 -> v1.10 -- ADR-41 (reglas de sesión sin archivo, autoría del repo)
  - `c68feab` · Jonas · co: Claude Sonnet 5 <noreply@anthropic.com> · instrucciones-proyecto-v2.md: v2 -> v2.2 -- procedencia documental y hallazgos de Hito D
  - `afa7c7f` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · hitoD-R3.2: veredicto B -- gate inalcanzable por construcción, escala no valor
  - `771ea26` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: T18 T-PASO2-EJECUCION -- veredictos en bloque designado (ADR-40)
  - `d26cfde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · tests: newest() por versión no lexicográfico; T17 asevera unicidad
  - `de3f22a` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · estado: consolida declaración canónica de cobertura del pre-registro (§4·S2)
  - `1a56210` · Claude · co: Claude <noreply@anthropic.com> · tests: T17 T-FICHAS-COUNT -- declarado en estado == encabezados ## R reales
  - `90eb140` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: revierte prefijo de ruta en 3 citas (T03 no las ve); documenta el hueco
  - `b28b144` · Claude · co: Claude <noreply@anthropic.com> · hitoD-preregistro: ficha de R3.2, pre-registrada antes de abrir ENCIG
  - `9fb8473` · Claude · co: Claude <noreply@anthropic.com> · tests: T14/T15/T16 -- convierte en test 4 de las 7 cifras que quedaron a mano
  - `e3d483b` · Claude · co: Claude <noreply@anthropic.com> · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `c377b97` · Claude · co: Claude <noreply@anthropic.com> · tests/baseline.json: congela 18 FAIL / 82 WARN tras la sesion de correcciones
  - `31fff96` · Claude · co: Claude <noreply@anthropic.com> · Censo de integridad: corrige causa raiz A/C, casos B/D/F, mueve documentos muertos, incorpora ADR-38/39
  - `f320550` · Claude · CI: usa el modo linea base en vez de check.py sin banderas
  - `3375a28` · Claude · baseline.json: actualiza HEAD al commit real que describe el arbol
  - `26e7ef4` · Claude · T03: normaliza punto/guion bajo, declara historicos, congela linea base P1
  - `69357d4` · Claude · Censo v1.1: procedencia por commit, denominador eb92d99/9efa61f, cadena del caso pelon
  - `9dbff7a` · Claude · Anade censo-integridad-v1_0: auditoria mecanica completa de canon/ y forense/
  - `9efa61f` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Corrige rotulo del perimetro del Hito D + registro congelado de IDs
  - `eb92d99` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-8.md: cierre de sesion del 29/jul
  - `8254fde` · Claude · co: Claude Sonnet 5 <noreply@anthropic.com> · Anade TRANSFER-maestra-7.md: documento de traspaso, estaba fuera del repo
  - `7d6535e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · estado v1.8: corrige "cubre las 27" y registra la auditoria de perimetro
  - `a79227e` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Nota forense: verificacion del perimetro y cobertura del pre-registro

**Archivos tocados:**
```
.github/workflows/verify.yml                       |    4 +-
 .gitignore                                         |   16 +
 AUTHORSHIP.md                                      |   84 ++
 AVISO-DE-ALCANCE.md                                |  106 +++
 CITATION.cff                                       |   35 +
 CONTRIBUTING.md                                    |   12 +-
 LICENSE                                            |   65 ++
 README.md                                          |    6 +-
 USO-ACEPTABLE.md                                   |   92 ++
 canon/cola.yaml                                    |  393 ++++++++
 ...do-programa-v1_7.md => estado-programa-v1_9.md} |   52 +-
 canon/glosario-v5_6.md                             |    6 +-
 canon/gobernanza-v1_15.md                          |  478 ++++++++++
 canon/gobernanza-v1_8.md                           |  336 -------
 canon/integrador-psicologia-mexicano.md            |    4 +-
 ...lo-decision-v3_2.md => modelo-decision-v3_4.md} |   94 +-
 canon/protocolo-sesion-v1_0.md                     |  107 +++
 ...ayer_of_Decisions__Environment_and_Structure.md |    2 +
 ...ucation_and_Information_as_Decision_Behavior.md |    2 +
 data/manifiesto.yaml                               | 1001 ++++++++++++++++++++
 forense/bitacora.md                                |  726 ++++++++++++++
 forense/censo-integridad-v1_0.md                   |  313 ++++++
 forense/censo-integridad-v1_1.md                   |  156 +++
 forense/historico/TRANSFER-maestra-7.md            |  169 ++++
 forense/historico/TRANSFER-maestra-8.md            |  210 ++++
 forense/historico/TRANSFER-maestra-9.md            |  188 ++++
 forense/hitoD-R3_2-veredicto-v1_0.md               |  136 +++
 forense/hitoD-preregistro-v2_0.md                  |  301 ++++++
 forense/notas/2026-07-29-b-correccion-perimetro.md |  217 +++++
 .../notas/2026-07-29-c-correccion-curaduria-66.md  |   30 +
 forense/notas/2026-07-29-d-bloqueo-encig.md        |   52 +
 forense/notas/2026-07-30-calx-g3-salida.txt        |  184 ++++
 ...26-07-30-ensanut2024-salud-post-autodirigido.md |   66 ++
 forense/notas/2026-07-30-fetch-vs-html-crudo.md    |   46 +
 instrucciones-proyecto-v2.md                       |   24 +-
 milpa/milpa-plan-v0_1.md                           |    2 +-
 milpa/procedencia.yaml                             |    7 +-
 revision-publicacion-2026-07-30.md                 |  463 +++++++++
 tests/baseline.json                                |  448 +++++++++
 tests/bitacora.py                                  |  276 ++++++
 tests/calx_g3.py                                   |  420 ++++++++
 tests/check.py                                     |  631 +++++++++++-
 tests/manifiesto.py                                |  339 +++++++
 tests/validador_registro_ids.py                    |  242 +++++
 44 files changed, 8161 insertions(+), 380 deletions(-)
```

**ADRs añadidos:** ADR-01, ADR-02, ADR-03, ADR-04, ADR-05, ADR-06, ADR-07, ADR-08, ADR-09, ADR-10, ADR-11, ADR-12, ADR-13, ADR-14, ADR-15, ADR-16, ADR-17, ADR-18, ADR-19, ADR-20, ADR-21, ADR-22, ADR-23, ADR-24, ADR-25, ADR-26, ADR-27, ADR-28, ADR-29, ADR-30, ADR-31, ADR-32, ADR-33, ADR-34, ADR-35, ADR-36, ADR-37, ADR-38, ADR-39, ADR-40, ADR-41, ADR-42, ADR-43, ADR-44, ADR-45, ADR-46, ADR-47
**Líneas de versión modificadas en canon/:** 5
  - evidencia: "canon/gobernanza-v1_14.md:2 (cabecera: \"### `gobernanza` · **v1.14** · 30 de julio de 2026\") vs :16 (\"**Versión de este documento:** 1.12\"). La misma línea 16 ya trae, entre paréntesis, una nota fechada 29/jul/2026 declarando que esa cifra decía antes '1.1' contradiciendo la cabecera del mismo archivo (que en ese momento ya decía 1.9) -- se corrigió una vez y volvió a quedar desfasada al subir el archivo a v1.14 sin que nadie actualizara el cuerpo. TERCER CASO, el mismo día: el commit que registró esta entrada (388e3a2, sella D-09/D-10 con ADR-47, sube gobernanza a v1.15/47 ADR) subió el archivo de v1.14 a v1.15 sin tocar la línea 16, que seguía en '1.12' -- el defecto reapareció en el propio commit que lo catalogó como I-12, antes de que el PR #13 se fusionara. Detectado por el autor revisando el diff, no por ningún test (verificado: T13 solo exige presencia de los campos ARCHIVO/NOMBRE ESTABLE, no coincidencia de valor -- no habría atrapado esto). canon/gobernanza-v1_15.md:90 tenía además una segunda ocurrencia de la misma familia, no catalogada hasta ahora: la fila de `gobernanza-programa.md` v1.0 en la tabla de §2 se autocitaba con el nombre de archivo YA renombrado y desfasado (\"hoy gobernanza-v1.12.md\", sin backticks para no leerse como cita viva) -- un segundo campo autodeclarado, en el mismo archivo, con el mismo desfase, corregido en el mismo commit."
  - ### `estado` · **v1.9** · 29 de julio de 2026 · **ÚNICA FUENTE DE ESTADO**
  - ### `gobernanza` · **v1.15** · 30 de julio de 2026 · **47 ADR**
  - ### `modelo` · **v3.4** · CANÓNICO OPERATIVO
  - ### `protocolo` · **v1.0** · 29 de julio de 2026

**Delta de suite:**
  - Antes: (tests/baseline.json no existía en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: C-01, D-01, D-02, D-03, D-04, D-05, D-06, D-07, D-08, D-09, D-10, D-11, E-01, E-02, E-03, E-04, E-05, E-06, I-01, I-02, I-03, I-04, I-05, I-06, I-07, I-08, I-09, I-10, I-11, I-12, I-13, I-14, I-15, I-16
  - Cerrados: (ninguno)

**Qué se decidió:** Nueva entrada I-16 en cola.yaml: gobernanza:16 afirma en presente 'modelo v2 y glosario v5 consolidados' -- falso (modelo va en v3.4, glosario en v5.6), congelado desde v1.1. Distinguida explicitamente de I-12: I-12 es sintactico (version vs nombre de archivo, mecanico, T19 lo atrapa); I-16 es semantico (prosa de estado envejecida, T19 NO lo atraparia). Barrido de canon/milpa/forense por otras frases de estado sin fecha: solo se encontro otra (estado-programa:91, Fase 1 pospuesta) y sigue siendo cierta. No se toco la linea de gobernanza -- queda para mesa por instruccion explicita.
**Qué quedó bloqueado:** La reescritura de gobernanza:16 (decision de contenido, no mecanica) -- queda para mesa. I-16 no se resuelve en esta sesion.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/i-01-false-positives-docs-jh7r2g` · **HEAD inicial (origin/main):** `78d5d54f8037569ef0acfbca8e59b2ba4922f0f6` · **HEAD final:** `2c157fac3d9a0cc54f9e6fc0b665b779cff9c1ae`

**Commits de la sesión:**
  - `2c157fa` · Claude · cola: I-01 sube a casos=3 -- backtick de I-12 en bitacora.md disparo T03 nuevo (PR #13)

**Archivos tocados:**
```
canon/cola.yaml | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: (ninguno)
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-08, I-09

**Qué se decidió:** Nueva entrada registrada: I-01 sube a casos=3. El tercero ocurrio hoy en el PR #13 (commit 388e3a2, ya fusionado): al redactar en forense/bitacora.md la evidencia de I-12, una cita de nombre de archivo entre backticks dentro de ese mismo parrafo se volcó al diff de sesión y disparó un T03 nuevo; se corrigió quitando los backticks antes de comitear, por eso no aparece en la corrida actual. Es la segunda vez el mismo dia que documentar un falso positivo genera otro -- la primera fue la nota de reconciliación del PR #1 (caso 2) -- y es el argumento mas fuerte que existe para la marca explicita que I-01 propone: el criterio de salida ya dice que un documento debe poder citar un archivo inexistente o descartado como ejemplo sin generar WARN.
**Qué quedó bloqueado:** La marca explicita de A1 (distinguir en T03 mención de referencia vs cita real) sigue en la cola como I-01, ahora con 3 casos; no se implementa en esta sesión.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/i-01-false-positives-docs-jh7r2g` · **HEAD inicial (origin/main):** `78d5d54f8037569ef0acfbca8e59b2ba4922f0f6` · **HEAD final:** `dd85b7b211150caffdc170cc164adc6ae501dde0`

**Commits de la sesión:**
  - `dd85b7b` · Claude · cola: registra I-17/I-18 -- baseline.json congelado en bitacora.py --cierra y clave sin numero de linea deduplica multiplicidad
  - `ce2918b` · Claude · bitacora: cierra sesion -- registra I-01 caso 3 (backtick de I-12, PR #13)
  - `2c157fa` · Claude · cola: I-01 sube a casos=3 -- backtick de I-12 en bitacora.md disparo T03 nuevo (PR #13)

**Archivos tocados:**
```
canon/cola.yaml     | 24 ++++++++++++++++++++++--
 forense/bitacora.md | 29 +++++++++++++++++++++++++++++
 2 files changed, 51 insertions(+), 2 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: I-17, I-18
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-08, I-09

**Qué se decidió:** Verificado el desfase que bitacora.py --cierra reporto (21 FAIL/84 WARN 'Antes' vs 19 FAIL/87 WARN reales) contra check.py: los FAIL cuadran (21-2 resueltos=19). Los WARN no son claves nuevas -- --baseline sigue VERDE -- son 3 ocurrencias adicionales de dos claves YA congeladas en baseline.json (T03 LICENSE-CORPUS.md paso de 1 a 3 citas en revision-publicacion-2026-07-30.md; T03 estado-programa-v1_8.md paso de 1 a 2 citas en censo-integridad-v1_1.md), invisibles porque _baseline_key() (tests/check.py:763) quita el numero de linea antes de deduplicar -- primera vez que esta limitacion se manifiesta con cifras verificables. Registradas dos entradas nuevas en cola.yaml sin resolver: I-17 (bitacora.py --cierra declara 'Antes' desde baseline.json congelado sin rotular la fuente -- misma familia que README:40/I-06/I-07) e I-18 (el hallazgo de fondo: la clave sin numero de linea deduplica multiplicidad de un defecto ya conocido; documentarlo no lo mitiga).
**Qué quedó bloqueado:** I-17 e I-18 quedan abiertas, sin implementarse -- por instruccion explicita, esta sesion solo registra. No se toco tests/bitacora.py ni tests/check.py.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/new-session-gdstpo` · **HEAD inicial (origin/main):** `78d5d54f8037569ef0acfbca8e59b2ba4922f0f6` · **HEAD final:** `ef9ac0c427eb989e85b0994e40bc7d6e37ddd027`

**Commits de la sesión:**
  - `ef9ac0c` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Hito E: recoge el plan de campaña (tipo 3, sin sello) + verificación de premisas

**Archivos tocados:**
```
canon/cola.yaml                                    |  33 +++
 forense/hitoE-campana-medicion-v2_0.md             | 232 +++++++++++++++++++++
 .../2026-07-30-verificacion-premisas-hitoE.md      | 153 ++++++++++++++
 3 files changed, 418 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-12, E-07, I-17, I-18
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-08, I-09

**Qué se decidió:** Se recogió al repo el plan de Hito E (adjunto de chat, tipo 3) VERBATIM y sin sello, con cabecera de procedencia, y se verificaron sus premisas contra 78d5d54 como exige instrucciones v2.1. Catorce afirmaciones sobre el estado del repo: DIEZ se sostienen -- incluidas las dos que cargan la tesis del documento (CAL-G3 declaró la opción (b), hitoD-preregistro-v2_0.md:511; R3.2 dejó el motor 4x-34x fuera de escala). CUATRO no: (1) los 15 coeficientes se reducen a NUEVE constructos, no ocho -- el plan lo declara derivado en su propio módulo de auditoría y omite radio_confianza (G1 y G5), que él mismo nombra en §8; propaga a la puerta E0->E1 que pre-registra '>=5 de 8', y 5/8 no es 5/9; (2) confianza_institucional no es un constructo sino un vector de SEIS (ADR-28.b) -- la mitigación de E2 'operacionalización única por constructo' derogaría ese ADR sin nombrarlo, y el vector sigue SIN POBLAR (procedencia.yaml:65); (3) '61 fuentes' no existe en ningún archivo -- reales: 56 entradas de manifiesto (55 sin la nota de clasificación), 27 de ellas paquetes de UNA encuesta, 6 programas distintos, 36 documentos de corpus; aparece dentro de una obligación de exhaustividad de E0, que así no se puede auditar; (4) 'ENSANUT 20 archivos bajados, desbloquea 4 fichas' -- data/raw/ no existe, el manifiesto no tiene ninguna entrada de ENSANUT, la nota de esa sesión inventaría 10 filas y prohíbe la descarga sin mesa, R4.2 es la única ficha asociada, y bajo ADR-46 no es paralelo sino dependencia de E1 por la misma sesión limpia. NO se corrigió el cuerpo del plan: instrucciones v2.1 prohíbe ajustar el texto para que cuadre, y los números tocados son puertas de decisión. Registrado en cola.yaml I-17 (instrumento), D-12 (decision), E-07 (evidencia). Y un hallazgo de INSTRUMENTO propio, I-18: bitacora.py --cierra tiene dos defectos que fabrican un bloque falso -- (a) deriva contra el ref LOCAL origin/main sin hacer fetch (el primer intento de esta sesión declaró 46 archivos, 8747 inserciones y los 47 ADRs como trabajo de la sesión, porque el ref estaba en 9301e59 y el remoto en 78d5d54; se descartó sin comitear, se hizo fetch y se regeneró: 3 archivos, 418 inserciones, ningún ADR); (b) tests/bitacora.py:235-237 calcula 'Cerrados' filtrando por el estado DESPUÉS sin compararlo con el estado ANTES, así que reporta como cerradas por la sesión las once que ya estaban cerradas en 78d5d54 -- esta sesión cerró CERO. El defecto (b) sigue presente en el bloque de abajo: su línea 'Cerrados' es falsa y se lee junto a I-18.
**Qué quedó bloqueado:** Las cuatro entradas nuevas quedan abiertas y sin resolver, deliberadamente. Las tres del plan: corregir el denominador de la puerta E0->E1 y decidir si confianza_institucional se mide como uno o como seis son decisiones de mesa, no correcciones de una sesión de verificación. La de instrumento (I-18): bitacora.py NO se arregló en esta sesión -- protocolo §4 prohibición 1 (no se abre trabajo de evidencia y de instrumento en la misma sesión) y prohibición 2 (no se congela una línea base en la misma corrida que cambió el medidor); el fetch se hizo a mano, el script sigue sin hacerlo. El plan de Hito E sigue SIN SELLO -- no hay ADR y su propia cabecera declara 'propuesta, no rige sin ADR'; nada de E0-E4 está aprobado ni se ejecutó. Referencia colgante no resuelta: 'D1' (plan §6) no existe en el repo; el candidato más cercano por contenido es ADR-44 (publicación del repositorio), sin confirmar. Esta sesión NO tocó ninguna fuente externa (sin petición de red a ningún portal de datos, sin descargas): bajo la condición verificable de ADR-46 no queda inhabilitada para pre-registrar contra nada. Pendiente ajeno: la sesión que está bajando ENSANUT debe cerrar y declarar su propio alcance -- hasta entonces '20 archivos' es tipo (3) y no entra al canon como hecho.

---

## 2026-07-30

**Fecha:** 2026-07-30 · **Rama:** `claude/new-session-gdstpo` · **HEAD inicial (origin/main):** `fe66ee9a9df71542381e5f6b507e9b1d78b4f291` · **HEAD final:** `ac5b95fe4f558daf81b77cbb05f0ee861c85390b`

**Commits de la sesión:**
  - `ac5b95f` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · merge origin/main -- resuelve cola.yaml y bitacora.md (append-only), renumera I-17/I-18 -> I-19/I-20
  - `0c64eaa` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · bitacora: cierra sesión -- Hito E verificado + I-18 (bitacora.py fabrica bloques falsos)
  - `ef9ac0c` · Claude · co: Claude Opus 5 <noreply@anthropic.com> · Hito E: recoge el plan de campaña (tipo 3, sin sello) + verificación de premisas

**Archivos tocados:**
```
canon/cola.yaml                                    |  44 ++++
 forense/bitacora.md                                |  31 +++
 forense/hitoE-campana-medicion-v2_0.md             | 234 +++++++++++++++++++++
 .../2026-07-30-verificacion-premisas-hitoE.md      | 155 ++++++++++++++
 4 files changed, 464 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 21 FAIL · 84 WARN (congelados en origin/main)
  - Después: 19 FAIL · 87 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: D-12, E-07, I-19, I-20
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-08, I-09

**Qué se decidió:** Merge de origin/main (fe66ee9, PR #14) en claude/new-session-gdstpo y resolución de los dos conflictos append-only (cola.yaml, bitacora.md) conservando ambos lados en orden cronológico. COLISION DE IDs resuelta renumerando LOS PROPIOS, nunca los de main (patrón E-04 -> E-06 de la sesión de ENCUCI): I-17 -> I-19 (plan Hito E, 8 vs 9 constructos y 61 fuentes) e I-18 -> I-20 (bitacora.py, baseline sin fetch y Cerrados); D-12 y E-07 no chocaron. Las dos renumeradas llevan nota declarando su ID original; los commits ef9ac0c/0c64eaa y el bloque de bitácora anterior citan los IDs viejos y NO se reescriben. La resolución NO fue concatenación ciega: main no era append puro de base -- había subido I-01 a casos=3 y extendido su evidencia (caso 3, PR #13) -- así que se reconstruyó como main completo + mi bloque, no como base + los dos apéndices, que habría perdido esa edición in-place. HALLAZGO QUE DESTAPO EL MERGE, registrado en I-20: el I-17 de main y mi I-20 tocan el MISMO script (tests/bitacora.py --cierra) por defectos DISTINTOS, sin que ninguna de las dos sesiones viera a la otra -- main-I-17 es sobre la fuente de la cifra 'Antes' (baseline.json congelado), I-20 es sobre el baseline del DIFF (ref local sin fetch) y sobre 'Cerrados'; con el I-18 de main (multiplicidad invisible a --baseline, en check.py) son cuatro defectos de instrumento registrados el mismo día por dos sesiones ciegas entre sí. Verificado antes de push: aritmética de líneas (cola 393+20+44=457=457; bitacora 894+61+31=986=986), cero marcadores de conflicto, 40 IDs sin duplicados, I-01 casos=3 conservado, check.py --baseline VERDE, validador OK, y el cuerpo del plan de Hito E sigue verbatim contra el adjunto original.
**Qué quedó bloqueado:** Sin cambios respecto al cierre anterior: las cuatro entradas (I-19, D-12, E-07, I-20) siguen abiertas y sin resolver -- corregir el denominador de la puerta E0->E1, decidir si confianza_institucional se mide como uno o como seis, y arreglar tests/bitacora.py son decisiones de mesa o trabajo de instrumento aparte (protocolo §4, prohibiciones 1 y 2). El plan de Hito E sigue SIN SELLO: no hay ADR. La línea 'Cerrados' del bloque de abajo sigue siendo falsa por el defecto (b) de I-20 -- esta sesión cerró CERO entradas; no se edita a mano porque el bloque es derivado y append-only, se lee junto a I-20. Queda pendiente abrir el PR de esta rama contra main.

---

## 2026-08-03

**Fecha:** 2026-08-03 · **Rama:** `sesion/cal-conf-faseb-pos4-envipe-paso1` · **HEAD inicial (origin/main):** `268d9dfc6b158849d2e49fe0824a8d2e93017850` · **HEAD final:** `e03b81cfbeff382f32595746d4942e25cc0e7b29`

**Commits de la sesión:**
  - `e03b81c` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · CAL-CONF Fase B, pos4 rehecho paso 1 (ENVIPE): TPer_Vic1 no tiene reactivo de exposicion_violencia

**Archivos tocados:**
```
forense/hallazgos.md                               |   1 +
 forense/hitoE-campana-medicion-v2_0.md             |  77 +++++
 .../2026-08-04-cal-conf-faseb-pos4-envipe-paso1.md | 322 +++++++++++++++++++++
 3 files changed, 400 insertions(+)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 19 FAIL · 83 WARN (congelados en origin/main)
  - Después: 19 FAIL · 84 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: (ninguno)
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-01, I-08, I-09, I-13

**Qué se decidió:** ENVIPE TPer_Vic1 examinado y descartado con argumento para exposicion_violencia (LA FUENTE NO TIENE EL DATO); adenda hitoE §19; contador sin cambio 8/14
**Qué quedó bloqueado:** C2 (G4 desenlaces vs. TPer_Vic1) declarado abierto, no resuelto; decisión de mesa pendiente sobre si el precedente aversion_riesgo/sens_estatus aplica a exposicion_violencia

---

## 2026-08-03

**Fecha:** 2026-08-03 · **Rama:** `sesion/hitoD-r7-2-delito-sin-seguro` · **HEAD inicial (origin/main):** `642be976c748f6e91a7888aceeb532e881fa100a` · **HEAD final:** `e9f6ac7ce32b3982eab5a50442e1ca6e0ec54fc4`

**Commits de la sesión:**
  - `e9f6ac7` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · Encargo J: R7.2 con las ocho olas ENVIPE — pareo por identificabilidad ejecutado a escala, D queda

**Archivos tocados:**
```
forense/hallazgos.md                       |   1 +
 forense/hitoD-preregistro-v2_0.md          |  14 ++
 forense/notas/2026-08-04-r7-2-ocho-olas.md | 148 +++++++++++++++++++
 tests/hitoD_r7_2_ocho_olas.py              | 226 +++++++++++++++++++++++++++++
 4 files changed, 389 insertions(+)
```
**Fecha:** 2026-08-03 · **Rama:** `sesion/cal-conf-faseb-pos4-envipe-tpervic2-tmodvic-paso2` · **HEAD inicial (origin/main):** `642be976c748f6e91a7888aceeb532e881fa100a` · **HEAD final:** `02d20b5200ecdb59acc8c5252538bee39bb2acc6`

**Commits de la sesión:**
  - `02d20b5` · Josanoforo · co: Claude Sonnet 5 <noreply@anthropic.com> · CAL-CONF Fase B, posición 4: mide exposicion_violencia (9 de 14)

**Archivos tocados:**
```
canon/modelo-decision-v4_0.md                      |  22 +-
 forense/hallazgos.md                               |   1 +
 forense/hitoE-campana-medicion-v2_0.md             |  70 +++++
 ...6-08-04-medicion-exposicion-violencia-envipe.md | 293 +++++++++++++++++++++
 milpa/procedencia.yaml                             | 122 +++++++++
 5 files changed, 497 insertions(+), 11 deletions(-)
```

**ADRs añadidos:** (ninguno detectado)
**Líneas de versión modificadas en canon/:** 0

**Delta de suite:**
  - Antes: 19 FAIL · 83 WARN (congelados en origin/main)
  - Después: 19 FAIL · 84 WARN (corrida real, sin --baseline)

**Cola — IDs afectados en la sesión:**
  - Abiertos: (ninguno)
  - Cerrados: D-05, D-06, D-07, D-08, D-09, D-10, E-04, E-05, E-06, I-01, I-08, I-09, I-13

**Qué se decidió:** Ocho olas ENVIPE agrupadas; pareo por identificabilidad ejecutado a escala -- ninguna vía cierra A sin reserva (desconocido: IC cruza 20; conocido: n insuficiente aun agrupado, 42/42 conglomerados singleton). D queda archivada, ambigüedad de Nota 12 disuelta sin ADR.
**Qué quedó bloqueado:** Ninguno propio. Decisión de mesa pendiente: si archiva este desenlace como entrada fechada en el bloque append-only de veredictos (no se archivó en este acto, es de mesa).
**Qué se decidió:** ENVIPE TPer_Vic2 mide exposicion_violencia (núcleo AP7_3_10-_14, binario 2024, ponderado FAC_ELE); AP7_3_09 extorsión aparte; estimador validado contra caso conocido (violación sexual 279/100k mujeres, 0.09% diff); C3 limpio, C2 sellado (dependencia BP1_23); clase MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO); contador 8→9/14, reparto cierra 9+0+2+3; sin ADR nuevo (propagación directa)
**Qué quedó bloqueado:** C2 sellado, no resuelto -- BP1_23/comunicacion.inseguridad.ver_oir_callar depende de la misma subpoblación por diseño del instrumento; H-12 no re-evaluado contra el nuevo reactivo (adjudicación fuera de alcance)

---

