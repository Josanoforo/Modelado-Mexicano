# Barrido de propagación forense → motor
### `barrido-propagacion-forense` · **v1.0** · 28 de julio de 2026
#### Los 22 veredictos `ROMPE` / `MATIZA` contra `modelo §3.B`

> | | |
> |---|---|
> | **ARCHIVO** | `barrido-propagacion-forense-v1.0.md` |
> | **REEMPLAZA A** | — *(nuevo)* |
> | **VERIFICAS ASÍ** | el marcador dice **6 NO LLEGÓ → aterrizados** |
> | **NOMBRE ESTABLE** | **`barrido-propagacion-forense`** — cítalo así, **nunca por nombre de archivo** |

> ⚠️ **ARTEFACTO FORENSE FECHADO — no se actualiza.** Registra lo hallado el 28/jul/2026. Reescribirlo para que cuadre con el estado posterior sería la racionalización post-hoc que el Bloque C prohíbe.


> **Por qué existe.** El *entregable central* de cada validación forense es, literalmente, **qué reglas del modelo el caso CONFIRMA / MATIZA / ROMPE**. Los cinco forenses producen **22 veredictos de ese tipo**. Nunca se habían barrido contra el motor.
>
> **Qué lo detonó.** `conf.08`: al partir la diagonal de §3.7 para poder falsarla, apareció que el forense V2 había declarado *ROTO PARCIALMENTE* el supuesto *"sin broker"* desde la Ronda 4 — escrito, fechado, archivado — y **nunca bajó al motor**. La pregunta obvia: ¿cuántos más?
>
> **Por qué ninguna auditoría anterior lo vio.** Las auditorías de este programa han sido **estructurales**: archivos, versiones, conteos, referencias. Todos los conteos cuadraban. Esta clase de defecto vive **dentro de una cláusula**, y solo aparece cuando alguien abre la cláusula.
>
> ⚠️ **Este barrido no busca nada nuevo.** Lee lo que los forenses ya concluyeron y comprueba si llegó. Sin investigación.

---

## Marcador

| Veredicto del barrido | Cuenta |
|---|---|
| ✅ **LLEGÓ** — el matiz o la rotura está en el motor o en la ficha | 8 |
| ⚠️ **NO LLEGÓ** — está en el forense, no en el motor | **6** → ✅ **los 6 aterrizados el 28/jul** |
| 🟡 **PARCIAL** — llegó la conclusión, no la condición que la acota | 3 |
| ⭕ **SIN OBJETO** — el veredicto toca una regla que el motor no tiene | 5 |
| **TOTAL** | **22** |

**Seis roturas o matices archivados que el motor nunca recibió.** Dos de ellos tocan reglas **dentro del perímetro del Hito D**.

> ✅ **CERRADO el 28/jul/2026.** Los seis bajaron. P-01, P-02 y P-03 en `modelo v2.4`. **P-04, P-05 y P-06 exigieron ampliación de alcance** —el motor no tenía reglas de crédito formuladas— y se decidió ampliarlo (**ADR-35**): dos reglas nuevas en `§3.1` y una prohibición dura en `§5.5`. El motor pasa a **49 reglas**.
>
> ⚠️ **Lo que la ampliación NO resuelve:** el motor sigue **sin entidad prestamista**. Modela al decisor, no al oferente. El hallazgo mejor sostenido del corpus sobre crédito —*el riesgo vive en el fondeo y el gobierno corporativo del prestamista, no en el deudor* (Famsa, Crédito Real; n=2)— **sigue sin poder representarse**, y su refutación sigue **sin objeto**.

---

## 1 · Los que NO llegaron *(entregable principal)*

### ⚠️ P-01 · `bandwidth tax` fue **parcialmente refutado como motor primario**, y el motor lo sigue citando como driver

**Forense:** `Crédito_Fácil` (V5), Regla 3.

