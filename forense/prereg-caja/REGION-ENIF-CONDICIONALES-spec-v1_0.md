# REGION-ENIF-CONDICIONALES · spec humana v1.0

El primer resultado que produzca este procedimiento es el que se reporta. ENIF 2024, personas elegidas de 18+ y las seis regiones oficiales `REGION=1..6`. R1/R2 fueron asentadas por mesa el 23/sep/2026: ninguna estimación estatal ENIF, punto e IC solo con denominador no ponderado ≥200, varianza estimable y requisito oficial más estricto. Las filas pequeñas conservan estado y cifras nulas. `adopta: NO`, **RETROSPECTIVA**.

Se heredan exactamente las seis tasas condicionales y los códigos de `ENIF-AHORRO-spec-v1_0.md` §3.2, §3.3 y §3.5, con sus RESULT nacionales de `CALC-ENIF-0001` para control, sin copiar cifras como fuente. Horizonte corto `P4_10∈{1,2}` y no corto `{3,4,5}`. El denominador para cada una de esas dos respuestas es, separadamente, `P3_13=7` (sin seguridad social) o `P3_13∈{1,2,3,4}` (con seguridad social), siempre con `P4_10` válido. Se miden los cuatro cruces con unidad **persona** y no se promedian denominadores distintos.

Desconfianza/mal servicio como razón principal: numerador `P5_20='03'`; denominadores separados de `P5_20∈{'01'..'10'}` con `P5_23=1` (conoce protección) y `P5_23=2` (no conoce). El código `10` «otro» queda en el denominador. Guardias previas: `P5_23` no puede tener vacío ni `b`; `P5_20` contestada no puede coincidir con ninguna cuenta declarada en `P5_4_1..9`. El código detiene la corrida si alguna falla.

Archivo `TMODULO.csv` en la CAJA autorizada; factor `FAC_PER`, estrato `EST_DIS`, UPM `UPM_DIS`, geografía `REGION`, todos leídos como texto salvo factor numérico. Estimación de dominio sobre el diseño completo por `estima_dominios`; réplicas UPM dentro de estrato, 1 000, semilla PCG64 `20260923`, compartidas por ola, con `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` pinado. IC bootstrap percentil, n efectivo Kish y R2. Los `-JSON` guardan réplicas conjuntas sin identificadores ni pesos individuales. No se altera el medidor nacional ni las fuentes U1.

## Auditoría de rigor extremo

El corte de horizonte es una convención del reactivo, no una propiedad permanente de la persona. Seguridad social y conocimiento de protección son dominios observados, no tratamientos causales. La región ENIF no identifica estado de residencia para publicación. Celdas suprimidas no son ceros, y una cobertura pequeña por región no se interpreta como preferencia cultural ni de clase.
