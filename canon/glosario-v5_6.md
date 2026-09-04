# Glosario del corpus
### `glosario` · **v5.6** · CANÓNICO · autocontenido

> | | |
> |---|---|
> | **ARCHIVO** | `glosario-v5.6.md` |
> | **REEMPLAZA A** | `glosario` — **borrar** |
> | **VERIFICAS ASÍ** | §15 marca la deuda de **ENA 2017 + AMUCSS 2014 como CERRADA** |
> | **NOMBRE ESTABLE** | **`glosario`** — cítalo así, **nunca por nombre de archivo** |



> 🔖 **SELLO DE VERSIÓN — v5.2 · 28/jul/2026.** *Para verificar de un vistazo qué versión tienes en el proyecto:* **debe existir un `§16 · Constructos que el motor usa sin tier leído`.** Si tu copia va de `§15 · Deudas vivas` directo a `Provenance`, es la v5.1 y le faltan las correcciones de la validación.
### Documento autocontenido · supersede y **reemplaza** a `glosario-corregido-v2`, `glosario-v3` y `glosario-v4`

> **v5.1 — 28 de julio de 2026.** La v5 se consolidó **antes** de ADR-30 y quedó una versión por detrás del modelo v2, invirtiendo la cadena de dependencia (el glosario debe ir *delante* del modelo, no detrás). Seis cambios:
>
> | # | Cambio | Origen |
> |---|---|---|
> | 1 | `familismo` se desdobla en **`familismo_apoyo`** y **`familismo_obligacion`** (§4) | ADR-30 |
> | 2 | Coeficientes de generador: **14 → 15**; G1 se desdobla en **G1a/G1b** (§13) | ADR-30 + cambio 7 del modelo v2 |
> | 3 | Conteo de números: **107 → 144**, recomputado y desglosado (§13) | ADR-28.a/b/d |
> | 4 | Entra **`transferencia directa universal`** como constructo con tier propio, y se abre **conf.07** por el empaquetado de la regla §3.7 (§8, §11) | Hito 2 + V2 forense |
> | 5 | §14 fugas 1 y 2: **actualizadas** — la marca (b) ya llega a la ficha; ADR-29 está aprobado; los parches a la fuente se aplicaron el **28/jul**, no el 27 | verificación 28/jul |
> | 6 | Entra **ADR-31** (se retira el "híbrido" de honor en foundational) | ADR-31 |
>
> **v5.2 — misma fecha, salida de la primera corrida del check de ADR-32.c.** Tres cambios más:
>
> | # | Cambio | Origen |
> |---|---|---|
> | 7 | Entra **§16 · constructos que el motor usa sin tier leído**: `trampa social` y `bandwidth tax`. Registrados, **NO tierizados** | ADR-32.c, 1.ª corrida |
> | 8 | **Fila de Marianismo: se corrige una afirmación falsa.** Decía *"marca añadida a la fuente el 27/jul"*. Verificado por `grep`: **no se había añadido**. Es el **tercer** caso del mismo patrón, tras Hofstede y honor | ADR-32.a |
> | 9 | §14: se registra el tercer falso positivo de retropropagación y se refuerza el requisito | ADR-32.a |
>
> **v5.3 — misma fecha, preparación del Hito D.** Dos cambios más:
>
> | # | Cambio | Origen |
> |---|---|---|
> | 10 | El constructo de transferencia directa **se desdobla**: la mitad de *atribución/aprobación* recibe su tier propio, **leído del forense V2: `Media`, correlacional, CONFUNDIDO**. El motor la traía dentro de un `[FUERTE]` | ADR-33 |
> | 11 | Entra **`conf.08`**: el `PORQUE` de la regla de autonomía decía *"no hay monitoreo ni broker"* y el forense V2 lo declaró **ROTO PARCIALMENTE** desde la Ronda 4. **Séptimo caso de propagación fallida** | ADR-29.a |

*27 de julio de 2026. Nada aquí está por referencia a una versión anterior: las tres quedan borrables. Construido leyendo los mapas de evidencia de los reports, las cuatro verticales, el registro de apuestas, la prueba de falsación, el Hito 2 y la lectura completa de los cuatro pivotes. Ningún tier reconstruido de memoria.*

**Corpus a la vista:** 60 archivos — 30 reports temáticos, 1 prueba del canal genético, 4 verticales forenses, 1 registro de apuestas, 24 de gobierno y método. ⚠️ **Nota fechada 29/jul/2026:** este párrafo es del corte del 27/jul (ver encabezado de la sección) y nunca se marcó como superado, a diferencia del resto de este glosario. Hoy son **31** reports temáticos (`ls corpus/reports/*.md`, verificado 28/jul en `estado §1`); el resto de la cuenta ("60 archivos") no se re-verifica aquí. *(`censo-integridad-v1_0.md` C1-09.)*

---

## 0 · Por qué existe esta consolidación

Los cuatro glosarios eran **deltas encadenados**: v4 remitía a v3, v5 remitía a ambos. Ninguno se podía borrar sin romper el vigente, y los cuatro seguían siendo recuperables por búsqueda semántica con tiers que se contradicen entre versiones — que es exactamente el defecto de `estado-proyecto`, multiplicado por cuatro.

La proliferación no fue descuido: **cada versión se escribió con un corpus distinto a la vista** — v3 con 34 archivos, v4 con 43 durante la pérdida, v5 con 60. Al estabilizarse el archivo, deja de pasar.

**Corrección de premisas heredada del v4.** El v4 declaró siete pérdidas; **seis se recuperaron** (integrador, modelo, ficha, las cuatro verticales, registro de apuestas, gobernanza, docs del simulador). La única real es **PD-01: 14 de 15 casos descartados del registro de apuestas, irrecuperables porque nunca se escribieron.** Todo cambio de tier que el v4 hizo a ciegas está reverificado aquí por lectura directa.

---

## 1 · Leyenda

**Tier de evidencia:** `Fuerte` · `Media` · `Hipótesis razonable` · `Narrativa popular`

**Procedencia de la evidencia:**
- **(a)** dato primario sobre población **EN México**
- **(b)** muestra **mexicano-americana / de diáspora** en EE.UU. — sujeta a aculturación y selección migratoria; **no es evidencia directa sobre México**
- **(c)** marco teórico importado

**Origen del tier** — quién lo decidió:
- **`LEÍDO`** — el report tiene mapa de evidencia y el tier se copió de ahí
- **`DERIVADO`** — el report **no tiene sistema de tiers**; se infiere de su aparato interno (n, diseño, caveats). Juicio del glosario, no del report
- **`FORENSE`** — proviene de una validación forense, no de un report

**Reports sin mapa de evidencia** (todo constructo suyo es `DERIVADO`): `Mérito`, `Psicología_del_Trabajo`, `La_arquitectura_invisible`, `Humor`, `Mexican_Population_Genomics`. Usan formato de actualización o mapa temático. Tienen caveats excelentes —sirven para derivar— pero no tiers. **La marca dice quién decidió, no si el tier es bueno.**

---

## 2 · Constructos maestros

| Constructo | Tier | Proc. | Origen | Base y reservas |
|---|---|---|---|---|
| **Estructura vs. cultura vs. adaptación racional** | **Media** como principio operativo | (a)+(c) | `DERIVADO` | Sigue siendo el eje correcto, pero la convergencia está **sobre-declarada**. Tres razones, en orden de fuerza: **(1) contraevidencia empírica interna** — Argentina comparte herencia católica y desigualdad con normas comunicativas *"dramáticamente diferentes"*, e Israel tiene UAI casi idéntica y es la cultura más directa del mundo (ambas en `arquitectura invisible`); **(2)** el Hito 2 muestra que de 13 reglas que las verticales dijeron estresar, **6 no existían en el motor**; **(3)** el marco premia el resultado y los cuatro autores confiesan el mismo sesgo direccional — cuatro confesiones no son cuatro confirmaciones. Válida dentro de dominios **material-económicos**; no generalizable a identidad, religión, familia, género. ⚠️ *El foundational no especifica qué la desconfirmaría — límite metodológico reconocido* |
| **Los tres sustitutos del enforcement** | **Fuerte** | (a) | `LEÍDO` | Se coopera fuera del parentesco cuando hay **(1) vínculo personal**, **(2) monitoreo y sanción social horizontal**, **(3) liderazgo confiable**. Sin ninguno, la cooperación colapsa —no por falta de valores, sino porque contribuir sin garantías es irracional. El mecanismo más limpio del corpus |
| **Adopción por canal de confianza personal** | **Fuerte** | (a) | `LEÍDO` | Adopción **individual**: producto que llega por canal de confianza personal → sube adopción; sin puente, desconfía |
| **Confianza radial como canal de difusión** | **Hipótesis** | (a) | `LEÍDO` | ⚠️ **Corrección de atribución:** ADR-20 no descubrió esto. El report de tecnología **ya lo tenía tierado como hipótesis razonable**, textual: *"mecanismo de difusión vía recomendación interpersonal — sin evidencia conductual directa mexicana"*. El defecto fue que el modelo no lo leyó |
| **Confianza radial — magnitud** | ⚠️ **NO ESTABLECIDA** | (a) | `LEÍDO` | `conf.06` **cerrado por ADR-64** (5/ago/2026): las tres cifras de ENCUCI 2020 no competían por el mismo reactivo — son **tres reactivos distintos** de la pregunta 5.1 (`AP5_1_1/2/3`), todos a corte **≥8/10**: **21.8%** = "la mayoría" · **32.1%** = vecinos · **62.1%** = conocidos (§11). **El residual ya no está "sin reconciliar": está adjudicado, y no converge en una cifra sustituta.** `ADR-111`/`FP-29` (18/ago/2026) prueba cada atribución del 22% contra microdato: WVS 2018 (`Q57`) **REFUTADA** — 10.51% `IC95%[8.86, 12.15]`; Latinobarómetro 2024 (`P10STGBS`) **NO SOSTENIDA** en su única ola — 26.06% `IC95%[22.45, 29.67]`; LAPOP **REFUTADA POR ERROR DE CATEGORÍA** — no fielda el reactivo, su ítem `it1` ("la gente de su comunidad") da 54.0/53.6/55.4% en 2019/2021/2023; ENAFI **INDECIDIBLE** — cero entradas en el manifiesto. **El 22% queda sin procedencia sostenible** (`ADR-111(b)`, `gobernanza-v1_15.md:2097`). El 18% de Pew **REPRODUCE EXACTO** contra fuente primaria (`Q104`, Spring 2025 GAS: 18% México, sin IC — el topline no publica `n` por país). El 12% (WVS 2012/Wave 6) queda **INDECIDIBLE** — la ola no está en el manifiesto; solo Wave 7 (2018), que mide 10.51%. **Rango medible hoy, por escala, nunca promediado:** binarios 10.5%–26.1% (2018–2025) · ENCUCI 21.9% a ≥8/10 (2020). Qué hace el canon con el 22% sin procedencia — retirarlo, sustituirlo por el rango, o esperar la prueba de procedencia documental — quedó decidido en `FP-58`: se sustituye por lo medido, reportado por escala. Detalle comando por comando: `forense/notas/2026-08-18-fp29-adjudicacion.md` |
| **Confianza institucional como vector, no escalar** | **Fuerte** | (a) | `LEÍDO` | **No es baja en bloque.** Marina 89%, familia 87%, escuelas públicas 77%, universidades 76% vs. partidos 23.9%, judicial, policía, legisladores. Un escalar predice que quien desconfía de la policía desconfía de la Marina: falso y medido (ADR-28.b) |
| **Sanción social horizontal** (chisme, envidia, nivelación) | **Fuerte** como mecanismo | (a) | `LEÍDO` | Sustituto #2 del enforcement. Con el correctivo de Cancian: el sistema de cargos **no nivela la riqueza — la legitima y estratifica** |
| **Pigmentocracia / colorismo** | **Fuerte** (correlación) | (a) | `DERIVADO` | ENADIS y MMSI-INEGI: el color de piel **predice** educación, ingreso y movilidad. Aparece en seis reports; su fuente principal (`Mérito`) no tiene mapa de evidencia. Entrelazado con clase —los reports lo reconocen—; la causalidad aislada no está demostrada. **Deuda: falta el control por origen social y red** |
| **Violencia como destructor selectivo** | **Fuerte** | (a) | `LEÍDO` | Colapsa la confianza **institucional**, no la personal. *"Violencia estructural, no cultural"* = Fuerte; *"cultura de la violencia mexicana"* = narrativa popular a refutar. Desaparecidos: **135,445** (CIDH, 30/06/2026) |