> *"'Horizonte corto + preferencia por el presente / G3 escasez' → **MATIZADA y parcialmente REFUTADA como motor primario**. La mentalidad de escasez tipo Mullainathan-Shafir es un **marco teórico IMPORTADO** y plausible, pero la evidencia mexicana directa lo relativiza: la ENIF muestra **alta aversión declarada al endeudamiento (38.4%)**, lo que contradice un cortoplacismo cultural."*

**Estado en el motor:** `§3.6` sigue diciendo *"pospone lo no urgente, improvisa el bomberazo — **PORQUE bandwidth tax (G3)**"*.

**Por qué es el hallazgo más serio del barrido.** Ayer marqué `bandwidth tax` como *"sin tier leído"* (glosario §16). **Es peor que eso: tenía veredicto, y el veredicto era desfavorable.** El forense lo identificó como marco importado **(c)** *y* lo relativizó con dato mexicano directo. Y toca **G3 — el único generador PROBADO del modelo**: si su mecanismo nombrado está parcialmente refutado, lo que sobrevive es la conducta observada, no la explicación.

**Acción:** el `PORQUE` de §3.6 no puede seguir nombrando `bandwidth tax` sin la marca **(c)** y sin el matiz de V5. Aplicado en `modelo v2.4`.

---

### ⚠️ P-02 · La agencia del votante **cede bajo dos condiciones específicas**, y el motor la enuncia sin ellas

**Forense:** `Clientelismo` (V2), dos cruces separados: *"MATIZA Regla 1 — la agencia no es absoluta; hay compra efectiva bajo condiciones específicas"* y *"MATIZA Regla 1 con un mecanismo falsable"*.

Las dos condiciones son concretas y están medidas: **(a) proximidad/focalización** — Cantú 2019 documenta efecto persuasivo real de las tarjetas Soriana; **(b) monitoreo percibido** — Ascencio-Chang 2025: la probabilidad de voto clientelar sube de **0.06 a 0.63** en laboratorio cuando el votante cree que su voto puede observarse.

**Estado en el motor:** `§3.7` enuncia la autonomía sin sus condiciones de cesión. `monitoreo del voto` aparece en la lista de disparadores del dominio, pero **no dentro de la regla**, y `proximidad/focalización` no aparece en ninguna parte.

**Por qué importa para el Hito D.** Es una regla `[FUERTE]` del perímetro. Un falsador escrito contra *"la transferencia no mueve el voto"* sin las condiciones de cesión es **infalsable por generalidad**: cualquier caso de compra efectiva se descarta como local. Con las condiciones, el falsador se vuelve preciso — *¿cede donde hay proximidad y monitoreo percibido, y sólo ahí?*

---

### ⚠️ P-03 · La distinción **turnout buying vs. vote-choice buying** no existe en el motor

**Forense:** V2. *"El clientelismo compra **ASISTENCIA** de simpatizantes cuando el partido puede monitorear al broker; distingue turnout buying de vote-choice buying."* Larreguy, Montiel Olea y Querubín (2017, AJPS): la eficacia del SNTE viene del **apego partidista**, no de la dádiva.

**Estado en el motor:** `§3.7` trata "el voto" como un objeto único. La dádiva **sí** compra que vayas a votar; **no** compra a quién le votas. Son dos conductas distintas y el motor no las separa.

**Consecuencia:** una regla que dice *"no mueve el voto"* es **verdadera para la elección y falsa para la asistencia**. Sin la distinción, el veredicto del Hito D saldrá ambiguo.

---

### ⚠️ P-04 · El **techo de mora** del crédito popular no está en el motor

**Forense:** `Crédito_Popular` (V4). *"CONFIRMA 'sí pagan aunque caro' pero **MATIZA fuerte**: el techo de mora en efectivo/tarjeta (**15–20%**) está cerca del límite donde solo un CAT de tres dígitos lo hace viable."* Y: *"el scoring alternativo **subestima el riesgo** en productos de efectivo/tarjeta al popular… el precio absorbe el error de predicción."*

**Estado en el motor:** ausente. La ficha §4 registra el *riesgo relocalizado* (fondeo y gobierno corporativo del prestamista, no el deudor), pero **el techo cuantificado no está en ninguna regla**.

