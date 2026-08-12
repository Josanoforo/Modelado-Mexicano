# E4c · R5.1-D2 — Commit 4: diseño resuelto por benchmark (Bloque D)

**No edita Commit 1 (`c6c9af1`) ni Commit 3 (`ea72336`).** Resuelve, con fuente, las dos decisiones que Commit 3 dejó `PENDIENTE mesa` (§1 umbral, §2 hogares mixtos) — no por criterio propio, sino yendo a ver cómo lo resolvió el precedente metodológico directo sobre la misma pregunta y la misma encuesta. Sigue sin producir resultado del diseño R5.1-D2.

## 0 · Verificación de la fuente — hecha antes de obedecer el encargo

El encargo instruyó verificar la fuente antes de usarla. Se hizo: descarga real (`curl`, HTTP 200, `application/pdf`, 253,790 bytes, `sha256 899dff85...`), lectura completa de las 39 páginas del PDF (no un resumen), y contraste literal de cada afirmación del encargo contra el texto:

| Afirmación del encargo | Verificado contra el PDF |
|---|---|
| Título/autores/fecha | "Old-Age Government Transfers and the Crowding Out of Private Gifts: The 70 and Above Program for the Rural Elderly in Mexico", Catalina Amuedo Dorantes (SDSU) y Laura Juárez González (Banxico), N° 2013-17, noviembre 2013 — **coincide exacto**, p.1-2 |
| Deflactan a pesos reales de año base 2010 | "We deflate all transfer and income variables using the consumer price index, so they are all expressed as monthly average amounts in **2010 pesos**" — p.10, sin discusión adicional de nominal-vs-real |
| DDD con grupo de edad no elegible como control adicional | "we include individuals **55 to 69 years old** as an additional control group... because they do not qualify for the program, regardless of the locality" — p.11 |
| Clustering a nivel municipio, cita Bertrand-Duflo-Mullainathan (2004) | "Standard errors are clustered at the municipality level to account for the serial correlation problem... (Bertrand, Duflo and Mullainathan, 2004)" — p.12, nota 21: **"Ideally, we would like to cluster standard errors at the locality level, but we lack locality identifiers"** — el municipio es un segundo mejor por falta de dato, no la elección ideal de los propios autores |
| Regla de hogar "al menos un elegible" | "our key independent variable is the triple interaction of dummy variables for having **at least one household member who is age 70 and older**..." — p.21 |
| Efecto a nivel hogar casi el doble que individual | Tabla 8: `-0.127***` (hogar, Any Remittances) vs. Tabla 3: `-0.066**` (individuo) — razón 1.92, **"casi el doble" confirmado** |
| Placebo con 2 olas pre-programa | Tabla 5, "Placebo Test Using Data from the ENIGH 2004 and 2006" — Treatment Effect `-0.038`, no significativo |
| Chequeo de tamaño de hogar, efecto pequeño negativo, sig. solo al 10% | "having any age-eligible individual in a treated locality in 2008 has a **small and negative**... effect on household size. The impact is... only statistically different from zero at the **10 percent level**" — p.21-22 |
| 37% crowding out (este paper) | Abstract: "the program crowds out private transfers by **37 percent**" |
| 86% Juárez (2009), Ciudad de México | p.2: "Juarez (2009) estimates... a crowding out of **86 percent**" |
| ~30% Jensen (2004), Sudáfrica | p.2: "Jensen (2004) finds that an age-conditioned pension in South Africa reduces private transfers by about **30 percent**" |
| Galiani y Gertler (2009): las transferencias privadas AUMENTARON | p.8-9: "private transfers received by qualifying households **increased** by **17.5 pesos per month**" |

