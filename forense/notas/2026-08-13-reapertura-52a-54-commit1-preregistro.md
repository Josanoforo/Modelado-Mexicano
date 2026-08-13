# ACTO REAPERTURA-52A-54 · COMMIT 1 — el universo y el criterio de parada, antes de abrir nada

## 0 · ARRANQUE

**REPO.** `/home/pc0/mm-reapertura-52a-54`, worktree propio (`git worktree add ... origin/main`), no compartido con otro acto. `git log -1` al arrancar → `1e6e6a9 Merge pull request #203 from Josanoforo/alias-p/motor-diag`. El encargo no declaró un SHA base (sin bloque `BASE DECLARADA`); se refrescó y se reporta la diferencia, igual que ABRIR-4 §ARRANQUE.2 enseña a hacer cuando el SHA no está o se movió: **no es PARO**.

**Verificación de origin, no de worktree.** `mm-w-r-tres-encargos` (el worktree donde primero se buscó contexto) estaba desactualizado — su último commit (`45cf9aa`) antecede a los merges de `#200` (APERTURA-ISSP), `#201` (censo-explotación) y `#202` (CAPA3-RECONCILIA), los tres insumos que este acto necesita. Este worktree se creó fresco desde `origin/main` verificado por `git fetch` + `git log origin/main -1`, no desde el estado de un worktree existente.

**ENTORNO.** CAJA con corpus, declarado por el encargo. `data/raw` y `descargas_mx` no traían enlace por defecto en un worktree nuevo — se crearon: `data/raw → /home/pc0/mm-corpus/raw` (mismo destino que el clon principal) y `descargas_mx → /mnt/c/Users/PC0/Descargas MX` (mismo destino que `data/raices.local.yaml` documenta en los worktrees hermanos). `data/raices.local.yaml` (gitignorado) copiado de `mm-w-r-tres-encargos` sin editar.

**ESPEJO.** Ninguna cifra de esta nota viene de espejo alguno del proyecto.

**GATE de `R5.1-D3`, verificado en el mismo arranque.** `ADJ-4` no existe en el repositorio bajo ninguna forma — detalle completo en `forense/encargos/2026-08-13-r5-1-d3.md`. Ese acto queda `VIVO`/bloqueado, no se toca en este PR.

---

## 1 · Las dos necesidades objetivo, con su texto del censo

Copiado verbatim de `forense/censo-estimabilidad-coeficientes-v1_0.md` (filas citadas por el encargo):

| fila | gen | θ | texto del censo |
|---|---|---|---|
| 3 | G2 | `sens_estatus` 0.55 | "Desenlace `dinero.consumo.estatus_mediado_por_credito` sí identificado en ENIGH (`gastotarjetas`/`tarjeta`/`pagotarjet`)... pero **no hay reactivo de `sens_estatus`**: búsqueda cerrada por ADR-54... examen de descriptor de `PR #64` recorrió los cinco instrumentos permitidos del régimen, ninguno sirve; usar el propio `gastotarjetas` de reactivo sería circular" |
| 11 | G4 | `sens_estatus` −0.15 | "Mismo parámetro que la fila 3 — búsqueda de reactivo cerrada (ADR-54)" |
| 4 | G2 | `aversion_riesgo` 0.20 | "Sin desenlace propio identificado... Único candidato de reactivo examinado y descartado: ENIF `P5_23`/`P5_24` mide conocimiento de protección de depósitos IPAB, el moderador que `dinero.ahorro.seguro_deposito_atenua_aversion` (regla de G1, no G2) pone en el SI — no una medida de aversión... Búsqueda cerrada (mismo criterio ADR-52 A)" |
| 6 | G3 | `aversion_riesgo` 0.40 | "Mismo parámetro que la fila 4 — la búsqueda de reactivo de `aversion_riesgo` es única y ya cerrada (ADR-52 A)... no se repite por generador" |

**Frase-criterio del constructo** (`forense/notas/2026-08-04-sens-estatus-examen-descriptor.md` §1, único documento que la fija con esa precisión — se adopta sin cambio):

