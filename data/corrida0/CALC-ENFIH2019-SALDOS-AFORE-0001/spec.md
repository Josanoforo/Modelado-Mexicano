# `CALC-ENFIH2019-SALDOS-AFORE-0001` — cara mecánica

Gobierna la especificación humana
`forense/prereg-caja/ENFIH2019-SALDOS-AFORE-spec-v1_0.md`.

Lee `TCONCENTRADORA.csv` y `TMODULO.csv` del mismo payload ENFIH 2019.
La unidad es hogar, la llave es `FOLIO+VIV_SEL+HOGAR`, el ponderador es
`FAC_HOG` de la concentradora y el diseño es `EDIS`/`UPM_DIS`.

`V_AFORE` solo se considera total válido cuando todas las personas tenedoras
del hogar tienen `P9_11` numérico entre 0 y 108264000. Los códigos
999999888/999999999 son no responde/no sabe. Un agregado positivo con algún
código especial es parcial y queda fuera de la distribución principal.

Los cuantiles usan inversa izquierda. La concentración usa exactamente el
10% superior de la masa y reparte uniformemente la fracción de inclusión en
el empate umbral. Los IC95 son percentiles de 2,000 bootstrap de UPM dentro
de EDIS, semilla 20260919. La sensibilidad `H_PPAL=1` comparte réplicas con
el universo principal.
