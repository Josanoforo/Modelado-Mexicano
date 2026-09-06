# S10 · Pre-registro de `MAESTRA38-L2` rama LISTA — `list::mexico` (subconjunto MPS-2012 ola 2)

### `prereg-caja-S10-L2-LISTA` · **v1.0** · 6 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/S10-L2-LISTA-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-S10-L2-LISTA`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro de caja para el acto que abra `data/mexico.tab` (paquete `list::mexico`, `github.com/SensitiveQuestions/list @ e088e5f`, `sha256 fe101499b591d90d9e2122f439e26306fcdeab443e42d14f9455e9efa1c04488`, 1 004 filas × 25 variables) — la opción **A** de `MAESTRA38-N15 §3`: convierte P3 (experimento de lista) de PROPUESTA de medición a medición de primera mano, sobre un subconjunto de MPS-2012 ola 2. |
> | **QUÉ NO ES** | No abre `data/mexico.tab`. No calcula ningún IC95, ninguna diferencia de medias, ninguna celda. No mueve `R7.3`/`R7.6` (0 de sus variables están en este dataset — §1). No sustituye la rama TEXTO ni MEDICIÓN de `S2-L2` sobre el `.dta` completo de ICPSR 35024: es un instrumento paralelo, más chico, ya abierto, no un reemplazo. |
> | **VERIFICAS ASÍ** | Caja, al abrir `data/mexico.tab`, compara nombres de columna reales contra §1; compara `n` real contra §1.1; compara wording de `man/mexico.Rd` contra §4 (heredado de la Procedencia de `MAESTRA38-N15`, no reverificado aquí — este acto no toca red). |

**Acto:** `ACTO MAESTRA38-N15 · SPEC-L2-LISTA`, 6/sep/2026, entorno **NUBE**, sobre `origin/main = a5350e59`, `COMPUERTA: ninguna` — no toca red ni corpus, sólo escribe esta spec.

---

## 0 · Procedencia y continuidad de rótulo, declarada

Este documento es un pre-registro **hermano** de `prereg-caja-S2-L2` (`forense/prereg-caja/S2-L2-spec-v1_0.md`), no su sucesor: `S2-L2` fija MEDICIÓN/TEXTO sobre el `.dta` completo y restringido de ICPSR 35024 (pendiente de solicitud de mesa, `FP-316`, §1 de `2026-09-06-MAESTRA38-N15-SPEC-L2-LISTA.md`); `S10-L2-LISTA` fija el mismo tipo de pre-registro sobre el subconjunto público `list::mexico`, ya abierto byte a byte hoy sin necesidad de esa solicitud. Ambos alimentan el mismo rótulo de acto, `MAESTRA38-L2`, por dos rutas de dato distintas — la caja decide cuál corre primero según cuál microdato llegue primero (mismo criterio de `S2-L2 §3`, aplicado ahora a dos fuentes en vez de dos ramas).

**Lo que este dataset NO hace, declarado antes de que se lea como cierre (heredado verbatim de `MAESTRA38-N15 §3`):** no mueve `R7.3` ni `R7.6` (0 de sus variables — `list::mexico` no trae `W2_P39B`, `W2_P40`, `W2_P36C` ni `W2_P8`); no trae ponderador (sin ponderar, declarado); es un subconjunto (1 004 de ~1 555 de la ola 2 completa) — universo restringido, declarado en §1.1.

---

## 1 · Universo

- **Fuente:** `data/mexico.tab`, paquete `list` (`github.com/SensitiveQuestions/list @ e088e5f`, 16/ene/2024), `sha256 fe101499b591d90d9e2122f439e26306fcdeab443e42d14f9455e9efa1c04488`.
- **`n` pre-registrado:** **1 004** filas, 25 variables — cifra de la Procedencia (`MAESTRA38-N15 §0`), a confirmar contra el archivo real al abrirlo (mismo criterio que `S2-L2 §1.3`: si el archivo real reporta un `n` distinto, se usa el `n` real, declarado, no se hereda el `1 004` como supuesto).
- **Ponderador:** **NINGUNO** — declarado sin ponderar, explícitamente, mismo criterio de `S2-L2 §1.0`: no se hereda un peso ni se inventa uno; toda estimación de este acto se reporta sin ponderar.
- **Relación con el universo de `S2-L2`:** subconjunto de la ola 2 de MPS-2012 (`n≈1 555` en `S2-L2 §1.3`); no es el mismo universo — 1 004 de ~1 555, universo restringido declarado, nunca tratado como equivalente al panel completo.

