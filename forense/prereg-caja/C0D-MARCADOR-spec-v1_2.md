# C0D-MARCADOR · Pre-registro del **marcador GEN2** — la pareada `L_SOLO ↔ L_CORPUS` como comparación de primera clase

### `prereg-caja-C0D-MARCADOR` · **v1.2** · 9 de septiembre de 2026 · `sucesora_de: v1_1`

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/C0D-MARCADOR-spec-v1_2.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-C0D-MARCADOR`** — cítalo así, nunca por nombre de archivo |
> | **SUCESORA DE** | **`v1.1`** (`forense/prereg-caja/C0D-MARCADOR-spec-v1_1.md`, `sha256 = 604008c7ae0d5f82e12bb8aacee39f73ae676c794d9c067de73b0e56ae3f40cd`), que a su vez sucede a **`v1.0`** (`sha256 = c249e3b2ad8efd64326dc4b65ca770ca20e0e7fdac78dc2696e84a9838c56bd9`). **Ningún sello anterior se edita:** los bytes de `v1.0` y `v1.1` quedan intactos, sus sidecars siguen verificando, y las dos corridas que existen contra ellas —`CALC-C0D-MARCADOR` (PARÓ por su propia guardia) y `CALC-C0D-MARCADOR-v2` (152 `RESULT`, `verify` REPRODUCE)— **siguen siendo corridas válidas de sus specs y no se retiran**. |
> | **LA ÚNICA DIFERENCIA, Y NINGUNA MÁS** | **§5 — el mapa de adjudicación**, y la guardia §3.5 que lo protege. `v1.1` mapeaba el veredicto de la pareada a un destino por una escalera con **veto de universo** y con un **`else` mudo**; el mapa decía más de lo que la evidencia sostiene. `v1.2` lo reescribe **exhaustivo, explícito y sin `else`**, deriva la adjudicación **sólo** de la pareada `L↔L` sobre `U_LL`, degrada el efecto de universo a **diagnóstico** y separa el **sucesor de alcance** del signo del veredicto. **`NC-0081`.** |
> | **QUÉ NO CAMBIA** | Todo lo demás, verbatim de `v1.1`: §0 entero, §1 (fuente del punto `L`, escala, las dos familias de `MAE_pp`), §2 (**la pareada primaria, su signo, su bootstrap y sus parámetros — ni una coma**), §3.1–§3.4 (secundarias, piso `B`, conmensurabilidad, convergencia), §4 (**las cuatro ramas del veredicto de la pareada y su precedencia — ni una coma**), §6, §7 y §8. **Las cifras no se tocan: `v1.2` no cambia ni un insumo, ni un estimador, ni un parámetro, ni una rama de §4. Cambia a dónde va el veredicto, no cuál es.** |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-C0D-MARCADOR-v3` en VERDE; después `run` y `verify`. |

**Acto:** `ACTO GEN2-C0-D-CORRECTIVO`, 9/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado.

**Firma que lo autoriza, verbatim de mesa (9/sep/2026):** *«chutate este»* — mesa remitió a dirección la revisión adversarial externa de `PR #649` y la validó; remitirla es ordenar la corrección.

---

## 0.5 · Por qué existe esta sucesora — el defecto está en el CÓDIGO, y se lee en él

`CALC-C0D-MARCADOR-v2` corrió, selló 152 `RESULT`, `verify` dio `REPRODUCE`, y **sus cifras son correctas**. El defecto no está en ninguna cifra: está en la función que traduce el veredicto a un destino. Verbatim de `data/corrida0/CALC-C0D-MARCADOR-v2/medidor.py:373-385`, que es el que corrió:

```python
    # --- 8) adjudicacion del hallazgo, por la precedencia de §5 -----------
    if diverge or out["RESULT-C0D-CONTROL-CORRESPONDENCIA"] != "CORRESPONDE":
        adj = "NO-ADJUDICA-POR-CONTROL"
    elif veredicto == "NO-ESTIMABLE-POR-COBERTURA":
        adj = "NO-ESTIMABLE-POR-COBERTURA"
    elif (not identicos) and (rank_marginal != rank_comun):
        adj = "EXPLICADO-POR-UNIVERSO"
    elif veredicto == "NO-DISCRIMINA":
        adj = "EXPLICADO-POR-METRICA"
    elif veredicto == "CORPUS-ESTORBA":
        adj = "CONFIRMADO-CON-ALCANCE"
    else:
        adj = "EXPLICADO-POR-METRICA"
```

