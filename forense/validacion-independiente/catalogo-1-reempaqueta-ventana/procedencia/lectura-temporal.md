# Correspondencia temporal P1 · preparación no ciega

EJECUTADO: `extrae_mapa.py` recupera 859 llaves exactas desde estimandos históricos y la columna `reserva` del catálogo publicado v1.2. Proyecta exclusivamente semántica y compara conducta/eje/segmento/CALC. Para 2021 comprueba cada ventana contra la tabla799 de #1194, HEAD `df54ad05258ea36c77b9efda44a839e250174d1a`, propuesta abierta; no incorpora sus contratos nuevos. Para 2016 cruza directamente las92 llaves del tar original v2. La posición, el ordinal y cualquier valor observado no intervienen en la correspondencia.

EJECUTADO: 767 identidades2021 (comunitaria100, escolar96, laboral100, nofísica471) y92 de2016. NF histórico tiene590: las119 restantes se enumeran en `excluidas-historico.tsv`; no se reempaquetan en esta subcohorte. Las32 propuestas materiales de1194 tampoco entran al mapa. Los históricos y el primer intento799 permanecen intactos. `mapa-resumen.json` conserva hashes de catálogo, tabla1194 y originales; `mapa-ventanas.tsv` es interfaz P2 por llave/paquete/ventana/estado.

LEÍDO: cuestionarios2021 A/B/C mediante extractos de1194, revisados en `/tmp/reempaqueta-p1`, y cuestionario2016 A disponible en el destino aislado histórico. Hashes, páginas y procedencia en `cuestionarios-revisados.json`. No se copian documentos a la entrada ni se adopta permiso por su coincidencia de hash.

| Módulo | Etiqueta publicada | Encabezado temporal y método histórico |
|---|---|---|
| Escolar2021 | vida | 7.6, durante su vida de estudiante; elegibilidad7.1 |
| Escolar2021 | desde_octubre_2020 | 7.8, últimos doce meses de octubre2020 a fecha; elegibilidad7.2 |
| Laboral2021 | vida | 8.9, en alguno de sus trabajos; elegibilidad8.1 |
| Laboral2021 | desde_octubre_2020 | 8.11, últimos doce meses de octubre2020 a fecha; elegibilidad8.4 |
| Comunitaria2021 | vida | 9.1, alguna vez |
| Comunitaria2021 | desde_octubre_2020 | 9.3, de octubre2020 a fecha |
| Nofísica2021 | vida_relacion | 14.1, desde inicio de relación; B incluye después de separación; C relación actual/última, conforme método |
| Nofísica2021 | desde_octubre_2020 | 14.3, de octubre2020 a fecha |
| Pareja física2016 | vida | 13.1, desde inicio de relación con esposo/pareja; alias histórico vida no significa vida fuera de esa relación |
| Pareja física2016 | desde_octubre_2015 | 13.3, de octubre2015 a fecha; termina entrevista2016 |

Las etiquetas son abreviaturas del periodo del estimando y su universo, no periodos intercambiables entre ámbitos. El método explícito restringe `vida` a escolaridad, trabajos o relación según módulo. Esta lectura no revela contradicción temporal; ninguna regla de universo, edad, escolaridad, IC o ponderación se cambia. No acredita corrección conceptual de todas las demás reglas históricas, ni adopta los métodos propuestos por1194.

LEÍDO: autoridad del mapa = significado publicado firmado (`firma_fp` por fila), con reserva literal y hash. Esto no convierte al catálogo en una especificación humana independiente anterior al productor. Las dos ventanas2016 cubren los mismos46 pares eje/segmento mediante dos llaves distintas y se conservan como identidades separadas. El cuestionario2021 no fundamenta las ventanas2016.

PROPUESTO-POR-EJECUTOR: usar solamente las columnas llave/paquete/ventana en sucesores, conservar la procedencia y esta lectura fuera de entrada, y verificar la autorización documental/raw e aislamiento por P3 antes de cualquier lanzamiento futuro. No se ejecutó validador ni recálculo.
