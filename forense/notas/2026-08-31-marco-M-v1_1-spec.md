# COMMIT-1 · spec congelada de MARCO-M-CORRIGE-Y-CENSA (ACTO C′)

`ACTO MAESTRA32-E15 · MARCO-M-CORRIGE-Y-CENSA-TRANSFERENCIA`, 31/ago/2026.
Receta escrita y congelada ANTES de recorrer los cuatro inventarios de
reactivos (`data/inventario-reactivos-v1_2.tsv`,
`data/inventario-reactivos-ext-v1_0.tsv`, `data/inventario-fd-v1_1.tsv`,
`data/inventario-fd-ext-v1_0.tsv`) para producir
`candidatos-marco-M-v1_1.tsv` en COMMIT-2. No se edita después de correr
COMMIT-2 — "el primer resultado que produzca este procedimiento es el que
se reporta" (última línea de este documento, verbatim del encargo).

## (a) Procedencia de `p` por regla — fija `ola_calibracion`

`tramite.mordida.discrecional` → `paga_mordida`: `milpa/tramite.yaml:40-50`.
`p: 0.62` en la línea 45 trae `clase: ASIGNADO` explícito — no `MEDIDO`.
`fuente:` en la línea 50: `["ENCIG2023", "Rothstein_trampa_social",
"report:politica"]`. `milpa/procedencia.yaml:782-786`
(`asignados_probabilidad`, regla `tramite.mordida.discrecional`) confirma
la misma clase con una verificación adicional fechada: *"verificado
29/jul/2026 contra microdatos ENCIG 2023 ... 0.62 NO corresponde a ninguna
categoría medida -- es ASIGNADO, confirmado"*.

