# Informe del programa · v1.0

**Modelado Mexicano — «Psicología del Mexicano Contemporáneo».**
Documento del programa, escrito para un lector externo. 15 de septiembre de 2026.

### `informe-programa` · **v1.0** · DOCUMENTO DEL PROGRAMA

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_0.md` |
> | **REEMPLAZA A** | — (artefacto nuevo, sin predecesor: el primero de su clase. El índice de infraestructura no tenía fila para esta clase de documento y se le añadió en la misma entrega, regla de conducto `ADR-70(c)`) |
> | **VERIFICAS ASÍ** | cada cifra del cuerpo tiene su fila en `canon/informe-programa-v1_0-ANEXO.md`, con universo (`A.10`) y comando; las dos derivaciones propias del anexo (§A.2, §A.3) llevan control positivo que reproduce cifras ya selladas; el módulo de auditoría de rigor extremo va contestado en §6, incluida la pregunta [NUEVO v2.3] |
> | **NOMBRE ESTABLE** | **`informe-programa`** — cítalo así, **nunca por nombre de archivo** |

> **Estampa de universo (A.10), global.** Derivado contra `origin/main = eba9fd2`
> (merge de `PR #788`, 15/sep/2026) — **re-derivado** desde `5973f12`, la base
> original, al integrar `main`: ver la nota de re-sello del anexo §A.1. En un
> acto de NUBE sin corpus montado
> (`tools/entorno.py`: `corpus=NO(examinados=0)`, `data_raw:NO`, red no ejecutada).
> **Fuentes: solo registro derivado y notas selladas.** Este informe no abre
> microdato, no hace llamadas a ningún modelo, no sella ninguna corrida y no
> mueve ningún contador. Cada cifra de abajo lleva su universo en el anexo
> (`canon/informe-programa-v1_0-ANEXO.md`); una cifra sin universo declarado no
> entra aquí.
>
> **Lo que este documento NO es:** no es una adjudicación, no re-abre ningún
> veredicto, y no es el sello de **D-A** (§D2 de la firma de mesa del 15/sep),
> que al escribirse esto todavía no existe en el árbol.

---

## 0 · En una página

El programa construye un modelo de decisión sobre conducta en México
(`canon/modelo-decision-v4_0.md`) a partir de fuentes públicas mexicanas
—encuestas de INEGI y otras—, con un aparato que obliga a que toda cifra que
entra al modelo tenga fuente, universo, unidad, ola y código verificables.

Hay tres piezas que conviene no confundir:

| pieza | qué es | qué NO es |
|---|---|---|
| **R** | la estimación derivada del microdato por el propio programa: el **árbitro**. Diseño muestral, ponderador y códigos explícitos | no es «la verdad»; tiene error estándar, y se publica con él |
| **M** | el **motor**: la regla del modelo emite un punto para una celda | no es un predictor acreditado. Ver §2 |
| **L** | un **modelo de lenguaje** respondiendo la misma pregunta, en dos brazos: `L_SOLO` (sin contexto) y `L_CORPUS` (con un paquete documental) | no es una fuente; es el competidor del duelo |
| **B** | una **línea base tonta**: «lo de la ola anterior de la misma serie» (persistencia) | no es una tesis ni un modelo. Es un piso de comparación |

Durante agosto y septiembre de 2026 el programa corrió un duelo (**F5**) entre
esas piezas sobre 14 celdas con árbitro, y este informe dice qué salió, qué se
puede usar, y qué no.

---

## 1 · La tesis, tal como la mesa la fijó

Se reproduce **verbatim** de la firma de mesa del 15/sep/2026 (§D1). Este
documento no la reinterpreta ni la suaviza:

> **D1 · Tesis.** Se acepta: mediciones reproducibles, éxito documental local y
> persistencia competitiva; el valor predictivo añadido de M queda por
> demostrar. M conserva sus otras funciones (organización de evidencia,
> aplicación consistente de reglas, escenarios), que se distinguen de la
> precisión predictiva y se acreditan por función. Esta reserva no es un juicio
> negativo del proyecto.

Traducido para un externo, sin añadir nada: **el programa mide bien y deja
rastro; que su motor *prediga mejor que una alternativa barata* todavía no está
demostrado.** Las otras funciones de M no quedan tocadas por esa reserva —
pero se acreditan una por una, no en bloque.

---

## 2 · Qué podemos usar hoy, y para qué

La regla de lectura es **por función acreditada**, no por nombre del artefacto.

### 2.1 · Lo que está acreditado y se puede usar

