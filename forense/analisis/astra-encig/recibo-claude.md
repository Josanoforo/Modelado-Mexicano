# Recibo a Claude · C-ASTRA ENCIG

Estado **EN-RAMA**, pendiente de merge de mesa; `origin/main=619748f5` no contenía estos CALC al último fetch. Plazo vigente por mandato posterior de Jonás: **antes de COMMIT-2** del piloto 5; sustituye «al abrir/en COMMIT-1» de la adenda histórica. Ambos CALC se sellaron y verificaron; la elegibilidad temporal requiere que estén en main antes de ese COMMIT-2. No se encontró la spec del piloto 5 en main ni en los PR abiertos consultados: la compatibilidad y la admisión quedan `PENDIENTE-DE-SPEC`. Este recibo del autor no adjudica por sí solo la etiqueta PROSPECTIVA.

`τ=0.15` y `ω=0.10` son **decisiones ex ante fijas**, no magnitudes aprendidas de persistencia histórica. El modelo usa los residuos históricos para cada celda con esos parámetros fijados. Los intervalos son aproximaciones predictivas condicionadas a marginales 2025 fijos; no hay calibración empírica ni réplicas conjuntas con R. Caja debe fijar **antes de R** cómo calcular la comparación primaria de ΔMAE y su IC, aplicando el mismo tratamiento a los comparadores pertinentes. No debe sortear valores de estos intervalos para simular un bootstrap que no existe.

| CALC | spec MD SHA256 | spec YAML SHA256 | código SHA256 | resultados SHA256 | sello SHA256 | verify/replay |
|---|---|---|---|---|---|---|
| `CALC-ASTRA-ENCIG-EDADXSEXO-0001` | `6086b46b82c34c996c5d71535e8ed0bdb14b857a359becc00620caa21db10ea0` | `c5e72bdc052b14f341c06619daaadb5ca98f730bd69d8eafb648f5c3c788c3a8` | `62069f8945c1ae9a2d3600f28f5b8ca6561d2119244c7c788e5c978c75ab6f52` | `be56470b7c15123c04d571f69a7330ff2deecede4b307cc774a3313963c91cb7` | `6e94e0a11caea6c0bff075021e3e0d090bf44bd43b3e29d480d0ef041b8aee66` | REPRODUCE / append propio |
| `CALC-ASTRA-ENCIG-ESCOLARIDADXSEXO-0001` | `7936304a9ceb72f2c776e21d56366f732d8b8e79eee08079c891fe6410e46db5` | `c9bd4e328c97ebb1f2fc368f7aa95241993c062aff27203ddf33dc5f589275b6` | `62069f8945c1ae9a2d3600f28f5b8ca6561d2119244c7c788e5c978c75ab6f52` | `ebd53cf16c4f920b4c3d439f558cbd5d73e6075e6dd155c88bb9d54787b8057f` | `e0dcdf3d50591cad952976aab3c14bba6eabb8e930eaf149877b5a666aa1e6ad` | REPRODUCE / append propio |

RESULT exactos por celda: cada base en la tabla siguiente tiene los cinco sufijos `-P`, `-IC-LO`, `-IC-HI`, `-NIVEL`, `-TIPO`, todos en los CALC respectivos. Nivel 0.95; tipo `PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS`. `forense/replay-evidencia.tsv` tiene los dos asientos. Commits: freeze `044c3f32`, corrida edad `0ad7f0f8`, corrida escolaridad `20fdc966`, replay y nota `d43ed1c2`. PR listo: https://github.com/Josanoforo/Modelado-Mexicano/pull/1030.

| Cruce | Celda | RESULT base | Punto | IC95 lo | IC95 hi | Tipo |
|---|---|---|---:|---:|---:|---|
| EDADXSEXO | 18-29-1 | `RESULT-ASTRA-ENCIG-EDADXSEXO-18-29-1` | 0.750164710 | 0.702656131 | 0.792326023 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 18-29-2 | `RESULT-ASTRA-ENCIG-EDADXSEXO-18-29-2` | 0.753654576 | 0.706349539 | 0.795544884 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 30-44-1 | `RESULT-ASTRA-ENCIG-EDADXSEXO-30-44-1` | 0.784549876 | 0.742075367 | 0.821710281 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 30-44-2 | `RESULT-ASTRA-ENCIG-EDADXSEXO-30-44-2` | 0.765145379 | 0.720241492 | 0.804795193 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 45-59-1 | `RESULT-ASTRA-ENCIG-EDADXSEXO-45-59-1` | 0.682454177 | 0.629335629 | 0.731211671 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 45-59-2 | `RESULT-ASTRA-ENCIG-EDADXSEXO-45-59-2` | 0.656985004 | 0.602155233 | 0.707923581 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 60-96-1 | `RESULT-ASTRA-ENCIG-EDADXSEXO-60-96-1` | 0.489136584 | 0.430458937 | 0.548115136 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| EDADXSEXO | 60-96-2 | `RESULT-ASTRA-ENCIG-EDADXSEXO-60-96-2` | 0.456315222 | 0.397761759 | 0.516101513 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | HASTA-PRIMARIA-1 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-HASTA-PRIMARIA-1` | 0.387920669 | 0.332200560 | 0.446734613 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | HASTA-PRIMARIA-2 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-HASTA-PRIMARIA-2` | 0.397040571 | 0.341105841 | 0.455802463 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | MEDIA-SUPERIOR-1 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-MEDIA-SUPERIOR-1` | 0.683881815 | 0.630811812 | 0.732557425 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | MEDIA-SUPERIOR-2 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-MEDIA-SUPERIOR-2` | 0.673746125 | 0.619914142 | 0.723356248 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | SECUNDARIA-1 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-SECUNDARIA-1` | 0.572107187 | 0.513379926 | 0.628870616 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | SECUNDARIA-2 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-SECUNDARIA-2` | 0.558353617 | 0.499408868 | 0.615698607 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | SUPERIOR-1 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-SUPERIOR-1` | 0.813580068 | 0.775236765 | 0.846675916 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |
| ESCOLARIDADXSEXO | SUPERIOR-2 | `RESULT-ASTRA-ENCIG-ESCOLARIDADXSEXO-SUPERIOR-2` | 0.811393202 | 0.772516163 | 0.844959586 | PREDICTIVO-CONDICIONAL-MARGINALES-2025-FIJOS |

Contrato de admisibilidad: [admisibilidad.tsv](admisibilidad.tsv) tiene las 16 filas con RESULT, claves, filtros, códigos, marginales, coberturas, hashes y commits. Deben cotejarse con la spec del piloto: claves/orden, unidad trámite, `N_TRA=01`, denominador `P7_3` {01,02,04,05,06}, evento {04,05}, `FAC_TRA`, rangos de edad, agrupación de `NIV`, fuente/precisión marginal, tratamiento de edades faltantes y método de ΔMAE/IC. Edad×sexo usa cobertura **del predictor marginal** edad 0.994308 y sexo 1.0; esa diferencia no redefine automáticamente la población objetivo ni invalida por sí sola la predicción. Caja resolverá la compatibilidad con el estimando. Escolaridad×sexo tiene ambos marginales con cobertura 1.0 y requiere su cotejo independiente. No se cambia una etiqueta de celda ni el estimando para hacerlo pasar. No se abrieron R ni cruces ENCIG 2025.
