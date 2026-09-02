# ENCARGO · ACTO MAESTRA35-N3 · SELLA-CIVICA-L6

Redacta dirección (Fable), 2/sep/2026, contra v2.12. Estado: LISTO PARA LANZAR. COMPUERTA: ninguna — declaración explícita. ENTORNO ASIGNADO: NUBE (`cloud_default`). NO se lanza en UBUNTU — no abre microdato; las cajas están ocupadas por MAESTRA35-L1 y MAESTRA35-L2. MODELO SUGERIDO: Sonnet (propagación mecánica, cero estimaciones; SELLA-3).

## Carriles

MAESTRA35-L1 (caja: `tools/medidor_*`, propuesta — appends de `tramite.*`/`dinero.*` al pie, `codificacion-R`) · MAESTRA35-L2 (caja: `tools/arbitra.py`, `corridas-R/`) · MAESTRA35-N2 (nube: `tools/emite_m.py`, `corridas-M/`, `exclusiones-v1_2.md`) · `/despacha` N3 → N5 (nube: corredor). Este acto edita DOS entradas `civico.*` existentes de la propuesta (líneas 594 y 873) y el tablero; no toca nada de los perímetros anteriores. MAESTRA35-L3 (caja, cívica) appendea una entrada nueva al pie de la propuesta: distinto rango de líneas. Renumera quien fusiona segundo.

## Firmas de mesa — verbatim, 2/sep/2026

El ejecutor propaga, no decide (SELLA-3). Mesa: «a1, b1 y c1.» — respuesta a la presentación en RH de FP-239, cuyas letras se reproducen aquí para que el ejecutor no las reconstruya:

* **a1** = aceptar el veredicto REFUTADA-COMO-CAUSAL de ACTO MAESTRA34-L6 sobre `civico.participacion.contingente_escalonado_2016_2024`; tier MEDIA, con la reserva escrita («2 de 14 entidades tratadas; wild cluster por entidad con p mínimo alcanzable 0.125; el bootstrap por municipio, que no sufre ese límite, también contiene cero»); sin cargar al motor (un Δ en pp no es una probabilidad, y está refutado como causal).
* **b1** = mover la entrada de ACTO MAESTRA34-L4, `civico.participacion.contingente`, a REFUTADA-COMO-CAUSAL citando a su sucesora, cuerpo intacto (p, Δ, IC, n, fuente, ponderador, universo: ni una cifra se toca).
* **c1** = autorizar el sucesor con el diseño corregido (efecto fijo de TIPO de año federal: presidencial / intermedia / sin federal) y la adquisición de las 12 entidades tratadas que faltan, empezando por Hidalgo. Este acto NO lo ejecuta: lo ejecuta ACTO MAESTRA35-L3; aquí solo se registra la firma.

Firmas previas que este acto cita y no re-decide: DC1-d (mesa, 2/sep/2026, «d») que dejó la entrada de L4 en MEDIA / APARCADA-HASTA-IDENTIFICACION vía MAESTRA34-N9; DE1 (no más actos de revisión operativa).

## Verificación de existencia (A.8) — contestada por dirección contra b6b923f

**(1) Estructura.** Propuestas → `milpa/tramite-ola5-propuesta-v0.yaml` (acumulador único; enmiendas in situ fechadas, cuerpo intacto — precedente `familia.corresidencia.adulto_familiar`); tablero → `forense/firmas-pendientes.tsv` (a mano). El motor `milpa/tramite.yaml` NO tiene ninguna regla `civico.participacion.*` (`grep -c "civico.participacion" milpa/tramite.yaml` → 0): nada que tocar ahí, y a1 lo confirma.

**(2) Contenido**, comando y salida cruda:

* `grep -n "^ - id: civico.participacion" milpa/tramite-ola5-propuesta-v0.yaml` → 594 (`contingente`, `situacion: APARCADA-HASTA-IDENTIFICACION # DC1-d…`, `tier: MEDIA # DC1-d…`, conducta `participa_mas_si_la_local_es_concurrente delta_pp 10.4790`) y 873 (`contingente_escalonado_2016_2024`, `situacion: PENDIENTE-DE-MESA`, `tier: PENDIENTE-DE-MESA`, `veredicto_falsador: REFUTADA-COMO-CAUSAL`, `delta_pp 0.0149`). → EXISTE-NO-SATISFACE ×2 (existen, sin la firma).
* `grep -P "^FP-239\t" forense/firmas-pendientes.tsv | cut -f6` → ABIERTA. FP máximo por comando 240; ADR máximo 289.

