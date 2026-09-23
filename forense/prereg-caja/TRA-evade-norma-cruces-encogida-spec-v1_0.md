# PILOTO 4 · interacción encogida · `evasion_norma` ENVIPE 2025 · cuatro cruces reservados · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1`, 22/sep/2026, CAJA, rama
`acto/gen2-celda-d-piloto-4-encogida-1`. Congelada **sin abrir microdato**: ninguna cifra de
ENVIPE 2025, 2024 ni 2023 se leyó para escribirla.

Firmas de mesa que la habilitan, verbatim en `forense/firmas-pendientes.tsv`:
**`FP-260922-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-a5a0-01`** (§2, autoriza el piloto con la lista de
cruces que `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2` confirme) y
**`FP-260922-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-a5a0-02`** (§6, la regla de λ: la MISMA REGLA del
piloto 3, no el mismo valor, re-derivada de los deltas históricos propios de `evasion_norma`).
`ADENDA-1` (C-ASTRA, archivo propio) sigue vigente y se cita en el cierre, no en el cuerpo.

---

## 0 · Herencia (verbatim de `ENVIPE-EVASION-NORMA-spec-v1_0.md §1`)

Esta spec **no** redefine el desenlace ni el universo: los hereda verbatim de la spec sellada
que registra la tasa nacional (`ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026,
`forense/prereg-caja/ENVIPE-EVASION-NORMA-spec-v1_0.md`, sidecar
`sha256 69605ea4c355b480acef91fe2419ac6b6223468e71e528e2769097b12817cefa`) — el mismo movimiento
que hizo `GEN2-CELDA-D-PILOTO-2` (`TRA-evade-norma-sxd12-spec-v1_0.md §2.2`), no la reformulación
de ese piloto:

- **Unidad de análisis: DELITO** (no persona). Universo: `BP1_20 ∈ {1,2}` en `tmod_vic` de cada
  ola de ENVIPE. `BP1_20`/`BP1_23`: texto de pregunta verificado idéntico en 2023/2024/2025
  (`fd_envipe202{3,4,5}.pdf` y `cuest_modulo_envipe202{3,4,5}.pdf`; constancia primaria en
  `TRA-evade-norma-sxd12-spec-v1_0.md §0.1-§0.2`, re-verificada de forma independiente en este
  acto por extracción directa de los nueve PDFs — mismo texto verbatim, único movimiento de
  *posición* del número de variable dentro del bloque BP, no de significado ni de número de
  pregunta 1.20/1.23).
- **Desenlace:** `evade_norma = 1 ⟺ BP1_20 == "2" ∧ BP1_23 ∈ {"04","05","06","08"}` (conjunta,
  no condicional — `BP1_23` solo se pregunta a quien no denunció; la reserva de que el estimando
  es la conjunta `P(no denunció ∧ razón de norma inútil o extractiva | enfrentó la norma)`, no la
  condicional, se hereda sin reabrir, `milpa/tramite.yaml:513-519`). Ninguna tercera categoría: el
  complemento es `1 − p`. `"b"`/blanco → vacío, nunca cuenta.
- **Ponderador:** `FAC_DEL`. **Diseño:** `EST_DIS × UPM_DIS`, bootstrap de conglomerado con
  reposición dentro de estrato, singleton de certeza.

**Nota de alcance, no reabre nada congelado (hallazgo propio de este acto, A.15 —
"nadie corrió el mecanismo contra esta fuente" ≠ "el mecanismo perdió"):** el salto previo a la
pregunta 1.20 del cuestionario de módulo pierde el código `(03) VANDALISMO` entre 2023/2024 y
2025 (`cuest_modulo_envipe2025.pdf` vs. `cuest_modulo_envipe202{3,4}.pdf`) — no cambia el texto de
BP1_20/BP1_23 ni sus códigos, y el universo de este piloto se toma directo del microdato
(`BP1_20 ∈ {1,2}` realmente observado), no del árbol de ruteo impreso, así que no afecta el
estimando. Se declara por si un acto posterior necesita explicar una diferencia de `n` entre olas
que no sea muestral.

## 1 · Los cuatro cruces, y por qué son éstos

**Confirmados `RESERVADA` hoy** (`data/corrida0/marcador-segmento.tsv`, verificado contra
`origin/main` tras la fusión de `GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2`, PR #1025 — su propia nota de
cierre los lista nombrando este piloto, línea 141-142 de
`forense/notas/2026-09-22-GEN2-MARCADOR-CONSUMO-Y-ADOPCION-2-nota.md`):

| cruce | celdas | ejes |
|---|---:|---|
| `dominio_urbano_rural × sexo` | 6 | 3 dominios × 2 sexos |
| `edad × escolaridad_proxy` | 16 | 4 bandas edad × 4 tramos escolaridad |
| `edad × sexo` | 8 | 4 bandas edad × 2 sexos |
| `escolaridad_proxy × sexo` | 8 | 4 tramos escolaridad × 2 sexos |
| **total** | **38** | |

`edad × dominio_urbano_rural` (12 celdas) sigue `CONSUMIDA-SIN-PILOTO` (`NC-0328`) y
`escolaridad_proxy × dominio_urbano_rural` (12 celdas) la adoptó ya el piloto 2
(`estado=ADOPTADO-POR-FIRMA`) — **no entran**, tal como el encargo lo anticipaba y el marcador lo
confirma.

**Los cuatro ejes ya están construidos y sellados como código**, en
`tools/celda_d/marginales_reproduccion.py` (extensión `ACTO GEN2-GUARDIAN-ENVIPE-EJES-IC-1`,
20/sep/2026): `escolaridad_proxy` y `dominio_urbano_rural` desde el piloto 2; `sexo` y `edad`
añadidos después, mismos objetos del árbitro (`ejes_maestra35_l1.py :: SEXO, tramos_edad`),
importados, no copiados. `PARES_VETADOS[2025]` ya bloquea `edad × dominio_urbano_rural` por
nombre (`ReservaRota`, sin bandera que lo salte) — este piloto no toca ese código, solo llama
`mr.cruce(ola, eje_a, eje_b)` para los cuatro pares de arriba.

**Marginales de 2025 ya sellados, por los cuatro ejes** (`CALC-ARBITRO-MARGINALES-ENVIPE2025-0001`,
13 RESULT: 2 sexo + 4 edad + 4 escolaridad_proxy + 3 dominio — confirmado en
`data/corrida0/marcador-segmento.tsv` líneas 142-154, `decision_ref` apunta a ese CALC). `C2` de
este piloto se construye directo de esos 13 RESULT, igual que el piloto 2 construyó su `C2` de un
dictamen sellado — **no re-deriva ningún marginal de 2025**.

## 2 · Candidatos, fórmulas exactas (por cruce; `a`, `b` = los dos ejes del cruce)

| id | rol | fórmula |
|---|---|---|
| **C1** | referencia | `p₂₄(a,b)` directo — cruce completo de ENVIPE 2024 (no reservada) |
| **C2** | **PISO A VENCER** | `expit(logit p₂₅(a) + logit p₂₅(b) − logit p₂₅)`, marginales de `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001` **sellados**, réplica por réplica compartida con `C-ENCOGIDA`/`C7` |
| **C7** | retador, sin encoger | `expit(logit C2 + δ̄(a,b))`, `δ̄ = (I₂₃(a,b) + I₂₄(a,b))/2` — interacción promediada completa (λ implícita = 1) |
| **C-ENCOGIDA** | retador, encogido | `expit(logit C2 + λ_cruce·δ̄(a,b))`, `δ̄` igual que `C7` |
| L | — | **no entra** (Firma de §2, verbatim: "sin L") |

`I_w(a,b) := logit p_w(a,b) − [logit p_w(a) + logit p_w(b) − logit p_w]` (interacción en escala
logit, misma definición que pilotos 2 y 3). Si algún término es exactamente 0 o 1, esa cantidad
queda `SIN-DEFINIR` — sin recorte, sin sustitución (mismo tratamiento que `TRA-evade-norma-sxd12`).

**No hay C6** (interacción de una sola ola sin encoger): el encargo lista `C2, C1, C-ENCOGIDA, C7`,
cuatro candidatos, no cinco.

### 2.1 · λ — una por cruce, NO pooled (firma de mesa §6, corrección de la recomendación del
propio encargo)

Mismo procedimiento que `GOB-gobierno-digital-exe15-spec-v1_1.md §3.1` (piloto 3), **misma
regla, no el mismo valor** — cada uno de los cuatro cruces re-deriva su propia `λ` de sus propios
deltas históricos, porque mezclar cruces con distinta heterogeneidad real (`edad×escolaridad_proxy`
con 16 celdas no es evidencia intercambiable con `dominio_urbano_rural×sexo` con 6) sesgaría el
encogimiento:

```
λ_cruce = τ̂²/(τ̂² + σ̄²)
τ̂²      = max(0, Var_entre(δ̄) − σ̄²)
Var(δ̄ᵢ) = (EE₂₃,ᵢ² + EE₂₄,ᵢ²) / 4                    por celda i del cruce
σ̄²      = media de Var(δ̄ᵢ) sobre las celdas PUNTUADA del cruce (excluida
          cualquier FUERA-DE-SOPORTE-EX-ANTE de ese cruce)
Var_entre = varianza muestral (ddof=1) de {δ̄ᵢ} sobre esas mismas celdas
k        = número de celdas PUNTUADA del cruce que entran al cómputo
```

`δ₂₃`, `δ₂₄`, `EE₂₃`, `EE₂₄` **no vienen de un CALC histórico separado** (a diferencia del piloto
3, que sí tenía `CALC-ENCIG202{1,3}-CRUCES-HISTORICOS-*` previos): para estos cuatro cruces **nadie
los ha medido antes** en ninguna ola — se calculan aquí mismo, dentro del `COMMIT-2` de este
piloto, desde ENVIPE 2023 y 2024 completas (no reservadas). `λ` no se teclea: el medidor la deriva
por comando (§4.3) y el resultado se sella junto con las emisiones. `τ̂² > 0` se reporta si el
`max(0,·)` no ata; si ata (`Var_entre ≤ σ̄²`), `λ_cruce = 0` y `C-ENCOGIDA = C2` para ese cruce —
resultado legítimo, no un error.

**El valor `0.8937949410086089` del piloto 3 es de otra familia (gobierno digital, ENCIG) y no se
hereda** — verificado contra `GOB-gobierno-digital-exe15-spec-v1_1.md §3.1`: `τ̂²=0.02525670198316379`,
`σ̄²=0.003001124084482884`, `k=15`, coincide exacto con la cita de mesa. Ninguna `λ` de este piloto
se inicializa con ese número.

## 3 · Soporte y adjudicación

- Celda **`PUNTUADA`** si `n ≥ 200` en **2023, 2024 y 2025** (mismo umbral de la casa, pilotos 2 y
  3). El tercer requisito (`n₂₀₂₅`) solo se puede verificar en `COMMIT-3`, con la guardia de una
  sola variable de agrupación — el `COMMIT-2` emite `SOPORTE-HISTORICO` con 2023/2024.
- **`FUERA-DE-SOPORTE` global por cruce** si fallan `≥ round(k_total_cruce / 3)` celdas de ese
  cruce: `dominio_urbano_rural×sexo` (6) → 2 · `edad×sexo` (8) → 3 · `escolaridad_proxy×sexo` (8)
  → 3 · `edad×escolaridad_proxy` (16) → 5. Fórmula, no cifra tecleada por cruce; coincide con el
  5/15 (≈1/3) del piloto 3 cuando se aplica a k=15.
- Por celda, `INDECIDIBLE` con las dos condiciones del programa, verbatim
  (`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38`): *"INDECIDIBLE si ambos caen dentro del
  IC de R o si |d_L−d_M| < 0.5·EE(R)"*, `EE(R) = (IC95sup − IC95inf)/3.92`.
- Un retador (`C7`, `C-ENCOGIDA`) **gana** contra un piso (`C1`, `C2`) sólo si vence en
  `≥ ¾` de las `PUNTUADA` de su propio cruce (mismo umbral de la casa).
- **Comparación primaria** (v2.16 §4, manda sobre el conteo de celdas): `ΔMAE = MAE(piso) −
  MAE(retador)` sobre las `PUNTUADA` de cada cruce, en pp, con IC **réplica por réplica**
  (estrato, UPM, ponderador y agrupación por delito respetados). Vence el retador si el IC de
  `ΔMAE` despeja 0 **y** el umbral (`0.5 pp`, mismo umbral de la casa); propuesta con reserva si
  despeja 0 pero no el umbral; nadie vence si el IC incluye 0. El conteo `≥¾` de celdas es
  secundario y descriptivo, no adjudica por sí solo.

### 3.1 · B-bis, declarado antes de ver el dato

Por cruce, y agregado a nivel piloto (cuatro cruces, dos challengers cada uno — familia de 8
comparaciones, sin valor-p):

- Nadie vence (ni `C7` ni `C-ENCOGIDA`) a `C2` **y** el límite superior de `ΔMAE ≤ 0.5 pp` para
  ambos → **corroborada**: "marginales sin interacción" es el estimador honesto de celda para
  `evasion_norma` también fuera de escolaridad×dominio — resultado de programa, no dice que la
  interacción no exista en la población.
- Nadie vence pero algún IC de `ΔMAE` admite `> 0.5 pp` → **falsador débil**, aunque sea la
  cuarta vez (pilotos 1 y 2 con `SIN-CANDIDATO-SUPERIOR`, piloto 3 con `FALSADOR DÉBIL`).
  **Si ambas lecturas caben, manda falsador débil** (mismo orden de precedencia de piloto 3).
- Un retador vence en un cruce → limita a `C2` **sólo** en ese desenlace, cruce y ola; `C2` sigue
  adoptado en los demás cruces y en `DIN`/`TRA` en general (A.10).
- `C-ENCOGIDA` vence y `C7` no, en el mismo cruce → el hallazgo es sobre **cuánto encoger**
  (replica el patrón `Sλ`/`S½` del piloto 3 con `C-ENCOGIDA`/`C7` en su lugar).
- Si un cruce sale `FUERA-DE-SOPORTE` global, ese cruce no cuenta en la lectura B-bis agregada —
  se declara aparte, no se trata como derrota.
- **Adopción: ninguna.** `champion_actual: NINGUNO`, `requiere_decision_mesa: false` — este piloto
  no adopta (mismo patrón que pilotos 2 y 3; adoptar es de mesa, y §7(c) del encargo lo prohíbe).

## 4 · Cuerpo de medición

Dos CALC, dos commits — mismo mecanismo E.6 de reserva que pilotos 2 y 3 (agrupación de una sola
variable en emisiones; el cruce por dos variables vive únicamente en el CALC del árbitro):

| | `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001` (`COMMIT-2`) | `CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001` (`COMMIT-3`) |
|---|---|---|
| ola | 2023 y 2024 enteras (parámetro); 2025 sólo marginales, ya sellados (no re-derivados) | única función autorizada a cruzar 2025 por los cuatro pares |
| carga | `mr.carga_ola(zip, año, reservada=False)` para 2023/2024; marginales 2025 leídos del `resultados.json` sellado de `CALC-ARBITRO-MARGINALES-ENVIPE2025-0001` (input de repo, sha256) | carga 2025 con `reservada=False` (el `COMMIT-2` ya no la reserva: solo tocó marginales, nunca el cruce) |
| agrupación | `mr.marginal`/`mr.cruce` con **una sola variable** por eje en 2023/2024 completas; el cruce de 2023/2024 sí se deriva aquí (no reservadas) | `mr.cruce(ola2025, eje_a, eje_b)` para los cuatro pares — único código autorizado |
| bootstrap | `mr.replicas_compartidas`, UPM con reposición dentro de estrato, `PCG64`, réplicas compartidas por ola (mismo diseño que pilotos 2/3) | mismas multiplicidades → `C2` recalculado reproduce el sellado, `R` comparte réplicas con `C2` |
| emite | `C1`, `C2`, `C7`, `C-ENCOGIDA` con IC por celda y por los cuatro cruces; `I₂₃`, `I₂₄`, `λ_cruce` (con `τ̂²`, `σ̄²`, `Var_entre`, `k`) por cruce; soporte histórico | `R(a,b)` por los 38 pares, soporte definitivo, veredicto por celda y por cruce, `ΔMAE` con IC, `B-BIS` por cruce y agregado |
| se niega si | firma §2/§6 no `FIRMADA` en `firmas-pendientes.tsv`; insumo con nombre que contiene "2025" y `ola≠2025`; marginales sellados con sha256 discordante | falta `emisiones_resultados`/`emisiones_sello`, sha256 no coincide, o `C2` recalculado no reproduce el sellado a `1e-9` |

`resultados:` de cada `spec.yaml` se deriva por comando (`esquema_resultados()`), no se teclea; la
prueba sintética exige que el conjunto emitido sea exactamente ese (mismo contrato que pilotos 2 y
3).

### 4.1 · ADENDA-1 · C-ASTRA

Si al abrir `COMMIT-1` (este acto) existe en `origin/main` un `CALC-ASTRA-<DOMINIO>-<CRUCE>-0001`
sellado que cumpla (a)-(c) de `forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-ADENDA-1.md`,
se copia por id como candidato adicional `C-ASTRA` de ese cruce, se somete al mismo criterio y se
rotula PROSPECTIVA solo si (b) se verifica. **Verificado en este acto: no existe ningún
`CALC-ASTRA-*` en el árbol hoy** (`git ls-tree -r origin/main | grep -i CALC-ASTRA` → vacío). El
`COMMIT-2` que efectivamente selle emisiones vuelve a verificarlo al abrir, por si Astra entregó
entretanto.

## 5 · Validación de «congelado» — D-22 (`tests/test_piloto4_v1_0.py`)

Cuatro pruebas obligatorias, análogas al patrón del piloto 3 (`tests/test_piloto3_v11.py`),
adaptadas donde la familia no tiene precedente:

- **(a) sintética:** `medir()` de punta a punta sobre un fixture sintético (ENVIPE 2023/2024/2025
  con `tmod_vic`+`tsdem`, ~7000 delitos, los cuatro ejes representados, una celda deliberadamente
  bajo `n=200`) produce las emisiones de los cuatro candidatos por celda, con IC, en los cuatro
  cruces; `adjudicacion.medir()` corre sobre un `R` sintético sellado y produce veredicto. El
  esquema declarado (`esquema_resultados()`) coincide exactamente con lo emitido.
- **(b) de control** (no hay "oro" propio: ningún CALC previo midió estos cuatro cruces en
  ninguna ola — se declara `NO-APLICA` como precedente directo). En su lugar, control indirecto
  sobre la **misma maquinaria compartida**: se reproduce `escolaridad_proxy × dominio_urbano_rural`
  (el cruce del piloto 2, no reservado, ya sellado en 2023/2024/2025 por
  `CALC-TRA-EVADE-NORMA-SXD-*`) llamando `mr.carga_ola`/`mr.cruce` desde este medidor, y se compara
  contra los RESULT sellados de ese piloto a `<1e-10`/`<1e-9` — prueba que el guardián, el
  bootstrap y el IC que este piloto reutiliza siguen produciendo lo mismo que ya se selló, aunque
  el cruce en sí no sea uno de los cuatro de este piloto.
- **(c) reserva:** ningún `ejecucion.json`/`resultados.json`/`sello*` en los dos CALC nuevos;
  ningún archivo versionado trae un `RESULT-TRA-CRUCES-ENCOGIDA-2025-*` de este piloto; el
  código fuente del medidor no menciona ningún zip de `envipe2025` fuera del insumo declarado.
- **(d) λ:** por cada uno de los cuatro cruces, el test re-implementa el método de momentos
  (independiente de cualquier función `lambda()` del medidor) sobre los `I₂₃`/`I₂₄`/`EE` que el
  propio `medir()` sintético produjo, y exige coincidencia con la `λ_cruce` emitida a `1e-12` —
  mismo patrón mecánico que `test_piloto3_v11.py::test_d`, adaptado porque aquí no hay un JSON
  sellado externo del que leer: el dato de entrada es el que el propio COMMIT-2 calcula (2023/2024,
  no reservadas), no un histórico separado.

## 6 · Lo que esta spec NO autoriza

- No adjudica ni corona campeón: adoptar es de mesa (§7(c) del encargo).
- No toca `edad × dominio_urbano_rural` (vetado por nombre, `NC-0328`) ni
  `escolaridad_proxy × dominio_urbano_rural` (ya adoptado por el piloto 2).
- No re-estima λ del piloto 3 ni la usa como valor inicial.
- No abre ENVIPE 2025 por ningún camino que no sea `mr.cruce()` en `COMMIT-3` (PARO (a) del
  encargo, scratch incluido).
- No edita `tools/celda_d/marginales_reproduccion.py` ni sus vetos.

## 7 · Auditoría (afirma sobre México)

El universo son delitos con contacto potencial de denuncia (`BP1_20` observado), lo que excluye
victimización no reportada del todo al INEGI en el módulo — más informal, más rural, menor
confianza previa en el sistema de justicia. `evade_norma` mide una razón *declarada* de no
denunciar (pérdida de tiempo, trámites largos, desconfianza, actitud hostil), no una medición
directa de disfuncionalidad institucional: es percepción de la víctima sobre el sistema, mediada
por su propia experiencia y la de su entorno. Cruzarla por sexo, edad, escolaridad_proxy y dominio
urbano/rural describe **variación de la percepción por posición social**, no jerarquiza a las
instituciones. Peligroso leído simplista: "el grupo X evade más la norma" como rasgo de ese grupo,
cuando puede ser exposición diferencial al tipo de delito, al tipo de autoridad con la que
interactúa, o a la oferta real de justicia en su región. Que `C2` (sin interacción) no sea vencido
en las tres familias anteriores (piloto 1, piloto 2, y probablemente ésta) es evidencia de que los
marginales por sí solos ya capturan casi todo lo estimable con este diseño — no evidencia de que
las subpoblaciones se comporten igual.

El primer resultado que produzca este procedimiento es el que se reporta.
