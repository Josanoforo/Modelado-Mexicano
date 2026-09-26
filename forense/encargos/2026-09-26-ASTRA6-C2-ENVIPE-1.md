# ENCARGO · ACTO ASTRA6-C2-ENVIPE-1 · dos familias ENVIPE con emisiones congeladas y prueba futura preparada

> ENTORNO: **CAJA para calibración, oro y emisiones; web pública solo para metadatos/calendario**. Derivar entorno al arrancar; toda lectura de registros individuales requiere CAJA y autorización de ola.

**SHA de redacción:** `34949751113358869be981e2220f25d97e8097bd` · **Fecha:** 26/sep/2026 · **Una sesión responsable** (D-17) · **Ejecutor:** Codex en la sesión configurada por mesa, sin imponer cambio de modelo · **MODO:** ABIERTO en diseño no congelado; RÍGIDO desde COMMIT-1 · **CONTADOR:** familias con protocolo y emisión sellada, familias inviables justificadas y atestaciones verificadas; cero adopciones y cero evaluación futura.

Ids ADR/NC/FP: derivados del 0-bis por la herramienta vigente, sin números manuales. Primera tanda ASTRA-6; no sustituye el alcance total de la misión.


Arranque: una sesión responsable, un worktree y un PR. Reportar ruta absoluta, rama, HEAD y estado; leer AGENTS.md aplicable, reglas de lectura de CLAUDE.md, instrucciones vigentes y /acto. Consultar objetos puntuales; no volcar archivos masivos. Usar `tools/consulta.py result <id>` para cifras cuando corresponda. Verificar la disponibilidad de datos antes de declarar ausencia. Cambios mecánicos y rutas se resuelven con la cláusula de autonomía.

Alcance de Git: archivar encargo y cuerpo inmutable en 0-bis; commits, push y PR propio son parte de la entrega prevista por la misión. No fusionar, no forzar historia, no borrar sellos ni ramas ajenas. El recibo técnico de Claude sigue pendiente hasta que exista: redactar `recibo-para-claude.md` no equivale a obtenerlo. Si falla una integración, conservar el trabajo y dar el comando concreto para publicarlo; no convertir la sesión en reparación general de CI.


## 1 · OBJETIVO Y HECHO

Entregar las familias ENVIPE-DENUNCIA-U4, ENVIPE-EVASION-NORMA como paquetes ejecutables, con emisiones históricas congeladas y condiciones de activación verificables. Hoy se preparan dos familias para una ola objetivo; no dos aperturas independientes.

«Hecho»: `python3 tools/familias-2027/envipe/cierre.py --verifica` (verificador propio a entregar) comprueba specs/código/hashes, pruebas de guardias y fronteras, emisión sin R futura, oro histórico y evidencia separada de reproducción, cobertura de las dos familias, calendario con estado y escenarios de potencia. Una familia inviable tiene dictamen fundado y propuesta concreta, no emisión inventada. La atestación externa se acredita solo con comprobante; su dependencia se declara si sigue pendiente.

## 2 · FIRMAS DE MESA

**Firma literal de Jonás, 26/sep/2026, 12:07:56, America/Mexico_City: «Acordado».** Responde a la ADENDA-1 adjunta después de que Astra aceptó sus precisiones. Activa la misión y la adenda; no constituye adopción anticipada de resultados ni permiso de abrir reservas. La cabecera de la adenda se conserva como documento recibido, aunque su condición de aprobación ya quedó satisfecha por esta firma.

Precedencia: esta firma y ADENDA-1; misión original en lo no modificado; instrucciones vigentes y cláusula de autonomía. El presente encargo concreta el lote bajo la autonomía de orden, agrupación y profundidad. Antes de asentar la firma, buscar si Claude u otro acto ya la incorporó: citar el asiento existente y evitar duplicarlo. El encargo conserva esta evidencia aunque el trámite global lo haga otro acto.

## 3 · PREMISAS Y FUENTES