**Por qué importa:** es el único número del corpus que marca **dónde deja de funcionar** una regla del modelo. Un límite cuantificado es material de falsador de primera calidad, y estaba archivado sin usar.

---

### ⚠️ P-05 · La advertencia condicional de la baja fricción

**Forense:** V5, Regla 2. *"'Utilidad + fricción baja vence aversión al riesgo' → SÍ debe incorporar una **ADVERTENCIA downstream, de fuerza MEDIA**… la baja fricción amplifica el riesgo **SOLO cuando se combina con tasas usurarias y con reporte crediticio incompleto** — es decir, la advertencia es **condicional a la estructura, no a la conducta pura**."*

**Estado en el motor:** ausente. La regla de utilidad quedó acotada a gobierno digital (cambio 11) y su versión de crédito se retiró — pero **el matiz downstream se retiró con ella**, cuando aplicaba al lado del crédito, que es donde el forense lo puso.

---

### ⚠️ P-06 · "Burbuja" debía degradarse y el motor nunca la tuvo — pero la ficha sí afirma el riesgo

**Forense:** V5, Regla 1. *"El modelo debe **DEGRADAR 'burbuja' a 'riesgo latente focalizado y vigilable'**, no afirmarla."* Base: la mora sube pero es baja, el crédito se desacelera, **IMORA en mínimos de una década**.

**Estado:** la ficha dice *"BNPL como riesgo latente"* ✅, pero **sin la evidencia que obliga a la degradación** (el IMORA en mínimos). Queda como afirmación sin su respaldo, que es la forma en que un matiz se convierte en eslogan.

---

## 2 · Los parciales

| # | Veredicto | Qué llegó | Qué falta |
|---|---|---|---|
| 🟡 **PP-01** | V3: *"no es 'el mexicano aspiracional', es **el hogar A/B con ingreso resiliente**"* — MATIZA con disciplina anti-esencialista | El motor segmenta el consumo compensatorio por perfiles 2, 3 y 5 | **La variable decisiva declarada es el NIVEL DE INGRESO (estructural)**, no la psicología. El motor conserva el driver psicológico (G2) como principal |
| 🟡 **PP-02** | V3: dos ROMPE limpios — **Ikea** (*"el supuesto psicológico NO importó; decidió accesibilidad + novedad de formato"*) y **autos chinos** (*"ganaron por precio + equipamiento + timing; el estatus de marca jugó EN CONTRA"*) | El motor marca `[FUERTE como correlación]` y anota que V1 lo rompió *"como driver decisivo aislado"* | **Dos casos donde el estatus jugó en contra** y donde la psicología no importó. Eso no es sólo "no es driver aislado": es evidencia direccional contraria en un segmento |
| 🟡 **PP-03** | V3: la premiumización **no es un bien de Veblen** — el driver es *wellness + gestión de ingresos* | — | El motor no tiene mecanismo alternativo para la premiumización; sigue enrutándola por estatus |

---

## 3 · Los que sí llegaron ✅

`credit scoring tipo EE.UU.` ROTO → datos alternativos · `el consumidor mexicano como bloque` ROTO · `confianza radial` permanece HIPÓTESIS → **G1b CONTRADICHO** en el modelo · `calidad y dignidad > barato` **NO VALIDADA** (su ancla era publicidad, no métrica de compra) · `el informal no paga` ROTO · **colapso de prestamista = fondeo, no deudor** (Famsa, Crédito Real) · `sin broker` ROTO PARCIALMENTE → **`conf.08`, corregido en v2.3** · **tier MEDIA correlacional** de la mitad de atribución → corregido en v2.3.

## 4 · Sin objeto ⭕

Cinco veredictos tocan **`masstige` / `premium accesible`** y **`el macho como palanca aspiracional`**. Ninguno de los dos es regla del motor: `masstige` fue precisamente **la regla fantasma del Hito 2** —una recomendación de negocio del integrador ascendida a "regla del modelo" por un prompt—. Se registra que V1 y V3 gastaron esfuerzo forense estresando algo que el motor nunca tuvo, **incluida la refutación de V3 de que el "SOLO" de esa regla es falso**.

