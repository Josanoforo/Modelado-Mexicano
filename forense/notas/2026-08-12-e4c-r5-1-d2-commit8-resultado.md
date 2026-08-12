# E4c · R5.1-D2 — Commit 8: resultado — veredicto PROPUESTO: fila A (refutación)

**No edita Commit 7 ni ningún commit anterior.** Primer resultado que produce el procedimiento congelado en Commit 7 — se reporta, conforme a Commit 7 §5. Mesa adjudica en acto propio; este acto no escribe en el bloque append-only de `hitoD-preregistro-v2_0.md` ni en las columnas `estado`/`veredicto` de `forense/registro-llaves-identificacion-v1_0.md` (perímetro de este acto: solo `escala_del_veredicto`, ya tocada en Paso 3 §0.2).

## 1 · Universo — verificado antes de leer el resultado como válido

| | 2018 | 2022 |
|---|---|---|
| Personas 65+ clasificables (≥1 fila en `ingresos`) | 20,751 | 28,626 |
| Excluidas (65+, 0 filas en `ingresos`) | 1,834 | 1,348 |
| Tratamiento (T) | 6,160 | 8,877 (deflactado) / 8,922 (nominal) |
| Comparación (C) | 14,591 | 19,749 (deflactado) / 19,704 (nominal) |
| Fracción T del universo clasificable | 29.7% | 31.0% |

**Sin fila D.** Ninguna celda cae bajo el umbral arbitrario de 5% de §6 (la más chica, T-2018, es 29.7% del universo esa ola) — no hay archivo por tamaño de muestra insuficiente. Identificación de §2 (clave `P032`) exitosa por el criterio ya declarado en Commit 1 §2.1 (inferencia por exclusión, no etiqueta literal "contributivo" en el catálogo — mismo estatus epistémico declarado entonces, no mejorado ni degradado aquí).

**A-bis regla 4 (universo):** el DiD reportado abajo es sobre el universo con ≥1 fila en `ingresos` — 1,834 (2018) y 1,348 (2022) personas 65+ quedan fuera por no tener ninguna fila, y no se les imputa. No se estratificó por ningún eje en esta corrida (ver §5).

## 2 · Resultado — DiD principal, ambos desenlaces, sensibilidad (a)/(b)

| Desenlace | Umbral 2022 | DiD (θ̂) | SE | IC95% | `n_estratos_singleton` (pre/post) |
|---|---|---|---|---|---|
| Transferencia (P040, persona) | (b) deflactado | **+2.32pp** | 0.91pp | (0.54pp, 4.10pp) | 0 / 0 |
| Transferencia (P040, persona) | (a) nominal | +2.32pp | 0.91pp | (0.54pp, 4.10pp) | 0 / 0 |
| Corresidencia (`clase_hog`, hogar) | (b) deflactado | **−0.81pp** | 1.53pp | (−3.82pp, 2.19pp) | 0 / 0 |
| Corresidencia (`clase_hog`, hogar) | (a) nominal | −0.74pp | 1.53pp | (−3.74pp, 2.26pp) | 0 / 0 |

**Sensibilidad (a) vs (b), comprometida en Commit 4 §1: la elección de umbral no mueve el resultado** — diferencia máxima entre variantes, 0.07pp, muy por debajo del ruido de estimación (SE~1-1.5pp). Las 45 personas que cambian de grupo (Commit 3) no alcanzan a mover ninguna conclusión.

**Escala (dirección predicha por sustitución = convergencia del grupo T hacia el grupo C, §6 del pre-registro, citado literal):**

- **Transferencia:** `d_pre=−16.28pp → d_post=−13.96pp` — la brecha se **achica** (converge) 2.32pp. Dirección predicha, magnitud <10pp, decisivo (IC95% excluye tanto 0 como 10pp por completo).
- **Corresidencia:** `d_pre=−2.92pp → d_post=−3.73pp` — la brecha **crece** (diverge) 0.81pp — **signo contrario al predicho por sustitución**. Magnitud <10pp con holgura amplia (todo el IC95% queda muy por debajo de 10pp en valor absoluto), aunque no distinguible de cero.

**Ambos desenlaces satisfacen la fila A por separado** — transferencia por la cláusula "DiD<10pp en la dirección predicha", corresidencia por la cláusula "o de signo contrario al predicho por sustitución". No hace falta que ambos cumplan la misma cláusula; §6 solo exige "al menos uno de los dos desenlaces", y aquí se cumple en los dos, cada uno por su propia vía.

