# ENCARGO · ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1 · Los dominios con más reports y cero cifras: salud, cuerpo y sustancias, salud mental, bienestar subjetivo, confianza y capital social — pisos por segmento desde ENSANUT, ENCODAT y ENBIARE, con lo que U5 ya bajó y lo que falte adquirido por el mismo acto

> ENTORNO: **CAJA** — microdato ENSANUT (2018, 2020 continua, 2021, 2022, 2023 salvo la ola más reciente reservada), ENCODAT 2016–17, ENBIARE 2021; `/adquiere` para lo que falte. Hook imprime ENTORNO-DERIVADO; si dice NUBE, PARA.

CABECERA · SHA de redacción `474a126e` (re-deriva al abrir) · una sola sesión, rama propia `acto/gen2-salud-y-bienestar-pisos-1` (o la que fije la plataforma; se declara) · MODELO: Opus · MODO: **AUTÓNOMO** · ids con raíz de acto (D-24) · D-21 aplica · «Si te encuentras escribiendo fuera de la lista de §9, PARA.» · cierre por /acto: `## NO-CORRIDO / RESERVAS` («Ninguno.» obligatorio si aplica) y `## CONSUMIDO` al pie.
CONTADOR: sella CALC de pisos por instrumento (`cuenta_gen2: SI`, `adopta: NO`); mueve «N conductas con piso GEN2 por dominio» (que la nota imprime); no evalúa prospectivamente (nada de `celdas_validadas`); las adopciones van a FP con ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR.

## 1 · OBJETIVO
Cuatro reports del corpus (*Salud, cuerpo y sustancias*, *Salud mental*, *Capital social*, *Confianza y desconfianza*; y *Religiosidad* si ENBIARE la pregunta) no tienen una sola cifra GEN2. (P1) Del mapa (`canon/mapa-dominios-v1_0.tsv`), las afirmaciones de esos dominios con dictamen MEDIBLE (en corpus o con adquisición ENSANUT/ENCODAT/ENBIARE): lista cerrada de conductas reportables por texto de pregunta (A.15), unidad (persona por grupo de edad; ENSANUT tiene módulos por edad), universo, segmentación (sexo, edad, escolaridad, localidad, entidad si el diseño lo permite; región U5 como referencia). (P2) Si una ola necesaria no está en manifiesto al abrir: `/adquiere` la trae (cláusula §1; U5 ya bajó 705 payloads de ENSANUT y 16 de ENCODAT en rama: **fusiona U5 o toma sus payloads por sha desde su rama, citándolo**). (P3) COMMIT-1 por instrumento (spec humana + `spec.yaml` + medidor) antes de abrir; pisos por segmento con IC de diseño; donde haya ≥ 3 olas (ENSANUT), **IC calibrado de persistencia** (método #1009/#1041) como parámetro reutilizable. (P4) Nota CONFIRMA / MATIZA / ROMPE contra cada report (formato Bloque C), con módulo de auditoría de rigor extremo (§3: no confundir precariedad con cultura; oferta antes que preferencia donde aplique: acceso a servicios vs. preferencia; firewall genético en sustancias: canal individual, nunca segmentación); FP de adopción por instrumento.
«Hecho»: ≥ 3 CALC sellados (uno por instrumento) con `verify` REPRODUCE y asiento · tabla conducta × segmento × ola con RESULT por id · N conductas con piso por dominio impreso en la primera línea de la nota · nota CONFIRMA/MATIZA/ROMPE por report · FP de adopción por instrumento · `check.py --baseline` VERDE.

## 2 · FIRMAS DE MESA — dadas, verbatim
**F-ASTRA-5-2** («ENSANUT + ENCODAT y ENBIARE primero»), **F-ASTRA-5-4** («adopción por instrumento al cierre de cada unidad, con FP y las opciones ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR»), **regla 6** (sin retadores, pilotos ni duelos), **E.6** (ola más reciente reservada: para ENSANUT, la última publicada; para ENCODAT y ENBIARE, si solo hay una ola en corpus se abre — no hay historia que reservar — y se declara).

## 3 · LO QUE DIRECCIÓN SABE
`[EJECUTADO]` mapa: ENSANUT 7 y ENCODAT 7 afirmaciones con instrumento nombrado; salud mental y capital social se citan por dominio (P1 los cuenta). U5 en rama: 705 ENSANUT (todas las olas y módulos), 16 ENCODAT, 2 ENBIARE en main. `[LEÍDO]` reports en `corpus/reports/` (títulos; el ejecutor lee los cuatro completos). `[SUPUESTO]` que ENSANUT expone factores de expansión y estratos por módulo; que ENBIARE 2021 tiene UPM/estrato públicos (si no: descriptivo sin IC, dicho).

## 4 · YA HECHO / YA DECIDIDO
`ls data/corrida0 | grep -ic 'ENSANUT\|ENCODAT\|ENBIARE'` → 1 (un CALC ENSANUT previo: cítalo, no lo repitas). `git ls-remote --heads origin | grep -i salud` → 0.

## 5 · PIEZAS
P1 lista cerrada por texto → P2 payloads (U5 o `/adquiere`) → P3 COMMIT-1 y medición por instrumento (ENSANUT primero: serie) → P4 nota, auditoría, FP.

## 6 · LATITUD — CLÁUSULA DE AUTONOMÍA v1.0 (`3fbc487684b77b7f`, verbatim en el ADR)
1. Discrepancias encargo↔repo las resuelve el ejecutor y las declara. 2. Firma con letra en choque e intención clara: INTERPRETACIÓN-DECLARADA, se sigue. 3. Lo redactable se redacta, rotulado PROPUESTO-POR-EJECUTOR, con fuente; mesa adopta al fusionar. 4. Bifurcación con opción recomendada: se ejecuta la recomendada. 5. PARO solo por D-19 estricta (dato reservado · sello · contador a mano/adoptar sin firma de contenido · procedimiento congelado · entorno). 6. Nunca: cifra tecleada, sello reescrito, reserva abierta, fuera de §9 sin declarar; merge de mesa cuando se sella o se escribe el motor. 7. El «Hecho» no se rebaja; lo no alcanzado va a NO-CORRIDO. Pregunta a mesa prevista: **ninguna**.

## 7 · PAROS — lista cerrada (D-19 estricta)
a) abrir la ola más reciente de ENSANUT (reservada) o cualquier otra reservada · b) reescribir un sello · c) adoptar aquí; teclear una cifra · d) cambiar la lista cerrada después de COMMIT-1 · e) NUBE.

