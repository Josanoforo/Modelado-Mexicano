# C0D-MARCADOR · Pre-registro del **marcador GEN2** — la pareada `L_SOLO ↔ L_CORPUS` como comparación de primera clase

### `prereg-caja-C0D-MARCADOR` · **v1.1** · 9 de septiembre de 2026 · `sucesora_de: v1_0`

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/C0D-MARCADOR-spec-v1_1.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-C0D-MARCADOR`** — cítalo así, nunca por nombre de archivo |
> | **SUCESORA DE** | **`v1.0`** (`forense/prereg-caja/C0D-MARCADOR-spec-v1_0.md`, `sha256 = c249e3b2ad8efd64326dc4b65ca770ca20e0e7fdac78dc2696e84a9838c56bd9`). **El sello de `v1.0` no se edita:** sus bytes quedan intactos, su sidecar sigue verificando, y `CALC-C0D-MARCADOR` —que corrió contra ella y **PARÓ por su propia guardia**— sigue siendo una corrida válida de `v1.0` y **no se retira**. |
> | **LA ÚNICA DIFERENCIA, Y NINGUNA MÁS** | **§1.1 — de dónde sale el punto `L`.** `v1.0` congeló *«media de `valor_extraido` sobre las réplicas del brazo con `valor_extraido` no nulo»*, citándolo verbatim de `agregado_v1_1._leer_l_variante`. **Esa regla es la del módulo BASE, y el agregado vigente la deroga.** `agregado_v1_2.py` sobreescribe `_leer_l_variante` por monkeypatch quirúrgico y lee el punto de **`forense/prereg-duelo-v2/L-extraido-v1_2.tsv`** (extractor `tools/extrae_l_v1_1.py`, `PR #497` / `ENMIENDA 3`), porque **`valor_extraido` es `null` en las 224 capturas crudas — por diseño, y declarado por el propio agregado** en `hallazgo_declarado.nota_v1_2`. `v1.1` escribe la fuente vigente. **`NC-0074`.** |
> | **QUÉ NO CAMBIA** | Todo lo demás, verbatim de `v1.0`: §0 entero (las cuatro premisas verificadas), §1.2 (la escala), §1.3 (las dos familias de `MAE_pp`), §2 (la pareada primaria, su signo, su bootstrap y sus parámetros), §3 (las secundarias, el piso `B` y su conmensurabilidad), §4 (**las tres ramas B-bis y la guardia de cobertura, sin tocar una coma**), §5 (**las cinco ramas de adjudicación y su precedencia, sin tocar una coma**), §6, §7 y §8. **Ni una rama pre-declarada se reescribe a la luz del dato: el dato que `v1.0` produjo fue `NO-ADJUDICA-POR-CONTROL`, que es precisamente la rama que mandó escribir esta sucesora.** |
> | **VERIFICAS ASÍ** | `python3 tools/corrida0.py preflight CALC-C0D-MARCADOR-v2` en VERDE; después `run` y `verify`. |

**Acto:** `ACTO GEN2-C0-D · EL MARCADOR`, 9/sep/2026, entorno **CAJA (UBUNTU)**, corpus montado.

**Firma que lo autoriza, verbatim de mesa (D-2 / `FP-348`, FIRMADA):** *«la idea central de todo este proyecto es un LLM puede superar a LLM con dato (todo el corpus), si esto no está claro ahorita entonces no estamos comparando correctamente.»*

---

## 0.5 · Por qué existe esta sucesora — el defecto, medido y no supuesto

`CALC-C0D-MARCADOR` (spec `v1.0`) corrió, selló 151 `RESULT` con `exit_code 0`, y **su propia guardia pre-declarada lo paró antes de adjudicar**:

```
RESULT-C0D-CONTROL-CONVERGENCIA-L = DIVERGE   (28 de 28 puntos, todos "uno-ausente")
RESULT-C0D-CONTROL-MAXDIF-L       = 0.0
RESULT-C0D-N-UNIVERSO-COMUN       = 0
RESULT-C0D-ADJUDICACION-HALLAZGO  = NO-ADJUDICA-POR-CONTROL      ← §5.4 de v1.0
```

