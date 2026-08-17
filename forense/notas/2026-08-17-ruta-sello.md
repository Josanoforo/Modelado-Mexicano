# ACTO RUTA-SELLO — sella `ADR-89`: taxonomía RUTA-A/RUTA-I/RUTA-C/SIN-RUTA canon, reparto estampado (A.10)

**Acto:** ACTO RUTA-SELLO · **Entorno:** repo-only, NUBE, sin `data/raw`, sin sonda HTTP (no aplica — este acto no toca red ni microdato) · **SHA de redacción del encargo:** `f3873c2` · **SHA real al sellar:** `4c9da5b` · **Depende de:** `ADR-79(f)` (`gobernanza:1179`, firma "sellémosla") · `ADR-87`/A10-ESTAMPA (`instrucciones-proyecto-v2_10.md`, A.10 escrito). Este acto no corre ningún diseño, no adjudica ninguna fila del censo — propaga y estampa una firma de mesa ya dada.

## §0 · ARRANQUE — dos lanzamientos, un gate

**Primer lanzamiento**, base `f3873c2`. Gate del encargo, comando literal:

```
$ git cat-file -e origin/main:instrucciones-proyecto-v2_10.md
fatal: path 'instrucciones-proyecto-v2_10.md' does not exist in 'origin/main'
```

`origin/main` llegaba solo hasta `instrucciones-proyecto-v2_9.md` (verificado: `git ls-tree -r --name-only origin/main | grep instrucciones-proyecto` → v2, v2_4..v2_9, nada más). Sin rama, PR ni encargo de `E-A10` en ningún sitio (`git branch -a`, `mcp__github__list_pull_requests`, `forense/encargos/` — los tres vacíos de "A10"). Conforme al encargo ("PARA y reporta 'gate no cumplido'") y al precedente ya escrito en este repo para un PARO de gate duro sin fase de repliegue (`forense/notas/2026-08-13-sella-mesa.md` §1, *"Segundo PARO, reportado, sin escritura"*): parado y reportado en el chat, **cero archivos tocados**.

**Segundo lanzamiento**, tras confirmación del usuario de que "instrucciones actualizadas y ese PR merged". Gate re-corrido:

```
$ git fetch origin && git rev-parse origin/main
4c9da5b1ba4a5c412b0d4057b70a0a294c9ce119
$ git cat-file -e origin/main:instrucciones-proyecto-v2_10.md && echo PASS
PASS
```

`origin/main` avanzó `f3873c2` → `4c9da5b` (9 commits: `bfae740`…`4c9da5b`, `ACTO A10-ESTAMPA` `#242` + `ACTO T22-DERIVA` + `ACTO E-HIG/HIGIENE-VIVOS` `#243`). Rama local `claude/ruta-sello-taxonomy-rou7xm` (ya en `f3873c2`, sin commits propios) actualizada por `git merge --ff-only origin/main` — limpio, sin conflicto. Retomado desde cero contra `4c9da5b`: ningún número de ADR ni cifra del primer intento se hereda (el primer intento no había escrito ninguno — no hubo nada que heredar, declarado por si acaso).

## §1 · Verificación de existencia de dirección, re-confirmada contra `4c9da5b`

Las cuatro citas del encargo, re-verificadas contra el árbol fresco (no heredadas del primer intento):

| Cita | Verificación | Resultado |
|---|---|---|
| `censo v1_1:45` verbatim | `sed -n '45p' forense/censo-estimabilidad-coeficientes-v1_1.md` | Idéntica, sin cambio entre `f3873c2` y `4c9da5b` (el rango no tocó ese archivo — confirmado por `git diff --stat f3873c2..4c9da5b`, censo ausente de la lista) |
| `gobernanza:1056`≈`ADR-72` | `grep -n "^\*\*ADR-72" canon/gobernanza-v1_15.md` → `974` | Línea distinta a la citada por dirección (984 en vez de 1056 en mi primera lectura, y el propio ADR-72 vive en 974) — el encargo cita la posición aproximada de otra sesión; el contenido (declara "esa taxonomía sigue sin sellarse") se verificó íntegro, sin cambio |
| `gobernanza:984` (contador provisional) | `sed -n '984p'` | Sin cambio: `RUTA-A=3 / RUTA-I=1 / RUTA-C=2 / SIN-RUTA=9` listado bajo "(A) Contadores con denominador o universo provisional" |
| `ADR-79(f)` en `gobernanza:1179`, verbatim "sellémosla." | `sed -n '1179p'` | Sin cambio — ninguno de los 9 commits del rango toca esa línea |
| `FP-13` en `firmas-pendientes.tsv` | `grep "^FP-13"` | Sin cambio, `ABIERTA`, mismas citas |