---

## 3 · Interacción, emoción moral y comunicación

| Constructo | Tier | Proc. | Origen | Base y reservas |
|---|---|---|---|---|
| **Indirección en el rechazo** | **Fuerte** | (a) | `DERIVADO` | **64% de estrategias indirectas** (Félix-Brasdefer, universitarios de Tlaxcala): respuestas indefinidas, explicaciones como acto principal, aceptación condicional. En negocios, un "sí" frecuentemente significa "probablemente" |
| **Evitación con superiores** | **Fuerte** | (a) | `DERIVADO` | Madlock, **N=168 trabajadores mexicanos**. Paradoja: la comunicación descendente **cumple la expectativa cultural**, así que produce alta satisfacción laboral. La evitación no equivale a infelicidad cuando es congruente con la norma |
| **Correctivo GLOBE** (asertividad hacia abajo / indirección hacia arriba) | **Fuerte** | (a)+(c) | `DERIVADO` | Se **desea** menos distancia de poder de la que se practica. La asertividad fluye hacia abajo (los jefes dirigen), la indirección hacia arriba |
| **PDI como correlato de la indirección** | **Media — correlato** | (c) | `DERIVADO` | Es lo que discrimina en el par México/Israel (81 vs. 13, la mayor brecha del corpus). **Correlato descriptivo, no causa** (ADR-06) |
| **UAI como driver de la indirección** | ⚠️ **RETIRADO** | (c) | `DERIVADO` | **Falsado internamente.** `arquitectura invisible` afirma que la UAI de 82 *"genera"* incomodidad con el conflicto, y cien líneas después documenta que **Israel tiene UAI 81 y es la cultura más directa del mundo**. Presentaba el mecanismo y su contraejemplo sin advertirlo |
| **Simpatía** | **Media** | **(b)** | `LEÍDO` | Script cultural, no rasgo: facilitar relaciones positivas, minimizar lo negativo en conflicto. Triandis 1984 + escala de Acevedo 2020, **US-Latina**. ⚠️ Ramírez-Esparza: los bilingües mexicano-americanos puntúan **más bajo** en autorreporte |
| **"Quedar bien" / facework** | **Media**; versión organizacional **Hipótesis** | (c)+(a) | `DERIVADO` | Goffman/Ting-Toomey (marco importado, apoyo mexicano indirecto) |
| **Sensibilidad reputacional** ⭐ | **Media** | (a) | `DERIVADO` | Menor disposición a perdonar ofensas que amenazan la reputación (Castillo 2019). Real y medible. Se explica como **face bajo dignidad**, no como honor |
| **Cultura de dignidad** | **Fuerte** (autopercepción) | (a) | `LEÍDO` | Smith 2017: México **2º en dignidad, 5º en honor, 8º en face** de nueve muestras. **Dignidad y face correlacionan r=+.96** —no se oponen—; ambas negativas con honor |
| **"México cultura de honor"** | **NARRATIVA POPULAR — retirada** ✅ | (c) | `LEÍDO` | Etiqueta importada (Leung-Cohen, Cross/Uskul) cuyos ejemplares se estipulan *a priori* y rara vez se validan con medida directa. Retirada por la meta-auditoría y **parchada en la fuente el 27/jul/2026**. ⚠️ *Pendiente:* `foundational` aún sostiene un "híbrido" (honor rural/tradicional + dignidad urbana/educada) — posición matizada, no error; requiere decisión |
| **Machismo vs. caballerismo** | **Media** | **(b)** | `LEÍDO` | Arciniega 2008, **muestra mexicano-americana**. Machismo tradicional → mayor depresión, ansiedad, ira (HCHS/SOL, N=4,426). Género aporta evidencia-en-contra: *"no es exclusivamente mexicano; la aculturación lo modifica"* |
| **Marianismo / autosilenciamiento** | **Media** | **(b)** | `LEÍDO` | Cinco pilares (Castillo 2010). Nuñez 2016, N=4,426 = **cohorte HCHS/SOL, hispana en EE.UU.** ⚠️ *Corregido en v5.2: la v5.1 decía "marca añadida a la fuente el 27/jul" y **era falso** — verificado por `grep`, la oración que cita a Nuñez en `La_arquitectura_invisible` seguía sin marca. **Añadida en la fuente, inline, el 28/jul/2026.** Tercer caso del patrón Hofstede/honor. Nota justa al corpus: `Salud_Mental` y `Reconfiguración_de_Género` **sí** traen la marca de origen y bien puesta; la fuga era del report de comunicación.* ⚠️ Wheeler 2010 (N=227 parejas mexicoamericanas) **invierte el estereotipo**: las esposas usan más control, los esposos más no-confrontación |
| **Abnegación / PHSC de Díaz-Guerrero** | **Media**, con caveat de vigencia | (a) | `LEÍDO` | Base empírica **1950-1990; requiere actualización**. El >80% original es de hace 60-70 años. Díaz-Loving 2011-17 halla el patrón **concentrado en menor educación y rural** — segmentado, no general |
| **Vergüenza / culpa** | **Fuerte** (mecanismo) | (a)+(c) | `LEÍDO` | Vergüenza-proneidad ligada a malestar; culpa reparadora (literatura TOSCA/GASP). *"La culpa católica lo explica todo"* = **narrativa popular** |
| **Somatización** | Patrón **Fuerte**; mecanismo causal **Hipótesis** | (a)+(b) | `LEÍDO` | Brambila-Tapia 2023, **N=1,008 adultos mexicanos** (dato (a)) + Escobar/immigrant paradox (b). *"Supresión→somatización"* sigue en hipótesis. ⚠️ Matiz: entre adolescentes mexicoamericanos la supresión de emociones **negativas** se asoció con **menor** anhedonia — la supresión culturalmente normativa puede ser adaptativa dentro de su marco |
| **Controlarse / aguantarse / sobreponerse** | **Media** | (a)+(c) | `DERIVADO` | Recursos culturales de afrontamiento; desadaptativos solo cuando producen supresión crónica |

---

## 4 · Familia, jerarquía y trabajo

| Constructo | Tier | Proc. | Origen | Base y reservas |
|---|---|---|---|---|
| **`familismo_apoyo`** — red disponible, corresidencia, pooling de ingreso y cuidado | **Fuerte** | (a)+**(b)** | `LEÍDO` | Valdivieso-Mora 2016 (39 estudios); meta-análisis Cahill 2021 (*Psychological Bulletin*): menos síntomas internalizantes y externalizantes, menos conflicto familiar, mejores resultados educativos. **Signo positivo** sobre bienestar y sobre capacidad de absorber choques. Escalas de Sabogal/Lugo Steidel/Knight **validadas en contextos migratorios** → la marca **(b)** viaja. Opera en **G3** (pooling ante volatilidad: la tanda, el préstamo del primo) y en **G5** (seguro ante Estado ausente) sin doble conteo: son mecanismos distintos |
| **`familismo_obligacion`** — creencia internalizada de que uno **debe** sacrificarse por la familia | **Media** | **(b)** | `LEÍDO` | *Nuevo en v5.1 (ADR-30).* Zeiders 2013: el familismo **obligatorio** no es protector y **puede ser factor de riesgo**. Fuligni 1999: relación **curvilínea** con logro académico — las obligaciones más altas producen calificaciones tan bajas como las más débiles. Puede empujar al abandono universitario. Calzada 2012 identifica empíricamente tres dimensiones (apoyo · obligaciones · familia como referente) y **los efectos adversos se concentran en la segunda**. **Signo negativo o no monotónico.** ⚠️ Toda la base es **(b)**: nadie ha medido este parámetro en población residente en México |
| ⚠️ **Por qué son dos y no uno curvado** | — | — | — | Apoyo y obligación son **constructos distintos**, no extremos de una escala. Un parámetro curvado no puede estar en dos puntos de la curva a la vez — y ésa es la situación modal de la cuidadora mexicana (39.7 h/sem no remuneradas): **apoyo alto y obligación alta simultáneos**. Curvar codificaría *"mucha familia daña"*, afirmación distinta y peor fundada que la que el corpus sostiene (*"la obligación daña, el apoyo protege"*) |
| **Distancia de poder / autócrata benevolente** | **Fuerte** (convergente) | (a)+(c) | `DERIVADO` | Hofstede PDI 81 + GLOBE + WVS 57% + ENCUCI 77.5%. Solo el paternalismo **benévolo** legitima; el autoritario no-benévolo empeora el desempeño. *"El PDI explica todo"* = mito en el propio report |
| **Hofstede: Indulgencia 97 / UAI 82** | **Media — correlato, no motor** | **(c)** | `DERIVADO` | ⚠️ **Corregido en la fuente el 28/jul/2026** (antes `Fuerte` en el report de consumidor). *La v5 daba esta corrección por aplicada el 27/jul; la verificación del 28/jul encontró que la decisión existía (ADR-06) pero **la nota nunca bajó al report**. Aplicada y verificada en la fuente el 28/jul.* "Replicado" no resuelve la falacia ecológica de McSweeney: la crítica es de **validez de constructo, no de existencia**. La dimensión no colapsa y está triangulada con experiencia vivida (crisis económicas repetidas), pero **no produce conducta individual** |
| **Burnout normalizado / improvisación forzada** | **Media** | (a) | `DERIVADO` | Report de trabajo |

