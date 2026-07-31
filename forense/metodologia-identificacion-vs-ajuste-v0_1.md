> **CLASE.** Propuesta sin sello. NO es canon. No rige hasta que exista ADR.
>
> **ORIGEN.** Conversación de chat, 31/jul/2026. El argumento es tipo (3).
>
> **QUÉ DE ESTO YA ES CANON.** Únicamente la clase `AJUSTADO` y sus cuatro
> rutas (`pseudo_panel` | `momentos` | `composicion` |
> `transversal_con_seleccion`), selladas por ADR-49 (D2) — ver
> `canon/gobernanza-v1_15.md` y `milpa/procedencia.yaml`. Todo lo demás en
> este documento —incluida la quinta ruta "panel intra-sujeto" del §4, la
> partición estado/ritmo/abierto del §3, la clase `AJUSTADO` como propuesta
> en sí (aquí solo se propone; el sello vino después y solo de las cuatro
> rutas de ajuste), y el orden "estados primero, ritmos al final" del §7—
> es razonamiento de esta conversación, no decisión de mesa.
>
> **CIFRAS SUPERADAS POR TRABAJO POSTERIOR — deriva, no copies de aquí.**
> - §3 (tabla) y §7.2: *"39 [probabilidades] de regla ... nadie lo ha
>   mirado"*. Superado: `forense/cobertura-motor.md` (31/jul/2026, ya en el
>   repo desde antes de esta sesión) examinó las 49 reglas del motor una
>   por una. El 39 sigue siendo correcto como conteo de VALORES en
>   `milpa/procedencia.yaml` (`medidos` + `derivados` +
>   `asignados_probabilidad`: 4 MEDIDO + 6 DERIVADO + 29 ASIGNADO = 39,
>   campo `estado:`), pero esos 39 valores caen sobre solo **15 de las 49**
>   reglas del motor — **34 reglas no tienen ningún valor**, ni MEDIDO ni
>   DERIVADO ni ASIGNADO. Vigente: `forense/cobertura-motor.md`,
>   `milpa/procedencia.yaml` (`estado:`).
> - §3: *"vector de seis"* de `confianza_institucional` y *"los 30 números
>   del vector de confianza"*. El tamaño del vector (6 componentes,
>   ADR-28.b) sigue vigente. "30" es el DELTA que
>   `milpa/procedencia.yaml` (`resumen.delta_v1_v2.confianza_institucional_vector`)
>   registra al pasar de escalar a vector, no el total de números del
>   vector: el vector completo son 6 componentes × 6 perfiles = **36**
>   números, todos `ASIGNADO` y marcados `SIN POBLAR` en el mismo
>   archivo — ninguno tiene valor por perfil hoy. Vigente:
>   `milpa/procedencia.yaml` (`resumen.desglose`, `resumen.delta_v1_v2`).
> - §3 y §7: *"instrumento verificado en disco"* para el vector de
>   confianza (ENCIG, ENCUCI, ENVIPE, ENIF). No verificable desde este
>   documento ni desde esta sesión: esa comprobación exige
>   `data/manifiesto.yaml`, fuera del perímetro de esta sesión (ADR-46).
>   Queda tal cual, sin contrastar aquí.
> - Lo demás verificado contra `forense/cobertura-motor.md`,
>   `corpus/indice.yaml`, `milpa/procedencia.yaml` y
>   `canon/gobernanza-v1_15.md` (ADR-49) se sostiene: 144 números totales,
>   90 `params_base` (= 15 × 6 perfiles), 15 coeficientes de generador —
>   todos `ASIGNADO` — y `unico_calibrable_hoy` retirado (ADR-49, D1).

---

# De identificación a ajuste — qué clase de problema es calibrar este modelo

**31/jul/2026 · propuesta metodológica, sin sellar. No es canon.**
Salió de la conversación entre el autor y la sesión de chat el 31/jul, después de que `CAL-ENOE` Fase A cerrara la última ruta de calibración causal declarada. Se escribe porque el razonamiento vale más que la conclusión, y en un traspaso operativo se pierde.

