# ENDUTIH-PISOS · especificación humana v1.0 · ASTRA5 U4

**El primer resultado que produzca este procedimiento es el que se reporta.**
Tres CALC independientes: `CALC-ENDUTIH-PISOS-2023-0001`, `...-2024-0001`,
`...-2025-0001`. `cuenta_gen2: SI`, `adopta: NO`, retrospectiva. El producto
describe personas elegidas de 6 años o más. Una edición no se usa para
predecir otra. Las tres olas comparten población objetivo y preguntas aquí
seleccionadas, pero los cambios de redacción se declaran abajo.

## Archivos, unidad, denominadores y preguntas

Por ola, el FD oficial registrado y el ZIP DBF registrado en el manifiesto son
los únicos inputs externos. Se unen `usuarios` y `usuarios2` por la llave
`UPM,VIV_SEL,HOGAR,NUM_REN` después de exigir unicidad y cobertura 1:1. La
unidad es la persona elegida. Se exige `EDAD>=6`, `FAC_PER>0` finito,
`EST_DIS` y `UPM_DIS` presentes. En 2023 la entidad es `ENT`; en 2024/2025,
`CVE_ENT`. `TLOC`: 1 ≥100 mil, 2 15–99,999, 3 2,500–14,999, 4 <2,500.

| Medida | Texto y referencia FD por cada ola | Universo de respuesta válida | Sí | No | Salto |
| --- | --- | --- | --- | --- | --- |
| internet | `P7_1`: «En los últimos tres meses, ¿ha utilizado internet en este hogar o fuera de él?»; hoja `tic_YYYY_usuarios` (2025 `ti25usu`) | persona 6+ | 1 | 2 | ninguno |
| celular | `P8_1`: «¿Dispone usted de celular?»; hoja `tic_YYYY_usuarios2` (2025 `ti25usu2`) | persona 6+ | 1 | 2 | ninguno |
| actividad_empleo | `P7_10_2`: buscó información sobre empleos/bolsas de trabajo en internet en los últimos tres meses | `P7_1=1` | 1 | 2 | `P7_1=2` |
| actividad_mensajes | `P7_12_3`: envió mensajes instantáneos por internet en los últimos tres meses | `P7_1=1` | 1 | 2 | `P7_1=2` |
| actividad_tramite | `P7_35_4`: realizó trámites del gobierno por internet en los últimos 12 meses | `P7_1=1` | 1 | 2 | `P7_1=2` |
| no_internet_acceso / costo / preferencia | `P7_2`: «¿Por qué no utiliza internet?» | `P7_1=2`, respuesta `P7_2` válida | 1 / 4 / 3 | otro 1–8 | `P7_1=1` |
| no_celular_costo / preferencia / cobertura | `P8_2`: «¿Por qué no dispone de un celular (común o Smartphone)?» | `P8_1=2`, respuesta `P8_2` válida | 1 / 2 / 3 | otro 1–8 | `P8_1=1` |

El FD 2023 escribe «Internet» y menciona Twitter como ejemplo de mensajería;
2024/2025 escriben «internet» y mencionan X. El ítem de trámites usa 12
meses en las tres olas, mientras `P7_1` usa tres meses. La combinación es
condicional sobre usuarios actuales y puede excluir usuarios de hace 4–12
meses. No se interpreta como coerción ni se compara como la misma unidad que
los trámites de ENCIG. `P7_2=1` habla de acceso personal; una razón de hogar
no se traslada a esta persona. La falta de recursos se describe como costo,
sin convertirla en preferencia. Cada razón es categoría de una sola pregunta
de respuesta excluyente; no se suman las tres elegidas como exhaustivas.

Todos los valores fuera de los códigos listados, incluido blanco, son `NR`;
el FD no documenta código explícito `NS` para estos ítems. `SALTO`, `NR`,
`NS`, `SI` y `NO` se cuentan por separado. El denominador de una proporción
es SI+NO dentro del universo indicado; se publica también el conteo de
estados y `n_tabla`. Ningún salto ni blanco entra como no evento.

## Ejes, precisión y salida

Ejes univariados por ola: total; sexo 1/2; edad 6–11, 12–17, 18–29, 30–59,
60+; `TLOC` 1–4; escolaridad `NIVEL` 00–02, 03–05, 06–11; entidad 01–32.
Edad 6–11 sólo existe aquí por diseño ENDUTIH; no se compara directamente
con una tasa MOCIBA 12+. Escolaridad 99 y otros códigos quedan fuera del eje
pero siguen en el total. La celda se suprime antes de publicar su punto si
`n<100` respuestas válidas, sin fusionar ejes ni buscar cortes favorables.

Estimador: razón de sumas de `FAC_PER`, personas que responden Sí sobre
respuestas válidas. IC95: 399 réplicas de UPM con reemplazo dentro de cada
`EST_DIS`, semilla `20260923` con `numpy.PCG64`; estratos de una sola UPM se
tratan como certeza. La misma matriz de réplicas sirve a todos los dominios
y desenlaces de la ola. Si menos de 380 réplicas tienen denominador positivo,
la celda es `NO-ESTIMABLE-REPLICAS`. Intervalo percentil 2.5/97.5. La salida
es una tabla JSON por ola con punto, IC, `n`, estados, peso del denominador,
estratos y UPM, más las réplicas agregadas de los totales (sin identificadores).
Las réplicas son suficientes para estudiar covarianza dentro de una ola; las
tres olas no se tratan como muestras independientes de MOCIBA. No hay IC
predictivo calibrado: sólo tres olas y dos transiciones, sin transición de
evaluación temporal separada del ajuste. Estado `SIN-HISTORIA-PARA-CALIBRAR`.

## Frontera de la medición

Se congela junto con `tools/dominios/endutih/pisos.py` y el lector DBF usado.
Pruebas sintéticas deben demostrar salto, blanco, llave única, supresión y
reproducción antes del primer dato real. No se usa `data/l6-gobierno-digital-
endutih-v1_0.json` como input; es una medición GEN1 de orientación.
