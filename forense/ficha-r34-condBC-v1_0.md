# Ficha `R3.4` · condiciones **B** (prueba de mecanismo) y **C** (anti-confusión) — censo de fuentes y propuesta

> | | |
> |---|---|
> | **QUÉ ES** | El censo de fuentes mexicanas para las dos condiciones del gate de `ADR-37` que hoy tienen base medida **0 de 2** y umbral `ASIGNADO`. Deriva candidatas del canon, las abre a nivel de **descriptor y cuestionario** (no de microdato), y emite veredicto `A.4` por candidata. |
> | **QUÉ NO ES** | **CONTADOR: cero, declarado.** No adjudica `R3.4`. No toca `tests/aceptacion_r3_4.py`. No re-abre la condición `A` (`SELLADA`, fila `A1`, `ADR-177`). No cablea disparadores a `milpa/tramite.yaml`. No descarga fuente nueva. No corre ninguna estimación: el censo cerró en cero `EXISTE-SATISFACE` y el encargo prohíbe forzar un proxy. |
> | **ACTO** | `R34-BC-MECANISMO`, 25/ago/2026, entorno **UBUNTU**, contra `2b7d787`. |

---

## 0 · Arranque y firma de entorno (`A.2`, tres partes)

| parte | salida cruda |
|---|---|
| variable | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = **`sin_variable`** (UBUNTU) |
| sonda de red | `curl -s -r 0-11 https://www.inegi.org.mx/` → `http=206 bytes=12 tiempo=0.575848` (GET crudo con rango, no `curl -I`) |
| corpus | `data/raw` → symlink a `/home/pc0/mm-corpus/raw`; `ls data/raw \| head -1` = `2005trim1_csv.zip`; **321 entradas**, 9.6 GB |

`SHA` de redacción `2b7d787` verificado contra el árbol: es `origin/main` exacto (`git rev-list --count 2b7d787..origin/main` = **0**), `PR #356`. La caja del acto se creó sobre él.

---

## 1 · `F0` · Verificación de existencia (`A.8`) — y corrección de una premisa propia

**Ningún abridor de `B`/`C` existe.** `find forense -type f \( -iname "*r34*" -o -iname "*r3_4*" -o -iname "*r3-4*" -o -iname "*codi*" -o -iname "*spei*" \)` sobre `forense/` completo (**1,524 archivos examinados**, 25/ago/2026) devuelve 8 archivos, y los 8 son de la **condición A** o de su cadena: `benchmark-unidad-homogenea-codi-spei-v1_0.md` · `encargos/2026-08-24-R34-CONDA-V2.md` · `encargos/2026-08-25-SELLA-A1-CODI.md` · `encargos/2026-08-25-SERIE-HOMOGENEA-CODI-r34.md` · `ficha-r34-conda-v2-spec.md` · `notas/2026-08-04-fichas-r3-1-r3-4.md` · `notas/2026-08-24-r34-conda-v2-cierre.md` · `notas/2026-08-25-sella-a1-codi-cierre.md`. **No hay `PARO`.**

**Las cuatro premisas del encargo, verificadas contra el árbol y las cuatro ciertas.** Se declaran porque la verificación se corrió y `A.5`/`A.13` exigen que el resultado se escriba, no que se asuma:

| premisa del encargo | comando | resultado |
|---|---|---|
| `ADR-177` sella la fila `A1` | `grep -n "ADR-177" canon/gobernanza-v1_15.md` | **cierta** — `gobernanza:3585`, `ACTO SELLA-A1-CODI` |
| `FP-104` trae verbatim «base medida 0 de 2, ambos `ASIGNADO`» | lectura de `forense/firmas-pendientes.tsv:105` | **cierta** — «*B y C no son hallazgos empiricos (estampa del emisor: base medida 0 de 2, ambos ASIGNADO)*», y de nuevo al cierre de la fila: «*B/C siguen con base medida 0 de 2*» |
| `ficha-r34-conda-v2-spec.md:148` aisló `friccion_uso` | lectura del archivo (400 líneas) | **cierta** — §4, par de control `DiMo ↔ CoDi`, «*el componente que la Nota 3 declara sin disparador*»; y **no corre** ahí por ausencia de serie primaria de DiMo |
| umbrales de `B`/`C` `ASIGNADO` | `grep -n "R3\.4" canon/estado-programa-v1_10.md` | **cierta** — `estado:190`: «*Los umbrales de B y C son **ASIGNADOS**; calibrar contra series de SPEI antes de Fase 1*» |

