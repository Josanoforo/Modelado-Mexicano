# Whitepaper · Simulador estructural de conducta para México
### `milpa-whitepaper` · **v0.1**

> | | |
> |---|---|
> | **ARCHIVO** | `milpa-whitepaper-v0.1.md` |
> | **REEMPLAZA A** | `01-whitepaper-simulador-mexico.md` — **borrar** |
> | **VERIFICAS ASÍ** | la cabecera dice `milpa-whitepaper` y trae la serie de lectura |
> | **NOMBRE ESTABLE** | **`milpa-whitepaper`** — cítalo así, **nunca por nombre de archivo** |

> **Serie MILPA — orden de lectura.** *(El `01/02/03` anterior codificaba el orden en el nombre y no la versión; ADR-36 lo invierte. El orden vive aquí, explícito.)*
>
> **1.** `milpa-whitepaper` — el **porqué** · **2.** `milpa-spec` — el **cómo** · **3.** `milpa-plan` — el **cuándo**

> **Modificado por ADR-57 (4/ago/2026):** las afirmaciones de intervención de §0 y la salvaguarda de §6.2 quedan bajo compuerta de identificación — ver gobernanza ADR-57. La versión no sube; excepción a ADR-36 declarada en el propio ADR.

### Codename **MILPA** — *Modelo de Interacción, Localidad, Población y Adaptación*

*Documento 1 de 3. Acompañan: (2) Especificación técnica del modelo, (3) Integración y plan de trabajo.*
*Versión 0.1 · Programa "Psicología del Mexicano Contemporáneo"*

---

## 0. Resumen ejecutivo

**Qué es.** Un simulador basado en agentes que instancia una **población sintética de México** sobre un **mapa de capas estructurales** (informalidad, violencia/impunidad, desigualdad, acceso financiero y digital, cobertura de salud, red de cuidados) y hace que cada agente decida usando el **modelo de decisión** ya construido por este programa: seis perfiles operativos, seis generadores estructurales y reglas SI-ENTONCES cuyo resultado depende del **contexto**, no del "carácter nacional".

**Para qué.** Para pasar de *explicar* conducta a *ensayar intervenciones*: qué le pasa a una población cuando formalizas empleo en una región, cuando digitalizas un trámite, cuando montas un sistema de cuidados, cuando llega una ola de violencia, cuando un producto financiero entra por el canal equivocado. El simulador convierte la tesis del corpus —**la conducta sigue al entorno**— en algo que se ve moverse en un mapa.

**Qué NO es.** No es un oráculo, no predice individuos, no colorea "el carácter" de las regiones, y no es un juguete de identidad nacional. Su valor está en la **capa epistémica**: cada regla lleva su nivel de evidencia, la incertidumbre se propaga, el mapa muestra dónde el modelo *no sabe*, y todo se somete a backtesting contra casos reales documentados.

**El riesgo central, dicho de una vez.** Un simulador así puede volverse *bellísimo, fluido y equivocado*: gráficas convincentes sobre supuestos frágiles. Este documento existe tanto para diseñar el sistema como para blindarlo contra su propio encanto.

---

## 1. El problema: tenemos el cerebro, falta el mundo

El programa ya produjo un **modelo de decisión validado**: dado un perfil, un dominio y un contexto, estima la conducta más probable con su driver y su nivel de evidencia. Eso es, en términos de simulación, **la función de decisión de un agente**.

Lo que no tenemos es todo lo demás que hace falta para que eso se vuelva un mundo:

| Pieza | Estado |
|---|---|
| Función de decisión (perfil × contexto → conducta) | ✅ Construida y parcialmente validada |
| Población sintética con proporciones reales | ❌ Falta |
| Mapa de capas estructurales por localidad | ❌ Falta |
| Red social por donde viaja confianza, información y cooperación | ❌ Falta |
| Bucle de retroalimentación (decisiones → entorno → decisiones) | ❌ Falta |
| Elasticidades/dinámica (a qué **ritmo** cambia la conducta al cambiar el entorno) | ⚠️ **El gran hueco** (ver §6.2) |
| Capa de honestidad epistémica | Parcial (los tiers existen; falta propagarlos) |

