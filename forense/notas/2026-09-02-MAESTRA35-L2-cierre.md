# ACTO MAESTRA35-L2 · R-v1_2-COMPLETA — nota de cierre

Encargo: `forense/encargos/2026-09-02-MAESTRA35-L2-R-v1_2-COMPLETA.md`
(dirección/Fable, maestra-35, formato corto v2.12, SHA de redacción `11af678`,
archivado por A.3 en `c685ffb`). Entorno UBUNTU, caja con corpus, worktree
propio `/home/pc0/mm-maestra35-l2`, rama `acto/maestra35-l2-r-v1_2-completa`.
Base real: `b6b923f`. Skills `/acto` (`ADR-237`) y `/arbitra`.

## 0 · Declaración de contaminación — las 4 celdas del lote quedan fuera

**Esta sesión vio cifras `p`/`M` del motor para las cuatro celdas que venía a
arbitrar.** Se declara primero, como manda el encargo y como hizo el precedente
que él mismo cita (`MAESTRA34-L2 §0`), porque decide el alcance del acto.

**Por dónde, y por qué no se pudo evitar.** No por abrir un archivo prohibido:
la lista ciega del encargo (`milpa/tramite.yaml`, `milpa/tramite-ola5-propuesta-v0.yaml`,
`milpa/procedencia.yaml`, `corridas-M/`, `corridas-L/`, `scoreboard*`,
`L-extraido*`, encargos y notas de `MAESTRA34-L1/L5/N1/N4/N9` y de
`MAESTRA35-N1/L1`) se respetó íntegra — ninguno de esos archivos se abrió, ni
«para confirmar». Las cifras venían dentro de dos archivos que el propio
procedimiento obliga a abrir:

1. **`forense/prereg-duelo-v2/marco-M-sorteado-v1_2.tsv`, columna `razon_DD`.**
   `/arbitra §COMMIT-1` — y el encargo, literalmente — exigen copiar la fila del
   marco **verbatim** para congelar la spec. Esa columna trae la cifra `p` que
   el motor emite para la celda, en prosa.
2. **`canon/gobernanza-v1_15.md`.** La cascada de cierre de `/acto` obliga a
   editarlo (ADR, cabecera de conteo). La entrada `ADR-289` cita `p` verbatim de
   varias reglas del motor, entre ellas la de las celdas `CIV-M-*` del mismo
   marco.

**Radio medido, con los valores enmascarados en el propio comando** (barrido de
las 14 filas × 32 columnas del marco, detector de cifras con forma de `p`):

```
filas examinadas: 14   columnas examinadas: 32
FAM-M-05   razon_DD    1   <0.XXXXXX>
FAM-M-06   razon_DD    1   <0.XXXXXX>
FAM-M-07   razon_DD    1   <0.XXXXXX>
TRA-M-02   razon_DD    1   <0.XXXXXX>
TOTAL de cifras tipo p incrustadas en el marco: 4
CELDAS AFECTADAS: 4 de 14 -> FAM-M-05 FAM-M-06 FAM-M-07 TRA-M-02
```

Las **cuatro celdas contaminadas son exactamente las cuatro que este acto venía
a arbitrar**; las otras diez del marco están limpias. No es coincidencia: son
las únicas que aún no tenían `R`, y por eso son las únicas cuya fila alguien
tuvo que razonar en prosa sobre `F-DD`.

Ninguna de esas cifras se transcribe en esta nota ni en ningún archivo que este
acto escribe: ya están en el repo una vez, y copiarlas las multiplicaría.

**Consecuencia aplicada, verbatim de la regla del encargo** («la celda afectada
queda fuera de lote»): **`FAM-M-05`, `FAM-M-06`, `FAM-M-07` y `TRA-M-02` no
entran en ningún lote de esta sesión.** No se calculó `R` para ninguna, no se
escribió ningún `corridas-R/*.json`, no se escribió la fila de codificación de
`TRA-M-02` — escribir esa codificación es el paso contaminable (define universo
y dicotomización), no sólo el cálculo, tal como lo estableció `MAESTRA34-L2`.
`COMMIT-1` del lote **no se escribió**: congelar la spec de un lote que no
existe habría parecido que el lote siguió.

