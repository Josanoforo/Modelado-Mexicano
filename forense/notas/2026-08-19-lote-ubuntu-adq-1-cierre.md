# Nota del acto · LOTE UBUNTU-ADQ-1 — adquisición e higiene del corpus, cinco tareas en un acto

**Fecha:** 2026-08-19 · **Entorno:** UBUNTU (asignado) · **Worktree:** `/home/pc0/mm-ubuntu-adq1` · **Rama:** `ubuntu-adq-1` · **Base:** `b4a9b3f` (`PR #292`).
**Encargo:** `forense/encargos/2026-08-19-LOTE-UBUNTU-ADQ-1.md` (archivado por A.3 en el Commit 0). **ADR:** `ADR-126` (número derivado al escribir; se re-deriva al fusionar).

---

## §0 · ARRANQUE — los cinco puntos, crudos

**1 · REPO.** Clon principal `/home/pc0/Modelado-Mexicano`, `HEAD = e25f2bd` (`PR #289`), `git status` limpio, `main` **2 commits detrás** de `origin/main`. Se refrescó (`git merge --ff-only origin/main`) y se abrió worktree propio.

**2 · SHA.** `b4a9b3f` **no existía en el clon** al arrancar (`git cat-file -t b4a9b3f` → `fatal: Not a valid object name`). Tras `git fetch origin`: `c489c9e..b4a9b3f main`. `origin/main = b4a9b3ffc6c166f805d002b80867108f36e6704f` (`Merge pull request #292`, 2026-08-19 11:07:15 -0600) — **coincide exacto con el SHA de redacción**, `git rev-list --count b4a9b3f..origin/main` → `0`. El SHA no se movió: lo que estaba desfasado era el clon local.

**3 · `data/raw`.** En el worktree nuevo: **no existía** (`ls: cannot access 'data/raw'`). **Se creó** el symlink → `/home/pc0/mm-corpus/raw` (284 entradas). Además faltaba `data/raices.local.yaml` (gitignorado, por máquina): **se copió** del clon principal — sin él, `descargas_mx` y `downloads` quedan como raíz-no-configurada y T2 no sería medible. Confirmación del hallazgo de `PR #278`: el symlink es por worktree, no se hereda.

**4 · ENTORNO (A.2, tres partes, crudas).**
- Variable: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → **vacía** (caja local, no nube). `uname`: `Linux 6.18.33.2-microsoft-standard-WSL2 x86_64`.
- Sonda de red: `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → **`200`**, exit 0. (La caja NUBE de `U2-EV1`, misma URL, dio `000` exit 56.)
- Corpus: `ls data/raw/ | head -1` → `20260813130000.export.CSV.zip`. Montado.

**`type grep`** → **es una función de shell** que envuelve `ugrep -I` (`exec -a ugrep "$_cc_bin" -G --ignore-files --hidden -I ...`). `command grep --version` → GNU grep 3.12. **Todo veredicto negativo de esta nota se declaró con `command grep`**, con conteo de archivos examinados y **control positivo en el mismo archivo y el mismo comando** — la regla que el hallazgo de ayer (`xargs -0 command grep` devuelve vacío sin correr) dejó escrita.

**5 · ESPEJO.** Nada. Todas las cifras de esta nota salen del disco o del clon, con el comando a la vista.

**Dueña única.** `pgrep -af claude` al arrancar: sólo los procesos de esta propia sesión (dos líneas, ambas el `bash -c` del comando que las imprimió). Sin sesión concurrente. Se cruzó además con `git reflog` (última entrada ajena: `2026-08-19 09:56:51`, fusión de `PR #289`) — el mecanismo que `ACTO CAJA-RESIDUOS` dejó escrito porque `pgrep` no ve una sesión de agente concurrente.

---

## §1 · T1 · U2-ADQ — los indicadores oficiales de precisión

**Contador: 2 payloads nuevos al manifiesto.**

### 1.1 · Qué se adquirió

La ley (`PROPUESTA-remediacion-brecha-documental.md:16`, §2) pide *"indicadores oficiales de precisión (CV/EE/IC) descargados con sha256"*. La receta del `PARO` (`forense/notas/2026-08-19-u2-ev1-paro-red.md` §7) apuntaba a `922/download/29534`. Sigue vigente. La ficha RNM 922 (ENASIC 2022) publica **exactamente dos** recursos bajo *Indicadores de la Calidad/Evaluación de la Calidad*, y se adquirieron los dos:

| id manifiesto | archivo (nombre oficial, `Content-Disposition`) | bytes | sha256 |
|---|---|---|---|
| `enasic2022_ipe_cv_ee_ic` | `IPE_CV-EE-IC_ENASIC_2022-00_Def_V1_260923.xlsx` | 51 724 | `c37b5fc687ae9fc727d0cd1d883adef00165086e54453d3070b9eae51801c540` |
| `inegi_ipe_formato_estandarizado_cv_ee_ic` | `CV-EE-IC_IPE_Externos_Encuestas_2022_08_26.xlsx` | 45 970 | `912fc9de75d95ded09db91b802b54e6db57292cf38eb5fd49796267f99759596` |

Los dos **al corpus compartido** `/home/pc0/mm-corpus/raw` (no sólo al worktree — defecto `PR #77`): el primero en `enasic2022/`, el segundo en `ipe_inegi/` porque es institucional cross-programa (`Externos_Encuestas`), no de ENASIC, aunque se obtuvo por la ficha 922.

**A.7 (patrón `#277`):** cada uno se bajó **dos veces** y se comparó `cmp` byte a byte. **Idénticos los dos** — la fuente no trae token de solicitud. Ningún `PARO`.

**A.1 — una invocación de `--verifica` por `--id`, las dos respuestas sin colapsar:**

```
$ python3 tests/manifiesto.py --verifica --id enasic2022_ipe_cv_ee_ic
enasic2022_ipe_cv_ee_ic [data_raw]: COINCIDE -- sha256 y tamaño (51724 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0

$ python3 tests/manifiesto.py --verifica --id inegi_ipe_formato_estandarizado_cv_ee_ic
inegi_ipe_formato_estandarizado_cv_ee_ic [data_raw]: COINCIDE -- sha256 y tamaño (45970 bytes) verificados contra data/manifiesto.yaml
  data_raw: coincide=1 · no_coincide=0 · ausente=0 · sin_configurar=0
```