**Lectura de este acto**: `p` es ASIGNADO, no MEDIDO — la mesa no calibró
esta probabilidad contra un procedimiento estadístico transparente; asignó
un juicio informado citando ENCIG2023 como ancla de *dirección*, no de
magnitud (mismo texto: *"la fuente citada sostiene la DIRECCIÓN, no la
magnitud"*, `procedencia.yaml:13-14`, clase ASIGNADO). Pese a no ser
MEDIDO, `ENCIG2023` es la ÚNICA encuesta/ola que el propio archivo de
reglas cita como ancla para este `p` — ninguna otra candidata compite. Este
spec fija, por esa razón declarada y no por adivinanza:

**`ola_calibracion(tramite.mordida.discrecional) = ENCIG 2023`**

Aplica a toda fila de este censo cuyo `regla = tramite.mordida.discrecional`
(`TRA-M-01`, `TRA-M-02`, y cualquier fila nueva de transferencia que
comparta esa regla) — es propiedad de LA REGLA, no de la fila.

## (b) Lista cerrada de estadísticas del motor a buscar en otras olas

Dos categorías, buscadas ambas, tratadas distinto en (e):

**Categoría A — desenlace de la propia regla `tramite.mordida.discrecional`**
(la única regla del motor con `p` + desenlace MEDIDO citable, per hallazgo
estructural de `MAESTRA32-E13`, cierre §"Por dominio": `cargar_reglas()`
solo lee `milpa/tramite.yaml`, 5 reglas, dominio único `tramite`):

  - `P8_3_1` (ENCIG) — desenlace de `coeficientes_generador_medidos.
    G1_confianza_institucional`, `procedencia.yaml:937` (batería
    `encig2023_01_sec1_A_3_4_5_8_9_10`).
  - `AP5_17`/`AP5_18` (ENCUCI, compuesto) — desenlace de
    `coeficientes_generador_medidos.G1_radio_confianza`, `procedencia.yaml:888`,
    corregido por C1 de este acto.

**Categoría B — desenlaces de los otros 4 pares medidos de la sección
`coeficientes_generador_medidos`** (`procedencia.yaml:884-1096`), buscados
por instrucción explícita del encargo ("se copian, no se interpretan"),
NO porque tengan regla compilada propia — verificado que NO la tienen, ver
(d):

  - `BP1_23` (ENVIPE) — desenlace compartido de `G4_exposicion_violencia`
    (`procedencia.yaml:998`) y `G4_confianza_institucional_justicia`
    (`procedencia.yaml:1029`). Calibración: ENVIPE 2025.
  - `p4_10`/`P4_10` (ENIF) — desenlace de `G3_familismo_apoyo`
    (`procedencia.yaml:969`, `dinero.ahorro.volatilidad_horizonte_corto`).
    Calibración: ENIF 2024.
  - `cr27` (ENNViH/MxFLS) — desenlace del par sellado en
    `coeficientes_generador_sellados` (`procedencia.yaml:1286-1296`,
    `gen: G3, coef: horizonte_temporal`), fuente
    `forense/notas/2026-08-24-cal-g3-puntual-cierre.md:38`: *"Desenlace =
    `cr27` ('Tiene ahorros'), binario `1=Sí` vs `3=No`"*. Calibración:
    ENNViH/MxFLS olas 2-3 (2005-06 → 2009-12) — panel, no una ola única
    (nota de la propia fuente, líneas 40-46).
    `G3_horizonte_temporal` dentro de `coeficientes_generador_medidos`
    (`procedencia.yaml:1060-1096`) es un `GATE·ID-X` que NO llegó a
    estimar nada (desenlace intentado `ah03h`/AFORE, no `cr27`) — el par
    que sí produjo número usa `cr27`, vive en
    `coeficientes_generador_sellados`, no en la sección A.

## (c) Criterio de "misma estadística en otra ola"

Mismo `variable_id` (comparación case-insensitive: los cuatro inventarios
mezclan mayúsculas/minúsculas para el mismo reactivo, verificado en (b) de
la nota de cierre) en un `instrumento` de la MISMA FAMILIA (prefijo
`encig`/`encuci`/`envipe`/`enif`/`ennvih`/`mxfls`) y otra `ola`, buscado
sobre la UNIÓN de los cuatro inventarios (`v1_2 ∪ ext-v1_0 ∪ fd-v1_1 ∪
fd-ext-v1_0`). Si el id cambió entre olas (p.ej. `BP1_23` en `envipe2011`
aparece como `BP1_23_1`/`BP1_23_2`, ítems desdoblados) NO se persigue por
coincidencia de `texto_reactivo`: las cuatro tablas traen `texto_reactivo`
vacío en el 100% de sus filas para el método `INSPECT_ZIP` (hecho ya
verificado por `ACTO MAESTRA31-E4`/FP-171, enmienda F1) — no hay texto que
comparar. Límite declarado, no resuelto aquí: un `variable_id` que cambió
de nombre entre olas queda fuera de este censo por construcción.

Instrumento distinto de la MISMA FAMILIA TEMÁTICA (p.ej. mordida
ENCIG↔ENCUCI, la relación exacta entre `TRA-M-01` y `TRA-M-02`) cuenta como
**transferencia de instrumento** — se marca `grado_transferencia=P1`,
`transferencia=SI`, con razón que dice "instrumento", no "ola".

## (d) `grado_sellado` y `grado_transferencia`

**`grado_sellado`**: el que dicta `forense/notas/2026-08-20-act-pil-2-marco.md`,
sección `### grado_dependencia, derivado y no tecleado`, línea 125,
verbatim: *"`P0` = el par `(encuesta, ola)` aparece en
`milpa/procedencia.yaml` como ruta de parametrización de `M`. Derivado por
barrido del YAML: **ENCIG 2021, ENCIG 2023, ENCUCI 2020, ENIF 2024, ENVIPE
2025, ENASIC 2022**, más **ENIGH 2022** ... `P1` = misma familia, otra ola,
o familia nombrada sin ola. `P2` = el resto."*

`grado_sellado` es propiedad del PAR `(encuesta, ola)`, no de la variable
ni de la regla — una fila puede caer P0 por parametrizar un par MEDIDO
distinto del que la fila mide (p.ej. ENCIG 2021 es P0 porque parametriza
`condicionales_confianza_institucional.salud` vía `P11_1_3`,
`procedencia.yaml:183-193`, no porque mida `P8_3_1`; una fila de censo con
`encuesta=ENCIG, ola=2021, variable=P8_3_1` es P0 por el PAR, con esa
salvedad citada en `razon`).

`grado_sellado` fijo por par, derivado mecánicamente de la lista de arriba,
SIN excepción ni interpretación:

| par | grado_sellado |
|---|---|
| ENCIG 2021 | P0 |
| ENCIG 2023 | P0 |
| ENCUCI 2020 | P0 |
| ENIF 2024 | P0 |
| ENVIPE 2025 | P0 |
| ENASIC 2022 | P0 |
| ENIGH 2022 | P0 (lectura conservadora, citada arriba) |
| cualquier otro par de las familias ENCIG/ENCUCI/ENVIPE/ENIF/ENNViH/MxFLS | P1 (misma familia, otra ola) |

**`grado_transferencia`**: `P1` si `(ola, instrumento)` de la fila ≠
`ola_calibracion` de su regla (de (a)); `P0` si coincide. Regla ESCRITA
aquí, NO adjudicada — es la misma tensión P0/P1 que `MAESTRA32-E13` declaró
para `grado_dependencia` (cierre, hallazgo 1) y que la mesa no ha resuelto
(D-D); este acto registra el resultado mecánico de la fórmula, no decide
cuál de los dos grados "vale". `grado_dependencia` (columna heredada de
v1_0) permanece SIN TOCAR en `TRA-M-01`/`TRA-M-02` (siguen `P1`, la
desviación declarada de E13) y se deja en blanco (`PENDIENTE-D-D`) en toda
fila nueva — asignarle un valor sería adjudicar D-D por la puerta de atrás.

## (e) Filas que produce este censo — regla de elegibilidad para la TABLA

Una fila de `candidatos-marco-M-v1_1.tsv` representa una celda que
`milpa/src/emisor.py:emitir_binaria(regla, conducta)` PODRÍA algún día
correr — exige `regla ∈ cargar_reglas()`, es decir `regla ∈
milpa/tramite.yaml`. Verificado directamente (`ls milpa/*.yaml` → solo
`procedencia.yaml`, `refutations.yaml`, `tramite.yaml` — CERO archivos de
reglas compilados para los dominios dinero, comunicación o familia) y confirmado
por el propio cierre de `MAESTRA32-E13`: *"el motor real (`cargar_reglas()`,
que solo lee `milpa/tramite.yaml`) no tiene ninguna regla de esos dominios
... el techo del criterio EMITE no es la disponibilidad de desenlaces
medidos, es la cobertura de dominios del motor mismo (1 de 10)"*.

