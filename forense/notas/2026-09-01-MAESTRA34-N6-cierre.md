# `ACTO MAESTRA34-N6 · CURADOR-Y-SUITE` — cierre

Encargo archivado (A.3):
`forense/encargos/2026-09-01-MAESTRA34-N6-CURADOR-Y-SUITE.md`.
SHA de redacción `3c3ab3a` (merge `PR #454`); base real del acto `e4af4ed`
(merge `PR #455`), que es `origin/main`. `3c3ab3a` es ancestro de `e4af4ed` y
el diff entre ambos sólo añade archivos de encargo: **cero deriva en el
perímetro de este acto**. Entorno **NUBE**
(`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` = `cloud_default`), `data/raw` **ausente**
y corpus **no montado** — esperado y declarado por el propio encargo, no un paro.
**COMPUERTA: ninguna** (archivado por `PR [COLA]` fusionado por mesa = firma).

Firmas de mesa que rigen, verbatim 1/sep/2026: *«DT - Revisa bien el repo y
asegurate de que efectivamente los payloads ya los vigila el manifiesto con sha,
si es así entonces A. DN-a. DS-a.»* La condición de DT se verificó contra el
árbol antes de ejecutar (§1). El ejecutor propaga, no decide (`SELLA-3`).

---

## CONTADOR

| magnitud | antes | después |
|---|---|---|
| tests utilizables en caja | 0 | **1** (`T27`) |
| necesidades en `necesidad-objeto-modelo.tsv` | 40 filas / `N35` | **41 filas / `N36`** (+1) |
| relaciones en `relaciones.tsv` | 199 | **204** (+5) |
| procedencias en `evidencias.tsv` | 200 | **205** (+5) |
| filas de `utilidad-modelo.tsv` | 199 | **204** (+5) |
| fusiones declaradas | 1 | **1** (sin cambio) |
| firmas ejecutadas | — | **2** (`FP-229`, `FP-230`) |
| estimaciones | — | **0** |

**A.13 — filas tocadas por tabla** (contadas sobre el diff, no tecleadas):

| tabla / archivo | filas nuevas | filas modificadas |
|---|---|---|
| `data/curacion-registro/necesidad-objeto-modelo.tsv` | 1 (`N36`) | 0 |
| `data/curacion-registro/relaciones.tsv` | 5 | 0 |
| `data/curacion-registro/evidencias.tsv` | 5 | 0 |
| `data/curacion-registro/utilidad-modelo.tsv` | 5 | 0 |
| `data/curacion-registro/baseline.json` | — | recifrado (7 `sha256` + 6 conteos + `procedencia.origen`) |
| `forense/firmas-pendientes.tsv` | 0 | 2 (`FP-229`, `FP-230` → `EJECUTADA`) |
| `tests/baseline.json` | — | recongelado (`HEAD` `c6a0d72` → `e4af4ed`) |
| `forense/hallazgos.md` | 1 | 0 |
| `tests/check.py` | +24 líneas, sólo `t27_infraestructura()` | `_T_INFRA_ARCHIVOS_CONOCIDOS` **sin tocar** |
| `data/INFRAESTRUCTURA-v1_0.md` | 0 | 1 celda (D1) |
| `tools/curador_registro/GUIA-CURADOR-REGISTRO.md` | 1 sección nueva | 0 |

---

## 1 · `P1` — `T27` exenta `data/raw/**` (`FP-229`, firma `DT-a`)

**La condición de mesa, medida antes de ejecutar.** `data/manifiesto.yaml`:
**845** entradas, **841** con `sha256` de 64 hex derivado por
`tests/manifiesto.py`; las **4** sin `sha` son «hechos», no payloads. Los
payloads **sí** los vigila el manifiesto con `sha` → la condición se cumple →
`DT-a` rige. Exentar `data/raw/**` de `T27` no deja ningún archivo sin custodia:
mueve la custodia al test que corresponde.

`t27_infraestructura()` salta toda ruta bajo `data/raw/` y toda raíz declarada
en `data/raices.local.yaml` (leída si existe; **no existe** en este árbol, y en
nube tampoco habría corpus que apuntar). `_T_INFRA_ARCHIVOS_CONOCIDOS` **no se
toca**, como el encargo exige. El comentario en el código cita `FP-229`,
`ADR-278` y la firma.