Ni `AUSENTE`, ni raíz-no-configurada, ni hash-discordante: las tres respuestas se mantienen separadas y ninguna aplica.

### 1.2 · Qué trae el archivo oficial — y qué NO trae

Hoja `INDICADORES`, 21 columnas (`Tipo_Programa … IntConf_Sup`), **337 filas barridas, 2 con contenido**:

| Variable | Parámetro | Estimación | CV | ErrorEst | Niv_Conf | IC inferior | IC superior |
|---|---|---|---|---|---|---|---|
| Población total *(se excluyen 21 090 casos que no especificaron la edad de la población menor de 15 años)* | Total | 128 857 388 | 1.391962655 | 1 793 646.71919227 | **90** | 125 907 101.688467 | 131 807 674.311533 |
| Sí requirió apoyo o cuidados *(misma exclusión)* | Total | 58 594 471 | 1.6048742386 | 940 367.570351719 | **90** | 57 047 703.9912394 | 60 141 238.0087606 |

**El reactivo `P7_12_7` NO está.** Veredicto `NO-ENCONTRADO`, con el universo A.4 a la vista, fecha 2026-08-19:

1. **El archivo entero**: las 337 filas de `INDICADORES` (2 con contenido, ninguna con `P7_12_7` ni con `Parametro` distinto de `Total`) + las 60 filas de la hoja `Catálogo` (catálogo institucional de claves, sin estimaciones).
2. **El segundo recurso** (`29535`): 276 filas barridas, 28 con contenido — es la **plantilla del formato estandarizado** aprobada por el Comité de Aseguramiento de la Calidad del INEGI, con la definición de las 21 columnas. Cero estimaciones.
3. **La ficha RNM 922 completa**: `catalog/922`, `/related-materials` y `/data-dictionary` descargadas y barridas. Enlaces de descarga declarados: **sólo `29534` y `29535`** (`command grep -o 'catalog/922/download/[0-9]*' | sort -u` sobre las dos páginas). `P7_12_7` en `/data-dictionary`: **0 coincidencias**.
4. **La página de programa de INEGI**, por el método que `ACTO ADQ-15` dejó escrito (no barrer patrones de URL: `www.inegi.org.mx` devuelve `200` con una página de 2 263 B para toda ruta inexistente — verificado otra vez aquí, 3 de 3 rutas candidatas dieron exactamente 2 263 B). El **JSON-LD `schema.org`** de `https://www.inegi.org.mx/programas/enasic/2022/` declara **una sola** `distribution.contentUrl`: `.../datosabiertos/conjunto_de_datos_enasic_2022_csv.zip` — microdato abierto, ningún archivo de precisión.
5. **El corpus propio, antes de hoy**: `command grep -in "precision|precisión|coeficiente de variacion" data/manifiesto.yaml` → **0 coincidencias** en las 722 entradas (1 archivo examinado).

### 1.3 · Defecto material en el pre-registro: dice `ENASIC 2021`, y es **2022**

`forense/notas/2026-08-19-u2-ev1-paro-red.md` (§5 dos veces, §7 una vez) y `forense/encargos/2026-08-19-U2-EV1.md` (§6) fijan el objeto del cruce como *"`familismo_obligacion` vía `ENASIC 2021`, reactivo `P7_12_7`"*. **La edición es 2022.** Medido por comando: `ENASIC 2021` aparece en **4 líneas de 2 archivos**, los dos escritos por el propio acto `U2-EV1` del 19/ago; `ENASIC 2022` aparece en **50 archivos** del repo. Y la especificación sellada es explícita — `especificaciones-produccion.json#ESP-OPACA-B-d13ec4fe`: `"edicion": "2022"`, `"periodo_levantamiento": "2022-10-24/2022-12-16"`, `"input_path": ".../enasic2022/enasic_2022_bd_csv.zip"`; la celda-D `G5.familismo_obligacion.actitud.yaml` dice `edicion_periodo: "2022"`; el manifiesto sólo tiene payloads `enasic2022_*`.

Era un defecto **material**: seguido al pie de la letra habría mandado al acto sucesor a buscar el indicador de precisión de una edición que no es la que produjo la θ. No se corrige la nota del `PARO` (es registro de lo que ese acto escribió); la corrección vive aquí, en `forense/hallazgos.md` y en `ADR-126`.

### 1.4 · Qué puede ya recalcular U2/EV-1 con esto

**(a) El cruce oficial-vs-propio SÍ es ejecutable hoy — sobre otro estimando.** Las dos filas oficiales son totales poblacionales nacionales de ENASIC 2022. El microdato que el corpus ya tiene (`enasic2022/enasic_2022_bd_csv.zip`, 6 miembros) trae `TCSDEMPO.csv` con **181 columnas, entre ellas `FAC_HOG`, `EST_DIS` y `UPM_DIS`** — el diseño complejo completo. `tools/curador_registro/produce.py::taylor_distribution` puede por tanto producir un EE propio directamente comparable contra `EE = 1 793 646.72` y `CV = 1.392 %`. **Sería la primera validación externa material del programa**, y no depende de adquirir nada más. *Reserva declarada, sin resolver aquí:* la fila oficial cuenta **personas** y el factor de esa tabla se llama `FAC_HOG`; el acto de medición debe fijar el factor correcto antes de correr, no después. Y el oficial reporta a `Niv_Conf = 90`, no 95: hay que convertir uno de los dos, con la fórmula a la vista.

**(b) El cruce pre-registrado, tal como está escrito, NO es ejecutable.** Su objeto es `P7_12_7` y el archivo oficial no lo trae (§1.2). Aplicar §5 del pre-registro *"tal cual"* exigiría sustituir la celda por la más cercana — que es exactamente lo que §7(4) de la receta prohíbe sin decirlo. Se dice.

