# Corrida de la batería de refutaciones
### 49 refutaciones contra el modelo · primera ejecución

*27 de julio de 2026. Leídos: `refutations.yaml` completo y `modelo-decisiones-mexicano.md` §1, §2, §3. Cero investigación nueva.*

---

## 0 · El problema de encuadre, y el reencuadre que hace la corrida posible

Por la tipología del **propio archivo**, la batería es hoy inejecutable en su totalidad:

| Tipo | Cuenta | Requiere | Estado |
|---|---|---|---|
| **A · mecánica** | 28 | El simulador | ❌ ausente |
| **B · paramétrica** | 11 | `validate.py` | ❌ ausente |
| **C · de lectura** | 10 | *"no ejecutable"* por definición | — |

**Cero de 49.** Ese habría sido el resultado si me atengo a cómo están escritas.

Pero las `falla_si` dicen todas *"el sim produce…"* y **esa no es la única lectura posible**. Una refutación que prohíbe un mecanismo prohíbe primero que el **modelo** lo codifique — y el modelo sí es legible. Reformulada así, la pregunta pasa de *"¿el simulador reproduce el mito?"* a **"¿el motor §3, los seis generadores o los 107 números codifican el mito?"**.

Con ese reencuadre, **30 de 49 se pueden correr hoy por lectura.**

---

## 1 · Resultado

| Veredicto | Cuenta |
|---|---|
| ✅ **PASA** — el modelo codifica el mecanismo estructural, no el mito | **27** |
| ❌ **FALLA** — el modelo codifica el mito que la refutación prohíbe | **3** |
| ⚠️ **SIN OBJETO** — el modelo no tiene la entidad o variable que se prueba | **8** |
| 🔒 **REQUIERE EJECUTABLE** — solo verificable con el simulador o el validador | **11** |

**El corpus se defiende bien: 27 de 30 refutaciones corribles pasan.** Los tres fallos son concretos, ya diagnosticados en otro lado, y reparables. Los ocho sin objeto son el hallazgo menos esperado.

---

## 2 · Los tres fallos

### FALLA 1 · `ref.B.09` — la confianza institucional está codificada como escalar

**El mito prohibido:** *"Los mexicanos no confían en las instituciones."*

**Lo que dice el modelo:** `§1.1` lista *Confianza institucional* como **una sola escala** (`baja / muy baja`) en la tabla de parámetros de los seis perfiles.

**Por qué falla:** un escalar predice que quien desconfía de la policía desconfía de la Marina. **Es falso y está medido**: Marina 89%, familia 87%, escuelas públicas 77%, universidades 76% vs. partidos 23.9%. El modelo codifica exactamente el mito que la refutación prohíbe.

⚠️ **Ya estaba diagnosticado.** **ADR-28.b** ordena convertirlo en **vector, no escalar**. Sigue sin incorporar. La refutación lo habría cazado el primer día que se corriera — y esta es la primera vez que se corre.

### FALLA 2 · `ref.A.23` — el coeficiente de familismo no puede representar el efecto que el corpus documenta

**El mito prohibido:** *"El familismo protege la salud mental."*

**Lo que dice el modelo:** `G5 → familismo: 0.50`, **monotónico positivo**.

**Por qué falla:** el corpus documenta un efecto **dual, no monotónico**. El meta-análisis de Cahill (2021) halla menos síntomas internalizantes y externalizantes — pero el **familismo obligatorio** (la creencia de que uno debe sacrificarse por la familia) **no es protector y puede ser factor de riesgo** (Zeiders 2013), y la relación con el logro académico es **curvilínea**: las obligaciones más altas producen calificaciones tan bajas como las más débiles (Fuligni 1999).

**Un coeficiente monotónico positivo no puede representar una relación curvilínea.** No es que el número esté mal calibrado: es que la **forma funcional** no admite el hallazgo. Subir `familismo` siempre mejora, cuando la evidencia dice que pasado cierto punto empeora.

*Este fallo es nuevo — no estaba diagnosticado en ningún ADR.*

### FALLA 3 · `ref.B.11` — los perfiles no tienen dispersión

**El mito prohibido:** *"Los miembros de un segmento se comportan igual."*

**Lo que dice el modelo:** `§1.1` asigna a cada perfil **valores puntuales** (`corto`, `alta`, `muy baja`), no distribuciones.

