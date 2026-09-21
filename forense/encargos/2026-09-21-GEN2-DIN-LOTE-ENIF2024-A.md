ENCARGO · ACTO GEN2-DIN-LOTE-ENIF2024-A · EL LOTE DE CRUCES ARRANCA: SE SABE QUÉ OLAS DE ENIF SON COMPARABLES POR TEXTO, LA SPEC QUEDA ESCRITA Y EL PAQUETE DE LOS LLM QUEDA LISTO — SIN ABRIR UN SOLO MICRODATO

ENTORNO: NUBE, entorno milpa-inegi (egreso a INEGI permitido). Se reconoce por la sonda de red, no por la variable (dice cloud_default en los dos). Si la sonda sale DENEGADA: PARA en una línea — sin descriptores ni cuestionarios este acto no tiene qué leer. NO es CAJA: aquí no se abre microdato de ninguna ola. Trampa conocida: en cuanto un payload cae en data/raw, ENTORNO-DERIVADO se voltea solo a CAJA. No es PARO ni cambio de entorno: decláralo y sigue.

CABECERA · SHA de redacción 1f197a2c; re-deriva al abrir · una sola sesión, rama acto/gen2-din-lote-enif2024-a · MODELO: Opus (juicio de comparabilidad) · MODO: ABIERTO — nada se congela aquí; la spec sale como PROPUESTA y la congela el COMMIT-1, en caja, otro acto · CONTADOR: no mueve ninguno numérico; cuenta_gen2 NO-APLICA · FP/ADR/NC: raíz de acto. Si al fusionar main choca la línea L0 de canon/estado-programa-v1_14.md: NO conserves los dos lados. Toma la de main completa y re-inserta solo tu anotación (pesa 27 MB por duplicaciones; TUBERÍA la está reparando). Si canon/L0/ ya existe cuando cierres, tu anotación va ahí.

1 · OBJETIVO

El lote abre una sola vez los 14 cruces reservados de ENIF 2024 para ahorra_solo_informal, con todos los contendientes sellados antes. Su retador principal (R2) es la interacción histórica encogida según cuánto se repite entre olas: eso exige saber, ola por ola, si el desenlace y los ejes se preguntan igual. Hoy se sabe para 2021↔2024 (piloto 1) y no se sabe para 2012, 2015 y 2018. El piloto 3 acaba de mostrar que encoger importa: la interacción cruda erró 10.6 pp, la encogida 1.9, el piso 3.4. «Hecho» significa: (1) diseño v0.1 y enmiendas v0.2 y v0.3 archivados; la v0.3 asentada como firma · (2) tabla de comparabilidad por texto del desenlace y de los cinco ejes en las cinco olas, con veredicto por fila y test en CI · (3) spec humana del lote escrita como PROPUESTA, con sidecar, que cumple §5-P3 · (4) paquete de los LLM listo para que mesa lo corra · (5) una nota de una página: qué olas alimentan a R2 y cuáles no, y por qué.

2 · FIRMAS DE MESA — verbatim

F1 y F2 (21/sep) ya están en el repo como FP-260921-GEN2-TRAMITE-FIRMAS-4-8a1f-01 y -02 [EJECUTADO: grep en firmas-pendientes.tsv]: cítalas de ahí. F2, para que la tengas a la vista: «La comparación primaria es C2 contra R2 sobre los 5 pares con C2 adjudicado (44 celdas). Los 4 pares de formalidad pasan a secundaria, rotulada, con su C2 restringido al universo de quien trabaja (C2-COMPUESTO-RESERVADAS-spec-v1_0.md:129-132 lo dictamina NO-EMITIBLE contra ejes de universo completo). R2 con λ estimada se define por la estabilidad de la interacción entre las olas históricas de ENIF que resulten comparables por texto de pregunta —el manifiesto trae microdato y descriptor de 2012, 2015, 2018 y 2021—; si solo una lo es, R2 es solo λ = ½ y se declara antes de abrir. La fila M se sella NO-DERIVABLE, con su razón. Los pares de cuenta_formal se adjudican aparte porque en "sin cuenta" el estimando cambia por construcción del cuestionario, no por tautología. Segundo oro: reproducir el C2 ya sellado. Dueño: dirección (PRODUCTO-DINERO cerró).» Enmienda v0.3 — propuesta de dirección tras el veredicto del piloto 3; el lanzamiento de mesa con este archivo es el sello; este acto la asienta (A.12): «Lote ENIF 2024, enmienda v0.3: la estadística primaria es la diferencia de error medio entre C2 y R2 sobre las celdas puntuadas de los 5 pares, con IC95 por réplica. Vence si el IC despeja 0.5 pp; propuesta con reserva si despeja 0 pero no 0.5; nadie vence si incluye 0. El conteo de ¾ de celdas pasa a secundario, descriptivo. El COMMIT-1 incluye una simulación de potencia de esta regla sobre datos ya abiertos (pilotos 1 a 3). El veredicto del piloto 3 no se toca: sigue siendo FALSADOR DÉBIL.»

