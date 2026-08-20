# Nota · ACTO APERTURA-ENFIH-ENSAFI

**Fecha:** 2026-08-20 · **Rama:** `apertura-enfih-ensafi` (worktree propio `/home/pc0/mm-apertura-enfih-ensafi`) · **Encargo:** `forense/encargos/2026-08-20-APERTURA-ENFIH-ENSAFI.md`.
**Base:** `origin/main = 9f4ea60` (merge PR #298, `LOTE-RETRIAGE`) — verificado por `git fetch origin main` al arrancar, sin cambio contra el gate que el encargo cita.
**Entorno:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=` (vacío, `sin_variable`) — coincide con lo esperado para UBUNTU. `pandas 2.3.3`, `openpyxl 3.1.5`, ninguno faltó. `data/raw`: no se hereda al crear worktree (gitignorado); se enlazó a `/home/pc0/mm-corpus/raw` y se copió `data/raices.local.yaml` en este acto, mismo mecanismo que `AI-apertura-issp` documentó. Este acto no usa red — no se sondeó ningún host.

---

## 0 · ARRANQUE — tres partes, y el defecto de premisa que la primera encontró

**Parte 1 — REPO.** Clon existente en `/home/pc0/Modelado-Mexicano`, `main` estaba en `867948c` (PR #297) al empezar y se actualizó con `git pull` a `9f4ea60` (PR #298, `LOTE-RETRIAGE`, ya fusionado — coincide con el gate declarado). Worktree propio creado: `apertura-enfih-ensafi`. `git worktree add` reportó `error: could not write config file .git/config: Device or resource busy` — es el defecto de sandbox ya documentado (`.git/config busy` es el bind-mount de sandbox, no git; corregido 19/ago, se resuelve reintentando o ignorando: el worktree quedó completo y funcional, verificado con `git log -1`/`git status`/`git branch --show-current` después).

**Parte 2 — SHA y VERIFICACIÓN A.8.** `data/coef-universo-v1_0.tsv` existe: **51 líneas, 50 filas de datos** (`wc -l` + header), coincide exacto con lo que el encargo declara. `data/apertura-enfih-ensafi-v1_0.tsv` (el archivo que este acto debe producir): **no existe** — `ls` confirma, `NO-ENCONTRADO`. Cobertura retroactiva: `data/coef-universo-v1_0.tsv` nació el 18/ago/2026 (`eb8b8e1`); `data/INFRAESTRUCTURA-v1_0.md` nació el 12/ago/2026 — es anterior, así que en principio sí podría gobernar el dominio. Verificado (`grep`): **`INFRAESTRUCTURA-v1_0.md` no menciona `abrir4-variables`, `apertura-issp-variables` ni `reapertura-52a-54-variables`** — las tres tablas precedentes de esta misma familia (variable-level opening de instrumentos) no están indexadas. No es un hueco que bloquee este acto (el archivo objetivo se verificó directamente, no por el índice), pero es un hallazgo real de tres actos de precedente sin cubrir — se declara en §6 y se abre como hallazgo, no se calla.

**Parte 3 — corpus.** Los tres payloads (`ensafi2023_bd_csv_zip`, `enfih2019_bd_csv_zip`, `enfih2019_fd_xlsx`) usan raíz `data_raw` (no `descargas_mx`, a diferencia de ISSP). `tests/manifiesto.py --verifica`, una invocación por `--id` (A.1):

```
ensafi2023_bd_csv_zip [data_raw]: COINCIDE -- sha256 y tamaño (5027338 bytes)
enfih2019_bd_csv_zip  [data_raw]: COINCIDE -- sha256 y tamaño (4404049 bytes)
enfih2019_fd_xlsx     [data_raw]: COINCIDE -- sha256 y tamaño (202396 bytes)
```

Los tres `COINCIDE`. Búsqueda física de un diccionario/codebook de ENSAFI no registrado: `find data/raw/ensafi2023` (1 archivo, el zip) · `find "/mnt/c/Users/PC0/Descargas MX" -iname "*ensafi*"` y `-iname "*enfih*"` (0 resultados) · mismo para `Downloads` (0 resultados). **Confirma, no refuta, lo que `ABRIR-4` (8/ago) ya declaró: ENSAFI no trae diccionario en este corpus.** Este acto no descarga nada — la ausencia se reporta, no se resuelve por adquisición (fuera de perímetro: "microdato solo lectura").

**El defecto de premisa, verificado antes de ejecutar (regla v2.1).** El encargo declara: *"Ley de fondo: APERTURA v1.2 §3, verbatim — ya en canon tras T-SELLO."* Verificado contra el árbol completo, por comando, no de memoria:

```
git log --all --oneline -S "APERTURA-FASE-CALCULO"   → 1 commit: 0ec4721 (T1 SELLA-ADV)
git log --all --oneline -S "APERTURA v1"              → el mismo 1 commit: 0ec4721
grep -rn "APERTURA v1\.2" canon/ forense/ *.md         → 2 líneas, ambas cabeceras de procedencia de
                                                          forense/ADV-1_demolicion_duelo_L_vs_M.md y
                                                          forense/informe_ADV2_estado_del_arte_y_rubrica.md
```

Las dos únicas apariciones de "APERTURA v1.2"/"APERTURA-FASE-CALCULO" en **toda la historia de git** vienen del mismo commit (`0ec4721`, `ACTO SELLA-ADV`, 20/ago/2026) y describen el **duelo adversarial L-vs-M del diseño del motor de cálculo** (`ADR-128`: celda-D contrato v0.5, `BASELINE_INGENUO`/`ENSAMBLE`, `D-4`/`D-5`/`D-6`) — un documento (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`) que dice de sí mismo: *"sustituye el §5 de APERTURA-FASE-CALCULO y se sella junto con ella como v1.2 (acto §T-SELLO...)"*. Es real, está en canon (`ADR-128`), y su §3 (no tocado por la sustitución) en principio "ya en canon" — **pero es un documento sobre el diseño del motor de generadores/celdas-D, no sobre protocolo de búsqueda de variables en instrumentos**. No hay ningún §3 de ese documento con contenido de "términos de búsqueda pre-registrados, codebooks primero" — verificado leyendo `ADR-128`/`ADR-129` completos en `canon/gobernanza-v1_15.md` y la nota de cierre `forense/notas/2026-08-20-sella-adv-cierre.md`: tratan de rótulos `D`, `T-ROTULOS`, `vocabulario_version`, nada de instrumentos financieros ni de reactivos.

