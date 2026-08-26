# Paquete de codificación — segundo codificador

**No leas ningún otro archivo de este repositorio antes de terminar.** Este paquete es
auto-contenido a propósito: trae las tres piezas que necesitas y nada más. Cualquier
documento adicional sobre este material contiene resultados previos que invalidarían
tu codificación como codificación independiente.

Contiene exactamente tres piezas: **(1)** el esquema de codificación, **(2)** las 12
transcripciones íntegras, **(3)** el código de contexto de cada unidad, ya asignado por el
corpus — no se te pide inferirlo.

## Qué se te pide

Clasifica cada una de las 12 unidades en **dos niveles**, aplicando el esquema de abajo:

- **Nivel 1:** `DIRECTO` · `INDIRECTO` · `NO-RECHAZO`
- **Nivel 2:** `DIRECTO` · `EXCUSA` · `APLAZAMIENTO` · `ALTERNATIVA` · `EVASION` · `NO-RECHAZO`

Devuelve una tabla de 12 filas con `unidad · Nivel 1 · Nivel 2`. Si quieres, añade una
columna de nota breve por unidad; es útil pero opcional. **No consultes a nadie ni
discutas ninguna unidad antes de entregar la tabla.**

---

## El esquema de codificación

**2.1 · Unidad de análisis.** El **turno de rechazo**, no la cadena léxica. Cada turno se descompone en:
- **Acto nuclear (*head act*):** el segmento que realiza el rechazo en sí — lo que, si se quitara, dejaría la interacción sin rechazo cumplido.
- **Adjuntos:** los segmentos que rodean al acto nuclear sin realizarlo (razones, disculpas, atenuadores, marcadores de apertura/cierre).

**2.2 · Regla de clasificación, sobre el acto nuclear únicamente:**
- **Directo:** el acto nuclear contiene una negación performativa explícita y no mitigada (`no`, `no puedo`, `me niego` funcionando como la propia realización del rechazo, no incrustada en una excusa).
- **Indirecto — cuatro subtipos, tomados del marco del ancla, cada uno con su regla de disparo:**
  - **Excusa:** el acto nuclear se realiza dando una razón externa que hace el rechazo implícito (*"tengo otra cita"*).
  - **Aplazamiento:** el acto nuclear pospone la decisión sin negar (*"lo pienso y te digo"*).
  - **Alternativa:** el acto nuclear ofrece una opción distinta a cambio del rechazo (*"mejor el jueves"*).
  - **Evasión:** el acto nuclear no responde directamente a la petición/invitación/sugerencia (cambio de tema, respuesta tangencial).

**2.3 · Regla explícita para excusas mitigadas — el defecto 1.1 de `hitoD-R10_1-defecto-spec-v1_0.md`.** Un acto nuclear que combine una negación (`no puedo`, `no, no`) con una razón externa en la misma cláusula o adyacente (*"no, pues no, no me puedo quedar [porque tengo otra cita]"*) se codifica **indirecto por excusa**, no directo. La negación aislada solo cuenta como acto nuclear directo cuando **no** va acompañada de razón externa en el mismo turno de rechazo.

**2.4 · Regla para negaciones que no son la cabeza — el defecto 1.2.** Una cadena de negación (`no puedo`, `no voy`, …) que se refiera a un objeto **distinto** del acto que se está codificando (p. ej. una negación sobre otra decisión mencionada dentro del mismo turno) **no se cuenta**. El codificador debe identificar primero el objeto del rechazo (qué petición/invitación/sugerencia se está rechazando) y clasificar la cabeza que responde a **ese** objeto, no la primera cadena de negación que aparezca en el texto.

**2.5 · Regla para interacciones sin rechazo consumado — el mismo defecto, su otra cara.** Una transcripción donde el interlocutor termina aceptando, aplazando sin resolver hacia el rechazo, o cuya interacción no cierra con un acto de rechazo identificable (`Rechazo 10` es el caso ya documentado: la interacción cierra con *"si salgo antes, pues llego"* / *"te espero"*) se marca **`NO-RECHAZO`** y se **excluye del denominador** de la tasa directo/indirecto de ambos brazos. No se cuenta como directo, indirecto, ni se descarta en silencio: se reporta con su motivo, por brazo, junto a la tasa.


---

## Las 12 unidades

