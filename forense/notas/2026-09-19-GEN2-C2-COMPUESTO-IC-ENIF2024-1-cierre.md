# ACTO GEN2-C2-COMPUESTO-IC-ENIF2024-1 · las 136 emisiones C2 de ENIF 2024 ganan su IC95, réplica por réplica

**Universo:** las 13 502 personas elegidas de `TMODULO.csv` (`enif_2024_bd_csv.zip`, sha256 `00e4b0b4…f039`), el universo del árbitro (`tools/medidor_ahorro_enif24.py::carga`) sin un filtro más · **unidad del dato:** PERSONA elegida 18+ · ponderador `FAC_PER`, estrato `EST_DIS`, UPM `UPM_DIS` (190 estratos, 2 164 UPM) · **escala:** proporción · **clase de evidencia:** (a) · **celdas que quedaron con IC: 136 de 136 emitibles, derivado** (`RESULT-C2IC-ENIF2024-G-N-CELDAS-CON-IC = 136`, `G-N-CELDAS-EMITIBLES = 136`, `G-N-FILAS-EMITIBLES = 18` de 28 filas ENIF 2024 del dictamen). El IC mide ruido muestral del estimador bajo el supuesto de no-interacción; **no** mide el error de ese supuesto. Un IC estrecho no es una celda bien estimada.

**19/sep/2026 · CAJA (Ubuntu/WSL2), Opus 5 · corpus montado (`tools/entorno.py --sonda-red`: `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`, `red=200`, `corpus=SI(examinados=419)`, `raices data_raw:SI descargas_mx:SI`).** Encargo archivado verbatim por 0-bis A.3 en `forense/encargos/2026-09-19-GEN2-C2-COMPUESTO-IC-ENIF2024-1.md`. Base `a92126f0` (= `origin/main` al abrir, 0 commits detrás); `origin/main` se movió 29 commits durante el acto y se fusionó limpio antes de la cascada (`8d66ff0`).

## 0 · Veredicto

`CALC-C2-COMPUESTO-IC-ENIF2024-0001--d2c22b3f1da5` **SELLADA**, `verify` aislado ×2 **REPRODUCE** (`CONTEXTO=IDENTICO`, 1 336/1 336 RESULT, 11/11 inputs `COINCIDE`). **Los dos controles de coherencia REPRODUCE**, así que el IC se publica:

| control | veredicto | cifra | comando |
|---|---|---|---|
| 1 · punto vs `CALC-C2-COMPUESTO-RESERVADAS-0001` | REPRODUCE | Δ máx abs = **0.0** en 136/136 | `jq '.resultados["RESULT-C2IC-ENIF2024-G-CONTROL-1-DELTA-MAX-ABS"]' data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001/resultados.json` |
| 2 · marginales de la réplica base vs R sellados del árbitro | REPRODUCE | \|Δp\| máx 7.99e-07 · \|ΔIC\| máx 4.94e-07 · Δn = 0 en 30/30 | `jq '.resultados \| with_entries(select(.key \| test("G-CONTROL-2")))' …/resultados.json` |

**Réplicas sin definir: 0** de 10 000 en las 136 celdas (`G-REPLICAS-SIN-DEFINIR-TOTAL = 0`); anchura del IC95: mín 0.0325, mediana 0.0514, máx 0.0772. C2 vectorizado vs `piso_log_aditivo`: Δ máx 1.1e-16.

**Contadores.** `N_corridas_selladas` +1 (`CALC-C2-COMPUESTO-IC-ENIF2024-0001`). `cuenta_gen2` nace **NO** por E.1 (cadena con input legacy `milpa/tramite-ola5-propuesta-v0.yaml`, `envuelto_legacy = SI`) — exactamente como su padre (`NC-0350`); se **propone** `SI` para mesa. `adoptados_activos`: **no se mueve** (0 adopciones; `G-ADOPTA = NO`). Los 18 pares siguen `RESERVADA`; las emisiones siguen `EMITIDA-SIN-EVALUAR`. `G-CRUCE-DERIVADO = NO`.

## 1 · Hallazgo P0 y desviación escrita (mesa, 19/sep/2026)

