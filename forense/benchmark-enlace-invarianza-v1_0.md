# BENCHMARK-ENLACE · colapsabilidad e invarianza, con literatura

### v1.0 · 13/ago/2026 · ACTO BENCHMARK-ENLACE · redactado contra `origin/main` = `b7aa67c` · Entorno NUBE con búsqueda web · repo-only, sin gate

**Qué es.** Un solo benchmark de literatura para dos preguntas que son la misma pregunta en dos capas — ¿cuándo dos cantidades son comparables? — aplicadas a dos decisiones pendientes de este programa: la función de enlace entre coeficiente marginal y condicional (`D-ABC`) y si ENCUCI y ENBIARE miden el mismo constructo de confianza interpersonal (gate de las 8 producciones de `radio_confianza`, `ADR-67(a)`).

**Qué NO es.** No sella `D-ABC`. No adjudica `radio_confianza`. No ejecuta el acto de vinculación-invarianza. Las dos cosas que este documento entrega son insumo para que mesa las selle, con este benchmark enfrente — el perímetro del encargo lo dice explícito y este acto lo respeta: cero escritura en `canon/**` o `milpa/procedencia.yaml`.

**Nota de vocabulario — "D4" y "D10" no son códigos preexistentes del canon.** El encargo que abre este acto los usa como atajo de sesión. Verificado antes de escribir una sola línea (`grep -n "D4\|D10" canon/estado-programa-v1_10.md canon/gobernanza-v1_15.md forense/hallazgos.md milpa/procedencia.yaml`): existe un **"D4" real en este repo, y no tiene nada que ver con esta pregunta** — es la corrección mecánica del 31/jul/2026 de `milpa/procedencia.yaml` `estado:` ("18/31"→"15/34"), sin ADR, registrada en `forense/hallazgos.md:44` y `gobernanza-v1_15.md:445,1044`. Existe también un "D-09/D-10" en `forense/hallazgos-congelados-2026-07-30.yaml`, cerrado por `ADR-47` ("falsar una regla ≠ calibrar un coeficiente") — otro asunto, ya cerrado. El §S5 de `canon/estado-programa-v1_10.md` ("Pendientes irresueltos", líneas 136-143) no nombra `D-ABC` ni ningún "D4"/"D10" en el sentido de este acto. Lo que este documento cierra, con precisión, es **`D-ABC`** (la función de enlace, nombrada así en `milpa/procedencia.yaml:780,812` y `gobernanza-v1_15.md:832`) y el gate de invarianza de **`ADR-67(a)`** sobre `radio_confianza`. Se escribe aquí para que nadie, leyendo "cierra D4 y D10", los busque en un casillero que no existe o los confunda con los que sí existen y significan otra cosa.

**Procedencia de este documento — léela antes que el contenido.** Tipo (1) todo lo citado del repo (archivo:línea, verificado contra el clon de esta sesión). Tipo (3) toda la literatura externa: búsqueda web (`WebSearch`), nunca lectura directa del PDF/HTML de la fuente primaria — `WebFetch` devolvió `EGRESS_BLOCKED` contra los ocho hosts académicos que este acto intentó (detalle en la nota, `forense/notas/2026-08-13-benchmark-enlace-invarianza.md`), límite del entorno declarado, no silencio. Donde una afirmación de literatura se corrobora por ≥2 fuentes independientes que citan o discuten directamente el artículo primario (no una única cadena de citas), se marca **(3+)** — más fuerte que una sola búsqueda, todavía corto de "se abrió el artículo". Regla de oro del programa, aplicada a bibliografía: nada se afirma de memoria; todo lleva su fuente, verificada en esta sesión.

**Regla de copyright de este acto:** paráfrasis siempre; ninguna cita textual de un artículo o libro salvo una frase corta con comillas y atribución — igual criterio que el resto del corpus forense de este programa ya aplica.

---

## COMMIT 1 · Las preguntas, antes de buscar

