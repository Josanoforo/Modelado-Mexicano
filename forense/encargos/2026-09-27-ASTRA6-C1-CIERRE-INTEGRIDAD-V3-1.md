# ASTRA6-C1-CIERRE-INTEGRIDAD-V3-1

Fecha: 27/sep/2026 CDMX · tanda6.
ARCHIVO: 01-ASTRA6-C1-CIERRE-INTEGRIDAD-V3-1.md
Corte: eda5bb9f871a85613cfb4eda7d40dc741e55d0b5.

## 1 · OBJETIVO

Corregir la cadena de integridad y comparación de #1241 hasta entregar un circuito sintético que rechace sustituciones y compare todos los componentes comprometidos. Continuar `codex/astra6-c1-ejecutor-v3-1`, sin abrir otro PR mientras siga abierto. Entorno CAJA/CLI autorizado. No repetir el diagnóstico de namespaces ni ejecutar C1 real.

## 2 · AUTORIDAD Y ARRANQUE

Concreción de MISION-ASTRA-6 y ADENDA-1 aceptadas por Jonás mediante «Acordado» el 26/sep/2026; ambas y la autonomía viajan íntegramente al final. La instrucción de mesa actual pide revisar nuestros PR y dar encargos completos. No se concede permiso adicional para reservas, ejecución real ciega, adopción ni fusión. Citar el asiento vigente de la firma, sin inventar otra.

Declarar worktree absoluto, rama, HEAD y estado. Leer AGENTS.md aplicable, canon/MEMORIA-OPERATIVA.md, este cuerpo íntegro y decisiones específicas del objeto. Verificar avances por identidad de encargo, PR, archivo y CONSUMIDO. Descontar lo ya resuelto en HEAD posterior; no repetir trabajo por inercia. Archivar este cuerpo como adenda/encargo nuevo conforme al régimen, preservando cuerpos anteriores; cierre solo al pie. Un responsable por rama. Subagentes por piezas según AGENTS, sin solapar escrituras.

## 3 · CORTE Y DEPENDENCIAS

Corte consultado: main eda5bb9f871a85613cfb4eda7d40dc741e55d0b5. #1237 archiva tanda5; no la ejecuta. #1240, #1241, #1242 y #1243 están abiertos, no fusionados. Main contiene 17 homónimos v2 de 31 originales; los tres PR editoriales proponen otros diez. No afirmar 27/31 consolidados ni 31/31 por sumar archivos de ramas.

Los sucesores de corrección continúan la rama indicada; si ya fusionó, abrir sucesor desde main, preservar historial y citar el commit efectivamente corregido. Los nuevos editoriales arrancan desde main actual. Las ramas abiertas son propuestas: pueden leerse por SHA para coordinación, nunca importarse como adopciones.

## 4 · HECHOS Y ALCANCE

HEAD revisado #1241: 0b999e5d0be7d2f4c73baea9193c1c0beffa56e4. El proceso aislado, NumPy, exportación extensa y estados v3 representan avance real. El broker de proveedor no existe en esa caja; el cierre lo reconoce. Este encargo no convierte un mock ni un subprocess en una sesión nueva acreditada.

Reproducciones propias del revisor, sobre runtime.py/session_request.py del HEAD: (a) cambiar resultado.json y actualizar bytes/hash en export-manifest.json pasa verify_export; (b) assemble acepta request_sha256='NOT-A-HASH' y un request_id sin solicitud cotejada. No se ejecutó aquí el namespace. Lectura adicional: write_evidence compara punto/estados pero la referencia omite los dos extremos del IC; cambiar solo el IC por otro ordenado no lo haría DISCREPA. La orden LANZAMIENTO describe un sellado externo, pero no incorpora una verificación invocable que lo haga obligatorio antes de comparar.

## 5 · PIEZAS

P1. Incorporar un ancla externa confiable para la congelación. El orquestador fija antes de revelar referencia el digest del manifiesto de exportación y de sus insumos relevantes; el verificador recibe esa identidad esperada desde fuera del directorio mutable. Comprobar también identidad de paquete y manifiesto de entrada esperado. No regenerar el digest esperado desde el mismo objeto que se está verificando. Distinguir validación de consistencia interna de verificación contra sello. Conservar exportaciones anteriores; no reescribir sus sellos.

P2. Vincular solicitud, respuesta y código en el ensamblado. Conservar solicitud canónica o evidencia suficiente para recalcular request_sha256; fijar prompt, request_id, proveedor/modelo cuando exista, herramientas, archivos y sesión. Exigir que assemble verifique esos vínculos y el digest externo del recibo antes de consumir código. Un booleano new_session no demuestra ausencia de memoria; es una atestación cuyo emisor y alcance deben quedar explícitos. Rechazar recibos sustituidos entre dos solicitudes del mismo paquete con prompts diferentes. No inventar firma criptográfica de proveedor si la API no la ofrece.

P3. Implementar congelación→verificación→comparación v3 como ruta invocable, reutilizando semántica y tolerancias existentes de v2. Comparar identidad, conjunto de llaves, unidades, estado de fila, estado IC y TODOS los componentes numéricos pedidos. Fijar tolerancias antes de revelar referencia y reportar resultados por componente. Ausencia de punto/IC se rige por contrato, no es igualdad numérica de null. DENOMINADOR-CERO y NO-IDENTIFICADA conservan significado; coincidencia no acredita validez inferencial. No editar adaptador v2 ni cambiar tolerancias históricas.

