# Hito C · La prueba de generadores
### ¿Qué caso del registro habría ROTO cada generador y cada coeficiente?

*27 de julio de 2026. Leídos: `modelo §2` (seis generadores con sus cláusulas falsables verbatim), `procedencia.yaml` (los 14 coeficientes), y los 16 casos conservados del registro de apuestas. Cero investigación nueva.*

---

## Método y límites pre-registrados

La prueba es simple de enunciar: por cada generador y cada coeficiente, recorrer los 16 casos y preguntar **cuál de ellos, de haber salido distinto, lo habría refutado**. Si ningún caso podía romperlo, el generador está **sin falsar en la práctica**, por más cláusula `falsable` que traiga escrita.

**Tres límites, declarados antes de correr y no después:**

1. **Dominio.** El registro se auto-declara *"VÁLIDO para el dominio financiero, HIPÓTESIS para los demás"*. Su §7 admite sobre-representación de fintech.
2. **Filtro no auditable.** Los 15 casos descartados eran, por motivo declarado, aquellos donde *"la variable estructural era claramente decisiva"* — es decir, **los candidatos más probables a refutar un generador psicológico**. Se filtraron sin archivarse (PD-01). Por tanto esta prueba **no puede distinguir** "ningún caso podía romper G*n*" de "los casos que podían se eliminaron antes de que existiera el registro".
3. **La diana estaba puesta.** `procedencia.yaml` pre-registró qué debía encontrarse: *"los generadores tienen el signo bien sostenido por el corpus y la magnitud sin sostener. Esto es lo que hace posible que un generador explique cualquier cosa si se le mueve el coeficiente — el riesgo de infalsabilidad que las instrucciones v2 marcan y que la prueba de generadores debe atacar."*

---

## Resultado en una frase

> **Ninguna de las seis cláusulas falsables especifica una condición que un caso del registro pudiera haber producido.** Y cuando un caso **sí** contradijo un generador, la cláusula estaba escrita de modo que el caso no podía contar.

Eso es peor que "infalsable por falta de material". Es **infalsable por diseño de la cláusula**.

---

## 1 · El defecto de nivel de análisis

Puestas juntas, las seis cláusulas revelan un patrón que por separado no se ve:

| Gen | Cláusula falsable (verbatim, abreviada) | ¿Qué exige? | ¿Alcanzable por un caso? |
|---|---|---|---|
| **G1** | *"si la confianza generalizada subiera por encima de ~30% y la impunidad cayera por debajo de ~80%…"* | Cambio **nacional** de confianza e impunidad | ❌ Ninguna empresa mueve eso |
| **G2** | *"si la movilidad ascendente mejorara…"* | Cambio **estructural** de movilidad social | ❌ |
| **G3** | *"con empleo formal e ingreso estable, los mismos sujetos ahorran… (ya observado)"* | Observación a nivel de sujeto | ✅ **Sí** |
| **G4** | *"si la cifra negra bajara por debajo de ~80%…"* | Cambio **nacional** de impunidad | ❌ |
| **G5** | *"con un Sistema Nacional de Cuidados y pensiones suficientes…"* | Que exista una **institución que no existe** | ❌ |
| **G6** | *"la autoridad autoritaria produce peor desempeño (ya observado)"* | Observación organizacional | ✅ **Sí** |

**Cuatro de seis cláusulas son contrafácticos macro-sociales.** No son "falsables pero aún no probadas": están escritas de forma que **solo la historia puede probarlas**. Un registro de apuestas empresariales no opera a ese nivel y nunca podrá.

**Y las dos que sí son de nivel-caso dicen "ya observado".** Una cláusula que declara la observación confirmatoria no está especificando un falsador: está describiendo corroboración. G3 enuncia lo que el generador **predice** (con ingreso estable, la gente ahorra), no lo que lo **refutaría** (sujetos con ingreso estable que no ahorran). La forma lógica está invertida.

---

## 2 · Generador por generador

### G1 · Baja confianza institucional + confianza radial — **CONTRADICHO, pero la cláusula no lo registra**

**¿Qué caso lo habría roto?** Uno de adopción masiva **sin puente personal** en entorno de baja confianza. Eso rompería el mecanismo de difusión que G1 postula.

**Ese caso está en el registro. Dos veces.**

- **Caso 2 · Nu México** — 15 millones de clientes, **sin sucursales**, 58% de adopción multiproducto **igual en zonas rurales y urbanas**, 78% de la base fuera de grandes urbes. Sin puente personal, sin presencia física, sin recomendación como canal. El propio registro dictamina: *"la difusión **no fue por 'confianza'** sino por utilidad y fricción baja"*.
- **Caso 3 · Kueski / Aplazo** — aprobación en segundos vía datos alternativos, 20 millones de préstamos, 50,000+ comercios. Cero mediación personal.

