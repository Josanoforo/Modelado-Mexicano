# `ACTO MAESTRA35-L6` — `COMMIT-3` · resultados de `D1'`

**2 de septiembre de 2026.** Ejecuta la spec de
`forense/notas/2026-09-02-MAESTRA35-L6-spec-3.md`, congelada antes de esta
corrida. `COMMIT-1` (`f77df14`) y `COMMIT-2` (`b0f0bfb`) no se tocaron.

---

## §1 · Control de regresión: pasa

La spec `§4` exigía que `D2` y `D3` reprodujeran **byte a byte** los valores de
`COMMIT-2` —mismo estimador, misma semilla, mismos datos, sólo cambió la
definición de `D1`—.

| desenlace | idéntico a `COMMIT-2` |
|---|---|
| `D2` tenencia de cuenta | **sí** |
| `D3` crédito formal | **sí** |

La corrección no arrastró nada.

Las dos guardias nuevas **no dispararon** con `D1'`: los tres desenlaces cubren
las 13 502 filas del universo declarado y ninguna celda satura. La guardia 1
(cobertura) es la que habría atrapado el defecto original: `D1` cubría 4 078.

## §2 · `D1'` · ahorro formal — el desenlace principal, ahora bien puesto

| celda | `p` | `IC95` | `n` | numerador | estratos | UPM |
|---|---|---|---|---|---|---|
| respaldo = **SÍ** | **`0.329405`** | `[0.307578, 0.351653]` | 3 145 | 1 113 | 188 | 1 402 |
| respaldo = **NO** | **`0.271254`** | `[0.258770, 0.283913]` | 10 357 | 2 965 | 190 | 2 146 |

Brecha **`+5.8151` puntos**, `IC95` **sin traslape** → **`CORROBORADA`**.

## §3 · Veredicto del acto, derivado por código

| desenlace | veredicto |
|---|---|
| `D1'` ahorro formal (**PRINCIPAL**) | **`CORROBORADA`** |
| `D2` tenencia de cuenta | `NO-DISCRIMINA` |
| `D3` crédito formal | `CORROBORADA` |

**Veredicto del acto: `ACOTADA`** — el signo que el bullet predice se sostiene
en el desenlace principal y en el crédito, y **no** se sostiene en la cuenta.
Es la regla de precedencia de la spec aplicada por el script, no a ojo.

## §4 · La sensibilidad `C` es el resultado más informativo, y voltea

`C` repite el contraste de `D1'` **dentro de cada estrato** de `P4_9_1`
(*«¿podría aprovechar la oportunidad con sus ahorros?»*). Se pre-registró en
`COMMIT-1` para atacar la lectura obvia —que el respaldo sólo esté midiendo
tener familia con dinero—. No la confirma ni la descarta: **la parte en dos.**

| estrato de `P4_9_1` | respaldo=SÍ | respaldo=NO | brecha | veredicto |
|---|---|---|---|---|
| **podría con sus ahorros = SÍ** | `0.353961` `[0.324342, 0.384001]` n=1 551 | `0.428355` `[0.401509, 0.455624]` n=2 414 | **`−7.4395`** pp | **`CONTRARIA`** |
| **podría con sus ahorros = NO** | `0.306340` `[0.277569, 0.336245]` n=1 594 | `0.224910` `[0.212358, 0.237841]` n=7 943 | **`+8.1430`** pp | **`CORROBORADA`** |

Los dos `IC95` sin traslape, en **direcciones opuestas**.

**Qué dice, con cuidado.** El `+5.82` de `D1'` en el agregado **no es un efecto
uniforme: es el promedio de dos poblaciones que se comportan al revés.** Entre
quienes ya podrían resolver la oportunidad **con recursos propios**, tener
además el respaldo de familiares se asocia con **menos** ahorro formal
(`35.40 %` contra `42.84 %`); entre quienes **no** podrían, se asocia con
**más** (`30.63 %` contra `22.49 %`).

La lectura que estos números soportan —y es una lectura, no una identificación—
es que **la red personal es sustituto donde hay recursos propios y puente donde
no los hay**. El bullet (`canon/modelo-decision-v4_0.md:501`) predice puente; el
dato lo confirma **sólo en la mitad de la población que no tiene con qué
sustituirlo**, y lo contradice en la otra. Que la brecha agregada sobreviva es
aritmética: el estrato «no podría» es cinco veces más grande (9 537 contra
3 965).

**Es exactamente el patrón que este programa ya encontró dos veces** — el `β`
cero de `MAESTRA34-L6` que era el promedio de `+2.41` y `−5.69`, y la escolaridad
no monótona de `MAESTRA35-L1` —. Se registra como tercera ocurrencia:
**un agregado que corrobora puede ser la media de un eje que se invierte.**

## §5 · Límites, sin rebajar

- **Asociación dentro de una corrida (A-bis 1/2), no efecto.** `P4_9_1` no es una
  asignación: estratificar por él no controla la riqueza, la describe.
- **Mide una de las dos condiciones del bullet.** `respaldo` sí; `canal personal`
  no, porque es inobservable fuera del universo de adoptantes (censo `P0` §6.2).
  **Acota la regla; no la cierra.**
- **`P4_9_4` mide respaldo declarado como disponible**, no ejercido, y ante un
  evento concreto (comprar casa, terreno o negocio), no en general.
- Los valores `0.74/0.21/0.05` y `0.52/0.33/0.15` del prior **no se tocan**: son
  tres conductas sin nombrar en un bullet sin `si`/`entonces`, y esta medición no
  los sustituye. Sella mesa.
