# ESTADO DEL PROGRAMA · Psicología del Mexicano Contemporáneo
### `estado` · **v1.8** · 29 de julio de 2026 · **ÚNICA FUENTE DE ESTADO**

> | | |
> |---|---|
> | **ARCHIVO** | `estado-programa-v1.8.md` |
> | **REEMPLAZA A** | `estado-programa-v1_7.md` — **borrar** |
> | **VERIFICAS ASÍ** | §0 lista `modelo` en **v3.2** y `hitoD-R1.1` · §7 registra el pre-registro en **24 de 27**, no en 27 de 27 |
> | **NOMBRE ESTABLE** | **`estado`** — cítalo así, **nunca por nombre de archivo** |

---

## 0 · Nomenclatura del programa *(ADR-36)*

```
<nombre-estable>-v<MAYOR>.<MENOR>.md
```
⚠️ **La plataforma convierte el punto en guion bajo al subir** (`...-v3.0.md` → `...-v3_0.md`). Es cosmético y no rompe nada: **cítalos siempre por nombre estable**, nunca por nombre de archivo.
**MAYOR** = estructura o alcance · **MENOR** = contenido.

| Nombre estable | Archivo vigente | Qué es |
|---|---|---|
| **`modelo`** | `modelo-decision-v3.2.md` | CANÓNICO OPERATIVO. **Se pega íntegro** en las corridas verticales |
| **`glosario`** | `glosario-v5.6.md` | CANÓNICO. Único punto legítimo de entrada de un tier |
| **`gobernanza`** | `gobernanza-v1.6.md` | 36 ADR, protocolo de cambio |
| **`estado`** | `estado-programa-v1.1.md` | Este archivo |
| **`milpa-whitepaper`** | `milpa-whitepaper-v0.1.md` | El **porqué** del simulador |
| **`milpa-spec`** | `milpa-spec-v0.2.md` | El **cómo** — incluye el gate de ADR-25/37 |
| **`milpa-plan`** | `milpa-plan-v0.1.md` | El **cuándo** |
| **`hitoD-preregistro`** | `hitoD-preregistro-v2.0.md` | **Falsadores pre-registrados.** Append-only una vez escrito un bloque |
| **`hitoD-R1.1`** | `hitoD-R1.1-veredicto-v1.0.md` | Veredicto forense · append-only |
| **`prompts-verticales`** | `prompts-verticales-validacion.md` | Operativo *(sin versionar aún)* |

**Serie MILPA:** se lee en orden `milpa-whitepaper` → `milpa-spec` → `milpa-plan`. ⚠️ **El orden vive en el cuerpo de los tres, no en el nombre** *(ADR-36.c)*: el `01/02/03` anterior lo codificaba en el archivo y se perdió al renombrar uno solo.

**Regla que sostiene el esquema:** las referencias internas citan el **nombre estable** (*"ver `modelo §3.B`"*), **nunca el nombre de archivo**. Así se puede subir versión indefinidamente sin dejar referencias colgando.

**Append-only, nunca se versionan:** los 31 reports, los 5 forenses y los artefactos forenses de proceso (`hito2`, `hitoC`, `corrida-refutaciones`, `lectura-cuatro-pivotes`, `barrido-propagacion-forense`, `descartes-forenses-registro`). Son evidencia fechada; reescribirlos es racionalización post-hoc.

**Cuántos archivos toca un cambio típico:** una regla, un tier o un conteo → **solo `modelo`**. Un tier leído de un report → `modelo` + `glosario`. Una decisión de proceso → + `gobernanza`. Cierre de sesión → + `estado`.

