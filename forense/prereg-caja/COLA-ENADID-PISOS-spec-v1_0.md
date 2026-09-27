# Pisos por segmento ENADID 2018 (disolución conyugal por tipo de unión; jefatura femenina en hogares con migrante varón) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-COLA-COMPLETA-1`, 26/sep/2026, CAJA, rama `acto/gen2-cola-completa-1`,
0-bis `0d4ae74d`. Encargo: `forense/encargos/2026-09-26-GEN2-COLA-COMPLETA-1.md` (§1 (a), cola v1.1:
PAREJA/ENADID, MIGRACIÓN/ENADID). CALC: `CALC-ENADID-COLA-2018-0001`. Congelada en el COMMIT-1, **antes** de
leer un solo valor de ENADID (sólo el descriptor de archivos (FD) y la línea de cabecera de los CSV).
**El primer resultado que produzca este procedimiento es el que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Payload `enadid2018_bd_csv_zip` (manifiesto), sha256 `3c6643b7…` COINCIDE; miembros `TMujer2.csv`
  (mujeres de 15–54 con módulo de historia conyugal), `TSdem.csv` (sociodemográfico de todos los residentes) y
  `TMigrante.csv` (migrantes internacionales). Descriptor: `enadid2018_fd_xlsx` (sha256 `f776c495…`), hojas
  `TMUJER2`, `TSDEM`, `TMIGRANTE` de `fd_enadid18.xlsx` («Descriptor de archivos de captura», tabla
  `TR_ENADID18_TMUJER` etc.).
- `[EJECUTADO]` Olas en corpus: 1992, 1997, 2009, 2014, 2018, 2023. 2018 es la ola abierta para estas conductas;
  **2023 (`enadid2023_base_datos_csv` / prefijo `cc1_inegi_enadid_2023`) queda RESERVADA** (E.6, la más reciente
  del programa): no se abre, no se cita, no se nombra como input; el medidor la excluye por guardia
  (`EXCLUIDOS_PREFIJO`). Sin IC de persistencia entre olas.
- `[LEÍDO]` El medidor abre **dos marcos** con bootstrap propio (UPM `upm_dis` dentro de estrato `est_dis`, uno
  por marco): MUJERES (`TMujer2`, peso `fac_per`) y HOGARES (`TSdem`, peso `fac_viv`, cruzado contra `TMigrante`
  por `llave_hog`). No hay variable ya construida de «disolución conyugal» ni de «hogar con migrante»: ambas son
  derivadas de esta spec sobre códigos crudos del FD.

## 1 · Unidad, universo, diseño

**Marco MUJERES:** unidad **mujer de 15 a 54 años con módulo de historia conyugal** (`TMujer2`, universo `um`:
`edad_muj` entre 15 y 54). Peso `fac_per` (FD `TMUJER2` id 78 aprox., factor a nivel persona-mujer). Bootstrap de
UPM `upm_dis` dentro de estrato `est_dis` (FD `TSDEM` ids 92–93: estrato `001…608`, UPM `00001…10376`; la misma
llave de diseño se usa para leer el marco de mujeres). Válido: peso > 0, estrato y UPM no vacíos.

**Marco HOGARES:** unidad **hogar, renglón de la jefatura** (`TSdem` filtrado a `paren` = 1, «Jefa(e)», FD id 10).
Peso `fac_viv` (FD `TSDEM` id 78, «Factor de expansión a nivel vivienda», `22…5001`). Bootstrap de UPM `upm_dis`
dentro de estrato `est_dis` (mismos ids 92–93). Válido: peso > 0, estrato y UPM no vacíos. El cruce con
`TMigrante` es sólo para derivar la partición (con/sin migrante varón); no cambia la unidad ni el peso del hogar.

## 2 · Conductas (por texto de pregunta, FD `fd_enadid18.xlsx`)

