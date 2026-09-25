# ENCARGO · ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1 · Confianza, capital social, religiosidad y valores: los reports más citados y menos medidos, con LAPOP, Latinobarómetro, WVS, PEW, ENBIARE y ENCIG en corpus

> ENTORNO: **CAJA**. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `40058c09` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie, con esas palabras.
**Forma común de toda unidad de medición (la misma que SALUD-Y-BIENESTAR, #1124):** (P1) lista cerrada de conductas por **texto de pregunta** (A.15) con unidad, universo y segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó), tomada de las afirmaciones del mapa para el dominio; los payloads se verifican por id en `data/manifiesto.yaml` y en `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` (131 programas adquiridos, 19 con ola reservada): lo que falte, el mismo acto lo adquiere con `/adquiere` (cláusula §1). (P2) COMMIT-1 por instrumento antes de abrir: spec humana + `spec.yaml` + medidor; ola más reciente **reservada** (E.6), históricas abiertas. (P3) pisos por segmento con IC de diseño; ≥ 3 olas → IC calibrado de persistencia (método #1009/#1041) como parámetro reutilizable. (P4) nota CONFIRMA / MATIZA / ROMPE contra cada report del dominio (Bloque C), módulo de auditoría de rigor extremo (§3: no confundir estructura con cultura; evidencia (a)/(b)/(c) etiquetada; firewall genético), FP de adopción por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR). CONTADOR: sella CALC (`cuenta_gen2: SI`, `adopta: NO`); mueve «N conductas con piso GEN2 por dominio» (primera línea de la nota); no evalúa prospectivamente. «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · nota CONFIRMA/MATIZA/ROMPE por report · FP por instrumento · `check.py --baseline` VERDE. PAROS (D-19 estricta): a) abrir la ola reservada · b) reescribir sellos · c) adoptar aquí; teclear · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE. COMPUERTAS: «COMMIT-1 antes de abrir» protege **abrir dato**; «unidad y universo por texto» protege **congelar**; «adopción solo por FP» protege **adoptar**.

## 1 · OBJETIVO (específico)
Dominios CONFIANZA, CAPITAL_SOCIAL, RELIGIOSIDAD, AUTORIDAD y VALORES del mapa. Conductas candidatas por texto: confianza interpersonal y en instituciones (LAPOP, Latinobarómetro, WVS, ENCIG: citar `CALC-ENCIG-*` de confianza ya sellados y `CALC-ENBIARE-*` de #1124), participación en organizaciones y ayuda mutua, asistencia religiosa y pertenencia (PEW *Religion in Latin America*, WVS, Latinobarómetro), actitudes hacia autoridad y orden, tolerancia. **Regla de comparación entre instrumentos**: escalas distintas no se comparan sin función de enlace (§4 v2.16); cada instrumento se reporta en su escala con dictamen de equivalencia textual por ola (como FIRMAS-15 T para LAPOP: sin serie hasta dictamen). Marcos importados (WVS, Hofstede) con crítica, no como hecho. Reports: *Confianza y desconfianza*, *Capital social*, *Religiosidad*, *Autoridad y jerarquía*, *Emociones morales* (solo lo medible).

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-4, regla 6, E.6, FIRMAS-15 T (dictámenes de política: LAPOP sin serie hasta equivalencia; ENCUP descriptivo en su escala), A3 (ENBIARE piso de una ola).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` manifiesto por prefijo: `pew_` 9, `lapop_` 1; Latinobarómetro y WVS bajo otros ids o pendientes de solicitud (D1 de FIRMAS-16: WVS ola 7 la solicita mesa; si no ha llegado, NO-OBTENIDO con receta y se sigue con lo demás). CALC que se citan: ENCIG confianza, ENBIARE (#1124), ENCUP (#1084/#1098). `[SUPUESTO]` que LAPOP 2004–2023 y Latinobarómetro traen pesos y diseño; si no, descriptivo sin IC, dicho.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'LAPOP\|LATINOBAR\|WVS\|PEW'` → reporta. `git ls-remote --heads origin | grep -i confianza` → 0.

## 5 · PIEZAS
P1 lista cerrada y dictamen de equivalencia por instrumento → P2 COMMIT-1 por instrumento → P3 pisos (sin series entre instrumentos) → P4 nota, auditoría, FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/CONFIANZA-*`, `data/corrida0/CALC-LAPOP-*`, `CALC-LATINOBAROMETRO-*`, `CALC-WVS-*`, `CALC-PEW-*`, `tools/dominios/confianza/`, `forense/analisis/confianza-capital-social/`, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: CALC previos (se citan), catálogo. En CAJA: CONSUMO, FAMILIA (PEW se comparte en lectura: FAMILIA toma migración, este acto religiosidad; se declara), CLASE-AMAI-2.

## 10 · LO QUE NO HACE · SUCESORES
No evalúa prospectivamente, no adopta, no construye series entre instrumentos. Sucesores: FIRMAS-18; catálogo v1.2.
