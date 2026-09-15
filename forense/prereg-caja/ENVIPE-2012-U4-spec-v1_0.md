# ENVIPE-2012-U4 · Pre-registro de la ruta declarada para construir `U4` (unidad PERSONA) en ENVIPE 2012 — join a `tsdem` por `N_REN == R_SEL`, cardinalidad verificada antes de medir

### `prereg-caja-ENVIPE-2012-U4` · **v1.0** · 14 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` · pieza **P2** (`NC-0099`; toca también `NC-0098` en su ola 2012) · CAJA (Ubuntu/WSL2) · base `origin/main = 7de3acb4`
**Encargo:** `forense/encargos/2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1.md` (A.3)
**Sucesora por extensión de:** `forense/prereg-caja/R-ENVIPE-SERIE-DBF-spec-v1_0.md` (`sha256 f5ce91e1…`, §5: «si algún acto futuro quisiera `U4` en estas olas … 2012 no [puede sin] un join a `tsdem` por `N_REN == R_SEL` que ninguna spec de esta familia declara … Esa ruta no se improvisa aquí») y de `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` (define `U4`, el colapso GEN1 y `FAC_ELE`). **Ninguna de las dos se edita.**
**Corrida:** `data/corrida0/CALC-ENVIPE-U4-2012/`

> **CONGELADA EN EL COMMIT-1, ANTES DE LEER UN SOLO VALOR DEL MICRODATO.**
> Lo único abierto al escribirla (E.5): `data/manifiesto.yaml`; la lista de
> miembros del ZIP con tamaños; los **descriptores de campo** de la cabecera de
> `tper_vic.dbf`, `tsdem.DBF`, `Tmod_Vic.DBF` y `tvivienda.dbf` (nombre, tipo,
> ancho) y su número de registros declarado; `fd_envipe2012.xls` (hojas
> `TPer_Viv`, `TSDem`, `TMod_Vic`); las specs selladas citadas; el medidor y
> los `RESULT` sellados de `CALC-R-CIV-M-01` (misma ola). **Ningún valor de
> ningún registro.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

| lo que el encargo declaró | lo real, verificado |
|---|---|
| «P2 = NC-0099: la ruta U4 en ENVIPE 2012 vía join a tsdem por N_REN == R_SEL» | CIERTO: `NC-0099` `ABIERTA`, sucesor «acto que abra U4 en olas DBF: tiene que DECLARAR en su spec el join a tsdem por N_REN == R_SEL antes de medir, y verificar la cardinalidad del join contra tsdem». Esta spec es esa declaración. |
| «Verificado: 0 filas U4/tsdem-2012 en corridas.tsv» | CIERTO por conjunto: ningún `CALC` del registro declara `archivo: tsdem.DBF` ni `archivo: tper_vic.dbf` entre sus `variables` (`grep -il 'archivo: *"\?\(tsdem\|tper_vic\.dbf\)' data/corrida0/*/spec.yaml` → 0 de 83 `spec.yaml` examinados; las 4 menciones léxicas que sí existen son la guardia `guardia_tper_vic2: NO-APLICA` del trío DBF y el `tper_vic2` de 2025). |

**Lo que la cabecera real de los DBF dice** (leída hoy, descriptor de 32 bytes por campo; el FD lo confirma):

| tabla | registros | campos relevantes (tipo·ancho) |
|---|---|---|
| `Tmod_Vic.DBF` | 32 493 | `CONTROL C6 · VIV_SEL C2 · HOGAR C1 · ND_TIPO C1 · BPCOD C2 · R_SEL C2 · BP1_20 C1 · BP1_23 C2 · FAC_DEL C6 · EST C3 · UPM C5` — **sin `ID_PER`, sin `N_REN`** |
| `tper_vic.dbf` | **311 436** | `CONTROL · VIV_SEL · HOGAR · N_INF C2 · R_SEL C2 · TOT_PER C2 · … · FAC_VIV C6 · FAC_ELE C6 · DOM · EST C3 · UPM C5` — **sin `N_REN`** |
| `tsdem.DBF` | **311 436** | `CONTROL · VIV_SEL · HOGAR · N_REN C2 · PAREN · SEXO · EDAD C2 · … · FAC_VIV C6 · DOM · EST C3 · UPM C5` |

FD (`fd_envipe2012.xls`, hoja `TPer_Viv`, filas 22-25): `N_INF` «Número de
renglón del informante», `R_SEL` «Renglón de la persona seleccionada»; fila
975-976: `FAC_ELE` «Factor de personas elegidas. Ponderador requerido para
estimar resultados de las preguntas de percepción de la seguridad pública y la
victimización de la población de 18 años y más». Hoja `TSDem` fila 21-22:
`N_REN` «3.1 Número de renglón». Hoja `TMod_Vic` fila 40-41: `R_SEL` «Renglón
de la persona seleccionada».