**Tres defectos, cada uno con su contraejemplo mecánico:**

### (a) El veto de universo — el ranking de `M` decide una comparación en la que `M` no participa

La línea 378 evalúa `rank_marginal != rank_comun` **antes** de mirar el veredicto de la pareada, y si el orden de los tres `MAE` cambió al igualar universos, adjudica `EXPLICADO-POR-UNIVERSO` **cualquiera que sea el intervalo de la primaria**.

Pero la primaria es `L_SOLO ↔ L_CORPUS` sobre `U_LL`: **misma celda, mismo `R`, misma ventana, mismo modelo, y la única diferencia es el corpus.** `M` no entra en ella. Su ranking puede cambiar por razones que no tocan un solo `d_i` — basta que `M` tenga punto en una celda donde `L_SOLO` no lo tiene.

**Contraejemplo A (falsador, ejecutado en §5-ter):** primaria concluyente con `ic_lo > 0` sobre `n_LL ≥ 10` (el corpus estorba, inequívocamente) **y** `rank_marginal ≠ rank_comun`. `v1.1` responde `EXPLICADO-POR-UNIVERSO`: **un intervalo que excluye cero queda archivado como artefacto de un universo que no lo produjo.** Es una comparación de primera clase vetada por un diagnóstico de tercera.

### (b) `NO-DISCRIMINA → EXPLICADO-POR-METRICA` — un intervalo que cruza cero no explica nada

La línea 380-381 llama **`EXPLICADO`** a lo que la línea 380 acaba de reconocer como **`NO-DISCRIMINA`**. Un IC95 que cruza cero dice *no sé de qué lado está*; el token `EXPLICADO-POR-METRICA` dice *ya sé por qué pasaba lo que se veía*. **Lo segundo no se sigue de lo primero.** Con `n_LL = 13` y un IC de `−0.80` a `+11.27`, la lectura honesta es que **la comparación no discrimina la dirección**, no que la diferencia marginal quede explicada.

Esto no es un matiz de redacción: el token es lo que viaja al ADR, a `estado-programa` y a cualquier acto que cite este resultado. Un `EXPLICADO` cierra una pregunta; un `INCONCLUSO` la deja abierta con su `n` a la vista.

### (c) El `else` mudo — la rama que refuta se reporta como la rama que explica

Las líneas 384-385 no son una rama: son el resto. Y en ese resto cae exactamente un caso, `CORPUS-AYUDA` (`ic_hi < 0`), que es **la refutación inequívoca del hallazgo del 8/sep** y la confirmación directa de D-2 en su lectura literal. `v1.1` la reportaría como `EXPLICADO-POR-METRICA`.

**Contraejemplo B (falsador, ejecutado en §5-ter):** primaria con `ic_hi < 0` sobre `n_LL ≥ 10`, universos idénticos. `v1.1` responde `EXPLICADO-POR-METRICA`. **El resultado más informativo que este marcador puede producir sale rotulado como el más neutro.**

### Lo que esta sucesora NO es

**No es una rama reescrita a la luz del dato.** Las cuatro ramas de §4 —las que miran el intervalo y deciden el veredicto— **no se tocan**, y el dato observado sigue cayendo en la misma: `NO-DISCRIMINA`. Lo que cambia es el nombre de su destino, y cambia **hacia menos**: de `EXPLICADO-POR-METRICA` a `INCONCLUSO`. Una corrección que redujera la exigencia sería sospechosa; ésta **retira una afirmación que el intervalo no sostenía**.

**Y se declara la contaminación, sin adorno (ADR-46):** al redactar `v1.2` la sesión **ya conoce** el resultado de `v2` — `+4.6978 pp`, `IC95 [−0.8022, +11.2747]`, `n = 13`, `NO-DISCRIMINA`. Por eso `v1.2` **congela que las cifras deben permanecer idénticas** (§5-bis, control `CIFRAS-INTACTAS`): si el mapa nuevo moviera una sola cifra, no sería un mapa nuevo sino una medición nueva disfrazada. Los dos contraejemplos que justifican la corrección son **sintéticos y ajenos al dato observado**: valen por la estructura del `if`, no por lo que salió.

---

## 1 · La cantidad que se mide

