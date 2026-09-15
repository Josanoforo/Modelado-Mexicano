# EDER-CORRESIDENCIA-ACTUAL-DISENO · Pre-registro de la re-estimación con diseño muestral de `familia.corresidencia.adulto_familiar_actual` (EDER 2017, ventana ACTUAL, universo Jefe/Cónyuge de `MAESTRA33-C1`)

### `prereg-caja-EDER-CORRESIDENCIA-ACTUAL-DISENO` · **v1.0** · 14 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` · pieza **P1** (`NC-0184`) · CAJA (Ubuntu/WSL2) · base `origin/main = 7de3acb4` (PR #761)
**Encargo:** `forense/encargos/2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1.md` (A.3, verbatim)
**Spec hermana (no se edita):** `forense/prereg-caja/EDER-CORRESIDENCIA-DISENO-spec-v1_0.md` (`sha256 b6c75544…`), corrida `CALC-EDER-0001` (PR #760). Esta spec **hereda su método de varianza byte a byte** y cambia el estimando: ventana ACTUAL y universo Jefe/Cónyuge.
**Sucesor de:** `familia.corresidencia.adulto_familiar_actual` (`ACTO MAESTRA33-C1 · RESPEC-CORRESIDENCIA`, 31/ago/2026, `FP-204`): `p = 0.057531`, `ic95 = [0.051297, 0.063913]` (bootstrap simple de filas, seed 42), `n = 9397`, ponderador `factor` — sellada **sin carga** en `milpa/tramite-ola5-propuesta-v0.yaml:192-210` (`SELLADA-SIN-CARGA`, `MAESTRA38-SELLO-3`); producida por `tools/tasas_base_corresidencia_actual.py` (`sha256 0f4569f8…`) bajo la spec `forense/notas/2026-08-31-c1-respec-corresidencia-spec.md` (`sha256 2c6260fc…`). No releva ninguna `CORR-*`.
**Corrida:** `data/corrida0/CALC-EDER-0002/`

> **CONGELADA EN EL COMMIT-1, ANTES DE LEER UN SOLO VALOR DEL MICRODATO.**
> Lo único abierto al escribirla (E.5): `data/manifiesto.yaml`; la lista de
> miembros del ZIP; la **cabecera** (primera línea) de `persona.csv`,
> `vivienda.csv`, `antecedentes.csv` e `historiavida.csv` y el conteo de líneas
> de los tres primeros; la spec y el script de `MAESTRA33-C1`; la spec sellada,
> el medidor y los `RESULT` de `CALC-EDER-0001`; la entrada de la regla en
> `tramite-ola5-propuesta-v0.yaml`. **Ningún valor de ninguna fila.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

### 0.1 · Lo que el encargo declaró, contrastado

| lo que el encargo declaró | lo real, verificado |
|---|---|
| «P1 = NC-0184: correr el CALC de la spec EDER-CORRESIDENCIA-DISENO-spec-v1_0» | **FALSO en la sustancia.** Esa spec **ya fue corrida** por el mismo PR #760 que la congeló: `data/corrida0/CALC-EDER-0001/` trae `resultados.json` (69 `RESULT`, `A-P = 0.9960856`, `A-REPRODUCE-GEN1 = REPRODUCE`), `sello.json`, `ejecucion.json`, y `corridas.tsv` la lista como `CALC-EDER-0001--0cbaba6cea97 · OFERTA · SELLADA · cuenta_gen2=SI`. `spec.yaml` de esa corrida cita la spec por su `sha256 b6c75544…` (`IN-EDER-SPEC-SELLADA`). |
| «cero corridas la consumen (grep -i corresid en corridas.tsv: 0 coincidencias, 166 filas examinadas — A.13)» | **CIERTO en la letra, falso en el conjunto** (diferencia de conjuntos, no léxico): `corridas.tsv` identifica la corrida por `CALC-EDER-0001`, no por la palabra «corresidencia»; el grep léxico dio 0 porque buscó la palabra equivocada. `grep -c "CALC-EDER" data/corrida0/corridas.tsv` → 1. |
| «Es puro COMMIT-2: el trabajo caro ya está hecho» | **FALSO.** Lo que `NC-0184` pide (texto verbatim de la fila: «re-estimar con diseno (est_dis x upm) la re-especificacion familia.corresidencia.adulto_familiar_actual (MAESTRA33-C1, p=0.057531, n=9397, factor; misma reserva factor vs factor_per) … acto de CAJA sucesor: spec v1.1 o spec hermana con el universo Jefe/Conyuge de C1») es **otro estimando** que la spec v1_0 excluyó explícitamente (§4.2: «no es tasa de fase 1 y queda fuera de este CALC, nombrada como sucesor»). Cerrar `NC-0184` exige **COMMIT-1 nuevo** (esta spec hermana) **y** COMMIT-2. |
| «Cierra la única regla EDER con IC de bootstrap simple» | **CIERTO como objetivo**: tras `CALC-EDER-0001`, `adulto_familiar_actual` es la única regla EDER cuyo IC sigue siendo bootstrap simple de filas. Esta spec es la que lo cierra. |

### 0.2 · Cobertura retroactiva (E.1)

El valor GEN1 (`0.057531`, `n = 9397`) es **control positivo posterior sobre el
punto**, jamás insumo: el medidor lo recibe como parámetro de referencia y sólo
lo usa para `A-DELTA-VS-GEN1`. El IC de C1 (bootstrap simple de filas,
`seed=42`) **no se compara** con ningún IC de esta corrida (A-bis.3).

### 0.3 · Contaminación declarada (ADR-46) — esta corrida NO es ciega

Al congelar, la sesión ya había leído: `p = 0.057531`, `ic95`, `n = 9397`, el
universo y el embudo de C1 (`n_persona_csv_total = 94101`, `n_ego = 16687`,
`n_universo = 9397`, distribución de `parentesco` propio: 41.0 % jefe, 29.0 %
cónyuge…), su reserva sobre `factor_per`; y **todos** los `RESULT` de
`CALC-EDER-0001` (291 `est_dis`, 3 780 `upm` en `U_A`, 3 estratos de UPM
única, perfil `est_dis` ancho 3, `factor_per` sube el punto +0.07 pp en la
tasa de fase 1). **Lo genuinamente desconocido al congelar:** cuántos estratos
y UPM cubre el universo Jefe/Cónyuge de 9 397, cuántos quedan con UPM única,
la anchura del IC de diseño, el signo y tamaño de `factor_per − factor` sobre
**este** estimando, y cuántos ego de C1 carecen de `factor_per`.

---

## 1 · Identidad

### 1.1 · Payload

`eder_2017_eder2017_bases_csv` → `data/raw/eder2017/eder2017_bases_csv.zip`,
`sha256 bcc7eb90c2d016976fd8ba24528ce614bf4db0c29a1e3e0cf674bdfb024de0e3`
(verificado hoy por `sha256sum`), ZIP de 5 miembros en la raíz:
`persona.csv` (58 columnas, 94 101 líneas de datos), `vivienda.csv` (109,
23 548), `antecedentes.csv` (52, 23 831), `historiavida.csv` (200),
`hogar.csv`. Mismo payload y mismo sha que fase 1, C1 y `CALC-EDER-0001`.

### 1.2 · Descriptor, verbatim de la spec de C1 y de la hermana

- `persona.csv[parentesco]`: pregunta B5 «¿Qué es (NOMBRE) del jefe?»
  (`eder2017_fd.pdf`, entrada #8, p. 37): `1=Jefe(a) · 2=Esposa(o)/compañera(o)
  · 3=Hija(o) · 4=Nieta(o) · 5=Nuera o yerno · 6=Madre o padre · 7=Suegra(o) ·
  8=Otro · 9=Sin parentesco`. **Codificado relativo al jefe(a) de hogar, no al
  entrevistado** — el hallazgo que gobierna el universo de C1.
- Diseño (tabla VIVIENDA, FD p. 15, #105-#109): `est_dis` «Estrato de diseño
  muestral» `C (4)` (el archivo lo trae de ancho 3: manda el archivo);
  `upm` `C (5)`; `factor` `N (5)`. `antecedentes.csv[factor_per]` (#52),
  ponderador oficial de las personas de 20-54 (FD §1.1.3; receta R
  `svydesign(id=~upm, strata=~est_dis, weights=~factor_per)`).
- Cabeceras reales: el primer nombre de columna llega con BOM (`ï»¿folioviv`
  bajo latin-1) y se resuelve por sufijo, como C1 y como la hermana.

---

## 2 · El estimando, verbatim de C1 (E.3: mismo estimando, sello viejo intacto)

`tools/tasas_base_corresidencia_actual.py::regla_corresidencia_actual`,
reproducido paso a paso:

1. `vivienda.csv` (`latin-1`, `low_memory=False`): **universo de viviendas** =
   `tipo_adqui` no nulo y distinto de `""` tras `astype(str).str.strip()`;
   `pesos_hogar = factor` indexado por `folioviv`.
2. `historiavida.csv`: el conjunto `ids_eder` de ternas
   `(folioviv, foliohog, id_pobla)` (como texto `strip`) — el universo
   respondiente EDER (20-54). Sólo se leen las tres columnas de llave.
3. `persona.csv`: `parentesco` como texto `strip`; `_hogar = (folioviv,
   foliohog)`. **Por hogar, sobre el roster COMPLETO (todas las edades, sin
   restringir a `ids_eder`)**: `_hay_cod6` = algún integrante con `parentesco
   == '6'`; `_hay_cod7` = alguno con `'7'`.
4. **Ego** = filas de `persona.csv` cuya terna está en `ids_eder` **y** cuyo
   `parentesco ∈ {'1','2'}`.
5. Desenlace: `ascendiente = (jefe ∧ _hay_cod6) ∨ (cónyuge ∧ _hay_cod7)`;
   `suegro = (jefe ∧ _hay_cod7) ∨ (cónyuge ∧ _hay_cod6)`; `d = 1` si
   `ascendiente ∨ suegro`, `0` en otro caso. (Un ego cuenta también si el
   código 6/7 lo porta… otro ego del mismo hogar: la regla es «existe algún
   otro integrante», y C1 la implementó sobre el hogar completo, incluido
   quien no es ego. Se reproduce tal cual.)
6. `peso = factor` de la vivienda del `folioviv` del ego (`map`); ego sin peso
   (vivienda fuera del universo) **sale** (`dropna`).
7. `p = Σ peso·d / Σ peso`.

**El universo, el ponderador, la codificación y el colapso NO cambian.** Lo
que esta corrida añade es (a) la varianza de diseño y (b) la sensibilidad
`factor_per` que C1 dejó **declarada y no ejecutada** («se deja para mesa o un
acto sucesor decidir»).

---

## 3 · Método — heredado byte a byte de la hermana

### 3.1 · Llaves opacas y unión con el diseño

`est_dis` y `upm` como **texto crudo** (`dtype=str`), unidos a cada ego por
`folioviv` desde `vivienda.csv`. Perfiles `G-PERFIL-EST-DIS`/`G-PERFIL-UPM`,
`G-UPM-ANIDA-EN-EST-DIS`. Clave de conglomerado `(est_dis, upm)`.

### 3.2 · Varianza de diseño

**Primaria (`A-IC-LO`/`A-IC-HI`):** bootstrap de `upm` con reemplazo dentro de
`est_dis`, conservando el número de UPM por estrato, **2 000 réplicas**,
percentiles 2.5/97.5, `seed = 20260914`, `numpy.PCG64`. Estrato con una sola
UPM: se re-muestrea a sí mismo, **no se colapsa, no se descarta**; si
`A-N-ESTRATOS-UPM-UNICA > 0`, `A-METODO-IC = IC-CON-ESTRATOS-DE-UPM-UNICA` y el
IC es **límite inferior** de la anchura verdadera. Sin diseño en toda `U` →
`NO-ESTIMABLE-DISENO-INCOMPLETO`, IC `null`, punto reportado igual.

**Secundaria (`A-EE-TAYLOR`, `A-IC-*-TAYLOR`):** linealización de Taylor con
la aproximación declarada de `survey.lonely.psu="adjust"`, idéntica a la
hermana. No se adopta.

### 3.3 · Sensibilidad de ponderador (`B-*`) — la reserva de C1, ejecutada y no adjudicada

Mismos ego que `A` (con `factor` presente), mismo desenlace, peso `factor_per`
de `antecedentes.csv` por la terna. Sin `factor_per`, no finito o `≤ 0` →
fuera de `B`, contados (`B-N-SIN-FACTOR-PER`, `B-N-FACTOR-PER-CERO`,
`B-N-FACTOR-PER-INVALIDO`). Misma varianza que `A`. `B-DELTA-VS-A` con signo.
**No hay cláusula `se_mueve_si` escrita por mesa para esta regla** (la entrada
`:192-210` trae `situacion: SELLADA-SIN-CARGA` sin cláusula): por eso **no se
emite ningún `RESULT` de cláusula** — inventarla sería adjudicar. La lectura
del delta es de mesa.

### 3.4 · Guardias — paran, no adivinan

- **G-1 miembros:** falta `persona.csv`, `vivienda.csv`, `historiavida.csv` →
  `NO-ESTIMABLE-MIEMBRO-AUSENTE:<m>`; falta `antecedentes.csv` → sólo `B` cae.
- **G-2 columnas:** falta cualquiera de `folioviv`(sufijo), `tipo_adqui`,
  `factor`, `est_dis`, `upm` (vivienda); `folioviv`, `foliohog`, `id_pobla`,
  `parentesco` (persona); `folioviv`, `foliohog`, `id_pobla` (historiavida);
  `factor_per` (antecedentes) → `NO-ESTIMABLE-COLUMNA-AUSENTE:<col>`.
- **G-3 llaves:** `folioviv` único en `vivienda.csv`; la terna única en
  `persona.csv` (si no, `A` y `B` → `NO-ESTIMABLE-LLAVE-NO-UNICA`) y en
  `antecedentes.csv` (si no, sólo `B`).
- **G-4 embudo de C1 como guardia con valor esperado** (premisa ajena escrita
  como guardia, no heredada): `G-N-FILAS-PERSONA` (esperado 94 101),
  `G-N-PERSONAS-HISTORIAVIDA` (23 831), `A-N-EGO-JEFE-O-CONYUGE` (16 687),
  `A-N-U` (9 397). Si alguno difiere el estimando **no se ajusta**: el conteo
  se reporta y `A-EMBUDO-C1` sale `EMBUDO-DISCORDA:<cual>`; `REPRODUCE`
  sigue decidiéndose sólo por el punto.
- **G-5 catálogo de `parentesco`:** conteo de valores fuera de `{'1'..'9'}`
  (`G-N-PARENTESCO-FUERA-DE-CATALOGO`); si hay, se reporta y no se imputa.
- Universo vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`. **Cero nunca sustituye falta
  de dato.**

---

## 4 · Ramas pre-declaradas

### 4.1 · Control positivo contra GEN1 (punto, no IC)

| celda | valor GEN1 (`propuesta-v0:196`, `:207`) | `RESULT` |
|---|---|---|
| `A-P` | `0.057531` | `A-DELTA-VS-GEN1`; `A-REPRODUCE-GEN1 ∈ {REPRODUCE (|Δ| ≤ 1e-6), NO-REPRODUCE}` |
| `A-N-U` | `9397` | `A-DELTA-N-VS-GEN1` |

`NO-REPRODUCE` no invalida, no autoriza tocar el medidor y no se ajusta hacia
atrás: se reporta con el embudo y se atribuye. Complemento contado
directamente (`A-P-COMPLEMENTO`), nunca `1 − p`; `A-SUMA` prueba exhaustividad.

### 4.2 · Adopción

El único consumidor (`tramite-ola5-propuesta-v0.yaml:192`, `SELLADA-SIN-CARGA`,
archivo que el motor no carga) **no tiene cita GEN2 vigente**. Este acto **no
escribe en `milpa/`**. `A-ADOPCION ∈ {LISTADO-PARA-MESA-REPRODUCE,
LISTADO-PARA-MESA-NO-REPRODUCE, NO-ADOPTABLE-NO-ESTIMABLE}`.

### 4.3 · Qué cambia y qué no

Si los controles pasan: **el punto no cambia**; cambia la varianza (de
bootstrap simple de filas a bootstrap de UPM dentro de estrato). La lectura de
C1 («5.75 % vs 99.6 % no es discordancia: incidencia acumulada vs prevalencia
puntual, más el recorte de universo») no se toca.

---

## 5 · Estimando

**DESCRIPTIVO.** Ningún `RESULT` es causal.
- **Sucesor (adoptable por mesa):** `A-P` con `A-IC-LO`/`A-IC-HI`.
- **Secundarios declarados:** `A-P-COMPLEMENTO`, Taylor, familia `B`
  (sensibilidad `factor_per`, **no** sucesor: cambia el estimando), perfiles y
  embudo.

## 6 · Límites declarados

Una sola ola (EDER 2017) · IC como límite inferior si hay estrato de UPM única ·
`factor` es ponderador de vivienda (ENH) y `factor_per` el oficial de persona:
el sucesor hereda `factor` por E.3, `factor_per` va como `B` · universo
Jefe/Cónyuge = 70 % de los respondientes (restricción del instrumento, C1 §2)
· el componente «hermanos» de la ventana «alguna vez» **no tiene análogo** en
la ventana actual (C1 §2) · A-bis.3 · contaminación §0.3 · causalidad: ninguna.

## 7 · Congelamiento

`data/corrida0/CALC-EDER-0002/spec.yaml` es la cara mecánica y cita el
`sha256` de este archivo; `medidor.py` se congela en el mismo commit y **no se
edita después** — si resultara equivocada, se escribe una `v1.1` fechada.

**El primer resultado que produzca este procedimiento es el que se reporta.**
