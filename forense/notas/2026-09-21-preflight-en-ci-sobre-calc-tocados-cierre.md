# ACTO GEN2-TUBERIA-PREFLIGHT-CI-1 · nota de cierre

**Encargo archivado (A.3):** `forense/encargos/2026-09-21-GEN2-TUBERIA-PREFLIGHT-CI-1.md`, 0-bis `9919f28`.
**SHA de redacción del encargo:** `5a888bcb`. **SHA al abrir:** `c1f6bd8`. **SHA tras fusionar main durante el acto:** `a61dd000` → cabeza de la rama `7ed6dd88`.
**Entorno:** NUBE (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default`), sin corpus, cero microdato.
**Modo:** ABIERTO. **Compuerta:** ninguna. **CONTADOR:** `cuenta_gen2 = NO` — este acto no mide ninguna celda del programa y no mueve ningún contador de GEN2.

---

## 0 · ARRANQUE (Bloque D, ejecutado por `/acto`)

```
ENTORNO-DERIVADO = NUBE
senal-corpus: montado=NO archivos_examinados=0
senal-nube-env: CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default
red: DENEGADA-POR-POLITICA (http_code=000, http_connect=403, x_deny_reason=ausente, via_proxy=SI)
head-vs-origin/main: detras=0 adelante=0 (sin fetch)
worktrees: 1
es-worktree: NO
ramas-locales-con-commits-propios: 1/2
data-raw-en-este-worktree: NO
```

El entorno derivado coincide con el que el encargo asigna: no hay PARO (e).
`data/raw` ausente y no hace falta: este acto no abre microdato. La sonda de
red sale DENEGADA-POR-POLITICA y no se usa para nada: el chequeo que se
construye no toca red.

**Ramas vivas, re-derivadas (A.13).** El encargo declaraba cinco. Al abrir
había **cinco**, pero **no las mismas**: `acto/gen2-tramite-firmas-3-propagacion`
ya había fusionado (`PR #940`) y en su lugar estaba
`acto/gen2-celda-d-piloto-3-commit-1-v1_2`. Comando:
`git ls-remote --heads origin` → 6 refs, una de ellas `main`. Al cerrar, tras
fusionar main, el remoto tenía **siete** ramas ≠ `main`. No es PARO: toca
logística (§2, D-19), se re-derivó y se declara.

**Duplicado por CONTENIDO, no por nombre (P0).** Examinadas **6 ramas remotas**
(las 5 vivas + `main`) y los **5 PR abiertos**:

```
for b in $(git ls-remote --heads origin | sed 's#.*refs/heads/##'); do
  git grep -l -i "PREFLIGHT-CI" origin/$b -- forense/ .github/ tools/ tests/ | wc -l
done
→ 0 en las 6
```

`NO-ENCONTRADO` (A.4): ninguna rama viva archiva este encargo ni contiene el
rótulo. Ningún PR abierto lo lleva en el título. Se siguió.

**`GEN2-TUBERIA-SIDECAR-CUERPO-1`** —la concurrencia que el encargo preveía
sobre `verify.yml`— no existe en ninguna rama ni PR abierto: no hubo
concurrencia sobre ese archivo. Se fusionó main hacia la rama de todos modos,
por las cuatro ramas que sí avanzaron durante el acto.

---

## 1 · OBSTÁCULO RESUELTO Y DECLARADO (D-19, LATITUD) — el clon era superficial

**El clon de esta sesión nació con `--depth` y sólo tenía historia desde el
19/sep.** Primer síntoma: `git log origin/main --first-parent -- data/corrida0`
devolvía **28** commits *en toda la historia*, y ninguno de los cinco PR que el
encargo cita en §4 (`#629`, `#775`, `#776`, `#781`, `#785`) aparecía en `main`.
La conclusión fácil —y falsa— habría sido «esos PR no están en main».

```
ls .git/shallow            → existe (1189 bytes)
git rev-list --count origin/main  → 440
git log origin/main --format=%cI | tail -1 → 2026-09-19T14:50:58-06:00
```

`git fetch --unshallow` (26 s) → 5358 commits, historia desde el 29/jul. Los
cinco PR aparecen inmediatamente. Obstáculo reversible y barato, resuelto y
declarado.

**Vale la pena asentarlo porque es la misma clase que `ACTO MOTOR-LINAJE-1`
midió ayer del otro lado**: allí un `fetch --depth=1` en el job `guardias` de
CI hacía que dos pruebas se clasificaran `FALLA-DE-VERDAD` cuando la causa era
el clon mutilado (D-23). Aquí el clon mutilado casi produce un negativo sobre
la existencia de cinco PR. **Un negativo derivado de un clon superficial no es
un negativo sobre el repo: es un negativo sobre el clon** (A.13, A.4).

---

## 2 · PREMISAS VERIFICADAS

| # | premisa del encargo | rótulo | verificación en esta sesión | veredicto |
|---|---|---|---|---|
| 1 | 168 CALC con `spec.yaml`, 15 sin `sello.json` | EJECUTADO | `find data/corrida0 -maxdepth 2 -name spec.yaml \| wc -l` → **168**; sin `sello.json` → **15** | SE SOSTIENE |
| 2 | los 15 sin sello, nombrados | EJECUTADO | los 15 directorios listados coinciden uno a uno con los del encargo | SE SOSTIENE |
| 2-bis | de los 15, «8 pasan preflight y 7 no», y los 7 son los nombrados | EJECUTADO | corrido el chequeo sobre los 15: **7 FAIL**, y son **exactamente** `DINERO-FAMILIARES-VEJEZ-0001`, `EVASION-NORMA-0001`, `HORIZONTE-VIA-DERIVADOS-0001`, `TIENE-AHORROS-0001`, `GOB-DIGITAL-EXE-EMISIONES-0001`, `GOB-DIGITAL-EXE-EMISIONES-0002`, `GOB-DIGITAL-EXE-ADJUDICACION-0001`. Ver el matiz de abajo | SE SOSTIENE |
| 3 | `preflight` resuelve `spec_md` relativa al directorio del CALC | EJECUTADO | `tools/corrida0.py:1615` — `md = d / str(spec.get("spec_md", "spec.md"))` | SE SOSTIENE |
| 4 | `preflight` devuelve un diccionario con `veredicto`/`bloqueos`/`avisos` | LEÍDO | `tools/corrida0.py:1592` `def preflight(calc_id, imprime=True) -> dict`; `return` en :1760 | SE SOSTIENE |
| 5 | las familias de bloqueo son 27 | LEÍDO | `grep -n 'bloqueos.append' tools/corrida0.py` → **29 sitios**, que colapsan a 27 familias contando `resultado_*` (5), `seed_*` (6) e `input_manifiesto_*` como una cada una. Ver §3 abajo: hay **dos vías más** que el encargo no enumera | SE SOSTIENE CON MATIZ |
| 6 | el CI clona con `--depth=1` la ref de merge y no tiene base | LEÍDO | `verify.yml`: `suite` y `adicionales` con `--depth=1`; `guardias` ya sin `--depth` desde `ACTO MOTOR-LINAJE-1` (21/sep). Ninguno de los tres trae `origin/main` ni el primer padre bajo ese nombre | SE SOSTIENE |
| 7 | `preflight` no escribe nada | EJECUTADO | docstring :1593; y verificado de punta a punta en la prueba por mutación, caso 7 (`git status --porcelain` vacío tras correr el chequeo) | SE SOSTIENE |
| 8 | `preflight` en `verify.yml`: 0 ocurrencias | EJECUTADO | `grep -c preflight .github/workflows/verify.yml` → 0 antes de este acto | SE SOSTIENE |

Ninguna premisa falsa. Ninguna tocaba qué se mide ni una firma de mesa, así que
no había PARO (a)–(f) en ningún punto.

**El matiz de 2-bis vale como confirmación del diseño, no como discrepancia.**
Corridos los 15 en esta sesión, `preflight` dice **BLOQUEADO en los 15**, no en
7 — porque el árbol de trabajo tenía los archivos de este acto sin commitear y
los 15 heredaron `working_tree_dirty=SI`. Clasificados, los ocho «extra» quedan
**LIMPIO**: su único bloqueo es `working_tree_dirty`, que este chequeo reporta
sin adjudicar precisamente porque **quien ensucia el árbol en CI es el propio
chequeo, no el PR**. Es decir: la medición de dirección («8 pasan, 7 no») se
reproduce **exactamente** una vez que el ruido del árbol se saca de la
adjudicación, que es lo que la clase `FUERA-DE-ALCANCE` existe para hacer. La
clasificación se validó contra un caso que nadie fabricó para ella.

---

## 3 · MATIZ A LA PREMISA 5 — dos vías de bloqueo que el encargo no enumera

El encargo previó exactamente esto («si al derivar las familias de bloqueo del
código encuentras una que no está en §3, no es PARO: aplica la regla y
decláralo»). Se encontraron **dos**, y ninguna sale de `bloqueos.append`:

1. **`_carga_spec` levanta `BloqueoPreflight`, no un bloqueo**
   (`tools/corrida0.py:1170,1174`): `spec_yaml_ausente` y `spec_yaml_no_es_mapa`
   son **excepciones**, así que `preflight(...)` nunca regresa y quien sólo lea
   `res["bloqueos"]` no ve nada. El chequeo las captura y las convierte en un
   bloqueo sintético `bloqueopreflight=<texto>`, que por la regla general cae en
   **FAIL** — que es lo correcto: un CALC cuyo `spec.yaml` ni siquiera carga es
   el caso más crudo del defecto, no una excepción a tratar aparte.
2. **`spec_sin_<campo>` e `ids_<nombre>_duplicados` son familias paramétricas**,
   igual que `input_manifiesto_<estado>`: el token lleva el campo pegado. La
   clasificación corta el token en el primer `=` o `(` antes de compararlo, así
   que `spec_sin_seed`, `spec_sin_tolerancia` y los nueve campos obligatorios
   entran los nueve sin enumerarlos.

Consecuencia práctica: **la lista de FAIL no existe y no debe existir.** La
única lista cerrada es la de estados legítimos, y todo lo demás —incluido lo
que dirección añada mañana a `corrida0.py`, que este acto no toca— se trata
como `preflight` lo trata.

---

## 4 · LO ENTREGADO

### P-a · `tools/preflight_calc_tocados.py`

- **Universo del cambio:** `git diff --name-only <base> <cabeza> -- data/corrida0`,
  agrupado por directorio de CALC, y de ésos se conservan los que en **`cabeza`**
  tienen `spec.yaml` y **no** tienen sello. El universo se deriva con
  `git ls-tree` sobre `cabeza`, no del disco: un CALC borrado por el PR no deja
  fantasma, y el universo es el mismo se corra donde se corra.
- **Sello:** `sello.json` **o** `sello.sha256`. `preflight` verifica por
  `sello.sha256`; dirección cuenta el universo por `sello.json`. Hoy los dos
  conjuntos coinciden (**153 y 153** sobre 168), así que la unión no cambia nada
  y cubre el desfase si un día llegaran separados.
- **Llamada:** `preflight(calc_id, imprime=False)` importando `tools/corrida0.py`
  **sin modificarlo** (PARO respetado).
- **Clasificación:** `WARN` si el token está en la lista cerrada de legítimos ·
  `FUERA-DE-ALCANCE` si es `calc_ya_sellado`, `sello_previo_incompatible` o
  `working_tree_dirty`, que se reportan sin adjudicar · **`FAIL` en todo lo demás**.
- **Salida:** por CALC, el veredicto de `preflight` y cada bloqueo con su clase
  **y su razón**, de modo que un rojo diga exactamente qué lo puso rojo y qué
  haría falta para que dejara de serlo.
- **Universo vacío:** pasa y lo dice — `0 CALC sin sello tocados`.
- **D-23:** no hace `fetch`, no escribe, y fija `PYTHONDONTWRITEBYTECODE` antes
  de importar `corrida0` — un `__pycache__` recién escrito es justo lo que
  `preflight` leería como `working_tree_dirty`, es decir un rojo fabricado por
  el propio chequeo.

La lista de estados legítimos vive en **un solo sitio** (`ESTADOS_LEGITIMOS` /
`PREFIJOS_LEGITIMOS`) y cada entrada trae por qué es legítimo, citando la nota
del 15/sep, la dependencia de cadena o la ausencia de corpus.

### P-b · el job `preflight-calc` en `.github/workflows/verify.yml`

Clon **propio** con `--depth=2` sobre la ref de merge —cuyo primer padre es la
punta de main—, porque D-23 prohíbe hacer `fetch` dentro del clon de otro job.
Corre en PR y en push a `main`, instala `requirements.txt` como los demás,
ejecuta primero la prueba por mutación (D-21: el acto cablea su propio test) y
después el chequeo. Añadido a `needs` del job `check`, que es el nombre que la
protección de rama exige, con su propia aserción de `success`.

### P-c · `tests/test_preflight_calc_tocados.py` — prueba por MUTACIÓN

Sobre CALC **sintéticos** en un repo git temporal —nunca sobre los reales, que
este acto no toca—. El repo temporal se arma con
`git archive HEAD tools milpa tests requirements.txt`: `corrida0.py` importa
`milpa.src.emisor` y `tests/payload_resolver` en su cabecera, así que copiar
sólo `tools/` no arranca (medido: falla con `ModuleNotFoundError` en las dos).
No se copia `data/corrida0`: el universo del repo temporal son exclusivamente
los CALC que la prueba fabrica.

Casos, todos en verde:

| caso | espera | da |
|---|---|---|
| clasificación: 6 tokens legítimos | WARN | WARN |
| clasificación: 14 tokens (los 13 reales + uno inventado) | FAIL | FAIL |
| clasificación: 3 tokens fuera de alcance | FUERA-DE-ALCANCE | idem |
| cada estado declara su razón | razón no vacía | 10/10 |
| universo vacío (cambio que no toca CALC) | pasa y lo dice | sí |
| CALC limpio | pasa, `preflight` VERDE | sí |
| **#926** · `spec_md` como ruta desde la raíz | rojo, y nombra el archivo | sí |
| **#903** · `seed` ausente | rojo, y nombra `spec_sin_seed` | sí |
| **#781** · sin `spec.md` | rojo, y nombra el archivo | sí |
| sólo `script_ausente` | WARN, no rojo | sí |
| sólo `input_repo_ausente` | WARN, no rojo | sí |
| CALC **sellado** con defecto adentro | no entra al universo | sí |
| el chequeo no ensucia el árbol (D-23) | `git status` vacío | sí |

El archivo bajo prueba se copia del **árbol**, no de `HEAD`: si se copiara de
`HEAD`, la prueba del primer commit de un acto ejercitaría una versión que
todavía no existe y pasaría en falso.

### P-d · re-corrida retrospectiva

En un **clon temporal compartido** (`git clone -s`, D-23: nunca sobre el clon
que se verifica), para cada commit de first-parent de `main` desde el 7/sep que
toca `data/corrida0` —**128** commits—, se hizo `checkout` de ese commit y se
corrió el chequeo con el **`corrida0.py` de ese commit**, leyendo su diccionario.

| | dirección (§4 del encargo) | esta sesión | |
|---|---|---|---|
| PR con CALC sin sello en el universo | 11 | **12** | +1, explicado abajo |
| chequeo **literal** (rojo si `preflight` dice BLOQUEADO) | 7 rojos, 4 falsos | **7 rojos, 4 falsos** | **idéntico** |
| los 4 falsos | #775, #776, #785 (`script_ausente`) y #629 (corpus) | **los mismos cuatro** | **idéntico** |
| chequeo **con clasificación** | 3 rojos, los 3 verdaderos | **3 verdaderos + 1 artefacto** | ver abajo |
| los verdaderos | #781, #903, #926 | **#781, #903, #926** | **idéntico** |

**El +1 y el «artefacto» son la misma fila, y no es un rojo falso del chequeo:**
es `#600` (8/sep), donde el chequeo revienta con
`ImportError: cannot import name 'preflight' from 'corrida0'` — en ese commit
**`preflight` todavía no existía** (nace con `ACTO GEN2-E3`, 7-8/sep). Correr el
chequeo de hoy contra un commit anterior a la función que el chequeo llama está
fuera de su rango de validez; en producción no puede ocurrir. Excluyéndolo, la
re-corrida reproduce **exactamente** lo que dirección midió: **11 PR en el
universo, 3 PR rojos, los tres verdaderos, cero rojos falsos.**

La conclusión de §4 queda **confirmada por medición independiente**, y con ella
la razón de ser de la clasificación: el chequeo literal habría puesto rojos **4
PR legítimos de 7**, es decir, más de la mitad de sus rojos habrían sido ruido —
y un chequeo que se equivoca la mitad de las veces se desactiva en una semana.

---

## 5 · LO QUE ESTE ACTO NO HACE

No arregla los dos CALC del piloto (`GOB-DIGITAL-EXE-EMISIONES-0002`,
`GOB-DIGITAL-EXE-ADJUDICACION-0001`): siguen BLOQUEADOS en `main` y su arreglo
es de `PR #944`. **El chequeo no los pone rojos mientras nadie los toque**, y
cuando el sucesor los corrija, el chequeo verificará el arreglo —comprobado: el
chequeo corrido sobre este propio PR da `0 CALC sin sello tocados`—. No corre
`preflight` sobre todos los CALC sin sello. No borra ni marca los cinco
superados. No cambia qué bloquea `preflight`. No toca la plantilla ni E.5/D-22:
sólo siembra el `PARA-v2.16`. No fusiona su propio PR.

---

## 5-ter · LA SUITE — `ROJO`, con cero FAIL de este acto

`python3 tests/check.py --baseline --parallel` en la cabeza de esta rama:
**2 FAIL nuevos** frente a `tests/baseline.json`, los dos de `T22`, sobre
`forense/encargos/2026-09-21-GEN2-SENAL-1.md` y su nota de cierre.

**No son de este acto, y no se afirma: se midió.** La misma suite corrida sobre
`origin/main` `a61dd000` **limpio**, en un clon temporal (D-23, nunca sobre el
clon que se verifica), da **exactamente esos dos FAIL y ningún otro**, con los
**mismos 25 WARN nuevos** de `T03`. El conjunto de FAIL de esta rama es
**idéntico** al de su base: **este acto no añade ni un FAIL ni un WARN**.

No se arreglan aquí: los dos archivos son de `ACTO GEN2-SENAL-1` y el PERÍMETRO
de éste (§9 del encargo) no los incluye; lo que `T22` pide es una fila en
`forense/firmas-pendientes.tsv`, que es una decisión de trámite, no un defecto
adyacente de ≤10 líneas. Asentado en
`NC-260921-GEN2-TUBERIA-PREFLIGHT-CI-1-9919-01`.

**El criterio de «hecho» del encargo pedía VERDE y no se entrega VERDE.** Se
dice así, sin suavizarlo: lo que se entrega es *el mismo rojo que ya tenía la
base*, declarado y medido contra ella.

**`T15` cobró su falsador dos veces en este mismo cierre**, y las dos veces
sobre texto de este acto: primero por el hueco de numeración (ver 5-bis), y
después porque la prosa que explicaba ese primer rojo **citaba el mensaje del
test verbatim**, y el número dentro de la cita cuenta como cita. Es el hallazgo
que `ADR-577` asentó para `T25` —«la cita de un defecto reproduce el defecto»—
reaparecido en un test distinto, al día siguiente, sin que nadie lo buscara. Se
reformularon las frases; **no se exentó ningún archivo**, porque aquí el texto
no es verbatim de nadie y reformularlo no falsea nada.

---

## 5-bis · IDS DE ESTE ACTO

- **ADR:** máximo real re-derivado con el comando de la casa contra `origin/main`
  `32e23f7a` → `583`; candidato contiguo **`584`**, que es el que este acto
  toma. **RENUMERADO `580` → `584`**: al primer cierre el máximo era `579`,
  pero `#942`, `#944` y los correctivos de `#945` fusionaron antes y `580`–`583`
  quedaron tomados — **renumera quien fusiona segundo**, regla de la casa.
  **Mesa fijó el orden de merge de este PR DESPUÉS de `PR #944`** (21/sep/2026),
  así que si ése u otro se lleva `584` primero, este acto vuelve a renumerar.
  **Se intentó primero saltar al `581`** para no disputar el número, dejando el
  hueco declarado — y `T15` lo rechazó con `FAIL`: la cabecera habría citado
  uno más de los ADR únicos que hay. La enmienda de `ADR-577` **acepta huecos
  en la numeración, no en el conteo**, porque su aserción (2) coteja el número
  citado contra los únicos. El aparato corrigió la lectura antes de que quedara
  escrita.

  **Y cobró su falsador dos veces en el mismo cierre.** Con la cabecera ya
  corregida, `T15` volvió a salir en rojo **por esta nota y por el ADR**: la
  redacción citaba el mensaje del test verbatim, y el número dentro de la cita
  cuenta como cita. Es el hallazgo que `ADR-577` asentó para `T25` —«la cita de
  un defecto reproduce el defecto»— reaparecido en `T15`, un test distinto, el
  día siguiente y sin que nadie lo buscara. Se reformularon las dos frases; **no
  se exentó ningún archivo**, porque aquí el texto no es verbatim de nadie y
  reformularlo no falsea nada.
- **NC y FP: ninguna.** El encargo pedía declarar cuál esquema de id aplicaba —
  raíz de acto si `main` ya contiene el merge de `GEN2-TUBERIA-SUCESOR-1`, o el
  viejo si no—. `main` **sí** lo contiene (`PR #939`; hay filas
  `NC-260921-GEN2-TUBERIA-SUCESOR-1-6e60-NN` en `forense/no-corrido.tsv`), así
  que el esquema aplicable habría sido el de **raíz de acto**
  (`<PREFIJO>-260921-GEN2-TUBERIA-PREFLIGHT-CI-1-9919-<NN>`, con `9919` del
  commit de 0-bis). **No se acuñó ninguno**: no hay pieza no corrida ni firma
  pendiente, y acuñar un id para decir «nada» sería aparato sin defecto (§1).

---

## 6 · FALSADOR A TRES MESES (§9)

Si al **21/dic/2026** el chequeo no ha puesto rojo un solo PR, se anota y se
revisa si valía el aparato. Si pone rojo un PR por un estado que resulta
legítimo, la lista de §4 está incompleta: se añade el estado **con su razón, en
un acto, visible** — nunca se relaja la regla de «todo lo demás es FAIL», y
nunca se añade un estado sin decir qué defecto real lo hace legítimo.

Contra qué se lee: hoy, `0` rojos puestos; el universo de referencia es
`origin/main` en `a61dd000`, con **168 CALC**, de los cuales **15 sin sello** y
**7 de esos 15 en FAIL** bajo esta clasificación (A.10: el sello porta su
universo; si el universo crece, esta línea queda VENCIDA EN ALCANCE, no
refutada).
