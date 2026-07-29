# Lectura de los cuatro pivotes · tiers corregidos
### La tarea que la verificación prescribió el 25 de julio y nadie ejecutó

*27 de julio de 2026. Leídos completos: `La_arquitectura_invisible` (4,343 palabras), `Psicología_del_Consumidor` (7,565), `Psicología__Conducta_y_Sociedad` (7,513), `Moral_Emotions_in_Mexico` (4,681).*

La nota de alcance de `verificacion-red-team-vs-corpus.md` decía: *"si vas a rehacer el glosario en firme, el siguiente paso natural es leer completos los ~4 reports pivote —comunicación, consumidor, foundational, moral emotions— para redactar los tiers corregidos palabra por palabra."* Esto es eso.

---

## 1 · El hallazgo que reordena todo: el mismo defecto, tres veces

El parche de Hofstede no era un caso aislado. **Es un patrón, y los tres casos tienen forma idéntica:** una corrección se decidió, viajó al glosario, y nunca volvió al report que la originó. Durante días el corpus sostuvo dos verdades simultáneas, y quien leyera la fuente —como se le pidió a las validaciones forenses— veía la versión sin corregir.

| # | Corrección | Ordenada | Llegó al glosario | Llegó al report |
|---|---|---|---|---|
| 1 | **Hofstede** `Fuerte` → `Media` (correlato, no motor) | Verificación §3.2, 25/jul | ✅ v3 | ❌ → **parchado hoy** |
| 2 | **Etiqueta "honor"** retirada | Meta-auditoría | ✅ v3 | ❌ → **parchado hoy** |
| 3 | **Honor como "híbrido"** en foundational | Superado por meta-auditoría | ✅ v3 | ❌ → **requiere tu decisión** |

**Los tres pivotes tenían tres posiciones distintas sobre honor**, simultáneamente, en el mismo corpus:

- **Comunicación:** México **es** cultura de honor (Cross/Uskul, Castillo 2019). *La más equivocada.*
- **Foundational:** *"La realidad probable es un híbrido"* — honor rural/tradicional + dignidad urbana/educada.
- **Moral emotions:** honor **periférico, no núcleo**; la autopercepción lo contradice; dignidad-face r=+.96, ambas negativas con honor.

La meta-auditoría falló a favor de moral emotions. Comunicación ya está parchado. **Foundational no**, porque "híbrido" es una posición defendible y matizada —no un error— y retirarla es una decisión tuya, no una corrección mía.

---

## 2 · Cinco números para el mismo constructo

La confianza interpersonal es el constructo más citado del corpus. Tiene **cinco magnitudes distintas** repartidas entre artefactos:

| Cifra | Fuente | Dónde |
|---|---|---|
| **12%** | WVS 2012 (caída desde 34% en 1990) | Comunicación |
| **21.8%** | ENCUCI 2020, "la mayoría de las personas" | Comunicación |
| **22%** | Latinobarómetro/ENAFI/LAPOP | Moral emotions |
| **32.1%** | **ENCUCI 2020**, "la mayoría" | Glosario v3 |
| **18%** | Pew 2025 | Glosario v3/v4 |

**Dos de ellas dicen ser la misma encuesta y difieren en 10.3 puntos.** El glosario ya marcaba *"magnitud item-dependiente"*, que es la etiqueta correcta — pero nunca reconcilió la contradicción ENCUCI. Es lo primero que hay que resolver antes de usar cualquier número de confianza en un modelo.

**Tier corregido:** *confianza radial* — **concepto Fuerte** (convergencia de cinco fuentes independientes en la dirección); **magnitud NO ESTABLECIDA** (no "item-dependiente": hay una contradicción abierta sobre la misma encuesta).

---

## 3 · La UAI está falsada por el propio corpus

El report de comunicación construye su tesis sobre tres pilares de Hofstede y afirma: *"La evitación de incertidumbre de 82 **genera** incomodidad con el conflicto abierto."*

Cien líneas después, en la sección de comparación internacional, documenta: **Israel tiene UAI 81 —casi idéntica a México (82)— y es *"la cultura comunicativa más directa del mundo"*.**

Si la UAI generara indirección, Israel sería indirecto. **No lo es.** El mecanismo está falsado por el propio report, que presenta la regla y su contraejemplo sin advertir la contradicción.

