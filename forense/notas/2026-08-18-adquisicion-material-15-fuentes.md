# Nota del acto · ADQ-15 — adquisición material de las 15 fuentes `EXISTE-NO-VERIFICADO`

18/ago/2026 · rama `adq-15` · SHA de arranque **`e563e5d`** (`origin/main` en el momento de crear el worktree; `PR #268`/`ACTO B2-SEMANTICO` ya fusionado — el orden que impuso el lanzamiento se cumplió).
Encargo: `forense/encargos/2026-08-18-ADQ-15.md`. Gate (`GATE-DURABLE-V7`, `PR #260`): cumplido desde antes de este acto.

## §6 · Auditoría — contadores movidos

**Cero.** `13 de 27`, `0 de 15`, `11 de 15`, `1 de 2` y `4 de 144` no se mueven. Este acto adquiere material y clasifica acceso; **no abre ninguna fuente a nivel variable** y no produce ninguna medición sobre México.

Afirmaciones de este artefacto que NO salen de un comando, declaradas por A.4/v2.1: (1) el juicio de que un veredicto concreto es `EXISTE-SATISFACE` y no `EXISTE-NO-SATISFACE` es lectura de la condición que la cola declaraba faltante contra lo que el payload trae — el inventario, los hashes y las cifras de cobertura sí son 100 % derivados; (2) la lectura de que `laoms.org` falla del lado del origen y no de la caja se apoya en un control positivo, no en una prueba directa sobre el servidor, y por eso se escribe con la fórmula de A.5 y no como hecho sobre el portal.

## §1 · Verificación de existencia (A.8) — re-corrida, no heredada

El comando del encargo, contra `e563e5d`:

```
$ awk -F'\t' 'NR>1 && $15=="2026-08-14"{print $13}' data/universo-puertas-2026-08-14.tsv | sort | uniq -c
     15 EXISTE-NO-VERIFICADO
      4 NO-ACCESIBLE
      3 NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS
      2 NO-ENCONTRADO
```

Coincide con el encargo. El cruce contra `cola-adquisicion-2026-08-12.tsv` también: **12 cruzan** por `fuente_canonica` y traen `palanca`; **3 no** (`EXPERIMENTO_DE_INFORMACION_ELECTORAL_2009`, `FINANZAS`, `GLOBAL_PREFERENCES_SURVEY`), trabajadas al final como manda el encargo.

**Defecto del encargo, menor, corregido en ejecución:** el perímetro cita `tools/manifiesto.py --registra`. Ese archivo no existe (`find . -name "manifiesto*.py"` → `./tests/manifiesto.py`). La vía correcta la declara `data/INFRAESTRUCTURA-v1_0.md:22`: **`tests/manifiesto.py --registra`**. Se usó ésa.

## §2 · El delta que más rindió — A.8 por fila contra el manifiesto

El lanzamiento ordenó cruzar **cada una de las 15** contra `data/manifiesto.yaml` antes de bajar nada, y marcar `YA-ADQUIRIDA` con el id en vez de descargar (lección WVS/GESIS de `ADR-77`). Criterio del cruce, para que sea reproducible y no una impresión: **host exacto de `url_origen` Y al menos un patrón de nombre/ruta**; los aciertos de un solo lado se inspeccionaron uno por uno y se descartaron por accidente de subcadena.

**Tres de las 15 ya estaban.** Ninguna se volvió a descargar:

| fila | entradas ya en el manifiesto | cobertura real |
|---|---|---|
| `GLOBAL_PREFERENCES_SURVEY` | 5 (`gps_dataset`, `gps_dataset_country_level`, `gps_questionnaires`, `gps_do_files_individual_level`, `gps_do_files_country_level`) | completa; `url_origen` = `https://gps.econ.uni-bonn.de/downloads`, **exactamente** la URL de la fila |
| `ENCUESTA_ANUAL_DE_COMPETENCIAS_FINANCIERAS_2019_2024` | 1 (`banxico_encuesta_competencias_financieras_2024`, 12/ago, P·LOTE-2) | **parcial** — es la ola 2024 sola; el nombre de la fila abarca 2019-2024 |
| `SERIES_SPEI_CODI_BANXICO` | 16 (grupo `R3.4_Banxico_CoDi_SPEI`, 6/ago) | **parcial** — cubre CoDi (CF881-CF885, IdMF 2019-2024); la URL propia de la fila, las series de SPEI, no tiene payload |

