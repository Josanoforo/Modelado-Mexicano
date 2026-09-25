**Conductas con piso GEN2 por dominio (este acto; derivado por `python3 forense/analisis/salud-bienestar/tabla_pisos.py`): SALUD 20 · SALUD_MENTAL 7 · CONFIANZA 4 · CAPITAL_SOCIAL 2 · RELIGIOSIDAD 2 — 35 conductas, 3 CALC sellados, 0 adopciones.**

# Nota de cierre · ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1

24/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado; `data/raices.local.yaml` apunta
`descargas_mx` al espejo `mm-corpus/descargas_mx_espejo`) · Opus 5.5 · rama
`acto/gen2-salud-y-bienestar-pisos-1` · 0-bis `6d56f7ff` · base `origin/main` `8358b891`.
Encargo: `forense/encargos/2026-09-24-GEN2-SALUD-Y-BIENESTAR-PISOS-1.md`.

**Continuidad declarada.** La sesión que abrió el acto se cortó (apagón de la máquina)
después del 0-bis, con la receta común sin commitear y tres agentes de estructura en
vuelo; sólo el de ENBIARE había entregado. Una segunda sesión recuperó la rama, commiteó
lo que había en disco (`eee7eacc`), relanzó los dos agentes de estructura perdidos
(ENSANUT, ENCODAT; sólo metadatos) y siguió. **Ningún valor de microdato se leyó antes del
COMMIT-1** (`a102ade3`): las dos sesiones sólo usaron `metadataonly=True`, el FD y la
primera línea de los CSV.

## 1 · Qué se midió

| CALC | olas | conductas | RESULT | verify aislado |
|---|---|---|---|---|
| `CALC-ENSANUT-PISOS-SALUD-0001` | 2021, 2022, 2023, 2024 (2025 RESERVADA) | 13 | 3 854 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-ENCODAT-PISOS-SUSTANCIAS-0001` | 2016–17 (2025 RESERVADA) | 10 | 658 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-ENBIARE-PISOS-BIENESTAR-0001` | 2021 (ola única, se abre) | 12 | 907 | REPRODUCE · IDENTICO, Δ máx 0.0 |

Lista cerrada, textos de pregunta y reglas: `forense/analisis/salud-bienestar/lista-cerrada-P1.md`.
Specs: `forense/prereg-caja/SALUD-{ENSANUT,ENCODAT,ENBIARE}-PISOS-spec-v1_0.md`. Tabla
conducta × segmento × ola con el id de cada RESULT: `forense/analisis/salud-bienestar/tabla-pisos-v1_0.tsv`
(978 filas, derivada de los `resultados.json` sellados). Diagnósticos: filas con diseño válido
= filas leídas en los 18 archivos; llaves no pareadas = 0 en los tres (ENCODAT: la llave
declarada `id_pers[:20] = id_hogar` pareó las 56 877 personas).

**IC calibrado de persistencia (ENSANUT).** τ² por (conducta, eje) sobre 2021→22→23→24 y
aplicado al piso 2024 (`-ICC-LO/-HI`). Es el parámetro reutilizable que pide el encargo; aquí
no se evalúa contra ninguna R.

**Sellado en disco, no registrado.** Los asientos E.7 de las tres corridas van en
`forense/replay-evidencia.tsv`; la vista `corridas/resultados.tsv` no viaja en el PR
(derivados protegidos, firma de mesa del 21/sep) → NC `-6d56-01`.

## 2 · Controles externos (el report cita una cifra de la misma encuesta y ola)

Cifras leídas de `tabla-pisos-v1_0.tsv`; el report, del mapa (`canon/mapa-dominios-v1_0.tsv`).

| afirmación | report | este acto | lectura |
|---|---|---|---|
| SALMEN-013 depresión adultos ENSANUT 2022 | 16.7 %; 60+ 38.3 % | 16.7 %; 60+ 38.3 % | COINCIDE (valida los cortes CESD-7 ≥ 9 / ≥ 5) |
| SALUD-009 necesidad de salud 2022 | H 21.6 % · M 27.4 % | H 21.6 % · M 27.4 % | COINCIDE |
| SALUD-006 atención en consultorio de farmacia 2022 | 17.7 % | 17.9 % [15.7, 19.9] | dentro del IC |
| JUV-009 ideación suicida 2022 | adol 7.6 % · adultos 7.7 % | adol 7.7 % · adultos 7.8 % | dentro del IC |

