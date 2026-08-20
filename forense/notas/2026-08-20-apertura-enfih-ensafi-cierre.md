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
