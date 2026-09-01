# REGLAS-OLA5-FASE2-A — spec / PARO de P1, cita de P2

`ACTO MAESTRA33-C4`, 31/ago-1/sep/2026. Ejecuta FP-190 fase 2-A acotada a
lo que `forense/notas/2026-09-01-mapeo-fp190.md` (E7) dejó
`EXISTE-SATISFACE`: SFT-04 (regla) y TIC-01/EMP-05 (θ). Verificado antes de
empezar: `milpa/tramite.yaml` tiene 8 reglas, ninguna con `sft` en el id
(`grep -c "^  - id:" milpa/tramite.yaml` = 8; `grep -i sft milpa/tramite.yaml`
vacío).

## P1 · SFT-04 — PARO, no se congela ninguna regla

El encargo (A.8) cita SFT-04 como `EXISTE-SATISFACE`, tomando la
clasificación de la nota de mapeo. Pero la propia nota de mapeo, leída
completa, contradice esa etiqueta en el detalle que importa:

- Definición verbatim de FP-190 (`forense/firmas-pendientes.tsv:186`):
  **"SFT-04 ayuda para bañarse (ABVD)"** — la conducta es **recibir
  ayuda**.
- Candidata primaria de la nota, la única con texto de reactivo real:
  `eder2017.historiavida.dta:baniar` / `baniar_d` = **"Dificultad para
  bañarse"** / "Nivel de dificultad para bañarse" — la conducta medida es
  **tener dificultad**, no recibir ayuda. Dificultad y ayuda recibida no
  son la misma variable: alguien puede tener dificultad y no recibir
  ayuda (o viceversa, aunque menos frecuente); el ABVD estándar de
  "ayuda en actividades de la vida diaria" pregunta por la ayuda, no por
  la dificultad subjetiva.
- Las otras dos candidatas (`ABVD_BANAR_18` de ENASEM, `H16D_18`) tienen
  **texto_reactivo vacío** en el inventario (variables construidas/CSV
  sin descripción de columna) — su relación con "ayuda" viene solo del
  nombre del constructo (`ABVD_BANAR_*`), no de un texto verificado; la
  propia nota las marca "(variable, no texto)".

El encargo mismo previó exactamente este caso: *"Si la variable
recomendada mide otra conducta que la de la celda (dificultad ≠ ayuda
recibida), PARO-reporta EXISTE-NO-SATISFACE con qué falta — no fuerces."*
Es el ejemplo textual que el encargo usa, y es lo que ocurre aquí.

**Veredicto de este acto: SFT-04 → `EXISTE-NO-SATISFACE`** (revierte la
lectura de A.8, con el detalle a la vista). Qué falta: una variable con
texto de reactivo verificable que mida *ayuda recibida* para bañarse
(no dificultad, no un nombre de constructo sin texto). Candidatas más
cercanas —`ABVD_BANAR_18/21/24` de ENASEM— existen en el corpus y su
sigla es compatible, pero confirmar que preguntan por ayuda (y no por
dificultad, como su vecina `baniar`) exige abrir el diccionario de datos
de ENASEM — fuera de perímetro de este acto (no abre microdato nuevo
para esto; el encargo no autoriza adquisición ni apertura de FD nuevos).

**No hay COMMIT-1 ni COMMIT-2 de regla para SFT-04.** No se escribe
ninguna entrada nueva en `milpa/tramite-ola5-propuesta-v0.yaml` para esta
celda — forzar una p sobre `baniar` mediría dificultad, no la conducta
de la celda, y el encargo lo prohíbe explícitamente.

## P2 · TIC-01 θ y EMP-05 θ — cita, no medición

Ninguna de las dos celdas trae G# explícito en el PORQUE de
`modelo-decision-v4_0.md` (`forense/prereg-duelo-v2/cobertura-15-v1_0.tsv`:
TIC-01 y EMP-05 son `SIN-CITA-G#-EXPLICITA`). Sin generador que sostenga
la θ, no hay coeficiente que estimar contra un eje condicionante — el
régimen de dos commits que el encargo reserva para "si la θ se mide" no
aplica aquí; esto es cita, y así se registra en
`milpa/procedencia.yaml:candidatas_theta_citadas_fp190` (nueva sección).

Ambas variables se abrieron en microdato real en esta sesión (A.13, no
solo la nota de mapeo) para poder declarar `valor` y `n` con evidencia
propia:

- **TIC-01** — `ennvih:ehh09.iiia_tb.dta:tb33b_p` ("PERTENECE A
  SINDICATO(PRIN)?"). Sin `value_label` embebida en el `.dta`
  (`StataReader.value_labels()` vacío, verificado) — solo dos códigos
  crudos observados (1.0 n=1171, 3.0 n=9757; sin código 2, patrón de
  salto). No se asigna cuál código es "sí pertenece" sin el diccionario
  de datos — declarado, no inventado.
- **EMP-05** — `endireh2016:BD_MUJERES_ENDIREH2016_SitioINEGI.dta:
  sit_conyugal` ("Situación conyugal"). Igual: sin `value_label`
  embebida, 7 categorías crudas observadas (n por código en la entrada
  de `procedencia.yaml`). El calificador "joven" de la definición de
  FP-190 es atributo de universo muestral, no del texto del reactivo —
  la nota de mapeo ya lo declaraba fuera de alcance de la búsqueda por
  diseño; esta cita no lo resuelve, lo hereda.

## Perímetro respetado

No se tocó `milpa/tramite.yaml` (verificado: `git diff --stat
milpa/tramite.yaml` vacío al cerrar). No se abrió microdato fuera de los
dos payloads de P2, ya presentes en el corpus compartido (no descarga,
Anti-PR#77 no aplica). No se cargó nada al motor.
