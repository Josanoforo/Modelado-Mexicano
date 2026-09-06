# COMMIT-1 · `MAESTRA38-A2-bis` — reconciliación de las dos definiciones de "sin registro"

**Universo y comando.** Dos raíces del universo de `prereg-caja-S1-A2` (`data_raw`, `descargas_mx`; `downloads` fuera): `python3 tests/corpus.py` corrido con sandbox deshabilitado (`descargas_mx` resuelve a `/mnt/c/Users/PC0/Descargas MX`, fuera del árbol permitido de lectura del sandbox por defecto — sin deshabilitarlo, `C1` da 0/0 para `descargas_mx` y `C3` da 315 `AUSENTE` falsos, porque el proceso no puede leer la carpeta, no porque falte el archivo). Con sandbox deshabilitado: `manifiesto: 1281 entradas` · `C1=185` (`data_raw`: 0 presente_bajo_otra_raiz + 37 sin_registro · `descargas_mx`: 73 presente_bajo_otra_raiz + 33 sin_registro · `downloads` (fuera de universo, sólo cuenta): 1 + 41) · `C2=0` · `C3=0`. Cifras idénticas a `forense/censo-raiz/2026-09-04.txt` — sin discrepancia nueva contra el censo del 4/sep.

**Sello.** `python3 tests/corpus.py` (con sandbox deshabilitado para leer `descargas_mx` bajo `/mnt/c`), 1281 entradas de manifiesto examinadas, C1=185/C2=0/C3=0 — el primer resultado que produce este procedimiento es el que se reporta.

## `descargas_mx` — reconciliación de los 33 "sin_registro"

Script dedicado (`tests/corpus.py` `c1_huerfanos()`/`_indice_por_sha_y_raiz()`, sin reinventar la clasificación): por cada uno de los 33, se hashea el archivo real y se busca ese sha256 en el manifiesto completo (1276 entradas con payload).

| clasificación | n | regla |
|---|---|---|
| **B — copia (n) byte-idéntica** | 32 | sha256 coincide con una entrada YA declarada `raiz: descargas_mx` bajo OTRO nombre de archivo (mismo patrón `(N)`/nombre alterno de la misma descarga: `DecAnuaTipCon (1).xls`, `ICPSR35024-...tabulados... (1..4).csv`, `LEEME-... (1..4).txt`, `icpsr35024-...crosstabs-derivadas (1..3).csv`, `ZA5900_cdb (1).pdf`, `ZA6980_q_mx (1).pdf`, y 9 archivos `ENSANUT2024-v2026-09-01/*` / `adultos_ensanut2024_w.*`/`hogar_ensanut2024_w_icb.stata...`/`integrantes_ensanut2024_w_icb.stata...`/`nse_*.stata...` que son la misma copia de la corrida `v2026-09-01` ya registrada con otro nombre de ruta). Excluido del conteo de candidatas nuevas per §3 de la spec — se anota, no se borra. |
| **A real — sin sha en manifiesto** | 1 | `descargas.php`: página guardada del portal (`EXTENSIONES_PAGINA`), no es dato — mismo hallazgo que el censo del 4/sep, no se promueve por diseño. |

Ningún archivo de los 33 cae en "sha registrado bajo `data_raw` sin raíz declarada" (ese patrón es el de los 73 `presente_bajo_otra_raiz`, abajo, no el de los 33 `sin_registro`). **0 candidatas nuevas reales de `descargas_mx`** — los 33 se explican en su totalidad: 32 copias + 1 página.

## `descargas_mx` — los 73 "presente_bajo_otra_raiz" (residuo categoría C, FP-308)

Los 73 son, sin excepción, archivos cuyo sha256 coincide con una entrada YA registrada bajo `raiz: data_raw` (verificado archivo por archivo: `AGS_PEL_2016.zip`→`sicee_local_ags_pel_2016_zip`, `WBES_Mexico2023_Data.zip`→`wbes_mexico_2023_microdato_dta_zip`, `35024-0001-Codebook-spanish.pdf.zip`→`icpsr35024_mexico_panel_study_2012_codebook_es_zip`, etc. — lista completa en la salida cruda archivada junto a este acto). Es decir: **el mismo archivo vive físicamente en las dos raíces** (`data_raw` y `descargas_mx`), el manifiesto sólo declara una. Clasificación per §4 de la spec: categoría **C**, "raíz declarada ≠ raíz física real" — pero la razón real no es un error de captura, es coexistencia física genuina (la mesa copió/descargó el mismo payload en las dos carpetas).