[LEÍDO] `forense/analisis/familias-2027/HOJA-FAMILIAS-2027-para-mesa.md` L5: seis familias condicionales; propone banda ±2 pp, gates por diseño y una apertura por instrumento. Sin retador, ΔMAE y B-bis son NO-APLICABLE. Releer la hoja completa y ambas specs del instrumento.

[LEÍDO] `forense/prereg-caja/FAMILIA-2027-ENVIPE-DENUNCIA-U4-spec-v1_2.md` L19: el primario usa diferencias respecto a un punto fijo, no una diferencia entre dos parámetros poblacionales con incertidumbre histórica propagada. Respetar el objeto y distinguirlo de un análisis de sensibilidad temporal.

[LEÍDO] `forense/analisis/familias-2027/calendario-y-exclusiones.md` L3: la consulta archivada del 23/sep no confirmó fechas futuras. No se hizo una búsqueda nueva de calendario al redactar este encargo; el ejecutor debe hacerla sin abrir resultados reservados.

[EXISTE] Las dos specs v1.2 están en el árbol del corte. [SUPUESTO] Los insumos históricos abiertos necesarios son accesibles en caja; buscar por identidad antes de declarar bloqueo.

Adjuntos originales y cláusula de autonomía están embebidos al final con hash. La plantilla v2.1 y la cláusula se leyeron completas al preparar esta tanda; si una versión posterior está vigente al arrancar, aplicar lo pertinente sin alterar la firma ni ampliar alcance.

## 4 · YA HECHO / YA DECIDIDO

[EJECUTADO] Consulta GitHub en esta preparación: rama main = `34949751113358869be981e2220f25d97e8097bd`. Árbol recursivo: 10046 rutas; 46 rutas coinciden con plantilla/autonomía/familias/ASTRA6/reports-v2/paquetes/CALC futuros. Cero rutas coinciden con `ASTRA6`, `ASTRA-6`, `reports-v2`, `catalogo-1/paquetes` o `CALC-FAMILIA-2027` en ese corte. Es una búsqueda de nombres, no prueba de que no exista trabajo equivalente bajo otro nombre.

[EJECUTADO] Consulta de PR abiertos en esta preparación: un resultado, #1162, ENSU. Su contenido es trabajo en curso; no se incorpora como consolidado. [REPORTADO] El transfer del 26/sep enumera COLA-LOTE-1, COLA-COMPLETA-1, CIERRE-SEMANAL-1 y PRODUCTO-CONSULTA-1 como trabajos en vuelo; no se verificaron aquí sus worktrees.

El ejecutor repite la búsqueda por sus objetos concretos en decisiones, firmas, encargos, CALC, incidencias con sucesor, PR y ramas vivas. Si encuentra trabajo cumplido, lo cita y completa solo la brecha. No reabre decisiones ni repite cálculos ya suficientes. Una versión nueva fusionada se usa si es pertinente; se registra un corte fijo para terminar el lote.

## 5 · PIEZAS

### P1 · Resolver el contrato antes de congelar

Leer ambas specs y las firmas que les correspondan. Distinguir propuesta técnica de regla ya firmada: la aprobación de la misión permite desarrollar el paquete, no cambiar un procedimiento previamente congelado. Mantener versiones previas intactas. Reutilizar el piso por RESULT y hash; no copiar números a mano. Precisar estimando, reactivos, periodo, unidades, exclusiones, diseño, pérdida/contraste y lo que el dictamen sí permite afirmar.

Mantener U4/persona/FAC_ELE separado de evasión/delito/FAC_DEL. Verificar el colapso U1→U4, unión persona-delitos, exclusión de NS/NR y conteos efectivos por estrato/UPM del universo correcto. Los conteos de diseño U1 no se atribuyen a U4. La hoja reporta ausencia de vectores históricos y estratos de UPM única: obtener auxiliares legítimos de la ola abierta, sin reemplazar sellos ni fabricar réplicas desde extremos.

