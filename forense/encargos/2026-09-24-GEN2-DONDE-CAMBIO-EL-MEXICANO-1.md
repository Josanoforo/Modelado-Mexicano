# ENCARGO · ACTO GEN2-DONDE-CAMBIO-EL-MEXICANO-1 · El complemento de la tesis: sobre toda conducta adoptada o adoptable con ≥ 3 olas, la serie 2011–2025 por segmento con un dictamen cerrado por conducta — ESTABLE · CAMBIO-SOSTENIDO · SALTO-DE-INSTRUMENTO · SIN-SERIE — y el documento «Dónde sí cambió el mexicano»

> ENTORNO: **CAJA** — olas históricas abiertas (ENVIPE 2011–2025, ENCIG 2011–2025, ENIF 2012–2024, ENUT, ENIGH, ENOE, ENDIREH, MOCIBA). Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `474a126e` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-donde-cambio-el-mexicano-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: sella CALC de serie por instrumento (`cuenta_gen2: SI`, `adopta: NO`); no evalúa prospectivamente; produce un documento de producto (`canon/donde-cambio-el-mexicano-v1_0.md`) con 0 cifras sin RESULT.

## 1 · OBJETIVO
La tesis dice que la persistencia gana; el producto necesita decir **dónde no**: qué conductas cambiaron de verdad entre olas, en qué segmentos, y cuáles «cambios» son saltos de instrumento. (P1) Vocabulario cerrado fijado antes de abrir dato, en la spec: `ESTABLE` (el piso t−1 cubre a t en todas las olas consecutivas con el IC calibrado de persistencia del instrumento), `CAMBIO-SOSTENIDO` (≥ 2 pares consecutivos fuera del IC en la misma dirección), `SALTO-DE-INSTRUMENTO` (un par fuera del IC coincidente con cambio documentado de cuestionario/modo/diseño, citado por texto), `SIN-SERIE` (< 3 olas comparables por texto). Umbrales y reglas de desempate escritos antes de ver una serie. (P2) Universo: toda conducta con RESULT adoptado o adoptable (catálogo U1, marcador, celdas-D) y toda serie ya sellada (`CALC-ENVIPE-SERIE-*` ×8, `CALC-ENCIG-SERIE-*` ×5, `ENUT-SERIE`, `DIN-CREDITO-HISTORIA` ×2, `ENCIG-ORIGEN-MOVIL`, `enif-fintech` ×2): lo sellado se cita y se dictamina, no se re-mide (E.5); lo que falte se mide por instrumento (COMMIT-1 antes de abrir). (P3) Por conducta y segmento: tabla ola × valor × IC × dictamen; IC calibrado de persistencia del instrumento (ENIF #1009, ENCIG #1041; ENVIPE, ENOE, ENDIREH, MOCIBA: se calcula aquí con el mismo método como parámetro reutilizable). (P4) Documento: por dominio, qué cambió (con segmento, magnitud en pp y ola), qué es salto (con la cita del cambio de cuestionario: ENCIG 2017→2019 ya dictaminado `SALTO-SIN-EXPLICAR` en #972), qué es estable; sin adjetivos; unidad en cada cifra; PROSPECTIVA/RETROSPECTIVA (aquí todo RETROSPECTIVA); módulo de auditoría de rigor extremo (¿qué cambio es estructura o crisis —2020— y no cultura?).
«Hecho»: spec con vocabulario y umbrales sellada antes del primer dato (commit citado) · ≥ 1 CALC de serie por instrumento con ≥ 3 olas, `verify` REPRODUCE · tabla con una fila por (conducta, segmento) y dictamen ∈ vocabulario, 0 filas sin dictamen · documento con 0 cifras sin RESULT (test) · resumen en la primera línea: N conductas ESTABLE / CAMBIO-SOSTENIDO / SALTO / SIN-SERIE · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**Mesa, 23/sep (chat, reserva de U5)**: «Dónde sí cambió el mexicano… unificadas bajo un vocabulario cerrado por conducta … fijado antes de leer» (aprobado en bloque como reserva; se activa con este encargo). **Regla 6**, **E.5** (lo sellado se cita), **v2.16 §4** (unidad y escala; RETROSPECTIVA rotulada), **B-bis** (vocabulario cerrado antes de ver el dato).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` series selladas: ENVIPE-SERIE 8, ENCIG-SERIE 5, ENUT-SERIE 1, DIN-CREDITO 2, ENCIG-ORIGEN-MOVIL 1, ENIGH-DUELO 1, enif-fintech 2; dictámenes sueltos: `SALTO-SIN-EXPLICAR` (ENCIG, #972), `TENDENCIA-*` en crédito. IC calibrado: ENIF (35 pp, #1009), ENCIG (#1041). `[SUPUESTO]` que MOCIBA (2015–2025 anual) y ENOE (trimestral) permiten series comparables por texto: el ejecutor lo verifica por cuestionario y dictamina SIN-SERIE donde no.

## 4 · YA HECHO / YA DECIDIDO
`ls canon | grep -c donde-cambio` → 0. `git ls-remote --heads origin | grep -i 'serie\|cambio'` → 0.

## 5 · PIEZAS
P1 spec y vocabulario (COMMIT-1) → P2 inventario de series y lo faltante → P3 medición + IC calibrado por instrumento → P4 tabla y documento.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir olas reservadas · b) reescribir series selladas · c) adoptar; teclear · d) cambiar vocabulario o umbral después de COMMIT-1 · e) NUBE.

## 8 · COMPUERTAS
«Vocabulario y umbrales sellados antes del primer dato» protege: **congelar** (B-bis). «Series selladas se citan, no se re-miden» protege: **borrar/reescribir**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/DONDE-CAMBIO-*`, `data/corrida0/CALC-*-SERIE-*` nuevos, `tools/series/`, `forense/analisis/donde-cambio/`, `canon/donde-cambio-el-mexicano-v1_0.md`, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: series selladas, catálogo (lo cita), marcador, celdas-D. En CAJA: PISOS-GEN2-2 y SALUD (olas distintas por conducta; si coinciden en una ola, solo lectura, no hay conflicto).

## 10 · LO QUE NO HACE · SUCESORES
No predice, no adopta. Sucesores: informe v1.3 §«dónde cambió»; U4 (familias 2027) usa los CAMBIO-SOSTENIDO como candidatos a estimando prospectivo.

## NO-CORRIDO / RESERVAS

- NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-01 · P2 universo «catálogo U1»: 16 filas ENCIG del catálogo no entraron al mapa · DIFERIDO-A:GEN2-DONDE-CAMBIO-EL-MEXICANO-2 · impacto: 16 filas ausentes de la tabla; todas de una ola salvo `adopta_encig2025_luz`, que extendería C-LUZ-DIGITAL a 2023→2025; ningún dictamen de las 7872 cambia · sucesor GEN2-DONDE-CAMBIO-EL-MEXICANO-2.
- NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-02 · P3 series ENDIREH dictaminables · DIFERIDO-A:GEN2-DONDE-CAMBIO-EL-MEXICANO-2: sin crosswalk de módulos ni tabla de comparabilidad por texto · impacto: 6311 series SIN-SERIE · sucesor GEN2-DONDE-CAMBIO-EL-MEXICANO-2.
- NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-03 · P2 ENOE `horas_ocupado`, `ingreso_ocupado_nominal` fuera del mapa · DIFERIDO-A:GEN2-DONDE-CAMBIO-EL-MEXICANO-2 · impacto: ninguno sobre dictámenes (serían SIN-SERIE) · sucesor GEN2-DONDE-CAMBIO-EL-MEXICANO-2.
- NC-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-04 · «Hecho»: CALC por instrumento para los ocho menores · SUSTITUIDO-POR:CALC-OTROS-SERIE-DICTAMEN-0001, que absorbe los ocho (21 SIN-SERIE); nada queda huérfano · impacto: ninguno · sucesor GEN2-DONDE-CAMBIO-EL-MEXICANO-2.

## CONSUMIDO

PR #1125 (rama `acto/gen2-donde-cambio-el-mexicano-1`), 24/sep/2026; ADR-260924-GEN2-DONDE-CAMBIO-EL-MEXICANO-1-96ee-01. Mesa fusiona.
