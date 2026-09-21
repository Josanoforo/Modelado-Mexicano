# `ACTO GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1` · el COMMIT-1 del piloto 3, esta vez con cuerpo: corrió sobre sintético y reprodujo 2023 antes de congelarse; ENCIG 2025 sigue sin abrirse

**20/sep/2026 · CAJA (`ENTORNO-DERIVADO = CAJA`, corpus montado) · Opus 5 · rama `acto/gen2-celda-d-piloto-3-commit-1-v1_1`, apilada sobre `PR #924` (`25fe4dd0` = `origin/main` `98c00806` + 4 commits) porque `FP-399`/`FP-400` y `NC-0407`–`NC-0410` sólo existen ahí; #924 estaba OPEN al abrir (merge de mesa).**

Encargo archivado (A.3): `forense/encargos/2026-09-20-GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1.md` (input de dirección con las firmas `FP-399` y `FP-400` verbatim; el lanzamiento es el sello).

**Cero microdato de 2025.** Este acto abrió `encig23_base_datos_csv.zip` (control de oro) y los RESULT sellados de 2021/2023; no abrió `encig25_base_datos_csv.zip` ni derivó un solo conteo de 2025 (`tests/test_piloto3_v11.py::test_c_reserva_encig2025_no_abierta`).

## 1 · Qué se congeló

| artefacto | qué es |
|---|---|
| `forense/prereg-caja/GOB-gobierno-digital-exe15-spec-v1_1.md` + `.sha256` (`62d8d07d…`) | spec humana v1.1. **Primera línea:** proporción de **pagos ordinarios del servicio de luz** (`N_TRA == 01`) por canal digital `{4,5}` entre canal válido `{1,2,4,5,6}`, por edad × escolaridad, unidad trámite — confirmado por texto: el código `01` de 6.1 es «el pago ordinario del servicio de luz?» en 2021, 2023 y 2025. Hereda VERBATIM §1–§4.2 de la v1.0 (FP-400); cambian cuerpo (§5), S2 (§0) y validación (§6). |
| `data/corrida0/CALC-GOB-DIGITAL-EXE-EMISIONES-0002/{spec.yaml,medidor.py}` | COMMIT-2. `repite_de: …-0001` → el registro deriva `SUPERADO→…-0002` para la v1.0 (`n_resultados = 0`; la casa no re-ejecuta un id: se sucede, y así se hizo). 565 `RESULT` declarados, lista derivada por `esquema_resultados()`. |
| `data/corrida0/CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001/{spec.yaml,adjudicacion.py}` | COMMIT-3, archivo SEPARADO: único código que agrupa 2025 por dos variables; se niega sin `emisiones_resultados` + `emisiones_sello` (sha256 verificado) y sin reproducir el C2 sellado a 1e-9. 349 `RESULT`. |
| `tests/test_piloto3_v11.py` | las dos pruebas obligatorias + reserva + λ. |
| `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml` | celda-D en estado SPEC-CONGELADA (contrato en verde). Celdas-D 5 → **6**. |
| `data/corrida0/corridas.tsv` (derivado) | `registro --escribe`: 3+/1− (los dos CALC nuevos `SPEC-FIJADA`; la v1.0 `SUPERADO→0002`). Pisadas fuera de mis filas: `corridas`/`resultados`/`usos` **IDENTICO**. |

Ids libres verificados en las 5 ramas remotas antes de nombrarlos (`git ls-tree` por rama).

## 2 · Cuerpo de medición (lo que la v1.0 no tenía)

- Carga por id de manifiesto (`inputs[payload_id]["ruta_absoluta"]`); lector idéntico al script sellado; **join `sec_7 ← residentes` por `ID_PER`, `m:1`, validado** — la v1.0 unía por índice de fila.
- Bootstrap de diseño: UPM con reposición dentro de estrato, singleton de certeza, `PCG64(20260919)`, 10 000 réplicas en bloques de 50 — semilla y réplicas **leídas del precedente** (`CALC-ENCIG2023-CRUCES-HISTORICOS-0002/spec.yaml:38-40`). El marco de diseño **entero** entra al sorteo y «caso completo» va dentro de cada máscara: recortar antes cambia el conjunto de UPM y, con él, las réplicas (la primera versión lo hacía y los IC diferían 2e-3 de los sellados; corregido antes de congelar, como manda el punto 3).
- Emisiones: marginales por **una** variable (4+4+1) con IC; C2 = `expit(logit p_a + logit p_b − logit p_all)` réplica por réplica; S½, Sλ sobre el C2 de cada réplica con δ sellados; C1a = `expit(logit p₂₃ − δ₂₃)` punto (IC no derivable: sin réplicas selladas de 2023, declarado); C1b punto e IC sellados; control C2-compuesto y `|C2 − control|`; residuos F1-bis; **S2 por código** (`97/98/99`, n y masa), `S2-FRACCION-97-EN-60MAS`, `S2-RESERVA`.
- Adjudicación: `n(a,b)` 2025 y soporte definitivo, `R(a,b)` con IC y réplicas compartidas con C2, veredicto por celda con las dos condiciones INDECIDIBLE verbatim, ¾, ΔMAE con IC réplica por réplica, B-bis con la cláusula «si ambas caben, manda falsador débil», marca `RESERVA-S2`.

