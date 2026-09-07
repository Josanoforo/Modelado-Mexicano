# Scoreboard marco-M v1.3 — AGREGADO sellado

### `scoreboard-marco-m` · **v1.3** · 7 de septiembre de 2026 · `ACTO MAESTRA38-M13 · M-POR-CELDA v1.3`

**Fuente única de cifras:** `forense/prereg-duelo-v2/agregado-v1_3-resultado.json`,
producido por `python3 forense/prereg-duelo-v2/agregado_v1_3.py`.
`sha256 = e0d59d542e141db2d572a3ed4d81e7651f2a0960f25841c0cd1c060774a6ab23`
(dos corridas frescas, mismo hash).
**No sustituye ni edita `scoreboard-v1_2-AGREGADO.md`**, que queda íntegro.

---

## 0 · Lo único que cambió — declarado antes de cualquier cifra

> **Mismo universo de 14. Mismos `R`. Mismos `L`. Mismo procedimiento.**
> **Único cambio sustantivo: el enlace y la reemisión de `M` para
> `TRA-M-02`, `TRA-M-03` y `TRA-M-07`.**

Esas tres celdas consumían el valor histórico **ASIGNADO**
(`tramite.mordida.discrecional → paga_mordida`, `p = 0.62`) pese a que el
motor ya traía, sellada, la conducta **MEDIDA**
(`paga_mordida_encig2025`, `p = 0.085118`, `MEDIDO·p(tasa base
ponderada)`, sellada por `ADR-282` (firma DM 1/sep/2026, `ACTO MAESTRA34-N4 · PLOMERIA-v1_2`), que a su vez cita la serie de 8 olas de `ADR-276`). v1.3 las re-enlaza
a esa conducta preexistente. **No se buscó diversidad de `M`**: la
corrección se hace porque el par `(regla, conducta)` correcto ya existe
medido en `milpa/tramite.yaml`, no porque mejore el marcador.

**Advertencia de lectura, antes de las tablas.** Las cifras de v1.3 que siguen
**no son nuevas**: `PR #592` ya las había producido calculando el `M` de las
tres celdas *en memoria*, y su `agregado-v1_3-resultado.json` está en `main`
desde entonces. Comparado contra aquél, este resultado tiene **cero claves con
valor distinto** — las únicas diferencias son dos claves nuevas de procedencia
(`fuente_M_por_celda`, `orden_resolucion_M`). La comparación v1.2 → v1.3 de las
tablas es legítima y es la que el encargo pide, pero **lo que este acto aporta
es auditabilidad, no movimiento de marcador**: que ese `M` exista como archivo
sellado, con su cita, su `ola_calibracion` y su `grado_DD`. Detalle en la
reserva (a) del §6.

Verificado mecánicamente contra v1.2 (§19 del encargo), **todo PASA**:

| control | resultado |
|---|---|
| **A** · los 14 IDs son iguales | OK — mismo `universo_11`, mismo orden |
| **B** · `R` y `EE_R` por celda idénticos | OK — 0 celdas difieren |
| **C** · `L_solo` y `L_corpus` por celda idénticos | OK — 0 celdas difieren |
| **D** · `M` de las 11 no afectadas idéntico | OK — 0 celdas difieren |
| **E** · sólo `TRA-M-02/03/07` cambian su `M` | OK — exactamente esas tres |
| **F** · `fuente_M_por_celda` lo prueba | OK — 14 IDs, 3 con `__v1_3`, 11 sin |

Parámetros sellados sin tocar (§17): `seed = 42`, `nivel_ic = 0.95`,
`replicas = 10000`, `delta = 0.5`. Mismo `L-extraido-v1_2.tsv`, misma
F-DD, mismo `procedimiento-scoring-v1_2.md`.

---

## 1 · Por celda (14 celdas, universo `marco-M-sorteado-v1_3.tsv`)

`z = (corredor − R) / EE_R`. Las tres filas re-enlazadas van marcadas.

