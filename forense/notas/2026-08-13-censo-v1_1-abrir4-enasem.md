# CENSO-v1.1 · Commit 1 — pre-registro: rescate de conducto (ABRIR-4/relaciones.tsv) + cruce ENASEM

**Resultado de este acto, dicho antes que nada:** de las 15 filas del censo v1.0, **3 (filas 12, 13, 14 — las tres de G5)** están contradichas por evidencia que ya vivía en el repo sin cruzar desde el 7-8/ago (`data/curacion-registro/relaciones.tsv`, commit `16180e6`, y `data/abrir4-variables-2026-08-08.tsv`, PR #159) — el censo del 4/ago escribió "Ninguna llave aplica" sobre las tres, y las tres tenían ya reactivo con texto verificado, co-observado con un desenlace candidato dentro del mismo instrumento. **Ninguna alcanza `RUTA-I`**: (B) sin (C) se sostiene en las tres — reclasifican a `RUTA-C` (candidata, la corrida no se ha ejecutado), no a identificación. El cruce de ENASEM (§4) **no aporta ninguna llave verificable** para ninguna de las 9 filas `SIN-RUTA`: 0 de 6,471 variables de las tres rondas (2018/2021/2024) mencionan `confianza`/`confía`; el único candidato de `familismo_obligacion` es un ítem genérico de personalidad ("cumplo mis obligaciones"), no de deber familiar; el único hallazgo con forma de llave es un candidato estructural de panel para `familismo_apoyo` (mismo ítem, tres olas, identificador de persona persistente) — se propone en §11, no se ejerce aquí. Las 9 filas `SIN-RUTA` salen de este acto con universo declarado en la celda: **9 de 9** (§5).

---

## 0 · ARRANQUE (resumen — detalle crudo ya corrido en la sesión, no repetido aquí)

Clon en `/home/pc0/Modelado-Mexicano` (no home). Worktree propio: `/home/pc0/mm-censo-v1_1`, rama `censo-v1_1-enasem`, creado desde `origin/main` fresco. `git worktree add` dio dos veces "Device or resource busy" al escribir `.git/config` — contención conocida de este entorno (`project_modelado_mexicano_git_config_contention`, memoria de sesiones previas); verificado sin daño: `git status` del worktree limpio, `HEAD` en `dcc4f6a`, tracking de rama confirmado (`git branch --show-current`).

**SHA.** Base declarada `b17a6f6`. `origin/main` real: `dcc4f6a` (merge PR #196). Diferencia — 5 commits, no es PARO: las 4 de `ACTO ENLACE-1` (Commits 1-4, `relaciones.tsv`/`hallazgos.md`) más el merge. Ninguna toca el perímetro de este acto; una sí importa como dato citado — ver §7 (el commit-count de `relaciones.tsv` que la addenda daba por uno).

**data/raw.** No aplica por instrucción del encargo para microdato — pero este acto sí abre los **diccionarios** `enasem*_fd_xlsx` (§4), que el propio encargo autoriza explícitamente ("Verificable desde los fd_xlsx de ENASEM, que son diccionarios — no exige abrir microdato"). El corpus compartido está montado en `/home/pc0/mm-corpus/raw` (mismo mecanismo que usan `wt-abrir4-*`/`wt-apertura-issp-*`); enlazado con `ln -s /home/pc0/mm-corpus/raw data/raw`, gitignorado, no se toca la red.

**ENTORNO.** Caja local (no `cloud_default`), consistente con el resto de la sesión. No se usó red en ningún comando de este acto.

**ESPEJO.** Ninguna cifra sale del espejo del proyecto. Todo comando queda a la vista abajo o ya corrió en la sesión (premisas, hashes, escaneo de diccionarios).

**Premisas del encargo, corridas:**

```
$ grep -cE '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md
15
$ grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      2 RUTA-C
      1 RUTA-I
      9 SIN-RUTA
$ awk -F'\t' 'NR>1 && $13=="EXISTE-SATISFACE"' data/abrir4-variables-2026-08-08.tsv | wc -l
4
$ grep -rl "abrir4\|verif3" tools/ tests/ | wc -l
0
$ ls forense/censo-estimabilidad-coeficientes-v1_1.md 2>/dev/null && echo "YA EXISTE - PARA"
(no existe, OK para continuar)
```

Las cinco premisas coinciden exactamente con lo que el encargo esperaba. No hubo que re-derivar ninguna.

---

## 1 · Fuentes leídas enteras (3.1)

- `canon/gobernanza-v1_15.md:617-633` — ADR-57 completo (a)-(e), no solo (c). Citado verbatim en §2.
- `forense/censo-estimabilidad-coeficientes-v1_0.md` completo (128 líneas) — §1 (cuatro rutas), §5 (15 filas), §7 (receta), §5-foto-del-corpus (línea 122).
- `data/abrir4-variables-2026-08-08.tsv` completo — 28 filas de datos, no solo las 4 `EXISTE-SATISFACE`. Resumen por instrumento: ENSAFI 2023 (7 filas, sin diccionario en corpus — columnas derivadas sin texto verificable), ENFIH 2019 (7 filas, 838 variables, instrumento más rico en conducta financiera y más pobre en actitud de los cuatro), ENASIC 2022 (7 filas, 1427 variables, hallazgo más fuerte del acto original — batería `P7_12`), ENBIARE 2021 (7 filas, texto de PDF, 2326 líneas, segundo hallazgo fuerte — Apartados A/B/F).
- `data/verif3-variables-2026-08-08.tsv` completo — 4 filas, las cuatro `EXISTE-NO-SATISFACE`, sobre `R7.3`/`R7.4`/`R7.5`/`R8.1`/`R2.1` (ACLED, Padrón Único de Bienestar, Contraloría Social, ECCO). **Ninguna de las cuatro filas de `verif3` toca ninguno de los 15 coeficientes de generador de este censo** — su universo de aplicación son las reglas del Hito D nombradas (`R7.x`/`R8.1`/`R2.1`/`R10.2`), no `milpa/procedencia.yaml`. Se declara la revisión completa y el negativo, per encargo ("mismo tratamiento") — no aporta ninguna celda a §5 de este acto.
- `forense/notas/2026-08-08-abrir4.md` completa (267 líneas) — arranque, verificación de hash (8/8 `COINCIDE`), declaración ADR-46 de esa sesión (inhabilitada para ENSAFI/ENFIH/ENASIC/ENBIARE), hallazgos por instrumento, §8 (qué decisiones de mesa habilita), §9 (defecto T02/T16 y su adenda de renombre — ver §9 de esta nota, mismo patrón).
- Las 6 entradas ENASEM de `data/manifiesto.yaml` — `usado_para` y `archivo`, sin abrir los zips de microdato (`enasem{2018,2021,2024}_{bd_csv_zip,fd_xlsx}`).
- `forense/registro-llaves-identificacion-v1_0.md` §3 y §4 completos — de dónde sale el `2` del denominador (fila `CAL-G3` + `R5.1-D2`) y la receta de conteo (§4, columna 6 de la tabla, patrón `EJERCIDA_`).

---

## 2 · ADR-57(c), verbatim completo — las tres llaves con su estado a la fecha del ADR

`canon/gobernanza-v1_15.md:623`, citado íntegro (el censo v1.0 solo citó la oración de ENNViH/MxFLS):

> **(c) COMPUERTA DE IDENTIFICACIÓN — sobre la clase de afirmación, no sobre el motor.** ADR-50/51 sobreviven íntegros: el motor se calibra por ajuste, MILPA sigue siendo la arquitectura objetivo, y sus parámetros necesitan reproducir conducta observada, no contrafactuales individuales. Lo que este inciso gobierna es qué puede afirmar cualquier artefacto o salida del programa: reproducir, describir y segmentar — siempre, con sus tiers y bandas; afirmaciones de intervención ("si se interviene X, pasa Y") — solo donde exista una llave de identificación declarada y sellada, de una de tres clases: (i) panel con el desenlace en el instrumento (mismos sujetos entre olas); (ii) experimento natural con grupo de comparación sobre encuestas repetidas; (iii) diseño experimental de terceros (evaluaciones aleatorizadas publicadas, clase Progresa/Oportunidades), usado como evidencia (a) con su cita. La lista corta inicial, con su estado verificado a la fecha de este ADR: **ENNViH/MxFLS** — panel de tres olas, dominio público; ruta viva vía `CAL-G3` (Fase C desbloqueada, olas 2-3, alcance descriptivo; la promoción de descriptivo a identificado exige su propio diseño intra-persona, no está concedida aquí). **ENASEM + pensión Bienestar** — panel 50+ con identificador de persona entre rondas más el experimento natural del programa; paso 1 ya corrido (Encargo S). **ENOE** — su panel rotativo queda refutado como ruta de conducta financiera (`CAL-ENOE` Fase A, 31/jul: el instrumento no trae reactivo de ahorro/crédito/deuda/planeación); permanece elegible únicamente como portador de desenlaces laborales para experimentos naturales (p. ej. salario mínimo de franja fronteriza). Ninguna llave de esta lista está ejercida: cada una exige su pre-registro propio. La compuerta abre por palanca, no en bloque — una llave sellada habilita afirmaciones de intervención solo sobre la relación que identifica.

**Lectura literal de la entrada ENASEM, importante para §4 abajo:** el ADR nombra el par "ENASEM + pensión Bienestar" como unidad, y lo que declara "verificado a la fecha" es específicamente la estructura de panel (identificador de persona entre rondas) y el experimento natural de la pensión — verificado por `Encargo S` (`forense/notas/2026-08-04-enasem-paso1-descriptor.md`), paso 1. El ADR no dice "cualquier ítem de ENASEM es llave para cualquier relación" — la última frase de (c) lo cierra explícitamente: *"la compuerta abre por palanca, no en bloque"*. Que la precondición estructural (identificador persistente, panel) exista no basta por sí sola: cada relación concreta (reactivo × desenlace) necesita su propia verificación, que es lo que §4 intenta para las tres filas de G5.

---

## 3 · Declaración ADR-46 — contaminación de esta sesión

Esta sesión, para escribir este censo:

- Leyó `data/abrir4-variables-2026-08-08.tsv` completo y `forense/notas/2026-08-08-abrir4.md` completo, que citan verbatim texto de reactivo, nombre de variable y (en algunos casos) frecuencias/valores observados de **ENSAFI 2023, ENFIH 2019, ENASIC 2022 y ENBIARE 2021**.
- Abrió directamente, vía `openpyxl`, los tres diccionarios `enasem{2018,2021,2024}_fd_xlsx` completos (§4) — 6,471 variables con `Nemónico` no vacío, nombre de variable y texto de pregunta.

Por el mismo criterio conservador que `ABRIR-4` se aplicó a sí mismo (ADR-46(4), "ante duda, se declara el nivel de exploración más alto"): **esta sesión queda inhabilitada, de forma permanente, para pre-registrar o adjudicar cualquier ficha del Hito D contra los cinco instrumentos: ENSAFI 2023, ENFIH 2019, ENASIC 2022, ENBIARE 2021 y ENASEM 2018/2021/2024.** Este acto no pre-registra ni adjudica nada contra ninguno de los cinco (perímetro declarado en el encargo, §6/§9 de la versión operativa) — costo aceptado, mismo patrón que `Encargo S` y `ABRIR-4` aceptaron para sus propios actos de mapeo. Contadores movidos por esta declaración: 0.

---

## 4 · Cruce de ENASEM — los tres diccionarios, abiertos y buscados, no solo citados de segunda mano

**Verificación de integridad (rule A.1), previa a abrir nada:**

```
$ python3 tests/manifiesto.py --verifica --id enasem2018_bd_csv_zip   → COINCIDE (8767343 bytes)
$ python3 tests/manifiesto.py --verifica --id enasem2018_fd_xlsx      → COINCIDE (628677 bytes)
$ python3 tests/manifiesto.py --verifica --id enasem2021_bd_csv_zip   → COINCIDE (7438658 bytes)
$ python3 tests/manifiesto.py --verifica --id enasem2021_fd_xlsx      → COINCIDE (633836 bytes)
$ python3 tests/manifiesto.py --verifica --id enasem2024_bd_csv_zip   → COINCIDE (11929796 bytes)
$ python3 tests/manifiesto.py --verifica --id enasem2024_fd_xlsx      → COINCIDE (617009 bytes)
```

**8/8... 6/6 COINCIDE.** Ningún AUSENTE, ningún hash discordante.

**Método.** `openpyxl`, formato "ESTRUCTURA DEL ARCHIVO" (idéntico al de ENFIH/ENASIC que `ABRIR-4` ya documentó): cada hoja trae bloques de sección con fila de cabecera (`ID`/`Nemónico`/`Alias`/`Nombre`/`Pregunta`/`Tipo`/`Long.`/`Códigos válidos`) seguida de filas de variable con separadores en blanco. Parser genérico: detecta la fila de cabecera por la presencia de `Nemónico` (insensible a acento/mayúscula), localiza columnas por nombre, y extrae `Nemónico`+`Nombre`+`Pregunta` de cada fila subsiguiente con `Nemónico` no vacío, hasta la siguiente cabecera. Corrido sobre las 11 hojas de 2018, 8 hojas de 2021 y 10 hojas de 2024 (`hojas`, ver salida cruda de la sesión): **2,167 variables (2018) + 2,092 (2021) + 2,212 (2024) = 6,471 variables con `Nemónico` no vacío**, texto acento-insensible, búsqueda de subcadena.

**Términos para las tres filas de G5, y resultado — negativo definitivo en dos de tres:**

| término | fila que cubre | coincidencias en 6,471 variables (3 rondas) |
|---|---|---|
| `confianza` / `confia` | 14 · radio_confianza | **0** |
| `obligacion` (literal) | 13 · familismo_obligacion | 1 (`D20`, batería Big-Five: *"Soy responsable. Por lo general cumplo con mis obligaciones lo mejor que puedo"* — autodescripción de personalidad, no deber hacia la familia; construcción distinta, no se cuenta como candidato) |
| `deber` | 13 · familismo_obligacion | 0 fuera del hit anterior |
| `apoyo`/`ayuda`/`familiar`/`hijo`/`nieto`/`conyuge` | 12 · familismo_apoyo | cientos — dominados por la Sección G (transferencias intergeneracionales), ver detalle abajo |

**Radio_confianza (fila 14): negativo limpio.** Cero variables, en las tres rondas y las 6,471 columnas, contienen `confianza` ni `confía`. ENASEM no tiene batería de confianza interpersonal ni institucional de ningún tipo — a diferencia de ENCUCI (reactivo activo de `radio_confianza` hoy) y de ENBIARE (candidato de `ABRIR-4`, Apartado B). **ENASEM no contribuye nada a la fila 14**, ni como reactivo ni como llave — no hay relación que una llave pudiera cubrir porque no hay reactivo que identificar.

**Familismo_obligacion (fila 13): negativo, con un falso candidato descartado explícitamente.** El único hit de `obligacion` es un ítem de personalidad general (responsabilidad/conscienciosidad, batería Big-Five de seis afirmaciones, `sect_a_c_d_f_e_pc_h_i` en 2018), no un ítem sobre el deber de cuidar a la familia. Es exactamente el tipo de error que `ADR-52 A` ya penalizó una vez (`P5_23` de ENIF, nombre sugerente sin texto que lo sostenga) y que `ABRIR-4` evitó a propósito con `CONF_FINAN` de ENSAFI (sin texto, no se selló `EXISTE-SATISFACE`) — aquí el texto **sí** existe y **sí** descarta la equivalencia: "cumplir obligaciones" en sentido de responsabilidad personal no es lo mismo que "deber de cuidar a los padres/cónyuge/hijos" (el ítem de `ENASIC P7_12_7` que `ABRIR-4` sí encontró). **ENASEM no contribuye ningún candidato a la fila 13.**

**Familismo_apoyo (fila 12): sin candidato de confianza/obligación, pero con una precondición de panel real — declarada, no ejercida.** La Sección G de ENASEM (idéntica en las tres rondas) mide transferencias intergeneracionales extensamente: `G17` — *"En los últimos dos años, ¿usted (o su cónyuge) ha recibido ayuda en dinero o en especie de cualquiera de sus hijos y/o nietos (y los de su cónyuge)?"* — presente con **redacción casi idéntica en las tres rondas** (`G17` 2018/2021, `G17_24` 2024, verificado directamente en las tres hojas `sect_g_j_k_sa`/`SECT_G_J_K_SA_2021`/`TR_ENASEM24_SECT_G_J_K`), y el identificador de persona `UNHHIDNP` persiste en las tres (verificado en la hoja `archivo_maestro_seguimiento`/`MASTER_FOLLOW_UP_FILE_2021`/`TR_ENASEM24_MASTER_FOLLOW_UP_FI` de cada ronda). Esto es **más** de lo que `Encargo S` (paso 1, 4/ago) documentó — esa sesión solo verificó `G17` en 2018→2021; este acto confirma la misma pregunta en la tercera ola (2024), que no existía en disco cuando `Encargo S` corrió.

Esto satisface, **como precondición estructural**, la clase (i) de ADR-57(c) — panel, mismos sujetos, con un ítem de apoyo familiar recibido presente en el instrumento a través de tres olas. **No** satisface, por sí sola, la compuerta: no hay aquí un diseño de identificación corrido (ningún corte intra-persona, ningún falsador pre-registrado), exactamente la misma situación que `CAL-G3` tiene para `horizonte_temporal` (fila 5, única `RUTA-I` del censo — "llave sellada, payload ya en disco... falta el diseño intra-persona, no un instrumento nuevo"). **Este acto NO promueve la fila 12 a `RUTA-I`** — sería exactamente el error que la addenda prohíbe (regla 1, Bloque A-bis: convertir una precondición en llave sin el diseño). Se deja como propuesta declarada en §11, con la salvedad honesta de que **no se verificó aquí** si `G17` (recibir ayuda) es el mismo constructo operacional que `familismo_apoyo` (0.50, G5) necesita como reactivo o como desenlace — es, en el mejor de los casos, un candidato de **desenlace** panel (cambio en recepción de apoyo entre olas), no un reactivo que prediga ese cambio; qué reactivo intra-persona podría acompañarlo no se examinó en este acto.

**Términos negativos adicionales corridos para las otras 6 filas `SIN-RUTA` (fuera de G5), reportados en §5 fila por fila:** `riesgo`/`arriesg` (0), `estatus` (0), `aparien` (1, discriminación por apariencia — constructo distinto de comparación de estatus), `vecin` (10, todas de contacto social, no comparación de estatus), `obedien`/`jerarqu`/`iniciativ`/`autoridad`/`deferenc`/`retroalimentacion` (0 cada uno).

---

## 5 · Las tres preguntas, aplicadas — universo declarado para las 9 filas `SIN-RUTA`

Formato por fila: **(A)** ¿hay reactivo? — **(B)** ¿co-observado con desenlace, mismo instrumento/muestra? — **(C)** ¿llave ADR-57(c)? — **clase resultante**.

**Fila 3 (G2, `sens_estatus`) y fila 11 (G4, `sens_estatus`, mismo parámetro).** (A) `NO-ENCONTRADO` — buscado en ENSAFI (369 encabezados crudos), ENFIH (838 variables), ENASIC (1427), ENBIARE (2326 líneas) por `ABRIR-4`, y en ENASEM (6,471 variables) por este acto: `estatus`/`aparien`/`comparar`/`vecinos`/`marca` = 0 relevante en los cinco. (B) no aplica sin (A). (C) sin relación que cubrir. **Universo:** ADR-54 sella "búsqueda cerrada, límite de régimen" sobre los cinco instrumentos originales (ENIGH/ENIF/ENCIG/ENCUCI/ENVIPE); `ABRIR-4` examinó cuatro instrumentos más (ENSAFI/ENFIH/ENASIC/ENBIARE) sin candidato; este acto examinó ENASEM (tres rondas) sin candidato. Ninguna de las tres llaves de `gobernanza:623` cubre comparación de estatus por consumo/apariencia: ENNViH/MxFLS no porque su ficha `CAL-G3` cubre horizonte temporal, no estatus · ENASEM no porque, verificado en este acto, no trae ningún ítem de comparación de estatus/apariencia frente a vecinos · ENOE no porque es elegible solo para desenlaces laborales, y `sens_estatus` no es un desenlace laboral. **Clase: `SIN-RUTA` — sin cambio.**

**Fila 4 (G2, `aversion_riesgo`) y fila 6 (G3, mismo parámetro).** (A) `EXISTE-NO-SATISFACE` — ENSAFI trae `CONF_FINAN`/`IMPULSIVID`/`GRA_CONTROL`/`ORIEN_FUT` con valores reales pero sin texto de pregunta recuperable en el corpus (`ABRIR-4`); ENFIH trae tenencia de seguro (producto, no actitud); ENASEM (este acto): `riesgo`/`arriesg` = 0 en 6,471 variables. (B) no se puede evaluar sin texto verificable. (C) sin relación que cubrir. **Universo:** ADR-52 A sella "búsqueda cerrada" sobre el candidato único examinado entonces (ENIF `P5_23`/`P5_24`); `ABRIR-4` examinó cuatro instrumentos más, cero candidatos nuevos con texto verificable; este acto examinó ENASEM, cero coincidencias de raíz. Ninguna llave de `gobernanza:623` cubre aversión al riesgo: ENNViH no trae esta batería (no revisado aquí en profundidad, fuera de perímetro — `CAL-G3` es sobre horizonte temporal) · ENASEM no porque no tiene el reactivo · ENOE no porque es solo laboral. **Clase: `SIN-RUTA` — sin cambio.**

**Fila 10 (G4, `horizonte_temporal`).** (A) `EXISTE-NO-SATISFACE` — ENBIARE trae `PA6`/`PA3_08` (escalera de vida a 5 años, satisfacción con perspectivas a futuro), reactivo limpio y verificado (`ABRIR-4`); ENASEM (este acto): `futuro` (34 hits) y `plazo` (11 hits) son en su enorme mayoría preguntas de productos financieros (depósitos a plazo fijo, ahorro) o de ayuda familiar futura, no una batería de horizonte/expectativa comparable a la de ENBIARE. (B) el candidato de ENBIARE **no** tiene desenlace de G4 (violencia/justicia) co-observable en el mismo instrumento — ENBIARE no trae bateria de victimización ni justicia (`ABRIR-4`, verificado). ENASEM tampoco trae desenlace de G4. (C) sin relación que cubrir. **Universo:** el reactivo de ENIF (`P4_10`) falla C3 frente al desenlace de G3 (fila 5); ENBIARE aporta un reactivo limpio de horizonte/expectativa (nuevo desde el 4/ago) que **no resuelve** la fila porque le falta el desenlace de G4, no el reactivo — se declara el refinamiento sin forzar un cambio de clase. Ninguna llave cubre esta relación concreta: ENNViH/MxFLS cubre horizonte temporal solo para G3 (`CAL-G3`, desenlace de crédito del hogar), no para G4 · ENASEM no tiene desenlace de G4 · ENOE es solo laboral, y G4 no es un desenlace laboral. **Clase: `SIN-RUTA` — sin cambio, universo enriquecido con el reactivo de ENBIARE declarado como insuficiente por sí solo.**

**Fila 12 (G5, `familismo_apoyo`) — RECLASIFICA.** (A) `EXISTE-SATISFACE` — `ENBIARE 2021`, `PB2_1`: *"En caso de que se le presente una urgencia o necesidad, ¿considera usted que siempre contará con la ayuda de personas de su familia?"* (Sí/No/No tiene familia), tabla `TENBIARE`, n=31,166 (`ABRIR-4`, verificado). No hereda la marca C3 del candidato actual (`ENIF p9_9_4`, circular con el desenlace de G5). (B) `SÍ` — Apartado F (`PF1_1..6`, dificultades económicas: pedir prestado para alimentos/renta/agua/luz/colegiaturas/medicinas), misma tabla `TENBIARE`, mismo folio/hogar/persona. **Con reserva declarada, no oculta:** `PF1_*` no es el desenlace formalmente nombrado de G5 (`familia.seguro.volatilidad_ausencia_estado`, que hoy vive en ENIF vía `P9_9_1..6`) — es un desenlace estructuralmente análogo (dificultad financiera del hogar) en un instrumento distinto; la equivalencia de constructo **no está verificada**, queda para que mesa la adjudique (mismo criterio que `ABRIR-4` ya declaró para esta fila). (C) `NO` — ENBIARE no es panel (inferencia estructural de `ABRIR-4`, ningún diccionario de los cuatro declara panel/corte transversal explícitamente), no hay grupo de comparación de experimento natural, no es diseño de terceros. ENASEM (este acto) **sí** ofrece una precondición de panel real (§4: `G17`, tres olas, `UNHHIDNP` persistente) para un desenlace de apoyo familiar recibido — pero sin diseño intra-persona corrido, no se sella como llave ejercida ni como `RUTA-I`; se propone en §11. **Clase: `SIN-RUTA` → `RUTA-C` (con desenlace candidato no formalmente nombrado en el motor — equivalencia de constructo no verificada, decisión de mesa; y con una precondición de panel en ENASEM declarada como candidata a diseño futuro, no como llave ejercida).**

**Fila 13 (G5, `familismo_obligacion`) — RECLASIFICA.** (A) `EXISTE-SATISFACE` — `ENASIC 2022`, `P7_12_7`: *"Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos"* (acuerdo/desacuerdo), tabla `TPER_ELE`, n=5,579 (`ABRIR-4`, verificado — hallazgo más fuerte del acto original). Candidato secundario más débil: `P6_38` (posible batería incompleta, no perseguido). (B) `SÍ` — la misma batería `P7_12` y la Sección `P6.x` (horas dedicadas, tareas específicas, corresidencia) miden conducta de cuidado real dentro del mismo instrumento, misma tabla. Reserva declarada: el desenlace es "conducta de cuidado" (dominio de cuidados), un constructo cognado pero no idéntico al desenlace de G5 (`familia.seguro.volatilidad_ausencia_estado`, que es sobre pooling económico/seguro ante ausencia del Estado, no reparto de tareas de cuidado) — mismo tipo de reserva que la fila 12. (C) `NO` — ENASIC es corte único (no panel), sin llave. ENASEM (este acto) no aporta nada: cero ítem de obligación familiar (§4). **Sigue sin magnitud asignada** (ADR-30, único de los 15 sin ella): tener reactivo por primera vez no da valor que calibrar — eso queda para un acto propio, y se anticipa aquí para que no se lea como fracaso de este censo. **Clase: `SIN-RUTA` → `RUTA-C` (con la misma reserva de desenlace-no-formal que la fila 12; sin magnitud asignada, sin cambio en esa condición).**

**Fila 14 (G5, `radio_confianza`, fila estructural — puente entre instrumentos) — RECLASIFICA.** (A) `EXISTE-SATISFACE` — `ENBIARE 2021`, `PB1_01`/`PB1_02` (confianza generalizada/conocida, 0-10, batería de 12 ítems incluyendo confianza institucional por nombre), tabla `TENBIARE`, n=31,166 (`ABRIR-4`). (B) `SÍ` — `PF1_1..6` (dificultades financieras) en la misma tabla, mismo folio/hogar/persona: satisface estructuralmente lo que hoy falla entre ENCUCI (reactivo activo de `radio_confianza`) y ENIF (desenlace de G5) — instrumentos sin muestra común. Reserva explícita, no verificada aquí ni por `ABRIR-4`: si `PB1_01`/`PB1_02` miden el mismo constructo que `radio_confianza` tal como está operacionalizado hoy con ENCUCI `AP5_1_1/2/3` — decisión de mesa. (C) `NO` — mismo régimen que la fila 12/13, ENBIARE no es panel. ENASEM (este acto) **no aporta nada**: cero variables de confianza en las tres rondas (§4) — negativo definitivo, la llave de panel de ENASEM no puede cubrir esta relación porque el reactivo mismo no existe en el instrumento. **Clase: `SIN-RUTA` → `RUTA-C` (con la reserva de equivalencia de constructo frente a ENCUCI declarada, no verificada; ENASEM descartado como fuente de reactivo, definitivamente).**

**Fila 15 (G6, `deferencia`).** (A) `NO-ENCONTRADO` para ambos desenlaces (`trabajo.jerarquia.deferencia_iniciativa_suprimida`, `comunicacion.retroalimentacion.privada_publica_capital_social`) dentro de Latinobarómetro (único proxy de θ, per v1.0) — `ABRIR-4` no examina Latinobarómetro (fuera de sus cuatro instrumentos), no aporta evidencia nueva aquí. ENASEM (este acto): `obedien`/`jerarqu`/`iniciativ`/`autoridad`/`deferenc`/`retroalimentacion` = 0 en 6,471 variables — negativo limpio, ENASEM no tiene ningún ítem de jerarquía/deferencia/iniciativa. (B)/(C) no aplican sin (A). **Universo:** `forense/notas/2026-08-01-p2-momentos-atributos.md:233` ya cerró esta búsqueda antes de este censo — "§3.2 es PRIORITARIO: las 8 fuentes en 'No' para `trabajo.jerarquia.deferencia_iniciativa_suprimida`; ENOE solo `P3A` (¿tiene jefe?), que el propio inventario clasifica 'cuenta como No de desenlace'" — ENOE, pese a ser elegible para desenlaces laborales (`gobernanza:623`), ya fue examinado y descartado para este desenlace específico antes del 4/ago. Ninguna llave de `gobernanza:623` cubre deferencia: ENNViH/MxFLS no porque su llave viva es sobre horizonte temporal (`CAL-G3`), no jerarquía · ENASEM no porque, verificado en este acto, no tiene el constructo en ningún ítem · ENOE no porque su único candidato cercano (`P3A`) ya se descartó formalmente antes de este censo, y el resto del instrumento no se re-examina aquí (sería re-abrir una búsqueda ya cerrada sin evidencia nueva). **Clase: `SIN-RUTA` — sin cambio.**

**Contador de este commit: 9 de 9 filas `SIN-RUTA` con universo declarado en la celda.** Objetivo del encargo, cumplido.

---

## 6 · Contador primario — cuántas de las 15 filas están contradichas (el titular, antes del reparto)

**Definición operacional, declarada antes de contar:** una fila del censo v1.0 está "contradicha" si su clasificación original se apoyó en la premisa de que no había reactivo/candidato disponible ("Ninguna llave aplica"/"búsqueda cerrada"/similar) y `abrir4-variables-2026-08-08.tsv` o `relaciones.tsv` muestran, para esa misma fila, `EXISTE-SATISFACE` en un instrumento que ya estaba en disco y en el manifiesto al 4/ago.

Por esa definición: **3 de 15 filas contradichas — las filas 12, 13 y 14**, exactamente las tres que la hipótesis original del encargo señaló antes de mirar el dato (§2.4 del borrador retirado, preservado en la memoria de la sesión ejecutora). Las filas 3, 4, 6, 10, 11 y 15 **no** están contradichas: `ABRIR-4` las examinó (salvo la 15, fuera de su alcance de cuatro instrumentos) y **confirmó** el negativo del censo v1.0, no lo revirtió — universo más rico, misma clase. Ninguna de las tres filas `RUTA-A` (1, 2, 7) ni las dos `RUTA-C` (8, 9) ni la única `RUTA-I` (5) están tocadas por `abrir4`/`verif3`/`relaciones.tsv` en este acto — fuera del universo de necesidades que esos registros cubren.

**Segunda fuente, independiente, mismo resultado — con una nota de precisión sobre la addenda.** `data/curacion-registro/relaciones.tsv`, filas para `N12`/`N13`/`N14` cruzadas con `ENBIARE`/`ENASIC`:

```
$ awk -F'\t' '$2=="N12"||$2=="N13"||$2=="N14"' data/curacion-registro/relaciones.tsv \
  | awk -F'\t' '$3=="ENBIARE"||$3=="ENASIC"{print $1"  "$2"  "$3"  capa4="$12}'
REL-010587549b42b447e0b551cc  N14  ENASIC   capa4=EXISTE-NO-SATISFACE
REL-4a609c6633a4bafac14a6930  N12  ENBIARE  capa4=EXISTE-SATISFACE
REL-51392f82de7f4c77d1bb75c1  N14  ENBIARE  capa4=SIN_APERTURA_EXPLICITA
REL-54217cb006dcd63c00de2f24  N12  ENASIC   capa4=EXISTE-NO-SATISFACE
REL-5741e12ce3e0a0e076ee48fc  N14  ENBIARE  capa4=EXISTE-SATISFACE
REL-a65a1433cd0298e7256aefae  N13  ENBIARE  capa4=NO-ENCONTRADO
REL-a750d90d3d9e1e19938fa8c4  N12  ENBIARE  capa4=SIN_APERTURA_EXPLICITA
REL-fe202a3fa76f0516a6e27f8b  N13  ENASIC   capa4=EXISTE-SATISFACE
```

**La addenda citó solo las tres filas `EXISTE-SATISFACE` (verificadas, correctas) — no las otras cinco, que también existen para las mismas necesidades y no contradicen nada.** `relaciones.tsv` registra más de una fila por par (necesidad × fuente) porque distintas combinaciones de reactivo/desenlace se prueban por separado: para `N14`×`ENBIARE` hay dos filas (una `EXISTE-SATISFACE`, la de `PB1`/`PF1`; otra `SIN_APERTURA_EXPLICITA`, un candidato distinto no abierto); para `N12`×`ENBIARE` igual (una `EXISTE-SATISFACE`, otra `SIN_APERTURA_EXPLICITA`); `N12`/`N14`×`ENASIC` y `N13`×`ENBIARE` son negativos, consistentes con que `ABRIR-4` no encontró candidato de `familismo_apoyo`/`radio_confianza` en ENASIC ni de `familismo_obligacion` en ENBIARE. **No hay contradicción entre las dos fuentes** — donde ambas hablan de la misma relación, coinciden.

**Correcciones a dos cifras de la addenda, verificadas contra el repo, no copiadas:**

1. `git log -- data/curacion-registro/relaciones.tsv` da **dos** commits, no uno: `16180e6` (baseline, 7/ago) y `1cd2797` (`ACTO ENLACE-1`, fusionado a `main` después de `b17a6f6` — el propio `ENLACE-1` corre en paralelo a este acto). El segundo añade 19 filas ISSP/WVS/CSES; ninguna toca `N12`/`N13`/`N14` (verificado por el mismo `awk` de arriba, corrido tras el refresh de esta sesión) — sin impacto en el hallazgo, la cifra "un solo commit" simplemente quedó vieja entre que se escribió la addenda y esta sesión la ejecutó.
2. `data/cola-adquisicion-2026-08-12.tsv`, columna `destraba_sin_ruta`, sí trae la fila `SI (censo fila 12,13,14; N12,N13,N14)` — pero pertenece a la fila `fuente_canonica=ISSP` (no a ENBIARE/ENASIC), con `clasificacion_a4_previa=CANDIDATAx13+NEGATIVAx1` — es decir, **ISSP** (módulo Social Networks, corriendo hoy vía `APERTURA-ISSP` en paralelo a este acto) se propone como otro candidato posible para las mismas tres necesidades, sin resolver ("falta verificar texto mexicano..."), y **no** es la misma evidencia que `ABRIR-4`/`relaciones.tsv` ya resolvieron. Hay también una fila `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014` (evaluación aleatorizada del Banco Mundial) con `destraba_sin_ruta=SI (censo fila 13; N13)`, clasificación `CANDIDATA(APERTURA_INDETERMINADA)` — un candidato de **clase (iii)** de ADR-57(c) (diseño experimental de terceros) para la fila 13, **sin resolver, no examinado por este acto** (fuera de perímetro: este acto no abre microdato ni evalúa evidencias externas nuevas; se declara su existencia porque callarla sería el mismo defecto de conducto que este acto existe para cerrar). Se deja nombrado en §11 para que un acto futuro lo examine — sería, si se confirma, la primera llave de clase (iii) que el programa tendría, y específicamente para la única fila sin magnitud asignada de los 15.

---

## 7 · Verif3 — declarado, sin relación con este censo

Las cuatro filas de `data/verif3-variables-2026-08-08.tsv` (`R7.3`-`R7.5`, `R8.1`, `R2.1`/`R10.2`) se leyeron completas per instrucción del encargo ("mismo tratamiento, mismo defecto de conducto"). Las cuatro son `EXISTE-NO-SATISFACE` sobre reglas del Hito D ajenas a los 15 coeficientes de generador (ACLED, Padrón Único de Bienestar, Contraloría Social, ECCO) — ninguna cita `milpa/procedencia.yaml` ni ninguno de los generadores G1-G6. No aporta ninguna fila a §5/§6 de este acto. Se declara la lectura completa y el negativo, no se omite, per el encargo — pero no cambia ningún número de este censo.

---

## 8 · Defecto de nombre de archivo (T02) — evitado, no reparado después

El encargo pedía escribir `forense/notas/2026-08-13-censo-v1_1.md` como nombre de la nota de este commit. El propio archivo de este encargo (`forense/encargos/2026-08-13-censo-v1_1.md`) tiene el **mismo nombre base**. `tests/check.py::t02_duplicates` normaliza por `os.path.basename` (quita acentos, minúsculas, no-alfanumérico) **sin considerar el directorio** — los dos nombres colisionarían exactamente, mismo mecanismo de defecto que ya mordió a `ABRIR-4` (`forense/notas/2026-08-08-abrir4.md` vs. `forense/encargos/2026-08-08-abrir-4.md`, colisión por la posición de un guion) y a `ÍNDICE-2`/PR #156 (mismo patrón). En los dos precedentes, el defecto se descubrió **después** de romper la suite y exigió autorización de mesa para desviar el perímetro y renombrar. Este acto lo evita antes de escribir: la nota de este commit se llama `forense/notas/2026-08-13-censo-v1_1-abrir4-enasem.md` en vez del nombre literal del encargo — desviación mínima, declarada aquí, del perímetro `ESCRIBE` (§2 de la versión operativa dice "1 nota", sin fijar el nombre exacto como requisito de aprobación; el archivo del encargo sí tiene nombre fijado por convención A.3 y no se toca). Verificado que no colisiona con ningún otro archivo del repo por el mismo mecanismo (`grep` sobre nombres normalizados de `forense/notas/` y `forense/encargos/` con fecha `2026-08-13`, sin otro par coincidente).

---

## 9 · Pre-registro de falsación (B-bis) — resultado real vs. lo anticipado

Lo que la versión operativa (§3.4) anticipó, contrastado con lo que ocurrió:

- *"Las tres filas de G5 cambian con alta probabilidad... pero no a RUTA-I."*  **Ocurrió exactamente así.** Las tres (12, 13, 14) reclasifican a `RUTA-C`, ninguna a `RUTA-I`.
- *"Si el vocabulario de cuatro rutas no tiene clase para 'co-observación disponible, no corrida', repórtalo; no fuerces."* **No fue necesario forzar nada ni inventar clase nueva.** `RUTA-C`, tal como el propio v1.0 la define en su §1 ("existe un reactivo... y un desenlace candidato, co-observables en principio dentro del mismo instrumento — pero la corrida no se ha ejecutado"), **ya es** exactamente esa clase — las filas 8 y 9 del v1.0 son precedente directo (reactivo + desenlace "Parcial", corrida no ejecutada). La addenda sugería que ninguna clase encajaría; releída con cuidado la definición propia del v1.0, sí encaja, con el matiz declarado en §5 de que el desenlace no es el formalmente nombrado del motor (matiz que las filas 8/9 no cargan, porque su desenlace sí es un `id` nombrado en `modelo-decision-v4_0.md` — diferencia real, documentada con el calificador "(con desenlace candidato no formalmente nombrado)"). Se reporta como corrección de la premisa de la addenda, verificada contra la fuente, no como desacato.
- *"Si ENASEM no aporta ninguna llave: cierre legítimo."* **Así fue para las filas 13 y 14** (negativos definitivos, §4). **Para la fila 12, ENASEM aporta una precondición de panel real** (no una llave ejercida) — resultado intermedio no anticipado en el pre-registro, que se declara aquí sin forzarlo hacia ninguno de los dos extremos previstos.
- *"La fila 13 probablemente siga sin calibrarse aunque tenga reactivo."* **Correcto.** ADR-30 sigue vigente, sin magnitud asignada; el nuevo reactivo (`ENASIC P7_12_7`) no cambia esa condición.
- *"Si alguna fila resulta que ya tenía evidencia... cuéntalas, va en el titular."* Hecho — §6, 3 de 15.

**El primer resultado que produzca este procedimiento es el que se reporta.** No hubo una segunda corrida ni un segundo criterio: las tres preguntas de §3.2 de la versión operativa, aplicadas una vez a cada una de las 9 filas, con las fuentes citadas arriba.

---

## 10 · La propuesta para la estación 3 (§3.5) — lista para firmar, no firmada aquí

**Ninguna fila cambia a `RUTA-I`.** Por la regla de precedencia sellada en la addenda ((B) sin (C) no es identificación) y porque, verificado en §4, ENASEM no aporta una llave ejercible para ninguna de las tres filas de G5 (dos negativos definitivos, una precondición sin diseño) — **este acto no tiene ninguna propuesta de cambio para `forense/registro-llaves-identificacion-v1_0.md`.** Su tabla de §3 (dos filas: `CAL-G3` + `R5.1-D2`, contador `0 de 2`) **no se toca y no hay diff que proponer** — la propia receta de conteo de ese archivo (§4: contar `EJERCIDA_*` en la columna `estado`) no tiene ningún insumo nuevo de este acto, porque ninguna fila alcanzó el estado `SELLADA_NO_EJERCIDA` (que exige llave ADR-57(c) sellada, no solo candidato de asociación).

Lo que sí queda como propuesta, para que un acto **futuro** (no este) la persiga si mesa lo autoriza:

1. **Diseño de panel para la fila 12 sobre ENASEM** (§4/§5): reactivo por definir + `G17` (recepción de ayuda de hijos/nietos) como desenlace candidato, tres olas (2018/2021/2024), `UNHHIDNP` como llave de persona. Requeriría su propio pre-registro (qué reactivo, qué estimador intra-persona, qué umbral) — mismo tipo de trabajo que `CAL-G3` ya hizo para la fila 5. No es instrumento nuevo; es diseño no concedido aquí.
2. **El candidato de clase (iii) para la fila 13** (§6, `EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014`, Banco Mundial): sin examinar por este acto, nombrado en `data/cola-adquisicion-2026-08-12.tsv` con clasificación previa `APERTURA_INDETERMINADA`. Si resultara viable, sería la primera llave de clase (iii) que el programa tendría, sobre la única fila de los 15 sin magnitud asignada.
3. **Los candidatos ISSP** para N12/N13/N14 (`data/cola-adquisicion-2026-08-12.tsv`), con reserva propia ya escrita en esa tabla ("no es panel; falta mapear texto, forma y si las conductas están referidas al propio hogar") — corriendo hoy vía `APERTURA-ISSP` en paralelo, no examinados aquí.

Ninguna de las tres es una llave sellada. Las tres son candidatas nombradas con su archivo:línea, para que mesa decida si autoriza el acto que las perseguiría — que es exactamente lo que P4 pide de la estación 3 cuando no se alcanza: la razón escrita, no el silencio.

---

## 11 · Lo que este commit NO hace

No abre microdato (ni un `.zip`, ni un `.csv`, ni un `.dbf`) — solo los diccionarios `_fd_xlsx`/`_fd_pdf` ya citados por `ABRIR-4` o abiertos por este acto. No mueve `milpa/procedencia.yaml`. No mueve el contador `0 de 2` de `registro-llaves-identificacion-v1_0.md` (§10, arriba: no hay propuesta de movimiento, solo candidatos sin llave). No amplía la lista de llaves de ADR-57(c). No adjudica ninguna ficha del Hito D. No edita `censo-estimabilidad-coeficientes-v1_0.md` ni ningún TSV de `abrir4`/`verif3` (solo lectura). No resuelve los candidatos ISSP/Banco Mundial de §10 — los nombra y los deja para acto propio.
