# endireh-pisos-2016-discriminacion-0001 · sucesor de contrato educativo propuesto

PROPUESTO-POR-EJECUTOR; firma de contenido pendiente. No describe el procedimiento histórico como si ya contuviera estos bins.

# Método: extracción fiel de especificación humana

# CALC-ENDIREH-PISOS-2016-DISCRIMINACION-0001 · ENDIREH 2016, empleo 7.3

Unidad: mujer de 15+; elegibilidad `P7_2=1`, trabajó al menos una semana por salario, pago o ganancia de octubre de 2011 a la entrevista. `P7_2=2`, blanco y salto quedan fuera. Cuestionarios A/B/C, sección VII. `P7_3_1_1` prueba de embarazo para entrar y `P7_3_1_2` para continuar/renovar: 1 sí, 2 no, blanco/9 desconocido. Se miden ambos y unión, positiva si alguna respuesta 1 y negativa solo si ambas son 2.

`P7_3_2_1` despido, `_2` no renovación y `_3` reducción de salario/prestaciones **por embarazarse**: 1 sí, 2 no, 3 **no estuvo embarazada en el periodo**, blanco/9 desconocido. Cada evento usa mujeres con respuesta 1/2 en el ítem; unión positiva si algún 1 y negativa solo con tres 2. El 3 es inelegibilidad estructural, nunca respuesta negativa entre embarazadas. Esta elegibilidad por respuesta no estima directamente la población total de trabajadoras embarazadas si hubo no respuesta.

Factor `FAC_MUJ` positivo sin normalizar, diseño `EST_DIS`/`UPM_DIS`; `TSDem` se une por `ID_MUJ` para edad y `NIV`. Cortes univariados nacional, edad 15–29/30–44/45–59/60+, escolaridad ninguna/básica/media superior/superior, localidad U/C/R, instrumento A1/A2/B1/B2/C1/C2 y entidad 01–32. IC percentil 2.5–97.5 con 200 réplicas de UPM dentro de estrato, conservando UPM de aporte cero; semilla 20260923. Publicable con n conocido ≥100, ≥5 UPM, ancho IC ≤0.20 y CV ≤0.30 cuando p>0. Se suprime punto e IC si falla; soporte y causa permanecen. Réplicas agregadas sin registros individuales.

Manifiesto `endireh_2016_bd_mujeres_endireh2016_sitioinegi_csv`, ZIP SHA256 `02c06ab73a53942ddb575e3e35d8c1dd775406277b74e0605735e3eced4e6f10`; FD incrustado SHA256 `d6b1805e4e0eae0d12df5acd834e4913e59e56dcc101d80d1036535e8c3f1cba`; cuestionario A SHA256 `0e66af1203f5455725c9a453925559b9390cb293e5c73d0956890c2d82834f64`, sección VII p. 11. Import efectivo `numpy==2.3.5`, demás biblioteca estándar; código autocontenido. Ninguna suma con prevalencia laboral 7.9 ni comparación automática con 2021 8.3.

## Mapeo educativo nuevo, explícito y común a este contrato

Fuente: FD2016 incrustado `fd-endireh2016.xlsx`, SHA256 d6b1805e4e0eae0d12df5acd834e4913e59e56dcc101d80d1036535e8c3f1cba, TSDem filas73–85, NIV. Ninguna remisión a hermana. Propuesta de nivel máximo por requisito de acceso: ninguna={0}; básica={1,2,3,5,8}; media superior={4,6}; superior={7,9,10,11}. NIV99/blanco/otros quedan fuera sólo del eje educativo y permanecen en nacional/otros ejes. NIV se parsea como entero decimal (00=0), sin imputación. Estudios técnicos con primaria y normal con primaria/secundaria quedan en básica; técnicos con secundaria en media superior; técnicos con preparatoria en superior. Esta agrupación es una convención propuesta, no una codificación INEGI de nivel homologado.

Identidades nuevas deben usar sufijo EDUCACION-CONTRATO-V2, conservar todas las llaves históricas como testigos y una remisión a este documento/hash. Una reconstrucción de este sucesor no acredita coincidencia histórica; el contrato de bootstrap histórico sigue sujeto a orden de UPM/base de semilla explícitos. No ejecutar bajo este acto.