---

## 5 · Economía, consumo y decisión

| Constructo | Tier | Proc. | Origen | Base y reservas |
|---|---|---|---|---|
| **Tandas / ROSCAs** | **Fuerte** | (a) | `LEÍDO` | CONDUSEF: **32.7%** entre quienes ahorran informalmente. ENSAFI 2023: 41% ahorra informalmente, de ellos 22% en tandas. Vélez-Ibáñez: 130 ROSCAs, 1,300 miembros, incumplimiento **~0.005%** — sostenido solo por reputación |
| **Tequio / faena** | **Fuerte/Media** | (a) | `LEÍDO` | Persiste en Oaxaca, Chiapas, Puebla, Guerrero y barrios originarios. **Con coerción real**: multas, exclusión, faccionalismo religioso, migrantes que pagan sustituto. *No romantizar.* ⚠️ La faena bajo **usos y costumbres** queda fuera del modelo: es obligación institucional de otro orden (ADR-10) |
| **Cooperación condicional (experimentos EN México)** | **Fuerte** | (a) | `LEÍDO` | Candelo/Eckel/Johnson, **n=1,274 en 11 aldeas**: dictator 34%, ultimatum 34-46%. Trust game Caja Mixtlán ~50.7%. **Contrapeso decisivo al "México desconfiado": la conducta coopera más que la encuesta** |
| **Asociacionismo formal bajo vs. cooperación informal alta** | **Fuerte** | (a) | `LEÍDO` | ENCUCI 2020: <1 de cada 4 pertenece a algún grupo; pero **22.1% trabajó con otros en problemas comunitarios**. Las encuestas subestiman la cooperación informal |
| **Consumo compensatorio · estatus** | **Fuerte** ⚠️ **sin sostén por procedencia** | (c) | `LEÍDO` | ⚠️ **`(a)+(c)` → `(c)`, `FP-38`, 18/ago/2026:** Velandia-Morales 2022 es un experimento del CIMCYC, Universidad de Granada, con un resultado nulo declarado adentro — **no es evidencia sobre población en México**. El tier `Fuerte` queda **sin sostén por esa cita**; no se sustituye por otra. Falsador ya identificado en el programa, no ejecutado: `recovery-plan`:65 asigna `R1.4` a **ENIGH, 6 olas** — dato mexicano propio, en disco. Desenlace: gasto en bienes posicionales (marca, logo, mensualidades). Mecanismo: beneficio simbólico. Partido de `consumo_compensatorio.recompensa` por ADR-94 (ejecuta ADR-92(e)/`FP-28`) — el modelo lo marca `FUERTE como correlación`; V1 lo rompió *"como driver decisivo aislado"* — **no es la misma afirmación**, y V1 omitió el perfil 5 |
| **Consumo compensatorio · recompensa** | **Hipótesis razonable** | (a)+(c) | `LEÍDO` | Desenlace: ingesta de comida y alcohol. Mecanismo: beneficio hedónico. Partido de `consumo_compensatorio.estatus` por ADR-94 (ejecuta ADR-92(e)/`FP-28`) — `Health, Body, Food`:35 declara *"poca medición directa"*; tier sin cambio |
| **Horizonte de planeación corto** | **Fuerte** (como adaptación) | (a) | `LEÍDO` | ENIF 2024: solo **4 de cada 10** adultos con metas de largo plazo; 68.2% espera depender de apoyos de gobierno en la vejez; 36.6% ahorró solo informalmente. **Teoría de la escasez**, no imprevisión cultural |
| **"El mexicano solo busca lo barato" (refutación)** | **Segmentada** ⚠️ | (a) | `FORENSE` | Se sostiene para **A/B/C+**; **se retira para D/E**, donde la métrica dura apunta a que gana el precio (ADR-15/29). Vacío marcado: **falta panel D/E** |
| **"Calidad y dignidad > precio en populares"** | **NO VALIDADA** | (a) | `FORENSE` | Su caso ancla (Mamá Lucha) es **publicidad, no métrica de compra**. ⚠️ La *regla del modelo* que V1 rompió era **FANTASMA** (Hito 2): el constructo se degrada por su propia evidencia, no por haber roto una regla. Lo que sigue vivo y sin probar es más modesto: *a precio igual, el encuadre importa* `[MEDIA]` |
| **"El informal paga CAT alto y es rentable"** | **Fuerte (auditado)** | (a) | `FORENSE` | IMOR regulado CNBV 5-16%, rentable vía CAT 80-97%. Azteca/BanCoppel/Findep + Banco Mundial (Bruhn & Love: +7.6% dueños de negocios informales). ⚠️ Se sostiene por su evidencia; las dos reglas que V3 dijo validar eran **fantasma** |
| **Riesgo del prestamista, no del deudor** | **Fuerte** | (a) | `FORENSE` | Famsa (autopréstamos, partes relacionadas por 1,812.2 mdp, ICAP −6.02%) y Crédito Real (cartera *evergreen* ~46%, cierre de fondeo). ⚠️ **n=2**: certificado como *"la estructura decidió estos dos"*, no como ley general |
| **BNPL como riesgo latente** | **Media** | (a) | `FORENSE` | Advertencia downstream, no desenlace ocurrido |

---

## 6 · Adopción tecnológica

*Dominio ausente de todos los glosarios previos. Es la fuente de la regla que más decisiones sostiene.*

| Constructo | Tier | Proc. | Origen | Base y reservas |
|---|---|---|---|---|
| **Utilidad + fricción baja como predictor de adopción** ⭐ | **Media-Fuerte** *en su alcance canónico* | (a) | `LEÍDO` | Fintech masiva (Nu México 13M+ clientes; 70M+ usuarios) vs. **fracaso de CoDi: 21.8M cuentas mayormente inactivas** (Banxico 2025). ⚠️ **Alcance:** `modelo §3.3` la acota a **gobierno digital** (CoDi coercitivo con riesgo fiscal vs. SPEI útil sin amenaza). Su extensión a crédito en §7 **no está autorizada** — Hito 2 |
| **Ejercicio de falsación de glosario, 27/jul/2026** ⭐ | **Veredicto informal B** | (a) | `FORENSE` | Fuente: `corpus/forense/Apuestas_Conductuales_sobre_el_Consumidor_Mexicano...md` (Etapa 3: búsqueda deliberada de contraejemplo a "utilidad + fricción baja > confianza"). Sin contraejemplo limpio tras barrer 8 dominios fuera de fintech. Candidato irresuelto: **seguro agrícola** (Fondos de Aseguramiento vs. aseguradoras externas) — no se aísla de precio, requisitos ni aprendizaje sobre si la aseguradora paga. ⚠️ **Techo estructural: el veredicto C global no es alcanzable con fuentes públicas** —los fracasos aburridos no se publican—. C solo por candidato, con dato primario. ⚠️ **Población propia (ADR-45): NO es el Hito D** (bloque append-only `RX.Y → veredicto A-D` de `hitoD-preregistro`, que no existía hasta el 28/jul) **ni el Hito C** (generadores G1-G6 de `hitoC-prueba-generadores`) — es un ejercicio suelto de este glosario, nunca archivado bajo el protocolo de ADR-40 |
| **Utilidad PERCIBIDA > confianza** ⭐ | **Hipótesis hermana** | (a) | `FORENSE` | CNSF: la limitante de los microseguros es el **escaso conocimiento de los beneficios** más la falta de canales baratos, no el rechazo al proveedor. Si se confirma, la regla mide el insumo equivocado. *Prueba:* si al elevar la comprensión sube la contratación, se reformula |
| **Brecha digital por competencia, no por rechazo** | **Fuerte** | (a) | `LEÍDO` | ENDUTIH 2024: 83.1% usa internet; **9.5% "no sabe usarlo"** |
| **WhatsApp como capa de confianza** | **Hipótesis** | (a) | `LEÍDO` | Reduce fricción de adopción. Sin evidencia conductual directa |
| **"El mexicano es tecnófobo/desconfiado por cultura"** | **NARRATIVA POPULAR** | — | `LEÍDO` | Marcada como tal en el propio report |

---

## 7 · Tiempo, conocimiento y salud

