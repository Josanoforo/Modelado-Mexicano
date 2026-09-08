# ACTO GEN2-T35-DISEÑO · LA SIRENA SOLO PARA CABLES CORTADOS

Nota de cierre. Encargo archivado verbatim en
`forense/encargos/2026-09-08-GEN2-T35-DISENO.md` (0-bis `bf4a3e9`). Implementa
`FP-360` (FIRMADA) sobre `ADR-416`.

## A.8 · hechos re-derivados contra el árbol de ejecución

Redactado contra `origin/main = 4f26fb92` (PR #638); verificado al arrancar
contra `origin/main` real = `51fec05` (PR #635 de por medio — cola de
adquisición, `manifiesto.yaml`, `hallazgos.md` — sin tocar el perímetro de
este acto).

```
$ python3 tests/check.py 2>&1 | tail -6
════════════════════════════════════════════════════════════════════════
  3 FAIL · 426 WARN
════════════════════════════════════════════════════════════════════════
```

Antes de P1: 3 FAIL legacy congelados (T06 ×2, T08 ×1) + 211 de T35, los
211 exclusivamente ramal (a) «activo GEN2 y sin consumidor» — verificado
contando por patrón antes de tocar el código:

```
$ python3 tests/check.py 2>&1 | grep -c "activo GEN2 y sin consumidor"
211
$ python3 tests/check.py 2>&1 | grep -E "\(b\)|\(c\)" | grep "T-REPRO"
(sin salida — cero (b)/(c))
```

`tests/check.py --baseline` antes de P1: **LÍNEA BASE ROJO** — 211 entradas
nuevas contra `tests/baseline.json` (`HEAD` congelado `dee5fc5`), exactamente
las 211 de T35 ramal (a).

## P1 · T35 cambia de semántica

En `tests/check.py::t35_repro`, la cola de la comprobación de `activos`
(`if usos_por_result.get(rid, 0) == 0`) deja de llamar `fail()` y en su
lugar se acumula en `sellada_sin_adoptar`. Después del bucle, por cada
entrada se deriva la antigüedad desde la fila del `CALC` (`spec_id`) en
`data/corrida0/decisiones.tsv` (columna `fecha`; `SIN-FECHA` si el `CALC`
no tiene fila) y se emite con `senal()` — el mismo mecanismo que usa `T22`
para sus WARN de vigía, excluido por diseño de la comparación de línea
base (`SENAL`, ver `tests/check.py:40-46` y `_baseline_compare`). El
agregado (`SELLADA-SIN-ADOPTAR: N · más vieja: X días`) se emite **antes**
que las N entradas individuales, para que quede en la vista previa de 3
líneas que el resumen de la suite imprime por test.

Los ramales (b) (`corrida0_resultado_id` no resuelve a ningún `RESULT`),
(d)/(e)/(f) (cadena incompleta o generación discordante) y el resto de
(a) (corrida inexistente, hashes/sello faltantes, sello que no coincide,
`spec.yaml` que no resuelve) **no se tocan**: siguen en `fail()`.

Salida real, hoy, contra el árbol de ejecución (`CALC-0001`, `CALC-0002`,
`CALC-0003-v2`, los tres con fila `cuenta_gen2=SI` en `decisiones.tsv`
fechada `2026-09-08` — la propia firma del contador, `ACTO
GEN2-FIRMA-CONTADOR`):

```
$ python3 tests/check.py --baseline 2>&1 | sed -n '/T-REPRO: 212/,+3p'
  · T-REPRO: 212
      SELLADA-SIN-ADOPTAR: 211 · más vieja: 0 días
      SELLADA-SIN-ADOPTAR RESULT-C1-POSEL-AMENAZA-DELTA: activo GEN2 y sin consumidor -- antigüedad 0 días
      SELLADA-SIN-ADOPTAR RESULT-C1-POSEL-AMENAZA-DESENLACE: activo GEN2 y sin consumidor -- antigüedad 0 días
```

`más vieja: 0 días` es correcto y esperado: las tres filas de
`decisiones.tsv` que cuentan estos `RESULT` como GEN2 se firmaron hoy
mismo (8/sep/2026, `ACTO GEN2-FIRMA-CONTADOR`). El número crecerá un día
por corrida, sin tocar código, hasta que mesa adopte por merge en
`C0-B`/`C0-D` — ese es el punto: la presión ahora es visible y envejece,
en vez de vivir en un `FAIL` binario indistinguible del cableado roto.

## P2 · los tres falsadores, con su salida

Tres casos nuevos en `tests/test_corrida0.py`
(`t_sellada_sin_adoptar_es_warn_no_fail`,
`t_sellada_sin_adoptar_no_tapa_cita_inexistente`,
`t_sellada_sin_adoptar_agregado_coincide`). Los tres pasan:

```
$ python3 tests/test_corrida0.py
tests/test_corrida0.py · 64 casos · 64 ok · 0 FALLOS
```

Salida cruda de cada caso, ejercido a mano contra `t35_repro` (los mismos
fixtures que usan los falsadores):

**(i) un RESULT sintético activo sin consumidor → WARN, no FAIL:**

```
=== (i) RESULT activo sin consumidor ===
FAILS: [('T-REPRO', '11.1 CALC-FIX-SSA: sin `input_sha256` efectivos')]
WARNS: [('T-REPRO', 'SELLADA-SIN-ADOPTAR: 1 · más vieja: SIN-FECHA'), ('T-REPRO', 'SELLADA-SIN-ADOPTAR RESULT-SSA: activo GEN2 y sin consumidor -- antigüedad SIN-FECHA')]
```

El único `FAIL` que sobrevive (`11.1 ... sin input_sha256 efectivos`) es
una comprobación de cadena-completa **distinta** (el fixture no declara
inputs) — no menciona `RESULT-SSA` ni "sin consumidor"; es exactamente el
tipo de `FAIL` de cableado que P1 declara intacto. `SIN-FECHA` es correcto:
`CALC-FIX-SSA` no tiene fila en el `decisiones.tsv` real (el fixture no lo
declara, y `_arbol_registro` no reapunta `C.DECISIONES`).

**(ii) una regla sintética citando `corrida0_resultado_id` inexistente →
FAIL:**

```
=== (ii) cita a corrida0_resultado_id inexistente ===
FAILS: [('T-REPRO', '`registro` no deriva: ParoRegistro: USO-A-RESULT-INEXISTENTE: /tmp/.../tramite.yaml:r.fantasma:c1 declara corrida0_resultado_id=RESULT-FANTASMA, que no existe')]
WARNS: []
```

`tools/corrida0.py::_filas_registro` para con `ParoRegistro` antes de que
`t35_repro` pueda derivar ninguna vista — sigue en `FAIL`, sin universo
para `SELLADA-SIN-ADOPTAR`. Cableado roto de verdad, tal como el encargo
exige.

**(iii) el conteo del agregado coincide con las entradas:**

```
=== (iii) agregado coincide con entradas ===
WARNS: [('T-REPRO', 'SELLADA-SIN-ADOPTAR: 2 · más vieja: SIN-FECHA'), ('T-REPRO', 'SELLADA-SIN-ADOPTAR RESULT-SSA1: activo GEN2 y sin consumidor -- antigüedad SIN-FECHA'), ('T-REPRO', 'SELLADA-SIN-ADOPTAR RESULT-SSA2: activo GEN2 y sin consumidor -- antigüedad SIN-FECHA')]
```

`N=2` en el agregado, 2 entradas individuales — coincide.

## P3 · el verde vuelve

```
$ python3 tests/check.py --baseline 2>&1 | tail -6
════════════════════════════════════════════════════════════════════════
  3 FAIL · 426 WARN
════════════════════════════════════════════════════════════════════════
────────────────────────────────────────────────────────────────────────
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado dee5fc544b4e6ff96d5506a1605546e1df6a68e3)
  (5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
────────────────────────────────────────────────────────────────────────
```

Los 3 `FAIL` legacy congelados (`T06` ×2, `T08` ×1) siguen igual. Las 211
entradas de T35 migran de `FAIL` a `WARN` de vigía — no desaparecen, y no
se congelan: `senal()` las excluye de la comparación de línea base por
diseño (mismo mecanismo que `T22`), así que `tests/baseline.json` no se
tocó y no corrió `--freeze`. Las "5 entradas de la línea base ya no
aparecen" son preexistentes a este acto (confirmado corriendo
`--baseline` sobre el `HEAD` anterior, `git stash` de por medio) — no las
introduce ni las explica este acto.