**Recongelado.** `python3 tests/check.py --freeze` → `tests/baseline.json` con
`HEAD` `e4af4ede7c3020b80981abaf36ccdc00258bbe05`, **19 `FAIL` · 113 `WARN`**.
El diff del archivo son **dos líneas**: el `HEAD` y un conteo de bucket
(`T22_sin_clasificar` 14 → 45, que es reclasificación de la misma deuda, no
deuda nueva). **Cero entradas nuevas absorbidas** — el recongelado no perdona
nada que no estuviera ya perdonado.

**Lo que la exención NO cubre, y por qué no se instrumenta hoy.** La dirección
inversa —un archivo en el corpus **sin** entrada en el manifiesto— queda sin
test. Se declara en `forense/hallazgos.md` y se instrumenta (`T28`) **el día que
aparezca un huérfano medido en `data/raw`** (`v2.3`): hoy no hay ni un caso
medido que le dé forma, y escribir el test contra un caso imaginado es
adivinar. El remedio (c) de `FP-229` —quitar el symlink autorreferente
`/home/pc0/mm-corpus/raw/raw`— **no se toca**: vive en la caja, no en el repo.

**Límite honesto de esta verificación.** En nube `data/raw` no existe, así que
el efecto de la exención sobre las 30 761 entradas `T27` que `MAESTRA34-A1`
midió en caja **no se puede reproducir aquí**. Lo que sí se verifica: la suite
sigue en **VERDE** contra la línea base y el código sólo puede reducir el
conjunto de rutas examinadas, nunca ampliarlo. La medición de control queda para
`MAESTRA34-L3` (caja), que es el sucesor.

---

## 2 · `P2` — necesidad `N36` para `R4.3` (`FP-230`, firma `DN-a`)

`R4.3` estaba en el perímetro de 27 reglas del Hito D **sin necesidad `N`
asignada** — el hueco que `MAESTRA34-A1` midió y no pudo reparar (esa tabla era
de sólo lectura en su perímetro). Cerrado:

- `necesidad_id` **derivado, no heredado**:
  `cut -f1 data/curacion-registro/necesidad-objeto-modelo.tsv | sort -V | tail -1`
  daba `N35` → **`N36`**.
- `objeto_modelo_origen` = `R4.3`, mismo patrón que `N21`–`N33`.
- Regla **verbatim** de `canon/modelo-decision-v4_0.md:529` (id
  `salud.adherencia.desabasto_vs_cuidadora`): *«SI hay desabasto + gasto de
  bolsillo alto ENTONCES abandono o intermitencia del tratamiento crónico; SI
  hay familia cuidadora + medicamento surtido ENTONCES mayor adherencia —
  PORQUE estructura + G5 — `[FUERTE / MEDIA]`.»*
- **Objeto de evidencia**: registro individual de desabasto + urgencias.
- Reserva escrita: es **compuesta** (dos falsadores, uno por mitad), ambas
  mitades archivadas con veredicto `D` el 4/ago/2026 (`ADR-56`); y el riesgo que
  su propia ficha declara (`hitoD-preregistro §374`) — la mitad B confunde
  estructura con cultura sin control socioeconómico obligatorio.

---

## 3 · `P3` — cinco relaciones en las tres tablas (`FP-230`, firma `DN-a`)

`FP-230` dice que la capa de relación **no admite fuentes nuevas** porque las
tres invariantes de `tools/curador_registro/baseline.py` están acopladas. La
ejecución es escribir las tres tablas **a la vez**:

| necesidad | fuente | objeto | `capa4` | clasificación | confianza |
|---|---|---|---|---|---|
| `N25` (`R7.1`) | `SICEE` | estadística de cómputos | `SIN_APERTURA_EXPLICITA` | `CANDIDATA` | `MEDIA` |
| `N26` (`R7.3`) | `SICEE` | estadística de cómputos | `SIN_APERTURA_EXPLICITA` | `CANDIDATA` | `BAJA` |
| `N36` (`R4.3`) | `CERO_DESABASTO` | registro individual histórico | `CANDIDATA-NUEVA-POTENCIALMENTE-MATERIAL` | `CANDIDATA` | `MEDIA` |
| `N36` (`R4.3`) | `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` | descriptores y catálogos | `SATISFACE-UMBRAL-DOCUMENTAL` | `CANDIDATA` | `MEDIA` |
| `N36` (`R4.3`) | `EXT_OF_05_URGENCIAS_CUBO_IMSS_INEGI` | microdato anual | `CANDIDATA-NUEVA-POTENCIALMENTE-MATERIAL` | `CANDIDATA` | `BAJA` |

