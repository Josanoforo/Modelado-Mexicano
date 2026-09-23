# CALC-RELEVO-ENCIG23-P83-0001-v1_1 · sucesión congelada

La v1 original produjo `RUN: FALLO` sin abrir filas ni sello: comparó el nombre del miembro ZIP convertido a minúsculas contra una constante que conservaba `A` mayúscula. `v1_1` cambia **solo** la comparación de nombre a minúsculas en ambos operandos. Universo, filtros, punto, fórmula y demás código quedan iguales; el fallo original se conserva en su commit `3461e8f6`. El primer resultado de esta sucesora se reportará cualquiera que sea.

23/sep/2026, ASTRA4-U2. **El primer resultado del medidor congelado se reporta, incluso si no reproduce el prior o no es estimable.** No se adopta ninguna cifra en `milpa/`.

## Identidad y fuentes cotejadas

ENCIG 2023, `encig23_base_datos_csv` (manifiesto: SHA-256 `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`). Se abre únicamente `encig2023_01_sec1_A_3_4_5_8_9_10.csv`, unidad persona informante elegida de 18 años o más, peso `FAC_P18`. Cuestionario oficial `encig23_cuestionario.pdf`, página impresa 20, pregunta 8.3: inciso 1 solicita o intenta apropiarse directamente; inciso 2 es tercero/coyote; inciso 3 es insinuación o condiciones. Cada inciso codifica Sí=1, No=2, NS/NR=9. La instrucción salta a IX si todos son 2 o 9. El descriptor `encig23_estructura_base_datos_pdf` localiza los tres campos en la tabla de persona y `FAC_P18` como ponderador. `P8_4` marca tipo de trámite con circunstancias anteriores; `P8_6` pregunta lo dado. Ninguno de los tres incisos por sí mismo mide pago consumado.

Antes de leer el CSV se conocen: prior ASIGNADO 0.62/0.38 de `RES-0001/0002`, la medición análoga de ENCIG 2025 y las mediciones 2023 de `P8_4`. Esta corrida no es ciega. No se conocen sus frecuencias 2023 de 8.3. La tabla de persona no fue abierta en la medición anterior de canal; esta apertura queda autorizada por el encargo U2 una vez congelado el código.

## Estimandos fijados

Primario `SOLANY`: proporción ponderada de personas con al menos un `1` entre `P8_3_1/2/3`, entre personas con peso finito positivo y los tres valores en `{1,2}`. `SOL1`: proporción ponderada con `P8_3_1=1` entre personas con peso positivo y ese inciso en `{1,2}`. Cada denominador es propio y se informa; no se fuerza equivalencia entre ambos. `NO-SOLANY` es complemento contado de `SOLANY` en su mismo denominador. Valores `9`, `NA`, blancos y códigos inesperados salen del denominador correspondiente y se cuentan; no se convierten a cero. Se publica soporte por inciso, n, masas, punto y diferencia firmada con los dos priors. Sin IC: este primer CALC es una medida de punto y cobertura; no se atribuye precisión muestral. `EST_DIS/UPM_DIS` se leerán para informar completitud de diseño, pero no se utilizarán para fabricar un intervalo.

## Correspondencia fijada antes de medir

`RES-0001/0002` dicen `paga_mordida`/`tramite_normal`, con prior **ASIGNADO** y sin universo declarado. El 8.3 pregunta intento, solicitud o insinuación; aun una coincidencia decimal no identifica pago. Dictamen preespecificado: `NO-EQUIVALENTE-PAGO`; se entrega a mesa como evidencia lateral y no se crea pin. Para `RES-0007/0008`, el CALC de flujo ya sellado `CALC-ENCIG2023-FLUJO-0001` declara `NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR`: es circunstancia, no pago, con repetición de tipo y cobertura parcial. La presente medida no altera ese dictamen.

Guardas: ZIP y columnas exactos; soporte de códigos limitado a `{1,2,9,NA,blanco}`; peso finito positivo; n y masas cierran; ausencia de columna o denominador vacío produce error explícito, sin sustituto. No se lee ni se agrega por evento.
