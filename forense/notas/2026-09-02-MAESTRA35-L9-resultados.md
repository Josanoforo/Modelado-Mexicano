# `ACTO MAESTRA35-L9 · REGLAS-ACTIVOS-L3` — `P1–P4` · resultados (`COMMIT-2`)

> | | |
> |---|---|
> | **SPEC CONGELADA** | `forense/notas/2026-09-02-MAESTRA35-L9-spec.md` (commit `a67e46b`) — **no se edita** |
> | **CENSO** | `forense/notas/2026-09-02-MAESTRA35-L9-P0-censo.md` (commit `418a22f`) |
> | **ARTEFACTOS** | `data/l9-clientelismo-lapop-v1_0.json` · `data/l9-protesta-lapop-v1_0.json` · `data/l9-entitlement-encuci-v1_0.json` · `data/l9-seguro-deposito-enif24-v1_0.json` |
> | **VERIFICAS ASÍ** | `python3 tools/medidor_<X>.py --mide` — las cuatro corridas empiezan verificando las guardias de lectura de `spec §0.5` y **PARAN** si un marginal no es el congelado |

**Ninguna spec se corrigió.** No hay `COMMIT-3`: las cinco piezas corrieron tal
como se congelaron, incluida la guardia que se anticipó que iba a morder y
mordió.

---

## §0 · Los cinco veredictos, en una tabla

| pieza | regla | tier | `Δ` principal | IC95 | veredicto `B-bis` |
|---|---|---|---|---|---|
| (a) | `R7.7` turnout ≠ vote-choice | `[MEDIA]` | asistencia **+3.96 pp** · elección −1.57 pp | `[−0.77, +8.62]` · `[−5.76, +2.85]` | **`NO-DISCRIMINA`** |
| (a-bis) | `R7.3` / `R7.6` agencia con secreto | `[FUERTE]` / `[MEDIA]` | SECRETO **+14.37 pp** · OBSERVABLE **+17.98 pp** | `[+1.43, +27.44]` · `[+10.75, +25.02]` | **`CONTRARIA`** |
| (b) | `R7.4` protesta y agravio urbano | `[MEDIA-FUERTE]` | `C1` **NO-ESTIMABLE** · `C2` **+5.60 pp** | — · `[+2.32, +8.96]` | **`CORROBORADA-PARCIAL`** |
| (c) | `R7.8` entitlement de derecho | `[HIPÓTESIS]` | **−6.57 pp** | `[−8.72, −4.43]` | **`CONTRARIA`** |
| (d) | `R1.5` seguro de depósito | `[MEDIA]` | **+0.60 pp** | `[−2.26, +3.71]` | **`NO-DISCRIMINA`** |

Los cinco veredictos salen de las reglas congeladas en `spec §2.1`, `§3.1`,
`§4.1`, `§5.1` y `§6.1`, aplicadas por código; ninguno se decidió a ojo.

---

## §1 · Control de regresión, antes de mirar nada

`spec §1.1` exige que el punto del bootstrap y el de la linealización
(`tests/svystat.py::prop_ultimate_cluster`) coincidan **byte a byte**, y hace
`PARA` si no. Las **84** celdas y contrastes con IC95 de este acto pasaron ese
control; ninguna corrida se detuvo por él.

Las **guardias de lectura de `spec §0.5`** —marginales con valor esperado,
congelados antes de correr— también pasaron en las cuatro fuentes. Ese control
existe porque un lector nuevo devuelve vacío, no error.

Y una optimización que se hizo a mitad de camino se verificó como tal: el
bootstrap se reescribió para acumular totales por UPM en vez de recorrer filas
(sin eso, 3 096 conglomerados × 10 000 réplicas no terminan). La corrida
posterior es **idéntica byte a byte** a la anterior, verificado comparando los
JSON completos.

---

## §2 · Pieza (a) · `R7.7` — la forma es la que la regla describe; la `n` no alcanza

