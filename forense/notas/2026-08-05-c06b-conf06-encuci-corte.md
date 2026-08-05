# ACTO C-06b — `conf.06` contra ENCUCI: prueba de corte ≥8/10 vs. ≥6/10

*5 de agosto de 2026. Contadores movidos: 0 — este acto no mide una
condicional del motor ni mueve el contador de Hito D (`8 de 14`, sin
cambio). Audita, contra microdato real, una cifra que circula por todo el
corpus (`conf.06`, seis cifras localizadas por C-06a, ninguna adjudicada
todavía).*

---

## 0 · Verificación de premisas antes de obedecer (Bloque D)

- **Repo.** Clon existente en `/home/pc0/Modelado-Mexicano` (no se clonó
  uno nuevo). Ese clon base estaba parado en rama ajena
  (`sesion/cal-conf-faseb-pos4-envipe-paso1`, `git log -1` = `302ac5a`) —
  no se trabajó ahí. Worktree propio creado en este acto:
  `git worktree add ~/mm-c06b-conf06-encuci -b sesion/c06b-conf06-encuci
  origin/main`. `git worktree add` emitió dos veces `error: could not
  write config file .git/config: Device or resource busy` (misma clase
  `I-11` ya registrada — escritura concurrente de otra sesión sobre el
  `.git` compartido; el worktree quedó consistente pese al error,
  verificado con `git status`/`git log -1` después). No PARO.
- **SHA.** `git fetch --all --prune` antes de comparar. `origin/main` =
  `06d04be` — **coincide exacto** con el SHA que el encargo declara
  (`git merge-base --is-ancestor 06d04be origin/main` → sí, y
  `git rev-list --count 06d04be..origin/main` → `0`). Main no se movió;
  no hace falta re-derivar nada.
- **data/raw.** No existía en el worktree nuevo (gitignorada, raíz
  integrada). Se enlazó a mano: `data/raw -> /home/pc0/mm-corpus/raw`
  (misma raíz compartida que usa el resto de worktrees vivos). Este acto
  **no descarga** nada nuevo — `BD_ENCUCI2020_dbf.zip` y
  `FD_ENCUCI2020.pdf` ya estaban en el corpus compartido antes de abrir
  esta sesión — así que no aplica la verificación de "payload quedó en el
  corpus y no solo en el worktree" (nada se agrega al corpus en este
  acto).