**`N25` es la necesidad cívica concurrente.** `R7.1` es la regla cuyo falsador
pide el contraste elección concurrente vs. **no** concurrente con granularidad
municipal; `MAESTRA34-A1` midió que el PREP 2024 no lo sirve por las dos
mitades (0 menciones de local/estatal/municipal en el `LEEME`, y geografía sólo
`ENTIDAD`/`DISTRITO_FEDERAL`/`SECCION`), y por eso `MAESTRA34-L3
CIVICA-CONCURRENTE` no se redactó. `SICEE` es la vía viva que queda, y ahora
tiene fila donde escribir su veredicto — que es lo único que `FP-230` pedía.

**`SICEE` no se fusiona con `INE`**: misma institución, objeto distinto, mismo
criterio que su fila de `aliases-fuentes.tsv`. Y **no tiene payload** al
1/sep/2026 (la fila de la cola está en
`NO-OBTENIDO-POR-ESTE-AGENTE(1 intento)`), así que `id_manifiesto` y
`sha256_fuente` van en `NO_DETERMINADO` y `capa2`/`capa3` en `NO_REFERENCIADO`.
No se estima nada.

**`DGIS urgencias` — la `N` de salud que `A1` mapeó es exactamente `R4.3`, y
ninguna más.** Medido, no supuesto: antes de este acto **ninguna** necesidad de
`N1..N35` cubre un objeto de salud (`N21`–`N33` son `R1.4`, `R2.1`, `R2.2`,
`R3.4`, `R7.1`, `R7.3`, `R7.4`/`R7.5`, `R8.1`, `R8.2`, `R8.3`, `R10.1`,
`R10.2`, `R10.3`; `N34`/`N35` son crédito y trabajo). `A1` no mapeó `DGIS
urgencias` a ninguna otra `N` porque no había ninguna otra a la que mapearla —
eso es literalmente lo que `FP-230` levanta. Se declara en vez de inventarse una
segunda necesidad.

**Ids derivados, ninguno a mano.** `relacion_id` con la función
`relacion_id()` de `baseline.py` importada, no reimplementada (el validador la
recomputa fila por fila). `OE-` y `PROV-` con la derivación que la `GUIA` fija
en su sección nueva, para que el mismo objeto dé el mismo id en altas futuras.

**Lo que este acto NO afirma haber hecho.** No abre payloads, no monta corpus,
no mide. `capa3_disco_real = EXISTE;COINCIDE;INTEGRO` en las tres filas con
payload se **cita** de la verificación anti-`PR #77` de `MAESTRA34-A1` (`sha256`
recalculado en el corpus, 38/38 idénticos, 0 discrepancias) y cada `nota` lo
dice con esas palabras, junto con el resultado que este entorno sí puede medir
(§5). Todo el contenido —11 036 filas, 7 914 reportes, 2019-02-18 a 2024-09-03,
los `sha256`, el hallazgo del `7z` mal etiquetado por DGIS— es cita de `A1` y
del manifiesto, verbatim.

**Validador en VERDE**, que es la condición que el encargo puso:

```
$ python3 tools/curador_registro/baseline.py data/curacion-registro
"ok": true · "errores": []
relaciones_activas 204 · procedencias_aceptadas 205 · fusiones_declaradas 1
candidatas 146 · confirmadas 3 · negativas 48 · no_accesibles 7
```

Las tres invariantes se sostienen por construcción: 5 relaciones ↔ 5
procedencias (≥1 cada una), utilidad 1:1, y `205 − 204 = 1 = len(fusiones)`
sin tocar `fusiones-relaciones.tsv`.

**`baseline.json` del curador recifrado**, igual que hizo `A1` y por la misma
razón mecánica: los `sha256` de las tres tablas quedan inválidos en cuanto se
escriben, así que el recifrado **no es opcional, es parte del alta**. No absorbe
ningún error preexistente — el árbol estaba en `"ok": true` antes de empezar,
verificado.

**La vía, escrita para que no haya que redescubrirla.**
`tools/curador_registro/GUIA-CURADOR-REGISTRO.md` gana la sección **«alta de
fuente nueva en tres tablas»** con las tres invariantes, la derivación de los
tres ids, el procedimiento de cinco pasos y los dos comandos de cierre.
`data/INFRAESTRUCTURA-v1_0.md` D1 pasa de «**SIN VÍA de script**» a «**VÍA
DOCUMENTADA, no script**» citándola — y dice explícitamente que **sigue sin
haber script**, para no vender más de lo que hay.

