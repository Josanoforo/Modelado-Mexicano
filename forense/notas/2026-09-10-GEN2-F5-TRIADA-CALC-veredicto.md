# `ACTO GEN2-F5-TRIADA-CALC` — el veredicto

**RESULTADO PRIMARIO: `SIN-GANADOR-UNICO`, sobre `U3 = 3` celdas del marco
de 14.**

Ningún contendiente —`L_SOLO`, `L_CORPUS` ni `M`— gana sus dos
comparaciones pareadas bajo la banda `δ = 0.5 pp` pre-registrada. El panel
no permite coronar a nadie, y la firma de mesa autorizaba expresamente esa
salida: *"No existe obligación de coronar a nadie."*

**Fecha:** 10/sep/2026 · **Entorno:** NUBE, Opus, cero microdato / cero red
/ cero llamadas nuevas a ningún modelo · **Base:** `origin/main = c439065`
(merge de `PR #680`, `ACTO GEN2-R-COMPLETA-MARCO`) · **Encargo:**
`forense/encargos/2026-09-10-GEN2-F5-TRIADA-CALC.md` (0-bis A.3, verbatim) ·
**Corrida:** `data/corrida0/CALC-TRIADA-0001/` — `preflight VERDE` →
`run exit=0` → `verify REPRODUCE` (`CONTEXTO=IDENTICO`), 259 `RESULT`,
sello `sha256 b58262722753b65d4c08b5ce64f7326fd3886f32fefc20d354e37a8129acbe38`.

**Compuerta: 4/4 cumplida por producto** contra `origin/main` antes de
escribir nada — extractor L v1.3 (`ecfbd849…`) + manifiesto de extracción
(`a1e5d609…`); spec TRIADA v1.1 sellada (`db6b24c5…`); `UR` congelado 14/14
(`840fc68c…`) con los 14 `CALC-R` sellados; snapshot M v1.0 con firewall por
celda (`b53ac6d5…`).

---

## 1 · Tabla MAE y ranking puntual

Todo en **puntos porcentuales**, sobre las **mismas 3 celdas** para los tres.

| Contendiente | `MAE` (pp) | Ranking puntual |
|---|---:|:--:|
| `M` (motor) | **0.1758** | 1 |
| `L_SOLO` (LLM solo) | **0.1990** | 2 |
| `L_CORPUS` (LLM con corpus) | **0.3466** | 3 |

`RESULT-TRIADA-RANKING-PUNTUAL = "M (MAE=0.1758 pp) < L_SOLO (MAE=0.1990 pp)
< L_CORPUS (MAE=0.3466 pp)"`.

**Esto es un ranking descriptivo, no una adjudicación.** La spec sellada
(§4) obliga a reportarlo siempre y a **no fusionarlo** con la escala de
banda: las tres distancias caben holgadamente dentro de `δ = 0.5 pp`, es
decir, los tres contendientes aciertan el árbitro dentro de dos décimas a un
tercio de punto porcentual en estas tres celdas. El orden 1/2/3 no
sobrevive a su propia incertidumbre — que es exactamente lo que dicen las
pareadas de §2.

## 2 · Las tres comparaciones pareadas, con IC95 y veredicto

`Δ(A,B) = media(error_A − error_B)`; **negativo favorece A**. Bootstrap
pareado sellado: `seed = 42` (heredada, `FP-168`), **10,000 réplicas**,
IC95 por cuantil tipo 7, **un solo vector de índices de celda por réplica
reutilizado por los tres contendientes** (`RESULT-TRIADA-BOOTSTRAP-INDICES-COMPARTIDOS
= SI`), y **el mismo `U3` para las tres** (`RESULT-TRIADA-PAREADAS-MISMO-U3 = SI`).