**Pero la cláusula de G1 exige que la confianza generalizada nacional supere el 30% y la impunidad baje del 80%.** Ninguna de esas cosas pasó, así que **por la letra de su cláusula G1 sigue intacto** — mientras dos casos de su propio registro contradicen su mecanismo.

**Esto es la infalsabilidad en su forma más exacta: la cláusula protege al generador de su mejor contraejemplo.**

⚠️ El corpus ya lo sabía a medias: **ADR-20** desdobló *adopción por canal de confianza personal* `[FUERTE]` de *confianza radial como canal de difusión* `[HIPÓTESIS]`. Pero **G1 en `§2` sigue empaquetando ambas**, y su cláusula falsable sigue siendo la de la versión empaquetada. La corrección llegó al ADR y al glosario; **no llegó al generador**. Es el cuarto caso del defecto de propagación.

> **Veredicto G1: CONTRADICHO a nivel de mecanismo por los Casos 2 y 3. Cláusula DEFECTUOSA — hay que reescribirla al nivel donde el generador opera.**

### G2 · Desigualdad + baja movilidad — **CONTESTADO, y el registro no lo leyó así**

**¿Qué caso lo habría roto?** Un segmento con movilidad bloqueada que **no** señaliza estatus, donde manda otra cosa.

**Caso 5 · Bodega Aurrera / Mamá Lucha.** Segmentos C/D/E — el extremo de movilidad bloqueada. El registro dictamina que el supuesto era *"CORRECTO pero no aislado"* y que **matiza que el precio SÍ manda en este segmento**.

Ese matiz es un falsador parcial de G2 en D/E, y **el registro lo anotó como confirmación**. Aguas abajo, ADR-15 degradó *"calidad y dignidad > precio"* a NO VALIDADA y V1 rompió el consumo compensatorio *"como driver decisivo aislado"*. El glosario v5 lo deja segmentado: la refutación de *"solo busca lo barato"* **se sostiene para A/B/C+ y se retira para D/E, donde gana el precio.**

Es decir: **el registro tenía en la mano el caso que acota G2 y lo clasificó como que lo confirmaba.** El potencial falsador existía y no se ejerció.

> **Veredicto G2: CONTESTADO en D/E por el Caso 5, leído como confirmación. La cláusula (movilidad nacional) sigue sin poder probarse.**

### G3 · Informalidad + volatilidad de ingreso — **PROBADO Y SOBREVIVE. El único resultado limpio**

**¿Qué caso lo habría roto?** Uno donde el ingreso se estabilizara y el horizonte **no** se alargara.

**Caso 6 · Progresa/Oportunidades.** Diseño **aleatorizado** — el propio registro lo llama *"el caso metodológicamente más limpio"*. Al estabilizar el ingreso: +14% de consumo del hogar, +11% de gasto en alimentos, mejoras en talla y matrícula. La conducta cambió en la dirección predicha.

**Ese caso pudo haber salido al revés y no salió.** Es la única falsación genuina de toda la prueba: un generador expuesto a refutación en un diseño limpio, que la resistió.

⚠️ **Con dos acotaciones que no hay que perder.** La prueba es **parcial**: CEPAL (2016) documenta impacto *"limitado y poco significativo"* en movilidad ocupacional intergeneracional. G3 queda confirmado en **conducta intermedia**, no en efecto estructural. Y confirma el **signo**, no la magnitud (ver §3).

> **Veredicto G3: FALSABLE Y FALSADO SIN ROMPERSE. Único generador con prueba real.**

### G4 · Exposición a violencia + impunidad — **CERO CASOS**

**¿Qué caso lo habría roto?** Uno donde exposición alta a violencia **no** produjera conducta defensiva, o donde la conducta defensiva apareciera sin violencia.

**Ninguno de los 16 casos toca violencia como variable.** Ni uno. El registro es de apuestas comerciales sobre consumo y crédito; la violencia no entra en su dominio.

Y su cláusula exige que la cifra negra baje del 80%. Está en **93.2%**.

> **Veredicto G4: INFALSABLE con este material. Cero casos aplicables y cláusula macro-social.**

### G5 · Familismo como seguro — **CERO CASOS, y la cláusula exige un mundo inexistente**

**¿Qué caso lo habría roto?** Uno donde el hogar dispusiera de alternativa institucional y **aun así** hiciera pooling familiar — o al revés.