*(Corrección de un negativo propio, declarada porque la regla de la casa la exige y no porque cambie nada: la primera corrida de `F0` de este acto se hizo por error sobre el worktree principal, parado en `ea22bdd` / rama `acto/cal-g3-puntual`, un árbol **anterior** a `PR #356`. Ahí `ficha-r34-conda-v2-spec.md` y `ADR-177` no existían y las premisas parecían falsas. Re-corrido `F0` sobre la caja del acto —`2b7d787`, el SHA que el encargo fija— las cuatro son ciertas. Es exactamente el modo de falla que `forense/hallazgos.md:349` ya registró: **re-correr el comando contra el árbol del momento, no heredar su salida**.)*

---

## 2 · Qué tiene que medir cada condición — leído de `ADR-37`, no de memoria

`gobernanza:267` (`ADR-37`), verbatim:

- **(B) Prueba de mecanismo** — «*al apagar **`riesgo_fiscal_percibido`** con **el canal constante**, la brecha debe **colapsar ≥70%***. Si no colapsa, el modelo llegó al desenlace por otro camino.»
- **(C) Anti-confusión** — «*al apagar **el canal de confianza personal** con `riesgo_fiscal_percibido` **encendido**, la brecha debe **PERSISTIR** (se reduce <30%)*.»

Y `gobernanza:213` (`ADR-25`, corrección del `S2` más antiguo): «*La explicación canónica del fracaso de CoDi es **riesgo fiscal percibido + fricción**, no desconfianza.*»

**Consecuencia operativa, y es la que gobierna todo este censo.** Las dos condiciones se apoyan sobre **la misma variable de exposición**: `riesgo_fiscal_percibido`. `B` la apaga; `C` la deja encendida mientras apaga otra cosa. Un instrumento que no mida esa percepción **no puede servir a ninguna de las dos**, por buena que sea en todo lo demás. El censo de abajo se organiza alrededor de esa pregunta.

Traducido al dato de encuesta, y declarado **antes** del censo, cada condición exige tres piezas sobre los mismos individuos:

| pieza | `B` | `C` |
|---|---|---|
| **desenlace** | no-uso de CoDi entre usuarios digitales | ídem |
| **exposición** | percepción de riesgo fiscal/vigilancia al usar el medio | canal de confianza **personal** (`§3.1`/`G1a`) |
| **el que se sostiene constante** | canal (de confianza) | `riesgo_fiscal_percibido`, **encendido** |
| **co-exposición obligada** | fricción declarada, medible **junto** a la fiscal | — |

---

## 3 · `F1` · Censo — universo, mecanismo y fecha (`A.4`)

**Universo declarado.** (i) `data/manifiesto.yaml` (15,426 líneas); (ii) los tres inventarios que el encargo nombra —`inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md`, `inventario-fuentes-tecnologia-digital-mexico.md`, `inventario_fuentes_tramites_estado_mexico.md`— más los 9 restantes de `data/inventarios/`; (iii) `data/diseno-muestral.yaml` (56 filas); (iv) **barrido mecánico de `data/raw/` completo** (321 entradas de primer nivel, 9.6 GB), abriendo cada PDF con **los dos extractores** (`pypdf` + `pdftotext -layout`, unión — la lección de `FP-111`), cada `.xlsx` hoja por hoja con `openpyxl`, y la **cabecera** de cada `.csv` suelto o dentro de `.zip`. Fecha: 25/ago/2026. Script: `tools/censo_r34_bc.py` (commiteado por este acto).

