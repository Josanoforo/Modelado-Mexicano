# ASTRA6-C1-VALIDACION-LOTE1-1 · Primeros recálculos independientes y comparación de nueve paquetes

Tanda2 · preparación 26/sep/2026 CDMX · base `4541b9f7e884b280e08014bf1f384fe0d1b7cd82`.
Entorno: **CAJA; orquestador NO CIEGO y validadores NUEVOS aislados**. Continuación de misión aprobada; no nueva adopción.

## 1 · OBJETIVO Y HECHO

Producir reconstrucciones independientes reales y dictámenes de comparación para los nueve paquetes disponibles de #1166 (3371 estimadores al corte histórico). El resultado es evidencia numérica nueva; probar el lanzador no cuenta como validar. Completar todos los paquetes ejecutables de este lote, sin esperar a los otros 59.

Esta sesión recibe contexto conocido y por ello SOLO orquesta, recibe hashes y compara. No puede convertirse en el calculador ciego ni pasar su contexto a un subagente como sustituto de una sesión limpia.

**Hecho verificable:** Verificador propio de lote: para cada comparación exige paquete hash previo, salida congelada recibida, esperados revelados después y correspondencia completa de identidades; detecta duplicados y estados sin evidencia. Evidencia del lanzamiento real, no solo prueba sintética. Un límite de acceso deja la fila pendiente y una receta ejecutable; jamás COINCIDE por defecto.

## 2 · FIRMAS DE MESA

**Firma literal de Jonás, 26/sep/2026, 12:07:56, America/Mexico_City: «Acordado».** Responde a la ADENDA-1 adjunta después de que Astra aceptó sus precisiones. Activa la misión y la adenda; no constituye adopción anticipada de resultados ni permiso de abrir reservas. La cabecera de la adenda se conserva como documento recibido, aunque su condición de aprobación ya quedó satisfecha por esta firma.

Precedencia: esta firma y ADENDA-1; misión original en lo no modificado; instrucciones vigentes y cláusula de autonomía. El presente encargo concreta el lote bajo la autonomía de orden, agrupación y profundidad. Antes de asentar la firma, buscar si Claude u otro acto ya la incorporó: citar el asiento existente y evitar duplicarlo. El encargo conserva esta evidencia aunque el trámite global lo haga otro acto.


## 3 · PREMISAS ETIQUETADAS

[LEÍDO EN MAIN] #1166 dejó 9 paquetes listos, 59 incompletos y todos los estimadores NO-EVALUADO. Corte C1: 4f125e709d3b3830078fe749c82068b3d55e6e70, catálogo v1.1, 36143 estimadores. No se sustituye por v1.2 silenciosamente.
[LEÍDO] #1168 cambió catálogo y vetos; al inicio cotejar vigencia por identidad. Una validación de un objeto histórico no rehabilita una fila vetada ni equivale a validar el catálogo actual.
[NO EJECUTADO AQUÍ] No se lanzó validador desde esta revisión; la disponibilidad de CAJA debe comprobarla el ejecutor.

## 4 · YA HECHO / YA DECIDIDO

[CONSULTADO EN GITHUB] Base de esta tanda: main `4541b9f7e884b280e08014bf1f384fe0d1b7cd82`. #1166 preparó C1 y archivó los seis encargos iniciales. #1170 ENVIPE, #1171 SOCIAL, #1172 ENCIG, #1173 CONSUMO-FAMILIA y #1174 ENIF están fusionados. #1178 contiene recibos con observaciones sobre HEAD anteriores, no una certificación del árbol actual. Este encargo continúa lo fusionado; no vuelve a archivar ni ejecutar la primera tanda.

Arrancar desde main actual, leer AGENTS.md aplicable, canon/MEMORIA-OPERATIVA.md y gobierno/instrucciones-proyecto-v2_16.md. Plantilla vigente encontrada: v2.1. Reportar ruta absoluta de worktree, rama, HEAD y estado. Buscar por objeto en encargos/CONSUMIDO, PR y firmas para no repetir un sucesor ya ejecutado. Fijar corte del lote, documentar solo discrepancias materiales. Si el repo avanzó, consumir lo ya resuelto y ejecutar la brecha.

No volcar derivados: usar tools/consulta.py y lecturas por identidad. Las sesiones concurrentes no escriben el trabajo de otras; entradas compartidas son de solo lectura. En los lotes de tres piezas de reports, cumplir la división por pieza de las instrucciones CLI con perímetros propios; la sesión responsable integra.

