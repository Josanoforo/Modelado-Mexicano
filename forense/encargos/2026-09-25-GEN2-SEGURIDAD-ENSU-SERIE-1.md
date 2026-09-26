# ENCARGO · ACTO GEN2-SEGURIDAD-ENSU-SERIE-1 · La serie más larga y frecuente del corpus sin medir: ENSU (percepción de inseguridad urbana, trimestral 2013–2025, por ciudad), pisos por segmento y ciudad, IC calibrado de persistencia trimestral, y el dictamen ESTABLE / CAMBIO-SOSTENIDO por ciudad que el report de violencia crónica pide

> ENTORNO: **CAJA** — 164 payloads de ENSU en manifiesto; último trimestre publicado reservado. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `aa36232a` (re-deriva al abrir) · una sola sesión, rama propia (la que fije la plataforma; se declara) · MODELO: Opus (mide; no bajar) · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` con esas palabras.
**Forma común de toda unidad de medición (SALUD #1124; CONSUMO #1155):** (P1) lista cerrada de conductas por **texto de pregunta** (A.15) con unidad, universo y segmentación (sexo, edad, escolaridad, localidad, formalidad, región, NSE donde A4 lo autorizó); payloads verificados por `programa_id` en `forense/analisis/corpus-completo/tabla-final-v1_0.tsv` y en el manifiesto; lo que falte lo adquiere el mismo acto (`/adquiere`). La verificación de texto se asienta en `forense/analisis/dominios/verificaciones-texto-v1_1.tsv` (o `no-construibles-v1_1.tsv`) y el derivador del mapa se re-corre: las afirmaciones del dominio suben a MEDIBLE-EN-CORPUS por comando (NC `…MAPA-DOMINIOS-V1-1-1-3cf7-01`). (P2) COMMIT-1 por instrumento antes de abrir; ola más reciente **reservada** (E.6), históricas abiertas. (P3) pisos por segmento con IC de diseño; ≥ 3 olas → IC calibrado de persistencia (#1009/#1041) como parámetro reutilizable. (P4) nota CONFIRMA / MATIZA / ROMPE contra cada report (Bloque C), módulo de auditoría de rigor extremo, FP de adopción por instrumento (ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR). CONTADOR: sella CALC (`cuenta_gen2: SI`, `adopta: NO`); «N conductas con piso GEN2 por dominio» en la primera línea; no evalúa prospectivamente. «Hecho»: ≥ 1 CALC sellado por instrumento con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · filas de verificación de texto y mapa re-derivado · nota CONFIRMA/MATIZA/ROMPE · FP por instrumento · `check.py --baseline` VERDE. PAROS (D-19 estricta): a) abrir ola reservada · b) reescribir sellos · c) adoptar aquí; teclear · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE. COMPUERTAS: «COMMIT-1 antes de abrir» protege **abrir dato**; «unidad y universo por texto» protege **congelar**; «adopción solo por FP» protege **adoptar**.

## 1 · OBJETIVO (específico)
Dominio VIOLENCIA (y CONFIANZA, VEJEZ por segmento). ENSU es trimestral y por ciudad (≈ 90 ciudades), la única serie del programa con esa frecuencia. Conductas candidatas por texto: percepción de inseguridad en la ciudad, en espacios concretos (cajero, transporte, calle), cambio de hábitos por miedo (dejar de salir de noche, de usar joyas, de dejar salir a menores), expectativa a 12 meses, confianza en policías, testigos de conductas delictivas. Unidad persona 18+ urbana; segmentación sexo, edad, ciudad (entidad y región). Además de los pisos: **serie 2013–2025 por conducta y ciudad** con el vocabulario cerrado de DONDE-CAMBIO (#1125: ESTABLE · CAMBIO-SOSTENIDO · SALTO-DE-INSTRUMENTO · SIN-SERIE, umbrales antes de abrir) e IC calibrado de persistencia **trimestral** como parámetro nuevo. Reports: *Efecto ambiental de la violencia crónica*, *Confianza y desconfianza*.

## 2 · FIRMAS DE MESA — dadas
F-ASTRA-5-3 (reserva solo del último periodo publicado), F-ASTRA-5-4, regla 6, vocabulario de DONDE-CAMBIO (aprobado en bloque 23/sep y ejecutado en #1125).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` manifiesto: 164 menciones `ensu`; cola v1.1: VIOLENCIA/ENSU 2024;2025, 4 afirmaciones. `[SUPUESTO]` que ENSU trae factor y diseño por trimestre y ciudad (sí, por diseño INEGI); que el cuestionario cambió en 2016 y 2020 (modo telefónico en pandemia): la spec dictamina SALTO-DE-INSTRUMENTO donde corresponda.

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic ENSU` → 0. `git ls-remote --heads origin | grep -i ensu` → 0.

## 5 · PIEZAS
P1 lista cerrada y vocabulario → P2 COMMIT-1 (un CALC de pisos, un CALC de serie) → P3 medición y IC trimestral → P4 nota, dictamen por ciudad, FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja. Pregunta a mesa prevista: **ninguna**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/ENSU-*`, `data/corrida0/CALC-ENSU-*`, `tools/dominios/ensu/`, `forense/analisis/seguridad-ensu/`, verificaciones de texto, mapa por derivador, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: ENVIPE (se cita), catálogo. En CAJA: COLA-LOTE-1 (otros programas).

## 10 · LO QUE NO HACE · SUCESORES
No compara ENSU con ENVIPE sin enlace (escalas distintas); no evalúa prospectivamente (una familia 2027 de ENSU trimestral es candidata natural: se propone en la nota). Sucesores: FIRMAS-20, catálogo v1.2, U4 familias.
