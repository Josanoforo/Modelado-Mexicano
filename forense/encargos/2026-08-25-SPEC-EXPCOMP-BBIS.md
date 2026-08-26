# Encargo `SPEC-EXPCOMP-BBIS` — redactar, a ciegas del microdato, la spec B-bis de la llave `EXP-COMPARTAMOS-1`

**Dirección, 25/ago/2026. ENTORNO: NUBE. SHA de redacción: `ba0a7e4`.**

**Por qué existe.** `forense/registro-llaves-identificacion-v1_0.md:64` (fila `EXP-COMPARTAMOS-1`, clase (iii), `SELLADA_NO_EJERCIDA`, `ADR-162`) declara que falta una spec B-bis, congelada antes de tocar el microdato, que declare qué θ o qué generador del modelo informa esta evidencia. La necesidad propia que la ancla ya la abrió `FP-147` (opción b de mesa: no reutiliza `confianza_institucional` ni `radio_confianza`) y el motor ya puede consumir la clase (`FP-144` implementado, `EVIDENCIA_EXPERIMENTAL_TERCEROS`).

**Ceguera.** Prohibido abrir el microdato del paquete (`.dta`/CSV de Compartamos-AEJ). Insumos permitidos, lista cerrada: `forense/registro-llaves-identificacion-v1_0.md:64` y §10 · `forense/notas/2026-08-25-eval-compartamos.md` · la fila `openicpsr — Compartamos AEJ` de `data/diseno-muestral.yaml` · los `.do`/documentación ya citados ahí · la necesidad `FP-147` · el molde de `forense/hitoD-R10_1-spec-v2_0-PROPUESTA.md` (`FP-128`) · `canon/modelo-decision-v4_0.md` §2 y `milpa/procedencia.yaml`.

**Entrega.** `forense/spec-bbis-exp-compartamos-v1_0-PROPUESTA.md` (COMMIT 1): objetivo, estimando, escala del veredicto ANTES del dato, escala B-bis completa con precedencia, límites. Ninguna firma en este acto — entrega una PROPUESTA; el sello es fila nueva de mesa.

**Perímetro.** La spec nueva · tablero (una fila) · gobernanza · estado · nota · encargo archivado. No abre microdato, no ejerce la llave, no toca `milpa/`, no fija números, no adjudica.

**CONSUMIDO** por este acto — ver `forense/notas/2026-08-25-spec-expcomp-bbis-cierre.md`.
