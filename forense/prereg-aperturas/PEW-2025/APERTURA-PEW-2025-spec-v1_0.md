# Expediente de apertura · Pew Global Attitudes Spring 2025 (México) · spec humana v1.0

ACTO `GEN2-APERTURAS-PREREGISTRADAS-1` (29/sep/2026), rama `claude/new-session-bhqoo8`, 0-bis `68b3c611`.
Esta spec basta para recalcular sin leer el código (D-15). **Nada se abre aquí**: la ola sigue
RESERVADA (E.6); la levanta el código congelado de este expediente, en caja, en el commit que
mesa autorice, o mesa por escrito. Entorno de redacción: NUBE, sin corpus montado; no se leyó
microdato, topline, short-read ni comunicado de 2025.

## 0 · Premisas

- [LEÍDO] Tres contendientes sellados declaran la ola reservada como no-input en su `spec.yaml`:
  `CALC-PEW-RELIGION-2024-0001` (l. 24: «2024 abierta; 2025 RESERVADA (E.6), no es input»),
  `CALC-PEW-PISOS-RELIGION-AUTORIDAD-0001` (l. 25: «2013-2024 abiertas; 2025 RESERVADA (E.6), no es input»),
  `CALC-PEW-MIGRACION-MEX-0001` (l. 24: «Pew GAS Spring 2025 (E.6): no es input»). Los tres tienen
  `sello.json` (commit `bf5fc5e7`, 27/sep/2026) y `resultados.json`. Regla 6: ningún contendiente nuevo.
- [EJECUTADO] Payload de microdato: `pew_gas_spring2025` (manifiesto por id con `yaml.CSafeLoader`:
  `archivo: UNIVERSO-2026-09/PEW/pew_gas_spring2025.zip`, `raiz: descargas_mx`, sha256 `ad04923a…4c2e62`,
  `usado_para`: «Pew Global Attitudes Mexico, microdato completo»). `pew_gas2025_social_trust_topline` (PDF) y
  `pew_gas2025_social_trust_shortread` (HTML) son publicaciones con cifras de la ola reservada: **no son payload
  y no se leen** (E.6: los tabulados y comunicados de una ola reservada tampoco se leen).
- [EJECUTADO] **Hallazgo:** `pew_gas_spring2025` no lleva `estado_reserva` en `data/manifiesto.yaml`
  (222 de 7 198 entradas lo llevan; esta no) y `tools/corpus_loader.motivo_reserva` devuelve `''` para su id
  (ningún patrón de `RESERVA_FUERA_DEL_MANIFIESTO` la cubre). La reserva **la declara la spec sellada de los
  contendientes** (E.6: «toda ola nueva de una encuesta con historia nace RESERVADA»), no el manifiesto; por eso
  este expediente no figura aún en `data/corrida0/aperturas-pendientes-v1_0.tsv`. La receta (paso 4a) no tiene
  custodia que levantar: `raiz: descargas_mx`.
- [EJECUTADO] Ninguno de los 390 `spec.yaml` de `data/corrida0/` contiene el id `pew_gas_spring2025`
  (`grep -l` por id); sólo dos medidores lo nombran, y para rechazarlo en su guardia de inputs
  (`CALC-PEW-RELIGION-2024-0001`: `EXCLUIDOS_PREFIJO`; `CALC-PEW-MIGRACION-MEX-0001`: `_RESERVADA`).
- [SUPUESTO→rama prevista] Los nombres de columna y códigos de 2025 no se conocen aquí (NUBE, sin corpus): se fijan
  **sobre la ola del piso** de cada conducta (las tablas de los medidores sellados), rotulado así; la diferencia se
  resuelve en el preflight documental de la receta (paso 3) y en §5.

## 1 · Estimandos

Por cada contendiente, conducta y categoría de cada eje que el contendiente publica:
**R = Σw·y / Σw** en las filas de México de Pew 2025, y = 1/0 según la tabla (todo otro código, incluidos
no sabe/no responde, queda fuera). Códigos de la ola del piso (columna «piso»), fijados sobre esa ola:

| contendiente | conducta | columna | 1 | 0 | piso | ejes | celdas | intervalo del piso |
|---|---|---|---|---|---|---|---|---|
| RELIGION2024 | CATOLICO | `religion_christian`=1 entre `religion_combined` ∈ {1..7, 99} | 1 | resto válido | 2024 | T/S/E/ESC | 11 | IC 11 |
| RELIGION2024 | SIN-RELIGION | `religion_combined`=7 entre ∈ {1..7, 99} | 7 | resto válido | 2024 | T/S/E/ESC | 11 | IC 11 |
| RELIGION2024 | CAMBIO-DE-RELIGION | `religion_switch` | 1 | 2 | 2024 | T/S/E/ESC | 11 | IC 11 |
| RELIGION2024 | CREE-EN-DIOS | `god` | 1 | 2 | 2024 | T/S/E/ESC | 11 | IC 11 |
| PISOS | RELIGION-MUY-IMPORTANTE | `religion_import` | 1 | 2,3,4 | 2024 | T/S/E/ESC | 11 | ICC 7 · IC 4 |
| PISOS | ORA-DIARIO | `pray_several` | 1,2 | 3..7 | 2017 | T/S/E/ESC | 11 | IC 11 |
| PISOS | CONFIANZA-INTERPERSONAL | `trustpeople` | 1 | 2,3 | 2017 | T/S/E/ESC | 11 | ninguno (0) |
| PISOS | CONFIA-GOBIERNO-NACIONAL | `trust_gov` | 1,2 | 3,4 | 2017 | T/S/E/ESC | 11 | IC 11 |
| PISOS | GOBIERNO-MILITAR-BUENO | `polsys_junta` | 1,2 | 3,4 | 2024 | T/S/E/ESC | 11 | ICC 11 |
| PISOS | LIDER-FUERTE-BUENO | `polsys_autocracy` | 1,2 | 3,4 | 2024 | T/S/E/ESC | 11 | ICC 11 |
| PISOS | EXPERTOS-DECIDEN-BUENO | `polsys_technocracy` | 1,2 | 3,4 | 2024 | T/S/E/ESC | 11 | ICC 11 |
| MIGRACION | IRIA-A-VIVIR-A-EEUU | `mex_live_us` | 1 | 2 | 2018 | T/S/E | 7 | ICC 7 |
| MIGRACION | IRIA-SIN-AUTORIZACION-ENTRE-QUIENES-IRIAN | `mex_wo_auth` (sólo si `mex_live_us`=1) | 1 | 2 | 2017 | T/S/E | 7 | ICC 6 · IC 1 |
| MIGRACION | EN-EEUU-SE-VIVE-MEJOR | `us_better_life` | 1 | 2,3 | 2023 | T/S/E | 7 | ICC 7 |
| MIGRACION | CONTACTO-REGULAR-CON-PARIENTES-O-AMIGOS-EN-EL-EXTRANJERO | `friends_abroad` | 1 | 2 | 2017 | T/S/E | 7 | ICC 7 |
| MIGRACION | RECIBE-DINERO-DE-PARIENTES-EN-EL-EXTRANJERO | `receive_money` | 1,2 | 3 | 2018 | T/S/E | 7 | ICC 7 |
| MIGRACION | BUENO-PARA-MEXICO-QUE-VIVAN-EN-EEUU | `good_live_us` | 1 | 2 | 2018 | T/S/E | 7 | IC 7 |

Total: **163 celdas** (44 + 77 + 42); 152 con intervalo del piso. T = TOTAL (TODOS); S = SEXO; E = EDAD;
ESC = ESCOLARIDAD. Ids de celda: `<contendiente>-<conducta>-<eje>-<cat>` con contendiente ∈ {RELIGION2024, PISOS,
MIGRACION}.

**Ola del piso** (regla fijada antes de abrir): la última ola del contendiente con la conducta y con P TOTAL finito
en su `resultados.json` sellado; si ninguna lo tiene, la última ola con la conducta y sus celdas quedan sin
intervalo (no se puntúan; su R se reporta). Así ORA-DIARIO y CONFIA-GOBIERNO-NACIONAL toman 2017 (2018/2023 y 2024
salen con N = 0 en el contendiente) y CONFIANZA-INTERPERSONAL (N = 0 en su única ola, 2017) no se puntúa.
Es la regla de piso que el propio `CALC-PEW-MIGRACION-MEX-0001` declara («piso = última ola con la pregunta»),
aplicada a los tres.

**Intervalo del piso** (lo, hi): ICC-LO/ICC-HI (IC calibrado de persistencia) si el contendiente lo publica finito
para esa celda en la ola del piso; si no, su IC de diseño IC-LO/IC-HI (bootstrap, percentiles 2.5/97.5). Punto del
piso: su P. Nada se recalcula: se lee del `resultados.json` sellado (sha256 fijado en el contrato).

