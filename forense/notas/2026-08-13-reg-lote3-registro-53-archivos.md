# REG-LOTE3 · registro del lote de 53 archivos en `descargas_mx/Descargas Manuales`

**2026-08-13 · worktree `/home/pc0/mm-reg-lote3` (rama `reg-lote3`, base `origin/main` @ `1cb6e3e`, PR #219)**

## 0 · ARRANQUE

- Dos clones existentes: `/home/pc0/Modelado-Mexicano` (canónico, hub de worktrees, sin `descargas_mx`) y `/home/pc0/proyectos/Modelado-Mexicano` (diverge 580/873 commits de `origin/main`, orphan ya señalado en memoria de sesión). Ninguno de los dos se usó directamente: se creó un worktree nuevo, `mm-reg-lote3`, desde `origin/main` real en el clon canónico — patrón worktree-por-tarea del proyecto.
- `origin/main` = `1cb6e3e` (PR #219, TRIAGE-63) en ambos clones tras `git fetch`; sin divergencia con lo que memoria de sesión ya tenía. Baseline declarado `3d0d1e5` (ADR-76(f)) verificado `--is-ancestor` de `origin/main`: sí.
- `data/raw` estaba AUSENTE en el worktree nuevo (worktrees no heredan symlinks no versionados de otros worktrees) — se enlazó a `/home/pc0/mm-corpus/raw`, mismo destino que el resto de worktrees.
- `data/raices.local.yaml` (gitignorado) tampoco existía — creado con las tres raíces (`data_raw`/`descargas_mx`/`downloads`), mismo patrón que `mm-reapertura-52a-54`.
- Entorno: `$CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacío, `curl` a INEGI → 200, `ls data/raw/` → contenido real. CAJA, no nube.
- `git worktree add` chocó dos veces con `error: could not write config file .git/config: Device or resource busy` (contención conocida de este equipo, ya documentada en memoria de sesión) — el worktree se creó igual; el tracking de rama no quedó configurado (push posterior debe usar `-u` explícito y verificarse por `gh`/`ls-remote`, no por texto de CLI).

## 1 · Verificación de premisas (ADR-39) — la cifra y la ventana horaria del encargo

El encargo declaraba "53 archivos... creados 13:33–13:40" como medición de INV-DESCMX. Verificado directo contra disco (`ls -la --time-style=full-iso` sobre `descargas_mx/Descargas Manuales/`, comando a la vista):

- **Conteo: 53 confirmado independientemente** (`ls -la | wc -l` → 56 líneas − 1 "total" − 2 `.`/`..` = 53; listado completo enumerado y contado a mano, coincide).
- **Ventana horaria: NO se sostiene para el lote completo.** Los mtimes reales caen en **tres** clústeres, no uno: 12:00:47–12:04:26 (22 archivos, IEPEP/LFEPIE/ECEPIE de Banco Mundial + AGEs + reporte de síntesis), 12:58:06–13:03:27 (4 archivos, Mass Mobilization + OECD Trust Survey + un .xls sin identificar), y 13:29:53–13:41:41 (25 archivos, LAPOP/GPS/openICPSR/CNGMD-tool/PILP). Solo el tercer clúster cae dentro de "13:33–13:40"; los otros dos son 30–90 minutos anteriores. Esto **no cambia la acción** (el proceso de registro es dedup-seguro por sha256 independientemente de qué clúster sea "el nuevo"), pero la premisa de ventana horaria del encargo era imprecisa — se reporta como ADR-39 exige, no se ajusta el texto para que cuadre.
- `tests/manifiesto.py --escanea descargas_mx` (sin subcarpeta) confirmó además la advertencia del propio encargo: escanea la RAÍZ (`/mnt/c/Users/PC0/Descargas MX`), no la subcarpeta — 69 archivos en raíz, 7 nuevos, **ninguno del lote de 53** (7 archivos sueltos de una tanda ENSANUT anterior, ajenos a este acto, no tocados).

## 2 · Vía admisible usada

Del encargo: "apuntar la raíz a la subcarpeta durante el acto y restaurarla al cerrar, o aplanar". Se usó la **primera** — `data/raices.local.yaml` (gitignorado, no toca código) redirigido temporalmente a `.../Descargas MX/Descargas Manuales` durante el registro, **restaurado a `.../Descargas MX` antes de cerrar** (confirmado con una corrida final de `--escanea`: vuelve a ver los 69/7 de la raíz, no la subcarpeta).

## 3 · Conteo derivado y duplicados

53 en disco − 2 ya registrados antes de este acto (`ABMex2023-Mexico-Questionnaire...` → `lapop_abmex2023_cuestionario_mexico`; `ASQ Questionnaires.zip` → `wb2661_asq_questionnaires`, ambos de 2026-08-03/08-12) = **51 nuevos**.

De los 51, **2 son duplicados byte-idénticos** (verificado `sha256sum` directo, comando a la vista) de otro archivo del mismo lote, dejados **fuera de todo `--grupo`** a propósito (nunca promovidos):
- `MEX_2012-2014_ECEPIE_v01_M_v01_A_PUF (1).xml` ≡ `...PUF.xml` (mismo sha256 `714056e1...`)
- `MEX_2023_LAPOP_AmericasBarometer_v1.0_w (1).dta` ≡ `...w.dta` (mismo sha256 `4a9410a5...`)

Verificado después del registro: una corrida de `--escanea` sobre la subcarpeta reconoce ambos como `ya registrados` bajo el id de su gemelo — el mecanismo de dedup por hash del propio script confirma la exclusión, no hace falta código nuevo.

**49 archivos registrados** en `data/manifiesto.yaml` (582 → 631 entradas).

## 4 · Grupos identificados, con evidencia (no de memoria del nombre de archivo)

Se verificó dry-run (`fnmatch` en Python sobre los 51 nombres reales) que los 27 patrones usados cubren exactamente los 49 archivos objetivo, una vez cada uno, cero colisiones, antes de tocar el manifiesto.

| Grupo | Evidencia de identificación |
|---|---|
| `wb1039_iepep_puf` (9: PUF + 4 AGEs + síntesis) | `Mexico_SynthesisReport.pdf` abierto con `pdftotext`: "Impact Evaluation of a Parental Empowerment Program in Mexico... Harry Anthony Patrinos" = catálogo 1039 exacto (fila 109 del puntero). AGEs (Alumnos/Directores/Maestros/Padres) = battery AGE/APF del mismo programa. |
| `wb2049_lfepie_puf` (5) | Nombre de archivo + `ddi-documentation...-2049.pdf` coincide con fila 108 |
| `wb2661_ecepie_puf` (6) | Ídem, fila 98; `ASQ Questionnaires.zip` ya registrado confirma el catálogo |
| Mass Mobilization (2) | `MM_users_manual_0515.pdf` abierto con `pdftotext`: "Mass Mobilization Data Project — Codebook and User's Manual — Clark & Regan, May 2015". `dataverse_files.zip` es el nombre genérico que Harvard Dataverse da a un export de "Access Dataset" — coincide con fila 104 (bloqueada AWS WAF para el agente) |
| OECD Trust Survey (1) | `ea3385cf-en.pdf` abierto con `pdftotext`: "OECD Survey on Drivers of Trust in Public Institutions in Latin America and the Caribbean, 2025 Results" — coincide con fila 114 (bloqueada Cloudflare para el agente) |
| openICPSR proj116334 (2) | `116334-V1.zip` listado con `zipfile` (sin `unzip` disponible en la caja): árbol `Compartamos_AEJ/...` — RCT de microcrédito Compartamos, coincide exacto con fila 110 (número de proyecto en la URL) y con los gaps `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT`/`..._RANDOMIZED_..._PLACEMENT_EXP` (filas 77/78). `LICENSE.txt` (BSD + CC BY 4.0, copyright AEA 2015) es la licencia estándar de paquetes de réplica AEA/openICPSR, mismo timestamp (segundos de diferencia) |
| LAPOP por ola (9 subgrupos, 21 archivos) | Ola 2004/2006: prefijo numérico de asset-id de CMS, sin coincidencia limpia con la convención de nombre "ABMexNNNN..." ya registrada — URL exacta NO reclamada, solo la página general. Olas 2018-19/2019/2021/2023 con prefijo `ABMex`/`ABMEX`/`MEX_`: 4 de ellas siguen el mismo patrón exacto de nombre de archivo que la entrada YA registrada `lapop_abmex2023_cuestionario_mexico` (`vanderbilt.edu/lapop/mexico/<archivo>`) — URL derivada por ese precedente, declarada como tal (no re-verificada por fetch) |
| GPS (3) | `GPS_Dataset.zip`/`GPS_Questionnaires.zip`/`GPS_dataset_country_level.zip` — coinciden con la fila 99 y con la nota YA registrada de `gps_do_files_country_level` en el manifiesto: "el dataset real... exige el formulario 'Dataset', enviado en esta sesión, entrega pendiente por correo" (2026-08-12). **Este lote ES esa entrega** |
| CNGMD tool (1) | `DescargaMasiva_1382026_134046.zip` contiene `DescargaMasivaOD.xml` con URLs reales `inegi.org.mx/contenidos/programas/cngmd/2023/datosabiertos/...` — coincide con fila 106 (ya `EXISTE-SATISFACE`); es la herramienta oficial de descarga masiva, no el payload |
| PILP workbook (1) | `MEX_PILP_TB_v1.xlsx` — instalado `xlrd` vía venv (no disponible por defecto) **falló** (`python3-venv` ausente en el sistema, `pip install --break-system-packages` no intentado por no forzar el entorno administrado); identificado en cambio vía `docProps/core.xml` (autoría: Florencia Rebolledo, creado 2024-04-02) + primeras `sharedStrings` del propio xlsx (sin necesitar `xlrd`): primera cadena literal "Tandas para bienestar", hoja `TB_d` — coincide con fila 28 (`Tandas_para_el_Bienestar`, portal oficial caído). **No es el portal**: es una compilación de tercero citando "Cuenta Pública" como fuente. Registrado sin `url_origen` |
| `DataDetails.xls` (1) | **Sin identificar.** Metadata OLE (`file`): autor "Minh Nguyen", último editor "Ziad Ghandour", creado 2010-05-13. `strings`/`xlrd` no disponibles (mismo bloqueo de herramientas que PILP). Registrado como inventario puro, sin `url_origen` ni `usado_para` — pendiente para un acto que tenga `xlrd`/LibreOffice disponible |

## 5 · Defecto reencontrado: `_formatear_entrada_staging` corrompe YAML con valores largos

Ya señalado por la nota de P·Lote-1 (2026-08-12) para `--escanea`+`--grupo` repetido sobre el mismo `--grupo`. Esta sesión **diagnosticó la causa raíz**: `_yaml_valor()` (`tests/manifiesto.py:587`) usa `yaml.safe_dump(..., default_flow_style=True)` **sin fijar `width`** — PyYAML envuelve escalares largos (`usado_para`/`url_origen` > ~80 caracteres) a la anchura por defecto, insertando un salto de línea que rompe la línea `f"  campo: {valor}"` armada a mano. Confirmado reproduciendo el traceback (`yaml.scanner.ScannerError`) con un `--usado-para` de ~200 caracteres.

**Workaround sin tocar código** (el perímetro de este acto es datos, no scripts): 27 ciclos `--escanea`/`--promueve` corridos **sin** `--url`/`--usado-para` largos (patrones únicamente, verificados sin colisión antes de ejecutar) → 49 entradas promovidas con `url_origen="no determinada"` por defecto → parche posterior de `url_origen`/`usado_para`/`url_origen_procedencia` **vía las funciones propias del módulo** (`import tests/manifiesto.py as m; m.leer_manifiesto/m.escribir_manifiesto`), el mismo camino seguro que usa `--promueve` para escribir el archivo final (`yaml.dump` con `_str_presenter`, que sí pliega correctamente prosa larga con `>`/`|`). Cero texto YAML tecleado a mano; cero cambio a `tests/manifiesto.py`. La corrupción del archivo staging (ocurrió una vez, sobre `wb1039_puf`) se recuperó con `git checkout -- data/manifiesto-staging.yaml` (archivo trackeado, derivable, sin pérdida real).

## 6 · Verificación hash (A.1 — una invocación por `--id`)

49 invocaciones separadas de `--verifica --id <id>`, sin colapsar categorías: **49 COINCIDE · 0 AUSENTE · 0 raíz-no-configurada · 0 hash-discordante**. (El reporte de cada invocación imprime además, por diseño del propio script — línea `cmd_verifica`, sección "Procedencia derivada" —, el listado de procedencia de las 631 entradas del manifiesto completo, no solo el id pedido; no es ruido de este acto, es el comportamiento documentado del comando.)

## 7 · `data/universo-puertas-2026-08-12.tsv`

**2 filas nuevas:**
- `MassMobilization_Dataverse_MMdata_adquisicion_REGLOTE3` — `EXISTE-SATISFACE`
- `OECD_TrustSurveyData_LAC2025_adquisicion_REGLOTE3` — `EXISTE-NO-SATISFACE` (PDF de resultados en mano, no confirmado si expone microdato aparte)

**8 filas actualizadas en sitio** (mismo criterio `ACTUALIZA` que la fila WVS de 2026-08-12 ya usa en este archivo — edición a mano es el diseño de Dominio 2, `INFRAESTRUCTURA-v1_0.md`: "ninguna tiene vía de escritura por script"):
- `LAPOP` (era `gap_mapeo_map_b`/`NO-ENCONTRADO`) → `EXISTE-SATISFACE`, evidencia real
- `WorldBank_MEX_ECEPIE_2012_2014_catalogo2661` (`EXISTE-NO-SATISFACE` → `EXISTE-SATISFACE`, microdato nuclear ya en corpus)
- `GPS_Global_Preferences_Survey` (`EXISTE-NO-SATISFACE` → `EXISTE-SATISFACE`, llegó la entrega por correo)
- `openICPSR_Microcredit_MexicoPlacement_proj116334` (`NO OBTENIDO POR AGENTE` → `EXISTE-SATISFACE`)
- `MICROCREDIT_IMPACTS_COMPARTAMOS_RCT` y `..._RANDOMIZED_..._PLACEMENT_EXP` (gaps → `EXISTE-SATISFACE`, mismo hallazgo que proj116334)
- `RNM_CNGMD_2023_catalogo977` (ya `EXISTE-SATISFACE`; solo nota corroborante, veredicto sin cambio)
- `Tandas_para_el_Bienestar` (nota sobre el workbook PILP; veredicto SIN CAMBIO — no es el mismo objeto que el portal)

Validado después de escribir: 122 filas de datos (120 + 2), las 122 con exactamente 15 columnas (`split('\t')`), editado con `split`/`join` de texto plano — **no** `csv.writer` (defecto ya conocido de este proyecto con estos TSV).

## 8 · `tests/check.py --baseline`: ROJO — 7 entradas nuevas, ninguna corregida unilateralmente

```
LÍNEA BASE: ROJO — 7 entradas nuevas frente a tests/baseline.json (HEAD congelado 3d0d1e5)
```

Desglosado, sin colapsar:
- **T02 × 2, genuinamente nuevas y ya declaradas en §3:** los dos duplicados byte-idénticos del propio lote (`ECEPIE (1).xml`, `LAPOP 2023 (1).dta`). No se borran ni renombran los archivos del usuario para silenciar el test — igual que el resto del proyecto trata este tipo de hallazgo, se reporta, no se resuelve editando el síntoma.
- **T02 × 2, preexistentes, no causadas por este acto:** `ZA5900_cdb (1).pdf`≡`ZA5900_cdb.pdf` y `ZA6980_q_mx (1).pdf`≡`ZA6980_q_mx.pdf`, ambos en la raíz de `descargas_mx` desde 2026-08-12 (P·Lote-1/APERTURA-ISSP). Aparecen como "nuevas" contra `baseline.json` porque T02 depende del filesystem real vía `data/raices.local.yaml` (gitignorado, no portable entre máquinas/worktrees) — es la primera vez que este worktree corre el check con `descargas_mx` configurado, no la primera vez que el duplicado existe.
- **T16 × 3:** citas desactualizadas de `canon/estado-programa-v1_10.md`/`canon/gobernanza-v1_15.md` sobre el conteo FAIL/WARN vigente ("18 FAIL" citado, corrida real da más). Preexistente y ajeno a este acto — no se tocó ningún archivo de `canon/`; coherente con el hallazgo ya hecho en este mismo acto (fuera de esta nota) de que `gobernanza-v1_15.md` deja de listar ADR nuevos después de ADR-54 pese a que la cabecera del archivo se seguía enmendando in situ.

No se corrió `--freeze`: recongelar la línea base exige ADR de mesa (precedente fijado por `ADR-76(f)`, citado en `hallazgos.md`), fuera de la autoridad de este acto.

## 9 · Fuera de perímetro, declarado

`tools/curador_registro/decide_acquisition.py` opera sobre `data/curacion-universo/universo-declarado-t0.tsv` + `activos-descubiertos-durante-ronda.tsv` → `decisiones-adquisicion.tsv` (Dominio 3) — **mecanismo distinto y desconectado** de `universo-puertas`/`cola-adquisicion` (Dominio 2), según `data/INFRAESTRUCTURA-v1_0.md`. No tiene acción para "fuente recién adquirida" (solo `NO_ADQUIRIR_AHORA`/`BUSQUEDA_DIRIGIDA`); `EN-ESPERA-DE-VÍA` es convención de prosa en encargos/hallazgos, no una columna/valor de ningún TSV (verificado por `grep`). No se tocó `decisiones-adquisicion.tsv` ni ningún archivo de Dominio 3.

## Contadores movidos

- Entradas de `data/manifiesto.yaml`: 582 → 631 (+49)
- Verificación hash: 0 → 49 COINCIDE (de las entradas nuevas)
- Filas de `universo-puertas`: 120 → 122 (+2); 8 filas cambian de veredicto o ganan nota corroborante
- Línea base de `tests/check.py`: VERDE (heredado) → ROJO, 7 entradas nuevas declaradas y explicadas (2 mías + 2 preexistentes recién visibles + 3 de documentación de canon, ninguna corregida sin autoridad de mesa)
