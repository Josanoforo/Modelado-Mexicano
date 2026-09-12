# ENSAFI 2023 · atraso y afrontamiento con diseño · spec v1.0

Congelada por el ACTO `GEN2-ENSAFI-MEDICION-DESCRIPTIVA-CON-DISENO` antes
de calcular errores estándar o intervalos. La extracción de #723 ya hizo
públicos los trece puntos; esta corrida los formaliza, explicita sus
denominadores y añade incertidumbre acreditada. No es un prerregistro ciego ni
una muestra independiente.

## 1. Corpus e identidad

- Microdato: `ensafi2023_bd_csv_zip`, SHA-256
  `c0594079ddf4733d4f574d00f5e84290c62c5330eab0567dd867c26d42fafacd`.
- Tablas: `THOGAR.csv` (hogar) y `TMODULO.csv` (persona elegida de 18 años y
  más); llaves `LLAVEHOG` y `LLAVEMOD`.
- Factores: `FAC_HOG` para hogar y `FAC_ELE` para persona.
- Diseño en ambas tablas: `EST_DIS` (estrato) y `UPM_DIS` (UPM de diseño). La
  unidad se construye como el par `(EST_DIS, UPM_DIS)`, aunque el control del
  corpus indique que `UPM_DIS` no cruza estratos.
- Documentos que fijan lectura: descriptor, cuestionario, diseño muestral y
  presentación manifestados por sus cuatro identidades en `spec.yaml`.

## 2. Estimandos y códigos

Los códigos `1=sí`, `2=no` son respuestas válidas; cualquier otro valor es
desconocido/no válido y sale del denominador, pero se publica su n y masa.

1. `HOG-FORMAL`: `P4_8_1=1` entre `P4_7_1=1` y `P4_8_1∈{1,2}`.
2. `HOG-CAJA-FAMILIA`: análogo con sufijo 2.
3. `HOG-EMPENO`: análogo con sufijo 3.
4. `HOG-PRESTAMISTA`: análogo con sufijo 4.
5. `PER-ATRASO`: `P6_7=1` entre `P6_8∈{1,2,3,4}` y `P6_7∈{1,2}`.
6. a 13. `PER-AFR-k`: `P6_10_k=1` entre `P6_9=2` y
   `P6_10_k∈{1,2}`, para `k=1..8`.

`P6_8=5`, `P6_8=9` y blanco no definen exposición al estimando general de
atraso. Para estrategias, `P6_9=1` está fuera del dominio. Las ocho respuestas
son múltiples: no se suman ni se fuerzan a cerrar en uno. Las cuatro clases de
deuda tampoco son categorías excluyentes. La primera clase es formal
**agregada** (tarjeta o crédito bancario, financiero o de tienda), no producto
exacto.

Por estimando se publican n expuesto, n válido, n y masa desconocida, n y masa
del numerador, masa del denominador, punto, EE, IC95, grados de libertad,
faltantes de diseño/peso y estado de precisión.

## 3. Punto e incertidumbre

El punto es la razón de totales ponderados
`p = sum(w*y*d)/sum(w*d)`. La varianza se fija antes de verla:

- linealización de razón por conglomerado último;
- UPM anidada en estrato mediante `(EST_DIS, UPM_DIS)`;
- muestra completa para dominios: una observación fuera del dominio aporta
  cero al total linealizado, pero no se elimina antes de construir estratos y
  UPM;
- estimador con reposición
  `sum_h m_h/(m_h-1) sum_i (z_hi - mean_h(z))^2`;
- grados de libertad `sum_h max(m_h-1, 0)`;
- IC bilateral 95% con cuantil t de Student y esos grados de libertad,
  truncado a `[0,1]`;
- no se aplica corrección por población finita porque el corpus/documentación
  consumida no publica las fracciones necesarias para esta implementación.

Un estrato singleton se cuenta y no aporta varianza ni grados de libertad; no
se agrupa con otro estrato. Si el denominador es nulo, el punto y la precisión
son `null` con causa. Si falta diseño en alguna fila ponderable, o `p` cae
exactamente en 0/1, el punto se conserva pero EE/IC quedan `null` con causa:
no se sustituyen por cero. Un factor ausente, no finito o no positivo no entra
al punto y se cuenta; si el corpus observado contradice la completitud
documentada, el resultado se reporta en las guardias y no se disimula.

## 4. Contrastes y decisiones

Los trece puntos se comparan a tolerancia absoluta `1e-10` con los CSV de
#723. `PER-ATRASO` debe redondear a 27.3% a un decimal, sólo como contraste con
la presentación oficial. No se ajusta la codificación para alcanzar 27.3%.

Uso permitido: descripción poblacional nacional de prevalencia y respuestas
ante insuficiencia. Prohibido: efecto causal; identificación de BNPL, CAT,
usura o producto exacto; conversión de tasas de hogar en riesgo individual;
suma de clases/estrategias como partición. No se adopta parámetro nuevo y
`NC-0164` conserva el residual causal/producto/costo/fricción.

## 5. Reproducibilidad

`CALC-ENSAFI-DISENO-0001` es una medición GEN2 con trece estimandos nominales,
no trece fuentes ni trece muestras. El medidor es determinista, sin semilla.
Después del sello se ejecutará un control independiente que no importe el
medidor y compare puntos, varianza y denominadores.
