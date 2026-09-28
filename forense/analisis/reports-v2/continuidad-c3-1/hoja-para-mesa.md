# Hoja para mesa · GEN2-ASTRA-CONTINUIDAD-C3-1 · P3 (reglas, firmas y pendientes de C3)

Contadores movidos por esta hoja: cero. No adopta ninguna regla, no mide, no escribe en `firmas-pendientes.tsv` ni en `no-corrido.tsv`: el asiento lo hace FIRMAS-21 con el texto de abajo.

## (a) Hoja de reglas: qué se decide

**Qué hay.** `forense/analisis/reports-v2/reglas-propuestas-v1_0.tsv` junta en un solo lugar 107 reglas SI-ENTONCES que Astra/Codex propuso en C3, cada una con su archivo y línea de origen (EJECUTADO, lector csv):

| PR | Qué | Reglas | Con RESULT |
|---|---|---|---|
| #1171 | Confianza, capital no familiar, religiosidad | 10 | 0 |
| #1173 / #1179 | Hojas de consumo y familia (la 2 sustituye a la 1) | 8 + 8 | 0 |
| #1180 | Género, violencia, salud mental | 9 | 0 |
| #1181 | Trabajo, mérito, clasemediero | 8 | 0 |
| #1196 | Finanzas, tecnología, conocimiento | 9 | 0 |
| #1197 | Vejez, migración, pareja | 10 | 1 |
| #1240 | Autoridad, psicología política, México rural | 9 | 0 |
| #1242 | Salud y cuerpo, juventud, tiempo | 10 | 0 |
| #1243 | Interacción, moral, humor, sanción (PROP-C3-*) | 9 | 0 |
| #1246 | Duelo ambiguo (report L91-94) | 4 | 0 |
| #1247 | Síntesis S1–S4 | 4 | 1 |
| #1251 | Genética (hoja, 7) + Genómica L73-74 (2) | 9 | 0 |

Solo 2 de 107 filas citan un RESULT sellado que existe (`RESULT-EDER-UNION-A-P-LIBRE`, `RESULT-ENOE-PISOS-TABLA`; `grep -l` sobre `data/corrida0/CALC-*/resultados.json`). Las otras 105 dicen «sin sellado». Las 107 están en PROPUESTA.

