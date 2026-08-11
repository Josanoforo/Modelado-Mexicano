> **NOTA DE RECUPERACIÓN · 11/ago/2026.** Este documento existía solo en el espejo del proyecto; el encargo del motor adaptativo lo citó y la Ronda 1 lo clasificó NO-ENCONTRADO en repo (universo: árbol + git log --all). Entra verbatim desde el espejo — procedencia tipo (2), sin sello de commit de origen. sha256 del original en espejo: 488fc19ee407b6620ad67eb6e50be888b354ba131d7693194227694bb332728a. Resolución M0 de mesa, 11/ago/2026. Su contenido NO se edita.

# BENCHMARKS METODOLÓGICOS PARA `D-ABC` · consolidado
### Mesa #20 · 5/ago/2026 · redactado contra `origin/main` = `5ff97a5` (PR #128)

---

## ⚠️ PROCEDENCIA — léela antes que nada

**Todo este documento es TIPO (3):** búsqueda web de mesa, **no verificada contra los papers
desde el repo**. Ninguna cita se ha leído en su fuente original; todas provienen de resultados de
búsqueda y de extractos.

**Clasificación por subclase** (protocolo de manejo, clase `(d)`):

| Subclase | Qué es | Cómo se promueve |
|---|---|---|
| **(d1)** | Teorema o identidad | **Reproduciéndolo** con dataset sintético en `tests/` → pasa a tipo (1) |
| **(d2)** | Resultado de simulación o estudio metodológico | Se cita **con sus condiciones**; lo accionable es verificar si el diseño las cumple |
| **(d3)** | Estándar o convención | Vale por **adopción**, no por verdad. Nunca justifica un número |

**Y la advertencia que gobierna el documento entero:**

> **Los papers dicen lo que dicen sobre sus propias condiciones. Que el diseño del programa
> CUMPLA esas condiciones es una afirmación de mesa, derivada de las notas del programa, y
> está SIN VERIFICAR.** Las afirmaciones marcadas **⚠️ INFERENCIA DE MESA** son las que
> `RED-TEAM-A` debe atacar primero.

**Ningún elemento de este documento entra al canon sin: claim + condiciones + qué cambiaría si
el paper estuviera mal.**

---

# PARTE I · Los cuatro benchmarks de la decisión

## 1 · `D-A` tiene benchmark casi exacto — y le falta un atributo

**Fuente:** ICH E9(R1), *Addendum on Estimands and Sensitivity Analysis in Clinical Trials*
(2019). **Clase (d3) — estándar regulatorio.**

**Claim:** un estimando completamente definido requiere **cinco atributos**, acordados como
conjunto: población · condiciones de tratamiento comparadas · variable/desenlace · **medida-resumen
a nivel poblacional** · **estrategia para eventos intercurrentes**.

**Mapeo contra `D-A`:**

| Atributo E9(R1) | En `D-A` |
|---|---|
| Población | ✅ *universo declarado* |
| Contraste de exposición | ✅ *normalización de θ declarada* |
| Variable / desenlace | ✅ implícito en la ficha |
| **Medida-resumen** | ✅ *enlace y forma declarados* |
| **Eventos intercurrentes** | ❌ **no está** |

**Lo que valida:** que el **enlace sea atributo definitorio del estimando y no una decisión de
estimación** es precisamente la innovación de E9(R1). Antes del addendum, un protocolo
especificaba población de análisis y método sin necesariamente conectarlos. `D-A` los conecta.

**Lo que falta, y ya mordió dos veces:** el análogo de *"eventos intercurrentes"* aquí es la
**no-aplicabilidad estructural**. `W1` tuvo **8,084 blancos** que eran *"sin contacto"* —no
no-respuesta, sino que la pregunta no existió— y `R1.3` encontró `TSDEM` con el campo en blanco
en **70% de las filas**. Las dos se resolvieron ad hoc, bien, y **fuera del marco**.

> **RECOMENDACIÓN `D-A` (1/2):** como está, **más un quinto requisito** — *"estrategia declarada
> para no-aplicabilidad estructural y no-respuesta, distinguiéndolas"*. Sin él, dos actos pueden
> tratar el mismo blanco de forma distinta y nadie lo nota.

⚠️ **A verificar:** si E9(R1), estándar de ensayos clínicos aleatorizados, transfiere a análisis
secundario observacional de encuestas. Y si el mapeo atributo-por-atributo se sostiene, en
particular *"normalización de θ"* como análogo del atributo **tratamiento**.

