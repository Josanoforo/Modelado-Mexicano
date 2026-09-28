# Diagnóstico agregado ENOE2024T4

EJECUTADO en CAJA sobre el mismo oro de #1195, ID `enoe_2024_4t_microdatos`, SHA `817f28d20a43fa4fed08195e62df58bf320b31c323a3049fe09b5194a1677305`. Elegibilidad: `data/enoe-olas-elegibles-preparacion-v1_0.tsv`, fila 2024T4, LIBRE-SUJETA-A-CONSULTA; manifiesto sin estado_reserva/retirada y autorización específica P1/P4. No se adquirieron otras olas.

| Marco | Filas | Estratos | UPM anidadas | Singleton | UPM sin dominio |
|---|---:|---:|---:|---:|---:|
| todas | 422408 | 1210 | 21057 | 39 | 0 |
| entrevistadas | 413024 | 1210 | 21056 | 39 | 0 |
| edad | 324241 | 1210 | 21056 | 39 | 0 |
| ocupados | 191738 | 1209 | 20971 | 40 | 85 |
| SEX1 | 111371 | 1209 | 20638 | 41 | 418 |
| SEX2 | 80367 | 1208 | 20038 | 61 | 1018 |

Los 39 estratos singleton de cada sexo son los mismos: unión 39, nunca 78. Son singleton observados en el archivo, no una afirmación de singleton poblacional. Todos ya son singleton en el archivo completo y permanecen tras entrevista y edad. Filtrar al dominio crearía otros singleton; el lector histórico conserva UPM de contribución cero (418 SEX1, 1018 SEX2), y no incurre en ese error.

La clave oficial ENT+EST_D_TRI coincide con la histórica en este oro porque ningún estrato cruza ENT. Ninguna UPM cruza ENT; 532 códigos UPM aparecen en varios estratos, por lo que la llave anidada se conserva como PROPUESTO-POR-EJECUTOR conforme a e/h/i. La repetición no demuestra independencia de unidades físicas: falta crosswalk oficial UPM a unidad primaria física/estrato. 186 estratos cruzan CD_A: esto no justifica agregar CD_A ni es evidencia de colisión; la receta oficial no lo requiere.

El sucesor se ejecutó después de fijar la receta humana (commit 82ea8d23). Reusa original.medir sin modificar sus bytes; verifica igualdad exacta de p0, numerador y denominador con enoe-oro.json. Todos los 39 singleton tienen residuo no cero en ambos grupos. No hay prueba de certeza, y certeza en primera etapa tampoco probaría varianza cero de etapas inferiores.

| Grupo | p0 histórico preservado | Componente parcial m>=2 (no varianza total) | SE total |
|---|---:|---:|---|
| SEX1 | 0.5395718673838116 | 9.012893581062026e-06 | NO IDENTIFICADO |
| SEX2 | 0.5515085438281366 | 1.0741917684764704e-05 | NO IDENTIFICADO |

Solicitud específica: instrucción oficial aplicable a estos estratos ENOE2024T4 que identifique su varianza y el crosswalk de los 532 códigos UPM repetidos entre estratos: indicador y probabilidades de certeza con etapas inferiores, estructura oficial de colapso o réplicas fundamentadas. FAC_TRI, duplicar grupos o reemplazar por Kish no resuelven esta falta. Recomendación: NO-LANZAR.

Pruebas: `python3 tools/familias-2027/enoe_inferencia_1/prueba_sintetica.py` PASS. Cinco casos verifican conservación del cero de dominio, singleton positivo/cero no identificable y certeza explícita en un modelo sintético de una sola etapa (sólo componente, no afirmación sobre el oro).

Reproducción: `python3 tools/familias-2027/enoe_inferencia_1/enoe_diagnostico.py --oro data/raw/enoe_microdatos_post2019/enoe_2024_trim4_csv.zip --salida forense/analisis/familias-2027-enoe-inferencia-1/diagnostico/enoe-auditoria.json`. La salida sólo contiene agregados por estrato, sin claves personales ni códigos UPM.