**Ninguna afirmación del encargo resultó falsa o exagerada.** No hay PARO por cita falsa. El PDF se registró en `data/manifiesto.yaml` (id `banxico_2013_17_crowding_out_70ymas`, `raiz: descargas_mx`, sha256 citado arriba) — único campo corregido a mano tras `--promueve`: `descargado_por` (el valor por defecto de `--escanea` para `descargas_mx` asume "usuario, vía navegador"; aquí fue el agente vía `curl` directo, corregido para no dejar una procedencia falsa en el propio registro de procedencia). Efecto colateral observado y declarado, no ocultado: `--promueve` reescribió el archivo completo con su propio serializador YAML, lo que reflowó (mismo contenido, distinto ancho de línea) una entrada preexistente no relacionada (`banxico_codi_cuentas_validadas_x_mil_hab`) — no es un cambio de contenido, es un artefacto de usar la herramienta canónica.

## 1 · PASO 2 · §1 resuelto — deflactar, año base declarado

**Decisión: opción (b).** La literatura no discute nominal-vs-real para ENIGH agrupada — lo asume de oficio (p.10, sin nota de pie que lo cuestione). Trasladado a R5.1-D2:

**Año base declarado: la ventana de levantamiento de la propia ola ENIGH 2018 (INPC nov-2018 = 102.303, no el 100 nativo de 2ª quincena julio-2018).** Se prefiere sobre el 100 nativo de la serie por una razón concreta: el umbral de $1,092 es el que regía, nominal, exactamente cuando ENIGH 2018 se levantó (ago-nov 2018) — no hay que ajustarlo para compararlo contra esa ola. Declarar el año base como "julio-2018=100" en cambio introduciría una cuña de 2.3% entre el umbral y su propia ola de referencia sin ninguna razón sustantiva, solo por ser la base nativa de la serie. Declarado aquí, antes de calcular, con la razón escrita — no es "deflactar 2022 hacia 2018" sin más: es fijar que **el umbral y la ola 2018 ya están en la misma base**, y solo la ola 2022 necesita traerse a ella.

**Deflactor de fuente primaria, no de compilación.** La API de indicadores de INEGI (`api_indicadores.html`) exige token por registro con correo — **no completable en esta sesión** (declarado como limitación real, no rodeado con un número sin verificar). Ruta primaria alterna, sí completada: **DOF**, publicación mensual rutinaria del INPC (obligación legal, Código Fiscal art. 20-Bis, confirmado en el propio comunicado de INEGI leído en Commit 3).

| Mes | INPC (base 2ª quincena jul-2018=100) | Fuente primaria DOF |
|---|---|---|
| Noviembre 2018 | **102.303** | `dof.gob.mx/nota_detalle.php?codigo=5546133&fecha=10/12/2018` — cita literal: "...que fue de 101.440" (oct) implica índice nov "una variación de 0.85 por ciento" — el nivel 102.303 se lee directo del documento, verificado por `WebFetch` (no `curl -k`, funcionó sin rodeo TLS esta vez) |
| Noviembre 2022 | **125.997** | `dof.gob.mx/nota_detalle.php?codigo=5676669&fecha=10/01/2023` — cita literal: "el índice correspondiente al mes de noviembre de 2022, que fue de 125.997" |

**El número primario NO difiere del 23.16% de Commit 3 — coincide exacto** (Commit 3 citó las mismas dos cifras de dos compilaciones secundarias que citaban a INEGI/Banxico; DOF las confirma dígito por dígito). No hay nada que cambiar hacia atrás — solo se sube la cita de secundaria a primaria. Deflactor = 125.997/102.303 = **1.231606** (23.16% acumulado nov-2018→nov-2022). Umbral deflactado 2022, sin cambio respecto a Commit 3: **$1,344.91/mes ≈ $4,034.74/trimestre** sobre `ing_tri`.

**El hallazgo de Commit 3 cambia de función, como pide el encargo.** Que el programa nunca haya indexado los $1,092 durante sus cinco ejercicios fiscales (2014-2018, tres cortes DOF verbatim) ya no es el argumento que sostiene la opción (a) — es una **reserva declarada del diseño (b)**: el umbral que se está deflactando fue, en su origen, un monto que el propio Estado dejó erosionar en términos reales mientras existió. Deflactarlo ahora corrige la comparación entre olas, no reconstruye una intención de política que nunca existió.

