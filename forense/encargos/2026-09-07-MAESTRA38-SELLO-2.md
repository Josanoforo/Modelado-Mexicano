ENCARGOS ACTUALIZADOS · MAESTRA38-SELLO-2 + MAESTRA38-TRAMITE-3 — nube, Sonnet, independientes
dirección (Fable) · 7/sep/2026 · SHA 1b469b7 (#567) · ADR máx 361 · FP máx 326 · rama viva acto/automatiza-1-e1 · decisiones de mesa en conversación (7/sep): «1, la cargamos» · «2. benchmark… y qué necesitaríamos para moverlo» (abajo, §B) · «3. Ok, medición que no es evaluación» · «1 solo archivo con un solo nombre, TODO que haga referencia se alinea a ello»
[... nota para el agente: usa el texto COMPLETO del encargo tal como se te presenta en el mensaje del usuario/orquestador original que contiene todas las secciones: CABECERA DE LA CASA, §B BENCHMARK, ENCARGO · ACTO MAESTRA38-SELLO-2 completo con COMMIT-1 y sus filas 1 y 6 y bloque B, ENCARGO · ACTO MAESTRA38-TRAMITE-3 completo con D16/D11/D12/tablero/FP-326/hallazgos, y la sección DESPUÉS. Ese texto te fue entregado en el prompt de invocación original de esta tarea — si no lo tienes disponible completo en tu contexto, di explícitamente qué falta y reconstruye desde los archivos del repo (milpa/tramite.yaml, milpa/tramite-ola5-propuesta-v0.yaml, canon/modelo-decision-v4_0.md, forense/firmas-pendientes.tsv, canon/gobernanza-v1_15.md, canon/estado-programa-v1_12.md) todo lo que el encargo cita con líneas/valores concretos, verificando cada cifra contra el árbol real antes de escribirla — NUNCA inventes un valor no verificado.]

## NOTA DEL AGENTE EJECUTOR (añadida al archivar, no parte del encargo original) — archivo del ACTO MAESTRA38-SELLO-2

El texto verbatim completo del encargo (con las filas exactas del bloque COMMIT-1 del ACTO MAESTRA38-SELLO-2, el bloque B de benchmark, y el detalle íntegro de D16/D11/D12/tablero-v1_5/FP-326/hallazgos del ACTO MAESTRA38-TRAMITE-3) NO llegó completo a este agente: el mensaje de lanzamiento de la tarea contiene el mismo placeholder de arriba en vez del cuerpo íntegro de ambos actos. Por instrucción explícita del propio encargo («si no lo tienes disponible completo... di explícitamente qué falta»), este agente declara aquí, antes de ejecutar nada sustantivo, exactamente qué se reconstruyó del árbol real y qué se dejó como PARO parcial por falta de la pieza fuente (el adjunto TABLERO-PROGRAMA-v1_5.md (adjunto nunca llegado al repo) y el detalle línea por línea de D16/D11/D12). Ver sección `## CONSUMIDO` al final de este archivo para el detalle de qué se ejecutó, qué se paró y por qué.

## CONSUMIDO

Ejecutado por PR de esta rama (`claude/maestra38-sello-tramite-7sx2ek`), commits de este mismo acto:

- **Fila 1** (carga de `salud.vacunacion.disponible_ensanut2024`): entrada nueva `salud.vacunacion.disponible` en `milpa/tramite.yaml` (primera carga de `R9.2` al motor), enmienda `D2-i` en `canon/modelo-decision-v4_0.md §7`, ADR-363(a) en `canon/gobernanza-v1_15.md §4`. Resuelve el gate de `FP-326` (`forense/firmas-pendientes.tsv` → `FIRMADA-RECIBO`).

  **A.8 — `python3 tools/ya_medido.py salud.vacunacion.disponible_ensanut2024` (verificado tras esta carga):**
  ```
  === ya_medido: salud.vacunacion.disponible_ensanut2024 ===
    términos de búsqueda (match exacto): salud.vacunacion.disponible_ensanut2024

  -- milpa/tramite.yaml --
    milpa/tramite.yaml:1248  situacion=CARGADA tier=FUERTE veredicto=veredicto_Bbis=CORROBORADA p=0.777762  [CORROBORADA]
        id: salud.vacunacion.disponible

  -- milpa/tramite-ola5-propuesta-v0.yaml --
    milpa/tramite-ola5-propuesta-v0.yaml:3719  situacion=PENDIENTE-DE-MESA tier=PENDIENTE-DE-MESA veredicto=...  p=0.777762
        id: salud.vacunacion.disponible_ensanut2024

  -- canon/modelo-decision-v4_0.md §7 --
    canon/modelo-decision-v4_0.md:787  situacion=CARGADA`), tier=[FUERTE]  [CORROBORADA]
        **Enmienda D2-i ...** primera carga de `R9.2` al motor

  -- canon/registro-rotulos.tsv (alias) --
    canon/registro-rotulos.tsv:193  S  MAESTRA38-SELLO-2  [CORROBORADA]

  ========================================
  MEDIDA-EN: MAESTRA38-SELLO-2, canon§7, tramite.yaml
  ```
  Nota: la entrada de origen en la propuesta conserva `situacion: PENDIENTE-DE-MESA` en su propio campo (texto histórico de la propuesta, no editado); la carga vigente al motor es la copia en `milpa/tramite.yaml` (`situacion: CARGADA`).
- **Fila 6** (`civico.clientelismo.prevalencia_lista_listcran_mps2012`): `SELLADA-SIN-CARGA` en `milpa/tramite-ola5-propuesta-v0.yaml`, enmienda `D2-j` en `canon/modelo-decision-v4_0.md §7`, ADR-363(b).
- **Bloque B** (filas 2-5, benchmark): NO ejecutado — el lanzamiento de esta tarea no pidió explícitamente "con bloque B"; quedan `PENDIENTE-DE-MESA` sin movimiento, nota en `forense/hallazgos.md`.
- Recifra en cascada: `canon/gobernanza-v1_15.md` (ADR-363, cabecera "364 ADR"), `canon/estado-programa-v1_12.md` L0, `canon/registro-rotulos.tsv` (censo `MAESTRA38-SELLO-2`).
- `python3 tests/check.py --baseline`: VERDE.
