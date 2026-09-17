# CALC-ENCIG2023-FLUJO-0001

Contrato ejecutable sucesor del agregado condicional de `P8_4`. Fue fijado
después de conocer los resultados del padre, pero antes de abrir en este acto
las columnas reales `P8_3_1/2/3`; no es ciego ni independiente.

## Insumos y lectura

Se usa `encig23_base_datos_csv`, SHA-256
`af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`.
Se leen exclusivamente:

- `sec_7`: `ID_VIV`, `ID_PER`, `ID_TRA`, `N_TRA`, `P7_3`, `FAC_TRA`;
- `sec_8`: `ID_VIV`, `ID_PER`, `ID_TRA`, `N_TRA`, `P8_4`;
- tabla persona: `ID_VIV`, `ID_PER`, `P8_3_1`, `P8_3_2`, `P8_3_3`.

La tabla persona ya fue abierta y usada en actos integrados anteriores; no hay
reserva científica vigente específica sobre estas cinco columnas. Ninguna
otra columna del miembro se abre.

## Contrato

La clasificación y su orden están fijados en
`forense/analisis/encig2023-flujo-estimando-1/01-contrato-flujo-evidencia.md`.
Las seis categorías son mutuamente excluyentes y exhaustivas. Toda fila de
`sec_7` debe emparejar una fila de tipo en `sec_8` y una sola persona; no se
tolera multiplicación. Todo `FAC_TRA` debe ser finito y positivo.

El punto del padre se reproduce sin reinterpretarlo: masa de `P8_4=1` entre
masa con `P8_4∈{0,1}`. Después se separa el desenlace individual:

- negativo conocido: `P8_4=0` aplicable o salto con los tres `P8_3_*=2`;
- positivo conocido: `P8_4=1` y un único evento en el `ID_TRA`;
- desconocido individual: todo lo demás, incluidos los tipos positivos con
  más de un evento.

Para cada `ID_TRA` aplicable con `P8_4=1`, al menos un evento es positivo. El
límite inferior ponderado suma el menor `FAC_TRA` de cada grupo positivo; el
superior es la masa del universo menos la masa negativa conocida. Estos
límites describen identificación lógica, no precisión muestral.

## Decisión preespecificada

Aunque el conjunto cierre, su desenlace es circunstancia de
solicitud/intento, no pago. Los dos dictámenes para `RES-0007/0008` serán
`NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR`. No se calcula `P8_6`, no se produce IC
nuevo y no se adopta ningún resultado en `milpa`.
