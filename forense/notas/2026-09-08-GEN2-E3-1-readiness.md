# `GEN2-E3-1 · READINESS-DEL-RUNNER` — nota de cierre

**Acto:** `ACTO GEN2-E3-1 · READINESS-DEL-RUNNER`, 8/sep/2026, entorno NUBE
(fixtures y smokes, sin corpus). Encargo archivado:
`forense/encargos/cola/2026-09-07-GEN2-E3-1-ENDURECE-CALC.md` (formato
corto de despacho, ESTADO/BITACORA gestionados en ese mismo archivo — el
0-bis A.3 de `/acto` se omite porque el archivo ya vivía en `cola/` antes de
que esta sesión lo tomara).

## 1 · A.8 — los ocho defectos confirmados antes de tocar nada

Contra `tools/corrida0.py` en `main` (verificado 7/sep, re-confirmado al
arrancar esta sesión):

1. `_inputs_para_medidor` construía `ruta_absoluta` solo para `origen:
   repo`; `medir(inputs, dict(spec["parametros"]))` — `seed`/`universo`/
   `filtros`/`ponderador`/`estimando` no viajaban. **Confirmado.**
2. Sin cotejo `outputs` declarados == devueltos. **Confirmado** — `run`
   escribía lo que `medir()` devolviera, sin comparar contra
   `spec["resultados"]`.
3. `seed None` → bloqueo, sin forma de declarar `aplica: false`.
   **Confirmado** — `spec.get("seed") is None` era la única condición.
4. `_firma_entorno()` llamada dos veces dentro de la construcción de
   `ejecucion.json`. **Confirmado**, línea por línea.
5. `preflight` distinguía AUSENTE/COINCIDE pero no devolvía `sha`/`ruta`/
   `tamaño` por id a `run` para los inputs `origen: manifiesto` — sólo para
   `origen: repo`. **Confirmado.**
6. `run` sobrescribía un CALC sellado por otro código con un **AVISO**, no
   un bloqueo (`:1170` de la versión auditada). **Confirmado.**
7. `sello.json` cubría solo `ejecucion.json`/`resultados.json`, nunca
   `spec.yaml`. **Confirmado.**
8. `verify` mezclaba en una sola lista de `salvedades` razones de dos ejes
   distintos (identidad de código/commit y cambio de inputs). **Confirmado.**

Más lo que A.8 marcó como no verificable por lectura: si `run` sellaba tras
un fallo del medidor. Se confirmó **empíricamente falso** al leer el código:
`run` escribía `ejecucion.json`/`resultados.json`/`sello.json` sin mirar
`exit_code` — el caso de prueba `T-RUN-FALLO-NO-SELLA` (P6) es justo lo que
A.8 pedía para dejar de depender de la lectura.

`.github/workflows/verify.yml:17-19` afirmaba "nadie importa yaml" siendo
que `tools/corrida0.py` sí lo hace desde `ACTO GEN2-E3`; confirmado y
corregido (§4).

## 2 · Compuerta — cumplida por producto

`COMPUERTA: git show origin/main:data/corrida0/decisiones.tsv | grep -c
FP-339` → `7` (≥ 1). Verificado contra `origin/main` real al arrancar esta
sesión (commit `b4a1cf0`), antes de tocar nada.

## 3 · Lo que se construyó (P1-P6)

- **P1.** `resolver_payload(payload_id)` extraído de
  `tests/manifiesto.py::cmd_verifica` a `tests/payload_resolver.py` (módulo
  nuevo, compartido) — mismo patrón de import directo que `tests/corpus.py`
  ya usaba. Cinco estados cerrados. `tools/corrida0.py` deja de invocar
  `tests/manifiesto.py --verifica` por subproceso: `preflight`,
  `_inputs_para_medidor` y `verify` comparten la misma resolución.
- **P2.** `contrato_ejecutable(spec)` normaliza `{variables, universo,
  filtros, ponderador, transformacion, estimando, parametros, seed}`; el
  medidor recibe `medir(inputs, contrato)`, nunca abre `spec.yaml`. `seed`
  acepta `{aplica: false}` (declaración válida) o `{aplica: true, valor,
  rng}`, retrocompatible con un valor suelto (`CALC-SMOKE-0001`, intacto).
  `tools/entorno.py` gana `dependencias_materiales_de(nombres)`.
