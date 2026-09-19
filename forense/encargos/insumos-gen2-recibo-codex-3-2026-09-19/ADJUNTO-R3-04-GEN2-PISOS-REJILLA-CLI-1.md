# ENCARGO · GEN2-PISOS-REJILLA-CLI-1

**Base de preparación:** `843a5f977e024ef5d74863e95856c763bee9e58d`, 19/sep/2026. **Entorno:** Codex CLI en Ubuntu/WSL con corpus; no nube sin corpus. **Sesión:** una sola, preferiblemente la que llevaba el 03; nuevo worktree y rama propia desde main, por ejemplo `codex/gen2-pisos-rejilla-cli-1`. **Compuerta:** ninguna dependencia de merge para empezar. **Modelo:** el modelo Codex ya asignado; sin llamadas a modelos ni cambio de proveedor. **Entrega:** un PR, sin merge.

## Resultado

Entregar pisos marginales comparables con el árbitro para ENVIPE 2024, ENCIG 2023 y ENIF 2021, con ambos desenlaces ENIF; código real congelado, RESULT numéricos por celda, replay asentado y publicación completa. Resolver dentro de este encargo el acceso al corpus y la reparación del registro que hoy impiden esa entrega. Una nota de inventario o un CALC sin publicación no sustituyen el resultado.

La autoridad más reciente de los adjuntos deja el marcador y la adopción en Claude. Este encargo sustituye el trabajo futuro de reparación que antes se había acumulado en el 03, no su historia. No desarrolla el consumidor ni el marcador.

## Firmas y límites

- D1 recibida: «El dueño del marcador es acá». `GEN2-MARCADOR-REDISENO-1`, del lado Claude, lleva construcción y adopción. Codex 03 cancelado para trabajo futuro.
- D2 recibida, mesa «si vetado»: veto a adopción de los cuatro `CALC-PISOS-*` de #866 hasta disponer de sucesores correctos. Preserva sus bytes.
- La D3 propuesta sobre el ENCIG original y su contador **no está firmada**. No la apliques ni deduzcas que SUPERADO implica dejar de contar.
- El brief 01 amplía el lote a los dos desenlaces ENIF. Esa ampliación sustituye la exclusión del secundario en el antiguo encargo 02.

Consulta AGENTS.md, instrucciones v2.14, este encargo, los briefs 00/01, el encargo 02 histórico y las specs selladas necesarias. `/acto` no es una dependencia de software de Codex: ejecuta el procedimiento aplicable con herramientas del repo. No pidas otra autorización para acciones ya incluidas aquí.

## Existencia y arranque

En la base revisada, #865/#866/#867 están fusionados. #868 está abierto en `9e9e89225f0d986cf51b955940ebee7526809f1b`: publica replay y añade integración de 20 C2, pero no contiene sucesores de pisos. `tools/pisos_ejes.py` de main conserva códigos crudos, edad hasta 97, denominador ENCIG amplio, eje de débito usado como cuenta y salida TABLA textual. La fuente de replay contiene 41 asientos recuperados; la publicación pendiente es trabajo útil ya intentado en #868. Re-verifica el delta actual antes de implementarlo.

Reporta ruta, rama, HEAD y estado; fetch/prune, localiza trabajos equivalentes y preserva cambios ajenos. Antes de salir del worktree del 03, guarda los cambios propios pendientes en un commit de avance y conserva el SHA remoto. No fuerces reset, no borres ramas ni cierres #868. Trabaja desde main en un worktree nuevo. No cherry-pickees el commit mixto de #868: no debes traer su motor, lector, mapa ni usos de adopción.

Archiva este encargo y fuentes con SHA-256 real en una ruta propia. Usa cuatro piezas operativas como máximo: A1 acceso/replay, A2 diseño, A3 medición, A4 publicación/entrega. No crees un encargo por instrumento.

## A1 · Acceso y registro: resolver el bloqueo dentro del lote

Inputs principales: `envipe2024_csv`, `encig23_base_datos_csv`, `enif2021_csv`, y los documentos técnicos que acrediten variables/códigos. Lee las entradas actuales del manifiesto y las ejecuciones de #866. El cuerpo de #868 reporta que no localizó esos payloads: eso no demuestra ausencia del corpus.

