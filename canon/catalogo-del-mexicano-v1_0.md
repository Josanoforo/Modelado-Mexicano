# Benchmark auditable del comportamiento del mexicano · catálogo v1.0

**1537 filas de estimando/segmento/ola en cinco áreas de consulta.** Es un censo de lecturas con estado, no un conteo de adopciones. La tesis de estabilidad se restringe a estimandos, olas, población y umbrales efectivamente evaluados; la tabla incluye series históricas y propuestas que no prueban estabilidad.

La tabla [TSV](catalogo-del-mexicano-v1_0.tsv) permite buscar por conducta, instrumento, ola, segmento y llave. Cada fila conserva universo/denominador, escala, punto, límites de IC, naturaleza del IC, estado, firma, temporalidad, RESULT de punto y límites, CALC, hashes verificados, uso y reserva.

**Integridad:** SHA-256 del inventario fuente `7409e6ef07aa706aa2f4b46434d0ad0c791c7aa241e0d95740e4c6ca0f5a2179`; `python3 forense/analisis/catalogo/genera.py` valida sellos de CALC y `python3 forense/analisis/catalogo/publica.py` regenera esta portada y el TSV.

## Cómo leerlo

1. Busque el tema en la columna `conducta` y filtre `dominio`. Lea el `instrumento_ola` y `universo_denominador` antes de comparar filas.
2. Interprete el punto en `unidad_escala`; un 0.25 en proporción equivale a 25 %, mientras que minutos e importes conservan sus propias unidades. Los límites vacíos significan IC no identificado, nunca cero.
3. Filtre `estado_adopcion`. `CONSUMO-GEN2-ACTIVO` y `ADOPTADO-POR-FIRMA` no son lo mismo que un piso histórico, un resultado sellado sin adopción, una firma de adoptar aún no consumida o un veto.
4. Resuelva `result_punto` en `calc/resultados.json` bajo `data/corrida0/` y compare el hash con `sha256_resultados`. El hash de `sello.json` figura en `sha256_sello`.

## Cobertura del censo

El conteo siguiente es de **filas**, no de personas ni de estudios independientes. Una conducta por segmento y ola ocupa una fila; sus dos límites de IC no añaden filas. La llave RESULT impide contar otra vez una aparición documental.

| Área | Filas |
|---|---:|
| Dinero y crédito | 1316 |
| Trámites y Estado | 45 |
| Seguridad y norma | 15 |
| Tiempo, cuidado y vínculos | 137 |
| Ingreso y gasto | 24 |

### Estado operativo

| Estado | Filas |
|---|---:|
| ADOPTADO-POR-FIRMA | 20 |
| CONSUMO-GEN2-ACTIVO | 52 |
| FIRMA-ADOPTAR; CONSUMO-PENDIENTE | 10 |
| PISO-EN-MARCADOR:EVALUADA; ADOPCION-POR-VERIFICAR | 57 |
| PISO-EN-MARCADOR:NO-COMPARABLE; ADOPCION-POR-VERIFICAR | 2 |
| PISO-HISTORICO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | 1242 |
| SELLADO-CONTEXTO; ADOPTABILIDAD-POR-DICTAMINAR | 120 |
| SELLADO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | 32 |
| VETADO-POR-MESA | 2 |

El bloque histórico de crédito 2012–2021 se incluye como contexto sellado, separado de la adopción GEN2. Nueve celdas-D del PR #1058 permanecen propuestas mientras el PR esté abierto. El bloque Banxico/LAPOP/MOTRAL firmado para adoptar conserva el rótulo de consumo pendiente hasta que exista asiento mecánico en consumidor.

## Ejemplos trazables

Estos ejemplos son entradas a la tabla, no una media entre áreas. La escala y el denominador en cada fila gobiernan la interpretación.

| Área | Lectura de muestra | Estado | RESULT / CALC |
|---|---|---|---|
| Dinero y crédito | ENIF 2012; 0.27462906631324147 [0.2595998048911695, 0.28960752532996575]; proporción ponderada [0,1] | PISO-HISTORICO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | `RESULT-DIN-CREDITO-PISOS-ENIF2012-K1-NACIONAL-TODOS-P` / `CALC-DIN-CREDITO-PISOS-ENIF2012-0001` |
| Trámites y Estado | ENCIG 2025; 0.08511814556534456 [0.08086657882961802, 0.08902075774693383]; [SECUNDARIO · CELDA GEN1 · ADOPTABLE] proporcion ponderada de personas a las que un(a) servidor(a) publico(a) intento apropiarse o solicito de forma directa un beneficio (P8_3_1=1), unidad PERSONA, FAC_P18, escala [0,1], mas alto = mas solicitud | CONSUMO-GEN2-ACTIVO | `RESULT-ENCIG-MOR-A-P-SOL1` / `CALC-ENCIG-0001` |
| Seguridad y norma | ENVIPE 2025; 0.29431298745731216 [0.2830197508253073, 0.3057991950047491]; particion GEN1 a nivel PERSONA con FAC_ELE -- UNICA celda que comparte codificacion Y unidad con la cifra GEN1 sellada, escala [0,1] | CONSUMO-GEN2-ACTIVO | `RESULT-ENVIPE-DEN-P-C2-U4` / `CALC-ENVIPE-0001` |
| Tiempo, cuidado y vínculos | ENIGH 2022; 0.04569409956405095 [0.043772848428537396, 0.047770249605883566]; [2022] proporcion ponderada de hogares con remesas>0, universo completo de concentradohogar [0,1] | CONSUMO-GEN2-ACTIVO | `RESULT-B-ENIGH-2022-P` / `CALC-B-0001` |
| Ingreso y gasto | ENIGH 2016; 0.20450197714811436 [0.19169283164017298, 0.21729360731117506]; proporcion | SELLADO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | `RESULT-ENIGH16-REMINT-PARTICIPACION-AGREGADA` / `CALC-ENIGH2016-INTENSIDAD-REMESAS-0001` |

## Interpretación y límites

La columna `oferta_compatible` distingue las medidas de oferta asociables de la ausencia de una medida compatible. Una cifra de oferta de otra ola es contexto; restarla de un marginal no identifica preferencia. Los IC muestrales no se presentan como cobertura calibrada. La comparación 2012–2021 de crédito debe mantener el recorte de 18–70 años y el mismo denominador; K2 entre tenedores y K2 poblacional son series distintas. La reserva K1 de predicción 2024 permanece.

La tabla es retrospectiva donde así se marca. No identifica efectos causales, psicología individual, preferencias frente a ausencia de oferta ni cambios futuros. No usa NSE AMAI calculado. La [matriz de calculabilidad](../forense/analisis/catalogo/matriz-amai-2024.md) documenta qué componentes ofrecen los cuestionarios.

**Auditoría de rigor:** sin promediar escalas heterogéneas; sin atribuir propuesta a main; sin convertir un IC de muestra en calibración; sin predicción prospectiva a partir de una lectura retrospectiva.