3 · LO QUE DIRECCIÓN SABE (contra 1f197a2c, sin corpus)
[EJECUTADO sobre data/manifiesto.yaml] descriptores y cuestionarios de ENIF, por id: enif_2012_fd_enif2012 · enif_2012_cuestionario_pdf · enif_2015_enif_2015_fd · enif_2015_cuestionario_pdf · enif2018_fd_xlsx · enif2018_cuestionario_pdf · enif2021_fd_zip · enif2021_cuestionario_pdf · enif2024_fd_xlsx · enif2024_cuestionario_pdf. Los dos cuestionarios de 2012 y 2015 entraron hoy (#960). En total < 8 MB.
[LEÍDO: forense/notas/2026-09-21-nube-piloto-1-bis-cierre.md:80-84] desde milpa-inegi, python3 tests/manifiesto.py --descarga --id <id> baja y verifica sha contra el manifiesto.
[EJECUTADO] precedente de forma: data/credito-comparabilidad-texto-v1_0.tsv (columnas conducta · ola · comparado_con · veredicto · alcance_del_veredicto · reactivo · texto_literal · opciones_y_codigos · filtro_y_flujo · unidad · poblacion_base · fuente · secciones_fd_recorridas · …) y su test tests/test_credito_comparabilidad_texto.py. Reúsalo: misma forma, mismo vocabulario de veredictos.
[EXISTE] definición vigente del desenlace y de los ejes: forense/prereg-caja/DIN-ahorro-solo-informal-lxe8-spec-v1_2.md (§0 trae los tres tropiezos de nemónico entre 2021 y 2024: la pregunta de ahorro informal cambia de número, el ponderador cambia de nombre, la edad cambia de variable) y forense/prereg-caja/PISOS-ENIF2021-ejes-spec-v2_1.md y PISOS-ENIF2021-formalidad-spec-v1_0.md para los ejes. [SUPUESTO] que esas tres specs bastan para fijar el texto ancla de cada fila: si no bastan, dilo y ancla contra el cuestionario 2021.
[LEÍDO] forense/prereg-caja/C2-COMPUESTO-RESERVADAS-spec-v1_0.md:129-132: formalidad vive en el universo de quien trabaja (cobertura 0.69) y es NO-EMITIBLE contra ejes de universo completo. [REPORTADO por PRODUCTO-DINERO] en «sin cuenta» el desenlace se reduce por construcción a «ahorra informal» (marginales sellados idénticos): confírmalo por el flujo del cuestionario, que es lo que este acto sí puede leer.
[LEÍDO en la rama de #961] piloto 3: 15/15 celdas con soporte; nadie vence por la regla de ¾ (3/15, 12 indecidibles, 0 derrotas); ΔMAE de la encogida 1.47 pp, IC95 [0.44, 2.12]. De ahí la v0.3.
[REPORTADO por la nota de #960] los dos diseños no llegaron a aquella sesión y no se archivaron: por eso el v0.1 viaja dentro de este archivo (Anexo A).
4 · YA HECHO

Por objeto («LOTE», «ENIF2024», «ahorro», «comparabilidad») en encargos, prereg-caja, data/ y ramas remotas (2 vivas: piloto 3 y TUBERÍA): hay comparabilidad por texto para crédito (#932), no para ahorro; hay spec del piloto 1 para un par; no hay spec del lote ni rama con ese rótulo. Ojo con el homónimo: forense/encargos/2026-09-09-GEN2-LOTE-ENIF-1.md es otro acto (un lote de CALC de ENIF del 9/sep), no este lote de cruces. Repítela tú.

5 · PIEZAS — P1 no depende de P0; P3 y P4 dependen de P1

P0 · Archivo y firma. Extrae el Anexo A a forense/prereg-caja/DISENO-LOTE-CRUCES-ENIF2024-protocolo-unico-v0_1.md: el contenido entre las dos líneas marcadoras, sin ellas, debe dar sha256 f9ea6d4fb8932d668f4bee808ed34e26d12297871be542457f1a4aa3845ed5a3; si no da, no lo «arregles»: repórtalo y sigue. Enmiendas …-enmienda-v0_2.md y …-enmienda-v0_3.md hermanas, con el texto verbatim de §2. Fila de firma para la v0.3. No edites el v0.1. P1 · Comparabilidad por texto. Para el desenlace ahorra_solo_informal (sus dos componentes: ahorro por vías informales y ahorro/tenencia por vías formales) y para cada eje —sexo, edad, escolaridad, localidad, formalidad, cuenta_formal— una fila por ola (2012, 2015, 2018, 2021 ancla, 2024): texto literal, opciones y códigos, filtro y flujo, unidad, población base, ponderador y variables de diseño que el descriptor declare, secciones del descriptor recorridas, y veredicto. Se busca por texto de pregunta, nunca por nombre de variable; un nemónico desplazado no es una pregunta ausente (A.15). Queda bien si: cada veredicto negativo cita el texto buscado y las secciones recorridas; el test hermano del de crédito pasa y está en CI; y la nota contesta sin adjetivos: ¿qué olas pueden alimentar la interacción histórica de cada par, y cuáles no? P2 · Consecuencia para R2, escrita antes de que nadie mida. Con el resultado de P1: si ≥ 2 olas históricas son comparables para un par, R2 lleva λ estimada por estabilidad entre ellas; si solo una, R2 es λ = ½ para ese par; si ninguna, P2, R1, R2 y R3 son NO-CONSTRUIBLE para ese par. Por par, en una tabla. El silencio no es un valor. P3 · Spec humana del lote — PROPUESTA, no congelada. forense/prereg-caja/DIN-lote-enif2024-spec-v0_1-PROPUESTA.md con sidecar. Queda bien si contiene, sin remitir a «como el piloto»: universo, unidad y escala en la primera línea · los 14 pares clasificados (5 primarios / 4 de formalidad secundarios / 5 de cuenta_formal aparte, con la razón correcta de cada grupo) · la lista cerrada de contendientes con fórmula cerrada —C2 con IC, persistencia 2021, R1 interacción cruda, R2 encogida (según P2), R3 ajuste proporcional iterativo, L1, L2, M = NO-DERIVABLE con razón— · rejilla y regla de soporte · la regla de la v0.3 con su estadística, su remuestreo y sus tres salidas · cobertura por celda y por par, con el apellido «dentro de ENIF 2024» · B-bis (qué pasa si el falsador no refuta; cuál manda) · los dos oros del COMMIT-1 (reproducir a 1e-9 lo sellado del piloto 1 en localidad × edad; reproducir el C2 ya sellado) · la simulación de potencia sobre pilotos 1 a 3 como pieza del COMMIT-1 · D-22 ampliada como definición de congelado · lo que NO significa. Lo que no puedas cerrar sin microdato (p. ej. umbrales de soporte que dependan de n) se escribe como regla, no como número. P4 · Paquete de los LLM. Prompts de L1 (solo) y L2 (con los marginales públicos de 2024), celdas, número de repeticiones, formato de captura y regla de agregación declarada (mediana, como la spec sellada de L), listos para que mesa los corra por su vía (FP-228: CLI, sin API). Modelo y versión se fijan al correr, con cita del proveedor para el corte. Las capturas se sellan antes del COMMIT-2 mecánico; este acto no las corre.

6 · LATITUD

Decides tú: forma exacta de la tabla dentro del precedente · cómo lees PDF y XLSX · orden · nombres. Replantea y sigue si main se movió, si un id del manifiesto cambió de nombre, o si un descriptor no trae texto de pregunta (usa el cuestionario y dilo). Una pieza que no sale no tumba las otras. Bifurcación que sí cambia el entregable y se pregunta a mesa con opciones y recomendación, siguiendo con lo demás: que el desenlace no sea construible igual ni siquiera en 2018 — deja a R2 en λ = ½ para todo el lote.

7 · PAROS — lista cerrada

a) abrir, descargar o leer microdato de cualquier ola de ENIF, o tabulados de ENIF 2024 (la reserva del lote y la de crédito de ENIF 2024 siguen vivas) · b) abrir o listar el payload de ENVIPE 2026 · c) editar el diseño v0.1 o una firma ya asentada, o alterar un texto verbatim · d) declarar algo congelado · e) entorno sin red a INEGI.

