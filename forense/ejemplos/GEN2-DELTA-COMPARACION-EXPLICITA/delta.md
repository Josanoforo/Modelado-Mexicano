# Informe de delta explicito

Entrada: `forense/ejemplos/GEN2-DELTA-COMPARACION-EXPLICITA/pares-v1_0.yaml` (`3a26d9f27496a30347f412934c5b74294f61d205420e75780e1bb12b98c5acf6`).

Pares examinados: **3** · comparables: **2** · incompatibles: **1** · comparabilidad no determinable: **0**.
Deltas calculados: **2** · materiales: **0** · materialidad no determinable: **3**.

Los veredictos aplican solo a los pares explicitos examinados. Cero materiales no demuestra coincidencia general y la equivalencia de representacion no determina materialidad cientifica.

## DELTA-REMESAS-ENIGH2022-GRANO

Consumidor/uso: `milpa/tramite.yaml:familia.seguro.volatilidad_ausencia_estado:recibe_remesas` — calibracion puntual ENIGH 2022; la serie de olas no se promedia.

- A: `0.045694` (FUENTE; RESUELTA).
- B: `0.04569409956405095` (RESULTADO-CORRIDA0; RESUELTA).
- Referencias: **ACREDITADA**.
- Comparabilidad: **DEMOSTRADA** — las ocho dimensiones tienen correspondencia acreditada.
- Diferencia B−A: **9.956405094824206e-08** proporcion de hogares; magnitud `9.956405094824206e-08`; pp `9.956405094824206e-06`; cambio relativo `2.178930514908786e-06` (CALCULADO).
- Representacion: **IGUAL-AL-GRANO** — grano del consumidor = 6 decimales.
- Materialidad: **NO-DETERMINABLE** — el contrato no contiene un criterio sustantivo citado; el grano no lo sustituye.
- Resultado: **DELTA-CALCULADO · REPRESENTACION-IGUAL-AL-GRANO · MATERIALIDAD-NO-DETERMINABLE**.

## DELTA-ENIF-CREDITO-APP-2024-MENOS-2021

Consumidor/uso: `dinero.credito.scoring_alternativo (R1.6)` — contexto descriptivo DESCRIPTIVO-NO-CALIBRA sobre canal del ultimo producto; no canal fintech exacto.

- A: `0.69803002012` (RESULTADO-CORRIDA0; RESUELTA).
- B: `0.575` (FUENTE; RESUELTA).
- Referencias: **ACREDITADA**.
- Comparabilidad: **DEMOSTRADA** — las ocho dimensiones tienen correspondencia acreditada.
- Diferencia B−A: **-0.12303002012000008** proporcion ponderada; magnitud `0.12303002012000008`; pp `-12.303002012000007`; cambio relativo `-0.17625319337820125` (CALCULADO).
- Representacion: **DISTINTO-AL-GRANO** — grano del consumidor = 3 decimales.
- Materialidad: **NO-DETERMINABLE** — #706 no define umbral sustantivo; el cambio es descriptivo y no causal.
- Resultado: **DELTA-CALCULADO · REPRESENTACION-DISTINTO-AL-GRANO · MATERIALIDAD-NO-DETERMINABLE**.

## RECHAZO-ENIF-CUENTA-APP-2024-2021

Consumidor/uso: `dinero.credito.scoring_alternativo (R1.6)` — contexto lado a lado, sin delta, del canal de la ultima cuenta entre tenedores del proxy fintech.

- A: `0.225282724538` (RESULTADO-CORRIDA0; RESUELTA).
- B: `0.306` (FUENTE; RESUELTA).
- Referencias: **ACREDITADA**.
- Comparabilidad: **INCOMPATIBILIDAD** — ruptura/incompatibilidad en: poblacion, evento, codigos.
- Diferencia B−A: **NO-APLICA** proporcion ponderada; magnitud `NO-APLICA`; pp `NO-APLICA`; cambio relativo `NO-APLICA` (NO-APLICA-COMPARABILIDAD).
- Representacion: **NO-APLICA**.
- Materialidad: **NO-DETERMINABLE** — el delta sustantivo se rechaza antes de preguntar materialidad.
- Resultado: **DELTA-SUSTANTIVO-RECHAZADO-INCOMPATIBILIDAD**.
