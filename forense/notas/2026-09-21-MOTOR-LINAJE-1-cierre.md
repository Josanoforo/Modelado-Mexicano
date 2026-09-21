# Nota de cierre · ACTO MOTOR-LINAJE-1 · 21/sep/2026

Contra \`origin/main = d5825063\`. Entorno **NUBE**, rama \`claude/ecstatic-edison-y1t005\`.
Cero microdato. \`data/raw\` AUSENTE — 0 archivos examinados (A.13). ENVIPE 2026 intacta.

## Salida cruda · P3 · las dos NC que se cierran (clon completo)

\`\`\`
$ git rev-parse --is-shallow-repository
false
$ git log --oneline | wc -l
5274

$ PYTHONPATH=. python3 tests/test_motor_holdout.py
  test_a2_firma_contra_el_commit_de_sello: ok
  test_a_conjunto_holdout_estable: ok
  test_b2_la_rebanada_completa_no_toca_holdout: ok
  test_b3_el_codigo_del_motor_no_llama_valor_de_en_holdout: ok
  test_b_ningun_valor_holdout_se_lee: ok
  test_c_roles_sellados_antes_que_todo_resultado: ok

T-MOTOR-HOLDOUT: 6 prueba(s) ok, 0 saltada(s)

$ PYTHONPATH=. python3 tests/test_celda_d_piloto_consumidor.py

----------------------------------------------------------------------
Ran 9 tests in 0.070s

OK
\`\`\`

## Salida cruda · P1 · los tres caminos del cargador, con datos sintéticos

\`\`\`
$ PYTHONPATH=. python3 tests/test_linaje_superado.py
Tercer estado de A.4: «no existe» no es «superado». ... ok
test_i_una_vigente_se_carga_como_siempre (__main__.TresCaminosDelCargador.test_i_una_vigente_se_carga_como_siempre) ... ok
test_ii_dos_vigentes_revientan_al_cargar (__main__.TresCaminosDelCargador.test_ii_dos_vigentes_revientan_al_cargar) ... ok
test_iii_cero_vigentes_no_revienta_el_indice_completo (__main__.TresCaminosDelCargador.test_iii_cero_vigentes_no_revienta_el_indice_completo) ... ok
test_iii_error_propio_por_corchete_y_por_get (__main__.TresCaminosDelCargador.test_iii_error_propio_por_corchete_y_por_get) ... ok
test_iii_la_entrada_no_se_omite_y_nombra_al_sucesor (__main__.TresCaminosDelCargador.test_iii_la_entrada_no_se_omite_y_nombra_al_sucesor) ... ok
test_iii_no_resuelve_al_sucesor_ni_devuelve_none (__main__.TresCaminosDelCargador.test_iii_no_resuelve_al_sucesor_ni_devuelve_none)
La adopción por la puerta de atrás es lo que esto impide. ... ok
test_iii_sin_sucesor_declarado_no_se_inventa (__main__.TresCaminosDelCargador.test_iii_sin_sucesor_declarado_no_se_inventa) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.004s

OK
\`\`\`

## Salida cruda · P2 · el delta, por comando (no a ojo)

\`\`\`
$ python3 tools/delta_pin_superado.py
DELTA-PIN-SUPERADO · universo=10542 ids · integramente_superados=222 · archivos_examinados=2 (A.13)
  SIN-PIN: 222
  VEREDICTO: ningun uso ACTIVO pin-ea un id integramente superado. No hay pin que actualizar ni delta que firmar.

$ python3 tools/delta_pin_superado.py --id RESULT-C1-POSEL-AMENAZA-DELTA
DELTA-PIN-SUPERADO · universo=10542 ids · integramente_superados=222 · archivos_examinados=2 (A.13)
  SIN-PIN: 1
  · RESULT-C1-POSEL-AMENAZA-DELTA → sucesor=CALC-0001-v2 · pines=NINGUNO · delta=None · SIN-PIN
  VEREDICTO: ningun uso ACTIVO pin-ea un id integramente superado. No hay pin que actualizar ni delta que firmar.
\`\`\`

> La receta se verifica contra un caso conocido (§2): el id que el encargo nombra da el sucesor `CALC-0001-v2` que `data/corrida0/resultados.tsv:213` declara en su campo `estado`, y `SIN-PIN`.

## Estado del test que el acto venía a destrabar

```
$ PYTHONPATH=. python3 tests/test_motor_gen2_explicito.py
ANTES:   Ran 0 tests  — ERROR en setUpClass
         ValueError: RESULT-C1-POSEL-AMENAZA-DELTA: se esperaba una fila vigente; hay 0
DESPUÉS: Ran 13 tests — FAILED (failures=1, errors=3)   → 9 en verde
```

Las 4 que quedan son **dos causas nuevas**, ninguna del cargador y las dos
vedadas por el CONTADOR y el PERÍMETRO de este encargo:

1. `test_01` · `share_horas_mujeres_40mas` → `NO_COVERAGE`, detalle verbatim:
   `p materializado no identifica al RESULT: 0.2215 vs 0.22148146779116093, tolerancia=5e-07`.
   El `p` vive en `milpa/tramite.yaml`; el CONTADOR dice «ninguna cifra de
   `milpa/tramite.yaml`». **No se toca.**
2. `test_08` / `test_10` / `test_11` · `construir_snapshot()` →
   `LookupError: tramite.evasion_norma: sin ola_calibracion: propia en milpa/tramite.yaml y sin entrada en _OLA_CALIBRACION_FIJA -- no se inventa, extiende la constante con la cita real antes de emitir esta celda.`
   Ni el yaml ni `tools/emite_m.py` están en el PERÍMETRO §9, y la cita real
   de la ola no es derivable en NUBE sin abrir dato. **No se inventa.**

Las dos son, cada una, un guardia funcionando correctamente. Lo que el acto
consiguió es que **se puedan ver**: estaban tapadas por una excepción de carga.

## Lo que este acto NO hizo

No cambió ninguna emisión del motor · no adoptó nada · no tocó la capa θ ni
la matriz · no adjudicó ninguna celda · no editó `data/corrida0/resultados.tsv`
(derivada) ni ninguna cifra de `milpa/tramite.yaml` · no abrió, derivó ni
imprimió dato de ninguna ola reservada.

Auditoría de rigor extremo: **no aplica** — este acto no afirma nada sobre México.
