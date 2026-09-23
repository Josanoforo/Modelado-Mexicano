# Cierre de la reserva de ENCIG 2025 · dos cruces, cuatro contendientes, una comparación primaria · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-DUELO-ENCIG2025-CIERRE-1`, 23/sep/2026, CAJA, rama
`acto/gen2-duelo-encig2025-cierre-1`, 0-bis `657c88d1`. Congelada **sin abrir ningún cruce de
ENCIG 2025**: ninguna cifra de 2025 por dos variables se ha derivado en ningún commit del árbol
para los dos cruces de esta spec (barrido §2). Lo único de 2025 que esta spec cita son
marginales **de un eje ya sellados** por otros actos (`CALC-ARBITRO-MARGINALES-ENCIG2025-0001`,
bloque público de `milpa/tramite-ola5-propuesta-v0.yaml`), que no son la cantidad reservada.

Firma de mesa que la habilita, verbatim en `forense/firmas-pendientes.tsv`, fila
**`FP-260923-GEN2-DUELO-ENCIG2025-CIERRE-1-657c-01`** (FIRMADA 23/sep/2026, mesa en sesión):
«Mesa autoriza abrir los cruces reservados de ENCIG 2025 en un solo acto con todos los
contendientes sellados antes del COMMIT-2 (C2, C-ASTRA #1030, C-ENCOGIDA misma regla del piloto
4, C7 si existe); comparación primaria = diferencia de error medio con IC por réplica; umbral = el
del piloto 4; vocabulario B-bis del piloto 4. Un retador que venza con IC que despeje va a firma
de adopción con su nombre; si nadie vence, la serie de retadores de la casa sobre ENCIG se cierra
con ese dictamen y se publica en el informe v1.3.»

Vigentes y citadas, no re-firmadas aquí: firma del 17/sep (un piso no vencido es el estimador
adjudicado de su celda); E.6 (una apertura sirve a todos los contendientes sellados antes);
FP-393 (unidad `evento`: el trámite no es la persona); FP-399/F1-bis (edad 97 es edad real
censurada y queda fuera del eje; 98/99 no especificada).

---

## 0 · Herencia, por identidad de archivo

Esta spec **no** inventa procedimiento: hereda el del piloto 4
(`forense/prereg-caja/TRA-evade-norma-cruces-encogida-spec-v1_0.md`, sidecar `342aa0d1…`, y su
enmienda `TRA-evade-norma-cruces-encogida-enmienda-2.md`) y cambia **solo** instrumento, desenlace,
ejes y fuente de los deltas históricos. Lo heredado se importa por sha256, no se copia:

| pieza | archivo sellado | sha256 | qué se toma |
|---|---|---|---|
| regla de λ | `data/corrida0/CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-EMISIONES-0001/medidor.py` | `6d4668fd…6b59` | la función `_lambda_cruce`, extraída por AST de esos bytes y ejecutada tal cual |
| regla primaria | `data/corrida0/CALC-TRA-EVADE-NORMA-CRUCES-ENCOGIDA-ARBITRO-CRUCES-0001/adjudicacion.py` | `ed6e80b8…647d` | la función `_estado_gana` (versión corregida por la enmienda 2, `7ffa0a0e`), extraída por AST |
| receta del cruce ENCIG | `tools/encig_cruces_historicos.py` | `31d7cf3b…8f83` | `_load_wave`, `_bootstrap`, `_summary`, `_logit`: la misma receta que produjo los deltas 2021/2023 sellados |

La receta ENCIG cambió de blob después de sellar `CALC-ENCIG2023-CRUCES-HISTORICOS-0002`
(`script_sha256_congelado 3899d086…` → hoy `31d7cf3b…`, commits `883ced7d`/`601e5c95`/`e7108881`
del 19/sep, que añadieron identidad y selección, no receta). No se supone que el cambio sea
inocuo: **se prueba**. El control de oro (§6 b) corre la receta de hoy sobre ENCIG 2023 y exige
reproducir P, N, IC y DELTA sellados de los dos cruces a `1e-10`.

## 1 · Estimando, universo, celdas

