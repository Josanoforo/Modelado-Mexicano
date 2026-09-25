**Conductas con piso GEN2 por dominio (este acto; derivado por `python3 forense/analisis/confianza-capital-social/tabla_pisos_confianza.py`, pares CALC×conducta con TOTAL estimado): CONFIANZA 31 · CAPITAL_SOCIAL 16 · AUTORIDAD 16 · RELIGIOSIDAD 13 · VALORES-FUERA-DEL-MAPA 3 — 79 pares, 4 CALC sellados, 0 adopciones.**

# Nota de cierre · ACTO GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1

25/sep/2026 · CAJA (Ubuntu/WSL2, corpus montado, `ENTORNO-DERIVADO = CAJA`; `data/raices.local.yaml`
apunta `descargas_mx` al espejo `mm-corpus/descargas_mx_espejo`) · Opus 5.5 · rama
`acto/gen2-confianza-religiosidad-capital-social-pisos-1` · 0-bis `ac7b169e` · base `origin/main`
`40058c09` (= SHA de redacción). Encargo:
`forense/encargos/2026-09-25-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1.md`.

**Secuencia.** 0-bis → informes de estructura (cuatro agentes Sonnet, sólo metadatos; `f4415f5c`) →
auditoría propia de cada código usado → COMMIT-1 `0d3b52bf` (lista cerrada, specs, `spec.yaml`,
medidores, motor, prueba sintética; preflight VERDE ×4, empujado a origin **antes** de abrir dato) →
COMMIT-2a..d (`21aa4be9`, `57e6cc71`, `b1adf575`, `1004fae4`: una corrida por CALC, la primera) →
verify aislado → asientos E.7. **Ningún valor de microdato de estos reactivos se leyó antes del
COMMIT-1.** Después del sello se leyeron dos diagnósticos descriptivos (no alteran nada sellado):
frecuencias de 4 reactivos PEW con n = 0 y de `ur` LAPOP 2004 (§1).

## 1 · Qué se midió

| CALC | olas abiertas (reservada) | conductas | RESULT | verify aislado |
|---|---|---|---|---|
| `CALC-WVS-PISOS-2018-0001` | 2018 (ola única, se abre) | 32 | 3 049 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-LATINOBAROMETRO-PISOS-2023-0001` | 2023 (**2024 RESERVADA**) | 21 | 1 794 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001` | 2013, 2015, 2017, 2018, 2023, 2024 (**2025 RESERVADA**) | 7 (23 conducta×ola) | 1 324 | REPRODUCE · IDENTICO, Δ máx 0.0 |
| `CALC-LAPOP-PISOS-CAPITAL-SOCIAL-0001` | 2004, 2006, 2019 (**2023 RESERVADA**; 2021 fuera) | 20 | 3 267 | REPRODUCE · IDENTICO, Δ máx 0.0 |

Lista cerrada, textos, códigos, diseño y dictamen de equivalencia:
`forense/analisis/confianza-capital-social/lista-cerrada-P1.md`. Specs:
`forense/prereg-caja/CONFIANZA-{WVS,LATINOBAROMETRO,PEW,LAPOP}-PISOS-spec-v1_0.md`. Tabla conducta ×
segmento × ola con el id de cada RESULT: `forense/analisis/confianza-capital-social/tabla-pisos-confianza-v1_0.tsv`
(1 852 filas, derivada de los `resultados.json` sellados).

