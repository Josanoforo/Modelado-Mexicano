# Registro de descartes de las validaciones forenses
### 28 de julio de 2026 · cumplimiento de **ADR-29.b** y su adenda

> **Por qué existe este archivo.** ADR-29.b hace de los forenses **evidencia primaria del mismo rango que los reports**, y su adenda ordena que *"el validador rechaza un artefacto forense sin tabla de descartes, igual que rechaza un número sin procedencia"*. Auditados los cinco forenses el 28/jul, **tres no tienen tabla de descartes**. Este archivo registra el estado de cada uno y, donde el descarte es irrecuperable, **lo declara en vez de reconstruirlo**.
>
> **Por qué importa y no es burocracia.** El descarte es el único lugar donde vive el **sesgo de superviviente**. Un forense que solo publica los casos que analizó no permite distinguir *"ningún caso podía romper la regla"* de *"los que podían se filtraron antes del registro"*. Esa distinción es justamente la que el Hito C **no pudo hacer**, y la razón es PD-01: los 15 descartes del registro de apuestas se filtraron *por motivo declarado* como "aquellos donde la variable estructural era claramente decisiva" — es decir, **los candidatos más probables a falsar un generador** — y 14 de ellos nunca se escribieron.

---

## 1 · Estado de los cinco forenses

| # | Forense | Tabla de descartes | Estado |
|---|---|---|---|
| **V1** | `Apuestas_Conductuales_sobre_el_Consumidor_Mexicano` | ✅ **Sí** | Archivó sus descartes **por disciplina de autor**, no porque la plantilla lo exigiera. ⚠️ Hereda el caveat de que **V1 no pudo leer los documentos del proyecto** |
| **V2** | `Validación_Forense_del_Clientelismo_Electoral` | ❌ **No** | El vertical mejor construido del programa —único con identificación causal y único cuyas reglas ancla son **fieles al motor** (Hito 2)— y aun así **sin descartes archivados** |
| **V3** | `Consumo_Aspiracional__Validación_Forense` | ⚠️ **Mención sin tabla** | **No archivó ninguno.** Misma plantilla que V1; distinto resultado. La diferencia fue la disciplina del autor, no el proceso |
| **V4** | `Crédito_Popular__Morosidad_Auditada` | ❌ **No** | — |
| **V5** | `Crédito_Fácil_y_Sobreendeudamiento` (escaneo) | ❌ **No** | Es un escaneo de indicadores adelantados, no un estudio de casos: la exigencia de descartes le aplica **de forma atenuada** (ver §3) |

---

## 2 · Declaración: qué es recuperable y qué no

**No recuperable (se declara, no se reconstruye):**

- **PD-01 · los 14 descartes del registro de apuestas.** Nunca se escribieron. **NO RECONSTRUIR.** Reconstruirlos de memoria produciría exactamente el artefacto que este programa existe para evitar: una racionalización post-hoc con apariencia de registro.
- **Los descartes de V2, V3 y V4.** El criterio de selección de casos no quedó escrito en ninguno de los tres, y ninguno de sus autores está disponible para declararlo. **Reconstruir el criterio hoy sería inventarlo.**

**Consecuencia epistémica, que debe viajar con esos tres forenses:**

> Los veredictos de **V2, V3 y V4 no permiten descartar sesgo de superviviente.** Sus hallazgos siguen siendo válidos **sobre los casos que analizaron**; lo que **no** puede afirmarse es que sean representativos del universo de casos disponibles. En particular, **ninguno de los tres puede usarse para sostener que "no se encontró contraejemplo"** — solo que no se encontró **entre los casos que llegaron al análisis**.

Esta marca es del mismo rango que la marca de procedencia (a)/(b)/(c) y **viaja igual**: hasta el modelo, hasta la ficha y hasta cualquier corrida que los cite.

---

## 3 · Requisito de salida, hacia adelante *(ADR-32.b aplicado a forenses)*

**Todo forense nuevo incluye, en la estructura del report y no como anexo:**

| Campo obligatorio | Qué debe decir |
|---|---|
| **Universo considerado** | Cuántos casos se identificaron antes de filtrar |
| **Filtro aplicado** | El criterio, escrito **antes** de ver los resultados |
| **Tabla de descartes** | Un renglón por caso descartado, **con su motivo** |
| **Descartes por "estructura decisiva"** | Marcados **aparte**: son los candidatos más probables a falsar una regla, y filtrarlos sin registrarlos es el mecanismo exacto de PD-01 |
| **Pares contrafactuales buscados y no hallados** | El anti-superviviente del Bloque C exige buscarlos activamente; si no aparecieron, decirlo |

**El artefacto que falta visiblemente si no se cumple:** la tabla. Sin ella el forense **no se archiva como canónico**. *La plantilla ya se parchó el 27/jul (`prompts-verticales-validacion`, "TABLA DE DESCARTES — OBLIGATORIA"); este archivo cierra el lado retrospectivo.*

**Excepción acotada.** A los **escaneos de indicadores** (V5) no les aplica la tabla de descartes de casos, porque no seleccionan casos: seleccionan **indicadores**. Su requisito equivalente es declarar **qué indicadores se consideraron y se dejaron fuera, y por qué** — sobre todo los que apuntaban en dirección contraria a la tesis del escaneo.

---

## Módulo de auditoría de rigor extremo

**¿Qué confunde estructura con cultura?** Nada en este archivo hace afirmación conductual. El riesgo es otro: leer la ausencia de descartes como descuido individual de tres autores, cuando fue **un defecto de plantilla** — la misma plantilla produjo un archivador y un no-archivador.

**¿Qué sobregeneraliza desde clases medias urbanas?** Indirectamente, sí: los cinco forenses son de dominio financiero, de consumo y electoral, todos con datos que existen **porque hay mercado formal que los genera**. El México popular informal aparece como objeto, casi nunca como fuente. Un descarte no registrado en ese terreno es más grave, porque hay menos casos para empezar.

**¿Qué está sesgado por marcos o muestras extranjeras?** El concepto mismo de "sesgo de superviviente" es un marco importado **(c)** de la estadística financiera anglosajona. Es adecuado aquí, pero conviene decirlo.

**¿Qué cambiaría con foco rural, indígena o popular?** Mucho. El candidato falsador más fuerte del programa —**seguro agrícola, Fondos de Aseguramiento**— vive en el hueco declarado del corpus. Si los descartes de V4 (crédito popular) hubieran quedado escritos, es plausible que ese candidato hubiera aparecido antes.

**¿Qué parece psicológico y es incentivo racional?** Que V1 archivara y V3 no **no fue rasgo del autor**: fue que archivar tenía costo y no tenía requisito. Cambiado el requisito, cambia la conducta — que es la tesis del corpus aplicada al propio programa.

**¿Dónde hay evidencia débil e intuición fuerte?** En suponer que los descartes de V2/V3/V4 **habrían cambiado algo**. Es plausible y no está demostrado: puede que no hubiera casos descartados relevantes. **La ausencia de la tabla impide saberlo — y ese es precisamente el problema, no una conclusión sobre el resultado.**

**¿Qué sería peligroso mal usado?** Dos lecturas opuestas e igual de malas: (a) *"V2, V3 y V4 no valen"* — sí valen, sobre los casos que analizaron, y V2 es el mejor trabajo del programa; (b) *"ya se registró, entonces está resuelto"* — no lo está: los descartes siguen sin existir y **la marca de sesgo de superviviente es permanente**, no se levanta escribiendo este archivo.