> **v1.1 — 28/jul.** Se añade §0 (nomenclatura, ADR-36) y se retira la ficha del inventario. **Sustituye y reemplaza a `CHECKPOINT-v2.md`, `mapa-y-roadmap.md` e `inventario-corpus.md`, ya borrados.**
>
> **Por qué se fusionan.** Los tres describían el estado del programa y **ninguno describía el estado del programa**: el CHECKPOINT se escribió a media sesión y quedó congelado antes del Hito C; `mapa-y-roadmap`, fechado el mismo día, tenía **cero menciones** de modelo v2, glosario v5, ADR-30, Hito C ni de la corrida de refutaciones; `inventario-corpus` declaraba 57 archivos y no mencionaba ninguno de los ocho artefactos de la última sesión. Cuatro cifras del mismo objeto circulaban a la vez —57, ~59, 61— y dos conteos de reports —30 y 31—.
>
> **Tres fuentes de estado es deriva, no redundancia.** La regla de la casa —*duplicar la fuente de verdad es el defecto*— aplica al estado igual que a los ADR.
>
> **v1.8 — 29/jul.** Auditoría de perímetro de la suite de verificación (`tests/check.py`). Cuatro cambios: (1) **§7 se corrige** — el pre-registro del Hito D cubre **24 de 27**, no 27 de 27, y el dominio `§3.3` del motor no tiene ficha alguna; (2) se cierra en §4·S2 una deuda abierta desde antes de ADR-37 — el perímetro **no está en duda**, es 27 y cuadra exacto contra el motor real; (3) entra en §4·S1 lo que sí queda vivo: **nada vigila el vocabulario de tier dentro del motor**, solo en `corpus/reports/`; (4) entra en §4·S2 el perímetro real de T07–T10, con el defecto de `integrador:174` (la marca de procedencia no viaja con el tier). La suite corre completa: **18 FAIL · 107 WARN**. Fuentes: `forense/notas/2026-07-29-perimetro-suite-T07-T10.md` y su verificación `forense/notas/2026-07-29-b-correccion-perimetro.md`, que **retira** la ambigüedad 20/27 planteada como hipótesis de trabajo y registra qué cifras de la primera nota no se reprodujeron.

---

## 1 · Inventario verificado

**56 archivos**, verificados el 28/jul/2026 por `diff` entre el índice del proyecto y el montaje de disco (sin discrepancias).

| Bloque | Cuenta | Notas |
|---|---|---|
| **Reports temáticos** | **31** | CANÓNICO, evidencia primaria. *Se decía 30: conteo de memoria* |
| **Validaciones forenses** | **5** | CANÓNICO por ADR-29.b |
| Gobierno y estado | 3 | `instrucciones-proyecto-v2` · `gobernanza-programa` v1.2 · **este archivo** |
| Síntesis y modelo | **3** | `glosario` v5.5 · `integrador` · `modelo` v3.0 **(absorbe la ficha)** |
| Forenses de proceso | **6** | `hito2-modelo-fantasma` · `hitoC-prueba-generadores` · `corrida-refutaciones` · `lectura-cuatro-pivotes` · `descartes-forenses-registro` · `barrido-propagacion-forense` |
| Auditorías y red team | 4 | `meta-auditoria-comunicacion` · `red-team-cuatro-verticales` · `verificacion-red-team-vs-corpus` · `curaduria-archivos` |
| Ejecutable (MILPA) | 6 | `milpa-whitepaper` · `milpa-spec` · `milpa-plan` + 3 YAML |
| Operativo | 1 | `prompts-verticales-validacion` |

**Borrados el 28/jul:** `ficha-canonica-modelo.md` *(ADR-36.b — absorbida en `modelo`)* · `CHECKPOINT-v2.md` · `mapa-y-roadmap.md` · `inventario-corpus.md` (fusionados aquí) · `ADR-30.md` (ya incorporado a gobernanza §4 — y además contenía la versión **superada**: retiraba `familismo` de G3, decisión revertida en mesa).