*Las seis preguntas de abajo son las del encargo tal como se lanzó — no las formula esta sesión ni las deriva de ningún resultado de búsqueda. Este commit las congela. Lectura de contexto del repo (`BENCHMARKS-metodologicos-D-ABC.md`, `ADR-64`, `ADR-67(a)`, la celda-D de `radio_confianza`) ya estaba hecha al escribir este commit — es premisa necesaria para entender qué se pregunta, exigida por Bloque D/A.1 de `instrucciones-proyecto`, y no cambia lo que se pregunta. Lo que este commit fija es que las respuestas de literatura (Commit 2) no existían todavía en este documento cuando estas preguntas se sellaron, y que el commit de respuestas no reescribe esta sección para que cuadren mejor con lo que la búsqueda encontró — se ve en el diff.*

### Bloque D4 · Colapsabilidad

**Pregunta 1.** ¿Qué medidas son colapsables y cuáles no? `forense/BENCHMARKS-metodologicos-D-ABC.md` §2 ya trae una lectura: diferencia de riesgos y razón de riesgos sí; momio (odds ratio) y hazard ratio no. Verificarla contra fuente — no heredarla. Ese documento es, por su propia cabecera, tipo (3) sin verificar contra los papers ("búsqueda web de mesa... ninguna cita se ha leído en su fuente original").

**Pregunta 2.** La consecuencia que importa para este programa, a responder explícitamente: los β̂ del programa están en diferencia de proporciones, que es colapsable — ¿implica eso que la inversión de signo al condicionar (verificada por el Encargo X sobre `radio_confianza`, `confianza_institucional` y `familismo_apoyo`) es señal real (confusión o modificación de efecto) y no artefacto? Y la segunda mitad: si `D-ABC` declarara enlace logit para un desenlace binario en un índice, marginal y condicional pasarían a ser estimandos distintos por construcción. Decir qué implica cada opción.

**Pregunta 3.** Recomendación para el sello de `D-ABC`, con la forma exacta de texto que trae el encargo: *"enlace declarado por coeficiente; si no es colapsable, se escribe que marginal y condicional son parámetros distintos, no versiones corregidas uno del otro."*

### Bloque D10 · Invarianza de medición

**Pregunta 4.** ¿Cuál es el procedimiento estándar para decidir si dos instrumentos miden el mismo constructo? (configural / métrica / escalar; ítems ancla; invarianza parcial como estado intermedio reconocido — vocabulario que `ADR-67(a)` (`canon/gobernanza-v1_15.md:864`) ya usa sin citar de dónde sale).

**Pregunta 5.** Qué exigiría aplicar ese procedimiento a ENCUCI `AP5_1_1/2/3` (escala 0-10) contra ENBIARE `PB1_01/02` (escala 0-10) — y si es siquiera posible sin muestra común. Esta es la pregunta que gatea las 8 producciones de `radio_confianza` sobre ENBIARE que `ADR-67(a)` desbloqueó como `PROXY_PARCIAL` (`DH-ea9e932f3970ce12`) sin adjudicar.

**Pregunta 6.** La advertencia de `ADR-64` (`canon/gobernanza-v1_15.md`, sellado 5/ago/2026), que este acto no puede ignorar al diseñar la pregunta 5: comparar operacionalizaciones de confianza a través de cortes distintos fabrica conflictos que no existen en el dato — ya ocurrió con `conf.06`, tres reactivos distintos de ENCUCI 2020 al mismo corte que ocho días de propagación incompleta hicieron parecer tres cifras en pugna.

### Reglas del bloque, declaradas antes de buscar

- **Copyright:** paráfrasis siempre, nunca cita larga.
- **Fuentes primarias:** artículo metodológico revisado por pares — no un blog, no un preprint sin revisar salvo que se declare como tal.
- **Regla de oro, extendida a bibliografía:** se lee, no se recuerda. Todo lo que se afirme de un paper lleva autor, año, revista y — donde la búsqueda lo entregue — DOI, verificados en esta sesión.

*Cierra Commit 1. Las respuestas viven exclusivamente en la sección "COMMIT 2" de abajo, en un commit separado que no edita esta sección.*