Cuatro cifras publicadas por terceros se reproducen desde el microdato con esta receta: es la
prueba de que universo, códigos y cortes son los del INSP. No es validación independiente
(E.2): la cifra ajena salió del mismo microdato.

## 3 · Bloque C por report

Vocabulario: CONFIRMA / MATIZA / ROMPE; NO-COMPARABLE cuando la escala o el universo no
enlazan (A-bis: sin función de enlace no se compara). Todas las cifras son de **personas**;
PROSPECTIVA/RETROSPECTIVA: ninguna — son pisos descriptivos contra afirmaciones ya escritas.

### *Salud, cuerpo y sustancias*

- **SALUD-009 / SALUD-036 («el hombre pospone»)** — MATIZA. La brecha grande está en
  **declarar** una necesidad (2024: H 21.2 %, M 26.8 %), no en **buscar** atención dada la
  necesidad (H 85.9 %, M 88.6 %; 2–4 pp todas las olas). Quien busca, es atendido: 98.8 %,
  sin gradiente. El mecanismo «machismo + costo de oportunidad» no se mide aquí; la conducta
  que el report predice existe pero es chica una vez condicionada a declarar la necesidad.
- **SALUD-006 / SALUD-030 (farmacia con consultorio)** — CONFIRMA el nivel 2021–2023
  (17.9–19.9 %) y MATIZA 2024: **10.9 %** [9.2, 12.6]. La caída coincide con el cambio de
  catálogo de `u0201` (IMSS-BIENESTAR se separa como categoría 26 en 2024; 23 → 26
  categorías). No se lee como caída de uso: es cambio de instrumento hasta que se demuestre
  lo contrario, y ensancha τ² de esa conducta. Por escolaridad no hay el gradiente
  «informal/barato» que el report implica (2024: primaria 7.5 %, secundaria 12.6 %, superior
  8.9 %); el eje «sin IMSS» no está en este CALC.
- **RURAL-021 (curandería, sistemas médicos propios)** — ROMPE como conducta de atención
  frecuente: curandero/hierbero/naturista es el lugar de atención de **0.2 %** de los
  utilizadores, también en lo rural (< 2 500 hab.: 0.2–0.3 %, IC hasta ~0.8 %), las cuatro
  olas. Acotación: `u0201` pregunta dónde se atendió quien usó servicios; la coexistencia de
  sistemas y su «lógica interna» no se miden. Con foco rural/indígena el número podría subir;
  ENSANUT no es muestra indígena.
- **SALUD-007 (alcohol en mujeres 62.6 % en 2016)** — NO-COMPARABLE en el nivel: ENCODAT
  2016 da **37.8 %** en los últimos 12 meses (12–65); la cifra del report no es de consumo
  anual (probablemente «alguna vez», que este acto no midió). La **dirección** que el report
  afirma (sube el consumo femenino) la CONFIRMA otra serie: ENSANUT adultas 20+, consumo en
  12 meses 40.1 % (2021) → 44.6 % (2022) → 49.1 % (2024), IC disjuntos 2021 vs 2024.
- **SALUD-008 (binge adolescente 8.3 % en 2016)** — MATIZA: 12–17 con 4+/5+ copas en un
  día del último año = **6.8 %** con la definición de §2; la del report no está verificada.
- **SALUD-019 (cigarro electrónico 1.1 % en 2016)** — NO-COMPARABLE: `tb50` se preguntó a
  una submuestra (N = 19 906 de 56 877); el 12.9 % de este CALC es **condicional al filtro
  del cuestionario**, no prevalencia poblacional. Se declara; no se usa como piso nacional.
- **SALUD-039 (opioides 0.1 % → 1.4 %)** — MATIZA: opiáceos sin receta **alguna vez** en
  2016 = 2.0 % [IC en la tabla]; la ventana del report (último año) no está en este CALC.
