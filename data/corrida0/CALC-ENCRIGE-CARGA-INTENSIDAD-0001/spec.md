# CALC-ENCRIGE-CARGA-INTENSIDAD-0001

Spec sucesora fijada antes de ejecutar la derivación. Consume exclusivamente
el CSV publicado por `CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001` y verifica su
cadena sellada; no abre microdatos, no relanza al padre y no agrega información
muestral independiente.

## Estimandos descriptivos

Para cada dominio `s`, `N_s` es la masa de empresas expuestas, `A_s` la masa
de empresas con al menos un acto y `T_s` el recuento expandido de trámites o
inspecciones con experiencia de corrupción. Se calculan `p_s=A_s/N_s`,
`m_s=T_s/N_s` y, si `A_s>0`, `r_s=T_s/A_s`, verificando `m_s=p_s*r_s`.

Las cuatro categorías de tamaño —sin el nacional— producen participaciones en
`ΣN`, `ΣA` y `ΣT`. Pequeña, Mediana y Grande se contrastan con Micro mediante
la descomposición simétrica fijada en
`forense/analisis/encrige-carga-intensidad-1/spec.md`.

## Semántica y precisión

El padre acredita la misma unidad empresa, periodo enero–entrevista 2020 y
denominador expuesto para ambos indicadores. `T` es el total de trámites o
inspecciones con experiencia de corrupción. Por ello `r` es una razón de
recuentos por empresa afectada, no reincidencia longitudinal, riesgo por
interacción ni probabilidad. `m` y `r` pueden superar uno.

Se usan `Decimal` y los absolutos publicados. La tolerancia de reconstrucción
nacional se fijó en `0.0003` unidades expandidas por el grano de cuatro
decimales; la de razones, identidades y descomposición es `1e-12`. Si `A=0`,
`r` es no estimable; denominadores incompatibles o `T<A` detienen la corrida.

No hay `n` muestral, EE, CV o IC utilizables. El resultado es descriptivo y
exploratorio: no acredita significancia, causalidad, tendencia, intervención
óptima, validación adicional del motor ni transferencia a personas.
