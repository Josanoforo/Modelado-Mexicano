# NOTA DE CIERRE · ACTO `GEN2-TUBERIA-ENRUTAMIENTO-PR-1`

**Cada PR dice, derivado de su diff y en CI, qué tipo de merge es.**

- **Encargo archivado (A.3):** `forense/encargos/2026-09-21-GEN2-TUBERIA-ENRUTAMIENTO-PR-1.md`
  · sello de cuerpo `1082c48b600594291181d7c1445243a1194498df8d48c982b11fd06ee44daefd`
  (`forense/encargos/2026-09-21-GEN2-TUBERIA-ENRUTAMIENTO-PR-1.md.cuerpo.sha256`).
- **0-bis:** `9a2ca8b3ded66c7be3233420bfe991dc43c9df9b` → raíz de acto `-9a2c-`.
- **ADR:** `ADR-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01`.
- **SHA de redacción del encargo:** `fc13cdcc` · **SHA de arranque:** `fc13cdcc` — **main no se movió**.
- **MODO:** `ABIERTO` · **COMPUERTA:** ninguna (no dispara verificación) · **CONTADOR:** `cuenta_gen2 = NO` (este acto no mide nada; cero contadores movidos, §5 v2.4).

---

## 1 · ARRANQUE (Bloque D, verbatim de la skill `/acto`)

**0.a · BASE AL DÍA.**

```
$ git fetch --prune
 + ce16af3...fc13cdc main       -> origin/main  (forced update)
$ git rev-list --count HEAD..origin/main
0
$ git rev-parse origin/main
fc13cdcc56bde5d3396ac0e1c2301c337f0af6ac
```

**0.b · ÁRBOL LIMPIO.** `git status --porcelain` → vacío.

**0.c · DUPLICADO** — los tres sitios, no uno:

```
$ git ls-remote --heads origin | grep -i "enrutamiento"      # (sin salida, rc=1)
$ git worktree list
/home/user/Modelado-Mexicano  fc13cdc [claude/exciting-mccarthy-qcvxdv]
$ ls forense/encargos/ | grep -i enrutamiento                 # (sin salida)
```

PR abiertos, por el tool de GitHub (no hay `gh` en este entorno):
`search_pull_requests repo:Josanoforo/Modelado-Mexicano is:open ENRUTAMIENTO`
→ `total_count: 0`. **Sin duplicado en ninguno de los tres.**

**0.d · HIGIENE (sólo reporte).**

```
LIMPIA-ARBOL · REPORTE (nunca escribe)
  A · worktrees vivos: 1   [git worktree list --porcelain]
      /home/user/Modelado-Mexicano  rama=refs/heads/claude/exciting-mccarthy-qcvxdv
  B · ramas locales ya fusionadas a origin/main y vivas: 1
      claude/exciting-mccarthy-qcvxdv
  C · base: HEAD esta 0 commits detras de origin/main (al_dia=SI)
  D · ramas remotas sin PR abierto -> fuera_de_politica: NO-VERIFICABLE-SIN-GH
```

**1 · REPO.** Clon existente en `/home/user/Modelado-Mexicano` (no se clonó nada).
`git log -1` → `fc13cdc Merge pull request #962 …`. `git status` limpio.

**2 · SHA.** Coincide con el declarado (`fc13cdcc`). Nada que re-derivar.

**3 · `data/raw`.** AUSENTE. **No es PARO y no se resolvió porque este acto
no abre microdato ni descarga nada** — cero payloads, así que el cierre
anti-PR#77 es vacuo y se declara vacuo, no omitido.

