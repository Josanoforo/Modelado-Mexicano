# Política y vida cívica · completar INE, ENCUP y LAPOP

Acto `ASTRA5-U3-POLITICA-COMPLETAR` (0-bis `d459637e`), 23/sep/2026, CAJA,
sucesor de `ASTRA5-U3-POLITICA` (#1084, fusionado en `72595501`). Contadores:
este acto sella **seis CALC nuevos** con `cuenta_gen2: SI` y `adopta: NO`;
no mueve `celdas_validadas` ni adopta nada. Todas las cifras son
**RETROSPECTIVAS**: no hay emisión prospectiva, serie calibrada ni retador.
Se conservan intactas las tablas de #1084 (`RESULTADOS-ASTRA5-U3.md`). Cada
instrumento va en su tabla, con su unidad: registros administrativos INE,
entrevistados ENCUP y entrevistados LAPOP. Nunca se mezclan.

## Tabla 1 · INE, producto administrativo

**Se conserva** `CALC-INE-PISOS-2024-0001`, marcas de voto sobre lista
nominal en los cuadernillos 2024 (Conteos Censales DECEyEC). No se
recalcula.

**Nuevo:** `CALC-INE-PISOS-SICEE-0002`. Participación publicada por el
SICEE-INE: votos totales sobre lista nominal, nacional, por cargo y año,
1991–2024. Es registro administrativo, sin IC de muestreo. `total_votos`
incluye nulos y candidaturas no registradas, así que no es voto válido.
Cuando las dos distribuciones SICEE dan la misma tasa se muestra una sola;
si difieren, se muestran ambas (`d1`/`d2`). `s/d` = `SIN-DATO-PUBLICADO`.
Unidad: % de la lista nominal.

| Año | `PRE` | `DIP_MR` | `DIP_RP` | `SEN` | `SEN_MR` | `SEN_RP` | `CONS_POP` | `CONS_POP_RM` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1991 | · | 65.5 | 66.0 | 66.3 | · | · | · | · |
| 1994 | 77.2 | 75.9 | 76.1 | d1 77.2 / d2 s/d | · | · | · | · |
| 1997 | · | 57.0 | 57.7 | · | · | 57.8 | · | · |
| 2000 | 64.0 | 63.2 | 63.6 | · | 63.4 | 63.8 | · | · |
| 2003 | · | 41.2 | 41.3 | · | · | · | · | · |
| 2006 | 58.2 | 57.7 | 58.1 | · | d1 58.0 / d2 58.5 | 58.5 | · | · |
| 2009 | · | 44.6 | d1 s/d / d2 44.8 | · | · | · | · | · |
| 2012 | 63.1 | 62.7 | d1 s/d / d2 63.0 | · | 62.9 | d1 s/d / d2 63.3 | · | · |
| 2015 | · | 47.4 | d1 s/d / d2 47.5 | · | · | · | · | · |
| 2018 | 63.4 | 62.8 | d1 s/d / d2 62.6 | · | 62.9 | d1 s/d / d2 62.3 | · | · |
| 2021 | · | 52.3 | d1 s/d / d2 52.6 | · | s/d | · | s/d | · |
| 2022 | · | · | · | · | · | · | · | s/d |
| 2023 | · | · | · | · | s/d | · | · | · |
| 2024 | 61.0 | 60.0 | d1 s/d / d2 60.5 | · | 60.2 | d1 s/d / d2 60.9 | · | · |

Control aritmético: la tasa recalculada con los enteros publicados coincide
con `porcentaje_participacion` en todas las filas con dato, con una
diferencia máxima de 0.00005 pp. `distribucion` es una llave SICEE que el
corpus no documenta, y se conserva opaca. En 12 pares cargo×año las dos
distribuciones difieren en votos o en lista, sobre todo las RP de
2009–2024. Por eso no se suman ni se elige una. Consulta popular 2021 y
revocación de mandato 2022 no son elecciones, y en el JSON nacional salen
`s/d`. Las extraordinarias de senado 2021 y 2023 también salen `s/d`.

Límites: los años presidenciales e intermedios son objetos distintos. La
tabla describe; no atribuye causas a las diferencias entre años. La tasa
por entidad existe (`a6_sicee_participacion_entidad_1991_2024`), pero queda
dictaminada y sin medir en este acto. Los demás objetos electorales del
manifiesto (SICEE por casilla, SICEE local, OPLE, bases académicas) quedan
dictaminados en `ine-objetos-restantes-v1_0.tsv`. Ninguno es producto
administrativo federal pendiente que deba sumarse a éste.

## Tabla 2 · ENCUP 2012

**Se conserva** `CALC-ENCUP-PISOS-2012-0003`: descripción de entrevistados
sin representatividad. **No hay CALC nuevo.** La base trae `factor` y `POND`,
pero sin documento que los defina ni variable de estrato. Esto corrige la
NC df0d-02, que decía que el peso no estaba en el XLSX. Tras buscar en el
corpus y en internet, falta diseño acreditable, así que no se pondera. Lo
que falta exactamente, y las otras bases (cuestionarios ENCUP sin base y la
encuesta UNAM, que es otro instrumento), está en
`encup-diseno-dictamen-v1_0.md`.

## Tabla 3 · LAPOP México por ola

Unidad: persona entrevistada. Cada celda es `% [IC95 bootstrap de UPM dentro
de estrato], n`. Olas presenciales:

| Reactivo y evento | 2004 | 2006 | 2019 | 2023 |
|---|---:|---:|---:|---:|
| Confianza alta en la Policía (`b18` 6–7 de 7) | 16.9 [14.4–19.6], n=1 530 | 13.6 [11.3–16.0], n=1 523 | 10.7 [9.1–12.5], n=1 558 | 14.0 [11.9–16.2], n=1 618 |
| Confianza alta en partidos (`b21` 6–7 de 7) | 14.5 [12.0–17.2], n=1 531 | 14.6 [12.5–16.8], n=1 512 | 10.9 [9.3–12.6], n=1 533 | 11.2 [9.5–13.0], n=1 613 |
| Interés en política mucho/algo (`pol1` 1–2 de 4) | ausente | 40.3 [37.1–43.7], n=1 544 | 36.8 [34.2–39.3], n=1 569 | 34.7 [32.4–37.0], n=1 618 |
| Eficacia externa alta (`eff1` 6–7 de 7) | ausente | ausente | 33.4 [30.9–35.8], n=1 543 | 27.5 [25.3–29.8], n=1 616 |
| Eficacia interna alta (`eff2` 6–7 de 7) | ausente | ausente | 24.1 [22.0–26.3], n=1 537 | 20.5 [18.5–22.5], n=1 607 |
| Tolerancia: votar (`d1` 6–10 de 10) | 62.3 [58.6–65.8], n=1 473 | 58.9 [55.1–63.0], n=1 495 | 59.3 [57.2–61.5], n=1 539 | ausente |
| Tolerancia: manifestarse (`d2` 6–10) | 66.8 [63.5–70.1], n=1 501 | 67.8 [64.4–71.3], n=1 498 | 65.4 [63.1–67.6], n=1 547 | ausente |
| Tolerancia: postularse (`d3` 6–10) | 58.6 [55.3–62.0], n=1 479 | 54.2 [49.9–58.3], n=1 493 | 35.9 [33.4–38.5], n=1 537 | 35.8 [33.0–38.7], n=1 607 |
| Tolerancia: discurso en TV (`d4` 6–10) | 60.3 [57.0–63.5], n=1 485 | 55.4 [51.7–59.3], n=1 500 | 39.3 [36.8–41.8], n=1 541 | 33.4 [30.4–36.3], n=1 606 |
| Oferta a la persona (`clien1na` sí) | ausente | ausente | 17.2 [15.3–19.1], n=1 578 | ausente |
| Oferta a un conocido (`clien1n` sí) | ausente | ausente | 28.4 [26.5–30.4], n=1 574 | ausente |

Fuentes de cada celda:
- `b18` y `clien1na` de 2019: `CALC-LAPOP-PISOS-2019-0001` (#1084),
  citados y no re-medidos.
- 2023 `b18`/`b21`: `RESULT-LAPOP-PISOS-2023-POL001`, el contrato U0
  POL-001.
- «ausente»: el reactivo no está en el archivo de esa ola (dictamen
  `lapop-dictamen-olas-v1_0.tsv`).

La ola 2021 va aparte. Es una **ruptura de modo y población**: telefónica
CATI por marcación aleatoria a celulares, sólo personas con celular, con
peso `wt`.

| Reactivo y evento | 2021 telefónica |
|---|---:|
| Confianza alta en la Policía (`b18` 6–7 de 7) | 12.9 [9.9–16.0], n=716 |
| Confianza alta en partidos (`b21` 6–7 de 7) | 11.8 [9.8–13.8], n=1 439 |

En 2021 cada entrevista es su propia UPM. `b21` se preguntó a media
muestra (n = 1 439, Core B). `b18` sólo llega a n = 716 de 2 998:
2 279 filas no tienen código sustantivo (inaplicable, no sabe o no
responde; el medidor no los separa) y 3 más faltan por diseño o peso. El
reporte técnico describe la división en Core A/B, pero no explica que
`b18` quede en una cuarta parte. Se reporta tal cual; el universo efectivo
de `b18` 2021 es una submuestra no documentada más allá de la división
aleatoria.

Lectura admitida por el dictamen:
- **Interés**, **eficacia** y **confianza alta** en policía y partidos se
  describen en las olas presenciales equivalentes, con fechas y marcos
  explícitos:
  - 2004: marzo, sitios por sección electoral.
  - 2006: último mes de la campaña presidencial.
  - 2019: enero–marzo, marco padrón 2010.
  - 2023: mayo–julio, marco Censo 2020.
- **Tolerancia `d3`/`d4`**: los valores de 2019 y 2023 están muy por debajo
  de 2004 y 2006. No se lee como cambio de actitud. Cuatro diferencias de
  instrumento lo impiden:
  - En 2019, D3 se antepone con «Siempre pensando en los que hablan mal…».
  - En 2023, D3 y D4 van sin D1 y D2 antes.
  - Los marcos y el modo de captura cambian (papel frente a dispositivo).
  - No hay cuestionario 2006 en el corpus.

  Quedan como puntos por ola con esas reservas, sin serie ni detección de
  cambio.
- **Oferta clientelar**: sólo existe en 2019. «A la persona»
  (`clien1na`) y «a un conocido» (`clien1n`) son objetos distintos y no se
  suman. Ninguno es recepción, aceptación ni voto comprado.

Todos los CALC son `SIN-HISTORIA-PARA-CALIBRAR`. En 2004 el peso es 1 por
ficha técnica, y `wt` viene vacío en las 1 556 filas. Las UPM de 2004
(estado × sección) son 131, frente a los 130 sitios que reporta la ficha.

## RESULT, CALC y hash

| Instrumento | CALC | RESULT | sello (sha256) |
|---|---|---|---|
| INE SICEE | `CALC-INE-PISOS-SICEE-0002` | `RESULT-INE-PISOS-SICEE-FILAS`, `-TABLA` | `3dcafc831b6f5a7c2af3563c957b8782b200a604fe0a3f845b6cdf5f0d86bb33` |
| LAPOP 2004 | `CALC-LAPOP-PISOS-2004-0002` | `RESULT-LAPOP-PISOS-2004-FILAS`, `-TABLA` | `7cbc822dc869e7281e7f09d85e24a60d286b016e563634a40b9d51680eed280f` |
| LAPOP 2006 | `CALC-LAPOP-PISOS-2006-0001` | `RESULT-LAPOP-PISOS-2006-FILAS`, `-TABLA` | `f8ae4528c20ecbd2bb1b1e3693602f773900d86d3436ebc7aff9584bd8459e77` |
| LAPOP 2019 | `CALC-LAPOP-PISOS-2019-0002` | `RESULT-LAPOP-PISOS-2019-COMPLEMENTO-FILAS`, `-TABLA` | `a143e081e4347ce4a46cca313059e7458a0c79edcea351f9c228ca5c052e62f3` |
| LAPOP 2021 | `CALC-LAPOP-PISOS-2021-0001` | `RESULT-LAPOP-PISOS-2021-FILAS`, `-TABLA` | `0d057b0d8875792cc54a473182c489affc89a3355698639035c09d47c0340ade` |
| LAPOP 2023 | `CALC-LAPOP-PISOS-2023-0001` | `RESULT-LAPOP-PISOS-2023-FILAS`, `-POL001`, `-TABLA` | `c6e7cd579eed339ba6e2386763b536b2b959d74223d91458324c88cdc6acd13c` |

Los seis tienen replay `REPRODUCE`/`IDENTICO` asentado en
`forense/replay-evidencia.tsv`. `CALC-LAPOP-PISOS-2004-0001` y
`CALC-INE-PISOS-SICEE-0001` fallaron antes del sello y no escribieron nada.
Quedan congelados sin editar. La causa y la corrección están en
`LAPOP-PISOS-OLAS-spec-v1_1.md` y en `INE-SICEE-PARTICIPACION-spec-v1_1.md`.

## Enlace editorial · U0 POL-001

| Afirmación | Componente observado | Juicio |
|---|---|---|
| «Confianza alta en instituciones que funcionan, baja en partidos y policía» (report político, L14 Hallazgo 1) | LAPOP 2023 `b18`/`b21`, proporción en 6–7 de 7 | **CONFIRMA** sólo el componente de nivel: una minoría declara confianza alta en policía y en partidos. **Sin contraste directo** de la jerarquía, porque POL-001 contrata sólo dos instituciones. Tampoco de la «calibración racional del desempeño», porque B18/B21 no miden desempeño ni experiencia. |
| Participación responde a interés y eficacia | LAPOP `pol1`/`eff1`/`eff2`; SICEE marcas sobre lista | **Sin contraste directo**: ningún cruce individual une interés o eficacia con votar, y la tasa SICEE es agregada. |
| Clientelismo: la oferta implica voto comprado | 2019 `clien1na` y `clien1n` | **Sin contraste directo** del efecto: la oferta se declara, no se asigna al azar; «a un conocido» es un reporte sobre terceros; el secreto del voto limita la inferencia. |

## Límites, tier y falsadores

- **Clase de evidencia**: (a) datos primarios en México, en los tres
  instrumentos.
- **Tier**:
  - SICEE: fuerte para el conteo administrativo publicado.
  - LAPOP presencial: media-fuerte para el nivel nacional de cada ola.
  - LAPOP 2021: media, por cobertura sólo de quienes tienen celular.
  - ENCUP 2012: descriptiva, sin representatividad.
- **Falsadores**: un nivel LAPOP de una ola se contradice si otra muestra
  probabilística nacional presencial del mismo periodo, con el mismo texto
  y umbral, da un IC que no se solapa. La tasa SICEE se contradice si los
  cómputos por casilla (`sicee_federal_*`), reagregados con la misma
  definición, se apartan de la cifra publicada más allá del redondeo.

## Auditoría de rigor extremo

- **¿Cuántos contadores movió este trabajo?** Seis CALC sellados, que
  quedan en disco sin registrar hasta el canal de `main`. Cero adopciones.
  `celdas_validadas` intacto.
- **¿En qué escala está cada cantidad?**
  - Personas entrevistadas: proporción sobre 1–7, 1–4, 1–10 o sí/no, con el
    umbral declarado.
  - Registros administrativos: marcas sobre lista nominal.

  Ninguna cifra de persona se promedia ni se compara con una de registro.
- **¿Qué es PROSPECTIVA y qué RETROSPECTIVA?** Todo es RETROSPECTIVA.
- **Pobreza y violencia confundidas con cultura.** La confianza baja en
  policía puede responder a experiencias de victimización y extorsión, no a
  una disposición cultural. Este acto no separa esos canales.
- **Sobregeneralización.** Un marginal nacional no dice nada de rural,
  indígena ni popular. La ola 2021 excluye a quien no tiene celular.
- **Lectura simplista peligrosa.**
  - Leer la caída de `d3`/`d4` como «México se volvió intolerante».
  - Leer `clien1n` como compra de votos.
  - Leer la participación de 2003 o 2009 como apatía, sin notar que son
    elecciones intermedias.
- **Estado del corpus escrito a mano.** Ninguna cifra de estas tablas se
  tecleó: las tablas se generaron desde los `resultados.json` sellados.