**MUJERES**, sobre `P10_1` («Situación conyugal», FD `TMUJER2` id 124, texto: «¿Actualmente usted...», códigos
1 vive con su pareja en unión libre · 2 está separada de una unión libre · 3 está separada de un matrimonio ·
4 está divorciada · 5 está viuda de una unión libre · 6 está viuda de un matrimonio · 7 está casada · 8 está
soltera):

| conducta | subpoblación (estado alguna vez UNIÓN LIBRE o MATRIMONIO) | UNO | CERO |
|---|---|---|---|
| SEPARADA-ENTRE-UNION-LIBRE | `P10_1` ∈ {1, 2, 5} (unión actual o última fue unión libre: vive en unión libre, separada de unión libre, viuda de unión libre) | 2 (separada) | 1, 5 |
| SEPARADA-O-DIVORCIADA-ENTRE-MATRIMONIO | `P10_1` ∈ {3, 4, 6, 7} (unión actual o última fue matrimonio: separada, divorciada, viuda, casada) | 3, 4 (separada, divorciada) | 6, 7 |

Es prevalencia de disolución en el **stock** de uniones (alguna vez unida por esa vía), no un riesgo por duración
de la unión. Códigos 8 (soltera) y 9/blanco (no especificado, si aparecieran) quedan fuera de ambas subpoblaciones.
La razón entre las dos filas se compara contra el «3.4 veces» del report como **orden**, no como el mismo
estimando (el report puede usar un denominador o ventana distinta).

**HOGARES**, jefatura femenina (`SEXO` de la persona con `PAREN` = 1, FD `TSDEM` id 12, texto: «(NOMBRE) es
hombre / (NOMBRE) es mujer», códigos 1 Hombre · 2 Mujer), partida por presencia de emigrante internacional varón
vivo hoy fuera de México (`TMigrante`: `P4_6` «Sexo del migrante» id 15, texto «(NOMBRE) es hombre. / (NOMBRE) es
mujer.», 1 Hombre; `P4_15` «País de residencia actual» id 31, texto «¿En qué país vive actualmente (NOMBRE)?»,
1 Estados Unidos de América · 2 México · 3 Otro país · 9 no especificado — `P4_6` = 1 y `P4_15` ∈ {1, 3} identifica
un migrante varón que hoy vive fuera de México, sea EUA u otro país):

| conducta | subpoblación (hogares) | UNO | CERO |
|---|---|---|---|
| JEFATURA-FEMENINA-CON-MIGRANTE-VARON | hogares con ≥1 emigrante internacional varón (`P4_6`=1 ∧ `P4_15`∈{1,3}) en `TMigrante` bajo la misma `llave_hog` | `SEXO`=2 (mujer) | `SEXO`=1 (hombre) |
| JEFATURA-FEMENINA-SIN-MIGRANTE-VARON | hogares sin ese migrante | `SEXO`=2 | `SEXO`=1 |

`P4_15` = 9 (no especificado) no cuenta como «vive fuera»: sólo 1 y 3 marcan la partición «con migrante»; el resto
(incluido 9) cae del lado «sin». Esto es una lectura conservadora declarada por esta spec (el medidor no filtra
`P4_15`=9 aparte; lo trata como «no es 1 ni 3» y por tanto no marca `con`).

## 3 · Ejes (uno a la vez)

**MUJERES:** EDAD (`edad_muj`: 15–24, 25–34, 35–44, 45–54) · TAMLOC (`tam_loc`, FD id 9: 1 100 000+, 2 15 000–99
999, 3 2 500–14 999, 4 menor a 2 500) · ESCOLARIDAD (`niv`, FD id 150, «¿Cuál es el último año o grado que aprobó
(NOMBRE) en la escuela?», 00 ninguno…11 doctorado; agrupado HASTA-PRIMARIA {00,01,02} · SECUNDARIA {03,04,05} ·
MEDIA-SUPERIOR {06,07} · SUPERIOR {08,09,10,11}, agrupación de esta spec).

