# ACTO S · `diff4_ultimate_cluster` — la variante de 4 celdas que E4c Commit 5 declaró y no implementó

**Por qué existe.** E4c/R5.1-D2 Commit 4 (§3, triple diferencia) propuso construir el DDD sumando dos salidas independientes de `did_ultimate_cluster` (una sobre 65+, otra sobre 55-64). Commit 5, tras un TRANSFER de auditoría de mesa sobre PR #176 verificado independientemente antes de aceptarlo, encontró que esa construcción reutiliza el argumento de independencia *entre olas* de `did_ultimate_cluster` para una resta *dentro de una ola* — las dos bandas de edad comparten estrato/UPM (un hogar con una persona en cada banda aporta a las dos desde la misma UPM), así que `Var((p_T-p_C)-(p_T2-p_C2)) ≠ Var(p_T-p_C) + Var(p_T2-p_C2)` en general. Commit 5 declaró la construcción correcta y la retiró sin implementarla, por perímetro (no toca `tests/`). Este acto la implementa.

## 1 · La función

`diff4_ultimate_cluster(rows)` en `tests/svystat.py`, extensión directa de `diff_ultimate_cluster`: `rows` es `(estrato, upm, peso, y, grupo)` con `grupo ∈ {"T","C","T2","C2",None}`. El residual linealizado es la resta de dos residuales de `diff_ultimate_cluster` — el de T-vs-C menos el de T2-vs-C2 — agregado por UPM antes de tomar varianza, no una función de otra familia:

```
z_i =   1{i∈T}  * w_i(y_i-p_T)  / N̂_T
      - 1{i∈C}  * w_i(y_i-p_C)  / N̂_C
      - 1{i∈T2} * w_i(y_i-p_T2) / N̂_T2
      + 1{i∈C2} * w_i(y_i-p_C2) / N̂_C2

var(d4_hat) = Σ_h [ (m_h/(m_h-1)) · Σ_i (z_hi - mean_i(z_hi))² ]
```

Cinco decisiones heredadas de `diff_ultimate_cluster`, sin política nueva (docstring completo en el propio código): unidades fuera de las 4 celdas permanecen y aportan `z_i=0` (estimación de dominio, no submuestreo); singleton salta y se cuenta; cuantil `1.959963985`; `rows = list(rows)`; celda vacía → `None` (extensión de la regla existente, con las cuatro lecturas sustantivas declaradas en el docstring para quien audite un `None`).

**Lo que NO se implementó, por contrato explícito del encargo:** un `did4_ultimate_cluster` que combine dos olas. "Entre olas no se implementa nada nuevo... es la resta que el llamador hace con dos salidas de esta función" — el argumento de independencia entre-olas ya está resuelto en `did_ultimate_cluster`; combinar dos llamadas a `diff4_ultimate_cluster` (post y pre) con `Var = Var(post)+Var(pre)` queda para quien corra el Paso 3 de E4c.

## 2 · Verificación — cuatro casos, dos con forma cerrada derivada a mano

Antes de fijar los valores esperados en `tests/test_svystat.py`, cada derivación se verificó numéricamente contra la implementación (script de scratch, no commiteado) — ninguna cifra se tecleó sin correr el cálculo primero.

- **Caso 1 (degenerado a `diff_ultimate_cluster`):** mismo dataset T/C del Caso 1 de ENCARGO B (`d=5/12`, `se=√(1463/10368)`, ya validado) más una fila T2 y una C2, cada una sola en su propio estrato (`y=0` → `p_T2=p_C2=0` exacto, el término de control se anula, ambas son singleton y no aportan varianza). `d4_hat` y `se` coinciden con `diff_ultimate_cluster(T,C)` a `1e-12`.
- **Caso 2 (el que justifica la función):** 6 UPM, las cuatro celdas en cada una, covarianza positiva por diseño entre la brecha T-C y la brecha T2-C2 (una UPM rompe el patrón, mismo criterio que el Caso 3 de ENCARGO B para evitar covarianza perfecta). `se(diff4)=0.325280` vs. `se` de la suma ingenua de dos `diff_ultimate_cluster` independientes `=0.563448` — difieren en `0.238168`, y en la dirección que la teoría predice (`Var(A-B)=Var(A)+Var(B)-2·Cov(A,B)`, covarianza positiva → SE correcto menor). La construcción que E4c Commit 4 proponía habría sobreestimado el SE en este dataset por un margen amplio, no marginal.
- **Caso 3 (singleton):** una sola UPM con las cuatro celdas — `d4_hat=1.0` calculable, `se=0.0` exacto, `n_estratos_singleton=1` — mismo patrón que `test_estrato_singleton()`.
- **Caso 4 (forma cerrada, el otro extremo del Caso 2):** T/C y T2/C2 en estratos SRS **distintos**, sin ninguna UPM compartida — por diseño, sin mecanismo de covarianza. Forma cerrada: `var(d4) = var(T,C) + var(T2,C2)`, la suma de dos formas cerradas ya validadas por separado (`1463/10368 + 5/54 = 2423/10368`). Coincide exacto — confirma que la función no inventa covarianza donde genuinamente no la hay, no solo que la detecta donde sí.

`python3 tests/test_svystat.py`: 13/13 casos coinciden (9 preexistentes + 4 nuevos). `python3 tests/check.py --baseline`: LÍNEA BASE VERDE, 22 FAIL · 101 WARN, sin cambio.

## 3 · Perímetro

Solo `tests/svystat.py` (una función nueva, `prop_/diff_/did_ultimate_cluster` sin modificar — verificado que sus bytes no cambiaron más allá del docstring del módulo) y `tests/test_svystat.py` (cuatro casos nuevos, los nueve existentes sin tocar). No se abrió microdato, no se tocó ninguna nota de E4c, no se toca `tools/`, `canon/`, `data/`.

## 4 · Lo que este acto habilita

El Paso 3 de E4c (la corrida real de R5.1-D2) deja de estar bloqueado por la ausencia de un estimador de varianza correcto para la triple diferencia. No corre nada de R5.1-D2, no adjudica ninguna fila del §6 — eso sigue siendo trabajo de E4c, sobre su propio microdato, con la especificación que sus Commits 1-5 ya fijaron.
