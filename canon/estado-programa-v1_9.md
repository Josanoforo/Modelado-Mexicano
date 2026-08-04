# ESTADO DEL PROGRAMA · Psicología del Mexicano Contemporáneo
### `estado` · **v1.9** · 29 de julio de 2026 · **ÚNICA FUENTE DE ESTADO**

> | | |
> |---|---|
> | **ARCHIVO** | `estado-programa-v1.9.md` |
> | **REEMPLAZA A** | `estado-programa-v1.8.md` — **borrar** |
> | **VERIFICAS ASÍ** | §0 lista `modelo` en **v3.4** y `hitoD-R1.1` · §4·S2 trae la declaración canónica de cobertura del pre-registro (cifra derivada, no tecleada) y el rótulo corregido del perímetro (20+1+1+5, no 20+5+2) · §7 no repite la cifra, cita §4·S2 · las tres poblaciones de "prueba de falsación" (Hito D, Hito C, ejercicio de glosario) se citan siempre con etiqueta (ADR-45, D-05) |
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
| **`modelo`** | `modelo-decision-v4.0.md` | CANÓNICO OPERATIVO. **Se pega íntegro** en las corridas verticales |
| **`glosario`** | `glosario-v5.6.md` | CANÓNICO. Único punto legítimo de entrada de un tier |
| **`gobernanza`** | `gobernanza-v1.15.md` | 54 ADR, protocolo de cambio |
| **`estado`** | `estado-programa-v1.9.md` | Este archivo |
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
> **v1.8 — 29/jul.** Auditoría de perímetro de la suite de verificación (`tests/check.py`). Cuatro cambios: (1) **§7 se corrige** — el pre-registro del Hito D cubre **24 de 27**, no 27 de 27, y el dominio `§3.3` del motor no tiene ficha alguna; (2) se cierra en §4·S2 una deuda abierta desde antes de ADR-37 — el perímetro **no está en duda**, es 27 y cuadra exacto contra el motor real; (3) entra en §4·S1 lo que sí queda vivo: **nada vigila el vocabulario de tier dentro del motor**, solo en `corpus/reports/`; (4) entra en §4·S2 el perímetro real de T07–T10, con el defecto de `integrador:174` (la marca de procedencia no viaja con el tier). La suite corre completa: **18 FAIL · 107 WARN** *(cifra vigente esa misma mañana del 29/jul: `TRANSFER-maestra-7/8.md` aún no entraban al árbol y la normalización de T03 de `26e7ef4` era horas después — no se toca aquí, es historia correcta cuando se escribió; ver §7, cierre de este archivo, para la cifra de hoy)*. Fuentes: `forense/notas/2026-07-29-perimetro-suite-T07-T10.md` y su verificación `forense/notas/2026-07-29-b-correccion-perimetro.md`, que **retira** la ambigüedad 20/27 planteada como hipótesis de trabajo y registra qué cifras de la primera nota no se reprodujeron.

---

## 1 · Inventario verificado

**59 archivos**, verificados el 28/jul/2026 por `diff` entre el índice del proyecto y el montaje de disco (sin discrepancias). ⚠️ **Corregido 29/jul/2026:** decía 56; es la suma de la propia tabla de abajo (31+5+3+3+6+4+6+1), nunca recalculada tras escribirse. *(`censo-integridad-v1_0.md` C1-01.)*

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

**L4 · Implementación — incompleta.** MILPA Fase 0: **3 de 10** `rules/*.yaml` (solo `tramite.yaml` es de dominio). **18 de 43 reglas implementadas**, sin criterio registrado de por qué esas. `masterclass-mexico.html` ausente. **Fase 1 ya NO está pospuesta: es la arquitectura objetivo del programa, calibrada por AJUSTE, no por identificación causal (ADR-50); la subidentificación bajo atributos persiste, calibrabilidad de los libres sin reactivo retirada (ADR-51).** *(Corregido 3/ago/2026, ADR-51: decía "Fase 1 POSPUESTA por decisión, no por olvido" — ADR-50 (31/jul/2026) ya había cambiado ese estado y declaró la cascada a esta línea pendiente, sin ejecutarla; ADR-51 la ejecuta.)*

