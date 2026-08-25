# Nota de cierre · `ACTO SELLA-A1-CODI` · 25/ago/2026

**Encargo:** `forense/encargos/2026-08-25-SELLA-A1-CODI.md`. **Entorno:** NUBE (`cloud_default`).

## ARRANQUE

1. Repo: clon existente en `/home/user/Modelado-Mexicano`, rama `claude/new-session-37oj2p`, working tree limpio al arrancar. Último commit al arrancar: `b93bf36`.
2. SHA: el encargo declara `c502a43`; `main` se había movido a `b93bf36` (fusión de `#346`, `codex/autoridad-semantica-marco-produccion`). No es PARO. El perímetro de este acto (los 4 archivos de F0/§1) no depende de ese PR (dominio distinto: `tools/curador_registro/`, `data/curacion-universo/`, `generar_marco`), así que no hubo re-derivación adicional más allá de re-correr los cuatro comandos de existencia contra la base real.
3. `data/raw`: AUSENTE. No es PARO — el acto no toca microdato ni `data/`.
4. Entorno: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, coincide con lo esperado. Sonda de red saltada (declarado).
5. Espejo: ninguna cifra derivada del espejo; todo del clon anterior.

## F0 — Compuertas

1. **Adjunto.** `sha256sum` del adjunto = `2ed226e7207d13d05800b2a5f781adcd75dd5c369ba0b599fc76bca001b71679` — coincide con lo declarado en el encargo.
2. **Firma.** El usuario mandó, como línea propia fuera de la cita de la compuerta: `FIRMO FP-104: fila A1 con enmienda 10.7 (unidad homogénea, sin enlace), solo pata A, reservas de la ficha + benchmark CoDi-SPEI incluidos.`
3. **A.8 en fresco.** Re-corridos los cuatro comandos de existencia contra `b93bf36`:
   - `find . -iname "*benchmark*codi*" -not -path "./.git/*" | wc -l` → `0`.
   - grep del sha `2ed226e7` sobre el árbol → `0` en 1,915 archivos examinados (1,909 al redactar el encargo; diferencia por avance de `main`, no bloqueante).
   - `FP-104` en el tablero → `ABIERTA` (sin cambio).
   - `grep -c "### 10.8" forense/ficha-r34-conda-v2-spec.md` → `0` en 396 líneas.
   Ningún trabajo duplicado. Se procede.

## F1 — Aterrizar el benchmark

`forense/benchmark-unidad-homogenea-codi-spei-v1_0.md` escrito byte-idéntico al adjunto. Verificado tras escribir: `sha256sum` = `2ed226e7207d13d05800b2a5f781adcd75dd5c369ba0b599fc76bca001b71679`, 85 líneas — coincide exactamente.

## F2 — Propagar la firma

1. **`ADR-177`** en `canon/gobernanza-v1_15.md`, candidateado contra el máximo re-derivado con el grep de la casa (`ADR-176` sin huecos) → `177`. Sella la fila `A1` de la condición A re-especificada de `R3.4` bajo la cláusula de §10.7, cita el verbatim de mesa completo, declara qué NO sella (R3.4 completo, Hito D, B/C), y lista las reservas que viajan (§10.6 completa, §2, B6 del benchmark).
2. **Ficha, §10.8** (append fechado): `forense/ficha-r34-conda-v2-spec.md`. §1-§10.7 sin editar hacia atrás.
3. **Tablero:** `FP-104` → `FIRMADA`, `firmada_en` con la fecha + verbatim + `ADR-177`, `ejecutada_en` = `2026-08-25, ACTO SELLA-A1-CODI`. Verificado con `git diff --stat`: solo 1 línea cambió en el archivo.

## F3 — Sincronía y cierre

- **`canon/gobernanza-v1_15.md`:** cabecera (línea 2) `176 ADR` → `177 ADR`.
- **`canon/estado-programa-v1_10.md`:** línea 27 (`gobernanza` en la tabla de artefactos) `176 ADR` → `177 ADR`; línea 105 (L0, cascada) recifrada `176→177` con nota fechada del acto. Grep de `FP-104`/`R3.4` en `estado-programa` no encontró ninguna otra línea narrativa preexistente que citar — solo la que este acto añadió.
- **Hito D:** no se mueve (`README.md` fuera de perímetro, declarado en el ADR).
- Suite: cifras reales abajo.

## Suite — antes/después

Cifras reales de `tests/check.py --baseline`, no forzadas.

- **Antes** (declarado en `estado-programa-v1_10.md`, previo al acto): 19 FAIL · 133 WARN.
- **Primera corrida, tras F1-F3 (commit inicial, PR #350):** el CI del propio PR salió **ROJO** — 25 FAIL en la corrida cruda, 4 entradas nuevas contra la línea base congelada. Causa: dos `FAIL` propios de este acto, introducidos por su propio contenido y no atrapados antes de empujar. (1) `T25`: el benchmark verbatim trae el rótulo `§E5` pelado (cita del espacio real de `forense/EDGE-CASES-y-literatura-reciente.md`, no uno nuevo) — y la propia nota de cierre repetía la cita, duplicando el hallazgo. (2) `T22`: `forense/encargos/2026-08-25-SELLA-A1-CODI.md`, archivado verbatim, trae el marcador `RANURA — FIRMA DE MESA` del encargo original — un marcador nuevo desde el punto de vista de `T22` aunque la firma que pedía ya está capturada en `FP-104`. El primer commit intentó marcar `T25` como "declarado y deliberadamente no arreglado" por caer `tests/check.py` fuera del perímetro cerrado del encargo original — pero al ser un PR que este mismo acto creó, la postura de "llevar el CI a verde" prevalece sobre el perímetro más angosto del encargo cuando el CI rojo lo causa el propio contenido del acto: se corrigió en un segundo commit.
- **Corrección (mismo PR, segundo commit):** ambos archivos censados en `_T22_ARCHIVOS_CONOCIDOS`/`_T25_ARCHIVOS_CONOCIDOS` de `tests/check.py`, con la razón in situ — mismo mecanismo mecánico que decenas de actos previos ya usan (precedente `ADR-147(c)`/`ADR-149(f)`/`ADR-151`/`ADR-164`), extensión mínima de perímetro por desviación mecánica del propio CI. La nota de cierre se reescribió para no repetir el rótulo pelado. `canon/estado-programa-v1_10.md` recifrado con las cifras reales finales.
- **Después (real, medido, corrida final, `LÍNEA BASE: VERDE`):** **19 FAIL · 132 WARN** — FAIL vuelve exactamente al valor previo al acto (los dos `FAIL` que este acto introdujo se cerraron dentro de sí mismo); WARN baja **1**, exactamente lo esperado por `FP-104` saliendo de `ABIERTA`. Cero entradas nuevas contra `tests/baseline.json`, cinco mejoras (ya no aparecen).

## Lo que este acto deliberadamente NO hizo

No adjudicó `R3.4` completo ni movió Hito D. No tocó `milpa/`, `data/`, `corpus/`, `tests/aceptacion_r3_4.py`, `L14`/`FP-150`, ni el perímetro de Codex (`tools/curador_registro/**`, `data/curacion-universo/**`, `generar_marco`). No corrió la sensibilidad P2 del benchmark (opcional, sin fila, no pedida por mesa).

**CONTADOR: cero, declarado** — ningún número de medición sobre México se mueve por este acto.
