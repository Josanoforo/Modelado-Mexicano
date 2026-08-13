# 2026-08-13 · ENCARGO ADR-PROVISIONALIDAD — nota de cierre

Huso de Mesa (`TZ=America/Mexico_City date`): corrida ~21:25–~22:10 del **12/ago/2026** (el reloj de Mesa cruza medianoche a mitad de este acto; el encargo, ADR-72 y esta nota se fechan **13/ago/2026** siguiendo la fecha que el propio encargo declara en su cabecera y en el texto VERBATIM del ADR — no se corrige, se declara la pequeña discrepancia de huso). Entorno: **NUBE**, `cloud_default`, sin sonda (ADR-59(b)) — repo-only, sin red a dominios de datos, sin microdato, sin corpus, tal como el encargo asigna.

Este acto es de escritorio y de cascada: no abre `data/raw`, no corre ningún estimador, no toca `milpa/**` ni `tests/**` ni `tools/**`.

---

## 1 · El número de ADR — derivado dos veces, contra dos `main` distintos

**Primera derivación**, contra `origin/main = b17a6f6` (el SHA de redacción del encargo, confirmado idéntico entre `HEAD` local y `origin/main` antes de escribir nada): `grep -oE '**ADR-[0-9]+' canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -nu` → **71 únicos, máximo 71** → siguiente = **72**.

