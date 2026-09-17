# ENCIG 2023 · contrato de flujo de `P8_4`

**Estado del contrato:** congelado antes de producir los conteos de este acto.
El análisis es posterior a resultados conocidos: no es un prerregistro ciego ni
una confirmación independiente. Ya se conocían los 123,186 eventos unidos, los
23,100 eventos con `P8_4` observado y el punto condicionado 0.2044306136200499.

## 1. Evidencia documental

Fuentes oficiales verificadas por SHA-256:

| documento | SHA-256 | referencia | hecho acreditado |
|---|---|---|---|
| Cuestionario general ENCIG 2023 | `65000ad38419da504e46b34a0a2426f218d1ba6e604ad37a14762bbd07881e1e` | PDF 20, impresa 20 | `P8_3` pregunta, para 2023, por tres circunstancias: solicitud o intento directo de apropiación por servidor público; petición de tercero/coyote; insinuación o condiciones generadas por servidor público. Códigos 1 Sí, 2 No, 9 No sabe/no responde. Con 2 o 9 en las tres opciones, pasa a sección IX. |
| Cuestionario general ENCIG 2023 | mismo hash | PDF 21, impresa 21 | `P8_4` pregunta **en cuál de los trámites o servicios** se suscitaron las circunstancias anteriores. La cuadrícula distingue el tipo reportado en 6.3a de la cantidad de veces; `P8_5` pregunta en cuántas repeticiones ocurrió el intento o apropiación. |
| Cuestionario general ENCIG 2023 | mismo hash | PDF 21, impresa 21 | `P8_6` pregunta la cantidad aproximada apropiada y ofrece `1 = No le dio nada`, seguido de intervalos de monto. La entrega/pago no queda determinada por `P8_4`. |
| Estructura de la base ENCIG 2023 | `eb89820cd58af0d8799387a376b9e60b062ed59daea74cdbea7ff3b4ee13a906` | PDF 36, impresa 32, cons. 249–251 | Texto y códigos 1/2/9 de `P8_3_1/2/3`. |
| Estructura de la base ENCIG 2023 | mismo hash | PDF 61, impresa 58, cons. 14 | Texto de `P8_4`; códigos `1 = Sí`, `0 = No`, `b = blanco`. |
| Estructura de la base ENCIG 2023 | mismo hash | PDF 62, impresa 59, cons. 18 | `P8_6`: `1 = No le dio nada`, 2–6 intervalos de monto, 7 otros, 9 no sabe/no responde y blanco. |

El descriptor documenta columnas y códigos; el cuestionario acredita el salto.
Ninguna etiqueta del consumidor se usa como evidencia del reactivo.

## 2. Flujo mínimo y unidad

```text
persona con trámites reportados en 6.3a
  └─ P8_3_1/2/3 (circunstancias, nivel persona)
       ├─ alguna = 1 → P8_4: selecciona tipos de trámite
       │                └─ P8_5: cuenta repeticiones dentro del tipo
       │                     └─ P8_6: distingue no entrega de monto
       └─ todas en {2,9} → salta a sección IX; P8_4 queda blanco
```

`sec_8` contiene una marca por `ID_TRA`, que identifica persona × tipo de
trámite; `sec_7` puede contener varias filas-evento para el mismo `ID_TRA`.
La marca `P8_4=1` significa que al menos una ocurrencia del tipo tuvo alguna
circunstancia de `P8_3`. No identifica cuál evento ni autoriza repetir “1”
como desenlace de cada evento. Si el grupo tiene una sola fila-evento, esa
única fila sí queda positiva; si tiene `k>1`, sólo se sabe que el número de
eventos positivos está entre 1 y `k`.

En cambio, `P8_4=0` en un tipo aplicable implica ausencia en todas sus
repeticiones. Si `P8_3_1=P8_3_2=P8_3_3=2`, el salto implica ausencia de las
tres circunstancias en todos los eventos de esa persona. Una combinación con
9 o blanco, sin ningún 1, no permite la misma inferencia.

## 3. Tabla de decisión congelada

El universo de clasificación son todas las filas-evento de `sec_7` con
`FAC_TRA` finito y positivo. Cualquier peso inválido o falla de cardinalidad
detiene la medición; no se descarta silenciosamente. La unión `sec_7 → sec_8`
se acredita por `ID_TRA` y llave de control; la unión a persona es muchos-a-uno
por `(ID_VIV, ID_PER)`. Una duplicación de persona o pérdida de evento detiene
la derivación.

| condición, en orden | categoría exhaustiva | numerador de circunstancia por evento | denominador |
|---|---|---|---|
| código fuera de mapa, o `P8_4` observado sin ningún `P8_3_*=1` | `CONTRADICCION` | desconocido | incluido |
| algún `P8_3_*=1` y `P8_4∈{0,1}` | `RESPUESTA_VALIDA_OBSERVADA` | con 0: conocido negativo; con 1: una positiva si el tipo es único, o restricción 1…k si se repite | incluido |
| algún `P8_3_*=1` y `P8_4` blanco | `RESPUESTA_FALTANTE_APLICABLE` | desconocido | incluido |
| los tres `P8_3_*=2` y `P8_4` blanco | `SALTO_NEGATIVO_LOGICO` | conocido negativo | incluido |
| ningún 1, al menos un 9 o blanco, y `P8_4` blanco | `ELEGIBILIDAD_NO_DETERMINABLE` | desconocido | incluido |
| fila no perteneciente al universo de eventos objetivo | `FUERA_UNIVERSO_NO_APLICA` | no entra | excluido; por construcción se espera cero |

Los blancos nunca se convierten automáticamente en cero. `No aplicable` no
es respuesta negativa. Las contradicciones conservan incertidumbre.

## 4. Pesos, canales y conjunto identificado

- Peso: `FAC_TRA` de cada fila-evento de `sec_7`; nunca `FAC_P18`.
- Duplicados: no se deduplican. Se conservan como eventos, pero la marca de
  tipo no se replica como un desenlace positivo individual.
- Canales: `PRE={1}`, `DIG={3,4,5}`, `OTRO={2,6,7,8,9}` y
  `CANAL_FALTANTE=blanco`. El último sólo es una parte contable, no un canal
  sustantivo.
- Para cada tipo con `P8_4=1`, la masa positiva mínima es el menor `FAC_TRA`
  de sus eventos y la máxima es la suma de sus pesos. A ello se agregan los
  eventos de desenlace completamente desconocido para el límite superior.
- Los límites se rotulan como identificación por flujo, no como intervalo de
  confianza. No se calcula precisión muestral nueva.

## 5. Correspondencia semántica fijada

`P8_4` identifica el tipo donde hubo solicitud, intento o condiciones de
corrupción; no identifica entrega o pago. `P8_6` demuestra documentalmente
que puede existir la situación con “No le dio nada”. Por tanto, cualquiera
que sea la aritmética real:

- `RES-0008` (`paga_mordida`): **NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR**.
- `RES-0007` (`tramite_normal` como complemento de pago):
  **NO-EQUIVALENTE-PARA-ESE-CONSUMIDOR**.

El agregado padre se conserva como descripción de marcas de tipo ponderadas
por eventos. El sucesor, si los datos cierran, será un conjunto identificado
para **circunstancia de solicitud/intento**, no una tasa de pago.