| Constructo | Tier | Proc. | Origen | Base |
|---|---|---|---|---|
| **Puntualidad como decisión situada** | **Media** | (a) | `LEÍDO` | 72% llega 5-10 min antes a reuniones **de trabajo** y 80% entrega a tiempo, pero solo **38%** llega antes a reuniones **sociales**. Muestra urbana escolarizada. *Mata el cliché: no hay impuntualidad de rasgo, hay contexto formal vs. informal* |
| **"Ahorita" como elasticidad del compromiso** | **Hipótesis razonable** | (a) | `LEÍDO` | Fuentes lexicográficas y periodísticas, **no medición conductual**. El report se abstiene de elevarlo |
| **"El mexicano es impuntual / no sabe planear"** | **NARRATIVA POPULAR** | — | `LEÍDO` | Cliché sin sustento representativo |
| **Verdad por proximidad del emisor** | **Hipótesis razonable** | (a) | `LEÍDO` | Traslado de la confianza radial a la evaluación de información. 81.2% usa internet, 91.2% mensajería; confianza en noticias **31%** (Reuters 2026) |
| **Educación como seguro anticaída / credencialismo** | **Fuerte** | (a) | `LEÍDO` | Retorno de la educación superior entre los más altos de la OCDE: **50%–150%** más que bachillerato. Coexiste con PISA 2022: **66% no alcanza nivel básico en matemáticas** |
| **Saber del oficio (competencia informal)** | **Hipótesis razonable** | (a) | `LEÍDO` | Vía prestigiada de competencia en segmentos populares/informales |
| **Entorno alimentario como estructura** | **Fuerte** | (a) | `LEÍDO` | ENSANUT 2022-2023 + efecto del impuesto al refresco por NSE (Colchero). *"Los mexicanos eligen comer mal"* y *"el fatalismo ante la diabetes es cultural"* = **narrativas populares** |
| **Farmacia con consultorio anexo como primer recurso** | **Fuerte** | (a) | `LEÍDO` | Automedicación **41%**, consultorio de farmacia **28%** como primer recurso. Adaptación racional al costo, el tiempo y el trato — no ignorancia |

---

## 8 · Política y cívico

| Constructo | Tier | Proc. | Origen | Base |
|---|---|---|---|---|
| **Agencia del votante; movilización/identidad > compra** | **Fuerte** | (a) | `FORENSE` | **El único constructo del corpus con identificación causal**: RCTs revisados por pares + contrafactual limpio (2018: AMLO ganó por 31 puntos repartiendo *menos* dádivas). ✅ Hito 2: es el único vertical cuyas reglas ancla son **fieles** al motor, tier incluido |
| **Desconfianza institucional calibrada (no apatía)** | **Fuerte** | (a) | `LEÍDO` | ENVIPE 2025: cifra oculta **93.2%**, denuncia 9.6%, resolución positiva **0.8%**. No denunciar es cálculo, no desidia. Participación presidencial **59.8%** vs. judicial **12.86%** |
| **Cifra negra 93.2%** | Fuerte **con reserva definicional** ⚠️ | (a) | `LEÍDO` | Agrega delitos **no denunciados** + denunciados **sin averiguación previa**. **No es P(no denuncia)**: usarla así confunde dos cantidades |
| **Transferencia directa universal → conserva autonomía de voto** | **Fuerte** | (a) | `FORENSE` | Sin **monitoreo del voto individual** ni sanción creíble, subir el tamaño del beneficio **no mueve el voto**. Base: RCTs con árbitro (De La O 2013; Imai, King y Velasco 2020) + contrafactual 2018 (el PRI repartió al **88.9%** de sus objetivo y perdió por **31 puntos**; Morena repartió al 15.5% y ganó). ⚠️ **v5.3: se retira «ni broker»** — ver `conf.08` |
| **Transferencia directa → atribución al líder, expresada como aprobación** | **Media**, **correlacional** ⚠️ **CONFUNDIDO** | (a) | `FORENSE` | *Desdoblado en v5.3.* Tier **leído literalmente del forense V2**: *"Tier: MEDIA (correlacional para la 4T)"*. ENEM 2024 (N=2,700): identificación morenista y aprobación de AMLO son **predictores dominantes**; ser beneficiario es **factor secundario**. **Confusores:** aprobación presidencial (73%), identidad partidista, maquinaria territorial, voto retrospectivo por salario mínimo, debilidad opositora. ⚠️ **La "gratitud" puede no ser psicológica:** el propio forense la lee como posible **voto retrospectivo racional** —recompensar ingreso real recibido—, no lealtad afectiva. **Falsador pre-registrado por el forense:** un RDD sobre la Pensión del Bienestar con efecto electoral **independiente de la aprobación presidencial** |
| **"Entitlement de derecho"** (el apoyo *corresponde*; el titular es reemplazable) | **Hipótesis** | (a) | `LEÍDO` | *Separado del anterior en v5.3: eran hipótesis **rivales** pegadas por una diagonal.* Ancla **institucional**: la pensión está en el **art. 4.º constitucional desde 2020**. Lo **no medido** es que el beneficiario lo viva así. **Falsador candidato:** conducta de reclamo ante retraso o falla de pago — *un derecho se exige, un favor se agradece* — observable sin preguntar por estados mentales |
| **Clientelismo desde abajo (agencia)** | **Media**; *"entitlement de derecho"* = **Hipótesis** | (a) | `LEÍDO` | Efecto de programas sociales sobre aprobación: hasta ~15 puntos (MCCI-Reforma). *"Los pobres venden su voto"* = **narrativa popular** |
| **Polarización afectiva moderada y centrada en líderes** | **Media** | (a) | `LEÍDO` | No ideológica, magnitud moderada. *"México partido en dos bandos irreconciliables"* = **narrativa popular** |
| **Linchamientos / autodefensas como respuesta al vacío** | **Fuerte** (CRAC-PC) | (a) | `LEÍDO` | Legalizada en 2011 (Ley 701); ~64% del estado de Guerrero. Con faccionalismo e infiltración documentados. *"Barbarie / atraso cultural"* = **narrativa popular** |
| **"La baja denuncia refleja tolerancia al delito"** | **Mito** | (a) | `LEÍDO` | Refutado: es cálculo ante 0.8% de resolución |
| **"La mordida es inherente a lo mexicano"** | **Mito (Fuerte)** | (a)+(c) | `LEÍDO` | Equilibrio de Bardhan. Uruguay y Chile, latinos, con corrupción mucho menor. *Falla si:* la mordida persiste tras digitalizar el trámite |
| **"El voto de clase media es antisistema"** | **Hipótesis** ↓ | (a) | `FORENSE` | Degradado en Ronda 4. ⚠️ La regla que V2 estresó era **FANTASMA** (Hito 2): consistente con patrones agregados, ningún estudio causal lo prueba |

---

## 9 · Los ocho dominios incorporados en v5

### 9.1 Ausencia y duelo — desaparecidos · `LEÍDO`

| Constructo | Tier | Base |
|---|---|---|
| **Pérdida ambigua / duelo suspendido** — estructura | **Fuerte** | 135,445 desaparecidos (CIDH, 30/06/2026); >70,000 cuerpos sin identificar; impunidad **99.6%**; activación del Art. 34 de la ONU (abril 2025) |
| Distrés severo en familiares | **Media** | Smid/Blaauw/Lenferink n=29; Almanza-Avendaño n=5 madres. Muestras pequeñas |
| Búsqueda como afrontamiento de doble filo | **Hipótesis** | Agencia + herida |
| Daño intergeneracional | **Hipótesis** | Por analogía (Holocausto/Argentina); poco medido en México |
| **"El mexicano tiene una relación especial con la muerte que lo ayuda"** | **NARRATIVA POPULAR** | ⭐ Falso; confunde cultura con estructura. **El cliché más grande del país sobre sí mismo, y estaba sin registrar** |
| "Las madres coraje que transforman el dolor en lucha" · "la búsqueda sana" | **NARRATIVA POPULAR** | Romantización |

### 9.2 Pareja, cortejo y apps · `LEÍDO`

| Constructo | Tier | Base |
|---|---|---|
| Retraso nupcial + auge de la unión libre | **Fuerte** | INEGI/EMAT 2022-23, ENADID, ENOE, censo |
| Violencia de pareja y noviazgo | **Fuerte** | ENDIREH 2021; Rodríguez-Hernández 2023 |
| Secularización parcial; matrimonio igualitario 2022; 5.1% LGBT+ | **Fuerte** | Censo 2020; ENDISEG 2021 |
| Psicometría de celos e infidelidad | **Media** | EMUCE, IMIN — **muestras universitarias, no representativas** |
| Guiones marianismo/caballerismo en la díada | **Media** ⚠️**(b)** | Hereda la marca de diáspora |
| Efecto causal de apps sobre calidad relacional | **Hipótesis** | Desacople sexo/romance/matrimonio |
| **"El mexicano celoso/machista/infiel"** · "unión libre = fracaso" | **NARRATIVA POPULAR** | Esencialismo |

### 9.3 Juventud / Gen Z · `LEÍDO` — *el perfil 5 del modelo*

| Constructo | Tier | Base |
|---|---|---|
| **Adultez aplazada** | **Fuerte** | EDER 2025: **16.9%** de los nacidos 1998-2007 se independizó antes de los 18, vs. **31.1%** en generaciones previas. Primera unión antes de los 18: de 22.4 a 15 de cada 100. OCDE: **46%** de los de 20-30 vive con sus padres |
| Malestar psicológico y conducta suicida por edad y sexo | **Fuerte** | ENSANUT 2022; ENCODAT 2025 |
| **"No rechazan la jerarquía, exigen que se justifique"** | **Media** | Berkeley 2024 + Deloitte 2025 |
| Voto joven 2024; actitudes hacia la democracia | **Media** | Mitofsky; Latinobarómetro 2024 |
| Crisis de salud mental atribuida a redes | **Hipótesis** | Correlación robusta, causalidad discutida |
| "Nativos digitales" · "generación de cristal" · "los ninis son ociosos" | **NARRATIVA POPULAR** | |

⚠️ **Dos notas de alcance.** El fenómeno es **global** (Grecia ~30.7, España ~30.3 años de emancipación media): es **efecto de periodo**, no rasgo mexicano. Y el Hito 2 mostró que **V1 borró el perfil 5** de la regla de consumo compensatorio — el perfil existe en el motor, no existía en el glosario, y nunca se probó.

### 9.4 Vejez y cuidado intergeneracional · `LEÍDO`

