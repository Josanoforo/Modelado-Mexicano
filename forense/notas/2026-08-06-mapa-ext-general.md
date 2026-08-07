# MAPA-EXT-1 · Fuentes externas con capacidad material

Fecha de revisión: 2026-08-06. Este acto no descarga microdatos, no ejecuta
mediciones, no modifica sellos ni adjudica resultados. `SATISFACE-UMBRAL-DOCUMENTAL`
solo indica que la documentación primaria parece contener las piezas exigidas.

## Punto de partida y reserva de paths

Worktree: `/home/pc0/proyectos/Modelado-Mexicano-mapa-ext-1`, rama
`agent/mapa-ext-1`, base `origin/main` en `f542c93` después del merge de PR #161.

Tres paths nombrados por el encargo no existen en esa base:
`data/catalogo-fuentes-v1_0.md`, `data/catalogo-fuentes-derivado.tsv` y
`data/cruce-catalogo-fichas-v2_0.tsv`. Se usaron sus artefactos vigentes
disponibles, `data/catalogo-fuentes-v2_0.md` y
`forense/cruce-catalogo-fichas-v2_0.md`. No se reconstruyeron los ausentes.

## Universo revisado y método

Se extrajeron de la matriz únicamente objetos en estados abiertos o bloqueados.
Las necesidades se agruparon por piezas de diseño, no por institución:

| grupo | objetos | constructo/exposición y desenlace requeridos | unidad/diseño | condición exacta faltante |
|---|---|---|---|---|
| crédito y consumo | R1.3 pierna 3, R1.4, R1.5-R1.7, R8.2 | canal de alta; compra real y marca; modalidad y daño crediticio; tanda y cumplimiento | persona/compra/grupo, misma muestra | canal propietario; panel de compra por estrato; BNPL separado; participantes desconocidos y ciclos |
| trabajo/organización | R2.1-R2.4, R10.2 | reporte voluntario de error, jerarquía/liderazgo, feedback y desempeño | trabajador dentro de organización, comparación | ninguna fuente conocida une tipología organizacional y resultado conductual/productivo |
| Estado/trámite | R3.1-R3.4 | reproducibilidad ENCIG; discrecionalidad; CoDi/SPEI y mecanismo | persona/trámite o serie; comando preservado | R3.1/R3.2 requieren artefacto, no fuente; R3.3 mapeo; R3.4 motivo individual y anti-confusión |
| salud/acceso | R4.1, R9.1, R9.2 | mejora fechada de acceso; consulta/no consulta; campaña y disponibilidad independiente | individuo/establecimiento/entidad, evento o enlace | evento operativo+CLUES+pre/post; llave hogar-establecimiento; payload externo con campaña, periodo y denominador |
| familia/pareja | R5.1-R5.4; familismo | tratamiento pensión; actitud/deber, conducta de cuidado, apoyo y desenlaces de pareja/apps | persona/hogar; panel cuando corresponda | 2018 ENASEM; actitud frente a conducta y población; desenlace coobservado |
| participación y conflicto | R7.1, R7.3-R7.9, R8.1-R8.4 | elección concurrente, clientelismo/atribución, protesta/autodefensa, cooperación/sanción, confianza | votante, evento, comité o municipio; panel/evento | misma muestra voto-mecanismo; evento+actor+entorno; comité individual+monitoreo+sanción |
| comunicación | R10.1, R10.3-R10.4 | rechazo indirecto por jerarquía; testificación protegida; directividad | interacción/persona; grupo comparable | muestra mexicana no universitaria y datos replicables; límite ético; reactivo conductual |
| coeficientes/condicionales | horizonte temporal, familismo, radio de confianza, deferencia y confianza institucional | reactivos directos y desenlace pertinente en misma muestra | persona; panel para horizonte causal | proxies débiles, instrumentos separados, diseño no publicado o equivalencia conceptual |

Para cada grupo se consultaron primero páginas del productor, cuestionarios,
codebooks, fichas de acceso y repositorios primarios. Se cruzaron nombres contra
catálogo v2, puertas, ABRIR-4, VERIF-3, EXPLORA-2, BARRIDO-1, índices y
manifiesto antes de promover una candidata. No se reabrieron ENNViH, ENBIARE,
ACLED_HDX, Cero Desabasto, CLUES, Latinobarómetro, LAPOP, Global Findex ni el
Mexico Panel Study 2012 cuando el repositorio ya documentaba su estado.