Un agente aislado no genera nada interesante. Lo interesante —y lo que justifica construir esto— es la **emergencia**: umbrales donde una colonia pasa de free-riding a organizarse, espirales de desconfianza que se retroalimentan, productos que se contagian por la red de confianza y no por publicidad, trampas de informalidad que se sostienen solas.

---

## 2. Tesis del simulador

El corpus sostiene que la conducta mexicana se explica sobre todo por **estructura + adaptación racional**, y muy poco por "cultura" entendida como carácter nacional. Esa tesis tiene una consecuencia técnica afortunada:

> **Si la conducta es función del entorno, entonces es simulable — porque el entorno es medible y modificable, mientras que el "carácter" no lo sería.**

Un modelo culturalista no se podría simular con honestidad (el "carácter" es una constante sin palanca, y una constante no genera dinámica). Un modelo estructural sí: las capas del mapa son variables con fuente estadística, y las intervenciones son operaciones sobre esas capas.

De ahí la regla de diseño más importante del sistema:

> **El mapa colorea ESTRUCTURA por defecto. La conducta se muestra siempre como una respuesta —un delta— y nunca como una propiedad intrínseca de una región.**

Cada visualización de conducta trae al lado su **mapa espejo**: la capa estructural que la causa. Si el usuario ve "aquí la gente no denuncia", ve inmediatamente al lado "aquí la impunidad es 94%". Esa es la diferencia entre un instrumento anti-esencialista y un mapa de estereotipos con estética de dashboard.

---

## 3. Arquitectura conceptual (siete capas)

```
┌──────────────────────────────────────────────────────────────┐
│  7 · CAPA EPISTÉMICA   tiers, incertidumbre, mapa de confianza│
├──────────────────────────────────────────────────────────────┤
│  6 · INTERVENCIONES    políticas, choques, productos          │
├──────────────────────────────────────────────────────────────┤
│  5 · RETROALIMENTACIÓN decisiones → indicadores → entorno     │
├──────────────────────────────────────────────────────────────┤
│  4 · MOTOR DE DECISIÓN reglas SI-ENTONCES + 7 disparadores    │
├──────────────────────────────────────────────────────────────┤
│  3 · RED SOCIAL        familia · puentes · lazos débiles      │
├──────────────────────────────────────────────────────────────┤
│  2 · POBLACIÓN         agentes sintéticos calibrados          │
├──────────────────────────────────────────────────────────────┤
│  1 · MUNDO             celdas con capas estructurales         │
└──────────────────────────────────────────────────────────────┘
```

**1 · Mundo.** México desagregado en celdas (municipio como unidad base; AGEB en zonas urbanas para el detalle). Cada celda carga las variables estructurales que **activan los seis generadores**: informalidad y cobertura IMSS (G3), homicidio/extorsión/impunidad (G4), Gini y movilidad (G2), confianza institucional y calidad de trámite (G1), estructura de hogar y remesas (G5), calidad de gobierno y tipo de empleador (G6), más la infraestructura de acceso (corresponsales bancarios, cajeros, conectividad, clínicas, escuelas).

**2 · Población.** Agentes sintéticos generados para que las **marginales de cada municipio calcen con el censo**: edad, sexo, escolaridad, ocupación, tamaño de hogar. A cada agente se le asigna un perfil (1–6) de forma probabilística dada su celda, más modificadores (género, generación, religiosidad por práctica, estatus migratorio). Sus parámetros de decisión —horizonte, radio de confianza, aversión al riesgo— **no son rasgos fijos: se derivan del perfil × la celda**. Esa es la implementación literal de la tesis.

**3 · Red social.** Un grafo con tres tipos de lazo: **familiares** (fuertes, alto peso, pueden ser transnacionales), **puentes** (compadrazgo, paisanaje, correligionarios — los que activan la confianza radial hacia fuera) y **débiles** (trabajo, vecindad). Por ahí viajan información y credibilidad, adopción de productos, tandas, cooperación, clientelismo y sanción social. Sin grafo no hay difusión, y sin difusión el simulador es sólo una calculadora repetida un millón de veces.

