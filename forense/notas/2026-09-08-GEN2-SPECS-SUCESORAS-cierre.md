# `ACTO GEN2-SPECS-SUCESORAS` · las cuatro erratas por la vía formal, y la prueba de robustez que las corroboradas se debían

**Acto:** `ACTO GEN2-SPECS-SUCESORAS · S6 v1.3 + S12 v1.1`, 8/sep/2026.
**Entorno:** UBUNTU (caja, corpus montado). **NO** se lanzó en nube.
**Base:** worktree nuevo desde `origin/main = c5b89a9` (`PR #642`). El encargo se
redactó contra `351fd25f` (`PR #639`) y `main` avanzó **9 commits** en el ínterin:
base re-derivada, no heredada (ARRANQUE paso 2). **Encargo archivado (A.3):**
`forense/encargos/2026-09-08-GEN2-SPECS-SUCESORAS.md`, 0-bis `9400c9c`.
**Firma de mesa, verbatim:** «si hagamos las specs sucesoras..»

---

## 0 · Entorno y compuerta (A.2 · A.13)

```
ENTORNO · commit=c5b89a9c303b · git_status=LIMPIO(0) · python=3.14.4
· numpy=2.3.5 pandas=2.3.3 scipy=1.16.3 yaml=6.0.3 pyreadstat=1.3.6
· CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable · red=no-ejecutada
· raices=data_raw:SI descargas_mx:SI · corpus=SI(examinados=400)
```

La red **no** se sondeó: este acto no descarga nada. El corpus sí — **400**
archivos examinados por `tools/entorno.py`, que es lo que sostiene el positivo.
`data/raw` y `data/raices.local.yaml` se enlazaron desde el clon padre **antes**
de evaluar nada (regla del `/acto` paso 3; corrige el defecto de `PR #522`).

**`COMPUERTA: ninguna`** — declaración explícita del encargo, no dispara
verificación. Guard 0 de arranque, las cuatro: base 0 commits detrás de
`origin/main`; árbol limpio; **duplicado**: `git ls-remote` sin coincidencia,
`git worktree list` sin coincidencia, `gh pr list --state open` → **0 PR
abiertos** en todo el repo; `limpia_arbol --reporta` pegado (15 worktrees vivos,
13 ramas locales ya fusionadas, base al día, 0 fuera de política).

---

## 1 · `P1` — `S6 v1.3` SELLADA, dos diferencias y ninguna más

`sucesora_de: v1_2` · `sha256 = e075356bb5b35eb59282481435707f42f0a12f4d5edb72cda0931d7ae27de3eb`

| # | § | `v1.2` decía | `v1.3` dice | de dónde sale | firma |
|---|---|---|---|---|---|
| **(a)** | §1 y §5 | «`T1 = 0` si `es09 == 0`» | «`T1 = 0` si `es09 == 3`» | `ehh02cb_b3b.pdf` **pág. 8** · `ehh02cb_bx.pdf` **pág. 49** | **`FP-349`** |
| **(b)** | §3.5 | conglomerado = **hogar**, *«la localidad no está en los archivos»*, **con reserva** | conglomerado = **localidad** (`id_loc`), **reserva levantada** | metadato de `ehh02dta_bc/c_portad.dta` | **`FP-351`** |

**La (a) toca dos sitios y sigue siendo una.** `v1.2` escribió el código «No»
en §1 **y otra vez** en la cláusula `se_mueve_si` de §5
(`Δ = P_PUB(es09=1) − P_PUB(es09=0)`). Corregir sólo la primera dejaría una
`v1.3` que se contradice en la cláusula que decide si la regla se mueve. El
hecho de codebook es el mismo y la cuenta de diferencias no sube.

**La (b) levanta una reserva, y sólo una.** Siguen íntegras: multiplicidad
(§2.5 — `C1`/`b3b` decide, una fila secundaria sola es `PROPUESTA con reserva`),
pareja de ponderadores (§3.2), coincidencia de signo base/sensibilidad (§2.4),
umbral `n < 10` (§4) y la prohibición causal (§3.6). **Levantar una reserva de
varianza no convierte una co-ocurrencia en una causa.**

