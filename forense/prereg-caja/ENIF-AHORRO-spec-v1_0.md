# ENIF-AHORRO · Pre-registro del horizonte de ahorro, la vía formal/informal y la desconfianza en protección de depósitos, ENIF 2024

### `prereg-caja-ENIF-AHORRO` · **v1.0** · 9 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-ENIF-1` · CAJA (Ubuntu/WSL2) · base `origin/main = 0f62668`
**Encargo:** `forense/encargos/2026-09-09-GEN2-LOTE-ENIF-1.md` (A.3, verbatim)
**Releva:** `CORR-0009` (ENIF2024) → los **8** `RESULT` que el encargo nombra: `RES-0046`…`RES-0049`, `RES-0057`…`RES-0060`
**Corrida:** `data/corrida0/CALC-ENIF-0001/`

> **CONGELADA EN EL COMMIT-1, ANTES DE ABRIR UN SOLO `*.csv` DEL MICRODATO.**
> Lo único abierto al escribirla: `data/manifiesto.yaml`, el descriptor
> `enif_2024_fd.xlsx`, el cuestionario `enif_2024_cuestionario.pdf`, la lista
> de miembros del ZIP (nombres y tamaños, no contenido), `milpa/tramite.yaml`
> y `data/corrida0/demanda-*.tsv`. **Ningún microdato.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Las premisas del encargo que NO se sostienen (ninguna bloquea)

| # | el encargo dice | el árbol / el codebook dice | consecuencia |
|---|---|---|---|
| P1 | «la plaza: **`CORR-0017`**» | `CORR-0017` es `S7-L17` (ENSANUT, vacunación), **2** `RESULT` (`RES-0063`, `RES-0064`), `entorno_requerido = INDECIDIBLE-SIN-PAYLOAD-DECLARADO`. La plaza ENIF2024 es **`CORR-0009`**: 10 `RESULT`, payload `enif_2024_enif_2024_bd_csv`, `entorno = CAJA` | **rótulo corregido**. Los 8 `RESULT` que el encargo nombra por `id` existen, todos en `CORR-0009`, todos con ese payload. Se obedece la **identidad** (los 8 `id`), no el rótulo de corrida |
| P2 | «¿adultos **18-70**?» | `EDAD_V` = **`18 - 95`** (+`97` = 97 y más, `98` = no especificada). El cuestionario rotula el bloque **«PARA PERSONAS DE 18 AÑOS Y MÁS»** | población = **18 y más**. El «18 a 70» que arrastra la `escala_legacy` de `RES-0059`/`RES-0060` es de una ola anterior; **esta corrida no lo hereda** |
| P3 | «el filtro de conocimiento de protección de depósitos **ANTES** de la pregunta de desconfianza» | El flujo es el **inverso**: `5.20` (razón de no tener cuenta) → **`PASE A 5.23`** → `5.23` (conocimiento de la protección). `5.23` va **después** | la premisa se invierte. Ver `3.5` — se escribe como **guardia que PARA**, no como supuesto |
| P4 | «el denominador de esa tasa es **solo quienes conocen**» | Los dos `RESULT` sellados son un **par de celdas** (`…_conoce_proteccion_enif2024` y `…_no_conoce_enif2024`): el eje **parte** el denominador, no lo recorta. Y `P5_23` **no trae código `b`** — se le pregunta a **todo el mundo**, no solo a quien tiene cuenta | denominador = **personas sin cuenta**, partido en dos por `P5_23`. Ver `3.4` |

Ninguna de las cuatro para el acto: las tres primeras se corrigen y se
declaran; la cuarta cambia el denominador y por eso se escribe explícito.

### 0.2 · Cobertura retroactiva — `FP-201` y `NC-0086`

`FP-201` declaró «sin campo de diseño UPM/estrato reproducible» para las cinco
fuentes de fase 1. Para ENVIPE resultó falso (hallazgo 3.3 del lote ENVIPE) y
`NC-0086` dejó **ENIF en la lista de re-examen**. Re-examinado aquí, contra el
descriptor:

