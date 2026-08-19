# ENCARGO · ACTO E5 — cerrar la Entrada 5 de `registro-recalculo` (`ADR-50` / `ADR-51` / `ADR-57(c)`)

**SHA de redacción:** `f3d3f95` (`origin/main`, tras `ADR-104` / `ACTO COND-ATRIB` `PR #263`, 18/ago/2026)
**Entorno asignado:** **NUBE** (`cloud_default`, repo-only). No toca microdato. NO va a Ubuntu.
**Estado:** CONSUMIDO — ejecutado por `ACTO LANE-A-E0-E5`, este PR (mismo acto que lo archiva; ver §"Por qué este encargo se archiva y se ejecuta en el mismo acto").
**Origen:** inciso **(7)** de `ADR-100`, verbatim: *"Obliga el AVISO del número al carril E5, con la instrucción «archívese E5 por A.3 antes de correr»"*. Cumplimiento de A.3 (`instrucciones-proyecto` Bloque D-bis): la Entrada 5 llevaba desde el 13/ago/2026 sin encargo propio archivado — hallazgo levantado y verificado por `ACTO MOTOR-1` (`forense/notas/2026-08-14-motor-1.md` §4.3) y re-verificado por `ACTO SELLO-FICHA-G3` (18/ago).

## Por qué este encargo se archiva y se ejecuta en el mismo acto

A.3 exige que el encargo se commitee **antes o junto con** su lanzamiento — no antes de su ejecución por un acto distinto. `ADR-100(7)` no manda un acto separado: manda *"archívese E5 por A.3 antes de correr"*, y `LANE-A-E0-E5` (Tarea 2) asigna esa archivación al mismo ejecutor que corre la Entrada 5 (Tarea 3). Se cumple al pie: este archivo entra al árbol en un commit **anterior** al que escribe la fila de la Entrada 5, de modo que el orden "archivar → correr" queda en la historia de git y es auditable por comando, no por declaración.

## Verificación de existencia (A.8), contestada por quien escribe

```
forense/registro-recalculo-v1_0.md, tabla §1, fila 5:   EXISTE, veredicto `ABIERTA`  (:41)
forense/notas/2026-08-14-motor-1.md §4:                 EXISTE-SATISFACE (universo, veredicto, cifra)
canon/gobernanza-v1_15.md, ADR-100:                     EXISTE (:1811) -- el número que faltaba
canon/gobernanza-v1_15.md, ADR-57 (a)-(d):              EXISTE -- anclas re-derivadas, no heredadas
forense/firmas-pendientes.tsv FP-15:                    EXISTE, línea 16, `estado=ABIERTA`
encargo propio de E5 archivado:                         NO EXISTÍA -- este archivo lo constituye
```

## Perímetro

ESCRIBE: `forense/registro-recalculo-v1_0.md` (la fila 5 de la tabla §1, **una fila**, append sobre su celda de veredicto) · `forense/firmas-pendientes.tsv` (`FP-15`, columnas `estado` / `ejecutada_en` / `encargo`) · `forense/encargos/` (este archivo) · nota del acto · `forense/hallazgos.md` (una línea).
NO ESCRIBE: `canon/**` (se cita `ADR-100` y `ADR-57(c)` por número; no se editan) · `milpa/procedencia.yaml` · `forense/registro-llaves-identificacion-v1_0.md` (la cifra `1 de 2` **se cita, no se mueve**) · `data/**` · `tools/**`.

## Tarea

1. **Formato de entrada.** Derivarlo del propio archivo: `registro-recalculo` **no** usa encabezados `^## Entrada`; sus entradas son **filas de la tabla de §1** (`| # | entrada | clase | por qué va aquí | gate | estado |`). La entrada se cierra escribiendo en la columna `estado` el veredicto, el acto/PR que lo cerró y **el universo declarado en la misma línea** (regla propia del archivo, cierre de §1).
2. **Universo a citar** (derivado por `ACTO MOTOR-1` §4.1, re-verificado contra el árbol antes de escribir, no heredado):
   - Bloque AJUSTE de `ADR-50`/`ADR-51`: el desglose 39 probabilidades / 15 coeficientes con la corrección de `ADR-51` (**libres del ajuste reales = 7 + 15 = 22**) y los incisos (3) *"los momentos a reproducir SE DECLARAN ANTES DE AJUSTAR"*, (4) *"motor como contexto"* CONSIDERADA Y NO ADOPTADA, (5) riesgo de identificabilidad, condición pendiente.
   - `ADR-57` completo, incisos (a)-(d), con sus anclas **re-derivadas hoy** — el `619-627` que los encargos viejos citan ya derivó.
   - **`ADR-100`** — el número que la fila esperaba desde el 13/ago; su inciso (7) declara expresamente que E5, al correr, lo citará en su universo.
3. **Veredicto sobre `ADR-57(c)`: `SIN CAMBIO`** — ya derivado y argumentado en cuatro pasos por `ACTO MOTOR-1` §4.2 (el ADR se acota en su título a *"la clase de afirmación, no el motor"*; las tres clases de llave son diseños de dato, no formas de cómputo; §1.4 de la propuesta es transcripción, no objeto nuevo; la propia propuesta lo concede en §4.3). Se transcribe con sus **dos asimetrías**, porque el `SIN CAMBIO` no es simétrico.
4. **La cifra que NO se copia.** `propuesta-motor-matriz-v0_1.md` §4.3 dice *"hoy hay cero"* llaves ejercidas: **vencida**. Hoy es **`1` de `2`**, con veredicto `EJERCIDA_INDECISA` (`ACTO ADJ-4`, `R5.1-D2`) y **`0` compuertas abiertas** — las tres cosas a la vez, o la cita es falsa en la letra o en el efecto. **Se cita; no se mueve el contador.**
5. **Cierre de `FP-15`** en `forense/firmas-pendientes.tsv` (línea 16, verificada por contenido, no por número): `estado` → cerrada, `ejecutada_en` = este PR, `encargo` = este archivo.

## Cierre

Entrada 5 cerrada con veredicto de los tres y universo declarado en la misma línea · `FP-15` cerrada · `tests/check.py --baseline` VERDE · línea en `hallazgos.md` · este encargo `CONSUMIDO`.

**Contadores de medición sobre México que este encargo mueve: cero.** `13 de 27`, `0 de 15`, `12 de 15`, `4 de 144` y `1 de 2` quedan exactamente donde están.
