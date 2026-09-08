# `CALC-0001` — cara local de `prereg-caja-S12`, con los códigos resueltos desde codebook

**Acto:** `ACTO GEN2-E5-0 · SPECS EJECUTABLES`, 8/sep/2026, entorno **UBUNTU (caja)**,
sobre `origin/main = d8b5f0b`.

**Spec sellada que gobierna:** `forense/prereg-caja/S12-CSES-spec-v1_0.md`,
`sha256 = 870522a34d9538454b5b774ddc33e46f9cd8e8d62a20f31b2d972f9755447336`
(íntegra contra su sidecar, verificado al abrir este acto). **Este archivo no la
sustituye ni la reescribe**: resuelve las ranuras que ella dejó explícitamente
abiertas «pendiente de codebook», con el codebook citado, y nada más.

**Qué se abrió:** únicamente **metadato** de los tres `.sav`
(`pyreadstat.read_sav(..., metadataonly=True)`: nombres, etiquetas de variable y
etiquetas de valor). **No se leyó ni una observación**, no se calculó ninguna
proporción, ningún IC95, ninguna celda.

---

## 1 · Códigos resueltos (S12 §1 los dejó «no confirmado sin abrir el `.sav`»)

Verificado en `cide_cses2015_nacional_poselectoral.sav` y
`cide_cses2015_nacional_preelectoral.sav` — **idénticos en los dos**:

| variable | etiqueta de valor (verbatim del codebook) |
|---|---|
| `pcyc13` (zanahoria, OFERTA) | `1 = Sí` · `2 = No` · `9 = Ns/NC` |
| `pcyc14` (garrote, AMENAZA) | `1 = Sí` · `2 = No` · `9 = Ns/NC` |

`OFERTA = 1` si `pcyc13 == 1`; `OFERTA = 0` si `pcyc13 == 2`; `9` y faltante
quedan **fuera de los dos grupos y se cuentan**. Ídem `AMENAZA` sobre `pcyc14`.
**No hay código `0`** en ninguna de las dos: se declara porque la forma
`== 0` habría seleccionado el conjunto vacío en silencio.

**Filtro real de `pcyc14`, resuelto (S12 §1 lo dejó «probablemente sobre
receptores»):** el texto de la propia pregunta lo dice —«Y si Usted recibe
alguno de estos beneficios…»— y la batería que la antecede es
`pcyc12` (LICONSA) · `pcyc12a` (PROCAMPO) · `pcyc12b` (PROSPERA). El
**denominador realizado** de cada brazo es dato de corrida (`RESULT-…-N-*`),
no de esta spec: aquí se declara la regla, no el conteo.

---

## 2 · Desenlace — **el hallazgo de apertura de este acto**

S12 §2 declaró el desenlace `NO-CONSTRUIBLE-SIN-CODEBOOK` e instruyó: *«caja abre
el cuestionario completo … antes de decidir si el desenlace existe»*. **Se abrió y
existe.** El inventario (censo de nombres con etiquetas truncadas) no lo mostraba;
el metadato del `.sav` sí:

| archivo | variable | etiqueta verbatim | qué es |
|---|---|---|---|
| `nacional_poselectoral` | **`peledip`** | «El pasado 7 de junio de 2015 fueron las elecciones para DIPUTADOS FEDERALES, ¿Por cuál partido votó usted?» | **voto emitido**, elección federal — la misma campaña que `pcyc13`/`pcyc14` preguntan |
| `nacional_preelectoral` | `pelegob` · `pelemun` | «El pasado 7 de junio de 2015 fueron las elecciones para gobernador/pdte mun / PRESIDENTE MUNICIPAL, ¿Por cuál partido votó usted?» | **voto emitido**, elección **local** — otro cargo |
| `estatal_preelectoral` | `pelegob` · `pelemun` | «**Si hoy fueran** las elecciones … ¿por cuál partido **votaría** usted?» | **intención**, no voto emitido |

**Tres correcciones de premisa, declaradas (no se corrige la spec sellada; se
declaran aquí y se elevan a mesa):**

1. **El desenlace de §2 sí existe.** El falsador principal de S12 §4 **no** queda
   `NO-ESTIMABLE por ausencia de desenlace`. Los tres candidatos que §2 examinó
   (`p9`, `p6`, `p8a`) quedan **fuera**: hay un voto emitido, del año correcto y
   con partido nombrado, que ninguno de los tres igualaba.
2. **El nombre del archivo miente sobre su contenido.** `nacional_preelectoral`
   trae ítems **post**-electorales de voto emitido (`pelegob`/`pelemun`, en
   pasado). Se identifica por el contenido, nunca por el rótulo del archivo.
3. **`nacional_preelectoral` NO es réplica del desenlace.** S12 §1 la ofrece como
   «réplica del mismo cuestionario sobre otra muestra»: lo es **para el
   disparador** (`pcyc13`/`pcyc14` idénticos), **no para el desenlace** — no trae
   `peledip`; su voto emitido es de **otro cargo** (gobernador/municipal). Se
   corre como fila aparte y se rotula como tal, jamás agrupada (S12 §0.2).

