# ENCARGO · ACTO GEN2-RUTINA-DERIVADOS-1

Recibido en mesa 16/sep/2026. Texto verbatim del lanzamiento:

> CAJA · ACTO GEN2-RUTINA-DERIVADOS-1 (Opus, integral; raíz montada — la
> caja es el único entorno que puede derivar el universo)
>
> P1 · /deriva (.claude/commands/deriva.md + tools/deriva_cron.sh),
> colgado del mismo scheduler y launcher, con su propio lock y rama
> derivados/<fecha> (el patrón checkout_o_crea_censo ya resolvió las
> colisiones de nombre compartido; se reutiliza). Una corrida = cuatro
> derivaciones, todas por script, ninguna por juicio: (a) snapshot del
> universo declarado como sucesión fechada T<fecha> con
> snapshot_universe.py sobre el corpus de hoy — T0 intacto, ledger de
> inspecciones arrastrado por hash, diff T<hoy>−T<anterior> por script;
> (b) tablero_programa.py --actualiza; (c) corrida0.py registro
> --verifica en seco y status; (d) tests/check.py --baseline reportando
> solo FAIL nuevos y WARN nuevos (la firma de hoy). Abre un PR
> [DERIVADOS] <fecha> con la huella (disparador=windows-task-scheduler)
> y las cuatro deltas; si nada cambió, huella NADA-QUE-HACER y cero PR,
> como despacha.
> P2 · Primera corrida = T1, a mano dentro del acto, con el denominador
> vigente a la vista: activos declarados hoy, adquiridos, inspeccionados,
> y el porcentaje que ADR-67 dejó en 1.43% en agosto.
> P3 · Guardarraíles, escritos en el runbook (agente-tramite v1.1, mismo
> archivo, sucesión): la rutina nunca escribe canon, milpa, decisiones ni
> adopta; nunca recongela la línea base; si el diff del universo es
> material (activos que desaparecen, hashes que cambian), lo reporta como
> hallazgo A.7 en el PR y no lo resuelve. Un PR diario es lo máximo que
> produce.
> D-14 contestado, en el encargo: defecto real — tres líneas base
> derivadas sin rutina, medidas hoy (T0 un mes/1 178 PRs; tablero 50 PRs;
> suite recongelada cuatro veces a mano); cambia decisiones — el servicio
> decide qué adquirir contra el universo de agosto; cuesta menos que
> corregirlo a mano — ya lo estamos pagando en cada corte.
> Perímetro: tools/deriva_cron.sh, deriva.md, launcher (una línea),
> runbook v1.1, data/curacion-universo/ (solo sucesiones nuevas), tablero
> (bloque derivado). Concurrencia: F6-PANEL-CAJA-1 y CAJA-REACTIVOS-FD-1
> no tocan nada de esto; el servicio de adquisición comparte scheduler y
> por eso el lock propio.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Instalación real de la tarea en Windows Task Scheduler (línea sugerida en `forense/agente-derivacion-v1_0.md` §1 / `forense/cron/REGISTRO-CRON-v1_0.md` §11) | `PARO-ENTORNO` — esta caja es Ubuntu/WSL sin acceso al Task Scheduler del host Windows; mismo criterio que `forense/encargos/2026-09-01-MAESTRA34-N7-SKILLS-COLA-Y-ADQ.md` fijó para el primer cron de adquisición | la rutina no corre todavía sola cada día; sigue disponible por invocación manual (`./tools/deriva_cron.sh`) hasta que mesa instale la tarea | mesa, vía `tools/windows/instala-tarea-adquisicion.ps1` como plantilla de referencia (tarea independiente, no la misma) |
| Corrida real de punta a punta de `tools/deriva_cron.sh` (lock + `checkout_o_crea_derivados` + commit + push + PR), fuera del seam `DERIVA_CRON_SOLO_DEFINE` | `NO-VERIFICABLE-AQUÍ` — la suite ambiental estaba `ROJO` (`T16`, drift ajeno) cuando se probó cada función por separado, y forzar la corrida real después de corregirlo habría abierto un segundo PR `[DERIVADOS] 2026-09-16` concurrente con el de este mismo acto, confuso para mesa el mismo día. Cada una de las cuatro funciones se ejerció por separado (P2, T1) y la sintaxis completa se verificó (`bash -n`) | falta la primera corrida disparada por el propio mecanismo automático (lock/heartbeat/trap/checkout(main)/push/PR real, no solo sus funciones) | la primera corrida real, disparada por `windows-task-scheduler` una vez mesa instale la tarea, o una invocación manual explícita post-merge |
| Prueba automatizada del script (`tests/test_deriva_cableado.py`, mismo patrón que `tests/test_adq_cableado.py` sobre el seam de solo-definición) | `FUERA-DE-PERÍMETRO` — el encargo declara perímetro cerrado a `tools/deriva_cron.sh, deriva.md, launcher, runbook, data/curacion-universo/, tablero`; no nombra `tests/` | el seam `DERIVA_CRON_SOLO_DEFINE` existe y quedó listo (mismo mecanismo que el precedente), pero nada en la suite lo ejercita todavía | acto futuro que amplíe el perímetro a `tests/`, o mesa si decide que aplica ahora |
| Cifra de "inspeccionado" distinta de "adquirido" (P2 las pide juntas; `ADR-67` ya las conflacionaba igual) | `NO-VERIFICABLE-AQUÍ` — el conteo compacto de `snapshot_universe.py` no distingue las dos; un desglose real exigiría cruzar contra `data/curacion-universo/ledger-inspecciones-*.tsv`, fuera de lo que P1 deriva | la cifra de T1 (1274/38364=3.32%) hereda la misma conflación de `ADR-67`, no mide inspección per se | quien recalcule contra los ledgers de inspección si mesa pide el desglose |
| Reconciliación de los 318 activos de diferencia entre el denominador textual de `ADR-67` (35 708) y el de `snapshot-t0.json` congelado (36 026) | `NO-VERIFICABLE-AQUÍ` — ambos describen el mismo universo en instantes de captura distintos; este acto no tiene evidencia de cuál comando produjo cuál cifra | la comparación de T1 usa 36 026 (el denominador de `T0`), declarado explícitamente en vez de silenciado | `SIN-ASIGNAR` |
