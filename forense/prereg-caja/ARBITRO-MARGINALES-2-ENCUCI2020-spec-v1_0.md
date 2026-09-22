# ARBITRO-MARGINALES-2 · ENCUCI2020 · spec v1.0

ACTO GEN2-ARBITRO-MARGINALES-2, P2 (pieza ENCUCI2020). Formaliza en GEN2, con
COMMIT-1 congelado por D-22, las dos reglas de `milpa/tramite-ola5-propuesta-v0.yaml`
que P1 clasificó `RE-MEDIDA (nueva)` para esta encuesta: no hay CALC GEN2 previo que
las cubra (verificado por búsqueda de valor y de variable en todo
`data/corrida0/*/{spec.yaml,resultados.json}`). El estimando, el universo, el
ponderador, el diseño y el método de IC **no se inventan aquí**: son los que el
propio GEN1 ya prerregistró y documentó línea por línea en el YAML (campos
`universo`, `diseno`, `ponderador`, `desenlaces`, `ic95`), producidos por
`ACTO MAESTRA35-L9/L11` (2/sep/2026). El oro de este COMMIT-1 es reproducir esos
números exactos desde el payload crudo.

## 0 · Premisas verificadas

- `[EJECUTADO]` payload `encuci2020_bd_dbf` COINCIDE en `data_raw`
  (`tests/manifiesto.py --verifica --id encuci2020_bd_dbf`, sha256 y tamaño
  6 913 684 bytes verificados contra `data/manifiesto.yaml`).
- `[EJECUTADO]` `ENCUCI_2020_SEC_6_7_8.dbf` dentro de `BD_ENCUCI2020_dbf.zip` trae
  `ID_PER`, `AP6_9`, `AP6_10`, `AP6_11`, `AP7_13`, `AP7_15`, `FAC_SEL`, `EST_DIS`,
  `UPM_DIS` — las 9 columnas que ambas reglas necesitan, en la MISMA tabla (no hace
  falta join con `ENCUCI_2020_SD.dbf`: sus columnas de diseño ya están en SEC_6_7_8).
  21 519 filas, `ID_PER` único.
- `[LEÍDO]` ninguna de las dos reglas tiene CALC GEN2 previo (P1, `ARBITRO-MARGINALES-2-clasificacion-v1_0.tsv`).

## 1 · Regla A — `civico.transferencia.entitlement_encuci2020`

**Universo**: personas con `AP6_9` en {1,2} (excluye 3=Ninguna, 9=NS/NR). n=20 868.
**Eje**: `AP6_10` (beneficiario de un programa social en los últimos 12 meses),
SI=1 / NO=2 (excluye 9=NS/NR).
**Desenlace principal**: `AP6_9 == 2` ("Los programas sociales son un derecho de
los ciudadanos", contra `AP6_9 == 1` "son una ayuda que da el gobierno").
**Eje anidado** (dentro de beneficiarios, `AP6_10==1`): `AP6_11` (le pidieron algo a
cambio), 1=Sí / 2=No (excluye 9, blanco=no aplica).
**Ponderador**: `FAC_SEL`. **Diseño**: `EST_DIS` × `UPM_DIS`, bootstrap de UPM con
reemplazo dentro de estrato, 10 000 réplicas, seed 42, percentiles 2.5/97.5.

Oro (GEN1, `civico.transferencia.entitlement_encuci2020`):
`p(AP6_9==2 | AP6_10==1)` = 0.540278 [0.523284, 0.557868] n=5 665;
`p(AP6_9==2 | AP6_10==2)` = 0.606014 [0.593683, 0.617803] n=15 186;
brecha = −6.5736 pp [−8.7157, −4.4277]; eje anidado `AP6_11==1` = 0.552875 n=294,
`AP6_11==2` = 0.540569 n=5 360.

## 2 · Regla B — `civico.voto.agencia_con_secreto_encuci2020`

**Universo restringido**: `AP6_10` en {1,2} × `AP7_15` en {1,2} × `AP7_13` con
código de 2 dígitos válido (no blanco, no '99'). n=15 083 de 21 519 = 70.09%.
**Rama**: `AP7_15==1` SECRETO / `AP7_15==2` OBSERVABLE.
**Eje**: `AP6_10` beneficiario SI=1/NO=2.
**Desenlace**: `AP7_13 == '07'` (simpatiza con MORENA).
Mismo ponderador/diseño que la regla A.

Oro (GEN1, `civico.voto.agencia_con_secreto_encuci2020`):
rama SECRETO: beneficiario_si 0.321633 [0.300274,0.342942] n=3 144; beneficiario_no
0.257825 [0.244352,0.271294] n=7 836; brecha +6.3809 pp [3.8238,8.8942].
rama OBSERVABLE: beneficiario_si 0.319745 [0.276605,0.362079] n=951; beneficiario_no
0.204092 [0.18712,0.221256] n=3 152; brecha +11.5652 pp [6.5748,16.5879].

## 3 · Tolerancia y veredicto de reproducción

`REPRODUCE` si cada punto cae dentro de 1e-3 absoluto del oro (redondeo del YAML a
6 decimales más margen de reconstrucción del bootstrap con semilla distinta pero
mismo método); si no, `NO-REPRODUCE` con el delta declarado — un `NO-REPRODUCE` no
es un fallo del COMMIT-1, es el hallazgo de P3 (ver nota de cierre), exactamente
como ya ocurrió con `tramite.mordida.discrecional` en `CALC-ENCUCI-0001`
(0.018 pp de delta, `NO-ADOPTABLE-POR-DISCREPANCIA`, denominador recortado).

## 4 · No hace

No re-mide `tramite.mordida.discrecional` ni `civico.protesta.agravio_urbano_encuci2020`
(ya GEN2, `CALC-ENCUCI-0001`, ver P1). No toca `milpa/`. No adopta.