- **`sens_estatus`**: *"disposición del sujeto a asignar valor a marcadores de estatus, prestigio o imagen social en su propia decisión de consumo o ahorro"*. Tres cosas que se confunden con el parámetro y no lo son: gasto observado en bienes de estatus (es el desenlace, no el reactivo — circular si se usa de C1), percepción de desigualdad/movilidad social (juicio sobre la sociedad, no sensibilidad propia), aspiración/satisfacción con nivel de vida (adyacente, no idéntico).
- **`aversion_riesgo`**: disposición al riesgo, tolerancia a la pérdida o preferencia por certidumbre. No cuenta el conocimiento de mecanismos de protección (p. ej. IPAB) — eso mide un moderador, no la disposición misma (mismo error ya cometido y corregido con `P5_23`/`P5_24`).

---

## 2 · El universo declarado — no son 5 instrumentos

### 2.1 · De dónde sale el número

**Base:** `data/manifiesto.yaml` tiene 554 entradas; 550 traen `archivo`+`sha256` a la vez (verificado, `python3`+`yaml.safe_load`, mismo comando que usó `forense/notas/2026-08-13-censo-explotacion.md` §ARRANQUE). Las 4 restantes no cuentan como payload — ninguna trae uno de los dos campos sin el otro.

**Filtro:** `data/censo-explotacion-2026-08-13.tsv` clasifica esos 550 en cuatro estados mutuamente excluyentes (definición operacional en `forense/notas/2026-08-13-censo-explotacion.md` COMMIT 1, no re-derivada aquí): `EXPLOTADO` (4) · `ABIERTO-SIN-HALLAZGO` (4) · `REFERENCIADO-NO-ABIERTO` (4) · `SIN-DEMANDA` (538).

El encargo pide, en ese orden: `REFERENCIADO-NO-ABIERTO` primero, `SIN-DEMANDA` con diccionario disponible después. `EXPLOTADO`/`ABIERTO-SIN-HALLAZGO` quedan fuera por construcción — son los 4 payloads que `ABRIR-4` ya abrió (ENSAFI/ENFIH/ENASIC/ENBIARE), no universo nuevo.

**"Diccionario disponible" — heurístico declarado, no editorializado.** `SIN-DEMANDA` no distingue microdato crudo de diccionario/cuestionario en su esquema; se aplicó un patrón por nombre de archivo (`_fd_`, `fd.xlsx`, `fd.pdf`, `diccionario`, `cuestionario`, `questionnaire`, `codebook`, `descriptor`, `etiquetas`, `catalog`, `layout`, `glosario`, `ficha técnica`, y variantes) sobre las columnas `archivo`/`id_manifiesto`, verificado contra `re.IGNORECASE` en Python. **Límite declarado:** es un heurístico de nombre, no de contenido — si un archivo marcado no resulta ser realmente abrible como diccionario (p. ej. una página de catálogo sin ítems, no un cuestionario), el COMMIT 2 lo reporta como tal, no lo fuerza a `NO-ENCONTRADO`. Resultado: **100 de los 538 `SIN-DEMANDA`** matchean el patrón.

**104 payloads totales** (4 `REFERENCIADO-NO-ABIERTO` + 100 `SIN-DEMANDA` con diccionario) — **no 5**. El régimen original cubría 5 de 137 instrumentos con payload conocido en 4/ago (`forense/REVERIFICACION-DEMANDA-vs-UNIVERSO-2026-08-07-v1_0.md:74`); este universo cubre 104 de 550 payloads con archivo+sha256 hoy — órdenes de magnitud más grande, y la métrica de conteo cambió (payloads con diccionario, no "instrumentos" en el sentido difuso del cierre original).

### 2.2 · Diligencia de cruce — 10 de los 104 ya están cubiertos, hoy mismo