**L5 · Validación — el estrato más problemático.** **Hito D** (reglas del motor; perímetro de 27, subconjunto de las 49 del motor): **3 de 27 corridas archivadas** — `R1.1` → veredicto `D`, `R3.2` → veredicto `B`, `R7.2` → veredicto `D` (bloque append-only de `hitoD-preregistro`, ver §7). 49 refutaciones narrativas corridas *(población distinta, `milpa/refutations.yaml`, ref.A.*)*: 27 pasan, 3 fallan, 8 sin objeto, 11 requieren el ejecutable. **15 coeficientes, cero medidos.** Cuatro generadores sin falsar (**Hito C**, distinto de lo anterior — ver `hitoC-prueba-generadores`).

**P3 · LCA de segmentación sobre ENIGH (población distinta de Hito D/Hito C — un pre-registro propio, `p3-lca-preregistro-v1_0.md`).** **Veredicto D5 — INESTABLE** (`forense/notas/2026-08-04-p3-lca-segmentacion.md`, adenda de cierre; ADR-53). No es victoria de ninguna hipótesis: los seis descriptores de `modelo` §1.1.D siguen sin respaldo estructural y sin refutar, y `§1.1.D` **no se toca**. **D6 (gradiente sin clases) se descarta con razón escrita**: la forma de la curva de BIC del ajuste principal (monótona decreciente, mínimo en `k=8`) es congruente con D6, pero la sensibilidad S1 (solo indicadores de persona) produce un mínimo interior en `k=4` — con solución no estable — que basta para que el descenso monótono deje de leerse como gradiente limpio; ver ADR-53 para las cifras re-derivadas y el límite declarado. **LCA multinivel: HABILITADO, no corrido** (tres condiciones en ADR-53 y en `p3-lca-preregistro-v1_0.md` §2.5). No mueve `8 de 14`, `4 de 144` ni ningún contador del Hito D.

