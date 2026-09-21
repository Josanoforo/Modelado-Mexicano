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
