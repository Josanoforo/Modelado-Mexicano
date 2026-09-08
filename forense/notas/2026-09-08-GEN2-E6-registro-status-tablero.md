# ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 — registro, status, tablero, T-REPRO en modo aviso

**Fecha.** 8/sep/2026 · **Entorno.** NUBE, sin corpus ni red · **Encargo.** `forense/encargos/2026-09-08-GEN2-E6-AUTOMATIZA-GEN2-2.md` (verbatim, 0-bis A.3) · **ADR.** `ADR-397`

---

## 0 · Dos arranques el mismo día, y por qué el primero cerró con cero commits

Este acto se lanzó **dos veces**. El primer intento hizo el ARRANQUE completo, verificó la compuerta por producto y **cerró con CERO COMMITS**:

```
$ git show origin/main:instrucciones-proyecto-v2_13.md
fatal: path 'instrucciones-proyecto-v2_13.md' does not exist in 'origin/main'
$ git show origin/main:instrucciones-proyecto-v2_13.md 2>/dev/null | grep -c "Bloque E"
0
```

`v2_13` no existía en `main` (la versión vigente era `v2_12`) y `forense/hallazgos.md:536` documenta por qué no era un descuido: las instrucciones se acumulan como entradas `PARA-v2.13` hasta que dirección entregue el archivo íntegro. Compuerta no cumplida → cero commits, sin adelantar «por si acaso» ningún paso del acto (`/acto` §2.3, defecto que `ADR-224`/`ADR-234` pagaron dos veces).

Entre los dos intentos fusionaron `PR #609` (`ACTO GEN2-V213`, que selló `v2_13`) y `PR #610` (`ACTO GEN2-E3-1-1`). En el relanzamiento, **antes de escribir una sola línea**, se revisaron los dos PR para ver si algo de este encargo ya estaba resuelto:

| PR | qué trajo | ¿resuelve algo de `GEN2-E6`? |
|---|---|---|
| `#609` · `GEN2-V213` | `instrucciones-proyecto-v2_13.md` (Bloque E, regla E.5), reencola `GEN2-E5-0`/`GEN2-E5`/`GEN2-E6`/`GEN2-E7`, y `GEN2-E6` pasa de `GATEADO` a `LISTO-NUBE` | **No.** Toca la cola y las instrucciones, no `corrida0.py`. Lo que sí hace es **abrir la compuerta** de este acto. |
| `#610` · `GEN2-E3-1-1` | los cuatro cables materiales del runner (D1–D4), 45 tests | **No.** Su propio cuerpo lo declara verbatim: «**No implementó `registro`/`status`/`vigencia`/`delta`**». |

Verificado además por producto sobre `origin/main = 0405879c`: `grep -n "^def cmd_registro\|^def cmd_status" ` sobre `tools/corrida0.py` → **0 aciertos**; `data/corrida0/` traía solo `CALC-SMOKE-0001`, `CALC-SMOKE-0002`, `decisiones.tsv` y los dos `demanda-*.tsv`. Nada de este encargo estaba hecho.

## 1 · Compuerta (relanzamiento), por producto

```
$ git show origin/main:instrucciones-proyecto-v2_13.md | grep -c "Bloque E"
2                     # >= 1 exigido -> CUMPLIDA
```

La compuerta v1.3 que vive en el archivo de cola (`≥2 directorios CALC-* sellados con esquema completo`, recomputada por `GEN2-V213` bajo la regla nueva **E.5** de `v2_13`, «el aparato se prueba con replays») también se cumple: `CALC-SMOKE-0001` y `CALC-SMOKE-0002`, sellados bajo `ADR-394`. Las dos formulaciones coinciden en el veredicto.

## 2 · A.8 — el terreno antes de tocarlo

