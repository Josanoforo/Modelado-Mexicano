# Censo de estimabilidad de los 15 coeficientes de generador
### `censo-estimabilidad-coeficientes` · **v1.0** · 4 de agosto de 2026 · Encargo E-CE, acto de escritorio (nube, sin microdato)

> | | |
> |---|---|
> | **ARCHIVO** | `censo-estimabilidad-coeficientes-v1_0.md` |
> | **QUÉ ES** | Para cada uno de los 15 coeficientes de generador (`milpa/procedencia.yaml:612-639`): su clase citada, un desenlace co-observado candidato si existe, el cruce obligatorio contra descartes ya registrados, la marca (b) si aplica, el estado de la compuerta de identificación de ADR-57(c) (`gobernanza:623`), y una clasificación de ruta + prioridad. |
> | **QUÉ NO ES** | No abre ningún microdato, no corre ninguna estimación, no cambia ningún valor `ASIGNADO`, no adjudica ningún veredicto de Hito D. Es censo de estado, no medición. |
> | **VERIFICAS ASÍ** | §7 trae el comando que deriva el reparto de rutas contra este mismo archivo — no se teclea la suma. |

---

## 0 · ARRANQUE (resumen; detalle en la nota propia)

Clon existente en `/home/user/Modelado-Mexicano` (no home). `HEAD` al abrir este acto: `8cdabcb` (merge de PR #106) — coincide exactamente con el SHA declarado por el encargo; `git fetch origin main` confirmó `origin/main == 8cdabcb`, cero deriva, no hubo que re-derivar nada. `git status`: árbol limpio. Modo del encargo: **"no toca microdato ni red"** — el punto 4 (ENTORNO) se salta por instrucción explícita del propio encargo (nube, sin sonda). `data/raw`: no aplica — este acto no descarga nada, no se verifica corpus compartido. Todo lo que sigue sale de `git grep`/`Read` contra el clon; ninguna cifra viene del espejo (§5 del Bloque D).

---

## 1 · Las cuatro rutas — definición nueva de este acto, no canon heredado

Búsqueda exhaustiva (`grep -rni` sobre `*.md`/`*.yaml`) de `RUTA-C`, `RUTA-I`, `RUTA-A`, `SIN-RUTA` y variantes: **cero resultados previos en el repo.** Esta taxonomía no existe en `canon/` ni en ningún ADR — la introduce este censo, por instrucción del propio encargo, y se declara así en vez de presentarla como heredada (Regla de oro, `instrucciones-proyecto-v2_4.md`). No rige nada hasta que una mesa la selle con ADR; hoy es etiqueta de censo, no compuerta del motor.

Las cuatro clases se derivan directamente de la compuerta de identificación que **ADR-57(c)** ya sella (`gobernanza-v1_15.md:623`) y del hecho, verificado en Encargo W, de que una co-observación limpia solo produce **asociación**, nunca identificación, salvo que exista una de las tres llaves nombradas:

- **RUTA-A · Asociación ya corrida.** Existe un β̂ marginal ya medido (reactivo × desenlace co-observados, misma tabla o mismo instrumento) y rotulado por ADR-57(a) como asociación, no identificación. Los tres casos del Encargo W caen aquí.
- **RUTA-I · Identificada, llave sellada y no ejercida.** Existe una llave de identificación de las tres que `gobernanza:623` nombra (panel con el desenlace en el instrumento / experimento natural con grupo de comparación / diseño experimental de terceros), verificada y viva para este coeficiente concreto — pero ninguna llave de la lista está ejercida hoy (`gobernanza:623`, verbatim), así que "identificada" describe la llave, no un coeficiente ya calibrado.
- **RUTA-C · Candidata.** Existe un reactivo (medido o `MEDIDO·PARCIAL`) y un desenlace candidato, co-observables en principio dentro del mismo instrumento — pero la corrida no se ha ejecutado, o el candidato tiene una limitación estructural declarada y no resuelta. Su techo, si se corre hoy contra el corpus transversal disponible, es RUTA-A: ninguna de las tres llaves de ADR-57(c) cubre estos casos.
- **SIN-RUTA.** No hay candidato de co-observación en el corpus citable hoy: falta el reactivo, falta el desenlace, el único candidato conocido es circular (marca C3), o la búsqueda de reactivo ya se cerró formalmente con argumento (ADR-52 A / ADR-54).

---

## 2 · Método y qué aportó cada fuente cruzada

- **`milpa/procedencia.yaml`** — fuente primaria de clase (`ASIGNADO`, línea 612-642), de los tres β̂ ya medidos (`coeficientes_generador_medidos`, líneas 659-745) y de las condicionales `MEDIDO·PARCIAL(x)` que sirven de reactivo candidato (`condicionales_confianza_institucional`, `condicionales_escalares`, `condicionales_escalares_exposicion_violencia`, líneas 133-423).
- **`data/manifiesto.yaml`** — confirma qué instrumentos tienen payload registrado (ENCIG, ENCUCI, ENIF, ENVIPE, ENNViH/MxFLS tres olas, ENOE/ENOEN, ENUT, ENIGH, ENSANUT, ENDIREH, ENDUTIH, MOCIBA, LAPOP, Latinobarómetro, CPV, ENADID, ENCUP — `grep -c "^- id:" data/manifiesto.yaml` = 202 entradas). Usado para verificar que un candidato citado más abajo no es hipotético: el instrumento existe en disco o está registrado.
- **`data/diseno-muestral.yaml`** — 9 `MAPEADO` / 2 `SIN_DISEÑO_PUBLICADO` / 32 `PENDIENTE` (cifra ya derivada y citada en `forense/hallazgos.md:110`). Relevante aquí solo donde cambia una clasificación: ENNViH/MxFLS (la llave viva de ADR-57(c)) está `PENDIENTE` en este censo de diseño — el payload de las tres olas existe (`manifiesto.yaml`, líneas 457-981) pero el nombre de columna de estrato/UPM no quedó citado ahí; **`CAL-G3` (abajo, fila G3·horizonte_temporal) sí cita su propio ponderador/estrato/UPM por ola**, desde antes de que `diseno-muestral.yaml` existiera — no hay contradicción, son dos censos con fecha de corte distinta.
- **`data/catalogo-fuentes-v2_0.md`** — inventario de fuentes por dominio/clase, no por variable (declarado en su propio §"Lo que este documento no hace", línea 184-187). Revisado completo: no aporta ningún candidato de reactivo o desenlace a nivel de coeficiente que no esté ya en `procedencia.yaml`/`modelo-decision`/`hitoD-preregistro` — su unidad es la fuente, no el ítem.
- **`forense/cruce-catalogo-fichas-v2_0.md`** ("cruce v2.0") — cruza el catálogo contra las 27 fichas de Hito D (veredictos de falsación de reglas), no contra los 15 coeficientes de generador. Revisado completo (§3.1-§3.10): cero mención de `coeficientes_generador_medidos`, cero mención de `asignados_coeficiente`. No aporta candidatos nuevos aquí — se declara el negativo en vez de omitirlo.
- **`canon/modelo-decision-v4_0.md`** §1.1.E-F (H-01 a H-12, líneas 214-227) y §2.1-2.2 (líneas 370-398) — origen de la mayoría de los candidatos y de los cierres de búsqueda ya sellados (ADR-52 A, ADR-54).
- **`forense/hitoD-preregistro-v2_0.md`** Notas 7-10 (líneas 478-651) — la ficha `CAL-G3`, único caso con llave de identificación ya corrida a nivel descriptivo.
- **`forense/hallazgos.md`** — barrido de actos de medición ya corridos sobre ENVIPE/ENDIREH para los desenlaces de G4 (líneas 72, 77, 87, 90, 94 del archivo).

---

## 3 · Cruce obligatorio — descartes ya registrados, ninguno se re-propone

**`forense/descartes-forenses-registro.md`, leído completo.** Registra los descartes de casos de los cinco forenses verticales V1-V5 (apuestas conductuales, clientelismo electoral, consumo aspiracional, crédito popular, crédito fácil) — sesgo de superviviente sobre estudios de caso de dominio financiero/electoral. **Cero traslape de dominio**: ninguno de los 15 coeficientes ni sus candidatos de este censo (ENCIG, ENCUCI, ENIF, ENVIPE, ENNViH, ENIGH, ENDIREH, Latinobarómetro) es un caso descartado en ese archivo — verificado por lectura completa, no por grep de nombre (el archivo no nombra instrumentos de encuesta, nombra casos de negocio). **Ninguna fila de este censo reutiliza un descarte de `descartes-forenses-registro.md`.**

**ADR-49 D1** (`gobernanza-v1_15.md:791`; también `modelo-decision-v4_0.md:402`) retira `unico_calibrable_hoy`: la premisa de que el panel rotativo de la ENOE permite estimar `G3 → horizonte_temporal` vía conducta financiera **muere a nivel de reactivo** — ningún cuestionario ENOE/ENOEN trae ahorro, crédito, deuda, planeación ni expectativas (`forense/hallazgos.md`, 31/jul/2026). Esta ruta (ENOE → `G3.horizonte_temporal`) **no se re-propone en este censo** — la fila `G3 · horizonte_temporal` (§5) reporta una ruta distinta (ENNViH/MxFLS, panel, vía `CAL-G3`), no la descartada. Se deja constancia explícita en la fila para que quede visible que la ruta descartada fue vista y rechazada, no que fue pasada por alto.

---

## 4 · Marca (b) — alcance verificado

Búsqueda de "(b)" contra `modelo-decision-v4_0.md` (líneas 216, 222-224, 239, 784): la marca **solo** cubre `familismo_apoyo` y `familismo_obligacion` — *"se sostienen en escalas validadas en muestras mexicano-americanas (Sabogal, Lugo Steidel, Knight, Calzada, Zeiders)... H-09, H-10 y H-11 heredan la marca"* (línea 239). `radio_confianza` la lleva solo en su hipótesis condicional de migración (H-03, línea 216: *"el radio transnacional se sostiene en evidencia de diáspora"*), no en su cita base (que es reactivo directo ENCUCI, población en México) — no se hereda al coeficiente. Ningún otro de los 15 (`confianza_institucional`, `sens_estatus`, `aversion_riesgo`, `horizonte_temporal`, `exposicion_violencia`, `deferencia`) tiene marca (b) declarada en ningún punto del corpus revisado.

**Aplica a:** `G3·familismo_apoyo`, `G5·familismo_apoyo`, `G5·familismo_obligacion` — mismo parámetro asignado, misma deuda de procedencia, citada tres veces porque aparece en dos generadores (`procedencia.yaml:633-635`, comentario ADR-30: *"AMBOS parámetros heredan marca (b)"*).

---

## 5 · Las 15 filas

| # | Gen | θ (coeficiente) | Clase citada | Desenlace co-observado candidato | (b) | Palanca ADR-57(c) — estado citado (`gobernanza:623`) | Ruta | Prioridad |
|---|---|---|---|---|---|---|---|---|
| 1 | G1 | `confianza_institucional` −0.60 | `ASIGNADO` (`procedencia.yaml:625`); β̂ marginal `MEDIDO·β̂` desde Encargo W (`procedencia.yaml:687-718`) | `tramite.mordida.discrecional` — ENCIG 2023 `P11_1_23`× `P8_3_1/2/3`, unidas por `ID_PER` (`procedencia.yaml:690`) | No | Ninguna llave cubre trámite/mordida (ENNViH, ENASEM y ENOE-laboral no aplican) — techo ya alcanzado: asociación, rotulada ADR-57(a) | **RUTA-A** | BAJA — ruta activa, no de censo; siguiente acto es de condicionamiento, ya corrido (Encargo X), no de apertura de ruta |
| 2 | G1 | `radio_confianza` −0.35 | `ASIGNADO` (`procedencia.yaml:625`); β̂ marginal `MEDIDO·β̂` desde Encargo W (`procedencia.yaml:660-686`) | `tramite.mordida.discrecional` — ENCUCI 2020 `AP5_1_1/2/3` × `AP5_17/18` (`procedencia.yaml:663`) | No | Ninguna llave aplica — techo ya alcanzado: asociación (ADR-57(a)) | **RUTA-A** | BAJA — ruta activa; además pasó a `ASIGNADO · SIGNO BAJO PRUEBA` (ADR-60(e), `gobernanza:695`), condición de resolución en el acto `W1-P`, fuera de este censo |
| 3 | G2 | `sens_estatus` 0.55 | `ASIGNADO` (`procedencia.yaml:626`) | Desenlace `dinero.consumo.estatus_mediado_por_credito` sí identificado en ENIGH (`gastotarjetas`/`tarjeta`/`pagotarjet`, `forense/notas/2026-07-31-inventario-segmentacion.md:332`) — pero **no hay reactivo de `sens_estatus`**: búsqueda cerrada por ADR-54 (`gobernanza` §4), examen de descriptor de `PR #64` recorrió los cinco instrumentos permitidos del régimen, ninguno sirve (`forense/notas/2026-08-04-sens-estatus-examen-descriptor.md`); usar el propio `gastotarjetas` de reactivo sería circular (mismo archivo, fila ENIGH: *"es el desenlace conductual... circular"*) | No | Ninguna llave cubre consumo por tarjeta | **SIN-RUTA** | BAJA — búsqueda de reactivo cerrada formalmente, exige instrumento fuera del régimen actual |
| 4 | G2 | `aversion_riesgo` 0.20 | `ASIGNADO` (`procedencia.yaml:626`) | Sin desenlace propio identificado (ninguna regla `PORQUE G2` lo nombra como driver único). Único candidato de reactivo examinado y descartado: ENIF `P5_23`/`P5_24` mide conocimiento de protección de depósitos IPAB, el moderador que `dinero.ahorro.seguro_deposito_atenua_aversion` (regla de **G1**, no G2) pone en el `SI` — no una medida de aversión (`modelo-decision-v4_0.md:270`, `hitoE §17`). Búsqueda cerrada (mismo criterio ADR-52 A) | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — búsqueda de reactivo cerrada formalmente; tampoco tiene desenlace propio nombrado |
| 5 | G3 | `horizonte_temporal` −0.60 | `ASIGNADO` (`procedencia.yaml:627`) | Transición formal/informal del instrumento de crédito del hogar (`CRH01`, 11 categorías por ola) sobre el panel **ENNViH/MxFLS**, tres olas, mismo hogar — ficha `CAL-G3` (`hitoD-preregistro-v2_0.md`, Nota 7 líneas 478-524, Adenda 1 líneas 525-553, Nota 8 líneas 554-648). Fase C **ya corrida** sobre olas 2-3, descriptiva, sin calibrar el `−0.60` y sin tocar `procedencia.yaml` (Nota 10, línea 649 y siguientes; *"No calibra el `-0.60`"*, línea 653; reproducible: `tests/calg3_fasec.py`) | No | **SÍ — llave (i) nombrada explícitamente**: *"ENNViH/MxFLS — panel de tres olas, dominio público; ruta viva vía `CAL-G3` (Fase C desbloqueada, olas 2-3, alcance descriptivo; la promoción de descriptivo a identificado exige su propio diseño intra-persona, no está concedida aquí)"* (`gobernanza:623`, verbatim) | **RUTA-I** | **ALTA** — llave sellada, payload ya en disco, fase descriptiva ya corrida; falta el diseño intra-persona para promover a identificación, no un instrumento nuevo |
| 6 | G3 | `aversion_riesgo` 0.40 | `ASIGNADO` (`procedencia.yaml:627`) | Mismo parámetro que la fila 4 — la búsqueda de reactivo de `aversion_riesgo` es única y ya cerrada (ADR-52 A, `modelo:270`), no se repite por generador | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — misma búsqueda cerrada que la fila 4 |
| 7 | G3 | `familismo_apoyo` 0.20 | `ASIGNADO` (`procedencia.yaml:627`); β̂ marginal `MEDIDO·β̂` desde Encargo W (`procedencia.yaml:719-745`) | `dinero.ahorro.volatilidad_horizonte_corto` — ENIF 2024 `p9_9_4` × `P4_10` (`procedencia.yaml:722`) | **Sí** | Ninguna llave aplica — techo ya alcanzado: asociación (ADR-57(a)) | **RUTA-A** | BAJA — ruta activa, no de censo |
| 8 | G4 | `exposicion_violencia` 0.70 | `ASIGNADO` (`procedencia.yaml:628`); θ ahora `MEDIDO·PARCIAL(edad,dominio,formalidad,ESTRATO)` — ENVIPE 2025 `TPer_Vic2`, `AP7_3_10`-`_14` (`procedencia.yaml:315-423`, Encargo K) | `comunicacion.inseguridad.ver_oir_callar` vía `BP1_23` (mismo ENVIPE 2025), candidato "Parcial" ya nombrado (`hitoE §15`; `procedencia.yaml:396-413`, `limite_c2`) — **con limitación estructural declarada y no resuelta**: `BP1_23` solo se pregunta a quien ya disparó `AP7_3_XX`=1, dependencia determinística de la misma subpoblación, no independiente por diseño del instrumento. `civico.protesta.agravio_urbano`/`civico.autodefensa.agravio_rural` buscados a fondo dentro de ENVIPE (`TPer_Vic1`: *"LA FUENTE NO TIENE EL DATO"*, `hallazgos.md:87`; `TPer_Vic2`/`TMod_Vic`: *"ningún wording literal... vive"*, `hallazgos.md:90`) — negativo declarado, no candidato aquí. ENDIREH (complemento declarado de `exposicion_violencia`, no el reactivo usado) queda abierto sin resolver por lectura incompleta (`hallazgos.md:77`) | No | Ninguna llave cubre exposición a violencia/conducta cívica — techo, si se corre: asociación | **RUTA-C** *(con limitación estructural declarada)* | MEDIA — requiere adjudicación de mesa sobre `BP1_23` antes de correr nada (la propia `procedencia.yaml` lo declara: *"adjudicación que corresponde a quien opere ese desenlace, no a un acto de medición"*) |
| 9 | G4 | `confianza_institucional[justicia]` −0.40 | `ASIGNADO` (`procedencia.yaml:628`); θ ya `MEDIDO·PARCIAL(edad,dominio)` por institución — ENVIPE 2025 `TPer_Vic1`, `AP5_4_01/02/03/05/06/07/11` (`procedencia.yaml:191-201`) | Mismo candidato `BP1_23`/`ver_oir_callar`, mismo instrumento ENVIPE 2025, unión vía `ID_PER` entre `TPer_Vic1` y `TPer_Vic2` (mismo patrón de *join* que ya usó la fila 1 entre tablas de ENCIG) — misma limitación estructural que la fila 8 | No | Ninguna llave aplica — techo: asociación | **RUTA-C** *(con la misma limitación estructural que la fila 8)* | MEDIA — mismo bloqueo de adjudicación sobre `BP1_23` |
| 10 | G4 | `horizonte_temporal` −0.20 | `ASIGNADO` (`procedencia.yaml:628`) | Sin reactivo dedicado: el único proxy conocido de `horizonte_temporal` (ENIF `P4_10`) falla C3 frente al desenlace de **G3** (fila 5, H-01, `modelo:214`), y aunque no fallara, vive en un instrumento distinto (ENIF) de los desenlaces de G4 (ENVIPE/ENDIREH) — sin muestra común, no co-observable. `CAL-G3`/ENNViH (fila 5) no observa ningún desenlace de G4 | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — búsqueda no cerrada formalmente, pero sin candidato hoy |
| 11 | G4 | `sens_estatus` −0.15 | `ASIGNADO` (`procedencia.yaml:628`) | Mismo parámetro que la fila 3 — búsqueda de reactivo cerrada (ADR-54) | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — misma búsqueda cerrada que la fila 3 |
| 12 | G5 | `familismo_apoyo` 0.50 | `ASIGNADO` (`procedencia.yaml:629`) | Único reactivo candidato conocido (ENIF `p9_9_4`, mismo de la fila 7) **excluido por circularidad**: el desenlace de G5 en ENIF es la misma batería `P9_9_1..6` (`familia.seguro.volatilidad_ausencia_estado`) que opera el reactivo — *"NO USAR para identificar G5·familismo_apoyo... circular"* (`procedencia.yaml:265-270`, marca C3) | **Sí** | Ninguna llave aplica | **SIN-RUTA** | BAJA — único candidato conocido, ya descartado por circularidad declarada en archivo |
| 13 | G5 | `familismo_obligacion` (signo negativo o no monotónico — **sin magnitud asignada**, único caso de los 15) | `ASIGNADO` sin magnitud (`procedencia.yaml:629`, ADR-30) | Su condicional θ_k(x) solo tiene "proxy con supuesto declarado" (ENUT 6.11/6.11a, H-11, `modelo:224,271`), forma **PENDIENTE**; ningún cruce contra desenlace intentado en el corpus revisado | **Sí** | Ninguna llave aplica | **SIN-RUTA** | BAJA — no hay siquiera magnitud que calibrar, solo dirección hipotética bajo prueba (ADR-30) |
| 14 | G5 | `radio_confianza` 0.15 | `ASIGNADO` (`procedencia.yaml:629`) | Reactivo existe (ENCUCI, mismo de la fila 2, `MEDIDO·PARCIAL`) pero el desenlace de G5 (`familia.seguro.volatilidad_ausencia_estado`) vive en ENIF — instrumento distinto, sin muestra común, no co-observable dentro de un mismo cuestionario | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — reactivo y desenlace existen por separado, en instrumentos que no comparten muestra |
| 15 | G6 | `deferencia` 0.45 | `ASIGNADO` (`procedencia.yaml:636`) | Único proxy de θ es Latinobarómetro 2024 `P4NOIJ` ("Obediencia" entre cualidades a inculcar en los niños), México n=1200 (H-07/H-08, `modelo:220-221`, ADR-51(f)) — ningún desenlace de G6 (`trabajo.jerarquia.deferencia_iniciativa_suprimida`, `comunicacion.retroalimentacion.privada_publica_capital_social`) documentado dentro de Latinobarómetro en el corpus revisado. Instrumento además `SIN_DISEÑO_PUBLICADO` (`data/diseno-muestral.yaml:465-466`) | No | Ninguna llave aplica | **SIN-RUTA** | BAJA — único proxy de θ es un instrumento internacional sin desenlace propio conocido, y sin diseño muestral publicado |

---

## 6 · Cero descartes resucitados — verificación fila por fila

Ninguna de las 15 filas propone la ruta ENOE→`G3.horizonte_temporal` (ADR-49 D1, §3 arriba) ni un caso de `descartes-forenses-registro.md`. Dos filas (12 y 3-4-6-11) reportan explícitamente un descarte **ya sellado por otro ADR/nota** (ADR-54, ADR-52 A, marca C3 de `procedencia.yaml`) — se citan, no se re-abren ni se re-proponen como candidato nuevo: se listan como razón de `SIN-RUTA`, que es precisamente lo que "no re-proponer" exige.

---

## 7 · Reparto — comando y resultado

**La receta se verifica antes de creer la cifra (v2.3).** Un primer intento, ingenuo, sobre todo el archivo:

```
grep -oE 'RUTA-[CIA]|SIN-RUTA' forense/censo-estimabilidad-coeficientes-v1_0.md | sort | uniq -c
```

sobre-cuenta, y por construcción no tiene una cifra estable que citar aquí: cuenta también las cuatro etiquetas nombradas en la definición de §1, las menciones de §3/§6 y el propio texto de este §7 — que a su vez cambia cada vez que este párrafo se edita, así que cualquier número fijado aquí quedaría obsoleto en la siguiente edición (auto-referencia, no cifra de reparto). Eso ya es evidencia suficiente de que la receta ingenua está mal — exactamente el modo de falla que v2.3 pide probar antes de confiar en un comando, sin necesidad de fijar el número inestable por escrito.

**Receta corregida — solo filas de datos de la tabla de §5** (cada fila empieza con `| N |`, patrón que ninguna línea de prosa de este archivo repite):

```
grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_0.md | grep -oE 'RUTA-[CIA]|SIN-RUTA' | sort | uniq -c
```

Resultado real, corrido contra este archivo tal como quedó escrito:

```
      3 RUTA-A
      2 RUTA-C
      1 RUTA-I
      9 SIN-RUTA
```

`grep -cE '^\| [0-9]+ \|'` confirma **15 filas de datos** en la tabla. **3 + 2 + 1 + 9 = 15.** Ninguna fila quedó sin clasificar, ninguna se contó dos veces.

---

## 8 · Lo que este censo NO hace

No corre ninguna estimación ni abre ningún ZIP de microdato — donde un candidato lo exigiría (adjudicar `BP1_23`, leer las 20 secciones de ENDIREH completas, diseñar el corte intra-persona de `CAL-G3`), **se declara y se deja a la tanda**, tal como el encargo instruye. No cambia ningún valor `ASIGNADO` ni ninguna clase de procedencia existente — solo añade el campo `ruta:` nuevo (`milpa/procedencia.yaml`, cascada de este mismo acto). No adjudica ningún veredicto de Hito D. No decide si `G1a` se desdobla, no toca el vector de `confianza_institucional`, no resuelve `W1-P`. No es canon: la taxonomía de rutas (§1) no rige nada hasta que exista un ADR que la selle.

**Foto del corpus, declarada.** El reparto de este censo se derivó contra `HEAD=8cdabcb` (merge de PR #106) — ver §0. `PR #107` (ENASEM 2018/2021/2024, BD+FD, seis payloads nuevos en `data/manifiesto.yaml`: `enasem{2018,2021,2024}_{bd_csv_zip,fd_xlsx}`) se fusionó a `main` en `65302f7` **después** del commit de este censo (`0db6d1d`, `Tue Aug 4 21:11:53 -0600`; `65302f7`, `Tue Aug 4 21:14:21 -0600` — 2 min 28 s de diferencia) y **no fue cruzado aquí**. ENASEM/MHAS es un panel 50+, tres olas ahora en disco: tiene la forma de una llave de identificación (panel con el desenlace en el instrumento — la misma definición de `RUTA-I`, §1), sin haberse cruzado contra ninguno de los 15 coeficientes; no se re-clasifica ninguna fila por esto, queda nombrado como el primer candidato a revisar del censo v1.1. El encargo declara, además, que el barrido `B-3` corre en paralelo y puede añadir más candidatos — no verificado contra este repositorio (`git grep` sobre `forense/`/`milpa/` para `B-3`: cero resultados al cierre de este acto), se reporta tal como mesa lo declaró. Por lo anterior, el reparto `RUTA-A=3 · RUTA-I=1 · RUTA-C=2 · SIN-RUTA=9` se lee **vigente al SHA `8cdabcb`**, no como estado del programa.

---

## Versión y nombre de archivo

Archivo nuevo — no reemplaza ninguno existente. No hay versión previa que retropropagar.