- **P3.** `_valida_outputs` exige exactitud de conjunto, `tipo` +
  `unidad`, finitud, rango de `proporcion`, y `null` solo con
  `permite_no_estimable`. `run` ya no escribe nada si el medidor falla o
  los outputs no validan.
- **P4.** `run` verifica inmutabilidad ANTES de llamar a `preflight`: un
  CALC sellado y válido responde `CALC-INMUTABLE · YA-SELLADO`, exit ≠ 0,
  bytes intactos — sin `--force`/`--overwrite`/`--replace`. `sello.json`
  cubre `spec.yaml` + `ejecucion.json` + `resultados.json` + el medidor si
  vive dentro del CALC. `ejecucion.json` gana `spec_yaml_sha256` y
  `spec_md_sha256`.
- **P5.** `verify` en cinco pasos ordenados y dos ejes: sello completo del
  recibo (sidecar + cada archivo que cubre) · `spec_yaml_sha256` · inputs
  re-resueltos con P1 · `CONTEXTO ∈ {IDENTICO, DISTINTO, NO-VERIFICABLE}` ·
  `RESULTADO ∈ {REPRODUCE, NO-REPRODUCE, NO-EJECUTABLE}`. `REPRODUCE` solo
  con `IDENTICO`; `REPLICA-RESULTADO · CONTEXTO-DISTINTO` si los RESULT
  coinciden con contexto distinto; `NO-VERIFICABLE` no se degrada. `verify`
  no escribe ningún artefacto canónico.
- **P6.** Catorce tests en `tests/test_corrida0.py` (§5). `CALC-SMOKE-0002`
  nace (`repite_de: CALC-SMOKE-0001`, que queda intacto). CI:
  `.github/workflows/verify.yml` corrige el comentario obsoleto y agrega
  `pip install -r requirements.txt` explícito.

## 4 · Validación real contra `CALC-SMOKE-0001` (sin tocar sus archivos)

`python3 tools/corrida0.py run CALC-SMOKE-0001` → `CALC-INMUTABLE ·
YA-SELLADO`, exit 1, bytes intactos (verificado byte a byte). `python3
tools/corrida0.py verify CALC-SMOKE-0001` → `REPLICA-RESULTADO ·
CONTEXTO-DISTINTO` (`RESULTADO=REPRODUCE` exacto en los nueve RESULT;
`CONTEXTO=DISTINTO` porque su `ejecucion.json`, sellado antes de este acto,
no trae `spec_yaml_sha256`/`dependencias_materiales_calc` y el commit
avanzó desde entonces) — el veredicto correcto para una corrida sellada bajo
el esquema anterior, no un defecto.

## 5 · `CALC-SMOKE-0002` — compuerta de salida

`python3 tools/corrida0.py preflight CALC-SMOKE-0002` → VERDE. `run` →
sellado (`sello` cubre `spec.yaml`, `ejecucion.json`, `resultados.json`,
`medidor.py`). `verify` → **`REPRODUCE` (`CONTEXTO=IDENTICO` ·
`RESULTADO=REPRODUCE`)**, con los mismos nueve valores que
`CALC-SMOKE-0001` selló bajo el runner anterior — confirma que el runner
endurecido reproduce exactamente el mismo cálculo. Un `run` posterior sobre
el mismo CALC ya da `CALC-INMUTABLE · YA-SELLADO`, verificado.

`python3 tests/test_corrida0.py` → 38 casos, 0 FALLOS (24 preexistentes +
los catorce de P6). `python3 tests/check.py --baseline` → VERDE.

**Los seis checks del GO, todos cumplidos:** `PAYLOAD-RESUELTO` ·
`CONTRATO-EJECUTABLE-COMPLETO` · `OUTPUTS-VALIDADOS` · `CALC-INMUTABLE` ·
`SELLO-COMPLETO` · `VERIFY-CONTEXTO+RESULTADO`.

