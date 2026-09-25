# Pisos por segmento ENSANUT 2021–2024 (salud, salud mental, sustancias, uso de servicios) · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-SALUD-Y-BIENESTAR-PISOS-1`, 24/sep/2026, CAJA, rama
`acto/gen2-salud-y-bienestar-pisos-1`, 0-bis `6d56f7ff`. Encargo archivado:
`forense/encargos/2026-09-24-GEN2-SALUD-Y-BIENESTAR-PISOS-1.md` (P3). CALC:
`CALC-ENSANUT-PISOS-SALUD-0001`. Congelada en el COMMIT-1, **antes** de ejecutar su medidor
sobre cualquier payload ENSANUT. **El primer resultado que produzca este procedimiento es el
que se reporta.**

## 0 · Premisas verificadas

- `[EJECUTADO]` Olas de microdato ENSANUT en `data/manifiesto.yaml`: 2006, 2012, 2016, 2018,
  2020, 2021, 2022, 2023, 2024 y 2025; la 2025 lleva `estado_reserva:
  RESERVADA-NO-ABIERTA-NO-INDEXAR-L` (24 payloads). E.6 del encargo: se reserva la última
  publicada → 2025. Esta spec no la nombra como input y el medidor para si un id reservado
  entra a su lista.
- `[EJECUTADO]` Estructura por metadatos (`pyreadstat`, `metadataonly=True`; ningún valor):
  `forense/analisis/salud-bienestar/estructura-ensanut.md` y verificación propia de nombres
  de diseño, sexo y edad en los 16 archivos (salida en la sesión del COMMIT-1). Los 16
  payloads coinciden por sha256 con el manifiesto.
- `[LEÍDO]` Un CALC ENSANUT previo: `CALC-ENSANUT-0001` (razones de no vacunación, ENSANUT
  2024). Se cita; no mide ninguna conducta de esta lista y no se repite.
- ENSANUT 2018 y 2020 quedan fuera (lista cerrada P1 §1: esquema, ventanas y reactivos
  distintos; 2020 es el cuestionario COVID) → NO-CORRIDO.

## 1 · Unidad, universo, diseño

Unidad: **persona**. Cuatro archivos por ola, cada uno con su propio universo y ponderador
`ponde_f`: adultos (seleccionado, 20+), adolescentes (seleccionado, 10–19), integrantes del
hogar (todas las edades), utilizadores de servicios de salud. Estrato de diseño `est_sel`,
UPM `upm` (se usa el par estrato+UPM como llave de conglomerado). Registro válido:
`ponde_f > 0` y estrato y UPM no vacíos; se cuentan filas totales y válidas por archivo
(`G-<ola>-<archivo>-FILAS`, `-FILAS-DISENO-VALIDO`).

Payloads (id del manifiesto): por ola, `ADUL`/`INTE`/`UTIL`/`ADOL` =
2021 `ensadul2021_entrega_w_15_12_2021`, `integrantes_ensanut2021_w_12_01_2022`,
`util2021_entrega_w_14_12_2021`, `ensadol2021_entrega_w_14_12_2021`; 2022 `ensadul2022`,
`integrantes_ensanut2022_w`, `util2022`, `ensadol2022`; 2023 `adultos_ensanut2023_w_n`,
`integrantes_ensanut2023_w_n`, `utilizadores_ensanut2023_w_n`, `adolescentes_ensanut2023_w_n`;
2024 `adultos_ensanut2024_w`, `integrantes_ensanut2024_w_icb`, `utilizadores_ensanut2024_w`,
`adolescentes_ensanut2024_w` (ids completos y sha256 en `spec.yaml`).

## 2 · Conductas y recodificación (por texto de pregunta)

La tabla completa, con texto, códigos 1 / 0 / fuera, está en
`forense/analisis/salud-bienestar/lista-cerrada-P1.md` §2 (ENSANUT) y es parte de esta spec.
Reglas que no caben en una fila:

- **CESD-7** (a0211–a0217, escala 1–4): puntos = código − 1; a0216 («¿disfrutó de la
  vida?») se invierte (3 − puntos); suma 0–21; **sintomatología depresiva** si suma ≥ 9
  (20–59 años) o ≥ 5 (60+). Si algún ítem está fuera de 1–4, la persona queda fuera.
- **ALCOHOL-EXCESIVO-30D**: hombres (`sexo` = 1) a1311 (5+ copas), mujeres (`sexo` = 2)
  a1312 (4+ copas); si a1308 ∈ {5 «No ha consumido en los últimos 12 meses», 6 «Nunca»},
  vale 0 (salto del cuestionario).
- **BUSCO-ATENCION** sólo entre h0401 = 1; **FUE-ATENDIDO** sólo entre h0404 = 1.
- **u0201**: denominador = categorías 1–26; 12 (consultorio de farmacia) y 20 (curandero,
  hierbero, naturista) no cambian de texto entre olas; el catálogo crece (23 → 25 → 26).

Universo por edad: adultos 20+ (`edad`), adolescentes 10–19, integrantes y utilizadores
todas las edades válidas.

## 3 · Ejes (uno a la vez; nunca cruces)