## 5 · PIEZAS

### P1 · Separación efectiva y primer lanzamiento

Leer `forense/validacion-independiente/catalogo-1/lanzamientos.md`, `lotes.json` y los scripts existentes. Empezar por ENDIREH 2021 comunitaria, después los ocho restantes. Reutilizar materializador, lanzador y comparador, sin rehacer la preparación.

Por paquete: verificar identidad y disponibilidad; revisar que las entradas no filtran resultados, código productor, comentarios con valores, tablas de salida ni ejemplos con objetivos. Registrar SHA-256 antes de entrega. Materializar en un directorio nuevo fuera del clon con raw mínimo autorizado; ejecutar la prueba de separación del lanzador y luego su modo real. El validador solo ve /entrada, /raw y /work, instrucciones mínimas, dependencias genéricas y documentos autorizados. No recibe este encargo, sus adjuntos, recibos, conversación, catálogo con esperados ni historial. No se hereda historial, memoria, skills del proyecto ni acceso al clon. Si la separación falla, no llamar ciego al resultado; conservarlo aparte como REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA.

### P2 · Reconstrucción congelada antes de revelar

Cada sesión nueva escribe su propio cálculo desde spec humana, cuestionario y FD. No usa helpers del productor ni completa métodos consultando el esperado. Congela código, estimadores, intervalos cuando se puedan reconstruir, estado y explicación en su salida. El orquestador recibe y registra hash/commit y recibo del paquete antes de cargar los esperados. Si una spec es insuficiente, documentar exactamente la ambigüedad sin adivinar ni revelar el productor para corregir el primer intento. Un intento posterior es otro objeto, no una validación ciega original retroactiva.

### P3 · Comparación y efecto sustantivo

Tras congelación ejecutar el comparador existente con el hash recibido. Mantener tolerancias previas; separar COINCIDE, DISCREPA, NO-RECALCULABLE-DESDE-SPEC, BLOQUEADO-POR-ACCESO y NO-EVALUADO. No equiparar discrepancia de intervalo aleatorio a diferencia del punto ni ajustar tolerancias después de verla. Investigar discrepancias después de preservar el primer resultado; identificar efectos sobre conclusiones/consumidores, sin corregir el sello original.

### P4 · Entrega de lote

Tabla por identidad de estimador y agregación por causa; numerador y denominador calculados. Informar cobertura sobre 3371 y sobre 36143 por separado, con estados pendientes explícitos. No anunciar cierre de C1, ni validez conceptual por coincidencia aritmética. Adjuntar receta exacta de repetición, recibos de entrega y orden temporal, y hoja corta de discrepancias que cambien resultados. No copiar raw ni credenciales al repo.

Paquetes exactos:
- `endireh-pisos-2011-modulos-0001` · 1894 estimadores · contenedor SHA-256 `79f5b09f44a638c493eef6c74b045d5dd392db79bcf92bfbe5562aae389dca88`.
- `endireh-pisos-2021-ayuda-0001` · 117 estimadores · contenedor SHA-256 `d806cb4493fc3bfc6c233824d124e318bdf1df6d3e90e7a50c2600ab707a5aee`.
- `endireh-pisos-2021-comunitaria-0001` · 100 estimadores · contenedor SHA-256 `9261eeb9b8ca7e95f66ee57b271f53e9fe6a08feff85377306126025a5e04d0b`.
- `endireh-pisos-2021-decisiones-0001` · 138 estimadores · contenedor SHA-256 `b82032c54922e476a80e4abe3ec3f949f6e4d342a56715d83895efdfc31131dc`.
- `endireh-pisos-2021-discriminacion-0001` · 286 estimadores · contenedor SHA-256 `162dc454c8958b31111e8fdb3c1f29ecb92643ed54341d83406dd9d79ed1f0fe`.
- `endireh-pisos-2021-escolar-0001` · 96 estimadores · contenedor SHA-256 `5e33677ef0904bcca544f450cdbbe6969f0884f86f606944cf3429ddd4d1be7a`.
- `endireh-pisos-2021-familiar-0001` · 50 estimadores · contenedor SHA-256 `80fd91b91fe15c9533bc16e8aed8a5f528aab4d075d44673e64ee4a01853e9d8`.
- `endireh-pisos-2021-laboral-0001` · 100 estimadores · contenedor SHA-256 `c56fd015b88af8659d19e8f771a20bc81839500d51e28d1c5efd08b2a9fa6c6f`.
- `endireh-pisos-2021-nofisica-bc-0001` · 590 estimadores · contenedor SHA-256 `37e0d9f4c235d915557f635c2ac9409e9cbf87d97d115ff4362589641ba304d9`.

