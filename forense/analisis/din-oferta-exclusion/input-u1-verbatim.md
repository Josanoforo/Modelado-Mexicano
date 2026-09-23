# ASTRA-3 · U1 · medir exclusión por oferta en ENIF

**Lanzamiento: AHORA, sesión nueva.** Rama `codex/astra3-enif-oferta-1`; worktree propio sugerido `/home/pc0/mm-astra3-enif-oferta-1`. Independiente de U2/U3 y ASTRA-2. No requiere una solicitud de adquisición para empezar.

## Objetivo

Sellar por ola la proporción de no-usuarios que reporta razones de oferta, preferencia y otras/no respuesta, para crédito formal y cuenta/ahorro formal cuando el instrumento permita separarlos. Personas 18–70; ejes sexo, edad, escolaridad, localidad y formalidad laboral, más nacional. Terminar con CALC por ola construible y enlace a cada piso de crédito histórico pertinente. No confundir cuenta con ahorro activo ni reportar una causa identificada: son motivos declarados.

## Decisiones de Astra que deben convertirse en spec antes del dato

1. Ola principal: ENIF2012/2015/2018/2021. No es necesario abrir ENIF2024 para cumplir el núcleo. No extiendas U1 a ENIF2024 por la autorización de U3: son objetos diferentes. Si se propone añadir una medida 2024, verificar primero que ese estimando exacto fue consumido y autorizado; nunca calibrar con él.
2. Denominador primario: todos los no-usuarios de la conducta correspondiente, personas 18–70 con estado de uso conocido y ponderador válido, dentro de cada categoría del eje. No-usuario actual, nunca usuario y solicitante rechazado NO son el mismo universo. Si razones solo se preguntan a una subpoblación, mide su cobertura del no-uso; no extrapoles razones al resto. Una tasa entre quienes solicitaron puede reportarse separada con su denominador, sin sustituir la requerida.
3. Tabla por opción, a partir de texto completo y pases de cada ola: rechazo/requisitos/distancia o ausencia de servicio/costo explícito → OFERTA; no necesitar/desconfianza/preferencia explícita por informal → PREFERENCIA, como convención de esta misión; resto/ambigüedad/NS → OTRO/NS. «No tengo dinero/ingreso» no equivale automáticamente a costo del producto: clasificar OTRO con submotivo salvo texto que explicite barrera de oferta. Desconfianza queda como motivo declarado bajo la convención, sin inferir que carezca de fundamento institucional.
4. Si hay razón principal única, usarla. Si hay respuesta múltiple sin principal, clasificar cada opción y crear la partición personal: solo oferta, solo preferencia, OTRO/NS (mixta oferta+preferencia, otras, incompleta o desconocida, con subcategorías explícitas). Añadir prevalencias de cualquier mención de oferta y de preferencia y su intersección; pueden sumar más de 100%, no son la partición. No resolver las mixtas con una prioridad oculta. Marcar no comparabilidad entre razón principal y cualquier mención cuando corresponda.
5. Mantener en OTRO/NS el no-uso con motivo no observado, distinguiendo pase estructural de no respuesta. Si no se observa en absoluto el motivo de oferta o preferencia, NO-CONSTRUIBLE para esa medida; no fabricar dos ceros y 100% OTRO. Opción ausente entre olas = NO-COMPARABLE para el contraste específico, aunque otras medidas de la ola sean construibles.
6. Bootstrap de UPM dentro de estrato con ponderadores del instrumento, 10 000 réplicas PCG64(42), compartidas por todas las celdas de cada ola, percentiles 2.5/97.5. Tratar edad y categorías como dominios conservando el marco muestral. Si existen pesos replicados oficiales pertinentes, utilizar su método documentado en vez de inventar uno y congelarlo. Declarar singleton, denominador cero y réplicas inválidas; sin seleccionar método tras ver amplitudes.

## Datos y ejecución

En main existen ids como `enif_2012_bases_enif2012_dbf`, `enif_2015_enif_2015_bd_dbf`, `enif2018_csv`, `enif2021_csv`, `enif_2021_enif_2021_bd_csv`. Son alternativas/formatos, no todos inputs obligatorios. Elige el payload ya usado por los lectores históricos compatibles y fija su hash. No abrir los datos antes de congelar códigos, pases y reglas.

Leer specs históricas de crédito y la firma del recorte18–70 para sus ejes. Congela `conmensuracion-v1_0.tsv` por conducta/ola/pregunta/opción/eje, cita documental y estado. Comprueba que formalidad significa el mismo proxy en cada ola; no rebautices derechohabiencia como contrato formal. No modificar pisos ni reestimarlos.

Emite P/IC95/N sin ponderar/denominador ponderado/estado por clase y celda; incluye cobertura de la batería y submotivos faltantes. Prueba con fixture dirigido única/múltiple, pases, opción ausente, denominador vacío y partición que suma uno. Ejecuta todas las olas construibles, incluso si otra falla por falta de pregunta. No forzar ≥3 CALC inventando estimandos: si el criterio esperado no se alcanza, cita exactamente por qué.

