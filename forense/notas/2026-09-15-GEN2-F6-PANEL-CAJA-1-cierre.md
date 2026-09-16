# Nota de cierre — ACTO GEN2-F6-PANEL-CAJA-1

Entorno: CAJA (Ubuntu), `data/raw` montada (`tools/entorno.py`: `corpus=SI`, `archivos_examinados=413`), red a `inegi.org.mx` en `200`. Base: `origin/main = a9eefeb` (merge de `PR #798`). Encargo archivado verbatim por 0-bis A.3 en `44a53b2`.

## P1 · MOCIBA (NC-0230, CERRADA)

**A.4/A.13.** Se leyeron 3 FD (xlsx, vía `openpyxl`): `data/raw/mociba2021/mociba2021_fd.xlsx` (129 886 B, sha256 `375bf7c1...`, COINCIDE con manifiesto), `mociba2022/mociba2022_fd.xlsx` (136 935 B, sha256 `923fa85a...`, COINCIDE — antes `POR VERIFICAR` en `F6-falta-conseguir-v1_0.tsv`, ahora verificado), `mociba2023/mociba2023_fd.xlsx` (138 846 B, sha256 `f4a5d24c...`, COINCIDE). Búsqueda de `denunci` sobre la columna `Pregunta` de las tres hojas, filas 1–2603 (2021), completas en las otras dos.

**Hallazgo.** Batería de acciones tras ciberacoso en `P12` (2021/2022) / `P12` con desdoble (2023). `P12_5` idéntica en 2021 y 2022, fila 2503/2728: *"12.5 ¿Qué acciones tomó o ha tomado como consecuencia de la(s) situación(es) que vivió(vive)? Denunciar ante el Ministerio Público o policía"*, códigos `1=Sí/2=No`. **2023 desdobla** el mismo reactivo en dos ítems separados: `P12_05` ("...Ministerio Público o Fiscalía Estatal", fila 2735) y `P12_11` ("Reportar ante la policía", fila 2753) — confirma exactamente lo que `NC-0237` (abierta, `ACTO GEN2-REACTIVOS-RESIDUALES-2`) ya señalaba como pregunta pendiente de mesa. **Por eso el par declarado es 2021+2022**, wording-consistente, y no 2021+2023: la pregunta de unión de `NC-0237` no aplica a este par y `NC-0237` queda abierta sin bloquear esta declaración.

**Universo:** `P4_01`..`P4_13` (fila 38 en ambas olas), batería de 13 situaciones de victimización; el universo de `P12` son quienes vivieron ≥1 situación (inferencia por numeración/estructura, no por nota "Aplica" explícita — el FD compacto de INEGI no trae esa nota, y no se abrió la BD para confirmar empíricamente: `NC-0161` exige leer SOLO estructura para preservar la reserva de la familia). **Ponderador:** `FACTOR` (fila 2531/2765). **Dominios:** `SEXO` (fila 2576/2810), `EDAD` (fila 2578/2812).

**Corrección de #798 a #791, con cita.** `ADR-518` (`ACTO GEN2-PANEL-F6-EXPANSION-1`, `PR #798`) ya corrigió la línea de exposición de `v1_1` para R01 ("`CALC/marco/corridas-R/prereg-caja 0`", incorrecta) citando `marco-congelado-piloto-v1_0.tsv` (`TIC-10` = MOCIBA 2023 `P4_01`, `TIC-11` = MOCIBA 2024 `P3`, ambas con tabulados abiertos por `FP-93`) y `crosswalk-pregunta-regla-v1_1.tsv` (ambas `NO-EMITE`), moviendo el par propuesto de 2021+2023 a 2021+2022. `v1_1` era la lista que `PR #791` (`ACTO GEN2-F5-CIERRE-Y-PANEL-1`) auditó y usó como insumo (P2 de su perímetro) para su cifra de "2 retenidas realistas" — la corrección de `#798` corrige, por transitividad, la premisa de exposición que `#791` había heredado sin saberlo de `v1_1`. Este acto no reabre `v1_1` ni `#791`: cita la cadena y declara el par ya corregido por `#798`.

**Resultado:** R01 pasa de "SI, condicionado — NO EJECUTABLE EN NUBE" a **CONGELABLE**. Escrito en `data/reactivos-contexto-verificados-v1_0.tsv` (4 filas: `mociba2021`/`mociba2022` × `P12_5`/`FACTOR`/`SEXO`, más `P4_01` cada una) y `data/reactivos-contexto-fuentes-v1_0.tsv` (3 filas: `mociba2021/2022/2023`).

## P2 · ISSP R09 (NC-0231, CERRADA)

**A.4/A.13.** `raiz: descargas_mx` (`/mnt/c/Users/PC0/Descargas MX`, DrvFs, fuera del sandbox por política — `dangerouslyDisableSandbox` usado solo para localizar/copiar/verificar sha256, la lectura y todo el resto de la sesión corrió sandboxed sobre la copia en scratchpad). `ZA6980_q_mx.pdf`, 247 978 B, sha256 `61bc0c80...` COINCIDE con manifiesto. `pdftotext -layout`, 8 páginas, búsqueda de "pedir prestad" sobre el texto completo.