| | `p` | IC95 | `n` | numerador |
|---|---|---|---|---|
| votó \| le ofrecieron | 0.832714 | [0.787546, 0.876494] | 269 | 224 |
| votó \| no le ofrecieron | 0.793103 | [0.771206, 0.814473] | 1 305 | 1 035 |
| **`Δ_asistencia`** | **+0.039610** | **[−0.007733, +0.086220]** | | contiene 0 |
| votó PRI \| ofrecieron | 0.063492 | [0.030120, 0.102151] | 189 | 12 |
| votó PRI \| no ofrecieron | 0.079196 | [0.059312, 0.101517] | 846 | 67 |
| **`Δ_elección` (PRI)** | **−0.015704** | **[−0.057575, +0.028525]** | | contiene 0 |
| **`Δ_elección` (MORENA)** | +0.054824 | [−0.007015, +0.114695] | | contiene 0 |

**Veredicto `NO-DISCRIMINA`**, por la regla congelada: `CORROBORADA` exigía que
el IC de la asistencia **excluyera** 0 —no lo hace—, y `CONTRARIA` exigía que el
de la elección lo excluyera —tampoco—.

**Lo que sí se puede decir.** Los puntos van en el sentido de la regla: la oferta
se asocia con **+3.96 pp** de asistencia declarada y con **−1.57 pp** de voto por
el PRI, el partido que tenía el gobierno federal en 2018. La regla afirma
exactamente esa forma —la dádiva mueve el ir a votar y no el a quién—, y el dato
la **ilustra sin probarla**: con 269 personas en la rama tratada, ninguno de los
dos intervalos despeja el cero.

**Las dos limitaciones, que estaban escritas antes de medir.** (1) La pierna de
elección **condiciona en haber votado**, que es el otro desenlace: colisionador
declarado, así que esa brecha es descriptiva **dentro de los votantes**. (2) El
instrumento **no observa quién dio la dádiva**, así que el desenlace es el voto
por un partido pre-registrado y no «el que dio», que es el enunciado literal de
la regla y no es medible aquí.

**El eje de escolaridad, reportado sin convertirlo en veredicto.** La brecha de
asistencia por tramo de años de educación es **no monótona y limpia en los dos
extremos**: 0-6 años **+10.74 pp** `[+1.09, +19.12]`, 7-9 −0.14 pp (contiene 0),
10-12 +5.23 pp (contiene 0), 13+ **+9.41 pp** `[+3.15, +14.84]`. `spec §1.4` fija
que un eje **sin signo pre-registrado** no puede dar más que `DISCRIMINA`, y este
no lo traía: se reporta y no se adjudica. Pero es la pista más concreta que deja
la pieza — la asociación entre oferta y asistencia existe y es limpia en los
extremos de la escolaridad, y se diluye en el medio.

**El contador que NO se mueve.** El encargo previó «cifra de laboratorio
sustituida por dato de encuesta: 1 si (a) satisface». **(a) no satisface**, así
que ese contador queda en **0**. Y aunque hubiera satisfecho, la reserva escrita
en `spec §2.1` seguía en pie: el 0.63 de Ascencio-Chang mide la condición de
**observabilidad del voto**, y esta pieza no tiene ese ítem.

---

## §3 · Pieza (a-bis) · `R7.3`/`R7.6` — la separación que el par afirma no aparece

| rama | ayuda | `p` | IC95 | `n` |
|---|---|---|---|---|
| **SECRETO** (`countfair3` = Siempre) | sí | 0.658228 | [0.546667, 0.766234] | 79 |
| | no | 0.514493 | [0.451493, 0.579151] | 276 |
| | **`Δ_SECRETO`** | **+0.143735** | **[+0.014272, +0.274364]** | **excluye 0** |
| **OBSERVABLE** (Algunas veces / Nunca) | sí | 0.650442 | [0.583673, 0.714286] | 226 |
| | no | 0.470665 | [0.433424, 0.507712] | 767 |
| | **`Δ_OBSERVABLE`** | **+0.179778** | **[+0.107487, +0.250213]** | **excluye 0** |

`Δ_diferencia` = **+3.60 pp** (sin IC: la spec no lo pre-registró).

**Veredicto `CONTRARIA`**, por la cláusula de precedencia que `spec §3.1`
congeló antes de medir: *«si `Δ_SECRETO` y `Δ_OBSERVABLE` dan las dos limpias y
en el mismo signo, la separación que el par afirma no existe: manda
`CONTRARIA`»*. Las dos excluyen cero y las dos son positivas.

