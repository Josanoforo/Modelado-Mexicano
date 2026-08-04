# P2 · ¿Los momentos por atributo identifican los libres del ajuste?

> **VEREDICTO GLOBAL — ADR-50 SE REESCRIBE.** La subidentificación **persiste sobre atributos**. El reencuadre arregla lo que estaba roto en la *segmentación* (las 4 celdas con dos uniones forzadas desaparecen; hay celdas con soporte real) y **no toca** lo que estaba roto en la *medición*: los 9 parámetros que los generadores multiplican siguen sin reactivo en 6 de 9 casos, y el número de celdas es irrelevante para eso. De **22 grados de libertad reales** (no 29 — ver §0), **7 quedan IDENTIFICADOS, 2 JUSTO IDENTIFICADOS, 5 INIDENTIFICABLES y 8 NO DETERMINABLES EN ESTE RÉGIMEN**. La clase "inidentificable con cualquier número de momentos" **no se encoge: rota** — sale la mitad que INV-SEG p3 le atribuía a `D-12`, entran cuatro miembros nuevos.

> **Punto 3(a) — G3/G5 sin grados de libertad: PERSISTE.** *(problema del modelo, no de la segmentación)*
> **Punto 3(b) — contraste ADR-30 apoyo/obligación: PERSISTE.** *(problema del modelo, no de la segmentación)*