**Hallazgo.** Página 3, Pregunta 8, inciso a: *"¿A quién o dónde acudiría primero para pedir prestada una gran suma de dinero?"* — 8 categorías: `1` Familiares o amigos cercanos · `2` Otras personas · `3` Compañías privadas · `4` Servicios públicos · `5` Organizaciones sin fines de lucro o religiosas · `6` Otras organizaciones · `7` Ninguna persona u organización · `8` No puedo elegir. Coincide con la etiqueta ya fijada por `#798` sin abrir el PDF ("`v26` = Q8a Whom or where to ask for help: borrow large sum of money?").

**Resultado:** R09 queda con las cinco piezas completas (reactivo, universo `c_alphan`, ponderador `WEIGHT`, dominio `SEX`, codificación) — **CONGELABLE**, la única familia del panel en ese estado sin condición pendiente. Escrito en `data/reactivos-contexto-verificados-v1_0.tsv` (fila `za6980`/`v26`) y `-fuentes-` (fila `za6980`).

## P3 · ENCO R10 (NC-0232, CERRADA)

**A.4/A.13.** Mismo mecanismo de raíz que P2. `UNIVERSO-2026-09/ENCO/c_enco_b_v4.pdf`, 170 567 B, sha256 `f7e9d6b9...` COINCIDE con manifiesto. `pdftotext -layout`, 2 páginas, texto completo revisado (15 ítems, `P1`–`P15`).

**Hallazgo:** `EXISTE-SATISFACE`. Página 1, ítem 10: *"¿ACTUALMENTE USTED tiene posibilidades de AHORRAR alguna parte de sus ingresos?"*, códigos `1=Sí/2=No/3=No sabe/4=No tiene ingresos`. Universo: personas de 18 años y más (cabecera del cuestionario). El modelo impreso trae pie "Modelo Octubre 2010", declarado por transparencia — no afecta la vigencia del ítem en el archivo agosto-2026 ya adquirido (mismo cuestionario básico).

**Resultado:** confirma (a) del F6-falta-conseguir; (b) — adquirir dos olas de microdato ENCO — sigue **fuera de perímetro** (servicio adq, cola sin tocar). R10 sigue **NO HOY**, con un solo bloqueador en vez de dos. Escrito en `data/reactivos-contexto-verificados-v1_0.tsv` (fila `enco`/`P10`) y `-fuentes-` (fila `enco`).

## P4 · Propagación de F-19 (NC-0233, CERRADA)

Firma de mesa verbatim (15/sep/2026, archivada en `forense/encargos/2026-09-15-GEN2-F6-PANEL-CAJA-1.md` §Texto del encargo): el crosswalk persona→establecimiento **NO** es admisible para F6 — las reglas de `M` están calibradas sobre persona y una familia de establecimiento mide otro estimando en otro universo (A-bis 4). `R02-TRA-WBES-SOBORNO` y `R08-TRA-ENCRIGE-CORRUPCION` dejan de perseguirse como celdas de transferencia y pasan a `estado = UNIDAD-DISTINTA-NO-TRANSFERENCIA` en el sucesor del panel — familias descriptivas del dominio TRA para el informe, no celdas. **F6 sigue sin abrirse.**

## Sucesor del panel

`forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`: mismas 27 filas que `v1_2`, solo 5 tocadas (`R01`, `R02`, `R08`, `R09`, `R10`); diff verificado por `familia_id` idéntico fila a fila y `git diff --numstat` = 10 líneas (5 borradas + 5 añadidas, exacto). **Conteo de ejecutables re-derivado, no heredado: 2** (`R01`, `R09`) — mismo número que `v1_2`, pero ahora ambas **CONGELABLES sin bloqueo** en vez de condicionadas/bloqueadas en nube. `F6-falta-conseguir-v1_0.tsv` **no se tocó** (fuera de perímetro, "el servicio ya tiene rutada").

## Efecto de segundo orden (bookkeeping, no contenido)

Cerrar 4 filas `NC` bajó el conteo de `WARN` de la suite en 4 (`4348→4344`), desincronizando la cifra que `ADR-520` había declarado al cerrar el mismo día. Recifrado en el mismo commit-cascada, mismo mecanismo ya precedentado por `ACTO T20-LLAVES`/`ACTO CENSO-CMD` (`forense/hallazgos.md`): se edita el número, no se narra al lado (`tests/check.py::T16` exige literal `**N FAIL · N WARN**`). `tests/baseline.json` sin tocar, cero `--freeze`. `LÍNEA BASE: VERDE` antes y después de este acto.

## Contador

**Cero.** Cero llamadas, cero mediciones, cero corridas selladas, cero cambios al motor, cero escritura en `data/cola-adquisicion-v1_0.tsv` ni en `data/curacion-registro/`. Este acto mueve ejecutables del panel (de bloqueados a congelables) y cierra la fila R02/R08 — exactamente lo que el encargo pedía como contador.

## NO hace

No abre F6. No re-sella `FP-374` (`firmas-pendientes.tsv` sin tocar). No adquiere (ni ENCO ni ninguna otra ola; `servicio adq` sin tocar).