**Decisión de mesa (2/sep/2026), consultada antes de escribir nada
irreversible.** Se le presentó a mesa el hallazgo con tres alcances posibles y
eligió: *regla literal + proyección ciega* — las cuatro fuera de lote, y se
autoriza a este acto a construir el instrumento que faltaba (§3). La consulta
se hizo **antes** de escribir cualquier `corridas-R/*.json` a propósito:
`produce()` **nunca sobreescribe** un JSON existente, así que un `R` escrito por
error habría quedado clavado y ninguna sesión limpia posterior habría podido
recalcularlo sin borrar archivos.

## 1 · ARRANQUE y compuerta

| paso | valor |
|---|---|
| 1 · REPO | `/home/pc0/mm-maestra35-l2`, worktree nuevo sobre el clon existente (no se clonó). `b6b923f` · working tree limpio. El clon principal estaba parado en otra rama (`L/corridas-v1_2`), condición normal. |
| 2 · SHA | Encargo declara `11af678`; base real `b6b923f`, **2 merges por delante** (`PR #468` `MAESTRA34-L6`, `PR #469` `MAESTRA35-N1`). No es PARO: perímetro y contadores re-derivados. |
| 3 · `data/raw` | Ausente al nacer el worktree (gitignorada). **Enlazada** a `/home/pc0/mm-corpus/raw`: 370 payloads. |
| 4 · ENTORNO (A.2, tres partes) | `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `sin_variable` · `curl https://www.inegi.org.mx/` → `200` · `ls data/raw/ \| head -1` → `2005trim1_csv.zip`, **no vacío ⇒ firma de entorno CUMPLIDA**. |
| 5 · ESPEJO | Toda cifra de esta nota sale de este clon, con el comando a la vista. |

`COMPUERTA: ninguna` — declaración explícita del encargo, no dispara
verificación (`/acto §2`).

## 2 · P1 · reparación acotada de la herramienta — HECHA (commit `ca9a08c`)

Cuatro piezas, todas en `tools/arbitra.py` salvo una línea de lógica en
`corridas-R/correr-R.py`:

- **(a) UMBRAL.** `_PATRON_UMBRAL` + `_predicado_umbral()`: `y=1 si VAR > K;
  y=0 si VAR == K`. `>`/`>=`/`<`/`<=`/`==` se aplican exactamente como estén
  escritos. Vacío o no numérico → `n_codigo_no_valido`, nunca `0` ni `1`.
- **(b) COMPUESTO OR de dos variables.** `_PATRON_COMPUESTO_OR` +
  `_predicado_compuesto_or()`. Cualquier combinación distinta queda fuera.
- **(a)(b) mecanismo.** `parsea_codificacion_binaria()` intenta en orden
  `BINARIO → SET → UMBRAL → COMPUESTO` y devuelve un **callable** para los dos
  nuevos (par de conjuntos para los dos viejos). `estima()` gana
  `codifica=None`: con `None`, el camino de conjunto queda **byte a byte** como
  estaba. El orden de intento es lo que garantiza que nada que ya calzaba
  cambie de rama — y se midió, no se supuso.
- **(c) lector por CONTENIDO.** `.dbf → dbf_zip`, `.csv → csv_zip`, cualquier
  otro sufijo → `NO-EJECUTABLE-LECTOR-AUSENTE` declarando el sufijo real, y el
  lote sigue. Antes, **todo lo que no fuera `.dbf` caía en `csv_zip()`**: un
  miembro `.dta` se leía como CSV y producía una cifra sin sentido en vez de
  una abstención. No se añadió lector `.dta` (fuera de alcance).
- **(c) captura por celda.** `produce()` envuelve cada celda en `try/except`:
  la excepción se registra en el JSON de esa celda (`estado: ERROR`, traza
  corta) y el lote **sigue**. Antes una sola celda tumbaba la corrida entera.