**Por qué falla:** un perfil con parámetros puntuales genera agentes idénticos. Es literalmente el mito. Y choca con el propio texto del modelo, que advierte que *"no son tipos puros: una persona real combina rasgos"* y que **la variación intranacional suele ser mayor que la internacional** (Fischer & Schwartz, citado en moral emotions).

El modelo **dice** que los perfiles se solapan y **codifica** que no.

---

## 3 · Las ocho sin objeto — el hallazgo inesperado

Ocho refutaciones no pueden fallar porque **el modelo no tiene qué probar**:

| Refutación | Tier | Qué falta en el modelo |
|---|---|---|
| **`ref.A.02` esfuerzo laboral** | **MUY_FUERTE** | **No hay variable de esfuerzo ni de horas.** Cero reglas |
| `ref.A.04` pobres no pagan | FUERTE | **No existe la entidad prestamista** (mismo hueco que `bt.credito_riesgo_del_prestamista`) |
| `ref.A.14` no cree en terapia | FUERTE | **No hay dominio de salud mental** — pese a existir un report entero |
| `ref.A.20` emprendimiento vibrante | MEDIA | Sin variable de emprendimiento |
| `ref.A.28` e-commerce transformador | MEDIA | Sin canal de compra |
| `ref.B.04` colorismo estructural | FUERTE | **El tono de piel no es parámetro** de ninguno de los seis perfiles |
| `ref.B.06` fatalismo no es religioso | FUERTE | Sin parámetro de religiosidad |
| `ref.A.17` líder fuerte ≠ autoritarismo | MEDIA | Parcial: `§3.2` distingue liderazgo benévolo de autoritario, pero no hay ítem actitudinal |

**Dos de estas duelen especialmente.**

`ref.A.02` es **la única MUY_FUERTE de las 49** — el tier más alto de toda la batería, con el dato más contundente del corpus (2,207 h/año, el mayor de la OCDE, 26% sobre el promedio; la baja productividad es déficit de capital, no de esfuerzo). Es la refutación del mito más dañino que existe sobre México. **Y el modelo no tiene dónde alojarla.**

`ref.B.04` deja el colorismo fuera del aparato: es `Fuerte (correlación)` en el glosario, predice educación, ingreso y movilidad — y no es parámetro de ningún perfil. La refutación no puede protegerlo porque no hay nada que proteger.

---

## 4 · Un desajuste de tier

**`ref.A.09` "los pobres venden su voto"** está tierizada **FUERTE** en la batería. La regla correspondiente del modelo —`§3.7`, transferencia directa universal → conserva autonomía de voto— está en **`[HIPÓTESIS]`**.

El modelo **sub-califica** lo que V2 validó con RCTs revisados por pares y un contrafactual limpio (2018: AMLO ganó por 31 puntos repartiendo *menos* dádivas). El glosario v5 la tiene en **Fuerte** y la llama *"el único constructo del corpus con identificación causal"*. Y el Hito 2 confirmó que V2 es el único vertical cuyas reglas ancla son fieles al motor.

Tres artefactos dicen Fuerte; el motor dice Hipótesis. **Es propagación pendiente, no desacuerdo.**

---

## 5 · Las 27 que pasan

El corpus aguanta bien, y en varios casos con la refutación escrita **dentro de la regla**. Los ejemplos más limpios:

- **`ref.A.01` vacunación** → `§3.9`: *"SI la vacuna está disponible y la campaña llega ENTONCES la mayoría acepta — PORQUE el default es aceptación y **el hueco es logístico (no actitudinal)**"* `[FUERTE]`. La refutación está literalmente en el PORQUE.
- **`ref.A.06` impuntualidad** → `§3.6`: el interruptor formal/informal con checador y sanción. El mito no tiene dónde entrar.
- **`ref.A.07` mordida** → `§3.3`: *"SI el trámite se digitaliza / hay testigos ENTONCES la mordida baja"*. Codifica un equilibrio, no un rasgo.
- **`ref.A.26` desconfía del experto** → `§3.9`: *"SI es caro, lejano o ya falló ENTONCES prevalece 'yo sé por experiencia' — PORQUE adaptación racional"*.
- **`ref.B.07` cultura de honor** → `§3.10` trae la nota explícita: *"el driver es adaptación racional + face bajo dignidad, **NO 'honor'**"*.
- **`ref.A.15` familismo amoral** → `§3.8`: cooperación condicional al puente personal, monitoreo y liderazgo. Refuta a Banfield con mecanismo.