Ninguna de las cuatro comprobaciones se movió entre `f3873c2` y `4c9da5b`. Sin brecha nueva que declarar.

## §2 · BARRIDO-2 — colisión de perímetro verificada, no solo asumida

```
$ git branch -a | grep -i barrido
  remotes/origin/codex/barrido-2
$ git merge-base origin/main origin/codex/barrido-2
f3873c25d12ec3e26730901dc257788011e5ceea
$ git diff --stat f3873c2 origin/codex/barrido-2
 ... 22 files changed, 6859 insertions(+), 13 deletions(-)
```

`BARRIDO-2` toca `data/**` (censo-explotación, curación-universo, fuera-de-disco) y `tools/curador_registro/**` — exactamente el territorio que el encargo declara prohibido y que este acto no toca en absoluto (confirmado: cero archivos de `data/`/`tools/` en el commit de este acto). Sí toca `canon/gobernanza-v1_15.md` (+24 líneas) y `canon/estado-programa-v1_10.md` — colisión real pero del género ya resuelto por convención (`número de ADR se deriva al sellar contra el main real, nunca se fija`): `codex/barrido-2` no ha fusionado a `origin/main` al momento de escribir este ADR (`únicos: 88` en `origin/main`, sin ningún ADR de `BARRIDO-2` todavía), así que `ADR-89` se deriva limpio contra lo que existe hoy. Si `BARRIDO-2` fusiona primero, este ADR se renumera al retomar — mismo mecanismo que ya vivieron `ADR-84`/`ADR-85` y `ADR-86`/`ADR-87`.

## §3 · T05 — glosario, verificado mecánicamente y no exigido

```
$ sed -n '244,262p' tests/check.py
```

`T05` (`ADR-32.c`) verifica una lista **cerrada** y hardcodeada de constructos del motor (`G1`…`G6`, `familismo_apoyo`, `familismo_obligacion`, `simpatía`, `machismo`, `marianis`, `face`, `trampa social`, `bandwidth`, `transferencia directa`, `turnout buying`, `vote-choice`, `confianza personalizada`, `interruptor formal`, `default es aceptación`) contra `canon/glosario-v*.md`. Ninguno de los cuatro nombres de esta taxonomía (`RUTA-A`, `RUTA-I`, `RUTA-C`, `SIN-RUTA`) está en esa lista, y este acto no añade ni quita ningún constructo de ella. `T05` no exige tocar `canon/glosario-v5_6.md` para este acto — verificado leyendo la función, no asumido.

## §4 · Las cuatro definiciones — fuente exacta, no reescrita

`censo-estimabilidad-coeficientes-v1_1.md:45` remite a v1.0 §1 sin repetirlo (verbatim citado en §1 arriba). El texto fuente:

```
$ sed -n '19,28p' forense/censo-estimabilidad-coeficientes-v1_0.md
```

Líneas 25-28, las cuatro definiciones (RUTA-A/RUTA-I/RUTA-C/SIN-RUTA), citadas íntegras y sin editar en `ADR-89`. Verificado que el propio v1.0 declara, línea 21: *"Búsqueda exhaustiva (`grep -rni`) de RUTA-C, RUTA-I, RUTA-A, SIN-RUTA... cero resultados previos en el repo. Esta taxonomía no existe en canon/ ni en ningún ADR — la introduce este censo... No rige nada hasta que una mesa la selle con ADR"* — la propia génesis del vocabulario, citada en `ADR-89` para que quede claro que hasta hoy (`ADR-89`) esas cuatro clases nunca habían sido canon, en ningún sitio.

## §5 · El reparto — comando, salida cruda, cruce independiente contra el propio censo

