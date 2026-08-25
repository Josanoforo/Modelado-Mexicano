# ACTO RECENSO-DISEÑO-2 — re-derivación de FP-117 y alta de llaves

**Fecha:** 2026-08-24 · **Entorno:** UBUNTU (corpus + `descargas_mx` montados) · **Sucesor de:** `FP-120` (mesa, `SELLA-AGO24-D` respuesta 6, "damos de alta TODO") · **ADR de este acto:** `ADR-153` · **Cierra:** `FP-117`, `FP-120` · **Abre:** `FP-123`

---

## 0 · Arranque

`data/raw` ya venía symlinkeado a `/home/pc0/mm-corpus/raw` (318 entradas). `data/raices.local.yaml` (gitignorado) NO venía en el worktree — se copió de `/home/pc0/Modelado-Mexicano/data/raices.local.yaml` (mismo modo de falla que documentan RECENSO-DISEÑO-14 y otros actos anteriores), lo que hizo legible `descargas_mx` (`/mnt/c/Users/PC0/Descargas MX`, 70 archivos) y confirmó `python3 tests/manifiesto.py --verifica`: `data_raw: coincide=678 · no_coincide=1 · ausente=0`; `descargas_mx: coincide=106 · no_coincide=0 · ausente=0`. El único `NO COINCIDE` (`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf`) es el defecto preexistente ya documentado, ajeno a este acto.

## 1 · Re-derivación de la lista (37 originales vs. lista real)

`FP-117` cifró la cobertura retroactiva en **37 llaves con payload material sin fila**, mediante un barrido léxico. Este acto repitió el cruce con `yaml.safe_load` sobre `data/manifiesto.yaml` (789 entradas) contra `data/diseno-muestral.yaml` (43 filas), agrupando por slug `/programas/<slug>/` de `url_origen` para INEGI y por host para el resto (mismo método que RECENSO-DISEÑO-14/`ADR-149` usó para derivar el universo de 18 `PENDIENTE`).

**Resultado: 13 llaves reales, no 37.** La discrepancia se explica así:

| Categoría | Cuenta | Detalle |
|---|---|---|
| INEGI, llave real sin fila | 5 | `engasto` (46 payloads), `enestyc` (15), `enafin` (3), `mmsi` (2), `encoap` (1) — coincide con lo que ya traía FP-117 |
| No-INEGI, llave real sin fila | 8 | WVS7 (11), ISSP 2017/ZA6980 (9), CSES Módulo 5 (3), GPS (5+3), Banco Mundial cat. 2661 (62 vía `microdata.worldbank.org`), Pew 2025 (2), OSF "Interacting as Equals" (10), openicpsr Compartamos AEJ (2) |
| Duplicado — ya cubierto por fila existente con otro nombre | 2 | `ensanut.insp.mx` (24 payloads) → misma fila `ENSANUT (2024)`; `www.vanderbilt.edu` (18 payloads) → mismo `fuente:` LAPOP/AmericasBarometer (ver §4) |
| Host administrativo/documental, no es una encuesta nombrada | ~13 | `banxico.org.mx`, `datosabiertos.cnbv.gob.mx`, `data.gdeltproject.org`, `omca.imta.gob.mx`, `fomentocivico.segob.gob.mx`, `repodatos.atdt.gob.mx`, `ift.org.mx`, `pragmatics.indiana.edu`, `ucdp.uu.se`, `dataverse.harvard.edu` (Mass Mobilization), `votarentrebalas.datacivica.org`, `gob.mx`, `datos.gob.mx` |

**Por qué no son "llaves" los ~13 hosts administrativos.** Se inspeccionó el campo `usado_para` de una muestra de cada host (ver script de derivación) — son páginas institucionales (SPEI/CoDi de Banxico), estadística agregada ya publicada (Ahorro Financiero de CNBV), datos de eventos (GDELT, UCDP GED, Mass Mobilization Data Project, votar-entre-balas), corpus lingüístico (Indiana), reportes PDF puntuales (IFT), o documentos de soporte de encargos distintos (`ADQ-15` palancas, `R1.1`/`R7.3` de `CONF-17`) — ninguno es una encuesta/estudio nombrado con su propia unidad de observación y diseño muestral propio. Un host con payload no es automáticamente una "llave" de este censo: **decisión de diseño de este acto**, análoga a por qué `NO_APLICA_REGISTRO_ADMINISTRATIVO` ya distinguía "censo/registro" de "encuesta sin diseño publicado" — aquí la distinción es "encuesta nombrada" vs. "documento de soporte sin identidad de fuente propia".

**Conclusión de gobernanza:** la lista re-derivada (13) MANDA sobre la cifra congelada de `FP-117` (37), tal como ordena el encargo. `FP-117` y `FP-120` se marcan `ejecutada_en: 2026-08-24` en `forense/firmas-pendientes.tsv`.

