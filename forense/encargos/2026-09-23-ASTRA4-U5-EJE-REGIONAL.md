# ENCARGO ASTRA4-U5 · EJE REGIONAL COMPLETO

23/sep/2026 · Sol 6 · CAJA para medir; preparación sin microdato · rama sugerida `codex/astra4-region-1` · modo ABIERTO dentro del perímetro · adopta: NO.

## Mandato

Ejecuta íntegra la unidad regional de ASTRA-4: pisos por geografía, incertidumbre de diseño, persistencia regional retrospectiva, cobertura y hoja de firma. Tres instrumentos obligatorios: ENVIPE, ENCIG y ENIF. ENIGH es opcional y solo dentro de la parte expresamente abierta; no retrases los tres instrumentos por ampliar el cuarto. No es retador, piloto ni duelo. No lances el sexto frente sugerido al pie del brief.

Base comprobada para preparar este encargo: `origin/main = 7ca31cb4853e9e0b39628b0d7c47c7b0634360b6`. El brief de dirección se adjunta verbatim al final. Sus cifras de inventario y representatividad son premisas que debes comprobar por instrumento/ola/estimando, no garantías por el nombre de la encuesta.

## Dos decisiones explícitas antes de abrir microdato

El brief reserva a mesa la regionalización y la regla de supresión. El siguiente diseño es PROPUESTA de Astra, no firma:

**R1 propuesta:** entidades donde el diseño y el estimando las admitan, más regiones oficiales de diseño de cada instrumento. No imponer 32 estimaciones estatales a un instrumento regional. No crear todavía una nueva partición cultural norte/centro/sur. La opción c de dirección requeriría aprobar además una tabla exhaustiva entidad→macroregión, sin solapamientos ni vacíos; «CDMX-metropolitana» no se obtiene automáticamente de entidades completas y «frontera» tampoco equivale al norte. No construyas esos grupos después de ver resultados. Presenta la tabla si mesa elige c y congélala antes del dato.

**R2 propuesta:** publicar el punto y su IC solo en dominios admitidos, con n no ponderado del denominador ≥200, además de varianza de diseño estimable y requisitos oficiales más estrictos cuando existan. El 200 es un umbral operativo propuesto, no una garantía estadística. Define por conducta la unidad contada; delitos repetidos de un hogar no son hogares independientes. Conserva en el catálogo todas las filas: SUPRIMIDA-N, NO-REPRESENTATIVA, VARIANZA-NO-ESTIMABLE o SIN-COMPARABILIDAD, sin convertirlas a cero. Congela antes del dato el tratamiento de UPM únicas, grados de libertad, réplicas inválidas y extremos; n suficiente no rescata una varianza degenerada. Reporta n efectivo y precisión donde sean calculables, sin imponer un corte posresultado.

Puedes iniciar ya el censo de fuentes, diseño, mapeo de consumidores, código y pruebas sintéticas. Publica la spec propuesta y solicita R1/R2 en la sesión antes de ejecutar el freeze definitivo y abrir microdato. La razón de esta compuerta es el apartado «Decisiones de mesa» del brief, no un requisito añadido. Una confirmación explícita posterior de Jonás satisface la compuerta; no la vuelvas a pedir. Continúa la preparación independiente mientras llega.

## Arranque y reutilización

Actualiza main con fetch; reporta ruta absoluta, rama, HEAD, estado y ramas vivas con conteo. Lee AGENTS.md, instrucciones vigentes, /acto y este encargo completo. Archívalo verbatim con hash según el procedimiento vigente. Revisa reservas y tareas en vuelo por objeto; no escribas en worktrees ajenos.

Busca CALC y ejes geográficos por contenido y consumidores, no solo por nombres REGION/ENTIDAD. Si ya hay una parte regional válida, consúmela y mide el faltante. Selecciona todas las conductas adoptadas/adoptables pertinentes del catálogo U1 o, si aún no existe, de decisiones, specs y celdas-D consolidadas. Fija el universo por commit antes del dato; no esperes a U1 para preparar ni cambies la selección por resultados favorables. Registra exclusiones justificadas y diferencias posteriores de catálogo.