| variable | hoja | tipo | tamaño | códigos válidos | veredicto |
|---|---|---|---|---|---|
| `EST_DIS` | `TMODULO` | Alfanumérico | 3 | `001 - 190` | **EXISTE** |
| `UPM_DIS` | `TMODULO` | Alfanumérico | 5 | `00001 - 02172` | **EXISTE** |
| `FAC_PER` | `TMODULO` | Numérico | 6 | `126 - 106896` | **EXISTE** |

→ **`FP-201` es FALSO también para ENIF 2024.** Las tres están en el bloque
`VARIABLES DE DISEÑO ESTADÍSTICO` de `TMODULO` (filas 1478-1483 del FD), y las
tres se usan en esta corrida.

⚠️ **`EST_DIS`/`UPM_DIS` son llaves opacas** y el descriptor sólo declara su
rango, no su semántica. Se usan **como llaves de conglomerado**, nunca como
cantidad. La guardia de `3.7` lo verifica contra el archivo.

⚠️ **A-bis.3.** Fase 1 midió **sin** diseño; esta corrida **sí** lo estima. Los
IC **no son comparables y no se comparan**. El control positivo de `5.1`
compara **sólo el punto**.

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Se declara, sin adorno, todo lo que esta sesión vio de GEN1 **antes** de
congelar:

1. Dirección pegó en el encargo tres valores GEN1: `0.3306`/`0.6694`
   (`RES-0046`/`RES-0047`) y `0.284927` (`RES-0057`).
2. Verificar la premisa `P1` (§0.1) obligó a leer `demanda-resultados.tsv`,
   que trae **los 8 valores GEN1** y sus `clase_legacy`.
3. Esa lectura expuso la cadena `«condicional a formalidad; P4_10='1',
   universo restringido A-bis 4, cobertura 66.89%»`. **Es decir: se sabe que
   GEN1 cortó «corto» en `P4_10 = '1'`.**
4. `ya_medido.py` (A.8, ADR-340) devolvió los `p` sellados de los cuatro
   consumidores en `milpa/tramite.yaml`.

Consecuencia honesta: el corte de `3.2` **no es una elección ciega**. Se
declara el corte primario por el codebook (§3.2), se declara que la
sensibilidad `S1` coincide con el de GEN1, y se dice aquí que se sabía.
**No se ajusta nada hacia atrás.**

---

## 1 · Identidad

### 1.1 · Payload, por el manifiesto y por la raíz

| campo | valor |
|---|---|
| `id` | `enif_2024_enif_2024_bd_csv` |
| `archivo` | `data/raw/enif_2024_bd_csv.zip` |
| `sha256` (manifiesto) | `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` |
| `sha256` (raíz, verificado) | `00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039` — **IDÉNTICO** |
| miembros | `THOGAR.csv` · `TMODULO.csv` · `TSDEM.csv` · `TVIVIENDA.csv` |

Codebook (payloads separados, ambos verificados por sha256 contra la raíz):

| `id` | archivo | `sha256` |
|---|---|---|
| `enif2024_fd_xlsx` | `enif_2024_fd.xlsx` | `17e2ad86ce9e4fd5783ee54e9b51ee436b934e002d5736b82094070c74a25db2` |
| `enif2024_cuestionario_pdf` | `enif_2024_cuestionario.pdf` | `32e37cc13da38691dee20fbffcef3637aeb87b8dac194e64f83bebed8b57ef8b` |

### 1.2 · Población, unidad y ponderador — **declarado, porque cambia el denominador**

| qué | valor | de dónde |
|---|---|---|
| población | **personas de 18 años y más**, residentes de viviendas particulares | cuestionario, rótulo de bloque `PARA PERSONAS DE 18 AÑOS Y MÁS`; `EDAD_V = 18 - 95` |
| unidad | **la persona elegida** (una por hogar, la del cumpleaños inmediato posterior) | cuestionario `2.7`; llave `LLAVEMOD` |
| tabla | **`TMODULO.csv`** — trae los cinco reactivos y las tres variables de diseño | FD, hoja `TMODULO` |
| ponderador | **`FAC_PER`** (factor de expansión a nivel **persona**) | FD `TMODULO:1483` |
| estrato · UPM | `EST_DIS` · `UPM_DIS` | FD `TMODULO:1481-1482` |