## 2 · Tabla resumen (las 13 altas)

| # | Fuente | Estado | Ponderador | Estrato | UPM | Qué falta si falta |
|---|---|---|---|---|---|---|
| 1 | ENGASTO 2012-2013 | **MAPEADO** | `FACTOR_VIV` / `factor_hog` | `EST_DIS` | `UPM` | — |
| 2 | ENESTYC 1992-2005 | PENDIENTE | — | — | — | Los 15 payloads son bases de "ejemplo" de 10 registros (confirmado con `tests/dbfmini.py`, 8 tablas × 10 filas en la edición 2005), no el microdato real |
| 3 | ENAFIN 2024 | PENDIENTE | — | — | — | El DDI describe el diseño en prosa (estratificado por tamaño de empresa, sin UPM), pero el único payload de microdato descargado es un tabulado agregado, no caso individual |
| 4 | MMSI 2016 | PENDIENTE | — | — | — | Solo manual del entrevistador y cuestionario en el corpus; sin archivo de datos ni FD (negativo con control positivo: 2 PDF, 0 aciertos de diseño, 12 aciertos de control) |
| 5 | ENCOAP 2023 | PENDIENTE | `FAC_VIV`/`FAC_SEL` (confirmado en microdato) | `EST_DIS` (confirmado) | `UPM_DIS` (confirmado) | Sin FD/diccionario en el corpus que defina esas columnas — mismo patrón que ENSAFI/ENSU en RECENSO-DISEÑO-14 |
| 6 | WVS7 México 2018 | **MAPEADO** | `W_WEIGHT` | `H_URBRURAL` | `I_PSU` | — |
| 7 | ISSP 2017/ZA6980 | SIN_DISEÑO_PUBLICADO | `WEIGHT` | ✗ no publicado | ✗ no publicado | ISSP publica ponderador de post-estratificación, no PSU/estrato para el módulo México |
| 8 | CSES Módulo 5 (Méx. 2018) | SIN_DISEÑO_PUBLICADO | `E1010_1`/`E1010_2` | descrito en prosa, sin columna | descrito en prosa, sin columna | El codebook detalla el diseño (regiones por partido, clusters municipales, PPS) pero no publica identificador de PSU/estrato en el archivo pooled |
| 9 | GPS (Global Preferences Survey) | SIN_DISEÑO_PUBLICADO | `wgt` | ✗ no publicado | ✗ no publicado | Solo `region` como covariable, sin documento de diseño específico de México |
| 10 | Banco Mundial cat. 2661 | PENDIENTE | — | — | — | Solo instrumentos de campo y reportes PDF descargados (pestaña "Documentation"); microdato de caso exige cuenta, no descargado |
| 11 | Pew Global Attitudes 2025 | PENDIENTE | — | — | — | Solo topline agregado y nota en prosa; el propio topline remite a un documento de metodología no incluido en el corpus |
| 12 | OSF "Interacting as Equals" | **NO_APLICA_REGISTRO_ADMINISTRATIVO** | no aplica | no aplica | no aplica | Paquete de réplica con datos electorales (INE) y de pobreza (CONEVAL) a nivel municipio — censales/administrativos, no muestra de individuos |
| 13 | openicpsr Compartamos AEJ | PENDIENTE | — | — | — | RCT de microcrédito; el vocabulario de este censo no tiene valor limpio para un experimento aleatorizado — `FP-123` |

**Conteo final:** 2 MAPEADO · 3 SIN_DISEÑO_PUBLICADO · 7 PENDIENTE · 1 NO_APLICA_REGISTRO_ADMINISTRATIVO. `data/diseno-muestral.yaml`: 43 → 56 filas.

## 3 · Verificación cruda (regla A.13 / A.6 del método, no es estimación)