**Primer resultado, tal cual (celdas sin estimación).** (i) PEW: cuatro celdas salen con n = 0 —
`CONFIANZA-INTERPERSONAL` 2017, `CONFIA-GOBIERNO-NACIONAL` 2024, `ORA-DIARIO` 2018 y 2023. Diagnóstico
posterior al sello: la variable existe en el archivo multipaís pero **no se aplicó en México** (todas
las filas mexicanas vacías). Es «la fuente no tiene el dato para México», no un defecto del medidor;
el informe de estructura contó presencia de la variable, no aplicación por país. (ii) LAPOP 2004: el
eje UR sale vacío — `ur` existe y está vacía en las 1 556 filas; ESCOLARIDAD, SEXO y EDAD sí salen.
(iii) WVS `Q289`: 84 de las 1 739 personas de 18+ (`-G-FILAS-18-MAS`) quedan fuera de
`PERTENECE-DENOMINACION`/`CATOLICO` (n 1 655) por código fuera de 0–7 («otros», según el cuestionario)
o sin respuesta, como fijó la lista cerrada.

**IC calibrado de persistencia (PEW).** τ² por (conducta, eje) sobre las olas con texto IDÉNTICO,
aplicado a 2024 (`-ICC-LO/-HI`): RELIGION-MUY-IMPORTANTE (6 olas, τ²_TOTAL sobre 5 Δ) y los tres
sistemas de gobierno (2017→2023→2024, 2 Δ en TOTAL). Parámetro reutilizable; no se evalúa aquí.
LAPOP: sin τ² (FIRMAS-15 T).

**Sellado en disco, no registrado.** Asientos E.7 de las cuatro corridas en
`forense/replay-evidencia.tsv`; la vista `corridas/resultados.tsv` no viaja en el PR (derivados
protegidos, firma de mesa del 21/sep) → NC `…-ac7b-01`.

## 2 · Controles externos (el report cita una cifra de la misma encuesta y ola)

| afirmación | report | este acto (RESULT) | lectura |
|---|---|---|---|
| AUTOR-004 obediencia como cualidad infantil, WVS 2018 | 57 % | 57.2 % [54.7, 59.6] (`…WVS-PISOS-2018-OBEDIENCIA-CUALIDAD-INFANTIL-2018-TOTAL-TODOS-P`) | COINCIDE |
| EMOC-019 confianza en el gobierno, Latinobarómetro 2023 | ~38 % | 38.1 % [35.2, 40.9] (`…LATINOBAROMETRO-PISOS-2023-CONFIA-GOBIERNO-2023-TOTAL-TODOS-P`) | COINCIDE |
| TRUST-001 / EMOC-017 confianza interpersonal generalizada, WVS 2018 | ~22 % | **10.5 %** [8.8, 12.1] (`…WVS-PISOS-2018-CONFIANZA-INTERPERSONAL-2018-TOTAL-TODOS-P`) | **NO SE REPRODUCE** |

Dos cifras publicadas se reproducen desde el microdato con esta receta (corte «mucha/algo» y
«mencionó» verificados). La tercera no: Q57 = 1 ponderado, 18+, sin no-sabe, da 10.5 %; el «22 %» no
sale de WVS 2018 México con ningún universo de esta spec. Ni el ~22 % ni el 12–28 % de TRAB-006 caben
en el IC. No es validación independiente (E.2).

## 3 · Bloque C por report

Vocabulario: CONFIRMA / MATIZA / ROMPE; NO-COMPARABLE cuando la escala, el universo o la ola no
enlazan (sin función de enlace no se compara; una ola reservada no se abre para adjudicar). Todas las
cifras son de **personas 18+**, RETROSPECTIVAS; ninguna PROSPECTIVA. Cada instrumento en su escala.

### *Confianza y desconfianza en México: anatomía de una sociedad dual*

- **TRUST-001 / EMOC-017 / CONS-012 / TRAB-006 (confianza generalizada «~22 %», «12–28 %»)** —
  **ROMPE la cifra, CONFIRMA la dirección.** WVS 2018: 10.5 % [8.8, 12.1]. Latinobarómetro 2023, con la
  misma pregunta dicotómica: 31.3 % [28.5, 34.0]. Las dos son la misma pregunta en dos encuestas y
  distan 20 pp: **el nivel de «confianza generalizada» mexicano no es un dato estable entre casas
  encuestadoras** (marco, orden, modo), y ningún report debería usar un solo número. La serie WVS
  1990–2012 (33 % → 16 % → 12 %) no está en corpus (sólo la ola 7): NO-VERIFICABLE-AQUÍ.
