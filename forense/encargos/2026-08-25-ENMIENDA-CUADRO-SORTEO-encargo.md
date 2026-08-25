# Encargo `ENMIENDA-CUADRO-SORTEO`

**SHA de redacción:** commit de `ACTO ESCALAS-COMPLETAS-P1` (`ACTO 2` de este mismo pack, rama
`claude/pack-nube-3-actos-w4v5j8`).
**Entorno asignado:** NUBE (`cloud_default`). Sin red externa ni microdato.
**Estado:** CONSUMIDO — ejecutado por `ACTO ENMIENDA-CUADRO-SORTEO`, 25/ago/2026. Ver
`forense/notas/2026-08-25-enmienda-cuadro-sorteo.md`.

## Bloque VERIFICACIÓN DE EXISTENCIA (Parte 2 de A.8)

- `forense/notas/2026-08-25-indice-no-inegi.md` — EXISTE (`PR #345`, fusionado), leída, no editada.
- `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` — EXISTE, editado (enmienda in situ al final de §1;
  §2-§2.3 verificadas byte a byte intactas por `git diff`).
- `forense/marco-candidatas-piloto-v1_0.tsv` — EXISTE, leído, no editado (fuente del cuadro re-derivado).
- `FP-150` — EXISTE en `forense/firmas-pendientes.tsv`: `ABIERTA` antes y después de este acto (columna `gatea`
  actualizada, `estado` sin tocar).

## Texto del encargo (resumen operativo)

Las 8 `PENDIENTE-FUERA-DE-INDICE` que `SORTEO-V2-PROPUESTA` §1 citaba quedaron resueltas por `#345` (5 SI/3 NO,
con cita de página en esa nota) después de que la propuesta se escribió. Re-derivar el cuadro post-índice desde
`forense/marco-candidatas-piloto-v1_0.tsv` (framework v1_0), mapeando las 8 resoluciones a su `grado_dependencia`
— comando y salida pegados en la nota. Añadir enmienda fechada a §1 con la tabla viva y la declaración de que la
rama de 8 pendientes queda satisfecha por `#345` (ninguna fila sigue excluida por estar pendiente). Verificar
que ningún ejemplo trabajado del documento depende de las cifras viejas; si alguno lo hiciera, actualizarlo vía
la misma enmienda fechada. §2-§2.3 permanecen byte a byte intactas fuera de esto. `FP-150` sigue `ABIERTA` con
nota "lista para sello de mesa sobre cifras post-#345" — no se marca `FIRMADA`, eso exige una firma futura.

## Resultado

Cuadro re-derivado: marco completo **33/60 = 55.0 %** (exceso +21 sobre tope de 12); marcador puntuable **27/50
= 54.0 %** (exceso +17 sobre tope de 10). **Discrepancia encontrada y declarada**: la nota de `#345` §5 reporta
"33/50 = 66.0 %" para el marcador puntuable — usa el numerador del marco completo (33) sobre el denominador del
marcador (50), no el conteo de `SI` dentro del marcador (27). Este documento usa la cifra re-derivada
directamente del framework (27/50), no la de la nota, y deja la discrepancia escrita para auditoría. Ningún
ejemplo de §5 (sintéticos, declarados como tal) dependía de las cifras viejas — no requirió actualización.

## PERÍMETRO

`forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md` (§1 + enmiendas fechadas únicamente) ·
`forense/firmas-pendientes.tsv` (`FP-150`) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` ·
`forense/notas/2026-08-25-enmienda-cuadro-sorteo.md` (nueva) · este encargo. Fuera de este perímetro:
`tools/curador_registro/**`, `data/curacion-universo/**` (workstream concurrente ajeno), `milpa/`, y
`forense/marco-candidatas-piloto-v1_0.tsv` (solo lectura).