**(c) Un criterio oficial que el programa ya puede aplicar hoy, y antes no tenía.** La ficha 922 publica los rangos de interpretación **aprobados** del CV, verbatim: *"alta [0 % - 20 %), moderada [20 % - 30 %) y baja ≥ 30 % para encuestas en unidades económicas y **alta [0 % - 15 %), moderada [15 % - 30 %) y baja ≥ 30 % para encuestas en hogares** y otras unidades distintas a las económicas."* ENASIC es encuesta en hogares. Aplicado a los números **ya sellados** de `ESP-OPACA-B-d13ec4fe` (aritmética `CV = EE/θ` sobre cifras existentes, no una estimación nueva):

| código | etiqueta | θ | EE | CV | banda oficial |
|---|---|---|---|---|---|
| 1 | De acuerdo (Sí) | 0.6932672 | 0.0105989 | **1.53 %** | alta |
| 2 | Desacuerdo (No) | 0.2995280 | 0.0105876 | **3.53 %** | alta |
| 8 | No responde | 0.0034694 | 0.0013053 | **37.62 %** | **baja** |
| 9 | No sabe | 0.0037353 | 0.0012719 | **34.05 %** | **baja** |

La θ titular (69.33 %) tiene precisión **alta** por el criterio del propio INEGI. Las dos categorías residuales caen en **baja precisión** — el `resultado.tsv` las marca hoy `ESTIMACION_SUSTENTADA` sin más. Es una etiqueta que el motor podría estar aplicando y no aplica.

---

## §2 · T2 · MANIFIESTO-49 — los payloads contados dos veces

**Contador: 0 (higiene). C3 antes → después: 49 → 0.**

### 2.1 · La lista vigente, derivada en la caja

```
$ python3 tests/corpus.py          (ANTES)
  153 WARN  (C1=104 · C2=0 · C3=49)
```

Las 49 de C3 declaran todas `raiz: descargas_mx`. La premisa del encargo sobre el `612` queda confirmada por comando y no heredada: el manifiesto tenía **612 entradas con payload bajo `data_raw`** antes de las 2 altas de T1 — ése es el número que da una caja sin corpus montado (`c3_entradas_sin_archivo` **omite** las raíces no configuradas, así que las 106 de `descargas_mx` ni se cuentan). Raíz-no-configurada, no ausencia.

### 2.2 · El diagnóstico

Las 49 entradas declaran `archivo:` con el **basename desnudo**; los 49 archivos viven en el subdirectorio **`Descargas Manuales/`** de esa misma raíz. `c3_entradas_sin_archivo` hace `os.path.exists(raíz + archivo)` → falla; `c1_huerfanos` compara la ruta relativa real contra el conjunto de `archivo` declarados → el mismo fichero, byte-idéntico, aparece como huérfano. **El mismo archivo dos veces, exactamente como el hallazgo del 18/ago decía.**

Verificado **antes** de tocar nada: para las 49, `sha256` recomputado de `Descargas Manuales/<basename>` contra el declarado → **49/49 COINCIDE**, 0 discordantes, 0 no existentes. Ni un `AUSENTE-REAL`, ni un `CORREGIR-RAIZ`, ni un `DUPLICADO`.

**Corroboración independiente.** Un segundo hilo derivó el mismo diagnóstico en paralelo, sin ver el primero, hasheando **el universo completo** (863 archivos, 3 raíces, 7.87 GB, sin acotar por tamaño) en vez de sólo los candidatos: mismas 49 rutas propuestas, `diff` = 0 diferencias, `CORREGIR-RUTA` 49 / `CORREGIR-RAIZ` 0 / `AUSENTE-REAL` 0 / `DUPLICADO` 0, y `C1` simulado 104 → 55 ejecutando el código real sobre una copia en memoria. Dos derivaciones separadas, mismo resultado.

### 2.3 · La corrección

Se antepone `Descargas Manuales/` al campo `archivo` de esas 49 entradas. **Ninguna entrada borrada** — se corrige, no se poda. Edición por línea (no el módulo `csv`, no el round-trip YAML que reformatearía 14 300 líneas), con aserción de que ningún valor nuevo introduce ` #` (el patrón que rompe este YAML) ni espacio final. `git diff --numstat` → **`49 49`**: una línea por entrada, un solo campo.

```
$ python3 tests/corpus.py          (DESPUÉS)
  55 WARN  (C1=55 · C2=0 · C3=0)

$ python3 tests/manifiesto.py --verifica          (completo)
  data_raw:     coincide=613 · no_coincide=1 · ausente=0 · sin_configurar=0
  descargas_mx: coincide=106 · no_coincide=0 · ausente=0 · sin_configurar=0
```

**C3 = 0.** Las 106 entradas de `descargas_mx` resuelven y hashean. C1 baja 104 → 55: se resuelven exactamente los 49, sin introducir ni un huérfano nuevo.

### 2.4 · El clúster `Descargas Manuales/` queda 100 % adjudicado

53 archivos físicos = **49 corregidos aquí** + **4 explicados por hash**, ninguno pendiente:

| archivo restante | qué es |
|---|---|
| `ABMex2023-Mexico-Questionnaire-V9.2.3.0-Spa-230511-W.pdf` | duplicado físico de `data_raw/lapop_abmex2023_cuestionario.pdf` (id `lapop_abmex2023_cuestionario_mexico`), sha256 idéntico |
| `ASQ Questionnaires.zip` | duplicado físico de `data_raw/wb2661_ASQ_Questionnaires.zip` (id `wb2661_asq_questionnaires`), sha256 idéntico |
| `MEX_2012-2014_ECEPIE_v01_M_v01_A_PUF (1).xml` | copia `(1)` del navegador, byte-idéntica a la entrada `mex_2012_2014_ecepie_v01_m_v01_a_puf`, que ahora sí resuelve |
| `MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta` | copia `(1)` del navegador, byte-idéntica a `mex_2023_lapop_americasbarometer_v1_0_w` |

Esto **confirma por hash** la contabilidad que `REG-LOTE3` declaró (49 registrados, 2 ya dentro, 2 duplicados byte-idénticos excluidos) y explica por qué siguen como huérfanos C1: son duplicados físicos entre raíces, que C1 por diseño **no** da por cubiertos.

