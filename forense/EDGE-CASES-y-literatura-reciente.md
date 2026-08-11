> **NOTA DE RECUPERACIÓN · 11/ago/2026.** Este documento existía solo en el espejo del proyecto; el encargo del motor adaptativo lo citó y la Ronda 1 lo clasificó NO-ENCONTRADO en repo (universo: árbol + git log --all). Entra verbatim desde el espejo — procedencia tipo (2), sin sello de commit de origen. sha256 del original en espejo: 89b0558583189c1e58a521cddc35c145ab27763d01e24ccb96be107e8b5e0baf. Resolución M0 de mesa, 11/ago/2026. Su contenido NO se edita.

# EDGE CASES Y LITERATURA RECIENTE · Estrés del paquete de remediación antes del encargo

### Consultoría (Conversación Mejoras 4) · 5/ago/2026 · contra `origin/main` = `a7f807e` · Complemento del CAREO (Partes I-III). TIPO (3) en lo bibliográfico: paráfrasis de búsqueda web, verificable por autor-año-DOI; nada citado verbatim.

**Método.** Cada ítem del paquete (AR-1…AR-5, EJ-1…EJ-7) se estresa por dos lados: (a) **bordes del programa** — condiciones reales del repo donde el método publicado no aplica limpio, derivadas de los archivos; (b) **crítica publicada** — la literatura que ataca al método mismo, priorizando 2019-2026. Cierra con el cambio que impone, si alguno. Un ítem sin cambio también se reporta: estrés que no rompe es certificación.

---

## E1 · E-value (AR-1(ii), R1-Rec-2) — sobrevive DEGRADADO a "una opción entre varias, nunca automática"

**Crítica publicada.** El E-value tiene un debate entero en Annals of Internal Medicine: Ioannidis, Tan & Blum (2019) documentan que hereda todos los problemas del estimador y su IC (reporte selectivo, dependencia del contraste de exposición elegido y del nivel de confianza), que su automatización invita a no pensar seriamente en la confusión, y que otros sesgos distintos de confusión quedan intactos; además la forma que entró a la práctica mira solo confusión que aleja del nulo, ignorando la que acerca. VanderWeele-Mathur-Ding respondieron corrigiendo malinterpretaciones, y Sjölander-Greenland muestran que con múltiples confusores no medidos el E-value puede ser a la vez demasiado optimista y demasiado pesimista según el escenario.

**Bordes del programa.** (i) El E-value canónico está definido sobre razón de riesgos; los β̂ del programa viven en **diferencia de proporciones** — usarlo exige conversión aproximada (prevalencia del desenlace de por medio) que hay que declarar. (ii) El uso que R1 le da —cuantificar una **reversión de signo**, no una asociación— es no estándar: el E-value mide qué fuerza de confusor explicaría *la asociación observada*, no *el cambio marginal→condicional*. (iii) En celdas con n~30-300, el E-value del IC será enorme por pura imprecisión y no informará nada.

**Cambio impuesto.** AR-1(ii) conserva "análisis de sensibilidad" como requisito pero deja de nombrar al E-value como *el* instrumento: pasa a "sensibilidad a confusión no medida con método declarado y su crítica citada (E-value con conversión declarada a escala RD, o análisis de sesgo cuantitativo con parámetros explícitos)". Prohibido reportarlo solo, sin la discusión de confusores concretos que Ioannidis et al. exigen.

## E2 · X2-CONT / splines bajo diseño complejo (EJ-2) — la Fase 1 gana tres candados; la Fase 2 gana penalización

**Bordes del programa, derivados de las tablas de X.** (i) **W2 no admite splines: θ tiene 4 niveles.** La receta RCS de R1 aplica a W1 (0-10); para W2 "no dicotomizar" = tratar los 4 niveles como categorías saturadas — que es exactamente lo que la Fase 1 ya hace. Ningún cambio, pero hay que decirlo para que nadie pida splines sobre 4 puntos. (ii) **Heaping en θ=5:** la tabla de X §5.1 muestra n=3,669 en el nivel 5 contra 265-795 en los niveles vecinos — preferencia de dígito clásica de escalas 0-10. Cualquier curva por nivel, y cualquier spline con nodo cerca de 5, hereda esa acumulación; el agrupamiento de R1-Rec-5 (≤3 / 4-5 / ≥6) la absorbe parcialmente y por eso se adopta como especificación de Fase 1 para W1, con el heaping declarado en la spec. (iii) **Sesgo de datos escasos:** Greenland-Mansournia-Altman (BMJ 2016) — estratificar fino infla estimadores hasta valores absurdos incluso en datasets grandes, y el remedio es penalización (Firth, priors logF). El cruce nivel×estrato de W1 (hasta 11×4 celdas) entra de lleno; el umbral n≥30 del programa mitiga pero no inmuniza (el sesgo es de conteos de *eventos*, no de filas: con tasas ~12%, una celda de n=30 tiene ~4 eventos). (iv) **Multiplicidad:** 39 celdas, 12 significativas, cero control de comparaciones múltiples — se declara como límite de lectura, no se "corrige" post-hoc.