**Una sola tabla, un solo ponderador — y aun así ningún denominador se
comparte.** Compartir la apertura del archivo **no** autoriza compartir
denominador: cada `RESULT` declara el suyo en §3.

### 1.3 · Los 8 `RESULT`, enumerados desde la demanda vigente

| `RESULT` | consumidor (`milpa/tramite.yaml`) | familia |
|---|---|---|
| `RES-0046` | `dinero.ahorro.horizonte_corto:horizonte_corto` | A |
| `RES-0047` | `dinero.ahorro.horizonte_corto:horizonte_no_corto` | A |
| `RES-0048` | `dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_corto` | A |
| `RES-0049` | `dinero.ahorro.horizonte_no_corto_con_seguridad_social:horizonte_no_corto` | A |
| `RES-0057` | `dinero.ahorro.via_informal:formal_cualquiera` | B |
| `RES-0058` | `dinero.ahorro.via_informal:informal_cualquiera` | B |
| `RES-0059` | `dinero.ahorro.seguro_deposito_enif2024:desconfianza_como_razon_principal_conoce_proteccion_enif2024` | C |
| `RES-0060` | `dinero.ahorro.seguro_deposito_enif2024:desconfianza_como_razon_principal_no_conoce_enif2024` | C |

**Fuera de este acto** (mismos `CORR-0009`/payload, pero el encargo no los
nombra): `RES-0031`/`RES-0032` (`dinero.ahorro.tiene_ahorros`, sellados por
`ACTO MAESTRA35-N1`). No se tocan. Van a `## NO-CORRIDO`.

---

## 2 · Los reactivos, verbatim del descriptor

### 2.1 · Familia A · `P4_10` — el horizonte

> **4.10** Si usted dejará de recibir ingresos, ¿por cuánto tiempo podría
> cubrir sus gastos con sus ahorros?

| código | etiqueta |
|---|---|
| `1` | Menos de una semana / **No tiene ahorros** |
| `2` | Al menos una semana, pero menos de un mes |
| `3` | Al menos un mes, pero menos de tres meses |
| `4` | Al menos tres meses, pero menos de seis meses |
| `5` | Seis meses o más |
| `8` | No responde |
| `9` | No sabe |

⚠️ **`P4_10` no trae código `b`** → se le pregunta a **toda** la población de
18 y más. El recorte de la familia A **no viene de este reactivo**, viene del
eje de `2.2`.

⚠️ **El código `1` es una categoría colapsada**: mezcla un horizonte
(«menos de una semana») con una **ausencia de ahorro** («no tiene ahorros»).
El descriptor no permite separarlas. Se declara y se arrastra al límite `6.1`.

### 2.2 · Familia A · `P3_13` — el eje de seguridad social

> **3.13** Por parte de su trabajo, ¿usted tiene derecho a los servicios
> médicos…

| código | etiqueta |
|---|---|
| `1` | del Seguro Social (IMSS)? |
| `2` | del ISSSTE? |
| `3` | del ISSSTE estatal? |
| `4` | de PEMEX, Defensa o Marina? |
| `5` | de un seguro privado de gastos médicos? |
| `6` | de otra institución? |
| `7` | Entonces, ¿carece de derecho a servicios médicos por parte de su trabajo (incluye IMSS-Bienestar, antes Seguro Popular, Instituto de Salud para el Bienestar)? |
| `9` | No sabe |
| `b` | Blanco por secuencia |

⚠️ **`P3_13` SÍ trae `b`.** Sólo se le pregunta a quien declaró actividad
económica (`3.8`/`3.9` → `PASE A 3.13`). Quien no trabajó **no tiene eje** y
por tanto **no está en el denominador de la familia A**. Ése es el complemento
de `5.2`.

