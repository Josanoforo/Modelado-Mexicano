# ENFIH 2019 · saldos Afore — pre-registro de `CALC-ENFIH2019-SALDOS-AFORE-0001`

Versión 1.0 · 19 de septiembre de 2026 · COMMIT-1

## Alcance y exposición

Medición descriptiva de hogares. Separa tenencia de cobertura del monto y de
la distribución condicional. No mide saldos individuales, cuentas, aportación
voluntaria, ahorro anual, formalidad, estabilidad laboral ni preferencias.
`CAT_POS` no entra.

No es una corrida ciega. Antes del congelamiento se leyeron
`CALC-ENFIH-0001`, `prereg-caja-ENFIH-AFORE` y la nota
`2026-09-01-MAESTRA33-E18-P3-L1-spec`; ya eran conocidas la tenencia
ponderada 0.538502, 17,765 hogares, 10,197 tenedores sin ponderar, 12,504
filas con `V_AFORE=0`, 5,261 con agregado positivo, 828 valores distintos y
máximo 108,264,000. La acreditación preparatoria de esta sesión también abrió
`P9_10/P9_11` y reveló 1,660 hogares con agregado positivo pero al menos un
tenedor con monto especial. Las reglas siguientes provienen del instrumento
y se congelan pese a esa exposición; el primer resultado del procedimiento
después de COMMIT-1 será el publicado.

La búsqueda por contenido no encontró otro CALC que estime cobertura completa,
cuantiles o concentración del saldo. `CALC-ENFIH-0001` se usa solo como
control de tenencia; sus resultados no se presentan como novedad.

## Fuente, unidad y construcción

- `enfih2019_bd_csv_zip`, SHA-256
  `be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5`.
- `enfih2019_fd_xlsx`, SHA-256
  `326b68b342797de45a7a4eb3dbf04f3790d11035df2611d7f9153d1ae12a48e1`.
- Universo: filas únicas de `TCONCENTRADORA.csv` por
  `FOLIO+VIV_SEL+HOGAR`, con `FAC_HOG` finito y positivo.
- Diseño: `EDIS` y `UPM_DIS` como texto opaco. `FAC_HOG` se toma de
  `TCONCENTRADORA.csv`.
- `C_AFORE`: 0 no tiene, 1 sí tiene. `H_PPAL`: 1 hogar principal.
- `P9_11`: saldo total personal en pesos corrientes hasta el momento de la
  entrevista; 000000000–108264000 es monto conocido, 999999888 no responde y
  999999999 no sabe. La captación fue individual para integrantes de 18 años
  o más. `V_AFORE` es la suma al hogar de montos personales conocidos.
- El cero de `V_AFORE` significa “sin valor específico” y por sí solo mezcla
  no tenencia, saldo declarado cero y desconocimiento. Por eso nunca clasifica
  cobertura sin `C_AFORE` y `TMODULO.P9_11`.
- No hay imputación monetaria oficial acreditada: la validación puede imputar
  “No especificado”, conservado como código especial y luego cero agregado;
  no sustituye un monto. Cada monto positivo o cero válido sí es respuesta
  numérica, pero un total del hogar solo es completo si todos sus tenedores
  tienen respuesta numérica.

El periodo de levantamiento fue 7 de octubre–29 de noviembre de 2019; cada
saldo es un stock al momento de la entrevista, no un mismo día calendario.

## Estados excluyentes

Entre hogares tenedores:

1. `CONOCIDO-CERO`: todos los tenedores responden monto y la suma es cero.
2. `CONOCIDO-POSITIVO`: todos responden monto y la suma es positiva.
3. `DESCONOCIDO-TOTAL`: ningún tenedor aporta monto numérico.
4. `PARCIAL`: conviven al menos un monto numérico y un código especial; aun
   si `V_AFORE>0`, no es total completo.

La distribución principal incluye 1+2. La distribución positiva incluye solo
2. No se imputan 3+4. Se reportan n y masa de todos los estados y las
incoherencias `C_AFORE/V_AFORE` sin corregirlas.

## Estimandos congelados

- Proporciones de tenedor, no tenedor y tenencia desconocida; la primera es
  control contra `CALC-ENFIH-0001`.
- Cobertura del monto completo entre todos los hogares tenedores.
- Entre tenedores con total completo: media y cuantiles p25, p50, p75 y p90.
- Entre tenedores con total completo positivo: media y mediana.
- Media por hogar del universo cubierto: no tenedores entran con cero porque
  `C_AFORE=0` implica ausencia; tenedores desconocidos/parciales salen. Se
  rotula como subconjunto cubierto, no como todos los hogares.
- Entre tenedores con total completo positivo, fracción del saldo ponderado
  en el 10% superior por masa de hogares.
- Sensibilidad única `H_PPAL==1`: cobertura, media y mediana; deltas
  sensibilidad menos principal.

No se estima stock nacional, no se actualizan precios, no se anualiza y no se
recortan extremos.

## Cuantiles, concentración e incertidumbre

Cuantil ponderado = inversa izquierda de la CDF: primer monto cuyo acumulado
alcanza `q*sum(w)`. Los ceros válidos permanecen. Para el 10% superior se
ordena monto descendente; si el umbral corta un empate, todos los hogares del
valor umbral reciben la misma fracción de inclusión, hasta completar
exactamente 10% de la masa.

IC95 percentil mediante 2,000 réplicas, `numpy.PCG64`, semilla 20260919:
UPM con reemplazo dentro de cada EDIS, conservando el número de UPM. El marco
completo se remuestrea y los dominios se estiman con indicadores. Umbral y
cuantiles se recalculan dentro de cada réplica. Los deltas `H_PPAL−principal`
se calculan en la misma réplica, conservando covarianza. Réplicas sin
denominador son `NaN`, nunca cero; se publica el conteo válido.

## Guardias y controles

Se exige llave de hogar y persona única; soporte de `C_AFORE` en {0,1}; mapa
exacto de especiales; igualdad de `C_AFORE` con la tenencia personal agregada;
e igualdad de `V_AFORE` con la suma de montos personales conocidos. Se prueban
estados completos, cuantiles monótonos, concentración [0,1], invariancia ante
escalamiento de pesos y de montos, y empates del umbral. Una media, un cuantil
y la varianza de cobertura se comprobarán independientemente tras la corrida.

## RESULT y reservas

Todos los RESULT se expresan en pesos corrientes de 2019 o proporciones según
su nombre. Ninguno es causal ni adoptable automáticamente. La selección de
quienes conocen todos los saldos del hogar limita cualquier lectura de la
distribución; la mesa puede usarla como descripción del dominio cubierto y
decidir si solicita sensibilidad bajo hipótesis adicionales. No se autoriza
esa imputación en esta corrida.