### 2.5 · Fuera de perímetro, una línea

`--verifica` completo destapa **1 `NO COINCIDE` bajo `data_raw`**: `endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf` (manifiesto 2 895 872 B / `784410e6…`; disco 102 349 631 B / `a990a007…`). **No es de este acto y no es nuevo**: `forense/notas/2026-08-07-repair1.md:120` lo declara textualmente *"NO COINCIDE (dejado así, a propósito)"* y `REPAIR-1` creó para ello el id `…_dbf_redescarga`, que sí COINCIDE. Se registra la línea y se sigue.

---

## §3 · T3 · FP-17 — las descargas de la etapa 8 de FP-26

**Contador: 9 payloads nuevos al manifiesto.**

### 3.1 · Qué quedaba pendiente, leído de la ley y no de un resumen

`FP-17` está `FIRMADA` (`ADR-91`, `PR #246`) y su `ejecutada_en` declara `ACTO ADQ-15`: 89 payloads, las 15 puertas fuera de `EXISTE-NO-VERIFICADO`. Lo pendiente sale de `data/cola-adquisicion-2026-08-12.tsv` (12 filas dentro de alcance, 42 `FUERA-DE-ALCANCE-ADQ15`) y de `forense/notas/2026-08-18-adquisicion-material-15-fuentes.md` §4/§5: **siete** residuos, no uno.

### 3.2 · Resultado

| # | fuente (palanca) | resultado | qué |
|---|---|---|---|
| P1 | SERIES SPEI/CoDi (45) | **DESCARGADO** | cuadros `CF891` y `CF890` del SIE, más 2 landings |
| P2 | ENCF 2019-2024 (32) | **DESCARGADO** | olas 2019 y 2021, xlsx + manual |
| P3 | IFT SFD (41) | **DESCARGADO** | `basededatossfd.zip` íntegro |
| P4 | WB 6667 Tutores (5) | `EXIGE-CREDENCIAL` | 6 `.dta` tras login; no se creó cuenta |
| P5 | WB 870 Enterprise Survey (8) | `EXIGE-CREDENCIAL` | todo enlace de datos va a `login.enterprisesurveys.org` |
| P6 | LAOMS protesta (27) | `NO-ENCONTRADO` | el host ya NO está caído; no publica la base |
| P7 | ENAFIN microdato (49) | `NO-ACCESIBLE-INSTITUCIONAL` | Laboratorio de Microdatos |

Los 9 payloads, `9/9 COINCIDE` con **una invocación de `--verifica` por `--id`**:

| id | archivo | bytes |
|---|---|---|
| `banxico_sie_cf891_operaciones_spei` | `R3.4_Banxico_CoDi_SPEI/banxico_sie_CF891_numero_operaciones_spei_2009_2026.csv` | 335 581 |
| `banxico_sie_cf890_monto_spei` | `R3.4_Banxico_CoDi_SPEI/banxico_sie_CF890_monto_operado_spei_2009_2026.csv` | 496 547 |
| `banxico_sie_cuadro_cf891_operaciones_landing` | `…/banxico_sie_cuadro_CF891_operaciones.html` | 164 217 |
| `banxico_sie_cuadro_cf890_monto_landing` | `…/banxico_sie_cuadro_CF890_monto.html` | 163 644 |
| `banxico_encuesta_competencias_financieras_2019` | `banxico_encuesta_competencias_financieras_2019.xlsx` | 1 522 196 |
| `banxico_encuesta_competencias_financieras_2019_manual` | `…_2019_manual.pdf` | 624 237 |
| `banxico_encuesta_competencias_financieras_2021` | `banxico_encuesta_competencias_financieras_2021.xlsx` | 1 555 601 |
| `banxico_encuesta_competencias_financieras_2021_manual` | `…_2021_manual.pdf` | 258 473 |
| `ift_sfd_base_de_datos_zip` | `ADQ15_IFT_SFD_uso_confianza/basededatossfd.zip` | 4 660 022 |

### 3.3 · Tres cosas que este tramo midió y no venían en el encargo

**(a) La serie SPEI es DIARIA, no mensual, y no se obtiene por `GET`.** 6 444 líneas, 01/01/2009–03/08/2026, seis aperturas (total, `<8 mil`, `8 mil–300 mil`, `>300 mil`, bajo valor, alto valor). La vía `GET` con `idCuadro` sólo entrega un *snapshot* de 3 días sin JS — **es la misma limitación que `ADQ-15` documentó para los cuadros CoDi `CF884`/`CF885`**, y explica por qué aquel acto se quedó con el lado CoDi. El `POST` a `consultarDirectorioInternetAction.do?accion=consultarSeries` con `anoInicial`/`series[]`/`formatoCSV` trae la serie histórica completa. Por eso se registran también los dos landings de cuadro: el CSV no tiene URL `GET` persistente y el landing es su única ancla de procedencia estable.

**(b) A.7 sobre el CSV del SIE: varía UNA línea, y se nombra.** El `sha256` crudo cambia entre corridas por la **línea 7**, `"Fecha de consulta: DD/MM/AAAA hh:mm:ss"`. Excluida esa línea el contenido es idéntico. El hash registrado es el del archivo tal como quedó en el corpus, que ya no cambia; queda escrito en el `nota:` de la entrada para que una re-descarga discordante **no** se lea como corrupción. Es el corolario de A.7 aplicado tal cual: identificar *qué campo* varía antes de concluir nada.

**(c) El ZIP del IFT, que `ADQ-15` no consiguió en 11 intentos, llegó íntegro al primero — y aun así se validó estructura antes de comparar hash.** Ese acto midió que `www.ift.org.mx` sirve archivos **truncados con hash repetible** (un PDF en 4 979 926 B sin `%%EOF`, el mismo objeto en 8 084 499 B a la segunda). Aquí: `zipfile.testzip()` limpio, un solo miembro (`Base de datos/Bases_de_datos_Servicios_Financieros_Digitales (SFD).xlsx`, 5 235 099 B, 2 hojas), y **tres** descargas byte a byte idénticas — la tercera corrida por el supervisor y no por el ejecutor. Sin truncamiento.