Por eso:

- **Categoría A** (P8_3_1, AP5_17|AP5_18 — desenlace de
  `tramite.mordida.discrecional`) produce fila COMPLETA de
  `candidatos-marco-M-v1_1.tsv`, con `regla`/`conducta` poblados igual que
  `TRA-M-01`/`TRA-M-02`, IDs nuevos `TRA-M-03`, `TRA-M-04`... en orden de
  ola ascendente. Estas filas SÍ cuentan para el umbral `≥8` de B-bis.

- **Categoría B** (BP1_23, p4_10, cr27 — desenlaces de pares MEDIDOS sin
  regla compilada en ningún dominio) se busca en el corpus por instrucción
  explícita de (b) y se REPORTA en la nota de cierre con A.13 completo
  (cuántas filas de inventario examinadas, cuántos hits, en qué olas), pero
  NO produce fila de `candidatos-marco-M-v1_1.tsv`: no hay `regla` que
  poblar sin inventarla, mismo criterio que aplicó `MAESTRA32-E13` para
  excluir los 4 candidatos de `asignados_probabilidad` con regla real pero
  sin encuesta/variable citada ("no hay `encuesta`/`variable` que teclear
  sin inventarla"). Aquí es lo simétrico: hay encuesta/variable, no hay
  regla. Estos hallazgos NO cuentan para el umbral `≥8` de B-bis — contarían
  como falso positivo de "el marco-M puede crecer" cuando en realidad
  ninguna fila de Categoría B es ejecutable por `emitir_binaria` hoy.

Regla de columnas para toda fila nueva de Categoría A: los campos que
exigirían re-derivar contra microdato (`universo` con n exactos,
`estimador`, `ponderador`, `n_no_ponderado`, `cv_arbitro` con batería
completa, `dificultad`, `estrato`, `clase_procedencia`, `en_marco_60`,
`elegible`) quedan **NO ESTIMADO EN ESTE ACTO** o en blanco — este acto es
un censo de EXISTENCIA sobre el inventario de reactivos (`variable_id`
presente en tal instrumento/ola), NO una re-derivación contra microdato
(el objeto lo dice: "Sin congelar. Sin sortear. Sin emitir."). `base_medida`
= `NO` en toda fila nueva (nada se ha medido todavía para esas olas en este
acto). `en_corpus` = `SI` si el `variable_id` aparece en al menos uno de
los cuatro inventarios para ese instrumento/ola, verificado por comando.

## (f) B-bis — interpretación (documentada, no adjudicada)

`≥8` celdas de transferencia (`transferencia=SI`, `en_corpus=SI`, contando
SOLO Categoría A + las dos filas corregidas de v1_0 que califiquen) → el
marco-M puede llegar a tamaño de sorteo real bajo D-D. `1-7` → corto, se
dice cuáles. `0` → el corpus no tiene otras olas de las estadísticas del
motor y la vía (ii) no puede crecer sin (i′). El resultado real se reporta
en la nota de cierre (COMMIT-2), no se adelanta aquí.

"El primer resultado que produzca este procedimiento es el que se reporta."
