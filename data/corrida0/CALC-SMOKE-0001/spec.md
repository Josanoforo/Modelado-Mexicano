# `CALC-SMOKE-0001` — replay sellado del agregado v1.3 (SMOKE de GEN2-E3)

**Acto:** `GEN2-E3 · AUTOMATIZA-GEN2-1` (7/sep/2026).
**Generación:** `LEGACY-GEN1` · **Tipo:** `REPLAY-SMOKE` ·
**Cuenta para el contador GEN2:** `NO` ·
**Validación independiente:** `NO-HECHA`.

## 1 · Qué se mide y por qué existe esta spec

Nada nuevo. Este `CALC` vuelve a ejecutar un cálculo **que ya ocurrió en
GEN1** — el agregado sellado `forense/prereg-duelo-v2/agregado_v1_3.py`,
que aplica el procedimiento `procedimiento-scoring-v1_2.md` sobre las 14
celdas de `marco-M-sorteado-v1_3.tsv` — con el aparato de corrida de GEN2
(`corrida0 preflight` → `run` → `verify`).

El objeto medido de esta spec **no es el duelo**: es el aparato. Lo que se
comprueba es que `preflight` sabe bloquear, que `run` sabe sellar y que
`verify` sabe reejecutar y comparar contra una tolerancia declarada. Que el
número reproduzca es la prueba; el número en sí ya estaba, y **citarlo como
si fuera una medición GEN2 sería falso** — por eso las cuatro etiquetas de
arriba viajan hasta `ejecucion.json` y no se pueden perder por el camino.

## 2 · Interfaz

`data/corrida0/CALC-SMOKE-0001/medidor.py` expone la interfaz estable del
plan v2.0 §4 (B-1):

    medir(inputs, params) -> {"RESULT-…": valor}

El medidor es un **adaptador**: importa `agregado_v1_3.py` por ruta y no le
edita una línea (el perímetro del acto excluye `forense/prereg-duelo-v2/`).
Ignora deliberadamente `inputs` — el script legacy resuelve sus rutas
relativas a su propio directorio, e inyectarle otras haría que el replay
dejara de ser un replay. Los `inputs` de `spec.yaml` existen para que
`preflight` y `verify` los **hasheen**, que es lo que se les pide.

## 3 · Resultados declarados

| id | qué es |
|---|---|
| `RESULT-SMOKE-PRINCIPAL-{PUNTO,IC-LO,IC-HI}` | comparación pareada principal `L_SOLO vs M` (banda `z`, veredicto primario de v1.1, intacto) |
| `RESULT-SMOKE-SECUNDARIA-{PUNTO,IC-LO,IC-HI}` | comparación `L_CORPUS vs M` |
| `RESULT-SMOKE-N-CELDAS-UNIVERSO` | 14 — control de forma: si el universo cambia, esto deja de ser el mismo cálculo |
| `RESULT-SMOKE-REPLICAS` · `RESULT-SMOKE-SEED` | `10000` · `42`, los parámetros sellados del duelo |

## 4 · Parámetros, seed y tolerancia

Parámetros y `seed` **no los elige esta spec**: los copia verbatim de
`parametros_sellados` del procedimiento v1.2 (`seed=42`, `replicas=10000`,
`nivel_ic=0.95`, `delta=0.5`). Cambiarlos aquí sería re-pre-registrar un
duelo por la puerta de atrás.

Tolerancia declarada: **`tipo: flotante`, `abs: 1e-10`**, la de la casa para
flotantes (encargo P1). Se elige esa y no `exacto` con razón fechada: el
7/sep/2026 dos corridas del mismo agregado sobre el mismo árbol difirieron
en **3·10⁻¹⁵ en `ic_hi`** — orden de magnitud del error de redondeo de
`float64` en una suma reasociada, no una diferencia de cálculo. `1e-10` deja
pasar eso y sigue atrapando cualquier cambio real: cinco órdenes de magnitud
de margen sobre el ruido observado, y once por debajo del valor medido.

Los enteros (`N-CELDAS-UNIVERSO`, `REPLICAS`, `SEED`) se comparan **exacto**:
`corrida0` aplica la tolerancia por tipo del valor, no por tipo de la spec, y
un entero que no cuadra no cuadra.

## 5 · Insumos

Los seis `inputs` de `spec.yaml` son archivos **versionados en el repo**
(`origen: repo`), con su `sha256` declarado: los cuatro `.py` de la cadena
de importación y los dos `.tsv` que fijan el universo y la captura `L`.

**Límite declarado.** `agregado_v1_1.py` lee además los directorios
`corridas-R/`, `corridas-M/` y `corridas-L/` completos, y `agregado_v1_3.py`
resuelve `M-<id>__v1_3.json → M-<id>.json → M-<id>__v1_2.json` por celda.
Esos archivos **no se enumeran uno por uno** en `inputs`: su identidad
colectiva queda cubierta por `git_commit` en `ejecucion.json`, que fija el
árbol entero. Se dice aquí porque un `inputs` que aparenta ser exhaustivo y
no lo es vale menos que uno corto con su límite escrito.

Este `CALC` **no abre microdato**: corre entero sobre insumos versionados, y
por eso no necesita corpus ni Ubuntu.

## 6 · `variables` (spec-check)

Vacío, y es una declaración, no un olvido: este cálculo no lee ningún
reactivo de ningún instrumento — consume artefactos ya derivados. `spec-check`
sobre esta spec examina los tres inventarios vigentes y reporta cero pares
declarados. La prueba de `spec-check` con pares reales vive en
`tests/test_corrida0.py` (caso `iiib_hs.dta::hs02g` vs `p_hs.dta::hs02g`).

## 7 · Veredicto esperado

`preflight` VERDE → `run` → `verify` → **`REPRODUCE`**.