**El protocolo que el T1-T4 de este encargo efectivamente describe SÍ existe en el árbol, pero no está canonizado con ese nombre ni con esa versión.** Es, casi palabra por palabra, el §3-§6 de `forense/encargos/2026-08-13-AI-apertura-issp.md` (`ACTO APERTURA-ISSP`, `PR #200`, el precedente directo de este mismo acto): "COMMIT 1 — pre-registro: los términos ANTES de abrir nada" · "el universo de apertura, declarado por módulo (A.4)... documentación primero, microdato después" · "co-observación limpia NO es identificación" · "el primer resultado que produzca este procedimiento es el que se reporta." Ese texto nunca se subió a un documento canónico versionado "APERTURA v1.x" — vive solo como el encargo de un acto ya `CONSUMIDO`.

**Conclusión de esta verificación, y lo que este acto hace con ella (no PARO — la instrucción operativa de T1-T4 es autocontenida y ejecutable sin el documento citado):** la cita "APERTURA v1.2 §3" es una premisa mal fundada — probablemente una confusión de nombre con `APERTURA-FASE-CALCULO v1.2` (mismo sustantivo "apertura", programa distinto, sellada el mismo día por el mismo acto `SELLA-ADV`/`T-SELLO`). Este acto **no fabrica un documento para que la cita cuadre** y **no bloquea**: seguir el T1-T4 verbatim del propio encargo, con el protocolo ya practicado por `AI-apertura-issp` como referencia metodológica declarada (no como ley de fondo inexistente), es la lectura que un colega cuidadoso haría. Se declara aquí como hallazgo para que mesa decida si vale la pena escribir/sellar el documento que el encargo asumía que ya existía.

---

## 1 · T1 — COMMIT A: los términos de búsqueda, pre-registrados antes de abrir un solo archivo

### 1.1 · La rejilla — celdas objetivo, derivadas de `data/coef-universo-v1_0.tsv` (no del censo β viejo)

`data/coef-universo-v1_0.tsv` tiene 50 filas sobre 14 `coef_id` con al menos una fila (`N6` no aparece — `SIN-DEMANDA`, `ADR-121`, fuera del perímetro derivado de este archivo) más una fila-resumen `TODOS-LOS-15`. Derivado por comando (`cut -f1,7 data/coef-universo-v1_0.tsv | tail -n +2 | sort -u` + inspección fila por fila de las 5 candidatas), un `coef_id` se cuenta **con ruta** si tiene ≥1 fila `EXISTE-SATISFACE` **o** una anotación posterior `variable_id_estado=RESUELTA`; **sin ruta** en caso contrario:

