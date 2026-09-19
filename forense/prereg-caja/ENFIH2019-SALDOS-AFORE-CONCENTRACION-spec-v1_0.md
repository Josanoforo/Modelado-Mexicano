# ENFIH 2019 · concentración de saldos Afore — complemento de dominio

Versión 1.0 · 19 de septiembre de 2026 · pre-ejecución

## Alcance, sucesión y exposición

Esta unidad responde una aclaración posterior al sello de
`CALC-ENFIH2019-SALDOS-AFORE-0001`. El encargo original decía “monto válido y
total positivo”; 0001 congeló y publicó legítimamente la concentración entre
totales completos positivos. No se declara erróneo ni se modifica.

La unidad nueva no es ciega. Antes de congelarla se conocen todos los resultados
de 0001, incluida su concentración positiva. Además, antes del COMMIT-1 de 0001
se abrieron `P9_10/P9_11` durante la acreditación preparatoria y se observó que
1,660 hogares tenían `V_AFORE>0` y al menos un tenedor con código especial.
Después de aquel COMMIT-1 se ejecutó el clasificador completo y el resultado
sellado identificó 1,681 hogares parciales en total. Esta cronología impide
afirmar ceguera o congelación anterior a toda apertura de respuestas.

La búsqueda por ID y contenido en CALC, preregistros, análisis, notas y encargos
no encontró otra medición del decil superior cuyo dominio poblacional incluya
los ceros válidos. Se reserva
`CALC-ENFIH2019-SALDOS-AFORE-CONCENTRACION-0001` como sucesor propio.

## Universo y estados

- Fuente: `enfih2019_bd_csv_zip`, identidad ya acreditada por 0001.
- Unidad: hogar único por `FOLIO+VIV_SEL+HOGAR`.
- Marco: todos los hogares con `FAC_HOG` finito y positivo; `EDIS` y `UPM_DIS`
  se conservan como texto.
- Tenedor: `C_AFORE=1`, verificado contra al menos un `P9_10=1`.
- Total completo válido: todos los tenedores del hogar tienen `P9_11` numérico
  entre 0 y 108264000; `V_AFORE` debe ser la suma exacta de esos montos.
- `999999888` (no responde) y `999999999` (no sabe) excluyen el hogar del
  dominio completo. No se imputan desconocidos ni parciales.

## Estimandos congelados

1. Principal: fracción del saldo ponderado captada por el 10% superior por
   masa entre **todos** los tenedores con total completo válido, incluido cero.
2. Comparativo: la misma fracción entre tenedores con total completo positivo,
   con etiqueta separada.
3. Contraste: principal menos comparativo, calculado dentro de cada réplica.
4. Para ambos dominios: n sin ponderar y masa ponderada. Se repite la cobertura
   del total completo solo para hacer explícito el alcance, no como novedad.

Los ceros válidos cuentan en la masa que fija el 10% del dominio principal.
El saldo ponderado agregado que sirve de denominador monetario debe ser
estrictamente positivo; si no, la concentración es no estimable y la corrida
se detiene. No se publica ese agregado como stock nacional.

## Umbral, empates e incertidumbre

Se ordena por saldo descendente. Si el 10% corta un valor empatado, todos los
hogares con ese valor reciben la misma fracción de inclusión hasta completar
exactamente el 10% de masa. La regla es invariante al orden de filas, al
escalamiento común de pesos y al escalamiento monetario positivo.

IC95 percentil con 2,000 réplicas `numpy.PCG64`, semilla 20260919: UPM con
reemplazo dentro de cada EDIS, manteniendo el marco y estimando dominios por
indicadores. El umbral se recalcula en cada réplica. Los tres estimandos usan
réplicas compartidas; una réplica sin denominador poblacional o monetario
positivo es `NaN`, no cero, y se publica el número válido.

## Falsadores y reservas

Control mínimo: para saldos `[0,10]` y pesos `[1,1]`, la concentración entre
todos los válidos es 0.20 y entre positivos 0.10. También se prueban empates,
orden, escalas, pesos de aporte cero y saldo agregado cero no estimable.

La selección por conocimiento del saldo permanece: el resultado no describe a
tenedores parciales o desconocidos y no autoriza imputación ni stock nacional.
No recalcula medias, medianas, perfiles o ejes de 0001. Contador y adopción
permanecen `PENDIENTE-DE-MESA`.