Clases efectivamente revisadas: federal/autónoma (INEGI, Banxico), municipal
(CNGMD y portal CDMX localizado pero no promovido), regulador/administrativo
(IMSS-BIENESTAR), universidades/repositorios (Bonn, CSES, GESIS/ISSP, Harvard),
civil/periodismo de datos (puertas previas y registros de protesta),
internacionales (OCDE, Banco Mundial, WVS, UCDP, GDELT) y restringidas
(ICPSR, Nielsen/Kantar, estudios pragmáticos).

## Candidatos materiales

La tabla completa vive en `data/mapa-fuentes-externas-2026-08-06.tsv`. Los
hallazgos principales son:

1. **Banxico Competencias Financieras 2019-2024.** Fuente omitida del catálogo
   que publica microdatos y manual por año. Documenta crédito de aplicación,
   microfinanciera, tienda, historial/estrés y tandas en el mismo instrumento.
   Puede desbloquear R1.5-R1.7; no se afirma que separe BNPL ni tandas entre
   desconocidos.
2. **ISSP Redes Sociales 2017 México (n=1,002).** Une redes, apoyo, deberes,
   confianza y participación en población general. Es la mejor puerta para
   resolver familismo sin el filtro de necesidad de cuidado.
3. **ISSP Familia 2012 México (n=1,527).** Permite contrastar actitudes, reparto
   doméstico/cuidado y empleo en la misma muestra. Requiere abrir MX12 antes de
   atribuir texto literal.
4. **CSES México 2018.** Microdato y diseño libres; coobserva voto, turnout,
   contactos, voz y actitudes. Es fuerte para R7.6-R7.9, no sustituye un padrón
   de beneficiarios ni crea un panel.
5. **Mass Mobilization.** Registra protesta, demanda, respuesta gubernamental,
   identidad y lugar para 1990-2018. Es la apertura de menor costo para saber si
   R7.4/R7.5 pueden pasar a evento×entorno.
6. **ENCOAP 2023.** Encuesta mexicana especializada, probabilística y urbana,
   con confianza interpersonal/institucional, servicios, voz y participación.
   Puede recalibrar condicionales en la misma muestra.
7. **Global Preferences Survey.** Reactivos validados directos de riesgo,
   tiempo y confianza. La cobertura/submuestra mexicana y los desenlaces deben
   verificarse antes de promoverla a medición.
8. **GDELT 2.0.** Proporciona actores, CAMEO, fecha y coordenadas; exige una
   construcción costosa de universo, deduplicación y entorno.
9. **IMSS-BIENESTAR infraestructura 2026.** Es una exposición de obra fechada y
   localizada potencial para R4.1 futuro; por su periodo no cambia hoy el
   resultado sellado.
10. **CNGMD 2023.** Tiene secciones explícitas de participación ciudadana a
    nivel municipal. Sigue sin mapear si observa comité, sanción o recurrencia.

## Candidatas secundarias y no-satisfacción

- **World Bank Enterprise Survey México 2023 (n=1,322)** coobserva gestión,
  fuerza laboral, corrupción y desempeño, pero la documentación revisada no
  contiene tipología jerárquica, reporte voluntario de error, liderazgo
  autoritario/benévolo ni feedback público/privado. `MAPEADO-NO-SATISFACE` para
  R2.1/R2.2/R10.2.
- **UCDP GED** aporta violencia organizada, actores y coordenadas, pero no el
  universo de respuestas colectivas —incluidas las no violentas— requerido por
  R7.4/R7.5. No sube a cola.
- **OECD Trust Survey** es la matriz internacional de ENCOAP, no una segunda
  fuente mexicana independiente para 2023. Puede aportar olas/comparadores bajo
  solicitud, por eso se marca duplicada y no prioritaria.

## Restringidas

- **Mexico Panel Study 2012/ICPSR 35024:** potencial alto para voto,
  clientelismo y violencia en panel, pero ya documentado por BARRIDO-1 y sujeto
  a Restricted Data Use Agreement. `DUPLICADA-DE-FUENTE-CONOCIDA`.
- **NielsenIQ/Kantar:** siguen siendo la puerta propietaria para compra real y
  marca por estrato de R1.4. No apareció una razón material nueva para repetir
  la búsqueda cerrada.
- **OECD public-use microdata:** requiere solicitud y justificación de uso; la
  ENCOAP pública debe abrirse primero.
- **Félix-Brasdefer/rechazos:** hay resultados y algún corpus docente, pero no
  archivo de replicación preservado ni muestra nacional no universitaria.

## Duplicados descartados

- WVS Wave 7, LAPOP, Latinobarómetro, Global Findex y ENNViH/MxFLS ya están
  representados en el catálogo o en rutas vigentes.