| pieza | función acreditada | evidencia | límite |
|---|---|---|---|
| **R** (14 celdas del panel F5, y las series del registro GEN2) | **medición descriptiva reproducible** con diseño muestral | 72 corridas selladas, 3 255 RESULT GEN2, 199 con validación independiente, `diferencias_materiales=0` | descriptiva; no es efecto causal |
| **B · persistencia** | **piso de comparación** para cualquier duelo futuro | 10 de 14 celdas cubiertas, control positivo `REPRODUCE-EXACTO` con `Δ = 0.0` en 10/10 | **no es ciego** (contaminación declarada TOTAL); no es una tesis sobre México |
| **Recuperación documental sobre paquete preparado** (F5 secundaria) | **convertir una fuente nativa en un punto trazable** | 16/16 réplicas dirigidas produjeron punto trazable; 0/16 con contexto temático | **local**: dos celdas, dos paquetes ya adquiridos. No es generalización |
| **M** | **organización de evidencia · aplicación consistente de reglas · escenarios** (D1) | el aparato de linaje, procedencia y trámite del motor | **no** precisión predictiva: ver 2.2 |

### 2.2 · Lo que NO está acreditado

**El valor predictivo añadido de M.** El duelo primario terminó en
`SIN-GANADOR-UNICO`: sobre las 12 celdas del universo común, M erró más que los
dos brazos de L (4.99 pp contra 3.89 y 3.96), pero ese orden **depende de cómo
se pesen las celdas** y por eso no se adjudicó ganador. Ver §3.1 — esta es la
cifra más fácil de citar mal de todo el informe.

**La transferencia de M a familias no vistas.** No se ha probado. La propuesta
existe (F6) y está compuertada; ver §4.

**Cualquier lectura de B como resultado sobre México.** B es aritmética sobre
la ola anterior. Que le gane a M en 8 de 10 celdas es un **diagnóstico** —dice
que el panel premia la persistencia— no una tesis.

---

## 3 · Qué comparaciones son válidas — y cuáles no

### 3.1 · La dependencia de composición, declarada

El resultado primario `SIN-GANADOR-UNICO` viaja siempre con este par de hechos,
y citarlo sin ellos lo tergiversa:

- **68.88%** del error de M sobre el universo común lo aportan **seis celdas de
  una sola familia** (cívicas, ENVIPE). No son seis confirmaciones
  independientes del mismo defecto: comparten parámetro y mecanismo.
- **El orden se invierte si se pesa por grupo en vez de por celda.** Con igual
  peso por celda M pierde (4.99 vs 3.89/3.96 pp); con igual peso por familia M
  gana (5.03 vs 7.53/7.32 pp). Mismo dato, dos composiciones, dos rankings.

Por eso no hay ganador: **el panel no tiene resolución para adjudicar uno.** La
conclusión honesta no es «L gana», ni «M gana», sino que la pregunta está mal
dimensionada con 12 celdas repartidas en 5 familias. Tabla completa en el anexo
§A.2.

### 3.2 · Universos que no se mezclan

| comparación | válida | por qué |
|---|---|---|
| M vs L sobre las 12 celdas de `U3` | **SÍ**, con §3.1 pegada | mismo universo, mismo árbitro |
| B vs M vs L sobre las **9 celdas comunes** | **SÍ**, descriptiva, sin IC | es la comparación de §D2, derivada en el anexo §A.3 |
| `MAE` de 14 celdas contra `MAE` de 10 | **NO** | otro universo. El marginal de 14 (`4.5066`) y el de 10 (`4.3073`) no se restan |
| la primaria (`SIN-GANADOR-UNICO`) junto con la secundaria (16/16 documental) | **NO como una sola lectura** | miden cosas distintas: precisión predictiva vs. recuperación documental. Esa lectura conjunta es de mesa y dirección, no del registro |
| el reanálisis protegido (`NO-ADJUDICABLE-POR-CONTROL`) como corrección de la corrida histórica | **NO** | contrato distinto y posterior. No «rescata» un ganador |

### 3.3 · La regla general

**Un cierre no puede concluir más ancho que el universo que declaró** (A.10,
corolario 2). En la práctica: antes de citar cualquier cifra de este informe,
lea su fila en el anexo. Si la fila dice `n=9`, la frase no puede hablar de 14.

---

## 4 · Dónde falta evidencia

Ordenado por lo que bloquea, no por antigüedad.