**(3) Cobertura retroactiva.** Ambas entradas nacen el 2/sep (PR #466 y #468), posteriores a las dos tablas; cubiertas.

## Piezas (cero estimaciones; toda cifra se copia verbatim de la propuesta y de ADR-288)

**P1 · a1 sobre la línea 873.**
`situacion: PENDIENTE-DE-MESA` → `situacion: SELLADA-SIN-CARGA # firma a1 (mesa, 2/sep/2026), ACTO MAESTRA35-N3 -- veredicto REFUTADA-COMO-CAUSAL aceptado; NO se carga al motor: un Δ en pp no es una probabilidad`.
`tier: PENDIENTE-DE-MESA` → `tier: MEDIA # firma a1 (mesa, 2/sep/2026), ACTO MAESTRA35-N3`.
Campo nuevo `reserva_tier:` con el texto de a1 entre comillas, más las cifras de ADR-288 verbatim: β = +0.0149 pp; IC95 wild cluster por entidad [−3.3765, +3.4064]; IC95 bootstrap por municipio [−1.3865, +1.3312]; 4 entidades medibles de 14 tratadas, 2 tratadas; p mínimo alcanzable del wild cluster con 4 conglomerados 0.125.
Campo nuevo `lectura_no_refutada:` verbatim de ADR-288: «ATT(Coahuila 2017→2018, presidencial) = +2.4113 pp IC95 [+1.53, +3.28]; ATT(Nayarit 2017→2021, intermedia) = −5.6914 pp IC95 [−6.94, −4.38]; ninguno cruza cero» — es la hipótesis que MAESTRA35-L3 pre-registra, y viaja con la entrada para que nadie la lea como «no pasa nada». `veredicto_falsador`, `nota`, `delta_pp`, `clase`: intactos.
ESTAMPA A.10 en la misma enmienda: universo = 4 entidades / 2 tratadas, SHA 11af678 (árbol de L6).

**P2 · b1 sobre la línea 594.**
`situacion: APARCADA-HASTA-IDENTIFICACION # DC1-d…` → `situacion: REFUTADA-COMO-CAUSAL # firma b1 (mesa, 2/sep/2026), ACTO MAESTRA35-N3 -- ver sucesora civico.participacion.contingente_escalonado_2016_2024 (ACTO MAESTRA34-L6, ADR-288); el Δ +10.4790 pp se reinterpreta como efecto de anio; la asociacion medida sigue siendo cierta y se conserva integra`.
`tier: MEDIA` se conserva con comentario añadido `# tier de la ASOCIACION (DC1-d); la lectura causal es la refutada`. Ninguna otra línea de la entrada cambia; el comentario histórico de DC1-d se conserva encima.
Estampa A.10: la lectura de L4 fue correcta contra su universo (163 municipios, un par de años) y quedó VENCIDA EN ALCANCE cuando L6 lo amplió a variación escalonada — escríbelo en el comentario con esas palabras, porque es el caso de libro de A.10.

**P3 · Tablero y hallazgos.**
FP-239 → `FIRMADA`, firmada_en `"a1, b1, c1 (mesa, 2/sep/2026, verbatim: a1, b1 y c1.)"`, ejecutada_en = ADR de este acto para (a) y (b) + `"c1 pendiente: ACTO MAESTRA35-L3"`.
Una línea en `forense/hallazgos.md`: `2026-09-02 · MAESTRA35-N3 · cívica: participacion.contingente REFUTADA-COMO-CAUSAL (L4 y L6 reconciliadas, cuerpo intacto); sucesor L3 autorizado (c1). Motor sin cambio.`

## Perímetro y concurrencia

`milpa/tramite-ola5-propuesta-v0.yaml` (dos entradas existentes, enmienda in situ; ningún append, ninguna línea `tramite.*`/`dinero.*`/`familia.*`) · `forense/firmas-pendientes.tsv` (una fila a FIRMADA) · `forense/hallazgos.md` (una línea) · A.3 · cascada de `/acto` (gobernanza, estado-programa, registro-rotulos: censa `MAESTRA35-N3` y `MAESTRA35-L3`, L0, T25, `tests/check.py --baseline`). NO toca `milpa/tramite.yaml`, `tools/`, `corridas-*`, `data/`, `instrucciones-proyecto-*`. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.

## FP/ADR candidatos

Ninguna fila nueva salvo hallazgo propio (primer FP libre al arrancar; máximo derivado 240, con rangos pre-asignados a L1/L2/N2 — dilo). ADR candidato por el comando de la casa (289 → primer libre); renumera quien fusiona segundo.

## Contador

Cero directo, declarado — mueve dos estados de sello, no un número. Reglas del motor: sin cambio.

## Lo que este acto NO hace

No mide; no carga la cívica al motor; no toca las entradas que L1/L3 escriben; no lanza L3; no edita instrucciones.

## Sucesores declarados, no lanzados

ACTO MAESTRA35-L3 · CIVICA-TIPO-DE-BOLETA (caja, c1).

## CONSUMIDO

Ejecutado por ACTO MAESTRA35-N3 · SELLA-CIVICA-L6 en la rama
`claude/maestra35-n3-launch-vhtedz`, commits `b374b93` (0-bis A.3),
`9da7b58` (P1-P3 + cascada: ADR-290, gobernanza, estado-programa L0,
registro-rotulos, T25 sin novedad, `tests/check.py --baseline` VERDE).
`PR #473`.