Lo que sí discrimina es la **distancia de poder**: México 81, Israel 13 — la mayor brecha de todos los pares comparados en el documento.

**Tier corregido:** *UAI como driver de la indirección* — **RETIRADO** (falsado internamente). *PDI como correlato de la indirección* — **Media** (correlato descriptivo, no causa; ADR-06).

---

## 4 · El corpus tiene su mejor contraevidencia y nunca la usó

El constructo maestro está en **Media** con la acotación de que la convergencia "estructura > psicología" está sobre-declarada. Los dos mejores argumentos para esa acotación **ya estaban escritos en un report** y ningún glosario los recogió:

- **Argentina** — herencia católica latinoamericana, desigualdad significativa, y *"normas comunicativas dramáticamente diferentes"*. Misma estructura, conducta distinta.
- **Israel** — UAI casi idéntica, tensiones sociales severas, y la cultura más directa del mundo.

Son dos cuasi-experimentos naturales contra la reducción de cultura a estructura. Y el report los usa para concluir, textualmente, que *"ambos factores —culturales y estructurales— son operativos y se refuerzan mutuamente"*.

**Esto refuerza el descenso del maestro a Media, pero por una razón distinta a la del v4.** El v4 lo bajó porque el red team mostró que la convergencia estaba *manufacturada por el marco*. Esto lo baja porque hay **contraevidencia empírica directa** dentro del propio corpus. La segunda razón es más fuerte: es falsación, no sospecha de sesgo.

---

## 5 · Moral emotions es el report modelo

Es el único de los cuatro que hace todo lo que las instrucciones piden, y debería ser la plantilla:

- **Critica sus propias tipologías antes de usarlas.** Cuatro objeciones a Benedict, cinco a Leung-Cohen, incluyendo que los ejemplares se estipulan *a priori* y *"en ninguno de estos estudios se ha empleado una medida directa para probar la validez de la postulación"*.
- **Marca la procedencia dentro del mapa de evidencia**, no en una nota al pie: *"muestras específicas —a menudo mexicano-americanos o estudiantes—"*, y por constructo: machismo *"muestra mexicano-americana"*, marianismo *"varios estudios en latinas, muchos en EE.UU."*.
- **Fecha sus fuentes:** PHSC de Díaz-Guerrero, *"base empírica de los 60–90, requiere actualización"*.
- **Separa los cuatro niveles** con narrativa popular incluida.

Y esa última marca choca de frente con comunicación, que usaba el 80% de Díaz-Guerrero de los años 50-60 **en presente**, como fundamento estructural. Ya está parchado con el caveat de vigencia y la nota de que las actualizaciones de Díaz-Loving encuentran el patrón **segmentado** (menor educación, rural), no general.

---

## 6 · Tiers corregidos, palabra por palabra

| Constructo | Tier anterior | **Tier corregido** | Razón (leída, no inferida) |
|---|---|---|---|
| Hofstede IVR 97 / UAI 82 | Fuerte *(en consumidor)* | **Media — correlato** | Falacia ecológica no resuelta por replicación. Parchado en la fuente |
| UAI → indirección | implícito Fuerte | **RETIRADO** | Falsado por Israel (UAI 81, cultura más directa del mundo) |
| PDI → indirección | implícito Fuerte | **Media — correlato** | Es lo que discrimina en el par México/Israel (81 vs. 13) |
| "México cultura de honor" | Narrativa popular *(glosario)* | **Narrativa popular — ahora también en la fuente** | Parchado en comunicación; pendiente en foundational |
| Sensibilidad reputacional | — | **Media** | Castillo 2019, real y medible; se explica como face bajo dignidad |
| Confianza radial — concepto | Fuerte | **Fuerte** | Cinco fuentes convergen en dirección |
| Confianza radial — magnitud | "item-dependiente" | **NO ESTABLECIDA** | Contradicción abierta: 21.8% vs. 32.1% en la misma ENCUCI 2020 |
| Simpatía | Media **(b)** | **Media (b)** — sin cambio | Triandis 1984, Acevedo 2020, US-Latina. Moral emotions ya lo marcaba |
| Marianismo / autosilenciamiento | Media **(b)** | **Media (b)** — marca añadida a la fuente | Nuñez 2016 N=4,426 = HCHS/SOL, cohorte hispana en EE.UU. Parchado |
| Abnegación (PHSC) | — | **Media, con caveat de vigencia y segmentación** | Base 1950-60; Díaz-Loving 2011-17 la halla concentrada en menor educación y rural |
| Estructura vs. cultura | Media | **Media — confirmado, razón más fuerte** | Ya no solo por sesgo de marco: hay contraevidencia empírica (Argentina, Israel) |
| Familismo — efectos duales | Fuerte | **Fuerte** — sin cambio | Cahill 2021 meta-análisis; el obligatorio **no** es protector (Zeiders 2013); relación curvilínea con logro (Fuligni 1999) |
| Dignidad-face r=+.96 | Fuerte | **Fuerte** — sin cambio | Smith 2017. México 2º en dignidad, 5º en honor, 8º en face de nueve muestras |