| Comparación | Δ puntual (pp) | IC95 (pp) | Veredicto (escala §4) |
|---|---:|---|---|
| `Δ(L_CORPUS, L_SOLO)` | **+0.1476** | `[−0.1000, +0.5000]` | **`INCONCLUSO`** |
| `Δ(M, L_SOLO)` | **−0.0231** | `[−0.0694, +0.0694]` | **`EMPATE-PRACTICO`** |
| `Δ(M, L_CORPUS)` | **−0.1708** | `[−0.4306, +0.0306]` | **`EMPATE-PRACTICO`** |

**Escala global (§4), aplicada mecánicamente:** para coronar a `X` hacen
falta sus **dos** comparaciones ganadas más cobertura no menor que la de sus
rivales. `M` empata sus dos; `L_SOLO` empata una y queda inconcluso en la
otra; `L_CORPUS` no gana ninguna. **Ninguno satisface la condición →
`SIN-GANADOR-UNICO`.** No hay `NO-ADJUDICABLE-POR-CONTROL`: los tres
controles de identidad/contaminación salieron limpios (§7).

## 3 · Cobertura sobre todo `U0`

`|U0| = 14` · `|UR| = 14` (techo de lo adjudicable) · `|U3| = 3`.

| | `L_SOLO` | `L_CORPUS` | `M` |
|---|---:|---:|---:|
| Celdas de `UR` con punto válido | **6 / 14** | **3 / 14** | **14 / 14** |
| Réplicas `EXTRAIBLE` (de 112 = 14 × k=8) | 33 | 23 | n/a |
| Réplicas `NO-EXTRAIBLE` | 75 | 89 | n/a |
| Réplicas `AMBIGUA` | 4 | 0 | n/a |
| Celdas excluidas de `U3` por falta de punto | 8 | 11 | 0 |

Capturas examinadas: **224 / 224**. Una réplica `NO-EXTRAIBLE` o `AMBIGUA`
**cuenta en cobertura**: no se sustituyó por cero ni se descartó en
silencio. Las 8 réplicas de una celda **no** se contaron como 8 tareas
independientes: colapsan a un punto por celda (mediana de las `EXTRAIBLE`)
antes de cualquier promedio.

`U3 = {FAM-M-05, FAM-M-06, FAM-M-07}` — las tres celdas ENIGH de
`recibe_remesas`. **`L_CORPUS` es el cuello de botella**: sólo tiene punto
en esas tres. Las seis celdas `CIV-M-*` (ENVIPE), `DIN-M-01` y `FAM-M-01`
vuelven **0/8 `EXTRAIBLE` en los dos brazos**; `TRA-M-02/03/07` tienen punto
de `L_SOLO` pero **0/8 en `L+corpus`**.

**Nota material, no cosmética:** esas exclusiones no son fallas del
extractor. El extractor v1.3 está validado contra el formato real (`ACTO
GEN2-F5-EXTRACTOR-L-v1`) y este acto **re-derivó** las 224 extracciones y
las coteja captura por captura contra el manifiesto sellado de `ENCARGO 1/5`:
**0 discordancias**. Lo que hay en esas capturas es, mayoritariamente,
`ANCLA-RECHAZO` y `SIN-ANCLA` — el modelo **se negó a dar una estimación
puntual** o no la ancló. Es un dato sobre el desempeño de `L`, no un fallo de
medición: un contendiente que se abstiene no tiene punto, y la cobertura es
donde eso se reporta.

## 4 · Tabla por celda (fila durable, las 14)

`R`, `L_SOLO`, `L_CORPUS`, `M` en escala `[0,1]`; errores en **pp**;
`k_LS`/`k_LC` = réplicas `EXTRAIBLE` de 8.

