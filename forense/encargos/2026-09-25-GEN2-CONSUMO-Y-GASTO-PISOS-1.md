# ENCARGO · ACTO GEN2-CONSUMO-Y-GASTO-PISOS-1 · El report que da nombre al proyecto (*Psicología del Consumidor Mexicano*) sin una cifra GEN2: pisos de consumo y gasto por segmento desde ENGASTO (28 payloads) y ENIGH (todas las olas abiertas), con la columna de oferta al lado y CONFIRMA/MATIZA/ROMPE contra el report

> ENTORNO: **CAJA**. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `40058c09` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie, con esas palabras.
**Forma común de toda unidad de medición (la misma que SALUD-Y-BIENESTAR, #1124):** (P1) lista cerrada de conductas por **texto de pregunta** (A.15) con unidad, universo y segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó), tomada de las afirmaciones del mapa para el dominio; los payloads se verifican por id en `data/manifiesto.yaml` y en `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` (131 programas adquiridos, 19 con ola reservada): lo que falte, el mismo acto lo adquiere con `/adquiere` (cláusula §1). (P2) COMMIT-1 por instrumento antes de abrir: spec humana + `spec.yaml` + medidor; ola más reciente **reservada** (E.6), históricas abiertas. (P3) pisos por segmento con IC de diseño; ≥ 3 olas → IC calibrado de persistencia (método #1009/#1041) como parámetro reutilizable. (P4) nota CONFIRMA / MATIZA / ROMPE contra cada report del dominio (Bloque C), módulo de auditoría de rigor extremo (§3: no confundir estructura con cultura; evidencia (a)/(b)/(c) etiquetada; firewall genético), FP de adopción por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR). CONTADOR: sella CALC (`cuenta_gen2: SI`, `adopta: NO`); mueve «N conductas con piso GEN2 por dominio» (primera línea de la nota); no evalúa prospectivamente. «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · nota CONFIRMA/MATIZA/ROMPE por report · FP por instrumento · `check.py --baseline` VERDE. PAROS (D-19 estricta): a) abrir la ola reservada · b) reescribir sellos · c) adoptar aquí; teclear · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE. COMPUERTAS: «COMMIT-1 antes de abrir» protege **abrir dato**; «unidad y universo por texto» protege **congelar**; «adopción solo por FP» protege **adoptar**.

## 1 · OBJETIVO (específico)
Dominios CONSUMO y DINERO del mapa (INEGI 22 afirmaciones con adquisición, ahora en corpus; ENGASTO 28 payloads; ENIGH 2016–2022 abiertas, 2024 reservada salvo lo abierto por el duelo). Conductas candidatas (Astra/ejecutor las fija por texto): estructura del gasto por rubro y decil, gasto en alimentos fuera del hogar, endeudamiento para consumo, compras a crédito/abonos, canal (tianguis, mercado, súper, en línea), gasto en celular e internet, remesas como ingreso de consumo (citando `CALC-ENIGH*-REMESAS-*` ya sellados, no re-medir). Unidad hogar y persona declaradas, nunca promediadas. Oferta antes que preferencia: cada marginal de canal o crédito con su columna de exclusión por oferta (RESULT de #1042 donde aplique; NO-CONSTRUIBLE donde no). Reports: *Psicología del Consumidor Mexicano*, *Finanzas conductuales*, *Clasemediero*.

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-4 (adopción por instrumento con FP), regla 6, E.6, §3 v2.16 (oferta antes que preferencia), C4 de FIRMAS-16 no aplica (no es ENOE).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` manifiesto: `engasto_` 28 payloads; ENIGH bajo ids no uniformes (verificar en tabla-final de CORPUS-COMPLETO). CALC sellados que se citan: `CALC-ENIGH20*-REMESAS-*`, `CALC-ENIGH*-PERFIL-ESTRUCTURAL-*`, `CALC-DIN-*`. Catálogo v1.1 (#1138) tiene la cobertura por dominio: CONSUMO sin medición. `[SUPUESTO]` que ENGASTO trae factores y diseño por trimestre: la spec lo verifica y declara la unidad temporal.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'ENGASTO\|CONSUMO'` → reporta (esperado 0 salvo remesas/perfil). `git ls-remote --heads origin | grep -i consumo` → 0.

## 5 · PIEZAS
P1 lista cerrada → P2 COMMIT-1 por instrumento (ENGASTO; ENIGH) → P3 pisos + IC calibrado ENIGH (≥ 3 olas) → P4 nota, auditoría, FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/CONSUMO-*`, `data/corrida0/CALC-ENGASTO-*`, `CALC-ENIGH*-CONSUMO-*`, `tools/dominios/consumo/`, `forense/analisis/consumo-gasto/`, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: CALC de remesas/perfil (se citan), catálogo, marcador. En CAJA: CLASE-AMAI-2 (ENIGH 2024, columnas distintas; sin conflicto), FAMILIA y CONFIANZA (otras olas).

## 10 · LO QUE NO HACE · SUCESORES
No evalúa prospectivamente, no adopta. Sucesores: FIRMAS-18 (adopción), catálogo v1.2.
