# Procedimiento de la corrida de M + scoring real — `ACTO MAESTRA30-E9`

**COMMIT-1.** 26/ago/2026. `main` en `6d213a6` (incluye E7 `#378`, E8 `#380` — el
gate de este acto —, E10 `#379`). Redactado **antes** de invocar
`ejecutar_scoring` ni una sola vez con datos reales, y antes de escribir
`corridas-M/`.

## 0 · Premisas heredadas, citadas, no re-derivadas donde ya están selladas

- `comparacion_principal_id = "L-solo"` — FIRMADA, `F0.1`/`ADR-197`
  (`prereg-corrida-v1_0.md`), candado `FP-63`. `L+corpus` es auxiliar
  no-gating (no ejecutado, `FP-165` FIRMADA).
- Contrato de `validar_configuracion` tras la enmienda `F1` (`ADR-208`,
  `prereg-corrida-v1_0.md` §`F1 · enmienda 2026-08-26`): mínimo obligatorio
  `{(L,solo):1, (M,principal):1}`; `(L,corpus)` y `(E,combinacion)`
  opcionales (0 o 1). `sha256` de `scoring-adv1-m3.py` verificado en este
  acto contra esa fila (no contra la tabla original de F1):
  `63418cc8cfdb03ba5d851d01f1bba23e2f21dbac5cfbed2d88c2832cba13a8cf` —
  coincide.
- Banda TOST / margen material: `Δ_material = 0.5·EE(R)` de la celda
  evaluada — FIRMADA, `FP-163`/`ADR-199`, verbatim de mesa: *"FIRMO
  FP-163: banda TOST y margen material del piloto = regla derivada
  `Δ_material = 0.5·EE(R)`, banda `[-0.5·EE(R), +0.5·EE(R)]`, tal como el
  pre-registro la justifica."* Esto **corrige la reserva del marcador
  v1.0**, que la citaba como `ABIERTA`.
- Enlace `SpecCelda → (regla, conducta)`: `enlace-M-v1_0.md` (`ACTO
  MAESTRA30-E8`, `ADR-208`). Sobre las 60 filas del marco: **1 EMITE**
  (`CIV-01`, fuera de las 15 sorteadas), **59 NO-EMITE**. Sobre las **15
  sorteadas** de este duelo: **0 EMITE**.

## 1 · Corredores activos reales de esta corrida (congelados)

| id | familia | variante | por qué |
|---|---|---|---|
| `L_SOLO` | `L` | `solo` | 120 capturas, `ACTO MAESTRA30-E6 · L-RUN`, `ADR-206`. Único corredor `L` ejecutado. |
| `M` | `M` | `principal` | Declarado activo porque el contrato `F1` lo exige como rol obligatorio; **emite 0 de 15 puntos** sobre las celdas sorteadas (ver §0). Declarar el corredor activo no implica que tenga mediciones — el contrato distingue ambas cosas. |

`(L,corpus)` y `(E,combinacion)`: **ausentes**, deliberadamente (`FP-165`
FIRMADA declara `L+corpus` no-ejecución permanente; `ADR-141` selló `E`
como `INEJECUTABLE` con menos de tres corredores — consecuencia ya
declarada en `FP-165`, no descubierta aquí). No se declaran como
corredores activos con variante `0` mediciones: simplemente no aparecen
en `corredores_activos`, que es lo que el contrato `F1` permite.

`comparaciones_l_m = [{"id": "L_SOLO_vs_M", "l_id": "L_SOLO", "m_id": "M"}]`.
`comparacion_principal_id = "L_SOLO_vs_M"`. `e_id = null` (no hay corredor
`E` activo).

## 2 · Celdas M emitibles según el enlace sellado — 0 de 15

Re-verificado en este acto **por ejecución real** de
`milpa.src.emisor.construir_crosswalk` (no por lectura del documento),
dos corridas frescas, salida idéntica entre sí y con las filas de datos
de `forense/crosswalk-pregunta-regla-v1_1.tsv` ya comprometido (el único
diff contra el archivo comprometido son las 9 líneas de comentario
documental que preceden a los datos, no datos). Las 15 sorteadas, todas
`NO-EMITE` en pasada 1 (variable+encuesta no coinciden en
`procedencia.yaml`/`tramite.yaml`): `CIV-08`, `DIN-03`, `DIN-05`,
`DIN-07`, `DIN-11`, `DOC-06`, `EMP-02`, `EMP-04`, `EMP-05`, `SFT-04`,
`SFT-06`, `TIC-01`, `TIC-06`, `TIC-08`, `TIC-12`. Ninguna alcanza siquiera
`CANDIDATO-EMITE`, así que ninguna llega a necesitar la verificación de
cita `(regla, conducta)` de la pasada 2. **0 emitibles → 0 invocaciones de
`emisor.emitir_binaria` posibles para este set** (la función exige un
objeto `Regla` real, y ninguna de las 15 lo tiene).