**La pre-declaración `B-bis` NO está en la spec, deliberadamente.** Vive en
`data/corrida0/CALC-0003-v3/spec.md` §5, congelada en el mismo `COMMIT-1` y
antes de abrir un `.dta` para calcular, para que el contrato sellado conserve
**exactamente dos** diferencias y la lectura de una corrida concreta no se cuele
dentro del pre-registro.

**Los sellos de `v1_0`, `v1_1` y `v1_2` no se editaron** y verifican contra sus
sidecars (`sella_sha256.py --verifica` → `SELLO_COINCIDE`).

---

## 2 · `P2` — cuatro commits, dos `CALC` sellados, y el defecto que la guardia encontró

### 2.1 · `CALC-0003-v3` — la corrida que el encargo pidió

`repite_de: CALC-0003-v2` · 142 `RESULT` (los 128 de v2 con sus mismos ids + 14
diagnósticos) · `corrida_id = CALC-0003-v3--6d648f99dc28` · sello
`3b2399b1ee8b7b4f5424eadeef537688bd7a499beb1cac5746d44201de001712`.

`PRE-FLIGHT VERDE → run → SELLADO → VERIFY: REPRODUCE`
(`CONTEXTO=IDENTICO · RESULTADO=REPRODUCE`), **142/142**.

**Control de regresión perfecto:** los 128 ids de v2 están los 128; los **104**
que no son `IC-LO`/`IC-HI`/`VEREDICTO` reproducen **idénticos**. **0 movidos.**

**Y los IC se estrecharon** (×0.90–×1.00) — **lo contrario** de lo que la propia
spec había declarado esperar antes de correr («conglomerados más grandes ⇒
intervalos más anchos»). Ese pronóstico escrito de antemano es lo único que
convirtió un número raro en un hallazgo en vez de en un resultado.

### 2.2 · La guardia dijo por qué

```
RESULT-C1-B3B-N-SIN-CONGLOMERADO =  182 de  342
RESULT-C1-BX-N-SIN-CONGLOMERADO  =   87 de   93
RESULT-C2-B3B-N-SIN-CONGLOMERADO = 1655 de 3179
RESULT-C2-BX-N-SIN-CONGLOMERADO  =  220 de  233
RESULT-C3-B3B-N-SIN-CONGLOMERADO =  160 de  301
RESULT-C4-B3B-N-SIN-CONGLOMERADO = 1473 de 2825
```

**La causa, medida:** `c_portad.dta` es **una fila por hogar** — 8 437 folios en
8 438 filas con llave, y su `ls` identifica al **respondente de la portada** (10
valores, moda `1` y `2`), no a cada persona. El `left-join` por `(folio, ls)`
—heredado de `CALC-0003` y nunca declarado por ninguna spec— resuelve **7 870 de
19 804** personas de `iiib_es`.

**Por qué `v2` no lo notó y `v3` sí.** En `v2` el conglomerado era el hogar: cada
fila huérfana conservaba su `folio` y seguía siendo su propio conglomerado — el
daño era un pseudo-estrato `NaN`, invisible y casi inocuo. En `v3` **todas** las
huérfanas caen en **un solo** conglomerado `NaN`, que el remuestreo dentro de ese
pseudo-estrato toma **siempre entero**, sin variabilidad. Eso **estrecha** el IC.

**El defecto es heredado, no introducido aquí.** `CALC-0003` y `CALC-0003-v2`
hacen el mismo join y su `estrato` estaba igual de ausente — sólo que ninguna
publicaba contador de cobertura, así que nadie lo vio.

### 2.3 · `CALC-0003-v4` — el reemplazo, congelado en un tercer commit

**No se corrigió hacia atrás.** `CALC-0003-v3` no se editó, no se retiró y no se
re-corrió: sus bytes quedan sellados tal como salieron, porque lo que aporta —el
diagnóstico que descubrió el defecto heredado— no lo aporta `v4`.

`repite_de: CALC-0003-v3` · 143 `RESULT` · `corrida_id = CALC-0003-v4--835dffff2dd1`
· sello `b3845dba01ec7856a003c5ec3f2d50b31573fd3cb80402ff6f4dc1fb52a6b230` ·
`VERIFY: REPRODUCE` **143/143**.