## 6 · LATITUD

Rige la cláusula de autonomía v1.0 embebida verbatim. Resolver nombres, rutas, organización y obstáculos reversibles; declarar interpretación sin preguntar por trámite ya autorizado. Redactar propuestas faltantes como PROPUESTO-POR-EJECUTOR. Una propuesta no constituye adopción ni permiso de modificar un procedimiento congelado.

Auditoría/control ~20% del esfuerzo salvo riesgo de resultado material. No convertir este encargo en reparación de CI, sincronización general o inventario decorativo. Una prueba nueva solo si protege un error real/material del objetivo. Avanzar sustancia y dejar una decisión o artefacto utilizable.

## 7 · PAROS Y CONTINUIDAD

Parar solo la pieza que exija reserva no autorizada, sello reescrito, adopción sin firma de contenido, contador a mano, procedimiento congelado alterado o entorno indebido. No pedir otra vez permiso para decisiones reversibles cubiertas. Entregar las demás piezas y una propuesta concreta para el impedimento. No rebajar el Hecho; distinguir qué quedó ejecutado y qué no.

## 8 · GATES MATERIALES

Acceso autorizado por campo y ola; aislamiento antes del lanzamiento; hash antes de entrega; congelación antes de comparación. No esperar a C2/C3 ni completar 59 paquetes para empezar estos nueve. La integración de estados al universo histórico es posterior y no modifica su denominador.

## 9 · PERÍMETRO

Escritura: `forense/validacion-independiente/catalogo-1-ejecucion-lote1/` nuevo, evidencia y scripts auxiliares propios si imprescindibles. Leer sin modificar `catalogo-1/` y `tools/validacion/astra6_catalogo/`. Los nueve paquetes originales quedan congelados. No escribir universo.tsv, lotes.json, preparacion ni registro global desde esta rama; entregar resultados en tabla propia para integración por identidad. La sesión 02 escribe en otra raíz. No modificar productores, sellos, datos, decisiones ni catálogo.

## 10 · CIERRE Y RECIBO

Una sesión responsable, un worktree y un PR por encargo. Archivar este nuevo cuerpo una vez según /acto y conservar su hash; buscar primero si ya existe. La misión aprobada habilita ejecución, commits, push y PR propio; no fusión, autoaprobación, mensajes externos ni adopción de resultados. No duplicar firma de la misión.

Sobre corte final con main incorporado, ejecutar verificaciones propias y el gate pertinente del repo; no usar CI verde como prueba sustantiva. No reparar fallos heredados ajenos. Entregar nota con resultado, decisión que permite, cobertura real y pendientes, separando EJECUTADO/LEÍDO/PROPUESTO. Hoja de firma concreta si hace falta, con opción recomendada.

Preparar recibo-para-claude.md local con objetos, hashes, comandos y reservas; solicitarlo por circuito de mesa en el PR, sin enviar mensajes externos. No afirmar revisión independiente obtenida. Preservar históricos y cuerpos sellados: sucesores/adendas, sin borrar ni sobrescribir testimonios. Los registros comunes exigidos se añaden por identidades propias y no se renumeran; integrar conflictos conservando actos ajenos.

## Adjuntos embebidos · preservar bytes y verificar antes de usar

Estos adjuntos contienen contexto de dirección y resultados conocidos. **Nunca se entregan a una sesión de recálculo ciego de C1.** Solo se usan en preparación, comparación, C2 y C3.

Extracción: bytes UTF-8 entre la línea BEGIN y la línea END, conservando el salto final inmediatamente anterior a END. Los delimitadores no forman parte del archivo. No copiar desde una vista renderizada. Los SHA-256 son:

- `MISION-ASTRA-6-integridad-y-frontera.md`: `ecd8cf1b417bbb1c70c8b5c42c05e2f01270d20a77f4c627cc67442ce53c754e`.
- `MISION-ASTRA-6-ADENDA-1.md`: `6d678178bf90ef60a20ec240b91343cd4eab167327de4c3ac5784db84967f182`.
- `CLAUSULA-AUTONOMIA-v1_0.md`: `3fbc487684b77b7f63d04392089abd51839c22daccd26ecab3c7d0c72f0f6b32`.