⚠️ **Los forenses de proceso NO se actualizan.** `hito2-modelo-fantasma`, `hitoC-prueba-generadores`, `corrida-refutaciones`, `lectura-cuatro-pivotes` y `curaduria-archivos` conservan los conteos que tenían el 27/jul (14 coeficientes, 42 reglas, 107 números). **Es deliberado:** son registros fechados de lo que se encontró ese día. Reescribir un registro forense para que cuadre con el estado posterior es precisamente la racionalización post-hoc que el Bloque C prohíbe. Se leen como historia, no como estado.

⚠️ **El índice del proyecto y el montaje de disco se han desincronizado dos veces.** Si un archivo no aparece, **"no lo veo" ≠ "no está"**: pedirlo o esperar, nunca concluir que falta.

---

## 2 · El estado real, en una frase

**El modelo es hoy una síntesis rigurosa de literatura con tiers leídos, no un artefacto validado** — y desde el 28/jul, además, un artefacto **sin deuda documental**: las cuatro capas de la cadena están sincronizadas entre sí y verificadas contra el archivo, no contra el registro.

Eso no lo invalida: un tier derivado de lectura disciplinada es evidencia legítima. Pero la diferencia importa mucho cuando alguien lo use para decidir algo caro.

---

## 3 · Estado por estrato

**L1 · Evidencia — completa.** 31 reports + 5 forenses. Sesgo declarado: sobre-muestreo del clasemediero urbano formal, sub-muestreo del popular informal (el peso demográfico dominante). El sistema indígena-comunal vivo queda **fuera por diseño**, no como hueco.

**L2 · Síntesis — completa.** Glosario v5.1 autocontenido (único punto legítimo de entrada de un tier) + integrador. La junta L1→L2 quedó reparada el 28/jul: los tres casos de corrección que no habían vuelto a la fuente ya están parchados **en el report dueño**, con nota fechada.

**L3 · Modelo — completo, y ya sin capa derivada. `modelo` v3.0: 49 reglas, 6 perfiles, 7 generadores, 144 números.** La ficha derivada **se eliminó** (ADR-36.b): perdía 4 reglas `[FUERTE]` y degradaba una, y era el mecanismo del Hito 2. **Una sección no se puede desincronizar de su propio documento.**

**L4 · Implementación — incompleta.** MILPA Fase 0: **3 de 10** `rules/*.yaml` (solo `tramite.yaml` es de dominio). **18 de 43 reglas implementadas**, sin criterio registrado de por qué esas. `masterclass-mexico.html` ausente. **Fase 1 POSPUESTA por decisión, no por olvido.**

**L5 · Validación — el estrato más problemático.** Una prueba de falsación pre-registrada corrida (veredicto **B**). 49 refutaciones corridas: 27 pasan, 3 fallan, 8 sin objeto, 11 requieren el ejecutable. **15 coeficientes, cero medidos.** Cuatro generadores sin falsar.

**L0 · Gobierno — completo y al día.** 32 ADR, protocolo de cambio con retropropagación bidireccional, severidades S1-S5, casillero de pendientes irresueltos.

---

## 4 · Deudas abiertas, por severidad

### S1 · Grande, sin resolver
- **Cero datos primarios propios.** Deuda del programa, no de ningún report.
- **PD-01 · 14 descartes irrecuperables.** Nunca se escribieron. **NO RECONSTRUIR.**
- **Vocabulario de tier del motor: 7 etiquetas donde el canónico define 4, y nada lo vigila.** Conteo real de `§3.B` (salida de T12, `tests/check.py` sobre HEAD `9301e59`): `20 [FUERTE] · 19 [MEDIA] · 5 [MEDIA-FUERTE] · 2 [HIPÓTESIS] · 1 [FUERTE como correlación] · 1 [FUERTE / MEDIA] · 1 [MEDIA / HIPÓTESIS]` = 49 reglas. Las cuatro primeras son el canónico (glosario, y el `CANONICO` de T07); las tres últimas son compuestas. **T07 solo vigila el vocabulario de `corpus/reports/`, nunca el del motor** — no hay registro de si las tres compuestas son extensión sancionada del vocabulario de 4 o deriva sin documentar, y **nada haría ruido si apareciera una cuarta**. Decisión pendiente, no tomada aquí. ⚠️ *Esto **no** implica ambigüedad de perímetro: ver §4·S2, cerrado.* *(`forense/notas/2026-07-29-b-correccion-perimetro.md §1, §3`)*