**Es el resultado más fuerte del lote, y toca una `[FUERTE]`.** `R7.3` dice que
sin monitoreo percibido del voto la agencia **se conserva** — recibir la
transferencia no debería mover a quién se vota. El dato dice que **sí la mueve, y
casi tanto** como donde el voto se percibe observable: **+14.37 pp** bajo secreto
percibido contra **+17.98 pp** sin él. La diferencia entre las dos ramas va en el
signo que `R7.6` predice, pero es **pequeña frente a la brecha que ya existe en
la rama donde `R7.3` esperaba cero**.

**Lo que esto no es, dicho con la misma claridad.** No es un efecto: es una
asociación transversal sin identificación, y la dirección más obvia de confusión
está abierta —quien apoya al oficialismo puede tener más probabilidad de estar en
un programa, no sólo al revés—. Lo que el dato contradice **no** es «la
transferencia compra el voto», sino la afirmación más débil y más concreta que
`R7.3` sí hace: que **bajo secreto percibido la asociación se anula**. No se
anula. Y la rama SECRETO se apoya en **79** personas tratadas: su IC despeja el
cero por poco (`[+1.43, +27.44]`). Se reporta como está, sin redondear la
conclusión hacia arriba.

**Universo restringido, declarado en la spec y no descubierto aquí:** `vb20`
cubre 87.18 % (< 90 %), así que las celdas de esta pieza **no se reconcilian**
contra ningún marginal poblacional (`A-bis 4`).

**Esta pieza no reabre la fila `C` de `R7.3`** (`ADR-155`) ni propone cambiarla:
aquel `C` dice que el RDD que su falsador exige no es construible, y aquí no se
construye ningún RDD.

---

## §4 · Pieza (b) · `R7.4` — el corazón de la regla no se midió, y estaba previsto

| celda | `p` | IC95 | `n` | numerador |
|---|---|---|---|---|
| urbano-víctima | 0.105727 | [0.080092, 0.132723] | 454 | 48 |
| urbano-no-víctima | 0.049689 | [0.033962, 0.066250] | 805 | 40 |
| rural-víctima | **`NO-ESTIMABLE`** | — | 65 | **7** |
| rural-no-víctima | 0.067729 | [0.036585, 0.100000] | 251 | 17 |

- `C1` (entorno, con agravio) = **`NO-ESTIMABLE`** — la celda rural-víctima cayó
  por la guardia de numerador < 10 de `spec §1.3`.
- `C2` (agravio, en urbano) = **+5.60 pp**, IC95 `[+2.32, +8.96]`, **excluye 0**.

**Veredicto `CORROBORADA-PARCIAL`.** `spec §4.1` fijó antes de correr que si `C1`
caía por la guardia, el veredicto saldría de `C2` solo **y habría que declarar
que el contraste de entorno —el corazón de la regla— no se midió**. Cayó, y se
declara.

Dentro de lo urbano el agravio **sí** mueve la protesta: 10.57 % entre víctimas
de delito contra 4.97 % entre no víctimas. Pero `R7.4` afirma que **el entorno
urbano con espacio público canaliza** el agravio hacia la protesta, y eso exige
comparar urbano contra rural bajo agravio — que es justo lo que no tiene dato.
Que `C2` corrobore no dice nada sobre si el entorno importa.

**Dato colateral que apunta en contra de la lectura urbana**, reportado sin
convertirlo en veredicto porque el eje no traía signo pre-registrado: la protesta
**no baja** con el tamaño de localidad — 6.68 % en municipios grandes (> 100 k),
7.59 % en medianos, 8.63 % en pequeños (< 25 k), con los tres IC95 traslapados.

**Esta pieza no reabre la fila `D` de `ADR-158`** y **no dice nada sobre `R7.5`**:
aquel `D` corrió sobre datos de **evento**; aquí la unidad es la **persona
auto-reportada**. Y mide **dos de los cuatro antecedentes** de la regla — «red
previa» y «falla estatal palpable» no están en el instrumento.

---

## §5 · Pieza (c) · `R7.8` — el primer dato de percepción, y va en contra

| | `p` | IC95 | `n` | numerador |
|---|---|---|---|---|
| dice «derecho» \| beneficiario | 0.540278 | [0.523284, 0.557868] | 5 665 | 3 048 |
| dice «derecho» \| no beneficiario | 0.606014 | [0.593683, 0.617803] | 15 186 | 9 124 |
| **`Δ_entitlement`** | **−0.065736** | **[−0.087157, −0.044277]** | | **excluye 0** |

**Veredicto `CONTRARIA`.** La brecha es negativa y limpia; el signo
pre-registrado era positivo.