| comando | salida | lectura |
|---|---|---|
| `grep -c "^def cmd_registro\|^def cmd_status" tools/corrida0.py` (en `main`) | `0` | los dos subcomandos seguían declarados y vacíos |
| `ls data/corrida0/` (en `main`) | `CALC-SMOKE-0001 · CALC-SMOKE-0002 · decisiones.tsv · demanda-corridas.tsv · demanda-resultados.tsv` | ninguna de las tres vistas existía |
| `grep -n "T3[0-9]" tests/check.py` | `T30 · T31 · T32 · T34` | `T33` libre pero **`T35` es el contiguo** tras `T34 · T-NO-CORRIDO` (de ahí el cambio de número respecto de la v1.3, que decía `T33`) |
| `grep -rn "corrida0_resultado_id" milpa/` | `0` | **ningún consumidor es GEN2 todavía**: por eso el check nuevo pasa por vacío, y por eso `dependencias_numericas_legacy_activas == N_resultados_activos` |
| filas de datos de `demanda-corridas.tsv` / `demanda-resultados.tsv` | `79` / `162` | las cifras que el encargo declara para `status` |

## 3 · Lo que se construyó

**`cmd_registro`** une los dos lados del plan v2.0 §5 y emite `corridas.tsv` (22 columnas · 81 filas), `resultados.tsv` (18 · 180) y `usos.tsv` (8 · 162), todas con `# DERIVADO — NO EDITAR`. Determinista: dos derivaciones seguidas dan bytes idénticos (`sha256sum -c`, verificado). Ocho validaciones **paran sin escribir nada** y tres **avisan**, exactamente las del plan.

**`cmd_status`** deriva §9 de esas filas **en memoria** — no de los TSV en disco, porque un contador leído de un archivo que nadie re-derivó es justo el defecto que este aparato existe para no repetir.

**El tablero** lee esos contadores del CLI (no los recalcula) y pierde dos hardcodes históricos. **`T35 · T-REPRO`** entra en modo aviso. **Nueve tests** de punta a punta sobre fixtures (45 → 54).

## 4 · Dos lecturas que el registro corrigió al derivar

Las dos aparecieron corriendo el código contra el árbol real, no razonando sobre él. Ninguna se «arregló» tocando el artefacto sellado.

**(a) La unicidad de un `resultado_id` es POR CORRIDA, no global.** El primer `registro` paró con `ID-DUPLICADO: RESULT-SMOKE-N-CELDAS-UNIVERSO aparece dos veces`. Correcto que parara, equivocada la razón: `CALC-SMOKE-0002` declara `repite_de: CALC-SMOKE-0001` y reproduce sus nueve `RESULT-SMOKE-*` **a propósito** — eso es lo que significa replicar. Una unicidad global habría vuelto imposible todo replay, que es la pieza sobre la que la regla E.5 apoya el aparato entero. La validación quedó: unicidad por `(corrida, resultado)`, y el mismo id en dos corridas **sin** cadena `repite_de` sí PARA (probado por fixture).

**(b) `CALC-SMOKE-0001` no trae `spec_yaml_sha256`.** Se selló bajo el runner de `GEN2-E3`; el campo lo añadió `GEN2-E3-1`, después. Es `LEGACY-GEN1 · cuenta_gen2 = NO`, así que el endurecimiento no le aplica, y **su sello no se reescribe para complacer al registro**: fabricar el hash sería exactamente la evidencia falsa y sellada que `ADR-396` cerró cuatro cables para no producir. Queda como aviso `HASH-AUSENTE-EN-LEGACY`, contado aparte. El mismo hueco en un CALC con `cuenta_gen2 = SI` **sí PARA** (probado por fixture). Es «la línea base congela GEN1» aplicada a un caso medido.

## 5 · Las cifras de hoy, y por qué el cero es correcto

```
$ python3 tools/corrida0.py status
N_corridas_requeridas=79            N_corridas_selladas=0
N_resultados_activos=162            N_resultados_sellados=0
N_resultados_pendientes=162         dependencias_numericas_legacy_activas=162
resultados_con_validacion_independiente=0   diferencias_materiales=0
no_corrido_abiertas=9               replays_legacy_sellados=2
```