---

## 2 · Estimandos

Todos declarados **en proporciones** (escala 0–1 o 0–100 pp, fijar una sola al reportar — nunca mezclar dentro del mismo documento de resultados), con IC95 en cada uno:

1. **Prevalencia por lista (diferencia de medias tratamiento−control).** El estimador estándar del experimento de lista: media del conteo declarado en el grupo tratamiento (lista con el ítem sensible) menos media del conteo en el grupo control (lista sin el ítem), con IC95 por bootstrap o por la fórmula analítica estándar del diseño (Blair & Imai 2012, misma familia de estimador que fundamenta `list::ictreg` — la caja declara cuál usó). Ésta es la prevalencia indirecta del ítem sensible (compra/venta del voto, u otro ítem que el wording de `man/mexico.Rd` confirme — ver §4).
2. **Prevalencia directa (`mex.direct`).** Proporción de "sí" a la pregunta directa equivalente, sin lista — nombre de columna esperado `mex.direct` (a confirmar contra `man/mexico.Rd` al abrir), con IC95 binomial estándar.
3. **Contraste lista−directa.** Diferencia entre (1) y (2), con IC95 de la diferencia — éste es el estimando central de la fila B-bis (§3): si la lista no supera a la directa, el contraste es ≈0 o negativo.
4. **Heterogeneidad.** (1) y (3) recalculados por subgrupo, estratificando por:
   - `mex.wealth` (riqueza, nombre esperado, a confirmar),
   - `mex.urban` (urbano/rural, nombre esperado, a confirmar),
   - `mex.loyal` (lealtad partidista, nombre esperado, a confirmar).
   Cada estrato reporta su propio IC95; no se pondera por tamaño de estrato (universo sin ponderar, §1).
5. **Participación verificada × directa.** Cruce entre el indicador de participación electoral **verificada** (contra padrón, si el dataset lo trae — nombre a confirmar) y la respuesta a la pregunta directa (2): tabla 2×2 con IC95 de la diferencia de proporciones entre verificados-que-votaron y no-verificados, en la tasa de "sí" directa. Si el dataset **no** trae un indicador de verificación distinto de la autodeclaración, este estimando se declara `SIN-INSTRUMENTO` explícitamente — no se sustituye por la autodeclaración sin decirlo.

**Nombres de columna:** todos los marcados "nombre esperado, a confirmar" son los que la Procedencia de `MAESTRA38-N15 §0` cita de memoria de `man/mexico.Rd`; este acto no toca red (`COMPUERTA: ninguna`) y no los reverifica byte a byte — la caja que abra `data/mexico.tab` los compara contra el archivo real antes de calcular nada, mismo patrón P0 que `S2-L2 §1.0` fija para el ponderador.

---

## 3 · Fila B-bis — qué significa que la lista no supere a la directa

Heredado del árbol de falsador de `B-bis` (`forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada-bis-v3.md`), aplicado aquí al contraste de §2.3:

- **Si la prevalencia por lista (§2.1) es estadísticamente indistinguible de, o menor que, la prevalencia directa (§2.2)** (IC95 del contraste de §2.3 incluye 0, o está por debajo de 0): esto **no** corrobora que "no hay deseabilidad social en la pregunta directa" — es evidencia de que el diseño de lista, en este dataset, no está detectando subreporte adicional. Lecturas posibles, ninguna forzada por este pre-registro: (a) el ítem sensible ya se reporta sin fricción en la pregunta directa (baja deseabilidad social real); (b) el diseño de lista tiene poca potencia con `n=1 004` sin ponderar (semiancho del IC95 grande, ver `NO-DISCRIMINA` de `S2-L2 §1.4`); (c) el efecto de "carryover" o de composición de lista (lista B ≠ lista A + un ítem, o el ítem añadido no es el sensible) invalida el diseño — verificar contra §4 de `S2-L2` (condición de entrada de la rama TEXTO) antes de interpretar (a) o (b).
- **Consecuencia declarada, no ejecutada aquí:** un contraste ≤0 **no** mueve ningún tier del canon (`R7.3`/`R7.6` no tienen variables en este dataset, §0) — su único efecto es sobre la interpretación de P3 (experimento de lista) como pieza aislada, y sobre si vale la pena repetir el diseño con el `.dta` completo de ICPSR 35024 cuando llegue (`FP-316`).