Estructura de la tabla verificada antes de escribir el comando (mismo hallazgo que el propio censo v1.1 §7 ya documentó para su primer intento — auto-referencia dentro de la celda de texto de las filas reclasificadas rompe un `grep -oE` de línea completa):

```
$ grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_1.md | awk -F'|' '{print NF, $1}'
11  (× 15 — columnas consistentes en las 15 filas)
$ grep -E '^\| [0-9]+ \|' forense/censo-estimabilidad-coeficientes-v1_1.md | awk -F'|' '{print $2, "->", $9}'
 1  ->  **RUTA-A**
 2  ->  **RUTA-A**
 3  ->  **SIN-RUTA**
 ... (campo 9 = columna Ruta en las 15 filas, verificado uno por uno)
```

Campo 9 confirmado como la columna `Ruta` en las 15 filas. Comando de derivación (aislando el campo, no la línea completa — inmune al defecto de sobre-cuenta que v1.1 §7 ya corrigió):

```
$ awk -F'|' '/^\| [0-9]+ \|/{print $9}' forense/censo-estimabilidad-coeficientes-v1_1.md | grep -oE 'RUTA-[AIC]|SIN-RUTA' | sort | uniq -c
      3 RUTA-A
      5 RUTA-C
      1 RUTA-I
      6 SIN-RUTA
$ awk -F'|' '/^\| [0-9]+ \|/{print $9}' forense/censo-estimabilidad-coeficientes-v1_1.md | grep -oE 'RUTA-[AIC]|SIN-RUTA' | wc -l
15
```

`3 + 5 + 1 + 6 = 15` — sin fila sin clasificar. **Reproduce exacto** el resultado que `censo-estimabilidad-coeficientes-v1_1.md` §7 ya publicó (tras corregir su propio primer intento), por una vía de extracción distinta (campo aislado por `awk`, no `grep -oE` de línea completa) — cruce independiente, no copia. **No se hereda** el reparto de v1.0 (`3/1/2/9`) ni ninguna cifra de memoria: v1.1 reclasificó las filas 12/13/14 de `SIN-RUTA` a `RUTA-C` (`ADR-74`).

## §6 · Estampa de universo (A.10) — los tres elementos, uno por uno

Texto operable de A.10, releído antes de aplicarlo (`instrucciones-proyecto-v2_10.md:366-384`, `git show origin/main:instrucciones-proyecto-v2_10.md`): *"Todo sello, veredicto o cierre declara en la línea donde se sella el universo bajo el que se tomó: el SHA contra el que se derivó, el corpus o los instrumentos examinados, y el denominador cuando exista."*

- **SHA:** `dcc4f6a` — no `4c9da5b` (el `main` de hoy) ni `f3873c2` (el de redacción del encargo). El censo v1_1 declara su propio SHA de derivación en su §8: *"Este v1.1 se derivó contra `origin/main = dcc4f6a`"* — el universo que se sella es el de la TABLA, no el del acto que la sella.
- **Corpus:** la tabla de 15 filas de `censo-estimabilidad-coeficientes-v1_1.md` §5 — explícitamente NO los instrumentos crudos (ENASEM, ENBIARE, etc.) que cada fila cita como evidencia; ese es un universo más amplio que este ADR no recorre ni verifica.
- **Denominador:** 15 (los 15 coeficientes de generador, `milpa/procedencia.yaml:612-639`).

**`VENCIBLE EN ALCANCE` vs. `VENCIDO EN ALCANCE`, la distinción que `ADR-89` hace explícita.** `VENCIDO EN ALCANCE` es el estado con nombre que A.10 define para un sello cuyo universo **ya** creció — no aplica hoy, porque el universo del censo v1_1 no ha crecido. El encargo pide un rótulo prospectivo distinto: `VENCIBLE EN ALCANCE al cierre de BARRIDO-2`. Motivo verificado, no supuesto: `BARRIDO-2` (`codex/barrido-2`, §2 arriba) escribe `data/censo-explotacion-2026-08-17.tsv` y cobertura material sobre el universo de fuentes — territorio adyacente a estimabilidad de coeficientes. Este acto **no verificó** si `BARRIDO-2` efectivamente amplía ese universo (fuera de perímetro) — solo declara que, si lo hace, este snapshot pasa a `VENCIDO EN ALCANCE` por el mecanismo ordinario de A.10 sin necesitar un ADR nuevo para decirlo.

