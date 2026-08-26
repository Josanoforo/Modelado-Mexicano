# Cruce exhaustivo de oferta y demanda del motor · v0.1

Fecha de revisión: **2026-08-25**. Base real: `5db163b17e57b02187d47f7fcf640dda2751baf1`. Redacción de referencia: `9e9132d`.

## Resultado ejecutivo

El cruce materializa **42 demandas únicas** y **1422 filas finales**. Recorrió **59 archivos**, todos legibles, e indexó **169,474 registros**. El producto cartesiano efectivamente evaluado fue de **7,117,908 pares demanda×registro**; no hubo muestra, límite, corte por puntuación ni salida temprana. Los **2,076 candidatos únicos** recibieron revisión: 1,411 quedaron como `EXISTE-NO-SATISFACE` y 665 como `DESCARTADO_NO-CANDIDATO`. Estos últimos no pasan al TSV. Once demandas quedaron `NO-ENCONTRADO` después del gate de cobertura y del control positivo reproducible `INEGI` (122,568 hits sobre el mismo universo).

Por fila final: `EXISTE-NO-SATISFACE`=1411, `NO-ENCONTRADO`=11. Ninguna coincidencia se promovió a `EXISTE-SATISFACE`: los nueve marcadores positivos encontrados acreditaban identidad o acceso del payload, no la magnitud, escala o condición completa pedida por la demanda.

La decisión operativa principal es clara: la primera palanca es `disparador_sin_base:riesgo_fiscal_percibido`, porque el emisor ejecutable ya consume ese concepto para el gate R3.4 sin una base medida. La segunda es la escala de `G3.horizonte_temporal`: es la única `RUTA-I` de los quince coeficientes, pero sigue `SUBDETERMINADA-PERSISTENTE`.

## Base, precedencia y alcance

- `origin/main` capturado: `5db163b17e57b02187d47f7fcf640dda2751baf1`; es el merge de #360 y contiene la versión vigente de R2.1.
- `9e9132d` es ancestro de la base real.
- `5db163b` es ancestro y coincide con la base capturada; se usó solo como comprobación informativa.
- `c6a5ab3` es ancestro obligatorio de la base real y no se añadió ninguna capa distinta.
- El preregistro vigente es `forense/hitoD-preregistro-v2_0.md`.
- El complemento del bloque append-only de veredictos son siete falsadores: R2.1, R2.2, R3.4, R8.2, R10.1, R10.2 y R10.3. El catálogo histórico que aún lista catorce pendientes no gobierna esta derivación.
- La antigua cifra 5/6 de EMISOR-M-2 se conservó como referencia histórica; el universo de entrada se rederivó y son seis disparadores sin base medida o cableado vivo completo.

## Demanda derivada

| tipo | demandas únicas |
|---|---:|
| `ASIGNADO_coef` | 15 |
| `theta_sin_escala` | 8 |
| `clase_procedencia_faltante` | 6 |
| `disparador_sin_base` | 6 |
| `falsador_sin_fuente` | 7 |
| **Total** | **42** |

Los falsadores se enlazaron a reglas reales del motor, no a la línea narrativa del preregistro: R2.1→`canon/modelo-decision-v4_0.md:506`; R2.2→`:507`; R3.4→`:517`; R8.2→`:561`; R10.1→`:579`; R10.2→`:580`; R10.3→`:581`.

### Tabla completa n(C)

| clase | n(C) | definición | primera entrada viva |
|---|---:|---|---|
| `MEDIDO` | 0 | `milpa/procedencia.yaml:8` | `NINGUNA (n(C)=0)` |
| `DERIVADO` | 0 | `milpa/procedencia.yaml:9` | `NINGUNA (n(C)=0)` |
| `ORDINAL→CARDINAL` | 0 | `milpa/procedencia.yaml:10` | `NINGUNA (n(C)=0)` |
| `ASIGNADO` | 0 | `milpa/procedencia.yaml:13` | `NINGUNA (n(C)=0)` |
| `AJUSTADO` | 0 | `milpa/procedencia.yaml:15` | `NINGUNA (n(C)=0)` |
| `MEDIDO·PARCIAL(x)` | 10 | `milpa/procedencia.yaml:28` | `milpa/procedencia.yaml:181` |
| `MEDIDO·NACIONAL` | 2 | `milpa/procedencia.yaml:40` | `milpa/procedencia.yaml:514` |
| `EVIDENCIA_EXPERIMENTAL_TERCEROS` | 0 | `milpa/procedencia.yaml:59` | `NINGUNA (n(C)=0)` |

