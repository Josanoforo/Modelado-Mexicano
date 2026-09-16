# T1 · primera corrida a mano de la rutina de derivación (P2)

`ACTO GEN2-RUTINA-DERIVADOS-1`
(`forense/encargos/2026-09-16-GEN2-RUTINA-DERIVADOS-1.md`, P2). Las cuatro
derivaciones de `tools/deriva_cron.sh` se ejercitaron a mano, dentro de
este acto, invocando las mismas funciones que la corrida programada usa
(`DERIVA_CRON_SOLO_DEFINE=1`, seam de solo-definición, sin lock ni commit
automático) — "por script, no por juicio" se cumple porque cada número
de abajo sale literalmente de esas funciones, no de una lectura manual.

## (a) Universo declarado — el denominador vigente que P2 pide a la vista

`data/curacion-universo/derivados/universo-2026-09-16.json`, comparado
contra `data/curacion-universo/snapshot-t0.json` (T0, congelado en
agosto, intacto — nunca se escribió).

| | T0 (agosto, congelado) | hoy (16/sep/2026) |
|---|---:|---:|
| activos declarados (`componentes_declarados_conservadores`) | 36 026 | 38 364 |
| adquirido/inspeccionado (`identidades_locales_verificadas`, misma conflación que `ADR-67`) | 509 | 1 274 |
| **porcentaje** | **1.41%** (509/36 026) | **3.32%** (1 274/38 364) |

**Comparación con `ADR-67` (mesa, 10/ago/2026, `canon/gobernanza-v1_15.md:1139`):**
esa decisión citó **509 de 35 708 activos declarados (1.43%)** como el
denominador vigente en ese momento. El `36 026` que trae `T0` congelado
difiere en 318 del `35 708` que cita `ADR-67` — ambos números describen
el mismo universo a instantes de captura ligeramente distintos (la
decisión de mesa y el congelamiento mecánico de `T0` no fueron el mismo
comando); no se reconcilia esa diferencia de 318 aquí, queda declarada.

**Lectura del movimiento desde agosto:** el numerador **más que se
duplicó** (509 → 1 274, ×2.50) mientras el denominador creció **más
lentamente** (36 026 → 38 364, ×1.065) — el mismo patrón que "los cierres
se sellaron cuando `ADR-67` medía 509/35 708" describe:  un universo que
sigue creciendo bajo la doctrina de estampa de universo de `ADR-67`
("ningún sello previo se trata como final"). La fracción de activos
adquiridos/inspeccionados subió de **1.41%** a **3.32%** — una mejora
real, y sigue siendo un universo mayoritariamente sin inspeccionar. La
cifra "adquirido e inspeccionado" aquí conflacionadas es la misma
conflación que `ADR-67` usó; un conteo de inspección per se (distinto de
adquisición) vive en `data/curacion-universo/ledger-inspecciones-*.tsv`
y no se recalcula en esta lectura T1.

**Material (activos que desaparecen / discrepancias de hash nuevas):**
ninguno. `discrepancias_hash_local` **bajó** (3→2, menos discrepancias
que en agosto, no más) y ningún conteo de activos bajó — sin `HALLAZGO
A.7` en esta corrida. El hash compuesto del snapshot cambió (esperado:
el universo creció 52→81 `inputs`), pero un cambio de hash por
crecimiento legítimo no se trata como material (ver comentario de
`tools/deriva_cron.sh::deriva_universo` sobre por qué el hash compuesto
por sí solo no es la señal — sería ruido diario).

## (b) Tablero

`tools/tablero_programa.py --actualiza` sobre `forense/tablero/
TABLERO-PROGRAMA.md`: bloque `<!-- TABLERO-DERIVADO -->` actualizado (24
inserciones, 25 eliminaciones) — no se tocaba en 50 PRs (premisa D-14 del
encargo, confirmada).

## (c) Registro (en seco)

`corrida0.py registro --verifica` (sin `--escribe`, no tocó ningún TSV):
diff proyectado sobre `resultado_replay`/`contexto_replay` para las
corridas selladas re-verificadas — salida cruda en
`forense/deriva-log/2026-09-16.log`.

`corrida0.py status`: `dependencias_numericas_legacy_activas=183 ·
N_resultados_gen2_sellados=3522 · N_resultados_gen2_pendientes_adopcion=12
· N_resultados_gen2_vetados_por_decision=2 ·
N_resultados_gen2_adoptados_activos=24 ·
resultados_con_validacion_independiente=215 · diferencias_materiales=0 ·
no_corrido_abiertas=64 · replays_legacy_sellados=5 ·
corredores_envueltos_legacy=21`.

## (d) Suite en línea base

`tests/check.py --baseline`: **ROJO en el momento de esta lectura** — 1
entrada nueva, `T16` (`canon/gobernanza-v1_15.md` cita un WARN vigente
que ya no coincide con la corrida real). **No causado por este acto**:
ni `canon/gobernanza-v1_15.md` ni el WARN citado se tocaron aquí; es
arrastre esperable de la actividad concurrente del programa (decenas de
actos cerrando el mismo día, cada uno mueve la cifra real de WARN). Se
corrige como parte de la propia edición de `canon/gobernanza-v1_15.md`
que este acto hace en su cascada de cierre (añadir la entrada `ADR`
propia toca esa misma vecindad de línea) — verificado de nuevo,
fresco, inmediatamente antes de esa edición, no reutilizando esta
lectura.

**Esto confirma, operacionalmente, el gate que `tools/deriva_cron.sh`
implementa:** una corrida automática hoy habría terminado en
`PARO-SUITE-ROJA` con cero commits, exactamente el guardrail de P3 ("la
suite corre primero; ROJO no apila universo/tablero encima"). El
universo y el tablero de este documento se corrieron a mano, fuera de
esa compuerta, precisamente porque P2 pide ver el denominador **dentro
de este acto** — la corrida automática de mañana sí quedará sujeta a la
compuerta.