`GLOBAL_PREFERENCES_SURVEY` es el caso que justifica que el delta sea *por fila* y no *por cola*: **no cruza la cola por nombre**, así que un acto guiado sólo por la cola la habría vuelto a bajar entera. Es la misma trampa de `ADR-77`, en una fila que la cola ni siquiera menciona.

## §3 · Qué se adquirió — 89 payloads, 56.5 MB, todos en el corpus compartido

```
$ python3 tests/manifiesto.py --verifica    (extracto)
  data_raw: coincide=606 · no_coincide=1 · ausente=0 · sin_configurar=0
  89 de 89 entradas adq15_* → COINCIDE
```

| grupo en `data/raw/` | payloads | MB |
|---|---:|---:|
| `ADQ15_WB6667_Tutores_Pedagogicos_Moviles_2016` | 24 | 6.46 |
| `ADQ15_CNBV_AhorroFinanciero_Financiamiento` | 14 | 17.10 |
| `ADQ15_CNBV_BDIF_inclusion_financiera` | 12 | 2.94 |
| `ADQ15_WB870_Enterprise_Survey_MX_2010` | 10 | 6.18 |
| `ADQ15_ENAFIN_2024_RNM_INEGI` | 10 | 4.76 |
| `ADQ15_OMCA_conflictos_agua` | 9 | 0.47 |
| `ADQ15_Brasdefer_corpus_pragmatico` | 3 | 0.58 |
| `ADQ15_VotarEntreBalas_DataCivica` | 2 | 1.06 |
| `ADQ15_IFT_SFD_uso_confianza` | 3 | 16.69 |
| `ADQ15_JPAL_Experimento_Informacion_Electoral_2009` | 2 | 0.28 |

**PR #77, atendido al arrancar y no al cerrar.** El worktree nuevo no traía `data/raw` ni `data/raices.local.yaml` (ambos gitignorados). Antes de bajar el primer byte se creó el symlink `data/raw -> /home/pc0/mm-corpus/raw` y se copió `raices.local.yaml`. Comprobación de cierre: `ls -la data/raw` → symlink al corpus compartido; los 89 payloads viven en `/home/pc0/mm-corpus/raw/ADQ15_*`, **no** dentro del worktree. `git status` no lista ninguno.

## §4 · Los quince veredictos

`awk` del encargo, re-corrido **después** de escribir:

```
      7 EXISTE-NO-SATISFACE
      6 EXISTE-SATISFACE
      4 NO-ACCESIBLE                              ← preexistentes, no de este acto
      3 NO OBTENIDO POR ESTE AGENTE EN 2 INTENTOS ← preexistentes, no de este acto
      3 NO-ENCONTRADO                             ← 2 preexistentes + FINANZAS
      1 NO OBTENIDO POR ESTE AGENTE EN 7 INTENTOS ← laoms.org
```

**Cero `EXISTE-NO-VERIFICADO`.** De las 15: 6 `EXISTE-SATISFACE`, 7 `EXISTE-NO-SATISFACE`, 1 `NO OBTENIDO … EN 7 INTENTOS`, 1 `NO-ENCONTRADO`.

