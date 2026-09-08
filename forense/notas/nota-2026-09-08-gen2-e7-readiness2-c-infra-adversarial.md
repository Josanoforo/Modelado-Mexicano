# ACTO GEN2-E7 · READINESS-2, Pieza C (caja) — verificación adversarial de INFRA con muestra propia

8/sep/2026 · entorno UBUNTU/WSL2, corpus montado · rama `acto/gen2-e7-readiness2-c`
sobre `origin/main = 9a950c9`. Cierra `NC-0001` (V1·P3, retrofit de `ACTO GEN2-T8`,
`ADR-393`). Método: **no se relee** la verificación post-hoc del 4/sep — se contrasta
con muestra propia, y todo negativo va con control que discrimina (`A.13`: se declara
qué examinó cada comando).

## Compuerta

```
$ git show origin/main:tools/corrida0.py | grep -c "def cmd_registro\|def cmd_status"
2
$ git show origin/main:tools/corrida0.py | grep -n "def cmd_registro\|def cmd_status"
2520:def cmd_registro(args) -> int:
2585:def cmd_status(args) -> int:
```

Verificada **por producto** (las dos funciones que `GEN2-E6` debía dejar), no por `grep` sobre
el log — el falso positivo que `ADR-277` midió.

---

## C1 · `test_alta_relacion.py`, cinco casos con fixture propio

**La premisa del encargo no se reproduce.** El encargo dice «lo que V1 pedía y nadie
hizo». El árbol dice otra cosa: el archivo existe desde el 3/sep, con cinco casos y
fixture propio (`tempfile.TemporaryDirectory`, nunca el corpus).

```
$ git log --format="%h %ad %s" --date=short -- tools/curador_registro/tests/test_alta_relacion.py
f62a761 2026-09-03 MAESTRA37-INFRA-1 Frente C (COMMIT-3): alta atómica de relaciones — tools/curador_registro/alta_relacion.py

$ python3 -m pytest tools/curador_registro/tests/test_alta_relacion.py -v
collected 5 items
...::test_alias_no_resuelto_hace_paro_explicito PASSED           [ 20%]
...::test_alta_exitosa_escribe_tres_tablas_y_recifra PASSED      [ 40%]
...::test_dry_run_no_escribe_nada PASSED                         [ 60%]
...::test_fallo_tardio_no_deja_tablas_adelantadas PASSED         [ 80%]
...::test_relacion_duplicada_siempre_rechaza PASSED              [100%]
============================== 5 passed in 0.15s ===============================
```

La ruta tampoco es la que el encargo cita: es `tools/curador_registro/tests/`, no
`tests/`. **No se escribió un archivo nuevo** — escribir `tests/test_alta_relacion.py`
habría duplicado cinco casos ya existentes bajo un nombre que colisiona.

**Hallazgo adversarial (H-1).** Los cinco casos pasan pero **la suite no los corre**:
`tests/check.py` sólo importa `tools/curador_registro/tsv_crudo.py` (T26-bis); no hay
ninguna referencia a `test_alta_relacion` en `check.py` ni en ningún `.yml`/`.json` del
árbol.

```
$ grep -n "test_alta_relacion\|curador_registro" tests/check.py
4410:    (2) REGRESIÓN del lector/escritor propio (`tools/curador_registro/
4443:    sys.path.insert(0, os.path.join(ROOT, "tools", "curador_registro"))
4447:        fail("T26-bis", f"no se pudo importar tools/curador_registro/tsv_crudo.py: {e}")

$ grep -rn "test_alta_relacion" --include=*.yml --include=*.yaml --include=*.json --include=*.py . \
    | grep -v "^./tools/curador_registro/tests"