**Ninguno de los 16 lo toca.** El Caso 5 menciona *"mujeres jefas de compra del hogar"*, pero eso es segmentación de mercado, no una prueba del familismo como seguro.

Y la cláusula exige *"un Sistema Nacional de Cuidados y pensiones suficientes"*. El report de vejez documenta que el Sistema está en **parálisis legislativa**. **La cláusula condiciona la falsación a una institución que no existe.**

> **Veredicto G5: INFALSABLE. Es el caso más nítido de cláusula escrita contra un contrafáctico inalcanzable.**

### G6 · Jerarquía + indulgencia — **DOS CASOS ADYACENTES, NINGUNO PROBATORIO**

**¿Qué caso lo habría roto?** Uno donde la autoridad autoritaria no-benévola produjera **buen** desempeño y satisfacción.

Dos casos rozan el terreno y ninguno concluye:

- **Caso 16 · Susana Distancia** — el registro lo declara **INDETERMINADO**: *"no hay métrica conductual limpia"*, y lo registra como ilustrativo del autócrata benévolo.
- **Caso 10 · Tecate** — masculinidad y jerarquía, pero **[ILUSTRATIVO]**, sin métricas de venta atribuibles.

> **Veredicto G6: INFALSABLE en la práctica. Los dos casos disponibles son no probatorios por decisión del propio registro.**

---

## 3 · Los 14 coeficientes: **0 de 14**

Aquí el resultado es limpio y no admite matiz.

| Gen | Coeficientes | ¿Algún caso pudo romperlo? |
|---|---|---|
| G1 | `confianza_institucional −0.60` · `radio_confianza −0.35` | ❌ |
| G2 | `sens_estatus 0.55` · `aversion_riesgo 0.20` | ❌ |
| G3 | `horizonte_temporal −0.60` · `aversion_riesgo 0.40` · `familismo 0.20` | ❌ |
| G4 | `exposicion_violencia 0.70` · `confianza_institucional −0.40` · `horizonte_temporal −0.20` · `sens_estatus −0.15` | ❌ |
| G5 | `familismo 0.50` · `radio_confianza 0.15` | ❌ |
| G6 | `deferencia 0.45` | ❌ |

**Ninguno de los 16 casos podía tocar ninguna magnitud**, y la razón es estructural, no de muestra. Un coeficiente es una **elasticidad**: exige observar a los **mismos sujetos** antes y después de un cambio en la capa estructural, y medir la **tasa** de cambio de disposición. El registro reporta **desenlaces** —adopción, escala, fracaso—, no tasas.

`procedencia.yaml` ya lo había diagnosticado con precisión: *"un coeficiente es una ELASTICIDAD, y el corpus es transversal — da estados, no ritmos. Ninguna de las fuentes citadas publica elasticidades. **No existían para ser citadas.**"*

**El único caso con el diseño correcto es el 6 (Progresa):** aleatorizado, mismos hogares, cambio de ingreso, medición antes/después. Y **aun así no calibra nada**, porque sus salidas son efectos sobre consumo (+14%, +11%), no sobre el parámetro de disposición `horizonte_temporal`. Confirma el **signo**. La magnitud queda intacta.

**Convergencia que vale registrar:** `procedencia.yaml` señala `G3 → horizonte_temporal` como *"la única elasticidad del modelo que México permite estimar con dato público"*, vía el panel rotativo de la ENOE (mismo hogar, cinco trimestres, cruzando formal↔informal). Y de forma independiente, el único caso del registro con el diseño adecuado prueba **ese mismo generador**. Dos rutas distintas apuntan al mismo punto de calibración. **Es por donde hay que empezar.**

---

## 4 · Tabla de resultados

| | Cláusula falsable | ¿Caso capaz de romperlo? | Veredicto |
|---|---|---|---|
| **G1** | Macro-social (inalcanzable) | **Sí — Casos 2 y 3, y lo contradicen** | ⚠️ **Contradicho; cláusula defectuosa** |
| **G2** | Macro-social (inalcanzable) | Sí — Caso 5, leído como confirmación | ⚠️ **Contestado en D/E** |
| **G3** | Nivel-sujeto ✅ | **Sí — Caso 6, aleatorizado** | ✅ **Probado y sobrevive** |
| **G4** | Macro-social (inalcanzable) | **No — cero casos** | ❌ **Infalsable** |
| **G5** | Institución inexistente | **No — cero casos** | ❌ **Infalsable** |
| **G6** | Nivel-organización ✅ | No — dos casos, ambos no probatorios | ❌ **Infalsable en la práctica** |
| **14 coefs** | — | **No — 0 de 14** | ❌ **Intocados** |