Cada unidad trae su **código de contexto** (`+P` / `−P`), tomado del corpus. Es un dato
del escenario, no algo que debas evaluar ni que deba influir en tu clasificación.

### U01

- **escenario:** Rechazos 1-2 — Estudiante y asesor: Un estudiante rechaza la sugerencia del asesor de tomar una clase. (+D, +P
- **código de contexto:** `+P`
- **situación:** El estudiante (Lisandro) rechaza la sugerencia de su asesor (René)

```
   Estudiante:       Eh, disculpe profesor, este vengo a mostrarle la tira de calificaciones que había hecho para este semestre
   Asesor:            ¿Cuáles son las materias que has seleccionado para cursar este semestre?
   Estudiante:      Eh, este, es, es este Lógica Formal, Filosofía Antigua, este, Teoría del Conocimiento y Introducción a la Filosofía.
   Asesor:           Bien, me parece interesante lo que tú has seleccionado, mas sin embargo te sugiero que en lugar de la última materia que mencionas, tomes la materia de redacción; es una de las materias que te van a ayudar a tener una buena formación y sobre todo a entender todas las otras materias que vas a a cursar.
   Estudiante:       Hijo, pero en este caso como ya hice mi tira, o sea ya el tiempo no me lo permite
   Asesor:           No habría ningún problema, nosotros podríamos platicar en servicios escolares para que se hiciera la modificación en tu asignatura.
   Estudiante:      Bueno, pero, ps, pues este, tendría que pensarlo también, pero, este, tendría uno que ver primero también si, me dan permiso allá y, ya si la tengo que tomar, pues la tomo
   Asesor:            Bueno, entons’ lo analizamos conjuntamente ¿te parece?
   Estudiante:      Sí.
```

### U02

- **escenario:** Rechazos 1-2 — Estudiante y asesor: Un estudiante rechaza la sugerencia del asesor de tomar una clase. (+D, +P
- **código de contexto:** `+P`
- **situación:** El estudiante (Omar) rechaza la sugerencia de su asesor (René)

```
   Asesor:              Buenas tardes, Omar.
   Estudiante:        Buenas tardes, Profesor.
   Asesor:            ¿Ya estás preparado para analizar las las materias que vas a cursar este semestre?
   Estudiante:       Sí, de hecho, ya tengo un plan en el cual este tengo escritas, registradas las materias que pienso tomar este semestre.
   Asesor:            ¿Como cúales serían?
   Estudiante:      Está Literatura Mexicana, Literatura Universal, Morfosintaxis I, y este, Fonología y este Literatura Espanola del Siglo XVIII.
   Asesor:            O.K., de acuerdo al plan de estudios, tú también tenías que haber llevado algunas materias relacionadas con este, teoría del conocimiento, este, como no has cumplido con todos estos cursos, yo te invitaría que antes de que tomaras algunas de estas materias que tú ya has mencionado, selecciones bien y hagas un cambio por esto que te estoy mencionando, porque te ayudaría bastante en tu formación, y sobre todo en el contexto en el que vas a entrar en este momento, relacionado con el conocimiento de la literatura.
   Estudiante:       Bueno, pero, no no tendría que ser necesariamente o forzoso y ahorita en este semestre, ¿o sí?
   Asesor:            De alguna manera sería, no tanto forzoso, pero sí necesario en cuanto a tu propia formación, eso te ayudaría mucho a tener claridad en el trabajo que vas a realizar.
   Estudiante:      Y ¿qué posibilidades hay de que la pueda yo posponer?, digamos para el semestre entrante, porque ahorita de hecho el tiempo que tengo está saturado y se me haría un poco, se me complicaría tomar otra materia más
   Asesor:            Te parece que lo analicemos con calma y lo platicamos en otra ocasión.
   Estudiante:      Me parece bien.
```

### U03

- **escenario:** Rechazos 3-4 — Jefe y empleado: Un empleado rechaza la petición del jefe de quedarse más tiempo en el trabajo (+D, +P)
- **código de contexto:** `+P`
- **situación:** El empleado (Lisandro) rechaza la petición de su jefe (René)

```
   Jefe:                 Lisandro, buenas tardes.
   Empleado:       Buenas tardes, jefe
   Jefe:                 Este, ¿te acuerdas que habíamos perdido algún, algunos libros porque no los encontraban en el correo?
   Empleado:       Ajá
   Jefe:               Bueno, pues, estos ya llegaron y también tienes conocimiento que son urgentes, ¿no? para que los alumnos puedan usarlos el próximo lunes, pues yo te pido de favor que te quedes dos horas más para que los puedas, este, organizar y clasificar.
   Empleado:       Pero, es que no me puedo quedar porque tengo otra otra este, cita, otra una cita digamos, y este tengo que llegar allá a las siete y media y no, pues no, no me puedo quedar.
   Jefe:                 Híjole, lo que pasa es que sí mi interesaría que lo hicieras, por favor.
   Empleado:          Hijo, pues es que también el transporte es el que no me dejaría quedarme
   Jefe:               Bueno el lunes tenemos que tener estos materiales y esperamos que los concluyas
   Emplado:        Pero, (...) es que le digo que esas dos horas no me puedo quedar, o sea, es que no es tanto que me vaya a pagar las horas, sino la situación para irme
   Jefe:                Pues gracias, Lisandro
   Empleado:       Sí, pues no se pudo.
```

### U04

- **escenario:** Rechazos 3-4 — Jefe y empleado: Un empleado rechaza la petición del jefe de quedarse más tiempo en el trabajo (+D, +P)
- **código de contexto:** `+P`
- **situación:** El empleado (Omar) rechaza la petición de su jefe (René)

```
   Jefe:                 Omar, buenas tardes.
   Empleado:       Buenas tardes, jefe
   Jefe:                Este, mira, te acuerdas que había un paquete de libros extraviado
   Empleado:       Sí,
   Jefe:                Y apenas lo encontraron en el correo y me lo remiten; y tú sabes muy bien esto se tenía que haber ya clasificado y organizado para que los alumnos pudieran hacer uso de ese material, yo te pediría de favor que te quedes hasta las nueve de la noche para que podamos trabajar esto este material, y el lunes ya aparezca en los estantes, y en este caso los alumnos puedan hacer uso de ellos.
   Empleado:       ¿Hasta las nueve?
   Jefe:                Hasta las nueve.
   Empleado:       Umm, lo que pasa que es que por lo regular a las ocho y media sale el último autobús a donde vivo, pero ?qué le parece, si nos quedamos a hacer, digamos, la mitad y el lunes tempranísimo estaría yo aquí para continuar con lo que falta. Podría ser una posibilidad.
   Jefe:                Este, ¿no podríamos, llegar hasta las nueve, entonces?
   Empleado:       Le digo, el problema no es, no es de ganas, sino sería de problema de transporte
   Jefe:                Bueno, entos’ así le hacemos,
   Empleado:       ¿Sí?
   Jefe:                =avanza lo más que puedas, y el lunes terminas
   Empelado:       Bueno
   Jefe:                Gracias
   Empleado:       A usted
```

### U05

- **escenario:** Rechazos 5-6 — Jefe y empleado: Un empleado rechaza la invitación del jefe de ir a una cena (+D, +P)
- **código de contexto:** `+P`
- **situación:** El empleado (Lisandro) rechaza la petición de su jefe (René)

```
   Jefe:              Lisandro, buenas tardes, tengo una noticia agradable
   Empleado:       Buenas tardes, señor
   Jefe:              Este mira, despúes de tantas actividades que hemos realizado conjuntamente y favorablemente la empresa, pues, nos ha premiado a los dos, yo de alguna forma voy a incorporarme a una dirección general en otra instancia en otro lugar, eso me permite pues sentirme agusto por estar en donde estoy actualmente y al mismo tiempo pues tengo ganas de de festejar este nuevo puesto y me gustaría que lo compartieras conmigo el próximo sábado a las 7 de la noche en uno de los restaurantes aquí abajo que se llama El Zócalo Restaurán de tal manera que podamos convivir conjuntamente esta, este nuevo puesto y además que sirva también de despedida, porque no voy a tener la oportunidad de hacerlo más adelante, ¿no?, entonces yo te agradecería que me acompañes este sábado a las 7 de la noche en este restaurán para festejar lo que implica el nuevo puesto y una despedida
   Empleado:       Y bueno, es que o sea la situación es que, discul-, discúlpeme, pero yo no puedo ir porque tengo otro compromiso el sábado igual a esa misma hora, y por lo tanto, pues no voy a poder asistir, por más que intente cancelarlo o algo así, no voy a poder asistir
   Jefe:                Entonces no sería posible
   Empleado:       No, lamentablemente no va a ser posible, discúlpeme pero no, no va a ser posible.
   Jefe:                 Bueno, será en otra ocasión.
   Empleado:       Gracias, discúlpeme de todas maneras
```

### U06

- **escenario:** Rechazos 5-6 — Jefe y empleado: Un empleado rechaza la invitación del jefe de ir a una cena (+D, +P)
- **código de contexto:** `+P`
- **situación:** El empleado (Omar) rechaza la petición de su jefe (René)

```
   Jefe:                Omar, buenas tardes, ¿cómo estamos?
   Empleado:       Buenas tardes, señor.
   Jefe:                Fíjate que después de todo el trabajo que hemos realizado y lo favorable que nos ha permitido la empresa desarrollarnos en, en la misma, este, pues les ha gustado el trabajo que hemos hecho y de alguna manera nos rencompensado recompensado con, pues tener otro puesto y entons’ en este caso pues la verdad que me interesaría poderlo compartir con contigo y con los tros companeros a través de una fiesta que vamos a llevar a cabo el día 7, perdón, el próximo sábado a las 7 de la noche en un restaurán aquí abajo en el centro de la ciudad de Tlaxcala, que sería en La Avenida y ahí pues, mi intención es fundamentalmente que compartamos ¿no? el y festejar de alguna manera este nuevo puesto que me han designado y al mismo tiempo el hecho de que tú puedas posiblemente también, este, ocupar el lugar que yo tenía en este en este momento la empresa, ¿no?
   Empleado:       Bueno, pues, en primer lugar felicidades y en segundo lugar le voy a pedir que me disculpe porque no puedo, no voy a poder asistir a su fiesta, eh, es un gran honor para mí ser un invitado y que Ud. me recuerde, pero tengo planes con la familia, y son planes que ya veníamos desarrollando de tiempo atrás.
   Jefe:                Pues, me me hubiera gustado que estuvieras con nosotros, pero si no es factible, pues gracias por el apoyo que me diste aquí en la empresa.
   Empleado:       Bueno, de nada y creo que no, no creo, creo que de esto no será la última vez que nos podamos juntar, um, hacer una reunión para una cena, creo que puede haber muchas más adelante y que tenga mucha suerte.
   Jefe:                Gracias, hasta luego.
   Empleado:       Pásele.
```

### U07

- **escenario:** Rechazos 7-8 — Amigos: Un amigo rechaza la petición de otro de pedir prestado los apuntes de una clase (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Lisandro) rechaza la petición de otro amigo (Jorge)

```
   Jorge:               ¿Qué tal, como estás?
   Lisandro:         ¿Qué hubo?
   Jorge:               Oye, un favorzote
   Lisandro:         A ver
   Jorge:              Mira, este, lo que pasa es que he faltado a algunas clases y ya me urgen los apuntes y quería ver si los tienes, oye, ¿qué onda?, préstamelos, ¿no?
   Lisandro:         Ah ha, es que lo que pasa que, este, no los traje ahora.
   Jorge:              Híjole, no me quedes mal, mira, este, deveras me urgen.
   Lisandro:         No, sí, es que, este, ahorita sí deveras no los traigo, es que como vemos otras materias, y no los traje, y este, me los hubieras pedido ayer, sí los traigo, si te los presto.
   Jorge:              A mí me urgen para manana, pero si me los puedes prestar mañana, nada más les saco copia y y te los devuelvo, ?cómo ves?
   Lisandro:         Ajá, bueno, mañana solamente que los traiga yo, pero hasta la tarde, bien en la tarde
   Jorge:               ¿Como a qué hora vienes para que te busque?
   Lisandro:         Como a las cinco
   Jorge:               Bueno, ¿dónde dónde nos vemos?
   Lisandro:         Pues aquí en la escuela
   Jorge:               Sale, pues, nos vemos después
   Lisandro:         Bye
```

### U08

- **escenario:** Rechazos 7-8 — Amigos: Un amigo rechaza la petición de otro de pedir prestado los apuntes de una clase (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Omar) rechaza la petición de otro amigo (Jorge)

```
   Jorge:               ¿Qué tal? ¿Cómo estás?
   Omar:              Pues bien.
   Jorge:               Oye mira fíjate que necesito un favorzote
   Omar:              A ver.
   Jorge:              Mira, como has visto, he faltadoa a algunas clases y este y el examen es es ya mañana, entonces, ¿qué onda? préstame tus apuntes, ¿no?
   Omar:             Eh, pero también tengo que estudiar pero, no sé, no sé, tal vez podríamos estudiar juntos o porque no le sacas una copia para que tú estudies y yo pudiera estudiar
   Jorge:             Pefecto, sí, necesito que me los prestes para sacarle nada más una copia y te los devuelvo rápido.
   Omar:              ¿Si?
   Jorge:               Sí
   Omar:              Pos órale
   Jorge:              Okey, gracias.
```

### U09

- **escenario:** Rechazos 9-10 — Amigos: Un amigo rechaza la invitiación de otro a su fiesta de cumpleaños (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Lisandro) rechaza la invitiación de otro amigo (Jorge)

```
   Jorge:               ¿Qué onda? ¿cabrón? ¿cómo estás?
   Lisandro:          Qué onda, yo estoy bien, Tú, ¿cómo estás?
   Jorge:               Bien bien, oye, qué bueno que te veo, ¿dónde te habías escondido?
   Lisandro:         Pues, aquí he andado en la escuela:
   Jorge:               No te había yo visto. Pues ya cuanto tiempo que no nos vemos
   Lisandro:         Sí, pues aquí andamos en la escuela
   Jorge:               Oye, ¿qué crees?
   Lisandro:         A ver
   Jorge:               Mira, fíjate que el, voy a cumplir años el viernes próximo y voy a hacer una fiesta a las ocho en casa, y pues como siempre estás cordialmente invitado, ¿qué onda? Pues te espero, ¿no?
   Lisandro:         Híjole, es que no pue:do
   Jorge:               ¿Por qué, ¿noo? no me quedes mal
   Lisandro:         Es que, te acuerdas la chava esa que la otra vez la andaba yo tirando la onda, pues se me hizo y me dijo que la fuera a ver a su casa
   Jorge:              Mira, no hay problema, no te preocupes, mira, ve por ella y llévala a la fiesta, no, no hay ningún problema
   Lisandro:           Pero falta que ella quiera también
   Jorge:              Pero, es que no puedes faltar, mira, es mi fiesta de cumpleaños, no todos los días cumplo años, mira no seas así
   Lisandro:         Sí, pero la bronca es te digo allá, y hay que ir a ver..
   Jorge:              Híjole, no:, mejor la ves mañana, o pasado, o más bien un día después.
   Lisandro:         Sí, la bronca es avisarle, pero no tiene teléfono
   Jorge:               Híjole, bueno, como puedas, yo te espero ahí a las 8, ya sabes dónde vivo
   Lisandro:         Ahí, si si me tengo tiempo, pues allá caigo, y si no, no voy a poder, de todas maneras te voy a decir que no, la verdad que no puedo, así te digo que no voy a poder ir
   Jorge:             Bueno, ni hablar
```

### U10

- **escenario:** Rechazos 9-10 — Amigos: Un amigo rechaza la invitiación de otro a su fiesta de cumpleaños (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Omar) rechaza la invitiación de otro amigo (Jorge)

```
   Jorge:               ¿Qué onda? canijo, ¿Cómo has estado?
   Omar:               Pues bien, bien bien mira aquí andamos.
   Jorge:              Oye, ¿qué onda?, fíjate que cumplo años el viernes. Y ya sabes, voy a hacer un fiestón en mi casa y este pues estás invitado.
   Omar:              Está bien, ¿no?, va a está super.
   Jorge:             Sí, ¿qué onda? te espero, ¿no?, va a ser a las ocho en mi casa, ya sabes dónde yo vivo.
   Omar:              Híjoles, ¿a las ocho?
   Jorge:               Sí, va a ser a las ocho.
   Omar:              ¿No puedo ir antes?
   Jorge:              Híjole, pues si empieza a las ocho, solamente que ayudes a ayudar a arreglar todo el relajo
   Omar:              Lo que pasa es que tengo una cita con el doctor, el dentista
   Jorge:              Muy bien
   Omar:              Y no sé si pueda llegar a las ocho, pero si no se tarda, pues, si puedo voy.
   Jorge:              No pues, mira, cambia la cita, no seas así
   Omar:              No puedo, lo que pasa es que son tres veces que la retraso.
   Jorge:              Híjole, bueno te espero a las nueve, ¿qué te parece?
   Omar:              Te digo, mira, seguro no es, pero que te parece si si salgo antes, pues llego por allá, nomás que los reventones se acaban temprano
   Jorge:              Exactamente, ya sabes cómo es la fiesta
   Omar:              Así es
   Jorge:              Bueno, sale, entons’ te espero, ¿eh?
   Omar:              Órale
   Jorge:              Órale
```

### U11

- **escenario:** Rechazos 11-12 — Amigos: Un amigo rechaza la sugerencia de otro de ir a un bar (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Lisandro) rechaza la sugerencia de otro amigo (Jorge)

```
   Jorge:           Oye, ¿qué onda?, bueno, este fíjate que después de platicar, veo que nos late el mismo tipo de música, y precisamente hoy, es más, en diez minutos, que desafortunadamente ahorita empieza la clase, va va a tocar el grupo, este, aquí abajo en los portales, del portal chico, se va a presentar este Par de Aces, que ves que nos late ese tipo de música, ¿qué onda? Pues vamos, tengo dos boletos, vienen las viejas, y ahí vienen las chavas, y este aparte pues ahí están unas chelas, ¿qué onda? vamos.
   Lisandro:       No, pues es que, fíjate, todavía no acabo de comer, y la clase empieza en diez minutos.
   Jorge:            Es es lo que decía yo, peor mira, este, vamos un rato, mira, además nada más nos vamos a voalr una clase, nada más es esta y vamos para ya, mira, es buena música, ¿pues cuándo nos volvemos a ver?
   Lisandro:       Sí, pero qué tal si el maestro nos, por la falta esa no nos deja hacer examen?
   Jorge:            Oye, pues vale la pena:, ¿lo buena onda quién nos lo quita?
   Lisandro:       Bueno, eso sí, ¿pero la falta quién te la quita?
   Jorge:            Hí:jole, no, ¿qué onda? no seas así
   Lisandro:       Me cay que no puedo, guey, por más que intente, no.., y luego ves que yo soy medio seso, pues no me gusta salir de mi clase
   Jorge:            Hijo, bueno, sale, ni hablar, nos vemos
   Lisandro:       Órale que te vaya bien
```

### U12

- **escenario:** Rechazos 11-12 — Amigos: Un amigo rechaza la sugerencia de otro de ir a un bar (-D, -P)
- **código de contexto:** `−P`
- **situación:** Un amigo (Omar) rechaza la sugerencia de otro amigo (Jorge)

```
   Jorge:               Oye, ¿qué crees?
   Omar:              ¿Qué pasó?
   Jorge:              Fíjate que después de estar platicando y todo esto, aquí abajo ahorita, en diez minutos, fíjate que va a tocar un grupo, este, musical, que se llama Par de Aces, y pues ves que nos late esta música, ¿qué onda? vamos ¿no?, nos volamos esta clase y este vamos a a dar una vuelta ¿no?, un rato.
   Omar:              Pues, suena bien, pero es que yo voy restrasado en esta materia, te imaginas si me la vuelo, me voy a atrasar más.
   Jorge:              No hombre, mira nada más te vuelas esta clase y este, bueno, nos volamos esta clase y vamos a la, al al concierto.
   Omar:              Pero va a tardar más de hora y media el concierto
   Jorge:              Sí
   Omar:              Mejor, ¿qué te parece si entramos en la clase y salgo... o corre, o ve tú y yo te alcanzo, termino mi clase, y me voy para allá?
   Jorge:             ¿Pero y si no llegas?
   Omar:               No, sí=
   Jorge:            Yo no tengo con quién ir, vamos, además nos late esta música
   Omar:            Ps, si, tú sabes que nos gusta pero, primero los deberes, ¿no crees?
   Jorge:            Pues, sale, entons’ te espero.
   Omar:            Órale.
```

---

## Tabla para devolver

| unidad | Nivel 1 | Nivel 2 | nota (opcional) |
|---|---|---|---|
| U01 |  |  |  |
| U02 |  |  |  |
| U03 |  |  |  |
| U04 |  |  |  |
| U05 |  |  |  |
| U06 |  |  |  |
| U07 |  |  |  |
| U08 |  |  |  |
| U09 |  |  |  |
| U10 |  |  |  |
| U11 |  |  |  |
| U12 |  |  |  |

