# `ACTO MAESTRA35-L6 · FUENTE-COERCITIVO-Y-PUENTE` — `COMMIT-2` · resultados

**2 de septiembre de 2026.** Ejecuta la spec congelada en
`forense/notas/2026-09-02-MAESTRA35-L6-spec.md` (`COMMIT-1`, commit `f77df14`),
que no se toca. **El primer resultado que produjo el procedimiento es el que se
reporta aquí**, incluido el que salió mal.

---

## §1 · `P1` · Adopción de trámites de gobierno por internet — ENDUTIH

`tools/medidor_gobierno_digital_endutih.py`. Estimador `wprop_ic_conglomerado`
(`n_boot=10000`, `seed=42`), ponderador `FAC_PER`, diseño `EST_DIS`×`UPM_DIS`.

**La guardia 3 de la spec pasó en las tres olas**, y eso es un resultado: el
universo de `P7_35_4` **coincide exacto** con `P7_1 == '1'` en 2023, 2024 y 2025
—cero filas con dato fuera del universo, cero filas en el universo sin dato—.
La premisa que el censo había medido en dos olas se escribió como guardia que
PARA, no como supuesto heredado, y la tercera ola la confirmó sola.

### Principal — `P7_35_4` («¿ha utilizado internet para realizar trámites del gobierno?»), universo `P7_1='1'`

| ola | papel | `p` | `IC95` | `n` | numerador | estratos | UPM | pob. expandida |
|---|---|---|---|---|---|---|---|---|
| **2025** | **PRINCIPAL** | **`0.207026`** | `[0.201085, 0.213148]` | 48 718 | 9 221 | 425 | 8 594 | 104 903 990 |
| 2024 | sensibilidad de ola | `0.171684` | `[0.166258, 0.177222]` | 47 240 | 8 163 | 437 | 8 741 | 100 249 527 |
| 2023 | sensibilidad de ola | `0.177463` | `[0.171968, 0.182858]` | 46 631 | 8 062 | 341 | 8 216 | 97 012 089 |

`sha256` de los payloads: 2025 `a927528779c56b45…`, 2024 `ef723ed125c81c4a…`,
2023 `29d195082796c269…` (completos en `data/l6-gobierno-digital-endutih-v1_0.json`).

### Sensibilidades pre-declaradas

| ola | `A` · unión `P7_35_1..4` (cualquier interacción) | `B` · universo ampliado (no usuarios = no adopción) |
|---|---|---|
| 2025 | `0.357185` `[0.350124, 0.364140]`, n=48 718 | `0.178152` `[0.172724, 0.183700]`, n=57 810 |
| 2024 | `0.329487` `[0.322545, 0.336408]`, n=47 240 | `0.142708` `[0.138120, 0.147342]`, n=58 080 |
| 2023 | `0.332377` `[0.325704, 0.338970]`, n=46 631 | `0.144070` `[0.139654, 0.148576]`, n=58 922 |

### Qué se lee, y qué no

**Uno de cada cinco usuarios de internet hizo un trámite de gobierno en línea en
2025** (`20.70 %`), y **la cifra subió**: el `IC95` de 2025 no se traslapa con el
de 2024 (`17.17 %`) ni con el de 2023 (`17.75 %`), y 2023 y 2024 sí se traslapan
entre sí. El salto es de la ola más reciente, no una tendencia de tres puntos.
Las tres sensibilidades `B` reproducen el mismo orden sobre la población de
informantes (`14.41 % → 14.27 % → 17.82 %`).

**La brecha entre *interactuar* y *tramitar* es de más de 15 puntos** en las tres
olas (2025: `35.72 %` contra `20.70 %`). Consultar información y descargar
formatos es mucho más frecuente que cerrar un trámite: quien mida «gobierno
digital» con la batería completa está midiendo otra cosa, y por casi el doble.

**Esto NO es la `p` de `tramite.gobierno_digital.coercitivo`.** El censo `P0` §3
estableció por qué, y `ADR-287` sigue en pie: la situación coercitiva no está en
el instrumento.