- **TRUST-002 (radial alta, amplia baja)** — **CONFIRMA**, con gradiente limpio en una sola encuesta
  y escala (WVS 2018, confía completamente o algo): familia 91.9 % · vecinos 49.7 % · conocidos 43.0 %
  · gente que conoce por primera vez 13.1 % · «la mayoría de las personas» 10.5 %. LAPOP (otra
  pregunta, «la gente de su comunidad es muy o algo confiable»): 63.5 % (2004), 65.8 % (2006),
  54.0 % (2019). La confianza «dual» es la forma del dato, no una metáfora.
- **POL-001 / AUTOR-026 (jerarquía institucional; baja institucional + alta interpersonal)** —
  **CONFIRMA la jerarquía, MATIZA el «alta interpersonal».** WVS 2018: iglesias 61.8 %, ejército
  50.7 % > tribunales 22.5 %, policía 21.3 %, elecciones 20.2 %, gobierno 17.5 %, congreso 14.6 %,
  partidos 11.3 %. Latinobarómetro 2023 (mucha/algo): FFAA 58.5 %, Iglesia 54.6 %, presidente 51.3 %
  > institución electoral 46.3 % > gobierno 38.1 %, poder judicial 34.0 %, congreso 32.7 %, policía
  31.1 %, partidos 24.6 %. Mismo orden en dos instrumentos. Lo «alto» es la confianza radial y
  comunitaria; la generalizada es baja en toda fuente. Que la jerarquía sea «calibración racional del
  desempeño» no se mide aquí (mecanismo): el orden es compatible con ella, pero no la prueba.
- **VIOL-037 (FFAA «alta y estable»)** — **CONFIRMA «alta» relativa, MATIZA «estable».** Es la
  institución secular más confiable en WVS y en Latinobarómetro, pero LAPOP (6–7 de 7) da 46.1 %,
  54.3 % y 44.2 % en 2004/2006/2019 (sin serie por FIRMAS-15 T; ruptura de 10 pp entre olas
  presenciales).
- **TRUST-022 / CONOC-014 / TEC-036 / TIME-030 / SANC-005 (Latinobarómetro 2024)** —
  **NO-COMPARABLE: ola RESERVADA**, no se abrió para adjudicar. Latinobarómetro 2023 queda como piso
  de la ola anterior (gobierno 38.1 %, confianza interpersonal 31.3 %).
- **CAPSOC-008 (PEW 2025, «18 % confía en la mayoría»)** — **NO-COMPARABLE: ola RESERVADA.** Además,
  PEW no aplicó `trustpeople` en México en 2017 (n = 0): no hay piso PEW previo con el que compararla.

### *Capital social no familiar en México*

- **CAPSOC-030 («dos tercios no contribuyó»; asociacionismo formal correlaciona con escolaridad)** —
  **CONFIRMA el nivel, ROMPE el gradiente educativo.** LAPOP «contribuyó a resolver un problema de su
  comunidad»: 32.1 % (2004), 30.9 % (2006) → cerca de dos tercios no. Pero ni esa conducta ni asistir
  a un comité de mejoras suben con la escolaridad: comité de mejoras 2019 hasta primaria 16.9 %
  [12.7, 21.2] vs superior 14.4 % [10.3, 19.0]; 2006 rural 26.3 % vs urbano 11.7 %. La participación
  comunitaria **es más rural y de menor escolaridad**, no de «barrios de mayor escolaridad». El
  gradiente que el report cita es de asociacionismo formal profesional (asociación profesional 7.0 %
  y 6.6 %, sin corte por escolaridad aquí): la afirmación mezcla dos objetos.
