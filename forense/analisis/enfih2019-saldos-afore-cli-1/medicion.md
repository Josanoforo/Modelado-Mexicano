# ENFIH 2019: saldos Afore de los hogares

`CALC-ENFIH2019-SALDOS-AFORE-0001` · pesos corrientes · stock al momento de
la entrevista (7/oct–29/nov/2019)

## Resultado sustantivo

Saber únicamente que un hogar tiene Afore deja sin identificar la mayor parte
de la distribución monetaria: 53.85% de los hogares tenía al menos una cuenta,
pero solo 37.16% de la masa de tenedores aportó un total completo del hogar
(IC95 de diseño 35.85–38.41%). La distribución monetaria siguiente describe
ese dominio cubierto, no a todos los tenedores.

Entre tenedores con total completo, el saldo medio fue **$180,198**, mientras
la mediana fue **$71,000**. La media equivale a 2.54 medianas y su IC es mucho
más ancho: el extremo superior domina el promedio. El 10% superior por masa
de hogares concentró **58.45%** del saldo ponderado observado (IC95
43.33–69.64%). Esto es concentración dentro del dominio cubierto, no riqueza
patrimonial total ni concentración de todos los hogares.

## Cobertura y estados monetarios

| Estado | n hogares | Masa expandida | % de todos los hogares | % de tenedores |
|---|---:|---:|---:|---:|
| No tenedor | 7,568 | 16,911,436 | 46.15% | — |
| Tenedor, total conocido cero | 36 | 61,135 | 0.17% | 0.31% |
| Tenedor, total conocido positivo | 3,601 | 7,271,752 | 19.84% | 36.85% |
| Tenedor, totalmente desconocido | 4,879 | 9,304,427 | 25.39% | 47.15% |
| Tenedor, total parcial | 1,681 | 3,095,930 | 8.45% | 15.69% |

Los 1,681 parciales tienen al menos una respuesta monetaria y al menos un
`no sabe/no responde`: aunque `V_AFORE` pueda ser positivo, no es el total del
hogar. La suma de desconocido total y parcial explica por qué la cobertura
completa es 37.16%, no el 53.85% que resulta de confundir saldo positivo con
tenencia. No hubo no tenedores con saldo positivo. Hubo 4,936 tenedores con
`V_AFORE=0`; solo 36 son ceros numéricos completos, el resto contiene
desconocimiento.

## Nivel y distribución condicional

| Estimando | Punto | IC95 de diseño | Universo |
|---|---:|---:|---|
| Cobertura de monto completo | 37.16% | 35.85–38.41% | Todos los tenedores |
| Media | $180,198 | $131,490–$246,710 | Tenedores con total completo |
| p25 | $25,000 | $22,000–$29,000 | idem |
| Mediana | $71,000 | $69,000–$80,000 | idem |
| p75 | $160,000 | $150,000–$172,000 | idem |
| p90 | $309,000 | $300,000–$340,000 | idem |
| Media, saldos positivos | $181,713 | $132,596–$248,865 | Tenedores con total completo positivo |
| Mediana, saldos positivos | $72,000 | $70,000–$80,000 | idem |
| Media por hogar cubierto | $54,502 | $39,520–$75,067 | No tenedores con cero + tenedores completos |
| Fracción del saldo del 10% superior | 58.45% | 43.33–69.64% | Tenedores completos positivos |

La media por hogar cubierto usa cero únicamente para no tenedores y excluye
tenedores parciales/desconocidos. Su universo son 11,205 hogares sin ponderar
y 24,244,323 hogares expandidos; no se rotula media de todos los hogares.

## Sensibilidad de hogar principal

| Estimando | Principal | `H_PPAL=1` | Delta sensibilidad−principal (IC95 compartido) |
|---|---:|---:|---:|
| Cobertura | 37.160% | 37.092% | −0.068 pp (−0.233, 0.090 pp) |
| Media | $180,198 | $182,221 | +$2,023 ($804–$3,656) |
| Mediana | $71,000 | $71,788 | +$788 (−$1,000–$2,000) |

