# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_2` · los dos CALC del piloto 3 pasan el preflight que sella, sin tocar una línea del código ni de la spec humana

**PREFLIGHT-PASÓ:** _(se llena en §3, después de correrlo; la lista esperada de §2 va antes)_

**21/sep/2026 (20/sep 22:20 CST) · CAJA (`ENTORNO-DERIVADO`: `corpus=SI(examinados=419)`, `raices=data_raw:SI descargas_mx:SI`, `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, python 3.14.4, numpy 2.3.5, pandas 2.3.3) · Opus 5 · rama `acto/gen2-celda-d-piloto-3-commit-1-v1_2`, worktree `/home/pc0/mm-piloto-3-v12`.**

**Base declarada:** `PR #941` **no estaba fusionado al abrir** → se arranca de su cabeza, como el encargo prevé. La cabeza ya no era `b1f1cb13`: antes de apilar, esta misma sesión fusionó `origin/main` (`887aecb6`, que trae `#939` con `ADR-577`) en `#941` y renumeró su ADR `577→578`; cabeza nueva `b6fc096e`. `FP-407` vive ahí (ABIERTA). Encargo archivado (A.3): `forense/encargos/2026-09-21-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_2.md` + sidecar `.sha256` (`6fe87bd8…`, `sha256sum -c` → OK), commit `a798f8b3`, rama empujada antes de cualquier paso sustantivo.

**Exposición de esta sesión (F3, `FP-407` a):** es la sesión que paró en `#941`. No tiene los diseños A/B ni el careo; de ENCIG 2025 sólo vio el `sha256` del preflight de `#941` y de los preflight de este acto. Por F3, **esta sesión no corre los COMMIT-2/3**.

---

## 1 · Arranque y §4 (búsqueda por objeto, con mi acceso)

- 0.a `HEAD..origin/main` = 0 tras el merge en `#941`. 0.b limpio. 0.c: `git ls-remote --heads origin | grep -i v1_2` → 0 ramas; `git worktree list` → 0 worktrees `v1_2`; `gh pr list --search v1_2` devolvió `#942` (`GEN2-RELEVO-TANDA-3`, coincidencia de texto, no del rótulo) → sin duplicado. 0.d como en `#941`.
- `data/raw` enlazada a `/home/pc0/mm-corpus/raw`; `raices.local.yaml` copiada. `tools/entorno.py`: `montado=SI`.
- **Objeto «`spec.yaml` del piloto 3 que pasa preflight»:** `git diff --stat origin/main origin/<rama> -- <los dos spec.yaml>` sobre **todas** las ramas remotas (≠ main) → 0 ramas con diferencia. Ninguna rama lo arregla. Ningún directorio `CALC-GOB-DIGITAL-EXE-*` tiene sello (E.3 no protege nada aquí).
- Premisas `[EJECUTADO]` de dirección, re-corridas aquí: huellas de los tres `resultados.json` sellados (`285eeb55…`, `b7d3dfe9…`, `be24d879…`) — idénticas a las que `#941` reportó y a las del encargo; `git show 826bf3a1:forense/firmas-pendientes.tsv` trae `FP-399 FIRMADA` y su `sha256` es `c79e37d7…`; el libro vivo hoy es `17b24afc…` (era `e0f1ec86…` en `04a2edeb` y `5df43a05…` en `b1f1cb13`: **tres huellas en dos días**, la premisa del cuarto defecto se sostiene). `medidor.py:103-111`: la guardia lee `ruta_absoluta` y sólo exige `estado = FIRMADA` de `FP-399`. `decisiones.tsv`: 63 filas `cuenta_gen2=SI`, **2** filas `CALC-GOB-DIGITAL-EXE-EMISIONES-0001` (F1-bis y F3, no `cuenta_gen2`), **0** para `-0002`/`ADJUDICACION-0001`.
- `dependencias_materiales` derivadas de los `import`: `medidor.py` → `numpy`, `pandas` (más stdlib `io`, `json`, `math`, `zipfile`, `pathlib`); `adjudicacion.py` → `numpy`, `pandas` (más stdlib `hashlib`, `importlib`, `json`, `math`, `pathlib`). Forma de la casa: `[numpy, pandas]` (39 specs).

## 2 · Lista esperada — escrita ANTES de correr los preflight (compuerta §8)

- `CALC-GOB-DIGITAL-EXE-EMISIONES-0002` → **`PRE-FLIGHT: VERDE`** (sin bloqueos; se admiten avisos, p. ej. `spec_md_no_esta_en_origin_main`, que no bloquean).
- `CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001` → **`PRE-FLIGHT: BLOQUEADO`** exactamente por estas cuatro entradas y ninguna otra:
  1. `input_repo_ausente=emisiones_resultados:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/resultados.json`
  2. `input_repo_no_commiteado=emisiones_resultados`
  3. `input_repo_ausente=emisiones_sello:data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/sello.json`
  4. `input_repo_no_commiteado=emisiones_sello`

Cualquier otra entrada en cualquiera de los dos → PARO (g), sin quinta llave.

## 3 · Salida cruda de los dos preflight

_(pegada tras correrlos)_
