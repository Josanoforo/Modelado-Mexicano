# Identificabilidad de perfiles y momentos · INV-SEG parte 3

> **VEREDICTO — el escenario realista NO supera cómodamente los 29 libres: gana el conteo (36–119 momentos) y pierde la estructura. Cuatro de los 29 parámetros libres son inidentificables con CUALQUIER número de momentos, y la segmentación entrega 4 celdas, no 6 perfiles — dos de ellas uniones forzadas ({1∪4} y {2∪3}). El ajuste por momentos queda SUBIDENTIFICADO: ADR-50(5) no es riesgo pendiente, es riesgo REALIZADO, y ADR-50 necesita revisión.**

*31 de julio de 2026. Responde al encargo INV-SEG parte 3.*

**Perímetro (ADR-46, declarado):** `canon/` · `milpa/` · `forense/`. No se abrió `data/raw/`, ni descriptor, ni microdato, ni `data/manifiesto.yaml`. Esta sesión razona sobre el inventario ya producido; no extrae. No añade contaminación de fuente sobre la ya declarada en INV-SEG partes 1-2.

**No se modificó ningún artefacto de `canon/`.** El veredicto contradice el supuesto operativo de ADR-50, y eso es entregable, no permiso para editarlo.

---

## 0 · Verificación de alcance (derivada, no heredada)

| magnitud | derivación | resultado |
|---|---|---|
| reglas en `modelo` §3.B | conteo de `**id:**` por encabezado `### 3.N` | **49** (20 prioritarias / 29 no-prioritarias) |
| reglas ausentes de Tabla B | ids de §3.B sin aparición literal en "Resto de dominios" | **8** ✔ coincide con el encargo |
| reglas en Tabla B | grupos-regla parseados (3 son `dos-ids-una-regla`) | **41** · 41 + 8 = 49 ✔ |
| parámetros libres | `procedencia.yaml`: valores en `valores:` sin `calibrable_con` + coeficientes | **14 + 15 = 29** ✔ |

Las 8 reglas ausentes — **revisado y no observable, cero momentos, no hueco**:
`dinero.credito.scoring_alternativo` · `tramite.evasion.norma_inutil_sancion_improbable` · `salud.prevencion.hombre_sin_permiso` · `salud.consumo.sellos_precio_similar` · `civico.clientelismo.turnout_no_vote_choice` · `civico.autodefensa.agravio_rural` · `informacion.credibilidad.allegado_confianza` · `informacion.escuela.miedo_a_caer_clase_media`

Derivación del 29 (por VALORES, no por id — como ADR-50 mismo especifica):

```
medidos 4 + derivados 6                          = 10 fijas
asignados_probabilidad: 13 ids, 29 valores
   6 ids con calibrable_con                      = 15 valores  (con ruta)
   7 ids sin calibrable_con                      = 14 valores  ← LIBRES
coeficientes de generador (G1:2 G2:2 G3:3 G4:4 G5:3 G6:1) = 15  ← LIBRES
                                        10+15+14 = 39 probabilidades ✔
                                       LIBRES = 14 + 15         = 29
```

⚠️ **Régimen asimétrico — declarado, y sí permite conteo honesto, con una salvedad.** Tabla B trae sí/no/parcial contra las 8 fuentes solo en los 5 dominios prioritarios; en §3.1/§3.3/§3.4/§3.7/§3.9 trae solo sí/parcial. Consecuencia: para los dominios no prioritarios **no se puede distinguir "no observable" de "no reportado"**, salvo por las 8 ausentes, que el inventario declara explícitamente como revisadas. El conteo de abajo por eso se da en **rango [estricto, laxo]** y nunca como cifra única. Donde el régimen muerde de verdad —las 7 reglas que cargan las 14 probabilidades libres— las 7 están en dominios no prioritarios, así que su estatus se leyó regla por regla, no por agregado.

---

## 3.A · Correspondencia perfil → observable

Los 6 perfiles de `modelo` §1.1 se definen por 10 parámetros (horizonte, radio de confianza, aversión, estatus, deferencia, `familismo_apoyo`, `familismo_obligacion`, violencia, `confianza_institucional`, acceso digital). **Ninguna encuesta del inventario pregunta ninguno de los diez.** El puente sólo puede construirse con los 6 ejes observables de Tabla A.

