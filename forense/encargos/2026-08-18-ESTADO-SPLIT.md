# ENCARGO · ESTADO-SPLIT — partir `estado-programa:101` en una cláusula por línea

**SHA de redacción:** `93a4dd9` (`origin/main`, tras `ADR-100`/`ADR-101`, ACTO MESA-18AGO, 18/ago/2026)
**Entorno asignado:** **NUBE** (`cloud_default`, repo-only). Edición mecánica de un archivo de canon, sin microdato.
**Estado:** VIVO — **gateado a que `GATE-DURABLE-V7` e `INTEGRATE-T23` fusionen** (ambos ya fusionados: `PR #255`, `PR #256`, contenidos en `93a4dd9`), porque parte el archivo que los tres actos concurrentes de hoy tocan. Escrito, no lanzado, por ese mismo motivo — un split en vivo mientras cualquier otro acto edita `estado-programa:101` sería el propio riesgo que `FP-48` nombra.
**Origen:** `FP-48`, decisión de mesa D-7 (`ADR-101`, verbatim: *"Partirlo completamente."*) — responde directamente la pregunta que `FP-48` planteaba (partir en una cláusula por línea / `merge=union` / revisión manual declarada): mesa elige **partirla**.

## Verificación de existencia (A.8), contestada por quien escribe

```
estado-programa:101, tamaño hoy:   ~26 800+ caracteres, un único párrafo, historia completa de
                                    numeración de ADR desde el 29/jul (32 -> 101)              MEDIDO
.gitattributes, precedente:        forense/hallazgos.md y forense/bitacora.md ya declaran
                                    merge=union -- estado-programa:101 no lo declara            VERIFICADO
riesgo medido, 4 actos:            ADR-92/93/94(via CIERRA-17AGO)/98 midieron, cada uno, que el
                                    automerge resuelve esa línea quedándose con un lado entero
                                    -- las dos veces de BARRIDO-2 salió bien por suerte (main
                                    iba atrás), no por diseño (hallazgos.md, 17/ago)            VERIFICADO
perímetro de este mismo acto:      "solo :27/:101 cascada" -- este encargo excede
                                    deliberadamente ese perímetro (restructura la línea
                                    entera), por eso no se ejecuta aquí                          DECLARADO
```

## Perímetro

ESCRIBE: `canon/estado-programa-v1_10.md` — **solo** la línea `:101` (el párrafo de "L0 · Gobierno"), convertida de un párrafo a una lista con **una cláusula (un ADR) por línea**, contenido idéntico, sin resumir ni perder ninguna cláusula · nota del acto con el diff completo, verificado cláusula por cláusula contra el original (mismo método que `ADR-98` ya usó para confirmar que ningún merge había perdido contenido). NO ESCRIBE: ningún otro archivo — este es un acto de forma, no de contenido.

## Tarea

1. Leer `estado-programa:101` completo, extraer las 101 cláusulas (una por ADR, desde "a 32..." hasta "a 101...").
2. Reescribir como lista Markdown, un ítem por ADR, **contenido verbatim** de cada cláusula (fecha, ACTO, descripción, cascada de contadores) — cero resumen, cero pérdida.
3. Verificar por diff automatizado (no lectura humana) que el texto plano concatenado de la lista nueva es idéntico, carácter por carácter salvo el formato de lista, al párrafo original.
4. Decidir y declarar si además se añade `merge=union` en `.gitattributes` para esa sección — la lista partida ya hace viable el merge por unión de líneas independientes; `merge=union` es una segunda capa, no un sustituto. Si se añade, verificar contra el precedente de `forense/hallazgos.md` (requiere salto de línea final siempre, y el botón "Merge pull request" de GitHub no honra el driver del lado servidor — solo el merge local lo garantiza, per `forense/notas/2026-08-12-union-vs-boton-github.md`).
5. Ejecutar el split **solo** cuando ningún otro acto tenga `estado-programa` en su perímetro activo — verificar `git branch -r` y los encargos `VIVO` de otros carriles antes de tocar el archivo.

## Cierre

`estado-programa:101` partida en lista, contenido verificado idéntico por diff · `tests/check.py --baseline` VERDE (T15 sigue derivando el conteo de ADR desde la lista nueva, no desde el párrafo) · `firmas-pendientes.tsv`: `FP-48` → `FIRMADA`, `ejecutada_en` este PR · línea en `hallazgos.md` · encargo `CONSUMIDO`.
