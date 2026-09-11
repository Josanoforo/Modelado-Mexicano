# ACTO GEN2-ENVIPE-SERIE-COMPLETA · cierre

Fecha: 10 de septiembre de 2026. Entorno: CAJA (Ubuntu/WSL2), microdato local montado, cero descargas y cero cambios al motor. Encargo archivado en `forense/encargos/cola/2026-09-10-GEN2-POST-685/05-GEN2-ENVIPE-SERIE-COMPLETA.md`.

## Resultado útil

La serie secundaria homologada `p(C1,U1)` queda completa para los **15/15 años-hecho 2010–2024**, sin interpolación. `U1` es delito personal no denunciado con respuesta sustantiva 01–08; `C1=1` para miedo al agresor, temor de extorsión y desconfianza en la autoridad (01/02/06), ponderado por `FAC_DEL`. Es una distribución de motivos declarados entre delitos no denunciados, **no** una tasa bruta de denuncia. La tabla canónica derivada es `data/corrida0/envipe-serie-denuncia-v1_0.tsv`.

| año del hecho | ola | p(C1,U1) | IC95 bootstrap | n U1 |
|---:|---:|---:|---:|---:|
| 2010 | 2011 | 0.293291 | [0.274312, 0.312794] | 13 015 |
| 2011 | 2012 | 0.295572 | [0.278911, 0.312172] | 14 532 |
| 2012 | 2013 | 0.293082 | [0.276097, 0.310009] | 16 411 |
| 2013 | 2014 | 0.320293 | [0.301008, 0.340626] | 16 855 |
| 2014 | 2015 | 0.285205 | [0.267635, 0.305203] | 17 393 |
| 2015 | 2016 | 0.267850 | [0.255042, 0.281045] | 16 242 |
| 2016 | 2017 | 0.256353 | [0.243752, 0.268999] | 18 905 |
| 2017 | 2018 | 0.262355 | [0.245131, 0.280354] | 19 651 |
| 2018 | 2019 | 0.276248 | [0.262948, 0.288910] | 18 981 |
| 2019 | 2020 | 0.236758 | [0.223527, 0.251013] | 16 164 |
| 2020 | 2021 | 0.239890 | [0.228350, 0.251226] | 16 798 |
| 2021 | 2022 | 0.249389 | [0.236995, 0.262793] | 16 241 |
| 2022 | 2023 | 0.243799 | [0.232411, 0.255911] | 16 283 |
| 2023 | 2024 | 0.226945 | [0.213112, 0.241137] | 17 297 |
| 2024 | 2025 | 0.231689 | [0.219191, 0.244462] | 20 225 |

Lectura descriptiva: el máximo puntual ocurre en 2013 (0.3203) y el mínimo en 2023 (0.2269). Entre 2018 y 2019 hay una caída cuyo par de intervalos no se solapa; no se le atribuye causa.

## Fases y evidencia

**Fase 0 — censo.** Los ocho pendientes de `NC-0101` eran realmente nuevos y los otros siete puntos ya estaban sellados. La frase histórica “trece posibles” era una cuenta desactualizada: ocho nuevos + siete existentes producen quince años contiguos. Por ola quedaron identificados payload, hash, miembro, formato, variable, año, unidad, ponderador y diseño.

**Fase 1 — insumos y correspondencia.** Los ocho archivos existen en `data/manifiesto.yaml`, coinciden en bytes con el corpus y son legibles; no fue necesaria adquisición. La ola 2011 usa `BP1_21`, diseño `EST/UPM`, códigos personales 04–14 y residuos 88/98/99. Las siguientes usan `BP1_23`; 2014 usa `EST/UPM` y desde 2016 `EST_DIS/UPM_DIS`. Esta ruptura nominal/residual está marcada, pero los códigos sustantivos de C1 permanecen 01/02/06 frente a 03/04/05/07/08.

**Fase 2 — congelamiento y cálculo.** `forense/prereg-caja/ENVIPE-SERIE-COMPLETA-spec-v1_0.md`, `tools/medidor_envipe_serie_completa.py` y los ocho specs se congelaron en `e65f711`, antes del primer resultado. Cada `CALC-ENVIPE-SERIE-{2011,2014,2016,2017,2018,2019,2020,2022}` pasó `spec-check`, `preflight VERDE`, `run` y `verify REPRODUCE` con `CONTEXTO=IDENTICO`, 40/40 RESULT y hash de entrada coincidente. Los ocho declaran `cuenta_gen2=SI` con cita y objeto explícitos.

**Fase 3 — producto.** `tools/deriva_serie_envipe_completa.py` sólo selecciona resultados sellados y falla ante duplicados o huecos; produjo 15/15 filas contiguas con `calc_id` y `result_id_punto` por ola. No se sustituyó ninguna regla del motor: `tools/ya_medido.py civico.denuncia.miedo_desconfianza` localiza el consumidor vigente y este acto entrega evidencia descriptiva, no una adopción nueva.

**Fase 4 — cierre.** `NC-0087`, `NC-0093` y `NC-0101` cierran por evidencia ejecutada. Los comprobantes `VERIFY-ESTRUCTURADO` se incorporan al registro con lote explícito para no pisar replay ajeno. `NC-0152` conserva como residual la validación por implementación independiente: reproducibilidad no se presenta como independencia.

## Resultado por ola nueva

| ola | payload / SHA256 | formato y miembro | punto p(C1,U1) | sello |
|---:|---|---|---:|---|
| 2011 | `envipe_2011_base_de_datos_envipe_2011_dbf` / `d6c660…` | DBF `tmod_vic.DBF` | 0.293291 | `CALC-ENVIPE-SERIE-2011` |
| 2014 | `envipe_2014_bd_envipe2014_dbf` / `8f1d0e…` | DBF `bd_envipe2014/bd_envipe2014/TMod_Vic.dbf` | 0.320293 | `CALC-ENVIPE-SERIE-2014` |
| 2016 | `envipe_2016_bd_envipe2016_dbf` / `8c9395…` | DBF `TMod_Vic.dbf` | 0.267850 | `CALC-ENVIPE-SERIE-2016` |
| 2017 | `envipe_2017_bd_envipe2017_dbf` / `86df99…` | DBF `BASE_DE_DATOS_ENVIPE_2017_en/TMod_Vic.dbf` | 0.256353 | `CALC-ENVIPE-SERIE-2017` |
| 2018 | `envipe2018_csv` / `aa2799…` | CSV `conjunto_de_datos_tmod_vic_envipe_2018.csv` | 0.262355 | `CALC-ENVIPE-SERIE-2018` |
| 2019 | `envipe2019_csv` / `24bb83…` | CSV `conjunto_de_datos_tmod_vic_envipe_2019.csv` | 0.276248 | `CALC-ENVIPE-SERIE-2019` |
| 2020 | `envipe2020_csv` / `26f468…` | CSV `conjunto_de_datos_tmod_vic_envipe_2020.csv` | 0.236758 | `CALC-ENVIPE-SERIE-2020` |
| 2022 | `envipe2022_csv` / `3a6e0f…` | CSV `conjunto_de_datos_tmod_vic_envipe_2022.csv` | 0.249389 | `CALC-ENVIPE-SERIE-2022` |

No se modificaron los CALC-R congelados, microdatos, consumidores ni el motor.
