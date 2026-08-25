# ACTO PYPDF-REBARRIDO-B — 24/ago/2026

Ejecuta `FP-122` (sucesor declarado de `FP-111`), sobre `forense/encargos/2026-08-24-PYPDF-REBARRIDO-B.md`. Base: `ec8da5b` (`origin/main` tras fusionar `MARCO-SATURA-CODEX`, PR #323).

## §1 · Universo del problema (derivación, no supuesto)

`FP-111` declaró el universo del problema como no-derivado: cuántos veredictos `NO-ENCONTRADO`/`EXISTE-NO-SATISFACE`/`SOLO_PRE=0`/`0 aciertos` del corpus se apoyan en `pypdf` (o en extracción de PDF sin extractor nombrado). Este acto lo deriva.

**Barrido mecánico, `ugrep -I` (`command grep` para todo negativo, `feedback_grep_es_ugrep_falsos_negativos`):**

- `data/*.tsv` (44 archivos) grepeados por líneas con `NO-ENCONTRADO`/`EXISTE-NO-SATISFACE`/`SOLO_PRE=0` **y** `.pdf` — 8 archivos con al menos un hit: `abrir4-variables-2026-08-08.tsv`, `censo-explotacion-2026-08-17.tsv`, `coef-universo-v1_0.tsv`, `exploracion-puertas-2026-08-07.tsv`, `reapertura-52a-54-variables-2026-08-13.tsv`, `universo-puertas-2026-08-12.tsv`, `universo-puertas-2026-08-14.tsv`, `verif3-variables-2026-08-08.tsv`.
- `forense/notas/*.md` (288 archivos) + `forense/hallazgos.md` grepeados por la misma combinación de vocabulario negativo + `.pdf`, excluyendo `pdftotext`/`pdfplumber`/`pdfminer` para aislar candidatos "extractor no nombrado".
- `pypdf`/`PyPDF2`/`pdfplumber` grepeado sobre todo `data/` + `forense/` sin filtro de verdicto, para no perder un negativo cuya fila no usara literalmente las cuatro etiquetas de vocabulario.

**Total de archivos examinados por el barrido: 44 (`data/*.tsv`) + 288 (`forense/notas/*.md`) + 1 (`forense/hallazgos.md`) + 1 (`forense/firmas-pendientes.tsv`) = 334.**

## §2 · Filtro de los candidatos

De las coincidencias `.pdf` + verdicto negativo, la inmensa mayoría **no es este defecto**:

- `reapertura-52a-54-variables-2026-08-13.tsv` (118 filas) cita `.pdf` sólo como nombre del instrumento (`ZA5900_q_mx.pdf`); su evidencia remite a `forense/notas/2026-08-13-apertura-issp.md:127`, que declara el extractor explícitamente: `pdftotext -layout` (Poppler 26.01.0) — no `pypdf`. Fuera de universo.
- `universo-puertas-2026-08-12.tsv`/`-14.tsv`, `exploracion-puertas-2026-08-07.tsv`, `censo-explotacion-2026-08-17.tsv`: los `NO-ENCONTRADO`/`EXISTE-NO-SATISFACE` ahí son de **adquisición** (trámite, descarga truncada, clasificación de documento) — no de búsqueda de término dentro de texto extraído de PDF. Fuera de universo (el encargo pide extracción de PDF sin extractor nombrado, no acceso a la fuente).
- `2026-08-11-e4b-sello-b-corrida-b.md` y `2026-08-13-enasic-split-verificacion.md` (`periodo_levantamiento` `NO_DETERMINADO`; guion de entrevista `NO-ENCONTRADO` sobre `889463927082.pdf`): ambos nombran el extractor explícitamente, `pdftotext -layout`. Fuera de universo.
- `data/coef-universo-v1_0.tsv:13` (fila `N13/G5.familismo_obligacion`, EDER 2025): la evidencia original cita un comando `pypdf`, pero la fila queda `RESUELTA` con evidencia posterior vía `pdftotext -layout` (8401 líneas, citas de línea) — ya no es un negativo pypdf-solo vigente. Fuera de universo.

**Un único candidato real** sobrevive el filtro: `data/coef-universo-v1_0.tsv:14` (fila `TODOS-LOS-15`, verdicto `NO-ENCONTRADO-EN-UNIVERSO-INSPECCIONADO`), evidencia: *"Texto completo extraido con pypdf de los 6 PDF (6408 a 35733 caracteres cada uno)"* — el mismo negativo que ya nombraba `FP-111`. No hay un segundo negativo pypdf-solo en el corpus.

## §3 · Re-corrida (Método, paso 2)

Los 6 PDF de `TODOS-LOS-15` (los cuestionarios ENOE `c_amp_v5/v6a`, `c_bas_v5/v7`, `c_sdem_v4/v5a`) se verificaron por `sha256` contra `data/manifiesto.yaml` antes de abrir (A.1) — las 6 coinciden exactamente. Se corrió `pdftotext -layout` + `pypdf` 6.16.1 (una invocación por id) y se buscó la **unión** de los mismos 7 términos que el negativo original citó como los únicos con hits (`ahorro`, `credito`, `deuda`, `riesgo`, `apoyo`, `autoridad`, `violencia`) — mismo patrón que `tools/barrido_enoe_constructos.py::texto_pdf`.

Resultado en `data/pypdf-rebarrido-2026-08-24.tsv`: **603,465 caracteres examinados** (pdftotext=463,074 + pypdf=140,391 — ≈3.3× más texto que el `pypdf`-solo original, que veía 140,391 sólo de estos 6). Los conteos por término reproducen exactamente lo que el negativo original describió (ahorro/crédito/deuda/riesgo presentes sólo en `c_amp_v5`/`v6a` como prestación laboral; `apoyo`/`autoridad` como boilerplate del Art. 45 SNIEG; `violencia` con un único hit sustantivo, dentro de la categoría de motivo de migración en `c_sdem_v5a` — cita exacta verificada, ver TSV). **Ningún término nuevo aparece con el triple de texto.**

**Veredicto: SOSTIENE.** Coincide con la conclusión que `forense/notas/2026-08-20-adq-enoe-pre2019-resultados.md` ya había alcanzado el 20/ago sobre este mismo negativo con el mismo método — este acto lo corrobora con evidencia propia (comandos corridos hoy, no sólo cita del precedente), no lo hereda sin verificar.

## §4 · Lo que voltea

**Nada voltea.** No hay enmienda in situ que escribir: el único candidato del universo derivado (§2) sostiene, y los demás quedaron fuera de universo por nombrar ya `pdftotext` o por no ser el defecto (adquisición, no extracción). `A.12` (fila de defecto) no aplica — no hay regla/contador/ficha que este volteo gatee, porque no hubo volteo.

## §5 · Nota a mesa

Cuántos negativos había: **1** (`data/coef-universo-v1_0.tsv:14`, `TODOS-LOS-15`) en todo el corpus (`data/*.tsv` + `forense/notas/` + `forense/hallazgos.md`, 334 archivos barridos) — el mismo que `FP-111` ya nombraba, no uno adicional. Un segundo candidato (`coef-universo-v1_0.tsv:13`, EDER 2025) usó `pypdf` en su comando original pero ya está `RESUELTA` con `pdftotext` posterior, así que no cuenta como negativo pypdf-solo vigente. Cuántos sostienen: **1 de 1** — con el triple de texto (unión pdftotext+pypdf, 603,465 caracteres contra 140,391 sólo-`pypdf`), el mismo negativo llega al mismo sitio, término por término. Cuántos voltean: **0**. Lo que importa: el universo real es minúsculo — este corpus no tiene una familia de negativos pypdf-solo sin verificar; el caso que motivó `FP-111` era, aparentemente, el único de su clase, y ya estaba corroborado desde el 20/ago por `ADQ-ENOE-PRE2019`. La pregunta abierta que sí queda para mesa: si vale la pena una regla permanente (p.ej. en `tools/curador_registro/` o en el patrón de futuros barridos de PDF) que exija por defecto la unión de dos extractores en vez de nombrarla caso por caso — este acto no la escribe, sólo la señala, por estar fuera de su perímetro declarado.

## §6 · Perímetro respetado

Tocados: `data/pypdf-rebarrido-2026-08-24.tsv` (nuevo), `forense/firmas-pendientes.tsv` (`FP-111` y `FP-122` reciben `ejecutada_en`), `canon/gobernanza-v1_15.md` (`ADR-156`, renumerado de `ADR-155` por colisión al fusionar con `SELLA-AGO24-C-v2`, PR #322), `canon/estado-programa-v1_10.md` (recifrado), esta nota, `forense/encargos/2026-08-24-PYPDF-REBARRIDO-B.md` (archivado, `CONSUMIDO`). No se editó ningún veredicto sellado; no se tocó `Hito D`, condicionales ni coeficientes — este acto es una auditoría de la base de negativos, no una medición.
