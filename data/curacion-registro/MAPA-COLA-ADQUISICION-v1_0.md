# P1 · Mapa columna→hogar de `data/cola-adquisicion-v1_0.tsv`

`ACTO MAESTRA33-A5 · RECONCILIA-ADQUISICION-CON-CURADOR`, 1/sep/2026.
Deriva contra `data/INFRAESTRUCTURA-v1_0.md` Dominios 1-3 y
`tools/curador_registro/GUIA-CURADOR-REGISTRO.md`, base `08101ad`
(main tras el merge de PR #437/#439, sin cambios de perímetro respecto al
`1fbefd6` que declaró el encargo — verificado, `git diff 1fbefd6 08101ad --
data/ tools/curador_registro/ .claude/commands/adquiere.md
tools/digesto_tramite.py` vacío).

Siete columnas de `cola-adquisicion-v1_0.tsv`. Ninguna tenía hogar en el
registro antes de este acto (`grep "cola-adquisicion-v1_0|adquiere"
data/INFRAESTRUCTURA-v1_0.md` → 0, A.8 del encargo). El veredicto por
columna:

| columna | ¿hogar preexistente? | hogar (post-acto) | script que escribe |
|---|---|---|---|
| `fuente_canonica` | Parcial. `data/curacion-registro/aliases-fuentes.tsv` normaliza *algunos* nombres de fuente (4 filas hoy: ENASIC/ENBIARE/ENFIH/ENSAFI); `data/curacion-universo/universo-declarado-t0.tsv` tiene `fuente_programa` para activos T0. Ninguna cubre las 73 filas de la cola. | `data/curacion-registro/cola-adquisicion-registro.tsv`, columna `fuente_canonica_normalizada` (resuelta contra `aliases-fuentes.tsv`; sin match declarado `SIN_ALIAS`, no forzado). | `tools/curador_registro/registra_cola_adquisicion.py` |
| `estado_A4A5` | **HUECO** — no hay tabla del registro con este vocabulario de estado (`OBTENIDO`/`PENDIENTE`/`NO-ACCESIBLE`/`NO-OBTENIDO-POR-ESTE-AGENTE(N)`). `decisiones-adquisicion.tsv` (Dominio 3) tiene su propio vocabulario de `estado` (`VIGENTE`/`EVIDENCIA_LOCALIZADA`) para decisiones, no para filas de cola. Los dos vocabularios no son intercambiables (confirmado, mismo patrón que la trampa #5 del Dominio 2: dos mecanismos con vocabulario compartido y sin conexión). | `cola-adquisicion-registro.tsv`, columna `estado_A4A5` (se conserva el vocabulario propio de la cola — no se reescribe como estado de decisión, sería inventar equivalencia no verificada). | `tools/curador_registro/registra_cola_adquisicion.py` |
| `prioridad` | **HUECO** — ninguna tabla de Dominio 1-3 tiene un campo de prioridad de caminata. | `cola-adquisicion-registro.tsv`, columna `prioridad`. | `tools/curador_registro/registra_cola_adquisicion.py` |
| `url_conocida` | Parcial. `manifiesto.yaml` tiene `url_origen`/`url_origen_sugerida` pero solo para payloads ya `OBTENIDO`; `universo-declarado-t0.tsv` tiene `url_localizador_principal` pero solo para activos T0 (no para las 73 filas de la cola, que no son activos T0). | `cola-adquisicion-registro.tsv`, columna `url_conocida`, con cita cruzada a `id_manifiesto` cuando la fila ya está `OBTENIDO` (evita duplicar la URL confirmada de `manifiesto.yaml`, solo la referencia). | `tools/curador_registro/registra_cola_adquisicion.py` |
| `ids_manifiesto` | **EXISTE-SATISFACE.** Es un puntero a `data/manifiesto.yaml`, que ya es su hogar real y ya tiene vía de escritura verificada (`tests/manifiesto.py --registra`/`--promueve`, Dominio 1). Esta columna de la cola es cita, no dato primario. | `data/manifiesto.yaml` (sin cambio; la cola solo cita el id). | `tests/manifiesto.py` (ya existente, Dominio 1) |
| `origen` | **HUECO** para su función específica en la cola (procedencia de la fila dentro del propio linaje de colas de agosto — `cola-adquisicion-2026-08-12.tsv:N`, `cola-ext-*-2026-08-06.tsv:N`, notas de mapeo `/mapea`). Ninguna tabla de Dominio 1-3 registra procedencia de fila entre colas. | `cola-adquisicion-registro.tsv`, columna `origen`, más `fila_origen` (cita `cola-adquisicion-v1_0.tsv:<n>` de la migración misma, A.13). | `tools/curador_registro/registra_cola_adquisicion.py` |
| `nota` | **HUECO** como campo libre de bitácora de caminata (payloads, códigos de red, recetas). Los campos `nota`/`justificacion`/`observaciones` de otras tablas (Dominio 1 y 3) cumplen función análoga pero para otro objeto (relación, activo, alias) — no para "intento de adquisición de esta fila". | `cola-adquisicion-registro.tsv`, columna `nota` (texto verbatim migrado, sin reescritura). | `tools/curador_registro/registra_cola_adquisicion.py` |

## Veredicto

Cinco de siete columnas (`estado_A4A5`, `prioridad`, `url_conocida`,
`origen`, `nota`) eran hueco real del índice — ninguna tabla de Dominio 1-3
las cubría. Este acto no inventa una vía forzando esas columnas dentro de
una tabla existente con otro contrato (p. ej. no se fuerza `estado_A4A5`
dentro de `decisiones-adquisicion.tsv`, cuyo vocabulario de `estado` mide
otra cosa). En su lugar, **crea el hogar que P4 registra en
`INFRAESTRUCTURA-v1_0.md` Dominio 1/3**: `data/curacion-registro/
cola-adquisicion-registro.tsv`, escrita únicamente por
`tools/curador_registro/registra_cola_adquisicion.py` — la vía que la
FIRMA DE MESA pide ("migramos todo al oficial") en vez de dejar la cola
huérfana indefinidamente. `fuente_canonica` e `ids_manifiesto` sí tenían
hogar parcial/total preexistente y se resuelven contra él, no se
reinventan.