**Verbatim de `v1.1` §1, sin cambio alguno.** Todo lo de esta sección se copia, sin reinterpretar, del procedimiento **ya sellado** `procedimiento-scoring-v1_2.md` §7 tal como `agregado_v1_1.py` y `agregado_v1_3.py` lo implementan. **Este marcador no inventa métrica; inventa la comparación que faltaba.**

### 1.1 · Punto por celda y corredor

- **`L_SOLO` / `L_CORPUS`** — media de la columna `valor` de `forense/prereg-duelo-v2/L-extraido-v1_2.tsv` sobre las filas de ese `(id_celda, variante)` con `estado == "EXTRAIBLE"`. Si ninguna de las 8 réplicas es `EXTRAIBLE`, el punto es `NO-DISPONIBLE`; **no se sustituye por 0 ni por nada**. El TSV trae **224 filas** y el conteo se **asevera**: si no son 224, PARA.
- **`M`** — `valor_punto` del archivo que resuelve el orden §16 de `MAESTRA38-M13`: `M-<id>__v1_3.json` → `M-<id>.json` → `M-<id>__v1_2.json`, primera coincidencia exacta.
- **`R`** — campo `R` de `corridas-R/<id>.json` cuando `estado == "COMPUTADO"`; su `EE_R` acompaña.
- **`B`** — §0.2: `RESULT-B-PERSISTENCIA-<ola>-P` y `RESULT-B-OPERATIVO-<ola>-P` de `CALC-B-0001`, sólo en `FAM-M-06` y `FAM-M-07`.

### 1.2 · Error, escala declarada (A-bis 3)

`err_pp(corredor, celda) = 100 · (punto − R)`, **con signo**. Unidad: **puntos porcentuales de una proporción ponderada**.

### 1.3 · Las dos familias de `MAE_pp`

- `RESULT-C0D-MAE-MARGINAL-<corredor>` — cada corredor sobre **su propio** subconjunto disponible. **Reproduce D4 y sirve sólo para comparar contra él.**
- `RESULT-C0D-MAE-COMUN-<corredor>` — cada corredor sobre el **universo común** `U∩`. **Ésta es la única que A-bis 4 autoriza a comparar entre corredores.**

---

## 2 · La comparación primaria: la pareada `L_SOLO ↔ L_CORPUS`

**Verbatim de `v1.1` §2, sin cambio alguno.**

**Universo:** `U_LL` = celdas con `R` computado **y** punto en `L_SOLO` **y** punto en `L_CORPUS`.

```
d_i = |err_pp(L_CORPUS, i)|  −  |err_pp(L_SOLO, i)|
```

**`d_i > 0` significa que el corpus ALEJÓ a `L` del patrón oro en esa celda.**

**Estadístico:** media de `d_i` sobre `U_LL`, con IC95 por **bootstrap no paramétrico sobre celdas**, con la maquinaria **ya sellada** del duelo consumida desde los bytes verificados por `sha256` de `forense/prereg-duelo-v2/scoring-adv1-m3.py`, y con los mismos parámetros sellados: **`seed = 42`**, **`replicas = 10000`**, **`nivel_ic = 0.95`**, `scope_id = "mae_pp::pareado::L_CORPUS_vs_L_SOLO::c0d_v1_0"`. **Los `scope_id` conservan el sufijo `c0d_v1_0` a propósito: cambiarlos cambiaría la semilla derivada y por tanto las cifras, que es justo lo que esta sucesora prohíbe.**

---

## 3 · Comparaciones secundarias — se reportan como tales, no adjudican

**Verbatim de `v1.1` §3.1–§3.4.** La primaria decide; las secundarias se reportan y no mueven el veredicto. Se calculan sobre `U∩` salvo donde se diga.

### 3.1 · `L_SOLO ↔ M` y `L_CORPUS ↔ M`
Mismo estadístico, `d_i = |err_pp(L, i)| − |err_pp(M, i)|`, con sus `scope_id` propios, sobre `U∩`.

### 3.2 · `M ↔ B`
Sólo sobre las 2 celdas de §0.2. **`n = 2`: se emite el par de errores crudo y NO un IC.** Se reporta `NO-ADJUDICA-POR-N`.

### 3.3 · La guardia de conmensurabilidad de `B` (A-bis 4)
`|RESULT-B-ENIGH-<ola>-P − R(celda)| ≤ 1.96 · EE_R(celda)` → `PISO-CONMENSURABLE`; si no, **`PISO-NO-CONMENSURABLE`** y `B` no entra a ninguna comparación.