**Conteo del barrido, que es lo que `A.13` exige junto a cualquier negativo — `20,838 archivos examinados`**, desglosados por clase: `19,061` cabeceras de CSV dentro de ZIP · `1,080` XLSX dentro de ZIP · `395` PDF dentro de ZIP · `170` PDF sueltos · `67` XLSX sueltos · `47` HTML/XML/JSON · `18` CSV sueltos. **Control positivo del propio comando: `20,280` de los `20,838` devolvieron texto de longitud > 0** (los `558` restantes son formatos que el barrido declara no leer, ver límite abajo). Y control positivo del patrón, no sólo del comando: el constructo `FISCAL` acierta en **232** archivos y el `PERSONAL` en **97** — el barrido **sí** encuentra estos términos donde están; lo que no encuentra es la conjunción que `B` necesita.

**Límites del barrido mecánico, declarados y no escondidos.** (a) Un `.csv` sólo aporta **nombres de variable**, no el texto del reactivo; el barrido por tanto **no puede** encontrar un ítem cuya redacción viva únicamente en un descriptor que el corpus no tiene — que es exactamente el caso de `ENSAFI 2023` (fila 10). (b) **No abre `.dbf`**: el microdato de `ENDUTIH` se distribuye en ese formato y sólo su `FD` en `.xlsx` fue leído — no es pérdida, porque el texto del reactivo vive en el `FD` y no en el `.dbf`, pero se declara. (c) Un acierto de patrón **no es un acierto de constructo**: los `22` archivos que co-ocurren `DIGITAL` y `FISCAL` se abrieron uno por uno y **ninguno resultó ser el constructo buscado** (§3.2). Por eso el censo **no se cierra con el barrido**: cada candidata con señal se abrió y se leyó **a nivel de reactivo**, y es esa lectura la que emite el veredicto.

### 3.1 · Veredicto por candidata

Vocabulario de `A.4`. Cada fila declara **qué se abrió** y **qué se leyó**, no sólo qué se concluyó.

| # | candidata (ola) | qué se abrió | desenlace CoDi | exposición **fiscal** | fricción | canal **personal** | veredicto `B` | veredicto `C` |
|---|---|---|---|---|---|---|---|---|
| 1 | **ENIF 2024** | cuestionario PDF + `enif_2024_fd.xlsx` + cabecera de `TMODULO.csv` (398 col.) | **sí** (`P7_2_1`/`P7_3_1`) | **sí, pero en otro objeto** (`P5_20`=09, `P5_21`=8, `P6_14`=8, `P6_15`=7) | sí (`P5_20`=04/08) | **sí** (`P5_15_2`) | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 2 | **ENIF 2021** | cuestionario PDF + `enif_2021_estructura_del_archivo.xlsx` | **sí** (7.2/7.3, sólo CoDi) | ídem (`5.21`=09, `5.22`=09, `6.15`, `6.16`) | sí | sí | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 3 | **ENIF 2018 / 2015 / 2012** | cuestionario PDF (2018) + `fd` (2015, 2012) | **no** (pre-CoDi en el instrumento) | **no** — el único «impuestos» de 2018 es *«pagos de impuestos o multas»*, un **tipo de pago**, no una razón | sí | sí | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 4 | **ENDUTIH 2023 · 2024 · 2025** | `fd_endutih*.xlsx` (8 hojas, 1,413 filas la de 2024) | **sí, y sobre el universo correcto** (`P7_32_6`, condicionado a `P7_28`=1) | **NO — cero ítems** | sí (`P7_29`=5, `P7_22_7`) | no (`P7_29`=1 es *«prefiere realizarlo en persona»*, presencialidad, no confianza en red personal) | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 5 | **IFT · Servicios Financieros Digitales 2024** | `basededatossfd.zip::…SFD.xlsx`, 2 bases (107 y 76 columnas) | **sí, y sobre el universo correcto** (*«Utilizó CoDi para realizar un pago o cobro»*) | **NO — cero ítems** | sí (*«No sabría cómo utilizarlo»*) | no (la escala de confianza es *hacia el SFD*, no hacia la red personal) | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 6 | **ENCIG 2011…2025** (8 olas) | `encig21_cuestionario.pdf` + `encig23`/`encig25_estructura_base_datos.pdf` | **no** (CoDi no aparece; sí adopción de **gobierno digital**: `P10_1_2`, `P10_1_3`, `P10_1_5`) | **NO** — *«trámites fiscales ante el SAT»* es un **tipo de trámite** (batería 9.x, código 06), no una percepción de riesgo | no | **sí, y separado del institucional en la misma batería** (`P11_1_09` parientes · `P11_1_11` vecinos · `P11_1_07` compañeros **frente a** `P11_1_04` Presidencia/Secretarías · `P11_1_23` servidores públicos), escala de 4 puntos + refinamiento `P11_1A_*` 0–10 | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 7 | **Banxico · Encuesta de Competencias Financieras 2019 · 2021 · 2024** | los 3 `.xlsx` (145 col. la de 2024) + los 2 manuales PDF | **no** | **NO** — 0 aciertos de `CoDi\|cobro digital\|impuest\|fiscal\|SAT` sobre los 2 manuales (**179,645 caracteres**, unión de extractores); control positivo `ahorro` = **34 y 38** aciertos | sí | sí (préstamo de familiares/amigos) | `EXISTE-NO-SATISFACE` | `EXISTE-NO-SATISFACE` |
| 8 | **Banxico · payloads de `R3.4`** (`R3.4_Banxico_CoDi_SPEI/`) | 6 Informes Anuales IdMF (2019-2024) + 9 cuadros SIE + landings | serie **agregada**, sin individuo | **NO** — sobre `informe_anual_IdMF_2024.pdf` (**879,375 caracteres**, unión) no hay encuesta de motivos; control positivo `CoDi` = **90** aciertos | no | no | `EXISTE-NO-SATISFACE` (es la fuente de **A**, no de B/C) | ídem |
| 9 | **«Encuestas CoDi de Banxico»** (la candidata que el encargo pide verificar) | `ls data/raw \| grep -i banxico` + `grep -n banxico data/manifiesto.yaml` | — | — | — | — | **`NO-ENCONTRADO`** — el corpus tiene de Banxico **series transaccionales e informes**, ninguna encuesta con motivo declarado. Universo: las 26 entradas `banxico*`/`codi*` de `data/raw` y sus filas de manifiesto, 25/ago/2026 | ídem |
| 10 | **ENSAFI 2023** | `ensafi_2023_bd_csv.zip` (4 tablas, `TMODULO` 253 columnas) | no determinable | no determinable | no determinable | no determinable | **`NO-ACCESIBLE`** — el microdato está, **el descriptor no**: sin `FD` no se puede citar el texto de ningún reactivo, sólo códigos `P5_*`. Ya registrado como hueco en `FP-115`(c) | ídem |