## 3 · `delta`, `nivel_ic`, `seed` — lo que el pre-registro fija y lo que no

El docstring de `scoring-adv1-m3.py` es explícito: *"seed, nivel_ic, delta
y la comparación principal nunca tienen default."* Este acto verifica los
cuatro contra el árbol, no da por buena la lista del encargo:

- **`comparacion_principal_id`**: FIJADA (§0). ✅
- **`delta`**: el pre-registro fija una **regla de forma por celda**
  (`0.5·EE(R)` de esa celda, FIRMADA), no un escalar único de corrida. El
  esquema de `Configuracion.delta` (`scoring-adv1-m3.py:87`) exige
  exactamente **un** `float` por documento, y `adjudicar_secuencia`
  compara ese único `delta` contra la diferencia del universo **agregado**
  (todas las celdas pareadas juntas, bootstrap sobre su media — ver §4).
  No existe una forma honesta de colapsar "una fracción distinta del
  `EE(R)` de cada celda" en un solo escalar sin inventar cuál celda (o qué
  combinación de las 9 `EE(R)` reales) representa al conjunto — el
  pre-registro nunca lo decide, porque nunca anticipó una comparación
  agregada entre celdas de escalas distintas (ver §4). **No se elige un
  valor.**
- **`nivel_ic`**: sin cita en ningún documento de `forense/prereg-duelo-v2/`
  ni en `canon/`. Búsqueda exhaustiva de este acto:
  `grep -rln "nivel_ic" --include="*.md" --include="*.json" --include="*.py" --include="*.tsv" .`
  (excluyendo `.git/`) → únicamente `scoring-adv1-m3.py` (la definición
  del campo) y `tests/test_scoring_adv1_m3.py` (fixtures sintéticos de
  prueba, `nivel_ic=0.80` — declarado ahí mismo como no cargan celdas
  reales, no es una cita de pre-registro). `banda-tost-margen-v1_0.md §4`
  ("Qué falta para que mesa firme") enumera exactamente 3 pendientes, y
  ninguno es `nivel_ic`. `ADR-197` (que sella `F0`-`F3` íntegro) tampoco lo
  menciona. **No se elige un valor.**
- **`seed`**: misma búsqueda, mismo resultado — solo aparece en la
  definición del script y en fixtures de prueba (`seed=20260824`,
  `seed=11`, `seed=12`, todos etiquetados como sintéticos). **No se elige
  un valor.**

**Frase que gobierna esta sección, igual que en `prereg-corrida-v1_0.md`
F1:** *no se inventa el enlace donde el motor no tiene regla* — aplicada
aquí a los parámetros del scoring: no se inventa un valor donde mesa no
lo ha fijado. Si el resultado de intentar `ejecutar_scoring` con esto es
un fallo cerrado de validación, **ese fallo es el dato**, no un defecto
de este acto.

## 4 · Límite estructural adicional, declarado antes de correr (no solo `nivel_ic`/`seed`)

`construir_matriz_mediciones`/`_construir_universo` (`scoring-adv1-m3.py`)
agregan el valor de cada corredor **entre celdas** (bootstrap de la media
sobre el conjunto de celdas incluidas), no celda por celda contra su
propio árbitro. El campo que se agrega se llama `skill` y su ruta
canónica es `1 - error_corredor/error_baseline` (`skill()`,
`scoring-adv1-m3.py:394-398`) — una cantidad **normalizada**, comparable
entre celdas de escalas distintas. El corredor `B` (baseline) es
`SIN_BASELINE` en las 15 celdas (`corridas-R/_corredor-B.json`, rama (3)
del propio corredor, heredada sin recalcular — fuera de perímetro).
**Sin `B` no hay una `skill` legítima que poblar para ningún corredor en
ninguna celda** — no solo para `M`. Cargar los valores brutos de `L-solo`
(percentiles/medianas en unidades de cada variable, `%` de escalas
distintas) en el campo genérico `skill` produciría un promedio entre
celdas heterogéneas sin sentido estadístico — exactamente el tipo de
número fabricado que este programa existe para no producir. Este acto
**no puebla `skills` con valores brutos** por esa razón: la matriz de
mediciones se construye vacía (`mediciones: {}` en las 15 celdas), lo cual
es la representación honesta de "no hay skill computable para ningún
corredor, en ninguna celda, sin `B`".