*1 de agosto de 2026. Responde al ENCARGO P2. Rama `claude/adr-50-momentos-atributo-qf8m7t`, base `d9af0ae` (`origin/main`, con PR #40 ya fusionado).*

**Perímetro (ADR-46, declarado):** `canon/` · `milpa/` · `forense/`. **No se abrió** `data/raw/`, ni descriptor, ni catálogo, ni cuestionario, ni microdato, ni `data/manifiesto.yaml`. Esta sesión razona **solo sobre inventarios ya producidos** y sobre el canon. **No añade contaminación de fuente** — no queda inhabilitada para pre-registrar contra ninguna de las ocho encuestas, a diferencia de INV-SEG partes 1-3 y de P1.

**No se modificó ningún artefacto de `canon/` ni de `milpa/`.** Este veredicto contradice el supuesto operativo de ADR-50 y corrige una cifra que ADR-50 escribe en su propio texto. Eso es **entregable, no permiso para editarlo** — mismo tratamiento que dio INV-SEG p3.

---

## 0 · Verificación de premisas y re-derivación del 29

Las cuatro premisas del encargo se verificaron antes de obedecerlas.

| # | premisa | verificación | veredicto |
|---|---|---|---|
| 1 | INV-SEG p3: 4 celdas, ajuste SUBIDENTIFICADO, ADR-50(5) riesgo realizado | `forense/notas/2026-07-31-identificabilidad-perfiles.md`, leído entero | **SE SOSTIENE** — es el punto de partida |
| 2 | P1 dio CONJUNTA COMPLETA, 3 ejes de nivel hogar sin varianza intra-hogar | `git log` → PR #40 fusionado en `d9af0ae`; `forense/notas/2026-07-31-p1-enigh-semilla.md` §3 | **SE SOSTIENE** — el caveat de §3 es restricción de diseño, aplicada en §1.b abajo |
| 3 | Los libres del ajuste son "29 = 14 + 15" | re-derivado por VALORES en esta sesión, receta abajo | **SE SOSTIENE la cifra 29 · NO SE SOSTIENE que sean 29 grados de libertad** — ver §0.2 |
| 4 | La revisión propone parámetros como condicionales sobre atributos observables | `revision-programa-2026-07-31.md` §2 | **SE SOSTIENE** — literal: *"los parámetros del modelo se expresan como distribuciones condicionales sobre atributos, no como constantes por perfil"* |

### 0.1 · Receta de derivación, probada contra un id conocido

Receta (la de INV-SEG p3 §0, re-implementada aquí, no heredada): contar **valores dentro de `valores:`**, no ids de regla; libre = valor de una regla **sin campo `calibrable_con`**; más los coeficientes de `asignados_coeficiente.detalle`.

**Prueba contra un id conocido** antes de confiar en ella — `dinero.ahorro.informal_sin_puente`, del que se sabe por lectura directa que tiene 3 valores y sí trae `calibrable_con`:

```
$ python3 derivar29.py     # sobre milpa/procedencia.yaml
== PRUEBA DE RECETA contra un id conocido ==
  dinero.ahorro.informal_sin_puente: n_valores=3 valores=[0.74, 0.21, 0.05] calibrable_con=True  (esperado: 3, True)
```

Salida cruda de la ejecución completa:

```
== CONTEO CRUDO ==
ids en asignados_probabilidad      : 13
valores totales                    : 29
ids CON calibrable_con             : 6  -> valores = 15
ids SIN calibrable_con (LIBRES)    : 7  -> valores = 14

-- las 7 reglas que cargan las probabilidades libres --
   dinero.consumo.estatus_mediado_por_credito           n=2  suma=1.0
   salud.atencion.grave                                 n=2  suma=1.0
   salud.prevencion.hombre_sin_permiso                  n=2  suma=1.0
   tramite.mordida.con_registro                         n=2  suma=1.0
   tramite.gobierno_digital.coercitivo                  n=2  suma=1.0
   tramite.gobierno_digital.util_sin_coercion           n=2  suma=1.0
   civico.denuncia.con_seguro                           n=2  suma=1.0

== COEFICIENTES DE GENERADOR ==
   G1: 2  ['confianza_institucional', 'radio_confianza']
   G2: 2  ['sens_estatus', 'aversion_riesgo']
   G3: 3  ['horizonte_temporal', 'aversion_riesgo', 'familismo_apoyo']
   G4: 4  ['exposicion_violencia', 'confianza_institucional', 'horizonte_temporal', 'sens_estatus']
   G5: 3  ['familismo_apoyo', 'familismo_obligacion', 'radio_confianza']
   G6: 1  ['deferencia']
   TOTAL coeficientes = 15

== LIBRES DEL AJUSTE (receta por VALORES, como ADR-50) ==
   14 probabilidades + 15 coeficientes = 29
```

**La receta reproduce exactamente lo que ADR-50 dice: 29 = 14 + 15.** No hay motivo para detenerse por discrepancia de conteo.

### 0.2 · Pero 29 no son 29 grados de libertad — hallazgo derivado, no heredado

El mismo script ejecuta un control que INV-SEG p3 no corrió:

```
== CONTROL DE SIMPLEX (derivado, no heredado) ==
   reglas cuyos valores NO suman 1: 0  []
   grados de libertad reales probabilidades libres = 14 - 7 = 7
   grados de libertad reales TODAS las asignadas   = 29 - 13 = 16
```

**Las 13 reglas de `asignados_probabilidad` tienen valores que suman exactamente 1.0, sin excepción.** Son distribuciones sobre desenlaces, no parámetros independientes: una regla con 2 valores aporta **1** grado de libertad, no 2; una con 3 aporta 2.

Consecuencia sobre la cifra que ADR-50 escribe en su propio texto: **las 14 probabilidades libres cargan 7 grados de libertad, no 14.** El objetivo real del ajuste es **22 = 7 + 15**, no 29.

Esto es **una corrección a canon, y va a favor de ADR-50**: el blanco es más chico de lo que el propio ADR declara. No cambia el veredicto global — lo que hunde al ajuste no es el tamaño del blanco sino qué momento toca qué parámetro — pero **`gobernanza-v1_15.md` §4, `estado-programa-v1_9.md` L0 y el texto de ADR-50 repiten "29 = 14 + 15" como si fueran 29 libertades, y no lo son.** Se reporta, no se corrige.

### 0.3 · Re-derivaciones de control (todas coinciden con INV-SEG p3)

| magnitud | derivación en esta sesión | resultado | control |
|---|---|---|---|
| ids de regla en `modelo` §3.B | regex `**id:** \`x\` [+ \`y\`]` sobre §3.B, pares desdoblados | **52 ids** (49 grupos-regla, 3 pares *dos-ids-una-regla*) | ✔ concuerda con los 49 de INV-SEG p3 |
| ids ausentes de Tabla B | ids de §3.B sin aparición (literal ni por sufijo) en el inventario | **8** | ✔ mismos 8, uno a uno |
| ids con `Sí` en ≥1 fuente | parseo de Tabla B, ids validados contra §3.B | **20** | ✔ 18 grupos, de los cuales 2 son pares → 20 |
| ids con `Sí` o `Parcial` | ídem | **35** | ✔ 32 grupos + 3 pares = 35 |
| ids sin ninguna observación | 52 − 35 | **17** | ✔ 9 todo-No + 8 ausentes |

Las 8 ausentes, re-derivadas (idénticas a INV-SEG p3):
`dinero.credito.scoring_alternativo` · `tramite.evasion.norma_inutil_sancion_improbable` · **`salud.prevencion.hombre_sin_permiso`** · `salud.consumo.sellos_precio_similar` · `civico.clientelismo.turnout_no_vote_choice` · `civico.autodefensa.agravio_rural` · `informacion.credibilidad.allegado_confianza` · `informacion.escuela.miedo_a_caer_clase_media`

⚠️ **Dos "ausencias" que no lo son, y que hay que no confundir.** `tramite.gobierno_digital.util_sin_coercion` y `civico.denuncia.con_seguro` dan **cero apariciones literales** en el inventario. No están ausentes: Tabla B los escribe abreviados dentro de la fila de su pareja (`...coercitivo` + `util_sin_coercion`, línea 337; `civico.denuncia.sin_seguro` + `con_seguro`, línea 353). Un conteo por `grep` del id completo los habría dado por muertos. Se marca porque es exactamente el error que el encargo prohíbe: **"no reportado con ese rótulo" ≠ "no existe"**.

---

## 1 · La malla de celdas de atributos

### 1.a · Qué la restringe de verdad (y qué no)

Los 6 ejes de P1: **formalidad · edad · urbanización · ingreso · acceso digital · migración**.

El impulso natural es multiplicar niveles y celebrar el resultado (2 × 3 × 4 × 4 × 2 × 2 = cientos de celdas frente a las 4 de INV-SEG p3). **Ese número es irrelevante y no se teclea aquí**, por dos razones derivables:

1. **Los niveles de corte no existen en el inventario.** Ni Tabla A ni P1 fijan tramos de edad, ni un umbral de ingreso, ni un corte de urbanización. `est_socio` trae 4 categorías y `tam_loc` 4 tramos (P1 §2) — esas sí están; edad, digital y migración no tienen partición canónica. Inventar los cortes para poder multiplicar sería teclear una cifra esperada.
2. **El rango de la matriz de diseño no crece con el número de celdas.** Si los parámetros se vuelven condicionales sobre atributos, θ_k(x), y el generador es y_g(c) = Σ_k β_gk · θ_k(x_c), entonces con condicional lineal en los 6 ejes lo que las celdas identifican son **6 pendientes compuestas + 1 intercepto = 7 cantidades por generador**, cualquiera que sea el número de celdas. Partir la edad en cinco tramos en vez de tres **no añade una sola cantidad identificable**. Este es el cambio de fondo respecto a INV-SEG p3, cuyo cuello de botella era el conteo de celdas; ahora el cuello está en otro lado y se analiza en §2.

Lo que sí restringe la malla, y es lo que se deriva abajo, es **la co-observación dentro de un mismo instrumento**.

### 1.b · Restricción (a) — los ejes de nivel hogar no separan personas del mismo hogar

**Declarado explícito en el diseño de la malla, como pide el encargo.** P1 §3 (caveat, verbatim): *"3 de 6 ejes (urbanización, ingreso, acceso digital) y el componente `remesas` del eje 6 son atributos de **hogar**, no de persona — todas las personas del mismo hogar comparten el mismo valor en esas columnas tras el join. […] esa varianza **no existe en ENIGH** — es indistinguible de una persona a otra del mismo hogar por diseño del instrumento."*

Consecuencias sobre la malla, aplicadas y no asumidas:

- **La malla de celdas es una malla mixta.** Sobre {urbanización, ingreso, acceso digital} la celda es una propiedad del **hogar**; sobre {formalidad, edad, migración-propia} es del **individuo**. Un agente sintético hereda 3 coordenadas de su hogar y porta 3 propias.
- **Ninguna celda puede definirse por contraste intra-hogar en los tres ejes de hogar.** "El hermano de ingreso alto y la hermana de ingreso bajo del mismo hogar" no es una celda: es una celda vacía por diseño del instrumento, en las ocho fuentes que miden ingreso a nivel hogar (Tabla A eje 4: ENIGH `ing_cor`/`est_socio` y ENSANUT `indice1`/`nseF` son de hogar; ENIF `P3_11A` y ENUT `P5_10` son individuales pero solo para quien trabajó, con lo que el no-ocupado del hogar queda sin valor propio).
- **Esta restricción es la que muerde en el punto 3(b)** — ver §3.b. El familismo es un constructo **relacional dentro del hogar**; su contraste natural (quien da cuidado vs. quien lo recibe, bajo el mismo techo) cae precisamente en la dimensión que los ejes de hogar no pueden resolver.
- No afecta al eje 2 ni al 1: edad y formalidad sí varían persona a persona (P1 §3), que es lo que salva a las celdas edad × formalidad.

### 1.c · Restricción (b) — soporte por eje y fuente, en rango [estricto, laxo]

Derivado por re-parseo de la Tabla A del inventario (nunca cifra única donde INV-SEG no la dio; `Sí…` → estricto y laxo, `Parcial` → solo laxo, `No` → ninguno):

```
== CAPACIDAD DE CELDA POR FUENTE (nº de ejes disponibles) ==
fuente     estricto  laxo   ejes estrictos
ENIGH             4     6   1,2,3,4
ENIF              6     6   1,2,3,4,5,6
ENVIPE            2     4   2,3
ENOE              5     5   1,2,3,4,6
ENCUCI            3     6   1,2,4
ENCIG             1     4   2
ENSANUT           3     6   2,3,4
ENUT              3     6   2,3,5
```

Lecturas derivadas de esta tabla:

- **ENIF es la única fuente con los 6 ejes en régimen estricto.** Es la malla más rica del corpus, y no era el hallazgo de P1 (que fue sobre ENIGH como *semilla* de síntesis, otra función).
- **ENCIG sigue siendo la fuente ciega**: un solo eje estricto (edad), cuatro en laxo, **sin ingreso en ninguno de los dos regímenes** (Tabla A eje 4, ENCIG = `No`, con `grep` sobre el diccionario 2023 completo) y con universo que excluye por diseño toda localidad <100 000 hab. Sostiene los desenlaces de trámite y no puede condicionarlos sobre ingreso ni sobre ruralidad. Este límite de INV-SEG p3 **sobrevive intacto al reencuadre**: no era un problema de perfiles.
- **ENVIPE pierde dos ejes en ambos regímenes** (digital `No`, migración `No`), lo que trunca toda condicional estimada ahí — importa para G4.
- **La mejora frente a INV-SEG p3 es real y grande**: donde había 4 celdas con dos uniones forzadas (`{1∪4}`, `{2∪3}`) y un solapamiento no resuelto (perfil 5), hay ahora 6 ejes con soporte estricto en al menos una fuente y **ninguna unión forzada**, porque no hay partición que violar. Las tres patologías nombradas por INV-SEG p3 §3.A —uniones forzadas, solapamiento del perfil 5, heterogeneidad del perfil 6— **desaparecen por construcción**. Eso es lo que el reencuadre sí arregla.

### 1.d · La restricción que el reencuadre no relaja: co-observación

Un momento sigue siendo *(desenlace observable, celda)* computable **solo si una misma fuente observa el desenlace e identifica la celda en el mismo instrumento** (unidad de INV-SEG p3 §3.B, conservada). El reencuadre **no relaja esto**, y la propia revisión lo dice de sí misma (§7): *"la síntesis IPF hereda sus propios supuestos (la conjunta de la semilla se preserva al reponderar) — no es magia"*.

**Corolario derivado, y es el eje de todo §2:** el IPF **reproduce marginales; no fabrica conjuntas que nadie midió**. Si el reactivo de un parámetro vive en la fuente A y el desenlace del generador que lo usa vive en la fuente B, ninguna reponderación crea la covarianza individual entre los dos. La síntesis amplía la malla de *atributos*; no amplía la malla de *pares (parámetro, desenlace)*.

Oferta de momentos por fuente (Tabla B re-parseada, ids validados contra §3.B):

```
fuente     reglas Sí  reglas Parcial
ENIGH              1               9
ENIF               6               9
ENVIPE             2               1
ENOE               1               4
ENCUCI             5               2
ENCIG              4               0
ENSANUT            3               4
ENUT               2               3
ids con Sí en >=1 fuente : 20   ·   ids con Sí o Parcial : 35   ·   sin observación : 17
```

---

## 2 · La aritmética rehecha: qué momento toca qué parámetro

### 2.a · El acoplamiento regla→generador, derivado

Un coeficiente `β_gk` solo se mueve por momentos sobre reglas que **el generador g enruta**. Derivado de las cláusulas `PORQUE` de §3.B (excluyendo las anotaciones `*(v…)*`, que citan generadores por historia y no por ruteo):

```
ids ruteados (con pares desdoblados): 52
reglas-id que NOMBRAN un generador en su PORQUE : 18
reglas-id SIN generador nombrado                : 34
ids por generador: {'G1': 6, 'G2': 2, 'G3': 3, 'G4': 3, 'G5': 2, 'G6': 3}
```

**34 de 52 ids no nombran ningún generador.** Sus momentos son informativos sobre la probabilidad de su propia regla y **no tocan un solo coeficiente**. La oferta efectiva de momentos para los 15 coeficientes no es "36–119": es lo que sale de **18 ids**, de los cuales solo una parte tiene desenlace observable.

Y sobre las 7 reglas que cargan las probabilidades libres:

```
   dinero.consumo.estatus_mediado_por_credito     -> G2
   salud.atencion.grave                           -> NINGUNO
   salud.prevencion.hombre_sin_permiso            -> NINGUNO
   tramite.mordida.con_registro                   -> NINGUNO
   tramite.gobierno_digital.coercitivo            -> NINGUNO
   tramite.gobierno_digital.util_sin_coercion     -> NINGUNO
   civico.denuncia.con_seguro                     -> NINGUNO
```

**Seis de las siete no están acopladas a ningún generador.** Buena noticia y noticia acotada: sus probabilidades se identifican directamente del desenlace observado por celda, **sin contaminarse del problema de los coeficientes** — pero también sin que ningún momento sobre ellas ayude a identificar un coeficiente.

### 2.b · El criterio de identificación de un coeficiente (derivado, no importado)

Bajo el reencuadre, θ_k deja de ser una constante `ASIGNADO` por perfil y pasa a ser una condicional θ_k(x) **que hay que estimar**. En el momento observado sobre la celda c:

> y_g(c) = Σ_k β_gk · θ_k(x_c)

Si θ_k(x) también se estima de estos mismos momentos, β y θ entran **solo como producto**: cualquier reescalamiento β_gk → λβ_gk, θ_k → θ_k/λ deja los momentos idénticos. **El producto es identificable; los factores no.** Ningún número de celdas rompe esto — es una no-identificación de rotación/escala, no de conteo.

Esto se rompe de una sola forma: **si θ_k está medido directamente por un reactivo**, deja de ser incógnita y β_gk queda identificado por regresión del desenlace sobre θ medido. De ahí el criterio, que se aplica coeficiente por coeficiente abajo:

> **`β_gk` es IDENTIFICADO si y solo si (C1)** existe un reactivo que mide θ_k, **(C2)** en una fuente que **también** observa un desenlace de una regla enrutada por g —mismo instrumento, porque IPF no fabrica esa conjunta (§1.d)—, **(C3)** ese desenlace no es la misma variable que el reactivo (si lo es, la regresión es circular), y **(C4)** las celdas de esa fuente dan variación.

**Este criterio es el que cambia el signo del veredicto respecto de lo que la revisión esperaba.** Bajo perfiles, θ_k venía **dado** por §1.1 (90 `ASIGNADO`): β era identificable en principio y lo que faltaban eran celdas. Bajo atributos, sobran celdas y **θ_k ya no viene dado**. El reencuadre cambia un supuesto por una medición — y la medición, para 6 de 9 parámetros, no existe o no es determinable.

### 2.c · ¿Qué parámetros del modelo tienen reactivo? (corrección a INV-SEG p3 §3.A)

INV-SEG p3 §3.A afirma: *"Ninguna encuesta del inventario pregunta ninguno de los diez [parámetros]."* **Esa afirmación es demasiado amplia y se corrige aquí con el propio inventario**, sin abrir fuente:

| parámetro | reactivo reportado en el inventario | fuente · cita | régimen |
|---|---|---|---|
| `radio_confianza` | `AP5_1_1` (confianza en la mayoría) / `AP5_1_2` (personas que conoce personalmente) / `AP5_1_3` (vecinos) — *"distingue explícitamente confianza generalizada de confianza con vínculo personal"* | **ENCUCI**, inventario l.264, Secc. 5.1 pp.21-22 | reportado, dominio **PRIORITARIO** §3.8 |
| `confianza_institucional` | batería XI de confianza institucional | **ENCIG**, inventario l.265, Secc. XI p.62 | reportado |
| `confianza_institucional[justicia]` (proxy) | `AP5_5_01..11` percepción de corrupción por institución | **ENVIPE**, inventario l.335 | reportado, **proxy** (percepción de corrupción ≠ confianza) |
| `exposicion_violencia` | `BP1_20`/`BP1_23`/`BP1_28` (victimización, denuncia y sus razones) | **ENVIPE**, inventario l.353 | reportado |
| `familismo_apoyo` | `P9_9_1..6` *"¿con qué piensa cubrir su vejez?"* con **familia** como opción explícita — *"distingue explícitamente familia vs. Estado vs. mercado"* | **ENIF**, inventario l.171 | reportado, dominio **PRIORITARIO** §3.5 |
| `horizonte_temporal` (proxy) | `P4_10` *"¿por cuánto tiempo cubriría gastos con ahorros?"* | **ENIF**, inventario l.320 | reportado, **proxy** (stock de ahorro ≠ tasa de descuento) |
| `familismo_obligacion` | **ninguno** | §3.5 es PRIORITARIO: rejilla completa 8 fuentes, ninguna mide obligación-como-carga separada del apoyo | **ausencia DETERMINABLE** |
| `deferencia` | **ninguno** | §3.2 es PRIORITARIO: las 8 fuentes en `No` para `trabajo.jerarquia.deferencia_iniciativa_suprimida`; ENOE solo `P3A` (¿tiene jefe?), que el propio inventario clasifica *"cuenta como No de desenlace"* | **ausencia DETERMINABLE** |
| `sens_estatus` | **no reportado** | vive en §3.1/§3.9, dominios **NO prioritarios** — el inventario solo trae filas sí/parcial, así que no se puede distinguir "no reportado" de "no existe" | **NO DETERMINABLE EN ESTE RÉGIMEN** |
| `aversion_riesgo` | **no reportado** — el único candidato, ENIF `P5_23`/`P5_24` (conocimiento de protección IPAB), es un **moderador** de la aversión, no una medida de ella | §3.1, dominio NO prioritario | **NO DETERMINABLE EN ESTE RÉGIMEN** |

**Cuatro de los nueve parámetros de generador tienen reactivo directo reportado; dos tienen proxy; dos tienen ausencia determinable; dos no son determinables en este régimen.** Ese es el insumo real del ajuste, y no depende de cuántas celdas se construyan.

### 2.d · Tabla parámetro × estatus

**Denominador: 22 grados de libertad** (7 de probabilidad + 15 coeficientes), derivado en §0.2. Se da también la cuenta en "valores" que usa ADR-50 (14 + 15 = 29) para que la mesa pueda reconciliar.

#### Probabilidades libres — 7 g.l. sobre 7 reglas (14 valores)

| regla · g.l. | estatus | celda o momento que lo sostiene |
|---|---|---|
| `dinero.consumo.estatus_mediado_por_credito` | **IDENTIFICADO** | ENIGH `Sí` (`tarjeta`/`pagotarjet`/`gastotarjetas`) × celdas ENIGH de 4 ejes estrictos (formalidad, edad, urbanización, ingreso). Nivel y pendiente separables con ≥2 celdas |
| `civico.denuncia.con_seguro` | **IDENTIFICADO** | ENVIPE `Sí` — `BP2_1` (vehículo asegurado) × `BP1_20` (denunció) × `BP1_28`, mismo instrumento; celdas ENVIPE edad × urbanización (2 ejes estrictos) |
| `tramite.mordida.con_registro` | **IDENTIFICADO en nivel · TRUNCADO en atributos** | ENCIG `Sí (estructural)` — `P7_3` × `P8_4-P8_7` vía llave `N_TRA`. El nivel se identifica con una celda; condicionarlo **no puede** hacerse sobre ingreso (ENCIG `No`) ni sobre ruralidad (universo ≥100k) |
| `salud.atencion.grave` | **JUSTO IDENTIFICADO** | Solo ENSANUT y solo `Parcial` (`H0409A-D`, códigos 2/3). Existe únicamente en régimen laxo; celdas ENSANUT de 3 ejes estrictos. Sin holgura |
| `salud.prevencion.hombre_sin_permiso` | **INIDENTIFICABLE** | Una de las **8 ausentes** (re-derivadas en §0.3): revisada contra las 8 fuentes y sin desenlace observable. Cero momentos. **No es un problema de segmentación** — sobrevive intacta al reencuadre |
| `tramite.gobierno_digital.coercitivo` | **INIDENTIFICABLE** | El desenlace de adopción se observa (ENCIG `Sí`), pero **lo que la regla distingue no**: el inventario dice de ENIF *"sin distinguir coerción/utilidad"* (l.337) y de ENCIG *"Sí (adopción) / **falta motivo**"* (l.338). Sin el contraste coerción/utilidad, las dos ramas no se separan |
| `tramite.gobierno_digital.util_sin_coercion` | **INIDENTIFICABLE** | Misma fila, mismo motivo. Es la rama complementaria del mismo contraste no observado |

⚠️ Las dos últimas son **hallazgo nuevo de esta sesión**: INV-SEG p3 §Prueba 1 las contó entre las *"12 de 14 alcanzables"* porque leyó `Sí` en la columna de fuente. El `Sí` es sobre **adopción**, no sobre el **motivo** que la regla predice. Más celdas no lo arreglan: el reactivo del contraste no está en ninguna de las dos fuentes.

#### Coeficientes de generador — 15 g.l.

| gen · coeficiente | estatus | celda o momento que lo sostiene |
|---|---|---|
| **G1** `radio_confianza` | **IDENTIFICADO** | C1 ENCUCI `AP5_1_1/2/3` · C2 ENCUCI observa `tramite.mordida.discrecional` `Sí` (`AP5_17`/`AP5_18`), G1 · C3 variables distintas · C4 ENCUCI 3 ejes estrictos / 6 laxos. ⚠️ **no** usar `cooperacion.confianza.puente_personal` como desenlace: su variable observada **es** `AP5_1_2`, el propio reactivo — sería circular |
| **G1** `confianza_institucional` | **IDENTIFICADO · TRUNCADO** | C1 ENCIG batería XI · C2 ENCIG observa `tramite.mordida.discrecional` `Sí` (`P8_3_1/2/3`), G1 · C3 ✔ · C4 **truncado**: solo edad en estricto; sin ingreso ni ruralidad en ningún régimen. ⚠️ hereda el supuesto de **pendiente común a los 6 componentes** (ADR-49 D3), declarado y no medido |
| **G3** `familismo_apoyo` | **IDENTIFICADO** | C1 ENIF `P9_9_4` · C2 ENIF observa `dinero.ahorro.volatilidad_horizonte_corto` `Sí` (`P4_10`), G3 · C3 variables distintas · C4 ENIF **6 ejes estrictos**, la malla más rica del corpus |
| **G4** `exposicion_violencia` | **IDENTIFICADO · TRUNCADO** | C1 ENVIPE `BP1_20` (victimización) · C2 ENVIPE observa `comunicacion.inseguridad.ver_oir_callar` `Parcial` (`BP1_23`), G4 · C3 variables distintas · C4 **truncado**: ENVIPE sin digital ni migración; el ingreso solo como `ESTRATO` de área, no declarado |
| **G4** `confianza_institucional[justicia]` | **JUSTO IDENTIFICADO** | C1 solo por **proxy** (ENVIPE `AP5_5_*`, percepción de corrupción) · C2 mismo instrumento, `ver_oir_callar` · C3 ✔ · C4 truncado. Un solo desenlace, `Parcial`, con proxy: cero holgura. La ruta limpia —batería XI de ENCIG— **no sirve**: ENCIG no observa ningún desenlace de G4 (`grep` de G4 en Tabla B: ni protesta, ni autodefensa, ni ver-oír-callar), y el IPF no crea esa conjunta (§1.d) |
| **G5** `familismo_obligacion` | **INIDENTIFICABLE** | Falla C1 con **ausencia determinable** (§3.5 prioritario, rejilla completa). Y falla antes que eso: `procedencia.yaml` lo declara *"signo negativo o no monotónico — **SIN MAGNITUD**"*. Un parámetro sin forma funcional declarada no lo identifica ningún número de momentos. Ver §3.b |
| **G6** `deferencia` | **INIDENTIFICABLE** | Falla C1 con **ausencia determinable** (§3.2 prioritario, las 8 en `No`) **y** falla C2: de las 3 reglas de G6, `trabajo.jerarquia` es todo-`No`, `comunicacion.retroalimentacion` es todo-`No`/no-equivalente, y solo `trabajo.rotacion` tiene un `Parcial` (ENOE `P9D`) — que no coexiste con ningún reactivo de deferencia |
| **G2** `sens_estatus` | **NO DETERMINABLE EN ESTE RÉGIMEN** | El desenlace **sí** existe (ENIGH `Sí`, `gastotarjetas`) y las celdas también (4 ejes estrictos). Falla C1: ningún reactivo de sensibilidad a estatus **reportado**, y §3.1/§3.9 son dominios no prioritarios → no se puede distinguir "no reportado" de "no existe" sin ir a la fuente. **No se colapsa a negativo** |
| **G4** `sens_estatus` | **NO DETERMINABLE EN ESTE RÉGIMEN** | Mismo fallo de C1. Además C2 exigiría el reactivo dentro de ENVIPE, cuyo estatus en §3.1 no está graduado |
| **G2** `aversion_riesgo` | **NO DETERMINABLE EN ESTE RÉGIMEN** | Sin reactivo reportado (§3.1 no prioritario). El único candidato, ENIF `P5_23`/`P5_24`, mide **conocimiento de protección de depósitos**: es el moderador que la regla `dinero.ahorro.seguro_deposito_atenua_aversion` pone en el `SI`, no una medida de aversión |
| **G3** `aversion_riesgo` | **NO DETERMINABLE EN ESTE RÉGIMEN** | Ídem |
| **G3** `horizonte_temporal` | **NO DETERMINABLE EN ESTE RÉGIMEN** | C1 solo por proxy (ENIF `P4_10`), y con ese proxy **falla C3**: `P4_10` es la variable con la que Tabla B observa `dinero.ahorro.volatilidad_horizonte_corto`, el desenlace de G3 — regresar el desenlace sobre sí mismo. El otro desenlace G3 en ENIF (`trabajo.prestaciones...`) es `Parcial` y el inventario lo declara *"sin desenlace de valoración"*. Si existe otro reactivo de horizonte, §3.1 no prioritario impide saberlo |
| **G4** `horizonte_temporal` | **NO DETERMINABLE EN ESTE RÉGIMEN** | Exigiría reactivo de horizonte en ENVIPE. Tabla A eje 4 verifica que **ENVIPE no tiene pregunta de ingreso** (`grep -i "ingreso"` solo en la batería de prioridades de política); de ahí no se sigue que no tenga una de horizonte de ahorro, y §3.1 no está graduado para ENVIPE |
| **G5** `familismo_apoyo` | **NO DETERMINABLE EN ESTE RÉGIMEN** | Distinto de su gemelo en G3, y por eso se reporta aparte: el reactivo (ENIF `P9_9_*`) y el desenlace G5 en ENIF (`familia.seguro.volatilidad_ausencia_estado`, `Sí`) son **la misma variable** — Tabla B l.171 observa esa regla precisamente con `P9_9_1..6`. Falla C3. El otro desenlace G5, `salud.adherencia`, vive en §3.4 (no prioritario) y ENIF no aparece en esa fila |
| **G5** `radio_confianza` | **NO DETERMINABLE EN ESTE RÉGIMEN** | C1 ✔ (ENCUCI). C2 falla en el dominio graduado: §3.5 es prioritario y ENCUCI está en `No` en las cuatro reglas de familia. El único resquicio es `salud.adherencia` (§3.4, no prioritario), donde ENCUCI no tiene fila — no determinable, no negativo |

#### Agregado

| estatus | probabilidades (g.l.) | coeficientes | total sobre 22 |
|---|---|---|---|
| **IDENTIFICADO** (2 de ellos truncados en atributos) | 3 | 4 | **7** |
| **JUSTO IDENTIFICADO** (cero holgura, infalsable) | 1 | 1 | **2** |
| **INIDENTIFICABLE** (ausencia determinable) | 3 | 2 | **5** |
| **NO DETERMINABLE EN ESTE RÉGIMEN** | 0 | 8 | **8** |
| | 7 | 15 | **22** |

**Nueve de 22 grados de libertad tienen un momento que los sostenga, y dos de esos nueve sin holgura alguna.** Trece no lo tienen o no se puede saber en este régimen. **El conteo de momentos vuelve a pasar y la estructura vuelve a fallar** — el mismo veredicto de INV-SEG p3, por una causa distinta y ahora localizada: no es que falten celdas, es que **faltan reactivos de parámetro co-observados con desenlaces**.

---

## 3 · Los dos hallazgos que el reencuadre no arregla por construcción

### 3.a · G3/G5 justo identificados con cero grados de libertad — **PERSISTE**

**Veredicto: PERSISTE — problema del modelo, no de la segmentación.**

Lo que sí cambia, y se reconoce sin regatear: **el "ajusta perfecto por construcción" desaparece.** Con condicionales sobre 6 ejes, cada generador expone 7 cantidades (6 pendientes compuestas + intercepto) contra un número de celdas que puede ser mayor. El empate exacto de 3 coeficientes contra 3 celdas que producía cero holgura en INV-SEG p3 §Prueba 2 **ya no ocurre**. En ese sentido literal, sí hay momentos sobrantes.

Y aun así el hallazgo persiste, por dos razones derivadas arriba:

1. **Lo sobrante sobra contra el compuesto, no contra el coeficiente.** Lo que las celdas sobre-determinan es Σ_k β_gk·γ_kj, no β_gk (§2.b). Para G3, los tres coeficientes salen **NO DETERMINABLE ×2 + IDENTIFICADO ×1**; para G5, **NO DETERMINABLE ×2 + INIDENTIFICABLE ×1**. El estado pasa de *"ajusta perfecto y no se puede refutar"* a *"no se puede fijar"*. **No es una mejora de identificabilidad: es la misma infalsabilidad, movida de sitio.**
2. **Solo la cláusula de G3 se vuelve comprobable; la de G5 no.** Las cláusulas falsables de §2.1 están escritas a nivel de **desenlace**, no de coeficiente, así que no dependen del compuesto:
   - **G3** — *"se refuta si al estabilizarse el ingreso el horizonte no se alarga"*: con celdas de formalidad × ingreso dentro de ENIF, y `P4_10` como desenlace, esto **es comprobable**. Hay malla y hay desenlace en el mismo instrumento. **Esta mitad sí la rescata el reencuadre.**
   - **G5** — *"se refuta si `familismo_obligacion` alto mejora simultáneamente bienestar y logro individual"*: exige medir `familismo_obligacion`, que no tiene reactivo (ausencia determinable, §2.c) ni magnitud declarada. **Ninguna celda de atributos la vuelve comprobable.** Es el mismo hallazgo 3(b) visto desde el generador.

No se suaviza el resultado a "RESUELTO" por la mitad que mejora: un veredicto RESUELTO enterraría el lado G5, que es el que el encargo existe para no enterrar. Lo que corresponde declarar es que **G3 sale de la clase infalsable a nivel de cláusula y no a nivel de coeficientes, y G5 no sale de ninguna de las dos.**

### 3.b · El check ADR-30 de familismo sin contraste apoyo/obligación — **PERSISTE**

**Veredicto: PERSISTE — problema del modelo, no de la segmentación.**

El check obligatorio, verbatim de `procedencia.yaml` y `modelo` §2.1: *"una configuración donde `familismo_obligacion` alto mejore TODOS los desenlaces se rechaza en compilación. Si el modelo no puede producir el caso en que la familia daña, el parámetro es adorno."*

**¿Alguna celda de atributos produce ese contraste?** No, y por **cuatro** vías independientes — cualquiera de ellas basta:

1. **Ninguno de los 6 ejes mide familismo.** La malla se construye sobre formalidad, edad, urbanización, ingreso, digital y migración. Ninguno separa apoyo de obligación; una celda de atributos puede correlacionar con familismo pero no lo **contrasta**, y un check que exige el caso en que la familia daña necesita el contraste, no la correlación.
2. **Solo existe reactivo del lado del apoyo, y en dominio graduado.** §3.5 es PRIORITARIO: la rejilla de 8 fuentes está completa y es legible. El único `Sí` que toca el constructo es ENIF `P9_9_4` — *"¿con qué piensa cubrir su vejez? … familia"*, que es **recepción esperada de apoyo**. **No hay contraparte de obligación** en ninguna de las ocho. Esto **no** es "no reportado": es ausencia determinable en un dominio prioritario.
3. **El candidato aparente es circular.** ENUT `Sí` en `familia.cuidado.recae_mujeres_40mas` (`P6_11_*`/`P6_12_*`/`P6_13_*`, tiempo de cuidado) parece medir carga = obligación. No sirve: **el tiempo de cuidado es el desenlace que G5 predice**, no el parámetro. Usarlo como θ es regresar el desenlace sobre sí mismo — el mismo fallo de C3 que ya inhabilita el par ENIF de G5 (§2.d). Y el otro flujo familiar de ENUT (`P3_20_3/4`) mezcla explícitamente *"familiares o amistades"*, con lo que ni siquiera aísla a la familia.
4. **Aquí es donde muerde la restricción (a) de P1, y es la razón estructural.** Apoyo y obligación divergen **dentro del hogar**: la hija cuidadora carga obligación mientras su hermano recibe apoyo, bajo el mismo techo. Ese es el contraste que el check necesita. Los tres ejes que podrían aproximar posición relativa —urbanización, ingreso, acceso digital— son **de nivel hogar** y **por diseño del instrumento asignan el mismo valor a las dos personas** (P1 §3). El contraste que separa apoyo de obligación cae exactamente en la dimensión que la malla no resuelve, y no por hueco de esta sesión: por diseño de las encuestas.

A eso se suma un fallo previo a todo dato: `familismo_obligacion` está declarado *"signo negativo o no monotónico — **SIN MAGNITUD**"*. **Sin forma funcional declarada no hay cantidad que estimar.** Un parámetro así no es inidentificable por escasez de momentos: es inidentificable por especificación, como `confianza_institucional` lo era por `D-12` bajo perfiles. El reencuadre disolvió aquel hueco (§4) y **no toca este**.

⚠️ Nota de disciplina: ambos veredictos de §3 se apoyan en dominios **PRIORITARIOS** (§3.2, §3.5), donde el inventario trae la rejilla completa contra las 8 fuentes. **No se están leyendo como negativo unos huecos del régimen laxo.** Donde el régimen impide saber —`sens_estatus`, `aversion_riesgo`, los slots de §3.1/§3.4— el estatus es NO DETERMINABLE, y así aparece en §2.d.

---

## 4 · Qué pasa con la clase "inidentificable con cualquier número de momentos"

INV-SEG p3 §3.C declaró **4 de 29** en esta clase. Re-derivada bajo el reencuadre, miembro por miembro:

| miembro según INV-SEG p3 | ¿sobrevive al reencuadre? | por qué |
|---|---|---|
| `salud.prevencion.hombre_sin_permiso` (contaba 2 valores) | **SOBREVIVE** — ahora **1 g.l.**, no 2 (simplex, §0.2) | Es una de las 8 ausentes: desenlace revisado y no observable en las 8 fuentes. Nunca fue un problema de segmentación |
| **G1** `confianza_institucional` | **SALE de la clase** | INV-SEG la puso ahí porque §1.1 no da valor por perfil y `D-12` está abierta — un **hueco de especificación de la tabla de perfiles**. El reencuadre **elimina la tabla**: θ pasa a estimarse como condicional, y hay reactivo (ENCIG batería XI) co-observado con un desenlace G1 (`tramite.mordida.discrecional`). Pasa a **IDENTIFICADO · TRUNCADO** |
| **G4** `confianza_institucional[justicia]` | **SALE de la clase** | Mismo argumento; ruta por proxy ENVIPE `AP5_5_*` co-observado con `ver_oir_callar`. Pasa a **JUSTO IDENTIFICADO** — sin holgura, pero fuera de la clase |
| *(el cuarto miembro era el segundo valor de `hombre_sin_permiso`)* | **absorbido por el simplex** | Los 2 valores de una regla binaria son 1 g.l. |

| entra a la clase (hallazgo nuevo de esta sesión) | por qué |
|---|---|
| `tramite.gobierno_digital.coercitivo` (1 g.l.) | El contraste coerción/utilidad no se observa en ninguna de las dos fuentes que traen la regla — inventario, literal: ENIF *"sin distinguir coerción/utilidad"*, ENCIG *"falta motivo"*. INV-SEG p3 la contó entre las alcanzables por leer el `Sí` de adopción |
| `tramite.gobierno_digital.util_sin_coercion` (1 g.l.) | Rama complementaria del mismo contraste no observado |
| **G5** `familismo_obligacion` | Ausencia determinable de reactivo en dominio prioritario **más** ausencia de magnitud/forma funcional declarada. Ver §3.b |
| **G6** `deferencia` | Ausencia determinable de reactivo (§3.2, las 8 en `No`) **y** de desenlace co-observado en 2 de las 3 reglas de G6. ⚠️ INV-SEG p3 §Prueba 2 marcaba G6 **"OK"** en los tres escenarios — ese veredicto valía bajo perfiles, donde θ venía dado por §1.1. **Bajo el reencuadre G6 empeora**, y es el ejemplo más limpio del intercambio de §2.b: se cambió un supuesto por una medición que no existe |

**La clase pasa de 4 miembros (en cuenta de valores) a 5 grados de libertad, y rota casi por completo: salen 2, entran 4.** No se encoge. Es el hecho central del veredicto global: el reencuadre **reubica** la subidentificación en vez de disolverla.

---

## 5 · Veredicto global y recomendación para el acto de sello

### **ADR-50 SE REESCRIBE.**

El criterio del encargo era binario y explícito: *SE CORRIGE* si cambia la unidad y sobrevive el método; *SE REESCRIBE* si la subidentificación persiste sobre atributos. **Persiste**: 5 de 22 g.l. son inidentificables con cualquier número de momentos, 8 más no son determinables en este régimen, y solo 7 quedan identificados —2 de ellos truncados— con 2 más justo identificados y por tanto infalsables. El método (ajuste por momentos, ruta 3 de la metodología) **no está refutado y no es lo que se reescribe**. Lo que se reescribe es **la afirmación operativa de ADR-50**: que los libres del ajuste son calibrables por ajuste. No lo eran sobre perfiles y no lo son sobre atributos, por causas distintas.

Un ADR de **corrección** —cambiar "perfil" por "atributo" en el texto de ADR-50 y conservar el resto— produciría un canon **falso en su afirmación central**, porque el obstáculo se movió de la segmentación a la medición de parámetros, y esa mudanza no cabe en un cambio de unidad.

### Recomendación de una página para la mesa

**1 · Lo que la reescritura debe conservar sin tocar.** El método. La reformulación identificación→ajuste sigue siendo correcta y la revisión la refuerza. Lo que ADR-50 acertó fue la ruta; lo que erró fue declarar calibrable un conjunto que no lo es.

**2 · Lo que la reescritura debe reemplazar: el conjunto "29 libres" por un conjunto particionado.** ADR-50 trata los 29 como una bolsa homogénea de parámetros a calibrar. Debe sustituirse por las cuatro clases de §2.d, con su miembro nombrado y su momento sostenedor: **IDENTIFICADO (7, dos truncados) · JUSTO IDENTIFICADO (2) · INIDENTIFICABLE (5) · NO DETERMINABLE EN ESTE RÉGIMEN (8)**. Un ADR que no distinga las cuatro vuelve a prometer calibración donde no la hay.

**3 · Debe corregir su propia aritmética: 22, no 29.** Los valores de las 13 reglas de `asignados_probabilidad` suman 1.0 sin excepción (§0.2): las 14 probabilidades libres son 7 g.l. La cifra "29 = 14 + 15" está repetida en el texto de ADR-50, en `gobernanza-v1_15.md` §4 y en `estado-programa-v1_9.md` L0. La reescritura debe fijar **22 = 7 + 15** y disparar la retropropagación de ADR-29 sobre esos tres artefactos.

**4 · Qué debe decir sobre los 4 inidentificables de INV-SEG p3.** Que **la clase no se resolvió: rotó** (§4). Salen los dos slots de `confianza_institucional`, porque su causa era `D-12` sobre la tabla §1.1 y el reencuadre elimina esa tabla — lo que confirma la lectura de `revision §3` de que **D-12 se disuelve**, y esta nota aporta la derivación que esa revisión pedía *("verificar antes de cerrarla")*. Entran cuatro miembros nuevos: las dos ramas de `tramite.gobierno_digital.*`, `familismo_obligacion` y `deferencia`. **Los cuatro nuevos son inmunes a cualquier trabajo de segmentación o de síntesis**: dos por contraste no observado, dos por ausencia determinable de reactivo. La reescritura debe nombrarlos y sacarlos del conjunto calibrable, no dejarlos como pendientes.

**5 · Debe declarar la restricción que el IPF no levanta.** La síntesis reproduce marginales; no fabrica la conjunta (parámetro, desenlace) que ninguna encuesta midió (§1.d, y la propia revisión §7 lo dice de sí misma). De ahí sale el criterio C1-C4 de §2.b, que es lo que debería sustituir al *"declarar los momentos antes de ajustar"* de ADR-50 §(3): no basta declarar momentos, hay que declarar **el par (reactivo de parámetro, desenlace) co-observado en un mismo instrumento**.

**6 · Qué hacer con ADR-50 §(1), la exención de los 90 `params_base`.** `revision §2` sostiene que la exención *"vuelve a ser verdadera, porque medir condicionales sobre atributos observables sí es posible en transversal"*. **Es verdadera solo para 4 de los 9 parámetros de generador** (los que tienen reactivo: `radio_confianza`, `confianza_institucional`, `exposicion_violencia`, `familismo_apoyo`), más 2 por proxy con reservas. Para `familismo_obligacion` y `deferencia` es falsa con ausencia determinable; para `sens_estatus` y `aversion_riesgo` no es determinable en este régimen. La reescritura debe **acotar la exención a la lista nombrada**, no concederla en bloque.

**7 · Los dos hallazgos que la reescritura no puede declarar resueltos.** G3/G5 y el check ADR-30 **PERSISTEN**, y no como deuda de dato: como **problema del modelo**. `familismo_obligacion` sin magnitud declarada y `deferencia` sin reactivo no son pendientes de trabajo de campo — son parámetros que el modelo postula y que nada puede fijar. La mesa tiene ahí una decisión que ADR-50 no puede tomar por ella: **retirarlos del modelo, o declararlos explícitamente no calibrables y aceptar que los generadores que los usan (G5 y G6) no son falsables por ajuste.** Mientras no se tome, el check obligatorio de ADR-30 sigue sin poder correrse, y G6 —que INV-SEG p3 daba por sano— entra a la lista.

**8 · Lo que esta nota NO decide.** No propone el diseño nuevo de §1.1 (es decisión de mesa). No estima cobertura ni corre IPF. No toca `4 de 144` ni el denominador (`revision §6.3`). No cierra `D-12`: aporta la derivación de que su premisa se disuelve bajo el reencuadre, y cerrarla es acto de mesa. No resuelve el asunto que INV-SEG p3 §Prueba 3 dejó abierto —las 34 reglas sin valor numérico que un ABM ejecutable necesitaría—, que sigue siendo decisión de mesa y sigue cambiando el denominador.

---

## Límites declarados

- **El régimen asimétrico manda, y se respetó.** Ocho de los 15 coeficientes quedan **NO DETERMINABLE EN ESTE RÉGIMEN**, no negativos: sus parámetros viven en §3.1/§3.4/§3.9, dominios donde Tabla B solo trae filas sí/parcial y no se puede distinguir "no reportado" de "no existe". **Determinar esos ocho exige ir a la fuente, y este encargo no va a la fuente.** Los dos INIDENTIFICABLE de coeficiente (`familismo_obligacion`, `deferencia`) sí son determinables: viven en dominios PRIORITARIOS con rejilla completa contra las 8 fuentes.
- **El criterio C1-C4 de §2.b es una derivación de esta sesión**, no un resultado medido. Se apoya en un supuesto declarado: que la condicional θ_k(x) sea lineal en los ejes. Con condicionales no lineales el conteo de compuestos cambia; **la no-separabilidad β·γ no cambia**, que es lo que sostiene el veredicto.
- **No se validó ninguna correspondencia atributo↔parámetro con dato.** Que ENCUCI `AP5_1_*` mida `radio_confianza`, o ENIF `P9_9_4` mida `familismo_apoyo`, es lectura de esta sesión sobre la etiqueta reportada en el inventario. Nadie ha comprobado la validez de constructo, y sin microdato no se puede.
- **Las cotas de INV-SEG p3 §Prueba 2 no se re-usaron** (estaban calculadas promediando celdas-unión y tratando ordinales como cardinales, contra ADR-28.a). Esta nota no hereda esos rangos: sustituye el análisis de rango por el criterio de co-observación, que no necesita cardinalizar nada.
- **`CAL-CONF` Fase B sigue sin existir** como artefacto. `revision §2` la redefine como *"medir confianza por institución condicionada a atributos observables"*; §2.d de esta nota indica dónde puede hacerse (ENCIG batería XI) y sobre qué atributos **no** puede (ingreso, ruralidad).
- **No se verificó nada contra disco.** Ni manifiesto, ni hashes, ni presencia de las fuentes citadas en `calibrable_con`. Fuera de perímetro por diseño del encargo — misma salvedad que ADR-50 declara para sí mismo.
- **Los scripts de derivación viven en el scratchpad de la sesión, no en el repo.** Sus salidas crudas están transcritas íntegras arriba (§0.1, §0.2, §1.c, §1.d, §2.a); las entradas son `milpa/procedencia.yaml`, `canon/modelo-decision-v3_4.md` §3.B y `forense/notas/2026-07-31-inventario-segmentacion.md`.

---

## Adenda 04/ago/2026 — `:229` y `:264` quedan vencidas, no corregidas en la fila

**Disciplina aplicada:** adenda fechada, append-only, mismo mecanismo que
`forense/hitoE-campana-medicion-v2_0.md` §15/§16. Las filas `:229` y `:264`
no se editan.

**Qué pasó.** `:229` describe el trío `BP1_20`/`BP1_23`/`BP1_28` de ENVIPE
como *"(victimización, denuncia y sus razones)"*, y `:264` cita "C1 ENVIPE
`BP1_20` (victimización)". La sesión que ejecutó la posición 4 de la cola
(`PR #57`, `forense/notas/2026-08-04-cal-conf-faseb-medicion-pos4.md`)
verificó el descriptor de ese trío contra `fd_envipe2025.pdf` y encontró que
no mide `exposicion_violencia`: `BP1_20` es *"¿Acudió a denunciar el
delito?"*, condicionado por construcción a ya haber sido víctima — mide
conducta de denuncia, no exposición a violencia. Registrado en
`forense/hallazgos.md` (04/ago/2026) y propagado en `hitoE` §15.

**Por qué no se edita la fila.** `:229` marca el trío como **reportado**
(estado del inventario), no **verificado** contra el cuestionario — la
distinción que `instrucciones` v2.1 exige. La fila no mintió: dijo de dónde
venía el dato sin verificarlo, y quien la citó después (la fila 4 de la cola
vieja, corregida en `hitoE` §15) leyó *reportado* como si dijera
*verificado*. Ese es el defecto real, y es transferible: la columna de
estado de una tabla es parte de la afirmación, no decoración. Editar `:229`
borraría el registro de que ese salto de lectura ocurrió. Detalle en
`forense/notas/2026-08-04-barrido-escritorio-pendientes.md` §7.
