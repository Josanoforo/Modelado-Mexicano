# ACTO RECENSO-DISEÑO-14 — re-censo acotado de diseño muestral

**Fecha:** 2026-08-24 · **Entorno:** UBUNTU (corpus montado) · **Firma que ejecuta:** `ADR-135(f)` (mesa, 20/ago/2026) · **Cierra:** `FP-95` · **ADR de este acto:** `ADR-148`

Este acto no decide nada de diseño: ejecuta el re-censo que `ADR-135(f)` ordenó y `FP-95` registró como pendiente.

---

## 0 · Arranque, entorno y compuerta

| Comprobación | Comando | Resultado |
|---|---|---|
| Clon | `git log -1 --format="%h %s"` en `/home/pc0/Modelado-Mexicano` | `89c939b`, árbol limpio, 14 commits detrás de `origin/main` |
| Base declarada por dirección | `git merge-base --is-ancestor fb02421 origin/main` | `fb02421` **sí** es ancestro; `main` avanzó **3** commits más allá |
| `REPARA-PROPAGA-15` (⛔ ORDEN) | `git log --oneline fb02421..origin/main` | fusionado en `4f5603b` (+ adenda `3491e04`), luego `22d792f` (PR #314). **Compuerta abierta** |
| Base efectiva del acto | `git worktree add … origin/main` | `22d792f` — se refrescó y re-derivó, no se trabajó sobre `fb02421` |
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | `echo` | `sin_variable` ✔ (UBUNTU) |
| Red | `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` | `200` |
| Corpus | `ls data/raw/ \| wc -l` | **316** entradas. `data/raw` **ya existía** como symlink a `/home/pc0/mm-corpus/raw` (no hubo que crearla ni enlazarla) |
| Suite al abrir y al cerrar | `python3 tests/check.py --baseline` | **LÍNEA BASE: VERDE** — 19 FAIL / 147 WARN, subconjunto estricto de la base congelada (24/112); 5 entradas de la base ya no aparecen |

`data/raices.local.yaml` está gitignorado y no venía en el worktree nuevo; se copió del clon principal para que `descargas_mx` (106 payloads) fuera legible. Sin ella, LAPOP habría salido como «sin payload» — el mismo modo de falla que `data/raw` sin symlink.

`pgrep -af claude` solo devolvió el shell de esta sesión. Como ya se documentó al cerrar `ADR-120`, eso **no** prueba ausencia de sesión concurrente; la concurrencia declarada (`TRIAGE-UNIVERSO-12` en NUBE) es disjunta salvo gobernanza/tablero.

---

## 1 · El universo no es 14 · son 18

Dirección pidió expresamente derivar la lista y reportar antes de censar si no daban 14. **No dan 14: dan 18.**

Derivación (`scratchpad/deriva_universo.py`, reproducible):

- 32 filas `PENDIENTE` en `data/diseno-muestral.yaml` (43 entradas totales; `MAPEADO` 9, `SIN_DISEÑO_PUBLICADO` 2).
- Atribución payload→fuente **por evidencia de URL, no por parecido de nombre**: para INEGI, el slug de `/programas/<slug>/` en `url_origen`; para el resto, el host. Un primer barrido léxico dio falsos positivos (CNGMD e INE aparecían con payload por coincidencia de subcadena en `usado_para`); con la regla de URL, **ambos tienen 0**.
- «Material» = el archivo existe en disco bajo su raíz. `python3 tests/manifiesto.py --verifica`: **755 COINCIDE**, 0 ausentes, 1 `NO COINCIDE` (`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf`, defecto preexistente ajeno a este acto).

**Resultado: 18 filas `PENDIENTE` con payload material** — ENNViH, ENOE, ENDIREH, ENDUTIH, MOCIBA, LAPOP, EDER, EDR, ELCOS, ENAPROCE, ENASEM, ENBIARE, ENASIC, ENFIH, ENPOL, ENSAFI, ENSU, ENTI.

### De dónde salió el 14

`FP-84` explica su propia aritmética: «14 de sus 32 fuentes PENDIENTE ya tienen payload material en data/raw hoy (**13 directorios propios más ENOE como zip**)». Hoy `ls -d data/raw/*/` muestra **16** directorios propios de fuentes `PENDIENTE` (`eder*`, `edr2024`, `elcos2012`, `enaproce*`, `enasem*`, `enasic2022`, `enbiare2021`, `endireh*`, `endutih*`, `enfih2019`, `ennvih`, `enpol2021`, `ensafi2023`, `ensu2025`, `enti2022`, `mociba*`), no 13, y el conteo se acotó a `data/raw`, lo que dejó fuera a LAPOP (raíz `descargas_mx`).

**No es deriva del universo desde el 20/ago:** `min`/`max` de `fecha_descarga` por fuente da `2026-07-30 … 2026-08-20`; ninguna de las 18 se adquirió después de que se escribiera `FP-84`. Es un **subconteo en el origen**. Se aplica la regla del encargo — la lista manda sobre la cifra — y se censan las 18, con la discrepancia declarada aquí y en `ADR-148`.

Coincidencia que conviene no confundir: las filas `PENDIENTE` **sin** payload material son exactamente **14**. El 14 correcto describe el complemento, no el universo.

### Cobertura retroactiva (§3 del encargo)

`diseno-muestral.yaml` es del 4/ago y es anterior a la ola de agosto. Barriendo al revés — llaves con payload material que **no** tienen fila en el censo — aparecen **37**, de las cuales cinco son programas de INEGI con microdato sustancial: `engasto` (46 payloads), `enestyc` (15), `enafin` (3), `mmsi` (2), `encoap` (1). El resto son hosts no-INEGI (`microdata.worldbank.org` 62, `banxico.org.mx` 25, `ensanut.insp.mx` 24, `datosabiertos.cnbv.gob.mx` 19, `worldvaluessurvey.org` 11, `osf.io` 10, `gesis.org` 9 …).

**No se inventa ninguna fila** — está fuera del alcance de `FP-95`. Queda como hallazgo en `FP-117`.

---

## 2 · Tabla resumen (las 18)

Estado en vocabulario A.4; entre paréntesis, el valor que se escribió en el `estado` del yaml (que solo admite tres).

| # | Fuente | Ponderador | Estrato | UPM | Réplicas | Estado A.4 |
|---|---|---|---|---|---|---|
| 1 | **ENOE / ENOEN** | `FAC` (clásica) · `FAC_TRI`/`FAC_MEN` (ENOEN) | `EST_D` · `EST_D_TRI`/`EST_D_MEN` | `UPM` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 2 | **ENDIREH 2021** | `FAC_VIV` (vivienda) · `FAC_MUJ` (mujer elegida) | `EST_DIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 3 | **ENDUTIH 2024** | `FAC_VIV`·`FAC_HOG`·`FAC_HOGAR`·`FAC_PER` | `EST_DIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 4 | **MOCIBA 2024** | `FACTOR` | `EST_DIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 5 | **LAPOP México** | `wt` (país/ola) · `weight1500` (comparados) | `strata` | `upm` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 6 | **EDER** | `factor` (vivienda) · `factor_per` (persona) | `est_dis` | `upm` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 7 | **ENASEM** | `FACTORH_21` (hogar) · `FACTORI_21` (individual) | `EST_DIS_21` | `UPM_DIS_21` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 8 | **ENBIARE 2021** | `FAC_VIV`·`FAC_HOG`·`FAC_ELE` | `EST_DIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 9 | **ENASIC 2022** | `FAC_VIV`·`FAC_HOG`·`FAC_CUI`·`FAC_UNI`·`FAC_ELE` | `EST_DIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 10 | **ENFIH 2019** | `FAC_VIV`·`FAC_HOG` | `EDIS` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 11 | **ENTI 2022** | `FAC` | `EST_D` | `UPM_DIS` | no publica | EXISTE-SATISFACE (MAPEADO) |
| 12 | **ENNViH / MxFLS** | `fac_1`…`fac_x` (uno por libro, universo hogar) | **✗ no existe** (`estrato` es tamaño de localidad) | **✗ no existe** | — | EXISTE-NO-SATISFACE (SIN_DISEÑO_PUBLICADO) |
| 13 | **EDR 2024** | **no aplica** (registro administrativo) | no aplica | no aplica | — | EXISTE-NO-SATISFACE (SIN_DISEÑO_PUBLICADO) |
| 14 | **ELCOS 2012** | `FAC_VIV`·`FAC_ELE` | **✗ no nombrado ni presente** | **✗ no nombrado ni presente** | — | EXISTE-NO-SATISFACE (SIN_DISEÑO_PUBLICADO) |
| 15 | **ENPOL 2021** | `FAC_PER` | `EST_DIS` | **✗ no existe** | — | EXISTE-NO-SATISFACE (PENDIENTE, falta 1 de 3) |
| 16 | **ENSAFI 2023** | `FAC_VIV`/`FAC_HOG`/`FAC_ELE` *(sin FD)* | `EST_DIS` *(sin FD)* | `UPM_DIS` *(sin FD)* | — | EXISTE-NO-SATISFACE (PENDIENTE, falta descriptor) |
| 17 | **ENSU 2025** | `FAC_VIV`/`FAC_SEL` *(sin FD)* | `EST_DIS` *(sin FD)* | `UPM_DIS` *(sin FD)* | — | EXISTE-NO-SATISFACE (PENDIENTE, falta descriptor) |
| 18 | **ENAPROCE** | `FAC_EXPA` *(en base de ejemplo)* | **✗** | **✗** | — | EXISTE-NO-SATISFACE (PENDIENTE, payload no es microdato) |

**11 EXISTE-SATISFACE · 7 EXISTE-NO-SATISFACE · 0 NO-ENCONTRADO.**

Movimiento del censo completo: `MAPEADO` 9 → **20**, `SIN_DISEÑO_PUBLICADO` 2 → **5**, `PENDIENTE` 32 → **18**. Las 25 filas no objetivo quedaron **idénticas campo a campo** (verificado recargando el YAML y comparando contra el estado previo).

**Ninguna fuente de las 18 publica réplicas** (BRR, jackknife o medias muestras). Se buscó explícitamente el patrón `REPLICA|JACKKNIFE|BRR|PSU|STRATA|bootstrap|balanced repeated|replicación` en todos los descriptores abiertos: cero aciertos en los diez FD de INEGI y en el reporte técnico de LAPOP. INEGI documenta el diseño por estrato+UPM y deja la varianza al usuario; el único documento que da receta ejecutable es el de EDER (`svydesign` de R) y el de LAPOP (`svyset` de Stata).

---

## 3 · Lo que corrige a `FP-84`

`FP-84` resolvió «de paso» siete ponderadores leyendo FD en segundos. Al citarlos con `archivo:línea` **cuatro de siete estaban incompletos o mal nombrados**:

| `FP-84` decía | Medido en este acto |
|---|---|
| ENPOL `FAC_PER` | correcto — pero ENPOL **no publica UPM** en absoluto |
| ENASIC `FAC_HOG`/`FAC_ELE` | son **cinco** ponderadores (`FAC_VIV`,`FAC_HOG`,`FAC_CUI`,`FAC_UNI`,`FAC_ELE`) |
| ENDUTIH `FAC_PER` | son **cuatro**; `FAC_PER` es el de *usuarios*, no el de la encuesta |
| MOCIBA `FACTOR` | correcto |
| ENFIH `FACTOR` | **no existe**; son `FAC_VIV`/`FAC_HOG`, y el estrato es `EDIS`, no `EST_DIS` |
| ENASEM `FACTORI_NN` | el nombre real lleva sufijo de ola: `FACTORI_21` |
| ENTI `FAC` | correcto |

Ninguna de estas correcciones invalida una cifra sellada: `diseno-muestral.yaml` nunca había sido fuente de una estimación. Pero sí muestran el modo de falla que este acto existe para cerrar — **un nombre de ponderador leído «en segundos» de un FD no distingue universos**, y elegir mal el universo cambia la estimación.

---

## 4 · Hallazgos materiales

### 4.1 · ENNViH no admite error estándar de diseño — bloquea el diseño de CAL-G3

La corrida #1 de mañana (`CAL-G3`) se diseña sobre ENNViH. Lo medido:

- **Ponderador: resuelto**, y por primera vez a nivel de columna. `data/raw/ennvih/ehh09w_all.zip` trae un `.dta` por «libro» con las columnas `fac_1, fac_2, fac_3a, fac_3b, fac_4, fac_5, fac_c, fac_ea, fac_en, fac_s` y `fac_3a_px/fac_3b_px/fac_4_px`, etiquetadas «FACTOR DE EXPANSIÓN LIBRO ⟨X⟩». Universo: **hogar** (`folio` = «IDENTIFICADOR DEL HOGAR»). El censo del 4/ago proponía justamente esto como «candidato para cerrarlo en un futuro acto»; queda cerrado.
- **Estrato: no existe** como variable de diseño. Negativo con conteo: se leyó la cabecera de **los 425 `.dta`** de las tres olas (137 + 147 + 141), **425 examinados sin fallo de lectura**, buscando `estrat|upm|usm|conglom|psu|strat`. Único acierto en las tres olas: `c_portad.dta`, columna `estrato` — cuyos cuatro valores son clases de tamaño de localidad (`<2500`, `2500-14,999`, `15,000-9,999`, `>=10,000`; el tercero es errata de la propia fuente). Eso es una covariable, no un estrato de muestreo.
- **UPM: cero aciertos** en los mismos 425 archivos.
- El método sí está documentado (`calculo-de-factores-de-expansion.pdf`: región → estrato → UPM con probabilidad igual → USM 6 por UPM con PPS → vivienda), pero en notación matemática, sin nombre de campo — lo que FASE B del ACTO M ya había concluido y este acto confirma **desde el microdato**, no solo desde el documento.

**Consecuencia para `CAL-G3`:** sobre ENNViH se pueden calcular estimaciones puntuales ponderadas, pero **no errores estándar basados en diseño** — no hay con qué declarar `strata` ni `id`/`cluster` en un `svydesign`. Quien necesite varianza tiene que (i) declarar explícitamente un supuesto de muestreo aleatorio simple y asumir el sesgo (que para un diseño por conglomerados subestima el error), o (ii) conseguir de la fuente el archivo de identificadores de diseño, que no está en `ennvih-mxfls.org/assets` según lo adquirido. **Es decisión de mesa, no de este acto.** `FP-118`.

### 4.2 · ENAPROCE: los 13 payloads son bases de ejemplo

Los 13 payloads de ENAPROCE (`/programas/enaproce/`, ediciones 2015 y 2018) son **todos** `ejem_base_micro_ciega` / `ejem_base_pyme_ciega`. Pesan entre 4 006 y 33 207 bytes; `ejem_base_micro_ciega.csv` tiene 288 columnas y **21 filas**. El microdato real de ENAPROCE nunca se descargó. Cuenta como «payload material» para el cruce de `FP-95` — y por eso entró al universo — pero no es material sobre el que se pueda censar diseño ni sostener una estimación. `FP-115`.

### 4.3 · ENSAFI y ENSU: existe el microdato, falta el descriptor

Ambas tienen **un solo payload registrado** (el zip de datos) y ninguno de los dos zips trae FD dentro. Las variables de diseño **sí** están en el microdato y completas (`FAC_*`, `EST_DIS`, `UPM_DIS` no vacías en el 100 % de las filas leídas), pero sin FD no se puede citar la definición de universo de cada ponderador — y este acto **no infiere diseño de encuestas parecidas**, aunque los nombres coincidan con la convención de INEGI. Es el obstáculo más barato de levantar de los siete: el FD sigue el mismo patrón de URL que `enasic_2022_fd.xlsx` y `enfih_2019_fd.xlsx`, ya en el corpus. Receta manual en las propias filas del YAML; **no se descargó aquí**. `FP-115`.

### 4.4 · EDR no tiene diseño muestral porque no es una muestra

`Descripcion_BD_Defunciones_2024.pdf` (dentro del zip de datos) define EDR como estadística «proveniente del aprovechamiento de los registros administrativos generados por el Registro Civil…». Es un censo de actas: no hay factor de expansión porque no hay muestra que expandir. Negativo con control positivo: sobre **2 327** líneas, el patrón `FACTOR|FAC_|PONDERAD|EST_DIS|UPM|Estrato de dise|expansi` da **0** aciertos y el control positivo `Ent_regis|defunci` da **142** — el comando sí examinó el archivo.

**Defecto de vocabulario que este acto no puede arreglar solo:** de los tres valores que admite el archivo, `SIN_DISEÑO_PUBLICADO` es el único que no miente, pero se lee como «debería publicar diseño y no lo hace» cuando lo correcto es «no hay diseño muestral que publicar». Se propone a mesa un cuarto valor (`NO_APLICA_REGISTRO_ADMINISTRATIVO`); cambiar el vocabulario del archivo es decisión de diseño, fuera del perímetro de un acto de ejecución. `FP-116`.

### 4.5 · Trampas de nombre que quedan documentadas fila por fila

En cuatro fuentes coexisten una variable `ESTRATO` y una `EST_DIS`, y **no son la misma cosa**: en ENDIREH, ENDUTIH, MOCIBA y ENFIH, `ESTRATO` es el estrato socioeconómico o sociodemográfico (1–4) y el de diseño es `EST_DIS` (o `EDIS` en ENFIH). Lo mismo con `UPM` (llave de identificación) frente a `UPM_DIS` (conglomerado de diseño), y con `EST` (C(2), ámbito) frente a `EST_D` en ENOE y ENTI. En LAPOP la trampa es al revés: la variable `strata` está **etiquetada** «Peso estandarizado», etiqueta que no corresponde a su rol. Y el FD de ENASIC etiqueta «FACTOR HOGAR DE EXPANSIÓN» a `FAC_CUI`, `FAC_UNI` y `FAC_ELE` por igual, aunque nombre, rango y universo difieren.

Todas quedan escritas en el campo correspondiente de cada fila, no solo aquí.

---

## 5 · Verificación cruda (confirmación de existencia, no cálculo)

Por cada fuente con nombre citado se abrió el microdato lo justo para confirmar que la columna existe y no está toda vacía. **Ningún número entra al canon.** Se contaron no-vacíos y valores distintos sobre las primeras 2 000–3 000 filas de cada tabla (o todas, si la tabla es menor).

Resultados que **no** fueron un simple «existe y está llena» y que quien estime necesita saber:

- **ENOE 2025-4t:** `est_d_men` 1 845/2 000 en `viv`/`hog` — la parte de la muestra sin panel mensual, no un defecto de lectura. `coe1`/`coe2` no traen estrato de diseño en ninguna era: hay que unir contra `sdem`/`hog`/`viv`.
- **ENASEM 2021:** `MASTER_FOLLOW_UP_FILE_2021.csv` solo trae valor en 1 587 de 3 000 filas leídas (incluye casos sin entrevista 2021). `SECT_G_J_K_SA_2021.csv` trae `FACTORH_21` pero **ni** `FACTORI_21` **ni** las variables de diseño.
- **ENTI 2022:** `EST_D` no vacío en cinco de siete tablas; `ENTI2022_COE1` y `ENTI2022_COE2` **no traen `EST_D` en absoluto**.
- **ENFIH 2019:** `EDIS` y `UPM_DIS` en las 16 tablas, pero el ponderador solo en `TVIVIENDA`, `THOGAR` y `TCONCENTRADORA`; las tablas de detalle no lo traen.
- **LAPOP MEX 2023:** `wt` no vacío en 1 622/1 622 pero con **un solo valor distinto (1)** — en esta edición de un solo país el peso de país es constante. Es correcto, no un defecto, pero significa que ponderar por `wt` aquí no mueve el punto estimado. `weight1500` **no existe** en este archivo: es la variable de los conjuntos comparados.
- **ENASIC 2022:** `THOG_UNIP.csv` tiene 928 filas en total, todas llenas (no es truncamiento).

Herramientas: `zipfile` + `csv` (sin `unzip`/`7z` en esta caja), `tests/dbfmini.py` para DBF, `pandas.read_stata` en modo iterador para `.dta`, `openpyxl` para `.xlsx`, `pdftotext -layout` para PDF. Para los dos `.xls` BIFF (ELCOS, EDER 2011) hizo falta `xlrd`, ausente del sistema: se instaló con `pip install --target` en el scratchpad, **sin tocar el intérprete del sistema ni el repo**.

---

## 6 · Perímetro

Escrito: `data/diseno-muestral.yaml` (solo las 18 filas objetivo) · `forense/notas/2026-08-24-recenso-diseno.md` (esta) · `forense/firmas-pendientes.tsv` · `canon/gobernanza-v1_15.md` (`ADR-148`) · `forense/encargos/2026-08-24-RECENSO-DISENO-14.md`.

No se tocó `data/manifiesto.yaml`, `data/censo-explotacion-2026-08-17.tsv` (ambos solo lectura, como manda el encargo), `milpa/`, `tests/`, `corpus/`, ni ningún `resultado.tsv`. **Cero escrituras sobre `data/raw/`**: el corpus se abrió en solo lectura y los archivos extraídos de zips se escribieron en el scratchpad. Este acto **no descargó nada**.