**Y NO se compara con el `0.673393` de `util_sin_coercion`.** Aquella cifra tiene
unidad **trámite** (no persona) y universo **`N_TRA=01`, pago del recibo de luz**
en ENCIG 2025; ésta tiene unidad **persona** y universo **usuarios de internet**
en ENDUTIH. Son dos cantidades distintas y ponerlas una junto a otra sería el
error de unidad contra el que `forense/ficha-r34-condBC-v1_0.md` ya advirtió.
Lo que esta cifra sí hace es **llenar la reserva que el propio motor tiene
escrita**: la `estampa A.10` de `util_sin_coercion` dice, verbatim, *«No es la
adopción de gobierno digital en México»*. Ahora esa adopción está medida, con
diseño completo y en tres olas. **Cómo se lea contra el prior es de mesa.**

---

## §2 · `P2` · Respaldo personal × adopción de producto formal — ENIF 2024

`tools/medidor_puente_enif24.py`. Payload `enif_2024_bd_csv.zip::TMODULO.csv`,
`sha256` en `data/l6-respaldo-enif2024-v1_0.json`. Universo **13 502** personas
18+. Eje `P4_9_4`: **respaldo=SÍ `3 145`** · **respaldo=NO `10 357`** ·
**fuera de eje `0`** — el eje cubre el universo completo, que es exactamente por
lo que se eligió sobre `P5_15_2`.

| desenlace | papel | respaldo=SÍ | respaldo=NO | brecha | `IC95` sin traslape | veredicto `B-bis` |
|---|---|---|---|---|---|---|
| `D1` ahorro formal (`P5_6_*`) | **PRINCIPAL** | `1.000000` `[1.0, 1.0]` n=1 113 | `1.000000` `[1.0, 1.0]` n=2 965 | `+0.0000` pp | no | **`NO-DISCRIMINA`** |
| `D2` tenencia de cuenta (`P5_4_*`) | secundario | `0.643963` `[0.620270, 0.667835]` n=3 145 | `0.658929` `[0.645542, 0.672644]` n=10 357 | `−1.4966` pp | no | `NO-DISCRIMINA` |
| `D3` crédito formal (`P6_2_*`) | secundario | `0.397447` `[0.374806, 0.420250]` n=3 145 | `0.342561` `[0.330049, 0.355527]` n=10 357 | **`+5.4886` pp** | **sí** | **`CORROBORADA`** |

**Sensibilidad `C` (control de riqueza declarada, `P4_9_1`)**: ambos estratos
`NO-DISCRIMINA` con brecha `+0.0000` — pero corre sobre `D1`, que está
defectuoso (§2.1), así que **no informa nada** y se reporta sólo para dejar
constancia de que se corrió.

**Veredicto del acto, derivado por código y no a ojo**: `NO-DISCRIMINA`
(precedencia sobre `D1`, que es el principal).

### §2.1 · `D1` salió degenerado, y la spec es la culpable — no se corrige hacia atrás

`p = 1.000000` en las dos celdas, con `n` de 1 113 y 2 965 sobre un universo de
13 502. Eso no es un resultado: es **un defecto de la spec**, diagnosticado
después de verlo y registrado aquí sin tocar `COMMIT-1`.

**Qué pasó.** La spec §2 definió `D1` con el operador de los otros dos
desenlaces: `1` si alguna `P5_6_i == '1'`, `0` si **todas** valen `'2'`, fuera de
universo en cualquier otro caso. Pero `P5_6_*` **no es una batería de tenencia**:
es la **subpregunta** de `P5_4_*`, y su «no» se codifica **en blanco**, no como
`'2'`. Contado sobre el CSV:

```
P5_4_1 : {'2': 9197, '1': 4305}   -- se pregunta a los 13 502, sin blancos
P5_6_1 : {NaN: 9197, '2': 2461, '1': 1844}   -- 9 197 = exactamente los P5_4_1='2'
```

Al exigir «todas `'2'`» para el cero, el operador se quedó con **4 078** personas
que ya tenían el producto, y ahí la tenencia vale `1` por construcción. Es la
**quinta** vez que este programa tropieza con la misma clase de defecto —una
variable observada sólo dentro del universo que ella misma define— y la primera
en que el tropiezo es del ejecutor y no del instrumento.

