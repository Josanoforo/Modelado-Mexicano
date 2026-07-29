# Verificación: la ambigüedad de perímetro 20/27 se retira

**Fecha:** 29 de julio de 2026
**Relación con `2026-07-29-perimetro-suite-T07-T10.md`:** complemento, **no corrección**. Esa nota es append-only y no se toca. Nada de lo que afirma queda invalidado aquí.

---

## 0. Qué se retira, y de dónde venía

Se retira la hipótesis de que **el perímetro fuerte del Hito D es ambiguo entre 20 y 27 reglas** según cómo se cuenten las etiquetas de tier compuestas del motor.

**Procedencia de la cifra: el encargo de trabajo del 29/jul**, que la planteó como punto abierto, textual: *"el motor usa 7 etiquetas de tier donde el canónico define 4, y el perímetro fuerte es 20 o 27 según dónde caiga la raya"*.

**La nota del 29/jul nunca afirmó esa ambigüedad.** Lo único que dice sobre el vocabulario del motor es `2026-07-29-perimetro-suite-T07-T10.md:26`:

> *"El motor (`canon/modelo-decision-v3_2.md`) solo lo revisan T04 (diagonal en ENTONCES) y T12 (conteos). Ningún test valida vocabulario de tiers, marcas de procedencia ni lenguaje causal dentro del motor, el glosario ni el integrador."*

Es cierto y sigue vigente. No menciona 20, ni 27, ni ambigüedad de perímetro. **Esta nota no corrige el registro: verifica una hipótesis de trabajo que nunca entró al registro.**

---

## 1. Evidencia que la refuta

### 1.a — Salida literal de T12

`tests/check.py` corrido sobre HEAD `9301e59`:

```
motor: 49 reglas · 20 [FUERTE] · 20`[FUERTE]` · 19`[MEDIA]` · 5`[MEDIA-FUERTE]`
       · 2`[HIPÓTESIS]` · 1`[FUERTE como correlación]` · 1`[FUERTE / MEDIA]`
       · 1`[MEDIA / HIPÓTESIS]`
```

*(La duplicación de `20 [FUERTE]` es del formato del `print`, no un doble conteo: el primero es la variable `fuerte`, el resto es el `Counter`.)*

Siete etiquetas distintas, sí. Cuatro canónicas (20+19+5+2 = 46) y tres compuestas (1+1+1 = 3). Total 49.

### 1.b — Cuáles son las "2 compuestas" del perímetro

`gobernanza-v1_8.md:266` fija el perímetro sin listar las reglas:

> **Registro de decisión · Perímetro del Hito D = 27 reglas** *(28/jul/2026, antes de escribir el primer falsador)*. 20 `[FUERTE]` + **5** `[MEDIA-FUERTE]` + 2 compuestas. *(Eran 26; la partición de protesta/autodefensa por ADR-33 convirtió una en dos.)*

El motor tiene **tres** etiquetas compuestas, no dos, así que la aritmética sola no dice cuáles entran. Lo resuelve `hitoD-preregistro-v2_0.md:17`, que nombra el tratamiento de cada una:

> *"Las compuestas llevan **un falsador por mitad**. La `[FUERTE como correlación]` se ataca **como correlación**, no como causa."*

Y las fichas confirman la membresía: `R1.4` lleva `[FUERTE como correlación]` (L59) y `R4.3` lleva `[FUERTE / MEDIA]` (L122). **`[MEDIA / HIPÓTESIS]` no aparece en ninguna ficha**: queda fuera del perímetro, coherente con no tener componente fuerte.

**Perímetro = 20 + 5 + 1 + 1 = 27.** Cuadra exacto contra `gobernanza:266`. **No hay ambigüedad 20/27, y no la hubo nunca en el motor real.**

---

## 2. De dónde salió el error de medida