**Sensibilidad (a), reportada junto a (b), no en su lugar — medición, no elección.** Commit 3 ya midió el costo de la decisión: **45 de 28,626 personas clasificables de 2022 (0.157%) cambian de grupo** entre (a) nominal y (b) deflactado. La corrida real (Paso 3 diferido) reporta ambas: (b) como especificación principal, (a) como sensibilidad citada junto al resultado — no dos veredictos, un veredicto con su robustez declarada.

## 2 · PASO 3 · §2 resuelto — "al menos un elegible", con el refinamiento de tres estados

**Decisión: la cuarta regla, tomada de la literatura, no de las tres que Commit 3 propuso.** p.21: la variable de tratamiento a nivel hogar del paper es un indicador de tener **al menos un integrante elegible**. Traducida a R5.1-D2, con la precisión que el paper no necesita (su elegibilidad es binaria por edad; la de R5.1-D2 tiene tres estados a nivel persona — T, C, fuera de universo):

> **El hogar es T si tiene al menos una persona T. Es C si tiene al menos una persona C y ninguna T. Queda fuera del universo del desenlace de corresidencia si no tiene ninguna persona clasificada (T o C).**

**Medido, con el umbral ya decidido en §1** (2018 nominal — es su propia base; 2022 deflactado):

| Ola | Hogares con ≥1 persona 65+ clasificada | → T (≥1 persona T) | → C (≥1 persona C, ninguna T) | De los T, cuántos eran "mixtos" bajo la regla ingenua de Commit 3 |
|---|---|---|---|---|
| 2018 | 16,469 | 5,821 | 10,648 | **1,312 = 22.5% del grupo T** |
| 2022 | 22,363 | 8,314 | 14,049 | **2,194 = 26.4% del grupo T** |

La regla **elimina** la ambigüedad de Commit 3 por construcción (ya no hay hogar en dos grupos a la vez ni hogar excluido por mezcla) — pero no la hace desaparecer del resultado: casi una cuarta parte (2018) a más de una cuarta parte (2022) del grupo de tratamiento de corresidencia son, precisamente, los hogares que tienen tanto una persona recién-elegible por regla como una persona que ya era elegible en ambos regímenes. Se declara esta composición explícitamente para que no se lea el grupo T como homogéneo.

**Calibración del paper, heredada como expectativa declarada antes del dato:** su estimado de hogar (`-0.127`) es casi el doble del individual (`-0.066`, §0 arriba). R5.1-D2 debe esperar la misma clase de divergencia entre su desenlace de corresidencia (hogar) y su desenlace de transferencia (persona) — no se lee como error si los dos números no coinciden en magnitud.

## 3 · PASO 4.1 · Triple diferencia — incorporada, con construcción declarada

**Decisión: sí, recomendada, incorporada a la especificación.** Análogo natural en el propio dato, tal como el encargo lo señala: personas por debajo de 65, no elegibles bajo ninguna regla en ninguna ola. Construcción precisa, declarada ahora (el paper usa 55-69 como banda adyacente a su corte de 70, no "toda persona menor a 70" — la misma razón de comparabilidad aplica aquí):

> **Banda de control: personas de 55 a 64 años.** Sobre esa banda, se aplica **la misma regla de §1** (clave `P032`, mismo umbral nominal/deflactado por ola) para construir un T'/C' de placebo — no porque esa banda sea elegible bajo ninguna regla (no lo es, por edad, en ninguna ola), sino para que la comparación T'-vs-C' capture tendencias de ingreso por pensión/jubilación ajenas a la reforma de 2019, con el mismo mecanismo de partición que T-vs-C.

Factibilidad verificada, no solo declarada: 2,980 personas 55-64 sobre el umbral en 2018, 4,084 en 2022 (`P032 > umbral`, universo con ≥1 fila en `ingresos`) — T' no es degenerado en ninguna ola.

