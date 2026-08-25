# Encargo `ESCALA-ASIGNADOS`

**SHA de redacción:** `26ea239` (`origin/main`, merge de `PR #338`).
**Entorno asignado:** NUBE (`cloud_default`). Sin red externa ni microdato.
**Estado:** CONSUMIDO — ejecutado por `ACTO ESCALA-ASIGNADOS`, 25/ago/2026. Ver `forense/notas/nota-2026-08-25-escala-asignados.md`.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- `FP-141` — EXISTE en `forense/firmas-pendientes.tsv`: `FIRMADA`, `firmada_en` cita "2026-08-25, mesa, hoja de las diez letras, L1/FP-127 opción b". Es la única excepción viva declarada a la regla general de no tocar `milpa/` (verificado: el texto de `FP-141` autoriza explícitamente "declarar la escala de los 15 coeficientes ASIGNADOS de `milpa/procedencia.yaml`").
- `milpa/procedencia.yaml:rutas_estimabilidad_coeficiente.detalle` — EXISTE, 15 filas (una por coeficiente ASIGNADO de generador), editado (dos campos nuevos por fila: `escala_asignado`, `escala_fuente`). Ningún otro contenido de `milpa/` se tocó.
- `canon/modelo-decision-v4_0.md:454-460` — EXISTE (tabla de coeficientes G1-G6), citado como fuente de escala.
- `CAL-G3` — EXISTE: `forense/registro-llaves-identificacion-v1_0.md` §11 y `canon/estado-programa-v1_10.md` (línea de llaves de identificación) documentan el β=+0.0146 medido contra el −0.60 ASIGNADO de `G3.horizonte_temporal`.
- `forense/firmas-pendientes.tsv` — EXISTE, editado (`FP-141` recibe `ejecutada_en`; fila nueva `FP-149`, `A.12`).

## Texto del encargo (verbatim, resumen operativo)

Ejecutar `FP-141` (`L1-b`): para las 15 entradas ASIGNADO de `milpa/procedencia.yaml`, rastrear su fuente de asignación y determinar la escala en que fue pensado el coeficiente. Si la fuente no declara ni permite derivar la escala, marcar `ESCALA_NO_DERIVABLE` con la cita de la fuente consultada — sin inventar escala. Añadir campos `escala_asignado:`/`escala_fuente:` a cada entrada. Escribir un párrafo (mesa/tablero, sin re-adjudicar) sobre la discrepancia de `−0.60` de `CAL-G3` bajo la escala declarada. Marcar `FP-141` ejecutada. Si alguna entrada ESCALA_NO_DERIVABLE bloquea una comparación futura, fila nueva en `A.12`.