### S2 · Bloquean trabajo futuro
- ✅ ~~ADR-25, backtest mal especificado~~ — **CERRADO el 28/jul (ADR-37)**, el S2 más antiguo del programa. El gate pasa de **una** condición a **tres**: reproducción · **prueba de mecanismo** (apagar `riesgo_fiscal_percibido` debe colapsar la brecha ≥70%) · **anti-confusión** (apagar el canal debe dejarla persistir). **Desbloquea `R3.4`.** ⚠️ Los umbrales de B y C son **ASIGNADOS**; calibrar contra series de SPEI antes de Fase 1. ⚠️ **Límite declarado:** el gate no separa **coerción de fricción**.
- **`civico.voto.clientelar` compilaba una cifra de laboratorio como campo** — `p: 0.63` de Ascencio-Chang con tier `FUERTE`. Degradada a `MEDIA`; campo **`procedencia_p`** obligatorio en toda regla. **Nadie había aplicado a las probabilidades de regla la disciplina que `procedencia.yaml` aplica a los parámetros.**
- **Los 90 parámetros de dispersión de ADR-28.d** no existen en archivo. Mientras falten, el check de varianza intraperfil de `modelo §1.2` **no puede correr**. Requisito de salida en `procedencia.yaml`.
- **Los 30 componentes de `confianza_institucional` por perfil**: el vector está declarado (ADR-28.b) y **sin poblar**.
- ⭐ **El pre-registro del Hito D cubre 24 de 27, y `§3.3` no tiene un solo falsador.** `hitoD-preregistro` v2.0 tiene **24 fichas** (encabezados `## R`, de `R1.1` a `R10.3`): 18 `[FUERTE]` + 4 `[MEDIA-FUERTE]` + 1 `[FUERTE como correlación]` + 1 `[FUERTE / MEDIA]`. **Faltan 3: dos `[FUERTE]` y una `[MEDIA-FUERTE]`.** No existe ningún encabezado `R3.x` — **el dominio `§3.3` del motor (autoridad, trámite y relación con el Estado) quedó entero fuera del pre-registro**. `R3.4` se nombra en el cuerpo pero **no tiene ficha**, pese a que ADR-37 la declaró desbloqueada el 28/jul. ⚠️ **Por qué pesa más que un conteo:** `§3.3` es donde vive `riesgo_fiscal_percibido`, el disparador del que depende el gate de Fase 1. **El dominio que sostiene el gate es el único sin falsadores, y tres artefactos lo daban por cubierto** — `hitoD-preregistro:8` (*"contiene 27 fichas"*), `:13` (*"27 de 27"*) y este archivo en su v1.7 §7. Corregido aquí; los otros dos son append-only y no se tocan. *(`forense/notas/2026-07-29-b-correccion-perimetro.md §4`)*
- ✅ ~~**Decisión de alcance del Hito D** sin registrar: ¿20 reglas `[FUERTE]` puras, o 26 incluyendo las 4 `[MEDIA-FUERTE]` y las 2 híbridas?~~ — **CERRADO, `gobernanza:266` (ADR-37, 28/jul):** perímetro = **27** (20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas; eran 26 hasta que ADR-33 partió protesta/autodefensa en dos). Las **2 compuestas** son `[FUERTE como correlación]` y `[FUERTE / MEDIA]` —así las nombra `hitoD-preregistro:17`, y así aparecen en las fichas de `R1.4` y `R4.3`—; `[MEDIA / HIPÓTESIS]` queda fuera. 20+5+1+1 = **27**, exacto contra el motor real (T12). **Esta entrada llevaba abierta desde antes de ADR-37 y nunca se cerró aquí — era deuda documental, no sustantiva.**
- **8 refutaciones sin objeto** — incluida `ref.A.02`, la única `MUY_FUERTE` de las 49 (2,207 h/año, el mayor de la OCDE). El modelo no tiene variable de esfuerzo, colorismo, salud mental ni entidad prestamista. **Ampliar el modelo o declarar el alcance y retirarlas.**
- **T07–T10 solo ven `corpus/reports/*.md`.** No cubren `canon/`, `corpus/forense/`, `forense/` ni `milpa/`. Ampliar **T09** a esos directorios **no añade señal**: los disparos nuevos son mención crítica o falso positivo por co-ocurrencia, **cero usos causales**. Ampliar **T10** sí encuentra algo real en `integrador-psicologia-mexicano.md`: **4 defectos de medida del propio T10** —el integrador marca la procedencia de diáspora con convenciones locales (`[Fuerte, con caveat US]`, `Caveat US:`, `muestras US-hispanas`) que el patrón literal de T10, `(b)`/"diáspora", no reconoce— y **1 defecto real del integrador**: `integrador:174` presenta a Arciniega 2008, Castillo 2010 y Wheeler 2010 como *"Evidencia a favor. **Sólido**"* sin marca de procedencia, mientras el caveat que las declara población latina en EE.UU. vive en `integrador:175`, bajo *"Evidencia en contra / límites"* — la sección opuesta. **El tier se asigna sin la marca; la marca llega como limitación.** *(Las dos líneas leídas textualmente.)* **Decisión pendiente, no tomada aquí:** ¿se amplía el patrón de T10 para reconocer las convenciones locales del integrador, o el integrador adopta el marcador formal `(b)` de `modelo §0.1`? ⚠️ **Los conteos de disparos de la nota original (66/45/5) no se reprodujeron** (65/57/14 al recomputar); no citarlos como verificados. El análisis cualitativo sí está verificado. *(`forense/notas/2026-07-29-perimetro-suite-T07-T10.md §3`; `…-b-correccion-perimetro.md §5, §6`)*

