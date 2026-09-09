# Cierre · ACTO GEN2-MOTOR-SEMANTICA

Encargo archivado en
`forense/encargos/2026-09-09-GEN2-MOTOR-SEMANTICA-propagacion.md` (A.3,
verbatim). Base `origin/main = cc1cfe2c`, sin diferencia al arranque
(`git rev-list --count HEAD..origin/main` → `0`). Árbol limpio, sin
duplicado (rótulo no encontrado en ramas remotas, worktrees ni PR abiertos).
COMPUERTA: `ninguna` (declarada en el encargo) — no dispara verificación.
No toca microdato ni red: se saltó la sonda de red (A.13, este acto examina
0 archivos de corpus).

## §11 · A.8 — `tools/ya_medido.py tramite.mordida.con_registro`

Corrido antes de escribir la enmienda de D3 (P2), porque el encargo cita
esa regla por `id` en su cuerpo. Salida cruda:

```
=== ya_medido: tramite.mordida.con_registro ===
  resuelto por canon: tramite.mordida.con_registro -> R3.2 (canon/modelo-decision-v4_0.md §3, registro congelado + tag **id:**)
  términos de búsqueda (match exacto): tramite.mordida.con_registro, R3.2

-- milpa/tramite.yaml --
  milpa/tramite.yaml:40  situacion=realiza_tramite_gobierno tier=FUERTE p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite.yaml:122  situacion=realiza_tramite_gobierno tier=FUERTE p=0.88
      id: tramite.mordida.con_registro

-- milpa/tramite-ola5-propuesta-v0.yaml --
  milpa/tramite-ola5-propuesta-v0.yaml:131  situacion=realiza_tramite_gobierno tier=SELLADA p=0.62
      id: tramite.mordida.discrecional
  milpa/tramite-ola5-propuesta-v0.yaml:462  situacion=realiza_tramite_gobierno tier=PENDIENTE-DE-MESA). p=0.085118
      id: tramite.mordida.discrecional_encig_serie
  milpa/tramite-ola5-propuesta-v0.yaml:543  situacion=realiza_tramite_gobierno tier=SELLADA veredicto=veredicto=digital: p=0.027358
      id: tramite.mordida.con_registro_encig2025
  milpa/tramite-ola5-propuesta-v0.yaml:903  situacion=PENDIENTE-DE-MESA tier=SELLADA p=0.642080
      id: dinero.ahorro.tiene_ahorros_enif2024

-- canon/modelo-decision-v4_0.md §7 --
  canon/modelo-decision-v4_0.md:704  tier=[MEDIA]
  canon/modelo-decision-v4_0.md:743  tier=[FUERTE]
      | `R3.2` | L233 | Digitalización/testigos/registrable → baja la mordida | `[FUERTE]` | Sí |

-- forense/notas/*-L*-*.md --
  (cinco archivos, censados; ver `tools/ya_medido.py` para el listado completo)

========================================
NUNCA-MEDIDA
```

**Veredicto = FALSO NEGATIVO conocido** (`ADR-438`, reabierto por `NC-0129`
del lote ENIF): la regla `tramite.mordida.con_registro` SÍ está medida y
sellada en `milpa/tramite.yaml:122` (`tier=FUERTE`, `p=0.88 ASIGNADO` +
enmiendas `MEDIDO` `paga_mordida_encig2025_presencial{,_r2}` /
`_digital{,_r2}`), y la propia sección de LISTADO de la herramienta la
ubica ahí. El defecto es de `_tiene_veredicto_real()` (no reconoce
`MEDIDO`, solo veredictos de falsación `R` o campo `veredicto:`), no de
este acto — que además no clasifica, pre-registra, carga ni sella nada: la
cita en P2 es para ratificar el método de IC que la propia spec sellada de
esta regla (vía `ENCIG-MORDIDA-spec-v1_0.md`) ya declaraba en §3.7.

## §12 · `tests/check.py --baseline`

Corrido en verde tras las tres piezas (P0/P1/P2, cierres P3, y la exención
de `_T_YAMEDIDO_ARCHIVOS_CONOCIDOS` de arriba). Salida completa en el commit
de cascada.

## §13 · Fix de CI post-PR (defecto real, no flake)

`PR #670`, CI en rojo: `tests/test_emite_m_calibracion.py::test_regresion_p2_pasa`
fallaba (regresión P2 de `M-TRA-M-01`/`M-TRA-M-02`, ver §5/§25.5 del acto
`MAESTRA38-M13`). Causa: `cita_p`/`cita_ola_calibracion` citan una línea
de `milpa/tramite.yaml` **por texto exacto** (`tools/emite_m.py::_primera_linea`
devuelve la línea completa, comentario incluido); este acto había anotado
`# SEMANTICA (D4, NC-0113)` **en la misma línea** que citan `M-TRA-M-01`,
`M-TRA-M-02`, `M-TRA-M-03`, `M-TRA-M-05`, `M-TRA-M-07` (línea `paga_mordida,
p: 0.62, ASIGNADO`) y `M-TRA-M-02__v1_3`/`M-TRA-M-03__v1_3`/`M-TRA-M-07__v1_3`
(línea `paga_mordida_encig2025, p: 0.085118`) — el texto citado ya no
coincidía con el archivado en esos `M-*.json`. Corregido moviendo las dos
anotaciones `SEMANTICA` a una línea de comentario propia, inmediatamente
antes de la línea citada (no matchea el regex `conducta:\s*<nombre>\b`,
así que no se convierte en el nuevo "primera línea" del bloque). Verificado:
censo de las 23 `cita_p`/`cita_ola_calibracion` no vacías en
`forense/prereg-duelo-v2/corridas-M/*.json` — ninguna otra cae sobre una
línea anotada por este acto. `tests/test_emite_m_calibracion.py` (16/16 OK),
`tests/check.py --baseline` (línea base VERDE) y `tests/test_svystat.py` /
`tests/test_scoring_adv1_m3.py` corridos en verde tras el fix.