**Procedencia.** Lo derivado del repo va citado con archivo. Lo que es razonamiento de la conversación va marcado como tal. La partición estado/ritmo y el mapeo a los 144 se verificaron contra `modelo §1.1` y `milpa/procedencia.yaml` en el commit `ce0658c`; el resto es argumento, no hallazgo.

---

## 1 · El marco que se heredó

Durante toda la jornada el problema se planteó así: para calibrar `G3 → horizonte_temporal` hacen falta tres cosas a la vez —un desenlace que mida el constructo, un panel que siga al mismo sujeto cruzando formal↔informal, y suficientes transiciones para tener poder—. Ninguna fuente mexicana reúne más de dos. ENIF tiene desenlace sin panel. ENNViH tenía los tres y el tercero se midió y falló: 7 a 14 hogares informativos, las 60 estimaciones cruzando el nulo. ENOE tenía el panel y, según `CAL-ENOE` Fase A, no tiene el desenlace.

Conclusión aparente: no se puede.

**El autor cuestionó el marco, y tenía razón.** Los tres requisitos no son una ley estadística: son lo que exige **una** estrategia de identificación —estimar una elasticidad causal con variación intra-sujeto—. Es la garantía más fuerte que existe. No es la única forma de obtener un parámetro.

Y el marco venía de una frase escrita en `milpa/procedencia.yaml`, campo `unico_calibrable_hoy`, que declaraba a ENOE como *"la única elasticidad del modelo que México permite estimar con dato público"*. Esa frase se escribió antes de que existiera el catálogo de 119 fuentes. La sesión de chat la heredó tres veces y la presentó como el terreno.

Es el mismo modo de falla que la restricción de red del primer día y la de la SPA de INEGI: **una restricción supuesta se hereda igual que una cifra supuesta, y es peor, porque nadie la audita.** Una cifra parece una afirmación; una restricción parece el terreno. La regla v2.2 existe exactamente para esto y no se aplicó a una restricción metodológica porque nadie pensó que las restricciones metodológicas contaran.

Cuentan.

---

## 2 · El reencuadre: identificación no es ajuste

El modelo de decisión es un ABM. Sus parámetros **no necesitan ser elasticidades causales.** Necesitan ser valores que hagan que la población simulada reproduzca la conducta observada.

Eso es un problema de **ajuste**, no de **identificación**, y son cosas distintas:

- **Identificación** pregunta: *si esta persona cruzara de formal a informal, ¿cuánto cambiaría su horizonte?* Es una pregunta contrafactual sobre un individuo. Exige variación intra-sujeto.
- **Ajuste** pregunta: *¿qué valor de este parámetro hace que la población simulada tenga la distribución de horizontes que observamos?* Es una pregunta sobre agregados. No exige panel.

El corpus, los datos disponibles y el propio `procedencia.yaml` apuntan al segundo problema. El archivo lo admite explícitamente: *"los ABM asignan parámetros de forma rutinaria. El escándalo sería no poder distinguir cuál es cuál."*

Formulado por el autor, y es la formulación correcta: *el mexicano decide de una forma u otra, esa estructura existe y está presente, y alrededor de ella hay un conjunto de datos. Solo necesitamos encontrar la ecuación.*

---

## 3 · La partición que ya estaba en el archivo

`milpa/procedencia.yaml` contiene, sin desarrollarla, la distinción que resuelve casi todo:

> *"un coeficiente es una ELASTICIDAD, y el corpus es transversal — da estados, no ritmos."*

Los 144 números no son una bolsa homogénea. Son dos clases y media, y la partición **coincide exactamente con el desglose que el archivo ya declara**:

| Clase | Qué es | Cuántos | Qué exige |
|---|---|---|---|
| **Estado** | un nivel por segmento | 90 `params_base` | transversal con la segmentación correcta |
| **Ritmo** | una respuesta a un cambio | 15 coeficientes | identificación, o alguna de sus alternativas |
| **Abierto** | probabilidad de conducta dado contexto | 39 de regla | nadie lo ha mirado |