### S3 · Sustantivas
- **15 coeficientes de generador nunca validados.** Único punto calibrable hoy: `G3 → horizonte_temporal` vía **panel rotativo ENOE** — sería el primer MEDIDO de 144.
- **48 de 49 reglas sin prueba de falsación pre-registrada.**
- **74 números ASIGNADOS sin calibrar.**
- **8 reports entraron a la síntesis vía glosario v2 (superado)**, no leídos a fondo.
- **26 reglas fuera de la implementación**, sin criterio registrado.
- **3 de 5 forenses sin tabla de descartes** → ver `descartes-forenses-registro.md`.
- ⚠️ **El motor sigue SIN ENTIDAD PRESTAMISTA** *(frontera declarada de ADR-35)*. Modela al decisor, no al oferente: el hallazgo mejor sostenido del corpus sobre crédito —*el riesgo vive en el fondeo del prestamista, no en el deudor* (Famsa, Crédito Real; n=2)— **no puede representarse**, y su refutación sigue **sin objeto**.
- **T03 (`tests/check.py`) produce 41 WARN, no 44** — verificado hoy. El total de WARN de la suite es **107**, no 110. La diferencia no tiene artefacto que la respalde y no se puede reconstruir. *(`forense/notas/2026-07-29-perimetro-suite-T07-T10.md §6`)*

### S5 · Pendientes irresueltos (no disparan propagación, tienen casillero)
- **conf.02** · policronía: Trabajo y Tiempo refutan el mismo mito con **mecanismos opuestos**.
- **conf.05** · consumo compensatorio: Fuerte (consumidor) vs. Hipótesis (salud). **No promediar.**
- **conf.06** ⭐ · **ninguna cifra de confianza interpersonal es usable.** Cinco en circulación; dos dicen ser la **misma ENCUCI 2020 con 10.3 puntos de diferencia**.
- **Instrumento de conf.04:** la escalera de Cantril mide **evaluación vital, no alegría**. *(La contradicción alegría/malestar quedó resuelta por ADR-27 como artefacto de agregación.)*