### 2.3 · Familia B · `P5_1_1`…`P5_1_6` — la vía informal

> **5.1** En los últimos 12 meses, de junio de 2023 a la fecha, ¿usted…

| nemónico | vía |
|---|---|
| `P5_1_1` | ahorró prestando dinero |
| `P5_1_2` | ahorró comprando animales o bienes |
| `P5_1_3` | guardó dinero en una caja de ahorro del trabajo |
| `P5_1_4` | guardó dinero con familiares o personas conocidas |
| `P5_1_5` | participó en una tanda |
| `P5_1_6` | guardó dinero en su casa |

Códigos: `1` = Sí · `2` = No. **Sin `b`** → se preguntan a toda la población.

### 2.4 · Familia B · `P5_6_1`…`P5_6_9` — la vía formal

> **5.6** De junio de 2023 a la fecha, ¿usted guardó o ahorró en su
> {nómina · pensión · apoyos de gobierno · cuenta de ahorro · cheques ·
> plazo fijo · fondo de inversión · cuenta por internet/app · otra cuenta}?

Códigos: `1` = Sí · `2` = No · `b` = Blanco por secuencia (no tiene esa
cuenta: `5.4` = 2 → no se le pregunta `5.6`).

El descriptor trae además la variable derivada
`FILTRO_S5_1` = «¿GUARDÓ DINERO EN ALGUNA CUENTA (5.6 = 1 EN CUALQUIER
OPCIÓN)?». **No se usa como fuente**: se deriva desde `P5_6_*` y se usa
`FILTRO_S5_1` sólo como **control interno** (§3.3).

### 2.5 · Familia C · `P5_20` — la razón principal de no tener cuenta

> **5.20** ¿Cuál es la razón principal por la que no tiene una cuenta o
> tarjeta?

| código | etiqueta |
|---|---|
| `01` | La sucursal le queda lejos o no hay |
| `02` | Los intereses son bajos o las comisiones son altas |
| **`03`** | **No confía en instituciones financieras o le dan mal servicio** |
| `04` | Piden requisitos que no tiene |
| `05` | Prefiere otras formas de ahorro (tanda, guardar en su casa, etcétera) |
| `06` | No la necesita |
| `07` | No le alcanza, sus ingresos son insuficientes o variables |
| `08` | No sabe qué es o cómo usarla |
| `09` | No quiere que le cobren impuestos |
| `10` | Otro |
| `b` | Blanco por secuencia |

⚠️ **El código `03` conflaciona dos cosas**: desconfianza *y* mal servicio.
El descriptor no permite separarlas. El `RESULT` mide la categoría del
codebook, **no** «desconfianza» pura. Se arrastra al límite `6.2`.

⚠️ **Razón principal vs. cualquier razón (el encargo lo pide):** `P5_20` es de
**respuesta única** (`Tamaño 2`, códigos `01`-`10`). ENIF 2024 **no trae**
versión de menciones múltiples para 5.20 (contraste: `5.7`, `5.8`, `5.15`,
`5.17` sí son baterías de mención). → **`cualquier_razon` = `NO-APLICA`**, y
`NO-APLICA` es un valor, no un hueco.

### 2.6 · Familia C · `P5_23` — el conocimiento de la protección

> **5.23** Los bancos o instituciones financieras como todas las empresas
> pueden cerrar o quebrar, ¿sabe si en ese caso los ahorros estarían
> protegidos?

| código | etiqueta |
|---|---|
| `1` | Sí |
| `2` | No |

⚠️ **`P5_23` NO trae código `b`** — y es la única pregunta del tramo
`5.19`-`5.24` que no lo trae. Se le pregunta a **toda** la población de 18 y
más: quien tiene cuenta llega por `5.22` → `5.23`, y quien no tiene llega por
`5.20` → `PASE A 5.23`. **No es un filtro de elegibilidad de `5.20`: es un eje
posterior que la parte en dos.**

---

## 3 · Universos, codificación y denominadores — todo pre-declarado