| palanca | fuente | veredicto | por qué |
|---|---|---|---|
| 2 | Brasdefer | `EXISTE-NO-SATISFACE` | 3 páginas de corpus adquiridas (197 interacciones); falta lo que la cola ya declaraba: sin archivo de replicación, sin muestra nacional no universitaria, y el corpus de servicio no es un pareado rechazo superior/inferior |
| 5 | WB 6667 Tutores | `EXISTE-NO-SATISFACE` | 24 payloads (22 materiales + DDI + JSON); faltan los 6 `.dta` que el propio DDI declara — exigen cuenta gratuita, que **no** es `NO-ACCESIBLE` por A.4 |
| 8 | WB 870 Enterprise Survey | `EXISTE-NO-SATISFACE` | 10 payloads; el microdato vive en `enterprisesurveys.org`, que redirige a `login.enterprisesurveys.org/en/signin` |
| 26 | OMCA conflictos por el agua | `EXISTE-SATISFACE` | base completa por el endpoint AJAX del mapa: **375 conflictos, 1926-2025, 31 entidades, 375/375 georreferenciados, 8 tipos, 370/375 con evidencia hemerográfica** — medido sobre el payload |
| 27 | Eventos de protesta (LAOMS) | `NO OBTENIDO … EN 7 INTENTOS` | ver §5 |
| 32 | ENCF 2019-2024 | `EXISTE-NO-SATISFACE` | `YA-ADQUIRIDA` (A.8): sólo la ola 2024; la condición faltante declarada es "comparabilidad", que una ola no da |
| 41 | IFT SFD | `EXISTE-NO-SATISFACE` | las **dos** versiones del reporte especial adquiridas e íntegras (8 084 499 B y 9 318 564 B, cada una confirmada por dos descargas byte-idénticas); `basededatossfd.zip` no obtenida en 11 intentos — ver §5 |
| 43 | Votar entre Balas | `EXISTE-SATISFACE` | base completa: **3 379 filas, 28 columnas, 2017-2026** (404 sin fecha, declarado) + diccionario + metodología → responde "reglas y años exactos" |
| 45 | Series SPEI/CoDi | `EXISTE-NO-SATISFACE` | `YA-ADQUIRIDA` parcial (16 entradas, lado CoDi); la URL propia de la fila (SPEI) sin payload |
| 47 | Ahorro Financiero y Financiamiento | `EXISTE-SATISFACE` | 14 payloads: 6 PDF del reporte trimestral (Mar2023-Mar2025) + 6 xlsx de la base 2000-Jun2023 + glosario + diccionario |
| 48 | BDIF | `EXISTE-SATISFACE` | 12 payloads vía `datosabiertos.cnbv.gob.mx` |
| 49 | ENAFIN | `EXISTE-NO-SATISFACE` | 10 payloads; los csv abiertos son **tabulados** (`DOMINIO_ESTUDIO`), no registros de empresa — el microdato exige el Laboratorio de Microdatos (eso sí `NO-ACCESIBLE` por restricción institucional) |
| — | Experimento información electoral 2009 | `EXISTE-SATISFACE` | paquete de replicación completo: `Chongetal_aggregate_JOP.dta`, `Chongetal_survey_JOP.dta` y sus dos `.do` |
| — | `FINANZAS` | `NO-ENCONTRADO` | identidad sin resolver; ver §5 |
| — | Global Preferences Survey | `EXISTE-SATISFACE` | `YA-ADQUIRIDA` (A.8), 5 entradas desde el 12-13/ago |

## §5 · A.7 — la doble descarga, y lo que atrapó que no era su objetivo

Todo payload se bajó **dos veces** y se comparó byte a byte. **Seis** resultaron con `sha256` crudo distinto; en los seis se identificó *qué campo* cambiaba antes de concluir nada, como exige el corolario de A.7, y en los seis el hash de contenido **coincide** → sin `PARO`. Los dos hashes quedan en el `nota:` de cada entrada, siguiendo el precedente del XML de Descarga Masiva.

| payload | campo que varía | hash de contenido |
|---|---|---|
| `enafin2024_rnm_catalog.html` | contador "Visitas a la página" | `bb2c9762acf39d69` |
| `enafin2024_rnm_get_microdata.html` | ídem | `24e8be8db1da72b4` |
| `enafin2024_rnm_related_materials.html` | ídem | `2ee69a473f2cdad0` |
| `omca_consulta.html` | **orden** de los `<option>` del selector de fuente (`ORDER BY` no determinista) | `d501a657e90b1e7b` |
| `jpal_evaluacion_landing.html` | token rotatorio `data-cfemail` de Cloudflare | `2c3c6382aaa9489e` |
| `votar_entre_balas_base.zip` | el servidor genera el ZIP al vuelo; el `mtime` de los miembros es la hora de la petición | `c1d343311977fec4` |

**Y atrapó algo para lo que no fue diseñada: transferencias truncadas.** `www.ift.org.mx` sirvió `reporteespecialserviciosfinancierosdigitalessfd.pdf` en **4 979 926 B sin marcador `%%EOF`**, y la segunda bajada del mismo objeto dio **8 084 499 B**. Sin la doble descarga ese PDF se habría registrado como bueno. **No se registró.** Reintentado con el criterio correcto —dos bajadas consecutivas idénticas *y* estructuralmente válidas—, el mismo objeto se obtuvo íntegro a la tercera: **8 084 499 B, `sha256 3238bdfe…`, dos veces seguidas**. El tamaño bueno es el grande; los 4 979 926 B eran el corte. El defecto en la primera versión del arnés —contar una segunda descarga fallida como "el contenido varía"— se detectó porque uno de los hashes reportados era `e3b0c44298fc1c14…`, el sha256 de la cadena vacía; el arnés se corrigió para validar estructura (`%%EOF` en PDF, directorio central en ZIP, parseo en JSON) antes de comparar, y se re-verificaron **los 89** payloads con él.