| celda | `R` | `L_SOLO` | `err LS` | `L_CORPUS` | `err LC` | `M` | `err M` | `k_LS` | `k_LC` | firewall | `U3` |
|---|---:|---:|---:|---:|---:|---:|---:|:--:|:--:|---|:--:|
| CIV-M-01 | 0.258999 | — | — | — | — | 0.294313 | 3.5314 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| CIV-M-02 | 0.243400 | — | — | — | — | 0.294313 | 5.0913 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| CIV-M-04 | 0.243668 | — | — | — | — | 0.294313 | 5.0645 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| CIV-M-10 | 0.204934 | — | — | — | — | 0.294313 | 8.9379 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| CIV-M-12 | 0.208112 | — | — | — | — | 0.294313 | 8.6201 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| CIV-M-13 | 0.194612 | — | — | — | — | 0.294313 | 9.9701 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| DIN-M-01 | 0.155581 | — | — | — | — | 0.174804 | 1.9223 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| FAM-M-01 | 0.557193 | — | — | — | — | 0.457707 | 9.9486 | 0 | 0 | LIMPIO-DE-OBJETIVO | NO |
| **FAM-M-05** | 0.047459 | 0.045000 | **0.2459** | 0.046000 | **0.1459** | 0.045694 | **0.1765** | 8 | 8 | LIMPIO-DE-OBJETIVO | **SI** |
| **FAM-M-06** | 0.047285 | 0.045000 | **0.2285** | 0.050000 | **0.2715** | 0.045694 | **0.1591** | 7 | 8 | LIMPIO-DE-OBJETIVO | **SI** |
| **FAM-M-07** | 0.043775 | 0.045000 | **0.1225** | 0.050000 | **0.6225** | 0.045694 | **0.1919** | 8 | 7 | LIMPIO-DE-OBJETIVO | **SI** |
| TRA-M-02 | 0.126025 | 0.140000 | 1.3975 | — | — | 0.085118 | 4.0907 | 1 | 0 | LIMPIO-DE-OBJETIVO | NO |
| TRA-M-03 | 0.044538 | 0.125000 | 8.0462 | — | — | 0.085118 | 4.0580 | 5 | 0 | LIMPIO-DE-OBJETIVO | NO |
| TRA-M-07 | 0.071815 | 0.146000 | 7.4185 | — | — | 0.085118 | 1.3303 | 4 | 0 | LIMPIO-DE-OBJETIVO | NO |

**Notas de corte** (durables, `RESULT-TRIADA-<celda>-NOTA-DE-CORTE`): las
ocho primeras salen por «sin punto válido de `L_SOLO`/`L_CORPUS`»; las tres
`TRA-M-*` por «sin punto válido de `L_CORPUS`»; las tres `FAM-M-*` entran
por «R sellado + punto válido de los tres + no contaminada». `DIN-M-01`
arrastra además la reserva `FP-371` sobre su `EE`/`IC` (diseño aproximado no
autorizado como *ground truth* inferencial) — **irrelevante para este
resultado**, porque la celda ya está fuera de `U3` por falta de punto de `L`,
y la métrica primaria usa el punto de `R`, no su `EE`.

Los errores de `M` **fuera** de `U3` se reportan por transparencia y **no
entran a ningún `MAE`**: `M` emite el mismo punto para las seis `CIV-M-*`
(`0.294313`, la regla `civico.denuncia.miedo_desconfianza` calibrada de
ENVIPE 2025) y para las tres `TRA-M-*` (`0.085118`), contra árbitros que
varían entre 0.19 y 0.26 — pero no hay contra qué compararlo, porque en esas
celdas ni `L_SOLO` ni `L_CORPUS` tienen punto.

## 5 · Secundaria TRANSFERENCIA

**`SIN-UNIVERSO`.** Bajo el criterio mecánico de §6 de la spec sellada
—heredado de `F5 v1.0` §2: *cita con año ≥ ola de la celda, o sin año
determinable, excluye*— **las 14 celdas de `UR` quedan
`M-NO-COMPARABLE-EN-TRANSFERENCIA`**: `M` calibra de ENVIPE 2025 (las seis
CIV), ENIGH 2022 (las tres FAM-M-05/06/07), ENCIG 2025 (las tres TRA),
ENIF 2024 (FAM-M-01) y ENNViH ola 2 / ENIF 2024 (DIN-M-01) — todas olas
iguales o posteriores a la ola que la celda evalúa. El universo secundario
queda vacío (`N = 0`) y la pareada secundaria sale `SIN-UNIVERSO-PAREADO`.