**4 · Motor de decisión.** El modelo ya construido, compilado a reglas ejecutables. Evalúa primero los **siete disparadores de contexto** (formal/informal · quién observa · sanción creíble · puente personal · urgencia/escasez · cobertura formal · segmento) y luego resuelve la regla del dominio. **La salida no es una conducta, es una distribución de probabilidad** — y el ancho de esa distribución lo fija el tier de la regla.

**5 · Retroalimentación.** Las decisiones individuales se agregan a indicadores de celda (mora, informalidad, confianza, participación, cobertura), y esos indicadores **actualizan las capas estructurales**, que a su vez modifican los parámetros. Aquí nacen los bucles: espiral de desconfianza, trampa de informalidad, trampa social de la mordida, bomba de crédito, nivelación.

**6 · Intervenciones.** La parte "WorldBox": políticas estructurales (formalización, digitalización de trámites, sistema de cuidados, cobertura de salud, conectividad, transferencias), choques (crisis cambiaria, ola de violencia, desabasto, choque migratorio), lanzamientos de producto (con su fricción y su canal) y campañas de comunicación. **Con una lección incorporada:** la intervención "campaña de concientización" produce un efecto casi nulo; la intervención "quitar la barrera" mueve el mapa. El usuario descubre por sí mismo que no se cambia conducta sermoneando.

**7 · Capa epistémica.** Ver §5. Es la capa que separa un instrumento de un juguete.

---

## 4. Qué genera valor (los casos de uso reales)

- **Política pública.** Ensayar el orden y la dosis de una intervención antes de gastarla: ¿formalizar empleo o ampliar transferencias? ¿digitalizar el trámite o subir la sanción al funcionario?
- **Diseño de producto y mercado.** Simular una entrada de producto con distintos canales (institucional frío vs. puente personal), fricciones y respaldos — el aprendizaje OXXO/CoDi convertido en simulador.
- **Análisis de riesgo.** Propagar el escenario del crédito fácil hacia adelante y ver dónde se concentra el estrés (el escaneo prospectivo de sobreendeudamiento, pero dinámico).
- **Pedagogía.** Es el mejor antídoto contra el esencialismo que existe: el usuario mueve una capa estructural y **ve** cambiar la conducta. Nada convence tanto como manipular el mecanismo con las manos.
- **Investigación.** Generar hipótesis falsables y priorizar dónde levantar datos primarios: el simulador expone, con brutalidad, dónde el modelo es ciego.

---

## 5. La capa epistémica (lo que lo hace serio)

Cuatro mecanismos, todos obligatorios:

**5.1 Tiers que se propagan como incertidumbre.** Cada regla lleva `FUERTE / MEDIA / HIPÓTESIS`. El tier no es una etiqueta decorativa: fija el **ancho de la distribución** de la que se muestrea la conducta y el **intervalo de confianza** de los coeficientes. Una regla HIPÓTESIS produce resultados con bandas anchas, no un número limpio.

**5.2 Modo "sin hipótesis".** Un interruptor global apaga todas las reglas de tier HIPÓTESIS. Si un resultado se sostiene con las hipótesis apagadas, es robusto; si se desmorona, el resultado dependía de nuestras intuiciones y hay que decirlo. **Ninguna conclusión debería publicarse sin correr este modo.**

**5.3 Mapa de confianza.** Junto a cada mapa de resultados va un mapa de *qué tan bien está evidenciado ese territorio*. Los municipios rurales, populares D/E e informales profundos salen **pálidos**, porque ahí el corpus admite vacío. Y los municipios con sistema de usos y costumbres salen **en gris de exclusión**, no en color tenue: no es que sepamos poco, es que **no aplica** (§7.2).

**5.4 Backtesting forense.** El simulador debe reproducir los casos ya documentados por la validación del programa. Si no los reproduce, hay un bug o una regla mala:
- **OXXO/Spin vs. CoDi** — el pago que integra el efectivo se adopta; el que asume sustitución, no.
- **Vacunación 2023–24** — la caída se explica por desabasto/logística, no por rechazo actitudinal.
- **Clientelismo** — la despensa no mueve el voto salvo cuando el agente *cree* que su voto puede ser observado.
- **Crédito popular** — el hogar informal paga; el colapso ocurre en el balance del prestamista (fondeo/gobierno), no en el impago.
- **Progresa** — al estabilizar el ingreso, se alarga el horizonte y cambia la inversión en capital humano.