**`laoms.org` (palanca 27), 7 intentos.** `https` → curl 35 (`TLS connect error: unexpected eof while reading`); `http` → 502 dentro de la caja y **curl 52 `Empty reply from server` fuera** de ella; `www.laoms.org` en los dos esquemas; TLSv1.2 forzado; TCP directo. **Control positivo en el mismo camino y el mismo minuto:** `votarentrebalas.datacivica.org` → 200 dentro y fuera del sandbox. Eso descarta la caja como causa, pero A.5 manda escribirlo como hecho sobre este agente. *Receta manual:* abrir `https://laoms.org/` en navegador; si tampoco carga, hay copia en `web.archive.org/web/2024/https://laoms.org/` (200, 115 907 B, verificado hoy) — **copia de archivo, no la base**.

**`basededatossfd.zip` (palanca 41), 11 intentos.** El host corta la conexión TLS (curl 35/56) y no honra `Range`; a diferencia de los dos PDF, que sí acabaron llegando, el ZIP no bajó **ni un byte** en ninguno de los 11 intentos. No obtenida. *Receta manual:* bajarla en navegador y **comprobar que el ZIP abre** antes de darla por buena — este host trunca.

## §5 bis · Tres cosas que este acto encontró y que no venían en el encargo

**(a) La cadena TLS de `*.cnbv.gob.mx` está resuelta, y sin `-k`.** `acceso-puertas-2026-08-13.tsv` dejaba dos filas (`AHORRO FINANCIERO Y FINANCIAMI` y `FINANZAS`) con la acción pendiente *"verificar en navegador real si el AIA fetching resuelve la cadena de certificado"*. Se hizo, programáticamente: el leaf (`CN=*.cnbv.gob.mx`, emisor `GlobalSign RSA OV SSL CA 2018`) se leyó por `CONNECT` a través del proxy, su extensión **AIA** declara `http://secure.globalsign.com/cacert/gsrsaovsslca2018.crt`, se bajó ese intermedio y se encadenó al `GlobalSign Root CA - R3` que el almacén del sistema ya tiene. Con ese bundle, `pnif.cnbv.gob.mx`, `www.cnbv.gob.mx` y `datosabiertos.cnbv.gob.mx` responden **200 con verificación completa**. El `000` del sondeo era cadena incompleta del servidor, no bloqueo.

**(b) El `200` de `gob.mx` que registró el sondeo TRIAGE-63 para BDIF es un reto de WAF.** `https://www.gob.mx/cnbv/acciones-y-programas/bases-de-datos-de-inclusion-financiera` devuelve **200 con 1 826 bytes y `<title>Challenge Validation</title>`** — bloqueo disfrazado, no portal. Persiste con cabeceras de navegador completas y `cookie jar`. El **CDN** del mismo dominio (`/cms/uploads/attachment/file/...`) **no** está tras el reto: de ahí salieron los 6 PDF de AFyFeM. Y la página propia de CNBV para BDIF (`cnbv.gob.mx/Inclusión/Paginas/Bases-de-Datos.aspx`) **no lista ningún archivo**: última modificación `15/03/2016` y contiene el marcador de plantilla literal `aqui no va nada`. La vía real y abierta es `datosabiertos.cnbv.gob.mx`.

**(c) El mismo fichero nominal de CNBV, servido por dos hosts oficiales, no es el mismo objeto.** `Base_Ahorro_Financiero_y_Financiamiento_2000-Sep2022.xlsx` pesa **386 483 B** en `www.cnbv.gob.mx/Documents/` y **387 045 B** en `datosabiertos.cnbv.gob.mx/Documentos/DGEE/`. No es artefacto de hash: comparados como contenedores OOXML, **15 de 31 miembros comunes difieren** —incluido `xl/worksheets/sheet1.xml` (267 746 vs 267 111 B)— y la copia de `datosabiertos` trae además un miembro `[trash]/0000.dat`. Son dos revisiones distintas del mismo nombre. Ninguna se presume canónica: **se registran las dos**, renombradas `…​.wwwcnbv.xlsx` y `…​.datosabiertos.xlsx`.