| perfil | combinación observable propuesta | debilidad | ¿identificable? |
|---|---|---|---|
| **1 · Clasemediero urbano formal** | formalidad=formal (`SEG_SOC`/`P3_13`/`AP3_15_4`) + `T_LOC` 1-2 + ingreso medio (`est_socio` medio-bajo/medio-alto, `ING7C` tramos centrales) + acceso digital alto | No separa de 4 por arriba: el corte "clase media / A-B" no existe en ningún descriptor del inventario. `est_socio` es un ordinal de 4 categorías y `ING7C` son múltiplos de salario mínimo; ninguno tiene un umbral principiado para élite. Los marcadores definitorios (estatus **alta**, deferencia recalibrada) no se observan | **PARCIAL** — sólo como `{1∪4}` |
| **2 · Popular informal** | informalidad (`SEG_SOC` sin acceso / `EMP_PPAL`/`TUE_PPAL`) + ingreso bajo + `T_LOC` 3-4 para el extremo rural | No separa de 3. Lo que distingue a 2 de 3 es horizonte (corto vs corto→mixto), estatus (media vs **alta, "miedo a caer"**) y acceso (bajo→medio vs medio). "Miedo a caer" es un estado subjetivo que ninguna fuente pregunta | **NO por separado** — sólo como `{2∪3}` |
| **3 · Vulnerable en ascenso** | igual que 2, más una trayectoria de ingreso ascendente | **"En ascenso" es una TRAYECTORIA, no un estado**: exige panel. El único panel del corpus es el rotativo de ENOE (5 trimestres), y `CAL-ENOE` Fase A ya cerró que ENOE no trae ni una pregunta de ahorro, crédito, deuda o planeación (`hallazgos.md` 31/jul). Se puede ver la trayectoria de ingreso, no el desenlace conductual | **NO** — colapsa en `{2∪3}` |
| **4 · Élite A/B urbana** | formal + urbano + ingreso techo + acceso "muy alto/global" | Tres fallas acumuladas: (a) sin corte principiado frente a 1; (b) la cola alta está sistemáticamente submuestreada en encuesta de probabilidad y el decil superior de ENIGH **no** es A/B; (c) "radio medio en **burbuja privada**" y "acceso global" no tienen observable — lo más cercano (`P3_15` de ENIF, vivió en el extranjero) confunde con el perfil 6 | **NO** — hueco declarado |
| **5 · Joven Gen Z urbano conectado** | edad (`EDAD_V` 18-29) + `T_LOC` 1-2 + acceso digital alto (`P3_14` smartphone, `P2_4_12/13`) | El mejor caso de los seis: sus tres marcas son tres de los seis ejes. Pero **no es una partición** — corta transversalmente la formalidad, así que un informal urbano de 24 años cae a la vez en 5 y en `{2∪3}`, y el modelo no da regla de prioridad. Su marca definitoria (deferencia **recalibrada**) no se observa | **SÍ, pero solapado** (no disjunto) |
| **6 · Migrante / transnacional** | migración propia (`P3_15`/`P3_16`, `CS_P20A-C`) · integrante ausente (`CS_AD_MOT/DES`) · remesas (`P7_5`, `remesas`, `P3_20_3`) | El proxy se parte en **tres poblaciones que no son la misma**: quien migró y volvió · el hogar que **se quedó** y recibe remesas · el hogar con integrante ausente. Recibir remesas no implica radio de confianza transnacional. Además el eje falta por completo en ENVIPE y ENCIG | **PARCIAL y heterogéneo** |

### Lo que sobrevive: 4 celdas, no 6 perfiles

```
A = {1 ∪ 4}   formal · urbano · ingreso medio-alto      (unión forzada)
B = {2 ∪ 3}   informal · ingreso bajo-medio             (unión forzada)
C = {5}       joven · urbano · digital alto             (SOLAPA con A y B)
D = {6}       migración / remesas                        (heterogéneo, 3 poblaciones)
```

Capacidad por fuente (una celda es computable si la fuente trae **todos** los ejes que la celda exige, en el mismo instrumento):

| fuente | estricto (sólo Sí) | laxo (Sí+Parcial) |
|---|---|---|
| ENIF | **A B C D** (4) | A B C D (4) |
| ENOE | A B D (3) | A B D (3) |
| ENIGH | A B (2) | A B C D (4) |
| ENCUCI | B (1) | A B C D (4) |
| ENUT | C (1) | A B C D (4) |
| ENVIPE | — (0) | A B (2) |
| ENSANUT | — (0) | A B C D (4) |
| ENCIG | — (0) | C (1) |

⚠️ **ENCIG no identifica ninguna celda en régimen estricto** y sólo una en laxo: no tiene variable de ingreso (ausencia verificada por `grep` en el diccionario 2023 completo) y su universo excluye por diseño toda localidad &lt;100 000 hab. Es la fuente que sostiene `tramite.mordida.*` — es decir, los desenlaces de trámite quedan observables pero **no segmentables por perfil**.

---

## 3.B · Momentos