`tools/celda_d/marginales_reproduccion.py` es **ENVIPE-only**: `carga_ola()` (líneas 172-231) lee `tmod_vic`/`tsdem`, universo `BP1_20`, `FAC_DEL`; `EJES` (línea 99) admite `escolaridad_proxy`, `dominio_urbano_rural`, `nacional`. Los cinco ejes de los 18 pares `EMITIBLE` de ENIF 2024 reciben `ValueError`. Sonda mecánica en la corrida: `G-P0-MODULO-GUARDADO-{SEXO,EDAD,ESCOLARIDAD,LOCALIDAD,CUENTA-FORMAL} = NO-ADMITE-EJE · ValueError…`; `G-P0-MODULO-GUARDADO-NACIONAL = ADMITE-EJE-POR-NOMBRE pero NO-ADMITE-OLA · TypeError…`; `G-P0-MODULO-GUARDADO-EJES-ADMITIDOS = 1` (de 6). Es el mismo hallazgo que el acto gemelo `GEN2-C2-COMPUESTO-IC-ENVIPE2025-1` (`ADR-553`, `FP-390`) hizo para `sexo`/`edad` en ENVIPE 2025.

Bajo la regla literal de P0, las 136 celdas habrían salido `IC-NO-CONSTRUIBLE`. Se preguntó a mesa con tres opciones (desviación escrita · PARO-PREMISA con cero CALC · sellar 136 × IC-NO-CONSTRUIBLE) y mesa eligió la primera, verbatim en `forense/prereg-caja/C2-COMPUESTO-IC-ENIF2024-spec-v1_0.md §0`: **el medidor lleva su propia guardia de una variable con la misma semántica** (`marginal_enif(ola, grupo: str)`: str posicional único → `TypeError` con lista o dos posicionales; whitelist de 6 ejes → `ValueError`; huella de la ola → `ReservaRota`; sin `cruce()`) **e importa del árbitro** (`tools/medidor_ahorro_enif24.py`) universo, desenlaces y la construcción de cada eje. `marginales_reproduccion.py` **no se modificó** (sha256 `f27728cb…` intacto, input `IN-MODULO-GUARDADO` del CALC); de él se importa `cotejo()` (control 2). Esto es, de facto, una cuarta vía frente a las tres de `FP-390`: no amplía el módulo, no renuncia al IC, no sella el hueco — pone la guardia junto al medidor y la prueba por mutación. Mesa decide si esa vía vale también para ENVIPE 2025 o si prefiere el camino 1 de `FP-390` (ampliar el módulo) y luego migrar este medidor a él.

## 2 · Guardia E.6 como código (NC-0328), probada por mutación

`auditoria_ast()` vive en el medidor y `medir()` la corre sobre su propio archivo **antes** de abrir el zip (`G-GUARDIA-AST = PASA`, `G-GUARDIA-AST-VIOLACIONES = 0`). `tests/test_c2_ic_enif2024_guardia.py`: **43/43** — 19 mutaciones detectadas (una o más por regla R1–R8: `import zipfile`, `groupby(["sexo","edad"])`, `crosstab`, `pivot_table`, `open()`, `getattr`, `.df` fuera del núcleo, `(celda == k) & (y_all > 0)` dentro del núcleo, `and` entre comparaciones, producto de dos máscaras, `OlaEnif(` fuera de sitio, `carga()` fuera de sitio, `_importa` de `marcador_segmento.py`, `marginal_enif` con lista / con tres posicionales, `def cruce_enif`, `inputs["envipe2025_csv"]`, `"conjunto_de_datos_tmodulo_enif2024.csv"`, `inputs["IN-OTRO"]`) + guardia en ejecución sobre datos fabricados (TypeError/ValueError/ReservaRota, marginal = razón de totales ponderados, réplicas deterministas por seed, C2 vectorizado = `piso_log_aditivo` a 1e-12) + `spec.yaml` ≡ catálogo del medidor (1 336 ids, tipos y `permite_no_estimable`). **Límite declarado:** R4 es sintáctico; lo que sostiene la reserva es R3 (el microdato sólo es alcanzable dentro de 7 funciones) más R1/R2/R5 (nada entra que no esté en la lista). CI: `tests/check.py` no auto-descubre `tests/test_*.py` y `.github/workflows/verify.yml` está fuera del perímetro de este acto → `NC` abajo; mientras tanto la guardia corre en cada `run`/`verify` porque vive en el medidor.

## 3 · Tabla afirmación → comando

