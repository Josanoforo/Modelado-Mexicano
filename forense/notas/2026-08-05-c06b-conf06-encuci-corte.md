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