P4. Pruebas sintéticas que fallan antes y pasan después: alteración conjunta archivo+manifiesto; sustitución completa de exportación consistente pero de otro paquete; request_sha inválido; replay de respuesta de otra solicitud; alteración de código después del recibo; cambio exclusivo de extremo IC que produce DISCREPA; cambios de llave/unidad/estado que se rechazan o dictaminan con causa. Repetir una prueba positiva completa con NumPy y TSV extenso bajo la frontera real. Los tests de allowlist válida y de aislamiento ya existentes se conservan; no sustituirlos por mocks.

P5. Si hay un proveedor autorizado ya utilizable, concretar el adaptador mínimo de broker y probar sesión nueva únicamente con sintéticos, prompt nuevo, sin historial/memoria/herramientas amplias. No lanzar datos reales. Si no lo hay, entregar la corrección de integridad completa y una sola ficha precisa de provisión: servicio/operación faltante, permisos mínimos, orden invocable y evidencia esperada. Mantener CONTEXTO-NUEVO-ACREDITADO pendiente; no sumar otra prueba mock como solución de esa dependencia. No prolongar el trabajo de infraestructura una vez precisada la capacidad faltante.

P6. Actualizar LANZAMIENTO con comandos realmente implementados y sus parámetros obligatorios. Verificar runtime concreto antes de declarar APTO: namespace probado no certifica imagen OCI ni otra máquina. Si OCI continúa expuesto, conservarlo como NO-VERIFICADO y no atribuirle el inventario del Python del host. Contrato y acceso siguen pendientes de sus firmas. Cierre con matriz de gates y producto corregido, sin adopción.

## 6 · AUTONOMÍA Y PAROS

Resolver premisas vencidas y obstáculos reversibles con evidencia. No dedicar el encargo a CI, fetch/sync, derivados o inventarios generales. Auditoría alrededor del 20% salvo error material. Parar solo la pieza que exija reserva sin permiso, reescribir sello, adoptar sin firma de contenido, alterar procedimiento congelado o usar entorno no permitido. Completar piezas independientes. Una publicación, snippet o resultado de búsqueda público no levanta una reserva: resolver instrumento/ola/módulo y alcance antes de buscar cifras.

No contactar terceros ni enviar mensajes externos. Cuenta/proveedor solo si ya disponible y autorizado; no solicitar ni imprimir claves. No sortear una denegación de aislamiento cambiando de canal o elevando privilegios.

## 7 · VERIFICACIÓN

Controles dirigidos a los defectos y criterios del encargo. Separar EJECUTADO, LEÍDO, PROPUESTO y NO-VERIFICADO. No presentar pruebas de transporte como medición científica, ni cobertura editorial como validación de tesis. Ejecutar el gate pertinente del repo, sin reparar fallos ajenos. Cero incremento de contadores por editorial, pruebas sintéticas o preparación.

## 8 · ENTREGA Y RECIBO

Producto usable, cambios sustantivos explicados, nota de cierre y recibo-para-claude con objetos, hashes, comandos, resultados y límites. Preservar históricos. Hoja de decisión únicamente para decisiones materiales pendientes, con recomendación y objetos concretos. Commits, push y PR propios bajo la autorización de la misión; ninguna fusión propia. Claude recibe por GEN2-RECIBO-ASTRA-PRODUCTO-N y mesa decide fusión/adopción. No afirmar recibo obtenido por haberlo solicitado. Los registros comunes exigidos contienen solo asientos propios.

## 9 · PERÍMETRO

tools/validacion/astra6_ejecutor_v3/ y forense/validacion-independiente/catalogo-1-ejecutor-v3/, más adenda/registro propio. No tocar aislamiento_v2, contenedores v2, resultados científicos, sellos históricos, catálogo, reservas, motor o CI. No abrir medidor/resultados reales para esta prueba.

## 10 · CRITERIO DE TERMINADO

Dos reproducciones del revisor dejan de aceptarse, el IC erróneo deja de coincidir, la ruta positiva completa conserva artefactos y el cierre dice exactamente qué proveedor/contexto se acreditó o qué capacidad falta. Recibo de Claude pendiente explícito. C1 real continúa sin lanzarse.

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

| Qué | Razón | Sucesor |
|---|---|---|
| Sesión real nueva de proveedor y C1 real | El adaptador local conserva y verifica solicitud, recibo y código, pero no hay servicio de broker de proveedor acreditado en esta caja. Faltan además firma del contrato v3 y autorización por paquete. | Ficha única `provision-broker-v3.md`; probar broker solo con sintéticos, obtener firmas y autorización antes de cualquier paquete real. |
| Backend OCI u otra máquina | Solo el namespace de esta caja pasó el circuito sintético; no se ejecutó una imagen OCI fijada por digest. | Repetir canarios, inventario y anclas en ese entorno antes de rotularlo APTO. |

## CONSUMIDO

Continuación del PR #1241 sobre `codex/astra6-c1-ejecutor-v3-1`, HEAD inicial `0b999e5d0be7d2f4c73baea9193c1c0beffa56e4`, main de corte `eda5bb9f871a85613cfb4eda7d40dc741e55d0b5`. Corregidas ancla externa de exportación, vínculo solicitud–recibo–código y comparación de punto e IC bajo congelación. Evidencia sintética y recibo sucesor en `forense/validacion-independiente/catalogo-1-ejecutor-v3/`. No hubo microdato, validación ciega real, adopción, incremento de contador ni fusión propia. Recibo de Claude pendiente.