ENVIPE 2026 sigue fuera de la autorización de este lote; no leer microdatos, tabulados o comunicados reservados, aunque otros actos hayan tenido aperturas acotadas. El año de referencia del delito, la edición y la publicación son campos distintos. La prueba futura no se anuncia como validación causal de la etiqueta «evasión de norma».

### P2 · COMMIT-1, diagnósticos históricos autorizados y prueba del lector

Congelar spec humana sucesora, YAML, código material y dependencias, guardias, listas blancas, semillas y tratamiento de falta de comparabilidad. Preparar pruebas sintéticas y de mutación que detecten lectura fuera del perímetro y errores de universo/ponderador. Los auxiliares nuevos para réplicas, soporte y potencia llevan su propia spec previa a lectura de registros históricos; no son reescrituras del productor ni re-mediciones para elegir una variante ganadora.

Probar el conducto con datos sintéticos y oro de olas abiertas. Verificar código y hashes reales, no un wrapper que importe contenido mutable. No prometer funcionamiento contra un descriptor futuro desconocido; dejar un contrato de aceptación y un procedimiento de adaptación puramente nominal, con parada ante cambio sustantivo.

### P3 · Incertidumbre y utilidad de la prueba

Calcular escenarios de potencia con réplicas autorizadas, cambios temporales plausibles y dependencia declarada. Reportar probabilidad de COMPATIBLE/INDETERMINADO/DESVÍO, error relevante, cambio mínimo detectable y sensibilidad a supuestos. Cuando falten series comparables, la parte temporal es escenario, no parámetro estimado.

El protocolo existente compara R con p0 fijo: `d_k = R_k - p0`. No agregar incertidumbre histórica a ese primario sin cambiar explícitamente el objeto antes del sello y respetar firmas. Sí distinguir escenarios adicionales sobre variación temporal. No emparejar olas distintas por el mero índice de réplica. Para resultados de una misma ola, preservar dependencia cuando comparten diseño real. No ajustar banda ni soporte después de ver R ni retirar familias porque una simulación favorece otro umbral.

### P4 · COMMIT-2, emisiones y activación

Sellar emisiones por familia con ids propios `CALC-FAMILIA-2027-ENVIPE-*`, sin R futura. Verificar su reproducción y, por separado, la del oro histórico. En esta primera tanda la recomendación de Astra es **cero retadores externos**: el resultado buscado es una prueba de las emisiones base. Si se identifica una hipótesis estructural distinta con valor claro, documentar propuesta bajo el máximo de uno por familia; no abrir una selección retrospectiva de candidatos ni hacerla dependencia del piso.

Una sola apertura futura para las dos familias. Dejar condiciones que exijan identidad de ola, metadatos comparables, estado de reserva y código autorizado; no modificar manifiesto ni activar una descarga. Ninguna apertura futura se realiza hoy. Los mensajes de producto distinguen familia, ola, fecha de referencia y publicación.

### P5 · Calendario, atestación y hoja de firma

Consultar fuente oficial de calendario y fichas del instrumento, registrar URL/fecha y separar fecha confirmada de ventana esperada. Si no existe anuncio, conservar CONDICIONAL sin bloquear código, emisiones y pruebas.

Entregar inventario exacto de hashes/commits para el siguiente manifiesto de sellos, sin editar el manifiesto ajeno. Estado SELLADO-INTERNAMENTE hasta envío acreditado; ENVIADO-A-ATESTACIÓN hasta comprobante verificable; solo entonces ATESTIGUADO-EXTERNAMENTE. La hoja propone activación, retiro o enmienda material, y explicita qué falta para el COMMIT-3. No afirmar eficacia predictiva antes de evaluarlo.

## 6 · LATITUD

Rige verbatim la cláusula de autonomía embebida al final. Decidir implementación, orden, nombres auxiliares, lotes y obstáculos reversibles. El límite sobre reservas, sellos y procedimientos congelados es estricto. La autonomía para redactar propuestas no autoriza ejecutar una modificación material de un protocolo ya congelado ni sustituye la firma de adopción.

