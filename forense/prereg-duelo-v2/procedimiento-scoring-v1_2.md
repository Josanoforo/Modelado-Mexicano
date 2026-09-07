# Procedimiento de scoring v1.2 — SELLADO — `ACTO MAESTRA38-M13 · M-POR-CELDA PASOS 1 Y 2`

**Estado: SELLADO, 7/sep/2026.** `procedimiento-scoring-v1_1.md` (SELLADO,
`ADR-262`) **verbatim, íntegro, sin ningún cambio de contenido** — cabecera
propia incluida (§0-§6 abajo, más su propia cabecera "Cabecera obligatoria
(P2)", son copia byte a byte del archivo sellado) — más una sección nueva,
§7, que fija la métrica secundaria pre-registrada que la fila `D4` del
benchmark (`forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md` §4-5,
`agregado-v1_2-resultado.json` como evidencia) dejó abierta: *"si una
`v1.2` del procedimiento de scoring debería sumar una métrica secundaria
... que sí discrimine entre corredores cuando `z`/banda no lo hace"*.
`procedimiento-scoring-v1_1.md` **no se edita** — sigue íntegro en su
ruta original (A.10, corolario 1).

**Firma de mesa que activa esta sección (verbatim, decisión de dirección
incluida en el encargo `MAESTRA38-M13`, la firma es el merge, 7/sep/2026,
`ACTO MAESTRA38-TRAMITE`):** *"D4 = puntos porcentuales (error absoluto en
pp, MAE por corredor), `z` sigue siendo la métrica primaria y sellada"* —
resuelve la disyuntiva que §4 del benchmark dejaba abierta (pp o Brier):
puntos porcentuales, porque las 14 celdas del universo vigente son todas
proporciones `[0,1]` (ninguna requiere la forma de Brier sobre una
predicción probabilística de un evento distinto de su propia tasa base).

**SHA de redacción (heredado de `procedimiento-scoring-v1_1.md`, sin
cambio en el cuerpo heredado):** `7e0fb716` (`main` tras fusionar
`PR #583`, `ACTO MAESTRA36-N2 · CIERRA-N3-AGREGA-2`, la corrida v1.2 sobre
14 celdas que produjo la evidencia de §4-5 del benchmark que motiva esta
sección nueva).

---
## 0 · La idea de reconciliación, en una frase

`procedimiento-scoring-v1_0.md` §3 (líneas 73-84) prueba que **no existe
forma honesta de convertir "`0.5·EE(R)` de cada celda" en el `float` único
que `Configuracion.delta` exige** (`scoring-adv1-m3.py:87`) mientras las
mediciones sigan en las unidades brutas de cada celda (proporciones de
escalas distintas: `civico.denuncia...`, `dinero.ahorro...`,
`tramite.mordida...`). La banda ya sellada no cambia — **la unidad de la
medición sí**: si cada celda se expresa como `z = dif/EE(R)` (P1.i, §1
abajo), la banda `[-0.5·EE(R), +0.5·EE(R)]` de esa celda se vuelve,
literalmente, `[-0.5, +0.5]` — la misma banda, en unidades donde ya no
depende de la celda. `delta = 0.5` dejó de ser un escalar inventado: es
`0.5·EE(R)/EE(R)`, la misma regla de `FP-163` reexpresada, no una regla
nueva. Nada más de este documento depende de una decisión que no sea esa
reexpresión — el resto (§§2-5) es la consecuencia mecánica de aplicar esa
unidad a lo que el motor ya sabe agregar (bootstrap) y a lo que el
pre-registro ya declaró ausente (baseline `B`, F-DD).

---

## 1 · (i) Unidades — `z = dif/EE(R)` y el escalar `delta = 0.5`

**Regla.** Para toda celda con `R`/`EE(R)` computado
(`corridas-R/<id>.json`, `estado="COMPUTADO"`) y un punto de corredor
disponible (`L-solo` o `M`), la medición de esa celda para efectos de este
procedimiento es:

```
z_L = (L_solo − R) / EE(R)      z_M = (M − R) / EE(R)
```

