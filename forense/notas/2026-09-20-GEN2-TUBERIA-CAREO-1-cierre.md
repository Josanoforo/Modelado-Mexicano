# GEN2-TUBERIA-CAREO-1 · careo de dos diseños de id no colisionante para NC/FP

**Acto:** GEN2-TUBERIA-CAREO-1 · **Entorno:** NUBE (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`)
**SHA de ejecución:** `b8438d76` (= SHA que declara el encargo; `origin/main` al abrir, 0 commits de diferencia)
**Encargo:** `forense/encargos/2026-09-20-GEN2-TUBERIA-CAREO-1.md` (archivado verbatim, 0-bis A.3)
**Desvío de ruta declarado (D-19, obstáculo reversible y barato).** El encargo §8 asigna a la nota la ruta `forense/notas/2026-09-20-GEN2-TUBERIA-CAREO-1.md`, idéntica en basename al encargo archivado. T02 la rechaza por colisión de nombre normalizado (`fail("T02", "nombre normalizado colisiona")`, `tests/check.py:224`). Se resuelve con el sufijo que el repo ya usa para notas de cierre: **`…-GEN2-TUBERIA-CAREO-1-cierre.md`**. Es logística, no procedimiento: no se para (§2 v2.15).

**Rótulos desacuñados (T25).** Los escenarios de P1 se numeraron primero `E1..E5`; T25 los marcó como rótulo pelado nuevo sin prefijo de espacio. Se renombraron a «Escenario 1..5», que no acuña rótulo alguno.

**Ramas vivas al abrir** (`git ls-remote --heads origin`, conteo 3): `main` · `acto/gen2-din-credito-comparabilidad-texto-1` · `claude/gracious-faraday-wf9b8j`. Ramas de acto vivas: **1**. La ventana de disparador de estado que mesa firmó (cero ramas de acto vivas) **no está abierta hoy**.

**Este acto no mide una celda: no mueve `cuenta_gen2`.** Produce un veredicto de diseño para firma de mesa (§5, auditoría v2.4: contadores movidos = 0, dicho en la primera línea).

---

## 0 · Verificación de premisas del encargo (§2 — quien ejecuta las verifica antes de obedecer)

| # | Premisa del encargo | Rótulo del encargo | Veredicto propio | Evidencia |
|---|---|---|---|---|
| 1 | T15 exige contigüidad vía `set(range(1,max+1)) − set(nums)` | EJECUTADO | **SOSTIENE** | `tests/check.py:833-835` |
| 2 | T16 y T25 no piden contigüidad | EJECUTADO | **SOSTIENE** | `tests/check.py:795-845`; T16 es FAIL/WARN self-check |
| 3 | El asignador es `tools/cierre_acto.py:132-133` (`real = adr_max(); candidato = real + 1`) | EJECUTADO | **SOSTIENE** | `tools/cierre_acto.py:132-133` verbatim |
| 4 | NC y FP no tienen test de contigüidad | EJECUTADO | **SOSTIENE** | `grep` sobre `tests/`: 3 aciertos, los 3 la palabra «hueco» en prosa, ninguno un test |
| 5 | `.gitattributes` aplica `merge=union` sólo a `hallazgos.md` y `bitacora.md`; `hitoD-preregistro` excluido a propósito | EJECUTADO | **SOSTIENE** | `.gitattributes` leído completo; el comentario de exclusión es explícito |
| 6 | 414 filas NC en `origin/main` | EJECUTADO | **SOSTIENE** | `tail -n +2 forense/no-corrido.tsv \| wc -l` → 414 |
| 7 | 389 filas FP | EJECUTADO | **EXISTE-NO-SATISFACE (menor)** | `grep -cE "^FP-" forense/firmas-pendientes.tsv` → **387**, no 389. Diferencia de 2. Es logística, el objetivo sigue alcanzable: replanteo, sigo y lo declaro (§2, v2.15). No cambia ninguna conclusión de abajo. |
| 8 | Caso sintético de dirección: 3 ramas → 9 filas, 3 ids, 9/9 citas rotas, sin conflicto | EJECUTADO, **viaja como afirmación a refutar** | **CORROBORADA y agravada** — ver P1·Escenario 1 | caso propio a 7 sesiones |

**Premisa que el encargo NO trae y tuve que derivar (declarado, no supuesto silencioso):** el encargo pide en P4 mutar «la T15 enmendada» pero **no incluye el texto de la enmienda** ni una ruta donde viva (`NO-ENCONTRADO` en el árbol, A.4). La reconstruí desde los cinco comportamientos que dirección reporta —verde hoy · verde con un id acuñado con salto · falla con duplicado · falla con el conteo mal citado del 29/jul · falla con una cita a un ADR inexistente— que determinan unívocamente: **T15-enmendada = T15 de hoy, menos el bloque `huecos`, más una comprobación de cita a ADR inexistente.** Todo P4 se lee contra esa reconstrucción. Si el texto real difiere, P4 debe releerse.

---

## P1 · Caso sintético propio — 7 sesiones

Montado en clon desechable fuera del árbol (scratchpad), con el mismo driver `merge=union` del repo. Un defecto barato de mi propio andamio (rama base `master` vs `main`) invalidó la primera corrida del esquema A; se corrigió y se re-corrió (D-19).

### Escenario 1 · Esquema de hoy (`max+1`), 7 sesiones desde la misma base

```
filas acuñadas por sesiones: 14
ids distintos acuñados:       3
NC-0013 aparece 7 veces · NC-0014 aparece 5 veces · NC-0015 aparece 2 veces
conflictos: 0 (los 7 merges: "Auto-merging nc.tsv")
```

**14 de 14 citas rotas. Cero conflictos.** La afirmación de dirección no sólo se sostiene: escala peor que lineal. A 3 ramas, 3 ids para 9 filas; a 7 ramas, **3 ids para 14 filas** — el estrechamiento es porque `max+1` es un punto fijo: cuantas más sesiones parten de la misma base, más convergen al mismo primer id. La corrupción es silenciosa y su ancho crece con la concurrencia.

### Escenario 2 · Esquema A (bloque reservado de 10), 7 sesiones compitiendo, `bloques.tsv` **sin** union

```
s1: bloque aceptado
s2..s7: RECHAZADO (CONFLICT content en bloques.tsv) -> debe reintentar
aceptados = 1   rechazos = 6
```

A **funciona como está diseñado**: la colisión se paga antes de que exista trabajo, y se paga **ruidosa**. Ningún id duplicado. Éste es el punto fuerte real de A y hay que concederlo.

### Escenario 3 · Esquema A-prima — la friccion «arreglada» con union (ataque, ver P2)

```
bloques tomados: 7 | rangos distintos: 1
COLISION SILENCIOSA: NC-0013..NC-0022 tomado por 7 actos
```

### Escenario 4 · Esquema B (raíz de acto), 7 sesiones + rama que fusiona `main` a mitad de vuelo y vuelve a acuñar

```
filas acuñadas: 15 | ids distintos: 15 | ids duplicados: 0 | citas rotas: 0 de 15
```

La rama que fusionó `main` a mitad de vuelo y re-acuñó (`NC-20260920-ACTO-S4-99`) no perturbó a nadie: en B el id no se deriva del estado compartido, así que fusionar main a mitad de vuelo es un no-evento.

### Escenario 5 · La trampa documentada: archivo sin salto de línea final bajo union

```
NC-0012  BASE  ULTIMA FILA COMPARTIDANC-XXX-S1  ACTO-S1  fila nueva
NC-0012  BASE  ULTIMA FILA COMPARTIDANC-XXX-S2  ACTO-S2  fila nueva
apariciones de NC-0012: 2        conflictos: 0
```

Reproducida exacta, tal como la nota del 5/ago la describe. **Hallazgo que el encargo no anticipó: esta trampa es ORTOGONAL al esquema de id.** Corrompe igual `NC-0012` que `NC-20260920-ACTO-S4-01`. **Ni A ni B la atrapan**, porque no es un problema de acuñación sino del driver `union` sobre un archivo mal terminado. Necesita su propia guarda (un test que aserte salto de línea final en todo archivo con `merge=union`), y esa guarda es barata y atrapa un defecto ya reproducido dos veces — pasa el gate D-14. **Queda como candidato a NC/sucesor, fuera del perímetro de este careo.**

### Tabla P1 — qué esquema sobrevive a qué

| Escenario | Hoy (`max+1`) | A (bloque) | B (raíz de acto) |
|---|---|---|---|
| 7 sesiones desde la misma base | **MUERE** — 3 ids / 14 filas, 14 citas rotas, 0 conflictos | SOBREVIVE — 1 acepta, 6 reintentan, ruidoso | **SOBREVIVE** — 15/15 únicos |
| rama que fusiona `main` a mitad de vuelo y re-acuña | MUERE | sobrevive (el bloque ya es suyo) | **SOBREVIVE** — no-evento |
| rama que toma bloque y nunca fusiona | n/a | **HUECO PERMANENTE** — ver P2 | n/a (no hay nada que tomar) |
| `bloques.tsv` puesto en union | n/a | **MUERE, 10× más ancho** (escenario 3) | n/a |
| archivo sin salto final + union | MUERE | **MUERE** | **MUERE** |

---

## P2 · Ataque al esquema A

**Consumo real de NC, derivado del repo (no supuesto).** Universo: las 414 filas de `forense/no-corrido.tsv`, columna `acto`.

```
actos distintos: 136    media = 3.04 NC/acto    max = 12
distribucion: 1 NC:44 actos · 2:26 · 3:16 · 4:21 · 5:13 · 6:6 · 7:4 · 8:2 · 9:1 · 10:2 · 12:1
por semana:  semana 37 -> NC=161 actos=67 ;  semana 38 -> NC=253 actos=69
```

**Límite de universo declarado (A.10):** las 414 NC abarcan del **2026-09-08 al 2026-09-20 — 13 días**. El registro NC entero tiene dos semanas. La tasa de abajo es la del único período que existe, no una tasa de régimen. Ésta es la mayor debilidad de mi propio ataque y la declaro antes de usarla.

### ¿Cuántos ids quedan huecos por semana con bloques de 10?

A ~68 actos/semana: **680 ids reservados, 207 consumidos → 473 huecos por semana (69.6 % de desperdicio).**

### El ataque que sí duele: **A destruye el formato que existe para preservar**

El argumento entero a favor de A es «conserva el formato `NC-####` y todo lo que lo lee». Pero `NC-####` son cuatro dígitos: 9 999 ids. Quedan 9 585.

```
9 585 ids restantes / 680 reservados por semana = 14.1 semanas
```

**Con bloques de 10 y el ritmo medido, el espacio de cuatro dígitos se agota en ~14 semanas — poco más de tres meses.** El día que se agota hay que ensanchar a `NC-#####`, y ensanchar rompe exactamente a los mismos consumidores que A prometía no tocar, sólo que tres meses después y con 2 000 filas más citadas. **A no evita el costo de B: lo difiere y lo encarece.**

Y no hay tamaño de bloque que escape la tenaza:

| Bloque | ids/semana | agotamiento 4 dígitos | actos que necesitan 2º bloque |
|---|---|---|---|
| 12 (= el máximo observado) | 816 | **11.7 semanas** | 0/136 |
| 10 (lo que propone el encargo) | 680 | **14.1 semanas** | 3/136 (2.2 %) |
| 5 | 340 | 28 semanas | 16/136 (12 %) |
| 4 | 272 | 35 semanas | 29/136 (21 %) |

Un bloque grande mata el espacio de direcciones; uno chico devuelve la coordinación que A existía para quitar. La media 3.04 con cola hasta 12 significa que **no hay un bloque bien dimensionado**: la distribución es demasiado dispersa.

### ¿`bloques.tsv` se convierte en el nuevo archivo de choque? — **Sí, y ése es su único modo seguro.**

Escenario 2: 6 rechazos de 7. A ~68 actos/semana `bloques.tsv` es un punto de serialización, y cada rechazo obliga a re-correr el 0-bis. Eso es tolerable —es ruido, no corrupción.

**Pero la seguridad de A descansa entera en que `bloques.tsv` NUNCA entre a `merge=union`.** El escenario 3 muestra el resultado de una línea en `.gitattributes`: los 7 actos creen poseer **el mismo bloque de 10**, sin un solo conflicto. Eso es la corrupción de hoy multiplicada por diez. Y la presión para añadir esa línea será exactamente la fricción que A genera por diseño — 6 rechazos de 7. El repo ya vivió este debate: el comentario de `.gitattributes` sobre `hitoD-preregistro` («un merge manual que conflictúa es ruidoso; un union que duplica no lo es») prueba que el equipo conoce la trampa **y también que la tentación es recurrente y hay que documentarla caso por caso.** A añade un archivo más a esa lista de vigilancia permanente. **La seguridad de A es una convención; la de B es una construcción.**

### ¿Qué pasa con un bloque tomado por un acto que muere?

Hueco permanente e irreclamable sin un segador. Y el segador tendría que distinguir «acto vivo» de «acto muerto», que es justamente el estado que A.17 obliga a re-verificar por ser caro y no derivable de un nombre. Un segador así es infraestructura nueva cuyo único defecto atrapado es «se gastaron ids de más» — el mismo desperdicio que ya corre al 69.6 %. **No pasa el gate D-14: no se construye.** Los bloques muertos se aceptan, y aceleran el agotamiento calculado arriba.

---

## P3 · Ataque al esquema B — censo de consumidores

### Consumidores en código (`tests/`, `tools/`, `.claude/`)

```
tools/tablero_programa.py:362   grep -oE '^FP-[0-9]+' ... | sort -n | tail -1
tools/digesto_tramite.py:2324   RE_FP_ID = re.compile(r"\bFP-\d+\b")
tools/estado_comun.py:197       re.findall(r"^FP-(\d+)", texto, re.M)
.claude/commands/revisa.md:432  grep -oE 'FP-[0-9]+' ... | sort -n | tail -1
.claude/commands/revisa.md:435  (idem contra origin/main)
```

**Resultado que refuta la forma fuerte del temor: cuántos regex asumen cuatro dígitos = CERO.** Los cinco usan `\d+` / `[0-9]+`, cantidad variable. Un id de cinco dígitos no rompería nada hoy.

Lo que sí asumen los cinco es que el id es **numérico**; y tres de los cinco (`tablero_programa`, `estado_comun`, `revisa.md`) derivan además el **siguiente id** de `max`, que es el asignador colisionante mismo. **Superficie de código a tocar en B: 4 archivos, 5 sitios.**

### Citas en prosa y en datos

```
canon    citas= 6 640  archivos=    8
forense  citas=16 409  archivos= 1 164
data     citas= 2 561  archivos=  321
TOTAL   ~25 610 citas en ~1 493 archivos
```

### **La premisa de costo de B que NO se sostiene**

El encargo afirma que B «cuesta formato nuevo **y una tabla de alias para las 414 NC y 389 FP ya citadas**». **Esa premisa no se sostiene, y es el hallazgo que decide el careo.**

Una tabla de alias hace falta cuando un id **cambia de dueño**. En B aplicado **sólo a acuñaciones nuevas**, ningún id viejo se reasigna: `NC-0001..NC-0414` y `FP-001..FP-387` quedan congelados, siguen significando lo que siempre significaron, y las ~25 610 citas existentes siguen resolviendo. El prefijo numérico se cierra; el nuevo espacio se abre al lado. **Cero migración, cero alias, cero citas tocadas.** Lo único que se retira es el **asignador** `max+1` — 4 archivos.

Lo que sí se rompe el día que un id deja de ser numérico, con su respuesta:

- **`sort -n | tail -1` para «siguiente id»** (3 sitios) → deja de existir como concepto. Es la eliminación buscada, no un daño colateral.
- **Vistas que ordenan por id** → `NC-20260920-ACTO-NN` es **lexicográficamente ordenable por fecha**; `sort` simple mantiene el orden cronológico dentro del espacio nuevo, y el espacio viejo ordena antes que el nuevo por prefijo. No requiere lógica mixta.
- **`RE_FP_ID = r"\bFP-\d+\b"`** (digesto) → un regex; dejaría de reconocer ids nuevos. Es el único cambio con riesgo de falso negativo silencioso, y por eso el acto sucesor debe cablear su test (D-21).

**Costo real de B: 4 archivos de código + 1 regex vigilado. No 1 493 archivos.**

---

## P4 · Mutación independiente de la T15 enmendada

Contra la T15-enmendada reconstruida (ver §0). Estado real hoy: `canon/gobernanza-v1_15.md`, **568 ADR únicos, 0 huecos, 0 duplicados, 0 citas colgantes en `canon/`** — la mutación 1 de dirección («verde hoy») se corrobora.

### M1 · Un segundo `canon/gobernanza-v*.md` durante un renombre
T15 lee `newest("canon/gobernanza-v*.md")`: **un solo archivo**. Una colisión de renumeración que viva en el archivo viejo es invisible. Hoy existe un solo `gobernanza-v*`, así que el hueco está **vacío**. **Dictamen: NO IMPORTA hoy** — anotar, no instrumentar (§1).

### M2 · Cita a un ADR inexistente **fuera de `canon/`**
La comprobación de cita colgante sólo recorre `canon/*.md`. Censo propio sobre `forense/`, `data/`, `tools/`, `tests/`, `.claude/`: **0 citas colgantes** hoy. El hueco es real y está vacío. **Dictamen: NO IMPORTA hoy** — anotar, no instrumentar.

### M3 · Conteo de ADR discordante fuera de `canon/`
**261 conteos discordantes en 115 archivos** (`forense/hallazgos.md`: 23; notas de agosto: 10, 10, 9…). La enmienda no los ve, y **hace bien**: son notas fechadas, correctas en su momento — exactamente lo que la marca `{cita-historica}` existe para eximir dentro de `canon/`, y lo que `forense/notas/` es por naturaleza. Instrumentarlo exigiría marcar 261 sitios sellados para atrapar cero defectos. **Dictamen: NO IMPORTA, y además instrumentarlo sería el defecto.** §1: se anota y no se instrumenta.

### M4 · **La renumeración internamente consistente — la que sí importa**

```
T15 antes : ADR=2 dup=ninguno huecos=ninguno -> VERDE
T15 despues: ADR=4 dup=ninguno huecos=ninguno -> VERDE
```

Acto X acuña ADR-3. Acto Y acuña ADR-3 y, como fusiona segundo, **renumera a ADR-4** — obedeciendo la regla escrita. La prosa que Y selló el 19/sep dice «el piso de la celda D se adopta por ADR-3». Después del merge, ADR-3 existe, no está duplicado, no deja hueco, y **es el acto X**. La cita apunta al ADR equivocado, con contenido plausible.

**T15 está VERDE antes y después. La enmienda no cambia nada: ni la versión con contigüidad ni la enmendada lo atrapan, y ninguna versión futura puede.** Un test de integridad sobre el registro no puede detectar una cita que era correcta cuando se escribió y dejó de serlo cuando otro la desplazó, porque el registro final es perfectamente consistente consigo mismo. La única evidencia vive en la prosa sellada y en el historial, no en el estado.

**Dictamen: IMPORTA, y es el defecto central del careo.** No es instrumentable: es **prevenible por construcción, y sólo por construcción**. Un id que nunca cambia de dueño no puede re-apuntar. Esto decide entre A y B a favor de cualquiera de los dos sobre el estado actual, y es la razón por la que la enmienda a T15 es **necesaria pero no suficiente**: quitar la contigüidad deja de castigar los huecos que A y B producen legítimamente, pero no protege nada nuevo.

### Veredicto P4 sobre la enmienda
**La enmienda a T15 sale de este careo CONFIRMADA en lo que hace y ACOTADA en lo que promete.** Quitar el bloque `huecos` es correcto y es prerrequisito de A y de B por igual (los dos producen huecos legítimos: A por bloques muertos, B porque abandona la secuencia). Añadir la comprobación de cita colgante es barato y correcto. Pero **ninguna de las dos toca M4**, y M4 es el defecto que motivó el careo. Las tres mutaciones que la enmienda no atrapa (M1, M2, M3) **no importan**, y M3 no debe instrumentarse nunca. El acto sucesor puede implementar la enmienda tal como está citada, sin cambios, siempre que su ADR no afirme que protege contra la renumeración.

---

## P5 · VEREDICTO

### **B — en su variante prospectiva, sin migración y sin tabla de alias. (Llámese B′.)**

**B′:** las acuñaciones nuevas usan `NC-<AAAAMMDD>-<ACTO>-<NN>`. El espacio `NC-####` / `FP-###` se **cierra**, no se migra: las 414 NC, las 387 FP y sus ~25 610 citas quedan congeladas y siguen resolviendo para siempre. Se retira el asignador `max+1` (4 archivos, 5 sitios).

**Las cuatro razones, en orden de peso:**

1. **A destruye el formato que existe para preservar, en ~14 semanas.** Es la razón decisiva y es cuantitativa, no estética. El único argumento a favor de A —conservar `NC-####` y sus lectores— caduca dentro de un trimestre al ritmo medido, y cuando caduque habrá que ensanchar el formato con 2 000 filas más citadas. A no evita el costo de B: lo difiere y lo encarece. Y no hay tamaño de bloque que escape: grande agota el espacio, chico devuelve la coordinación.

2. **La premisa de costo de B no se sostiene (P3).** El encargo cotiza B contra una tabla de alias de 803 ids. Esa tabla no existe porque en B′ ningún id viejo se reasigna. Y ni un solo regex del árbol asume cuatro dígitos: son cinco sitios con `\d+`, en cuatro archivos. **B′ cuesta 4 archivos, no 1 493.** Cotizado bien, B es más barato que A incluso antes de contar el agotamiento.

3. **La seguridad de A es una convención; la de B es una construcción (Escenarios 2 y 3).** A es seguro sólo mientras `bloques.tsv` quede fuera de `merge=union`; una línea lo convierte en la corrupción de hoy multiplicada por diez, en silencio. Y la presión para añadir esa línea es la fricción que A genera por diseño (6 rechazos de 7). B no tiene una línea equivalente que alguien pueda escribir: no hay archivo compartido que proteger, porque no hay coordinación.

4. **B es indiferente a la concurrencia; A la serializa.** Escenario 4: 7 sesiones, incluida una que fusiona `main` a mitad de vuelo y re-acuña, → 15/15 ids únicos, 0 citas rotas. La ventana de «cero ramas de acto vivas» que mesa necesita para A es una restricción permanente sobre el programa; B no necesita ventana ninguna, ni para adoptarse ni para operar.

**Lo que hay que concederle a A, y que mesa debe pesar:** A es la única opción que mantiene un id corto, legible y dictable en voz alta. `NC-20260920-MARCADOR-ENLACE-2-01` es feo y largo, y aparecerá 25 000 veces en prosa. Si mesa valora la legibilidad del id por encima de todo lo demás, A es defendible **con bloque de 4 y ensanchamiento a cinco dígitos ya planeado** — pero entonces mesa está eligiendo pagar la coordinación (21 % de actos con segundo bloque) y el ensanchamiento, a cambio de ids cortos, y debe decirlo así.

### Lo que este veredicto NO dice

No dice que B′ arregle el archivo sin salto de línea final (Escenario 5): **no lo arregla, y A tampoco**. Ése es un defecto del driver `union`, ya reproducido dos veces, con guarda barata, y debe ir a su propio sucesor.
No dice que la enmienda a T15 proteja contra la renumeración: **no protege** (M4), y su ADR no debe afirmarlo.
No decide: mesa decide.

### **Falsabilidad — qué tendría que ser verdad para que cambie de opinión**

1. **Que el ritmo de 68 actos / 207 NC por semana sea un artefacto del arranque.** Es mi eslabón más débil y lo declaro: las 414 NC abarcan **13 días** (8–20/sep), así que mi tasa es la del único período que existe. **Si el régimen real resulta ser ≤ 15 actos/semana, el agotamiento de A se mueve de 14 semanas a más de un año, la razón 1 cae, y A gana por legibilidad.** Falsador concreto: volver a derivar esta misma tabla dentro de cuatro semanas, sobre un universo de seis semanas. Si `NC/semana < 60`, este veredicto queda **VENCIDO EN ALCANCE** y se re-carea.
2. **Que exista un consumidor que exija orden total por id entre el espacio viejo y el nuevo**, y que no se satisfaga con «viejo antes que nuevo». Mi censo cubrió `tests/`, `tools/`, `.claude/` y el conteo de citas en `canon/`, `forense/`, `data/` — pero censé **consumidores de formato**, no consumidores de **orden**. Si aparece una vista que deba intercalar cronológicamente ambos espacios, B′ necesita lógica mixta y su costo sube.
3. **Que mesa declare que la ventana de cero-ramas-vivas es el régimen permanente** y no una ventana. Si el programa pasa a un acto a la vez de forma estable, la razón 4 se vacía, la 3 se debilita (sin concurrencia no hay fricción que tiente al `union`), y quedan sólo la 1 y la 2 — que siguen bastando, pero ya no con holgura.
4. **Que la propuesta A traiga un `bloques.tsv` con test propio que asegure su exclusión de `union` y no-solapamiento de rangos.** Eso neutralizaría el escenario 3 y subiría a A a paridad de seguridad — a costa de infraestructura nueva que debe pasar D-14 por sí misma.

### Tercer esquema — **entregado como candidato, no como veredicto** (§6 latitud)

**C · Sufijo de desempate sobre el formato de hoy.** Se acuña `NC-####` como hoy, y ante colisión detectada al fusionar **no se renumera: se sufija** (`NC-0423`, `NC-0423b`). Conserva el formato y su legibilidad (razón de A), no reasigna nunca un id ya acuñado (mata M4, razón de B), no necesita coordinación previa ni `bloques.tsv` (mata el escenario 3), y no agota el espacio más rápido que hoy. Su costo: el id deja de ser numérico puro —el mismo costo que B en los 4 archivos censados— y exige una guarda que detecte la colisión al fusionar, que hoy no existe y que `union` oculta por construcción. **No lo evalué a fondo y no lo recomiendo desde aquí**; lo dejo porque, si mesa se inclina por A por legibilidad, C parece darle la legibilidad sin la tenaza de bloque del P2. Merece su propio careo si mesa lo quiere.

---

## Firma pendiente que este acto genera

Mesa debe adjudicar entre **A**, **B′** (recomendado), **C** (candidato sin evaluar) o **ninguno**, y declarar si acepta que el espacio `NC-####`/`FP-###` se cierre en lugar de migrarse.

## NO-CORRIDO / RESERVAS

| Qué no se corrió | Razón | Impacto | Sucesor |
|---|---|---|---|
| Evaluación a fondo del esquema C | FUERA-DE-PERÍMETRO | C se entrega como candidato sin conteos propios; mesa no puede adjudicarlo hoy | careo propio si mesa lo pide |
| Guarda de salto de línea final para archivos `merge=union` (Escenario 5) | FUERA-DE-PERÍMETRO | la trampa sigue viva para los dos esquemas y para el de hoy | acto sucesor, ver `forense/hallazgos.md` |
| Censo de consumidores de **orden** por id (falsabilidad 2) | FUERA-DE-PERÍMETRO | el costo de B′ podría subir si existe una vista que intercale ambos espacios | acto que implemente el esquema adjudicado |
| Verificación de las 389 vs 387 filas FP (premisa 7) | NO-VERIFICABLE-AQUÍ | ninguno: la diferencia de 2 no toca ninguna conclusión | acto que implemente el esquema adjudicado |
| Implementación de la enmienda a T15 | FUERA-DE-PERÍMETRO (el encargo lo excluye explícitamente) | ninguno: el careo la dictamina, no la aplica | acto sucesor que enmiende T15 |

## CONSUMIDO

PR: pendiente de apertura al cierre de este acto.