La estimación descartada usó `grep -oE '\`\[[^]]*\]\`'` sobre **el archivo completo** del motor, no sobre las reglas de `§3.B`. Resultado: 32 `[FUERTE]`, 21 `[MEDIA]`, 9 `[MEDIA-FUERTE]`, 4 `[HIPÓTESIS]`, 3 · 3 · 2 en las compuestas — **74 etiquetas para 49 reglas**. Las 25 de más son menciones en prosa, cabeceras, ejemplos y notas de versión.

T12 no comete ese error porque parsea solo las líneas que empiezan con `- **SI**` dentro de `§3.B`.

**El patrón:** contar con `grep` sobre un archivo entero mide *menciones*, no *reglas*. Es la misma familia del defecto que la nota original documenta en T10 — un patrón literal que no distingue **uso** de **mención**.

---

## 3. Qué queda vivo del hallazgo original

**T07 no vigila el vocabulario de tier del motor.** Solo audita `corpus/reports/*.md`. Las tres etiquetas compuestas existen en `§3.B`, no hay registro de si son extensión sancionada del vocabulario de 4 o deriva sin documentar, y **nada haría ruido si apareciera una cuarta**. Sigue abierto; es lo único que sobrevive de la hipótesis del encargo.

---

## 4. Hallazgo nuevo: el pre-registro cubre 24, no 27

Verificado al buscar la membresía del perímetro.

| Fuente | Afirma | Verificación |
|---|---|---|
| `hitoD-preregistro-v2_0.md:8` | *"contiene **27 fichas** (R1.1 a R10.3)"* | **24** encabezados `## R` |
| `hitoD-preregistro-v2_0.md:13` | *"v2.0 completa el perímetro: **27 de 27**"* | **24** |
| `estado` §7, en su v1.7 | *"✅ Paso 1 COMPLETO. `hitoD-preregistro` v2.0 cubre las 27 del perímetro"* | **24** |

**Conteo por tier de los 24 encabezados:** 18 `[FUERTE]` + 4 `[MEDIA-FUERTE]` + 1 `[FUERTE como correlación]` + 1 `[FUERTE / MEDIA]` = 24.
**Faltan 3 fichas:** 2 `[FUERTE]` y 1 `[MEDIA-FUERTE]`.

### 4.a — Las tres reglas que faltan

**No existe ningún encabezado `R3.x` en el pre-registro.** El dominio `§3.3` del motor —*autoridad, trámite y relación con el Estado*— quedó **entero** fuera. Tiene 4 reglas, de las cuales **3 son de perímetro**, y son exactamente las 3 que faltan:

| `modelo §3.3` | Tier | Regla (texto del motor, recortado) |
|---|---|---|
| regla 1 | `[FUERTE]` | *"**SI** el trámite es presencial con funcionario discrecional y sin registro **ENTONCES** alta probabilidad de mordida — PORQUE trampa social (G1)"* |
| regla 2 | `[FUERTE]` | *"**SI** el trámite se digitaliza / hay testigos / el funcionario es registrable **ENTONCES** la mordida baja — PORQUE se rompe la trampa"* |
| regla 4 | `[MEDIA-FUERTE]` | *"**SI** se ofrece un servicio de gobierno digital de forma **coercitiva y con riesgo fiscal** (tipo CoDi/SAT) **ENTONCES** se rechaza"* |

*(La regla 3 de `§3.3` —norma inútil → evasión— es `[MEDIA]` y no pertenece al perímetro. 2 `[FUERTE]` + 1 `[MEDIA-FUERTE]` = 3, que cierra exacto contra 27 − 24.)*

⚠️ **Sobre los identificadores:** se citan por sección y posición en el motor, no por `Rn.n`. El pre-registro **renumera**: su `R4.2` es la regla 3 de `modelo §3.4`, porque salta las `[MEDIA]`. Con dos convenciones en circulación, el texto de la regla es la única referencia que no se presta a confusión.

### 4.b — `R3.4` nombrada sin ficha

