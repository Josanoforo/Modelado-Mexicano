# ACTO MAESTRA30-E7 · R-SCORING — nota de cierre

**26/ago/2026.** Encargo: `forense/encargos/2026-08-26-E7-R-SCORING.md` (dirección, maestra-30, `SHA` de redacción `8b317d3`; archivado por `A.3` **antes** de ejecutar). `ADR-207`. Rama `acto/e7-r-scoring`.

**Rótulo, D-6.** Dirección rotuló el encargo con el token pelado `E7`, token que ya colisiona en el espacio `E`. Este acto **se declara `ACTO MAESTRA30-E7 · R-SCORING`** en todo archivo que escribe y no reclama el token pelado; queda censado en `canon/registro-rotulos.tsv`. El encargo archivado conserva el texto verbatim y por eso vive en `_T25_ARCHIVOS_CONOCIDOS` — el texto de dirección no se edita para complacer a un test.

---

## §1 · Firma de entorno (A.2)

| | |
|---|---|
| Clon | `/home/pc0/mm-e7-r-scoring`, worktree de `/home/pc0/Modelado-Mexicano` (clon existente; **no se clonó nada nuevo**) |
| Base | `3bc28b1` — `Merge pull request #377 from Josanoforo/acto/e6-l-run` |
| `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` | `sin_variable` (esperado) |
| Sonda de red | `curl -s -o /dev/null -w "%{http_code}" --max-time 10 https://www.inegi.org.mx/` → `200`. Nunca `curl -I`. **Este acto no descargó nada** — el encargo prohíbe la red y todo insumo estaba en corpus. |
| `data/raw` | symlink a `/home/pc0/mm-corpus/raw`. `ls data/raw/ \| head -1` → `2005trim1_csv.zip`; **321 entradas**. |
| `grep` | En UBUNTU `grep` envuelve `ugrep -I`. **Todo `grep` de este acto es `command grep`**, y se declara. |
| Espejo | No se tocó. Toda cifra sale del clon, con el comando a la vista. |

**El `SHA` se movió y se re-derivó, no se asumió.** El encargo declara `8b317d3`; `main` estaba en `3bc28b1`, tres merges por delante (`#375`/`ADR-204`, `#376`/`ADR-205`, `#377`/`ADR-206`).

---

## §2 · Compuerta cero

**Hashes `F1` — 6 de 6 COINCIDEN**, re-calculados contra `3bc28b1` (no se citó el cálculo hecho contra el `SHA` viejo). Cero discordancias ⇒ `A.7` no aplica.

```
a772a4bc…a45b1d  pipeline-L-adv1-m2.py          14dbf289…a94ebf1  corredor-B-tasa-base.py
7752ced2…6b63767d corredor-E-combinacion-LM.py  beec0e1c…beba8e0efb scoring-adv1-m3.py
3a0dcf01…0c3742e2 marco-congelado-piloto-v1_0.tsv 140b00a8…fbf251c11 sorteo-resultados-v1_0.md
```

**Gate de E6 — abre, y no por la cifra que el encargo pedía.** El encargo exige `240` JSON en `corridas-L/` y manda `PARO` por debajo. Hay **`120`**:

```
$ git ls-tree -r --name-only origin/main -- forense/prereg-duelo-v2/corridas-L/ | wc -l
120
   .json 120 · L-solo 120 · L+corpus 0 · celdas distintas 15 · repeticiones por celda 8 (valor único)
```

**`FP-165` está `FIRMADA` y nombra a este acto**, verbatim: «AGUAS ABAJO, y por eso se declara aquí **para que E7 no pare en falso** […] eso es **REPORTE, no PARO**. NO gatea: L-solo, la comparación principal FP-162, los hashes F1, el corredor B, ni el árbitro R». La cifra `240` se redactó **antes** de esa firma. La firma es posterior, más específica y enumera qué no gatea: **la compuerta abre**.

**`valor_extraido`** — A.13, universo examinado: **los 120 archivos, uno por uno**: **103 poblados · 17 `null` · 0 ausentes**. `17/120` = 14.2%, no «`null` masivo».

**El entregable no existía** — A.13 con conteo propio: `find forense data milpa canon -type f` → **1 920 archivos examinados**; `corridas-R` **0**, `marcador-piloto` **0**, control positivo `corridas-L` **120**.

---

## §3 · Paso 2 — la derivación de M, y el PARO-reporte que produjo

Detalle completo en `corridas-R/DERIVACION-M-v1_0.md`. En corto:

- El procedimiento sellado **existe y cubre las 15** (`forense/crosswalk-pregunta-regla-v1_0.tsv`, 60 filas, **cero celdas ausentes**).
- Su salida: **`NO-EMITE` en 12**, `CANDIDATO-EMITE` en 3.
- **Los 3 `CANDIDATO-EMITE` son falsos positivos de subcadena**, abiertos uno por uno: `P7_1` empareja `AP7_1` de ENCUCI y `P7_12_7` de ENASIC; `P5_3` empareja `AP5_3_XX` de ENVIPE 2025 y `AP5_3_6/7/8` de ENCUCI 2020; `P2` empareja la cadena `(P2 §2.d)`, **una referencia documental**. `construir_crosswalk` decide con `if var and var in l` y **no compara la columna `encuesta`**.
- Y aunque no lo fueran: su propio docstring dice que `CANDIDATO-EMITE` «**exige aún enlace de escala/universo declarado antes de emitir**», y esa pasada **no está sellada en el árbol**. Nada mapea `SpecCelda → (regla, conducta)`.

**Huérfanas, lista exacta como el encargo pide: `DIN-03`, `DIN-11`, `TIC-06`.** Las otras 12 no son huérfanas — el procedimiento las cubre y responde `NO-EMITE`, que `emisor.py` declara «salida de primera clase, nunca silencio».

**No se inventó un mapeo ni se tocó el crosswalk.** Los falsos positivos se reportan; no se reparan.

---

## §4 · Los tres commits del Bloque D, más uno

| commit | qué |
|---|---|
| `A.3` | encargo íntegro, antes de ejecutar |
| **`COMMIT-1`** | `PROCEDIMIENTO-R-v1_0.md` + `DERIVACION-M-v1_0.md`, **antes de abrir un solo valor** |
| **`ENMIENDA 1`** | **por adición, no hacia atrás** — el `COMMIT-1` no se editó |
| **`COMMIT-2`** | las corridas |

**La `ENMIENDA 1` existe porque el `COMMIT-1` tenía dos huecos y un error, los tres hallados leyendo catálogos y descriptores — sin abrir un valor:**

- **(A)** faltaba la regla de codificación `y→{0,1}`. Se congeló por celda con la etiqueta verbatim del catálogo. **`CIV-08` lleva polaridad invertida** (`y=1` es el código `2`, *Inseguro*), porque la celda mide **inseguridad** percibida; declararlo antes de correr es lo que impide elegir después la polaridad que cuadre.
- **(B)** **error del `COMMIT-1`:** nombró `ENTI2022_05A11.DBF` (5 a 11 años) cuando el universo es 12 a 17. Al ir a corregirlo apareció algo peor: la `SpecCelda` de `TIC-06` tiene **cuatro referentes incompatibles** — `variable P2` es «¿comparten un mismo gasto para comer?» (tabla `VIV`); el universo nombra `ENTI2022_CB12A17.DBF`, que **no existe**; el estimador nombra la categoría «Tiene menos de un año en este trabajo», que es **`P5F15` de `COE1`**; y la `frase_discriminacion` nombra «Trabaja todos los meses del año», que es **`P5F14`**, otra categoría. El marco está sellado y **no se edita**: `TIC-06` → `RESERVA-SPEC-INCONSISTENTE`. Arbitrables **10 → 9**.
- **(C)** `TIC-12` es `categorica k=10` y su estimador dice «por categoría»: se congeló la categoría `8` como `R` principal (la que la propia `frase_discriminacion` señala) y **el vector completo de las 10 se escribe igual** en el JSON.

---

## §5 · Payloads (A.1) y diseño de varianza

**12 invocaciones de `tests/manifiesto.py --verifica --id <id>`, una por payload: 12 de 12 `COINCIDE`.** Cero discordancias, cero ausentes. **Este acto no descargó nada.**

**Celdas `MAPEADO` vs. reserva** — el diseño de varianza sale de `data/diseno-muestral.yaml` y **jamás se infiere de otra encuesta**:

| celda | encuesta | ponderador · estrato · UPM | estado |
|---|---|---|---|
| CIV-08 | ENVIPE 2023 | `FAC_ELE` · `EST_DIS` · `UPM_DIS` | MAPEADO |
| DIN-03 | ENIF 2012 | `FAC_PER` · `EST_DIS` · `UPM_DIS` | MAPEADO |
| DIN-05 | ENFIH 2019 | `FACTOR` · `EDIS` · `UPM_DIS` | MAPEADO |
| DIN-11 | ENIF 2018 | `fac_per` · `est_dis` · `upm_dis` | MAPEADO |
| SFT-04 | ENASEM 2018 | `FACTORI_18` · `EST_DIS` · `UPM_DIS` | MAPEADO |
| SFT-06 | ENASEM 2024 | `FACTORI_24` · `EST_DIS_24` · `UPM_DIS_24` | MAPEADO |
| TIC-01 | ENOE 2024 T1 | `fac_tri` · `est_d_tri` · `upm` | MAPEADO-CON-JOIN |
| TIC-08 | ENDUTIH 2024 | `FAC_PER` · `EST_DIS` · `UPM_DIS` | MAPEADO |
| TIC-12 | ENOE 2024 T1 | `fac_tri` · `est_d_tri` · `upm` | MAPEADO-CON-JOIN |
| DIN-07 | ECF Banxico/CNBV 2019 | — | **RESERVA-SIN-MICRODATO** |
| EMP-02 | ENAFIN 2024 | — (censo dice `PENDIENTE`) | **RESERVA-SIN-MICRODATO** |
| EMP-04 | ENAFIN 2024 | — (censo dice `PENDIENTE`) | **RESERVA-SIN-MICRODATO** |
| EMP-05 | CPV 2020 C. Ampliado | — | **RESERVA-SIN-MICRODATO** |
| DOC-06 | BMV / HR Ratings | no aplica (censo administrativo) | **RESERVA-SIN-PAYLOAD** |
| TIC-06 | ENTI 2022 | — | **RESERVA-SPEC-INCONSISTENTE** |

**Las dos uniones se declararon antes de correr.** ENOE: `p3i`/`p3n` viven en `COE1`, `est_d_tri` en `SDEM`; llave `cd_a+ent+con+v_sel+n_hog+h_mud+n_ren`. ENIF 2012: `SEXO`/`EDAD` vienen de `stsdem_e2`, llave `CONTROL+VIV_SEL+HOGAR+R_SEL=N_REN`.

**Por qué las cuatro `SIN-MICRODATO` lo son, verificado y no supuesto:** ENAFIN publica **tabulados** (`tr_enafin_tam_sec_loc_2024.csv`, `tr_enafin_tot_2024.csv`), no registros — `FAC_EXPA` no aparece porque no hay registro que ponderar. La ECF Banxico/CNBV solo trae un XLSX de tabulados y un PDF de manual. De CPV 2020 el corpus tiene CAAS (unidad área), ITER (localidad) y CEU (manzana/vialidad): `SITUA_CONYUGAL` **no aparece como columna en ninguno de los 6 CSV examinados**. `DOC-06` no tiene payload alguno **y** su ola de árbitro (`4T2026`) es futura respecto de hoy.

---

## §6 · SKIP y estratos singleton

**`CV ≥ 30% ⇒ SKIP` (FP-79) aplicado aquí y solo aquí: CERO SKIP en las 9.**

| celda | CV | | celda | CV |
|---|---:|---|---|---:|
| DIN-05 | 11.73% | | DIN-11 | 1.58% |
| SFT-04 | 6.86% | | TIC-12 | 0.51% |
| DIN-03 | 4.30% | | CIV-08 | 0.44% |
| SFT-06 | 2.56% | | TIC-08 | 0.26% |
| TIC-01 | 1.46% | | | |

Ninguna se acerca al umbral. **Estratos singleton: 1 en `SFT-04` y 1 en `TIC-08`**, escritos en su JSON y **no forzados a cero** — la cláusula que el docstring de `prop_ultimate_cluster` exige.

---

## §7 · El marcador y lo que exhibe

`forense/prereg-duelo-v2/marcador-piloto-v1_0.md`, con la cabecera verbatim de `D-i`.

**Cuatro de los cinco corredores están vacíos**, cada uno por una razón distinta y verificada: `L+corpus` no ejecutado (`FP-165`), `M` `NO-EMITE` en las 15, `B` `SIN_BASELINE` en las 15, `E` `INEJECUTABLE` (`ADR-141`). **`L-solo` es el único con valores**, y `R` el único árbitro.

**El scoring no adjudica porque no arranca.** Ejecutado, falla cerrado: `CONFIGURACION_INVALIDA: se requiere exactamente 1 corredor L/corpus; hay 0`. Registro en `corridas-R/_scoring-intento.json`. **No se le pasó una configuración falsa para arrancarle números.**

**Ninguna casilla de `ADV1-M5 v2` es evaluable**, y no solo por `D-i`: las cinco se deciden sobre `IC(Δs)` y `s` es *skill* **contra `B`**. Sin `B` no hay `s`.

