# ADR del sello del motor — esqueleto, SIN sellar

### 14 de agosto de 2026 · ACTO S7-MOTOR-2-AMANUENSE · `cloud_default`, repo-only

> | | |
> |---|---|
> | **ARCHIVO** | `ADR-MOTOR-2-esqueleto-2026-08-14.md` |
> | **QUÉ ES** | El esqueleto del ADR de ocho incisos que `forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md` §6 manda escribir, con las **seis** ranuras de firma de M1-M6 vacías. Insumo directo de MOTOR-2 |
> | **QUÉ NO ES** | **No es el ADR sellado.** No lleva número, no entra a `canon/gobernanza-v1_15.md`, y no cierra ninguna de las seis preguntas. Sellarlo es acto de mesa, no de este acto |
> | **NÚMERO DEL ADR** | **No se pone aquí.** Se deriva con la receta de T15 contra el `main` real en el momento de sellar — el propio §6 lo advierte: *"el número no se hereda de ningún documento, incluido éste"* (cinco colisiones históricas). Al derivar esta cascada, `ADR sellados = 83`, así que el candidato es **84**, pero esa cifra se re-deriva al sellar, no se copia de aquí |
> | **TRABAJO DE MESA** | **Seis renglones, entre comillas** — una firma verbatim por cada M, en las ranuras marcadas `[FIRMA M_ — VACÍA]`. Los incisos (7) y (8) no son ranuras de firma: su texto ya lo fija el §6 del encargo y va reproducido tal cual |

---

## Precondiciones del sello — estado medido hoy, no al abrir el ADR

- **Compass ×3 + RT-B/RT-D en repo (cadena A.3 de CAREO cerrada).** **Incumplida.** `forense/encargos/2026-08-14-MOTOR-1-consolidado.md` — tercera sesión consecutiva en que los cinco archivos no llegan (`find . -iname "*compass*"` → `0`). Mientras siga así, un ADR que cite CAREO cita ausentes.
- **Veredicto RONDA-M sobre la mesa.** **Cumplida.** `forense/RONDA-M-motor-matriz-veredicto-opus-2026-08-13-v1_0.md` — **APROBAR CON CAMBIOS**, doce defectos materiales (siete bloquean el sello de la propuesta, no de este ADR), ninguno conceptual.
- **Numeración derivada AL SELLAR con T15 contra el `main` real.** Pendiente por definición — no se satisface antes de sellar.

**Conclusión de precondiciones: el ADR no es sellable hoy.** La primera sigue incumplida. Esto no impide preparar el esqueleto; impide firmarlo.

---

## (1)-(6) · Las seis M, cascada ≤3 líneas + ranura de firma vacía

Preguntas verbatim de `propuesta-motor-matriz-v0_1.md` §9 (`:214-219`); cascada derivada en `forense/CASCADA-M1-2026-08-14.md` §2.

### M1 · ¿Se adopta el cómputo matricial como definición del ejecutable —la reescritura que el banner de ADR-62 espera— con el ABM por agentes como modo derivado; y procede antes del gate de Fase 1 de `milpa-plan`, o espera su veredicto?

> Toca: `milpa-spec:4` (banner: resolver o reescribir) + el renombre a v0.3 con universo de **8 archivos** · `milpa-plan:106,140,156` (la rama que se firme) · `modelo:262,640` (los 22 g.l. cambian de forma) · `procedencia:705-716` (la lista de `B` pasa a leerse como matriz, sobre **siete** clases, no seis).
> Contadores: **`ADR 83 → 84`**. Ningún otro. `0 de 15` explícitamente no (`propuesta:206`); `4 de 144` explícitamente no (`propuesta:200`).
> Si se firma incompleta —solo el banner, sin la rama del gate— queda un ADR que no dice cuándo procede lo que autoriza: por eso el encargo la marca **M1 COMPLETO**.

**Firma de mesa (M1):** `[FIRMA M1 — VACÍA]`

---

### M2 · Granularidad `D`: ¿cortes iniciales por eje (respetando los tres ejes de hogar), y quién los sella?

> Toca: `modelo` §1.1.A (el vector de atributos y sus ejes) y, en cascada, cuáles momentos son computables por celda — es decir, el inciso (5) de `gobernanza:465`.
> Contadores: **ninguno directo.** Indirecto y real: `D` fija cuántos momentos entran al denominador de identificación de §4.1 (*"número de momentos informativos ≥ número de parámetros libres"*).
> Sin dueño de sello, M2 es el hueco por donde `D` se fija por default al escribir el primer catálogo — y `propuesta:207` declara que `D` se sella en el commit 1 del catálogo, o sea en M4.

**Firma de mesa (M2):** `[FIRMA M2 — VACÍA]`

---

### M3 · ¿Se acepta campo medio como tratamiento declarado de `G1b` mientras conserve estatus HIPÓTESIS?

