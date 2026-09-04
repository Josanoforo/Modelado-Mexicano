**Cabecera — archivado post-hoc por N6; ejecutado por PR #530 (ADR-335).** Este
encargo corrió y se fusionó el 4/sep/2026 sin que su propio A.3 se cumpliera: el
texto de abajo vivía solo en una conversación, nunca en un commit empujado a este
repositorio (`ACTO MAESTRA38-N4`, el mismo día, buscó exhaustivamente —
`git log --all -S "N1-lite"` sobre todo blob de todo ref, los 11 commits de `PR
#530` uno por uno con `git show --stat` — y no lo encontró en ningún lugar
accesible; ver `forense/hallazgos.md`, entrada del 4/sep/2026, `MAESTRA38-N4`).
`ACTO MAESTRA38-N6 · PROPAGA-FP298-TESTS-Y-A3` archiva aquí, verbatim, el texto
que dirección pegó inline en su propio encargo (convención exigida por
`forense/encargos/convencion.md`: «si el texto no está en el repo, va pegado
inline o el encargo no se lanza») — reparando retroactivamente el defecto de A.3,
no reabriendo el trabajo sustantivo, que ya está ejecutado y fusionado.

---

ENCARGO · ACTO MAESTRA38-N1-lite · REPARA-TABLERO-Y-COLA (sólo repo) — invoca /acto. SHA: 68ce2a8d · COMPUERTA: ninguna · ENTORNO: NUBE · NO en CAJA · MODELO: Sonnet · CARRIL: N2 en paralelo. FIRMA — verbatim (4/sep): «Se me fue el internet y caja quedó fuera temporalmente fuera de servicio. La sesión se cortó y no pudo pushear nada. Algún encargo que podamos correr en nube?» Alcance reducido a propósito: nada que dependa de saber qué hay en disco (FP-286, FP-282, depósitos de mesa, ENFIH-4) queda fuera y se declara. A.8 contra 68ce2a8d: grep -c '^FP-291' forense/firmas-pendientes.tsv → 0 · filas CSES → 2 · ## INDETERMINADO → 46 · acto.md punto 3 sin la línea de enlace previo a compuerta. SPEC: P1 restaurar filas de 38-A1 como FP-291/FP-292 (creado=2026-09-03, nota «perdidas en merge #527»), enmienda in situ al encargo 38-A1, pegar T-FIRMAS; P2 CSES dedup (queda OBTENIDO, la PENDIENTE → SUPERADA-POR); P3 FP-290: 46 INDETERMINADO por dos reglas mecánicas (rótulo compartido hereda; resto ## CERRADO-POR-HISTORIA), FP-290 → EJECUTADA, FP-289 enterada; P4 línea en acto.md punto 3 (enlazar data/raw y raices.local.yaml antes de compuerta); P5 listar los 19 FAIL absorbidos → FP-293; hallazgos (A.12 no atrapó fila perdida; A2 ejecutado dos veces); receta de abiertas por prefijo en tramite.md. PERÍMETRO: tablero · cola (2 filas) + vista · encargo 38-A1 · 46 encargos (append) · nota N9 · acto.md · tramite.md · hallazgos · A.3 · cascada. NO toca: data/manifiesto.yaml · tests/** · tools/** · milpa/** · relaciones · estados de FP-286/282/288. FP/ADR: ADR-334 · FP-291/292 · FP-293 · FP-294 recibo. CONTADOR: abiertas 6 → 4 · medición: cero.

---

## CONSUMIDO

Ejecutado por `PR #530` (`ADR-335`, renumerado desde el candidato original
`ADR-334` al fusionar `origin/main` — `PR #529`/`MAESTRA38-N2` ya traía `ADR-334`
tomado con candidato propio idéntico derivado de forma independiente; regla de la
casa, renumera quien fusiona segundo), 4/sep/2026, entorno NUBE, restauración a
perímetro estricto. Detalle completo del qué-se-ejecutó vive en
`canon/gobernanza-v1_15.md` (entrada `ADR-335`) — resumen aquí, para que este
archivo cierre su propio A.3 sin duplicar esa fuente:

1. **`FP-291`/`FP-292` restauradas.** Declaradas por
   `forense/encargos/2026-09-03-MAESTRA38-A1-SONDA-Y-DESCARGA-UNIVERSO-1.md`
   desde el 3/sep/2026, ausentes de `forense/firmas-pendientes.tsv` — confirmado
   contra ambos padres del merge de `PR #527` (`68ce2a8`), que nunca las
   tuvieron, no que el merge las descartara. Restauradas con el contenido que el
   propio encargo `38-A1` fija, enmienda in situ en ese encargo (0 líneas
   borradas).
2. **Dedup de `CSES`.** Fila duplicada en
   `data/curacion-registro/cola-adquisicion-registro.tsv` (una `OBTENIDO`, una
   `PENDIENTE` que la sonda lateral de `38-A1` ya había superado sin retirar):
   la `PENDIENTE` pasa a `estado_A4A5=SUPERADA-POR` con nota, vista regenerada
   con el writer oficial (`tools/vista_cola_adquisicion.py`).
3. **`FP-290` (los 46 `## INDETERMINADO` de `ACTO MAESTRA37-N9`) resueltos** por
   mesa con dos reglas mecánicas: (a) heredar de hermano de rótulo compartido
   con desenlace ya sellado, 0 casos; (b) `## CERRADO-POR-HISTORIA` por append,
   46 casos — tabla en
   `forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md`. `FP-290` →
   `EJECUTADA`; `FP-289` → `ENTERADA`.
4. **`.claude/commands/tramite.md`**: receta de conteo de `ABIERTA` corregida de
   igualdad exacta a prefijo (`$6 ~ /^ABIERTA/`, subcontaba 2 de 6).
5. **`.claude/commands/acto.md` punto 3**: enlazar `data/raw`/
   `data/raices.local.yaml` desde el clon padre ANTES de evaluar la compuerta
   (defecto de `PR #522`).
6. **`tests/check.py --baseline`** en línea base: **19 FAIL** absorbidos contra
   `tests/baseline.json` (sin cambio frente al estado previo), listados en
   `forense/notas/2026-09-04-baseline-fail-absorbidos.md`; `FP-293` abierta
   para que mesa decida cuáles se pagan (luego pagados por `ACTO MAESTRA38-N4`,
   `FP-295`).

**Qué NO decidió `PR #530`.** No reabrió ninguno de los 46
`CERRADO-POR-HISTORIA` con juicio nuevo. No corrigió ninguno de los 19 FAIL
absorbidos (fuera de perímetro). No tocó `data/manifiesto.yaml`, `milpa/**`, ni
los estados de `FP-286`/`FP-282`/`FP-288`.

**Hallazgo (una línea, `ACTO MAESTRA38-N6`).** El defecto no fue el trabajo de
`PR #530` — verificado correcto contra `ADR-335` — sino que ese trabajo corrió y
se fusionó sin que A.3 lo archivara primero; este documento repara sólo eso.

**Verificación de este archivo (`ACTO MAESTRA38-N6`, 4/sep/2026).** `python3
tests/check.py`: `T-A3` (`T28`) pasa de `FAIL` a `ok` con este archivo presente
(control positivo pegado en el `## CONSUMIDO` del encargo `MAESTRA38-N6`).