**Única diferencia:** `estrato` e `id_loc` se toman por la llave de **hogar**
(`folio`). **La corrección no elige nada:** son atributos del hogar y se verificó
que son **constantes dentro de `folio`** — `RESULT-COBERTURA-DISENO` =
`DEDUP-LOSSLESS`, 0 folios con más de un `estrato`, 0 con más de un `id_loc`; la
dedup descarta **una** fila (folio `8486000`, `ls` 1 y 7, con
`edo`/`mpio`/`loc`/`estrato`/`id_loc` idénticos). Cobertura resultante ~100 %
(`iiib_es` 19 799/19 804 · `iiib_ec` 17 723/17 728 · `iiib_hs` 19 794/19 799 ·
`iiib_ce` 19 798/19 803 · `p_es`/`p_hs`/`p_ce` 1 847/1 848 cada uno).

**Cobertura reparada — los seis a 0:**

| fila | conglomerados v3 → v4 | sin conglomerado v3 → v4 | universo |
|---|---|---|---|
| `C1-B3B` | 91 → **118** | 182 → **0** | 342 |
| `C1-BX` | 6 → **60** | 87 → **0** | 93 |
| `C2-B3B` | 150 → **150** | 1 655 → **0** | 3 179 |
| `C2-BX` | 10 → **94** | 220 → **0** | 233 |
| `C3-B3B` | 83 → **111** | 160 → **0** | 301 |
| `C4-B3B` | 145 → **147** | 1 473 → **0** | 2 825 |

**Control de regresión: 103 ids comparables, 103 idénticos, 0 movidos — contra
`v2` y contra `v3`.** Ningún punto estimado se movió. La reparación tocó la
varianza y nada más.

**Diseño verificado** (`RESULT-CONGLOMERADO-LOCALIDAD` /
`RESULT-CONGLOMERADO-ANIDAMIENTO`): `id_loc` → **150** conglomerados;
`(edo, mpio, loc)` → **150**; **`BIYECCION-VERIFICADA`**, las dos llaves
particionan igual. `loc` a secas → **61**: no es único a nivel nacional y **no se
usa** — es la trampa que la guardia existía para impedir. 4 estratos, 8 437
hogares, 18–75 localidades por estrato, **`ANIDADO`** (0 localidades cruzan
estrato, 0 hogares cruzan localidad, 0 `id_loc` nulos).

### 2.4 · La tabla comparativa · `v2` (hogar) → `v3` (localidad, rota) → `v4` (localidad, reparada)

Misma escala, mismo universo, misma `seed` — comparable sin enlace de registro.
**El `Δ` puntual es el mismo en las tres.**

| fila | `Δ` | IC95 `v2` | IC95 `v3` | IC95 `v4` | ancho v4/v2 | veredicto (las tres) |
|---|---|---|---|---|---|---|
| **`C1-B3B-FAC3B`** (primaria) | −0.065961 | [−0.148043, +0.020537] | [−0.144938, +0.019668] | **[−0.198439, +0.072787]** | **×1.61** | `NO-DISCRIMINA` |
| `C1-BX-FAC3APX` | +0.000790 | [−0.036578, +0.022008] | [−0.036578, +0.022008] | [−0.179814, +0.273356] | ×7.74 | `NO-DISCRIMINA` |
| `C1-BX-FAC3BPX` | +0.000148 | [−0.037034, +0.021274] | [−0.037034, +0.021274] | [−0.181408, +0.271057] | ×7.76 | `NO-DISCRIMINA` |
| `C2-B3B-FAC3B` | +0.032666 | [−0.003639, +0.069743] | [−0.001537, +0.070521] | [−0.022682, +0.086848] | ×1.49 | `NO-DISCRIMINA` |
| `C2-BX-FAC3APX` | −0.026564 | [−0.088181, +0.032465] | [−0.080491, +0.028927] | [−0.192102, +0.168135] | ×2.99 | `NO-DISCRIMINA` |
| `C2-BX-FAC3BPX` | −0.027617 | [−0.089011, +0.031167] | [−0.081452, +0.027784] | [−0.192237, +0.166242] | ×2.98 | `NO-DISCRIMINA` |
| **`C3-B3B-FAC3B`** | **+0.181865** | [+0.090029, +0.281877] | [+0.101355, +0.277414] | **[+0.014702, +0.356366]** | **×1.78** | **`CORROBORADA`** |
| **`C4-B3B-FAC3B`** | **+0.067035** | [+0.027643, +0.104595] | [+0.031635, +0.100787] | **[+0.012579, +0.120725]** | **×1.41** | **`CORROBORADA`** |

