# Nota de cierre · ACTO GEN2-MOTOR-DEUDA-LOTE-1 · 23/sep/2026

Ver `canon/gobernanza-v1_15.md`, entrada `ADR-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-01`, para el relato completo. Esta nota fija la evidencia cruda citada ahí.

## PARO-PREMISA en P1 — verificación de D7/FIRMAS-11

```
$ git merge-base --is-ancestor origin/acto/gen2-tramite-firmas-11 origin/main
$ echo $?
1
$ git show origin/main:forense/firmas-pendientes.tsv | grep -c FIRMAS-11
0
```

`D7` («A.», autoriza editar `motor.py:20`/`:129`) solo existe en `origin/acto/gen2-tramite-firmas-11` (PR #1049), no fusionada. `git show origin/acto/gen2-tramite-firmas-11:forense/encargos/2026-09-23-GEN2-TRAMITE-FIRMAS-11.md` confirma el texto verbatim citado por este encargo, pero es una lectura tipo (3) (§2 regla de oro): no cuenta como hecho hasta re-leerse en main. `NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-01` en `origin/main` sigue `ABIERTA` con la pregunta de mesa sin contestar.

## P2 — commit_declaracion ADR-68

```
$ git log --diff-filter=A --format="%H %ad" --date=short -- milpa/catalogo-momentos-v0_1.tsv | tail -1
e860e77fe3d6bb09daf414033b4cd06a7539acf9 2026-09-21
$ git log --diff-filter=A --format="%H %ad" --date=short -- milpa/src/motor.py | tail -1
e860e77fe3d6bb09daf414033b4cd06a7539acf9 2026-09-21
```

Mismo commit → dictamen `NO-PROCEDE-HISTÓRICO`. `tests/test_motor_holdout.py` editado (única edición de código de este acto): la aserción de `test_c_roles_sellados_antes_que_todo_resultado` se sustituyó por `saltar(...)` con la razón citada.

```
$ python3 tests/test_motor_holdout.py
  test_a2_firma_contra_el_commit_de_sello: ok
  test_a_conjunto_holdout_estable: ok
  test_b2_la_rebanada_completa_no_toca_holdout: ok
  test_b3_el_codigo_del_motor_no_llama_valor_de_en_holdout: ok
  test_b_ningun_valor_holdout_se_lee: ok
  test_c_roles_sellados_antes_que_todo_resultado: skip -- NO-PROCEDE-HISTÓRICO: catálogo y motor entraron en el mismo commit (e860e77, previo a la exigencia de ADR-68); no se reescribe historia -- NC-260921-MOTOR-THETA-CONGELADA-1-e8fa-02

T-MOTOR-HOLDOUT: 5 prueba(s) ok, 1 saltada(s)
```

## P3/P4 — universo vencido en alcance

```
$ python3 -m pytest tests/test_motor_gen2_explicito.py tests/test_consulta_gen2.py -q
...
FAILED tests/test_motor_gen2_explicito.py::MotorGen2Explicito::test_01_parametro_nuevo_apto_emite_result_completo
FAILED tests/test_motor_gen2_explicito.py::MotorGen2Explicito::test_08_transferencia_operativa_legitima_sigue_funcionando
FAILED tests/test_consulta_gen2.py::ConsultaGen2::test_01_cada_familia_directa_emite_su_valor_vigente
FAILED tests/test_consulta_gen2.py::ConsultaGen2::test_01b_guardia_suficiencia_protege_horizonte_colapsado
FAILED tests/test_consulta_gen2.py::ConsultaGen2::test_08_cli_verifica_respuestas_reproducibles
FAILED tests/test_consulta_gen2.py::ConsultaGen2::test_09_cli_verifica_alcance_menor_reproducible
6 failed, 25 passed, 25 subtests passed
```

`test_01`/`test_01b` fallan por consumidores GEN2 nuevos de universo `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv:*` (32 directos vs 13 esperados; 6 vs 3 en el guardia de suficiencia), no por el `p` de `tramite.evade/cuidado` que NC-0445 documentaba. `test_08` de `test_motor_gen2_explicito.py` falla contra `snapshot-M-gen2-explicito-v1_2.json` con un diff de 234 298 caracteres (90 933 vs 41 410) — el universo casi se duplicó desde que se congeló el snapshot (celda-D piloto 3/4, marco-M-sorteado, posteriores al 21/sep). `test_08`/`test_09` de `test_consulta_gen2.py` siguen siendo las respuestas de ejemplo congeladas que NC-0446 ya señalaba, pero verificar que cada diferencia se explique por un RESULT sellado posterior (condición que la propia NC exige) para 2 respuestas de ejemplo completas, sumado a la corrección de los dos conteos de universo, excede lo verificable de pasada en este acto y toca directamente qué se mide.

Ninguna causa documentada en `NC-0445`/`NC-0446` (fijadas 21/sep) coincide con las fallas reales de hoy. Se declaran `VENCIDAS EN ALCANCE` (A.10) y se abren NC nuevas con raíz de este acto, sin editar las viejas.

## Suite

```
$ python3 tests/check.py --rapido
...
  FAIL: 0 — VERDE
  0 FAIL · 335 WARN
```

## Perímetro

Tocado: `tests/test_motor_holdout.py` (P2), `forense/no-corrido.tsv` (3 filas nuevas `e270-01/02/03` + cierre de `e8fa-02`), `canon/gobernanza-v1_15.md`, esta nota, `canon/L0/ADR-260923-GEN2-MOTOR-DEUDA-LOTE-1-e270-01.md`, `canon/registro-rotulos.tsv`, `forense/encargos/2026-09-23-GEN2-MOTOR-DEUDA-LOTE-1.md` (cascada de cierre). No tocado: `milpa/src/motor.py`, `matriz.py`, `celdas.py`, `tramite.yaml`, `tests/test_motor_gen2_explicito.py`, `tests/test_consulta_gen2.py`, `forense/ejemplos/GEN2-*`, ningún CALC sellado.
