# Cruce exhaustivo de oferta y demanda del motor · v0.1

Fecha de revisión: **2026-08-25**. Base real: `ba0a7e463c32e1e94228d02630079df3eee0d6fc`. Redacción de referencia: `9e9132d`.

## Resultado ejecutivo

El cruce materializa **42 demandas únicas** y **49 filas finales**. Recorrió **59 archivos**, de los cuales **59** fueron leídos y **0** quedaron registrados como inaccesibles; indexó **169,474 registros**. El producto cartesiano efectivamente evaluado fue de **7,117,908 pares demanda×registro**. No hubo muestra, top-k, corte por puntuación ni salida temprana.

Los **2,076 hits únicos deduplicados** fueron revisados semánticamente, uno por uno en la tabla de revisión temporal; **2,076/2,076** quedaron cubiertos. Inventarios, `estado-activos`, `reportes-inspeccion`, manifiesto y ledgers se trataron como pistas de procedencia. Un hit descartado no pasó al TSV. Solo una tupla con fuente + instrumento/ola + reactivo y existencia semántica verificada puede convertirse en oferta.

Por fila final: `EXISTE-NO-SATISFACE`=7, `NO-ACCESIBLE`=1, `NO-ENCONTRADO`=41. La precarga de #359 conserva siete ofertas verificadas que no satisfacen y una candidata `NO-ACCESIBLE`; el resto de los hits de curación no sustituyó esa prueba.

La decisión operativa principal es clara: la primera palanca es `disparador_sin_base:riesgo_fiscal_percibido`, porque el emisor ejecutable ya consume ese concepto para el gate R3.4 sin una base medida. La segunda es la escala de `G3.horizonte_temporal`: es la única `RUTA-I` de los quince coeficientes, pero sigue `SUBDETERMINADA-PERSISTENTE`.

## Base, precedencia y alcance

- `origin/main` capturado e incorporado: `ba0a7e463c32e1e94228d02630079df3eee0d6fc`; contiene la versión vigente de R2.1 y los cambios de PASE-FALSADORES posteriores a `5db163b`.
- `9e9132d` es ancestro de la base real.
- `5db163b` es ancestro de la base vigente y se conserva como base de comparación, no como base de esta corrida.
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

La indexación abarcó todas las filas TSV/CSV, cada entrada lógica de los YAML, cada línea lógica enumerable de Markdown, JSON/JSONL y los artefactos de autoridad. El gate exige siempre `leídos + no accesibles = universo`.

## Método de cruce y revisión

Para cada demanda se evaluaron los 169,474 registros. La normalización solo ordenó la búsqueda léxica: cada frase semilla se comparó con frontera de token, evitando falsos positivos como `face` dentro de `satisface`. No se excluyó ningún registro por puntuación. La deduplicación usó exclusivamente igualdad exacta del texto y conservó todos los localizadores `archivo:línea`.

Cada hit único tuvo una fila en `revision.tsv`. Una coincidencia en esquema/script, inventario, manifiesto, estado o ledger se marcó `DESCARTADO_NO-CANDIDATO` con motivo concreto. Solo la autoridad semántica capaz de resolver simultáneamente fuente, ola y variable podía promoverse desde el índice. Las candidatas de #359 se precargaron desde su apertura real a nivel de reactivo, fuera de la búsqueda léxica, y conservaron su veredicto y su estado de fetch.

La auditoría de los 2,076 hits quedó cerrada así: **1,282** pistas de procedencia/inspección; **356** menciones sin tupla completa; **203** menciones de gobernanza; **196** pistas explícitamente no verificadas, marcadas `SIN-FETCH`; y **39** hits de inventario ciego. La suma es 2,076; ninguno queda sin motivo.

## Precarga verificada de #359 · censo R3.4 B/C

La receta reejecutada fue `python3 tools/censo_r34_bc.py <salida.jsonl>` sobre `data/raw` completo. Produjo **20,838 archivos examinados**, **20,280** con texto, control `FISCAL` en **232**, control `PERSONAL` en **97** y **22** co-hits DIGITAL×FISCAL. Delta contra #359: archivos **+0**, texto **+0**, FISCAL **+0**, PERSONAL **+0**.

Las candidatas abiertas permanecen en `forense/ficha-r34-condBC-v1_0.md:74-88`: ENIF, ENDUTIH, IFT SFD, ENCIG, ECF Banxico, ENSAFI y ENAFIN. Las series agregadas de Banxico y la búsqueda negativa de una encuesta CoDi no se convirtieron en filas de oferta porque no resuelven un reactivo individual.