| N | Gen.coeficiente | Filas en coef-universo | ¿Con ruta? | Evidencia |
|---|---|---|---|---|
| N3 | G2.sens_estatus | 1, `NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO` | **NO — SIN-RUTA** | Búsqueda cerrada `ADR-54`; `COEF-UNIVERSO` (19/ago) no la reabre |
| N4 | G2.aversion_riesgo | 1, `NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO` | **NO — SIN-RUTA** | Búsqueda cerrada `ADR-52 A`; ídem |
| N7 | G3.familismo_apoyo | 1, `EXISTE-NO-SATISFACE`, pero con anotación `variable_id_estado=RESUELTA` (ENIF 2021, `P9_8_1..6` × `P5_1_5`, co-observados en `TModulo`) | **SÍ — excluida de la rejilla** | Censo v1.2 fila 7 ya la traía `RUTA-A` desde antes; la anotación de `COEF-UNIVERSO` la confirma. No es celda objetivo de este acto |
| N11 | G4.sens_estatus | 1, `EXISTE-NO-SATISFACE` (MMSI 2016, posición social autopercibida, no sensibilidad) | **NO — SIN-RUTA** | Misma búsqueda cerrada `ADR-54` que N3 (declarado verbatim en la fila) |
| N15 | G6.deferencia | 5, todas `EXISTE-NO-SATISFACE` (ENCUP, ISSP ZA7600, WVS ×2, ENSANUT adolescentes) | **NO — SIN-RUTA** | Ningún proxy trae desenlace de G6 en el mismo instrumento; frontera de dominio declarada en cada fila |

Contraste contra `forense/censo-estimabilidad-coeficientes-v1_2.md` (el censo β "del plan viejo, superado" que el encargo dice no usar para celdas): ese censo trae **6** `SIN-RUTA` (`N3,N4,N6,N10,N11,N15`), no 5. La diferencia es real y es la razón por la que el encargo manda derivar de `coef-universo`, no del censo: `N6` es `SIN-DEMANDA` (no aparece en `coef-universo`, `ADR-121`) y `N10` **ganó ruta** desde que se escribió el censo v1.2 — `coef-universo` trae 3 filas nuevas para `N10` con `EXISTE-SATISFACE` (Banxico Competencias Financieras 2024, Global Preferences Survey, Compartamos Banco RCT) que el censo v1.2 no tenía. Usar el censo viejo aquí habría desperdiciado dos de las ocho celdas de este acto en `N6` (sin demanda) y `N10` (ya resuelto) — exactamente lo que la instrucción de la VERIFICACIÓN A.8 anticipaba.

**Celdas objetivo de este acto: 4 necesidades × 2 instrumentos = 8 celdas** (`N3`, `N4`, `N11`, `N15` × `ENSAFI 2023`, `ENFIH 2019`).

### 1.2 · Términos de búsqueda por necesidad, derivados del censo y de `coef-universo` — no de memoria

| Necesidad | Definición (censo v1.1 fila correspondiente + `modelo-decision-v4_0.md` §2.1 `G2`/`G4`/`G6`) | Términos (idénticos a los ya usados en `ABRIR-4`/`REAPERTURA-52A-54`/`COEF-UNIVERSO` sobre estos mismos instrumentos — reutilizados por continuidad, no reinventados) |
|---|---|---|
| `N3`/`N11` · `sens_estatus` | Comparación de estatus social por consumo/apariencia/ostentación frente a otros (`G2`: "ansiedad de estatus, consumo compensatorio"); `ADR-54` cerró la búsqueda de reactivo sobre el régimen de 5 instrumentos, ampliado a 104 por `REAPERTURA-52A-54` | `estatus`, `aparent`, `apariencia`, `comparar`, `comparación`, `vecino`, `vecinos`, `marca`, `ostenta`, `ostentación`, `prestigi`, `clase social`, `nivel de vida`, `lujo`, `moda`, `impresionar` |
| `N4` · `aversion_riesgo` | Disposición actitudinal hacia el riesgo financiero (`G2`/`G3`); `ADR-52 A` cerró la búsqueda — único candidato examinado (ENIF `P5_23`/`P5_24`) mide conocimiento de protección IPAB, un moderador, no la actitud | `riesgo`, `arriesg`, `azar`, `apostar`, `pérdida`, `perder`, `certidumbre`, `cauteloso`, `conservador`, `imprevisto`, `emergencia`, `seguro` (con reserva: tenencia de producto ≠ actitud, ya penalizado en ENFIH `P9_12`) |
| `N15` · `deferencia` | `G6`: "jerarquía + indulgencia → deferencia, iniciativa suprimida, paternalismo"; se refuta si autoridad autoritaria no benévola produce buen desempeño y satisfacción. Desenlaces del modelo: `R2.1 trabajo.jerarquia.deferencia_iniciativa_suprimida` y retroalimentación privada/pública (capital social laboral) | `obedien`, `jerarqu`, `autoridad`, `deferenc`, `iniciativ`, `retroalimenta`, `jefe`, `supervisor`, `autónom`, `queja`, `castig`, `sanción`, `permiso`, `respeto` |

