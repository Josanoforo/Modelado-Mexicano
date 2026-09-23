# Reservas de marginales y crédito para el catálogo

**Corte:** 23/sep/2026. Lectura de decisiones y RESULT sellados; no adopta ni levanta vetos.

| Instrumento | Resultado de cobertura retrospectiva del IC muestral del piso | Estado que puede decir el catálogo | Operación de mesa |
|---|---|---|---|
| ENVIPE 2025 | 8/15 = 0.53, Wilson [0.30, 0.75], `RESULT-ARBERR-AGG-ENVIPE2025-{N,N-DENTRO,COBERTURA,COBERTURA-IC-LO,COBERTURA-IC-HI}` en `CALC-ARBITRO-PERSISTENCIA-ERROR-0001` | Piso t−1 adoptado por firma de `FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02`; el margen muestral no acredita calibración futura | Conservar la reserva de ancho; no prometer cobertura de la siguiente ola. |
| ENIF 2024 | 6/32 = 0.19 [0.09, 0.35] con IC muestral, mismos RESULT `…-ENIF2024-*`; `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` cubre mecánicamente 32/32 con intervalo mediano de 35 pp, 8.9 veces el muestral, calibrado con un solo choque 2018→2021 | La mesa firmó `FP-260922-GEN2-ENIF-PERSISTENCIA-IC-CALIBRADO-1-2868-01` como **ADOPTAR-CON-RESERVA-DE-ANCHO**. El marcador y el consumo efectivo se comprueban por separado; el inventario no los promueve por la firma sola | Ejecutar sucesor `GEN2-MARGINALES-ADOPCION-2` por su mecanismo; rotular «conservador: calibrado con un solo choque 2018→2021» y nunca «cobertura». No crear otra FP para una opción ya firmada. |
| ENCIG 2025 | 0/10 [0.00, 0.28] con IC muestral (`RESULT-ARBERR-AGG-ENCIG2025-*`); el [CALC de IC de persistencia ENCIG](../../../data/corrida0/CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001/resultados.json) evaluó retrospectivamente 9/10 de 2021→2023, con ancho mediano 14.53 pp y una celda fallida | `FP-260921-GEN2-ARBITRO-MARGINALES-1-ed7d-02` veta el nivel en ENCIG 2025. La evaluación histórica del IC no es garantía 2025 | **Propuesta de FP específica, sin firma:** mantener veto de nivel hasta medir con protocolo congelado la cobertura en la ola/estimando que se pretenda usar, declarar denominador y dependencia de celdas, y justificar el ancho admisible. No trasladar automáticamente el 9/10 retrospectivo. |

**Crédito ASTRA-3.** Las cuatro olas ENIF 2012, 2015, 2018 y 2021, sus segmentos y sus IC bootstrap están enlazados en el TSV por RESULT/CALC/hash. Son **contexto histórico**, no adopciones nuevas. Un ejemplo que ilustra el cambio de universo: `RESULT-DIN-CREDITO-PISOS-ENIF2012-K1-NACIONAL-TODOS-P` corresponde a personas 18–70; `RESULT-DIN-CREDITO-PISOS-ENIF2021-K1-NACIONAL-TODOS-P` usa 18+ y **no** es el comparador correcto sin recorte. En la lectura de serie debe elegirse explícitamente el RESULT 2021 de 18–70. La [nota ASTRA-3 de oferta](../din-oferta-exclusion/nota-oferta-enif.md) documenta 413 enlaces contextuales y 829 sin enlace: la falta de oferta medible se mantiene visible, no se interpreta como preferencia. La [nota K1 2024](../../notas/nota-2026-09-22-gen2-din-credito-prediccion-2024-commit-2-3.md) conserva **PROPUESTA-CON-RESERVA** para K1 (+1.90 pp de ΔMAE, IC [+0.62,+2.65], 5/9 de cobertura); no se convierte en superioridad adoptada.

### Lectura absorbida de `GEN2-DIN-CREDITO-SERIE-LECTURA-1`

El encargo de serie estaba archivado sin entrega ejecutada ni propietaria activa al corte. Se leen aquí sus CALC ya sellados, sin reabrir dato. Las cifras son proporciones ponderadas [0,1] y los corchetes sus IC95 bootstrap; cada renglón conserva su RESULT de punto en el TSV y el hash de `resultados.json`.

| Ola ENIF | K1 tenencia, población 18–70 | K2 bancario, población | K2 bancario entre tenedores |
|---|---|---|---|
| 2012 | 0.2746 [0.2596,0.2896] | 0.0903 [0.0813,0.0995] | 0.3290 [0.3009,0.3572] |
| 2015 | 0.2905 [0.2752,0.3061] | 0.1076 [0.0978,0.1180] | 0.3704 [0.3422,0.3990] |
| 2018 | 0.3115 [0.3000,0.3231] | 0.1053 [0.0977,0.1131] | 0.3381 [0.3174,0.3591] |
| 2021 | 0.3268 [0.3157,0.3380] **recorte 18–70** | 0.1012 [0.0939,0.1085] **18+** | 0.3239 [0.3044,0.3433] **18+** |

K1 sube en estos cuatro puntos descriptivos. K2 bancario no tiene trayectoria monotónica en 2012–2018; **2021 cambia de 18–70 a 18+** en el CALC de K2 y no se interpreta como continuación de la misma serie. K2 poblacional y entre tenedores no son dos estimaciones del mismo denominador. Tampoco se infiere que la serie K1 identifica una causa ni que toda persona sin crédito lo haya rechazado: la oferta y elegibilidad cambian. La lectura 2021 de K1 sin recorte, 0.3125 [0.3021,0.3228], queda fuera de la primera columna. Los RESULT K1 proceden de `CALC-DIN-CREDITO-PISOS-ENIF{2012,2015,2018,2021}-0001`, usando `-RECORTE1870-` en el ID 2021; K2 de `CALC-DIN-CREDITO-K2-BANCARIA-HISTORIA-0002`.

**Estado de #1058.** El PR se fusionó el 23/sep/2026. Sus nueve archivos de celda-D están en main, pero `celdas_validadas` permanece en 92 porque el contador aún no admite la unidad «conducta agregada»; `NC-260923-GEN2-DIN-CREDITO-CELDAS-D-2-f6a3-02` deja esa decisión a tubería. El catálogo distingue presencia del archivo, validación del contador y adopción.

**Verificación:** `python3 tools/corrida0.py status` mostró 72 RESULT GEN2 activos, 10 pendientes de adopción, 4 vetados y 92 celdas validadas. Esas cantidades son estados operativos derivados, no mediciones de conducta.