### 3.4 · Control de convergencia — el marcador contra el agregado sellado
`RESULT-C0D-CONTROL-CONVERGENCIA-L` = `CONVERGE` / `DIVERGE:<lista>` y `RESULT-C0D-CONTROL-MAXDIF-L`. **`DIVERGE` manda** por §5.1.

### 3.5 · Guardia de correspondencia TSV ↔ capturas — **REFORZADA en `v1.2`**

`RESULT-C0D-CONTROL-CORRESPONDENCIA` = `CORRESPONDE` / `DISCORDA:<detalle>`.

**El defecto que `v1.1` dejaba pasar:** su guardia construía la llave de captura como `(cid, variante, k)` donde `cid` y `k` salían **del identificador del input** (`IN-L-<tag>-<cid>-<kk>`, es decir del nombre del archivo), y **sólo `variante` se contrastaba contra el contenido declarado por la captura**. Una captura cuyo `id_celda` o `indice` internos no coincidieran con su propio nombre de archivo pasaba la guardia sin ruido — y el punto `L` de esa celda se habría formado con réplicas de otra.

**`v1.2` contrasta las tres:** para cada captura, `id_celda`, `variante` e `indice` se leen **del contenido del JSON** y se comparan contra los que el identificador del input declara. Cualquier discordancia es `DISCORDA` y **PARA la adjudicación** por §5.1, igual que `DIVERGE`. El detalle nombra el campo que discordó, no sólo el conteo.

Es la misma lección desde el otro lado que ya pagó `v1.0`: *una lectura que no se apoya en las capturas que dice leer no adjudica nada* — y «las capturas que dice leer» se identifica **por identidad declarada, no por rótulo de archivo**.

---

## 4 · B-bis — las cuatro ramas del veredicto de la pareada

**Verbatim de `v1.1` §4, sin tocar una coma.** Sea `IC95(media d)` = `[lo, hi]` sobre `U_LL`, y `n_LL = |U_LL|`.

| # | rama | condición mecánica | lectura |
|---|---|---|---|
| **0** | **`NO-ESTIMABLE-POR-COBERTURA`** | `n_LL < 10` | **No adjudica, cualquiera que sea el intervalo.** Precede a todas las demás. |
| **1** | **`CORPUS-ESTORBA`** | `lo > 0` | El corpus **aleja** a `L` del patrón oro, pareado y con el mismo universo. **CONFIRMA** el hallazgo del 8/sep. |
| **2** | **`CORPUS-AYUDA`** | `hi < 0` | El corpus **acerca** a `L` al patrón oro. **REFUTA** el hallazgo del 8/sep y sostiene D-2 en su lectura directa. |
| **3** | **`NO-DISCRIMINA`** | `lo ≤ 0 ≤ hi` | La pareada **no distingue** los dos brazos. |

**Ninguna otra rama existe**, y las cuatro son **exhaustivas y mutuamente excluyentes** sobre cualquier `(lo, hi, n_LL)`: `n_LL < 10` o no; y si no, `lo > 0`, `hi < 0` y `lo ≤ 0 ≤ hi` cubren la recta sin hueco ni solape (dado `lo ≤ hi`). Si el cómputo produjera algo fuera de las cuatro, el veredicto es `NO-ESTIMABLE-POR-COBERTURA` por la rama 0, con `n_LL` escrito.

**La lectura que NO se autoriza:** que `CORPUS-ESTORBA` signifique *«el corpus es malo»*. A-bis 1–2 aplican íntegras. El enunciado máximo que la rama 1 autoriza es: *«con el corpus del 1–2/sep delante, este corredor se alejó más del patrón oro en estas 14 celdas»* — y el simétrico para la rama 2.

---

## 5 · La adjudicación del hallazgo `corpus-empeora` — **reescrita en `v1.2`**

**Principio, y es el que la revisión adversarial impuso: la adjudicación es una FUNCIÓN del veredicto de §4, y de nada más.** La primaria se deriva **sólo** de `L↔L` sobre `U_LL`. Ningún diagnóstico sobre `M`, sobre universos o sobre marginales puede vetarla, precederla ni sustituirla.

**Precedencia — dos guardias de insumo, y luego el mapa. La primera que aplica decide.**

