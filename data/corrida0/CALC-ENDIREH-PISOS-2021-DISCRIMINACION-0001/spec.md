# CALC-ENDIREH-PISOS-2021-DISCRIMINACION-0001 · ENDIREH 2021, empleo 8.3

El primer resultado que produzca este procedimiento es el que se reporta. GEN2 descriptivo, retrospectivo, adopción NO, origen numérico exclusivo del microdato ENDIREH 2021. No se suma este módulo a violencia laboral interpersonal 8.9.

Unidad: mujer de 15 años o más. Elegibilidad: `P8_2=1`, trabajó al menos una semana por salario, pago o ganancia entre octubre de 2016 y la entrevista. `P8_2=2`, no respuesta y saltos quedan fuera, nunca como discriminación ausente. Cuestionarios A/B/C comparten el texto de 8.3; el archivo es `TB_SEC_VIII.csv`.

`P8_3_1_1`: «¿Le pidieron una prueba de embarazo como requisito para trabajar?»; `P8_3_1_2`: «¿Le pidieron prueba de embarazo como requisito para continuar en su trabajo o renovarle el contrato?». 1 sí, 2 no, 9/blanco desconocido. Se miden ambas y su unión: positivo si cualquier 1; negativo solo si ambas 2.

`P8_3_2_1` a `_3`: «por embarazarse» la despidieron, no renovaron contrato o le bajaron salario/prestaciones. 1 sí, 2 no, 3 **no estuvo embarazada en ese periodo**, 9/blanco desconocido. Cada evento se mide entre embarazadas con respuesta 1/2 al evento; la unión es positiva si alguna respuesta 1 y negativa solo con tres 2. Código 3 no es negativo entre embarazadas; mezclas de 2 y 3 sin positivo son desconocidas. Esta elegibilidad por respuesta al módulo no estima la proporción de todas las trabajadoras embarazadas si hay subcaptura de embarazo.

Factor `FAC_MUJ` sin normalizar, diseño `EST_DIS`/`UPM_DIS`, `TSDem` por `ID_PER` para edad y `NIV`. Cortes univariados: nacional, edad 15–29/30–44/45–59/60+, escolaridad ninguna/básica/media superior/superior, localidad U/C/R, instrumento A1/A2/B1/B2/C1/C2 y entidad 01–32. No hay cruces pequeños ni identificadores públicos. IC percentil 2.5–97.5 con 200 réplicas UPM dentro de estrato, manteniendo UPM sin casos en dominio; semilla 20260923. Publicable solo con n conocido ≥100, ≥5 UPM, ancho IC ≤0.20 y CV ≤0.30 si p>0. En caso contrario se conserva causa y soporte pero no estimación. Se guardan solo réplicas agregadas por celda.

Manifiesto `endireh2021_bd_csv_zip`, SHA recalculado `e4f1e7b1898cc53b3126ed959a9089091afd2ffdd1439911f5419e6c99c6037e`. Descriptor SHA `5c30a3f7f88123ca672f1042ec3b5c37cc1d7989f07fd23ecbf088cca6dda180`; cuestionario A SHA `d2de0f03b8d347b298f7355312953d772a94edf21443bded042dd2a2ec487ae1`; cuestionarios B/C SHA `beffe06a96a58d3b028539f419d28b5d9d325bbd0ee70f576e06e2608d63e689`/`793a87dfa9757b135accd2ed27f75f7b9575e8de24003b63d93cb31d24f277be`. Ninguna inferencia causal ni transición temporal se deriva.

Import efectivo congelado: `numpy==2.3.5`; biblioteca estándar `csv`, `io`, `json`, `zipfile`, `collections`. El medidor es autocontenido.
