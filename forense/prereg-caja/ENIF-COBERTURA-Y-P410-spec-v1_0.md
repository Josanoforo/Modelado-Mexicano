# ENIF-COBERTURA-Y-P410 · Pre-registro de (P3) la reconciliación de la «cobertura 66.89 %» de GEN1 contra la remedición del lote ENIF-1 y (P4) la descomposición interna de la categoría colapsada `P4_10 = 1`

### `prereg-caja-ENIF-COBERTURA-Y-P410` · **v1.0** · 14 de septiembre de 2026

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` · piezas **P3** (`NC-0125`) y **P4** (`NC-0126`), una sola corrida (D-15: un lote es una corrida coherente) · CAJA (Ubuntu/WSL2) · base `origin/main = 7de3acb4`
**Encargo:** `forense/encargos/2026-09-14-GEN2-LOTE-MEDICION-PENDIENTE-1.md` (A.3)
**Specs que no se editan:** `forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md` (`sha256 697ab9e8…`, `CALC-ENIF-0001`, PR #667) y `forense/notas/2026-09-02-MAESTRA35-L7-spec.md` (GEN1, `MAESTRA35-L7`).
**Corrida:** `data/corrida0/CALC-ENIF-0003/`

> **CONGELADA EN EL COMMIT-1, ANTES DE LEER UN SOLO VALOR DEL MICRODATO.**
> Lo único abierto al escribirla (E.5): `data/manifiesto.yaml`; la lista de
> miembros del ZIP y la **primera línea** de `TMODULO.csv`; `enif_2024_fd.xlsx`
> (hoja `TMODULO`, texto de 4.10, 5.1, 5.4, 5.6); la spec sellada, el
> `spec.yaml`, el medidor y los `RESULT` de `CALC-ENIF-0001`/`0002`; el log
> GEN1 `data/l7-log-pieza-d.txt`, `tools/medidor_horizonte_enif24.py`,
> `tools/medidor_ahorro_enif24.py`, las notas de `MAESTRA35-L7` y la historia
> git de `milpa/tramite.yaml:1082,1112`. **Ningún valor de ninguna fila.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

---

## 0 · Premisas verificadas contra el árbol

| lo que la fila / el encargo declaró | lo real, verificado |
|---|---|
| `NC-0125`: «el script de fase 1 no existe en el arbol (script_legacy = NO-DECLARADO-EN-EL-REGISTRO …)» | **FALSO.** El script GEN1 existe: `tools/medidor_horizonte_enif24.py` (`ACTO MAESTRA35-L7`, pieza d), y su salida cruda está archivada en `data/l7-log-pieza-d.txt` (commit `0ce351f`, 2/sep/2026). Lo que no existe es la **cita** en `demanda-resultados.tsv` (`script_legacy` vacío). |
| «fase 1 declaró 66.89 %» | **CIERTO en `milpa/tramite.yaml:1082,1112`** (`historico_gen1.definicion: "… cobertura declarada 66.89%"`), escrito por `ACTO MAESTRA35-N8 · SELLA-L7` (commit `b434770`, 3/sep) en la `clase` de las cuatro conductas; hoy conservado como histórico por `c11e0c7` (10/sep). **Pero el propio L7 declaró 68.97 %** para la cobertura de `P3_13` (`data/l7-log-pieza-d.txt:14`: «válidos 1-7: 9,312 de 13,502 = 68.9676%»; spec L7 §d; `propuesta-v0.yaml:2172` «cobertura 68.97% coincide exacto con la ya declarada por L1»). Y el mismo log trae **otra** cifra: «universo triple (ahorro-elegible ∧ P3_13 válido ∧ P4_10 válido): n = 9,031 de 13,502» — **9 031 / 13 502 = 0.66886 → 66.89 %**. La entrada `propuesta-v0.yaml:2169` escribe `cobertura: 0.668937` con `universo: "… n = 9 031 de 13 502"`. |
| «la corrida mide 67.53 / 68.06» | CIERTO: `2026-09-09-GEN2-LOTE-ENIF-1-cierre.md:112`; `CALC-ENIF-0001` `A-C-SIN-EJE-BLANCO-FRACCION = 0.319422` (ponderada, denominador «personas 18+ con FAC_PER valido»), y `1 − 0.319422 = 0.680578` → 68.06 %. |

### Hipótesis pre-registrada (P3), escrita antes de abrir el dato

**H1 (documental, sale del árbol):** la «cobertura 66.89 %» que N8 selló **no es
la cobertura de `P3_13`** (68.97 % sin ponderar) **ni la ponderada que midió el
lote** (67.53 % / 68.06 %): es la fracción **no ponderada** del **universo
triple** de la pieza d de L7 (`P3_13 ∈ {1..7} ∧ P4_10 ∈ {1..5}`) sobre las
13 502 filas de `TMODULO`: 9 031 / 13 502. Las tres cifras son cantidades
distintas (numerador distinto, ponderación distinta), no un residuo de medición.
**Lo que la corrida verifica** es el recuento: si `C-N-UNIVERSO-TRIPLE = 9031`
y `C-N-TMODULO = 13502`, H1 queda **REPRODUCIDA** y `NC-0125` cierra como
«reconciliada por definición»; si no, se reporta el conteo real y H1 cae. La
sexta cifra de `0.668937` se contrasta contra las dos variantes candidatas
(no ponderada, ponderada `FAC_PER`) y se declara cuál la reproduce, o ninguna.

### Contaminación (ADR-46)

La sesión leyó todos los `RESULT` de `CALC-ENIF-0001`/`0002` y el log GEN1
(conteos de `P4_10` por código: 4275/2443/3405/1328/1479/74/498; 9 312;
9 031). **Lo desconocido al congelar:** todo lo de P4 — cuántas personas con
`P4_10 = 1` no ahorraron por ninguna vía en 12 meses, y la misma fracción en
los demás códigos y en los universos del lote.

---

## 1 · Identidad

`enif_2024_enif_2024_bd_csv` → `data/raw/enif_2024_bd_csv.zip`, `sha256
00e4b0b42775276b2da236a5bba8c64dc5a92c289908a4727dec93dc7684f039`, miembro
`TMODULO.csv` (unidad: persona elegida 18+, `FAC_PER`, `EST_DIS`, `UPM_DIS`).
Lectura idéntica a `CALC-ENIF-0001`: `utf-8-sig` con caída a `latin-1`
declarada, toda celda como cadena, llaves opacas.

Reactivos (FD hoja `TMODULO`): **4.10** «Si usted dejara de recibir ingresos,
¿por cuánto tiempo podría cubrir sus gastos con sus ahorros?» `P4_10`:
`1 = Menos de una semana / No tiene ahorros · 2 = al menos una semana pero
menos de un mes · 3 · 4 · 5 = seis meses o más · 8 = No responde · 9 = No sabe`
(sin `b`: se pregunta a toda la población). **5.1** `P5_1_1..6` «En los
últimos 12 meses … ¿usted ahorró … (prestando dinero / comprando animales o
bienes / caja de ahorro del trabajo o de conocidos / …)?» `1 = Sí, 2 = No`
(sin `b`). **5.6** `P5_6_1..9` «De junio de 2023 a la fecha, ¿usted guardó o
ahorró en su (nómina / pensión / apoyos / cuenta de ahorro / cheques / plazo
fijo / fondo de inversión / cuenta digital / otra)?» `1 = Sí, 2 = No, b =
blanco por secuencia (no tiene esa cuenta)`. **3.13** `P3_13` como en la spec
sellada (`{1..6}` con derecho, `7` sin, `9` NS, `b` por secuencia).

---

## 2 · P3 — reconciliación de cobertura (recuento, sin ponderar y ponderado)

Sobre las filas de `TMODULO.csv` (`C-N-TMODULO`; L7: 13 502) y sobre las que
tienen `FAC_PER` finito `> 0` (`C-N-FAC-PER-VALIDO`; `CALC-ENIF-0001`: 0 sin
ponderador):

| `RESULT` | definición | valor GEN1/lote que se contrasta |
|---|---|---|
| `C-N-P3-13-1-7` | filas con `P3_13 ∈ {1..7}` | 9 312 (log L7) |
| `C-FRAC-P3-13-1-7-NO-PONDERADA` | `C-N-P3-13-1-7 / C-N-TMODULO` | 0.689676 → 68.97 % |
| `C-FRAC-P3-13-1-7-PONDERADA` | `Σ FAC_PER[P3_13∈{1..7}] / Σ FAC_PER` | 67.53 % (lote) |
| `C-FRAC-P3-13-1-7-9-PONDERADA` | idem con `{1..7, 9}` | 0.680578 (= 1 − 0.319422) |
| `C-N-UNIVERSO-TRIPLE` | filas con `P3_13 ∈ {1..7} ∧ P4_10 ∈ {1..5}` | 9 031 (log L7) |
| `C-FRAC-UNIVERSO-TRIPLE-NO-PONDERADA` | `9031-candidato / C-N-TMODULO` | **66.89 % (H1)** |
| `C-FRAC-UNIVERSO-TRIPLE-PONDERADA` | `Σ FAC_PER[triple] / Σ FAC_PER` | candidato alterno de `0.668937` |

Veredictos mecánicos, pre-declarados: `C-VEREDICTO-68-97 = REPRODUCE` si
`round(100·frac_1_7_np, 2) == 68.97`; `C-VEREDICTO-67-53` idem con la
ponderada; `C-VEREDICTO-68-06` idem con `{1..7,9}` ponderada;
`C-VEREDICTO-66-89 ∈ {LOCALIZADA:UNIVERSO-TRIPLE-NO-PONDERADA,
LOCALIZADA:UNIVERSO-TRIPLE-PONDERADA, LOCALIZADA:<otra de la tabla>,
NO-LOCALIZADA}` según cuál(es) de las siete fracciones redondee a 66.89 (se
listan todas las que calcen, separadas por `;`); `C-VEREDICTO-0-668937 ∈
{REPRODUCE:NO-PONDERADA, REPRODUCE:PONDERADA, NO-REPRODUCE}` a 6 decimales.
`C-VEREDICTO-H1 = REPRODUCIDA` si `C-N-UNIVERSO-TRIPLE == 9031 ∧ C-N-TMODULO
== 13502`; `REFUTADA` en otro caso. Además `C-N-P4-10-<k>` para `k ∈
{1,2,3,4,5,8,9}` como guardia con valor esperado (log L7).

## 3 · P4 — descomposición interna de `P4_10 = 1`

**Proxy declarado, con su límite escrito antes del dato:** «no ahorró por
ninguna vía en los últimos 12 meses» ≡ `P5_1_1..6` todas `≠ '1'` **y**
`P5_6_1..9` todas `≠ '1'` (`'2'` y `'b'` cuentan como no). Es el mejor
indicador interno de «no tiene ahorros» que trae ENIF 2024, y **no es
equivalente**: alguien pudo ahorrar antes de junio de 2023 y conservarlo, o
ahorrar y gastarlo. Por eso todo `RESULT` de P4 se lee como **cota** de la
fracción de «no tiene ahorros» dentro del código 1, nunca como su valor.
`FILTRO_S5_1` no se usa como filtro (la spec sellada ya midió 0
discrepantes).

Universos, todos con `FAC_PER` finito `> 0`:
- `D0_k` = filas con `P4_10 = k`, `k ∈ {1, 2, 3-5}`: `D-P-NINGUNA-VIA-EN-<k>`
  (proporción ponderada, IC de diseño para `k = 1`), `D-N-<k>`,
  `D-N-NINGUNA-VIA-EN-<k>`. El contraste entre `k = 1` y `k = 2` es la lectura
  central: si el código 1 está dominado por no-ahorradores y el 2 no, el
  colapso muerde.
- `U_A_SIN` (`P3_13 = '7' ∧ P4_10 ∈ {1..5}`) y `U_A_CON` (`P3_13 ∈ {1,2,3,4} ∧
  P4_10 ∈ {1..5}`), los universos del lote: `D-P-P410-1-NINGUNA-VIA-<SIN|CON>`
  = proporción ponderada del universo que es `P4_10 = 1 ∧ ninguna vía` (la
  parte del corte `S1 = {1}` y del primario `{1,2}` atribuible a
  no-ahorradores, en puntos de proporción del universo);
  `D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-<SIN|CON>` = entre quienes tienen
  `P4_10 = 1` en ese universo, la fracción ponderada sin ninguna vía;
  `D-FRAC-DE-CORTO-12-QUE-ES-P410-1-NINGUNA-VIA-<SIN|CON>` = entre quienes
  tienen `P4_10 ∈ {1,2}`, la fracción que es `1 ∧ ninguna vía`.

IC: bootstrap de `UPM_DIS` dentro de `EST_DIS`, 1 000 réplicas (como
`CALC-ENIF-0001`), percentiles 2.5/97.5, `seed 20260909`, `numpy.PCG64`;
estrato de UPM única se re-muestrea a sí mismo (límite inferior). Sólo se
emite IC para `D-P-NINGUNA-VIA-EN-1`, `D-P-NINGUNA-VIA-EN-2` y las dos
`D-FRAC-DE-P410-1-QUE-ES-NINGUNA-VIA-*`; el resto son puntos y conteos.

**Qué NO hace P4:** no cambia ningún corte, no re-estima ningún `RESULT` del
lote, no adjudica. La adjudicación de `NC-0126` («¿se mantiene el corte con
el 1 dentro, se mueve a `S1`, o se pide otro reactivo?») es de mesa, con
estas cotas a la vista.

## 4 · Guardias

Miembro/columna ausente → `ESTADO = NO-ESTIMABLE-*`. `P4_10` o `P3_13` con
código fuera de dominio → contado (`G-N-FUERA-DE-DOMINIO-*`), no imputado.
Filas sin `FAC_PER` válido → contadas, fuera de las ponderadas, dentro de los
recuentos no ponderados. Universo vacío → `NO-ESTIMABLE-UNIVERSO-VACIO`.
**Cero nunca sustituye falta de dato.**

## 5 · Estimando

**DESCRIPTIVO.** Ningún `RESULT` es causal, ninguno adopta, `milpa/` no se toca.

## 6 · Congelamiento

`data/corrida0/CALC-ENIF-0003/spec.yaml` cita el `sha256` de este archivo;
`medidor.py` se congela en el mismo commit y **no se edita después**.

**El primer resultado que produzca este procedimiento es el que se reporta.**