`maxdif = 0.0` con 28 divergencias es la firma exacta del defecto: **ningún par de números discrepó — es que un lado del par nunca existió.** Los 28 puntos `L` re-derivados salieron `None` porque `valor_extraido` es `null` en las 224 capturas; el agregado los tenía porque los lee de otra parte.

**Lo que esto NO es:** no es que las capturas estén rotas, ni que el agregado esté desfasado, ni que el duelo haya medido mal. Las tres cosas están bien y **el propio agregado lo dice en su salida**:

> *«Sigue siendo cierto que `valor_extraido` es null en las 224 capturas crudas de `corridas-L/` para v1.2 — eso no cambia (las capturas no se editan). El punto de L de este agregado se lee de `L-extraido-v1_2.tsv` … no de `valor_extraido`.»*

**Lo que sí es:** `v1.0` leyó la regla en el módulo que el procedimiento nombra (`agregado_v1_1`) y no en el módulo que hoy corre (`agregado_v1_2`, que lo parchea). Una spec puede citar verbatim la fuente equivocada y seguir siendo verbatim. **La guardia congelada antes del dato es lo único que separó esto de una pareada sobre `n = 0` leída como falta de cobertura.**

`v1.1` corrige **la fuente y nada más**. Ninguna rama de veredicto se toca: reescribir una rama después de ver que el dato no llegó sería exactamente el vicio que el pre-registro existe para impedir.

---

## 1 · La cantidad que se mide

Todo lo de esta sección se copia, sin reinterpretar, del procedimiento **ya sellado** `procedimiento-scoring-v1_2.md` §7 tal como `agregado_v1_1.py` y `agregado_v1_3.py` lo implementan. **Este marcador no inventa métrica; inventa la comparación que faltaba.**

### 1.1 · Punto por celda y corredor

- **`L_SOLO` / `L_CORPUS`** — media de la columna `valor` de `forense/prereg-duelo-v2/L-extraido-v1_2.tsv` sobre las filas de ese `(id_celda, variante)` con `estado == "EXTRAIBLE"`. Si ninguna de las 8 réplicas es `EXTRAIBLE`, el punto es `NO-DISPONIBLE`; **no se sustituye por 0 ni por nada** (verbatim de `agregado_v1_2._leer_l_variante_v1_2`, que es el que corre). El TSV trae **224 filas** (14 celdas × 2 brazos × 8 réplicas) y el conteo se **asevera**: si no son 224, PARA — misma aserción que `_cargar_l_tsv_v1_2`.
  **Y la guardia nueva que `v1.0` no tenía** (`§3.5`): cada fila del TSV tiene que corresponder a una captura que existe en `corridas-L/`, y cada captura a una fila. Un TSV que describa réplicas inexistentes, o capturas que el TSV no cubre, **PARA** — es el defecto que `v1.0` pagó, mirado desde el otro lado.
- **`M`** — `valor_punto` del archivo que resuelve el orden §16 de `MAESTRA38-M13`: `M-<id>__v1_3.json` → `M-<id>.json` → `M-<id>__v1_2.json`, primera coincidencia exacta, sin otra heurística.
- **`R`** — campo `R` de `corridas-R/<id>.json` cuando `estado == "COMPUTADO"`; su `EE_R` acompaña. Si no es `COMPUTADO`, la celda no tiene patrón oro y **sale de todo agregado**.
- **`B`** — §0.2: `RESULT-B-PERSISTENCIA-<ola>-P` (brazo primario) y `RESULT-B-OPERATIVO-<ola>-P` (secundario) de `CALC-B-0001`, citados por `corrida0_resultado_id`, sólo en `FAM-M-06` y `FAM-M-07`.

### 1.2 · Error, escala declarada (A-bis 3)

`err_pp(corredor, celda) = 100 · (punto − R)`, **con signo**. Unidad: **puntos porcentuales de una proporción ponderada**. No es probabilidad de conducta, no es efecto, no es coeficiente: es la distancia de un corredor al patrón oro de su celda, dentro de una misma corrida. Comparable entre celdas del mismo marco porque **todas** las 14 son `escala = binaria` y su `R` es una proporción — verificado en §0.4, no supuesto.

### 1.3 · La guardia de universo (A-bis 4) — y por qué es el corazón de este acto