**Ningún veredicto de ninguna de las ocho filas cambia entre `v2` y `v4`.** Y
ahora los IC ensanchan (×1.41 a ×7.76), que es la dirección declarada de
antemano. El brazo `bx` es el que más paga: con 60 y 94 localidades sobre
universos de 93 y 233 personas, su IC se multiplica por casi 8 — y su
`PAREJA = COINCIDEN-EN-SIGNO` sigue en pie.

### 2.5 · La pre-declaración `B-bis`, aplicada verbatim

Congelada en el `COMMIT-1` (`6d648f9`), **antes** de que existiera un solo número
de `v3`, y **no reescrita** al nacer `v4` — reescribirla después de ver los IC de
`v3` habría sido exactamente lo que el patrón de dos commits existe para impedir.

1. **`C1`/`b3b` NO cambia de estado.** Sigue `NO-DISCRIMINA`. **No hay «EL
   hallazgo»**, y eso se reporta primero porque la regla lo mandaba.
2. **`C3` y `C4` conservan su intervalo sobre el umbral → corroboración
   SECUNDARIA ROBUSTA.** Y el margen adelgaza, y se dice: `C3` `IC-LO`
   **+0.090029 → +0.014702**; `C4` **+0.027643 → +0.012579**. Con el
   conglomerado del diseño y cobertura completa, siguen excluyendo 0 — por poco.
3. **Ninguna fila cruza 0: ninguna baja a `PROPUESTA`.**

**Y lo que ninguna de las tres autoriza.** El veredicto de la **regla** lo decide
`C1`/`b3b` (`S6` §2.5): con `C1` en `NO-DISCRIMINA`, `C3`/`C4` solas son
`PROPUESTA con reserva`, no `CORROBORADA` de `R4.4`. `C3`/`C4` corren sobre `T2`
(`ec01*`), que `S6` §1 declara aproximación de «crónico», **no** de «crónico
complejo». Las cuatro celdas miden **co-ocurrencia, no secuencia** (`S6` §3.6:
`es09` es *de por vida*, `hs01` *12 meses*, `ce01` *4 semanas*). **`R4.4` /
`salud.atencion.grave` NO se mueve por estos `CALC`** — etiqueta de la propia
spec sellada, heredada sin cambio.

---

## 3 · `P3` — `S12 v1.1` SELLADA

`sucesora_de: v1_0` · `sha256 = 31100ef824ca7163747adf16ae1708187644cc578542e4e4c2aafaf1bc8418a7`

**(a) `FP-350` · el desenlace sí existe.** Es **`peledip`** («El pasado 7 de junio
de 2015 fueron las elecciones para DIPUTADOS FEDERALES, ¿Por cuál partido votó
usted?»), en `nacional_poselectoral`. Con él, dos correcciones más de premisa:
`nacional_preelectoral` **trae ítems post-electorales pese a su nombre**
(`pelegob`/`pelemun`, en pasado) y por eso **no es réplica del desenlace** — lo
es para el disparador, no para el desenlace. §0.5 incorpora al papel el
**crosswalk de partido**: cinco códigos coinciden en número y discrepan en
partido (`4` = PT vs. PRD, `8` = MORENA vs. PT, `9` = Humanista vs. PVEM…), así
que `pcyc13_1 == peledip` daría alineamientos falsos **en silencio**.

**(b) `FP-357` · `NO-ESTIMABLE-CON-ESTA-FUENTE`.** Los cuatro brazos de
`CALC-0001` salen `N-T0 = 0`:

| brazo | `N-T1` | `N-T0` | `N-NSNC` | `P-T1` |
|---|---|---|---|---|
| POSEL · OFERTA | 42 | **0** | 12 | 0.37922545290553505 |
| POSEL · AMENAZA | 14 | **0** | 11 | 0.438740191776023 |
| PREEL · OFERTA | 23 | **0** | 1 207 | 0.2468700731109074 |
| PREEL · AMENAZA | 10 | **0** | 1 213 | 0.18369940751162478 |