Esto **no** es un hallazgo nuevo: `F5-contrato-triada-spec-v1_1.md` §6 ya lo
anticipaba por escrito para `FAM-M-05/06/07`, `TRA-M-03/07` y las seis
`CIV-M-*`. Este acto lo verifica sobre el snapshot real y lo extiende a las
14. **La secundaria no veta ni reemplaza la primaria** y nunca fue condición
de `GANADOR-TRIADA-X`.

## 6 · `B` — sólo como diagnóstico, y sí aporta información

`B` no tiene fila por `id_celda` de marco-M: **0**, consistente con
`procedimiento-scoring-v1_2.md` §4. Pero `CALC-B-0001` sí trae la serie
ENIGH de remesas, y el control de este acto encuentra que **esas cifras
coinciden al grano de float con el propio `R` de las tres celdas de `U3`**:

- `RESULT-B-ENIGH-2016-P` == `R(FAM-M-05)` = `0.04745859252351374`
- `RESULT-B-ENIGH-2018-P` == `R(FAM-M-06)` = `0.04728548395278385`
- `RESULT-B-ENIGH-2020-P` == `R(FAM-M-07)` = `0.04377543852935772`

**Lectura diagnóstica:** en este panel `B` **no es un piso independiente** —
es el mismo número que el árbitro, medido por la misma vía. No hay
*baseline* contra el cual calcular `skill` sin circularidad, y por eso `B`
queda fuera de `U3`, del ranking, de la adjudicación y de cualquier veto
(§7), como la spec ya mandaba. Dato adyacente, del mismo `CALC-B-0001`:
`RESULT-B-ENIGH-2022-P = 0.04569409956405095` es, redondeado, el punto que
`M` emite para las tres celdas (`0.045694`) — es decir, **`M` en `U3` está
reproduciendo la tasa base ENIGH 2022**, no derivando una predicción
específica por ola.

## 7 · Controles, medidos aquí y no heredados

| Control | Resultado |
|---|---|
| Identidad de las 224 capturas contra el manifiesto sellado de `F5-RECAPTURA-L` (`sha256` + tripleta `id_celda`/`variante`/`índice` en nombre, manifiesto y JSON) | **0 fallas** |
| Re-derivación de la extracción con el extractor v1.3 sellado, cotejada captura por captura contra el manifiesto de `ENCARGO 1/5` | **0 discordancias** (224/224) |
| Celdas `CONTAMINADA-POR-OBJETIVO` en `UR` | **0** — las 14 `LIMPIO-DE-OBJETIVO` en el snapshot, y el control propio `punto_M == R` da `DISTINTO-DE-R` en las 14 |
| Mismo `U3` para las tres pareadas | **SÍ** |
| Mismos índices de bootstrap para los tres contendientes | **SÍ** |

Por eso el veredicto **no** es `NO-ADJUDICABLE-POR-CONTROL`: el control no
se rompió. Lo que falta es cobertura, no limpieza.

## 8 · Sensibilidad pre-registrada, y el borde de la banda

La spec sellada pre-registra **una** regla de decisión (la escala exhaustiva
de §4) y **ninguna** sensibilidad adicional; este acto no inventa otras.
Pero hay un hecho aritmético del número sellado que debe reportarse:

**`Δ(L_CORPUS, L_SOLO)` tiene `IC-HI` exactamente en el borde de la banda.**
El valor sellado es `+0.5000000000000004 pp`. La réplica de bootstrap que lo
produce es la que remuestrea tres veces `FAM-M-07`, cuya diferencia pareada
es `(0.050 − R) − (0.045 − R) = 0.005` → **exactamente `+0.5 pp`** en
aritmética decimal; el `…04` final es residuo de coma flotante de calcular
`|L − R|` dos veces con el mismo `R`.

