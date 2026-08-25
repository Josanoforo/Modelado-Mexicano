# COERCIÓN Y ADOPCIÓN · rediseño del criterio · 20/ago/2026

**PROPUESTA (no sellada) — adjunto de mesa 24/ago, sha256 f77d705eac4b9f5eadd846e96503c4add5ef798b779de52e3e4f8080c107f5cb**

> | | |
> |---|---|
> | **QUÉ ES** | Rediseño de la condición A de `R3.4` desde el criterio, no desde el dato. Benchmark web de cuatro campos + siete casos mexicanos derivados. **PROPUESTA, no sellada.** |
> | **POR QUÉ** | Mesa: *«lo importante es tener el criterio correcto que forme la base del motor… no tomamos decisiones por costo sino por lo que le otorgue lo mejor al modelo.»* |
> | **PROCEDENCIA** | Repo verificado contra `origin/main`; benchmark web 20/ago; cifras de terceros marcadas como tales. **Ninguna cifra de este documento entra al motor sin acto propio.** |
> | **LO QUE URGE** | **Hay una ventana de medición abierta que se cierra en julio.** §5. |

---

## 1 · El error de raíz, y no era de aritmética

`ADR-37` corrigió la v0.1 del gate porque el criterio estaba escrito **en términos de canal** cuando lo que prueba es §3.3 (utilidad vs. coerción con riesgo fiscal). El diagnóstico fue exacto y **la corrección no llegó a la condición A**: la A corregida sigue comparando CoDi contra *«el canal retail-efectivo tipo OXXO Pay»*.

Y hay algo peor, que el propio corpus ya tenía escrito y nadie propagó al gate:

> *«CoDi fracasó porque los mexicanos rechazan al gobierno.» **No: fracasó por fricción, miedo al SAT y falta de utilidad marginal sobre SPEI.***
> — `corpus/reports/Adopción_y_Resistencia_Tecnológica…:166`

**Tres componentes. El motor tiene un disparador.** La Nota 3 de `R3.4` lo declara para dos; el tercero —utilidad marginal sobre un sustituto ya existente— no está ni nombrado.

**Y el benchmark añadió un cuarto que ningún documento del programa tiene:** la coerción del lado de la **oferta**. El corpus dice que Brasil y la India lo lograron *«mediante diseño abierto, gratuidad, **obligatoriedad de participación de bancos**»*. Pix obligó a los bancos; CoDi no obligó efectivamente a nadie. **Esa es una explicación estructural del fracaso de CoDi que compite con la psicológica, y el gate no puede distinguirlas** — que es exactamente lo que el Bloque C existe para impedir.

---

## 2 · Lo que dice el estado del arte, y reencuadra la variable dependiente

**El hallazgo que manda sobre todos los demás.** En contextos obligatorios, la literatura de aceptación tecnológica dice que *es engañoso examinar la conducta de uso como una «elección», porque incluso los usuarios con percepciones negativas se ven compelidos a usar el sistema* (Coping Theory, EJIS 2017). Y la crítica formal a UTAUT lo confirma: *la voluntariedad supone que el individuo tiene latitud considerable en su decisión de adopción — lo que no tiene por qué ser cierto cuando la adopción es mandatada* (Information Systems Frontiers 2017).

**Traducción: bajo mandato, lo que se mide es CUMPLIMIENTO, no ADOPCIÓN. Son dos variables dependientes distintas y `R3.4` las confunde en una.**

**Y el mecanismo mismo cambia con la coerción.** UTAUT: *en contextos de adopción obligatoria los efectos de influencia social son sustancialmente más fuertes; en contextos voluntarios domina la expectativa de desempeño y la presión social es mínima.* **El generador que explica CoDi no puede ser el mismo que explique el registro de líneas** — y si el motor usa uno solo, va a estar mal en uno de los dos.

**Y la coerción produce respuesta propia:** el uso forzado suele producir insatisfacción y resistencia. Eso no es una nota al pie: es una variable de desenlace que el modelo no tiene.

