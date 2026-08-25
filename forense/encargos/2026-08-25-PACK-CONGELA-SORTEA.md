# PACK `CONGELA-SORTEA` — ruling de mesa (marco v1 · pool 253 · n_sorteo) + congelado + sorteo real de `ACT-PIL-3` · dos actos, dos PR

**Estado de este archivo:** **CONSUMIDO**. `ACTO A` (`CONGELA-SORTEA`, `ADR-179`, `FP-154`) y `ACTO B` (`SORTEA`, `ADR-188`) cerrados — ver `forense/notas/2026-08-25-congela-cierre.md` y `forense/notas/2026-08-25-sortea-cierre.md`.

SHA de redacción: `dfdf4fd` (`origin/main` al redactar, verificado por clon; merge de `#352`). Redactado por: sesión de dirección (maestra), 25/ago/2026. Mandato de mesa verbatim: «traigo un elemento de chatgpt, revísalo y dame el encargo extendido, necesitamos desbloquear las firmas, sellos o congelados para avanzar con esta entrega».

Firma de mesa recibida en el lanzamiento del `ACTO A`, fuera de la cita de esta compuerta (candado de autocaptura, `FP-63`):

> `FIRMO: para el piloto v1 gobierna el marco vigente de 60 bajo FP-150/ADR-178; las 253 de #349/#352 son pool de saturación (marco-produccion-total-v1_0.tsv se lee como pool-candidatas-autorizadas), no marco v1; FP-82 queda satisfecha como barrido y medición de la oferta. Fijo n_sorteo=15 dentro del rango pre-registrado 12–15. Procede CONGELA-SORTEA.`

ENTORNO ASIGNADO: NUBE (`cloud_default`) para AMBOS actos. `ACTO B` solo puede lanzarse DESPUÉS de que el PR del `ACTO A` esté fusionado — el reglamento sellado (§3, `forense/prereg-duelo-v2/sorteo-act-pil-3-v2-PROPUESTA.md`) deriva la semilla del SHA de merge, y ese SHA no existe antes de fusionar.

## Perímetro

**`ACTO A`** (este cierre, `ADR-179`) tocó: `forense/marco-candidatas-piloto-v1_0.tsv` (solo la celda `frase_discriminacion` de `DIN-09`) · nuevos en `forense/prereg-duelo-v2/`: `marco-congelado-piloto-v1_0.tsv`, `sorteo_v2.py`, `tests_sorteo_v2.py`, `CONGELADO-v1_0.sha256` · `canon/gobernanza-v1_15.md` (`ADR-179`) · `forense/firmas-pendientes.tsv` (`FP-154`, nace `FIRMADA`) · `canon/estado-programa-v1_10.md` (recifrado + nota) · `forense/notas/2026-08-25-congela-cierre.md` · este archivo.

**`ACTO B`** (pendiente, tocará): nuevo `forense/prereg-duelo-v2/sorteo-resultados-v1_0.md` · gobernanza (ADR-B) · tablero (`ejecutada_en` de `FP-154`) · estado · `forense/notas/2026-08-2X-sortea-cierre.md`. No toca marco, congelado, `sorteo_v2.py` ni reglamento.

Ver `forense/notas/2026-08-25-congela-cierre.md` para el detalle completo del cierre de `ACTO A`, y `ADR-179` (`canon/gobernanza-v1_15.md`) para el ruling.

## Lo que este pack deliberadamente NO hace

No toca las 253 ni `data/curacion-universo/**` ni `tools/**`. No calcula CV/`n` para 60 ni para 253. No corre ni encarga sesiones `L`. No declara saturación. No reabre la curación del marco. No adjudica veredicto del piloto. No mueve Hito D ni `README.md`.
