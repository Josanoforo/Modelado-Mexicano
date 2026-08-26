# Enlace SpecCelda -> (regla, conducta) -- v1.0

ACTO MAESTRA30-E8, 26/ago/2026. Sella el enlace que el docstring de
`construir_crosswalk` (`milpa/src/emisor.py`) exige antes de que un
`CANDIDATO-EMITE` de la pasada 1 se convierta en un punto M real:
`SpecCelda -> (regla, conducta)`, el par que `emisor.emitir_binaria(regla,
conducta)` toma como argumento. Pasada declarada sobre las **60 filas**
del marco congelado (`forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv`),
no solo las 15 sorteadas -- A-bis 3.

## Método

Para cada fila del marco:

1. Si el crosswalk v1_1 (`forense/crosswalk-pregunta-regla-v1_1.tsv`,
   emparejamiento corregido -- ver ADR-208) la marca `NO-EMITE` en pasada
   1 (ni variable+encuesta coinciden en `procedencia.yaml`/`tramite.yaml`),
   la fila es `NO-EMITE` aquí también -- no hay nada que enlazar.
2. Si es `CANDIDATO-EMITE`, se busca una cita real de `(regla, conducta)`
   -- el `regla_id` debe existir en `milpa.src.emisor.cargar_reglas()`
   (las 5 reglas de `milpa/tramite.yaml`, el único motor de decisión que
   `emitir_binaria` consulta) y `procedencia.yaml` debe declarar la fila
   como desenlace medido (no ASIGNADO, no transporte fuera de dominio) de
   esa regla. Si no hay tal cita -- CIV-06, CIV-07, CIV-12 son ejemplos --
   la fila queda `NO-EMITE`: **no se inventa el enlace donde el motor no
   tiene regla** (prohibido explícito del encargo).

Escala/universo declarados por fila emitible (A-bis 3): ver columna
`escala/universo` de la única fila `EMITE`.

## Resultado

Sobre las 60 filas: **1 EMITE** (`CIV-01`), **59 NO-EMITE**.
Sobre las 15 sorteadas del duelo (`ADV1-M2`): **0 EMITE** -- ninguna de
las tres filas `CANDIDATO-EMITE` de la pasada 1 (ninguna, tras la
corrección: ver `forense/crosswalk-pregunta-regla-v1_1.tsv`) cae en la
muestra de 15, y de las 15 mismas ninguna tiene ya `CANDIDATO-EMITE` que
resista pasada 1. **Este es el resultado honesto, no forzado**: si tras
la pasada M sigue en 0 emitibles sobre las 15, ese es el dato que
alimenta el marcador v1.1 (E9), no un enlace fabricado para evitar el
cero.

