# PROCEDIMIENTO R v1.0 — congelado antes de abrir un solo valor de microdato

**ACTO MAESTRA30-E7 · R-SCORING**, 26/ago/2026. `COMMIT-1` de la regla de dos commits del Bloque D.

**Qué es.** La especificación completa de cómo se computará `R` — el valor del microdato — para cada una de las 15 celdas del piloto ADV1-M2, y de cómo se computará su `EE(R)` de diseño. Se congela **antes** de que este acto lea un solo valor. Lo único que se leyó para escribirlo fueron **nombres de columna y etiquetas de variable**, que es exactamente lo que el encargo permite («permitido leer nombres/etiquetas de variables para localizar la columna; prohibido mirar un valor antes de este commit»).

**Qué NO es.** No es una re-derivación del marco: la `SpecCelda` de cada celda —encuesta, ola, universo, variable, estimador, escala— se copia **verbatim** de `forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv` (`sha256 3a0dcf01…0c3742e2`, verificado en la compuerta cero). Este documento añade únicamente lo que el marco no fija: **qué payload, qué tabla, qué columna y qué diseño de varianza**.

---

## 1 · Estimador y varianza — la regla, una sola vez

**Estimador puntual.** Proporción ponderada (o su razón, donde la `SpecCelda` diga `razón ponderada`):

```
p_hat = Σ(w·y) / Σ(w)
```

**Varianza.** `EE(R)` se calcula con el estimador de **conglomerado último** (*ultimate cluster*, Wolter) ya sellado en el repo — **`tests/svystat.py:prop_ultimate_cluster`**, que este acto **importa y no reimplementa**:

```
t_h_i = Σ(w·y) en la UPM i del estrato h        n_h_i = Σ(w) en la UPM i del estrato h
e_h_i = t_h_i − p_hat · n_h_i
var(p_hat) = (1/N_hat²) · Σ_h [ (n_h/(n_h−1)) · Σ_i (e_h_i − ē_h)² ]
EE(R)  = √var(p_hat)
```

Su contrato, verbatim del docstring: «Estratos con una sola UPM no aportan varianza estimable con este método (grados de libertad insuficientes) — **se reportan aparte, no se fuerzan a cero silenciosamente**». Este acto respeta esa cláusula: `n_estratos_singleton` se escribe en el JSON de cada celda.

