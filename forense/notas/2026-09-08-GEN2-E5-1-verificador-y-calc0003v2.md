# `ACTO GEN2-E5-1` · verificador reparado + `CALC-0003-v2` + la firma del contador

**Acto:** `ACTO GEN2-E5-1 · VERIFICADOR REPARADO + CALC-0003-v2 + LA FIRMA DEL
CONTADOR`, lote D-11, 8/sep/2026 · **UBUNTU (caja)**, corpus montado · **Opus**
· worktree nuevo desde `origin/main`.

**Compuerta, verificada por PRODUCTO y no por rótulo.** El encargo se redactó
contra la rama de `PR #631` (`e441ea84`) y `main` se movió **durante el
ARRANQUE**: la primera comprobación dio `origin/main = e36c66d` (PR #630) y los
dos sellos **ausentes**; la re-derivada, tras `git fetch --prune`, dio
`origin/main = d48014e` (`Merge pull request #631`). Comandos y salida cruda:

```
$ git cat-file -e origin/main:data/corrida0/CALC-0001/sello.json   -> EXISTE
$ git cat-file -e origin/main:data/corrida0/CALC-0002/sello.json   -> EXISTE
$ git merge-base --is-ancestor e441ea84 origin/main                -> SI-ancestro
```

---

## 1 · `P1` — los dos arreglos del verificador

### (a) `FP-353` · `_evalua_contexto` comparaba llaves de distinto tipo

`spec.yaml` viene del YAML, que conserva `29` como `int`; `ejecucion.json` pasó
por JSON, que convirtió esa misma llave en `'29'`. Aislado antes de tocar nada:

```
llaves con TIPO distinto spec vs ejecucion (CALC-0001): 12
  /crosswalk_partido/1 … /crosswalk_partido/12   spec=int  ejecucion=str
  /coaliciones/29                                spec=int  ejecucion=str
```

`_canoniza_llaves` canoniza **ambos lados** a la forma que sobrevive el viaje
por JSON: llaves a cadena, recursivo, y el mapping como **lista ordenada de
pares** —no como `dict`— para que dos llaves que colapsan a la misma cadena
(`{1: 'a', '1': 'b'}`) sigan siendo dos. Colapsarlas afirmaría una igualdad que
no se comprobó, que es el mismo defecto al revés.

### (b) `FP-354` · `_compara_result` no tenía rama para `None`

`None` es un valor que la propia spec **autoriza** (`permite_no_estimable:
true`), que `_valida_outputs` respeta y que `run` sella. Las dos funciones
implementaban contratos **contradictorios** sobre el mismo valor. Ahora: los dos
`None` con autorización → `REPRODUCE`; `None` contra valor → `NO-REPRODUCE` con
mensaje propio; los dos `None` **sin** autorización siguen sin reproducir.

### Falsadores, con su control positivo

Un falsador que sólo pasa después del arreglo no prueba nada si nunca se le vio
fallar. Los dos se corrieron contra el `tools/corrida0.py` de `HEAD`:

| falsador | contra el código SIN arreglar | con el arreglo |
|---|---|---|
| `T-VERIFY-CONTEXTO-LLAVES` | **2 asertos fallan** (`{29:[2,9]}` vs `{'29':[2,9]}` dio `DISTINTO`) | pasa |
| `T-VERIFY-NO-ESTIMABLE` | **5 asertos fallan** (`None`/`None` no reprodujo) | pasa |

`tests/test_corrida0.py`: **61 casos · 61 ok · 0 FALLOS**.

### La tabla nueva de `verify` — los sellos v1 **no se tocaron** (E.3)

| CALC | antes | después | `parametros` |
|---|---|---|---|
| `CALC-0001` | 32 `REPRODUCE` / **22** `NO-REPRODUCE` | **54 / 0** | `DISTINTO` → `IDENTICO` |
| `CALC-0002` | 25 `REPRODUCE` / **4** `NO-REPRODUCE` | **29 / 0** | `IDENTICO` (control positivo de `FP-353`) |

**83 de 83 `RESULT` GEN2 sellados reproducen.** Los 26 `NO-REPRODUCE` eran
exactamente los dos defectos —`sellado == hoy` en los 26—, no divergencias
numéricas. 83 cifras pasan de «selladas con etiqueta falsa» a «selladas y
reproducidas».

### Lo que NO llegó, y no se forzó · `FP-358` (nueva)

El encargo esperaba `CALC-0002 → REPRODUCE · IDENTICO`. **No llega**, y la
causa es **distinta de las dos diagnosticadas**: queda `commit_distinto`.
`_evalua_contexto` compara `git rev-parse HEAD` de hoy contra el
`ejecucion.json.git_commit` en que la corrida se selló.

**Control positivo, sobre `CALC-0003-v2` y sin que un byte del CALC cambiara:**

```
en el commit del sello:      CONTEXTO: IDENTICO   VERIFY: REPRODUCE
un commit después (COMMIT-2, que el protocolo OBLIGA a hacer):
                             CONTEXTO: DISTINTO  razon: commit_distinto
                             VERIFY: REPLICA-RESULTADO · CONTEXTO-DISTINTO
   …con los mismos 128/128 RESULT reproduciendo y el sello COINCIDE.
```

**Alcance, medido en el árbol: 12 de 12 corridas selladas** tienen
`git_commit != HEAD` de hoy. Ninguna puede dar `REPRODUCE`. No es la misma
causa que `FP-353` —aquélla era una comparación mal hecha; ésta es una
comparación bien hecha de una cosa que cambia por diseño—, y **no se arregla
aquí**: el perímetro sólo abre `_evalua_contexto` para `FP-353`, y la decisión
es de diseño (¿debe la identidad del commit gatear `CONTEXTO`, o ser un eje
propio junto al sello y al script, que sí son estables y sí salieron
`IDENTICO` en los tres CALC?).

---

## 2 · `P2` — `CALC-0003-v2` SELLADA

`repite_de: CALC-0003`. `CALC-0003` queda **`SUPERADO→CALC-0003-v2`** en el
registro; sus bytes, **intactos**. El PARO de v1 no se reabre: se supera.

### La premisa del encargo no se reprodujo, y se corrigió contra el archivo

El encargo y `FP-355` piden filtrar «3 filas **totalmente vacías**» de
`c_portad.dta`. Medido en el archivo crudo, **antes** de escribir la spec:

```
c_portad.dta filas totales: 8441   columnas: 11
filas COMPLETAMENTE vacias (las 11 columnas NaN):        0
filas con folio, ls y estrato NaN:                       3   (indices 7321, 7567, 8189)
```

Las 3 traen **8 de sus 11 columnas con dato** (`rel`, `reh`, `edo`, `mpio`,
`loc`, `control`, `edad`, `id_loc`). **Implementar el filtro por el rótulo
«vacía» habría descartado cero filas y `CALC-0003-v2` habría vuelto a parar
igual que v1.** Se filtra por la **llave de join ausente**, que es lo que
rompe el merge: `_llave` la vuelve `<NA>`, `duplicated` cuenta `NA == NA` como
repetido y `validate="m:1"` levanta.

**Universo declarado: nada alcanzable cambia.** Una fila sin `folio`/`ls` no
puede casar con ninguna fila real de ningún miembro; el join ya la descartaba
por construcción, sólo que levantando en vez de omitiendo. Medido: `c_portad`
**8441 → 8438** filas, **2 → 0** llaves duplicadas.

### Guardia marginal antes de correr — las **seis** tablas, no las tres

`FP-355` observó que la guardia del medidor cubre 3 de las 6 tablas que el
código usa como lado derecho de un `m:1`. Se midieron las seis:

| tabla | filas | llave ausente | dup. antes | dup. después |
|---|---|---|---|---|
| `c_portad` | 8 441 | **3** | **2** | 0 |
| `w_b3b` | 35 677 | 0 | 0 | 0 |
| `w_bx` | 35 677 | 0 | 0 | 0 |
| `iiib_es` | 19 804 | 0 | 0 | 0 |
| `p_es` | 1 848 | 0 | 0 | 0 |
| `iiib_ec` | 17 728 | 0 | 0 | 0 |

Sólo `c_portad`. No había una segunda sorpresa esperando en el siguiente merge.

### Resultado

`PRE-FLIGHT: VERDE` → `run` → `SELLADO` → `VERIFY: REPRODUCE`
(`CONTEXTO=IDENTICO · RESULTADO=REPRODUCE`), **128/128**. `+128 RESULT`, con
los **mismos ids** que v1: el conteo A.13 viaja dentro de
`RESULT-LLAVE-UNICA-PORTAD`, que la spec ya declaraba.

```
RESULT-LLAVE-UNICA-PORTAD = UNICA · A.13 c_portad.dta: 8441 filas leidas ·
                            3 filtradas por llave (folio/ls) ausente · 8438 al join
```

Las 3 filtradas son exactamente las 3 previstas.

| celda · brazo | delta | IC | veredicto |
|---|---|---|---|
| `C1-B3B-FAC3B` | −0.065961 | [−0.148043, +0.020537] | `NO-DISCRIMINA` |
| `C1-BX-FAC3APX` | +0.000790 | [−0.036578, +0.022008] | `NO-DISCRIMINA` |
| `C1-BX-FAC3BPX` | +0.000148 | [−0.037034, +0.021274] | `NO-DISCRIMINA` |
| `C2-B3B-FAC3B` | +0.032666 | [−0.003639, +0.069743] | `NO-DISCRIMINA` |
| `C2-BX-FAC3APX` | −0.026564 | [−0.088181, +0.032465] | `NO-DISCRIMINA` |
| `C2-BX-FAC3BPX` | −0.027617 | [−0.089011, +0.031167] | `NO-DISCRIMINA` |
| `C3-B3B-FAC3B` | **+0.181865** | **[+0.090029, +0.281877]** | **`CORROBORADA`** |
| `C4-B3B-FAC3B` | **+0.067035** | **[+0.027643, +0.104595]** | **`CORROBORADA`** |

**Brazo `bx` con su regla de coincidencia de signo intacta:** `C1-BX` y `C2-BX`
→ `COINCIDEN-EN-SIGNO`. Ningún `RESULT` salió `NO-ESTIMABLE` (0 de 128).

`R4.4 / salud.atencion.grave` **no se mueve por este CALC** (etiqueta de la
propia spec): esto es el falsador de `S6 v1.2` Rama A′, no una adopción.

---

## 3 · `P3` — la cláusula imposible, reescrita (`NC-0047` cierra)

Texto vigente desde este acto:

> «sin árboles ni ramas fuera de política **propios de este acto**; lo ajeno se
> reporta con conteo y no bloquea».

Firma de mesa del mensaje de lanzamiento, verbatim:

> «El reporte nunca sale vacío por diseño (siempre imprime el worktree en
> curso): la cláusula vieja era literalmente incumplible y ya costó dos
> desviaciones declaradas.»

**Control positivo de que era incumplible**, medido en este mismo worktree:

```
A · worktrees vivos: 12          <- uno es el worktree del acto que evalúa la compuerta
D · fuera_de_politica: 1
      acto/gen2-e5-1-verificador-calc0003v2   <- la rama del PROPIO acto,
                                                 contada así sólo porque su PR
                                                 aún no existía al comprobar
```

El acto se descalificaba a sí mismo por existir. Reescrita en los dos encargos
de cola que la traían como compuerta (`GEN2-E5-0`, `GEN2-E5`), con la firma
citada verbatim al pie de cada uno.

**Reserva declarada (`NC-0050`):** la **versión maestra**
`forense/notas/ENCARGOS-GEN2-v1_5-aparato-antes-de-calcular-2026-09-08.md`
sigue trayendo el texto viejo en sus líneas 45 y 58, y está **fuera del
perímetro** de este acto. `tools/verifica_encargos_gen2.py --aplica` copia el
cuerpo maestro sobre el de cola: si un encargo GEN2 se reactiva, **revertiría
esta reescritura en silencio**. Hoy no ocurre (`--verifica` →
`SIN-ENCARGOS-GEN2-ACTIVOS`, exit 0), pero es una trampa armada.

---

## 4 · `P4` — la firma del contador: **no viajó** en el lanzamiento

El mensaje de mesa **no trae la firma**. La cadena `cuenta_gen2 = SI` aparece
**una sola vez** en el encargo, y dentro de la propia condición que la pide
(«Si el mensaje de mesa trae la firma verbatim de…»): mencionar una firma no es
firmarla, y no hay autoridad, fecha ni objeto citados, a diferencia de las
filas ya existentes de `decisiones.tsv` (`fuente = D-1 (mesa 2026-09-08, ACTO
GEN2-T9)`).

**`P4` no escribió nada.** `data/corrida0/decisiones.tsv` queda intacto y los
contadores se quedan **honestamente en cero**.

**Control positivo, con la firma SIMULADA en memoria** (`decisiones.tsv`
restaurado byte a byte y verificado):

| contador | hoy | con la firma |
|---|---|---|
| `N_corridas_selladas` | 0 | **3** |
| `N_resultados_sellados` | 0 | **211** |
| `N_resultados_gen2_sellados` | 0 | **211** |
| `N_resultados_gen2_pendientes_adopcion` | 0 | **5** |

### El control positivo mordió — `FP-359` (nueva)

El procedimiento que `ADR-410` recomienda —«simula la firma **en memoria**, sin
escribir nada»— **sí escribe**. `status` no se puede leer sin pasar por
`registro()`, y `registro()` escribe `corridas.tsv`, `resultados.tsv` y
`usos.tsv` como efecto colateral. Restaurar `decisiones.tsv` —que es lo que el
procedimiento dice, y lo que hice, y verifiqué byte a byte— **no basta**: el
archivo que se restaura no es el que quedó contaminado.

Resultado real, en este acto: el commit de cascada `d598210` salió con las tres
corridas GEN2 marcadas `cuenta_gen2 = SI`, motivo «FIRMA SIMULADA» — publicando
una firma que mesa no dio, que es exactamente lo que `P4` existe para no hacer.
Se detectó porque `git status` mostró `corridas.tsv` y `resultados.tsv`
modificados **después** del `COMMIT-2` que ya los había sellado, y no había
razón para que cambiaran. Corregido hacia adelante en `COMMIT-3` (`a8793a7`),
verificado por tres vías: `cuenta_gen2` de los cuatro CALC de vuelta en
`PENDIENTE-DE-MESA`; `grep -rlI "FIRMA SIMULADA"` sobre `data/ forense/ canon/`
→ **0** archivos; `git diff eeceb25 -- data/corrida0/*.tsv` → **0 líneas**,
idéntico byte a byte al `COMMIT-2`.

**Alcance:** `origin/main` está **limpio** — `GEN2-E5` corrió la misma
simulación y no la publicó. No es un defecto heredado: es una trampa que se
arma al repetir un procedimiento recomendado, y que ni `ADR-410` ni la nota de
`GEN2-E5` advierten.

Lo que falta firmar son **tres** filas: `CALC-0001`, `CALC-0002` y
`CALC-0003-v2` con `cuenta_gen2 = SI`. `FP-356` sigue **ABIERTA**;
`NC-0045`/`NC-0046` siguen **ABIERTAS**, y `T35` sigue sin ejercerse sobre
cadena GEN2 real por la misma razón.

---

## 5 · `P5` — `delta` GEN2↔GEN1: **no se pudo correr, y la respuesta es `SIN-BASE-COMPARABLE`**

Pregunta de mesa, verbatim del 8/sep: «**¿Esto quiere decir que las de gen2
coinciden con Gen 1?**»

**No se puede decir que coincidan ni que difieran.** Dos razones mecánicas,
verificadas por separado:

**(i) El script no existe.** `corrida0 delta` es un subcomando **declarado y
vacío**:

```
$ python3 tools/corrida0.py delta
NO-IMPLEMENTADO: `corrida0 delta` se declara aqui y lo llena ACTO GEN2-E3 …
EXIT=2
```

Implementarlo está **fuera del perímetro** (`tools/corrida0.py` sólo abierto
para `_evalua_contexto` y `_compara_result`). Y hacer la comparación **a mano**
sería exactamente lo que `E.1` prohíbe: la diferencia se calcula por script,
después de medir.

**(ii) Aunque existiera, no tendría con qué.** Los insumos que un `delta`
necesitaría **no están declarados**:

- Los **211** `RESULT` GEN2 sellados salen del registro con `valor_legacy =
  NO-COMPARABLE` y `delta_legacy = NO-COMPARABLE` — pero eso **no es un
  hallazgo medido**: `tools/corrida0.py:2963` los escribe como **constante**
  para todo el lado OFERTA. El registro está declarando que **no lo calcula**,
  no que no haya contraparte. No se lee como medición.
- La columna que **sí** emparejaría un consumidor GEN1 con un `RESULT` de
  `corrida0` es `usos.corrida0_resultado_id`, y se deriva de las marcas reales
  de `milpa/`. Medido sobre **205 usos** (A.13): **0** la traen poblada.
  **Control positivo: también vacío** — no es que los GEN2 no estén citados y
  los GEN1 sí; es que **ningún consumidor cita ningún `RESULT` de `corrida0`**,
  de ninguna generación. Un negativo cuyo control positivo también sale vacío
  no es un negativo: es una columna sin poblar.

**Veredicto honesto: `SIN-BASE-COMPARABLE` para los 211.** No se inventa el
cruce. **Diferencias materiales listadas aparte: ninguna, y no porque no las
haya — porque no son computables hoy.**

**Ésta es la cosecha de `P5`**, y es un requisito, no un número: antes de que la
pregunta de mesa tenga respuesta hace falta (1) que `delta` se implemente
—`B-7`, asignado a otro acto— y (2) que **alguien declare el emparejamiento**,
escribiendo `corrida0_resultado_id` en los consumidores de `milpa/` que hoy
leen cifras GEN1. Sin (2), `delta` correría sobre el vacío y devolvería «cero
diferencias» — que es la forma en que este aparato ya se equivocó antes.

---

## 6 · Contador del programa

**Medición: sí.** `CALC-0003-v2` es corrida sellada nueva con cadena completa
(`preflight → run → sello → verify REPRODUCE`), **+128 `RESULT`**. `P1`
convierte **83** cifras ya selladas de «con etiqueta falsa» a «selladas y
reproducidas». **211** `RESULT` GEN2 sellados en total.

**Los contadores publicados siguen en cero**, y es correcto que sigan: falta la
firma de mesa (`FP-356`). Nada se adopta al motor — la adopción sigue siendo
humana (`E.2`).