**Aviso de método, para el próximo acto que sondee INEGI:** barrer patrones de URL contra `www.inegi.org.mx` **no sirve**. Devuelve `200` con una página de **2 263 B** para toda ruta inexistente (soft-404). Un barrido de 24 candidatos dio 24 "HIT 200" — los 24, la misma página. Se descartaron por tamaño idéntico. La vía correcta resultó ser el **JSON-LD `schema.org`** que cada página de programa incrusta: su campo `distribution.contentUrl` trae la URL real de datos abiertos (`.../datosabiertos/...`, no `.../microdatos/...`).

## §7 · Perímetro — qué se escribió y qué no

**Escrito:** `data/manifiesto.yaml` (89 entradas nuevas, vía `tests/manifiesto.py --registra`; 0 entradas preexistentes cambiaron de contenido, verificado comparando el YAML parseado contra `HEAD`) · `data/universo-puertas-2026-08-14.tsv` (15 filas, columnas `clasificacion_a4` y `universo_declarado`; `git diff --numstat` → `15 15`) · `data/cola-adquisicion-2026-08-12.tsv` (alta material: dos columnas nuevas al final, `estado_adquisicion_ADQ15` e `ids_manifiesto_ADQ15`; 12 filas con alta, 42 marcadas `FUERA-DE-ALCANCE-ADQ15` para que una celda vacía no se lea como "no adquirida") · `forense/firmas-pendientes.tsv` (`FP-17`, columna `ejecutada_en`) · `forense/hallazgos.md` · esta nota · el encargo a `CONSUMIDO`.

Antes de ampliar el esquema de la cola se verificó que **ningún script la lee** (`grep -rn "cola-adquisicion" tools/ tests/` → vacío) y que `INFRAESTRUCTURA-v1_0.md:40` la declara snapshot con **0 lectores**. Las columnas se añaden **al final**: los índices existentes no se mueven.

**No escrito:** `canon/`, `tests/`, `milpa/` — como manda el perímetro.

## §8 · Suite, fusión y el defecto que este acto se hizo a sí mismo

**`T02` mordió, y el mordisco era mío.** La primera versión de esta nota se llamaba `forense/notas/2026-08-18-adq-15.md` y colisionaba por nombre normalizado con `forense/encargos/2026-08-18-ADQ-15.md` — el mismo trampolín que `ÍNDICE-2` ya había pisado con los nombres del propio encargo. `tests/check.py --baseline` lo marcó **`ROJO`, 2 entradas nuevas** (`T02` por la colisión y `T16` porque ese FAIL extra desalineaba la cifra declarada en `estado-programa`). Renombrada a `2026-08-18-adquisicion-material-15-fuentes.md` y actualizadas sus dos citas (el encargo y la fila `FP-17`), la suite vuelve a **`VERDE`**. *Un encargo con fecha y sigla, y una nota que quiera nombrarse igual, colisionan siempre: la nota tiene que llevar nombre descriptivo, no el del encargo.*

**Fusión de `origin/main`, un conflicto real y dos automerges verificados a mano.** `origin/main` avanzó **12 commits** durante este acto (hasta `6650047`, `PR #275`/`FP29-RECONCILIA`). Único conflicto: `data/manifiesto.yaml`, donde **los dos lados apendizan al final** — 89 entradas `adq15_*` contra 2 entradas `pew_*`. Resuelto como unión conservando ambos bloques: **722 entradas, cero ids duplicados**, verificado con `yaml.safe_load`. `forense/hallazgos.md` y `forense/firmas-pendientes.tsv` automergearon con el driver `union`, y **se verificaron a mano contra el modo de falla que el propio `hallazgos.md` documenta dos veces esta semana**: 325 entradas con **cero duplicados exactos** y salto de línea final intacto; 58 filas de 9 columnas sin ids repetidos.

**Cifra de la suite sobre el árbol fusionado**, que es la única que existe (lección de la colisión `#264`/`#265`, 18/ago): **19 FAIL · 118 WARN · `LÍNEA BASE: VERDE`**, nada nuevo frente a `tests/baseline.json`. No hay cascada a `estado-programa` desde este acto: `T16` no reporta desalineación, porque la cifra que `origin/main` ya declaraba es la que el árbol fusionado produce.

**Observado y NO arreglado, porque está fuera de perímetro:** `tests/manifiesto.py --verifica` reporta **1 `NO COINCIDE` preexistente** (`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf`, raíz `data_raw`) y **49 `AUSENTE` en `descargas_mx`**. Ninguno es de este acto —los 89 payloads nuevos dan 89/89 `COINCIDE`— y los 49 son la deuda que `FP29-RECONCILIA` (`PR #275`) ya nombró. Se declara, no se toca.