- **Entorno.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` → valor crudo:
  cadena vacía (variable sin definir) → firma Ubuntu-con-red, coincide con
  lo que el encargo declara (`Entorno: Ubuntu · NO en la nube`). Sonda de
  red **no aplicable y saltada, declarado**: el encargo fija
  "Red: solo git" para este acto — no se abre ninguna URL externa, solo
  `git fetch`/`push` y lectura de microdato ya presente en disco. No se
  corrió `curl` porque no hay a qué apuntarlo.
- **Espejo.** No se usó ningún espejo del proyecto. Toda cifra de esta
  nota sale del clon de este worktree, con el comando a la vista en cada
  sección.
- **Entorno asignado.** Ubuntu, no nube — este acto no se lanza en un
  entorno cloud.
- **Perímetro.** Toca: este archivo, `tests/c06b_conf06_encuci.py`
  (nuevo), `forense/hallazgos.md` (una línea, apéndice). No toca
  `canon/glosario-v5_6.md`, `forense/hitoD-preregistro-v2_0.md`,
  `forense/cruce-catalogo-fichas-v2_0.md`, ni `milpa/procedencia.yaml`.
  Si esta sesión se encuentra escribiendo fuera de esa lista, PARA.
  **Concurrencia verificada:** `gh pr list --state open` → vacío (sin PRs
  abiertos al momento de arrancar); no existía rama ni worktree `c06b*`
  antes de crear el propio en este acto (`git branch -r | grep -i c06b` →
  vacío antes de este acto).
- **Premisa "`conf.06` sigue abierto y sin ADR"** — re-verificada fresca
  contra el árbol de este worktree, no heredada de la cita de C-06a:
  `canon/glosario-v5_6.md:320` (tabla §11) sigue marcando `conf.06` como
  **"⚠️ Abierto"**, y `:398` (§15) lo sigue listando entre las entradas
  "sin ADR". Se sostiene.
- **Premisa "la marca C3 de `radio_confianza` sigue vigente"** —
  re-verificada: `milpa/procedencia.yaml:226-228` sigue marcando que
  `radio_confianza` (mismo dato, `AP5_1_1/2/3`) **NO identifica**
  `cooperacion.confianza.puente_personal` (circular — el desenlace
  observado de esa regla en Tabla B es `AP5_1_2`, el propio reactivo). Se
  sostiene, y viaja con cualquier cifra que produzca este acto (§1.11).
- **Leído completo antes de escribir esta especificación:**
  `forense/notas/2026-08-04-c06a-cinco-cifras-conf06-localizadas.md`
  (las cinco/seis cifras, el mapa de compatibilidad §4, la especificación
  §5 que este acto ejecuta) y
  `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md`
  (la medición ≥6/10 ya hecha — instrumento, join, ponderador, universo,
  que este acto reutiliza donde aplica y declara donde se aparta, §1.2
  abajo). Grep dirigido, no completo:
  `instrucciones-proyecto-v2_4.md` (Bloque A-bis, Bloque D, patrón de dos
  commits — confirmado el texto exacto del sello) ·
  `milpa/procedencia.yaml:230-250` (entrada `radio_confianza`) ·
  `canon/glosario-v5_6.md:84,320,398` (entrada `conf.06`) ·
  `tests/svystat.py` completo (34 líneas de cuerpo, no modificado) ·
  `tests/test_svystat.py` completo · `tests/cal_conf_faseb_pos5_6.py`
  completo (la lógica de extracción/recodificación que este acto adapta).
  **Verificado directamente contra la fuente primaria, no heredado de la
  cita de la nota previa:** `FD_ENCUCI2020.pdf` páginas 24-25 (cons.
  68-70, pregunta 5.1 completa, los tres reactivos con su rango de código
  00-10+99) y página 32 (cons. 160-164, "Campos empleados para el diseño
  muestral": `FAC_SEL`, `DOMINIO`, `ESTRATO`, `UPM_DIS`, `EST_DIS` — los
  cinco viven en la tabla `ENCUCI_2020_SEC_4_5`, la misma que los
  reactivos, confirmado por lectura directa de las páginas, no por cita
  de la nota previa).

---

## 1 · Especificación — congelada antes de abrir el `.dbf`

### 1.1 Reactivos

`AP5_1_1` (*"la mayoría de las personas"*) · `AP5_1_2` (*"la mayoría de
las personas que conoce personalmente"*) · `AP5_1_3` (*"la mayoría de las
personas que viven en su colonia y localidad"*) — pregunta 5.1,
`ENCUCI_2020_SEC_4_5`, verificada en este acto contra `FD_ENCUCI2020.pdf`
p.24-25 (no solo heredada): *"En una escala de cero a diez, como en la
escuela, donde cero es nada y diez es completamente, en general ¿cuánto
confía en…"*. Tipo Carácter, códigos `00`-`10` + `99` (No sabe/no
responde); no existe código de blanco para estos tres ítems (a diferencia
de otros bloques de la Sección IV que sí lo traen) — confirmado en el PDF,
no supuesto. Se miden **por separado, no como índice** — mismo criterio
que toda medición previa de Fase B (tres referentes sociales distintos, no
repeticiones del mismo escenario).

`AP5_1_4` (servidores públicos) existe en el mismo bloque y no se mide —
no lo pide ninguna de las tres cifras de `conf.06` bajo prueba (§7 de
C-06a, tabla de §5).

### 1.2 Universo — completo, sin condicionar, y por qué se aparta de la forma (no del fondo) de la medición previa

**Completo: todo entrevistado, sin filtro de identificación previo** —
mismo universo que ya verificó
`2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §1.1 (21 519 filas
de `SEC_4_5`, cero blancos en los tres campos). Eso es lo que la
especificación de C-06a (§5, columna "Universo") marca como **"Idéntico"**
y este acto lo reutiliza sin cambio en su definición.