**L0 · Gobierno — completo y al día.** 54 ADR, protocolo de cambio con retropropagación bidireccional, severidades S1-S5, casillero de pendientes irresueltos. *(Corregido 29/jul/2026: decía 32, contradiciendo §0 de este mismo archivo — `censo-integridad-v1_0.md` C1-02. Subió a 39 en la misma sesión, con la aprobación de ADR-38/39 en `gobernanza §4`; a 40 después, con ADR-40, misma sesión de tests; a 41 después, con ADR-41, misma sesión; a 43 después, con ADR-42/43, misma sesión; a 44 después, con ADR-44, sesión de canon del 30/jul (publicación del repositorio sin ADR previo); a 45 después, con ADR-45, misma sesión (vocabulario de "prueba de falsación", cierra D-05); a 46 después, con ADR-46, sesión distinta el mismo día (unidad de contaminación es la sesión, no la máquina, corrige `forense/hallazgos-congelados-2026-07-30.yaml` E-03); a 47 después, con ADR-47, misma fecha (falsar una regla ≠ calibrar un coeficiente, cierra `forense/hallazgos-congelados-2026-07-30.yaml` D-09/D-10); a 48 después, con ADR-48, misma fecha (R0 congela el aparato de auditoría); a 49 después, con ADR-49, 31/jul/2026 (tres decisiones de mesa: retira `unico_calibrable_hoy`, sella la clase `AJUSTADO`, G1a homogeneidad de pendientes declarada); a 50 después, con ADR-50, 31/jul/2026, misma fecha (el motor se calibra por AJUSTE, no por identificación causal; MILPA Fase 1 deja de estar POSPUESTA; 29 libres del ajuste = 14 probabilidades sin ruta + 15 coeficientes); a 51 después, con ADR-51, 3/ago/2026 (ADR-50 SE REESCRIBE: sobrevive el ajuste y MILPA como arquitectura objetivo, se retira la calibrabilidad de los libres sin reactivo; **corrige 29→22 grados de libertad reales del ajuste** (7+15, no 14+15 — las 13 reglas de `asignados_probabilidad` suman 1.0 cada una); registra M2/M3 con veredicto de C; cierra `D-12`); a 52 después, con ADR-52, 4/ago/2026 (dos decisiones de mesa en un acto: reparto de las 14 sella "búsqueda abierta"/"búsqueda cerrada"; `G1a` nombra su componente, `confianza_institucional[financiera]`, no se desdobla); a 53 después, con ADR-53, 4/ago/2026 (sella el veredicto D5-INESTABLE de P3, descarta D6 con razón escrita, habilita sin correr el LCA multinivel condicional de `p3-lca-preregistro-v1_0.md` §2.5); a 54 después, con ADR-54, 4/ago/2026 (`sens_estatus` sale de "búsqueda abierta" y cierra en "búsqueda cerrada (límite de régimen)", vía el precedente de `aversion_riesgo` en ADR-52 A, fundado en el examen de descriptor de `PR #64`).)*

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
- ⭐ **DECLARACIÓN CANÓNICA DE COBERTURA (§4·S2).** `hitoD-preregistro` tiene **25 fichas** — conteo real de encabezados `## R`, derivado con `grep -c "^## R" forense/hitoD-preregistro-v2_0.md` el 29/jul/2026, no copiado de ningún documento — de un perímetro de **27** (`gobernanza:276`, Registro de decisión ADR-37: 20+1+1+5, verificado además contra el motor real por T12; no es cifra asignada, tiene fuente). Desglose por tier, también derivado de los propios encabezados y no tecleado a mano: **19 `[FUERTE]` + 4 `[MEDIA-FUERTE]` + 1 `[FUERTE como correlación]` + 1 `[FUERTE / MEDIA]`**. **Faltan 2, ambas de `§3.3`** (autoridad, trámite y relación con el Estado): `R3.1` `[FUERTE]` y `R3.4` `[MEDIA-FUERTE]` — el gate de Fase 1. `R3.2`, la tercera regla del dominio, ya tiene ficha (`hitoD-preregistro` Nota 4, commit `b28b144`, 29/jul/2026); `R3.3` es `[MEDIA]`, fuera del perímetro, y nunca le faltó ficha. `R3.4` se nombra en el cuerpo pero **no tiene ficha**, pese a que ADR-37 la declaró desbloqueada el 28/jul. ⚠️ **Por qué pesa más que un conteo:** `§3.3` es donde vive `riesgo_fiscal_percibido`, el disparador del que depende el gate de Fase 1. **Esta línea es la fuente única de esta cifra en todo el documento — `§7` y la cabecera `VERIFICAS ASÍ` la citan, no la repiten.** *(`forense/notas/2026-07-29-b-correccion-perimetro.md §4`; consolidado 29/jul/2026.)*
- ✅ ~~**Decisión de alcance del Hito D** sin registrar: ¿20 reglas `[FUERTE]` puras, o 26 incluyendo las 4 `[MEDIA-FUERTE]` y las 2 híbridas?~~ — **CERRADO, `gobernanza:266` (ADR-37, 28/jul):** perímetro = **27** (20 `[FUERTE]` + 1 `[FUERTE como correlación]` + 1 compuesta `[FUERTE / MEDIA]` + 5 `[MEDIA-FUERTE]`; eran 26 hasta que ADR-33 partió protesta/autodefensa en dos). ⚠️ **Corrección de RÓTULO, 29/jul/2026:** solo `R4.3` (`[FUERTE / MEDIA]`) es compuesta —su ficha en `hitoD-preregistro` lo declara "dos falsadores, uno por mitad"—; `R1.4` es tier `[FUERTE como correlación]`, distinto de una compuesta, con un solo falsador contra la correlación. La entrada anterior llamaba a las dos "2 compuestas"; el mismo rótulo se corrige en `gobernanza §4` y `modelo §7` (cambio 34). `[MEDIA / HIPÓTESIS]` sigue fuera. 20+1+1+5 = **27**, exacto contra el motor real (T12). **El perímetro no cambia — es corrección de rótulo, no de alcance. Esta entrada llevaba abierta desde antes de ADR-37 y nunca se cerró aquí — era deuda documental, no sustantiva.**
- **8 refutaciones sin objeto** — incluida `ref.A.02`, la única `MUY_FUERTE` de las 49 (2,207 h/año, el mayor de la OCDE). El modelo no tiene variable de esfuerzo, colorismo, salud mental ni entidad prestamista. **Ampliar el modelo o declarar el alcance y retirarlas.**
- **T07–T10 solo ven `corpus/reports/*.md`.** No cubren `canon/`, `corpus/forense/`, `forense/` ni `milpa/`. Ampliar **T09** a esos directorios **no añade señal**: los disparos nuevos son mención crítica o falso positivo por co-ocurrencia, **cero usos causales**. Ampliar **T10** sí encuentra algo real en `integrador-psicologia-mexicano.md`: **4 defectos de medida del propio T10** —el integrador marca la procedencia de diáspora con convenciones locales (`[Fuerte, con caveat US]`, `Caveat US:`, `muestras US-hispanas`) que el patrón literal de T10, `(b)`/"diáspora", no reconoce— y **1 defecto real del integrador**: `integrador:174` presenta a Arciniega 2008, Castillo 2010 y Wheeler 2010 como *"Evidencia a favor. **Sólido**"* sin marca de procedencia, mientras el caveat que las declara población latina en EE.UU. vive en `integrador:175`, bajo *"Evidencia en contra / límites"* — la sección opuesta. **El tier se asigna sin la marca; la marca llega como limitación.** *(Las dos líneas leídas textualmente.)* **Decisión pendiente, no tomada aquí:** ¿se amplía el patrón de T10 para reconocer las convenciones locales del integrador, o el integrador adopta el marcador formal `(b)` de `modelo §0.1`? ⚠️ **Los conteos de disparos de la nota original (66/45/5) no se reprodujeron** (65/57/14 al recomputar); no citarlos como verificados. El análisis cualitativo sí está verificado. *(`forense/notas/2026-07-29-perimetro-suite-T07-T10.md §3`; `…-b-correccion-perimetro.md §5, §6`)*

