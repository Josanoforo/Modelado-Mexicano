# PISOS ENCIG 2023 · especificación congelada v1.0

Congelada el 19/sep/2026 antes de abrir respuestas. Mide
`p_2023(gobierno_digital_util_sin_coercion | sexo, edad, escolaridad)` para el
destino ENCIG 2025, sin abrir éste. Unidad: evento de trámite de sec_7 con
`N_TRA=01`; el desenlace y sus códigos se verifican contra el cuestionario y
catálogo 2023 antes de medir. La fila de evento se une por `ID_PER` a residentes
para sexo, edad y `NIV`; el join debe ser uno-a-uno y conservar el conteo.

Ponderador, estrato y UPM se toman del lado de evento (`FAC_TRA`, `EST_DIS`,
`UPM_DIS`), no del ponderador de persona. Categorías: sexo hombre/mujer,
edad 18--29/30--44/45--59/60+, y escolaridad hasta primaria/secundaria/media
superior/superior. Cualquier discrepancia del texto de P7.3, su universo o el
mapa frente al estimando de 2025 deja la celda `NO-CONSTRUIBLE`.

El IC95 es bootstrap de diseño (10 000, seed 42, UPM con reemplazo dentro de
estrato); estratos de UPM única no se colapsan. No es un IC predictivo ni una
evaluación contra 2025.
