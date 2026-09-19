# `CALC-ENFIH2019-SALDOS-AFORE-CONCENTRACION-0001` — cara mecánica

Gobierna `forense/prereg-caja/ENFIH2019-SALDOS-AFORE-CONCENTRACION-spec-v1_0.md`.
Es sucesor aditivo de `CALC-ENFIH2019-SALDOS-AFORE-0001`; no lo corrige,
reescribe ni resella.

El dominio principal son todos los hogares tenedores cuyo total es completo:
todos sus tenedores tienen `P9_11` numérico, incluido cero. El 10% superior se
define con la masa ponderada de ese dominio; por tanto los ceros permanecen en
el denominador poblacional. El denominador monetario debe ser positivo.

El dominio comparativo contiene solo totales completos positivos. Ambos
estimandos conservan empates mediante fracción uniforme y usan las mismas
2,000 réplicas de UPM dentro de EDIS para estimar el contraste pareado.