---

## 2 · ⚠️ El hallazgo que cambia `D-C`: **no-colapsabilidad**

**Fuentes:** Greenland, Robins & Pearl (1999) y literatura posterior. **Clase (d1) — resultado
matemático, verificable por derivación o simulación.**

**Claim:** la **no-colapsabilidad** significa que la razón condicional difiere de la marginal
**incluso en ausencia completa de confusión**. Las razones de momios marginal y condicional
**miden cantidades distintas** y no pueden compararse directamente — compararlas equivale a
comparar coeficientes medidos en escalas distintas.

**El dato que decide:** las medidas de la mayoría de los modelos lineales generalizados **son
colapsables** — la **diferencia de riesgos y la razón de riesgos lo son; el momio y el hazard
ratio no**.

**Qué significa para el programa:**

- Los β̂ están en **diferencia de proporciones**. **Es colapsable.** Así que cuando `X` encontró
  que el marginal se invierte al condicionar, **eso es señal en esa escala** —confusión o
  modificación de efecto—, no artefacto del enlace. **A-bis regla 1 se sostiene ahí.**
- `W1-P` usó **razón de riesgos**, también colapsable. Esa comparación fue limpia.
- **Pero si `D-C` declara enlace logit** —la elección natural para un desenlace binario en un
  índice— **marginal y condicional se vuelven estimandos distintos por construcción**, y parte de
  la reversión que el programa interpretó como inestabilidad pasaría a ser **aritmética del
  enlace**.

> **RECOMENDACIÓN `D-C`:** debe declarar, **por coeficiente**, si el enlace es colapsable o no.
> Si no lo es, escribir que **marginal y condicional son parámetros distintos, no versiones
> corregidas uno del otro**.

**Corolario que mejora la redacción de `D-A`:** *"marginales jamás entran"* es correcto, **pero
por una razón que conviene escribir bien**. Con enlace colapsable el marginal es un estimando
poblacional legítimo — solo que **otro**. Con enlace no colapsable es **directamente otro
parámetro**. En los dos casos no va en una casilla condicional, pero **la razón cambia el rótulo
de lo que sí es**.

**El borde temporal, y hay que registrarlo:** si en algún momento el programa migra a momios para
el enlace del índice, **todas las comparaciones marginal/condicional hechas hasta hoy dejan de
ser comparables hacia atrás**. No se pierden — **cambian de significado**.

⚠️ **A verificar:** si la colapsabilidad de la diferencia de riesgos es **incondicional** o tiene
condiciones. Y si "colapsable" implica que una reversión al condicionar sea **necesariamente**
confusión o modificación de efecto, **o si hay otras causas** —selección, error de medición
diferencial, agregación— que producen lo mismo. **Mesa no las consideró.**

---

## 3 · Pre-registrar el conjunto de ajuste **no basta**

**Fuente:** Cinelli, Forney & Pearl, *A Crash Course in Good and Bad Controls*, **Sociological
Methods & Research** 53 (2024), 1071-1104. **Clase (d1)/(d2).**

**Claim:** controlar por Z puede **bloquear el efecto mismo que se quiere estimar** —sesgo de
sobrecontrol—; los modelos que lo hacen **violan el criterio de puerta trasera**, que excluye
controles descendientes del tratamiento por caminos hacia el desenlace. Y **contra el folclore
econométrico, no todas las variables post-tratamiento son malos controles**.

**El punto:** pre-registrar un conjunto de ajuste garantiza que **no lo elegiste viendo el
resultado**. No garantiza que **sea el conjunto correcto**. **Un mal control pre-registrado sigue
siendo un mal control.**

**Y toca los ejes del programa directamente.** Son `formalidad`, `edad`, `ingreso`,
`urbanización`. **`edad` es plausiblemente pre-tratamiento. `formalidad` e `ingreso` no**: la
experiencia de mordida puede afectar ingreso y situación laboral, lo que los vuelve candidatos a
**descendiente o colisionador**. Condicionar sobre ellos puede ser **sobrecontrol** — justo lo que
A-bis regla 2 advierte sin operacionalizar.

> **RECOMENDACIÓN `D-A` (2/2):** el conjunto de ajuste entra **con su justificación gráfica
> declarada** —qué se supone causa qué, y por qué el conjunto satisface puerta trasera— **o el
> resultado se rotula "asociación condicional sobre el conjunto S", no coeficiente.** Es la
> diferencia entre honestidad procedimental y validez de identificación.

