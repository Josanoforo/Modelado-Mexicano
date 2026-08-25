# ACTO ADQ-CORRE-R74R75 — 24/ago/2026

Ejecuta el GO de mesa `FP-124` (`ADR-155`, firma verbatim «F5: GO, para eso creamos una infraestructura robusta…»), sobre `forense/encargos/2026-08-24-ADQ-CORRE-R74R75.md`. Base: `b053491` (`origin/main`, PR #325, `ACTO CAL-G3-PUNTUAL`/`ADR-157`) — sin movimiento durante todo el acto.

## §0 · ARRANQUE

1. **Repo:** clon existente en `/home/pc0/Modelado-Mexicano`; worktree nuevo en `/home/pc0/mm-adq-corre-r74r75`, rama `adq-corre-r74r75` (reutilizada — ya existía apuntando al mismo `b053491`, sin commits propios).
2. **SHA/gate:** el encargo exige "SELLA-AGO24-B fusionado". **Ese acto nunca existió.** `ADR-155`/`FP-124` (24/ago/2026, `ACTO SELLA-AGO24-C-v2`) ya lo había declarado, prospectivamente: *"el gate de `ADQ-CORRE-R74R75` se lee contra este ADR. Su texto original citaba `SELLA-AGO24-B`, y `grep` sobre `.md`/`.tsv` del árbol devuelve cero coincidencias tanto de `SELLA-AGO24-B` como de `ADQ-CORRE-R74R75`"* (`gobernanza:3184`). Re-verificado aquí, mismo resultado (`grep` sobre el árbol completo, cero coincidencias de "SELLA-AGO24-B" fuera de esa propia declaración). El GO real que gatea este acto es `FP-124`, `FIRMADA`, verbatim citado arriba. Gate satisfecho por la vía correcta, no la nombrada por el encargo.
3. **`data/raw`:** symlink nuevo a `/home/pc0/mm-corpus/raw` (318 entradas visibles).
4. **Entorno, firma de tres partes:** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío · `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `200` · `ls data/raw | head -1` → `2005trim1_csv.zip` (no vacío). `pgrep -af claude` sin otra sesión de agente concurrente.

## §1 · PARTE A — tres payloads, no cinco, con un hallazgo de terreno por fuente

Las 5 filas de la cola (líneas 12,14-17) resultaron ser **tres fuentes descargables reales, no cinco**:

- **`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`** (línea 14) y **`MASS_MOBILIZATION_PROTEST_DATA_MEXICO`** (línea 16) **no son fuentes separadas.** `url_conocida` de ambas es `VACIO`. La colección Harvard Dataverse del proyecto (`MMdata`, enlazada desde `massmobilization.github.io`) tiene **un solo dataset** (`doi:10.7910/DVN/HTTWYL`) con dos versiones del mismo archivo global (`mmALL_073120_csv.tab`, `mmALL_073120_v16.tab`) más un manual PDF — ninguno con "Mexico" en nombre o metadato. Verificado además: el sitio del proyecto (4 páginas) sin mención de "Mexico"; `api.github.com/orgs/MassMobilization` → `404`. La propia regla de dedup por sha256 de `tests/manifiesto.py --registra` lo confirmó de la única forma que un script puede: intentar registrar un segundo id para el mismo contenido aborta con el id ya existente.
- **UCDP GED v26.1 ya estaba adquirido** — registrado el 13/ago/2026 por `ACTO GDELT-UCDP-RECON` (`ucdp_ged261_csv`). `tests/manifiesto.py --registra` lo confirmó por la misma vía: mismo sha256 ya presente. **No se re-descargó.**
- **GDELT se intentó dos veces.** La primera (`GDELT.MASTERREDUCEDV2.1979-2013.zip`, el enlace de descarga masiva histórica de `gdeltproject.org/data.html`) resultó, al inspeccionar el contenido real (no la portada), un **agregado diario actor-par-CAMEO sin columna de país** (`Source`/`Target` son códigos CAMEO de 3 letras que mezclan país/región/rol — `AFR`="Africa", no un país), sin texto de artículo, geo casi siempre vacío — inservible para aislar México o clasificar agravio/respuesta. Corregido con un **día UTC completo de GDELT 2.0 real** (`2026-08-24`, 96/96 archivos `.export.CSV.zip`, 6.1 MB, íntegros), filtrado por `ActionGeo_CountryCode=='MX'` — mecanismo ya validado empíricamente por `GDELT-UCDP-RECON` el 13/ago (columna 54, awk-indexado) y reconfirmado aquí sobre datos de hoy: 487 de 97,839 filas.

**Registro** (`tests/manifiesto.py --registra`, una invocación por id, salida cruda en la sesión): `adqcorre_r74r75_gdelt_masterreducedv2`, `adqcorre_r74r75_gdelt2_export_mx_20260824`, `adqcorre_r74r75_massmobilization_mmall_v16`. Ninguna de las tres respuestas negativas (AUSENTE/raíz-no-configurada/hash-discordante) aplicó — las tres descargas fueron reales y nuevas.

**Cola marcada** (`data/cola-adquisicion-2026-08-12.tsv`, columnas `estado_adquisicion_R74R75`/`ids_manifiesto_R74R75` al final, solo las 5 filas; las 50 filas restantes reciben celda vacía para mantener el TSV rectangular — verificado `awk -F'\t' '{print NF}' | sort -u` → `12` uniforme en las 55 líneas).

**Verificación cruzada de corpus compartido (defecto `PR #77`):** los tres archivos nuevos son visibles y con hash idéntico desde `/home/pc0/Modelado-Mexicano/data/raw/` (clon independiente, no este worktree) — `readlink -f data/raw` coincide en ambos (`/home/pc0/mm-corpus/raw`).

**Dos correcciones propias, detectadas y arregladas en la misma sesión, declaradas para que no queden como una tercera cifra distinta:** el conteo de filas `EventRootCode` 18/19/20 de GDELT se citó primero como "33" y se corrigió a **26** (recontado con el propio script); el total global de Mass Mobilization se citó primero como "17,146" (de `wc -l`, que incluye el encabezado) y se corrigió a **17,145** filas de dato. Ambas correcciones ya están aplicadas en `data/manifiesto.yaml` y en la cola.

## §2 · PARTE B — Commit 1 (ficha) y Commit 2 (corrida)

Detalle completo en `forense/hitoD-R7_4-R7_5-especificacion-v1_0.md` (Commit 1) y `forense/hitoD-R7_4-R7_5-veredicto-v1_0.md` (Commit 2). Resumen:

**Commit 1** declara, sin ocultarlo, que este acto es de adquisición real —no de reconocimiento de metadato— y que construir/verificar los tres payloads exigió abrir contenido antes de congelar la spec (§1 de esa ficha lista exactamente qué se vio). Razona por qué eso no contamina el árbol: el Umbral (`≥25%`) y la definición del falsador compartido vienen fijados desde `hitoD-preregistro` v2.4 (`ADR-33`), anteriores a este acto y a cualquier inspección de estos tres payloads.

**Commit 2** corre la tabla Q1-Q4 (universo de casos · forma de respuesta · entorno · conjunción) contra las tres fuentes completas:

| fuente | universo MX | Q2 (forma) | Q3 (entorno) |
|---|---|---|---|
| Mass Mobilization | 153 de 17,145 | 100% protesta por diseño de inclusión; 0% puede ser autodefensa | texto libre de lugar, sin bandera |
| UCDP GED v26.1 | 25,714 de 417,968 | 98.5% narcotráfico cártel-vs-cártel; 1 solo actor nombrado tipo autodefensa | texto libre de lugar, sin bandera |
| GDELT 2.0 (1 día) | 487 de 97,839 | 1 caso de protesta sin corroborar; 0 de 26 candidatos de violencia (inspeccionados uno por uno) relevantes al mecanismo | texto libre de lugar, sin bandera |

**Ninguna fuente construye universo+forma+entorno sobre la misma unidad de caso**, y verificado aparte: este corpus no tiene ningún catálogo rural/urbano en ningún punto de `data/raw` (`ls | grep -iE "rural|urban|localidad|cuaeg|marco.?geo"` → vacío). La razón, en las tres fuentes, es de **diseño de instrumento** (qué relevan por criterio de inclusión), no de dato mexicano faltante — México está sobrerrepresentado en dos de las tres (153 casos en MassMob; 4° país más frecuente en UCDP).

## §3 · Veredicto y Hito D

**`R7.4` → `D`, `R7.5` → `D`**, archivadas por este mismo acto bajo `ADR-55`/`ADR-56` (un `D` es afirmación sobre nuestro instrumental, lo archiva quien lo establece). `C` también se lee cierta (un registro así es concebible con un clasificador de texto y un catálogo geográfico nuevos, ninguno existe hoy) y **`D` manda**, mismo precedente que `R8.1`/`R4.1`/`R4.3`/`R9.1`/`R9.2`. `Hito D`: **16 de 27 → 18 de 27**. Sin fila de tablero nueva para estas dos reglas — no hay propuesta `A`/`B`/`C`/`E` que necesite firma de mesa, las dos cierran directo en `D`.

## §4 · Lo que voltea

**Nada en el motor.** No se toca `milpa/`, ningún tier `[MEDIA-FUERTE]`, ninguna otra de las 25 fichas del pre-registro. Lo que sí voltea es documental: el conteo de Hito D en los 8 sitios marcados `T20:HITO-D` (`README.md:36`, `estado-programa:95,276`, `modelo-decision:65,700,885`, `gobernanza:360,2959`), y un sitio adicional que había quedado **dos versiones atrás sin marcador** (`estado-programa:201`, seguía en "15/16 de 27" pese a que `SELLA-AGO24`/`SELLA-AGO24-C-v2` ya habían movido el contador principal) — hallazgo propio de este acto, repropagado de una sola vez.

## §5 · Nota a mesa

**Cuántas fuentes se pidieron: 5 filas de cola. Cuántas eran reales: 3.** Dos de las cinco (`MASS_MOBILIZATION_DATA_PROJECT_EVENTOS_MEXICO`, `MASS_MOBILIZATION_PROTEST_DATA_MEXICO`) nombran, con `url_conocida` vacío en ambas, un producto que no existe — no es una fuente que resultó inaccesible, es una fuente que nunca fue distinta de su vecina. Vale la pena que quien redacte la próxima cola de adquisición sepa que un nombre con sufijo geográfico en la columna `fuente_canonica` no garantiza que exista un archivo o endpoint con ese recorte ya hecho — este acto tuvo que verificarlo contra la fuente real, no contra el nombre.

**Sobre el gate:** el encargo llegó citando un acto ("SELLA-AGO24-B") que nunca se lanzó — ya lo sabía `ADR-155`, escrito el mismo día por otro acto, antes de que este existiera. El GO de mesa real (`FP-124`) sí estaba firmado y este acto lo ejecutó sin bloquearse, pero el hallazgo importa para quien programe encargos sucesores citando actos por nombre: verificar que el nombre exista en el árbol, no solo que la firma de mesa exista.

**Sobre el veredicto:** `R7.4`/`R7.5` llevaban ocho meses (desde `ADR-33`, v2.4) pre-registradas como "probable `D`" sin que ningún acto anterior intentara de verdad adquirir y correr el falsador. Este acto lo intentó con las tres fuentes reales que la cola nombraba y confirma la probabilidad como hecho medido: ninguna de las tres está diseñada para relevar "respuesta colectiva a agravio, categorizada por entorno y forma" — dos capturan solo una de las dos formas de respuesta (protesta pura / violencia letal pura) y la tercera, GDELT, la que en principio podría cubrir ambas, produjo en un día real 26 candidatos de violencia inspeccionados uno por uno y ninguno relevante. **Lo que desbloquearía la ficha, si mesa quiere encargarlo como acto aparte:** un clasificador de agravio/respuesta sobre el flujo GDELT y un catálogo de localidad→rural/urbano — ninguno de los dos existe en este corpus hoy (`hitoD-R7_4-R7_5-veredicto-v1_0.md §5`).

## §6 · Suite y perímetro respetado

`python3 tests/check.py` → **19 FAIL · 145 WARN**, idéntico al árbol base `b053491` **antes** de este acto (verificado corriendo la suite en un worktree separado sobre ese commit exacto) — cero regresiones netas. `T18`/`T19c`/`T20` (los que este acto toca a propósito) quedan **verdes** tras la propagación completa de `16→18 de 27`.

**Tres FAIL autoinfligidos, encontrados y cerrados dentro del mismo acto — declarados, no ocultados, mismo mecanismo que `ACTO RETRIAGE-4` y `ACTO MARCO-SATURA-CODEX` ya documentaron para sus propios autoinfligidos:**
- **`T02`** — el encargo archivado (`forense/encargos/2026-08-24-ADQ-CORRE-R74R75.md`) y esta nota colisionaban por nombre normalizado. Resuelto con el sufijo `-cierre` en la nota (renombrada a `2026-08-24-adq-corre-r74r75-cierre.md`), mismo patrón que `ADR-135`/`SELLA-MESA-6` y que `feedback_t02_autocolision_encargo_nota` ya tenía documentado.
- **`T15`** — al escribir `ADR-158`, `gobernanza` pasó a 158 ADR únicos y cuatro sitios (`estado:27,103,207`, `gobernanza:2`) seguían citando 157. Recifrados los cuatro; uno de ellos (`estado:207`, frase heredada de `ACTO CAL-G3-PUNTUAL`: *"T15 recifrado a `157 ADR`"*) le faltaba el marcador `{cita-historica}` que el resto de la misma línea ya usa — añadido, sin editar el contenido sustantivo de esa frase ajena.
- **`T25`** — el encargo archivado verbatim trae, en su línea `ORDEN`, *"E-3 espera a este"*: rótulo pelado real, no nuevo — el `Encargo E-3` de `tests/svystat.py` (4/ago/2026, PR #97, ya citado dos veces en `forense/hallazgos.md`) nunca se había censado en `canon/registro-rotulos.tsv`. Censado ahí (nueva fila, HABITANTE adicional del espacio `E`, colisiona en forma bare con `E3-TRIAGE`) y en `_T25_ARCHIVOS_CONOCIDOS` de `tests/check.py` — el texto de dirección no se edita para complacer un test. **Recursión de un nivel, atrapada y cerrada en el mismo acto:** al narrar este mismo hallazgo, este párrafo vuelve a citar `"E-3"` en prosa — `T25` lo marcó una segunda vez, contra esta nota. Esta nota entra también a `_T25_ARCHIVOS_CONOCIDOS`.

Ninguno de los tres era pre-existente: los tres nacieron de escribir este mismo acto y los tres se cerraron antes de declarar la suite verde. Los 19 fallos que sí quedan son pre-existentes y no relacionados (`T09` marcos importados, `T05` glosario, `T02` `curador_registro` — colisión distinta, ya vieja —, `T06` Gini/confianza, `T08` mapas de evidencia, `T11` cuantificador absoluto).

Tocados: `data/manifiesto.yaml` (3 entradas nuevas, `--registra`), `data/cola-adquisicion-2026-08-12.tsv` (2 columnas nuevas, 5 filas), `forense/hitoD-preregistro-v2_0.md` (Nota 33 + bloque append-only, append-only respetado), `forense/hitoD-R7_4-R7_5-especificacion-v1_0.md` y `-veredicto-v1_0.md` (nuevos), `forense/firmas-pendientes.tsv` (`FP-124` recibe `ejecutada_en`), `canon/gobernanza-v1_15.md` (`ADR-158`, candidateado — a re-verificar por quien fusione; y el contador de `:360`/`:2959`), `canon/estado-programa-v1_10.md` (recifrado en 3 sitios), `README.md:36`, `canon/modelo-decision-v4_0.md` (`:65`/`:700`/`:885`), esta nota, `forense/encargos/2026-08-24-ADQ-CORRE-R74R75.md` (archivado, `CONSUMIDO`). Tres archivos nuevos en `data/raw/` (corpus compartido, verificado desde clon independiente), cero escrituras fuera del registro. No se tocó `milpa/`, ni ninguna otra ficha del Hito D, ni `tablero` fuera de la fila `ejecutada_en` de `FP-124`.