No añadir controles por anomalías cosméticas. Las pruebas propias protegen errores materiales y deben permanecer en el perímetro; no editar workflows ni arreglar fallos heredados ajenos. Si falta red para literatura o calendario, probar una alternativa autorizada; entregar las demás piezas y declarar la brecha exacta, sin simular investigación.

## 7 · PAROS Y CONTINUIDAD

Parar únicamente la pieza afectada si exige abrir una reserva sin autorización, reescribir un sello, adoptar sin firma, mover un contador a mano, modificar un procedimiento congelado o ejecutar microdato en entorno equivocado. Si el objetivo resulta imposible por vías legítimas, entregar el dictamen fundado. Continuar con las demás piezas.

Un nombre distinto, una ruta faltante, un conteo desactualizado o un campo por redactar no son PARO. Enmiendas de cableado siguen D-18 cuando aplique; no convertirlas en permiso para cambiar universos, umbrales o código sellado. Una dependencia externa pendiente queda identificada con receta y sucesor, sin anunciar el lote como completo si falta un criterio sustantivo.

## 8 · COMPUERTAS

Spec y código congelados protegen la apertura de datos del acto. Hashes de insumos y código material protegen el sello. Guardias y autorización de ola protegen reservas. COMMIT-2 anterior a R protege prospectividad. Comparabilidad del futuro cuestionario protege la evaluación. La ausencia de una fecha oficial o de OTS no impide construir ni sellar internamente; impide afirmar fecha confirmada o atestación externa.

## 9 · PERÍMETRO Y CONCURRENCIA

Propio: versiones nuevas de las dos specs `FAMILIA-2027-ENVIPE-*`; `tools/familias-2027/envipe/`; CALC y auxiliares nuevos del instrumento bajo `data/corrida0/`; análisis `forense/analisis/familias-2027/astra6-envipe/`; pruebas propias, asientos reales de replay y cascada de cierre. No cambiar la hoja global de familias ni los archivos de otros instrumentos: entregar hoja local para integración posterior.

Ajeno: sellos históricos, reservados, adquisición/manifiesto, marcador, celdas-D, catálogo, CI, motor, tablero y derivados protegidos. Si publicar una vista exige el canal ajeno, asentar evidencia real y rotular «sellada en disco, no registrada»; no forzar registros de corridas ajenas. Atestación global corresponde a mesa/circuito existente. Familias nuevas ENSU/ENOE/ENSANUT/MOCIBA serán un lote posterior de diseño; no ampliar este lote.

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

| Qué | Razón | Impacto | Sucesor |
|---|---|---|---|
| Atestación externa de COMMIT-1/2 | NO-VERIFICABLE-AQUÍ: sin envío ni comprobante OTS; inventario exacto preparado | Atestaciones verificadas permanece en cero | Mesa / siguiente manifiesto de sellos y OTS |
| Fecha oficial de publicación ENVIPE 2027 | NO-VERIFICABLE-AQUÍ: búsqueda oficial sin confirmación; ventana inferida rotulada | Activación permanece CONDICIONAL | FP-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-01 |
| Apertura, adaptación nominal y evaluación futura COMMIT-3 | DIFERIDO-A:COMMIT-3-ENVIPE-2027; depende de descriptor, comparabilidad y autorización aún inexistentes; no se abre hoy | R futura y adopciones ausentes | COMMIT-3-ENVIPE-2027 / FP-260926-GEN2-ASTRA6-C2-ENVIPE-1-7045-01 |
| Recibo técnico de Claude | NO-VERIFICABLE-AQUÍ: paquete de recibo entregado; revisión independiente no realizada por esta sesión | Recibo técnico no se acredita como obtenido | Claude / GEN2-RECIBO-ASTRA-PRODUCTO-N |

## CONSUMIDO

PR #1170 · rama `codex/astra6-c2-envipe-1` · dos emisiones prospectivas selladas internamente para una ola, oro y escenarios verificados; ninguna evaluación futura ni adopción. Recibo técnico de Claude y OTS pendientes; entrega para circuito de mesa. Cuerpo y sello archivados en #1166 intactos, firma de mesa no duplicada.