### 3.1 · Regla general

- Escala de todo `RESULT` de esta spec: **`p` (proporción ponderada)**, con el
  denominador que cada familia declara abajo. **Se escribe por `RESULT`.**
- `8` / `9` (No responde / No sabe) y `b` **no entran al numerador**. Su trato
  en el denominador se declara **por familia** (no hay regla global).
- Faltantes: se cuentan **antes y después** de cada recorte, ponderados y sin
  ponderar, y viajan en `resultados.json` como `embudo`.
- **`NO-APLICA` es un valor.** Un estimando sin reactivo sale
  `NO-CONSTRUIBLE` con el codebook citado, no `0`.

### 3.2 · Familia A · el corte de «corto» — **declarado, no heredado**

**Corte primario (el que se reporta):**

> **`horizonte_corto` ⇔ `P4_10 ∈ {1, 2}`** — «menos de un mes».

Razón, del codebook y sólo del codebook: `P4_10` está construido con cortes en
semana / mes / tres meses / seis meses. El **mes** es el primer límite que el
propio reactivo nombra como frontera cerrada (`2` = «…pero menos de un mes»,
`3` = «Al menos un mes…»). «Corto» = no llega al mes.

> **`horizonte_no_corto` ⇔ `P4_10 ∈ {3, 4, 5}`.**

`8` y `9` **salen del numerador y del denominador** de la familia A y se
cuentan como faltantes. El par `{corto, no_corto}` es entonces **exhaustivo y
excluyente dentro de su propio denominador, por construcción**.

**Sensibilidad `S1`, pre-declarada aquí (§0.3 punto 3):**

> `horizonte_corto_S1 ⇔ P4_10 = 1` — «menos de una semana / no tiene ahorros».

`S1` **es el corte que GEN1 usó**, y esta sesión lo sabía al escribir esto.
Se emite como sensibilidad rotulada, **no** como el valor reportado. El
`RESULT` que se sella es el del corte primario.

### 3.3 · Familia A · el eje, y los tres destinos de `P3_13`

| celda | regla | `RESULT` |
|---|---|---|
| **sin seguridad social** | `P3_13 = 7` | `RES-0046` (corto) · `RES-0047` (no corto) |
| **con seguridad social** | `P3_13 ∈ {1, 2, 3, 4}` | `RES-0048` (corto) · `RES-0049` (no corto) |
| **fuera del par** | `P3_13 ∈ {5, 6, 9}` **o** `P3_13 = b` | complemento §5.2 — **sin `RESULT`** |

Por qué `{1,2,3,4}` y no `{1,…,6}`: seguridad social es derecho a servicios
médicos **por una institución pública de seguridad social**. El `5` es un
**seguro privado** (no es seguridad social) y el `6` («otra institución») el
descriptor no lo resuelve. Ambos, más el `9`, salen del par **con su peso
declarado**, no borrados.

**Denominador de `RES-0046`/`RES-0047`:** personas 18+ con `P3_13 = 7` y
`P4_10 ∈ {1,2,3,4,5}`.
**Denominador de `RES-0048`/`RES-0049`:** personas 18+ con `P3_13 ∈ {1,2,3,4}`
y `P4_10 ∈ {1,2,3,4,5}`.
**Son denominadores DISTINTOS.** `RES-0046`+`RES-0047` = 1 y
`RES-0048`+`RES-0049` = 1, cada par **dentro de su propia celda**; los cuatro
juntos **no** suman nada interpretable.

### 3.4 · Familia B · formal e informal **COEXISTEN**

| estimando | numerador | `RESULT` |
|---|---|---|
| `formal_cualquiera` | `P5_6_j = 1` para **algún** `j ∈ {1..9}` | `RES-0057` |
| `informal_cualquiera` | `P5_1_k = 1` para **algún** `k ∈ {1..6}` | `RES-0058` |

**Denominador de ambos: idéntico** — toda la población de 18 y más con
`FAC_PER` válido. Es el **único** par de esta spec que comparte denominador, y
se dice explícitamente porque la regla por defecto es la contraria.