| afirmación | comando |
|---|---|
| 136 celdas emitibles, 18 filas (par × desenlace) de 28 filas ENIF 2024 del dictamen — derivado | `python3 - <<'X'` … `csv.DictReader` sobre `data/corrida0/c2-compuesto-dictamen-v1_0.tsv`, filtro `ola == "ENIF 2024" and veredicto == "EMITIBLE"`, suma de `n_celdas` `X` → 28 / 18 / 136; y `jq '.resultados["RESULT-C2IC-ENIF2024-G-N-CELDAS-EMITIBLES"]' …/resultados.json` → 136 |
| 136/136 con IC95 | `jq '.resultados["RESULT-C2IC-ENIF2024-G-N-CELDAS-CON-IC"]' …/resultados.json` → 136 |
| 0 réplicas sin definir | `jq '.resultados["RESULT-C2IC-ENIF2024-G-REPLICAS-SIN-DEFINIR-TOTAL"]'` → 0 |
| control 1 REPRODUCE, Δ máx 0.0 | `jq '.resultados["RESULT-C2IC-ENIF2024-G-CONTROL-1-PUNTO-VEREDICTO"], .resultados["RESULT-C2IC-ENIF2024-G-CONTROL-1-DELTA-MAX-ABS"]'` |
| control 2 REPRODUCE en 30/30 marginales | `jq '.resultados \| with_entries(select(.key \| test("CONTROL-2-VEREDICTO"))) \| map_values(.) '` → 12 ejes×desenlace REPRODUCE; `G-CONTROL-2-N-GRUPOS = 30` |
| el módulo guardado no admite 5/5 ejes de ENIF | `jq '.resultados \| with_entries(select(.key \| test("G-P0-MODULO")))'` |
| `marginales_reproduccion.py` intacto | `git diff a92126f0 HEAD -- tools/celda_d/marginales_reproduccion.py` → vacío; `sha256sum` = `f27728cb…` (= `IN-MODULO-GUARDADO`) |
| verify REPRODUCE ×2 | `python3 tools/corrida0.py verify CALC-C2-COMPUESTO-IC-ENIF2024-0001` (dos veces) → `VERIFY: REPRODUCE (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)` |
| guardia AST 43/43 | `python3 tests/test_c2_ic_enif2024_guardia.py` → `Ran 43 tests … OK` |
| pisadas en las vistas derivadas: 0 filas ajenas modificadas o borradas | `git show origin/main:data/corrida0/corridas.tsv \| grep -v C2-COMPUESTO-IC-ENIF2024 \| sort > a; grep -v C2-COMPUESTO-IC-ENIF2024 data/corrida0/corridas.tsv \| sort > b; comm -23 a b \| wc -l` → 0 (ídem `resultados.tsv`, `usos.tsv`) |
| CALC-id reservado libre al congelar | `for r in $(git ls-remote --heads origin \| awk '{print $2}'); do git grep -l CALC-C2-COMPUESTO-IC-ENIF2024-0001 origin/${r#refs/heads/}; done` → 0 aciertos en 6/6 ramas; control positivo `CALC-C2-COMPUESTO-RESERVADAS-0001` → 3 archivos |
| suite | `python3 tests/check.py --baseline` → LÍNEA BASE VERDE |

## 4 · Control 2 por eje y desenlace (réplica base vs `milpa/tramite-ola5-propuesta-v0.yaml:1415-1599` y `NACIONALES`)

| desenlace | eje | veredicto | \|Δp\| max | \|ΔIC\| max | cobertura | fuera |
|---|---|---|---|---|---|---|
| ahorra-solo-informal | cuenta-formal | REPRODUCE | 3.87e-07 | 4.77e-07 | 1.000000 | 0 |
| ahorra-solo-informal | edad | REPRODUCE | 4.70e-07 | 4.80e-07 | 0.998889 | 15 |
| ahorra-solo-informal | escolaridad | REPRODUCE | 4.57e-07 | 4.55e-07 | 0.999630 | 5 |
| ahorra-solo-informal | localidad | REPRODUCE | 4.61e-07 | 4.64e-07 | 1.000000 | 0 |
| ahorra-solo-informal | sexo | REPRODUCE | 2.68e-07 | 4.94e-07 | 1.000000 | 0 |
| ahorra-solo-informal | nacional | REPRODUCE | 7.99e-07 | 0.00e+00 | 1.000000 | 0 |
| informal-cualquiera | cuenta-formal | REPRODUCE | 1.81e-07 | 4.77e-07 | 1.000000 | 0 |
| informal-cualquiera | edad | REPRODUCE | 4.87e-07 | 4.70e-07 | 0.998889 | 15 |
| informal-cualquiera | escolaridad | REPRODUCE | 3.76e-07 | 4.05e-07 | 0.999630 | 5 |
| informal-cualquiera | localidad | REPRODUCE | 4.39e-07 | 4.68e-07 | 1.000000 | 0 |
| informal-cualquiera | sexo | REPRODUCE | 4.83e-07 | 1.57e-07 | 1.000000 | 0 |
| informal-cualquiera | nacional | REPRODUCE | 4.79e-07 | 3.07e-07 | 1.000000 | 0 |

