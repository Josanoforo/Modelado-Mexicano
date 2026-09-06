# `ACTO MAESTRA38-L4` · `civico.voto.clientelar_si_observable` (`R7.6`) sobre LAPOP México 2019 — resultados

**Pieza 1 de 3 del `ACTO MAESTRA38-LOTE-LAPOP`.** Ejecuta, sin editarla, la spec sellada
`prereg-caja-S4-L4` (`forense/prereg-caja/S4-L4-spec-v1_0.md`,
`sha256 7847e35ab37ef30ba1356c21ad1e151fd92773e7cad80e791cc8eafd2b5ae1ff`, verificado contra
su `.sha256` al arrancar y otra vez al cerrar). Base: `origin/main = a5350e59` (`PR #549`).
Entorno **UBUNTU con corpus**. Ponderador `wt`, constante = 1.

---

## 0 · A.8 — qué había antes, y por qué esto no es la primera medición

`python3 tools/ya_medido.py civico.voto.clientelar_si_observable` → **`MEDIDA-EN: L11, L12, L9, S4`**
(salida completa en `forense/notas/2026-09-06-MAESTRA38-LOTE-LAPOP-A8.md`).

`MAESTRA35-L9 §3` (LAPOP 2023) y `MAESTRA35-L11 §1` (ENCUCI 2020) ya midieron **el otro brazo**
de la disyunción del `SI` — «el votante percibe que su voto puede ser monitoreado» — y las dos
dieron **`CONTRARIA`** (`Δ_SECRETO` +14.37 pp `[+1.43,+27.44]` / `Δ_OBSERVABLE` +17.98 pp
`[+10.75,+25.02]`; y +6.38 `[+3.82,+8.89]` / +11.57 `[+6.57,+16.59]`). La Enmienda `D2-f`
(firma de mesa 3/sep/2026) ya movió por eso el tier motor-consumido de la **gemela** `R7.3`.
Esta pieza mide el **otro** brazo — «proximidad/focalización del reparto» — sobre la única ola
que trae la batería `clien*`. **Se cita ese antecedente; no se reabre, no se recalcula, no se
mueve ningún sello ajeno.**

## 1 · Guardias de lectura (spec §2), antes de estimar nada

| guardia | esperado | obtenido | |
|---|---|---|---|
| filas de la ola | 1 580 | **1 580** | OK |
| `clien1na` válidos | 1 578 | **1 578** | OK |
| `clien1na` «sí» | 271 | **271** | OK |

`sha256` del payload = `c88f79eb…4a57`, **COINCIDE** con `data/manifiesto.yaml`.

## 2 · Universo declarado (A-bis 4) y escala (A-bis 3)

**Universo:** personas de 18+ con código válido (`∈{1,2}`) en `clien1n` **o** en `clien1na` y con
`vb3n` válido → **n = 1 035**. `vb3n` sólo tiene 1 035 válidos de 1 580 porque la pregunta se hace
a quien votó: **universo restringido, declarado**, no una pérdida silenciosa.

**Tratamiento (spec §3, literal).** `EXPUESTO=1` si `clien1n=1` **o** `clien1na=1`; `EXPUESTO=0`
**sólo** si las dos valen 2. Sobre la muestra completa: **501 / 1 073 / 6 sin clasificar**; dentro
del universo: **344 / 688 / 3 sin clasificar**. Los 3+6 sin clasificar son quienes tienen una de
las dos en «no» y la otra faltante: por el texto de la spec **no cumplen «las dos son 2»** y no se
imputan. Está contado, no desaparecido.

> Nota de implementación, declarada porque es una trampa real: `_filas()` de la casa descarta la
> fila si **cualquiera** de las columnas pedidas falta. La regla de `EXPUESTO` es una **disyunción**
> — quien tiene `clien1n` faltante y `clien1na=1` **sí** es `EXPUESTO=1` —, así que usar `_filas()`
> tal cual habría borrado casos válidos antes de evaluar la disyunción. `tools/medidor_l4_*.py`
> clasifica primero y arma las tuplas a mano, sin tocar `tools/medidor_clientelismo_lapop.py`.

**Escala:** 2 desenlaces × 2 celdas = **4 celdas** del estimando principal, más 8 celdas de la
robustez `vb10`. Un solo eje, una sola ola.