Entrega enlace por identidad a los RESULT de piso de crédito2012–2021, con RESULT de exclusión de la misma ola/universo/eje o causa de no enlace. No vincular por posición ni usar tasa de cuenta para acompañar crédito sin identificar el producto distinto. También entregar las medidas de cuenta/ahorro requeridas aunque no tengan esos pisos consumidores.

## Perímetro y hecho

`forense/prereg-caja/DIN-OFERTA-EXCLUSION-ENIF-spec-v1_0.md` y sidecar; `data/corrida0/CALC-DIN-OFERTA-EXCLUSION-ENIF<ola>-0001/`; `tools/astra/enif/oferta/`; `tests/test_astra3_enif_oferta.py`; `forense/analisis/din-oferta-exclusion/` (conmensuración, enlace-pisos.tsv, nota, recibo y originales); append propio de replay. No NC/FP ni adquisiciones directas en el manifiesto desde esta rama.

Hecho = cada ola construible sellada y reproducible, razones no comparables explícitas y enlace completo de los pisos, con una lectura sustantiva de cuánto no-uso puede describirse por barreras reportadas. No atribuir causalidad a esta descomposición.

## Reglas de ejecución de esta tanda

Adjunta y lee íntegra `MISION-ASTRA-3-mide-lo-que-falta.md`. Base verificada por Astra `523f3c6d8ddc3d11594efe33f97a1e9a89bab228`; `git fetch origin` al abrir, declara ruta/HEAD/status y comprueba por objeto que tu unidad no esté ya ejecutándose. Una sesión escritora por unidad y un PR propio. No tomar el worktree de ASTRA-2 ni detener esa misión.

Usa primero manifiesto, catálogos, documentación y corpus compartido existente. Los ids abreviados de la misión no son necesariamente ids exactos: deriva id/ruta/hash del manifiesto y de las specs vigentes; no crees duplicados. Si falta un insumo concreto, búsqueda primaria y adquisición por carril adq autorizado, antes de consumirlo; no un inventario general. La ausencia de data/raw en un worktree no prueba ausencia de bytes.

Entorno CAJA para microdato. Antes de lectura de valores: cuestionarios/FD, decisiones de método, spec humana + sidecar y spec.yaml con inputs/hash, medidor completo y commit de freeze. Incluye «el primer resultado que produzca este procedimiento es el que se reporta». Hash y presencia del payload pueden verificarse sin tabularlo. Una lectura previa de resultados debe declararse; un git log por sí solo no prueba que nadie abrió bytes. Las sesiones que ya vieron una ola no vuelven a declararse ciegas.

Lee las reservas aplicables, sin abrir los resultados que protegen. No ENCIG2025, ENVIPE2026, ENCO2025/2026 ni ENIGH2024; ENVIPE2025 queda fuera de estas tareas. ENIF2024 se permite solo en el alcance consumido expresamente autorizado a cada unidad. No extrapolar esa autorización a crédito o variables nuevas.

El proceso continúa hasta cerrar: preparación documental → freeze → preflight → run → verify → asiento propio append en forense/replay-evidencia.tsv → nota y recibo → commit/push/PR. No esperes otra tanda entre fases ya autorizadas. No modificar registro ni correr `registro --escribe`; no tocar CI/check.py/verify.yml, tablero, marcador, celdas-D, milpa ni sellos ajenos. Tests dirigidos propios, sin instrumentar CI. Un defecto fuera de perímetro se declara en una línea y no absorbe el encargo.

Etiquetas completas: generacion GEN2, cuenta_gen2 SI para las corridas de esta misión, adopta NO y origen_numerico verdadero conforme al contrato (MICRODATO si se estima de microdato; cálculo sobre RESULT sellados, rotulado según el esquema vigente sin fingir nueva apertura). Tipo de evidencia e incertidumbre explícitos. Una estimación no construible es nula con causa, nunca cero.

No dejar la entrega en una spec si es ejecutable. Reutiliza herramientas selladas por ruta/hash sin modificarlas, prueba únicamente transformaciones y fallos materiales propios. Replay REPRODUCE y tolerancia fijada antes. Corrige bugs preservando primera emisión y exposición; no seleccionar variantes por resultado.

Cada nota/recibo usa EJECUTADO/LEÍDO/REPORTADO según la evidencia, cifras con comando, escala, unidad, universo, generación, hashes/commits, límites y lo no corrido con razón. `## NO-CORRIDO / RESERVAS` («Ninguno.» si aplica) y `## CONSUMIDO` con PR. Guarda misión e input verbatim en tu carpeta de análisis propia. Publicar rama/PR está autorizado; fusionar o adoptar queda en mesa.

