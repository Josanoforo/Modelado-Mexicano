# Índice local · ASTRA6-C3-SOCIAL-1

Corte fijo `2c646cba93eebc9189a8135a5369bb45e8d29b89`. Tres reports completos, 604 registros de afirmación, 113 filas del mapa cubiertas y 139 registros cuantitativos propios/externos. Un registro no equivale a un fenómeno independiente: el mapa y la lectura completa del v1 pueden referir la misma proposición. Cero mediciones y cero adopciones nuevas.

| Report | Afirmaciones | Mapa | CONFIRMA | MATIZA | ROMPE | SIN-CIFRA | Cifras | Fuentes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [confianza](../../../../corpus/reports-v2/Confianza_y_Desconfianza_en_México__Anatomía_Psicológica_de_una_Sociedad_Dual.md) | 357 | 33 | 0 | 150 | 6 | 201 | 45 | 7 |
| [capital](../../../../corpus/reports-v2/Non-Family_Social_Capital_in_Mexico__Cooperation__Trust__and_Collective_Action_Beyond_Kinship.md) | 88 | 42 | 0 | 5 | 0 | 83 | 32 | 7 |
| [religion](../../../../corpus/reports-v2/Religiosidad_y_Psicología_del_Mexicano_Contemporáneo__Moral__Afrontamiento__Consumo_e_Identidad_en_Transformación.md) | 159 | 38 | 2 | 106 | 4 | 47 | 62 | 15 |

Cada report tiene tablas `*-afirmaciones.json/.tsv`, cobertura por líneas `*-cobertura.json`, cifras `*-cifras.json`, fuentes `*-fuentes.json`, reglas propuestas y revisión dirigida. Las exclusiones de cobertura son explícitas; SIN-CIFRA conserva su razón y no significa refutación.

## Uso y comprobación

`python3 forense/analisis/reports-v2/social-1/verifica_lote.py --prueba-mutacion`

El control verifica igualdad de valores y hashes sellados, firmas de adopción, cobertura del mapa y de líneas no vacías, fuentes y vínculo de cifras al report. Las unidades incluidas agrupan proposiciones según su tabla; la cobertura de líneas no decide exhaustividad semántica ni calidad de las citas. Las revisiones `*-revision.json` y los argumentos individuales documentan esa revisión humana.

Las vistas de RESULT están rezagadas para los pisos recientes: se intentó `tools/consulta.py` y se conservó el resultado de consulta; la extracción puntual del JSON sellado usa hash, clave y firma, sin modificar derivados. C1 sigue pendiente y no se declara validación independiente a partir del replay.

[Hoja de reglas](social-hoja-reglas.md) · [Recibo solicitado a Claude](recibo-para-claude.md) · [Corte y hashes](social-corte.json).