> Toca: `propuesta` §1.7 (`G1b`, "la única excepción, declarada" — campo medio como aproximación) y la fila `G1` de `B` en `procedencia:705`, que agrupa lo que ADR-20 desdobló: el `−0.60` está adjudicado a **G1a**, y `G1b` va **"a revisión — el generador está contradicho"** (`modelo:403`).
> Contadores: **ninguno.** `G1b` no entra ni sale del `0 de 15` por aceptarse un tratamiento; sigue `ASIGNADO`.
> Es la M más barata de firmar y la más fácil de olvidar: si no se firma, la matriz tiene una celda cuyo tratamiento es implícito, que es la clase de cosa que §1.7 existe para impedir.

**Firma de mesa (M3):** `[FIRMA M3 — VACÍA]`

---

### M4 · ¿El catálogo de momentos se constituye como el pre-registro que `gobernanza:461` exige, con roles `AJUSTE`/`HOLDOUT` sellados en commit 1?

> Toca: **archivo nuevo** (el catálogo `M`), con la forma de §3.1 y las tres obligaciones heredadas; salda la deuda que el inciso (3) declaró y no creó. Y es la mitigación que el veredicto de Ronda 1 pide contra doble uso de datos y contra D8.
> Contadores: **ninguno al constituirlo** — declara demanda, no mide.
> Es la única M que salda una deuda ya escrita en `canon/`; las otras cinco autorizan trabajo nuevo. Firmarla sin la regla anti-circularidad de §3.3 (roles ANTES del escaneo) la vacía.

**Firma de mesa (M4):** `[FIRMA M4 — VACÍA]`

---

### M5 · ¿El curador deriva sus necesidades del libro de demanda (fuente única), o mantienen listas separadas con cruce declarado?

> Toca: `tools/curador_registro/` (**19** scripts, medido) y `data/curacion-registro/necesidad-objeto-modelo.tsv`. ADR-68(a) ya selló que el motor del curador **no se modifica durante el piloto** y que su integración es decisión **post-GO** — M5 no puede firmarse "para ya" sin chocar con eso.
> Contadores: **ninguno.** Es de fuente de verdad, no de medición.
> La rama "listas separadas con cruce declarado" es compatible con ADR-68(a) hoy; la rama "fuente única" queda gateada por el GO del piloto. El ADR debe decir eso en vez de dejar M5 abierta sin fecha.

**Firma de mesa (M5):** `[FIRMA M5 — VACÍA]`

---

### M6 · ¿Los tres dictámenes compass entran al repo (hoy son espejo sin sello) antes de sellar cualquier ADR que los cite?

> Toca: `forense/` — los tres compass, más RT-B y RT-D por la cadena A.3 de CAREO. **Estado hoy: los cinco siguen fuera del árbol** (`find . -iname "*compass*"` → `0`), tercera sesión consecutiva en que no llegan.
> Contadores: **ninguno.** Es de procedencia.
> **M6 es la única M que bloquea el sello por sí sola**, y su respuesta ya está escrita en canon: ADR-68(e) dispone *"ningún menú de «modelos elegibles» se sella sin ellos a la vista"*. **Si M6 no se resuelve, MOTOR-2 no se firma.**

**Firma de mesa (M6):** `[FIRMA M6 — VACÍA]`

---

## (7) · E5 — declara y notifica, NO cierra la Entrada 5

Texto fijado por `forense/encargos/2026-08-13-MOTOR-COND-v2-encargos-finales.md` §6 (acuerdo E5), reproducido — no es ranura de firma:

Este ADR **declara** que ADR-50/51 quedan reescritos por él, junto con el veredicto derivado sobre ADR-57(c). Este ADR **no cierra** la Entrada 5. Obliga el **AVISO del número** al carril E5 — con la instrucción **"archívese E5 por A.3 antes de correr"**, porque hoy `grep -rln "Entrada 5" forense/encargos/` no encuentra el encargo de E5 archivado (solo menciones de terceros: `forense/encargos/2026-08-14-MOTOR-1-consolidado.md` inciso 2). Queda escrito que E5, al correr, citará este ADR en su universo.

## (8) · Glosario celda-D/x/B — opcional-nombrado

Texto fijado por el mismo §6, reproducido — no es ranura de firma:

El glosario celda-D/x/B sigue **sin hacerse** (verificado: cero hits — pendiente de ADR-68(g)). Este ADR **lo anexa, o lo re-nombra con dueño** — pero no lo deja huérfano otra vez. La opción concreta (anexar aquí vs. abrir acto propio con dueño y fecha) es la única decisión de mesa dentro de este inciso; no lleva ranura de firma verbatim porque el §6 no la pide como tal — se resuelve en la redacción final del ADR, no aquí.

---

## Cierre — qué falta para que esto deje de ser esqueleto

1. Las seis ranuras de firma de arriba, llenas, verbatim, entre comillas.
2. M6 resuelta afirmativamente en el terreno (compass ×3 + RT-B/RT-D en el árbol) — sin eso, firmar las otras cinco no basta: *"si M6 no se resuelve, MOTOR-2 no se firma"*.
3. El número del ADR, derivado con T15 contra el `main` del momento de sellar — nunca heredado de este archivo.

Este archivo no edita `canon/`, `milpa/`, `data/` ni `tests/`. Perímetro de escritura de este acto: un archivo nuevo en `forense/` — éste.