El conteo usa nodos YAML `clase:` con posición. Para `MEDIDO·PARCIAL(x)` usa el prefijo `MEDIDO·PARCIAL(`; las otras clases usan coincidencia exacta. Las secciones narrativas `medidos:` y `derivados:` no se hicieron pasar por nodos `clase:`.

## Universo exhaustivo de oferta

Se incluyeron los 46 archivos de `data/curacion-universo/`: **16 perfil**, **7 pool** y **23 autoridad**. Se añadieron completos `data/manifiesto.yaml` (792 entradas), `data/diseno-muestral.yaml` (56 entradas) y los **11 inventarios**:

- `data/inventarios/inventario-fuentes-credito-ahorro-finanzas-hogar-mexico.md`
- `data/inventarios/inventario-fuentes-migracion-mexico.md`
- `data/inventarios/inventario-fuentes-tecnologia-digital-mexico.md`
- `data/inventarios/inventario_fuentes_capital_social_mexico.md`
- `data/inventarios/inventario_fuentes_clase-fuente-mexico.md`
- `data/inventarios/inventario_fuentes_cultura_valores_opinion_mexico.md`
- `data/inventarios/inventario_fuentes_salud_mexico.md`
- `data/inventarios/inventario_fuentes_seguridad_justicia_mexico.md`
- `data/inventarios/inventario_fuentes_trabajo_ingreso_formalidad_mexico.md`
- `data/inventarios/inventario_fuentes_tramites_estado_mexico.md`
- `data/inventarios/inventario_fuentes_uso_del_tiempo_cuidados_hogar_mexico.md`

La indexación abarcó todas las filas TSV/CSV, cada entrada lógica de los YAML, cada línea lógica enumerable de Markdown, JSON/JSONL y los artefactos de autoridad. Ningún archivo quedó `NO-ACCESIBLE`; si hubiera ocurrido, el gate habría exigido `leídos + no accesibles = universo`.

## Método de cruce y revisión

Para cada demanda se evaluaron los 169,474 registros. La normalización solo ordenó la búsqueda léxica: cada frase semilla se comparó con frontera de token, evitando falsos positivos como `face` dentro de `satisface`. No se excluyó ningún registro por puntuación. La deduplicación usó exclusivamente igualdad exacta del texto y conservó todos los localizadores `archivo:línea`.

Cada candidato tuvo una fila en `revision.tsv`. Una coincidencia en esquema/script, una mención de gobernanza de clase o un cierre negativo histórico se marcó `DESCARTADO_NO-CANDIDATO` con motivo concreto. Una fuente real sin prueba de cobertura completa quedó `EXISTE-NO-SATISFACE`. Todo negativo final porta el resumen compacto de cobertura y un control positivo sobre el mismo universo.

## Cobertura exhaustiva

La siguiente tabla contiene una fila por demanda_id. `N_registros_evaluados` no se imprime porque fue comprobado internamente igual a `N_registros_indexados` en las 42 filas.

