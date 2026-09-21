# NOTA DE CIERRE · `ACTO GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2`

`ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01` · 21/sep/2026 · **NUBE**
(`cloud_default`) · Opus 5 · **MODO ABIERTO** · **COMPUERTA: ninguna** ·
**CONTADOR: `cuenta_gen2 = NO`** · cero microdato · encargo archivado en
`forense/encargos/2026-09-21-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2.md`
(`sha256` del cuerpo `9af66c7b…febf`, sellado en el 0-bis `8e53c0e`).

---

## 0 · ARRANQUE (A.2, tres partes, salida cruda del hook)

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

El encargo declara **ENTORNO: NUBE** y el derivado es **NUBE**: coinciden, no
hay PARO de entorno. `data/raw` ausente **no es PARO** y aquí ni siquiera se
enlaza: este acto no abre microdato (A.13 — `archivos_examinados=0`, y por eso
ningún veredicto de esta nota es un negativo sobre el corpus).

**Base al día** (tras `git fetch --prune`, que el hook no había corrido — las
cifras `detras=535 adelante=448` son de antes del fetch y no describen el árbol):

```
git rev-list --count HEAD..origin/main   -> 0
git rev-list --count origin/main..HEAD   -> 0
git status --porcelain | wc -l           -> 0
```

`HEAD` = `origin/main` = **`fc13cdc`**, que es exactamente el SHA que el encargo
declara (`fc13cdcc`, merge de `#962`). No hubo que refrescar ni re-derivar.

**Duplicado (0.c, los tres sitios):** `git ls-remote --heads origin | grep -i
"SIN-CHOQUE"` → 0 aciertos · `git worktree list` → 1, este · PR abiertos → **0**
(`mcp__github__list_pull_requests state=open` → `[]`). Sin duplicado.

**Higiene (0.d):** `python3 tools/limpia_arbol.py --reporta` → 1 worktree vivo ·
1 rama local fusionada y viva · base al día · `D` = `NO-VERIFICABLE-SIN-GH`.

---

## 1 · P0.1 · La prueba de no-pérdida de la `L0`, re-corrida por este acto

### La unidad de fragmento, definida aquí y no heredada

`#962` reporta «149 fragmentos» sin decir qué es un fragmento, y no dejó nota.
Este acto **deriva la unidad del texto**, no la supone: la línea `L0` es una
cadena de anotaciones `*( … )*` concatenadas — se ve al comparar la línea de
27 MB de `fc13cdc~1` con `canon/L0/HISTORICO.md`, que es su prefijo hasta el
carácter **214 945**, donde `#962` eliminó la primera anotación duplicada. Un
**fragmento** es, por tanto, una anotación `*(…)*`.

### El universo: se declara, y se agota

El encargo pide «las 49 versiones distintas de la línea `L0` en el primer padre
de `main` desde el 19/sep». **Esa cifra no es alcanzable y se declara**, sin
ajustar el procedimiento para que cuadre (§2 de las instrucciones):

| universo | commits | versiones distintas de `L0` |
|---|---|---|
| primer padre de `origin/main` desde el 19/sep | 62 | **44** |
| primer padre, toda la historia del archivo | 44 | **44** |
| `estado-programa-v1_13.md` / `v1_12.md` (mismo criterio) | 0 | 0 |
| **`git rev-list --all` — universo MÁXIMO, sin primer padre** | **161** | **92** |

`canon/estado-programa-v1_14.md` sólo tiene **44** commits de primer padre en
toda su historia: 49 versiones de primer padre no existen. Las **92** del
universo máximo **dominan estrictamente** las 49 que el encargo pedía, así que
la prueba se corrió sobre ése y la diferencia de conteo deja de importar. La
premisa es `REPORTADO` y toca **logística** (contabilidad del universo), no qué
se mide: se replantea, se sigue y se declara (D-19 / §2 v2.15).

### El comando y su salida cruda

