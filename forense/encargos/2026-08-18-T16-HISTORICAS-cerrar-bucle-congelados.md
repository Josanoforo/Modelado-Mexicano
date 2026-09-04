# ENCARGO · ACTO T16-HISTÓRICAS — cerrar el bucle de congelados por su última puerta

**SHA de redacción:** `d2fedb0` (merge #253, `origin/main`, verificado por `git ls-remote` el 18/ago/2026)
**Entorno asignado:** **NUBE** (sesión nueva, clon fresco).
**NO lo lances en Ubuntu:** esa caja está en pausa por degradación de servicio, y `acto-b2-v7` sigue abierta ahí.
**Estado:** `CONSUMIDO` — ejecutado en la rama `claude/new-session-cy41al`, commits `6e02d62` (commit 1, `T16` honra `MARCA_HISTORICA`), `8249140` (commit 2, marca las ocho narraciones de acto pasado), y los commits de cierre de commit 3/4 (tabla de sellos derivada, `ADR-97`, `FP-50` → `FIRMADA`, fila `FP-52` nueva). PR no abierto en este acto — no solicitado explícitamente por quien lanzó el encargo; la rama queda lista para revisión. Detalle completo, comando por comando, en `forense/notas/2026-08-18-t16-historicas.md`.
**Gatea:** `FP-50` (abierta por `ACTO CI-CATEGORÍA`, `ADR-96`).

---

════════ ARRANQUE — hazlo antes de leer el resto del encargo ════════
Reporta las cinco líneas de abajo y NO empieces hasta tenerlas. Si algo
no cuadra, PARA y repórtalo: encontrar que el terreno no es el que el
encargo supone es entregable, no interrupción.

1 · REPO. Localiza el CLON EXISTENTE. No clones uno nuevo salvo que no
haya ninguno, y si clonas, dilo.
Reporta:  ruta absoluta  ·  git log -1 --format="%h %s"  ·  git status
⚠️ No arranques desde el home.

2 · SHA. Escrito contra `d2fedb0`. Si main se movió: NO es PARO — refresca,
re-deriva el censo del §1, y reporta la diferencia antes de editar.
⚠️ **La rama `acto-b2-v7` está viva** y toca un solo archivo,
`tools/curador_registro/correr-olas-v7.py`. Perímetro disjunto del tuyo,
verificado. Si fusiona mientras trabajas, no te afecta.

3 · data/raw. AUSENTE NO ES PARO, y este acto **no la usa**. Repórtalo y sigue.

4 · ENTORNO. Reporta los tres valores crudos (A.2):
```sh
echo "[${CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE:-sin_variable}]"
curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
ls data/raw/ 2>/dev/null | head -1
```
NUNCA `curl -I`. Este acto no toca microdato ni red de datos: un 403 de
INEGI aquí es un hecho sobre la allowlist de esta caja, no sobre INEGI (A.5).

5 · ESPEJO. Toda cifra sale del clon de (1), con el comando a la vista.
════════════════════════════════════════════════════════════════════

═══ VERIFICACIÓN DE EXISTENCIA — contestada por quien escribe el encargo ═══

**1 · ESTRUCTURA.** Gobiernan este dominio `tests/check.py` (el vigía),
`canon/gobernanza-v1_15.md` y `canon/estado-programa-v1_10.md` (las citas
vigiladas), `tests/baseline.json` (el congelado) y
`forense/firmas-pendientes.tsv` (A.12). Este encargo escribe los tres
primeros y el cuarto. **NO escribe `tests/baseline.json`** — deliberadamente,
ver §5. `data/INFRAESTRUCTURA-v1_0.md` no gobierna `tests/` ni `canon/`,
verificado.

**2 · CONTENIDO.** Corrido contra `d2fedb0`, salida cruda:

```
grep -n "MARCA_HISTORICA" tests/check.py          → 536 (definición) · 560 (uso, dentro de t15_adr_count)
grep -c "MARCA_HISTORICA" tests/check.py          → 2      # T16 NO la usa
grep -rn "cita-historica" canon/                  → gobernanza:970 · gobernanza:1686 · gobernanza:1700
```

- El mecanismo de exención inline: **`EXISTE-SATISFACE`**. `{cita-historica}`
  ya existe, ya es canon, ya lo honra `T15` desde la sesión de tests del
  29/jul, y ya está en uso tres veces en `gobernanza`. **No hay que inventar
  ninguna convención nueva.**
- Que `T16` lo honre: **`NO-ENCONTRADO`** en `tests/check.py` — `t16_suite_self_check`
  solo consulta `_CAMBIO_FECHADO`, nunca `MARCA_HISTORICA`.
- El remedio ya construido: **`NO-ENCONTRADO`** en el árbol.

**3 · COBERTURA RETROACTIVA.** `MARCA_HISTORICA` nació con `T15` (29/jul/2026);
`gobernanza` y `estado-programa` son anteriores. Todo lo escrito antes de esa
fecha nunca tuvo ocasión de llevar el marcador, y su ausencia **no significa
que la cita sea vigente**. Es exactamente por eso que el censo del §1 se
deriva por lectura de cada línea, no por presencia del marcador.

════════════════════════════════════════════════════════════════════

**PERÍMETRO Y CONCURRENCIA.** Este acto toca, y solo esto:
`tests/check.py` · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md` ·
`forense/firmas-pendientes.tsv` · `forense/notas/<fecha>-t16-historicas.md` ·
`forense/hallazgos.md` (append, `merge=union`) · `forense/encargos/` (marcar CONSUMIDO).
En paralelo puede fusionar `acto-b2-v7`, cuyo único archivo es
`tools/curador_registro/correr-olas-v7.py`. Cero solape, verificado por
`comm -12` sobre las dos listas de `git diff --name-only`.
Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba
mal calculado y saberlo vale más que el atajo.

---

## 0 · El defecto, medido y no concebido — y no es solo de CI

`ACTO CI-CATEGORÍA` sacó `T22`(a) de la comparación y el CI volvió a distinguir.
Quedó una puerta abierta, y al medirla resultó ser más grande que un problema de CI.

**Censo derivado contra `d2fedb0` — 11 citas bajo la vigilancia de `T16` en `canon/`:**

| clase | n | dónde |
|---|---|---|
| exenta por changelog (`_CAMBIO_FECHADO`) | 1 | `estado-programa:50` |
| **FAIL permanente** | 3 | `gobernanza:1106` · `:1136` · `:1658` |
| **"rastreador vivo"** — hay que resincronizarla a mano cada vez que el WARN se mueve | **7** | `estado-programa:129`, `:221` · `gobernanza:764`, `:856`, `:1274`, `:1387`, `:1393` |

**Y aquí está lo que no es un problema de CI.** De esas 7, **cinco están dentro de
ADR ya sellados y narran lo que un acto pasado midió**. Se las ha venido
sobreescribiendo hacia adelante para mantener el test verde. El caso más claro,
derivado por `git show`, no supuesto:

> `gobernanza:764` (ADR-62) dice hoy: *"la cifra real al correr `tests/check.py`
> **en este acto** es **19 FAIL · 135 WARN**"*.
> **"Este acto" es ADR-62, sellado el 5/ago/2026 en `4195f37`, y en ese commit la
> línea decía `18 FAIL · 95 WARN`.**
> La línea afirma hoy que un acto del 5/ago midió una cifra que no existió hasta el 18/ago.

Lo mismo en `:856`, `:1274`, `:1387` y `:1393`. Los rastros entre paréntesis que
han ido creciendo —*"(105 al sellar este inciso; baja a 104 por…; sube a 107 por…)"*—
son el programa compensando en prosa un número que sabía falso en las negritas.

**Qué le costó a un lector (impuesto de v2.3, pagado).** `gobernanza` es el registro
de decisiones: qué se decidió y con qué evidencia. **Cinco ADR sellados cargan hoy una
medición que nunca hicieron.** Y en el camino, cada resincronización obligada fue un
CI rojo, y cada CI rojo fue un candidato a recongelado — de ahí salen varios de los 22.

---

## 1 · COMMIT 1 · Que `T16` honre el marcador que ya existe

**No inventes convención.** `T15` ya resuelve este problema exacto con
`MARCA_HISTORICA` (`tests/check.py:536`, usado en `:560`), con la semántica correcta:
*"la marca exime SOLO la cita inmediatamente anterior; una línea con dos citas y una
marca deja la otra vigilada"*. `T16` simplemente no la lee.

El parche es de cuatro líneas, en `t16_suite_self_check`, espejo exacto de `T15`:

```python
m1 = re.search(r"\*\*(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN\*\*", l)
if m1 and re.match(MARCA_HISTORICA, l[m1.end():]):
    m1 = None
if m1 and not historico:
    ...
m2 = re.search(r"total de WARN de la suite es\s*\*{0,2}(\d+)", l)
if m2 and re.match(MARCA_HISTORICA, l[m2.end():]):
    m2 = None
if m2 and not historico:
    ...
```

Y **amplía el `LÍMITE DECLARADO` del docstring de `t16_suite_self_check`**: hoy dice que
el único marcador mecánico de "esto es historia" es `_CAMBIO_FECHADO`. Deja de ser cierto
con este commit. Dilo, con la fecha y el acto.

**Los tres controles, y córrelos antes de commitear. Pega la salida cruda de cada uno.**

| # | qué haces | qué DEBE pasar |
|---|---|---|
| N1 | inyectas en `canon/` una cita vigente **mala** y **sin** marcador: `Control: **99 FAIL · 99 WARN** sin marca.` | `T16` **FAIL** — la protección sigue intacta |
| N2 | la **misma** cita, ahora con ` {cita-historica}` justo detrás | `T16` **[ ok ]** — el marcador exime |
| N3 | `T15` con los 8 marcadores nuevos del §2 | sigue **[ ok ]** — no le rompiste su propio uso del marcador |

⚠️ **N1 es fácil de romper como control y ya se rompió una vez al verificar este
encargo.** El regex exige `**` **inmediatamente** antes del dígito: `**Prueba: 99 FAIL
· 99 WARN**` **no matchea** y da un falso verde tranquilizador. Si N1 sale `[ ok ]`,
sospecha de tu control antes que del código. Revierte las inyecciones antes de seguir.

---

## 2 · COMMIT 2 · Marcar las ocho, sin tocar sus cifras

Añade ` {cita-historica}` **inmediatamente después** de la cifra en negritas, en las
ocho narraciones de acto pasado: `gobernanza:764` · `:856` · `:1106` · `:1136` ·
`:1274` · `:1387` · `:1393` · `:1658`.

**Re-deriva el censo tú mismo antes de marcar** — los números de línea de arriba son
de `d2fedb0` y se mueven con cualquier edición previa. Clasifica cada una de las 11 por
lectura, no por número de línea, y **reporta tu censo**. Si tu clasificación difiere de
la tabla del §0, la que manda es la tuya: repórtala y di en qué difiere.

**Criterio de clasificación, y es el único que importa:** ¿la línea afirma un estado
**vigente** de la suite, o narra lo que un acto **pasado** midió? Si narra el pasado,
la cifra no debe seguir al real y va marcada. Si afirma el presente, se queda vigilada.

**Las dos que NO se marcan:** `estado-programa:129` y `:221`. Son declaraciones de
estado vigente y deben seguir el número real — ésa es su función. **Verificado: hoy ya
traen los valores correctos (`135 WARN` y `19 FAIL · 135 WARN`) y no hay que
resincronizarlas**, porque siempre declararon el núcleo sin `T16` y el remedio hace que
el total coincida con el núcleo.

**Y dilo sin maquillar en la nota:** marcar una cita cuya cifra es falsa **congela la
falsificación en su sitio**. Es deliberado y es el mal menor: la alternativa es
seguir reescribiéndola hacia adelante cada semana, que es lo que produjo el defecto.
La verdad histórica se pone sobre la mesa en el §3; restaurarla es de mesa, no tuyo.

---

## 3 · COMMIT 3 · Qué decía cada una cuando se selló — derivado, no restaurado

Para cada una de las ocho, recupera el valor que la línea traía en el commit que la
selló. **Es recuperable — probado con `:764`:**

```sh
git log --reverse --format="%h" -S "<fragmento estable de la línea>" -- canon/gobernanza-v1_15.md | head -1
git show <sha>:canon/gobernanza-v1_15.md | grep -oE "<fragmento>.{0,220}"
```

Entrega **una tabla** en la nota del acto: cita · ADR · fecha de sello · **cifra
original** · cifra de hoy · commits que la sobreescribieron. Ejemplo ya derivado, para
que compares tu receta contra un caso con respuesta conocida:

> `gobernanza:764` · ADR-62 · sellado `4195f37`, 5/ago/2026 · original **18 FAIL · 95 WARN** · hoy **19 FAIL · 135 WARN**

**NO restaures ninguna.** Editar la cifra de un ADR sellado es decisión de mesa, y
además hay una pregunta previa que no te toca contestar: si `:1274` narra explícitamente
su propia trayectoria (*"se actualizaron en este acto a 18 FAIL · 119 WARN… tras `T21`
subieron a 138… quedan en 19 FAIL · 135 WARN"*), restaurar la primera cifra podría
romper una prosa que ya es correcta. **Abre una fila `ABIERTA`** con la tabla como
evidencia y la pregunta redactada:

> ¿Se restauran las cifras originales de las N narraciones sobreescritas, o se conserva
> el texto actual con el marcador y la tabla del acto como registro de la sobreescritura?

Si tu derivación muestra que alguna de las ocho **nunca** fue sobreescrita —su cifra de
hoy es la que se selló—, dilo: ésa no necesita nada más que el marcador, y saber
cuántas son de cada tipo es parte del entregable.

---

## 4 · COMMIT 4 · Cierre

- **`FP-50` pasa a `FIRMADA`** con el ADR de este acto en `firmada_en` y el PR en
  `ejecutada_en`. Es la fila que este acto gatea; no la dejes a medias.
- **Fila nueva `ABIERTA`** con la pregunta del §3.
- **Revisa `FP-51`** (la regla del recongelado, redactada y sin sellar por
  `ACTO CI-CATEGORIA`). Este acto es su primera prueba real — ver §5. Si cierra sin
  congelar, **anótalo en la fila como evidencia a favor**, sin firmarla: la firma es de mesa.
- **ADR nuevo** en `gobernanza`. **Re-derívalo, no lo teclees:**
  `grep -oE "^\*\*ADR-[0-9]+" canon/gobernanza-v1_15.md | grep -oE "[0-9]+" | sort -n | tail -1`
  (contra `d2fedb0` el máximo es 96, cero huecos). Cuidado con la cascada: sellar un ADR
  sube el conteo y `T15` vigila `(\d+)\s*ADR\b` en **todos** los `canon/*.md` —
  `estado-programa:27`, `:99`/`:101` tendrán que subir con él. **Eso está dentro del
  perímetro**, no es desviación.
- Nota del acto en `forense/notas/`, con el censo del §2 y la tabla del §3.
- Una línea en `forense/hallazgos.md` (append, `merge=union`), sin fila en el tablero.
- Marca este encargo `CONSUMIDO` con su PR.
- **Merge local siempre.** GitHub no honra `merge=union` del lado servidor.
  ⚠️ `canon/estado-programa-v1_10.md:101` se automergea en silencio quedándose con un
  lado entero — es `FP-48` y ya bloqueó cuatro actos. Si tu merge lo toca, revísalo
  cláusula por cláusula.

---

## 5 · 🚫 PROHIBIDO CONGELAR — y esta vez no es una restricción, es el entregable

**No corras `--freeze`. Bajo ninguna circunstancia.**

Verificado en scratch contra `d2fedb0` antes de escribir este encargo — **premisa a
re-derivar, no a creer**:

| | antes | después |
|---|---|---|
| `T16` | 3 FAIL | **`[ ok ]`** |
| suite cruda | 22 FAIL · 135 WARN | **19 FAIL · 135 WARN** |
| rastreadores vivos | 7 | **2** |
| línea base | VERDE | **VERDE**, con 2 entradas que dejan de aparecer |

**El remedio cierra en verde sin recongelar**, porque quitar entradas solo puebla
`resueltos`, que no bloquea. Si tu corrida contradice esta tabla, **la premisa era mía y
estaba mal: párate y repórtalo** — es entregable, no interrupción.

Y si cierra como está previsto, **eso es el falsador de `FP-51` pasando su primera
prueba**: un acto que arregla la causa en vez de apagar el vigía, y termina verde sin
tocar el congelado. Dilo en la nota con esas palabras, porque es la evidencia que mesa
necesita para firmar la regla.

Si en algún momento te encuentras queriendo congelar, el remedio del §1 falló o el
censo del §2 clasificó mal alguna línea. **Para y reporta cuál.**

---

## 6 · Módulo de auditoría — contesta solo lo aplicable

Este artefacto no afirma nada sobre México, así que el módulo de rigor extremo no
aplica (v2.3, alcance). Contesta únicamente:

**¿Cuántos contadores movió el trabajo que produjo este artefacto?**
La respuesta esperada es **cero**: `13 de 27`, `0 de 15`, `11 de 15` y `1 de 2` no se
mueven aquí. **Dilo en una línea al inicio, sin justificarlo.**

Y una segunda, que este acto sí tiene que contestar porque toca registros sellados:
**¿qué afirmación de este artefacto describe el estado del corpus y no fue derivada,
sino escrita a mano?** (A.4/v2.1). El censo del §2 y la tabla del §3 tienen que salir
de comando, con el comando a la vista. Ninguna cifra de este acto se teclea.

---

## 7 · Lo que este acto NO hace

- **No restaura ninguna cifra histórica.** Deriva, tabula, y lo deja en mesa.
- **No toca `_baseline_key`.** La normalización de `_T16_REAL_SUFIJO` (ADR-90) sigue
  siendo necesaria para las 2 citas vivas que quedan, y la colisión de clave que el
  transfer del 18/ago describía **se disuelve sola** al bajar de 7 rastreadores a 2:
  verifica que es así y dilo, o dilo si no.
- **No cierra `FP-47`, `FP-48` ni `FP-51`.** `FP-51` recibe evidencia, no firma.
- **No toca `tools/`, `data/`, `milpa/` ni `.barrido2/`.**
- **No arranca ninguna etapa de `FP-26`.** Ese disparador sigue gateado.

## INDETERMINADO

Derivado por auditoría 2026-09-03 (ACTO MAESTRA37-N9 · AUDITA-ENCARGOS-166). `grep -Fn -- "2026-08-18-T16-HISTORICAS-cerrar-bucle-congelados.md" canon/gobernanza-v1_15.md` cita ADR-97, pero el bloque mezcla lenguaje de ejecución y de encargo pendiente (o el rótulo del ADR es compartido entre varios encargos sin desenlace individual claro) — rastro parcial, no se decide aquí. Para mesa: verificar manualmente contra ADR-97 en canon/gobernanza-v1_15.md.

## CERRADO-POR-HISTORIA

Regla mecánica (b) de la resolución de mesa sobre FP-290 (2026-09-04):
sin hermano de rótulo compartido con desenlace ya sellado (regla a no
aplicó -- ver tabla en forense/notas/2026-09-03-MAESTRA37-N9-auditoria-encargos.md,
enmienda 2026-09-04), este encargo queda cerrado por antigüedad e
inacción declarada, no por evidencia positiva de ejecución o
sustitución. Si aparece evidencia nueva, esta marca se reabre -- no es
`## CONSUMIDO`.