**Identidad de la persona seleccionada en 2012**, derivada del descriptor y no
supuesta: `(CONTROL, VIV_SEL, HOGAR, R_SEL)`. `Tmod_Vic` la porta en cada
delito; `tper_vic` la porta en cada una de sus 311 436 filas (una por
integrante del hogar, sin decir cuál integrante es cada fila); `tsdem` porta
`N_REN` por integrante. **La ruta:** el delito se atribuye a la persona por
`(hogar, R_SEL)`; el ponderador `FAC_ELE` y el diseño `EST/UPM` se toman de
`tper_vic` **por hogar**, y la existencia de esa persona se verifica en
`tsdem` por `N_REN == R_SEL` del mismo hogar — **con cardinalidad medida y
pre-declarada, nunca supuesta** (lección: un join nuevo devuelve vacío, no
error).

---

## 1 · Identidad

`envipe_2012_base_de_datos_envipe_2012_dbf` →
`data/raw/envipe2012/base_de_datos_envipe_2012_dbf.zip`, `sha256
d7caa74ea4264d59fecfc1d1959824051adfe43613514e2e5ca22f24f31548f5`
(verificado hoy), 6 miembros: `tper_vic.dbf` (87 832 474 B), `tsdem.DBF`
(12 146 582 B), `tvivienda.dbf`, `Tmod_Vic.DBF` (5 690 597 B),
`ENVIPE12_Cuest.zip`, `FD_ENVIPE12.zip`. Descriptor externo:
`data/raw/envipe2012/fd_envipe2012.xls` (`sha256 dcca5373…`). Mismo payload
que `CALC-R-CIV-M-01`.

Los DBF se leen con el mismo lector de `CALC-R-CIV-M-01`: cabecera de 32 bytes
+ descriptores del **propio archivo**, todo campo como texto `latin-1`, registros
borrados excluidos y contados. Las llaves de hogar se comparan **tras `strip()`**
en las tres tablas (mismo ancho declarado en las tres: `C6/C2/C1`; el `strip`
se aplica igual en las tres, así que no puede partir una llave en una tabla y
no en otra) y `EST`/`UPM` se agrupan como texto crudo `strip`, nunca `int()`.

---

## 2 · Universos y codificación — copiados, no elegidos

- **`U1` (delito), homologado a `prereg-caja-ENVIPE-DENUNCIA` con el
  corrimiento de 2012 sellado en `R-ENVIPE-SERIE-DBF` §3.1:** filas de
  `Tmod_Vic.DBF` con `BPCOD ∈ {04,…,14}` (bloque personal **de esta ola**),
  `BP1_20 = 2`, `BP1_23 ∈ {01,…,08}`, `FAC_DEL` finito `> 0`. Se emite
  `PERFIL-BPCOD` (estructural, sin ponderador, antes de todo filtro) para
  falsar el corrimiento: 2012 no puede tener un `15`.
- **Codificación** (verbatim): `C1 = 1 si BP1_23 ∈ {01,02,06}`, `0 si ∈
  {03,04,05,07,08}`; `C2 = 1 si ∈ {01,02,06,08}`, `0 si ∈ {03,04,05,07}`.
- **`U4` (persona):** personas seleccionadas `(hogar, R_SEL)` con **≥ 1 delito
  en `U1`**, con `FAC_ELE` finito `> 0` resuelto por la regla §3.1 y con
  **exactamente una** fila de `tsdem` con `N_REN == R_SEL` en su hogar (§3.2).
  **Colapso GEN1 verbatim:** `d(persona) = max` de `d(delito)` sobre sus
  delitos de `U1`, por separado para `C1` y `C2`.
- **Control interno de lectura (no de estimando):** `p(C1, U1)` y `N-U1` se
  recalculan aquí y se comparan contra los `RESULT` sellados de
  `CALC-R-CIV-M-01` (`P-C1-U1 = 0.29557241046799515`, `N-U1 = 14532`,
  `N-FILAS-TABLA = 32493`), recibidos como parámetro de referencia. Si no
  coinciden al `1e-9`, `G-CONTROL-U1 = NO-REPRODUCE` y **la corrida se
  reporta igual**: el defecto sería del lector o del universo, no del dato, y
  se atribuye en la nota.

## 3 · La ruta, pre-declarada como guardias

### 3.1 · `FAC_ELE`, `EST`, `UPM` por hogar desde `tper_vic`