```
$ python3 - <<'EOF'
import re,subprocess,glob,os
FRAG=re.compile(r"\*\(.*?\)\*",re.S); ARCH="canon/estado-programa-v1_14.md"
def sh(*a): return subprocess.run(a,capture_output=True,text=True).stdout
vista=open("canon/L0/HISTORICO.md",encoding="utf-8").read()
for p in sorted(glob.glob("canon/L0/*.md")):
    if os.path.basename(p)!="HISTORICO.md": vista+="\n"+open(p,encoding="utf-8").read()
commits=sh("git","rev-list","--all","--",ARCH).split()
vistos=set()
for c in commits:
    b=sh("git","show",f"{c}:{ARCH}")
    l0=[l for l in b.split("\n") if l.startswith("**L0 · Gobierno")]
    if l0: vistos.add(l0[0])
print("UNIVERSO MÁXIMO (git rev-list --all, sin primer padre)")
print("commits que tocan el archivo:",len(commits))
print("versiones DISTINTAS de la línea L0:",len(vistos))
todos=set()
for t in vistos: todos.update(FRAG.findall(t))
print("fragmentos distintos:",len(todos))
falt=[f for f in todos if f not in vista]
tt=0;ok=0
for fr in todos:
    c=fr[2:-2];n=len(c)
    pr=[c] if n<90 else [c[int(n*f):int(n*f)+30] for f in (0.25,0.50,0.75)]
    tt+=len(pr); ok+=sum(1 for p in pr if p in vista)
print("trozos del medio:",tt,"presentes:",ok)
print("ausentes ENTEROS:",len(falt))
print("VEREDICTO:", "SIN PÉRDIDA" if not falt and tt==ok else "PÉRDIDA")
EOF
UNIVERSO MÁXIMO (git rev-list --all, sin primer padre)
commits que tocan el archivo: 161
versiones DISTINTAS de la línea L0: 92
fragmentos distintos: 142
trozos del medio: 426 presentes: 426
ausentes ENTEROS: 0
VEREDICTO: SIN PÉRDIDA
```

Los tres trozos son del **medio** del fragmento (25 %, 50 %, 75 %, 30 caracteres
cada uno), nunca del borde: el borde es el delimitador `*(`/`)*` y casaría
trivialmente contra cualquier otro fragmento.

**Veredicto: `#962` no perdió nada.** 142 fragmentos distintos en 92 versiones
distintas de la línea, los 142 presentes en la vista vigente
(`canon/L0/HISTORICO.md` + los fragmentos por acto), 426 de 426 trozos del medio
presentes, cero ausencias.

**Estado colateral, no defecto:** `HISTORICO.md` contiene **180** ocurrencias de
fragmento para **142** distintos — la deduplicación de `#962` no fue total. No
es pérdida y no cambia ningún veredicto; se anota y no se instrumenta (§1: el
aparato tiene costo).

---

## 2 · P0.2 · Las cuatro `NC`, cerradas con evidencia

Las cuatro quedan **CERRADAS** en `forense/no-corrido.tsv` (columna `estado`,
con `cerrado_por` y `fecha_cierre`). Dos por arreglo, dos por quedarse sin
objeto.

### `NC-260921-GEN2-TUBERIA-SIDECAR-CUERPO-1-3d08-03` — CERRADA, sin objeto

Decía que `cierre_acto.py --aplica` derivaba los tres contadores del **máximo**
de ADR y no del conteo de **únicos**. P-B de `#962` dejó esos tres contadores
HISTÓRICOS, así que `--aplica` ya no los escribe y la aritmética no tiene
superficie. Evidencia, corrida sobre este árbol:

```
$ python3 tools/cierre_acto.py --aplica
contadores HISTÓRICOS (P-B, no se escriben): cabecera de gobernanza, L0 de
estado-programa, fila de tabla §0 -- ADR numérico real: 593 (`EC.adr_max`);
los ADR de raíz de acto (P-C) no participan de este conteo.
sin cambios -- ningún archivo de gobierno escrito por esta fase
$ git status --porcelain
(vacío)
```

### `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-04` — CERRADA **por arreglo**, y el defecto ya había ocurrido

El encargo la describía como «obsoleta pero ruidosa»: recetas que derivan el
máximo por `max+1` sobre el espacio cerrado, que «no se rompen y no mienten».
**Sí mentían.** Medido aquí:

```
$ python3 -c "import sys;sys.path.insert(0,'tools');import estado_comun as EC;print('fp_max=',EC.fp_max('.'))"
fp_max= 260921
```

`EC.fp_max` usaba `^FP-(\d+)` y casaba las **17** filas de raíz de acto
(`FP-260921-GEN2-…`), devolviendo el **FP fantasma 260921**. `#962` puso el
guardia `(?![\d-])` en `adr_max` —y documentó por qué, en su propio
docstring— **y no lo puso en `fp_max`, en el mismo archivo**. Arreglado aquí,
una línea, defecto adyacente de ≤ 10 líneas (D-21):

```
$ python3 -c "import sys;sys.path.insert(0,'tools');import estado_comun as EC;print('fp_max=',EC.fp_max('.'))"
fp_max= 409
$ grep -oE '^FP-[0-9]+\b' forense/firmas-pendientes.tsv | grep -vE '^FP-[0-9]{6}$' | grep -oE '[0-9]+' | sort -n | tail -1
409
```

