# Nota · ACTO GEN2-TRAMITE-FIRMAS-7 · 22/sep/2026

Encargo: `forense/encargos/2026-09-22-GEN2-TRAMITE-FIRMAS-7.md` (A.3, sello de cuerpo en el 0-bis).

## Tabla firma · fila · qué desbloquea

| Firma | Fila en `decisiones.tsv` | FP → estado | Qué desbloquea |
|---|---|---|---|
| **F1** · K2 réplica | `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002` → `cuenta_gen2=NO` (RÉPLICA de `-0001`; verificado en este acto 92/92 RESULT idénticos, delta 0, contra `resultados.json` completo de ambos CALC) | sin FP (decisión directa de mesa en el cuerpo del encargo) | `N_corridas_selladas` baja 1 (la `-0002` deja de contar aparte de la `-0001`); cierra la duplicación de contador que motivó la firma. |
| **F2** · ENIF-IC 2868-01 | `FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01` → `firma=ADOPTAR-CON-RESERVA-DE-ANCHO` | ABIERTA → **FIRMADA** | Las 32 marginales de ENIF 2024 quedan adoptadas (piso t−1) con el IC rotulado «conservador»; desbloquea que el marcador/informe las cite sin llamar al ancho cobertura. Pregunta aneja de mesa (¿calibrar τ solo con 2018→2021?) sigue abierta — no bloquea esta firma. |
| **F3** · MARCO-M 02e6-01 | `FP-260922-GEN2-MARCO-M-CONSUMIDOR-1-02e6-01` → `firma=HISTÓRICO-SIN-RETIRO` | ABIERTA → **FIRMADA** | El marco M deja de ser candidato a lecturas nuevas sin romper las 7 herramientas que hoy lo leen; desbloquea el mapa de sustitución (43 lecturas SIN-SUSTITUTO) como el único gate para el retiro futuro. |
| **F4** · `origen_numerico` (NC c45c-01) | **YA HECHO** — `git log -S` muestra `5ef1f41` (PR #1002, en `origin/main`) acreditando las 15 filas `origen:CALC-PISOS-ENVIPE2024-EJES-0002:<RESULT>` con `origen_numerico=NUEVO`. La FP `…-c45c-01` ya está `FIRMADA` y la NC `…-c45c-01` ya está `CERRADA` desde ese PR. Este acto no repite la fila (sería un duplicado del mismo objeto): confirma el estado y sigue con lo que falta. | ya `FIRMADA`/`CERRADA` (PR #1002) | Nada nuevo que desbloquear por esta vía — **pero el propio commit de cierre declaró `adoptados_activos 72 → 87` sin que quedara commiteado**: `milpa/estimadores-por-segmento.yaml` nunca se regeneró con `marcador_segmento.py --escribe` (última tocada en `78a406c`, PR #957; sin clave `marginales`). Hallazgo en `forense/hallazgos.md` (no impide medir, §1); NC `…-369b-02` con sucesor que tenga `milpa/` en su perímetro. |
| **F5** · Hoja de adopción 18fa-01 | `FP-260922-GEN2-TRAMITE-PENDIENTES-1-18fa-01` → `firma=ADOPTAR-10-VETAR-2` (mesa no editó la lista de la hoja: los 10 ADOPTAR y los 2 VETAR quedan tal como los escribió TRÁMITE-PENDIENTES-1). Los 2 VETAR (`RESULT-CTX-2021-P-ALTO`, `RESULT-EDER-A-P`) sí quedan asentados como `adopcion=VETADA-POR-DECISION` — contabilidad pura en `decisiones.tsv`, no toca `milpa/` — y mueven `N_resultados_gen2_pendientes_adopcion` 12→10 y `N_resultados_gen2_vetados_por_decision` 2→4. | ABIERTA → **FIRMADA** | La firma queda registrada y auditable; los 2 vetos ya cuentan. **La mecánica de bloque (`[ADOPCION-BLOQUE 18fa-01]`) para los 10 ADOPTAR NO se ejecutó**: el único mecanismo existente para que un RESULT cuente como uso activo GEN2 (`corrida0_resultado_id` + `rol_uso: proxy_descriptivo`, precedente `milpa/tramite.yaml:185-188`) exige escribir en `milpa/tramite.yaml` — y el propio encargo (§9 Perímetro) marca `milpa/` como AJENO a este acto. Las cuatro reglas de la hoja (Banxico, LAPOP, MOTRAL) ya traen los campos `corrida0_resultado_id`/`rol_uso: proxy_descriptivo` completos en `milpa/tramite-ola5-propuesta-v0.yaml:3985-4090` — sólo falta moverlas/citarlas desde un consumidor activo. Confirmé el SUPUESTO de la cabecera es FALSO dentro de este perímetro: NC `…-369b-01` abierta con sucesor. |

## Contador, antes/después (este acto)

Medido con `python3 tools/corrida0.py status` sobre el árbol de este acto:

```
N_corridas_selladas: 164 → 163 (cuenta_gen2 NO de K2-0002, F1)
N_resultados_gen2_pendientes_adopcion: 12 → 10 (los 2 VETAR de F5 quedan `adopcion=VETADA-POR-DECISION` en decisiones.tsv — contabilidad, no adopción; salen de la cola)
N_resultados_gen2_vetados_por_decision: 2 → 4 (los 2 nuevos vetos de F5, sumados a los 2 precedentes RESULT-C1-POSEL-*)
N_resultados_gen2_adoptados_activos: 72 (sin cambio — los 10 ADOPTAR de F5 no se movieron: NC …-369b-01. El hallazgo de que ya debería leer 87 por F4 es de PR #1002, no de este acto — NC …-369b-02)
```

## Verificación de premisas (§0/§4)

- `[EJECUTADO]` (encargo §3): 0 filas con `K2-…-0002`, `RESERVA-DE-ANCHO`, `HISTÓRICO-SIN-RETIRO` en `decisiones.tsv` al redactar — confirmado antes de escribir.
- `[EJECUTADO]` (encargo §3): 15 filas con `origen_numerico` — confirmado, y trazado a `5ef1f41`/PR #1002 (F4 ya hecho).
- `[LEÍDO]` FP `…-2868-01`, `…-02e6-01`, `…-18fa-01`: releídas en `origin/main` fusionado, mismo contenido que cita el encargo, las tres siguen `ABIERTA` al arrancar.
- `[SUPUESTO]` mecanismo de adopción por bloque: **refutado dentro del perímetro declarado** (F5, arriba). Camino previsto por la propia cabecera («si resulta falso, P2 abre NC… y el bloque queda en la FP FIRMADA, sin ejecutar») seguido tal cual.

## Pregunta de mesa (§6, latitud) — no bloqueó el resto del acto

¿Un RESULT de la hoja `18fa-01` que cambió de `verify` desde #1011 se adopta con el veredicto nuevo o se saca del bloque? Verificado: la hoja (`ba50030`) es posterior a los cuatro CALC que cita y nada tocó `verify.yml`/esos CALC desde entonces — el `verify` no cambió. Pregunta queda sin materia por ahora; se reabre si el sucesor de F5 encuentra otra cosa.