> **REGLA DURA (Astra §2.4, respaldada por el hallazgo 3.2 del lote ENVIPE):
> formal e informal COEXISTEN. `RES-0057` + `RES-0058` NO se fuerza a 1, no se
> normaliza, no se re-escala, y si suma más de 1 eso NO es un defecto** — es
> gente que ahorra por las dos vías. La suma se **reporta** como diagnóstico,
> nunca se **corrige**.

Un `P5_6_j = b` **no** es un `No`: es «no tiene esa cuenta». Para
`formal_cualquiera` da lo mismo (no aporta un `1`), pero se cuenta aparte en el
embudo para que el `0` de origen sea legible.

**Control interno (no fuente):** `formal_cualquiera` derivado de `P5_6_*` debe
coincidir con `FILTRO_S5_1 = 1`. Si no coincide → se reporta la diferencia con
el conteo de filas discrepantes. **No se ajusta ninguna de las dos.**

### 3.5 · Familia C · el denominador que el encargo tenía al revés

**Guardia que PARA** (la premisa `P4` de §0.1 es ajena y se verifica, no se
supone):

```
G-C1  Si  P5_23  trae algún valor 'b' / vacío  en el archivo
      → PARO. El descriptor dice que no lo trae; si el archivo lo trae,
        el descriptor miente y el eje NO es una partición de la población.
        No se estima; se reporta.
G-C2  Si  {filas con P5_20 != b}  no es subconjunto de
        {filas sin ninguna cuenta declarada en 5.4}
      → PARO. El flujo del cuestionario dice que 5.20 sólo lo contesta
        quien no tiene cuenta. Si no se cumple, el denominador de la
        familia C no es el que esta spec declara.
```

Pasadas las guardias:

| estimando | denominador | numerador | `RESULT` |
|---|---|---|---|
| conoce | 18+ con `P5_20 ≠ b` **y** `P5_23 = 1` | `P5_20 = '03'` | `RES-0059` |
| no conoce | 18+ con `P5_20 ≠ b` **y** `P5_23 = 2` | `P5_20 = '03'` | `RES-0060` |

**Dos denominadores distintos.** `RES-0059` + `RES-0060` **no suma nada**: son
dos tasas condicionales a celdas ajenas. Cualquier lectura que las sume está
mal y la nota de cierre lo dice.

⚠️ **`P5_20` no trae `8`/`9`** (no hay «no responde» codificado); `10` = «Otro»
sí existe y **queda en el denominador**, no en el numerador.

### 3.6 · Escala declarada, por `RESULT`

| `RESULT` | escala |
|---|---|
| `RES-0046`, `RES-0047` | `p` — proporción ponderada de **personas 18+ con trabajo sin seguridad social (`P3_13=7`) y `P4_10` válido** |
| `RES-0048`, `RES-0049` | `p` — proporción ponderada de **personas 18+ con trabajo con seguridad social (`P3_13∈{1,2,3,4}`) y `P4_10` válido** |
| `RES-0057` | `p` — proporción ponderada de **personas 18+** (denominador total) |
| `RES-0058` | `p` — proporción ponderada de **personas 18+** (denominador total) |
| `RES-0059` | `p` — proporción ponderada de **personas 18+ sin cuenta que SÍ conocen la protección** |
| `RES-0060` | `p` — proporción ponderada de **personas 18+ sin cuenta que NO conocen la protección** |

### 3.7 · Diseño: ponderador, estrato y UPM — la lección de `FP-201`

Punto: `p̂ = Σ FAC_PER·1[num] / Σ FAC_PER·1[den]`, dentro del denominador
declarado.

IC: **bootstrap de conglomerados**, re-muestreando `UPM_DIS` **dentro de**
`EST_DIS`, `B = 1000`, semilla fija `20260909`, percentiles 2.5/97.5.

**Guardias de diseño — paran, no adivinan:**