## 2 · Universo, unidad, ponderador, diseño

Unidad persona. Filas de México: código de la variable `country` cuya etiqueta de valor es «Mexico» (sin distinguir
mayúsculas; regla que el docstring del contendiente de migración ya declara); si no identifica exactamente un código,
PARO antes de leer una fila. Peso `weight` finito > 0 (sin estrato ni UPM: R es un punto). Edad `age`:
RELIGION2024 y MIGRACION 18–97 (98/99 = no sabe/no responde fuera); PISOS ≥ 18 (su regla sellada; 98/99 caen en
60-MAS, como en su piso). Ejes: SEXO (1 HOMBRE, 2 MUJER), EDAD 18–29/30–44/45–59/60-MAS (60–97 en MIGRACION),
ESCOLARIDAD `d_educ_mexico` 1–3 HASTA-PRIMARIA, 4–5 SECUNDARIA, 6–9 MEDIA-SUPERIOR, 10–12 SUPERIOR.
Columnas de diseño, primera presente de cada lista (nombres de las olas del piso): país `country`; peso `weight`;
edad `age`; sexo `gender`, `sex`; escolaridad `d_educ_mexico`, `d_educ_mexico_2017`. País, peso o edad ausentes →
PARO (sólo metadatos leídos); sexo o escolaridad ausentes → ese eje NO-ESTIMABLE.
Payload: `pew_gas_spring2025` (zip con un único miembro `.sav`). R es un punto; no se calcula IC de R.

## 3 · Agregador y guardia (E.6)

Único agregador: `guardia_apertura.proporcion_por_grupo` — UNA variable de agrupación por llamada; un cruce
levanta `ParoDeGuardia`. Antes de leer un byte, `medir()` corre `auditoria_ast` sobre su propio archivo:
`groupby`/`value_counts` con dos llaves, `crosstab`, `pivot`, `pivot_table`, `unstack` o una lectura fuera
de `lee_payload_reservado` → PARO. La lectura trae sólo las filas de México y sólo las columnas pedidas.
Probado por mutación sobre sintético: `tests/test_prereg_aperturas.py` (las mutaciones de
`expediente_apertura.MUTACIONES` + borrado de la llamada a la auditoría; ramas terminales por
`corrida0._valida_outputs`) y `tests/test_apertura_pew_2025.py` (esquema de los tres contendientes: con soporte,
conducta sin soporte, categoría vacía, alias de columnas, conducto `medir()` completo sobre un `.sav` en zip con
filas de otro país, PARO sin peso o sin «Mexico»).

## 4 · Regla y umbral de adjudicación (fijados antes de abrir)

Celda puntuada: lo, hi del piso y R finitos. **Primaria** (una sola, para los tres contendientes): cobertura
k/n = #celdas con lo ≤ R ≤ hi, con IC de Wilson al 95 %. Dictamen de vocabulario cerrado: **CALIBRADO** si
0.95 ∈ Wilson; **SUBCUBRE** si Wilson_hi < 0.95; **SOBRECUBRE** si Wilson_lo > 0.95; **NO-ESTIMABLE** si
n = 0. Si dos filas pudieran satisfacerse a la vez, manda NO-ESTIMABLE > SUBCUBRE > SOBRECUBRE > CALIBRADO
(excluyentes por construcción). Secundarias, descriptivas, no adjudican: cobertura por conglomerado
(= CALC contendiente: las celdas de 2025 comparten muestra), por fuente de intervalo (ICC / IC) y error absoluto
medio punto-del-piso vs R.
B-bis: CALIBRADO = pisos **corroborados en alcance** para 2025; SOBRECUBRE = pisos **acotados** (intervalos
conservadores); SUBCUBRE = los pisos no anticipan la ola. Prevista: las celdas con IC de diseño (sin τ²) tienden a
SUBCUBRIR porque su IC no incluye el cambio entre olas; se declara ahora y no se corrige después.
Una apertura sirve a todos los sellados antes (E.6): los tres contendientes entran juntos, con esta única
comparación; ninguno se aparta.

## 5 · Diferencias con la ola del piso (se declaran al abrir, no se corrigen)

