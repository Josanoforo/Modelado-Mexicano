# DIN · lote ENIF 2024 · ENMIENDA-1 — adjudicación secundaria de los 5 pares con `formalidad` en su propio estrato «universo T»

> `ACTO GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1`, 22/sep/2026, CAJA, rama
> `acto/gen2-din-lote-enif2024-secundaria-1`. Archivo propio: la spec v1.0
> (`DIN-lote-enif2024-spec-v1_0.md`, sha256 `64bb52f2…`) queda **intacta, no
> se edita**. Ejecuta la opción A de `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01`
> (FIRMADA, asentada en `#1003`).
>
> **Contrato ejecutable:** `data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001/spec.yaml`,
> generado a mano (no hay flag de `genera_specs.py` para un CALC secundario —
> verificado por lectura completa de ese script, D-18 latitud de cableado);
> el código que mide es `medidor.py` del mismo CALC, depositado byte a
> byte. **Ningún parámetro vive en dos sitios.**
>
> **El primer resultado que produzca este procedimiento es el que se reporta.**

## 1 · Qué mide y por qué es un estrato aparte

Los cinco pares `formalidad × {sexo, edad, escolaridad, localidad,
cuenta_formal}` quedaron `NO-EMITIBLE` en la spec v1.0 (§3, A-bis 4:
`formalidad` cubre 68.97 % del universo poblacional — universo restringido,
C2 no compone contra ejes de universo completo). `GEN2-DIN-LOTE-C2-RESTRINGIDO-1`
selló un piso alternativo para esos mismos cinco pares, restringido al
universo **T = quien trabaja** (`P3_13` en 1..7 en 2024; `P3_10` en 1..6 en
2021 — la variable existe en las dos olas, es uno de los seis ejes del
árbitro desde la spec v1.0 §1): `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001`, 5/5
pares, 28/28 celdas con punto e IC95, oro contra el árbitro GEN2
`REPRODUCE` a 0.0.