## Registro

`FP-360`: `ABIERTA` → `FIRMADA` (`forense/firmas-pendientes.tsv`), citando
la firma de mesa verbatim del encargo, `ADR-416`.

`NC-0053`: sigue `ABIERTA` (`forense/no-corrido.tsv`) — este acto no la
cierra, la adopción real (E.2, vía `C0-B`/`C0-D`) sigue siendo de mesa.
Línea añadida al campo `impacto`: la presión vive ahora en el `WARN` con
antigüedad, no en un rojo de línea base.

`forense/hallazgos.md`: una línea — los tres PR (`#636`, `#637`, `#638`)
que se fusionaron con `T35` en rojo, causa única (el mismo veredicto
`FAIL` cubría cableado roto y sellado-sin-adoptar), semántica corregida.

## Perímetro cumplido

`tests/check.py` (sólo `T35`) · `tests/test_corrida0.py` (falsadores de
`T35`) · `forense/firmas-pendientes.tsv` · `forense/no-corrido.tsv`
(línea en `NC-0053`, sin cerrarla) · `forense/hallazgos.md` (una línea) ·
esta nota · `canon/gobernanza-v1_15.md` (`ADR-416`) ·
`canon/estado-programa-v1_12.md` (§L0) · `canon/registro-rotulos.tsv`.
**No tocó** `tools/corrida0.py`, `data/corrida0/**`, `milpa/**` ni la
línea base congelada.

## Contador

Cero GEN2 — aparato declarado. No adopta ningún `RESULT`, no cierra
`NC-0053`, no congela la línea base, no toca los 3 `FAIL` legacy.
