# Verificación del Red Team contra el corpus real
### Qué aguantó y qué no, al contrastar cada ataque con el texto completo de los 25 reports

*25 de julio de 2026. Verificación hecha leyendo el texto real en `/mnt/project/`, no los extractos del glosario.*

---

## 0. El titular (honesto e incómodo para el red team)

**La mayoría de los ataques del red team NO sobreviven al contacto con los reports completos.** No porque el corpus sea perfecto, sino porque es **mucho más riguroso de lo que el glosario dejaba ver**: los reports tienen sistemas de tiers de evidencia (`[SÓLIDO]`/`[MEDIO]`), meta-auditorías y caveats explícitos que marcan **exactamente** las debilidades que el red team creyó "descubrir".

Esto vindica al pie de la letra la advertencia que el propio red team se puso en su §5: *"es posible que algún report ya contenga la defensa contra alguno de estos ataques; verificar contra los reports completos antes de re-tierar."* La verificación confirma que sí — y que **el eslabón débil no es el corpus: es el glosario** (mi propio `estado-proyecto`), que al comprimir los reports les arrancó los caveats y convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón.

Un red team que la verificación refuta es un **buen** resultado: significa que el corpus aguantó el golpe. Lo que no aguantó fue la capa de síntesis.

---

## 1. El patrón que explica casi todo

El mecanismo del error, en un ejemplo limpio (**simpatía**):

- **Lo que dice el report** (foundational, moral emotions): la simpatía se ancla parcialmente en Ramírez-Esparza —bilingües **mexicano-americanos**, que además puntúan *más bajo* en simpatía en autorreporte— y se marca como **`[MEDIO]`**, con la nota "muestras específicas, a menudo mexicano-americanos o estudiantes".
- **Lo que hizo el glosario**: la subió a **"Fuerte"** y borró la nota.
- **Lo que atacó el red team**: la sobre-confianza del glosario… atribuyéndosela al corpus.

La sobre-confianza existía. Pero vivía en la **capa de glosario**, no en los reports. El red team disparó a la capa equivocada. Esto se repite ataque tras ataque.

---

## 2. Ataque por ataque

### Ataques sistémicos (A1–A5)

| Ataque | Qué muestra el texto real | Veredicto |
|--------|---------------------------|-----------|
| **A1 · Problema mexicano-americano** ("el corpus cita estudios US-Latino como si fueran de México, sin marcarlo") | **Falso a nivel de reports.** Salud mental lo marca 3 veces y lo mete en su auditoría ("se señala explícitamente"); género etiqueta "Wheeler, N=227 parejas de origen mexicano" y añade "no es exclusivamente mexicano; la aculturación lo modifica"; moral emotions tiene un tier entero "muestras específicas —mexicano-americanos—" y dice "casi todo el andamiaje" está sesgado; foundational usa Ramírez-Esparza *con* el matiz bicultural | **REFUTADO** a nivel de corpus. Sobrevive solo para **comunicación** (ver §3) |
| **A2 · Importó Hofstede sin crítica** (IVR 97/UAI 82 como "motor") | **Mixto.** Consumidor sí ratea "Hofstede 97/82 = **Fuerte**" (sobre-calificado; "replicado" ≠ válido, no arregla la falacia ecológica de McSweeney). PERO triangula con experiencia vivida ("crisis económicas repetidas"), y **foundational ya hace mi crítica**: "Hofstede… datos de IBM de los años 60-70" | **SOSTIENE parcialmente** (solo en consumidor; el fenómeno está triangulado, no colapsa) |
| **A3 · El "88%" es artefacto** (y la baja confianza no es distintivamente mexicana) | **Refutado y superado.** El report ni usa 88% —reporta ~22% (WVS)—; lista *"'México es sociedad de baja confianza' como categoría fija"* entre los **mitos**; y ya dice *"'no confían por cultura'… oscurece las causas estructurales"* (Morris & Klesner: corrupción↔desconfianza). El report **ya hacía mi argumento** | **REFUTADO.** La confianza radial como concepto **sobrevive** |
| **A4 · Estructura-vs-cultura es infalsable** | **Parcial.** Foundational ancla la maniobra en investigación concreta (Ramondt & Ramírez: el fatalismo como "evaluación precisa" de oportunidades), no como aserción en blanco. Pero **no especifica qué evidencia la desconfirmaría** | **SOSTIENE parcialmente** (límite metodológico real, menos grave de lo planteado) |
| **A5 · Fuentes delgadas + sin autocrítica** | **Falso.** Foundational tiene "## 9. Meta-auditoría" con subsecciones sobre sesgos de marcos EE.UU./Europa y "lo que parece psicológico pero es adaptación racional"; autoridad tiene "Módulo de rigor extremo"; Cernas Ortiz (2018) flaggea las escalas gringas. La autocrítica es **extensa** | **REFUTADO** (la parte "sin datos primarios" sí es cierta, pero eso el corpus lo admite) |

### Afirmaciones (claims 1–8)