| hueco | estado | qué lo desbloquea |
|---|---|---|
| **Transferencia de M** a familias no vistas | `FP-374` **ABIERTA**. 0 familias retenidas ejecutables: el snapshot tiene 10 familias conocidas durante el desarrollo y ninguna con rol retenido | la **lista nominal** de 6 familias piloto + 12 confirmatorias, con acceso y consumidor, **antes de cualquier llamada** (§D4). Sacar `NC-0161`/`NC-0162` de espera es consecuencia de esa lista, no sustituto |
| **Comparabilidad cívica** (el 68.88%) | diagnosticado, no reparado. El error mezcla desfase semántico y temporal con precisión | una tarjeta M/R con igual unidad, recorte, códigos y ola — **o** excluir la pareada por no comparable. Se cambia la evaluación antes de tocar el parámetro |
| **Cobertura de B** | 10 de 14. Las 4 restantes no se rellenan: primera ola del panel, reactivo que nace después, serie de una sola ola, reactivo ausente en la ola previa | nada por ahora: un `B` por crosswalk saldría de la familia y es decisión de mesa (`NC-0179`) |
| **Generalización del éxito documental** | 2 celdas, paquetes ya adquiridos | celdas nuevas con paquete adquirido y congelado antes de capturar |
| **Incertidumbre total del duelo** | los IC pareados actuales tratan R como fijo | integrar simultáneamente el EE de R y la variación entre réplicas de L |
| **Consumo de B-MARCO** | 471 RESULT, **0 adopciones**, por diseño | la próxima corrida de tríada que consuma `MAE_pp(B)` (`NC-0187`) — no un acto de adopción al motor |

**Un hueco de infraestructura, encontrado por este acto y corregido en la misma
entrega:** el índice de infraestructura (`data/INFRAESTRUCTURA-v1_0.md`) no tenía
fila para «voy a escribir un documento del programa». Se añadió, por regla de
conducto (`ADR-70(c)`).

---

## 5 · Reglas de decisión

Forma `SI [condición] ENTONCES [qué se puede hacer] — PORQUE [evidencia]`.

1. **SI** se necesita una cifra descriptiva sobre México con diseño muestral
   **ENTONCES** se usa **R**, citando ola, unidad, universo, códigos y su EE —
   **PORQUE** es lo único del programa con validación independiente y
   `diferencias_materiales=0`.
2. **SI** se quiere afirmar que M predice mejor que una alternativa
   **ENTONCES** no se hace con este panel — **PORQUE** el resultado es
   `SIN-GANADOR-UNICO` y su orden se invierte al cambiar la ponderación (§3.1).
3. **SI** se cita `SIN-GANADOR-UNICO` **ENTONCES** viaja con el 68.88% y con la
   inversión por grupo — **PORQUE** sin ellas la cifra afirma una resolución que
   el panel no tiene.
4. **SI** se usa M para organizar evidencia, aplicar reglas de forma consistente
   o construir escenarios **ENTONCES** se puede, acreditando **esa** función —
   **PORQUE** D1 las conserva y las distingue de la precisión predictiva.
5. **SI** un duelo futuro compara brazos **ENTONCES** incluye **B** como piso,
   con sus reglas fijadas antes de ver resultados — **PORQUE** ganarle a L no
   acredita ganarle a B (§D3).
6. **SI** se cita B **ENTONCES** se declara que no es ciego y que es
   diagnóstico — **PORQUE** su contaminación es TOTAL por construcción y
   declarada.
7. **SI** se quiere abrir F6 **ENTONCES** primero la lista nominal de 6 + 12
   familias reservadas, y **cero llamadas** antes de ella — **PORQUE** una
   familia que se evalúa sin estar reservada deja de ser retenida para siempre.
8. **SI** una fuente no permite el estimando **ENTONCES** la abstención es el
   resultado correcto y se registra como tal — **PORQUE** las 16 abstenciones de
   F5 fueron válidas: el acceso funcionó y faltó el documento, no la capacidad.
9. **SI** dos cifras vienen de universos distintos **ENTONCES** no se restan ni
   se ordenan juntas — **PORQUE** A.10 corolario 2.

---

## 6 · Módulo de auditoría de rigor extremo

Este documento afirma algo sobre el modelo, así que el módulo es obligatorio
(`instrucciones-proyecto-v2_13.md`, [REFINADO v2.3]). Contestado, no recitado.

**[NUEVO v2.3] ¿Cuántos contadores movió el trabajo que produjo este
artefacto?** **Cero.** (Se dice al inicio del módulo, sin justificarlo, como
manda la regla.)

**¿Qué parte del análisis podría estar confundiendo pobreza, desigualdad,
violencia o informalidad con «cultura»?** Ninguna afirmación de este informe es
sobre conducta mexicana: todas son sobre el aparato de medición. El riesgo se
traslada a los artefactos que sí afirman (los reports y el modelo de decisión),
donde el módulo se contesta por separado.

