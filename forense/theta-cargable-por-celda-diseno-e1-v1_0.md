# DISEÑO E1 · θ cargable por celda — esquema de identificación (v1.0)

`ACTO GEN2-E1-DISENO-CALIBRACION-1`, 16/sep/2026, NUBE. Objeto: `NC-0239`
(`ACTO GEN2-MARCADOR-C0-D`, `ADR-520`, 15/sep/2026 — `theta.valor()` lanza
`ThetaNoDisponible` en 43/43 entradas), autorizado por `F-18`
(`forense/encargos/2026-09-16-GEN2-FIRMAS-MESA-3.md`).

**Qué es esto y qué no es.** Es el diseño del esquema que hace falta para
que una celda pueda declarar, de forma verificable por máquina y no solo
en prosa dispersa, si su θ es cargable — y con qué garantías. No es una
corrida: **cero números nuevos**, `milpa/src/theta.py` y
`milpa/src/motor.py` intactos (verificado: `git status --porcelain
milpa/src/theta.py milpa/src/motor.py` vacío antes y después de este
acto). El primer resultado que produzca la corrida de calibración es
trabajo de un acto de caja posterior, sobre la spec que este documento
deja congelada.

## 1 · Por qué `procedencia.yaml` no basta tal como está

`milpa/procedencia.yaml` (1474 líneas, 144 números censados desde
v0.1.0) ya trae, disperso y con vocabulario distinto según la sección en
que se escribió, gran parte de lo que un cargador necesitaría:

- **`escala`** aparece explícita en `rutas_estimabilidad_coeficiente.detalle`
  (`escala_asignado`/`escala_fuente`/`escala_derivada`, censo `ACTO
  ESCALAS-COMPLETAS-P1`, 25/ago/2026), en `coeficientes_generador_sellados`
  (`escala:`), y en las entradas más nuevas (`candidatas_theta_citadas_fp190`,
  `thetas_informativas`). Está **ausente** como campo propio en
  `medidos`, `derivados`, `asignados_probabilidad` y
  `asignados_coeficiente.detalle` — se infiere de contexto (son
  probabilidades de rama SI-ENTONCES, `[0,1]`), pero A-bis regla 3 exige
  que la escala se **declare**, no que se infiera.
- **`universo`** aparece explícito en las secciones `condicionales_*` (los
  seis componentes de confianza institucional, `radio_confianza`,
  `familismo_apoyo`, `confianza_institucional_generico_servidores_publicos`,
  `exposicion_violencia`, `norma_de_género`, `obligación_medida`) y en
  las dos entradas de `coeficientes_generador_medidos` con universo
  restringido (`G4_exposicion_violencia`, `G4_confianza_institucional_justicia`).
  Está **ausente** como campo propio en `medidos`/`derivados`/
  `asignados_probabilidad`/`asignados_coeficiente` — varias de esas
  entradas sí traen un `universo:` suelto dentro de `medidos` (líneas
  707-726), pero no es sistemático: la mitad de `medidos` no lo trae.