**HOGARES:** TAMLOC (`tam_loc`, mismo catálogo) · ENTIDAD (`ent`, FD id 8, 01–32).

No hay eje cruzado entre marcos (mujeres y hogares son universos y unidades distintas); un eje a la vez dentro de
cada marco.

## 4 · Estimación

Razón ponderada Σw·y/Σw con bootstrap de UPM dentro de estrato (marco propio para mujeres y para hogares; UPM
única del estrato = de certeza), receta y motor por sha256 (`tools/dominios/salud/pisos_diseno.py` +
`tools/dominios/confianza/motor_pisos.py`, misma forma que ENDISEG/MMSI §4), semilla y réplicas del contrato de
la corrida (`contrato["seed"]["valor"]`, `contrato["parametros"]["bootstrap_replicas"]`), contrato conservador
(una réplica degenerada → sin EE ni IC). Un eje a la vez; nunca cruces.

**Semilla y réplicas (para recalcular):** `numpy.PCG64(20261001)`, 2000 réplicas, bloques de 50; el valor ejecutable vive en `data/corrida0/CALC-ENADID-COLA-2018-0001/spec.yaml` (`seed`, `parametros.bootstrap_replicas`) y es este mismo.

## 5 · Controles, secuencia

Sintético en `tests/test_cola_completa_pisos_gen2.py` (`test_enadid_dos_marcos`, `test_enadid_sin_migrantes_rama_
vacia`, `test_guardia_ola_reservada_o_excluida_para` con `enadid2023_base_datos_csv`): todas las ramas terminales
por `corrida0._valida_outputs` sin NaN ni inf; prueba explícita de la rama sin soporte (ningún migrante varón →
`JEFATURA-FEMENINA-CON-MIGRANTE-VARON` sin resultado, no cero espurio); guardia que PARA si la ola 2023 (por
prefijo `enadid2023*` o `cc1_inegi_enadid_2023*`) entra como input. Ninguna ejecución diagnóstica sobre el dato:
la primera corrida es `corrida0 run`.

## 6 · Auditoría (afirma sobre México)

**Escala y unidad:** dos universos distintos en la misma pieza — proporciones de mujeres de 15–54 alguna vez
unidas (marco MUJERES) y proporciones de hogares con jefatura (marco HOGARES); ninguna cifra de un marco se
promedia o compara numéricamente con el otro (la comparación mujeres/report es de orden, declarada en §2).
**Estructura ≠ cultura:** una mayor separación entre uniones libres frente a matrimonios es primero un artefacto
de qué disoluciones producen «separada» vs. «divorciada» según el tipo de unión (el matrimonio formal tiene una
vía adicional, el divorcio, que la unión libre no distingue igual en el cuestionario), no una diferencia de
«compromiso» o «cultura» entre los dos tipos de unión. La brecha de jefatura femenina por migración masculina
(RESULT del marco HOGARES) es composicional: el hogar queda con una mujer al frente porque el varón migró, no
porque la migración «cause» un cambio de normas de género en el hogar. **Evidencia:** (a) datos primarios en
México. **Temporalidad:** RETROSPECTIVO; ninguna cifra PROSPECTIVA. **Cifra escrita a mano:** ninguna; todo
código y todo umbral de esta spec proviene del FD o del medidor citados arriba.

**Defecto medidor↔descriptor:** ninguno encontrado. Los ocho campos usados por el medidor (`p10_1`, `edad_muj`,
`tam_loc`, `niv`, `fac_per`, `est_dis`, `upm_dis` en `TMujer2`; `paren`, `sexo`, `ent`, `tam_loc`, `fac_viv`,
`est_dis`, `upm_dis` en `TSdem`; `llave_hog`, `p4_6`, `p4_15` en `TMigrante`) existen en el FD con el rango de
códigos que el medidor usa.

El primer resultado que produzca este procedimiento es el que se reporta.