`N15` es la única necesidad de las 4 que **nunca** se buscó antes en ENSAFI ni en ENFIH — no forma parte de la rejilla de 7 necesidades que `ABRIR-4` cubrió el 8/ago (`sens_estatus`, `aversion_riesgo`, `horizonte_temporal`, `familismo_apoyo`, `familismo_obligacion`, `radio_confianza`-puente, theta subjetivos). Es la única celda de las 8 sin precedente de búsqueda cerrada.

### 1.3 · El universo de apertura, declarado por instrumento (A.4) — documentación primero, microdato después

**ENFIH 2019** (`enfih2019_fd_xlsx`, único diccionario disponible, 16 hojas `TVivienda`…`TConcentradora`, 838 variables — ya extraídas en su totalidad por `ABRIR-4`, 8/ago, vía `openpyxl`, columnas `Pregunta`+`Concepto`+`Nemónico`). Orden: **releer las 838 filas ya extraídas contra los términos de `N15` (búsqueda nueva)**; para `N3`/`N4`/`N11` no se repite el barrido completo — la búsqueda está formalmente cerrada por `ADR-52 A`/`ADR-54` y `COEF-UNIVERSO` (19/ago) ya declaró que no la reabre sobre este mismo universo — se **coteja** el candidato ya hallado (`P9_12_1..6`, tenencia de seguro) contra los términos de `N4` una vez más por completitud, sin volver a correr las 838 filas contra `estatus`/`riesgo` desde cero. `enfih2019_bd_csv_zip` (microdato) se abre solo si el FD arroja un candidato de `N15` que necesite verificarse contra valores reales.

**ENSAFI 2023** (`ensafi2023_bd_csv_zip`, sin diccionario en el corpus — confirmado físicamente en §0 de esta nota). Universo: los **369 encabezados** de las 4 tablas (`TSDEM`, `TVIVIENDA`, `THOGAR`, `TMODULO`) vía `zipfile`+`csv` — `ABRIR-4` ya corrió el grep automático de términos sobre los 369 y leyó a mano solo las últimas 17 columnas de `TMODULO` (donde salieron `IMPULSIVID`/`GRA_CONTROL`/`CONF_FINAN`/`ORIEN_FUT`/`OPTIMISMO`/`NIV_ESTRES`). Este acto lee a mano **las tablas que `ABRIR-4` no leyó columna por columna** (`TSDEM`, `TVIVIENDA`, `THOGAR` completas, más el resto de `TMODULO` no cubierto por las últimas 17) buscando candidatos de `N15` que un grep de cadena no encontraría (los nombres derivados de este instrumento no contienen las palabras que buscan, como ya penalizó a `IMPULSIVID`/`CONF_FINAN`).

**Techo declarado de antemano para ENSAFI, antes de ver ninguna columna nueva:** sin diccionario, ningún hallazgo en ENSAFI puede sellar `EXISTE-SATISFACE` (`A.4`: "un nombre de columna sin texto no es un reactivo", mismo criterio que ya aplicó `ABRIR-4` a `CONF_FINAN`). El techo de este instrumento en este acto es `EXISTE-NO-SATISFACE` (candidato con valores reales, sin texto verificable) o `NO-ENCONTRADO`, salvo que aparezca un diccionario no registrado — y ya se buscó físicamente y no está.

### 1.4 · Pre-registro de falsación (Bloque B-bis) — qué significa NO encontrar, y qué sería el resultado interesante

