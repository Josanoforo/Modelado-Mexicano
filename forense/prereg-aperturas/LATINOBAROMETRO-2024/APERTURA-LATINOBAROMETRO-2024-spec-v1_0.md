# Expediente de apertura · Latinobarómetro 2024 (México) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito. Entorno de redacción: NUBE, sin corpus montado; no se leyó
microdato, ficha técnica, cuestionario ni comunicado de 2024.

## 0 · Premisas

- [LEÍDO] Dos contendientes sellados declaran la ola reservada como no-input en su `spec.yaml`:
  `CALC-LATINOBAROMETRO-PISOS-2023-0001` (l. 25: «2023 abierta; 2024 RESERVADA (E.6), no es input») y
  `CALC-LATINOBAROMETRO-COLA-2023-0001` (l. 24, misma frase). Ambos con `sello.json` (commit `bf5fc5e7`,
  27/sep/2026) y `resultados.json`; ambos leen `latinobarometro2023_bd_stata_zip`, filas `idenpa = 484`.
  Regla 6: ningún contendiente nuevo.
- [EJECUTADO] Payload de microdato: `latinobarometro2024_bd_stata` (manifiesto por id con `yaml.CSafeLoader`:
  `archivo: latinobarometro2024_bd_stata.zip`, sha256 `469a94c5…1f5e97`, `formato`: «ZIP con microdato Stata
  (.dta, esp/eng) y cuestionarios PDF»; `usado_para: sin uso asignado`; sin campo `raiz`, es decir la raíz por
  defecto del corpus). Su `nota` (REPORTADO por el acto que lo descargó) nombra los miembros
  `Latinobarometro_2024_Stata_esp/eng_v20250817.dta` y dice que el `.dta` no se abrió. `latinobarometro2024_cuestionario_esp`
  y `latinobarometro2024_fichas_tecnicas` son documentación (PDF), no payload.
- [EJECUTADO] **Hallazgo:** `latinobarometro2024_bd_stata` no lleva `estado_reserva` en `data/manifiesto.yaml`
  (222 de 7 198 entradas lo llevan; esta no) y `tools/corpus_loader.motivo_reserva` devuelve `''` para su id.
  La reserva **la declara la spec sellada de los contendientes** (E.6: «toda ola nueva de una encuesta con
  historia nace RESERVADA»), no el manifiesto; por eso no figura aún en `data/corrida0/aperturas-pendientes-v1_0.tsv`.
- [EJECUTADO] Ninguno de los 390 `spec.yaml` de `data/corrida0/` ni ningún `medidor.py` contiene el id
  `latinobarometro2024_bd_stata` (`grep -l` por id).
- [SUPUESTO→rama prevista] Nombres de columna y códigos de 2024 no se conocen aquí (NUBE): se fijan **sobre la ola
  del piso, 2023** (las tablas de los medidores sellados), rotulado así. Latinobarómetro renumera preguntas entre
  olas con frecuencia (SUPUESTO, no verificado en el corpus: no hay otra ola abierta con la que comparar); el
  riesgo principal es un nombre presente con otra pregunta, y lo resuelve §5.

## 1 · Estimandos

Por cada contendiente, conducta y categoría de cada eje: **R = Σw·y / Σw** en las filas de México de 2024,
y = 1/0 según la tabla (todo otro código, incluidos no sabe/no responde, queda fuera). Códigos fijados sobre 2023:

| contendiente | conducta | columna (2023) | 1 | 0 |
|---|---|---|---|---|
| PISOS | CONFIANZA-INTERPERSONAL | `P9STGBS` | 1 | 2 |
| PISOS | CONFIA-FFAA | `P13STGBS_A` | 1,2 | 3,4 |
| PISOS | CONFIA-POLICIA | `P13STGBS_B` | 1,2 | 3,4 |
| PISOS | CONFIA-IGLESIA | `P13ST_C` | 1,2 | 3,4 |
| PISOS | CONFIA-CONGRESO | `P13ST_D` | 1,2 | 3,4 |
| PISOS | CONFIA-GOBIERNO | `P13ST_E` | 1,2 | 3,4 |
| PISOS | CONFIA-PODER-JUDICIAL | `P13ST_F` | 1,2 | 3,4 |
| PISOS | CONFIA-PARTIDOS | `P13ST_G` | 1,2 | 3,4 |
| PISOS | CONFIA-INSTITUCION-ELECTORAL | `P13ST_H` | 1,2 | 3,4 |
| PISOS | CONFIA-PRESIDENTE | `P13ST_I` | 1,2 | 3,4 |
| PISOS | CATOLICO | `S1` | 1 | 2–14, 96, 97 |
| PISOS | SIN-RELIGION | `S1` | 13, 14, 97 | 1–12, 96 |
| PISOS | PRACTICANTE | `S1A` | 1,2 | 3,4 |
| PISOS | DEMOCRACIA-PREFERIBLE | `P10STGBS` | 1 | 2,3 |
| PISOS | AUTORITARISMO-A-VECES-PREFERIBLE | `P10STGBS` | 2 | 1,3 |
| PISOS | NO-IMPORTA-GOBIERNO-NO-DEMOCRATICO | `P18STM_B` | 1,2 | 3,4 |
| PISOS | APOYARIA-GOBIERNO-MILITAR | `P20STM` | 1 | 2 |
| PISOS | PREFIERE-SOCIEDAD-DE-COSTUMBRES | `P19N` | 1 | 2 |
| PISOS | TRABAJA-POR-COMUNIDAD | `P44ST_B` | 1,2 | 3,4 |
| PISOS | FIRMO-PETICION | `P45ST_A` | 1 | 2,3 |
| PISOS | ASISTIO-MANIFESTACION | `P45S_B` | 1 | 2,3 |
| COLA | SATISFECHO-CON-LA-VIDA | `P1ST` | 1,2 | 3,4 |
| COLA | SATISFECHO-CON-LA-DEMOCRACIA | `P11STGBS_A` | 1,2 | 3,4 |
| COLA | APRUEBA-GOBIERNO-DEL-PRESIDENTE | `P15STGBS` | 1 | 2 |

Ejes (uno a la vez, los mismos en los dos contendientes): TOTAL (TODOS); SEXO `sexo` 1 HOMBRE, 2 MUJER; EDAD
`edad` 18–29/30–44/45–59/60-MAS; ESCOLARIDAD `REEEDUC_1` 1–3 HASTA-BASICA, 4–5 MEDIA, 6–7 SUPERIOR; TAMLOC
`tamciud` 1–3 MENOS-20MIL, 4–6 20MIL-100MIL, 7–8 100MIL-MAS; CLASE-SUBJETIVA `S2` 1–2 ALTA-MEDIA-ALTA, 3 MEDIA,
4 MEDIA-BAJA, 5 BAJA. 17 categorías por conducta: **408 celdas** (357 PISOS + 51 COLA), todas con intervalo del
piso. Ids de celda: `<contendiente>-<conducta>-<eje>-<cat>`, contendiente ∈ {PISOS, COLA}.

**Apartada sin abrir** (E.6: lo que se aparta se declara y por qué): `ORO-CONFIA-GOBIERNO` de COLA. Es la misma
conducta, columna, recorte y piso que `CONFIA-GOBIERNO` de PISOS (COLA la midió como oro de reproducción, E.5);
contarla daría la misma R dos veces en k/n.

**Intervalo del piso** (lo, hi): IC de diseño IC-LO/IC-HI 2023 del contendiente (bootstrap ponderado de
entrevistas, «MAS-PONDERADO», percentiles 2.5/97.5; una sola ola abierta: no hay ICC). Punto: su P 2023. Se leen
del `resultados.json` sellado (sha256 fijado en el contrato); nada se recalcula.

## 2 · Universo, unidad, ponderador, diseño

