# ENDIREH 2003 · dictamen documental previo a cualquier serie

Fuente: `endireh_2003_fd_endireh2003`, descriptor PDF SHA256 recalculado `719da9d636da254732a0be1c31bffd21d06b7609b048f5396e5872c75345daf3`, y cuestionario `C_endireh.pdf` dentro de `endireh_2003_bd_endireh_2003_csv`, SHA256 del miembro `57d05a3fb5c672969810c9a2e3a2f24a961c1f0c7385d73917bd4108795be95a`. Se leyó documentación; **no se abrió ningún registro de microdato 2003**.

| Aspecto | ENDIREH 2003 documentada | ENDIREH 2021 documentada | Dictamen |
|---|---|---|---|
| Elegibilidad | Cuestionario 2003, sección II: mujer de 15+ con pareja **residente en la vivienda** | 2021 FD: mujer de 15+ con A1 pareja residente o A2 pareja ausente temporal, además B/C para otros estados conyugales | No usar población de todas las mujeres ni empalmar denominadores sin restricción explícita a A1. |
| Módulo de pareja | 2003 `nacionalm2`, capítulo VIII, relación actual | 2021 `TB_SEC_XIV`, relación actual o última según A/B/C | Comparar solo A1 y contenido de actos homólogos tras una matriz literal de códigos. |
| Ventana | 2003, capítulo VIII pregunta 1: «Durante los últimos 12 meses» / «en el último año» | 2021 14.1 desde inicio de relación; 14.3 «De octubre de 2020 a la fecha» | La prevalencia de vida 2021 no es comparable con la pregunta 1 de 2003; la ventana reciente requiere verificar fechas de entrevista y actos idénticos. |
| Factor | Descriptor: factor de vivienda, poblador y mujer elegida, en cada archivo; `FAC_PER` figura en el inventario de `nacionalm2` | 2021 `FAC_MUJ` | No reutilizar factor entre estructuras sin equivalencia demostrada. |
| Diseño | El descriptor 2003 leído es una descripción de archivos; no contiene aquí un contrato completo de estratos y UPM equiparable al FD 2021 | 2021 `EST_DIS`, `UPM_DIS`, `FAC_MUJ` | Sin diseño 2003 documentado, no producir IC comparable ni una quinta ola de serie. |

**Dictamen:** 2003 es un levantamiento real con módulo propio, no un formato duplicado ni una quinta medición automática. Queda **fuera de cualquier serie y calibración GEN2** hasta resolver correspondencia de reactivos, códigos, factor y diseño mediante fuente documental primaria. El examen documental no excluye estudiar 2003 por separado si esas piezas se obtienen y se congela una spec distinta. Ni el número de ZIP ni la coincidencia de tema prueban comparabilidad.

## NO-CORRIDO / RESERVAS

Microdato 2003 no abierto ni medido en este dictamen. No se adjudica ausencia de violencia por saltos o no respuesta.

## CONSUMIDO

Descriptor y cuestionario 2003 en el corpus compartido; FD y cuestionario A 2021 de #1082.

## Verificación final de diseño · 23/septiembre/2026

La [publicación primaria de INEGI sobre el diseño de ENDIREH 2003](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/metodologias/est/dm_endireh03.pdf), pp. 2–4 y 8–10, confirma muestra probabilística trietápica, estratificada y por conglomerados; define la UPM y calcula precisión por conglomerados últimos dentro de entidad y estrato. Por tanto el diseño **sí existe**, pero sus identificadores de réplica no están en el microdato público consumido. La salida del primer dictamen se precisa: no es ausencia de diseño de la encuesta, sino ausencia de llave de diseño en el paquete.

Se verificaron los encabezados de los cinco CSV del ZIP del manifiesto `endireh_2003_bd_endireh_2003_csv` (SHA256 del ZIP registrado en manifiesto): `nacionalcv` tiene 30 campos, `nacionalds` 26, `nacionalm1` 204, `nacionalm2` 198 y `nacionalm3` 195. `nacionalm2` contiene los actos de pareja y `FAC_PER`, pero ninguno de los cinco encabezados contiene `UPM`, `EST_DIS`, estrato de selección o un identificador de conglomerado documentado. `LLAVE` figura como llave de registro; ni `FD_ENDIREH2003.pdf`, `fd_exp.xls` ni `leeme.txt` documentan que un tramo de ella sea la UPM o el subestrato. El `leeme.txt` declara que los cinco CSV fueron actualizados con proyecciones posteriores al Conteo 2005 y que llevan factor de expansión; tampoco entrega equivalencia para réplicas. La metodología oficial describe 606 subestratos; no los asigna a cada registro liberado.

**Dictamen de medibilidad bajo este encargo: dependencia externa demostrada.** Es identificable un punto ponderado de mujeres de 15+ con pareja residente en `nacionalm2`, pero no su IC de diseño ni las réplicas agregadas exigidas, y por tanto no se ejecuta ni publica tabla 2003. Pieza exacta requerida: una llave por registro que vincule el microdato distribuido a UPM y estrato (o pesos replicados equivalentes) junto con documentación de uso para el factor actualizado. La tabla eventual será independiente de las otras olas y tendrá ventana anual de relación actual; ninguna prevalencia de vida 2021 ni el 70.1% puede rellenar esta celda. Los otros ámbitos y las mujeres sin pareja residente quedan **excluidos por diseño** del cuestionario 2003. No se abrió ninguna fila de microdato 2003 para este dictamen; solo nombres de columnas y documentos.