**Lo que sí cambia, declarado antes de calcular, no descubierto después:**
la medición de Fase B condicionaba por formalidad×edad, lo que exige
cruzar `SEC_4_5` contra `ENCUCI_2020_SD` por
`UPM+VIV_SEL+R_SEL=N_REN` — y ese cruce pierde 1 265-1 314 filas por
ítem ("sin cruce") que no tienen formalidad/edad identificable. Las tres
cifras de `conf.06` (21.8%, 32.1%, 62.1%) se citan en el corpus como
**puntos nacionales sin condicionar** ("el 21.8% de los mexicanos...",
"62.1% confía..."), no como celdas de una tabla condicionada. Pedirle al
dato un cruce que el propio estimando que se intenta reproducir no pide
sería exactamente el error que la Regla 4 de Bloque A-bis prohíbe ("un
estimando restringido a una subpoblación no se compara contra uno
poblacional"): el universo correcto para un agregado nacional es la
población completa con respuesta válida al ítem, **no** la subpoblación
que además tiene formalidad/edad identificables. Por eso este acto **no
hace join a `ENCUCI_2020_SD`** — `FAC_SEL`, `EST_DIS`, `UPM_DIS` viven en
`SEC_4_5` (verificado en este acto contra el FD, §0), así que ponderador y
diseño no requieren el cruce. Esto no es una desviación de "Idéntico": es
la misma definición de universo aplicada sin una restricción que el
propio estimando nacional no necesita.

**Exclusión:** código `99` (No sabe/no responde) por ítem — no imputado,
excluido. Blanco no se observa (§1.1).

### 1.3 Ponderador

`FAC_SEL` — mismo campo y mismo valor de verificación ya hecho por Fase B
(suma sobre las 21 519 filas de `SEC_4_5` = 96 427 583 ≈ Censo 2020,
población 15+). No se recalcula desde cero la suma total en este acto
(ya verificada dos veces por sesiones anteriores); si el guardia de
pipeline de §1.10 pasa, la extracción de `FAC_SEL` es la misma.

### 1.4 Diseño / dispersión

Conglomerado último — `EST_DIS` (Estrato de Diseño, `001`-`999`, cons.
164 del FD) + `UPM_DIS` (`0000001`-`9999999`, cons. 163) — **no** el campo
`ESTRATO` simple (cons. 162, `1`-`4`), que no es el que usa la medición ya
validada de Fase B. Ambos campos, verificado en este acto contra el FD
(§0), viven en `SEC_4_5`, mismo registro que el reactivo — no requieren
join.

### 1.5 Estimador

`tests/svystat.py::prop_ultimate_cluster` — **no se modifica**. Respaldo:
tres casos de referencia archivados
(`forense/notas/2026-08-04-svystat-casos-referencia.md`: caso sintético
de 2 estratos derivado a mano, reproducción de Hito D R7.2 ocho olas,
reproducción de CAL-CONF Fase B ola 2 — los tres coinciden contra cifra
archivada) más el autochequeo del propio módulo. Revalidado en este
entorno, no heredado por cita: `python3 tests/test_svystat.py` corrido en
este acto antes de escribir esta especificación —

```
TEST 1 -- coincide con la derivacion a mano dentro de tolerancia 1e-9.
TEST 2 -- el estrato singleton queda marcado, no escondido en un cero falso.
TEST 3 -- resultado sobre generador identico al de la lista.
TEST 4 (autochequeo _caso_conocido) -- Coincide a 9 decimales. Validado.
```

Los cuatro casos coinciden en este entorno. No hay PARO de instrumento.

### 1.6 Cortes a probar — exactamente dos, fijados aquí, ninguno más

- **≥6/10** ("aprobatorio"): el corte que ya usa la medición existente de
  Fase B, ancla declarada en el propio enunciado de la pregunta ("como en
  la escuela"). Entra a este acto como **punto de control/comparación**,
  no como hipótesis nueva — si ninguna de las tres cifras del corpus
  reproduce a ≥6/10 (ya se sabe que las celdas condicionadas no
  reproducen, C-06a §5; aquí se prueba el agregado nacional, nunca antes
  calculado a este corte).
- **≥8/10**: la hipótesis bajo prueba. Ancla textual, no inventada aquí:
  `Non-Family_Social_Capital_in_Mexico...md:12` cita **62.1%** con la
  frase literal *"confía (grado 8-10)"* — corte explícito en la fuente
  primaria del corpus, localizado por C-06a §5.

**No se prueba un tercer corte.** Ninguna cita del corpus ancla un corte
distinto de estos dos (ni ≥7, ni ≥9, ni el punto exacto `=10`) para
ninguna de las tres cifras de `conf.06`. Probar uno más sin una cita que
lo motive sería ajustar la búsqueda al resultado — exactamente lo que el
encargo prohíbe explícitamente (§11: *"Prohibido buscar el corte que
reproduzca la cifra y declararlo hallazgo"*). Si ninguno de los dos cortes
declarados reproduce una cifra, eso es el resultado, y es informativo tal
cual — no dispara una búsqueda de un tercer corte dentro de este acto.

### 1.7 Recodificación

`y = 1` si `código ∈ [corte, 10]`; `y = 0` si `código ∈ [0, corte)`;
excluido si `código == 99` o vacío. Misma lógica exacta que
`cal_conf_faseb_pos5_6.py` (`y = 1 if code >= 6 else 0`), generalizada al
parámetro `corte` y sin el condicionamiento formalidad×edad (§1.2).

### 1.8 Qué cuenta como "cifra reproducida" — criterio fijado antes de calcular, con tolerancia declarada

**Una cifra del corpus (21.8%, 32.1% o 62.1%) se declara reproducida en
una celda ítem×corte si y solo si el valor cae dentro del IC95% calculado
para esa celda.** Cercanía del punto estimado sin que el IC95% contenga
la cifra **no** cuenta como reproducida — aplicación literal de la
contraparte que `instrucciones-proyecto-v2_4.md` (Bloque A-bis) ya deja
escrita: *"Un punto estimado que satisface un umbral con un intervalo de
confianza que no lo despeja no adjudica. Se reporta como propuesta con la
reserva escrita."* No se usa un margen de tolerancia en puntos
porcentuales inventado aparte — el IC95% ya es la tolerancia declarada, y
usar dos criterios (uno de cercanía y uno estadístico) sería exactamente
la clase de "se parece" que el encargo prohíbe.

**Las tres cifras se comparan contra las seis celdas completas de la
matriz (3 ítems × 2 cortes), no solo contra la celda que C-06a §5 marcó
como candidata principal** (21.8%→`AP5_1_1`; 32.1%→`AP5_1_1` **o**
`AP5_1_3`, a decidir por el resultado; 62.1%→`AP5_1_2`) — comparar contra
las seis evita sesgar la búsqueda hacia la celda esperada; si una cifra
reproduce en una celda que C-06a no anticipó, se declara igual, sin
descartarla. Se marca en el reporte cuál celda era la candidata declarada
de antemano y cuáles son control adicional.

**No se compara ninguna cifra contra 12%/18%/22%** — no son ENCUCI
(WVS/Pew/Latinobarómetro, C-06a §5-§6), fuera de lo que este microdato
puede reproducir.

### 1.9 n mínimo

30 sin ponderar por celda, igual que toda medición previa del programa.
Por debajo: SIN SOPORTE. No se espera que aplique — universo nacional sin
condicionar, n en el orden de 10⁴ por celda — se declara por
consistencia con la convención, no porque se anticipe un problema.

### 1.10 Guardia de pipeline — assert duro antes de calcular algo nuevo

Antes de calcular ninguna celda a ≥6/10 o ≥8/10, el script reproduce
`n_filas=21519` (total de `SEC_4_5`) y `no_respuesta(99)` por ítem = **110
(`AP5_1_1`) · 74 (`AP5_1_2`) · 116 (`AP5_1_3`)** — cifras ya publicadas en
`2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` §3.1, e
independientes del join a `SD` (el conteo de `99` se hace sobre el código
del propio ítem, antes de cualquier cruce, verificado leyendo
`cal_conf_faseb_pos5_6.py:188-192`). Si no coincide exacto, el script se
detiene antes de tocar el corte ≥8/10 — mismo patrón de guardia que usa
todo el programa desde Fase B ola 2.

### 1.11 Lo que este acto no hace

- No edita `canon/glosario-v5_6.md` — resolver `conf.06` exige ADR y es
  acto de mesa.
- No adjudica `R8.3`.
- No sella ningún ADR de gobernanza (declara ADR-46 de procedencia de
  lectura al cierre, §5 de la nota de resultados — no es lo mismo).
- No toca `milpa/procedencia.yaml` — es de `E-ENCIG`.
- **Cualquier cifra que produzca este acto sigue marcada C3**: no
  identifica `cooperacion.confianza.puente_personal` (el desenlace
  observado de esa regla en Tabla B es `AP5_1_2`, el propio reactivo —
  circular, `milpa/procedencia.yaml:226-228`). Un nuevo corte sobre el
  mismo reactivo no cambia esa circularidad — compra, cuando mucho, la
  condicional de `G1`, nunca el coeficiente de esa regla específica.
- No construye índice de `radio_confianza` — los tres ítems se miden por
  separado (§1.1).
- No condiciona por formalidad×edad ni dominio en este acto — eso ya
  existe, a ≥6/10, en la nota de Fase B (§3.1 de esa nota). Este acto
  agrega el **punto agregado nacional sin condicionar** que esa nota
  nunca calculó (declarado explícitamente en su Auditoría §4.1,
  Propiedad 1: *"nunca un punto nacional único"*), a los dos cortes de
  §1.6 — es un estimando distinto, no una repetición ni una corrección
  de lo ya publicado.
- No cierra `conf.06` — reproducir o no reproducir una cifra a ≥8/10 dice
  qué corte usó (probablemente) el report que la cita; no resuelve por sí
  solo el conflicto de atribución de C-06a §4.2 (a qué reactivo
  corresponde 32.1%) salvo que el propio resultado numérico lo decida
  (§1.8), ni cierra la condición A de `R8.3` (C-06a §7).

---

el primer resultado que produzca este procedimiento es el que se reporta.

---

## 2 · Corrida

Comando exacto: `python3 tests/c06b_conf06_encuci.py` (nuevo,
`tests/c06b_conf06_encuci.py`, no modifica `svystat.py`/`dbfmini.py`).
Salida cruda completa abajo, sin editar.

```
======================================================================
§0 -- validacion del estimador (caso conocido, re-corrida en este entorno)
======================================================================
OK -- caso conocido (SRS, n=200, k=80, PSU=persona):
  p_hat calculado = 0.400000 (esperado 0.400000)
  se calculado    = 0.034728 (formula SRS p(1-p)/(n-1) = 0.034728)
Coincide a 9 decimales. Validado.

======================================================================
Guardia de pipeline -- reproduce no_respuesta(99) ya publicado antes de calcular algo nuevo
======================================================================
n_filas=21519 (esperado 21519)
  no_respuesta(99) AP5_1_1 = 110 (esperado 110)
  no_respuesta(99) AP5_1_2 = 74 (esperado 74)
  no_respuesta(99) AP5_1_3 = 116 (esperado 116)
Guardia de pipeline verificada -- coincide exacto con lo publicado. Procede con la matriz item x corte.
```

Guardia pasada — la extracción de `SEC_4_5` en este acto (sin join a
`SD`) coincide dígito por dígito con la ya validada por Fase B en lo que
ambas comparten (total de filas, conteo de `99` por ítem). El script no
llegó a calcular ningún corte nuevo hasta que este `assert` pasó.

## 3 · Resultados — matriz completa ítem × corte (agregado nacional, sin condicionar)

| Ítem | Corte | n útil | p̂ | SE | IC95% | n_estratos (singleton) |
|---|---|---|---|---|---|---|
| `AP5_1_1` (mayoría de las personas) | ≥6/10 | 21 409 | 46.0% | 0.54pp | [45.0%, 47.1%] | 281 (0) |
| `AP5_1_1` (mayoría de las personas) | ≥8/10 | 21 409 | 21.9% | 0.42pp | [21.1%, 22.7%] | 281 (0) |
| `AP5_1_2` (personas que conoce) | ≥6/10 | 21 445 | 77.9% | 0.44pp | [77.0%, 78.7%] | 281 (0) |
| `AP5_1_2` (personas que conoce) | ≥8/10 | 21 445 | 62.2% | 0.53pp | [61.2%, 63.3%] | 281 (0) |
| `AP5_1_3` (vecinos) | ≥6/10 | 21 403 | 55.4% | 0.53pp | [54.4%, 56.5%] | 281 (0) |
| `AP5_1_3` (vecinos) | ≥8/10 | 21 403 | 32.3% | 0.50pp | [31.3%, 33.3%] | 281 (0) |

`n útil` = 21 519 − no_respuesta(99) del ítem (§1.10) — no se resta
ninguna pérdida de cruce, porque este acto no cruza contra `SD` (§1.2).
Ninguna celda cae bajo el mínimo de 30 (§1.9); la más chica tiene
n=21 403. Ningún estrato queda singleton (0 en las seis celdas) — la
varianza de las seis celdas es estimable en su totalidad, sin
advertencia de grados de libertad insuficientes.

**Patrón, descrito sin comparar entre ítems distintos de escala (mismo
límite de Bloque A-bis regla 3 — misma escala, sí es comparable dentro de
`radio_confianza`):** monotonía esperada en los tres ítems (≥8/10 da
siempre un p̂ menor que ≥6/10, por construcción — es un subconjunto del
mismo evento). La caída de ≥6 a ≥8 no es uniforme entre ítems: `AP5_1_1`
cae 24.1pp, `AP5_1_2` cae 15.7pp, `AP5_1_3` cae 23.1pp — el ítem de
"conocidos" tiene más masa concentrada por encima de 8 que los otros dos.

## 4 · Comparación contra las tres cifras de `conf.06` — y lo que decide

**Criterio aplicado, fijado en §1.8 antes de calcular: cae dentro del
IC95%, no cercanía puntual.** Las tres cifras se compararon contra las
seis celdas completas, no solo contra la celda candidata de C-06a §5.

| Cifra del corpus | Candidata C-06a §5 | Resultado contra las 6 celdas |
|---|---|---|
| **21.8%** | `AP5_1_1` | **Reproduce solo en `AP5_1_1` ≥8/10** (21.9%, IC95%=[21.1%,22.7%] — contiene 21.8%, interior, no al borde). Ninguna otra de las 6 celdas la contiene. |
| **32.1%** | `AP5_1_1` **o** `AP5_1_3` (ambiguo, a decidir por el resultado) | **Reproduce solo en `AP5_1_3` ≥8/10** (32.3%, IC95%=[31.3%,33.3%] — contiene 32.1%, interior). **No** reproduce en `AP5_1_1` ≥8/10 (21.9%, no contiene 32.1%). Ninguna otra celda la contiene. |
| **62.1%** | `AP5_1_2` | **Reproduce solo en `AP5_1_2` ≥8/10** (62.2%, IC95%=[61.2%,63.3%] — contiene 62.1%, interior). Ninguna otra celda la contiene. |

**Las tres cifras reproducen, cada una en exactamente una celda, las tres
al corte ≥8/10, cada una en un ítem distinto sin superposición. Ninguna
de las tres cifras cae en ninguna de las tres celdas a ≥6/10.** No es un
resultado ambiguo ni parcial: de 18 comparaciones (3 cifras × 6 celdas),
exactamente 3 dan "SI — REPRODUCE", las tres al mismo corte, cada una con
su propio ítem, sin ninguna coincidencia cruzada ni ningún caso límite
(las tres caen claramente al interior de su intervalo, no pegadas al
borde).

**Resuelve, como subproducto verificado y no buscado, el conflicto de
atribución de C-06a §4.2.** La especificación (§1.6, §1.8) fijó de
antemano que 32.1% se probaría contra ambos ítems candidatos y que
decidiría el propio resultado — no se buscó el ítem que la reprodujera
después de verla. El resultado es unívoco: **32.1% es `AP5_1_3`
("vecinos de su colonia/localidad"), no `AP5_1_1` ("la mayoría de las
personas")**. De las dos citas mutuamente excluyentes que C-06a localizó
(`Psicología__Conducta_y_Sociedad...md:71`: 32.1%=vecinos;
`Non-Family_Social_Capital...md:12`: 32.1%="la mayoría"), la primera
tenía el reactivo correcto. La segunda —que es también la fuente de la
cita literal "grado 8-10" que motivó la hipótesis de corte de este
acto— tenía el corte correcto pero el reactivo equivocado para ese
número específico (aunque sí correcto para 62.1%, que cita en la misma
oración).

**Consecuencia declarada — no adjudicada, tal como pide §10 del
encargo.** Si el corte que usan los reports que citan estas tres cifras
es en efecto ≥8/10 (lo que este resultado hace plausible para las tres,
no solo para 62.1%), entonces:

- `conf.06` deja de ser, en su forma actual, un conflicto de **magnitud
  entre fuentes** ("¿21.8% o 32.1%, cuál es la correcta?") para ser un
  **desajuste de umbral de dicotomización**: las tres cifras podrían ser
  correctas a la vez, cada una midiendo un reactivo distinto de la misma
  encuesta al mismo corte, no dos cifras compitiendo por el mismo
  reactivo. El "conflicto directo" que C-06a §4.1 nombraba (21.8% vs.
  32.1%-si-es-`AP5_1_1`) se disuelve porque la premisa que lo sostenía
  —que ambas compiten por el mismo reactivo— no se sostiene: son
  reactivos distintos (`AP5_1_1` y `AP5_1_3`).
- **Las tres cifras del corpus no son comparables contra ninguna
  celda de `2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md`** (todas
  a ≥6/10) — comparar una cifra a ≥8/10 contra una celda a ≥6/10 sería el
  error de escala que Bloque A-bis regla 3 prohíbe si se tratara como
  discrepancia. La medición condicionada por formalidad×edad de Fase B
  sigue vigente y sigue siendo la única fuente de las celdas
  condicionadas — este acto no la reemplaza, mide un estimando distinto
  (agregado nacional, corte distinto).
- Esto **no** resuelve por sí solo si ≥8/10 es "el corte correcto" en
  algún sentido normativo — solo que es el corte que, aplicado al
  microdato real, reproduce las tres cifras que el corpus ya cita. Qué
  corte debería usar el programa hacia adelante para `radio_confianza`
  es una decisión de mesa (edita `milpa/procedencia.yaml`, fuera de este
  acto).

## 5 · Qué decide esto y qué NO decide — límites explícitos

- **No cierra `conf.06`.** Reproducir las tres cifras a un corte da
  evidencia fuerte a favor de la hipótesis de C-06a §5, no un cierre —
  cerrarlo exige ADR y es acto de mesa: este acto no edita
  `canon/glosario-v5_6.md`, no edita `forense/hitoD-preregistro-v2_0.md`,
  no edita `forense/cruce-catalogo-fichas-v2_0.md`, no sella ningún ADR
  de gobernanza.
- **No toca `milpa/procedencia.yaml`** — es de `E-ENCIG`, fuera de este
  perímetro.
- **No adjudica `R8.3`.** La condición C de su ficha (`hitoD-preregistro-
  v2_0.md:236-246`, "exigiría reconciliar `conf.06` primero") avanza con
  este resultado, pero la condición A (falsador de "disposición a
  transar con desconocidos") sigue sin existir en el corpus — este acto
  no la crea, no la busca, no la toca.
- **La marca C3 sigue vigente sobre cualquier cifra de este acto**,
  igual que sobre la de Fase B: `radio_confianza` (mismo dato,
  `AP5_1_1/2/3`, cualquier corte) **no identifica**
  `cooperacion.confianza.puente_personal` — su desenlace observado en
  Tabla B es `AP5_1_2`, el propio reactivo (`milpa/procedencia.yaml:
  226-228`, circular). Este acto, si algo, compra la condicional de
  `G1` con más precisión de umbral — nunca el coeficiente de esa regla
  específica.
- **No construye índice** — los tres ítems se reportan y comparan por
  separado (§1.1, §3).

## 6 · ADR-46 — procedencia de lectura

Esta sesión abrió microdato de ENCUCI 2020 (`ENCUCI_2020_SEC_4_5.dbf`,
campos `AP5_1_1/2/3`, `FAC_SEL`, `EST_DIS`, `UPM_DIS`) y su diccionario de
datos completo en las páginas citadas (`FD_ENCUCI2020.pdf` p.15-32) —
**inhabilitada para pre-registrar hipótesis nuevas contra ENCUCI** en lo
que resta de esta sesión (ADR-46). No aplica: esta sesión no pre-registra
nada — mide contra una especificación ya congelada en el commit 1.

## 7 · El contador

**Contadores movidos: 0.** Declarado en el encabezado y sostenido aquí:
este acto no mide una condicional nueva del motor ni mueve el contador
de Hito D (`13 de 27` tras `ADR-63`, sin cambio) — audita, con microdato
real, la atribución de tres cifras que ya circulaban en el corpus antes
de este acto. El hallazgo de §4 es sustantivo (resuelve una atribución
que C-06a había dejado abierta) sin mover ningún contador — exactamente
la clase de artefacto que v2.3 permite declarar en una línea sin
justificarlo más.

## 8 · Suite y verificación de payload

**Payload — no se descargó nada nuevo.** `BD_ENCUCI2020_dbf.zip` y
`FD_ENCUCI2020.pdf` ya estaban en el corpus compartido
(`/home/pc0/mm-corpus/raw`) antes de abrir esta sesión. Verificado contra
el manifiesto de todos modos, por la disciplina de Bloque D (el defecto
de `PR #77`) — no por sospecha concreta de que faltara algo:

```
$ python3 tests/manifiesto.py --verifica | grep -i encuci
encuci2020_bd_dbf [data_raw]: COINCIDE -- sha256 y tamaño (6913684 bytes) verificados contra data/manifiesto.yaml
encuci2020_fd_pdf [data_raw]: COINCIDE -- sha256 y tamaño (1758249 bytes) verificados contra data/manifiesto.yaml
```

`python3 tests/check.py --baseline`, corrido antes y después de escribir
este acto:

```
18 FAIL · 95 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe56d523615259efb77c17c84fee86ac684)
```

Idéntico antes y después — este acto no introduce ningún FAIL ni WARN
nuevo. `git status --short` tras escribir todo el acto muestra únicamente
`data/raw` (symlink recreado, gitignorado) como no rastreado además de
los archivos de este mismo acto — no se tocó `canon/`, `milpa/`, ni
ningún archivo fuera del perímetro declarado en §0.

**Límite de lectura declarado (ADR-46, detalle):** leído completo en esta
sesión: `forense/notas/2026-08-04-c06a-cinco-cifras-conf06-localizadas.md`
· `forense/notas/2026-08-03-cal-conf-faseb-pos5-6-radio-familismo.md` ·
`forense/notas/2026-08-04-svystat-casos-referencia.md` ·
`tests/svystat.py` · `tests/test_svystat.py` ·
`tests/cal_conf_faseb_pos5_6.py`. Grep dirigido:
`instrucciones-proyecto-v2_4.md` (Bloque A-bis, Bloque D) ·
`milpa/procedencia.yaml:218-262` · `canon/glosario-v5_6.md:84,320,398`.
Microdato abierto y leído: `FD_ENCUCI2020.pdf` p.15-32 (páginas
completas) · `ENCUCI_2020_SEC_4_5.dbf` (campos `AP5_1_1/2/3`, `FAC_SEL`,
`EST_DIS`, `UPM_DIS`, vía `tests/c06b_conf06_encuci.py`). No se abrió
`ENCUCI_2020_SD.dbf` en este acto (§1.2 — no hace falta para un agregado
nacional sin condicionar). No se tocó `canon/`, `milpa/`, ni ningún
archivo de `corpus/` en este acto.