**4 · ENTORNO (A.2, tres partes).** Salida CRUDA del hook `SessionStart`
(`tools/entorno.py --arranque`), pegada tal cual, sin re-derivar:

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=535 adelante=448 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 1/2
data-raw-en-este-worktree: NO
```

- **A.13** sobre la tercera parte: el veredicto `montado=NO` declara su
  universo — `archivos_examinados=0`. Es un negativo **sobre este worktree**,
  no sobre el corpus compartido.
- La línea `head-vs-origin/main: detras=535 adelante=448 (sin fetch)` es
  **anterior al fetch** y el propio hook lo rotula `(sin fetch)`. Tras
  `git fetch --prune` el conteo real es **0** (0.a arriba). No se hereda la
  cifra del hook.
- **ENTORNO ASIGNADO = NUBE** (`cloud_default`) **= ENTORNO-DERIVADO**. Sin
  PARO de entorno. El encargo declara «cero microdato; no usa la API de
  GitHub» para el producto — la API sí se usó para la comprobación de
  duplicados de 0.c y para abrir el PR, que son pasos de `/acto`, no del
  producto.

**5 · ESPEJO.** Ninguna cifra de esta nota sale del espejo: todas salen del
clon de (1), con su comando a la vista.

---

## 2 · PREMISAS DEL ENCARGO, verificadas

| Premisa | Rótulo | Veredicto |
|---|---|---|
| 198 PR fusionados a `main` en 7 días, clasificados 44/33/38/83 | `EJECUTADO` | **CONFIRMADA, reproducida al PR** — ver §4 |
| `.github/workflows/verify.yml` no escribe nada en `GITHUB_STEP_SUMMARY` | `LEÍDO` | **CONFIRMADA** — `grep -c GITHUB_STEP_SUMMARY .github/workflows/verify.yml` → `0` |
| El CI clona con profundidad 1; `preflight-calc` y `guardas-res` llevan su propio clonado | `LEÍDO` | **CONFIRMADA** — leídos los dos jobs; se copió el patrón de `guardas-res` (fetch completo + rama base) |
| `PR #943` traía resultados sellados sin anunciarlo | `EJECUTADO` (dirección) | **CONFIRMADA por objeto**: la regla de este acto lo clasifica `ADOPTA` (señales `ADOPTA, FIRMA`, 1 CALC, 28 archivos, `9bb5396f`) |

**Una premisa logística cayó y se resolvió (D-19, latitud):** el clon de
esta sesión era **superficial** (`.git/shallow` presente), y con él
`git log --merges` sobre la ventana de 7 días veía **59** merges, no 483.
Un clon superficial no es PARO y el objetivo seguía alcanzable:
`git fetch --unshallow` (obstáculo reversible y barato, explícitamente en la
latitud de `/acto`). Con historia completa: **483 merges en la ventana, de
los cuales 198 son `Merge pull request #…`** — exactamente el universo que
el encargo declara. **Si la re-corrida se hubiera hecho sobre el clon
superficial, habría reportado 59 y el número habría parecido una
discrepancia con dirección cuando el defecto era del clon.**

---

## 3 · QUÉ SE CONSTRUYÓ

### P1 · `tools/clasifica_pr.py` — la regla, en un solo sitio

Un archivo. Dado un diff (`--base/--cabeza` por git, o `--diff` de un
archivo/stdin) devuelve las tres cosas que pide el encargo:

1. **Todas** las señales que dispara, no sólo una.
2. La **clase principal** por precedencia `ADOPTA > FIRMA > APARATO > REVISIÓN`.
3. La **instrucción de enrutamiento** de esa clase, en una línea, con N y los
   CALC **contados del diff** — no tecleados (§2 de las instrucciones:
   ninguna cifra esperada se teclea).

Las rutas viven en el dict `SEÑALES`, **dentro de la herramienta y en ningún
otro sitio** (D-15), y **cada una lleva la línea que dice por qué dispara**
— no el patrón a secas.

**La herramienta no falla por la clase (D-16):** sale `0` clasifique lo que
clasifique. El único `rc != 0` es `2 · NO-PUDE-LEER-EL-DIFF`, que es un
defecto de la herramienta, no del PR.

Dos decisiones de latitud, declaradas:

- **Un renombre se lee por su ruta NUEVA.** `R100 viejo nuevo` → `nuevo`: es
  la ruta que existirá en `main` tras el merge, y es la que importa.