- **Diagnóstico previo** (sin afirmación directa en el mapa): diabetes 10.8 %, hipertensión
  17.7 % (2024). Gradiente fuerte por escolaridad (diabetes: primaria 19.8 % vs superior 6.4 %)
  que **es sobre todo edad** (la escolaridad baja se concentra en 60+) y acceso a
  diagnóstico: no se lee como conducta.

### *Salud mental*

- **SALMEN-013** — CONFIRMA (§2, cifra exacta). **SALMEN-014 (brecha por sexo)** — CONFIRMA:
  2024 M 22.0 % vs H 11.2 %, estable 2021–2024 (IC calibrado incluido).
- **JUV-009** — CONFIRMA la ideación; el «intento» no es construible por texto en 2021–2023
  (a1213 es autolesión) → NC.
- **Gradiente educativo** (no está en el mapa como afirmación; útil para el modelo):
  depresión 27.4 % con hasta primaria vs 9.8 % con superior (2024), mismo patrón en ENBIARE
  (29.2 % vs 12.1 %). Riesgo de mala lectura: mezcla edad (60+ con escolaridad baja),
  ingreso y acceso; no es «cultura de la resignación».
- **Ansiedad (GAD-2 ≥ 3, ENBIARE 2021)**: 19.3 %; M 23.2 % vs H 15.0 %; más alta en
  localidades < 2 500 (22.3 %) que en ≥ 100 mil (17.4 %). Cribado, no diagnóstico.

### *Bienestar subjetivo* (EMOC-028)

- **EMOC-028 («satisfacción alta»)** — CONFIRMA el nivel: satisfacción con la vida 8.45/10,
  escalera de Cantril 7.73/10 (ENBIARE 2021). La comparación entre países («la más alta, la
  depresión más baja») no se mide; y la depresión por CESD-7 en el mismo instrumento es
  18.4 %, así que «alta satisfacción» y «síntomas depresivos en uno de cada cinco» conviven.
- **CLASE-040 (facilidad para cubrir gastos)** — NO-CONSTRUIBLE: el ítem no está en ENBIARE
  2021. El gradiente de satisfacción por escolaridad (8.14 → 8.74) es compatible con una
  lectura económica pero no la identifica.

### *Confianza y desconfianza*

- **TRUST-007 (confianza personal alta, institucional baja, a la vez)** — CONFIRMA: gente
  conocida 7.62/10, mayoría de la gente 5.30, policía municipal 3.87, partidos 3.53.
- **TRUST-009 («México: las mujeres confían más que los hombres»)** — ROMPE en ENBIARE
  2021: en la mayoría de la gente M 5.11 [5.05, 5.16] vs H 5.51 [5.45, 5.56]; en conocidos
  M 7.56 vs H 7.67. Acotación: la afirmación viene de otro instrumento (WVS); aquí el signo
  es el contrario y los IC no se tocan.
- **TRUST-011 (menor escolaridad confía más en el gobierno)** — MATIZA/CONFIRMA en
  dirección con otras instituciones: partidos 4.09 (hasta primaria) vs 3.01 (superior);
  policía municipal 4.13 vs 3.69. ENBIARE no pregunta por el gobierno federal.
  Lectura cuidadosa: las localidades < 2 500 confían **más** en policía y partidos (4.42 y
  4.05) que las de ≥ 100 mil (3.47 y 3.19) — evaluación de instituciones distintas, no
  «deferencia rural».
- **TRUST-015 (horizontal intacta)** — CONFIRMA en nivel: 94.8 % cuenta con ayuda de la
  familia ante una urgencia; 72.2 % con la de amistades.
- **TRUST-001 (confianza generalizada ~22 %, WVS)** — NO-COMPARABLE: ENBIARE da una media
  0–10 (5.30), no la proporción dicotómica de WVS; sin enlace no se compara.

### *Capital social no familiar*

- **CAPSOC-002 / -003 (ENCUCI: 32.1 % alta en la mayoría; 62.1 % en conocidos)** —
  NO-COMPARABLE en nivel (media vs proporción 8–10); CONFIRMA el orden conocidos ≫ mayoría.