## 3 · DDD (robustez declarada, no adjudica — Commit 7 §2)

| Desenlace | Umbral | θ̂ | SE | IC95% |
|---|---|---|---|---|
| Transferencia | (b) | +3.49pp | 1.25pp | (1.04pp, 5.95pp) |
| Corresidencia | (b) | +0.07pp | 2.54pp | (−4.90pp, 5.04pp) |

**Confirma, no contradice, al DiD principal.** Transferencia: misma dirección (convergencia), magnitud algo mayor pero igual <10pp, igual decisivo (IC excluye cero y 10pp). Corresidencia: prácticamente nulo, igual que el DiD principal, IC más ancho (como predecía el MDE de Commit 7 §2, 1.72× menos preciso) pero sin cambiar la conclusión cualitativa. **Regla de precedencia a nivel hogar, declarada ahora, no resuelta en commits 1-7:** un hogar puede tener a la vez una persona 65+ clasificada y una 55-64 clasificada — la banda principal (T/C) gana sobre la de control (T2/C2) si el hogar tiene ambas, porque un hogar con miembro 65+ ya pertenece al universo principal del diseño, sin importar si además tiene un miembro 55-64. Bajo esta regla: hogares T2/C2 puros (sin ningún miembro 65+ clasificado) = 2,453/10,406 (2018), 3,279/13,229 (2022) — no degenerados.

## 4 · Monto documentado como suficiente

Criterio heredado de la corrida previa (`2026-08-04-hitoD-r5-1-pension-bienestar.md` §6: monto / gasto per cápita del hogar tratado en la ola post) — **aproximado aquí con ingreso per cápita del hogar, no gasto** (no se abrió tabla de gastos, fuera de lo que este acto tenía preparado; declarado como limitación, no oculto):

- De las 8,877 personas tratadas (2022, deflactado), **73.2% reporta recibir efectivamente `P104`** (Programa para el Bienestar de las Personas Adultas Mayores) — la eligibilidad de §2 no se traduce 1:1 en recepción observada; 26.8% son elegibles por regla pero no reciben (no-uso, no verificado por qué).
- Monto medio mensual entre quienes reciben: **$1,705/mes**.
- Ingreso per cápita mensual del hogar (hogares con ≥1 tratado): media $8,516, mediana $5,852.
- **P104 mensual / ingreso per cápita mensual: 20.0% (sobre la media), 29.1% (sobre la mediana).** No trivial frente al presupuesto del hogar — se declara **suficiente** bajo este proxy.

## 5 · A-bis regla 1 · identificación, no solo co-observación

La vía de `gobernanza:623` que sostiene este diseño es la **(ii)**: "experimento natural con grupo de comparación sobre encuestas repetidas". El supuesto que la sostiene, escrito: **tendencias paralelas entre el grupo tratamiento y comparación en ausencia de la reforma** — sin el cambio de regla de 2019, no hay razón para esperar que la brecha (T−C) de transferencia o corresidencia se hubiera movido de forma distinta entre 2018 y 2022 para los dos grupos, ya que ambos comparten edad (65+), la misma encuesta, y solo difieren en su nivel de pensión contributiva. **No verificado con un placebo real en este acto** (Commit 4 §4.3 declaró factible un placebo 2014→2018; no se corrió aquí — reserva, no ejecutado, ver §7). Un DiD sin este supuesto escrito es una asociación con más pasos; aquí queda escrito, no verificado empíricamente con datos pre-tratamiento.

## 6 · A-bis regla 2 · condicionado no reemplaza al marginal

No se estratificó por ningún eje en esta corrida (los dos ejes declarados en Commit 1 §2.7 — ámbito urbano/rural, sexo — no se ejecutaron; **reserva declarada, no un hallazgo**: si un futuro acto estratifica y encuentra un resultado discordante, eso establece que el marginal no es robusto a ese eje, no que el estratificado sea "el verdadero" — la regla se cita para que quede escrita antes de que exista la tentación de usarla al revés).

## 7 · Enganche entre desenlaces (Commit 4 §6) — verificado, no aplica

