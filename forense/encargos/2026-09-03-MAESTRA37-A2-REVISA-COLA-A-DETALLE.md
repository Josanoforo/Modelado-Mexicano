ENCARGO · ACTO MAESTRA37-A2 · REVISA-COLA-A-DETALLE — invoca /acto

SHA de redacción: 2e79d153 · COMPUERTA: PR de N8 fusionado (mismo archivo de cola; N8 reclasifica estados, éste añade informe por fila). ENTORNO ASIGNADO: NUBE con red (cloud_default; sonda INEGI como control positivo de red). NO descarga: este acto lee, sondea y recomienda; descargar es de MAESTRA38-A1 y de mesa. MODELO SUGERIDO: Opus (búsqueda de hermanas y juicio de identidad de fuente; Codex si mesa prefiere — es CLI, no exige caja).

FIRMA DE MESA — verbatim: la de «Descargas manuales» en §0. Regla que la traduce: ninguna fila se cierra por veredicto de agente; el entregable es información para que mesa decida.

═══ A.8 ═══ Cola: 112 filas; no OBTENIDO/CERRADA: 29 (9 PENDIENTE, 9 NO-ACCESIBLE, 7 NO-OBTENIDO-POR-ESTE-AGENTE, 2 OBTENIDO-PARCIAL, 1 NO-ACCESIBLE-DESDE-LA-CAJA, 1 firma c1) — tras N8: 5 pasan a NO-ADQUIRIDA-POR-COSTO y 2 a PENDIENTE-DE-MESA; el universo de este acto es lo que quede no OBTENIDO, derivado al arrancar. .claude/commands/adquiere.md ya exige ≥4 rutas y receta ≤1 min (ADR-261) — se reutiliza, no se rediseña. aliases-fuentes.tsv (14 fuentes) es la tabla de hermanas conocidas.

SPEC — dos commits. COMMIT-1: lista congelada de filas y, por fila, la pregunta que la fila responde (regla/necesidad que la cita, derivada de relaciones.tsv/necesidad-objeto-modelo.tsv; si ninguna la cita, se dice — es información para mesa, no cierre). COMMIT-2, por fila: (a) cuatro rutas con salida cruda (A.5), sonda de alcanzabilidad antes de contenido (v2.2); (b) hermanas: mismo objeto en otra fuente/portal/espejo/año, con la distinción de identidad de A.7 (mismo contenido, distinta envoltura ≠ fuente distinta); (c) qué exactamente trae cada candidata (tabla de variables / temas si hay FD público) y qué le falta contra la pregunta de (a); (d) recomendación en tres valores: BAJAR (receta ≤1 min) · NO-BAJAR-PORQUE (razón sustantiva) · MESA-DECIDE (dos opciones con costo). Ningún NO-ENCONTRADO sin universo, términos y fecha en la misma línea (A.4/A.13). Salida: forense/notas/2026-09-0X-MAESTRA37-A2-revision-cola.md + PAQUETE-RECETAS-3 + nota append por fila en la cola (writer de INFRA-1), sin cambiar estado_A4A5.