## 6 · Decisiones de mesa que este ADR propaga

**D11.** `milpa/src/motor.py`, `theta.py`, `pi.py`, `celdas.py`,
`momentos.py` son scaffold/calibración histórica, **no** la definición de
«motor limpio GEN2»; el sistema numérico activo es
`tramite.yaml + emisor + matriz B`. Ningún gate de `GEN2-E5`/`GEN2-E6` los
usa. Este acto no tocó ninguno de esos cinco archivos (fuera de perímetro),
y no hacía falta: la decisión es declarativa, no un cambio de código.

**D12.** La readiness del marcador (wrapper M por celda del marco vigente;
R por `payload_id` exacto; corredor L sucesor de los CLI actuales; agregado
sucesor que consuma `RESULT-R/M/L`) se atiende en `ACTO GEN2-E7`, antes de
C0-D — no en `ACTO GEN2-E5`. Este acto no implementó nada de eso (fuera de
perímetro, declarado desde el propio encargo).

## 7 · `NO-CORRIDO / RESERVAS` heredado — `NC-0003`

`ACTO GEN2-T8` (8/sep/2026) dejó `NC-0003` ABIERTA con sucesor `E3.1`: de
los cinco límites que la nota de cierre de `ACTO GEN2-E3`
(`forense/notas/2026-09-07-GEN2-E3-nucleo-corrida0.md` §7) declaraba,
cuatro los cierra este acto y uno se conserva por diseño:

1. *"El test no cubre el smoke de punta a punta."* **Cerrado** —
   `CALC-SMOKE-0002` corre `preflight`→`run`→`verify` de punta a punta en
   caja real (§5), fuera de `tests/check.py` (que sigue sin poder — el
   árbol de CI está sucio durante la corrida, mismo límite que ya
   declaraba `t32_corrida0`).
2. *"`inputs` del smoke no es exhaustivo, y lo dice."* **Cerrado** —
   `CALC-SMOKE-0002/spec.md` §5 hereda la misma declaración explícita, y
   además ahora declara `dependencias_materiales: []` con su propia
   verificación (§4 de esa spec).
3. *"`verify` no re-verifica los inputs de manifiesto."* **Cerrado** — P5
   paso (3) re-resuelve CADA input `origen: manifiesto` con
   `resolver_payload` (P1) y lo compara contra el SHA sellado; ya no se
   limita a citar que `preflight` ya lo hizo.
4. *"El guard de duplicado no puede consultar PRs por sí mismo."*
   **Cerrado** para el perímetro de este acto — el ARRANQUE de esta sesión
   corrió las tres comprobaciones del paso `0.c` de `/acto` (rama remota,
   worktree, PR abierto vía el tool de GitHub disponible) y no encontró
   duplicado; el límite estructural (que `git`/`gh` no sean intercambiables
   en toda sesión) sigue siendo cierto, pero no bloqueó esta ejecución.
5. *"`limpia_arbol` no hace `fetch`."* **Se conserva, válido por diseño**
   — confirmado contra el propio docstring de `tools/limpia_arbol.py`: es
   deliberado (el ARRANQUE de `/acto` ya corre `git fetch --prune` antes;
   un fetch escondido haría que el conteo dependiera de cuándo se llamó al
   script). No es deuda de `E3.1` — la fila se cierra igual, con esta razón
   explícita, no como "resuelto".

`forense/no-corrido.tsv`: `NC-0003` pasa a `estado=CERRADA`,
`cerrado_por=<PR de este acto>`, `fecha_cierre=8/sep/2026` — `id`/`fecha`/
`acto`/`pr`/`pieza` sin tocar (append-only salvo estado y cierre, tal como
manda A.14).

## 8 · Sucesores

`ACTO GEN2-E5-0 · SPECS-EJECUTABLES` (gateado a este acto fusionado) resuelve
códigos/ponderadores exactos y congela los `spec.yaml` de `CALC-0001/0002/
0003`. `ACTO GEN2-E7` atiende D12 (readiness del marcador). Ninguno de los
dos se adelantó aquí — perímetro disjunto, declarado desde el propio
encargo.