### S3 · Sustantivas
- **15 coeficientes de generador nunca validados. Ninguno con ruta de calibración hoy** — `unico_calibrable_hoy` se retiró (ADR-49, D1): la vía ENOE no identifica conducta financiera (`forense/hallazgos.md`, 31/jul/2026).
- **46 de 49 reglas del motor sin prueba de falsación pre-registrada corrida** (3 corridas archivadas: `R1.1` → `D`, `R3.2` → `B`, `R7.2` → `D`). **Dentro del perímetro decidido del Hito D (27 reglas, subconjunto de las 49): 24 de 27 sin corrida.**
- **74 números ASIGNADOS sin calibrar.**
- **8 reports entraron a la síntesis vía glosario v2 (superado)**, no leídos a fondo.
- **25 reglas fuera de la implementación** (43−18), sin criterio registrado. *(Corregido 29/jul/2026: decía 26, no cuadraba contra el propio 18 de 43 de `§3·L4` — `censo-integridad-v1_0.md` C1-03. El "43" en sí sigue sin sustento localizable en el repo, NO-VERIFICABLE — no se toca aquí.)*
- **3 de 5 forenses sin tabla de descartes** → ver `descartes-forenses-registro.md`.
- ⚠️ **El motor sigue SIN ENTIDAD PRESTAMISTA** *(frontera declarada de ADR-35)*. Modela al decisor, no al oferente: el hallazgo mejor sostenido del corpus sobre crédito —*el riesgo vive en el fondeo del prestamista, no en el deudor* (Famsa, Crédito Real; n=2)— **no puede representarse**, y su refutación sigue **sin objeto**.
- **T03 (`tests/check.py`) produce hoy 18 WARN; el total de WARN de la suite es 84.** *(Corregido 29/jul/2026, `python3 tests/check.py` sobre HEAD vigente — `censo-integridad-v1_0.md` C1-07. Decía "41, no 44... total 107, no 110", cifra que a su vez ya estaba superada el mismo 29/jul por la fusión de `TRANSFER-maestra-7/8.md`. Y, en contra de lo que decía esta misma línea, la diferencia **sí tiene artefacto que la respalda**: el commit `26e7ef4` bajó T03 a 23; esta misma sesión de correcciones lo bajó más — 3 nombres nuevos en `HISTORICOS` (Paso 2) y la corrección del propio §2 de `gobernanza`, que dejó de citar en backticks los nombres viejos que estaba corrigiendo (Paso 3 ejecutado) — hasta 17. Cada bajada queda con su commit y su comando; ninguna es un número tecleado sin origen. Sesión de la subida a `instrucciones-proyecto-v2.md` v2.2: el renombre de `gobernanza` a v1_10 subió T03 a 18 (una cita fechada en `forense/censo-integridad-v1_0.md` a `gobernanza-v1_9.md` pasó a colgante); añadir `renombr` al regex de palabras-disparo de T03 (Cambio 6) la bajó a 16 — dos citas fechadas de renombre que antes no calificaban para la exención. Sesión de cierre del gate T17 (30/jul): aterrizar `forense/historico/TRANSFER-maestra-9.md` verbatim subió T03 de 16 a 18 — el propio TRANSFER-9 cita, entre backticks y a modo de ejemplo, los mismos fragmentos `-v3.2.md`/`-v3_2.md` que este párrafo ya documenta como falso positivo conocido; mismo patrón, bucket propio en `tests/baseline.json`. Refreeze tras el merge del PR #1 (30/jul): `revision-publicacion-2026-07-30.md` entra a `main` citando 3 veces, entre backticks y como propuesta de su FASE 5, el artefacto LICENSE-CORPUS que su propia Nota de reconciliación declara descartado (D-05) — T03 sube de 18 a 21; patrón I-01 (el test no distingue mención de referencia), bucket propio en `tests/baseline.json`. `python3 tests/check.py` corrido antes y después de cada fix, todos los conteos derivados, ninguno tecleado.)* *(30/jul/2026, ADR-48 · R0: la marca `{cita-ilustrativa}` de T03 baja el test de 21 a 18 — las tres citas de `LICENSE-CORPUS.md` en `revision-publicacion-2026-07-30.md`, que eran el caso 2 de I-01 —, y con ello el total de la suite de 87 a 84. Derivado de `python3 tests/check.py` en la sesión que congela la cola; FAIL no se mueve.)*
- **De las 7 cifras que esta ronda de correcciones tecleó a mano, 4 ya se derivan solas: T14/T15/T16 en `tests/check.py` (sesión de tests, 29/jul/2026) cubren el inventario de §1, el conteo de ADR y el estado FAIL/WARN de esta misma sección, con prueba negativa cada uno. Quedan 3 sin test, con diagnóstico — no como pendiente genérico, sino como hallazgo puntual de cada uno:**
  - **`procedencia.yaml` (14→15 coeficientes de generador):** mecanizable con un regex sobre el propio archivo (sumar las entradas de `detalle:`), sin salir de la librería estándar — no implementado en esta sesión, no porque sea difícil sino porque no se pidió.
  - **`milpa-plan` (9→15 parámetros base):** no es un conteo de archivos ni de ADR — es consistencia numérica entre 4 documentos (`glosario §13`, `modelo §0/§2.2`, `procedencia.yaml`, `milpa-plan`), el mismo molde que **T06** ya usa para Gini y confianza interpersonal. Candidato natural a extender T06, no a inventar un test nuevo.
  - **"25 reglas fuera de la implementación" (43−18, arriba):** **esto no es un test pendiente.** El "43" no tiene fuente independiente en ningún archivo del repo (NO-VERIFICABLE desde `censo-integridad-v1_0.md` C1-04) — un test que solo verificara `43−18=25` certificaría que la resta es correcta sobre un número que no está anclado a nada. El hallazgo real es que **43 no tiene origen**, no que falte automatizar la resta; automatizarla no lo arregla.

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

**HITO D — falsación sistemática. Perímetro DECIDIDO: 27 reglas** = 20 `[FUERTE]` + 1 `[FUERTE como correlación]` + 1 compuesta `[FUERTE / MEDIA]` + 5 `[MEDIA-FUERTE]`. *(El motor tiene **49 reglas**, no 47. ⚠️ **Corregido 29/jul/2026:** "47" era la cuenta del motor en v2.4, antes de que v2.5 sumara 2 reglas de crédito por ADR-35 (P-04/P-05 del barrido); este mismo archivo ya dice 49 en `§4·S1`, y el motor real (`modelo §7`, T12) confirma 49. La cifra vieja había quedado congelada de una versión anterior de esta sección.)*

⚠️ **Antes del Hito D se corrió el `barrido-propagacion-forense`.** De los **22 veredictos ROMPE/MATIZA** de los cinco forenses, **6 nunca habían bajado al motor** y 3 llegaron a medias — tasa de fuga **~41%** en la capa que ADR-29.b considera evidencia primaria. Tres se aterrizaron en v2.4 (**P-01** bandwidth tax, **P-02** condiciones de cesión de la agencia, **P-03** turnout vs. vote-choice). **Los seis quedaron aterrizados**: P-01/02/03 en v2.4; **P-04/05/06 en v2.5, con ampliación de alcance decidida (ADR-35)** — el motor gana dos reglas de crédito y una prohibición dura, y pasa a **49 reglas**.

**⚠️ Paso 1 INCOMPLETO.** Cobertura del pre-registro de `hitoD-preregistro`: ver **declaración canónica en §4·S2** (arriba) — no se repite aquí el conteo ni el detalle de qué falta, para que no haya dos fuentes de la misma cifra en este documento.

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

**Paso 2 — EN CURSO. 3 de 27 corridas.**

**`R1.1` → veredicto `D` (inejecutable).** El candidato falsador más fuerte de todo el programa. Y `D` **no por hueco de dato: por hueco de mercado.**
- El **Seguro Agrícola Catastrófico**, que cubre al productor de temporal, **NO PUEDE SER CONTRATADO POR LOS PRODUCTORES** (SADER, textual). El productor aporta ~**2.5%** de la prima (80.7 de 3,262.2 mdp).
- Los **Fondos de Aseguramiento**, que sí son voluntarios y plurianuales, concentran **62% de fondos y 66% de cobertura en Sonora-Sinaloa-Tamaulipas**: riego, tecnificado, gran extensión. **No es la población de volatilidad máxima.**
- Donde hay adopción voluntaria en pequeños, está **atada al financiamiento** — AMUCSS: *"si no es porque el seguro se vuelve una obligación al obtener financiamiento, no existe la demanda"*. **Es el confusor pre-registrado, textual.**
- **Cero de seis candidatos** sobrevivieron al confusor. Tabla de descartes en `hitoD-R1.1`.

⚠️ **La ausencia de seguro voluntario en temporal NO cuenta como apoyo a R1.1** — está confundida con exclusión de mercado por partida triple. **Leerla como horizonte corto sería la confusión estructura-por-cultura en su forma más pura.** R1.1 **sale igual que entró**.

⚠️ **Lección del pre-registro:** el veredicto lo decidió **el confusor escrito antes de buscar**, no el umbral —que nunca llegó a evaluarse—. Sin esa cláusula, los **10.2 millones de hectáreas** aseguradas del SAC habrían parecido un contraejemplo espectacular y habrían refutado la regla **por un artefacto**.

⚠️ **Sobre el hueco rural-popular:** el brief decía que el mejor candidato vive ahí y que *"no es casualidad"*. Correcto, pero el mecanismo es otro: **no es solo que el corpus no muestree ahí — es que el mercado tampoco.** Las dos ausencias tienen la misma raíz, y por eso **el hueco no se cierra leyendo más**: se cierra con dato primario propio, la deuda S1 del programa.

**`R7.2` → veredicto `D` (inejecutable como está especificada).** `[FUERTE]`, ENVIPE 2025 (`TMod_Vic`). No por hueco de dato: `BP2_1` ("Vehículo robado asegurado") es la única variable de cobertura de seguro del instrumento, y solo se formula para `BPCOD=01` (robo total de vehículo) — verificado por diseño de cuestionario y empíricamente contra microdato (1 028 de 40 280 filas válidas, 100% `BPCOD=01`). La ficha exige, para pasar a evaluable, que la cobertura **varíe entre clases de delito**; no varía — hueco de instrumento, no de mercado ni de muestra. Hallazgo adyacente, declarado y no adjudicado: dentro de `BPCOD=01`, denuncia 79.1% (asegurado, n=402) vs. 67.2% (no asegurado, n=614) — brecha de 11.9pp en la dirección del "vuelco" de la propia ficha, pero no prueba el falsador tal como está redactado (compara clases, no subgrupos de una). Detalle completo: `hitoD-R7.2`.

⚠️ **Corrección de staleness, encontrada al tocar esta línea:** la edición anterior de este párrafo listaba *"Siguiente en el orden: R3.2 (ENCIG tiene serie) · R5.1 · R7.2"* — pero `R3.2` ya estaba archivada (veredicto `B`, 29/jul/2026, §L5 arriba) desde antes de que esta línea se escribiera la última vez; nunca se retiró de la lista de pendientes al cerrarla. No se investiga aquí por qué; se corrige de paso, con esta nota, al mover el contador por `R7.2`.

**Siguiente en el orden, por valor informativo y no por facilidad:** R5.1 (Pensión del Bienestar como choque exógeno).

**HITO F · MILPA Fase 1 — POSPUESTO por decisión.**

---

**Suite de verificación (`tests/check.py`) — última corrida verificada, 30/jul/2026.** La suite corre completa: **19 FAIL · 84 WARN** *(sin cambio neto tras sellar D-09/D-10 con ADR-47 y subir `gobernanza` a v1.15 (ADR-48) esta misma sesión: las citas viejas a `gobernanza-v1.14.md` y al conteo de ADR anterior en este mismo archivo se corrigieron en el mismo commit que sube la versión, así que T03/T15 no llegan a disparar. Trayectoria de WARN: 107 (auditoría del 29/jul, antes de `TRANSFER-maestra-7/8.md`) → 89 (`26e7ef4` normaliza T03) → 86 (esta sesión declara 3 nombres en `HISTORICOS`) → 83 (esta sesión corrige `gobernanza §2` para dejar de citar en backticks los nombres viejos que corrige) → 84 (sesión de la subida a v2.2: `gobernanza` se renombra a v1_10, una cita fechada a `gobernanza-v1_9.md` pasa a colgante) → 82 (Cambio 6 de esa misma sesión añade `renombr` al regex de disparo de T03) → 84 (sesión de cierre del gate T17, 30/jul: aterrizar `TRANSFER-maestra-9.md` sube T03 en 2 — cita verbatim, a modo de ejemplo, el mismo falso positivo `-v3.2.md`/`-v3_2.md` ya documentado arriba) → 87 (refreeze tras el merge del PR #1, 30/jul: `revision-publicacion-2026-07-30.md` cita 3 veces, como propuesta descartada por D-05, el artefacto LICENSE-CORPUS que no se creará — patrón I-01, bucket propio en el baseline) → 84 (30/jul, ADR-48 · R0: la marca `{cita-ilustrativa}` cierra I-01 y esas mismas 3 citas dejan de disparar T03 — 21 → 18); `censo-integridad-v1_0.md` C1-06)*. **FAIL sube de 18 a 19 (29/jul):** T17 se amplió para escanear también el cuerpo vigente del propio `hitoD-preregistro` (antes solo leía `estado`), y con eso capturó la autodeclaración falsa de `hitoD-preregistro:8` ("contiene 27 fichas", contra 25 reales) — deuda congelada por decisión de mesa en `tests/baseline.json`, pendiente de un ADR futuro que decida si la cabecera append-only de un pre-registro está cubierta por esa protección. Según la nota del 29/jul, el desglose por test se reprodujo de forma independiente en Windows 11/Python 3.14 contra la corrida original en contenedor Linux. `CONTRIBUTING.md` tenía un byte UTF-8 truncado (pos 2149) que rompía T03 con `UnicodeDecodeError` antes del final de la corrida; corregido en `09bfb05`.

**Lo que la auditoría movió:** se corrigió §7 (cobertura del pre-registro — ver declaración canónica en §4·S2); se cerró una deuda abierta desde antes de ADR-37 (el perímetro **es 27**, sin ambigüedad — §4·S2); quedan abiertos que **T07 no vigila el vocabulario de tier del motor** (§4·S1) y la disyuntiva de **T10 vs. la convención de procedencia del integrador** (§4·S2).

⚠️ **Al usar la nota del 29/jul:** su análisis cualitativo está verificado, pero **sus conteos de disparos de T10 (66/45/5) no se reprodujeron** (65/57/14 al recomputar). Detalle en `forense/notas/2026-07-29-b-correccion-perimetro.md §6`. ⚠️ **Corregido 29/jul/2026:** este párrafo decía que una cita suya a `curaduria-archivos.md:23` "no checa contra el archivo" — **falso**. `curaduria-archivos.md:23` sí trae, verbatim, *"...convirtió un `[MEDIO], muestra mexicano-americana` en un `Fuerte` pelón—"*. La afirmación errónea nació en `a79227e` y se heredó aquí sin verificar 17 segundos después (`7d6535e`); retractada en `forense/notas/2026-07-29-b-correccion-perimetro.md §9` y trazada en `censo-integridad-v1_1.md §3`.