8 · COMPUERTAS

Ninguna: este acto no abre dato, no congela, no adopta, no borra.

9 · PERÍMETRO

Propio: los tres archivos de diseño en forense/prereg-caja/ · data/ahorro-comparabilidad-texto-v1_0.tsv (o el nombre que el índice de infraestructura pida) y su test, cableado en CI · la spec PROPUESTA y su sidecar · el paquete L en forense/ · la fila de firma de la v0.3 · entradas de manifiesto solo si bajas algo que no estaba · nota · cascada. Ajeno: todo data/corrida0/ · tools/ · celdas-D · cualquier spec sellada. Si te encuentras escribiendo fuera de esta lista, PARA.

10 · NO HACE · SUCESORES · AUDITORÍA · CIERRE

No escribe código del medidor · no congela · no corre los LLM · no abre nada. Sucesores: COMMIT-1 del lote en CAJA (dirección lo escribe con lo que P1 y P2 digan) · mesa corre el paquete L · COMMIT-2/3a/3 en otra sesión. Auditoría (la spec afirma sobre México): ahorrar solo por vías informales responde a acceso, ingreso y oferta antes que a preferencia — la spec lo dice en «lo que NO significa»; los ejes localidad y formalidad existen para ver el sesgo de clase y se reportan por eje; universo: adulto elegido de ENIF, sub-representa a quien no decide el dinero del hogar; toda la evidencia es clase (a), dato primario en México; escala: proporción de personas y pp, no comparable contra ENCIG (unidad trámite) ni contra el duelo nacional. ## NO-CORRIDO / RESERVAS · ## CONSUMIDO.

