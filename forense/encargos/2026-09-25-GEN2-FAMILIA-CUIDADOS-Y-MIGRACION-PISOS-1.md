# ENCARGO · ACTO GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1 · Familia, pareja, vejez y cuidado, y migración: cuatro reports sin cifra GEN2, con ENADID, ENASIC, ENUT, EMIF y PEW ya en corpus

> ENTORNO: **CAJA**. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `40058c09` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie, con esas palabras.
**Forma común de toda unidad de medición (la misma que SALUD-Y-BIENESTAR, #1124):** (P1) lista cerrada de conductas por **texto de pregunta** (A.15) con unidad, universo y segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó), tomada de las afirmaciones del mapa para el dominio; los payloads se verifican por id en `data/manifiesto.yaml` y en `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` (131 programas adquiridos, 19 con ola reservada): lo que falte, el mismo acto lo adquiere con `/adquiere` (cláusula §1). (P2) COMMIT-1 por instrumento antes de abrir: spec humana + `spec.yaml` + medidor; ola más reciente **reservada** (E.6), históricas abiertas. (P3) pisos por segmento con IC de diseño; ≥ 3 olas → IC calibrado de persistencia (método #1009/#1041) como parámetro reutilizable. (P4) nota CONFIRMA / MATIZA / ROMPE contra cada report del dominio (Bloque C), módulo de auditoría de rigor extremo (§3: no confundir estructura con cultura; evidencia (a)/(b)/(c) etiquetada; firewall genético), FP de adopción por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR). CONTADOR: sella CALC (`cuenta_gen2: SI`, `adopta: NO`); mueve «N conductas con piso GEN2 por dominio» (primera línea de la nota); no evalúa prospectivamente. «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · nota CONFIRMA/MATIZA/ROMPE por report · FP por instrumento · `check.py --baseline` VERDE. PAROS (D-19 estricta): a) abrir la ola reservada · b) reescribir sellos · c) adoptar aquí; teclear · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE. COMPUERTAS: «COMMIT-1 antes de abrir» protege **abrir dato**; «unidad y universo por texto» protege **congelar**; «adopción solo por FP» protege **adoptar**.

## 1 · OBJETIVO (específico)
Dominios FAMILIA_CUIDADOS, VEJEZ, PAREJA y MIGRACION del mapa. Conductas candidatas por texto: corresidencia y tipo de hogar, unión y primera unión por cohorte (citando `CALC-EDER2017-*` ya sellados), fecundidad deseada vs observada, división de cuidados (ENUT: citar `CALC-ENUT-*`; ENASIC 2022: quién cuida a quién y con qué ayuda), dependencia y arreglos de vejez, intención y experiencia migratoria (ENADID módulo migración; EMIF flujos; PEW percepciones). Unidad persona / hogar / flujo declaradas. Reports: *Familia mexicana*, *Pareja y apps*, *Vejez y cuidado*, *Migración*. Segmentación adicional: condición de pareja y tamaño de hogar.

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-4, regla 6, E.6, §3 v2.16 (evidencia (b) diáspora ≠ México: PEW se etiqueta (b) cuando encuesta a mexicanos en EE. UU.).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` manifiesto por prefijo: `enasic_` 1, `pew_` 9, `mmsi_` 2; ENADID, ENUT, EMIF bajo otros ids (verificar en tabla-final de CORPUS-COMPLETO por `programa_id`). CALC que se citan: `CALC-ENADID-*` (5), `CALC-ENUT-*` (7), `CALC-EDER2017-*` (2). `[SUPUESTO]` que EMIF (COLEF) se obtuvo; si no, `/adquiere` o NO-OBTENIDO con receta.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'ENADID\|ENASIC\|EMIF'` → reporta (ENADID 5 previos: citar, no repetir). `git ls-remote --heads origin | grep -i familia` → 0.

## 5 · PIEZAS
P1 lista cerrada → P2 COMMIT-1 por instrumento (ENADID primero: serie) → P3 pisos + IC calibrado → P4 nota, auditoría, FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/FAMILIA-*`, `data/corrida0/CALC-ENADID*-FAMILIA-*`, `CALC-ENASIC-*`, `CALC-EMIF-*`, `CALC-PEW-*`, `tools/dominios/familia/`, `forense/analisis/familia-migracion/`, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: CALC previos de ENADID/ENUT/EDER (se citan), catálogo. En CAJA: CONSUMO, CONFIANZA, CLASE-AMAI-2 (olas distintas).

## 10 · LO QUE NO HACE · SUCESORES
No evalúa prospectivamente, no adopta. Sucesores: FIRMAS-18; catálogo v1.2.

## NO-CORRIDO / RESERVAS

| id | qué | por qué | impacto | sucesor |
|---|---|---|---|---|
| NC-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01 | «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento — registro en la vista (corridas/resultados.tsv) de los 3 CALC | DIFERIDO-A:GEN2-TUBERIA -- derivados protegidos no viajan en PR; el asiento en replay-evidencia.tsv publica la fila cuando el job de main corra registro --lote | los 3 CALC quedan sellados en disco, no registrados, hasta el job | mesa / job de push a main (registro --lote) |
| NC-…-2a0e-02 | [SUPUESTO] que EMIF (COLEF) se obtuvo; si no, `/adquiere` o NO-OBTENIDO con receta | DIFERIDO-A:GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 -- NO OBTENIDO POR ESTE AGENTE EN 1 INTENTO (colef.mx/emif/ sin enlaces estáticos a bases; bases.php 404; CKAN sin JSON); receta en lista-cerrada-familia-migracion-P1 §4 | sin piso de flujos EMIF | GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 |
| NC-…-2a0e-03 | fecundidad deseada vs observada | DIFERIDO-A:GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 -- el ideal de hijos cambia de número y nemónico por ola en el módulo de la mujer | sin piso de fecundidad deseada | GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 |
| NC-…-2a0e-04 | ENADID primero: serie — 1992 y 1997 | DIFERIDO-A:GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 -- otro esquema, sin estrato/UPM de diseño estándar ni clase de hogar derivada | la serie empieza en 2009 (τ² de 2 Δ) | GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 |
| NC-…-2a0e-05 | segmentación: formalidad, región, NSE; TLOC en ENASIC; escolaridad/urbanidad en Pew | DIFERIDO-A:GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 -- formalidad fuera de las tablas usadas; NSE no construido para estas encuestas; ENASIC no publica localidad; Pew cambia variables por ola | ninguna afirmación regional ni por formalidad medida | GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 |
| NC-…-2a0e-06 | FP de adopción por instrumento | DECISIÓN-DE-MESA-PENDIENTE -- FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01..03 | ningún consumidor usa estos pisos hasta la firma | FP-260925-GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-1-2a0e-01 |
| NC-…-2a0e-07 | ola más reciente reservada (E.6): ENADID 2023 (conductas de esta lista) y Pew GAS Spring 2025 | DIFERIDO-A:GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 -- reservadas por diseño; este acto no evalúa prospectivamente | reservas sin abrir; celdas_validadas no se mueve | GEN2-FAMILIA-CUIDADOS-Y-MIGRACION-PISOS-2 |
