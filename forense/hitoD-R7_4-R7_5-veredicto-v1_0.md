# HITO D · `R7.4`/`R7.5` — el falsador compartido corrido contra las tres fuentes adquiridas, archiva `D` en las dos

### `hitoD-R7.4-R7.5-veredicto` · **v1.0** · 24 de agosto de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R7_4-R7_5-veredicto-v1_0.md` |
> | **NOMBRE ESTABLE** | **`hitoD-R7.4-R7.5-veredicto`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | La corrida (COMMIT 2) de `hitoD-R7.4-R7.5-especificacion`: la tabla Q1-Q4 llena contra las tres fuentes reales adquiridas por `ACTO ADQ-CORRE-R74R75`. |
> | **QUÉ NO ES** | No inventa un cuarto instrumento. No toca `milpa/` ni los tiers de las reglas. |
> | **VERIFICAS ASÍ** | los tres payloads en `data/manifiesto.yaml` (ids `adqcorre_r74r75_*`, `ucdp_ged261_csv`); comandos Python reproducidos línea a línea en §1-§3; las 26 filas de §3 inspeccionadas una por una en `SOURCEURL`. |

**ESTAMPA DE UNIVERSO (`A.10`).** Sello sobre `origin/main = b053491`, 24/ago/2026, entorno **UBUNTU**. Universo examinado: **tres** payloads abiertos completos, no muestreados — UCDP GED v26.1 (417,968 filas, filtrado a 25,714 Mexico), Mass Mobilization mmALL v16 (17,145 filas, filtrado a 153 Mexico), GDELT 2.0 un día UTC completo real (97,839 filas, filtrado a 487 Mexico vía `ActionGeo_CountryCode`). GDELT 1.0 (`adqcorre_r74r75_gdelt_masterreducedv2`) se abrió y se descartó por defecto estructural, ver §0.

---

## 0 · GDELT 1.0 descartado antes de la tabla — sin columna de país

Las primeras líneas reales del archivo (`GDELT.MASTERREDUCEDV2.TXT` dentro del zip) traen encabezado `Date,Source,Target,CAMEOCode,NumEvents,NumArts,QuadClass,Goldstein,SourceGeoType,SourceGeoLat,SourceGeoLong,TargetGeoType,TargetGeoLat,TargetGeoLong,ActionGeoType,ActionGeoLat,ActionGeoLong` — 17 campos declarados, pero las filas reales traen 11 o 17 según si el geo viene poblado (`19790101 AFR FRA 043 1 4 1 2.8` = 11 campos; sin geo). **`Source`/`Target` son códigos CAMEO de actor de 3 letras** (mezclan país, región y rol — `AFR` es "Africa", no un país), **no hay ninguna columna equivalente a `ActionGeo_CountryCode`**, y no hay texto de artículo ni URL. Es un agregado diario actor-par-código, no un evento georreferenciado individual. **Inservible para Q1 (no aísla México) y para Q2 (no hay texto que clasificar).** Sustituido por el día real de GDELT 2.0 adquirido en el mismo acto (`adqcorre_r74r75_gdelt2_export_mx_20260824`), que sí trae `ActionGeo_CountryCode` (verificado empíricamente por `GDELT-UCDP-RECON`, 13/ago/2026, y reconfirmado aquí sobre datos de hoy).

---

## 1 · Mass Mobilization — Q1 parcial, Q2 y la conjunción imposibles por diseño

**153 filas `country=='Mexico'` de 17,145 globales, 1990-2020** (corrige el caveat "termina 2018" de la cola — ver `data/cola-adquisicion-2026-08-12.tsv` línea 15). `protesterdemand1` sobre las 153: `political behavior, process`=113 · `police brutality`=18 · `labor wage dispute`=9 · `price increases, tax policy`=4 · `land farm issue`=4 · `removal of politician`=4 · `social restrictions`=1 (suma=153). Muestra de `location` (texto libre): *Taxco, Guerrero state, western Michoacan state, Mexico City, San Luis Potosi, city of Guanajuato, Morelia, Nuevo Laredo, Juchitan, Teopisca…*