**A mitad de ARRANQUE, `origin/main` se movió**: `b17a6f6` → `dcc4f6a` (PR #196, `ACTO ENLACE-1`). Re-derivado antes de escribir el número, como exige §2.1 del encargo: `git show origin/main:canon/gobernanza-v1_15.md` seguía en 71 únicos/71 máximo — PR #196 no toca `canon/`, sin colisión. Se hizo `git merge origin/main` (limpio, sin conflicto — los únicos archivos que tocó PR #196 no se solapan con nada escrito hasta ese momento por este acto) antes de sellar. **ADR-72 se sella contra el `main` real post-merge, no contra el del encargo.**

PR #196 sí tocó `data/curacion-registro/relaciones.tsv` (42 líneas), lo cual afecta directamente la evidencia de la ADDENDA 5 (ver §5) — vuelto a verificar después del merge, no antes.

---

## 2 · Sitios de cascada tocados, con línea

- `canon/gobernanza-v1_15.md:2` — cabecera de conteo, `71 ADR` → `72 ADR`.
- `canon/gobernanza-v1_15.md:940` — nueva entrada `**ADR-72 · ...**` (texto VERBATIM de §2.3 del encargo, sin editar), insertada después de ADR-71 y antes de `## 5. Deuda declarada`.
- `canon/gobernanza-v1_15.md` (tras la entrada, antes del `---` de cierre) — enmienda declarada de ADDENDA 5 (segundo contador + evidencia), rotulada como enmienda, no como reescritura del texto sellado.
- `canon/estado-programa-v1_10.md:27` — tabla "Registro de artefactos", `71 ADR` → `72 ADR`.
- `canon/estado-programa-v1_10.md` (línea de L0, "Gobierno — completo y al día") — `71 ADR` → `72 ADR`, más cláusula nueva "; a 72 después, con ADR-72, 13/ago/2026, ENCARGO ADR-PROVISIONALIDAD (...)" al final de la narrativa histórica, mismo patrón que cada ADR anterior desde el 29 hasta el 71.
- `canon/estado-programa-v1_10.md:130` — "el total de WARN de la suite es" `101` → `105` (la cifra "T03 produce hoy 29 WARN" de la misma línea **no** se toca: T16 no la vigila, y tocarla habría excedido el perímetro de este acto).
- `canon/estado-programa-v1_10.md:222` — `**18 FAIL · 101 WARN**` → `**19 FAIL · 105 WARN**`.
- `canon/gobernanza-v1_15.md:760` (dentro de ADR-62(g), sellado 4/ago) — `**18 FAIL · 95 WARN**` → `**19 FAIL · 105 WARN**`.
- `canon/gobernanza-v1_15.md:852` (dentro de la Cascada de ADR-66, sellado 10/ago) — `**18 FAIL · 95 WARN**` → `**19 FAIL · 105 WARN**`.
- `forense/registro-recalculo-v1_0.md` — archivo nuevo, append-only, cinco entradas de ADR-72 §2.4 más la entrada `0` de la enmienda.

**NO tocado, deliberadamente** (ver §4): `canon/gobernanza-v1_15.md:938`, dentro del propio texto sellado de ADR-71.

---

## 3 · La cifra de suite — tres corridas, la trampa del encargo más una segunda vuelta

El encargo asumía, contra su propia redacción (`b17a6f6`): real `22 FAIL · 104 WARN`, punto fijo `18 FAIL · 104 WARN`. **Esa aritmética no sobrevivió el propio ARRANQUE de este acto** — PR #196 (ENLACE-1) fusionó a mitad de camino y movió el terreno.

**Corrida 1 — contra `b17a6f6`, antes de fusionar `origin/main`:**
```
22 FAIL · 104 WARN
```
Coincide exactamente con lo que el encargo declaraba, verificado antes de tocar nada.

**Corrida 2 — contra `dcc4f6a`, después de `git merge origin/main`, antes de escribir ADR-72:**
```
22 FAIL · 106 WARN
```
El WARN subió (104→106) por el propio contenido que trajo PR #196; el FAIL se mantuvo en 22 (T16 seguía aportando 4, con cifras "vigente…101/95 WARN" vs. "real 106 WARN").

**Corrida 3 — después de insertar la entrada ADR-72 y abrir `forense/registro-recalculo-v1_0.md`, antes de corregir los 4 sitios de T16:**
```
23 FAIL · 105 WARN
```
El WARN bajó un punto (el `T03` colgante que el propio archivo de encargo generaba contra `registro-recalculo-v1_0.md` se resolvió solo al crear el archivo). **El FAIL subió a 23 — no por T16, sino por un fail nuevo de T15**, ver §4.

**Corrida 4 — final, con los 4 sitios de T16 corregidos a `19 FAIL · 105 WARN`:**
```
19 FAIL · 105 WARN
```
`T16` vuelve a `[ ok ]`. Desglose verificado: T09=8 · T05=5 · T06=2 · T07=1 · T08=1 · T11=1 (=18, idéntico al desglose que el encargo declaraba, sin cambio) **+ T15=1** (nuevo, ver §4) **+ T16=0** (corregido) = **19**. WARN: T03=39 · T10=65 · T13=1 = 105.

**El punto fijo real de este acto no es `18 FAIL · 104 WARN` (el del encargo): es `19 FAIL · 105 WARN`**, derivado en el momento de cerrar, no copiado de la redacción. `tests/check.py --baseline` corrido antes y después de cada corrida — comandos y salidas arriba, ninguno tecleado.

---

## 4 · Hallazgo NO resuelto al cerrar COMMIT 2 — resuelto después, ver §9

*(Encabezado y cuerpo de esta sección sin editar: son el estado real al cerrar COMMIT 2, antes de que mesa decidiera. §9 narra la resolución, sin borrar esto.)*

Al sellar `**ADR-72`, `python3 tests/check.py --baseline` pasó a **ROJO** — no por T16 (que este acto sí resuelve, §3), sino por **T15 (T-ADR-COUNT)**, con exactamente un fallo nuevo:

```
canon/gobernanza-v1_15.md:938 cita 71 ADR; gobernanza tiene 72 únicos
```

**Causa raíz.** `canon/gobernanza-v1_15.md:938` vive **dentro del propio texto sellado de ADR-71** — su párrafo "Cascada — historia completa de la numeración, no solo el resultado" narra la saga de renumeración de ese ADR (71→70→71) y, para eso, escribe literalmente *"Sitios de cascada tocados (a `71 ADR`): ..."*. Es el **único** ADR de los 71 que embebe un dígito de conteo bruto en su propia narrativa — ADR-44 a ADR-70 aprendieron a evitarlo (dicen "conteo de ADR vía receta T15" o "N de M ADR" solo en la cabecera/tabla, nunca dentro de la prosa de una entrada ya sellada), precisamente porque un dígito embebido ahí se vuelve una mina para el siguiente ADR. ADR-71 no tuvo esa opción: necesitaba narrar la historia completa de su propia renumeración, y esa historia incluye el número.

**T15, a diferencia de T16, no tiene excepción histórica.** `t15_adr_count()` (`tests/check.py:486-507`) escanea *todo* `canon/*.md` con `re.finditer(r"(\d+)\s*ADR\b", l)`, línea por línea, sin ningún marcador equivalente al `_CAMBIO_FECHADO` de T16 (que exime líneas con el formato `> **vX.Y — DD/mon.**`). Cualquier cita `"N ADR"` en cualquier `canon/*.md`, sin importar si narra un hecho pasado o un estado presente, debe igualar el conteo único vigente — hoy, 72.

**Por qué este acto NO lo corrige.** Un cambio mecánico de dígito (`71`→`72` en la línea 938) **no es un cascada limpio, como sí lo fue en los 4 sitios de T16 (§3)**: la misma oración de ADR-71, dos cláusulas antes, dice *"real (únicos en gobernanza) pasa de 70... a 71, contiguo"* — cambiar solo el dígito posterior a `72` dejaría el propio párrafo **contradiciéndose consigo mismo** (dice `71` y `72` dos frases seguidas, describiendo el mismo momento). Arreglarlo de verdad exigiría reescribir la narrativa de ADR-71 — decisión de contenido sellado, fuera del perímetro que este encargo concede (`§4: la entrada del ADR nuevo`, no las anteriores) — o ampliar `T15` con una excepción histórica análoga a la de T16 — cambio a `tests/**`, explícitamente `NO ESCRIBE` en este encargo. Ninguna de las dos es decisión de este acto.

**Lo que este acto sí hace: reportarlo, íntegro, sin maquillarlo** — exactamente lo que §3 del encargo exige ("si un test truena, ese es el hallazgo"), y exactamente el mismo criterio que el propio encargo ya aplicaba a la pregunta de regenerar el baseline ("decisión de mesa, no de este acto"). `tests/baseline.json` (HEAD congelado `948ad70`, el que dejó ENLACE-1 al fusionar) queda en **ROJO, con una sola entrada nueva**: `T15: canon/gobernanza-v1_15.md: cita 71 ADR; gobernanza tiene 72 únicos`. Este acto **no corre `--freeze`** — es justo la clase de decisión que el encargo reserva a mesa.

---

## 5 · ADDENDA 5 — verificada, no copiada a ciegas

Dos addenda llegaron juntas a mitad de ARRANQUE, antes de escribir cualquier archivo (archivadas verbatim en `forense/encargos/2026-08-13-adr-provisionalidad.md`, sección "Addenda recibida"). La ADDENDA 4 es de `SONDA-1`, acto ajeno — no se ejecuta aquí. La ADDENDA 5 ("un contador más y una evidencia más") es de este acto, y llega explícita en que entra como enmienda de COMMIT 2, sin reescribir COMMIT 1 — así se hizo.

**Verificado antes de escribir, no copiado de la addenda:**
- `forense/censo-estimabilidad-coeficientes-v1_0.md` filas 12/13/14 → confirmado `SIN-RUTA`, "Ninguna llave aplica", verbatim.
- `data/curacion-registro/relaciones.tsv`, N12/N13/N14 → confirmado al menos una fila cada una con `capa4_apertura_mapeo=EXISTE-SATISFACE` + `clasificacion_relacion=CONFIRMADA` (`REL-4a609c6633a4bafac14a6930` · `REL-fe202a3fa76f0516a6e27f8b` · `REL-5741e12ce3e0a0e076ee48fc`), verificado **dos veces** — antes y después del merge de PR #196, que tocó ese mismo archivo — las tres filas sobrevivieron intactas.
- `grep -rln "censo-estimabilidad" tests/ tools/` → `0`, confirmado.
- `git log --oneline -- data/curacion-registro/relaciones.tsv` → **la propia addenda quedó desactualizada por el merge**: decía "un solo commit, `16180e6`"; al cerrar este acto son **dos** (`16180e6` + `1cd2797`, este último del propio PR #196 que se fusionó a mitad de ARRANQUE). Se declara la cifra vigente en la enmienda, no la de la addenda — mismo criterio que este encargo exige para el número de ADR en §2.1.

**No se hizo el cotejo completo de las 15 filas del censo** — la addenda llama a esto "derivable con un awk", pero el censo no trae un `necesidad_id` cruzable por máquina; las 3 filas confirmadas se identificaron por lectura semántica, la misma clase de trabajo que resolver las 12 restantes exigiría. Hacerlo aquí habría abierto el censo en bloque — lo que el Método de ADR-72 prohíbe. Queda como la entrada `0` del registro, sin cerrar.

---

## 6 · Contadores que NO se mueven — declarado, como exige §3 del encargo

`13 de 27` (Hito D) · `15 coeficientes, 0 medidos` · `9 de 14` (condicionales) · `llaves de identificación ejercidas 0 de 2` · `capa2 SI 24 de 197`. **Ninguno se mueve con ADR-72 ni con su enmienda.** El contador nuevo que ADR-72 instituye (`8 de 550 = 1.45%`) y el segundo que su enmienda añade (`3 filas confirmadas en desacuerdo`, cotejo parcial) son ambos contadores **sobre el aparato del programa**, no sobre México — ninguno mide algo nuevo sobre el país.

---

## 7 · La línea honesta

**Este acto no mide nada.** Lo que hace es sellar que el cuerpo de cálculo previo es provisional, abrir la cola donde se recalculará entrada por entrada, y — sin buscarlo — encontrar que la propia maquinaria de conteo del canon (T15) tiene un punto ciego que su hermana T16 no tiene. Lo primero era el encargo. Lo segundo es el hallazgo que produjo hacerlo con cuidado.

---

## 8 · Un tercer hallazgo, pequeño y sí corregido: T02 colisionaba consigo mismo

El propio encargo nombra, en su lista `ESCRIBE` de §1, dos archivos con el **mismo nombre base**: `forense/notas/2026-08-13-adr-provisionalidad.md` y `forense/encargos/2026-08-13-adr-provisionalidad.md`. `t02_duplicates()` normaliza por `os.path.basename()`, sin considerar directorio — apenas existieron los dos, T02 pasó a FAIL (`nombre normalizado colisiona: forense/notas/... · forense/encargos/...`), verificado que ningún par igual existía antes en el repo (`comm -12` entre los dos directorios, vacío hasta este acto).

**Corregido aquí, a diferencia del hallazgo de §4.** Esta colisión es distinta en un punto que importa: es enteramente propia de este acto (los dos archivos son míos, de hoy), evitarla no exige tocar texto sellado de nadie ni ampliar `tests/**`, y dejarla habría sido un FAIL nuevo, evitable, por descuido de nomenclatura — no un hallazgo genuino sobre el estado del programa. Se renombra la nota a `forense/notas/2026-08-13-adr-provisionalidad-cierre.md` (el archivo de encargo conserva su nombre exacto, que es el que fija la convención de archivado A.3); las dos referencias cruzadas (este archivo y `forense/hallazgos.md`) se actualizan en el mismo commit. `python3 tests/check.py` reverifica T02 en `[ ok ]` tras el cambio.

---

## 9 · Resolución de §4 — mesa decidió, mismo día, vía PR #199

El hallazgo de §4 se reportó, no se resolvió, y se abrió PR #199 con `--baseline` en ROJO por esa única entrada, exactamente como §4 documenta. Mesa (el operador humano, en el hilo de la PR) respondió directamente: *"solve Pr cant merge"* — una instrucción explícita de resolver el bloqueo, dada fuera del marco de este encargo (que había reservado la decisión) y por encima de él. Las tres opciones que §4 dejó abiertas seguían siendo las mismas; se implementó la **opción 2**: ampliar `T15` con una excepción histórica, mirando exactamente el mecanismo que `T03` ya usa (`MARCA_ILUSTRATIVA` / `{cita-ilustrativa}`, `tests/check.py:198-208`).

**Por qué esa opción y no las otras dos.** La opción 1 (reescribir la narrativa de ADR-71) habría alterado contenido de una decisión ya sellada para maquillar una cita que, en su momento, era correcta. La opción 3 (`--freeze`) habría aceptado el hueco sin cerrarlo — el mismo `t15_adr_count()` seguiría sin poder distinguir una cita histórica de una vigente, y el próximo ADR con la misma necesidad narrativa volvería a pisar la misma mina. La opción 2 corrige la causa raíz, no reescribe ninguna palabra de ADR-71, y no oculta nada en un archivo de línea base — es aditiva y reversible.

**Implementación, verbatim del cambio:**
- `tests/check.py` — `MARCA_HISTORICA = r"` `?\s*\{cita-historica\}"` (el `` `? `` opcional porque, a diferencia de T03, el regex de T15 no incluye los backticks de la cita en el match); el bucle de `t15_adr_count()` salta una cita si la marca la sigue de inmediato, idéntico patrón a T03's `re.match(MARCA_ILUSTRATIVA, l[mo.end():])`.
- `canon/gobernanza-v1_15.md:938` — se añadió ` {cita-historica}` inmediatamente después de `` `71 ADR` ``, dentro del párrafo de ADR-71. **Ninguna otra palabra de ese párrafo se tocó.** La cita sigue diciendo, correctamente, lo que decía: que ADR-71 trajo el conteo a 71.

**Efecto de segundo orden, derivado, no asumido.** Corregir T15 cambia lo que T16 considera "real": su subproceso interno excluye solo T16 de sí mismo, no T15 — con T15 limpio, el "real" que T16 compara bajó de `19 FAIL` a `18 FAIL` (WARN sin cambio, 105). Los 3 sitios que COMMIT 2 había fijado en `19 FAIL · 105 WARN` (`estado-programa-v1_10.md:222`, `gobernanza-v1_15.md:760,852`) se corrigieron una vez más, a `18 FAIL · 105 WARN` — el mismo mecanismo de punto fijo de §3, una vuelta más.

**Corrida 5 — final, con T15 exento y el punto fijo re-derivado:**
```
18 FAIL · 105 WARN
```
Desglose sin cambio en el contenido: T09=8 · T05=5 · T06=2 · T07=1 · T08=1 · T11=1 (=18, el mismo desglose de siempre, idéntico al que el propio encargo declaraba el 13/ago contra `b17a6f6`). T15=0. T16=0.

```
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 948ad70343320b62f000d31fd39e2b2b68336ad9)
(3 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

`tests/check.py` completo: los 22 tests nombrados en `[ ok ]`/`[warn]`/`[FAIL]` verificados uno a uno; T02, T15, T16, T20 en `[ok]`. No se corrió `--freeze` — no hizo falta: no quedó ninguna entrada nueva que aceptar.

**Alcance de este cambio, declarado.** Toca `tests/**`, fuera del `NO ESCRIBE` original del encargo — autorizado explícitamente por mesa en el hilo de la PR, no una decisión unilateral de este acto. No se mintió un ADR nuevo para esto: es mantenimiento de aparato de verificación, misma clase que las excepciones de `data/raw` y de nomenclatura por-run que T02 ya tenía, ninguna de las cuales necesitó ADR propio tampoco.

---

**Requisito de salida.** Este archivo; línea en `forense/hallazgos.md` (append, merge local) — dos entradas, el hallazgo (§4) y su resolución (§9); `forense/encargos/2026-08-13-adr-provisionalidad.md` actualizado de `VIVO` a `CONSUMIDO`; `tests/check.py --baseline` corrido al cierre final — **VERDE**, cero entradas nuevas, tres mejoras frente al congelado de ENLACE-1.