| 11 | **ENAFIN 2024 / 2019-2021** (financiamiento de empresas) | `MEX-INEGI.EEC3.05-ENAFIN-2024.xml` (metadatos RNM, 2,259,786 caracteres) | **no** | **no** — sus aciertos fiscales son *«Tipo de régimen fiscal de la empresa»* (`P3`), la cláusula de confidencialidad del INEGI y el glosario; ninguno es percepción de riesgo | — | sí, pero como **fuente de fondos** (`P30_1` *«¿Quién le otorgó los recursos en 2023? Familiares o amistades»*), no como canal de confianza | `EXISTE-NO-SATISFACE` — y además **la unidad de observación es la empresa**, no la persona usuaria | ídem |

**Cierre del censo: cero `EXISTE-SATISFACE` para `B` y cero para `C`.** Es el desenlace que el encargo previó y ordenó reportar tal cual, «*sin forzar un proxy*».

### 3.2 · Los 22 casi-aciertos del barrido, abiertos uno por uno

El barrido marcó **22** archivos donde co-ocurren el constructo `DIGITAL` y el `FISCAL`. Se abrieron los 22 y se leyó **qué** disparó el acierto. Ninguno es el constructo buscado, y el desglose importa porque es lo que impide que este negativo se apoye en una ausencia de aciertos en vez de en una lectura:

| qué disparó `FISCAL` | archivos | qué resultó ser |
|---|---|---|
| `impuest` | 8 de `ENIF` (2018, 2021, 2024 — cuestionario y `FD`; 2015 `FD` con `Hacienda`) | la opción *«No quiere que le cobren impuestos»* de las baterías de **no tenencia de cuenta/crédito** — el casi-acierto real, tratado en §3.4 |
| `vigilanc` | 3 de `ENDUTIH` (`FD` 2023, 2024, 2025) | *«sistemas de **video vigilancia** (cámara de seguridad…)»*, un **dispositivo del hogar** (`P5_13`). **Falso positivo de patrón** |
| `rastreo` · `Hacienda` | 3 de `IFT SFD` (base + los 2 PDF del reporte) | *«robo… de datos»*/`rastreo` en el bloque de fraude, y una mención institucional a la **SHCP** en el reporte. **No hay reactivo fiscal** |
| `impuest` · `vigilanc` | 5 Informes Anuales `IdMF` de Banxico (2019-2022, 2024) | prosa de regulación y supervisión (**vigilancia** de infraestructuras de pago, en su sentido regulatorio). **No hay encuesta** |
| `impuest` | `encig2011/fd_encig2011.pdf` | *«pagos por internet»* como canal de trámite y *«impuesto»* como **tipo de trámite** — mismo patrón que las olas 2021/2025 |
| `impuest` · `fiscal` | `ENAFIN 2024` (XML de RNM) | régimen fiscal **de la empresa** y glosario; fila 11 |
| `HACIENDA` | instructivo de codificación geográfica de `ENOE` | un **topónimo**. Falso positivo puro |

**Hallazgo colateral, declarado porque un sucesor lo necesita.** El reporte especial del `IFT` publica, en su Gráfico 1.2.2.1 (*«¿A través de qué medios se enteró de los SFD?»*), la categoría **«Familiares y amistades» con 3.3 %** — un canal personal. Esa categoría **no existe como columna propia en la base liberada**: las columnas publicadas son sucursal · aplicación de celular · página de Internet · redes sociales · `Otro` · `Ns/Nc`. El canal personal está **medido y publicado en agregado, pero no expuesto en el microdato**. Además es *fuente de información*, no confianza — construto más débil que la batería de `ENCIG`. Se registra como reserva, no como candidata.


### 3.3 · La razón única, y es una sola variable

El censo no falla por falta de fuentes: falla por **falta de un constructo**, y siempre el mismo.

> **Ningún instrumento del corpus mide la percepción de riesgo fiscal o de vigilancia asociada a usar un medio de pago o un servicio de gobierno digital.**
> Universo del negativo: los 11 bloques de la tabla de §3.1, abiertos a nivel de reactivo, **más** el barrido mecánico de `data/raw/` completo. Mecanismo: `pypdf` + `pdftotext -layout` en unión para PDF, `openpyxl` hoja por hoja para XLSX, cabecera para CSV. Fecha: 25/ago/2026. Conteo de archivos examinados y control positivo: §3 y §3.2.

Lo demás que `B` y `C` necesitan **sí está**, y está bien:

- el **desenlace exacto** —no-uso de CoDi entre usuarios digitales— existe **dos veces**, en dos emisores distintos: `ENDUTIH` `P7_32_6` (INEGI, tres olas, con `FAC_PER`/`UPM_DIS`/`EST_DIS`) e `IFT SFD 2024` (*«Utilizó CoDi para realizar un pago o cobro»*, dos bases);
- la **fricción declarada** existe en tres instrumentos;
- el **canal personal frente al institucional**, que es la pieza cara de `C`, existe en `ENCIG` **separado ítem por ítem dentro de la misma batería y sobre los mismos individuos** — parientes y vecinos junto a Presidencia y servidores públicos, misma escala, misma ola.

Falta **una** variable, y de ella cuelgan las dos condiciones: `B` la apaga, `C` la sostiene encendida.

### 3.4 · Dos defectos de forma que bloquean incluso al mejor casi-acierto

Se declaran porque un sucesor que sólo leyera la tabla podría creer que `ENIF` «casi sirve»:

1. **La batería fiscal de `ENIF` es de respuesta única.** `5.20`/`P5_20` dice, verbatim, **`CIRCULE UN SOLO CÓDIGO`**, y sus diez opciones ponen a competir *«No quiere que le cobren impuestos»* (09) contra *«Piden requisitos que no tiene»* (04) y *«No sabe qué es o cómo usarla»* (08). `B` exige que riesgo fiscal **y** fricción estén asociados **a la vez**; un instrumento que obliga a elegir una sola razón **no puede** medir esa conjunción, ni siquiera sobre su propio objeto. Lo mismo en `6.14`/`P6_14`. *(Contraste medido, no supuesto: `ENDUTIH` `P7_22` **sí** es de opción múltiple —`P7_22_1`…`P7_22_10`, cada una `[1-2]`— y `IFT SFD` también; pero ninguna de las dos trae opción fiscal, y `ENDUTIH` `P7_29`, la de pagos, vuelve a ser única `[1-8]`.)*
2. **El objeto de la batería fiscal de `ENIF` no es CoDi.** `P5_20` pregunta por la **no tenencia de cuenta o tarjeta**; `P6_14`, por la de **crédito**. El bloque de CoDi de la misma encuesta —`7.2`/`7.3`, `P7_2_1`/`P7_3_1`— es **conocimiento y uso, y nada más**: no tiene batería de razones. Verificado en las dos olas post-lanzamiento (2021 y 2024) y confirmado en el microdato: entre las 398 columnas de `TMODULO` de 2024 no hay ninguna variable de motivo colgada de `P7_3_*`.

**Y un tercer defecto, de universo, que afecta a las dos fuentes que sí traen el desenlace correcto:** en `ENDUTIH` y en `IFT SFD` la batería de razones se le pregunta a quien **no usa** el servicio digital en absoluto (`P7_29` sólo si `P7_28`=2; la batería del `SFD` sólo a quien marcó *«Ninguno»*), mientras que el desenlace que `B` necesita —no usar **CoDi** **siendo** usuario digital— vive en el universo **complementario**. Las dos piezas están en la misma encuesta y **no se tocan**: por diseño del salto, ningún individuo tiene las dos.

---

## 4 · `F2` · Lo que se congela — y por qué no es una spec de corrida

El encargo ordena congelar spec **«solo sobre `EXISTE-SATISFACE`»**. Con cero, **no hay spec de corrida que congelar**, y este acto no la inventa. Lo que sí se congela, y se congela **antes** de cualquier sucesor, es el **criterio de aceptación**: qué tendría que traer una fuente para que este veredicto cambie. Se escribe aquí para que un sucesor no pueda relajarlo después de ver su dato.

**Criterio congelado — `B` queda satisfecha si y sólo si** una única fuente, sobre **los mismos individuos**, trae las tres: (i) uso/no-uso de CoDi (u otro medio de pago digital coercitivo nombrado) **entre quienes ya usan medios digitales**; (ii) un reactivo de **percepción de riesgo fiscal o de vigilancia** referido a **usar ese medio** —no a tener un producto financiero—, con escala declarada; (iii) un reactivo de **fricción** que pueda coexistir con (ii) en la misma respuesta, es decir **opción múltiple o escalas independientes, nunca respuesta única**. Y el patrón que cuenta como `B`-satisfecha es: (ii) y (iii) **ambos** asociados al no-uso, con el canal de confianza sostenido constante.

**Criterio congelado — `C` queda satisfecha si y sólo si** una única fuente, sobre los mismos individuos, trae (i) el mismo desenlace; (ii) la **misma** variable de riesgo fiscal de `B`, **encendida**; (iii) confianza en el **canal personal** (`§3.1`/`G1a`) separable de la confianza institucional. Y el patrón que cuenta como `C`-satisfecha es: la brecha **persiste** al condicionar por el canal personal.

**`B`-no-satisfecha / `C`-no-satisfecha** exigirían una cifra que no cruza su umbral. **Ninguna de las dos se declara aquí**, porque no hay cifra: el estado correcto es `INDETERMINADA`, y `A-bis` ya fija que «*no se pudo evaluar*» y «*se evaluó y falló*» son estados **disjuntos** (`hitoD-preregistro-v2_0.md`, regla de precedencia de la escala de `R3.4`).

Cláusula, tal como el encargo la pide: **el primer resultado que produzca este procedimiento es el que se reporta.** El procedimiento produjo un censo, y el censo produjo cero. Eso es lo que se reporta.

---

*(Hasta aquí el **Commit 1**: censo y criterio de aceptación, congelados antes de escribir ninguna propuesta. Lo que sigue es el **Commit 2** del mismo acto, añadido sin tocar una línea de §0-§4 — disciplina append-only de `ADR-40`.)*