**Es estructural, no `n` corta:** el desenlace se construye sobre
`pcyc13_1`/`pcyc14_1` («¿qué partido le ofreció / lo amenazó?»), preguntas que
**sólo existen para quien contestó que sí**. Control positivo sobre el dato crudo
— el código `2 = No` existe y es mayoritario:

```
poselectoral   pcyc13: {1: 58, 2: 1130, 9: 12}   NaN=0
               pcyc14: {1: 24, 2: 1165, 9: 11}   NaN=0
preelectoral   pcyc13: {1: 63, 2: 1130, 9: 7}    NaN=1200
               pcyc14: {1: 23, 2: 1164, 9: 13}   NaN=1200
```

Había 1 130 y 1 165 personas en el brazo control y **ninguna podía tener
desenlace**. Multiplicar la muestra por diez multiplicaría por diez un `N-T0` que
seguiría siendo **cero**.

**§4.2 · lo que este `NO-ESTIMABLE` NO concluye.** Es **ausencia de medición, no
evidencia contra `R7.3` ni `R7.6`**: los tiers `[MEDIA]` de D2-f y D2-g quedan
**exactamente donde estaban** y las tres piezas gemelas de la propuesta no se
tocan. Tampoco invalida el instrumento: CIDE-CSES 2015 mide bien la
**prevalencia** (58 y 24 casos declarados) y `§2-bis` sigue en pie sobre otro
archivo.

**§5 conservada verbatim y declarada INEJECUTABLE.** Reescribir una cláusula de
falsación después de saber que no dispara sería elegir el criterio con el
resultado a la vista. **Una `se_mueve_si` que no puede evaluarse no es una
`se_mueve_si` cumplida.**

**El contraste acotado a receptores NO se cuela** (§4.1): cambia el estimando —ya
no compara expuestos vs. no expuestos sino la composición interna de los
expuestos—, y va como fila de decisión (`FP-363`).

**`CALC-0001` no se re-corre: sus 54 `RESULT` no cambian — el defecto era del
papel, no del cálculo.** Abrió el cuestionario que `v1.0` §2 mandó abrir,
encontró el desenlace, construyó el crosswalk y publicó `N-T0 = 0` con
`NO-ESTIMABLE`: la respuesta correcta, por el camino correcto.

**Dos anotaciones de resolución, no diferencias** (§1 y §3): códigos
`1 = Sí` / `2 = No` / `9 = Ns/NC` sin código `0`; filtro de `pcyc14` sobre
`pcyc12`/`12a`/`12b`; `PONDFIN` global en los tres archivos, `dominio` estrato,
`upmmn` UPM. **Se citan sin borrar el texto que declaró la incertidumbre** — ese
texto es el registro de qué se sabía al congelar.

---

## 4 · `P4` — registro, y el contador que se queda quieto a propósito

`corrida0 registro` re-derivó las tres vistas: **102 corridas · 886 resultados ·
205 usos**. Cadena en el registro:

```
CALC-0003        SUPERADO→CALC-0003-v2
CALC-0003-v2     SUPERADO→CALC-0003-v3    cuenta_gen2=SI
CALC-0003-v3     SUPERADO→CALC-0003-v4    cuenta_gen2=PENDIENTE-DE-MESA
CALC-0003-v4     SELLADA                  cuenta_gen2=PENDIENTE-DE-MESA
```

**`data/corrida0/decisiones.tsv` NO se tocó, y se dice por qué.** El encargo lo
condicionó explícitamente —«fila `cuenta_gen2` del v3 **SOLO si la firma viaja en
el lanzamiento** — mismo estándar que `FIRMA-CONTADOR`: autoridad, fecha,
objeto»— y la firma de este lanzamiento («si hagamos las specs sucesoras..»)
tiene por **objeto** las specs sucesoras, **no el contador**. Escribir la fila
sería inventar una firma.

**Consecuencia, medida:**

```
N_resultados_gen2_sellados = 211   (sin cambio)
N_corridas_selladas        = 3     (sin cambio)
```

**Simulado EN MEMORIA, sin escribir el árbol** (`registro()` escribe las vistas
derivadas: una firma «simulada» en el archivo sí contamina): con
`CALC-0003-v4 cuenta_gen2=SI` el conjunto pasaría a **226 (+15)** y las corridas
a **4**. Los 15 ids nuevos son exactamente los diagnósticos de conglomerado y
cobertura. Va como **`FP-362`**.

