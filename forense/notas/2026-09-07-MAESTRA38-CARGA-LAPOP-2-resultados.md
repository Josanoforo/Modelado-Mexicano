# ACTO MAESTRA38-CARGA-LAPOP-2 · PROPAGA-FP316-FP315-CORREGIDO — resultados

Encargo: `forense/encargos/2026-09-07-MAESTRA38-CARGA-LAPOP-2.md` (0-bis). Spec verbatim §1–§3: `forense/notas/2026-09-07-MAESTRA38-CARGA-LAPOP-2-spec.md`. COMPUERTA (`PR de ADR-358 fusionado`) verificada por producto:

```
$ git merge-base --is-ancestor 4501c636d2a27042965b14cef2024e3ef106286e origin/main && echo "ancestor"
ancestor
$ git log --oneline -1 origin/main
28c3965 Merge pull request #566 from Josanoforo/claude/r7-6-split-observability-proximity-246grd
```

Cumplida.

## A.8 al arrancar

```
$ grep -n -A12 "id: civico.voto.clientelar_si_observable_lapop2019\|id: civico.voto.agencia_lapop2023\|id: civico.voto.agencia_con_secreto_encuci2020\|id: civico.protesta.agravio_urbano_multiola\|id: civico.protesta.agravio_urbano_lapop2019\|id: comunicacion.inseguridad.ver_oir_callar_lapop2004" milpa/tramite-ola5-propuesta-v0.yaml | grep -E "id:|situacion:|tier:"
2284:  - id: civico.voto.agencia_lapop2023
2287-    situacion: PENDIENTE-DE-MESA
2288-    tier: PENDIENTE-DE-MESA
2356:  - id: civico.protesta.agravio_urbano_lapop2019
2359-    situacion: SELLADA-SIN-CARGA  # D2-e ...
2361-    tier: MEDIA  # D2-e
2555:  - id: civico.voto.agencia_con_secreto_encuci2020
2558-    situacion: PENDIENTE-DE-MESA
2559-    tier: PENDIENTE-DE-MESA
3383:  - id: civico.voto.clientelar_si_observable_lapop2019
3393-    situacion: PENDIENTE-DE-MESA  # ...
3394-    tier: PENDIENTE-DE-MESA
3449:  - id: civico.protesta.agravio_urbano_multiola
3460-    situacion: PENDIENTE-DE-MESA  # ...
3461-    tier: PENDIENTE-DE-MESA
3542:  - id: comunicacion.inseguridad.ver_oir_callar_lapop2004
3551-    situacion: PENDIENTE-DE-MESA  # ...
3552-    tier: PENDIENTE-DE-MESA
```

Coincide exactamente con lo esperado por el encargo: cinco `PENDIENTE-DE-MESA` y `_lapop2019` `SELLADA-SIN-CARGA`. Sin desajuste — se procede.

## Tiers en canon

```
$ grep -n "^| \`R7.3\`\|^| \`R7.6\`\|^| \`R7.4\`\|^| \`R10.3\`" canon/modelo-decision-v4_0.md
761:| `R7.3` | L267 | ... | `[FUERTE]` | Sí |
762:| `R7.6` | L268 | ... | `[MEDIA]` | No |
766:| `R7.4` | L272 | ... | `[MEDIA-FUERTE]` | Sí |
778:| `R10.3` | L299 | ... | `[FUERTE]` | Sí |
```

`R7.3`/`R7.6` `[FUERTE]`/`[MEDIA]` en la tabla histórica; el tier que el motor consumiría, tras `D2-f`, es `[MEDIA]` para ambas (`R7.3` degradada por `D2-f`; `R7.6` nunca fue `[FUERTE]`). Coincide con lo declarado por el encargo.

## D2-f como plantilla

```
$ grep -n "Enmienda D2-f" canon/modelo-decision-v4_0.md
781:**Enmienda D2-f (append, 0 líneas borradas) · firma de mesa 3/sep/2026...
```

## `validador_registro_ids.py` antes y después — idéntico

```
$ python3 tests/validador_registro_ids.py   # ANTES de las ediciones
OK — canon/modelo-decision-v4_0.md
  49 reglas · 27 en perímetro · 49 IDs verificados, todos con ancla y tier consistentes

$ python3 tests/validador_registro_ids.py   # DESPUÉS de D2-g/D2-h y las 5 ediciones de propuesta
OK — canon/modelo-decision-v4_0.md
  49 reglas · 27 en perímetro · 49 IDs verificados, todos con ancla y tier consistentes
```

Sin cambio: 49 IDs, 27 en perímetro. Este acto no toca `§3.7`, la tabla de `§7` ni `REGISTRO`.

## `milpa/tramite.yaml` — intacto

```
$ grep -c "^  - id:" milpa/tramite.yaml
20
```

20 antes, 20 después (no tocado por este acto).

## `ya_medido.py` sobre las cuatro reglas — cita ADR previos, no reabre

`R7.3`, `R7.6`, `R7.4`, `R10.3` devuelven `MEDIDA-EN:` citando `2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md`, `L2`/`L4`/`L5`/`L9`/`L11`/`L18`, `S2`/`S4`/`S5`, `canon§7`, `tramite-ola5-propuesta-v0.yaml` — ninguna reabre un veredicto ya archivado.

## Ediciones hechas

1. **`canon/modelo-decision-v4_0.md §7`**: enmiendas `D2-g` (R7.6 por lectura, brazo observabilidad/proximidad) y `D2-h` (cláusula de movimiento de R10.3), append inmediatamente después de `D2-f`. Ninguna fila de la tabla de IDs editada, ningún bullet de `§3.7` añadido.
2. **`milpa/tramite-ola5-propuesta-v0.yaml`**: cinco entradas — `civico.voto.agencia_lapop2023`, `civico.voto.agencia_con_secreto_encuci2020`, `civico.voto.clientelar_si_observable_lapop2019` → `SELLADA-SIN-CARGA` (heredan `[MEDIA]`); `civico.protesta.agravio_urbano_multiola` → `ACOTADA-CON-RESERVA` (hereda `[MEDIA-FUERTE]`); `comunicacion.inseguridad.ver_oir_callar_lapop2004` → `SELLADA-SIN-CARGA` (hereda `[FUERTE]`). `civico.protesta.agravio_urbano_lapop2019` (D2-e) intacta.
3. **`forense/firmas-pendientes.tsv`**: `FP-315` → `FIRMADA`; `FP-316` → `FIRMADA`.
4. Cascada: `ADR-359` (principal) + `ADR-360` (inciso D2-g) + `ADR-361` (inciso D2-h); `canon/gobernanza-v1_15.md` cabecera 358→361 ADR; `canon/estado-programa-v1_12.md` L0 y línea de resumen 358→361; `canon/registro-rotulos.tsv` gana `MAESTRA38-N17`; `forense/hallazgos.md` con la regla candidata sobre costo de partición por ID vs. por lectura.

## Suite

```
$ python3 tests/check.py --baseline
...
3 FAIL · 172 WARN
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado accf688c6ad98f9b3264b4bf0343431d5649e666)
────────────────────────────────────────────────────────────────────────
```

Los 3 FAIL (T06, T08) son preexistentes, ya en `tests/baseline.json`, sin relación con este acto. `tests/check.py` gana una entrada en `_T_YAMEDIDO_ARCHIVOS_CONOCIDOS` para el propio encargo verbatim de este acto (cita `civico.protesta.agravio_urbano_lapop2019` solo para declarar que no se toca — no es clasificación/carga/sello nuevo).