**Estimando.** Proporción de **pagos ordinarios del servicio de luz** (`N_TRA == 01`) hechos por
canal digital (`P7_3 ∈ {4,5}`: internet/app · cajero o kiosco inteligente) entre los pagos hechos
por un canal válido (`P7_3 ∈ {1,2,4,5,6}`), por celda de dos ejes, ENCIG 2025. **Unidad:
TRÁMITE** (quien pagó doce veces contribuye doce veces; FP-393 → `unidad_objetivo: evento`).
Ponderador `FAC_TRA > 0`; diseño `EST_DIS × UPM_DIS`; unión trámite→persona por `ID_PER`, `m:1`
validada. Es el mismo objeto que la regla del motor `tramite.gobierno_digital.util_sin_coercion`
y que el piloto 3; no es «gobierno digital» en general ni confianza en el Estado.

**Texto de pregunta, no nombre de variable (A.15).** Reactivo 7.3 (canal de pago), nueve opciones
y códigos idénticos en 2021/2023/2025; `N_TRA = 01` es «el pago ordinario del servicio de luz?»
en las tres olas; el catálogo 2025 inserta el trámite `15` y desplaza `15–22 → 16–23`, fuera del
estimando. Constancia primaria: `NC-0355` cerrada `CAMBIO-MENOR` (PR #924), citada por
`GOB-gobierno-digital-exe15-spec-v1_1.md:3,13`. `SEXO` (1 hombre, 2 mujer), `EDAD` (años
cumplidos) y `NIV` (nivel de escolaridad) de `encig{ola}_02_residentes_sec_2.csv`, las mismas
variables que los CALC históricos declaran (`CALC-ENCIG2023-CRUCES-HISTORICOS-0002/spec.yaml`).

**Ejes y celdas** (idénticos a la receta y a los históricos):
`EDAD` `18-29 · 30-44 · 45-59 · 60-96` (97 y 98/99 fuera: FP-399/F1-bis; la etiqueta pública
`60+` opera como `60-96`, `CALC-ARBITRO-MARGINALES-ENCIG2025-0001`, FP c09b-01) ·
`ESCOLARIDAD` `HASTA-PRIMARIA {0,1,2} · SECUNDARIA {3} · MEDIA-SUPERIOR {4,5,6,7} · SUPERIOR {8,9}` ·
`SEXO` `1 · 2`.

**Universo de R por par:** casos completos en los dos ejes del par (receta: `complete =
eje_a.notna() & eje_b.notna()`); el residuo del otro eje queda fuera, contado. En `edad × sexo`
ese residuo es la edad fuera de 18-96 (104 trámites en 2021, 107 en 2023; es la causa de la
marca `PARO-COHERENCIA-UNIVERSO` que los CALC históricos imprimen para `SEXO-EDAD`, que aquí es
el universo declarado, no un defecto).

## 2 · Los dos cruces, y por qué son dos y no tres

`data/corrida0/marcador-segmento.tsv` (origin/main `73b7f115`) muestra tres filas
`CRUCE-GRUPO::tramite.gobierno_digital.util_sin_coercion_ejes_encig2025::…` en `RESERVADA`:
`edadxescolaridad`, `edadxsexo`, `escolaridadxsexo`.

- **`edad × escolaridad` NO se reabre.** Su celda-D
  `data/curacion-registro/celdas-d/GOB.gobierno_digital.encig2025.edad_x_escolaridad.yaml`
  (l.84-86) está adjudicada: `veredicto: FALSADOR-DEBIL`, `champion_actual: C2` (firma F3,
  21/sep). E.6: un cruce visto se declara consumido y no se relanza. Que el marcador siga
  mostrándolo `RESERVADA` es una discrepancia del derivador (pregunta a mesa respondida el
  23/sep: «Consumido; NC al marcador»), no una reserva viva.
- **Entran `edad × sexo` (8 celdas) y `escolaridad × sexo` (8 celdas).** Ningún CALC del árbol
  derivó R de 2025 para estos pares: barrido de los 259 directorios `data/corrida0/CALC-*` por
  ids que contengan `SEXO` y (`EDAD` o `ESCOLAR`) con `ENCIG`/`2025` → sólo aparecen
  `CALC-ASTRA-ENCIG-{EDADXSEXO,ESCOLARIDADXSEXO}-0001` (emisiones, sin R),
  `CALC-C2-COMPUESTO-RESERVADAS-0001` (emisión, sin R) y los dos CALC históricos 2021/2023
  (control positivo: el barrido encuentra los cinco conocidos).

Soporte histórico **ex ante**, leído de los CALC sellados: las 16 celdas tienen `n ≥ 200` en 2021
y en 2023 (mínimo 1 239 trámites, `SEXO-ESCOLARIDAD-1-HASTA-PRIMARIA` 2023) y `CAUSA = OK` con
10 000 réplicas válidas. No hay `FUERA-DE-SOPORTE-EX-ANTE`.

## 3 · Contendientes — lista cerrada, por id

Por celda `c = (a, b)` del cruce; `L = logit`, `expit` su inversa.

| id | rol | punto | fuente sellada |
|---|---|---|---|
| **C2** | **PISO** | `expit(L p₂₅(a) + L p₂₅(b) − L p₂₅)`, marginales públicos 2025 sin interacción | `CALC-C2-COMPUESTO-RESERVADAS-0001` (`RESULT-C2COMP-ADOPTA-ENCIG2025-LUZ-{EDADXSEXO,ESCOLARIDADXSEXO}-…`), copiado por id |
| **C7** | RETADOR | `expit(L C2 + δ̄(c))`, `δ̄ = (δ₂₁ + δ₂₃)/2` sin encoger | se emite en COMMIT-2 de `C2` + `DELTA` sellados |
| **C-ENCOGIDA** | RETADOR | `expit(L C2 + λ_cruce · δ̄(c))` | se emite en COMMIT-2; `λ_cruce` §3.1 |
| **C-ASTRA** | RETADOR | modelo normal con τ = 0.15, ω = 0.10 fijos (su spec) | `CALC-ASTRA-ENCIG-{EDADXSEXO,ESCOLARIDADXSEXO}-0001` (PR #1030), copiado por id |
| C1 | REFERENCIA (no adjudica) | `p₂₃(a,b)` directo (persistencia) | `CALC-ENCIG2023-CRUCES-HISTORICOS-0002` `-P`, `-P-IC-LO/HI` |

`δ_t(c) := L p_t(a,b) − L p_t(a) − L p_t(b) + L p_t` sobre el universo común del par: es el
`-DELTA` (y `-DELTA-EE`) sellado de `CALC-ENCIG2021-CRUCES-HISTORICOS-0003` y
`CALC-ENCIG2023-CRUCES-HISTORICOS-0002`. **Nada se re-mide** (§8 del encargo: contendientes por id).
C2 es exactamente la composición de los marginales públicos: recalcularlo desde el bloque
`…_ejes_encig2025` (sexo, edad, escolaridad) y el nacional `0.673393` reproduce los 16 puntos
sellados con diferencia **0** (verificado al redactar). Es el mismo `B25` sobre el que Astra
construye su punto, lo que cumple la condición que la propia spec de Astra impone («el piloto
debe confirmar que su C2 usa estos mismos marginales»).

**IC de las emisiones de la casa (descriptivo, no adjudica).** C7 y C-ENCOGIDA llevan un
intervalo **condicional a C2 fijo**: `expit(L C2 + λ δ̄ ± z · λ · √((EE₂₁² + EE₂₃²)/4))`,
`z = 1.959963984540054`, `λ = 1` para C7. Omite la incertidumbre de los marginales 2025 (C2 no
trae réplicas: su CALC declara `N-CELDAS-CON-IC = 0`, «la incertidumbre no se fabrica»). Tipo
rotulado `CONDICIONAL-C2-FIJO-SOLO-DELTA-HISTORICO`. Con `λ = 0` el intervalo colapsa al punto:
es lo que ese intervalo dice, no un error. C-ASTRA trae el suyo, `PREDICTIVO-CONDICIONAL-
MARGINALES-2025-FIJOS`, y se copia tal cual.

**Lo que se aparta sin abrir, y por qué (E.6).** `S-MEDIO`/`S-LAMBDA` del piloto 3: familia
sustituida por C7/C-ENCOGIDA del piloto 4 (la firma nombra la familia del piloto 4). `L`: no
entra (piloto 4, «sin L»). `C1A` del piloto 3 (compuesto con marginales 2023): no es de la lista
firmada. `TENDENCIA-SERIE` (FP -852f-01): propuesta para marginales, no para cruces. `C6`: no
existe en la familia. Ningún otro CALC sellado emite para estos pares (§2).

### 3.1 · λ — una por cruce, misma regla del piloto 4

```
λ_cruce = τ̂² / (τ̂² + σ̄²)          τ̂² = max(0, Var_entre(δ̄) − σ̄²)
Var(δ̄_i) = (EE₂₁,i² + EE₂₃,i²)/4    σ̄² = media de Var(δ̄_i) sobre las celdas del cruce
Var_entre = varianza muestral (ddof = 1) de {δ̄_i};  k = celdas con δ y EE definidos (k < 2 → λ = 0, K-INSUFICIENTE)
```

Es `_lambda_cruce` del piloto 4, **ejecutada desde sus bytes** con los pares (2021, 2023) en
lugar de (2023, 2024). La λ no se teclea ni se inicializa con ninguna otra (ni la del piloto 3,
`0.8937949410086089`, que es de edad × escolaridad). Si `max(0, ·)` ata, `λ = 0` y
C-ENCOGIDA = C2 en ese cruce: resultado legítimo.

### 3.2 · Admisión de C-ASTRA — (a)–(c) de la ADENDA-1 del piloto 4, celda por celda

`forense/encargos/2026-09-22-GEN2-CELDA-D-PILOTO-4-ENCOGIDA-1-ADENDA-1.md`, verbatim: el CALC
«(a) cite las mismas celdas que la spec del piloto, (b) esté congelado antes de cualquier
lectura de la ola de evaluación (…), y (c) declare punto, IC y tipo de incertidumbre por celda».
Plazo vigente (enmienda 2 del piloto 4): en `origin/main` **antes del COMMIT-2**.

- **(a)** celdas `EDAD ∈ {18-29,30-44,45-59,60-96} × SEXO ∈ {1,2}` y
  `ESCOLARIDAD ∈ {HASTA-PRIMARIA,…,SUPERIOR} × SEXO ∈ {1,2}`, mismo desenlace (`P7_3 ∈ {4,5}` sobre
  `{1,2,4,5,6}`), unidad trámite, `FAC_TRA`; su `B25` es el C2 de esta spec. El recibo #1033
  dejó esto como NC («nadie corrió el cotejo celda por celda contra una spec de piloto»): el
  medidor lo corre en cada emisión (`G-C-ASTRA-A-CELDAS`) y para si falta un id.
- **(b)** sellos del 22/sep (`0ad7f0f8`, `20fdc966`), inputs sólo `origen: repo` (históricos y
  bloque público), `exposicion_historica: CIEGO-A-ENCIG2025-CRUCE-NO-ABIERTO`; ningún R de estos
  pares existe en el árbol (§2). Rótulo: **PROSPECTIVA**.
- **(c)** `-P`, `-IC-LO`, `-IC-HI`, `-NIVEL`, `-TIPO` por celda.

C-ASTRA entra a la **comparación primaria**, como C7 y C-ENCOGIDA: la firma §2 lo nombra entre
los contendientes (esto difiere del piloto 4, donde por decisión posterior fue secundario). Su IC
propio no se empareja con réplicas de R (su spec lo advierte) y sólo se usa en la cobertura
descriptiva (§4.3).

## 4 · R, soporte y adjudicación

**R** (sólo en el árbitro, COMMIT-3): la receta ENCIG sobre `encig25_base_datos_csv`
(`sha256 47daf2f7…9e12`, manifiesto), universo §1, máscaras por celda en el orden de la receta
(`ab, a, b, todo` sobre el universo común del par) más los 11 marginales de un eje sobre su propio
denominador (sexo 2, edad 4, escolaridad 4, total 1), **un solo** bootstrap: 10 000 réplicas,
UPM con reposición dentro de estrato, singleton de certeza, `PCG64(20260919)` (la semilla de los
históricos). `R(c)` = punto; IC 2.5/97.5 con el contrato conservador de la receta (si una réplica
degenera, no se publica IC). `EE(R) = (IC95sup − IC95inf)/3.92`. Se emite `δ₂₅(c)` como
descripción.

**Controles del árbitro antes de adjudicar** (umbrales declarados aquí):
- los 11 marginales de un eje reproducen `CALC-ARBITRO-MARGINALES-ENCIG2025-0001` (`-P`, `-N`) a
  `1e-10` → `REPRODUCE`; si no, `NO-REPRODUCE` y el IC de C2 no se emite;
- la composición de esos marginales reproduce el C2 sellado a `1e-5` (C2 se armó con números
  públicos a seis decimales); si no, igual;
- los sellos de las dos emisiones coinciden (sha256 de `resultados.json` = el de `sello.json`)
  — si no, **PARA** sin leer el cruce.

**IC del piso para el registro de la celda.** El contrato v0.6 de celda-D exige que el campeón
adoptado cite punto **e** IC. C2 no trae IC y sus `DIAG-INF/SUP` están rotulados «NO es un
IC95». El árbitro emite `C2-IC-LO/HI` como percentiles de `expit(L p_r(a) + L p_r(b) − L p_r)`
sobre las mismas réplicas; el punto que se adopta es el sellado. Ese IC **nace con R**: no entra
a la comparación primaria ni a la cobertura prospectiva, y se rotula `NACE-CON-R`.

**Soporte.** `PUNTUADA` si `n ≥ 200` en 2021, 2023 y 2025, IC de R definido y los cuatro puntos
de la comparación primaria (C2, C7, C-ENCOGIDA, C-ASTRA) definidos (tres si C-ASTRA no pasó la
admisión de §3.2: entonces no compite y su `GANA` es `NO-ENTRA`). `FUERA-DE-SOPORTE` global por
cruce si fallan `≥ round(k/3)` celdas: `round(8/3) = 3` en los dos cruces (fórmula del piloto 4).

**Por celda** (descriptivo), cada retador contra C2, condiciones verbatim de
`forense/CAREO-ADV-DUELO-diseno-v2-2026-08-19.md:38`: «INDECIDIBLE si ambos caen dentro del IC de
R o si |d_L−d_M| < 0.5·EE(R)», `d = |candidato − R|` en pp; si no, `GANA-CHALLENGER` o
`GANA-PISO`. El conteo `≥ ¾` es **secundario y descriptivo**, no adjudica (enmienda 2 del piloto 4).

**Comparación primaria, por cruce y por retador `j`:** `ΔMAE_j = MAE(C2) − MAE(j)` sobre las
`PUNTUADA`, en pp. IC por réplica: en cada réplica `r` de R,
`mean_c(|C2(c) − R_r(c)| − |j(c) − R_r(c)|)·100`, con los puntos de los candidatos **fijos** (son
emisiones selladas; es el IC condicional a las emisiones de la enmienda 2 del piloto 4),
percentiles 2.5/97.5. **Umbral 0.5 pp** (el del piloto 4). Regla (`_estado_gana` del piloto 4):
límite inferior `> 0.5` → **vence** (`SI`); `> 0` y `≤ 0.5` → **`PROPUESTA-CON-RESERVA`**; `≤ 0` →
`NO`. Una comparación primaria: seis contrastes (2 cruces × 3 retadores), sin valor-p.

### 4.1 · B-bis y dictamen — declarado antes del dato

Vocabulario del piloto 4, por cruce; `W` = retadores que vencen:
- `W` vacío y el límite superior de `ΔMAE ≤ 0.5 pp` para los **tres** retadores →
  **`CORROBORADA`** (marginales sin interacción es el estimador honesto de celda para estos
  pares; no dice que la interacción no exista en la población).
- `W` vacío y algún límite superior `> 0.5` → **`FALSADOR-DEBIL`**. Si las dos caben, **manda
  FALSADOR-DEBIL**.
- `W = {C-ENCOGIDA}` o `W = {C7}` → **`LIMITA-C2-SOBRE-CUANTO-ENCOGER`** (el hallazgo es cuánto
  encoger; mismo mapeo que el código del piloto 4).
- cualquier otro `W` no vacío (incluido todo `W` que contenga C-ASTRA) → **`LIMITA-C2`**, con los
  ganadores nombrados en `G-GANADORES`.
- cruce `FUERA-DE-SOPORTE` global o sin `PUNTUADA` → **`FUERA-DE-SOPORTE-GLOBAL`**; no cuenta en el
  agregado y no es derrota.

**Qué manda si dos filas caben**, en el cruce y en el agregado: `LIMITA-C2` >
`LIMITA-C2-SOBRE-CUANTO-ENCOGER` > `FALSADOR-DEBIL` > `CORROBORADA` (precedencia del piloto 4).
Un retador con reserva (límite inferior entre 0 y 0.5 pp) no vence: el piso sigue no vencido, y
el caso se lleva a mesa como pregunta, no como adopción.

**Si el falsador NO refuta** (nadie vence): con `CORROBORADA` la serie de retadores de la casa
sobre ENCIG se cierra corroborando al piso; con `FALSADOR-DEBIL` se cierra igual, pero el
dictamen dice que el aparato no tenía poder para descartar mejoras de hasta el límite superior
del IC — «acotada» por ese número, no «corroborada». Firma §2: en los dos casos se publica en el
informe v1.3.

### 4.2 · Registro (celda-D) y adopción

Una celda-D nueva por cruce, `GOB.gobierno_digital.encig2025.edad_x_sexo` y
`GOB.gobierno_digital.encig2025.escolaridad_x_sexo`, vocabulario 0.6, `unidad_objetivo: evento`,
candidatos C2/C7/C-ENCOGIDA/C-ASTRA/C1, `veredicto`:
`CORROBORADA → SIN-CANDIDATO-SUPERIOR` · `FALSADOR-DEBIL → FALSADOR-DEBIL` (con el B-bis literal
anotado) · `LIMITA-C2*`/`FUERA-DE-SOPORTE-GLOBAL` → el literal.
`champion_actual`: **C2** si el piso no fue vencido, los controles del árbitro dieron
`REPRODUCE` y el IC de C2 existe en las ocho celdas del cruce (firma 17/sep; la adopción es la
que esa firma ya dice, este acto no decide otra); `NINGUNO` en cualquier otro caso. Si un
retador vence: `NINGUNO`, la celda queda marcada para decisión de mesa y se abre FP de adopción
con el nombre del retador. **Este acto nunca adopta un retador.**

### 4.3 · Cobertura y «punto dentro del IC de R» — secundarias, reportadas aparte

Cobertura = `R ∈ IC del candidato`, sólo para candidatos cuyo IC se selló antes de R (C1, C7,
C-ENCOGIDA, C-ASTRA), por cruce: `k` de `n` celdas `PUNTUADA` con intervalo de Wilson 95%; las
celdas de una ola comparten muestra y no son independientes (un conglomerado: ENCIG 2025). Aparte,
«punto del candidato dentro del IC de R» para los cinco. Ninguna frase de producto las colapsa.
Todas las emisiones comparadas son **PROSPECTIVA** (selladas antes de que exista R); el IC de C2
es `NACE-CON-R` y no entra.

## 5 · Cuerpo de medición — tres CALC, tres commits (E.6)

Un solo archivo de código, `tools/encig/duelo_2025/duelo.py`, depositado **byte a byte** como
`medidor.py` en cada CALC (el sello cubre el código que mide); `medir()` despacha por
`parametros.punto_de_entrada`.

| | `CALC-ENCIG-DUELO-2025-EDADXSEXO-EMISIONES-0001` · `…-ESCOLARIDADXSEXO-EMISIONES-0001` (COMMIT-2) | `CALC-ENCIG-DUELO-2025-ADJUDICACION-0001` (COMMIT-3) |
|---|---|---|
| lee | sólo `origen: repo`: C2 compuesto, históricos 2021/2023, C-ASTRA del cruce, firma congelada, medidor del piloto 4 | `encig25_base_datos_csv` + receta ENCIG + las dos emisiones y sus sellos + marginales 2025 sellados + árbitro del piloto 4 |
| ENCIG 2025 | **nada** (ni marginal ni cruce) | único código autorizado a cruzarla, y sólo por los dos pares declarados |
| emite | C2, C7, C-ENCOGIDA, C-ASTRA, C1 por celda; λ y sus piezas; soporte histórico; admisión de C-ASTRA | R, n, soporte, veredictos, ΔMAE con IC, B-bis por cruce y agregado, cobertura, IC de C2 |
| se niega si | firma §2 no FIRMADA en la copia congelada; cualquier input de manifiesto o con `encig25`/`encig_2025`/`encig2025_` en id o ruta; un id sellado ausente | la auditoría de su propio código falla; falta un sello de emisión o no coincide; se pide un par fuera de la lista |

**Guardia de agrupación (E.6, vive en el medidor porque ENCIG no tiene módulo guardián).** Toda
máscara del árbitro se construye por `_mascara(ejes)`, que admite 0 ejes (total), 1 eje, o
exactamente `EDAD×SEXO` / `ESCOLARIDAD×SEXO`; `EDAD×ESCOLARIDAD` (consumido) y cualquier otro par
levantan `ReservaRota`. La emisión no toca 2025 en absoluto, y lo prueba en cada corrida
alimentándose a sí misma un input prohibido (`G-GUARDIA-PROBADA`).

**Auditoría automática del código antes de abrir** (`auditoria(fuente)`, sobre los bytes del
propio `medidor.py`, en cada corrida; el árbitro PARA si no sale limpia): (1) desde `emisiones`
no se alcanza, en el grafo de llamadas del módulo, ninguna lectura de payload (`_load_wave`,
`_bootstrap`, `ZipFile`, `read_csv`, `_frame_2025`); (2) toda llamada a `_bootstrap` en el
árbitro recibe máscaras hechas por `_mascara`; (3) `PARES_AUTORIZADOS` es exactamente los dos
pares; (4) `_guardia_emisiones` y `_guardia_sellos` se llaman al entrar. **Prueba por mutación**
(§6 e): cinco mutantes del código (quitar cada guardia, añadir `EDAD×ESCOLARIDAD` a los pares,
leer 2025 desde `emisiones`) y la auditoría o el test los atrapan a todos.

**Secuencia.** COMMIT-1 (este): spec humana + `spec.yaml` de los tres CALC + código + test D-22.
COMMIT-2: `corrida0 run` de las dos emisiones, sello, asiento de replay. COMMIT-3a: el
`spec.yaml` del árbitro recibe los sha256 de las dos emisiones selladas (única edición admitida;
`preflight` del árbitro antes de esto: BLOQUEADO **exactamente** por
`input_repo_ausente`/`input_repo_no_commiteado` de esos cuatro inputs). COMMIT-3: `corrida0 run`
del árbitro, sello, celdas-D, asientos, dictamen.

## 6 · Validación de «congelado» — D-22 (`tests/test_encig_duelo_2025.py`)

- **(a) sintética, todas las ramas terminales**: emisiones y árbitro de punta a punta sobre
  fixtures ENCIG fabricados (`encig{ola}_04_sec_7.csv` + `…_02_residentes_sec_2.csv`), y
  `corrida0._valida_outputs` vacío contra el `resultados:` de cada `spec.yaml` en: todo con
  soporte · soporte parcial · fuera de soporte global · cero puntuadas · celda vaciada en una
  réplica · categoría con masa cero · delta histórico degenerado (λ con k < 2). Ningún `NaN` ni
  `inf` (None y NaN se enumeran los dos).
- **(b) oro**: con el corpus montado, las funciones del árbitro sobre ENCIG 2023
  (`encig23_base_datos_csv`) reproducen `CALC-ENCIG2023-CRUCES-HISTORICOS-0002` en P, N,
  P-IC-LO/HI, DELTA, DELTA-EE de las 16 celdas a `1e-10`, y los marginales de un eje reproducen
  `CALC-PISOS-ENCIG2023-EJES-0002` en `-P` a `1e-10`. En NUBE se omite y se dice.
- **(c) reserva**: ningún `resultados.json`/`ejecucion.json`/`sello*` en los tres CALC al congelar;
  la firma ausente o `ABIERTA` para; un input de manifiesto en la emisión para.
- **(d) λ**: re-implementación independiente del método de momentos sobre los mismos
  `DELTA`/`DELTA-EE` y coincidencia con la λ emitida a `1e-12`; y identidad con `_lambda_cruce` del
  piloto 4 leída de sus bytes.
- **(e) mutación**: los cinco mutantes de §5 son atrapados.
- **(f) identidad**: los tres `medidor.py` son byte a byte `tools/encig/duelo_2025/duelo.py`;
  los `resultados:` de los tres `spec.yaml` son exactamente `esquema_resultados(...)`;
  `_estado_gana` extraída coincide con la del módulo del piloto 4 en una rejilla.
- **`corrida0 preflight`**: VERDE para las dos emisiones; para el árbitro, BLOQUEADO sólo por los
  cuatro inputs de COMMIT-3a. Salida cruda en la nota.

## 7 · Ejecución diagnóstica

**Ninguna sobre 2025.** El oro sobre 2023 (§6 b) es control de maquinaria sobre una ola no
reservada, ya sellada por otros; no produce ningún número de este acto. El primer `run` del
árbitro es el resultado.

**Una, declarada aquí, sobre las emisiones.** Después de commitear este COMMIT-1 (código ya
congelado) y antes del COMMIT-2, `emisiones` se ejecuta una vez sobre sus insumos reales sólo
para probar el conducto sobre oro (D-22(2): `_valida_outputs` vacío con los bytes reales). Es
aritmética cerrada sobre bytes sellados, sin semilla y sin 2025: el `run` del COMMIT-2 tiene que
reproducirla **bit a bit** (se compara el JSON); si difiere en un solo valor, el acto PARA. Sus
números no se leen para nada más antes de sellar.

## 8 · Lo que esta spec NO autoriza

No adopta retadores (PARO c) · no reabre `edad × escolaridad` · no edita sellos ajenos (C2
compuesto, Astra, históricos, piloto 3, piloto 4) · no cambia umbral, regla, λ, lista de
candidatos ni B-bis después de este commit (PARO d) · no lee 2025 fuera del árbitro, ni tabulados
ni comunicados de 2025 (PARO a) · no toca ENCIG ≤ 2023 salvo el oro de §6 b · no diseña la familia
2027.

## 9 · Auditoría (afirma sobre México)

Una línea de contadores: este procedimiento, si corre, mueve tres corridas selladas y dos
`celdas_validadas`; no mueve adopciones de retadores. **Escala:** proporciones de **trámites** de
pago de luz, en pp; ninguna se promedia con cifras por persona ni con otros trámites. **Universo:**
ENCIG cubre ciudades de 100 mil habitantes o más: nada aquí habla de lo rural ni de localidades
chicas; «¿qué cambia con foco rural/popular?» — casi todo: pagar la luz en línea supone cuenta
bancaria o tarjeta, conectividad y un recibo a nombre propio, y la oferta de cajeros y kioscos
es urbana. Un gradiente por escolaridad o edad describe **acceso y oferta** (exclusión financiera,
conectividad, infraestructura de cobro) antes que preferencia o «cultura digital»; oferta antes
que preferencia (§3 de las instrucciones). Sexo no discriminó en el marginal (0.681 vs 0.665): si
un cruce con sexo muestra interacción, lo primero a descartar es composición (quién es titular
del contrato de luz en el hogar), no conducta. Peligroso leído simplista: «los viejos no usan lo
digital» — el denominador es quien pagó, no quien pudo pagar. Evidencia media: asociación
transversal, sin identificación. **PROSPECTIVA vs RETROSPECTIVA:** toda cifra de candidato es
PROSPECTIVA; el IC de C2 nace con R y se rotula aparte.

El primer resultado que produzca este procedimiento es el que se reporta.