- **Participación religiosa como capital social (CAPSOC-023)** — **CONFIRMA que la religiosa es la
  asociación de masas.** WVS 2018: miembro de iglesia u organización religiosa 55.5 %, activo 26.9 % —
  contra deportiva 13.5 %, partido 5.1 %, ayuda mutua 6.9 % (activo). LAPOP: asiste a reuniones de
  organización religiosa al menos mensual 41.3 % / 55.1 % / 39.9 %, mujeres por encima de hombres en
  las tres olas (2006: 62.4 % vs 47.6 %). La especificidad evangélico-pentecostal y de clase baja no
  se mide (sin corte por denominación).
- **Acción política no convencional** — Latinobarómetro 2023: firmó una petición 20.4 %, asistió a
  manifestación autorizada 11.5 %, trabaja (muy) frecuentemente por su comunidad 18.0 %. WVS 2018:
  11.3 % y 9.1 %. Distinta redacción y casa: sólo dirección («minoría de uno de cada diez a uno de
  cada cinco»), sin enlace.

### *Religiosidad y psicología del mexicano contemporáneo*

- **RELIG-002 / JUV-016 / EMOC-029 (católicos 67–78 %; descenso; «sin religión» joven)** —
  **CONFIRMA la dirección, NO-COMPARABLE el nivel.** Católico: WVS 2018 79.0 %; Latinobarómetro 2023
  70.3 % [67.7, 73.0]. Sin religión (agnóstico, ateo, ninguna) Latinobarómetro 2023: 11.7 %, 15.4 %
  en 18–29 vs 6.8 % en 60+. El Pew 2026 (67 %) sale de la ola 2025, RESERVADA; el Censo es otra
  unidad (población total, no 18+).
- **La religiosidad no está cayendo en «importancia»** (lo que el report sugiere con la
  desafiliación) — **MATIZA.** PEW, texto idéntico 2013–2024, «la religión es muy importante en su
  vida»: 45.0 %, 37.2 %, 51.3 %, 52.6 %, 47.0 %, 50.1 %; IC calibrado 2024 [34.6, 65.6]. Seis olas sin
  tendencia descendente; lo que cae es la adscripción católica, no la importancia declarada. El
  gradiente por edad es fuerte y estable (2024: 18–29 43.0 %, 60+ 67.7 %; WVS 2018: 41.7 % vs
  64.0 %): cohorte o ciclo de vida, no separable con estas olas.
- **RELIG-004/005 (asistencia; ENCREER)** — **NO-COMPARABLE** (otra encuesta, católicos vs total).
  Asistencia mensual o más: WVS 2018 60.7 % (mujeres 65.8 %, hombres 55.1 %); LAPOP 2019 61.7 %.
  Importancia de Dios (WVS, 1–10): media 8.59.
- **Pew *Religion in Latin America* 2014 (RELIG-017/023)** — no está en corpus: NC con receta.

### *Autoridad y jerarquía en el México contemporáneo*

- **AUTOR-004 (57 % obediencia)** — **CONFIRMA** (COINCIDE, §2). Lo que el report le añade («respeto
  performativo») no se mide. Gradiente leve por escolaridad (hasta primaria 59.8 %, superior 51.7 %).
  **AUTOR-008 (EE. UU. 28 %, Japón 3 %)**: esas olas no están en corpus → NO-VERIFICABLE-AQUÍ.
- **AUTOR-001/010 («77.5 % quiere un líder fuerte», ENCUCI)** — **MATIZA por instrumento.** WVS 2018,
  «un líder fuerte que no se moleste por el congreso y las elecciones» muy o algo bueno: 71.7 % —
  cerca del 77.5 % de ENCUCI, pero otra encuesta. PEW, otro texto («sin interferencia del parlamento
  o las cortes»): 29.3 % (2017), 51.2 % (2023), 43.8 % (2024). LAPOP, «un líder fuerte que no tenga que
  ser elegido»: 16.9 % (2004), 11.9 % (2006). **El «apoyo al líder fuerte» va de 12 % a 72 % según
  si la pregunta cuesta elecciones o no**: no es una disposición única que se pueda citar con un número.
