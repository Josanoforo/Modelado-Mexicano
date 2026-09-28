# M23 · ENSAFI 2023 · ahorro solo informal (contraste de definición frente a ENIF 2024)

El primer resultado que produzca este procedimiento es el que se reporta.

Acto `GEN2-CALC-ALTERNOS-LOTE-1` (0-bis `795b1053`), fila 65 de
`canon/mapa-instrumentos-alternos-v1_0.tsv` («contraste de definición frente
a ENIF 2024, RETROSPECTIVA»). Firma R07 A1 (b): «M23 recibe relevo
descriptivo con el RESULT sellado de ENIF 2024, rotulado RETROSPECTIVA, y
ENSAFI 2023 como contraste. Ambas specs declaran que consumen HOLDOUT». Un
CALC: `CALC-ALT-M23-ENSAFI2023-0001`. El relevo con ENIF 2024 es el RESULT
ya sellado (se cita, no se recalcula); este CALC es sólo el contraste.

## Qué ya está medido (E.5)

`ya_medido.py dinero.ahorro.via_informal` → `CALC-ENIF-0001`,
`CALC-HORIZONTE-VIA-DERIVADOS-0001-v1_1`, … (ENIF). Los CALC ENSAFI
sellados (`CALC-ENSAFI-DISENO-0001`, `CALC-ENSAFI2023-ESTRATEGIAS-CONJUNTAS-*`)
miden atraso y estrategias (`P4_7`, `P4_8`, `P6_9`, `P6_10`); ninguno la
sección 6.1–6.3.

## Estimando, unidad, escala, universo

- **Unidad:** persona elegida 18+ (`TMODULO`), `FAC_ELE`.
- **Reactivos (A.15, cuestionario ENSAFI 2023 p. 15):**
  - «6.1 Actualmente, ¿usted… 1. ahorra prestando dinero? 3. tiene dinero
    guardado en una caja de ahorro del trabajo o de personas conocidas?
    4. tiene dinero guardado con familiares o personas conocidas?
    5. participa en una tanda? 6. ahorra dinero en su casa?» (`Sí 1, No 2`).
    El inciso 2 («comprando propiedades, animales u otros bienes») queda
    fuera: es activo, no ahorro en dinero (misma selección que la fila 65
    del mapa).
  - «6.2 ¿Usted tiene… 01–10» (cuentas y productos formales, `Sí 1, No 2`).
  - «6.3 Actualmente, ¿usted tiene ahorros en alguna de esas cuentas que
    mencionó?» (`Sí 1, No 2`; pase: sólo si algún 6.2 = 1).
- **Construcción (derivadas, en este orden):**
  - `INFORMAL` = 1 si algún `P6_1_{1,3,4,5,6}` = 1; 2 si los cinco = 2;
    vacío si no.
  - `TIENE_CUENTA` = 1 si algún `P6_2_01..10` = 1; 2 si los diez = 2.
  - `FORMAL` = 1 si `TIENE_CUENTA` = 1 y `P6_3` = 1; 2 si `TIENE_CUENTA` = 2
    o `P6_3` = 2 (el pase estructural es «no ahorra formal», no un perdido).
  - `SOLO_INFORMAL` = 1 si `INFORMAL` = 1 y `FORMAL` = 2; 2 si `INFORMAL` = 2
    o `FORMAL` = 1.
- **Estimandos:** `p(SOLO_INFORMAL)`, `p(INFORMAL)`, `p(FORMAL)`; nacional y
  por tamaño de localidad `TLOC` (FD: `1` 100 000+, `2` 15 000–99 999,
  `3` 2 500–14 999, `4` < 2 500); contraste `p(SOLO_INFORMAL | TLOC 4) −
  p(SOLO_INFORMAL | TLOC 1)`. n mínimo 30.

## Oferta antes que preferencia (encargo §1)

ENSAFI 2023 no pregunta, en 6.1–6.3, por qué no se ahorra formalmente: no hay
reactivo de oferta (acceso, sucursal, requisitos) para separarla de la
preferencia. Se declara: este CALC **no** distingue oferta de preferencia; la
lectura por oferta vive en `CALC-DIN-OFERTA-EXCLUSION-ENIF2024-0001` (ENIF
2024, sellado) y se cita.

## Ponderador y diseño

`FAC_ELE`, `EST_DIS`, `UPM_DIS` (FD `TMODULO`). IC95 bootstrap UPM en
estrato, 2 000 réplicas, semilla PCG64 `20260928`.

## Agregador (E.1)

Razón de sumas ponderadas por celda.

## Qué pasa si el falsador no refuta

Contraste de **definición**, no prueba: la diferencia con el RESULT ENIF
2024 se lee como sensibilidad de la cifra a encuesta y redacción (otra ola,
otro cuestionario). No se promedian las dos cifras, no se elige una
(A-bis 2). Si difieren, se reporta; ninguna corrige a la otra.

## Auditoría v2.16

- **Unidad:** persona 18+. **Escala:** proporción.
- **RETROSPECTIVA:** ENSAFI 2023 (ola vista, EXPUESTA por F5 E05).
- **¿Incentivo o psicología?** Conducta declarada de ahorro; el canal
  informal puede ser costo/acceso (incentivo) o confianza (psicología); no
  se separan aquí.
- **¿Clase media urbana?** Se reporta por `TLOC`, rural incluido.
- **HOLDOUT gastado: `M23`** (ya consumido según R07 (b): «consume HOLDOUT
  de M23 (ya consumido)»; censo C2: 0 menciones en 140 archivos).
  `holdout_gastado = M23`.