- **El argumento de identificación (o su ausencia)** está, de hecho, ya
  escrito para casi todos los `MEDIDO·β̂` — con las palabras exactas de
  A-bis 1/2 ("asociar ≠ identificar", "A-bis regla 2", "NINGUNA lectura
  causal") — pero como **prosa en `nota`/`adr57_a`/`marca_c2`/`marca_c3`**,
  no como un campo con vocabulario cerrado que un validador pueda leer.
  El único intento de identificación genuina del archivo
  (`G3_horizonte_temporal`, llave `ADR-57(c)` (i), `GATE·ID-X`) **no
  alcanzó potencia** con datos reales — el propio archivo lo dice: "el
  gate detiene el acto antes de cruzar... no tiene potencia suficiente".

La consecuencia práctica: hoy nada impide que un cargador futuro lea un
`β̂` marginal de `coeficientes_generador_sellados` y lo trate como
coeficiente identificado, porque "identificado" y "asociación medida" se
escriben con el mismo tipo de campo (`clase`, `nota`) en secciones
distintas del archivo, con redacciones distintas. **θ cargable por celda
exige que esa distinción sea estructural, no de estilo de redacción.**

## 2 · El esquema (tres campos, vocabulario cerrado)

Toda entrada nombrada de `procedencia.yaml` que aspire a ser cargada por
celda declara, de aquí en adelante, tres campos. Los tres son
**metadato sobre un número que puede no existir todavía** — declarar el
esquema no crea ni corrige ningún valor.

### 2.1 `escala`

Uno de:

- `PROPORCION_PONDERADA_01` — proporción/prevalencia ponderada, dominio `[0,1]`.
- `DIFERENCIA_DE_PROPORCIONES` — β̂ marginal o condicional, dominio `[-1,1]`, **nunca** comparable en magnitud contra `PROPORCION_PONDERADA_01` sin función de enlace declarada (A-bis regla 3, ya citada así en el propio archivo: "no comparable en magnitud... ningún ADR de D-ABC ha sellado función de enlace").
- `ORDINAL_CARDINALIZADO(n)` — etiqueta cualitativa de ficha convertida a número sobre una escala ordinal de `n` puntos (p. ej. `pr02` 1-7); la cardinalización en sí no tiene respaldo (`hallazgo_ordinal_cardinal`, ya en el archivo).
- `CATEGORICA_NOMINAL(k)` — `k` categorías sin orden (p. ej. situación conyugal, 7 vías).
- `INDICE_SIN_ENLACE_DECLARADO` — el caso de los 15 coeficientes de generador: `canon/modelo-decision-v4_0.md` §2.1-2.2 no declara escala/unidad numérica para ninguna salida de generador (ya medido así por `ACTO ESCALAS-COMPLETAS-P1`, `escala_derivada: SUBDETERMINADA-PERSISTENTE` en 9 de 15 pares).
- `ESCALA_NO_DERIVABLE` — el token que `rutas_estimabilidad_coeficiente.detalle` ya usa cuando ninguno de los dos extremos (θ, salida del generador) declara unidad.

### 2.2 `universo`

Texto libre, pero con tres requisitos mecánicos (ya varias entradas los
cumplen; el esquema los hace obligatorios):

1. Instrumento + año + tabla/reactivo (nunca solo "ENVIPE" o "ENIF" a secas).
2. Filtro de elegibilidad exacto (edad, condición de aplicabilidad, no-blancos) — si el filtro selecciona sobre una variable relacionada con el desenlace, se declara como tal (colisionador/selección, mismo criterio que `G4_confianza_institucional_justicia` ya declara).
3. Si el universo es una **subpoblación** (p. ej. "18+ que trabajan"), se declara así explícitamente y **no se reconcilia contra un marginal poblacional sin recalcular el marginal al mismo universo** (A-bis regla 4, ya citada verbatim en `confianza_institucional_generico_servidores_publicos`).

Caso especial declarado aquí, no antes: los **90 `params_base_de_perfil`**
(`resumen.desglose.params_base_de_perfil`, valores viven en
`canon/modelo-decision-v4_0.md`, no en este archivo) no tienen universo
en el sentido de 1-3: su "universo" es un **perfil arquetípico** (una de
seis tipologías de la ficha canónica), no una subpoblación muestreada.
Se declara `universo: TIPOLOGIA_NO_MUESTRAL(perfil)` — un valor de
`universo` que el esquema admite explícitamente para no forzarlo a
parecer una subpoblación real que no es.

### 2.3 `identificacion`

Uno de dos, nunca un tercero inventado:

- **`ARGUMENTO_EXPLICITO: <método>`** — solo si existe un mecanismo que
  rompa la confusión declarada en A-bis regla 1 (diseño experimental de
  terceros, discontinuidad, variación exógena declarada y defendida
  *antes* de ver el desenlace, panel con efectos fijos que aíslen la
  vía). Hoy, censado el archivo completo, **ninguna entrada de
  `procedencia.yaml` alcanza este valor para el modelo propio**: el
  único intento (`G3_horizonte_temporal`, panel ENNViH/MxFLS,
  `GATE·ID-X`) declaró de antemano su argumento de identificación
  (efectos fijos de hogar) y **el propio gate lo detuvo por falta de
  potencia** antes de producir un estimando — no llegó a identificar
  nada, así que no hay una entrada con `ARGUMENTO_EXPLICITO` que citar
  todavía. `evidencia_experimental_terceros`
  (`dinero.credito.baja_friccion_usura_dano_downstream`, RCT de
  Compartamos) sí tiene argumento de identificación **para su propio
  experimento** — pero el propio archivo ya declara que no calibra ni
  sustituye la magnitud de la regla de este modelo: identifica el
  mecanismo ajeno, no la θ propia.
- **`AUSENCIA_DECLARADA(A-bis 1/2): <por qué>`** — el caso por defecto,
  y hoy el único que el archivo puede sostener con evidencia: co-observar
  θ y desenlace (A-bis 1) o condicionar sobre un eje (A-bis 2) no
  identifica nada sin argumento adicional. La razón concreta ya está
  escrita, entrada por entrada, en la mayoría de los `MEDIDO·β̂`
  (`nota`/`adr57_a`/`marca_c2`): "asociar ≠ identificar", frecuentemente
  con evidencia de que condicionar **invierte el signo** del marginal
  (`G1_radio_confianza`, `G1_confianza_institucional`,
  `G3_familismo_apoyo`: la mayoría o totalidad de las celdas invierten
  signo al condicionar — la ilustración empírica más directa de por qué
  A-bis regla 2 existe).

No hay un tercer valor. Una entrada sin ninguno de los dos declarado
**no está lista para cargarse por celda** — se marca `FALTA-IDENTIFICACION`
en el censo de la sección 3, y el motor no la consume hasta que alguien
(mesa o un acto de medición) escriba uno de los dos.

## 3 · Censo, nombre por nombre

Unidad de censo: el nombre addressable que el resto del programa ya usa
para citar una entrada (`sección.subnombre`, o `{gen, coef}` donde el
archivo mismo usa esa llave). Cuando un grupo entero comparte los tres
campos (p. ej. los 90 `params_base_de_perfil`), se censa una vez por
grupo y se nombra la excepción si la hay. `LISTO` = los tres campos
existen hoy, aunque sea repartidos en varios campos de la entrada
(`nota`, `universo`, `escala`); `FALTA-X` = ese campo no existe en
ninguna forma reconocible hoy.

| nombre (procedencia.yaml) | escala | universo | identificación | veredicto |
|---|---|---|---|---|
| `condicionales_confianza_institucional.{salud,educación,financiera,seguridad-FFAA,justicia-policía,electoral-partidos}` (6) | implícita (proporción ponderada por ítem); sin token cerrado | presente, explícito por entrada | ausencia declarada de facto ("condicional genuina... no una media puntual"; nunca se llama identificado) pero sin token `AUSENCIA_DECLARADA` | `FALTA-ESCALA` (token) |
| `condicionales_escalares.{radio_confianza,familismo_apoyo}` (2) | implícita | presente | `marca_c3` ya declara circularidad y no-identificación por entrada | `FALTA-ESCALA` (token) |
| `condicionales_escalares_confianza_generica.confianza_institucional_generico_servidores_publicos` | implícita | presente, cita A-bis regla 4 verbatim | presente, cita A-bis regla 2 verbatim | `FALTA-ESCALA` (token) |
| `condicionales_escalares_exposicion_violencia.exposicion_violencia` | implícita | presente | presente ("ninguna lectura causal ni de intervención (A-bis 2)") | `FALTA-ESCALA` (token) |
| `condicionales_escalares_medido_nacional.{norma_de_género,obligación_medida}` (2) | implícita (marginal, `x=∅`) | ausente como campo propio — `fuente` da instrumento/tabla pero no filtro de elegibilidad completo | presente ("no se declara EXISTE-SATISFACE"; cita A-bis regla 3 verbatim en `obligación_medida`) | `FALTA-ESCALA`, `FALTA-UNIVERSO` (filtro) |
| `medidos` (7 entradas `donde:`) | ausente como campo | parcial: 3 de 7 traen `universo:` (líneas 707-726), 4 no | ausente — solo `reserva` textual, sin declarar identificado/no-identificado | `FALTA-ESCALA`, `FALTA-UNIVERSO` (parcial), `FALTA-IDENTIFICACION` |
| `derivados` (9 ítems de lista; 8 declaran `donde:` y el noveno, `{valor: 0.11, de: 0.89, tipo: complemento}`, ni siquiera dice a qué regla pertenece — re-contado contra el archivo por este acto, que corrige el «8 entradas» de su propio borrador) | ausente | ausente (heredaría del `medido`/`asignado` del que derivan, no declarado explícitamente) | ausente — `DERIVADO` es aritmética sobre otra clase, no mide nada por sí mismo; el esquema hereda la identificación de su origen, no declarado hoy | `FALTA-ESCALA`, `FALTA-UNIVERSO`, `FALTA-IDENTIFICACION` (herencia sin declarar) |
| `asignados_probabilidad` (13 reglas, ~29 valores) | ausente (implícita `[0,1]` de rama SI-ENTONCES) | ausente como campo — "calibrable_con" nombra instrumento pero no universo/filtro | ausencia declarada de facto en cada `que_sostiene_de_verdad` ("sostiene la dirección, no la magnitud") pero sin token | `FALTA-ESCALA`, `FALTA-UNIVERSO`, `FALTA-IDENTIFICACION` (token) |
| `evidencia_experimental_terceros.dinero.credito.baja_friccion_usura_dano_downstream` | presente (`escala:`, con advertencia de no-comparabilidad ya citando A-bis regla 3) | presente, con A.10 explícito | presente — identificación real, pero **del experimento de terceros**, no de la θ propia del modelo (el propio archivo lo aísla: "NO calibra ni sustituye la magnitud... de esta regla") | `LISTO` (como evidencia externa; no como θ propia calibrable) |
| `asignados_coeficiente.detalle` (15 pares gen×coef) | ausente como campo en esta sección (sí existe, redundante, en `rutas_estimabilidad_coeficiente.detalle` para los mismos 15 pares) | ausente | ausencia declarada de facto (`diagnostico`: "todos ASIGNADO... el corpus es transversal, da estados no ritmos") | `FALTA-ESCALA` (aquí; existe en la sección hermana), `FALTA-UNIVERSO`, `FALTA-IDENTIFICACION` (token) |
| `rutas_estimabilidad_coeficiente.detalle` (mismos 15 pares) | presente y ya normalizado (`escala_asignado`/`escala_fuente`/`escala_derivada`, `ACTO ESCALAS-COMPLETAS-P1`) | ausente | ausente como campo (la `ruta` RUTA-A/RUTA-I/RUTA-C/SIN-RUTA es un proxy de "hay intento de medir", no de "está identificado") | `LISTO` (escala), `FALTA-UNIVERSO`, `FALTA-IDENTIFICACION` (token) |
| `coeficientes_generador_medidos.{G1_radio_confianza,G1_confianza_institucional,G3_familismo_apoyo,G4_exposicion_violencia,G4_confianza_institucional_justicia}` (5, todas `MEDIDO·β̂`; la sexta llave de la sección es `G3_horizonte_temporal`, censada en su propia fila abajo. `G5_familismo_apoyo` **no está en esta sección** — ver la última fila) | presente (`clase` describe la escala en prosa: "diferencia de proporciones") | presente (universo declarado, con colisionador/selección nombrado cuando aplica) | **presente y ya con el vocabulario correcto**: cada una cita `adr57_a`/`marca_c2`/`marca_c3` con "asociar ≠ identificar" — es la sección más cerca de `LISTO` de todo el archivo | `FALTA-ESCALA` (token cerrado; el texto ya basta para derivarlo) |
| `coeficientes_generador_medidos.G3_horizonte_temporal` (GATE·ID-X) | presente ("no aplica — no hay estimando que escalar") | presente | presente — el único intento de `ARGUMENTO_EXPLICITO` del archivo, **sin potencia**: no produjo identificación, solo confirmó que la llave (i) no alcanza con este panel | `LISTO` (como registro del intento fallido; no produce una θ calibrable) |
| `coeficientes_generador_sellados` (7 pares, override que `matriz.py` consulta) | presente (`escala:` explícito, enlace identidad o lineal según ADR) | heredado de `coeficientes_generador_medidos` (no repetido aquí, pero rastreable por `fuente:`) | presente (`reserva:` repite "asociar ≠ identificar" por entrada; `rotulo: ASOCIACION-MEDIDA·*` es ya, de hecho, un token cerrado) | `LISTO` — la sección más madura del archivo para este esquema; solo falta renombrar `rotulo` a `identificacion` con el vocabulario de §2.3 |
| `candidatas_theta_citadas_fp190.{TIC-01,EMP-05}` | presente (`escala:`, cita A-bis regla 3 verbatim) | ausente como campo propio (el "universo" es el archivo/ola citados, sin filtro de elegibilidad declarado) | ausente — son citas sin generador ("cita, no medición"), el esquema no aplica identificación a algo que no se usa en el motor | `FALTA-UNIVERSO`; identificación `N/A` (declarado, no un hueco) |
| `thetas_informativas.corresidencia_actual` | presente (`escala:`) | presente (`universo:`, con el detalle del catálogo de parentesco) | `N/A` declarado — "clasificación INFORMATIVA... no genera regla, no se le asigna generador" (mesa ya decidió que no compite por identificación) | `LISTO` |
| `params_base_de_perfil` (90, valores en `canon/modelo-decision-v4_0.md`, no en este archivo) | `ORDINAL_CARDINALIZADO` de facto (`hallazgo_ordinal_cardinal` ya lo dice: "la ficha dice horizonte mixto→largo; el YAML dice 0.70") pero sin token | `TIPOLOGIA_NO_MUESTRAL(perfil)` — nuevo en este documento, ningún universo muestral existe hoy | ausencia declarada de facto (`hallazgo_ordinal_cardinal.implicacion`: "ninguna salida... debe reportarse con precisión decimal") pero sin token, y **sin fuente numérica en este archivo** — la deuda de fondo (`deuda_dispersion`, 90 parámetros de dispersión) sigue `ABIERTA`, S2, y bloquea incluso escribir el censo completo de esta fila | `FALTA-ESCALA` (token), `FALTA-IDENTIFICACION` (token), y una `PARO-PREMISA` propia: no se puede congelar universo/escala por valor individual mientras `deuda_dispersion` no liste los 90 con su familia de distribución |
| `propuesta_de_esquema.G5_familismo_apoyo` (1, `MEDIDO·β̂`) — **entrada real alojada en la sección equivocada** | presente en prosa (`clase`/`nota`: "diferencia de proporciones… NO la escala del índice del generador", cita A-bis regla 3) sin token | presente (`n_util` por base, EDER 2017 y ENDIREH 2016 como robustez) | presente (`nota` declara circularidad y contaminación de constructo; nunca se llama identificado) | `FALTA-ESCALA` (token) y, antes que eso, `FUERA-DE-SECCION`: `milpa/procedencia.yaml:1244` la escribe como llave hija de `propuesta_de_esquema:` (línea 1228), no de `coeficientes_generador_medidos:` — `yaml.safe_load` la devuelve fuera de esa sección, así que ningún cargador que recorra `coeficientes_generador_medidos` la vería. Defecto de colocación **preexistente**, ajeno a este acto, que no edita `procedencia.yaml`: declarado aquí, no corregido |

## 4 · Lo que queda congelado hoy

1. El esquema de tres campos (§2), con vocabulario cerrado.
2. El censo de qué nombre tiene qué campo, sección por sección (§3) — un
   mapa de huecos, no una promesa de que todos se llenan igual.
3. El hallazgo de que **ninguna θ propia del modelo alcanza hoy
   `ARGUMENTO_EXPLICITO`**: la sección más avanzada
   (`coeficientes_generador_sellados`) ya rotula sus siete entradas como
   `ASOCIACION-MEDIDA·*`, exactamente lo que `AUSENCIA_DECLARADA(A-bis
   1/2)` formaliza. Cargar θ por celda con el estado actual del corpus
   significa cargar **asociaciones medidas con su ausencia de
   identificación declarada**, nunca coeficientes identificados — y el
   esquema hace esa distinción visible para el motor, no solo para quien
   lea la prosa.
4. El caso especial de los `params_base_de_perfil` (universo tipológico,
   no muestral) y su dependencia dura de `deuda_dispersion` (S2, ABIERTA).

   **ENMIENDA FECHADA (17/sep/2026, `ACTO GEN2-ESQUEMA-E1-CAPA-1`).** No se
   reescribe nada de arriba: se corrige aquí, in situ, la forma en que este
   documento nombra la deuda de dispersión. Donde §2.2 y §3 la cuentan como
   **«90 parámetros de dispersión»**, el conteo vigente es **15 familias de
   distribución**. La cifra de 90 es la de la tabla de perfiles; bajo el v4.0
   la dispersión es parte de la especificación de cada condicional
   (`canon/modelo-decision-v4_0.md` §1.1.B), así que no son 90 números
   sueltos sino 15 familias sin declarar, una por par `gen×coef` —
   `canon/modelo-decision-v4_0.md:806` («Las 15 familias de distribución
   exigidas por `ADR-28.d` no están declaradas»), con el cambio de forma de la
   deuda explicado en `:307` y `:671`. La deuda **no se salda**: mientras las
   15 sigan `NO-DECLARADA`, el check de varianza intra-celda de `ADR-28.d`
   sigue sin poder correr. Lo que cambia es su tamaño y su forma, y que ahora
   es enumerable por máquina: las 15 viven en la sección `dispersion:` de
   `milpa/theta-esquema-e1-v1_0.yaml` —la capa separada que `ADR-531` rama B
   selló («Esquema E1: capa separada»)—, derivadas por código de
   `asignados_coeficiente.detalle`, no transcritas a mano. Declararlas sigue
   siendo alcance de mesa; esta enmienda solo deja de contarlas mal.

   El resto de §4.4 se mantiene: `params_base_de_perfil` conserva su universo
   tipológico (`TIPOLOGIA_NO_MUESTRAL(perfil)`) y su dependencia dura de
   `deuda_dispersion` (S2, `ABIERTA`) — que es esta misma deuda, ahora bien
   contada.
5. Un defecto de **colocación** encontrado al censar, y medido, no
   supuesto: `G5_familismo_apoyo` es una entrada `MEDIDO·β̂` completa
   (β̂, IC por bootstrap de conglomerados, `n_util` por base, reserva de
   circularidad escrita) que vive en `milpa/procedencia.yaml:1244` como
   llave hija de `propuesta_de_esquema:` (línea 1228), **no** de
   `coeficientes_generador_medidos:`. Comando:
   `python3 -c "import yaml;print(list(yaml.safe_load(open('milpa/procedencia.yaml'))['coeficientes_generador_medidos']))"`
   → seis llaves, y `G5_familismo_apoyo` no está entre ellas
   (`G3_horizonte_temporal` sí). Un cargador que recorriera la sección
   perdería esa medición entera sin emitir un solo error. Es exactamente
   la clase de defecto que el esquema de §2 existe para volver visible —
   y la razón de que el censo se haga contra el árbol cargado
   (`yaml.safe_load`), no contra la lectura visual del archivo. Es
   **preexistente y ajeno a este acto**: la llave ya está así en la base
   (`git show origin/main:milpa/procedencia.yaml | sed -n '1228p;1244p'`
   → `propuesta_de_esquema:` / `  G5_familismo_apoyo:`). La medición en sí
   es de `ACTO MAESTRA32-E16`, 31/ago/2026, según el `fuente:` de la
   propia entrada; este acto no le atribuye la colocación, que no
   verificó. Y no lo corrige: `procedencia.yaml` no se toca en el diseño
   (mandato de `F-18`); queda declarado, con su fila propia en §3 y su
   `NC-0263`.

## 5 · Huecos abiertos para mesa (no se cierran aquí)

- ¿El esquema de §2 se escribe como campos reales en
  `milpa/procedencia.yaml` (edición del archivo, con su propio acto y
  revisión) o como una capa separada que lo referencia por nombre sin
  tocar el archivo sellado? Este diseño no decide dónde vive el esquema,
  solo qué campos exige.
- ¿`rotulo: ASOCIACION-MEDIDA·*` de `coeficientes_generador_sellados` se
  promueve tal cual a `identificacion: AUSENCIA_DECLARADA(...)`, o mesa
  quiere un vocabulario distinto para las dos clases (identificado /
  asociación) del que aquí se propone?
- `deuda_dispersion` (90 parámetros de dispersión, ADR-28.d) sigue
  bloqueando el censo completo de `params_base_de_perfil` línea por
  línea — mesa decide si ese acto se prioriza antes de que la
  calibración por celda intente tocar esa familia de parámetros.
- El crosswalk de ejes (`NC-0240`, objeto real de `F-17`) es prerrequisito
  del **marcador por segmento** (la pieza que viene después de esta
  calibración, según el propio sucesor de `NC-0239`), no de este diseño
  — pero mesa puede querer secuenciarlos antes de autorizar la corrida
  de caja.

## 6 · Contador

Cero mediciones nuevas del modelo. Tres correcciones al propio censo, todas
re-contadas contra el árbol cargado y no contra el borrador (`derivados`
8→9 ítems de lista; `coeficientes_generador_medidos` 6→5 entradas
`MEDIDO·β̂` más `G3_horizonte_temporal` en su fila; `G5_familismo_apoyo`
movida a fila propia con su defecto de colocación declarado): corrigen lo
que este documento dice de sí mismo, no un número del modelo. Ninguna
corrida, ningún `RESULT`, ninguna adopción, ningún cambio a
`milpa/src/theta.py` ni `milpa/src/motor.py`, ningún número nuevo en
`milpa/procedencia.yaml` (no se editó). Este documento es diseño puro:
un esquema y un censo de qué le falta a cada nombre para cumplirlo.
