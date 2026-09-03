# `ACTO MAESTRA35-L11 · ROBUSTECE-L9` — `P1-P4` · resultados

> | | |
> |---|---|
> | **CENSO** | `forense/notas/2026-09-02-MAESTRA35-L11-P0-censo.md` |
> | **SPEC HEREDADA** | `forense/notas/2026-09-02-MAESTRA35-L9-spec.md` §3.1 (pieza b) y §4.1 (pieza c) — verbatim, sólo cambia el instrumento y sus campos de diseño |
> | **MEDIDOR** | `tools/medidor_l11_encuci2020.py` (hermano de los medidores de `L9`, no los edita) |
> | **ARTEFACTO** | `data/l11-encuci2020-v1_0.json` |
> | **CONTROL DE REGRESIÓN** | Ningún medidor de `L9` fue tocado en este acto: `L9` reproduce byte a byte trivialmente. El estimador (`prop_bootstrap`/`diff_bootstrap`, `tests/svystat.py::prop_ultimate_cluster`) se **importa**, no se reimplementa |
> | **VERIFICAS ASÍ** | `python3 tools/medidor_l11_encuci2020.py --mide --json data/l11-encuci2020-v1_0.json` |

---

## §0 · Los dos veredictos de este acto, en una tabla

| pieza | regla | tier | instrumento | `Δ`/contraste principal | IC95 | veredicto `B-bis` (este acto) |
|---|---|---|---|---|---|---|
| (b) | `R7.3`/`R7.6` agencia con secreto | `[FUERTE]`/`[MEDIA]` | ENCUCI 2020 | SECRETO **+6.38 pp** · OBSERVABLE **+11.57 pp** | `[+3.82, +8.89]` · `[+6.57, +16.59]` | **`CONTRARIA`** |
| (c) | `R7.4` protesta y agravio urbano | `[MEDIA-FUERTE]` | ENCUCI 2020 | `C1` +2.03 pp (contiene 0) · `C2` **+3.72 pp** | `[−0.18, +4.12]` · `[+2.22, +5.22]` | **`CORROBORADA-PARCIAL`** |

`(a)` `R7.7` y las tres piezas sobre Latinobarométro 2024 quedaron
`EXISTE-NO-SATISFACE` en el censo (`P0` §2-§4) — no se midieron, no hay veredicto
que forzar. `(d)` `R1.5`/Mexico Panel 2012 quedó `NO-LANZADA` por compuerta desde
el arranque.

---

## §1 · Pieza (b) · `R7.3`/`R7.6` sobre ENCUCI 2020 — la separación vuelve a no aparecer

| rama | transferencia | `p` | IC95 | `n` | numerador |
|---|---|---|---|---|---|
| **SECRETO** (`AP7_15`=1) | sí (`AP6_10`=1) | 0.321633 | [0.300274, 0.342942] | 3 144 | 1 059 |
| | no (`AP6_10`=2) | 0.257825 | [0.244352, 0.271294] | 7 836 | 2 088 |
| | **`Δ_SECRETO`** | **+0.063809** | **[+0.038238, +0.088942]** | | **excluye 0** |
| **OBSERVABLE** (`AP7_15`=2) | sí | 0.319745 | [0.276605, 0.362079] | 951 | 285 |
| | no | 0.204092 | [0.187120, 0.221256] | 3 152 | 754 |
| | **`Δ_OBSERVABLE`** | **+0.115652** | **[+0.065748, +0.165879]** | | **excluye 0** |

`Δ_diferencia` = **+5.18 pp** (sin IC: la spec §3.1 no lo pre-registró, y este
acto hereda esa decisión).

**Veredicto `CONTRARIA`**, por la misma cláusula de precedencia de `spec §3.1`
que dio `CONTRARIA` en `L9`: las dos ramas dan `Δ` positivo y limpio — la
separación que el par afirma (que bajo secreto percibido la asociación se
anula) **no aparece** en este instrumento tampoco.

**Es la MISMA forma que `L9` encontró con LAPOP 2023, con un segundo
instrumento y un desenlace distinto.** Aquí el antecedente es transferencia de
programa social (no la ayuda genérica de `mexwf1_19`), el moderador es la
misma pregunta de percepción de secreto (formulación equivalente:
«¿cree que su voto es secreto o se puede descubrir?»), y el desenlace es
simpatía con el partido en el gobierno (no intención de voto explícita). Con
todo eso distinto, la forma se repite: recibir la transferencia se asocia con
simpatizar más con el oficialismo **tanto bajo secreto percibido (+6.38 pp)
como bajo voto observable (+11.57 pp)**, y la diferencia entre las dos ramas
(+5.18 pp) es, otra vez, pequeña frente a la brecha que ya existe donde `R7.3`
esperaba cero.