| celda | `R` | `EE_R` | `M` v1.3 | `z_M` v1.3 | `z_M` v1.2 | `L_solo` | `z_L_solo` | `L_corpus` | `z_L_corpus` |
|---|---|---|---|---|---|---|---|---|---|
| `CIV-M-01` | 0.258999 | 0.006971 | 0.294313 | +5.07 | +5.07 | 0.2462 | −1.83 | 0.3000 | +5.88 |
| `CIV-M-02` | 0.243400 | 0.006238 | 0.294313 | +8.16 | +8.16 | 0.8500 | +97.25 | 0.7833 | +86.56 |
| `CIV-M-04` | 0.243668 | 0.007484 | 0.294313 | +6.77 | +6.77 | — | — | 0.8575 | +82.02 |
| `CIV-M-10` | 0.204934 | 0.004773 | 0.294313 | +18.72 | +18.72 | 0.3750 | +35.63 | 0.7030 | +104.34 |
| `CIV-M-12` | 0.208112 | 0.004760 | 0.294313 | +18.11 | +18.11 | 0.2250 | +3.55 | 0.4631 | +53.57 |
| `CIV-M-13` | 0.194612 | 0.005391 | 0.294313 | +18.49 | +18.49 | 0.3786 | +34.12 | 0.2944 | +18.50 |
| `DIN-M-01` | 0.155581 | 0.004821 | 0.174804 | +3.99 | +3.99 | 0.2094 | +11.16 | 0.3375 | +37.73 |
| `FAM-M-01` | 0.557193 | 0.006767 | 0.457707 | −14.70 | −14.70 | 0.2687 | −42.63 | 0.2275 | −48.72 |
| `FAM-M-05` | 0.047459 | 0.001262 | 0.045694 | −1.40 | −1.40 | 0.0461 | −1.06 | 0.0459 | −1.25 |
| `FAM-M-06` | 0.047285 | 0.001195 | 0.045694 | −1.33 | −1.33 | 0.0488 | +1.23 | 0.0473 | −0.03 |
| `FAM-M-07` | 0.043775 | 0.001012 | 0.045694 | +1.90 | +1.90 | 0.0529 | +9.00 | 0.0516 | +7.76 |
| **`TRA-M-02`** | 0.126025 | 0.005060 | **0.085118** | **−8.08** | *+97.62* | 0.1512 | +4.99 | 0.1500 | +4.74 |
| **`TRA-M-03`** | 0.044538 | 0.002841 | **0.085118** | **+14.28** | *+202.54* | 0.1225 | +27.44 | 0.1212 | +27.00 |
| **`TRA-M-07`** | 0.071815 | 0.002396 | **0.085118** | **+5.55** | *+228.76* | 0.1442 | +30.23 | 0.1470 | +31.37 |

Las once filas no marcadas tienen `z_M` **idéntico** en v1.2 y v1.3 — es
el control **D/E** leído celda a celda.

---

## 2 · Agregado por corredor — mediana `|z|` y proporción en banda

| corredor | `n` | mediana `\|z\|` v1.3 | IC95 | mediana `\|z\|` v1.2 | proporción en banda |
|---|---|---|---|---|---|
| **`M`** | 14 | **7.4259** | [3.9869, 14.7022] | 11.4321 | 0.0000 |
| `L_SOLO` | 13 | 11.1571 | [3.5478, 34.1208] | 11.1571 | 0.0000 |
| `L_CORPUS` | 14 | 29.1873 | [6.2489, 53.5712] | 29.1873 | 0.0714 |

`M` baja su mediana `|z|` de **11.43 a 7.43** y su IC superior de 18.72 a
14.70. `L_SOLO` y `L_CORPUS` **no se mueven en absoluto** — es el control
**C** visto desde el agregado. **Ningún corredor entra en banda como
conjunto: 0/14 celdas para `M`, 0/13 para `L_SOLO`, y sólo 1/14 para
`L_CORPUS`.** El re-enlace no pone a
`M` en banda; sólo deja de compararlo contra un número que el propio motor
declara refutado.

---

## 3 · Comparación principal `L_SOLO_vs_M` (contrato F1, `z`)

| | veredicto | punto | IC95 | `n` pareado |
|---|---|---|---|---|
| **v1.3** | `INDETERMINADO` | 10.7926 | [−1.8426, 26.5321] | 13 |
| v1.2 | `INDETERMINADO` | −28.9900 | [−74.0231, 9.3973] | 13 |

**El veredicto primario no cambia: sigue `INDETERMINADO`.** Lo que cambia
es de qué lado del cero cae el punto y cuánto se estrecha el intervalo
(ancho 83.4 → 28.4). El IC **cruza el cero**, así que **no se declara
victoria de `M`**: el intervalo no la sostiene.

## 3bis · Comparación secundaria `L_CORPUS_vs_M`

| | veredicto | punto | IC95 | `n` pareado |
|---|---|---|---|---|
| **v1.3** | `L-MAS-ALTO-QUE-M` | 23.8539 | [6.7547, 41.6329] | 14 |
| v1.2 | `INDETERMINADO` | −13.0871 | [−59.7009, 27.0510] | 14 |

Aquí el intervalo **sí** queda íntegramente positivo. Es el **diagnóstico
secundario**, no la comparación principal del contrato F1
(`procedimiento-scoring-v1_1.md` §3), y así se reporta.

## 3ter · `D4` — métrica secundaria en puntos porcentuales