### 5.1 · `NO-ADJUDICA-POR-CONTROL` — guardia de insumo
Si `RESULT-C0D-CONTROL-CONVERGENCIA-L` empieza por `DIVERGE` **o** `RESULT-C0D-CONTROL-CORRESPONDENCIA` no es `CORRESPONDE`. Entonces la lectura no se apoya en las capturas que dice leer, y adjudicar sobre ella sería adjudicar sobre nada.

### 5.2 · `NO-ESTIMABLE-POR-COBERTURA` — guardia de cobertura
Si el veredicto de §4 es `NO-ESTIMABLE-POR-COBERTURA` (`n_LL < 10`). Se reporta el punto y no se adjudica.

### 5.3 · El mapa — **exhaustivo, explícito, sin `else`**

Pasadas las dos guardias, el veredicto de §4 sólo puede ser uno de tres, y cada uno tiene **su** destino:

| veredicto de §4 | adjudicación | lectura autorizada |
|---|---|---|
| **`CORPUS-ESTORBA`** (`lo > 0`) | **`CONFIRMADO-CON-ALCANCE`** | El hallazgo del 8/sep **sobrevive al pareo**, con el alcance de §5.4. |
| **`CORPUS-AYUDA`** (`hi < 0`) | **`REFUTADO-CON-ALCANCE`** | El hallazgo del 8/sep **queda refutado**: pareado, el corpus acercó a `L` al patrón oro. Con el mismo alcance de §5.4, que limita igual a la refutación que a la confirmación. |
| **`NO-DISCRIMINA`** (`lo ≤ 0 ≤ hi`) | **`INCONCLUSO`** | **La comparación no discrimina la dirección.** No se afirma que el hallazgo esté explicado, ni que sea falso, ni que sea cierto: se afirma que **con este `n` y este intervalo no se puede decidir**, y se nombran las celdas dominantes (`RESULT-C0D-CELDAS-DOMINANTES`) como descripción, no como explicación. |

**El mapa se implementa como diccionario, no como escalera:** las tres claves son exactamente las tres ramas no-guardia de §4, y una clave ausente **levanta excepción y para la corrida**. No hay `else`, no hay destino por defecto, y ninguna rama de §4 puede quedarse sin destino sin que la corrida caiga ruidosamente.

**Prohibido, explícitamente:** introducir una prueba de equivalencia, un umbral post-hoc, una banda de indiferencia o cualquier otro criterio que convierta `INCONCLUSO` en una afirmación positiva de «no hay diferencia». `INCONCLUSO` es la ausencia de una conclusión, y esta spec no autoriza fabricar una.

### 5.4 · El sucesor de alcance — **separado del signo del veredicto**

`v1.1` ataba el sucesor a `CONFIRMADO-CON-ALCANCE`, de modo que sólo una confirmación podía nombrarlo. Es la condición equivocada: **el alcance limita a los tres destinos por igual**, porque el corpus que estaba delante del corredor es el mismo cualquiera que sea el signo del intervalo.

`v1.2` vuelve a la condición del encargo original, que es **material y no de signo**:

> Si `RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES > 0` —es decir, si entró corpus al manifiesto **después** de la ventana de captura del brazo `L+corpus`—, el brazo `L+corpus` se midió contra un corpus **pre-GEN2**, y el sucesor se nombra: **`NC-0077`**, la fila de deuda que `ACTO GEN2-C0-D` ya abrió para la re-captura de `L_CORPUS` con corpus GEN2.

**`NC-0077` se REUTILIZA, no se duplica: este acto no abre deuda nueva por este concepto.** Si el conteo es `0`, `RESULT-C0D-ADJUDICACION-SUCESOR = NO-APLICA`. El número gradúa la urgencia; **la existencia del sucesor la decide el conteo, no el veredicto.**

---

## 5-bis · El efecto de universo — **diagnóstico separado, jamás adjudicación**

`RESULT-C0D-DIAGNOSTICO-UNIVERSO`, texto, uno de tres:

- **`UNIVERSOS-IDENTICOS`** — los tres subconjuntos marginales son el mismo conjunto de celdas; la distinción no muerde.
- **`ORDEN-ESTABLE`** — los universos difieren pero el orden de los tres `MAE` no cambia al igualarlos.
- **`ORDEN-CAMBIA:<rank_marginal>→<rank_comun>`** — los universos difieren **y** el orden cambia.

