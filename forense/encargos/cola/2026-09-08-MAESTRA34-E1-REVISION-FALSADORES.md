ESTADO: CONSUMIDO
ENTORNO: NUBE
ENCOLADO: 2026-09-02 · gesto de encolado, precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026)
BITACORA:
- 2026-09-02 · LISTO-NUBE · encolado por PR [COLA] encola MAESTRA34-N7 y MAESTRA34-E1. COMPUERTA propia del encargo: NO-LANZAR-ANTES-DE 2026-09-08 (fecha del sistema ≥ 2026-09-08, verifica `date -u`) Y digesto del día existente en forense/digesto/. Si falta cualquiera, cero commits.
- 2026-09-02 · CONSUMIDO · ejecutado con la skill `/acto` en rama `claude/maestra34-e1-falsadores-ou8qcp`; compuerta sustituida (digesto del día) verificada CUMPLE; detalle en `forense/notas/2026-09-08-MAESTRA34-E1-revision-falsadores-cierre.md`, ADR-285.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

ENCARGO · ACTO MAESTRA34-E1 · REVISION-FALSADORES — invoca /acto
SHA de redacción: e4af4ed. Redacta dirección (Fable), 1/sep/2026, contra v2.12, para ejecutarse el 2026-09-08 (FP-226, adelanto D5-b: «D5-b si ya dio frutos se mantiene»). Estado: GATED por FECHA — NO-LANZAR-ANTES-DE: 2026-09-08. Acto de DIRECCIÓN: decide con evidencia, no mide.

ENTORNO ASIGNADO: NUBE. NO se lanza en UBUNTU. MODELO SUGERIDO: Fable (auditoría de dirección, D-13); Opus aceptable.
COMPUERTA: fecha del sistema ≥ 2026-09-08 (verifica `date -u`) Y digesto del día existente en forense/digesto/. Si falta cualquiera, cero commits.

FIRMAS DE MESA — verbatim: 1/sep/2026 «D5-b si ya dio frutos se mantiene» (criterio de este acto: cada pieza se juzga por su fruto medido; la que lo tenga se mantiene). 13/ago/2026, v2.12 «Falsador y caducidad. Si en un mes (a) la skill no evita ni un solo acto perdido por compuerta, o (b) el tamaño mediano de encargo no baja al menos 50%, o (c) un lote deja pasar un defecto de contenido que el formato largo habría atrapado — a juicio de mesa, con el caso citado —, se revierte la pieza que falló y se anota». Este acto PROPONE veredictos; mesa firma.

