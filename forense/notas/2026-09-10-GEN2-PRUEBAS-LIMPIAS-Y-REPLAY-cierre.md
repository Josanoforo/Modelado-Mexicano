# ACTO GEN2-PRUEBAS-REPLAY · cierre

Fecha: 10 de septiembre de 2026. Base de ejecución: `origin/main = 44134745ce7f19af18a87b153a99de3d506063b0`. Rama: `acto/gen2-pruebas-replay`.

## Resultado

- La prueba de demanda escribe de verdad, pero sólo bajo `TemporaryDirectory`; los dos TSV reales conservaron sus bytes antes/después. `tests/test_corrida0.py`: 84/84.
- T15 reutiliza `inspeccion_gobernanza`/`L0_ADR_RE` de `tools/cierre_acto.py` y exige una sola ancla L0. El fixture cubre una, duplicada, ausente y cita histórica literal. `tests/test_cierre_acto.py`: 8/8.
- `fuente_replay` ya se deriva con correspondencia por corrida/resultado/uso y distingue `VERIFY-ESTRUCTURADO`, `HEREDADO-DEL-REGISTRO-PUBLICADO`, `SIN-FUENTE` y `NO-CORRIDA`. Los fixtures cubren las tres primeras y comprueban que un uso recibe la fuente de su resultado efectivo.
- El comprobante real de `CALC-ENVIPE-0001` quedó asentado en `forense/replay-evidencia.tsv`: ENVIPE 2025, 39 resultados sobre razones de no denuncia, C1/C2, U1/U3, U4 y bootstrap; sello coincidente, spec, inputs, código, parámetros, seed y dependencias idénticos; 39/39 resultados reproducidos, deltas numéricos cero. Fecha `2026-09-10T19:22:26-06:00`; entorno `CLI-UBUNTU-WSL2 · Python 3.14.4 · numpy 2.3.5 · pandas 2.3.3`.
- El seco `registro --fuentes` propuso 139 corridas, 2889 resultados y 205 usos. La publicación explícita `registro --escribe --lote CALC-ENVIPE-0001` se negó antes de escribir porque cambiaría 64 campos de replay de 32 corridas ajenas. No se usó `--force` ni se amplió el lote.

## Inmutabilidad comprobada

| Pieza | SHA256 antes y después |
|---|---|
| `data/corrida0/demanda-resultados.tsv` | `03618a288c1530acadbbd11c9552b2da3875f5d2cedf8f957fa6fb555f528c1d` |
| `data/corrida0/demanda-corridas.tsv` | `a7f57269eaf39596db5ac22f9180ed38d35fe7e24c676039ee4ca364dfb80db2` |
| `data/corrida0/corridas.tsv` | `c663dba43e17a345ea313fc4525c2818f7fea086c392c18929fa6dff7862f962` |
| `data/corrida0/resultados.tsv` | `11c45d3a81c882b7d2125497324c3fb039f61d190382a463fa8dcb87b7a09fbd` |
| `data/corrida0/usos.tsv` | `e8ff1333dc57c6a844b061eda4f92324087be90c99ebb705e440cc643f747e5f` |

## Transiciones ajenas rechazadas

`Hash inputs` es SHA256 de la cadena canónica completa `input_sha256_efectivos`; la columna `Input` da cantidad e IDs iniciales para identificar el conjunto sin duplicar cientos de campos. `Antes/después` expresa `resultado_replay / contexto_replay`.