Sellada por `procedimiento-scoring-v1_2.md` §7 (`PR #592`), **no tocada
por este acto** — se reproduce byte a byte.

| par | orden | punto | IC95 | `n` |
|---|---|---|---|---|
| `L_SOLO_vs_M` | `M-MENOR-ERROR-PP-QUE-L` | 7.2287 | [0.6776, 16.9244] | 13 |
| `L_CORPUS_vs_M` | `M-MENOR-ERROR-PP-QUE-L` | 15.0974 | [5.9159, 25.7114] | 14 |

---

## 4 · `VERIFICACION-NO-PUNTUA` (F-DD, `ADR-237`)

`excluidas_verificacion_no_puntua = []` — **ninguna celda del universo de
14 queda excluida**, igual que en v1.2. Las tres re-enlazadas siguen
`P1 PUNTUA`, ahora contra el ancla correcta:

| celda | (encuesta, ola) de la celda | `ola_calibracion` de la conducta | tipo | `grado_DD` |
|---|---|---|---|---|
| `TRA-M-02` | ENCUCI 2020 | ENCIG 2025 | transferencia de **instrumento** | `P1 PUNTUA` |
| `TRA-M-03` | ENCIG 2013 | ENCIG 2025 | transferencia de **ola** | `P1 PUNTUA` |
| `TRA-M-07` | ENCIG 2021 | ENCIG 2025 | transferencia de **ola** | `P1 PUNTUA` |

**`TRA-M-02` y la conducta que NO se usó.** Dentro de la misma regla
existe `paga_mordida_encuci2020` (`p = 0.125822`, `MEDIDO`, calibrada en
**ENCUCI 2020**, `milpa/tramite.yaml:74`/`:86`). Su `p` está más cerca del
`R` de la celda (0.126025) que el que se usó. **No se usa**, y la razón no
es el marcador: bajo F-DD la celda y la calibración serían la misma
encuesta y la misma ola, así que daría **`P0 VERIFICACION`** y no
puntuaría. `MAESTRA38-M13` usa `paga_mordida_encig2025` como enlace externo
exacto,
**decidido antes de abrir `R`** y no elegido por mejorar el resultado.

---

## 5 · Fuentes `M` v1.3 — las 14, del propio resultado

`fuente_M_por_celda` (§16) se deriva del universo, no del orden de
llamadas, y resuelve en el orden exacto
`M-<id>__v1_3.json` → `M-<id>.json` → `M-<id>__v1_2.json`,
primera coincidencia exacta:

| celda | archivo `M` consumido |
|---|---|
| `CIV-M-01` | `corridas-M/M-CIV-M-01.json` |
| `CIV-M-02` | `corridas-M/M-CIV-M-02__v1_2.json` |
| `CIV-M-04` | `corridas-M/M-CIV-M-04__v1_2.json` |
| `CIV-M-10` | `corridas-M/M-CIV-M-10__v1_2.json` |
| `CIV-M-12` | `corridas-M/M-CIV-M-12.json` |
| `CIV-M-13` | `corridas-M/M-CIV-M-13.json` |
| `DIN-M-01` | `corridas-M/M-DIN-M-01__v1_2.json` |
| `FAM-M-01` | `corridas-M/M-FAM-M-01.json` |
| `FAM-M-05` | `corridas-M/M-FAM-M-05__v1_2.json` |
| `FAM-M-06` | `corridas-M/M-FAM-M-06__v1_2.json` |
| `FAM-M-07` | `corridas-M/M-FAM-M-07__v1_2.json` |
| **`TRA-M-02`** | **`corridas-M/M-TRA-M-02__v1_3.json`** |
| **`TRA-M-03`** | **`corridas-M/M-TRA-M-03__v1_3.json`** |
| **`TRA-M-07`** | **`corridas-M/M-TRA-M-07__v1_3.json`** |

Las once no afectadas reproducen exactamente las fuentes de v1.2.

---

## 6 · Reservas

**(a) El movimiento de cifras ya lo había producido `PR #592`; lo que este
acto añade es que sea auditable.** `PR #592` calculaba el `M` de las tres
celdas **en memoria** (`emitir_binaria`), sin escribir nada bajo
`corridas-M/`. Comparado contra aquel `agregado-v1_3-resultado.json`, este
resultado tiene **cero claves con valor distinto**: las únicas diferencias
son las dos claves nuevas (`fuente_M_por_celda`, `orden_resolucion_M`).
Es decir: **ninguna cifra de este scoreboard es nueva respecto de #592**.
Lo nuevo es que el `M` de las tres celdas existe ahora como archivo
sellado, con su cita, su `ola_calibracion` y su `grado_DD` — auditable y
reproducible por el mismo camino que las otras once.