**Cambio impuesto.** Spec de Fase 1: niveles agrupados en W1, saturado en W2, n mínimo por evento (no solo por fila) reportado por celda, heaping declarado. Fase 2 (post cruce-contra-R): RCS solo en W1, con penalización tipo Firth/logF evaluada si hay separación o celdas con <5 eventos, y la advertencia de multiplicidad en la cabecera.

## E3 · ACOTADO / Manski (AR-5) — sobrevive con dos candados y un piloto obligatorio

**Crítica y bordes.** R3 ya trae los tres clásicos (confusión de los tres objetos; Imbens-Manski-Stoye; Ley de Manski). Los bordes que R3 roza y el programa sufre de lleno: (i) **dependencia entre los 15 β** — los generadores comparten θs, instrumentos y desenlaces (la `marca_c2` de procedencia ya documenta dos entradas no independientes); propagar 15 intervalos como independientes con cotas de Fréchet produce el peor caso estructuralmente, y el programa no conoce la dependencia; (ii) **cotas bajo diseño muestral** — la literatura de bounds asume iid en su mayoría; con ponderadores/conglomerados los IC de las cotas exigen el mismo tratamiento svystat que todo lo demás; (iii) **el motor necesita ejecutar**: milpa consume números; una p-box exige motor de propagación que hoy no existe — costo real, no de papel.

**Cambio impuesto.** ACOTADO entra a AR-5 con: la regla de los tres objetos verbatim de R3, la declaración de dependencia (o Fréchet explícito como peor caso rotulado), y un **piloto sobre UN coeficiente** (candidato natural: uno de los 9 SIN-RUTA con cota de peor caso barata) antes de comprometer los 15 — si la cota del piloto incluye cero con holgura absurda, el benchmark de salida de R3 se activa temprano y se ahorra el resto.

## E4 · CALIBRADO / history matching (AR-5) — sobrevive, y el edge case más citado es un REGALO para el programa

**Crítica publicada.** La condición de Aquiles es la **discrepancia del modelo**: Brynjarsdóttir-O'Hagan (ya en R2) muestran la no-identificabilidad θ-vs-discrepancia, y la guía práctica de history matching (Challenor; el handbook de hmer; Andrianakis et al.) advierte que una discrepancia declarada demasiado pequeña vacía la NROY por la razón equivocada. Pero el hallazgo central de esa misma literatura es el que importa: **si el simulador y los datos son incompatibles, la NROY se va a cero — y la calibración clásica lo esconde** (siempre entrega el punto "más cercano", aunque esté lejísimos, con incertidumbre decreciente). En ABM aplicado (tutoriales de UQ para ABM; Covasim) el flujo por olas con emulador es práctica establecida.

**Borde del programa que es oportunidad.** NROY=∅ es un **estado de falsación del motor completo** — la versión agregada de lo que el Hito D hace regla por regla. Si mesa adopta CALIBRADO, el programa gana gratis un falsador que hoy no tiene: "no existe ningún vector de 15 β compatible con los momentos observados" es un veredicto archivable, con la misma dignidad que un D. El costo real sigue siendo el vacío ya declarado (presupuesto de corridas de milpa, sin estimar) más la especificación honesta de discrepancia y error de observación — y para esto último R2-Rec-2 ya dio la pieza: los errores estándar de diseño de svystat son la varianza de observación natural.

**Cambio impuesto.** CALIBRADO entra a AR-5 con tres declaraciones obligatorias en su ficha: discrepancia del modelo (con el método de perturbación del handbook como receta), error de observación (= SE de diseño de los momentos objetivo), y **NROY=∅ pre-registrado como desenlace de falsación del motor**, no como fracaso del método.

## E5 · Invariancia de medición (EJ-7, V4) — mi cláusula de la Parte III estaba DESACTUALIZADA; se corrige

**Crítica publicada, y es un debate abierto en las dos direcciones.** Robitzsch & Lüdtke (Structural Equation Modeling, 2023): la invariancia total, parcial o aproximada **no es prerrequisito** para comparaciones válidas entre grupos — hay ambigüedad inevitable en cómo definir la comparación bajo violación, no hay base para preferir invariancia parcial sobre alignment, linking robusto o invariancia bayesiana aproximada, y hasta un modelo deliberadamente mal especificado con parámetros invariantes puede justificarse. Raykov (2024) responde por el otro flanco: la invariancia tampoco es **suficiente** para comparaciones significativas. Y Kusano-Napier-Jost (PSPB 2025) argumentan que el estándar de invariancia es frecuentemente inapropiado en investigación comparativa. El campo está en disputa activa: exigir "evidencia de invariancia" como compuerta, que es lo que mi V4 hacía, adopta un bando de la disputa como si fuera la norma.

**Borde del programa.** El caso del programa ni siquiera es el de la disputa (mismos ítems, grupos distintos): es **ítems distintos, instrumentos distintos, misma θ pretendida** — armonización ex-post pura, donde ni la MGCFA clásica ni el alignment aplican sin ítems ancla o respondientes comunes, que no existen entre ENCUCI y ENCIG.