- OECD Trust 2023 y ENCOAP 2023 son implementaciones de la misma matriz, no dos
  observaciones independientes.
- Mexico Panel Study 2012 ya está en `universo-puertas-2026-08-08.tsv`.
- ACLED evento detallado sigue siendo la puerta con registro ya conocida; el
  XLSX HDX agregado ya fue abierto y descartado por VERIF-3.

## Búsquedas negativas delimitadas

| necesidad | universo, consultas y mecanismo | intentos/fecha | resultado delimitado y condición no encontrada |
|---|---|---|---|
| R1.3 canal de alta fintech | páginas CNBV ya revisadas, catálogo del proyecto y búsqueda dirigida `customer acquisition/referral fintech Mexico data` | dos mecanismos acumulados (artefacto previo + búsqueda web), 2026-08-06 | `NO-ENCONTRADO-EN-UNIVERSO-DECLARADO`: no se encontró canal de adquisición por operación/cliente; no se afirma inexistencia fuera de regulador y documentación pública |
| R1.4 compra/brand premium | catálogo, BARRIDO-1, EMOVI, puertas Nielsen/Kantar y búsqueda académica de panel de compra México | dos clases de acceso, 2026-08-06 | accesible EMOVI sin consumo/marca; panel comercial propietario; ninguna fuente pública revisada une compra real, sustituto funcional y estrato |
| R2.1/R2.2/R10.2 organización | ECCO ya abierto, WBES México 2023, ENAPROCE/ENESTYC previas y búsquedas `leadership hierarchy error reporting performance Mexico dataset` | dos intentos por puerta nueva, 2026-08-06 | accesible pero sin reactivo: desempeño existe separado de jerarquía/reporte/feedback; no se encontró misma muestra con tipología requerida |
| R9.1 enlace acceso-conducta | CLUES/SINERHIAS previos, ENSANUT y nueva infraestructura IMSS-BIENESTAR | dos familias administrativas, 2026-08-06 | reactivo/desenlace viven en instrumentos distintos; no se encontró llave pública persona/hogar↔establecimiento consultado |
| sens_estatus | GPS, ISSP Social Inequality 2019, WVS conocido; búsqueda por status comparison/social inequality Mexico microdata | dos repositorios, 2026-08-06 | ISSP 2019 final no incluye México; GPS no mide comparación de estatus; ADR-54 no se reabre |
| R10.1 rechazo indirecto | repositorios OSF/Harvard, corpus IU y publicaciones Félix-Brasdefer; términos `Mexico refusal speech act dataset replication` | dos búsquedas, 2026-08-06 | estudio accesible parcialmente, sin archivo replicable ni muestra mexicana no universitaria superior/inferior pareada |
| panel crédito+horizonte | repositorios académicos ya barridos y GPS/ECF nuevos | dos fuentes nuevas contrastadas, 2026-08-06 | GPS es transversal y ECF no documenta panel; no se encontró panel adicional a ENNViH que coobserve preferencia temporal y desenlace crediticio |

## Reservas y regla de parada

- No se descargó documento ni microdato; la evidencia revisada fue HTML/PDF
  indexado por páginas primarias y artefactos locales existentes.
- No se atribuye texto literal donde solo se leyó cobertura temática. Esas
  filas dicen expresamente “pendiente de abrir”.
- GDELT y Mass Mobilization dependen de noticias; cobertura y deduplicación son
  parte del diseño, no detalles cosméticos.
- ENCOAP 2023 es nacional urbano, no representa población rural.
- La búsqueda se detiene porque cada grupo material recibió al menos una ruta
  dirigida, hay una cola de diez acciones y el refinamiento siguiente sería
  abrir documentación o rastrear portales de menor impacto.

## Recomendación al checkpoint

- **A · abrir ahora:** Banxico Competencias Financieras, ISSP Redes 2017, ISSP
  Familia 2012, CSES México 2018, Mass Mobilization, ENCOAP y GPS.
- **B · mantener en espera:** GDELT después de Mass Mobilization;
  IMSS-BIENESTAR para una medición futura; CNGMD como contexto municipal.
- **C · descartar para el proyecto por ahora:** WBES para R2.1/R2.2/R10.2,
  UCDP para el universo literal R7.4/R7.5 e ISSP 2019 para estatus mexicano.
- **D · requiere decisión de mesa:** solicitar OECD/ICPSR restringidos; decidir
  si R7.5 puede acotarse a violencia organizada; adjudicar si ISSP resuelve
  simultáneamente actitud/conducta/población/forma para familismo.
