Contadores movidos: 0. (Este acto es de instrumento, no de evidencia — no
toca Hito D ni el contador de condicionales del motor.)

# Encargo E-3 · svystat.py contra casos de referencia

*4 de agosto de 2026.* Ejecutor: sesión nueva en `mm-svystat-casos-referencia`
(rama `sesion/svystat-casos-referencia`, worktree creado en este acto desde
`origin/main`). Base `main = 4b27869` (PR #95 fusionado) — local `main`
estaba 39 commits detrás (fast-forward limpio, 0 commits propios por
delante); sincronizado con `git fetch origin` antes de empezar.

**Sin módulo de auditoría** — este artefacto no afirma nada sobre México.
Prueba un estimador contra casos de referencia; no es report temático,
integrador ni validación forense de un constructo del canon.

**Por qué ahora.** `tests/svystat.py` se reimplementó desde cero el
03/ago/2026 (commit `40e5248`, CAL-CONF Fase B / segunda ola) y desde
entonces varios actos del programa dependen de él para producir cifras
que entran al modelo — CAL-CONF Fase B (tres componentes), Hito D R7.2, y
hay trabajo en curso al momento de abrir esta sesión que también lo usa
para medir una condicional nueva. El único autochequeo que traía el
módulo (`_caso_conocido`) es un caso degenerado (SRS, un solo estrato, un
solo elemento por UPM): nunca ejercita más de un estrato, ni más de una
observación por UPM, ni pesos desiguales entre UPM — exactamente lo que
la fórmula de conglomerado último tiene que agregar correctamente. Nadie
lo había probado contra un caso independiente que sí ejerza esa lógica.

## 0 · Entorno

```
$ python3 tests/bitacora.py --abre
HEAD == origin/main (4b27869). Divergencia: ninguna.
check.py --baseline:        exit=0 · LÍNEA BASE: VERDE (18 FAIL · 84 WARN)
validador_registro_ids.py:  exit=0 · OK — 49 IDs verificados
instrucciones vigente:      v2.3, commit 4fb7964 (coincide con la que tenía en contexto)

$ ls data/raw | wc -l
189   (symlink -> /home/pc0/mm-corpus/raw, 2.5G)
```

`data/raw` no traía el symlink al crear el worktree (todo worktree nuevo
nace sin raíces — ya documentado en `forense/hallazgos.md`, 31/jul); se
creó apuntando a la misma raíz compartida que usan los demás worktrees
vivos (`/home/pc0/mm-corpus/raw`). No hay PARO de entorno.

**Nota de proceso, no PARO:** `git worktree add` emitió dos veces
`error: could not write config file .git/config: Device or resource
busy` durante la creación (probablemente escritura concurrente de otra
sesión sobre el mismo `.git` compartido — clase de defecto ya registrada
como `I-11`, "checkout compartido... se bloquea sin que ninguna sesión
haga nada mal", en `forense/hallazgos-congelados-2026-07-30.yaml`). El
worktree quedó consistente pese al error: `git worktree list` lo lista,
`HEAD` coincide con `origin/main`, árbol limpio, `.git/config` del
worktree original (`Modelado-Mexicano`, rama ajena
`sesion/cal-conf-faseb-pos4-envipe-paso1`) verificado intacto después.
No se reintenta ni se investiga más — ya es una clase conocida, no una
nueva.

## 1 · Premisas — verificadas contra archivo, no aceptadas por cita

**PE-1.** `tests/svystat.py` existe en main, contiene una sola función
pública (`prop_ultimate_cluster`) y un autochequeo (`_caso_conocido`).
Leído completo antes de escribir cualquier caso nuevo. **Se sostiene.**

**PE-2.** Dos estimaciones archivadas con spec y resultado completos,
payload en el corpus, cifra citada con nota y línea:

- **Hito D R7.2, "ocho olas"** — `forense/notas/2026-08-04-r7-2-ocho-olas.md`
  (Encargo J, rama `sesion/hitoD-r7-2-delito-sin-seguro`, HEAD `eac2a57`),
  script `tests/hitoD_r7_2_ocho_olas.py` (commiteado en esa misma rama,
  no en main todavía). Cifra ancla: §3, brecha 2025 = 11.9pp
  IC95%=[6.4pp,17.4pp] (línea 60 de la nota). Payload: ocho
  `envipe20XX_csv.zip` (2018-2025) — **verificados presentes**, 17-24MB
  cada uno.
- **CAL-CONF Fase B, segunda ola** —
  `forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md` (rama
  `sesion/cal-conf-faseb-ola2`, ya fusionada a main en `40e5248`), script
  `tests/cal_conf_faseb_ola2.py` (commiteado en main). Cifra ancla: §3.1,
  Guardia Nacional, tramo 18-29 = n=16 620, 82.2%, se=0.43pp,
  IC95=[81.4%,83.1%] (línea 354 de la nota) — una de 121 celdas
  verificadas, ver §2.3 abajo. Payload: `envipe2025_csv.zip` y
  `BD_ENCUCI2020_dbf.zip` — **verificados presentes**.

Se descartó `cal_conf_faseb_pos4.py` como candidata: su medición tiene un
rótulo de constructo corregido después (`forense/hallazgos.md`,
2026-08-04, línea sobre `BP1_20`/`BP1_23`/`BP1_28`) — el número no está
cuestionado, pero se prefirió una candidata sin historial de corrección
para no mezclar la validación del estimador con una discusión de rótulo
ajena a este acto.

**PE-3.** `prop_ultimate_cluster` leído completo (34 líneas de cuerpo,
`tests/svystat.py:34-86`) antes de diseñar el caso sintético — la fórmula
de la sección "1" de abajo es la que el módulo implementa, no una
paráfrasis.

Las tres premisas se sostienen. No hay PARO de premisas.

## 2 · Los tres resultados

### 2.1 · Caso sintético — el que valida

Dataset construido en este acto (no existía antes): 2 estratos, 5 UPM (3
en A, 2 en B), pesos y conteos de fila desiguales, ninguna UPM con una
sola fila — la combinación que `_caso_conocido` no ejercita. Derivación
completa a mano (fracciones exactas, denominadores potencia de 2 por
construcción — sin redondeo que esconda un error) en el docstring de
`test_caso_sintetico_dos_estratos()`, `tests/test_svystat.py`. Resumen:

```
p_hat esperado (19/32)        = 0.593750000000
se esperado   (sqrt(313/262144)) = 0.034554308619

p_hat calculado = 0.593750000000  -- coincide
se calculado    = 0.034554308619  -- coincide, 12 decimales
n_estratos=2 · n_upm_total=5 · n_estratos_singleton=0  -- los tres esperados
```

**Coincide exacto.** Segundo caso, barato, adyacente: un estrato de una
sola UPM (tres filas, pesos desiguales, p_hat=0.5 a mano) confirma que el
estimador excluye esa UPM de la varianza y lo **marca**
(`n_estratos_singleton=1`, `se=0.0` — no un `NaN`, no una excepción, no
un cero indistinguible de precisión real). Detalle en
`test_estrato_singleton()`, mismo archivo.

### 2.2 · Reproducción — Hito D R7.2, ocho olas

Re-corrido `tests/hitoD_r7_2_ocho_olas.py` **tal cual está commiteado**,
sin ninguna modificación, en `mm-hitoD-r7-2` (HEAD `eac2a57`, su propio
`data/raw` ya apuntaba a la misma raíz compartida):

```
$ python3 tests/hitoD_r7_2_ocho_olas.py
...
  asegurado: n=402 p=79.1% se=2.15pp IC95=[74.9%,83.3%]
  no_asegurado: n=614 p=67.2% se=1.77pp IC95=[63.7%,70.7%]
  BRECHA = 11.9pp se=2.79pp IC95=[6.4pp,17.4pp]
  REPRODUCE 11.9pp IC[6.4,17.4]: SI
  identificabilidad asegurado: n=121 %conocido=1.5% IC95=[0.4%,2.5%]
  identificabilidad no_asegurado: n=124 %conocido=5.1% IC95=[4.0%,6.2%]
...
  asegurado: n=858 n_pond=546709 p=81.2% se=1.50pp n_estratos=516 singleton=381 (74%)
  no_asegurado: n=800 n_pond=403843 p=63.7% se=1.62pp n_estratos=588 singleton=468 (80%)
  BRECHA (DESCONOCIDO) = 17.5pp se=2.21pp IC95=[13.2pp,21.9pp]  -- CRUZA 20
```

**Coincide exacto, dígito por dígito, en el 100% de lo que el script
imprime** — no solo el control de 2025 (que trae su propio assert
interno, `REPRODUCE 11.9pp IC[6.4,17.4]: SI`), sino también §2
(comparabilidad año×variable: `n_EST_DIS` de las ocho olas, 593, 231,
603, 598, 604, 604, 601, 739) y §3 agrupado (n por año y celda,
n ponderado, ambos estratos de identificabilidad, ambas brechas) contra
`forense/notas/2026-08-04-r7-2-ocho-olas.md` §3 y §5 completos. Cero
discrepancias. (La cifra de contexto "11.7pp marginal" de la nota §5 no
la produce este script — no la calcula, así que no es parte de esta
reproducción.)

### 2.3 · Reproducción — CAL-CONF Fase B, segunda ola

**Hallazgo adyacente antes del resultado**, ver §3 abajo: el script
commiteado (`tests/cal_conf_faseb_ola2.py:91-95`) extrae dos `.dbf` a una
ruta absoluta de scratch de otra sesión
(`/tmp/claude-1000/-home-pc0/61e9e624.../scratchpad/encuci_ola2`), que no
existe en este entorno y está fuera de lo que este sandbox puede escribir.
**No se editó el archivo commiteado.** Se corrió una copia en el propio
scratch de esta sesión, con `cp` + `sed` (nunca tecleada a mano), con
**solo esas 4 líneas** sustituidas — diff completo, mostrando que nada
más cambió:

```diff
91,92c91,92
<     z.extract("ENCUCI_2020_SD.dbf", ".../61e9e624.../scratchpad/encuci_ola2")
<     z.extract("ENCUCI_2020_SEC_4_5.dbf", ".../61e9e624.../scratchpad/encuci_ola2")
---
>     z.extract("ENCUCI_2020_SD.dbf", ".../bd56b188.../scratchpad/encuci_ola2_extract")
>     z.extract("ENCUCI_2020_SEC_4_5.dbf", ".../bd56b188.../scratchpad/encuci_ola2_extract")
94,95c94,95
< SD_PATH = ".../61e9e624.../scratchpad/encuci_ola2/ENCUCI_2020_SD.dbf"
< SEC45_PATH = ".../61e9e624.../scratchpad/encuci_ola2/ENCUCI_2020_SEC_4_5.dbf"
---
> SD_PATH = ".../bd56b188.../scratchpad/encuci_ola2_extract/ENCUCI_2020_SD.dbf"
> SEC45_PATH = ".../bd56b188.../scratchpad/encuci_ola2_extract/ENCUCI_2020_SEC_4_5.dbf"
```

Corrido desde la raíz del repo (`import svystat`/`import dbfmini` cargan
los módulos reales de `tests/`, no una copia):

```
OK -- caso conocido (SRS, n=200, k=80, PSU=persona): ... Coincide a 9 decimales. Validado.
n_filas=21519 no_respuesta=1483 sin_cruce=1265 utiles=18771  (assert interno del script -- pasó)
  ('Formal', '18-29'): n=1035 p=82.4% se=1.41pp
  ... (8 celdas, todas coinciden)
Guardia Nacional (`AP5_4_04`): identifica=71742 (78.7%) · no identifica/NS=19440 · sin respuesta=911
  18-29 | 16620 | 82.2% | 0.43pp | [81.4%, 83.1%] |
  ... (135 celdas y cabeceras más, FFAA + justicia-policía + electoral-partidos)
```

**Verificado el conjunto completo de §2-§3 de
`forense/notas/2026-08-03-cal-conf-faseb-medicion-ola2.md`** (líneas
269-625): las 4 cifras + 8 celdas de la validación de pipeline (§2), y
las 15 fichas de §3 (4 seguridad-FFAA + 7 justicia-policía + 4
electoral-partidos) — 121 celdas de tabla (n, %, SE, IC95 lo/hi) más 15
líneas de cabecera (identifica/no-identifica/sin-respuesta o
no-respuesta/sin-cruce/útiles según la ficha). **Cero discrepancias en
ninguna** — incluida la celda más fría del acto, Diputados locales
Formal×60+ (n=215, se=8.89pp, IC95=[12.3%,47.2%], señalada como frágil en
la nota original), que reproduce exacta.

## 3 · Hallazgo — ruta de scratch ajena en script commiteado

`tests/cal_conf_faseb_ola2.py:91-95` fija una ruta absoluta de
`/tmp/claude-1000/.../scratchpad/` de la sesión que lo escribió
(03/ago/2026). Cualquier sesión nueva que lo corra tal cual falla en
`zipfile.ZipFile.extract` (`FileNotFoundError`, directorio inexistente) o,
si el sandbox lo permite, escribe fuera de su propio scratch. No impide
medir — se reprodujo igual, con la sustitución declarada en §2.3 — pero
es un defecto de portabilidad real, no hipotético: esta sesión lo pisó al
primer intento. **No se corrige aquí** (fuera de perímetro de E-3: el
encargo prueba `svystat.py`, no repara otros scripts); línea en
`forense/hallazgos.md`.

## 4 · Qué no se hace aquí

- No se modifica `tests/svystat.py` — se prueba, no se toca. Los tres
  casos de §2 pasan contra el código tal como está.
- No se modifica `tests/cal_conf_faseb_ola2.py` ni ningún archivo de
  `mm-hitoD-r7-2` — ambas reproducciones corren contra el committeado, o
  contra una copia de scratch con la única sustitución declarada en §2.3.
- `tests/test_svystat.py` **no se cablea a `check.py`** — corre solo
  (`python3 tests/test_svystat.py`, exit 0). Volverlo obligatorio es
  decisión de mesa aparte (instrumento sobre instrumento).
- No se toca `canon/estado-programa` ni `canon/modelo-decision` — este
  acto no mide ninguna condicional ni ficha de Hito D, no hay contador
  que mover.

## 5 · Desenlace

**Los tres casos coinciden. El estimador queda respaldado por caso
conocido, no solo por autochequeo degenerado y por reproducibilidad de
sí mismo.** Ningún PARO. La capa medida que depende de `svystat.py`
(CAL-CONF Fase B, Hito D R7.2, y cualquier condicional en curso que lo
use) no pierde nada si este acto no encuentra nada — y no encontró nada
en el estimador. Lo único que encontró es el hallazgo de portabilidad de
§3, ajeno al estimador mismo.
