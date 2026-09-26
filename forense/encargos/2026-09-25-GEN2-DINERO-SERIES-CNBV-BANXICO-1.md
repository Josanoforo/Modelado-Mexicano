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

## NO-CORRIDO / RESERVAS

- **qué:** «(P2) Adquisición como constancia congelada» de las series CNBV que sostienen 10 afirmaciones NO-ACCESIBLE (R16 por institución e IMORA del boletín de banca múltiple; boletín estadístico SOFIPO por entidad; BDIF corresponsales) · **por qué:** PARO-ENTORNO — el proxy de esta sesión NUBE niega por política `portafolioinfo.cnbv.gob.mx`, `www.cnbv.gob.mx`, `www.gob.mx` y `web.archive.org` (403 a CONNECT); el encargo previó «si la sesión no tiene red, CAJA» · **impacto:** 10 afirmaciones sin RESULT (APUEST-018, CRFAC-003, CRPOP-005/017/031/036/049/057/060, CLASE-042, y la parte por institución de 6 RESULT de sistema); el «Hecho» «30 con RESULT o NO-CONSTRUIBLE» no se alcanza · **sucesor:** GEN2-DINERO-SERIES-CNBV-BANXICO-2 (CAJA o NUBE con esos hosts permitidos)
- **qué:** «(P2)» de las series Banxico que sostienen 5 afirmaciones NO-ACCESIBLE (SIE financiamiento CF297 —ya en el manifiesto, payload fuera de este clon—; RIB de tarjetas y de créditos personales) · **por qué:** PARO-ENTORNO — `www.banxico.org.mx` denegado (403) y corpus no montado · **impacto:** CRFAC-004, CRFAC-011, CRFAC-013, CRPOP-050, CONS-021 sin RESULT (con las 10 de arriba, 15 NO-ACCESIBLE) · **sucesor:** GEN2-DINERO-SERIES-CNBV-BANXICO-2
- **qué:** «(P4) Columna de oferta … la nota dice qué pisos ganan columna» · **por qué:** PARO-ENTORNO — la serie de oferta (BDIF de CNBV: sucursales, corresponsales, puntos de acceso) está en host denegado y no hay constancia de oferta en el repo · **impacto:** 0 pisos de crédito/ahorro con columna de oferta nueva; «N pisos con columna de oferta» no se alcanza · **sucesor:** GEN2-DINERO-SERIES-CNBV-BANXICO-2; catálogo v1.2
- **qué:** «(P5) verificación de texto asentada; mapa re-derivado» · **por qué:** DIFERIDO-A:catálogo v1.2 — la definición oficial de cada serie se cita en la spec §2 y en `afirmacion-serie-v1_0.tsv`, pero no se añade a `verificaciones-texto-v1_1.tsv` (su compuerta A.15 exige casar con un inventario de reactivos de encuesta, y una serie no tiene reactivo); el derivador del mapa no lee series, y COLA-LOTE-1 está en vuelo sobre la cola; `redictamina_v1_1.py --verifica` → COINCIDE (mapa re-derivado sin cambio) · **impacto:** `canon/mapa-dominios-v1_1.tsv` y la cola siguen mostrando las 30 como MEDIBLE-CON-ADQUISICIÓN; el dictamen vive en la tabla propia · **sucesor:** catálogo v1.2 (que el derivador lea `forense/analisis/dinero-series/afirmacion-serie-v1_0.tsv`)
- **qué:** publicación en la vista (`data/corrida0/{corridas,resultados}.tsv`) de las filas de los 2 CALC · **por qué:** DIFERIDO-A:/deriva — `corrida0 registro --lote … --escribe` reescribía ~146 mil líneas ajenas (la vista no se regenera en main desde #1076); se revirtió y se asentó el replay por acto en `forense/replay-evidencia.tsv`, patrón de los actos recientes · **impacto:** `corrida0 status` no muestra los 56 RESULT hasta la próxima regeneración de la vista; el asiento de replay sí existe · **sucesor:** /deriva (regeneración diaria de derivados)
- **qué:** validación independiente de los dos CALC (spec: `validacion_independiente: PENDIENTE-POST-SELLO`) · **por qué:** DIFERIDO-A:GEN2-DINERO-SERIES-CNBV-BANXICO-2 — el encargo no la pide; reproducir no es validar (E.2) · **impacto:** los 56 RESULT se reproducen pero no tienen validación independiente · **sucesor:** GEN2-DINERO-SERIES-CNBV-BANXICO-2
