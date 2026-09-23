# Hoja de propuestas de familias prospectivas · para mesa

**Continuación U4 · corte 23/sep/2026.** Las seis familias quedan **CONDICIONALES** por fecha oficial e identidad futura del instrumento. El estado temporal no deja pendientes las decisiones técnicas que pueden proponerse ahora. “2027” es etiqueta, no anuncio de INEGI.

## Decisión técnica propuesta

- Tolerancia material primaria: error local absoluto de **2.0 puntos porcentuales (pp)** alrededor del piso, con signo e intervalo de `d=R−piso`. Es margen práctico para un falsador puntual, no una prueba general de equivalencia ni tolerancia numérica del CALC.
- Soporte, faltantes y comparabilidad: regla específica en cada spec v1.1; mínimo común: universo, unidad, definición del resultado y ponderador equivalentes; diseño estrato/UPM identificado; bootstrap prospectivo con al menos 1,000 réplicas válidas de 2,000 y menos de 5% degeneradas.
- Dictamen por estimando: `CALIBRADO-LOCAL` requiere punto dentro de ±2 pp, IC95 de `d` que contiene cero e intervalo interpretable; `DESVÍO-MATERIAL` si todo el IC95 queda fuera del margen por un lado; `INDETERMINADO` si cruza el límite, la precisión no permite resolverlo o falla la interpretación del diseño; `NO-ESTIMABLE` por soporte/faltantes; `NO-COMPARABLE` por cambio de concepto/unidad.
- Un valor dentro del IC del piso no basta para concluir calibración. El resultado sólo describe compatibilidad del piso para este estimando, ola y margen. No hay retador: superioridad/ΔMAE = NO-APLICABLE.

## Familias y dependencias

| Familia | Piso y RESULT | Soporte factual del artefacto sellado | Propuesta primaria | Estado y activación verificable |
|---|---|---|---|---|
| ENIF-AHORRO-FORMAL | `CALC-ENIF-0001` · `RESULT-ENIF-AHO-B-P-FORMAL-P` (ENIF 2024; SHA `0c908018…f76de6`) | n=13,502; 190 estratos; 2,164 UPM; IC95 [0.274161,0.296777]; cero UPM únicas/sin diseño. | ±2 pp; soporte n≥10,000, ≥150 estratos, ≥1,000 UPM; faltantes del reactivo fuera de numerador, reportados, sin imputar. | CONDICIONAL a fecha oficial en ventana 23/sep/2026–23/mar/2028, cuestionario equivalente, FAC_PER y dominio B replicables. Comparte una apertura ENIF. |
| ENIF-HORIZONTE-AHORRO | `CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1` · `RESULT-HVD-A-AMBAS-VIAS` (derivado ENIF 2024; SHA `1c8b329f…d92609`) | n común heredable del padre=13,502; HVD es aritmética de tres proporciones; su CALC declara **sin IC propio** por falta de covarianza conjunta. | ±2 pp sobre estimación directa conjunta; si no hay microdato/variables que identifiquen ambas vías para mismas personas, no reconstruir desde marginales: NO-ELEGIBLE/NO-ESTIMABLE. | CONDICIONAL adicional a instrumento futuro capaz de identificar formal, informal y tenencia total en mismo universo. Mismo acceso ENIF que familia anterior. |
| ENCIG-PAGO-DIGITAL | `CALC-ENCIG-0001` · `RESULT-ENCIG-MOR-C-P-ADOPTA` (ENCIG 2025; SHA `9db7e8f2…b6cbf58d7`) | n=20,203 trámites; 441 estratos; 8,486 UPM; IC95 [0.662900,0.684530]; 8 estratos UPM única (IC subestima anchura). | ±2 pp; n≥10,000; ≥100 estratos y ≥1,000 UPM; residuo canal ≤1% de peso elegible; unidad con FAC_TRA. | CONDICIONAL a misma definición servicio/pago, P7_3, universo C, FAC_TRA, llaves y fecha. Una apertura ENCIG junto a solicitud-mordida. |
| ENCIG-SOLICITUD-MORDIDA | `CALC-ENCIG-0001` · `RESULT-ENCIG-MOR-A-P-SOL1` (ENCIG 2025; mismo SHA) | n=40,042 personas; 442 estratos; 9,172 UPM; IC95 [0.080867,0.089021]; 94 NS/NR P8_3_1, cero blanco/sin diseño. | ±2 pp; n≥10,000; ≥100 estratos, ≥1,000 UPM; faltantes ≤2% de peso de A; universo con respuesta válida P8_3_1/FAC_P18. | CONDICIONAL a equivalencia textual y de saltos, outcome SOL1 (sin mezclar SOLANY), población y FAC_P18. Misma apertura ENCIG; un paquete de resultados conjunto. |
| ENVIPE-DENUNCIA-U4 | `CALC-ENVIPE-0001` · `RESULT-ENVIPE-DEN-P-C2-U4` (ENVIPE 2025; SHA `18310f8a…90cbde16`) | n=13,023 personas U4; masa FAC_ELE=14,982,594; CALC declara 2,000 réplicas; IC [0.283020,0.305799]. 83 estratos UPM única se cuentan en U1, y el IC es límite inferior de anchura; réplicas no almacenadas. | ±2 pp; n≥5,000; ≥100 estratos/≥1,000 UPM; cero sin FAC_ELE/diseño. No interpretar IC histórico como calibrado. | CONDICIONAL a fecha/cuestionario, FAC_ELE, C2/U4 y diseño de persona. Compartir acceso ENVIPE con evasión-norma; no abrir ENVIPE 2026. |
| ENVIPE-EVASION-NORMA | `CALC-EVASION-NORMA-0001-v1_1` · `RESULT-EVASIONNORMA-A-P-EVADE` (ENVIPE 2025; SHA `8076d9ff…9d2abe8`) | n=40,280 delitos; numerador 21,761; 10,694 UPM; 10,000 réplicas seed 42; IC [0.551982,0.573448]. No se conservan réplicas ni conteos de estrato/UPM única. | ±2 pp; n≥10,000; ≥100 estratos/≥1,000 UPM; cero faltantes de diseño/outcome; faltantes de peso ≤1%; exportar réplicas futuras. | CONDICIONAL a BP1_20/BP1_23, categorías, FAC_DEL, unidad delito y diseño. Una apertura ENVIPE junto a U4. No confundir con resultado por persona. |

