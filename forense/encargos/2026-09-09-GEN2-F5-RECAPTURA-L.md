# ENCARGO · ACTO GEN2-F5-RECAPTURA-L

Recibido en mesa 9/sep/2026. Texto verbatim del lanzamiento:

> ENCARGO · ACTO GEN2-F5-RECAPTURA-L · EL DUELO DE LA MISMA GENERACIÓN, PRIMERA MITAD — el contrato se congela, y las 224 capturas se toman en una caja aislada donde ni el corpus del programa ni las respuestas pueden filtrarse
>
> CABECERA · CAJA (UBUNTU/WSL de mesa), Opus · NO se lanza en NUBE — mesa exige la captura dentro de una caja Ubuntu controlada, y la sesión claude autenticada vive ahí · COMPUERTA: GATED a PR del ACTO GEN2-RETIRO-CRON-LEGADO fusionado (fila de caja; además garantiza que ningún cron dispare a media captura) · redactado contra origin/main = ffeeca2c (PR #667) · candidatos: deriva al cierre, no heredes. ⚠️ MECÁNICA DE MODELO, decidida y no negociable: Claude Code CLI en modo print (claude -p), CERO API — firma de mesa del 2/sep/2026 citada verbatim en runner_l_cli.py: «dame una opcion donde no tenga que usar API ni gastar en API, la anterior se consumió 20 dolares de API y fue un reto la api key y todo eso.»
>
> FIRMA DE MESA, 9/sep/2026, verbatim (adentro; su merge sella): «Ya habíamos decidido no hacerlo a través de API, solo quiero asegurar que las llamadas que me compartes son dentro de una caja en ubuntu sin acceso al corpus etc, necesito eso turbo blindado, así que avancemos.» — y la elección de diseño que dirección propuso y mesa avanzó: transferencia como pregunta primaria, uso documental como secundaria pre-registrada, re-captura ya.
>
> VERIFICACIÓN DE EXISTENCIA (A.8, contestada por dirección, 9/sep/2026, contra ffeeca2c): (1) ESTRUCTURA — gobiernan: forense/prereg-duelo-v2/runner_l_cli.py (EXISTE: invariantes pre-registrados — prompt de sistema reemplazado por cadena mínima fija, k=8, dos variantes, versión del cliente derivada de claude --version al correr, sufijo -M para no colisionar con las 424 capturas históricas) · forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv (14 celdas) · los seis CALC-R-CIV-M-* GEN2 + corridas-R/ (los árbitros con cadena) · PAQUETE-L-v1_1.md y prereg-corrida-v1_0.md (el contrato heredado que este acto sucede, no reescribe). (2) CONTENIDO — capturas GEN2 del marco v1_3: NO-ENCONTRADO (las 424 existentes son pre-GEN2, NC-0077: 435 payloads posteriores a su ventana — la razón de ser de este acto). La serie R 2012→2025 con cadena EXISTE completa (#657/#661): el corte de transferencia por ola es construible por primera vez. (3) COBERTURA RETROACTIVA — las capturas viejas NO se borran ni renombran (evidencia histórica); el marcador INCONCLUSO (#651) es el estado que este duelo viene a superar por sucesión.
>
> PIEZAS (dos commits + captura; el CALC del duelo es acto sucesor, no éste): P1 · EL CONTRATO, CONGELADO ANTES DE CAPTURAR (COMMIT-1 — nada se captura hasta que esto esté commiteado). La spec del duelo declara: (a) pregunta primaria = TRANSFERENCIA: para cada celda de ola X, L_CORPUS recibe únicamente material permitido por el corte temporal de X (lista explícita por celda, derivada de fechas de los documentos del paquete — un documento que contenga cifras de la ola X o posteriores queda EXCLUIDO de esa celda); M y B se evalúan bajo el mismo corte; (b) secundaria = USO DOCUMENTAL: el paquete completo congelado, conclusión acotada al panel — las dos preguntas no se mezclan en una afirmación; (c) el paquete-corpus: lista cerrada de documentos con hash individual y del bundle, construida desde el corpus GEN2 adoptado, excluyendo por construcción todo artefacto que contenga los valores objetivo — CALC-R/, corridas-R/, la serie del cierre DBF, resultados del marcador, y esta misma conversación de dirección no existe para la caja; la lista de exclusión se pega en la spec con la razón de cada una; (d) 14 celdas × 2 brazos × k=8 = 224 invocaciones, orden contrabalanceado fijado por semilla declarada, reintentos acotados y contados; (e) escala de adjudicación EXHAUSTIVA pre-declarada (B-bis): qué significa que L_CORPUS gane, pierda, empate, e INCONCLUSO como salida válida con su regla de precedencia; qué corrobora y qué acota cada desenlace, dicho antes de ver dato; (f) incertidumbre con sus tres fuentes separadas (celdas/panel · réplicas · error del árbitro R condicional, con su límite declarado); prohibido ampliar n tras ver el signo sin diseño secuencial previo; (g) contaminación declarada: los valores R están en el repo público del programa y en la memoria de dirección — por eso el blindaje de P2 es de aislamiento físico, no de promesa. Cierra con la frase: «el primer resultado que produzca este procedimiento es el que se reporta». P2 · EL BLINDAJE, VERIFICABLE Y PEGADO (antes de la primera invocación). La captura corre desde un directorio de trabajo aislado fuera de todo clon, que contiene EXCLUSIVAMENTE: el runner (copiado, con su hash), la spec sellada, y el paquete-corpus (solo para las invocaciones L_CORPUS de cada celda, según su corte). Evidencia obligatoria pegada en la nota: (1) ls del directorio aislado — sin repo, sin data/raw, sin corridas-R; (2) firma A.2 de la sesión mostrando que el proceso de captura no tiene el corpus de microdatos montado ni ruta al clon; (3) cada claude -p se invoca sin --add-dir, sin herramientas de archivo sobre el clon, prompt construido por el runner desde la spec — el texto exacto de cada prompt se hashea y registra; (4) claude --version y timestamps por captura; (5) los dos brazos en la misma ventana, sesiones stateless independientes (una invocación = una captura, sin memoria entre celdas ni entre brazos). Si cualquiera de las cinco evidencias no puede producirse, PARA antes de capturar — el blindaje es compuerta, no decoración. P3 · LA CAPTURA Y SU REGISTRO (COMMIT-2+). Las 224 capturas a corridas-L-M/ con el esquema verificado del runner, embudo contado (éxitos, reintentos, rechazos, truncamientos — un brazo que se abstiene en celdas difíciles se reporta con cobertura sobre TODO el marco, no solo sobre sus éxitos), manifiesto de capturas con hash por archivo, y la fila de cada captura ligada a su prompt-hash (guardia §3.5: cada captura su fila, cada fila su captura). NADA se adjudica aquí: cero cómputo del marcador, cero comparación contra R — eso es del CALC sucesor, con las capturas ya selladas e inamovibles.
>
> PERÍMETRO Y CONCURRENCIA. Toca: forense/prereg-duelo-v2/ (spec nueva del duelo + corridas-L-M/ + manifiesto de capturas) · forense/notas/ · forense/no-corrido.tsv (append) · 0-bis · cascada. El directorio aislado vive FUERA del clon y se documenta, no se commitea (salvo sus hashes). EN PARALELO: trámites NUBE — intersección solo en no-corrido.tsv y derivados. NO toca: milpa/, CALC-*, capturas históricas, marcador. «Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.»
>
> CONTADOR: no — las capturas son insumos sellados del duelo, no una medición; el CALC sucesor es quien contará, con su propia firma. Se dice en una línea al cierre.
>
> LO QUE NO HACE: no llama a ninguna API ni maneja key alguna · no adjudica la tesis ni corre el marcador · no toca las 424 capturas históricas · no amplía k ni celdas sobre la marcha · no mete al paquete-corpus nada fuera de su lista cerrada · no decide margen_utilidad_pp (si mesa lo quiere, viaja como firma al lanzar el CALC sucesor, antes de ver resultados).
>
> SUCESORES: ACTO GEN2-F5-DUELO-CALC (NUBE u caja según demanda — consume capturas selladas + los seis R GEN2, ejecuta la escala pre-declarada, con firma de contador viajando en su lanzamiento) · la decisión de mesa que el veredicto pida.
>
> CIERRE · Cascada completa + ## NO-CORRIDO / RESERVAS + ## CONSUMIDO con el PR.

## Desviación acotada, autorizada por mesa a mitad de sesión

La COMPUERTA declarada ("GATED a PR del ACTO GEN2-RETIRO-CRON-LEGADO fusionado")
no se cumplía al arrancar: ese PR no existía en ningún estado, y el crontab
legado de WSL seguía instalado (verificado empíricamente). Presentada la
evidencia, mesa autorizó ejecutar P1+P2 ahora y detener antes de P3 (patrón
[[feedback-partial-gate-deviation]]). A mitad de sesión, `PR #668 ·
GEN2-RETIRO-CRON-LEGADO` se fusionó (`cc1cfe2`) — la compuerta se cumple desde
ese momento. P3 sigue sin ejecutarse en este acto: lanzarlo es una decisión de
mesa que esta sesión no se autoconcede solo porque la compuerta se despejó.

## NO-CORRIDO / RESERVAS

| NC | Qué no se corrió | Razón | Impacto | Sucesor |
|---|---|---|---|---|
| `NC-0134` | P3 completo: las 224 invocaciones reales de `runner_l_cli.py --correr`, `corridas-L-M/`, manifiesto de capturas | `DECISIÓN-DE-MESA-PENDIENTE` — la compuerta que bloqueaba P3 se cumplió a mitad de sesión (`PR #668`), pero el encargo autorizó explícitamente solo P1+P2; lanzar 224 invocaciones reales con captura sellada e inamovible no es una expansión de alcance que esta sesión se autoconceda | Ninguna captura GEN2 del marco v1.3 existe todavía; `NC-0077` (435 payloads posteriores a la ventana) sigue abierta | Este mismo acto (`GEN2-F5-RECAPTURA-L`), P3, en cuanto mesa autorice el lanzamiento — el blindaje (P2) y el contrato (P1) ya están verificados y listos |
| — | Cascada completa de cierre (ADR, L0, `registro-rotulos.tsv`, T25) | `DIFERIDO-A` el cierre completo del acto — sellar un ADR para un contrato cuyas dos terceras partes (P2 ejercido solo parcialmente sin captura real, P3) siguen pendientes sería prematuro; `cierre_acto.py` ya deriva el candidato (`443`, dado que `442` lo tomó `PR #668`) para cuando corresponda | Ninguno — `canon/gobernanza-v1_15.md` sigue coincidiendo (441 ADR reales = cabecera = L0) | Cierre completo del acto, tras P3 + `ACTO GEN2-F5-DUELO-CALC` |
| — | Registro del rótulo `GEN2-F5-RECAPTURA-L` en `canon/registro-rotulos.tsv` | `NO-VERIFICABLE-AQUÍ` — `cierre_acto.py` marca `que_significa`/`donde_vive` como juicio humano, no mecánico | Ninguno hoy | Cierre completo del acto |

**Contador:** no se movió — cero llamadas a `claude`, ninguna captura, ningún
cómputo del marcador. Se dice en una línea, como el encargo pide.

## Estado

`ACTO GEN2-F5-RECAPTURA-L` — **CONSUMIDO (parcial)**: P1 y P2 completos y
verificados con el PR de la rama `acto/gen2-f5-recaptura-l` (base `origin/main =
ffeeca2c`, ejecutado contra `origin/main = cc1cfe2` tras el merge de `PR #668`
a mitad de sesión — número de PR pendiente de asignar al abrirlo). P3 queda
`ABIERTA` (`NC-0134`) hasta que mesa autorice su lanzamiento.