### 2.1 · Crosswalk de partido — obligatorio, y por qué

`pcyc13_1`/`pcyc14_1` (¿de cuál partido ofreció/amenazó?) y `peledip`/`pelegob`/
`pelemun` (¿por cuál partido votó?) **usan esquemas de código distintos**. Cinco
códigos coinciden en número y **discrepan en partido**:

| código | `pcyc13_1`/`pcyc14_1` | `peledip`/`pelegob`/`pelemun` |
|---|---|---|
| `3` | PRD | *(no existe)* |
| `4` | **PT** | **PRD** |
| `8` | **MORENA** | **PT** |
| `9` | **Partido Humanista** | **PVEM** |
| `10` | **Encuentro Social** | **OTRO** |
| `12` | **Otro** | **NO SABE** |

Una igualdad directa `pcyc13_1 == peledip` produciría alineamientos falsos en
silencio, sin error. El crosswalk congelado va en `spec.yaml`
(`parametros.crosswalk_partido`), código a código, en el único sentido
`oferente → voto`. `29 = PRI-PVEM` (coalición) cuenta como alineado si el
oferente fue PRI (`2`) o PVEM (`5`) — decisión declarada aquí, antes del dato.
`11 NINGUNO` · `12 NO SABE` · `13 BLANCO` · `14 ANULADO` · `39 CANDIDATO
INDEPENDIENTE` no tienen contraparte de oferente: cuentan `ALINEADO = 0`.
`97 Ninguno` y `99 NS/NC` del oferente son **faltante del brazo**, no un cero.

---

## 3 · Ponderador y diseño (S12 §3 los dejó «ninguno confirmado sin codebook»)

Confirmado por etiqueta en el metadato:

| archivo | ponderador | estrato | UPM |
|---|---|---|---|
| `nacional_poselectoral` | **`PONDFIN`** «Ponderador nacional» | `dominio` | `upmmn` |
| `nacional_preelectoral` | **`PONDFIN`** «Ponderador Global» | `dominio` «Estratos de diseño muestral» | `upmmn` |
| `estatal_preelectoral` | **`PONDFIN`** «Ponderador Global» | `dominio` «Estratos de diseño muestral» | `upmmn` |

`PONDOM`/`PONDDOM`/`PONDOM1`/`PONDOM2`/`PONDDOM1`/`PONDDOM2` son ponderadores
**por dominio**, no globales: no entran. `PONDSEX` y `ponde` no traen etiqueta y
**no se usan** — un nombre no es una etiqueta (S13 §3 fijó el criterio).
`dominio` y `upmmn` **sí existen en los tres archivos**, corrigiendo el «no
confirmado» de S12 §3: el diseño es estimable y el IC no tiene que fingir MAS.

⚠️ **Ranura que S12 no pre-registró y este acto NO inventa en silencio:** S12 §4
exige «IC95 de la diferencia» pero **no pre-registra el método**. Se congela
aquí, declarado: **bootstrap de UPM (`upmmn`) dentro de estrato (`dominio`),
`B = 2000`, `seed = 20260908`, `rng = numpy.PCG64`**, percentil 2.5/97.5. Es una
elección del ejecutor sobre una ranura vacía, no una lectura de la spec sellada
— queda elevada a mesa como `FP` en la nota de este acto.

---

## 4 · §2-bis — el experimento de encuadre

`pvoto1`/`pvoto2`/`pvoto3` existen **sólo** en `estatal_preelectoral`
(confirmado), con códigos **idénticos entre las tres**: `1 = Sí` · `2 = No` ·
`9 = Ns/Nc`. `CREE_QUE_DESCUBREN = 1` si `== 1`, `0` si `== 2`, `9`/faltante
fuera y contados.

**El diseño (split-ballot vs. secuencial) NO se resuelve aquí**: S12 §2-bis lo
hace depender de las tasas de cobertura por variable, que son **valores**, no
metadato. Se congela como **guardia que evalúa el medidor en E5**, con el umbral
pre-registrado por S12: si las tres variables tienen cobertura ~1/3 disjunta →
split-ballot y el contraste corre; si las tres tienen cobertura completa →
`NO-ESTIMABLE-DISEÑO-NO-EXPERIMENTAL` y **no se calcula el contraste**.

---

## 5 · Qué NO hace este `CALC` en `GEN2-E5-0`

No abre microdato. No calcula. No edita `S12-CSES-spec-v1_0.md` ni su sidecar. No
mueve el tier de `R7.3` ni de `R7.6`. No agrupa levantamientos. No sustituye el
desenlace por `p9` (§2 lo permitía como reserva: **no hace falta**, y no se usa).

**El primer resultado que produzca este procedimiento es el que se reporta.**