`n` exacto en las 30 celdas (`G-CONTROL-2-DELTA-N-MAX = 0`). Cobertura de `edad` 0.998889 (15 personas de 97+ años quedan fuera del tramo `60+ = 60..96` del árbitro) y de `escolaridad` 0.999630 (5 con `NIV = 99`): las mismas que el yaml sella. Poblacion expandida 94 221 441.

## 5 · Las 136 celdas — punto (sellado) e IC95 réplica por réplica

Rótulo del IC: `IC95-BOOTSTRAP-REPLICA-POR-REPLICA-MARGINALES-COMPARTIDOS` · supuesto `ausencia de interaccion en escala logit` · estado de la emisión `EMITIDA-SIN-EVALUAR`. El punto es el ya sellado por `CALC-C2-COMPUESTO-RESERVADAS-0001` (Δ = 0.0). Tabla derivada de `resultados.json` + `_plan()` del medidor (136 filas):

| desenlace | par | celda a | celda b | punto (sellado) | IC95 inf | IC95 sup | anchura | réplicas válidas | Δ control 1 |
|---|---|---|---|---|---|---|---|---|---|
| ahorra_solo_informal | cuenta_formal × edad | sin cuenta | 18-29 | 0.571586 | 0.539817 | 0.601154 | 0.0613 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | sin cuenta | 30-44 | 0.513488 | 0.484579 | 0.541034 | 0.0565 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | sin cuenta | 45-59 | 0.460650 | 0.432128 | 0.489645 | 0.0575 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | sin cuenta | 60+ | 0.402263 | 0.372582 | 0.431684 | 0.0591 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | con cuenta | 18-29 | 0.353608 | 0.328387 | 0.379643 | 0.0513 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | con cuenta | 30-44 | 0.302044 | 0.281017 | 0.323811 | 0.0428 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | con cuenta | 45-59 | 0.259365 | 0.239567 | 0.279595 | 0.0400 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × edad | con cuenta | 60+ | 0.216261 | 0.193632 | 0.240047 | 0.0464 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | sin cuenta | 18-29 | 0.644746 | 0.613722 | 0.673535 | 0.0598 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | sin cuenta | 30-44 | 0.558717 | 0.529519 | 0.586053 | 0.0565 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | sin cuenta | 45-59 | 0.427048 | 0.398186 | 0.455989 | 0.0578 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | sin cuenta | 60+ | 0.318044 | 0.293797 | 0.342032 | 0.0482 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | con cuenta | 18-29 | 0.734715 | 0.713601 | 0.755849 | 0.0422 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | con cuenta | 30-44 | 0.658949 | 0.637788 | 0.679205 | 0.0414 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | con cuenta | 45-59 | 0.532143 | 0.508442 | 0.556150 | 0.0477 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × edad | con cuenta | 60+ | 0.415780 | 0.387720 | 0.444342 | 0.0566 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | sin cuenta | hasta primaria | 0.487434 | 0.456140 | 0.517178 | 0.0610 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | sin cuenta | secundaria | 0.555038 | 0.526261 | 0.582469 | 0.0562 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | sin cuenta | media superior | 0.527888 | 0.494914 | 0.559427 | 0.0645 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | sin cuenta | superior | 0.381797 | 0.353686 | 0.409680 | 0.0560 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | con cuenta | hasta primaria | 0.280533 | 0.257956 | 0.303266 | 0.0453 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | con cuenta | secundaria | 0.338385 | 0.315811 | 0.360990 | 0.0452 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | con cuenta | media superior | 0.314347 | 0.289585 | 0.340775 | 0.0512 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × escolaridad | con cuenta | superior | 0.202059 | 0.182431 | 0.222584 | 0.0402 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | sin cuenta | hasta primaria | 0.349326 | 0.321318 | 0.376728 | 0.0554 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | sin cuenta | secundaria | 0.487990 | 0.459002 | 0.516597 | 0.0576 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | sin cuenta | media superior | 0.572202 | 0.540500 | 0.602716 | 0.0622 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | sin cuenta | superior | 0.574661 | 0.548071 | 0.600826 | 0.0528 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | con cuenta | hasta primaria | 0.450328 | 0.425349 | 0.476359 | 0.0510 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | con cuenta | secundaria | 0.592571 | 0.569825 | 0.614844 | 0.0450 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | con cuenta | media superior | 0.671173 | 0.647837 | 0.694680 | 0.0468 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × escolaridad | con cuenta | superior | 0.673388 | 0.649492 | 0.697457 | 0.0480 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × localidad | sin cuenta | menor de 15 000 | 0.548527 | 0.518354 | 0.576541 | 0.0582 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × localidad | sin cuenta | 15 000 y mas | 0.463312 | 0.440027 | 0.485834 | 0.0458 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × localidad | con cuenta | menor de 15 000 | 0.332516 | 0.309825 | 0.355305 | 0.0455 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × localidad | con cuenta | 15 000 y mas | 0.261428 | 0.245413 | 0.277941 | 0.0325 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × localidad | sin cuenta | menor de 15 000 | 0.480919 | 0.451725 | 0.508715 | 0.0570 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × localidad | sin cuenta | 15 000 y mas | 0.500131 | 0.478114 | 0.521805 | 0.0437 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × localidad | con cuenta | menor de 15 000 | 0.585718 | 0.564773 | 0.606498 | 0.0417 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × localidad | con cuenta | 15 000 y mas | 0.604244 | 0.587027 | 0.621974 | 0.0349 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × sexo | sin cuenta | 1 Hombre | 0.466255 | 0.443765 | 0.487987 | 0.0442 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × sexo | sin cuenta | 2 Mujer | 0.516480 | 0.491374 | 0.541333 | 0.0500 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × sexo | con cuenta | 1 Hombre | 0.263719 | 0.246254 | 0.281353 | 0.0351 | 10000 | 0.0e+00 |
| ahorra_solo_informal | cuenta_formal × sexo | con cuenta | 2 Mujer | 0.304576 | 0.287212 | 0.322055 | 0.0348 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × sexo | sin cuenta | 1 Hombre | 0.491003 | 0.467646 | 0.513555 | 0.0459 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × sexo | sin cuenta | 2 Mujer | 0.495677 | 0.470290 | 0.520561 | 0.0503 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × sexo | con cuenta | 1 Hombre | 0.595479 | 0.575658 | 0.615536 | 0.0399 | 10000 | 0.0e+00 |
| informal_cualquiera | cuenta_formal × sexo | con cuenta | 2 Mujer | 0.599975 | 0.583667 | 0.616475 | 0.0328 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 18-29 | hasta primaria | 0.426111 | 0.395728 | 0.455324 | 0.0596 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 18-29 | secundaria | 0.493397 | 0.463477 | 0.522719 | 0.0592 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 18-29 | media superior | 0.466104 | 0.427293 | 0.504526 | 0.0772 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 18-29 | superior | 0.325329 | 0.292367 | 0.359055 | 0.0667 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 30-44 | hasta primaria | 0.370027 | 0.342062 | 0.398684 | 0.0566 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 30-44 | secundaria | 0.435173 | 0.406268 | 0.463355 | 0.0571 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 30-44 | media superior | 0.408504 | 0.375830 | 0.442117 | 0.0663 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 30-44 | superior | 0.276128 | 0.251090 | 0.302575 | 0.0515 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 45-59 | hasta primaria | 0.322176 | 0.294947 | 0.350200 | 0.0553 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 45-59 | secundaria | 0.384032 | 0.354311 | 0.414245 | 0.0599 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 45-59 | media superior | 0.358508 | 0.328037 | 0.389364 | 0.0613 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 45-59 | superior | 0.235873 | 0.212856 | 0.259548 | 0.0467 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 60+ | hasta primaria | 0.272474 | 0.240071 | 0.307071 | 0.0670 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 60+ | secundaria | 0.329425 | 0.298639 | 0.360446 | 0.0618 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 60+ | media superior | 0.305729 | 0.278448 | 0.334182 | 0.0557 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × escolaridad | 60+ | superior | 0.195642 | 0.173172 | 0.219428 | 0.0463 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 18-29 | hasta primaria | 0.568304 | 0.536389 | 0.599519 | 0.0631 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 18-29 | secundaria | 0.700333 | 0.673917 | 0.725618 | 0.0517 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 18-29 | media superior | 0.766343 | 0.739998 | 0.791563 | 0.0516 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 18-29 | superior | 0.768138 | 0.742263 | 0.793278 | 0.0510 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 30-44 | hasta primaria | 0.478730 | 0.448110 | 0.509262 | 0.0612 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 30-44 | secundaria | 0.619828 | 0.591870 | 0.646681 | 0.0548 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 30-44 | media superior | 0.695871 | 0.668269 | 0.722474 | 0.0542 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 30-44 | superior | 0.697994 | 0.671197 | 0.724043 | 0.0528 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 45-59 | hasta primaria | 0.350921 | 0.323081 | 0.379583 | 0.0565 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 45-59 | secundaria | 0.489741 | 0.458267 | 0.520992 | 0.0627 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 45-59 | media superior | 0.573917 | 0.542154 | 0.605411 | 0.0633 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 45-59 | superior | 0.576373 | 0.548276 | 0.605262 | 0.0570 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 60+ | hasta primaria | 0.252775 | 0.225104 | 0.282205 | 0.0571 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 60+ | secundaria | 0.375213 | 0.345422 | 0.405057 | 0.0596 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 60+ | media superior | 0.457348 | 0.425147 | 0.490358 | 0.0652 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × escolaridad | 60+ | superior | 0.459844 | 0.428810 | 0.491814 | 0.0630 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 18-29 | 1 Hombre | 0.405489 | 0.377201 | 0.433710 | 0.0565 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 18-29 | 2 Mujer | 0.454745 | 0.426095 | 0.482653 | 0.0566 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 30-44 | 1 Hombre | 0.350462 | 0.327519 | 0.373594 | 0.0461 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 30-44 | 2 Mujer | 0.397503 | 0.373008 | 0.422201 | 0.0492 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 45-59 | 1 Hombre | 0.303920 | 0.281189 | 0.327015 | 0.0458 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 45-59 | 2 Mujer | 0.348062 | 0.324769 | 0.372242 | 0.0475 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 60+ | 1 Hombre | 0.255971 | 0.232357 | 0.279726 | 0.0474 | 10000 | 0.0e+00 |
| ahorra_solo_informal | edad × sexo | 60+ | 2 Mujer | 0.296110 | 0.269790 | 0.323331 | 0.0535 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 18-29 | 1 Hombre | 0.702858 | 0.678054 | 0.727164 | 0.0491 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 18-29 | 2 Mujer | 0.706748 | 0.682955 | 0.730513 | 0.0476 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 30-44 | 1 Hombre | 0.622666 | 0.598157 | 0.646956 | 0.0488 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 30-44 | 2 Mujer | 0.627049 | 0.603531 | 0.649453 | 0.0459 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 45-59 | 1 Hombre | 0.492754 | 0.465715 | 0.519943 | 0.0542 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 45-59 | 2 Mujer | 0.497429 | 0.473268 | 0.521984 | 0.0487 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 60+ | 1 Hombre | 0.378044 | 0.351116 | 0.405467 | 0.0544 | 10000 | 0.0e+00 |
| informal_cualquiera | edad × sexo | 60+ | 2 Mujer | 0.382451 | 0.356501 | 0.409139 | 0.0526 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | hasta primaria | menor de 15 000 | 0.403394 | 0.369794 | 0.437082 | 0.0673 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | hasta primaria | 15 000 y mas | 0.324519 | 0.302131 | 0.346974 | 0.0448 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | secundaria | menor de 15 000 | 0.470031 | 0.440941 | 0.498358 | 0.0574 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | secundaria | 15 000 y mas | 0.386569 | 0.362575 | 0.410513 | 0.0479 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | media superior | menor de 15 000 | 0.442900 | 0.410385 | 0.475865 | 0.0655 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | media superior | 15 000 y mas | 0.360975 | 0.333281 | 0.389032 | 0.0558 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | superior | menor de 15 000 | 0.305128 | 0.278273 | 0.332702 | 0.0544 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × localidad | superior | 15 000 y mas | 0.237808 | 0.216377 | 0.260185 | 0.0438 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | hasta primaria | menor de 15 000 | 0.401925 | 0.369693 | 0.434787 | 0.0651 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | hasta primaria | 15 000 y mas | 0.420538 | 0.397350 | 0.443611 | 0.0463 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | secundaria | menor de 15 000 | 0.544011 | 0.516246 | 0.571292 | 0.0550 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | secundaria | 15 000 y mas | 0.563010 | 0.539037 | 0.586796 | 0.0478 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | media superior | menor de 15 000 | 0.626070 | 0.597825 | 0.654219 | 0.0564 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | media superior | 15 000 y mas | 0.643888 | 0.618808 | 0.669399 | 0.0506 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | superior | menor de 15 000 | 0.628420 | 0.602718 | 0.654053 | 0.0513 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × localidad | superior | 15 000 y mas | 0.646189 | 0.621330 | 0.671084 | 0.0498 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | hasta primaria | 1 Hombre | 0.327119 | 0.302781 | 0.351231 | 0.0485 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | hasta primaria | 2 Mujer | 0.372824 | 0.346917 | 0.399052 | 0.0521 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | secundaria | 1 Hombre | 0.389379 | 0.365821 | 0.413004 | 0.0472 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | secundaria | 2 Mujer | 0.438119 | 0.412646 | 0.463101 | 0.0505 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | media superior | 1 Hombre | 0.363709 | 0.336118 | 0.392087 | 0.0560 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | media superior | 2 Mujer | 0.411401 | 0.382776 | 0.440504 | 0.0577 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | superior | 1 Hombre | 0.239960 | 0.217695 | 0.262542 | 0.0448 | 10000 | 0.0e+00 |
| ahorra_solo_informal | escolaridad × sexo | superior | 2 Mujer | 0.278528 | 0.255525 | 0.302404 | 0.0469 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | hasta primaria | 1 Hombre | 0.411666 | 0.385329 | 0.438063 | 0.0527 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | hasta primaria | 2 Mujer | 0.416203 | 0.389578 | 0.442764 | 0.0532 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | secundaria | 1 Hombre | 0.554006 | 0.528692 | 0.579072 | 0.0504 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | secundaria | 2 Mujer | 0.558622 | 0.534451 | 0.582668 | 0.0482 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | media superior | 1 Hombre | 0.635471 | 0.608249 | 0.663022 | 0.0548 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | media superior | 2 Mujer | 0.639792 | 0.614849 | 0.664195 | 0.0493 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | superior | 1 Hombre | 0.637796 | 0.612248 | 0.663165 | 0.0509 | 10000 | 0.0e+00 |
| informal_cualquiera | escolaridad × sexo | superior | 2 Mujer | 0.642106 | 0.617535 | 0.666218 | 0.0487 | 10000 | 0.0e+00 |
| ahorra_solo_informal | localidad × sexo | menor de 15 000 | 1 Hombre | 0.383137 | 0.358901 | 0.407212 | 0.0483 | 10000 | 0.0e+00 |
| ahorra_solo_informal | localidad × sexo | menor de 15 000 | 2 Mujer | 0.431649 | 0.405181 | 0.457467 | 0.0523 | 10000 | 0.0e+00 |
| ahorra_solo_informal | localidad × sexo | 15 000 y mas | 1 Hombre | 0.306191 | 0.287992 | 0.324532 | 0.0365 | 10000 | 0.0e+00 |
| ahorra_solo_informal | localidad × sexo | 15 000 y mas | 2 Mujer | 0.350496 | 0.331811 | 0.369206 | 0.0374 | 10000 | 0.0e+00 |
| informal_cualquiera | localidad × sexo | menor de 15 000 | 1 Hombre | 0.547000 | 0.521778 | 0.572393 | 0.0506 | 10000 | 0.0e+00 |
| informal_cualquiera | localidad × sexo | menor de 15 000 | 2 Mujer | 0.551630 | 0.528445 | 0.574447 | 0.0460 | 10000 | 0.0e+00 |
| informal_cualquiera | localidad × sexo | 15 000 y mas | 1 Hombre | 0.565974 | 0.546773 | 0.585574 | 0.0388 | 10000 | 0.0e+00 |
| informal_cualquiera | localidad × sexo | 15 000 y mas | 2 Mujer | 0.570563 | 0.551829 | 0.589241 | 0.0374 | 10000 | 0.0e+00 |