---

## 7 · Qué queda pendiente y por qué no lo hice

1. **Foundational y su "híbrido" de honor.** Es una posición matizada, no un error; superarla es decisión tuya.
2. **Hofstede como fundamento causal en comunicación.** El párrafo de apertura y la sección de los tres pilares dicen que el perfil *"predice con precisión"* y que la UAI *"genera"* la incomodidad. Corregirlo no es una línea: **toca la tesis del report**. Requiere reescritura, no parche.
3. **Comunicación sigue sin módulo de auditoría.** La verificación lo señaló como el único que carece de él. Añadirlo es escribir sección nueva.
4. **Cifra de desaparecidos desactualizada** en comunicación (114,570) frente al report de ausencia (135,445, CIDH 30/06/2026). Trivial, pero es inconsistencia interna.

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** Al revés en este caso: mi hallazgo §4 es que el corpus **sobre-corrigió hacia estructura** y tenía su propia contraevidencia sin usar. El riesgo de este documento es empujar el péndulo de vuelta demasiado lejos — Argentina e Israel acotan la reducción estructural, no la refutan.

**¿Qué sobregeneraliza desde clases medias urbanas?** Foundational lo dice mejor que yo: la autopercepción de dignidad se concentra en *"poblaciones urbanas y educadas"*, y Díaz-Loving encuentra el patrón tradicional en *"menor educación y rurales"*. Buena parte de lo que el corpus llama "el mexicano moderno" es el polo educado de una distribución segmentada.

**¿Qué está sesgado por marcos o muestras extranjeras?** Los cuatro pivotes descansan en Hofstede, GLOBE, Leung-Cohen, Benedict, Ting-Toomey y Goffman. Moral emotions es el único que los critica antes de usarlos. Los otros tres los aplican.

**¿Qué cambiaría con foco rural, indígena o popular?** El "híbrido" de foundational se volvería la posición correcta y no la superada: si los elementos de honor persisten *"particularmente en comunidades rurales y tradicionales"*, retirar la etiqueta para todo México puede ser sobre-corrección urbana. **Es un argumento real contra mi propio parche**, y por eso dejé foundational sin tocar.

**¿Qué parece defecto de documento y es otra cosa?** Los tres parches del §1 no son descuidos de redacción: son **el mismo defecto de proceso tres veces**. No existía requisito de propagar hacia atrás hasta que ADR-29 lo escribió, y ADR-29 sigue **sin aprobar**. Mientras no se apruebe, el cuarto caso es cuestión de tiempo.

**¿Dónde hay evidencia débil e intuición fuerte?** En el §3. Que la UAI esté "falsada" por un solo par de países es un argumento fuerte pero no es una prueba: Israel podría ser atípico por razones que ninguno de los dos reports examina. Lo correcto es *retirar la afirmación causal*, que es lo que hice, no afirmar la causalidad inversa.

**¿Qué conclusión sería peligrosa mal usada?** Que los pivotes "están mal" y hay que re-tierar todo hacia abajo. La verificación ya advirtió exactamente contra eso: *"no re-tieres los reports hacia abajo — ya están bien tierados por dentro"*. De los trece tiers revisados, **nueve quedaron sin cambio**. Cambiaron cuatro, y de esos, uno subió de precisión en vez de bajar de confianza.