`agregado_v1_3.py` calcula `MAE_pp` de cada corredor sobre *«el universo de 14 **o el subconjunto con punto de corredor disponible**»*, **independientemente por corredor**. Es decir: `MAE_pp(L_SOLO)`, `MAE_pp(L_CORPUS)` y `MAE_pp(M)` **pueden estar calculados sobre conjuntos de celdas distintos**, y su comparación directa —que es la que produjo `19.60 / 11.69 / 4.51`— sería entonces una comparación entre universos distintos.

Este marcador, por tanto, emite **dos familias de `MAE_pp`**, y las distingue en el `id` del RESULT:

- `RESULT-C0D-MAE-MARGINAL-<corredor>` — cada corredor sobre **su propio** subconjunto disponible. **Reproduce D4 y sirve sólo para comparar contra él.**
- `RESULT-C0D-MAE-COMUN-<corredor>` — cada corredor sobre el **universo común** `U∩`: las celdas donde `R`, `L_SOLO`, `L_CORPUS` y `M` tienen los cuatro punto. **Ésta es la única que A-bis 4 autoriza a comparar entre corredores.**

Y emite el diagnóstico mecánico de si la distinción muerde: `RESULT-C0D-UNIVERSOS-IDENTICOS` (`SI`/`NO`) y el `n` de cada uno.

---

## 2 · La comparación primaria: la pareada `L_SOLO ↔ L_CORPUS`

**Universo:** `U_LL` = celdas con `R` computado **y** punto en `L_SOLO` **y** punto en `L_CORPUS`. Misma celda, misma escala, mismo `R`, misma ventana de captura, mismo modelo — **la única diferencia entre los dos números que se restan es si el corredor tenía el corpus delante** (§0.3).

**Diferencia por celda, con signo:**

```
d_i = |err_pp(L_CORPUS, i)|  −  |err_pp(L_SOLO, i)|
```

**`d_i > 0` significa que el corpus ALEJÓ a `L` del patrón oro en esa celda.** El signo se fija aquí, antes del dato, para que no haya lectura de conveniencia después.

**Estadístico:** media de `d_i` sobre `U_LL`, con IC95 por **bootstrap no paramétrico sobre celdas**, con la maquinaria **ya sellada** del duelo, consumida desde los bytes verificados por `sha256` de `forense/prereg-duelo-v2/scoring-adv1-m3.py` — `generar_indices_bootstrap`, `derivar_seed_scope`, `_cuantil_7` — y con los mismos parámetros sellados: **`seed = 42`**, **`replicas = 10000`**, **`nivel_ic = 0.95`**, `scope_id = "mae_pp::pareado::L_CORPUS_vs_L_SOLO::c0d_v1_0"`. Ni un parámetro se elige aquí: se citan.

---

## 3 · Comparaciones secundarias — se reportan como tales, no adjudican

Multiplicidad declarada al modo de `S6`: **la primaria decide; las secundarias se reportan y no mueven el veredicto.** Se calculan sobre `U∩` salvo donde se diga.

### 3.1 · `L_SOLO ↔ M` y `L_CORPUS ↔ M`

Mismo estadístico, `d_i = |err_pp(L, i)| − |err_pp(M, i)|`, con sus `scope_id` propios. Reproducen las dos pareadas que D4 sí hace — **sobre `U∩`**, que es donde son comparables entre sí.

### 3.2 · `M ↔ B`

Sólo sobre las 2 celdas de §0.2, brazo `PERSISTENCIA` como primario y `OPERATIVO` como secundario. **`n = 2`: se emite el par de errores crudo y NO un IC** — un bootstrap sobre dos celdas no es un intervalo, es un adorno. Se reporta `NO-ADJUDICA-POR-N`.

### 3.3 · La guardia de conmensurabilidad de `B` (A-bis 4)

`B` mide su propia observada de la ola (`RESULT-B-ENIGH-<ola>-P`, universo completo de `concentradohogar`). El duelo mide `R` de la misma ola con **su** universo y **su** estimador. Antes de usar `B` como piso, el marcador comprueba mecánicamente que las dos son la misma cantidad:

- Si `|RESULT-B-ENIGH-<ola>-P − R(celda)| ≤ 1.96 · EE_R(celda)` → `PISO-CONMENSURABLE`.
- Si no → **`PISO-NO-CONMENSURABLE`**: `B` se reporta con su cita y su cifra, **y no entra a ninguna comparación**. No se ajusta, no se re-escala, no se explica al vuelo.