<!-- BEGIN MISION-ASTRA-6-integridad-y-frontera.md -->
# MISION-ASTRA-6 · INTEGRIDAD Y FRONTERA: validar a ciegas lo que el programa ya afirma, sellar hoy lo que se probará en 2027, y reescribir los 31 reports contra lo medido
**Dirección (Claude), 26/sep/2026 · main `34949751` (re-deriva) · para Astra (decide el cómo, dictamina, firma recibos) y Codex (ejecuta en CAJA/NUBE hasta cerrar) · MODO AUTÓNOMO-AMPLIO (cláusula v1.0 + amplitud de mandato del 26/sep: orden, agrupación y profundidad los decide la sesión; una hoja de firmas al cierre de cada carril) · sin retadores, pilotos ni duelos (regla 6) · sin CI, tablero ni derivados · todo por recibo.**

Tres carriles. Cada uno es grande a propósito y termina en algo que un lector usa.

---

## C1 · VALIDACIÓN INDEPENDIENTE DEL CATÁLOGO (E.2, segunda pregunta): ¿lo adoptado se reproduce desde la spec humana y el cuestionario, sin leer el código?

**Objetivo.** El programa adoptó 136 filas (`data/corrida0/decisiones.tsv`) que sostienen el catálogo v1.1/v1.2 y la tabla de piso del reto. E.2 hace tres preguntas que no se colapsan: ¿se reproduce? (replay: sí, `verify`) · **¿pasó validación independiente?** · ¿se adopta? La segunda solo la han pasado los pilotos (#970: 35/35 COINCIDE) y el lote ENIF. Este carril la contesta para **todo lo adoptado**: recalcular cada estimador **desde la spec humana, el cuestionario y el descriptor de archivos, sin abrir `medidor.py` ni `resultados.json`**, con código propio, commitear los números antes de abrir los sellados (E.2, orden por sello), y comparar: COINCIDE (dentro de la tolerancia declarada en el RESULT) · DISCREPA (con la diferencia y la causa probable: ponderador, universo, tratamiento de NS/NR, recorte) · NO-RECALCULABLE (la spec no basta — **ese es un hallazgo de D-15**, no un fallo tuyo).

**Antecedentes.** `VALIDACION-INDEPENDIENTE-PILOTOS-1` (#970, 35/35), `-LOTE-1` (#…), `-2` (15/sep), `-PARAMETROS-ACTIVOS` (11/sep): patrón y forma. E.2: «la validación independiente recalcula desde la spec humana, el cuestionario y el descriptor, sin leer el código que produjo la cifra, y commitea sus números antes de abrir los sellados». D-15: «una spec humana debe bastar para recalcular sin leer el código; si no basta, ese es el hallazgo».

**Perímetro.** Propio: `forense/validacion-independiente/catalogo-1/` (specs leídas, código propio en `tools/validacion/`, números commiteados con sello de tiempo interno antes de comparar, tabla RESULT × COINCIDE/DISCREPA/NO-RECALCULABLE), `forense/replay-evidencia.tsv` (asiento `validacion_independiente` por RESULT), NC por DISCREPA y por NO-RECALCULABLE (a la spec, no al RESULT), nota. **Ajeno**: `medidor.py` y `resultados.json` de cualquier CALC hasta el commit de tus números (regla ciega, verificable por historial), `decisiones.tsv`, catálogo.

**Datos autorizados.** Microdato de olas abiertas desde CAJA, por id del manifiesto; cuestionarios y FD desde nube. Nada reservado.

**Amplitud.** Orden y muestreo: tuyos (recomendación: todo lo adoptado; si el tiempo no alcanza, muestra estratificada por instrumento con semilla declarada y cobertura reportada). Una DISCREPA no se «arregla»: se documenta; corregir un sello es acto de otro.

**Criterio de terminado.** Tabla completa con 0 RESULT sin estado; `validacion_independiente` asentada por RESULT; NC por cada spec que no bastó (D-15) y por cada DISCREPA; una línea de producto: «de N estimadores adoptados, M coinciden, K discrepan (lista), J no son recalculables desde su spec». Hoja de firmas: qué DISCREPA propone retirar de la tabla de piso hasta corregir.

---

## C2 · FAMILIAS 2027, DE PRE-REGISTRO A PAQUETE EJECUTABLE Y SELLADO HOY: que cuando INEGI publique cada ola solo falte el COMMIT-3

**Objetivo.** U4 dejó seis familias con spec humana y hoja para mesa (ENIF-AHORRO-FORMAL, ENIF-HORIZONTE-AHORRO, ENCIG-PAGO-DIGITAL, ENCIG-SOLICITUD-MORDIDA, ENVIPE-DENUNCIA-U4, ENVIPE-EVASION-NORMA; `forense/analisis/familias-2027/`, `forense/prereg-caja/FAMILIA-2027-*`). Falta lo que las vuelve prueba de verdad: por familia, **COMMIT-1 completo** (D-22: `spec.yaml`, medidor congelado que lee la ola futura con guardia de una sola variable de agrupación, auditoría automática del código, prueba por mutación, preflight VERDE sobre sintético y sobre oro de la ola anterior, ids nulos declarados, ningún hash sobre archivo vivo), **COMMIT-2** con las emisiones del piso selladas (y de a lo sumo **un retador externo tuyo por familia, solo si crees que es estructuralmente distinto** — si no, ninguno, y se dice), y **atestación externa** de los sellos (el manifiesto de sellos y OpenTimestamps que mesa activa este fin de semana: cada COMMIT-1/2 de familia entra al siguiente manifiesto). Más: **calendario INEGI citado** por familia (fecha de publicación esperada), cálculo de potencia con las réplicas de la última ola, y la regla de activación («cuando `enif_2027` entre al manifiesto nace RESERVADA; solo este código la abre»). Y proponer **hasta cuatro familias nuevas** sobre instrumentos que hoy sí tenemos serie y no tenían (ENSU trimestral por ciudad; ENOE trimestral; ENSANUT; MOCIBA), con la misma forma, para firma de mesa.

**Antecedentes.** E.6 (tres commits, orden del diff = sello, guardia, mutación, nada en scratch), D-22, B-bis (vocabulario cerrado antes de ver el dato; qué pasa si el falsador no refuta), la comparación primaria de v2.16 §4 (diferencia de error medio con IC por réplica; umbral fijado antes), los duelos ENVIPE 2026 y ENIGH 2024 como plantilla de tres commits sobre ola nunca vista.

**Perímetro.** Propio: `forense/prereg-caja/FAMILIA-2027-*` (v1.3+ con `spec.yaml`), `data/corrida0/CALC-FAMILIA-2027-*` (COMMIT-1/2: emisiones selladas, sin R), `tools/familias-2027/`, `forense/analisis/familias-2027/` (calendario, potencia, hoja v2), asientos, nota. **Ajeno**: manifiesto (las olas 2027 entran por `/adquiere` cuando existan), marcador, celdas-D, cualquier ola reservada.

**Datos autorizados.** Olas históricas abiertas para calibrar y para oro de preflight; **ninguna futura, ninguna reservada**. Calendario INEGI desde nube.

**Amplitud.** Qué familia primero, si un retador externo vale la pena, cómo agrupar en PR: tuyo. Una familia cuya potencia sea inútil se dictamina así y se propone retirar.

**Criterio de terminado.** Seis familias con COMMIT-1 y COMMIT-2 sellados y `verify` REPRODUCE sobre el oro de la ola anterior; sellos en el siguiente manifiesto de sellos; hoja de firmas v2 (activación por familia, retadores externos si los hay, familias nuevas propuestas); una frase de producto: «N pruebas prospectivas selladas y atestiguadas, esperando N olas con fecha».

---

## C3 · REPORTS v2: los 31 reports GEN1 reescritos contra lo medido — CONFIRMA / MATIZA / ROMPE por afirmación, cifras por RESULT, evidencia (a)/(b)/(c) y literatura al día

**Objetivo.** Los 31 reports de `corpus/reports/` son GEN1: intuición fuerte, literatura de 2024–25, sin una cifra sellada. Hoy hay 285 corridas, 26 dominios medidos y un mapa con 1 396 afirmaciones dictaminadas. Este carril produce **`corpus/reports-v2/<report>.md`** por cada report: misma estructura del Bloque B (§5 v2.16: resumen ejecutivo con hallazgos sólidos / malinterpretados / útiles · marco · mapa de evidencia por tier · patrones con a favor / en contra / segmentos / causas / riesgo de mala lectura · causas cultura vs estructura vs adaptación · segmentación · comparación internacional · implicaciones · mitos · síntesis · reglas SI-ENTONCES con tier y falsador), donde **cada afirmación del v1 lleva su dictamen** (CONFIRMA con RESULT; MATIZA con RESULT y en qué; ROMPE con RESULT; SIN-CIFRA con el dictamen del mapa: no medible por diseño / con adquisición / no construible) y cada cifra es un `RESULT-*`. Literatura: actualización 2025–26 por dominio con etiqueta (a) primaria en México / (b) diáspora / (c) marco importado, y crítica a Hofstede/GLOBE/WVS como marcos, no como hechos. Módulo de auditoría de rigor extremo completo al final de cada uno, con las preguntas [v2.16]. Los cinco dominios no medibles por diseño (humor, sanción social, emociones morales, duelo ambiguo; genética por firewall) se reescriben igual, como narrativa con tier y sin cifra, diciendo por qué.

**Antecedentes.** §3 y §5 de v2.16; el catálogo v1.1/v1.2 (reglas SI-ENTONCES por dominio); «Dónde sí cambió el mexicano»; el informe v1.3/v1.4; el mapa v1.1; el informe de competencia (dónde ganan los otros; no prometer cambios entre olas).

**Perímetro.** Propio: `corpus/reports-v2/` (31 archivos + índice), `forense/analisis/reports-v2/` (tabla afirmación × dictamen × RESULT por report, derivada por comando desde el mapa y `resultados.json`), test: 0 cifras sin RESULT en `reports-v2/`, nota por lote. **Ajeno**: `corpus/reports/` (v1 intacto, E.1), catálogo, mapa (se citan), CALC.

**Datos autorizados.** Solo RESULT sellados (`cuenta_gen2: SI`), el mapa y la literatura pública (con URL y fecha; sin reproducir texto: paráfrasis, una cita corta por fuente como máximo).

**Amplitud.** Orden de reports, lotes por PR, profundidad de literatura: tuyos. Sugerencia: empezar por los dominios con más RESULT (dinero, seguridad, trámites, trabajo, salud) y cerrar con los no medibles.

**Criterio de terminado.** 31 reports v2 en `main`, índice con la tabla resumen (por report: afirmaciones CONFIRMA / MATIZA / ROMPE / SIN-CIFRA), test de cifras VERDE, módulo de auditoría en cada uno, hoja de firmas: qué reglas SI-ENTONCES nuevas propone al catálogo v1.3 con tier y falsador.

---

## Lo que esta misión NO hace
No construye ni evalúa retadores contra olas vistas (C2 sella emisiones para olas futuras, que es otra cosa y está firmada); no toca CI, tablero, derivados, motor ni manifiesto; no adopta: propone por hoja al cierre de cada carril. Si un carril descubre que su premisa es falsa (una spec que no basta, una familia sin potencia, un report sin dominio medible), decirlo con cita y conteo es el entregable.

## Recibo
Cada PR entra por `GEN2-RECIBO-ASTRA-PRODUCTO-N` (Claude): cifras sin RESULT = DEVOLVER; regla ciega de C1 verificable por historial (`git log -p -S` sobre `medidor.py` antes del commit de tus números); orden de sellos de C2 por diff; literatura de C3 sin texto reproducido. Lo que cumple, mesa lo fusiona.
<!-- END MISION-ASTRA-6-integridad-y-frontera.md -->

<!-- BEGIN MISION-ASTRA-6-ADENDA-1.md -->
# MISION-ASTRA-6 · ADENDA-1 · Acuerdo dirección–Astra sobre la propuesta del 26/sep: se incorporan sus precisiones sin reducir los tres objetivos
**Dirección (Claude), 26/sep/2026 · archivo propio · pendiente de una palabra de mesa («acordado») para que rija; hasta entonces es el texto que dirección propone. Base: `PROPUESTA-ASTRA-6-PARA-CLAUDE-2026-09-26.md` (Astra) y `MISION-ASTRA-6-integridad-y-frontera.md` (`ecd8cf1b417bbb1c`). Donde chocan, manda esta adenda; donde esta adenda calla, manda la misión.**

## Común a los tres carriles (se acepta íntegro)
Universos distintos y no intercambiables (decisión · CALC · RESULT · registro de tabla · afirmación); el denominador de C1 es el catálogo vigente al commit de corte, no las 136 filas de `decisiones.tsv`. Cada entrega declara su commit de corte. Autoridad: Astra diseña y dictamina; Codex ejecuta; Claude recibe; mesa adopta y fusiona. Cuatro preguntas que no se colapsan: coincidencia numérica · validez del estimando · adopción · capacidad predictiva; cada conclusión dice cuál contesta. Sin registros ni formatos nuevos. Un PR por lote, con resultado usable y recibo; nada de PR gigantes.

## C1 · se acepta con dos precisiones
- **Ceguera por separación, no por historial.** La evidencia de ceguera es el paquete de entrada (spec humana, cuestionario, descriptor, insumos autorizados, olas abiertas) entregado a una **sesión nueva sin historial**; el historial de Git acredita el orden de commits y nada más. **Precisión de dirección:** cada paquete se archiva en `forense/validacion-independiente/catalogo-1/paquetes/<lote>/` con su `sha256` **antes** de entregarse, para que el recibo verifique qué recibió la sesión ciega y qué no. Un lote sin separación garantizada se rotula `REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA` y no cuenta como validación ciega.
- **Estados y efectos.** `COINCIDE` · `DISCREPA` · `NO-RECALCULABLE-DESDE-SPEC` (hallazgo D-15) · `BLOQUEADO-POR-ACCESO` · `NO-EVALUADO`; ninguno de los dos últimos se hace pasar por los tres primeros. Cada `DISCREPA` con efecto: cifra · incertidumbre · alcance · conclusión · ninguno material. Coincidir con una spec errónea no valida el estimando: defecto conceptual aparte, con consecuencia. Tolerancias preexistentes; si faltan, se fijan antes de revelar valores y nunca se ajustan. Métodos aleatorios: equivalencia estadística ≠ identidad bit a bit. Muestra intermedia con selección, semilla y cobertura declaradas, sin extrapolar tasa global desde selección por riesgo. **El cierre exige cero `NO-EVALUADO` y cero bloqueos pendientes**; un corte parcial no se anuncia como validación del catálogo.
- **Precisión de dirección:** la sesión de Astra que diseñó C1 ya leyó resultados y así lo declara; no ejecuta recálculos.

## C2 · se acepta íntegro
Familia ≠ ola (reportar ambos conteos y dependencia entre pruebas que compartan muestra). Calendario: fecha oficial cuando exista; si no, ventana esperada con fuente; no inventar fechas 2027. Lector contra esquema explícito probado con sintéticos y ola histórica; cambio de nombre sin cambio de significado = adaptación de cableado documentada; cambio de estimando o cuestionario = detener y dictaminar comparabilidad; **no se promete que solo faltará COMMIT-3**. Potencia con escenarios de cambio temporal y dependencia, supuestos rotulados, cambio mínimo detectable y probabilidad de conclusión informativa; umbrales fijos. Conducto: reproducción de emisiones y ejecución contra oro histórico por separado; ninguna acredita acierto futuro. Retador externo: máximo uno por familia, solo si es hipótesis estructural distinta. Familias nuevas (ENSU, ENOE, ENSANUT, MOCIBA): solo las defendibles, sin llenar cupo. Estados `SELLADO-INTERNAMENTE` · `ENVIADO-A-ATESTACIÓN` · `ATESTIGUADO-EXTERNAMENTE`; el manifiesto de sellos no es atestación; la dependencia de mesa (OTS) se declara sin detener C1 ni C3. Frase de producto: «N familias con emisiones congeladas para M olas futuras; K con atestación externa verificada; fechas confirmadas o ventanas esperadas».

## C3 · se acepta con una precisión
Orden por lotes empezando por confianza, capital social, religiosidad, consumo y familia; afirmaciones materiales ausentes del mapa se registran en la tabla del carril sin alterar el mapa; `SIN-CIFRA` con razón diferenciada (adquisición pendiente · falta de ejecución · instrumento inadecuado · no comparabilidad · restricción del proyecto · imposibilidad justificada); ausencia de evidencia ≠ refutación; distinguir descripción, asociación, predicción e identificación causal y decir qué observación separaría explicaciones rivales; sellados no adoptados como evidencia provisional explícita; cifras externas con fuente primaria, separadas de los RESULT; **el control automático comprueba trazabilidad de afirmaciones cuantitativas, no presencia de dígitos** (años, n bibliográficos y cifras de literatura no exigen RESULT: el test de CIERRE-SEMANAL y el de este carril se alinean a esa regla); literatura 2025–26 dirigida a tesis, con (a)/(b)/(c) y límites de transporte; sin apartados vacíos; tier de frecuencia separado del tier de mecanismo; C3 avanza sin esperar a C1 y corrige solo lo afectado por hallazgos materiales. **Precisión de dirección sobre 3.7:** «no medible por diseño» es un dictamen por afirmación del mapa, no una clasificación de dominios enteros, y el firewall genético es regla del proyecto; Astra puede proponer estimandos para humor, duelo ambiguo o emociones morales, que se reciben como **propuestas para la cola de medición**, no como medición en este carril.

## Organización
La tabla de responsabilidades y secuencia de la propuesta (§6) se adopta tal cual. Perímetros de la misión sin cambio: nada de CI, tablero, derivados, motor, manifiesto ni los objetos de CIERRE-SEMANAL-1 y PRODUCTO-CONSULTA-1; se reutiliza lo fusionado y se cita el corte disponible. Éxito = la lista defendible de afirmaciones que conservamos, las que cambiamos y las pruebas que podrán obligarnos a cambiar de nuevo.
<!-- END MISION-ASTRA-6-ADENDA-1.md -->

<!-- BEGIN CLAUSULA-AUTONOMIA-v1_0.md -->
# CLÁUSULA DE AUTONOMÍA DEL EJECUTOR · v1.0 · 24/sep/2026
**Dirección (Claude) con mandato de mesa («le damos autonomía a la sesión para que corra completo y resuelva; es Opus 5.5»). Se incluye verbatim en §6 de todo encargo desde hoy; entra a la PLANTILLA-ENCARGO v2.2 por el siguiente trámite. Precisa D-19; no lo contradice.**

1. **Discrepancias entre el encargo y el repo las resuelve el ejecutor, no mesa.** Rutas, ramas, nombres de archivo, existencia o ausencia de un objeto, conteos, premisas de estado: se verifica por comando, se corrige, se declara en la nota con la salida cruda, y se sigue. Ninguna de estas es PARO ni pregunta.
2. **Cuando la letra de una firma choca con un hecho verificado pero su intención es clara, el ejecutor sigue con la interpretación que preserva la intención** y la rotula `INTERPRETACIÓN-DECLARADA` en la nota (qué decía, qué se encontró, qué se hizo). Mesa ratifica al fusionar o revierte; no se espera.
3. **Lo que falte para llegar al objetivo y sea redactable, el ejecutor lo redacta** — una regla del motor, un tier, un porqué, un falsador, un esquema de columna, un contrato — rotulado `PROPUESTO-POR-EJECUTOR` en el propio archivo y en la nota, con la fuente que usó (RESULT, report, cuestionario). Mesa lo adopta al fusionar (E.2: el merge del bloque es la adopción) o lo devuelve. Un campo `PENDIENTE-DE-MESA` heredado de una propuesta previa no es PARO: es un campo por redactar.
4. **Bifurcación con opción recomendada = se ejecuta la recomendada.** Se anota la alternativa y por qué no; mesa puede revertir. Solo se pregunta cuando ninguna opción es claramente mejor **y** elegir mal cambiaría una medición o una firma de contenido.
5. **PARO solo por la lista cerrada de D-19, leída estricta:** abrir o derivar dato reservado fuera del código autorizado · borrar, forzar o reescribir algo sellado · mover un contador a mano o adoptar sin firma **de contenido** (un consumidor nuevo del motor se crea rotulado, no se para) · cambiar un procedimiento congelado (umbral, estimando, universo, código sellado) · entorno equivocado. «Objetivo inalcanzable» solo aplica cuando **no existe** ruta legítima; si existe una que requiere redactar o interpretar, es §2–§3, no PARO.
6. **Lo que nunca cambia por autonomía:** ninguna cifra tecleada (todo por RESULT o comando); ningún sello reescrito; ninguna ola reservada abierta; nada fuera del perímetro de §9 sin declararlo; el merge lo da mesa cuando el acto sella corridas o escribe en el motor.
7. **El «Hecho» se mide igual.** La autonomía no rebaja el criterio; lo que no se alcanzó va a NO-CORRIDO con razón y sucesor. Una nota que diga «PARO-PREMISA» por algo que §1–§4 cubren es un defecto del ejecutor, no del encargo.
<!-- END CLAUSULA-AUTONOMIA-v1_0.md -->


## NO-CORRIDO / RESERVAS

C1 global permanece abierto; specs insuficientes, diferencias de punto, IC y publicabilidad documentadas en la tabla sucesora. Sin adopcion, reservas abiertas ni recibo de Claude concedido.

## CONSUMIDO

EJECUTADO por codex/astra6-c1-validacion-lote1-1 en /home/pc0/mm-astra6-c1-validacion-lote1-1. Nueve sesiones efectivas aisladas y comparaciones congeladas; entrega: forense/validacion-independiente/catalogo-1-ejecucion-lote1/informe-lote1.md. Mesa conserva fusion y Claude el recibo.