**Por qué este y no otro.** Es el estimador que `U2-CRUCE` (PR #335, ADR-165) ya validó reproduciendo una cifra publicada del INEGI **al peso y su EE a nueve decimales** sobre la misma muestra. No se elige aquí: se hereda.

**CV y SKIP.** `CV = EE(R)/R`. La regla `CV ≥ 30% ⇒ SKIP` (FP-79) se aplica **en el COMMIT-2 y solo ahí**, con cada SKIP listado junto a su CV. Este documento no anticipa ningún SKIP porque no ha visto ningún valor.

**Banda TOST.** `Δ_material = 0.5 · EE(R)` de la celda evaluada, **regla de forma, no constante numérica** — `prereg-corrida-v1_0.md` F3, verbatim: «la banda es una regla de forma (fracción del EE propio de cada celda…), no una constante numérica fija». La constante `0.5` **no está firmada por mesa** (`FP-163` sigue abierta en esos términos): se aplica como el prereg la propaga, y el marcador lo dirá.

---

## 2 · Verificación de payload (A.1)

Una invocación de `tests/manifiesto.py --verifica --id <id>` por payload, salida cruda pegada en la nota de cierre. **12 de 12 COINCIDE**, cero discordancias. Un payload ausente o con hash discordante es `PARO`, no descarga — este acto **no toca la red**.

---

## 3 · Las 15 celdas, una por una

`estado_R` tiene cuatro valores y ninguno informal: **`MAPEADO`** (payload de microdato presente, columna localizada, diseño con los tres campos citados en `data/diseno-muestral.yaml`) · **`MAPEADO-CON-JOIN`** (igual, pero la variable y el diseño viven en tablas distintas y hay que unirlas — la llave se declara aquí, antes de correr) · **`RESERVA-SIN-MICRODATO`** (el payload existe y su hash coincide, pero **no es microdato**: son tabulados o una unidad de análisis distinta de la que la `SpecCelda` pide) · **`RESERVA-SIN-PAYLOAD`** (no hay payload).

Las dos `RESERVA-*` **se escriben, no se silencian**, y ninguna se corre con diseño inferido de otra encuesta — el encargo lo prohíbe expresamente y este procedimiento no lo hace en ningún caso.


### CIV-08 — ENVIPE, ola 2023

- **Universo** (verbatim del marco): población de 18 años y más (TPer_Vic1)
- **Variable** (marco): `AP4_4_03` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FAC_ELE`
- **Payload**: `envipe2023_csv` → `envipe2023_csv.zip`
  - `sha256 0dcc00a7fc37b79806f1bf1b85b12cd090b5ecc8e76983a3a1a861f2ef3fb404`
- **Tabla / columna**: `tper_vic1_envipe2023/conjunto_de_datos/conjunto_de_datos_tper_vic1_envipe2023.csv` · columna `AP4_4_03`
- **Diseño de varianza**: ponderador `FAC_ELE` · estrato `EST_DIS` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**

### DIN-03 — ENIF, ola 2012

- **Universo** (verbatim del marco): mujeres de 18 a 70 años, persona elegida del hogar, residentes en viviendas particulares
- **Variable** (marco): `P7_1` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FAC_PER`
- **Payload**: `enif_2012_bases_enif2012_dbf` → `bases_enif2012_dbf.zip`
  - `sha256 7bafcf6fdd3747bf330099dd752f2010441e0cd18fe942c35b15249d98092e55`
- **Tabla / columna**: `stmodulo2_e2.dbf` · columna `P7_1`
- **Diseño de varianza**: ponderador `FAC_PER` · estrato `EST_DIS` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**

### DIN-05 — ENFIH, ola 2019

- **Universo** (verbatim del marco): personas de 18 años y más residentes en viviendas particulares, en localidades de menor de 2,500 habitantes
- **Variable** (marco): `P8_1_1` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FACTOR`
- **Payload**: `enfih2019_bd_csv_zip` → `enfih2019/enfih_2019_base_de_datos_csv.zip`
  - `sha256 be372533d5043920892142e8bf792b7293a5f20ab466a6441bc89925b42ef4d5`
- **Tabla / columna**: `TMODULO.csv` · columna `P8_1_1`
- **Diseño de varianza**: ponderador `FACTOR` · estrato `EDIS` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**
- **RESERVA DECLARADA**: El censo nombra EDIS como estrato de diseno; la tabla trae ademas ESTRATO, que NO se usa.

### DIN-07 — Encuesta de Competencias Financieras (Banxico/CNBV), ola 2019

- **Universo** (verbatim del marco): personas de 18 años y más que administran o aportan dinero al hogar, de nivel socioeconómico D o E (AMAI)
- **Variable** (marco): `SF2` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `PESOP`
- **Payload**: `banxico_encuesta_competencias_financieras_2019` → `banxico_encuesta_competencias_financieras_2019.xlsx`
  - `sha256 9fc9eb34e98b576991a13fbb63d60e5d61ef0e3bd018a93ca03a1c25538b698f`
- **Tabla / columna**: `(solo tabulados XLSX)` · columna `SF2`
- **Diseño de varianza**: ponderador `PESOP` · estrato `--` · UPM `--`
- **`estado_R`**: **RESERVA-SIN-MICRODATO**
- **RESERVA DECLARADA**: La ECF Banxico/CNBV no tiene microdato en el corpus: el unico payload de la ola 2019 es un XLSX de tabulados y un PDF de manual. PESOP y SF2 solo existen a nivel de registro. R NO computable.

### DIN-11 — ENIF, ola 2018

- **Universo** (verbatim del marco): personas de 18 a 70 años, persona elegida del hogar, residentes en viviendas particulares
- **Variable** (marco): `P5_3` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FAC_PER`
- **Payload**: `enif2018_csv` → `enif2018_csv.zip`
  - `sha256 51f33ec74ccd596dc74b695587310d02e651923467255520aadc4d9fe13461d5`
- **Tabla / columna**: `conjunto_de_datos_tmodulo_enif_2018/conjunto_de_datos/tmodulo.csv` · columna `P5_3`
- **Diseño de varianza**: ponderador `fac_per` · estrato `est_dis` · UPM `upm_dis`
- **`estado_R`**: **MAPEADO**

### DOC-06 — BMV / HR Ratings, Financiera Independencia (desenlace documentado no-e, ola 4T2024 parametriza, 4T2026 arbitra

- **Universo** (verbatim del marco): cartera de credito personal popular no bancario de Financiera Independencia (Findep)
- **Variable** (marco): `IMOR ajustado de la cartera total` · **Estimador**: razon sobre censo regulatorio · **Escala**: continua (porcentaje)
- **Ponderador que el marco pide**: `NO APLICA -- censo administrativo, no muestra`
- **Payload**: **ninguno en `data/manifiesto.yaml`**
- **Tabla / columna**: `--` · columna `IMOR ajustado`
- **Diseño de varianza**: ponderador `NO APLICA` · estrato `--` · UPM `--`
- **`estado_R`**: **RESERVA-SIN-PAYLOAD**
- **RESERVA DECLARADA**: Cero payloads en el manifiesto para BMV/HR Ratings/Findep. Ademas la propia SpecCelda dice '4T2026 arbitra': la ola del arbitro es FUTURA respecto de hoy (26/ago/2026). R no existe todavia POR DISENO, no por falta de busqueda.

### EMP-02 — ENAFIN (Encuesta Nacional de Financiamiento de las Empresas), ola 2024

- **Universo** (verbatim del marco): solicitudes de credito hechas por empresas en 2024, por tamano de empresa
- **Variable** (marco): `razon derivada de Creditos que fueron rechazados a las empresas sobre Total de creditos que solicitaron las empresas, po` · **Estimador**: razon ponderada · **Escala**: continua (proporcion)
- **Ponderador que el marco pide**: `FAC_EXPA`
- **Payload**: `adq15_enafin_conjunto_de_datos_enafin_2024_csv` → `ADQ15_ENAFIN_2024_RNM_INEGI/conjunto_de_datos_enafin_2024_csv.zip`
  - `sha256 0f0ff75db3b728f218e33210c9eb08e0c20ec04fe4317aacacfef45ab8cb5e45`
- **Tabla / columna**: `tr_enafin_tam_sec_loc_2024.csv` · columna `razon derivada`
- **Diseño de varianza**: ponderador `FAC_EXPA` · estrato `--` · UPM `--`
- **`estado_R`**: **RESERVA-SIN-MICRODATO**
- **RESERVA DECLARADA**: El 'conjunto de datos' publicado de ENAFIN 2024 son TABULADOS (prefijo tr_), no registros: 2 CSV de tabulado + diccionario + metadatos. FAC_EXPA no aparece porque no hay registro que ponderar. Ademas ENAFIN esta PENDIENTE en data/diseno-muestral.yaml (ponderador y estrato 'no determinable').

### EMP-04 — ENAFIN (Encuesta Nacional de Financiamiento de las Empresas), ola 2024

- **Universo** (verbatim del marco): creditos solicitados por empresas en 2024, por tamano de localidad
- **Variable** (marco): `razon derivada de Creditos que fueron aprobados sobre Total de creditos que solicitaron, contrastando localidades de 500` · **Estimador**: razon ponderada · **Escala**: continua (proporcion)
- **Ponderador que el marco pide**: `FAC_EXPA`
- **Payload**: `adq15_enafin_conjunto_de_datos_enafin_2024_csv` → `ADQ15_ENAFIN_2024_RNM_INEGI/conjunto_de_datos_enafin_2024_csv.zip`
  - `sha256 0f0ff75db3b728f218e33210c9eb08e0c20ec04fe4317aacacfef45ab8cb5e45`
- **Tabla / columna**: `tr_enafin_tam_sec_loc_2024.csv` · columna `razon derivada`
- **Diseño de varianza**: ponderador `FAC_EXPA` · estrato `--` · UPM `--`
- **`estado_R`**: **RESERVA-SIN-MICRODATO**
- **RESERVA DECLARADA**: Identica a EMP-02: mismo payload, mismos tabulados, mismo estado PENDIENTE del censo de diseno.

### EMP-05 — CPV Censo de Poblacion y Vivienda -- Cuestionario Ampliado, ola 2020

- **Universo** (verbatim del marco): personas de 20 a 29 anos residentes en viviendas particulares habitadas
- **Variable** (marco): `SITUA_CONYUGAL` · **Estimador**: proporcion ponderada · **Escala**: categorica k=8
- **Ponderador que el marco pide**: `FACTOR`
- **Payload**: `cpv2020_caas_eum_csv` → `Censo2020_CAAS_eum_csv.zip`
  - `sha256 10b56a3b724c14c000464f3a632a9eb845dd5fa0ffc800d16644840d74b7c125`
- **Tabla / columna**: `(ninguna tabla de persona)` · columna `SITUA_CONYUGAL`
- **Diseño de varianza**: ponderador `FACTOR` · estrato `ESTRATO` · UPM `UPM`
- **`estado_R`**: **RESERVA-SIN-MICRODATO**
- **RESERVA DECLARADA**: Los tres payloads CPV del corpus son CAAS (TI_TRA/TI_USU/TR_ALO, unidad area), ITER (localidad) y CEU (manzana/vialidad). SITUA_CONYUGAL no aparece como columna en ninguno de los 6 CSV examinados. La muestra del Cuestionario Ampliado a nivel PERSONA no esta en el corpus.

### SFT-04 — ENASEM, ola 2018

- **Universo** (verbatim del marco): Personas de 50 años y más residentes en la vivienda seleccionada y su cónyuge o pareja de cualquier edad, entrevista directa (tabla sect_a_c_d_f_e_pc_h_i; AGE_18 017…107)
- **Variable** (marco): `H16D_18` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FACTORI_18`
- **Payload**: `enasem2018_bd_csv_zip` → `enasem2018/enasem_2018_bd_csv.zip`
  - `sha256 bfd8ffd172e2728f7822a953e338bfbd47fd181f8f4725866d98a12b41c13a3b`
- **Tabla / columna**: `SECT_A_C_D_F_E_PC_H_I_2018.csv` · columna `H16D_18`
- **Diseño de varianza**: ponderador `FACTORI_18` · estrato `EST_DIS` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**

### SFT-06 — ENASEM, ola 2024

- **Universo** (verbatim del marco): Personas de 50 años y más residentes en la vivienda seleccionada y su cónyuge o pareja de cualquier edad, entrevista directa (tabla TR_ENASEM24_SECT_A_C_D_E_PC_F_H)
- **Variable** (marco): `F55_24` · **Estimador**: proporción ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FACTORI_24`
- **Payload**: `enasem2024_bd_csv_zip` → `enasem2024/enasem_2024_bd_csv.zip`
  - `sha256 6712f1b0cc5e15f70c7124c2de2f7d398e419d4d1e5adcf3c673363dfbd1c9a4`
- **Tabla / columna**: `tr_enasem24_sect_a_c_d_e_pc_f_h_i.csv` · columna `F55_24`
- **Diseño de varianza**: ponderador `FACTORI_24` · estrato `EST_DIS_24` · UPM `UPM_DIS_24`
- **`estado_R`**: **MAPEADO**

### TIC-01 — ENOE, ola 2024 1er trimestre

- **Universo** (verbatim del marco): poblacion ocupada subordinada y remunerada de 15 anios y mas residente en viviendas particulares, con empleo actual (tabla COE1), por sexo
- **Variable** (marco): `p3i` · **Estimador**: proporcion ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `fac_tri`
- **Payload**: `enoe_2024_1t_csv` → `conjunto_de_datos_enoe_2024_1t_csv.zip`
  - `sha256 0beed808bf4f1457d6ec13600a8bdd3ca8db7e7276ab14675a44e74e6a33592c`
- **Tabla / columna**: `coe1 ⨝ sdem` · columna `p3i`
- **Diseño de varianza**: ponderador `fac_tri` · estrato `est_d_tri` · UPM `upm`
- **`estado_R`**: **MAPEADO-CON-JOIN**
- **RESERVA DECLARADA**: p3i vive en COE1; est_d_tri vive en SDEM. Union por la llave estandar de ENOE (cd_a, ent, con, v_sel, n_hog, h_mud, n_ren). Declarado aqui, antes de correr.

### TIC-06 — ENTI, ola 2022

- **Universo** (verbatim del marco): poblacion de 12 a 17 anios residente en viviendas particulares con trabajo actual (tabla ENTI2022_CB12A17.DBF), por sexo (variable SEX de la misma tabla)
- **Variable** (marco): `P2` · **Estimador**: proporcion ponderada (categoria 'Tiene menos de un anio en este trabajo') · **Escala**: categorica k=3
- **Ponderador que el marco pide**: `FAC`
- **Payload**: `enti2022_bd_dbf_zip` → `enti2022/enti_2022_bd_dbf.zip`
  - `sha256 9443db5e0970d73795925766fe5bccd8c56687d3fe5b8946a9b67b4e10bceaf5`
- **Tabla / columna**: `ENTI2022_05A11.DBF` · columna `P2`
- **Diseño de varianza**: ponderador `FAC` · estrato `EST_D` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**
- **RESERVA DECLARADA**: El censo advierte que EST (C(2)) es distinta de EST_D (C(3)); se usa EST_D.

### TIC-08 — ENDUTIH, ola 2024

- **Universo** (verbatim del marco): persona elegida de 6 anios y mas (variable EDAD, tabla tic_2024_usuarios) residente en viviendas particulares, por estrato socioeconomico (variable ESTRATO de la misma tabla)
- **Variable** (marco): `P7_15` · **Estimador**: proporcion ponderada · **Escala**: binaria
- **Ponderador que el marco pide**: `FAC_PER`
- **Payload**: `endutih2024_bd_dbf_zip` → `endutih2024/endutih2024_bd_dbf.zip`
  - `sha256 ef723ed125c81c4a9036b74fab67f520de007a2d52c5e0b03d4ebec509e1ae87`
- **Tabla / columna**: `tic_2024_usuarios.DBF` · columna `P7_15`
- **Diseño de varianza**: ponderador `FAC_PER` · estrato `EST_DIS` · UPM `UPM_DIS`
- **`estado_R`**: **MAPEADO**

### TIC-12 — ENOE, ola 2024 1er trimestre

- **Universo** (verbatim del marco): poblacion ocupada subordinada y remunerada de 15 anios y mas residente en viviendas particulares, con empleo actual (tabla COE1), por ambito urbano/rural (variable ur de la misma tabla)
- **Variable** (marco): `p3n` · **Estimador**: proporcion ponderada (por categoria de medio de entero) · **Escala**: categorica k=10
- **Ponderador que el marco pide**: `fac_tri`
- **Payload**: `enoe_2024_1t_csv` → `conjunto_de_datos_enoe_2024_1t_csv.zip`
  - `sha256 0beed808bf4f1457d6ec13600a8bdd3ca8db7e7276ab14675a44e74e6a33592c`
- **Tabla / columna**: `coe1 ⨝ sdem` · columna `p3n`
- **Diseño de varianza**: ponderador `fac_tri` · estrato `est_d_tri` · UPM `upm`
- **`estado_R`**: **MAPEADO-CON-JOIN**
- **RESERVA DECLARADA**: Misma union que TIC-01; p3n vive en COE1.

---

## 4 · Recuento del procedimiento

| `estado_R` | celdas | cuáles |
|---|---:|---|
| `MAPEADO` | 8 | CIV-08, DIN-03, DIN-05, DIN-11, SFT-04, SFT-06, TIC-06, TIC-08 |
| `MAPEADO-CON-JOIN` | 2 | TIC-01, TIC-12 |
| `RESERVA-SIN-MICRODATO` | 4 | DIN-07, EMP-02, EMP-04, EMP-05 |
| `RESERVA-SIN-PAYLOAD` | 1 | DOC-06 |
| **arbitrables** | **10** | las de las dos primeras filas |
| **no arbitrables** | **5** | las de las dos últimas |

**Diez de quince celdas tienen árbitro computable.** Las otras cinco no lo tienen y este documento dice, celda por celda, por qué — antes de correr nada, que es la única forma de que esa cifra no sea una excusa construida después de ver el resultado.

---

## 5 · Lo que este procedimiento NO decide

- **No adjudica.** `D-i` manda: el marcador puntúa, no adjudica `ADV1-M5`, no mueve tier, no abre fila de tablero.
- **No sella la constante `0.5`** de la banda TOST — `FP-163` sigue en los términos en que `banda-tost-margen-v1_0.md §4` la dejó.
- **No re-implementa** ninguno de los tres scripts pineados ni `svystat.py`: los importa y los invoca conforme a sus propias firmas.
- **No toca `corridas-L/`** — solo la lee.
- **No decide qué hacer con las cinco celdas sin árbitro.** Las declara. Qué se hace con ellas es firma de mesa, no de este acto.

---

## 6 · Cierre

Este procedimiento queda congelado en el `COMMIT-1` de `ACTO MAESTRA30-E7 · R-SCORING`. El `COMMIT-2` lo ejecuta **sin editarlo**. Si el `COMMIT-1` resultara tener un error, un **tercer** commit lo dice — nunca se corrige hacia atrás.

«el primer resultado que produzca este procedimiento es el que se reporta»