**De medición, tres reglas que ya adoptamos y aquí se confirman:**
- **Acceso ≠ uso** (Findex): la oferta y la demanda no se comparan entre sí.
- **La definición se impone antes** (GSMA/CGAP): registrado vs. activo a 30/90 días. Globalmente, ~75% de las cuentas registradas está inactivo cada mes — elegir mal cambia la respuesta por un factor de ~4.
- **Fuentes que no observan las mismas unidades entregan cotas, no puntos** (StatMatch); un umbral se adjudica por posición del intervalo (Manski).

---

## 3 · Banxico ya publica la distinción exacta que necesitábamos

`codi.org.mx/secundarias/estadisticas.html` publica, por separado: **cuentas validadas** · **cuentas que han realizado al menos una transacción** · operaciones · monto · **distribución geográfica por municipio** y **proporción de cuentas validadas sobre población adulta por municipio**. Y hay API (`SieAPIRest`).

**Cifra de terceros, a verificar contra la fuente antes de usarse:** a junio de 2024, CoDi tenía **>20 millones de cuentas validadas** y **1.9 millones** habían hecho al menos un pago (1.03M un cobro) — razón activo/validado ≈ **1:10.5**. Es el problema registrado/activo de GSMA, con las dos series publicadas por el mismo emisor. **La brecha de conmensurabilidad que mató mi cálculo anterior no existe en este par.**

⚠️ **Y desmiente la cifra que el motor usa.** `tramite.yaml:77` dice *«CoDi = 3.09M cuentas con ≥1 transacción en 6 años»*; el report dice 21.8M mayormente inactivas; Banxico a junio/2024 da >20M validadas y 1.9M con pago. **`hitoD-preregistro:810` ya había declarado esta discrepancia sin resolver.** El acto de medición la cierra o la declara.

---

## 4 · Los siete casos, y las cinco variables que los separan

| Caso | Coerción | Sanción | Dato sensible | Sustituto previo | Lado obligado | Desenlace |
|---|---|---|---|---|---|---|
| **SPEI** (2004–) | no | — | no | — *(es el incumbente)* | — | adoptado ampliamente |
| **CoDi** (2019–) | no | — | no | **SPEI, fuerte** | ninguno efectivo | validadas ≫ activas |
| **DiMo** (2023–) | no | — | no | SPEI/CoDi | — | ~7M cuentas |
| **OXXO Pay / Spin** | no | — | no | efectivo *(integra, no sustituye)* | — | 13M+ usuarios |
| **RENAUT** (2008) | **sí** | suspensión | CURP | — | **usuario** | **base vulnerada, datos a la venta, suspendido** |
| **PANAUT** (2021) | **sí** | suspensión | **biométricos** | — | **usuario** | **anulado por la SCJN antes de operar** |
| **Registro 2026** | **sí** | **bloqueo, corte en julio** | CURP, **sin biométricos** | — | **usuario** | **EN CURSO** |
| *(Pix, Brasil)* | **sí** | — | no | — | **bancos** | ~80% de adultos |

**Lo que este conjunto permite y ningún par permitía:**

- **`PANAUT` contra `Registro 2026` es el contraste más limpio del conjunto entero.** Misma coerción, misma sanción, mismo emisor, mismo objeto — **difieren solo en la sensibilidad del dato pedido**. El registro de 2026 fue diseñado, textualmente, *«con pinzas para no cometer los errores del pasado»* y **no pide biométricos**. Eso aísla la variable de riesgo/vigilancia mejor que cualquier comparación de pagos.
- **`RENAUT` da el desenlace que a `PANAUT` le falta**: corrió, su base se vulneró, los datos acabaron a la venta y el Senado lo suspendió. **Es evidencia de desenlace documentado, no marginal de encuesta** — la clase que `ADV1-M1` exige y que casi no existe.
- **`Pix` contra `CoDi` aísla el lado obligado**: oferta contra nadie. Es la explicación estructural que compite con la psicológica.
- **`CoDi` contra `SPEI` aísla utilidad marginal**, no riesgo fiscal — porque **SPEI también es trazable al SAT** y aun así se adoptó.
- **`DiMo` contra `CoDi`** es casi un experimento de laboratorio: mismos rieles, mismo emisor, misma trazabilidad, **distinta fricción de UX** (alias telefónico contra QR). **Aísla el componente que la Nota 3 declara sin disparador.**