### Huecos de dato (ausencia de mundo, no deuda técnica)
Panel D/E de consumo popular · elasticidades · granularidad municipal · control por origen social en pigmentocracia · pragmática en lenguas indígenas · **tabulado ENA 2017 + AMUCSS 2014** (cerrarían el candidato falsador del seguro agrícola) · **ENIF 2024** (la prueba de falsación usó la ola 2018).

---

## 5 · Reglas que no se negocian

- **Los tiers se LEEN** del glosario v5.1 y de los mapas de evidencia. **No se reconstruyen.** Si un tier no está a la vista, ir a buscarlo antes de afirmarlo.
- **Las reglas se CITAN TEXTUALMENTE** de `modelo v2.1 §3.B`, con tier, dominio y perfiles. Sin cita, es propuesta nueva y su veredicto **no cuenta como validación**.
- **Marcar procedencia:** (a) dato EN México · (b) muestra de diáspora · (c) marco importado. **La marca VIAJA hasta la ficha.**
- **Segmentar siempre.** Una afirmación sobre "el mexicano" es señal de alarma.
- **Hallar que la psicología NO importó es un resultado VÁLIDO.**
- **Descartar con rigor es entregable.** Archivar los descartes (ADR-29.b).
- **Consolidar PRIMERO, borrar DESPUÉS.** Al revés se pierde.
- **Todo principio nuevo nace con su artefacto de salida** (ADR-32). Si no falta visiblemente cuando no se cumple, no obliga a nada.
- **Español.**

---

## 6 · Trampas de este momento

- **El v2 tiene MÁS parámetros asignados que el v1** (familia partida, vector de confianza, distribuciones). Eso es superficie nueva en un modelo cuyo defecto documentado es la infalsabilidad. **Lo que lo hace defendible son los tests que corren solos** (28.c, 28.d, 30) — y **28.d hoy no puede correr** porque le faltan los 90 parámetros de dispersión. Sin esos tests, esta versión empeora el problema en vez de arreglarlo.
- **Ninguna salida con decimales.** 60 de 144 números son ordinales cardinalizados; 74 asignados. La aritmética conserva orden, **no magnitud**.
- **V1 (vertical de consumo) no pudo leer los documentos del proyecto.** Todo lo que dependa de V1 hereda ese caveat.
- **Las corridas verticales anteriores al 28/jul usaron una ficha incompleta.** Si una corrida tocaba **Familia y pareja**, la **tanda** o el **puente personal** y reportó que la regla no existía, el hueco estaba en la ficha, no en el motor. **Sus veredictos sobre esos dominios no transfieren.**
- **El patrón que explica casi todos los fallos del programa:** principio declarado **sin requisito de salida**. Codificado como ADR-32.

---

## 7 · Qué sigue

**HITO D — falsación sistemática. Perímetro DECIDIDO: 27 reglas** = 20 `[FUERTE]` + 5 `[MEDIA-FUERTE]` + 2 compuestas. *(El motor tiene **47 reglas** desde v2.4.)*

⚠️ **Antes del Hito D se corrió el `barrido-propagacion-forense`.** De los **22 veredictos ROMPE/MATIZA** de los cinco forenses, **6 nunca habían bajado al motor** y 3 llegaron a medias — tasa de fuga **~41%** en la capa que ADR-29.b considera evidencia primaria. Tres se aterrizaron en v2.4 (**P-01** bandwidth tax, **P-02** condiciones de cesión de la agencia, **P-03** turnout vs. vote-choice). **Los seis quedaron aterrizados**: P-01/02/03 en v2.4; **P-04/05/06 en v2.5, con ampliación de alcance decidida (ADR-35)** — el motor gana dos reglas de crédito y una prohibición dura, y pasa a **49 reglas**.