⚠️ **A verificar, y es la objeción más fuerte contra esta recomendación:** el programa investiga
observacionalmente **cuál es el mecanismo causal**. Exigir un DAG declarado antes de estimar
exige conocer justo lo que se está investigando. **¿No es un requisito que ningún análisis podría
cumplir, y por tanto una regla que garantiza que nada entre nunca a la casilla?** Existe
literatura sobre selección de covariables **sin grafo conocido** (criterio de causa disyuntiva
modificado, análisis de sensibilidad a confusión omitida) que haría la recomendación
innecesariamente fuerte.

---

## 4 · ⚠️ La dicotomización de θ puede estar fabricando la reversión de `X`

**Fuente:** MacCallum, Zhang, Preacher & Rucker, *On the Practice of Dichotomization of
Quantitative Variables*, **Psychological Methods** 7(1) (2002), 19-40. Más Maxwell & Delaney
(1993) y Vargha, Rudas, Delaney & Maxwell (1996). **Clase (d2) — simulación con condiciones.**

**Claim central:** la dicotomización **rara vez es defendible y a menudo produce resultados
engañosos**.

**Tres consecuencias:**

**Pérdida de señal, cuantificada.** En su ejemplo, dicotomizar redujo *r* de **.30 a .21** y *r²*
de **.09 a .04** — más de la mitad de la varianza explicada, perdida por el corte.

**Las relaciones no lineales quedan borradas.** Si la relación es no lineal, la dicotomización la
**oscurece por completo**; presentar resultados basados en análisis hechos tras dicotomizar así
sería **engañoso e inválido**.

**Inflación del error tipo I en pruebas de interacción.** Dicotomizar artificialmente los
predictores **infla la tasa de error tipo I para la prueba de interacción** entre ellos **si
están correlacionados y uno tiene relación no lineal con el desenlace** (Maxwell & Delaney).
Vargha et al. mostraron que los resultados espuriamente significativos ocurren **incluso cuando
solo uno de los dos predictores se dicotomiza**.

### ⚠️⚠️ INFERENCIA DE MESA — **el elemento más frágil de todo este documento**

Mesa afirmó que **las cuatro condiciones se cumplen** en `W1`/`X`:

| Condición | Mesa dice |
|---|---|
| θ dicotomizada | ✅ `radio_confianza` a **≥6/10** |
| relación θ→Y no lineal | ✅ `X §5.1`: curva **no monótona, pico en 4** |
| predictores correlacionados | ✅ formalidad, edad e ingreso, entre sí y con θ |
| se prueban interacciones | ✅ *"eso es exactamente el condicionamiento de `X`"* |

**Y de ahí concluyó** que *"lo que `X` llamó reversión en 33 de 39 celdas es formalmente
indistinguible, con este diseño, de la firma de error tipo I inflado"*.

**⚠️ EL SALTO QUE MESA NO VERIFICÓ:** Maxwell-Delaney y Vargha trabajan sobre **regresión con
término producto** (`X₁·X₂` en una ecuación). El programa **no hace eso**: **estratifica la
muestra por celdas y estima diferencias de proporciones dentro de cada celda**. Mesa **asumió
equivalencia**. Si no la hay, toda esta alarma se desinfla.

**⚠️ Segundo salto sin verificar:** los resultados pueden depender de que el **desenlace sea
continuo**. El del programa es **binario**.

**Lo que sí se sostiene, independientemente del salto:** el corte `≥6` **no coincide con ningún
salto de la curva** por nivel, y `C-06b` estableció que el corpus cita a **≥8/10** mientras el
programa mide a **≥6/10**. **Dos cortes arbitrarios distintos sobre la misma escala**, ninguno
justificado por la distribución — el `≥6` salió del enunciado *"como en la escuela"*.

> **PRUEBA QUE LO RESUELVE, y es barata:** re-estimar `W1`/`X` con **θ cruda 0-10 o con spline**,
> sin dicotomizar. **Si la reversión desaparece, era el corte. Si sobrevive, es real y queda mucho
> mejor fundada.** Dato en disco, una sesión.

---

# PARTE II · Formulaciones avanzadas y bordes

## 5 · Lo que el programa hace tiene nombre formal: **data fusion**

**Fuente:** Bareinboim & Pearl, *Causal inference and the data-fusion problem*, **PNAS** 113(27)
(2016), 7345-7352. **Clase (d1).**

