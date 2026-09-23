# Aviso de alcance y limitaciones

**Léelo antes de citar cualquier cifra de este repositorio.**

El resto de la documentación está escrita para quien trabaja dentro del programa y
da por sabido el contexto. Este archivo es para quien llega de fuera.

---

## Qué es esto

Un benchmark auditable de estimaciones y predicciones segmentadas sobre
microdatos oficiales, con especificaciones, RESULT y sellos por evaluación.
Conserva un corpus de reports y el modelo de decisión anterior. El [informe
v1.2](canon/informe-programa-v1_2.md) distingue los pilotos prospectivos
respecto de R, las comparaciones retrospectivas y las reservas de alcance.
Sellar antes de abrir R no equivale a sellar antes de la publicación de una ola.

En julio la portada describía sobre todo síntesis de literatura y un modelo
asignado por juicio. Las mediciones GEN2 añadieron contrastes sellados desde
microdato oficial; no borraron esa historia ni validaron por ello todos los
parámetros del modelo.

## Qué no es

**No hay encuesta propia, experimento ni trabajo de campo.** Sí hay estimaciones
propias sobre microdatos de terceros, con unidad y universo declarados por CALC.

**No tiene revisión por pares del conjunto.** Existen validaciones independientes
de resultados concretos; no se extienden al resto del repositorio.

**No es un instrumento validado.** De los 144 números del modelo, **4 están
medidos** <!-- modelo §6.1 (90 params_base + 15 coeficientes + 39 probabilidades =
144; 4 MEDIDO); forense/hallazgos.md, 2026-07-31: "Congelamiento de `4 de 144`" —
decisión de mesa, no ADR --> — `4 de 144` sigue **[MESA-M4]**: congelado 31/jul/2026
por decisión de mesa, no se recalcula. De los 15 coeficientes de generador,
**ninguno está en escala del modelo** <!-- modelo §2.2 ("Los quince coeficientes
son ASIGNADO. Ninguno es medido"); milpa/procedencia.yaml:
asignados_coeficiente / coeficientes_generador_medidos --> — tres asociaciones
marginales (β̂) existen (Encargo W), pero ADR-57(a) las rotula asociaciones, no
coeficientes: ninguna sobrevive condicionar. Una regla marcada `[FUERTE]` significa
que la literatura la sostiene bien, no que su probabilidad esté calibrada contra
datos.

**No fue escrito principalmente por un humano.** Ver `AUTHORSHIP.md`.

---

## Los cuatro sesgos que hay que conocer

**Clase.** El corpus sobre-muestrea al clasemediero urbano formal y sub-muestrea al
popular informal, que es el peso demográfico dominante del país. Está declarado y no
corregido. Cualquier afirmación sobre "los mexicanos" hay que leerla con ese peso
encima.

**Alcance institucional.** El sistema indígena-comunal vivo —asamblea, cargos,
tequio, usos y costumbres— queda **fuera por diseño**. No es un hueco: es otro orden
institucional, con su propia lógica, que este corpus no cubre y sobre el que no debe
extrapolarse.

**Procedencia de la evidencia.** Parte del material proviene de muestras
mexicano-americanas, sujetas a aculturación y selección migratoria, que no son
evidencia directa sobre población en México. Se marcan `(b)` donde se detectaron; la
suite documenta que el marcado está incompleto.

**Marcos importados.** Hofstede, GLOBE, WVS y las tipologías honor/dignidad/face
aparecen en el corpus. Se usan con crítica declarada, pero la suite detecta ocho
lugares <!-- python3 tests/check.py → T09 --> donde un marco importado se usa
como causa sin la marca `(c)`.

---

## El repositorio publica sus propios defectos

Es deliberado. `python3 tests/check.py` corre una suite de verificación contra
el propio corpus y congela su recuento de FAIL/WARN como línea base — córrelo
para ver la cifra vigente; no se teclea aquí porque una cifra tecleada se
desactualiza sin que nadie lo note (le pasó a este mismo párrafo — ver
`forense/hallazgos.md`, ENCARGO MT-mantenimiento). El CI está verde porque no
ha empeorado, no porque no haya nada roto.

Entre lo que la suite documenta <!-- python3 tests/check.py → T06/T07/T08 -->:
siete valores distintos del coeficiente de Gini circulando en el corpus, doce
valores distintos de confianza interpersonal, siete vocabularios de tier
incompatibles, y siete reports sin mapa de evidencia.

`forense/` contiene el registro fechado de los errores que el programa encontró
auditándose. Es append-only: nada de eso se borra ni se reescribe.

Un hallazgo de método que conviene tener presente: **varios de los defectos más
graves no los encontró la suite**. Los encontró alguien pidiendo la cita textual de
una cifra que todo el mundo daba por buena.

---

## Cómo usarlo bien

Como punto de partida documentado y falsable. Trae siempre el tier y la marca de
procedencia junto a cualquier cifra que cites. Si una afirmación te importa de
verdad, ve a la fuente original que el report cita y verifícala tú.

Y si vas a usarlo para decidir algo que afecte a personas concretas, lee primero
`USO-ACEPTABLE.md`. La respuesta corta es que no deberías.
