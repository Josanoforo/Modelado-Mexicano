# Serie ENCIG 2015–2023 · pago ordinario de luz por canal digital útil · spec v1.0

ACTO GEN2-ENCIG-SERIE-Y-TENDENCIA-1 (21/sep/2026), pieza P2. Prerregistro
escrito antes de abrir ENCIG 2015, 2017, 2019 y 2021; ENCIG 2023 ya está
abierta por el piso adjudicado y aquí sirve de oro.

El primer resultado que produzca este procedimiento es el que se reporta.

## 1 · Qué se mide

Por ola (2015, 2017, 2019, 2021, 2023), un CALC `CALC-ENCIG-SERIE-CANAL-<ola>`
con el mismo medidor `tools/encig_serie_canal.py`:

- **Unidad:** trámite (una fila de `sec_7` por persona elegida × tipo de
  trámite; quien pagó doce veces contribuye doce veces).
- **Universo:** `N_TRA` normalizado == 1 (pago ordinario del servicio de luz)
  con `P7_3` ∈ {1, 2, 4, 5, 6}. Los códigos 3, 7, 8, 9 y blanco quedan fuera
  y se cuentan (`P7-3-EXCLUIDAS`); nunca se convierten en no adopción.
- **Desenlace:** digital útil = `P7_3` ∈ {4, 5} (Internet/app; cajero o
  kiosco inteligente).
- **Ponderador:** `FAC_TRA`. **Diseño:** `EST_DIS` × `UPM_DIS` de `sec_7`.
- **Celdas:** nacional `ALL-ALL` + sexo (1, 2) + edad (18–29, 30–44, 45–59,
  60–96) + escolaridad homologada de `NIV` ({0,1,2} hasta primaria · {3}
  secundaria · {4,5,6,7} media superior · {8,9} superior). Once celdas.
  Valores inválidos de un eje se excluyen solo de ese eje (la celda nacional
  no exige demografía válida).
- **Ejes** desde la tabla de residentes: `SEXO`, `EDAD`, `NIV`. Join m:1
  por `ID_PER` en 2017–2023; en 2015 (sin `ID_PER`) por
  `ENT+UPM+V_SEL+N_HOG+R_ELE` (sec_7) = `ENT+UPM+V_SEL+N_HOG+N_REN`
  (residentes). Si la llave de residentes no es única, el medidor PARA
  (RuntimeError): no se deduplica ni se elige.
- **IC95:** 10 000 remuestras de UPM dentro de estrato, `PCG64(42)`, un plan
  compartido por las once celdas — `_estimate` verbatim del piso
  `CALC-PISOS-ENCIG2023-EJES-0002/medidor.py`. Soporte vacío produce
  P/IC nulos (`permite_no_estimable`) con N=0 y B-VALIDAS=0.

## 2 · Oro

Sobre `encig23_base_datos_csv`, las diez celdas marginales de
`CALC-ENCIG-SERIE-CANAL-2023` deben coincidir a 1e-10 con las de
`CALC-PISOS-ENCIG2023-EJES-0002/resultados.json` (P, IC-LO, IC-HI, N,
DEN-W, B-VALIDAS), id por id según el mapa `SEXO-1 ↔ DIGITAL-SEXO-1`, etc.
Lo verifica `tests/test_encig_serie_canal.py::test_oro_2023` cuando el CALC
2023 está sellado; hasta entonces el test se salta y lo dice.

## 3 · Lo que este acto no hace aquí

No abre ENCIG 2025 (PARO a): el punto 2025 entra a P3 desde valores ya
sellados. No agrupa nada por dos variables. No cambia el piso adjudicado.

## 4 · Comparabilidad (P1)

`data/encig-canal-comparabilidad-texto-v1_0.tsv`: 2017, 2019 = MISMO-INSTRUMENTO
contra 2021 (ancla); 2015, 2023, 2025 = CAMBIO-MENOR sin efecto sobre el
estimando. Seis olas comparables; la serie empieza en 2015.