**El estimando cambia, declarado:** de una diferencia de brechas [(T-C)_post − (T-C)_pre] a una diferencia de diferencias de brechas **[(T-C)_post − (T-C)_pre] − [(T'-C')_post − (T'-C')_pre]**. `did_ultimate_cluster` (Commit 3 §3) no tiene un tercer nivel — la implementación de la resta final queda para el acto que corra Paso 3: dos llamadas a `did_ultimate_cluster` (una sobre 65+, una sobre 55-64) y la diferencia de sus `theta_hat`, con la varianza sumada por el mismo argumento de independencia entre-olas que ya sostiene `did_ultimate_cluster` — **declarado aquí, no implementado**: no se toca `tests/`.

## 4 · PASO 4.2 · Clustering — R5.1-D2 NO copia al paper, con el argumento escrito

Ya resuelto en Commit 3 §3.2-3.3: el clustering de diseño por (estrato, UPM) que `diff_ultimate_cluster` implementa es el correcto para R5.1-D2, no el clustering municipal del paper. Reforzado aquí con lo que la verificación de fuente añadió (§0 arriba): **los propios autores declaran, en su nota 21, que el municipio no fue su elección ideal** — "we would like to cluster standard errors at the locality level, but we lack locality identifiers". Su clustering geográfico es una segunda-mejor opción forzada por el dato disponible, atada a que **su** tratamiento es geográfico (localidad × edad). El tratamiento de R5.1-D2 no lo es — varía por persona, por su `P032`. Bajo el mismo criterio que el propio paper articula (clusterizar al nivel al que se asigna el tratamiento), copiar su elección municipal sería aplicar la solución de un problema distinto.

**Salvedad, ya declarada en Commit 3, no reabierta:** el ingreso contributivo correlaciona con urbanidad/formalidad — posible correlación intra-municipio en el desenlace que el clustering por UPM no captura. `diff_ultimate_cluster` no acepta una clave de cluster arbitraria (agrega por estrato/UPM de diseño); forzar el municipio como UPM mezclaría diseño con tratamiento. Limitación conocida del estimador, no de esta decisión — sensibilidad por municipio, si mesa la quiere, es acto propio sobre `svystat.py`.

## 5 · PASO 4.3 · Placebo — declarado, dos olas pre-régimen-nuevo

**Factibilidad verificada, no solo citada:** `enigh2012_nc_csv`, `enigh2014_nc_csv`, `enigh2016_nc_csv` — los tres en `data/manifiesto.yaml` con sha256/tamaño, **y los tres presentes físicamente en `data/raw`** (hash real verificado ahora mismo contra el manifiesto, coincide exacto en los tres).

**Placebo declarado: ENIGH 2014 → ENIGH 2018.** Ambas olas bajo el régimen 2014-2018 sin cambio de regla (Commit 3 §1.1: verbatim idéntico en DOF 2014/2015/2018) — nadie cambia de elegibilidad entre esas dos olas por construcción. Misma partición T/C por el corte de $1,092, **sin deflactar**: dado que el umbral nunca se indexó durante ese régimen (mismo hallazgo de Commit 3 citado en su nueva función, §1 arriba), comparar nominal 2014 contra nominal 2018 es exactamente comparable — no hay reforma que aísle, así que no hay razón para introducir un ajuste real que el propio diseño principal solo necesita por el salto 2018→2022. Expectativa a priori, declarada ahora: **DiD≈0, sin significancia** — un efecto que apareciera aquí sería evidencia de tendencia previa que el diseño principal no podría distinguir de un efecto real de la reforma.

## 6 · PASO 4.4 · El enganche entre desenlaces — nombrado, no resuelto