ANEXO A · diseño v0.1, verbatim · sha256 f9ea6d4fb8932d668f4bee808ed34e26d12297871be542457f1a4aa3845ed5a3 · el contenido es lo que está ENTRE las dos líneas marcadoras

<<<ANEXO-A-INICIO>>>
DISEÑO · LOTE DE CRUCES ENIF 2024 · un protocolo, todos los contendientes, una apertura por cruce · v0.1 · 21/sep/2026

Documento de dirección para firma de mesa. No es encargo ni spec: es lo que la spec de PRODUCTO-DINERO tiene que cumplir. Contadores que mueve: cero (diseño). Base leída: origin/main = 4bb29d96. Rótulos: [E] lo corrí · [L] lo leí, cito línea · [S] supuesto que verifica quien congele.

1 · Qué es y para qué

Hoy cada piloto abre un cruce, con diseño propio, y produce 8 a 15 celdas. El piloto 3 lleva seis actos para 15 celdas. Este lote abre los 14 cruces reservados de ENIF 2024 para ahorra_solo_informal con una sola spec y todos los contendientes declarados antes, y contesta tres preguntas de producto a la vez:

¿El intervalo del piso cumple? Hoy C2 cubre 18 de 20 y la persistencia 10 de 20. Con 20 celdas no se puede afirmar que el IC95 cubra lo que promete.
¿Algún retador le gana al piso en algún lado? Es la regla de salida de la capa θ: hoy valor_añadido = 0.
¿Dónde falla? Por segmento: localidad, formalidad, escolaridad — donde un comprador no tiene intuición propia y donde muerde el sesgo de clase.
2 · Qué se gasta y qué se aparta
Se gastan: los 14 pares RESERVADA de ENIF 2024 en el marcador [E]. Ejes y categorías leídos del marcador [E]: sexo 2 · edad 4 · escolaridad 4 · localidad 2 · formalidad 2 · cuenta_formal 2. Son 15 pares posibles y 104 celdas nominales; localidad × edad (8) ya se gastó en el piloto 1 → 96 celdas nominales.
Se apartan, sin abrir: 4 cruces de ENVIPE 2025, 2 de ENCIG 2025, 1 de ENUT 2024 y ENVIPE 2026 entera. Razón: una reserva no caduca para un contendiente mecánico nuestro que todavía no existe (una θ calibrada); sí caduca para un LLM, que acabará leyendo la ola en su entrenamiento — por eso los LLM entran ahora.
Encadenamiento: una ola adjudicada se vuelve historia de la siguiente. ENIF 2024, ya abierta, alimenta a los retadores del próximo levantamiento.
3 · Dos límites que se declaran antes, no después