---

## 5 · Lectura

**6 de 22 no llegaron, 3 llegaron a medias.** Es una tasa de fuga del **~41%** en la capa que el programa considera *evidencia primaria del mismo rango que los reports* (ADR-29.b).

**Y el patrón no es aleatorio: se fugó lo condicional.** Lo que llegó fueron los veredictos **binarios** —"esto está roto", "esto no se validó"—. Lo que no llegó fueron los **matices con condición**: *cede bajo proximidad y monitoreo* · *solo con tasas usurarias y reporte incompleto* · *el techo está en 15–20%* · *parcialmente refutado como motor primario*.

Tiene sentido mecánico: un ROMPE binario cabe en una línea del changelog; un matiz condicional exige reescribir la regla. **La retropropagación se ejecutó donde era barata.**

**Consecuencia para el Hito D, que es lo que motivó el barrido:** dos de las seis fugas (P-02, P-03) tocan reglas `[FUERTE]` del perímetro, y una tercera (P-01) toca el `PORQUE` de una regla `[MEDIA]` en G3. Escribir sus falsadores sin estos matices habría producido pruebas contra afirmaciones que el corpus ya había acotado — el escenario de `conf.08` repetido.

**Requisito de salida propuesto (ADR-34).** Todo forense nuevo cierra con una **tabla de propagación**: veredicto · regla del motor citada textualmente · edición concreta que exige · casilla de aplicado con fecha. Sin esa tabla el forense no se archiva como canónico. *El defecto no fue que faltara el protocolo —ADR-29 lo ordena— sino que el forense podía terminar sin dejar nada que faltara visiblemente si el matiz no bajaba.*

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** El barrido en sí, no. Pero el hallazgo P-01 lo hace visible en el motor: `bandwidth tax` es un mecanismo **cognitivo** puesto a explicar una conducta que V5 relativiza con dato estructural (aversión declarada al endeudamiento del 38.4%). Ese es exactamente el movimiento que el corpus existe para vigilar, y estaba dentro del propio modelo.

**¿Qué sobregeneraliza desde clases medias urbanas?** Los cinco forenses son de dominio financiero, de consumo y electoral — terrenos con dato porque hay mercado formal o padrón que lo genera. **Ninguna de las 22 fugas viene del México rural-popular**, no porque ahí no las haya, sino porque ahí no hubo forense.

**¿Qué está sesgado por marcos extranjeros?** P-01 es un caso puro: `bandwidth tax` (Mullainathan y Shafir) es marco importado **(c)** que llevaba dos años operando como driver sin marca, y con un veredicto desfavorable archivado.

**¿Qué cambiaría con foco rural, indígena o popular?** El techo de mora (P-04) es urbano-popular formal. Su equivalente rural —el crédito de avío, los Fondos de Aseguramiento— es justo donde vive el candidato falsador más fuerte del programa y no tiene forense.

**¿Qué parece psicológico y es incentivo racional?** El propio V2 lo dice de su hallazgo: *"la 'gratitud' al líder puede ser **voto retrospectivo racional** —recompensar ingreso real recibido—, no lealtad afectiva."* Ese matiz también estaba archivado y sin bajar.

**¿Dónde hay evidencia débil e intuición fuerte?** En mi propia tasa de fuga del 41%: sale de **22 ítems de 5 forenses**, todos leídos por mí hoy, sin segundo lector. Un ítem clasificado como ⭕ SIN OBJETO por error se convertiría en ⚠️ NO LLEGÓ y movería la cifra. **La tasa es orientativa; los seis casos nombrados son verificables uno por uno.**

**¿Qué sería peligroso mal usado?** Leer "41% de fuga" como *"los forenses no sirvieron"*. Es al revés: los forenses **hicieron su trabajo y lo dejaron por escrito**. Lo que falló fue el canal de bajada. Y la lectura opuesta es igual de mala — *"ya se barrió, entonces está limpio"*: este barrido cubre lo que los forenses **declararon** como veredicto, no lo que quedó implícito en sus casos.