Consecuencia encadenada, verificada por lectura del código (no por
corrida con valores inventados): aun si `delta`/`nivel_ic`/`seed`
existieran, `ejecutar_scoring` (`scoring-adv1-m3.py:1029-1048`) construye
el universo pareado de la comparación principal y, si
`paquete_principal["n_celdas"] == 0`, lanza
`ErrorScoring("SIN_CELDAS_PAREADAS", "ninguna celda contiene L
seleccionada y M evaluables")` **antes de calcular nada más**. Con `M` en
cero puntos sobre las 15 (§2) y `L_SOLO` sin `skill` poblado (párrafo
anterior), `n_celdas = 0` es la consecuencia lógica del propio dato, no
una suposición. `interval_score` y `crps_normal_aprox` están definidas en
el módulo pero **`ejecutar_scoring` nunca las invoca** en su cuerpo
(verificado leyendo la función completa, líneas 1029-1125): no hay una
salida de esas dos métricas que este acto pueda reportar sin calcularla
por fuera del script sellado, lo cual está prohibido (no se edita ni se
recalcula al margen del procedimiento congelado).

## 5 · Lo que SÍ se reporta sin la maquinaria de `ejecutar_scoring`

`dif` (`L-solo − R`) y la banda TOST (`±0.5·EE(R)` de esa misma celda) son
aritmética declarada, celda por celda, contra el árbitro real de cada
celda — exactamente el método que el marcador v1.0 ya usaba para estas
mismas 9 celdas computables (`prereg-corrida-v1_0.md` F3, regla de forma).
Esto no depende de `ejecutar_scoring` ni de `skill`/`B`: usa `L-solo`
(mediana de `corridas-L/`) y `R`/`EE_R` (`corridas-R/{celda}.json`)
directamente. Se recalcula en este acto para las 9 celdas computables y
se re-confirma idéntico al marcador v1.0 (ningún insumo de `L` ni `R`
cambió desde `E6`/`E7`).

## Frase de sello

**El primer resultado que produzca este procedimiento es el que se
reporta.**

---

## 6 · Resultado (COMMIT-2)

`python3 forense/prereg-duelo-v2/corridas-M/intento_scoring_e9.py`, salida
verbatim:

```json
{
 "resultado": "ErrorScoring",
 "codigo": "CONFIGURACION_INVALIDA",
 "mensaje": "faltan parámetros obligatorios: delta, nivel_ic, seed"
}
```

**El scoring real arranca un nivel más allá que en `E7`** (supera la
validación de corredores que `E8` relajó) **y falla cerrado en el
siguiente**: los tres parámetros de bootstrap que ningún acto anterior
pre-registró. Es el resultado que §3 anticipó antes de correr, verbatim,
sin segunda corrida con valores inventados para ver qué pasa después —
el hallazgo estructural adicional de §4 (`SIN_CELDAS_PAREADAS` esperado
incluso si los tres existieran) se deja como lectura de código, declarada
y citada, no como una segunda ejecución contaminada. Registro completo,
con el documento de entrada íntegro: `corridas-M/_intento-scoring-v1_1.json`.

**Esto no es un defecto de este acto ni, estrictamente, de `E8`**: `E8`
resolvió exactamente lo que su propio encargo le pedía (el contrato de
corredores). El hueco de `nivel_ic`/`seed` viene de más atrás —
`PREREG-CORRIDA`/`ADR-197` (25-26/ago/2026) selló `F0`-`F3` sin cubrir
estos dos de los cuatro campos que el script declara sin default. Se
reporta la genealogía, no se le asigna culpa a quien no la tiene:
ningún acto previo tenía en su encargo la instrucción de fijarlos.

Las cifras `dif`/banda TOST del marcador v1.1 (§5) no dependen de este
resultado — se computan directo contra el árbitro, celda por celda, sin
pasar por `ejecutar_scoring`.