## 8 · COMPUERTAS
«COMMIT-1 antes de abrir cada ola» protege: **abrir dato**. «Unidad y universo por texto de pregunta antes de medir» protege: **congelar**. «Adopción solo por FP» protege: **adoptar**.

## 9 · PERÍMETRO Y CONCURRENCIA
Propio: `forense/prereg-caja/SALUD-*`, `data/corrida0/CALC-ENSANUT-*`, `CALC-ENCODAT-*`, `CALC-ENBIARE-*`, `tools/dominios/salud/`, `forense/analisis/salud-bienestar/`, manifiesto solo vía `/adquiere` si falta algo, `replay-evidencia.tsv`, TSV de gobierno, nota, L0, cascada. Ajeno: catálogo de Astra (lo consume después), marcador, celdas-D, `milpa/`. En CAJA: U5 y CORPUS-COMPLETO escriben manifiesto (rebasar si choca); PISOS-GEN2-2 (otras olas).

## 10 · LO QUE NO HACE · SUCESORES
No evalúa prospectivamente (eso será una familia 2027 de U4 si mesa la firma), no adopta. Sucesores: FIRMAS-16 (adopciones); catálogo v1.1 (U1) consume; `-2` para conductas NO-CONSTRUIBLES con la pregunta que faltó.

## NO-CORRIDO / RESERVAS

- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01** · qué: registro en la vista (corridas/resultados.tsv) de los 3 CALC (pieza: «Hecho»: ≥ 3 CALC sellados … con `verify` REPRODUCE y asiento) · por qué: DIFERIDO-A:GEN2-TUBERIA -- derivados protegidos no viajan en PR (firma 21/sep); el asiento en replay-evidencia.tsv publica la fila cuando el job de main corra registro --lote · impacto: los 3 CALC quedan sellados en disco, no registrados, hasta el job · sucesor: mesa / job de push a main (registro --lote desde el diff de replay-evidencia.tsv)
- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-02** · qué: ENSANUT 2018 y 2020 fuera de la serie (pieza: microdato ENSANUT (2018, 2020 continua, 2021, 2022, 2023 …)) · por qué: DIFERIDO-A:GEN2-SALUD-Y-BIENESTAR-PISOS-2 -- 2018 cambia esquema, llaves y ventanas (último mes, alcohol sin 5+/4+, sin utilizadores); 2020 es el cuestionario COVID · impacto: la serie empieza en 2021; τ² sale de 3 Δ, no de 5 · sucesor: GEN2-SALUD-Y-BIENESTAR-PISOS-2
- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-03** · qué: módulos ENSANUT fuera de la lista: etiquetado, vacunación, HbA1c, antropometría/obesidad regional, actividad física, anticoncepción, motivos de atención (pieza: (P1) … las afirmaciones de esos dominios con dictamen MEDIBLE) · por qué: DIFERIDO-A:GEN2-SALUD-Y-BIENESTAR-PISOS-2 -- archivos distintos (menores, sangre, antropometría, actividad física, etiquetado) no cableados en este CALC · impacto: 11 afirmaciones del mapa sin cifra GEN2 (APUEST-024/025/037, CONOC-010/018, SALUD-014/016/024/025/031/032/037) · sucesor: GEN2-SALUD-Y-BIENESTAR-PISOS-2
- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-04** · qué: eje entidad / región (pieza: segmentación (… entidad si el diseño lo permite; región U5 como referencia)) · por qué: DIFERIDO-A:GEN2-SALUD-Y-BIENESTAR-PISOS-2 -- 32 celdas por ola con n de 1.9–13 mil adultos no sostienen IC; ENCODAT 2016 no trae región · impacto: ninguna afirmación regional medida (SALUD-016, SALUD-017, TRUST-030) · sucesor: GEN2-SALUD-Y-BIENESTAR-PISOS-2
- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-05** · qué: NO-CONSTRUIBLES por texto: intento de suicidio (ENSANUT 2021–2023), facilidad para cubrir gastos (ENBIARE 2021), malestar psicológico (ENCODAT 2016) (pieza: `-2` para conductas NO-CONSTRUIBLES con la pregunta que faltó) · por qué: DIFERIDO-A:GEN2-SALUD-Y-BIENESTAR-PISOS-2 -- la pregunta no existe en la ola abierta (A.15: textos y secciones en lista-cerrada-P1 §3) · impacto: JUV-009 (intento), CLASE-040, JUV-010 sin cifra · sucesor: GEN2-SALUD-Y-BIENESTAR-PISOS-2
- **NC-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-06** · qué: adopción de los 3 instrumentos (pieza: las adopciones van a FP con ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR) · por qué: DECISIÓN-DE-MESA-PENDIENTE -- FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01..03 · impacto: ningún consumidor usa estos pisos hasta la firma · sucesor: FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01

## CONSUMIDO

PR #1124 (rama `acto/gen2-salud-y-bienestar-pisos-1`), 24/sep/2026.