**¿Qué parte podría estar sobregeneralizando desde clases medias urbanas?** El
panel F5 hereda la cobertura de ENVIPE/ENCIG/ENIGH/ENIF/ENCUCI/ENNViH, que son
nacionales con diseño probabilístico. Pero **6 de 12** celdas del universo común
son de una sola familia cívica: cualquier lectura del duelo está sobreponderando
un dominio, y §3.1 lo dice en la cifra.

**¿Qué parte está sesgada por literatura escrita desde marcos estadounidenses o
europeos?** El brazo `L_SOLO` es un modelo de lenguaje entrenado
mayoritariamente en inglés, respondiendo sobre México sin contexto. Que gane a M
por MAE en algunas celdas no acredita conocimiento del caso mexicano: puede ser
regresión a un prior plausible. El informe **no** lo lee como ventaja de L.

**¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?**
No se sabe, y se dice: ninguna celda del panel está estratificada por esos ejes.
El duelo se corrió sobre agregados nacionales.

**¿Qué parece psicológico pero en realidad es un incentivo racional ante un
entorno específico?** No aplica directamente: este documento no interpreta
conducta. Sí aplica su análogo de aparato — el error de M en las cívicas **parece**
imprecisión del motor y en realidad es **uso/evaluación no alineados** (unidad,
recorte, códigos y ola distintos). Confundir los dos llevaría a «ajustar el
parámetro» contra un desalineamiento semántico.

**¿Dónde hay evidencia débil pero intuición social fuerte?** En leer
`SIN-GANADOR-UNICO` como «el modelo no sirve» o como «el LLM ya sabe». Ambas son
intuiciones fuertes y el dato no sostiene ninguna.

**¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?**
Tres: (a) «B le gana a M, el motor sobra» — B es aritmética sobre la ola previa y
no es ciego; (b) «16/16 prueba que el sistema recupera documentos» — son dos
celdas con paquetes ya adquiridos; (c) «el reanálisis protegido corrige la
corrida histórica» — es otro contrato, no una corrección.

**[NUEVO v2.1] ¿Qué afirmación describe el estado del corpus y no fue derivada,
sino escrita a mano?** Ninguna. Los conteos de §2.1 y §4 salen de
`tools/corrida0.py status` y `tools/tablero_programa.py --json` corridos en este
acto; las cifras del duelo salen de las notas selladas y de sus TSV, con el
comando pegado en el anexo. La derivación de §3.1/§A.3 se validó con un control
positivo: reproduce al cuarto decimal las cuatro cifras que la nota sellada de
B-MARCO ya publicaba.

**[NUEVO v2.2] ¿Qué deuda «asumida a propósito» debe re-examinarse porque cambió
la función del programa?** Una, y está viva: el panel F5 se diseñó para
**evaluar uso documental**, con transferencia como secundaria. La función que la
mesa quiere ahora (§D3) es **evaluar transferencia**. La deuda «0 familias
retenidas» era tolerable mientras la pregunta era la primera; con la segunda
pasa a ser el bloqueo principal, y por eso `FP-374` sigue ABIERTA en vez de
cerrarse por inercia.

**[NUEVO v2.4] ¿En qué escala están las cantidades, y contra qué se comparan?**
Todos los `MAE` y `err_pp` de este informe están en **puntos porcentuales de una
proporción ponderada**, `err_pp = 100·(punto − R)`, comparados contra **R** como
árbitro. Ningún número de este documento entra al motor: no hay `p`, coeficiente,
corte ni momento adoptable aquí.

---

## 7 · Procedencia

Todo lo citado arriba está sellado en el repositorio; el anexo da ruta y comando
por cifra. Las dos piezas que la firma de mesa menciona y que **no** están en el
árbol —la *LECTURA ESTRATÉGICA F5 v1.1* y el adversarial de Astra— no se
reconstruyen ni se citan como leídas: son documentos de mesa, y su ausencia se
declara en vez de ocultarse.

El **sello de D-A** (§D2: la comparación descriptiva de 9 celdas como corrida de
registro) no existía al escribirse esto. El informe **no lo espera** (§D5): la
tabla de §A.3 es derivación propia con procedencia declarada, y **no** sustituye
a ese sello. Cuando D-A selle, esta versión queda `VENCIDA EN ALCANCE` en esa
tabla y se re-sella contra el universo nuevo — nunca editando ésta.

**Anexo técnico:** `canon/informe-programa-v1_0-ANEXO.md`.
