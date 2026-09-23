# Benchmark auditable del comportamiento del mexicano · catálogo v1.0

> | | |
> |---|---|
> | **ARCHIVO** | `catalogo-del-mexicano-v1_0.md` |
> | **NOMBRE ESTABLE** | `catálogo del mexicano` |
> | **ESTADO** | Producto consultable con reservas expresas de adopción y mecanismo |

**1537 filas de estimando/segmento/ola en cinco áreas de consulta.** Es un censo de lecturas con estado, no un conteo de adopciones. La tesis de estabilidad se restringe a estimandos, olas, población y umbrales efectivamente evaluados; la tabla incluye series históricas y propuestas que no prueban estabilidad.

La tabla [TSV](catalogo-del-mexicano-v1_0.tsv) permite buscar por área, conducta, instrumento, ola, segmento y llave. Cada fila conserva universo/denominador, escala, punto, límites de IC, naturaleza del IC, estado, firma, temporalidad, RESULT de punto y límites, CALC, hashes verificados, uso y reserva.

**Integridad:** SHA-256 del inventario fuente `399726f7b9da30f0ebae821079bef9fc554dbdc114facba117f4633356c922e7`; `python3 forense/analisis/catalogo/genera_catalogo.py` valida sellos de CALC y `python3 forense/analisis/catalogo/publica.py` regenera esta portada y el TSV.

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

### Reconciliación por procedencia

| Capa de lectura | Filas | Condición |
|---|---:|---|
| RESULT distintos con uso GEN2 activo | 72 | 85 usos pueden reutilizar un RESULT; no se duplican |
| Pisos históricos ASTRA-3 crédito 2012–2021 | 1 242 | Contexto por conducta, ola y segmento; no adopción nueva |
| Pisos adicionales del marcador | 59 | 57 evaluados y 2 no comparables; adopción por verificar |
| ENUT 2009/2014/2019/2024 | 120 | Sellados; adoptabilidad por dictaminar |
| ENIGH remesas 2016/2018/2020/2022 | 24 | Contexto sellado |
| Banxico/LAPOP/MOTRAL/EDER pendientes | 12 | 10 firma adoptar con consumo pendiente y 2 vetos |
| K2 bancario histórico adicional | 8 | Sellado y separado por denominador |
| **Total** | **1 537** | Suma de capas, no número de adopciones |

El bloque histórico de crédito 2012–2021 se incluye como contexto sellado, separado de la adopción GEN2. Las nueve celdas-D de crédito del PR #1058 ya están en main. El PR #1086 cerró la decisión P3 de tubería: sus siete celdas-D PUNTUADA aportan 111 celdas al contador `celdas_validadas`; k4a y k4b siguen SKIP. El contador global pasó de 92 a 219 e incluye además 16 celdas de ENCIG 2025. Contar validación no firma adopción ni acredita consumo de los RESULT en un modelo. El bloque Banxico/LAPOP/MOTRAL firmado para adoptar conserva el rótulo de consumo pendiente hasta que exista asiento mecánico en consumidor.

## Ejemplos trazables

Estos ejemplos son entradas a la tabla, no una media entre áreas. La escala y el denominador en cada fila gobiernan la interpretación.

| Área | Lectura de muestra | Estado | RESULT / CALC |
|---|---|---|---|
| Dinero y crédito | ENIF 2012; 0.27462906631324147 [0.2595998048911695, 0.28960752532996575]; proporción ponderada [0,1] | PISO-HISTORICO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | `RESULT-DIN-CREDITO-PISOS-ENIF2012-K1-NACIONAL-TODOS-P` / `CALC-DIN-CREDITO-PISOS-ENIF2012-0001` |
| Trámites y Estado | ENCIG 2025; 0.08511814556534456 [0.08086657882961802, 0.08902075774693383]; [SECUNDARIO · CELDA GEN1 · ADOPTABLE] proporcion ponderada de personas a las que un(a) servidor(a) publico(a) intento apropiarse o solicito de forma directa un beneficio (P8_3_1=1), unidad PERSONA, FAC_P18, escala [0,1], mas alto = mas solicitud | CONSUMO-GEN2-ACTIVO | `RESULT-ENCIG-MOR-A-P-SOL1` / `CALC-ENCIG-0001` |
| Seguridad y norma | ENVIPE 2025; 0.29431298745731216 [0.2830197508253073, 0.3057991950047491]; particion GEN1 a nivel PERSONA con FAC_ELE -- UNICA celda que comparte codificacion Y unidad con la cifra GEN1 sellada, escala [0,1] | CONSUMO-GEN2-ACTIVO | `RESULT-ENVIPE-DEN-P-C2-U4` / `CALC-ENVIPE-0001` |
| Tiempo, cuidado y vínculos | ENIGH 2022; 0.04569409956405095 [0.043772848428537396, 0.047770249605883566]; [2022] proporcion ponderada de hogares con remesas>0, universo completo de concentradohogar [0,1] | CONSUMO-GEN2-ACTIVO | `RESULT-B-ENIGH-2022-P` / `CALC-B-0001` |
| Ingreso y gasto | ENIGH 2016; 0.20450197714811436 [0.19169283164017298, 0.21729360731117506]; proporcion | SELLADO-CONTEXTO; NO-ADOPCION-POR-CATALOGO | `RESULT-ENIGH16-REMINT-PARTICIPACION-AGREGADA` / `CALC-ENIGH2016-INTENSIDAD-REMESAS-0001` |