---

## 4 · Reutilización verbatim de `S2-L2 §1.2`

Heredado verbatim de `forense/prereg-caja/S2-L2-spec-v1_0.md §1.2`, aplicado aquí donde el diseño es el mismo tipo de instrumento (experimento de lista) aunque la fuente de dato sea distinta:

> Ítems, verbatim de `tools/medidor_l12_mps2012.py:444-445` y `forense/notas/2026-09-03-MAESTRA36-L12-spec-congelada.md:128-129`:
>
> - **Ronda 1 (marzo):** `P35A` (lista A), `P35B` (lista B).
> - **Ronda 2 (julio):** `W2_P35A` (lista A), `W2_P35B` (lista B).
> - Excluir código `9` (NC) de ambas rondas antes de calcular.
> - Contraste: pregunta directa `W2_P41` (oferta recibida, autorreporte).
>
> **Condición de entrada, heredada verbatim de `l12-mps2012-v1_0.json:775` y `resultados.md:176-179`, no relajada aquí:** *"que lista B = lista A + UN ítem, y que ese ítem sea la venta del voto... si el cuarto ítem no es el sensible, la pieza entera se cae."*

**Aplicación a `list::mexico`:** el ítem de tratamiento (`man/mexico.Rd`, citado en la Procedencia de `MAESTRA38-N15 §3`) es *"Exchange your vote for a gift, favor, or access to a service"* — en inglés, ítem `c` sólo en el grupo tratamiento. Este wording satisface por texto la misma condición de entrada (lista tratamiento = lista control + un ítem, y ese ítem es venta/compra del voto) que `S2-L2 §1.2` exige para el `.dta` de ICPSR 35024 — la caja, al abrir `data/mexico.tab`, confirma que el conteo de ítems de control es exactamente uno menos que el de tratamiento antes de calcular ningún estimando de §2. Si no lo es, la pieza completa de este pre-registro se declara `PROPUESTA-REFUTADA-POR-DISEÑO`, mismo criterio que `S2-L2 §2.2` fija para T5.

---

## 5 · Escala declarada

Todas las cifras de §2 se reportan **en proporciones** (0–1), con una nota de conversión a puntos porcentuales (×100) sólo en prosa de resultados, nunca en la tabla numérica — mismo criterio que evita mezclar escalas dentro de un mismo documento (defecto ya atrapado en actos previos de la serie `MAESTRA36`/`MAESTRA37`).

---

## 6 · `se_mueve_si`

Ningún tier del canon (`R7.3`, `R7.6`) se mueve por este dataset — declarado en §0 y §3. Lo único que este pre-registro autoriza mover es el **estado de P3** (experimento de lista, hoy `PROPUESTA` en `S2-L2 §1.2`/`§2.2`):

- **`P3 → MEDIDO (primera mano, subconjunto)`** si la caja ejecuta §2 completo sobre `data/mexico.tab` con veredicto reportado (cualquiera de los estimandos, incluido un contraste de fila B-bis ≤0) — el estado se anota como "primera mano, subconjunto restringido `n=1 004` sin ponderar", nunca como "primera mano, panel completo" (eso requiere el `.dta` de ICPSR 35024, `FP-316`).
- **`P3` permanece `PROPUESTA`** si §4 refuta la condición de entrada (lista tratamiento ≠ control + un ítem sensible) — se declara `PROPUESTA-REFUTADA-POR-DISEÑO` para esta fuente específicamente, sin prejuzgar el `.dta` completo cuando llegue.
- Cuando el `.dta` de ICPSR 35024 (`FP-316`) llegue y la rama MEDICIÓN de `S2-L2 §1.2` corra sobre el panel completo, su veredicto **reemplaza**, no promedia con, el de este documento — éste es el instrumento paralelo más chico, ya abierto; aquél es la medición de primera mano sobre el universo restringido que el canon cita.

---

## 7 · Qué NO hace este acto

No abre `data/mexico.tab` — no está en esta sesión NUBE (sin corpus). No calcula ningún IC95, ninguna diferencia de medias, ninguna celda. No mueve `R7.3`/`R7.6`. No sustituye ni adelanta la rama MEDICIÓN/TEXTO de `S2-L2` sobre ICPSR 35024. No toca `milpa/tramite.yaml` (el motor).

---

**el primer resultado que produzca la caja al ejecutar este procedimiento es el que se reporta.**
