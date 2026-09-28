# Propuesta de re-especificación de R03 · GEN2-MAPA-INSTRUMENTOS-ALTERNOS-1 (P2)

**Es una propuesta, no un CALC.** No mide ni abre bases; la firma es de mesa. Contadores movidos: cero.

## 1 · Qué pedía R03 y por qué no se ejecutó

- [LEÍDO] `forense/prereg-duelo-v2/F5-panel-candidatos-v1_3.tsv`, línea 4. Familia `R03-TRA-ENAPROCE-TRAMITES`, unidad «empresa micro/pequeña/mediana», pregunta «Carga regulatoria y pago informal en trámites de la MIPYME», regla `tramite.mordida.discrecional`. Faltaba el microdato real y «la misma firma de unidad de R02».
- [LEÍDO] OBTENCION-PREVIA-1 P4: ENAPROCE no tiene ningún reactivo de solicitud o pago informal, así que la parte «mordida» no se puede medir con ENAPROCE por ninguna vía.
- [LEÍDO] **La «firma de unidad de R02» ya existe y dice que no.** Es la firma F-19 de mesa (15/sep/2026; ADR-529; `forense/notas/2026-09-15-GEN2-F6-PANEL-CAJA-1-cierre.md` §P4): «el crosswalk persona→establecimiento **NO** es admisible para F6». A raíz de ella, R02 (WBES) y R08 (ENCRIGE) quedaron como `UNIDAD-DISTINTA-NO-TRANSFERENCIA`, es decir, familias descriptivas del dominio TRA para el informe y no celdas.

Consecuencia: re-especificar R03 como celda de transferencia sobre cualquier encuesta de empresas chocaría con F-19. Lo que sí se puede es darle a R03 un instrumento que **mida la mordida en la empresa**, como familia descriptiva junto a R02 y R08.

## 2 · Qué hay en el corpus que responde la pregunta de R03 (verificado por texto de pregunta)

| ítem de R03 | ENCRIGE 2020 (empresa) | ENVE 2024 (establecimiento) | WBES México 2023 (establecimiento) |
|---|---|---|---|
| (i) corrupción al hacer trámites, pagos, solicitudes o inspecciones | `P9_3_1..3` (2020), `P9_4/P9_5` por trámite | `P6_1..P6_4` (2023), `P6_5..P6_7` | `c5, c14, g4, j5, j12, j15`, `j7a` |
| (ii) otra empresa le refirió actos de corrupción (cota superior) | `P9_2` («¿Recuerda si alguna otra empresa…?») | NO-ENCONTRADO (solo `P3_4`, corrupción de autoridades) | NO-ENCONTRADO en etiquetas del DDI |
| (iii) carga regulatoria | `P8_714_H` (horas por trámite), `P5_5` (personal dedicado), `P5_7/P5_8` (gasto) | solo ranking `P2_1` | `j2` (% del tiempo gerencial) |
| (iv) tamaño y sector | `P1_4CAL`, `GRAN_SECTOR` | `ESTRATO`, `GRAN_SECT` | `a6a`, sector |
| (v) expansión y diseño | `FAC_EXP` (estrato y UPM no son variables en el DDI) | `FAC_EXPA` | `wstrict/wmedian`, `strata` |
| acceso al microdato | no se distribuye (RNM 691, «Data Access Not Available»); tabulados en el corpus | RNM 1058 con plantilla abierta, SIN-FETCH | en el corpus (.dta) |

Fuentes: `inegi_rnm_ddi/encrige2020_rnm691_ddi.xml`, `inegi_rnm_ddi/enve2024_rnm1058_ddi.xml` (registrados en el manifiesto por este acto), `MEX_2023_WBES_v01_M.xml`, cuestionarios del corpus; acceso: `acceso-rnm.tsv`.

## 3 · Re-especificación propuesta

- **Nombre:** R03 deja de ser una familia de ENAPROCE y se **funde con R08** (ENCRIGE) como familia descriptiva `UNIDAD-DISTINTA-NO-TRANSFERENCIA`. WBES (R02) y ENVE 2024 sirven de segundo y tercer instrumento. La parte de carga regulatoria de ENAPROCE sigue sin vía (I1).
- **Unidad:** empresa (ENCRIGE); establecimiento (ENVE, WBES). No se promedian entre sí (A-bis 4).
- **Universo:** empresas micro, pequeñas y medianas (`P1_4CAL` sin «grande») de industria, comercio y servicios que en 2020 hicieron al menos un trámite, pago o solicitud o recibieron una inspección. Es el denominador de los tabulados `t6_33/t6_36`.
- **Estimandos:**
  - (est. 1) proporción ponderada de empresas con al menos una experiencia de corrupción (`P9_3_*`), por tamaño;
  - (est. 2) cota superior «conocimiento y/o participación» (`P9_2` ∪ `P9_3_*`);
  - (est. 3) horas por trámite y gasto de cumplimiento, por tamaño y por experiencia de corrupción. Esta es la única pieza que exige microdato.
- **Ola:** 2020, con periodo de referencia 2020. ENVE 2024 refiere a 2023; WBES 2023 a su año fiscal.
- **Qué ya está hecho y se cita, no se re-mide (E.5):** est. 1 y est. 2 por tamaño en los tabulados, extraídos y sellados por #826 (`CALC-ENCRIGE-CORRUPCION-DESCRIPTIVA-0001`).
- **Qué falta:** est. 3 y cualquier cruce requieren el microdato ENCRIGE 2020, que implica SOLICITUD a INEGI. El segundo instrumento, ENVE 2024, requiere antes el dictamen de reserva de la ola y luego OBTENER vía RNM 1058.

## 4 · Qué no decide esta propuesta

No decide adopción, levantar reservas ni que R03 vuelva a ser celda. Tampoco fija umbral ni congela spec: cada CALC sucesor lleva su COMMIT-1.
