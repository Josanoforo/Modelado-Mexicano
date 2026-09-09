# `CALC-0003-v4` — cara local de `prereg-caja-S6-L16` **v1.3** (ENNViH-1 2002)

**Acto:** `ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1`, 8/sep/2026,
**UBUNTU (caja)**, sobre `origin/main = c5b89a9`. **Tercer commit del mismo
acto** — el que congela el reemplazo cuando la corrida anterior salió con un
defecto: `CALC-0003-v3` **no se edita, no se retira y no se re-corre**; sus
bytes y su sello quedan intactos y su `resultados.json` es el registro de lo
que efectivamente pasó. Cadena completa:

`CALC-0003` (PARO, `MergeError`, `FP-355`) → `CALC-0003-v2` (SELLADA) →
`CALC-0003-v3` (SELLADA; su guardia nueva mordió) → **`CALC-0003-v4`** (esta).

---

## 0 · 🛑 La ÚNICA diferencia operativa con `CALC-0003-v3`

> Los atributos de diseño (`estrato`, `id_loc`) se toman de `c_portad.dta` por
> la llave de **HOGAR** (`folio`), no por la de **PERSONA** (`folio`, `ls`).

Todo lo demás es byte por byte el de `v3` —que a su vez es el de `v2` salvo el
conglomerado—: universo, disparadores, desenlaces, las tres tablas, `P_PUB` y
su sensibilidad, `seed` (`20260908`), réplicas (`2000`), umbral `n < 10`,
pareja de ponderadores, tolerancia. **143 `RESULT`**: los 142 de `v3` con sus
mismos ids, más `RESULT-COBERTURA-DISENO`.

### 0.1 · Por qué — el defecto que `v3` publicó y este `CALC` repara

`CALC-0003-v3` introdujo, junto con el conglomerado localidad de
`S6 v1.3 §3.5`, la guardia `RESULT-<fila>-N-SIN-CONGLOMERADO`. **Mordió:**

| fila | sin conglomerado | de |
|---|---|---|
| `C1-B3B` | **182** | 342 |
| `C1-BX` | **87** | 93 |
| `C2-B3B` | **1 655** | 3 179 |
| `C2-BX` | **220** | 233 |
| `C3-B3B` | **160** | 301 |
| `C4-B3B` | **1 473** | 2 825 |

**La causa, medida y no supuesta.** `c_portad.dta` es **una fila por hogar**:
**8 437** folios distintos en **8 438** filas con llave, y su `ls` identifica al
**respondente de la portada** (10 valores distintos, moda `1` y `2`), no a cada
persona del hogar. El join por `(folio, ls)` —que `v1`, `v2` y `v3` heredaron
sin que ninguna spec lo declarara— resuelve **7 870 de 19 804** personas de
`iiib_es`. El join por `folio` resuelve **8 057 de 8 060** hogares, es decir
**~100 %** de las personas (`iiib_es` 19 799/19 804 · `iiib_ec` 17 723/17 728 ·
`iiib_hs` 19 794/19 799 · `iiib_ce` 19 798/19 803 · `p_es`/`p_hs`/`p_ce`
1 847/1 848 cada uno).

**Por qué `v2` no lo notó y `v3` sí.** En `v2` el conglomerado era el hogar:
una fila huérfana de `c_portad` conservaba su propio `folio` y seguía siendo su
propio conglomerado — el daño era un pseudo-estrato `NaN`, invisible y casi
inocuo. En `v3` el conglomerado es la localidad: **todas** las huérfanas caen en
**un solo** conglomerado `NaN`, que el remuestreo dentro de ese pseudo-estrato
toma **siempre entero**, sin variabilidad. Eso **estrecha** el IC. Es
exactamente lo contrario de la dirección que `CALC-0003-v3/spec.md` §0 declaró
esperar antes de correr —«conglomerados más grandes ⇒ intervalos más anchos»—
y por eso el estrechamiento observado en `v3` **no se leyó como hallazgo**.

**La corrección no elige nada.** `estrato` e `id_loc` son atributos **del
hogar**, y se verificó que son **constantes dentro de `folio`**: cero folios con
más de un `estrato` y cero con más de un `id_loc`. Tomarlos por `folio` es leer
el mismo atributo por la llave a la que pertenece, no sustituir un criterio por
otro. La deduplicación (8 438 filas con llave → 8 437 hogares) descarta **una**
fila, la segunda del único folio repetido (`8486000`, `ls` 1 y 7), cuyas dos
filas traen `edo`/`mpio`/`loc`/`estrato`/`id_loc` **idénticos**.

**Guardia que PARA de disimular, publicada como `RESULT`.**
`RESULT-COBERTURA-DISENO` emite filas con llave, hogares únicos, filas de más
por folio repetido, y **cuántos folios traen más de un `estrato` o más de un
`id_loc`**. Si alguno lo hiciera, el resultado dice `DEDUP-NO-LOSSLESS` y **no
se elige un valor**: el hogar no determinaría el atributo y eso sería un
hallazgo sobre el archivo, no un detalle de implementación.

### 0.2 · Lo que este `CALC` NO reclama