## 3 · Diseño

`estratopri` (4) × `upm` (129), ponderador `wt` **constante = 1** en las 1 580 filas — la proporción
ponderada es idéntica a la simple y todo el efecto de diseño vive en el conglomerado. IC95 por
**bootstrap de conglomerado**, 10 000 réplicas, seed 42, remuestreo de UPM dentro de estrato.

**La reserva de spec §2 queda cerrada, no heredada.** La spec dejó escrito que nadie había abierto
el codebook de 2019 para confirmar que no existe un segundo campo de ponderación post-estratificación
distinto de `wt`. Se abrió: `Mexico LAPOP AmericasBarometer 2019_Codebook_v1.0_W.pdf` (`sha256`
COINCIDE) menciona **una sola** vez cualquier término de peso, y es `wt`; y de las 221 columnas del
`.dta`, la única candidata (`wt`, «Peso del país») es constante 1. **No existe tal segundo campo.**

## 4 · Resultados

**Desenlace principal — `vb3n = 103` (Meade, PRI):**

| celda | p | IC95 | n | numerador |
|---|---|---|---|---|
| `EXPUESTO=1` | **4.9419 %** | `[2.7701, 7.2508]` | 344 | 17 |
| `EXPUESTO=0` | **9.0116 %** | `[6.7511, 11.5214]` | 688 | 62 |

> **`Δ_elección (PRI)` = −4.0698 pp · IC95 `[−7.3492, −0.7200]` · EXCLUYE 0**

**Desenlace secundario — `vb3n = 101` (AMLO, MORENA):**

| celda | p | IC95 | n | numerador |
|---|---|---|---|---|
| `EXPUESTO=1` | 79.0698 % | `[74.7126, 83.3846]` | 344 | 272 |
| `EXPUESTO=0` | 74.2733 % | `[70.6056, 77.8748]` | 688 | 511 |

> `Δ_elección (MORENA)` = +4.7965 pp · IC95 `[−0.8721, +10.5456]` · **contiene 0**

**Control de regresión.** El punto del bootstrap y el de la linealización coinciden byte a byte en
las cuatro celdas. Y el contraste principal se re-estimó por una **segunda vía independiente**
(`tests/svystat.py::diff_ultimate_cluster`, linealización de Taylor con conglomerado último, que
**no** es el bootstrap que produjo la cifra de arriba): `d = −0.040698`, IC95
`[−0.073886, −0.007509]`, excluye 0. Las dos vías coinciden en el punto y en el veredicto.

**Robustez `vb10` (declarada, no veredicto).** La celda `EXPUESTO=1 · con partido` cae por la
guardia de numerador (`1 < 10`) y se reporta `NO-ESTIMABLE` con su `n`; no participa de nada.

## 5 · Veredicto `B-bis`

> ## **`CONTRARIA`**
> `Δ_elección (PRI)` < 0 con IC95 que excluye 0 (spec §4.1).

La cláusula de precedencia de §4.1 **no se activa**: exige que los dos estimandos vayan «limpios»
y discrepen en signo. `Δ(MORENA)` contiene 0, así que no es limpio; manda PRI, que es además el
desenlace principal. Se reporta el par completo, como la spec pide.

### 5.1 · Las dos filas que `B-bis` exige

- **Si el falsador NO refutara** (`NO-DISCRIMINA`, o `CORROBORADA` con IC ancho): el brazo de
  proximidad/focalización **no quedaría descartado** — la rama expuesta es minoritaria y el
  instrumento no observa quién dio la oferta ni si el votante creyó que su voto podía verificarse.
  El `id` seguiría `[MEDIA]`, sin evidencia nueva en ningún sentido.
- **El falsador SÍ refutó.** Por §4.2, esto suma una **tercera** pieza `CONTRARIA` sobre el mismo
  `id`, ahora **en los dos brazos de la disyunción** y en **tres instrumentos distintos**
  (LAPOP 2019, LAPOP 2023, ENCUCI 2020). Es exactamente la combinación que `se_mueve_si` describe.

### 5.2 · Lectura junto a `L9`/`L11` — comparación de signo, sin celda conjunta