## Delta contra la corrida basada en `5db163b`

| métrica | `5db163b` | base vigente | delta |
|---|---:|---:|---:|
| demandas únicas | 42 | 42 | +0 |
| archivos de universo | 59 | 59 | +0 |
| registros indexados | 169,474 | 169,474 | +0 |
| evaluaciones | 7,117,908 | 7,117,908 | +0 |
| hits brutos | 2,076 | 2,076 | +0 |
| hits únicos revisados | 2,076 | 2,076 | +0 |
| filas TSV | 1,422 | 49 | -1,373 |

La reducción de filas TSV no es un recorte del censo: es el efecto de restaurar el contrato semántico. En la corrida anterior, una pista léxica podía convertirse indebidamente en fila `EXISTE-NO-SATISFACE`; ahora los 2,076 hits se revisan, pero solo las ofertas resolubles sobreviven.

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
| 2 | `theta_sin_escala:G3.horizonte_temporal` | 2 | G3 → ahorro informal/planeación; llave CAL-G3 | `NO-ENCONTRADO` |
| 3 | `ASIGNADO_coef:G3.horizonte_temporal` | 2 | G3 → ahorro informal/planeación; llave CAL-G3 | `NO-ENCONTRADO` |
| 4 | `ASIGNADO_coef:G1.confianza_institucional` | 2 | G1 → mordida/registro y gate R3.4 | `NO-ENCONTRADO` |
| 5 | `ASIGNADO_coef:G1.radio_confianza` | 2 | G1 → puente personal y adopción por confianza | `NO-ENCONTRADO` |
| 6 | `ASIGNADO_coef:G3.familismo_apoyo` | 2 | G3 → tanda/pooling económico | `NO-ENCONTRADO` |
| 7 | `ASIGNADO_coef:G4.confianza_institucional` | 2 | G4 → respuesta a autoridad no confiable | `NO-ENCONTRADO` |
| 8 | `ASIGNADO_coef:G4.exposicion_violencia` | 2 | G4 → protesta/autodefensa y silencio adaptativo | `NO-ENCONTRADO` |
| 9 | `ASIGNADO_coef:G2.aversion_riesgo` | 2 | G2 → crédito y decisión bajo riesgo | `NO-ENCONTRADO` |
| 10 | `ASIGNADO_coef:G2.sens_estatus` | 2 | G2 → consumo compensatorio/aspiracional | `NO-ENCONTRADO` |
| 11 | `ASIGNADO_coef:G3.aversion_riesgo` | 2 | G3 → pooling y ahorro bajo volatilidad | `NO-ENCONTRADO` |
| 12 | `ASIGNADO_coef:G4.horizonte_temporal` | 2 | G4 → adaptación ante inseguridad | `NO-ENCONTRADO` |
| 13 | `ASIGNADO_coef:G4.sens_estatus` | 2 | G4 → respuesta cívica situada | `NO-ENCONTRADO` |
| 14 | `ASIGNADO_coef:G5.familismo_apoyo` | 2 | G5 → familia como seguro | `NO-ENCONTRADO` |
| 15 | `ASIGNADO_coef:G5.familismo_obligacion` | 2 | G5 → carga de cuidado/obligación familiar | `NO-ENCONTRADO` |
| 16 | `ASIGNADO_coef:G5.radio_confianza` | 2 | G5 → apoyo familiar y red de confianza | `NO-ENCONTRADO` |
| 17 | `ASIGNADO_coef:G6.deferencia` | 2 | G6 → jerarquía R2.1 y retroalimentación R10.2 | `NO-ENCONTRADO` |
| 18 | `theta_sin_escala:G2.aversion_riesgo` | 2 | G2 → crédito y decisión bajo riesgo | `NO-ENCONTRADO` |
| 19 | `theta_sin_escala:G2.sens_estatus` | 2 | G2 → consumo compensatorio/aspiracional | `NO-ENCONTRADO` |
| 20 | `theta_sin_escala:G3.aversion_riesgo` | 2 | G3 → pooling y ahorro bajo volatilidad | `NO-ENCONTRADO` |
| 21 | `theta_sin_escala:G4.horizonte_temporal` | 2 | G4 → adaptación ante inseguridad | `NO-ENCONTRADO` |
| 22 | `theta_sin_escala:G4.sens_estatus` | 2 | G4 → respuesta cívica situada | `NO-ENCONTRADO` |
| 23 | `theta_sin_escala:G5.familismo_obligacion` | 2 | G5 → carga de cuidado/obligación familiar | `NO-ENCONTRADO` |
| 24 | `theta_sin_escala:G6.deferencia` | 2 | G6 → jerarquía R2.1 y retroalimentación R10.2 | `NO-ENCONTRADO` |
| 25 | `disparador_sin_base:friccion_uso` | 3 | R3.4 / vocabulario EMISOR-M-2 (friccion_uso) | `NO-ENCONTRADO` |
| 26 | `disparador_sin_base:utilidad_marginal_sobre_sustituto` | 3 | R3.4 / vocabulario EMISOR-M-2 (utilidad_marginal_sobre_sustituto) | `NO-ENCONTRADO` |
| 27 | `disparador_sin_base:lado_obligado` | 3 | R3.4 / vocabulario EMISOR-M-2 (lado_obligado) | `NO-ENCONTRADO` |
| 28 | `disparador_sin_base:sancion` | 3 | R3.4 / vocabulario EMISOR-M-2 (sancion) | `NO-ENCONTRADO` |
| 29 | `disparador_sin_base:dato_sensible` | 3 | R3.4 / vocabulario EMISOR-M-2 (dato_sensible) | `NO-ENCONTRADO` |
| 30 | `falsador_sin_fuente:R3.4` | 3 | gate R3.4 | `NO-ENCONTRADO` |
| 31 | `falsador_sin_fuente:R2.1` | 3 | Hito D R2.1 | `NO-ENCONTRADO` |
| 32 | `falsador_sin_fuente:R2.2` | 3 | Hito D R2.2 | `NO-ENCONTRADO` |
| 33 | `falsador_sin_fuente:R8.2` | 3 | Hito D R8.2 | `NO-ENCONTRADO` |
| 34 | `falsador_sin_fuente:R10.1` | 3 | Hito D R10.1 | `NO-ENCONTRADO` |
| 35 | `falsador_sin_fuente:R10.2` | 3 | Hito D R10.2 | `NO-ENCONTRADO` |
| 36 | `falsador_sin_fuente:R10.3` | 3 | Hito D R10.3 | `NO-ENCONTRADO` |
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
- Qué falta: CoDi y percepción de riesgo fiscal/vigilancia
- Contador o mecanismo que movería: gate R3.4 / emisor ejecutable
- Veredicto A.4 secundario: `EXISTE-NO-SATISFACE`