3.1 · Celdas casi tautológicas. Cruzar «ahorra solo por vías informales» con «tiene cuenta formal» produce celdas que se predicen solas: quien no tiene cuenta difícilmente ahorra por vía formal. Eso es estructura de acceso, no conducta, y contarlas inflaría la exactitud. Los 5 pares con cuenta_formal (28 celdas nominales) se adjudican aparte y no entran a la cifra principal. Quedan 9 pares y 68 celdas nominales en la lectura principal. [S] quien congele confirma, con el texto de la pregunta y el universo de la spec del piloto 1, si la tautología es total o parcial, y lo escribe.

3.2 · Las celdas no son independientes. Los 14 pares salen de una sola muestra; edad × sexo y edad × escolaridad comparten a las mismas personas. La cobertura sobre 68 celdas se reporta tres veces: por celda, por par (9 conglomerados) y junto a las 20 + 15 celdas de los otros dos instrumentos. Lo que este lote puede afirmar es amplitud dentro de ENIF 2024; independencia entre levantamientos solo la dan ENVIPE y ENCIG. Ninguna frase de producto dice «cobertura del 9X %» sin ese apellido.

4 · Contendientes — lista cerrada, todos sellados antes de derivar un solo cruce
#	Contendiente	Clase	De dónde sale
P1	C2: composición de marginales públicos de la misma ola, con IC	piso adjudicado (firma 17/sep)	como en pilotos 1–3
P2	Persistencia: el mismo cruce en ENIF 2021	piso	spec piloto 1 §4.1 [L]
R1	Interacción histórica 2021 cruda sobre marginales 2024	retador	C1a/C1b del piloto 3
R2	R1 encogida hacia el piso, con λ = ½ y λ estimada	retador — familia primaria	S½ / Sλ del piloto 3
R3	Ajuste proporcional iterativo: marginales 2024 sobre tabla 2021	retador	nuevo; mecánico
L1	LLM solo	retador	spec piloto 1 §4.3 [L]; tubería de capturas existente
L2	LLM con corpus (recibe los marginales 2024)	retador	ídem
M	Emisor del motor / matriz B(x)·h_r	se declara; hoy INEJECUTABLE / NO-APLICA (spec piloto 1 §4.4–4.5 [L])	si MOTOR entrega una θ candidata antes del COMMIT-1, entra; si no, el silencio se escribe como NO-EMITE

Modelos, versiones, temperatura y prompts de L1/L2 se congelan en el COMMIT-1. Las capturas se sellan antes de que exista el COMMIT-2 mecánico.

5 · Regla de victoria y pre-registro de falsación (B-bis) — antes de ver el dato
Comparación primaria, una sola: piso C2 contra la familia R2, sobre las celdas con soporte de los 9 pares principales. Un retador vence si gana en ≥ ¾ de las celdas puntuadas y el IC95 de ΔMAE despeja 0.5 pp (regla del piloto 3, verbatim). Un punto que cumple con un IC que no despeja no adjudica: propuesta con reserva (A-bis).
Todo lo demás es secundario y se rotula así: R1, R3, L1, L2, M, los 5 pares de cuenta_formal. Con ocho contendientes y 96 celdas alguno gana por azar; por eso no adjudican solos.
Cobertura: se reporta la del IC95 de C2 y la de persistencia, por celda y por par. Se declara de antemano qué la refutaría: cobertura de C2 por par < 80 % en la lectura principal → el argumento de producto «sé cuánto me equivoco» queda acotado a los cruces ya vistos y no se generaliza.
Si el falsador no refuta: corroborada (nadie vence, cobertura ≥ 80 %) · acotada (vence alguien solo en un eje: se nombra el eje) · falsador débil (≥ ⅓ de las celdas sin soporte). Si caben dos, manda falsador débil.
Lo que NO significa, escrito ya: que el piso gane no dice que la conducta sea estable por cultura; dice que la interacción entre ejes aporta poco sobre los marginales en este levantamiento. Ahorro informal responde a acceso, ingreso y oferta antes que a preferencia (§3 de las instrucciones). Universo: adulto elegido de ENIF; sub-representa a quien no decide el dinero del hogar.
6 · «Congelado», con lo que costó aprender
corrida0 preflight VERDE sobre el commit final del COMMIT-1 con origin/main fusionado. Ningún input con hash sobre un archivo vivo: constancias.
Ensayo de sellabilidad: _valida_outputs sin problemas en cada rama terminal —todas con soporte, soporte parcial, fuera de soporte global, cero puntuadas, celda rara— sobre sintético. Todo id que el código pueda emitir nulo por lectura estática está declarado.
Oro que ya existe: el código genérico, corrido sobre localidad × edad, reproduce a 1e-9 las emisiones y la R selladas del piloto 1. Es retrospectivo, no gasta nada, y prueba el conducto de punta a punta con corrida0 run.
Los CALC encadenados traen previsto su COMMIT-3a.
7 · Secuencia y quién