**Unidad usada:** un momento = *(regla con desenlace observable, celda de perfil)* computable porque **alguna fuente observa ese desenlace Y identifica esa celda en el mismo instrumento**. La misma regla vista en tres fuentes es **un** momento medido tres veces, no tres momentos — cuenta para precisión, no para identificación.

Insumo (Tabla B, parseada): 41 grupos-regla · **18** con Sí en ≥1 fuente · **14** sólo Parcial · **9** todo-No · **+8** ausentes. Reglas con desenlace observable: **18 (estricto) / 32 (laxo)**. Sin ningún momento posible: 9 + 8 = **17 de 49**.

| escenario | supuesto | aritmética | momentos |
|---|---|---|---|
| **OPTIMISTA** | toda fuente identifica los 6 perfiles | 18 × 6 · 32 × 6 | **108 – 192** |
| **REALISTA** | celdas de 3.A, por regla, en fuente que observa el desenlace | Σ por regla | **36 – 119** |
| **PESIMISTA** | sólo formal/informal (2 celdas) | 18 × 2 · 32 × 2 | **36 – 64** |

**Contra 29 libres, el conteo bruto pasa en los tres escenarios.** Y el conteo bruto es la métrica equivocada. Tres pruebas estructurales lo desmienten:

### Prueba 1 — ¿qué momento toca qué parámetro libre?

Las 14 probabilidades libres viven en **7 reglas concretas**. Un momento sobre cualquier otra regla no las identifica.

| regla que carga probabilidad libre | valores | desenlace observable |
|---|---|---|
| `dinero.consumo.estatus_mediado_por_credito` | 2 | Sí — ENIGH `gastotarjetas` |
| `salud.atencion.grave` | 2 | Parcial — ENSANUT `H0409A-D` |
| `tramite.mordida.con_registro` | 2 | Sí — ENCIG (relación `P7_3` × `P8_4-7`) |
| `tramite.gobierno_digital.coercitivo` | 2 | Sí — ENIF/ENCIG |
| `tramite.gobierno_digital.util_sin_coercion` | 2 | Sí — misma fila ENIF/ENCIG |
| `civico.denuncia.con_seguro` | 2 | Sí — ENVIPE `BP2_1`/`BP1_28` |
| **`salud.prevencion.hombre_sin_permiso`** | **2** | **NO — es una de las 8 ausentes** |

→ **12 de 14 alcanzables · 2 muertas por construcción.** Ningún número de momentos las rescata.

Peor: de las 6 reglas alcanzables, tres (`tramite.*`) dependen de **ENCIG**, que no segmenta (arriba). Sus momentos existen a nivel nacional pero **no por celda**, así que constriñen el nivel y no la variación — que es lo que los coeficientes necesitan.

### Prueba 2 — rango del diseño, por generador

Un coeficiente es una elasticidad: identificarlo exige que las celdas **varíen en ese parámetro de forma independiente**. Rango de la matriz celda×parámetro (centrada), por generador:

| gen | coefs | optimista (6) | realista (4) | pesimista (2) |
|---|---|---|---|---|
| G1 | 2 | 1 · **falta 1** | 1 · **falta 1** | 1 · **falta 1** |
| G2 | 2 | 2 · OK | 2 · OK | 1 · **falta 1** |
| G3 | 3 | 3 · saturado | 3 · **saturado, 0 gl** | 1 · **faltan 2** |
| G4 | 4 | 3 · **falta 1** | 3 · **falta 1** | 1 · **faltan 3** |
| G5 | 3 | 3 · saturado | 3 · **saturado, 0 gl** | 1 · **faltan 2** |
| G6 | 1 | 1 · OK | 1 · OK | 1 · OK |
| **no identificables** | | **2 de 15** | **2 de 15** | **9 de 15** |

Tres lecturas, todas malas:

1. **G1 y G4 fallan hasta en el escenario optimista**, y no por segmentación: `confianza_institucional` **no tiene valor por perfil en §1.1** — es el vector de §1.3, cuya resolución es `D-12`, abierta (ADR-49 D3; ADR-50 declara que no la cierra). Es un hueco de especificación, no de dato. Ningún trabajo de campo lo arregla mientras D-12 siga abierta.
2. **G3 y G5 quedan JUSTO identificados, con cero grados de libertad residuales.** Ajustan perfecto por construcción y **no se pueden refutar**. Es literalmente el riesgo que `procedencia.yaml` ya se nombra a sí mismo: *"un generador explique cualquier cosa si se le mueve el coeficiente — el riesgo de infalsabilidad"*.
3. `familismo_apoyo` y `familismo_obligacion` difieren **en un solo perfil de los seis** (el 1: medio-alto vs medio) — y el perfil 1 es justo el que se funde en la unión `{1∪4}`. Su separación entera descansa en un escalón ordinal de un perfil que la segmentación no puede aislar. El check obligatorio de ADR-30 (*"una configuración donde `familismo_obligacion` alto mejore TODOS los desenlaces se rechaza"*) **no puede satisfacerse por ajuste**: no hay contraste que separe los dos efectos.