**Firmas.** `FP-349`, `FP-350`, `FP-351`, `FP-357` → **`EJECUTADAS`**, cada una
con estampa de universo (qué cierra y qué **no**). Nuevas: **`FP-361`** (el hueco
del pre-registro: `S6` §3.4 tabula cinco joins y ninguno es contra `c_portad`,
de donde §3.5 toma `estrato` e `id_loc` — no se parcha editando un sello),
**`FP-362`** (contador), **`FP-363`** (el contraste acotado a receptores).
`ABIERTAS`: 8 → **7**.

---

## 5 · Validación

| qué | comando | salida |
|---|---|---|
| spec ejecutable v3 | `corrida0 spec-check CALC-0003-v3` | **78 OK · 0 FAIL · 317 718 filas** |
| spec ejecutable v4 | `corrida0 spec-check CALC-0003-v4` | **79 OK · 0 FAIL · 317 718 filas** |
| corrida v3 | `preflight` → `run` → `verify` | `VERDE` → `SELLADO` → **`REPRODUCE` 142/142** |
| corrida v4 | `preflight` → `run` → `verify` | `VERDE` → `SELLADO` → **`REPRODUCE` 143/143** |
| sellos previos | `sella_sha256.py --verifica` sobre `S6 v1_2` y `S12 v1_0` | **`SELLO_COINCIDE`** los dos |
| suite (base `c5b89a9`) | `tests/check.py --baseline` | **`LÍNEA BASE: VERDE`** |
| suite (tras fusionar `origin/main = 0763457`) | `tests/check.py --baseline` | **`ROJO` — 1 entrada, heredada, ver abajo** |

🛑 **El rojo es de `origin/main`, no de este acto — con control positivo.** Al fusionar `origin/main = 0763457` (`PR #643`, `ACTO GEN2-TRAMITE-BANDEJA`) la suite pasa a `ROJO` por **una** entrada: `T-YAMEDIDO: forense/encargos/2026-09-08-GEN2-TRAMITE-BANDEJA.md: cita R8.3 y no trae salida de tools/ya_medido.py`. **Control:** `git worktree add <tmp> origin/main` — un árbol limpio, **sin un solo commit de esta rama** — y `tests/check.py --baseline` ahí da **exactamente la misma única entrada**. **Esta rama añade cero entradas nuevas sobre esa base.** No se repara aquí: exigiría editar `tests/check.py` (fuera del perímetro declarado del acto) o el encargo verbatim de otro acto (lo prohíbe la regla de la casa). Queda como **`NC-0066`**.

**Siete commits, en el orden que hace verificable la disciplina** — es el orden,
y no la palabra del ejecutor, lo que prueba que la spec se fijó antes del número:

```
9400c9c  0-bis A.3 (encargo verbatim)
6d648f9  COMMIT-1  S6 v1.3 SELLADA + CALC-0003-v3 congelado
3058e63  COMMIT-2  CALC-0003-v3 SELLADA -- la guardia mordió
835dfff  COMMIT-3  CALC-0003-v4 congelado (el reemplazo)
8250fc8  COMMIT-4  CALC-0003-v4 SELLADA
017f198  COMMIT-5  S12 v1.1 SELLADA
   ↓     COMMIT-6  cascada (ADR-421, L0, registro, firmas, nota)
```

---

## 6 · Contador del programa

**Medición: SÍ.** Dos `CALC` sucesores sellados con cadena completa y `verify
REPRODUCE`; 285 `RESULT` nuevos entre los dos. **Y las corroboradas salieron
honestamente matizadas**, que era el objeto del encargo: mismo veredicto, margen
mucho más delgado, y **por primera vez con el conglomerado del diseño y con
cobertura completa** — `C3` `IC-LO` +0.090029 → +0.014702, `C4` +0.027643 →
+0.012579.

**El contador GEN2 se queda en 211 esperando una firma, no roto** (`FP-362`).

**Lo que este acto no reclama.** No mueve `R4.4` ni `R7.3`/`R7.6`. No adopta
ningún `RESULT` al motor. No cierra `NC-0053`. No congela línea base.