Por hogar `(CONTROL, VIV_SEL, HOGAR)` de `tper_vic` se miden, **antes de
resolver nada**: `G-PER-N-HOGARES`; `G-PER-N-HOGARES-FILAS-NE-TOT-PER` (hogares
cuyo número de filas ≠ `TOT_PER`); `G-PER-N-HOGARES-R-SEL-MULTI` (más de un
`R_SEL` distinto en el hogar); `G-PER-N-HOGARES-FAC-ELE-MULTI` (más de un
`FAC_ELE` distinto, como texto `strip`, entre las filas del hogar);
`G-PER-N-HOGARES-EST-UPM-MULTI` (más de un par `EST/UPM`). Regla de
resolución del ponderador de la persona seleccionada, **en este orden y sin
cuarta rama**:

1. todas las filas del hogar traen el **mismo** `FAC_ELE` (texto) → ése;
2. si no, **exactamente una** fila del hogar trae `FAC_ELE` finito `> 0` →
   ése (`N-HOGARES-FAC-ELE-RESUELTO-POR-UNICA-VALIDA`);
3. si no → el hogar sale de `U4`, contado (`N-U4-FAC-ELE-AMBIGUO`).

`EST`/`UPM` se resuelven igual (rama 1; si hay más de un par → contado en
`N-U4-DISENO-AMBIGUO`, la persona entra al punto y **no** al diseño). `R_SEL`
del hogar en `tper_vic` debe coincidir con `R_SEL` del delito en `Tmod_Vic`:
si no, el delito no es atribuible (`N-DELITOS-R-SEL-DISCORDA`, fuera de `U4`).

### 3.2 · Cardinalidad del join a `tsdem` por `N_REN == R_SEL`

Para cada persona candidata a `U4`: número de filas de `tsdem` de su hogar con
`N_REN == R_SEL` (texto `strip`, comparación **numérica** tras `int()` porque
`C2` puede traer `' 3'` o `'03'` — se mide `G-TSDEM-PERFIL-N-REN` para
delatarlo). `N-U4-TSDEM-0` (cero: persona sin renglón — sale, contada),
`N-U4-TSDEM-1` (una: entra), `N-U4-TSDEM-MULTI` (más de una: llave no única —
sale, contada). Además, sobre las que entran: `N-U4-EDAD-MENOR-18` y
`N-U4-EDAD-NO-ESPECIFICADA` (`EDAD ∈ {98, 99}`), **sólo contadas** — la
persona elegida es de 18+ por diseño (FD `FAC_ELE`), y una edad `< 18` es
hallazgo, no filtro. `G-TSDEM-N-HOGARES-FILAS-NE-TPER` cuenta hogares con
distinto número de filas en `tsdem` y `tper_vic`.

Si `N-U4-TSDEM-1 = 0` con candidatos `> 0` → `ESTADO =
NO-ESTIMABLE-JOIN-VACIO` (el join no calzó nada: defecto de llave, no dato).

### 3.3 · Varianza

Bootstrap de `UPM` con reemplazo dentro de `EST`, 2 000 réplicas, percentiles
2.5/97.5, `seed = 20260909` (la de la serie ENVIPE), `numpy.PCG64`; estrato de
UPM única se re-muestrea a sí mismo (`METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA`
→ límite inferior). Taylor de cotejo con la aproximación declarada de
`lonely.psu="adjust"`, secundaria.

## 4 · Estimandos

**DESCRIPTIVO.** Ningún `RESULT` es causal. Ninguno adopta nada ni toca `milpa/`.

- **Primario de esta pieza:** `P-C2-U4` (la partición GEN1 en unidad persona,
  `FAC_ELE`) con IC de diseño; `P-C1-U4` como secundario homologado. **No hay
  valor GEN1 de 2012 en unidad persona contra el cual controlar** (los tres
  dictámenes del trío viejo son de unidad delito, `NC-0098`): no se declara
  `REPRODUCE-GEN1` para `U4`, y **no se compara** con el `0.294313` de 2025
  (otra ola).
- **Secundarios:** embudo completo de la ruta (§3), `P-C1-U1` de control,
  masas, perfiles de llave.

## 5 · Límites declarados

Una sola ola (2012) · la ruta vale para 2012 y se declara aquí; 2013/2015 no
se tocan (`NC-0098` conserva esas olas) · `FAC_ELE` de la persona seleccionada
se lee de `tper_vic` **por hogar** bajo la regla §3.1 — si la rama 1 no se
cumple en todos los hogares, el hallazgo se reporta con sus conteos y la
regla 2 es la única sustituta permitida · A-bis.3 · sin comparación entre olas.

## 6 · Congelamiento

`data/corrida0/CALC-ENVIPE-U4-2012/spec.yaml` cita el `sha256` de este archivo;
`medidor.py` se congela en el mismo commit y **no se edita después**.

**El primer resultado que produzca este procedimiento es el que se reporta.**