### 3.4 · Los cuatro no conseguidos, con universo A.4 (fecha 2026-08-19)

- **WB 6667** — 8 intentos (catálogo, `get-microdata`, DDI, JSON, 4 rutas `/download/F1`). La página declara *"Login to access data — user must be logged in"*; las rutas directas dieron 404 o HTML público sin enlace de archivo. `EXIGE-CREDENCIAL`. **No se creó cuenta ni se entregó dato personal.**
- **WB 870** — 4 intentos. Los cuatro enlaces de datos de `/en/data` apuntan a `login.enterprisesurveys.org/en/signin`, página de firma real y verificada. `EXIGE-CREDENCIAL`. **No se creó cuenta.**
- **LAOMS** — 8 `GET`, **los 8 `200`** (portada, categoría de eventos de protesta, página completa del proyecto, 4 subdominios temáticos, página de descargables). **El host ya no está caído**: contradice los 7 intentos con `curl 35`/`curl 52` del 18/ago. Pero la página del proyecto describe la base como accesible *"mediante una plataforma tecnológica"* sin publicar enlace, los subdominios son foros y "descargables" sólo tiene libros. `NO-ENCONTRADO` — no `HOST-NO-RESPONDE`, que hoy sería falso, ni `DESCARGADO`, que no hay archivo. No se consultó `web.archive.org`: no hizo falta, el sitio vivo respondió.
- **ENAFIN** — verificación, no descarga (por instrucción). Catálogo RNM 1106, pestaña *Get Microdata*: único recurso, *"Solicitud de acceso a los microdatos en las instalaciones del productor"*. Restricción institucional **vigente hoy**. `NO-ACCESIBLE-INSTITUCIONAL`: no es una falla de descarga.

**En ningún intento del acto hizo falta desactivar el sandbox.** Los cinco hosts que `ADQ-15` daba por bloqueados o caídos respondieron `200` directo. La lista blanca cambió desde el 18/ago — mismo patrón que `P·LOTE-2` documentó con `zenodo.org`/`osf.io`. Es un hecho de infraestructura, no un logro de método, y la lección es la contraria a la que parece: **un bloqueo de host es un hecho fechado sobre un agente, no una propiedad de la fuente.**

### 3.5 · ¿Queda ejecutada la etapa 8 de `FP-26`?

**Sí, en todo lo alcanzable sin credencial ni convenio institucional — y no, si «ejecutada» se lee como «los siete residuos resueltos».** Se dice con las dos mitades: los tres residuos que eran **fallas de descarga** están resueltos (SPEI, ENCF, IFT); los cuatro restantes **no son fallas de descarga** — dos exigen cuenta de usuario, uno exige convenio con INEGI y uno no publica el dato. Ninguno se resuelve bajando otra vez.

### 3.6 · Perímetro, declarado

`data/cola-adquisicion-2026-08-12.tsv` **no está en el perímetro de este lote** y **no se editó**. Consecuencia dicha, no ocultada: sus columnas `estado_adquisicion_ADQ15` quedan caducas para las palancas **32**, **41** y **45**. El registro material vive en `data/manifiesto.yaml` y en `ejecutada_en` de `FP-17`.

---

## §4 · T4 · Los 3 PDFs `REFERENCIADO-NO-ABIERTO`

**Contador: 0 payloads — pero SÍ hay hallazgo sustantivo (§4.3).**

### 4.1 · Los tres abren, y su identidad es triple

`data/censo-explotacion-2026-08-17.tsv` tiene **4** filas `REFERENCIADO-NO-ABIERTO`; **3 son pdf** (474, 617, 623). La cuarta (línea 74, `cses5_modulo5_2016_2021_cuestionario`) es `.txt` y queda **fuera del perímetro**: el encargo dice filas pdf. No se tocó.

**No se usó `pdfinfo` como oráculo de cifrado** — es el hallazgo de los 83 falsos `PDF_CIFRADO`. El oráculo fue extraer texto de verdad:

| id | páginas | líneas | caracteres | `pdftotext -layout` |
|---|---|---|---|---|
| `f00006635_wvs7_questionnaire_mexico_2018_spanish` | 7 | 449 | 59 118 | exit 0 |
| `za5900_q_mx` | 7 | 553 | 36 019 | exit 0 |
| `za6980_q_mx` | 7 | 542 | 38 190 | exit 0 |

`sha256` real del archivo en disco = columna 12 del censo = `data/manifiesto.yaml`, **triple coincidencia en los tres**. (`ZA5900_q_mx.pdf` lo marca `file` como *"zip deflate encoded"* — es compresión, no cifrado; extrae limpio.)

### 4.2 · Veredictos A.4, por necesidad

| id | veredicto de fila | estado nuevo (col. 8) | por qué |
|---|---|---|---|
| `f00006635_wvs7_…` | `EXISTE-NO-SATISFACE` | `REFERENCIADO-NO-ABIERTO` → **`ABIERTO-SIN-HALLAZGO`** | N15/`G6.deferencia`: ya sellado `EXISTE-NO-SATISFACE` por `COEF-UNIVERSO` (`coef-universo-v1_0.tsv` fila 37). N5/`G3.horizonte_temporal`: probado **por primera vez aquí**, también `EXISTE-NO-SATISFACE` |
| `za5900_q_mx` | `EXISTE-SATISFACE` | → **`EXPLOTADO`** | N13/`familismo_obligacion` con cita textual (línea 139) |
| `za6980_q_mx` | `EXISTE-SATISFACE` | → **`EXPLOTADO`** | N13, N30 y N12 con cita textual (líneas 183, 163-165, ítem 8) |

Las citas, verbatim del texto extraído en esta sesión:

- ZA5900, línea 139 (ítem 7f): *"Los hijos adultos son una importante fuente de ayuda para los padres ancianos"* — batería de acuerdo/desacuerdo 1-5.
- ZA6980, línea 183 (ítem 13a): *"Los hijos adultos tienen el deber de cuidar a sus padres ancianos"* — el que `forense/hallazgos.md` llama el ítem de obligación normativa más directo de todo `APERTURA-ISSP`.

