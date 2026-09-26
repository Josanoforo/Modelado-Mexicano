# ENCARGO · ACTO ASTRA6-C1-PAQUETES-1 · universo adoptado y paquetes listos para validadores nuevos

> ENTORNO: **CAJA para resolver y preparar insumos locales; no recalcular microdato**. Derivar entorno al arrancar; toda lectura de registros individuales requiere CAJA y autorización de ola.

**SHA de redacción:** `34949751113358869be981e2220f25d97e8097bd` · **Fecha:** 26/sep/2026 · **Una sesión responsable** (D-17) · **Ejecutor:** Codex en la sesión configurada por mesa, sin imponer cambio de modelo · **MODO:** ABIERTO en preparación; paquete congelado antes de entrega · **CONTADOR:** paquetes completos y estimadores cubiertos; cero recálculos y cero adopciones.

Ids ADR/NC/FP: derivados del 0-bis por la herramienta vigente, sin números manuales. Primera tanda ASTRA-6; no sustituye el alcance total de la misión.


Arranque: una sesión responsable, un worktree y un PR. Reportar ruta absoluta, rama, HEAD y estado; leer AGENTS.md aplicable, reglas de lectura de CLAUDE.md, instrucciones vigentes y /acto. Consultar objetos puntuales; no volcar archivos masivos. Usar `tools/consulta.py result <id>` para cifras cuando corresponda. Verificar la disponibilidad de datos antes de declarar ausencia. Cambios mecánicos y rutas se resuelven con la cláusula de autonomía.

Alcance de Git: archivar encargo y cuerpo inmutable en 0-bis; commits, push y PR propio son parte de la entrega prevista por la misión. No fusionar, no forzar historia, no borrar sellos ni ramas ajenas. El recibo técnico de Claude sigue pendiente hasta que exista: redactar `recibo-para-claude.md` no equivale a obtenerlo. Si falla una integración, conservar el trabajo y dar el comando concreto para publicarlo; no convertir la sesión en reparación general de CI.


## 1 · OBJETIVO Y HECHO

Entregar el universo adoptado del catálogo vigente a un corte fijo y todos sus paquetes de validación independientes, preparados para sesiones nuevas. Este encargo es de PREPARACIÓN NO CIEGA; no es la validación ni produce una tasa de coincidencia.

«Hecho»: `python3 tools/validacion/astra6_paquetes.py --verifica` (script propio a entregar) verifica la cobertura exacta del universo, referencias y hashes de paquetes, ubicación de insumos y ausencia de archivos productores/resultados en las entradas; una revisión dirigida comprueba filtraciones textuales. El verificador no pretende demostrar por sí solo independencia cognitiva. Entregar un lanzamiento concreto por lote y el primer lote completamente disponible, además del resto de paquetes o sus faltantes explícitos. No marcar completo el paquete cuyo insumo autorizado no esté accesible.

## 2 · FIRMAS DE MESA

**Firma literal de Jonás, 26/sep/2026, 12:07:56, America/Mexico_City: «Acordado».** Responde a la ADENDA-1 adjunta después de que Astra aceptó sus precisiones. Activa la misión y la adenda; no constituye adopción anticipada de resultados ni permiso de abrir reservas. La cabecera de la adenda se conserva como documento recibido, aunque su condición de aprobación ya quedó satisfecha por esta firma.

Precedencia: esta firma y ADENDA-1; misión original en lo no modificado; instrucciones vigentes y cláusula de autonomía. El presente encargo concreta el lote bajo la autonomía de orden, agrupación y profundidad. Antes de asentar la firma, buscar si Claude u otro acto ya la incorporó: citar el asiento existente y evitar duplicarlo. El encargo conserva esta evidencia aunque el trámite global lo haga otro acto.

## 3 · PREMISAS Y FUENTES

[LEÍDO] ADENDA-1 C1: denominador = catálogo vigente al corte; se exige paquete con SHA antes de entrega, sesión sin historial, estados distintos y cero pendientes para cerrar la validación total.

[LEÍDO] Catálogo v1.1, sección «Cómo leerlo», distingue estimadores dentro de tablas, firmas y origen. No asumir una fila por RESULT ni una decisión por estimador. Releer versión vigente y sus fuentes de adopción al arrancar.

[SUPUESTO] La caja puede resolver los insumos abiertos del catálogo. Si alguno falta, buscar por identidad en manifiesto y ubicaciones autorizadas; documentar BLOQUEADO-POR-ACCESO. No confundirlo con una spec insuficiente.

Adjuntos originales y cláusula de autonomía están embebidos al final con hash. La plantilla v2.1 y la cláusula se leyeron completas al preparar esta tanda; si una versión posterior está vigente al arrancar, aplicar lo pertinente sin alterar la firma ni ampliar alcance.

## 4 · YA HECHO / YA DECIDIDO