### 2. `theta_sin_escala:G3.horizonte_temporal`

- Palanca: nivel 2 — RUTA-I, única llave de identificación de los 15; fija la base dimensional de un coeficiente vivo antes de interpretar su consumo
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: base dimensional de θ=horizonte_temporal y escala de salida del generador G3
- Contador o mecanismo que movería: G3 → ahorro informal/planeación; llave CAL-G3
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 3. `ASIGNADO_coef:G3.horizonte_temporal`

- Palanca: nivel 2 — RUTA-I, única llave de identificación de los 15; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.horizonte_temporal
- Contador o mecanismo que movería: G3 → ahorro informal/planeación; llave CAL-G3
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 4. `ASIGNADO_coef:G1.confianza_institucional`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:826`
- Qué falta: magnitud empírica y escala compatible del coeficiente G1.confianza_institucional
- Contador o mecanismo que movería: G1 → mordida/registro y gate R3.4
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 5. `ASIGNADO_coef:G1.radio_confianza`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:826`
- Qué falta: magnitud empírica y escala compatible del coeficiente G1.radio_confianza
- Contador o mecanismo que movería: G1 → puente personal y adopción por confianza
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 6. `ASIGNADO_coef:G3.familismo_apoyo`

- Palanca: nivel 2 — RUTA-A, asociación ya corrida; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.familismo_apoyo
- Contador o mecanismo que movería: G3 → tanda/pooling económico
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 7. `ASIGNADO_coef:G4.confianza_institucional`

- Palanca: nivel 2 — RUTA-C, candidato coobservable; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.confianza_institucional
- Contador o mecanismo que movería: G4 → respuesta a autoridad no confiable
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 8. `ASIGNADO_coef:G4.exposicion_violencia`

