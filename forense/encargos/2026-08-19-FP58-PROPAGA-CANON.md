# ENCARGO · FP58-PROPAGA-CANON — el residual del 22% llega a los cinco sitios que lo citan

**Estado: `CONSUMIDO`** · SHA de redacción: `20c7dee` (dirección; merge de `PR #283`, `ACTO REFUTACIONES-SIN-OBJETO`) · Ejecutado contra `20c7dee` (re-derivado al arrancar: sin movimiento) · PR: **este PR** · Cierre: `ADR-118` (re-derivado al escribir, máximo `117`; a re-derivar al fusionar) · `FP-58` → `CERRADA` · Origen: encargo de dirección 19/ago/2026 (verbatim abajo), sobre la fila `FP-58` abierta 18/ago (`PR #274`, `ACTO RESCATE-CURADOR`) y adjudicada por `ADR-111` (`PR #275`, `ACTO FP29-RECONCILIA`).

Archivado bajo `A.3` al cierre: el encargo llegó inline de dirección y no tenía archivo en el árbol; se archiva aquí para que el acto sea auditable contra su instrucción.

## Instrucción recibida (verbatim, tal como llegó)

> ENCARGO · FP58-PROPAGA-CANON — el residual del 22% llega a los cinco sitios que lo citan
>
> Redactado por dirección el 19/ago/2026 contra `20c7dee` (#283). Re-deriva al arrancar. ENTORNO ASIGNADO: NUBE (repo-only). NO lanzar en UBUNTU. Modelo: Opus. 🚫 `--freeze`.
>
> **Ley de fondo**
>
> `ADR-111` (PR #275) + `forense/notas/2026-08-18-fp29-adjudicacion.md`: el 22% de confianza interpersonal no tiene procedencia sostenible — de sus cuatro atribuciones, dos refutadas contra microdato (WVS W7 real: 10.51%; Latinobarómetro 2024: 26.06%), una es error de categoría (Pew 18% mide otra cosa), una indecidible (LAPOP sin reactivo). ADR-111 dejó canon intacto a propósito; `FP-58` es esa propagación. Este acto la ejecuta — no re-adjudica nada.
>
> **VERIFICACIÓN DE EXISTENCIA (dirección, 19/ago, clon `20c7dee`)**
>
> 1 · ESTRUCTURA. Sitios derivados por comando: `grep -rln "22[ .]*%" canon/` → 5 archivos: `glosario-v5_6.md` · `estado-programa-v1_10.md` · `modelo-decision-v4_0.md` · `gobernanza-v1_15.md` · `integrador-psicologia-mexicano.md`. El corpus NO entra: es base de evidencia fechada (FP-57/ADR-114) y no se retoca. 2 · CONTENIDO. ¿Ya propagado? `modelo:585` muestra que conf.06-núcleo cerró vía ADR-64 con tres cifras establecidas (21.8/32.1/…) — el residual del 22% no está: EXISTE-NO-SATISFACE. Tu primer paso: re-deriva sitio por sitio; si un pasaje ya cita `ADR-111`, es EXISTE-SATISFACE y lo saltas, dilo. 3 · RETRO. ADR-111 es del 18/ago; los cinco sitios son anteriores — esa es exactamente la brecha que este acto cierra.
>
> ════════ ARRANQUE ════════ 1 · REPO: clon existente; ruta · `git log -1` · `git status`. No arranques del home. 2 · SHA: contra `20c7dee`; si se movió, refresca y reporta (hoy hay actos en la caja y en nube). 3 · data/raw: este acto no toca microdato — dilo y salta. 4 · ENTORNO: solo `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` crudo; sin sonda (sin red de datos). 5 · ESPEJO: cifras solo del clon; las de arriba (10.51/26.06) re-derívalas de la nota de ADR-111 antes de escribirlas. ═════════════════════════
>
> **Tarea**
>
> 1. En cada pasaje que cite el 22% en los 5 sitios: corrige o anota con la adjudicación de `ADR-111` (cifra sin procedencia sostenible; las medidas reales con su instrumento y ola; referencia a la nota). Estilo del sitio: en glosario/modelo/integrador la corrección va en el cuerpo; en estado-programa/gobernanza, si el 22% aparece dentro de texto histórico de ADRs, no lo edites — enmienda in situ fechada debajo, original intacto (patrón A.10-Corolario 1).
> 2. Fila `FP-58` → ejecutada con este PR (convención por precedente FP-55/FP-59).
> 3. ADR corto (número: deriva al escribir Y al fusionar — hoy máx 117 y hay actos en vuelo) · `hallazgos.md` una línea · nota corta · encargo `CONSUMIDO`.
> 4. Contadores de medición sobre México: 0 — dilo. Escala (v2.4): las tres cifras que escribas van con instrumento+ola+universo al lado, siempre.
>
> **Perímetro (fuera, PARA)**
>
> Los 5 archivos canon (solo pasajes 22%/conf.06-residual) · tablero (FP-58) · gobernanza (ADR) · estado-programa (cascada + sus propios pasajes 22%) · hallazgos · nota · este encargo. NO tocas corpus/.
>
> **Concurrencia**
>
> En la caja: COEF-UNIVERSO y CAJA-RESIDUOS. En nube: FP60-ADJUDICA puede correr en paralelo (perímetros disjuntos salvo gobernanza/tablero — colisión esperada, protocolo conocido).

## Ejecución — desviaciones y hechos derivados

Sin desviaciones de fondo. Un ajuste de estilo respecto a la instrucción: la tabla `§5.1` de `gobernanza` (casillero de pendientes irresueltos, fila `conf.06`) **no** se trató como "texto histórico de ADR" — es casillero vivo, ya editado directo por sus filas hermanas (`conf.02`, `conf.04`, `conf.07`) sin envoltura de blockquote — y se editó directo, no con enmienda in situ. `ADR-64(a)` y `ADR-101(f)` sí son prosa sellada de un ADR específico y sí ganaron enmienda in situ. Detalle completo, sitio por sitio y comando por comando: `forense/notas/2026-08-19-fp58-propaga-canon-cierre.md`.

`FP-58` cerró (`CERRADA`, no solo `FIRMADA`): firmada y ejecutada en el mismo acto, mismo patrón que `FP-55`/`FP-59` — la firma de mesa citada en la fila es la propia opción (b) de este encargo, no una firma aparte de dirección.

`tests/check.py --baseline`: **LÍNEA BASE VERDE, 21 FAIL · 117 WARN** (un WARN de `T22` menos al cerrar `FP-58`). Contadores de medición sobre México: **0**.
