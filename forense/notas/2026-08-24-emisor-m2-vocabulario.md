# Nota · `ACTO EMISOR-M-2` — dos variables dependientes y disparadores por componente

*(24/ago/2026. Entorno NUBE (`cloud_default`), modelo Opus. Base: `origin/main = bcd318f`, incluye `SELLA-AGO24`/`PR #310` ya fusionado — verificado por la presencia de `forense/notas/2026-08-24-corrobora-motor.md` en el árbol al arrancar. `data/raw` no aplica: este acto no la usa. Sin red: no se abre ninguna fuente externa.)*

## Qué hace

Ejecuta la reformulación de `FP-104` que `ADR-145`/`D3` dictó (firma de mesa verbatim citada ahí y en `canon/gobernanza-v1_15.md` §ADR-145): da al emisor dos variables dependientes (`cumplimiento`, `adopcion`) y seis disparadores por componente, de forma que ninguna celda futura pueda medir una diciendo que mide la otra.

## Vocabulario — dónde vive y por qué (T1)

Declarado en `milpa/src/emisor.py:362+` (sección "Vocabulario EMISOR-M-2"), no en el crosswalk pregunta↔regla ni en un contrato nuevo: `emisor.py` ya es quien gobierna el vocabulario de disparadores del gate (`CTX_A`/`CTX_B`, `riesgo_fiscal_percibido`, `emisor.py:227-229`), y las celdas-D consumen ese vocabulario a través de su campo `dominio` (`tests/test_celdas_d.py:70`, enum `DOMINIOS`). "tecnología/pagos/registros" del encargo mapea al único valor del enum que los cubre: `TEC` (`DOMINIOS_EXIGEN_DV_M2 = {"TEC"}`).

Validación dura (`valida_dv_celda_m2`): una celda de dominio `TEC` sin `variable_dependiente` produce error nombrando este acto (`ACTO EMISOR-M-2`); una `variable_dependiente` fuera de `{cumplimiento, adopcion}` también; los `disparadores_m2` declarados, si los hay, se validan contra el enum de cada uno.

## T2 — estampa de base extendida, tal cual, sin maquillar

`emisor.estampa_base_extendida_m2()`, derivada de las clases (`clase:`) realmente consumidas por `milpa/tramite.yaml` (`cargar_reglas()`), no tecleada:

```
estampa de base extendida EMISOR-M-2 (T2, casi ninguno tiene base medida):
  dato_sensible: SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla
  friccion_uso: SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla
  lado_obligado: SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla
  riesgo_fiscal_percibido: SIN BASE MEDIDA — clases consumidas: ['ASIGNADO'] (ninguna MEDIDO)
  sancion: SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla
  utilidad_marginal_sobre_sustituto: SIN-REGLA-QUE-LO-USE — el disparador no está aún cableado a ninguna regla
```

**Casi ninguno**, tal como el encargo predijo: de los seis, cinco no están cableados a ninguna regla del dominio `tramite`, y el sexto (`riesgo_fiscal_percibido`, el único ya existente) solo tiene clase `ASIGNADO` — las 10 probabilidades de `tramite.yaml` (v0.3.0) son ASIGNADAS por mesa, ninguna `MEDIDO` (`milpa/tramite.yaml:9-16`).

## T3 — tests

`tests/test_emisor_m2.py`, 7 casos: (a) celda `TEC` sin DV → rechazo con mensaje que nombra el acto; (b) celda `TEC` con DV + disparadores bien formados → `errs == ()`, sin adjudicar nada; disparador desconocido y enum inválido → rechazo; dominio no cubierto (`FIN`) → no exige DV; (c) verificado por separado corriendo `tests/test_emisor_fidelidad.py` + `tests/aceptacion_r3_4.py` + `tests/test_celdas_d.py` sin editarlos: siguen verdes.

```
$ python -m pytest tests/test_emisor_m2.py tests/test_emisor_fidelidad.py tests/aceptacion_r3_4.py tests/test_celdas_d.py -q
...                                                                     [100%]
```

## T4 — documento fuente

`COERCION-Y-ADOPCION-rediseno-2026-08-20.md` no llegó adjunto a este acto. Por `transfer §9` NO se reconstruye. Se creó `forense/coercion-adopcion-espec-operativa-v0_1.md`, rotulado `PROPUESTA·PARCIAL`, solo con el bloque inline que dirección pegó en el encargo. Fila `FP-113` añadida a `firmas-pendientes.tsv` pidiendo a mesa el documento íntegro.

## T5 — discrepancia CoDi

No se resuelve aquí (sin red). Citada en `forense/coercion-adopcion-espec-operativa-v0_1.md`, apuntando a `forense/hitoD-preregistro-v2_0.md` (sección "Discrepancia numérica encontrada al verificar la ancla", ficha de R3.4, ≈línea 810): `tramite.yaml:61` dice 3.09M vs. report 21.8M vs. Banxico >20M.

## Lo que este acto deliberadamente NO hace

No re-especifica la condición A de R3.4 (eso es el sucesor, con la FP-104 ya reformulada por `SELLA-AGO24`). No toca `milpa/refutations.yaml` ni `milpa/tramite.yaml` (razón: sin red no se puede resolver la discrepancia CoDi ya anotada — T5). No abre red. No mide nada — todo lo emitido es vocabulario y validación de forma, cero adjudicación de casos.

## Cobertura retroactiva

`emisor.py` nació el 21/ago (`ADR-138`/`ADR-139`); todo lo que este acto extiende es posterior a las tablas que lo gobiernan — sin brecha.