**Controles, los tres con control positivo:**

- **A · barrido completo**, parser viejo (`git show HEAD:tools/arbitra.py`)
  contra nuevo, sobre **las 34 filas** de `codificacion-R-v1_0.tsv`:
  27 idénticas de conjunto · 4 idénticas `None` (siguen absteniéndose) ·
  **3 ahora CALLABLE** (`FAM-M-05/06/07`, antes `None`) · **0 cambios de rama
  indebidos**.
- **B · 20 casos unitarios sintéticos** de los dos predicados (umbral:
  positivo, `0`, `0.00`, vacío, no numérico, columna ausente, negativo;
  compuesto: las cuatro combinaciones válidas más `9`/vacío/ausente; el camino
  de conjunto sigue devolviendo par; `estima(codifica=None)` contra
  `estima(codifica=<equivalente>)` da `R`, `EE` y conteos idénticos):
  **20 de 20 OK, 0 fallos**.
- **C · regresión P1(d)**, `--regresion`, sin escribir nada:
  **12 de 12 COINCIDE**, `exit 0`.

| celda | R recalculado == existente | n_efectivo |
|---|---|---|
| `DIN-11` | `0.4583913965555015` | 12446 |
| `SFT-04` | `0.0604055335123943` | 10103 |
| `TIC-08` | `0.9044714694763597` | 47240 |
| `CIV-M-01` | `0.25899878251638075` | 26848 |
| `CIV-M-02` | `0.24339981393062482` | 40889 |
| `CIV-M-04` | `0.24366832225578466` | 39286 |
| `CIV-M-10` | `0.20493399286059008` | 32967 |
| `CIV-M-12` | `0.20811159524290274` | 31012 |
| `CIV-M-13` | `0.1946118021509308` | 33108 |
| `FAM-M-01` | `0.5571925669683186` | 12054 |
| `TRA-M-03` | `0.04453797671500066` | 22081 |
| `TRA-M-07` | `0.07181522879909936` | 39763 |

El encargo pedía la regresión de las 3 del precedente «y además contra las 9 R
ya computadas del sorteado v1_2 (si `--regresion` acepta esos ids)». **Sí las
acepta** — las nueve tienen fila en `codificacion-R-v1_0.tsv` — así que la
regresión se extendió a las doce.

**La misma regresión se corrió contra el árbol SIN parchar, antes de editar una
sola línea, y también daba 12 de 12.** Sin ese control previo, un «12 de 12»
posterior no distinguiría «la reparación no movió nada» de «la regresión no
mide nada».

**Orden verificable en git:** `ca9a08c` (P1, con su regresión) es **anterior**
al commit en que esta sesión leyó el marco contaminado. El único grado de
libertad que esta sesión tenía sobre el estimador quedó sellado antes de la
exposición.

## 3 · El hallazgo, y el instrumento que sale de él (commit `db69b98`)

**El defecto no es de un ejecutor descuidado: es del procedimiento contra el
artefacto.** `/arbitra COMMIT-1` exige la fila del marco verbatim; el marco
trae `p` en `razon_DD`; luego **ninguna sesión ciega puede congelar la spec de
estas cuatro celdas sin ver `M`**. Ejecutar el encargo al pie de la letra y
contaminarse son el mismo acto. Un ejecutor «más cuidadoso» no lo evita, y el
sucesor chocaría con el mismo muro.

Autorizado por mesa, este acto construye la salida:
`tools/arbitra.py --proyecta-ciego` y su producto
`forense/prereg-duelo-v2/espec-R-ciega-v1_2.tsv`.

- **LISTA BLANCA de 14 columnas**, no lista negra: una columna nueva en una
  versión futura del marco queda **fuera por omisión**, no dentro por descuido.
  Conservadas: `id encuesta ola universo variable estimador ponderador escala
  cv_arbitro n_no_ponderado dominio en_corpus elegible elegible_v1_1`.
  Descartadas: las 18 de prosa y grado del lado `M`, incluidas `razon`,
  `razon_DD` y `publicada`.