[EJECUTADO] Consulta GitHub en esta preparación: rama main = `34949751113358869be981e2220f25d97e8097bd`. Árbol recursivo: 10046 rutas; 46 rutas coinciden con plantilla/autonomía/familias/ASTRA6/reports-v2/paquetes/CALC futuros. Cero rutas coinciden con `ASTRA6`, `ASTRA-6`, `reports-v2`, `catalogo-1/paquetes` o `CALC-FAMILIA-2027` en ese corte. Es una búsqueda de nombres, no prueba de que no exista trabajo equivalente bajo otro nombre.

[EJECUTADO] Consulta de PR abiertos en esta preparación: un resultado, #1162, ENSU. Su contenido es trabajo en curso; no se incorpora como consolidado. [REPORTADO] El transfer del 26/sep enumera COLA-LOTE-1, COLA-COMPLETA-1, CIERRE-SEMANAL-1 y PRODUCTO-CONSULTA-1 como trabajos en vuelo; no se verificaron aquí sus worktrees.

El ejecutor repite la búsqueda por sus objetos concretos en decisiones, firmas, encargos, CALC, incidencias con sucesor, PR y ramas vivas. Si encuentra trabajo cumplido, lo cita y completa solo la brecha. No reabre decisiones ni repite cálculos ya suficientes. Una versión nueva fusionada se usa si es pertinente; se registra un corte fijo para terminar el lote.

## 5 · PIEZAS

### P1 · Universo sin duplicaciones

Fijar commit y versión del catálogo. Resolver sus filas hasta CALC/RESULT/registro de tabla y las decisiones que habilitan su uso, con vetos y sucesores. Separar número de decisiones, CALC, RESULT, estimadores únicos y afirmaciones. Conservar el mapeo entre reutilizaciones. Una discrepancia material entre catálogo y decisiones se muestra; no se arregla alterando el catálogo desde este acto.

### P2 · Partición completa y entradas separadas

Agrupar por familia de cálculo e instrumento, ponderación y universo; partición exhaustiva con prioridad a conclusiones expuestas y métodos sensibles. No muestrear como reemplazo del universo total. Cada paquete incluye spec humana, cuestionarios, FD, identificadores de insumos abiertos, códigos y tolerancias ya documentadas sin valores objetivo, instrucciones de ejecución y ruta autorizada de acceso a esos insumos.

Archivar en `forense/validacion-independiente/catalogo-1/paquetes/<lote>/` antes de entregarlo. No copiar microdatos al repositorio. Especificar acceso al conjunto mínimo de archivos raw abiertos mediante una carpeta/entorno aislado que no exponga el clon completo ni otras reservas. Un symlink dentro de una sesión con acceso libre al repo no basta para afirmar aislamiento; verificar la separación efectiva en el lanzamiento. Si no puede garantizarse, rotular REIMPLEMENTACIÓN-INDEPENDIENTE-NO-CIEGA.

No incluir código productor, resultados, reports, historial del repo, esta conversación, este encargo completo ni adjuntos de dirección en el paquete del validador. No completar una spec leyendo código. Si un documento mezcla método y resultados, conservar el original fuera del paquete y una extracción fiel de método con vínculo de procedencia fuera del alcance del validador; no fabricar método omitido. Revisar ejemplos que filtren valores objetivo. Faltantes materiales se preservan como tales.

### P3 · Lanzamiento y comparación separados

Crear un encargo mínimo por paquete para una sesión NUEVA: únicamente entradas autorizadas, estimandos a reconstruir y cómo congelar código/números antes de revelación. La ejecución debe conservar evidencia de qué paquete recibió. Permitir dependencias estadísticas genéricas, nunca helpers numéricos del productor. Semillas y criterio para métodos aleatorios quedan predeclarados.

Preparar el comparador y la correspondencia con valores esperados en un directorio de preparación no entregado al ciego. El comparador no se ejecuta hasta que el responsable reciba el commit/hash inmutable de la reconstrucción. Usa tolerancias previas y no las afloja. No simular estados COINCIDE con fixtures ni registrar validaciones inexistentes.

### P4 · Cobertura y siguiente lanzamiento

La tabla del universo comienza NO-EVALUADO, con estados previos independientes solo si tienen evidencia suficiente citada y corresponden al mismo objeto vigente. Preparación de paquete no cambia estado a validado. Entregar orden de lotes, entradas disponibles, archivos que se entregarán al validador y orden de revelación al comparador. Incidencias por causas compartidas, sin una NC por cada fila repetida.

La sesión termina cuando deja ejecutable la preparación entera y los lanzamientos; no se transforma ella misma en validador ni reclama cierre de C1. La validación completa es el sucesor por lotes y exige todos los estados finales y cero bloqueos pendientes.

## 6 · LATITUD

Rige verbatim la cláusula de autonomía embebida al final. Decidir implementación, orden, nombres auxiliares, lotes y obstáculos reversibles. El límite sobre reservas, sellos y procedimientos congelados es estricto. La autonomía para redactar propuestas no autoriza ejecutar una modificación material de un protocolo ya congelado ni sustituye la firma de adopción.

