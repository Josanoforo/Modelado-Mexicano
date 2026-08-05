# CORRIDA-IDG3 — ejecución de `ficha-id-g3-v1_0.md`

Encargo de mesa #20, 5/ago/2026, contra `origin/main = a7f807e` (PR #125). Ejecutado en worktree `~/mm-corrida-idg3`, rama `sesion/corrida-idg3`, Ubuntu (pc0), con `data/raw` enlazada al corpus compartido (`~/mm-corpus/raw`).

Este documento es la especificación de ejecución (commit 1). No re-escribe la ficha — dice cómo se ejecutó.

---

## §0 · Declaración ADR-46 (sesión limpia)

Sesión nueva, sin relación con `sesion/e-mxfls-g3-horizonte-ficha` (diseño, PR #117) ni con `sesion/s2-idg3-sello` (sello, PR #125) — ambas corridas en worktrees y conversaciones distintas, ya fusionadas antes de que esta sesión abriera nada.

**Declarado de más, no de menos (ADR-46(3)):** esta sesión tiene acceso a un sistema de memoria persistente entre conversaciones (fuera del concepto de "sesión" que ADR-46 mismo define, que asume una conversación aislada). Esa memoria contenía, antes de abrir la ficha: (a) la estructura general del proyecto (worktrees, ADR, disciplina forense); (b) un hallazgo puntual de la sesión E-MXFLS — que `CAL-G3` cita ponderador pero no estrato/UPM — que resultó ser exactamente lo que la ficha misma declara en su §0.2, sin margen adicional; (c) el estado de `conf.06` (tema no relacionado, confianza interpersonal vía ENCUCI). Ninguna de las tres contiene un resultado de Fase C de `CAL-G3` sobre la relación `G3→horizonte_temporal` más allá de lo que la propia ficha cita en su §0.1. Verificado explícitamente contra la lista de §0.1(A-G) de la ficha antes de escribir esta nota.

No se leyó `forense/hitoD-preregistro-v2_0.md`, `tests/calx_g3.py`, `tests/calg3_fasec.py` ni sus notas de salida — fuera del perímetro de este acto por instrucción explícita del encargo.

---

## §1 · Verificación de premisas

1. `git fetch` hecho; `origin/main` avanzó de `a7f807e` a `5ff97a5` durante la sesión (PR #124 conf.06/ADR-64, luego PR #128 P2/instrucciones v2.5) — no es PARO, se refrescó y se re-derivó contra el nuevo HEAD antes de escribir esta nota. Ninguno de los dos PR toca `milpa/procedencia.yaml` ni la ficha.
2. `forense/ficha-id-g3-v1_0.md` en `main`, 172 líneas, cabecera v1.0 — confirmado, leída completa.
3. `python3 tests/manifiesto.py --verifica --id <id>`, uno por id (19 invocaciones separadas, waves 2 y 3 completas — wave 1 no se usa en este diseño): 19 de 19 `COINCIDE`. `ennvih_mxfls_licencia` no tiene payload (nota de documentación, no hash aplicable) — no es AUSENTE ni discordante, es una categoría distinta.
4. `milpa/procedencia.yaml` no tenía entrada de `G3_horizonte_temporal` en `coeficientes_generador_medidos` antes de este acto — verificado por `grep`.
5. Censo de estimabilidad (`forense/censo-estimabilidad-coeficientes-v1_0.md`) confirma `G3·horizonte_temporal` como la única `RUTA-I` de los 15 coeficientes (§7 del censo: `RUTA-A=3 · RUTA-I=1 · RUTA-C=2 · SIN-RUTA=9`).

Ninguna premisa falló.

---

## §2 · Episodio de entorno (hallazgo de proceso, no anécdota)

Este acto abrió microdato por primera vez en la sesión. El entorno Ubuntu (pc0) asignado no tenía `pandas` ni `pyreadstat` instalados, ni `pip`/`ensurepip` disponibles para instalarlos, ni acceso root (`sudo` bloqueado por la bandera de contenedor `no new privileges`, no por contraseña). `apt-cache policy` confirmó que `python3-pandas` existe como paquete candidato en el repositorio estándar de Ubuntu — el bloqueo era de permiso, no de disponibilidad del paquete.

Se intentó, y se abandonó, un lector `.dta` artesanal en Python puro (sin dependencias) para rodear la ausencia de librería. Produjo cifras que coincidían con varias anclas ya publicadas (tabla `ah03h` de la ficha, media de `estrato`) — y esa coincidencia parcial es precisamente el riesgo: un desalineamiento de bytes que ajusta en algunas columnas puede seguir mal en otras sin ningún síntoma visible. El usuario, actuando como mesa, ordenó **PARAR** ese enfoque en firme —no como preferencia de estilo, sino citando el precedente `W1-P` (un campo que llegó como `"1.000000000000000"` y produjo `n_contact=0` en el primer parseo) como la clase de defecto que un ajuste-que-cuadra-parcialmente no detecta. El usuario instaló `python3-pandas` fuera de esta sesión (con su propio acceso root a la máquina); esta sesión verificó la instalación en el mismo intérprete (`/usr/bin/python3`, sin procesos `python` viejos vivos) antes de continuar, y descartó por completo el parser artesanal — no se cita, no se reutiliza, no se compara contra él en ningún punto de esta nota.

**Por qué es hallazgo y no anécdota:** la firma de entorno de tres partes que este mismo día introdujo `instrucciones-proyecto-v2_5.md` Bloque D-bis A.2 (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` + sonda de red + `ls data/raw/`) sigue sin cubrir "¿qué librerías están instaladas?". Un entorno con la firma completa correcta (Ubuntu, sin variable, red responde, corpus montado) puede aun así carecer de la herramienta para leer el corpus que tiene montado. Este acto no propone instrumentar esto (repetiría el costo que v2.3 ya advirtió) — lo deja registrado para que la próxima sesión que abra `.dta` no repita el intento artesanal desde cero.

---

## §3 · Compuerta ID-X — reproducción y recálculo con n reales

**Reproducción del pre-cálculo sellado.** `python3 tests/idx_g3.py` (sin modificar) reproduce exactamente `IC95%sup = 1.237` para el escenario B (única transición ejecutable, olas 2-3) — `COINCIDE` contra la cifra publicada en la ficha, Paso 2(8) fila `ID-X`. Margen original sobre el umbral de 1.25: **0.013**, bajo un solo escenario (la ficha declara que este cálculo no admite barrido de ICC, a diferencia de `CRH`/`CAL-G3`).

**Recálculo con los n reales**, una vez armada la muestra analítica (§4), usando la MISMA fórmula de `tests/idx_g3.py` (`se_log_rr`, importada sin modificar — no reimplementada) con `techo` y `N` derivados de la muestra real en vez de los conteos poblacionales completos que el pre-cálculo usó:

| especificación | n_util | Sí ola2 | Sí ola3 | techo | N=2×n_util | p | IC95%sup | ¿cruza <1.25? | margen |
|---|---|---|---|---|---|---|---|---|---|
| **Primaria (jefe)** | 762 | 167 | 175 | 342 | 1,524 | 22.44% | **1.483** | NO | −0.233 |
| Sensibilidad (algún miembro) | 1,562 | 318 | 302 | 620 | 3,124 | 19.85% | **1.372** | NO | −0.122 |

**Ninguna de las dos especificaciones alcanza el umbral.** El pre-cálculo (1.237) usó como "techo" la suma de los `Sí` marginales sobre las poblaciones completas de cada ola (2,253 sobre N=17,177) — una cota flojísima que no exige enlace de panel, aplicabilidad de TB33 ni ausencia de faltantes. La muestra real, una vez aplicados exactamente esos filtros, es dos órdenes de magnitud más chica (762, no ~8,588 persona-ola-slots que el pre-cálculo asumía implícitamente) — el mismo patrón, cualitativamente, que redujo el techo nominal de `CRH`/`CAL-G3` (1,457) a sus 7-14 hogares informativos reales.

**Veredicto de la compuerta: fila = `ID-X` para la especificación primaria** (la que decide, por regla de precedencia de la ficha) **y también para su sensibilidad** — no es un artefacto de una sola definición estrecha de exposición; ambas rutas de armar el "algún miembro" más generoso siguen sin alcanzar. Correr la relación exposición-desenlace sobre una compuerta que no alcanza produciría un veredicto que no significa lo que aparenta — el mismo defecto `D-09` que `ADR-47` cerró para `CAL-G3`. Este acto **reporta, no fuerza**: no se cruza `FORMAL_CONTRATO`/`INFORMAL` contra `ah03h` en ningún punto de esta sesión.

---

## §4 · Construcción de la muestra analítica — cascada completa

Fuente: `data/raw/ennvih/ehh05dta_all.zip` (ola 2) y `ehh09dta_all.zip` (ola 3), leídos con `pandas.read_stata` directamente desde el `.zip` (sin extraer a disco), `convert_categoricals=False`. Módulos abiertos, exactamente los que permite la ficha §(10): roster Libro C (`c_ls.dta`), TB Libro IIIA (`iiia_tb.dta`), AH sección `ii_ah` de Libro II (`ii_ah.dta`). No se abrió `CRH`, `SE` ni `CR` en ningún punto.

Cada pieza se validó contra documentación publicada o una cifra ya archivada en el repo con archivo:línea — nunca contra un cálculo propio anterior (instrucción explícita del usuario tras el episodio de §2):

- **Jefatura** (`ls05_1==1`, Libro C): cuenta exacta contra el manual de codificación — `ehh05cb_bc.pdf`: 8,334; `ehh09cb_bc.pdf`: 9,261 (categoría "1. Jefe del Hogar"/"01. Jefe del Hogar").
- **`ronda_origen`** (dígito 7 de `pid_link`, código de apertura de hogar A/B/C): documentado en `guia_de_usuario_ennvih-3.pdf`, pp. 40-41 ("El séptimo dígito indica en qué ronda se abrió ese hogar por primera vez... 'A'... 'B'... o 'C' en el caso de hogares nuevos abiertos en la tercera ronda"). Jefes de ola 3 con origen C = **192**, exacto contra la cita de la ficha (Nota 10(c): "192 jefes de ronda C de ola 3, no enlazables").
- **`tb33p_a/b/c/d`**: n exactos contra `ehh09cb_b3a.pdf` (cerca de línea 4285-4299): 2,582/658/1,470/2,687. Confirmado bateria de opción múltiple con co-ocurrencia REAL entre tipo de contrato e IMSS (1,524+366+188=2,078 casos con `a` o `b` Y `d` simultáneos, ola 3) — el confundidor mecánico que el Paso 1 de la ficha nombra está empíricamente presente, no es solo un riesgo teórico.
- **`ah03h`**: conteos Sí/No exactos contra la tabla de la ficha Paso 1 (1,117/7,015 ola2; 1,136/7,909 ola3), en última instancia de `ehh0{5,9}cb_b2.pdf`.
- **`estrato`**: N exacto (8,437/10,104) contra ficha §(7)/codebook; media 2.5127 (ola2, redondea a 2.51, coincide) y 2.5573 (ola3) contra "2.55" publicado en el codebook — diferencia de 0.007 explicada por truncamiento del codebook, no por error de lectura (N idéntico en ambos casos).

**Cascada** (especificación primaria, jefe):

| paso | n | pérdida | razón |
|---|---|---|---|
| Jefes ola 2 (`ls05_1==1`) | 8,334 | — | — |
| Jefes ola 3 (`ls05_1==1`) | 9,261 | — | — |
| ... menos ronda C (no enlazables) | 9,069 | −192 | primer registro en ola 3, sin dato de olas previas por construcción |
| Enlazados en AMBAS olas (`pid_link`, tras despojar el código de ronda de ola 3) | 6,818 | — | intersección de jefes-ola2 ∩ jefes-ola3-enlazable |
| Con `TB33` determinado (`a`/`b`/`c`, sin ambigüedad) en AMBAS olas | 771 | −6,047 | la mayoría de jefes no tiene un empleo con tipo-de-contrato determinado en alguna de las dos olas (jubilados, campesinos de su parcela, trabajador familiar sin retribución, o con `d`/`e`/`f`.../`i` marcado pero ninguno de `a`/`b`/`c` — ver nota abajo) |
| Con `ah03h` no faltante en AMBAS olas — **muestra analítica final** | **762** | −9 | faltante de item, marginal |

**Nota sobre el paso de mayor pérdida.** No toda esa caída es "sin trabajo": de los 8,334 jefes de ola 2, 1,479 no aparecen en el módulo TB en absoluto; 2,592 aparecen pero sin ninguna marca de `tb33p_*`; **2,147 aparecen CON alguna marca `tb33p_d..i` pero SIN ninguna de `a/b/c`** (verificado: `tb17`, "campesino de su parcela", no explica este subgrupo — sale `NaN` en el 100% de esos casos). Bajo la definición literal de la ficha (`FORMAL_CONTRATO = a∨b`, `INFORMAL = c`, nada más), estas 2,147 personas no caen en ninguna de las dos categorías — se excluyen del contraste principal por construcción de la propia ficha, no por una decisión de esta sesión. Se declara esto explícitamente porque agrupa dos poblaciones de exclusión distintas ("TB33 no aplicable en absoluto" vs. "TB33 aplicable pero la respuesta no cae en `a/b/c`") bajo un mismo paso de cascada, y mesa debe poder verlas por separado si audita esta cifra.

37 casos ambiguos (`a` Y `c` simultáneos, ola 2) y 12 (ola 3) — descartados de ambas especificaciones, no forzados a una categoría.

**Transición de exposición** (estructura del instrumento, NO cruzada con el desenlace — el gate ya decidió que no se cruza en este acto):

```
              exp_ola3=FORMAL   exp_ola3=INFORMAL
exp_ola2=FORMAL      528              48
exp_ola2=INFORMAL     77             109
```
(n=762, muestra analítica final)

---

## §5 · Ponderador, estrato y UPM

- **Ponderador**: `fac_2l` (Libro II, longitudinal, hogar, ola 2) como ancla de la especificación primaria — mismo criterio de precedencia que la ficha fija (§8, "ah03h sin ponderar Y con fac_2l ola 2"). Se reportaría también sin ponderar y con `fac_3al` (ola 3), como corroboración — ninguna decide la fila.
- **Estrato**: columna `estrato` de Libro C, confirmada presente y con valores plausibles (§4). Disponible para estratificar el error estándar.
- **UPM**: **no confirmado como nombre de columna** — reverificado independientemente en esta sesión contra las columnas completas de `c_ls.dta`, `c_portad.dta` y `c_rc.dta` de ola 3 (`folio`/`ls`/`ls00`/`ls01a-19e_1`/`panel`/`pid_link`/`edad`/`ent`/`estrato`/`id_loc`/`loc`/`mpio`/`reh`/`rel`/`rc01-02*` — ninguna se llama `upm` ni `conglomerado`), mismo hallazgo que la ficha ya declaraba. **Sustituto declarado**: de haberse ejecutado la estimación (no ocurrió — ver §3), cada hogar/persona habría entrado a `tests/svystat.py` (`prop_ultimate_cluster`) como su propio conglomerado singleton (upm=folio único), colapsando la fórmula de varianza de conglomerado último a una varianza estratificada (por `estrato`) sin ajuste por conglomeración de primera etapa — mismo límite declarado que `CAL-G3` (EE tipo HC1/sandwich, potencialmente anti-conservador si el efecto de diseño por UPM real es alto). No se finge una corrección que el instrumento no documenta.

---

## §6 · Especificación primaria y sensibilidad

**Primaria**: exposición = `FORMAL_CONTRATO` (`tb33p_a ∨ tb33p_b`) vs. `INFORMAL` (`tb33p_c`) del **jefe de hogar**, olas 2-3, ponderada con `fac_2l` (ancla) y sin ponderar. Decide la fila.

**Sensibilidad (única, pre-registrada)**: exposición = "algún miembro del hogar tiene `FORMAL_CONTRATO`" (dominante) vs. "algún miembro tiene `INFORMAL` y ninguno `FORMAL_CONTRATO`", agregada a nivel de hogar sobre el mismo módulo TB. Se reporta, no decide.

Ninguna sensibilidad reincorpora `tb33p_d` (IMSS) — reabrir ese canal reabriría exactamente el confundidor mecánico que el Paso 1 de la ficha excluyó por diseño.

---

## §7 · Significado de cada fila de la rejilla en esta ejecución concreta

- **`ID-A`** (RR≥1.5, IC95% excluye 1): no se alcanzó a evaluar — el gate para antes. De haberse alcanzado, por el confundidor (6.1) de la ficha, NO se habría leído como corroboración de `horizonte_temporal` (canal administrativo residual).
- **`ID-B`**: igual — no evaluado, mismo gate.
- **`ID-C`** (RR≤1, IC95%sup<1.25, submuestra con oferta verificada): es la fila que el gate mide directamente — y es la que NO se alcanza (§3). No se llegó siquiera a verificar el confundidor de oferta local (`eloc`), porque el gate cierra el acto antes.
- **`ID-D`** (inejecutable — panel no arma muestra, o confundidor de localidad sin descartar y mesa decide que no informa): **no es esta fila** — el panel SÍ arma una muestra analítica real y no trivial (762 primaria, 1,562 sensibilidad); el problema no es que no exista muestra, es que la muestra existente no tiene precisión suficiente para el umbral pre-registrado.
- **`ID-X`** (gate inalcanzable por construcción — chequeo previo): **es esta fila**, confirmada con n reales para ambas especificaciones (§3).
- **`ID-9b`** (nulo estricto con poder): no evaluado, mismo gate.
- **Fila `E`** (el falsador corrió limpio y no se satisfizo): no aplica aquí en su forma prospectiva original — esa fila describe el desenlace de CORRER el contraste y no encontrar señal con poder suficiente. Aquí el gate impide llegar siquiera a correr el contraste. La ficha misma anticipó esto como posible desenlace de esta ruta (§8: "es plausible... que el número real de hogares informativos quede de nuevo por debajo de lo necesario") — y ese desenlace, confirmado, es exactamente `ID-X`, no `E`: la diferencia es que `E` presupone que el contraste SÍ corrió y no refutó; `ID-X` es que el contraste NUNCA debió correr.

el primer resultado que produzca este procedimiento es el que se reporta.

---

## §8 · Resultados (commit 2 — no edita lo anterior)

**Fila propuesta: `ID-X`.** Confirmada para la especificación primaria (jefe, n_util=762, IC95%sup=1.483) y para su sensibilidad pre-registrada (algún miembro, n_util=1,562, IC95%sup=1.372) — ninguna de las dos alcanza el umbral `<1.25` de la ficha (§3, §6, §7 arriba). El gate se ejecutó y se detuvo el acto **antes** de cruzar `FORMAL_CONTRATO`/`INFORMAL` contra `ah03h` — no se calculó ningún RR, ninguna razón de riesgo, ningún IC95% sobre la relación exposición-desenlace. Lo único calculado sobre `ah03h` dentro de la muestra final son sus tasas marginales por ola (167/762 y 175/762), que son un hecho sobre el instrumento y la muestra, no sobre la relación bajo prueba — misma distinción que el Paso 0 de la ficha ya establece para sus propias cifras de estructura.

Script reproducible: `tests/idg3_corrida.py` (este commit). `python3 tests/idg3_corrida.py` reproduce íntegramente la cascada, ambos gates y el veredicto de arriba.

## §9 · Límites, declarados explícitamente

- **No se descartó el confundidor de oferta local** (`eloc`, ficha punto 6.2) — el gate cierra el acto antes de que ese paso fuera necesario. Queda sin verificar, no como omisión sino porque no había una relación que ese confundidor pudiera oscurecer.
- **No hay ancla externa publicada contra la cual validar un RR** de `FORMAL_CONTRATO`→`ah03h` específicamente (a diferencia de las anclas de estructura de §4, que sí existen) — no aplica de todas formas, porque no se calculó ningún RR. Se declara como límite general de esta ruta, no de esta corrida puntual.
- **UPM sigue sin confirmarse como columna** (§5) — reverificado, no resuelto; mismo límite que la ficha ya declaraba, ahora confirmado independientemente contra las tres tablas completas de Libro C de ola 3.
- **La atrición de 6,818 a 771/1,595 no se descompone completamente** entre "sin empleo actual" y "con empleo pero TB33 no cubre su situación contractual" más allá de lo declarado en §4 — se reportó la cifra agregada (2,147 casos en la categoría intermedia, ola 2) porque acotarla más finamente habría exigido abrir variables de TB fuera del perímetro de lectura de la ficha (§10) que no aportan a la decisión ya tomada por el gate.
- **El episodio de entorno (§2)** es un límite del acto, no del diseño: esta sesión no habría podido completar ni siquiera la construcción de la muestra sin la instalación de `pandas` fuera de esta sesión por el usuario.

## §10 · Lo que este acto NO hace

No modifica `ficha-id-g3-v1_0.md`. No sella ningún ADR. No toca `canon/`. No mueve el Hito D. No mueve el contador 0 de 15 (no se produjo ningún coeficiente, identificado o no — el gate paró el acto antes de estimar nada). No declara enlace ni forma funcional. No descarga nada de red (todo el corpus ya estaba en disco, verificado por hash antes de abrir). No abre tablas fuera de la restricción del Paso 10 de la ficha (`CRH`, `SE`, `CR` permanecen sin abrir). No adjudica su propia fila — la propone; mesa adjudica.