Y no es juicio. Es construcción, verificable en el árbol:

- Los **90 `params_base`** son 15 parámetros × 6 perfiles. `modelo §1.1` declara **nueve escalas escalares** —horizonte temporal, radio de confianza, aversión al riesgo, sensibilidad a estatus, deferencia, `familismo_apoyo`, `familismo_obligacion`, exposición a violencia, acceso digital— más `confianza_institucional` como **vector de seis** por ADR-28.b. Nueve más seis son quince. Son niveles por definición.
- Los **15 coeficientes** son elasticidades porque el archivo dice que un coeficiente *es* una elasticidad. Son ritmos por definición.
- Los **39 de probabilidad de regla** son el único conjunto genuinamente indeterminado. El cruce de Hito E los excluyó explícitamente por "unidad distinta" y nadie ha vuelto.

*(De paso, esto cierra el hallazgo abierto sobre "el 15º `params_base` sin identidad legible": no faltaba un nombre. Se buscaban quince escalares y hay nueve más un vector de seis.)*

**Consecuencia incómoda.** Si esto es correcto, el cuello de botella del programa nunca fue la falta de panel. Fue haber tratado 90 estados como si fueran 90 elasticidades. Los 30 números del vector de confianza llevan tres días con instrumento verificado en disco —ENCIG, ENCUCI, ENVIPE, ENIF con sus descriptores— sin que nadie los midiera, porque estaban clasificados mentalmente como parte del mismo problema irresoluble.

---

## 4 · Las cinco rutas

Ordenadas por fuerza de garantía. Solo la primera exige los tres requisitos.

**1 · Panel intra-sujeto.** Sigue a la misma persona a través del cambio. Identifica causalmente. Es la que México no permite hoy para este constructo — ENNViH lo permitía y no alcanzó el poder, ENOE tiene el panel y no el desenlace.

**2 · Pseudo-panel de cohortes.** La ruta más desaprovechada, y la que mejor le queda a este paisaje de datos. No puedes seguir a Juan entre 2018 y 2024, pero sí a *los hombres nacidos en 1985, con secundaria, del Bajío urbano*: ese grupo existe en las dos olas y sus miembros son intercambiables. La cohorte se vuelve la unidad de observación, y con suficientes olas hay efectos fijos de cohorte y variación temporal real. Se diseñó para exactamente este problema — muchas transversales repetidas, ningún panel. Y las olas existen: ENVIPE 8, ENIGH 6, ENOE 28 trimestres, ENIF 3. **Nadie ha construido ese panel de cohortes.**

**3 · Ajuste por momentos / inferencia indirecta.** En vez de estimar un coeficiente aislado, se elige el conjunto de parámetros que hace que la población simulada reproduzca momentos observados: tasas de ahorro por decil, penetración de crédito por formalidad, horizontes declarados por segmento. Todo eso está en fuentes que ya están en disco. Es como se calibran los ABM en la práctica.

**4 · Transversal con selección declarada.** Una sola ola. No separa causa de selección. Se usa cuando no hay más, se declara el límite, y se acota.

**5 · Composición.** Propuesta del autor, y abre una vía distinta a las otras cuatro. Un parámetro que no se puede estimar entero a veces **se descompone** en piezas, cada una medible en una fuente distinta, con la regla de composición declarada. No es promediar fuentes: es afirmar que el parámetro *es* el producto o la suma de partes, y medir cada parte donde se pueda.

> Condición innegociable: **la descomposición se declara antes de ver los datos.** Si se inventa después para que salga el número, es post-hoc y el Bloque C lo prohíbe explícitamente.

Y la observación del autor que ordena todo esto: **la estrategia se elige por parámetro, no por programa.** Uno puede ir por ajuste, otro por pseudo-panel, otro por composición. El paisaje de datos no elige una estrategia; cada número elige la suya.

---

## 5 · El costo, dicho sin suavizar

