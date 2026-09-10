# ENCARGO · ACTO GEN2-M-SNAPSHOT-TRIADA

Recibido en mesa 10/sep/2026 (despacho 4/5 de la batería que la firma de
mesa pidió el 9/sep — "necesito que midas al menos 5 encargos a correr en
claude code... dame 5 completos"). Texto verbatim del lanzamiento:

> ENCARGO 4/5 · ACTO GEN2-M-SNAPSHOT-TRIADA
>
> CONGELAR AL MOTOR ANTES DE ENSEÑARLE EL EXAMEN
>
> OBJETIVO: producir el snapshot de M que competirá contra L_SOLO y
> L_CORPUS en exactamente las tareas del marco, sin modificar el motor
> después de mirar los R de evaluación.
>
> CABECERA: NUBE preferente, Opus. Si alguna emisión exige caja, separar
> únicamente esa ejecución, no cambiar el contrato. Cero nuevas
> adquisiciones.
>
> COMPUERTA: contrato TRIADA fusionado. No depende de que ENCARGO 3/5
> haya terminado, porque el snapshot de M no debe mirar R.
>
> FIRMA DE MESA:
> El motor que compite es el motor vigente congelado para evaluación, no
> una versión retocada después de ver los árbitros. Desde este snapshot y
> hasta el cierre del TRIADA-CALC no se adoptan al motor cifras
> procedentes de los targets de evaluación con el propósito de mejorar el
> duelo. Una mejora futura del motor pertenece a otra generación de
> evaluación.
> Esta firma protege la pregunta central contra overfitting accidental.
>
> P1 · CONGELAR IDENTIDAD DEL MOTOR
> Al arrancar:
>
> * derivar `origin/main`;
> * registrar hash del árbol relevante de `milpa/`;
> * hash del emisor;
> * hash/configuración de reglas, conductas, coeficientes y valores que M
>   consume;
> * fecha;
> * versión de herramientas.
>
> Tomar como referencia histórica el estado existente tras PR #674.
> Si entre #674 y este acto cambió materialmente el árbol que alimenta M,
> declarar exactamente qué cambió. No ocultarlo tras el SHA general del
> repo.
>
> P2 · REUSAR O REEMITIR
> Para las 14 celdas:
> primero verificar si los `M-<id>__v1_3.json` existentes fueron
> producidos por exactamente el mismo estado material del motor.
>
> * Si SÍ: reutilizarlos, citando hash y procedencia.
> * Si NO: reemitir M para esas celdas desde el snapshot congelado.
>
> No seleccionar entre M antiguo y M nuevo según cuál quede más cerca de
> R.
> La regla de elección se decide sólo por identidad del snapshot.
>
> P3 · FIREWALL DE OBJETIVO
> Construir para cada celda la cadena de insumos de M suficiente para
> responder: ¿algún valor que M consume es exactamente el árbitro de esa
> misma celda, la misma ola/variable objetivo o una materialización
> directa de ella?
> Estados:
>
> * `LIMPIO-DE-OBJETIVO`.
> * `CONTAMINADO-POR-OBJETIVO`.
> * `INDETERMINADO-POR-PROCEDENCIA`.
>
> No se decide por cercanía numérica.
> Una celda contaminada no se repara aquí. Se etiqueta y queda fuera de
> `U3`.
> Una calibración en otra ola/fuente puede seguir siendo válida para la
> primaria operacional, pero su aptitud para TRANSFERENCIA se decide por
> el corte secundario de la spec TRIADA.
>
> P4 · CALC/SNAPSHOT
> Crear un producto sellado que entregue, por celda:
>
> * id;
> * punto M;
> * snapshot/hash;
> * fuentes/valores materiales consumidos;
> * estado firewall;
> * corrida M reutilizada o nueva;
> * razón de exclusión si la hay.
>
> No calcular error contra R.
> La salida debe poder entregarse al ENCARGO 5/5 sin abrir nuevamente
> `milpa/`.
>
> P5 · SONDA DE INMUTABILIDAD
> Antes y después del snapshot:
> `git diff` de todo el perímetro motor = cero, salvo artefactos nuevos de
> registro/snapshot fuera de `milpa/`.
> Este acto mide al motor; no lo mejora.
>
> PERÍMETRO: artefacto snapshot/CALC M, notas, registro, 0-bis, cascada.
> NO TOCA: `milpa/` salvo lectura, R, L, capturas, extractor,
> calibraciones, adopciones.
> CONTADOR: `cuenta_gen2 = SI` para el snapshot/CALC si entra como
> resultado GEN2 con cadena completa. No crea adopción.
> CIERRE: tabla de 14 celdas con punto M y firewall; NC únicamente para
> contaminaciones/procedencias que cambien `U3`.
> SUCESOR: ENCARGO 5/5.

## NO-CORRIDO / RESERVAS

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| Verificación de la cadena de payload (M vs R) para las 8 celdas fuera de `UR` (`DIN-M-01`, `FAM-M-01/05/06/07`, `TRA-M-02/03/07`) | `NO-VERIFICABLE-AQUÍ` — no existe `R` sellado para ninguna de las 8 (`NO-EXISTE-ARBITRO`, censado por `universo-triada-v1_0.tsv`); no hay contra qué comparar el payload de calibración de `M` más allá de la vía mecánica de F-DD | su estado `LIMPIO-DE-OBJETIVO` descansa solo en que `grado_DD` da `P1 PUNTUA` (ola de calibración ≠ ola evaluada); si en el futuro se calcula `R` para alguna de estas 8, el firewall debe repetirse contra ese `R` antes de admitir la celda a cualquier universo pareado — no se hereda por default (mismo principio que `F5-contrato-triada-spec-v1_0.md` §1.4 ya fija para `UR`) | quien calcule `R` para esa celda (fuera de perímetro de este acto, que no toca `corridas-R/`) |
| Actualización de `forense/prereg-duelo-v2/universo-triada-v1_0.tsv` (columnas `M_punto_valido`/`en_U3`, hoy `PENDIENTE (snapshot ENCARGO 4/5 no existe aun)`) | `FUERA-DE-PERÍMETRO` — ese sidecar pertenece a `ACTO GEN2-F5-CONTRATO-TRIADA` (`PR #675`, ya `CONSUMIDO`); el propio contrato (`F5-contrato-triada-spec-v1_0.md` §1.3) nombra a quien ejecute P2 (presumiblemente `ENCARGO 5/5`) como quien "cierra esta fila derivando `U3` en firme" | `universo-triada-v1_0.tsv` sigue leyendo `PENDIENTE` hasta que `ENCARGO 5/5` lo reconcilie contra este snapshot y contra `NC-0144` (extracción de `L`) | `ENCARGO 5/5` (`ACTO GEN2-F5-TRIADA-CALC`) |

Ninguna contaminación ni procedencia que cambie `U3` se encontró en este
acto (14/14 `LIMPIO-DE-OBJETIVO`) — por instrucción explícita del propio
`CIERRE` de este encargo ("NC únicamente para contaminaciones/procedencias
que cambien `U3`"), no se abre ninguna fila nueva en
`forense/no-corrido.tsv`: las dos reservas de arriba son de procedencia
verificable a futuro y de perímetro, no hallazgos de contaminación.

## CONSUMIDO

`ACTO GEN2-M-SNAPSHOT-TRIADA` — **CONSUMIDO**. Ejecutado por **`PR #677`**
(rama `claude/acto-gen2-m-snapshot-ys3vn7`, contra `origin/main = da08846`,
merge de `PR #676`; `PR #674 = eab46ed` es ancestro). Entorno **NUBE**, cero
microdato, cero adquisición nueva, cero apertura de `corridas-R/`. **NO
fusionado por el ejecutor: mesa fusiona.**

**P1.** Identidad del motor congelada: `git rev-parse HEAD:milpa =
1669f8bc3f9…`; `git diff --stat eab46ed..HEAD -- milpa/` vacío (árbol
idéntico al de `PR #674`, nada material cambió en ese tramo). Hallazgo
declarado, no oculto tras el SHA general: `milpa/tramite.yaml` fue
enriquecido, **antes** de `PR #674`, con proveniencia
`corrida0_resultado_id`/`corrida0_generacion` en 9/14 conductas (`ACTO
GEN2-LOTE-ENVIPE-1`, `ACTO GEN2-PRIMERA-SILLA`, `ACTO GEN2-LOTE-ENCIG-1`) —
el dict original `{conducta,p,clase}` sobrevive intacto como prefijo del
dict vivo, y las tres remediciones `corrida0` reproducen el mismo `p`
publicado (deltas `~1e-7`–`1e-8`) sin citar ningún resultado del duelo.

**P2.** `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.py` re-deriva en
vivo, con `tools.emite_m.emite_celda` (misma función, no reimplementada),
las 14 filas de `marco-M-sorteado-v1_3.tsv` y las compara campo a campo
contra la resolución ya sellada por `ACTO MAESTRA38-M13` §16
(`M-<id>__v1_3.json > M-<id>.json > M-<id>__v1_2.json`). **14/14
`REUTILIZADAS`, 0 reemitidas** — regla de elección aplicada: solo identidad
de snapshot (`ciego_a_R` verificado mecánicamente: el script jamás abre
`corridas-R/`).

**P3.** `grado_DD` (F-DD, `ADR-237`) recomputado en vivo: **14/14 `P1
PUNTUA`**, cero `P0`. **14/14 `LIMPIO-DE-OBJETIVO`**, 0
`CONTAMINADO-POR-OBJETIVO`, 0 `INDETERMINADO-POR-PROCEDENCIA`. Para las 6
celdas de `UR` se repitió además la cadena de payload de
`F5-contrato-triada-spec-v1_0.md` §1.4: `M` calibra `envipe2025_csv`, `R`
lee `Tmod_Vic.DBF` de la ola propia de cada celda — objetos distintos,
no-comparabilidad declarada por escrito en `milpa/tramite.yaml:488`.

**P4.** Producto sellado: `forense/prereg-duelo-v2/snapshot-M-triada-v1_0.json`
— 14 celdas con `id_celda`, `punto_M`, snapshot/hash del motor, fuentes
materiales consumidas, estado firewall, corrida M reutilizada, y
`razon_exclusion` vacía en las 14 (ninguna excluida). Ningún error contra
`R` calculado en ningún punto. Entregable a `ENCARGO 5/5` sin reabrir
`milpa/`.

**P5.** `git status --porcelain` y `git diff --stat -- milpa/` vacíos antes
y después de correr el snapshot — cero cambios al perímetro del motor.

**Determinismo.** Dos corridas frescas del script producen el mismo
contenido sustantivo (verificado comparando ambas salidas con el campo
`fecha_snapshot` excluido — solo ese timestamp difiere).

**Baseline.** `python3 tests/check.py --baseline` → **VERDE**, sin `FAIL`
nuevo. 3 `FAIL` / 1688 `WARN`, los tres preexistentes (`T06`×2, `T08`).

Cascada: `ADR-451` (`canon/gobernanza-v1_15.md`), `L0`
(`canon/estado-programa-v1_12.md`), rótulo `GEN2-M-SNAPSHOT-TRIADA`
censado (`canon/registro-rotulos.tsv`). Nota de resultado:
`forense/notas/2026-09-10-GEN2-M-SNAPSHOT-TRIADA-resultado.md`. Sin `NC`
nueva (§`NO-CORRIDO / RESERVAS` arriba explica por qué: ninguna
contaminación/procedencia que cambie `U3`). Este acto no tocó `milpa/`
(salvo lectura), `R`, `L`, capturas, el extractor, calibraciones ni
adopciones.

**Reservas materiales que quedaron:** ver `## NO-CORRIDO / RESERVAS` arriba
(firewall de las 8 celdas sin `R` sellado, pendiente de repetirse si algún
día se calcula su `R`; reconciliación de `universo-triada-v1_0.tsv`,
diferida a `ENCARGO 5/5` por pertenecer al sidecar de otro acto ya
`CONSUMIDO`).

**Sucesor:** `ENCARGO 5/5` — ejecutor de P2 del contrato
`F5-CONTRATO-TRIADA` (`U3`, `MAE_X`, las tres `Δ(A,B)`, la escala de
adjudicación), con los dos insumos que `F5-contrato-triada-spec-v1_0.md`
§1.3 nombraba como pendientes ahora resueltos: extractor validado
(`tools/extrae_l_v1_3.py`, `ACTO GEN2-F5-EXTRACTOR-L-v1`) y snapshot de `M`
(este acto). Hallazgo heredado, no resuelto por este acto: bajo el
extractor validado las 96/96 capturas de las 6 celdas de `UR` son
`NO-EXTRAIBLE` (`NC-0144`), por lo que `U3` puede resultar vacío o casi
vacío incluso con el snapshot de `M` ya disponible.