La restricción a hogar principal casi no cambia cobertura ni mediana. La media
sube alrededor de 1.1%; el contraste usa las mismas réplicas, no trata los dos
universos como muestras independientes. La lectura general no depende de esta
sensibilidad.

## RESULT → significado → universo

| RESULT o familia | Significado | Universo |
|---|---|---|
| `P-TENEDOR`, `P-NO-TENEDOR`, `P-TENENCIA-DESCONOCIDA` | Cobertura de cuentas; control, no novedad | 17,765 hogares con peso válido |
| `DELTA-TENENCIA-VS-CALC-ENFIH-0001` | Diferencia contra el control sellado; fue exactamente 0 | Mismo universo |
| `ESTADOS-JSON` | n, masa y proporción de cinco estados excluyentes | Mismo universo |
| `COHERENCIA-JSON` | Cruces tenencia/agregado y presencia de códigos especiales | Mismo universo |
| `COBERTURA-MONTO` y `-IC95-*` | Fracción con total completo | Todos los tenedores |
| `MEDIA`, `P25`, `MEDIANA`, `P75`, `P90` y `-IC95-*` | Distribución del saldo total completo | Tenedores completos, n=3,637; masa=7,332,887 |
| `POSITIVO-MEDIA`, `POSITIVO-MEDIANA` y `-IC95-*` | Distribución sin ceros válidos | Tenedores completos positivos, n=3,601; masa=7,271,752 |
| `MEDIA-UNIVERSO-CUBIERTO` y `-IC95-*` | Cero para no tenedor, monto para tenedor completo | Subconjunto cubierto, no todos los hogares |
| `TOP10-FRACCION-SALDO` y `-IC95-*` | Fracción del saldo observado en 10% superior por masa | Tenedores completos positivos |
| `HPPAL-*`, `DELTA-HPPAL-*` y `-IC95-*` | Sensibilidad y contraste pareado | Dominio anterior restringido a `H_PPAL=1` |
| `REPLICAS-VALIDAS-JSON`, `METODO-IC` | Diagnóstico del bootstrap | 2,000/2,000 válidas en cada estimando |
| `CONTROL-*` | Cuantiles monótonos y concentración en [0,1] | Resultados publicados |

Todos los nombres completos llevan el prefijo
`RESULT-ENFIH2019-SALDOS-AFORE-`.

## Método y comprobaciones

Los intervalos son percentiles de 2,000 réplicas que remuestrean UPM dentro
de EDIS y recalculan dominios, cuantiles y umbral superior. La semilla es
20260919. Los cuantiles son la inversa izquierda de la CDF ponderada; los
empates del umbral del 10% reciben una fracción uniforme.

Una implementación independiente, que no importó el medidor, reprodujo la
media `$180197.67951517596`, la mediana `$71000` y el IC95 de cobertura
`[0.358490451722213, 0.38410298125059866]`; la desviación estándar de sus
réplicas de cobertura fue 0.00660142. Las 65 salidas reprodujeron con delta
cero en `corrida0 verify`; sello SHA-256
`2e87a67eb4e349839adaf09ff7ac5876722be7bf7f34246a162baf8c0c4cf4b5`.

## Interpretación y reservas

El saldo añade una dimensión que la tenencia sola no contiene: revela una
distribución muy asimétrica y concentrada. Pero esa ganancia informativa está
condicionada por selección: 62.84% de la masa de tenedores no tiene un total
completo. Sin una hipótesis adicional sobre esos hogares no se puede inferir
la distribución de todos los tenedores ni un stock nacional.

No hay evidencia aquí de planeación, preferencias, aportaciones voluntarias,
flujo anual de ahorro, formalidad o estabilidad laboral. No se construye serie
temporal con una ola, no se actualizan pesos de 2019 y no se usa `CAT_POS`
como formalidad.