Cuidado al leerla: hay reglas que se repiten entre hojas y reports (consumo-familia 1 y 2; `social-1/social-hoja-reglas.md`, que repite las 10 de #1171 y no se contó dos veces). Las columnas segmento, tier y driver se copiaron de la celda vecina del original y no se normalizaron. Si una regla se va a usar, se lee en su fuente.

**Recomendación: recibir sin adoptar.** Por E.2, una regla solo se adopta dentro de un bloque que mesa fusiona, y tiene que apoyarse en un RESULT. Por eso ninguna de estas es candidata a adopción hoy. Las dos que citan RESULT pueden entrar a un bloque de adopción futuro, pero solo cuando exista un consumidor identificado.

> Texto de firma: «Recibo `reglas-propuestas-v1_0.tsv` (107 reglas C3) como inventario de propuestas. Ninguna se adopta. Una regla pasa a adopción solo en un bloque de mesa con RESULT sellado y consumidor identificado.»

## (b) Firmas pendientes de C3: estado real (A.17, lector csv sobre `forense/firmas-pendientes.tsv`)

| FP | Estado en el TSV | Estado real |
|---|---|---|
| `FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-01` | ABIERTA | Mesa ya la firmó en `2026-09-27-GEN2-RECIBO-ASTRA6-2-ADENDA-1.md` L10 («recibir sin adoptar»), pero la fila nunca se marcó. Solo falta el asiento. |
| `FP-260926-ASTRA6-C3-DINERO-TECNOLOGIA-CONOCIMIENTO-1-9df0-01` | ABIERTA | Igual: firmada en la ADENDA-1, L10. Falta el asiento. |
| `FP-260926-GEN2-ASTRA6-C3-CUIDADO-MIGRACION-PAREJA-1-13c5-02` | ABIERTA | Igual: firmada en la ADENDA-1, L11 (excluir ENADID 2023, sin permiso retroactivo). Falta el asiento. |
| `FP-260927-ASTRA6-C3-AUTORIDAD-CIVISMO-COMUNALIDAD-1-3a1f-01` | ABIERTA | Abierta de verdad (reglas de #1240). |
| `FP-260927-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1-b544-01` | ABIERTA | Abierta de verdad (reglas de #1242). |
| `FP-260927-ASTRA6-C3-SALUD-JUVENTUD-TIEMPO-1-b544-02` | ABIERTA | Abierta de verdad (exposición E.6 de #1242). |
| `ed83-01`, `ed83-02`, `edf7-01`, `9d28-01`, `5803-01`, `92f8-01` | FIRMADA | Ya firmadas (FIRMAS-20). No hay nada que hacer. |

Ninguna FP lleva `RECIBO-ASTRA6-3` en su id: las tres decisiones de ese recibo siguen sin fila (NC `8c5c-02`).

**Recomendación.** Las tres ya firmadas (13c5-01, 9df0-01 y 13c5-02) se marcan FIRMADA en FIRMAS-21 citando la ADENDA-1. No se firman otra vez. Para las tres abiertas, este es el texto:

> 3a1f-01 · «Recibo los tres reports de autoridad, civismo y comunalidad y sus reglas como propuestas (RP-C3 de #1240 en `reglas-propuestas-v1_0.tsv`); no adopto ninguna.»
> b544-01 · «Recibo las diez reglas de salud, juventud y tiempo como propuestas (RP-C3 de #1242); no adopto ninguna.»
> b544-02 · «Adjudico la exposición documental a EDER2025, ENADID2023, ENCODAT2025 y a las publicaciones ENUT2024, ENIF2024 y ENSU-dic2025: se excluyen esas fuentes del producto saneado, se mantiene la reserva y no hay autorización retroactiva ni lectura futura (E.6).»

## (c) Pendientes (NC) de C3 dictaminados por objeto (lector csv sobre `forense/no-corrido.tsv`)

| NC | Estado actual | Dictamen |
|---|---|---|
| `NC-260928-GEN2-RECIBO-ASTRA6-3-8c5c-04` (firewall en Autoridad y Rural; [v2.16] en 3 reports) | ABIERTA | **CERRABLE-POR-ESTE-ACTO**. P2 añadió el bloque `C3-V216` a los 31 reports y a INDICE: `grep -l C3-V216` da 32 archivos, y «firewall» aparece en Autoridad, Rural y Juventud. |
| `…-8c5c-06` (afirmaciones de salud sin texto; firewall en Juventud) | ABIERTA | **SIGUE-ABIERTA**, a medias. El firewall de Juventud ya quedó. `salud/afirmaciones.tsv` todavía no tiene la columna de texto. Sucesor: pasada editorial C3 o recibo sucesor. |
| `…-8c5c-05` (tres esquemas de tabla) | ABIERTA | **SIGUE-ABIERTA**. P2 no unificó los esquemas. Sucesor: encargo corto de corrección C3. |
| `…-8c5c-07` (exposición de #1242) | ABIERTA | **SIGUE-ABIERTA**. Sucesor: FIRMAS-21 (b544-02, arriba). |
| `…-8c5c-08` (citas de la muestra de #1243 sin abrir) | ABIERTA | **SIGUE-ABIERTA**. Sucesor: un recibo con red sobre esas 10 filas. |
| `…-8c5c-09` (9 PROP-C3 sin FP) | ABIERTA | **SIGUE-ABIERTA**. Esas reglas ya están en el TSV (RP-C3 de #1243). Sucesor: FIRMAS-21 asienta la fila, con el texto de (a). |
| `…-8c5c-01`, `-02`, `-03`, `-10`, `-11`, `-12`, `-13` | ABIERTA | **DE-OTRO-CARRIL**: son de C1 o del ejecutor (#1241, #1221, #1229, #1222). |
| `NC-260926-GEN2-ASTRA6-C3-CONSUMO-FAMILIA-2-9d28-01` (nuevo recibo de Claude) | ABIERTA | **SIGUE-ABIERTA**. RECIBO-ASTRA6-1 probablemente satisfizo el objeto (supuesto, no verificado aquí). Sucesor: FIRMAS-21 la cierra citando esa nota, después de verificarla. |
| `…-9d28-02` (validación numérica de RESULT) | ABIERTA | **DE-OTRO-CARRIL** (C1). |
| `…-9d28-03` (cifras externas retiradas del v1) | ABIERTA | **SIGUE-ABIERTA**. Sucesor: lectura primaria en un recibo con red. |
| `NC-260926-GEN2-ASTRA6-C3-TRABAJO-MOVILIDAD-1-ed83-01` (revisión humana y recibo) | ABIERTA | **SIGUE-ABIERTA**. Sucesor: un recibo de producto por circuito de mesa. |
| `…-ed83-03` (cifra CEEY con condicionamiento disputado) | ABIERTA | **SIGUE-ABIERTA**. Sucesor: aclaración primaria del CEEY. |
| `…-ed83-02` | CERRADA | Ya cerrada por FIRMAS-20. |

## (d) Tres firmas nuevas que proponen los recibos de este acto (`forense/notas/2026-09-28-GEN2-ASTRA-CONTINUIDAD-C3-1/`)

1. **El report de genómica está entero en inglés** (`pr-1251.md` L28 y L35; §3 exige «todo en español»). **Recomendación:** aceptarlo tal como está en v2, con una nota en INDICE, y traducirlo en v3. Traducirlo ahora reescribiría un report de Astra sin cifras nuevas.
   > «Acepto el report de genómica en inglés como v2 con la advertencia; la traducción al español entra como requisito del v3.»
2. **Cifra de cuerpos en el report de duelo** (`pr-1246.md` L39): L8 dice «más de 70 mil cuerpos» y cita F03, pero DUEL-026 deja «más de 72 mil» (IBERO) como SIN-CIFRA. **Recomendación:** dejar la cifra de L8 marcada «pendiente de cotejo de fuente y corte» y no publicarla como número verificado hasta que un acto con red compruebe si F03 es una fuente distinta.
   > «La cifra “más de 70 mil cuerpos” del report de duelo queda como pendiente de cotejo; no se usa como dato verificado hasta que un acto con red confirme fuente y corte.»
3. **CIE-11 sin cotejar** (`pr-1246.md` L41): dos ROMPE clínicos se apoyan solo en DSM-5-TR. **Recomendación:** mantener los ROMPE con la reserva «una sola fuente» y encargar el cotejo de CIE-11 a un acto con red.
   > «Mantengo los ROMPE DUEL-X04 y DUEL-018 con la reserva “solo DSM-5-TR”; el cotejo de CIE-11 queda para un acto con red.»
