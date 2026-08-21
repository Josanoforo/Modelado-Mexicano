# Nota de cierre — `ACTO SELLA-M5-V2`, 20/ago/2026

**Entorno:** NUBE, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`, repo-only, sin sonda de red de datos. `data/raw` no se usó (este acto no la toca).
**Dueña única:** `pgrep -af claude` al arrancar → un solo proceso claude (esta sesión). Sin concurrencia detectada durante la ejecución.
**SHA de arranque:** `8b73aee` (`git log -1 --format="%h %s"`), sin drift al escribir.

## Compuerta de arranque

El lanzamiento inicial llegó **sin** el adjunto `ADV1-M5-v2-propuesta-2026-08-20.md`. Conforme a instrucción explícita (precedente `ADR-124`), el acto **PARÓ** y pidió el archivo en vez de reconstruirlo. Verificación en ese momento: `pgrep -af claude` (dueña única, un solo proceso) y `find / -iname "*ADV1-M5-v2-propuesta*"` (sin resultados). El adjunto llegó en el turno siguiente, vía ruta `/root/.claude/uploads/…/a4b2533b-ADV1M5v2propuesta20260820.md`. Este paro es correcto y no cuenta como sesión perdida.

## Verificación de existencia (A.8)

- `forense/escala-cinco-casillas-piloto-v1_0.md`: existe, 33 líneas, `NO SELLADO — COMPUERTA B-bis ACTIVADA` — confirmado leyendo el archivo completo, no solo `wc -l`.
- `ADV1-M5 v2`: NO-ENCONTRADO antes de este acto — `forense/prereg-duelo-v2/mesa-pendientes.md` §2 con las tres opciones abiertas, ninguna elegida (confirmado leyendo el archivo).
- `forense/prereg-duelo-v2/scoring-adv1-m3.py:24-26`: confirmado — cabecera declara que el script calcula las cinco condiciones por separado y deja la composición pendiente de mesa.
- Corrección de ruta: el encargo asume `forense/adv-duelo/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md`; el archivo real vive en `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` (nunca movido a `forense/adv-duelo/`, a diferencia de los cuatro informes adversariales). Usado el path real en todas las citas.
- ADR máximo re-derivado: `grep -oE 'ADR-[0-9]+' canon/gobernanza-v1_15.md | sort -t- -k2 -n -u | tail -1` → `135`, coincide con lo declarado.
- FP máximo y estados re-derivados: `awk -F'\t' 'NR>1{print $6}' forense/firmas-pendientes.tsv | sort | uniq -c` → `10 ABIERTA · 16 CERRADA · 1 CERRADA POR PREMISA REFUTADA · 68 FIRMADA` (95 filas), y `cut -f1 … | grep -oE 'FP-[0-9]+' … | sort -n | tail -1` → `95`. Coincide con lo declarado.
- Cobertura retroactiva: sin brecha — careo y escala son del 20/ago, tablero es de agosto.

## Tabla T1–T5

| Tarea | Entregable | `sha256` |
|---|---|---|
| T1 | `forense/adv-duelo/ADV1-M5-v2-propuesta-2026-08-20.md` (adjunto verbatim + cabecera de procedencia; `diff` de cuerpo contra el adjunto original: vacío, verificado) | `2aa0fa036f481024f9a36466cac0de33e5b9443f636bb3adb773c07ad6871ff0` |
| T2 | `forense/escala-cinco-casillas-piloto-v2_0.md` (nueva) + `forense/escala-cinco-casillas-piloto-v1_0.md` (banner de una línea, cuerpo intacto) | `v2_0`: `4ca179d9df34d1169b40ca45bbafe743517d252aa2cdc6ef2b080921eef419ad` · `v1_0`: `5645f7502212ae5b358e76d92cc4d5de1ea5c87452371a7de2cfc5bc54c5faea` |
| T3 | `canon/gobernanza-v1_15.md` `ADR-136` (a)-(f) | — (ver ADR en el archivo) |
| T4 | `forense/firmas-pendientes.tsv` filas `FP-96` (FIRMADA), `FP-97` (ABIERTA), `FP-98` (ABIERTA) | — |
| T5 | `forense/hallazgos.md`, dos líneas nuevas (solapamiento de ejes; `E` sin casilla) | — |

**Adjunto original:** `sha256` `f4d8ad2f282fb0c4f82cc6803a817342acd0fbbd8f539a4a6d84981fc1a536cf`, párrafo fuente `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:42`.

## Perímetro

Tocado: `forense/adv-duelo/`, `forense/escala-cinco-casillas-piloto-{v1_0,v2_0}.md`, `canon/gobernanza-v1_15.md`, `forense/firmas-pendientes.tsv`, `forense/hallazgos.md`, `forense/encargos/`, esta nota. No tocado: `milpa/`, `data/`, `corpus/`, `tests/` (incluido `scoring-adv1-m3.py`, sin editar), `forense/marco-candidatas-piloto-v1_0.tsv`, `forense/prereg-duelo-v2/` (solo lectura), el párrafo original del careo.

## Contador

Medición sobre México movida por este acto: **0** (dicho, v2.3). Lo que este acto compra es el desbloqueo de `D-ii`.

## Línea base

`python3 tests/check.py --baseline` (corrida final, tras converger `T15`/`T16`/`T25`/`T03` que este acto disparó y corrigió en el terreno):

```
21 FAIL · 138 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado e24d033ed3c095f1e81c2fbb8248f108e9d3ef65)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

Recifrado `135→138` WARN (`FP-97`/`FP-98` nuevas `ABIERTA`, `T22`), FAIL sin cambio en `21` (núcleo sin `T16`, punto fijo). `gobernanza`/`estado` recifrados `135→136` ADR (`T15`). `sha256` de este acto quedan en la tabla T1-T5 arriba. Sin `--freeze` en ningún punto.