El patrón que ameritaría la lectura "confundido por composición del hogar" es que **ambos** desenlaces se movieran en la dirección de convergencia a la vez (corresidencia sube lo bastante como para que menos tratados aparezcan recibiendo transferencia registrada). Aquí no ocurre: transferencia converge (+2.32pp), corresidencia diverge levemente y sin significancia (−0.81pp) — direcciones distintas, no el patrón que activaría la reserva. Se declara verificado, no se aplica la lectura de confusión.

## 8 · La contraparte de A-bis — ¿algún punto satisface un umbral sin que el IC lo despeje?

No, en el sentido que bloquea adjudicar: el umbral relevante para la fila A es **<10pp en valor absoluto**, y en los cuatro resultados de §2 (2 desenlaces × 2 sensibilidades) el **IC95% completo** queda muy por debajo de 10pp en valor absoluto — no hay ambigüedad sobre si el punto cruza esa frontera. (La falta de significancia de corresidencia frente a **cero** es una pregunta distinta de si cruza **10pp**; para la fila A solo importa la segunda.)

## 9 · Veredicto PROPUESTO: fila A — la regla se refuta a este nivel de identificación

**Por el orden de precedencia sellado (A → E → B → C → D, §9 del pre-registro tras Paso 3 §0.1):** A se evalúa primero y se satisface — DiD<10pp (transferencia) o de signo contrario (corresidencia), identificación de §2 exitosa, monto documentado como suficiente. No se llega a evaluar E, B, C ni D.

**Vocabulario del registro de llaves (Commit 6 §2): `EJERCIDA_REFUTA`.**

### Por qué este resultado difiere de tres estimaciones publicadas — exigido por Commit 4 §7, no se anota el número sin más

La literatura citada en Commit 4 (86% Ciudad de México, Juárez 2009; 37% rural, este paper; ~30% Sudáfrica, Jensen 2004) mide crowding out bajo un diseño **estructuralmente distinto** en un punto que importa:

1. **El disparador de elegibilidad es geográfico/etario, no de ingreso.** Los tres estudios comparan personas que cruzan un corte de **edad** (70 años) en localidades **ya cubiertas** por el programa contra personas en localidades no cubiertas — un evento simple, visible, fácil de que la familia lo note. Aquí el disparador es un **cambio de regla sobre el ingreso por pensión contributiva** de la propia persona — mucho menos visible, y no coincide con ningún evento observable para la familia (nadie "cumple años" el día que deja de aplicar la prueba de ingreso).
2. **La población tratada aquí no es la misma clase de población.** Los tres estudios de referencia miden en poblaciones **sin ninguna pensión previa** (el objetivo original del programa: adultos mayores rurales sin cobertura de seguridad social). El grupo de tratamiento de este diseño son personas con pensión **contributiva superior a $1,092/mes** — ya relativamente mejor cubiertas que la población que motivó esos estudios. La propia brecha pre-tratamiento (`d_pre=−16.28pp` en transferencia: el grupo tratamiento YA recibía 16 puntos porcentuales MENOS transferencia familiar que el grupo comparación, antes de que existiera ningún cambio de regla) es consistente con que esta población tenía, de entrada, menos necesidad de apoyo familiar — y por tanto menos margen para que ese apoyo se retire.
3. **Elegibilidad no es recepción.** Solo 73.2% del grupo tratamiento recibe efectivamente el beneficio (§4) — un 26.8% de dilución hacia el efecto nulo que un diseño de intención-de-tratar (como este) absorbe pero un diseño de recepción efectiva no tendría.

Ninguna de las tres es una refutación de que el fenómeno de sustitución exista en general — son razones por las que **este diseño específico, sobre esta subpoblación específica**, tiene menos margen para detectarlo, incluso si existiera.

## 10 · Contadores — declarado explícito

**Este acto no mueve ningún contador.** `13 de 27`, `9 de 14`, `4 de 144` intactos. **Llaves de identificación ejercidas: sigue en 0 de 2** — este acto propone, no firma. Si mesa firma `EJERCIDA_REFUTA`, la fila de `forense/registro-llaves-identificacion-v1_0.md` se actualiza en un acto de adjudicación propio, fuera del perímetro de este commit.

---

*Commit 8 de este acto (Bloque A-bis/D). No edita Commits 1, 3, 4, 5, 6 ni 7. Primer y único resultado que produce el procedimiento — no se corrige hacia atrás. Veredicto PROPUESTO a mesa: fila A, `EJERCIDA_REFUTA`. Este acto no firma.*