Localiza el clon padre, configuración de raíces, variables del resolvedor, worktrees de las ejecuciones originales y corpus compartido; después las ubicaciones documentadas de WSL/Windows, descargas y contenedores. Busca nombres y variantes con inventario acotado. Comprueba archivo, tamaño y hash del objeto correcto. No confundas ZIP y miembro. No publiques rutas privadas ni microdatos; no muevas originales ni copies el corpus a Git.

Deja la configuración persistente y verifica desde nueva terminal y subproceso. Si el archivo no se localiza, queda autorizada la **recuperación del mismo archivo/edición desde su origen público documentado**, mediante el mecanismo existente de adquisición. Comprueba hash antes de usarlo. Si el proveedor cambió bytes, conserva ambos objetos y registra un input nuevo con procedencia acreditada; congela la revisión de diseño correspondiente antes de leer respuestas. No alteres la identidad del input histórico para hacerlo coincidir. No adquieras olas actuales ni nuevas familias.

Antes de COMMIT-1 solo puedes localizar, hashear y leer cuestionarios/FD/metadatos; no leer respuestas ni correr replay que las abra. Si hay un bloqueo real de acceso, conserva el diseño realizable y explica la intervención precisa; no llames NO-CONSTRUIBLE a una falta de montaje.

Después de COMMIT-1, completa la reparación de replay pendiente con la evidencia aislada válida ya obtenida, sin repetir las 41 corridas por rutina. Compara identidades actuales y prepara transiciones justificadas. Puedes reutilizar la evidencia del #868, pero las vistas se generan sobre este árbol, sin sus adopciones.

La publicación de los 38 REPRODUCE/IDENTICO y el NO-REPRODUCE/IDENTICO de DIN está autorizada mediante el `--lote` existente cuando la evidencia siga vigente. DIN conserva NC-0313 y la discrepancia `G-R-EXISTE-AL-CERRAR`; acredita separadamente los puntos/IC C2 por RESULT, sin cambiar el veredicto global.

Para las limitaciones de ENCRIGE/ENSANUT localiza también `conjunto_de_datos_encrige_2020_csv`, `encrige2020_cuestionario` y `adultos_ensanut2024_w_stata_stata__v2026_09_01`. Reproduce solo las corridas existentes necesarias en procesos aislados. Recupera evidencia primaria concluyente previa si existe y no la sustituyas con una limitación local. Si no hay evidencia concluyente acreditable, conserva NO-VERIFICABLE y su causa; se autoriza publicar esa transición desde NO-VERIFICADO con justificación explícita. No inventes REPRODUCE ni fechas.

No desactives REPLAY-PISADO ni uses exclusiones. `--lote` autoriza transiciones revisadas; no selecciona qué verificar. Valida la proyección y el guardia antes de escribir. Una corrida ajena nueva se investiga antes de autorizarla. No conviertas esta pieza en replay general del corpus.

## A2 · Congelar rejilla, universos y código antes de las respuestas

Deriva las identidades objetivo del árbitro vigente, incluyendo desenlace, instrumento, edición/periodo, unidad/universo, eje y categoría. Extrae un snapshot mínimo de esos **metadatos**, sin valores R, errores ni resultados de la ola actual; conserva la referencia/hash del origen. El cálculo usa ese snapshot congelado, no un árbitro mutable como entrada numérica. Mapea los reactivos de la ola anterior por texto y catálogo.

| Instrumento | Desenlaces y ejes | Referencia orientativa |
|---|---|---|
| ENVIPE 2024 | evasión: sexo, edad, escolaridad_proxy, dominio; denuncia: cobertura_seguro | 13 + 2 |
| ENCIG 2023 | adopción digital del universo acreditado: sexo, edad, escolaridad | 10 |
| ENIF 2021 | principal `ahorra_solo_informal` y secundario `informal_cualquiera`; cada uno por sexo, edad, escolaridad, localidad y cuenta_formal | 14 + 14 |

No impongas 53 resultados ni 74 como denominador universal. Formalidad ENIF queda fuera de ambas mediciones si se confirma la ausencia de P3_13 comparable: registra las cuatro celdas excluidas por identidad. No fusionas los dos desenlaces aunque coincidan sus cortes.