Lo que compra el panel intra-sujeto y no compran los otros cuatro es **separar la causa de la selección**.

Sin variación dentro del mismo sujeto no se distingue *"caer en informalidad acorta el horizonte"* de *"la gente de horizonte corto acaba en informalidad"*. Los datos se ven idénticos.

Y aquí eso no es un tecnicismo econométrico. Es el corazón de la tesis del corpus. Si se estima transversalmente y el coeficiente sale de la selección, se está codificando **una característica de las personas** como si fuera un efecto de la estructura. Es el esencialismo entrando por la puerta de atrás, con ropa de econometría — la misma falla que el Bloque A persigue en la cultura, cometida con un instrumento más respetable.

El pseudo-panel mitiga bastante —la composición de una cohorte es más estable que la de un individuo— pero no lo elimina. El ajuste por momentos lo esquiva sin resolverlo: reproduce el agregado sin afirmar el mecanismo.

**Ninguna de las cuatro alternativas compra lo que compra el panel.** Lo honesto no es fingir que sí, es etiquetar qué compró cada una.

---

## 6 · La clase que falta

`procedencia.yaml` tiene cuatro clases: `MEDIDO`, `DERIVADO`, `ORDINAL→CARDINAL`, `ASIGNADO`. Ninguna describe un parámetro obtenido por ajuste o por pseudo-panel.

**Propuesta, sin sellar:** una clase `AJUSTADO` — *reproduce los momentos observados; no está identificado causalmente*.

Es mejor que `ASIGNADO`, que es juicio informado. Y no finge ser `MEDIDO`, que es transcripción de un dato publicado.

Un coeficiente importado de otro país sería una **quinta** clase distinta, y el proyecto tiene un argumento fuerte en contra: si la conducta responde a la estructura y no a la cultura, una elasticidad estimada en otra estructura —otro seguro social, otra composición de informalidad, otro acceso a crédito— midió otra cosa. La estructura no es ruido alrededor del parámetro: **la estructura es el parámetro.** Importarlo sin el contexto asume precisamente lo que el corpus niega.

*(Matiz honesto en contra: las elasticidades viajan mejor que los niveles, y que el horizonte se acorte al caer en informalidad es plausiblemente universal en dirección. Pero la dirección de G3 ya está sostenida por el corpus. Lo que falta es la magnitud, y la magnitud es justo lo que no viaja.)*

---

## 7 · Qué cambia mañana

**La pregunta de Fase A deja de ser** *"¿tiene esta fuente el desenlace?"* — una compuerta que se cierra en seco — **y pasa a ser** *"¿qué estrategia de estimación soporta este paisaje de datos para este parámetro, y qué garantía compra?"*.

Y el orden se invierte respecto a como veníamos:

1. **Los 90 estados primero.** Son lo que este programa sí puede medir hoy, no exigen identificación, y 30 de ellos tienen instrumento verificado en disco. Ese es el contador que se puede mover esta semana.
2. **Los 39 abiertos después**, porque nadie los ha mirado y pueden ser estados disfrazados de ritmos. Si resultan genuinamente contestados, ahí gana su costo el método de tres brazos.
3. **Los 15 ritmos al final**, y por las rutas 2, 3 y 5 — no por la 1, que ya sabemos que no está disponible.

**Un cuidado con la formulación del autor.** *"Solo necesitamos encontrar la ecuación"* asume que hay una. Puede que el mismo driver tenga signo distinto por segmento, y entonces no es una ecuación sino una familia. Eso no cambia nada de lo anterior: solo significa que el ajuste se hace por perfil, que es como el modelo ya está construido.

---

## 8 · Lo que este documento no hace

No corrige `procedencia.yaml`. No sella la clase `AJUSTADO`. No reordena la cola de Hito E. No toca el modelo ni el pre-registro.

Todo eso es decisión de mesa, y conviene tomarla en un solo acto junto con la cascada de `unico_calibrable_hoy` que dejó abierta `CAL-ENOE` Fase A — porque son la misma decisión vista desde dos lados.