⚠️ Estos rangos son **cotas superiores generosas**: se calcularon promediando las celdas-unión (supone medición perfecta de la media de la unión) y tratando los ordinales de §1.1 como cardinales — que es exactamente lo que ADR-28.a prohíbe (*"la aritmética conserva orden, no magnitud"*). La identificación real es **peor** que esta tabla.

### Prueba 3 — el denominador no es 29 si el ABM debe ejecutar

`cobertura-motor.md`: **15 reglas con valor, 34 sin ninguno**. Los 144 números cubren las probabilidades de 15 reglas. Cruzando con observabilidad:

| | desenlace observable | sin desenlace |
|---|---|---|
| **con** valor numérico | 13 | 0 |
| **sin** valor numérico | 19 | 9 (+8 ausentes) |

ADR-50 declara que el motor es *"un ABM EJECUTABLE"*. Un ABM no ejecuta una regla sin probabilidad. Si esas 34 reglas necesitan número para correr, el conteo de libres no es 29 — es 29 más lo que cueste poblarlas, y **17 de las 49 no tienen ningún momento con qué poblarse**. No lo resuelvo aquí: es decisión de mesa si esas 34 entran al ajuste, quedan fuera del motor ejecutable, o se fijan por otra vía. Se reporta porque cambia el denominador del veredicto.

---

## 3.C · Veredicto

**El escenario realista NO supera cómodamente los 29 libres.**

Supera el **conteo** (36–119 vs 29) y falla la **estructura**, que es lo que decide identificación:

| | inidentificable | por qué | ¿lo arregla más dato? |
|---|---|---|---|
| 2 de las 14 probabilidades | `salud.prevencion.hombre_sin_permiso` | desenlace revisado y no observable en las 8 fuentes | **No** |
| 2 de los 15 coeficientes | G1 y G4 sobre `confianza_institucional` | sin valor por perfil en §1.1 — `D-12` abierta | **No** — se arregla cerrando D-12 |
| **4 de 29** | | | |

Y sobre los 25 restantes, el ajuste que se podría correr hoy es **untestable en G3 y G5** (cero grados de libertad) y descansa en una segmentación de **4 celdas con dos uniones forzadas** — no en los 6 perfiles que el modelo declara. Los perfiles 1 vs 4 y 2 vs 3 **no se separan con ninguna combinación de variables del inventario**; el 5 se identifica pero solapa; el 6 se parte en tres poblaciones distintas.

Consecuencia directa sobre ADR-50: su §(1) exime a los 90 `params_base` del ajuste porque *"se miden de transversal"*. **Esa exención no esquiva el problema**: medir 15 escalares × 6 perfiles en transversal exige identificar los 6 perfiles en la transversal, que es exactamente lo que 3.A muestra que no se puede. La precondición es la misma.

**ADR-50(5) escribió esto como *condición pendiente, no resuelta*. Queda resuelto, y en contra: es riesgo REALIZADO. ADR-50 necesita revisión.**

No se propone el arreglo — es decisión de mesa (ADR-50 §(3) además exige que los momentos se declaren antes de ajustar, y esta nota no los declara).

---

## Límites declarados

- **El régimen asimétrico impide distinguir "no observable" de "no reportado"** en los 5 dominios no prioritarios, salvo por las 8 ausentes. Por eso todo conteo va en rango [estricto, laxo] y las 7 reglas críticas se leyeron una por una.
- **Los rangos de la Prueba 2 son cotas superiores** (promedio de uniones + ordinales tratados como cardinales, contra ADR-28.a). La identificación real es peor, no mejor.
- **La correspondencia de 3.A es una propuesta de esta sesión**, no un resultado medido: nadie ha corrido una validación de que `formalidad + ingreso + localidad` recupere al perfil 2. Sin microdato no se puede — y el microdato está fuera de perímetro por diseño del encargo.
- **`CAL-CONF` Fase B sigue sin existir** como artefacto. ADR-50(5) la nombra, junto al chequeo de ejes, como lo que decide esto. Esta nota es el chequeo de ejes; Fase B sigue pendiente.
- No se verificó si las fuentes citadas en `calibrable_con` están en disco — exige `data/manifiesto.yaml`, fuera de perímetro (misma salvedad que ADR-50 declara para sí mismo).