## §7 · Cascada — T15 (conteo de ADR) y T16 (resync de FAIL/WARN)

**T15**, receta corrida en vivo contra `4c9da5b`:

```
$ python3 -c "
import re
from collections import Counter
s = open('canon/gobernanza-v1_15.md').read()
nums = [int(n) for n in re.findall(r'^\*\*ADR-(\d+)', s, re.M)]
print('únicos:', len(set(nums)), '· max:', max(nums), '· huecos:', sorted(set(range(1,max(nums)+1))-set(nums)))
"
únicos: 88 · max: 88 · huecos: []
```

Siguiente ADR: **89**. Sitios de cascada: `gobernanza-v1_15.md:2` · `estado-programa-v1_10.md:27` · `estado-programa-v1_10.md:101` (los tres mismos que `ADR-75`-`ADR-88` ya usaron). `estado-programa-v1_10.md` no está en la lista cerrada del encargo — desborde de perímetro declarado, mismo precedente que `ADR-62`/`ADR-87`, cambio mínimo (un dígito por sitio + la cláusula nueva en la oración histórica de `L0`).

**T16**, descubierto al correr `--baseline` después de escribir el sello (no antes — este efecto no era previsible sin correr la suite):

```
$ python3 tests/check.py --baseline   # antes de tocar nada
20 FAIL · 131 WARN — LÍNEA BASE: VERDE
$ python3 tests/check.py --baseline   # tras FP-13 -> FIRMADA, sin sincronizar aún
27 FAIL · 130 WARN — LÍNEA BASE: ROJO, 4 entradas
```

`FP-13 → FIRMADA` baja `T22 T-FIRMAS` de 19 a 18 WARN (una fila `ABIERTA` menos) — mecánico, esperado, es el propósito del tablero. Eso baja el WARN real de la suite de 131 a 130, lo que desincroniza toda cita `**N FAIL · M WARN**` en negritas que T16 vigila. Enumeradas por comando (replicando la regex exacta de T16, no de memoria):

```
$ python3 -c "
import re, glob
_CAMBIO_FECHADO = re.compile(r'^>\s*\*\*v\d+\.\d+\s*—\s*\d{1,2}/\w{3}\.\*\*')
for p in glob.glob('canon/*.md'):
    for i, l in enumerate(open(p).read().split(chr(10)), 1):
        historico = bool(_CAMBIO_FECHADO.match(l))
        m1 = re.search(r'\*\*(\d+)\s*FAIL\s*·\s*(\d+)\s*WARN\*\*', l)
        if m1 and not historico: print(f'{p}:{i}', m1.group(0))
        m2 = re.search(r'total de WARN de la suite es\s*\*{0,2}(\d+)', l)
        if m2 and not historico: print(f'{p}:{i}', m2.group(0))
"
canon/estado-programa-v1_10.md:129 total de WARN de la suite es 131
canon/estado-programa-v1_10.md:221 **18 FAIL · 131 WARN**
canon/gobernanza-v1_15.md:764 **18 FAIL · 131 WARN**
canon/gobernanza-v1_15.md:856 **18 FAIL · 131 WARN**
canon/gobernanza-v1_15.md:1106 **18 FAIL · 104 WARN**   <- permanente, NO tocada
canon/gobernanza-v1_15.md:1136 **18 FAIL · 104 WARN**   <- permanente, NO tocada
canon/gobernanza-v1_15.md:1274 **18 FAIL · 131 WARN**
canon/gobernanza-v1_15.md:1387 **18 FAIL · 131 WARN**
canon/gobernanza-v1_15.md:1393 **18 FAIL · 131 WARN**
```