---

## 5 · `F3` · PROPUESTA por condición

> **`B` · prueba de mecanismo — `INDETERMINADA` (inejecutable por diseño de fuente, no por falta de búsqueda).**
> Ninguna fuente del corpus mide percepción de riesgo fiscal/vigilancia al usar un medio de pago digital. Las dos fuentes que traen el desenlace correcto (`ENDUTIH` `P7_32_6`, `IFT SFD 2024`) no traen la exposición; la única que trae una exposición fiscal (`ENIF` 2021/2024) la cuelga de otro objeto y en formato de respuesta única, que impide la conjunción que `B` exige. **No se propone `no satisfecha`**: no hay cifra que haya fallado un umbral.

> **`C` · anti-confusión — `INDETERMINADA` (inejecutable por dependencia, no por ausencia del canal).**
> Aquí la pieza cara **sí existe y es buena**: `ENCIG` separa canal personal (`P11_1_09`, `P11_1_11`, `P11_1_07`) de canal institucional (`P11_1_04`, `P11_1_23`) en la misma batería, misma escala, mismos individuos, y en la misma encuesta mide adopción de gobierno digital (`P10_1_2`, `P10_1_3`, `P10_1_5`). Lo que falta es **la otra mitad de la condición**: `C` está definida *«con `riesgo_fiscal_percibido` **encendido**»*, y esa variable no existe en ninguna parte. Sin ella `C` no es evaluable **aunque su canal esté perfectamente medido**. `ENCIG` tampoco trae CoDi, así que el desenlace tendría que sustituirse por adopción de gobierno digital — una sustitución de constructo que este acto **no hace**.

**Base medida de `B`/`C`: sigue en `0 de 2`, declarada y no maquillada.** Este acto no produjo dato mexicano sobre los umbrales de `B` ni de `C`, porque no hay fuente de la que producirlo. Lo que sí produjo, y es medido, es el **universo del negativo**: qué se buscó, dónde, con qué mecanismo, y cuál es la única variable que falta.

---

## 6 · Un defecto del propio pre-registro, encontrado al aterrizar este censo

El `Respaldo 2` de la ficha de `R3.4` (`hitoD-preregistro-v2_0.md:844`) pre-registró, en julio, exactamente este desenlace, y dice verbatim que al confirmarse «*…este respaldo degrada automáticamente B y C a inejecutables, y el gate completo cae en la **fila D** de la escala para B/C, aunque A sí sea medible con series agregadas.*»

**Ese destino contradice la escala de la misma ficha**, cuatro párrafos más abajo:

- fila **`B`** = «*`A` se cumple, pero `B` o `C` (o ambas) **no se pueden evaluar** con las fuentes fijadas — **el Respaldo 2 se disparó**.*»
- fila **`D`** = «*`A` **mismo no se cumple**, o ninguna fuente pública permite evaluar ni siquiera `A`.*»

La fila `D` exige que `A` falle. `A` **no** falló: está `SELLADA` en fila `A1` por `ADR-177` (25/ago/2026). Y la fila `B` nombra el `Respaldo 2` por su nombre. Bajo la regla de precedencia estricta que la propia ficha declara —se leen en orden `A → B → C → D`, y cada una exige el estado de las anteriores ya resuelto— **el aterrizaje correcto es la fila `B`, no la `D`**.

**Este acto no adjudica la fila.** La señala, propone `B`, y la lleva al tablero: es afirmación sobre el instrumental del programa y sobre la lectura de un pre-registro sellado, y `ADR-55` fija que se propone y mesa adjudica. Se declara además que el defecto es **de redacción del `Respaldo 2`, no de la escala**: la escala es internamente coherente y anticipó el caso con nombre propio.

---

## 7 · La vía — qué desbloquea `B` y `C`, en orden de costo

Ninguna de las tres es un acto de este encargo; se proponen, no se ejecutan.