Tres pasos, una apertura por cruce. (a) NUBE: spec humana + capturas L1/L2 selladas. (b) CAJA: COMMIT-1 — código genérico sobre (instrumento, par), spec.yaml, los cuatro puntos de §6. (c) CAJA, otra sesión: COMMIT-2 emisiones mecánicas → 3a → COMMIT-3, los 14 pares en una corrida. Dueño: PRODUCTO-DINERO — esto es su «piloto de ahorro», ensanchado. MOTOR recibe la invitación de la fila M. TUBERÍA no está en el camino crítico: si corrida0 ensayo existe a tiempo se usa; si no, el ensayo va como script, como en el v1.3.

8 · Firma que se pide

«Se aprueba el lote: los 14 cruces reservados de ENIF 2024 para ahorra_solo_informal se abren una vez, bajo una sola spec, con la lista cerrada de contendientes de §4 sellada antes. Comparación primaria: C2 contra la familia encogida, regla de ¾ e IC que despeje 0.5 pp; lo demás es secundario. Los 5 pares con cuenta_formal se adjudican aparte. La cobertura se reporta por celda y por par, con el apellido "dentro de ENIF 2024". Se apartan sin abrir ENVIPE 2025, ENCIG 2025, ENUT 2024 y ENVIPE 2026. "Congelado" es §6 completo. cuenta_gen2 = SI para las corridas del lote, sea cual sea el veredicto. Dueño: PRODUCTO-DINERO.»

9 · Auditoría (§5 de las instrucciones)

¿Estructura confundida con cultura? — el riesgo central; atendido en 3.1 y 5. ¿Sobre-generalización desde clase media urbana? — los ejes localidad y formalidad existen para verlo; se reportan por eje. ¿Marcos importados? — ninguno: todo es dato primario en México, clase (a). ¿Qué cambia con foco rural/popular? — menor de 15 000 y sin seguridad social son donde se espera más error; se reporta aparte. ¿Afirmación escrita a mano? — las cifras 14, 96, 68 y 28 se derivaron hoy del marcador; 18/20 y 10/20 vienen del tablero derivado. ¿Escalas? — proporción de personas, error en pp; no se compara contra el duelo nacional ni contra ENCIG (unidad trámite). Falsabilidad del propio diseño: si el oro de §6.3 no reproduce al piloto 1, el código genérico no es el mismo procedimiento y el lote no se lanza.
<<<ANEXO-A-FIN>>>

## NO-CORRIDO / RESERVAS

Cuatro filas. `forense/no-corrido.tsv`, ids `NC-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01` a `-04`, todas `ABIERTA`.

**1 · P4 — las capturas de `L1` y `L2`.** El paquete queda escrito y sellado (`forense/prereg-duelo-v2/PAQUETE-L-LOTE-ENIF2024-v0_1.md`: prompts verbatim, 44 celdas, `k = 8`, formato de captura y agregador declarados), pero las 704 llamadas no se corren.
**Por qué:** `DIFERIDO-A:mesa corre el paquete L por CLI sin API (FP-228)`; el propio encargo lo declara en §10, «no corre los LLM».
**Impacto:** `L1` y `L2` no tienen emisiones. Son retadores **secundarios**, así que no bloquean la adjudicación primaria (`C2` contra `R2`) ni mueven ningún contador; bloquean el bloque secundario del COMMIT-2.
**Sucesor:** mesa (corrida `L`) → COMMIT-2 del lote.

