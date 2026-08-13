# ENASIC-SPLIT — verificación de los dos supuestos detrás de "dos medidas donde hoy hay una"

**Acto:** ENCARGO ENASIC-SPLIT · **Entorno:** CAJA con corpus (Ubuntu/WSL local) · **SHA de redacción del encargo:** `19d885d` (`origin/main`) · **Depende de:** ADR-67(b) (`canon/gobernanza-v1_15.md:866`), sellado — este acto propone enmendarlo, no lo aplica ni lo sella.

Este commit (1) fija qué se busca y con qué criterio, antes de abrir `enasic2022/889463927082.pdf` o `enasic_2022_fd.xlsx` de primera mano en este acto. No corre ningún cómputo. Ningún resultado vive en este commit.

## §0 · Premisas verificadas (ARRANQUE + verificación de premisas del encargo)

**Arranque crudo.** Worktree dedicado `~/mm-enasic-split`, rama `enasic-split`, creado con `git worktree add ... origin/main` desde `/home/pc0/Modelado-Mexicano`. `git worktree add` emitió el error conocido de contención de `.git/config` en esta máquina (`error: could not write config file .git/config: Device or resource busy`, ×2) — verificado sin pérdida: a diferencia de otras ocurrencias de este defecto en este corpus, aquí el tracking sí completó (`branch 'enasic-split' set up to track 'origin/main'`), y `git worktree list` / `git log -1` confirman `HEAD = 19d885d = origin/main`, sin divergencia. `data/raw` ausente en el worktree fresco (gitignorada, normal), enlazada a `/home/pc0/mm-corpus/raw` — mismo mecanismo que todo worktree hermano (`mm-capa3-reconcilia`, `mm-w-r-tres-encargos`, `mm-p-lote2`, `mm-censo-v1_1`, verificado por `readlink` antes de replicar).

**Firma de entorno, tres partes (Bloque D-ter A.2), cruda:**
```
[1] CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable
[2] curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/  ->  200
[3] ls data/raw/ 2>/dev/null | head -1  ->  BD_ENCUCI2020_dbf.zip  (75 entradas en total)
```
Consistente con "Entorno: CAJA con corpus" declarado por el encargo — corpus montado y poblado, red alcanzable, sin variable de entorno de nube.

**Apertura de sesión** (`python3 tests/bitacora.py --abre`): `HEAD == origin/main`, sin divergencia. `check.py --baseline`: exit=0, LÍNEA BASE VERDE (HEAD congelado `948ad70343320b62f000d31fd39e2b2b68336ad9`). `validador_registro_ids.py`: OK, 49 reglas, 27 en perímetro. **Defecto encontrado, no perseguido más allá (regla de señal v2.3 — una línea, ver `forense/hallazgos.md`):** el script reportó la "versión de instrucciones vigente" como v2.3, commit `7706e3c`. Verificado contra el código (`tests/bitacora.py:124`): lee `instrucciones-proyecto-v2.md` (nombre sin versión, obsoleto) en vez del `vN` más alto presente en el repo. `instrucciones-proyecto-v2_6.md` (271 líneas, hasta Bloque D-ter/v2.6) existe en el repo raíz y es lo que efectivamente rige esta sesión — verificado por lectura directa, no por lo que el script reportó. Mismo patrón que `I-16` (self-report de versión desactualizado), no se corrige aquí (fuera de perímetro de este acto).

**Colisión — ningún acto concurrente detectado.** `git worktree list` (clon `/home/pc0/Modelado-Mexicano`) y `git worktree list` (clon `/home/pc0/proyectos/Modelado-Mexicano`, el segundo clon independiente que este programa ya sabe que existe): ninguna rama con `enasic`/`familismo`/`p6_38`/`p7_12` en su nombre fuera de esta propia. Ningún `forense/encargos/*.md` con `Estado: VIVO` toca ENASIC.

**Verificación de premisas del encargo contra archivo** (regla v2.1 — se verifica antes de ejecutar, no se hereda):

