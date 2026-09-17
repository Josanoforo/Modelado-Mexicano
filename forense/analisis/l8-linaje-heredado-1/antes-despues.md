# GEN2-L8-LINAJE-HEREDADO-1 · evidencia antes/después

Fecha de ejecución: 17 de septiembre de 2026 UTC (16 de septiembre en
America/Mexico_City). Base inicial consultada: `origin/main @
4fff914f286021574ac0897273ee0e6971b38f04`; rama sincronizada antes del commit
con `origin/main @ e4f5f771b7fd9bccc88d3b6c30d0e5362b0e52a5`.

## Identidad y procedencia verificadas

- `data/l8-resultados-tipo-boleta-v1_0.json` conserva SHA-256
  `30f3e16dd6ea770ad72ab957547159c5427788a97a24a0ef30f2765752ef8f99`,
  igual al declarado por `IN-L8-JSON` en la spec sellada.
- El artefacto aparece por primera vez en el commit histórico
  `1c33155d53bdd6fe111b23907945d9c46021087f`, fechado
  `2026-09-02T19:05:06-06:00` y titulado `MAESTRA35-L8 COMMIT-2: resultados
  -- ACOTADA`.
- `forense/notas/2026-09-02-MAESTRA35-L8-spec.md:215-217` identifica como
  productor `tools/l8_amplia_tipo_boleta.py --json` y como salida el JSON
  anterior. El commit de congelamiento inmediatamente previo
  (`cbe467674a74b15b5129424c1724f988e6832ee4`) declara incluso que esa salida
  ya se había observado antes de congelar la spec histórica.
- `CALC-L8-CONVERSION-0001` es una derivación posterior y determinista de ese
  JSON. Su spec GEN2 y su veredicto `REPRODUCE` acreditan reproducción, no una
  fuente numérica independiente ni nueva.

La evidencia confirma por tanto `HEREDADO` para esa identidad exacta. No
acredita `data/` como familia, archivos `.json` en general ni nombres
parecidos.

## Tres resultados: origen, valor y aptitud

| RESULT | Origen antes | Origen después | Valor antes | Valor después | Sello | MEDICION-GEN2 | CONFIRMACION-INDEPENDIENTE | HISTORICO / BASELINE / DESCRIPTIVO / CALIBRACION |
| --- | --- | --- | ---: | ---: | --- | --- | --- | --- |
| `RESULT-L8CONV-A-P-MINIMO` | `INDETERMINADO` | `HEREDADO` | 0.345267 | 0.345267 | `COINCIDE` | `NO-APTA` | `NO-APTA` | `APTA-CON-HERENCIA-DECLARADA` |
| `RESULT-L8CONV-A-P-MAXIMO` | `INDETERMINADO` | `HEREDADO` | 0.750567 | 0.750567 | `COINCIDE` | `NO-APTA` | `NO-APTA` | `APTA-CON-HERENCIA-DECLARADA` |
| `RESULT-L8CONV-A-P-MEDIA` | `INDETERMINADO` | `HEREDADO` | 0.619867 | 0.619867 | `COINCIDE` | `NO-APTA` | `NO-APTA` | `APTA-CON-HERENCIA-DECLARADA` |

La tabla de aptitud proviene de `milpa.src.linaje.aptitud_para_uso`; no es una
tabla inventada para este acto. `APTA-CON-HERENCIA-DECLARADA` sólo califica
linaje: no acredita compatibilidad del estimando, validez causal o decisión de
consumo.

## Contadores separados de la clasificación

| Contador derivado por `corrida0.py status --json` | Antes | Después | Lectura |
| --- | ---: | ---: | --- |
| `corredores_envueltos_legacy` | 21 | 22 | La CALC L8 queda reconocida como envoltura de legado. |
| `dependencias_numericas_legacy_activas` | 183 | 183 | No hubo cita/adopción; reclasificar no elimina dependencias. |
| `N_resultados_gen2_adoptados_activos` | 24 | 24 | Este acto no adopta los tres resultados. |
| `diferencias_materiales` | 0 | 0 | Los valores permanecen idénticos. |

La etiqueta administrativa `cuenta_gen2=SI` ya existente tampoco vuelve nuevo
el número: origen, contador y aptitud son dimensiones distintas.

## Integridad preservada

| Artefacto previo, sólo lectura | SHA-256 antes y después |
| --- | --- |
| `data/corrida0/CALC-L8-CONVERSION-0001/resultados.json` | `b4a57cdc2504ce379b20870b1acefd81d4259fe675b1849247fe8c8dd40d33cf` |
| `data/corrida0/CALC-L8-CONVERSION-0001/sello.json` | `3d16bc120b5db1419ed6847e99288fadaf381e379b839949d38b4f41e290fd45` |
| `data/corrida0/CALC-L8-CONVERSION-0001/sello.sha256` | `c6023e4064bd601213d7d1dacfbfdf1736bd187387f73b06d02550df6e69045c` |

La regresión también altera un byte en memoria y confirma que el medidor emite
`NO-ESTIMABLE-INSUMO-DISCORDA`; reconocer la ruta como histórica no neutraliza
la guarda SHA ya existente.

## Decisión concreta para mesa

Conservar los tres resultados como **legado explícito bajo uso
`DESCRIPTIVO`**, porque la propia spec los define `DESCRIPTIVO-DERIVADO`. No
citarlos como `MEDICION-GEN2` ni `CONFIRMACION-INDEPENDIENTE`. La futura cita
de consumo, su compatibilidad con el estimando y cualquier adopción requieren
decisión separada de mesa; este acto no modifica `milpa/tramite.yaml`.

Interpretación de cierre: queda resuelta la indeterminación técnica de
NC-0253, no toda la fila ni la adopción de RES-0050/0051/0052. No aparece una
medición nueva y no baja el contador de dependencias heredadas.