**⚠️ Paso 1 INCOMPLETO — `hitoD-preregistro` v2.0 cubre 24 de las 27 del perímetro.** *(Corregido el 29/jul: la v1.7 de este archivo decía "cubre las 27", repitiendo la autodeclaración del propio pre-registro en `:8` y `:13`. El conteo de encabezados `## R` da **24**.)* Las 24 traen falsador, umbral y veredictos A/B/C/D, **con cero búsquedas** — eso se sostiene. **Faltan 3 fichas: dos `[FUERTE]` y una `[MEDIA-FUERTE]`, y son todo `§3.3`** (autoridad, trámite y Estado), incluida `R3.4`, que se nombra en el cuerpo sin ficha propia. Ver §4·S2.

**Seis defectos de redacción detectados sin buscar nada** — todos de la familia de ADR-33, `PORQUE` que no sostiene su `ENTONCES`:

| # | Regla | Defecto |
|---|---|---|
| **D-01** | R1.2 | ✅ **CORREGIDO en `modelo` v3.1.** El `PORQUE` de **capacidad** (*"permite"*) pasa a mecanismo: *el ingreso estable baja el costo esperado de comprometerse a largo plazo* |
| **D-02** | R4.2, R5.2 | ⏸️ **NO se toca: es el blanco.** `PORQUE` mezcla driver **(b)** de diáspora con driver **(a)** estructural, bajo tier `[FUERTE]`. Sus falsadores separan los dos drivers |
| **D-03** | R2.2, R10.2 | ⏸️ **NO se toca: es el blanco.** La fuerza vive en **una palabra** — *"SOLO"* legitima, *"destruye"* capital social. **Corregirlas ahora sería mover el blanco después de apuntar** |
| **D-04** | R4.1, R9.1 | ✅ **CORREGIDO en v3.1.** *"Adaptación racional"* queda acotada con su prueba: **si el acceso mejora, la conducta debe moverse**. ⚠️ Los dos veredictos se registran **juntos**: si ambas fallan por el mismo lado no son dos refutaciones, **son una**, y el comodín está en todo el motor |
| **D-05** | R7.1 | ✅ **CORREGIDO en v3.1.** Reformulada contra **peso percibido**; las cifras (59.8% presidencial, >85% abstención judicial) bajan a **instancias**. Ahora es comprobable con elecciones locales concurrentes vs. no concurrentes |
| **D-06** | R8.3 | Depende de `conf.06`, abierto. **Ningún veredicto apoyado en esas cifras cuenta** |

**Ocho de 27 pre-registradas como probables `D`** (inejecutables): R1.4 · R2.1 · R2.2 · R7.4/R7.5 · R8.2 · R8.3 · R10.2 · R10.3. Las agrupa: dato organizacional **propietario**, **huecos de dato ya declarados** (panel D/E, conf.06) y **un límite ético** (R10.3: preguntar por disposición a testificar en zona de violencia activa expone a quien responde — `D` es preferible).

**Dos posiblemente ya falsadas** por evidencia que el corpus contiene: **R1.3** (Nu, 15M sin puente, rural = urbano) y **R1.4** (G2 contestado en D/E). Declarado **antes** de buscar.

~~**Una bloqueada:** R3.4~~ — ✅ **desbloqueada el 28/jul por ADR-37.** Su umbral es ahora el criterio de tres condiciones del gate. ⚠️ **Desbloqueada no es pre-registrada:** `R3.4` sigue **sin ficha** en `hitoD-preregistro` v2.0 (§4·S2).

⚠️ **Esto es el Paso 1. Ninguna regla ha sido probada todavía.** Los 27 umbrales son **ASIGNADOS**, juicio propio, no leídos de ningún report. Un revisor puede moverlos con argumento; **lo que no se vale es moverlos después de ver el resultado**.