## 6 · Salida cruda del `verify` (asiento de `forense/replay-evidencia.tsv`)

```
VERIFY CALC-C2-COMPUESTO-IC-ENIF2024-0001   (data/corrida0/CALC-C2-COMPUESTO-IC-ENIF2024-0001)
  [1/5 SELLO] COINCIDE -- sello y todos los archivos que cubre coinciden
  [2/5 SPEC.YAML] IDENTICO  sellado=fdf2fdca357c7084d63ca841da703af0416332bcf856b2abe624f02b4c5f163d  hoy=fdf2fdca357c7084d63ca841da703af0416332bcf856b2abe624f02b4c5f163d
  [3/5 INPUT COINCIDE] enif_2024_enif_2024_bd_csv (manifiesto)  sellado=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039  actual=00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039
  [3/5 INPUT COINCIDE] IN-DICTAMEN (repo)  sellado=1e770c086a38fc3856ae04dee2f0260b300b41ae741a2c40adf9aa13d584dc6e  hoy=1e770c086a38fc3856ae04dee2f0260b300b41ae741a2c40adf9aa13d584dc6e
  [3/5 INPUT COINCIDE] IN-ARBITRO-MARGINALES (repo)  sellado=93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f  hoy=93dfa3f9aab250dabf9cbe8c93ccef2012cb763c5367d023f24dbfbd867fbc8f
  [3/5 INPUT COINCIDE] IN-PUNTOS-SELLADOS (repo)  sellado=be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb  hoy=be24d879d22d28a05c36441b471976a6b0b3d40f2877efa2cd514a13e5bae3cb
  [3/5 INPUT COINCIDE] IN-SPEC-SELLADA (repo)  sellado=4f712d5fdac20a21a5e268000fe38ef52801ac8aa3e5e70dbc38dd2369008acb  hoy=4f712d5fdac20a21a5e268000fe38ef52801ac8aa3e5e70dbc38dd2369008acb
  [3/5 INPUT COINCIDE] IN-ARBITRO-MEDIDOR (repo)  sellado=58c429598c3cedd6d1f8927e8854bbb6f4461f04a94d4a92568a388c7f1f2c95  hoy=58c429598c3cedd6d1f8927e8854bbb6f4461f04a94d4a92568a388c7f1f2c95
  [3/5 INPUT COINCIDE] IN-ARBITRO-EJES (repo)  sellado=502f5a4138c6733677f9472947cfe8c112dd04618e6ac325dd816758f7206c4d  hoy=502f5a4138c6733677f9472947cfe8c112dd04618e6ac325dd816758f7206c4d
  [3/5 INPUT COINCIDE] IN-MODULO-GUARDADO (repo)  sellado=f27728cb7c24888237717cdab7ebd7c17eca782a72dc31311faa56057e05da84  hoy=f27728cb7c24888237717cdab7ebd7c17eca782a72dc31311faa56057e05da84
  [3/5 INPUT COINCIDE] IN-FORMA-C2-SELLADA (repo)  sellado=71878f9ca98698a4d770b77e583e5086875509dcd022ba6928b86caa976a12d9  hoy=71878f9ca98698a4d770b77e583e5086875509dcd022ba6928b86caa976a12d9
  [3/5 INPUT COINCIDE] IN-C2-COMPUESTO (repo)  sellado=eebadf7f2473266bf87662a444820e40704d66332a5ff128b19640c621af652e  hoy=eebadf7f2473266bf87662a444820e40704d66332a5ff128b19640c621af652e
  [3/5 INPUT COINCIDE] IN-WPROP-ARBITRO (repo)  sellado=b2e636b059538e43c57f4f1a288e028c796ef34965186c5bbb771bea5a462bd3  hoy=b2e636b059538e43c57f4f1a288e028c796ef34965186c5bbb771bea5a462bd3
  [4/5 CONTEXTO] codigo=IDENTICO  commit_informativo=DISTINTO  (FP-358: no gatea)  parametros=IDENTICO  seed=IDENTICO  dependencias=IDENTICO
  CONTEXTO: IDENTICO

VERIFY: REPRODUCE   (CONTEXTO=IDENTICO · RESULTADO=REPRODUCE)
```

## 7 · Módulo de auditoría (afirma sobre México; verbatim del encargo)

El IC que sale de aquí mide ruido muestral de un estimador que supone no-interacción; no mide el error de ese supuesto, que es el que importa en las celdas donde los ejes se refuerzan (mayor edad con baja escolaridad, localidad chica sin cuenta formal). Un IC estrecho no es una celda bien estimada. En ENIF, formalidad quedó NO-EMITIBLE por vivir en el universo de quien trabaja: no se intentó rescatar. El ahorro informal es primero oferta bancaria y choque de ingreso, después conducta. Los ejes son marcadores de estructura, no rasgos culturales; la rejilla no ve región ni condición indígena. Ninguna cifra esperada en este encargo. Peligroso leído simplista: «ya tiene intervalo» como «ya está validado».