**Todo negativo, con universo y con control positivo en el mismo archivo y el mismo comando:**

- **N5 en WVS7**: `plazo` 0 · `planea` 0 · `planific` 0 · `porvenir` 0 · `paciencia` 0 · `largo plazo` 0. Control positivo `obedien` → 1 acierto (el ítem 17 que `COEF-UNIVERSO` ya había hallado). Los únicos candidatos son el ítem **13 "Ser ahorrativo con el dinero"** (batería Inglehart de cualidades del niño: es un valor de crianza) y el ítem **286 "¿Durante el último año su familia pudo ahorrar…?"** (situación financiera retrospectiva del hogar). Ninguno operacionaliza horizonte temporal ni descuento → `EXISTE-NO-SATISFACE`, no `NO-ENCONTRADO`: los ítems existen, no satisfacen.
- **N30 en ZA5900**: `confia` · `confía` · `confío` · `confianza` · `se puede confiar` · `desconocid` · `extrañ` · `la mayoría de la gente` → **0 aciertos los ocho**, sobre las 553 líneas íntegras. Control positivo `hijos adultos` → 1 acierto, mismo archivo y mismo comando.
- **N28 en ZA6980**: `monitore` 0 · `sancion` 0 · `coopera` 2 (ninguno sustantivo: catálogo de organizaciones). Control positivo `confia` → 7.

Coincide con la adjudicación ya sellada por `APERTURA-ISSP` (`data/apertura-issp-variables-2026-08-13.tsv`), fila por fila y razón por razón — incluida la de N12 en ZA5900 (*"las únicas coincidencias de apoyo/ayuda pertenecen íntegramente a la batería de cuidado a personas mayores, ya contabilizada en necesidad 13"*). Dos lecturas independientes del mismo PDF, mismo resultado.

### 4.3 · El hallazgo: el estado estaba **caduco antes de escribirse**

`ACTO APERTURA-ISSP` (`PR #200`, commit `0582650`, **2026-08-12**) abrió y citó **por página** los dos cuestionarios ISSP: su propio `universo_declarado` dice `"cdb pp.79,99,101,103 + q_mx pp.2-3 (español) via pdftotext -layout"`, y `forense/notas/2026-08-13-apertura-issp.md:277` dice que N12 y N14 se resolvieron *"leyendo `reader.variable_labels()` del propio `.dta` más el cuestionario en español (`za6980_q_mx`)"*. **Cinco días antes** del censo del 17/ago que los marca `REFERENCIADO-NO-ABIERTO`.

La causa está en la propia columna 9 de esas filas: el `universo_declarado` enumera **cuatro archivos** — `manifiesto.yaml + relaciones.tsv + abrir4-variables-2026-08-08.tsv + verif3-variables-2026-08-08.tsv` — y **no incluye** `data/apertura-issp-variables-2026-08-13.tsv` ni `reapertura-52a-54-variables-2026-08-13.tsv`, que ya estaban en `main`. El censo no concluyó de más sobre el mundo: concluyó exactamente lo que su universo permitía, y el universo estaba desactualizado. Es la misma clase de defecto que `ADR-67(b)` elevó a doctrina — *la conclusión de un cierre no puede ser más ancha que su universo declarado* — sólo que aquí el universo se quedó corto por no re-derivarse.

Consecuencia medible: la cifra `REFERENCIADO-NO-ABIERTO = 4` que ese censo exhibía estaba inflada en 2 desde el día en que se escribió.

### 4.4 · Fuera de perímetro, una línea

La columna 8 del mismo censo tiene **77 filas con `PRESENTE-INTEGRO`**, un valor del eje de integridad (columna 14) usado en la columna de explotación. Son exactamente los payloads nuevos entre el censo del 13/ago y el del 17/ago: se les copió un valor de integridad en vez de correr la clasificación de explotación. No toca a las 3 filas de este acto y **no se corrige aquí** (fuera de perímetro); queda la línea.

---

## §5 · T5 · `variable_id` para las 21 co-observables

**Contador: 0 (no se midió nada). Exposición resuelta 21 de 21; desenlace resuelto 16, candidato fuera de dominio 2, `NO-ENCONTRADO-EN-CODEBOOK` 3.**

### 5.1 · El hueco de esquema: no lo había

El encargo preveía la posibilidad de que el esquema no admitiera columna y exigía reportar el hueco antes de inventar. **No hay hueco.** `data/coef-universo-v1_0.tsv` no lo valida ningún test: `T23` valida `data/cableado-universo-v1_0.tsv`, que es otro archivo, y `command grep -rn "coef-universo" tests/*.py` → 0 coincidencias. Se añaden cuatro columnas — `variable_id_exposicion`, `variable_id_desenlace`, `variable_id_estado`, `variable_id_evidencia` — sin tabla puente. `git diff --numstat` → `51 51`; 13 columnas en las 51 filas; `T23 T-CABLEADO` → `[ ok ]` bajo `--require-cableado`.

### 5.2 · El resultado

