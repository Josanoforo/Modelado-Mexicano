# ENCARGO · ACTO GEN2-DINERO-SERIES-CNBV-BANXICO-1 · Lo primero de la cola de medición v1.1: 30 afirmaciones de dinero sostenidas por series administrativas de CNBV y Banxico (crédito, morosidad, inclusión, remesas, tasas), que no son encuesta y por eso nadie las había medido — entran como RESULT con unidad, fuente y fecha, y como columna de oferta al lado de los pisos de crédito

> ENTORNO: **NUBE** con red para portales públicos (CNBV/Banxico: series descargables; cadena TLS de CNBV puede exigir la receta de U0) — si la sesión no tiene red, **CAJA**. Hook imprime ENTORNO-DERIVADO.

CABECERA · SHA de redacción `aa36232a` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
CONTADOR: sella CALC de series administrativas (`cuenta_gen2: SI`, `adopta: NO`, `tipo: SERIE-ADMINISTRATIVA`), unidad y periodicidad declaradas; «N afirmaciones de DINERO con RESULT» en la primera línea; no evalúa prospectivamente.

## 1 · OBJETIVO
La cola de medición v1.1 abre con DINERO/CNBV (21 afirmaciones, 5 reports) y DINERO/BANXICO (9, 5 reports), ambas `SIN-OLA-CASADA` porque son **series administrativas**, no encuestas: cartera y morosidad por producto (IMOR), inclusión financiera (puntos de acceso, cuentas por 10 mil adultos), remesas mensuales, tasas y CAT, boletines SOFIPO. El programa ya las cita (`CALC-BANXICO-*`, `CALC-IMOR-*`, `RESULT-BANXICO-2024-*` adoptados en #1119) pero sin cubrir esas 30 afirmaciones. (P1) Por afirmación: qué serie exacta la sostiene (nombre de la serie en el portal, id de serie Banxico SIE / tabla CNBV, periodicidad, unidad: pesos, %, cuentas por 10 mil, personas), citada por URL y fecha de consulta; lo que no exista como serie → NO-CONSTRUIBLE con lo buscado. (P2) Adquisición como **constancia congelada** (E.6/D-22: una serie viva no se sella; se sella una descarga con fecha y sha en el CALC): `/adquiere` o descarga directa a `data/corrida0/<CALC>/insumos/` con sha, nunca a `data/raw` como microdato. (P3) CALC por fuente: RESULT por serie × periodo relevante (último dato, promedio del año, cambio interanual) con unidad y **rótulo de que no es encuesta ni persona**: nunca se promedia con un piso de ENIF (§4 v2.16). (P4) **Columna de oferta**: donde una serie mide oferta (puntos de acceso, sucursales, corresponsales por municipio), se registra como RESULT de exclusión-por-oferta citable junto a los pisos de crédito y ahorro (§3: oferta antes que preferencia); la nota dice qué pisos ganan columna. (P5) Nota CONFIRMA/MATIZA/ROMPE contra los cinco reports; verificación de texto asentada; mapa re-derivado.
«Hecho»: ≥ 2 CALC sellados (CNBV, Banxico) con `verify` REPRODUCE, asientos, insumos con sha y fecha · 30 afirmaciones con RESULT o NO-CONSTRUIBLE (0 sin dictamen) · N pisos de crédito/ahorro con columna de oferta nueva (citados por id) · mapa re-derivado · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas
Regla §3 (oferta antes que preferencia) y §4 (unidades no se promedian); FP-404 (frontera de conductas de dinero); B1 de FIRMAS-16 no aplica. Constancia congelada: E.6/D-22. Regla 6.

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` cola v1.1: CNBV 21 / BANXICO 9, `n_texto_verificado` 0 (son series, no preguntas: la «verificación de texto» aquí es la definición oficial de la serie, citada). CALC previos: `CALC-BANXICO-*`, `CALC-IMOR-*` (los cita, no los repite). Receta de acceso de U0 para CNBV (TLS). `[SUPUESTO]` que Banxico SIE expone API/CSV estable por id de serie; CNBV por portafolio de información.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'CNBV\|BANXICO\|IMOR'` → reporta (citar). `git ls-remote --heads origin | grep -i 'cnbv\|banxico'` → 0.

## 5 · PIEZAS
P1 mapeo afirmación → serie → P2 constancias → P3 CALC → P4 oferta → P5 nota y mapa.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) no aplica (no hay ola reservada en series) · b) sellar contra una serie viva sin constancia; reescribir sellos · c) promediar una serie con un piso de persona; adoptar · d) no aplica · e) —

## 8 · COMPUERTAS
«Serie sellada solo como constancia con fecha y sha» protege: **congelar** (E.6/D-22). «Unidad administrativa nunca promediada con persona» protege: **congelar** (§4).

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/DINERO-SERIES-*`, `data/corrida0/CALC-CNBV-SERIES-*`, `CALC-BANXICO-SERIES-*`, `tools/dominios/dinero-series/`, `forense/analisis/dinero-series/`, `forense/analisis/dominios/verificaciones-texto-v1_1.tsv` (append), mapa por derivador, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: pisos de ENIF (se citan), catálogo. En vuelo: SEGURIDAD-ENSU (otro dominio), COLA-LOTE-1.

## 10 · LO QUE NO HACE · SUCESORES
No mide encuestas, no adopta. Sucesores: catálogo v1.2 (columna de oferta), FIRMAS-20.