Unidad persona. Filas de México: `idenpa = 484` (código ISO de país; el de 2023, fijado sobre la ola del piso).
Peso `wt` finito > 0 (sin estrato ni UPM, como en 2023). Universo `edad ≥ 18`. `idenpa`, `wt` o `edad` ausentes
en 2024 → PARO antes de leer una fila (sólo metadatos leídos); un eje ausente → ese eje NO-ESTIMABLE.
Payload: `latinobarometro2024_bd_stata`, miembro = el único `.dta` del zip cuyo nombre contiene `_esp` (la lista de
miembros es envoltura, A.7); si no es único, PARO. R es un punto; no se calcula IC de R.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera
de `lee_payload_reservado` → PARO. La lectura trae sólo `idenpa = 484` y sólo las columnas pedidas.
Probado por mutación sobre sintético: `tests/test_prereg_aperturas.py` y `tests/test_apertura_latinobarometro_2024.py`
(esquema de los dos contendientes: con soporte, conducta sin soporte, categoría vacía, conducto `medir()` completo
sobre un zip con `.dta` esp/eng y filas de otro país, PARO sin peso o sin `.dta` español).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del piso y R finitos. **Primaria** (una sola, para los dos contendientes): cobertura
k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si
0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si
n = 0. Orden si dos filas pudieran satisfacerse: NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO (excluyentes por
construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado (= CALC contendiente; las celdas
de 2024 comparten muestra) y error absoluto medio punto-del-piso vs R.
B-bis: CALIBRADO = pisos 2023 **corroborados en alcance** para 2024; SOBRECUBRE = pisos **acotados**; SUBCUBRE = el
piso 2023 no anticipa 2024. Prevista: el IC de una sola ola sin τ² (y sin efecto de diseño: MAS-PONDERADO) no
incluye el cambio entre olas ni la varianza de conglomerado; SUBCUBRE es la expectativa a priori y se declara ahora.
Una apertura sirve a todos los sellados antes (E.6): los dos contendientes entran juntos con esta única comparación.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- Regla fijada: **columna ausente en 2024 → esa conducta (o ese eje) sale NO-ESTIMABLE** (se omite R; no se
  recodifica ad hoc).
- Nombre presente con otra pregunta: la receta (paso 3, preflight documental con
  `latinobarometro2024_cuestionario_esp`, que no es abrir) compara, para cada columna de la tabla §1, el texto de
  pregunta y los códigos de 2024 contra 2023. Si alguno no casa, la apertura **no corre con v1.0**: se re-sella una
  v1.1 de esta spec y del medidor antes de abrir (mapeando el nombre por texto de pregunta o quitando la conducta),
  y se declara. Con la numeración de Latinobarómetro, esta rama es probable y es la que protege la reserva.
- El zip 2024 trae dos `.dta` (español e inglés; REPORTADO por el manifiesto): se usa el español, como en 2023
  (`Latinobarometro_2023_Esp_Stata_v1_0.dta`).

## 6 · Salidas

`RESULT-APERTURA-LATINOBAROMETRO-2024-<contendiente>-<conducta>-<eje>-<cat>-R` (408), `-DICTAMEN`, `-K`, `-N`,
`-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE,
Wilson y MAE cuando n = 0.

Contrato: `APERTURA-LATINOBAROMETRO-2024-spec.yaml` en formato `corrida0` (calc_id
`CALC-APERTURA-LATINOBAROMETRO-2024-0001`; payload con sha del manifiesto; los dos medidores sellados, sus
`resultados.json`, `motor_pisos.py`, la guardia y la plantilla común como inputs `origen: repo` con sha).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: los contendientes se sellaron (27/sep/2026) antes de que exista R; la ola sigue sin
  abrir. Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona**; nada se promedia con hogar, delito o trámite. Escala: proporción 0..1; «mucha o algo» de
  confianza (1–4) no se compara con «6 ó 7» de LAPOP (1–7) sin función de enlace; se compara «R dentro del IC del
  piso»; el MAE es descriptivo.
- Procedencia (§3): **(a)** datos primarios en México (entrevistas a residentes). Los constructos son **(c)** marcos
  importados de cultura política comparada (preferencia por la democracia, confianza institucional à la
  Almond-Verba/Inglehart): «la democracia es preferible» o «apoyaría un gobierno militar» son respuestas a un fraseo
  con equivalencia transnacional no demostrada; se leen como opinión declarada, no como carácter autoritario.
- Segmentación: un eje a la vez; TAMLOC aproxima lo rural (MENOS-20MIL) y CLASE-SUBJETIVA es clase **declarada**,
  no ingreso: el sesgo de clase media urbana no se corrige aquí y se declara. Sin muestra indígena propia.
- Estructura ≠ cultura: baja confianza en policía, partidos o jueces es evaluación de instituciones con desempeño
  medible (impunidad, victimización), adaptación racional posible; la aprobación presidencial es coyuntura (2024 es
  año de elección y cambio de gobierno en México: hipótesis razonable de salto, no medida aquí).
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «el mexicano perdió fe en la democracia»; dice que
  el piso 2023, con su IC de muestreo, no anticipa 2024 en esa proporción de celdas.
- Cifras escritas a mano: ninguna; constantes = hashes fijados, nombres y códigos leídos de los medidores sellados,
  umbrales de la regla (0.95, z = 1.959964), declarados antes de abrir.