`R7.8` es `[HIPÓTESIS]` y afirma que la transferencia no condicionada **se vive
como derecho**. El glosario `conf.07` la separó de
`civico.voto.agencia_con_secreto` precisamente porque esa mitad no tenía
identificación, y `MAESTRA33-E18` descartó ENASEM por medir afiliación y no
percepción. **ENCUCI 2020 la pregunta literal, y la contesta al revés**: los
beneficiarios dicen «derecho» **menos** que los no beneficiarios —54.03 % contra
60.60 %, −6.57 pp sin traslape, sobre 20 868 personas—. Recibir el programa se
asocia con verlo más como **«una ayuda que da el gobierno»**, que es exactamente
la otra mitad de la diagonal partida (`civico.transferencia.atribucion_lider`,
`[MEDIA]`).

**La condicionalidad no explica la brecha.** El eje anidado `AP6_11` —a quién le
pidieron dinero, documentos, favores o que votara por algún partido a cambio de
entrar o permanecer en el programa: 297 de 5 789 beneficiarios, 5.1 %— **no
discrimina**: 55.29 % contra 54.06 %, IC95 de la brecha `[−6.13, +8.98]`. Quien
fue condicionado no vive el programa menos como derecho que quien no lo fue.
`spec §5.1` ya había fijado que este eje **no puede voltear** el principal.

**Reserva, escrita en `COMMIT-1`:** es una asociación transversal. Que el
beneficiario diga «derecho» menos es compatible con que el programa cambie la
percepción **y** con que quien ya pensaba distinto se inscribiera más. Este
diseño no los separa.

Ejes no anidados, todos con IC95 traslapados entre sí salvo escolaridad: sexo
58.63 % / 59.21 %; edad 59.15 / 58.99 / 59.39 / 57.83 %; escolaridad
55.49 / 60.71 / 61.47 / 57.70 % — no monótona, con la punta baja en «hasta
primaria». Sin signo pre-registrado, no se adjudican.

---

## §6 · Pieza (d) · `R1.5` — el moderador no mueve nada, y el marginal dice por qué

| desenlace | conoce protección | no conoce | `Δ` | IC95 |
|---|---|---|---|---|
| `D1` desconfianza (`P5_20 = 03`) | 0.060780 | 0.054767 | **+0.006013** | [−0.022646, +0.037052] |
| `D2` desconfianza o efectivo (`03,05`) | 0.120107 | 0.102699 | **+0.017408** | [−0.022218, +0.058105] |

(`n` = 426 conocen / 2 544 no.)

**Veredicto `NO-DISCRIMINA`** en los dos: los IC contienen cero. La cláusula de
precedencia de `spec §6.1` no se dispara —ninguno es limpio y además coinciden
en signo—. Los dos puntos van en el signo **contrario** al predicho, sin alcanzar
significancia.

**El hallazgo limpio de esta pieza está en el marginal, no en el cruce.** `R1.5`
pone en su `SI` un «seguro de depósito **visible**». `P5_23` no mide visibilidad:
mide la **creencia** de que existe protección. Y las dos se separan de verdad:

- **4 136** personas dicen saber que sus ahorros están protegidos si el banco
  quiebra.
- De ésas, **3 148 (76.1 %) contestan «no sabe»** cuando se les pide nombrar la
  institución.
- **362 en toda la muestra de 13 502 (2.7 %)** nombran al **IPAB**.

La condición que la regla pone en su antecedente la cumple el **2.7 %** de la
población. En México el seguro de depósito prácticamente **no es visible**, y esa
es la explicación más plausible de que el moderador no mueva nada. La entrada
**acota** `R1.5`; no la cierra.

**Segunda reserva, de `COMMIT-1`:** `P5_20` es **razón principal**. Quien
desconfíe pero elija otra razón dominante —«no le alcanza» (894) o «no la
necesita» (1 029) son mucho más frecuentes— no cuenta como desconfiado.

**Los ejes secundarios cayeron casi enteros** por la guardia de numerador < 10:
de escolaridad sólo sobrevivió «secundaria» (+1.33 pp, contiene 0), y de edad
ninguno. Con 183 casos de desconfianza en todo el universo, el desenlace no
soporta desagregación. **El eje que el encargo pedía y no es construible** es
«tenencia de cuenta»: `P5_20` sólo existe para quien no tiene cuenta, así que no
varía dentro del universo. No se sustituyó por nada.