Sin este cruce, este acto habría re-abierto trabajo hecho en las últimas horas por otros dos actos en `main`. Cruzado contra (a) el propio examen original (`PR #64`, la base literal de ADR-52A/54), (b) los dos actos que cerraron hoy y tocan estas dos necesidades exactas (`APERTURA-ISSP` PR#200, `CENSO-v1.1` PR#198) — **no** un barrido exhaustivo de los cientos de notas de `forense/`, que queda fuera de perímetro declarado:

| id_manifiesto | por qué ya está cubierto |
|---|---|
| `za5900_q_mx` | APERTURA-ISSP (PR#200, 13/ago/2026) ya buscó sens_estatus/aversion_riesgo aquí -- NO-ENCONTRADO ambas (forense/notas/2026-08-13-apertura-issp.md:151-152). Censo-explotacion quedó desactualizado en este payload (su corrida fue anterior al merge de APERTURA-ISSP). |
| `za6980_q_mx` | APERTURA-ISSP (PR#200, 13/ago/2026) ya buscó sens_estatus/aversion_riesgo aquí -- NO-ENCONTRADO ambas (forense/notas/2026-08-13-apertura-issp.md:151-152). Censo-explotacion quedó desactualizado en este payload. |
| `enasem2018_fd_xlsx` | CENSO-v1.1 (PR#198, 13/ago/2026) ya buscó ambas necesidades en las 3 rondas ENASEM -- 0/6,471 variables (forense/censo-estimabilidad-coeficientes-v1_1.md filas 3-4). |
| `enasem2021_fd_xlsx` | CENSO-v1.1 (PR#198, 13/ago/2026) ya buscó ambas necesidades en las 3 rondas ENASEM -- 0/6,471 variables. |
| `enasem2024_fd_xlsx` | CENSO-v1.1 (PR#198, 13/ago/2026) ya buscó ambas necesidades en las 3 rondas ENASEM -- 0/6,471 variables. |
| `encig2021_cuestionario_pdf` | PR #64 ya examinó este cuestionario (ENCIG 2021) -- cero coincidencias. Cierre original ADR-52A/54. |
| `encuci2020_fd_pdf` | PR #64 ya examinó exactamente este archivo (FD_ENCUCI2020.pdf, única edición) -- cero coincidencias; sí encontró y examinó el ítem 4.1 (orgullo de ser mexicano), descartado por constructo distinto. Cierre original ADR-52A/54. |
| `enif2018_cuestionario_pdf` | PR #64 (forense/notas/2026-08-04-sens-estatus-examen-descriptor.md §3) ya examinó este cuestionario completo (ENIF 2018) por barrido de vocabulario -- cero coincidencias de estatus/prestigio/riesgo. Es el cierre ORIGINAL que ADR-52A/54 invoca -- no una búsqueda distinta. |
| `enif2021_cuestionario_pdf` | PR #64 ya examinó este cuestionario completo (ENIF 2021) -- cero coincidencias. Cierre original ADR-52A/54. |
| `enif2024_cuestionario_pdf` | PR #64 ya examinó este cuestionario completo (ENIF 2024) -- cero coincidencias. Cierre original ADR-52A/54. |

Estos 10 payloads **se citan, no se reabren**. `censo-explotación.tsv` quedó desactualizado en 2 de ellos (`za5900_q_mx`, `za6980_q_mx`: su corrida fue anterior al merge de `APERTURA-ISSP`) — declarado aquí, no oculto; el archivo committeado sigue diciendo `REFERENCIADO-NO-ABIERTO` porque nadie volvió a correr el censo, y este acto no lo edita (fuera de su perímetro — `NO ESCRIBE`).

### 2.3 · El universo nuevo — 94 payloads

2 `REFERENCIADO-NO-ABIERTO` (CSES Módulo 5, WVS7 México) + 92 `SIN-DEMANDA` con diccionario. Listado completo, con su estado censal:

| # | estado | id_manifiesto | archivo |
|---|---|---|---|
| 1 | REFERENCIADO-NO-ABIERTO | `cses5_modulo5_2016_2021_cuestionario` | cses5_Questionnaire.txt |
| 2 | REFERENCIADO-NO-ABIERTO | `f00006635_wvs7_questionnaire_mexico_2018_spanish` | F00006635-WVS7_Questionnaire_Mexico_2018_Spanish.pdf |
| 3 | SIN-DEMANDA (diccionario) | `1_vfinal_cuestionario_hogar_ensanut_2024_etiquetas_cuestionarios` | 1 VFINAL Cuestionario Hogar ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf |
| 4 | SIN-DEMANDA (diccionario) | `2_vfinal_cuestionario_nios_0_a_9_ensanut_2024_etiquetas_cuestionarios` | 2 VFINAL Cuestionario nios 0 a 9 ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf |
| 5 | SIN-DEMANDA (diccionario) | `3_vfinal_cuestionario_adolescentes_ensanut_2024_etiquetas_cuestionarios` | 3 VFINAL Cuestionario adolescentes ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf |
| 6 | SIN-DEMANDA (diccionario) | `4_vfinal_cuestionario_adultos_ensanut_2024_etiquetas_cuestionarios` | 4 VFINAL Cuestionario adultos ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf |
| 7 | SIN-DEMANDA (diccionario) | `5_vfinal_cuestionario_utilizadores_ensanut_2024_etiquetas_cuestionarios` | 5 VFINAL Cuestionario utilizadores ENSANUT 2024_ETIQUETAS.Cuestionarios.pdf |
| 8 | SIN-DEMANDA (diccionario) | `conf17_r9_1_ensanut_2018_cuestionario_utilizadores` | R9_1_ENSANUT_utilizadores/ensanut_2018_utilizadores_servicios_salud.pdf |
| 9 | SIN-DEMANDA (diccionario) | `cpv2020_caas_descriptor_bd_xlsx` | Censo2020_CAAS_descriptor_bd.xlsx |
| 10 | SIN-DEMANDA (diccionario) | `cpv2020_ceu_descriptor_bd_xlsx` | Censo2020_CEU_descriptor_bd.xlsx |
| 11 | SIN-DEMANDA (diccionario) | `cpv2020_cuestionario_ampliado_pdf` | Censo2020_cuest_ampliado.pdf |
| 12 | SIN-DEMANDA (diccionario) | `cpv2020_diccionario_cuestionario_ampliado_xlsx` | diccionario_cuestionario_ampliado_cpv2020.xlsx |
| 13 | SIN-DEMANDA (diccionario) | `cpv2020_fd_iter_pdf` | fd_iter_cpv2020.pdf |
| 14 | SIN-DEMANDA (diccionario) | `cses5_modulo5_2016_2021_codebook` | cses5_codebook.zip |
| 15 | SIN-DEMANDA (diccionario) | `eder_2017_eder2017_fd` | eder2017/eder2017_fd.pdf |
| 16 | SIN-DEMANDA (diccionario) | `elcos2012_fd_xls` | elcos2012/elcos_fd.xls |
| 17 | SIN-DEMANDA (diccionario) | `enadid2023_fd_xlsx` | fd_enadid23.xlsx |
| 18 | SIN-DEMANDA (diccionario) | `enadid2023_hogar_cuestionario_pdf` | hogar_enadid23.pdf |
| 19 | SIN-DEMANDA (diccionario) | `enadid2023_mujer_modulo_cuestionario_pdf` | mujer_enadid23.pdf |
| 20 | SIN-DEMANDA (diccionario) | `encig2015_cuestionario_pdf` | encig15_cuestionario.pdf |
| 21 | SIN-DEMANDA (diccionario) | `encig2017_cuestionario_pdf` | encig17_cuestionario.pdf |
| 22 | SIN-DEMANDA (diccionario) | `encig2019_cuestionario_pdf` | encig19_cuestionario.pdf |
| 23 | SIN-DEMANDA (diccionario) | `encig2019_fd_pdf` | encig19_estructura_base_datos.pdf |
| 24 | SIN-DEMANDA (diccionario) | `encig_2011_fd_encig2011` | encig2011/fd_encig2011.pdf |
| 25 | SIN-DEMANDA (diccionario) | `encup_2001_cuestionario_pdf` | encup_2001_cuestionario_pdf.pdf |
| 26 | SIN-DEMANDA (diccionario) | `encup_2003_cuestionario_pdf` | encup_2003_cuestionario_pdf.pdf |
| 27 | SIN-DEMANDA (diccionario) | `encup_2005_cuestionario_pdf` | encup_2005_cuestionario_pdf.pdf |
| 28 | SIN-DEMANDA (diccionario) | `encup_2008_cuestionario_pdf` | encup_2008_cuestionario_pdf.pdf |
| 29 | SIN-DEMANDA (diccionario) | `encup_2012_cuestionario_pdf` | encup_2012_cuestionario_pdf.pdf |
| 30 | SIN-DEMANDA (diccionario) | `endireh2021_fd_pdf` | endireh2021/endireh2021_fd.pdf |
| 31 | SIN-DEMANDA (diccionario) | `endireh_2003_fd_endireh2003` | endireh2003/fd_endireh2003.pdf |
| 32 | SIN-DEMANDA (diccionario) | `endireh_2006_fd_endireh06` | endireh2006/fd_endireh06.xls |
| 33 | SIN-DEMANDA (diccionario) | `endireh_2011_fd_endireh11` | endireh2011/fd_endireh11.xls |
| 34 | SIN-DEMANDA (diccionario) | `endutih2024_fd_xlsx` | endutih2024/fd_endutih2024.xlsx |
| 35 | SIN-DEMANDA (diccionario) | `endutih_2023_fd_endutih2023` | endutih2023/FD_ENDUTIH2023.xlsx |
| 36 | SIN-DEMANDA (diccionario) | `endutih_2025_fd_endutih2025` | endutih2025/fd_endutih2025.xlsx |
| 37 | SIN-DEMANDA (diccionario) | `engasto_2012_engasto12_fd` | engasto2012/engasto12_fd.pdf |
| 38 | SIN-DEMANDA (diccionario) | `enif2018_fd_xlsx` | enif_2018_fd.xlsx |
| 39 | SIN-DEMANDA (diccionario) | `enif2021_fd_zip` | enif_2021_fd_pdf.zip |
| 40 | SIN-DEMANDA (diccionario) | `enif2024_fd_xlsx` | enif_2024_fd.xlsx |
| 41 | SIN-DEMANDA (diccionario) | `enif_2012_fd_enif2012` | fd_enif2012.xlsx |
| 42 | SIN-DEMANDA (diccionario) | `enif_2015_enif_2015_fd` | enif_2015_fd.xlsx |
| 43 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_ampliado_v5_pdf` | c_amp_v5.pdf |
| 44 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_ampliado_v6a_pdf` | c_amp_v6a.pdf |
| 45 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_basico_v5_pdf` | c_bas_v5.pdf |
| 46 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_basico_v7_pdf` | c_bas_v7.pdf |
| 47 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_sociodemografico_v4_pdf` | c_sdem_v4.pdf |
| 48 | SIN-DEMANDA (diccionario) | `enoe_cuestionario_sociodemografico_v5a_pdf` | c_sdem_v5a.pdf |
| 49 | SIN-DEMANDA (diccionario) | `enpol2021_fd_pdf` | enpol2021/fd_enpol2021.pdf |
| 50 | SIN-DEMANDA (diccionario) | `enti2022_fd_pdf` | enti2022/enti_2022_fd.pdf |
| 51 | SIN-DEMANDA (diccionario) | `enut2002_fd_pdf` | enut2002_fd.pdf |
| 52 | SIN-DEMANDA (diccionario) | `enut2009_diccionario_variables_html` | enut2009_diccionario_variables.html |
| 53 | SIN-DEMANDA (diccionario) | `enut2009_fd_pdf` | enut2009_fd.pdf |
| 54 | SIN-DEMANDA (diccionario) | `enut2014_diccionario_variables_html` | enut2014_diccionario_variables.html |
| 55 | SIN-DEMANDA (diccionario) | `enut2014_fd_xls` | enut2014_fd.xls |
| 56 | SIN-DEMANDA (diccionario) | `enut2019_diccionario_variables_html` | enut2019_diccionario_variables.html |
| 57 | SIN-DEMANDA (diccionario) | `enut2019_fd_xlsx` | enut2019_fd.xlsx |
| 58 | SIN-DEMANDA (diccionario) | `enut2024_diccionario_variables_html` | enut2024_diccionario_variables.html |
| 59 | SIN-DEMANDA (diccionario) | `enut2024_fd_xlsx` | enut2024_fd.xlsx |
| 60 | SIN-DEMANDA (diccionario) | `envipe2018_fd_pdf` | fd_envipe2018.pdf |
| 61 | SIN-DEMANDA (diccionario) | `envipe2019_fd_pdf` | fd_envipe2019.pdf |
| 62 | SIN-DEMANDA (diccionario) | `envipe2020_fd_pdf` | fd_envipe2020.pdf |
| 63 | SIN-DEMANDA (diccionario) | `envipe2021_fd_pdf` | fd_envipe2021.pdf |
| 64 | SIN-DEMANDA (diccionario) | `envipe2022_fd_pdf` | fd_envipe2022.pdf |
| 65 | SIN-DEMANDA (diccionario) | `envipe2023_fd_pdf` | fd_envipe2023.pdf |
| 66 | SIN-DEMANDA (diccionario) | `envipe2024_fd_pdf` | fd_envipe2024.pdf |
| 67 | SIN-DEMANDA (diccionario) | `envipe2025_fd_pdf` | fd_envipe2025.pdf |
| 68 | SIN-DEMANDA (diccionario) | `envipe_2011_fd_envipe2011` | envipe2011/fd_envipe2011.xls |
| 69 | SIN-DEMANDA (diccionario) | `envipe_2012_fd_envipe2012` | envipe2012/fd_envipe2012.xls |
| 70 | SIN-DEMANDA (diccionario) | `envipe_2013_fd_envipe2013` | envipe2013/fd_envipe2013.xlsx |
| 71 | SIN-DEMANDA (diccionario) | `envipe_2014_fd_envipe2014` | envipe2014/fd_envipe2014.pdf |
| 72 | SIN-DEMANDA (diccionario) | `envipe_2015_fd_envipe2015` | envipe2015/fd_envipe2015.pdf |
| 73 | SIN-DEMANDA (diccionario) | `envipe_2016_fd_envipe2016` | envipe2016/fd_envipe2016.pdf |
| 74 | SIN-DEMANDA (diccionario) | `envipe_2017_fd_envipe2017` | envipe2017/fd_envipe2017.pdf |
| 75 | SIN-DEMANDA (diccionario) | `indice_de_bienestar_cuestionarios` | Indice de Bienestar.Cuestionarios.docx |
| 76 | SIN-DEMANDA (diccionario) | `inegi_rnm_catalog_330_enaproce2015` | R2.1_R2.2_R10.2_RNM_microdato/inegi_rnm_catalog_330_enaproce2015.html |
| 77 | SIN-DEMANDA (diccionario) | `inegi_rnm_catalog_518_enaproce2018` | R2.1_R2.2_R10.2_RNM_microdato/inegi_rnm_catalog_518_enaproce2018.html |
| 78 | SIN-DEMANDA (diccionario) | `inegi_rnm_search_intento_param` | R2.1_R2.2_R10.2_RNM_microdato/inegi_rnm_catalog_search_intento_search_param.html |
| 79 | SIN-DEMANDA (diccionario) | `lapop_abmex2023_cuestionario_mexico` | lapop_abmex2023_cuestionario.pdf |
| 80 | SIN-DEMANDA (diccionario) | `latinobarometro2024_cuestionario_esp` | latinobarometro2024_cuestionario_esp.pdf |
| 81 | SIN-DEMANDA (diccionario) | `latinobarometro2024_fichas_tecnicas` | latinobarometro2024_fichas_tecnicas.pdf |
| 82 | SIN-DEMANDA (diccionario) | `mmsi_2016_cuestionario` | inegi_mmsi_2016/cuestionario_mmsi_2016.pdf |
| 83 | SIN-DEMANDA (diccionario) | `mociba2024_fd_xlsx` | mociba2024/mociba2024_fd.xlsx |
| 84 | SIN-DEMANDA (diccionario) | `mociba_2015_mociba2015_fd` | mociba2015/mociba2015_fd.xlsx |
| 85 | SIN-DEMANDA (diccionario) | `mociba_2016_mociba2016_fd` | mociba2016/mociba2016_fd.xlsx |
| 86 | SIN-DEMANDA (diccionario) | `mociba_2017_mociba2017_fd` | mociba2017/mociba2017_fd.xlsx |
| 87 | SIN-DEMANDA (diccionario) | `mociba_2019_mociba2019_fd` | mociba2019/mociba2019_fd.xlsx |
| 88 | SIN-DEMANDA (diccionario) | `mociba_2020_mociba2020_fd` | mociba2020/mociba2020_fd.xlsx |
| 89 | SIN-DEMANDA (diccionario) | `mociba_2021_mociba2021_fd` | mociba2021/mociba2021_fd.xlsx |
| 90 | SIN-DEMANDA (diccionario) | `mociba_2022_mociba2022_fd` | mociba2022/mociba2022_fd.xlsx |
| 91 | SIN-DEMANDA (diccionario) | `mociba_2023_mociba2023_fd` | mociba2023/mociba2023_fd.xlsx |
| 92 | SIN-DEMANDA (diccionario) | `mociba_2025_mociba2025_fd` | mociba2025/mociba2025_fd.xlsx |
| 93 | SIN-DEMANDA (diccionario) | `wb2661_asq_questionnaires` | wb2661_ASQ_Questionnaires.zip |
| 94 | SIN-DEMANDA (diccionario) | `za5900_questionnaire_development_report` | ZA5900_questionnaire_development_report.pdf |

**Nota sobre solape declarado, no verificado.** Algunas filas de este universo son ediciones adyacentes de instrumentos que `PR #64` sí examinó pero en un documento distinto (p. ej. `enif2018_fd_xlsx`/`enif2021_fd_xlsx`/`enif2024_fd_xlsx` son la ficha de datos, no el cuestionario que `PR #64` leyó de esas mismas ediciones; `encig2019_fd_pdf` trae "estructura_base_datos" en el nombre pero el año en el id es 2019, no el 2023 que `PR #64` examinó — no se asume que sean el mismo archivo sin abrirlo). Estas filas **se buscan en este acto** — la duda se resuelve abriendo, no asumiendo solape para descartarlas del universo.

---

## 3 · Términos de búsqueda por necesidad

Punto de partida: la unión de los tres actos que ya buscaron estas dos necesidades exactas (`PR #64`, `ABRIR-4` §2, `APERTURA-ISSP` §3.2) — no la lista mínima de un encargo viejo tomada sola. Lección de `ABRIR-4` (`familismo_obligacion`, necesidad distinta pero método aplicable aquí): "obligación" literal dio 0 y el hallazgo real vino de "deber" — los términos se derivan del texto de la necesidad y se amplían con sinónimos, no se copian sin pensar.

**`sens_estatus`** — español: `estatus`, `prestigi(o/oso)`, `aparent(ar/e)`, `ostenta(r/ción)`, `presum(ir/ido)`, `imagen social`, `marca` (reconocida/de lujo), `qué dirán`, `clase social`, `nivel social`, `posición social`, `envidia`, `admirac(ión/iar)`, `comparación social`, `conspicu(o)`, `nivel de vida`, `desigualdad`, `movilidad social`, `aspiraci(ón/onal)`, `lujo`, `moda`, `tendencia`, `impresionar`, `reconocimiento social` — inglés (instrumentos internacionales: CSES, WVS, ISSP dev. report): `status`, `prestige`, `appearance`, `compar(e/ison)`, `neighbors`, `brand`, `esteem`, `conspicuous consumption`, `keeping up`.

**`aversion_riesgo`** — español: `riesgo`, `arriesg(ar/ado/oso)`, `pérdida`, `perder`, `seguro` (como certidumbre, no solo producto), `certidumbre`, `certeza`, `apostar`, `azar`, `lotería`, `prudente`, `cauteloso`, `conservador` (financiero), `tolerancia al riesgo`, `propensión al riesgo`, `especulat(ivo/ión)`, `imprevisto`, `emergencia` — inglés: `risk`, `risk-averse`, `gamble`, `loss`, `uncertain(ty)`, `chance`, `cautious`, `conservative`.

Cada término se reporta en el COMMIT 2 aunque dé cero coincidencias — descartar es entregable (`ABRIR-4` §3, mismo criterio, adoptado sin cambio).

---

## 4 · Criterio de parada

Adoptado del encargo, sin enmienda: **la búsqueda de una necesidad se cierra cuando una pasada completa sobre el universo declarado (104 payloads, §2) no produce candidato nuevo, y ese cierre lleva el universo en la misma línea.** No es la regla de "tres actos nombrados" de ADR-52A — esa contaba actos, no cobertura, y por eso cerró sobre el 0.52%. Este criterio cuenta cobertura: una pasada sobre el universo entero declarado aquí, no sobre una muestra ni sobre los primeros N que rindan algo.

Este acto ejecuta **una** pasada completa (COMMIT 2). Si esa pasada no produce candidato: la búsqueda de `sens_estatus`/`aversion_riesgo` sobre *este* universo declarado se cierra aquí, con el universo citado — no se abre una tercera ronda sin que aparezca universo nuevo (p. ej. una fuente adquirida después de esta fecha) que justifique repetir el criterio.

---

## 5 · Pre-registro de falsación (B-bis)

**Tasa base, medida antes de correr esta pasada:** de los cierres ya hechos sobre estas dos necesidades exactas, ningún candidato ha sobrevivido examen:

- `ABRIR-4` (8/ago): 4 instrumentos × 2 necesidades = 8 celdas → 6 `NO-ENCONTRADO`, 2 `EXISTE-NO-SATISFACE` (ambas descartadas con argumento: `IMPULSIVID`/`GRA_CONTROL` de ENSAFI sin texto de reactivo verificable; batería de tenencia de seguro de ENFIH mide producto, no actitud). Verificado contra `data/abrir4-variables-2026-08-08.tsv` con `csv.reader` (no `awk` — el archivo trae campos con salto de línea embebido que rompe el conteo por línea): 28 filas totales del acto, `Counter` → `{NO-ENCONTRADO: 13, EXISTE-NO-SATISFACE: 11, EXISTE-SATISFACE: 4}`, coincide exacto con el "13 de 28" que cita el encargo.
- `APERTURA-ISSP` (13/ago, hoy): ZA5900 + ZA6980 × 2 necesidades = 4 celdas → 4 `NO-ENCONTRADO`.
- `CENSO-v1.1`/ENASEM (13/ago, hoy): 3 ediciones × 2 necesidades, reportado agregado → 0 candidatos, `0/6,471` variables.
- El régimen original (ENIGH/ENIF/ENCIG/ENCUCI/ENVIPE, `PR #64`): 0 candidatos de 5 instrumentos.

**N=9 instrumentos-edición examinados antes de este acto para estas dos necesidades, 0 candidatos utilizables.** Volver de esta pasada de 104 payloads sin candidato nuevo es la continuación esperada de ese patrón — **no es fracaso del acto ni evidencia de que el criterio de búsqueda esté mal planteado**. El entregable de este acto es que el cierre (si lo hay) lleve el universo completo en la línea, no que aparezca un reactivo.

**Si aparece un candidato:** este acto entrega su texto literal, archivo y página — no lo promueve a θ, no lo declara `EXISTE-SATISFACE` sin verificar que mide el constructo (no el desenlace, no un moderador adyacente — la trampa exacta que ya penalizó a `P5_23` y a `gastotarjetas`). Adjudicar si un candidato cierra la búsqueda formalmente es de mesa, con el hallazgo enfrente — mismo límite que `ABRIR-4` y `APERTURA-ISSP` ya declararon para sí mismos.

---

## 6 · Contaminación declarada (ADR-46(4), conservador)

Esta sesión, antes de este commit, leyó documentos que citan contenido literal de instrumentos — declarado para que quien audite después sepa qué terreno ya se había visto:

- `forense/notas/2026-08-04-sens-estatus-examen-descriptor.md` (íntegro): cita un ítem verbatim de ENCUCI 2020 (4.1, orgullo de ser mexicano) y describe sin citar texto el resultado nulo de ENIGH/ENIF/ENVIPE/ENCIG. Los cinco instrumentos de este documento **no están en el universo nuevo de este acto** (§2.2 — los que se solapan quedan citados, no reabiertos).
- `forense/notas/2026-08-13-apertura-issp.md` (parcial, secciones de arranque/rejilla/resultado, no el detalle variable-por-variable): resultado agregado `NO-ENCONTRADO`/`NO-ENCONTRADO` para ZA5900/ZA6980 en estas dos necesidades. Ambos payloads excluidos del universo nuevo (§2.2).
- `forense/censo-estimabilidad-coeficientes-v1_1.md` (íntegro) y `forense/notas/2026-08-13-censo-explotacion.md` (parcial): documentos de censo/metodología, no contenido de instrumento.
- `data/abrir4-variables-2026-08-08.tsv` (íntegro, vía `csv.reader`): resultados ya públicos del acto anterior, mismo criterio.

**Ningún archivo de los 94 del universo nuevo (§2.3) fue abierto ni su contenido leído antes de este commit** — la exploración de esta sesión se quedó en metadatos (`censo-explotación.tsv`, `manifiesto.yaml`, notas forenses sobre cierres/resultados ya públicos), nunca en el diccionario mismo de ninguno de los 94.

---

## 7 · Qué NO hace este commit

No abre ningún diccionario de los 94 del universo nuevo — eso es COMMIT 2. No escribe `data/reapertura-52a-54-variables-2026-08-13.tsv` — ese archivo nace en COMMIT 2 con datos reales, no como plantilla vacía en este commit. No reabre `ADR-52A` ni `ADR-54` — eso es firma de mesa. No edita `censo-estimabilidad-*.md`, `relaciones.tsv`, ni el manifiesto. No adjudica nada de `R5.1-D3` — ese acto queda aparte, bloqueado (`forense/encargos/2026-08-13-r5-1-d3.md`).
