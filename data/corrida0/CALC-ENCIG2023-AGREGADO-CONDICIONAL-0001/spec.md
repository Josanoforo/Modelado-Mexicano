# CALC-ENCIG2023-AGREGADO-CONDICIONAL-0001

Spec congelada para el agregado descriptivo condicional de ENCIG 2023. Es un
CALC sucesor independiente de `CALC-ENCIG-2023-0001-v1_1`: reutiliza su
contrato acreditado de archivos, unión y diseño, pero no modifica sus
artefactos ni deriva el nuevo resultado de sus tasas por canal.

## Autoridad y condición de conocimiento

Lo autoriza `GEN2-ENCIG2023-AGREGADO-CONDICIONAL-1`, 16/sep/2026. La medición
no es ciega ni confirmatoria nueva: antes de congelar esta spec ya se conocían
las tasas por canal de la corrida anterior (`PRE=0.13079648341932204`,
`DIG=0.02340709180348316`), su residuo ponderado de canal
(`0.25474042831730237`) y su unión exacta. No se conocían las masas por canal,
el numerador del residuo ni el cociente agregado que esta spec fija.

## Insumo, unidad y unión

- Único payload estadístico: `encig23_base_datos_csv`, SHA-256 completo
  `af733d867a568cbb0dadef4a5a793b02488a71728d1157860f14501f3d4c393d`.
- Miembros autorizados: `encig2023_04_sec_7.csv` y
  `encig2023_05_sec_8.csv`; no se abren los otros cuatro miembros.
- Unidad: evento de trámite, una fila de `sec_7`, sin deduplicar.
- Unión primaria: `ID_TRA`. `ID_TRA` debe ser única en `sec_8`.
- Control: `(ID_VIV, ID_PER, ID_TRA, N_TRA)` debe emparejar exactamente las
  mismas filas de `sec_7`. Una multiplicidad inválida o una discrepancia para
  la medición; no se toma la primera fila ni se deduplica sobre la marcha.
- Ponderador: `FAC_TRA` de `sec_7`, finito y estrictamente positivo.
  `FAC_P18` de `sec_8` se verifica como columna pero no se usa.

## Estimandos fijados

Primario: entre eventos unidos con `P8_4` válido en `{0,1}` y `FAC_TRA`
positivo,

`p = sum(FAC_TRA * I[P8_4=1]) / sum(FAC_TRA)` y
`q = sum(FAC_TRA * I[P8_4=0]) / sum(FAC_TRA)`.

No se restringe `P7_3`. Para reconstruir el agregado se descompone en cuatro
partes mutuamente excluyentes: `PRE={1}`, `DIG={3,4,5}`, `OTRO={2,6,7,8,9}` y
`FALTANTE=blanco`. Un blanco de `P8_4` queda fuera del denominador; nunca se
convierte en cero.

Secundario descriptivo `PREDIG`: el mismo cociente y la misma unidad, limitado
a la unión de `PRE` y `DIG`. Se anuncia aquí antes de abrir el agregado real y
no sustituye al primario según cuál se parezca al prior.

Para ambos universos se emiten `p`, `q`, `n`, masa de denominador y masa de
numerador. Para cada parte de canal se emiten las mismas cantidades, de modo
que la suma de sus masas y conteos reconstruya el primario. `q` se cuenta
directamente sobre `P8_4=0`; su IC se obtiene por la transformación monotónica
`[1-hi_p, 1-lo_p]` y no mediante un segundo bootstrap.

## Coberturas y reserva

Se distinguen:

1. cobertura de unión: filas de `sec_7` emparejadas / filas de `sec_7`, además
   de la versión ponderada sobre pesos positivos;
2. cobertura efectiva del desenlace: eventos con `P8_4` válido / eventos
   emparejados con peso positivo, además de la versión ponderada.

Una unión de 100% no convierte la cobertura observada del desenlace en 100%.
Todos los resultados quedan `CON-RESERVA`: son proporciones condicionales al
flujo que hizo observable `P8_4`, no tasas para toda la población ni para todo
trámite.

## Incertidumbre

Bootstrap de `UPM_DIS` con reemplazo dentro de `EST_DIS`, 2,000 réplicas,
`numpy.PCG64`, semilla `20260915`. En cada réplica se recalcula el cociente
completo del universo correspondiente; no se combinan IC de canales como si
fueran independientes. `EST_DIS` y `UPM_DIS` se leen como texto opaco.

Un estrato con una sola UPM se remuestrea a sí mismo y aporta variación cero.
Se informa su conteo y se rotula el método
`BOOTSTRAP-UPM-EN-ESTRATO-CON-UPM-UNICA`. Esto identifica una limitación del
estimador de varianza; la spec no llama automáticamente al intervalo “cota
inferior”. También se informa el número de réplicas no estimables. Si no hay
información de diseño utilizable, se conserva el punto y el IC queda nulo; no
se fabrica un intervalo binomial.

## Interpretación y no adopción

El resultado es descriptivo y no demuestra que el agregado sea equivalente a
los consumidores actuales sin canal. No enlaza ningún `RESULT` a `milpa`, no
adopta la opción B del modelo y no toca `RES-0001/0002`. La correspondencia
posible queda limitada a una propuesta posterior para `RES-0007/0008`, con
`paga_mordida=p` y `tramite_normal=q` sobre exactamente el mismo denominador,
sujeta a decisión de mesa.