═══ VERIFICACIÓN DE EXISTENCIA (A.8) — dirección contra e4af4ed ═══
(1) ESTRUCTURA: tabla «Falsadores vivos y su fecha de revisión» al pie del digesto diario (forense/agente-tramite-v1_0.md §3 la genera desde .claude/commands/*.md y forense/agente-*.md); instrucciones-proyecto-v2_12.md l.416 (falsador D-10..D-13); tablero FP-222 (30/sep, original) y FP-226 (8/sep, sucesor).
(2) CONTENIDO: el digesto del 1/sep lista 5 piezas con falsador (/acto, agente y skill de trámite, agente y skill de despacho) y declara 2 con falsador «en un mes» fuera de la tabla (revisa.md, agente-revisor-v1_0.md) — hallazgo pendiente. Revisión previa de falsadores: NO-ENCONTRADO (`ls forense/notas | grep -i falsador` → solo fichas de reglas, no de piezas de operación). Evidencia acumulada al 1/sep, a re-derivar el 8/sep, no heredar: compuertas que pararon con cero commits (MAESTRA33-E6, MAESTRA33-E13 ×2, MAESTRA33-S2, MAESTRA34-N2 ×1, MAESTRA34-N3 ×2 → `grep -l "cero commits" forense/notas/2026-0[89]*.md | wc -l`); tamaño mediano de encargo (MAESTRA34 50 líneas vs MAESTRA32 63 vs formato largo previo a v2.12 — deriva con `wc -l` por serie); BLOQUEA del revisor (6 en la calibración A1; comentarios en PRs #442–#455, mesa los lee en GitHub); duplicados de nube (0 desde D4-a: verificar `git log --merges` sin rótulo repetido).
(3) COBERTURA RETROACTIVA: la tabla del digesto nace el 31/ago; las piezas de v2.12 nacen el 13/ago — el «mes» de v2.12 vence el 13/sep, este acto adelanta 5 días por firma.

PIEZAS
P1 · UNIVERSO. Lista completa de piezas con falsador: las 5 de la tabla + las 2 fuera de ella (revisa, agente-revisor) + las 4 reglas de v2.12 (D-10 skill, D-11 lotes, D-12 formato corto, D-13 modelos/agente) + A.13 y A.10/A.12 si su ventana de tres meses no ha vencido (deriva de sus fechas). Conteo A.13 de archivos examinados.
P2 · POR FALSADOR: (i) texto del falsador verbatim; (ii) evidencia derivada por comando, con salida cruda; (iii) veredicto SOBREVIVE / CAE / SIN-DATO; (iv) si CAE: la pieza exacta que se revierte y el commit que la introdujo; (v) si SIN-DATO: qué medición faltó y quién la produce. Prohibido juzgar sin comando (A.13) y prohibido «sobrevive» por ausencia de evidencia — eso es SIN-DATO.
P3 · CASO (c) DE v2.12. Buscar activamente un defecto de contenido que un lote dejó pasar y el formato largo habría atrapado: revisar los ADR de lotes (MAESTRA33-L1, MAESTRA34-L1/L2) contra sus notas de cierre y los comentarios del revisor. Si no aparece ninguno, se dice con el universo examinado; si aparece, se cita el caso (la firma es «a juicio de mesa, con el caso citado»).
P4 · CIERRE. Nota forense/notas/2026-09-08-MAESTRA34-E1-revision-falsadores.md; enmienda fechada en instrucciones-proyecto-v2_12.md al pie del bloque D-quater («revisión del 8/sep: resultado») sin subir versión; las 2 piezas fuera de tabla entran a la tabla (corrige el runbook de trámite §3 o el archivo de la pieza, lo que el digesto exija); FP-226 → EJECUTADA con veredictos PROPUESTOS; FP-222 → cerrada como sustituida por FP-226. Propuesta a mesa en lenguaje de RH: por pieza, mantener / revertir / medir más, con lo que cada opción desbloquea.

PERÍMETRO Y CONCURRENCIA: forense/notas/ · instrucciones-proyecto-v2_12.md (enmienda fechada al pie, A.9: mesa la pega en el proyecto de Claude en el mismo acto) · forense/agente-tramite-v1_0.md o las dos piezas fuera de tabla (solo su línea de falsador) · tablero · A.3 · cascada. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
FP/ADR CANDIDATOS: deriva al arrancar el 8/sep.
CONTADOR: cero directo, declarado (dirección).
LO QUE NO HACE: no revierte nada por sí mismo (propone; mesa firma); no toca skills salvo su línea de falsador; no mide.
SUCESORES: los actos de reversión que mesa firme, si alguno · la revisión de los tres meses de A.10/A.12/A.13 en su fecha.

──── ENMIENDA FECHADA (MAESTRA34-N8, 2026-09-02) — al pie, cuerpo verbatim arriba intacto ────

COMPUERTA (sustituye): digesto del día existente en forense/digesto/. La
fecha 2026-09-08 pasa a ser `vence`, no compuerta. Ejecutable desde hoy.

Nota de nombre de archivo: no se renombra a `2026-09-02-…` porque
`/despacha` toma el `LISTO-NUBE` más antiguo por nombre de archivo —
renombrar a una fecha anterior lo adelantaría en la cola, no lo dejaría
al final; la condición para renombrar (dejarlo al final indebidamente)
no se cumple.

## CONSUMIDO

Ejecutado por `ACTO MAESTRA34-E1 · REVISION-FALSADORES` (`ADR-285`), rama
`claude/maestra34-e1-falsadores-ou8qcp`, `PR #463`. Detalle:
`forense/notas/2026-09-08-MAESTRA34-E1-revision-falsadores-cierre.md` —
sufijo `-cierre` añadido sobre el nombre que P4 nombra arriba (mismo
patrón que las demás notas de cierre, p. ej.
`2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md`): el nombre sin sufijo
colisiona en `T02` (nombre normalizado) contra este mismo archivo de
cola, que CI trata como `FAIL` nuevo y bloquea el merge; con el sufijo,
`tests/check.py --baseline` queda VERDE.
