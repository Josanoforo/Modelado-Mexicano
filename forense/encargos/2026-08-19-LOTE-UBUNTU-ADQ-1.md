# LOTE · UBUNTU-ADQ-1 — adquisición e higiene del corpus, cinco tareas en un acto

Redactado por dirección el 19/ago/2026 contra `b4a9b3f` (#292). Re-deriva al arrancar. ENTORNO ASIGNADO: UBUNTU (todo toca corpus o red a INEGI). NO nube (egreso bloqueado, medido en `FP-67`). Modelo: Opus. 🚫 `--freeze`. Dueña única: `pgrep -af claude` al arrancar y reporta.

## Doctrina de LOTE

La misma de `LOTE-NUBE-DECISIONES-1`, textual: una sesión, un PR, tareas en orden con commits `T<n>`; PARO por tarea, no por lote (el reporte es el entregable de esa tarea); línea de contador por tarea; perímetro = unión declarada, fuera = PARA global; ADR único con subsección por tarea; filas y ADR con máximo derivado al escribir Y al fusionar. Dependencia declarada: **T2 va antes que T3** (T3 escribe al manifiesto y T2 lo sanea).

## ARRANQUE

1. **REPO**: clon principal; ruta · `git log -1` · `git status`.
2. **SHA**: contra `b4a9b3f`; si se movió, refresca y reporta.
3. **`data/raw`**: enlázala al corpus real `/home/pc0/mm-corpus/raw` (hallazgo #278: `barrido2/data/raw` es symlink). Reporta: existe/enlacé/creé.
4. **ENTORNO (A.2 tres partes)**: variable · sonda `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` · `ls data/raw/ | head -1`. Crudos. Además `type grep` — esta caja envuelve `ugrep -I`: usa `command grep` con conteo de archivos examinados en todo veredicto, y recuerda el hallazgo de ayer: `xargs -0 command grep` puede devolver vacío sin correr — verifica que tu tubería examinó >0 archivos antes de aceptar un negativo.
5. **ESPEJO**: nada; cifras del disco/clon con comando a la vista.

## T1 · U2-ADQ — los indicadores de precisión que U2/EV-1 necesita

Ley: `forense/encargos/2026-08-19-U2-EV1.md` §adquisición + fila `FP-67` (asignación a Ubuntu). Descarga los CV/EE/IC oficiales (INEGI) que la ley pide, al corpus compartido (no solo tu worktree — defecto PR #77), registra en `data/manifiesto.yaml` con hash, y verifica **una invocación de `--verifica` por `--id`** (regla A.1: varios `--id` en una invocación solo verifica el último). Las tres respuestas no se colapsan: AUSENTE · raíz-no-configurada · hash-discordante. Deja dicho en la nota qué puede ya recalcular U2/EV-1 con esto. **Contador: payloads nuevos al manifiesto, número dicho.**

## T2 · MANIFIESTO-49 — los payloads contados dos veces

Ley: hallazgo 18/ago (`tests/corpus.py` C3: 49/49 registrados-sin-resolver Y presentes-sin-registrar — el mismo archivo dos veces). Deriva la lista vigente EN LA CAJA (aquí el corpus sí está montado; el 612 que da una caja sin corpus es raíz-no-configurada, no esto). Adjudica por payload: corrige la raíz/ruta del manifiesto para que resuelva, o registra el presente-sin-registrar con su hash, o marca AUSENTE real con universo. Meta: `corpus.py` C3 = 0 en la caja, **sin borrar ninguna entrada histórica** (se corrige, no se poda). **Contador: 0 (higiene), pero di el C3 antes→después.**

## T3 · FP-17 — las descargas de la etapa 8 de FP-26

Ley: la fila `FP-17` y su encargo/cola referida (léela; es tu ley, no este resumen). Ejecuta las descargas pendientes con el mismo protocolo de T1 (corpus compartido, hash, una invocación por id, doble descarga y comparación byte a byte si la fuente trae token — patrón A.7/#277). Al cerrar, di explícitamente si con esto la etapa 8 de `FP-26` queda ejecutada. **Contador: payloads, número dicho.**

## T4 · Los 3 PDFs REFERENCIADO-NO-ABIERTO

Ley: `data/censo-explotacion-2026-08-17.tsv` (filas pdf con ese estado). Ábrelos (`pdftotext`/`pdfplumber` — **NO `pdfinfo` como oráculo de cifrado**: hallazgo de los 83 falsos `PDF_CIFRADO`), veredicto A.4 por archivo contra lo que los referencia, actualiza su estado en el censo. **Contador: 0 salvo hallazgo sustantivo.**

## T5 · `variable_id` para las 21 co-observables del cableado

Ley: hallazgo COEF (`reactivo_id` es idéntico a `objeto_logico_id` en 37/37 y ninguna nombra variable) + `data/coef-universo-v1_0.tsv` (las 21 con `co_observacion=S`). Para cada una, deriva del **codebook** del payload el nombre real de variable (exposición y desenlace) y escríbelo en columna nueva `variable_id` (o tabla puente si el esquema de cableado-universo no admite columna — en ese caso el hueco de esquema es entregable y lo reportas antes de inventar). Sin abrir microdato más allá del codebook; sin medir nada aquí — esto es el cimiento para que el siguiente lote de medición no adivine variables. `T23` debe seguir verde. **Contador: 0; di cuántas de 21 quedaron con variable resuelta y cuántas NO-ENCONTRADO-EN-CODEBOOK.**

## Cierre del lote

ADR único (número derivado al escribir Y al fusionar) · hallazgos, una línea por hallazgo real · nota con tabla T1–T5, contadores y C3 antes/después · encargo CONSUMIDO · `tests/check.py --baseline` y `tests/corpus.py` VERDES en la caja, salidas pegadas.

## Perímetro (unión; fuera = PARA)

Corpus compartido y `data/raw` (escritura solo de payloads nuevos T1/T3) · `data/manifiesto.yaml` (T1/T2/T3, append/corrección) · `data/censo-explotacion-2026-08-17.tsv` (T4, solo esas 3 filas) · `data/coef-universo-v1_0.tsv` o tabla puente (T5) · tablero (`FP-17` y las que tus tareas ejecuten) · gobernanza (ADR) · estado-programa (cascada) · hallazgos · nota · este encargo. Si puedes usar agentes en sonnet úsalos y tú supervisas el trabajo.

---

## Estado de consumo

**CONSUMIDO** por `ACTO LOTE UBUNTU-ADQ-1`, 19/ago/2026 — ver `forense/notas/2026-08-19-lote-ubuntu-adq-1-cierre.md`.

## CONSUMIDO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `git grep -Fl -- "2026-08-19-LOTE-UBUNTU-ADQ-1.md"` (excluyendo forense/digesto/) cita nota(s) de cierre: forense/notas/2026-08-19-lote-ubuntu-adq-1-cierre.md. Encargo pre-ADR-por-archivo (anterior al 18/ago/2026): la evidencia de ejecución vive en la nota de cierre, no en canon/gobernanza-v1_15.md. Marca ausente era defecto de trámite retroactivo, resuelto por esta auditoría.