## Reglas de lectura y déficit de mecanismos

Las reglas siguientes son **descripciones condicionadas**, salvo donde se cite expresamente un mecanismo identificado. `[DESCRIPTIVO]` significa que el RESULT estima una frecuencia para el segmento declarado, no que identifique por qué ocurre ni que prediga otra ola. El falsador especifica una observación que puede desmentir la generalización propuesta, sin convertir esta lectura en evaluación prospectiva.

1. **Trámites y Estado.** **SI** el evento de trámite ENCIG 2025 pertenece al canal presencial (`P7_3=1`) en áreas urbanas de 100 mil habitantes o más **ENTONCES** la proporción ponderada de mordida (`P8_4=1`) observada es 0.1410 [0.1164, 0.1685]; **SI** pertenece a canal digital (`P7_3∈{3,4,5}`), es 0.0299 [0.0210, 0.0398] — **PORQUE** el registro del funcionario y la menor discrecionalidad son un mecanismo propuesto en `modelo §3.3`, **no** un efecto identificado por esta comparación de canales. **[DESCRIPTIVO; mecanismo MEDIA no identificado aquí]**. Alcance: eventos, rama SD sin deduplicar, población urbana de ENCIG 2025, no México entero. Falsador de la generalización: una evaluación que iguale tipo de trámite y soporte entre canales y no conserve la dirección de la diferencia. Fuentes: `RESULT-ENCIG-MOR-B-P-PRE-SD`, `RESULT-ENCIG-MOR-B-P-DIG-SD`, `CALC-ENCIG-0001`; `canon/modelo-decision-v4_0.md §3.3`.
2. **Familia dentro de tiempo y cuidado.** **SI** el universo es el total de hogares ENIGH Nueva Serie 2022, sin otro filtro, **ENTONCES** 0.0457 [0.0438, 0.0478] presenta remesas positivas — **PORQUE** la familia como seguro ante volatilidad y ausencia estatal es el mecanismo *propuesto* en `modelo §3.5`, pero este marginal no prueba ni la volatilidad ni la sustitución causal. **[DESCRIPTIVO; mecanismo FUERTE en canon, no identificado por este RESULT]**. Falsador de la generalización: una ola comparable que, con el mismo indicador y universo, muestre un nivel incompatible con este intervalo; para el mecanismo se requiere medir conjuntamente volatilidad, cobertura estatal y transferencias. Fuentes: `RESULT-B-ENIGH-2022-P`, `CALC-B-0001`; `canon/modelo-decision-v4_0.md §3.5`.

**Déficit material para la cuota de cinco por área.** Dinero y crédito aporta numerosos marginales y pisos, pero la mayoría no cruza oferta con adopción en el mismo universo/ola; 829 de 1 242 enlaces de crédito carecen de oferta enlazable. Trámites aporta contraste de canal, pero el tipo de trámite y selección de canal impiden llamarlo efecto de digitalización. Seguridad y norma tiene pocos RESULT y mezcla unidad persona/delito; no da cinco drivers diferenciables. Tiempo y cuidado tiene 120 lecturas ENUT de uso del tiempo, todavía sin una prueba de mecanismo por carga de cuidado. Ingreso y gasto tiene 24 descriptores de remesas, no un repertorio general de gasto. Completar las cuotas con los enunciados del motor como si todos estuvieran corroborados por esta tabla inventaría respaldo. Se conserva la falta como tal.


## Interpretación y límites

La columna `oferta_compatible` distingue las medidas de oferta asociables de la ausencia de una medida compatible. Una cifra de oferta de otra ola es contexto; restarla de un marginal no identifica preferencia. Los IC muestrales no se presentan como cobertura calibrada. La comparación 2012–2021 de crédito debe mantener el recorte de 18–70 años y el mismo denominador; K2 entre tenedores y K2 poblacional son series distintas. La reserva K1 de predicción 2024 permanece.

La tabla es retrospectiva donde así se marca. No identifica efectos causales, psicología individual, preferencias frente a ausencia de oferta ni cambios futuros. No usa NSE AMAI calculado. La [matriz de calculabilidad](../forense/analisis/catalogo/matriz-amai-2024.md) documenta qué componentes ofrecen los cuestionarios.

El [dictamen de marginales y crédito](../forense/analisis/catalogo/dictamen-marginales-y-credito.md) expone firmas, reservas de ancho, lectura de la serie y la propuesta de FP para ENCIG sin mover el veto.

**Auditoría de rigor:** sin promediar escalas heterogéneas; sin atribuir propuesta a main; sin convertir un IC de muestra en calibración; sin predicción prospectiva a partir de una lectura retrospectiva.