**Firma FP-308 (iii), ejecutada aquí:** *"coexistencia deliberada; no se recifra raíz en ninguna de las 73"*. Consecuencia declarada: **ninguna de las 73 entradas de `data/manifiesto.yaml` cambia su campo `raiz`** en este acto. Las dos rutas físicas coexisten, ninguna se borra. `FP-308` pasa de `ABIERTA` a `FIRMADA (iii)` en `forense/firmas-pendientes.tsv` (hecho en `P0`).

## `data_raw` — reconciliación de los 37 "sin_registro" (34 en staging + 3 a explicar)

| clasificación | n | detalle |
|---|---|---|
| **A real — sin sha en manifiesto (candidatas nuevas)** | 34 | Grupo 1 `ennvih/doc/*.pdf` (24) · Grupo 2 `enaproce2018/*.zip` (4) + `DescargaMasivaOD_582026_171540_NACIONAL_7930url.xml` (1) · Grupo 3 `ADQ15_ENAFIN_2024_RNM_INEGI/*.html.2a` (3) + `ADQ15_JPAL_.../jpal_evaluacion_landing.html.2a` (1) + `ADQ15_VotarEntreBalas_DataCivica/votar_entre_balas_base.zip.2a` (1) = 24+4+1+3+1+1 = 34. Coincide exactamente con las 34 entradas ya preservadas en `data/manifiesto-staging.yaml` (A2, 4/sep) — sin novedad, mismo universo. |
| **B — copia byte-idéntica ya registrada bajo `data_raw`** | 3 | `ADQ15_OMCA_conflictos_agua/omca_consulta.html.2a` → sha ya registrado como `adq15_omca_omca_consulta` (mismo contenido, ruta `.2a` alterna) · `eder2025/889463930242.pdf` → sha ya registrado como `eder2025_descripcion_bd_pdf` · `ennvih_diseno/calculo-de-factores-de-expansion.pdf` → sha ya registrado como `ennvih3_2009_factores_exp`. Los tres son "3 a explicar" del encargo: duplicado de contenido dentro de la MISMA raíz (no cruza raíces, por eso `c1_huerfanos()` los reporta `sin_registro` con anotación `sin_registro_pero_duplica_contenido_de(<id>)`, no `presente_bajo_otra_raiz`) — excluidos del conteo de candidatas nuevas, no se promueven (ya hay una entrada con ese contenido). |

**0 residuo C dudoso adicional** en `data_raw` (su C1 `presente_bajo_otra_raiz` da 0 — verificado arriba). El único residuo C de este acto son los 73 de `descargas_mx`, ya firmados (FP-308 iii).

## Tabla nominal de los seis depósitos — re-verificado hoy (5/sep/2026)

`find` dedicado sobre las dos raíces reales de esta máquina (sandbox deshabilitado para alcanzar `/mnt/c/Users/PC0/Descargas MX`):

| pieza | resultado 5/sep | comando |
|---|---|---|
| ICPSR `.dta` (`ICPSR_35024/35024-0001-Data.dta`) | **AUSENTE-EN-RAIZ** — `ICPSR_35024/` existe (con `ICPSR_35024-V1.zip` ya registrado), 0 `.dta` nuevos | `find "descargas_mx" -iname "*ICPSR_35024*"` |
| WB 6667 (`ADQ15_WB6667_.../<microdato>.dta`) | **AUSENTE-EN-RAIZ** — carpeta no existe | `find "descargas_mx" -iname "*WB6667*" -o -iname "*Tutores*"` |
| PDN S1 (`PDN_S1v2.zip`) | **AUSENTE-EN-RAIZ** — sólo `PDN_S3v2.zip` presente | `find "descargas_mx" -iname "PDN_S*"` |
| PDN S2 (`PDN_S2v2.zip`) | **AUSENTE-EN-RAIZ** | ídem |
| PDN S6 (`PDN_S6v2.zip`) | **AUSENTE-EN-RAIZ** | ídem |
| ENFIH-4 (`enfih2019/enfih_2019_base_de_datos_csv.zip`) | **AUSENTE-EN-RAIZ** en ambas raíces | `find data/raw "descargas_mx" -iname "*enfih*"` — 0 coincidencias |

**Los seis depósitos siguen AUSENTE-EN-RAIZ, sin cambio contra `forense/censo-raiz/2026-09-04.txt`.** Condición del encargo para COMMIT-3 ("sólo si los seis depósitos aparecieron") **no se cumple** — COMMIT-3 no se ejecuta en este acto. `FP-288` (ENFIH, reserva de las 4 filas `relaciones.tsv`) permanece **ABIERTA**: no hay nada nuevo que decida la reserva, la razón declarada en el tablero sigue vigente.

**El primer resultado que produce este procedimiento es el que se reporta.**