No añadir controles por anomalías cosméticas. Las pruebas propias protegen errores materiales y deben permanecer en el perímetro; no editar workflows ni arreglar fallos heredados ajenos. Si falta red para literatura o calendario, probar una alternativa autorizada; entregar las demás piezas y declarar la brecha exacta, sin simular investigación.

## 7 · PAROS Y CONTINUIDAD

Parar únicamente la pieza afectada si exige abrir una reserva sin autorización, reescribir un sello, adoptar sin firma, mover un contador a mano, modificar un procedimiento congelado o ejecutar microdato en entorno equivocado. Si el objetivo resulta imposible por vías legítimas, entregar el dictamen fundado. Continuar con las demás piezas.

Un nombre distinto, una ruta faltante, un conteo desactualizado o un campo por redactar no son PARO. Enmiendas de cableado siguen D-18 cuando aplique; no convertirlas en permiso para cambiar universos, umbrales o código sellado. Una dependencia externa pendiente queda identificada con receta y sucesor, sin anunciar el lote como completo si falta un criterio sustantivo.

## 8 · COMPUERTAS

Paquete sin resultados/código productor y sesión nueva con acceso restringido protegen la independencia del recálculo. Hash del paquete antes de entrega protege identidad de entradas. Commit de números antes de revelar el esperado protege la comparación. Autorización de ola abierta protege acceso a datos. No existe compuerta de «esperar a que termine C2/C3».

## 9 · PERÍMETRO Y CONCURRENCIA

Propio: `forense/validacion-independiente/catalogo-1/` (paquetes, universo, preparación y lanzamientos), `tools/validacion/astra6_paquetes.py`, comparador de preparación bajo `tools/validacion/astra6_catalogo/`, prueba dirigida propia si necesaria y evidencia mínima de cierre. Las copias temporales de datos autorizados viven en el entorno aislado, nunca en Git.

Ajeno: productores, sellos, decisiones, catálogo, mapa, registro de validaciones (hasta que una validación real lo autorice), CI, motor, manifiesto, tableros y derivados protegidos. No tocar `forense/replay-evidencia.tsv` para asentar una preparación como validación. Archivos de otros carriles no se escriben.

Perímetro de cierre: encargo propio y adjuntos archivados, nota, recibo, fragmento L0 y asientos propios según reglas vigentes. Reutilizar mecanismos; no cambiar productores centrales por conveniencia. Nada de ediciones manuales a contadores. Incidencia real fuera de alcance se declara con siguiente acción y se continúa.

## 10 · CIERRE Y RECIBO

Sobre el commit final con main incorporado, ejecutar la verificación propia que figura en §1 y las pruebas dirigidas necesarias. Registrar comando, salida y alcance. Los cambios de main fuera del universo congelado no obligan a ampliar el lote. No dedicar la entrega a CI/sync ni usar verde como sustituto de resultado.

La nota y `recibo-para-claude.md` dicen primero: resultado nuevo, decisión que permite, cobertura real, reservas materiales y siguientes acciones. Cada afirmación de ejecución distingue EJECUTADO/LEÍDO/PROPUESTO. Hoja de firmas breve con recomendación y alternativa; no pedir a mesa que resuelva implementación.

Usar ids derivados del 0-bis y registros existentes para incidencias, propuestas y cascada. No modificar líneas históricas ajenas ni renumerar. El cuerpo del encargo no se rellena ni se cambia; /acto añade al final NO-CORRIDO/RESERVAS y CONSUMIDO cuando corresponda. Adendas posteriores son archivos propios. Abrir el PR del lote y solicitar el recibo mediante el circuito de mesa, sin inventar revisión ni fusionar. No enviar mensajes externos por iniciativa de esta sesión.

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

| qué | por qué | impacto | sucesor |
|---|---|---|---|
| P2 · Partición completa y entradas separadas | DIFERIDO-A:SIN-ASIGNAR: 59 paquetes con faltantes documentales, método mixto, tolerancia ausente o proyección autorizada pendiente; lista exacta en lotes.json y faltantes.json. | 32772 estimadores sin paquete completo; no cambia validación ni adopción. | SIN-ASIGNAR; continuación de preparación descrita en lanzamientos.md |
| Perímetro de cierre · recibo técnico de Claude | DIFERIDO-A:SIN-ASIGNAR: el recibo requiere revisión real por el circuito de mesa. | PR sin recibo; no se declara aceptado ni se fusiona. | SIN-ASIGNAR; GEN2-RECIBO-ASTRA-PRODUCTO-N por asignar en mesa |

## CONSUMIDO

Preparación entregada en PR #1166: universo completo, nueve paquetes disponibles y primer lanzamiento aislado probado; faltantes de los demás paquetes explícitos. No es validación total de C1. Recibo de Claude pendiente; no fusionado.