```
G-D1  Las tres columnas EST_DIS, UPM_DIS, FAC_PER existen en TMODULO.csv
      → si falta una: PARO. El FD las declara (§0.2); su ausencia
        significa que el archivo no es el que el descriptor documenta.
G-D2  FAC_PER numérico y > 0 en toda fila usada → si no: PARO con el conteo.
G-D3  Ningún EST_DIS con una sola UPM_DIS distinta entre las filas usadas
      → si lo hay, el bootstrap de ese estrato es degenerado: NO se colapsa
        en silencio; se reporta cuántos estratos y con cuánto peso, y el IC
        de ese RESULT sale rotulado IC-DEGENERADO-EN-<n>-ESTRATOS.
G-D4  EST_DIS y UPM_DIS se leen como TEXTO (son llaves opacas, con ceros a
      la izquierda: '001'-'190', '00001'-'02172'). Leerlas como número
      colapsa llaves distintas. Si el lector las entrega como número: PARO.
```

Codificación de lectura: `TMODULO.csv` se abre **con `dtype=str` en todas las
columnas** y `keep_default_na=False`, para no perder `'01'` ni convertir `'b'`
en `NaN`. `FAC_PER` se convierte a `float` **explícitamente y sólo él**.

⚠️ **Encoding:** los `.zip` de INEGI mezclan UTF-8 y latin-1. La lectura prueba
`utf-8` y cae a `latin-1` **declarando cuál usó** en `ejecucion.json`. Como
todos los reactivos de esta spec son códigos ASCII, el encoding **no puede**
cambiar ningún estimando; si lo cambiara, es un defecto y la guardia `G-D5` lo
atrapa:

```
G-D5  El conjunto de valores distintos de cada reactivo usado debe ser
      subconjunto de los códigos que el FD declara (más '' y 'b').
      Cualquier valor fuera de ese conjunto: PARO, con el valor y su conteo.
```

---

## 4 · Nada causal

`P4_10`, `P5_1_*`, `P5_6_*`, `P5_20` y `P5_23` son **declaraciones del
informante** recogidas en una sección transversal. Ningún `RESULT` de esta
spec se rotula causal, ninguno soporta «porque», y la nota de cierre lo repite.
`P3_13` **no** es una asignación aleatoria: la comparación entre las celdas de
la familia A es **descripción**, no efecto.

---

## 5 · Ramas pre-declaradas — escritas ANTES del dato

### 5.1 · Control positivo posterior contra GEN1 (`REPRODUCE-GEN1`)

Se corre **después** de sellar, por script separado
(`forense/prereg-caja/ENIF-AHORRO-control-gen1.py`), y **no** puede modificar
el medidor ni los `RESULT`.

`DELTA-VS-GEN1 = medido − sellado`, con signo. `REPRODUCE` si
`|delta| ≤ 1e-6`; `NO-REPRODUCE` en otro caso; `NO-COMPARABLE` si el estimando
salió `NO-ESTIMABLE`.

| `RESULT` | valor GEN1 |
|---|---|
| `RES-0046` | `0.3306` |
| `RES-0047` | `0.6694` |
| `RES-0048` | `0.1734` |
| `RES-0049` | `0.8266` |
| `RES-0057` | `0.284927` |
| `RES-0058` | `0.56192` |
| `RES-0059` | `0.06078` |
| `RES-0060` | `0.054767` |

**Se espera `NO-REPRODUCE` en la familia A**, y la razón está escrita **antes**
de correr: el corte primario de §3.2 es `{1,2}` y el de GEN1 es `{1}`. Por eso
`S1` se emite: para que la discrepancia sea **atribuible**, no misteriosa.

⚠️ **A-bis.3:** sólo se compara el **punto**. Los IC de esta corrida (con
diseño) y los de fase 1 (sin diseño) **no se comparan** — no se pega una tabla
que los ponga lado a lado.

**`NO-REPRODUCE` no invalida la corrida, no autoriza tocar el medidor y no se
ajusta hacia atrás**: se reporta con el embudo completo a la vista.