**Tasa base, medida:** `ABRIR-4` (8/ago) cerró las 14 celdas de su propia rejilla (7 necesidades × 2 instrumentos, un grid más amplio y distinto de este) en `NO-ENCONTRADO` o `EXISTE-NO-SATISFACE` — **0 de 14 en `EXISTE-SATISFACE`** sobre estos mismos dos instrumentos. Una corrida de este acto que vuelva con 0 de 8 en `EXISTE-SATISFACE` está dentro de lo esperado dado ese precedente directo y no es un fracaso — acota, no refuta.

**El resultado más interesante posible:** si `N15` (`deferencia`) encuentra co-observación limpia en `ENFIH` (exposición + desenlace de jerarquía/retroalimentación en la misma tabla) — sería la primera vez que un instrumento financiero sirve a `G6`, y `N15` lleva sin ruta desde el censo original (único proxy conocido, Latinobarómetro `P4NOIJ`, sin desenlace propio). Se declara ahora para que no se lea como ruido si aparece.

**Si `N3`/`N4`/`N11` (`ADR-52A`/`ADR-54`) arrojan un candidato con texto verificable que estos instrumentos nunca tuvieron antes** (posible solo en `ENFIH`, que sí tiene diccionario — `ENSAFI` no puede producir texto verificable por construcción, §1.3): **no se sella `EXISTE-SATISFACE` unilateralmente ni se declara la búsqueda reabierta.** Aplica `T3` del encargo verbatim — propuesta acotada con el reactivo exacto a la vista, fila abierta en `forense/firmas-pendientes.tsv` (`A.12`), la reapertura es firma de mesa.

**Co-observación limpia no es identificación** — mismo texto que `AI-apertura-issp` §3.6, reutilizado aquí porque no hay ley de fondo canonizada que lo diga por sí misma (§0): ISSP es transversal, ENFIH y ENSAFI también. Encontrar reactivo y desenlace en la misma muestra habilita una asociación, no un coeficiente identificado. La columna `llave_ADR57c` se llena `Ninguna` salvo que exista evidencia de lo contrario.

**Precedencia declarada al sellar:** si una celda de `ENSAFI` satisface por columna/valor pero el texto del reactivo no es verificable, manda la ausencia de texto — no se sella `EXISTE-SATISFACE` aunque el patrón sea sugestivo (misma regla que ya aplicó `ABRIR-4` a `CONF_FINAN`, y que reaparece aquí porque hay dos hallazgos previos de ese instrumento —`IMPULSIVID` y `CONF_FINAN`— que son exactamente el caso límite).

Cierra el commit con: **el primer resultado que produzca este procedimiento es el que se reporta.**

---

## 2 · T2 — COMMIT B: los veredictos, celda por celda

No edita `COMMIT A` (§1). Produce `data/apertura-enfih-ensafi-v1_0.tsv`, 8 filas, contrato idéntico de 14 columnas a `abrir4-variables-2026-08-08.tsv`/`apertura-issp-variables-2026-08-13.tsv`/`reapertura-52a-54-variables-2026-08-13.tsv` (verificado por comparación de encabezado, las tres son byte-idénticas entre sí). Resultado, por celda:

| Instrumento | Necesidad | `clasificacion_a4` | Resumen |
|---|---|---|---|
| ENSAFI 2023 | `N3`/G2.sens_estatus | `NO-ENCONTRADO` | 0/369 encabezados, incluidas las 15 columnas derivadas con nombre legible |
| ENSAFI 2023 | `N4`/G2.aversion_riesgo | `EXISTE-NO-SATISFACE` | `IMPULSIVID`/`GRA_CONTROL` reconfirmados, sin texto verificable (sin diccionario en el corpus) |
| ENSAFI 2023 | `N11`/G4.sens_estatus | `NO-ENCONTRADO` | Mismo universo que `N3` sobre este payload (ADR-54, un solo reactivo cerrado para ambos) |
| ENSAFI 2023 | `N15`/G6.deferencia | `NO-ENCONTRADO` | 0/369, primera vez que se busca en este instrumento |
| ENFIH 2019 | `N3`/G2.sens_estatus | `NO-ENCONTRADO` | 0/780 variables (Nemónico no vacío) de las 16 hojas |
| ENFIH 2019 | `N4`/G2.aversion_riesgo | `EXISTE-NO-SATISFACE` | `P9_12_1..6` reconfirmado, tenencia de seguro, no actitud |
| ENFIH 2019 | `N11`/G4.sens_estatus | `NO-ENCONTRADO` | Mismo universo que `N3` sobre este payload |
| ENFIH 2019 | `N15`/G6.deferencia | `NO-ENCONTRADO` | 2 candidatos de superficie (`PAREN`, `SX_JEFE`), ambos jefatura de hogar por parentesco, descartados por dominio; primera vez que se busca en este instrumento |

