ENCARGO · ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166 — invoca /acto

SHA de redacción: 2e79d153 · COMPUERTA: ninguna. ENTORNO ASIGNADO: NUBE, en paralelo con N8 (perímetro disjunto: sólo forense/encargos/*.md, convencion.md, tablero). MODELO SUGERIDO: Sonnet (derivación mecánica contra ADR/PR; lo no derivable se lista, no se decide).

FIRMA DE MESA — verbatim (D9): «hagamos la auditoría de una vez, si no reitero, nos quedamos con pendientes abiertos.»

═══ A.8 ═══ Digesto del 3/sep: 305 .md en forense/encargos/, 303 con prefijo de fecha; con marca ## CONSUMIDO 137; sin marca 166 = 98 en/después del piso (18 marcados NO MARCAR por la skill) + 68 anteriores (5–17/ago). canon/gobernanza-v1_15.md cita rótulos de acto por ADR (327 ADR): es la fuente de derivación.

SPEC — dos commits. COMMIT-1 congela la lista de los 166 con el comando del digesto. COMMIT-2: por cada encargo, derivar por comando (grep -c "<RÓTULO>" canon/gobernanza-v1_15.md canon/registro-rotulos.tsv + git log --grep + PR en cabecera de gobernanza) exactamente una de cuatro marcas, append al final del archivo, texto intocable: ## CONSUMIDO (ADR/PR citados) · ## SUSTITUIDO (por qué archivo) · ## NO-EJECUTADO (cero rastro en 327 ADR ni en git log, con el comando) · ## INDETERMINADO (rastro parcial: rótulo compartido, ADR que lo cita sin PR, etc. — se lista, no se marca). Tabla resumen en forense/notas/2026-09-0X-MAESTRA37-N9-auditoria-encargos.md con los cuatro conteos y la lista íntegra de INDETERMINADO para mesa. convencion.md gana la línea: «la ausencia de marca en un encargo anterior a 2026-08-18 se resolvió por auditoría el <fecha>; desde entonces toda marca ausente es defecto». .claude/commands/tramite.md: el digesto D.2 (pasivo histórico) pasa a reportar 0 o lo que quede INDETERMINADO.

PERÍMETRO. Toca: forense/encargos/*.md (append de una sección, 166 archivos) · forense/encargos/convencion.md · forense/notas/…N9… · .claude/commands/tramite.md (una línea) · tablero (recibo) · A.3 · cascada. NO toca: nada fuera de forense/encargos/, forense/notas/, la skill de trámite y el tablero. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

FP/ADR: ADR-329 (deriva) · FP-286 recibo · FP-287 sólo si INDETERMINADO > 0 (lista para mesa, con fecha vence a 7 días). CONTADOR: encargos sin marca 166 → declara el real · medición: cero.

## CONSUMIDO

Ejecutado el 3/sep/2026 en entorno NUBE con la skill `/acto` (`ADR-237`),
rama `claude/auditoria-encargos-maestra37-p8k51b`, cascada en `ADR-330`
(candidato original `ADR-328`; renumerado al fusionar `origin/main`/`PR #523`,
commit `d96bf44`, que ya llevaba fusionados `ADR-328`/`ADR-329` de
`MAESTRA37-N8` — regla de la casa, "renumera quien fusiona segundo").
Commits: `89d9eb2` (COMMIT-1, congela universo de 166), `867fbe3`
(COMMIT-2, deriva y marca los 166), más este commit de cierre y cascada.

Resultado: **107 `## CONSUMIDO`** · **46 `## INDETERMINADO`** (lista
íntegra para mesa en `forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md`,
`FP-287`, vence 2026-09-10) · **13 `## NO-EJECUTADO`** · **0
`## SUSTITUIDO`** (ningún caso mostró evidencia positiva de reemplazo con
la misma fuerza que un ADR de ejecución o una nota de cierre; no se forzó
la marca sin evidencia — declarado, no rodeado). `forense/encargos/convencion.md`
y `.claude/commands/tramite.md` §3.3 actualizados: la ausencia de marca en
un encargo anterior a 2026-08-18 queda resuelta por esta auditoría; en
adelante toda marca ausente es defecto. `canon/registro-rotulos.tsv`
censa `MAESTRA37-N9`. `python3 tests/check.py --baseline` → **VERDE**
(19 FAIL · 171 WARN, nada nuevo frente a `tests/baseline.json`).

Recibo `FP-286`. Deuda abierta `FP-287` (los 46 `INDETERMINADO`, mesa
decide archivo por archivo).