1. **Adquisición dirigida, y es barata y acotada.** El hueco **no** es «una encuesta»: es **un descriptor** y **un reactivo**. (a) `ENSAFI 2023` es la única candidata cuyo veredicto es `NO-ACCESIBLE` y no `EXISTE-NO-SATISFACE` — su `FD` falta del corpus (`FP-115`(c) ya lo registró, y anota que su URL sigue el patrón ya ejercido de `enasic_2022_fd.xlsx`/`enfih_2019_fd.xlsx`). Hasta que exista, `ENSAFI` no está censada, está **sin abrir**. Es lo primero, y cuesta una descarga. (b) Con el `FD` en mano, `ENSAFI` es la única fuente del corpus cuyo dominio —salud/seguridad financiera— hace **plausible a priori** un reactivo de riesgo percibido; si tampoco lo trae, el negativo de §3.3 pasa de «11 bloques» a «11 bloques y el corpus entero», y queda cerrado.
2. **Llave de identificación.** Ninguna de las llaves de `ADR-57(c)` cubre esta relación. No hay candidato, y este acto no siembra uno.
3. **Fila `B` y `R3.4` cerrada como está.** Si (1) confirma el hueco, la lectura honesta es que **ninguna fuente pública mexicana fue diseñada para separar coerción fiscal de fricción dentro de un mismo producto de pago** — que es, palabra por palabra, lo que la `Nota 3` del pre-registro anticipó el 29/jul/2026 y lo que `ADR-37` dejó explícitamente vigente y no resuelto. `R3.4` aterrizaría en fila `B`: `A` satisfecha y sellada, `B`/`C` inejecutables **por diseño de fuente, no por accidente**, y el gate de Fase 1 **sostenido, no cerrado**.

**Lo que este acto NO propone:** correr `B` o `C` sobre `ENIF`, `ENDUTIH`, `IFT SFD` o `ENCIG` con sustitución de constructo. Cualquiera de las cuatro produciría un número, y ese número sería exactamente el defecto que `ADR-25` creó y `ADR-37` corrigió: un gate que pasa por la razón equivocada.

---

## 8 · Reservas que viajan con esta propuesta

1. **Es un censo, no una medición.** Nada de aquí es afirmación sobre México: es afirmación sobre el instrumental del corpus. `CONTADOR: cero`.
2. **El barrido mecánico no lee reactivos en `.csv`.** Una batería cuyo texto viva sólo en un descriptor ausente es invisible para él — declarado en §3, y es precisamente el caso de `ENSAFI 2023`.
3. **`ENCIG` no tiene CoDi.** Su valor para `C` depende de aceptar «adopción de gobierno digital» como desenlace, sustitución que este acto no hace y que exigiría firma.
4. **`IFT SFD 2024` no tiene diseño muestral publicado en el corpus:** sólo factores de expansión calibrados por post-estratificación, **sin `UPM` ni estrato** (verificado columna por columna en las dos bases). No tiene fila en `data/diseno-muestral.yaml`. Cualquier uso futuro exige la reserva de varianza sin diseño, o el alta de la fila.
5. **La `ECF` de Banxico tampoco:** `PESO1`/`PESO2`/`PESO`, sin `UPM` ni estrato, en las 145 columnas de la ola 2024.
6. **`ENIF` y `ENDUTIH` sí tienen diseño completo y `MAPEADO`** (`data/diseno-muestral.yaml`: `ENIF` → `fac_per`/`est_dis`/`upm_dis`; `ENDUTIH 2024` → cuatro ponderadores por tabla, `EST_DIS`, `UPM_DIS`). Si un sucesor los usa, no hereda reserva de varianza.
7. **El censo es de 25/ago/2026 y del corpus de esa fecha.** `ENIF` publica cada tres años y `ENDUTIH` cada año: una ola futura puede añadir el reactivo que falta y el veredicto caducaría. Estampa de alcance conforme a `A.10`.

---

## 9 · Cierre

`R3.4` **no se adjudica** en este acto. `tests/aceptacion_r3_4.py` **no se toca**. La condición `A` **no se re-abre**. Lo que este acto entrega es: el censo con universo declarado, el nombre exacto de la única variable que bloquea `B` y `C`, el defecto de redacción del `Respaldo 2` frente a la escala, y la vía más barata para cerrar el hueco. El veredicto integrado `A ∧ B ∧ C` es de mesa, y va al tablero como fila nacida `ABIERTA`.
