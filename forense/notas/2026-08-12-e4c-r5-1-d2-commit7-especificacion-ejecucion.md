# E4c · R5.1-D2 — Commit 7: especificación de ejecución congelada (Bloque A-bis/D)

**No reabre los Commits 1, 3, 4, 5 ni 6 — los cita y añade solo lo que falta para correr.** Todo lo de abajo se fija antes de abrir ningún desenlace sustantivo (`clase_hog`, `P040`). Lo único abierto para escribir este commit es lo que Commit 1 ya autorizaba abrir (clasificación por `P032`, ya parte de la especificación congelada) y la estructura de diseño (`est_dis`/`upm`/`factor`) — ningún dato de corresidencia ni de transferencia se leyó todavía.

## 1 · La llamada exacta

Por ola, sobre **todas** las personas de la ola (no filtradas — Commit 3 §3.3, regla heredada de `diff_ultimate_cluster`/`diff4_ultimate_cluster`: filtrar antes de llamar cambia la estructura de estratos/UPM y baja el SE en silencio):

- `diff4_ultimate_cluster(rows)` con `rows = (estrato, upm, peso, y, grupo)`, `grupo ∈ {"T","C","T2","C2",None}` — `grupo=None` para quien no sea 65+/55-64 clasificable. Una llamada por ola (2018, 2022).
- La resta entre olas, hecha por el llamador (Commit 5 §2 / ACTO S: `did4_ultimate_cluster` no existe y no se implementa aquí — fuera de perímetro, `tests/` no se toca): `DDD = d4_hat_post − d4_hat_pre`, `Var(DDD) = Var(d4_post) + Var(d4_pre)` — válido porque 2018 y 2022 son muestras transversales independientes (mismo argumento que sostiene `did_ultimate_cluster`).
- El DiD principal de 2 celdas (T/C, banda 65+) sale de `did_ultimate_cluster(rows_pre, rows_post)` directamente — ya existente, sin cambio.
- Diseño: `est_dis`/`upm`/`factor` de `concentradohogar` de cada ola (Commit 1 §2.5, sin cambio).
- `folioviv`: ancho derivado de la primera fila de `concentradohogar` de cada ola (mecanismo de ACTO J, PR #180 — no `zfill(10)` fijo). **Verificado ahora, no supuesto:** ventana de este acto = 2018, 2022. Ancho derivado: **2018 → 10 caracteres, 2022 → 10 caracteres** — ambos coinciden con lo ya sabido (2018 se corrige de su truncamiento nativo al ancho real de `concentradohogar`; 2022 ya nace en 10). Ninguna ola de esta ventana tiene el esquema `C(6)` de 2012 — no aplica aquí, declarado para que quede explícito que se verificó, no se asumió.

## 2 · Magnitud mínima detectable (MDE) — declarada antes de ver ningún desenlace

**Método:** con la estructura de diseño real (pesos, estratos, UPM de `concentradohogar`, tamaños de grupo por `P032`) pero un desenlace **simulado** `y ~ Bernoulli(0.5)` (semilla fija `20260812`, declarada, sin relación con `clase_hog` ni `P040`) — la varianza máxima posible de una proporción, para no subestimar el SE real. No es un desenlace sustantivo: es la forma estándar de correr un cálculo de potencia sin abrir el dato que se va a falsar.

Tamaños de grupo (por `P032`, ya parte de Commit 1 — no es el desenlace):

| | 2018 T | 2018 C | 2022 T | 2022 C |
|---|---|---|---|---|
| 65+ (principal) | 6,160 | 14,591 | 8,877 | 19,749 |
| 55-64 (control, T2/C2) | 2,980 | 15,568 | 4,084 | 19,375 |

| Contraste | SE (peor caso) | MDE 95% |
|---|---|---|
| DiD principal (2 celdas, 65+) | 0.014028 | **±2.75pp** |
| DDD (4 celdas) | 0.024142 (= √(0.018454² + 0.015566²)) | **±4.73pp** |

**Razón MDE_DDD/MDE_DiD = 1.72×.** `n_estratos_singleton` en ambos contrastes, ambas olas: **0** — sin advertencia de singleton que leer.

**Decisión, declarada aquí:** ambos MDE caen cómodamente bajo los dos umbrales operativos de §6 (10pp de la fila A, 20pp de la fila E) — ninguno de los dos contrastes está, en abstracto, subpotenciado para el diseño. Pero el DDD es **1.72× menos preciso** que el DiD principal, un costo real, no marginal: cerca de cualquiera de los dos umbrales, un CI 72% más ancho es sustancialmente más propenso a no despejarlo (A-bis regla del Paso 3: un punto que satisface el umbral con IC que no lo despeja no adjudica). **El DDD entra como robustez declarada, no como estimando principal — el §6 adjudica sobre el DiD de dos celdas.** Se reporta igual, con su propio IC, pero no decide la fila si difiere del DiD principal en si despeja o no.

## 3 · Contadores de singleton — salida obligatoria, ya verificados en §2

Reportados arriba con el placeholder de MDE (0/0 en ambos contrastes, ambas olas). Se vuelven a reportar en Commit 8 con el desenlace real — si cambiaran de 0 a algo distinto de cero al pasar de `y` simulado a `y` real, sería porque la estructura de UPM/estrato cambió entre la corrida de MDE y la corrida real, lo cual no debería pasar (mismas filas, mismo `grupo`, mismo diseño) — declarado como chequeo de consistencia a verificar en Commit 8, no asumido igual sin más.

## 4 · Escala de veredicto vigente — citada de §9 tras Paso 3 §0.1

`forense/r5-1-diseno-por-regla-preregistro-v1_0.md` §9 (enmendado 12/ago/2026 por ADR-71(b), reubicado por Paso 3 §0.1 de este mismo acto):

- Orden de precedencia: **A → E → B → C → D**.
- Fila E es de **un solo nivel** — no distingue "decisivo en uno de los dos desenlaces" de "decisivo en ambos". Si ambos desenlaces resultan decisivos en Commit 8, se reporta cuántos cruzaron el umbral (transparencia), pero el estado de registro sigue siendo el mismo — no hay un nivel más fuerte que el diseño sellado contemple.
- "Monto insuficiente" (cláusula de B) gana sobre E **sin excepción por magnitud del DiD** — resuelto por ADR-71(b), no por este acto (Commit 6).
- Mapeo al vocabulario del registro de llaves (Commit 1 §3, reconciliado por Commit 6 §2): fila A → `EJERCIDA_REFUTA`; fila E → `EJERCIDA_ACOTA` (única fila de corroboración vigente para R5.1-D2 — `EJERCIDA_CORROBORA` propia de este acto queda retirada); fila B → `EJERCIDA_INDECISA`; filas C/D → `NO_EJECUTABLE` o archivo por diseño, según corresponda.

## 5 · Cierre

**El primer resultado que produzca este procedimiento, sobre los dos desenlaces de §5 del pre-registro, con la escala de §6/§9 tal como quedó tras Paso 3 §0.1, es el que se reporta en Commit 8.**

---

*Commit 7 de este acto (Bloque A-bis/D). No edita Commits 1, 3, 4, 5 ni 6. Solo especificación de ejecución — ningún desenlace sustantivo abierto, ningún resultado producido. No se edita jamás.*