---

## §7 · Desviaciones respecto del encargo, todas declaradas

1. **La ola principal de (a) es 2019, no 2023.** El encargo planteaba 2023 como
   principal y 2019/2021 como serie; la batería clientelar **sólo existe en
   2019**. Los ids de la propuesta llevan la ola que de verdad los midió.
2. **(c) no cerró en `EXISTE-NO-SATISFACE`.** El encargo previó que ningún
   instrumento preguntara la percepción; ENCUCI 2020 `AP6_9` la pregunta literal.
3. **`R7.3`/`R7.6` no se miden contra la dádiva** sino contra la transferencia:
   ninguna ola cruza dádiva con secreto sobre la misma persona.
4. **La serie de LAPOP no se construyó.** El encargo pedía «olas múltiples como
   serie»; 2021 no trae ninguna de las variables y 2006 no es el mismo
   instrumento. Cada pieza corre sobre una sola ola, declarada.
5. **`P5` (inventario de reactivos): no se editó.** Ver §8.

## §8 · `P5` · registro — el inventario de reactivos NO se toca

El encargo condiciona la entrada de LAPOP a `data/inventario-reactivos-v1_2.tsv`
a que **el procedimiento de ETIQUETA lo permita sin re-extracción**, y manda
leerlo: `forense/notas/2026-08-30-etiqueta-v1_2-spec.md`. **Leído, y no lo
permite** — por dos razones distintas, las dos del propio archivo:

1. **No es una vía de ingesta.** `ETIQUETA-v1_2` es una spec de **etiquetado**:
   rellena la columna `instrumento` de filas **que ya están** en el inventario,
   derivando la familia de `payload_id` (regla `v1_1`, §1.1) o de campos
   declarados de `data/manifiesto.yaml` (regla `v1_2`, §1.2). No añade filas.
   Meter las variables de LAPOP exigiría **extraer reactivos con texto de cuatro
   payloads `.dta`** que ese pipeline nunca ha recorrido — re-extracción, que es
   justo lo que el encargo pone como condición de exclusión.
2. **Su lista de familias es cerrada y LAPOP no está en ella.** `§1.2` la
   deriva por comando de los *stems* ya presentes en la columna `instrumento`
   (44 familias, todas INEGI/Banxico salvo los `adq15_*`/`adqcorre_*`/`r*`), y
   fija que lo que ninguna regla resuelve **queda `(sin-instrumento-derivable)`
   — no se fuerza ninguna otra heurística**. Coherente con el censo `A.4` §2:
   `lapop`/`barometer`/`latinobar` dan **0** en el inventario, contados en
   Python con control positivo.

**Se deja como hallazgo y NO se edita el inventario**, que es exactamente la
rama que el encargo prescribe. Queda registrado en `forense/hallazgos.md`.

## §9 · Contador real de este acto

- **Reglas del modelo con dato (pendiente sello): 6** — `R7.7`, `R7.3`, `R7.6`,
  `R7.4`, `R7.8`, `R1.5`. Las seis que el encargo nombraba. Ninguna se carga al
  motor; las cinco entradas quedan `PENDIENTE-DE-MESA` al pie de la propuesta.
- **Celdas y contrastes con IC95: 84.**
- **Cifra de laboratorio sustituida por dato de encuesta: 0.** (a) salió
  `NO-DISCRIMINA`; el contador que el encargo condicionaba a que satisficiera
  **no se mueve**.
- **Veredictos `B-bis`:** 2 `CONTRARIA` (`R7.3`/`R7.6` y `R7.8`),
  1 `CORROBORADA-PARCIAL` (`R7.4`), 2 `NO-DISCRIMINA` (`R7.7`, `R1.5`).
- **Piezas cerradas en `P0`:** 3 `EXISTE-NO-SATISFACE`.
- **Specs corregidas:** 0 — no hubo `COMMIT-3`.

**Lo que este acto no hizo:** no cargó al motor, no abrió Ola 6, no descargó
nada, no tocó `milpa/tramite.yaml`, `procedencia.yaml`, `corridas-*`, medidores
existentes, el manifiesto, `data/raw` ni el inventario de reactivos, y no editó
instrucciones. No reabrió las filas `C` de `R7.3` ni `D` de `R7.4`.
