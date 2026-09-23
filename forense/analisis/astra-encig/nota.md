# C-ASTRA ENCIG · nota de ejecución

Estado: **EJECUTADO** en rama `codex/astra-encig-1`; no en main. Base de redacción indicada `43394b06`; rederivado contra `origin/main=34c5d85b28c5f4453f8102b7873f0adea719a1ad` al crear el worktree. Ruta: `/home/pc0/mm-astra-encig-1`. Spec/código congelados en `044c3f32`; corrida edad×sexo en `0ad7f0f8` y escolaridad×sexo en `20fdc966`.

## Procedencia y exposición

LEÍDO: encargo entregado (SHA 55bf8e8da886cfde6eca3d8e4881ae73881de96bf41090226c06e64ac207e261), misión (SHA 949a0f1a9c0054a9a82a802f8a4ce4eadab6d9d9838ecd0f765f69dde7d905bc), AGENTS, spec histórica, dos RESULT históricos, `decisiones.tsv` con lector CSV, manifiesto, metadatos/consumos de marcador, bloque de marginales públicos de milpa y código de mapeo de edad. El archivo `00-ARRANQUE-Y-COORDINACION-ASTRA-1.md` no estuvo localizado en el repo ni entre los adjuntos disponibles; no se afirma leído. No se abrió el payload ENCIG 2025, sus miembros ni sus filas; tampoco R de los cruces objetivo. La exposición previa de esta sesión a edad×sexo y escolaridad×sexo 2025 es sólo a marginales publicados, no a sus cruces. Edad×escolaridad 2025 fue consumido por piloto 3 y se excluyó. Git por sí solo no demuestra ceguera; esta declaración se complementa con las entradas ejecutables y trazas de corrida.

Los dos CALC históricos sellados tienen `SELLO_COINCIDE` y residuos `CAUSA=OK`, `B-VALIDAS=10000` en las 16 celdas usadas. `origen_numerico: MICRODATO` expresa el linaje último de los agregados, no acceso directo de esta corrida al ZIP histórico. `encig2021_csv` y `encig23_base_datos_csv` están identificados por hash en las specs; el campo de licencia de 2023 no se presenta como términos completos leídos aquí.

## Diseño, comprobación y límites

Dos olas (2021/2023), modelo normal con `τ=0.15`, `ω=0.10`; posterior normal de interacción media y componente de innovación 2025. Punto e intervalo 95% predictivo condicional calculados por fórmula cerrada. EE histórico de cada residuo proviene de bootstrap de UPM compartido por términos dentro de ola; la emisión no hace réplicas nuevas ni combina réplicas con el árbitro. Históricos correlacionados entre celdas se tratan en forma marginal por celda, por lo que no hay cobertura conjunta ni IC de ΔMAE. Marginales 2025 se condicionan como fijos, sin EE ni covarianza 2025. Sexo×escolaridad comparte universo público; en edad×sexo, edad cubre 99.4308% y sexo 100%, así que C2 usa marginales con dominios algo distintos. Esa incompatibilidad potencial debe comprobarse frente al piloto. `60+` de la fuente corresponde a 60–96 según código del medidor sellado. El `p` nacional publicado tiene seis decimales.

EJECUTADO: ensayo sintético de transformación para 40 RESULT por cruce, frontera `logit(0)` rechazada, ruta ficticia reservada rechazada; `preflight → run → verify` por CALC, ambos `PRE-FLIGHT: VERDE` (spec NO-EN-MAIN declarado), ambos `VERIFY: REPRODUCE (CONTEXTO=IDENTICO)`. Asiento propio añadido por append a `forense/replay-evidencia.tsv`. No corrí `registro --escribe`, no abrí R ni recalculé microdato histórico. La spec del piloto 5 no está en `origin/main=34c5d85b` ni en PR abiertos vistos al cierre; no invento sus umbrales, λ, candidaturas ni adjudicación. La entrada exige comparación exacta de celdas y método de evaluación por el piloto. No afirmo que C-ASTRA venza a C2 ni que el plazo de admisión se haya cumplido.

## Emisiones selladas

Cada fila da RESULT base; agregue sufijos `-P`, `-IC-LO`, `-IC-HI`, `-NIVEL`, `-TIPO`.

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