**Uno de seis generadores tiene una prueba real. Cero de catorce coeficientes.**

Y la restricción que traíamos —*"solo G1, G2 y G3 son falsables con este material"*— resultó **medio correcta**: G1 y G2 sí tienen casos con capacidad falsadora, pero **sus cláusulas están escritas de modo que esos casos no cuentan**. Que G4, G5 y G6 salgan infalsables es el resultado esperado; que G1 esté contradicho por su propio registro **sin que la cláusula lo registre** no lo era.

---

## 5 · Qué hacer

1. **Reescribir las seis cláusulas al nivel donde el generador opera.** Una cláusula falsable de un generador que se usa para predecir conducta debe poder refutarse con **conducta observable**, no con un cambio de régimen nacional. Regla de redacción: *si la cláusula solo puede probarla la historia, no es una cláusula falsable — es una predicción histórica.*
2. **Desdoblar G1 en el motor**, como ADR-20 ya hizo en el glosario: adopción individual por canal de confianza `[FUERTE]` vs. difusión por confianza radial `[HIPÓTESIS]`. Los Casos 2 y 3 refutan la segunda, no la primera. Hoy el generador no permite distinguirlo.
3. **Reabrir el Caso 5 contra G2.** Fue leído como confirmación y contiene un falsador parcial para D/E. Es lectura, no investigación.
4. **Calibrar `G3 → horizonte_temporal` con el panel ENOE.** Dos rutas independientes lo señalan como el único punto calibrable. Sería el **primer coeficiente medido** de los 107 números.
5. **Marcar G4, G5 y G6 como `SIN FALSAR` en el modelo**, con la razón. No es un demérito: es información que quien use el modelo necesita.
6. **No re-correr esta prueba con el mismo registro.** El techo no es de esfuerzo: es que el material no opera al nivel de las cláusulas.

---

## Módulo de auditoría de rigor extremo

**¿Qué parte confunde pobreza, desigualdad o informalidad con "cultura"?** No aplica directamente. Pero el hallazgo de G2 va en esa dirección: si en D/E manda el precio y no la señalización de estatus, entonces parte de lo que G2 atribuye a un generador psicológico es **restricción presupuestal**. Es la pregunta que el Caso 5 dejó abierta.

**¿Qué sobregeneraliza desde clases medias urbanas?** El registro entero. Su §7 lo admite: sobre-representa fintech, que es el dominio donde el usuario es más bancarizable, más urbano y más digital. Los generadores más expuestos a ese sesgo son G1 y G2 — justo los dos con veredicto contradicho/contestado.

**¿Qué está sesgado por marcos o muestras extranjeras?** Nada aquí: los 16 casos son de organizaciones operando en México sobre población en México. Es de lo más limpio del corpus en procedencia.

**¿Qué cambiaría con foco rural, indígena o popular?** G5 dejaría de ser infalsable por falta de casos: el familismo como seguro es directamente observable en corresidencia y cuidado, y el report de vejez tiene los datos (82% de hogares con adultos mayores nucleares/ampliados; brecha de cuidado de 21.5 h/sem). **El problema no es que G5 sea infalsable — es que el registro mira al lugar equivocado.**

**¿Qué parece psicológico pero es estructura?** El resultado de G3, si se lee mal. Progresa confirma que **al estabilizar el ingreso cambia la conducta** — lo cual es tanto una victoria del generador como una demostración de que el driver es estructural. G3 es el generador que mejor sobrevive **y** el que más claramente dice que lo que manda es el entorno.

**¿Dónde hay evidencia débil e intuición fuerte?** En dos lugares. **(1)** Leer el Caso 2 (Nu) como contradicción de G1: Nu opera sobre recomendación boca a boca que no aparece en las métricas públicas, así que "sin puente personal" es inferencia mía desde la ausencia de sucursales, no un dato. **(2)** Clasificar el Caso 5 como falsador parcial de G2 contradice la lectura del propio registro. Ambas son lecturas defendibles y las marco como tales, no como hechos.

**¿Qué conclusión sería peligrosa mal usada?** Que "los generadores no sirven". El signo de los seis está **bien sostenido por el corpus** — eso lo dice `procedencia.yaml` y esta prueba no lo toca. Lo que queda demostrado es más estrecho y más útil: **el aparato de falsación de los generadores no funciona**, porque sus cláusulas están escritas al nivel equivocado. Un generador con signo sostenido y cláusula inservible sigue siendo una hipótesis útil; lo que no es, todavía, es una hipótesis puesta a prueba.