| Constructo | Tier | Base |
|---|---|---|
| **Hogar multigeneracional como colchón** | **Fuerte** | **82%** de los hogares con adultos mayores son nucleares/ampliados (tamaño medio 3.4); hasta **28%** de los hogares mexicanos son multigeneracionales |
| **Su erosión** | **Fuerte** | Hogares unipersonales de mayores: **16.8%** (1.8 millones). Chile redujo a la mitad los arreglos de tres generaciones entre 1982-2017 |
| **Brecha de cuidado por género** | **Fuerte** | ENUT 2024: mujeres **39.7 h/sem** vs. hombres **18.2** — brecha de 21.5 horas |
| Baja cobertura de pensión contributiva y su sesgo de género | **Fuerte** | CONEVAL, CONSAR |
| Sobrecarga y depresión en cuidadoras | **Media** | Escalas Zarit locales |
| Familismo-como-seguro · "familismo desprotegido de ingreso medio" | **Hipótesis** | |
| "Aquí a los viejos se les cuida" · "economía plateada = 28% del PIB" · abandono generalizado | **NARRATIVA POPULAR** | ⚠️ La corresidencia es **en parte estrategia económica**, no puro amor filial |

### 9.5 Religiosidad · `LEÍDO` — *dominio que el v4 señaló como decisivo y no llenó*

| Constructo | Tier | Base |
|---|---|---|
| Declive católico y auge de "sin religión" | **Fuerte** | Serie censal INEGI 1895-2020; generacional y urbano |
| Distribución regional (Chiapas vs. Bajío) | **Fuerte** | |
| Guadalupanismo masivo | **Fuerte** | Cifras oficiales de peregrinación |
| Brecha de práctica católico/evangélico | **Fuerte** | ENCREER 2016 |
| Expulsiones de Chiapas y sistema de cargos | **Fuerte** | |
| Afrontamiento religioso como recurso de salud mental | **Media** | Estudios mexicanos con muestras acotadas |
| **Fe ≠ fatalismo** | **Hipótesis razonable** | Bien fundamentada, sin consenso cerrado |
| Teología de la prosperidad como respuesta a la precariedad | **Hipótesis** | |
| "México es profundamente católico y ya" · "el guadalupanismo une a todos" · "La Santa Muerte es solo del narco" | **NARRATIVA POPULAR** | |

### 9.6 Migración México–EE.UU. · `LEÍDO` (`[SÓLIDO]` propio)

| Constructo | Tier | Base |
|---|---|---|
| **Contracción de remesas** | **Sólido** | **61,791 mdd** en 2025, **−4.6%** frente a 2024 — primera caída en más de una década |
| **El estatus migratorio modula todo** | **Sólido** | Documentado vs. indocumentado: ansiedad, circularidad, planeación, identidad |
| Separación: efecto distinto en quien va y quien queda | **Sólido** | Duelo migratorio ≠ síndrome de Ulises (solo casos extremos) |
| **Ansiedad por deportación como respuesta racional** | **Sólido** | No rasgo cultural |
| Consecuencias en niños ciudadanos de hogares de estatus mixto | **Sólido** | |
| Desplazamiento forzado interno por violencia criminal | **Sólido** | ≥28,900 personas en 2024, **+129%** |
| Remesas sostienen consumo, no transforman estructura | **Sólido** | Canales, De Haas |

⚠️ **Este report es la fuente de la marca (b)** de buena parte del corpus. Todo constructo de diáspora debe citarlo.

### 9.7 Humor · `DERIVADO` (sin mapa de evidencia)

| Constructo | Tier | Base |
|---|---|---|
| Escalas de humor desarrolladas en y para población mexicana | **Fuerte** (declarado inline) | Superan la dependencia de adaptaciones extranjeras |
| Humor como afrontamiento | **Media-débil** | Toribio y Andrade 2024 — ⚠️ *el humor es un ítem dentro de una batería más amplia, no la variable central; la evidencia es indirecta* |
| Humor digital masivo | **Fuerte** (descriptivo) | 93.0M de usuarios activos (DataReportal, ene 2025); #MéxicoOIA >1M de videos en 24h |
| **Albur como negociación indirecta de jerarquía** | **Media** | Doble sentido deniable: permite expresar desacuerdo y probar límites sin las consecuencias de la confrontación |
| Humor organizacional mexicano | ⚠️ **VACÍO** | El report declara ausencia de investigación revisada por pares 2023-2026; el contenido en línea es marketing o generado por IA |