- **`publicada` sale aunque hoy esté vacía**: es la cifra contra la que se
  compara `R`, y el árbitro no la necesita para medir.
- **`estrato` sale**: en este marco es la etiqueta compuesta
  `dominio|grado|dificultad`, no una variable de diseño — el propio docstring
  de `arbitra.py` lo advierte. El diseño real vive en `codificacion-R-v1_0.tsv`.
- **Generado por código, nunca a mano.**

Salida cruda del generador (`exit 0`):

```
sha256_marco : 98d34f64be8c1e84b774fe1df52d76360602ca743c6364af36e79f12085ce33c
filas: 14   columnas_origen: 32   conservadas: 14   descartadas: 18
control_positivo_cifras_en_marco: 4
control_positivo_celdas: ['FAM-M-05','FAM-M-06','FAM-M-07','TRA-M-02']
control_positivo_columnas: ['razon_DD']
filas_escritas: 14   campos_examinados_tras_escribir: 196
cifras_de_motor_en_la_salida: 0
sha256_salida: b2dacd8a4f66ccb29eb97e448c2d0e9cf1b70002669d0c5770a49def061beb53
VEREDICTO: PROYECCION CIEGA ESCRITA
```

Verificada en tres frentes, no en uno:

1. **Consumible por el propio árbitro, sin adaptador.** `lee_marco()` devuelve
   14 filas con las 14 claves; `_encuesta_ola_del_marco()` resuelve
   `FAM-M-05 → ('ENIGH','2016')`, `FAM-M-07 → ('ENIGH','2020')`,
   `TRA-M-02 → ('ENCUCI','2020')`, `CIV-M-01 → ('ENVIPE','2012')`.
2. **La guardia PARA de verdad** (negativo con control positivo y código de
   salida): alimentarle la proyección ya limpia da `CONTROL POSITIVO FALLIDO`,
   `exit 1`, y el archivo de salida **no existe** (`ls: No such file or
   directory`). El generador también **relee del disco** lo que escribió — no
   declara limpio lo que tenía en memoria — y si aparece residuo, borra la
   salida y sale `1`.
3. **Regresión intacta tras el cambio**: `DIN-11`/`SFT-04`/`TIC-08` COINCIDE,
   `exit 0`.

## 4 · P2 y P3 — fuera de lote, con razón

- **`FAM-M-05` / `FAM-M-06` / `FAM-M-07`** (ENIGH 2016/2018/2020 NS,
  `concentradohogar`, umbral sobre `remesas`): **fuera de lote por §0**. Su
  codificación ya estaba escrita y verificada contra microdato por
  `MAESTRA34-L2`, y la herramienta que las bloqueaba ya está reparada (§2): lo
  único que falta es una sesión que no haya visto su `M`.
- **`TRA-M-02`** (ENCUCI 2020, `SEC_4_5`, compuesto `AP5_17`/`AP5_18`):
  **fuera de lote por §0**, segundo acto consecutivo — `MAESTRA34-L2` ya la
  dejó fuera por la misma cifra, vista entonces por otra vía. Su codificación
  **no se escribió**. Tampoco se verificaron los códigos del FD
  (`encuci2020_fd_pdf`): esa verificación es parte del paso contaminable y le
  toca a la sesión limpia, con la spec ciega en la mano.

**Las cuatro son ejecutables el día que las corra una sesión limpia**: el
bloqueo que las mantenía sin `R` era de herramienta (§2) y ya no existe. Lo que
queda es un requisito de higiene de sesión, no de dato ni de código.

## 5 · Contador — el real, no el planeado