### 3.4 · Control de convergencia — el marcador contra el agregado sellado

El medidor re-deriva los 28 puntos `L` (14 celdas × 2 brazos) **desde `L-extraido-v1_2.tsv`** con la regla de §1.1, y los compara contra los que `agregado-v1_3-resultado.json` ya selló. Emite `RESULT-C0D-CONTROL-CONVERGENCIA-L` = `CONVERGE` / `DIVERGE:<lista>` y `RESULT-C0D-CONTROL-MAXDIF-L`.

**`DIVERGE` no es un fallo del marcador: es el hallazgo de que el agregado vigente está desfasado de las capturas**, y en ese caso §5.4 manda. Se declara aquí porque *«convergencia entre dos lecturas corrobora la LECTURA, no el mecanismo»*: este control dice que estoy leyendo las mismas capturas que el duelo, y **nada más que eso**.

---

### 3.5 · Guardia de correspondencia TSV ↔ capturas (nueva en `v1.1`)

`RESULT-C0D-CONTROL-CORRESPONDENCIA` = `CORRESPONDE` / `DISCORDA:<detalle>`. Compara el conjunto de llaves `(id_celda, variante, indice)` del TSV contra el conjunto de archivos `corridas-L/L-<id>-M__<variante>__NN.json` declarados como input. **`DISCORDA` PARA la adjudicación por la misma vía que §5.4**, y por la misma razón: una lectura que no se apoya en las capturas que dice leer no adjudica nada.


---

## 4 · B-bis — las tres ramas de la pareada, escritas ANTES del dato

Sea `IC95(media d)` = `[lo, hi]` sobre `U_LL`, y `n_LL = |U_LL|`.

**Precedencia — se evalúa en este orden y la primera que aplica decide:**

| # | rama | condición mecánica | lectura |
|---|---|---|---|
| **0** | **`NO-ESTIMABLE-POR-COBERTURA`** | `n_LL < 10` | **No adjudica, cualquiera que sea el intervalo.** Una pareada sobre menos de 10 de las 14 celdas del marco no sostiene un veredicto sobre «el corpus»; se reporta el punto y se nombra sucesor. Esta guardia **precede a todas las demás** y existe porque una spec congelada puede salir degenerada por cobertura sin que nadie lo note. |
| **1** | **`CORPUS-ESTORBA`** | `lo > 0` | El corpus **aleja** a `L` del patrón oro, pareado y con el mismo universo. Es la rama que **CONFIRMA** el hallazgo del 8/sep. |
| **2** | **`CORPUS-AYUDA`** | `hi < 0` | El corpus **acerca** a `L` al patrón oro. Es la rama que refuta el hallazgo del 8/sep y sostiene D-2 en su lectura directa. |
| **3** | **`NO-DISCRIMINA`** | `lo ≤ 0 ≤ hi` | La pareada **no distingue** los dos brazos. El hallazgo del 8/sep no sobrevive como veredicto: era una diferencia entre marginales que la pareada no confirma. |

**Ninguna otra rama existe.** Si el cómputo produce algo que no cae en las cuatro (por ejemplo `U_LL` vacío), el veredicto es `NO-ESTIMABLE-POR-COBERTURA` por la rama 0, con `n_LL = 0` escrito.

**Y la lectura que NO se autoriza:** que `CORPUS-ESTORBA` signifique *«el corpus es malo»*. Este marcador mide **un modelo, una ventana de captura, 14 celdas, un corpus fechado**; A-bis 1–2 (asociación, no efecto) aplican íntegras. El enunciado máximo que la rama 1 autoriza es: *«con el corpus del 1–2/sep delante, este corredor se alejó más del patrón oro en estas 14 celdas»*.

---

## 5 · La adjudicación del hallazgo `corpus-empeora` — pre-declarada

El encargo pide que este acto convierta el hallazgo en veredicto **o lo explique**. Las ramas se fijan aquí, antes del dato.

**Precedencia — la primera que aplica decide:**