**Y la lectura que este RESULT autoriza, verbatim y máxima:** *igualar el universo cambia (o no) la ordenación de los marginales.* **Nada más.** En particular **NO** autoriza concluir que la diferencia marginal quede explicada por el universo, ni tiene efecto alguno sobre §5. Es descriptivo de las tres cifras marginales; la adjudicación vive en la pareada.

El acompañamiento numérico se conserva de `v1.1` sin cambio: `RESULT-C0D-UNIVERSOS-IDENTICOS`, `RESULT-C0D-N-UNIVERSO-COMUN`, `RESULT-C0D-ORDEN-MARGINAL`, `RESULT-C0D-ORDEN-COMUN`.

---

## 5-ter · Falsadores del mapa — **ejecutados, no argumentados**

El mapa de §5 es código, y se falsa corriéndolo. El medidor evalúa la función de adjudicación sobre casos **sintéticos y ajenos al dato observado**, y sella el destino que produce. Un falsador que no dé el valor esperado **no se corrige al vuelo: para la corrida**.

| RESULT | caso sintético | esperado |
|---|---|---|
| `RESULT-C0D-FALSADOR-A-VETO-UNIVERSO` | veredicto `CORPUS-ESTORBA`, `n_LL = 13`, controles limpios, **universos distintos y orden cambiado** | **`CONFIRMADO-CON-ALCANCE`** — la primaria manda; el ranking de `M` no la veta |
| `RESULT-C0D-FALSADOR-B-CORPUS-AYUDA` | veredicto `CORPUS-AYUDA`, `n_LL = 13`, controles limpios, universos idénticos | **`REFUTADO-CON-ALCANCE`** — su rama propia, no el `else` |
| `RESULT-C0D-FALSADOR-C-NO-DISCRIMINA` | veredicto `NO-DISCRIMINA`, `n_LL = 13`, controles limpios | **`INCONCLUSO`** |
| `RESULT-C0D-FALSADOR-D-CONTROL` | controles **sucios** (`DIVERGE`) con veredicto `CORPUS-ESTORBA` | **`NO-ADJUDICA-POR-CONTROL`** — la guardia de insumo precede |
| `RESULT-C0D-FALSADOR-E-COBERTURA` | `n_LL = 9`, controles limpios | **`NO-ESTIMABLE-POR-COBERTURA`** — la guardia de cobertura precede |
| `RESULT-C0D-FALSADOR-F-EXHAUSTIVO` | una rama de §4 inventada, ajena a las cuatro | **`LEVANTA-EXCEPCION`** — el mapa no tiene destino por defecto |
| `RESULT-C0D-FALSADOR-G-SUCESOR-SIN-SIGNO` | `payloads_posteriores > 0` con veredicto `CORPUS-AYUDA` | **`NC-0077`** — el sucesor no depende del signo |

**Los falsadores A y B son los dos contraejemplos de la revisión adversarial**, ejecutados: son la prueba de que el defecto (a) y el defecto (c) de §0.5 están cerrados, y no la afirmación de que lo están.

---

## 5-quater · Control `CIFRAS-INTACTAS` — la corrección no puede mover una cifra

`RESULT-C0D-CONTROL-CIFRAS-INTACTAS` = `INTACTAS` / `MOVIDAS:<lista>`.

El medidor compara **toda** cifra que `CALC-C0D-MARCADOR-v2` selló y que `v3` vuelve a producir, contra `data/corrida0/CALC-C0D-MARCADOR-v2/resultados.json` (input `IN-V2-RESULTADOS`), con tolerancia `0.0` (**identidad exacta**, no aproximación).

**Los `RESULT` nuevos de `v1.2` quedan fuera por construcción** —no existen en `v2`, así que no hay contra qué compararlos—: `RESULT-C0D-DIAGNOSTICO-UNIVERSO` (§5-bis), los siete `RESULT-C0D-FALSADOR-*` (§5-ter), `RESULT-C0D-CONTROL-CIFRAS-INTACTAS` y `RESULT-C0D-CONTROL-N-CIFRAS-COMPARADAS`.

**Los únicos `RESULT` que SÍ existen en `v2` y quedan autorizados a diferir son tres, declarados por nombre** en `parametros.result_autorizados_a_diferir`:

