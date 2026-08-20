# ADV-1 · Demolición del duelo L vs M

> **Nota de procedencia (20/ago/2026 · `ACTO SELLA-ADV` T1):** entregable de revisión adversarial senior, sesión limpia fuera del proyecto, autodeclarado en su propio cuerpo ("sesión limpia · 19-ago-2026", "Entregable para CAREO previo al sellado de APERTURA v1.2"). Insumo `ADV-1` del careo adjudicado en `forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md` §A. Modelo autor: no autodeclarado en el cuerpo; CAREO §Insumos cita dos corridas `ADV-1 (Opus/Fable)` sin mapear archivo↔modelo — no se asigna aquí para no fabricar procedencia (ver `forense/hallazgos.md`). sha256 del adjunto verificado contra el paquete de lanzamiento del 19/ago/2026: `064eaba2392d967c73cd2022abb291c4b343a54b1bc31e54c7949ec7616375c9`, coincidencia exacta. Archivado verbatim, sin edición de cuerpo; a partir de este commit es base de evidencia fechada del programa y no se retoca (mismo patrón que `compass-4`, doctrina `FP-57`/`ADR-114`).

**Revisión adversarial senior de diseño de evaluación** · sesión limpia · 19-ago-2026
Entregable para CAREO previo al sellado de APERTURA v1.2

---

## 0. Veredicto en una línea

El diseño es **fuerte en procedencia y débil en inferencia**. Toda la disciplina cara —espec congelada, dos commits, universos declarados, clases de procedencia, escala de falsación— protege contra el fraude y contra el auto-engaño *narrativo*, y no compra nada contra el auto-engaño *estadístico*. Con N=12 y criterio "≥7 de N", el diseño declara un ganador con probabilidad ≈77% **cuando no existe ninguna diferencia real entre L y M**. Y las tres vías de contaminación (memorización de tabulados, circularidad dentro-de-muestra, corpus escrito sobre la literatura que resume a R) están declaradas como preocupación pero no controladas por ningún mecanismo del diseño.

19 hallazgos: **11 ROMPE-DISEÑO, 7 DEBILITA, 1 COSMÉTICO**. La buena noticia: los 11 ROMPE-DISEÑO se arreglan con **6 mecanismos**, no con 11 parches, y cuatro de esos seis son baratos. El caro es uno solo: el criterio de admisión de preguntas, que probablemente mate la mitad del set v1 actual.

---

## A. Tabla de hallazgos

### A.0 · Resumen