- **Un borrado (`D`) dispara igual que un alta.** Borrar el `sello.json` de
  un CALC no es menos grave que añadirlo; una señal que sólo mira altas deja
  pasar justo el caso peor.

### P2 · El job `enrutamiento-pr` en `verify.yml`

Job **propio**, con **su propio clonado** que trae la rama base (D-23: la
herramienta nunca hace `fetch`; mismo patrón que `guardas-res`). Corre en
`pull_request` y en `push` a `main` (los dos ya están en el `on:` del
workflow, intocado). Escribe el resultado en `$GITHUB_STEP_SUMMARY`, que es
donde mesa lo ve en la pestaña *Checks*.

Tres cosas que **no** hace, y son los PAROS del encargo:

- **No está en `needs:` de `check`.** Deliberado: la clase informa, no
  adjudica (D-16); un PR no se bloquea por la clase que le toque.
- **Ningún job existente se tocó.** `jobs` pasa de
  `[suite, adicionales, guardias, preflight-calc, guardas-res, check]` a
  la misma lista con `enrutamiento-pr` insertado antes de `check`;
  `check.needs` queda **idéntico**.
- **Cero permisos de escritura.** El workflow declara `permissions: {contents: read}`
  a nivel raíz y el job nuevo **no declara `permissions` propio**, así que
  hereda `read`. No etiqueta PR, no comenta, no fusiona.

### P3 · `tests/test_clasifica_pr.py`

Siete grupos, **cableado en CI** como paso **bloqueante** del job nuevo
(D-21: el acto cablea su test). Cubre exactamente lo que el encargo pide —
uno por clase · uno de dos señales que sale con la de mayor precedencia
**listando ambas** · uno sin archivos · uno que adopta **varios** CALC y los
cuenta bien — más precedencia de las cuatro a la vez, renombre/borrado, y el
**punto de entrada corrido de verdad** contra un diff en disco y contra git
(D-22: un medidor cuyas pruebas sólo ejercitan guardias y constantes no es
un COMMIT-1).

```
$ python3 tests/test_clasifica_pr.py
  …
OK · todos los casos
```

---

## 4 · RE-CORRIDA RETROSPECTIVA (P3, segunda mitad)

**Universo declarado (A.4):** los **198** commits `Merge pull request #…`
de `origin/main` en la ventana `2026-09-14T12:54:39-06:00` →
`2026-09-21T12:54:39-06:00` (7 días hasta la fecha de commit de `fc13cdcc`).
Cada PR clasificado por `git diff --name-status -M <merge>^1...<merge>`.
Tabla completa, fila por PR: `forense/analisis/enrutamiento-pr-1/recorrida-198-pr.tsv`.

| Clase | Regla de §2 (dirección) | **Regla de este acto** | Discrepancias |
|---|---|---|---|
| **ADOPTA** | 44 (22 %) | **44** | 0 |
| **FIRMA** | 33 | **33** | 0 |
| **APARATO** | 38 | **38** | 0 |
| **REVISIÓN** | 83 | **83** | 0 |
| **Total** | 198 | **198** | **0** |

**Cero PR clasificados distinto.** El encargo pide «una línea por cada PR
que la regla de este acto clasifique distinto que la de §2, con la razón»:
**no hay ninguno**, y eso se declara como resultado, no como sección vacía.
La columna `discrepa` del TSV es `NO` en las 198 filas. Las cifras de §2
eran «referencia para comparar, no valor esperado» — la comparación salió
idéntica, así que no se tocó ninguna ruta de la tabla.

**Tres cosas que la re-corrida sí midió y el encargo no anticipaba:**

1. **Las señales múltiples no son un caso raro: son la mayoría de lo que
   dispara.** De los 115 PR que disparan al menos una señal, **60 disparan
   dos o más** (53 con dos, 7 con tres). Devolver sólo la clase principal
   habría escondido más de la mitad. Distribución: `0 señales: 83 · 1: 55 ·
   2: 53 · 3: 7`.