| contador | encargo planeaba | real |
|---|---|---|
| celdas del sorteado v1_2 con `R` | 9 → 13 | **9 → 9** (las 4 fuera de lote, §0) |
| dominio familia con `R` | 1 → 4 | **1 → 1** |
| dominio trámite con `R` | 2 → 3 | **2 → 2** |
| celdas puntuables por N3/N5 con `L∩M∩R` | +4 | **+0** |
| reparación de herramienta | 1, con regresión 3 de 3 | **1, con regresión 12 de 12** |
| instrumento nuevo | — | **1** (proyección ciega, autorizada por mesa) |
| hallazgos | 0 planeados | **2** (`FP-243`, `FP-244`) — **ambas FIRMADAS por mesa el mismo día** (§10) |

El «9» de partida se censó por comando, no se heredó: `for id in $(grep -v "^#"
marco-M-sorteado-v1_2.tsv | cut -f1 | tail -n +2); do ls corridas-R/$id.json;
done` → existen 9, faltan 5 (las 4 del lote + `DIN-M-01`, excluida por `DF-a`).
Coincide con lo que el encargo declaró. **El tablero y `ADR-277` dicen «R 11 →
14»: ese conteo cuenta filas de codificación escritas, no `R` computadas.** Se
declara la diferencia; corregir el tablero no es de este acto.

## 6 · Archivos que esta invocación abrió (lo manda `/arbitra`)

**Abiertos:** `.claude/commands/acto.md` · `.claude/commands/arbitra.md` ·
`forense/prereg-duelo-v2/marco-M-sorteado-v1_2.tsv` (obligado por COMMIT-1;
**vía de contaminación 1**) · `forense/prereg-duelo-v2/codificacion-R-v1_0.tsv`
· `tools/arbitra.py` · `forense/prereg-duelo-v2/corridas-R/correr-R.py` ·
`forense/prereg-duelo-v2/corridas-R/*.json` (por `--regresion`, sólo lectura,
12 celdas) · `data/manifiesto.yaml` y los zips de `data/raw/` (leídos por la
herramienta durante la regresión) ·
`forense/notas/2026-09-01-MAESTRA34-L2-ARBITRA-v1_2-cierre.md` (el precedente
que el encargo cita; **no** está en la lista ciega) ·
`forense/firmas-pendientes.tsv` y `forense/hallazgos.md` (sólo estructura y
numeración) · `canon/gobernanza-v1_15.md` (**vía de contaminación 2**) ·
`canon/estado-programa-v1_10.md` · `canon/registro-rotulos.tsv` ·
`.claude/commands/arbitra.md` y `.claude/commands/acto.md` (**perímetro
ampliado por la respuesta de mesa**, §10).

**Entró por el merge de `origin/main` sin abrirse:**
`milpa/tramite-ola5-propuesta-v0.yaml` llegó modificado por `PR #473`. El merge
lo resolvió solo; **ninguna línea suya se leyó ni se editó en esta rama** — es
de la lista ciega y sigue sin abrirse.

**NO abiertos, ni «para confirmar»:** `milpa/tramite.yaml` ·
`milpa/tramite-ola5-propuesta-v0.yaml` · `milpa/procedencia.yaml` · ningún otro
archivo de `milpa/` · `forense/prereg-duelo-v2/corridas-M/` · `corridas-L/` ·
`scoreboard*` · `L-extraido*` · ningún encargo ni nota de `MAESTRA34-L1`,
`MAESTRA34-L5`, `MAESTRA34-N1`, `MAESTRA34-N4`, `MAESTRA34-N9`,
`MAESTRA35-N1` ni `MAESTRA35-L1`.

## 7 · Numeración, re-derivada al arrancar

- **ADR.** Comando de la casa → máximo `289` en `b6b923f`; candidato **`290`**,
  contiguo y sin huecos. **Colisión confirmada por mesa**: `PR #471`
  (`ACTO MAESTRA35-L1`) reclama el mismo `ADR-292` y los mismos `FP-243`/`FP-244`.
  **Desenlace: tocó renumerar, y no por `PR #471`.** Mientras esta sesión
  trabajaba fusionó `PR #473` (`ACTO MAESTRA35-N3 · SELLA-CIVICA-L6`) y tomó
  `ADR-290`. Re-derivado contra `origin/main` = `fb3aa8e`: máximo real de ADR
  **`290`**, candidato contiguo **`291`** → **`ADR-290` → `ADR-292`** en las
  **13** ocurrencias, ninguna de las cuales venía de la base (verificado
  archivo por archivo con `git show b6b923f:<f> | grep -c`). `FP-243`/`FP-244`
  siguen **libres** en `fb3aa8e` (máximo de FP `240`) y se conservan; `PR #471`
  sigue `OPEN` reclamándolos — si fusiona primero, se renumeran igual. Regla de
  la casa: **renumera quien fusiona segundo**, y aquí tocó.