| demanda_id | universo | leídos | registros | hits | candidatos | revisados | no accesibles |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ASIGNADO_coef:G1.confianza_institucional` | 59 | 59 | 169474 | 111 | 111 | 111 | 0 |
| `ASIGNADO_coef:G1.radio_confianza` | 59 | 59 | 169474 | 6 | 6 | 6 | 0 |
| `ASIGNADO_coef:G2.sens_estatus` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |
| `ASIGNADO_coef:G2.aversion_riesgo` | 59 | 59 | 169474 | 2 | 2 | 2 | 0 |
| `ASIGNADO_coef:G3.horizonte_temporal` | 59 | 59 | 169474 | 37 | 37 | 37 | 0 |
| `ASIGNADO_coef:G3.aversion_riesgo` | 59 | 59 | 169474 | 2 | 2 | 2 | 0 |
| `ASIGNADO_coef:G3.familismo_apoyo` | 59 | 59 | 169474 | 20 | 20 | 20 | 0 |
| `ASIGNADO_coef:G4.exposicion_violencia` | 59 | 59 | 169474 | 6 | 6 | 6 | 0 |
| `ASIGNADO_coef:G4.confianza_institucional` | 59 | 59 | 169474 | 111 | 111 | 111 | 0 |
| `ASIGNADO_coef:G4.horizonte_temporal` | 59 | 59 | 169474 | 37 | 37 | 37 | 0 |
| `ASIGNADO_coef:G4.sens_estatus` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |
| `ASIGNADO_coef:G5.familismo_apoyo` | 59 | 59 | 169474 | 20 | 20 | 20 | 0 |
| `ASIGNADO_coef:G5.familismo_obligacion` | 59 | 59 | 169474 | 24 | 24 | 24 | 0 |
| `ASIGNADO_coef:G5.radio_confianza` | 59 | 59 | 169474 | 6 | 6 | 6 | 0 |
| `ASIGNADO_coef:G6.deferencia` | 59 | 59 | 169474 | 14 | 14 | 14 | 0 |
| `theta_sin_escala:G2.sens_estatus` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |
| `theta_sin_escala:G2.aversion_riesgo` | 59 | 59 | 169474 | 2 | 2 | 2 | 0 |
| `theta_sin_escala:G3.horizonte_temporal` | 59 | 59 | 169474 | 37 | 37 | 37 | 0 |
| `theta_sin_escala:G3.aversion_riesgo` | 59 | 59 | 169474 | 2 | 2 | 2 | 0 |
| `theta_sin_escala:G4.horizonte_temporal` | 59 | 59 | 169474 | 37 | 37 | 37 | 0 |
| `theta_sin_escala:G4.sens_estatus` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |
| `theta_sin_escala:G5.familismo_obligacion` | 59 | 59 | 169474 | 24 | 24 | 24 | 0 |
| `theta_sin_escala:G6.deferencia` | 59 | 59 | 169474 | 14 | 14 | 14 | 0 |
| `clase_procedencia_faltante:MEDIDO` | 59 | 59 | 169474 | 6 | 6 | 6 | 0 |
| `clase_procedencia_faltante:DERIVADO` | 59 | 59 | 169474 | 61 | 61 | 61 | 0 |
| `clase_procedencia_faltante:ORDINAL→CARDINAL` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `clase_procedencia_faltante:ASIGNADO` | 59 | 59 | 169474 | 285 | 285 | 285 | 0 |
| `clase_procedencia_faltante:AJUSTADO` | 59 | 59 | 169474 | 308 | 308 | 308 | 0 |
| `clase_procedencia_faltante:EVIDENCIA_EXPERIMENTAL_TERCEROS` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `disparador_sin_base:riesgo_fiscal_percibido` | 59 | 59 | 169474 | 251 | 251 | 251 | 0 |
| `disparador_sin_base:friccion_uso` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `disparador_sin_base:utilidad_marginal_sobre_sustituto` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `disparador_sin_base:lado_obligado` | 59 | 59 | 169474 | 3 | 3 | 3 | 0 |
| `disparador_sin_base:sancion` | 59 | 59 | 169474 | 46 | 46 | 46 | 0 |
| `disparador_sin_base:dato_sensible` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `falsador_sin_fuente:R2.1` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |
| `falsador_sin_fuente:R2.2` | 59 | 59 | 169474 | 18 | 18 | 18 | 0 |
| `falsador_sin_fuente:R3.4` | 59 | 59 | 169474 | 255 | 255 | 255 | 0 |
| `falsador_sin_fuente:R8.2` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `falsador_sin_fuente:R10.1` | 59 | 59 | 169474 | 0 | 0 | 0 | 0 |
| `falsador_sin_fuente:R10.2` | 59 | 59 | 169474 | 325 | 325 | 325 | 0 |
| `falsador_sin_fuente:R10.3` | 59 | 59 | 169474 | 1 | 1 | 1 | 0 |

## Ranking completo por palanca del motor

La clasificación primaria fue dependencia concreta, no tipo de demanda ni veredicto A.4: nivel 1 desbloquea un cómputo/mecanismo vivo; nivel 2 calibra o vuelve interpretable un parámetro consumido; nivel 3 habilita cableado, prueba o procedencia sin bloquear el cómputo principal. Dentro de nivel se usó la ruta real (`RUTA-I`→`RUTA-A`→`RUTA-C`→`SIN-RUTA`) y la cercanía al mecanismo. A.4 solo desempata palancas equivalentes.

| rank | demanda_id | nivel | mecanismo/contador | mejor A.4 |
|---:|---|---:|---|---|
| 1 | `disparador_sin_base:riesgo_fiscal_percibido` | 1 | gate R3.4 / emisor ejecutable | `EXISTE-NO-SATISFACE` |
| 2 | `theta_sin_escala:G3.horizonte_temporal` | 2 | G3 → ahorro informal/planeación; llave CAL-G3 | `EXISTE-NO-SATISFACE` |
| 3 | `ASIGNADO_coef:G3.horizonte_temporal` | 2 | G3 → ahorro informal/planeación; llave CAL-G3 | `EXISTE-NO-SATISFACE` |
| 4 | `ASIGNADO_coef:G1.confianza_institucional` | 2 | G1 → mordida/registro y gate R3.4 | `EXISTE-NO-SATISFACE` |
| 5 | `ASIGNADO_coef:G1.radio_confianza` | 2 | G1 → puente personal y adopción por confianza | `EXISTE-NO-SATISFACE` |
| 6 | `ASIGNADO_coef:G3.familismo_apoyo` | 2 | G3 → tanda/pooling económico | `EXISTE-NO-SATISFACE` |
| 7 | `ASIGNADO_coef:G4.confianza_institucional` | 2 | G4 → respuesta a autoridad no confiable | `EXISTE-NO-SATISFACE` |
| 8 | `ASIGNADO_coef:G4.exposicion_violencia` | 2 | G4 → protesta/autodefensa y silencio adaptativo | `EXISTE-NO-SATISFACE` |
| 9 | `ASIGNADO_coef:G2.aversion_riesgo` | 2 | G2 → crédito y decisión bajo riesgo | `EXISTE-NO-SATISFACE` |
| 10 | `ASIGNADO_coef:G2.sens_estatus` | 2 | G2 → consumo compensatorio/aspiracional | `EXISTE-NO-SATISFACE` |
| 11 | `ASIGNADO_coef:G3.aversion_riesgo` | 2 | G3 → pooling y ahorro bajo volatilidad | `EXISTE-NO-SATISFACE` |
| 12 | `ASIGNADO_coef:G4.horizonte_temporal` | 2 | G4 → adaptación ante inseguridad | `EXISTE-NO-SATISFACE` |
| 13 | `ASIGNADO_coef:G4.sens_estatus` | 2 | G4 → respuesta cívica situada | `EXISTE-NO-SATISFACE` |
| 14 | `ASIGNADO_coef:G5.familismo_apoyo` | 2 | G5 → familia como seguro | `EXISTE-NO-SATISFACE` |
| 15 | `ASIGNADO_coef:G5.familismo_obligacion` | 2 | G5 → carga de cuidado/obligación familiar | `EXISTE-NO-SATISFACE` |
| 16 | `ASIGNADO_coef:G5.radio_confianza` | 2 | G5 → apoyo familiar y red de confianza | `EXISTE-NO-SATISFACE` |
| 17 | `ASIGNADO_coef:G6.deferencia` | 2 | G6 → jerarquía R2.1 y retroalimentación R10.2 | `EXISTE-NO-SATISFACE` |
| 18 | `theta_sin_escala:G2.aversion_riesgo` | 2 | G2 → crédito y decisión bajo riesgo | `EXISTE-NO-SATISFACE` |
| 19 | `theta_sin_escala:G2.sens_estatus` | 2 | G2 → consumo compensatorio/aspiracional | `EXISTE-NO-SATISFACE` |
| 20 | `theta_sin_escala:G3.aversion_riesgo` | 2 | G3 → pooling y ahorro bajo volatilidad | `EXISTE-NO-SATISFACE` |
| 21 | `theta_sin_escala:G4.horizonte_temporal` | 2 | G4 → adaptación ante inseguridad | `EXISTE-NO-SATISFACE` |
| 22 | `theta_sin_escala:G4.sens_estatus` | 2 | G4 → respuesta cívica situada | `EXISTE-NO-SATISFACE` |
| 23 | `theta_sin_escala:G5.familismo_obligacion` | 2 | G5 → carga de cuidado/obligación familiar | `EXISTE-NO-SATISFACE` |
| 24 | `theta_sin_escala:G6.deferencia` | 2 | G6 → jerarquía R2.1 y retroalimentación R10.2 | `EXISTE-NO-SATISFACE` |
| 25 | `disparador_sin_base:friccion_uso` | 3 | R3.4 / vocabulario EMISOR-M-2 (friccion_uso) | `NO-ENCONTRADO` |
| 26 | `disparador_sin_base:utilidad_marginal_sobre_sustituto` | 3 | R3.4 / vocabulario EMISOR-M-2 (utilidad_marginal_sobre_sustituto) | `NO-ENCONTRADO` |
| 27 | `disparador_sin_base:lado_obligado` | 3 | R3.4 / vocabulario EMISOR-M-2 (lado_obligado) | `EXISTE-NO-SATISFACE` |
| 28 | `disparador_sin_base:sancion` | 3 | R3.4 / vocabulario EMISOR-M-2 (sancion) | `EXISTE-NO-SATISFACE` |
| 29 | `disparador_sin_base:dato_sensible` | 3 | R3.4 / vocabulario EMISOR-M-2 (dato_sensible) | `NO-ENCONTRADO` |
| 30 | `falsador_sin_fuente:R3.4` | 3 | gate R3.4 | `EXISTE-NO-SATISFACE` |
| 31 | `falsador_sin_fuente:R2.1` | 3 | Hito D R2.1 | `EXISTE-NO-SATISFACE` |
| 32 | `falsador_sin_fuente:R2.2` | 3 | Hito D R2.2 | `EXISTE-NO-SATISFACE` |
| 33 | `falsador_sin_fuente:R8.2` | 3 | Hito D R8.2 | `NO-ENCONTRADO` |
| 34 | `falsador_sin_fuente:R10.1` | 3 | Hito D R10.1 | `NO-ENCONTRADO` |
| 35 | `falsador_sin_fuente:R10.2` | 3 | Hito D R10.2 | `EXISTE-NO-SATISFACE` |
| 36 | `falsador_sin_fuente:R10.3` | 3 | Hito D R10.3 | `EXISTE-NO-SATISFACE` |
| 37 | `clase_procedencia_faltante:AJUSTADO` | 3 | registro de procedencia | `NO-ENCONTRADO` |
| 38 | `clase_procedencia_faltante:ASIGNADO` | 3 | registro de procedencia | `NO-ENCONTRADO` |
| 39 | `clase_procedencia_faltante:DERIVADO` | 3 | registro de procedencia | `NO-ENCONTRADO` |
| 40 | `clase_procedencia_faltante:EVIDENCIA_EXPERIMENTAL_TERCEROS` | 3 | registro de procedencia | `NO-ENCONTRADO` |
| 41 | `clase_procedencia_faltante:MEDIDO` | 3 | registro de procedencia | `NO-ENCONTRADO` |
| 42 | `clase_procedencia_faltante:ORDINAL→CARDINAL` | 3 | registro de procedencia | `NO-ENCONTRADO` |

## Justificación del Top ≤15

El shortlist se calculó después de crear `cobertura-completa.ok` y contiene quince demandas del ranking completo.

### 1. `disparador_sin_base:riesgo_fiscal_percibido`

- Palanca: nivel 1 — desbloquea el cómputo de mecanismo B/C que hoy consume un disparador sin base medida
- Parámetro convertido: `milpa/src/emisor.py:384`
- Qué falta: base empírica y cableado vivo para el disparador EMISOR-M-2 riesgo_fiscal_percibido
- Contador o mecanismo que movería: gate R3.4 / emisor ejecutable
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 2. `theta_sin_escala:G3.horizonte_temporal`

- Palanca: nivel 2 — RUTA-I, única llave de identificación de los 15; fija la base dimensional de un coeficiente vivo antes de interpretar su consumo
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: base dimensional de θ=horizonte_temporal y escala de salida del generador G3
- Contador o mecanismo que movería: G3 → ahorro informal/planeación; llave CAL-G3
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 3. `ASIGNADO_coef:G3.horizonte_temporal`

- Palanca: nivel 2 — RUTA-I, única llave de identificación de los 15; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.horizonte_temporal
- Contador o mecanismo que movería: G3 → ahorro informal/planeación; llave CAL-G3
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 4. `ASIGNADO_coef:G1.confianza_institucional`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:826`
- Qué falta: magnitud empírica y escala compatible del coeficiente G1.confianza_institucional
- Contador o mecanismo que movería: G1 → mordida/registro y gate R3.4
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 5. `ASIGNADO_coef:G1.radio_confianza`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:826`
- Qué falta: magnitud empírica y escala compatible del coeficiente G1.radio_confianza
- Contador o mecanismo que movería: G1 → puente personal y adopción por confianza
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 6. `ASIGNADO_coef:G3.familismo_apoyo`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.familismo_apoyo
- Contador o mecanismo que movería: G3 → tanda/pooling económico
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 7. `ASIGNADO_coef:G4.confianza_institucional`

- Palanca: nivel 2 — RUTA-C, candidato coobservable; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.confianza_institucional
- Contador o mecanismo que movería: G4 → respuesta a autoridad no confiable
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 8. `ASIGNADO_coef:G4.exposicion_violencia`

- Palanca: nivel 2 — RUTA-C, candidato coobservable; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.exposicion_violencia
- Contador o mecanismo que movería: G4 → protesta/autodefensa y silencio adaptativo
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 9. `ASIGNADO_coef:G2.aversion_riesgo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:827`
- Qué falta: magnitud empírica y escala compatible del coeficiente G2.aversion_riesgo
- Contador o mecanismo que movería: G2 → crédito y decisión bajo riesgo
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 10. `ASIGNADO_coef:G2.sens_estatus`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:827`
- Qué falta: magnitud empírica y escala compatible del coeficiente G2.sens_estatus
- Contador o mecanismo que movería: G2 → consumo compensatorio/aspiracional
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 11. `ASIGNADO_coef:G3.aversion_riesgo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.aversion_riesgo
- Contador o mecanismo que movería: G3 → pooling y ahorro bajo volatilidad
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 12. `ASIGNADO_coef:G4.horizonte_temporal`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.horizonte_temporal
- Contador o mecanismo que movería: G4 → adaptación ante inseguridad
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 13. `ASIGNADO_coef:G4.sens_estatus`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.sens_estatus
- Contador o mecanismo que movería: G4 → respuesta cívica situada
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 14. `ASIGNADO_coef:G5.familismo_apoyo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:830`
- Qué falta: magnitud empírica y escala compatible del coeficiente G5.familismo_apoyo
- Contador o mecanismo que movería: G5 → familia como seguro
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 15. `ASIGNADO_coef:G5.familismo_obligacion`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:830`
- Qué falta: magnitud empírica y escala compatible del coeficiente G5.familismo_obligacion
- Contador o mecanismo que movería: G5 → carga de cuidado/obligación familiar
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