PERÍMETRO. Toca: data/curacion-registro/cola-adquisicion-registro.tsv (sólo columna nota, append) · vista T26 · forense/notas/…A2… · forense/notas/…PAQUETE-RECETAS-3.md · tablero · A.3 · cascada. NO toca: estado_A4A5 · data/manifiesto.yaml · aliases-fuentes.tsv (propone hermanas, no las da de alta) · milpa/**. No descarga. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR: ADR-330 (deriva) → renumerado a **ADR-331** al fusionar `origin/main` (`ADR-330` ya tomado por `MAESTRA37-N9`, misma rama) · FP-288 recibo · FP-289: «mesa firma la clasificación final de las N filas con el informe a la vista» (vence a 7 días desde 4/sep/2026 → 11/sep/2026). CONTADOR: filas con informe 0 → 28 · medición: cero.

## COMPUERTA SATISFECHA — 4/sep/2026

Verificado contra `origin/main` tras `git fetch && git merge`:
`MAESTRA37-N8 · CONSOLIDA-DECISIONES` corrió en NUBE el 4/sep/2026,
quedó `## CONSUMIDO` en
`forense/encargos/2026-09-04-MAESTRA37-N8-CONSOLIDA-DECISIONES.md`, y se
fusionó a `main` vía `PR #523` (commit de merge `4b508ad`, commit de
cierre de N8 `d96bf44`). Su P5 reclasificó
`data/curacion-registro/cola-adquisicion-registro.tsv`: cinco filas
comerciales (Homescan/NielsenIQ, Kantar Worldpanel, Tanda+ ×2,
Mercer/GPTW) `NO-ACCESIBLE` → `NO-ADQUIRIDA-POR-COSTO`; `WB6667` →
`PENDIENTE-DE-MESA`. La COMPUERTA de este acto («PR de N8 fusionado») **sí
está satisfecha**.

**Universo real, derivado al arrancar (no se asume el `29` original del
§A.8):** `data/curacion-registro/cola-adquisicion-registro.tsv` tiene hoy
112 filas; **28** no `OBTENIDO`/`CERRADA` (83 `OBTENIDO` + 1
`CERRADA-PREEXISTENTE` = 84; 112 − 84 = 28). Nota: el `§A.8` original
anticipaba "2 a `PENDIENTE-DE-MESA`" pero N8 sólo movió **una** (`WB6667`;
`ICPSR 35024` quedó ambigüedad documentada sin degradar estado, ya
`OBTENIDO`) — de ahí que el universo real (28) sea uno menos que el
aritmético ingenuo (29) del `§A.8`.

**Colisión de numeración detectada al fusionar `origin/main`.** El `§FP/ADR`
de este encargo pedía `ADR-330`, pero ese número ya lo tomó
`ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166` (esta misma rama, renumerado
desde su candidato original `ADR-328` al chocar con `ADR-328`/`ADR-329`
de `MAESTRA37-N8`, ya fusionados). Por la regla de la casa ("renumera
quien fusiona segundo"), este acto (`MAESTRA37-A2`) toma **`ADR-331`**,
contiguo tras `ADR-330`. `FP-288`/`FP-289` siguen libres (máximo real
`FP-287`) y se usan sin cambio.

Se ejecuta ahora el SPEC completo (dos commits) sobre el universo de 28
filas.

## CONSUMIDO

Ejecutado el 4/sep/2026 en entorno NUBE con red, con la skill `/acto`
(`ADR-237`), rama `claude/auditoria-encargos-maestra37-p8k51b`, cascada
en `ADR-331` (candidato original `ADR-330`; renumerado tras chocar con
`MAESTRA37-N9`, misma rama, por la regla de la casa "renumera quien
fusiona segundo").

COMPUERTA satisfecha: `MAESTRA37-N8` fusionó a `main` vía `PR #523`
(commit de merge `4b508ad`, cierre `d96bf44`).

Universo real derivado al arrancar: **28** filas no `OBTENIDO`/`CERRADA`
de `data/curacion-registro/cola-adquisicion-registro.tsv` (112 filas
totales; 83 `OBTENIDO` + 1 `CERRADA-PREEXISTENTE` = 84 cerradas) — no las
29 que el `§A.8` original anticipaba (`MAESTRA37-N8` movió una sola fila
a `PENDIENTE-DE-MESA`, no dos).

COMMIT-1 congeló la lista de las 28 filas con la pregunta (regla/
necesidad) que cada una responde. COMMIT-2 produjo, por fila: (a)
síntesis de las rutas de A.5 ya sondeadas (evidencia de 1-3 días,
salida cruda con fecha, código HTTP y bytes citados); (b) hermanas
conocidas (`aliases-fuentes.tsv`, criterio A.7); (c) qué trae/qué falta
cada candidata contra la pregunta; (d) recomendación en exactamente uno
de tres valores. Resultado: **`BAJAR` 7** (con receta ≤1 min cada una) ·
**`NO-BAJAR-PORQUE` 18** · **`MESA-DECIDE` 3** (dos opciones con costo
cada una). Detalle completo: `forense/notas/2026-09-04-MAESTRA37-A2-revision-cola.md`.
Recetas: `forense/notas/2026-09-04-MAESTRA37-A2-PAQUETE-RECETAS-3.md`.
Cada una de las 28 filas de la cola recibió un append en su columna
`nota` con puntero al informe y la recomendación; ninguna cambió
`estado_A4A5`. Vista T26 (`data/cola-adquisicion-v1_0.tsv`) regenerada
por `tools/vista_cola_adquisicion.py`. Recibo en tablero:
`forense/tablero/TABLERO-PROGRAMA-v1_1.md` §8.2.

Qué NO decide: ninguna fila se cierra por veredicto de agente (firma de
mesa del encargo, verbatim); no se descargó contenido real (perímetro
explícito); no se tocó `estado_A4A5`, `data/manifiesto.yaml`,
`aliases-fuentes.tsv` (hermanas propuestas en texto, no dadas de alta),
ni `milpa/**`.

Deuda que abre: `FP-289` (mesa firma la clasificación final de las 28
filas, vence 2026-09-11). Recibo: `FP-288`.
