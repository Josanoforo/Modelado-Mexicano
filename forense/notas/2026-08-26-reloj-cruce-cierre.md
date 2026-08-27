# ACTO MAESTRA31-E1 · RELOJ-CRUCE — cierre

Dirección (maestra-31), 26/ago/2026. Ejecutor: worktree propio `/home/pc0/mm-e1-reloj-cruce`, rama `acto/e1-reloj-cruce`, base `origin/main` = `44cd841` (el clon `/home/pc0/Modelado-Mexicano` estaba parado en `acto/cal-g3-puntual`, no en `main` — mismo patrón que ACTO MAESTRA30-E9/ADR-209).

## Arranque

1. **REPO.** No se clonó ninguno nuevo. Se creó worktree propio `/home/pc0/mm-e1-reloj-cruce` sobre `origin/main` desde `/home/pc0/Modelado-Mexicano` (que estaba en `acto/cal-g3-puntual`, rama equivocada). `git log -1 --format="%h %s"` → `44cd841 Merge pull request #381 from Josanoforo/acto/e9-scoring-v2`.
2. **SHA.** Declarado por el encargo: `6d213a6`. `origin/main` real al momento de arranque: `44cd841` — se movió (PR #381 y posteriores ya fusionados). No es PARO; se refresca y se reporta la diferencia.
3. **data/raw.** Ausente en el worktree nuevo (gitignorado, no se materializa con `git worktree add`). Se enlazó: `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo destino que usa `/home/pc0/Modelado-Mexicano/data/raw`). Tras el enlace, `ls data/raw | wc -l` → 321 entradas.
4. **ENTORNO.** `echo $CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → vacío (esperado). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. A.2 tercera parte: `ls data/raw/ 2>/dev/null | head -1` → `2005trim1_csv.zip` (no vacío tras el enlace del paso 3) — el acto NO para aquí.
5. **ESPEJO.** Ninguna cifra de este cierre sale del espejo del proyecto; todas se derivan del worktree `/home/pc0/mm-e1-reloj-cruce` sobre `origin/main`.

**Compuerta cero (paso 1 del encargo):** `gh pr view 381 --json state,mergedAt,number` → `{"mergedAt":"2026-08-27T00:11:47Z","number":381,"state":"MERGED"}`. FUSIONADO. El acto continúa.

## Paso 2 — Alcance del falsador, declarado

Texto completo leído en `forense/notas/2026-08-25-cruce-oferta-demanda.md:321-359` (sección "## Cita de gobierno y falsador a catorce días" con su subsección "### Regla de mantenimiento").

Cita literal del falsador (línea 341):

> **Falsador exacto a catorce días — 2026-09-08:** `<1 medición lanzada ⇒ la maestra registra infraestructura en forense/hallazgos.md.`

**Veredicto: AMBIGUO.** El texto no dice, en ningún punto de las líneas 321-359, si "medición lanzada" se refiere solo a mediciones derivadas de este cruce o a cualquier medición del programa. La sección vive dentro de la nota del cruce-oferta-demanda (contexto local), pero la frase del falsador en sí ("<1 medición lanzada") no lleva calificador ("de este cruce", "del programa", "que use este TSV"). No se elige entre las dos lecturas — se declaran ambas y se cuenta bajo ambas por separado (paso 3).

Confirmación con universo declarado: `grep -rIn --exclude-dir=.git --exclude-dir=raw -E "2026-09-08|catorce días" .` sobre el árbol completo del worktree (excluyendo `.git` y `data/raw`) devuelve coincidencias en **1 archivo**, `forense/notas/2026-08-25-cruce-oferta-demanda.md`, en 2 líneas (321 y 341). Sin fila de tablero, sin ADR dedicado — confirmado.

### Tensión B-bis

Derivado con `awk` sobre la columna 8 (`veredicto_A4`) de `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` (49 filas de datos, cabecera excluida):

```
awk -F'\t' 'NR>1{c[$8]++} END{for(k in c) print k, c[k]}' data/curacion-registro/cruce-oferta-demanda-v0_1.tsv
```

Resultado:

- `NO-ENCONTRADO` → 41
- `EXISTE-NO-SATISFACE` → 7
- `NO-ACCESIBLE` → 1

Total 49, **0 filas `EXISTE-SATISFACE`**. Coincide exactamente con la cifra que el encargo daba para verificar.

**La tensión se sostiene.** La "Regla de mantenimiento" (líneas 335-339 de la nota del cruce) exige, para promover a un acto medidor, "solo una fila `EXISTE-SATISFACE`, con reactivo abierto, estado `VERIFICADO-REACTIVO`, población/diseño compatibles y ruta parámetro→mecanismo explícita" — y el TSV tiene cero filas así. El falsador del 8/sep exige `≥1 medición lanzada` a los 14 días o dispara el registro de infraestructura; pero la única vía de promoción que la propia regla de mantenimiento habilita (`EXISTE-SATISFACE` desde el cruce) está en cero, así que el cruce por sí solo no puede satisfacer el falsador — es, como declara el encargo, un defecto de clase **B-bis**: una escala (la regla de mantenimiento) sin fila para el desenlace que va a ocurrir el 8/sep si nada más se mueve por otra vía.

Esto NO decide si el falsador se satisface por otras vías (mediciones fuera del cruce) — eso es la RANURA M-RELOJ, de mesa.

## Paso 3 — Conteo A.13 (mediciones lanzadas desde 2026-08-25)

Método: se probó primero contra un caso conocido — `ADR-196` (`+1`, `R10.2`→D) — para calibrar el patrón de extracción antes de correr sobre todo el rango.

Comando usado para listar ADRs fechados 25-26/ago con su bloque `CONTADOR`:

```python
import re
text = open('canon/gobernanza-v1_15.md', encoding='utf-8', errors='replace').read()
entries = re.findall(r'\*\*ADR-\d+.*?(?=\n\*\*ADR-\d+|\Z)', text, re.S)
for e in entries:
    m = re.match(r'\*\*(ADR-\d+)', e)
    adr = m.group(1)
    if re.search(r'2026-08-2[56]', e):
        cont = re.search(r'CONTADOR:?\**\s*(.{0,150})', e, re.S)
        ...
```

44 entradas de ADR con fecha 25/ago o 26/ago dentro de su bloque. De esas, con `CONTADOR` explícitamente no-cero (número o medición nombrada, no "cero"/"cero directo"/"cero declarado"):

- `ADR-172` (`ACTO INDICE-NO-INEGI`) → "la columna `publicada` de las 8" (movimiento clasificatorio, no una medición del cruce).
- `ADR-196` (`ACTO PROPAGA-LETRAS`) → `+1` — `R10.2` archivado a `D`, **usando el cruce `#363` como parte de su universo declarado**.
- `ADR-209` (`ACTO MAESTRA30-E9 · SCORING-V2`) → "el marcador v1.1 — la medición de la sesión" (scoring corrió en vivo; no usa el cruce del 25/ago).

Además, censo directo de `forense/hitoD-preregistro-v2_0.md` (bloque append-only, enmiendas fechadas 25-26/ago): 6 fichas archivadas/movidas desde el 25/ago — `R10.2`→D, `R8.2`→B, `R2.2`→D, `R2.1`→D, `R3.4`→B, `R10.1`→C. De esas, **4 citan expresamente el cruce `#363`** (`data/curacion-registro/cruce-oferta-demanda-v0_1.tsv`) como parte de su universo declarado: `R10.2`, `R8.2`, `R2.2`, `R2.1`. Las otras 2 (`R3.4`, `R10.1`) no citan el cruce.

Llaves de identificación ejercidas desde 25/ago (`forense/registro-llaves-identificacion-v1_0.md` + notas de cierre): `llave2-decreto` (25/ago), `ejerce-llave-compartamos` (26/ago) — ninguna de las dos cita el cruce `#363`.

### Conteo crudo bajo las dos lecturas (sin fusionar)

- **Lectura "acotada a este cruce"** (solo mediciones/archivos que citan explícitamente el cruce `#363` como evidencia): **≥4** — las 4 fichas de Hito D que citan el cruce (`R10.2`, `R8.2`, `R2.2`, `R2.1`), de las cuales `R10.2`/`R2.1` corresponden además a ADRs con `CONTADOR` no-cero (`ADR-196`, `ADR-208`).
- **Lectura "del programa entero"** (cualquier medición lanzada desde 25/ago, cite o no el cruce): **≥7** — las 6 fichas de Hito D archivadas/movidas + el marcador v1.1 de `ADR-209` (scoring), sin contar aparte llaves ejercidas ni el movimiento clasificatorio de `ADR-172` por no ser inequívocamente "medición".

Bajo cualquiera de las dos lecturas, el conteo crudo es **≥1**, así que el falsador del 8/sep (`<1 medición lanzada`) NO se dispara con lo lanzado hasta hoy (26/ago), independientemente de cuál lectura sea la correcta. Esta es una observación derivada, no una adjudicación de la RANURA M-RELOJ (que decide si "medición" en el falsador exige además ser resultado del propio cruce, algo que el texto no aclara).

## Paso 4 — Censo de la palanca #1

Ver commits separados en este mismo PR:
- **COMMIT-1** (protocolo, antes de abrir payload): sección "Palanca #1 · COMMIT-1" más abajo.
- **COMMIT-2** (resultado real, commit separado): sección "Palanca #1 · COMMIT-2" más abajo.

## Palanca #1 · COMMIT-1 (protocolo, congelado antes de abrir payload)

Fila `disparador_sin_base:riesgo_fiscal_percibido` de `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` — 8 candidatas, filtradas con:

```
awk -F'\t' '$1=="disparador_sin_base:riesgo_fiscal_percibido"' data/curacion-registro/cruce-oferta-demanda-v0_1.tsv
```

| # | instrumento_ola | que_le_falta (columna 9 del TSV) |
|---|---|---|
| 1 | ECF 2019, 2021 y 2024 | CoDi y percepción de riesgo fiscal/vigilancia |
| 2 | SFD 2024 | reactivo fiscal y coobservación del desenlace con las razones |
| 3 | ENAFIN 2024 | unidad persona usuaria, CoDi y percepción fiscal asociada al uso |
| 4 | ENCIG 2011–2025 | CoDi y riesgo fiscal referido a usar el servicio digital |
| 5 | ENDUTIH 2023, 2024 y 2025 | reactivo de percepción de riesgo fiscal o vigilancia |
| 6 | ENIF 2012, 2015 y 2018 | objeto CoDi y percepción fiscal asociada a su uso |
| 7 | ENIF 2021 y 2024 | riesgo fiscal referido a usar CoDi y coobservable con fricción |
| 8 | ENSAFI 2023 | descriptor que permita citar texto y código exactos del reactivo |

**Términos de búsqueda exactos** (aplicados a diccionarios de datos, catálogos y descriptores/FD de cada payload, byte a byte, no a documentos secundarios sobre el payload): `codi`, `riesgo fiscal`, `fiscal`, `vigilanc`, y los códigos de reactivo ya citados en el TSV para cada instrumento (p. ej. `P7_32_6`, `P7_29`, `P5_20`, `P6_14`, `P10_1_2`, `P11_1_04`, `P3`, `P30_1`, `P5_*`).

**Control positivo:** el mismo que usa el TSV para toda la fila — `INEGI=122568/169474` (columna 13, `control_positivo`) — confirma que el índice/mecanismo de búsqueda SÍ encuentra hits reales cuando el término existe (se corrobora abriendo al menos un archivo donde `codi` u otro término de control aparezca antes de declarar ausencia en el resto).

**Escala de veredicto A.4** (aplicada tal cual, sin inventar casillas):
- `EXISTE-SATISFACE`: el payload trae, en el mismo reactivo o en reactivos coobservables de la misma unidad, CoDi/pago digital Y percepción de riesgo fiscal o vigilancia asociada a su uso.
- `EXISTE-NO-SATISFACE con qué falta`: el payload existe y es legible, pero falta explícitamente lo que el TSV ya declara en `que_le_falta`.
- `NO-ENCONTRADO con dónde y con qué términos`: se buscó con los términos de arriba en los archivos declarados y no aparece ninguna coincidencia real (control positivo confirmado en el mismo mecanismo).
- `NO-ACCESIBLE`: el payload declarado en el manifiesto no está en `data/raw/` o no se puede abrir con las herramientas disponibles en esta caja.

**Qué pasa si ninguna satisface:** se reporta B-bis en la palanca #1 (mismo patrón que el paso 2) — el disparador queda sin fuente que lo alcance en el corpus ya descargado; no se promueve, no se re-especifica, no se lanza sucesor.
**Qué pasa si alguna sí satisface (`EXISTE-SATISFACE`):** se reporta como hallazgo, con la cita exacta (archivo, columna/reactivo, valor); NO se promueve a acto medidor aquí — promover es de la Regla de mantenimiento, ejecutada por un acto medidor futuro, no por este censo.

«El primer resultado que produzca este procedimiento es el que se reporta.»

## Palanca #1 · COMMIT-2 (resultado real, byte a byte)

Universo declarado global: worktree `/home/pc0/mm-e1-reloj-cruce`, `origin/main` = `44cd841`, `data/raw` enlazado a `/home/pc0/mm-corpus/raw` (321 payloads), fecha 26/ago/2026. Mecanismo: extracción real de cada zip/xlsx/pdf/dbf (Python `zipfile`/`openpyxl`, `pdftotext`, `strings` sobre `.DBF`) — no lectura de documentos secundarios sobre el payload.

1. **ECF 2019/2021/2024 — Banxico Encuesta de Competencias Financieras.** Payload: `banxico_encuesta_competencias_financieras_2024.xlsx` (manifiesto id `banxico_encuesta_competencias_financieras_2024`, `data/raw/banxico_encuesta_competencias_financieras_2024.xlsx`, 1,210,013 bytes). Abierto con `openpyxl`; 1 sola hoja (`Sheet 1`), barrida completa por texto de celda buscando `codi` (excluyendo `codigo`/`código`) — 0 coincidencias. **Veredicto: `EXISTE-NO-SATISFACE`** — confirma el `que_le_falta` del TSV (CoDi y percepción de riesgo fiscal/vigilancia ausentes; el archivo es un índice/manual, no trae el reactivo).

2. **SFD 2024 — IFT Servicios Financieros Digitales.** Payload: `ADQ15_IFT_SFD_uso_confianza/reporte_especial_SFD.pdf` (manifiesto id `adq15_ift_sfd_reporte_especial_sfd`, 8,084,499 bytes). Convertido a texto con `pdftotext` (8,056 líneas); `grep -in "riesgo fiscal|vigilanc|fiscal"` → 1 coincidencia, "Área de ciberataques de la Fiscalía" (Ministerio Público, no riesgo fiscal); `grep -ic "codi"` → 4 menciones de CoDi, ninguna coobservada con riesgo fiscal. **Veredicto: `EXISTE-NO-SATISFACE`** — confirma el TSV (reactivo fiscal y coobservación del desenlace ausentes).

3. **ENAFIN 2024.** Payload: `ADQ15_ENAFIN_2024_RNM_INEGI/conjunto_de_datos_enafin_2024_csv.zip` (manifiesto id `adq15_enafin_conjunto_de_datos_enafin_2024_csv`, 96,758 bytes). Extraído; contiene tabulados agregados (`tr_enafin_tot_2024.csv`, `tr_enafin_tam_sec_loc_2024.csv`) con sus diccionarios de datos. `grep -n "codi"` en los diccionarios → 1 hit real: columna `L_70` = "Número de empresas según medio utilizado para realizar sus pagos, 2023_Pagos con códigos QR (CoDi)" — un conteo agregado de empresas, no un reactivo de persona usuaria. Búsqueda de `P3`/`P30_1` (los códigos de reactivo que cita el TSV, propios de microdato a nivel persona) → 0 coincidencias en este payload agregado; y 0 coincidencias de `riesgo fiscal`/`vigilanc`. **Veredicto: `EXISTE-NO-SATISFACE`** — CoDi existe como tabulado agregado por empresa, pero no la unidad persona usuaria ni la percepción fiscal que el `que_le_falta` exige.

4. **ENCIG 2011–2025.** Payload: `encig2023_datosabiertos_csv.zip` (manifiesto id `encig2023_datosabiertos_csv`, 26,171,769 bytes). Extraído; búsqueda de los códigos de reactivo del TSV (`P10_1_2`, `P11_1_04`) en diccionarios → 3 archivos cada uno (reactivos existen como columnas). Búsqueda de `riesgo fiscal` → 0; `vigilanc` → 1 hit, pero es contenido de una fila de datos libre (dirección/nombre de colonia con "vigilancia" en el texto), no un reactivo de riesgo fiscal — verificado abriendo la línea completa. **Veredicto: `EXISTE-NO-SATISFACE`** — confirma el TSV (CoDi y riesgo fiscal referido a usarlo, ausentes).

5. **ENDUTIH 2023/2024/2025.** Payload: `endutih2024/endutih2024_bd_dbf.zip` (manifiesto id `endutih2024_bd_dbf_zip`, 8,823,853 bytes). Extraído (`.DBF` binario, leído con `strings`). Códigos `P7_32_6`/`P7_29` presentes (1 archivo cada uno, en el diccionario correspondiente). `riesgo fiscal` → 0. `vigilanc` → 2 archivos `.DBF`, pero el contenido real (`strings`) es "CÁMARAS DE VIGILANCIA"/"VIDEOVIGILANCIA" — reactivos de infraestructura de vivienda/seguridad, no de riesgo fiscal — confirmado leyendo el contexto extraído. **Veredicto: `EXISTE-NO-SATISFACE`** — confirma el TSV.

6. **ENIF 2012/2015/2018 (pre-CoDi).** Payload: `enif2018_csv.zip` (manifiesto id `enif2018_csv`, 4,450,312 bytes; años 2012/2015 no re-abiertos individualmente porque el TSV los agrupa como "olas pre-CoDi" y 2018 es la más tardía del grupo, la más favorable a encontrar CoDi si existiera). Extraído; `grep -rli "codi"` → 2 archivos, ambos falsos positivos por subcadena (`codigo`/`código`, verificado con `grep -n`: columna `codigo` de clasificación de persona elegida, nada de CoDi). **Veredicto: `EXISTE-NO-SATISFACE`** (arrastrando la lectura de "olas pre-CoDi": el instrumento es anterior al lanzamiento de CoDi en México, 2019, por eso el reactivo no puede existir) — confirma el TSV.

7. **ENIF 2021/2024.** Payloads: `enif2021_csv.zip` (2,511,357 bytes) y `enif2024_csv.zip` (3,086,077 bytes). Extraídos; búsqueda en diccionarios de `P7_2_1`/`P7_3_1` (CoDi) → 2 archivos cada uno (reactivos existen); `P5_20`/`P6_14` (razón, respuesta única) → 2 archivos cada uno (reactivos existen). `riesgo fiscal` → 0 archivos. `vigilanc` → 0 archivos. **Veredicto: `EXISTE-NO-SATISFACE`** — CoDi y la batería de razones existen como reactivos separados, pero ninguno coobservable con riesgo fiscal/vigilancia — confirma el TSV exactamente.

8. **ENSAFI 2023.** El TSV declara `NO-ACCESIBLE` con `que_le_falta` = "descriptor que permita citar texto y código exactos del reactivo". Re-verificado hoy: `ensafi2023_fd_xlsx_zip` (manifiesto id, `data/raw/ensafi2023/ensafi_2023_fd_xlsx.zip`, 1,108,577 bytes) **SÍ está en `data/raw/` y SÍ se abre** — extraído con `zipfile`, contiene `ensafi_2023_fd.pdf` y `ensafi_2023_fd.xlsx`; el FD tiene 4 hojas (`TVIVIENDA`, `THOGAR`, `TSDEM`, `TMODULO`), barridas completas por texto de celda con `openpyxl`. Esto coincide con el hallazgo ya registrado del programa (ADR-198/ENSAFI-DESCRIPTOR: el FD real es `_xlsx.zip`, no `.xlsx` suelto) — la razón `NO-ACCESIBLE` del TSV está **desactualizada** para este acto, aunque no se edita el TSV (fuera de perímetro). Búsqueda de `codi`/`fiscal`/`vigilanc` en las 4 hojas → 0 coincidencias; la sección 5 de `TMODULO` (reactivos `P5_*`) cubre discapacidad, unión libre, hijos, ingreso, gasto — ningún reactivo de CoDi ni de riesgo fiscal. **Veredicto: `EXISTE-NO-SATISFACE`** — el FD SÍ es accesible y legible byte a byte (contradice `NO-ACCESIBLE` del TSV), pero no contiene el reactivo que el `que_le_falta` exige; se reporta como hallazgo, sin editar el TSV.

### Síntesis

**0 de 8 candidatas alcanza `EXISTE-SATISFACE`.** 7 confirman exactamente el `que_le_falta` que el TSV ya declaraba (byte a byte, sin contradicción); 1 (ENSAFI) corrige de facto `NO-ACCESIBLE`→`EXISTE-NO-SATISFACE` porque el FD sí se pudo abrir hoy, sin que eso cambie el resultado final (sigue sin satisfacer). Se sostiene B-bis para la palanca #1: el disparador `riesgo_fiscal_percibido` no tiene fuente que lo alcance en el corpus ya descargado. No se promueve ninguna fila, no se re-especifica el disparador, no se edita el TSV.

**Contador del acto: 8 veredictos A.4 con universo declarado, derivados de payload abierto.**

## FP-169

Fila agregada a `forense/firmas-pendientes.tsv` (SOLO esa fila; el segundo encargo de la serie en paralelo usa `FP-170+`).

## ADR

Máximo derivado con: `grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | grep -oE "[0-9]+" | sort -n | tail -1` → `209`. Candidateado: **ADR-210**. Nota para quien fusione segundo: si otro acto en paralelo (p. ej. el segundo encargo de la serie) también candidatea `ADR-210`, renumerar el que fusione después.

## RANURA M-RELOJ

(vacía — de mesa, no se llena en este acto. Copiada tal cual del encargo: la RANURA decide si el falsador se satisface/dispara/re-especifica; este acto no decide nada de eso.)