- **AUTOR-031 («33 % acepta formas autoritarias»)** — **CONFIRMA el orden de magnitud con otro
  instrumento.** Latinobarómetro 2023: «en algunas circunstancias un gobierno autoritario puede ser
  preferible» 34.7 %; democracia preferible sólo 36.4 %. Pero «no me importaría un gobierno no
  democrático si resuelve los problemas» sube a 58.5 %, y apoyaría un gobierno militar «si las cosas
  se ponen muy difíciles» 44.5 %. PEW «que los militares gobiernen» muy o algo bueno: 44.0 % (2017),
  59.0 % (2023), 63.7 % (2024); IC calibrado 2024 [41.8, 81.1]. LAPOP golpe «justificado» ante mucha
  delincuencia: 49.0 %, 63.1 %, 44.0 %. **El apoyo condicional a salidas militares es mayoritario o
  cercano a la mitad en cuatro instrumentos**; su gradiente es de escolaridad (PEW 2023 hasta
  primaria 67.8 % vs superior 47.1 %) y, en PEW, no se ve el colapso por edad que un relato «Gen Z
  igualitaria» esperaría (τ² por edad alto: la serie es ruidosa, ver τ²).
- **AUTOR-005/006/014, INTER-031 (Hofstede PDI 81, GLOBE)** — marcos importados, no medibles aquí
  (índice de empleados de IBM; GLOBE sin microdato). Se citan con crítica, no como hecho (§3).
- **Justicia por propia mano (LAPOP e16, sólo 2004/2006)**: 28.1 % y 17.2 % aprueban (6–10 de 10).
  Descriptivo; APUEST-006 (mordida, módulo EXC) no se midió (NC).

### *Tolerancia* (VALORES, fuera del mapa)

- LAPOP «aprueba que homosexuales se postulen a cargos públicos» (6–10): 49.1 %, 51.6 %, 60.6 %
  (2004/2006/2019); 18–29 68.6 % vs 60+ 47.7 % en 2019. WVS 2018: no quiere homosexuales de vecinos
  22.8 % (60+ 30.9 %); homosexualidad justificable, media 4.39 de 10. Sin report del mapa que las
  reclame: pisos disponibles.

### *Emociones morales* (sólo lo medible)

Ningún reactivo de culpa, vergüenza o dignidad existe en los cuatro instrumentos. EMOC-017/019
(confianza) se dictaminan arriba. Lo demás del report: NC.

## 4 · Auditoría de rigor extremo

- **¿Cuántos contadores movió?** «N conductas con piso GEN2 por dominio»: 79 pares CALC×conducta en
  cinco rótulos de dominio (primera línea). `celdas_validadas`: no se toca (descriptivo, ninguna
  celda-D). Adopciones: 0.
- **¿Pobreza, violencia o informalidad confundidas con cultura?** La baja confianza en policía (WVS
  21.3 %, sin gradiente por tamaño de localidad: 19.8–23.0 %) y tribunales es evaluación de
  instituciones con desempeño medible, no rasgo; la nota no la lee como «desconfianza cultural». El
  apoyo a gobierno militar sube donde baja la escolaridad: primero exposición a inseguridad e ingreso,
  no «autoritarismo mexicano».
- **¿Sobregeneralización de clase media urbana?** Los ejes de localidad y escolaridad existen en los
  cuatro CALC; la participación comunitaria es rural y de baja escolaridad (§3), lo contrario de la
  lectura clasemediera.
- **¿Marcos importados?** WVS se usa como encuesta (datos primarios en México, evidencia (a)); sus
  índices culturales (Inglehart-Welzel) y Hofstede no se usan. Ninguna cifra es (b) diáspora.
- **¿Foco rural/indígena?** Sólo el eje de localidad; no hay muestra indígena ni lengua. Firewall
  genético: ninguna segmentación por color de piel, etnia ni ascendencia (LAPOP trae `colorr`; no se
  usa).
