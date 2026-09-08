# `CALC-SMOKE-0002` — replay sellado del agregado v1.3, bajo el runner endurecido (SMOKE de GEN2-E3-1)

**Acto:** `GEN2-E3-1 · READINESS-DEL-RUNNER` (8/sep/2026). **`repite_de`:**
`CALC-SMOKE-0001`.
**Generación:** `LEGACY-GEN1` · **Tipo:** `REPLAY-SMOKE` ·
**Cuenta para el contador GEN2:** `NO` ·
**Validación independiente:** `NO-HECHA`.

## 1 · Qué se mide y por qué existe esta spec

Lo mismo que `CALC-SMOKE-0001` medía: nada nuevo. Este `CALC` vuelve a
ejecutar el cálculo que ya ocurrió en GEN1 — el agregado sellado
`forense/prereg-duelo-v2/agregado_v1_3.py` — con el aparato de corrida de
GEN2 **ya endurecido** por `ACTO GEN2-E3-1 · READINESS-DEL-RUNNER` (P1-P6):
resolver único de payload, contrato ejecutable normalizado, outputs
validados, inmutabilidad y sello completo, `verify` en dos ejes.

`CALC-SMOKE-0001` queda **intacto** (el acto no lo toca): este `CALC` nace
aparte, con `repite_de: CALC-SMOKE-0001` declarado en `spec.yaml`, y es el
que prueba que el runner endurecido reproduce exactamente lo mismo que el
runner original — mismo cálculo, mismo resultado, `verify` en
`REPRODUCE`/`IDENTICO`.

El objeto medido de esta spec **no es el duelo**: es el aparato, ahora con
seis piezas más estrictas. Que el número reproduzca es la prueba; el número
en sí ya estaba, y **citarlo como si fuera una medición GEN2 sería falso** —
por eso las cuatro etiquetas de arriba viajan hasta `ejecucion.json` y no se
pueden perder por el camino.

## 2 · Interfaz

`data/corrida0/CALC-SMOKE-0002/medidor.py` expone la interfaz estable
endurecida por P2:

    medir(inputs, contrato) -> {"RESULT-…": valor}

(`CALC-SMOKE-0001/medidor.py` exponía `medir(inputs, params)` — la spec
vieja no cambia, y el runner acepta ambas formas porque el contrato es el
SEGUNDO argumento posicional, no algo que el medidor tenga que declarar por
nombre.) El medidor es un **adaptador**: importa `agregado_v1_3.py` por ruta
y no le edita una línea (el perímetro del acto excluye
`forense/prereg-duelo-v2/`). Ignora deliberadamente `inputs` y `contrato` —
el script legacy resuelve sus rutas relativas a su propio directorio, e
inyectarle otras haría que el replay dejara de ser un replay. Los `inputs`
de `spec.yaml` existen para que `preflight` y `verify` los **hasheen**.

## 3 · Resultados declarados

Cada uno declara `tipo` y `unidad` (P3 — antes no era obligatorio):

| id | tipo | unidad | qué es |
|---|---|---|---|
| `RESULT-SMOKE-PRINCIPAL-{PUNTO,IC-LO,IC-HI}` | flotante | `z` | comparación pareada principal `L_SOLO vs M` (banda `z`, veredicto primario de v1.1, intacto) |
| `RESULT-SMOKE-SECUNDARIA-{PUNTO,IC-LO,IC-HI}` | flotante | `z` | comparación `L_CORPUS vs M` |
| `RESULT-SMOKE-N-CELDAS-UNIVERSO` | entero | `celdas` | 14 — control de forma: si el universo cambia, esto deja de ser el mismo cálculo |
| `RESULT-SMOKE-REPLICAS` | entero | `replicas` | `10000`, el parámetro sellado del duelo |
| `RESULT-SMOKE-SEED` | entero | `adimensional` | `42`, la semilla sellada del duelo |

## 4 · Parámetros, seed y tolerancia

Parámetros y `seed` **no los elige esta spec**: los copia verbatim de
`parametros_sellados` del procedimiento v1.2 (`seed=42`, `replicas=10000`,
`nivel_ic=0.95`, `delta=0.5`) — igual que `CALC-SMOKE-0001`. La diferencia
endurecida (P2): `seed` se declara `{aplica: true, valor: 42, rng:
numpy.PCG64}` en vez de un entero suelto — `aplica: true` porque el
bootstrap de 10 000 réplicas sí depende de la semilla, no se inventa una
donde no aplicaría.

Tolerancia declarada: **`tipo: flotante`, `abs: 1e-10`**, la misma razón
fechada que `CALC-SMOKE-0001` — el 7/sep/2026 dos corridas del mismo
agregado sobre el mismo árbol difirieron en 3·10⁻¹⁵ en `ic_hi` (redondeo de
`float64`). Los enteros se comparan **exacto**.

## 5 · Insumos

Los mismos seis `inputs` de `CALC-SMOKE-0001/spec.yaml`, `origen: repo`, con
su `sha256` declarado. **Límite declarado**, igual que en `CALC-SMOKE-0001`:
`agregado_v1_1.py` lee además `corridas-{R,M,L}/` completos, cubiertos por
`git_commit` en `ejecucion.json`, no enumerados uno por uno.

`dependencias_materiales` declarado: `[]` — la cadena completa
(`agregado_v1_1/v1_2/v1_3.py`, `statistics` de la librería estándar) no usa
`numpy`/`pandas`/`scipy`/`pyreadstat`; confirmado porque `CALC-SMOKE-0001`
ya corrió con las cuatro `AUSENTE` en `firma_entorno.dependencias_
materiales` y produjo exit_code 0.

Este `CALC` **no abre microdato**: corre entero sobre insumos versionados.

## 6 · `variables` (spec-check)

Vacío, declarado — igual que `CALC-SMOKE-0001`: este cálculo no lee ningún
reactivo de ningún instrumento.

## 7 · Veredicto esperado

`preflight` VERDE → `run` → `verify` → **`REPRODUCE`** (`CONTEXTO=IDENTICO`
· `RESULTADO=REPRODUCE`) — mismos números que `CALC-SMOKE-0001`, bajo el
runner endurecido.
