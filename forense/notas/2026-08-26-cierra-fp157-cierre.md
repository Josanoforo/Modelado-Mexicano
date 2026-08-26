# Nota de cierre · `ACTO CIERRA-FP157` (`E1`) — 26/ago/2026

## Arranque (A.13)

1. **REPO.** `/home/user/Modelado-Mexicano` (clon existente, no se clonó ninguno nuevo). `git log -1 --format="%h %s"` → `186f090 Merge pull request #369 from Josanoforo/claude/cierra-4-firmas-8b6f2r`. `git status` limpio, ya en `claude/firma-mesa-r3-4-33dkb1`.
2. **SHA.** `git fetch origin main` → `origin/main` = `186f090`, coincide con el declarado por el encargo (dad74ee..186f090 fue el rango del fetch, ya integrado en la base local — `main` no se movió respecto a lo declarado). Sin diferencia que refrescar.
3. **`data/raw`.** Ausente en este clon — no es paro; este acto no toca microdato ni la necesita (no abre ninguna fuente, solo re-lee cifras ya citadas en `forense/ficha-r34-condBC-v1_0.md`). No se creó ni se enlazó: fuera de perímetro de este acto.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` (NUBE, como el encargo exige). `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `000` (sin conexión — política de red de NUBE; declarado, no examina archivos, no es un negativo de A.13 sobre datos). Este acto no toca microdato ni red — el punto se corrió por disciplina de arranque, no porque el acto lo necesite.
5. **ESPEJO.** No se derivó ninguna cifra del espejo del proyecto. Todas las cifras de esta nota salen del clon de (1), comandos a la vista abajo.

## Compuerta de la ranura

La ranura de mesa llegó **precargada y afirmativa** en el propio texto del encargo:

> FIRMA M-FP157: «FIRMO FP-157: gate R3.4 = fila B; Respaldo 2 corregido por enmienda fechada.»

No está vacía ni alterada — la compuerta **pasa**. El acto ejecuta el objeto completo, no solo el paso 0-bis.

## Qué se hizo

1. **Paso 0-bis (A.3):** encargo íntegro guardado en `forense/encargos/2026-08-26-E1-CIERRA-FP157.md`.
2. **Enmienda fechada al Respaldo 2** (`forense/hitoD-preregistro-v2_0.md`, localizado en `grep -n "degrada automáticamente"` línea 871, no la línea 844 que el encargo citaba — la ficha `R3.4` real vive en el Respaldo 2 de la sección "Regla de selección de pregunta/serie", punto 3): texto de julio intacto; párrafo nuevo debajo, fechado 26/ago/2026, cita la firma verbatim y corrige el aterrizaje de "cae en la fila D" a fila `B`, conforme a la regla de precedencia de la propia escala (`D` exige que A no se cumple; A sí se cumple, `ADR-177`) y a `forense/ficha-r34-condBC-v1_0.md:185`.
3. **Emisión** al final del bloque `## Registro de veredictos archivados`: `` `R3.4` → veredicto `B` ``, formato exacto del parser `_VEREDICTO_CANONICO` (`tests/check.py:830`), con estampa A.10 del universo del gate.
4. **Contador re-derivado por parser**, no a mano:
   - `python3 tests/check.py` (antes de escribir README/estado/gobernanza) reportó: *"README.md:36 declara 23 de 27 corridas archivadas ...; el bloque append-only ... tiene 24 veredictos archivados en forma canónica"* — confirma **24 de 27**, tal como la dirección había derivado.
   - Distribución de letras derivada por comando sobre el bloque append-only (`grep -oE '`R[0-9]+\.[0-9]+` → veredicto `[A-E]`'`, deduplicando `R4.3` que archiva dos mitades A/B bajo una sola regla): **13D·4B·4A·2E·1C** — coincide con la derivación de dirección.
   - `README.md:36`, `canon/estado-programa-v1_10.md` (línea `L5`, cadena de correcciones fechadas, y la fila de la tabla de deudas abiertas) y `canon/gobernanza-v1_15.md:360` (línea "Hito D" y su cadena `Corregido de nuevo`) recifrados: `23 de 27` → `24 de 27`, `13D·3B·4A·2E·1C` → `13D·4B·4A·2E·1C`.