### §1.1 · Veredicto conjunto (regla de sello de este acto)

`L9` (LAPOP 2023): `CONTRARIA`, `Δ_SECRETO` +14.37 pp `[+1.43,+27.44]`,
`Δ_OBSERVABLE` +17.98 pp `[+10.75,+25.02]`.
`L11` (ENCUCI 2020): `CONTRARIA`, `Δ_SECRETO` +6.38 pp `[+3.82,+8.89]`,
`Δ_OBSERVABLE` +11.57 pp `[+6.57,+16.59]`.

**Mismo signo en las dos ramas, IC95 fuera de 0 en las cuatro celdas de
diferencia (dos ramas × dos instrumentos).** Por la regla de sello que el
encargo fija: *«se sella CONTRARIA si replica en un segundo instrumento
independiente (mismo signo, IC fuera de 0)»*. Se cumple.

**→ `CONTRARIA-REPLICADA`.** Dos instrumentos, dos preguntas de secreto con
formulación distinta, dos antecedentes de transferencia distintos (dádiva vs.
programa social), dos desenlaces distintos (intención de voto explícita vs.
simpatía de partido), y la misma forma: bajo secreto percibido la agencia **no**
se conserva. `R7.3` es `[FUERTE]`. Esto es lo que la regla de sello de mesa
exige para tocar una `[FUERTE]` con un dato — el pre-registro de la regla de
sello quedó escrito en el encargo, antes de medir nada de esta pieza.

**Reservas que siguen en pie, sin cambio respecto a `L9`.** Las dos son
asociaciones transversales sin identificación causal; la dirección obvia de
confusión —quien ya simpatiza con el oficialismo puede tener más probabilidad
de estar en un programa— sigue abierta en los dos instrumentos. Y el desenlace
de este acto (`AP7_13`, simpatía) es todavía más laxo que `vb20` de `L9`
(intención de voto): simpatizar no es la misma cosa que votar o pretender
votar. La replicación es de **forma**, no de identificación.

## §2 · Pieza (c) · `R7.4` sobre ENCUCI 2020 — el corazón de la regla sigue sin discriminar, y la mitad urbana vuelve a corroborar

| celda | `p` | IC95 | `n` | numerador |
|---|---|---|---|---|
| urbano-agravio | 0.112192 | [0.101885, 0.123641] | 8 322 | 883 |
| urbano-sin-agravio | 0.074959 | [0.064972, 0.085672] | 6 356 | 450 |
| rural-agravio | 0.091912 | [0.074435, 0.110359] | 2 050 | 188 |
| rural-sin-agravio | 0.066996 | [0.056831, 0.077389] | 3 456 | 219 |

- `C1` (entorno, con agravio) = **+2.03 pp**, IC95 `[−0.18, +4.12]`, **contiene 0**.
- `C2` (agravio, en urbano) = **+3.72 pp**, IC95 `[+2.22, +5.22]`, **excluye 0**.

**Veredicto `CORROBORADA-PARCIAL`.** A diferencia de `L9` —donde `C1` cayó por
la guardia de numerador (rural-víctima con sólo 7 casos) y el veredicto salió
de `C2` solo por regla explícita de `spec §4.1`— aquí **las cuatro celdas son
estimables** (rural-agravio tiene 188 numerador, muy por encima de 10). `C1`
**sí se pudo estimar** con este instrumento, y su punto va en el signo
esperado (+2.03 pp) pero **no discrimina**: el IC roza 0 por el lado bajo
(`−0.18`). `C2` sí discrimina, en el signo esperado. La spec heredada no
anticipó este caso exacto (estimable-pero-no-limpio), así que este acto lo
resuelve con la misma lógica de fondo que `spec §4.1` ya fija para el caso
`NO-ESTIMABLE`: si uno de los dos contrastes no separa nada, el veredicto sale
del que sí separa, y se declara qué parte de la regla no se cerró.

**Lo que sí se puede decir sobre el corazón de la regla, con este instrumento
—a diferencia de `L9`, que no pudo decir nada—.** El contraste
urbano-contra-rural bajo agravio **sí tiene dato aquí** (2 050 casos en la
celda rural-agravio, contra 65 en LAPOP), y el punto va en el signo que `R7.4`
predice (el entorno urbano canaliza más el agravio hacia la protesta:
11.22 % contra 9.19 %), pero el IC95 no despeja el cero por 0.18 puntos
porcentuales. Es la primera vez que este contraste se puede intentar con `n`
suficiente, y da un resultado **ambiguo, no nulo**: la brecha existe en el
punto, pero el diseño (y la escala temporal distinta: «alguna vez» contra
«últimos 12 meses» de LAPOP) no alcanza a probarla limpiamente.