El valor coincide con el comando de control independiente. Además,
`tools/tablero_programa.py` deja de publicar el espacio cerrado como si fuera el
universo: `adr_max` → `adr_max_espacio_cerrado`, `fp_max` →
`fp_max_espacio_cerrado`, ambos con su nota («espacio NUMERICO cerrado (D-2): no
es el ultimo id acuñado»), y un indicador nuevo `ids_raiz_de_acto` que cuenta la
época vigente por comando:

```
$ grep -coE '^\*\*ADR-[0-9]{6}-' canon/gobernanza-v1_15.md   -> 1
$ grep -coE '^FP-[0-9]{6}-' forense/firmas-pendientes.tsv    -> 17
$ grep -coE '^NC-[0-9]{6}-' forense/no-corrido.tsv           -> 34
```

Universo de consumidores examinado antes de renombrar (A.4/A.13):
`grep -rn "adr_max\|fp_max" --include=*.py --include=*.md --include=*.json .` →
los únicos consumidores **productivos** son `tools/estado_comun.py` y
`tools/tablero_programa.py`; el resto de aciertos son notas históricas
(`forense/tablero/*`, `forense/hallazgos.md`, encargos archivados) que describen
snapshots ya declarados obsoletos en su propio texto.

La otra pata de la `NC`, `.claude/commands/revisa.md:432,435`, **no requiere
cambio**: su único `tail -1` superviviente (línea 452) está acotado de forma
explícita, en las líneas 444–451, a **detectar colisión** sobre el espacio
CERRADO, no a derivar ids nuevos — `#962` ya lo había reescrito.

### `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-05` — CERRADA, sin objeto (`SUSTITUIDO-POR` la raíz de acto)

Pedía evaluar a fondo el esquema C (sufijo de desempate). Era una alternativa a
evaluar **antes** de elegir; D-2 (firma de mesa del 21/sep) eligió raíz de acto y
**congeló la forma**, y el árbol ya tiene 52 ids de esa época (1 + 17 + 34,
conteo de arriba). Un careo sobre una decisión ya firmada no es entregable.

### `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-08` — CERRADA, sin objeto

El propio encargo de este acto la declara verbatim **ERROR DE DIRECCIÓN** (un
conteo de líneas en vez de filas). Control corrido hoy, que reproduce el
mecanismo:

```
$ grep -cE '^FP-' forense/firmas-pendientes.tsv   -> 412   (filas)
$ wc -l < forense/firmas-pendientes.tsv           -> 415   (líneas)
```

La diferencia son saltos de línea embebidos en el campo de texto — exactamente
lo que produjo el `389 vs 387` del careo. No hay nada que conciliar en el árbol.

---

## 3 · P1 · `canon/registro-rotulos.tsv` deja de chocar

### P1.1 · La forma, sin perder ninguna fila

La cabecera estaba en la línea **2** y una fila de datos (`C · MAESTRA33-C4 · …`)
en la **1**. Se intercambiaron. **Antes de moverla** se verificó que ningún
lector dependiera de ese orden — los tres únicos lectores programáticos son:

| lector | cómo lee | ¿depende del orden? |
|---|---|---|
| `tools/ya_medido.py:427` (`busca_alias_registro_rotulos`) | itera TODAS las líneas, filtra por término | **no** — la cabecera simplemente nunca casa |
| `tools/cierre_acto.py:217-219` | `rotulo in texto` (subcadena) | **no** |
| `tests/check.py::t25` | sólo comprueba que el archivo exista | **no** |

Ninguno hace `skip(1)` ni `next(reader)`. Verificación del intercambio:

```
cabecera ahora en linea 1: True
mismo CONJUNTO de filas (multiconjunto ordenado): True
filas antes: 436 filas despues: 436
```

### P1.2 · La guarda: `T51 · T-ROTULOS-PAR-UNICO`

`T47` no sirve tal cual: su llave es un id al principio de la línea
(`NC-`/`FP-`), y la identidad de este registro es el **par `(espacio, valor)`**.
`T51` es esa misma aserción con la llave correcta. Estado medido hoy:

```
pares (espacio,valor) distintos: 426
pares REPETIDOS hoy: 7
   ('A', 'MAESTRA37-A2') 2
   ('E', 'E5') 2
   ('E', 'E9') 2
   ('E', 'GEN2-E7') 2
   ('E', 'MAESTRA34-E1') 2
   ('GEN2', 'GEN2-TRAMITE-4') 2
   ('M', 'M5') 4
```

