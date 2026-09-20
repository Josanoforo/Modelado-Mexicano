ENCARGO · ACTO GEN2-RECIBO-CODEX-6 · CIERRE DEL CARRIL CODEX: RECIBO DE ONCE PR, DIECISÉIS CORRIDAS QUE ESPERAN CONTADOR, CUATRO RAMAS HUÉRFANAS Y EL RECIBO-5 QUE CODEX SE HIZO A SÍ MISMO

CABECERA (D-12) · SHA de redacción 4dedab48; re-deriva · ENTORNO: NUBE; NO caja · una sola sesión, rama propia · compuerta: ninguna · MODELO: Sonnet · CONTADOR: cuenta_gen2 = NO; mueve N_corridas_selladas solo por firma · FP/ADR/NC: deriva al cierre; renumera quien fusione segundo (corre TABLERO-SENAL-1; comparte hallazgos.md). Contexto: mesa retiró a Codex del programa el 19/sep por límite de uso. Este es el último recibo del carril; después la caja vuelve a Claude.

FIRMA DE MESA (propuesta; tu lanzamiento es el sello; sin texto, PARA esa pieza y sigue)

Contador en bloque, condicionado. "Cuentan (cuenta_gen2 = SI) las corridas SELLADA · PENDIENTE-DE-MESA con resultado_replay = REPRODUCE que P2 encuentre limpias de ejecución previa a su spec. Las NO-VERIFICADO no cuentan hasta tener asiento de replay. Las PENDIENTE-DE-CASCADA-DIFERIDA y PENDIENTE-DE-INTEGRACION-SERIAL no se tocan: tienen su propio trámite."

VERIFICACIÓN DE EXISTENCIA (contra 4dedab48)

PR Codex fusionados desde 6f365928: #886, #888, #890, #891, #892, #893, #895, #896, #898, #899, #900 (once). corridas.tsv: 16 SELLADA con cuenta_gen2 pendiente — 12 PENDIENTE-DE-MESA (una de ellas NO-VERIFICADO: CALC-WBES2023-PRECISION-INTERACCIONES-0001), 2 CASCADA-DIFERIDA, 2 INTEGRACION-SERIAL. Dos corridas sucedidas después de correr: CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-0001 (16 RESULT, NO-VERIFICADO) → -v1_1; CALC-ENUT2024-DISTRIBUCION-HORAS-0001 (26 RESULT) → -0002. Ramas presentes además de main: 4, todas codex/*.

PIEZAS

P1 · El recibo-5 lo ejecutó Codex (#895), aunque el encargo decía «carril Claude — si existe codex/*recibo-codex-5*, PARA». Tocó gobernanza, registro-rotulos, no-corrido.tsv, hallazgos.md, firmas-pendientes.tsv, estado-programa-v1_14.md. No lo reviertas. Compáralo pieza por pieza contra ENCARGO-GEN2-RECIBO-CODEX-5-2026-09-19.md (P1–P7): qué cubrió, qué no, y si alguna firma de contador se aplicó sin la verificación de orden que P2 de ese encargo exigía antes. Lo no cubierto se hace aquí. Una línea en hallazgos: tercera vez en un día que un encargo de gobierno corre en el carril equivocado (RECIBO-3, MARCADOR-ADOPCION, RECIBO-5); semilla PARA-v2.15: el ejecutor de un encargo se nombra en la cabecera y /acto lo comprueba — ya es D-17; anota que D-17 atrapó algo, para su falsador a tres meses. P2 · Orden spec → resultado, por git log --reverse, en las 12 PENDIENTE-DE-MESA y en las dos sucedidas tras correr. Para ENSAFI y ENUT-DISTRIBUCION: ¿qué cambió entre la versión que corrió y su sucesora, y el cambio pudo depender de haber visto el resultado? Si sí, la sucesora se marca con reserva (propuesta con reserva, no adjudica) y no cuenta hasta FP de mesa. No se reabre ninguna corrida (E.3). P3 · Firma de contador tras P2. status antes/después con worktree. P4 · Las cuatro ramas. (a) codex/gen2-enadid2023-union-sexo-edad-cli-2: 16 commits propios, cuatro versiones de CALC (-0001 a -0004, tres con resultados) sin fusionar. Lee su cadena de sucesión con el mismo criterio de P2 y dictamina para mesa: fusionable tal cual / fusionable solo -0004 con la historia asentada / no fusionable. No la fusiones tú. (b) Las tres codex/optimiza-verificacion-ci* tocan tests/check.py y .github/workflows/verify.yml — carril Claude — y una trae un commit «test temporal: fallos y omisiones para comprobar compuerta CI»: ninguna se fusiona; si la idea (paralelizar la suite) vale, queda como una línea de demanda. Fila en hallazgos pidiendo a mesa el borrado de las tres. P5 · ADR de recibo y de cierre de carril, una línea por PR. Incluye el balance que dirección entregó a mesa (adjunto EVALUACION-CARRIL-CODEX-2026-09-20.md) como anexo citado, no como texto normativo. P6 · Rótulos de contenido en las mediciones con fuente no oficial o sin diseño acreditado (ISSP ×3, WBES ×3): clase de evidencia, si hay o no incertidumbre muestral, y universo. WBES es encuesta a empresas: evidencia sobre establecimientos formales registrados, no sobre "los mexicanos" ni sobre el sector informal, que es la mayoría del empleo — una línea por CALC; si algún consumidor del motor lo cita sin ese universo, NC.

PERÍMETRO

TSV y ADR de gobierno · registro-rotulos · derivados por comando · specs solo en cuenta_gen2 si ése es el mecanismo · nota. No toca tools/, tests/, milpa/, marcador, tablero (es de TABLERO-SENAL-1), resultados de ningún CALC, ni las ramas Codex. «Si te encuentras escribiendo fuera de esta lista, PARA.»

LO QUE NO HACE

No mide · no fusiona ni borra ramas · no interpreta resultados · no revierte #895.

CIERRE

Cascada D-10 · ## NO-CORRIDO / RESERVAS · ## CONSUMIDO · cero ramas propias.