**Discrepancia de conteo declarada, no reconciliada.** Este acto extrajo **780** variables de `enfih2019_fd_xlsx` (filas con `Nemónico` no vacío, vía `openpyxl`); `ABRIR-4` (8/ago) declaró **838** sobre el mismo archivo. Metodologías de conteo distintas — no se reprodujo la receta de `ABRIR-4` para reconciliar la diferencia, y no cambia el resultado sustantivo: ampliar la ventana de lectura (todas las 16 hojas, no solo las que `ABRIR-4` había citado) no encontró ninguna variable adicional relevante a los términos de `N3`/`N4`/`N11`/`N15`. Se declara por la misma regla que obliga a probar una receta de conteo antes de usarla (`instrucciones-proyecto-v2_10.md`, "y la receta de derivación también se verifica") — no se fuerza la coincidencia con una cifra heredada.

`ENSAFI`: **369** encabezados coincide exacto con lo que `ABRIR-4` ya reportó — misma cifra, dos sesiones, mismo comando (`zipfile`+`csv` sobre las 4 tablas).

`data/coef-universo-v1_0.tsv`: 8 filas anexadas (51→59 líneas, solo la columna de ruta, esquema de 13 columnas sin tocar), una por cada celda de la tabla de arriba, con `variable_id_estado=SIN-RUTA (sin cambio)` en las 8 — ninguna celda cambió de estado. Verificado `git diff --numstat` antes de commitear: `8 0`, cero líneas preexistentes tocadas (el riesgo conocido del módulo `csv` de este proyecto — corrompe comillas de filas ajenas — no aplica porque ambos archivos se escribieron con `'\t'.join(...)` línea por línea, nunca con `csv.writer`).

## 3 · T3 — la contingencia de `ADR-52A`/`ADR-54`: no se dispara

Los dos únicos candidatos con valores reales de las 8 celdas (`IMPULSIVID`/`GRA_CONTROL` en `ENSAFI`, `P9_12_1..6` en `ENFIH`, ambos bajo `N4`/`aversion_riesgo`) **no son reactivos nuevos**: son exactamente los mismos que `ABRIR-4` ya declaró el 8/ago/2026 y que `censo-estimabilidad-coeficientes-v1_1.md` fila 4 ya incorporó a la evidencia de "búsqueda cerrada" de `ADR-52 A`. Este acto los reconfirma con una extracción independiente (780 variables de ENFIH, no heredadas; 369 encabezados de ENSAFI, con lectura manual ampliada) y no encuentra nada que no estuviera ya sobre la mesa. `N3`/`N11` no producen ningún candidato, nuevo o viejo, en ninguno de los dos instrumentos.

**Conclusión: `T3` no aplica.** No se escribe propuesta acotada, no se abre fila de reapertura en `forense/firmas-pendientes.tsv` para `ADR-52A`/`ADR-54` — no hay reactivo que reabrirlos. La única fila nueva del tablero de este acto (`FP-87`) es sobre la premisa "APERTURA v1.2 §3" (§0), no sobre `ADR-52A`/`ADR-54`.

## 4 · T4 — cierre

**Contador del encargo, los dos números derivados: `SIN-RUTA` con ruta, antes → después = `0 de 4` → `0 de 4`.** Ninguna de las cuatro celdas objetivo (`N3`, `N4`, `N11`, `N15`) ganó ruta. Dentro de lo pre-registrado en `COMMIT A` (§1.4): la tasa base medida por `ABRIR-4` sobre estos mismos dos instrumentos era `0` de `14` en `EXISTE-SATISFACE`; este acto suma `0` de `8` más, sin romper el patrón. Acota, no refuta, y no es fracaso — es la ejecución honesta del procedimiento pre-registrado.

**Fichas B-bis nuevas: cero.** Ninguna de las 8 celdas alcanzó `EXISTE-SATISFACE`; no hay nada "medible ya" que congelar en una ficha B-bis. Declarado explícitamente porque el encargo pide fichas "para lo medible ya" — la respuesta honesta a esa instrucción es que el conjunto está vacío, no que se omitió.

**Lo que este acto deliberadamente no hace.** No calcula ningún β ni ninguna θ. No reabre `ADR-52A`/`ADR-54` (§3). No toca `data/manifiesto.yaml`, `data/curacion-registro/**`, `canon/modelo-decision-v4_0.md`, `milpa/`, ni `data/diseno-muestral.yaml`. No escribe en `data/raw/` — microdato solo lectura, verificado (`--verifica` recomputa `sha256`, no escribe).