**No se borró ninguno.** Los 7 quedan congelados como **exención declarada**
(`_T51_EXENCION`, con su conteo): la guarda falla sólo sobre repeticiones
**nuevas** — o sobre un par de la exención que **crezca**. `T51` comprueba
además que la línea 1 siga siendo la cabecera, para que el defecto de forma de
P1.1 no vuelva en silencio.

### P1.3 · La mutación de `#962`, con el caso exacto

`tests/test_tuberia_ids_union.py` gana **`G3-bis`** (una rama edita en su sitio
la última fila, otra añade debajo, se fusiona con `union`; `T51` **debe** fallar)
y **`G3-ter`** (la exención tolera el conteo de hoy y falla en cuanto ese mismo
par crece una fila). `G3` se conserva intacto como el registro de por qué el
archivo quedó fuera el 21/sep por la mañana. Salida cruda:

```
  OK    G3-bis registro-rotulos.tsv: sin conflicto real + T51 atrapa el par (espacio, valor) repetido con contenido contradictorio -> ENTRA a union -- conflicto=False T51=[('T51', "canon/registro-rotulos.tsv: el par (espacio, valor) ('E', 'GEN2-X') aparece 2 veces (congelado: 1) -- dos filas del mismo rótulo son dos significados contradictorios, y cuál gana depende del orden de lectura")] resultado='espacio\tvalor\tque_significa\tdonde_vive\nE\tGEN2-X\tEDITADO por A\tsitio-a\nE\tGEN2-X\toriginal\tsitio-a\nE\tGEN2-Y\tnueva\tsitio-b\n'
  OK    G3-ter T51: la exención congelada tolera el conteo de hoy y falla en cuanto ese mismo par crece una fila más -- sin_fail=True con_fail=[('T51', "canon/registro-rotulos.tsv: el par (espacio, valor) ('M', 'M5') aparece 3 veces (congelado: 2) -- dos filas del mismo rótulo son dos significados contradictorios, y cuál gana depende del orden de lectura")]
────────────────────────────────────────────────────────────────────────
  TODO VERDE
```

**La mutación falla ⇒ el archivo ENTRA.** `.gitattributes` gana
`canon/registro-rotulos.tsv merge=union`, con el porqué escrito al lado del
párrafo de `#962` que lo dejaba fuera — ese párrafo **no se borra**, se completa.

### P1.4 · `T46` y `T50` lo cubren solos

Pre-comprobado antes de declararlo `union`, para no meter un FAIL nuevo:

```
termina en salto de linea: True          (T46)
lineas >=200 caracteres repetidas: 0     (T50)
```

---

## 4 · P2 · `estado-programa` deja de tocarse en cada cierre

### Premisa que cayó (logística, no qué se mide)

El encargo pide medir «en los PR posteriores a `#962`». **No hay ninguno**:
`fc13cdc` (el merge de `#962`) **es** la cabeza de `origin/main`. Se replantea
al universo que sí existe (D-19) y se declara: los **11** PR de primer padre
**anteriores** a `#962` que modifican el archivo, más los pasos de `acto.md` que
lo mencionan.

### Lo que un cierre seguía escribiendo a mano

Medido con `git diff --unified=0 <merge>^1 <merge> -- canon/estado-programa-v1_14.md`
sobre los 12 merges de primer padre más recientes que tocan el archivo:

| qué se escribe | en cuántos de los 11 PR previos a `#962` |
|---|---|
| la línea `L0` | 11 de 11 *(ya congelada por `#962`)* |
| la fila `gobernanza` de la tabla §0 (`\| **gobernanza** \| … \| NNN ADR …`) | **11 de 11** |
| una línea `*Anotación L0 (fecha): …` nueva en §0 | **6 de 11** |

El propio `#962` (`fc13cdc`) ya no escribió ninguna de las dos últimas: sólo
tocó la `L0`. Pero el canal seguía abierto, y es **la misma forma** que infló la
`L0` a 27 MB: un apéndice por acto en un punto compartido de un archivo
compartido. Hay **96** de esas anotaciones acumuladas en §0.

### El mismo trato que la `L0`

1. Las **96** anotaciones y la fila de la tabla quedan **HISTÓRICAS**, con su
   hash fijado — igual que `T49` fija el de `canon/L0/HISTORICO.md`.
2. Guarda nueva **`T52 · T-ESTADO-PROGRAMA-SIN-APENDICE`**: conteo (96), sha256
   del bloque (`ebbfe58c…c50f`) y la fila `gobernanza` verbatim. Cualquier
   apéndice nuevo es FAIL, con el «qué hacer» en el propio mensaje.