| # | Superficie | Severidad | Costo del arreglo | Mecanismo v2 |
|---|---|---|---|---|
| 1 | Contaminación de L por memorización de tabulados | ROMPE-DISEÑO | 2 ses. | M1 |
| 2 | Circularidad de M (R de la ola que parametrizó la celda) | ROMPE-DISEÑO | 1 ses. + regenerar set | M1 |
| 3 | No-independencia L↔R de 2.º orden vía literatura | ROMPE-DISEÑO | 1 ses. + 15 min/pregunta | M1 |
| 4 | Marcador sin regla de scoring propia; sin calibración | ROMPE-DISEÑO | 2–3 ses. | M3 |
| 5 | Incertidumbre del árbitro ignorada (EE/CV de R) | ROMPE-DISEÑO | 0.5 ses. | M3 |
| 6 | Ausencia de baseline trivial obligatorio | ROMPE-DISEÑO | 1 ses. | M3 |
| 7 | Escalas incommensurables entre celdas | DEBILITA | 0 (gratis con #6) | M3 |
| 8 | Selección del set por el dueño del motor | ROMPE-DISEÑO | 2 ses. | M1 |
| 9 | Filtro oculto "momentos con dato real disponible" | DEBILITA | 0.5 ses. + celdas caras | M1 (parcial) |
| 10 | "≥X de N" sin poder, magnitudes ni multiplicidad | ROMPE-DISEÑO | 0.5 ses. (caro en narrativa) | M4 |
| 11 | Sesgo del redactor de L; ciego ausente | ROMPE-DISEÑO | 1–2 ses. | M2 |
| 12 | Varianza del LLM; versión/fecha no fijadas | ROMPE-DISEÑO | 0.5 ses. | M2 |
| 13 | Especificación incompleta de la pregunta | ROMPE-DISEÑO | 1 ses. | M1 |
| 14 | Goodhart en la regla semanal | DEBILITA | 0 (gratis con #8) | M1 |
| 15 | Los 7 umbrales del GO son de proceso | DEBILITA | 1 ses. | M6 |
| 16 | Consecuencias pre-declaradas ausentes; falta el 3.er resultado | ROMPE-DISEÑO | 1 ses. | M5 |
| 17 | Re-validación bajo demanda: errores fuera del muestreo | DEBILITA | 3–5 ses. | fuera de v2 |
| 18 | Sin corredor híbrido ni techo de referencia | DEBILITA | ≈0 | extra recomendado |
| 19 | Retórica de "duelo/superar" y contadores públicos | COSMÉTICO | 0 | — |

---

### A.1 · Contaminación de L por memorización de tabulados — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. La pregunta 4 del set v1 es "prevalencia de victimización en población adulta, 2023". Es un dato de titular: aparece en el boletín de prensa de INEGI, en notas periodísticas, en decenas de páginas replicadas.
2. L responde el número del boletín, con dos decimales y sin derivación.
3. R, calculado del microdato con el mismo universo, coincide casi exactamente. Distancia de L ≈ 0.2 puntos.
4. M, cuya celda mezcla un parámetro medido y uno asignado, cae a 3.1 puntos.
5. **El marcador anota: L gana.** Y no está mal medido: L *sí* quedó más cerca.
6. La inferencia que se hará —"el LLM supera al motor"— es falsa. L no modeló nada: hizo un lookup de memoria. En la pregunta siguiente, que pide la misma tasa **cruzada por decil de ingreso y jefatura femenina** (cruce que ningún boletín publica), L improvisa y se desploma.

El diseño no distingue entre "acertar" y "recordar", y en un set de 12 preguntas basta que 4 sean de titular para que el marcador se decida por memoria.

**Arreglo.** Cuatro piezas, todas dentro del criterio de admisión (M1):
- (a) Clasificar cada pregunta candidata como *publicada* (existe en boletín/tabulado) o *no publicada* (exige procesar microdato: cruces, condicionales, subpoblaciones). Techo duro: ≤20% del set puede ser publicada, y esas se reportan aparte como "control de memoria", no en el marcador.
- (b) **Sonda de perturbación**: reformular universo o escala en un margen que cambie el valor real (18+ → 15+, nacional → urbano ≥100k hab.). Una respuesta memorizada no se mueve; una modelada sí. Se corre para todas las preguntas y se publica cuánto se movió L.
- (c) **Sonda placebo**: una pregunta sobre un indicador plausible pero inexistente. Si L da un número seguro, su seguridad no es informativa en ninguna celda.
- (d) **Ola retenida / post-corte**: al menos 2 celdas cuyo R provenga de una ola posterior al corte declarado del modelo, o de una ola que el equipo aparte y no toque hasta cerrar commits.

**Costo.** 2 sesiones (taxonomía + redacción de sondas). Barato para lo que compra.

---

### A.2 · Circularidad de M: gana por construcción — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. La celda 7 tiene procedencia "medido nacional": su parámetro se estimó de ENIGH 2022.
2. La pregunta correspondiente pide una cantidad de ENIGH 2022.
3. R se calcula del microdato de ENIGH 2022.
4. M devuelve el parámetro. Distancia = 0.0, a dos decimales.
5. L, que no tiene acceso al microdato, queda a 1.8 puntos.
6. **M gana la celda.** No se probó capacidad de modelado: se probó que la función identidad es exacta. Si tres celdas del set son así, M gana el duelo sin haber predicho nada.

Esto es el espejo exacto de #1: el diseño premia a M por memoria de ajuste igual que premia a L por memoria de entrenamiento.

**Arreglo.** Etiquetar cada celda con un **grado de dependencia** respecto de R, declarado antes de abrir datos:
- **Grado 2** — R proviene de la misma encuesta *y* la misma ola *y* el mismo universo que alimentó el parámetro → **excluida del marcador**; va a un anexo de "verificación de plomería" (útil, pero no es el duelo).
- **Grado 1** — misma familia de encuesta, distinta ola / distinto universo / distinta subpoblación → puntúa, y se reporta por separado.
- **Grado 0** — R independiente del ajuste (otra encuesta, desenlace documentado, registro administrativo) → puntúa con peso pleno.

Regla mínima: **el marcador solo cuenta grados 0 y 1, y al menos 1/3 del set debe ser grado 0.**

**Costo.** 1 sesión para el esquema. El costo real está escondido: aplicar el filtro probablemente descalifica la mitad del set v1 y obliga a generar preguntas nuevas (2–3 sesiones más). Ese es el precio honesto de que el duelo signifique algo.

---

### A.3 · No-independencia de segundo orden: el corpus leyó a R — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. La pregunta 9 es sobre horas semanales de trabajo de cuidados no remunerado por sexo.
2. El corpus temático que L usa cita un artículo académico que, a su vez, reporta la cifra de la encuesta oficial.
3. L responde la cifra del artículo. Distancia a R ≈ 0.4 horas.
4. **L gana la celda** — pero L y R no son independientes: el corpus es una compresión con pérdida de R, transmitida por la literatura. Es el mismo lookup de #1, con un salto intermedio que lo vuelve invisible al filtro "¿está publicado en un boletín?".

Este es el hallazgo más profundo de los tres: determina si el duelo puede discriminar *algo*. Un corpus escrito por LLMs a partir de la literatura que resume las encuestas oficiales tiene, por diseño, una vía de fuga hacia el árbitro.

**¿Qué pregunta puede siquiera discriminar?** Solo cuatro clases:
- **Conjuntas y condicionales no publicadas**: interacciones de ≥2 variables que ni el boletín ni la literatura tabulan (conducta × tamaño de localidad × composición del hogar).
- **Fuera de periodo**: olas posteriores al corpus y al corte del modelo.
- **Contrafactuales con desenlace documentado**: un choque, un programa evaluado, un cambio normativo con registro — donde R es un desenlace, no una marginal.
- **Ordenamientos**: el ranking de 8 subgrupos según una conducta, cuando la literatura publica marginales pero no el orden conjunto.

**Arreglo.** Criterio de admisión operativo y verificable: **la prueba del bibliotecario**. Una persona (o una sesión con búsqueda) sin acceso al motor intenta 15 minutos encontrar la respuesta en (i) tabulados oficiales y (ii) la bibliografía propia del corpus. Si la encuentra, la pregunta **queda descalificada del marcador**. Se registra el resultado de la prueba junto a la pregunta.

**Costo.** 1 sesión para definir el protocolo + ~15 min por pregunta candidata. Para un marco de 50 preguntas: ~2 sesiones. Es el arreglo con mejor rendimiento por peso del informe.

---

### A.4 · El marcador "distancia a R": puntos contra distribuciones — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. L emite "21.0%". Un punto, sin intervalo, sin base declarada.
2. M emite "23.5%" con un intervalo declarado [20.1, 26.9] derivado de la incertidumbre de sus parámetros.
3. R = 21.4%.
4. **L gana por 2.1 puntos.** El marcador registra una victoria de L.
5. Pero M *contuvo* a R en su intervalo y L no declaró ninguno. Un corredor que dice "21.0" y otro que dice "23.5 ± 3.4" no son comparables con una resta: el primero está apostando todo a una cifra y el segundo está reportando lo que sabe y lo que no. El diseño premia sistemáticamente la falsa precisión.
6. Al final del piloto no existe ninguna afirmación sobre **calibración** —si los intervalos de alguien cubren lo que dicen cubrir— que es, para un motor destinado a producir escenarios, más importante que la exactitud puntual.

**Arreglo.**
- Ambos corredores emiten **distribución o intervalo**, nunca punto solo. Para L esto sale gratis del ensemble de #12 (cuantiles empíricos de K corridas). Para M sale de la incertidumbre de parámetros ya declarada.
- Puntuar con una **regla propia**: escala continua → *interval score* / CRPS; binaria o categórica → Brier o log.
- Reportar **calibración por separado**: cobertura empírica de los intervalos al 80% a lo largo de las N celdas. Es un resultado por derecho propio y no depende de quién gane.

**Costo.** 2–3 sesiones: cambiar el formato de elicitación de ambos corredores y escribir un script de scoring de ~100 líneas. Es la diferencia entre un marcador y un horóscopo.

---

### A.5 · La incertidumbre del propio árbitro — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. La celda pide una conducta en una subpoblación con n no ponderado ≈ 180 casos.
2. R = 21.4% con error estándar amplio; el intervalo de confianza cubre holgadamente tanto a L (21.0) como a M (23.5).
3. El marcador anota victoria de L por 2.1 puntos.
4. Si se hubiera extraído otra muestra de la misma encuesta, R habría sido 22.9% y **M habría ganado la misma celda**.
5. El marcador no midió competencia: midió ruido muestral. Con 12 celdas y la mitad así, el ganador del duelo lo decide el diseño muestral de INEGI, no los corredores.

**Arreglo.** Dos reglas, ambas pre-declaradas:
- **Admisión**: se excluyen ex ante las celdas donde R no sea estimable con precisión suficiente. Fijar el umbral tomándolo del documento metodológico de cada encuesta (INEGI publica criterios de precisión por coeficiente de variación; adoptarlos en vez de inventarlos) y añadir un piso de n no ponderado.
- **Banda de indecidibilidad**: si |d_L − d_M| < 0.5 · EE(R), la celda se declara **INDECIDIBLE** y no da punto a nadie. El conteo de indecidibles se publica con la misma prominencia que el marcador — es información sobre la potencia del duelo, no un fracaso.

**Costo.** 0.5 sesión. Es el arreglo más barato del informe y elimina la fuente de error más vergonzosa.

---

### A.6 · No hay baseline. Dos malos estimadores producen un ganador — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. Cierra el piloto: M gana 8 de 12.
2. Titular: "el motor estructural supera al LLM".
3. Nadie calculó lo obvio: la **marginal nacional de la ola anterior**, o la media del estrato, o "predice la tasa base". Ese baseline tonto habría quedado más cerca de R que ambos corredores en 9 de las 12 celdas.
4. La conclusión correcta —"ambos artefactos son peores que no hacer nada, y M es el menos malo"— es exactamente la que el diseño **no puede** producir, porque no tiene con qué compararse.

Este es el hueco que ningún ítem del brief original nombra, y es el más caro de descubrir tarde. En cualquier hub de pronóstico serio el baseline no es opcional: es la vara.

**Arreglo.** Un tercer corredor obligatorio, **B**, definido mecánicamente y por adelantado: para cada pregunta, la estimación más tonta defendible (marginal nacional publicada de la ola previa; si no existe, media del estrato más grueso disponible). B se calcula por script, sin juicio humano. Y el marcador deja de reportar distancias crudas para reportar **skill score**:

> s = 1 − error(corredor) / error(B)

s > 0 significa "aportó algo sobre la tontería"; s ≤ 0 significa "no". Un corredor puede ganar el duelo y tener s negativo — y ese hecho tiene que ser legible en la primera línea del marcador.

**Costo.** 1 sesión. Rendimiento por costo: el más alto de todo el informe.

---

### A.7 · Escalas incommensurables entre celdas — DEBILITA

**Edge case.** La celda 3 está en pesos (R = $4,200; L = $4,150; M = $4,600) y la celda 4 en puntos porcentuales (R = 21.4; L = 21.0; M = 23.5). El marcador de "quién quedó más cerca" trata ambas como un voto de igual peso, ocultando que un error de $400 en gasto mensual puede ser irrelevante y uno de 2.1 puntos en victimización puede ser enorme. Sumar votos sobre escalas distintas es sumar peras y kilómetros.

**Arreglo.** Gratis si entra #6: el skill score contra B ya es adimensional y comparable entre celdas. Alternativa equivalente: normalizar por EE(R).

**Costo.** 0.

---

### A.8 · El dueño del motor elige las preguntas — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. Llega la semana de armar el set v1. Se eligen "los momentos con celda terminada".
2. Las celdas terminadas son, por selección natural del trabajo, aquellas donde hubo buen microdato y el parámetro salió limpio.
3. M gana 9 de 12 — y habría ganado igual con un motor la mitad de bueno, porque el set se muestreó de la región donde M es fuerte.
4. El sesgo funciona idénticamente en reversa: un escéptico armando el set con 12 celdas exóticas produce una victoria de L igual de vacía.
5. Además entran "regalos": preguntas de tasa base trivial (¿qué proporción de hogares tiene refrigerador?) donde ambos aciertan dentro de un punto, inflan N y no discriminan nada.

**Arreglo.**
- Construir un **marco de 40–60 preguntas candidatas antes de saber qué celdas están listas**, derivado de los codebooks de las encuestas, estratificado por dominio × tipo de escala × grado de dependencia × dificultad esperada.
- Un adversario externo aporta ≥1/3 del marco.
- El set v1 se **sortea del marco por muestreo estratificado con semilla pública**. Nadie elige.
- Las preguntas donde B queda dentro de la banda de indecidibilidad respecto de R no se descartan: se conservan y se puntúan, y ahí lo que se prueba es si algún corredor **le gana a la tontería**. Deja de ser un empate gratis y se vuelve una prueba de habilidad.

**Costo.** 2 sesiones (marco + script de muestreo). Efecto colateral valioso: resuelve #14 sin costo adicional.

---

### A.9 · El filtro oculto: "momentos con dato real disponible" — DEBILITA

**Edge case.** El set se restringe, por necesidad operativa, a conductas que las encuestas oficiales miden bien. Pero las conductas que las encuestas miden bien son exactamente aquellas sobre las que más se ha escrito — y por tanto sobre las que L está mejor entrenado. Y son también las que el motor tuvo más fácil parametrizar. El filtro de disponibilidad **sesga hacia ambos corredores a la vez**, y hacia el territorio menos interesante: el duelo termina hablando solo de "conductas encuestables", que no es la clase de fenómeno para la que un simulador de agentes se construye.

**Arreglo.** Dos cosas, ninguna cara en sí misma:
- Declarar el límite de alcance en la conclusión, textualmente: *el duelo mide estimación de cantidades encuestables; no dice nada sobre conducta emergente, contrafactuales ni dinámica.*
- Incluir en el marco al menos 2 celdas cuyo R sea un **desenlace documentado** (evaluación de programa, choque con registro administrativo, experimento natural publicado) y no una marginal de encuesta. Estas son grado 0 por construcción y son las únicas celdas donde el motor puede mostrar aquello para lo que existe.

**Costo.** 0.5 sesión de declaración; 1–2 sesiones **por celda** de desenlace documentado. Son caras: por eso son dos, no seis.

---

### A.10 · "≥X de N": el criterio declara ganadores inexistentes — ROMPE-DISEÑO

Este es el hallazgo con el número más incómodo del informe.

**Edge case, paso a paso.**
1. N = 12, X = 7. Supongamos que L y M son **exactamente igual de buenos**: cada celda es un volado.
2. P(L consigue ≥7 de 12) = 0.387. Por simetría, P(M consigue ≥7) = 0.387.
3. **P(alguien "gana") ≈ 0.774.** En ~3 de cada 4 mundos donde no hay ninguna diferencia, este diseño imprime un ganador.
4. Declarar victoria con 7 de 12 equivale a reportar p ≈ 0.39: literalmente ninguna evidencia.
5. Para que 12 celdas den un resultado defendible (prueba de signos, α=0.05 bilateral) haría falta **10 de 12**. Y la potencia para detectarlo:

| Efecto real (fracción de celdas que gana el mejor) | N para 80% de potencia |
|---|---|
| 87 / 13 | ~12 |
| 80 / 20 | ~20 |
| 70 / 30 | ~50 |

Es decir: **el piloto solo puede detectar una masacre.** Cualquier ventaja realista —"M gana 7 de cada 10"— es invisible con N=12, y el diseño no lo advierte en ninguna parte.

Se suma que no hay corrección por multiplicidad (12 celdas leídas individualmente producirán "hallazgos" espurios) ni prueba de equivalencia para declarar el empate: hoy "empate" es una regla de dedazo, no una afirmación estadística.

**Arreglo.** Dos movimientos, ambos casi gratis en trabajo y caros en narrativa:
- **Cambiar el estadístico de conteo a magnitud.** Comparar la *diferencia media de skill scores* con bootstrap por bloques sobre celdas, reportando efecto + intervalo. Esto **compra potencia sin comprar celdas**: es la única mejora estadística gratis del diseño.
- **Cambiar el entregable del piloto.** Pre-registrar que con N=12–15 el piloto **no declara ganador**. Sus productos son: (i) el intervalo sobre la diferencia de skill, (ii) la calibración de cada corredor, (iii) el conteo de indecidibles, (iv) **el N necesario para v2**. El veredicto se emite en v2 con N calculado.

**Costo.** 0.5 sesión de escritura y un script de bootstrap. El costo real es político: mata el titular. Vale la pena decirlo sin adorno — un titular que se sostiene el 23% de las veces no es un activo.

---

### A.11 · El redactor de L conoce el motor — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. El mismo analista que construyó la celda 7 redacta la pregunta y corre a L.
2. Sabe que M dice 23.5. No hace trampa: hace algo peor, porque es invisible. Al redactar la pregunta usa la ontología del motor ("perfil × contexto"), que orienta a L hacia el mismo marco.
3. Al elegir cómo formular el universo, elige —sin registrarlo— la formulación que le "parece justa", que es la que él ya sabe que discrimina.
4. El commit de L se sella **antes** de ver la salida del motor, y la regla del diseño se cumple al pie de la letra. Pero el commit previo no protege de nada: el sesgo no entró al ver la salida, entró en meses de conocer el motor por dentro.

El diseño trata "commit anterior" como sinónimo de "ciego". No lo es.

**Arreglo — ciego mínimo viable, sin equipo grande:**
- El **texto de la pregunta no lo escribe nadie**: se deriva mecánicamente del codebook de la encuesta (pregunta literal + universo + escala + estimador), sin vocabulario del motor.
- El **prompt de L es una plantilla pre-registrada única**, idéntica para las N preguntas, con un solo hueco para la spec de la pregunta.
- L se corre en sesión sin corpus, sin proyecto, sin contexto del motor, mediante un **script**: spec → llamada a API → hash comprometido. Sin humano en el bucle.
- Idealmente, modelo distinto del que escribió el corpus. Si no es posible, se declara y se registra como limitación.

**Costo.** 1–2 sesiones para el script y la plantilla. Elimina también #12 casi por completo.

---

### A.12 · Varianza del LLM y versión no fijada — ROMPE-DISEÑO

**Edge case.** Se corre L tres veces sobre la misma pregunta: 19%, 24%, 31%. Se commitea la primera. R = 23. Si se hubiera committeado la segunda, L gana la celda; la tercera, la pierde por goleada. **El marcador es función de la semilla.** A esto se suma que "el LLM" no es un objeto estable: sin nombre de modelo, versión, fecha y temperatura, el resultado no es replicable ni siquiera por el mismo equipo en tres meses.

**Arreglo.** Pre-registrar: modelo + versión + fecha + temperatura + **K ≥ 10 corridas** + regla de agregación (mediana para el punto, cuantiles empíricos 10/90 para el intervalo). Archivar las K salidas crudas. Y reportar la **dispersión entre corridas como resultado**, no como estorbo: un corredor que oscila 12 puntos entre corridas está diciendo algo importante sobre sí mismo.

Bonus: el ensemble le da a L la distribución que #4 necesita. Un arreglo, dos agujeros.

**Costo.** 0.5 sesión y K llamadas de API. El mejor rendimiento por costo del informe junto con #6.

---

### A.13 · La pregunta no está definida hasta que se fija cómo se calcula — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. La pregunta dice "adultos". L la interpreta como 18+.
2. Al calcular R, el operador —que ya vio las respuestas de L y M— usa 15+, porque "así lo reporta la encuesta".
3. R se mueve 1.6 puntos y con eso cambia el ganador de la celda.
4. Nadie mintió. La spec estaba incompleta, y la ambigüedad se resolvió después de ver los corredores. Es adjudicación post-hoc con cara de rigor.

**Arreglo.** La pregunta se commitea como **spec ejecutable**: encuesta, ola, filtro de universo, variable(s), estimador, ponderador, escala, decimales. R se computa corriendo esa spec. Si dos personas corren la spec y obtienen números distintos, la spec estaba mal y la celda se anula **antes** de puntuar.

**Costo.** 1 sesión para el esquema. Se paga sola la primera vez que evita una discusión de adjudicación.

---

### A.14 · Goodhart en la regla semanal — DEBILITA

**Edge case.** Semana 9, nada está listo. Para no romper el contador, se termina la celda más fácil disponible: parámetro asignado, R de titular publicado. El contador queda verde. Repetido tres meses, el piloto llega a sus gates con 12 celdas baratas y "pasa" sin haber probado nada. La regla no produjo honestidad: produjo relleno con procedencia impecable.

**Arreglo.** Gratis si entra #8: la celda de la semana **no se elige**, se toma en el orden aleatorizado del marco. Si esa celda no se puede producir, se registra un **SKIP con motivo** y el contador de skips se publica al lado del de celdas. Añadir un tope: máximo 1 celda contada por semana, para que la velocidad no compense la calidad.

**Costo.** 0.

---

### A.15 · Los 7 umbrales del GO son de proceso — DEBILITA

**Edge case.** Los 7 umbrales son verificables por comando: "≥7 celdas con universo y escala declarados", "dos commits por celda", "procedencia etiquetada". Todos se satisfacen escribiendo YAML correctamente. Un motor **completamente equivocado** pasa los 7. Un gate cuyos umbrales están todos bajo control del equipo no es un gate: es una lista de tareas con firma.

**Arreglo.** Conservar 5 umbrales de proceso y **convertir 2 en umbrales de resultado**, es decir, determinados por la naturaleza y no por el equipo:
- **U6 (calibración):** los intervalos al 80% de M cubren a R en ≥60% de las celdas puntuadas.
- **U7 (habilidad):** M le gana al baseline B en ≥2/3 de las celdas puntuadas (skill score > 0).

Y un tercero si cabe: las sondas de contaminación de #1 se comportan como se predijo (L se mueve al perturbar el universo; L no confabula ante el placebo).

**Costo.** 1 sesión, y depende de que #4 y #6 ya estén construidos.

---

### A.16 · Consecuencias pre-declaradas: falta la tabla y falta el tercer resultado — ROMPE-DISEÑO

**Edge case, paso a paso.**
1. L gana 8 de 12.
2. Sin tabla de decisión escrita de antemano, la lectura que se impone en la reunión es "el motor no aporta; pivotemos al LLM".
3. Pero el duelo solo muestreó **estimación puntual de cantidades encuestables**. Nunca probó contrafactuales, mecanismos, escenarios ni la trazabilidad de supuestos — que es para lo que existe un simulador estructural. Se abandona un artefacto por perder una competencia en la que no compite.
4. El error simétrico: M gana 8 de 12 y se declara "motor validado", cuando ambos pueden estar peor que B (ver #6). **"M > L" no prueba "M es bueno."**
5. Y falta por completo el tercer resultado, que en este dominio es el más probable: **ambos lejos de R**. La literatura de predicción de desenlaces de vida con datos ricos —el caso de referencia es el Fragile Families Challenge— sugiere que hay techos de predictibilidad bastante bajos para conducta individual, y que equipos con microdato longitudinal excelente predicen poco. Un piloto que no puede reportar "el techo está bajo y ninguno de los dos lo alcanza" está diseñado para no aprender su lección más valiosa.

**Arreglo.** Tabla de decisión pre-registrada, con B dentro. Cinco casillas, no dos:

| Resultado | Qué queda probado | Qué NO queda probado |
|---|---|---|
| M > L y M > B, con intervalos calibrados | M tiene habilidad demostrada **en esta clase de pregunta** | Nada sobre contrafactuales, mecanismos ni transferencia a otras clases |
| M > L pero ninguno > B | Nada está validado; ambos son decorativos para esta clase | Que el motor sea inútil para su uso previsto |
| L > M y L > B | El corpus es un estimador barato competitivo para cantidades cercanas a lo publicado — **condicionado a pasar las sondas de contaminación** | Que el LLM "modele"; sin sondas limpias no se concluye nada |
| Ambos lejos de R, B cerca | El problema tiene techo bajo o las preguntas están mal elegidas | Cualquier comparación entre L y M |
| Mayoría de celdas INDECIDIBLE | El duelo no tuvo potencia; se reporta el N necesario | Cualquier veredicto |

Y una cláusula de alcance, escrita antes de correr nada: *ningún resultado de este piloto autoriza abandonar L ni M para usos que el piloto no muestreó.*

**Costo.** 1 sesión. Es la página que evita el pivote estratégico injustificado, que es el daño más caro que este diseño puede producir.

---

### A.17 · La re-validación bajo demanda deja errores fuera del muestreo para siempre — DEBILITA

**Edge case, paso a paso.**
1. El duelo toca 12 celdas, que dependen de ~10 de los ~30 reports.
2. Los 20 reports restantes nunca son contradichos por el duelo, porque el duelo nunca los interroga.
3. La doctrina dice: solo se re-tieriza lo que el duelo contradiga. Por tanto, esos 20 reports **jamás** se revisan: la doctrina garantiza su inmortalidad.
4. Entre ellos hay una afirmación etiquetada "narrativa" que, tres documentos río abajo, quedó citada como si fuera "fuerte". Diez meses después sostiene una decisión.

**Arreglo — barrido mínimo complementario, que no re-audita nada en bloque.** Tres piezas, en orden de rendimiento:
- **(a) Barrido de etiqueta, no de contenido.** Para los ~30 reports, verificar solo la coherencia del tier con su cita: ¿hay cita? ¿la cita sostiene el alcance de la afirmación? ¿el tipo de cita corresponde al tier? Es mecánico, ~20 min por report.
- **(b) Muestreo de aserciones.** Extraer k=5 aserciones al azar por report con semilla pública y verificar solo esas. Da una **tasa de error estimada por report**, publicable, y una regla de disparo: si la tasa muestral supera el umbral, ese report sí va a re-auditoría completa. Es muestreo de aceptación clásico: barato y **acota lo desconocido** en vez de ignorarlo.
- **(c) Priorización por carga.** Auditar primero lo que sostiene peso: los nodos del grafo de dependencias que alimentan parámetros del motor o que aparecen citados en decisiones.

**Costo.** (a) ~10 horas. (b) 30 reports × 5 aserciones = 150 verificaciones, 3–5 sesiones. Real, pero acotado y con producto publicable.

---

### A.18 · No hay corredor híbrido ni techo de referencia — DEBILITA

El duelo tiene dos corredores y ninguna vara superior. Si M gana, no se sabe si es porque M es bueno o porque L es malo. Y —esto importa dado el mandato anti-purista— la conclusión que el programa dice querer (el híbrido) **no está siendo medida por el diseño**: se la deja como moraleja de sobremesa en vez de ponerla a correr.

**Arreglo.** Añadir el corredor **E = combinación mecánica de L y M** (promedio de puntos, o mezcla 50/50 de distribuciones), calculado por script sin elicitación adicional. Costo marginal ≈ 0. Si E le gana a ambos —que es lo que suele pasar con ensembles en pronóstico— la respuesta a "¿LLM o motor?" queda medida y no argumentada.

Opcional y caro: un corredor **H** (experto humano de dominio, sin acceso a R) como techo de referencia. Recomendable en v2, no en el piloto.

**Costo.** ≈0 para E. Es la **única adición no-ROMPE que recomiendo meter en v2**, precisamente porque no cuesta nada y responde la pregunta que el programa dice tener.

---

### A.19 · Retórica de "duelo" y contadores públicos — COSMÉTICO

"Duelo", "superar", "marcador", más contadores públicos de avance, generan presión de audiencia hacia un desenlace decisivo. Es el mismo incentivo de #14 en la capa narrativa: el peor resultado para el relato ("indecidible") es el más probable para la estadística.

**Arreglo.** Llamarlo **comparación pre-registrada**, y publicar el contador de INDECIDIBLES y de SKIPS con el mismo tamaño de letra que el marcador. **Costo.** 0.

---

## B. El diseño reconstruido: comparación pre-registrada v2

*Solo los arreglos ROMPE-DISEÑO, más una adición de costo cero. Nada de perfección.*

**Corredores: cuatro, no dos.**
**L** (LLM/corpus) · **M** (motor) · **B** (baseline tonto, obligatorio) · **E** (combinación mecánica L+M, gratis).

**M1 · El marco antes que las celdas.**
Se construye un marco de 40–60 preguntas candidatas *antes* de saber qué celdas están listas, cada una como **spec ejecutable** (encuesta, ola, universo, variable, estimador, ponderador, escala). Tres filtros de admisión, todos verificables:
1. **No publicada** — pasa la prueba del bibliotecario (15 min con búsqueda + bibliografía del corpus). Máximo 20% del set puede ser "publicada", y esas se reportan como control de memoria, fuera del marcador.
2. **Fuera de muestra para M** — grado de dependencia 0 o 1; el grado 2 va a anexo. Mínimo 1/3 del set en grado 0, incluyendo ≥2 celdas cuyo R sea desenlace documentado y no marginal de encuesta.
3. **Árbitro decidible** — R estimable con la precisión que el propio documento metodológico de la encuesta considera aceptable, y con piso de n no ponderado.
El marco se estratifica (dominio × escala × dependencia × dificultad); el set se **sortea con semilla pública**. La celda de cada semana es la siguiente del orden sorteado; lo que no se produce se registra como SKIP con motivo.

**M2 · Elicitación mecánica y ciega.**
Un script toma la spec y produce las cuatro respuestas sin humano en el bucle: L con modelo+versión+fecha+temperatura fijados y **K=10 corridas** (mediana + cuantiles 10/90); M con punto e intervalo derivados de su incertidumbre de parámetros; B por fórmula; E por combinación. Hashes de las cuatro comprometidos **antes** de que R exista. La pregunta se deriva del codebook, no la redacta nadie.

**M3 · Scoring propio, comparable y con el árbitro incierto adentro.**
Por celda: skill score contra B, **s = 1 − error/error(B)**, con *interval score*/CRPS para escalas continuas y Brier para binarias. Celda **INDECIDIBLE** si |d_L − d_M| < 0.5·EE(R). Se reporta, para cada corredor: skill medio con IC por bootstrap de bloques, y **cobertura empírica de los intervalos al 80%** (calibración) como resultado independiente del ganador.

**M4 · El piloto no declara ganador.**
Pre-registrado: con N=12–15 la prueba de signos solo detecta efectos de ~87/13. Los productos del piloto son (i) el intervalo sobre la diferencia de skill, (ii) la calibración de cada corredor, (iii) el conteo de indecidibles y skips, (iv) **el N requerido para v2** (≈20 para un efecto 80/20; ≈50 para 70/30). El veredicto se emite en v2, con N calculado, usando magnitud y no conteo.

**M5 · Tabla de decisión pre-declarada, con las cinco casillas** de A.16, más la cláusula de alcance: *ningún resultado autoriza abandonar L ni M para usos no muestreados; el duelo mide estimación de cantidades encuestables y nada más.*

**M6 · Dos de los siete umbrales del GO son de resultado:** cobertura de los intervalos de M ≥60% de celdas puntuadas, y M > B en ≥2/3 de celdas puntuadas. Al menos un umbral debe estar determinado por la naturaleza, no por el equipo.

**Lo que se queda fuera de v2 a propósito:** el barrido complementario del corpus (#17, va en paralelo, no en el duelo), el corredor experto humano (#18, v2 tardío), y toda mejora que no arregle un ROMPE-DISEÑO.

**Costo total de v2 sobre v1:** ~12–15 sesiones, de las cuales ~6 son escritura y scripts (baratas) y el resto es regenerar el set de preguntas bajo el nuevo criterio de admisión (caro e inevitable).

---

## C. Qué cambiaría mi veredicto

Cinco condiciones. Si se cumplen, mis objeciones caen y el diseño original es defendible casi tal cual.

1. **Si ≥80% de las celdas son cruces conjuntos o condicionales que no aparecen en tabulados oficiales ni en la bibliografía del corpus, y las sondas de contaminación se comportan como se predice** (L se mueve cuando se perturba el universo; L no confabula ante el placebo) → caen #1 y #3, y "L ganó" pasa a ser información en vez de un lookup.

2. **Si el árbitro de ≥la mitad de las celdas proviene de fuentes independientes del ajuste de M** —desenlaces documentados, registros administrativos, evaluaciones de programa, olas retenidas— → cae #2, y "M ganó" deja de poder explicarse por la función identidad.

3. **Si el titular deja de ser binario**: si el entregable pasa de "quién gana ≥X de N" a "diferencia de skill con intervalo, más calibración, más el N necesario para concluir" → cae #10 completo, y el piloto con N=12 se vuelve honesto sin necesidad de más celdas.

4. **Si L se produce por pipeline mecánico** —versión fijada, K corridas, plantilla pre-registrada, sin humano que redacte, hash publicado antes de que R exista— → caen #11 y #12, y el "commit previo" empieza a significar lo que el diseño cree que significa.

5. **Si existe B y ambos corredores emiten intervalos puntuados con regla propia** → caen #4, #5, #6 y #7 de un golpe, y el marcador deja de poder ser decidido por el diseño muestral de INEGI.

Añado una sexta, más blanda: **si la tabla de decisión de A.16 se firma antes de correr la primera celda**, entonces incluso un piloto imperfecto es seguro, porque su peor resultado deja de ser un pivote estratégico y pasa a ser un dato.

---

## Nota de cierre para el CAREO

Nada en este informe sugiere abandonar ninguno de los dos corredores. El motor tiene una propiedad que L no tiene ni tendrá —procedencia trazable por parámetro, que es lo que permite discutir un supuesto en vez de discutir una intuición— y L tiene una propiedad que el motor no tiene: cobertura barata de preguntas para las que nadie parametrizó una celda. El diseño actual está construido para que solo una de las dos pueda ganar, cuando la respuesta más probable del piloto —si se le añade B y se le añade E— es que **el ensemble le gana a los dos y ninguno de los tres le gana por mucho al baseline**. Ese resultado, hoy, el diseño no lo puede ni escribir. Ese es el arreglo.
