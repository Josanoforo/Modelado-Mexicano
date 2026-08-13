# ACTO ENLACE-1 · Commit 1 — reglas de correspondencia, congeladas antes de tocar una fila

**Encargo:** `forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md` · **Base:** `origin/main = b17a6f6` (post-#195) · **Entorno:** nube, sin red (declarado, sonda saltada) — ver §5 sobre la limitación de corpus que este entorno concreto expuso.

## §0 · Premisas verificadas (script literal del encargo)

```
$ python3 tools/curador_registro/via_capa2.py | head -4
Filas en relaciones.tsv: 197
Diffs propuestos (capa2_manifiesto): 0
Diagnóstico auxiliar ...: 97

$ awk -F'\t' 'NR>1 && $7=="NO_DETERMINADO"' data/curacion-registro/relaciones.tsv | wc -l
173
$ awk -F'\t' 'NR>1 && $3=="ISSP"' data/curacion-registro/relaciones.tsv | wc -l
14
$ grep -cE "^- id: za(6980|5900|7600)" data/manifiesto.yaml
16
```

Los cuatro coinciden exacto con lo declarado en el encargo. `origin/main` en el momento de redactar este commit: `b17a6f6` (confirmado por `git merge-base --is-ancestor` contra la rama de trabajo).

## §1 · La convención del precedente (derivada del árbol, no inventada)

Las 24 filas `capa2_manifiesto=SI` existentes se leyeron una a una (`id_manifiesto`, `objeto_evidencia_id_canonico`, y su registro correspondiente en `data/curacion-registro/evidencias.tsv`, columnas `variable_reactivo_tabla`/`texto_evidencia`). Las 24 son `tipo_fuente=FUENTE_DATOS`, y se dividen en dos patrones limpios, sin excepción:

- **ENASIC / ENBIARE / ENFIH (18 de 24):** `id_manifiesto` apunta al objeto **FD** (`enasic2022_fd_xlsx`, `enbiare2021_fd_pdf`, `enfih2019_fd_xlsx`). En cada caso, `evidencias.tsv.texto_evidencia` cita el reactivo exacto, numerado, tal como aparece en el cuestionario/descriptor (ej. `6.45.06 ¿Por qué no ha buscado...`; `B2. En caso de que se le presente una urgencia...`; `11.1 Si hoy tuviera una urgencia económica...`). El manifiesto marca esos FD como efectivamente abiertos y leídos (`"descriptor abierto íntegro"`).
- **ENSAFI (6 de 24):** `id_manifiesto` apunta al objeto **BD** (`ensafi2023_bd_csv_zip`). `evidencias.tsv.texto_evidencia` declara explícitamente `[SIN TEXTO DE REACTIVO -- ENSAFI no trae diccionario en este corpus; nombre de columna derivada, hallada por lectura manual del encabezado]` — no existe FD para ENSAFI en el manifiesto; el objeto que evidencia la relación es el que realmente se inspeccionó.

**Regla derivada (la que aplica igual a las ~21, no una nueva):** `id_manifiesto` apunta al objeto del manifiesto que **efectivamente evidencia** la relación — el FD/cuestionario cuando el objeto es un reactivo/variable ya documentado con texto citable; el payload de datos cuando el objeto es el microdato mismo (inspeccionado directamente, sin documento intermedio). En ambos casos, el común denominador es: **el objeto elegido es el que de hecho se abrió/leyó**, no el que "debería" tener la respuesta por tipo de archivo.

`sha256_fuente`: en las 24, el valor es una copia literal del campo `sha256` de la entrada de manifiesto asignada — nunca recalculado, nunca vacío. Se aplica igual aquí.

## §2 · El mapeo módulo↔necesidad de ISSP — las 14 filas, pre-registradas

ISSP tiene tres módulos en el manifiesto: `za6980` (2017 Social Networks and Social Resources, 4 objetos), `za5900` (2012 Family and Changing Gender Roles IV, 10 objetos), `za7600` (2019 Social Inequality V, 2 objetos) — 16 en total.

**Asignación del módulo, por fila, jerarquía MAP-B nivel 1 (URL/cita — no por nombre):** las 14 filas citan, en `evidencia_ref`, líneas de `data/mapa-ext-general-2026-08-06.tsv`, `data/mapa-ext-academico-2026-08-06.tsv` o `data/mapa-fuentes-externas-consolidado-2026-08-06.tsv`. Cada línea citada trae su propia `URL_primaria`/`url_primaria`, y esa URL coincide **exacta** (no por parecido) con el `url_origen` de uno de los tres módulos del manifiesto — cada módulo GESIS tiene DOI y URL de estudio distintos (za6980 doi=10.4232/1.13322; za5900 doi=10.4232/1.12661; za7600 doi=10.4232/1.14009):

| línea citada | URL_primaria | módulo GESIS que la misma URL identifica en el manifiesto |
|---|---|---|
| `mapa-ext-general.tsv:L5` (MAPA-EXT-004) | `.../social-networks/2017` | `za6980` |
| `mapa-ext-general.tsv:L6` (MAPA-EXT-005) | `.../family-and-changing-gender-roles/2012` | `za5900` |
| `mapa-ext-general.tsv:L15` (MAPA-EXT-014) | `.../social-inequality/2019` | `za7600` |
| `mapa-ext-academico.tsv:L8` (ISSP_SOCIAL_NETWORKS_2017_MEXICO) | — nombre de estudio inequívoco | `za6980` |
| `mapa-ext-academico.tsv:L9` (ISSP_FAMILY_2012_MEXICO) | — nombre de estudio inequívoco | `za5900` |
| `mapa-fuentes-consolidado.tsv:L10` (ISSP Social Networks 2017 México) | — | `za6980` |
| `mapa-fuentes-consolidado.tsv:L38` (ISSP Social Inequality V 2019) | — | `za7600` |

(No se citó ninguna línea que apunte a `za5900` vía `mapa-fuentes-consolidado`; la única fila de ese módulo por ese archivo llega vía `mapa-ext-general:L6` y `mapa-ext-academico:L9`, ambas ya listadas.)

**El hallazgo que cambia el resultado: `za7600` (ISSP 2019 Social Inequality) queda EXCLUIDO para las dos filas que lo citan — México está estructuralmente ausente de ese módulo, verificado por el propio manifiesto, no por este acto:** `za7600_v3_0_0_dta` (`usado_para`) declara *"NINGUNA -- Mexico ausente de la muestra... el resto de las 7 necesidades de la cola fueron asignadas al módulo 2017/2012, no a este"*, con la verificación programática citada ahí mismo (`c_alphan`/`country`: 29 países listados, MX/484 nunca aparece, sobre 44,975 filas). El mismo hallazgo aparece independiente en `mapa-ext-general:L15` (*"México no figura en la lista final revisada"*, `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`) y en `mapa-fuentes-consolidado:L38` (idéntica conclusión). Tres fuentes independientes, cero contradicción. Esto no es una lectura discutible del objeto — es ausencia de país verificada por dato real. Las dos filas N3 (`REL-6b71873b3adacde57117ad99`, `REL-796c0458c0c71745f0a6b2a4`) **quedan `NO_DETERMINADO`**, con esa razón en `nota`.

**Asignación del objeto específico dentro de cada módulo (za6980 o za5900):** ninguna de las 14 filas tiene, en `evidencias.tsv`, un reactivo documentado todavía (las 14 traen `tipo_evidencia=MAPA`, `variable_reactivo_tabla=NO_DETERMINADO`, y textos como *"Sin reactivo [N] abierto"* — candidatas de nivel temático del barrido del 6/ago, no verificación de variable). Aplicando la regla de §1 (el objeto que efectivamente se abrió/leyó): dentro de cada módulo, el único objeto documental marcado en el manifiesto como realmente leído y con México verificado en el microdato asociado es el cuestionario aplicado — `za6980_q_mx` (*"Documento leído en esta sesión... Microdato asociado verificado: México presente, N=1002 de 44492"*) y `za5900_q_mx` (mismo patrón, N=1527 de 61754). El resto de los objetos de documentación (`backgroundvar_mx`, `bq`, `cdb`, `mr`, `overview`, `questionnaire_development_report`) están marcados `"No abierto a nivel de contenido en esta sesión"`. Se asigna el cuestionario, no el microdato (`_dta`/`_sav`), porque ningún reactivo específico dentro del microdato se ha identificado todavía para estas 12 filas — apuntar al `.dta` implicaría una lectura de variable que nadie hizo.

**Tabla completa, las 14 filas:**

| relación | necesidad | construct | módulo | `id_manifiesto` asignado |
|---|---|---|---|---|
| `REL-62c97ccb92d0e95c8120d776` | N28 (R8.1) | — débil, ver nota | za6980 | `za6980_q_mx` |
| `REL-72ff714a3ba6d0bab952e05f` | N2 (radio_confianza) | Q7/Q8/Q11 | za6980 | `za6980_q_mx` |
| `REL-75b2ff53a19d8058eba2dbb7` | N13 (familismo_obligación) | — débil, ver nota | za6980 | `za6980_q_mx` |
| `REL-845a93bc24990147a394f897` | N2 (radio_confianza) | Q7/Q8/Q11 | za6980 | `za6980_q_mx` |
| `REL-8d2952203ec3678f3bd0c473` | N30 (R8.3) | puente personal, Q1/Q11 | za6980 | `za6980_q_mx` |
| `REL-9dfab617c356df5594575a3c` | N12 (familismo_apoyo) | Q7/Q8/Q11 | za6980 | `za6980_q_mx` |
| `REL-b034b04e9ba040bd02e39b8b` | N14 (radio_confianza) | Q7/Q8/Q11 | za6980 | `za6980_q_mx` |
| `REL-e95e26820797a0f55c9246d7` | N12 (familismo_apoyo) | Q7/Q8/Q11 | za6980 | `za6980_q_mx` |
| `REL-7751c832c7e30e4e4d7603cc` | N12 (familismo_apoyo) | adyacente | za5900 | `za5900_q_mx` |
| `REL-cd0d1c5fd7e85418603c73cd` | N13 (familismo_obligación) | V27/V35/V36 | za5900 | `za5900_q_mx` |
| `REL-d630dc1ea394364e53631401` | N13 (familismo_obligación) | V27/V35/V36 | za5900 | `za5900_q_mx` |
| `REL-f219eb1a0e1b71beb5a36f6f` | N30 (R8.3) | adyacente | za5900 | `za5900_q_mx` |
| `REL-6b71873b3adacde57117ad99` | N3 (sens_estatus) | — | za7600 | **`NO_DETERMINADO`** — México ausente, ver arriba |
| `REL-796c0458c0c71745f0a6b2a4` | N3 (sens_estatus) | — | za7600 | **`NO_DETERMINADO`** — México ausente, ver arriba |

**Caveat declarado, no resuelto aquí — N28/N13 vía za6980:** el propio manifiesto marca za6980 como *"débil temáticamente"* para N13/N28 (*"sin item de obligación normativa ni de monitoreo+sanción"*). El objeto (`za6980_q_mx`) sigue siendo el único candidato ISSP identificado para esas dos filas — la asignación de `id_manifiesto` (existencia del objeto correcto) es distinta de `clasificacion_relacion` (si el contenido satisface la necesidad), y esta última columna está fuera del perímetro de este acto. Se deja la advertencia en `nota` de ambas filas para que la revisión de `clasificacion_relacion` (fuera de ENLACE-1) la retome.

## §3 · WVS (N5, N15)

Ambas filas citan `mapa-ext-general.tsv:L17` (MAPA-EXT-016), constructo declarado `"G6 deferencia; confianza; familismo; horizonte_temporal"` — coincide exacto con `N5=G3.horizonte_temporal` y `N15=G6.deferencia` (`necesidad-objeto-modelo.tsv`). El manifiesto trae 11 objetos WVS, todos `WVS7 Mexico 2018` (una sola ola, sin ambigüedad de módulo — a diferencia de ISSP). Ningún objeto WVS está marcado como leído a nivel de contenido en esta sesión (a diferencia de `za6980_q_mx`/`za5900_q_mx`); las notas describen el mecanismo de descarga, no verificación de variable. Mismo criterio que ISSP: se asigna el cuestionario aplicado en español, el objeto documental más directo y el que el propio manifiesto etiqueta explícitamente `"doc. N5/N15"` — `f00006635_wvs7_questionnaire_mexico_2018_spanish` — para ambas filas.

| relación | necesidad | `id_manifiesto` asignado |
|---|---|---|
| `REL-3d6a985a8dafc13fdbd39e4a` | N5 (horizonte_temporal) | `f00006635_wvs7_questionnaire_mexico_2018_spanish` |
| `REL-57df012cdba3e281563c1068` | N15 (deferencia) | `f00006635_wvs7_questionnaire_mexico_2018_spanish` |

## §4 · CSES (N17, N25, N26×2, N27)

Las 5 filas citan `mapa-ext-general.tsv:L7` (MAPA-EXT-006) o `mapa-fuentes-externas-consolidado.tsv:L12`, ambas identifican, por URL/DOI (`cses.org`, DOI `10.7804/cses.module5.2023-07-25`), el mismo estudio único que el manifiesto trae en 3 objetos (`cses5_modulo5_2016_2021_csv`, `_codebook`, `_cuestionario`) — sin ambigüedad de módulo. Ninguna de las 5 filas tiene reactivo documentado (`evidencias.tsv`: *"Solo existe ficha/indexación"*, *"INDEXADO-NO-DESCARGADO"*). El propio manifiesto declara, para el CSV, que *"cobertura de México NO verificada en esta sesión (no se abre a nivel variable, prohibido por ese acto)"* — a diferencia de `za7600`, esto es una verificación **no realizada**, no una ausencia **confirmada**: México 2018 es, por diseño del estudio (CSES Módulo 5 es por definición un post-electoral por país, y "México 2018" es el nombre mismo del caso, corroborado independientemente por ambas líneas del barrido), parte declarada del universo CSES. Se deja constancia de la verificación pendiente en `nota` de cada fila. Mismo criterio de objeto que ISSP/WVS: se asigna el cuestionario — `cses5_modulo5_2016_2021_cuestionario`.

| relación | necesidad | `id_manifiesto` asignado |
|---|---|---|
| `REL-02b8ee6d0e13dfb6dc7d3331` | N27 (R7.4/R7.5) | `cses5_modulo5_2016_2021_cuestionario` |
| `REL-162b116abdb2212886430f08` | N25 (R7.1) | `cses5_modulo5_2016_2021_cuestionario` |
| `REL-48285fd8e0a22a38147245ed` | N17 (ver caveat) | `cses5_modulo5_2016_2021_cuestionario` |
| `REL-c0ffdbcc616f342880df820a` | N26 (R7.3) | `cses5_modulo5_2016_2021_cuestionario` |
| `REL-ee1e829631a8bb7de93bcfd3` | N26 (R7.3) | `cses5_modulo5_2016_2021_cuestionario` |

**Observación declarada, no resuelta aquí — anomalía de catálogo en N17:** `necesidad-objeto-modelo.tsv` define `N17` como `tramite.gobierno_digital.{coercitivo,util_sin_coercion}` (trámite de gobierno digital), pero las 14 filas de `relaciones.tsv` con `necesidad_id=N17` cubren un conjunto temático incoherente con esa definición (GDELT, ACLED, UCDP, Mass Mobilization, CSES, ENFIH, ENSAFI, GPS, un experimento de polarización) — ninguna es sobre trámites de gobierno digital. Contraste: N25/N26/N27 (mismo archivo, mismo formato de definición) SÍ cohieren limpio con su propia definición R7.x y con las fuentes que efectivamente los sirven. Esto huele a un desalineamiento de catálogo N-id entre sub-programas (el `G1-G6` financiero, el `R7-R8` cívico-electoral, y el `tramite.*` de gobierno digital pueden haber numerado independientemente y colisionado en `N17`). No es competencia de ENLACE-1 resolverlo — el perímetro de este acto es fuente↔manifiesto, no la validez del `necesidad_id` ya escrito en la fila — pero la correspondencia fuente↔manifiesto para la fila CSES/N17 (`REL-48285fd8e0a22a38147245ed`) es sólida por sí sola (URL/DOI exacto), independiente de si "N17" está bien nombrado. Se declara para que quien mantenga el catálogo de necesidades lo revise.

## §5 · La cuestión de los pares — declarada, no resuelta (punto 3 del encargo)

El precedente ENSAFI/ENFIH (ej. N3: 2 filas `SI` + 2 filas `NO_DETERMINADO`, mismo `necesidad_id`, distinto `objeto_evidencia_id_canonico`, ambas fuentes con ficha real) confirma que varias filas por necesidad, con destinos distintos, es un patrón ya vigente en el archivo — no una anomalía que este acto introduzca. Este acto produce una variante: varias filas por necesidad **que sí se resuelven todas** (N12: 3 filas, 2→za6980 + 1→za5900; N13: 3 filas, 1→za6980 + 2→za5900; N2: 2→za6980; N26: 2→CSES) — no queda ninguna mitad-resuelta porque, a diferencia de ENSAFI/ENFIH, las 12 filas asignables comparten el mismo nivel de evidencia (URL/cita de módulo confirmada, ningún reactivo específico pinpointeado) — no había base para resolver unas sí y otras no arbitrariamente. Se sigue el precedente al pie de la letra: cada objeto conserva su propia fila, cada fila su propia evidencia — no se fusionan. La política general de cuándo cerrar vs. dejar abierto un par sigue siendo decisión de ENLACE-2/mesa, según el propio encargo.

## §6 · `sha256_fuente` — valores a copiar (regla de §1, aplicada)

| `id_manifiesto` | `sha256_fuente` a copiar |
|---|---|
| `za6980_q_mx` | `61bc0c80415521965ec1b2546fbe3b2400cfacb2e6b0b542583304821544f2ed` |
| `za5900_q_mx` | `d8fe53baeb29455b8ec9aa772a63eae4eb8308456aa1e1986d2c96b5067e5375` |
| `f00006635_wvs7_questionnaire_mexico_2018_spanish` | `d84607c68d30985f537a18048c5c903b2f5b73e57420f37689ab67758bac387d` |
| `cses5_modulo5_2016_2021_cuestionario` | `d4deba9a038639871db1625158ef437fe476a3f8b2a0edc5a8041347528abc6c` |

Total del alcance: **21 filas** (14 ISSP + 2 WVS + 5 CSES) — **19 con asignación**, **2 `NO_DETERMINADO`** (N3×2, ambas por ausencia de México en `za7600`, verificada por dato real).

## §7 · Bloqueo verificado para Commit 2 — el corpus no está montado en este entorno

`data/raw/` y `data/raices.local.yaml` están en `.gitignore` (líneas 5-6) y **no existen en este checkout** — confirmado por búsqueda de sistema de archivos completa (`find / -iname "ZA6980_q_mx.pdf"` → 0 resultados). Los payloads de ISSP/WVS se bajaron manualmente por el usuario en su navegador (`descargado_por: usuario, vía navegador`, manifiesto) — viven en el disco local del usuario, no en este contenedor de nube efímero. El propio ARRANQUE del encargo lo anticipa: *"la verificación de payload la hace la vía contra disco — SÍ necesitas el corpus montado"*.

Consecuencia mecánica (`tools/curador_registro/via_capa2.py:verificar_entrada`): sin `raices.local.yaml`, cualquier entrada con `raiz: descargas_mx` (todas las de este acto) resuelve a `RAIZ_NO_CONFIGURADA`, nunca a `COINCIDE` — la vía no puede promover ninguna fila a `SI` en este entorno, sea cual sea el `id_manifiesto` escrito. Esto no es una falla de la asignación semántica anterior (§1-§6); es una limitación de dónde puede ejecutarse la verificación de disco.

Este commit congela la asignación completa y verificable por lectura (§1-§6). **Commit 2 (escritura en `relaciones.tsv` + corrida de la vía + `--escribe` + suite) queda pendiente de un entorno con el corpus montado** — reportado a mesa/usuario junto con este commit, no ejecutado a ciegas.

**La frase:** el primer resultado que produjo este procedimiento es el que se reporta.

---

## §8 · Commit 2 — ejecución y resultados (entorno LOCAL, corpus montado)

**Entorno:** LOCAL (Ubuntu, Claude CLI), worktree `~/mm-enlace1-commit2` sobre `claude/new-session-s98494`, `HEAD=afd9661` (Commit 1) al arrancar, `b17a6f6`=`origin/main` confirmado ancestro.

**Premisas re-verificadas** (mismas de §0, mismo checkout): `197` filas / `0` diffs / `97` diagnóstico auxiliar, `173` `NO_DETERMINADO`, `14` filas ISSP, `16` entradas za-módulo — las cuatro coinciden exacto. La comprobación de corpus en disco (`ZA6980_q_mx.pdf`) inicialmente dio "NO encontrado" porque `yq` no está instalado en este entorno (el `find` cayó a `/nonexistent`) — no por ausencia real del corpus. Verificado en su lugar con `sha256sum` directo: los 4 archivos fuente (`ZA6980_q_mx.pdf`, `ZA5900_q_mx.pdf`, `F00006635-WVS7_Questionnaire_Mexico_2018_Spanish.pdf` bajo `descargas_mx`; `cses5_Questionnaire.txt` bajo `data_raw`/`mm-corpus`) existen en disco y su sha256 real coincide, byte a byte, con `data/manifiesto.yaml` y con la tabla congelada de §6. Ningún mapeo resultó contradicho — no hizo falta un tercer commit de corrección.

**Verificación adicional, no pedida por el encargo pero motivada por el historial real de la rama:** `git log` expone ACTO R-RETRACCIÓN (`764b6bf`), que formaliza el retiro de un registro ISSP/ZA6980 incompatible de ACTO R (PR #190, `ddecf23`, id `za6980_issp2017sn_cuestionario_mx_pdf`), superado por ACTO R″ (PR #193, ya fusionado en `main`). Confirmado antes de escribir: `za6980_q_mx`/`za5900_q_mx` (los ids que usa este acto) son el registro vigente post-retracción — mismo PDF/sha256 que el id retirado, según la propia nota de retracción — no un remanente. `grep -c issp2017sn data/manifiesto.yaml` = `0`; `554` entradas totales; `0` duplicados por `sha256` — re-verificado igual que en el cierre de ACTO R-RETRACCIÓN, sin cambio.

**Escritura:** las 19 filas de §6 escritas exactamente como estaba especificado (`id_manifiesto` + `sha256_fuente`, edición por líneas preservando el TSV, sin `csv.writer` propio). Caveats de §2/§4 (za6980 "débil temáticamente" en N13/N28; cobertura de México no verificada en CSES; anomalía de catálogo N17) escritos en `nota` de las filas correspondientes — no estaban ya presentes pese a la expectativa de la nota de arranque de Commit 2 ("ya debería, por Commit 1"): Commit 1 fue estrictamente de lectura y no tocó `relaciones.tsv`. Las 2 filas N3 (za7600) recibieron el mismo enriquecimiento de `nota`; `id_manifiesto` sin tocar.

**Corrida de la vía:**
```
$ python3 tools/curador_registro/via_capa2.py        # antes de escribir
Diffs propuestos (capa2_manifiesto): 19               # exactamente las 19 filas de §6, todas estado=COINCIDE
$ python3 tools/curador_registro/via_capa2.py --escribe
19 filas escritas en relaciones.tsv.
$ python3 tools/curador_registro/via_capa2.py         # después de escribir
Diffs propuestos (capa2_manifiesto): 0
```
`via_capa2.py --escribe` reescribe el archivo completo vía `csv.DictWriter`; verificado que las 178 filas no tocadas quedaron byte-idénticas (`git diff --numstat` = 21/21 líneas, exactamente las filas de este acto).

**Contador: capa2 `SI`: 24 → 43. Diagnóstico auxiliar: 97 → 78** (78 = 97 − 19: las 19 filas resueltas salen del pool de candidatas a revisión).

**`tests/check.py --baseline`: ROJO, no VERDE — 22 FAIL · 105 WARN, 4 entradas nuevas contra `tests/baseline.json` (HEAD congelado `e7cd99d`).** Verificado con `git stash` de los cambios de este commit que el ROJO es idéntico con y sin ellos — preexistente a Commit 2, no introducido aquí:
- 1/4 (T03): `forense/encargos/2026-08-13-enlace1-mapeo-id-manifiesto.md` (añadido por Commit 1, `afd9661`) cita en prosa `PLANENLACECAPA220260813.md` — el documento que subió el usuario para lanzar el encargo, nunca un archivo del repo. Falso positivo del escáner de referencias colgantes de T03, no una cita rota real.
- 3/4 (T16): `canon/estado-programa-v1_10.md` y `canon/gobernanza-v1_15.md` declaran conteos WARN desactualizados (101, 95) frente al real 105 — deriva ajena a este acto, no relacionada con `relaciones.tsv` ni con ISSP/WVS/CSES.

No corregido aquí: el archivo que dispara T03 es de Commit 1, ya empujado — corregirlo excede el perímetro declarado de Commit 2 y no es "la verificación de disco contradice el mapeo" (la única condición que autoriza tocar el resultado de Commit 1). Los documentos `canon/` son de competencia de mesa, no de la sesión ejecutora. Declarado en `forense/hallazgos.md`, no investigado más allá de fijar la causa.

`tests/test_celdas_d.py` (ejecutado directo — `pytest` no está instalado en este entorno, `python3 tests/test_celdas_d.py` corre el mismo `main()`): 2/2 archivos válidos contra el contrato v0.3 §3, sin relación con este acto.

**La frase (Commit 2):** el primer resultado que produjo esta corrida es el que se reporta — 19/19 filas escritas sin contradicción de disco, 0 pares o candidatas adicionales resueltos más allá del alcance congelado en §6.