3. Marca en el archivo, encima del bloque, diciendo que está congelado y a
   dónde va la anotación de cada acto.
4. `acto.md`, paso 3 de la cascada (dentro de los pasos que §1 del encargo
   autoriza): **«un cierre estándar no modifica
   `canon/estado-programa-v1_14.md`»**, con las cifras de la tabla de arriba y
   la comprobación por `git status`.

### Criterio de «hecho» de P2, verificado

```
$ python3 tools/cierre_acto.py --aplica
sin cambios -- ningún archivo de gobierno escrito por esta fase
$ git status --porcelain            # cero archivos, estado-programa incluido
```

Y este acto es su propio acto sintético: su anotación va a
`canon/L0/ADR-260921-GEN2-TUBERIA-CIERRE-SIN-CHOQUE-2-8e53-01.md`, y de
`estado-programa` sólo toca la marca de congelación de P2 — nunca el bloque
congelado ni la fila.

---

## 5 · P3 · Lo que queda fuera, medido

El mapa se **re-deriva aquí**, no se hereda: el encargo lo da sobre «198 PR
fusionados en 7 días» y este acto mide sobre **62 merges de primer padre** desde
el 14/sep (`git log --first-parent --since=2026-09-14 origin/main`), cruzados con
`git diff --name-only <m>^1 <m>`. El **denominador difiere, el orden no**: los
porcentajes de abajo no son los del encargo y son los que este árbol da.

| archivo | PR que lo tocan | % de 62 | hoy | veredicto |
|---|---:|---:|---|---|
| `canon/estado-programa-v1_14.md` | 43 | 69.4 | fragmento por acto + bloque congelado (`T52`) | **se resuelve solo** — *esta pieza* |
| `canon/gobernanza-v1_15.md` | 43 | 69.4 | `union` + `T15` | se resuelve solo |
| `canon/registro-rotulos.tsv` | 41 | 66.1 | `union` + `T51` | **se resuelve solo** — *esta pieza* |
| `forense/hallazgos.md` | 40 | 64.5 | `union` | se resuelve solo |
| `forense/no-corrido.tsv` | 39 | 62.9 | `union` + `T47` | se resuelve solo |
| `forense/firmas-pendientes.tsv` | 35 | 56.5 | `union` + `T47` | se resuelve solo |
| `forense/analisis/ci-guardias/censo-tests.tsv` | 14 | 22.6 | vista derivada por `tools/ci_guardias.py --censo` | **no se toca** — vista |
| `tests/check.py` | 12 | 19.4 | lista de registro de tests | **no se toca** — es código |
| `data/corrida0/corridas.tsv` | 8 | 12.9 | vista derivada, re-derivada por cada acto que sella | **no se toca** — E.7 |
| `data/corrida0/resultados.tsv` | 7 | 11.3 | ídem | **no se toca** — E.7 |

Tres cosas para el sucesor, ninguna tocada aquí:

- **Las vistas derivadas** (`corridas.tsv`, `resultados.tsv`, 12–13 %). Chocan
  porque cada acto que sella las re-deriva enteras. Cambiarlo toca **E.7**
  («toda corrida sellada entra a la vista en el mismo acto que la sella»), que es
  regla de instrucciones: **DECISIÓN-DE-MESA-PENDIENTE**.
- **`forense/analisis/ci-guardias/censo-tests.tsv` (22.6 %)** — **hallazgo nuevo
  de este acto, que el mapa del encargo no nombra**: es la séptima fuente de
  choque del árbol, por delante de `tests/check.py`, y es una vista derivada por
  comando (`tools/ci_guardias.py --censo`), no un registro. Misma clase que las
  de `corrida0`, mismo sucesor.
- **`tests/check.py` (19.4 %)**: los actos añaden su test a una sola lista de
  registro. Es código; `union` no le sirve.

---

## 6 · Módulo de auditoría

**No aplica.** Este artefacto no afirma nada sobre México: es tubería de
gobierno del repo, cero microdato, cero regla del motor, cero cifra sobre
población mexicana. **Contadores movidos: cero** (`cuenta_gen2 = NO`, declarado
en la cabecera del encargo) — el trabajo es de aparato, y §1 exige decirlo en una
línea al inicio cuando es cero.

## 7 · Falsador (del encargo, §6)

Si en dos semanas `canon/registro-rotulos.tsv` vuelve a aparecer en un conflicto
de fusión, o un cierre vuelve a modificar `canon/estado-programa-v1_14.md`, el
mecanismo no hizo lo que dice. `T51` y `T52` caducan a los tres meses
(21/dic/2026) si no atrapan nada, y se anota (§9).