**Y una con reserva:** `ref.B.03` (machismo no es rasgo) **pasa estructuralmente** —el modelo lo trata como *modificador*, no como universal— pero `§3.4` tiene una regla `[FUERTE]` cuyo driver nombrado es **machismo**, constructo `Media (b)`, **sin marca de procedencia**. Pasa la letra y falla el espíritu.

---

## 6 · Qué hacer

1. **Incorporar ADR-28.b**: `confianza_institucional` → vector. Cierra la FALLA 1. Ya está redactado; solo falta aprobarlo.
2. **Redactar ADR nuevo para la forma funcional de `familismo`.** No es recalibrar el 0.50: es que un coeficiente monotónico no puede representar un efecto curvilíneo. Requiere umbral o término cuadrático. **Fallo nuevo, sin ADR.**
3. **Dar dispersión a los perfiles.** Parámetros como distribuciones, no puntos. Cierra la FALLA 3 y es prerequisito de cualquier simulación con agentes.
4. **Decidir sobre las ocho sin objeto.** Dos rutas: ampliar el modelo (esfuerzo/horas, salud mental, colorismo, prestamista) o **retirarlas de la batería declarando el alcance**. Lo que no se vale es dejarlas contando como refutaciones activas cuando no pueden fallar.
5. **Corregir el tier de `§3.7`**: HIPÓTESIS → FUERTE, alineado con glosario, V2 y Hito 2.
6. **Reescribir las `falla_si` en dos niveles**: una condición verificable contra el **modelo** y otra contra el **simulador**. Hoy solo tienen la segunda, y por eso la batería llevaba meses sin poder correrse.
7. **Actualizar el meta del archivo**: dice `refutaciones_compiladas: 41`; las entradas tipadas suman **49** (28 A + 11 B + 10 C).

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** Nada aquí: la batería existe justamente para impedirlo, y las 27 que pasan lo hacen porque el modelo nombra el mecanismo estructural en el PORQUE de la regla.

**¿Qué sobregeneraliza desde clases medias urbanas?** La FALLA 3 lo agrava: perfiles sin dispersión convierten al clasemediero urbano formal —el perfil mejor evidenciado y fuente declarada del sesgo— en un punto en vez de una distribución. El sesgo del corpus queda **endurecido** por la forma del parámetro.

**¿Qué está sesgado por marcos externos?** La reserva de `ref.B.03`: machismo entra como driver de una regla `[FUERTE]` sin la marca **(b)** que el glosario sí le pone.

**¿Qué cambiaría con foco rural, indígena o popular?** `ref.B.04` (colorismo) y `ref.A.02` (esfuerzo) pesan mucho más ahí, y son dos de las ocho sin objeto. **El modelo no tiene parámetros para las dos refutaciones que más protegerían al México popular.** No es casualidad: es el sesgo de clase reproducido en la elección de variables.

**¿Qué parece defecto técnico y es otra cosa?** Que la batería llevara meses sin correrse **no fue negligencia**: sus `falla_si` están escritas contra un simulador que no existe. El instrumento se diseñó para un objetivo que aún no estaba construido, y eso lo volvió inútil mientras tanto. Es el mismo error de nivel de análisis que el Hito C encontró en las cláusulas falsables de los generadores — **segunda aparición del mismo defecto de método**.

**¿Dónde hay evidencia débil e intuición fuerte?** En clasificar como PASA varias de tipo C. Son guardarraíles de presentación y las juzgué contra `§5` del modelo y el glosario, no contra una salida real. Si el modelo se usa para generar texto, esas siete podrían fallar en el output sin fallar en el diseño.

**¿Qué conclusión sería peligrosa mal usada?** Que "27 de 30 pasan, el modelo está bien". Los tres fallos no son periféricos: uno afecta a un parámetro de los seis perfiles, otro a la forma funcional de un generador, y el tercero a que los agentes puedan diferir entre sí. Y **once refutaciones siguen sin poder correrse**, con el agravante de que son las paramétricas —las que vigilan que ningún número codifique el mito—. El marcador correcto es: **el corpus se defiende bien, el aparato de defensa está a medio construir.**