**La "palanca más grande dormida del corpus" — lo que este acto encuentra sobre esa frase.** El único candidato con valores reales y sin texto verificable que sigue "dormido" en sentido literal es el par `IMPULSIVID`/`GRA_CONTROL`/`CONF_FINAN`/`ORIEN_FUT`/`OPTIMISMO` de `ENSAFI` — y su despertar no depende de un acto de apertura más cuidadoso: depende de que exista un diccionario que este corpus no tiene y que este acto verificó, por segunda vez, que no está (§0). Si la "palanca" que el plan maestro describe es esa, el acto que la acciona es una adquisición (bajar el cuestionario/codebook real de ENSAFI 2023 de INEGI, si existe), no una apertura — declarado para que el sucesor no repita esta misma búsqueda sobre el mismo corpus sin ese archivo.

## 5 · Suite y cierre de commit — cifras previas a la fusión con `origin/main`

Antes de descubrir la fusión concurrente de `§6` (abajo), este acto llegó a punto fijo sobre `origin/main = 9f4ea60`:

```
$ python3 tests/check.py --baseline   (con corpus enlazado)
21 FAIL · 129 WARN
LÍNEA BASE: VERDE

$ python3 tests/check.py --baseline   (con data/raw desenlazada)
LÍNEA BASE: VERDE — sin cambio

$ python3 tests/check.py --baseline   (con data/raices.local.yaml y data/secretos.local.yaml retirados)
21 FAIL · 129 WARN
LÍNEA BASE: VERDE — sin cambio
```

`T02`/`T03`/`T25` no disparaban sobre ningún archivo de este acto. La cascada de la cabecera de ADR (`gobernanza` 131→132, `estado` en sus **tres** sitios que la citan — más el WARN 128→129 por `FP-87`) se propagó hasta punto fijo: la primera corrida tras escribir `ADR-132` sin propagar el resto dio `24 FAIL · 129 WARN` con `T15`/dos `T16` disparando; declarado en vez de ocultar el paso intermedio. **Estas cifras quedaron superadas por la fusión de `§6` — ver ahí las vigentes.**

Sin `--freeze` (prohibido por el encargo).

---

## 6 · Corrección post-fusión — §0 quedó correcto contra su terreno y superado por uno nuevo, en el mismo acto

**No se edita §0 hacia atrás** (`A.10`, corolario 1): el texto de arriba es exactamente lo que este acto verificó, con el comando a la vista, contra `origin/main = 9f4ea60`. Lo que sigue es lo que cambió entre ese commit y el cierre de este acto, declarado en el mismo acto y no en uno posterior.

Al fusionar `origin/main` antes del push final, `git log` mostró un commit nuevo: `a72ead3`, merge de `PR #299` (`ACTO T-SELLO`, rama distinta, corriendo en paralelo a este acto sin que ninguna de las dos sesiones lo supiera). Ese PR aterriza `canon/APERTURA-FASE-CALCULO-v1_2.md` — el documento exacto cuya existencia §0 había buscado y no encontrado. Leído completo tras la fusión: su **§3** es, casi verbatim, el `T1`-`T4` que este acto ejecutó —

> *"Ley de fondo: PLAN-CALCULO-TOTAL §3-OLA2 + celdas objetivo del censo de β (re-derivado de `data/coef-universo-v1_0.tsv`, filas ENFIH/ENSAFI)... T1 · Abre ENFIH 2019 y ENSAFI 2023 a nivel variable contra las celdas objetivo, con términos pre-registrados en tu COMMIT A antes de abrir un solo archivo... T2 · Por celda objetivo: veredicto A.4... T3 · Si aparece reactivo que reabre ADR-52A/54: NO reabres... T4 · Cierra: cuántos de los SIN-RUTA ganaron ruta..."*

— casi palabra por palabra el encargo que esta sesión recibió y ejecutó. **La premisa "APERTURA v1.2 §3, ya en canon tras T-SELLO" no se sostenía cuando este acto la verificó, y se sostiene ahora.** No fue un error de verificación: `canon/APERTURA-FASE-CALCULO-v1_2.md` genuinamente no existía en el árbol contra el que se corrió `git log --all -S` en `§0` — el commit que lo trae (`0ec4721` era el único con "APERTURA v1.2" en toda la historia hasta ese punto) es, precisamente, el mismo `T-SELLO` que después lo completó con `v1.2`, en una rama que este acto no podía ver hasta que se fusionó.