- Palanca: nivel 2 — RUTA-C, candidato coobservable; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.exposicion_violencia
- Contador o mecanismo que movería: G4 → protesta/autodefensa y silencio adaptativo
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 9. `ASIGNADO_coef:G2.aversion_riesgo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:827`
- Qué falta: magnitud empírica y escala compatible del coeficiente G2.aversion_riesgo
- Contador o mecanismo que movería: G2 → crédito y decisión bajo riesgo
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 10. `ASIGNADO_coef:G2.sens_estatus`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:827`
- Qué falta: magnitud empírica y escala compatible del coeficiente G2.sens_estatus
- Contador o mecanismo que movería: G2 → consumo compensatorio/aspiracional
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 11. `ASIGNADO_coef:G3.aversion_riesgo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:828`
- Qué falta: magnitud empírica y escala compatible del coeficiente G3.aversion_riesgo
- Contador o mecanismo que movería: G3 → pooling y ahorro bajo volatilidad
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 12. `ASIGNADO_coef:G4.horizonte_temporal`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.horizonte_temporal
- Contador o mecanismo que movería: G4 → adaptación ante inseguridad
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 13. `ASIGNADO_coef:G4.sens_estatus`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:829`
- Qué falta: magnitud empírica y escala compatible del coeficiente G4.sens_estatus
- Contador o mecanismo que movería: G4 → respuesta cívica situada
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 14. `ASIGNADO_coef:G5.familismo_apoyo`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:830`
- Qué falta: magnitud empírica y escala compatible del coeficiente G5.familismo_apoyo
- Contador o mecanismo que movería: G5 → familia como seguro
- Veredicto A.4 secundario: `NO-ENCONTRADO`

### 15. `ASIGNADO_coef:G5.familismo_obligacion`

- Palanca: nivel 2 — SIN-RUTA en el censo vigente; calibra la magnitud de un coeficiente vivo ya consumido por el motor
- Parámetro convertido: `milpa/procedencia.yaml:830`
- Qué falta: magnitud empírica y escala compatible del coeficiente G5.familismo_obligacion
- Contador o mecanismo que movería: G5 → carga de cuidado/obligación familiar
- Veredicto A.4 secundario: `NO-ENCONTRADO`

## Cita de gobierno y falsador a catorce días

### Cita literal de ADENDA 1

> **(a) El defecto, nombrado sin adorno.** El punto (3) de `CAL-G3` declaró el desenlace primario "recodificada en tres estados exhaustivos: formal / informal / ninguno" — una partición mutuamente excluyente. El instrumento no la sostiene: `CRH01`, verbatim en las tres olas, dice **"(CIRCULE TODAS LAS QUE APLIQUEN)"** — es una pregunta de selección múltiple. Un hogar puede marcar Banco y Tanda a la vez; tres estados excluyentes no son construibles desde ahí sin una regla de agregación que la ficha nunca declaró.

Fuente literal: `forense/hitoD-preregistro-v2_0.md:553`.

### Regla de mantenimiento

- **Quién agrega:** la maestra del registro —o quien integre una fuente por delegación explícita— añade la fila en el mismo cambio que incorpora evidencia semántica de fuente, instrumento/ola y reactivo.
- **Cuándo se revalida y caduca:** se revalida antes de cada consumo y ante cualquier cambio en el preregistro, motor, `data/curacion-universo`, inventarios, manifiesto o diseño muestral. La fila caduca al primer SHA que cambie cualquiera de esos insumos sin una nueva revisión; queda `SIN-FETCH` o `NO-ACCESIBLE` hasta revalidarse, nunca `EXISTE-*` por arrastre.
- **Cuándo se promueve:** solo una fila `EXISTE-SATISFACE`, con reactivo abierto, estado `VERIFICADO-REACTIVO`, población/diseño compatibles y ruta parámetro→mecanismo explícita, puede promoverse a un acto medidor. Este cruce no crea ese acto.

**Falsador exacto a catorce días — 2026-09-08:** `<1 medición lanzada ⇒ la maestra registra infraestructura en forense/hallazgos.md.`

## Reproducibilidad y gates

- Script temporal único: `cruce.py`; quedó fuera del repositorio.
- Universo: 59/59 archivos leídos; 0 inaccesibles.
- Índice: 169,474 registros.
- Cruce: 7,117,908 evaluaciones; 2,076 hits únicos.
- Revisión: 2,076/2,076 hits únicos.
- Control positivo: `INEGI` sobre el mismo índice, consignado por demanda en el TSV.
- Gate: `timeout 900 python3 tests/check.py --baseline` → `LÍNEA BASE: VERDE`, sin `--freeze`.
- Archivos entregados: `data/curacion-registro/cruce-oferta-demanda-v0_1.tsv` y esta nota.

El TSV conserva quince columnas; la cobertura detallada vive aquí y el resumen compacto se repite en todas las filas de cada demanda. El artefacto no modifica el motor ni adjudica veredictos de Hito D: hace explícito qué oferta podría mover qué parámetro y dónde la oferta actual queda corta.