Corrige estos defectos:

- Escolaridad: cuatro categorías acreditadas, verificando la correspondencia de los códigos propios de cada ola.
- Edad: 18–29, 30–44, 45–59 y 60–96 donde esa sea la definición sellada; excluye centinelas/blancos del eje, sin convertir faltantes a texto. No apliques exclusiones de edad o escolaridad a otros ejes indiscriminadamente.
- Localidad ENIF: {1,2} = 15 000 y más; {3,4} = menor de 15 000, según catálogo.
- Cuenta formal ENIF: P5_6 de 2021 es débito en la evidencia documental de DIN emisiones §0.1; confirma FD y usa P5_4 para tenencia cuando la equivalencia esté acreditada. D9 usa P5_1_1..6 e inexistencia de ahorro en P5_7_1..9; el secundario usa ahorro informal cualquiera. D7 no sustituye D9.
- ENCIG: N_TRA=01, adopción P7_3=4/5, no adopción 1/2/6, exclusiones restantes según equivalencia acreditada de 2023. Normaliza códigos antes de filtrar. Conserva unidad trámite y evita multiplicación por joins.
- ENVIPE evasión: universo BP1_20 válido 1/2. Los blancos/otros se cuentan después de COMMIT-1 y se excluyen según diseño.
- Denuncia por seguro: verifica desenlace BP1_20 y universo BPCOD=01, BP2_1 válido 1/2; mide asegurado/no asegurado o documenta la diferencia que impide construirlo.

Fija ponderadores propios de ola, estratos, UPM, llaves, tratamiento de secuencia/no respuesta, límites de soporte y universo por eje. Bootstrap de diseño 10 000 réplicas, seed 42, esquema sellado compatible; declara estratos con una UPM, denominadores vacíos y réplicas compartidas entre celdas/desenlaces del instrumento. No sustituyas por bootstrap i.i.d. ni ocultes réplicas indefinidas con una salida numérica automática.

Crea una spec humana con sidecar, spec.yaml ejecutable y medidor completo por instrumento construible, con ids sucesores libres según la casa. **COMMIT-1 incluye código ejecutable real y diseño**, no un shim cuyo helper mutable quede fuera del sello. Preferencia: medidor autocontenido dentro de cada CALC. Si usa módulos locales, sus bytes deben quedar congelados y comprobados por el mecanismo existente; no inventes un framework de sellado.

Incluye «el primer resultado que produzca este procedimiento es el que se reporta». Declara honestamente la exposición histórica: esto es un correctivo sobre datos previamente usados, no un piloto ciego nuevo. No se hace corrida en seco sobre respuestas antes del commit. Specs y COMMIT-1 preceden también los replay de A1 que reabran microdatos.

## A3 · Medir, controlar y suceder

Abre únicamente las olas anteriores autorizadas para las nuevas mediciones. No abras ENVIPE 2025, ENCIG 2025 ni ENIF 2024 para recalibrar el piso o comparar su rendimiento. Las excepciones de replay son solo para corridas existentes y nunca autorizan abrir reservas no consumidas.

Ejecuta preflight → run → verify aislado por instrumento. Usa un CALC por instrumento para todas sus celdas y desenlaces comparables. Conserva resultados diagnósticos y cualquier fallo real; una corrección posterior al sello crea un sucesor.

Cada celda construida tiene un RESULT puntual numérico propio, RESULT de IC95 inferior/superior, n sin ponderar, denominador ponderado y metadatos de universo/escala. Usa el esquema de la casa; estos RESULT auxiliares no son celdas adicionales. Los excluidos tienen conteos identificables. No serialices todas las celdas en un RESULT de texto.

Produce una tabla de entrega por identidad completa con estado CONSTRUIBLE/NO-CONSTRUIBLE, o ausencia por soporte claramente diferenciada, CALC, referencias, punto, IC, n, denominador y consumidor previsto. La falta de acceso se declara aparte, no como diferencia semántica. Explica en una línea que el IC representa incertidumbre muestral en t−1, no predicción de t ni causalidad.

