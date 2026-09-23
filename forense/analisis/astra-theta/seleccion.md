# ASTRA-2 · selección después del mapa v1.0

Estado: **ningún diseño congelable todavía**. Ruta prioritaria: `RES-0091`,
`milpa/procedencia.yaml:asignados_probabilidad:tramite.mordida.con_registro`.
Su contraste causal es la oferta efectiva de un trámite digital registrable
sobre la solicitud/entrega de mordida entre usuarios elegibles. Eso es un
efecto institucional total sobre una conducta de la regla, no el efecto puro
de confianza institucional. El valor asignado `[0.88, 0.12]` no es su
estimación ni una escala automáticamente comparable. No se ha abierto
microdato en esta sesión ni se ha estimado un desenlace.

## Base y perímetro leídos

- Worktree `/home/pc0/mm-astra-theta-1`, rama `codex/astra-theta-1`, base
  `origin/main` `619748f5e5775f1060a3d8bcea74b11cd579233b`; limpio al abrir.
- Misión adjunta, SHA256 `df2bbebf2312b720010f2a915045abc02da391e7167f5d4dc19fe3a3ac80a6ce`;
  encargo04 individual; `AGENTS.md`; decisiones `reserva:*` en
  `data/corrida0/decisiones.tsv`; `data/manifiesto.yaml` y
  `data/corrida0/relevo-usos-v1_0.tsv`.
- `canon/integrador-psicologia-mexicano.md`, `canon/modelo-decision-v4_0.md`
  §§2.1–2.2/3.3, `milpa/procedencia.yaml`, capa E1,
  `forense/estado-motor-v1_0.md`, `forense/escalas-eleccion-ciega-v1_0.md`,
  registro de llaves, `data/catalogo-fuentes-v2_0.md`, inventarios temáticos
  de trámites, tecnología, seguridad y trabajo, report tecnológico y report
  político. No se usaron
  cruces de ASTRA-1, ENVIPE 2026, ENIGH 2024 ni crédito ENIF 2024.
- El mapa cruza **40** filas exactas de `relevo-usos-v1_0.tsv`, todas
  `SIN-CANDIDATO`: 7 coeficientes ejecutables, 8 asignados, 13
  probabilidades y 12 condicionales. Las **43** entradas E1 son otra unidad;
  el mapa no fuerza 40=43. El conteo vigente de E1 es 24
  `AUSENCIA_DE_FACTO`, 12 `AUSENCIA_DECLARADA`, 7 `ASOCIACION-MEDIDA`, 0
  `ARGUMENTO_EXPLICITO`; difiere del titular histórico de la misión y no
  paraliza la búsqueda.
