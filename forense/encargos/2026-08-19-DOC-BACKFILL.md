# ENCARGO · ACTO DOC-BACKFILL — U3, las cuatro preguntas del transfer sobre las fuentes que sostienen celdas vivas

SHA de redacción: derivar al lanzar (escrito el 18/ago/2026 por `ACTO MESA-19AGO`). Entorno asignado: derivar al lanzar. **GATEADO a «`B2-SEMANTICO` fusionado»** — no se lanza antes. Estado: **VIVO**. Origen: firma de mesa D-6 de `MESA-19AGO`, `ADR-106(f)`, fila `FP-33`.

## 1 · Lo que la mesa firmó (verbatim)

D-6: **`Escribir gateado`** — *"Se escribe `DOC-BACKFILL` ahora, con su A.8 citando las cuatro preguntas por ruta y línea (la fila FP-33 del tablero), gateado a B2-SEMÁNTICO fusionado y con la población re-derivable, no copiada. No se lanza aquí."*

## 2 · A.8 — las cuatro preguntas, citadas por ruta (texto pegado inline en su día, no re-pedido aquí)

Fuente: fila **`FP-33`** de `forense/firmas-pendientes.tsv`, columna `qué_se_firma` — texto pegado inline por `ACTO REGISTRA-17AGO-II` (17/ago/2026), **procedencia tipo (3)**: recuperado de la conversación de proyecto *"003 - Maestra 25 (Fable)"* del 12/ago/2026, **no del repo**. Selle original: `canon/gobernanza-v1_15.md`, `ADR-70`, que sella `PROPUESTA-remediacion-brecha-documental.md:16` (SS2).

1. **Ficha RNM abierta** — url + fecha + qué campos `NO_DETERMINADO`/inferidos quedaron resueltos, con atención a `periodo_levantamiento`, `periodo_referencia_por_variable` y los nombres exactos de ponderador/estrato/conglomerado.
2. **Indicadores de calidad** — existen o no en su catálogo, con URL; si aparecen nuevos, se suman a la cola de `EV-1`.
3. **Diseño muestral oficial vs. inferido**, por producción que lo use.
4. **`NO-ENCONTRADO` en su cadena** cuyo universo no incluyera el nivel documental — *"solo si gatea algo vivo se reabre; si no, una línea y se queda"*.

## 3 · Población — cerrada por criterio, no por lista

Las fuentes que sostienen (a) las producciones vigentes, (b) las celdas-D registradas, (c) las fichas de Hito D con acto en cola.

⚠️ **Aviso que la fila lleva escrito y este encargo hereda:** la enumeración original del 12/ago decía *"las 11 producciones… ocho fichas, no 958"* — **foto vencida**. Re-derivada contra `1282ae3`: **12** producciones (`data/curacion-registro/produccion-modelo.tsv`, 12 `PROD-` distintos) y **3** celdas-D (`data/curacion-registro/celdas-d/`, 3 archivos). **La población se re-deriva por comando al ejecutar; copiar las ocho de la foto original sería heredarla vencida** — y las cifras de este párrafo son ellas mismas una foto del 17/ago, no un dato de hoy.

## 4 · Por qué estaba perdido

Verificado por comando al firmar: `grep -rln DOC-BACKFILL forense/ canon/` daba **CERO** en todo el árbol. El acto se nombró en la propuesta sellada por `ADR-70` y nunca volvió a aparecer. Este encargo es el primer archivo del árbol que lo nombra.

## 5 · La decisión que el gate deja viva

La fila `FP-33` ofrecía dos desenlaces: lanzarlo, o **declararlo absorbido por los productos de `BARRIDO-2` y cerrarlo sin correr**. La firma D-6 decide **escribirlo gateado**; si al abrirse el gate los productos de `BARRIDO-2` ya cubren el backfill, este acto se cierra con acta declarándolo absorbido — y ese cierre también es su ejecución, no su omisión.

## 6 · Lo que NO hace

No se lanza antes del gate · no re-pide el texto de las cuatro preguntas (ya está inline, se cita) · no copia la población de ninguna foto.