**Cambio impuesto — y es corrección a mi propia Parte III.** La cláusula V4 se reescribe: el default **constructo-por-instrumento se mantiene** (esquiva la disputa entera y ya es la práctica de `procedencia.yaml`); pero la compuerta deja de ser "evidencia de invariancia o rótulo" y pasa a "**todo pooling entre instrumentos exige un argumento de vinculación declarado** (anclas, alignment, linking robusto, o juicio experto rotulado como tal), citando que la exigibilidad de la invariancia clásica está en disputa (Robitzsch-Lüdtke 2023 vs. Raykov 2024)". Menos exigente en la forma, más honesto con el estado del arte, e igual de protector: lo que se prohíbe es el pooling *silencioso*, no el pooling.

## E6 · Transportabilidad / nodo-S (D-A) — sobrevive con una línea de alcance

**Borde.** Los resultados de completitud de Bareinboim-Pearl son para efectos **causales** con DAGs; los β̂ del programa son asociaciones. La cláusula nodo-S-en-prosa sigue siendo válida y barata, pero lo que declara es invariancia de **distribuciones condicionales** entre población fuente y población de agentes — no de mecanismos causales. Una línea en D-A lo fija para que nadie lea la cláusula como licencia causal: "la invariancia declarada es distribucional salvo que el coeficiente esté en el nivel (i) de la casilla".

## E7 · Colapsabilidad y convexidad (EJ-1, taxonomía) — sobrevive con el matiz de pesos escrito

**Borde.** La regla de convexidad de RT-D ("modificación de efecto sola no invierte el marginal") usa como pesos la composición poblacional; bajo diseño complejo esos pesos son los de expansión, y si el diseño es informativo la RD marginal ponderada puede diferir del promedio ingenuo de celdas sin que nada esté "mal". Ya estaba anotado en la Parte I como quinta puerta (composición/ponderación); el cambio es solo de redacción en EJ-1: la regla de convexidad se escribe "bajo no-confusión **y con los pesos de diseño como composición**".

## E8 · Bordes transversales que ningún método individual cubre — dos, y uno exige decisión

- **¿Qué hace milpa con PENDIENTE?** La hoja D-ABC (con la marca de la maestra 20 que acepté) deja `radio_confianza` en PENDIENTE. Si el motor necesita un número para correr, PENDIENTE colapsa silenciosamente en el ASIGNADO previo — el supuesto disfrazado de parámetro que el propio fuente denunció. **El ADR de D-ABC debe declarar el manejo:** el coeficiente PENDIENTE corre como ASIGNADO-con-rótulo-visible, o como ACOTADO de peor caso, o el generador se excluye del output con nota — cualquiera de las tres, pero escrita. Es la versión de casilla del defecto de B-bis ("escala sin fila para el desenlace que ocurrió").
- **θ no manipulable, ahora con consecuencia operativa:** ya estaba en AR-3 como declaración; el borde es que TODA la maquinaria causal del paquete (disyuntiva, E-value, transporte causal) presupone contraste de exposición bien definido. Para θs psicosociales el techo del programa es el nivel (ii) de la casilla salvo diseño intra-persona (ID-G3 es la excepción precisamente porque el cambio temporal intra-sujeto define el contraste). Una línea en D-A lo cierra: "para exposiciones no manipulables, el nivel (i) exige diseño que defina el contraste (intra-persona u otro); no hay ruta (i) transversal".

---

## Tabla de cierre — qué cambió en el paquete por esta revisión

| Ítem | Veredicto del estrés | Cambio |
|---|---|---|
| AR-1(ii) E-value | degradado | "método de sensibilidad declarado + crítica citada"; E-value nunca solo ni automático; conversión RD declarada |
| EJ-2 X2-CONT | reforzado | Fase 1: agrupado W1 / saturado W2 / eventos-por-celda / heaping θ=5 declarado; Fase 2: penalización Firth-logF si escasez; multiplicidad declarada |
| AR-5 ACOTADO | condicionado | tres objetos verbatim + dependencia/Fréchet explícito + piloto de 1 coeficiente antes de 15 |
| AR-5 CALIBRADO | reforzado + regalo | discrepancia y error de observación declarados; **NROY=∅ pre-registrado como falsador del motor** |
| EJ-7 invariancia | **corregido** (mi V4 estaba desactualizada) | pooling entre instrumentos exige argumento de vinculación declarado; la exigencia de MI clásica se cita como disputa, no como norma |
| D-A nodo-S | intacto + 1 línea | invariancia declarada es distribucional, no causal, salvo nivel (i) |
| EJ-1 convexidad | intacto + 1 línea | pesos de diseño como composición |
| D-ABC | **decisión nueva requerida** | manejo explícito de PENDIENTE en el motor (3 opciones, una escrita) |
| D-A no-manipulable | intacto + 1 línea | sin ruta (i) transversal para θ psicosocial; ID-G3 como excepción por diseño |

Nada del paquete cayó; dos piezas se degradaron con honra (E-value, mi cláusula de invariancia), una ganó un falsador nuevo para el motor (NROY=∅), y apareció una decisión que ningún documento del episodio había visto (el manejo de PENDIENTE). El paquete queda listo para el encargo a Opus.