Aplicada al número sellado, la escala da la cuarta fila (`INCONCLUSO`),
porque `ic_hi ≤ 0.5` es falso por ese residuo. Aplicada al valor exacto,
daría la tercera (`EMPATE-PRACTICO`). **El veredicto global es invariante a
esa elección:** con `EMPATE-PRACTICO` en esa pareada, `L_CORPUS` seguiría sin
`A-GANA` y `L_SOLO` sin `B-GANA`, así que ninguno gana sus dos y el resultado
sigue siendo `SIN-GANADOR-UNICO`. Se reporta el veredicto que el
procedimiento sellado produjo, sin editarlo; el borde queda asentado como
`NC-0147` para que una spec futura declare tolerancia numérica en los
límites de la banda.

## 9 · Límites — lo que este resultado NO autoriza

Ninguna de estas líneas es opcional; la firma de mesa las fijó antes del
resultado.

1. **Cobertura, no empate de fondo.** `U3 = 3/14` (21% del marco). El
   `SIN-GANADOR-UNICO` se apoya en tres celdas de **una sola familia**
   (ENIGH `recibe_remesas`, olas 2016/2018/2020) y de **una sola escala**.
   No es una afirmación sobre el marco de 14, ni sobre las familias ENVIPE,
   ENCIG, ENCUCI, ENIF o ENNViH — en esas, dos de los tres contendientes
   simplemente no compitieron.
2. **`L` se abstuvo, no falló.** En 11 de 14 celdas `L_CORPUS` no produjo
   estimación puntual anclada, y en 8 tampoco `L_SOLO`. Eso es un dato de
   desempeño operacional que la métrica de error **no captura**: el `MAE` se
   calcula sólo donde los tres respondieron.
3. **`M` en `U3` reproduce una tasa base.** Su punto es el mismo para las
   tres celdas (`0.045694`, ENIGH 2022) — que gane el ranking puntual sobre
   tres olas cuyo árbitro varía entre 0.0438 y 0.0475 dice que la serie es
   plana, no que el motor esté modelando la ola.
4. **Nada de esto autoriza** causalidad · «todos los mexicanos» · «todos los
   LLM» · ningún modelo o versionado futuro · ninguna tarea fuera del marco ·
   ni declarar que el corpus «explica» diferencia alguna · ni que el motor
   sea universalmente mejor.
5. **Lectura permitida, la única (P4 del encargo, verbatim):** *"El panel no
   permite identificar un ganador único bajo la magnitud, incertidumbre y
   cobertura pre-registradas."*
6. **No se adopta nada.** Este acto no mueve ninguna cifra de
   `milpa/tramite.yaml`, no adopta al motor en ningún consumidor, no toca
   capturas, extractor, spec TRIADA, `R` sellados, snapshot `M`, `milpa/`,
   marcador histórico, `F5 v1.0`, `B` ni corpus.

## 10 · Qué sigue (P5 del encargo, por diagnóstico y no por preferencia)

El encargo fija el sucesor según el diagnóstico, y el diagnóstico aquí es
**`SIN-GANADOR-UNICO`**:

> *"Si `SIN-GANADOR-UNICO`: estudiar la fuente dominante de incertidumbre o
> ampliar prospectivamente el marco bajo una spec nueva. No añadir celdas a
> este CALC."*

- **`F6 · COSECHA` NO procede.** Requiere ganador único con cobertura
  suficiente; no hay ninguna de las dos cosas.
- **La fuente dominante de incertidumbre está medida y nombrada:** la
  abstención de `L` (11/14 celdas sin punto de `L_CORPUS`), no la varianza
  del árbitro ni la del motor. Un sucesor que quiera adjudicar esta pregunta
  tiene que atacar eso primero — bajo **spec nueva**, no ampliando este CALC.
- Queda asentado en `NC-0146`.