| línea | coef_id | exposición | desenlace | estado |
|---|---|---|---|---|
| 7 | `N12/G5.familismo_apoyo` | `cuid_may1..cuid_may7` | — | RESUELTA-PARCIAL |
| 10 | `N7/G3.familismo_apoyo` | `P9_8_1..P9_8_6` | `P5_1_5` (tanda) | RESUELTA |
| 13 | `N13/G5.familismo_obligacion` | `tarea_dom`/`hora_dom`/`compa_dom`/`paren_dom`/`inst_dom` | `nivela_pe` | RESUELTA |
| 15 | `N8/G4.exposicion_violencia` | `AP7_3_09..AP7_3_14` | `BP1_23` | RESUELTA |
| 16 | `N8/G4.exposicion_violencia` | `AP7_3_10..AP7_3_14` | `BP1_23` | RESUELTA |
| 17 | `N8/G4.exposicion_violencia` | `AP7_3_10..AP7_3_14` | `BP1_23` | RESUELTA |
| 18 | `N8/G4.exposicion_violencia` | `AP7_3_10..AP7_3_15` | `BP1_23` | RESUELTA |
| 21 | `N9/G4.confianza_institucional` | `AP5_4_01,02,03,05,06,07,11` | `BP1_23` | RESUELTA |
| 22 | `N9/G4.confianza_institucional` | `AP5_4_1..AP5_4_9` | `BP1_23` | RESUELTA |
| 26 | `N8/G4.exposicion_violencia` | `P4_01..P4_13` | `P12_01..P12_13,P12_99` | RESUELTA |
| 27 | `N8/G4.exposicion_violencia` | `P4_01..P4_13` | `P12_01..P12_13,P12_99` | RESUELTA |
| 28 | `N8/G4.exposicion_violencia` | `P3_1..P3_10` | `P7_{X}_1..P7_{X}_8` × 10 | RESUELTA |
| 32 | `N14/G5.radio_confianza` | `PB1_01`/`PB1_02`/`PB2_1`/`PB2_2` | `PA1` / `PA3_03` | RESUELTA |
| 33 | `N15/G6.deferencia` | `P44A` | — | RESUELTA-PARCIAL |
| 35 | `N1/G1.confianza_institucional` | `P11_1_22` **(corregido)** + `P8_3_1..3` | `P8_6`/`P8_7` (fuera de dominio) | RESUELTA-PARCIAL |
| 38 | `N13/G5.familismo_obligacion` | `CUID_ESP_INT_HOG_CON_CP` | `NIV`/`GRA` | RESUELTA |
| 41 | `N15/G6.deferencia` | `d0901a..k` / `d0902` | `d0601a..g` (fuera de dominio) | RESUELTA-PARCIAL |
| 42 | `N2/G1.radio_confianza` | `Q15_2_mean_people` | `in_admin` / `Q21_3_comp` | RESUELTA |
| 43 | `N1/G1.confianza_institucional` | `Q15_2_mean_formal` | `in_admin` / `Q21_3_comp` | RESUELTA |
| 45 | `N10/G4.horizonte_temporal` | `impatient_now` / `present_bias_dum` | — | RESUELTA-PARCIAL |
| 46 | `N13/G5.familismo_obligacion` | `P4_2..P4_10` (9 ítems) | `P7_2` / `P7_3` | RESUELTA |

Las 29 filas con `co_observacion` distinto de `S` quedan `NO-DERIVADO-FUERA-DE-T5`: es alcance, no veredicto. Los tres `NO-ENCONTRADO-EN-CODEBOOK` de desenlace (líneas 7, 33, 45) llevan su universo A.4 en la columna de evidencia: archivo abierto, cuántos campos/hojas examinados, término buscado, fecha.

### 5.3 · Tres hallazgos, uno de ellos material

**(a) `P11_1_23` no existe en ENCIG 2017; `P11_1_22` sí, y es el mismo concepto** — verificado por el supervisor, no sólo reportado: `pdftotext -layout encig17_estructura_base_datos.pdf` + `command grep -c` sobre 4 983 líneas → `P11_1_22` **1**, `P11_1_23` **0**, `P11_1_21` **1** (control positivo). Es el ítem consecutivo **38** de la batería `P11_1_1..22`, etiqueta *«Servidores públicos o empleados de gobierno»*, escala 1 *Mucha confianza* … 4 *Mucha desconfianza*, más 5/9. El negativo que traía `universo_declarado` era **cierto sobre el mnemónico y falso sobre el concepto** — y la propia fila declaraba honestamente no haber revisado el mnemónico alterno. Defecto material corregido.

**(b) `BP1_23` no mide lo que su glosa de canon dice.** Leído del `diccionario_de_datos_tmod_vic_envipe2025.csv` dentro de `envipe2025_csv.zip`: `BP1_20` = *«Denuncia ante el MP o Fiscalía Estatal»*, **`BP1_23` = «Razón principal de la no denuncia»**, `BP1_28` = *«Razón principal de denuncia ante el MP»*. Etiqueta estable en las cuatro olas revisadas (2013/2017/2018/2025). `forense/censo-estimabilidad-coeficientes-v1_1.md` filas 8 y 9 lo glosan como `comunicacion.inseguridad.ver_oir_callar` con «limitación estructural declarada»; `canon/modelo-decision-v4_0.md:236` ya registra que `PR #57` retiró esa familia de `H-12` porque *«medía conducta de denuncia, no exposición»*. Esto **no contradice** al canon: **precisa** cuál es la limitación, con cita textual — que es exactamente lo que el hallazgo de `COEF-UNIVERSO` pedía para el siguiente lote. La variable queda escrita como desenlace en las seis filas que la usan, **con su condicionamiento a la vista** (sólo aplica a quien no denunció), no en silencio.

**(c) El «núcleo» `AP7_3` no es el mismo subconjunto entre sesiones.** La línea 15 (2025) usa `09-14`, las 16/17 (2018/2017) usan `10-14`, la 18 (2013) usa `10-15` — tres operacionalizaciones distintas del mismo constructo, cada una confirmada contra el codebook de su propia ola, sin que ninguna sesión las haya reconciliado. Relevante para cualquier estimación longitudinal futura. No se reconcilia aquí.

Corrección menor, registrada: la fila 28 (MOCIBA 2015) enumeraba en prosa **siete** acciones de la batería de desenlace y omitía la primera (`P7_X_1` = *«Bloquear a la persona»*); su propia notación compacta `P7_X_1..P7_X_8` ya tenía el conteo correcto de ocho.

### 5.4 · Lo que T5 NO hace

No mide. No adjudica ningún coeficiente. No resuelve la tensión `N1/G1.confianza_institucional` entre la línea 35 (dominio corrupción gubernamental) y la 43 (dominio confianza financiera) — dos payloads candidatos para el mismo nodo, en dominios opuestos: declarado, no resuelto. No sella `P11_1_22` como operacionalización. No abre microdato más allá del codebook o del header.

---
## §6 · Cierre del lote

### 6.1 · Tabla T1–T5 y contadores

