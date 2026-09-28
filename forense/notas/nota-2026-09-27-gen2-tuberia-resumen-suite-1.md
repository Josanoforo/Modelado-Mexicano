# Nota de cierre · ACTO GEN2-TUBERIA-RESUMEN-SUITE-1 · ADR-260927-GEN2-TUBERIA-RESUMEN-SUITE-1-6127-01

Encargo: `forense/encargos/2026-09-27-GEN2-TUBERIA-RESUMEN-SUITE-1.md` (A.3; sha256 del adjunto `bcf35b22…d462`, verificado contra el `.sha256` recibido; 0-bis `6127c7bb`). SHA de redacción `5f708a47`; base real `9536e5e2` (origin/main al abrir, 0 detrás). ENTORNO: NUBE (hook), cero microdato.
Contador: cero mediciones; no adopta; `celdas_validadas: 219 → 219 (Δ0) @ 6127c7bb`. Ningún valor de `status` cambia; se añade una clave.

## P3 · marca de definición del legacy en `status` — HECHO
- `tools/corrida0.py`: `_legacy_definicion_desde()` deriva el commit por pickaxe (`git log -S`) sobre las dos líneas que definen hoy el contador (B3 de FIRMAS-16: `TIPOS_FUERA_DEL_CONTADOR]`, `07e97205`, 25/sep; H1–H3 de FIRMAS-18: `_es_historico_sin_relevo(u, _marcados_h)`, `e907aa0a`, 26/sep) y publica el más reciente. Un clon superficial cuyo borde "introduce" la línea da `NO-VERIFICABLE-CLON-SUPERFICIAL` en vez de adivinar (D-23).
- [EJECUTADO] `python3 tools/corrida0.py status | grep -c "legacy.*definicion_desde"` → `1`; valor `dependencias_numericas_legacy_definicion_desde=e907aa0`; `git merge-base --is-ancestor e907aa0a origin/main` → sí. Sin cambio: `dependencias_numericas_legacy_activas=67`, `…__corte_pi=6`, `…__historico_sin_relevo=54`, `celdas_validadas_definicion_desde=38dd709`.

## P2 · T03 ve `.claude/` — HECHO
- `tests/check.py` T03: `.claude/**` entra explícito al índice de existentes (no a los documentos escaneados: la suite no cambia qué verifica). Se evitó `glob(include_hidden=True)` (3.11+). Salen de `HISTORICOS` `tramite.md` y `revisa.md`, que sólo estaban por esa limitación.
- [EJECUTADO] T03 antes/después sobre el mismo árbol: 304 → 250 avisos; 54 resueltos (todos citas de `acto.md`), 0 nuevos. `tramite.md` y `revisa.md` no aparecen como colgantes sin `HISTORICOS`. (Las «19 de 117» del tablero son [REPORTADO] de otro corte; no se copian.)

## P1 · resumen de la suite, derivado y publicado — CÓDIGO HECHO; primera publicación pendiente del merge
- `tools/resumen_suite.py` (nuevo): lee el log de `tests/check.py --baseline` y escribe `data/derivados/suite-resumen.tsv` (`clave<TAB>valor`: commit, fecha, run_id, resultado VERDE/ROJO/NO-TERMINÓ, fail_total, warn_total, fail_nuevos, warn_nuevos, duracion_s, y una fila por `fail_nuevo`/`warn_nuevo`).
- `verify.yml`, job `suite`: el mismo comando con `tee` al log (la suite corre UNA vez); paso `resumen` sólo en `schedule`/`workflow_dispatch` sobre main que expone el TSV como output del job (sin actions de marketplace).
- Job nuevo `resumen-suite` (needs `suite`, sólo main + nocturno/manual): publica el archivo en `derivados/suite-<run_id>` con commit `[deriva] …` (auto-merge por prefijo, R(a)/D4-A), abre PR, cierra sólo los `derivados/suite-*` anteriores superados, despacha verify en la rama. **Decisión declarada (§5):** job aparte y no dentro de `derivados`: no suma al presupuesto de 900 s de trozos, no toca `derivados/auto-*` ni su bucle, y no depende de que el drenaje termine.
- `tools/tablero_programa.py`: la clave `suite` lee el resumen (`resumen_suite.linea`), con commit y fecha; más de 2 días → «suite: sin corrida nocturna desde …».
- Adyacente declarado (≤ 10 líneas, D-21): `tests/test_check_parallel.py` añade `resumen-suite` a la excepción nombrada `fuera_del_gate` (publica, no verifica; mismo trato que `derivados`), y asegura que sólo corre sobre main. Sin esto el test del gate exigía meterlo en `needs` de `check`, que el perímetro veda.
- A.17: CI-TIEMPO-2 post-merge — el canal sigue vivo (`derivados/auto-36338353579` al cerrar); no se tocó el job `derivados`.

## Test propio
`tests/test_resumen_suite.py` (huérfano, invocador `script`): 6/6 OK — VERDE/ROJO/NO-TERMINÓ, ida y vuelta del TSV, aviso de viejo, T03 sin colgantes bajo `.claude/`, clave P3 con forma de commit o NO-VERIFICABLE.