---

## 6. Los dos huecos que hay que declarar antes de empezar

### 6.1 Granularidad: casi ninguna encuesta es municipal

ENCIG y ENCUCI cubren localidades de 100 mil habitantes o más; ENSU es urbana; ENVIPE y ENIF son representativas a nivel estatal. **Bajar a municipio exige estimación en áreas pequeñas (SAE)**, que es legítima pero **inyecta incertidumbre que el mapa hará invisible si no se muestra a propósito**. Este es el riesgo #1 del proyecto: producir un mapa que se ve mucho más preciso de lo que es. Mitigación: el mapa de confianza (§5.3) es obligatorio y no se puede ocultar en la interfaz.

### 6.2 Dinámica: el corpus es transversal, la simulación necesita elasticidades

Este es el hueco intelectualmente más serio y conviene decirlo sin rodeos.

El corpus establece **estados**: informalidad → horizonte corto; impunidad → no-denuncia; puente personal → adopción. Lo que casi nunca establece son **ritmos y elasticidades**: si formalizo el empleo de un municipio, ¿en cuántos trimestres se alarga el horizonte de planeación, y cuánto? ¿La confianza institucional se recupera al mismo ritmo al que se destruyó? (Casi seguro **no**: la evidencia sugiere que se pierde rápido y se reconstruye lento — pero eso es una hipótesis, no un parámetro medido.)

Consecuencia práctica: **muchos coeficientes del bucle de retroalimentación entrarán como tier HIPÓTESIS**, y el simulador será mucho más confiable en **dirección y orden de magnitud** que en **magnitud y tiempo**. Debe presentarse así:

> El simulador responde bien a *"¿en qué dirección mueve esto, y qué es más potente que qué?"*, y mal a *"¿cuántos puntos porcentuales en 18 meses?"*.

Fuentes que sí aportan dinámica y hay que exprimir: evaluaciones aleatorizadas (Progresa/Oportunidades), series de panel (ENOE es rotativa), evaluaciones de impuestos y etiquetado, series municipales de violencia, y la literatura de choques (crisis 1994, pandemia).

---

## 7. Fronteras duras (no negociables)

**7.1 Firewall genético.** Ninguna variable de ascendencia entra al cerebro del agente. Prohibida la inferencia ascendencia → conducta de grupo. El único canal genético admitido por la evidencia (metabolismo de alcohol/nicotina) es **individual, pequeño frente a la estructura y modifica una consecuencia, no una decisión**: si algún día se modela, va como modificador de desenlace de salud, jamás como segmentador de población. *(La distribución de tono de piel sí puede aparecer, pero como* **capa de discriminación estructural** *—predice movilidad, y eso es un hecho sobre el trato que recibe la gente, no sobre su biología—, y sólo con etiqueta explícita.)*

**7.2 Frontera de alcance: el sistema indígena-comunal.** Las comunidades que operan bajo usos y costumbres (asamblea como autoridad, cargos rotativos, tierra comunal, tequio obligado) **no se simulan con este cerebro**: es otro orden institucional, no un México sub-medido. En el mapa aparecen **enmascaradas y en gris**, con la leyenda explícita "fuera de alcance — otro modelo". Simularlas con reglas de mercado sería el error categorial más grave que este sistema puede cometer. *(La huella indígena difusa —sincretismo, folk-psicología, compadrazgo— sí vive dentro de los perfiles modernos y ya está incorporada.)*

**7.3 Prohibición de salida a nivel individuo real.** El sistema produce distribuciones sobre agentes sintéticos. No acepta como entrada, ni emite como salida, juicios sobre personas identificables. Ninguna versión del sistema debe poder usarse para scoring de individuos en crédito, contratación o seguros.

**7.4 Anti-esencialismo cartográfico.** Ya enunciado en §2 y llevado a la interfaz: conducta siempre con su mapa espejo estructural.