---

## 4 · `P4` — trámite

**Tablero.** `forense/firmas-pendientes.tsv`: `FP-229` y `FP-230` pasan a
`EJECUTADA` con recibo que nombra el remedio elegido, la medición que lo
autoriza y lo que queda fuera.

**`MACU` y `CAFR León` siguen sin fila**, y se dice en el recibo: sus objetos de
modelo tampoco están en el universo de necesidades, y este acto **no les inventó
una**. El encargo pedía `SICEE`, `Cero Desabasto` y `DGIS urgencias`; ampliar el
alcance a dos fuentes más habría exigido decidir dos necesidades nuevas sin
firma que las respalde.

---

## 5 · `via_capa2.py` en lectura — qué confirma y qué no

```
$ python3 tools/curador_registro/via_capa2.py --root .
Filas en relaciones.tsv: 204
Estados de verificación: COINCIDE=0 NO_COINCIDE=0 AUSENTE=54 SIN_PAYLOAD=0 RAIZ_NO_CONFIGURADA=14
Diffs propuestos (capa2_manifiesto): 0
cero payloads verificables — ¿está data/raw montada?
```

**Los 0 diffs no son una confirmación positiva, y decirlo importa.** El script
**nunca degrada** una fila: su regla es
`derivado = "SI" if estado == "COINCIDE" else actual`. «0 diffs» significa que
no contradice ningún `capa2`, no que lo haya verificado.

**Lo que sí se verificó aquí, fila por fila**, corriendo `verificar_entrada()`
sobre las cinco nuevas:

| relación | `capa2` escrito | estado que devuelve |
|---|---|---|
| `REL-2cefaeb67676718b2db5fe9b` (`N25`/`SICEE`) | `NO_REFERENCIADO` | sin `id_manifiesto` — correcto, no hay payload |
| `REL-46f084b007404d4533052205` (`N26`/`SICEE`) | `NO_REFERENCIADO` | sin `id_manifiesto` — correcto |
| `REL-ff6da3b0a22322433d42b4eb` (`N36`/Cero Desabasto) | `SI` | `AUSENTE` |
| `REL-814040652b29189344a6dc4c` (`N36`/DGIS descriptor) | `SI` | `AUSENTE` |
| `REL-b4c434431bd19bbf369d322d` (`N36`/DGIS microdato) | `SI` | `AUSENTE` |

**`AUSENTE` es la respuesta correcta de un entorno sin corpus, no un defecto de
la fila.** `cargar_raices()` devuelve `{}` porque `data/raices.local.yaml` no
existe y `data/raw` no está montada — el propio script lo dice en su última
línea. Los tres `id_manifiesto` **sí resuelven** contra `data/manifiesto.yaml`
con su `sha256` (comprobado: ninguno da `ID_NO_EN_MANIFIESTO`), que es lo que
`capa2_manifiesto = SI` afirma. Lo que **no** se puede afirmar en nube es
`capa3_disco_real`, y por eso queda citado de `A1` y marcado como no
reverificado en las tres `nota`.

**Confirmación positiva de `capa2 = SI` → pendiente de un acto en caja.**
`MAESTRA34-L3` es el candidato natural: correr
`via_capa2.py --root .` con el corpus montado debe devolver `COINCIDE` en esas
tres filas y seguir proponiendo 0 diffs. Si devolviera otra cosa, la fila está
mal y hay que corregirla — se deja escrito para que el sucesor pueda tumbarlo.

---

## 6 · Suite

`python3 tests/check.py --baseline` → **VERDE**, corrido después de cada pieza:
**19 `FAIL` · 169 `WARN`**, *nada nuevo frente a `tests/baseline.json`*
(`HEAD` congelado `e4af4ed`). Ninguna pieza introduce una entrada nueva.

---

## 7 · Lo que este acto no hizo

No abrió payloads · no descargó nada por red · no tocó `data/manifiesto.yaml` ·
no midió nada nuevo · no abrió Ola 6 (eso es `N5` con estos insumos) · no
fusionó su propio PR · no tocó `_T_INFRA_ARCHIVOS_CONOCIDOS` · no escribió fuera
del perímetro declarado.