**Comparación principal `L-solo` (FP-162), 9 celdas:** **1 dentro de la banda TOST** y **1 dentro del `IC80` de `R`** — la misma, `CIV-08`. Desviación absoluta mediana **14.34 pp**, máxima **57.95 pp** (`TIC-08`). **`L+corpus` como auxiliar: no hay auxiliar.**

**`CIV-08` se reporta como cae, con su reserva.** `L-solo` `62.00%` contra `61.88% ± 0.270`: dentro de la banda por `0.12` pp sobre una banda de `0.135` — **margen de 0.015 pp**. No se convierte en «acierto»: una celda de nueve, banda estrecha porque el `EE` es pequeño, y la constante `0.5` que la define **no está firmada** (`FP-163`). `IC`/banda que no despejan se reportan como caen, jamás se fuerza casilla.

---

## §8 · Firma abierta

**`FP-166`, `ABIERTA`** — mesa decide qué hacer con el piloto a la vista de que cuatro de cinco corredores no tienen valores. Cuatro caminos documentados sin editarlos hacia atrás: (i) aceptar el marcador tal como cae; (ii) sellar el enlace `SpecCelda → (regla, conducta)` para que `M` emita; (iii) adquirir tasa base para `B`; (iv) re-sellar el contrato de scoring para menos de cuatro corredores — la opción que `FP-165` dejó nombrada y **no ejercida**. **Este acto no elige:** `D-i` le prohíbe adjudicar y el perímetro le prohíbe tocar `ADR-141`, el crosswalk y el marco congelado.

---

## §9 · Perímetro, desviaciones y lo que este acto NO hizo

**Perímetro tocado**, dentro de la lista del encargo: `corridas-R/**` (nuevo) · `marcador-piloto-v1_0.md` (nuevo) · esta nota · el encargo (`A.3`) · `canon/gobernanza-v1_15.md` · `canon/estado-programa-v1_10.md`.

**Extensión mínima declarada, con precedente:** `forense/firmas-pendientes.tsv` (abre `FP-166`, mismo movimiento que `E6` con `FP-165`), `canon/registro-rotulos.tsv` y la lista blanca `T25` de `tests/check.py` (desviación mecánica del CI por el rótulo pelado — precedente `E4`, `E5`, `E6`).

**NO se hizo:** adjudicar casilla o letra · mover tier · abrir fila de tablero · tocar `corridas-L/` (solo lectura) · editar `milpa/` · re-implementar los scripts pineados o `svystat.py` (se importan) · inferir diseño de varianza de otra encuesta · cruzar escalas sin enlace · usar la red · editar el marco congelado, `ADR-141` o el crosswalk.

**Suite:** `python3 tests/check.py --baseline` — **LÍNEA BASE VERDE** en **19 FAIL · 128 WARN**. Se cita el núcleo, no el modo plano. El acto subió el `WARN` en 1 y no movió el `FAIL`. Tres correcciones de propagación que su propia escritura hizo necesarias:

- **`T15`** — el conteo de ADR citado en la cabecera de `gobernanza`, en la tabla `§0` de `estado` y en `§L0` subió a `207`.
- **`T16`** — las dos afirmaciones de `ADR-206` sobre su corrida dejaron de ser vigentes al escribir `ADR-207` y se marcaron `{cita-historica}`, con la marca **fuera** de las negritas: es el tramo que `T16` empareja, y `T15` empareja el contrario. Son reglas distintas y **no se generalizan la una a la otra**.
- **`T25`** — los cuatro documentos nuevos traían `E7` pelado. `D-6` aplicado donde se puede aplicar: el acto se declara **`ACTO MAESTRA30-E7 · R-SCORING`** en todo archivo que escribe, con el mismo prefijo que la fila `MAESTRA30-E1..E4` del registro por ser de la misma serie de dirección. **Solo el encargo archivado (verbatim, `A.3`) y esta nota entran a la lista blanca** — los documentos de trabajo se arreglaron de verdad, no se eximieron.

**Y un cuarto arreglo que fue error propio, no propagación:** el negativo del lector `DBF` (`dbfmini.field_names` devuelve tuplas `(nombre, tipo, ancho)`, no cadenas) dio «la variable no aparece» en las tres tablas `DBF` del piloto. **El control positivo lo destapó** — imprimir los campos realmente leídos mostró `P7_1` en la lista. Sin ese control, `DIN-03`, `TIC-06` y `TIC-08` habrían entrado al marcador como celdas sin columna localizable.
