# ENCARGO CU · Cascada vigilada + merge de append-only

**Resumen.** Dos defectos independientes, ambos ya declarados por el propio canon como deuda abierta. Defecto A: cinco líneas VIGENTES de `canon/` declaraban "12 de 27" corridas del Hito D mientras el bloque append-only real ya tenía 13 (ADR-63, `R1.3`→`E`, 5/ago/2026) — dos de ellas (`gobernanza:358,810`) porque el perímetro acotado de ADR-63 las dejó fuera a propósito (declarado en `gobernanza:786`); las otras tres (`modelo-decision:64,636,821`) porque **ninguna cascada anterior las había nombrado nunca** como deuda — hallazgo propio de este acto, no debt heredada. Corregidas las cinco con cascada completa, marcadas ocho líneas (las cinco corregidas + tres que ya estaban correctas) con la convención `<!-- T20:HITO-D pob=reglas -->`, y escrito `T20` en `tests/check.py` para que la próxima cascada acotada no vuelva a dejar un sitio invisible. Defecto B: `forense/hallazgos.md`/`bitacora.md` entran a `merge=union` en `.gitattributes`, verificado empíricamente en ramas locales desechables (no empujadas). `hitoD-preregistro-v2_0.md` queda fuera a propósito. No se aplicó `--freeze`. No se produjo ninguna estimación. `tests/check.py --baseline`: VERDE antes y después, `18 FAIL · 95 WARN` en ambos casos, idéntico.

---

## 0 · ARRANQUE (Bloque D)