| Afirmación | Qué muestra el texto real | Veredicto |
|-----------|---------------------------|-----------|
| 1 · Confianza radial | El report separa confianza/desconfianza (Yáñez), atribuye a estructura, no exagera el número | **Concepto sobrevive**; el ataque a los números era al glosario |
| 2 · IVR 97/UAI 82 = motor | Ver A2: sobre-rateado como "Fuerte" pero triangulado | **Bajar a Media** (no colapsa) |
| 3 · Familismo = adaptación económica | Family lo trata con matiz (Ispa: enmeshment culturalmente variable); no es la aserción cruda que ataqué | **Debilitado**: el ataque de tautología aplica menos de lo pensado |
| 4 · Dignidad vs. face (contradicción) | **PARCHEADO.** Moral emotions lo resuelve: en Smith (2017) los mexicanos correlacionan dignidad y face **r=.96 positivo** (¡no se oponen!) y honor negativo. Arquitectura por segmentos: dignidad declarada + face conductual + culpa católica residual | **RESUELTO** por Ronda 2. Mi framing de "opuestos" era impreciso |
| 5 · Consumo compensatorio | Sigue siendo hipótesis en el report también | **Se mantiene como hipótesis** (aquí sí coincidimos) |
| 6 · Simpatía | Ver §1: `[MEDIO]` en el report, "Fuerte" en el glosario | **El report ya la tenía bien tierada** |
| 7 · Pigmentocracia >100% causal | Mérito la enmarca como "**predice** educación/ingreso" con ENADIS/MMSI/INEGI; autoridad dice "la clase modula más que la cultura" + Colmex 2018; foundational cita a Tenoch Huerta ("racismo y clasismo son lo mismo"). El ">100% causal puro" es **artefacto del glosario** | **Debilitado**: los reports ya reconocen el enredo con clase; no sobre-afirman causalidad pura |
| 8 · Machismo → depresión (HCHS/SOL) | Salud mental y género ya dicen "**muestras mexicano-americanas**" y dan evidencia-en-contra | **El report ya lo caveateaba** |

---

## 3. Lo que SÍ sobrevivió la verificación

El red team no queda en cero. Cuatro cosas aguantan — y son ahora la lista de pendientes reales:

1. **El report de comunicación (`arquitectura invisible`) es el eslabón débil genuino.** Es el que más carga estudios US-Latino (Ramírez-Esparza, Gabrielidis, Arciniega, Castillo, Wheeler, Escobar — todos) **y el único sin sección de meta-auditoría ni caveats de muestra**. Presenta la simpatía y los hallazgos de conflicto como mexicanos sin la nota que sí ponen salud mental, género y moral emotions. Aquí A1 y A5 **sostienen de lleno**. Además mete a México en "cultura de honor" (Cross/Uskul) — justo lo que moral emotions luego *refuta* (honor correlaciona negativo). Es el report que hay que corregir.
2. **Consumidor sobre-califica Hofstede como "Fuerte".** "Replicado" no arregla la falacia ecológica. Debe bajar a **Media** con la nota de McSweeney.
3. **A4 (infalsabilidad) es un límite real.** Ni el foundational especifica qué desconfirmaría una lectura estructural. No es fatal, pero es una disciplina que falta.
4. **El glosario (`estado-proyecto`) es el artefacto sobre-confiado de verdad.** No los reports. Es el que hay que rehacer.

---

## 4. Qué hacer (el reframe accionable)

El giro más importante: **no re-tieres los reports hacia abajo — ya están bien tierados por dentro.** El problema era la síntesis. Entonces:

1. **Regenera el glosario DESDE los tiers propios de los reports** (`[SÓLIDO]`/`[MEDIO]`), no desde memoria comprimida. Concretamente: simpatía → Media; machismo→malestar → Media (US-Latino); Hofstede → Media; confianza radial → concepto Fuerte / números Media. La mayoría de estos ya están así **en los reports**; solo hay que dejar de pisarlos al resumir.
2. **Arregla el report de comunicación:** añádele una meta-auditoría y marca sus constructos US-Latino, o intégralo con las notas que salud mental/género ya tienen.
3. **La contradicción dignidad-face ya está resuelta** (moral emotions, r=.96). Actualiza el glosario para reflejar la resolución en vez de listarla como problema abierto.
4. **Lo único que el corpus entero admite y no puede arreglar solo es la falta de datos primarios** — que es, otra vez, el argumento para la tarea B.

---

## 5. Meta: por qué esto es un buen resultado

Un red team existe para forzar exactamente esta verificación. La hizo, y reveló que:

- El corpus es **más confiable** de lo que parecía, no menos: aguantó un pase adversarial serio.
- El eslabón débil real —el glosario— quedó **identificado con precisión**, que es más útil que una sospecha difusa.
- La verificación se **auto-corrige**: varias heridas que el red team marcó ya estaban parcheadas (moral emotions) o caveateadas (salud mental, género) dentro del propio corpus.

Y hay una lección de método que trasciende este proyecto: **el glosario compró la sobre-confianza que el red team luego atacó**. Cuando comprimes 25 reports rigurosos en una tabla, lo primero que se pierde son los caveats — y sin ellos, un resumen fiel se vuelve una caricatura segura de sí misma. El integrador que sigue debe construirse leyendo los tiers de los reports, no re-resumiéndolos de memoria. Si no, reproducirá el mismo error a mayor escala.

---

### Nota de alcance
Verificación hecha por extracción dirigida (tiers de evidencia, secciones de auditoría, citas y cifras específicas) sobre el texto completo en `/mnt/project/`, no por lectura íntegra de los 25 reports. Los veredictos se apoyan en evidencia textual concreta (los `[SÓLIDO]`/`[MEDIO]`, el r=.96 de Smith, la línea de Hofstede-IBM en foundational, Cernas Ortiz sobre escalas gringas, ENADIS/MMSI en pigmentocracia). Si vas a rehacer el glosario en firme, el siguiente paso natural es leer completos los ~4 reports pivote (comunicación, consumidor, foundational, moral emotions) para redactar los tiers corregidos palabra por palabra.