- **ENGASTO:** `tests/dbfmini.py` sobre `vivienda.dbf`/`viviendas.dbf` de 2012 y 2013 — columnas `EST_SOCIO, EST_DIS, UPM, FACTOR_VIV` byte-idénticas entre ediciones. La FD 2012 (`engasto12_fd.pdf`, extraída con `pdftotext -layout`, 8411 líneas) define las cuatro a nivel de campo (líneas 1909, 1937, 1948, 1965, 3818). 2013 no tiene FD propia — no se infiere el diseño "por parecido": se confirma identidad de columnas y se aplica la misma FD porque describe exactamente esas columnas.
- **ENCOAP:** `TVIV.csv` (1965 filas) — `FAC_VIV`/`UPM_DIS`/`EST_DIS` 1965/1965 no vacíos (136/467/132 valores distintos). `TSDEM.csv` (6324 filas, primeras 2000 leídas) — `FAC_VIV`/`FAC_SEL`/`UPM_DIS`/`EST_DIS` 2000/2000 no vacíos.
- **WVS7:** `pandas.read_stata` sobre `WVS_Wave_7_Mexico_Stata_v5.1.dta` — N=1741 (coincide con el documento de diseño). `W_WEIGHT`/`I_PSU`/`H_URBRURAL` 1741/1741 no vacíos; `I_PSU` con 454 valores distintos.
- **ISSP/ZA6980:** `WEIGHT` presente entre 356 columnas; `command grep -niE "sample design|strat|psu|cluster|multi-stage|multistage"` sobre 2836 líneas de `ZA6980_backgroundvar_mx.pdf` → 0 aciertos de diseño (control: el propio grep encontró y procesó el archivo completo, un acierto irrelevante en línea 2783).
- **CSES:** `E1010_1` 1239/1239 no vacío para `E1006_UNALPHA3=MEX` (coincide con el N del codebook). `command grep -niE "psu|cluster|strat|precinct"` sobre las partes 2 y 6 del codebook → solo descripciones en prosa, ninguna definición de columna.
- **GPS:** `wgt` 1000/1000 no vacío para `isocode=MEX` (110 valores distintos); 17 columnas totales del archivo, ninguna de estrato/PSU.
- **ENSANUT (dedup, no nueva fila):** con `descargas_mx` ahora legible, se releyó `integrantes_ensanut2024_w_ICB.csv` (delimitador `;`, 36021 filas) — `ponde_f`/`estrato`/`est_sel`/`upm` presentes y no vacíos en las primeras 2000 filas, corroborando la fila `ENSANUT (2024)` ya `MAPEADO` que RECENSO-DISEÑO-14 había dejado sin verificación cruda por carpeta ausente. No se editó la fila (no era necesario, el hallazgo es una confirmación, no una corrección).
- **ENAFIN:** el diccionario de datos de `conjunto_de_datos_enafin_2024_csv.zip` confirma que las columnas entregadas (`C_0, C_1a, D_1a...`) son ya agregados por dominio de estudio (0 columnas tipo `FACTOR`/`PONDERAD`/`EST_`/`UPM`).
- **ENESTYC:** `struct.unpack` sobre el encabezado de cada `.dbf` (campo `nrecords`) — las 8 tablas de la edición 2005 tienen exactamente 10 registros cada una.
- **MMSI:** `command grep -niE "factor|ponderad|estrato|upm|conglomer|dise.o muestral"` sobre los 2 PDF → 0 aciertos; control positivo "MMSI" → 12 aciertos combinados.

## 4 · LAPOP (vanderbilt.edu, 18 payloads) — por qué no se abre fila nueva

La fila `LAPOP / AmericasBarometer` ya existe (`MAPEADO`, de RECENSO-DISEÑO-14), pero su verificación fue exclusivamente sobre `MEX_2023_LAPOP_AmericasBarometer_v1.0_w.dta`. Los 18 payloads del host incluyen además olas 2004, 2006, 2019 y 2021 (`Mexico 2004 Export Version.sav`, `Mexico_LAPOP_final 2006 data set`, `MEX_2021_LAPOP_AmericasBarometer_v1.2_w.dta`, etc.) — mismo `fuente:` nombrado, ediciones distintas no censadas individualmente. No se abre fila separada porque el `fuente:` ya existe y cubrirlas exige releer cada reporte técnico de ola (fuera del método "no se infiere de ediciones parecidas" — el propio hallazgo 4.5 de RECENSO-DISEÑO-14 ya documentó que la etiqueta de `strata` en LAPOP puede mentir edición a edición). Queda declarado aquí como brecha conocida dentro de una fila ya `MAPEADO`, no como llave nueva.

## 5 · Perímetro

Escrito: `data/diseno-muestral.yaml` (13 filas nuevas, ninguna existente tocada) · `forense/firmas-pendientes.tsv` (`FP-117`/`FP-120` ejecutadas, `FP-123` nueva) · `canon/gobernanza-v1_15.md` (`ADR-153`) · `canon/estado-programa-v1_10.md` (conteo de ADR recifrado, 152→153) · esta nota · `data/raices.local.yaml` (copiada del clon principal, gitignorada, no entra al diff commiteable). No se tocó `data/manifiesto.yaml`, `milpa/`, `tests/`, `corpus/`, ni ningún `resultado.tsv`. No se descargó nada — todo lo examinado ya estaba en `data/raw` o `descargas_mx`. Ningún contador de Hito D, condicionales o coeficientes se mueve.

**No se marca el encargo como CONSUMIDO ni se hizo commit/push** — instrucción explícita del encargo; el worktree queda con los cambios sin commitear para revisión del supervisor.
