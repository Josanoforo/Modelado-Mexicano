# ENCARGO · ACTO GEN2-COLA-LOTE-1 · Lote D-11 con cuatro programas chicos de la cola v1.1 que ningún dominio grande cubre: EMAT 2022–23 (pareja), Censo 2020 muestra (familia y cuidados), ENPECYT 2017 (conocimiento) y EDR (salud mental/familia): pisos por segmento y verificación de texto, uno por pieza

> ENTORNO: **CAJA**. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `aa36232a` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
**Forma común de toda unidad de medición (SALUD #1124; CONSUMO #1155):** (P1) lista cerrada de conductas por **texto de pregunta** (A.15) con unidad, universo y segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó); payloads verificados por `programa_id` en `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` y en el manifiesto; lo que falte lo adquiere el mismo acto (`/adquiere`). La verificación de texto se asienta en `forense/analisis/dominios/verificaciones-texto-v1_1.tsv` (o `no-construibles-v1_1.tsv`) y el derivador del mapa se re-corre: las afirmaciones del dominio suben a MEDIBLE-EN-CORPUS por comando (NC `…MAPA-DOMINIOS-V1-1-1-3cf7-01`). (P2) COMMIT-1 por instrumento antes de abrir; ola más reciente **reservada** (E.6), históricas abiertas. (P3) pisos por segmento con IC de diseño; ≥ 3 olas → IC calibrado de persistencia (#1009/#1041) como parámetro reutilizable. (P4) nota CONFIRMA / MATIZA / ROMPE contra cada report (Bloque C), módulo de auditoría de rigor extremo, FP de adopción por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR). CONTADOR: sella CALC (`cuenta_gen2: SI`, `adopta: NO`); «N conductas con piso GEN2 por dominio» en la primera línea; no evalúa prospectivamente. «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · filas de verificación de texto y mapa re-derivado · nota CONFIRMA/MATIZA/ROMPE · FP por instrumento · `check.py --baseline` VERDE. PAROS (D-19 estricta): a) abrir ola reservada · b) reescribir sellos · c) adoptar aquí; teclear · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE. COMPUERTAS: «COMMIT-1 antes de abrir» protege **abrir dato**; «unidad y universo por texto» protege **congelar**; «adopción solo por FP» protege **adoptar**.

## 1 · OBJETIVO (específico, cuatro piezas; una que PARA no tumba las otras)
- **P-EMAT** (PAREJA, 5 afirmaciones, report *Elegir, cortejar y amar*): Encuesta de Matrimonio? — **el ejecutor verifica qué es EMAT en `tabla-final` y en el cuestionario antes de nada**; si es lo que el mapa supone (matrimonios y uniones), conductas por texto: edad a la unión, unión libre vs matrimonio, disolución.
- **P-CCPV** (FAMILIA_CUIDADOS, 4, Censo 2020 muestra ampliada): tipo de hogar, corresidencia intergeneracional, hogares con 60+ y con menores, jefatura; unidad hogar y persona; segmentación por entidad y localidad (el censo lo permite).
- **P-ENPECYT** (CONOCIMIENTO, 3, ENPECYT 2017): actitudes y conocimiento científico, fuentes de información, confianza en ciencia; una ola → descriptivo.
- **P-EDR** (SALUD_MENTAL/FAMILIA, 4): el catálogo de corpus lista EDR 1990/1995/2000 (INEGI) y la cola dice 2022;2024: **discrepancia que el ejecutor resuelve primero** (¿qué programa es EDR en el mapa: Estadísticas de Defunciones Registradas? ¿la cola casó mal la ola?); si es registro administrativo de defunciones, se trata como serie (unidad defunción, nunca persona-encuesta) y se declara.
Cada pieza: lista cerrada por texto, COMMIT-1, pisos, verificación de texto asentada, FP de adopción por instrumento.

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-4, regla 6, E.6, §4 (unidades no se promedian: defunciones ≠ personas encuestadas).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` cola v1.1: EMAT 2022;2023 (5) · CCPV 2020 (4) · ENPECYT 2017 (3) · EDR 2022;2024 (4); catálogo de corpus: EDR solo 1990/1995/2000. `[SUPUESTO]` que los cuatro tienen payload en corpus por `programa_id` (tabla-final): si alguno no, `/adquiere` o NO-OBTENIDO con receta.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'EMAT\|CCPV\|CENSO\|ENPECYT\|EDR'` → reporta (EDER ≠ EDR: no confundir). `git ls-remote --heads origin | grep -i 'cola-lote'` → 0.

## 5 · PIEZAS
Orden: CCPV (más afirmaciones sostenidas por report) → EMAT → ENPECYT → EDR (la que más verificación previa exige).

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/{EMAT,CCPV,ENPECYT,EDR}-*`, `data/corrida0/CALC-{EMAT,CCPV,ENPECYT,EDR}-*`, `tools/dominios/cola-lote-1/`, `forense/analisis/cola-lote-1/`, verificaciones de texto, mapa por derivador, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: CALC previos (ENADID, EDER: se citan), catálogo. En CAJA: ENSU, DINERO-SERIES.

## 10 · LO QUE NO HACE · SUCESORES
No adopta. Sucesores: FIRMAS-20; COLA-LOTE-2 con las siguientes filas de la cola v1.1.