Este CALC adjudica esos 28 pares-celda contra ese piso, dentro del **mismo**
universo T — nunca contra el universo poblacional (A-bis 4, misma
declaración que C2-RESTRINGIDO). El resultado es un estrato **aparte**: no
se suma al ΔMAE primario del lote (5 pares primarios, 44 celdas) ni cambia
la frase de producto de las 44 celdas — por construcción, no por acuerdo:
los RESULT de este CALC llevan el prefijo `RESULT-DIN-LOTE24-ADJ-T`, que no
aparece en ningún cómputo de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001` (el
CALC primario nunca lee este prefijo; test §5).

## 2 · Universo T, por texto

`T` = personas elegidas de 18 años y más de `TMODULO`, bajo régimen
**ARBITRO-2024** (todo el marco, sin filtro de `TLOC`, «fuera» declarado por
eje — el mismo régimen que selló `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` y
que la firma real de Q2 fija para toda comparación contra el árbitro, §4),
**con `formalidad` declarada** (no `FUERA`): `P3_13` en {1..7} en 2024,
`P3_10` en {1..6} en 2021 (categoría `9`/no sabe y blanco por secuencia,
fuera de T). Ninguna fila se descarta: fuera de T, cada eje vale `FUERA` —
la misma técnica que `_ola_desde_df` de `C2-RESTRINGIDO`, generalizada aquí
a las dos olas (2021 y 2024) en vez de sólo 2024, porque el bootstrap debe
sortear sobre el marco de diseño **entero** y no sobre un subconjunto ya
recortado (si se recorta antes de sortear, una UPM sin ninguna fila en T
desaparece de la lista de llaves `EST\tUPM` y desplaza toda la secuencia de
remuestreo — el mismo defecto que ya se midió una vez reusando el bootstrap
de la casa, `GEN2-CELDA-D-PILOTO-3-COMMIT-1-v1_1`).

## 3 · El piso C2R, citado — y sus réplicas, re-derivadas

El **punto** de cada una de las 28 celdas se **cita** por id de RESULT desde
`CALC-C2-RESTRINGIDO-IC-ENIF2024-0001/resultados.json` (input `origen: repo`,
`IN-C2R-SELLADO`; los 28 ids viven en `spec.yaml::parametros.c2r_result_ids`).
Ese CALC no persiste sus réplicas bootstrap (sólo el punto y el IC95
resumidos), así que las **réplicas** del piso se **re-derivan** aquí — «con
el mismo procedimiento», PIEZAS §5 del encargo — importando
`piso_log_aditivo` (vía el `medidor.py` sellado de C2-RESTRINGIDO, por
sha256, nunca copiado) sobre marginales de UN eje dentro de T que este CALC
deriva de su propia ola 2024 (mismo régimen ARBITRO-2024, mismo universo T,
mismo seed `PCG64(42)`: determinista, reproduce bit a bit el sorteo de
C2-RESTRINGIDO). El **punto** re-derivado con la misma fórmula se compara
contra el punto citado como control (`REPRODUCE` si la peor diferencia
absoluta ≤ tolerancia declarada en `spec.yaml`); el punto **oficial** que se
adjudica es siempre el **citado**, nunca el re-derivado.

## 4 · Régimen de universo — corrección de cita (logística, no premisa)

El encargo de este acto (§1) y la propia `FP-…4e12-01` (ya `FIRMADA`) citan
«régimen ARBITRO-2024, firma Q2 (`FP-…6c10-04`)». `…6c10-04` responde **Q3**
(agregador de L, tema ajeno). La firma real de **Q2** (régimen de universo
del lote) es `FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-03`, **FIRMADA**
(`ADR-260922-GEN2-TRAMITE-FIRMAS-6-7c2c-01`); su verbatim en la nota de
cierre de ese acto (`forense/notas/2026-09-22-GEN2-TRAMITE-FIRMAS-6-cierre.md`,
tabla P3): «Fija régimen ARBITRO-2024 para comparaciones contra el árbitro;
PILOTO-1 sólo dentro de sus celdas-D ya selladas.» El intercambio de
etiquetas Q2/Q3 entre `…6c10-03` y `…6c10-04` ya fue declarado una vez por
ese mismo acto como «logística de citación, no premisa sobre qué se mide».
Este CALC compara contra el árbitro (su piso viene de un CALC sellado bajo
ARBITRO-2024): usa **ARBITRO-2024** para las dos olas — la premisa
sustantiva del encargo se sostiene; sólo se corrige el id de la firma
citada. No es PARO (A.12/§0: verificación de premisas, logística).

## 5 · Procedimiento de réplicas — idéntico al lote

`n_h` UPM con reemplazo dentro de cada estrato, generador `PCG64(42)`,
estratos y UPM en orden lexicográfico, 10 000 réplicas — la misma receta de
`enif_lote.py::replicas()` y de `C2-RESTRINGIDO::replicas_t()`, reescrita en
este `medidor.py` (no importada como función porque opera sobre la ola T de
ESTE CALC, que ninguno de los dos sellados construye) pero con la fórmula
verbatim. Contendientes, misma familia del lote, sin reestimar nada:

| candidato | fórmula | procedencia |
|---|---|---|
| `C2` (piso) | citado de `CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` (punto); réplicas re-derivadas con `piso_log_aditivo` | citado + re-derivado |
| `P2` | persistencia: cruce 2021 dentro de T (`cruce_t`, nuevo) | derivado |
| `R1` | `expit(logit C2 + δ21)` | `tools/duelo/cruces_familia.py::desplazada`, importado |
| `R2` (retador primario) | `expit(logit C2 + ½·δ21)`, **λ = ½ fija** (igual que los 14 pares primarios: no se estima) | ídem |
| `R3` | raking a tres vías, tabla 2021 (a,b,D) a los márgenes T de 2024 (a,D)/(b,D) | `tools/lote_enif2024/lote_familia.py::ipf_3vias`, importado |

`R` = el cruce **observado** de ENIF 2024 dentro de T — código nuevo de este
CALC (`cruce_t()`), porque `C2-RESTRINGIDO` prohíbe por diseño cualquier
función de cruce (su propia guardia AST, regla R7) y `enif_lote.py::cruce()`
no conoce el universo T.

## 6 · Criterio y `INDECIDIBLE` — verbatim de la spec v1.0 §7

**Regla v0.3, sin cambio:** `Δ = MAE(C2) − MAE(R2)` en pp, sobre las celdas
**puntuadas** (`n ≥ 200` en las dos olas, dentro de T), IC95 por réplica
(misma réplica k en `R`, `C2` y `R2`). `IC95inf > 0.5` → `VENCE-RETADOR`;
`0 < IC95inf ≤ 0.5` → `PROPUESTA-CON-RESERVA`; incluye 0 →
`NADIE-VENCE` (con el signo del superior). La misma regla, rotulada
`SECUNDARIA`, se aplica a `P2`, `R1`, `R3` y a cada celda por separado.
Calcular dos IC y restarlos está prohibido. `cuenta_formalxformalidad` es el
par que el encargo señala como posible colineal (§6, LATITUD): si su
marginal T de cualquiera de sus dos ejes cae en `{0,1}` o sin filas, la
celda es `NO-CONSTRUIBLE` por declaración (`permite_no_estimable`), nunca
NC-forzada a un valor — decisión ya tomada por dirección (recomendada), no
se pregunta a mesa de nuevo.

## 7 · Rótulo PROSPECTIVA / RETROSPECTIVA — verificado, no supuesto

El SUPUESTO de la cabecera del encargo («R de estos 5 pares ya fue derivado
en COMMIT-3 del lote») es **falso**: `forense/notas/2026-09-21-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-cierre.md`
§1 dice, verbatim, que los pares con `formalidad` salieron
`NO-ADJUDICABLE-SIN-PISO` — «no existe comparador R fuera de los 5 pares
primarios en este CALC»; sólo se calculó `P2` descriptivo
(`SIN-PISO-SOLO-COBERTURA`). `R` restringido a T, además, nunca pudo haberse
derivado antes de este acto porque el propio piso T (`CALC-C2-RESTRINGIDO`)
no existía. **Las 28 celdas se rotulan `PROSPECTIVA`** — la rama que el
propio encargo preveía como mejor si el supuesto resultaba falso, y así se
dice.

## 8 · Test declarado — estrato T fuera del ΔMAE primario, por construcción

`tests/test_lote_enif2024_adjudicacion_t.py` prueba, sobre el
`resultados.json` sellado de `CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001` (el
CALC primario, ya sellado, lectura únicamente): ningún id de ese archivo
empieza con `RESULT-DIN-LOTE24-ADJ-T` (`grep` sobre el JSON, control
positivo: el propio archivo de este CALC secundario sí tiene 100+ ids con
ese prefijo). Prueba además, sobre el `medidor.py` **primario** (lectura de
su fuente, sin ejecutarlo), que no importa ni referencia el `medidor.py` de
este CALC secundario. Corre como huérfano en CI (`ci_guardias
--ejecuta-huerfanos`, D-21).

## 9 · Lo que no cambia, lo que no decide

La spec v1.0 sigue intacta y sigue rigiendo los 14 pares y las 44 celdas
primarias. Este CALC no adopta nada (`cuenta_gen2 = SI`, no adopta, igual
que C2-RESTRINGIDO); no reabre el veredicto primario (`PROPUESTA-CON-RESERVA`,
`R2` sobre 5 pares/44 celdas); no toca `milpa/`; no deriva ningún cruce de
ENIF 2024 fuera de `cruce_t()` sobre los 5 pares autorizados (PARO a). El
sucesor natural (si algún par tiene ganador `VENCE-RETADOR`) es una firma de
mesa que decida si el estrato T se adopta como estimador de esas celdas —
NO decidido aquí (universo restringido: sesgo de clase declarado, quien
trabaja no es la población general).