- **ADR-67(b) existe y dice lo que el encargo asume** (`canon/gobernanza-v1_15.md:866`, leído completo): sella `COMPLEMENTAR_PROXY_ENUT` para `familismo_obligacion`, con la reserva de encuadre de género escrita y "sensibilidad con el candidato secundario `P6_38` **si la spec lo admite**" — una medida con una nota lateral, no dos medidas. Confirma la premisa del encargo tal cual.
- **`familismo_obligacion` es 1 de los 14 condicionales** (`canon/modelo-decision-v4_0.md:253`, "`D`=14 condicionales = 8 escalares + 6 componentes de `confianza_institucional`"), y el contador vigente es **9 de 14** `MEDIDO·PARCIAL` (`gobernanza:872,904,938`, ninguno de esos actos lo mueve) — `familismo_obligacion` **no** cuenta entre los 9 porque `requiere_decision_mesa:true` sigue sin resolver (celda-D `G5.familismo_obligacion.actitud.yaml`, campo `requiere_decision_mesa`, leído directo). Confirma exactamente la lectura del encargo: el contador se movería a 10 de 14 cuando mesa firme, no antes, y no por este acto.
- **`P7_12_7` ya tiene θ calculada y verificada** — U1/E4b′ (`forense/notas/2026-08-12-u1-e4b-prime-recorrida.md` §6, **PR #185, confirmado `MERGED` vía `gh pr view 185` — `mergedAt: 2026-08-12T20:57:44Z`**, no "open" como declaraba un registro de memoria anterior de esta asistente, ya desactualizado y no usado como fuente aquí): De acuerdo(Sí)=0.6933 [IC95 0.6725-0.7140], n=5,579, `TPER_ELE`. Esto es lectura de un resultado ya sellado por otro acto (celda-D, `produccion-modelo.tsv`), no apertura nueva de microdato por esta sesión.
- **La cita de ABRIR-4 sobre `P6_38` es casi verbatim, con un detalle no verificado.** Leído directo `forense/notas/2026-08-08-abrir4.md` §6: *"Candidato secundario, más débil, para familismo_obligacion: `P6_38` ('¿usted las cuida por... obligación?'), variable única sin desglose visible de otras razones en el diccionario — posible batería incompleta, no perseguido más allá en este acto."* El encargo la cita coincidiendo palabra por palabra, **salvo que añade "código válido '1'"** — ese detalle específico no aparece en el texto de ABRIR-4 tal como está escrito. No se asume: se verifica directo contra el diccionario en este acto (§1.2 abajo), y se reporta si coincide o no.
- **`data/manifiesto.yaml`, `enasic_2022_889463927082`: el campo existe y dice lo que el encargo cita** (`archivo: enasic2022/889463927082.pdf`, `usado_para: sin uso asignado`) — **pero esa afirmación de "sin uso asignado" es falsa**, mismo patrón ya conocido de este corpus (`usado_para` se escribe una vez y no se re-deriva). `forense/notas/2026-08-11-e4b-sello-b-corrida-b.md` §1 declara en primera persona que E4b abrió este mismo PDF **íntegro** ("el segundo se había abierto solo hasta su §1.1 en DESC-1... este acto lo abre íntegro por primera vez", `pdftotext -layout`, 26 páginas completas) — buscando `periodo_levantamiento`, no la mecánica de lectura de `P7_12_7`. Se reporta como hallazgo de una línea (`forense/hallazgos.md`), no bloquea: el PDF se abre igual, de primera mano, en COMMIT 2, con objetivo distinto al de E4b.
- **"D3"** (línea 2 del encargo, "Cierra D3"): buscado como identificador rastreado de este programa — `canon/gobernanza-v1_15.md`, `canon/modelo-decision-v4_0.md`, `forense/hallazgos.md`, y las tres notas forenses citadas arriba, 13/ago/2026. Las únicas coincidencias literales de "D3" pertenecen a esquemas de numeración local **no relacionados**: ADR-49 (3)/`D3` (homogeneidad de pendientes de `G1a`) y el `D1/D2/D3` propio de MAP-A (denominadores del universo de puertas). Ninguno tiene relación temática con ENASIC, `familismo_obligacion` ni ADR-67(b). Se interpreta como numeración externa de la propia mesa (este acto es el "4·" de una lista de mesa que no vive en este repo) — no bloquea, el resto del encargo es autocontenido y no depende de resolver esta etiqueta.
- **Hallazgo de infraestructura, no perseguido más allá:** `tools/curador_registro/` (el motor formal que E4b/PR #173 y U1/PR #185 corrieron y citan extensamente — `produce.py`, `prepare_production.py`, `integrate_production.py`) **no existe** en `origin/main` HEAD (`19d885d`) ni en la punta de ninguna de esas dos ramas ya fusionadas (`git ls-tree` vacío en ambas). Su única aparición en el historial de todas las ramas es el commit `59d6c40` ("BARRIDO-COMPLETO N1-N33: commit de preservación, cubeta (i)"); sigue presente localmente en algunos worktrees más antiguos (`~/mm-capa3-reconcilia/tools/`) como residuo no versionado o de una base distinta, no investigado más allá — posible relación con `PURGA-PRIVACIDAD`/`remapeo-shas-purga-2026-08-10.tsv` (`canon/`), fuera de perímetro de este acto. **No impide medir aquí**: este acto no depende del motor formal — si `P6_38` sostiene una θ, se calcula con `tests/svystat.py::prop_ultimate_cluster` (presente, trackeado, validado, ver §1.5).

**Declaración de contaminación (mismo criterio que ADR-46, aplicado a este pre-registro).** Esta sesión **no** ha abierto todavía, ni en este acto ni en ningún otro, `enasic2022/889463927082.pdf` ni `enasic_2022_fd.xlsx` de primera mano. Todo lo citado arriba sobre su contenido proviene de notas forenses de actos anteriores (ABRIR-4, E4b) — lectura de segunda mano, marcada como tal, nunca tratada como verificación propia. El §1 de abajo se escribe antes de esa apertura directa.

## §1 · Pre-registro

### 1.1 · Qué se busca en el cuestionario (o su sustituto) para resolver (1)

Se abre `data/raw/enasic2022/889463927082.pdf` completo, de primera mano, con `pdftotext -layout` (mismo método que E4b, no fetch resumido por IA — v2.6 A.6). Primero se determina **qué tipo de documento es**, por su tabla de contenidos y un barrido de términos (`cuestionario`, `guion`, `entrevistador`, `lea:`, `aplica a`, `instrucciones de aplicación`) contra los del tipo contrario (`estructura del archivo`, `descripción de variables`, `diccionario`) — el propio título citado por E4b ("Conociendo la base de datos") sugiere que podría ser documento de orientación de base de datos, no guion de campo; se confirma o se corrige aquí, no se hereda la sospecha como hecho.

- **Si es guion de entrevista real:** se busca la sección/pregunta correspondiente a `P7_12_7` y se lee el texto exacto tal como debe pronunciarse, más cualquier instrucción condicional sobre el sexo del informante (columna o nota de tipo "SI SEXO=1 LEA…SI SEXO=2 LEA…", o dos variantes de texto separadas). Esto sería evidencia directa de **lectura (i)**.
- **Si NO es guion de entrevista** (confirmado documento de estructura/orientación): se declara **NO-ENCONTRADO** el guion de entrevista dentro de `889463927082.pdf` — universo: texto íntegro (todas las páginas), término buscado: los de arriba, fecha: 13/ago/2026 (v2.6 A.4, vocabulario obligatorio). Se sigue entonces la instrucción explícita del encargo: se busca en `enasic_2022_fd.xlsx`, hoja `TPER_ELE`, la fila de `P7_12_7` completa (columnas `Pregunta`/`Nemónico`/`Tipo`/`Tamaño`/`Códigos Válidos`/`Concepto`) — cualquier columna de aplicabilidad, nota de bifurcación, o referencia cruzada a una variable de sexo del informante ya leído cuenta como evidencia de **lectura (i)**; su ausencia total en ambos documentos (PDF íntegro + fila del FD) se declara **NO-ENCONTRADO** con el mismo universo declarado, y se trata explícitamente como **inferencia por ausencia hacia la lectura (ii)** — no como hallazgo positivo de "fórmula genérica" leída en texto. La distinción entre "encontré el texto que dice que es genérica" y "no encontré evidencia de que se bifurque" se mantiene explícita en COMMIT 2, no se colapsan (mismo criterio que separa `EXISTE-NO-SATISFACE` de `NO-ENCONTRADO`).

### 1.2 · Qué se busca en el diccionario para resolver (2)

Se abre `enasic_2022_fd.xlsx` completo vía `openpyxl` (mismo método que ABRIR-4), hoja `TPOB_CUI` (donde E4b ya localizó `P6_38` — `forense/notas/2026-08-11-e4b-sello-b-corrida-b.md` §6 — verificado de nuevo aquí, no heredado).

1. **Fila de `P6_38` completa**, citada verbatim: `Pregunta`/`Nemónico`/`Tipo`/`Tamaño`/`Códigos Válidos`/`Concepto`. Se confirma o corrige el detalle "código válido '1'" que el encargo añade sobre la cita de ABRIR-4 (§0).
2. **Barrido de la Sección 6 completa** en `TPOB_CUI` (no solo filas contiguas a `P6_38` por número — una batería puede no ser contigua) buscando en `Concepto`/`Pregunta` el mismo tallo de pregunta ("¿…las cuida por…?") con desenlaces distintos (cariño, costumbre, no había quien más, cercanía, obligación…). Cualquier fila que comparta el tallo con un final distinto de "obligación" cuenta como variable hermana de batería.
3. **Control de coherencia de codificación:** si no aparecen hermanas y `Códigos Válidos` de `P6_38` es en efecto un único código, se compara ese patrón contra cómo el mismo diccionario codifica una batería de selección múltiple ya conocida en esta hoja o en `TPER_ELE` (p. ej. `P7_12_1`-`P7_12_8`, que SÍ trae 4 códigos oficiales completos por ítem) — para no confundir "posible batería incompleta" con "así es como este instrumento codifica selección múltiple de un solo motivo, y de hecho sí sostiene una proporción bien definida". Se reporta cuál de las dos aplica, con la fila exacta que sirve de contraste.
4. **Universo y denominador:** población de `TPOB_CUI`, columnas de estrato/UPM/ponderador declaradas en esa hoja (se leen, no se heredan de `TPER_ELE` — E4b ya advirtió que `FAC_ELE`/`EST_DIS`/`UPM_DIS` son de `TPER_ELE`, no necesariamente los mismos nombres en `TPOB_CUI`), y si existe un total de personas de `TPOB_CUI` a quienes se les formuló la Sección 6 completa (denominador real) frente a solo quienes ya fueron identificados cuidadores — necesario para saber si una θ, de existir, tendría universo no degenerado.

### 1.3 · Criterio de "dos medidas separables" (escrito antes de mirar)

Dos variables candidatas constituyen "dos medidas separables" si y solo si, **las tres a la vez**:

- **(a) Suficiencia de dato.** Cada variable, por sí sola, tiene universo/población bien definido, estructura de respuesta válida no degenerada (denominador real; idealmente varianza real, no un campo donde solo es codeable un desenlace) y diseño (estrato/UPM/ponderador) declarado — la misma barra que `P7_12_7` ya superó en E4b/U1.
- **(b) Distinción de constructo, nombrada.** Su contenido apunta a constructos conceptualmente distintos, cada uno nombrable en una frase — no basta con que sean ítems distintos. *Norma de género*: creencia normativa/general sobre quién **debe** cargar un deber de cuidado, dirigida a una tercera persona genérica según su sexo ("se debe enseñar a…"). *Obligación medida*: reporte en primera persona de la **propia** motivación de quien ya cuida, condicional a haber sido ya identificado como cuidador/a ("¿usted… por obligación?"). La distinción es norma-sobre-otros/genérica vs. auto-reporte de motivo propio — no meramente "número de ítem distinto".
- **(c) Evidencia textual, no inferida.** La etiqueta de constructo de cada medida se sostiene en el texto literal del ítem y en el encabezado de sección oficial del propio instrumento (`P7_12_7` vive en "Sección 7, Percepción cultural de los cuidados"; `P6_38` vive en Sección 6, dirigida a quien la sección ya identificó como cuidador/a) — no se afirma desde el mnemónico o el número de variable solos.

### 1.4 · Falsación (B-bis)

Tal como el encargo la declara, verbatim, y se pre-registra sin modificar: **si (1) resuelve por lectura (ii) —fórmula genérica—, la partición no es posible con este instrumento, y eso es el resultado; se reporta, no se fuerza.** **Si `P6_38` no sostiene θ (falla el criterio (a) de 1.3), se dice explícitamente, y "obligación medida" queda sin operacionalización — con una frase declarando qué haría falta para tenerla** (p. ej.: un ítem de motivo de cuidado con universo `TPOB_CUI` bien definido y códigos que permitan denominador, hoy ausente del corpus adquirido).

Las dos condiciones son independientes — puede fallar (1), (2), ambas, o ninguna; cada una se reporta por separado, sin que el resultado de una determine el de la otra.

**Glosa propia, declarada como interpretación y no como parte del pre-registro que gobierna el resultado:** no es evidente, antes de ver el documento, por qué la lectura (ii) —fórmula genérica, sin bifurcación por sexo del informante— tendría que impedir la partición: `P7_12_7` seguiría siendo, en su propio texto, un enunciado normativo sobre un deber diferenciado por sexo, y bajo el criterio (b) de arriba eso ya lo distingue de `P6_38` (norma-sobre-otros vs. auto-reporte). La lectura que hace consistente la falsación tal como el encargo la escribe es otra: bajo (i), el acuerdo condicionado al sexo del propio informante habilita un análisis adicional (asimetría de internalización de la norma, comparando el acuerdo de mujeres con "a la mujer" contra el de hombres con "al hombre") que bajo (ii) no existe — y si la mecánica de aplicación no diferencia por sexo del informante, cabe la duda de si el ítem, tal como efectivamente se administra, comunica un contenido de género tan nítido como su texto impreso sugiere, acercándolo conceptualmente a una norma de deber familiar sin marca de género — lo que sí tensiona el criterio (b). Esta nota no resuelve esa tensión por su cuenta: se aplica el criterio del encargo tal como está escrito, y esta glosa se ofrece para que mesa la lea junto al resultado, no en su lugar.

### 1.5 · Método pre-comprometido para "obligación medida", si (2) resuelve positivo

Si `P6_38` supera el criterio de suficiencia (1.3.a), la proporción se calcula con `tests/svystat.py::prop_ultimate_cluster` — presente, trackeado en este repo, validado contra un caso SRS conocido (`_caso_conocido()`, coincide a 9 decimales) — construyendo tuplas `(estrato, upm, peso, y)` desde las columnas de diseño que `TPOB_CUI` declare (a verificar en 1.2.4, no asumidas iguales a `TPER_ELE`) y `y = 1{P6_38 == código de "sí/obligación"}`. **No** se usa `tools/curador_registro/produce.py` (ausente de este checkout, §0) ni se registra una `ESP-OPACA-*` nueva en `especificaciones-produccion.json`. El cuantil usado será `1.959963985` (el que `svystat.py` ya usa), declarado para que el IC95 no se compare dígito a dígito contra el de `produce.py::taylor_distribution` (que usa `1.96`) — mismo aviso que el propio módulo ya deja escrito para sus otras funciones.

### 1.6 · Qué NO se hace en este acto

No sella ni edita `canon/gobernanza-v1_15.md` — el diff de la enmienda a ADR-67(b) se presenta en COMMIT 2 como propuesta (bloque de texto, antes/después), no se aplica. No crea ni edita ninguna celda-D en `data/curacion-registro/celdas-d/`, no registra ninguna especificación nueva en `especificaciones-produccion.json`, no mueve `condicionales 9 de 14` (eso es de mesa, al firmar — §0). Cualquier cómputo que este acto produzca para `P6_38` es propuesta de mesa, no sellado, no registrado en el motor formal — mismo criterio que MAP-A usó para presentar cifras nuevas sin sellar adjudicación.

**El primer resultado que produzca este procedimiento es el que se reporta.**

## §2 · Commit 2 (resultado) — sin editar §0-§1 arriba

Sesión separada, misma rama (`enasic-split`), sobre el mismo `enasic_2022_bd_csv.zip`/`enasic_2022_fd.xlsx` ya verificados `COINCIDE` por ABRIR-4 (§0). Abiertos de primera mano en este acto por primera vez en esta sesión: `889463927082.pdf` (texto íntegro, `pdftotext -layout`), `enasic_2022_fd.xlsx` (hojas `TPER_ELE` y `TPOB_CUI`, vía `openpyxl`), `TPOB_CUI.csv` (microdato, vía `csv.DictReader`, codificación `latin-1`).

### §2.1 · Resultado de (1) — lectura (ii), confirmada por evidencia positiva, no solo por ausencia

`889463927082.pdf` **no es el cuestionario.** Confirmado por su propio índice (Introducción · 1. Características de la base de datos [Objetivo, Conceptos básicos, **Estructura de la base de datos**, Unidad de análisis, **Factor de expansión**, Relación entre tablas, Modelo entidad relación] · 2. Principales poblaciones · 3. Precisiones estadísticas · 4. Principales indicadores · Anexos [código R]) y por barrido de término sobre las 1,251 líneas de texto extraído: `entrevistador`=0, `guion`/`guión`=0, `lea:`=0, `aplica a`=0, `instrucciones de aplicación`=0, `P7_12`=0. `cuestionario` aparece **una sola vez**, y es una remisión explícita hacia otro documento: *"cada pregunta del cuestionario... para un correcto uso de las tablas se consulte el Descriptor de Archivos (FD)"* (línea 191) — el propio documento declara que el detalle de pregunta vive en el FD, no en sus páginas. NO-ENCONTRADO para guion de entrevista dentro de `889463927082.pdf`: universo=texto íntegro (26pp/1251 líneas), términos=los de arriba, mecanismo=`pdftotext -layout` + `grep`, fecha=13/ago/2026 (vocabulario v2.6 A.4).

Siguiendo la instrucción del encargo, se buscó en `enasic_2022_fd.xlsx`, hoja `TPER_ELE`. Fila 713, columna `Pregunta` (definida por el propio FD como *"la pregunta textual del instrumento de captación"*, fila 7), citada verbatim y completa:

> `7.12.7 Le voy a leer unas frases. Usted me responderá si está de acuerdo o en desacuerdo. Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos`

Un **único** mnemónico (`P7_12_7`), un **único** texto de captura, con el paréntesis impreso dentro de la misma cadena — sin columna de bifurcación, sin nota de "SI SEXO=1/2", sin un segundo mnemónico. Contraste directo dentro de la misma estructura: donde el instrumento sí trae dos ítems realmente distintos, usa dos mnemónicos distintos (`P7_12_2` "...responsabilidad de la mujer" vs. `P7_12_4` "...responsabilidad del hombre" — dos enunciados con contenido distinto, cada uno su propia variable). Para `P7_12_7` no hizo eso: un mnemónico, una cadena. Existe una variable `SEXO` en la misma tabla (fila 1058, "Sexo de la persona elegida") — permite un cruce analítico posterior por sexo del informante como cualquier otra variable demográfica, pero no hay ningún campo que registre o condicione qué versión del paréntesis se leyó.

**Esto es evidencia positiva, no solo ausencia:** la propia definición de columna del FD ("la pregunta textual del instrumento de captación") describe esta cadena como lo que efectivamente se captura. **Lectura (ii) — fórmula genérica, una sola versión administrada y capturada — es la que sostiene el diccionario**, con el matiz declarado en §1.1: no se pudo abrir un guion de campo real que confirme qué se dice en voz alta (`889463927082.pdf` no lo es, y no hay otro candidato en el corpus adquirido) — lo que se verifica aquí es lo que el **dato capturado** permite reconstruir, que es una sola respuesta por persona, sin distinción de versión leída.

**Aplicación de la falsación (B-bis), tal como el encargo la declara, sin modificarla:** bajo lectura (ii), **"la partición no es posible con este instrumento"** — se reporta así, no se fuerza. Concretamente: no existe, en este corpus, una vía para reconstruir un `P7_12_7` desdoblado en "versión-mujer" / "versión-hombre" por informante, porque el dato capturado es una sola cadena por persona sin marca de cuál paréntesis se pronunció.

**Glosa propia (interpretación declarada, no sustituye la falsación de arriba — ver §1.4).** Esta falsación específica es sobre un desdoblamiento **interno** de `P7_12_7` (una partición por versión leída dentro de la misma medida) — **no** es, en este acto, lo mismo que la partición que mesa pidió (`P7_12_7` como medida separada de `P6_38`). Esa segunda partición se rige por el criterio de separabilidad de §1.3 (suficiencia + distinción de constructo + evidencia textual), no por la lectura (i)/(ii). Bajo ese criterio distinto, evaluado en §2.3 abajo, `P7_12_7` (norma de género, enunciado normativo de tercera persona sobre un deber diferenciado por sexo) y `P6_38` (obligación medida, autorreporte en primera persona del propio motivo) **sí resultan separables** — la lectura (ii) acota lo que se puede decir sobre `P7_12_7` internamente (no hay asimetría de internalización por sexo del informante reconstruible), pero no colapsa `P7_12_7` en `P6_38` ni viceversa: siguen siendo, textualmente, una norma-sobre-terceros y un motivo-propio-reportado. Mesa decide si esta lectura de "partición" (interna a `P7_12_7`) es la que gobierna el alcance de la enmienda, o si la separabilidad de §1.3 basta — este acto presenta ambas, sin fusionarlas.

### §2.2 · Resultado de (2) — corrige a ABRIR-4: `P6_38` es batería completa de 5 razones, no variable huérfana

**ABRIR-4 (`forense/notas/2026-08-08-abrir4.md` §6) no se sostiene contra verificación directa del diccionario.** Su caracterización — *"variable única sin desglose visible de otras razones en el diccionario — posible batería incompleta"* — describe la fila 1172 de `TPOB_CUI` aislada (`P6_38`, código `1`, concepto `"obligación?"`), pero **las filas 1173-1176, mismo mnemónico `P6_38`, completan la misma pregunta con cuatro razones más**, verbatim:

> `6.38 A las personas que declaró cuidar, ¿usted las cuida por...`
> `1` — `obligación?`
> `2` — `decisión familiar?`
> `3` — `ser la (el) única(o) que podía?`
> `4` — `petición de quien necesita el cuidado?`
> `5` — `iniciativa propia?`

Es exactamente el mismo patrón de fila-por-código que `P7_12_7` (Pregunta/Nemónico en la primera fila, Códigos Válidos/Concepto continuando en las filas siguientes, mismo mnemónico) — ABRIR-4, en un barrido de término de cuatro instrumentos completos, no continuó leyendo las filas siguientes de este hit particular. **No es una batería incompleta: es una variable categórica de elección única, cinco categorías, completa.** Se corrige aquí, no se edita la nota original (append-only) — mismo criterio que ADR-67(b) §(b) ya usó para su propia corrección de hallazgo (`gobernanza:866`).

**Universo.** `FILTRO 6.10` (fila 1170, inmediatamente antes de `P6_38`): *"¿LA (EL) INFORMANTE ES CUIDADOR(A) DE PERSONAS DE SU HOGAR Y/O DE OTROS HOGARES?"* — gatilla la pregunta. Verificado contra el microdato (`TPOB_CUI.csv`, n=5,677): `FILTRO6_10='1'` en el 100% de las filas — la tabla `TPOB_CUI` ya está construida como población cuidadora (definición oficial del PDF, línea 384: *"Población de 15 años y más que, durante la semana anterior a la fecha de referencia, declaró que brindó cuidados a por lo menos una población susceptible"* — discapacidad/dependencia, niñas/niños 0-5, niñas/niños/adolescentes 6-17, personas 60+, o personas enfermas temporales, todas sin discapacidad salvo la primera categoría), así que `P6_38` se formula a la población cuidadora completa de la tabla, sin exclusión adicional — confirmado empíricamente, no solo por lectura de la lógica de filtro. `dominio` = Nacional, mismo criterio ya verificado por E4b sobre el corpus íntegro (`forense/notas/2026-08-11-e4b-sello-b-corrida-b.md` §1: barrido de las 6 hojas + PDF completo, términos "nacional"/"cobertura"/"representa", sin restricción subnacional encontrada — aplica a la encuesta completa, no reverificado hoja por hoja de nuevo en este acto). `periodo_referencia` = "la semana anterior a la fecha de referencia" (declarado en la misma definición de población, línea 384-385) — **distinto** del de `P7_12_7` (momento de la entrevista, sin ventana retrospectiva).

**Completitud del dato, verificada:** `P6_38` no trae código de blanco/no-sabe/no-responde en el diccionario (a diferencia de `P6_36_3`, filas 1163-1165, que sí trae `'b' Blanco por secuencia`) — y el microdato lo confirma: **0 valores en blanco o fuera de {1,2,3,4,5} en las 5,677 filas.** Diseño: `EST_DIS`/`UPM_DIS` (filas 1481-1482, viven directo en `TPOB_CUI`, no requieren unión), `ponderador = FAC_CUI` (fila 1483, "FACTOR HOGAR DE EXPANSIÓN"), mismo patrón que `TPER_ELE`/`FAC_ELE` que E4b ya documentó, verificado aquí de nuevo para `TPOB_CUI` específicamente (nombres de columna no se heredan).

**Cómputo** (`tests/svystat.py::prop_ultimate_cluster`, declarado en §1.5 antes de correr; comando y salida cruda en el historial de esta sesión):

| código | razón | n | proporción | IC95 |
|---|---|---|---|---|
| 1 | obligación | 479 | 0.0765 | [0.0661, 0.0868] |
| 2 | decisión familiar | 366 | 0.0671 | [0.0579, 0.0763] |
| 3 | ser la (el) única(o) que podía | 193 | 0.0356 | [0.0286, 0.0426] |
| 4 | petición de quien necesita el cuidado | 72 | 0.0123 | [0.0083, 0.0162] |
| 5 | iniciativa propia | 4,567 | 0.8086 | [0.7918, 0.8254] |

n=5,677, suma de pesos (`FAC_CUI`)=31,652,127, 148 estratos (0 singleton — sin pérdida de grados de libertad), 861 UPM. Suma de las cinco proporciones puntuales = 1.0001 (redondeo). **`P6_38` sostiene θ**: universo no degenerado, denominador completo, diseño declarado, cinco categorías mutuamente excluyentes con variación real — el criterio de suficiencia (§1.3.a) se cumple, contra lo que ABRIR-4 y el propio encargo (citándola) anticipaban.

**Escala y comparabilidad (Bloque A-bis regla 3).** Distribución descriptiva categórica (5 categorías), diseño muestral (conglomerado último, Wolter). **No** es un coeficiente de índice ni una asociación identificada. **Contra qué no se compara:** el 7.65% de `P6_38` (motivo propio, entre cuidadores ya identificados, ventana de una semana) y el 69.33% de `P7_12_7` (acuerdo con una norma general, población elegida completa, sin ventana retrospectiva) **no se restan ni se comparan como si fueran la misma escala** — universos distintos, preguntas distintas, escalas distintas (proporción-de-acuerdo-con-norma vs. proporción-de-motivo-entre-cinco). Verlas juntas es exactamente el punto de "dos medidas, dos análisis": no se funden en un solo número.

### §2.3 · Separabilidad, aplicando el criterio de §1.3

- **(a) Suficiencia** — ambas cumplen: `P7_12_7` (E4b/U1, ya sellado) y `P6_38` (§2.2, este acto), cada una con universo, diseño y denominador completo declarados.
- **(b) Distinción de constructo, nombrada** — *norma de género* (`P7_12_7`): creencia normativa sobre quién **debe** cargar el deber de cuidar, en tercera persona genérica diferenciada por sexo del sujeto enseñado. *Obligación medida* (`P6_38`): autorreporte en primera persona del motivo **propio** de quien ya cuida, entre cinco razones posibles, sin marca de género en el ítem mismo. Son, textualmente, una norma-sobre-otros y un motivo-propio-reportado — constructos distintos, tal como el criterio exige.
- **(c) Evidencia textual** — `P7_12_7` vive en Sección 7 ("Percepción cultural de los cuidados", batería de acuerdo/desacuerdo con enunciados normativos); `P6_38` vive en Sección 6, dirigida específicamente a quien la propia sección ya identificó como cuidador/a (`FILTRO 6.10`). Ubicación de sección y encabezado oficial, no inferencia por número de variable.

**Los tres se cumplen. Bajo el criterio de §1.3, la partición mesa/encargo (dos medidas: norma de género y obligación medida) procede** — con la reserva de §2.1 sobre qué significa exactamente "partición" en la frase de falsación del encargo (interna a `P7_12_7`, no bloquea esta separación).

## §3 · Las dos medidas propuestas

**Medida 1 — norma de género.**

**Advertencia de procedencia, aplicable a toda la Medida 1 (encontrada al escribir este §, no antes — no estaba en el pre-registro de Commit 1 porque ADR-72 se selló el mismo día y esta sesión no lo había leído hasta ahora).** `canon/gobernanza-v1_15.md:942`, **ADR-72** (sellado 13/ago/2026, ya en `origin/main` antes de que este worktree se abriera): *"Se declara `PROVISIONAL` todo veredicto, coeficiente, contador, reparto y cierre de búsqueda producido por este programa antes del 13/ago/2026 [...] ninguna decisión nueva puede citarlos como asentados."* U1/E4b′ (PR #185) fusionó `2026-08-12T20:57:44Z` — antes del corte. La tabla de abajo **es la misma que ese acto verificó** (Taylor/conglomerado último, reproducción byte a byte por `integrate_production.py`) y no se pone en duda por ADR-72 — pero se cita aquí **como provisional, no como asentada**, tal como ADR-72 exige de cualquier decisión nueva que la use. Además, `forense/registro-recalculo-v1_0.md` entrada `0` ya señala, sin resolver, que `censo-estimabilidad-coeficientes-v1_0.md` clasifica `familismo_obligacion` (N13) `SIN-RUTA` mientras `data/curacion-registro/relaciones.tsv` trae `EXISTE-SATISFACE`/`CONFIRMADA` para la misma necesidad (`REL-fe202a3fa76f0516a6e27f8b`, el mismo `P7_12_7`) — desacuerdo de bookkeeping entre dos tablas del programa, absorbido por CENSO-v1.1 (entrada 1 del registro), **no resuelto ni tocado por este acto.**

Variable: `P7_12_7` (ENASIC 2022, tabla `TPER_ELE`). Texto literal: *"Se debe enseñar a la mujer (al hombre) que su deber es cuidar a los padres, cónyuge, hijas e hijos"* (lectura (ii), fórmula única — §2.1). Escala: acuerdo/desacuerdo, 4 categorías oficiales. Universo: personas de 15-60 años, persona elegida, vivienda particular, Nacional. Tabla (ya calculada y verificada, U1/E4b′, PR #185 MERGED — citada, no recalculada en este acto, **provisional per ADR-72**):

| código | categoría | proporción | IC95 |
|---|---|---|---|
| 1 | De acuerdo (Sí) | 0.6933 | [0.6725, 0.7140] |
| 2 | Desacuerdo (No) | 0.2995 | [0.2788, 0.3203] |
| 8 | No responde | 0.0035 | [0.0009, 0.0060] |
| 9 | No sabe | 0.0037 | [0.0012, 0.0062] |

n=5,579, suma_pesos=80,237,061. Constructo que ampara: creencia normativa sobre deber de cuidado diferenciado por sexo (norma de género), Sección 7 "Percepción cultural de los cuidados".

**Medida 2 — obligación medida.** Variable: `P6_38` (ENASIC 2022, tabla `TPOB_CUI`). Texto literal: *"A las personas que declaró cuidar, ¿usted las cuida por…"* con 5 opciones (obligación / decisión familiar / ser la (el) única(o) que podía / petición de quien necesita el cuidado / iniciativa propia). Escala: categórica, 5 categorías, elección única. Universo: población cuidadora de 15+ años (≥1 población susceptible atendida en la semana de referencia), Nacional. Tabla: ver §2.2 (n=5,677, suma_pesos=31,652,127). Constructo que ampara: motivo autorreportado del propio comportamiento de cuidado ya realizado (obligación medida), Sección 6, condicional a `FILTRO 6.10`.

**Nota de rigor, aplicable a ambas:** ninguna de las dos tablas de arriba es resultado sellado de este acto salvo la de la Medida 2, que sí se calculó aquí (§2.2) — es propuesta para que mesa decida, no registro formal en `data/curacion-registro/` (§1.6, no se crea celda-D nueva ni se registra `ESP-OPACA-*` nueva en este acto).

## §4 · Diff propuesto para ADR-67(b) — PROPUESTA, no aplicado, no sellado por este acto

Texto vigente hoy (`canon/gobernanza-v1_15.md:866`, verbatim):

```diff
- **(b) `DH-332a13a70cbbf875` (N13) → `COMPLEMENTAR_PROXY_ENUT`, con roles declarados.**
- ENASIC `P7_12_7` opera la **θ actitudinal** de `familismo_obligacion` — con la
- reserva del encuadre de norma de género ("enseñar a la mujer/al hombre") escrita
- en la especificación CRES-7cb78abf, y sensibilidad con el candidato secundario
- `P6_38` si la spec lo admite. ENUT 6.11/6.11a queda como **capa conductual**
- (momento m-lado / validación), no como θ: [...]
```

Texto propuesto (inserta una enmienda in situ fechada, mismo mecanismo que este mismo archivo ya usa repetidamente para enmendar un párrafo sellado sin subir el número de versión ni renombrar el archivo — p. ej. la propia ADR-49 (3) trae, en el mismo sitio, un "Corregido 4/ago/2026" fechado que no reemplaza el texto original, lo sigue; no relacionado en tema con "D3" del encargo, §0, solo con la técnica de enmienda — no reemplaza el párrafo original de ADR-67(b), lo sigue):

```diff
  **(b) `DH-332a13a70cbbf875` (N13) → `COMPLEMENTAR_PROXY_ENUT`, con roles declarados.**
  ENASIC `P7_12_7` opera la **θ actitudinal** de `familismo_obligacion` — con la
  reserva del encuadre de norma de género ("enseñar a la mujer/al hombre") escrita
  en la especificación CRES-7cb78abf, y sensibilidad con el candidato secundario
  `P6_38` si la spec lo admite. ENUT 6.11/6.11a queda como **capa conductual**
  (momento m-lado / validación), no como θ: [...]
+
+ *(Enmienda in situ, 13/ago/2026, ENASIC-SPLIT — mismo criterio que ADR-48 a
+ ADR-65: el número de versión no sube, el archivo no se renombra.) `P6_38`
+ deja de ser sensibilidad condicional de `familismo_obligacion` y pasa a
+ medida propia, nombrada: `obligación_medida` (ENASIC 2022, `P6_38`, tabla
+ `TPOB_CUI`, θ categórica de 5 vías, n=5,677 — tabla y verificación en
+ `forense/notas/2026-08-13-enasic-split-verificacion.md` §2.2/§3). El
+ `familismo_obligacion` atitudinal (`P7_12_7`) se renombra en el mismo acto a
+ `norma_de_género` para no seguir compartiendo nombre con una medida que ya
+ no es la misma cosa. Las dos son celdas-D distintas, sin `rol: COMPLEMENTO`
+ entre ellas (mismo criterio que ya separa la celda de actitud ENASIC de la
+ celda de conducta ENUT, `gobernanza:888`) — dos medidas, dos análisis, sin
+ fusión ni jerarquía. Corrección de premisa: la caracterización previa de
+ `P6_38` como "variable única sin desglose de otras razones" (ABRIR-4,
+ `forense/notas/2026-08-08-abrir4.md` §6) no se sostuvo contra el diccionario
+ — es categórica completa de 5 vías (verificado, misma nota §2.2). Pendiente
+ de mesa, no ejecutado por esta enmienda: registrar la celda-D
+ `G5.obligación_medida` (o el nombre que mesa fije) en
+ `data/curacion-registro/celdas-d/`, y decidir si `familismo_obligacion`
+ sobrevive como nombre de generador en `canon/modelo-decision-v4_0.md` o si
+ también se desdobla ahí — este acto no lo decide ni lo toca.*
```

**Firma de mesa:** este bloque es el que mesa firmaría, tal como está, o con los cambios que decida — este acto no lo aplica a `canon/gobernanza-v1_15.md`.

## §5 · Contador

**`condicionales 9 de 14` no se mueve en este acto** — declarado, mismo criterio que todo ADR ya citado en §0. **El propio contador está listado, verbatim, en el alcance (A) de ADR-72 como uno de los que hoy son `PROVISIONAL`** (`gobernanza:952`) — no solo no lo mueve este acto: el "14" y el "9" que hoy lo componen no están, ellos mismos, asentados hasta que su entrada de recálculo cierre (`forense/registro-recalculo-v1_0.md`, no cerrada). Si mesa firma la enmienda de §4 **sobre el estado actual, provisional, del contador**: `familismo_obligacion`/`norma_de_género` (uno de los 8 escalares de `D`, `modelo-decision-v4_0.md:253`) pasaría a `MEDIDO` cuando la decisión de uso en modelo (`requiere_decision_mesa`) se resuelva — eso movería el contador a 10 de 14, pero es un acto de mesa firmando, no de esta sesión, y hereda la misma reserva de provisionalidad que el 9 de 14 ya tiene hoy. `obligación_medida`, si mesa la registra como condicional nueva y no como sub-componente de la misma, sería un cambio de denominador (`D` pasaría de 14 a 15) que tampoco decide este acto — se señala como pregunta abierta para mesa, no como recomendación.

## §6 · Qué NO se hizo en este acto (declarado, no implícito)

No se editó `canon/gobernanza-v1_15.md`, ninguna celda-D, ni `especificaciones-produccion.json`. No se registró `obligación_medida` en el motor formal (ausente de este checkout, §0) ni en ningún registro de `data/curacion-registro/`. No se decidió si `familismo_obligacion` sobrevive como nombre de generador en `modelo-decision-v4_0.md`. No se resolvió la reserva de encuadre de género de `P7_12_7` (`requiere_decision_mesa: true` sigue como está). El cómputo de `P6_38` (§2.2) es real, verificado y reproducible (comando + salida cruda en esta sesión), pero es propuesta para mesa, no producción sellada.

## §7 · Verificación de cierre

`python3 tests/check.py --baseline`, corrido dos veces (antes y después de añadir la línea de `forense/hallazgos.md`), ambas idénticas:

```
18 FAIL · 105 WARN
────────────────────────────────────────────────────────────────────────
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
────────────────────────────────────────────────────────────────────────
```

Ningún archivo de `canon/`, `data/curacion-registro/`, `milpa/` tocado por este acto.

**El primer resultado que produjo este procedimiento es el reportado arriba — no se corrió el cómputo de `P6_38` una segunda vez, no se buscó un resultado distinto.**

## ADENDA (post-Commit 2, al fusionar `origin/main` para cerrar) — corrige el hallazgo de `tools/curador_registro/` de §0/§2.2, no edita el texto sellado arriba

Al refrescar contra `origin/main` para cerrar este acto, `origin/main` había avanzado de `19d885d` (base de este acto) a `fbe4e0a` (PR #204 y otros, fusionados durante la ejecución de este acto). `git ls-tree -r fbe4e0a --name-only | grep curador_registro` muestra el directorio **completo**, incluidos `produce.py`/`prepare_production.py`/`integrate_production.py` — restaurado por trabajo concurrente (rama `motor/via-capa2`, ACTO V2, ya visible en `git worktree list` al arrancar este acto, §0). **El hallazgo de §0/§2.2 ("`tools/curador_registro/` ausente de `origin/main`") era exacto contra la base real de este acto (`19d885d`, verificado con el mismo comando) y ya no lo es contra el `origin/main` post-fusión** — no se edita el texto original (append-only, mismo criterio que toda corrección de este corpus), se declara aquí. No cambia ningún resultado de este acto: el cómputo de `P6_38` (§2.2) usó `tests/svystat.py`, no el motor formal, por decisión pre-registrada en §1.5 antes de saber si el motor existía o no — la restauración del motor no lo invalida ni lo hace redundante retroactivamente, porque este acto nunca sella nada en `data/curacion-registro/` (§1.6).

`git merge origin/main --no-edit`: limpio, sin conflicto en `forense/hallazgos.md` (driver `merge=union`, ambas entradas — la de este acto y las 3 nuevas de `origin/main` — sobreviven intactas, verificado por conteo: 229+3=232 líneas). Citas de línea de este documento a `canon/gobernanza-v1_15.md` (866, 942, 952) verificadas de nuevo tras el merge: el diff de `origin/main` solo añade contenido después de la línea 973 — ninguna cita de arriba se desplazó. `python3 tests/check.py --baseline`, corrido una tercera vez tras el merge: **VERDE, 18 FAIL · 105 WARN, idéntico** a antes del merge.