---

## 8. Riesgos y mitigaciones

| Riesgo | Por qué es grave | Mitigación |
|---|---|---|
| **Falsa precisión** (SAE + elasticidades inventadas) | Convierte incertidumbre en números convincentes | Mapa de confianza obligatorio; bandas por tier; modo sin-hipótesis; nunca reportar decimales que el dato no sostiene |
| **Esencialismo cartográfico** | Un mapa de "conducta por región" es un mapa de estereotipos con estética de datos | Mapa espejo estructural; colorear estructura por defecto |
| **GIGO estético** | Un front-end bonito compra credibilidad que el modelo no ganó | La suite de backtests es requisito de release, no de "fase 2" |
| **Captura política** | Usar el sim para justificar una política ya decidida | Reglas versionadas y auditables en repo; log de escenarios inmutable; publicar el diff cuando se cambia una regla |
| **Uso discriminatorio** | Targeting de segmentos vulnerables | §7.3 + licencia de uso restringida + sin salida individual |
| **Invisibilizar el vacío** | Pintar igual lo bien medido y lo no medido | Palidez proporcional a la confianza; el vacío es visible, no interpolado |
| **Deriva del modelo** | El sim evoluciona y deja de reflejar el corpus | La ficha canónica es la fuente de verdad; cualquier regla nueva requiere tier y fuente |

---

## 9. Qué promete y qué no

**Promete:** dirección del efecto, jerarquía entre palancas, umbrales cualitativos, mapas de dónde una intervención rinde más, emergencia de bucles conocidos, y una herramienta pedagógica excepcional contra el esencialismo.

**No promete:** magnitudes precisas, calendarios, predicción de eventos, ni cobertura del México rural profundo, popular D/E o comunal-indígena. En esos territorios el sistema debe **decir que no sabe**, que es exactamente lo que el corpus hace hoy.

---

## 10. § Duelo — formulación sellada (31/ago/2026, `ADR-237`)

*(Sección nueva, fechada — `ACTO MAESTRA32-E19 · SELLA-CAMINO-1`, firma de
mesa `F-DUELO`, 31/ago/2026. Este whitepaper es v0.1, previo a todo el
ciclo de medición que arrancó el 4/ago/2026: no traía, hasta hoy, ninguna
formulación del duelo. El texto de abajo es esa formulación, verbatim tal
como mesa la selló al confirmar el entendimiento — "el duelo real … es:
¿el LLM supera al motor = LLM + data real?" — y entra sin tocar el resto
del documento.)*

El duelo no compara "IA contra datos". Compara dos formas de usar el mismo
conocimiento: L es el LLM elicitado en directo — implícito, ciego, en
sesiones limpias fuera del proyecto; M es ese mismo conocimiento hecho
estructura explícita y auditable (reglas, generadores, parámetros con
procedencia declarada), con sus priors de juicio (`ASIGNADO`) sustituidos
pieza a pieza por mediciones en microdato mexicano; R es la realidad,
calculada por un árbitro desde microdato no publicado — la "prueba del
bibliotecario", 56 de 60 celdas del marco original — precisamente para que
L no pueda haberla memorizado. La pregunta del programa es doble: ¿explicitar
y calibrar añade valor predictivo sobre preguntar directo?, y ¿cuánto del
conocimiento implícito del LLM sobrevive al pasar por esa disciplina?
Asimetría declarada, no escondida: L y M comparten la familia de LLM de
origen; eso mantiene el LLM constante y aísla el valor marginal de
estructura + datos. Descomposición prevista y no activada: el corredor E
("combinación": LLM con datos, sin estructura) existe como ranura en la
configuración sellada del scoring y separaría, el día que mesa lo active,
cuánto aporta el dato y cuánto la estructura.

---

*Este whitepaper hereda las reglas del programa (Bloque A/B/C, v2): anti-esencialismo, distinción estructura/cultura/adaptación racional, evidencia tierizada, marcado de procedencia, firewall genético, y el módulo de auditoría como requisito de cierre en cada artefacto. El simulador no es una excepción a esas reglas: es su implementación ejecutable.*