Los generadores combinan β̂ de **ENCUCI 2020, ENIF 2024, ENVIPE, ENCIG 2023, ENIGH** —
poblaciones, años y diseños muestrales distintos— fusionados en un motor con agentes sintéticos.
**Eso es el problema de fusión de datos, y tiene aparato formal completo.**

**Claim 1 — selection diagrams:** representan **dónde difieren** las poblaciones fuente y
objetivo. Si difieren en la distribución de edad, un nodo `S` apunta a edad; si difieren en cómo
una variable depende de la edad, apunta a otro sitio; **un confusor no medido entre dos variables
impide la transportabilidad**.

**Claim 2 — y hay que leerlo dos veces:** existen criterios gráficos y algorítmicos para decidir
transportabilidad y fusión, procedimientos automáticos para extraer las fórmulas de transporte, y
**la garantía de que cuando el algoritmo falla, la fusión es inviable sin importar el tamaño de
muestra**.

**Consecuencia para el `0 de 15`:** puede que **parte del bloqueo no sea falta de dato ni falta de
enlace, sino inviabilidad de transporte** — y si es eso, **ninguna descarga lo arregla**. Es la
diferencia entre *"nos falta medir"* y *"esto no se puede fusionar"*, **y hoy el programa no las
distingue**.

> **RECOMENDACIÓN:** que `D-A` exija, para todo β̂ que venga de un instrumento distinto al de su
> desenlace, **declarar qué se supone invariante entre la población fuente y la población de
> agentes del motor**. Es el nodo `S` en prosa. **Sin eso, cada fusión es un supuesto no
> escrito.**

---

## 6 · La salida a `PENDIENTE` que el programa no usa: **identificación parcial**

**Fuente:** Manski, *Identification for Prediction and Decision* (Harvard UP, 2007) y trabajo
previo. **Clase (d1)/(d3).**

`D-A` es **binario**: un β̂ entra o no entra. Si no entra, el motor usa un valor **ASIGNADO** — un
punto **sin intervalo, sin datos, y sin representación de incertidumbre**.

**Manski lo nombra:** los investigadores, sabiendo que no pueden formar una estimación puntual
creíble, en vez de enfrentar la incertidumbre **cambian de objetivo** y se enfocan en otro
estimando que no es de interés sustantivo pero sí se puede estimar puntualmente: **sacrifican
relevancia por certeza**.

**Ley de credibilidad decreciente:** *la credibilidad de la inferencia decrece con la fuerza de
los supuestos mantenidos*.

**El punto sobre el diseño, y es fuerte:**

> **Un `ASIGNADO −0.35` sin intervalo es peor que un `[−0.35, +0.12]` derivado de datos.** El
> primero es un supuesto disfrazado de parámetro; el segundo dice honestamente lo que los datos
> permiten.

> **RECOMENDACIÓN ARQUITECTÓNICA:** que la casilla admita **tres estados, no dos** —
> **`IDENTIFICADO`** (punto) · **`ACOTADO`** (intervalo) · **`ASIGNADO`** (supuesto)— y que la
> simulación **propague el intervalo**. Nueve de los quince son `SIN-RUTA`; **casi todos
> admitirían cotas, aunque anchas**. Las cotas anchas ya sirven para descartar afirmaciones
> extremas, aunque no basten para decidir.
>
> **Eso convierte el `0 de 15` de un muro en un gradiente, sin relajar un solo criterio de
> `D-A`.**

⚠️ **A verificar antes de adoptarlo:** (a) qué tan **anchas** salen las cotas en aplicaciones
reales con datos observacionales de encuesta — si salen `[0,1]` siempre, la propuesta es inútil;
(b) si **propagar intervalos por un modelo generativo produce output interpretable**; (c) la
objeción de Imbens de que **reportar solo cotas descarta información disponible** bajo los
supuestos mantenidos.

---

# PARTE III · Marcas de mesa, decisión por decisión

**⚠️ Todas quedan sujetas a `RED-TEAM-A`.**