- **Q1 (universo con denominador):** parcial — 153 es un denominador real, pero **solo del universo "protesta"**, no del universo "toda respuesta colectiva a agravio" que la ficha pide (protesta + autodefensa).
- **Q2 (forma, categórica):** **NO construible.** El dataset es 100% protesta por criterio de inclusión (`protest`=1 constante) — 0 de 153 filas pueden, por diseño, caer en la categoría "autodefensa". Búsqueda de patrón (`autodefensa|self.defen|vigilant|comunitari`) sobre `protesteridentity`+`notes`+`protesterdemand1`: **1** coincidencia de 153, tangencial (no describe un caso de autodefensa como desenlace).
- **Q3 (entorno):** **NO construible sin trabajo nuevo.** `location` es texto libre de nombre de lugar (ciudad, estado, o frase como "Tabasco to Mexico City") — ninguna bandera rural/urbano, y §1.5 de la spec confirmó que no existe catálogo de referencia en este corpus para derivarla.
- **Conjunción Q4:** **imposible de construir.** Sin Q2 de dos categorías, no hay conjunción que contar.

---

## 2 · UCDP — Q1 hostil por umbral de letalidad, un solo caso nombrado, Q2/Q3 no construibles

**25,714 filas `country=='Mexico'` de 417,968 globales, 1989-2025.** `type_of_violence`: no-estatal=25,324 (98.5%) · unilateral=355 (1.4%) · estatal=35 (0.1%). Pares `side_a`/`side_b` dominantes: `Juarez Cartel`/`Sinaloa Cartel` (4,934) · `Jalisco Cartel New Generation`/`Sinaloa Cartel` (4,485) · `Jalisco Cartel New Generation`/`Santa Rosa de Lima Cartel` (3,516) — **narcotráfico entre organizaciones criminales, no la conjunción "agravio + falla estatal + red previa" que antecede a la regla.**

**El único actor nombrado que se acerca a "autodefensa" en las 25,714 filas mexicanas:** `Autodefensas Unidas de Michoacán` (búsqueda de patrón `autodefensa|comunitari|vigilant|civil defen` sobre `side_a`/`side_b`, 1 coincidencia). Sus eventos registran enfrentamiento armado con cárteles — el dataset registra la **violencia**, no el antecedente de agravio/falla estatal que la motivó, y no hay ningún caso comparable de "protesta institucional" en UCDP para poner del otro lado del cruce (UCDP no releva protesta no violenta, es su propio caveat de cola).

- **Q1:** hostil — el umbral de inclusión de UCDP (conflicto organizado con víctimas) excluye por construcción la enorme mayoría de "respuesta colectiva a agravio" que nunca escala a violencia letal sostenida. Lo que sí incluye está dominado 98.5% por un fenómeno distinto (narcotráfico) del mecanismo de la regla.
- **Q2:** **NO construible.** Un solo actor nombrado no es una categoría con n suficiente para nada, y UCDP no tiene contraparte de "protesta institucional" con la que cruzarlo.
- **Q3:** **NO construible sin trabajo nuevo** — mismo problema que MassMob: `adm_1`/`where_description` son nombre de lugar, no bandera rural/urbano.
- **Conjunción Q4:** **imposible de construir**, mismo motivo que MassMob, en el sentido opuesto (solo violencia, no protesta).

---

## 3 · GDELT 2.0 — el único con Q2 nominalmente completo, y por eso el más informativo: ruido, no clasificación

**487 filas `ActionGeo_CountryCode=='MX'` de 97,839 totales, día UTC 2026-08-24 completo (96/96 archivos, 6.1 MB, sin fallo de integridad).** Consistente con la extrapolación de `GDELT-UCDP-RECON` (13/ago/2026: ~532 filas MX/día estimadas desde muestra de 13/96 archivos, factor ×7.4) — validación cruzada entre dos actos independientes.