```
RESULT-C0D-ADJUDICACION-HALLAZGO       (destino nuevo, §5.3)
RESULT-C0D-ADJUDICACION-SUCESOR        (condición nueva y material, §5.4)
RESULT-C0D-CONTROL-CORRESPONDENCIA     (guardia reforzada, §3.5)
```

**Cualquier otra diferencia es `MOVIDAS` y PARA la corrida.** `RESULT-C0D-CONTROL-N-CIFRAS-COMPARADAS` escribe cuántas cifras entraron efectivamente a la comparación, para que «`INTACTAS`» no pueda leerse sin su `n` — un control que compara cero cifras y dice `INTACTAS` no es un control (A.13). Es el control que separa «corregí el mapa» de «volví a medir hasta que saliera otra cosa», y se congela aquí, antes de correr.

---

## 6 · Lo que el marcador emite

Las familias de `v1.1` §6, **más** las tres nuevas de `v1.2`:

1. **Por celda** (14 × 6): `R`, `EE_R`, `err_pp` de los tres corredores, y `d_i`.
2. **`MAE_pp`** marginal y común, por corredor, con su `n` y su IC95.
3. **Las tres pareadas**: la primaria `L_CORPUS ↔ L_SOLO` y las dos secundarias contra `M`.
4. **`B`**: cita, cifra, conmensurabilidad y error, en las 2 celdas de §0.2.
5. **Veredicto** `RESULT-C0D-VEREDICTO-PAREADA` (§4) y **adjudicación** `RESULT-C0D-ADJUDICACION-HALLAZGO` (§5).
6. **Controles y alcance**: convergencia, correspondencia reforzada, universos, payloads posteriores.
7. **`v1.2`:** `RESULT-C0D-DIAGNOSTICO-UNIVERSO` (§5-bis), los siete `RESULT-C0D-FALSADOR-*` (§5-ter), `RESULT-C0D-CONTROL-CIFRAS-INTACTAS` y `RESULT-C0D-CONTROL-N-CIFRAS-COMPARADAS` (§5-quater). **Total: 152 de `v2` + 10 = 162.**

---

## 7 · Lo que esta spec explícitamente NO autoriza

Todo lo de `v1.1` §7, íntegro:

- No autoriza re-capturar `L` con otro corpus: eso es `NC-0077`.
- No autoriza tocar la banda `z` primaria del duelo ni `agregado_v1_*.py`.
- No autoriza mover ninguna regla, `tier`, `p` ni veredicto del motor (`T9`).
- No autoriza extender `B` fuera de la serie ENIGH·remesas (§0.2).
- No autoriza incorporar las 15 celdas del piloto, que no tienen brazo `L+corpus`.
- No autoriza aflojar `tolerancia.abs` para que una adopción pase.

**Y lo que `v1.2` añade:**

- **No autoriza editar los bytes de `v1.0`, de `v1.1`, ni de las corridas `CALC-C0D-MARCADOR` y `CALC-C0D-MARCADOR-v2`.** La corrección va por sucesión, hacia adelante, nunca hacia atrás.
- **No autoriza prueba de equivalencia ni umbral post-hoc** que convierta `INCONCLUSO` en una afirmación de no-diferencia (§5.3).
- **No autoriza que ningún diagnóstico** —universo, marginales, ranking de `M`, celdas dominantes— entre a la adjudicación (§5-bis).
- **No autoriza mover una sola cifra** de las que `v2` selló (§5-quater).

---

## 8 · Sello

**Parámetros congelados, idénticos a `v1.1`:** `seed = 42` · `replicas = 10000` · `nivel_ic = 0.95` · `n_minimo_pareada = 10` · `k_umbral_conmensurabilidad = 1.96` · `tolerancia_convergencia_L = 1e-9` · `n_filas_l_tsv = 224`.

**Parámetros nuevos de `v1.2`:** `tolerancia_cifras_intactas = 0.0` (identidad exacta) · `sucesor_alcance = NC-0077` · `result_autorizados_a_diferir` (los tres de §5-quater) · `falsadores_pre_declarados` (los siete de §5-ter, con su valor esperado escrito ANTES de correr).

**Insumos:** los **260** de `v2`, **byte-idénticos** (mismos `id`, mismas rutas, mismos `sha256`), más **uno solo de control**, `IN-V2-RESULTADOS`, que **ninguna medición lee** y que existe únicamente para §5-quater. Total declarado: **261**.

**Frase de sello, verbatim:** *el primer resultado que produzca este procedimiento es el que se reporta.*
