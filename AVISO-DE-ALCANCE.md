# Aviso de alcance y limitaciones

**Léelo antes de citar cualquier cifra de este repositorio.**

El resto de la documentación está escrita para quien trabaja dentro del programa y
da por sabido el contexto. Este archivo es para quien llega de fuera.

---

## Qué es esto

Una síntesis de literatura sobre conducta, psicología y estructura social en México
—**31 reports temáticos**<!-- ls corpus/reports/*.md | wc -l -->—, más un modelo de
decisión que convierte esa síntesis en **49 reglas**<!-- python3
tests/validador_registro_ids.py --> segmentadas, más un aparato para refutarlas.

## Qué no es

**No es investigación primaria.** No hay encuestas propias, ni experimentos, ni
trabajo de campo. Todo se apoya en literatura publicada por terceros.

**No tiene revisión por pares.** Ninguna afirmación fue validada por un investigador
independiente.

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

---

---

## Bloque para insertar en `README.md`

*(Va inmediatamente después del título y la línea de descripción, antes de la cita
en bloque que ya existe. No sustituye a este archivo.)*

```markdown
> ### ⚠️ Antes de citar nada
>
> **Síntesis de literatura, sin revisión por pares, escrita en su mayor parte
> por modelos de lenguaje.** Sí hay dato primario propio: **223 payloads**
> <!-- grep -cE '^\s*sha256:' data/manifiesto.yaml --> con `sha256` y estimandos
> propios sobre ENVIPE/ENCIG/ENCUCI/ENIF/ENIGH, con un estimador
> (`tests/svystat.py`) respaldado contra tres casos de referencia (Encargo E-3,
> PR #97) y validado contra cifras publicadas de INEGI en al menos dos actos
> (Encargo K, ENVIPE; Encargo P, ENIGH). El modelo en sí sigue mayormente sin
> medir: de los 144 números, 4 están medidos (`4 de 144`, **[MESA-M4]**:
> congelado 31/jul/2026, no se recalcula); de los 15 coeficientes en escala del
> modelo, ninguno — tres asociaciones marginales existen pero ADR-57(a) las
> excluye del conteo. Y la mayoría de las 49 reglas sigue descansando en
> síntesis de literatura, no en dato propio: **36 de 49**
> <!-- 49 (validador_registro_ids.py) − 13 (fichas del bloque append-only,
> T18) = 36 --> sin corrida de falsación pre-registrada. El corpus
> sobre-muestrea al clasemediero urbano formal y deja el sistema
> indígena-comunal **fuera por diseño**.
>
> Léelo entero en **[`AVISO-DE-ALCANCE.md`](AVISO-DE-ALCANCE.md)**.
> Autoría e IA en **[`AUTHORSHIP.md`](AUTHORSHIP.md)**.
> Si piensas usar el modelo sobre personas concretas:
> **[`USO-ACEPTABLE.md`](USO-ACEPTABLE.md)** — la respuesta corta es que no.
```