| tarea | qué se hizo | contador | PARO |
|---|---|---|---|
| **T1 · U2-ADQ** | Adquiridos y registrados con `sha256` los 2 recursos de precisión de la ficha RNM 922 (ENASIC 2022). A.7 doble descarga idéntica; A.1 una invocación por `--id`, las dos `COINCIDE` | **2 payloads** | no |
| **T2 · MANIFIESTO-49** | Las 49 entradas `C3` corregidas por prefijo de ruta, con `sha256` verificado antes de tocar nada; ninguna entrada podada | **0** (higiene) · **C3 49 → 0** | no |
| **T3 · FP-17** | 3 de los 7 residuos ejecutados (SPEI, ENCF 2019/2021, ZIP del IFT); los 4 restantes nombrados por su barrera real | **9 payloads** | no |
| **T4 · 3 PDFs** | Los 3 abiertos con `pdftotext`, veredicto A.4 por necesidad, estado actualizado en el censo | **0** · 1 hallazgo sustantivo | no |
| **T5 · variable_id** | 4 columnas nuevas en `coef-universo`; exposición resuelta **21/21**, desenlace 16 resueltos · 2 fuera de dominio · 3 `NO-ENCONTRADO-EN-CODEBOOK` | **0** | no |

**Ninguna tarea paró.** Total de payloads nuevos al manifiesto: **11** (2 de T1 + 9 de T3). **Contadores de medición sobre México: cero** — este acto adquiere, sanea y nombra variables; no corre ninguna estimación nueva.

**`corpus.py` C3, antes → después: `49 → 0`.** El total de WARN de ese script baja de **153** (`C1=104 · C2=0 · C3=49`) a **55** (`C1=55 · C2=0 · C3=0`).

### 6.2 · Suite, salidas crudas

```
$ python3 tests/corpus.py
  [ ok ]  C2 duplicado por contenido
  [ ok ]  C3 entrada sin archivo

  55 WARN  (C1=55 · C2=0 · C3=0)
  Ninguna comprobación de este script emite FAIL: no gatea nada,
  no toca tests/baseline.json, no tiene --freeze.
```

```
$ python3 tests/check.py --baseline
════════════════════════════════════════════════════════════════════════
  21 FAIL · 123 WARN
════════════════════════════════════════════════════════════════════════

────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
  (1 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
────────────────────────────────────────────────────────────────────────
```

**Sin `--freeze`.** `tests/baseline.json` no se tocó. `T23 T-CABLEADO` → `[ ok ]` bajo `--require-cableado`.

**Recifrado, con las dos causas nombradas:** el neto es cero y no por inercia — `FP-67` sale de `ABIERTA` (−1 WARN de `T22`) y `FP-70` entra `ABIERTA` (+1). `FP-17` recibe `ejecutada_en` complementada sin salir de `FIRMADA`, así que no mueve el conteo. `T15` sube de 125 a 126 ADR.

**Un defecto de forma, medido dentro del propio acto:** el marcador `{cita-historica}` **no se reconoce si va fuera de las negritas**. `**124 → 125 ADR**{cita-historica}` deja el `FAIL` de `T15` vivo; `**124 → 125 ADR{cita-historica}**` lo cierra. La causa está en el código: `MARCA_HISTORICA = r"`?\s*\{cita-historica\}"` tolera un backtick opcional antes de la marca, no un `**`. El precedente correcto ya estaba en `gobernanza:2492`; esta redacción lo reprodujo mal a la primera y lo corrigió por la corrida, no por lectura.

### 6.3 · Cascada

`ADR-126` (número derivado al escribir contra `origin/main = b4a9b3f`, máximo `125` sin huecos ni duplicados; **se re-deriva al fusionar**) · `FP-67` → `CERRADA` · `FP-17` → `ejecutada_en` complementada · `FP-70` → nueva, `ABIERTA` · `forense/hallazgos.md` +8 líneas · `canon/estado-programa-v1_10.md` cabecera, `L0` y bloque de suite · `canon/gobernanza-v1_15.md` cabecera de conteo · encargo **CONSUMIDO**.

### 6.4 · Lo que queda abierto, dicho

1. **`FP-70`** — el objeto del cruce de `U2/EV-1`: correrlo sobre los dos totales nacionales (ejecutable hoy), declararlo sin objeto, o mantenerlo vivo. Con dos reservas que cualquier opción debe resolver: `Niv_Conf` 90 contra IC95, y el factor correcto (`FAC_HOG` en una fila que cuenta personas).
2. **El censo `2026-08-17` no se regenera aquí.** Sus 3 filas pdf quedan al día; las 77 filas con `PRESENTE-INTEGRO` en la columna de explotación y la 4ª fila `REFERENCIADO-NO-ABIERTO` (`.txt`) quedan fuera de perímetro.
3. **`data/cola-adquisicion-2026-08-12.tsv`** queda caduca para las palancas 32, 41 y 45 — fuera de perímetro, dicho y no corregido.
4. **`BP1_23`**, la tensión `N1/G1` entre las líneas 35 y 43, y la falta de reconciliación del núcleo `AP7_3` entre olas: nombradas, no adjudicadas.
5. **`endireh_2016_bd_mujeres_endireh2016_sitioinegi_dbf`** sigue `NO COINCIDE` — así lo dejó `REPAIR-1` a propósito, con su `…_redescarga` al lado.

### 6.5 · La pregunta de cierre de `AGENTS.md`

> ¿El proyecto quedó más cerca de producir una explicación, medición, decisión o modelo mejor?

**Sí, por tres vías distintas.** (1) La primera validación externa del programa dejó de estar bloqueada por adquisición: el insumo oficial está en el corpus con hash, y lo que falta es una decisión de mesa sobre su objeto, no una descarga. (2) El manifiesto dejó de contar 49 payloads dos veces y la etapa 8 de `FP-26` avanzó lo que se podía avanzar sin credencial. (3) Las 21 co-observables del cableado ya nombran una variable con su etiqueta de codebook citada — el siguiente lote de medición ya no tiene que adivinarlas, que era exactamente la consecuencia operativa que `COEF-UNIVERSO` había medido y dejado abierta.
