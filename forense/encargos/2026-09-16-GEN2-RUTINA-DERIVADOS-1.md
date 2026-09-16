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

## CONSUMIDO

`ACTO GEN2-RUTINA-DERIVADOS-1` — **CONSUMIDO**. Ejecutado por **`PR #814`**
(rama `acto/gen2-rutina-derivados-1`, contra `origin/main`; base al arrancar
`ce25695`, con dos merges de `origin/main` absorbidos durante el acto —
`84bd7fd` y `09dcf7d` — el segundo con conflicto real de renumeración contra
`PR #811`/`ACTO GEN2-E1-DISENO-CALIBRACION-1`, resuelto: `ADR-527`→`ADR-528`,
`NC-0261..0265`→`NC-0264..0268`). Entorno **CAJA** (Ubuntu/WSL2, `data/raw`
montado por symlink, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir), cero
llamadas a modelo dentro de la propia rutina, cero adquisición. **NO
fusionado por el ejecutor: mesa fusiona.**

**P1.** `tools/deriva_cron.sh` + `.claude/commands/deriva.md` +
`forense/agente-derivacion-v1_0.md` instaurados. Cuatro derivaciones por
script (suite primero, universo fechado, tablero, registro en seco), lock y
rama propios, sin invocar modelo. Hallazgo A.7 declarado sobre el launcher
(`tools/adquiere_launcher.sh` es adquisición-específico; entrada
independiente en `forense/cron/REGISTRO-CRON-v1_0.md` §11, sin tocarlo).
Materialidad del universo refinada tras medirla en T1 (el hash compuesto no
es señal por sí solo). `T27 T-INFRA`, defecto propio de la familia fechada,
corregido dentro del mismo acto (exención por regex).

**P2.** T1 a mano ejecutado (`forense/notas/2026-09-16-GEN2-RUTINA-
DERIVADOS-1-t1.md`): denominador vigente 1274/38364=3.32% frente al
509/35708=1.43% que `ADR-67` dejó en agosto. Sin hallazgo material. Tablero
refrescado (50 PRs de atraso, confirma D-14).

**P3.** Guardrails escritos en `forense/agente-derivacion-v1_0.md` §0 y en
`.claude/commands/deriva.md` §0: nunca canon/milpa/decisiones/adopción,
nunca `--freeze`, hallazgo A.7 si el diff del universo es material (no
resuelto por la rutina), un PR diario máximo. **Desviación declarada:** no
se escribió como enmienda a `forense/agente-tramite-v1_0.md` (perímetro
duro cerrado de esa pieza, incompatible) — runbook propio, razón explicada
en la cabecera de `forense/agente-derivacion-v1_0.md`.

**D-14.** Confirmado por T1: T0 sin refrescar un mes/1178 PRs, tablero 50
PRs, suite recongelada cuatro veces a mano.

**Cascada:** `ADR-528` (`canon/gobernanza-v1_15.md`), `L0`
(`canon/estado-programa-v1_13.md`), rótulo `GEN2-RUTINA-DERIVADOS-1`
censado (`canon/registro-rotulos.tsv`). `NC-0264..0268` nuevas (ver
`## NO-CORRIDO / RESERVAS` arriba). `tests/check.py --baseline` → **VERDE**,
3 FAIL · 4351 WARN (los 3 FAIL heredados del corpus documental, ajenos a
este perímetro).

**Perímetro respetado:** cero escritura en `milpa/`, cero decisión de mesa
tomada por el ejecutor, cero adopción, `data/curacion-universo/` solo con
la sucesión fechada nueva (`T0` intacto).