- Apoyo de adquisición leído sin fusionar: `forense/analisis/astra-theta-adq/recibo-encig-historica.md`
  en `codex/adq-astra-theta-1@1d99b5f0a92eeb873ae50e6b1fe986dce5690cb4`
  (PR #1034). Los ZIP ENCIG 2021/2023 y cuatro documentos ya están en el
  corpus compartido, con ID/hash/tamaño cotejados y términos de INEGI
  leídos. Sus descriptores verifican `ID_TRA`, `ID_PER`, `P7_1/P7_2` (lugar
  del trámite) y `P7_3` (canal). Municipio del trámite no implica
  representatividad municipal; canal usado no es asignación.

## Shortlist, antes de medir desenlaces

| Orden | Llave y mecanismo | Asignación/observación localizada | Razón de decisión |
|---|---|---|---|
| 1 | `RES-0091` · `tramite.mordida.con_registro`: hacer registrable la interacción reduce la oportunidad de mordida; canon §3.3 y report tecnológico/político. | [CDMX anunció en 2019 renovación de licencia y tarjeta de circulación en línea](https://jefaturadegobierno.cdmx.gob.mx/comunicacion/nota/presentan-la-adip-y-la-semovi-la-digitalizacion-de-los-tramites-para-la-renovacion-de-licencia-tipo-y-tarjeta-de-circulacion); [Tabasco permite renovar y pagar en la app](https://tabasco.gob.mx/noticias/presentan-sspc-y-pec-avances-y-beneficios-de-app-licencias-e-infracciones-digitales). ENCIG repite medición de corrupción por trámite y entidad. | Mejor enlace con una regla y fuente potencial de variación. **Pendiente:** calendario de disponibilidad efectiva y cobertura de todos los servicios/celdas de comparación. ENCIG `05` mezcla licencia, verificación, refrendo, placas y otros: [cuestionario 2023](https://www.inegi.org.mx/contenidos/programas/encig/2023/doc/encig23_cuestionario.pdf). No se puede tratar a todo `05` como renovación digital ni elegir controles sin calendario. |
| 2 | `RES-0072` · `G3.horizonte_temporal`: estabilidad del ingreso y horizonte/ahorro; canon §2.1, report tiempo. | ENNViH panel olas 2–3, `CAL-G3` ejercido, enlace lineal para θ en procedencia. | Disponibilidad alta y enlace existente, pero la variación intra-persona de `pr02` no fue asignada; primeras diferencias no eliminan shocks simultáneos. El CAL vigente está rotulado asociación. Falta un shock exógeno enlazable a sujetos/periodos; Progresa apoya dirección pero no aporta por sí solo esa llave a ENNViH. |
| 3 | `RES-0094` · `civico.denuncia.con_seguro`: seguro crea incentivo de denuncia; canon §3.7, report político. | ENVIPE mide denuncia y cobertura en algunas olas. | Seguro se selecciona según ingreso, vehículo, riesgo y lugar. Una regla de seguro en carreteras federales no demuestra cobertura del delito observado ni ofrece por sí sola un corte en el archivo público. Falta llave de asignación antes de preregistro. |

## Por qué no se congela aún `RES-0091`

La unidad de asignación sería entidad×servicio×fecha de operación efectiva;
la unidad observada ENCIG es persona/trámite en ciudades de 100 mil habitantes
o más, con entidad pública. La encuesta 2023 incluye un código `05` que
agrega servicios tratados y no tratados. No hay hoy una tabla verificada de
fechas, servicios, obligatoriedad, canal y volumen por entidad. Los ZIP
históricos 2021/2023 sí son accesibles y sus hashes están verificados por
el recibo del apoyo; **la falta es el calendario de exposición**. Una ley o
anuncio no garantiza uso ni una ventanilla registrable. Además, dos estados
vistos en prensa no son base suficiente para inferencia agrupada estatal;
hay que censar cohortes y controles. Comparar usuarios digitales contra
presenciales introduciría selección. Elegir una ventana después de mirar
tasas de mordida violaría el freeze.

Se requiere la fila `solicitud-adquisicion.tsv` antes de decidir tratamiento,
cohortes y comparación. El primer diseño elegible sería un efecto de **oferta
registrable** en trámites realmente cubiertos, con adopción observada como
verificación de primera etapa. Si el calendario revela suficientes estados,
periodos y servicios comparables, congelar método de DiD escalonado con
comparaciones aún no tratadas, inferencia al nivel entidad y diseño ENCIG;
pretrends/anticipación/composición/cambios simultáneos se fijarán en la spec.
Si solo se encuentra una o dos unidades tratadas, o `05` no permite aislar
exposición, esta ruta queda como **efecto reducido no identificado o
no estimable**, y no se renombra como θ causal.

## Decisión que permitiría la evidencia adicional

Con el calendario y el texto/código de los reactivos, decidir si existe
una spec de `RES-0091` que identifique una magnitud local para la regla.
No hay segundo efecto elegido: los otros renglones son contraste de viabilidad
antes de observar resultados. Si la intervención mide solo disponibilidad
digital y se quisiera cargar como coeficiente de `G1.confianza_institucional`,
eso cambiaría el constructo/enlace y requiere decisión de Jonás; **recomiendo
mantenerlo en `RES-0091`**, y como alternativa conservarlo solo como efecto
institucional reducido, sin destino en el motor.

## Auditoría de rigor extremo

La oferta digital y la capacidad administrativa covarían con ingreso urbano,
infraestructura e incidencia de corrupción. Esos factores pueden explicar
un gradiente que parezca "cultura" o confianza. ENCIG excluye localidades
menores de 100 mil habitantes: ni un efecto válido transporta a México rural
o indígena sin argumento adicional. La menor mordida puede provenir de menos
contacto y trazabilidad, no de una transformación psicológica. Leer una caída
como prueba de que "los mexicanos dejan de corromperse al usar apps" sería
una sobreinterpretación; leer una ausencia de efecto como prueba de que el
registro nunca sirve también lo sería si la cobertura de `05` es baja.

No se corrió `preflight → run → verify`: todavía no existe una spec honesta
con población tratada, fuente de asignación y controles fijados. No hay
`RESULT` ASTRA-THETA, `CALC`, sello, `replay-evidencia.tsv` ni contador GEN2
que atribuir a este mapa.