Reutiliza los estimandos, codificaciones, cargadores, infraestructura CALC y métodos existentes. Lee íntegros los métodos de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001` y `CALC-ENCIG-PERSISTENCIA-IC-CALIBRADO-0001`, incluidos sus imports fijados y decisiones; no infieras el método desde el título. `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` se reutiliza por hash, no por copia. Su interfaz supone una Ola y columnas de diseño específicas; demuestra compatibilidad para cada instrumento con adaptador propio. No renombres columnas sin comprobar su significado ni asumas que un algoritmo de réplica es válido para todo diseño. Si es materialmente incompatible, presenta la adaptación necesaria y continúa las piezas compatibles sin alterar el módulo compartido.

## Diseño congelado

1. Tabla de conductas con RESULT consumidor, fuente, olas autorizadas, reactivo/códigos, denominador, factor, estrato, UPM, ámbito geográfico de referencia y límites de representatividad. Distingue entidad de residencia, ocurrencia del delito y realización del trámite. No uses una de ellas como sustituto silencioso de otra. La representatividad estatal de una encuesta no implica precisión garantizada para cada subpoblación y conducta.
2. Cartografía reproducible por códigos y ola, incluida comparabilidad temporal. Agrega regiones mediante totales ponderados del numerador y denominador, nunca media simple de porcentajes estatales. No mezcles regiones oficiales distintas bajo etiquetas iguales. Sin nueva segmentación entidad×edad×sexo: el encargo es región×conducta, salvo que el consumidor ya exija ese universo.
3. Protocolo de diseño: réplicas compartidas entre dominios de una misma ola, con llaves únicas correctas y dependencia hogar/persona/evento preservada. Estimación de dominio sobre el diseño completo, no remuestreo ingenuo de filas filtradas. Declarar método, semilla, cantidad de réplicas y tratamiento de estratos únicos antes de abrir. No suponer que identificadores iguales hacen a dos olas un panel.
4. Persistencia: define piso t−1, IC de muestreo frente a IC predictivo calibrado y regla exacta heredada. Requisito de ≥3 olas es elegibilidad inicial, no garantía de calibración fiable. Fija las transiciones de ajuste y evaluación antes de ejecutar: para evaluar t no ajustes con t. Si solo puedes dar cobertura dentro de la muestra de calibración, etiquétala como tal, sin llamarla validación temporal. Sin historia suficiente: punto/IC de diseño y SIN-HISTORIA-PARA-CALIBRAR; no fabriques intervalo calibrado.
5. Mapa de estabilidad: reporta cobertura y error, sin interpretar «cubre» como equivalencia ni «no cubre» como cambio sostenido demostrado. Congela categorías, comparación y tratamiento de multiplicidad; un mapa de muchos IC marginales no concede significación simultánea. Para IC binomial, explicita eventos, denominador y supuesto de independencia. Para cobertura por conglomerado define qué se agrupa y por qué; entidades, UPM y transiciones no son intercambiables. Réplicas para cobertura dependiente cuando el método lo permita; si no se puede inferir válidamente, muestra conteos descriptivos y límite declarado.
6. Conserva réplicas o suficientes estadísticos autorizados, sin datos individuales, con identidad de columnas, semillas y hash para que posteriores consumidores no necesiten reabrir raw. Incorpora su formato al contrato previo; no dejes solo extremos de IC si la incertidumbre posterior requiere la distribución conjunta. No incorpores identificadores crudos ni pesos individuales al repo.

Una spec humana REGION por instrumento, sidecar, spec ejecutable y medidor efectivo en COMMIT-1. Frase obligatoria: «el primer resultado que produzca este procedimiento es el que se reporta». Código que realmente mide y dependencias fijados, no solo un shim mutable. Pruebas sintéticas antes del freeze: ponderación desigual, dominios pequeños, códigos geográficos repetidos, UPM repetidas entre estratos, denominador cero, extremos y calendario sin filtración futura.

## Datos y ejecución

Solo CAJA y manifiesto: ENVIPE 2011–2025, ENCIG 2011–2025, ENIF 2012–2024 en la medida en que cada ola esté disponible y no reservada. Comprobar la reserva vigente antes de cada apertura. ENIGH ≤2024 únicamente la porción abierta, nunca extrapolar autorización a todo el archivo. Prohibido ENVIPE 2026, ENCO 2025/2026 y cualquier ola nueva reservada. Cuestionarios y diseño públicos sí; tabulados solo como constancia de diseño, no fuente del estimador.

Localiza primero raw y manifiesto compartidos. No redescargues lo existente. Faltante real: solicitud dirigida por id/ola/archivo/geografía y carril adq; licencia, tamaño y hash antes de usar. No declares NO-CONSTRUIBLE por no encontrar un archivo al primer intento.

Tras decisiones y freeze: preflight → run → sello → verify según CLI vigente; COMMIT-2 con resultados completos. cuenta_gen2: SI solo si las reglas vigentes lo permiten, adopta: NO y origen_numerico explícito. Preserva primer resultado y todas las celdas prometidas, incluso suprimidas/no estimables. No ajustes n, regiones o calibración para mejorar el mapa. No reescribas CALC sellados. Por cada replay ejecutado, asiento en `forense/replay-evidencia.tsv` en el mismo PR; comprobar hashes no es replay.

Tres CALC sellados es el mínimo del brief, no autorización para comprimir distintas olas de forma incompatible con la infraestructura. Si el contrato requiere un CALC por ola y otro de calibración, hazlos; las piezas afines se agrupan según D-11. Continúa hasta cubrir los tres instrumentos, no cierres tras el primero.

## Producto y conexión con U1–U4

Genera por comando `canon/eje-regional-v1_0.md` y `.tsv`. Una fila por conducta/geografía/ola/naturaleza de estimación; campo nivel_geografico evita duplicados entre entidad y región. Punto, límites, unidad/escala, universo, n, calidad, generación, temporalidad, estado de publicación, RESULT, CALC y hash; descompón filas si hay varios tipos de IC. Ninguna cifra empírica tecleada. Cada derivación adicional cita fuentes, fórmula y artefacto; no inventes ids RESULT sin CALC.

Cobertura del catálogo: define denominador de celdas esperadas y distingue ausencia de muestra, falta de soporte de diseño, incompatibilidad temporal y supresión. Publica lista completa de estimables/no estimables. Para sesgo urbano/popular, contrasta el universo cubierto y exclusiones geográficas con documentación y datos autorizados; no llames sesgo al mero hecho de que una entidad tenga menos muestra. No infieras condición indígena ni preferencias culturales desde el estado de residencia.

Texto usable por conducta: dónde puede consultarse el dato, qué cambió en las transiciones evaluadas y qué no puede concluirse. No llames a una fila de Nuevo León «Monterrey» ni a Baja California «Tijuana». Tier, fuente mexicana/diáspora/importada cuando corresponda y falsador; distingue estructura/oferta de preferencias. Auditoría de rigor extremo al final y todo análisis histórico rotulado RETROSPECTIVA.

Hoja de firma en `forense/analisis/region/HOJA-EJE-REGIONAL-para-mesa.md`: decisiones R1/R2 asentadas, unidad por conducta comprobada, propuesta de entrada al marcador por instrumento/dominio, reservas de precisión y recomendación. Adopción pendiente hasta mesa. U1 consume tu tabla por commit sin que edites su catálogo; U3/dirección pueden citarla; U4 recibe elegibilidad y precisión histórica sin convertirla automáticamente en familia firmada. Ninguna de estas entregas requiere que edites archivos de los otros frentes.

## Perímetro y cierre

Propio: `canon/eje-regional-v1_0.{md,tsv}` (entregable explícito del brief), `forense/prereg-caja/REGION-*` y sidecars, `data/corrida0/CALC-REGION-*`, `tools/astra/region/**`, `forense/analisis/region/**`, tests regionales propios, replay append y perímetro de cierre permanente /acto (encargo, nota, ADR con raíz, registros, NC/FP y recibo). Ajeno: marcador, celdas-D, milpa, catálogo U1, anexo U3, CI, derivados globales y módulos compartidos fuera del medidor propio.

Autorizados rama, commits, push y PR por unidad o lote coherente; no fusionar, firmar ni publicar adopción. Entrega recibo Codex para Claude con EJECUTADO/LEÍDO/REPORTADO, comandos y cifras; nota abre con contadores antes/después. Baseline y pruebas relevantes con salidas, NO-CORRIDO / RESERVAS y CONSUMIDO con PR. Registro por canal vigente: si la vista aún no incorporó la corrida, declara «sellada en disco, no registrada» y dependencia concreta; nunca edites derivados para simularlo.

Aceptación: al menos tres CALC pertinentes con sello y verify REPRODUCE, universo de conductas cerrado y totalmente dictaminado, tabla/mapa/hoja de firma completos, cero cifras sin trazabilidad, reglas de diseño y retrospectiva respetadas. Tests de sumas ponderadas, integridad referencial, supresión, agregación y ausencia de filtración temporal. Si una premisa es falsa, demuestra alcance y entrega las partes válidas; no afirmes cumplimiento integral mientras falte una pieza material. Obstáculos reversibles se resuelven, no crean encargos de auditoría. La sesión continúa las piezas independientes ante dependencias externas.

---
## Anexo · brief de dirección verbatim

# ASTRA-4 · U5 · EL EJE QUE FALTA: REGIÓN
**Dirección (Claude), 23/sep/2026 · main `7ca31cb4` al redactar (re-deriva) · frente independiente de U1–U4; Astra lo convierte en encargo completo hasta cierre; Codex mide en CAJA.**

## Necesidad pendiente que resuelve (verificada)
La regla §3 de las instrucciones abre con «segmenta por **región**, clase, edad, género, escolaridad, urbanización…». Hoy el modelo no tiene región: `ls data/corrida0 | grep -ic 'REGION\|ENTIDAD\|ESTATAL'` → **0** CALC; los ejes del marcador son sexo, edad, escolaridad, localidad (<15 000 / ≥15 000), formalidad, cuenta, remesas. La mención de "región/entidad" aparece en 50 specs solo como descripción de universo, nunca como eje de estimación. Y el corpus sí lo permite: ENVIPE (15 olas) y ENCIG (8) tienen representatividad **estatal** por diseño; ENIF (5) tiene regiones de diseño; ENIGH representatividad estatal desde 2016. Es la brecha más grande entre lo que las instrucciones exigen y lo que el modelo entrega, y ningún otro frente la toca.

## Consumidor concreto
1. El catálogo (U1 v1.1) y el informe (dirección): hoy toda afirmación es nacional o por localidad; un lector de Monterrey, Oaxaca o Tijuana no encuentra su fila. 2. Cualquier usuario del motor que pregunte «¿en el norte / en Chiapas / en la frontera…?». 3. La tesis de persistencia: hoy está probada por segmento sociodemográfico; si la persistencia se sostiene también por entidad —o si hay entidades donde no—, el informe gana su hallazgo más vendible (dónde el país cambia y dónde no). 4. Mesa, para decidir si «región» entra como eje adoptable del marcador.

## Resultado usable
- **Pisos regionales**: para cada conducta ya adoptada o adoptable (las de ENVIPE, ENCIG y ENIF que U1 cataloga), el estimador de la última ola por entidad (32) y por región agregada, con IC de diseño y —donde haya ≥ 3 olas— **IC calibrado de persistencia regional** (mismo método que #1009 y #1041, aplicado por entidad). Unidad y escala declaradas; persona, hogar, delito y trámite nunca se promedian.
- **Mapa de estabilidad**: por conducta, qué entidades muestran persistencia (el piso t−1 cubre a t) y cuáles no, con IC binomial y por conglomerado (v2.16 §4), rotulado RETROSPECTIVA (olas ya vistas).
- **Cobertura del modelo por región**: qué fracción de las celdas del catálogo son estimables por entidad con n suficiente, y dónde el sesgo urbano-clasemediero del §3 se concentra geográficamente.
- Entrega: `canon/eje-regional-v1_0.{md,tsv}` + CALC sellados + una **hoja de firma** para que mesa decida si región entra al marcador como eje.

## Perímetro propio
`forense/prereg-caja/REGION-*` (spec humana por instrumento, con sidecar), `data/corrida0/CALC-REGION-*`, `tools/astra/region/` (medidor: agregación por entidad con factor y estratos del instrumento; reutiliza `tools/celda_d/marginales_reproduccion.py::replicas_compartidas` por sha, no copia), `forense/analisis/region/`, tests propios, `replay-evidencia.tsv` (append), nota, NC, FP. **Ajeno**: marcador (derivado; si región debe entrar, es firma de mesa y acto de TUBERÍA), celdas-D, `milpa/*.yaml`, catálogo de U1 (U1 cita este eje cuando exista, no antes), CI.

## Datos autorizados
Microdato desde CAJA de olas **no reservadas**: ENVIPE 2011–2025, ENCIG 2011–2025, ENIF 2012–2024, ENIGH ≤ 2024 (la parte abierta por el duelo; lo no abierto sigue reservado). Prohibido: ENVIPE 2026, ENCO 2025/2026, toda ola nueva. Cuestionarios, FD y notas de diseño muestral desde nube. Nada de tabulados de INEGI como fuente de un estimador: solo como constancia para verificar diseño.

## No se solapa con U1–U4
U1 consume estimadores existentes (ninguno regional). U2 releva cifras legacy del motor (ninguna es regional). U3 tabula las seis evaluaciones (todas nacionales/sociodemográficas). U4 diseña familias 2027 (podrá incluir una familia regional *después* de que este frente diga si región es estimable con potencia; U5 le da el insumo, no al revés). Regla 6 intacta: no hay retador, piloto ni duelo; los pisos regionales son estimadores, y su persistencia se mide en retrospectiva.

## Decisiones de mesa que requiere (con recomendación de dirección)
1. **Esquema regional**: (a) 32 entidades + agregado en regiones de diseño de cada instrumento (ENIF usa 6; ENVIPE/ENCIG son estatales) · (b) solo 5–6 regiones grandes (norte, centro-norte, centro, sur, sureste, CDMX-metropolitana) · (c) ambas. Recomendación: **(c)**, con la regla de que una celda entidad×conducta se publica solo si el instrumento la declara representativa y n ≥ el mínimo que la spec fije antes de abrir datos.
2. **Umbral de n mínimo y regla de supresión** fijados en la spec antes de abrir microdato (D-22); no se ajustan con el resultado.
3. **Si región entra al marcador como eje adoptable**: se decide al final con la hoja de firma, viendo cobertura y potencia; hasta entonces los RESULT nacen `adopta: NO`.
4. **Unidad de la conducta por instrumento** cuando ENVIPE mezcla persona/hogar/delito: la spec declara una por conducta y no se promedian.

## Criterio de terminado
`ls -d data/corrida0/CALC-REGION-*` ≥ 3 (uno por instrumento, ENVIPE/ENCIG/ENIF), cada uno con sello, asiento y `verify` REPRODUCE · tabla con una fila por (conducta, entidad/región, ola) y 0 cifras sin `RESULT-*` · mapa de estabilidad con IC binomial por conglomerado y rótulo RETROSPECTIVA · sección de cobertura (celdas estimables / no estimables por n, con la lista) · hoja de firma con las cuatro decisiones y su recomendación · módulo de auditoría de rigor extremo al final del .md (¿qué cambia con foco rural/indígena/popular? aquí es literal: qué entidades) · `check.py --baseline` VERDE.

## Reserva (si mesa quiere un sexto frente después)
«Dónde sí cambió el mexicano»: las series 2011–2025 por segmento que ya existen (ENVIPE 8 CALC, ENCIG 5, ENUT 1, crédito 2) unificadas bajo un vocabulario cerrado por conducta —ESTABLE · CAMBIO-SOSTENIDO · SALTO-DE-INSTRUMENTO · SIN-SERIE— fijado antes de leer; ya hay 3 dictámenes `SALTO-SIN-EXPLICAR` y 6 `TENDENCIA-*` sueltos. Es el complemento narrativo de la tesis. No se lanza junto con U5 porque comparten caja y olas.