`R3.4` **sí aparece en el cuerpo** del pre-registro, pero **no tiene ficha propia**. Es la regla del gate: la que ADR-37 declaró desbloqueada el 28/jul y que `estado §7` registra como *"✅ desbloqueada el 28/jul por ADR-37. Su umbral es ahora el criterio de tres condiciones del gate."*

**Desbloqueada no es pre-registrada.** Se le asignó umbral en `gobernanza` y se la dio por lista, sin que llegara a existir el artefacto que la haría falsable.

### 4.c — Por qué pesa más que un conteo

`§3.3` es donde vive **`riesgo_fiscal_percibido`**, el disparador del que depende el gate de Fase 1 (ADR-37, ADR-26). **El dominio que sostiene el gate es el único sin un solo falsador pre-registrado.**

### 4.d — Tres autodeclaraciones que decían 27

| Artefacto | Afirma | Real |
|---|---|---|
| `hitoD-preregistro` L8 (cabecera *VERIFICAS ASÍ*) | *"contiene **27 fichas** (R1.1 a R10.3)"* | 24 |
| `hitoD-preregistro` L13 | *"v2.0 completa el perímetro: **27 de 27**"* | 24 |
| `estado` §7, en su v1.7 | *"✅ Paso 1 COMPLETO […] cubre las 27 del perímetro"* | 24 |

**Ninguna de las tres es una lectura: las tres son la misma afirmación repitiéndose.** Es el patrón que ADR-32 nombró —*dos de los seis casos de propagación figuraban como ✅ sin estarlo, y el glosario, el modelo y la gobernanza repetían el ✅ unos de otros*— reaparecido en el conteo de fichas. La cabecera `VERIFICAS ASÍ` de ADR-36 existe precisamente para que un lector compruebe la cifra en dos segundos; aquí **la cabecera declara el número que hay que verificar, y nadie lo contó**.

**No se corrige aquí, y no se propone cómo llenar el hueco** — eso es decisión aparte. `hitoD-preregistro` es append-only y `modelo` no se toca. Lo único que se corrige es `estado`, por ser la única fuente de estado y publicar hoy una cifra que su propio artefacto no respalda.

---

## 5. Una cita de la nota original que no checa

`2026-07-29-perimetro-suite-T07-T10.md:87` atribuye a `forense/curaduria-archivos.md:23` la frase:

> *"convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón"*

`curaduria-archivos.md:23` es una fila de tabla sobre `estado-proyecto-psicologia-mexicano.md` —**borrado** el 27/jul— y su estado de SUPERADO. La frase citada **no aparece en ese archivo, ni en ningún otro del repo** — `grep -rn "pelón"` sobre `forense/`, `corpus/` y `canon/` solo la encuentra dentro de la propia nota que la cita.

**No se edita la nota** (append-only). Se registra aquí para que la cita no se propague: **el mecanismo que describe —el tier que viaja sin su marca de procedencia— sigue documentado y verificado en `integrador:174`/`175`**, que sí se leyeron textualmente. Lo que no tiene respaldo es la atribución de esa frase a ese archivo y esa línea.

---

## 6. Cifras de la nota original que no se reprodujeron

Al recomputar con los patrones literales de T10 sobre el árbol en `9301e59`:

| Cifra | Nota original (§3, §5) | Recomputado hoy |
|---|---|---|
| T10 sobre `corpus/reports/` | 66 "ya atrapados" | **65** |
| T10 sobre `canon/` + `forense/` | 45 "nuevos" | **57** |
| T10 solo en el integrador | 5 | **14** |

**No se corrige la nota.** La diferencia puede venir de un conjunto de archivos distinto o de deduplicación manual — no consta el método. Se registra para que estas cifras **no se citen como verificadas** aguas abajo. Lo que sí está verificado y se sostiene es el análisis cualitativo de §3: los **4 defectos de medida** y el **defecto real de `integrador:174`**, cada uno con su bloque leído textualmente.

---

## 7. Resumen