**Paso 2 — EN CURSO. 1 de 27 corrida.**

**`R1.1` → veredicto `D` (inejecutable).** El candidato falsador más fuerte de todo el programa. Y `D` **no por hueco de dato: por hueco de mercado.**
- El **Seguro Agrícola Catastrófico**, que cubre al productor de temporal, **NO PUEDE SER CONTRATADO POR LOS PRODUCTORES** (SADER, textual). El productor aporta ~**2.5%** de la prima (80.7 de 3,262.2 mdp).
- Los **Fondos de Aseguramiento**, que sí son voluntarios y plurianuales, concentran **62% de fondos y 66% de cobertura en Sonora-Sinaloa-Tamaulipas**: riego, tecnificado, gran extensión. **No es la población de volatilidad máxima.**
- Donde hay adopción voluntaria en pequeños, está **atada al financiamiento** — AMUCSS: *"si no es porque el seguro se vuelve una obligación al obtener financiamiento, no existe la demanda"*. **Es el confusor pre-registrado, textual.**
- **Cero de seis candidatos** sobrevivieron al confusor. Tabla de descartes en `hitoD-R1.1`.

⚠️ **La ausencia de seguro voluntario en temporal NO cuenta como apoyo a R1.1** — está confundida con exclusión de mercado por partida triple. **Leerla como horizonte corto sería la confusión estructura-por-cultura en su forma más pura.** R1.1 **sale igual que entró**.

⚠️ **Lección del pre-registro:** el veredicto lo decidió **el confusor escrito antes de buscar**, no el umbral —que nunca llegó a evaluarse—. Sin esa cláusula, los **10.2 millones de hectáreas** aseguradas del SAC habrían parecido un contraejemplo espectacular y habrían refutado la regla **por un artefacto**.

⚠️ **Sobre el hueco rural-popular:** el brief decía que el mejor candidato vive ahí y que *"no es casualidad"*. Correcto, pero el mecanismo es otro: **no es solo que el corpus no muestree ahí — es que el mercado tampoco.** Las dos ausencias tienen la misma raíz, y por eso **el hueco no se cierra leyendo más**: se cierra con dato primario propio, la deuda S1 del programa.

**Siguiente en el orden, por valor informativo y no por facilidad:** R3.2 (ENCIG tiene serie) · R5.1 (Pensión del Bienestar como choque exógeno) · R7.2 (ENVIPE, trae su propio vuelco).

**HITO F · MILPA Fase 1 — POSPUESTO por decisión.**

---

**Suite de verificación (`tests/check.py`) — auditoría de perímetro, 29/jul.** La suite corre completa: **18 FAIL · 107 WARN**. Según la nota del 29/jul, el desglose por test se reprodujo de forma independiente en Windows 11/Python 3.14 contra la corrida original en contenedor Linux. `CONTRIBUTING.md` tenía un byte UTF-8 truncado (pos 2149) que rompía T03 con `UnicodeDecodeError` antes del final de la corrida; corregido en `09bfb05`.

**Lo que la auditoría movió:** se corrigió §7 (el pre-registro cubre **24 de 27**, y `§3.3` no tiene ficha alguna — §4·S2); se cerró una deuda abierta desde antes de ADR-37 (el perímetro **es 27**, sin ambigüedad — §4·S2); quedan abiertos que **T07 no vigila el vocabulario de tier del motor** (§4·S1) y la disyuntiva de **T10 vs. la convención de procedencia del integrador** (§4·S2).

⚠️ **Al usar la nota del 29/jul:** su análisis cualitativo está verificado, pero **sus conteos de disparos de T10 (66/45/5) no se reprodujeron** y una cita suya a `curaduria-archivos.md:23` no checa contra el archivo. Detalle en `forense/notas/2026-07-29-b-correccion-perimetro.md §5–§6`.
