# ENFIH 2019: cobertura y saldos Afore por CAT_POS — sucesora v1.1

Sucesora de v1.0 / `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001`: su sello y
sus bytes no se editan. `CALC-...-0002` completa, sin cambiar estimandos
puntuales, precisión para estados monetarios, p25/p75/p90 y positivos. Toda
réplica con dominio vacío o denominador cero hace su IC `null`; nunca se
descarta para calcular un percentil con las restantes. El residuo vacío se
publica con `null` y causa explícita. Añade reconstrucción de estados y un
cálculo independiente de cobertura/media CAT_POS=1.

Identidad: `CALC-ENFIH2019-COBERTURA-SALDOS-CATPOS-0001`.

## Pregunta y límites

Describe, por la **Categoría de posición en el trabajo de la persona de
referencia** (`CAT_POS`), la cobertura de saldo Afore completo y la
distribución condicional de sus totales de hogar. `CAT_POS` no mide
formalidad, ingreso, conducta individual, planeación ni causalidad.

La unidad es hogar (`FOLIO+VIV_SEL+HOGAR`). Se usa `FAC_HOG` de
`TCONCENTRADORA.csv`; `EDIS` y `UPM_DIS` son llaves opacas del diseño. El
marco son hogares únicos con peso finito positivo, sin filtrar antes de formar
réplicas por categoría ni por estado de saldo.

## Variables acreditadas y clasificación

El FD describe `CAT_POS` como “Categoría de posición en el trabajo”; sus
códigos nativos son 0 persona no ocupada, 1 empleado(a) u obrero(a), 2
jornalero(a) o peón(a), 3 patrón(a) o empleador(a), 4 trabajador(a) por su
cuenta y 5 trabajador(a) familiar sin pago. Blanco/fuera de ese catálogo se
conserva como `DESCONOCIDO`, separado de los contrastes sustantivos.

`C_AFORE` se comprueba contra `P9_10==1`. Para tenedores, el total es completo
solo cuando todos sus `P9_11` son numéricos en [0,108264000]. Los códigos
999999888 y 999999999 son desconocimiento, no pesos. Así se particiona en
`COMPLETO-CERO`, `COMPLETO-POSITIVO`, `PARCIAL` y `DESCONOCIDO-TOTAL`.
`V_AFORE` se verifica contra la suma de importes numéricos personales y se
interpreta como pesos corrientes al momento de entrevista ENFIH 2019.

## Estimandos

Por cada categoría nativa y `DESCONOCIDO`: n y masa del marco, tenencia de
control, y entre tenedores n/masa/proporción de los cuatro estados, con
denominador todos los tenedores. Entre completos: media ponderada, p25,
mediana, p75 y p90 por inversa izquierda; y media/mediana de positivos como
sensibilidad. Ceros completos quedan en la distribución principal.

Para cada categoría nativa, el contraste es categoría menos el resto de las
categorías nativas (excluye `DESCONOCIDO` en ambos lados): cobertura completa,
media y mediana. Las réplicas se comparten. Los intervalos son descriptivos,
sin ajuste por multiplicidad; no establecen rankings concluyentes.

## Precisión y controles

Bootstrap de UPM con reemplazo dentro de `EDIS`, 2,000 réplicas,
`numpy.PCG64(20260919)`. Un estrato de UPM única se remuestrea a sí mismo;
la precisión es un límite inferior. Réplicas de dominio vacío dan precisión no
disponible para ese estimando, nunca cero.

Controles: los grupos más residuo reconstruyen n/masa/estados nacionales, el
agregado reproduce cobertura/media/mediana de
`CALC-ENFIH2019-SALDOS-AFORE-0001`, los complementos no se solapan, y las
proporciones y la media no cambian al escalar todos los pesos.

## Exposición previa

No es una medición ciega: ya se conocían la tenencia por `CAT_POS`, la
cobertura completa nacional 37.16%, y los resultados nacionales de saldos de
los CALC antecedentes. La desagregación monetaria y sus contrastes no se
usaron como objetivo de ajuste.