Siete sitios `131→130`, resincronizados con el cambio mínimo (solo el dígito, sin reescribir la prosa alrededor). Los dos "permanentes" (`1106`,`1136`, `18 FAIL · 104 WARN`) **no se tocan**: son historia sellada de `ADR-76(f)` (*"Estado derivado en este acto, no copiado"*, el estado de la suite el día que ese ADR selló su propio precedente) — editarlos sería reescribir historia, lo que este archivo nunca hace. Las menciones en texto plano (sin negritas) de "`T22` sigue emitiendo sus 19 WARN" (`gobernanza:1393`,`:1437`) **tampoco se tocan** — el propio `ADR-88` estableció la convención de que solo lo que va en negritas es cita vigilada por T16 ("`sin bold a propósito`", `gobernanza:1439`); lo no-negrita es, por diseño de ese mismo ADR, snapshot histórico no vigilado.

## §8 · El latente expuesto — `_baseline_key` no normaliza el `real_warn` que T16 incrusta en sus mensajes "permanentes"

Tras resincronizar los siete sitios:

```
$ python3 tests/check.py --baseline
20 FAIL · 130 WARN
LÍNEA BASE: ROJO — 1 entradas nuevas
  · T16: canon/gobernanza-v1_15.md: declara 18 FAIL · 104 WARN vigente; la corrida real da 18 FAIL · 130 WARN
  (2 entradas de la línea base ya no aparecen — mejora, no bloquea)
```

Causa raíz, leída en `tests/check.py:1330`:

```python
def _baseline_key(msg):
    msg = re.sub(r":\d+ ", ": ", msg, count=1)
    return _T22_EDAD_VARIABLE.sub("(N días)", msg)
```

`_baseline_key` normaliza (a) el número de línea inicial y (b) la antigüedad variable de `T22` (el arreglo que `ADR-88` acaba de sellar, horas antes). **No normaliza** el sufijo `"...la corrida real da {real_fail} FAIL · {real_warn} WARN"` que `T16` construye para sus mensajes de las líneas `1106`/`1136`. `tests/baseline.json` tenía congelado (por `ADR-88`, mismo día) ese mensaje con `real_warn=131`; al bajar a 130 —por una causa completamente ajena a `T22`/`ADR-88`, el `FP-13` de este acto— el texto del mensaje cambia, `_baseline_key` ya no lo reconoce, y las dos entradas antes-aceptadas (WARN) colapsan en una sola clave nueva (FAIL) porque la normalización de línea las vuelve idénticas entre sí.

Es la misma familia de defecto que `ADR-88` cerró para `T22` ("cualquier cambio de estado externo rompe el freeze aunque el contenido no haya cambiado") — pero sin cerrar, para este segundo punto ciego de T16 sobre sí mismo. **No se corrige en este acto:** `tests/**` está fuera del perímetro de `ACTO RUTA-SELLO`, y recongelar exige ADR de mesa propio, sin condiciones adicionales (`ADR-76(f)`) — mismo criterio que `ADR-87`/`ADR-88` ya aplicaron para no colar mantenimiento de suite dentro de un acto de contenido. Registrado como hallazgo (`forense/hallazgos.md`, 2026-08-17) para que quien sella el próximo ADR de mantenimiento de `T16` lo encuentre sin releer esta nota.

## §9 · `git diff --check`

```
$ git diff --check
(sin salida — limpio, sin errores de espacio en blanco)
```

## §10 · Frase de sello

**La taxonomía RUTA-A/RUTA-I/RUTA-C/SIN-RUTA, censada el 4/ago/2026 y ampliada el 13/ago/2026, deja de ser "etiqueta de censo" y pasa a ser canon.** Firma de mesa `ADR-79(f)`, verbatim: *"sellémosla."* — `ADR-89` la ejecuta: las cuatro definiciones son vocabulario que rige, el reparto `3 RUTA-A / 5 RUTA-C / 1 RUTA-I / 6 SIN-RUTA` queda estampado (A.10) como snapshot del censo v1_1 al SHA `dcc4f6a`, `FP-13` pasa de `ABIERTA` a `FIRMADA`, y el tablero de firmas queda en 25 filas · 18 `ABIERTA` · 7 `FIRMADA`. Ninguna fila individual del censo se reabre. Ningún contador de medición sobre México se mueve. `LÍNEA BASE` queda `ROJO` por una única entrada, declarada arriba (§8), no causada por contenido nuevo sino por un latente de la propia suite que este acto expone y no le corresponde corregir.

Contadores movidos: 0.