| Decisión | Marca de mesa |
|---|---|
| **`D-A`** | **Como está, con dos añadidos:** el quinto atributo de no-aplicabilidad estructural (§1) y la justificación gráfica del conjunto de ajuste (§3). **La cláusula de identificación causal como rótulo aparte queda tal cual** — alineada con E9(R1), que separa el estimando de su estimación. *Considerar además el nodo `S` de §5 y el estado `ACOTADO` de §6.* |
| **`D-B`** | **SÍ, sin reserva.** Si las θ llevan escala y normalización declaradas, sus β deben llevarlas también. **A-bis regla 3 aplicada consistentemente.** |
| **`D-C` · `confianza_institucional`** | **Adoptar** el enlace sobre la relación **condicional por edad**; la curva marginal de `X §5.2` **no se sella sola** (§4.2 la hace sospechosa de composición). **Añadir la escala del enlace** y, si es no colapsable, la frase de §2. |
| **`D-C` · `radio_confianza`** | **`PENDIENTE`, no "no paramétrica".** `X §5.1` no encontró forma. Declarar *"no paramétrica por nivel"* **es declarar una forma**, y una que **no puede entrar a un índice lineal `Σβ·θ`**. `PENDIENTE` es lo que el modelo mismo exige *"donde no hay evidencia"*. |
| **`D-C` · `familismo_apoyo`** | **`β(formalidad, urbanización)`, CON la reserva de §3.** `formalidad` es **el eje con más riesgo de mal control**. O se declara el grafo, o se rotula asociación condicional. |
| **`D-C` · `G4`** (`exposicion_violencia`, `confianza_institucional_justicia`) | **NÓMBRALOS.** Dejarlos fuera con una frase es lo peor de las dos opciones: **ya están MEDIDOS**, alguien los va a consumir, y **sin enlace nombrado los consumirá en la escala equivocada**. Es literalmente el defecto que A-bis regla 3 existe para prevenir. |
| **Taxonomía del censo** (`RUTA-A/I/C/SIN-RUTA`) | **Como el §1 del censo, sin cambios.** Ya está bien definida y se declaró inventada con condición de vigencia. |

---

# PARTE IV · Referencias

| # | Referencia | Clase | Claim usado |
|---|---|---|---|
| 1 | ICH E9(R1), *Addendum on Estimands and Sensitivity Analysis in Clinical Trials* (2019) | (d3) | Cinco atributos del estimando; el enlace como atributo definitorio |
| 2 | Greenland, Robins & Pearl (1999), *Confounding and Collapsibility in Causal Inference*, **Statistical Science** | (d1) | No-colapsabilidad; OR y HR no colapsables, RD y RR sí |
| 3 | Cinelli, Forney & Pearl (2024), *A Crash Course in Good and Bad Controls*, **Sociological Methods & Research** 53:1071-1104 | (d1)/(d2) | Sobrecontrol; puerta trasera; no todo post-tratamiento es mal control |
| 4 | MacCallum, Zhang, Preacher & Rucker (2002), *On the Practice of Dichotomization of Quantitative Variables*, **Psychological Methods** 7(1):19-40 | (d2) | Pérdida de señal; no linealidad borrada |
| 5 | Maxwell & Delaney (1993), *Bivariate median splits and spurious statistical significance*, **Psychological Bulletin** 113(1):181-190 | (d2) | Inflación de error tipo I en interacción |
| 6 | Vargha, Rudas, Delaney & Maxwell (1996) | (d2) | Ocurre aun dicotomizando **solo uno** de dos predictores |
| 7 | Bareinboim & Pearl (2016), *Causal inference and the data-fusion problem*, **PNAS** 113(27):7345-7352 | (d1) | Selection diagrams; inviabilidad de fusión independiente del `n` |
| 8 | Manski (2007), *Identification for Prediction and Decision*, Harvard UP | (d1)/(d3) | Ley de credibilidad decreciente; relevancia sacrificada por certeza |
| 9 | Sanabria-Pulido & Langbein (2025), *I'll Bribe You Because I Trust You*, **Public Integrity**, doi 10.1080/10999922.2025.2520710 | (d2) | Confianza generalizada ↑ solicitud de soborno; **excepción: policía**. *Ya sellado como tipo (3) en ADR-60(e)* |

**Ninguna verificada contra su fuente original desde el repo. Todas tipo (3).**

---

## Cierre · qué hacer con este documento

**No entra al canon como está.** Su función es doble:

1. **Ser el insumo de `RED-TEAM-A`**, que ataca primero los cuatro puntos de la Parte I y en
   particular las dos **inferencias de mesa** marcadas en §4.
2. **Alimentar la hoja `D-ABC`** — **después** del red team, no antes. Llenarla ahora es sellar en
   canon lo que se está auditando.

**Y el criterio de aterrizaje, sin excepción:** solo entra al repo lo que traiga **claim +
condiciones + qué cambiaría si el paper estuviera mal**. Una bibliografía sin eso **se ve como
rigor y no lo es**.