Los SHA abreviados de tabla son de `sello.json`; el SHA completo vive en cada spec. `data/corrida0/resultados.tsv` contiene los RESULT con estado SELLADA; los objetos íntegros y hashes se comprueban con `corrida0 verify`. Los puntos no se copian aquí para evitar que una tabla sustituya a sus fuentes canónicas.

## Incertidumbre y condición de análisis

Los CALC de origen ya ejecutados no se modifican. ENIF-Ahorro y las dos tasas ENCIG tienen intervalos históricos de diseño, pero no vectores exportados de réplicas que permitan estimar la distribución del error contra un resultado futuro. ENVIPE-Denuncia registra los extremos y cantidad de réplicas, pero el IC usa estratos con una sola UPM que aportan varianza cero. Evasión-norma registra número de réplicas y extremos, no las réplicas. HVD no tiene intervalo conjunto ni covarianza entre tres marginales y además su resultado es aritmético sobre RESULT sellados, no medición conjunta nueva.

Por ello **no se declara potencia ni efecto mínimo detectable** con los artefactos actuales; no se infiere EE de extremos de IC y no se reconstruyen réplicas. Cada futura corrida debe guardar resultados por réplica, estratos/UPM únicos, n efectivo y tasas de exclusión. Para HVD debe medir la intersección en registros individuales o proporcionar las réplicas emparejadas y covarianzas autorizadas. Si no existe ese artefacto, el dictamen de precisión queda INDETERMINADO y no se rebaja soporte después de observar R.

## Dependencias de activación

1. Calendario oficial que confirme fecha de publicación dentro de la ventana; referencia, levantamiento y publicación se documentan por separado. Si no está anunciado, la fila permanece CONDICIONAL.
2. Cuestionario, descriptor, pesos y diseño de la ola futura cotejados antes de COMMIT-1; el nombre del año no prueba fecha ni equivalencia.
3. Una apertura por instrumento (tres en total), con las dos familias del instrumento congeladas juntas. Ningún estimando añadido tras R, ni selección de entre outcomes.
4. En HVD, estimación conjunta directa obligatoria; si la ola no permite identificar el evento conjunto, no se activa esa familia.
5. Ninguna condición autoriza en esta continuación abrir microdatos, olas reservadas, ENCO o ENVIPE 2026; adquisición y reserva se asientan por el canal correspondiente.

FP-374 y NC-0161/0162/0234 permanecen como referencias históricas de otra cadena decisional: esta hoja no cambia su estado ni abre F6. La presente entrega propone seis familias de encuestas con piso y R futuro, no seis oportunidades independientes ni evidencia de transferencia confirmatoria.

## EJECUTADO / LEÍDO / PROPUESTO

- **EJECUTADO:** seis especificaciones humanas v1.1 con sidecar regenerable; hash de cada piso verificado contra sello, sidecar y RESULT numérico; hoja de decisiones coherente; referencias originales v1.0 preservadas.
- **LEÍDO:** specs y CALC sellados ENIF, HVD, ENCIG, ENVIPE denuncia-U4 y evasión-norma; `calendario-y-exclusiones.md`; encargo original. Sin nueva lectura de microdato ni replay de los CALC históricos.
- **PROPUESTO:** tolerancia ±2 pp, soportes por familia, faltantes, comparabilidad y reglas de dictamen descritas arriba. Efecto mínimo detectable/potencia quedan NO-CALCULABLES hasta disponer del vector de réplicas requerido; esto no deja pendiente la propuesta técnica.

## NO-CORRIDO / RESERVAS

Ningún calendario futuro consultado fuera de la fuente ya archivada; no se verificó anuncio posterior por la falla de red inicial. No se abrieron datos. No se corrieron CALC ni pruebas sobre microdatos. No se obtuvo precisión/potencia porque los vectores de réplica histórica no existen en los artefactos descritos. Las fechas oficiales futuras, las tres aperturas, la equivalencia de cuestionarios y el asiento de reservas de adquisición permanecen pendientes. No se fusiona.

## CONSUMIDO

PR #1076 · `codex/astra4-familias-prospectivas-1` · base comprobada `d21f1551c571b77e43e1f72bc9a36a91151f63a3`.

**Recibo Codex para revisión:** propuestas U4 v1.1 completas y condiciones de activación explícitas; conservar como CONDICIONAL hasta calendario oficial y cotejo instrumental; revisión por Claude y firma de mesa por merge. No autoriza F6, adquisición de datos ni apertura de olas.
