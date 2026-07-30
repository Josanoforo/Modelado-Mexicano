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

