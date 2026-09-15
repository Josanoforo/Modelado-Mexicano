# ENVIPE-2012-U4 · v1.1 — enmienda hacia adelante: el estrato de diseño de la persona seleccionada se toma de `Tmod_Vic.DBF`, porque el `EST` de `tper_vic.dbf`/`tsdem.DBF` no es el estrato de diseño

### `prereg-caja-ENVIPE-2012-U4` · **v1.1** · 14 de septiembre de 2026 · sucesora de `v1.0` (`sha256 4742880b…`), que **no se edita**

**Acto:** `ACTO GEN2-LOTE-MEDICION-PENDIENTE-1` · pieza **P2** (`NC-0099`), COMMIT-3 de la pieza (D-11: «se corrige hacia adelante en un COMMIT-3 propio de esa pieza — nunca reescribiendo»).
**Corrida:** `data/corrida0/CALC-ENVIPE-U4-2012-v1_1/` · **Corrida v1.0 (intacta, sellada):** `data/corrida0/CALC-ENVIPE-U4-2012/`.

> **CONGELADA ANTES DE CORRER EL MEDIDOR v1.1.** Al escribirla la sesión ya
> había leído **todos** los `RESULT` de `CALC-ENVIPE-U4-2012` (v1.0) y, para
> atribuir el hallazgo, la distribución de `EST` en las tres tablas (4 valores
> en `tper_vic`/`tsdem`, 361 en `Tmod_Vic`), que `Tmod_Vic` trae un solo par
> `(EST, UPM)` por hogar (0 hogares con más de uno, de 19 648) y que su `UPM`
> coincide con el de `tper_vic` en los 19 648. **Lo desconocido:** la anchura
> del IC de `U4` bajo el estrato de diseño verdadero. El punto no puede
> cambiar (mismo `U4`, mismo `FAC_ELE`, mismo colapso): se declara como
> control con valor esperado.
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

## 1 · El hallazgo que motiva la v1.1 (de la corrida v1.0, sellada)

`CALC-ENVIPE-U4-2012` cerró `CALCULADO` con `G-CONTROL-U1 = REPRODUCE`,
`N-U4 = 9 854` (join a `tsdem`: 9 854 / 0 / 0), `P-C2-U4 = 0.33839682673243365`
— y **`N-ESTRATOS = 4`** con `G-PERFIL-DISENO-PERSONAS =
ESTRATO[len3=311436;bordes_con_espacio=311436]`. El descriptor
(`fd_envipe2012.xls`, hojas `TPer_Viv` y `TSDem`) declara `EST` «Estrato de
diseño muestral, 001 … 303» para las tres tablas; **el archivo lo contradice
en dos**: `tper_vic.dbf` y `tsdem.DBF` traen en `EST` un dígito con dos
espacios (`'1  '`…`'4  '`, 4 valores; por su forma, un estrato
socioeconómico, no el de diseño), y sólo `Tmod_Vic.DBF` trae el estrato de
diseño (`'143'`, `'217'`…, 361 valores). El descriptor documenta una variable
que dos de los archivos no tienen. **El punto v1.0 es válido; su IC está
estratificado por 4 estratos y no por los de diseño**, así que es un IC de
conglomerados con estratificación más gruesa que la del diseño — se conserva
sellado y se sucede.

## 2 · Lo único que cambia respecto de v1.0

- El par de diseño `(EST, UPM)` de cada persona de `U4` se toma de
  **`Tmod_Vic.DBF`, por hogar** (todas las filas del hogar, no sólo las de
  `U1`), con guardia `G-MOD-N-HOGARES-EST-UPM-MULTI` (hogares con más de un
  par; si una persona cae en uno, entra al punto sin diseño,
  `N-U4-DISENO-AMBIGUO`) y `G-N-HOGARES-UPM-DISCORDA-MOD-VS-PER` (hogares
  cuyo `UPM` difiere entre `Tmod_Vic` y `tper_vic`; se cuentan, y la persona
  usa el par de `Tmod_Vic`).
- Se emiten `G-N-EST-DISTINTOS-PERSONAS` (esperado: 4) y
  `G-N-EST-DISTINTOS-MODULO` (esperado: 361) para dejar el hallazgo medido.
- **Control con valor esperado contra v1.0:** `P-C2-U4`, `P-C1-U4`, `N-U4` y
  `MASA-FAC-ELE-U4` deben coincidir exactamente (`G-CONTROL-V1-0 =
  REPRODUCE`); si no, la v1.1 se reporta y no se corrige hacia atrás.
- Todo lo demás (universos, colapso, ruta a `tsdem`, `FAC_ELE` por hogar,
  bootstrap 2 000 réplicas `seed 20260909`, Taylor) es **idéntico** a v1.0.

## 3 · Qué NO cambia

`NC-0099` queda cerrada por la ruta declarada en v1.0 (join a `tsdem` con
cardinalidad 9 854/9 854); v1.1 sólo corrige la fuente del estrato para el IC.
Ninguna adopción, `milpa/` intacto, ninguna comparación con 2025.

**El primer resultado que produzca este procedimiento es el que se reporta.**