### 5.2 · Complementos — con denominador escrito y **sin rango de cantidad medida**

Misma regla que ENCIG: hipótesis del codebook, **no** herencia.

| complemento | qué es | qué se emite |
|---|---|---|
| `A-FUERA-DEL-EJE` | peso de `P3_13 ∈ {5,6,9}` y de `P3_13 = b` sobre la población 18+ | **peso ponderado + denominador escrito**. NO se le calcula `horizonte_corto`: no es un `RESULT`, no lleva cita en `milpa/` |
| `A-FALTANTE-P4_10` | peso de `P4_10 ∈ {8,9}` dentro de cada celda del eje | conteo y peso, en el embudo |
| `B-NINGUNA-VIA` | peso de quien no marcó ninguna vía formal ni informal | peso ponderado + denominador |
| `B-AMBAS-VIAS` | peso de quien marcó **las dos** | peso ponderado + denominador. **Es la prueba directa de la coexistencia** |
| `C-OTRAS-RAZONES` | peso de `P5_20 ∈ {01,02,04,…,10}` dentro de cada celda | peso ponderado + denominador |

Ninguno de los cinco lleva cita `corrida0_*` en `milpa/tramite.yaml`
(§P3 del encargo): **complementos no medidos como `RESULT` no se citan**, y
cada uno deja su `NC` de advertencia.

### 5.3 · `NO-CONSTRUIBLE`

Si un reactivo no está en `TMODULO.csv` como el FD lo declara, el `RESULT`
sale **`NO-CONSTRUIBLE`** con el codebook citado (nemónico, fila del FD,
códigos esperados) y **el consumidor sube a la vista `--mesa`**. No se
sustituye por un proxy, no se estima «lo más parecido».

### 5.4 · `VEREDICTO-EXHAUSTIVIDAD`, por familia

- Familia A: `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE` — se sabe de
  antemano que el residuo (`P3_13 ∈ {5,6,9,b}`) pesa `> 0`. Se mide cuánto.
- Familia B: **no aplica** — el par no es una partición **por construcción**
  (§3.4). Emitir un veredicto de exhaustividad aquí sería un error de tipo.
- Familia C: `EXHAUSTIVAS-Y-EXCLUYENTES-SOLO-BAJO-EL-RECORTE` dentro de cada
  celda; el residuo es `C-OTRAS-RAZONES`.

---

## 6 · Límites declarados (van también en la nota de cierre)

1. **`P4_10 = 1` es una categoría colapsada** (§2.1): «menos de una semana» y
   «no tiene ahorros» son la misma casilla. Cualquier corte que incluya el `1`
   —el primario y `S1`— arrastra gente sin ahorros dentro de «horizonte
   corto». El descriptor no permite separarlas.
2. **`P5_20 = '03'` conflaciona desconfianza y mal servicio** (§2.5). El
   `RESULT` mide la categoría, no el constructo.
3. **El eje de la familia A excluye a quien no trabaja.** No es un descuido:
   `P3_13` no se les pregunta. El peso excluido se mide (§5.2) pero el
   estimando **no existe** para ellos.
4. **`razón cualquiera` es `NO-APLICA`** en ENIF 2024 (§2.5), no `0`.
5. **Los IC no son comparables con fase 1** (A-bis.3, §0.2).
6. **La población es 18+, no 18-70** (§0.1 `P2`). La `escala_legacy` de
   `RES-0059`/`RES-0060` que dice «18 a 70» queda **desmentida** por el
   descriptor de esta ola; se corrige al escribir la escala nueva.

---

## 7 · Congelamiento

Esta spec, `data/corrida0/CALC-ENIF-0001/spec.yaml` y
`data/corrida0/CALC-ENIF-0001/medidor.py` se congelan en el **COMMIT-1** de
`ACTO GEN2-LOTE-ENIF-1`, **antes de abrir un solo `*.csv` del microdato**.
El COMMIT-2 corre `preflight → run → verify` y **no edita el COMMIT-1**.

**El primer resultado que produzca este procedimiento es el que se reporta.**