Por spec §0.4/§4.3 **no se computa** ninguna celda de tres factores: no existe una sola ola LAPOP
con oferta clientelar y observabilidad percibida sobre la misma persona (`clien*` sólo en 2019,
`countfair3` sólo en 2023), y forzarla exigiría suponer que dos muestras independientes separadas
por cinco años son intercambiables persona a persona. Lo que sí se reporta es la **comparación de
signo entre piezas** — y hay que hacerla con los números, no con los rótulos:

| pieza | brazo | antecedente → desenlace | `Δ` | signo |
|---|---|---|---|---|
| **L4** (ésta) | proximidad/focalización | oferta clientelar → voto PRI 2018 | **−4.07 pp** | **negativo** |
| `L9` | observabilidad | transferencia → voto oficialismo 2023 (secreto / observable) | +14.37 / +17.98 pp | positivo |
| `L11` | observabilidad | beneficiario → apoyo oficialismo (secreto / observable) | +6.38 / +11.57 pp | positivo |

**Los signos NO coinciden.** Las tres piezas comparten el **rótulo** `CONTRARIA`, y eso es otra
cosa: cada una refuta la predicción de **su propio** diseño — ésta porque el efecto directo sale
negativo; `L9`/`L11` porque la **separación** entre secreto y observabilidad que su par `B-bis`
exige no aparece, con los dos brazos hacia arriba. Coincidir en el rótulo no es coincidir en la
dirección empírica; tratarlo como lo mismo sería comparar léxico en vez de conjuntos.

Por la letra de spec §4.3, entonces, **aplica la segunda rama, no la primera**: «si dan en sentidos
distintos, la lectura es que los dos mecanismos (proximidad vs. observabilidad) se comportan
distinto y el `id` necesita partirse — decisión de mesa, no de este pre-registro». Se declara así,
con la salvedad de que los dos brazos tampoco miden el mismo antecedente ni el mismo desenlace
(oferta de beneficio por el voto → PRI 2018, frente a recepción de transferencia → oficialismo
2023), así que «signo opuesto» aquí **no** es que dos mediciones de una misma cantidad se
contradigan.

**Lo que sí comparten las tres, y es lo que importa para la regla:** en ninguna aparece la cesión
de autonomía que `[MEDIA]` predice. Adjudicar si eso parte el `id`, lo degrada, o ninguna de las
dos, **no es de este acto** — es de mesa (`FP-315`).

## 6 · `se_mueve_si` — verbatim de spec §5

> Si entre `clien1n`/`clien1na`=sí la proporción que vota PRI **no es mayor** que entre
> `clien1n`/`clien1na`=no (controlando `vb10`), este brazo de la cesión de autonomía local
> **no se sostiene** con este proxy — el falsador queda planteado, no corrido (medición: cero, es
> diseño), y se lee junto con el veredicto ya `CONTRARIA` (×2) de `L9`/`L11` sobre el otro brazo,
> per §4.3.

**Se cumplió la condición:** la proporción que vota PRI entre los expuestos **no es mayor** — es
menor, y el IC95 excluye 0.

## 7 · Reservas

Asociación **transversal**, sin identificación causal: el diseño no separa que la oferta cambie el
voto de que a los votantes de cierto perfil se les ofrezca más. El instrumento es auto-reporte de
haber sido blanco de una oferta, con la subdeclaración que eso arrastra. `vb3n` está condicionado
a haber votado — la celda es descriptiva **dentro de los votantes**. La rama expuesta del desenlace
principal se apoya en **17** casos: por encima de la guardia pre-registrada, pero es el número que
sostiene el veredicto y hay que citarlo con él.

## 8 · Qué NO hace este acto

No mueve el tier de `civico.voto.clientelar_si_observable` (`[MEDIA]`, `modelo-decision-v4_0.md:554`)
ni el de su gemela `civico.voto.agencia_con_secreto` — mover tier es de mesa. No reabre `FP-298`
(`EJECUTADA`). No reabre ni recalcula `L9`/`L11` ni la Enmienda `D2-f`. No toca
`milpa/tramite.yaml`, `data/manifiesto.yaml`, la cola, `relaciones`, staging ni ninguna spec.
No carga nada al motor: eso es `FP-315`, con el dato a la vista.