1. **REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó ninguno nuevo). Al abrir: rama `claude/cascada-vigilada-append-only-zw2rq5` ya creada, `git log -1` = `4fe6551 Merge pull request #123 from Josanoforo/sesion/c06b-conf06-encuci`, `git status` limpio.
2. **SHA.** El encargo declara `b93ffc6` (PR #120). `git fetch origin main` real: `origin/main` = `08b8b6c` (PR #121, "g3-horizonte" — el acto paralelo nombrado en el encargo, ya fusionado para cuando arrancó este acto). `git merge-base --is-ancestor HEAD origin/main` → sí: mi rama no tenía commits propios, era puro ancestro de `origin/main`. Fast-forward limpio (`git merge --ff-only origin/main`, `4fe6551..08b8b6c`). El único cambio que trajo: la línea de `forense/hallazgos.md` y la nota propias de g3-horizonte — exactamente el traslape que el encargo predijo, nada en `canon/`, `README.md` ni `tests/check.py`. `sesion/p-lapop-microdato` no aparece como PR abierto en este momento (`mcp__github__list_pull_requests`, state=open, repo vacío) — no bloquea nada, se queda como riesgo de traslape teórico sobre `forense/hallazgos.md`, sin evidencia de colisión inminente.
3. **`data/raw`.** Ausente (clon fresco, gitignorada). El propio encargo declara que este acto no toca microdato — no se creó ni se enlazó, para no producir ruido sin propósito.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` — coincide con lo esperado. Sin sonda `curl`, como indica el encargo (solo `git`).
5. **ESPEJO.** Buscado en disco fuera del clon (`find / -maxdepth 4 -iname "*modelado*"`); no se encontró ningún espejo del proyecto, solo directorios de caché/metadata de la propia CLI. Toda cifra de este documento sale del clon de (1), con comando a la vista.

---

## 1 · Tarea 1 · Inventario de afirmaciones de conteo de Hito D

Comando: `grep -n "[0-9]\+ de 27" README.md canon/*.md` (más `canon/glosario-v5_6.md`, `canon/integrador-psicologia-mexicano.md`, `canon/protocolo-sesion-v1_0.md` — sin resultados en los tres, no aparecen en la tabla). 25 ocurrencias.

Valor derivado (comando exacto, reproducible):

```
$ python3 -c "
import sys; sys.path.insert(0, 'tests'); import check
h = check.newest('forense/hitoD-preregistro-v*.md')
bloque = check._bloque_veredictos(check.read(h))
fichas = {}
for l in bloque.split(chr(10)):
    m = check._VEREDICTO_CANONICO.search(l)
    if m: fichas[m.group(1)] = m.group(2)
print(len(fichas), dict(__import__('collections').Counter(fichas.values())))
"
13 {'D': 7, 'B': 2, 'A': 2, 'E': 2}
```

**Dos denominadores que conviven, verificados por separado:** el bloque tiene **13 reglas distintas** con veredicto (lo que T18/T19c comparan — `R4.3` se archiva en dos líneas, "mitad A" y "mitad B", y el diccionario `fichas` colapsa ambas bajo la misma llave `R4.3`, contando 1) pero **14 líneas** matchean `_VEREDICTO_CANONICO` dentro del bloque (verificado imprimiendo cada línea con su número: `hitoD-preregistro-v2_0.md:1058-1071`, dos de ellas — 1064 y 1065 — son ambas `R4.3`). Cada sitio VIGENTE de la tabla que sigue declara "reglas" (13), no "líneas" (14); ninguno usa el denominador de líneas, así que no hay un defecto adicional de "sitio que no dice cuál cuenta" que reportar aquí.

**Prueba de la receta contra la trampa conocida (v2.3):** recortar el bloque con `.index("## Registro de veredictos archivados")` en vez del regex anclado `^## Registro de veredictos archivados.*$` que usa `_bloque_veredictos`. En este archivo, `.index()` encuentra primero una mención en prosa (una frase del propio archivo que *cita* el nombre de la sección al explicar por qué el bloque es append-only, antes de la cabecera real) — un corte más temprano y más amplio que el anclado. Probado explícitamente: el conjunto de fichas resultante es **idéntico** (13, mismas llaves) — en el texto actual, entre esa mención temprana y la cabecera real no hay ninguna línea con forma canónica de veredicto, así que la trampa no infla el número *hoy*. Se usó, de todos modos, el método anclado (`_bloque_veredictos`), no el ingenuo — el hecho de que no difieran esta vez no es garantía de que no diferirán la próxima.

### Tabla completa

| # | archivo:línea | clasificación | declarado | derivado | coincide |
|---|---|---|---|---|---|
| 1 | `README.md:36` | VIGENTE | 13 | 13 | SÍ (ya con receta propia; se añade marca T20) |
| 2 | `estado-programa:50` | HISTÓRICA (`_CAMBIO_FECHADO`, `> **v1.8 — 29/jul.**`; además población distinta — cobertura de fichas, no corridas) | — | — | N/A |
| 3 | `estado-programa:95` | VIGENTE (L5) | 13 | 13 | SÍ |
| 4 | `estado-programa:99` | HISTÓRICA (transición con flecha "12 de 27 → 13 de 27" dentro de la narración de ADR-63, en la cadena L0 de conteo de ADR; no matchea `_CAMBIO_FECHADO` mecánicamente pero mismo criterio de tiempo verbal — narra un cambio pasado) | — | — | N/A |
| 5 | `estado-programa:115` | DENOMINADOR/OTRA POBLACIÓN ("27 de 27" = cobertura de fichas del pre-registro, territorio de T17, no corridas archivadas) | — | — | N/A |
| 6 | `estado-programa:122` | VIGENTE, forma COMPLEMENTO ("14 de 27 sin corrida") | 14 | 14 (27−13) | SÍ — **no se marca** (ver límite declarado de T20) |
| 7 | `estado-programa:196` | VIGENTE (ya vigilada por T18) | 13 | 13 | SÍ (se añade marca T20 también) |
| 8 | `gobernanza:13` | HISTÓRICA (narración corrida ADR-44…63, incluye "12 de 27 → 13 de 27" al describir ADR-63) | — | — | N/A |
| 9 | `gobernanza:355` | EJEMPLO ILUSTRATIVO DE FORMA — `"2 de 27 corridas (`D`, `B`)", nunca solo "2 de 27"` ilustra la regla de que la letra viaja con el conteo; no es una afirmación de estado, es la explicación de una convención | — | — | N/A |
| 10 | `gobernanza:358` | **VIGENTE** ("Hoy: …") | 12 | 13 | **NO** → corregido |
| 11 | `gobernanza:577` | HISTÓRICA (ADR-55 sellado, "3 de 27 → 4 de 27") | — | — | N/A |
| 12 | `gobernanza:589` | HISTÓRICA (registro de cascada ya ejecutada, cifras viejas por diseño) | — | — | N/A |
| 13 | `gobernanza:597` | HISTÓRICA (ADR-56 sellado, "4 de 27 → 8 de 27") | — | — | N/A |
| 14 | `gobernanza:609` | HISTÓRICA (registro de cascada ya ejecutada) | — | — | N/A |
| 15 | `gobernanza:647` | HISTÓRICA (nota meta-narrativa: documenta una deuda que ADR-60 ya cerró) | — | — | N/A |
| 16 | `gobernanza:736` | HISTÓRICA (snapshot fechado de ADR-61: "12 de 27 Hito D... Ninguno [se mueve]") | — | — | N/A |
| 17 | `gobernanza:786` | HISTÓRICA (ADR-63 sellado; declara la deuda de `:358`/`:810` que este acto cierra) | — | — | N/A |
| 18 | `gobernanza:810` | **VIGENTE** (tabla de pendientes) | 12 (+15 compl., +37 de 49) | 13 (+14, +36) | **NO** → corregido (las tres cifras de la línea) |
| 19 | `gobernanza:857` | HISTÓRICA (tabla de enmiendas, entrada ADR-56) | — | — | N/A |
| 20 | `gobernanza:858` | HISTÓRICA (tabla de enmiendas, entrada ADR-55) | — | — | N/A |
| 21 | `modelo-decision:21` | HISTÓRICA (`_CAMBIO_FECHADO`, `> **v3.4 — 30/jul/2026**`) | — | — | N/A |
| 22 | `modelo-decision:64` | **VIGENTE** | 12 | 13 | **NO** → corregido |
| 23 | `modelo-decision:636` | **VIGENTE** | 12 | 13 | **NO** → corregido |
| 24 | `modelo-decision:637` | CITA DEPENDIENTE de `:636` ("no cuenta en el '12 de 27' de arriba") — no es una afirmación propia, es una referencia cruzada a la línea anterior | 12 (cita) | — | corregida junto con `:636`, sin marca propia |
| 25 | `modelo-decision:821` | **VIGENTE** (tabla "VERIFICAS ASÍ") | 12 | 13 | **NO** → corregido |

**9 VIGENTE, 5 desincronizadas — más del "al menos dos" que el encargo anticipaba.** `gobernanza:358,810` ya estaban nombradas como deuda por el propio ADR-63 (`gobernanza:786`). `modelo-decision:64,636,821` **no lo estaban** — ninguna nota de cascada anterior (`gobernanza:647`, `:786`) las menciona; es un hallazgo propio de este acto, declarado así en la cola fechada de cada corrección. La premisa del encargo se sostiene, con más fuerza de la que el encargo mismo afirmaba.

---

## 2 · Tarea 2 · Marcado, corrección y `T20`

### (a) Convención de marcado

Comentario HTML `<!-- T20:HITO-D pob=reglas -->`, en cualquier punto de la misma línea física que la cifra. Cumple las tres condiciones del encargo: invisible al renderizar, declara la población (Hito D, reglas — no líneas, ver §1), y es un token literal (`T20:HITO-D`) que no puede confundirse con ninguna receta de comentario que `README.md` ya traía. No requiere adyacencia estricta con la cifra: `T20` toma la **primera** coincidencia de `(\d+)\s*de\s*27` en la línea marcada, y en las ocho líneas marcadas la afirmación vigente siempre antecede a cualquier mención histórica de transición que venga después en la misma línea (verificado línea por línea antes de escribir el test, no asumido).

**8 sitios marcados:** `README:36`, `estado-programa:95,196`, `gobernanza:358,810`, `modelo-decision:64,636,821`. Incluye los tres que ya estaban correctos (`README:36`, `estado:95,196`) — dos de ellos ya vigilados por `T19c`/`T18` respectivamente. Redundancia observada y deliberada, no un descuido: la "cascada vigilada" debía cubrir el universo declarado, no detenerse justo donde ya había un test angosto. **No se marcó `estado-programa:122`** — declara la cifra en forma complemento ("14 de 27 sin corrida"), y `T20` compara directo contra el valor derivado sin restar de 27; marcarla habría producido un FAIL falso. Queda sin marcar a propósito, declarado aquí — no un sitio que T20 "no vio", uno que se decidió no exponerle.

### (b) Correcciones (cascada completa, no acotada)

Las cinco líneas VIGENTE desincronizadas se corrigieron a 13, con `R1.3`→`E` añadida a cada enumeración y una nueva cola fechada *(Corregido 5/ago/2026, ADR-63, Encargo CU — …)* que no borra ni edita las colas anteriores, solo se añade. `gobernanza:810` además corrige sus dos cifras derivadas de la misma (15→14 sin corrida, 37→36 de 49); `modelo-decision:637` (cita dependiente) se actualiza de "12 de 27" a "13 de 27" junto con `:636`, sin marca propia por no ser una afirmación independiente.

### (c) `T20` en `tests/check.py`

Último test declarado antes de este acto: `T19c` (verificado leyendo `main()`, no asumido de la numeración del encargo). `T20` es el siguiente libre. Recorre `README.md` + `canon/*.md`, encuentra líneas con `T20:HITO-D`, deriva el valor real con `_bloque_veredictos` + `_VEREDICTO_CANONICO` (mismo parser que T18/T19c) y falla si el declarado difiere. Cabecera del test declara explícitamente sus dos límites: (1) solo vigila sitios marcados — un contador nuevo sin marcar sigue invisible; (2) no entiende forma complemento — por eso `estado:122` queda fuera. No duplica ni borra T18/T19c; anota la redundancia observada con ambos (mismo criterio del encargo: "si tu T20 haría redundante a alguno, no lo borres").

**Sanity check de que T20 realmente vigila (no pasa en verde por vacío):** se corrompió temporalmente `README.md:36` (13→14), se corrió la suite (`T20` cae con mensaje preciso citando archivo:línea, declarado, derivado y la fuente), se revirtió de inmediato. Diff confirmado limpio después.

### (d) Línea base

```
$ git stash push -u -m "cascada-vigilada-wip"      # revierte todo el WIP para medir el ANTES real
$ python3 tests/check.py --baseline
  18 FAIL · 95 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe...)
$ git stash pop                                     # restaura el WIP
$ python3 tests/check.py --baseline
  18 FAIL · 95 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe...)
```

Antes y después: idéntico, `18 FAIL · 95 WARN`, VERDE. Ningún `--freeze`. `T20` sale verde porque las cinco líneas ya se corrigieron en (b), no porque se haya congelado nada rojo.

---

## 3 · Tarea 3 · `merge=union`

### (a) Censo de append-only

Además de `hallazgos.md`/`bitacora.md`/`hitoD-preregistro-v2_0.md`, son append-only por declaración propia del repo: todo `corpus/reports/`, todo `corpus/forense/`, y dentro de `forense/` — que es append-only como política de directorio completo (`README.md:25`, `gobernanza:422`) — los archivos individuales `hitoC-prueba-generadores.md`, `censo-integridad-v1_0.md` y `censo-integridad-v1_1.md`, `barrido-propagacion-forense-v1_0.md`, `hitoE-campana-medicion-v2_0.md`, y las fichas `hitoD-R*-veredicto-v1_0.md`.

Verificado por qué **ninguno de estos entra a `union` en este acto**, con evidencia, no solo declaración:

```
$ for f in forense/hallazgos.md forense/bitacora.md forense/hitoD-preregistro-v2_0.md \
           forense/hitoC-prueba-generadores.md forense/censo-integridad-v1_0.md \
           forense/barrido-propagacion-forense-v1_0.md forense/hitoE-campana-medicion-v2_0.md; do
  echo "$f: $(git log --oneline --all -- "$f" | wc -l) commits"
done
forense/hallazgos.md: 73 commits
forense/bitacora.md: 6 commits
forense/hitoD-preregistro-v2_0.md: 13 commits
forense/hitoC-prueba-generadores.md: 1 commit
forense/censo-integridad-v1_0.md: 1 commit
forense/barrido-propagacion-forense-v1_0.md: 1 commit
forense/hitoE-campana-medicion-v2_0.md: 8 commits
```

`hitoC-prueba-generadores`, `censo-integridad`, `barrido-propagacion-forense`: un commit cada uno, nunca tocados en concurrencia — no hay problema que `union` resuelva. `hitoD-preregistro`: excluido a propósito por el motivo que el encargo ya da (T18/T19c/T20 cuentan su bloque designado; `union` duplicaría en silencio el contador del programa entero) — el conteo de 13 commits confirma que sí se toca seguido, lo que hace la exclusión deliberada, no un descuido.

**Hallazgo no anticipado por el encargo: `hitoE-campana-medicion-v2_0.md` tiene historia real de colisión** (`git log --grep` sobre el repo completo devuelve `8a2fd46 Merge origin/main (PR #79): resuelve conflicto append-only en hitoE`) y 8 commits — un perfil de concurrencia parecido al de `bitacora.md`. **No se añade a `union` en este acto**: (1) el encargo cierra la lista de entrada con "Entran: X y Y", sin nombrar este archivo; (2) estructuralmente es distinto — no es un log plano de una línea por entrada, sino adendas fechadas insertadas en subsecciones numeradas (`§12`, `§13`, `§14.3`…), y no está verificado que `union` se comporte bien cuando el contenido nuevo no siempre llega al final del archivo. Se reporta aquí para que mesa lo evalúe en un acto separado, no se decide unilateralmente.

`corpus/reports/`/`corpus/forense/` no tienen este problema en absoluto: cada entrada nueva es un **archivo nuevo**, no una edición del mismo archivo — sin edición compartida no hay conflicto que un merge driver deba resolver.

### (b) Condición de salto de línea

```
$ tail -c1 forense/hallazgos.md | od -c
0000000  \n
$ tail -c1 forense/bitacora.md | od -c
0000000  \n
```

Ambos terminan en salto de línea. Confirmado, no se necesitó corregir nada.

### (c) Verificación empírica (ramas locales desechables, `test/union-*`, ninguna empujada — worktrees en `/tmp/.../scratchpad/`, todas borradas al final)

**Caso limpio.** Rama base `test/union-base` (desde `origin/main`) con `.gitattributes` de prueba (`forense/hallazgos.md merge=union`, `forense/bitacora.md merge=union`) committeado. Dos ramas hijas, cada una añade una entrada distinta al final de `hallazgos.md` (con salto de línea correcto):

```
$ git merge test/union-b --no-edit -q      # sobre test/union-a
Auto-merging forense/hallazgos.md
$ git status --short                        # (vacío -- cero conflictos)
$ grep -c "PRUEBA-A\|PRUEBA-B" forense/hallazgos.md
2                                            # ambas presentes, ninguna duplicada
$ diff <(git show test/union-base:forense/hallazgos.md) <(grep -v "PRUEBA-A\|PRUEBA-B" forense/hallazgos.md)
                                              # (vacío -- resto del archivo intacto)
```

Cero conflictos, ambas entradas presentes, ninguna duplicada, resto intacto. Exactamente lo que el encargo predice.

**Caso feo, en dos variantes — la primera fue un error propio, corregido antes de confiar en el resultado.** Primer intento: quité el salto final de `hallazgos.md` y en cada rama usé `printf '\n- entrada...'` (con salto **inicial**) para separar — eso, sin querer, repara el archivo de forma idéntica en ambas ramas antes de añadir contenido distinto, y el merge sale limpio sin reproducir nada. Es un resultado real pero no es el caso que el encargo describe, así que no basta con reportarlo: hay que repetir sin ese salto inicial para que ambas ramas de verdad editen la misma línea física, como la receta manual advierte.

Segundo intento, fiel a la descripción del encargo — `printf -- '- entrada...\n' >> archivo` **sin** salto separador, sobre una base sin salto final, en dos ramas distintas:

```
$ git merge test/union-d2 --no-edit -q      # sobre test/union-d1
Auto-merging forense/hallazgos.md
$ git status --short                         # (vacío -- cero conflictos, exit 0)
$ tail -3 forense/hallazgos.md
... ACTO S-IDG3: ... Contadores movidos: 0.- **PRUEBA-D1** · pegada sin separador, rama D1.
... ACTO S-IDG3: ... Contadores movidos: 0.- **PRUEBA-D2** · pegada sin separador, rama D2, distinta de D1.
```

**El párrafo entero de la entrada S-IDG3 (la última línea compartida antes del corte) aparece dos veces completas**, una pegada a cada entrada de prueba — sin ningún marcador de conflicto, `git merge` reporta éxito (`Auto-merging`, exit 0). Confirma exactamente lo que el encargo predice, y muestra por qué (b) importa: la garantía de "cero conflictos, sin duplicados" que se verificó en el caso limpio depende por completo de que el archivo nunca deje de terminar en salto de línea. Mientras esa invariante se sostenga (verificado hoy, (b) arriba), el riesgo es teórico; si algún acto futuro la rompe, el síntoma es silencioso — sale verde, sin conflicto, con una entrada entera duplicada.

Limpieza: `git worktree remove --force` × 8, `git worktree prune`, `git branch -D` × 8 (`test/union-base/-a/-b/-nonl/-c1/-c2/-d1/-d2`). Verificado `git worktree list`/`git branch` sin residuos, y `git status`/`git branch --show-current` de la rama real sin tocar.

### (d) Lo que este encargo no sabe

No verificado, y no se afirma en ninguna dirección: si el botón "Merge pull request" de GitHub aplica `merge=union` del lado servidor. `union` es un driver interno de git (no personalizado — no requiere entrada en `.git/config`), pero eso no dice nada sobre la maquinaria de merge del servidor de GitHub. La ruta garantizada es el merge local (`git merge`, con `.gitattributes` presente en el árbol de ambas ramas). La primera colisión real en `hallazgos.md` después de este PR lo confirma o lo desmiente sin necesidad de probar nada a propósito.

### (e) Ironía operativa

Este PR probablemente conflictúe a mano contra alguno de los actos vivos en paralelo, porque el `.gitattributes` nuevo no gobierna el merge que lo introduce — ver §4 más abajo para el resultado real.

---

## 4 · Qué no decide este acto

Si esto lleva ADR: de mesa. Este acto puede razonablemente ir sin ADR propio (precedente: T19a/b/c se añadieron sin ADR), citando el requisito de salida abierto de ADR-45 (`gobernanza:362`) y el ADR que originó cada veredicto que faltaba propagarse (ADR-63). Si `I-07` se declara cerrada: también de mesa — este acto reporta que el instrumento (`T20`) existe y cubre las afirmaciones DIRECTAS marcadas; los sitios sin marca (`estado:122`, forma complemento) y cualquier sitio VIGENTE futuro sin marcar siguen fuera, declarado, no oculto.

---

## 5 · Perímetro final tocado

`.gitattributes` · `tests/check.py` (T20) · `README.md` (1 marca) · `canon/gobernanza-v1_15.md` (2 correcciones+marcas) · `canon/modelo-decision-v4_0.md` (3 correcciones+marcas, 1 cita dependiente) · `canon/estado-programa-v1_10.md` (2 marcas, sin corrección) · esta nota · una línea de cierre en `forense/hallazgos.md`. Coincide exactamente con el perímetro declarado por el encargo. No se tocó `forense/notas/` de los actos paralelos, ni la ficha `ID-G3`, ni `milpa/`, ni `forense/hitoD-preregistro-v2_0.md`.
