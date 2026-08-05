# Autoría y uso de modelos de lenguaje

**Este repositorio se produjo con asistencia intensiva de modelos de lenguaje.**
No es un detalle de método: es la condición de existencia del corpus. Se declara
aquí con el mismo nivel de precisión que el programa exige para cualquier otra
afirmación de procedencia.

---

## 1 · Quién hizo qué

**Autor responsable:** Jonatan Jahzeel Guadarrama García — GitHub `Josanoforo`.
Responde por el contenido publicado, incluidas sus faltas. Fijó el objeto de
investigación, el reglamento de rigor (`instrucciones-proyecto-v2.md`), las
prioridades de cada sesión, y decidió qué entraba al canon y qué se descartaba.

**Modelos de lenguaje (familia Claude, de Anthropic).** Redactaron el texto de los
reports temáticos a partir de búsqueda de literatura; escribieron la suite de
verificación y los artefactos forenses; ejecutaron auditorías contra archivo; y
co-redactaron el canon. La mayor parte del texto publicado tiene autoría material
de un modelo.

**Ninguna afirmación de este repositorio está avalada por revisión por pares, ni
por un investigador humano independiente.**

---

## 2 · Lo que dice el registro

Derivado en sesión con `git log`, no escrito de memoria (HEAD `c3adff8`,
30/jul/2026):

| | |
|---|---|
| Commits totales | 37 |
| Autor `Claude <noreply@anthropic.com>` | 21 |
| Autor `Jonas <jonieqsa@gmail.com>` | 12 |
| Autor `corpus <corpus@local>` | 4 |
| Trailers `Co-Authored-By` nombrando a un modelo | 29, en cinco formas |

**La historia no se reescribe.** Los primeros 21 commits registran a un modelo
como autor y a ningún humano, y eso queda: es el registro fiel de cómo se hizo el
trabajo. Falsificarlo sería falsificar procedencia — el defecto exacto que este
programa existe para atrapar. El hallazgo está documentado en
`gobernanza §4` (**ADR-41**), y el esquema corregido —autor humano,
modelo como co-autor, con el nombre del modelo como campo variable— en **ADR-43**.

De ahí en adelante, cada commit declara qué modelo lo co-escribió.

---

## 3 · Qué controles existen, y qué no controlan

El riesgo obvio de un corpus así es la fabricación: citas inventadas, cifras
plausibles sin fuente, síntesis que suena bien y no se sostiene. Contra eso hay
maquinaria real, y conviene saber qué alcanza:

**Existe.** Una suite de verificación automática (`tests/check.py`) que corre en
CI sobre cada push y cada PR, y que documenta como deuda conocida y congelada
un recuento de FAIL/WARN que se mueve con cada corrección — la cifra vigente
se deriva corriendo `python3 tests/check.py`; no se teclea aquí porque una
cifra tecleada se desactualiza sin que nadie lo note (le pasó a este mismo
párrafo — ver `forense/hallazgos.md`, ENCARGO MT-mantenimiento). Ver también
`README.md` (`## Estado del modelo`) para el resto de los números vivos del
modelo. Un sistema de tierización de evidencia. Marcas de procedencia
`(a)` dato en México / `(b)` muestra de diáspora / `(c)` marco importado. Un
registro append-only de errores propios en `forense/`. 43 decisiones de arquitectura
razonadas.

**No existe.** Verificación humana independiente de las fuentes citadas, una por
una. Un tercero que haya releído el corpus completo. Datos primarios propios: todo
es síntesis de literatura publicada.

**Lo más honesto que se puede decir del método:** varios de los defectos más graves
del programa no los encontró la suite — los encontró alguien pidiendo la cita
textual de una cifra. Está documentado en `forense/`. Léelo antes de confiar en el
resto.

---

## 4 · Cómo leer esto

Un corpus asistido por IA no es por eso falso, y no es por eso verdadero. Es una
síntesis de literatura con un aparato de auditoría inusualmente explícito y sin
revisión externa. Trátalo como lo que es: un punto de partida documentado y
falsable, no una fuente de autoridad.

Si encuentras un error, ábrelo como issue. El registro es append-only: se corrige
con nota fechada, nunca en silencio.