- **¿En qué escala está cada cantidad?** Proporciones de personas 18+ en la escala de su instrumento;
  dos medias 1–10 (WVS). Ninguna comparación numérica entre instrumentos: donde dos instrumentos
  aparecen juntos es dirección, dicha así. **¿PROSPECTIVA/RETROSPECTIVA?** Todo RETROSPECTIVO.
- **¿Evidencia débil e intuición fuerte?** Latinobarómetro sin estrato ni UPM: su IC es una cota
  inferior. WVS sin estrato: IC de conglomerados con estrato único (más ancho que el de diseño). PEW
  2013/2023/2024 sin diseño publicado: MAS ponderado.
- **¿Qué sería peligroso leído simplista?** «Sólo 10 % confía» (WVS) y «31 % confía»
  (Latinobarómetro) son la misma pregunta: citar una sola es elegir casa encuestadora. «Los mexicanos
  quieren un líder fuerte» vale 12 % o 72 % según el texto.
- **¿Afirmación sobre el corpus escrita a mano?** Ninguna cifra tecleada: toda sale de
  `tabla-pisos-confianza-v1_0.tsv` o de un RESULT citado. Las tres cifras de conteo que la sesión tecleó en un
  borrador de la lista cerrada se re-derivaron por comando antes del COMMIT-1.

## 5 · FP de adopción por instrumento (PROPUESTAS; mesa firma)

| FP | instrumento | recomendación | razón |
|---|---|---|---|
| `FP-260925-GEN2-CONFIANZA-RELIGIOSIDAD-CAPITAL-SOCIAL-PISOS-1-ac7b-01` | WVS 2018 | CON-RESERVA-DE-ANCHO | una ola; sin estrato (IC de conglomerados con estrato único); confianza generalizada 10.5 % discrepa del ~22 % citado — el piso es el dato, el report se corrige |
| `…-ac7b-02` | Latinobarómetro 2023 | CON-RESERVA-DE-ANCHO | sin estrato ni UPM (IC = cota inferior); 2024 RESERVADA |
| `…-ac7b-03` | PEW 2013–2024 | CON-RESERVA-DE-ANCHO | diseño parcial por ola; IC calibrado ancho (τ² 0.20–0.67 en sistemas de gobierno); 4 celdas sin aplicación en México |
| `…-ac7b-04` | LAPOP 2004/2006/2019 | CON-RESERVA-DE-ANCHO | sin serie hasta dictamen de equivalencia (FIRMAS-15 T; dictamen textual propuesto en lista cerrada §6); UR 2004 vacía |

## 6 · Premisas del encargo que no se sostuvieron (declaradas, no PARO)

1. «WVS bajo otros ids o pendiente de solicitud»: estaba en manifiesto desde el 12/ago
   (`f000…`); se midió.
2. «Citar `CALC-ENCIG-*` de confianza ya sellados»: no existe ninguno (0 ids en 41 directorios
   ENCIG) → NC.
3. «LAPOP y Latinobarómetro traen pesos y diseño» `[SUPUESTO]`: LAPOP sí; Latinobarómetro trae peso
   sin diseño → rama prevista por el encargo, dicha.
4. «PEW *Religion in Latin America*»: no está en corpus → NC con receta.
5. «VALORES» como dominio: no existe en el mapa (0 de 1 396 filas).

## 7 · Latitud usada (cláusula de autonomía)

Regla 1: discrepancias encargo↔repo resueltas y declaradas (§6). Regla 3: dictamen de equivalencia
textual por ola, **PROPUESTO-POR-EJECUTOR** (lista cerrada §6), fuente: etiquetas y cuestionarios.
Regla 4: alcance recomendado ejecutado — cuatro instrumentos con microdato, olas más recientes
reservadas, LAPOP 2021 fuera. Preguntas a mesa: ninguna.