| Afirmación | Estado |
|---|---|
| Perímetro ambiguo 20/27 | ❌ **RETIRADA.** Es 27; cuadra exacto contra `gobernanza:266` |
| Origen de la cifra 20/27 | El encargo del 29/jul, no el registro |
| T07 no vigila el vocabulario del motor | ✅ **VIVA.** Único superviviente de la hipótesis |
| El pre-registro cubre 27 | ❌ **FALSA.** Cubre 24; `§3.3` sin ficha alguna |
| `curaduria-archivos.md:23` dice *"Fuerte pelón"* | ❌ **NO CHECA.** El mecanismo sigue en pie vía `integrador:174`/`175` |
| Conteos de T10 de la nota (66/45/5) | ⚠️ **NO REPRODUCIDOS** (65/57/14). Análisis cualitativo intacto |
| El pre-registro cubre 24; faltan las 3 de `§3.3` | ✅ **NUEVO.** Ver §4 |

---

## 8 · Método: seis cifras cayeron el mismo día, todas por lo mismo

El 29/jul cayeron **seis cifras** del programa. Ninguna cayó por análisis, discusión ni relectura general. **Las seis cayeron al pedirles cita textual y número de línea.**

| # | Cifra | Decía | Es | Cómo cayó |
|---|---|---|---|---|
| 1 | WARN de T03 | 44 | **41** | Se corrió la suite y se leyó el contador |
| 2 | Estimación de disparos T09/T10 | 22 y 46 | **26 y 111** | Se enumeraron los disparos uno por uno |
| 3 | Perímetro fuerte del motor | *"20 o 27 según dónde caiga la raya"* | **27, sin ambigüedad** | Se leyó la salida de T12 en vez de `grep` sobre el archivo entero |
| 4 | Atribución de esa ambigüedad | *"la nota `9301e59` lo afirma"* | **La nota nunca lo dijo**; venía del encargo | Se pidió la línea exacta de la nota |
| 5 | Cita a `curaduria-archivos.md:23` | *"convirtió un `[MEDIO]` en un `Fuerte` pelón"* | **Esa frase no está ahí, ni en ningún archivo** | Se abrió la línea 23 |
| 6 | Cobertura del pre-registro | 27 de 27 | **24 de 27** | Se contaron los encabezados `## R` |

**Ninguna la habría atrapado la suite.** Los 13 tests corren verdes o con sus FAIL conocidos mientras las seis circulan: T12 compara conteos de reglas entre canónicos, pero **nadie compara una cifra declarada contra el artefacto que la respalda**. T11 vigila cuantificadores absolutos en afirmaciones de estado, no números. Las seis vivían en el punto ciego.

**El patrón, y no es nuevo aquí:**

- Las seis son **cifras que se citaban unas a otras** en lugar de citar la fuente. La #6 es el caso puro: tres artefactos decían 27 y ninguno había contado.
- Cinco de las seis **se produjeron con un método más barato que la verificación**: estimar en vez de enumerar (#2), `grep` sobre el archivo entero en vez del parser (#3), recordar la procedencia en vez de abrirla (#4, #5), heredar el número del artefacto anterior (#1, #6). **El método barato no es más rápido: es más rápido hasta que alguien pide la cita.**
- ADR-32 ya nombró la causa raíz —*principio declarado sin requisito de salida*—. Aquí aparece su versión numérica: **cifra publicada sin obligación de recontarla.**

**Lo que sí funcionó, y es replicable:** una sola pregunta, aplicada seis veces — *¿de qué línea de qué archivo sale este número?* Cinco de las seis cayeron en menos de un minuto cada una. La #6 tardó lo que tarda un `grep -c`.

⚠️ **Registro deliberado.** Este apartado vale tanto como los hallazgos: los seis defectos ya están corregidos o registrados, pero **el método que los produjo sigue disponible** para la próxima sesión. Un hallazgo se archiva; un método se repite.