`EventRootCode` sobre las 487: `04`=127 · `01`=62 · `05`=43 · `17`=39 · `03`=35 · `11`=25 · `06`=24 · `08`=24 · `02`=23 · **`19`=19** · `12`=18 · `09`=11 · `07`=11 · **`18`=7** · `16`=7 · `10`=5 · `13`=4 · `15`=2 · **`14`=1** · `20`=0. `QuadClass`: cooperación verbal=290 · conflicto material=74 · cooperación material=70 · conflicto verbal=53.

- **`EventRootCode=='14'` (PROTESTA): 1 de 487 (0.2%).** Su `ActionGeo_FullName`: *"Jalisco, Baja California, Mexico"*; su artículo real (`SOURCEURL`) describe una comunidad **rural** en protesta — una sola observación, insuficiente para cualquier tasa, pero se registra que su entorno declarado (rural) contradice la asociación fuerte de `R7.4` (urbano→protesta) que el propio motor predice, sin que esto pueda leerse como cruce ni como confirmación con n=1.
- **`EventRootCode` en (`18`,`19`,`20`) — códigos adyacentes a fuerza/asalto/violencia: 26 filas (19:19, 18:7, 20:0), las 26 inspeccionadas una por una contra su `SOURCEURL` real** (no una muestra: el universo completo de esa categoría en el día). **Cero de 26** describe un caso de agravio+entorno→autodefensa. Contenido real: una columna nostálgica de historia local de un periódico de Washington (3 filas, mismo artículo), economía de importación de ganado (3 filas), un caso de homicidio en EE.UU. con sospechoso mexicano (3 filas), riesgo de tortura de un informante deportado (2 filas), una exhibición de arte sobre deportación, expansión de mapa de videojuego, orden de arresto de una concursante de Miss Universo, arrestos de ICE, una persecución policial cruzando a Texas, y una acusación de tráfico de cártel en Carolina del Sur. **Es ruido de clasificador automático sobre texto de prensa en inglés que menciona "Mexico" incidentalmente — exactamente el caveat que la cola ya declaraba ("ruido, validación y costo") y que este acto confirma con evidencia de contenido real, no con la portada.**

- **Q1:** GDELT es la única fuente con **potencial** de universo conjunto (protesta + violencia en el mismo esquema), pero el subconjunto real de un día no produce ni un caso limpio de ninguna de las dos ramas relevantes al mecanismo de la regla.
- **Q2:** nominalmente completo (existen los dos códigos), **sustantivamente vacío**: 1 caso de protesta sin corroborar agravio+entorno, 0 casos de autodefensa entre 26 candidatos inspeccionados.
- **Q3:** **NO construible sin trabajo nuevo.** `ActionGeo_FullName` da nombre de lugar (ej. "Mexico City, Distrito Federal, Mexico"; "La Placita, Durango, Mexico") — descriptivo, no codificado; mismo hueco que las otras dos fuentes, confirmado una tercera vez.
- **Conjunción Q4:** **no construible con un día de muestra**, y la vía de escalar (adquirir más días) no resuelve Q3 ni el ruido de clasificación de Q2 — son defectos de instrumento, no de volumen.

---

## 4 · Propuesta de fila, contra el árbol congelado

**Rama 3 → fila `D`, para `R7.4` y para `R7.5` — el mismo falsador, la misma corrida, dos veredictos.** Ninguna de las tres fuentes adquiridas construye Q1+Q2+Q3 sobre la misma unidad de caso, y la razón es la que `hitoD-R7.4-R7.5-especificacion §3-§4` predijo antes de correr: **las tres fuentes están diseñadas para relevar un tipo de evento (protesta pura, violencia letal pura, o prensa sin filtrar), no para relevar "respuesta colectiva a agravio, categorizada por entorno y forma" como objeto propio.** No es un hueco de dato mexicano —México está sobrerrepresentado en dos de las tres fuentes (153 casos en MassMob, 4° país más frecuente en UCDP)— es un hueco de **diseño de instrumento**, igual que `R8.1` y `R7.3`.