**Y una variable de segundo orden que el corpus ya midió y hay que conservar:** la resistencia biométrica es *«más de élites informadas»*. El registro de 2026, con sanción de bloqueo, cae sobre la población general. **La composición de quién resiste es parte del desenlace, no ruido.**

---

## 5 · La ventana que se cierra en julio — y es lo más valioso de todo esto

**El registro de líneas de 2026 está corriendo ahora**, con corte en julio y **bloqueo de línea** como sanción, sobre un universo de ~148 millones de líneas activas.

Eso es, simultáneamente:
- **coerción con sanción real y masiva**, no una encuesta de intención;
- **desenlace documentado**, no marginal;
- **fuera de muestra por construcción**, porque el resultado **todavía no existe**;
- **posterior al corte de cualquier modelo de lenguaje**, que es el filtro (v) de `ADV1-M1` — el que el programa **no puede satisfacer con ninguna encuesta**, porque todas las olas disponibles son anteriores.

**Un pre-registro hecho ahora, antes de julio, es la única celda genuinamente limpia que este programa puede construir.** Y se pierde si no se hace antes del corte.

**Lo que exige, y es poco:** declarar hoy, en commit, qué predice el modelo sobre la tasa de cumplimiento —global y por segmento: rural/urbano, edad, prepago/pospago— y qué predice el corredor `L`, **con los hashes comprometidos antes de que exista el dato.** Es `ADV1-M2` aplicado a un desenlace real.

---

## 6 · El objetivo, redefinido

**No es adjudicar la condición A.** Es darle al motor un criterio que distinga los cuatro componentes que hoy confunde:

1. **Dos variables dependientes, no una.** `cumplimiento` bajo mandato y `adopción` sin mandato **no son la misma conducta**, y la literatura dice que ni siquiera responden a los mismos determinantes. El motor necesita las dos, y `R3.4` debe declarar cuál mide.
2. **Un disparador por componente**: `riesgo_fiscal_percibido` (ya existe) · `friccion_uso` (declarado faltante en la Nota 3) · `utilidad_marginal_sobre_sustituto` (sin nombrar) · `lado_obligado` ∈ {ninguno, oferta, usuario} · `sancion` ∈ {ninguna, suspensión, bloqueo} · `dato_sensible` ∈ {no, identificador, biométrico}. **Eso es trabajo de `EMISOR-M-2`, y ahora tiene razón concreta en vez de ser ampliación genérica.**
3. **Re-especificar la condición A** para que compare pares que difieran en **una** variable. Con la tabla de §4 hay al menos cuatro pares así, y ninguno es el que la spec fijó.
4. **Medir con las series que el emisor sí publica**, en la misma definición y ventana, y **reportar cotas** donde las fuentes no observen las mismas unidades.

---

## 7 · Lo que esto le hace a `FP-104`

Deja de ser *«¿pareja-SPEI o retail-OXXO?»*. **Ninguno de los dos aísla el mecanismo**, y elegir entre ellos era elegir entre dos instrumentos inválidos.

Pasa a ser: **¿se re-especifica la condición A de `ADR-37` sobre pares de una sola variable, o se declara que `R3.4` prueba la diferencia total y se renombra lo que afirma?** Y como corolario: **¿se abre el pre-registro del registro de líneas antes de julio?**

**La primera es de mesa y es más grande que la anterior. La segunda tiene fecha de caducidad.**

---

## 8 · Reservas, declaradas

Las cifras de CoDi, Spin, DiMo, SPEI y las 148M de líneas **son de terceros y de esta sesión de búsqueda**: se verifican contra la fuente primaria antes de entrar a cualquier ficha. La lectura de que `PANAUT` nunca operó es de nota de prensa y del comunicado de la SCJN; hay que confirmar que no hubo registro parcial entre abril/2021 y abril/2022. La tabla de §4 es **diseño, no medición**: cada celda es una hipótesis de clasificación que el acto debe verificar. Y todo el §2 es marco importado — procedencia **(c)** del Bloque A, adoptado con crítica: sirve para nombrar variables, no para afirmar nada sobre México.