- **FP.** Máximo registrado en `forense/firmas-pendientes.tsv` = **`240`**
  (230 ids examinados, control positivo). El encargo pre-asignó `FP-244..246`
  pero ordenó «re-deriva el máximo al arrancar … toma el primer libre y dilo»:
  el primer libre es **`241`**, y se toman **`FP-243`** y **`FP-244`**.
  `MAESTRA35-N1` ya consumió el `240` que el encargo reservaba a
  `MAESTRA35-L1`; quien redacte `L1` re-deriva.

## 8 · Sucesores declarados, no lanzados

1. **CAJA · `MAESTRA35-L4 · R-v1_2-CIEGA`** — arbitra las cuatro
   (`FAM-M-05/06/07`, `TRA-M-02`) desde `espec-R-ciega-v1_2.tsv`, **sin abrir
   `marco-M-sorteado-v1_2.tsv` ni `canon/gobernanza-v1_15.md` durante el
   lote**. La herramienta ya no la bloquea. Requisito de higiene: sesión nueva
   que no haya visto `M`; la cascada de cierre (que sí obliga a tocar
   `gobernanza`) va **después** de escribir los `R`, nunca antes.
2. **Los tres sucesores que el encargo ya traía**, intactos: (i) NUBE,
   `F-DD` a rangos de ola en `tools/emite_m.py` para emitir `M` de `DIN-M-01`;
   (ii) CAJA, `R` de `DIN-M-01` con lector `.dta` + join `fac_3b`, sólo con (i)
   fusionado; (iii) `N3` re-corrido o `N5` leyendo las `R` nuevas — lo decide
   `/despacha` por producto.
3. **Higiene de la cascada** (de `FP-244`): que `/acto §CIERRE` no obligue a una
   sesión ciega a leer `p` del motor. Es cambio de regla operativa: se acumula
   en `hallazgos.md` bajo `PARA-v2.13`, no se edita
   `instrucciones-proyecto-v2_12.md` acto por acto.

## 9 · Lo que este acto NO hizo

No calculó ninguna `R`. No escribió ningún `corridas-R/*.json`. No escribió la
codificación de `TRA-M-02`. No re-computó ninguna `R` existente. No arbitró
`DIN-M-01` (`DF-a`) ni añadió lector `.dta`. No tocó `milpa/`, `corridas-M/`,
`corridas-L/`, scoreboards, `marco-M-*`, `data/manifiesto.yaml` ni `data/raw`.
No corrigió el «R 11 → 14» del tablero. No editó
`instrucciones-proyecto-v2_12.md`.

## 10 · Respuesta de mesa (2/sep/2026) — propagada, no decidida

Mesa contestó los dos hallazgos el mismo día. Firmas verbatim en
`forense/firmas-pendientes.tsv`; aquí lo que se ejecutó:

1. **`FP-243` → `FIRMADA`, opción `a`.** «la proyección ciega es el insumo
   obligatorio del lado R. `/arbitra §COMMIT-1` se redacta contra
   `espec-R-ciega-<v>.tsv` … nunca contra el marco sorteado. El marco sellado
   NO se toca; `razon_DD` se queda como está, es historia.» Ejecutado: enmienda
   fechada al principio de `§COMMIT-1` en `.claude/commands/arbitra.md`, **una
   sola vez**, verificada por `grep` antes de escribir — 0 ocurrencias previas,
   con control positivo del propio `grep` (`COMMIT-1` aparece 5 veces en ese
   archivo, así que el 0 no viene de un comando que no examinó nada).