**La predicción pre-declarada se confirma, tercera vez que este patrón aparece en el programa.** La spec (§7) anticipó `falsador débil` como desenlace más probable "no por falta de casos mexicanos... sino porque ningún instrumento de los tres codifica conjuntamente entorno y forma sobre el mismo caso" — se confirma sin matiz.

**Verificado, sin solape de filas sin resolver.** `A`/`B` exigen una tasa o un caso cruzado con denominador; ninguna fuente lo da. `C` ("exigiría un registro codificado por entorno") **también se lee cierta** — y por la precedencia fijada en la spec (§6, precedente `ADR-56`), **manda `D`**: un registro así es concebible (GDELT + un clasificador de agravio/respuesta + un catálogo rural/urbano nuevo), pero construirlo es trabajo de instrumento nuevo, no un inventario pendiente de consultar. Ninguna de las dos reglas queda con fila sin decidir.

**Sobre archivar.** `D` es afirmación sobre nuestro instrumental, no sobre México, y `ADR-55`/`ADR-56` fijan que el acto que lo establece lo archiva. Este acto **archiva `R7.4` → `D` y `R7.5` → `D`** en el bloque append-only de `hitoD-preregistro-v2_0.md`, y el contador se mueve por esta ficha: **16 de 27 → 18 de 27.**

---

## 5 · Lo que desbloquearía `R7.4`/`R7.5`, nombrado y no genérico

1. **Un clasificador de agravio/respuesta sobre el flujo GDELT México** (no solo `EventRootCode` crudo — un modelo o regla que separe señal de los falsos positivos de §3, entrenado o validado contra una muestra etiquetada a mano) — es la pieza que convertiría "ruido" en "universo".
2. **Un catálogo de localidad→rural/urbano** unido por nombre de lugar o coordenada — no existe en este corpus (§1.5 de la spec) y ninguna de las tres fuentes lo trae. Es la pieza más barata de las dos: existen catálogos públicos de localidad de INEGI que este acto no adquirió (fuera de las 5 filas de la cola que gatillaron este acto).
3. **Lo que NO desbloquea:** más días de GDELT sin el clasificador de (1) — escalar volumen no resuelve un problema de precisión de clasificación ni construye Q3. Tampoco desbloquea adquirir más fuentes del mismo tipo (más catálogos de protesta pura o de violencia pura): el hueco es la conjunción, no el volumen de ninguna rama por separado.

---

## 6 · Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** Ninguna cifra de este veredicto se lee como "México no tiene autodefensas ni protesta rural" — el hallazgo es sobre **qué mide cada catálogo**, no sobre el fenómeno mexicano. `Autodefensas Unidas de Michoacán` sí existe en el registro; lo que no existe es el dato que conectaría su aparición con el antecedente de agravio y con un universo comparable del otro brazo.

**¿Qué cambiaría con foco rural, indígena o popular?** El caso de protesta rural encontrado en GDELT (n=1, Jalisco/Baja California) apunta en la dirección de que el foco rural SÍ tiene casos de protesta institucional — justo el tipo de caso que, con denominador, cruzaría la predicción de `R7.4`. No se puede escalar de n=1 a ningún veredicto, y se declara en vez de forzarlo.

**¿Qué afirmación describe el estado del corpus y no fue derivada?** Ninguna: las tres fuentes se abrieron completas (no muestreadas, salvo GDELT 2.0 acotado a un día declarado como tal). El desvío de §0 de la spec (inspección de contenido antes de congelar) se declaró ahí y no se repite aquí como si fuera nuevo.

**Corrección propia, declarada:** una nota de registro de este mismo acto en `data/manifiesto.yaml` (payload `adqcorre_r74r75_gdelt2_export_mx_20260824`) y la fila `GDELT` de la cola citaron primero "33" filas para el código 18/19/20 antes de recontar con el propio script y corregir a **26** — ambas fuentes ya llevan la cifra corregida; se declara aquí para que quien audite no encuentre una tercera cifra distinta.

---

**el primer resultado que produjo este procedimiento es el que se reporta.**