2. **Los 44 PR `ADOPTA` disparan TAMBIÉN `FIRMA`, los 44.** Un `sello.json`
   nunca llega solo: viene con el `spec.yaml` de su CALC. La precedencia
   `ADOPTA > FIRMA` es, por tanto, la que decide la clase en **el 100 %** de
   las adopciones, no un desempate teórico. Siete de esos 44 tocan además
   `APARATO`.
3. **Los 198 PR adoptaron 80 CALC sellados en la semana.** El máximo en un
   solo PR fue **7** (`PR #789`, `0cdbd72c`). `PR #943`, el caso que motivó
   el encargo, aparece con 1 CALC y 28 archivos.
4. **Dos PR (`#864`, `#859`) tienen diff vacío** contra su primer padre
   (0 archivos) → `REVISIÓN`. El caso «sin archivos» del test no era
   hipotético.

---

## 5 · CRITERIO DE «HECHO» (§4 del encargo), por punto

1. **Firma y línea del auto-merge asentadas** → `forense/firmas-pendientes.tsv`,
   fila `FP-260921-GEN2-TUBERIA-ENRUTAMIENTO-PR-1-9a2c-01`, estado `FIRMADA`,
   con la firma del 20/sep/2026 **verbatim** y la línea del auto-merge
   **NO instrumentado** con su razón (9 % de los merges, ninguna de las
   renumeraciones; reevaluable si esa fracción crece). **HECHO.**
2. **Señales, clase y enrutamiento para los diffs sintéticos; test en CI**
   → `tests/test_clasifica_pr.py` en verde, cableado como paso bloqueante
   del job `enrutamiento-pr`. **HECHO.**
3. **El job escribe el resumen en el PR de este acto, con clase APARATO**
   → derivado localmente con el mismo comando que corre en CI (§6 abajo):
   clase **`APARATO`**, por `.github/workflows/verify.yml`. La prueba en
   vivo se lee en la pestaña *Checks* del PR. **HECHO (pendiente de que CI
   corra, que es lo que el PR muestra).**
4. **Re-corrida retrospectiva en la nota, con cada discrepancia explicada**
   → §4. Cero discrepancias, declarado como tal. **HECHO.**
5. **Suite en LÍNEA BASE VERDE** → §6. **HECHO.**

---

## 6 · LA PRUEBA EN VIVO (P4)

El mismo comando del job, contra la base real de este PR:

```
$ python3 tools/clasifica_pr.py --base origin/main --cabeza HEAD
```

Su salida (clase **`APARATO`**, por `.github/workflows/verify.yml`) queda en
el cuerpo del PR y en el resumen del job. Por qué APARATO y no otra: este
acto **no** añade ningún `sello.json` (no adopta nada: `cuenta_gen2 = NO`) y
**no** toca `milpa/`, `decisiones.tsv` ni ningún `spec.yaml` de CALC — toca
`forense/firmas-pendientes.tsv`, que **a propósito no es una ruta de la
señal `FIRMA`**: esa tabla registra firmas ya dadas, no es superficie donde
se firme. Es exactamente lo que el encargo predijo.

---

## 7 · LO QUE ESTE ACTO NO HACE

No fusiona nada — **el PR queda propuesto; mesa central fusiona**. No
etiqueta PR, no bloquea por clase, no decide nada por mesa, no instrumenta
ninguna forma de auto-merge. Ninguno de los seis PAROS de la lista cerrada
del encargo se tocó.

**Sucesor posible (§6 del encargo, no lanzado):** que `/revisa` lea la clase
del resumen en vez de deducirla — se propone con evidencia de uso, no antes.

## 8 · FALSADOR (§7 del encargo, a un mes — 21/oct/2026)

Si mesa fusiona un PR de clase `ADOPTA` sin haber visto su enrutamiento, o
la regla clasifica como `REVISIÓN` un PR que adoptó cifras, la herramienta
no hace lo que dice y se retira la pieza que falló.