2. **`FP-244` → `FIRMADA`**, basta la mitigación de oficio y se escribe:
   línea nueva en `§CIERRE` de `.claude/commands/acto.md` — «la cascada corre
   **después** de commitear `corridas-R/*.json`; nunca antes». Mismo control:
   0 previas, `CIERRE` aparece 2 veces (control positivo).
3. **Rótulo del sucesor corregido: `MAESTRA35-L3` → `MAESTRA35-L4 ·
   R-v1_2-CIEGA`.** `MAESTRA35-L3` ya es de `CIVICA-TIPO-DE-BOLETA`
   (dirección, 2/sep/2026), que este acto **no** censa porque no es suyo.
   Renombrado en las **9** ocurrencias, en 7 archivos, verificado por conteo
   (`MAESTRA35-L3` → 0, `MAESTRA35-L4` → 9). El cuerpo verbatim del encargo
   (líneas 1–31) quedó intacto: la única ocurrencia en ese archivo estaba en la
   sección `## CONSUMIDO`, que es de este acto, y una aserción lo comprobó
   antes de escribir. **El encargo de `MAESTRA35-L4` lo redacta dirección, no
   el ejecutor de este acto.**
4. **La corrección «R 11 → 14 son 9 computadas» se queda como se declaró**
   (§5), por instrucción de mesa.

**Perímetro ampliado por esta respuesta, y declarado:** `.claude/commands/arbitra.md`
y `.claude/commands/acto.md` no estaban en el perímetro del encargo original;
entran por instrucción explícita de mesa (punto 4-i de su respuesta). Ningún
otro archivo se sumó.

**Lo que mesa confirmó que este acto NO hace:** no arbitra — esta sesión ya vio
`p` —; no toca el marco ni `codificacion-R-v1_0.tsv`. **La fila de `TRA-M-02`
la escribe `MAESTRA35-L4` en ciego.**

5. **Renumeración, ejecutada.** Mesa avisó que `PR #471` competía por
   `ADR-290`/`FP-243`/`FP-244`. Quien fusionó primero fue otro: `PR #473`
   (`MAESTRA35-N3`) tomó `ADR-290` durante la sesión. Re-derivado y renumerado
   a **`ADR-292`**; los dos `FP` se conservan porque siguen libres. El merge de
   `origin/main` = `fb3aa8e` dejó **291 ADR únicos, máximo 291, cero
   duplicados** — el defecto que la casa ya midió (un merge limpio puede dejar
   dos `**ADR-N` iguales) se comprobó por comando, no a ojo.

   La línea `L0` (**89 288 caracteres en una sola línea**) **no** se resolvió
   por sufijo común: el primer intento lo hizo así y una aserción lo atrapó
   **perdiendo una anotación**, porque el sufijo común a nivel de carácter
   cortaba *dentro* de una anotación — las dos ramas encadenan con separadores
   distintos (`)* *(` aquí, `), ` en `N3`). Se resolvió anclando en
   `` `ADR-289` (derivado por el comando ``, el punto exacto donde las dos
   ramas vuelven a ser idénticas (87 251 caracteres de cola, comparados byte a
   byte antes de tocar nada). Control final: anotaciones `mia=57 suya=57
   cola=56 resultado=58 = 57+57−56`, y `ADR-292`/`ADR-290`/`ADR-289` abren
   **una** anotación cada uno.

**Suite sobre el árbol fusionado** — `python3 tests/check.py --baseline` →
**LÍNEA BASE VERDE**, `exit 0`, núcleo **19 FAIL · 166 WARN**. Base `fb3aa8e`
medida en worktree separado: **19 FAIL · 166 WARN**. **Delta de este acto: 0
FAIL, 0 WARN** — los `+2 WARN` que había abierto desaparecieron al pasar
`FP-243`/`FP-244` de `ABIERTA` a `FIRMADA`.