### §2.1 · Veredicto conjunto (regla de sello de este acto)

`L9` (LAPOP 2019): `CORROBORADA-PARCIAL`, `C1` **no estimable** (n=65,
numerador 7), `C2` +5.60 pp `[+2.32,+8.96]`.
`L11` (ENCUCI 2020): `CORROBORADA-PARCIAL`, `C1` +2.03 pp `[−0.18,+4.12]`
(estimable, no discrimina), `C2` +3.72 pp `[+2.22,+5.22]`.

El sub-resultado que sí replica limpio es `C2` (agravio, dentro de lo
urbano): mismo signo, IC95 fuera de 0 en los dos instrumentos → **`C2`
`CORROBORADA-REPLICADA`**. El sub-resultado que la regla realmente necesita —
`C1`, el contraste de entorno— **sigue sin discriminar en los dos intentos**,
aunque por razones distintas: en `L9` la celda no alcanzaba (`n < 10`
esperado); en `L11` la celda alcanza (188 numerador) pero el IC roza cero. Por
la regla de sello de mesa, `R7.4` es `[MEDIA-FUERTE]` y su sub-claim de entorno
no tiene, en ninguno de los dos intentos, un `CORROBORADA` ni un `CONTRARIA`
limpio que sellar — así que el veredicto conjunto sobre el **corazón** de la
regla es **`AMBIGUA-ENTRE-INSTRUMENTOS`** por acumulación de evidencia
insuficiente, no por señales contradictorias: los dos instrumentos apuntan al
mismo signo, ninguno lo prueba. `R7.4` sigue **acotada**, no cerrada, en su
mitad más importante.

**Esta pieza no reabre la fila `D` de `ADR-158`** (evento, no persona) ni dice
nada sobre `R7.5` (autodefensa) — mismas reservas que `L9`.

## §3 · Lo que este acto no midió, y por qué

1. **`R7.7` (turnout ≠ vote-choice), ambos instrumentos.** `EXISTE-NO-SATISFACE`
   en el censo — ni ENCUCI ni Latinobarómetro traen recepción personal de
   dádiva y desenlace de vote-choice sobre la misma persona (`P0` §2).
2. **`R1.5` (seguro de depósito), Mexico Panel 2012.** `NO-LANZADA` por
   compuerta: ICPSR 35024 no está registrado como microdato en
   `data/manifiesto.yaml` (verificado por el orquestador antes de arrancar).
3. **Las tres piezas sobre Latinobarómetro 2024.** `EXISTE-NO-SATISFACE`: la
   ola no trae ningún ítem de compra de voto, secreto del voto, transferencia
   condicionada, protesta ni agravio localizado (`P0` §2-§4, búsqueda por
   etiqueta sobre las 332 columnas).

## §4 · Contador real de este acto

- **Veredictos de `L9` con segundo instrumento: 2 de 5 posibles** —
  `R7.3`/`R7.6` (`b`) y `R7.4` (`c`). `R7.7` (`a`) y `R1.5` (`d`) no llegaron a
  medirse por razones de instrumento/compuerta, declaradas arriba.
- **Celdas y contrastes con IC95 en este acto: 10** (4 celdas + 2 `Δ` de la
  pieza `b`; 4 celdas + 2 contrastes de la pieza `c`).
- **`CONTRARIA-REPLICADA`: 1** (`R7.3`/`R7.6`, contra una `[FUERTE]`).
- **`AMBIGUA-ENTRE-INSTRUMENTOS`: 1** (el corazón de `R7.4`, contraste
  urbano/rural bajo agravio — es un entregable: impide sellar `CORROBORADA` con
  un solo dato, y aquí impide sellarla con dos).
- **`CORROBORADA-REPLICADA` (sub-claim): 1** (`C2` de `R7.4`, agravio dentro
  de lo urbano).
- **Reglas del motor: sin cambio.** Nada se cargó a `milpa/tramite.yaml`.

**Lo que este acto no hizo:** no selló nada (todas las entradas nuevas quedan
`PENDIENTE-DE-MESA`), no tocó el modelo canónico, no descargó el Mexico Panel,
no reabrió las entradas de `L9` en la propuesta, no editó
`data/inventario-reactivos-v1_2.tsv`.
