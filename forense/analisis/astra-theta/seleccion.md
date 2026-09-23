# ASTRA-2 · selección después del mapa v1.0

Estado de la primera lectura: **ningún diseño congelable todavía**. Ruta inicialmente prioritaria: `RES-0091`,
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

## Revisión posterior al recibo ENCIG: elección concreta

El recibo #1034 resolvió acceso, no tratamiento. `P7_3` es el canal que
eligió una persona, y el código `05` agrupa servicios de cobertura digital
distinta. Por ello `RES-0091` **no es el primer diseño ejecutable** con los
objetos adquiridos. La geografía que habría que usar es la **del trámite**
(`P7_1/P7_2`) porque la ventanilla se asigna donde se presta el servicio,
no el domicilio (`ENT/MUN` o `CVE_ENT/CVE_MUN`). Su calendario exacto sigue
solicitado, pero no bloquea la elección de otra ruta.

La ruta mejor identificada es el experimento de **Seguro Popular** de King
et al. (2009), [publicación y descripción del tratamiento](https://gking.harvard.edu/files/abs/spi-abs.shtml?page=0%2C0%2C0%2C0%2C1),
[réplica pública DOI 10.7910/DVN/P6NC0M](https://doi.org/10.7910/DVN/P6NC0M).
Se sortearon 74 pares en siete estados y se siguieron 50 pares en seis;
el análisis disponible se refiere a estos últimos. El
tratamiento fue promoción de afiliación **junto con** mejora de instalaciones
y suministro. El código primario de réplica `Eval/define.treatment.R` y
`Eval/control.matches.R` enumera los conglomerados y 50 pares. La
asignación corresponde al **conglomerado de residencia/atención**, no a la
entidad del trámite ENCIG. Los cuestionarios basal y de seguimiento miden
IMSS al inicio, razón de consulta y establecimiento; el seguimiento codifica
farmacia `P10E0501=9` y motivo respiratorio `P10E0401=3`. El basal usa
`P11D0501=9` y `P11D0401=3`. Los codebooks y README se leyeron sin abrir
`ALL.tab`; el corpus local contiene ENSANUT pero no esta réplica.

**Necesidad exacta:** `RES-0087`,
`milpa/procedencia.yaml:asignados_probabilidad:salud.atencion.leve_sin_imss`,
consumidor `asignados_probabilidad[5]` (ver fila AT-21 del mapa), regla
`R4.1` en canon §3.4. El mecanismo documentado es respuesta del lugar de
atención al costo, tiempo y trato de la oferta; el report de salud §Patrón D
registra la prevalencia de farmacia con consultorio en ENSANUT. La
intervención cambia cobertura y oferta sanitaria para personas sin IMSS,
pero **no documenta que las tres dimensiones mejoraron** ni separa sus
efectos. Además, la categoría «farmacia» en 2005–06 no identifica
consultorio anexo frente a compra/automedicación. El desenlace causal que
puede congelarse sin seleccionar sobre síntomas posteriores es el **evento
conjunto por adulto elegible al inicio**: consulta por motivo respiratorio
codificado 3 en farmacia durante el seguimiento. El contrafactual es la
oferta usual en los conglomerados control, en 2005–06; el parámetro es ITT
en puntos porcentuales. No es la probabilidad `P(farmacia | padecimiento
leve-moderado, sin IMSS)` que usa el vector `[0.66,0.24,0.10]` del motor.

**Dictamen de selección:** congelar y medir ese ITT reducido como prueba
causal parcial de `R4.1`, sin instalarlo como θ ni cambiar el vector. Para
convertirlo en magnitud del consumidor, Jonás tendría que **aprobar un
enlace nuevo** entre evento conjunto y probabilidad condicional, sustentado
en incidencia de necesidad, no respuesta de reporte al tratamiento, y
clasificación de consulta en farmacia con consultorio. Alternativa: una
evaluación asignada de acceso con registro de síntomas **antes** de ofrecer
atención y lugar efectivo de consulta, entre no derechohabientes IMSS.
Esta decisión permite un primer efecto reproducible sin fingir que el ITT
identifica el θ completo.

Comparación de rutas tras revisar disponibilidad: `RES-0091` tiene ENCIG
adquirida pero no asignación verificable y mezcla de servicios; `RES-0072`
tiene panel ENNViH y CAL-G3 existente, pero no shock exógeno; `RES-0087`
tiene sorteo documentado y dos olas, pero su microdato de réplica requiere
registro por `codex/adq-*` y el efecto es parcial. La solicitud específica
se añadió en `solicitud-adquisicion.tsv`.

## Guardia del primer diseño, posterior al freeze

Preregistro `ASTRA-THETA-SALUD-OFERTA-spec-v1_0.md` congelado en
`codex/astra-theta-1@c529cdf0` antes de abrir el encabezado de `ALL.tab`.
Adquisición #1037 `codex/adq-astra-theta-salud-1@37cfd059`: seis archivos
del DOI registrados y verificados con hash/tamaño en la raíz compartida.
El diagnóstico `diagnostico-salud-oferta.json` lee **solo encabezados y
hashes**, ninguna fila de desenlace. En `ALL.tab` (647 columnas) faltan
`P11D0401`, `P11D0501`, `P10E0401_T2`, `P10E0501_T2` y los dos códigos
de seguro basal fijados. El código original `Eval/utilization.formerge.R`
lee `tbl_seccion11_vis.dta` y renombra `P11D0501` a `vis.loc`, pero ni esa
tabla ni `vis.loc` están en los seis objetos del depósito. La columna
`P10D04` de `ALL.tab` es mamografía en el codebook basal, no razón de
consulta. `Eval/Insurance.formerge.R` muestra que `healthins_obl` procede
de `P01D1301`, una codificación distinta de la asumida por el codebook;
reemplazarla sin armonización sería cambiar la spec.

**Resultado de la guardia: NO-ESTIMABLE**, no cero numérico. No se ejecuta
`preflight → run → verify` con un desenlace que el archivo no contiene;
no existe `CALC` ni `RESULT` sellado, ni contador GEN2 que sumar. La
imposibilidad es de **este estimando en el único microdato público de
réplica localizado**, no de toda la salud mexicana: los cuestionarios sí
incluyen las preguntas, pero la tabla de análisis pública las omite.
La fila nueva de `solicitud-adquisicion.tsv` identifica exactamente las
tablas fuente, llaves y custodia que mesa necesita conseguir. Alternativa
de mesa si no consigue las tablas: autorizar explícitamente un **nuevo
estimando reducido** para un desenlace que sí aparece en `ALL.tab` (p. ej.
uso ambulatorio total), con preregistro nuevo antes de leer sus valores;
ese efecto no mediría elección de farmacia ni cargaría `RES-0087`.