Preserva los cuatro CALC de #866 y `tools/pisos_ejes.py` tal como fueron usados. Registra los nuevos sucesores y su linaje. Se autoriza únicamente la compatibilidad mínima de lectura necesaria para reconocer `sucesor_de` ya declarado y el mecanismo `repite_de`; no cambies aptitud, precedencia de replay, contadores ni consumidores para facilitar la entrega. Si no hace falta tocar corrida0, no lo toques. Nunca adoptes el ENCIG v1.1 intermedio para resolver el estado de su antecesor.

La generación numérica se documenta; la inclusión de nuevas corridas en el contador se propone a mesa. Si el contrato soporta el token existente `PENDIENTE-DE-MESA`, úsalo explícitamente para no heredar SI por defecto. No elijas SI o NO ni reclasifiques sellos existentes por tu cuenta. Deriva estado y contador reales, indicando esa reserva administrativa separada de la publicación de resultados.

Controles proporcionales: (1) un control de conjuntos, cuya clave incluya **entrada y desenlace**, que compare la rejilla congelada con las celdas emitidas más dictámenes y rechace duplicados, faltantes, sobrantes o categoría nan; (2) control puntual independiente sencillo, al menos uno por instrumento y ambos desenlaces ENIF, con las mismas definiciones. Reutiliza pruebas existentes de código/contrato; no construyas tests ceremoniales por cada celda ni declares validación independiente del IC por repetir el mismo bootstrap.

## A4 · Publicar y entregar listo para Claude

Asienta cada nuevo replay antes de publicar, con identidad y evidencia cruda citada. Regenera demanda/vistas afectadas por los comandos de la casa. Publica los sucesores y relaciones resueltas en este PR; conserva la distinción sellada-en-disco/publicada si existe un bloqueo externo real.

Verifica el resultado de los comandos y el diff de las vistas; un árbol sucio no acredita publicación. Repetir la derivación con las mismas fuentes debe ser estable. Los nuevos pisos tienen cero usos de producción: la medición y el merge de este PR no autorizan su adopción, que pertenece a Claude.

Entrega `pisos-rejilla-entrega.tsv` y una nota suficiente para B y Claude: celdas por instrumento/desenlace; no construibles y su causa; exclusiones observadas, incluidos BP1_20 blancos; respuesta de cuenta/débito con cita del FD; controles; sucesión técnica; propuestas de clasificación; replay recuperado; cambios frente a los pisos vetados; cobertura potencial derivada sobre el árbitro completo. No cambies el marcador para calcular esa cobertura: el mapa técnico basta.

## Perímetro, coordinación y cierre

Propios: specs/sidecars nuevos, CALC sucesores y código congelado, snapshot de metadatos, `tests/test_pisos_rejilla.py`, mapa técnico, evidencia y fuente de replay, demanda y vistas corrida0 por generador, configuración local de corpus fuera de Git, entradas nuevas de manifiesto solo si recuperación acredita otro objeto, nota y archivo propios. `tools/corrida0.py` únicamente la compatibilidad de sucesión indispensable descrita arriba. La justificación de transiciones usa el mecanismo existente, no su relajación.

B es dueño de decisiones, firmas, NC, hallazgos, ADR, relevo, estado e infraestructura. Tu nota entrega los hechos para esos registros. No toques sus archivos canónicos. No toques motor, mapa de adopción, marcador, celdas-D, crosswalk, θ, R ni cron. «Si te encuentras escribiendo fuera de esta lista, PARA» aplica a esa ampliación, no cancela las piezas independientes autorizadas.

Prioriza cifra y publicación; no persigas WARN ni limpiezas ajenas. Ejecuta pruebas dirigidas y baseline pertinente al cierre, corrigiendo fallos introducidos y distinguiendo los heredados. No redefines un baseline para esconderlos.

Antes de entregar sincroniza main y regenera desde fuentes; comunica a B el SHA y el mapa. Un PR con HEAD remoto, sin merge, con `NO-CORRIDO / RESERVAS` y `CONSUMIDO`. Solo se declara completo cuando el acceso está resuelto, las mediciones están publicadas y el mapa permite el consumo posterior, o cuando un residuo externo exacto está demostrado sin presentar trabajo parcial como completo.