## Cita de gobierno y falsador a catorce días

> Todo sello porta desde hoy el universo bajo el que se tomó; un sello cuyo universo creció queda VENCIDO EN ALCANCE — no refutado, no borrado, no vigente para el territorio nuevo.

**Falsador a catorce días — 2026-09-08:** si para esa fecha ninguna de las quince primeras demandas produce una medición nueva, calibra un parámetro, cambia un contador o desbloquea el mecanismo concreto que su fila nombra, el ranking no añadió señal operativa. En ese caso se revisa la justificación de palanca antes de reutilizar el Top; no se reordena retroactivamente este corte.

## Reproducibilidad y gates

- Script temporal único: `cruce.py`; quedó fuera del repositorio.
- Universo: 59/59 archivos leídos; 0 inaccesibles.
- Índice: 169,474 registros.
- Cruce: 7,117,908 evaluaciones; 2,076 candidatos únicos.
- Revisión: 2,076/2,076.
- Control positivo: `INEGI`, 122,568 hits sobre el mismo índice.
- Archivos entregados: `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` y esta nota.

El TSV conserva quince columnas; la cobertura detallada vive aquí y el resumen compacto se repite en todas las filas de cada demanda. El artefacto no modifica el motor ni adjudica veredictos de Hito D: hace explícito qué oferta podría mover qué parámetro y dónde la oferta actual queda corta.