en vez de `dif = punto − R` en unidades brutas. La banda de indiferencia es
`[-0.5, +0.5]` en `z` — **el mismo intervalo** `[-0.5·EE(R), +0.5·EE(R)]`
de `Δ_material` (`procedimiento-scoring-v1_0.md:20-24`, verbatim de mesa:
*"banda TOST y margen material del piloto = regla derivada `Δ_material =
0.5·EE(R)`"*), dividido entre el mismo `EE(R)` que ya lo definía.
`Configuracion.delta` (`scoring-adv1-m3.py:87`) recibe **un** `float`:
`0.5`.

**Deriva de:**
`procedimiento-scoring-v1_0.md:20-25` (banda sellada, `FP-163`/`ADR-199`) ·
`procedimiento-scoring-v1_0.md:73-84` (§3, prueba de que no hay forma
honesta de colapsar la banda en unidades brutas — la razón por la que este
punto cambia la unidad en vez de inventar el escalar) ·
`scoring-adv1-m3.py:87` (`delta: float`, el campo que exige exactamente un
número).

**Lo que este punto NO hace:** no cambia el valor de `Δ_material`, no
recalcula `R`/`EE(R)`, no toca `corridas-R/`. `delta` sigue siendo `0.5·EE(R)`
en el sentido literal de `FP-163` — solo la unidad de medición se mueve
para que el escalar sea representable.

---

## 2 · (ii) Agregado marginal por corredor — proporción dentro de banda y mediana de `|z|`

**Regla.** Por corredor (`L_SOLO`, `M`, por separado — nunca mezclados),
sobre el universo marginal de celdas con `z` definido para ese corredor
(mismo criterio de inclusión que `construir_universo_marginal`,
`scoring-adv1-m3.py:653-656`, aplicado a `z` en vez de `skill`), se
reportan dos estadísticos:

1. **Proporción dentro de banda** — fracción de celdas con `-0.5 ≤ z ≤
   0.5`.
2. **Mediana de `|z|`** — mediana de los valores absolutos, sobre el mismo
   universo.

Ambos con intervalo de confianza por bootstrap: `replicas=10000` (default
técnico del script, docstring `scoring-adv1-m3.py:27-28`: *"`replicas` usa
el default técnico visible `10000` cuando la clave se omite"*),
`nivel_ic=0.95`, `seed=42` — los mismos tres números que `FP-168` ya selló
(`scoreboard-v1_1.md:83-84`, *"`nivel_ic=0.95`/`seed=42` ya están sellados
(`FP-168`, FIRMADA 30/ago/2026, `ACTO MAESTRA32-E9 · PROPAGA-2`)"*), **sin
declarar un segundo bootstrap con otros parámetros** — es el mismo sello,
aplicado a un estadístico distinto. El remuestreo reutiliza, importadas y
sin editar, las dos primitivas de `scoring-adv1-m3.py` que no son
específicas de `skill`:

- `generar_indices_bootstrap(n_celdas, replicas, seed)`
  (`scoring-adv1-m3.py:683-690`) — genera los índices; no lee ningún campo
  de celda, solo `n_celdas`.
- `derivar_seed_scope(seed, scope_id)` (`scoring-adv1-m3.py:720-723`) — la
  semilla por-scope vía SHA-256, "nunca usa `hash()` de Python".

Lo que **no** se reutiliza tal cual es `bootstrap_marginal`
(`scoring-adv1-m3.py:769-802`): esa función indexa
`celda.skills[corredor_id]` (línea 789) — hardcodeado a `skill`. Este
procedimiento necesita la misma mecánica de remuestreo sobre `z` (para la
mediana de `|z|`) y sobre el indicador binario `dentro_de_banda(z)` (para
la proporción), no sobre `skill`. Se declara explícitamente: esto **adapta
la forma** de `bootstrap_marginal` a una cantidad distinta, reutilizando su
motor de remuestreo — no reinventa el bootstrap.

**Carácter no-gatante.** Igual que `calcular_paso_0`
(`scoring-adv1-m3.py:997-1019`, *"PASO 0 siempre se calcula y nunca altera
el veredicto"*), este agregado marginal es diagnóstico: describe qué tan
cerca anda cada corredor de `R` por separado, pero **no adjudica** — la
adjudicación es el punto (iii), §3 abajo.

**Deriva de:**
`scoring-adv1-m3.py:683-690` (`generar_indices_bootstrap`, primitiva
reutilizada) · `scoring-adv1-m3.py:720-723` (`derivar_seed_scope`,
primitiva reutilizada) · `scoring-adv1-m3.py:769-802` (`bootstrap_marginal`,
patrón adaptado, no reutilizado tal cual) · `scoring-adv1-m3.py:997-1019`
(`calcular_paso_0`, precedente del carácter no-gatante/diagnóstico) ·
`scoreboard-v1_1.md:83-84` (`FP-168`, `nivel_ic`/`seed` sellados) ·
`scoring-adv1-m3.py:27-28` (docstring, `replicas` default `10000`).

---

## 3 · (iii) Comparación principal — L-vs-M pareada, en unidades `z`

**La comparación principal no cambia**: sigue siendo `L_SOLO_vs_M`
(`comparacion_principal_id`), FIRMADA `F0.1`/`ADR-197`
(`procedimiento-scoring-v1_0.md:10-12`) y confirmada como el único par
obligatorio del contrato `F1` (`procedimiento-scoring-v1_0.md:13-19`:
mínimo `{(L,solo):1,(M,principal):1}`). Este punto solo re-expresa esa
misma comparación en las unidades de §1.

**Regla.** Sobre el universo pareado (celdas con `z_L` **y** `z_M`
definidos simultáneamente — mismo criterio de intersección que
`_construir_universo`, `scoring-adv1-m3.py:616-650`, aplicado a `z` en vez
de `skill`), la cantidad pareada por celda es:

```
dif_pareada_z = z_L − z_M = (L_solo − M) / EE(R)
```

(el término `R` se cancela algebraicamente porque ambos lados restan la
misma `R` de la misma celda — la comparación sigue siendo contra el
árbitro real, solo que `R` no aparece como término separado). Se
bootstrapea la media de `dif_pareada_z` sobre las celdas del universo
pareado, con el mismo `seed=42`/`nivel_ic=0.95`/`replicas=10000` de §2,
reutilizando `generar_indices_bootstrap`/`derivar_seed_scope` (misma cita
que §2) — la forma es la de `bootstrap_pareado`
(`scoring-adv1-m3.py:826-886`), adaptada de `skill` a `z` por la misma
razón que §2 declara para `bootstrap_marginal`.

**Adjudicación — solo PASO 2, nunca PASO 1.** `adjudicar_secuencia`
(`scoring-adv1-m3.py:908-994`) tiene dos pasos: PASO 1 (`scoring
-adv1-m3.py:927-937`) exige que `skill` de `L` o de `M` "supere cero" —
literalmente, que el IC de `1 − error/error_baseline` supere cero, lo cual
solo tiene sentido con `error_baseline` real. PASO 2
(`scoring-adv1-m3.py:952-969`) es la regla `±delta` sobre una diferencia ya
bootstrapeada — **no menciona `skill` ni `baseline` en su cuerpo**, solo
`lo`/`hi`/`delta`. Con `B` declarado NO-APLICA (§4 abajo), PASO 1 no tiene
insumo: este procedimiento **omite PASO 1** y adjudica directamente con la
regla de PASO 2, aplicada a `[ic_lo, ic_hi]` de `dif_pareada_z` contra
`delta=0.5`:

| Condición (`scoring-adv1-m3.py:961-969`) | Código v1.0 (requiere `skill`/`B`) | Código v1.1 (sin `B`, honesto) |
|---|---|---|
| `ic_lo ≥ −0.5` y `ic_hi ≤ 0.5` | `EQUIVALENTES` | `EQUIVALENTES-EN-BANDA` |
| `ic_lo > 0.5` | `GANA_L` | `L-MAS-ALTO-QUE-M` (dirección, no superioridad) |
| `ic_hi < −0.5` | `GANA_M` | `M-MAS-ALTO-QUE-L` (dirección, no superioridad) |
| `ic_lo ≤ 0 ≤ ic_hi` | `INDETERMINADO` | `INDETERMINADO` |
| resto | fallo cerrado `POSICION_NO_DEFINIDA` | fallo cerrado `POSICION_NO_DEFINIDA` |

**Por qué la columna derecha no dice "gana".** `GANA_L`/`GANA_M` en el
motor sellado significa "tiene más `skill`" — es decir, menos error
relativo a un `baseline` real. `dif_pareada_z` es una diferencia de **sesgo
firmado** respecto a `R` (¿quién se desvía más, y hacia dónde?), no una
diferencia de error normalizado por `baseline`. Etiquetarla "gana" tomaría
prestada la semántica de superioridad de `skill` sin tener el `baseline`
que la sostiene — exactamente el defecto que §4 existe para no cometer. La
dirección (`L-MAS-ALTO-QUE-M` / `M-MAS-ALTO-QUE-L`) sí es honesta: dice
hacia dónde apunta la diferencia, no quién es mejor.

**Deriva de:**
`procedimiento-scoring-v1_0.md:10-12` (comparación principal FIRMADA,
`F0.1`/`ADR-197`) · `procedimiento-scoring-v1_0.md:13-19` (contrato `F1`,
par obligatorio) · `scoring-adv1-m3.py:616-650` (`_construir_universo`,
criterio de intersección adaptado) · `scoring-adv1-m3.py:826-886`
(`bootstrap_pareado`, patrón adaptado) · `scoring-adv1-m3.py:908-994`
(`adjudicar_secuencia`) · `scoring-adv1-m3.py:927-937` (PASO 1, por qué se
omite) · `scoring-adv1-m3.py:952-969` (PASO 2, regla reutilizada verbatim).

---

## 4 · (iv) Baseline `B` — NO-APLICA para marco-M

**Declaración.** El corredor `B` (baseline) **no aplica** a ninguna celda
de `marco-M-sorteado-v1_1.tsv` en este procedimiento. Dos razones
independientes, ninguna inventada por este acto:

**(a) Estructural — `procedimiento-scoring-v1_0.md` §4 (líneas 107-127).**
`skill()` (`scoring-adv1-m3.py:394-398`) es `1 − error_corredor/
error_baseline`: sin `error_baseline` no hay `skill` legítima que poblar,
"no solo para `M`" (línea 118). Verificado empíricamente en este acto,
contra el árbol real (no por lectura del procedimiento v1.0 nada más):
`forense/prereg-duelo-v2/corridas-R/_corredor-B.json` — el único archivo
`B` que existe en el repo — trae `metodo="SIN_BASELINE"` para las 15
celdas del marco piloto (`CIV-08`, `DIN-03`, …) y **cero entradas** para
cualquier `id_celda` de marco-M (`grep -c "CIV-M\|TRA-M\|FAM-M"
_corredor-B.json` → `0`, sobre el archivo completo, no una muestra): `B`
no solo carece de valor para marco-M, carece de fila.

**(b) De diseño — asimetría declarada del whitepaper.**
`milpa/milpa-whitepaper-v0_1.md:212-214` (§10, sellado `ADR-237`):
*"Asimetría declarada, no escondida: L y M comparten la familia de LLM de
origen; eso mantiene el LLM constante y aísla el valor marginal de
estructura + datos."* `L` y `M` no son dos predictores independientes que
compiten contra un tercero neutral (`B`) — son dos formas de usar el
**mismo** conocimiento de origen (el LLM), con y sin estructura explícita.
Un `baseline` de "adivinar sin el LLM" mediría algo que el diseño del
duelo nunca se propuso aislar; el whitepaper reserva esa descomposición
para el corredor `E` ("combinación... separaría... cuánto aporta el dato y
cuánto la estructura", líneas 214-217), no para `B`. `B` fue diseñado y
poblado para el marco piloto (15 celdas, `_corredor-B.json`) bajo una
pregunta distinta; extenderlo a marco-M sin que el diseño lo contemple
sería inventar una medición, no leer una ya sellada.

**Consecuencia para este procedimiento:** ninguna sección de §§1-3 usa
`skill`, `error_baseline` ni PASO 1 de `adjudicar_secuencia`. `mediciones`
sigue `{}` en la `entrada.json` de `tools/score_marco_m.py`
(`score_marco_m.py:152-154`, sin editar) — este procedimiento no le pide
que cambie.

**Deriva de:**
`procedimiento-scoring-v1_0.md:107-127` (§4, razón estructural) ·
`scoring-adv1-m3.py:394-398` (`skill()`) ·
`forense/prereg-duelo-v2/corridas-R/_corredor-B.json` (verificación
empírica, 0 de 0 celdas marco-M) · `milpa/milpa-whitepaper-v0_1.md:212-217`
(§10, asimetría declarada, `ADR-237`) · `tools/score_marco_m.py:152-154`
(`mediciones: {}`, ya sellado por `MAESTRA33-E8`, no tocado aquí).

---

## 5 · (v) F-DD — `VERIFICACION-NO-PUNTUA` queda fuera del agregado

**Regla.** Toda celda cuya columna `grado_DD` (marco-M, `ADR-237`) marque
`VERIFICACION-NO-PUNTUA` se excluye de §2 (agregado marginal) y de §3
(comparación pareada) **antes** de calcular `z` para esa celda — no entra
al universo marginal ni al pareado, no cuenta en `n_celdas` de ningún
bootstrap. Es la misma exclusión que `tools/score_marco_m.py` ya aplica
para construir `celdas` de `scoring-adv1-m3.py` (`_es_no_puntua_dd`,
`score_marco_m.py:59-61`; `puntuable = (not no_puntua_dd) and …`,
`score_marco_m.py:110`; `if entrada["verificacion_no_puntua"]: continue`,
`score_marco_m.py:150-151`) — este procedimiento no la redefine, la hereda
para las mismas celdas.

**Estado actual, declarado sin que este punto lo cambie:** `0` de las `11`
celdas de `marco-M-sorteado-v1_1.tsv` están marcadas
`VERIFICACION-NO-PUNTUA` bajo F-DD hoy (`scoreboard-v1_1.md:35-39`,
`scoreboard-v1_1.md` §1) — esta regla no tiene efecto observable en el
universo actual; se declara para que un sorteo futuro con celdas de
`ola_calibracion` incluidas no requiera una segunda decisión de mesa.

**Deriva de:**
`tools/score_marco_m.py:12-15` (descripción de la exclusión F-DD) ·
`tools/score_marco_m.py:59-61` (`_es_no_puntua_dd`) ·
`tools/score_marco_m.py:110` (fórmula de `puntuable`) ·
`tools/score_marco_m.py:150-151` (exclusión al construir `celdas`) ·
`scoreboard-v1_1.md:21-39` (§1, tabla de universo + columna F-DD,
`0` de `11` hoy).

---

## 6 · Qué NO decide este documento

- No sella `delta=0.5` — eso es la firma de mesa (`mesa-pendientes.md` §5,
  P3).
- No corre `ejecutar_scoring` ni ningún bootstrap real — §§1-5 son regla,
  no resultado. Ninguna cifra de las 4 celdas visibles (cabecera) se
  recalculó aquí en unidades `z`.
- No decide qué pasa si `n_celdas` del universo pareado (§3) es `0` o `1`
  — con `4` celdas puntuables hoy (todas del mismo corredor `M`, ninguna
  con `L` real todavía, `scoreboard-v1_1.md:41-43`) el universo pareado de
  §3 está vacío hasta que `L` exista para al menos una de ellas (el PR
  `[L] corridas v1_1` que `PAQUETE-L-v1_1.md` describe). Esa cuenta es
  consecuencia del dato, no una decisión de este documento — igual que
  `SIN_CELDAS_PAREADAS` (`scoring-adv1-m3.py:1044-1048`) es consecuencia,
  no defecto, en `procedimiento-scoring-v1_0.md:129-143`.
- No re-abre `F0`-`F3` (`ADR-197`), no re-abre la banda TOST
  (`FP-163`/`ADR-199`), no re-abre `FP-168`. Las tres siguen firmadas
  exactamente como estaban.

## Frase que gobierna esta propuesta

**Ningún valor de este documento se eligió mirando un resultado.** Los tres
números que aparecen (`delta=0.5`, `nivel_ic=0.95`, `seed=42`) están
sellados desde antes del 1/sep/2026 (`FP-163`/`ADR-199`, 26/ago;
`FP-168`, 30/ago) — antes de que las 4 cifras `M`-vs-`R` que este acto
tuvo visibles (cabecera) existieran. Lo único que este documento decide es
la **unidad** en la que esos tres números ya sellados se aplican, y qué
partes del motor sellado (PASO 2 sí, PASO 1 no; `bootstrap_marginal`/
`bootstrap_pareado` como forma, no como función) siguen siendo honestas sin
`B`.

---

## 7 · Métrica secundaria (D4, pre-registrada) — puntos porcentuales, MAE por corredor

**Pre-registrada antes de correr** (`ACTO MAESTRA38-M13`, cabecera, punto
B-bis): esta sección fija la métrica **antes** de que `agregado_v1_3.py`
produjera ningún número — la expectativa declarada en el encargo
(`z ≈ −8/+14/+6` en `TRA`, mediana `|z|` de `M` ≈ 7.4) se verificó
**después** de escribir esta sección, no al revés. *"El primer resultado
que produzca este procedimiento es el que se reporta"* — cierre del
encargo, propagado aquí verbatim.

**Regla — `err_pp` por celda.** Para toda celda con `R` computado y un
punto de corredor disponible (`M`, `L_solo` o `L+corpus`):

```
err_pp = 100 · (punto_corredor − R)
```

con signo (positivo: el corredor sobre-estima `R`; negativo: sub-estima).
Es la misma resta que ya alimenta `z` (§1), sin dividir entre `EE(R)` y
multiplicada por 100 — puntos porcentuales de una proporción `[0,1]`, la
escala de las 14 celdas del universo vigente (`marco-M-sorteado-v1_3.tsv`,
columna `clase_procedencia`: todas `MEDIDO·p(...)` o `NO ESTIMADO (censo
de existencia)` sobre una tasa base, ninguna Brier de una predicción
probabilística de un evento).

**Regla — `MAE_pp` por corredor.** Por corredor, sobre el universo de
celdas con `err_pp` definido para ese corredor (mismo criterio de
inclusión que §2, aplicado a `err_pp` en vez de `z`):

```
MAE_pp = media( |err_pp| )
```

con intervalo de confianza por bootstrap, **mismos parámetros sellados**
que §§1-5 (`seed=42`, `nivel_ic=0.95`, `replicas=10000`) — ningún segundo
bootstrap con otros parámetros, mismo sello aplicado a un estadístico
distinto (mismo principio que §2 declara para `nivel_ic`/`seed`).

**Regla — comparación pareada de `MAE_pp`.** Sobre el universo pareado
(celdas con `err_pp` de ambos corredores del par — mismo criterio de
intersección que §3), la cantidad pareada por celda es
`|err_pp_corredor| − |err_pp_M|`, bootstrapeada con los mismos parámetros.
Dos pares, los mismos que §3/`comparacion_secundaria_l_corpus_vs_m` de
`agregado_v1_2.py` ya calculan para `z`: `L_SOLO_vs_M` y `L_CORPUS_vs_M`.
**Adjudicación de orden, no de banda** — esta métrica no tiene `delta`
propio (D4 no lo pre-registra): reporta signo del IC de la diferencia
pareada — `M-MENOR-ERROR-PP-QUE-L` (IC íntegramente `> 0`),
`L-MENOR-ERROR-PP-QUE-L` (IC íntegramente `< 0`, mismo nombre invertido
para el corredor `L`), o `INDETERMINADO` (IC cruza 0) — **nunca** "gana":
mismo principio de honestidad de nombres que §3 declara para `z`
(`GANA_L`/`GANA_M` exigiría `skill`/`baseline`, ausentes aquí también).

**Carácter no-gatante, igual que §2.** Esta métrica es diagnóstica: **no
sustituye ni reabre la banda `z` de §1/§3**, que sigue siendo el
veredicto primario y sellado. Se añade para la situación que motivó `D4`
(`BENCHMARK-MOTORES-COMPARABLES.md` §4): cuando `z`/banda no discrimina
entre corredores (proporción en banda `0.000` para dos de tres corredores,
comparación principal pareada `INDETERMINADO`), reportar si una métrica
sin dividir por `EE(R)` sí lo hace.

**Resultado de la primera corrida (`agregado-v1_3-resultado.json`,
`metrica_secundaria_pp_d4`) — reportado, no ajustado:**

| corredor | n celdas | `MAE_pp` (punto) | IC95 |
|---|---|---|---|
| `M` | 14 | **4.51** | [2.71, 6.37] |
| `L_SOLO` | 13 | 11.69 | [4.13, 21.72] |
| `L_CORPUS` | 14 | 19.60 | [9.28, 30.92] |

| comparación pareada (`|err_pp_corredor| − |err_pp_M|`) | n pareado | punto | IC95 | orden |
|---|---|---|---|---|
| `L_SOLO_vs_M` | 13 | +7.23 pp | [+0.68, +16.92] | **`M-MENOR-ERROR-PP-QUE-L`** |
| `L_CORPUS_vs_M` | 14 | +15.10 pp | [+5.92, +25.71] | **`M-MENOR-ERROR-PP-QUE-L`** |

**Esto es lo que `D4` buscaba.** La comparación principal pareada en
unidades `z` (§3, `comparacion_principal_pareada` de
`agregado-v1_3-resultado.json`) sigue `INDETERMINADO` (IC `[−1.84,
+26.53]`, cruza 0) — no discrimina. La métrica secundaria en puntos
porcentuales **sí discrimina, en ambos pares**: los dos intervalos de la
tabla de arriba son íntegramente positivos — `M` tiene, con esta métrica,
un error absoluto medio significativamente menor que `L_solo` y que
`L+corpus`, sobre las 14 celdas. **Esto no reabre ni sustituye el
veredicto primario `INDETERMINADO` de §3** (regla de arriba, "carácter
no-gatante") — es la respuesta a la pregunta que `D4` pre-registró: sí,
existe una métrica secundaria pre-registrada que discrimina donde `z`/
banda no discrimina, y el sentido de la discriminación es que `M` se
desvía menos de `R`, en puntos porcentuales absolutos, que cualquiera de
los dos corredores `L`.

**Deriva de:**
`forense/benchmark/BENCHMARK-MOTORES-COMPARABLES.md` §4-5 (`D4`, la
pregunta que esta sección responde) · `agregado-v1_2-resultado.json`
(evidencia numérica que motivó `D4`: proporción en banda 0-7%,
`comparacion_principal_pareada` `INDETERMINADO`) · §1-§3 de este documento
(unidades, agregado marginal, comparación pareada — la forma que esta
sección reutiliza con `err_pp` en vez de `z`) · decisión de dirección del
encargo `MAESTRA38-M13` (D-B: `D4` = puntos porcentuales, no Brier) ·
`agregado_v1_3.py` (`_metrica_secundaria_pp`, cálculo real, primera y
única corrida).

**Lo que esta sección NO hace:** no fija ningún `delta_pp` (banda de
indiferencia en puntos porcentuales) — `D4` no lo pre-registró, y esta
sección no inventa uno; el orden reportado es de signo del IC, no de
banda. No cambia `delta=0.5` de §1 ni la banda `z`. No re-abre `D1`
(corredor `P`) ni ninguna de las tres decisiones (`D2`/`D3`) que el
benchmark dejó sin contenido.
