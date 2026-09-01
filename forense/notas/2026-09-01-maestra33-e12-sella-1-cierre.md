# MAESTRA33-E12 · SELLA-1 — cierre

`ACTO MAESTRA33-E12 · SELLA-1`, 1/sep/2026, entorno NUBE, `SHA de redacción
5a905b3` (merge `PR #431`) = tip literal de `origin/main` al arrancar y al
cerrar (`git fetch origin main` re-verificado, `HEAD` idéntico), sin drift
que refrescar. `COMPUERTA: ninguna de merge`, declarada por el encargo — no
dispara verificación, se continúa directo al 0-bis A.3.

## §0 · Encargo, verbatim (referencia)

El encargo llegó pegado en el mensaje que invocó `/acto`; el propio 0-bis
A.3 lo escribió en `forense/encargos/2026-09-01-MAESTRA33-E12-SELLA-1.md`
(primer commit del acto, antes de cualquier paso sustantivo). Las tres
firmas de mesa verbatim que trae, entre guillemets, con los corchetes
literales:

- «[sello scoring v1_1 — cinco decisiones]»
- «[sello reglamento sorteo v1.1]»
- «[enterado FP-218]»

Ninguna llegó vacía — la condición del propio encargo ("el corchete de
abajo con texto — vacío → cero commits") queda satisfecha, `P1` se
ejecuta.

## §1 · P1 — sellado

### 1.1 · `procedimiento-scoring-v1_1.md`

`sha256` de `forense/prereg-duelo-v2/procedimiento-scoring-v1_1-PROPUESTA.md`
verificado **antes** de escribir la copia sellada:

```
$ sha256sum forense/prereg-duelo-v2/procedimiento-scoring-v1_1-PROPUESTA.md
7c7cfc2c8d273ed50048438b9a21e1e7d9612ce183558d8461140541b5a8fd39  forense/prereg-duelo-v2/procedimiento-scoring-v1_1-PROPUESTA.md
```

Copia escrita a `forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md`:
cabecera nueva (estado SELLADO, firma verbatim, `sha256` de la PROPUESTA
citado, SHA de redacción heredado) + cuerpo (`§0`-`§6`) copiado byte a
byte. Verificado por `diff` entre el cuerpo de la copia (desde `## Cabecera
obligatoria`) y el cuerpo de la PROPUESTA (misma sección en adelante):
**sin diferencias**. `sha256` de la PROPUESTA re-verificado **después** de
escribir la copia: idéntico, sin drift — la PROPUESTA no se tocó.
`.sha256` sidecar propio de la copia (hash del archivo sellado, mismo
patrón que `L-spec-v1_1.sha256`):

```
$ sha256sum forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md
1bb38b49bc076fcc214b3012ccc953ea7ed4183a4a5b81267ca0a1a4f0d2c7f5  forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md
```

### 1.2 · `reglamento-sorteo-v1_1.md`

Mismo procedimiento. `sha256` de
`forense/prereg-duelo-v2/reglamento-sorteo-v1_1-PROPUESTA.md` verificado
antes y después de escribir la copia (idéntico, sin drift):

```
$ sha256sum forense/prereg-duelo-v2/reglamento-sorteo-v1_1-PROPUESTA.md
ee97ab79c4b4f7973b44a428791987523d4de9a8efc833a223345f343138b828  forense/prereg-duelo-v2/reglamento-sorteo-v1_1-PROPUESTA.md
```

La cabecera de la copia responde, verbatim, las cuatro preguntas de la
Sec.5 de la PROPUESTA (detalle completo en la cabecera del propio
archivo): **(1)** SÍ, la implementación exacta escrita (piso 1 + Hamilton,
efecto general de Sec.3) — no la alternativa quirúrgica, que no se
escribió; **(2)** NO reabre `v1_1` (confirma `FP-213`/opción A, no la
reinterpreta); **(3)** la segunda cláusula de la regla 3 sigue sin
implementar, `PENDIENTE-DE-MESA` para un acto futuro — este sello no la
necesita resuelta; **(4)** número: `ADR-260`/`FP-216`. `diff` del cuerpo
(desde `## 0 · Perímetro`) contra la PROPUESTA: **sin diferencias**.
`.sha256` sidecar:

```
$ sha256sum forense/prereg-duelo-v2/reglamento-sorteo-v1_1.md
856dfc02d3b80c994b2c2a080935c3108ca40a0a21c83c04389918ee47276caa  forense/prereg-duelo-v2/reglamento-sorteo-v1_1.md
```

### 1.3 · `mesa-pendientes.md` §5

La línea `**Firma de mesa:** _(pendiente)_` se rellenó con la firma
verbatim, fecha, acto y `ADR-260`, más una línea de consecuencia (qué
archivo quedó escrito). El resto de la sección (las cinco decisiones
enumeradas, la cabecera del acto `MAESTRA33-E10`, el vencimiento) **no se
tocó** —
verificado por `git diff` que el único cambio en el archivo es esa línea.

### 1.4 · Tablero — `FP-216`

`ABIERTA` → `FIRMADA`. Edición quirúrgica de una sola fila: se leyó la
fila exacta con `sed -n`, se construyó el reemplazo con el mismo número de
columnas (`estado`, `firmada_en`) y se verificó con `git diff` que
**ninguna otra fila del archivo cambió** (primer intento con el módulo
`csv` de Python normalizó comillas en 19 filas no relacionadas por
diferencias de estilo de citado — descartado antes de commitear,
`git checkout --` sobre el archivo, rehecho con edición de texto dirigida
sobre la fila exacta). `firmada_en` cita las cuatro respuestas de la Sec.5
del reglamento (mismo texto que la cabecera del archivo sellado, §1.2
arriba) y declara que firmar esto no ejecuta nada.

### 1.5 · Tablero — `FP-218`

`ABIERTA` → `CERRADA-PREEXISTENTE` (valor de `estado` nuevo, pedido
literal por el encargo — sin precedente exacto en el tablero, más cercano
a `CERRADA` que a `FIRMADA`: no hay decisión nueva que firmar, solo el
reconocimiento de que el trabajo de fondo ya estaba hecho). Verificado en
el árbol, no solo citado de la nota de `MAESTRA32-E8`, que las dos
entradas existen hoy en `milpa/procedencia.yaml::coeficientes_generador_sellados`:

```
$ grep -n "coeficientes_generador_sellados" -A1 milpa/procedencia.yaml | head -2
1242:coeficientes_generador_sellados:
1243-- gen: G1
```

- `{gen: G1, coef: radio_confianza, valor_ejecutable: -0.06626, alpha:
  0.7441, ic: IC95% -0.116675,-0.015844}` (líneas 1254-1266)
- `{gen: G4, coef: confianza_institucional, valor_ejecutable: -0.166208,
  alpha: 0.8085, ic: IC95% -0.212384,-0.120031}` (líneas 1289-1301)

`alpha ≥ 0.50` en ambas (regla `§d` de la spec de `MAESTRA32-E8`), IC95
excluye 0 en ambas → sin sufijo `NO-DISTINGUIBLE-DE-CERO`. De las dos
alternativas que `FP-218` planteaba (fila cierra sin trabajo adicional, o
hay un paso posterior no identificado), es la primera: no hay regla
ejecutable de `milpa/tramite.yaml` que cargar con este β̂ — es un
coeficiente de generador `ASIGNADO`-reemplazado (capa de coeficientes,
`G1`/`G4`), no una regla de conducta del motor.

## §2 · P2 — verificación `--dry-run` (sin puntuar)

Ni `tools/score_marco_m.py` ni `forense/prereg-duelo-v2/carga_scoring_v1_1
_propuesta.py` declaran `--dry-run` como flag — verificado por `--help` de
ambos y por lectura de fuente; el segundo lo dice explícito en su propio
docstring ("No hay smoke-test, no hay `--dry-run`"). Declarado, no
escondido: ninguno de los dos lo necesita para ser seguro de correr,
porque **ninguno de los dos llama `ejecutar_scoring`** — ambos solo censan
el árbol y arman un documento JSON en memoria/stdout. Se corrieron tal
cual (invocación normal, sin flag), y se verificó después con
`git status --porcelain forense/prereg-duelo-v2/corridas-M forense/prereg-duelo-v2/corridas-R forense/prereg-duelo-v2/corridas-L`
(salida vacía) que ningún archivo de corrida se tocó.

### 2.1 · `tools/score_marco_m.py`

```
$ python3 tools/score_marco_m.py > /tmp/score_marco_m-dryrun.json
$ echo $?
0
```

Resumen (censo completo en el JSON, no reproducido íntegro aquí):

| campo | valor |
|---|---|
| `marco_censado` | `marco-M-sorteado-v1_1.tsv` |
| `n_celdas_universo` | `11` |
| `n_verificacion_no_puntua` | `0` |
| `n_puntuables` | `8` |
| celdas con `L` disponible | `0` de `11` |
| celdas con `mediciones` no vacías | `0` de `11` |
| `configuracion["delta"]` | ausente (como diseñado) |

Por celda (`M`/`R`/`L` disponible, `puntuable`):

```
CIV-M-01  M=True  R=True   L=False   puntuable=True
CIV-M-06  M=True  R=True   L=False   puntuable=True
CIV-M-08  M=True  R=True   L=False   puntuable=True
CIV-M-09  M=True  R=True   L=False   puntuable=True
CIV-M-11  M=True  R=True   L=False   puntuable=True
CIV-M-12  M=True  R=True   L=False   puntuable=True
CIV-M-13  M=True  R=True   L=False   puntuable=True
FAM-M-01  M=True  R=True   L=False   puntuable=True
TRA-M-03  M=True  R=False  L=False   puntuable=False
TRA-M-05  M=True  R=False  L=False   puntuable=False
TRA-M-07  M=True  R=False  L=False   puntuable=False
```

**`L pendiente: 11 celdas`** — cero de las once tiene ninguna corrida `L`
(`corridas-L/` trae 120 archivos totales, ninguno con prefijo de celda
marco-M — mismo conteo que `MAESTRA33-E9` ya había declarado).

### 2.2 · `carga_scoring_v1_1_propuesta.py`

```
$ python3 forense/prereg-duelo-v2/carga_scoring_v1_1_propuesta.py > /tmp/carga-scoring-v1_1-dryrun.json
$ echo $?
0
```

| campo | valor |
|---|---|
| `estado` (auto-declarado por el script) | `PROPUESTA -- PENDIENTE-DE-MESA -- este script no se ejecutó en MAESTRA33-E10` (literal del script, describe su propia historia en `ACTO MAESTRA33-E10` — no editado, no es una afirmación vigente sobre el sello de este acto) |
| `entrada_scoring_v1_1_propuesta.configuracion["delta"]` | `0.5` |
| `n` celdas | `11` |
| celdas con `mediciones` no vacías | `0` de `11` |

Único campo que cambia respecto a `tools/score_marco_m.py`:
`configuracion["delta"]` (ausente → `0.5`), exactamente como la cabecera
del cargador declara que haría. `celdas` sin tocar. Ningún llamado a
`ejecutar_scoring`; `scoring-adv1-m3.py` sin diff (verificado por
`git status --porcelain` sobre el archivo, vacío).

## §3 · Cascada

- **ADR.** Re-derivado por comando (`grep -oE '^\*\*ADR-[0-9]+'
  canon/gobernanza-v1_15.md | grep -oE '[0-9]+' | sort -n | tail -1` →
  `259`, sin huecos) → candidato **`ADR-260`**, contiguo. Ningún otro acto
  en vuelo conocido al escribir esto. Entrada nueva al final de `§4.
  Registro de decisiones` de `canon/gobernanza-v1_15.md` (la sección es
  cronológica ascendente — se ordena por fecha de merge, no se prepende;
  confirmado leyendo la sección completa antes de editar, no asumido del
  patrón de `L0`, que sí prepende). Cabecera de conteo: `259 → 260 ADR`.
  La auto-cita de `ADR-259` ("`258 → 259 ADR`", en su propio párrafo de
  cascada) recibió la marca `{cita-historica}` — sin ella, `T15` la
  reportaría como una afirmación vigente incorrecta ahora que el conteo
  real subió a 260 (mismo mecanismo que protege la cita de `ADR-234`,
  visible más arriba en el mismo documento).
- **L0.** `canon/estado-programa-v1_10.md`: conteo `259→260` en la tabla
  de artefactos (línea 27) y en la cabecera de la línea `L0`; anotación
  nueva insertada **antes** de la de `ADR-258`/`MAESTRA33-E11` (la más
  reciente hasta ahora), sin tocar ninguna de las que ya estaban.
- **`registro-rotulos.tsv`.** Fila nueva `MAESTRA33-E12` en el espacio
  `E`, después de la fila de `MAESTRA33-C7` — mismo patrón que
  `MAESTRA33-E7` a `MAESTRA33-E11`.
- **T25.** `_T25_ROTULO_BARE` (`(M|E)-?(\d{1,2})` sin alfanumérico/guión
  antes) verificado a mano contra el encargo verbatim y contra este
  archivo: toda mención del rótulo va precedida de guión
  (`MAESTRA33-E12`), ninguna pelada — no requiere entrada nueva en
  `_T25_ARCHIVOS_CONOCIDOS`. Confirmado por la corrida real de `--baseline`
  (§3.1 abajo): `T25` no aparece en la lista de `FAIL`.
- **T22.** El encargo archivado (A.3) dispara `_T22_MARCADOR_PENDIENTE`
  (`PROPUESTA.*mesa`, en la línea de `A.8`: "...-PROPUESTA.md ... EXISTEN
  sin sellar (mesa-pendientes.md §S5)") — no es un pendiente nuevo sin
  registrar, es la descripción del estado que este mismo acto resuelve en
  el mismo commit. `forense/encargos/2026-09-01-MAESTRA33-E12-SELLA-1.md`
  añadido a `_T22_ARCHIVOS_CONOCIDOS` con el razonamiento en el comentario
  (mismo patrón que las entradas previas de esa lista). El encargo mismo
  **no se editó** (A.3, verbatim).
- **`python3 tests/check.py --baseline`.**

### 3.1 · Salida de `--baseline`

Antes de las correcciones de cascada (T15/T22), la corrida reportaba:

```
LÍNEA BASE: ROJO — 3 entradas nuevas frente a tests/baseline.json (HEAD congelado c6a0d72fe298e4a98fecc67912760a012fff5d8a)
· T15: canon/estado-programa-v1_10.md: cita 259 ADR; gobernanza tiene 260 únicos
· T15: canon/gobernanza-v1_15.md: cita 259 ADR; gobernanza tiene 260 únicos
· T22: forense/encargos/2026-09-01-MAESTRA33-E12-SELLA-1.md trae un marcador de ranura/pendiente-de-mesa nuevo...
```

Después de rellenar los conteos de ADR (`gobernanza-v1_15.md:2`, la
auto-cita de `ADR-259` con `{cita-historica}`, `estado-programa-v1_10.md`
líneas 27 y 105) y de añadir el encargo a `_T22_ARCHIVOS_CONOCIDOS`:

```
19 FAIL · 167 WARN
LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado c6a0d72fe298e4a98fecc67912760a012fff5d8a)
```

Los 19 `FAIL` restantes (`T09`×8, `T05`×5, `T02`×2, `T06`×2, `T08`×1,
`T11`×1) son preexistentes, ninguno tocado por este acto — mismos que la
corrida traía antes de este acto (24 totales, de los cuales 5 eran los
`T15`×4/`T22`×1 que este acto introdujo y corrigió en el mismo commit de
cascada).

## §4 · Perímetro y contador

**CONTADOR: 0** — ningún corredor corrido (`R`/`M`/`L`), ningún archivo de
`corridas-M/`, `corridas-R/` ni `corridas-L/` tocado (verificado por
`git status --porcelain` limpio sobre los tres directorios en todo el
acto). No corre el agregado (`ejecutar_scoring` nunca invocado). No edita
las PROPUESTA (`sha256` de ambas verificado idéntico antes y después). No
toca `scoring-adv1-m3.py` ni `sorteo_v2.py`/`sorteo_v3.py`/`sorteo_marco_m
*.py`. `D-6` aplicado: el acto se declara `ACTO MAESTRA33-E12` en todo
archivo que escribe.

## §5 · Archivos tocados

`forense/encargos/2026-09-01-MAESTRA33-E12-SELLA-1.md` (nuevo, A.3) ·
`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.md` (nuevo) ·
`forense/prereg-duelo-v2/procedimiento-scoring-v1_1.sha256` (nuevo) ·
`forense/prereg-duelo-v2/reglamento-sorteo-v1_1.md` (nuevo) ·
`forense/prereg-duelo-v2/reglamento-sorteo-v1_1.sha256` (nuevo) ·
`forense/prereg-duelo-v2/mesa-pendientes.md` (§5, una línea) ·
`forense/firmas-pendientes.tsv` (`FP-216`, `FP-218`) ·
`canon/gobernanza-v1_15.md` (`ADR-260` + marca `{cita-historica}` en
`ADR-259` + cabecera de conteo) · `canon/estado-programa-v1_10.md` (L0 +
tabla de artefactos) · `canon/registro-rotulos.tsv` (fila `MAESTRA33-E12`)
· `tests/check.py` (`_T22_ARCHIVOS_CONOCIDOS`) · esta nota.

No tocados: `procedimiento-scoring-v1_1-PROPUESTA.md`,
`reglamento-sorteo-v1_1-PROPUESTA.md`, `tools/score_marco_m.py`,
`scoring-adv1-m3.py`, `carga_scoring_v1_1_propuesta.py`, `corridas-M/`,
`corridas-R/`, `corridas-L/`, `sorteo_v2.py`, `sorteo_v3.py`,
`sorteo_marco_m.py`, `sorteo_marco_m_v1_1.py`,
`sorteo-act-pil-3-v2-PROPUESTA.md`.