| candidata_id | encuesta | variable | enlace | evidencia |
|---|---|---|---|---|
| CIV-01 | ENCIG | P8_3_1 | **EMITE** | `(regla=tramite.mordida.discrecional, conducta=paga_mordida)` — procedencia.yaml:937 (join ENCIG 2023 P8_3_1/2/3 x P11_1_23, ID_PER, 38966 filas, cero pérdida) sella P8_3_1 como desenlace dicotomizado de `tramite.mordida.discrecional`, regla real de `milpa/tramite.yaml` (`cargar_reglas()`); escala binaria [0,1], universo ENCIG 2023 población 18+ con trámite, n=38966 |
| CIV-02 | ENCIG | P11_1_02 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-03 | ENCIG | P9_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-04 | ENCIG | P5_10A | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-05 | ENCUCI | AP5_4_2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-06 | ENCUCI | AP5_3_8 | NO-EMITE | CANDIDATO-EMITE en pasada-1 (`milpa/procedencia.yaml:254`) pero sin `(regla,conducta)` real citada en canon/modelo-decision-v4_0.md ni procedencia.yaml para esta fila -- no se inventa el enlace |
| CIV-07 | ENVIPE | BP1_20 | NO-EMITE | CANDIDATO-EMITE en pasada-1 (`milpa/procedencia.yaml:395;milpa/procedencia.yaml:997`) pero sin `(regla,conducta)` real citada en canon/modelo-decision-v4_0.md ni procedencia.yaml para esta fila -- no se inventa el enlace |
| CIV-08 (15-sorteada) | ENVIPE | AP4_4_03 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-09 | ENVIPE | AP5_6_02 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-10 | ENVIPE | AP5_6_04 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-11 | ENVIPE | AP4_4_01 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| CIV-12 | ENPOL | P3_21_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-01 | ENIF | P5_4 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-02 | ENIF | P6_4 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-03 (15-sorteada) | ENIF | P7_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-04 | ENIF | P4_4_6 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-05 (15-sorteada) | ENFIH | P8_1_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-06 | ENFIH | P8_8_2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-07 (15-sorteada) | Encuesta de Competencias Financieras (Banxico/CNBV) | SF2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-08 | Encuesta de Competencias Financieras (Banxico/CNBV) | SF7 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-09 | Encuesta de Competencias Financieras (Banxico/CNBV) | SF5 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-10 | Encuesta de Competencias Financieras (Banxico/CNBV) | SF13 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-11 (15-sorteada) | ENIF | P5_3 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DIN-12 | Encuesta de Competencias Financieras (Banxico/CNBV) | SF10e | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-01 | ENASIC | P4_13 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-02 | ENASIC | P4_12 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-03 | ENASIC | P7_12_2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-04 (15-sorteada) | ENASEM | H16D_18 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-05 | ENASEM | H14_21 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-06 (15-sorteada) | ENASEM | F55_24 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-07 | ENUT | P6_10_7 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-08 | ENUT | TRAB_NO_REM_CUID_HOG | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-09 | ENADID | P8_10 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-10 | ENDIREH | P14_3_11 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-11 | ENBIARE | PA3_02 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| SFT-12 | ENBIARE | PC1_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-01 (15-sorteada) | ENOE | p3i | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-02 | ENOE | p3j | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-03 | ENOE | p2d6 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-04 | ENOEN | p3d | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-05 | ENTI | P1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-06 (15-sorteada) | ENTI | P2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-07 | ENDUTIH | P7_1 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-08 (15-sorteada) | ENDUTIH | P7_15 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-09 | ENDUTIH | P7_10_2 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-10 | MOCIBA | P4_01 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-11 | MOCIBA | P3 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| TIC-12 (15-sorteada) | ENOE | p3n | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-01 | ENAFIN (Encuesta Nacional de Financiamiento de las Empresas) | FAC_EXPA aplicado al indicador Empresas que tuvieron algun credito o financiamiento, dominio Micro | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-02 (15-sorteada) | ENAFIN (Encuesta Nacional de Financiamiento de las Empresas) | razon derivada de Creditos que fueron rechazados a las empresas sobre Total de creditos que solicitaron las empresas, por tamano de empresa | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-03 | ENAFIN (Encuesta Nacional de Financiamiento de las Empresas) | razon derivada de Total de empresas que tuvieron algun credito sobre Total de empresas, contrastando Micro contra Grande | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-04 (15-sorteada) | ENAFIN (Encuesta Nacional de Financiamiento de las Empresas) | razon derivada de Creditos que fueron aprobados sobre Total de creditos que solicitaron, contrastando localidades de 500 mil o mas habitantes contra 50 mil a 499 999 | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-05 (15-sorteada) | CPV Censo de Poblacion y Vivienda -- Cuestionario Ampliado | SITUA_CONYUGAL | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| EMP-06 | CPV Censo de Poblacion y Vivienda -- Cuestionario Ampliado | SITTRA | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-01 | CNBV Portafolio de Informacion / HR Ratings (desenlace documentado no-encuesta) | IMOR ajustado = (cartera vencida + castigos 12m) / (cartera total + castigos 12m) | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-02 | CNBV / HR Ratings (desenlace documentado no-encuesta) | IMOR ajustado y su trayectoria IMOR simple 8.4% (3T24) a 5.5% (3T25) | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-03 | CNBV (desenlace documentado no-encuesta) -- razon derivada, NO enunciada en ninguna fuente | razon IMOR_ajustado(Azteca) / IMOR_ajustado(tarjeta banca multiple) | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-04 | SEC EDGAR 10-K FirstCash Holdings (desenlace documentado no-encuesta) | proporcion de inventario con antiguedad mayor a un ano | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-05 | BMV / CNBV, reportes trimestrales de Gentera (desenlace documentado no-encuesta) -- fraccion NO enunciada | castigos del ejercicio como fraccion de la cartera total promedio del ejercicio | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |
| DOC-06 (15-sorteada) | BMV / HR Ratings, Financiera Independencia (desenlace documentado no-encuesta) -- OLA RETENIDA | IMOR ajustado de la cartera total | NO-EMITE | sin hit pasada-1 en crosswalk v1_1 (variable+encuesta no coinciden en procedencia.yaml/tramite.yaml) |

## Nota sobre B (RANURA FP-166)

Las 9 celdas arbitrables tienen `publicada=NO` por diseño del sorteo
(columna `publicada` del marco) y el bibliotecario FP-93 ya cerró
`NO-ENCONTRADO` sobre ellas. Por la firma de la RANURA, B queda
**opcional** en el contrato re-sellado de scoring (enmienda F1); las
casillas que dependan de skill se reportan `no evaluable` cuando B no
exista -- no se corre B en este acto (prohibido, es E9).
