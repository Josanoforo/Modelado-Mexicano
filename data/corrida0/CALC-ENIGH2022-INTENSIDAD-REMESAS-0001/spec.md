# CALC-ENIGH2022-INTENSIDAD-REMESAS-0001

Spec congelada para describir monto e intensidad contable de las remesas entre
hogares receptores de ENIGH 2022. Es sucesora independiente de
`CALC-ENIGH-0001`: reutiliza su identidad de hogar, ponderador y diseño, pero no
modifica al padre ni deriva estos estimandos de su prevalencia.

## Autoridad y condición de conocimiento

Lo autoriza `GEN2-ENIGH2022-INTENSIDAD-REMESAS-1`, lanzado el 16/sep/2026.
No es un estudio ciego ni confirmatorio: antes de congelar se conocía la
prevalencia ponderada del padre (`0.04569409956405095`), pero no se habían
leído para esta corrida los valores reales de `remesas` ni `ing_cor`.

## Identidad documental de monto y periodo

- Payload estadístico único: `enigh2022_nc_csv`, SHA-256
  `3b2b0bc9c95323b470608113d2902ff3a832764367135f136270b4ce092c9e06`.
- Miembro estadístico único: `conjunto_de_datos_concentradohogar_enigh2022_ns/
  conjunto_de_datos/conjunto_de_datos_concentradohogar_enigh2022_ns.csv`.
- El diccionario del mismo ZIP construye `remesas` como suma de
  `ingresos.ing_tri` para P041, “Ingresos provenientes de otros países”.
- El mismo diccionario construye `ing_cor` como
  `ingtrab+rentas+transfer+estim_alqu+otros_ing`; `transfer` incluye
  `remesas`. Por tanto, la documentación acredita a `remesas` como componente
  no negativo de `ing_cor`.
- La descripción oficial de la base declara que todos los ingresos y gastos
  de `concentradohogar` son trimestrales y que `ing_tri` es ingreso trimestral
  normalizado según la decena de levantamiento. La nota técnica expresa los
  resultados 2022 en pesos. La unidad publicada será **pesos de 2022 por
  trimestre normalizado**; no se anualiza ni se hace una deflación propia.

Los dos PDF oficiales se registran como adiciones documentales del manifiesto:
`enigh2022_descripcion_base_pdf` y `enigh2022_nota_tecnica_pdf`. El diccionario
y el metadato internos se identifican por miembro del ZIP estadístico, sin
crear una fuente estadística adicional.

## Universo y dominios

El marco es el universo completo de 90,102 hogares del concentrado, con llave
`folioviv+foliohog`, y conserva todas sus filas para construir los remuestreos.
`est_dis` y `upm` son identidades de texto opacas. `factor` es el ponderador de
hogar, finito y estrictamente positivo.

Un valor ausente, no numérico, no finito o negativo de `remesas` no equivale a
cero: se cuenta y se excluye de los estimandos que requieren `remesas`. El
dominio receptor es `remesas>0` entre filas con ponderador y remesas válidos.
Se informan su n no ponderado, masa expandida y prevalencia sobre el universo
válido, con control contra `CALC-ENIGH-0001`.

El dominio de participación añade `ing_cor>0`, finito y válido. Entre
receptores se cuentan por separado las exclusiones por `ing_cor` ausente/no
finito, igual a cero o negativo, con su masa `factor`. Ninguna se convierte en
cero. El cambio de denominador queda visible.

## Cinco estadísticos principales

Sobre receptores:

1. media ponderada de `remesas`;
2. mediana ponderada de `remesas`, definida como el menor valor observado cuya
   distribución ponderada acumulada alcanza al menos 0.5; ante empate se
   devuelve ese valor menor, sin interpolación.

Sobre el dominio de participación, idéntico para los tres cocientes:

3. participación media por hogar,
   `sum(factor*remesas/ing_cor)/sum(factor)`;
4. participación agregada o razón de masas,
   `sum(factor*remesas)/sum(factor*ing_cor)`;
5. proporción ponderada de hogares con `remesas/ing_cor>=0.5`.

La media de razones y la razón de sumas son estimandos distintos. El umbral
50% es descriptivo y predefinido; no es umbral de pobreza, riesgo o causalidad.

Como la documentación acredita la relación de componente, se verifica
`remesas <= ing_cor + 0.01` pesos en cada fila del dominio. Las excepciones se
cuentan y pesan, no se truncan ni se eliminan. Cualquier excepción deja los
tres cocientes calculados para diagnóstico pero marca el estado
`REPORTADO-CON-INCOMPATIBILIDAD-R-MAYOR-Y`; no se presentan como proporciones
acotadas hasta resolver la incompatibilidad.

## Incertidumbre

Los IC95 prioritarios corresponden a los estadísticos 3, 4 y 5. Se usa
bootstrap de `upm` con reemplazo dentro de `est_dis`, 2,000 réplicas,
`numpy.PCG64`, semilla `20260916`, percentiles 2.5 y 97.5. En cada réplica se
recalculan los tres cocientes completos. Los conglomerados se forman con el
marco completo: las filas fuera del dominio aportan contribuciones cero; no se
filtra primero a receptores.

Una UPM única se remuestrea a sí misma y aporta variación cero. Se informa su
conteo y el método se rotula con esa limitación, sin afirmar que el intervalo
sea una cota inferior garantizada. Si no hay diseño operativo se conservan los
puntos y los IC quedan nulos; no se fabrica un IC binomial.

## Interpretación y límites

La participación es contable y transversal. No identifica dependencia causal,
pérdida contrafactual de ingreso, volatilidad, respuesta a choques, ausencia de
Estado ni efecto protector de la familia. No cambia el parámetro ni el tier de
`familia.seguro.volatilidad_ausencia_estado` (R5.1), no enlaza resultados a
`milpa` y no constituye una fuente independiente respecto del mismo microdato
usado por el padre.