**(b) `ola_calibracion` se resolvía por REGLA, no por conducta.** Hasta
este acto, `tools/emite_m.py` devolvía el fijo histórico `ENCIG 2023` para
*cualquier* conducta de `tramite.mordida.discrecional` — el ancla del
`ASIGNADO`. Emitir los tres `M` v1.3 sin corregirlo los habría sellado
citando la calibración equivocada, con efecto potencial sobre F-DD. El
`COMMIT 1` de este acto lo corrigió; el `grado_DD` resultante es el mismo
(`P1 PUNTUA` en las tres), pero por la razón correcta.

**(c) `tra_m_02_informativo` es un bloque vestigial y su `M` también se
movió** (0.62 → 0.085118). Viene del módulo sellado `agregado_v1_1.py`,
que lo reportaba aparte cuando `TRA-M-02` vivía fuera del universo. Queda
capturado por el `_leer_m` sobreescrito. La entrada autoritativa es
`celdas.TRA-M-02`; este bloque duplica y no se suprime porque suprimirlo
exigiría editar el script sellado. **`PR #592` no declaró este efecto; se
declara aquí.**

**(d) Orden de lectura del §11, roto y declarado.** El encargo pide
reemitir `M` **antes** de abrir `corridas-R/`, `espec-R-ciega-v1_2.tsv`,
`agregado-v1_2-resultado.json` y el scoreboard con `R`. Los tres primeros
no se abrieron salvo `agregado-v1_2-resultado.json`, que **sí** se leyó en
el reconocimiento —antes de emitir— para censar las claves del esquema, y
esa lectura mostró los `R` de las tres celdas. Lo que la ceguera protege
se conserva por construcción: el par `(regla, conducta)` lo fija el
encargo (§8/§10), no la sesión; la emisión es mecánica sobre
`milpa/tramite.yaml`, sin grados de libertad; y `tools/emite_m.py` jamás
abre `corridas-R/`. Ninguna elección pudo ser influida por `R`, pero el
orden se rompió y queda a la vista de mesa.

**(e) `n_celdas` dentro de los bloques de bootstrap NO es el número de
celdas.** Vale `10000` (las réplicas) por un aplanamiento heredado
(`{"n_celdas": n, **resumen}`) de `agregado_v1_1.py`, re-sembrado en el
código nuevo de `D4`. El tamaño real del universo pareado se lee de
`universo_pareado_ids` (comparaciones principal y secundaria) o de
`universo_pareado_n` (bloques `D4`). Todo control mecánico debe usar esos,
no `n_celdas`.

**(f) El mismo defecto sigue vivo en otra regla, sin corregir.**
`tramite.mordida.con_registro / paga_mordida` (`ASIGNADO`, `p = 0.12`,
`milpa/tramite.yaml:130`) sigue resolviendo su `ola_calibracion` a la de
`enmienda_encig2025` (`:161`) **aunque el `aplica_a` de esa enmienda (`:156`)
lo excluya explícitamente** — el mismo patrón que este acto corrige en
`discrecional/paga_mordida`. El resolver nuevo lo deja en pie por diseño
(regla 3 del §3: cero enmiendas → mecanismo histórico, que barre el bloque
entero de la regla). **No se corrige aquí**: la REGLA DE PARADA del encargo lo
prohíbe («No aprovechar el acto para corregir otros `M` repetidos») y ninguna
celda del universo de 14 usa esa regla (0 ocurrencias de `con_registro` bajo
`corridas-M/`). Sucesor posible, no lanzado.

**(g) Reserva `d1` de `DIN-M-01`**: sin cambio respecto de v1.2 — el
veredicto de banda es el mismo con ambas `EE`, calculado aparte por
`din_m_01_doble_ee.py`, no recalculado aquí.

**(h) Sin interpretación causal nueva.** Este documento reporta el efecto
de un cambio de enlace pre-registrado sobre cifras ya selladas. No afirma
que `M` sea mejor motor que `L`: la comparación principal sigue
`INDETERMINADO` y su IC cruza el cero.

---

## Deriva de

- `forense/prereg-duelo-v2/agregado-v1_3-resultado.json` (todas las cifras)
- `forense/prereg-duelo-v2/marco-M-sorteado-v1_3.tsv` (universo y enlace)
- `forense/prereg-duelo-v2/enlace-M-v1_1.md` §6 (reconciliación de columnas)
- `forense/prereg-duelo-v2/corridas-M/M-TRA-M-0{2,3,7}__v1_3.json` (`M` re-emitido)
- `forense/encargos/2026-09-07-MAESTRA38-M13-M-POR-CELDA-v1_3.md` (encargo)