**2 · P3 — `spec.yaml`, la capa ejecutable de D-15.** La spec sale sólo en su capa humana y como `PROPUESTA`. La rejilla de celdas (tramos de `edad` y de `escolaridad`), el umbral de soporte, la semilla y el número de remuestras quedan escritos **como regla y no como número**.
**Por qué:** `FUERA-DE-PERÍMETRO:del COMMIT-1 del lote, en CAJA` — el encargo §10 se lo asigna a dirección «con lo que P1 y P2 digan», y §5-P3 ordena expresamente escribir como regla lo que no se pueda cerrar sin microdato.
**Impacto:** ninguna corrida puede citar esta spec como congelada mientras diga `PROPUESTA` en el nombre. Cero contadores afectados.
**Sucesor:** COMMIT-1 del lote ENIF 2024 (CAJA).

**3 · P2 — `R2` con `λ` estimada.** Queda en `λ = ½` fija para los catorce pares. La rama de `λ` estimada exige admitir 2018 bajo un desenlace `D8` armonizado y recortar 2021 a 18-70: es una bifurcación que cambia el entregable.
**Por qué:** `DECISIÓN-DE-MESA-PENDIENTE`.
**Impacto:** `R2` entra al lote con el mismo encogimiento fijo que ya midió el piloto 3 (`S½`). **No bloquea el COMMIT-1:** la firma F2 ya dictamina `λ = ½` para el caso «solo una ola comparable», y el caso se cumple. Si mesa toma la Opción B, la spec se enmienda **con archivo propio antes del COMMIT-1**, nunca in situ.
**Sucesor:** mesa — opciones A/B/C y recomendación (la A) en `forense/notas/2026-09-21-lote-enif2024-comparabilidad-y-R2.md` §5. Ranura de mesa asentada (A.12) como `FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-02`, `ABIERTA`.

**4 · P0 — el sha256 declarado del Anexo A.** El contenido entre las dos líneas marcadoras da `bd1dcfd89a108cdd…` (o `5dff45e67558d1c2…` conservando el salto de línea inicial), no el `f9ea6d4fb8932d66…` que el encargo declara. El texto viajó por el canal de chat, que renormaliza los tabuladores de las tablas del §4 del diseño. **No se «arregló»:** el encargo ordena reportarlo y seguir, y eso se hizo.
**Por qué:** `PARO-PREMISA`.
**Impacto:** el testigo `f9ea6d4f…` queda **VENCIDO EN ALCANCE** (A.10), no refutado y no borrado. El v0.1 archivado lleva su propio sidecar `bd1dcfd8…` y **no se edita**. Ningún contador afectado; el contenido del diseño está íntegro.
**Sucesor:** `SIN-ASIGNAR` — si mesa conserva el original byte a byte en otro sitio, se re-sella ahí; el archivado no se toca.

## CONSUMIDO

Ejecutado por `ACTO GEN2-DIN-LOTE-ENIF2024-A`, 21/sep/2026, rama `acto/gen2-din-lote-enif2024-a`, entorno **NUBE `milpa-inegi`**, Opus 5, **MODO ABIERTO**, **COMPUERTA: ninguna**. **PR #967** — https://github.com/Josanoforo/Modelado-Mexicano/pull/967

`ADR-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01` (raíz de acto; `a98a` = 4 hex del commit de 0-bis `a98a483`) en `canon/gobernanza-v1_15.md`, con su fragmento en `canon/L0/ADR-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01.md`. Rótulo censado en `canon/registro-rotulos.tsv`. Firma de la enmienda v0.3 asentada como `FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-01` (`FIRMADA`); ranura de la bifurcación como `FP-260921-GEN2-DIN-LOTE-ENIF2024-A-a98a-02` (`ABIERTA`). Cuatro filas `NC` abiertas. `python3 tests/check.py --baseline --parallel`: **LÍNEA BASE VERDE**. `cuenta_gen2 = NO-APLICA`; cero microdato abierto; cero contadores movidos.

**Adendas de mesa a este encargo: ninguna.**