5. **`FP-157` → `FIRMADA`** en `forense/firmas-pendientes.tsv`: `firmada_en` = verbatim de la ranura + fecha; `ejecutada_en` = `ADR-201, ACTO CIERRA-FP157` (renumerado, ver punto 6). Tablero verificado: `awk -F'\t' '$6=="ABIERTA"{c++} END{print c+0}' forense/firmas-pendientes.tsv` → **0**. **El tablero queda con 0 filas `ABIERTA`.**
6. **ADR nuevo:** máximo re-derivado por conteo entero (`re.findall(r'ADR-(\d+)')` sobre `canon/gobernanza-v1_15.md`) → `199`, sin huecos → candidateó **`ADR-200`**. Entrada formal añadida en `canon/gobernanza-v1_15.md` inmediatamente después del cierre de `ADR-199` (antes de `ADR-188`, que en este documento no sigue orden numérico estricto). `canon/estado-programa-v1_10.md` recifrado en la misma sección (`L5`) con la cadena de correcciones extendida. **COLISIÓN, resuelta al fusionar:** `origin/main` avanzó mientras este acto corría — `PR #371` (`ACTO E2-PREP-L-RUN`) candidateó también `ADR-200` y fusionó primero, quedándose con el número. Regla de la casa, la misma de `ADR-194`/`ADR-198`/`ADR-199`: quien fusiona segundo renumera al resolver el merge, re-derivando el máximo con comando, nunca a mano. Máximo re-derivado contra el árbol ya fusionado (`re.findall(r'ADR-(\d+)')` → `200`, sin huecos) → este acto renumera `ADR-200` → **`ADR-201`**. La contribución ajena (`ADR-200`, `ACTO E2-PREP-L-RUN`) se conserva íntegra, sin editar hacia atrás. Propagado a `README.md:36`, `canon/estado-programa-v1_10.md`, `canon/gobernanza-v1_15.md` (cabecera `200→201 ADR` y cuerpo del ADR), `canon/modelo-decision-v4_0.md` y `forense/firmas-pendientes.tsv`. El encargo archivado (`forense/encargos/2026-08-26-E1-CIERRA-FP157.md`) conserva su texto verbatim sin editar — candidateaba `ADR-200` porque esa era la cifra vigente al lanzarse; la renumeración vive aquí, no ahí.
7. Esta nota.
8. `python3 tests/check.py --baseline` corrido tras todos los cambios (ver abajo).

## Contador antes/después (derivado por parser, comandos a la vista)

| | antes | después |
|---|---|---|
| Hito D archivadas | 23 de 27 | **24 de 27** |
| Distribución | 13D·3B·4A·2E·1C | **13D·4B·4A·2E·1C** |
| Tablero `firmas-pendientes.tsv`, filas `ABIERTA` | 1 (`FP-157`) | **0** |
| ADR máximo | 199 | **200** |

## Suite

`python3 tests/check.py --baseline` corrido sobre el árbol con todos los cambios de este acto — **LÍNEA BASE: VERDE**, nada nuevo frente a `tests/baseline.json` (HEAD congelado `e24d033`). Núcleo (sin `T16`): **19 FAIL · 128 WARN**, neto de WARN −1 sobre la corrida anterior (`FP-157` sale de `ABIERTA`, pasa a `FIRMADA`). Los recifrados de `19 FAIL · 129 WARN` → `19 FAIL · 128 WARN` y de `199 ADR` → `200 ADR` se propagaron a las citas vigentes de `canon/estado-programa-v1_10.md` y `canon/gobernanza-v1_15.md` (marcando `{cita-historica}` las citas que narran el estado en un punto pasado, sin editar su cifra hacia atrás). También se recifró `canon/modelo-decision-v4_0.md` (fuera del perímetro nominal del encargo, pero mantenido en sincronía por disciplina de T18/T20, como ya hacían los actos precedentes `ADR-194`/`ADR-199`).

## Perímetro respetado

Solo se tocó: `forense/hitoD-preregistro-v2_0.md` (Respaldo 2 + bloque de emisiones), `README.md:36`, `forense/firmas-pendientes.tsv` (fila `FP-157`), `canon/gobernanza-v1_15.md`, `canon/estado-programa-v1_10.md`, esta nota, y `forense/encargos/2026-08-26-E1-CIERRA-FP157.md`. No se editó el texto viejo del Respaldo 2, no se tocaron fichas o emisiones de otras reglas, no se derivó ninguna cifra del espejo, no se abrió microdato ni red.

## Lo que este acto NO hace

No re-abre la propuesta de censo B/C (`ADR-189`). No toca `tests/aceptacion_r3_4.py`. No ejerce ni siembra la vía de adquisición dirigida del reactivo de `ENSAFI 2023` (`forense/ficha-r34-condBC-v1_0.md` §7/§Anexos) — queda VENCIBLE EN ALCANCE, sembrada, no ejercida. No toca `R2.1`/`R10.1`/duelo-corredores/pool/milpa.