**Una precisión de cableado que mesa debe ver (spec v1.1 §4):** la v1.0 decía que el tercer requisito de soporte (`n ≥ 200` en 2025) «sólo se puede verificar en el COMMIT-2». Leer `n(a,b)` de 2025 es agrupar la ola reservada por dos variables, y E.6 lo reserva al código del COMMIT-3. Por eso el COMMIT-2 emite `SOPORTE-HISTORICO` y el COMMIT-3 fija `PUNTUADA`/`FUERA-DE-SOPORTE` con **la misma regla** antes de adjudicar. La regla se hereda verbatim; el momento cambia por E.6 y queda declarado. Si mesa prefiere que el COMMIT-2 exponga `n(a,b)` (un conteo sin desenlace), es una línea en `medidor.py` y una firma — no se decidió aquí.

## 3 · Validación de «congelado» — salida cruda

```
tests/test_piloto3_v11.py
  test_a_medir_punta_a_punta_sintetico        PASSED   (7 000 personas, 3 estratos, 24 UPM; 16 celdas × {C2,S½,Sλ} con IC; esquema == emitido)
  test_a_adjudicacion_sobre_r_sintetico       PASSED   (≥12 PUNTUADA, CON-SOPORTE, B-BIS emitido; sin sello → ParoDeGuardia; sello alterado → para)
  test_c_guardias_paran                       PASSED   (FP-399 ABIERTA → para; CAMBIO-DE-INSTRUMENTO → para; insumo 2025 con ola≠2025 → para)
  test_c_fp399_firmada_en_el_repo             PASSED
  test_c_reserva_encig2025_no_abierta         PASSED   (sin ejecucion/resultados/sello en los dos CALC; ningún RESULT-…-2025 en el árbol)
  test_d_lambda_se_rederiva_de_los_sellados   PASSED   (λ, τ̂², σ̄² a 1e-12 / 1e-15)
  test_b_oro_2023_reproduce_los_sellados      PASSED   (16 n exactos; |Δp| = 0.0; |Δδ| = 1.7e-16; |ΔIC| < 1e-9; residuo 107 = 107×98)
7 passed in 20.55s
tests/test_celdas_d.py + tests/test_piloto3_guardias.py: 26 passed
corrida0 spec-check: EMISIONES-0002 9 OK · 0 FAIL; ADJUDICACION-0001 9 OK · 0 FAIL (317 718 filas de inventario; ningún dato abierto)
```

El control de oro (b) **no es una medición nueva**: no se sella, no entra a `corridas.tsv`, no mueve contador.

## 4 · Trámite

`FP-399` y `FP-400` → **FIRMADA** (texto de mesa verbatim en `firmada_en`). `NC-0407`–`NC-0410`: enmienda fechada con este sucesor (siguen ABIERTAS: lo que falta es ejecutar COMMIT-2/3, no congelar). `FP-393` (unidad de celda-D sobre eventos) **sigue ABIERTA**: la celda se registró con `unidad_objetivo: persona` (la del modelo) y `universo_instrumento: TRÁMITES` por el precedente `TRA.evade_norma`; si mesa añade `evento`/`tramite` al enum, es una línea. `cuenta_gen2 = SI` propuesto en las dos specs, nace PENDIENTE-DE-MESA. Dos líneas `PARA-v2.15` en `hallazgos.md`.

**Contadores:** `N_corridas_selladas` +0 (COMMIT-1 no sella); celdas-D 5 → 6 (una en SPEC-CONGELADA); el par `edad×escolaridad` de ENCIG 2025 sigue `RESERVADA`; nada se adopta.

## 5 · Lo que sigue (otra sesión, F3)

COMMIT-2 en CAJA: `corrida0 run CALC-GOB-DIGITAL-EXE-EMISIONES-0002`; vista y replay en el mismo acto (E.7); commit y push antes de seguir. COMMIT-3, sólo con el COMMIT-2 empujado: `corrida0 run CALC-GOB-DIGITAL-EXE-ADJUDICACION-0001`; llena la celda-D; re-deriva el marcador; declara el par consumido. Ninguna lectura no pre-registrada entra al veredicto.