**Lo que esto cambia y lo que no cambia.** No cambia ningún resultado de `§2`-`§4`: los 8 veredictos A.4, el contador `0 de 4`, la no-activación de `T3`, son independientes de si el documento canónico existía. Cambia el estatus de la propia observación de `§0`: de "hallazgo de premisa mal fundada" a "condición de carrera entre dos sesiones concurrentes, resuelta al fusionar". La fila de tablero que este acto había preparado (`FP-87`, "mesa decide si vale la pena sellar un documento real") se retira antes de commitear — no hay pregunta pendiente, el documento ya existe y ya está en canon vía `ADR-132` de `T-SELLO`.

**Mecánica de la fusión.** `git merge origin/main` produjo conflicto real en tres archivos — los mismos que `ACTO T-SELLO` ya había identificado como su propio punto de colisión con `LOTE-RETRIAGE`: `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, `forense/firmas-pendientes.tsv`. Resuelto a mano, conservando la contribución de `T-SELLO` íntegra (su `ADR-132`, sus `FP-87`…`FP-91`) y renumerando la propia: el `ADR-132` de este acto candidateado contra `9f4ea60` pasa a **`ADR-133`** (T-SELLO fusionó primero con el mismo número), con el párrafo `(e)` reescrito para reflejar lo de arriba en vez de mantener una afirmación que el propio acto ya sabía superada. `FP-87` de este acto se retira sin dejar hueco (el tablero no re-usa números: el máximo queda en `91`, de `T-SELLO`). `hallazgos.md` recibe una entrada nueva junto a la original, marcada `{cita-historica}`, en vez de editar la primera — mismo mecanismo que el resto del archivo ya usa para toda corrección.

```
$ python3 tests/check.py --baseline   (tras la fusión y la resolución de conflictos, con corpus enlazado)
21 FAIL · 138 WARN
LÍNEA BASE: VERDE

$ python3 tests/check.py --baseline   (con data/raw desenlazada)
LÍNEA BASE: VERDE — sin cambio

$ python3 tests/check.py --baseline   (con data/raices.local.yaml y data/secretos.local.yaml retirados)
LÍNEA BASE: VERDE — sin cambio
```

El FAIL núcleo (21) coincide exacto con el que este acto ya tenía antes de descubrir la fusión — la subida transitoria a 22-26 durante la resolución fue enteramente mecánica (conteo de ADR desincronizado en tres sitios, más dos citas históricas de `canon/PLAN-CALCULO-TOTAL-v1_1.md:8`, heredadas de `T-SELLO`, que quedaron colgantes contra `T15` en cuanto el conteo de ADR subió con `ADR-133`; marcadas `{cita-historica}` dentro de sus negritas, no reescritas — mismo mecanismo que `T15` ya usa en todo el archivo). El WARN (138) es enteramente de `T-SELLO`: este acto no abre ninguna fila de tablero.

---

## 7 · Tercera fusión — `PR #300`/`ACTO DUELO-PREREG-V2`, limpia

Tras empujar el commit de `§6`, `origin/main` avanzó una tercera vez: `PR #300` (`ACTO DUELO-PREREG-V2`, sucesor de `T-SELLO` bajo el mismo plan `APERTURA-FASE-CALCULO`, corriendo en NUBE mientras este acto seguía abierto). Reportado en el cierre de esa misma sesión que dejó el PR de este acto en `mergeable: CONFLICTING` — declarado y no perseguido en ese momento.

**Diferencia con la segunda fusión (`§6`): esta no colisiona.** `git diff a72ead3 origin/main` muestra que `PR #300` solo tocó `forense/firmas-pendientes.tsv` (una línea, la columna `dónde` de `FP-90`, sin tocar su `estado`) y `forense/hallazgos.md` (una línea nueva, append-only) — ningún ADR nuevo, `canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` sin tocar. `git merge origin/main` resolvió **sin un solo conflicto** (`git status` limpio tras el merge, ningún marcador `<<<<<<<`). Re-verificado con `python3 tests/check.py --baseline`, las tres pasadas (corpus enlazado, `data/raw` desenlazada, gitignorados retirados): **LÍNEA BASE: VERDE, 21 FAIL núcleo · 138 WARN, sin cambio en ninguna de las tres cifras** frente a `§6`. `mergeable` vuelve a `MERGEABLE` en `PR #302` tras empujar este commit — no queda declarado ningún hallazgo nuevo, la fusión fue mecánica.