**No corrige `S6 v1.3`.** La spec sellada **no especifica la llave** del join
contra `c_portad`: su §3.4 tabula cinco joins y **ninguno es contra
`c_portad`**, pese a que §3.5 toma de ahí `estrato` y (en `v1.3`) `id_loc`. El
hueco es del pre-registro y se eleva a mesa como firma pendiente — **no se
parcha editando una spec sellada** (E.3).

**No reabre `CALC-0003-v2` ni `CALC-0003-v3`.** Sus bytes quedan intactos. Que
`v2` tuviera la misma cobertura parcial de `estrato` es un hecho que esta pieza
**mide y declara**, no una invalidación que esta pieza pronuncie: el efecto de
un pseudo-estrato `NaN` sobre su IC es materia de mesa, y `v2` publicó su `Δ`
puntual, que **no cambia**.

**No cambia el estimando, el universo ni el ponderador.** Sigue siendo un
cambio de estimador de varianza — ahora, además, uno bien alimentado.

---

## 1 · Control de regresión — la guardia que distingue «se arregló» de «se movió otra cosa»

Por construcción de §0, **todo lo que no sea `IC-LO` / `IC-HI` / `VEREDICTO` ni
uno de los cinco textos que describen el propio join debe reproducir idéntico a
`CALC-0003-v3` y a `CALC-0003-v2`**: los ocho `DELTA`, los ocho `DELTA-SENS`,
las dieciséis `P-T1`/`P-T0`, las `N-T1`/`N-T0`, los `N-UNIVERSO`, los cuatro
niveles de `LUGAR` por fila, los `N-PONDERADOR-VALIDO`, `RESULT-JOINS`,
`RESULT-LLAVE-UNICA-W_B3B`/`W_BX`, `RESULT-DHS-N-EPISODIOS-*`,
`RESULT-T2-N-VARIABLES`, `RESULT-VENTANAS` y `RESULT-CODIGOS-SI-NO`.

**Los que sí cambian, y por qué, dicho antes de correr:**
`RESULT-LLAVE-UNICA-PORTAD` (mide unicidad por `folio` y no por `(folio, ls)`),
`RESULT-CONGLOMERADO-LOCALIDAD` y `RESULT-CONGLOMERADO-ANIDAMIENTO` (se
calculan sobre la tabla de hogares), los seis `RESULT-<fila>-N-CONGLOMERADOS`
(deben **subir**) y los seis `RESULT-<fila>-N-SIN-CONGLOMERADO` (deben **bajar
a cerca de 0**; si alguno no baja, la reparación no funcionó y se reporta como
tal). Y `RESULT-COBERTURA-DISENO`, que es nuevo.

**Un `DELTA` que se moviera sería prueba de que la reparación arrastró algo que
no debía, y se reporta como defecto, no como resultado.**

---

## 2 · La pre-declaración `B-bis` sigue siendo la de `v3` §5, sin reescribir

Se aplica **a esta corrida**, que es la que tiene el conglomerado bien
alimentado, y su texto **no se toca**: fue congelado en el `COMMIT-1` de este
acto, antes de abrir un solo `.dta` para calcular, y reescribirlo ahora —
después de haber visto los IC de `v3`— sería exactamente lo que el patrón de
dos commits existe para impedir. Se cita, verbatim, y se aplica:

1. **Si `C1`/`b3b` —primaria, `NO-DISCRIMINA` en `v2` y en `v3`— CAMBIA DE
   ESTADO en cualquier dirección, ESO es EL hallazgo y se reporta PRIMERO**,
   con la advertencia de que un cambio de estado producido por un cambio de
   varianza no es evidencia nueva sobre la conducta.
2. **Si `C3` y/o `C4` conservan su intervalo por encima del umbral, su
   corroboración es SECUNDARIA ROBUSTA.**
3. **Si el IC95 de `C3` o de `C4` cruza 0, esa fila BAJA a `PROPUESTA` y se
   dice** — sin rescatarla, sin bajar el umbral, sin apelar a la sensibilidad.

**Y la advertencia que ninguna de las tres deroga:** el veredicto de la regla lo
decide `C1`/`b3b` (`S6` §2.5); `C3`/`C4` corren sobre `T2`, que `S6` §1 declara
aproximación de «crónico», no de «crónico complejo»; las cuatro celdas miden
co-ocurrencia y no secuencia (`S6` §3.6); y **`R4.4` no se mueve por este
`CALC`**.

---

## 3 · Qué NO hace

No edita `S6-L16-spec-v1_3.md` ni ninguna spec sellada. No edita ni re-corre
`CALC-0003`, `CALC-0003-v2` ni `CALC-0003-v3`. No reclasifica instituciones. No
adjudica el ponderador del `bx`. No cambia universo, estimando, `seed`,
réplicas ni umbral. No usa `loc` a secas ni `control`. No mueve el tier de
`R4.4`. No corre 2005/2009 ni `ENDIREH`. No re-corre `CALC-0001` ni
`CALC-0002`. No sostiene ninguna afirmación causal.

**El primer resultado que produzca este procedimiento es el que se reporta — de
cada celda y de cada brazo, por separado.**