El §5 sellado del pre-registro prohíbe combinar corresidencia y transferencia en un índice, pero no dice qué hacer si uno confunde al otro. El paper lo enfrenta indirectamente (comprueba tamaño de hogar como proxy, p.21-22, porque su corresidencia no es un desenlace propio). **R5.1-D2 no tiene ese problema de segundo orden — mide corresidencia directamente como desenlace #1**, así que puede cruzar los dos desenlaces entre sí en vez de necesitar un proxy adicional.

**Declaración pre-dato, ahora:** si `corresidencia` sube (dirección de sustitución) y `transferencia` baja (misma dirección) en el mismo grupo T, ambas apuntan al mismo canal (la familia sustituye apoyo monetario por convivencia) — lectura consistente, no hay conflicto que nombrar. **El caso que sí hay que nombrar ahora:** si ambos se mueven de forma que uno pudiera explicar mecánicamente al otro — específicamente, si `corresidencia` sube lo suficiente como para que menos personas T vivan en hogares donde recibirían una transferencia registrada como tal (un mayor que se muda con su donante deja de "recibir transferencia" en el instrumento, no porque el apoyo cesó sino porque ya son el mismo hogar) — ese patrón se reporta explícitamente como **confundido por composición del hogar**, no como doble evidencia de crowding-out. No se resuelve con un ajuste estadístico aquí; se nombra la lectura correcta para cuando aparezca el dato, siguiendo la misma prevención que motivó el propio chequeo del paper.

## 7 · PASO 5 · Declaración pre-dato que B-bis exige — el prior de la literatura, cuantificado

Tres estimaciones publicadas de crowding-out en el mismo tipo de programa: **86% Ciudad de México** (Juárez 2009, urbano), **37% rural** (este paper), **~30% Sudáfrica** (Jensen 2004) — con **Galiani y Gertler (2009)** como excepción declarada: sobre la muestra piloto del propio *70 y Más*, las transferencias privadas **aumentaron** 17.5 pesos/mes (no lo contradicen: su muestra cubre solo el entorno de los cortes de edad/localidad del arranque del programa, no representativa a nivel nacional, según el propio paper de referencia, p.8).

**Consecuencia, escrita antes de ver el dato:** la fila **A** del §6 del pre-registro — refutación, DiD<10pp — es, dado el estado de la literatura, **el desenlace menos esperado a priori**, no el default neutral. Commit 1 §3 ya declaró que un resultado corroborante sería más interesante que la refutación; esto lo cuantifica con evidencia externa publicada, no con intuición. **Sube la vara de la fila A:** si el resultado de R5.1-D2 cae ahí, el commit que lo reporte tiene que explicar por qué difiere de tres estimaciones publicadas sobre el mismo fenómeno — no basta con anotar el número y seguir.

## 8 · PASO 6 · Lo que este commit NO resuelve

- **§4 de Commit 3 (precedencia sobre la cláusula de "monto insuficiente" de la fila B) sigue exactamente como Commit 3 la dejó: PROPUESTA a mesa, no regla.** No se reabre aquí. Si el caso ocurre en la corrida real, se para y se reporta con los cuatro elementos crudos.
- **El defecto de `folioviv` en ENIGH 2018 (Commit 3 §3.4): el arreglo `zfill(10)` aplica a los análisis de este acto** (§2-§5 arriba, todos corridos con el arreglo activo). **El re-run de fichas previas de R5.1/P3-LCA que pudieran haber cruzado `poblacion`/`ingresos` 2018 con `concentradohogar` 2018 sin este arreglo es acto propio, fuera de este perímetro — no se toca aquí, ya está registrado** (`forense/hallazgos.md`, entrada de Commit 3).

---

*Commit 4 de este acto (Bloque D). No edita Commits 1 ni 3. Resuelve §1 y §2 por benchmark citado, incorpora las cuatro adiciones del PASO 4, declara el prior de literatura del PASO 5. §4 de Commit 3 sigue sin resolver. Paso 3 del encargo original (la corrida, el veredicto, la fila del registro, la celda-D) sigue diferido — con la especificación ahora completa salvo la propuesta de precedencia.*
