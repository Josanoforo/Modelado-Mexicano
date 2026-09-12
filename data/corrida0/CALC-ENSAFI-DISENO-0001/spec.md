# `CALC-ENSAFI-DISENO-0001` · ENSAFI 2023 con diseño

Cara humana de `spec.yaml`. Gobierna el prerregistro
`forense/prereg-caja/ENSAFI-ATRASO-AFRONTAMIENTO-DISENO-spec-v1_0.md`.

Mide cuatro tasas de atraso de hogar por clase amplia, una tasa general de
atraso de persona y ocho estrategias múltiples ante insuficiencia de ingreso.
Los puntos usan `FAC_HOG` o `FAC_ELE`; los errores estándar usan
`EST_DIS`/`UPM_DIS`, linealización de razón sobre la muestra completa y un
IC95 t con grados de libertad de diseño.

Publica expuestos, respuestas válidas, desconocidos y su masa, numerador y
denominador ponderados, punto, EE/IC95, grados de libertad y guardias de
diseño. No suma clases ni estrategias y no interpreta asociaciones como
efectos causales. `P6_7` no identifica producto ni ventana temporal; la clase
formal de hogar agrega banco, financiera y tienda.

Los puntos conocidos de #723 son contraste de replay; 27.3% es contraste de
redondeo oficial. La incertidumbre es la extensión nueva y se calcula por
primera vez después de congelar esta especificación. No adopta N34/R1.7 ni
cierra el residual causal de `NC-0164`.