TOTAL · SEXO (1 HOMBRE, 2 MUJER; `h0302` en integrantes, `sexo` en los demás) · EDAD
(adultos 20–39/40–59/60+; integrantes 0–9/10–19/20–59/60+; utilizadores 0–19/20–59/60+;
adolescentes 10–14/15–19; `h0303` o `edad`) · ESTRATO (`estrato`: 1 RURAL < 2 500 hab,
2 URBANO 2 500–99 999, 3 METROPOLITANO ≥ 100 mil) · ESCOLARIDAD (`h0317a` de integrantes,
sólo 20+; en adultos y utilizadores se trae por `FOLIO_I`+`FOLIO_INT` con llaves únicas en
integrantes — no pareados en `G-<ola>-<archivo>-JOIN-SIN-INTEGRANTE`): HASTA-PRIMARIA
{1 preescolar, 2 primaria, 6 técnica con primaria}, SECUNDARIA {3, 7}, MEDIA-SUPERIOR
{4 preparatoria, 5 normal básica, 8 técnica con preparatoria}, SUPERIOR {9–12}. Adolescentes
sin ESCOLARIDAD. Sin entidad ni región (P1 §2).

## 4 · Estimación e intervalos

Por conducta, ola, eje y categoría: razón ponderada Σw·y/Σw (`-P`), N sin ponderar (`-N`).
**IC de diseño:** bootstrap de UPM con reposición dentro de estrato, UPM única del estrato
= de certeza, `PCG64(20260924)`, **2 000 réplicas** en bloques de 50, una corrida de
bootstrap por archivo y ola (todas las máscaras de ese archivo comparten réplicas);
`-EE` = desviación estándar de réplicas; `-IC-LO/-IC-HI` = percentiles 2.5/97.5; si alguna
réplica degenera (denominador 0), no se publica EE ni IC (contrato conservador de la receta
ENCIG). Código: `tools/dominios/salud/pisos_diseno.py`, input `origen: repo` por sha256,
ejecutado desde sus bytes.

**IC calibrado de persistencia** (método de `CALC-ENIF-PERSISTENCIA-IC-CALIBRADO-0001`,
spec §4, reutilizado como parámetro): grupo g = (conducta, eje). Δ = logit p(ola+1) −
logit p(ola) por categoría, para 2021→22, 22→23, 23→24, sólo con ambos p en (0, 1).
τ²_g = media de Δ² **sin centrar y sin restar ruido** (`-TAU2`, `-N-DELTAS`). Sobre el
piso **2024**: ee_m = (logit IC-HI − logit IC-LO)/(2·1.959964); IC calibrado =
expit(logit p ± 1.959964·√(ee_m² + τ²_g)) (`-ICC-LO/-ICC-HI`). Sin Δ definido o sin IC
en (0, 1) → NO-ESTIMABLE. Se publica como parámetro; aquí no se evalúa contra ninguna R
(el encargo no evalúa prospectivamente).

## 5 · Controles, oro, secuencia (D-22)

- Sintético: todas las ramas terminales (con soporte, conducta sin soporte en una ola,
  categoría vacía, réplica degenerada, sin Δ) pasan `corrida0._valida_outputs` sin NaN ni
  inf: `tests/test_salud_pisos_gen2.py`.
- Oro: **no hay** piso GEN2 sellado previo de estas conductas (búsqueda en
  `data/corrida0/` por `ENSANUT`: 1 CALC, de otra conducta). Se declara; la receta de
  bootstrap es la de ENCIG, cuyo contrato está probado en el sintético.
- Ejecución diagnóstica sobre microdato: **ninguna**. COMMIT-1 = esta spec + `spec.yaml` +
  `medidor.py` + receta + test; COMMIT-2 = `corrida0 run`, sello y asiento de replay.

## 6 · Auditoría (afirma sobre México)

Contadores: una corrida sellada (`cuenta_gen2: SI`, `adopta: NO`). **Escala:** todas las
cifras son proporciones de **personas**, cada una sobre el universo de su archivo; no se
comparan entre archivos (adultos 20+ vs integrantes todas las edades) sin decirlo.
**Precariedad ≠ cultura:** ATENCION-CONSULTORIO-FARMACIA y -CURANDERO miden **dónde** se
atendió quien usó servicios, no por qué; un gradiente por escolaridad o estrato describe
acceso y oferta (afiliación, distancia, costo) antes que preferencia, y la medida de
oferta que acompaña es BUSCO-ATENCION y FUE-ATENDIDO por el mismo eje. **Diagnóstico ≠
prevalencia:** DX-DIABETES y DX-HIPERTENSION son diagnóstico previo autorreportado; su
gradiente por escolaridad o estrato mezcla enfermedad con acceso a quien diagnostique.
**Firewall genético:** ningún eje es étnico ni hereditario; alcohol y tabaco se describen
por segmento social, nunca por ascendencia. **Sobre-generalización urbana:** ESTRATO
separa lo rural (< 2 500). **PROSPECTIVA/RETROSPECTIVA:** son pisos descriptivos; nada se
evalúa aquí. **Cifra escrita a mano:** ninguna; los cortes CESD-7 vienen de la validación
citada en P1 y se fijan antes del dato.

El primer resultado que produzca este procedimiento es el que se reporta.