- **Apoyo de amistades ante urgencia** (72.2 %) con gradiente educativo (66.2 % hasta
  primaria vs 82.0 % superior) y de tamaño de localidad (67.9 % en < 2 500 vs 74.6 % en
  ≥ 100 mil): la red no familiar es más delgada abajo y en lo rural. Riesgo de mala lectura:
  no es «familismo» cultural, la red familiar es igual de alta en todos los segmentos
  (93–97 %).

### *Religiosidad* (ENBIARE la pregunta → entra)

- **RELIG-007 («sin religión» 8.1 %, Censo 2020)** — MATIZA: ENBIARE 2021 «¿Usted tiene una
  religión?» = **81.8 %** sí → 18.2 % no. El doble del Censo se explica por la pregunta: el
  creyente sin adscripción (categoría que el Censo separa) puede contestar «no»; no se lee
  como secularización de 10 puntos.
- **RELIG-026 (generación joven menos religiosa)** — CONFIRMA en México: tiene religión
  73.0 % (18–29) vs 91.4 % (60+), IC disjuntos; asistencia 33.7 % vs 65.1 %.
- **RELIG-004 (47.8 % de los católicos asiste semanalmente)** — NO-COMPARABLE: PG7 no
  pregunta frecuencia ni denominación; 48.1 % de todos los adultos «acostumbra asistir».

## 4 · Módulo de auditoría (§5 de las instrucciones)

- **Contadores que movió este trabajo:** 3 CALC sellados con `cuenta_gen2: SI` (sellados en
  disco, no registrados en la vista; ver NC-01); «conductas con piso GEN2 por dominio» de 0 a
  35 en los cinco dominios del encargo; 0 adopciones; `celdas_validadas` 219 → 219.
- **¿Precariedad confundida con cultura?** Los gradientes por escolaridad y tamaño de
  localidad (depresión, ansiedad, apoyo de amistades, confianza en instituciones, farmacia)
  se leen como ingreso, acceso y oferta antes que como rasgo; el acto no tiene medida de
  ingreso y no identifica mecanismo.
- **Oferta antes que preferencia.** Uso de farmacia y curandero se publica al lado de
  BUSCO-ATENCION y FUE-ATENDIDO por los mismos ejes; lo que falta (afiliación, distancia,
  costo) queda para el sucesor.
- **Firewall genético.** Alcohol y tabaco se describen por sexo, edad, escolaridad y
  localidad; ningún eje es étnico ni hereditario.
- **Sobre-generalización urbana.** ENSANUT separa lo rural (< 2 500); ENCODAT también
  (`estrato`); ENBIARE por TLOC. Ninguna de las tres es muestra indígena.
- **Escalas.** Proporciones de personas y medias 0–10 nunca se comparan entre sí; tres
  afirmaciones quedaron NO-COMPARABLE por eso. Los universos difieren por archivo (adultos
  20+, integrantes todas las edades, utilizadores, 12–65, 18+) y así se reportan.
- **Evidencia débil con intuición fuerte.** Cigarro electrónico (universo filtrado) y
  farmacia 2024 (catálogo) quedan marcados; no se usan como piso sin reserva.
- **Cifra escrita a mano:** ninguna. Los números de esta nota se leyeron de
  `tabla-pisos-v1_0.tsv` en la sesión; los del report, del mapa.

## 5 · Adopción por instrumento (F-ASTRA-5-4)

Tres FP abiertas, una por instrumento, con ADOPTAR / CON-RESERVA-DE-ANCHO / VETAR:
`FP-260924-GEN2-SALUD-Y-BIENESTAR-PISOS-1-6d56-01` (ENSANUT; recomendada
CON-RESERVA-DE-ANCHO: farmacia 2024 y curandero con IC calibrado ancho),
`-6d56-02` (ENCODAT; recomendada CON-RESERVA-DE-ANCHO: cigarro electrónico condicional al
filtro, sin serie), `-6d56-03` (ENBIARE; recomendada ADOPTAR como piso de una ola, sin
persistencia). Este acto no adopta nada.