⚠️ **Aporte crítico a conf.04.** El WHR 2025 (#10 de 147, 6.979/10) es **de este report**, y su propio caveat advierte que la escalera de Cantril mide **evaluación vital, no humor ni alegría**, y que *"la conexión humor-bienestar es inferencial"*. Parte de la "alegría declarada" es un instrumento midiendo otra cosa.

### 9.8 Mérito y movilidad · `DERIVADO`

| Constructo | Tier | Base |
|---|---|---|
| **Movilidad bloqueada** | **Fuerte** | CEEY/ESRU-EMOVI 2023: de cada 100 nacidos en el quintil más bajo, **50 no salen** y **solo 2 llegan al más alto**; 73 siguen en pobreza por ingresos |
| **La educación dejó de ser motor de movilidad** | **Fuerte** | Solo **1 de cada 10** con padres de primaria o menos alcanza estudios profesionales; con padres profesionales, **7 veces** más probable |
| **Meritocracia rechazada como explicación** | **Media** ⚠️ | Mijs y Hoy 2021, N=1,600: **12%** atribuye la riqueza al mérito, 15% la pobreza; **47%** la atribuye a corrupción. *Caveat propio: trabajo de campo 2017, sin réplica reciente; usar como referencia estructural, no como medición actual* |
| Descenso de pobreza y desigualdad | **Fuerte con reserva** | Pobreza multidimensional 29.6% (de 43.2% en 2016); Gini 0.391, el más bajo registrado —sin transferencias habría sido 0.450—. *Reserva: cambios de cuestionario en la ENIGH 2024 afectan comparabilidad* |
| Informalidad | **Fuerte** | **54.8%** de la población ocupada (ENOE, 1T 2026) |

---

## 10 · Falsabilidad de los constructos maestros

Las instrucciones piden decir qué evidencia cambiaría cada patrón fuerte — sobre todo para que "adaptación racional" no se vuelva infalsable.

- **Confianza radial** → la falsaría hallar cooperación alta con desconocidos **sin** puente personal, monitoreo ni liderazgo confiable, en entorno de impunidad alta. *Los experimentos de Candelo ya la tensionan: la conducta coopera más que la encuesta.*
- **Tres sustitutos del enforcement** → la falsaría documentar cooperación sostenida donde ninguno de los tres opera, o colapso donde los tres están presentes.
- **Adaptación racional (general)** → la falsaría que la conducta **no** cambie cuando cambia el incentivo estructural. *Los datos de tiempo muestran lo contrario (72% vs. 38%): el patrón sobrevive su propia prueba.*
- **Violencia como destructor selectivo** → la falsaría que la victimización erosionara también la confianza **interpersonal cercana**.
- **Pigmentocracia** → la falsaría que el efecto del tono de piel desapareciera al controlar por origen social, red y escolaridad. *Ese control aún no existe en el corpus: es la deuda empírica del constructo.*
- **Utilidad + fricción baja > confianza** → la falsaría un producto de alta utilidad y baja fricción que fracasara por desconfianza pura. **Ejercicio de este glosario corrido, 27/jul/2026: veredicto informal B** (§6) — no el Hito D ni el Hito C, ver ADR-45. No apareció contraejemplo limpio; queda un candidato irresuelto y un techo estructural.
- **Estructura > cultura** → la falsarían casos de misma estructura con conducta divergente. **Ya existen dos dentro del corpus: Argentina e Israel.** Por eso el constructo está en Media.

---

## 11 · Conflictos abiertos

| # | Conflicto | Estado |
|---|---|---|
| **conf.01** | Calidad vs. precio (consumidor §10 vs. ADR-15/V1) | ✅ **Resuelto por precedencia**: segmentado — A/B/C+ sí, D/E no |
| **conf.02** | **Policronía**: se adopta el mecanismo de `Tiempo` (norma contextual + estructura) y se conserva el desenlace de `Trabajo` (el mito es falso) | ✅ **Resuelto por ADR-94, 18/ago/2026.** No es empate ni "adoptar uno y archivar el otro": la policronía sobrevive como preferencia individual medible, sin adscripción nacional; no como rasgo cultural mexicano. Razón escrita: `forense/BENCHMARK-conf02-policronia-2026-08-17.md` |
| **conf.03** | Hofstede como evidencia | ✅ Resuelto por ADR-06 (correlato); **parchado en la fuente el 28/jul/2026** *(la v5 lo daba por hecho el 27/jul; la verificación encontró que el parche no existía en el report)* |
| **conf.04** | **Alegría declarada vs. malestar documentado** | ✅ **Resuelto por ADR-27: es un ARTEFACTO DE AGREGACIÓN, no una contradicción.** Ambos lados son verdaderos en sus segmentos y solo chocan al promediarlos en un número nacional. *Alineado con `gobernanza §5.1` el 28/jul — la v5 lo declaraba "irresuelto" y la gobernanza "resuelto"; el texto correcto es el de la gobernanza.* **Queda vivo, separado y menor:** la escalera de Cantril mide **evaluación vital, no alegría** (desajuste de instrumento, casillero S5) |
| **conf.05** | **Consumo compensatorio** partido en dos constructos con tier propio: `consumo_compensatorio.estatus` (Fuerte) y `consumo_compensatorio.recompensa` (Hipótesis razonable) | ✅ **Resuelto por ADR-94, 18/ago/2026.** No había una sola cosa que promediar — son dos hallazgos con desenlace y mecanismo distintos (ver `glosario:136`). Razón escrita: `forense/BENCHMARK-conf05-consumo-compensatorio-2026-08-17.md` |
| **conf.06** | **Magnitud de la confianza interpersonal**: 21.8% vs. 32.1% en la **misma ENCUCI 2020** | ✅ **Cerrado por ADR-64, 5/ago/2026.** No competían: son **tres reactivos distintos** de la pregunta 5.1, ENCUCI 2020, ponderador `FAC_SEL`, los tres al corte **≥8/10** — `AP5_1_1` ("la mayoría de las personas") = **21.8%** · `AP5_1_3` (vecinos) = **32.1%** · `AP5_1_2` (personas que conoce) = **62.1%**. Resuelto por lectura el 28/jul (`README.md:91`), propagación al canon pendiente ocho días; confirmado contra microdato por C-06b (las tres dentro de su IC95% a ≥8/10, ninguna a ≥6/10). Las otras cifras del racimo (12% WVS 2012, 22% Latinobarómetro/LAPOP, 18% Pew 2025) **no son ENCUCI y quedan fuera de este cierre** — "confianza radial — magnitud" como constructo **no queda establecida** (§2). *El residual quedó adjudicado por `ADR-111`/`FP-58` (18-19/ago/2026): el 22% no tiene procedencia sostenible (WVS 2018 REFUTADA 10.51%; Latinobarómetro 2024 NO SOSTENIDA 26.06%; LAPOP error de categoría; ENAFI indecidible), el 18% de Pew reproduce exacto, el 12% queda indecidible por falta de la ola — ver `glosario-v5_6.md:84`* |
| **conf.08** ⭐ | **El `PORQUE` de la regla de autonomía de `§3.7` decía "no hay monitoreo **ni broker**"** — y el forense V2 lo declaró **ROTO PARCIALMENTE** desde la Ronda 4: **Langston (2025) documenta a los Servidores de la Nación** como capa de intermediación centralizada. **Sí hay broker** (de afiliación y propaganda), aunque **no de monitoreo del voto individual** | ✅ **Corregido en `modelo v2.3` el 28/jul.** ⚠️ **Séptimo caso de propagación fallida:** la rotura estaba escrita, fechada y archivada en el forense, y **nunca bajó al motor**. No la detectó ninguna auditoría de archivos — apareció al **partir la regla para poder falsarla**. *Lección: la deuda documental que las auditorías de consistencia no ven es la que vive dentro de una cláusula compuesta* |
| **conf.07** ⭐ | **`modelo §3.7` empaquetaba dos afirmaciones de tier distinto bajo un solo `[FUERTE]`**: *"se vive como derecho/gratitud al líder"* (**Hipótesis**, sin identificación causal) + *"conserva autonomía de voto"* (**Fuerte**, con RCT y contrafactual) | ✅ **Resuelto por ADR-106, 18/ago/2026.** El **acto material** es anterior al sello y por eso la deuda sobrevivió tres semanas sin ADR: la regla **ya está partida** desde `modelo v2.1` (`modelo-decision:437`) y la diagonal desde `v2.3` — hoy son tres reglas con tier propio: `civico.voto.agencia_con_secreto` **`[FUERTE]`**, `civico.transferencia.entitlement_derecho` **`[HIPÓTESIS]`**, `civico.transferencia.atribucion_lider` **`[MEDIA]`** correlacional ⚠️ CONFUNDIDO. **El ascenso HIPÓTESIS→FUERTE del cambio 10 se sostiene** sobre la primera. **Requisito de salida VERIFICADO y SATISFECHO** (primera vez desde que se escribió): el pre-registro del Hito D cita la **mitad**, no el paquete — `forense/hitoD-preregistro-v2_0.md:166`, ficha `R7.3`, `[FUERTE]`, con P-02 y P-03 incorporadas; cero fichas con tier dependiente del empaquetado |

**Sobre conf.04**, el más delicado: de un lado, felicidad #10 mundial (WHR 2025) y 83-88% de autoevaluación positiva; del otro, 18.1M de carga de salud mental (GBD 2021), 39.8% de soledad en adultos mayores y 135,445 desaparecidos. Parte es real (capital de vínculos), parte es artefacto de medición (negación adaptativa, sesgo de positividad, simpatía) **y parte es que el instrumento mide evaluación vital, no alegría** (§9.7). **Declararlo irresuelto es el entregable.** Ambas resoluciones fáciles son esencialistas: *"el mexicano feliz pese a todo"* y su gemela *"la felicidad declarada es pura negación"*.

Las otras cuatro contradicciones heredadas del v1 se mantienen: aspiración + cinismo · deseo hedónico + aversión al riesgo · marca extranjera + orgullo nacional · red familiar + independencia retrasada.

---

## 12 · Firewall genético

Prohibida la inferencia **ascendencia → conducta de grupo**. No existe un "genoma mexicano": la variación de mestizaje es tal que la genética de poblaciones, bien leída, es **argumento contra** el determinismo. Se admite un canal individual estrecho, molecularmente explícito y de efecto pequeño frente a la estructura.

| Canal | Estado |
|---|---|
| **Metabolismo del alcohol** (ADH1B rs1229984) | **El único canal individual real.** Holmes 2014: −17.2%. El *firewater myth* está desmentido por ausencia de ALDH2 |
| **Metabolismo de nicotina** (CYP2A6) | Canal individual acotado |
| **Tolerancia al riesgo** | Poligenicidad extrema; PGS ≈1.6% de varianza. Predicción **despreciable** frente a la estructura |
| **MAOA "gen guerrero"** | Registrado como **el caso de CÓMO NO hacerlo** |

El canal pertenece al report de **salud/sustancias y a `Genetica_y_Conducta`**, no al de genómica poblacional (que es biología y mercado). *Cuidado con la predisposición metabólica: modifica una consecuencia, no una decisión.*

⚠️ **Defecto operativo pendiente:** el validador evalúa el firewall con **granularidad de línea**, así que una refutación del determinismo genético lo dispara —para negarlo hay que nombrarlo—. Arreglo: evaluar por entrada YAML.

---

## 13 · Los 144 números *(eran 107 en v5)*

**⚠️ Recomputado en v5.1 (28/jul/2026). El v1 tenía 107; el v2 tiene 144.** El modelo v2 §6 declaraba el aumento (*"el v2 aumenta el conteo"*) pero nunca publicaba la cifra nueva. Aquí está, y es reproducible por lectura:

| Clase | v1 | **v2** | Qué significa |
|---|---|---|---|
| MEDIDO | 4 | **4** | Viene de una medición real |
| DERIVADO | 6 | **6** | Calculado desde algo medido |
| ORDINAL→CARDINAL | 54 | **60** | Era un orden ("más que"), se le puso número |
| ASIGNADO | 43 | **74** | Se puso a criterio |
| **TOTAL** | **107** | **144** | **97.2% no medido** (era 96%) |

**Desglose del salto 107 → 144, línea por línea:**

| Componente | v1 | v2 | Δ | Por qué |
|---|---|---|---|---|
| `params_base` de perfil | 54 | **90** | +36 | 9 → 15 parámetros por perfil × 6 perfiles |
| ↳ de los cuales: `familismo` desdoblado | — | — | +6 | ADR-30 · clase **ORDINAL→CARDINAL** (la etiqueta "medio/alto" existe en la tabla del modelo) |
| ↳ de los cuales: `confianza_institucional` de escalar a **vector de 6** | — | — | +30 | ADR-28.b · clase **ASIGNADO**. ⚠️ **Los 30 no están escritos todavía**: el modelo §1.3 declara el vector y da porcentajes *nacionales*, pero no lo puebla **por perfil**. Nadie ha medido confianza en la Marina por perfil |
| Coeficientes de generador | 14 | **15** | +1 | ADR-30 · `familismo_obligacion` en G5, **ASIGNADO** y sin magnitud: su spec es "signo negativo o no monotónico" |
| Probabilidades de regla | 39 | **39** | 0 | Sin cambio de esquema. ⚠️ Corresponde a las **18 reglas implementadas** de 42; recuento pendiente cuando existan los 10 `rules/*.yaml` (hoy solo existe `tramite.yaml`) |

**Los 15 coeficientes por generador (v2):** G1a:2 · **G1b: a revisión — el generador está CONTRADICHO** · G2:2 · G3:3 · G4:4 · **G5:3** · G6:1. *(La v5 decía 14 con `G1` sin desdoblar y `G5:2`.)*

⚠️ **DEUDA ABIERTA CON REQUISITO DE SALIDA — parámetros de dispersión.** ADR-28.d obliga a que **cada `params_base` sea una distribución, no un punto**, y el check de compilación rechaza varianza intraperfil cero. Eso implica **90 parámetros de dispersión adicionales** que **hoy no existen ni tienen familia declarada**. Mientras no se declaren, el check de 28.d no puede correr: *es un principio sin artefacto de salida.*
**Requisito:** `procedencia.yaml` debe listar, para cada uno de los 90 `params_base`, su familia de distribución y su parámetro de dispersión con clase de procedencia. Si el archivo no los tiene, el conteo real no es 144 sino 234 y 90 de ellos son invisibles.

Los `params_base` no son medidos ni inventados: son la **cuantificación de etiquetas** ("alto", "corto", "muy baja"). Como `params = base + Σ coef` y los coeficientes también son asignados, la aritmética **conserva orden pero no magnitud**.

→ **Ninguna salida del simulador debe reportarse con decimales.** Rangos o categorías.

**Los 15 coeficientes de generador** están en `procedencia.yaml` (v0.2.0). Todos **ASIGNADOS**, **cero medidos**. Esta capa **nunca ha sido validada**, ni por vertical ni por falsación. `unico_calibrable_hoy` se retiró (ADR-49): la vía ENOE no identifica la elasticidad — ningún cuestionario ENOE/ENOEN trae conducta financiera (`forense/hallazgos.md`, 31/jul/2026). Ningún coeficiente de generador tiene ruta de calibración hoy.

---

## 14 · Fugas de custodia detectadas

1. ✅ **CERRADA el 28/jul/2026 en la ficha; parcialmente en el modelo.** *(Texto v5: "la procedencia (b) muere antes de la capa operativa. Glosario ✅ → modelo ⚠️ → ficha ❌ cero → verticales ❌".)* **La ficha regenerada sí lleva las marcas (a)/(b) y las declara en su cabecera**, con leyenda propia y advertencia de que la marca viaja con el constructo. Persiste el residuo: Y los constructos se fugan de su dominio marcado: `§1.3` usa *"modificador marianismo"*, `§3.6` usa *"PORQUE simpatía"*, y **`§3.4` tiene una regla `[FUERTE]` cuyo driver nombrado es machismo** —constructo Media (b)— sin marca. El patrón conductual probablemente tiene dato mexicano; la **atribución causal** no.
2. ✅ **CERRADA el 28/jul/2026 — los tres casos.** *(Texto v5: "los dos primeros parchados el 27/jul; el tercero requiere decisión. ADR-29 lo ordena y sigue sin aprobar".)* **Las dos afirmaciones eran falsas:** ADR-29 **sí** está aprobado (gobernanza v1.1), y los dos parches **no existían en el report** — la decisión se había tomado y registrado, pero la nota nunca bajó al documento. Estado real hoy: Hofstede en consumidor **parchado 28/jul**; honor en comunicación **parchado 28/jul**; honor "híbrido" en foundational **resuelto por ADR-31 y parchado 28/jul**. Los tres llevan nota de corrección fechada en la fuente (ADR-29.a).
⚠️ **Lección con requisito de salida:** el registro decía ✅ sin que nadie hubiera verificado el archivo. **Un ADR de retropropagación no se marca aplicado sin `grep` contra el report dueño.**

⚠️ **CUARTO caso, hallado el 28/jul después de cerrar los tres primeros:** la fila de **Marianismo** de este mismo glosario afirmaba *"marca añadida a la fuente el 27/jul"* — y tampoco se había añadido. **El patrón no estaba en tres lugares: estaba en cuatro, y el cuarto vivía dentro del glosario.** Corregido y parchado inline el 28/jul (v5.2).
**Consecuencia:** toda anotación del tipo *"parchado / marcado / añadido a la fuente"* que exista hoy en este glosario y **no** lleve la fecha 28/jul debe considerarse **no verificada** hasta que alguien corra el `grep`. Cuatro de cuatro resultaron falsas.
3. ⚠️ **ABIERTA, pero ya con artefacto de salida.** *La regla estrella nunca tuvo constructo tierizado, y por eso pudo migrar de dominio sin que nada rechinara.* La v5.1 cierra los tres huérfanos detectados (`familismo_apoyo`, `familismo_obligacion`, `transferencia directa universal`), pero **la ruta sigue abierta**: nada impide que la próxima regla nazca sin tier leído.
**Requisito de salida (nuevo, ADR-32 propuesto):** el validador rechaza toda regla de `modelo §3` cuyo `PORQUE` nombre un constructo que no exista en este glosario. La comprobación es mecánica —`grep` del constructo contra §2-§9— y **falta visiblemente si no se hace**: sin ella, el principio es decorativo. *Éste es el patrón que explica casi todos los fallos del programa: principio declarado sin requisito de salida.*

---

## 15 · Deudas vivas

- **PD-01** — 14 descartes irrecuperables. **No reconstruir.**
- ~~**conf.07** — sin ADR~~ — ✅ **sale de esta lista, re-derivado 18/ago/2026 desde §11: resuelto por ADR-106** (`ACTO CONF-07-CIERRE`, el acto propio que la propia línea anunciaba; el sello llegó, la partición ya estaba ejecutada desde `v2.1`). *(Con ésta, **ninguno de los ocho conflictos de §11 queda abierto**: conf.02 y conf.05 salieron el 18/ago, resueltos por ADR-94; conf.04 por ADR-27; conf.06 por ADR-64; conf.08 estaba corregido en `modelo v2.3`. Estado derivado de §11, no tecleado.)*
- **Panel D/E de consumo popular** — dato primario que no existe.
- **Confianza radial como canal medible** — hipótesis sin aislar (ADR-20).
- **Control por origen social y red** en pigmentocracia — no existe en el corpus.
- **Los 15 coeficientes de generador** — nunca validados. *(Eran 14; ADR-30 añadió `familismo_obligacion` en G5.)*
- **Los 30 componentes de `confianza_institucional` por perfil** — el vector está declarado (ADR-28.b) y **sin poblar**. Nuevo en v5.1.
- **Los 90 parámetros de dispersión de ADR-28.d** — obligatorios por esquema, inexistentes en archivo. Nuevo en v5.1.
- ~~**conf.07** — `modelo §3.7` empaqueta Fuerte + Hipótesis bajo un solo tier. Nuevo en v5.1.~~ — ✅ **duplicado de la línea de arriba**, arrastrado desde v5.1 y no visto por ninguna auditoría hasta hoy; cerrado por el mismo `ADR-106`. *(Hallazgo colateral del acto: la re-derivación de §15 desde §11 lo delató; una lista mantenida a mano puede llevar la misma deuda dos veces sin que ningún vigía lo note.)*
- **`trampa social`** — usado por el motor, **sin tier leído**. Ver §16. Nuevo en v5.2.
- ~~`bandwidth tax`~~ — ✅ **retirado del motor en v2.4**: tenía veredicto forense desfavorable (P-01), no solo ausencia de tier.
- ~~Los 6 veredictos forenses que nunca bajaron al motor~~ — ✅ **los seis aterrizados el 28/jul** (v2.4 y v2.5). Ver `barrido-propagacion-forense`.
- **El motor no tiene entidad prestamista** — frontera declarada de **ADR-35**. El hallazgo *"el riesgo vive en el fondeo del prestamista, no en el deudor"* no puede representarse; su refutación (`ref.A.04`) sigue **sin objeto**. Nuevo en v5.5. *(19/ago/2026: enmienda a ADR-35 redactada y no ejecutada — `forense/notas/2026-08-19-adr35-enmienda-borrador.md`, `FP-61`. Las otras siete refutaciones sin objeto de la misma batería ya ganaron variable declarada, `ADR-117`, `modelo §1.1.G`.)*
- **Anotaciones de "parchado" sin fecha 28/jul** — no verificadas. Cuatro de cuatro resultaron falsas. Nuevo en v5.2.
- **Humor organizacional** — vacío declarado por el propio report.
- ~~Foundational y su "híbrido" de honor~~ — ✅ **resuelto por ADR-31 y parchado en la fuente el 28/jul/2026.**
- ✅ ~~Tabulado ENA 2017 + AMUCSS 2014 — cerrarían el candidato agrícola~~ — **CERRADA el 28/jul/2026.** Los dos datos existen y cierran el candidato, pero **como `D` (inejecutable), no como refutación ni confirmación.** ENA 2017: **solo 5% de las UP** tienen póliza, 98% de ellas de pequeños y medianos. AMUCSS 2014: los productores **de temporal y minifundistas no han adoptado** los programas. Y el mecanismo, de la directora de AMUCSS: *"si no es porque el seguro se vuelve una obligación al obtener financiamiento, no existe la demanda"* — que es **exactamente el confusor pre-registrado**. Ver `hitoD-R1.1`.
- ⚠️ **El instrumento de prueba no existe para la población volátil** *(nuevo en v5.6)*. El **Seguro Agrícola Catastrófico** —el que cubre al productor de temporal— **NO PUEDE SER CONTRATADO POR LOS PRODUCTORES** (SADER, textual): lo contrata la Secretaría con los estados, 80/20, y el productor aporta ~**2.5%** de la prima. Los **Fondos de Aseguramiento**, que sí son voluntarios, concentran **62% de fondos y 66% de cobertura en Sonora-Sinaloa-Tamaulipas** — riego y gran extensión. **La ausencia de seguro voluntario entre productores de temporal es exclusión de mercado, no horizonte corto. Leerla como preferencia temporal es la confusión estructura-por-cultura en su forma más pura.**
- **ENIF 2024** — la prueba de falsación usó la ola 2018; el corpus usa 2024.
- **Pragmática en lenguas indígenas** — ausente.
- **Cero datos primarios propios** — deuda del programa, no de ningún report.

---

## 16 · Constructos que el motor usa **sin tier leído** *(nuevo en v5.2 — salida del check ADR-32.c)*

> **Cómo se detectaron.** Primera corrida del check de ADR-32.c —*el validador rechaza toda regla de `modelo §3` cuyo `PORQUE` nombre un constructo ausente de este glosario*—, por `grep`, el 28/jul/2026. **El check falló en su estreno, que es exactamente lo que debe poder hacer un requisito de salida.**
>
> ⚠️ **Estas entradas NO llevan tier, y es deliberado.** Un tier se **lee** de un report con mapa de evidencia; ninguno de los dos está tierizado en ningún report. Inventarles un tier aquí metería por la puerta de atrás justo lo que ADR-02 prohíbe. **Registrar el hueco es el entregable; rellenarlo sería el fallo.**

| Constructo | Dónde lo usa el motor | Qué es trazable | Qué falta |
|---|---|---|---|
| **Trampa social** | `§3.3`, **las dos reglas `[FUERTE]`** de la mordida: *"PORQUE trampa social (G1): cada quien paga porque supone que los demás pagan"* | **Sí, bajo otro nombre.** Este glosario tierea *"la mordida es inherente a lo mexicano"* como **Mito (Fuerte)** (a)+(c), con base en el **equilibrio de Bardhan** y el contraste Uruguay/Chile; `tramite.yaml` cita `ENCIG2023` + `Rothstein_trampa_social`. El dato mexicano **(a)** y el marco **(c)** existen | **La entrada positiva.** Hoy el constructo solo vive como **refutación de un mito**, no como mecanismo con tier propio. Las dos reglas `[FUERTE]` de §3.3 —**dominio prioritario del Hito D**— se apoyan en un nombre que este glosario no define |
| **Bandwidth tax** ⚠️ **PEOR QUE «SIN TIER»: TIENE VEREDICTO, Y ES DESFAVORABLE** | `§3.6` lo citaba como `PORQUE`. **Retirado del motor en v2.4** | El fenómeno adyacente sí está tierizado: *"horizonte de planeación corto"* **Fuerte (como adaptación)** (a), ENIF 2024 | **v5.4 — corrección al propio §16.** La v5.3 lo registró como *"sin tier leído"*. **El barrido de propagación forense (P-01) encontró que sí tenía veredicto:** el forense V5 lo declaró *"marco teórico **IMPORTADO**"* **(c)** y la regla *"**MATIZADA y parcialmente REFUTADA como motor primario**"*, porque la **ENIF muestra 38.4% de aversión declarada al endeudamiento** — dato mexicano que contradice un cortoplacismo cultural. Archivado desde la Ronda 4, nunca bajó al motor. **Y toca G3, el único generador PROBADO.** Sobrevive la conducta; no el mecanismo cognitivo |
| **Interruptor formal/informal** *(nuevo en v5.6, FP-293/T05, ADR-32.c)* | `§3` L543, regla `[MEDIA]`: *"SI la cita es formal-laboral con checador/sanción/dinero ENTONCES puntual (5-10 min antes); SI es social-familiar sin sanción ENTONCES hora aproximada, 'ahorita' — PORQUE el interruptor formal/informal"* · **id:** `tiempo.puntualidad.formal_vs_social` | El fenómeno adyacente (puntualidad diferencial formal/social) sí aparece en la ficha de tiempo del programa, sin cita a un tier de report específico verificada aquí | **La entrada positiva.** El "interruptor" (qué activa el modo formal vs. el social) es un nombre de mecanismo, no un dato leído — ningún report de `corpus/reports/` lo tieriza hoy con mapa de evidencia propio |
| **Turnout buying** / **vote-choice buying** *(nuevo en v5.6, FP-293/T05, ADR-32.c)* | `§3` L555, regla `[MEDIA]` **(a)**: *"SI hay dádiva o transferencia Y el partido puede monitorear al broker (no al votante) ENTONCES compra ASISTENCIA a las urnas de simpatizantes, no la elección de voto — PORQUE turnout buying ≠ vote-choice buying"* · **id:** `civico.clientelismo.turnout_no_vote_choice` | Sí trazable a la fuente citada en el propio `PORQUE`: Larreguy, Montiel Olea y Querubín 2017 (AJPS) — la eficacia del SNTE viene del apego partidista, no de la dádiva; distinción ya con RCT y contrafactual 2018 (sube a `[FUERTE]` en el motor, v2 del propio §3) | **La entrada positiva en este glosario.** El motor ya distingue las dos conductas y las cita con fuente — lo que falta es que "turnout buying"/"vote-choice buying" tengan definición propia aquí, no solo en el `PORQUE` del motor |
| **Confianza personalizada** *(nuevo en v5.6, FP-293/T05, ADR-32.c)* | `§3` L565, regla `[FUERTE]`: *"SI conoce personalmente a la organizadora/miembros ENTONCES entra a la tanda; SI es tanda de desconocidos ENTONCES alto riesgo de fraude, evita — PORQUE confianza personalizada como sustituto de enforcement"* · **id:** `cooperacion.tanda.conoce_organizadora` | Adyacente a **Trampa social** (fila de arriba, mismo §16): ambos nombran un mecanismo de confianza/enforcement sin tier propio leído de un report | **La entrada positiva.** "Confianza personalizada" describe el mecanismo que sustituye enforcement institucional en la tanda, pero ningún report tieriza el constructo en sí (solo la conducta observable, "entra"/"evita") |
| **Default es aceptación** *(nuevo en v5.6, FP-293/T05, ADR-32.c)* | `§3` L575, regla `[FUERTE]`: *"SI la vacuna/servicio está disponible y la campaña llega ENTONCES la mayoría acepta — PORQUE el default es aceptación y el hueco es logístico (no actitudinal)"* · **id:** `salud.vacunacion.disponible` ⚠️ *id con dominio equivocado en `procedencia.yaml` (`salud.*` en un id de §3.9), no corregido aquí — ver `forense/hallazgos.md`* | El hueco logístico-no-actitudinal es la distinción que la regla exige, sin tier propio de report leído | **La entrada positiva.** "Default es aceptación" es un mecanismo de economía conductual (sesgo de default) aplicado a vacunación, sin report que lo tierize como constructo con mapa de evidencia propio |

**Consecuencia operativa, que viaja hasta la ficha y hasta cualquier corrida vertical:**

1. Las dos reglas `[FUERTE]` de `§3.3` **conservan su tier** —lo sostienen ENCIG 2023 y el contraste internacional—, pero **el nombre de su mecanismo no tiene entrada propia**. Al pre-registrar su falsador en el Hito D, escribirlo contra **el dato** (*¿baja la mordida al digitalizar y hacer registrable al funcionario?*), **no contra la etiqueta "trampa social"**, que no es falsable porque aquí no está definida.
2. `§3.6` **no puede citar "bandwidth tax" como driver con respaldo**. Su tier `[MEDIA]` se sostiene por la conducta observada, no por el mecanismo cognitivo. **Marcar (c) donde se use.**

**Requisito de salida:** este apartado se vacía de dos maneras legítimas —leer un tier de un report que sí los trate, o reescribir el `PORQUE` del motor para que nombre un constructo que sí existe aquí—. **Nunca escribiéndoles un tier a criterio.**

---

## Provenance

Leídos en esta sesión: mapas de evidencia de `Ausencia_sin_certeza`, `Elegir__Cortejar_y_Amar`, `Psicología_de_la_Juventud`, `Vejez_y_Cuidado`, `Religiosidad`, `Adopción_y_Resistencia_Tecnológica`, `Psychology_of_Mexico-US_Migration`; hallazgos y caveats de `Humor` y `Mérito`; **lectura completa de los cuatro pivotes** (`La_arquitectura_invisible`, `Psicología_del_Consumidor`, `Psicología__Conducta_y_Sociedad`, `Moral_Emotions_in_Mexico`); `prompts-verticales-validacion` contra `modelo §1/§2/§3`; `verificacion-red-team-vs-corpus`; `red-team-cuatro-verticales` §7-§9; registro de apuestas; prueba de falsación; `procedencia.yaml`; `refutations.yaml`; ADR-26 a 29.

**Añadido en v5.1 (28/jul/2026):** ADR-30 y ADR-31; `modelo` §1.1, §1.3, §2.2, §3, §6, §7; la ficha canónica *(eliminada, ADR-36.b)* regenerada; `gobernanza` v1.1 §2, §4, §5.1; `tramite.yaml`; verificación por `grep` contra los tres reports dueños de las correcciones de retropropagación. **Los conteos de §13 se recomputaron leyendo el modelo, no copiando la v5.**

Tiers de v2/v3/v4 conservados **con su contenido traído íntegro a este documento**, con origen marcado. **Este glosario no remite a ninguna versión anterior: las tres son borrables.**

---

## Módulo de auditoría de rigor extremo

**¿Qué parte podría confundir pobreza, desigualdad o informalidad con "cultura"?** El riesgo mayor entra por los dominios nuevos. **Vejez** es el caso claro: *"aquí a los viejos se les cuida"* describe una corresidencia que es en buena parte **pooling económico de vivienda e ingreso** ante pensión contributiva escasa. El report lo marca; el glosario debe mantenerlo marcado o el constructo se leerá como amor filial. Lo mismo con **adultez aplazada**, que es global y coincide con vivienda inalcanzable.

**¿Qué parte sobregeneraliza desde clases medias urbanas?** Los tres constructos de pareja con psicometría vienen de **muestras universitarias**. Puntualidad situada viene de **muestra urbana escolarizada**. Adultez aplazada es *"más fuerte en jóvenes urbanos de clase media escolarizados"* por texto del propio report. Y foundational admite que la autopercepción de dignidad se concentra en *"poblaciones urbanas y educadas"*. Buena parte de lo que el corpus llama "el mexicano moderno" es **el polo educado de una distribución segmentada**.

**¿Qué parte está sesgada por marcos o muestras extranjeras?** Los cuatro pivotes descansan en Hofstede, GLOBE, Leung-Cohen, Benedict, Ting-Toomey y Goffman; **solo moral emotions los critica antes de usarlos** — los otros tres los aplican. Y cuatro constructos siguen marcados **(b)**: simpatía, machismo/caballerismo, marianismo y parte de familismo. Marianismo reaparece ahora por la puerta de pareja: es la tercera vez que entra a un dominio distinto arrastrando su marca.

**¿Qué hallazgos cambiarían si el foco fuera México rural, indígena o popular?** El *"híbrido"* de foundational se volvería la posición correcta y no la superada: si los elementos de honor persisten *"particularmente en comunidades rurales y tradicionales"*, retirar la etiqueta para todo México puede ser sobre-corrección urbana. **Es un argumento real contra el parche que apliqué hoy**, y por eso foundational sigue intacto. Además, religiosidad y vejez —dos de los ocho dominios recién incorporados— pesan mucho más en el México popular y rural: que hayan estado ausentes hasta ahora **no es casualidad**, es el sesgo de clase del corpus operando sobre qué reports lograron aportar constructos.

**¿Qué parece psicológico pero es un incentivo racional?** Adultez aplazada, de manual. También: no denunciar (0.8% de resolución), farmacia con consultorio (costo, tiempo, trato), horizonte corto (volatilidad del ingreso), corresidencia en la vejez (pooling), y la desconfianza en el proveedor del seguro agrícola (fraude documentado de ANAGSA). En todos, leerlo como rasgo sería el error paradigmático del programa.

**¿Dónde hay evidencia débil pero intuición social fuerte?** En tres lugares. **(1)** Mantener el maestro en Media: lo confirmo por lectura del red team y del Hito 2, pero sin haber releído las cuatro verticales completas. **(2)** Declarar la UAI "falsada" por un solo par de países: es argumento fuerte, no prueba — Israel podría ser atípico por razones que ningún report examina; por eso *retiré la afirmación causal* en vez de afirmar la inversa. **(3)** Los tiers `DERIVADO`: son cinco reports y el juicio es mío.

**¿Qué conclusiones serían peligrosas si alguien las usara de forma simplista?** Tres. **(1)** Leer `DERIVADO` como "tier inventado, ignorar": `Mérito` y `Humor` tienen caveats más rigurosos que varios reports con mapa formal. **(2)** Re-tierar el corpus hacia abajo: de trece tiers revisados en los pivotes, **nueve quedaron sin cambio** — la verificación ya advirtió que los reports están bien tierados por dentro y que el problema vivía en la síntesis. **(3)** Usar cualquier cifra de confianza interpersonal como si estuviera establecida: hay cinco números y dos se contradicen sobre la misma encuesta.