(cero coincidencias fuera del propio archivo)
```

Consecuencia: una regresión en `alta_relacion.py` no la atrapa `--baseline`. Un test que
nadie corre no es cobertura. Sucesor: `FP-344`.

---

## C2 · Dos escritores simultáneos sobre un manifiesto de fixture

Arnés: `--registra` concurrente contra una raíz de fixture (`--root`, override
documentado como «solo para pruebas»), nunca contra `data/manifiesto.yaml` del repo.
N escritores lanzados a la vez, cada uno con su id y su archivo de contenido distinto;
se compara **procesos que reportaron éxito** contra **entradas realmente en el archivo**.

Tres brazos, para que lo que separe los casos sea el lock y no el temporizado:

| brazo | `flock` | ventana de carrera | lanzados | reportan éxito | en el archivo | perdidas |
|---|---|---|---|---|---|---|
| CON-LOCK | intacto | ninguna | 8 | 8 | **8** | 0 |
| CON-LOCK-VENTANA | intacto | `sleep(0.30)` entre leer y escribir | 8 | 8 | **8** | 0 |
| SIN-LOCK (control) | anulado | `sleep(0.30)` | 8 | 8 | **1** | **7** |

```
[CON-LOCK] escritores lanzados=8  procesos con exito=8  entradas pay_* en el manifiesto=8
[CON-LOCK] >>> sin escritura perdida
[CON-LOCK-VENTANA] escritores lanzados=8  procesos con exito=8  entradas pay_* en el manifiesto=8
[CON-LOCK-VENTANA] >>> sin escritura perdida
[SIN-LOCK] escritores lanzados=8  procesos con exito=8  entradas pay_* en el manifiesto=1
[SIN-LOCK] >>> ESCRITURA PERDIDA: 7 entradas reportadas como escritas no estan en el archivo
```

El brazo CON-LOCK-VENTANA es el que hace concluyente al control: con **la misma** ventana
de 0.30 s, el lock intacto no pierde ninguna. El `0` de CON-LOCK es un negativo medido,
no un arnés que no discrimina.

**Doble escritura en sentido estricto** (dos escritores, el **mismo** id, a la vez):

```
[CON-LOCK] mismo id x2 -> aceptados=1 rechazados=1 entradas 'mismo_id' en archivo=1
ERROR: el id 'mismo_id' ya existe. Este script no sobreescribe entradas registradas [...]
[SIN-LOCK] mismo id x2 -> aceptados=2 rechazados=0 entradas 'mismo_id' en archivo=1
```

Sin lock, **los dos procesos salen con éxito y sólo uno escribió**: el modo de fallo no es
un archivo corrupto, es un `Registrado` mentiroso. Con lock, uno escribe y el otro es
rechazado explícitamente. **El lock de `tests/manifiesto.py` hace lo que dice.**

Límite declarado, ya en el docstring del propio `_con_lock_manifiesto` y confirmado aquí:
protege escritores que comparten el **mismo archivo de lock**; no coordina clones
independientes. Los worktrees de este proyecto comparten `.git` pero **no** `data/` — cada
worktree tiene su propio `data/.manifiesto.lock`. Dos actos registrando a la vez desde dos
worktrees distintos no están cubiertos por esta prueba ni por este lock. Sucesor: `FP-345`.

**Defecto del arnés, corregido y anotado** (`A.13`): la primera corrida dio
`exito=0 / entradas=0` y el arnés lo leyó como «sin escritura perdida». Era un cero vacío,
no un negativo — la entrada semilla del fixture era inválida (`sin sha256`) y los ocho
procesos abortaron. Se leyó el log crudo antes de concluir; sin esa lectura, C2 habría
declarado VERDE examinando cero escrituras.

---

## C3 · `tools/arbitra.py` contra fixture (no contra corpus)

`tools/arbitra.py` fija `RAIZ = dirname(dirname(__file__))` y de ahí deriva `MANIFIESTO`,
`CORRIDAS_R`, `REGISTRO` y `ALIASES`. **No tiene punto de inyección**: no acepta `--root`
ni ninguna variable de entorno. Correrlo «contra fixture» exigió **copiar la herramienta a
una raíz falsa** completa (`tools/`, `tools/curador_registro/`, `data/manifiesto.yaml`,
`data/curacion-registro/*.tsv` con sólo cabecera, `forense/prereg-duelo-v2/corridas-R/`).
Este es ya el primer hallazgo: correr `arbitra.py` en el árbol real **escribe** en
`corridas-R/` y regenera `data/cola-adquisicion-v1_0.tsv`, ambos fuera del perímetro de
esta pieza. Un wrapper GEN2 (pieza A2) no puede envolver esto sin abrirle una raíz
inyectable primero.

**H-2 · el árbol incompleto revienta con traceback, no con estado declarado.** Con
`tools/curador_registro/` ausente, la primera celda sin payload aborta el lote entero:

```
ModuleNotFoundError: No module named 'curador_registro'
  ... File "tools/arbitra.py", line 137, in encola_no_obtenido
```

No hay estado `NO-EJECUTABLE-...` para esto: es excepción. (Contrasta con `produce()`, que
desde `MAESTRA35-L2/P1c` sí aísla la excepción por celda.)

**Ambigüedad de payload — se declara, no se adivina.** Manifiesto de fixture con **dos**
entradas que casan `(ENCIG, 2023)`:

```
"id_celda": "FIX-AMBIGUA",
"estado": "NO-EJECUTABLE-SIN-CODIFICACION",
"payload_id_candidatos": ["encig2023_uno", "encig2023_dos"],
```

`localiza_payload` devuelve la lista completa y `procesa_fila` la escribe entera; en los
caminos ejercitados **no** elige `candidatos[0]`. Y la celda sin payload sí se encola:

```
NO-EJECUTABLE-SIN-CODIFICACION: 1 -> FIX-AMBIGUA
NO-OBTENIDO: 1 -> FIX-SIN-PAYLOAD
```

**H-3 · el estado `NO-EJECUTABLE-SIN-CODIFICACION` es una constante del camino, no una
medición.** `procesa_fila` calcula `faltantes` y **acto seguido fija el estado sin
mirarlo** (`tools/arbitra.py:200-204`). Falsador: marco de fixture que **sí** trae
`codificacion`, `estrato_diseno` y `upm`, de modo que `faltantes` quede vacío.

```
NO-EJECUTABLE-SIN-CODIFICACION: 1 -> FIX-COMPLETA
estado   : NO-EJECUTABLE-SIN-CODIFICACION
faltantes: []
```

`faltantes: []` con estado `SIN-CODIFICACION` es un artefacto que se contradice a sí
mismo. **Alcance honesto:** esto vale para el camino por defecto
(`arbitra.py <marco.tsv>`), que es el que `main()` ejecuta. El camino que sí calcula un
número es `--produce`, que no lee las columnas del marco sino
`codificacion-R-v1_0.tsv`; **no se ejercitó aquí** (necesita corpus y está fuera del
perímetro C). Consecuencia para la pieza A2/B: envolver `main()` como corredor R
envolvería una función que, por construcción, nunca emite un R ejecutable. Sucesor:
`FP-346`.

---

## C4 · worktree sin `data/raw` → `RAIZ_NO_CONFIGURADA`, no excepción

Worktree nacido de `git worktree add ... origin/main`, sin `data/raw` y sin
`data/raices.local.yaml`. Se sondeó **un id por cada raíz declarada** en el manifiesto real
(1 569 entradas leídas; `data_raw` 277 entradas, `descargas_mx` 335) más un id inexistente
como control.

```
worktree           : /home/pc0/mm-gen2-e7-c
data/raw existe    : False
raices.local existe: False
entradas leidas    : 1569
ids sondeados      : {'data_raw': 'encig23_base_datos_csv', 'descargas_mx': 'descargamasiva_3072026_105543'}

[data_raw] encig23_base_datos_csv
  -> estado=AUSENTE ruta=.../data/raw/encig23_base_datos_csv.zip EXCEPCION=no
[descargas_mx] descargamasiva_3072026_105543
  -> estado=RAIZ_NO_CONFIGURADA ruta=None EXCEPCION=no

control id inexistente -> AUSENTE
```

**Ninguna excepción** — que es lo que C4 pedía comprobar. Control positivo: enlazadas
`data/raw` y `data/raices.local.yaml`, la **misma** sonda voltea de estado, así que
discrimina:

```
data/raw existe    : True
raices.local existe: True
[data_raw] encig23_base_datos_csv        -> estado=COINCIDE     (AUSENTE -> COINCIDE)
[descargas_mx] descargamasiva_...        -> estado=AUSENTE      (RAIZ_NO_CONFIGURADA -> AUSENTE)
```

**H-4 · la expectativa del encargo es imprecisa, y el código tiene razón.** «Worktree sin
`data/raw` → `RAIZ_NO_CONFIGURADA`» sólo se cumple para raíces **externas**. Para
`RAIZ_INTEGRADA` (`data_raw`), `resolver_raiz` devuelve siempre `raw_dir` — la raíz
integrada está *configurada por código*, así que el estado correcto es `AUSENTE` (no hay
archivo), no `RAIZ_NO_CONFIGURADA` (no hay raíz). Es exactamente lo que el docstring de
`tests/payload_resolver.py` declara. No es defecto: es la expectativa del encargo la que
se corrige.

El `AUSENTE` de `descargas_mx` tras enlazar **no** es del resolver: su raíz apunta a
`/mnt/c/...`, que el sandbox de esta sesión no lee. Verificado fuera del sandbox — el
archivo existe (602 155 B). Se declara para que nadie lo lea como payload perdido.

---

## Veredicto

| check | resultado | evidencia |
|---|---|---|
| C1 · cinco casos con fixture propio | **YA EXISTÍA** (3/sep), 5 PASSED — premisa del encargo no se reproduce | H-1: no cableado a la suite → `FP-344` |
| C2 · lock ante escritores simultáneos | **CUMPLE** — 8/8 con lock, 1/8 sin él, misma ventana | límite entre worktrees → `FP-345` |
| C3 · `arbitra.py` contra fixture | **CORRE**, no adivina payload — pero sin raíz inyectable | H-2 traceback; H-3 estado constante → `FP-346` |
| C4 · sin `data/raw` → sin excepción | **CUMPLE** — `RAIZ_NO_CONFIGURADA` sin excepción, control positivo voltea | H-4: expectativa del encargo corregida |

`NC-0001` → **CERRADA** por este PR: los cuatro checks corrieron con muestra propia y
salida cruda. `infraestructura_verificada_adversarialmente` se mueve. Lo que la
verificación **encontró** (H-1..H-3) no reabre `NC-0001`: se asienta como tres filas `FP`
con sucesor, que es la vía de la casa para deuda medida, no para deuda no corrida.

**Insumo para la pieza B (Go/No-Go del marcador).** El check `R-SIN-HEURÍSTICA` no puede
cumplirse envolviendo `arbitra.py` tal como está: (i) no tiene raíz inyectable — un wrapper
que lo invoque escribe en `corridas-R/` del árbol real; (ii) su camino por defecto emite un
estado constante que nunca es un R ejecutable. La R de GEN2 sale de `--produce` o de un
adaptador nuevo, no de `main()`.