**Qué NO pasó.** `D2` (`P5_4_*`) y `D3` (`P6_2_*`) sí se preguntan a las 13 502
personas con `1`/`2` y sin blancos: sus universos son correctos, sus `n` cuadran
exacto con el universo declarado, y **sus resultados se sostienen tal como
salieron**.

**Qué falta, y dónde.** La `D1` correcta —`1` sse alguna `P5_6_i == '1'`, `0` en
cualquier otro caso sobre el universo completo, que es como
`tools/medidor_ahorro_enif24.py` construye la pata formal de
`dinero.ahorro.tiene_ahorros`— se congela en un **tercer commit** y se corre ahí.
`COMMIT-1` no se edita y `COMMIT-2` no se reescribe: ésa es toda la regla.

### §2.2 · Qué se lee de `D2` y `D3`, que sí son válidos

**`D3` · crédito formal: `CORROBORADA`.** Quien declara que podría aprovechar
una oportunidad con el préstamo de familiares o amistades tiene crédito formal
**`39.74 %`** contra **`34.26 %`** de quien no —`+5.49` puntos, `IC95` sin
traslape—. Va en el signo que el bullet predice: **con respaldo, más adopción**.

**`D2` · tenencia de cuenta: `NO-DISCRIMINA`,** y el punto estimado va al revés
(`64.40 %` con respaldo contra `65.89 %` sin), con `IC95` traslapados.

**La lectura que estos dos números soportan, y sus límites.** El respaldo
personal se asocia con el producto que **requiere ser evaluado por un tercero**
—el crédito— y no con el que se abre por ventanilla —la cuenta—. Es congruente
con que el mecanismo del bullet opere donde hay una **puerta que franquear**, y
no donde no la hay; también es congruente con explicaciones que nada tienen que
ver con el bullet (quien tiene red también tiene ingreso, y el ingreso predice
crédito). **Es asociación dentro de una corrida (A-bis 1/2), no efecto**, y mide
**una** de las dos condiciones que el bullet exige: `respaldo` sí, `canal
personal` no, porque el canal es inobservable fuera del universo de adoptantes
(censo `P0` §6.2). **Acota la regla; no la cierra.** La sensibilidad `C`, que
existía justamente para atacar la lectura de riqueza, quedó inservible por el
defecto de `D1` y se re-corre en el tercer commit.

---

## §3 · Backtest de la `nota_validacion` de `coercitivo` (pieza (b)) — sin entrada

La `nota_validacion` de `tramite.gobierno_digital.coercitivo` dice: *«Backtest:
CoDi = 3.09M cuentas con ≥1 transacción en 6 años.»* La serie primaria del
corpus, abierta en el censo `P0` §4, da **`21 884 617` cuentas validadas
acumuladas a 2025-T3** (nacional, `Cifras_Estatales`, cross-check exacto contra
`Fuente_LADA`). Cuentas **validadas** y cuentas **con transacción** son
cantidades distintas y la serie no publica la segunda: el backtest **queda
actualizado en su denominador y sin actualizar en su numerador**. Se reporta
aquí, en la nota, **sin entrada en la propuesta**, tal como el encargo ordenó, y
con la escala declarada: **cuentas, no personas**.

---

## §4 · Contadores reales

- **priors `ASIGNADO` con dato: `+0`.** `S1` del tablero **sigue en 1**:
  `tramite.gobierno_digital.coercitivo` continúa siendo el único prior
  `ASIGNADO` vigente sin dato. El acto no lo mueve y lo dice.
- **candidatas censadas: `5`** (las 4 del encargo más las Encuestas de
  Competencias Financieras de Banxico, que la supervisión añadió) en **7 piezas**,
  con **7 refutaciones adversariales** y **0 veredictos tumbados**.
- **celdas nuevas con `IC`: `15`** — 9 de `P1` (3 olas × principal/`A`/`B`) y 6
  de `P2` (3 desenlaces × 2 celdas del eje), más 4 de la sensibilidad `C` que el
  defecto de `D1` inutilizó.
- **entradas nuevas en la propuesta: `2`**, ambas `PENDIENTE-DE-MESA`, ninguna
  cargada al motor.