- [LEÍDO] Los nombres mnemónicos (`religion_import`, `trust_gov`, `polsys_*`, `pray_several`) son idénticos en
  2017, 2023 y 2024 del contendiente; los de migración pasaron de `qNNN` (2013/2015) a mnemónicos (2017+). El sexo
  se llama `sex` en 2017–2023 y `gender` en 2024; el código de país de México cambia en cada ola (25, 21, 20, 15,
  24, 35): por eso se identifica por etiqueta.
- 2025 puede no traer una o varias conductas (varias sólo se preguntaron en una ola). Regla fijada: **columna
  ausente → esa conducta sale NO-ESTIMABLE** (se omite R; no se recodifica ad hoc). Si el preflight documental
  (receta, paso 3: cuestionario/libro de códigos de 2025, que no es abrir) muestra que un nombre **presente** trae
  otro texto de pregunta u otros códigos, la apertura **no corre con v1.0**: se re-sella una v1.1 de esta spec y del
  medidor antes de abrir (quitando esa conducta o mapeando el nombre por texto de pregunta), y se declara.
- Diseño: 2024 del contendiente no traía estrato ni UPM; si 2025 los trae, no cambian R (punto).

## 6 · Salidas

`RESULT-APERTURA-PEW-2025-<contendiente>-<conducta>-<eje>-<cat>-R` (163), `-DICTAMEN`, `-K`, `-N`,
`-WILSON-LO/HI`, `-MAE-PUNTO`, `-MARCA` (= PROSPECTIVA). Ningún None/NaN fuera de R de celdas NO-ESTIMABLE,
Wilson y MAE cuando n = 0.

Contrato: `APERTURA-PEW-2025-spec.yaml` en formato `corrida0` (calc_id `CALC-APERTURA-PEW-2025-0001`; payload con
sha del manifiesto; los tres medidores sellados, sus `resultados.json`, `motor_pisos.py`, la guardia y la plantilla
común como inputs `origen: repo` con sha). La apertura es copiarlo a
`data/corrida0/CALC-APERTURA-PEW-2025-0001/spec.yaml` y correr (receta).

## 7 · Módulo de auditoría (v2.16; afirma qué se medirá sobre México)

- Contadores movidos por este expediente: **cero** (no mide, no abre, no adopta).
- PROSPECTIVA por construcción: los tres contendientes se sellaron (27/sep/2026) antes de que exista R; la ola
  sigue sin abrir. Ninguna frase mezcla esta cobertura con marcadores RETROSPECTIVOS.
- Unidad: **persona** en R y en los pisos; nada se promedia con hogar, delito o trámite. Escala: proporción 0..1;
  se compara «R dentro del intervalo del piso» (cobertura), no punto contra punto; el MAE es descriptivo. Las
  proporciones de «muy importante» (1–4) no se comparan con las de LAPOP o Latinobarómetro sin función de enlace.
- Procedencia (§3): **(a)** datos primarios en México (entrevistas a residentes en México; no es diáspora ni
  muestra mexicano-americana). Los constructos son **(c)** marcos importados de encuesta comparada estadounidense
  (religiosidad declarada, «sistemas de gobierno», intención migratoria): «religión muy importante» o «un líder
  fuerte sería bueno» miden respuesta a un fraseo traducido, no moral ni autoritarismo de carácter; sin crítica
  de equivalencia de traducción, la lectura es descriptiva.
- Segmentación: un eje a la vez (sexo, edad, escolaridad); **no hay eje rural ni de clase** en Pew: el sesgo de
  clase media urbana (muestra cara a cara, n ≈ 1 000, sobre-cobertura urbana posible) no se corrige aquí y se
  declara. Foco rural/indígena/popular: no identificable con este instrumento.
- Estructura ≠ cultura: la intención de emigrar y recibir remesas siguen a ingreso, violencia y redes; la confianza
  en el gobierno es evaluación de desempeño. Oferta antes que preferencia no aplica (sin conducta de mercado).
- Qué sería peligroso leído simplista: un SUBCUBRE no dice que «los mexicanos se volvieron menos religiosos»; dice
  que el piso de la ola anterior, con su intervalo, no anticipa 2025 en esa proporción de celdas. 2025 es también el
  primer año del segundo gobierno Trump (hipótesis razonable, no medida aquí): el cambio en conductas migratorias puede ser coyuntura bilateral.
- Cifras escritas a mano: ninguna; las constantes del medidor son hashes fijados, nombres de columna leídos de los
  medidores sellados y los umbrales de la regla (0.95 nominal, z = 1.959964), declarados antes de abrir.
