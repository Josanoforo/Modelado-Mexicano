# `CALC-ENIF-0001` — cara mecánica

Gobernado por la spec **SELLADA**
`forense/prereg-caja/ENIF-AHORRO-spec-v1_0.md`
(`prereg-caja-ENIF-AHORRO`, v1.0, 9/sep/2026). Donde este archivo y aquél
difieran, manda aquél.

**Acto:** `ACTO GEN2-LOTE-ENIF-1`, 9/sep/2026, CAJA (Ubuntu), sobre `0f62668`.
**Releva:** `CORR-0009` (ENIF2024) → los **8** `RESULT` que el encargo nombra:
`RES-0046`…`RES-0049` (familia A), `RES-0057`/`RES-0058` (familia B),
`RES-0059`/`RES-0060` (familia C).
**NO releva** `RES-0031`/`RES-0032` (misma corrida, sellados por
`ACTO MAESTRA35-N1`): fuera del encargo, van a `## NO-CORRIDO`.

**CONGELADO en el COMMIT-1, antes de abrir un solo `*.csv` del microdato.**

---

## Qué mide

Tres mecanismos financieros que **coexisten** y **no comparten denominador**,
todos sobre `TMODULO.csv` (unidad: la persona elegida, 18 años y más,
ponderador `FAC_PER`):

- **A · horizonte de ahorro** (`P4_10`), dentro del eje de seguridad social
  (`P3_13`). Dos celdas, **dos denominadores**.
- **B · vía de ahorro** (`P5_1_*` informal, `P5_6_*` formal). **Un solo
  denominador compartido — el único de esta spec — y las dos tasas COEXISTEN.**
- **C · desconfianza como razón de no tener cuenta** (`P5_20 = '03'`), partida
  por el conocimiento de la protección de depósitos (`P5_23`). Dos celdas,
  **dos denominadores**.

## Las cuatro premisas del encargo que esta spec corrige

1. La plaza es **`CORR-0009`**, no `CORR-0017` (que es ENSANUT, 2 `RESULT`).
2. La población es **18 y más** (`EDAD_V = 18-95`), no 18-70.
3. El conocimiento de la protección (`5.23`) va **DESPUÉS** de la razón
   (`5.20`), no antes: `5.20 → PASE A 5.23`.
4. El denominador de la familia C **no** es «sólo quienes conocen»: es la
   población **sin cuenta**, **partida en dos** por `P5_23`.

Ninguna bloquea. Las dos últimas van además como **guardias que PARAN**
(`G-C1`, `G-C2`), porque son premisas ajenas sobre el dato.

## Lo que esta spec decide y GEN1 no

- **El corte de «corto»:** primario `P4_10 ∈ {1,2}` (menos de un mes, la
  frontera que el propio reactivo nombra). Sensibilidad `S1`: `P4_10 = {1}`
  — que **es el corte de GEN1**, y esta sesión lo sabía (contaminación
  declarada, §0.3 de la spec sellada). Se reporta el primario.
- **Qué es seguridad social:** `P3_13 ∈ {1,2,3,4}` (IMSS, ISSSTE, ISSSTE
  estatal, PEMEX/Defensa/Marina). El `5` es seguro **privado** y no lo es;
  el `6` el descriptor no lo resuelve; ambos, más el `9` y el `b`, salen del
  par **con su peso medido**.
- **El diseño:** `FP-201` decía que ENIF no tenía campo de diseño
  reproducible. **Es falso:** `EST_DIS`, `UPM_DIS` y `FAC_PER` están en
  `TMODULO`. Esta corrida los usa. Cierra la parte ENIF de `NC-0086`.

## Diseño

Punto `p̂ = Σ FAC_PER·1[num] / Σ FAC_PER·1[den]`, sumas en orden fijo de fila.
IC por **bootstrap de `UPM_DIS` con reemplazo dentro de `EST_DIS`**,
`B = 1000`, semilla `20260909`, percentiles 2.5/97.5.
`EST_DIS`/`UPM_DIS` se agrupan como **cadena cruda** — son llaves opacas, y
convertirlas a entero fusiona estratos en silencio.

⚠️ **A-bis.3:** fase 1 midió **sin** diseño. Los IC de esta corrida y los de
fase 1 **no son comparables y no se comparan.** El control positivo compara
**sólo el punto**.

## Control positivo y adopción

`REPRODUCE-GEN1` corre **después** de sellar, por script separado
(`forense/prereg-caja/ENIF-AHORRO-control-gen1.py`), y no puede tocar el
medidor. `REPRODUCE` si `|medido − sellado| ≤ 1e-6`.

**Se espera `NO-REPRODUCE` en la familia A y la razón está escrita antes de
correr:** el corte primario difiere del de GEN1. `S1` existe para que la
discrepancia sea atribuible.

Adopción P3: sólo las **cantidades genuinamente medidas** reciben cita
`corrida0_*` en `milpa/tramite.yaml`. Los complementos de §5.2 de la spec
sellada van **sin cita** y con fila `NC` de advertencia (patrón `NC-0085`).

## Lo que NO hace

- **Nada causal.** `P4_10`, `P5_1_*`, `P5_6_*`, `P5_20`, `P5_23` son
  declaraciones del informante. `P3_13` no es asignación aleatoria: comparar
  celdas de la familia A es **descripción**.
- **No fuerza a sumar 1** `RES-0057` + `RES-0058`. Si suman más de 1, eso es
  coexistencia, no defecto.
- **No suma** `RES-0059` + `RES-0060`: son tasas condicionales a celdas
  ajenas.
- No mide ENCUCI. No toca marcador, capturas ni `CALC-R`. No toca
  `RES-0031`/`RES-0032`.