| Corrida | Antes | Después | Input | Hash inputs | Causa |
|---|---|---|---|---|---|
| `CALC-C0D-MARCADOR--aca07923903a` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `REPRODUCE / IDENTICO` | 258: `IN-MARCO-V1-3`, `IN-SCORING-M3`, `IN-AGREGADO-V1-3-RESULTADO`… | `9d3f1fc310d8c8bf123b9041ec9f6d64c09343dad7c03b34addee90ba9433094` | asiento heredado contradice la vista publicada |
| `CALC-C0D-MARCADOR-v2--e6fe5cea2f5d` | `NO-REPRODUCE · CONTEXTO-DISTINTO / DISTINTO` | `REPRODUCE / IDENTICO` | 260: `IN-L-EXTRAIDO-V1-2`, `IN-SPEC-SELLADA-V1-1`, `IN-MARCO-V1-3`… | `86d74b6bb11ff088615e8228e69d6367eb4419240c24d6958ab7c8c538e412a8` | asiento heredado contradice la vista publicada |
| `CALC-DUELO-0001--e905fed3578e` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 114: `cap_CIV-M-01_L_solo_01`, `cap_CIV-M-01_L_solo_02`, `cap_CIV-M-01_L_solo_03`… | `ccad00267d3d6ebb19e5528c8d8cf85f8e61065975eae94a439104ba395635a0` | `SIN-FUENTE` |
| `CALC-ENCIG-0001--c3ae00e62e59` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 2: `encig25_base_datos_csv`, `IN-ENCIG-SPEC-SELLADA` | `fc2c1a8f7f9ae57e0a768e890d7d4ca8f0c40db36d767e205ad8f6aa0e464adb` | `SIN-FUENTE` |
| `CALC-ENCUCI-0001--18d21cdff449` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 2: `encuci2020_bd_dbf`, `IN-ENCUCI-SPEC-SELLADA` | `07a73b2f6393e056ad01006e00d1c9eef506d9db949edd33c7f5bc38843074c4` | `SIN-FUENTE` |
| `CALC-ENIF-0001--afbf3c76d71b` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 2: `enif_2024_enif_2024_bd_csv`, `IN-ENIF-SPEC-SELLADA` | `3ff3abfaf5107b78c3baefe8e243967e1b1c65c2a2f039825f2055f6da50aa83` | `SIN-FUENTE` |
| `CALC-R-DIN-M-01--3d8e024f64d6` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 4: `ennvih1_2002_hogar_dta`, `ennvih1_2002_ponderador`, `IN-CODIFICACION-R-V1-1`… | `741b6917be18adccb55926b550a11907e9c42490f0eec8b8a6d3222e1bed9f1b` | `SIN-FUENTE` |
| `CALC-R-DIN-M-01-v2--a796ed134a16` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 4: `ennvih1_2002_hogar_dta`, `ennvih1_2002_ponderador`, `IN-CODIFICACION-R-V1-1`… | `77fe8702f9a96111cea225be76708e122277953008e0cf3f58f6a963478d24cf` | `SIN-FUENTE` |
| `CALC-R-DIN-M-01-v3--b33438455954` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 4: `ennvih1_2002_hogar_dta`, `ennvih1_2002_ponderador`, `IN-CODIFICACION-R-V1-2`… | `1a0b3f175d87936cd47e66ca4b475f221a53b2f660828ee2a19b32cc4a7df51d` | `SIN-FUENTE` |
| `CALC-R-DIN-M-01-v4--be85dac5f660` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 8: `ennvih1_2002_hogar_dta`, `ennvih1_2002_ponderador`, `IN-CODIGO-ARBITRA`… | `0d1ca0a78762b59d375dc85b958f4092d38d957ec32d28272bd772c44e964a3f` | `SIN-FUENTE` |
| `CALC-R-FAM-M-01--6f2c4a08ac71` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enif2018_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `b2be0faedf16b98b1ea9e56d97d17850158318ba59c6fbd42ed2a8bb7290bd0c` | `SIN-FUENTE` |
| `CALC-R-FAM-M-01-v2--98be8f02c99c` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enif2018_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `c072197194e7e8f052aa02e80236564937613faf7c8dfa912fe82cdaaada0e11` | `SIN-FUENTE` |
| `CALC-R-FAM-M-01-v3--67c15af3b8ae` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `enif2018_csv`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `4bca1be59d35b7bbc74f3dbf9fbc871dfa341449ab2a49ec73a96cb77f8bf3f0` | `SIN-FUENTE` |
| `CALC-R-FAM-M-05--5111ae11d465` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2016_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `3a84f77e529184db2e5b6c8dad4346a2ebfad1e51758fc0663acf620b3614495` | `SIN-FUENTE` |
| `CALC-R-FAM-M-05-v2--591940409156` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2016_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `dbb6003461e329e4d0c9c0c114581bc90ba60b896b6d143c56f831f1109560f1` | `SIN-FUENTE` |
| `CALC-R-FAM-M-05-v3--2f403e54ae30` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `enigh2016_nc_csv`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `c6c35dd11a6e439e391d0d4204998eaaadf90890a2aab331f67c1bc1d62c7cad` | `SIN-FUENTE` |
| `CALC-R-FAM-M-06--ea0445166b16` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2018_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `32500075ae79acb00ca11bd5643d48378bee198ba58dde4d2dbdef81c47f5186` | `SIN-FUENTE` |
| `CALC-R-FAM-M-06-v2--ae16bd5fd7a3` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2018_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `b29f3c95737daa0e3ee674e31ec109d4c64542a0d311539eee73570db6f97dae` | `SIN-FUENTE` |
| `CALC-R-FAM-M-06-v3--a32df7b4aaf9` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `enigh2018_nc_csv`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `d9dc029158d35403b34cf3809119c3483bfd477fc00c273dd79ce76d78516c47` | `SIN-FUENTE` |
| `CALC-R-FAM-M-07--c475b9d645f7` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2020_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `28ccf4202dc38b45886d4b21bd68be1ed848782f802292adab943d2e581f44dd` | `SIN-FUENTE` |
| `CALC-R-FAM-M-07-v2--f3034948f8c9` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `enigh2020_nc_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `78fbdf9ee1ad778fe35397c5bd7ac886e7f2ccf0424753457c2eea11a25510a5` | `SIN-FUENTE` |
| `CALC-R-FAM-M-07-v3--af3e74610050` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `enigh2020_nc_csv`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `e8b57c24cc3536953ac67781781d6f60e76329815e1ec04ee1ab582971094ab5` | `SIN-FUENTE` |
| `CALC-R-TRA-M-02--25bc1387eac3` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encuci2020_bd_dbf`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `2b626a7aa3a998e9c0534c69085369483fb8e820f54e921edb6d308a8bf1dd94` | `SIN-FUENTE` |
| `CALC-R-TRA-M-02-v2--534a48693b3d` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encuci2020_bd_dbf`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `e7165295a14540cfdc3881a6eadd44bb3a11abe284e1c25fff19f1c522a282ae` | `SIN-FUENTE` |
| `CALC-R-TRA-M-02-v3--e2dae47942fc` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `encuci2020_bd_dbf`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `be8d0855748f7af90e85e30f12acf7ca3db8f07f0c54aaec027df9e35acec515` | `SIN-FUENTE` |
| `CALC-R-TRA-M-03--0eef08f24eca` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encig_2013_encig13_base_datos_dbf`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `5663ee333ed29adcdabcbcc24033c4509dac3a2d64d73833fcb06ff97e632899` | `SIN-FUENTE` |
| `CALC-R-TRA-M-03-v2--ca02150fe81c` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encig_2013_encig13_base_datos_dbf`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `d9eb519c88d7654f798ed013afab051ea5f6d3be6e2eb3ca9a543af662b8d447` | `SIN-FUENTE` |
| `CALC-R-TRA-M-03-v3--78fc1d76aac4` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `encig_2013_encig13_base_datos_dbf`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `5fc0c739c0487009f81f2a0106587bc751bb2ea60cc5987d1a1fd601dc4ee4a7` | `SIN-FUENTE` |
| `CALC-R-TRA-M-07--80300420a54d` | `REPLICA-RESULTADO · CONTEXTO-DISTINTO / DISTINTO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encig2021_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `a3d9cea6f60e36287267317d4e9551eb5557180898a97d3de1f657dbd62fd5b6` | `SIN-FUENTE` |
| `CALC-R-TRA-M-07-v2--3a962a16f863` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 3: `encig2021_csv`, `IN-CODIFICACION-R-V1-1`, `IN-MARCO-R-V1-3` | `b39cfa6a6a9ac94f9c5a1e49223d163d31d6927ef279d8205ceda6a0dfff9c6c` | `SIN-FUENTE` |
| `CALC-R-TRA-M-07-v3--9557bf487772` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 7: `encig2021_csv`, `IN-CODIGO-ARBITRA`, `IN-CODIGO-CORRER-R`… | `9d4f5f1b9d4d9f4f6ec85303b013cd9e11aa029b93d46b2e5a96995cae5b5bb5` | `SIN-FUENTE` |
| `CALC-TRIADA-0001--4629bc2bc875` | `REPRODUCE / IDENTICO` | `NO-VERIFICADO / NO-VERIFICADO` | 248: `triada_spec_md`, `universo_triada_v1_4`, `marco_m_sorteado_v1_3`… | `1acdae422493eb35c8b4a6e259698a65cd36935568f74f9b594291c5c2ad2d7c` | `SIN-FUENTE` |

## Estado de los tres NC

| NC | Estado de cierre | Evidencia |
|---|---|---|
| `NC-0141` | CERRADA | escritura real confinada a temporal, 84/84 y hashes de demanda invariantes |
| `NC-0148` | CERRADA | guard compartido y fixture 1/2/0 con cita histórica, 8/8 |
| `NC-0104` | ABIERTA, parcial | comprobante real y derivador completos; falta publicar efectivamente `fuente_replay` en las tres vistas |

PR #682 y PR #683 son antecedentes resueltos; este acto no reabre `NC-0140` ni `NC-0145`.

## NO-CORRIDO / RESERVAS

- No se publicaron las tres vistas: la compuerta `REPLAY-PISADO` preservó sus bytes ante 64 cambios ajenos. El sucesor debe adjudicar o producir evidencia para las 32 corridas de la tabla y volver a ejecutar una publicación explícita.
- La colisión administrativa quedó resuelta: PR #687 fusionó primero `ADR-455`; este acto, que fusiona después, se actualizó contra `main` y tomó `ADR-456`. No se copió trabajo sustantivo de aquel PR.
- No se recalculó, adoptó ni alteró ningún resultado sellado. El `verify` sólo reprodujo `CALC-ENVIPE-0001` y asentó su comprobante.
