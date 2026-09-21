# Núcleo común de cuidado en ENUT · pisos 2019 por eje, R 2024 por eje, serie 2009-2024 y persistencia · spec v1.0

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-ENUT-PISOS-Y-SERIE-1` (21/sep/2026, CAJA), encargo archivado en
`forense/encargos/2026-09-21-GEN2-ENUT-PISOS-Y-SERIE-1.md`. Esta spec humana
gobierna tres `spec.yaml` (D-15): `CALC-ENUT2024-NUCLEO-EJES-0001` (P3),
`CALC-ENUT2019-NUCLEO-EJES-0001` (P2) y `CALC-ENUT-SERIE-2009-2014-NUCLEO-0001`
(P4, serie), y la derivación de P4 (`tools/enut_persistencia_serie.py`). El
código que mide es uno, `tools/enut_nucleo.py`, congelado con este texto.
Ningún registro de microdato de ENUT se abrió antes de sellar esto.

## 0 · Por qué este estimando y no el sellado

`ADR-557` (PR #908) dictaminó por texto que el `horas_cuidado` sellado de
ENUT 2024 (`*_CON_CP`) no es construible en 2019. P1 de este acto
(`data/enut-comparabilidad-texto-v1_0.tsv`) lo confirma y lo extiende: 2014 ≡
2019 ítem por ítem; 2009 es otra batería. Mesa (21/sep/2026) eligió la opción
A: «Núcleo común + CON_CP 2024 como secundario». Consecuencia: los pisos y la
persistencia se miden sobre un estimando NUEVO, `horas_cuidado_nucleo`; las
21 celdas del marcador (C1) siguen `NO-CONSTRUIBLE` y este acto no las toca.

## 1 · Estimandos

- **C2 · NUCLEO** (2014, 2019, 2024): suma de horas de los ítems `=`/`≈`
  de los bloques *cuidados especiales* (6.11), *0-14* (6.12 ∪ 6.13) y *60+*
  (6.15); sin los emocionales ni las esperas «sin hacer otra actividad» de
  2024; cuidado pasivo tal cual lo pregunta cada ola (2024 exige presencia;
  2014/2019 no — diferencia declarada, no corregida). 15-59 fuera, como en C1.
- **C3 · MIN** (2009, 2014, 2019, 2024): subconjunto de C2 presente en las
  cuatro olas (P1, filas C3).
- **C1 · CONCP** (sólo 2024, secundario): Σ de las cuatro columnas
  `*_CON_CP` de `tvar_crea`, la definición de `CALC-ENUT-0001`.
- **C4 · razón** por variante: Σ_h w_h·(horas de mujeres 40+ del hogar) /
  Σ_h w_h·(horas del hogar), todos los hogares con ponderador (0/0 dentro),
  emitida sólo nacional. Escala [0,1]; nunca se compara con horas (PARO b).

Los ítems exactos por ola y variante están en `tools/enut_nucleo.py::ITEMS`,
transcripción de P1 que el test coteja.

## 2 · Universo, horas, ejes, diseño

- Universo: personas de 12+ con registro en la tabla del módulo de la base
  nacional (las tablas `_indígena`/`_PI` son extracciones, P1). Quien no
  declara ninguna hora aporta 0. Hogares: los que tienen al menos una persona
  en el universo.
- Horas por ítem: `h_LV + min_LV/60 + h_SD + min_SD/60`, sin tope; blanco o
  no numérico = 0; los ítems «Sí» sin ningún tiempo se cuentan
  (`*-SI-SIN-TIEMPO`) y se declaran.
- Ejes de la casa, **una variable por celda**: nacional · sexo (1/2) · edad
  (12-17, 18-29, 30-39, 40-59, 60+; `EDAD_V` en 2019/2024, `EDAD` de TSDem
  en 2009/2014) · escolaridad homologada (NIV → hasta_primaria {0,1,2} ·
  secundaria {3} · media_superior {4-7; 2009: 4,5,6} · superior {8+; 2009:
  7,8,9}; misma regla que `PISOS-REJILLA-escolaridad-catalogos-v1_0.tsv`) ·
  localidad (rural = TLOC 4 / LOC 2; urbano el resto). Código inválido sale
  sólo de su eje.
- Ponderador: `FAC_PER` (medias); hogar: `FAC_HOG` (2019 THOGAR, 2024 tsdem)
  o `FAC_VIV` (2009, 2014; no existe FAC_HOG). Diseño `EST_DIS` (`EDIS` en
  2014) × `UPM_DIS`, llaves opacas como texto.
- IC95: bootstrap de UPM dentro de estrato, 10 000 réplicas, `PCG64(42)`,
  un plan de réplicas compartido por todas las celdas de la ola (molde
  `CALC-PISOS-ENVIPE2024-EJES-0002`); estrato con UPM única se re-muestrea a
  sí mismo. Celda sin soporte → punto/IC nulos (`permite_no_estimable`),
  N/DEN-W/B-VALIDAS se conservan.

## 3 · Guardia de una sola variable (3D) y auditoría

`celdas_de_eje(frame, eje)` admite un solo `str` de `EJES`; no existe
`cruce()`. `auditoria_ast()` recorre el módulo antes de abrir el zip: R1
imports en lista blanca · R2 `crosstab/pivot/MultiIndex/eval/…` prohibidos ·
R3 `groupby` sólo en `_por_llave` y con la única llave literal `_llave`
(hogar o persona, nunca un eje) · R4 ningún nodo combina dos comparaciones
(`&`, `*`, `and`, `.mul`) · R5 lecturas sólo en `_lee_*` · R6 ningún token de
otro instrumento. El numerador «mujer 40+» de C4 vive en `_mujer40`, es una
subpoblación del hogar y no produce celda: la razón sale sólo nacional. El
cruce reservado `reparto_hogar × sexo_edad` no se ve ni se deriva.
`tests/test_enut_nucleo_conducto.py` prueba la guardia por mutación (11
controles positivos) y el conducto completo sobre sintético (D-22).

## 4 · Oro (D-22 ampliada) y compuerta

En 2024 el mismo módulo (a) recalcula la razón CONCP exactamente como
`CALC-ENUT-0001` (SEXO/EDAD de tvar_crea, FAC_HOG de tsdem) y reporta
`ORO-A-R-DELTA` contra `RESULT-ENUT-A-R` sellado (input con sha256), y (b)
compara persona por persona la suma de TODOS los ítems crudos de cada bloque
con la columna `*_CON_CP` (`VALIDACION-CONCP-*`). Son RESULT: si no dan ~0,
el CALC sella igual y el hallazgo se reporta; no se parcha (PARO e). Orden:
COMMIT-1 (esta spec + módulo + tres spec.yaml + test sintético) en origin →
`run` 2024 → verificar oro → `run` 2019 → `run` serie. `CALC-ENUT2024-
DISTRIBUCION-HORAS-0002` (FP-409) no se usa como oro.

## 5 · P4 · Calificación y serie — reglas fijadas antes de ver dato

Deriva `tools/enut_persistencia_serie.py` desde los `resultados.json`
sellados (nunca los edita) a `data/corrida0/enut-persistencia-serie-v1_0.tsv`.

**5.1 Persistencia 2019→2024**, para cada variante V ∈ {NUCLEO, MIN} y
escala (media por celda de eje; razón nacional): `error = R_2024 − piso_2019`
en la escala de la conducta; `cobertura = 1[R_2024 ∈ IC95(piso_2019)]`;
sobre las celdas con piso e R definidos, `k/n` con IC exacto de
Clopper-Pearson 95 %; MAE en la escala.

**5.2 Origen móvil — RETROSPECTIVA-MECÁNICA**, por celda, todas las
variantes entran o ninguna (§2 del encargo):
- V1 persistencia: `ŷ_t = y_{t−1}`;
- V2 tendencia 2 olas: `ŷ_t = y_{t−1} + (y_{t−1} − y_{t−2})·(t − t_{−1})/(t_{−1} − t_{−2})`;
- V3 tendencia serie: OLS de `y` sobre el año con TODAS las olas previas
  (≥ 3 puntos; si hay menos, `NO-APLICA`).
Objetivos: 2024 desde {2014, 2019} (NUCLEO: V1, V2; MIN: V1, V2, V3 con 2009)
y 2019 desde {2009, 2014} (MIN: V1, V2; NUCLEO: V1 desde 2014). Por variante y
objetivo: MAE y `cobertura_proxy = 1[|error| ≤ semi-anchura del IC95 del R
objetivo]` (mismo criterio para todas las V); para V1 además la cobertura
del IC del piso (5.1).

**5.3 Dictamen por conducta, una palabra**, léxico cerrado:
- `CAMBIO-DE-INSTRUMENTO`: C1 (las 21 celdas del marcador) por texto
  (ADR-557 + P1); también cualquier par de olas que P1 marque así.
- Media (NUCLEO y MIN, 14 celdas): con n < 4 celdas definidas →
  `NO-DECIDIBLE`. Si el límite inferior CP95 de la cobertura V1 ≥ 0.5 →
  `PERSISTE`, salvo que `MAE_V2 ≤ 0.5·MAE_V1` y `cobertura_proxy_V2 >
  cobertura_proxy_V1` → `TENDENCIA`. Si el límite inferior < 0.5: `MAE_V2 ≤
  0.5·MAE_V1` → `TENDENCIA`; si no → `NO-DECIDIBLE`.
- Razón (1 celda): `PERSISTE` si `R_2024 ∈ IC95(piso_2019)` y `piso_2019 ∈
  IC95(R_2024)`; `TENDENCIA` si los cambios 2014→2019 y 2019→2024 tienen el
  mismo signo y cada |Δ| excede la semi-anchura del IC95 de su ola destino;
  si no, `NO-DECIDIBLE`.
La distancia CONCP − NUCLEO por eje en 2024 se reporta como tamaño del cambio
de instrumento; no entra en ningún dictamen.

## 6 · Lo que no hace

No abre el cruce reservado · no dictamina FP-409 · no adopta · no edita el
marcador (las filas `SIN-PISO` se reportan antes y después por comando) · no
compara horas con razones ni núcleo con CON_CP sin enlace.