`0 / 79`, `0 / 162` y `162 legacy activas` son **la lectura correcta, no un error**: `GEN2-E6` corre *antes* de `GEN2-E5` por decisión de mesa, así que no existe todavía ninguna corrida GEN2. Los dos replays sellados están contados aparte y no suman ni una unidad (hay un test que lo comprueba sobre el árbol de verdad). `diferencias_materiales = 0` porque no hay `valor_gen2` que comparar y el criterio de materialidad lo firma `delta` (B-7, `GEN2-E7`): se declara, no se calla. `no_corrido_abiertas` leía **6** al derivar P2 y hoy lee **9** porque este mismo acto asienta sus tres reservas — el contador es derivado, y que se mueva solo es la prueba de que lo es.

## 6 · Por qué T-REPRO entra en aviso y cuándo deja de estarlo

El gate solo puede congelarse contra una corrida GEN2 **verdadera**. Hoy no existe ninguna: congelar el FAIL contra un universo vacío sería declarar verde un test que nunca se ejerció. Por eso `T35` usa `warn()` y **pasa a `fail()` en el cierre de `GEN2-E5`** — declarado aquí, en el comentario de cabecera del propio test y en `ADR-397`.

Dos decisiones dentro de esa: (1) `warn()` y no `senal()`, porque `warn` **sí entra en la comparación de línea base** — un aviso NUEVO ya es una regresión detectable hoy, no dentro de dos actos; (2) el check `(11.2)` de inmutabilidad **sí** se aplica a los replays `LEGACY-GEN1`: no cuentan como medición GEN2, pero un sello es un sello. Sobre los dos smokes `T35` pasa **limpio**.

**A.13 — el límite de este acto.** `T35` no se ejerció nunca contra un RESULT GEN2 real, porque no existe: (a), (b), (c) y (11.1) corren hoy sobre un universo vacío. Lo que sí está falsado es el mecanismo: `t_repro_atrapa_valor_movido` construye el caso GEN2 completo en un fixture y comprueba que mover la cifra materializada sin mover el RESULT da distinto — sin ese caso, `T35` sería un test que no puede fallar. La verificación contra dato real es de `GEN2-E5`.

## 7 · Falsadores

Los nueve tests nuevos se falsaron por **mutación deliberada** sobre `tools/corrida0.py`, restaurando el archivo después de cada una:

| mutación | qué falló | ¿el test correcto? |
|---|---|---|
| la unicidad deja de comparar el id | `T-REGISTRO-PARA-DUPLICADO: no paro por id duplicado` | sí, y solo ese |
| `_verifica_ciclos` se vuelve `pass` | `T-REGISTRO-PARA-CADENA: el ciclo no paro` | sí, y solo ese |
| `gen2()` deja de filtrar por `cuenta_gen2` | `T-STATUS-SMOKES` (×2) y `T-STATUS` (×2): «un replay GEN1 conto como GEN2» | sí, los cuatro |

## 8 · Perímetro y lo que NO se tocó

Cumplido: `tools/corrida0.py` (solo `cmd_registro`/`cmd_status`; `preflight`/`run`/`verify` intactos) · `tools/tablero_programa.py` · `tests/test_corrida0.py` · `tests/check.py` · `data/corrida0/{corridas,resultados,usos}.tsv` · `forense/no-corrido.tsv` · cascada (`gobernanza` `ADR-397`, `estado-programa` L0 + los tres contadores por `cierre_acto.py --aplica`, `registro-rotulos`, exención T25 por ARCHIVO, `data/INFRAESTRUCTURA-v1_0.md` por T27).

**No se tocó** `milpa/**`, canon de reglas, specs, `data/manifiesto.yaml`, `CALC-SMOKE-0001/0002` ni valor alguno del modelo. **`NC-0007`/`NC-0008` no se cierran** y `forense/tablero/TABLERO-PROGRAMA.md` no se regenera: las tres razones son de perímetro y están en `## NO-CORRIDO / RESERVAS` del encargo, con sucesor nombrado (`NC-0012`/`NC-0013`/`NC-0014`).

**Contador: cero directo.** Este acto no mide nada. Lo que cambia es que el tablero pasa a derivar GEN2 con `0/N` explícito en vez de callarlo.
