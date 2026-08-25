# Encargo `ESCALAS-COMPLETAS-P1`

**SHA de redacción:** commit de `ACTO SELLA-G` (`ACTO 1` de este mismo pack, rama
`claude/pack-nube-3-actos-w4v5j8`).
**Entorno asignado:** NUBE (`cloud_default`). Sin red externa ni microdato.
**Estado:** CONSUMIDO — ejecutado por `ACTO ESCALAS-COMPLETAS-P1`, 25/ago/2026. Ver
`forense/notas/2026-08-25-escalas-p1.md`.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- `FP-149` — EXISTE en `forense/firmas-pendientes.tsv`: `FIRMADA` desde `ACTO SELLA-G` (`ADR-173`), opción (d),
  Paso 1 es exactamente lo que este encargo ejecuta.
- `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle` — EXISTE, 15 filas, editado (campo nuevo
  `escala_derivada:` en las 15, único cambio verificado por `git diff --stat`).
- `milpa/procedencia.yaml:condicionales_confianza_institucional`, `condicionales_escalares`,
  `condicionales_escalares_confianza_generica`, `condicionales_escalares_exposicion_violencia` — EXISTEN,
  leídas, no editadas (perímetro de solo lectura para este acto).
- `canon/modelo-decision-v4_0.md` §2 (líneas 422-460) — EXISTE, leída completa, no editada.
- `milpa/src/matriz.py`, `milpa/src/procedencia.py`, `tests/cal_enoe_fasea.py`, `tests/test_motor_procedencia.py`,
  `tools/censo_estimabilidad.py` — los cinco archivos `.py` del árbol que citan `asignados_coeficiente` o
  `rutas_estimabilidad_coeficiente` (`grep -rln`, verificado, cinco resultados, ninguno más); ninguno multiplica
  por `B` — `matriz.py:cargar_B` solo construye el objeto `Matriz`, sin aritmética que lo consuma en el árbol.

## Texto del encargo (resumen operativo)

Ejecutar el Paso 1 que `FP-149` firmó: para las 15 entradas `ASIGNADO`, buscar (no en la fuente de asignación,
ya agotada por `FP-141`) los dos extremos de cada relación — la escala declarada de la θ que el coeficiente
multiplica (`milpa/procedencia.yaml`, secciones `condicionales_escalares*`) y la escala declarada de la salida
del generador (`canon/modelo-decision-v4_0.md` §2). Blindaje: solo fuentes fechadas el 24/ago/2026 o antes; el β
medido de `CAL-G3` y su discrepancia no entran a la derivación. Por entrada: `DERIVADA(forma, dos citas)` si
ambos extremos están sellados, `SUBDETERMINADA(extremo faltante, por qué)` si no. Campo `escala_derivada:` nuevo
en las 15 filas, citas solo donde `DERIVADA`. Si `G3.horizonte_temporal` termina `DERIVADA`, releer `CAL-G3` bajo
esa escala sin re-adjudicar; si `SUBDETERMINADA`, decirlo y parar ahí. Actualizar la fila `ESCALAS-COMPLETAS`
del tablero con la lista de subdeterminadas.

## Resultado

**0 de 15 `DERIVADA`. 15 de 15 `SUBDETERMINADA`** — el extremo del generador (§2 de `modelo-decision-v4_0.md`)
no está declarado para ninguno de los siete generadores, así que ninguna de las 15 puede tener forma forzada
aunque 7 de ellas sí tengan su extremo θ declarado. `G3.horizonte_temporal` es una de las 8 sin ningún extremo
declarado — no se relee `CAL-G3`, por regla de la propia firma. Detalle completo, con las citas de cada
extremo: `forense/notas/2026-08-25-escalas-p1.md`.

## PERÍMETRO

`milpa/procedencia.yaml` (solo el campo `escala_derivada:` en las 15 filas de `rutas_estimabilidad_coeficiente`)
· `forense/firmas-pendientes.tsv` (`FP-149`) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` ·
`forense/notas/2026-08-25-escalas-p1.md` (nueva) · este encargo. Fuera de este perímetro:
`tools/curador_registro/**`, `data/curacion-universo/**` (workstream concurrente ajeno), y cualquier otro campo
de `milpa/procedencia.yaml` fuera de las 15 filas ya declaradas.