### 5.1 · `EXPLICADO-POR-UNIVERSO`
Si `RESULT-C0D-UNIVERSOS-IDENTICOS = NO` **y** el orden de los tres `MAE-COMUN` difiere del orden de los tres `MAE-MARGINAL`. Lectura: `19.60 / 11.69 / 4.51` comparaba corredores medidos sobre conjuntos de celdas distintos (A-bis 4); corregido el universo, la ordenación cambia. El hallazgo era un artefacto de universo.

### 5.2 · `EXPLICADO-POR-METRICA`
Si los universos son idénticos (o su corrección no cambia el orden) **pero** la pareada cae en `NO-DISCRIMINA`. Lectura: la diferencia entre marginales `MAE_pp` existe, pero **no sobrevive al pareo** — es decir, no es una diferencia por celda sino la sombra de unas pocas celdas con error grande. Se nombra cuáles (`RESULT-C0D-CELDAS-DOMINANTES`: las de mayor `|d_i|`).

### 5.3 · `CONFIRMADO-CON-ALCANCE`
Si la pareada cae en `CORPUS-ESTORBA`. **El alcance es obligatorio y ya está escrito** (§0.3): *el corpus del 1–2 de septiembre de 2026*, un modelo (`claude-opus-4-6`), `k = 8`, temperatura 1.0, 14 celdas del marco `v1_3`. `RESULT-C0D-ALCANCE-PAYLOADS-POSTERIORES` cuantifica cuánto corpus entró después. **Sea cual sea ese número, el sucesor se nombra igual** —re-captura `L_CORPUS` con corpus GEN2, fase 5 del plan de dirección— y **no se ejecuta aquí**; el número sólo gradúa la urgencia, no la existencia del sucesor.

### 5.4 · `NO-ADJUDICA-POR-CONTROL`
Si `RESULT-C0D-CONTROL-CONVERGENCIA-L = DIVERGE`. Entonces el agregado vigente y las capturas no dicen lo mismo, y **eso** es el hallazgo que se reporta primero: adjudicar sobre una lectura desfasada sería adjudicar sobre nada. Precede a 5.1–5.3 en la escritura de la nota **aunque se evalúe al final**, porque invalida el insumo de todas.

### 5.5 · `NO-ESTIMABLE-POR-COBERTURA`
Rama 0 de §4.

---

## 6 · Lo que el marcador emite

Todo `RESULT` con `tipo`, `unidad` y escala declarada, según `data/corrida0/CALC-C0D-MARCADOR/spec.yaml`, que es la cara mecánica de este documento. Las familias:

1. **Por celda** (14 × 6): `R`, `EE_R`, `err_pp` de los tres corredores, y `d_i` de la pareada.
2. **`MAE_pp`** marginal y común, por corredor, con su `n` y su IC95.
3. **Las tres pareadas** (`punto`, `ic_lo`, `ic_hi`, `n`): la primaria `L_CORPUS ↔ L_SOLO` y las dos secundarias contra `M`.
4. **`B`**: cita, cifra, conmensurabilidad y error, en las 2 celdas de §0.2.
5. **Veredictos**: `RESULT-C0D-VEREDICTO-PAREADA` (§4) y `RESULT-C0D-ADJUDICACION-HALLAZGO` (§5).
6. **Controles y alcance**: convergencia, universos, payloads posteriores.

---

## 7 · Lo que esta spec explícitamente NO autoriza

- No autoriza re-capturar `L` con otro corpus: eso es el sucesor de §5.3.
- No autoriza tocar la banda `z` primaria del duelo ni `agregado_v1_*.py`.
- No autoriza mover ninguna regla, `tier`, `p` ni veredicto del motor (`T9`).
- No autoriza extender `B` fuera de la serie ENIGH·remesas (§0.2).
- No autoriza incorporar las 15 celdas del piloto, que no tienen brazo `L+corpus` (§0.4).
- No autoriza aflojar `tolerancia.abs` para que una adopción pase (precedente `PRIMERA-SILLA` §1: para eso existe `tolerancia_adopcion`).

---

## 8 · Sello

**Parámetros congelados:** `seed = 42` · `replicas = 10000` · `nivel_ic = 0.95` · `n_minimo_pareada = 10` · `k_umbral_conmensurabilidad = 1.96` · `tolerancia_convergencia_L = 1e-9` · `n_filas_l_tsv = 224`.

**Frase de sello, verbatim:** *el primer resultado que produzca este procedimiento es el que se reporta.*
